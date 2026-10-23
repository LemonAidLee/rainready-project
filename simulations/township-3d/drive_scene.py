"""RainReady township: let the screening simulator drive the scene (step 6, 20 Oct 2026).

Reads outputs.json (screening.py), inputs.json, data/scenario_features.json (plan_zones.py) and builds, in collection
SIMULATOR (everything here is named rr_* and keeps its own flat materials; look_ghibli skips rr_* and zone_*):
  zone colours        each zone_Zxx material keyframed from neutral to its band per scenario
  pond gauge          fill_pct keyframed on pond_A_water / pond_B_water from the simulator's `gauge` (their drivers
                      move the water): storage required as a share of an entered capacity, or, with no capacity
                      (option a), of the largest requirement across the scenarios. A gauge, never a depth
  rr_flow_arrows      animated chevrons along every drain path, in the OSM way direction (usually, not always, the
                      flow direction [verify]); rr_flow_arrows_cross: the one drain that crosses the council line
  rr_rain_*           particle rain; its opacity is keyframed, so the rain fades in and out
  rr_upstream_change  INVENTED low blocks and paved aprons in Z01 that rise for the "upstream change" scenario
  pond_whatif(_water) INVENTED what-if pond on the OSM brownfield in Z06, appears for the "pond added" scenario
  rr_caption_*        captions, legend and a status tag in front of the sequence camera
Every rendered frame also carries the status note through the render stamp, from any camera: "ILLUSTRATIVE VALUES"
while any input is a placeholder, otherwise "SCREENING ESTIMATE - MSMA 2 method, stated assumptions".

Video sequence (24 fps, frames 1-720, camera SEQ_CAMERA): clear day -> rain -> ponds fill -> upstream change ->
pond added -> gap shrinks. See KEYS.

Run after build_zones.py and screening.py:
    exec(open(r"D:\\Progmata\\SDP\\simulations\\township-3d\\drive_scene.py").read())
Re-runnable: it removes its own objects and keyframes first. No depths are shown; the pond water height is a gauge
of fill %, not a depth.
"""
import bpy, bmesh, json, math, os
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HERE = r"D:\Progmata\SDP\simulations\township-3d"
GIS = r"D:\Progmata\SDP\research\AR1_site_model\gis"
SEQ_CAMERA = "cam_overview"
FPS = 24
# key frames of the sequence
KEYS = dict(start=1, rain_on=96, rain_full=144, arrows_on=120, arrows_full=168, fill_end=264, bands_on=216,
            now_hold=264, up_on=312, up_built=360, up_result=432, up_hold=432, pond_on=480, pond_built=528,
            pond_result=600, end=720)
BAND = {"low": ((0.02, 0.36, 0.16), 0.45), "medium": ((0.95, 0.48, 0.02), 0.45),
        "high": ((0.80, 0.04, 0.03), 0.48), "unknown": ((0.36, 0.36, 0.40), 0.30)}
NEUTRAL = ((0.93, 0.92, 0.89), 0.18)      # same as build_zones.NEUTRAL
SCEN = ("now", "upstream", "upstream_plus_pond")
DRY_LEVEL = 0.10                            # pond gauge before the storm: display only
ARROW_LIFT, ARROW_STEP = 0.9, 30.0          # above zone overlay (0.68), zone edge (0.70), council band (0.75)
RAIN_TOP, RAIN_SPEED = 260.0, 55.0          # emitter height (m) and fall speed (m/s): look only


def ground_fn():
    bm = bmesh.new()
    for n in ("terrain_cop30", "ground_sketch_fill"):
        o = bpy.data.objects[n]
        me = o.data.copy(); me.transform(o.matrix_world); bm.from_mesh(me); bpy.data.meshes.remove(me)
    bvh = BVHTree.FromBMesh(bm); bm.free()

    def z(x, y):
        hit = bvh.ray_cast(Vector((x, y, 500)), Vector((0, 0, -1)))
        if hit[0]:
            return hit[0].z
        n = bvh.find_nearest(Vector((x, y, 10)))
        return n[0].z if n[0] else 0.0
    return z


def coll(name):
    c = bpy.data.collections.get(name)
    if not c:
        c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c)
    for o in list(c.objects):
        data = o.data
        bpy.data.objects.remove(o)
        if data and data.users == 0:
            (bpy.data.meshes if isinstance(data, bpy.types.Mesh) else bpy.data.curves).remove(data)
    return c


def link(c, name, bm, mats):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats:
        me.materials.append(m)
    o = bpy.data.objects.new(name, me); c.objects.link(o)
    o.visible_shadow = False
    return o


def flat_material(name, color, alpha=1.0, alpha_node="rr_alpha"):
    """Unlit colour mixed with transparency; the mix node is named so its opacity can be keyframed."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    if nt.animation_data:
        nt.animation_data_clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission"); em.name = "rr_color"; em.inputs["Color"].default_value = (*color, 1)
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader"); mix.name = alpha_node; mix.inputs[0].default_value = alpha
    nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    try:
        m.surface_render_method = "BLENDED"
    except (AttributeError, TypeError):
        m.blend_method = "BLEND"
    m.diffuse_color = (*color, alpha)
    return m


def key(sock_or_obj, path, frame, value=None, const=False):
    if value is not None:
        if path.startswith("["):
            sock_or_obj[path[2:-2]] = value
        else:
            setattr(sock_or_obj, path, value)
    sock_or_obj.keyframe_insert(path, frame=frame)
    if const:
        ad = sock_or_obj.animation_data if hasattr(sock_or_obj, "animation_data") else None
        if ad and ad.action:
            for fc in _fcurves(ad.action):
                if fc.data_path == path:
                    for kp in fc.keyframe_points:
                        kp.interpolation = "CONSTANT"


def _fcurves(action):
    """F-curves of an action (Blender 4.4+ layered actions keep them in channelbags)."""
    if hasattr(action, "fcurves") and len(action.fcurves):
        return list(action.fcurves)
    out = []
    for layer in getattr(action, "layers", []):
        for strip in layer.strips:
            for bag in getattr(strip, "channelbags", []):
                out += list(bag.fcurves)
    return out


def clear_anim(idblock):
    if idblock and idblock.animation_data and idblock.animation_data.action:
        idblock.animation_data.action = None


# ---------------------------------------------------------------- zones and ponds
def drive_zones_and_ponds(res, inp):
    s = res["scenarios"]
    for zid in inp["zones"]:
        o = bpy.data.objects.get("zone_" + zid)
        if not o:
            print("missing zone", zid); continue
        zi = inp["zones"][zid]
        o["c_now"] = zi["c_now"]["value"]; o["c_upstream"] = zi["c_upstream"]["value"]
        o["c_status"] = zi["c_now"]["status"]
        for sc in SCEN:
            o["band_" + sc] = s[sc]["zones"][zid]["band"]
            r = s[sc]["zones"][zid]["ratio"]
            o["ratio_" + sc] = round(r, 3) if r is not None else "n/a"
        o["band"] = s["now"]["zones"][zid]["band"]
        o["values_status"] = "ILLUSTRATIVE - placeholder inputs" if res["illustrative"] else "from inputs.json"
        m = o.data.materials[0]
        nt = m.node_tree
        clear_anim(nt)
        col = nt.nodes["zone_color"].inputs["Color"]; alp = nt.nodes["zone_alpha"].inputs[0]

        def band_key(frame, band):
            c, a = NEUTRAL if band is None else BAND[band]
            col.default_value = (*c, 1); col.keyframe_insert("default_value", frame=frame)
            alp.default_value = a; alp.keyframe_insert("default_value", frame=frame)
        band_key(KEYS["start"], None)
        band_key(KEYS["bands_on"], None)
        band_key(KEYS["fill_end"], s["now"]["zones"][zid]["band"])
        band_key(KEYS["up_built"], s["now"]["zones"][zid]["band"])
        band_key(KEYS["up_result"], s["upstream"]["zones"][zid]["band"])
        band_key(KEYS["pond_built"], s["upstream"]["zones"][zid]["band"])
        band_key(KEYS["pond_result"], s["upstream_plus_pond"]["zones"][zid]["band"])
    for pid, p in inp["ponds"].items():
        w = bpy.data.objects[pid + "_water"]
        clear_anim(w)
        start = DRY_LEVEL
        f = {sc: s[sc]["ponds"][pid]["gauge"] for sc in SCEN}
        for frame, v in ((KEYS["start"], start), (KEYS["rain_full"], start), (KEYS["fill_end"], f["now"]),
                         (KEYS["up_built"], f["now"]), (KEYS["up_result"], f["upstream"]),
                         (KEYS["pond_built"], f["upstream"]), (KEYS["pond_result"], f["upstream_plus_pond"])):
            key(w, '["fill_pct"]', frame, v)
        w["fill_status"] = ("ILLUSTRATIVE: keyframed from outputs.json (placeholder inputs)" if res["illustrative"]
                            else "Gauge keyframed from outputs.json: " + s["now"]["ponds"][pid]["gauge_basis"])
        po = bpy.data.objects[pid]
        for sc in SCEN:
            po["storage_required_m3_" + sc] = round(s[sc]["ponds"][pid]["storage_required_m3"])
            po["change_vs_now_" + sc] = round(s[sc]["ponds"][pid]["change_vs_now"], 3)
            po["gauge_" + sc] = round(s[sc]["ponds"][pid]["gauge"], 3)
        po["capacity_m3_input"] = p["capacity_m3"]["value"] if p["capacity_m3"]["value"] else "none (planner input)"
        po["capacity_note"] = "Option (a): no capacity is claimed; stated_capacity_m3 stays TBD until sourced"
        for k in [k for k in po.keys() if k.startswith(("gap_m3_", "fill_pct_", "capacity_used"))]:
            del po[k]


# ---------------------------------------------------------------- flow arrows
def flow_material(name, color, width_k=0.9, speed=0.8):
    """Chevrons that move along the ribbon's U direction (U = distance / ARROW_STEP). Opacity node: rr_flow."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    if nt.animation_data:
        nt.animation_data_clear()
    N = nt.nodes.new
    out = N("ShaderNodeOutputMaterial")
    uv = N("ShaderNodeUVMap"); uv.uv_map = "flow"
    sep = N("ShaderNodeSeparateXYZ"); nt.links.new(uv.outputs[0], sep.inputs[0])

    def math(op, a, b=None):
        n = N("ShaderNodeMath"); n.operation = op
        for i, x in enumerate((a, b)):
            if x is None:
                continue
            if isinstance(x, (int, float)):
                n.inputs[i].default_value = x
            else:
                nt.links.new(x, n.inputs[i])
        return n.outputs[0]
    t = N("ShaderNodeValue"); t.name = "rr_time"
    fc = t.outputs[0].driver_add("default_value")
    fc.driver.type = "SCRIPTED"; fc.driver.expression = f"frame / {FPS} * {speed}"
    a = math("ABSOLUTE", math("SUBTRACT", sep.outputs[1], 0.5))
    s = math("SUBTRACT", math("ADD", sep.outputs[0], math("MULTIPLY", a, width_k)), t.outputs[0])
    chev = math("LESS_THAN", math("FRACT", s), 0.38)
    strength = N("ShaderNodeValue"); strength.name = "rr_flow"; strength.outputs[0].default_value = 0.0
    fac = math("MULTIPLY", math("MULTIPLY", chev, math("LESS_THAN", a, 0.46)), strength.outputs[0])
    em = N("ShaderNodeEmission"); em.inputs["Color"].default_value = (*color, 1)
    tr = N("ShaderNodeBsdfTransparent")
    mix = N("ShaderNodeMixShader"); nt.links.new(fac, mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    try:
        m.surface_render_method = "BLENDED"
    except (AttributeError, TypeError):
        m.blend_method = "BLEND"
    m.diffuse_color = (*color, 1)
    return m


def seg_cross(a, b, c, d):
    def o(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return o(a, b, c) * o(a, b, d) < 0 and o(c, d, a) * o(c, d, b) < 0


def council_xy():
    f = json.load(open(os.path.join(GIS, "council_line.geojson"), encoding="utf-8"))["features"][0]
    return [((lon - 101.436) * 111158.0, (lat - 3.09) * 110572.0) for lon, lat in f["geometry"]["coordinates"]]


def build_arrows(c, gz):
    council = council_xy()
    main_m = flow_material("rr_flow", (0.86, 0.96, 1.0))
    cross_m = flow_material("rr_flow_cross", (1.0, 0.97, 0.80), width_k=1.1)
    bms = {"rr_flow_arrows": bmesh.new(), "rr_flow_arrows_cross": bmesh.new()}
    crossing = []
    for d in sorted((o for o in bpy.data.objects if o.name.startswith("drain_") and "path" in o.keys()),
                    key=lambda o: o.name):
        pts = [Vector((p[0], p[1], 0)) for p in d["path"]]
        if len(pts) < 2:
            continue
        crosses = any(seg_cross(a[:2], b[:2], p, q) for a, b in zip(pts, pts[1:]) for p, q in zip(council, council[1:]))
        if crosses:
            crossing.append(d.name)
        run = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            n = max(1, int((b - a).length // 4.0))
            run += [a.lerp(b, k / n) for k in range(1, n + 1)]
        main = d.name == "drain_888406336"
        half = 7.0 if crosses else 5.0 if main else 3.0      # wider than the drains: legible from the overview
        bm = bms["rr_flow_arrows_cross" if crosses else "rr_flow_arrows"]
        uvl = bm.loops.layers.uv.get("flow") or bm.loops.layers.uv.new("flow")
        prev, dist = None, 0.0
        for i, p in enumerate(run):
            if i:
                dist += (p - run[i - 1]).length
            t = run[min(i + 1, len(run) - 1)] - run[max(i - 1, 0)]
            if t.length < 1e-6:
                continue
            t.normalize(); n = Vector((-t.y, t.x, 0)) * half
            z = gz(p.x, p.y) + ARROW_LIFT
            pair = (bm.verts.new((p.x + n.x, p.y + n.y, z)), bm.verts.new((p.x - n.x, p.y - n.y, z)), dist)
            if prev:
                f = bm.faces.new([prev[0], prev[1], pair[1], pair[0]])
                u0, u1 = prev[2] / ARROW_STEP, dist / ARROW_STEP
                for loop, uv in zip(f.loops, ((u0, 1.0), (u0, 0.0), (u1, 0.0), (u1, 1.0))):
                    loop[uvl].uv = uv
            prev = pair
    objs = {}
    for name, bm in bms.items():
        o = link(c, name, bm, [cross_m if name.endswith("cross") else main_m])
        o["direction_note"] = "Arrows follow the OSM way direction of each drain: usually, not always, the flow [verify]"
        objs[name] = o
    objs["rr_flow_arrows_cross"]["drains"] = ", ".join(crossing) or "none found"
    objs["rr_flow_arrows_cross"]["note"] = "The one mapped drain that crosses the Klang / Shah Alam council line"
    for m in (main_m, cross_m):
        sock = m.node_tree.nodes["rr_flow"].outputs[0]
        for frame, v in ((KEYS["start"], 0.0), (KEYS["arrows_on"], 0.0), (KEYS["arrows_full"], 1.0)):
            sock.default_value = v; sock.keyframe_insert("default_value", frame=frame)
    print("flow arrows; council-line crossing drain(s):", crossing)


# ---------------------------------------------------------------- rain
def build_rain(c):
    drop_m = flat_material("rr_rain", (0.82, 0.88, 0.96), 0.0, alpha_node="rr_rain_alpha")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= 0.5; v.co.y *= 0.5; v.co.z *= 14.0          # a stylised streak: 0.5 x 0.5 x 14 m
    drop = link(c, "rr_rain_drop", bm, [drop_m])
    drop.location = (0, 0, -2000)                              # source kept far below the plinth, out of every shot
    bm = bmesh.new()
    x0, x1, y0, y1 = -1300, 1780, -900, 680
    v = [bm.verts.new(p) for p in ((x0, y0, 0), (x0, y1, 0), (x1, y1, 0), (x1, y0, 0))]  # clockwise: normal points down
    bm.faces.new(v)
    em = link(c, "rr_rain_emitter", bm, [])
    em.location = (0, 0, RAIN_TOP)
    em.hide_render = False
    ps_mod = em.modifiers.new("rain", "PARTICLE_SYSTEM")
    ps = ps_mod.particle_system.settings
    ps.name = "rr_rain"
    life = int(RAIN_TOP / RAIN_SPEED * FPS) + 6
    ps.count = 220000
    ps.frame_start = -life - 10; ps.frame_end = KEYS["end"] + 1; ps.lifetime = life
    ps.emit_from = "FACE"; ps.use_emit_random = True
    ps.normal_factor = RAIN_SPEED; ps.factor_random = 2.0
    ps.effector_weights.gravity = 0.0
    ps.render_type = "OBJECT"; ps.instance_object = drop
    ps.particle_size = 1.0; ps.size_random = 0.4
    ps.use_rotations = False
    ps.display_method = "DOT"; ps.display_percentage = 10
    em.show_instancer_for_render = False; em.show_instancer_for_viewport = False
    sock = drop_m.node_tree.nodes["rr_rain_alpha"].inputs[0]
    for frame, val in ((KEYS["start"], 0.0), (KEYS["rain_on"], 0.0), (KEYS["rain_full"], 0.7)):
        sock.default_value = val; sock.keyframe_insert("default_value", frame=frame)
    sun = bpy.data.objects.get("Sun")
    if sun:
        clear_anim(sun.data)
        e0 = sun.data.get("rr_dry_energy", sun.data.energy)
        sun.data["rr_dry_energy"] = e0
        for frame, val in ((KEYS["start"], e0), (KEYS["rain_on"], e0), (KEYS["rain_full"], e0 * 0.55)):
            sun.data.energy = val; sun.data.keyframe_insert("energy", frame=frame)


# ---------------------------------------------------------------- scenario features
def build_upstream_change(c, gz, feats):
    """INVENTED blocks and paved aprons that rise in Z01 (shape key 'built' 0 -> 1)."""
    M = bpy.data.materials
    mats = [M.get("gh__sidewalk"), M.get("gh__building") or M.get("gh__sidewalk")]
    bm = bmesh.new()
    lows, highs = [], []
    for b in feats["upstream_change"]:
        za = min(gz(x, y) for x, y in b["apron"])
        ring = [bm.verts.new((x, y, za - 0.6)) for x, y in b["apron"]]
        f = bm.faces.new(ring); f.material_index = 0
        lows += [(v, za + 0.62) for v in ring]
        zr = za + 0.6
        base = [bm.verts.new((x, y, za - 0.6)) for x, y in b["roof"]]
        top = [bm.verts.new((x, y, za - 0.6)) for x, y in b["roof"]]
        bm.faces.new(top).material_index = 1
        for i in range(4):
            j = (i + 1) % 4
            bm.faces.new([base[i], base[j], top[j], top[i]]).material_index = 1
        lows += [(v, zr) for v in base]
        highs += [(v, zr + b["h"]) for v in top]
    bm.normal_update(); bm.verts.index_update()
    order = {v.index: z for v, z in lows + highs}
    me = bpy.data.meshes.new("rr_upstream_change"); bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    o = bpy.data.objects.new("rr_upstream_change", me); c.objects.link(o)
    o.shape_key_add(name="Basis")
    sk = o.shape_key_add(name="built")
    for i, z in order.items():
        sk.data[i].co.z = z
    o["invented"] = True
    o["note"] = ("INVENTED display for the 'upstream change' scenario: more paved land in Area A (Z01). Not a mapped "
                 "or planned development")
    for frame, v in ((KEYS["start"], 0.0), (KEYS["up_on"], 0.0), (KEYS["up_built"], 1.0)):
        sk.value = v; sk.keyframe_insert("value", frame=frame)
    return o


def build_whatif_pond(c, gz, feats, res, inp):
    wp = feats["what_if_pond"]
    ring = [Vector((x, y, 0)) for x, y in wp["ring"]]
    cen = Vector((*wp["centre"], 0))
    zmax = max(gz(p.x, p.y) for p in ring)
    zmin = min(gz(p.x, p.y) for p in ring)
    M = bpy.data.materials
    bm = bmesh.new()                                    # bank: a low wall around the pond, top 1.2 m over the highest ground
    lo = [bm.verts.new((p.x - cen.x, p.y - cen.y, zmin - cen.z - 0.3)) for p in ring]
    hi = [bm.verts.new((p.x - cen.x, p.y - cen.y, zmax + 1.2)) for p in ring]
    for i in range(len(ring)):
        j = (i + 1) % len(ring)
        bm.faces.new([lo[i], lo[j], hi[j], hi[i]])
    flo = [bm.verts.new((p.x - cen.x, p.y - cen.y, zmax + 0.05)) for p in ring]
    bm.faces.new(flo).material_index = 1
    bm.normal_update()
    bank = link(c, "pond_whatif", bm, [M.get("gh__bank"), M.get("gh__floor") or M.get("gh__bank")])
    bank.location = cen
    bm = bmesh.new()
    bm.faces.new([bm.verts.new((p.x - cen.x, p.y - cen.y, 0)) for p in ring])
    w = link(c, "pond_whatif_water", bm, [M.get("gh__water")])
    w.parent = bank
    w["fill_pct"] = 0.0
    fc = w.driver_add("location", 2)
    fc.driver.type = "SCRIPTED"
    v = fc.driver.variables.new(); v.name = "f"; v.type = "SINGLE_PROP"
    v.targets[0].id = w; v.targets[0].data_path = '["fill_pct"]'
    fc.driver.expression = f"{zmax + 0.1:.3f} + min(max(f, 0), 1) * 1.0"
    pond = inp["what_if_pond"]
    bank["invented"] = True; bank["what_if"] = True
    bank["note"] = ("INVENTED what-if pond on land OSM tags brownfield (way 1267917541), zone Z06. Location and size are "
                    "a what-if for the demo, not a proposal")
    bank["capacity_used_m3"] = pond["capacity_m3"]["value"]; bank["capacity_used_status"] = pond["capacity_m3"]["status"]
    bank["area_m2"] = wp["area_m2"]
    wr = res["scenarios"]["upstream_plus_pond"]["what_if_pond"]
    fill = min(1.0, wr["ratio"]) if wr["ratio"] is not None else 1.0
    for frame, s in ((KEYS["start"], 0.01), (KEYS["pond_on"], 0.01), (KEYS["pond_built"], 1.0)):
        bank.scale = (s, s, 1.0); bank.keyframe_insert("scale", frame=frame)
    for frame, f in ((KEYS["start"], 0.0), (KEYS["pond_built"], 0.0), (KEYS["pond_result"], fill)):
        key(w, '["fill_pct"]', frame, f)
    for frame, hidden in ((KEYS["start"], True), (KEYS["pond_on"], False)):
        for o in (bank, w):
            key(o, "hide_render", frame, hidden, const=True)
            key(o, "hide_viewport", frame, hidden, const=True)


# ---------------------------------------------------------------- captions and the status label
def m3(x):
    return f"{round(x / 100.0) * 100:,.0f} m\u00b3"


def pct(r):
    d = round((r - 1.0) * 100)
    return f"{'+' if d > 0 else ''}{d}%"


def captions(res):
    s = res["scenarios"]
    A = {sc: s[sc]["ponds"]["pond_A"] for sc in SCEN}
    B = {sc: s[sc]["ponds"]["pond_B"] for sc in SCEN}
    T = {sc: s[sc]["trunk_drain"] for sc in SCEN}
    storm = f"{s['now']['duration_h']:g}-hour"
    full = T["now"]["ratio"] >= 1.0
    up_ponds = A["upstream"]["change_vs_now"] - 1.0
    return [
        (KEYS["start"], "Clear day. Nine draft drainage zones; two retention ponds (A, B)."),
        (KEYS["rain_on"], f"A 100-year, {storm} design storm (MSMA 2). Water moves west along the drains."),
        (KEYS["now_hold"], f"Today: pond A must hold about {m3(A['now']['storage_required_m3'])}, pond B "
                           f"{m3(B['now']['storage_required_m3'])}" + ("; the shared trunk drain is full." if full else ".")),
        (KEYS["up_on"], "Scenario: more paved land upstream, where peak control is not fully achieved."),
        (KEYS["up_hold"], f"The shared trunk drain carries {round((T['upstream']['change_vs_now'] - 1) * 100)}% more"
                          + (f"; pond A's storage need {pct(A['upstream']['change_vs_now'])}." if up_ponds > 0.005
                             else "; the ponds already hold the whole storm.")),
        (KEYS["pond_on"], "What-if: a pond on vacant land upstream of pond A."),
        (KEYS["pond_result"], f"A what-if pond holding {m3(s['upstream_plus_pond']['what_if_pond']['capacity_m3'] or 0)} "
                              + (f"cuts pond A's storage need by {-round((A['upstream_plus_pond']['change_vs_now'] - 1) * 100)}%."
                                 if A["upstream_plus_pond"]["change_vs_now"] < 0.995 else
                                 f"changes pond A's storage need by {pct(A['upstream_plus_pond']['change_vs_now'])}.")),
    ]


def status_text(res):
    return ("ILLUSTRATIVE VALUES \u00b7 placeholder inputs, not BBR data" if res["illustrative"] else
            "SCREENING ESTIMATE \u00b7 MSMA 2 method \u00b7 not a design, not a forecast")


def text_obj(c, cam, name, body, loc, size, mat, align="LEFT"):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body; cu.size = size; cu.align_x = align; cu.align_y = "CENTER"
    cu.materials.append(mat)
    t = bpy.data.objects.new(name, cu); c.objects.link(t)
    t.parent = cam; t.location = loc
    t.visible_shadow = False
    return t


def plate(c, cam, name, x0, x1, y0, y1, z, mat):
    bm = bmesh.new()
    bm.faces.new([bm.verts.new(p) for p in ((x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z))])
    o = link(c, name, bm, [mat]); o.parent = cam
    return o


def build_captions(c, res):
    cam = bpy.data.objects[SEQ_CAMERA]
    d = 10.0                                                        # metres in front of the lens
    sw = cam.data.sensor_width
    hw = d * sw / 2 / cam.data.lens                                 # half-width of the view at distance d
    r = bpy.context.scene.render
    hh = hw * r.resolution_y / r.resolution_x
    white = flat_material("rr_caption_text", (1.0, 1.0, 1.0), 1.0)
    dark = flat_material("rr_caption_plate", (0.03, 0.04, 0.08), 0.62)
    plate(c, cam, "rr_caption_bar", -hw, hw, -hh, -hh + 0.11 * hh * 2, -d - 0.01, dark)
    for k, (frame, body) in enumerate(captions(res)):
        t = text_obj(c, cam, f"rr_caption_{k}", body, (-hw * 0.95, -hh * 0.89, -d), hh * 0.075, white)
        nxt = captions(res)[k + 1][0] if k + 1 < len(captions(res)) else None
        key(t, "hide_render", KEYS["start"], frame != KEYS["start"], const=True)
        key(t, "hide_viewport", KEYS["start"], frame != KEYS["start"], const=True)
        key(t, "hide_render", frame, False, const=True); key(t, "hide_viewport", frame, False, const=True)
        if nxt:
            key(t, "hide_render", nxt, True, const=True); key(t, "hide_viewport", nxt, True, const=True)
    plate(c, cam, "rr_illustrative_plate", -hw * 0.02, hw, hh * 0.70, hh * 0.84, -d - 0.01, dark)
    t = text_obj(c, cam, "rr_illustrative_tag", status_text(res), (hw * 0.97, hh * 0.77, -d), hh * 0.055, white,
                 align="RIGHT")
    t["note"] = "Status on every frame (also burned in by the render stamp)"
    # band legend, top left, from the moment bands appear
    leg = [plate(c, cam, "rr_legend_plate", -hw, -hw * 0.16, hh * 0.70, hh * 0.84, -d - 0.01, dark)]
    x = -hw * 0.97
    leg.append(text_obj(c, cam, "rr_legend_title", "Zone band:", (x, hh * 0.77, -d), hh * 0.05, white))
    x += hw * 0.17
    for band, label in (("low", "low"), ("medium", "medium"), ("high", "high"), ("unknown", "outlet TBD")):
        col, _ = BAND[band]
        sq = hh * 0.035
        leg.append(plate(c, cam, f"rr_legend_{band}", x, x + 2 * sq, hh * 0.77 - sq, hh * 0.77 + sq, -d,
                         flat_material(f"rr_legend_{band}", col, 1.0)))
        leg.append(text_obj(c, cam, f"rr_legend_{band}_t", label, (x + 2.6 * sq, hh * 0.77, -d), hh * 0.045, white))
        x += hw * 0.15
    for o in leg:
        key(o, "hide_render", KEYS["start"], True, const=True); key(o, "hide_viewport", KEYS["start"], True, const=True)
        key(o, "hide_render", KEYS["bands_on"], False, const=True)
        key(o, "hide_viewport", KEYS["bands_on"], False, const=True)


def stamp(res):
    r = bpy.context.scene.render
    on = True
    r.use_stamp = on
    for a in ("date", "time", "render_time", "frame", "frame_range", "memory", "hostname", "camera", "lens", "scene",
              "marker", "filename", "sequencer_strip", "peak_memory"):
        if hasattr(r, "use_stamp_" + a):
            setattr(r, "use_stamp_" + a, False)
    r.use_stamp_note = on
    r.stamp_note_text = status_text(res).replace("\u00b7", "-")
    r.use_stamp_labels = False
    r.stamp_font_size = 14
    r.stamp_background = (0.03, 0.04, 0.08, 0.75)


def run():
    res = json.load(open(os.path.join(HERE, "outputs.json"), encoding="utf-8"))
    inp = json.load(open(os.path.join(HERE, "inputs.json"), encoding="utf-8"))
    feats = json.load(open(os.path.join(HERE, "data", "scenario_features.json"), encoding="utf-8"))
    scene = bpy.context.scene
    scene.frame_start, scene.frame_end = KEYS["start"], KEYS["end"]
    scene.render.fps = FPS
    scene.camera = bpy.data.objects[SEQ_CAMERA]
    gz = ground_fn()
    c = coll("SIMULATOR")
    drive_zones_and_ponds(res, inp)
    build_arrows(c, gz)
    build_rain(c)
    build_upstream_change(c, gz, feats)
    build_whatif_pond(c, gz, feats, res, inp)
    build_captions(c, res)
    stamp(res)
    scene.frame_set(KEYS["start"])
    print("illustrative:", res["illustrative"], "| frames", scene.frame_start, "-", scene.frame_end,
          "| camera", SEQ_CAMERA)


run()
