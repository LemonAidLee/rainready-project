# Resolution of every [TBD] and [verify]

**Written for:** the team leader, and anyone editing the deck, appendix or website. **As of:** 21 October 2026.
**Why:** the team leader asked for every open marker to be settled: sourced where a public source exists, otherwise
replaced by a stated assumption. **Status key:** **Sourced** (a cited document), **Checked** (we tested it
directly), **Assumed** (no public source; a stated assumption with reasoning), **Team** (only the team can supply it).
Confidence **H / M / L**. Where this file and an older document disagree, **this file wins**; the main documents were
updated on the same day (list at the end).

## A. New data found today: JPS Selangor's GIS server is back

`jpsselgis.selangor.gov.my/gis/rest/services` returned HTTP 503 on 11 October 2026. **On 21 October 2026 it answers**
(ArcGIS Server 10.61, public, no login). Only public query endpoints were used; layers marked internal and the
Survey123 layers (which may hold personal data) were not opened. What it settles:

| Layer | What it shows for our site | Conf. |
|---|---|---|
| `AppHydro/Kolam_Fasa_JPS`, layer `kolam_fasa_1` | **Ponds A and B are on JPS Selangor's pond list**, phase 1: **K02** (Persiaran Batu Belah, Bandar Bukit Raja, lot 63232, 12 acres, "kawasan kolam") = pond A (OSM 399570465); **K03** (Persiaran Batu Belah, lots 62804 and 46963, 14 acres, "kawasan kolam takungan") = pond B (OSM 359496461). Surveyed 2 Sep 2011. Matched by the survey coordinates in the attributes (03°05′21.4″ N 101°26′06.1″ E and 03°05′06.2″ N 101°26′06.6″ E), which fall within about 20 m of the OSM pond centroids | H (match); M (that the list means JPS maintains them) |
| `AppHydro/Kolam_Fasa_JPS`, layer `kolam_fasa_4` | Two more ponds in **Taman Mutiara Bukit Raja** (K22, Jalan Mahkota 5, 4 acres; K23, Persiaran Waja, 1 acre), surveyed 27 Jul 2014. East of our model | H |
| `Hosted/Laporan_Banjir_2023`, `Hosted/BANJIR_2024` | **Official flood records:** "Bandar Bukit Raja, Klang", ponding (*genang*), at 3.0906 N 101.4317 E, in both 2023 and 2024; "Taman Mutiara Bukit Raja", ponding (2023, 2024); **"Setia Alam", flash flood (*kilat*), 2024**, at 3.0964 N 101.4460 E, just north of our model on the Shah Alam side | H |
| `Hosted/Banjir_2019`, `Banjir_2020`, `Banjir_2022_Upen` | Nearby 2019–2022 records are outside the model or have a non-rain cause (a burst main at Mutiara Bukit Raja, 5 May 2019) | H |
| `Hosted/Stesen_Hidrologi`, layer "Stesen Rain Fall (RF)" | **Telemetri Telok Gong at 2.9951 N, 101.3679 E**, about 13 km SW of BBR. Nearer JPS gauges exist (Bandar Klang 4.7 km, Pekan Meru 5 km) but have no IDF constants in MSMA 2 Table 2.B1 | H |
| `Kawasan_Tadahan` | River basins only (Sg. Kapar Besar 29,109 ha; Sg. Klang 126,678 ha). The basin line passes through BBR: the pond A block reads as Kapar Besar, Setia Alam as Klang. Far too coarse for a township catchment | M (the service's polygons sit about 280 m west of their survey coordinates, a datum issue, so points near the line are uncertain) |
| `KOLAM_TAKUNGAN_MSMA`, `Parit2022` | Cover Sabak Bernam, Hulu Selangor, Gombak and Kuala Langat only. **Nothing for Klang** | H |

**Caveat for any reuse:** the service's own geometry for the pond and catchment layers is shifted about 280 m west
of the surveyed coordinates (Cassini to WGS84 without a datum shift). Use the attribute coordinates, not the shapes.

## B. Every marker, resolved

### Evidence and the project

| # | Item (where it was marked) | Resolution | Status | Conf. |
|---|---|---|---|---|
| 1 | Year of the SDP managing director's quote (CLAUDE.md, concept v2, deck, problem validation) | **21 November 2024.** Exact words: *"It is quite urgent, and this is a top priority for us,"* Datuk Seri Azmir Merican, at a virtual earnings briefing, on the recurring flash floods in Bandar Bukit Raja ([The Edge, node 734847](https://theedgemalaysia.com/node/734847)). The page gives "Thursday, November 21"; 21 Nov 2024 was a Thursday and the article's image file is dated 2024 | Sourced | M–H |
| 2 | Taman Mutiara pond: completed after March 2025? (status, verify list) | **Not confirmed complete.** Last public reports: 25 % built, completion moved from 28 Oct 2024 to about 6 Mar 2025, JPS reviewing the design and pump capacity ([Utusan, 13 Nov 2024](https://www.utusan.com.my/berita/2024/11/hujan-lebat-luar-biasa-punca-banjir-kilat-di-selangor-semalam/); [Kosmo, 13 Nov 2024](https://www.kosmo.com.my/?p=682021)). No completion report found on 21 Oct 2026. Say "delayed in 2024; completion not publicly reported" | Sourced + Assumed | M |
| 3 | Scope of "over 300 unmanned ponds, about 55 taken over" | **Selangor-wide.** Said by Selangor exco Izham Hashim at MBDK, Klang; about 600 ponds in Selangor, just over 100 under JPS, few under councils ([Sinar Harian, 5 May 2025](https://www.sinarharian.com.my/ampArticle/726836)). **Attribution fix:** this figure is Sinar Harian's; Bernama's report of the same day is the source of "17 projects across 13 hotspots" | Sourced | H |
| 4 | Which BBR neighbourhoods SDP built (Taman Mutiara, Pekan Meru) | Not settled by public sources. **Assumption:** we do not attribute Taman Mutiara Bukit Raja or Pekan Meru to SDP anywhere; we only say "Bandar Bukit Raja, developed by SDP" | Assumed | L |
| 5 | Whether the organisers expect a 2–3 year implementation (deck, verify list) | **Not in the briefing.** COMPETITION_HUB, transcribed from the official slides, sets no timeline. Present our own: *a 12-month pilot in BBR, then other townships* | Checked | H |
| 6 | MET Malaysia warning tier names (playground) | Continuous-rain warnings: **Waspada** (yellow), **Buruk** (orange, > 60 mm in 6 h), **Bahaya** (red, > 150 mm in 24 h); a separate thunderstorm warning (> 20 mm/h for over an hour) ([RTM](https://berita.rtm.gov.my/nasional/senarai-berita-nasional/senarai-artikel/met-malaysia-keluar-amaran-hujan-berterusan-kategori-waspada-hingga-bahaya/) and press summaries of MetMalaysia statements; confirm on met.gov.my before quoting thresholds) | Sourced | M–H |
| 7 | Flood-pin dates and sources; Persiaran Batu Belah (3D doc 4.4, `.glb` extras) | All three come from **one article, [Sinar Harian, 25 May 2024](https://www.sinarharian.com.my/ampArticle/666626)** (residents' council president). **Correction:** only **Jalan Makyong** is reported as flooding ("at least three times a year"). **Jalan Sumazau** is named only as a place for a temporary retention pond; **Persiaran Batu Belah** (with Persiaran Sungai Keramat) for bigger drains. Spot 2 was wrongly labelled "residents report flooding"; fixed on the website. The Blender captions and `.glb` extras still carry the old note **[fix at the next Blender session]** | Sourced | H |
| 8 | Hit rate on documented flood spots (deck appendix) | **1 of 1:** the only official JPS flood record inside the model (2023 and 2024) lies in zone Z03, which drains to pond A. The one resident-reported flood street (Spot 1, Jalan Makyong) is in Z03 too. With the assumed pond capacity (item 22), pond A is over capacity and Z03 is the "high" band; with no capacity entered, bands show change only and this test does not apply. FastFlood also pools water there ([FASTFLOOD_CROSSCHECK.md](FASTFLOOD_CROSSCHECK.md)) | Checked | M (n = 1) |
| 9 | Streets covered by advisories; responsibility coverage (deck appendix) | Streets: **3** mapped streets (Spots 1–3), each tied to its zone and to the official warning links (resident mock-up). Responsibility: **2 of 5** assets in the record have an evidenced agency (ponds A and B, on JPS's pond list); 3 are assigned by rule (item 16) | Checked + Assumed | M |
| 10 | Who pays (concept v2, commercial value) | **Assumption:** SDP funds the BBR pilot from its township flood and sustainability budget (the MD called it "a top priority"); councils and JPS use the shared picture free; later, a per-township licence for developers. To be tested with SDP if shortlisted | Assumed | L |
| 11 | Booklet: remaining pages; Wetland Townpark location | The Wetland Townpark is **60 acres** ([The Edge, 28 Jul–3 Aug 2025](https://theedgemalaysia.com/node/763883)) and adds **over 50,000 m³** of storage ([SDP sustainability page](https://www.simedarbyproperty.com/sustainability/urbanbiodiversity/spotlight-bandar-bukit-raja.html)). No public source places it on a map. **Assumption:** it lies outside our model, and its design volumes are not used in the screening | Sourced + Assumed | M |
| 12 | Team names, video link, survey responses, reviewing lecturer | **Team.** Prototype link is now known: **https://rainready-wheat.vercel.app**. The rest only the team can fill | Team | — |

### Data, licences and access

| # | Item | Resolution | Status | Conf. |
|---|---|---|---|---|
| 13 | JPS Selangor GIS 503: permanent or transient? (problem validation, AR1) | **Transient.** Up on 21 Oct 2026; findings in part A | Checked | H |
| 14 | PISMA "Klang and Petaling" 2026: started, scope? | No public report of it found on 21 Oct 2026. The latest Klang study found is the **Klang District Stormwater Master Plan (2009)**; JPS said in Sep 2026 that MSMA itself is under full review. **Assumption:** the 2026 study is not yet published; RainReady would feed it, not replace it | Sourced + Assumed | M |
| 15 | Is BBR in the "no man's land" Fasa 1 exercise? | The dashboard's data is not public (HTTP 403). **But ponds A and B are on JPS's own pond list (part A), so they are not "unowned" ponds.** Whether any BBR drain is in Fasa 1 remains unknown; assume not stated | Checked + Assumed | M |
| 16 | **Superseded 21 Oct 2026 by [RESPONSIBILITY_RECORD.md](RESPONSIBILITY_RECORD.md)** (official State Assembly rules). Drain owners: "KDEB if ≤ 1.5 m, other agency if wider" (3D doc 4.7) | KDEB Waste Management says its drain cleaning covers drains "under 1.5 m" (reports differ on width vs depth). **Selangor rule (Sep 2025):** unowned drains that run to rivers are maintained by **JPS**, those that run to monsoon drains by the **council** ([Utusan, 4 Sep 2025](https://www.utusan.com.my/berita/2025/09/banjir-selangor-teruskan-selenggara-500km-longkang-tak-bertuan/)). **Assumption for the record:** small drains: MBDK (cleaning by KDEBWM); shared trunk drain: MBDK; main ditch (runs to Sungai Puloh / Kapar): JPS Selangor; council-line crossing drain: MBSA upstream of the line, MBDK below it | Sourced + Assumed | L–M |
| 17 | data.gov.my licence and rate limits | **Rate limit: 4 requests per minute per API family** (HTTP 429 beyond) ([developer.data.gov.my](https://developer.data.gov.my/rate-limit)). No licence page found. **Decision:** RainReady's mock-up only links out to official warnings; it calls no API, so the licence does not block the submission | Sourced + Assumed | M |
| 18 | Esri World Imagery in the deck, viewer or site; FastFlood maps on imagery | **Not cleared.** World Imagery is under the Esri Master License Agreement with attribution required, and is not an open licence. **Decision:** no Esri or other satellite tiles in anything public; use `plan_map_clean.png`, our own renders, or a FastFlood map exported **without** the basemap | Sourced | H |
| 19 | myPublicInfoBanjir access | **Decision:** link only, no scraping. The site and mock-ups link to Public Infobanjir and METMalaysia | Assumed | — |
| 20 | Asset licences for imported 3D assets (Sketchfab) | None recorded as imported: the model uses its own geometry plus OSM data. If the architecture student imports any asset, record its licence | Checked (records) | M |
| 21 | Area A township name (3D doc labels) | **Setia Alam confirmed:** OSM reverse geocoding at 3.095 N 101.448 E returns *Seksyen U13, Shah Alam*, the section Setia Alam occupies; JPS 2024 also logs a flash flood named "Setia Alam" at 3.0964 N 101.4460 E. Klang side: Bandar Bukit Raja | Sourced | H |

### Hydrology inputs (all values now sourced or stated)

| # | Item | Resolution | Status | Conf. |
|---|---|---|---|---|
| 22 | **Pond A and B capacity** (3D doc 5.2, `.glb` `stated_capacity_m3: TBD`) | No public figure. **Assumption, offered as a preset only ("Assumed pond capacity"), never the default:** mapped water area × **1.5 m** of live storage above the normal water level: pond A 55,611 m² → **83,400 m³**; pond B 57,255 m² → **85,900 m³**. Why 1.5 m: residents called the ponds "shallow" in 2024; the model's visual basin is 2.5 m; no MSMA or JPS depth for these ponds was found. JPS's lot areas (12 and 14 acres) include banks and are not used | Assumed | L |
| 23 | Rainfall IDF station location (HY inputs, `inputs.json`) | **2.9951 N, 101.3679 E** (JPS station layer), ~13 km SW; nearest gauge with Table 2.B1 constants | Checked | H (location) / M (that it is gauge 2913001) |
| 24 | Rational Method form and limits (3D doc 5.1, HY request) | **Q = C·i·A/360**, not for catchments **> 80 ha**, nor for designing storage (MSMA 2, Eq. 2.3 and 2.3.1.2); all zones ≤ 77.2 ha. Already in [HY_screening_inputs.md](HY_screening_inputs.md) | Sourced | H |
| 25 | Hydrograph shape (3D doc 5.1) | Rational Hydrograph Method, V = Q·d (MSMA 2 2.3.2) | Sourced | H |
| 26 | Band thresholds (3D doc 5.1) | Change vs today: medium ≥ 1.05, high ≥ 1.20; vs capacity: 0.8 / 1.0 (team choice, in `inputs.json`) | Assumed | L |
| 27 | Outlet capacity (3D doc 5.2) | Ponds release at most the pre-development peak (MSMA 1.2.1, Qpost ≤ Qpre, C 0.40) and only into room left in the trunk drain (Manning, n 0.018) | Sourced rule + Assumed section | M / L |
| 28 | Shared trunk drain section | **6 m top, 3 m bottom, 2 m deep** concrete trapezoid, slope 0.0013 (stated assumption, L). The biggest lever; a slider on the site (3–14 m). The one measurement worth asking a council for | Assumed | L |
| 29 | Upstream area beyond the edge (`EXT_A`) | **50 ha** test value (slider 0–300 ha). JPS's catchment layer is river-basin scale only (part A), so no official sub-catchment exists in public data | Assumed | L |
| 30 | Z05 outlet: trunk drain or pond B? | **Assumption: trunk drain** (via the Jalan Meru drain), as modelled. If it drains to pond B, pond B's need rises by Z05's volume | Assumed | L |
| 31 | Z06 route to pond A | **Assumption:** north to the Sungai Keramat drain, then pond A (no internal drain is mapped). If part of it reaches pond B instead, pond A's need falls and pond B's rises by that share | Assumed | L |
| 32 | Z09 outlet | **Assumption:** leaves the model to the east (drains along Persiaran Astana run east); shown as "outlet unknown" | Assumed | L |
| 33 | OSM way direction read as flow direction | Assumed true for every drain (usual OSM practice for waterways); the site says so on every card | Assumed | M |
| 34 | Add the 4.9 ha pond OSM 721223351 as pond C? | **No** for 23 Oct: it serves Z08, which drains to the trunk drain in our draft; adding it needs a routing decision not yet made | Assumed | — |
| 35 | Deck appendix rows "pond depth, design storm, runoff C" | Design storm **100-year, 3-hour, 49.6 mm/h** (Telok Gong); C **0.63–0.78 per zone** (MSMA 2 Table 2.5 over the model's land cover); pond depth: not public, see item 22 | Sourced | H / M |

### Model and team items

| # | Item | Resolution | Status |
|---|---|---|---|
| 36 | How the architecture student built the sketch | **Team** (ask the student). Evidence so far: it matches OSM footprints to 0.66 m, so it is almost certainly OSM-based (M) | Team |
| 37 | SketchUp OBJ import (AR1) | Moot: the architecture track works in Blender (decision of 20 Oct 2026) | Checked |
| 38 | A LiDAR or IFSAR DTM; a usable upstream catchment boundary (AR1) | Not publicly available (JPS layer is river-basin scale). Stays a stated limitation | Checked |
| 39 | `water_tasik_setia_alam` keeps its real name in the `.glb`; whether the site lists object names | The site never lists object names, so the name is not shown. Keep | Checked |

## C. Documents updated on 21 Oct 2026 to match

CLAUDE.md (key evidence), [PROJECT_STATUS.md](../documentation/PROJECT_STATUS.md) (sections 4 and 8),
[TOWNSHIP_3D_AND_SIMULATOR.md](../documentation/TOWNSHIP_3D_AND_SIMULATOR.md) (labels, pins, drain owners),
[HY_screening_inputs.md](HY_screening_inputs.md) (station, section 7),
[PROBLEM_VALIDATION.md](../documentation/supporting/PROBLEM_VALIDATION.md) and
[FLOOD_PITCH_DECK.md](../documentation/supporting/FLOOD_PITCH_DECK.md) (markers), the website (Spot labels, evidence
ticker, Brief owners, assumed-capacity preset) and `make_inputs.py` (station note). Markers left in other files are
superseded by this table.
