"""RainReady township: build the clean town layout in Blender (team leader, 20 Oct 2026).

Exports the kept buildings and the sketch's parks, runs plan_town.py (system Python with shapely) when they changed,
then builds roads, pavements, lanes, kerbs, markings, new buildings, trees and park paths on the ground, and hides the
pieces it replaces (the sketch's road patches and scattered trees, the AR1 road strips, the first generic fill).

Run order:  style_scene.py -> build_features.py -> build_town.py -> look_ghibli.py
    exec(open(r"D:\\Progmata\\SDP\\simulations\\township-3d\\build_town.py").read())
Everything built here is INVENTED for a clean simulated township; the flood features are untouched.
"""
import bpy, bmesh, hashlib, json, os, subprocess
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HERE = r"D:\Progmata\SDP\simulations\township-3d"
DATA = os.path.join(HERE, "data")
LIFT = {"roads": 0.48, "lanes": 0.46, "walks": 0.56, "markings": 0.60, "kerbs": 0.60, "paths": 0.30}


def orig(o):
    om = o.get("orig_mats")
    if om:
        return om[0]
    return o.data.materials[0].name if o.type == "MESH" and o.data.materials and o.data.materials[0] else ""


def hull2d(pts):
    pts = sorted(set((round(p[0], 2), round(p[1], 2)) for p in pts))
    if len(pts) < 3:
        return pts
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def export_kept():
    blds = []
    for o in bpy.data.collections["SKETCH"].objects:
        if o.type == "MESH" and orig(o).startswith("TPX_BUILDINGS") and not o.hide_render:
            ws = [o.matrix_world @ v.co for v in o.data.vertices]
            z0 = min(w.z for w in ws)
            blds.append(dict(src="sketch", name=o.name, ring=hull2d([(w.x, w.y) for w in ws if w.z < z0 + 0.1])))
    for o in bpy.data.collections["AR1_buildings"].objects:
        if not o.hide_render:
            blds.append(dict(src="ar1", name=o.name, ring=hull2d([(o.matrix_world @ v.co)[:2] for v in o.data.vertices])))
    parks = []
    for o in bpy.data.collections["SKETCH"].objects:
        if o.type == "MESH" and orig(o).startswith("TPX_VEG"):
            for p in o.data.polygons:
                parks.append([tuple((o.matrix_world @ o.data.vertices[i].co)[:2]) for i in p.vertices])
    txt = json.dumps(dict(buildings=blds, sketch_parks=parks))
    path = os.path.join(DATA, "kept_features.json")
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if old != txt:
        os.makedirs(DATA, exist_ok=True)
        open(path, "w", encoding="utf-8").write(txt)
    return old != txt


def ensure_plan(changed):
    plan = os.path.join(DATA, "town_plan.json")
    newer = os.path.exists(plan) and os.path.getmtime(plan) >= max(
        os.path.getmtime(os.path.join(HERE, "plan_town.py")), os.path.getmtime(os.path.join(DATA, "kept_features.json")))
    if changed or not newer:
        print("running plan_town.py (a few minutes) ...")
        r = subprocess.run(["python", os.path.join(HERE, "plan_town.py")], capture_output=True, text=True, cwd=HERE)
        print(r.stdout[-800:], r.stderr[-800:])
    return json.load(open(plan, encoding="utf-8"))


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
        me = o.data
        bpy.data.objects.remove(o)
        if me and me.users == 0:
            bpy.data.meshes.remove(me)
    return c


def mesh_obj(c, name, verts, faces, mat, props=None):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me); c.objects.link(o)
    for k, v in (props or {}).items():
        o[k] = v
    return o


def tri_mesh(c, name, tris, lift, gz, mat, props=None):
    idx, verts, faces = {}, [], []
    for t in tris:
        f = []
        for x, y in t:
            k = (x, y)
            if k not in idx:
                idx[k] = len(verts); verts.append((x, y, gz(x, y) + lift))
            f.append(idx[k])
        if len(set(f)) == 3:
            faces.append(f)
    return mesh_obj(c, name, verts, faces, mat, props)


def line_mesh(c, name, lines, width, lift, gz, mat, props=None):
    verts, faces = [], []
    for ln in lines:
        prev = None
        for i, (x, y) in enumerate(ln):
            a = Vector(ln[max(i - 1, 0)] + [0]); b = Vector(ln[min(i + 1, len(ln) - 1)] + [0])
            d = (b - a); d.z = 0
            if d.length < 1e-6:
                continue
            d.normalize(); n = Vector((-d.y, d.x, 0)) * width / 2
            z = gz(x, y) + lift
            verts += [(x + n.x, y + n.y, z), (x - n.x, y - n.y, z)]
            cur = len(verts) - 2
            if prev is not None:
                faces.append((prev, prev + 1, cur + 1, cur))
            prev = cur
    return mesh_obj(c, name, verts, faces, mat, props)


def hide(o):
    o.hide_render = True
    if o.name in bpy.context.view_layer.objects:
        o.hide_set(True)


def run():
    changed = export_kept()
    plan = ensure_plan(changed)
    gz = ground_fn()
    M = bpy.data.materials
    town = coll("TOWN")
    inv = {"invented": True, "note": "Clean simulated-town layout (plan_town.py). Not surveyed."}
    tri_mesh(town, "town_roads", plan["roads"], LIFT["roads"], gz, M["road_asphalt"], inv)
    tri_mesh(town, "town_lanes", plan["lanes"], LIFT["lanes"], gz, M["road_asphalt"], inv)
    tri_mesh(town, "town_walks", plan["walks"], LIFT["walks"], gz, M["sidewalk"], inv)
    tri_mesh(town, "town_markings", plan["markings"], LIFT["markings"], gz, M["road_marking"], inv)
    line_mesh(town, "town_kerbs", plan["kerbs"], 0.35, LIFT["kerbs"], gz, M["kerb"], inv)
    line_mesh(town, "town_park_paths", plan["paths"], 3.0, LIFT["paths"], gz, M["sidewalk"], inv)
    # buildings: one object each, so each gets its own wall and roof colour
    for i, b in enumerate(plan["buildings"]):
        ring = b["ring"][:-1] if b["ring"][0] == b["ring"][-1] else b["ring"]
        z0 = min(gz(x, y) for x, y in ring)
        cx = sum(x for x, _ in ring) / len(ring); cy = sum(y for _, y in ring) / len(ring)
        n = len(ring)
        verts = [(x - cx, y - cy, 0) for x, y in ring] + [(x - cx, y - cy, b["h"]) for x, y in ring]
        faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))] + \
                [(k, (k + 1) % n, n + (k + 1) % n, n + k) for k in range(n)]
        o = mesh_obj(town, f"town_bld_{i:04d}", verts, faces, M["TPX_BUILDINGS_mat"],
                     dict(inv, kind=b["kind"], height_m=b["h"]))
        o.location = (cx, cy, z0)
    # trees: copies of one sketch tree, one object per kind (street, park, pond, green)
    sk = bpy.data.collections["SKETCH"].objects
    trunk = next(o for o in sk if orig(o).startswith("TPX_TreeTrunk"))
    crown = bpy.data.objects[trunk.name.replace("trunk", "crown")]
    tz = min(v.co.z for v in trunk.data.vertices)
    tc = sum((v.co for v in trunk.data.vertices), Vector()) / len(trunk.data.vertices)
    for kind in sorted({t[3] for t in plan["trees"]}):
        tv, tf, tm = [], [], []
        for x, y, s, k in plan["trees"]:
            if k != kind:
                continue
            z = gz(x, y) - 0.2
            for me_t, mi in ((trunk.data, 0), (crown.data, 1)):
                base = len(tv)
                tv += [((v.co.x - tc.x) * s + x, (v.co.y - tc.y) * s + y, (v.co.z - tz) * s + z) for v in me_t.vertices]
                for p in me_t.polygons:
                    tf.append(tuple(base + j for j in p.vertices)); tm.append(mi)
        o = mesh_obj(town, f"town_trees_{kind}", tv, tf, M[trunk.data.materials[0].name if "orig_mats" not in trunk else trunk["orig_mats"][0]], inv)
        o.data.materials.append(M[crown["orig_mats"][0] if "orig_mats" in crown else crown.data.materials[0].name])
        for p, mi in zip(o.data.polygons, tm):
            p.material_index = mi
    # hide what the clean layout replaces (kept in the file, not rendered)
    n = 0
    for o in sk:
        if o.type == "MESH" and orig(o).startswith(("TPX_ROADS", "TPX_Tree")):
            hide(o); n += 1
    for name in ("roads_all", "sidewalks", "road_markings", "road_kerbs"):
        if bpy.data.objects.get(name):
            hide(bpy.data.objects[name])
    if "generic_extension" in bpy.data.collections:
        bpy.data.collections["generic_extension"].hide_render = True
        bpy.context.view_layer.layer_collection.children["generic_extension"].hide_viewport = True
    print("town: %d buildings, %d trees; hid %d sketch road/tree objects" % (len(plan["buildings"]), len(plan["trees"]), n))


run()
