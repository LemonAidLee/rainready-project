# Imagery used to verify the site model, 11 October 2026

Working evidence for the *Imagery verification* section of
[../../AR1_site_model.md](../../AR1_site_model.md). Red, magenta and yellow lines are OpenStreetMap geometry drawn
on top by us; everything underneath is the basemap.

## Source and terms — read before reusing any of this

| | |
|---|---|
| Layer | **Esri World Imagery**, `services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer` |
| Fetched | 11 October 2026, zoom 17–19 (0.60–0.15 m per pixel) |
| Attribution the service publishes | *Source: Esri, Vantor, Earthstar Geographics, and the GIS User Community* |
| Capture date | Not published per tile. The tile over pond A is byte-identical to the Esri **Wayback release of 24 September 2026** and differs from the release of 18 December 2025, so the image was taken somewhere between about December 2025 and September 2026 |
| Licence | **Esri terms of use — not an open licence.** These files are kept as working evidence. **Do not put them in the deck, the viewer, the website or anything public until the terms have been checked.** [verify] |
| Geometry overlaid | OpenStreetMap contributors, **ODbL** — that part is free to reuse with attribution |

If the Esri terms do not allow reuse, the fallback already exists:
[../plan_map_clean.png](../plan_map_clean.png) carries the same information with no imagery in it.

## The files

| File | What it shows | Check |
|---|---|---|
| `pondA_399570465_z18.png` | Pond A with its OSM outline | 1 |
| `pondB_359496461_z18.png` | Pond B with its OSM outline | 2 |
| `basin_z18.png` | The 216 m² basin — scrub and bare ground, no water | 3 |
| `pondA_timeseries.png` | Pond A in the 2018, 2022 and 2026 Wayback releases — water throughout; the housing on its south bank arrived between 2018 and 2022 | 1 |
| `council_corner_z18.png` | The council line (magenta), drains (blue) and the basin (yellow) at the north-east corner | 5 |
| `ditchW3_z19.png` | The main ditch as a concrete-lined trapezoidal channel, about 8–10 m top width, at 3.0976 N 101.4337 E | 6 |
| `coverage_overview_z17.png` | The whole block with every mapped building outlined — the unmapped estates in the west and north-west are the point of this one | 7 |
| `s1_NWterrace_z19.png` | North-west terraces: roughly 80–110 houses standing, **zero** mapped | 7 |
| `s3_Emapped_z19.png` | East sample: 88 polygons, about 90% of visible units mapped | 7 |
| `east_ponds_z17.png` | The water bodies east of the extent — detention basins and a treatment works, none of them a landscaped wetland park | 9 |

Check numbers refer to the nine-row table in `AR1_site_model.md`.

## Added 21 October 2026: trunk drain width check

Same source and terms as above (Esri World Imagery, zoom 19, 0.298 m per pixel, fetched 21 Oct 2026); made with
`trunk_drain_imagery.py`. Yellow = the OSM ditch chain of the shared trunk drain; white bar = 20 m with 1 m ticks.
Findings in [../../HY_ASSUMPTIONS_CHECK.md](../../HY_ASSUMPTIONS_CHECK.md) section 1.

| File | Where | What it shows |
|---|---|---|
| `trunk_drain_p1_z19.jpg` | 3.0930 N 101.4290 E | Grassed reserve beside the road; a narrow dark channel line, about 1 m |
| `trunk_drain_p2_z19.jpg` | 3.0928 N 101.4320 E | Narrow channel at the back of the terraces; a grass strip about 15 m wide to the road |
| `trunk_drain_p3_z19.jpg`, `trunk_drain_p3_zoom.jpg` | 3.0929 N 101.4352 E | Two mapped lines either side of the road; a dark water strip about 2 m wide in grass |
| `trunk_drain_p4_z19.jpg` | 3.0925 N 101.4395 E | Line under a tree-covered strip by the road; channel not visible |
| `trunk_drain_p5_z19.jpg` | 3.0930 N 101.4428 E | Runs under the highway ramps near the council corner |

