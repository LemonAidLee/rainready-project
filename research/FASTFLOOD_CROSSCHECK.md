# FastFlood Cross-check of the Screening Model

**Written for:** the team leader and the judges' appendix. **As of:** 21 October 2026.
**Input:** two FastFlood runs in [`../FastFlood Simulation Progress/`](../FastFlood%20Simulation%20Progress/)
(settings `.json`, report `.pdf`, map `.png` for each). **Method of this note:** the reports were read in full; each map
was georeferenced from the bounding box stated in its settings, and the OSM outlines of ponds A and B and our three
spots were drawn on it (script kept in the session scratchpad; it reads `research/AR1_site_model/gis/water.geojson`).

House rule: **the depth maps are not shown on the website or in the deck as depths.** Our terrain error is about 1 m,
which is the size of the depths shown. They are used here only for *where* water collects.

## 1. What the two runs are

| | "Moderate Rain BBR" | "Heavy Rain BBR" |
|---|---|---|
| Model | FastFlood v1.0.20 (Fast Hazard B.V.), run 15 Oct 2026, report 21 Oct 2026 | same |
| Domain | 101.42707–101.45162 E, 3.08142–3.09462 N, **4.01 km²** (BBR core) | 101.41849–101.44991 E, 3.07379–3.10516 N, **12.19 km²** (BBR plus land to the north and south) |
| Grid | "veryhigh" resolution; report states 20 m DEM | "medium" resolution; 20 m DEM |
| Terrain / land cover | Copernicus GLO-30 (FastFlood filter); ESA WorldCover 10 m; ISRIC SoilGrids; **land use and infiltration maps switched on** (`d_lu`, `d_inf`) | same data; land-use and infiltration options **not** switched on |
| Rain | **100-year** design storm, **70.70 mm in 1 h** (GPM IMERG), areal reduction factor 1.084 | **the same 100-year, 70.70 mm in 1 h**, ARF 1.079 |
| Boundary inflow | none | **one inflow, 13.1 m³/s** (GloFAS v4, bias-corrected) |
| Effective runoff coefficient (report) | **0.793** | **0.777** |

**The labels "Moderate" and "Heavy" are misleading.** Both runs use the same 100-year storm. They differ in domain
size, upstream area, an external river inflow and grid resolution, all at once. Rename them by domain ("BBR core"
and "BBR + surroundings") before they go anywhere public.

**An inconsistency in the reports.** Section 1.3 states 70.70 mm over 1 hour; section 2.1 states a spatially
averaged intensity of about 154 mm/h. These do not agree. We do not know which one the solver used. Check the
run in the FastFlood interface **[open]**.

## 2. What agrees with our screening model

| Check | Finding | Conf. |
|---|---|---|
| **Ponds A and B** | The OSM outlines of both ponds sit exactly on FastFlood's two largest areas of pooled water in the core run. This also confirms our georeferencing | H |
| **East–west corridors** | Both runs pool water along the east–west corridor at the north edge of BBR (about y = 340 m in model coordinates, the line of our **shared trunk drain**) and along Persiaran Sungai Keramat south of the ponds | H for what the maps show; M that it reflects the drains rather than the DEM's road embankments |
| **Runoff coefficient** | FastFlood's effective C is 0.78–0.79 for the event. Our MSMA 2 Table 2.5 area-weighted C per zone is 0.63–0.78 today. Same order; ours is lower, as expected for a rational-method C on a simulated town with lawns | M |
| **Spots** | Spot 1 (Jalan Makyong) has pooled water next to it in the larger run (36 % of the pixels within ~60 m), little in the core run. Spot 3 (Persiaran Batu Belah) is at the west edge of pond A's pooled area in both runs (23 % and 65 %). Spot 2 (Jalan Sumazau) has little (5–6 %) | M |
| **Official record** | The only JPS flood record inside our model area (ponding at "Bandar Bukit Raja", 3.0906 N 101.4317 E, in JPS's 2023 and 2024 layers) lies in zone **Z03**, which drains to pond A. FastFlood pools water in the same block | H for the record; M for the match |

## 3. What it does not show, and why we keep our own method

- **Rainfall.** FastFlood's 100-year, 1-hour rain is 70.7 mm (satellite-based, GPM IMERG). MSMA 2's IDF for the
  Telok Gong gauge gives about **114 mm** for 100-year, 1-hour (i = λT^κ/(d+θ)^η with the Table 2.B1 constants).
  Satellite products are known to under-read short, intense tropical storms, and MSMA 2 is the Malaysian design
  standard, so our screening keeps MSMA 2. **Our storm is therefore heavier than FastFlood's.**
- **Depths.** Not used (house rule; terrain error ~1 m).
- **The upstream effect.** The larger run carries more water into BBR, but it changes four things at once (domain,
  upstream land, a 13.1 m³/s river inflow, resolution), so it is **not** a test of upstream development. A clean
  test would be two runs on the same domain and grid, one with the Setia Alam land as today and one with it paved
  (FastFlood lets you draw land-use changes) **[suggested next run]**.
- **Drains and ponds as built.** FastFlood estimates channels from drainage area and OSM streamlines; it does not
  know the trunk drain's size or the ponds' outlets either. It cannot settle our biggest unknown.

## 4. How to use it in the pitch

One line, in the appendix and the About drawer: *"An independent hydrodynamic model (FastFlood, global data, 100-year
storm) pools water in the same ponds and along the same east–west drain corridor that our screening identifies."*
Show the map only without the depth legend and **without the satellite basemap** (the imagery's licence is not
cleared, see [TBD_VERIFY_RESOLUTION.md](TBD_VERIFY_RESOLUTION.md) item 18), or describe it in words. Never quote a
depth from it.

Sources: the two FastFlood reports (Fast Hazard B.V., generated 21 Oct 2026); OSM pond outlines (ODbL); JPS Selangor
GIS layers `Hosted/Laporan_Banjir_2023` and `Hosted/BANJIR_2024`, read 21 Oct 2026.
