"""RainReady township: 2D town plan (plain Python + shapely, no Blender).

Turns the OSM road centrelines into one clean road network (uniform widths, rounded junctions, pavements, kerbs,
markings), cuts the land between roads into blocks, and lays out a tidy town in the empty parts of each block:
terrace rows with back lanes, taller shophouses along main roads, parks in very large empty areas, green pockets in
leftover scraps, and street and park trees. Real features are kept and avoided: the sketch's and AR1's buildings, the
ponds, the drains and the sketch's parks.

EVERYTHING THIS SCRIPT ADDS IS INVENTED for a clean simulated township (team leader, 20 Oct 2026). The flood features
(ponds, ditch, drains, council line, flood spots) stay from AR1 / OSM.

Run by build_town.py (or by hand):  python plan_town.py
Reads  data/kept_features.json (exported from Blender) and AR1 GIS files; writes data/town_plan.json and
data/town_plan.png.
"""
import json, math, os, random
import shapely
from shapely import affinity
from shapely.geometry import LineString, Point, Polygon, MultiPolygon, box, mapping
from shapely.ops import unary_union, substring
from shapely.prepared import prep
from shapely.strtree import STRtree

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
GIS = r"D:\Progmata\SDP\research\AR1_site_model\gis"
EXTENT = (1222.0, 608.0)
OUTLINE = box(-1222, -830, 1700, 608)   # the model rectangle (team leader, 20 Oct 2026); AR1 extent is the part |y|<=608, |x|<=1222

# carriageway and pavement widths (m), ASSUMED by class; same carriageway widths as style_scene.py
ROAD_W = {"motorway": 22, "trunk": 18, "primary": 14, "secondary": 12, "tertiary": 10, "unclassified": 6.5,
          "residential": 7, "service": 5, "motorway_oneway": 11, "trunk_oneway": 9, "link": 7}
WALK_W = {"trunk": 3.0, "trunk_oneway": 2.5, "primary": 3.0, "secondary": 3.0, "tertiary": 2.5, "unclassified": 2.0, "residential": 2.0}
MAJOR = {"trunk", "trunk_oneway", "primary", "secondary", "tertiary"}
SERVICE_MIN_LEN = 120.0           # shorter service ways (driveways, car-park aisles) are dropped for a clean look
SECTION_TOP = {"main": 9.0, "ditch": 3.0, "drain": 1.5}

# town layout (m)
LOT, DEPTH, LANE = 6.5, 14.0, 8.0     # terrace lot width, depth, back-lane width
GROUP = 10                            # lots per terrace row before a gap
SETBACK = 3.0                         # from the pavement edge
SHOP_BAND = 35.0                      # within this of a main road, buildings are 3-storey shophouses
H_TERRACE, H_SHOP = 7.0, 11.0
MIN_FILL = 1500.0                     # smaller empty pieces become green pockets
PARK_OVER = 40000.0                   # empty pieces bigger than this get a building ring around a park
PARK_RING = 40.0                      # depth of that building ring
# Building budget, matched to the real amount (team leader, 20 Oct 2026). AR1: OSM maps 606 buildings / 141,000 m2 in
# the extent, about 40-60 % of what stands, so real footprint ~235,000-353,000 m2. Kept buildings already give
# ~205,000 m2, so new fill inside the extent is capped here (upper part of the range: the unmapped west estates
# are dense terraces).
BUDGET_M2 = 120000.0
WEST_ESTATES = box(-1222, -608, -300, 608)   # AR1 imagery check: whole estates here, almost none mapped
BUILD_USES = {"residential", "commercial", "retail"}
PARK_USES = {"park", "recreation_ground"}
VACANT_USES = {"construction", "brownfield"}
# road markings: (offset, dashed) per class; see build_features.MARKINGS (same rules)
MARKINGS = {
    "motorway_oneway": [(-1.8, True), (1.8, True), (-5.0, False), (5.0, False)],
    "motorway": [(0.0, False), (-5.5, True), (5.5, True), (-10.3, False), (10.3, False)],
    "trunk": [(0.0, False), (-4.5, True), (4.5, True), (-8.3, False), (8.3, False)],
    "trunk_oneway": [(0.0, True), (-4.0, False), (4.0, False)],
    "primary": [(0.0, True), (-6.4, False), (6.4, False)],
    "secondary": [(0.0, True), (-5.4, False), (5.4, False)],
    "tertiary": [(0.0, True), (-4.4, False), (4.4, False)],
    "unclassified": [(0.0, True)], "residential": [(0.0, True)],
    "link": [(-3.0, False), (3.0, False)],
}
DASH, GAP, LINE_W = 3.0, 5.0, 0.3
rnd = random.Random(20261020)


def proj(lon, lat):
    return ((lon - 101.436) * 111158.0, (lat - 3.09) * 110572.0)


def load(name):
    p = os.path.join(GIS, name)
    return json.load(open(p, encoding="utf-8"))["features"] if os.path.exists(p) else []


def polys(g):
    if g is None or g.is_empty:
        return []
    if isinstance(g, Polygon):
        return [g]
    return [p for p in getattr(g, "geoms", []) if isinstance(p, Polygon)] + \
           [q for p in getattr(g, "geoms", []) if not isinstance(p, Polygon) for q in polys(p)]


def tris(g, seg=8.0):
    """Constrained triangulation of (multi)polygons, edges no longer than `seg` so the mesh can follow the ground."""
    out = []
    for p in polys(g):
        p = shapely.segmentize(p.buffer(0), seg)
        for t in shapely.constrained_delaunay_triangles(p).geoms:
            c = list(t.exterior.coords)[:3]
            out.append([[round(x, 2), round(y, 2)] for x, y in c])
    return out


def rings(g):
    out = []
    for p in polys(g):
        out.append([[round(x, 2), round(y, 2)] for x, y in p.exterior.coords])
    return out


# ---------------------------------------------------------------- roads
# all OSM roads over the whole model area if fetched (roads_full_osm.geojson), else AR1 roads + supplement
feats = load("roads_full_osm.geojson") or (load("roads.geojson") + load("roads_supplement.geojson"))
roads = []
for f in feats:
    c = f["properties"]["c"]
    line = LineString([proj(*ll) for ll in f["geometry"]["coordinates"]])
    if line.length < 1 or not line.intersects(OUTLINE):
        continue
    if c == "service" and line.length < SERVICE_MIN_LEN:
        continue
    roads.append((c, line))
road_area = unary_union([l.buffer(ROAD_W.get(c, 6) / 2, quad_segs=4) for c, l in roads]).intersection(OUTLINE)
walk_outer = unary_union([l.buffer(ROAD_W.get(c, 6) / 2 + WALK_W[c], quad_segs=4) for c, l in roads if c in WALK_W])
walk_area = walk_outer.intersection(OUTLINE).difference(road_area)
streets = unary_union([road_area, walk_area])
major_lines = unary_union([l for c, l in roads if c in MAJOR])

# ---------------------------------------------------------------- kept features (to avoid)
kept = json.load(open(os.path.join(DATA, "kept_features.json"), encoding="utf-8"))
existing = [Polygon(b["ring"]) for b in kept["buildings"] if len(b["ring"]) >= 3]
existing = [p.buffer(0) for p in existing if p.area > 1]
sketch_parks = unary_union([Polygon(r).buffer(0) for r in kept["sketch_parks"] if len(r) >= 3])
ponds = unary_union([Polygon([proj(*ll) for ll in f["geometry"]["coordinates"][0]]).buffer(0)
                     for f in load("water.geojson") + load("water_supplement.geojson")
                     if f["properties"]["a"] >= 1000]).intersection(OUTLINE)
main_id = load("main_ditch.geojson")[0]["geometry"]["coordinates"][0]
drain_buf = []
for f in load("drains.geojson") + load("drains_supplement.geojson"):
    cs = f["geometry"]["coordinates"]
    kind = "main" if abs(cs[0][0] - main_id[0]) < 1e-5 and abs(cs[0][1] - main_id[1]) < 1e-5 else f["properties"]["c"]
    drain_buf.append(LineString([proj(*ll) for ll in cs]).buffer(SECTION_TOP.get(kind, 1.5) / 2 + 4))
drain_core = unary_union([g.buffer(-3.5) for g in drain_buf])   # the channel itself (buffer added 4 m)
walk_area = walk_area.difference(drain_core.buffer(0.5))          # pavements stop at drains; roads cross them
streets = unary_union([road_area, walk_area])
exclude = unary_union([unary_union([p.buffer(5) for p in existing]), ponds.buffer(15), unary_union(drain_buf),
                       sketch_parks.buffer(2)])
existing_u = unary_union(existing)

# ---------------------------------------------------------------- blocks and fill
lu = [(f["properties"]["use"], Polygon([proj(*ll) for ll in f["geometry"]["coordinates"][0]]).buffer(0))
      for f in load("landuse_osm.geojson")]
build_land = unary_union([p for u, p in lu if u in BUILD_USES] or [Polygon()])
park_land = unary_union([p for u, p in lu if u in PARK_USES] or [Polygon()])
vacant_land = unary_union([p for u, p in lu if u in VACANT_USES] or [Polygon()])
blocks = [b for b in polys(OUTLINE.difference(streets)) if b.area > 150]
inner = OUTLINE.buffer(-8)
new_bld, lanes, trees, paths, green, parks, block_out = [], [], [], [], [], [], []


def orient(poly):
    r = poly.minimum_rotated_rectangle
    cs = list(r.exterior.coords)
    best = max(((cs[i], cs[i + 1]) for i in range(4)), key=lambda e: math.dist(*e))
    return math.degrees(math.atan2(best[1][1] - best[0][1], best[1][0] - best[0][0]))


def fill_rows(P, ang, origin):
    """Terrace rows (back-to-back pairs with a back lane) inside polygon P, aligned to angle `ang`."""
    R = affinity.rotate(P, -ang, origin=origin)
    pr = prep(R)
    minx, miny, maxx, maxy = R.bounds
    made, y = [], miny + 1.0
    while y + 2 * DEPTH <= maxy + DEPTH:
        used = []
        for k in (0, 1):
            y0 = y + k * DEPTH
            run = []
            x = minx
            while x + LOT <= maxx:
                ok = pr.contains(box(x, y0 + 0.25, x + LOT, y0 + DEPTH - 0.25))
                if ok:
                    run.append(x)
                if (not ok or x + 2 * LOT > maxx) and run:
                    for g in range(0, len(run), GROUP + 1):
                        grp = run[g:g + GROUP]
                        if len(grp) >= 3:
                            b = box(grp[0], y0 + 0.25, grp[-1] + LOT, y0 + DEPTH - 0.25)
                            made.append(b); used.append(b.bounds)
                    run = []
                x += LOT
        if used:
            x0, x1 = min(u[0] for u in used), max(u[2] for u in used)
            lane = box(x0, y + 2 * DEPTH, x1, y + 2 * DEPTH + LANE).intersection(R)
            if lane.area > 80:
                lanes.append(affinity.rotate(lane, ang, origin=origin))
        y += 2 * DEPTH + LANE
    return [affinity.rotate(b, ang, origin=origin) for b in made]


def scatter_trees(P, spacing, kind, limit=None, per=1800):
    """Clustered tree points inside P (park look): cluster centres, a few trees around each."""
    pts = []
    pr = prep(P)
    minx, miny, maxx, maxy = P.bounds
    centres = [(rnd.uniform(minx, maxx), rnd.uniform(miny, maxy)) for _ in range(int(P.area / per) + 1)]
    for cx, cy in centres:
        for _ in range(rnd.randint(4, 9)):
            x, y = cx + rnd.gauss(0, 12), cy + rnd.gauss(0, 12)
            if pr.contains(Point(x, y)) and all(math.dist((x, y), q[:2]) > spacing for q in pts[-30:]):
                pts.append((x, y, rnd.uniform(0.7, 1.05), kind))
    return pts[:limit] if limit else pts


def park_from(piece, kind="park"):
    """Defined open land: a park (paths + clusters) when large, otherwise a lawn with sparse tree clusters."""
    if piece.area > PARK_OVER or kind == "park":
        parks.append(piece)
        trees.extend(scatter_trees(piece.buffer(-4), 10, "park", per=3600))
        for lp in polys(piece.buffer(-14)):
            if lp.area > 2000:
                paths.append(lp.exterior)
    elif kind == "vacant":
        green.append(piece)   # construction / brownfield: open field, a few trees along the edge
        edge = piece.buffer(-4).exterior if not piece.buffer(-4).is_empty and piece.buffer(-4).geom_type == "Polygon" else None
        if edge:
            for d in range(0, int(edge.length), 40):
                q = edge.interpolate(d); trees.append((q.x, q.y, rnd.uniform(0.7, 0.95), "green"))
    else:
        green.append(piece)
        trees.extend(scatter_trees(piece.buffer(-3), 10, "green", per=9000))


# 1. collect fillable pieces with a priority; 2. fill in priority order until the footprint budget is used;
# 3. everything left becomes defined open land (park, lawn or vacant field)
cands, opens = [], []
for bi, b in enumerate(blocks):
    P = b.buffer(-SETBACK).intersection(inner).difference(exclude)
    for piece in polys(P):
        if piece.area < MIN_FILL:
            if piece.area > 200:
                green.append(piece)
                trees.extend(scatter_trees(piece.buffer(-2), 9, "green", limit=4))
            continue
        lu_build = piece.intersection(build_land)
        lu_park = piece.intersection(park_land).difference(build_land)
        lu_vacant = piece.intersection(vacant_land).difference(build_land)
        rest = piece.difference(unary_union([build_land, park_land, vacant_land]))
        for q in polys(lu_build):
            if q.area >= MIN_FILL:
                cands.append((0, q.centroid.distance(existing_u), q, bi))
        for q in polys(lu_park):
            opens.append((q, "park"))
        for q in polys(lu_vacant):
            opens.append((q, "vacant"))
        for q in polys(rest):
            if q.area < MIN_FILL:
                continue
            if WEST_ESTATES.contains(q.centroid):
                cands.append((1, q.centroid.distance(existing_u), q, bi))   # unmapped estates (AR1 imagery check)
            else:
                opens.append((q, "lawn"))
cands.sort(key=lambda c: (c[0], c[1]))
used = 0.0
for prio, _, q, bi in cands:
    in_frame = q.centroid.x <= EXTENT[0] and abs(q.centroid.y) <= EXTENT[1]
    if used >= BUDGET_M2:
        opens.append((q, "lawn")); continue
    b = blocks[bi]
    if q.area > PARK_OVER:   # big piece: ring of buildings around a park
        rows = fill_rows(q.difference(q.buffer(-PARK_RING)), orient(b), b.centroid)
        for pk in polys(q.buffer(-PARK_RING - 4)):
            park_from(pk, "park")
    else:
        rows = fill_rows(q, orient(b), b.centroid)
    new_bld.extend(rows)
    if in_frame:
        used += sum(r.area for r in rows)
for q, kind in opens:
    park_from(q, kind)
for b in blocks:
    block_out.append({"ring": rings(b)[0], "area": round(b.area)})
print("new building footprint in the AR1 extent: %.0f m2 (budget %.0f)" % (used, BUDGET_M2))

# trees around the ponds (like the sketch), and inside the sketch's parks
for p in polys(ponds):
    ring = p.buffer(9).exterior
    for d in range(0, int(ring.length), 21):
        q = ring.interpolate(d)
        if inner.contains(q) and not streets.contains(q) and not existing_u.buffer(3).contains(q):
            trees.append((q.x, q.y, rnd.uniform(0.75, 1.0), "pond"))
for p in polys(sketch_parks):
    if p.area > 600:
        trees.extend(scatter_trees(p.buffer(-3), 9, "park"))

# street trees on the pavements, every 12 m, kept clear of junctions
road_tree = STRtree([l for _, l in roads])
for c, l in roads:
    if c not in WALK_W:
        continue
    off = ROAD_W[c] / 2 + WALK_W[c] / 2
    for side in (1, -1):
        try:
            ol = l.offset_curve(side * off, quad_segs=2)
        except Exception:
            continue
        for d in range(12, int(ol.length), 24):
            q = ol.interpolate(d)
            if not walk_area.buffer(-0.2).contains(q) or not inner.contains(q):
                continue
            near = [roads[i] for i in road_tree.query(q.buffer(14))]
            if any(o is not l and o.distance(q) < ROAD_W.get(oc, 6) / 2 + WALK_W.get(oc, 0) + 3 for oc, o in near):
                continue
            trees.append((q.x, q.y, rnd.uniform(0.58, 0.72), "street"))

# drop trees standing on buildings
all_bld = unary_union(existing + new_bld).buffer(2.5)
pb = prep(all_bld)
trees = [t for t in trees if not pb.contains(Point(t[0], t[1]))]

# heights: shophouses along main roads, terraces elsewhere
bld_out = []
for b in new_bld:
    shop = b.centroid.distance(major_lines) < SHOP_BAND
    bld_out.append({"ring": rings(b)[0], "h": H_SHOP if shop else H_TERRACE, "kind": "shophouse" if shop else "terrace"})

# ---------------------------------------------------------------- markings and kerbs
mark = []
inner_road = road_area.buffer(-0.4)
for c, l in roads:
    for off, dashed in MARKINGS.get(c, []):
        try:
            ol = l if off == 0 else l.offset_curve(off, quad_segs=2)
        except Exception:
            continue
        if ol.is_empty or ol.length < 2:
            continue
        pieces = []
        if dashed:
            d = 0.0
            while d < ol.length:
                pieces.append(substring(ol, d, min(d + DASH, ol.length)))
                d += DASH + GAP
        else:
            pieces = [ol]
        for pc in pieces:
            if pc.length > 0.5:
                mark.append(pc.buffer(LINE_W / 2, cap_style="flat"))
# junctions, merges and slip roads: where two roads' surfaces overlap, no road's markings are drawn (plus 4 m),
# so lines stop cleanly at the junction instead of crossing each other
bufs = [l.buffer(ROAD_W.get(c, 6) / 2, cap_style="flat") for c, l in roads]
btree = STRtree(bufs)
def continuation(a, b):
    """True when OSM split one street into two ways: they meet end to end and keep roughly the same direction."""
    for pa, na in ((a.coords[0], a.coords[1]), (a.coords[-1], a.coords[-2])):
        for pb, nb in ((b.coords[0], b.coords[1]), (b.coords[-1], b.coords[-2])):
            if math.dist(pa, pb) < 0.5:
                da = math.atan2(pa[1] - na[1], pa[0] - na[0])
                db = math.atan2(nb[1] - pb[1], nb[0] - pb[0])
                diff = abs((da - db + math.pi) % (2 * math.pi) - math.pi)
                if diff < math.radians(35):
                    return True
    return False


zones = []
for i, bf in enumerate(bufs):
    for j in btree.query(bf):
        if j > i and bufs[j].intersects(bf) and not continuation(roads[i][1], roads[j][1]):
            ov = bf.intersection(bufs[j])
            if ov.area > 1:
                zones.append(ov)
junctions = unary_union(zones).buffer(4) if zones else Polygon()
markings = unary_union(mark).intersection(inner_road).difference(junctions)
print("junction zones without markings: %.0f m2" % junctions.area)
kerbs = []
for p in polys(road_area):
    for r in [p.exterior] + list(p.interiors):
        kerbs.append([[round(x, 2), round(y, 2)] for x, y in shapely.segmentize(LineString(r.coords), 6).coords])

lanes_u = unary_union(lanes).difference(streets) if lanes else None
plan = {
    "note": "INVENTED town layout for the simulated township; see plan_town.py docstring.",
    "roads": tris(road_area), "walks": tris(walk_area), "lanes": tris(lanes_u) if lanes_u else [],
    "markings": tris(markings, 50), "kerbs": kerbs,
    "buildings": bld_out, "trees": [[round(t[0], 2), round(t[1], 2), round(t[2], 2), t[3]] for t in trees],
    "paths": [[[round(x, 2), round(y, 2)] for x, y in shapely.segmentize(LineString(p.coords), 6).coords] for p in paths],
    "blocks": block_out,
}
json.dump(plan, open(os.path.join(DATA, "town_plan.json"), "w"))
print("roads tris", len(plan["roads"]), "| walks", len(plan["walks"]), "| lanes", len(plan["lanes"]),
      "| marking tris", len(plan["markings"]), "| kerb rings", len(kerbs))
print("blocks", len(blocks), "| new buildings", len(bld_out),
      "(shophouse rows %d)" % sum(b["kind"] == "shophouse" for b in bld_out),
      "| trees", len(trees), "| parks", len(parks), "| green pockets", len(green))

# ---------------------------------------------------------------- check map
try:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(18, 9), dpi=100)
    from shapely.plotting import plot_polygon
    def fillp(g, **kw):
        for p in polys(g):
            plot_polygon(p, ax=ax, add_points=False, linewidth=0, facecolor=kw["color"], zorder=kw.get("zorder", 1))
    fillp(OUTLINE, color="#cfe0b8", zorder=0)
    fillp(parks and unary_union(parks), color="#9cc58a", zorder=1)
    fillp(ponds, color="#4a90d9", zorder=2)
    fillp(walk_area, color="#e8e2d6", zorder=2)
    fillp(road_area, color="#55585f", zorder=3)
    fillp(lanes_u, color="#8d9097", zorder=3)
    for p in existing:
        xs, ys = p.exterior.xy; ax.fill(xs, ys, color="#6d6f80", zorder=4)
    for b in bld_out:
        xs, ys = zip(*b["ring"]); ax.fill(xs, ys, color="#e7a96b" if b["kind"] == "shophouse" else "#f2dcb3", zorder=4)
    tx = [t[0] for t in trees]; ty = [t[1] for t in trees]
    ax.scatter(tx, ty, s=2, color="#2f6b45", zorder=5)
    ax.set_aspect("equal"); ax.set_title("Town plan: grey = kept buildings, cream = new terraces, orange = new shophouses")
    plt.tight_layout(); plt.savefig(os.path.join(DATA, "town_plan.png"))
except Exception as e:
    print("plot skipped:", e)
