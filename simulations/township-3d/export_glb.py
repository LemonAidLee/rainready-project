"""RainReady township: export the model for the website (step 8, 21 Oct 2026).

Writes exports/township.glb (glTF binary, Y up, custom properties as glTF `extras`, Draco-compressed meshes) and
exports/trees.json, and copies inputs.json and outputs.json next to it, so the website can either show the precomputed scenarios (outputs.json) or recompute them
live with screening.ts (inputs.json). Data contract: TOWNSHIP_3D_AND_SIMULATOR.md 4.7; hand-off notes: section 5.7.

Trees: the 5,007 trees were 70 % of an uncompressed export (merged copies of one tree). They are left out of the
mesh and sent as ONE prototype (`tree_proto`, trunk + crown, base at the origin) plus exports/trees.json, one row per
tree [x, y, z, scale, kind] in Blender coordinates (x east, y north, z up; glTF position = (x, z, -y)), for
instanced drawing on the website. Same placement rule as build_town.py, so the result is identical.

What is left out: hidden objects, the video-only layers (captions, legend, illustrative tag, rain), cameras and
lights. Animations are not exported: the website sets the state itself from the simulator results. Modifiers ARE
applied (the ground's pond cuts are booleans; without them the ground covers the ponds), except the toon outline
hulls (gh_outline), which are switched off for the export: they would double the building geometry.

Materials: the toon shaders do not survive glTF (they arrive as black + white glow, and the zones lose their
transparency), so for the export ONLY every material is swapped for a plain web_* material in the same palette
(look_ghibli.PAL): web_wall_0..4 / web_roof_0..4 per building, web_road, web_water, web_zone_Z01 ... (18 % neutral,
transparent), web_flow, and so on. The .blend keeps its toon look. The website restyles by material name.

Proxy names: the flood-spot objects carry real street names inside the .blend. For the export ONLY they are renamed
spot_1 ... spot_3 (the on-screen names); the internal name goes along as the extra `internal_name`, and the .blend is
restored afterwards.

Pond gauges: the water height is a driver in Blender, which glTF drops, so each *_water object gets
gauge_z_empty / gauge_z_full (metres, Blender Z = glTF Y): height = empty + fill_pct * (full - empty). It is a
display gauge of fill %, NOT a depth.

Run in Blender after drive_scene.py:
    exec(open(r"D:\\Progmata\\SDP\\simulations\\township-3d\\export_glb.py").read())
"""
import bpy, json, os, shutil
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HERE = r"D:\Progmata\SDP\simulations\township-3d"
OUT = os.path.join(HERE, "exports")
PROXY = {"spot_jalan_makyong": "spot_1", "spot_jalan_sumazau": "spot_2", "spot_persiaran_batu_belah": "spot_3"}
VIDEO_ONLY = ("rr_caption", "rr_legend", "rr_illustrative", "rr_rain", "town_trees_")


def gauges():
    """Read the water-height driver at fill 0 and 1 (fill_pct is keyframed, so it cannot simply be set and read)."""
    for o in bpy.data.objects:
        if o.name.endswith("_water") and "fill_pct" in o.keys() and o.animation_data and o.animation_data.drivers:
            fc = next(d for d in o.animation_data.drivers if d.data_path == "location" and d.array_index == 2)
            expr = fc.driver.expression                      # our own expressions: "<a> + min(max(f, 0), 1) * <b>"
            parent_z = o.parent.matrix_world.translation.z if o.parent else 0.0
            zs = [parent_z + eval(expr, {"__builtins__": {}, "min": min, "max": max}, {"f": f}) for f in (0.0, 1.0)]
            o["gauge_z_empty"], o["gauge_z_full"] = round(zs[0], 3), round(zs[1], 3)
            o["gauge_note"] = "Water height = empty + fill_pct * (full - empty), Blender Z = glTF Y. A gauge, not a depth"


def ground_fn():
    bm = __import__("bmesh").new()
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


def tree_instances():
    """One prototype tree object plus the instance list, using build_town.py's placement rule."""
    sk = bpy.data.collections["SKETCH"].objects
    trunk = next(o for o in sk if (o.get("orig_mats") or [""])[0].startswith("TPX_TreeTrunk"))
    crown = bpy.data.objects[trunk.name.replace("trunk", "crown")]
    tz = min(v.co.z for v in trunk.data.vertices)
    tc = sum((v.co for v in trunk.data.vertices), Vector()) / len(trunk.data.vertices)
    verts, faces, mats = [], [], []
    for me_t, mi in ((trunk.data, 0), (crown.data, 1)):
        base = len(verts)
        verts += [(v.co.x - tc.x, v.co.y - tc.y, v.co.z - tz) for v in me_t.vertices]
        for p in me_t.polygons:
            faces.append(tuple(base + j for j in p.vertices)); mats.append(mi)
    me = bpy.data.meshes.new("tree_proto"); me.from_pydata(verts, [], faces); me.update()
    for src in (trunk, crown):
        me.materials.append(src.data.materials[0])
    for p, mi in zip(me.polygons, mats):
        p.material_index = mi
    proto = bpy.data.objects.new("tree_proto", me)
    bpy.context.scene.collection.objects.link(proto)
    proto["note"] = "Prototype tree for instancing; positions in trees.json. Invented layout (build_town.py)"
    plan = json.load(open(os.path.join(HERE, "data", "town_plan.json"), encoding="utf-8"))
    gz = ground_fn()
    rows = [[round(x, 2), round(y, 2), round(gz(x, y) - 0.2, 2), round(s, 3), k] for x, y, s, k in plan["trees"]]
    json.dump(dict(note="Tree instances for tree_proto in township.glb. Rows: [x, y, z, scale, kind] in Blender "
                        "coordinates (x east, y north, z up); glTF / three.js position = (x, z, -y), uniform scale, "
                        "no rotation. INVENTED town layout (build_town.py).", count=len(rows), trees=rows),
              open(os.path.join(OUT, "trees.json"), "w", encoding="utf-8"))
    return proto, len(rows)


NEUTRAL = ((0.93, 0.92, 0.89), 0.18)   # zone overlay before bands (build_zones.NEUTRAL)
EDGE = (0.10, 0.11, 0.14)               # zone edge (build_zones.EDGE)
SKIP_MATS = ("gh_outline", "gh_label_edge")   # only used by the (unexported) outline modifiers


def palette():
    """PAL from look_ghibli.py, read without running it."""
    import ast
    tree = ast.parse(open(os.path.join(HERE, "look_ghibli.py"), encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "PAL":
            return ast.literal_eval(node.value)


def web_mat(name, color, alpha=1.0, rough=0.9, emit=0.0):
    """Plain glTF-friendly material (Principled), so the model reads in any viewer before the site restyles it."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = 0.0
    b.inputs["Alpha"].default_value = alpha
    if emit:
        b.inputs["Emission Color"].default_value = (*color, 1)
        b.inputs["Emission Strength"].default_value = emit
    nt.links.new(b.outputs[0], out.inputs[0])
    if alpha < 1:
        try:
            m.surface_render_method = "BLENDED"
        except (AttributeError, TypeError):
            m.blend_method = "BLEND"
    m.diffuse_color = (*color, alpha)
    m["web_material"] = True
    return m


def swap_materials(objs, pal):
    """Export-only: replace the toon materials (which glTF cannot carry) by web_* materials in the same palette.
    Buildings get web_wall_k / web_roof_k (roof = faces facing up, as in look_ghibli), k picked per building."""
    fixed = {"boundary_curtain": ("web_boundary_curtain", pal["council"][0], 0.25, 0.9, 1.0),
             "zone_edge": ("web_zone_edge", EDGE, 1.0, 1.0, 1.0),
             "rr_flow": ("web_flow", (0.86, 0.96, 1.0), 0.75, 1.0, 1.0),
             "rr_flow_cross": ("web_flow_cross", (1.0, 0.97, 0.80), 0.85, 1.0, 1.0)}
    slots, roofs, done = [], [], set()
    for o in objs:
        data = o.data
        if data is None or data.as_pointer() in done:
            continue
        done.add(data.as_pointer())
        mats = data.materials
        k = sum(map(ord, o.name)) % len(pal["wall"])
        building = False
        for i, m in enumerate(mats):
            if not m or m.name.startswith(SKIP_MATS):
                continue
            n = m.name
            if n.startswith("zone_Z"):
                new = web_mat("web_" + n, NEUTRAL[0], NEUTRAL[1], 1.0, 1.0)
            elif n in fixed:
                new = web_mat(*fixed[n])
            elif n == "gh__building":
                building = True
                new = web_mat(f"web_wall_{k}", pal["wall"][k])
            elif n.startswith("gh__"):
                cat = n[4:]
                new = web_mat("web_" + cat, pal.get(cat, [(0.6, 0.6, 0.6)])[0], 1.0,
                              0.2 if cat == "water" else 0.9, 1.0 if cat == "label" else 0.0)
            else:
                new = web_mat("web_other", (0.6, 0.6, 0.6))
            slots.append((data, i, m)); mats[i] = new
        if building and o.type == "MESH":
            roofs.append((data, len(mats), [p.material_index for p in data.polygons]))
            mats.append(web_mat(f"web_roof_{k}", pal["roof"][k % len(pal["roof"])]))
            ri = len(mats) - 1
            for p in data.polygons:
                if p.normal.z > 0.7:
                    p.material_index = ri
    return slots, roofs


def restore_materials(slots, roofs):
    for data, n, idx in roofs:
        for p, i in zip(data.polygons, idx):
            p.material_index = i
        while len(data.materials) > n:
            data.materials.pop()
    for data, i, m in slots:
        data.materials[i] = m
    for m in [m for m in bpy.data.materials if m.get("web_material") and m.users == 0]:
        bpy.data.materials.remove(m)


def run():
    scene = bpy.context.scene
    scene.frame_set(scene.frame_start)        # neutral state: clear day, normal pond levels
    gauges()
    os.makedirs(OUT, exist_ok=True)
    proto, n_trees = tree_instances()
    vl = bpy.context.view_layer
    keep = [o for o in vl.objects
            if o.type in ("MESH", "FONT", "CURVE") and o.visible_get() and not o.hide_render
            and not o.name.startswith(VIDEO_ONLY)] + [proto]
    # the what-if pond is hidden and shrunk at frame 1: export it full size, tagged with its scenario
    held = []
    for n in ("pond_whatif", "pond_whatif_water"):
        o = bpy.data.objects.get(n)
        if o:
            held.append((o, o.animation_data.action if o.animation_data else None))
            if o.animation_data:
                o.animation_data.action = None
            o.hide_render = False; o.hide_viewport = False; o.hide_set(False)
            if n == "pond_whatif":
                o.scale = (1, 1, 1)
            o["shown_in_scenario"] = "upstream_plus_pond"
            if o not in keep:
                keep.append(o)
    renamed = {}
    for old, new in PROXY.items():
        o = bpy.data.objects.get(old)
        if o:
            o["internal_name"] = old
            o.name = new; renamed[new] = old
    swapped = ([], [])
    # apply modifiers (the ground's pond cuts are booleans) but not the toon outline hulls
    outlines = [m for o in keep for m in o.modifiers if m.type == "SOLIDIFY" and m.name == "gh_outline"]
    outline_state = [(m, m.show_viewport, m.show_render) for m in outlines]
    try:
        for m in outlines:
            m.show_viewport = m.show_render = False
        swapped = swap_materials(keep, palette())
        bpy.ops.object.select_all(action="DESELECT")
        for o in keep:
            o.select_set(True)
        path = os.path.join(OUT, "township.glb")
        bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_extras=True,
                                  export_yup=True, export_apply=True, export_animations=False,
                                  export_cameras=False, export_lights=False,
                                  export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6)
    finally:
        for m, v, r in outline_state:
            m.show_viewport, m.show_render = v, r
        restore_materials(*swapped)
        for new, old in renamed.items():
            bpy.data.objects[new].name = old
        bpy.ops.object.select_all(action="DESELECT")
        me = proto.data; bpy.data.objects.remove(proto); bpy.data.meshes.remove(me)
        for o, act in held:
            o.animation_data.action = act
        scene.frame_set(scene.frame_start)
    for f in ("inputs.json", "outputs.json"):
        shutil.copy2(os.path.join(HERE, f), os.path.join(OUT, f))
    print("exported", len(keep), "objects ->", path, round(os.path.getsize(path) / 1e6, 1), "MB;", n_trees,
          "tree instances ->", round(os.path.getsize(os.path.join(OUT, "trees.json")) / 1e6, 2), "MB")


run()
