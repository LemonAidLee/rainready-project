# 3D Township and Screening Simulator: How We Implement It

**Written for:** the next Claude session and the team (architecture, hydrology, frontend). **As of:** 20 October 2026.
**Builds on:** [RAINREADY_CONCEPT_V2.md](RAINREADY_CONCEPT_V2.md) section 5 (implementation split) and
[../research/AR1_site_model.md](../research/AR1_site_model.md) (the site data).
**Status (21 Oct 2026):** **the 3D township is built** (steps 1–3 of section 6), the **draft drainage zones** are
drawn (step 4, draft, 4.8), and the **screening simulator v2 runs on sourced values** (MSMA 2nd
Edition and public data, [../research/HY_screening_inputs.md](../research/HY_screening_inputs.md); section 5.8). It
drives the scene's keyframed 30 s sequence (5.6) and the **website** ([WEBSITE.md](WEBSITE.md)), and the `.glb`
is exported (5.7). Next: step 7 (render the sequence). **Exception to the research-phase
rule:** the team leader has approved implementation work on these two parts; everything else stays research.

House rules apply: risk bands, never depths · advisory, never forecast · neutral wording · no invented numbers.

**21 Oct 2026, later:** the website was redesigned (WEBSITE.md section 6) and every open marker in this file is settled
in [../research/TBD_VERIFY_RESOLUTION.md](../research/TBD_VERIFY_RESOLUTION.md). **At the next Blender session:** fix
Spot 2's note and caption (it is a retention-pond request, not a flood report) in `build_features.py` / `drive_scene.py`
and re-export the `.glb`.

### Start here (next session)

1. In Blender (5.2, opened from Steam): open `simulations/township-3d/township.blend`, press `N` → *MCP for Blender* →
   *Start MCP Server* → *Connect to Claude*. Check with `get_scene_info`.
2. **Do not rebuild unless something changed.** The saved file is the current model. Rebuild order, one script per
   `execute_blender_code` call (a single call running all of them times out the MCP link, though Blender finishes):
   `style_scene.py` → `build_features.py` → `build_town.py` → `look_ghibli.py` → `build_zones.py` →
   `drive_scene.py`. `build_town.py` calls `plan_town.py` (system Python + shapely, ~4–6 min) only when its inputs
   changed; to avoid the MCP timeout, run `python plan_town.py` from the terminal first. The terminal steps for the
   simulator part: `python plan_zones.py` (zones and scenario features, ~10 s) before `build_zones.py`, and
   `python screening.py` (writes `outputs.json`) before `drive_scene.py`.
3. **When an input changes:** edit `inputs.json` → `python screening.py --check` →
   `python screening.py` → re-run `drive_scene.py`. To redraw a zone: edit `ZONES` / cut lines in
   `plan_zones.py` → `python plan_zones.py` → `build_zones.py` → update `area_ha` in `inputs.json` (screening warns
   if they differ) → screening → `drive_scene.py`.
4. Then **step 7: render** the sequence (camera `cam_overview`, frames 1–720) and stills. After any change, re-run
   `export_glb.py` (website package) and `check_parity.ts` (if `screening.py` changed).

**What the model is now (one paragraph for the deck appendix):** a *simulated* township loosely based on Bandar Bukit
Raja. Mapped features from AR1 / OpenStreetMap: retention ponds A and B (water level driven by `fill_pct`), the main
ditch and 59 drains (10 short gaps bridged as *inferred culverts*), the Klang / Shah Alam council line, flood-spot pins,
the full OSM road network including the West Coast Expressway. The architecture student's sketch buildings are kept.
Everything else (172 rows of terraces and shophouses, parks, lawns, 5,007 trees, pavements, markings) is an **invented**
clean town layout, capped so the built footprint (~325,000 m²) sits inside the estimate for real BBR. Look:
Ghibli-inspired painted style (section 4.6). Renders: `simulations/township-3d/renders/town_v*_*.png`.

**Model area (20 Oct 2026, team leader):** a rectangle, **x −1,222 to +1,700 m, y −830 to +608 m** (about
2.9 × 1.4 km), constant `MODEL` in `build_features.py` and `OUTLINE` in `plan_town.py`. AR1's own data and GLO-30
ground cover only the AR1 extent (x ±1,222, y ±608); outside it the ground is continued from the AR1 edge
(`ground_sketch_fill`, look only), roads come from `roads_full_osm.geojson`, and water and drains from
[`water_supplement.geojson`](../research/AR1_site_model/gis/water_supplement.geojson) (4 water bodies, incl. a 4.9 ha
flood retention pond on the east side) and [`drains_supplement.geojson`](../research/AR1_site_model/gis/drains_supplement.geojson)
(5 drains), Overpass 20 Oct 2026, ODbL. The council line now runs to the east edge, and the Shah Alam label sits in the
upper-right corner. The building budget still applies only to the AR1 extent; the new corners get houses only on
OSM residential land (none mapped there), so they are roads, lawns and trees. Render:
`renders/town_v4_rect_overview.png`.

**Proxy names on screen (20 Oct 2026, team leader):** the model shows proxy names only. Labels float 24 m up (above
roofs and trees); spot tags float above each pin. The real places are kept in each object's `proxy_for` property and
in this table (team use; the deck states the mapping once, see below).

| On screen        | Stands for                                                            | Object                                          |
| ---------------- | --------------------------------------------------------------------- | ----------------------------------------------- |
| **AREA A** | Setia Alam, Shah Alam council side (upstream); confirmed 21 Oct 2026 (Seksyen U13, OSM) | `label_area_A`                                |
| **AREA B** | Bandar Bukit Raja, Klang council side (downstream)                    | `label_area_B`                                |
| **SPOT 1** | Jalan Makyong (Sinar Harian)                                          | `spot_jalan_makyong`, `label_spot_1`        |
| **SPOT 2** | Jalan Sumazau (Sinar Harian): **a retention-pond request, not a flood report** (corrected 21 Oct 2026) | `spot_jalan_sumazau`, `label_spot_2`        |
| **SPOT 3** | Persiaran Batu Belah (drain request, not a flood report; same Sinar Harian article, 25 May 2024) | `spot_persiaran_batu_belah`, `label_spot_3` |

Why: the town fabric is simulated, so real names on invented buildings would mislead; the flood issue is a live public
dispute, so neutral labels fit the house rule; "upstream Area A / downstream Area B" also reads as a reusable pattern.
**Keep the real names in the pitch:** one line in the deck and video — *"Area A and Area B are a simulated pair based on
Setia Alam (Shah Alam) and Bandar Bukit Raja (Klang)"* — and the evidence slides keep real names and sources, because
the link to SDP's own township carries strategic fit and evidence marks. Object names still contain real street names
(internal); rename them before exporting the `.glb` if the website must not show them **[decide at step 8]**.

Tags are pure white, unshaded (emission), with a navy inverted-hull outline (`label_outlines()` in `look_ghibli.py`),
so they read on grass, roads and water and stay clear of the band colours. Water bodies of which only a sliver lies
in the model (< 1,500 m² or < 20 m deep inside) are skipped, and pond outlines are kept 1 m inside the edge: a pond
cutter touching the open ground edge made the boolean drop 25 m "flaps" off the south edge (fixed 20 Oct).

Trees reduced on 20 Oct to 5,007 (street trees every 24 m, sparser park and lawn clusters, pond ring every 21 m).

**Known quirks:**

- Windows sometimes locks `township.blend` during a save ("Cannot change old file (file saved with @)"). Nothing is
  lost while Blender stays open; save again.
- Long MCP calls return "No data received" but complete in Blender; check state with a short follow-up call.
- `python -I` hides the user-installed shapely; run `plan_town.py` with plain `python`.

---

## 1. Summary

| Part                          | Where it lives                                                             | What it does                                                                                                                                                                                                             |
| ----------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **3D township**         | Blender 5.2, driven by Claude through the Blender MCP                      | A simulated township loosely based on BBR, Ghibli-inspired look: mapped flood features (AR1 / OSM) and the architecture student's buildings, inside an invented, labelled clean town layout. **Built 20 Oct 2026** |
| **Screening simulator** | One small Python module (later ported to the website)                      | MSMA 2 Rational Method plus a volume balance → storage required, storage gap, risk band per zone                                                                                                                        |
| **The link**            | Object names and custom properties in the `.blend`, exported to `.glb` | The data contract: the simulator's outputs drive what the model shows                                                                                                                                                    |

The water in the model is a **gauge, not a movie**. The calculation decides each zone's band and each pond's fill
percentage; the model only displays them.

## 2. Decisions and why

| # | Decision                                                                                                                                  | Why                                                                                                                                                                                                                                                                                                                                  |
| - | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1 | **Model in Blender, through the MCP**                                                                                               | Better styling than the AR1 web viewer (which the team leader does not want as the look). Meets the "Blender or SketchUp only" rule for the architecture track, and the architecture student can open and edit the same file                                                                                                         |
| 2 | **No Blender fluid simulation as the physics**                                                                                      | It outputs water depths, which our rule bans; our three DEMs disagree by 3–6 m, so any depth would look exact and be false. It takes hours to bake, cannot run interactively on a website, and is not the MSMA 2 method in the concept                                                                                              |
| 3 | **Screening calculation in plain Python, results drive the scene**                                                                  | Same method as the concept; defensible; instant to recompute; easy to port to the website                                                                                                                                                                                                                                            |
| 4 | **Blender first, website later**                                                                                                    | Blender tests whether the visual language reads in five seconds, and renders the fly-through footage for the 5-minute video. The interactive web version can follow for the 11 Nov refined submission if shortlisted                                                                                                                 |
| 5 | **Base = the architecture student's sketch; AR1 adds the hydrology features and the context outside it** (team leader, 20 Oct 2026) | The sketch is richer (about 1,000 buildings, 2,400 trees, parks, road surfaces). AR1 carries the sourced features the story needs: ponds, main ditch, drains, council line, flood streets. See section 4.4                                                                                                                           |
| 6 | **Look: Ghibli-inspired painted style** (team leader, 20 Oct 2026; replaces the ink look the same day, which felt vague)            | Must work live in the viewport, in deck stills and in video, so it is real-time EEVEE with no Freestyle. Palette kept soft and off the risk-band hues (section 4.6). Built by `look_ghibli.py`. The ink look (`look_ink.py`) and the stylised-colour look (`LOOK = "stylised"` in `style_scene.py`) are kept as alternatives |
| 7 | **Extend west and north with generic fill** (team leader asked for the sketch to be extended, 20 Oct 2026)                          | The sketch misses Jalan Makyong, the main ditch and the council corner. Filled in the sketch's manner, labelled as invented (section 4.5) until the architecture student extends the sketch                                                                                                                                          |

## 3. Setup (done 20 Oct 2026)

| Item                 | State                                                                                                                                                                                                                 |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Blender              | **5.2**, installed through Steam. User config at `%APPDATA%\Blender Foundation\Blender\5.2\`                                                                                                                  |
| MCP server           | [mcp-for-blender](https://github.com/ahujasid/mcp-for-blender), registered **project-scoped** in [../.mcp.json](../.mcp.json) as `blender`, run by `uvx mcp-for-blender`, with `DISABLE_TELEMETRY=true`     |
| Add-on               | Copied to `%APPDATA%\Blender Foundation\Blender\5.2\scripts\addons\blender_mcp.py`. User has enabled it and connected                                                                                               |
| Claude Code approval | `claude mcp list` showed the server as **pending approval** on 20 Oct. Approve it when the new session asks                                                                                                   |
| Safe mode            | **Off**, deliberately: safe mode blocks file access, and we need to import OBJ/GeoJSON and export `.glb`. The add-on's socket on `localhost:9876` has no authentication, so stop the server when not in use |
| Known bug            | `uvx mcp-for-blender install-addon` crashes on Windows when printing its message (cp1252 console). Prefix with `PYTHONIOENCODING=utf-8` if it ever needs re-running                                               |

**Connecting in a new session:** in Blender press `N` → *MCP for Blender* tab → *Start MCP Server* →
*Connect to Claude*; then call `get_scene_info` to confirm the link. Save before running any code. (See "Start here"
at the top for the current state.)

**Step 1 done (20 Oct 2026):** link confirmed (Blender 5.2.2 LTS, add-on 1.8 up to date, telemetry off; Poly Haven
on, Sketchfab and Poly Pizza off, no 3D generators). Clean scene saved as
`simulations/township-3d/township.blend` (metric, empty). Folders `exports/`, `renders/` and `reference/` created.

**Architecture sketch found in the session.** The open Blender held the architecture student's rough 3D sketch of BBR,
unsaved. It is kept, unchanged, as `simulations/township-3d/reference/architecture_sketch_BBR.blend` (14,829 objects:
about 1,000 buildings, 1,600+ trees, road / vegetation / waterway hatches; materials prefixed `TPX_`). It is **not on
the AR1 grid**: about 1,966 × 1,122 m with its origin at a corner, against AR1's 2,450 × 1,220 m centred on
3.0900 N, 101.4360 E. Resolved the same day: the sketch is the base (decision 5, section 4.4). Its data source and how
it was made still need recording **[TBD — ask the architecture student]**.

MCP tools available: `execute_blender_code` (runs Python in the live session; save first), `look` (view or render),
`get_scene_info`, `search_assets` / `import_asset` (Poly Haven, Sketchfab, Poly Pizza), `generate_3d`,
`get_addon_status`, `disable_telemetry`, `record_trajectory_feedback`.

**Asset licences:** anything pulled through `search_assets` or `generate_3d` needs its licence recorded before it goes in
the video or the submission. Poly Haven is CC0; Sketchfab varies per model **[verify each]**.

## 4. The 3D township

### 4.1 Base data (already exists)

All in [../research/AR1_site_model/](../research/AR1_site_model/). Metres, **X east, Y north, Z up**, origin at the centre
of the extent, **3.0900 N, 101.4360 E**. Extent 3.0845–3.0955 N, 101.4250–101.4470 E (1220 × 2450 m).

| File                                        | Use                                  | Watch out                                                                                                                                  |
| ------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `terrain.obj`                             | Ground, smoothed SRTM                | Absolute heights unusable; keep only the direction of fall. Vertical exaggeration on terrain only, never on buildings                      |
| `buildings.obj`                           | 633 footprints, grouped by type      | **Heights are assumed.** Only 40–60% of standing buildings; west and north-west estates missing                                     |
| `water.obj`                               | 4 water bodies                       | Pond A and B are real (imagery-checked). The 216 m² basin is **not a pond**; drop it. Tasik Setia Alam is mostly outside the extent |
| `roads.obj`                               | 487 centrelines                      | No widths; assign by road class                                                                                                            |
| `drains.obj`                              | 65 drains and ditches, 15,068 m      | Position only. Main ditch (OSM way 888406336) is a concrete trapezoid, top width about 8–10 m                                             |
| `council_line.obj`                        | Klang / Shah Alam line               | OSM, not cadastral                                                                                                                         |
| `rainready_site.geojson` and `gis/`     | Same layers in WGS84 with attributes | Use for names, types and IDs                                                                                                               |
| `contours_1m.dxf`, `plan_map_clean.png` | Reference                            | `plan_map_imagery.jpg` is on Esri tiles — **not cleared for reuse**                                                               |

### 4.2 What to build on top

- **Buildings:** style the 633 mapped footprints; fill the unmapped estates with generic terrace housing in a separate
  collection named `generic_*`, so it can be shown or labelled as invented.
- **Roads:** give width by class, kerbs, simple markings.
- **Retention ponds A and B:** banks, a water surface object that can move up and down (the fill gauge). No depth is
  read from the model; capacity comes from the simulator inputs.
- **Main ditch and drains:** the main ditch as a lined trapezoid channel; smaller drains as narrow channels. Each drain
  carries a path for flow arrows.
- **Council line:** a visible but neutral marker (for example a thin light wall or ground line), labelled with both
  council names. Neutral styling — no "us and them" colours.
- **Zones:** 5–10 drainage zones as separate ground overlays that can be coloured by band. **Not yet drawn** — Claude
  can draft them from roads and drains; the team leader checks them.
- **Documented flood spots:** pins on Jalan Makyong, Jalan Sumazau and Persiaran Batu Belah, each with its source.
- **Upstream (Setia Alam side):** simplified massing beyond the council line, enough to show where water comes from.
- **Scenario toggle:** a second version of the upstream area with more paved land, for the "upstream change" scenario.

### 4.3 Style — first look: stylised city (superseded by the plain ink look, 4.5)

The team leader chose a stylised city look from a reference image: warm-tinted facades with window grids, flat roofs
with parapets and rooftop units, red tiled pitched roofs, soft daylight. It was first built on the AR1 buildings; the
base has since changed to the architecture sketch (section 4.4), so the style now applies only to the AR1 context
buildings outside the sketch. Applying it to the sketch is open (decision 6).

Built by [`simulations/township-3d/style_scene.py`](../simulations/township-3d/style_scene.py) (re-runnable; it
re-imports the AR1 buildings each time). First renders: `simulations/township-3d/renders/style_v1_*.png`.

| Element               | How                                                                                                                                      | Status                                                  |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Walls                 | Procedural window grid (3.0 m bays, 3.3 m floors), tint random per building; shops and commercial get a glazed ground floor              | Look only                                               |
| Houses (417)          | Gable roof, 25° pitch, ridge along the lot's short side so a terrace row reads as one roof                                              | Pitch and form **assumed**                        |
| Other buildings (216) | Flat roof, 0.9 m parapet, rooftop boxes scattered by geometry nodes                                                                      | Look only                                               |
| Heights               | AR1's assumed heights by type, unchanged. The reference image's towers are **not** copied: BBR in the extent is low-rise           | **Assumed** (AR1)                                 |
| Roads                 | Ribbons draped on the terrain, width by OSM class, dashed centre and edge lines; pavements on trunk, tertiary, residential, unclassified | Widths **assumed** (`ROAD_WIDTH` in the script) |
| Water                 | Ponds A and B and the Tasik Setia Alam edge; the 216 m² basin dropped                                                                   | —                                                      |
| Light                 | Sun plus Preetham sky, AgX, exposure −0.4. No world volume (it blacks out EEVEE)                                                        | —                                                      |

Still to do for the look: trees and greenery from the aligned sketch, drains as channels, the council line marker,
zone overlays. Check that green / amber / red zone bands stay readable against the warm facades and red roofs; if
not, mute the facades in the scenario shots.

### 4.4 Hybrid base: sketch plus AR1 features (built 20 Oct 2026)

Built by [`simulations/township-3d/build_features.py`](../simulations/township-3d/build_features.py), run after
`style_scene.py`. Render: `simulations/township-3d/renders/hybrid_v1_overview.png`.

**Alignment.** The sketch is a copy (collection `SKETCH`) of the reference file, shifted by **(−288.13, −794.99) m**
into the AR1 frame. Fitted on 426 matched building centroids: median residual 0.66 m, rotation 0.1°, scale 0.9998.
So the sketch is almost certainly built on the same OSM footprints as AR1 **[confirm with the student]**. Its heights
match Copernicus GLO-30 (sketch roads a median 0.6 m above it), not SRTM (4 m below).

**Coverage gap — important.** The sketch covers only the south-east of the AR1 extent and runs further east:
about x −290 to +1,670 m, y −800 to +295 m. **Outside it: Jalan Makyong (the most-cited flood street), the main ditch,
the council corner and the drain crossing at the corner, and all of the Setia Alam side.** These areas use AR1
buildings and roads (211 AR1 buildings shown where no sketch building is within 40 m).

| Layer        | Object(s)                                                                              | Built from                                                                                  | What is assumed                                                                                                                       |
| ------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Ground       | `terrain_cop30` (lowered 1.0 m), `ground_sketch_fill` beyond the AR1 edge          | GLO-30; fill shaped from sketch road heights                                                | Absolute heights unusable (AR1)                                                                                                       |
| Ponds A, B   | `pond_A`, `pond_B`, `*_water`; also `water_tasik_setia_alam_edge`              | OSM outlines (AR1), cut into the ground                                                     | Basin depth 2.5 m is **visual only**. Capacity `TBD`                                                                          |
| Fill gauge   | `fill_pct` on `pond_*_water` (0–1) drives the water height by a driver            | —                                                                                          | Currently **0.5, placeholder**                                                                                                  |
| Main ditch   | `drain_888406336`                                                                    | OSM way 888406336                                                                           | Width 9 m from imagery (AR1). Drawn on the ground as a concrete and water band, not cut in                                            |
| Other drains | `drain_D01`… (59)                                                                   | OSM (AR1)                                                                                   | Widths assumed (ditch 3 m, drain 1.5 m); OSM ids not carried in AR1 → `TBD`                                                        |
| Council line | `council_line`, `council_line_band`, `label_Klang`, `label_Shah_Alam`          | OSM way 1231162275                                                                          | Not cadastral                                                                                                                         |
| Flood pins   | `spot_jalan_makyong`, `spot_jalan_sumazau`, `spot_persiaran_batu_belah`          | All three: Sinar Harian, 25 May 2024 (settled 21 Oct 2026). Only Makyong is reported as flooding; Sumazau is a retention-pond request | Pin = a point on the mapped street, **not** a measured flood location. Batu Belah is a drain request, not a reported flood spot |
| Hidden       | sketch base slab `Geom3D`, sketch water hatches, AR1 SRTM `terrain`, raw AR1 lines | —                                                                                          | Kept in the file, not rendered                                                                                                        |

Lessons: cutting thin drains into a 30 m ground grid leaves triangle artefacts, so only the ponds are cut. Map lines
with few vertices sink into the ground, so all lines are resampled every 8 m before draping.

### 4.5 Plain ink look, grounding and extension (20 Oct 2026)

**Run order** (each script is re-runnable; run all three after any change):
`style_scene.py` → `build_features.py` → `build_town.py` (section 4.6b) → `look_ghibli.py` (current look; section 4.6) or `look_ink.py`. Renders: `renders/ink_v1_close.png`, `renders/ink_v1_overview.png`
(about 17 s each at 1920 × 1080 with outlines).

| Fix or addition                         | What was done                                                                                                                                                                                                                                                                                                                                                       |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Black stripes in the viewport** | They were the sketch's 8,616 import empties (one per building and tree), drawn as small crosses. Every sketch mesh now holds its own world position and the empties are deleted. They never showed in renders                                                                                                                                                       |
| **Floating buildings**            | AR1 buildings sat on SRTM heights (about 4–5 m above the GLO-30 ground now shown); sketch buildings up to about 3.5 m above it. `snap_to_ground` rests every sketch building, tree and AR1 building on the lowest ground point under it, and drapes the sketch's road and park surfaces onto the ground                                                          |
| **Ground beyond the AR1 edge**    | `ground_sketch_fill` continues the GLO-30 edge outward (stable on re-runs)                                                                                                                                                                                                                                                                                        |
| **Extension (west and north)**    | `generic_extension` collection: **2,805 generic terrace lots** (6.4 × 13.8 × 6.5 m) along residential streets where OSM maps no buildings, and **2,992 street trees** every ~14 m along roads, copied from the sketch's tree. Both carry `invented: true`. Mapped AR1 buildings and roads are kept as they are                                    |
| **Ink look**                      | Every material swapped to `ink__<original>` (original kept in the object's `orig_mats`). Tone from the lit brightness, halftone dots in screen space, walls never below 45 % tone, cast shadows go black. Outlines by Freestyle (**render only**, not in the viewport), none on the ground. Sun from the east-north-east; white background for the camera |

**Honesty notes for the deck and video.** The generic terraces show that houses stand in the west and north-west
(AR1 imagery check), not where each house is; say so in the appendix or label one shot. The street trees are placed by
rule. Both disappear once the architecture student extends the sketch.

**File-save note.** One save on 20 Oct failed with "Cannot change old file (file saved with @)": Windows briefly locked
`township.blend` (likely an antivirus scan), leaving only `.blend1` and `.blend@`. Saving again worked. If it recurs,
nothing is lost while Blender stays open: just save again.

### 4.6 Ghibli-inspired look (current, 20 Oct 2026)

Why it changed: the ink look read as vague (white on white; outlines only in final renders). The team leader wants
judges to be drawn in and to tell buildings, roads, water, trees and our features apart at a glance, in deck stills,
the video and live demos alike. A five-style spike (clay, map colours, pastel diorama, night digital twin, flat
diagram; `renders/style_options/`) came first; the team leader then chose a Ghibli-inspired look.

| Element      | How (all real-time in EEVEE)                                                                                                                                                                                                                                                                                                                                      |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Shading      | Soft two-tone cel step on the lit amount; shadows tinted cool blue-violet, never black; faint highlight in full sun                                                                                                                                                                                                                                               |
| Painted feel | Slow world-space brightness noise (±6 %) like brush strokes                                                                                                                                                                                                                                                                                                      |
| Sky          | Gradient (pale horizon to deep blue) with procedural cumulus clouds, seen only by the camera; the scene is lit by a soft even sky so shadows stay readable                                                                                                                                                                                                        |
| Haze         | Fades toward the horizon colour from 1.5 km, max 30 %                                                                                                                                                                                                                                                                                                             |
| Outlines     | Warm dark-brown inverted hull (Solidify, 0.6 m, back-face culled) on buildings only. Works in the viewport and survives a glTF export as geometry                                                                                                                                                                                                                 |
| Sun          | Warm, from the south-east, soft shadows                                                                                                                                                                                                                                                                                                                           |
| Roads        | Darker asphalt; cream `road_markings` along OSM centrelines (dashed centre on residential and main roads, solid edges on main roads, lane dashes and edges on the trunk road and expressway, edges on ramps), drawn only over road surfaces; light `road_kerbs` along the sketch's road edges. Stylised, not surveyed (`MARKINGS` in `build_features.py`) |

Renders: `renders/ghibli_v1_hero.png` (low angle with sky), `ghibli_v1_top.png`, `ghibli_v1_overview.png`; about 4–9 s
each at 1920 × 1080, so a fly-through is practical.

**Palette rule (so the flood-risk bands stay readable later).** The scene stays soft and fairly low in saturation, and
keeps off the band hues: cream walls with **grey** roofs (no red or orange, and no blue, so water is the only blue);
sage-teal trees; a muted sage ground; indigo (not red) flood pins; white council line. Colours live in `PAL` at the top of
`look_ghibli.py`.

**Recommendation for the bands [for the hydrology and frontend tracks to confirm].** Draw them as strong, saturated
fills with a dark edge, so they separate from the soft scene. Because the ground and trees are green-leaning, a pale or
muted "low" green will blend in. Either use a strong emerald for low, or leave low-risk zones uncoloured and colour only
medium (amber) and high (red). Water should stay blue in every scenario.

### 4.6a Model check against OSM, and fixes (20 Oct 2026)

The team leader saw roads cut halfway, isolated buildings, a broken ditch and objects hanging off the edge. Each was
measured against OSM (AR1 `roads.geojson`, `drains.geojson`) and a fresh Overpass download, then fixed:

| Symptom                                              | Cause found                                                                                                                                                                                                                                       | Fix                                                                                                                                                                                                                                     | After                                                       |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Roads cut halfway                                    | AR1 road strips were trimmed per OSM segment (some hundreds of metres long), so one crossing deleted a whole stretch; parks and water also counted as "sketch road"                                                                               | Strips split into ~6 m pieces; trim only under sketch road surfaces                                                                                                                                                                     | Uncovered road samples 158 → 13 of 14,545                  |
| Toll plaza alone in a field                          | **AR1's OSM query left out `highway=construction` and `*_link`.** The West Coast Expressway (Lebuhraya Pesisiran Pantai Barat) is still tagged *construction* in OSM, though imagery (Dec 2025–Sep 2026) shows it built with traffic | 38 missing ways (8 expressway carriageways, 30 ramps) added from Overpass as [`research/AR1_site_model/gis/roads_supplement.geojson`](../research/AR1_site_model/gis/roads_supplement.geojson) (ODbL, source and date in its `note`) | Expressway continuous from the west edge to the interchange |
| Ditch discontinuous                                  | 10 gaps of 6–29 m between OSM drain pieces, mostly at road crossings (culverts OSM does not map)                                                                                                                                                 | `drain_culverts_inferred` bridges gaps ≤ 30 m, **labelled inferred**                                                                                                                                                           | All 10 bridged                                              |
| Objects cut at the edge                              | The model simply stopped at the extent                                                                                                                                                                                                            | Earth-coloured plinth (`plinth`) around the shown ground; generic trees and terraces kept 4 m inside                                                                                                                                  | Edge reads as a deliberate base                             |
| Pond and buildings floating at the north-east corner | The full Tasik Setia Alam outline was built though only part lies in the extent; 14 AR1 buildings straddle the north edge (centroids at y ≈ 613 > 608); street-tree crowns overhung the edge                                                     | Pond outlines clipped to the extent; AR1 buildings that cross the edge hidden; generic trees kept 8 m inside; council labels laid flat (they read mirrored from the north when upright)                                                 | Ground check: no building or pond off the ground            |
| Isolated buildings                                   | 13 buildings with no neighbour within 60 m: 10 from the sketch (east edge), 3 mapped in OSM                                                                                                                                                       | **Kept**: they are real; their neighbours are missing from OSM                                                                                                                                                                    | —                                                          |

Remaining dead-end roads (26) are service roads and cul-de-sacs, as in reality. A correction saying the AR1 road layer lacks
construction and link roads has been added to [AR1_site_model.md](../research/AR1_site_model.md).

### 4.6b Clean simulated town (20 Oct 2026)

**Decision (team leader):** the model is a *simulated* township loosely based on BBR, so it should read as a clean,
coherent town rather than a patchwork of uneven sources. The flood features stay as built from AR1 / OSM.

**Run order now:** `style_scene.py` → `build_features.py` → `build_town.py` → `look_ghibli.py`.
`build_town.py` exports the kept buildings and the sketch's parks to `data/kept_features.json`, runs
[`plan_town.py`](../simulations/township-3d/plan_town.py) (system Python + shapely, about 3–5 min) when needed, and
builds the result into the `TOWN` collection. Check map: `simulations/township-3d/data/town_plan.png`.

| Layer                      | How                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Source                                                                                                                                                                                             |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Roads                      | One network from OSM centrelines over the whole model area, buffered by class width and merged, so junctions are rounded and widths uniform; service ways under 120 m (driveways, car-park aisles) dropped                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | [`research/AR1_site_model/gis/roads_full_osm.geojson`](../research/AR1_site_model/gis/roads_full_osm.geojson): 869 ways, Overpass 20 Oct 2026, ODbL (AR1's own road file stopped at the AR1 edge) |
| Pavements, kerbs, markings | Pavements by class (none on the expressway, ramps or service roads), stopping at drains; kerbs along every road edge; markings clipped to the road surface                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Invented, by rule                                                                                                                                                                                  |
| Blocks                     | Land between the streets: 267 blocks                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Derived                                                                                                                                                                                            |
| New buildings              | **Matched to the real amount** (team leader, 20 Oct 2026). Footprint budget inside the AR1 extent: **120,000 m²**, so kept (~205,000 m²) + new ≈ **325,000 m²**, inside the estimated real 235,000–353,000 m² (OSM's 141,000 m² ÷ AR1's 40–60 % mapped share). Placed in priority order: land OSM tags residential, commercial or retail ([`landuse_osm.geojson`](../research/AR1_site_model/gis/landuse_osm.geojson), Overpass 20 Oct 2026), then the west and north-west estates (x < −300 m) where AR1's imagery check found whole estates unmapped. Result: 172 rows of terraces (2 storeys, 6.5 × 14 m lots, back lanes) and shophouses (3 storeys, within 35 m of main roads); kept clear of real buildings, ponds, drains, the sketch's parks and the edge | **Invented** (`invented: true` on every object); the budget is an estimate, not a count                                                                                                    |
| Open land                  | Everything not built becomes defined open land: OSM parks and recreation grounds and any piece over 4 ha become parks (tree clusters, loop path); construction and brownfield become open fields with a few edge trees; the rest become lawns with sparse tree clusters. 19 parks, 159 lawns and fields                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | **Invented** layout; vacant land is vacant in reality too                                                                                                                                    |
| Trees                      | 5,007 (was 5,904): street trees every 24 m on pavements (60–70 % size), park clusters, a ring around each pond                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | **Invented**                                                                                                                                                                                 |
| Kept unchanged             | The sketch's and AR1's buildings, ponds, main ditch, drains, culverts, council line and labels, flood pins, plinth                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | AR1 / OSM / sketch                                                                                                                                                                                 |
| Hidden (kept in the file)  | The sketch's road patches and 2,400 scattered trees, AR1 road strips, the first generic fill (`generic_extension`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | —                                                                                                                                                                                                 |

**Junctions (20 Oct 2026):** wherever two roads' surfaces overlap (junctions, merges, slip roads) no markings are
drawn, plus 4 m, so lines stop cleanly instead of crossing. Ways that OSM merely split end to end (same direction
within 35°) are not treated as junctions.

**Council boundary (20 Oct 2026):** shown as a translucent white light curtain (14 m, fading upward, material
`boundary_curtain`, exempt from the toon look) along OSM way 1231162275, a dashed white ground band drawn above roads,
and flat labels **KLANG · Bandar Bukit Raja** and **SHAH ALAM · Setia Alam** (township names confirmed 21 Oct 2026).
Neutral: neither side is tinted. A clipping bug that dropped the east–west stretch (the way starts 3.6 km outside the
model) was fixed by densifying lines before clipping; the same fix applies to drains crossing the edge.

**Elevation between the two sides (checked 20 Oct 2026):** the model shows **no** visible step, and the data cannot
support one. Ground medians inside the extent: GLO-30 5.8 m (Shah Alam side) vs 5.3 m (Klang side); SRTM 9.1 m vs
10.3 m. The 0.5–1.5 m differences are below the 3–6 m disagreement between the DEMs, and the two DEMs disagree on
which side is higher. Only ~8 ha of the Shah Alam side lies in the extent. The upstream relation is a drainage one
(the main ditch carries water from the Setia Alam side into BBR), best shown with flow arrows (step 6), not with
exaggerated terrain.

**Honesty note for the deck and video:** say once that the town fabric is a simulated layout loosely based on BBR, and
that the ponds, drains, ditch, council line and flood streets are mapped features. Do not present the generated
buildings as BBR's actual buildings.

### 4.7 Naming and custom properties (the data contract)

Every object the simulator touches gets a fixed name and custom properties. Blender exports custom properties into the
`.glb` as glTF `extras`, so the website can read them without rebuilding the model.

| Object             | Name pattern           | Custom properties                                                                                                        |
| ------------------ | ---------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Zone               | `zone_Z01` …        | `area_ha`, `c_now`, `c_upstream`, `drains_to`, `council`, `source`                                           |
| Pond               | `pond_A`, `pond_B` | `osm_id`, `stated_capacity_m3` (or `TBD`), `capacity_source`, `owner`, `owner_conf`                          |
| Pond water surface | `pond_A_water`       | driven: `fill_pct`                                                                                                     |
| Drain              | `drain_<osm_id>`     | `type`, `width_m` if known, `owner` (assumed by the Selangor 2025 rule: drains to rivers JPS, to monsoon drains the council; see research/TBD_VERIFY_RESOLUTION.md item 16), `owner_conf` |
| Council line       | `council_line`       | `osm_way` 1231162275, `source`                                                                                       |
| Flood spot         | `spot_<street>`      | `source`, `date`                                                                                                     |
| Generic fill       | `generic_*`          | `invented: true`                                                                                                       |

Owners default to `[TBD]` with confidence L unless a source says otherwise.

### 4.8 Draft drainage zones (step 4, 20 Oct 2026, **draft**)

Drawn by [`plan_zones.py`](../simulations/township-3d/plan_zones.py) (system Python + shapely; writes
`data/zones.json`, the check map `data/zones_check.png` and `data/scenario_features.json`), built in Blender by
[`build_zones.py`](../simulations/township-3d/build_zones.py) (collection `ZONES`). **Check map:**
[`simulations/township-3d/data/zones_check.png`](../simulations/township-3d/data/zones_check.png). Renders:
`renders/zones_v1_overview.png`, `zones_v1_check.png`, `zones_v1_hero.png`.

**How they were drawn.** The model rectangle (420.18 ha) is cut along **mapped lines only**, then each cell is
grouped by the drain or pond it reaches. The nine zones cover the rectangle with no gaps or overlaps:

| Cut line                                                                                                            | Source                                   |
| ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| Council line                                                                                                        | OSM way 1231162275                       |
| Trunk drain: the east–west drain at y ≈ 300, from the council corner west to the main ditch                       | AR1 `drains.geojson` (chain of 9 ways) |
| Persiaran Batu Belah (dual carriageway averaged to one centreline)                                                  | `roads_full_osm.geojson`               |
| Persiaran Sungai Keramat, continued east by Persiaran Astana / KU 2                                                 | same                                     |
| Jalan Meru, south of the trunk drain (dual carriageway averaged)                                                    | same                                     |
| Centre split: unnamed residential way 739555185 (x ≈ 301), extended straight to the trunk drain and Sungai Keramat | same                                     |

| Zone | Name                          | Area (ha) | Water (ha) | Drains to     | Council   | Route (OSM way directions; all **[verify]**)                                                                                                                                                  | Conf. |
| ---- | ----------------------------- | --------- | ---------- | ------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| Z01  | Upstream, Shah Alam side      | 23.14     | 1.99       | trunk drain   | Shah Alam | Tasik Setia Alam and the drains south of it, then the **one mapped drain that crosses the council line** (3.09294 N, 101.44433 E; `drain_D32`), then the council corner and the trunk drain | M     |
| Z02  | North strip                   | 66.16     | 0          | trunk drain   | Klang     | Ditch along Jalan Sungai Puloh and the trunk drain run west to the main ditch, which crosses the north-west corner                                                                                  | M     |
| Z03  | West, north of Sungai Keramat | 63.68     | 0          | pond A        | Klang     | Ditch at y ≈ 74 runs east into pond A's west side. South part: the Sungai Keramat drain runs east to pond A's south tip. Holds **Spot 1**                                                    | M     |
| Z04  | Pond A, centre                | 35.25     | 5.56       | pond A        | Klang     | Land around pond A. Pond A's outlet runs north to the trunk drain. Holds **Spot 3**                                                                                                           | M     |
| Z05  | Centre-east (Sumazau estate)  | 36.81     | 0          | trunk drain   | Klang     | **No internal drain mapped.** Assumed: north / east to the trunk drain via the drain along Jalan Meru. Could instead go south to pond B **[TBD]**. Holds **Spot 2**               | L     |
| Z06  | South-west                    | 40.12     | 0.01       | pond A        | Klang     | **No internal drain mapped.** Assumed: north to the Sungai Keramat drain on its edge, then to pond A **[verify]**                                                                       | L     |
| Z07  | South-centre (pond B)         | 77.24     | 5.86       | pond B        | Klang     | Drains along Sungai Keramat (running west) and north along x ≈ 323 and x ≈ 825, to the junction between the ponds and into pond B                                                                 | M     |
| Z08  | East, Klang side              | 38.21     | 4.92       | trunk drain   | Klang     | Retention pond OSM 721223351 (4.9 ha) and the drain running north-west from it; the drain along Jalan Meru. Both reach the council corner                                                           | M     |
| Z09  | South-east                    | 39.57     | 0          | **TBD** | Klang     | Drains along Persiaran Astana run east, out of the model. Outlet unknown                                                                                                                            | L     |

**Assumptions and doubts:**

1. **Terrain is not used for the edges.** AR1 (11 Oct 2026) showed that D8 routing on GLO-30 fails here: the DSM
   climbs 13 m along the main ditch (embankments), and drains have a median 0.32 m of relief. The fall of the ground
   enters only as the **regional direction**: rises east and north-east, falls south-west (M at catchment scale, L
   inside the block). This agrees with the mapped drains running west to the main ditch.
2. **OSM way direction is read as flow direction.** It usually is, but not always. The check map draws it as arrows.
3. **Council corner:** a short chain of OSM drains there runs **north**, out of the model (x ≈ 800), so part of the
   flow may leave that way rather than west.
4. **Ponds A and B are joined** by a short link at about (−100, −300). They may work as one system. The simulator
   currently treats them as two ponds with separate outlets.
5. **Z01 is only the in-model part of Area A.** The rest of the upstream area enters as `EXT_A` in `inputs.json`, a
   placeholder area (AR1 has no usable upstream boundary).
6. **Areas are plan areas, water included.** Areas are fine to measure; depths are not.
7. **Rational Method size limit:** the largest zone is 77.2 ha (Z07). If MSMA 2's limit is 80 ha, all zones are
   within it (limit confirmed: MSMA 2 2.3.1.2). This was a reason to split the centre and the east into separate zones.
8. **The 4.9 ha pond OSM 721223351** (Z08) is not in the pond contract. Open: add it as `pond_C`?

**In Blender.** `zone_Z01`…`zone_Z09`: draped overlays cut into 10 m tiles so they follow the ground, **0.68 m up**
(above roads 0.48, pavements 0.56 and markings 0.60; below the council band 0.75). Water bodies are cut out, so ponds
stay blue. No shadows. `zone_Zxx_edge`: a dark 3 m edge line at 0.70 m. `label_zone_Zxx`: a flat white tag 16 m up,
in the same style as the spot tags. Colour **neutral** (warm white at 18 % opacity) until the simulator sets the bands.
Each zone has its own material `zone_Zxx`, with nodes `zone_color` (emission) and `zone_alpha` (mix).
`look_ghibli.py` now skips materials named `zone_*` and `rr_*`.

**Properties on each zone** (data contract 4.7, plus extras): `area_ha`, `c_now`, `c_upstream` (written by
`drive_scene.py` from `inputs.json`, with `c_status`), `drains_to`, `council`, `source`, plus `zone_name`, `route`,
`water_area_ha`, `holds_water`, `drain_objects` (every `drain_*` with a path point in the zone; a drain on an edge is
listed in both zones), `status` = "DRAFT - not an official catchment", `band` and `band_<scenario>`.

## 5. The screening simulator

### 5.1 Method

Per zone, for a chosen design storm:

1. **Peak flow — Rational Method:** `Q = C · i · A / 360`, with Q in m³/s, C the runoff coefficient, i rainfall
   intensity in mm/hr, A area in hectares (MSMA 2 Eq. 2.3; not for catchments over 80 ha; sourced, see 5.8).
2. **Volume balance:** water in over the storm (from Q and duration) minus what the outlet drain can pass, compared
   with the pond's stated capacity. The exact hydrograph shape (simple triangle or MSMA 2 procedure) is the hydrology
   pair's call **[TBD]**.
3. **Storage gap** = storage required − stated capacity, computed twice: **with and without** the upstream change.
   Shown as a scenario difference ("with the upstream change, the gap grows from A to B"), never as an attribution.
4. **Risk band** per zone: low / medium / high from the ratio of storage required to capacity. Thresholds **[TBD]**,
   set by the team leader and written in the assumption ledger.

Outputs: storage required, storage gap (two scenarios), band per zone, fill percentage per pond. **No depths, no times
to recede, no compliance verdicts.**

### 5.2 Inputs — all open (superseded: every input below is now sourced or stated, see 5.8 and research/TBD_VERIFY_RESOLUTION.md)

| Input                                             | Status                                | Where it should come from                                                                                                                                                                                                |
| ------------------------------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Design rainfall intensity and duration            | **[TBD]**                       | MSMA 2 IDF data for Klang **[verify availability]**                                                                                                                                                                |
| Runoff coefficients now and after upstream change | **[TBD]**                       | MSMA 2 tables by land use                                                                                                                                                                                                |
| Zone areas                                        | **[TBD]** until zones are drawn | Measured from the model geometry (areas are fine to measure; depths are not)                                                                                                                                             |
| Pond A and B capacity                             | **[TBD]**                       | No public figure. Do **not** derive from model geometry (AR1 assumption 3). The booklet's 16,000 / 34,000 / 50,000 m³ belongs to the Wetland Townpark, which is **not located and lies outside the extent** |
| Outlet capacity                                   | **[TBD]**                       | Assumption, stated in the ledger                                                                                                                                                                                         |

Until real values arrive, the code runs on **placeholder values clearly flagged as placeholders**, and any render made
with them carries an on-screen "illustrative values" label.

### 5.3 How the result drives the scene

| Simulator output    | In Blender                                                                                                        |
| ------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Pond fill %         | `pond_*_water` moves between empty and bank-top level                                                           |
| Zone band           | Zone overlay material: green / amber / red, with a legend                                                         |
| Flow direction      | Animated arrows along drain paths, crossing the council line where the mapped drain does (3.09294 N, 101.44433 E) |
| Rain slider / storm | Rain particle density, keyframed                                                                                  |
| Upstream switch     | Swap upstream massing; recompute; bands and fill update                                                           |

Scenarios are baked as keyframes so one timeline gives the video sequence: clear day → rain starts → ponds fill →
upstream switch → a pond is added → gap shrinks.

### 5.4 Code location

`simulations/township-3d/` — **exists** (model side built 20 Oct 2026):

| File                                                                          | State                                        | What                                                                                                                                             |
| ----------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `style_scene.py`                                                            | built                                        | Imports and styles AR1 buildings (`LOOK = "plain"` / `"stylised"`), AR1 road strips, ground, water, sun                                      |
| `build_features.py`                                                         | built                                        | Hybrid base: ground, ponds (+ `fill_pct` driver), ditch and drains, inferred culverts, council boundary, pins, plinth, grounding of the sketch |
| `plan_town.py`                                                              | built                                        | 2D town plan with shapely → `data/town_plan.json`, check map `data/town_plan.png`                                                           |
| `build_town.py`                                                             | built                                        | Builds the town plan in Blender (`TOWN` collection), hides what it replaces                                                                    |
| `look_ghibli.py`                                                            | built, **current look**                | Toon materials, sky, outlines. `look_ink.py` is the alternative                                                                                |
| `plan_zones.py`                                                             | built (step 4)                               | Draft zones with shapely → `data/zones.json`, check map `data/zones_check.png`, scenario features `data/scenario_features.json` (4.8)     |
| `build_zones.py`                                                            | built (step 4)                               | Builds the zone overlays, edges and tags in Blender (`ZONES` collection), neutral colours                                                      |
| `data/`                                                                     | built                                        | `kept_features.json`, `town_plan.json`, `zones.json`, `scenario_features.json`, check maps                                               |
| `township.blend`, `renders/`, `reference/architecture_sketch_BBR.blend` | built                                        | Model, stills, untouched sketch copy                                                                                                             |
| `screening.py`                                                              | built (step 5), **placeholder inputs** | The calculation only, no Blender imports, standard library only. `--check` runs the self-checks (5.5)                                          |
| `inputs.json`                                                               | built (step 5), **36 placeholders**    | Every input with value, unit, status (sourced / assumed / measured / placeholder), source and what is still unknown                     |
| `outputs.json`                                                              | written by `screening.py`                  | Results for the three scenarios, with `illustrative: true` while any input is a placeholder                                                    |
| `drive_scene.py`                                                            | built (step 6)                               | Reads `outputs.json`; keyframes zone bands, `fill_pct`, flow arrows, rain, upstream change, what-if pond, captions (5.6)                     |
| `screening.ts` | built 21 Oct | TypeScript port for the website (mode B); no dependencies, no file access (5.7) |
| `check_parity.ts` | built 21 Oct | Python vs TypeScript on 216 input sets (incl. drain blockage and a held storm duration, added 21 Oct); must pass after any method change |
| `export_glb.py` | built 21 Oct | Writes the hand-off package in `exports/` (5.7) |
| `exports/` | built 21 Oct | `township.glb` (2.8 MB), `trees.json`, `inputs.json`, `outputs.json` |

Scripts run through `execute_blender_code`, and are saved to these files so the build is reproducible without the MCP.

### 5.5 As built: `screening.py` and `inputs.json` (step 5, 20 Oct 2026) — **superseded by v2 (5.8)**

*Kept as the record of the placeholder version. The method and the numbers below were replaced on 21 Oct 2026.*

**Status: runs end to end on placeholder inputs.** 36 inputs are placeholders: round numbers picked so the demo shows
every band and both directions of change. **They say nothing about BBR.** Each one names what to ask the hydrology
pair ([HY_INPUT_REQUEST.md](archive/HY_INPUT_REQUEST.md)).

How 5.1 was made concrete (every step is an assumption, open to replacement):

| Step         | As coded                                                                                                                                                                                                                                  |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Peak flow    | `Q = C·i·A/360` per zone and for `EXT_A` (Area A beyond the model edge)                                                                                                                                                             |
| Volume       | `V = k·Q·D`, with `k` = `hydrograph_volume_factor` (1.0 = rectangle)                                                                                                                                                              |
| Trunk drain  | Zones and `EXT_A` that drain straight to it use up part of its capacity. The **spare** is what ponds A and B can release, shared in proportion to their outlet sizes. **This is how the upstream change reaches the ponds** |
| Pond balance | storage required = inflow − release over the storm; gap = required − capacity (positive = shortfall); fill = required / capacity, capped at 100 %                                                                                       |
| Band         | Pond zones: required / capacity of their pond. Trunk zones: trunk demand / capacity. Outlet TBD: `unknown`. Thresholds 0.8 / 1.0 (placeholders)                                                                                         |
| What-if pond | Catches Z06 runoff, releases at its outlet rate, passes on only the overflow                                                                                                                                                              |

**Self-checks** (`python screening.py --check`): the Rational units (1 ha, C = 1, 360 mm/hr gives 1 m³/s); band edges;
volume balance closes for every pond and scenario; releases never exceed inflow; more paving upstream never shrinks a
pond's storage requirement. All pass (20 Oct).

**Illustrative result** (placeholder inputs; for the demo only, never for the deck as fact):

| Scenario                                               | Trunk drain demand / capacity | Pond A: required of 60,000 m³ (fill), gap | Pond B: required of 40,000 m³ (fill), gap |
| ------------------------------------------------------ | ----------------------------- | ------------------------------------------ | ------------------------------------------ |
| Now                                                    | 30.7 / 40 m³/s               | 54,878 (91 %), −5,122                     | 31,682 (79 %), −8,318                     |
| Upstream change                                        | 36.8 / 40                     | 68,814 (100 %), **+8,814**           | 38,650 (97 %), −1,350                     |
| Upstream change + what-if pond (25,000 m³, 74 % used) | 36.8 / 40                     | 50,348 (84 %), −9,652                     | 38,650 (97 %), −1,350                     |

Bands: now Z03, Z04 and Z06 are medium, the rest low (Z09 unknown). With the upstream change, the pond A zones turn
high and the rest medium. With the what-if pond, everything is medium. Wording on screen states scenario differences
("pond A goes from 5,100 m³ to spare to a shortfall of 8,800 m³"), never attributions.

### 5.6 As built: `drive_scene.py` (step 6, 20 Oct 2026)

Everything it adds is in collection `SIMULATOR`, named `rr_*` (plus `pond_whatif`). It is re-runnable: it clears its
own objects and keyframes first.

| Part                 | How                                                                                                                                                                                                                                                                                                                                                 |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Zone bands           | Keyframes on each `zone_Zxx` material (colour and opacity), from neutral to the band for each scenario. Low = strong emerald, medium = amber, high = red, outlet TBD = grey (the 4.6 recommendation). Per-scenario bands and ratios are also stored as properties (`band_now`, `band_upstream`, `band_upstream_plus_pond`) for the `.glb` |
| Pond fill            | `fill_pct` keyframed on `pond_A_water` / `pond_B_water`; their existing drivers move the water. The water height is a gauge of fill %, **not a depth**. `stated_capacity_m3` stays `TBD`; the placeholder used is stored apart as `capacity_used_m3` with its status                                                              |
| Flow arrows          | `rr_flow_arrows`: chevrons on ribbons 0.9 m above ground along every `drain_*` path, moving in the OSM way direction (animated shader, so it works in the viewport too). `rr_flow_arrows_cross`: brighter and wider on **`drain_D32`, the one mapped drain that crosses the council line**                                            |
| Rain                 | `rr_rain_emitter`: 220,000 particles (stylised 14 m streaks) over the model; opacity keyframed; the sun dims to 55 %                                                                                                                                                                                                                              |
| Upstream change      | `rr_upstream_change`: 54 **invented** low blocks on paved aprons on open land in Z01, rising by a shape key. Not a mapped or planned development                                                                                                                                                                                            |
| What-if pond         | `pond_whatif` / `_water`: an **invented** 2.9 ha pond inside the OSM brownfield (way 1267917541) in Z06, scaling in. It is a what-if for the demo, not a proposal                                                                                                                                                                         |
| Captions, legend     | Text in front of `cam_overview`: a caption per phase (numbers from `outputs.json`), a band legend, and an "ILLUSTRATIVE VALUES · placeholder inputs, not BBR data" tag                                                                                                                                                                         |
| Label on every frame | The **render stamp** burns "ILLUSTRATIVE VALUES - placeholder inputs, not BBR data" into every rendered frame from **any** camera while `outputs.json` says `illustrative: true`. The camera tag covers the viewport and live demos                                                                                                 |

**Sequence** (24 fps, frames 1–720 = 30 s, camera `cam_overview`):

| Frames   | Phase                                                                                      | Caption                                                                                      |
| -------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| 1–95    | Clear day, neutral zones, ponds at normal level                                            | "Clear day. Nine draft drainage zones; two retention ponds (A, B)."                          |
| 96–263  | Rain fades in (96–144), arrows (120–168), ponds fill (144–264), bands appear (216–264) | "Design storm. Water moves west along the drains; the ponds fill."                           |
| 264–311 | Hold on today's result                                                                     | "Today: pond A 91% full (5,100 m³ to spare), pond B 79% full."                              |
| 312–431 | Upstream blocks rise (312–360); bands and fill move to the upstream result (360–432)     | "Scenario: more paved land upstream in Area A. The shared trunk drain fills up."             |
| 432–479 | Hold                                                                                       | "With the upstream change, pond A goes from 5,100 m³ to spare to a shortfall of 8,800 m³." |
| 480–599 | What-if pond scales in (480–528); results update (528–600)                               | "What-if: a pond on vacant land upstream of pond A."                                         |
| 600–720 | Hold: gap shrinks                                                                          | "With the what-if pond, pond A's shortfall closes: 9,700 m³ to spare."                      |

Test renders: `renders/sim_v1_001_clear.png`, `sim_v1_300_now.png`, `sim_v1_450_upstream.png`,
`sim_v1_700_whatif_pond.png`, `sim_v1_council_corner.png` (`cam_check`, frame 400). About 7 s per frame at 50 %
resolution, with the rain. The particle system steps from frame −120, so render the sequence in order.

**Known limits:** the captions follow `cam_overview` only (re-parent them for another camera; the stamp works
anyway). The caption numbers are rebuilt from `outputs.json` on each run. The rain reads as stylised streaks, not
realistic rain. The sequence compares scenarios. It is **not** a time series: pond A's fill drops in the last phase
because the scenario changes, not because water drains away. Say so in the voice-over.

### 5.7 The website: both modes, one engine (21 Oct 2026, team leader)

**Decision:** the website gets **both** modes. **A, precomputed:** it loads `outputs.json` and switches between the three
scenarios. Feasible for the 23 Oct prototype link. **B, live:** it runs
[`screening.ts`](../simulations/township-3d/screening.ts) in the browser on `inputs.json`, so sliders recompute at
once. Planned for the 11 Nov refined submission. **`screening.py` stays the reference**: any change to the method is
made there first, then ported, then `check_parity.ts` must pass. That way the website, the video and the deck never
show different numbers. The web stack itself is still the frontend track's call; everything below is stack-neutral.

**Parity** (`node --experimental-strip-types check_parity.ts`, from `simulations/township-3d/`, Node 22+): runs Python
and TypeScript on `inputs.json`, 6 edge cases (trunk drain full / huge, no pond outlets, what-if pond overflowing /
huge outlet, all values sourced) and 200 randomly perturbed input sets, and compares every output field (relative
tolerance 1e-9). **21 Oct: 207 of 207 match.** A planted 0.1 % bug was caught in 148 cases, so the check is real.

**Hand-off package** (`simulations/township-3d/exports/`, written by
[`export_glb.py`](../simulations/township-3d/export_glb.py), run in Blender after `drive_scene.py`):

| File | Size | What |
|---|---|---|
| `township.glb` | 3.5 MB | 1,518 objects, Draco-compressed (`KHR_draco_mesh_compression`: the loader needs a Draco decoder), Y up, custom properties as glTF `extras`. No animations, cameras or lights. Modifiers applied (pond cuts in the ground) except the toon outlines. **Materials:** the toon shaders do not survive glTF, so the export swaps in plain `web_*` materials in the Ghibli palette (`web_wall_0..4`, `web_roof_0..4`, `web_road`, `web_water`, `web_zone_Z01…`, `web_flow`, …); the site restyles by these names |
| `trees.json` | 0.2 MB | 5,007 rows `[x, y, z, scale, kind]` for the one `tree_proto` mesh. **Blender coordinates**; glTF / three.js position = `(x, z, −y)`, uniform scale, no rotation. Draw with instancing (the merged trees were 70 % of a 61 MB first export) |
| `outputs.json` | 12 kB | Mode A: the three scenarios, `illustrative`, `placeholder_inputs` |
| `inputs.json` | 18 kB | Mode B: the inputs for `screening.ts`; also the source and status of every value, for an "about these numbers" panel |

**What the site drives, by object name** (the data contract, 4.7):

| Object | From | How |
|---|---|---|
| `zone_Z01`…`Z09` (material `web_zone_Zxx`, transparent) | `scenarios.<s>.zones.<id>.band` | Colour and opacity per band. Blender used low = emerald, medium = amber, high = red, unknown = grey, neutral = warm white at 18 %. Each zone's `extras` also hold `band_<scenario>` |
| `pond_A_water`, `pond_B_water`, `pond_whatif_water` | `scenarios.<s>.ponds.<id>.fill_pct` (what-if: `.what_if_pond.fill_pct`) | Height = `gauge_z_empty + fill_pct × (gauge_z_full − gauge_z_empty)` (from `extras`; Blender Z = glTF Y). **A gauge, not a depth** |
| `pond_whatif`, `pond_whatif_water` | scenario | Shown only in `upstream_plus_pond` (`extras.shown_in_scenario`) |
| `rr_upstream_change` | scenario | Morph target `built`: weight 0 for `now`, 1 for the upstream scenarios |
| `rr_flow_arrows`, `rr_flow_arrows_cross` | always (fade in with rain) | Ribbons whose UV U = distance / 30 m along the OSM way direction. Scroll a chevron texture along U. `_cross` is the council-line crossing drain |
| `spot_1`…`spot_3` | — | Flood-spot pins. Proxy names in the export; the real street is in `extras.internal_name` and `proxy_for` |

**Checked 21 Oct 2026:** Khronos glTF Validator: 0 errors, 0 warnings. Loaded in Chromium with three.js r169
(GLTFLoader + DRACOLoader, trees as `InstancedMesh`) in 0.4–0.6 s locally: all 9 zones, the ponds, the pond gauge
(pond A at 91 % → height 2.192 m, as in Blender) and `spot_1`…`spot_3` found. **Performance note for the site:** about
2,900 draw calls and 0.94 M triangles as exported. Fine on a laptop. For phones, merge static meshes by material at
load (three.js `BufferGeometryUtils.mergeGeometries`), keeping the zones, pond water, what-if pond, upstream blocks
and arrows as separate objects.

**Rules the site must keep:** show "illustrative values" whenever `illustrative` is true (mode A) or `placeholders()`
returns anything (mode B). State scenario differences, never attributions. No depths, no forecast. The town fabric is a
simulated layout; say so once on the page.

**Names:** node names no longer carry the flood streets. `extras` still hold sources and `proxy_for` (real place
names), by design, because the sources must stay citable. `water_tasik_setia_alam` keeps its name **[decide if the site
lists object names]**.

### 5.8 Simulator v2 on sourced values (21 Oct 2026, team leader)

**Why:** no sourced inputs were available, so the team leader asked Claude to source them, and chose
**option (a)** for pond capacity: no capacity is claimed; the headline is **storage required**, and a planner may enter
a stated capacity to see the gap. Full sourcing, the result and the sensitivity table:
[../research/HY_screening_inputs.md](../research/HY_screening_inputs.md).

| Change from v1 | v2 |
|---|---|
| Rainfall | MSMA 2 IDF (Eq. 2.2), gauge 2913001 Telok Gong, ARI 100 yr; durations 0.5–24 h; the **design storm is today's critical duration**, used for every scenario |
| Runoff C | MSMA 2 Table 2.5 (major system), area-weighted over each zone's land cover ([`landcover.py`](../simulations/township-3d/landcover.py)) |
| Pond release | Pre-development peak (MSMA 1.2.1, Qpost ≤ Qpre, former oil palm C 0.40), limited by room in the trunk drain |
| Trunk drain | Manning (n 0.018, Table 2.3) on an **assumed** 6 m concrete trapezoid (L) |
| Pond capacity | **Planner input**, none by default (option a) |
| Bands | Change versus today (≥ 1.05 medium, ≥ 1.20 high); against capacity when one is entered |
| Inputs file | Written by [`make_inputs.py`](../simulations/township-3d/make_inputs.py); 0 placeholders, so the label is now **"Screening estimate · MSMA 2"** |
| Parity | `check_parity.ts`: 210 of 210 cases match (21 Oct); a planted 0.1 % bug is caught in every case |

**Result:** a 100-year, 3-hour design storm. Pond A must hold **151,100 m³** and pond B **83,600 m³**, because the
shared trunk drain is full. The upstream change adds **10 %** to the trunk drain's load. A 25,000 m³ what-if pond cuts
pond A's need by **17 %**. **The trunk drain's size decides the story** (sensitivity, research file section 4): with
a main-ditch-sized drain, the upstream change raises the ponds' storage need by 10–16 %. That is why the website makes
it a slider.

The scene driver (`drive_scene.py`) was updated: pond gauges, storage captions, and the status label on every frame
are now "SCREENING ESTIMATE · MSMA 2 method · not a design, not a forecast". The `.glb` was re-exported.

## 6. Order of work (deadline 23 Oct 2026, 11:59 p.m.)

1. Confirm the MCP link; save a clean `.blend`. **Done 20 Oct.**
2. Agree the style. **Done 20 Oct: Ghibli-inspired look (4.6)**, after stylised (4.3) and ink (4.5) were tried.
3. Import and style the base layers; drop the 216 m² basin. **Done 20 Oct**, extended to the hybrid base (4.4), the
   OSM check and fixes (4.6a) and the clean simulated town (4.6b).
4. Draft zones. **Done 20 Oct (draft): 9 zones (4.8)**; check map
   `data/zones_check.png`.
5. Write `screening.py` with placeholder inputs. **Done 20 Oct (5.5).** Real inputs sourced 21 Oct (5.8).
6. Drive the scene. **Done 20 Oct (5.6):** bands, pond fill, flow arrows (incl. the council-line crossing), rain, the
   30 s keyframed sequence, and the "illustrative values" label on every frame. Re-run `drive_scene.py` when the inputs
   change.
7. Render fly-through shots and stills for the video and deck. Cameras in the file: `cam_hero` (low, with sky),
   `cam_overview`, `cam_style`, `cam_check`, `cam_close`.
8. Export `.glb` with custom properties for the frontend track. **Done 21 Oct (5.7)**, with `screening.ts` and the
   parity check, so the website can run precomputed (A) and live (B). Re-run `export_glb.py` after any model or
   input change.

## 7. Open questions and risks

- **Hydrology inputs** were sourced on 21 Oct (5.8); the weakest is the trunk drain size (L).
- **Zones** are a draft; a wrong zone map undermines the bands. Weakest: Z05, Z06 (no internal drain),
  Z09 (outlet unknown), the council-corner split, the A–B pond link (4.8).
- **The upstream mechanism is an assumption.** In the simulator, the upstream change reaches the ponds **only** by
  using up the shared trunk drain, which leaves less room for the pond outlets (5.5). It is a reasonable screening
  idea, and it is the core of the story, so it is stated as an assumption on every screen.
- **Pond capacities** have no public source for pond A and B.
- **Invented town fabric:** say once in the deck or video that the town is a simulated layout loosely based on BBR and
  that the ponds, drains, ditch, council line and flood streets are mapped. Never present generated buildings as BBR's.
- **Render time:** about 4–9 s per 1920 × 1080 frame in the Ghibli look (20 Oct 2026); a fly-through is feasible.
  The file is ~52 MB and full rebuilds are slow.
- **Band colours vs the scene:** the scene is green-leaning; use a strong emerald for "low" or colour only medium and
  high (4.6).
- **To verify:** township names on the boundary labels (Bandar Bukit Raja, Setia Alam); how the architecture student
  built the sketch (it aligns with OSM to 0.66 m, so likely OSM-based); Esri imagery licence before any satellite
  image goes public; flood-pin dates; the Persiaran Batu Belah source.
- **Elevation:** no defensible height difference between the Klang and Shah Alam sides (4.6b); show the upstream link
  with flow arrows, not terrain.
- **Web version**: Next.js + React Three Fiber on Vercel was suggested by Eujin and is **not decided**.
- **Asset licences** for anything imported from online libraries.
