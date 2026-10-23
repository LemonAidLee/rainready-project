"""RainReady township: hybrid base and AR1 hydrology features.

Base (team leader's decision, 20 Oct 2026): the architecture student's sketch (collection SKETCH, appended from
reference/architecture_sketch_BBR.blend and shifted by SKETCH_OFFSET into the AR1 frame). AR1 supplies the ground
(Copernicus GLO-30), the hydrology features and the context outside the sketch.

Run inside Blender after style_scene.py:
    exec(open(r"D:\\Progmata\\SDP\\simulations\\township-3d\\build_features.py").read())

Everything that is not measured is labelled in the objects' custom properties. Basin and channel depths are VISUAL
ONLY: no depth is read from this model (house rule: risk bands, never depths).
"""
import bpy, bmesh, json, os
from mathutils import Vector
from mathutils.bvhtree import BVHTree

GIS = r"D:\Progmata\SDP\research\AR1_site_model\gis"
# Fitted on 426 matched building centroids: median residual 0.66 m, rotation 0.1 deg, scale 0.9998 (20 Oct 2026)
SKETCH_OFFSET = (-288.13, -794.99)
GROUND_DZ = -1.0          # GLO-30 lowered so sketch roads sit on it (sketch roads are a median 0.6 m above GLO-30)
EXTENT = (1222.0, 608.0)  # AR1 half-extent in x and y (where AR1's ground and data are)
MODEL = (-1222.0, 1700.0, -830.0, 608.0)   # x0, x1, y0, y1: the whole shown model, a rectangle (team leader, 20 Oct 2026)
BASIN_VIS = 2.5           # visual basin depth, NOT a measured or design depth
# Channel sections (top width, bottom width, visual depth), metres. Main ditch top width from imagery (8-10 m, AR1);
# all other values ASSUMED.
SECTION = {"main": (9.0, 4.5, 2.0), "ditch": (3.0, 1.5, 1.2), "drain": (1.5, 0.8, 0.8)}
SOURCES = {
    "sinar": "https://www.sinarharian.com.my/ampArticle/666626",
}


def proj(lon, lat):
    """Same equirectangular frame as the AR1 OBJ files (origin 3.0900 N, 101.4360 E)."""
    return Vector(((lon - 101.436) * 111158.0, (lat - 3.09) * 110572.0, 0.0))


def load(name):
    return json.load(open(os.path.join(GIS, name), encoding="utf-8"))["features"]


def load_all(name):
    """AR1 layer plus its OSM supplement for the model rectangle (`<name>_supplement.geojson`), if fetched."""
    sup = name.replace(".geojson", "_supplement.geojson")
    return load(name) + (load(sup) if os.path.exists(os.path.join(GIS, sup)) else [])


def coll(name, hide_render=False):
    c = bpy.data.collections.get(name)
    if not c:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    for o in list(c.objects):
        me = o.data
        bpy.data.objects.remove(o)
        if me and me.users == 0 and isinstance(me, bpy.types.Mesh):
            bpy.data.meshes.remove(me)
    c.hide_render = hide_render
    return c


def material(name, color, rough=0.8, emit=0.0, alpha=1.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Emission Color"].default_value = (*color, 1)
    b.inputs["Emission Strength"].default_value = emit
    b.inputs["Alpha"].default_value = alpha
    return m


def link(c, name, bm, mats):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    for m in mats:
        me.materials.append(m)
    o = bpy.data.objects.new(name, me)
    c.objects.link(o)
    return o


def inside(p):
    return MODEL[0] <= p.x <= MODEL[1] and MODEL[2] <= p.y <= MODEL[3]


def clip(pts):
    """Split a polyline into runs that stay inside the AR1 extent."""
    runs, cur = [], []
    for p in pts:
        if inside(p):
            cur.append(p)
        elif cur:
            runs.append(cur); cur = []
    if cur:
        runs.append(cur)
    return [r for r in runs if len(r) > 1]


# ---------------------------------------------------------------- ground
def setup_ground():
    g = bpy.data.objects["terrain_cop30"]
    g.location.z = GROUND_DZ
    g.data.materials.clear(); g.data.materials.append(bpy.data.materials["ground"])
    g["source"] = "Copernicus GLO-30 DSM via AR1; lowered 1.0 m to sit under the sketch. Absolute heights unusable."
    t = bpy.data.objects["terrain"]
    t.hide_set(True); t.hide_render = True
    bm = bmesh.new(); bm.from_mesh(g.data); bm.transform(g.matrix_world)
    bvh = BVHTree.FromBMesh(bm); bm.free()

    def z(p):
        hit = bvh.ray_cast(Vector((p.x, p.y, 500)), Vector((0, 0, -1)))
        return hit[0].z if hit[0] else 0.0
    return g, z


def clip_to_extent(ring, margin=1.0):
    """Sutherland-Hodgman clip of a polygon to the model rectangle, kept `margin` m inside the edge (a pond cutter that
    touches the open ground edge makes the boolean drop walls down off the model)."""
    def clip(poly, inside_fn, cut):
        out = []
        for i, cur in enumerate(poly):
            prev = poly[i - 1]
            if inside_fn(cur):
                if not inside_fn(prev):
                    out.append(cut(prev, cur))
                out.append(cur)
            elif inside_fn(prev):
                out.append(cut(prev, cur))
        return out
    for axis, lim, sign in ((0, MODEL[1] - margin, 1), (0, MODEL[0] + margin, -1),
                            (1, MODEL[3] - margin, 1), (1, MODEL[2] + margin, -1)):
        if not ring:
            break
        ins = lambda p, a=axis, l=lim, sg=sign: sg * p[a] <= sg * l
        def cut(a, b, ax=axis, l=lim):
            t = (l - a[ax]) / (b[ax] - a[ax])
            return a.lerp(b, t)
        ring = clip(ring, ins, cut)
    return ring


def offset_ring(ring, t):
    """Move each vertex of a counter-clockwise ring inward by t along the corner bisector."""
    out, n = [], len(ring)
    for i in range(n):
        dp = (ring[i] - ring[i - 1]); dp.z = 0; dp.normalize()
        dn = (ring[(i + 1) % n] - ring[i]); dn.z = 0; dn.normalize()
        a, b = Vector((-dp.y, dp.x, 0)), Vector((-dn.y, dn.x, 0))
        bis = a + b
        bis = bis.normalized() if bis.length > 1e-6 else b
        out.append(ring[i] + bis * (t / max(0.35, bis.dot(b))))
    return out


def build_outer_ground(c, gz, mats):
    """Ground for the part of the model rectangle beyond the AR1 extent (east of x = 1222, south of y = -608).
    Each point takes the GLO-30 height at the nearest point on the AR1 edge, so the ground simply continues outward.
    Stable across re-runs (it does not depend on anything this script moves). Look only, not a terrain source."""

    def axis(lo, edge, hi, step=30.0):
        a, v = [], lo
        while v < edge:
            a.append(v); v += step
        a.append(edge); v = edge + step
        while v < hi:
            a.append(v); v += step
        return a + [hi]
    xs = axis(MODEL[0], EXTENT[0] + 0.5, MODEL[1])
    ys = list(reversed([-v for v in axis(-MODEL[3], EXTENT[1], -MODEL[2])]))   # -830 .. -608 .. 608
    bm = bmesh.new()
    grid = {}
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            p = Vector((x, y, 0))
            z = gz(Vector((min(x, EXTENT[0] - 0.5), max(y, -EXTENT[1] + 0.5), 0)))
            grid[i, j] = bm.verts.new((x, y, z))
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            cx, cy = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
            if abs(cx) < EXTENT[0] and abs(cy) < EXTENT[1]:
                continue
            bm.faces.new([grid[i, j], grid[i + 1, j], grid[i + 1, j + 1], grid[i, j + 1]])
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context="VERTS")
    o = link(c, "ground_sketch_fill", bm, [mats["ground"]])
    o["note"] = "Ground beyond the AR1 extent, continued from the GLO-30 edge. Look only."
    for p in o.data.polygons:
        p.use_smooth = True


# ---------------------------------------------------------------- ponds
def build_ponds(c, cutters, gz, mats):
    ids = {399570465: "A", 359496461: "B"}
    for f in load_all("water.geojson"):
        pid = f["properties"]["id"]
        ring = clip_to_extent([proj(*ll) for ll in f["geometry"]["coordinates"][0]])   # Tasik Setia Alam crosses the edge
        if len(ring) < 3:
            continue
        xs_, ys_ = [p.x for p in ring], [p.y for p in ring]
        a_in = abs(sum(ring[i].x * ring[i - 1].y - ring[i - 1].x * ring[i].y for i in range(len(ring)))) / 2
        if a_in < 1500 or min(max(xs_) - min(xs_), max(ys_) - min(ys_)) < 20:
            continue   # only a sliver of this water body lies in the model: skip (it would show as a thin strip at the edge)
        if (ring[0] - ring[-1]).length < 0.01:
            ring.pop()
        n = len(ring)
        area = sum(ring[i].x * ring[(i + 1) % n].y - ring[(i + 1) % n].x * ring[i].y for i in range(n))
        if area < 0:
            ring.reverse()
        if f["properties"]["a"] < 1000:
            continue  # 216 m2 basin: not a pond (AR1)
        ztop = min(gz(p) for p in ring) - 0.2
        name = (f"pond_{ids[pid]}" if pid in ids else "water_tasik_setia_alam" if pid == 164881251
                else f"water_{pid}")
        bm = bmesh.new()
        rim = [bm.verts.new((p.x, p.y, ztop)) for p in ring]
        flo = [bm.verts.new((p.x, p.y, ztop - BASIN_VIS)) for p in offset_ring(ring, 6.0)]
        for i in range(len(ring)):
            j = (i + 1) % len(ring)
            bm.faces.new([rim[i], rim[j], flo[j], flo[i]])          # sloped bank, inside the basin
        bm.faces.new(flo).material_index = 1                        # basin floor
        # skirt from the rim up to the surrounding ground, so no gap shows where the ground is cut
        sk = [bm.verts.new((p.x, p.y, gz(p) + 0.05)) for p in ring]
        for i in range(len(ring)):
            j = (i + 1) % len(ring)
            bm.faces.new([rim[j], rim[i], sk[i], sk[j]])
        bm.normal_update()
        o = link(c, name, bm, [mats["bank"], mats["basin_floor"]])
        o["osm_id"] = pid
        o["mapped_area_m2"] = f["properties"]["a"]
        o["basin_depth_note"] = "Basin depth in the model is VISUAL ONLY, not measured or designed"
        if pid in ids:
            o["stated_capacity_m3"] = "TBD"
            o["capacity_source"] = "No public figure (AR1). Do not derive from model geometry."
            o["owner"] = "TBD"; o["owner_conf"] = "L"
        # water surface: a flat sheet that moves between the basin floor (0 %) and the rim (100 %)
        bmw = bmesh.new()
        bmw.faces.new([bmw.verts.new((p.x, p.y, 0)) for p in ring])
        w = link(c, name + "_water", bmw, [mats["water"]])
        w["fill_pct"] = 0.5
        w["fill_status"] = "PLACEHOLDER until the screening simulator drives it"
        floor = ztop - BASIN_VIS
        fc = w.driver_add("location", 2)
        fc.driver.type = "SCRIPTED"
        v = fc.driver.variables.new(); v.name = "f"; v.type = "SINGLE_PROP"
        v.targets[0].id = w; v.targets[0].data_path = '["fill_pct"]'
        fc.driver.expression = f"{floor:.3f} + 0.05 + min(max(f, 0), 1) * {BASIN_VIS - 0.1:.3f}"
        # cutter for the ground
        bmc = bmesh.new()
        lo = [bmc.verts.new((p.x, p.y, ztop - 30)) for p in ring]
        hi = [bmc.verts.new((p.x, p.y, ztop + 60)) for p in ring]
        bmc.faces.new(list(reversed(lo))); bmc.faces.new(hi)
        for i in range(len(ring)):
            j = (i + 1) % len(ring)
            bmc.faces.new([lo[i], lo[j], hi[j], hi[i]])
        bmc.normal_update()
        link(cutters, "cut_" + name, bmc, [])


# ---------------------------------------------------------------- channels
def densify(run, step=8.0):
    out = [run[0]]
    for a, b in zip(run, run[1:]):
        n = max(1, int((b - a).length // step))
        out += [a.lerp(b, k / n) for k in range(1, n + 1)]
    return out


def resample(run, step):
    """Points every `step` metres along a polyline (by distance travelled, not per segment)."""
    out, carry = [run[0]], 0.0
    for a, b in zip(run, run[1:]):
        seg = (b - a).length
        t = step - carry
        while t <= seg:
            out.append(a.lerp(b, t / seg)); t += step
        carry = seg - (t - step)
    return out


def ribbon(bm, run, zs, half, dz, uv=None):
    """Flat strip of half-width `half`, following the ground at height zs + dz."""
    prev = None
    for i, p in enumerate(run):
        d = run[min(i + 1, len(run) - 1)] - run[max(i - 1, 0)]
        d.z = 0; d.normalize(); n = Vector((-d.y, d.x, 0))
        pair = (bm.verts.new(p + n * half + Vector((0, 0, zs[i] + dz))),
                bm.verts.new(p - n * half + Vector((0, 0, zs[i] + dz))))
        if prev:
            bm.faces.new([prev[0], prev[1], pair[1], pair[0]])
        prev = pair


def build_channels(c, gz, mats):
    """Channels drawn ON the ground (concrete band plus a water band), not cut into it: thin cuts through a 30 m
    ground grid leave artefacts, and depth is not shown anyway."""
    main = load("main_ditch.geojson")[0]["geometry"]["coordinates"]
    bmw = bmesh.new()
    k = 0
    for f in load_all("drains.geojson"):
        coords = f["geometry"]["coordinates"]
        is_main = abs(coords[0][0] - main[0][0]) < 1e-5 and abs(coords[0][1] - main[0][1]) < 1e-5
        kind = "main" if is_main else f["properties"]["c"]
        top, bot, _ = SECTION.get(kind, SECTION["drain"])
        for run in clip(densify([proj(*ll) for ll in coords], 4.0)):   # densify first: keep parts of segments that cross the edge
            k += 1
            run = densify(run)
            zs = [gz(p) for p in run]
            bm = bmesh.new()
            ribbon(bm, run, zs, top / 2, 0.35)
            ribbon(bmw, run, zs, bot / 2, 0.42)
            bm.normal_update()
            name = "drain_888406336" if is_main else f"drain_D{k:02d}"
            o = link(c, name, bm, [mats["concrete"]])
            o["type"] = "main ditch" if is_main else kind
            o["osm_id"] = 888406336 if is_main else "TBD"
            o["width_m"] = top if is_main else "TBD"
            o["section_note"] = ("Top width from imagery (8-10 m, AR1)" if is_main
                                 else "Width ASSUMED for display; position from OSM")
            o["owner"] = "TBD"; o["owner_conf"] = "L"
            o["path"] = [list(p[:2]) for p in run[::4]]   # for flow arrows later
    link(c, "drains_water", bmw, [mats["water"]])


def build_culverts(c, gz, mats, max_gap=30.0):
    """Bridge short gaps between OSM drain pieces (usually a culvert under a road, which OSM often leaves out).
    Drawn as the narrower channel section. INFERRED, not mapped: every bridge is listed in the object's properties."""
    feats = load_all("drains.geojson")
    lines = [[proj(*ll) for ll in f["geometry"]["coordinates"]] for f in feats]
    kinds = [f["properties"]["c"] for f in feats]
    bm, bmw, made = bmesh.new(), bmesh.new(), []
    for i, pts in enumerate(lines):
        for e in (pts[0], pts[-1]):
            if not inside(e):
                continue
            best = None
            for j, q in enumerate(lines):
                if j == i:
                    continue
                for a, b in zip(q, q[1:]):
                    ab = b - a
                    t = max(0.0, min(1.0, (e - a).dot(ab) / max(ab.length_squared, 1e-9)))
                    p = a + ab * t
                    d = (p - e).length
                    if best is None or d < best[0]:
                        best = (d, p, j)
            if not best or not (1.0 < best[0] <= max_gap):
                continue
            key = tuple(sorted((i, best[2])))
            if any(k == key and (m - e).length < 1 for k, m in [(x[0], x[1]) for x in made]):
                continue
            made.append((key, e, best[1], round(best[0], 1)))
            top, bot, _ = SECTION.get(kinds[i], SECTION["drain"])
            run = densify([e, best[1]], 3.0)
            zs = [gz(p) for p in run]
            ribbon(bm, run, zs, top / 2, 0.35)
            ribbon(bmw, run, zs, bot / 2, 0.42)
    o = link(c, "drain_culverts_inferred", bm, [mats["concrete"]])
    o["note"] = ("INFERRED links across gaps of up to %d m between OSM drain pieces (likely culverts under roads). "
                 "Not mapped; shown so the drainage reads as connected." % max_gap)
    o["gaps_m"] = [g for *_, g in made]
    w = link(c, "drain_culverts_inferred_water", bmw, [mats["water"]])
    print("culvert links:", len(made), sorted(g for *_, g in made))


PLINTH = [(MODEL[0], MODEL[3]), (MODEL[1], MODEL[3]), (MODEL[1], MODEL[2]), (MODEL[0], MODEL[2])]   # the model rectangle


def build_plinth(c, gz, mats, depth=14.0):
    """A finished, diorama-style edge: earth sides from the ground edge down, so the model's boundary reads as
    deliberate rather than as roads and trees cut off in mid-air."""
    bm = bmesh.new()
    ring = PLINTH + [PLINTH[0]]
    prev = None
    for a, b in zip(ring, ring[1:]):
        a, b = Vector((*a, 0)), Vector((*b, 0))
        n = max(1, int((b - a).length // 10.0))
        for k in range(n + 1):
            if prev is not None and k == 0:
                continue
            p = a.lerp(b, k / n)
            inward = Vector((max(MODEL[0] + 0.5, min(MODEL[1] - 0.5, p.x)), max(MODEL[2] + 0.5, min(MODEL[3] - 0.5, p.y)), 0))
            pair = (bm.verts.new((p.x, p.y, gz(inward) + 0.02)), bm.verts.new((p.x, p.y, -depth)))
            if prev:
                bm.faces.new([prev[0], prev[1], pair[1], pair[0]])
            prev = pair
    bm.normal_update()
    o = link(c, "plinth", bm, [mats["plinth"]])
    o["note"] = "Display base around the model edge. Look only."


# ---------------------------------------------------------------- council line, pins
CURTAIN_H = 14.0      # height of the translucent boundary curtain (look only)
LABEL_Z = 24.0        # area labels float this high: above roofs (max ~11 m) and tree crowns


def curtain_material():
    """Soft white light curtain, fading upward. Kept out of the toon looks (name starts with 'boundary_')."""
    m = bpy.data.materials.get("boundary_curtain") or bpy.data.materials.new("boundary_curtain")
    m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    uv = nt.nodes.new("ShaderNodeUVMap"); uv.uv_map = "curtain"
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(uv.outputs[0], sep.inputs[0])
    fade = nt.nodes.new("ShaderNodeMapRange"); nt.links.new(sep.outputs[1], fade.inputs["Value"])
    fade.inputs["To Min"].default_value = 0.6; fade.inputs["To Max"].default_value = 0.0
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (1.0, 0.98, 0.92, 1)
    em.inputs["Strength"].default_value = 1.6
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(fade.outputs["Result"], mix.inputs[0]); nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    for attr, val in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
        try:
            setattr(m, attr, val)
        except Exception:
            pass
    m.use_backface_culling = False
    return m


def build_council_line(c, gz, mats):
    """The Klang / Shah Alam council line: a translucent light curtain, a dashed ground band drawn above the roads,
    and a label on each side. Neutral styling: neither side is coloured differently."""
    coords = load("council_line.geojson")[0]["geometry"]["coordinates"]
    bm, band = bmesh.new(), bmesh.new()
    uvl = bm.loops.layers.uv.new("curtain")
    for run in clip(densify([proj(*ll) for ll in coords], 4.0)):   # densify first: the line starts 3.6 km outside
        run = densify(run, 4.0)
        zs = [gz(p) for p in run]
        prev, dist = None, 0.0
        for i, (p, z) in enumerate(zip(run, zs)):
            if i:
                dist += (p - run[i - 1]).length
            pair = (bm.verts.new((p.x, p.y, z)), bm.verts.new((p.x, p.y, z + CURTAIN_H)))
            if prev:
                f = bm.faces.new([prev[0], pair[0], pair[1], prev[1]])
                for loop in f.loops:
                    loop[uvl].uv = (dist / 10.0, 1.0 if loop.vert in (pair[1], prev[1]) else 0.0)
            prev = pair
        # dashed band, 10 m on / 5 m off, above roads and pavements
        d, seg = 0.0, []
        for i, p in enumerate(run):
            if i:
                d += (p - run[i - 1]).length
            if d % 15.0 < 10.0:
                seg.append(i)
            elif len(seg) > 1:
                ribbon(band, [run[k] for k in seg], [zs[k] for k in seg], 1.6, 0.75); seg = []
            else:
                seg = []
        if len(seg) > 1:
            ribbon(band, [run[k] for k in seg], [zs[k] for k in seg], 1.6, 0.75)
    o = link(c, "council_line", bm, [curtain_material()])
    o["osm_way"] = 1231162275
    o["source"] = "OpenStreetMap administrative boundary (rel 10715532 Klang / 8347577 Shah Alam). NOT cadastral."
    b = link(c, "council_line_band", band, [mats["council"]])
    b["note"] = "Dashed ground band marking the council line; neutral styling"
    # PROXY NAMES on screen (team leader, 20 Oct 2026): the town is simulated and the flood issue is a live dispute,
    # so the model shows Area A / Area B. The real places are kept in "proxy_for" for the team and the deck.
    for name, text, pos, real in (("area_B", "AREA B", (640, 170), "Bandar Bukit Raja (Klang council side)"),
                                  ("area_A", "AREA A", (1380, 470), "Setia Alam (Shah Alam council side) [verify]")):
        cu = bpy.data.curves.new("label_" + name, "FONT")
        cu.body = text; cu.size = 40; cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.extrude = 0.8
        t = bpy.data.objects.new("label_" + name, cu)
        p = Vector((*pos, 0)); t.location = (p.x, p.y, gz(p) + LABEL_Z)
        t.rotation_euler = (0, 0, 0)        # flat, raised above roofs and trees: reads from any side, never mirrored
        t["proxy_for"] = real
        t.data.materials.append(mats["label"])
        t["note"] = "Proxy area name; side taken from the OSM council boundary"
        c.objects.link(t)


def build_pins(c, gz, mats):
    roads = load("roads.geojson")
    spots = [
        ("Makyong", "spot_jalan_makyong", SOURCES["sinar"], "[verify date]",
         "Residents' association: floods at least three times a year, especially Jalan Makyong"),
        ("Sumazau", "spot_jalan_sumazau", SOURCES["sinar"], "[verify date]",
         "Named with Jalan Makyong as low-lying early phases that flood"),
        ("Batu Belah", "spot_persiaran_batu_belah", "2024 residents' memorandum, as summarised in AR1 study-area note [verify]",
         "2024", "Larger drains requested. A drainage request, NOT a reported flood spot"),
    ]
    for k, (key, name, src, date, note) in enumerate(spots, start=1):
        pts = [proj(*ll) for f in roads if key in (f["properties"].get("n") or "") for ll in f["geometry"]["coordinates"]]
        pts = [p for p in pts if inside(p)]
        if not pts:
            print("no road found for", key); continue
        cen = sum(pts, Vector()) / len(pts)
        p = min(pts, key=lambda q: (q - cen).length)   # a point ON the street nearest its centroid
        z = gz(p)
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.6, radius2=0.6, depth=24,
                              matrix=__import__("mathutils").Matrix.Translation((0, 0, 12)))
        bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=4,
                                  matrix=__import__("mathutils").Matrix.Translation((0, 0, 26)))
        o = link(c, name, bm, [mats["pin"]])
        o.location = (p.x, p.y, z)
        o["source"] = src; o["date"] = date; o["note"] = note
        o["position_note"] = "Pin on the mapped street, near its middle. NOT a measured flood location."
        # proxy name on screen; the real street stays in the object name and "proxy_for" for the team
        o["display_name"] = f"Spot {k}"
        o["proxy_for"] = key
        cu = bpy.data.curves.new(f"label_spot_{k}", "FONT")
        cu.body = f"SPOT {k}"; cu.size = 9; cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.extrude = 0.4
        t = bpy.data.objects.new(f"label_spot_{k}", cu)
        t.location = (p.x, p.y, z + 33)
        t.data.materials.append(mats["label"])
        t["proxy_for"] = key
        c.objects.link(t)


# ---------------------------------------------------------------- context outside the sketch
def trim_context():
    sk_build = [o for o in bpy.data.collections["SKETCH"].objects if o.type == "MESH" and o.data.materials
                and o.data.materials[0] and o.data.materials[0].name.startswith("TPX_BUILDINGS")]
    cents = []
    for o in sk_build:
        ws = [o.matrix_world @ v.co for v in o.data.vertices]
        cents.append(sum(ws, Vector()) / len(ws))
    from mathutils.kdtree import KDTree
    kd = KDTree(len(cents))
    for i, c in enumerate(cents):
        kd.insert(Vector((c.x, c.y, 0)), i)
    kd.balance()
    shown = 0
    for o in bpy.data.collections["AR1_buildings"].objects:
        hit = kd.find(Vector((o.location.x, o.location.y, 0)))
        crosses_edge = any(not inside(o.matrix_world @ v.co) for v in o.data.vertices)   # partly off the model
        hide = crosses_edge or (hit[2] is not None and hit[2] < 40)
        o.hide_render = hide; o.hide_set(hide) if o.name in bpy.context.view_layer.objects else None
        shown += not hide
    # roads: drop AR1 road faces that lie on a sketch road surface
    bm = bmesh.new()
    for o in bpy.data.collections["SKETCH"].objects:
        if o.type == "MESH" and o.data.materials and o.data.materials[0] and o.data.materials[0].name.startswith("TPX_ROADS"):
            tmp = bmesh.new(); tmp.from_mesh(o.data); tmp.transform(o.matrix_world)
            for v in tmp.verts:
                v.co.z = 0
            me = bpy.data.meshes.new("_tmp"); tmp.to_mesh(me); tmp.free(); bm.from_mesh(me); bpy.data.meshes.remove(me)
    bvh = BVHTree.FromBMesh(bm); bm.free()
    for name in ("roads_all", "sidewalks"):
        r = bpy.data.objects[name]
        rb = bmesh.new(); rb.from_mesh(r.data)
        kill = [f for f in rb.faces
                if not inside(f.calc_center_median())
                or bvh.ray_cast(Vector((f.calc_center_median().x, f.calc_center_median().y, 5)),
                                Vector((0, 0, -1)), 10)[0] is not None]
        bmesh.ops.delete(rb, geom=kill, context="FACES")
        rb.to_mesh(r.data); rb.free()
    print("AR1 context buildings shown:", shown)


# ---------------------------------------------------------------- one ground, everything on it
def make_gz(objs):
    """Height of the shown ground (GLO-30 plus the fill beyond the AR1 edge) at a point."""
    bm = bmesh.new()
    for o in objs:
        tmp = o.data.copy(); tmp.transform(o.matrix_world); bm.from_mesh(tmp); bpy.data.meshes.remove(tmp)
    bvh = BVHTree.FromBMesh(bm); bm.free()

    def z(p):
        hit = bvh.ray_cast(Vector((p.x, p.y, 500)), Vector((0, 0, -1)))
        if hit[0]:
            return hit[0].z
        near = bvh.find_nearest(Vector((p.x, p.y, 10)))
        return near[0].z if near[0] else 0.0
    return z


def tpx(o, prefix):
    return o.type == "MESH" and o.data.materials and o.data.materials[0] and o.data.materials[0].name.startswith(prefix)


def snap_to_ground(gz):
    """Rest sketch buildings and trees on the ground (lowest ground point under the base), drape the sketch's road and
    park surfaces onto it, and set AR1 context buildings on it. Re-runnable: shifts are recomputed each time."""
    sk = bpy.data.collections["SKETCH"].objects
    moved = 0
    for o in sk:
        if tpx(o, "TPX_BUILDINGS"):
            me = o.data
            z0 = min(v.co.z for v in me.vertices)
            base = [v.co for v in me.vertices if v.co.z < z0 + 0.05]
            dz = min(gz(p) for p in base) - z0
            for v in me.vertices:
                v.co.z += dz
            me.update()
            moved += abs(dz) > 0.05
    trunks = {o.name.replace("trunk", ""): o for o in sk if tpx(o, "TPX_TreeTrunk")}
    for o in sk:
        if tpx(o, "TPX_TreeCrown"):
            t = trunks.get(o.name.replace("crown", ""))
            if not t:
                continue
            z0 = min(v.co.z for v in t.data.vertices)
            c = sum((v.co for v in t.data.vertices), Vector()) / len(t.data.vertices)
            dz = gz(c) - 0.2 - z0
            for me in (t.data, o.data):
                for v in me.vertices:
                    v.co.z += dz
                me.update()
    for o in sk:
        lift = 0.18 if tpx(o, "TPX_ROADS") else 0.12 if tpx(o, "TPX_VEG") else None
        if lift is None:
            continue
        for v in o.data.vertices:
            v.co.z = gz(v.co) + lift
        o.data.update()
    for o in bpy.data.collections["AR1_buildings"].objects:
        foot = [o.matrix_world @ v.co for v in o.data.vertices if v.co.z < 0.05]
        o.location.z = min(gz(p) for p in foot) if foot else gz(o.location)
    print("sketch buildings moved:", moved)


# ---------------------------------------------------------------- extension west and north (generic, labelled)
SKETCH_COVER = (-290.0, 1670.0, -800.0, 295.0)     # x0, x1, y0, y1 of the sketch after alignment
GENERIC_ROADS = {"residential"}                     # terrace fill only along residential streets
TREE_ROADS = {"residential", "tertiary", "unclassified", "secondary", "primary", "trunk"}
ROAD_W = {"motorway": 22, "trunk": 18, "primary": 14, "secondary": 12, "tertiary": 10,
          "unclassified": 6.5, "residential": 7, "service": 4.5,
          "motorway_oneway": 11, "trunk_oneway": 9, "link": 7, "toll_plaza": 30}   # same as style_scene.py


def in_extension(p):
    x0, x1, y0, y1 = SKETCH_COVER
    in_frame = MODEL[0] + 8 <= p.x <= MODEL[1] - 8 and MODEL[2] + 8 <= p.y <= MODEL[3] - 8   # clear of the plinth edge
    return in_frame and not (x0 <= p.x <= x1 and y0 <= p.y <= y1)


def build_extension(gz, mats):
    """Fill the AR1 area outside the sketch in the sketch's manner:
    - street trees along roads (rule-based placement, NOT surveyed);
    - generic terrace rows along residential streets where OSM has no buildings (INVENTED, see 4.2 of the doc).
    Mapped AR1 buildings and roads stay as they are."""
    from mathutils.kdtree import KDTree
    import random
    c = coll("generic_extension")
    roads = []
    for f in load("roads.geojson"):
        roads.append((f["properties"]["c"], densify([proj(*ll) for ll in f["geometry"]["coordinates"]], 3.0)))
    if os.path.exists(os.path.join(GIS, "roads_supplement.geojson")):   # expressway and ramps AR1 missed
        for f in load("roads_supplement.geojson"):
            roads.append((f["properties"]["c"], densify([proj(*ll) for ll in f["geometry"]["coordinates"]], 3.0)))
    road_pts = [(p, k) for k, (cl, pts) in enumerate(roads) for p in pts]
    kd_road = KDTree(len(road_pts))
    for i, (p, _) in enumerate(road_pts):
        kd_road.insert(Vector((p.x, p.y, 0)), i)
    kd_road.balance()
    blocked = []
    for o in bpy.data.collections["AR1_buildings"].objects:
        blocked += [o.matrix_world @ v.co for v in o.data.vertices]
        blocked.append(o.matrix_world.translation.copy())
    for o in bpy.data.collections["RAINREADY_features"].objects:
        if o.name.startswith(("pond_", "water_", "drain_")) and o.type == "MESH":
            blocked += [o.matrix_world @ v.co for v in o.data.vertices]
    kd_b = KDTree(len(blocked))
    for i, p in enumerate(blocked):
        kd_b.insert(Vector((p.x, p.y, 0)), i)
    kd_b.balance()
    ponds = [[proj(*ll) for ll in f["geometry"]["coordinates"][0]] for f in load_all("water.geojson")]

    def in_pond(p):
        for ring in ponds:
            j, ins = len(ring) - 1, False
            for i in range(len(ring)):
                a, b = ring[i], ring[j]
                if (a.y > p.y) != (b.y > p.y) and p.x < (b.x - a.x) * (p.y - a.y) / (b.y - a.y) + a.x:
                    ins = not ins
                j = i
            if ins:
                return True
        return False

    def clear_of_roads(p, own, margin):
        for _, i, d in kd_road.find_range(Vector((p.x, p.y, 0)), 14.0):
            k = road_pts[i][1]
            if k != own and d < ROAD_W.get(roads[k][0], 6) / 2 + margin:
                return False
        return True

    # --- generic terraces
    verts, faces, placed = [], [], []
    for k, (cl, pts) in enumerate(roads):
        if cl not in GENERIC_ROADS:
            continue
        sp = resample(pts, 6.6)
        for i in range(len(sp) - 1):
            a, b = sp[i], sp[i + 1]
            d = b - a; d.z = 0
            if d.length < 3:
                continue
            d.normalize(); n = Vector((-d.y, d.x, 0))
            mid = (a + b) / 2
            for side in (1, -1):
                cen = mid + n * side * (ROAD_W[cl] / 2 + 1.5 + 2.0 + 6.9)
                corners = [cen + d * sx * 3.2 + n * sy * 6.9 for sx in (-1, 1) for sy in (-1, 1)]
                if not all(in_extension(q) for q in corners + [cen]) or in_pond(cen):
                    continue
                if kd_b.find_range(Vector((cen.x, cen.y, 0)), 14.0):
                    continue
                if not all(clear_of_roads(q, k, 1.0) for q in corners + [cen]):
                    continue
                if any((cen - q).length < 6.0 for q in placed[-80:]):
                    continue
                placed.append(cen)
                z = min(gz(q) for q in corners)
                base = len(verts)
                for zz in (z, z + 6.5):
                    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                        verts.append(tuple(cen + d * sx * 3.2 + n * sy * 6.9 + Vector((0, 0, zz))))
                faces += [(base, base + 1, base + 5, base + 4), (base + 1, base + 2, base + 6, base + 5),
                          (base + 2, base + 3, base + 7, base + 6), (base + 3, base, base + 4, base + 7),
                          (base + 4, base + 5, base + 6, base + 7)]
    me = bpy.data.meshes.new("generic_terraces"); me.from_pydata(verts, [], faces); me.update()
    me.materials.append(mats["building"])
    o = bpy.data.objects.new("generic_terraces", me); c.objects.link(o)
    o["invented"] = True
    o["note"] = ("INVENTED: 6.4 x 13.8 x 6.5 m terrace lots placed along residential streets where OSM maps no "
                 "buildings. Shows that houses stand there, not where each one is.")
    # --- street trees, copied from one of the sketch's trees
    sk = bpy.data.collections["SKETCH"].objects
    trunk = next(o for o in sk if tpx(o, "TPX_TreeTrunk"))
    crown = bpy.data.objects[trunk.name.replace("trunk", "crown")]
    tz = min(v.co.z for v in trunk.data.vertices)
    tc = sum((v.co for v in trunk.data.vertices), Vector()) / len(trunk.data.vertices)
    trees = []
    rej = {"area": 0, "blocked": 0, "road": 0, "spacing": 0}
    for k, (cl, pts) in enumerate(roads):
        if cl not in TREE_ROADS:
            continue
        sp = resample(pts, 14.0)
        for i in range(len(sp) - 1):
            a, b = sp[i], sp[i + 1]
            d = b - a; d.z = 0
            if d.length < 5:
                continue
            d.normalize(); n = Vector((-d.y, d.x, 0))
            for side in (1, -1):
                p = a + n * side * (ROAD_W[cl] / 2 + 2.2)
                if not in_extension(p) or in_pond(p):
                    rej["area"] += 1; continue
                if kd_b.find_range(Vector((p.x, p.y, 0)), 5.0):
                    rej["blocked"] += 1; continue
                if not clear_of_roads(p, k, 1.5):
                    rej["road"] += 1; continue
                if any((p - q).length < 8.0 for q in trees[-40:]):
                    rej["spacing"] += 1; continue
                trees.append(p)
    rnd = random.Random(7)
    tv, tf, tm = [], [], []
    for p in trees:
        s = rnd.uniform(0.8, 1.2)
        z = gz(p) - 0.2
        for me_t, mi in ((trunk.data, 0), (crown.data, 1)):
            base = len(tv)
            tv += [((v.co.x - tc.x) * s + p.x, (v.co.y - tc.y) * s + p.y, (v.co.z - tz) * s + z) for v in me_t.vertices]
            for poly in me_t.polygons:
                tf.append(tuple(base + i for i in poly.vertices)); tm.append(mi)
    me = bpy.data.meshes.new("generic_street_trees"); me.from_pydata(tv, [], tf); me.update()
    for poly, mi in zip(me.polygons, tm):
        poly.material_index = mi
    me.materials.append(trunk.data.materials[0]); me.materials.append(crown.data.materials[0])
    o = bpy.data.objects.new("generic_street_trees", me); c.objects.link(o)
    o["invented"] = True
    o["note"] = "Street trees placed by rule (every ~14 m along roads), copied from the sketch's tree. Not surveyed."
    print("generic terraces:", len(placed), "| street trees:", len(trees), "| tree rejections:", rej)


# ---------------------------------------------------------------- road markings and kerbs (look only)
# lines per class: (offset from centreline in m, dashed?) ; widths match ROAD_W. Markings are stylised, NOT surveyed.
MARKINGS = {
    "motorway_oneway": [(-1.8, True), (1.8, True), (-5.0, False), (5.0, False)],
    "motorway": [(0.0, False), (-5.5, True), (5.5, True), (-10.3, False), (10.3, False)],
    "trunk": [(0.0, False), (-4.5, True), (4.5, True), (-8.3, False), (8.3, False)],
    "primary": [(0.0, True), (-6.4, False), (6.4, False)],
    "secondary": [(0.0, True), (-5.4, False), (5.4, False)],
    "tertiary": [(0.0, True), (-4.4, False), (4.4, False)],
    "unclassified": [(0.0, True)],
    "residential": [(0.0, True)],
    "link": [(-3.0, False), (3.0, False)],
}
DASH, GAP, LINE_W = 3.0, 5.0, 0.3


def road_surface_bvh():
    bm = bmesh.new()
    objs = [bpy.data.objects["roads_all"]] + [o for o in bpy.data.collections["SKETCH"].objects if tpx(o, "TPX_ROADS")]
    for o in objs:
        me = o.data.copy(); me.transform(o.matrix_world); bm.from_mesh(me); bpy.data.meshes.remove(me)
    for v in bm.verts:
        v.co.z = 0
    bvh = BVHTree.FromBMesh(bm); bm.free()
    return lambda p: bvh.ray_cast(Vector((p.x, p.y, 5)), Vector((0, 0, -1)), 10)[0] is not None


def build_road_markings(c, gz, mats):
    on_road = road_surface_bvh()
    feats = load("roads.geojson")
    if os.path.exists(os.path.join(GIS, "roads_supplement.geojson")):
        feats += load("roads_supplement.geojson")
    bm = bmesh.new()
    n_dash = 0
    for f in feats:
        rules = MARKINGS.get(f["properties"]["c"])
        if not rules:
            continue
        run = [p for p in densify([proj(*ll) for ll in f["geometry"]["coordinates"]], 1.0)]
        if len(run) < 2:
            continue
        # running distance and a side normal at each sample
        dist, normals = [0.0], []
        for i in range(1, len(run)):
            dist.append(dist[-1] + (run[i] - run[i - 1]).length)
        for i, p in enumerate(run):
            d = run[min(i + 1, len(run) - 1)] - run[max(i - 1, 0)]; d.z = 0
            d = d.normalized() if d.length > 1e-6 else Vector((1, 0, 0))
            normals.append(Vector((-d.y, d.x, 0)))
        for off, dashed in rules:
            seg = []
            for i, p in enumerate(run):
                q = p + normals[i] * off
                visible = (not dashed or (dist[i] % (DASH + GAP)) < DASH) and inside(q) and on_road(q)
                if visible:
                    seg.append((q, normals[i]))
                if (not visible or i == len(run) - 1) and len(seg) > 1:
                    prev = None
                    for q2, n2 in seg:
                        z = gz(q2) + 0.5
                        pair = (bm.verts.new(q2 + n2 * LINE_W / 2 + Vector((0, 0, z))),
                                bm.verts.new(q2 - n2 * LINE_W / 2 + Vector((0, 0, z))))
                        if prev:
                            bm.faces.new([prev[0], prev[1], pair[1], pair[0]])
                        prev = pair
                    n_dash += 1
                if not visible:
                    seg = []
    o = link(c, "road_markings", bm, [mats["marking"]])
    o["note"] = "Stylised lane and centre lines along OSM centrelines, drawn only over road surfaces. Not surveyed."
    print("road marking pieces:", n_dash)


def build_kerbs(c, gz, mats):
    """Light kerb along the outer edges of the sketch's road surfaces (boundary edges after welding the pieces)."""
    bm = bmesh.new()
    for o in bpy.data.collections["SKETCH"].objects:
        if tpx(o, "TPX_ROADS"):
            me = o.data.copy(); me.transform(o.matrix_world); bm.from_mesh(me); bpy.data.meshes.remove(me)
    for v in bm.verts:
        v.co.z = 0
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.3)
    out = bmesh.new()
    n = 0
    for e in bm.edges:
        if len(e.link_faces) != 1:
            continue
        a, b = e.verts[0].co.copy(), e.verts[1].co.copy()
        if (b - a).length < 0.5:
            continue
        run = densify([a, b], 6.0)
        d = (b - a).normalized(); nrm = Vector((-d.y, d.x, 0)) * 0.25
        prev = None
        for p in run:
            z = gz(p) + 0.32
            pair = (out.verts.new(p + nrm + Vector((0, 0, z))), out.verts.new(p - nrm + Vector((0, 0, z))))
            if prev:
                out.faces.new([prev[0], prev[1], pair[1], pair[0]])
            prev = pair
        n += 1
    bm.free()
    o = link(c, "road_kerbs", out, [mats["kerb"]])
    o["note"] = "Kerb lines along the edges of the sketch's road surfaces. Look only."
    print("kerb edges:", n)


def restore_original_materials():
    """Undo look_ink.py's material swap, so material-name checks below see the original names."""
    for o in bpy.data.objects:
        if "orig_mats" in o and o.type in ("MESH", "FONT"):
            for i, name in enumerate(o["orig_mats"]):
                if name and name in bpy.data.materials and i < len(o.data.materials):
                    o.data.materials[i] = bpy.data.materials[name]
            del o["orig_mats"]


def run():
    restore_original_materials()
    mats = {
        "bank": material("pond_bank", (0.24, 0.32, 0.17), 0.9),
        "basin_floor": material("basin_floor", (0.22, 0.19, 0.15), 0.95),
        "water": bpy.data.materials["water_surface"],
        "concrete": material("drain_concrete", (0.55, 0.55, 0.52), 0.85),
        "council": material("council_line", (0.95, 0.95, 0.92), 0.5, emit=0.6),
        "label": material("label", (0.15, 0.15, 0.15), 0.6),
        "pin": material("flood_spot_pin", (0.10, 0.28, 0.55), 0.4),
        "plinth": material("plinth_soil", (0.30, 0.22, 0.16), 0.95),
        "marking": material("road_marking", (0.92, 0.90, 0.82), 0.6),
        "kerb": material("kerb", (0.75, 0.74, 0.70), 0.8),
    }
    g, gz = setup_ground()
    feats = coll("RAINREADY_features")
    cutters = coll("_cutters", hide_render=True)
    mats["ground"] = bpy.data.materials["ground"]
    build_outer_ground(feats, gz, mats)
    gz = make_gz([g, bpy.data.objects["ground_sketch_fill"]])
    build_ponds(feats, cutters, gz, mats)
    build_channels(feats, gz, mats)
    build_culverts(feats, gz, mats)
    build_council_line(feats, gz, mats)
    build_pins(feats, gz, mats)
    build_plinth(feats, gz, mats)
    for o in cutters.objects:
        o.display_type = "WIRE"; o.hide_set(True)
    for ground in (g, bpy.data.objects["ground_sketch_fill"]):   # ponds beyond the AR1 edge sit in the fill ground
        mod = ground.modifiers.get("cut") or ground.modifiers.new("cut", "BOOLEAN")
        mod.operation = "DIFFERENCE"; mod.operand_type = "COLLECTION"; mod.collection = cutters
        mod.solver = "EXACT"; mod.use_hole_tolerant = True
        mod.show_viewport = mod.show_render = True
    slab = bpy.data.objects.get("Geom3D")   # the sketch's 20 m base block; AR1 ground is used instead
    if slab:
        slab.hide_set(True); slab.hide_render = True
    # the sketch's own water hatches would lie over the new basins; AR1 ponds replace them
    for o in bpy.data.collections["SKETCH"].objects:
        if o.type == "MESH" and o.data.materials and o.data.materials[0] and o.data.materials[0].name.startswith("TPX_WATER"):
            o.hide_render = True; o.hide_set(True)
    bpy.data.collections["AR1_water"].hide_render = True
    bpy.context.view_layer.layer_collection.children["AR1_water"].hide_viewport = True
    for n in ("AR1_buildings", "AR1_roads"):
        bpy.data.collections[n].hide_render = False
        bpy.context.view_layer.layer_collection.children[n].hide_viewport = False
    trim_context()
    snap_to_ground(gz)
    mats["building"] = bpy.data.materials.get("TPX_BUILDINGS_mat") or bpy.data.materials["facade"]
    build_extension(gz, mats)
    build_road_markings(feats, gz, mats)
    build_kerbs(feats, gz, mats)
    for n in ("AR1_drains", "AR1_council_line"):
        bpy.data.collections[n].hide_render = True
        bpy.context.view_layer.layer_collection.children[n].hide_viewport = True
    print("build_features: done")


run()
