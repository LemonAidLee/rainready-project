"""RainReady township: Ghibli-inspired painted look (team leader, 20 Oct 2026).

Soft two-tone cel shading with cool blue-violet shadows, a faint painted texture, warm sun, gradient sky with
cumulus clouds, distance haze, and thin warm outlines on buildings. Real-time in EEVEE: it shows the same in the
viewport, in stills and in video (no Freestyle).

PALETTE RULE: the scene stays soft and low-saturation, and avoids the hues the flood-risk bands will use
(saturated green, amber, red). So: no red or orange roofs, sage-teal (not yellow-green) trees, khaki (not ochre)
ground, indigo (not red) flood pins. The bands, drawn later in strong colour, will then stand out.

Run last, after style_scene.py and build_features.py:
    exec(open(r"D:\\Progmata\\SDP\\simulations\\township-3d\\look_ghibli.py").read())
Swaps material slots to "gh__<category>" and remembers the originals in "orig_mats" (same as look_ink.py).
"""
import bpy, math

SUN_REF = 0.9                       # lit brightness counted as fully lit (see look_ink.py)
SHADOW_TINT = (0.50, 0.54, 0.80)    # shadows go cool blue-violet, never black
HAZE = (0.80, 0.87, 0.94)           # distance haze colour (matches the sky horizon)
HAZE_NEAR, HAZE_FAR, HAZE_MAX = 1500.0, 5000.0, 0.30
OUTLINE = (0.20, 0.16, 0.16)        # warm dark brown, not black
OUTLINE_M = 0.6                     # outline thickness in metres (inverted hull)

# category -> list of colours (one picked per object at random, for a hand-painted variety)
PAL = {
    "wall": [(0.96, 0.92, 0.82), (0.93, 0.88, 0.78), (0.98, 0.95, 0.88), (0.90, 0.87, 0.80), (0.94, 0.90, 0.86)],
    "roof": [(0.42, 0.42, 0.46), (0.34, 0.40, 0.41), (0.48, 0.44, 0.42), (0.30, 0.32, 0.35), (0.40, 0.46, 0.44)],  # greys, NOT blue: water stays the only blue
    "crown": [(0.26, 0.47, 0.36), (0.22, 0.42, 0.34), (0.32, 0.52, 0.38), (0.25, 0.44, 0.40)],
    "trunk": [(0.42, 0.33, 0.28)],
    "road": [(0.20, 0.21, 0.25)],   # darker asphalt so cream markings read
    "sidewalk": [(0.62, 0.60, 0.55)],
    "park": [(0.30, 0.42, 0.24)],
    "ground": [(0.36, 0.44, 0.27)],   # linear values: shows as a soft sage meadow
    "water": [(0.14, 0.46, 0.78)],
    "bank": [(0.33, 0.43, 0.28)],
    "floor": [(0.42, 0.46, 0.44)],
    "drain": [(0.74, 0.74, 0.72)],
    "council": [(0.99, 0.98, 0.94)],
    "label": [(1.0, 1.0, 1.0)],          # area and spot tags: pure white, unshaded, with a navy outline (LABEL_EDGE)
    "pin": [(0.24, 0.25, 0.58)],
    "plinth": [(0.30, 0.22, 0.17)],
    "marking": [(0.93, 0.91, 0.84)],
    "kerb": [(0.70, 0.69, 0.66)],
}
CATS = [("TPX_BUILDINGS", "building"), ("facade", "building"), ("roof_", "building"), ("rooftop", "building"),
        ("TPX_TreeCrown", "crown"), ("TPX_TreeTrunk", "trunk"), ("TPX_ROADS", "road"), ("road_asphalt", "road"),
        ("sidewalk", "sidewalk"), ("TPX_VEG", "park"), ("ground", "ground"), ("water", "water"),
        ("pond_bank", "bank"), ("basin_floor", "floor"), ("drain_concrete", "drain"), ("council_line", "council"),
        ("label", "label"), ("flood_spot_pin", "pin"), ("plinth", "plinth"), ("road_marking", "marking"), ("kerb", "kerb")]
OUTLINED = ("SKETCH", "AR1_buildings", "generic_extension", "TOWN")   # collections whose buildings get outlines


def cat_of(name):
    for pre, c in CATS:
        if name.startswith(pre):
            return c
    return "building"


# ---------------------------------------------------------------- shading
def toon_group():
    ng = bpy.data.node_groups.get("ghibli_toon")
    if ng:
        bpy.data.node_groups.remove(ng)
    ng = bpy.data.node_groups.new("ghibli_toon", "ShaderNodeTree")
    ng.interface.new_socket("Color", in_out="INPUT", socket_type="NodeSocketColor").default_value = (1, 1, 1, 1)
    ng.interface.new_socket("Shader", in_out="OUTPUT", socket_type="NodeSocketShader")
    N, L = ng.nodes, ng.links
    gi, go = N.new("NodeGroupInput"), N.new("NodeGroupOutput")

    def math_(op, a, b=None):
        n = N.new("ShaderNodeMath"); n.operation = op
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                n.inputs[i].default_value = v
            else:
                L.new(v, n.inputs[i])
        return n.outputs[0]

    def mix(fac, a, b, blend="MIX"):
        n = N.new("ShaderNodeMix"); n.data_type = "RGBA"; n.blend_type = blend
        if isinstance(fac, (int, float)):
            n.inputs["Factor"].default_value = fac
        else:
            L.new(fac, n.inputs["Factor"])
        for s, v in ((n.inputs[6], a), (n.inputs[7], b)):
            if isinstance(v, tuple):
                s.default_value = (*v, 1)
            else:
                L.new(v, s)
        return n.outputs[2]

    # light amount at this point (white diffuse, after sun, shadows and sky)
    diff = N.new("ShaderNodeBsdfDiffuse")
    s2r = N.new("ShaderNodeShaderToRGB"); L.new(diff.outputs[0], s2r.inputs[0])
    bw = N.new("ShaderNodeRGBToBW"); L.new(s2r.outputs[0], bw.inputs[0])
    lit = math_("DIVIDE", bw.outputs[0], SUN_REF)
    # soft two-tone step: shadow below ~0.32, lit above ~0.5
    step = N.new("ShaderNodeMapRange"); step.interpolation_type = "SMOOTHSTEP"
    L.new(lit, step.inputs["Value"]); step.inputs["From Min"].default_value = 0.32; step.inputs["From Max"].default_value = 0.52
    shade_col = mix(1.0, gi.outputs["Color"], SHADOW_TINT, "MULTIPLY")
    col = mix(step.outputs["Result"], shade_col, gi.outputs["Color"])
    # gentle highlight where fully sunlit
    hi = N.new("ShaderNodeMapRange"); L.new(lit, hi.inputs["Value"])
    hi.inputs["From Min"].default_value = 0.85; hi.inputs["From Max"].default_value = 1.1
    hi.inputs["To Max"].default_value = 0.04
    col = mix(hi.outputs["Result"], col, (1.0, 0.97, 0.88))
    # painted texture: slow world-space brightness wobble, like brush strokes
    geo = N.new("ShaderNodeNewGeometry")
    nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 0.08; nz.inputs["Detail"].default_value = 6
    nz.inputs["Roughness"].default_value = 0.6
    L.new(geo.outputs["Position"], nz.inputs["Vector"])
    wob = N.new("ShaderNodeMapRange"); L.new(nz.outputs["Fac"], wob.inputs["Value"])
    wob.inputs["From Min"].default_value = 0.3; wob.inputs["From Max"].default_value = 0.7
    wob.inputs["To Min"].default_value = 0.93; wob.inputs["To Max"].default_value = 1.05
    wob_c = N.new("ShaderNodeCombineColor")
    for k in range(3):
        L.new(wob.outputs["Result"], wob_c.inputs[k])
    col = mix(1.0, col, wob_c.outputs[0], "MULTIPLY")
    # aerial haze with distance from the camera
    cam = N.new("ShaderNodeCameraData")
    hz = N.new("ShaderNodeMapRange"); L.new(cam.outputs["View Distance"], hz.inputs["Value"])
    hz.inputs["From Min"].default_value = HAZE_NEAR; hz.inputs["From Max"].default_value = HAZE_FAR
    hz.inputs["To Max"].default_value = HAZE_MAX
    col = mix(hz.outputs["Result"], col, HAZE)
    em = N.new("ShaderNodeEmission"); L.new(col, em.inputs["Color"])
    L.new(em.outputs[0], go.inputs["Shader"])
    return ng


def palette_node(nt, cols):
    """Colour picked per object from a palette (constant ramp on Object Info > Random)."""
    if len(cols) == 1:
        rgb = nt.nodes.new("ShaderNodeRGB"); rgb.outputs[0].default_value = (*cols[0], 1)
        return rgb.outputs[0]
    oi = nt.nodes.new("ShaderNodeObjectInfo")
    r = nt.nodes.new("ShaderNodeValToRGB"); r.color_ramp.interpolation = "CONSTANT"
    els = r.color_ramp.elements
    while len(els) < len(cols):
        els.new(0.5)
    for i, c in enumerate(cols):
        els[i].position = i / len(cols); els[i].color = (*c, 1)
    nt.links.new(oi.outputs["Random"], r.inputs[0])
    return r.outputs[0]


def gh_material(cat, ng):
    m = bpy.data.materials.get("gh__" + cat) or bpy.data.materials.new("gh__" + cat)
    m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    g = nt.nodes.new("ShaderNodeGroup"); g.node_tree = ng
    if cat == "building":
        # walls cream, roofs (upward faces) slate / teal / charcoal blue
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Normal"], sep.inputs[0])
        up = nt.nodes.new("ShaderNodeMath"); up.operation = "GREATER_THAN"; up.inputs[1].default_value = 0.7
        nt.links.new(sep.outputs[2], up.inputs[0])
        mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"
        nt.links.new(up.outputs[0], mx.inputs["Factor"])
        nt.links.new(palette_node(nt, PAL["wall"]), mx.inputs[6]); nt.links.new(palette_node(nt, PAL["roof"]), mx.inputs[7])
        nt.links.new(mx.outputs[2], g.inputs["Color"])
        m.diffuse_color = (*PAL["wall"][0], 1)
    elif cat == "label":
        # tags must always read: flat emission, not toon-shaded, so they never dim in shadow or haze
        em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (*PAL["label"][0], 1)
        em.inputs["Strength"].default_value = 1.0
        nt.nodes.remove(g)
        nt.links.new(em.outputs[0], out.inputs["Surface"])
        m.diffuse_color = (*PAL["label"][0], 1)
        return m
    elif cat == "water":
        # clear blue with a few soft light glints
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 0.6; nz.inputs["Detail"].default_value = 3
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].position = 0.62; ramp.color_ramp.elements[0].color = (*PAL["water"][0], 1)
        ramp.color_ramp.elements[1].position = 0.70; ramp.color_ramp.elements[1].color = (0.62, 0.82, 0.95, 1)
        nt.links.new(nz.outputs["Fac"], ramp.inputs[0]); nt.links.new(ramp.outputs[0], g.inputs["Color"])
        m.diffuse_color = (*PAL["water"][0], 1)
    else:
        nt.links.new(palette_node(nt, PAL[cat]), g.inputs["Color"])
        m.diffuse_color = (*PAL[cat][0], 1)
    nt.links.new(g.outputs[0], out.inputs["Surface"])
    return m


def outline_material():
    m = bpy.data.materials.get("gh_outline") or bpy.data.materials.new("gh_outline")
    m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*OUTLINE, 1)
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    m.use_backface_culling = True
    m.diffuse_color = (*OUTLINE, 1)
    return m


def apply_materials():
    ng = toon_group()
    cache = {}
    for o in bpy.data.objects:
        if o.type not in ("MESH", "FONT") or not o.data.materials:
            continue
        mats = o.data.materials
        orig = list(o.get("orig_mats", [])) or [m.name if m else "" for m in mats
                                                 if not (m and m.name in ("gh_outline", "gh_label_edge"))]
        o["orig_mats"] = orig
        for i, name in enumerate(orig):
            # the boundary curtain, zone overlays and simulator layers (rr_*) keep their own flat materials
            if not name or name.startswith(("boundary_", "zone_", "rr_")):
                continue
            c = cat_of(name)
            if c not in cache:
                cache[c] = gh_material(c, ng)
            mats[i] = cache[c]
    print("ghibli materials:", sorted(cache))


LABEL_EDGE = (0.08, 0.11, 0.24)   # navy outline around the white tags
LABEL_EDGE_M = 0.9


def label_outlines():
    """Navy inverted-hull outline on every area and spot tag, so the white text reads on any background."""
    m = bpy.data.materials.get("gh_label_edge") or bpy.data.materials.new("gh_label_edge")
    m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*LABEL_EDGE, 1)
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    m.use_backface_culling = True
    n = 0
    for o in bpy.data.objects:
        if o.type != "FONT" or cat_of((o.get("orig_mats") or [""])[0]) != "label":
            continue
        mats = o.data.materials
        if "gh_label_edge" not in [x.name for x in mats if x]:
            mats.append(m)
        mod = o.modifiers.get("gh_outline") or o.modifiers.new("gh_outline", "SOLIDIFY")
        mod.thickness = LABEL_EDGE_M; mod.offset = 1.0
        mod.use_flip_normals = True; mod.use_rim = False
        mod.material_offset = [x.name if x else "" for x in mats].index("gh_label_edge")
        n += 1
    print("outlined tags:", n)


def outlines():
    """Inverted-hull outlines: a slightly larger, flipped copy drawn only from behind. Real-time and web-portable."""
    om = outline_material()
    n = 0
    for cname in OUTLINED:
        for o in bpy.data.collections[cname].objects:
            if o.type != "MESH" or not o.data.materials or o.hide_render:
                continue
            first = (o.get("orig_mats") or [""])[0]
            if cat_of(first) != "building":
                continue
            mats = o.data.materials
            if "gh_outline" not in [m.name for m in mats if m]:
                mats.append(om)
            idx = [m.name if m else "" for m in mats].index("gh_outline")
            mod = o.modifiers.get("gh_outline") or o.modifiers.new("gh_outline", "SOLIDIFY")
            mod.thickness = OUTLINE_M; mod.offset = 1.0
            mod.use_flip_normals = True; mod.use_rim = False
            mod.material_offset = idx
            mod.show_viewport = mod.show_render = True
            n += 1
    print("outlined objects:", n)


# ---------------------------------------------------------------- sky, sun, render
def sky_and_light():
    scn = bpy.context.scene
    w = scn.world; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nrm = nt.nodes.new("ShaderNodeVectorMath"); nrm.operation = "NORMALIZE"; nt.links.new(tc.outputs["Generated"], nrm.inputs[0])
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(nrm.outputs[0], sep.inputs[0])
    # gradient: pale warm horizon to clear blue zenith
    grad = nt.nodes.new("ShaderNodeValToRGB")
    e = grad.color_ramp.elements
    e[0].position = 0.0; e[0].color = (*HAZE, 1)
    e[1].position = 0.30; e[1].color = (0.20, 0.47, 0.86, 1)
    e.new(0.65).color = (0.12, 0.33, 0.74, 1)
    nt.links.new(sep.outputs[2], grad.inputs[0])
    # cumulus clouds: soft noise blobs, only above the horizon, flattened toward it
    sc = nt.nodes.new("ShaderNodeVectorMath"); sc.operation = "MULTIPLY"; sc.inputs[1].default_value = (1.0, 1.0, 2.6)
    nt.links.new(nrm.outputs[0], sc.inputs[0])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 1.6
    nz.inputs["Detail"].default_value = 8; nz.inputs["Roughness"].default_value = 0.55
    nt.links.new(sc.outputs[0], nz.inputs["Vector"])
    cl = nt.nodes.new("ShaderNodeMapRange"); cl.interpolation_type = "SMOOTHSTEP"
    nt.links.new(nz.outputs["Fac"], cl.inputs["Value"]); cl.inputs["From Min"].default_value = 0.50; cl.inputs["From Max"].default_value = 0.60
    above = nt.nodes.new("ShaderNodeMapRange"); above.interpolation_type = "SMOOTHSTEP"
    nt.links.new(sep.outputs[2], above.inputs["Value"]); above.inputs["From Min"].default_value = 0.03; above.inputs["From Max"].default_value = 0.15
    mask = nt.nodes.new("ShaderNodeMath"); mask.operation = "MULTIPLY"
    nt.links.new(cl.outputs["Result"], mask.inputs[0]); nt.links.new(above.outputs["Result"], mask.inputs[1])
    cloud_col = nt.nodes.new("ShaderNodeMix"); cloud_col.data_type = "RGBA"   # lit tops, cool undersides
    nt.links.new(nz.outputs["Fac"], cloud_col.inputs["Factor"])
    cloud_col.inputs[6].default_value = (0.80, 0.83, 0.92, 1); cloud_col.inputs[7].default_value = (1.0, 0.99, 0.96, 1)
    skymix = nt.nodes.new("ShaderNodeMix"); skymix.data_type = "RGBA"
    nt.links.new(mask.outputs[0], skymix.inputs["Factor"])
    nt.links.new(grad.outputs[0], skymix.inputs[6]); nt.links.new(cloud_col.outputs[2], skymix.inputs[7])
    cam_bg = nt.nodes.new("ShaderNodeBackground"); nt.links.new(skymix.outputs[2], cam_bg.inputs["Color"])
    # what the scene is LIT by: an even soft sky (keeps shadows readable)
    light_bg = nt.nodes.new("ShaderNodeBackground")
    light_bg.inputs["Color"].default_value = (0.75, 0.82, 0.95, 1); light_bg.inputs["Strength"].default_value = 0.35
    lp = nt.nodes.new("ShaderNodeLightPath")
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
    nt.links.new(light_bg.outputs[0], mx.inputs[1]); nt.links.new(cam_bg.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs["Surface"])
    sun = bpy.data.objects["Sun"]
    sun.data.energy = 3.2; sun.data.color = (1.0, 0.93, 0.80); sun.data.angle = math.radians(3)
    sun.data.use_shadow = True
    sun.rotation_euler = (math.radians(52), 0, math.radians(-35))   # late-morning sun from the south-east
    scn.render.engine = "BLENDER_EEVEE"
    scn.render.use_freestyle = False
    scn.view_settings.view_transform = "Standard"
    scn.view_settings.exposure = 0.0
    for o in bpy.data.objects:
        if o.type == "CAMERA":
            o.data.dof.use_dof = False


apply_materials()
outlines()
label_outlines()
sky_and_light()
print("look_ghibli: done")
