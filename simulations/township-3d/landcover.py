"""RainReady township: land cover and runoff coefficient C per drainage zone (plain Python + shapely, 21 Oct 2026).

MSMA 2nd Edition (DID 2012), Chapter 2, Table 2.5 gives runoff coefficients by land use, and Equation 2.4 area-weights
them: C_avg = sum(C_j * A_j) / sum(A_j). The design ARI here is 100 years (major system, Table 1.1), so the
"Major System (> 10 year ARI)" column is used. Verified against the page images of the official PDF, 21 Oct 2026.

Every block of land between roads (data/town_plan.json) is classed:
  built block (buildings cover >= 15 % of it)  -> link and terrace house 0.90, or commercial 0.95 where OSM tags the
                                                  land commercial / retail / industrial or the block holds shophouses
  open block                                   -> OSM park / recreation ground: park 0.40; OSM construction /
                                                  brownfield: bare soil 0.60; anything else: grass cover 0.50
Land outside the blocks is road reserve (roads and highways 0.95). Water bodies count as detention ponds with an
outlet (0.95).
Upstream change: the land under the invented upstream-change aprons in Z01 (data/scenario_features.json) becomes
commercial 0.95, the same change the 3D scene shows.

LIMITS: the town fabric is a SIMULATED layout loosely based on BBR (its built footprint is capped to the estimate for
real BBR), so these C values describe the model town, not surveyed land cover. Confidence M (table) / L (cover).
Run:  python landcover.py   ->  data/landcover.json
"""
import json, os
from shapely.geometry import Polygon
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
GIS = r"D:\Progmata\SDP\research\AR1_site_model\gis"
C_MAJOR = {"terrace": 0.90, "commercial": 0.95, "park": 0.40, "bare": 0.60, "grass": 0.50, "road": 0.95,
           "water": 0.95}
SOURCE = ("MSMA 2nd Ed. (DID 2012) Table 2.5, Major System column (> 10 yr ARI), area-weighted by Eq. 2.4; land cover "
          "from the simulated model town (landcover.py)")
BUILT_SHARE = 0.15


def proj(lon, lat):
    return ((lon - 101.436) * 111158.0, (lat - 3.09) * 110572.0)


def poly(f):
    g = f["geometry"]
    rings = g["coordinates"] if g["type"] == "Polygon" else [r for p in g["coordinates"] for r in p][:1]
    return Polygon([proj(*c) for c in rings[0]]).buffer(0)


def main():
    plan = json.load(open(os.path.join(DATA, "town_plan.json"), encoding="utf-8"))
    kept = json.load(open(os.path.join(DATA, "kept_features.json"), encoding="utf-8"))
    zones = json.load(open(os.path.join(DATA, "zones.json"), encoding="utf-8"))["zones"]
    feats = json.load(open(os.path.join(DATA, "scenario_features.json"), encoding="utf-8"))
    landuse = json.load(open(os.path.join(GIS, "landuse_osm.geojson"), encoding="utf-8"))["features"]
    water = unary_union([poly(w) for n in ("water.geojson", "water_supplement.geojson")
                         for w in json.load(open(os.path.join(GIS, n), encoding="utf-8"))["features"]
                         if w["properties"]["a"] >= 1000])
    lu = {k: unary_union([poly(f) for f in landuse if f["properties"]["use"] in v] or [Polygon()])
          for k, v in {"commercial": {"commercial", "retail", "industrial"}, "park": {"park", "recreation_ground"},
                       "bare": {"construction", "brownfield"}}.items()}
    blds = [Polygon(b["ring"]).buffer(0) for b in kept["buildings"] if len(b["ring"]) >= 3]
    shops = [Polygon(b["ring"]).buffer(0) for b in plan["buildings"] if b["kind"] == "shophouse"]
    blds += [Polygon(b["ring"]).buffer(0) for b in plan["buildings"]]
    all_blds, all_shops = unary_union(blds), unary_union(shops)
    up = unary_union([Polygon(b["apron"]) for b in feats["upstream_change"]])
    classed = []                                    # (class, polygon) for every block, water removed
    for b in plan["blocks"]:
        g = Polygon(b["ring"]).buffer(0).difference(water)
        if g.is_empty:
            continue
        share = g.intersection(all_blds).area / g.area
        if share >= BUILT_SHARE:
            com = g.intersection(lu["commercial"]).area > 0.5 * g.area or g.intersection(all_shops).area > 0
            classed.append(("commercial" if com else "terrace", g))
        else:
            parts = [("park", g.intersection(lu["park"])), ("bare", g.intersection(lu["bare"]).difference(lu["park"]))]
            rest = g.difference(lu["park"]).difference(lu["bare"])
            classed += [(k, p) for k, p in parts + [("grass", rest)] if not p.is_empty]
    blocks_all = unary_union([p for _, p in classed])
    out = {}
    for z in zones:
        zp = unary_union([Polygon(r) for r in z["outline"]]).buffer(0)
        area = {k: 0.0 for k in C_MAJOR}
        area["water"] = zp.intersection(water).area
        for k, p in classed:
            area[k] += p.intersection(zp).area
        area["road"] = max(0.0, zp.area - area["water"] - zp.intersection(blocks_all).area)
        c_now = sum(C_MAJOR[k] * a for k, a in area.items()) / zp.area
        # upstream change: the aprons' land becomes commercial (only Z01 holds them)
        moved = {k: 0.0 for k in C_MAJOR}
        for k, p in classed:
            moved[k] += p.intersection(zp).intersection(up).area
        a_up = dict(area)
        for k, a in moved.items():
            a_up[k] -= a
        a_up["commercial"] += sum(moved.values())
        c_up = sum(C_MAJOR[k] * a for k, a in a_up.items()) / zp.area
        out[z["id"]] = dict(area_ha=round(zp.area / 1e4, 2), c_now=round(c_now, 3), c_upstream=round(c_up, 3),
                            cover_ha={k: round(a / 1e4, 2) for k, a in area.items()},
                            upstream_paved_ha=round(sum(moved.values()) / 1e4, 2))
        print(f"{z['id']}  C now {c_now:.3f}  upstream {c_up:.3f}  ", {k: round(a / 1e4, 1) for k, a in area.items()})
    json.dump(dict(note="Runoff coefficient per draft zone. " + SOURCE, c_major=C_MAJOR, built_share=BUILT_SHARE,
                   zones=out), open(os.path.join(DATA, "landcover.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
