"""RainReady township: stylised look (reference: stylised city render chosen by the team leader, 20 Oct 2026).

Run inside Blender (Text Editor or via the MCP):
    exec(open(r"D:\\Progmata\\SDP\\simulations\\township-3d\\style_scene.py").read())

Needs the AR1 layers already imported into collections AR1_terrain, AR1_buildings, AR1_water, AR1_roads.
Everything here is LOOK ONLY. Building heights are AR1's assumptions; road widths are assumptions by class
(ROAD_WIDTH below). Nothing in this file is a measurement.
"""
import bpy, bmesh, json, math, os
from mathutils import Vector
from mathutils.bvhtree import BVHTree

AR1 = r"D:\Progmata\SDP\research\AR1_site_model"

# Assumed carriageway widths in metres by OSM highway class. ASSUMPTIONS, not measured.
ROAD_WIDTH = {"motorway": 22, "trunk": 18, "primary": 14, "secondary": 12, "tertiary": 10,
              "unclassified": 6.5, "residential": 7, "service": 4.5,
              "motorway_oneway": 11, "trunk_oneway": 9, "link": 7, "toll_plaza": 30}
SIDEWALK = {"trunk": 2.5, "tertiary": 2.0, "residential": 1.5, "unclassified": 1.5}
PITCHED = {"house", "semidetached_house"}
# "plain": flat-topped blocks like the architecture sketch (team leader, 20 Oct 2026).
# "stylised": pitched roofs, parapets and rooftop units (the first look, kept for later).
LOOK = "plain"
PITCH_DEG = 25.0
FLOOR_H = 3.3


# ---------------------------------------------------------------- helpers
def mat(name):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return m, nt, bsdf


class Math:
    """Tiny builder for chains of shader math nodes."""
    def __init__(self, nt):
        self.nt = nt

    def op(self, operation, a, b=None):
        n = self.nt.nodes.new("ShaderNodeMath")
        n.operation = operation
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                n.inputs[i].default_value = v
            else:
                self.nt.links.new(v, n.inputs[i])
        return n.outputs[0]

    def between(self, x, lo, hi):
        return self.op("MULTIPLY", self.op("GREATER_THAN", x, lo), self.op("LESS_THAN", x, hi))


def ramp(nt, fac, colors):
    r = nt.nodes.new("ShaderNodeValToRGB")
    els = r.color_ramp.elements
    while len(els) < len(colors):
        els.new(0.5)
    for i, c in enumerate(colors):
        els[i].position = i / (len(colors) - 1)
        els[i].color = (*c, 1)
    r.color_ramp.interpolation = "CONSTANT" if len(colors) > 2 else "LINEAR"
    nt.links.new(fac, r.inputs[0])
    return r.outputs[0]


def mix_rgb(nt, fac, a, b):
    n = nt.nodes.new("ShaderNodeMix")
    n.data_type = "RGBA"
    nt.links.new(fac, n.inputs["Factor"])
    for sock, v in ((n.inputs[6], a), (n.inputs[7], b)):
        if isinstance(v, tuple):
            sock.default_value = (*v, 1)
        else:
            nt.links.new(v, sock)
    return n.outputs[2]


def mix_float(nt, fac, a, b):
    n = nt.nodes.new("ShaderNodeMix")
    n.data_type = "FLOAT"
    nt.links.new(fac, n.inputs["Factor"])
    n.inputs[2].default_value = a
    n.inputs[3].default_value = b
    return n.outputs[0]


# ---------------------------------------------------------------- materials
def facade_material():
    m, nt, bsdf = mat("facade")
    M = Math(nt)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Position"], sp.inputs[0])
    sn = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Normal"], sn.inputs[0])
    so = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], so.inputs[0])
    # u runs along the wall: P . (-Ny, Nx); v is height above the building base (object origin at base)
    u = M.op("SUBTRACT", M.op("MULTIPLY", sp.outputs[1], sn.outputs[0]), M.op("MULTIPLY", sp.outputs[0], sn.outputs[1]))
    v = so.outputs[2]
    bh = nt.nodes.new("ShaderNodeAttribute"); bh.attribute_type = "OBJECT"; bh.attribute_name = "bh"
    shop = nt.nodes.new("ShaderNodeAttribute"); shop.attribute_type = "OBJECT"; shop.attribute_name = "shop"
    wx = M.op("FRACT", M.op("DIVIDE", u, 3.0))
    wy = M.op("FRACT", M.op("DIVIDE", v, FLOOR_H))
    wall = M.op("LESS_THAN", M.op("ABSOLUTE", sn.outputs[2]), 0.5)
    below_top = M.op("LESS_THAN", v, M.op("SUBTRACT", bh.outputs["Fac"], 1.1))
    win = M.op("MULTIPLY", M.between(wx, 0.22, 0.78), M.between(wy, 0.30, 0.80))
    win = M.op("MULTIPLY", win, M.op("MULTIPLY", below_top, M.op("GREATER_THAN", v, 0.6)))
    # shops: glazed ground floor instead of punched windows
    ground = M.op("LESS_THAN", v, FLOOR_H)
    is_shop_ground = M.op("MULTIPLY", shop.outputs["Fac"], ground)
    shopwin = M.op("MULTIPLY", M.between(wx, 0.05, 0.95), M.between(v, 0.25, 2.7))
    win = M.op("MAXIMUM", M.op("MULTIPLY", win, M.op("SUBTRACT", 1.0, is_shop_ground)),
               M.op("MULTIPLY", shopwin, is_shop_ground))
    win = M.op("MULTIPLY", win, wall)
    band = M.op("MULTIPLY", M.op("LESS_THAN", wy, 0.07), M.op("GREATER_THAN", v, 2.0))
    # colours: wall tint per building, glass varies per window
    oi = nt.nodes.new("ShaderNodeObjectInfo")
    wall_col = ramp(nt, oi.outputs["Random"], [(0.72, 0.60, 0.44), (0.60, 0.60, 0.58), (0.80, 0.76, 0.66),
                                              (0.50, 0.40, 0.31), (0.70, 0.56, 0.40), (0.45, 0.47, 0.50)])
    wall_col = mix_rgb(nt, M.op("MULTIPLY", band, 0.35), wall_col, (0.35, 0.33, 0.30))
    cell = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(M.op("FLOOR", M.op("DIVIDE", u, 3.0)), cell.inputs[0])
    nt.links.new(M.op("FLOOR", M.op("DIVIDE", v, FLOOR_H)), cell.inputs[1])
    wn = nt.nodes.new("ShaderNodeTexWhiteNoise"); wn.noise_dimensions = "3D"
    nt.links.new(cell.outputs[0], wn.inputs["Vector"])
    glass = ramp(nt, wn.outputs["Value"], [(0.04, 0.07, 0.11), (0.22, 0.30, 0.40)])
    nt.links.new(mix_rgb(nt, win, wall_col, glass), bsdf.inputs["Base Color"])
    rough = nt.nodes.new("ShaderNodeMix"); rough.data_type = "FLOAT"
    nt.links.new(win, rough.inputs["Factor"]); rough.inputs[2].default_value = 0.85; rough.inputs[3].default_value = 0.12
    nt.links.new(rough.outputs[0], bsdf.inputs["Roughness"])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.8
    bump.inputs["Distance"].default_value = 0.15
    nt.links.new(M.op("SUBTRACT", 1.0, win), bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return m


def roof_tile_material():
    m, nt, bsdf = mat("roof_tile")
    M = Math(nt)
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Position"], sp.inputs[0])
    oi = nt.nodes.new("ShaderNodeObjectInfo")
    base = ramp(nt, oi.outputs["Random"], [(0.62, 0.20, 0.08), (0.52, 0.16, 0.07)])
    stripe = M.op("LESS_THAN", M.op("FRACT", M.op("DIVIDE", sp.outputs[2], 0.32)), 0.18)
    nt.links.new(mix_rgb(nt, M.op("MULTIPLY", stripe, 0.4), base, (0.25, 0.07, 0.03)), bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.7
    return m


def flat_material(name, color, rough=0.8, noise=True):
    m, nt, bsdf = mat(name)
    if noise:
        tex = nt.nodes.new("ShaderNodeTexNoise"); tex.inputs["Scale"].default_value = 0.4
        nt.links.new(mix_rgb(nt, M_fac(nt, tex.outputs["Fac"]), tuple(c * 0.9 for c in color), color),
                     bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = rough
    return m


def M_fac(nt, fac):
    return fac


def road_material():
    """Asphalt with white edge lines and a dashed centre line. Uses attributes hw (half width) and UV (u=metres along, v=metres across)."""
    m, nt, bsdf = mat("road_asphalt")
    M = Math(nt)
    uv = nt.nodes.new("ShaderNodeUVMap"); uv.uv_map = "road"
    s = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(uv.outputs[0], s.inputs[0])
    hw = nt.nodes.new("ShaderNodeAttribute"); hw.attribute_name = "hw"
    across = M.op("ABSOLUTE", s.outputs[1])
    wide = M.op("GREATER_THAN", hw.outputs["Fac"], 3.2)
    centre = M.op("MULTIPLY", M.op("LESS_THAN", across, 0.08),
                  M.op("LESS_THAN", M.op("FRACT", M.op("DIVIDE", s.outputs[0], 9.0)), 0.5))
    edge = M.between(across, M.op("SUBTRACT", hw.outputs["Fac"], 0.55), M.op("SUBTRACT", hw.outputs["Fac"], 0.4))
    line = M.op("MULTIPLY", M.op("MAXIMUM", centre, edge), wide)
    tex = nt.nodes.new("ShaderNodeTexNoise"); tex.inputs["Scale"].default_value = 0.8
    asphalt = ramp(nt, tex.outputs["Fac"], [(0.10, 0.10, 0.11), (0.16, 0.16, 0.17)])
    nt.links.new(mix_rgb(nt, line, asphalt, (0.85, 0.85, 0.82)), bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.9
    return m


def water_material():
    m, nt, bsdf = mat("water_surface")
    bsdf.inputs["Base Color"].default_value = (0.10, 0.30, 0.42, 1)
    bsdf.inputs["Roughness"].default_value = 0.06
    tex = nt.nodes.new("ShaderNodeTexNoise"); tex.inputs["Scale"].default_value = 0.15
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.08
    nt.links.new(tex.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs[0], bsdf.inputs["Normal"])
    return m


# ---------------------------------------------------------------- buildings
def reset_buildings():
    """Re-import AR1 buildings so the styling can be re-run from clean footprints."""
    coll = bpy.data.collections["AR1_buildings"]
    for o in list(coll.objects):
        me = o.data
        bpy.data.objects.remove(o)
        if me.users == 0:
            bpy.data.meshes.remove(me)
    lc = bpy.context.view_layer.layer_collection.children[coll.name]
    bpy.context.view_layer.active_layer_collection = lc
    bpy.ops.wm.obj_import(filepath=os.path.join(AR1, "buildings.obj"), forward_axis="Y", up_axis="Z",
                          use_split_groups=True)


def footprint(o):
    """Ordered, counter-clockwise footprint (x, y) from the top face of an AR1 box, plus base z and height."""
    me = o.data
    zs = [v.co.z for v in me.vertices]
    z0, z1 = min(zs), max(zs)
    # the OBJ roof can be split into triangles: walk the outer boundary of all faces lying at the top
    tops = [p for p in me.polygons if all(abs(me.vertices[i].co.z - z1) < 1e-3 for i in p.vertices)]
    count = {}
    for p in tops:
        for e in p.edge_keys:
            count[e] = count.get(e, 0) + 1
    nxt = {}
    for p in tops:
        vs = list(p.vertices)
        for k in range(len(vs)):
            e = (vs[k], vs[(k + 1) % len(vs)])
            if count[tuple(sorted(e))] == 1:
                nxt[e[0]] = e[1]
    start = next(iter(nxt))
    ring, cur = [start], nxt[start]
    while cur != start and len(ring) <= len(nxt):
        ring.append(cur); cur = nxt[cur]
    pts = [me.vertices[i].co.to_2d() for i in ring]
    clean = []
    for p in pts:
        if not clean or (p - clean[-1]).length > 0.05:
            clean.append(p)
    if len(clean) > 3 and (clean[0] - clean[-1]).length < 0.05:
        clean.pop()
    area = sum(clean[i].x * clean[(i + 1) % len(clean)].y - clean[(i + 1) % len(clean)].x * clean[i].y
               for i in range(len(clean)))
    if area < 0:
        clean.reverse()
    return clean, z0, z1 - z0


def inset_ring(pts, t):
    out = []
    n = len(pts)
    for i in range(n):
        dp = (pts[i] - pts[i - 1]).normalized(); dn = (pts[(i + 1) % n] - pts[i]).normalized()
        np_, nn = Vector((-dp.y, dp.x)), Vector((-dn.y, dn.x))
        bis = (np_ + nn)
        bis = bis.normalized() if bis.length > 1e-6 else nn
        out.append(pts[i] + bis * (t / max(0.3, bis.dot(nn))))
    return out


def style_buildings(mats):
    tan = math.tan(math.radians(PITCH_DEG))
    for o in list(bpy.data.collections["AR1_buildings"].objects):
        btype = o.name.split("_", 1)[1].rsplit(".", 1)[0]
        pts, z0, h = footprint(o)
        c2 = sum(pts, Vector((0, 0))) / len(pts)
        pts = [p - c2 for p in pts]
        bm = bmesh.new()
        n = len(pts)
        base = [bm.verts.new((p.x, p.y, 0)) for p in pts]
        top = [bm.verts.new((p.x, p.y, h)) for p in pts]
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new([base[i], base[j], top[j], top[i]])            # walls, facade
        pitched = LOOK == "stylised" and btype in PITCHED and n == 4
        if pitched:
            p3 = [Vector((p.x, p.y, 0)) for p in pts]
            e0, e1 = p3[1] - p3[0], p3[2] - p3[1]
            # ridge parallel to the street = along the lot's SHORT side, so a terrace row reads as one roof
            R = (e0 if e0.length < e1.length else e1).normalized()
            S = Vector((-R.y, R.x, 0))
            a = max(abs(q.dot(R)) for q in p3)
            b = max(abs(q.dot(S)) for q in p3)
            eave = 0.6
            zr, ze = h + b * tan, h - eave * tan
            V = lambda r, s, z: bm.verts.new(R * r + S * s + Vector((0, 0, z)))
            B = b + eave
            for f in (bm.faces.new([V(-a, -B, ze), V(a, -B, ze), V(a, 0, zr), V(-a, 0, zr)]),
                      bm.faces.new([V(-a, B, ze), V(-a, 0, zr), V(a, 0, zr), V(a, B, ze)])):
                f.material_index = 2
            bm.faces.new([V(a, -b, h), V(a, b, h), V(a, 0, zr)])          # gable ends, facade
            bm.faces.new([V(-a, b, h), V(-a, -b, h), V(-a, 0, zr)])
            bh = h
        elif LOOK == "plain":
            bm.faces.new(top).material_index = 1                           # flat roof, no parapet
            bh = h
        else:
            ph = 0.9
            inner = inset_ring(pts, 0.3)
            up = [bm.verts.new((p.x, p.y, h + ph)) for p in pts]
            iu = [bm.verts.new((p.x, p.y, h + ph)) for p in inner]
            il = [bm.verts.new((p.x, p.y, h)) for p in inner]
            for i in range(n):
                j = (i + 1) % n
                bm.faces.new([top[i], top[j], up[j], up[i]])                # parapet outer face
                bm.faces.new([up[i], up[j], iu[j], iu[i]])                  # cap (wall colour)
                bm.faces.new([iu[i], iu[j], il[j], il[i]])                  # parapet inner face
            bm.faces.new(il).material_index = 1                             # roof deck
            bh = h + ph
        bm.normal_update()
        me = bpy.data.meshes.new(o.name)
        bm.to_mesh(me); bm.free()
        for k in ("facade", "roof_flat", "roof_tile"):
            me.materials.append(mats[k])
        old = o.data
        o.data = me
        bpy.data.meshes.remove(old)
        o.location = (c2.x, c2.y, z0)
        o["bh"] = bh
        o["btype"] = btype
        o["shop"] = 1.0 if btype in ("retail", "commercial") else 0.0
        o["parapet"] = 0 if (pitched or LOOK == "plain") else 1
        o["height_source"] = "ASSUMED from OSM building type (AR1), not measured"


def rooftop_units_modifier():
    """Geometry nodes: scatter boxes (AC units, tanks) on flat-roof faces (material roof_flat)."""
    ng = bpy.data.node_groups.get("rooftop_units")
    if ng:
        bpy.data.node_groups.remove(ng)
    ng = bpy.data.node_groups.new("rooftop_units", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N, L = ng.nodes, ng.links
    gi, go = N.new("NodeGroupInput"), N.new("NodeGroupOutput")
    sel = N.new("GeometryNodeMaterialSelection"); sel.inputs[0].default_value = bpy.data.materials["roof_flat"]
    dist = N.new("GeometryNodeDistributePointsOnFaces")
    dist.distribute_method = "POISSON"
    dist.inputs["Distance Min"].default_value = 3.5
    dist.inputs["Density Max"].default_value = 0.015
    L.new(gi.outputs[0], dist.inputs["Mesh"]); L.new(sel.outputs[0], dist.inputs["Selection"])
    cube = N.new("GeometryNodeMeshCube")
    tr = N.new("GeometryNodeTransform"); tr.inputs["Translation"].default_value = (0, 0, 0.5)
    L.new(cube.outputs[0], tr.inputs[0])
    inst = N.new("GeometryNodeInstanceOnPoints")
    L.new(dist.outputs["Points"], inst.inputs["Points"]); L.new(tr.outputs[0], inst.inputs["Instance"])
    rv = N.new("FunctionNodeRandomValue"); rv.data_type = "FLOAT_VECTOR"
    rv.inputs["Min"].default_value = (1.2, 1.2, 0.8); rv.inputs["Max"].default_value = (3.0, 2.5, 1.8)
    L.new(rv.outputs["Value"], inst.inputs["Scale"])
    setm = N.new("GeometryNodeSetMaterial"); setm.inputs[2].default_value = bpy.data.materials["rooftop_unit"]
    L.new(inst.outputs[0], setm.inputs[0])
    join = N.new("GeometryNodeJoinGeometry")
    L.new(setm.outputs[0], join.inputs[0]); L.new(gi.outputs[0], join.inputs[0])
    L.new(join.outputs[0], go.inputs[0])
    for o in bpy.data.collections["AR1_buildings"].objects:
        if o.get("parapet") and not o.modifiers.get("rooftop_units"):
            o.modifiers.new("rooftop_units", "NODES").node_group = ng


# ---------------------------------------------------------------- roads
def build_roads(mats):
    for name in [o.name for o in bpy.data.objects if o.name.startswith(("roads_", "sidewalks"))]:
        bpy.data.objects.remove(bpy.data.objects[name])
    for me in [m for m in bpy.data.meshes if m.name.startswith(("roads_all", "sidewalks")) and m.users == 0]:
        bpy.data.meshes.remove(me)
    classes = [f["properties"]["c"] for f in json.load(open(os.path.join(AR1, "gis", "roads.geojson"), encoding="utf-8"))["features"]]
    lines, verts, cur = [], [], None
    for ln in open(os.path.join(AR1, "roads.obj"), encoding="utf-8"):
        if ln.startswith("g "):
            cur = []; lines.append(cur)
        elif ln.startswith("v "):
            x, y, z = map(float, ln.split()[1:4]); verts.append(Vector((x, y, z)))
        elif ln.startswith("l "):
            cur.extend(verts[int(i) - 1] for i in ln.split()[1:])
    assert len(lines) == len(classes), (len(lines), len(classes))
    # roads AR1 missed (e.g. the expressway through the toll plaza), fetched from OSM later; see the file's "note"
    sup = os.path.join(AR1, "gis", "roads_supplement.geojson")
    if os.path.exists(sup):
        for f in json.load(open(sup, encoding="utf-8"))["features"]:
            lines.append([Vector(((lon - 101.436) * 111158.0, (lat - 3.09) * 110572.0, 0.0))
                          for lon, lat in f["geometry"]["coordinates"]])
            classes.append(f["properties"]["c"])
    # drape on the ground actually shown (GLO-30 once build_features has set it up), else on the SRTM terrain
    terr = bpy.data.objects.get("terrain_cop30") or bpy.data.objects["terrain"]
    tbm = bmesh.new(); tbm.from_mesh(terr.data); tbm.transform(terr.matrix_world)
    bvh = BVHTree.FromBMesh(tbm)

    def ground(p):
        hit = bvh.ray_cast(Vector((p.x, p.y, 500)), Vector((0, 0, -1)))
        return hit[0].z if hit[0] else p.z

    def ribbon(bm, uvl, hwl, pts, hw, lift):
        # split long OSM segments into ~6 m pieces: the strip then follows the ground, and later trimming
        # (build_features.trim_context) removes only the pieces that really lie under a sketch road
        fine = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            n = max(1, int((b - a).length // 6.0))
            fine += [a.lerp(b, k / n) for k in range(1, n + 1)]
        pts = [Vector((p.x, p.y, ground(p) + lift)) for p in fine]
        if len(pts) < 2:
            return
        left, right, dist, s = [], [], [], 0.0
        for i, p in enumerate(pts):
            d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]); d.z = 0
            if d.length < 1e-6:
                d = Vector((1, 0, 0))
            d.normalize(); n = Vector((-d.y, d.x, 0))
            if i:
                s += (p - pts[i - 1]).length
            left.append(bm.verts.new(p + n * hw)); right.append(bm.verts.new(p - n * hw)); dist.append(s)
        for i in range(len(pts) - 1):
            f = bm.faces.new([left[i], right[i], right[i + 1], left[i + 1]])
            for loop in f.loops:
                j = i if loop.vert in (left[i], right[i]) else i + 1
                loop[uvl].uv = (dist[j], hw if loop.vert in left else -hw)
            for v in f.verts:
                v[hwl] = hw

    groups = {}
    for pts, c in zip(lines, classes):
        groups.setdefault(c, []).append(pts)
    rank = {k: i for i, k in enumerate(["service", "unclassified", "residential", "tertiary", "secondary",
                                         "primary", "trunk", "motorway"])}
    for kind in ("road", "sidewalk"):
        bm = bmesh.new(); uvl = bm.loops.layers.uv.new("road"); hwl = bm.verts.layers.float.new("hw")
        for c, plist in groups.items():
            w = ROAD_WIDTH.get(c, 6)
            if kind == "sidewalk":
                if c not in SIDEWALK:
                    continue
                w += 2 * SIDEWALK[c]
            lift = (0.30 + 0.01 * rank.get(c, 0)) if kind == "road" else 0.22
            for pts in plist:
                ribbon(bm, uvl, hwl, pts, w / 2, lift)
        me = bpy.data.meshes.new("roads_all" if kind == "road" else "sidewalks")
        bm.to_mesh(me); bm.free()
        me.materials.append(mats["road_asphalt"] if kind == "road" else mats["sidewalk"])
        ob = bpy.data.objects.new(me.name, me)
        ob["width_source"] = "ASSUMED by OSM class (style_scene.py ROAD_WIDTH), not measured"
        bpy.data.collections["AR1_roads"].objects.link(ob)
    tbm.free()
    for o in bpy.data.collections["AR1_roads"].objects:
        if not o.name.startswith(("roads_", "sidewalks")):
            o.hide_render = True; o.hide_viewport = True


# ---------------------------------------------------------------- ground, water, light
def style_ground_water(mats):
    t = bpy.data.objects["terrain"]
    t.data.materials.clear(); t.data.materials.append(mats["ground"])
    for p in t.data.polygons:
        p.use_smooth = True
    for o in list(bpy.data.collections["AR1_water"].objects):
        area = sum(p.area for p in o.data.polygons)
        if area < 1000:  # the 216 m2 basin: not a pond (AR1); dropped per TOWNSHIP_3D_AND_SIMULATOR.md 4.1
            bpy.data.objects.remove(o); continue
        o.data.materials.clear(); o.data.materials.append(mats["water_surface"])
        o.location.z = 0.35  # sit above the smoothed terrain so it shows


def lighting():
    scn = bpy.context.scene
    sun = bpy.data.objects.get("Sun")
    if not sun:
        sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN")); scn.collection.objects.link(sun)
    sun.data.energy = 4.0
    sun.data.angle = math.radians(1.5)
    sun.data.color = (1.0, 0.96, 0.9)
    sun.rotation_euler = (math.radians(50), 0, math.radians(35))
    w = scn.world or bpy.data.worlds.new("World"); scn.world = w
    w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground"); bg.inputs["Strength"].default_value = 1.0
    sky = nt.nodes.new("ShaderNodeTexSky")
    sky.sky_type = "PREETHAM"
    try:
        sky.sun_direction = sun.matrix_world.to_3x3() @ Vector((0, 0, 1))
        sky.turbidity = 3.0
    except Exception as e:
        print("sky:", e)
    nt.links.new(sky.outputs[0], bg.inputs[0]); nt.links.new(bg.outputs[0], out.inputs["Surface"])
    # No world volume: in EEVEE it fills infinite distance and turns the frame black. Haze, if wanted, goes in
    # the compositor (mist pass) instead.
    bg.inputs["Strength"].default_value = 0.25
    scn.view_settings.view_transform = "AgX"
    scn.view_settings.exposure = -0.4
    for attr, val in (("use_raytracing", True), ("use_shadows", True), ("taa_render_samples", 64)):
        try:
            setattr(scn.eevee, attr, val)
        except Exception as e:
            print("eevee:", attr, e)


def run():
    mats = {
        "facade": facade_material(),
        "roof_tile": roof_tile_material(),
        "roof_flat": flat_material("roof_flat", (0.58, 0.58, 0.56)),
        "rooftop_unit": flat_material("rooftop_unit", (0.72, 0.72, 0.70), noise=False),
        "ground": flat_material("ground", (0.26, 0.32, 0.20), rough=0.95),
        "sidewalk": flat_material("sidewalk", (0.55, 0.54, 0.52)),
        "road_asphalt": road_material(),
        "water_surface": water_material(),
    }
    reset_buildings()
    style_buildings(mats)
    if LOOK == "stylised":
        rooftop_units_modifier()
    build_roads(mats)
    style_ground_water(mats)
    lighting()
    print("style_scene: done")


run()
