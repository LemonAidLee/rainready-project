"""RainReady township: DRAFT drainage zones (plain Python + shapely, no Blender).

Cuts the model rectangle into drainage zones along MAPPED lines only, then groups the cells by the drain or pond they
reach. Terrain is NOT used to draw edges: AR1 (11 Oct 2026) showed that D8 routing on GLO-30 fails on this plain (the
DSM climbs 13 m along the main ditch; drains have a median 0.32 m of relief). The fall of the ground enters only as the
regional direction (rises east and north-east, falls south-west; M at catchment scale, L inside the block), which
agrees with the mapped drains running west to the main ditch.

Cut lines (all OSM, via AR1 GIS files):
  council line      OSM way 1231162275 (council_line.geojson)
  trunk drain       the east-west drain chain at y ~ 300 (drains.geojson D4, D8, D20, D23-D28), from the council corner
                    to the west edge, where it meets the main ditch
  Batu Belah        Persiaran Batu Belah centreline (dual carriageway averaged)
  south line        Persiaran Sungai Keramat, continued east by Persiaran Astana / KU 2
  Jalan Meru        trunk road centreline (dual carriageway averaged), south of the trunk drain only
  centre split      unnamed residential way 739555185 (x ~ 301), extended straight to the trunk drain and south line

Also writes the two scenario features drive_scene.py shows (both INVENTED, display only):
  upstream_change   low blocks with paved aprons on open land in Z01, for "more paved land upstream"
  what_if_pond      a pond outline inside the OSM brownfield (way 1267917541) in Z06, for "a pond is added"

Status: DRAFT by Claude, 20 Oct 2026, checked by the team leader. Not an official catchment.
Run:   python plan_zones.py      ->  data/zones.json, data/zones_check.png, data/scenario_features.json
"""
import json, math, os
import numpy as np
import shapely
from shapely.geometry import LineString, Point, Polygon, MultiPolygon, box
from shapely.ops import unary_union, polygonize, polylabel

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
GIS = r"D:\Progmata\SDP\research\AR1_site_model\gis"
OUTLINE = box(-1222, -830, 1700, 608)   # the model rectangle (same as plan_town.OUTLINE)
AR1 = box(-1222, -608, 1222, 608)
TILE = 10.0                             # overlay is cut into 10 m tiles so it can follow the ground in Blender
SOURCE = ("DRAFT by Claude 20 Oct 2026: cut along mapped OSM lines (AR1 drains.geojson, roads_full_osm.geojson, "
          "council_line.geojson); grouped by the drain or pond each cell reaches. Draft; not an official catchment.")

# zone id -> (short name, drains to, route as mapped, council). Routes read OSM way directions, which usually but not
# always follow the flow: every route is [verify] until checked against imagery.
ZONES = {
    "Z01": ("Upstream, Shah Alam side", "trunk_drain",
            "Tasik Setia Alam and the drains south of it -> the one mapped drain that crosses the council line "
            "(at 3.09294 N, 101.44433 E) -> council corner -> trunk drain -> main ditch", "Shah Alam"),
    "Z02": ("North strip", "trunk_drain",
            "Second east-west ditch along Jalan Sungai Puloh (y ~ 330) and the trunk drain -> main ditch at the west "
            "edge; the main ditch itself crosses the north-west corner. At the council corner a short chain of "
            "OSM drains runs NORTH (x ~ 800, out of the model): part of the flow may leave that way [verify]", "Klang"),
    "Z03": ("West, north of Sungai Keramat", "pond_A",
            "Ditch along y ~ 74 running east -> pond A west side; south part -> the drain along Persiaran Sungai "
            "Keramat running east -> pond A south tip", "Klang"),
    "Z04": ("Pond A, centre", "pond_A",
            "Local land around pond A -> pond A. Pond A outlet: drain north along x ~ -140 to -270 -> trunk drain",
            "Klang"),
    "Z05": ("Centre-east (Sumazau estate)", "trunk_drain",
            "No internal drain mapped. ASSUMED: north / east to the trunk drain (via the drain along Jalan Meru to "
            "the council corner). Could instead go south to the Sungai Keramat drain and pond B [TBD]", "Klang"),
    "Z06": ("South-west", "pond_A",
            "No internal drain mapped. ASSUMED: north to the drain along Persiaran Sungai Keramat (on the zone's north "
            "edge, running east) -> pond A south tip [verify]", "Klang"),
    "Z07": ("South-centre (pond B)", "pond_B",
            "Drains along Sungai Keramat (running west) and north along x ~ 323 and x ~ 825 -> junction between the "
            "ponds -> pond B. A short link joins pond B to pond A: they may work as one system [verify]", "Klang"),
    "Z08": ("East, Klang side", "trunk_drain",
            "Retention pond OSM 721223351 (4.9 ha, not in the pond contract) and the drain running north-west from "
            "it, plus the drain along Jalan Meru -> council corner -> trunk drain", "Klang"),
    "Z09": ("South-east", "TBD",
            "Drains along Persiaran Astana (OSM 1329626248-50) run east, out of the model. Outlet unknown [TBD]",
            "Klang"),
}
LABEL_AT = {"Z05": (690, -170), "Z01": (1560, 370)}   # check-map / scene label positions where the default hits a pin


def proj(lon, lat):
    return ((lon - 101.436) * 111158.0, (lat - 3.09) * 110572.0)


def load(name):
    return json.load(open(os.path.join(GIS, name), encoding="utf-8"))["features"]


def line_of(f):
    cs = f["geometry"]["coordinates"]
    return [proj(*c) for c in (cs[0] if f["geometry"]["type"] == "Polygon" else cs)]


def centreline(feats, axis, lo, hi, step=10.0):
    """Average a dual carriageway (several ways) into one line, sampling along `axis` ('x' or 'y')."""
    lines = [LineString(line_of(f)) for f in feats]
    pts = []
    for v in np.arange(lo, hi + step, step):
        probe = LineString([(v, -5000), (v, 5000)]) if axis == "x" else LineString([(-5000, v), (5000, v)])
        hits = []
        for ln in lines:
            g = ln.intersection(probe)
            for p in getattr(g, "geoms", [g]):
                if isinstance(p, Point):
                    hits.append(p.y if axis == "x" else p.x)
        if hits:
            m = float(np.mean(hits))
            pts.append((v, m) if axis == "x" else (m, v))
    return pts


def extend(pts, d0, d1):
    """Extend a polyline straight past both ends (so polygonize closes the cells; dangles are dropped)."""
    (x0, y0), (x1, y1) = pts[0], pts[1]
    (xa, ya), (xb, yb) = pts[-2], pts[-1]
    n0 = math.hypot(x0 - x1, y0 - y1) or 1; n1 = math.hypot(xb - xa, yb - ya) or 1
    return ([(x0 + (x0 - x1) / n0 * d0, y0 + (y0 - y1) / n0 * d0)] + pts +
            [(xb + (xb - xa) / n1 * d1, yb + (yb - ya) / n1 * d1)])


def interp_fn(pts, axis):
    """f(v) -> the other coordinate of a line, by linear interpolation along `axis`."""
    k = 0 if axis == "x" else 1
    s = sorted(pts, key=lambda p: p[k])
    a = np.array([p[k] for p in s]); b = np.array([p[1 - k] for p in s])
    return lambda v: float(np.interp(v, a, b))


def build_lines():
    roads = load("roads_full_osm.geojson")
    drains = load("drains.geojson")
    named = lambda n: [f for f in roads if (f["properties"].get("n") or "") == n]
    council = line_of(load("council_line.geojson")[0])
    # trunk drain chain, east to west (drain index in drains.geojson, as in build_features: D01 = index 0 ... )
    chain = []
    for i in (28, 27, 25, 26, 24, 23, 8, 20, 4):
        ln = line_of(drains[i])
        if chain and math.dist(chain[-1], ln[0]) > math.dist(chain[-1], ln[-1]):
            ln = ln[::-1]
        chain += ln
    trunk = extend(chain, 80, 40)
    batu = centreline(named("Persiaran Batu Belah") + named("Persiaran Batu Belah KU5"), "y", -830, 300)
    south = centreline(named("Persiaran Sungai Keramat") + named("Persiaran Astana / KU 2"), "x", -1222, 1700)
    meru = [p for p in centreline(named("Jalan Meru"), "y", -830, 330)]
    split = line_of(next(f for f in roads if f["properties"].get("osm_id") == 739555185))
    split = sorted(split, key=lambda p: p[1])
    return dict(council=council, trunk=trunk, batu=extend(batu, 30, 60), south=extend(south, 30, 30),
                meru=extend(meru, 30, 40), split=extend(split, 60, 260)), (trunk, batu, south, meru, split)


def classify(p, f):
    """Which zone a cell belongs to, from its representative point and the side of each mapped line."""
    x, y = p.x, p.y
    if f["shah"].contains(p):
        return "Z01"
    if y > f["trunk_y"](x):
        return "Z02"
    north = y > f["south_y"](x)
    if x < f["batu_x"](y):
        return "Z03" if north else "Z06"
    if x < f["meru_x"](y):
        if north:
            return "Z04" if x < f["split_x"](y) else "Z05"
        return "Z07"
    return "Z08" if north else "Z09"


def tiles(poly):
    """Cut a polygon into TILE x TILE pieces and triangulate each, so the mesh can follow the ground."""
    out = []
    x0, y0, x1, y1 = poly.bounds
    grid = [box(x, y, x + TILE, y + TILE) for x in np.arange(math.floor(x0 / TILE) * TILE, x1, TILE)
            for y in np.arange(math.floor(y0 / TILE) * TILE, y1, TILE)]
    tree = shapely.STRtree(grid)
    prepped = shapely.prepared.prep(poly)
    for i in tree.query(poly):
        cell = grid[i]
        piece = cell if prepped.contains(cell) else cell.intersection(poly)
        for g in getattr(piece, "geoms", [piece]):
            if isinstance(g, Polygon) and g.area > 0.05:
                for t in shapely.constrained_delaunay_triangles(g).geoms:
                    out.append([[round(a, 2), round(b, 2)] for a, b in list(t.exterior.coords)[:3]])
    return out


def spots():
    """Same placement rule as build_features.build_pins: a point on the mapped street near its middle."""
    roads = load("roads.geojson")
    out = {}
    for k, key in enumerate(("Makyong", "Sumazau", "Batu Belah"), start=1):
        pts = [proj(*ll) for f in roads if key in (f["properties"].get("n") or "")
               for ll in f["geometry"]["coordinates"]]
        pts = [p for p in pts if abs(p[0]) <= 1222 and abs(p[1]) <= 608]
        cx, cy = np.mean([p[0] for p in pts]), np.mean([p[1] for p in pts])
        out[f"SPOT {k}"] = min(pts, key=lambda q: math.dist(q, (cx, cy)))
    return out


def main():
    cut, (trunk, batu, south, meru, split) = build_lines()
    parts = [LineString(v).intersection(OUTLINE.buffer(40)) for v in cut.values()]
    noded = unary_union(parts + [OUTLINE.boundary])
    cells = [c.intersection(OUTLINE) for c in polygonize(noded)]
    cells = [c for c in cells if c.area > 1.0]
    # side of the council line: the piece of (council line + rectangle) that holds the Area A label point
    shah = next(c for c in polygonize(unary_union([parts[0], OUTLINE.boundary])) if c.contains(Point(1380, 470)))
    f = dict(shah=shah, trunk_y=interp_fn(trunk, "x"), south_y=interp_fn(south, "x"), batu_x=interp_fn(batu, "y"),
             meru_x=interp_fn(meru, "y"), split_x=lambda y: 301.5)
    groups = {}
    for c in cells:
        groups.setdefault(classify(c.representative_point(), f), []).append(c)
    water = []
    for n in ("water.geojson", "water_supplement.geojson"):
        for w in load(n):
            if w["properties"]["a"] >= 1000:
                water.append((w["properties"]["id"], Polygon(line_of(w)).buffer(0), w["properties"]["w"]))
    pond_of = {399570465: "pond_A", 359496461: "pond_B", 164881251: "water_tasik_setia_alam"}
    zones = []
    for zid in sorted(ZONES):
        g = unary_union(groups.get(zid, [])).buffer(0)
        wet = unary_union([w for _, w, _ in water]).intersection(g)
        dry = g.difference(unary_union([w for _, w, _ in water])).buffer(0)
        name, to, route, council = ZONES[zid]
        holds = [f"{pond_of.get(i, f'water_{i}')} ({t})" for i, w, t in water if w.intersection(g).area > 1500]
        main_poly = max(getattr(dry, "geoms", [dry]), key=lambda p: p.area)
        lab = Point(LABEL_AT[zid]) if zid in LABEL_AT else polylabel(main_poly, tolerance=2.0)
        rings = [[[round(x, 2), round(y, 2)] for x, y in p.exterior.coords] for p in getattr(g, "geoms", [g])]
        zones.append(dict(
            id=zid, name=name, drains_to=to, route=route, council=council,
            area_ha=round(g.area / 1e4, 2), water_area_ha=round(wet.area / 1e4, 2),
            in_ar1_extent_pct=round(100 * g.intersection(AR1).area / g.area, 1),
            holds_water=holds, label=[round(lab.x, 1), round(lab.y, 1)], outline=rings, tris=tiles(dry)))
        print(f"{zid} {name:32s} {g.area / 1e4:7.2f} ha  water {wet.area / 1e4:5.2f} ha  -> {to:12s} "
              f"tris {len(zones[-1]['tris'])}  holds {holds}")
    total = sum(z["area_ha"] for z in zones)
    print("total", round(total, 2), "ha; model rectangle", round(OUTLINE.area / 1e4, 2), "ha")
    sp = spots()
    for k, p in sp.items():
        hit = [z["id"] for z in zones if any(Polygon(r).contains(Point(p)) for r in z["outline"])]
        print(k, [round(v) for v in p], hit)
    os.makedirs(DATA, exist_ok=True)
    json.dump(dict(note="DRAFT drainage zones, not an official catchment. " + SOURCE, source=SOURCE,
                   cut_lines={k: [[round(x, 2), round(y, 2)] for x, y in v] for k, v in cut.items()},
                   spots={k: list(p) for k, p in sp.items()}, zones=zones),
              open(os.path.join(DATA, "zones.json"), "w", encoding="utf-8"))
    check_map(zones, sp)
    scenario_features(zones)


def scenario_features(zones):
    """Invented display geometry for the two scenario switches; nothing here is mapped or proposed."""
    plan = json.load(open(os.path.join(DATA, "town_plan.json"), encoding="utf-8"))
    kept = json.load(open(os.path.join(DATA, "kept_features.json"), encoding="utf-8"))
    zp = {z["id"]: unary_union([Polygon(r) for r in z["outline"]]) for z in zones}
    water = unary_union([Polygon(line_of(w)).buffer(0) for n in ("water.geojson", "water_supplement.geojson")
                         for w in load(n)])
    blocks = unary_union([Polygon(b["ring"]).buffer(0) for b in plan["blocks"]])
    blds = unary_union([Polygon(b["ring"]).buffer(0) for b in plan["buildings"]] +
                       [Polygon(b["ring"]).buffer(0) for b in kept["buildings"] if len(b["ring"]) >= 3])
    trees = unary_union([Point(t[0], t[1]).buffer(5.0, 6) for t in plan["trees"]])
    # 1. upstream change: 22 x 14 m low blocks on 30 x 22 m paved aprons, wherever a whole apron fits on open land
    free = (zp["Z01"].intersection(blocks).buffer(-5.0)
            .difference(blds.buffer(6.0)).difference(water.buffer(10.0)).difference(trees))
    fp = shapely.prepared.prep(free)
    x0, y0, x1, y1 = free.bounds
    up = []
    for k, x in enumerate(np.arange(x0, x1 - 30, 31.0)):
        for y in np.arange(y0, y1 - 22, 23.0):
            apron = box(x, y, x + 30, y + 22)
            if fp.contains(apron):
                roof = box(x + 4, y + 4, x + 26, y + 18)
                up.append(dict(apron=[list(c) for c in apron.exterior.coords][:-1],
                               roof=[list(c) for c in roof.exterior.coords][:-1], h=[5.0, 7.0, 9.0][(k + len(up)) % 3]))
    # 2. what-if pond: inside the brownfield, 20 m clear of its edge and of trees, rounded
    bf = next(f for f in load("landuse_osm.geojson") if f["properties"]["osm_id"] == 1267917541)
    site = Polygon(line_of(bf)).buffer(0).intersection(zp["Z06"]).buffer(-20.0).difference(trees).difference(blds.buffer(6))
    site = max(getattr(site, "geoms", [site]), key=lambda p: p.area)
    pond = site.buffer(-12.0).buffer(10.0, 8).simplify(1.5)
    pond = max(getattr(pond, "geoms", [pond]), key=lambda p: p.area)
    out = dict(note="INVENTED display geometry for the scenario switches (drive_scene.py). Not mapped, not a proposal.",
               upstream_change=up,
               what_if_pond=dict(ring=[[round(a, 2), round(b, 2)] for a, b in pond.exterior.coords][:-1],
                                 area_m2=round(pond.area), osm_landuse=1267917541,
                                 centre=[round(pond.centroid.x, 1), round(pond.centroid.y, 1)]))
    json.dump(out, open(os.path.join(DATA, "scenario_features.json"), "w", encoding="utf-8"))
    print("upstream change blocks:", len(up), "| what-if pond", round(pond.area), "m2 at",
          [round(v) for v in pond.centroid.coords[0]])


def check_map(zones, sp):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as MPoly
    fig, ax = plt.subplots(figsize=(20, 11.5))
    tint = {"pond_A": "#d9d4c7", "pond_B": "#cfd6d2", "trunk_drain": "#e8e6e1", "TBD": "#f3f1ec"}
    for z in zones:
        for r in z["outline"]:
            ax.add_patch(MPoly(r, closed=True, fc=tint[z["drains_to"]], ec="#333", lw=2.2, zorder=1))
    for fe in load("roads_full_osm.geojson"):
        g = LineString(line_of(fe)).intersection(OUTLINE)
        for s in getattr(g, "geoms", [g]):
            if not s.is_empty:
                x, y = s.xy
                ax.plot(x, y, color="#b5b5b5", lw=0.5 if fe["properties"]["c"] in ("residential", "service") else 1.4,
                        zorder=2)
    for i, fe in enumerate(load("drains.geojson") + load("drains_supplement.geojson")):
        g = LineString(line_of(fe)).intersection(OUTLINE)
        for s in getattr(g, "geoms", [g]):
            if not s.is_empty:
                x, y = s.xy
                ax.plot(x, y, color="#1f5fbf", lw=2.6 if i == 11 else 1.6, zorder=3)
                # arrow in the OSM way direction (usually, not always, the flow direction)
                if s.length > 60:
                    a = s.interpolate(0.5, normalized=True); b = s.interpolate(min(1, 0.5 + 15 / s.length), normalized=True)
                    ax.annotate("", xy=(b.x, b.y), xytext=(a.x, a.y), zorder=4,
                                arrowprops=dict(arrowstyle="-|>", color="#1f5fbf", lw=1.2, mutation_scale=14))
    for n in ("water.geojson", "water_supplement.geojson"):
        for w in load(n):
            if w["properties"]["a"] >= 1000:
                p = Polygon(line_of(w)).intersection(OUTLINE)
                for q in getattr(p, "geoms", [p]):
                    if not q.is_empty:
                        ax.add_patch(MPoly(list(q.exterior.coords), closed=True, fc="#7fb3e6", ec="#1f5fbf", lw=1,
                                           zorder=3))
    for lab, xy in (("POND A", (-135, -90)), ("POND B", (-100, -530))):
        ax.text(*xy, lab, ha="center", va="center", fontsize=10, weight="bold", color="#0b2f66", zorder=6)
    c = LineString(line_of(load("council_line.geojson")[0])).intersection(OUTLINE)
    for s in getattr(c, "geoms", [c]):
        x, y = s.xy
        ax.plot(x, y, color="#7a1fa2", lw=2.2, ls=(0, (6, 3)), zorder=5)
    ax.text(1240, 590, "council line (OSM, not cadastral)", color="#7a1fa2", fontsize=9, va="top", zorder=6)
    ax.text(1430, 380, "SHAH ALAM side", color="#7a1fa2", fontsize=9, ha="center", zorder=6)
    ax.text(1430, 270, "KLANG side", color="#7a1fa2", fontsize=9, ha="center", zorder=6)
    ax.plot(926, 325, marker="o", ms=11, mfc="none", mec="#7a1fa2", mew=2, zorder=6)
    ax.annotate("only mapped drain crossing\nthe council line (D31)", xy=(926, 325), xytext=(1010, 220), fontsize=8,
                color="#7a1fa2", arrowprops=dict(arrowstyle="->", color="#7a1fa2"), zorder=6)
    for k, p in sp.items():
        ax.plot(*p, marker="v", color="#2b2f7a", ms=10, zorder=6)
        ax.text(p[0] + 12, p[1] + 12, k, color="#2b2f7a", fontsize=9, weight="bold", zorder=6)
    for z in zones:
        to = {"pond_A": "pond A", "pond_B": "pond B", "trunk_drain": "trunk drain", "TBD": "outlet TBD"}[z["drains_to"]]
        ax.text(*z["label"], f"{z['id']}\n{z['name']}\n{z['area_ha']:.1f} ha -> {to}", ha="center", va="center",
                fontsize=9, zorder=7, bbox=dict(fc="white", ec="#333", lw=0.8, alpha=0.92))
    ax.set_xlim(-1222, 1700); ax.set_ylim(-830, 608); ax.set_aspect("equal")
    ax.set_xlabel("x east (m), origin 3.0900 N 101.4360 E"); ax.set_ylabel("y north (m)")
    ax.set_title("RainReady model - DRAFT drainage zones (20 Oct 2026). Edges follow mapped "
                 "roads, drains and the council line; NOT an official catchment.\nBlue arrows = OSM way direction "
                 "(usually the flow, not always). Shading = where each zone drains (A / B / trunk / TBD). "
                 "Areas measured on plan, incl. water.", fontsize=11)
    ax.text(-1210, -820, "Data: OpenStreetMap contributors (ODbL), via AR1 GIS files. Check map only; no depths.",
            fontsize=8, color="#555")
    plt.savefig(os.path.join(DATA, "zones_check.png"), dpi=110, bbox_inches="tight")


if __name__ == "__main__":
    main()
