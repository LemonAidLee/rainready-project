"""RainReady township: build the DRAFT drainage zones in Blender (step 4, 20 Oct 2026).

Reads data/zones.json (written by plan_zones.py, system Python + shapely) and builds, in collection ZONES:
  zone_Z01 ...        translucent ground overlay per zone, draped on the ground 0.68 m up: above roads (0.48),
                      pavements (0.56) and markings (0.60), below the council band (0.75). Water bodies are cut out,
                      so ponds stay blue. Custom properties follow the data contract (TOWNSHIP_3D_AND_SIMULATOR.md 4.7)
  zone_Z01_edge ...   dark edge line along each zone boundary
  label_zone_Z01 ...  flat white tag, same style as the spot tags
Colours stay NEUTRAL until the screening simulator sets the bands (drive_scene.py). Each zone has its own material
zone_Z01 ... with nodes named "zone_color" (Emission) and "zone_alpha" (Mix), so a band can be set per zone.

Run after look_ghibli.py (look_ghibli skips materials named zone_*):
    exec(open(r"D:\\Progmata\\SDP\\simulations\\township-3d\\build_zones.py").read())
Re-runnable. The zones are a DRAFT, not an official catchment.
"""
import bpy, bmesh, json, os
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HERE = r"D:\Progmata\SDP\simulations\township-3d"
LIFT, EDGE_LIFT, EDGE_W = 0.68, 0.70, 3.0
TAG_Z, TAG_SIZE = 16.0, 32.0
NEUTRAL = ((0.93, 0.92, 0.89), 0.18)     # colour, opacity: neutral until bands exist
EDGE = (0.10, 0.11, 0.14)


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


def zone_material(name, color, alpha):
    """Flat, unlit tint (emission mixed with transparency), so a band colour reads exactly as set."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission"); em.name = em.label = "zone_color"
    em.inputs["Color"].default_value = (*color, 1); em.inputs["Strength"].default_value = 1.0
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader"); mix.name = mix.label = "zone_alpha"
    mix.inputs[0].default_value = alpha
    nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    try:
        m.surface_render_method = "BLENDED"
    except (AttributeError, TypeError):
        m.blend_method = "BLEND"
    m.use_backface_culling = False
    m.diffuse_color = (*color, alpha)
    return m


def edge_material():
    m = bpy.data.materials.get("zone_edge") or bpy.data.materials.new("zone_edge")
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (*EDGE, 1)
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    m.diffuse_color = (*EDGE, 1)
    return m


def inside(pt, ring):
    x, y = pt; c = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def densify(ring, step=8.0):
    out = []
    for a, b in zip(ring, ring[1:]):
        a, b = Vector((*a, 0)), Vector((*b, 0))
        n = max(1, int((b - a).length // step))
        out += [a.lerp(b, k / n) for k in range(n)]
    return out + [Vector((*ring[-1], 0))]


def run():
    data = json.load(open(os.path.join(HERE, "data", "zones.json"), encoding="utf-8"))
    gz = ground_fn()
    c = coll("ZONES")
    em = edge_material()
    tag = bpy.data.objects["label_spot_1"]          # copy the spot tags' look (white, navy outline)
    drains = [o for o in bpy.data.objects if o.name.startswith("drain_") and "path" in o.keys()]
    for z in data["zones"]:
        zid = z["id"]
        # overlay
        idx, verts, faces = {}, [], []
        for t in z["tris"]:
            f = []
            for x, y in t:
                k = (x, y)
                if k not in idx:
                    idx[k] = len(verts); verts.append((x, y, gz(x, y) + LIFT))
                f.append(idx[k])
            if len(set(f)) == 3:
                faces.append(f)
        me = bpy.data.meshes.new("zone_" + zid); me.from_pydata(verts, [], faces); me.update()
        me.materials.append(zone_material("zone_" + zid, *NEUTRAL))
        o = bpy.data.objects.new("zone_" + zid, me); c.objects.link(o)
        o.visible_shadow = False
        # data contract (4.7). Runoff coefficients come from inputs.json; until then TBD here
        rings = [[tuple(p) for p in r] for r in z["outline"]]
        # drains with any path point in the zone (a drain on a zone edge is listed in both zones)
        mids = sorted(d.name for d in drains if any(inside(tuple(p), r) for p in d["path"] for r in rings))
        props = dict(area_ha=z["area_ha"], c_now="TBD", c_upstream="TBD", drains_to=z["drains_to"],
                     council=z["council"], source=data["source"], zone_name=z["name"], route=z["route"],
                     water_area_ha=z["water_area_ha"], holds_water=", ".join(z["holds_water"]) or "none",
                     drain_objects=", ".join(mids) or "none", band="unset",
                     status="DRAFT - not an official catchment",
                     area_note="Measured on plan from the zone outline, water included. Areas are fine to measure; "
                               "depths are not shown")
        for k, v in props.items():
            o[k] = v
        # edge line
        bm = bmesh.new()
        for r in z["outline"]:
            run_ = densify(r)
            prev = None
            for i, p in enumerate(run_):
                d = run_[min(i + 1, len(run_) - 1)] - run_[max(i - 1, 0)]
                if d.length < 1e-6:
                    continue
                d.normalize(); n = Vector((-d.y, d.x, 0)) * EDGE_W / 2
                zz = gz(p.x, p.y) + EDGE_LIFT
                pair = (bm.verts.new((p.x + n.x, p.y + n.y, zz)), bm.verts.new((p.x - n.x, p.y - n.y, zz)))
                if prev:
                    bm.faces.new([prev[0], prev[1], pair[1], pair[0]])
                prev = pair
        me = bpy.data.meshes.new(f"zone_{zid}_edge"); bm.to_mesh(me); bm.free()
        me.materials.append(em)
        e = bpy.data.objects.new(f"zone_{zid}_edge", me); c.objects.link(e)
        e.visible_shadow = False
        e["zone"] = zid
        # tag
        cu = bpy.data.curves.new("label_zone_" + zid, "FONT")
        cu.body = zid; cu.size = TAG_SIZE; cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.extrude = 0.4
        for m in tag.data.materials:
            cu.materials.append(m)
        t = bpy.data.objects.new("label_zone_" + zid, cu); c.objects.link(t)
        lx, ly = z["label"]
        t.location = (lx, ly, gz(lx, ly) + TAG_Z)
        t["orig_mats"] = ["label"]
        t["zone"] = zid
        for src in tag.modifiers:
            mod = t.modifiers.new(src.name, src.type)
            for a in ("thickness", "offset", "use_flip_normals", "use_rim", "material_offset", "use_even_offset"):
                if hasattr(src, a):
                    setattr(mod, a, getattr(src, a))
        print(zid, z["area_ha"], "ha ->", z["drains_to"], "|", len(faces), "faces |", len(mids), "drains")


run()
