"""Build a RainReady site pack automatically from open data (22 Oct 2026).

    python build_site.py <id> "<name>" <south> <west> <north> <east> [--refresh]

writes sites/<id>/: site.json (what the site is, its evidence, how it was built and how long it took), inputs.json
(network format, every value with status, source and confidence), geo.json (the map), outputs.json (network.py),
register_template.csv (for a planner to fill and upload) and source/ (the raw downloads, so a rebuild is offline).

What it does, and what each step assumes (all screening, all stated on the site):
  1. OpenStreetMap (Overpass): major roads, railways, waterways, water bodies, land use, buildings, and the council
     (admin_level 7) boundaries. OSM is incomplete (at BBR it held an estimated 40-60 % of buildings, AR1)
  2. Terrain: Copernicus GLO-30 (a surface model: buildings and trees are in it; error ~1 m or more in built-up
     areas). Used only to tell which end of a drain is lower, never for depths
  3. Ponds: JPS Selangor's pond list (data/jps_ponds_selangor.geojson) plus OSM water bodies of 0.2 ha or more.
     Capacity ASSUMED = water area x 1.5 m live storage, the same stated rule as BBR (L); a planner replaces it
  4. Drains: OSM waterways (drain, ditch, canal, stream) grouped into chains. Size ASSUMED by OSM type (L); slope
     from the terrain between the chain's ends, kept within 0.05-2 %; each chain drains to the chain or pond it meets
     at its lower end, else out of the area. Rivers are where the water leaves (the method does not model rivers)
  5. Zones: the area is cut along mapped roads, railways, waterways and council lines (as BBR's draft zones were);
     each block drains to the registered pond it touches, else to the drain on its edge or nearest to it; blocks
     with the same outlet and council are merged up to 75 ha (MSMA: Rational Method not above 80 ha)
  6. Runoff C: MSMA 2 Table 2.5 major-system values, area-weighted by Eq. 2.4 over OSM land cover, as landcover.py
     did for BBR. Upstream scenario: open and vacant land built out (0.90)
  7. Storm: the nearest MSMA 2 Table 2.B1 gauge (data/msma2_idf_selangor.json); method values as BBR's (sourced)
  8. What-if pond: the largest open parcel in a zone that drains to the most loaded pond
  9. Flood evidence: JPS Selangor flood records (2017-2024) and JPS's 2017 flash-flood list inside the area
"""
import json, math, os, sys, time, csv
from collections import defaultdict

import requests
from pyproj import Transformer
from shapely.geometry import LineString, MultiLineString, Point, Polygon, box, mapping, shape
import warnings
from shapely.ops import linemerge, polygonize, transform, unary_union
warnings.filterwarnings("ignore", category=DeprecationWarning)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import network  # noqa: E402

OVERPASS = ["https://overpass-api.de/api/interpreter", "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter", "https://overpass.private.coffee/api/interpreter"]
UA = {"User-Agent": "RainReady-site-builder/1.0 (university hackathon research on open flood data)"}
DEM_URL = ("/vsicurl/https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N{lat:02d}_00_E{lon:03d}_00_DEM/"
           "Copernicus_DSM_COG_10_N{lat:02d}_00_E{lon:03d}_00_DEM.tif")
NATIONAL = os.path.join(HERE, "..", "..", "website", "public", "data", "national.json")
BBR_INPUTS = os.path.join(HERE, "..", "township-3d", "inputs.json")

C = {"terrace": 0.90, "commercial": 0.95, "park": 0.40, "bare": 0.60, "grass": 0.50, "road": 0.95, "water": 0.95}
C_SOURCE = ("MSMA 2nd Edition (DID Malaysia, 2012), Chapter 2, Table 2.5 (major system) area-weighted by Eq. 2.4 over "
            "OpenStreetMap land cover, as landcover.py did for BBR: terrace 0.90, commercial 0.95, park 0.40, bare 0.60, "
            "grass and other open land 0.50, roads 0.95, water 0.95")
ROAD_HALF_W = {"motorway": 12, "trunk": 10, "primary": 8, "secondary": 7, "tertiary": 5,
               "motorway_link": 4, "trunk_link": 4, "primary_link": 4}
SECTIONS = {   # assumed by OSM waterway type; not measured (L)
    "ditch": (2.0, 1.0, 1.0), "drain": (3.0, 1.5, 1.5), "stream": (6.0, 3.0, 2.0), "canal": (8.0, 4.0, 2.0)}
LIVE_DEPTH_M = 1.5
MAX_ZONE_HA = 75.0
BUILT_SHARE = 0.15
COMMERCIAL = {"commercial", "retail", "industrial"}
BUILT_LU = {"residential", "commercial", "retail", "industrial", "institutional", "education", "religious",
            "military", "railway", "garages"}
PARK = {"park", "pitch", "garden", "playground", "recreation_ground", "golf_course", "village_green", "cemetery",
        "nature_reserve", "grass"}
BARE = {"construction", "brownfield", "greenfield", "landfill", "quarry"}
OPEN = {"forest", "wood", "scrub", "grassland", "meadow", "farmland", "orchard", "plantation", "wetland", "heath",
        "allotments", "farmyard"}


def a(value, unit, status, source, conf):
    return dict(value=value, unit=unit, status=status, source=source, confidence=conf)


# ------------------------------------------------------------------------------------------------ downloads
def overpass(q, path, refresh):
    if os.path.exists(path) and not refresh:
        return json.load(open(path, encoding="utf-8"))
    err = None
    for attempt in range(8):           # public servers are often overloaded: rotate through them
        url = OVERPASS[attempt % len(OVERPASS)]
        try:
            r = requests.post(url, data={"data": q}, timeout=300, headers=UA)
            if r.ok and r.text.lstrip().startswith("{") and '"remark": "runtime error' not in r.text[:2000]:
                open(path, "w", encoding="utf-8").write(r.text)
                return r.json()
            err = f"{url}: {r.status_code} {r.text[:120]!r}"
        except requests.RequestException as e:
            err = f"{url}: {e}"
        print("  overpass retry:", err)
        time.sleep(5)
    raise RuntimeError(f"Overpass failed: {err}")


def fetch(src, bb, refresh):
    s, w, n, e = bb
    b = f"{s},{w},{n},{e}"
    main = overpass(f"""[out:json][timeout:240];(
      way[highway~"^(motorway|trunk|primary|secondary|tertiary|motorway_link|trunk_link|primary_link)$"]({b});
      way[railway~"^(rail|light_rail|subway)$"]({b});
      way[waterway~"^(river|stream|canal|drain|ditch)$"]({b});
      way[natural=water]({b}); rel[natural=water]({b});
      way[landuse]({b}); rel[landuse]({b});
      way[leisure~"^(park|pitch|golf_course|garden|playground|recreation_ground|nature_reserve)$"]({b});
      way[natural~"^(wood|scrub|grassland|wetland|heath)$"]({b});
    );out geom;""", os.path.join(src, "osm.json"), refresh)
    bld = overpass(f'[out:json][timeout:240];way[building]({b});out geom;', os.path.join(src, "buildings.json"), refresh)
    adm = overpass(f'[out:json][timeout:240];rel[boundary=administrative][admin_level=7]({b});out geom;',
                   os.path.join(src, "councils.json"), refresh)
    return main, bld, adm


def dem_sampler(src, bb, refresh):
    """Copernicus GLO-30 window around the area, cached as a small .npy; returns z(lon, lat), the median of 3x3."""
    import numpy as np
    path = os.path.join(src, "dem_glo30.npz")
    if not os.path.exists(path) or refresh:
        import rasterio
        from rasterio.merge import merge
        s, w, n, e = bb
        # every 1-degree tile the area touches (a site can straddle a whole degree, e.g. 3.0 N)
        tiles = [DEM_URL.format(lat=la, lon=lo) for la in range(int(math.floor(s - 0.005)), int(math.floor(n + 0.005)) + 1)
                 for lo in range(int(math.floor(w - 0.005)), int(math.floor(e + 0.005)) + 1)]
        dss = [rasterio.open(t) for t in tiles]
        try:
            mosaic, t = merge(dss, bounds=(w - 0.005, s - 0.005, e + 0.005, n + 0.005))
        finally:
            for ds in dss:
                ds.close()
        arr = mosaic[0]
        np.savez_compressed(path, z=arr, t=np.array([t.a, t.b, t.c, t.d, t.e, t.f]))
    d = np.load(path)
    z, (ta, tb, tc, td, te, tf) = d["z"], d["t"]

    def at(lon, lat):
        col, row = int((lon - tc) / ta), int((lat - tf) / te)
        win = z[max(0, row - 1):row + 2, max(0, col - 1):col + 2]
        return float(np.median(win)) if win.size else float("nan")
    return at


# ------------------------------------------------------------------------------------------------ geometry
def way_line(el):
    return LineString([(p["lon"], p["lat"]) for p in el["geometry"]]) if len(el.get("geometry", [])) >= 2 else None


def way_poly(el):
    g = el.get("geometry", [])
    if len(g) >= 4 and g[0] == g[-1]:
        p = Polygon([(q["lon"], q["lat"]) for q in g])
        return p if p.is_valid else p.buffer(0)
    return None


def rel_poly(el):
    outer = [LineString([(q["lon"], q["lat"]) for q in m["geometry"]]) for m in el.get("members", [])
             if m.get("type") == "way" and m.get("role", "outer") in ("outer", "") and len(m.get("geometry", [])) >= 2]
    inner = [LineString([(q["lon"], q["lat"]) for q in m["geometry"]]) for m in el.get("members", [])
             if m.get("type") == "way" and m.get("role") == "inner" and len(m.get("geometry", [])) >= 2]
    if not outer:
        return None
    polys = list(polygonize(unary_union(outer)))
    if not polys:
        return None
    g = unary_union(polys)
    if inner:
        holes = list(polygonize(unary_union(inner)))
        if holes:
            g = g.difference(unary_union(holes))
    return g if g.is_valid else g.buffer(0)


def lonlat(geom, to_ll):
    return transform(to_ll, geom)


def r6(geom):
    """Round coordinates to 6 decimals (about 0.1 m) for a smaller geo.json."""
    def rnd(c):
        if isinstance(c, (list, tuple)) and c and isinstance(c[0], (int, float)):
            return [round(c[0], 6), round(c[1], 6)]
        return [rnd(x) for x in c]
    m = mapping(geom)
    return dict(type=m["type"], coordinates=rnd(m["coordinates"]))


# ------------------------------------------------------------------------------------------------ build
def build(site_id, name, bb, refresh=False):
    t0 = time.time()
    out_dir = os.path.join(HERE, "sites", site_id)
    src = os.path.join(out_dir, "source")
    os.makedirs(src, exist_ok=True)
    s, w, n, e = bb
    lat0, lon0 = (s + n) / 2, (w + e) / 2
    zone_utm = 32600 + int((lon0 + 180) // 6) + 1
    fwd = Transformer.from_crs(4326, zone_utm, always_xy=True).transform
    back = Transformer.from_crs(zone_utm, 4326, always_xy=True).transform

    main, bld, adm = fetch(src, bb, refresh)
    z_at = dem_sampler(src, bb, refresh)
    t_fetch = time.time() - t0

    area_ll = box(w, s, e, n)
    area = transform(fwd, area_ll)
    m = lambda g: transform(fwd, g).intersection(area)            # noqa: E731  lon/lat -> metres, clipped

    # ---- classify OSM features
    roads, rails, ways, rivers, water, lu = [], [], defaultdict(list), [], [], defaultdict(list)
    for el in main["elements"]:
        t = el.get("tags", {})
        if el["type"] == "way" and "highway" in t:
            ln = way_line(el)
            if ln is not None:
                roads.append((m(ln), t["highway"]))
        elif el["type"] == "way" and "railway" in t:
            ln = way_line(el)
            if ln is not None:
                rails.append(m(ln))
        elif el["type"] == "way" and "waterway" in t:
            ln = way_line(el)
            if ln is not None:
                g = m(ln)
                if not g.is_empty:
                    (rivers if t["waterway"] == "river" else ways[(t["waterway"], t.get("name"))]).append((g, el["id"]))
        poly = (way_poly(el) if el["type"] == "way" else rel_poly(el) if el["type"] == "relation" else None)
        if poly is None or poly.is_empty:
            continue
        pg = m(poly)
        if pg.is_empty:
            continue
        if t.get("natural") == "water" or t.get("landuse") in ("basin", "reservoir"):
            if t.get("water") not in ("river", "canal", "stream", "ditch", "drain"):
                water.append((pg, el["type"][0] + str(el["id"]), t.get("name")))
        elif t.get("landuse"):
            lu[t["landuse"]].append(pg)
        elif t.get("leisure"):
            lu[t["leisure"]].append(pg)
        elif t.get("natural"):
            lu[t["natural"]].append(pg)
    buildings = [m(p) for p in (way_poly(el) for el in bld["elements"]) if p is not None]
    buildings = [b for b in buildings if not b.is_empty]
    bld_kind = {}

    # ---- councils
    councils = []
    for el in adm["elements"]:
        g = rel_poly(el)
        if g is None:
            continue
        gm = m(g)
        if gm.area > 1e4:
            councils.append((el["tags"].get("name", f"r{el['id']}"), gm))
    council_lines = unary_union([c.boundary for _, c in councils]).intersection(area.buffer(-1)) if len(councils) > 1 \
        else LineString()

    def council_of(geom):
        p = geom.representative_point() if geom.geom_type != "Point" else geom
        for nm, c in councils:
            if c.contains(p):
                return nm
        return min(councils, key=lambda c: c[1].distance(p))[0] if councils else None

    # ---- ponds: JPS list + OSM water >= 0.2 ha
    jps = json.load(open(os.path.join(HERE, "data", "jps_ponds_selangor.geojson"), encoding="utf-8"))
    jps_in = [(m(shape(f["geometry"])), f["properties"]) for f in jps["features"]
              if shape(f["geometry"]).intersects(area_ll)]
    ponds = []
    used_jps = set()
    for g, oid, nm in water:
        if g.area < 2000:
            continue
        hit = [(jg, jp) for jg, jp in jps_in if jg.intersects(g) and jp["code"] not in used_jps]
        if hit:
            jg, jp = max(hit, key=lambda h: h[0].intersection(g).area)
            used_jps.add(jp["code"])
            ponds.append(dict(id=jp["code"], geom=g, osm=oid, name=nm, jps=jp))
        else:
            ponds.append(dict(id=f"OSM_{oid}", geom=g, osm=oid, name=nm, jps=None))
    for jg, jp in jps_in:
        if jp["code"] not in used_jps and jg.area > 500:
            used_jps.add(jp["code"])
            ponds.append(dict(id=jp["code"], geom=jg, osm=None, name=None, jps=jp))
    for p in ponds:
        p["council"] = council_of(p["geom"])
        p["z"] = z_at(*back(p["geom"].centroid.x, p["geom"].centroid.y))

    # ---- drain chains
    chains = []
    unnamed = defaultdict(list)
    for (kind, nm), parts in list(ways.items()):
        if nm and kind in ("ditch", "drain") and nm.lower().startswith(("sungai", "sg ", "sg.", "anak sungai", "parit")):
            kind = "stream"           # a named watercourse: at least stream-sized, whatever its OSM tag
        if nm:
            chains.append((kind, nm, unary_union([g for g, _ in parts]), [i for _, i in parts]))
        else:
            unnamed[kind] += parts
    for kind, parts in unnamed.items():   # connected components of unnamed ways of one type
        geoms = [g for g, _ in parts]
        merged = unary_union(geoms)
        comps = list(merged.geoms) if merged.geom_type.startswith("Multi") else [merged]
        groups = unary_union([c.buffer(1.0) for c in comps])
        for grp in (groups.geoms if groups.geom_type == "MultiPolygon" else [groups]):
            mine = [(g, i) for g, i in parts if g.intersects(grp)]
            chains.append((kind, None, unary_union([g for g, _ in mine]), [i for _, i in mine]))
    drains = []
    for k, (kind, nm, g, ids) in enumerate(sorted(chains, key=lambda c: -c[2].length)):
        if g.length < 120:
            continue
        ln = linemerge(g) if g.geom_type == "MultiLineString" else g
        ends = [Point(c) for part in (ln.geoms if ln.geom_type == "MultiLineString" else [ln]) for c in (part.coords[0], part.coords[-1])]
        zs = [(z_at(*back(p.x, p.y)), p) for p in ends]
        zs = [(zv, p) for zv, p in zs if not math.isnan(zv)]
        lo, hi = min(zs, key=lambda q: q[0]), max(zs, key=lambda q: q[0])
        slope = min(0.02, max(0.0005, (hi[0] - lo[0]) / max(g.length, 1.0)))
        drains.append(dict(id=f"D{len(drains) + 1:02d}", kind=kind, name=nm, geom=g, osm=ids, z_low=lo[0], low=lo[1],
                           z_high=hi[0], slope=slope))
    # split a drain where it crosses a council line: the upper piece drains into the lower one
    split = []
    for d in drains:
        if len(councils) > 1 and d["geom"].crosses(council_lines.buffer(0.5)) if not council_lines.is_empty else False:
            pieces = [(nm, d["geom"].intersection(c)) for nm, c in councils]
            pieces = [(nm, pg) for nm, pg in pieces if pg.length > 60]
            if len(pieces) > 1:
                def zmin(pg):
                    cs = [c for part in (pg.geoms if pg.geom_type.startswith("Multi") else [pg]) for c in part.coords]
                    return min(z_at(*back(*c)) for c in (cs[0], cs[-1]))
                pieces.sort(key=lambda q: -zmin(q[1]))
                for j, (nm, pg) in enumerate(pieces):
                    split.append(dict(d, id=f"{d['id']}{'abcdefgh'[j]}", geom=pg, council=nm, z_low=zmin(pg),
                                      chain_next=(f"{d['id']}{'abcdefgh'[j + 1]}" if j + 1 < len(pieces) else None)))
                continue
        split.append(dict(d, council=council_of(d["geom"]), chain_next=None))
    drains = split
    # where each drain goes: the next piece of its own chain, else the drain or pond it meets at its lower end
    key = {d["id"]: (d["z_low"], d["id"]) for d in drains}
    river_geom = unary_union([g for g, _ in rivers]) if rivers else None
    for d in drains:
        if d["chain_next"]:
            d["drains_to"], d["to_basis"] = d["chain_next"], "the same mapped drain, across the council line"
            continue
        low = d["low"] if d["geom"].distance(d["low"]) < 1 else d["geom"].interpolate(d["geom"].project(d["low"]))
        best = None
        for o in drains:
            if o["id"] == d["id"] or o["id"].rstrip("abcdefgh") == d["id"].rstrip("abcdefgh"):
                continue
            if key[o["id"]] < key[d["id"]] and o["geom"].distance(low) < 30:
                if best is None or o["geom"].distance(low) < best["geom"].distance(low):
                    best = o
        if best:
            d["drains_to"], d["to_basis"] = best["id"], "mapped junction at its lower end"
        elif river_geom is not None and river_geom.distance(low) < 60:
            d["drains_to"], d["to_basis"] = "outfall", "a mapped river at its lower end"
        else:
            d["drains_to"], d["to_basis"] = "outfall", "leaves the area (assumed)"
    # a drain is assumed at least as large as any drain that flows into it (OSM often tags the lower end 'ditch')
    rank = ["ditch", "drain", "stream", "canal"]
    byid = {d["id"]: d for d in drains}
    for _ in range(len(drains)):
        for d in drains:
            nxt = byid.get(d["drains_to"])
            if nxt and rank.index(d["kind"]) > rank.index(nxt["kind"]):
                nxt["kind"], nxt["upsized"] = d["kind"], d["id"]
    for p in ponds:
        near = [d for d in drains if d["geom"].distance(p["geom"]) < 150]
        if near:
            best = min(near, key=lambda d: (d["geom"].distance(p["geom"]), d["z_low"]))
            p["drains_to"], p["to_basis"] = best["id"], "nearest mapped drain within 150 m (assumed outlet)"
        else:
            p["drains_to"], p["to_basis"] = "outfall", "no mapped drain within 150 m (assumed outlet)"

    # ---- blocks: cut the area along mapped lines
    cut = [area.boundary] + [g for g, _ in roads] + rails + [d["geom"] for d in drains] + [g for g, _ in rivers]
    if not council_lines.is_empty:
        cut.append(council_lines)
    blocks = [b for b in polygonize(unary_union([c for c in cut if not c.is_empty])) if b.area > 50]
    # merge slivers (< 1 ha) into the neighbour they share most edge with
    blocks.sort(key=lambda b: b.area)
    changed = True
    while changed:
        changed = False
        for i, b in enumerate(blocks):
            if b.area >= 1e4:
                continue
            nb = [(j, o.boundary.intersection(b.boundary).length) for j, o in enumerate(blocks) if j != i]
            nb = [x for x in nb if x[1] > 0]
            if nb:
                j = max(nb, key=lambda x: x[1])[0]
                blocks[j] = blocks[j].union(b).buffer(0)
                del blocks[i]
                changed = True
                break
    # split blocks over 75 ha into strips along their long axis
    out = []
    for b in blocks:
        k = math.ceil(b.area / (MAX_ZONE_HA * 1e4))
        if k <= 1:
            out.append(b)
            continue
        x0, y0, x1, y1 = b.bounds
        vertical = (x1 - x0) >= (y1 - y0)
        for j in range(k):
            strip = box(x0 + (x1 - x0) * j / k, y0, x0 + (x1 - x0) * (j + 1) / k, y1) if vertical else \
                box(x0, y0 + (y1 - y0) * j / k, x1, y0 + (y1 - y0) * (j + 1) / k)
            piece = b.intersection(strip)
            if piece.area > 50:
                out.append(piece)
    blocks = out

    # ---- where each block drains
    def block_z(b):
        """Median terrain height over a 60 m grid inside the block (a surface model: only for which way is down)."""
        import numpy as np
        x0, y0, x1, y1 = b.bounds
        pts = [Point(x, y) for x in np.arange(x0 + 30, x1, 60) for y in np.arange(y0 + 30, y1, 60)]
        zs = [z_at(*back(p.x, p.y)) for p in pts if b.contains(p)] or [z_at(*back(*b.representative_point().coords[0]))]
        return float(np.median(zs))

    pond_union = {p["id"]: p["geom"] for p in ponds}
    targets = []
    for b in blocks:
        cn = council_of(b)
        touching = [p for p in ponds if p["geom"].distance(b) < 20 and p["council"] == cn]
        if touching:
            p = max(touching, key=lambda p: p["geom"].intersection(b.buffer(20)).area)
            targets.append((p["id"], "touches a registered or mapped pond (assumed to drain to it)", cn))
            continue
        if river_geom is not None and river_geom.distance(b) < 10:
            targets.append(("outfall", "a mapped river on its edge, where water leaves the area (rivers are not "
                                       "modelled)", cn))
            continue
        edge = [d for d in drains if d["geom"].distance(b) < 5]
        same = [d for d in edge if d["council"] == cn] or edge
        if same:
            d = min(same, key=lambda d: d["z_low"])
            targets.append((d["id"], "a mapped drain on its edge (the lowest, where there are several)", cn))
            continue
        near = sorted(drains, key=lambda d: d["geom"].distance(b))
        if near and near[0]["geom"].distance(b) < 400:
            targets.append((near[0]["id"], f"nearest mapped drain, {near[0]['geom'].distance(b):.0f} m away (assumed)", cn))
            continue
        # terrain fallback: the nearest mapped drain or pond at least 2 m lower than the block, within 2 km
        zb = block_z(b)
        lower = [(d["geom"].distance(b), d["id"], "drain") for d in drains if d["z_low"] < zb - 2] +                 [(p["geom"].distance(b), p["id"], "pond") for p in ponds if p["z"] < zb - 2]
        lower = [x for x in lower if x[0] < 2000]
        if lower:
            dist, nid, what = min(lower)
            targets.append((nid, f"no mapped drain nearby; terrain fallback: the nearest {what} at least 2 m lower, "
                                 f"{dist:.0f} m away (L)", cn))
        else:
            targets.append(("TBD", "no mapped drain or pond within 400 m and none lower within 2 km: outlet not known", cn))

    # ---- merge blocks into zones: same outlet and council, adjacent, up to 75 ha
    left = set(range(len(blocks)))
    zones = []
    while left:
        i = max(left, key=lambda j: blocks[j].area)
        left.discard(i)
        grp, geom = [i], blocks[i]
        grown = True
        while grown:
            grown = False
            for j in sorted(left, key=lambda j: -blocks[j].area):
                if targets[j][0] == targets[i][0] and targets[j][2] == targets[i][2] and \
                        geom.buffer(1).intersects(blocks[j]) and (geom.area + blocks[j].area) <= MAX_ZONE_HA * 1e4:
                    grp.append(j)
                    geom = unary_union([geom, blocks[j]]).buffer(0.5).buffer(-0.5)
                    left.discard(j)
                    grown = True
        zones.append(dict(geom=geom, to=targets[i][0], basis=targets[i][1], council=targets[i][2], blocks=len(grp)))
    zones.sort(key=lambda z: (-z["geom"].centroid.y, z["geom"].centroid.x))
    for k, z in enumerate(zones):
        z["id"] = f"Z{k + 1:02d}"

    # ---- land cover and C per zone
    road_area = unary_union([g.buffer(ROAD_HALF_W.get(k, 4)) for g, k in roads]) if roads else Polygon()
    water_u = unary_union([g for g, _, _ in water] + [p["geom"] for p in ponds]) if (water or ponds) else Polygon()
    by = lambda keys: unary_union([g for k in keys for g in lu.get(k, [])]) if any(lu.get(k) for k in keys) else Polygon()  # noqa
    park_u, bare_u, open_u = by(PARK), by(BARE), by(OPEN)
    comm_u, built_u = by(COMMERCIAL), by(BUILT_LU - COMMERCIAL)
    bld_u = unary_union(buildings) if buildings else Polygon()
    for z in zones:
        g = z["geom"]
        taken = Polygon()
        parts = {}
        for k, layer in (("water", water_u), ("road", road_area), ("park", park_u), ("bare", bare_u),
                         ("commercial", comm_u), ("terrace", built_u), ("grass", open_u)):
            piece = g.intersection(layer).difference(taken)
            parts[k] = piece.area
            taken = taken.union(piece)
        rest = g.difference(taken)
        cover = rest.intersection(bld_u).area / rest.area if rest.area > 1 else 0.0
        parts["rest_built" if cover >= BUILT_SHARE else "rest_open"] = rest.area
        c_now = (sum(C[k] * v for k, v in parts.items() if k in C) + 0.90 * parts.get("rest_built", 0)
                 + 0.50 * parts.get("rest_open", 0)) / g.area
        built_out = parts["bare"] + parts["grass"] + parts.get("rest_open", 0)
        c_up = c_now + (0.90 - 0.60) * parts["bare"] / g.area + (0.90 - 0.50) * (parts["grass"] + parts.get("rest_open", 0)) / g.area
        z.update(c_now=round(c_now, 3), c_up=round(c_up, 3), open_m2=built_out, parts={k: round(v) for k, v in parts.items()},
                 bld_cover=round(g.intersection(bld_u).area / g.area, 3))

    # ---- storm: nearest MSMA 2 gauge
    idf = json.load(open(os.path.join(HERE, "data", "msma2_idf_selangor.json"), encoding="utf-8"))
    km = lambda la, lo: math.hypot((lo - lon0) * 111.32 * math.cos(math.radians(lat0)), (la - lat0) * 110.57)  # noqa
    st = min(idf["stations"], key=lambda q: km(q["lat"], q["lon"]))
    st_km = km(st["lat"], st["lon"])
    bbr = json.load(open(BBR_INPUTS, encoding="utf-8"))
    tb = lambda v: f"{idf['source']}, station {st['id']}"  # noqa
    storm = dict(
        ari_years=bbr["storm"]["ari_years"],
        idf=dict(station=f"{st['id']} {st['name']}",
                 **{k: a(st[k], "-", "sourced", tb(k), "H") for k in ("lambda", "kappa", "theta", "eta")},
                 station_choice=a(st["id"], "-", "assumed",
                                  f"Nearest Table 2.B1 gauge to the site centre, {st_km:.1f} km away ({st['position']})",
                                  "M" if st["position_confidence"] == "M" and st_km < 15 else "L")),
        durations_h=bbr["storm"]["durations_h"],
        design_duration_h=bbr["storm"]["design_duration_h"],
        tc_hours=a(0.5, "h", "assumed", "As BBR (MSMA Table 2.1 overland + drain flow, ~23 min, rounded up); not "
                   "worked out for this site", "L"))
    method = json.loads(json.dumps(bbr["method"]))
    method["c_predevelopment"]["status"] = "assumed"
    method["c_predevelopment"]["confidence"] = "M"
    method["c_predevelopment"]["source"] = ("MSMA 2nd Edition (DID 2012), Chapter 2, Table 2.5 'Sport Fields, Park and "
                                            "Agriculture' (major system), as at BBR: the land before development is "
                                            "taken as agricultural or open land. Not checked for this site")

    # ---- inputs (network format)
    def zone_in(z):
        return dict(name=f"Block group {z['id']}", council=z["council"], drains_to=z["to"], drains_to_basis=z["basis"],
                    area_ha=a(round(z["geom"].area / 1e4, 2), "ha", "measured",
                              "Plan area of the generated zone (cut along mapped roads, railways, waterways and council "
                              "lines; OpenStreetMap)", "M"),
                    c_now=a(z["c_now"], "-", "measured", C_SOURCE, "M"),
                    c_upstream=a(z["c_up"], "-", "assumed",
                                 "Upstream scenario: every bare, open and unmapped open block in the zone built out "
                                 "as terrace housing (0.90)", "L"))

    def drain_in(d):
        top, bot, dep = SECTIONS[d["kind"]]
        typ = f"OSM waterway={d['kind']}" + (f" (raised to the size of {d['upsized']}, which flows into it)"
                                              if d.get("upsized") else "")
        return dict(name=d["name"] or f"Unnamed {d['kind']}", council=d["council"], drains_to=d["drains_to"],
                    drains_to_basis=d["to_basis"], osm_ways=d["osm"][:20],
                    section=dict(top_width_m=a(top, "m", "assumed", f"Typical for {typ}; not measured", "L"),
                                 bottom_width_m=a(bot, "m", "assumed", f"Typical for {typ}; not measured", "L"),
                                 depth_m=a(dep, "m", "assumed", f"Typical for {typ}; not measured", "L"),
                                 manning_n=a(0.018, "-", "assumed", "MSMA 2 Table 2.3 lined concrete drain, rough "
                                             "finish (as BBR's trunk drain); lining not checked", "L"),
                                 slope=a(round(d["slope"], 5), "-", "measured",
                                         "Copernicus GLO-30 fall between the chain's ends over its length, kept to "
                                         "0.05-2 % (a surface model; L)", "L")),
                    blockage=a(0.0, "-", "planner input", "Share of capacity lost to silt and rubbish; 0 = clean", "-"))

    def pond_in(p):
        cap = round(p["geom"].area * LIVE_DEPTH_M, -2)
        src = (f"JPS Selangor pond list {p['jps']['code']} (phase {p['jps']['phase']}, {p['jps']['town']}, "
               f"{p['jps']['address']})" if p["jps"] else "OpenStreetMap water body")
        return dict(name=(p["jps"]["address"].title() if p["jps"] else p["name"] or "Unnamed pond"),
                    council=p["council"], drains_to=p["drains_to"], drains_to_basis=p["to_basis"],
                    listed=src, osm=p["osm"], water_area_m2=round(p["geom"].area),
                    capacity_m3=a(cap, "m3", "assumed",
                                  f"ASSUMED: water area {p['geom'].area:,.0f} m2 (mapped) x {LIVE_DEPTH_M} m live "
                                  "storage, the stated BBR rule (research/HY_screening_inputs.md section 7). No public "
                                  "capacity exists; a planner replaces it", "L"))

    inputs = dict(
        _about=f"RainReady network inputs for {name}, GENERATED by build_site.py on {time.strftime('%d %b %Y')} from "
               "open data. Screening only. Every value carries its status, source and confidence; most are assumed.",
        _status_key=bbr["_status_key"], site=site_id, storm=storm, method=method,
        zones={z["id"]: zone_in(z) for z in zones},
        drains={d["id"]: drain_in(d) for d in drains},
        ponds={p["id"]: pond_in(p) for p in ponds},
        what_if_ponds={},
        scenarios=dict(now=dict(c="c_now", what_if_ponds=[], label="Today's land cover"),
                       upstream=dict(c="c_upstream", what_if_ponds=[], label="Open and vacant land built out"),
                       upstream_plus_pond=dict(c="c_upstream", what_if_ponds=["W1"],
                                               label="Built out, plus a what-if pond")))
    # drop drains nothing reaches (no zone, pond or upstream drain), repeatedly
    while True:
        used = {z["drains_to"] for z in inputs["zones"].values()} | {p["drains_to"] for p in inputs["ponds"].values()} | \
               {d["drains_to"] for d in inputs["drains"].values()}
        dead = [k for k in inputs["drains"] if k not in used]
        if not dead:
            break
        for k in dead:
            del inputs["drains"][k]
    drains = [d for d in drains if d["id"] in inputs["drains"]]

    # ---- what-if pond: the biggest open parcel in a zone draining to the most loaded pond (or drain)
    probe = json.loads(json.dumps(inputs))
    probe["scenarios"] = {"now": probe["scenarios"]["now"]}
    r0 = network.run(probe)["scenarios"]["now"]
    loaded = sorted(r0["ponds"].items(), key=lambda kv: -(kv[1]["ratio"] or 0)) + \
        sorted(r0["drains"].items(), key=lambda kv: -(kv[1]["ratio"] or 0))
    whatif = None
    for node, _ in loaded:
        cands = [z for z in zones if z["to"] == node]
        for z in sorted(cands, key=lambda z: -z["open_m2"]):
            parcels = [g.intersection(z["geom"]) for k in (BARE | OPEN) for g in lu.get(k, [])]
            parcels = [p for p in parcels if p.area > 5000]
            if parcels:
                pg = max(parcels, key=lambda p: p.area)
                if pg.geom_type == "MultiPolygon":
                    pg = max(pg.geoms, key=lambda q: q.area)
                whatif = dict(zone=z["id"], geom=pg, node=node)
                break
        if whatif:
            break
    if whatif:
        cap = round(whatif["geom"].area * LIVE_DEPTH_M, -3)
        inputs["what_if_ponds"]["W1"] = dict(
            _what=f"Illustrative new pond on open land in {whatif['zone']} ({whatif['geom'].area / 1e4:.1f} ha, OSM land "
                  f"use), catching {whatif['zone']}'s runoff before {whatif['node']}. A what-if, not a proposal",
            serves=[whatif["zone"]], drains_to=whatif["node"],
            capacity_m3=a(cap, "m3", "planner input", f"Test size: parcel area x {LIVE_DEPTH_M} m (a what-if, not a fact)", "-"),
            outlet_m3_s=a(0.0, "m3/s", "planner input", "Default 0: holds what it catches during the storm, as at BBR", "-"))
    else:
        inputs["scenarios"].pop("upstream_plus_pond")

    t_build = time.time() - t0 - t_fetch
    res = network.run(inputs)

    # ---- flood evidence inside the area
    nat = json.load(open(NATIONAL, encoding="utf-8"))
    inside = lambda c: w <= c[0] <= e and s <= c[1] <= n  # noqa
    floods = [f for f in nat["flood"] if inside(f["c"])]
    flash = [f for f in nat["flash"] if km(f["c"][1], f["c"][0]) < 6]

    # ---- geo.json (lon/lat)
    feats = []
    add = lambda geom, **props: feats.append(dict(type="Feature", geometry=r6(lonlat(geom.simplify(1.5), back)), properties=props))  # noqa
    add(area, kind="area")
    for nm, c in councils:
        add(c.intersection(area), kind="council", name=nm)
    if not council_lines.is_empty:
        add(council_lines, kind="council_line")
    for z in zones:
        add(z["geom"], kind="zone", id=z["id"])
    for p in ponds:
        add(p["geom"], kind="pond", id=p["id"])
    def downhill(g):
        """Each part drawn from its higher end to its lower end, so the site can animate flow downstream."""
        parts = list(g.geoms) if g.geom_type == "MultiLineString" else [g] if g.geom_type == "LineString" else []
        out = [LineString(pt.coords[::-1]) if z_at(*back(*pt.coords[0])) < z_at(*back(*pt.coords[-1])) else pt for pt in parts]
        return MultiLineString(out) if len(out) > 1 else out[0] if out else g
    for d in drains:
        add(downhill(d["geom"]), kind="drain", id=d["id"])
    for g, _ in rivers:
        add(g, kind="river")
    if whatif:
        add(whatif["geom"], kind="whatif", id="W1")
    for d in drains:     # where a mapped drain crosses a council line
        if not council_lines.is_empty:
            x = d["geom"].intersection(council_lines.buffer(0.5))
            if not x.is_empty and d["id"][-1] in "abcdefgh":
                feats.append(dict(type="Feature", properties=dict(kind="crossing_point", drain=d["id"]),
                                  geometry=r6(lonlat(x.centroid, back))))
    for f in floods:
        feats.append(dict(type="Feature", geometry=dict(type="Point", coordinates=f["c"]),
                          properties=dict(kind="flood", year=f["y"], type=f["t"] or "Not stated", place=f["p"])))
    geo = dict(type="FeatureCollection", features=feats)

    # ---- site.json
    n_jps = sum(1 for p in ponds if p["jps"])
    cross_now = res["scenarios"]["now"]["crossings"]
    tests = [
        dict(test="JPS flood records inside the area", passed=len(floods) > 0,
             detail=f"{len(floods)} records, {min([f['y'] for f in floods], default='-')}-{max([f['y'] for f in floods], default='-')}"),
        dict(test="Drainage crosses a council line", passed=len(cross_now) > 0,
             detail=f"{len(cross_now)} crossing links between {', '.join(sorted({c for c in [p['council'] for p in ponds] + [z['council'] for z in zones] if c}))}"),
        dict(test="Public pond or drain register", passed=n_jps > 0, detail=f"{n_jps} ponds on JPS Selangor's pond list"),
    ]
    site = dict(
        id=site_id, name=name, kind="generated", view="2d", state="Selangor",
        centre=[round(lat0, 5), round(lon0, 5)], bbox=[s, w, n, e],
        councils=[nm for nm, _ in councils], confidence="L",
        label="SCREENING · GENERATED FROM OPEN DATA · LOWER CONFIDENCE",
        summary=f"{len(zones)} zones, {len(inputs['drains'])} drains, {len(ponds)} ponds ({n_jps} on JPS's list), "
                f"{len(councils)} councils",
        tests=tests,
        evidence=dict(flood_records=[dict(year=f["y"], type=f["t"] or "Not stated", place=f["p"], district=f["d"])
                                     for f in sorted(floods, key=lambda f: (f["y"], f["p"]))],
                      flash_2017=[dict(town=f["t"], places=f["e"]) for f in flash]),
        storm=dict(station=storm["idf"]["station"], distance_km=round(st_km, 1)),
        sources=["OpenStreetMap contributors (ODbL), via Overpass, " + time.strftime("%d %b %Y"),
                 "Copernicus DEM GLO-30 (ESA / EU), AWS open data mirror",
                 "JPS Selangor pond list (Kolam_Fasa_JPS), jpsselgis.selangor.gov.my",
                 "JPS Selangor flood records 2017-2024 and JPS flash-flood list 2017 (website/public/data/national.json)",
                 "MSMA 2nd Edition (DID Malaysia, 2012), Chapter 2, Tables 2.3, 2.5, 2.B1"],
        limits=["Zones follow mapped roads and drains, not surveyed catchments; outlets are assumed",
                "Drain sizes are typical values by OSM type, not measured; this is the weakest input",
                "Pond capacities are assumed from water area x 1.5 m; enter stated capacities to replace them",
                "OSM misses buildings and drains; terrain is a surface model with ~1 m error or more",
                "Flash floods and ponding only; rivers are treated as where water leaves"],
        build=dict(script="simulations/platform/build_site.py", date=time.strftime("%Y-%m-%d"),
                   fetch_s=round(t_fetch, 1), build_s=round(t_build, 1), refreshed=bool(refresh)))
    old = os.path.join(out_dir, "site.json")
    if t_fetch < 5 and os.path.exists(old):        # downloads came from the cache: keep the time they really took
        site["build"]["fetch_s"] = json.load(open(old, encoding="utf-8")).get("build", {}).get("fetch_s", site["build"]["fetch_s"])
    json.dump(site, open(os.path.join(out_dir, "site.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(inputs, open(os.path.join(out_dir, "inputs.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(res, open(os.path.join(out_dir, "outputs.json"), "w", encoding="utf-8"), indent=1)
    json.dump(geo, open(os.path.join(out_dir, "geo.json"), "w", encoding="utf-8"), separators=(",", ":"))
    with open(os.path.join(out_dir, "register_template.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["kind", "id", "name", "capacity_m3", "live_depth_m", "top_width_m", "bottom_width_m", "depth_m",
                     "source"])
        for pid, p in inputs["ponds"].items():
            wr.writerow(["pond", pid, p["name"], "", "", "", "", "", ""])
        for did, d in inputs["drains"].items():
            wr.writerow(["drain", did, d["name"], "", "", "", "", "", ""])
    print(f"{site_id}: {site['summary']}; fetch {t_fetch:.0f} s, build {t_build:.0f} s")
    for t in tests:
        print(f"  {'PASS' if t['passed'] else 'FAIL'}  {t['test']}: {t['detail']}")
    network.report(res)
    return site


if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    build(args[0], args[1], tuple(float(x) for x in args[2:6]), refresh="--refresh" in sys.argv)
