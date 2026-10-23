# AR1b — What exactly should the architecture track model, and how much of it is reliable?

**Owner:** Team leader (for Architecture) · **Date:** 11 October 2026 · **Confidence: M**

Follow-on to [AR1_study_area_selection.md](AR1_study_area_selection.md), which chose the extent. This note turns that
extent into something that can be modelled: real building footprints, roads, ponds, drains and the council line,
with a ground surface and an explicit statement of what is measured and what is assumed.

Method: online only. Geometry from OpenStreetMap via the Overpass API, queried 11 October 2026. Ground levels from
SRTM 30 m via the Open Topo Data public API, same date. No site visit, no survey, no satellite imagery check yet.

---

## Answer in five lines

The block holds **633 mapped buildings, 487 road ways, 65 drains and ditches, four water bodies and one council
boundary line** — enough to model without inventing anything, **though an imagery check on 11 October 2026 found
those 633 footprints are only an estimated 40–60% of the buildings standing in the frame, with whole estates in the
west and north-west unmapped**. Footprints and street positions are mapped data and can
be trusted. **Every building height is an assumption**, because not one building in the extent carries a height or
storey tag. The ground is the weak part: two global DEMs disagree by 5–6 m on this plain, so the model should carry
the **direction** of fall and not the absolute metres. Nothing here is a flood model, and the elevation data could not
support one. AR1's proposed drainage corridor **is not confirmed**: a denser transect breaks it into two separate
depressions with higher ground between them, one of which sits next to mapped wastewater ponds. A persistent low does
sit at the council corner, but a low spot is not a flow path.

**Deliverables:** an interactive 3D view at
[claude.ai/artifact/WbjXfctgufzpWse3Zm3FMx](https://claude.ai/artifact/WbjXfctgufzpWse3Zm3FMx)
(private — share it before the architecture student can open it), and importable files in
[AR1_site_model/](AR1_site_model/).

**Correction, 20 October 2026.** The road layer (`roads.obj`, `gis/roads.geojson`) **leaves out `highway=construction`
and all `*_link` ways**. That drops most of the West Coast Expressway (Lebuhraya Pesisiran Pantai Barat) across the
north of the block, which OSM still tags as under construction although the imagery shows it built, and 30 ramps.
The 38 missing ways are in [`gis/roads_supplement.geojson`](AR1_site_model/gis/roads_supplement.geojson). The road
counts above exclude them. Found while checking the 3D model; see
[TOWNSHIP_3D_AND_SIMULATOR.md](../documentation/TOWNSHIP_3D_AND_SIMULATOR.md) section 4.6a.

---

## Evidence

### What is in the extent (3.0845–3.0955 N, 101.4250–101.4470 E)

| Layer | Count | Detail | Confidence |
|---|---|---|---|
| Buildings | 633 | 415 house · 116 retail · 68 untyped · 15 semi-detached · 14 commercial · 3 roof · 1 hospital · 1 office | **H** for position and footprint |
| Road ways | 487 | 175 residential · 171 service · 86 tertiary · 35 unclassified · 17 trunk · 3 motorway | **H** |
| Drains and ditches | 65 | 44 tagged `drain`, 21 tagged `ditch` | **M** — position only, no section or depth |
| Water bodies | 4 | see below | **M** |
| Council line | 1 way | OSM way 1231162275, source tagged `Sinar Project` | **M** |

Mean footprint by type: house 99 m², retail 198 m², semi-detached 204 m², commercial 1625 m², office 756 m²,
hospital 4496 m². A 99 m² mean for the 415 houses is consistent with a standard terraced lot, which is a useful
cross-check that the OSM data is sane.

### The named streets from the 2024 memorandum are all present

Jalan Makyong appears as about 20 numbered branches (`Jalan Makyong 1/KU5`, `2B`, `4D`, `6E` and so on),
Jalan Sumazau as about 6 (`1E`, `2B`, `3C`, `4/KU5`), and Persiaran Batu Belah runs along the south.
Also inside the frame: Persiaran Sungai Keramat, Jalan Meru, Persiaran Setia Prima, Jalan Kuda Kepang, Jalan Rodat,
Jalan Gamelan. **H**

### Water bodies

| OSM id | Name tag | Type tag | Centre | Area | Confidence |
|---|---|---|---|---|---|
| 399570465 | `Flood Retention Pond` | pond | 3.0891 N, 101.4348 E | **55,611 m²** (5.6 ha) | **M** |
| 359496461 | `Flood Retention Pond` | lake | 3.0851 N, 101.4350 E | **57,255 m²** (5.7 ha) | **M** |
| 164881251 | — | flood_retention_pond | 3.0945 N, 101.4473 E | 16,677 m² inside the frame | **M** |
| 1329584049 | — | flood_retention_pond | 3.0928 N, 101.4443 E | **216 m²** | **L** |

The first two are the ponds AR1 located, and they match its coordinates to within about 10 m. AR1 recorded them as
OSM tags; both in fact carry the **name** `Flood Retention Pond`, which is slightly stronger than a bare tag, though
still volunteer-entered. The third is the western part of Tasik Setia Alam. The fourth is new since AR1 and is only
216 m², which is too small for a retention pond — treat it as unconfirmed.

A wider query over the 18 km² hydrology extent found **25 water bodies**, including a chain east of the model extent
at 3.0893–3.0906 N, 101.4488 / 101.4534 / 101.4573 E. This is the chain AR1 flagged as a possible Wetland Townpark.
Still **[verify]**.

### The council line, located precisely

AR1 could only bracket it between 3.0925 N (Klang) and 3.0935 N (Shah Alam). The boundary relations for
**Bandaraya Klang** (OSM relation 10715532) and **Shah Alam** (relation 8347577) share one way, 1231162275, whose
vertices through this area are:

```
3.092872 N, 101.468709 E
3.092906 N, 101.444343 E   <- corner, inside the model extent
3.095012 N, 101.443847 E
3.109798 N, 101.442055 E
```

Inside the extent the line therefore enters the **east edge at about 3.0929 N**, runs **west to a corner at
3.0929 N, 101.4443 E**, then turns **north-north-west** and leaves the north edge near 101.4438 E. That corner sits
about 350 m north-east of the end of Jalan Sumazau. **M** — this is OSM's administrative boundary, not cadastral.

Worth noting without drawing a conclusion: the 216 m² basin (id 1329584049) sits almost exactly on that corner.

### Ground levels — the two DEMs disagree *(a third was added on 11 Oct 2026; see Terrain and catchment)*

| | AR1 (Open-Meteo, ~90 m) | This note (SRTM 30 m) |
|---|---|---|
| Phase 1 plain | 4–6 m | 8–12 m |
| Retention pond A | 4 m | 11 m |
| Retention pond B | 4 m | 10 m |
| Range across the block | — | 1–18 m raw, 4.8–15.7 m smoothed |
| Hill to the south-east | 25–39 m | 31–60 m, peak at 3.0800 N, 101.4639 E |

Both agree on the **pattern** and disagree on the **numbers**. A least-squares plane through the smoothed SRTM
surface falls toward **bearing 210°, south-south-west, at about 1.3 m per km**. AR1 recorded the fall as
north-east to south-west. Those are the same story. **M**

Across the 18 km² hydrology extent SRTM spans 0–60 m, with the low ground west and south-west
(lowest at 3.0800 N, 101.4217 E) and the high ground south-east. The model block sits on that slope and is
nearly flat within itself.

### Where the upstream area is

Upstream is the **eastern and north-eastern side — the Setia Alam ground, across the council line.** Mean elevation
of each quarter of the 18 km² hydrology extent, SRTM 30 m:

| Quarter of the hydrology extent | Mean | Max |
|---|---|---|
| South-east | 16.3 m | 60 m |
| North-east | 14.2 m | 41 m |
| North-west | 10.4 m | 18 m |
| South-west | 7.7 m | 16 m |

Jalan Makyong reads 5 m and Jalan Sumazau 7 m, so the streets named in the memorandum sit at the bottom of that
slope. **M** — the pattern is consistent across both DEMs even where the absolute values are not.

There are **two distinct higher areas**, and only one of them is settled:

- **Setia Alam, north-east.** About 13–14 m at the town, rising to 41 m in that quarter. Tasik Setia Alam reads 14 m.
  This is the side the residents' case and the council-boundary argument rest on. **M**
- **The hill to the south-east**, reaching 60 m at 3.0800 N, 101.4639 E. Higher, but whether it drains into Phase 1 or
  away to the south cannot be told from quarter means. **Unresolved — [TBD]**

**How much higher, honestly.** The east side averages only about **6–8 m above the west** across roughly 2–3 km — a
regional slope of a few metres per kilometre, not a visible hillside. The large maxima (60 m and 41 m) sit at the far
eastern edge of the 18 km² box, 2–3 km from Phase 1, and may well drain into a different catchment entirely. So the
quarter means establish a direction and nothing more.

**What the upstream claim actually rests on.** Not this DEM. It rests on the public record already logged in
[BBR_PUBLIC_DOCUMENT_SURVEY.md](../documentation/supporting/BBR_PUBLIC_DOCUMENT_SURVEY.md) — residents' accounts of water arriving
from the Setia Alam side, the two councils, and Shah Alam's own RM150m programme of works for Setia Alam. The terrain
here is **consistent with** that account at the regional scale. It does not independently prove it, and it cannot show
the path.

### AR1's drainage corridor — tested, and it does not hold up

AR1 proposed a low corridor running west from the Setia Alam edge into Phase 1, read off the 90 m DEM at two cells
(3.0933 N at 101.447 E and 101.453 E, both 5 m), and used it to justify placing the model's eastern edge at about
101.447 E. It was marked **[verify]**.

A first, coarse re-sample at three longitudes appeared to support it. **A dense transect along the same latitude does
not.** SRTM 30 m, west to east along 3.0933 N:

| 101.438 | .4395 | .4410 | .4425 | **.4440** | **.4455** | .4470 | .4485 | .4500 | .4515 | **.4530** | .4545 | .4560 | .4590 | .4620 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 12 | 10 | 10 | 10 | **4** | **4** | 8 | 7 | 7 | 8 | **4** | 11 | 9 | 14 | 25 |

Three problems with reading this as a corridor:

1. **It is not continuous.** The two low areas — 101.4440–101.4455 and 101.4530 — are separated by 7–8 m ground
   across 101.4470–101.4515. They are two depressions with a sill between them, not one lane.
2. **At 101.447 E, the cell AR1 cited as 5 m, SRTM reads 8 m** — not a low at all, and the local high point of the
   western depression's eastern shoulder.
3. **The 4 m cell at 101.4530 is 111 m from mapped wastewater ponds** (OSM 922786118, 922786119, 922786120 at
   3.0937–3.0940 N, 101.4509–101.4521 E). SRTM returns erratic values over water, so that reading is suspect.

**What does survive.** Both DEMs see low ground at 3.0933 N relative to the ground immediately north and south of it,
and the dense transect puts a persistent 4 m low at **101.4440–101.4455 E** — within about 150 m of the council corner
at 3.0929 N, 101.4443 E, and close to the 216 m² basin. That co-location is worth noting. But a depression is not a
conveying channel, and nothing in this data shows water moving along it in any direction.

**Confidence: L.** AR1's **[verify]** on the corridor **stays open**, and the justification for the 101.447 E eastern
edge rests on the council line and Tasik Setia Alam, not on this corridor.

**Method note.** Point-to-point swings along this transect reach 7 m over 150 m on flat developed ground. That is
noise, not landform. No channel geometry should be read from this DEM at point level — only aggregates over many
cells, as in the quarter means above, are usable.

---

## Imagery verification (11 October 2026)

Done in the AR1c refinement pass. **QGIS was not used** — see
[AR1_qgis_refinement_plan.md](archive/AR1_qgis_refinement_plan.md) section 8: the QGIS MCP server could not start and QGIS
is not installed on this machine. Instead, public basemap tiles were fetched over HTTP, the OSM geometry was drawn
on them, and each check below was read off the resulting image. The images are kept in
[AR1_site_model/verification/](AR1_site_model/verification/).

### The source, and what may be done with it

| | |
|---|---|
| Layer | **Esri World Imagery**, `services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer`, tiles fetched **11 October 2026**, zoom 17–19 (0.60–0.15 m per pixel) |
| Attribution the service publishes | *Source: Esri, Vantor, Earthstar Geographics, and the GIS User Community* |
| Capture date | **Not published per tile.** Bracketed instead with the Esri Wayback archive: the tile over pond A is byte-identical to the Wayback release of **24 September 2026**, differs from the release of 18 December 2025, and was unchanged from 14 December 2022 through 18 December 2025. So the picture being read was **taken between about December 2025 and September 2026**. **M** |
| Earlier states available | Wayback releases back to 2017; 2018, 2020, 2021 and 2022 were pulled for pond A |
| Licence | **Esri's terms of use, not an open licence.** Fine for looking at. **Putting any of these tiles in the deck, the viewer or anything public is [verify] and must be settled before submission.** If it fails, the fallback is to describe what the imagery shows in words and draw the geometry on a plain background |

### The nine checks

| # | Check | Verdict | Conf. |
|---|---|---|---|
| 1 | **Pond A** 3.0891 N, 101.4348 E | Open water, present continuously since at least December 2018. The OSM outline follows the visible edge on the north, east and south; on the **west it runs roughly 10–20 m inside** the water, so the polygon slightly **under**-states the pond. Most of the surface carries a pale floating mat — vegetation or algae. Depth cannot be read from imagery at all | **H** water · **M** outline |
| 2 | **Pond B** 3.0851 N, 101.4350 E | Open water. Outline matches on all four sides within about 10 m; water continues a few metres south of the mapped edge. Same pale surface mat over much of it | **H** water · **M** outline |
| 3 | **Small basin** 3.0928 N, 101.4443 E | **No water.** Scrub and bare ground on the verge of the motorway interchange, beside a mapped drain. It is not a pond. Possibly a dry sump; nothing in the image makes it one | **M–H** |
| 4 | **"Tasik Setia Alam"** 3.0945 N, 101.4473 E | A **landscaped lake** with mown grass banks, in two parts split by a road — real, and well mapped (16,677 m², recomputed 16,691 m² in EPSG:32647). Two corrections: OSM gives it **no name** and tags it `water=flood_retention_pond`, not a lake; and it sits at 101.4464–101.4483 E, so **only a ~60 m western sliver is inside the 101.4470 extent edge** | **H** |
| 5 | **Council line** | The **north–south leg follows a visible feature** — the eastern edge of the main road corridor and its reserve. The **east–west leg does not**: it crosses open grassland with no road, fence or hedge on it, but runs 15–25 m north of, and parallel to, a mapped drain, which is consistent with a drainage or utility reserve. It cuts through no building in this frame. **One mapped drain crosses it**, at 3.09294 N 101.44433 E, together with two roads — counted geometrically, not by eye | **M** |
| 6 | **Main ditch** way 888406336 | Visible as an open channel, and engineered. At **3.0976 N, 101.4337 E** it is a **concrete-lined trapezoidal channel, top width about 8–10 m**, with a low-flow invert. At **3.0941 N, 101.4258 E** the water surface reads about **10–16 m** across in a maintained corridor of roughly 20 m. At the north-east end (3.1012 N, 101.4424 E) it runs along an active earthworks edge and cannot be measured. This is the only capacity clue the project has, and it is a width, not a section | **H** exists · **L–M** width |
| 7 | **Building coverage** | **Uneven, and much worse than assumed.** East sample (101.4428–101.4448 E, 3.0878–3.0893 N): 88 polygons, essentially every visible terrace unit mapped, about 90%. North-west terraces (101.4265–101.4285 E, 3.0932–3.0947 N): **zero** mapped against roughly 80–110 visible units. Older west blocks (101.4262–101.4282 E, 3.0900–3.0915 N): **zero** against roughly 40–60. Central industrial plot (101.4345–101.4365 E, 3.0905–3.0920 N): **zero** against about 10 sheds. Whole estates in the west and north-west of the frame carry no footprints. Best estimate: the 633 mapped footprints are **40–60% of what stands in the extent** | **H** that whole estates are missing · **L** on the share |
| 8 | **Building storeys** | **Not performed — this source cannot answer it.** The imagery is near-nadir with no oblique view, the acquisition time is not published so shadow length cannot be converted to height, and eaves hide most of what little facade there is. Heights stay assumed, exactly as before. The route that would work is Google Street View along the named streets, opened by a person in a browser | — |
| 9 | **Wetland Townpark** | **None of the water east of the extent looks like it.** The window 101.449–101.458 E / 3.089–3.096 N holds four unnamed `flood_retention_pond` polygons (721223351, 740109841, 740109842, and 164881251 from check 4) and three `wastewater` ponds (922786118/9/20) beside a treatment works. Every one of them reads as an unlandscaped detention basin next to industrial or commercial plots — no paths, no planting, no park structure. None is named in OSM. **The Wetland Townpark is still unlocated [TBD]** | **M** |

### What this changes in the rest of this note

- **"No satellite imagery has been consulted" is no longer true.** The line under *Limits* is superseded by this
  section.
- **Assumption 5 is withdrawn.** "The OSM extract is complete enough" does not survive check 7. The extract is
  complete enough for the **east** of the frame and not for the **west**. Any statement of the form "633 buildings is
  what is there" has to become "633 buildings is what OpenStreetMap has mapped, which is roughly half of what
  stands".
- **The ponds are confirmed as water bodies**, which is the first independent support the project has for the two
  5.5–5.7 ha retention ponds. It says nothing about their depth or storage, and the residents' 2024 description of
  the ponds as shallow is neither supported nor contradicted by imagery.
- **"Tasik Setia Alam" is our label, not a source's.** OSM leaves the lake unnamed.
- New measurement from the same pass: the 65 mapped drains total **15,068 m** of channel inside the extent.

---

## Terrain and catchment (11 October 2026)

The second half of the AR1c pass. Same constraint as above: no QGIS, so the DEM work was done in Python
(`rasterio`, `numpy`, `scipy`) with a priority-flood sink fill, D8 flow direction, flow accumulation and an
upstream-tracing catchment, all written for this job and all reproducible from the files in
[AR1_site_model/gis/](AR1_site_model/gis/).

### The DEM: Copernicus GLO-30, not FABDEM

FABDEM was the plan's first choice because it strips buildings and trees. It was **not obtained**: on 11 October
2026 `data.bris.ac.uk` returned HTTP 503 on the dataset page and 404 on the guessed tile-pack name, and FABDEM V1
carries a **Non-Commercial Government Licence**, which sits badly against the competition's Commercial value
criterion. The sanctioned alternative was used instead:

**Copernicus DEM GLO-30**, tile `Copernicus_DSM_COG_10_N03_00_E101_00_DEM`, read from the public AWS mirror on
11 October 2026, clipped to 101.36–101.50 E / 3.045–3.135 N and reprojected to **EPSG:32647** at 30 m.
Licence: free and open, attribution *© DLR e.V. 2010–2014 and © Airbus Defence and Space GmbH … provided under
COPERNICUS by the European Union and ESA*. **It is a surface model (DSM): buildings and trees are in it.** That
matters below.

### GLO-30 against the SRTM surface already in the model

Sampled at all 3,362 vertices of `terrain.obj`, and against raw SRTM 30 m re-fetched from Open Topo Data at 841 of
them:

| Comparison | Mean | Spread (sd) | Range |
|---|---|---|---|
| GLO-30 − `terrain.obj` (smoothed SRTM) | **−3.73 m** | 2.94 m | −9.22 to +5.72 m |
| GLO-30 − raw SRTM 30 m | **−3.70 m** | 3.37 m | −12.62 to +7.12 m |
| `terrain.obj` − raw SRTM 30 m | −0.00 m | 1.40 m | *(this is the smoothing, not a source difference)* |

**This does not settle the disagreement — it widens it.** GLO-30 sits about **3.7 m lower** than SRTM across the
block, with a 3.4 m spread, so a third global source has produced a third answer. Both are surface models, so
neither is ground. The earlier conclusion stands and hardens: **absolute elevation here is unusable; only the
direction of fall and the kilometre-scale pattern survive.**

### Direction of fall — the earlier reading survives, but only at catchment scale

Plane fits to GLO-30:

| Window | Gradient | Falls towards |
|---|---|---|
| Model extent, 3 km² | 5.09 m/km, dominated by the north-east corner | 174° (south) |
| Hydrology extent, 18 km² | **1.30 m/km** | **205° (south-south-west)** |
| Wide window, 156 km² | **2.94 m/km** | **225° (south-west)** |

At 18 km² and wider, GLO-30 agrees with AR1b: the ground **rises to the east and north and falls to the
south-west**, so "upstream is east" holds. Over the 3 km² block itself the fit is meaningless — the block is flat,
median slope **1.09%**, 90th percentile 3.55%, and the apparent 5 m/km is one corner of high ground, not a slope
across the site. **M** at catchment scale, **L** inside the block.

### The catchment delineation — attempted, and it does not stand up

Done exactly as planned: fill sinks (31% of cells raised, mean rise 0.88 m, max 13.5 m — the signature of a very
flat surface), D8, flow accumulation, then trace everything draining to the pour point at **3.0931 N, 101.4236 E**
where the main ditch leaves the block.

| Variant | Catchment at the pour point |
|---|---|
| Terrain only, as the plan specifies | **1.94 km²** |
| Mapped drains burned 1 m into the DEM | 1.22 km² |
| Burned 5 m | 1.25 km² |
| Burned 20 m | 21.34 km² |

**Do not use any of these numbers.** Three pieces of evidence say the routing is wrong, not merely uncertain:

1. **The DSM climbs along a channel that can only fall.** Along the 28 nodes of the main ditch (OSM way 888406336)
   GLO-30 runs from 4.07 m to **17.19 m**, with **eight** node-to-node rises above 0.5 m and one of **+8.5 m**. Those
   are the motorway embankment and its flyovers, captured as ground. A D8 router cannot cross them, so the modelled
   water never follows the real channel.
2. **The modelled flow leaves in the wrong direction.** Tracing downstream from the pour point gives 315 cells
   running **south** to 3.0451 N, 101.3966 E. The mapped ditch runs **west**. The window's dominant flow line
   carries 56 km² and does not pass through the block's mapped outlet at all.
3. **The drains have no fall to work with.** The median elevation range along a mapped drain, over its whole length,
   is **0.32 m** — inside the noise of the DEM. And only when the burn depth (20 m) is several times the entire
   relief of the block does the catchment follow the drains, which means that result is the *drain map* speaking,
   not the terrain.

**Conclusion.** On this plain, at 30 m, with a surface model, terrain-derived catchment delineation does not work.
The plan hoped this would be "the figure the whole pitch has been missing". It is not, and presenting it would be
presenting an artefact. **Confidence L — not fit for the deck.** The files are kept
(`catchment.geojson`, `flow_accumulation.tif`, `streams_18ha.geojson`, `streams_90ha.geojson`) so the next person
can see the attempt and its failure rather than repeat it.

**What would actually answer it**, in order of cost: `Kawasan_Tadahan` from JPS Selangor (Phase 3, server down —
see below); a LiDAR or IFSAR DTM for Klang; or a drain-network trace done as hydraulics on the mapped channels
rather than as terrain routing — which is **HY work**, and is now the clear recommendation for the hydrology work.

### What can still be said about the boundary, from geometry alone

No DEM involved, so this part is solid:

- The mapped drain network inside the extent totals **15,068 m**.
- Exactly **one mapped drain way crosses the council line**, at **3.09294 N, 101.44433 E**, together with **two
  roads**. The main ditch does not cross it.
- Both retention ponds, all four water bodies and the whole mapped drain network inside the extent sit on the
  **Klang** side. What crosses the line is a single drain and the road corridor.

### Phase 3 — official JPS layers: still unavailable

`jpsselgis.selangor.gov.my` answers on `/` with a default IIS page (HTTP 200), but its ArcGIS REST endpoint
`/gis/rest/services` returned **HTTP 503 on every attempt on 11 October 2026**, over both HTTP and HTTPS, and
`/arcgis/rest/services` returns 404. So `KOLAM_TAKUNGAN_MSMA`, `Parit2022` and `Kawasan_Tadahan` remain
**[TBD]**. Only public endpoints were tried; nothing authenticated was attempted. Retry before the submission.

### New files from this pass

Everything produced on 11 October 2026 is listed once, in
*Files for the architecture track* below: `terrain_cop30.obj`, the two contour DXFs, the sections, the two plan
maps, `verification/` and `gis/`. Two of them carry warnings worth repeating here:

- **`plan_map_imagery.jpg` is built on Esri tiles and its reuse is not cleared.** `plan_map_clean.png` carries the
  same information with no imagery in it and is free to use.
- **The flow rasters and `catchment.geojson` are the failed attempt**, kept so nobody repeats it. They are not
  evidence of anything except that this method does not work here.

---

## Assumptions

1. **Every building height.** No building in the extent has a `height` or `building:levels` tag, so heights were
   assigned by type: house and untyped 6.5 m, semi-detached 7 m, retail 8 m, commercial and office 11 m, roof 4 m,
   hospital 16 m. These are placeholders for massing only. **L.** If they are wrong, the model looks wrong but no
   analysis changes, because nothing downstream depends on building height yet.
2. **Buildings sit on the smoothed ground**, 0.3 m below the lowest point under each footprint. If the ground
   surface is later replaced with FABDEM, every building re-seats and the export has to be regenerated.
3. **Ponds are flat at the lowest ground on their outline**, minus 0.5 m. Real water level and pond depth are
   unknown. **L.** This matters if the hydrology work ever needs storage volume from the model geometry — it should
   not, and should use the published design figures instead.
4. **A 30 m DEM is treated as ground.** SRTM is a surface model, so it includes trees and buildings. A check comparing
   cells containing a building centroid against cells without found only a **+0.6 m** difference, which is inside the
   noise, so the bias here appears small — but that is a weak test, not a clean one.
5. ~~**The OSM extract is complete enough.**~~ **Withdrawn 11 October 2026.** Checked against imagery, and it is not:
   whole estates in the west and north-west of the frame have no footprints at all, while the east is near-complete.
   The 633 mapped buildings are an estimated 40–60% of what stands. See *Imagery verification* check 7. **L** on the
   share, **H** that the gap is real.

## Limits

- **This is not a flood model and cannot become one on this data.** No depth, no extent, no return period. It is a
  stage to run scenarios over.
- ~~No satellite imagery has been consulted.~~ **Done on 11 October 2026** — see *Imagery verification* above.
  What remains open from it: the Esri licence question, building storeys, and the location of the Wetland Townpark.
- **Absolute elevation is not usable.** Only relative fall and the km-scale pattern survive the disagreement between
  the DEMs — now **three** of them, after Copernicus GLO-30 came in 3.7 m below SRTM on 11 October 2026. FABDEM was
  not obtainable and is non-commercial; what would settle it is a LiDAR or IFSAR DTM. **[TBD]**
- **The upstream catchment still has no usable boundary.** It was delineated on 11 October 2026 and the result was
  thrown out — see *Terrain and catchment* above. The reasoning below is unchanged and is now backed by evidence: Knowing the ground rises to the east is not the same as knowing
  which area drains into the block. In a built township, drains and culverts routinely cross topographic divides, so
  the real contributing area needs flow routing over the drainage network, not terrain slope alone. The 65 mapped
  drains stop at the extent edge and have not been traced beyond it. This is **HY work**, and it is what would turn
  "upstream is east" into an actual boundary. **[TBD]**
- **The Wetland Townpark is still unlocated** and is outside the model extent in any case.
- **Nothing is cadastral.** Lot lines, pond ownership and the legal council boundary are all outside what public
  mapping can give.

## One figure

The interactive model: [claude.ai/artifact/WbjXfctgufzpWse3Zm3FMx](https://claude.ai/artifact/WbjXfctgufzpWse3Zm3FMx)

It carries three selectable ground surfaces — **Trend** (the plane fit, the only part that survives both DEMs),
**Smoothed**, and **Raw** (shown so the noise is not hidden) — with vertical exaggeration applied to the terrain only,
never to buildings.

### Files for the architecture track

In [AR1_site_model/](AR1_site_model/). All are in **metres**, with **X east, Y north, Z up**, origin at the centre of
the extent (3.0900 N, 101.4360 E).

| File | What | Notes |
|---|---|---|
| `terrain.obj` | 41 × 82 ground mesh, smoothed | 1220 × 2450 m. True scale, no exaggeration |
| `buildings.obj` | 633 extruded footprints, grouped and named by type | **Heights are assumed** |
| `water.obj` | 4 water bodies, flat | Level assumed |
| `roads.obj` | 487 centrelines | Centrelines only, **no widths** |
| `drains.obj` | 65 drains and ditches | Position only |
| `council_line.obj` | The Klang / Shah Alam line | Not cadastral |
| `rainready_site.geojson` | Everything in WGS84 | For QGIS, and for the frontend track later |
| `site_model.html` | The viewer, standalone | Same as the link, works offline |
| **Added 11 Oct 2026** | | |
| `terrain_cop30.obj` | The same grid with Copernicus GLO-30 heights | **Alternative, not a replacement.** ~3.7 m below `terrain.obj` |
| `contours_1m.dxf` | 1 m contours, model metres, layer `CONTOUR` | **Use this one** |
| `contours_0p5m.dxf` | 0.5 m contours | Mostly noise at this DEM resolution |
| `sections.png` + `section_A-A_east_west.csv` + `section_B-B_north_south.csv` | Two sections through the block centre, both DEMs | Shows the 3.7 m offset |
| `plan_map_clean.png` | Labelled plan map, 4101 × 2053, 0.60 m/px | **No imagery — free to reuse** |
| `plan_map_imagery.jpg` | The same map on Esri imagery | **Esri terms, reuse not cleared [verify]** |
| `verification/` | The imagery evidence, with its own README on terms | Working evidence, not deck material |
| `gis/` | Split GeoJSON layers, the DEM and derived rasters, and `build_qgis_project.py` | See `gis/build_qgis_project.py` for the QGIS project |

Blender imports `.obj` directly through File › Import. SketchUp needs an importer extension for OBJ **[verify]** —
if that is a problem, the GeoJSON can be converted to DXF or DAE instead. Both Blender and SketchUp import DXF,
so the contours should drop straight in; they are in the same metre grid and origin as the OBJ files, so they
land on top of the model without moving anything.

---

## Sources

- OpenStreetMap via Overpass API, queried 11 October 2026. Contributor data, ODbL. Ways and relations cited by id above.
- SRTM 30 m via Open Topo Data (`api.opentopodata.org`, dataset `srtm30m`), queried 11 October 2026. 3,362 points over
  the model extent, 1,426 over the hydrology extent, plus 7 points re-sampled at AR1's corridor cells.
- [AR1_study_area_selection.md](AR1_study_area_selection.md) for the extent and the earlier 90 m DEM figures.

Added in the AR1c pass, 11 October 2026:

- **Esri World Imagery**, `services.arcgisonline.com`, tiles at zoom 17–19, fetched 11 October 2026. Attribution:
  *Source: Esri, Vantor, Earthstar Geographics, and the GIS User Community*. **Esri terms of use — reuse in the
  deck is not cleared [verify].**
- **Esri Wayback**, `wayback.maptiles.arcgis.com`, releases 2018–2026, used only to bracket the capture date.
- **Copernicus DEM GLO-30**, tile `Copernicus_DSM_COG_10_N03_00_E101_00_DEM`, public AWS mirror, read 11 October
  2026. Free and open; attribution *© DLR e.V. 2010–2014 and © Airbus Defence and Space GmbH … provided under
  COPERNICUS by the European Union and ESA*.
- **OpenStreetMap** via Overpass, second query 11 October 2026: way 888406336 (the main ditch) and the water
  bodies east of the extent. ODbL.
- **Open Topo Data** `srtm30m`, 841 points, re-queried 11 October 2026 for the DEM comparison.
- **FABDEM** was *not* used: `data.bris.ac.uk` returned 503 and the licence is non-commercial.
- **JPS Selangor** `jpsselgis.selangor.gov.my/gis/rest/services` returned HTTP 503 on every attempt, 11 October
  2026. Nothing from it is in this note.
