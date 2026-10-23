# AR1c — QGIS MCP refinement plan for the BBR Phase 1 site model

**Owner:** Team leader · **Date written:** 11 October 2026 · **Status: worked through on 11 October 2026**

> **Outcome — read this before re-running anything.**
> **Phase 0 failed:** the QGIS MCP server could not start (no `uv`/`uvx` on the machine) and **QGIS is not
> installed** at all, so none of the five capability checks passed. Section 8 fallback 2 was taken and everything
> below was done in Python instead, with one extension: basemap tiles were fetched over HTTP and read as images,
> so **Phase 2 was done in full** rather than skipped.
> **Phase 1** done — layers in [AR1_site_model/gis/](../AR1_site_model/gis/), extents check passed.
> **Phase 2** done — nine checks, eight answered, written into [AR1_site_model.md](../AR1_site_model.md). Biggest
> finding: OSM has only an estimated 40–60% of the buildings. Check 8 (storeys) is **not answerable** from
> near-nadir imagery and was not guessed at.
> **Phase 3** still blocked — JPS returned HTTP 503 again on 11 October 2026.
> **Phase 4** done and the result **rejected**: FABDEM was unobtainable and non-commercial, Copernicus GLO-30 was
> used, and terrain-derived catchment delineation does not work on this plain — the surface model climbs 8.5 m
> over the motorway embankment where the ditch passes under it. The figure this plan hoped for cannot be produced
> from this data. Section 6c's expectation does not survive contact with the evidence.
> **Phase 5** done, except that `terrain.obj` was **not** replaced; GLO-30 ships alongside it as
> `terrain_cop30.obj` and as a fourth surface in the viewer, because it is a different surface model, not a
> better one.

**How to use this.** It is written to be handed to a fresh Claude session that has none of the earlier context.
Read section 0 first, then section 1, then work the phases in order. Each phase states what done looks like and what
to record. Stop and report if a phase's exit check fails — do not improvise past it.

---

## 0. Context a new session needs

### What this is

A simulated township for the Sime Darby Property University Hackathon 2026, based on a real block of Bandar Bukit
Raja (BBR), Klang, Selangor, Malaysia. An architecture student models it in **Blender or SketchUp only**. The point
of the model is to show how water crosses the Klang / Shah Alam council boundary. Read
[../CLAUDE.md](../../CLAUDE.md) and [AR1_site_model.md](../AR1_site_model.md) before touching anything.

### Extents, fixed — do not change them

| | Latitude | Longitude | Size |
|---|---|---|---|
| **3D model extent** | 3.0845 – 3.0955 N | 101.4250 – 101.4470 E | 1.22 × 2.45 km, ≈3.0 km² |
| **Hydrology extent** | 3.080 – 3.110 N | 101.415 – 101.465 E | ≈18 km² |

**Local projection used by the existing exports:** origin at **3.0900 N, 101.4360 E**, X east, Y north, Z up,
metres. Metres per degree used: lat 110574, lon 111158.

**Suggested working CRS in QGIS:** **EPSG:32647** (WGS 84 / UTM 47N). Malaysia's national grid is **EPSG:3375**
(GDM2000 / Peninsular Malaysia RSO) — use it if anything official has to line up.

### What already exists, and must not be redone

In [AR1_site_model/](../AR1_site_model/), all in metres, X east / Y north / Z up, origin as above:

| File | Contents |
|---|---|
| `rainready_site.geojson` | **Start here.** Everything in WGS84: 633 buildings, 487 roads, 65 drains, 4 water bodies, council line |
| `terrain.obj` | 41 × 82 ground mesh, SRTM 30 m smoothed |
| `buildings.obj` | 633 extruded footprints, grouped by type. **Heights assumed** |
| `water.obj`, `roads.obj`, `drains.obj`, `council_line.obj` | As named |
| `site_model.html` | Standalone 3D viewer |

Published viewer: <https://claude.ai/artifact/WbjXfctgufzpWse3Zm3FMx>

### Key features, with coordinates

| Feature | Position | Status |
|---|---|---|
| Retention pond A | 3.0891 N, 101.4348 E | 55,611 m². OSM name `Flood Retention Pond`. **Unverified against imagery** |
| Retention pond B | 3.0851 N, 101.4350 E | 57,255 m². OSM name `Flood Retention Pond`. **Unverified** |
| Tasik Setia Alam | 3.0945 N, 101.4473 E | Western part only inside the frame |
| Small basin | 3.0928 N, 101.4443 E | 216 m². Probably too small to be a pond. **Low confidence** |
| Council corner | 3.0929 N, 101.4443 E | OSM way 1231162275, relations 10715532 (Klang) / 8347577 (Shah Alam) |
| Main ditch | 3.1012 N, 101.4424 E → 3.0917 N, 101.3939 E | OSM way 888406336, 5.66 km, drains north-east to west |

### Known problems in the current model

1. **Every building height is assumed.** No building in the extent carries a `height` or `building:levels` tag.
2. **Terrain is unreliable.** SRTM 30 m. Two DEMs disagree by 5–6 m on this plain. Point-to-point noise reaches 7 m
   over 150 m on flat ground.
3. **Nothing has been checked against satellite imagery.** This is the largest open item.
4. **No catchment boundary exists.** Upstream and downstream are known only by direction.

---

## 1. Honest answer: what QGIS MCP will and will not improve

**It will not add much detail to the 3D model.** The model's detail ceiling is set by the **source data**, not by the
tool. QGIS does not create data. The OSM extract already pulled is the same data QuickOSM would fetch, and QGIS
cannot invent building heights or raise a DEM's resolution.

**What it genuinely adds, in order of value:**

1. **Satellite imagery verification** — the one thing nothing else in the toolchain can do, and the largest open
   item on this project. Pond outlines, the council line, the 216 m² basin, missing buildings.
2. **Terrain and hydrology processing** — with a better DEM, QGIS can fill sinks, derive flow direction and flow
   accumulation, and delineate a catchment. That is the only route to answering the upstream/downstream boundary
   question properly.
3. **Correct projection and measurement** — proper metric CRS instead of the hand-rolled approximation above.
4. **Repeatability** — a `.qgz` project the team can reopen, instead of ad-hoc scripts.
5. **Contours and section lines** for the architecture student, which OBJ alone does not give.

**Set expectations accordingly.** The deliverable at the end of this plan is a **verified** model, not a more
detailed one. Verified is worth more to the pitch than detailed.

---

## 2. Phase 0 — Capability check

**Do this before anything else and report the result.** The plan below assumes capabilities described in a
third-party summary that has not been tested.

1. Confirm the QGIS MCP server is connected and list every tool it exposes.
2. Confirm whether QGIS must be running with a project open, and whether the plugin needs the GUI.
3. Test one trivial round trip: create a point layer, add one feature, read it back.
4. Check whether these are reachable **through the MCP** or only by hand in the GUI:
   - **QuickOSM** (Overpass queries)
   - **QuickMapServices** (basemap tiles)
   - the Processing toolbox, specifically GDAL and **SAGA or GRASS** hydrology tools
5. Check whether the MCP can **export a rendered map image** that this session can then read back.

**Exit check:** a written list of which of the five phases below are actually possible. If 4 or 5 fail, go to
section 8.

---

## 3. Phase 1 — Project setup

1. New QGIS project, CRS **EPSG:32647**.
2. Load `AR1_site_model/rainready_site.geojson`. Split into layers by geometry and attribute:
   buildings, roads, drains, water, council line.
3. Create two rectangle layers for the **3D model extent** and the **hydrology extent** from the coordinates in
   section 0.
4. Add the six key features from section 0 as a labelled point layer.
5. Save as `AR1_site_model/rainready.qgz`.

**Exit check:** every layer renders in the right place, and the two extent rectangles measure ≈1.22 × 2.45 km and
≈18 km². If the sizes are wrong, the CRS is wrong — stop.

---

## 4. Phase 2 — Imagery verification (highest value, do this first)

Add a satellite basemap through QuickMapServices, then check each item and **record a verdict and a confidence
letter for every one**.

| # | Check | Verdict to record |
|---|---|---|
| 1 | **Pond A** 3.0891 N, 101.4348 E | Water visible? Outline matches OSM? Over- or under-sized? |
| 2 | **Pond B** 3.0851 N, 101.4350 E | Same |
| 3 | **Small basin** 3.0928 N, 101.4443 E | Is there anything there at all? |
| 4 | **Tasik Setia Alam** 3.0945 N, 101.4473 E | Extent inside the frame |
| 5 | **Council line** along 3.0929 N and 101.4443 E | Does it follow a visible feature — road, drain, fence line — or cut through blocks? |
| 6 | **Main ditch** way 888406336 | Visible as an open channel? Estimate its width. This is the one capacity clue available |
| 7 | **Building coverage** | Sample 3–4 areas. Roughly what share of visible buildings are mapped? Note any whole missing rows |
| 8 | **Building storeys** | Sample 20 houses and 10 shoplots. Count storeys from shadows or obliques if the imagery allows. Mark **L** — this is estimation, not measurement |
| 9 | **Wetland Townpark** | Water bodies east of the extent, 101.449–101.457 E at 3.089–3.095 N. Is any of them it? |

**Record for every check:** the imagery **source, date and licence terms**. If the date is unknown, say so. Do not
put an image into the deck without its attribution and reuse terms.

**Exit check:** a table of 9 verdicts with confidence letters, written into
[AR1_site_model.md](../AR1_site_model.md) under a new "Imagery verification" section.

---

## 5. Phase 3 — Official JPS layers

See [../documentation/PROBLEM_VALIDATION.md](../../documentation/supporting/PROBLEM_VALIDATION.md) for background.

JPS Selangor runs an ArcGIS server at `jpsselgis.selangor.gov.my` carrying layers named **`KOLAM_TAKUNGAN_MSMA`**,
**`Parit2022`** and several **`Kawasan_Tadahan`** (catchment) layers. On 11 October 2026 its REST endpoint returned
**HTTP 503** on every attempt.

1. Retry `http://jpsselgis.selangor.gov.my/gis/rest/services?f=json`.
2. If it responds, add the services to QGIS as ArcGIS REST connections and look for the three layer groups.
3. If `KOLAM_TAKUNGAN_MSMA` loads, **compare its pond outlines with the OSM ones**. Official geometry would replace
   volunteer tags and close the largest confidence gap in the model.
4. If `Kawasan_Tadahan` loads, that is an **official catchment boundary** and supersedes everything in Phase 4.

**Only read. Do not attempt any authenticated or non-public endpoint.** If it is still 503, record the date and
move on. Mark the whole phase **[TBD]**.

**Exit check:** either official layers loaded and compared, or a dated note that the server was unavailable.

---

## 6. Phase 4 — Terrain upgrade and catchment delineation

### 6a. Get a better DEM

**FABDEM** removes buildings and trees from Copernicus GLO-30. Hosted by the University of Bristol,
dataset `25wfy0f9ukoge2gs7a5mqpq2j7` on `data.bris.ac.uk`, supplied as 10° × 10° zips containing 1° × 1° tiles.
For this site you need the tile covering **N03 E101** — likely inside the `N00E100-N10E110` pack. Exact filename
**[verify]**.

> **Licence warning.** FABDEM V1-0 tiles are listed under a **Non-Commercial Government Licence**. A student
> hackathon entry is very likely fine, but the competition scores **Commercial value**, so if this ever becomes a
> product the licence is a problem. **Record this in the appendix.** If it matters, use **Copernicus GLO-30**
> directly instead — openly licensed, same base, but buildings and trees not removed.

### 6b. Process it

1. Clip to the **hydrology extent**, reproject to EPSG:32647.
2. Compare against the existing SRTM surface. Record where they differ and by how much — this either settles or
   deepens the 5–6 m disagreement already documented.
3. Derive hillshade, slope and **0.5 m contours** over the 3D extent.

### 6c. Hydrology — the real prize

Using SAGA or GRASS in the Processing toolbox:

1. **Fill sinks** on the clipped DEM.
2. **Flow direction**, then **flow accumulation**.
3. Extract a **synthetic stream network** and compare it with the 65 mapped drains and the main ditch. Do they
   agree? Where they disagree, the drains probably win, because engineered channels cross natural divides.
4. **Delineate the catchment** draining to a pour point on the west edge at about **3.0931 N, 101.4236 E** — where
   the main ditch leaves the block.
5. Overlay the council line on that catchment.

**This is the figure the whole pitch has been missing:** the catchment in one colour, the council boundary cutting
across it, showing that the drainage area and the jurisdiction do not coincide.

> **Honesty requirement.** On ground this flat, with 30 m cells, a delineated catchment is **indicative, not
> authoritative**. Label it **M at best**, state the method, and never present it as the official catchment. If
> Phase 3 produced `Kawasan_Tadahan`, use that instead and say so.

**Exit check:** a catchment polygon, a stream network, contours, and a written comparison of FABDEM against SRTM.

---

## 7. Phase 5 — Regenerate the deliverables

1. Re-export `terrain.obj` from the FABDEM surface, same origin and orientation as section 0, so it drops straight
   into the existing scene.
2. Re-seat buildings on the new ground. Apply any storey estimates from Phase 2 check 8, and **keep the assumed
   heights clearly labelled as assumed**.
3. Correct any pond outline that Phase 2 showed to be wrong.
4. Add two new files for the architecture student: **contours** (DXF or SVG) and **one or two section lines**
   across the block.
5. Export a labelled **plan map** as PNG at a stated scale — for the deck and for the student's reference.
6. Update the viewer at <https://claude.ai/artifact/WbjXfctgufzpWse3Zm3FMx> rather than publishing a new one, so
   the link the team already has keeps working.
7. Update [AR1_site_model.md](../AR1_site_model.md): the verification table, the new terrain source, revised
   confidence letters.

**Exit check:** the architecture student can open the new files and see what changed and why.

---

## 8. If QGIS MCP does not work

Nothing here depends on QGIS specifically. Fallback, in order of preference:

1. **QGIS by hand, Claude processes the files.** The user does imagery checks and layer loading in the GUI and
   reports verdicts; Claude does the DEM maths, exports and documentation in Python. Loses automation, keeps every
   outcome.
2. **Python only.** `rasterio`, `richdem` or `pysheds` and `shapely` cover clipping, sink filling, flow
   accumulation and catchment delineation. **None of these are currently installed** — the machine has `numpy`,
   `requests` and `PIL` only. Imagery verification would still have to be done by eye.
3. **Drop Phase 4, keep Phase 2.** Imagery verification is the highest-value phase and needs no hydrology tooling.

---

## 9. What to record, whatever happens

Every phase writes back into [AR1_site_model.md](../AR1_site_model.md):

- Each verification verdict with **H / M / L**.
- Every data source with its **date, provider and licence**.
- Anything that **contradicts** what is already written. Earlier claims in this project have already had to be
  retracted once; correcting the record is normal and expected.
- Anything still open as **[verify]** or **[TBD]**.

**Do not** quietly raise a confidence letter. State what new evidence moved it.

---

## 10. Risks

| Risk | Note |
|---|---|
| Imagery licence | Basemap tiles may not be reusable in a deck. Check before embedding. **[verify]** |
| Imagery date | A pond may have been built or filled since the image. Record the date |
| FABDEM licence | Non-commercial. Conflicts with the Commercial value criterion if it ever ships |
| JPS server | May stay 503 indefinitely |
| Flat-ground hydrology | Catchment delineation on a 30 m DEM over a 3 m fall is indicative only |
| Scope creep | Phase 2 alone justifies the whole exercise. If time runs short, do Phase 2 and stop |
