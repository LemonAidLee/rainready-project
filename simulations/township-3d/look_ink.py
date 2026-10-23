"""RainReady township: plain ink-and-tone look (reference: "Lines + tone" image chosen by the team leader, 20 Oct 2026).

White surfaces, black outlines (Freestyle, render only), screen-space halftone dots for faces turned from the sun,
dense dots to black in shadow. Run last, after style_scene.py and build_features.py:
    exec(open(r"D:\\Progmata\\SDP\\simulations\\township-3d\\look_ink.py").read())

Swaps each material slot to an "ink__<original>" material and remembers the original in the object's custom property
"orig_mats", so restore_colour() can bring the colour look back.
"""
import bpy, math

DOT_PX = 5.0          # halftone cell size in pixels at the render resolution
LINE_PX = 1.0         # Freestyle line thickness in pixels
SUN_REF = 0.9         # lit brightness that counts as full white (sun 4.0 gives about 4/pi = 1.27 on a white face
                      # facing it; ground at this sun angle gets about 0.8-0.9)
WALL_FLOOR = 0.45     # minimum tone on walls, so shaded walls get dots instead of solid black

# Base lightness per original material (1 = white paper, 0 = solid black)
TONE = [("TPX_BUILDINGS", 1.0), ("facade", 1.0), ("roof_", 1.0), ("TPX_TreeCrown", 0.85), ("TPX_TreeTrunk", 0.5),
        ("TPX_ROADS", 0.92), ("road_asphalt", 0.92), ("sidewalk", 0.97), ("TPX_VEG", 0.8), ("ground", 1.0),
        ("water", 0.45), ("pond_bank", 0.92), ("basin_floor", 0.5), ("drain_concrete", 0.75),
        ("council_line", 1.0), ("label", 0.0), ("flood_spot_pin", 0.0)]
NO_LINES = ("terrain_cop30", "ground_sketch_fill", "terrain")


def tone_for(name):
    for prefix, v in TONE:
        if name.startswith(prefix):
            return v
    return 1.0


def ink_group():
    ng = bpy.data.node_groups.get("ink_tone")
    if ng:
        bpy.data.node_groups.remove(ng)
    ng = bpy.data.node_groups.new("ink_tone", "ShaderNodeTree")
    ng.interface.new_socket("Base", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    ng.interface.new_socket("Shader", in_out="OUTPUT", socket_type="NodeSocketShader")
    N, L = ng.nodes, ng.links
    gi, go = N.new("NodeGroupInput"), N.new("NodeGroupOutput")

    def op(o, a, b=None):
        n = N.new("ShaderNodeMath"); n.operation = o
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                n.inputs[i].default_value = v
            else:
                L.new(v, n.inputs[i])
        return n.outputs[0]

    # how lit is this point? (diffuse of the base grey, measured after lighting)
    diff = N.new("ShaderNodeBsdfDiffuse")
    grey = N.new("ShaderNodeCombineColor")
    for k in range(3):
        L.new(gi.outputs["Base"], grey.inputs[k])
    L.new(grey.outputs[0], diff.inputs["Color"])
    s2r = N.new("ShaderNodeShaderToRGB"); L.new(diff.outputs[0], s2r.inputs[0])
    bw = N.new("ShaderNodeRGBToBW"); L.new(s2r.outputs["Color"], bw.inputs[0])
    v = op("MINIMUM", op("DIVIDE", bw.outputs[0], SUN_REF), 1.0)
    # walls never go fully black (they read as dotted tone, as in the reference); cast shadows on flat ground do
    geo = N.new("ShaderNodeNewGeometry")
    nz = N.new("ShaderNodeSeparateXYZ"); L.new(geo.outputs["Normal"], nz.inputs[0])
    is_wall = op("LESS_THAN", op("ABSOLUTE", nz.outputs[2]), 0.5)
    v = op("MAXIMUM", v, op("MULTIPLY", is_wall, WALL_FLOOR))
    # screen-space dot grid, rotated 45 degrees
    tc = N.new("ShaderNodeTexCoord")
    sc = N.new("ShaderNodeVectorMath"); sc.operation = "MULTIPLY"
    L.new(tc.outputs["Window"], sc.inputs[0])
    res = bpy.context.scene.render
    sc.inputs[1].default_value = (res.resolution_x / DOT_PX, res.resolution_y / DOT_PX, 0)
    rot = N.new("ShaderNodeVectorRotate"); rot.rotation_type = "Z_AXIS"; rot.inputs["Angle"].default_value = math.radians(45)
    L.new(sc.outputs[0], rot.inputs["Vector"])
    fr = N.new("ShaderNodeVectorMath"); fr.operation = "FRACTION"; L.new(rot.outputs[0], fr.inputs[0])
    ce = N.new("ShaderNodeVectorMath"); ce.operation = "SUBTRACT"; L.new(fr.outputs[0], ce.inputs[0])
    ce.inputs[1].default_value = (0.5, 0.5, 0)
    ln = N.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"; L.new(ce.outputs[0], ln.inputs[0])
    # dot radius grows as the point gets darker: none above 0.8, cells fully black below about 0.1
    darkness = op("MAXIMUM", op("DIVIDE", op("SUBTRACT", 0.8, v), 0.7), 0.0)
    radius = op("MULTIPLY", op("POWER", op("MINIMUM", darkness, 1.0), 0.5), 0.75)
    ink = op("LESS_THAN", ln.outputs["Value"], radius)
    paper = op("SUBTRACT", 1.0, ink)
    col = N.new("ShaderNodeCombineColor")
    for k in range(3):
        L.new(paper, col.inputs[k])
    em = N.new("ShaderNodeEmission"); L.new(col.outputs[0], em.inputs["Color"])
    L.new(em.outputs[0], go.inputs["Shader"])
    return ng


def ink_material(orig_name, ng):
    name = "ink__" + orig_name
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    g = nt.nodes.new("ShaderNodeGroup"); g.node_tree = ng
    g.inputs["Base"].default_value = tone_for(orig_name)
    nt.links.new(g.outputs[0], out.inputs["Surface"])
    return m


def apply_ink():
    ng = ink_group()
    cache = {}
    for o in bpy.data.objects:
        if o.type not in ("MESH", "FONT") or not o.data.materials:
            continue
        mats = o.data.materials
        orig = list(o.get("orig_mats", [])) or [m.name if m else "" for m in mats]
        o["orig_mats"] = orig
        for i, name in enumerate(orig):
            if not name:
                continue
            if name not in cache:
                cache[name] = ink_material(name, ng)
            mats[i] = cache[name]
    print("ink materials:", len(cache))


def restore_colour():
    for o in bpy.data.objects:
        if "orig_mats" in o and o.type in ("MESH", "FONT"):
            for i, name in enumerate(o["orig_mats"]):
                if name and name in bpy.data.materials:
                    o.data.materials[i] = bpy.data.materials[name]
            del o["orig_mats"]


def lines_and_world():
    scn = bpy.context.scene
    vl = bpy.context.view_layer
    # ground pieces get no outlines (their 30 m grid would draw noise)
    nl = bpy.data.collections.get("_no_lines") or bpy.data.collections.new("_no_lines")
    for n in NO_LINES:
        o = bpy.data.objects.get(n)
        if o and o.name not in nl.objects:
            nl.objects.link(o)
    scn.render.use_freestyle = True
    scn.render.line_thickness_mode = "ABSOLUTE"
    scn.render.line_thickness = LINE_PX
    fs = vl.freestyle_settings
    fs.crease_angle = math.radians(130)
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new("ink")
    ls.select_by_visibility = True; ls.visibility = "VISIBLE"
    ls.select_by_edge_types = True
    ls.select_silhouette = ls.select_border = ls.select_crease = ls.select_external_contour = True
    ls.select_by_collection = True; ls.collection = nl; ls.collection_negation = "EXCLUSIVE"
    ls.linestyle.color = (0, 0, 0)
    ls.linestyle.thickness = LINE_PX
    # world: white paper for the camera, a dim sky for the lighting that drives the tone
    w = scn.world; nt = w.node_tree
    out = next(n for n in nt.nodes if n.type == "OUTPUT_WORLD")
    sky_bg = next(n for n in nt.nodes if n.type == "BACKGROUND")
    paper = nt.nodes.get("paper") or nt.nodes.new("ShaderNodeBackground"); paper.name = "paper"
    paper.inputs["Color"].default_value = (1, 1, 1, 1); paper.inputs["Strength"].default_value = 1.0
    lp = nt.nodes.get("lp") or nt.nodes.new("ShaderNodeLightPath"); lp.name = "lp"
    mix = nt.nodes.get("mixbg") or nt.nodes.new("ShaderNodeMixShader"); mix.name = "mixbg"
    nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs[0])
    nt.links.new(sky_bg.outputs[0], mix.inputs[1]); nt.links.new(paper.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    scn.view_settings.view_transform = "Standard"
    scn.view_settings.exposure = 0.0
    # sun from the east-north-east, so walls facing the usual south-west cameras fall into tone, not plain white
    sun = bpy.data.objects.get("Sun")
    if sun:
        sun.rotation_euler = (math.radians(48), 0, math.radians(115))


apply_ink()
lines_and_world()
print("look_ink: done")
