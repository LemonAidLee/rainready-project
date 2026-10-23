# Project Status

**As of:** 22 October 2026 · **Phase:** research and planning · **Proposal deadline:** 23 October 2026, 11:59 p.m.

Read [../CLAUDE.md](../CLAUDE.md) first for conventions. The live tracker is the
[RainReady Team Task List](https://docs.google.com/spreadsheets/d/1gMBz5Y6DVhsBYTpGtS3eAw-8-bzyhJkBsQZhWgv-G8s/edit)
Google Sheet; this file holds the things a spreadsheet cannot: why we are here, what is still unknown, and what would sink us.

---

## 1. Where we are

We are entering the competition with **RainReady**. Our reference site is **Bandar Bukit Raja (BBR), Klang**, with
**Setia Alam** upstream in Shah Alam. We picked BBR because it is the only Sime Darby Property township where the problem
is documented, repeated, resident-organised, and already called a priority by the developer itself.

**The concept is [RAINREADY_CONCEPT_V2.md](RAINREADY_CONCEPT_V2.md)** (20 Oct 2026): one shared picture, two doors.
Planners see where storage falls short, residents act in time, and their reports shape the next plan. The problem
statement, users, nine features, video plan, deck outline and the decisions of 20 Oct live there and are not repeated
here.

The whole team is in the **research phase**, with one approved exception: the **3D township is built** (20 Oct 2026),
with **draft drainage zones** and a **screening simulator** that drives it on **sourced MSMA 2 inputs** (21 Oct); the team leader, with
Claude, does and checks the hydrology work (see
[TOWNSHIP_3D_AND_SIMULATOR.md](TOWNSHIP_3D_AND_SIMULATOR.md), "Start here").
The research questions are tracked on the Google Sheet's Research List.

**Design principle:** decision support under uncertainty, not prediction. Risk bands, never predicted flood depths.

---

## 2. What changed from v1

v1 (11 Oct) had four planner-only features: catchment view, retention-pond what-if, responsibility record, street-level
advisories. v2 keeps all four and adds:

- a **resident door**: report and track through existing messaging, and a move-now plan on official warnings;
- from Eujin's HydroShield ideas: the **before-you-build check** and the one-page **Shared Capacity Brief**
  (merge note in [archive/HYDROSHIELD_INTEGRATION.md](archive/HYDROSHIELD_INTEGRATION.md));
- the **loop**: residents' reports appear as pins in the planner view.

The supporting documents in [supporting/](supporting/) were written for v1. Their evidence still holds; where they
describe features or slides, the concept v2 wins.

---

## 4. Decision log

| # | Step | What we found | Decision |
|---|---|---|---|
| 1 | Reviewed an 18-source walkability evidence pack | Car dependence is clear nationally, but the barrier evidence was thin and several summary claims overstated their sources | Walkability is real but only moderately evidenced |
| 2 | Compared candidate themes using online sources only | Flood strongest on evidence; heat and shade strongest on remote demonstrability | Near tie, wide margins |
| 3 | Shaped a shade-prioritisation tool (Teduh / CoolPath) | Precedents exist as planner-facing tools | Developed as a planner decision tool |
| 4 | **Umbrella objection** | A study found a UV parasol gave at least 75% of the street-tree benefit, and many people already use them | Shade concept weakened; set aside |
| 5 | Considered haze | Timely, but the developer cannot act on the cause | Rejected as the project |
| 6 | Township gap analysis | BBR floods at least three times a year; a 583-resident memorandum; the developer calls it a top priority | **Chose flood at BBR** |
| 7 | Feasibility survey | Public data supports screening with stated assumptions, not engineering-grade prediction | Scope limited to tier A |
| 8 | Public-document survey | Many funded projects already exist; over 300 unmanned ponds identified nationally | Reframed as "no shared picture", not "no action" |
| 9 | Restructured the team into four tracks | Earlier five-role split did not match how the work actually divides | Architecture, Hydrology, Frontend and AI, Team leader |
| 10 | Put research before build | The project is still in planning; building first would lock in unverified assumptions | Research List created; tasks follow from it |
| 11 | Merged Eujin's HydroShield ideas (20 Oct) | Inflow-versus-capacity account and pre-build check are strong; the compliance verdict and unsourced figures are not | Took the before-you-build check and the Shared Capacity Brief; dropped verdicts and blame |
| 12 | Concept v2 brainstorm (20 Oct) | Reporting loops already exist elsewhere (Chatham, Riskmap, PetaBencana, KDEB) | Added the resident door; claim only the combination. Six decisions in [concept v2 section 10](RAINREADY_CONCEPT_V2.md#10-decisions-proposed-20-oct-2026-team-to-confirm), **team to confirm** |
| 13 | 3D township base (20 Oct) | The architecture student's sketch aligns with OSM to 0.66 m but covers only the south-east; AR1 holds the flood features | Sketch as base, AR1 flood features on top ([TOWNSHIP_3D_AND_SIMULATOR.md](TOWNSHIP_3D_AND_SIMULATOR.md) 4.4) |
| 14 | Model look (20 Oct) | Ink look read as vague; the look must work live, in stills and in video | **Ghibli-inspired painted style**, palette kept off the risk-band hues (4.6) |
| 15 | Model checked against OSM (20 Oct) | AR1's road layer missed construction and link roads, incl. the West Coast Expressway; drains had culvert gaps | Roads re-fetched; culverts bridged and labelled inferred; AR1 note corrected (4.6a) |
| 16 | Clean simulated town (20 Oct) | Mixed sources looked patchy and undefined | Model is a **simulated township loosely based on BBR**: invented, labelled town layout around the mapped features, building footprint capped to the estimate for real BBR (4.6b) |
| 17 | Elevation between Klang and Shah Alam sides (20 Oct) | Differences of 0.5–1.5 m, below the 3–6 m DEM disagreement; DEMs disagree on direction | No height step shown; the upstream link is shown by flow along the drains |
| 18 | Model area made a rectangle (20 Oct) | The L-shaped outline looked arbitrary | Rectangle x −1,222..1,700, y −830..608 m; water and drains for the new corners fetched from OSM (adds a 4.9 ha retention pond east) |
| 19 | Proxy names in the 3D model (20 Oct) | Simulated town + live dispute; but the real link to SDP's township carries strategic fit and evidence | Model shows **Area A** (Setia Alam side) / **Area B** (BBR side) and Spot 1–3; the deck states the mapping once and evidence slides keep real names ([TOWNSHIP_3D_AND_SIMULATOR.md](TOWNSHIP_3D_AND_SIMULATOR.md) "Start here") |
| 20 | Draft drainage zones (20 Oct) | Terrain routing fails on this plain (AR1); the mapped drains and roads are the only defensible edges | **9 draft zones** cut along mapped lines and grouped by the drain or pond they reach; all ≤ 77.2 ha; **draft, checked by the team leader and Claude** ([TOWNSHIP_3D_AND_SIMULATOR.md](TOWNSHIP_3D_AND_SIMULATOR.md) 4.8) |
| 21 | Screening simulator on placeholders (20 Oct) | No sourced hydrology values yet; the demo still needs to run end to end | Rational Method + volume balance with a **shared trunk drain** (how the upstream change reaches the ponds); 36 placeholders, all flagged; "illustrative values" on every frame (5.5, 5.6) |
| 23 | Inputs sourced by Claude; pond capacity option (a) (21 Oct, team leader) | No sourced hydrology values were available; no public pond capacity exists | MSMA 2 values with confidence per input; storage required is the headline, capacity a planner input. Result depends most on the trunk drain size (L) ([research/HY_screening_inputs.md](../research/HY_screening_inputs.md)) |
| 24 | Website opens on a Malaysia map (21 Oct, team leader) | The planner covers one township; the resident door works anywhere. A national view shows scale, and real coordinates let the map hand over to the planner | **Landing page = night globe of Malaysia** with real JPS Selangor flood records (2017–2024, no depths) and EXAMPLE resident reports; zooming into BBR opens the planner (`#/planner`). [verify] JPS reuse terms. [WEBSITE.md](WEBSITE.md) section 8 |
| 25 | Map nationwide; one meaning per colour (21 Oct, team leader) | Selangor-only dots undersold a national problem; red meant two things in the planner | Map adds JPS 2017 flash-flood locations (town-level, all states, geocoded) and DFO major events 1991–2021 (region centres). Revised: one risk band (room for water) on every area in every preset; change from today shown as ▲/▼ on zone tags, no second colour scale. [verify] DFO terms. [WEBSITE.md](WEBSITE.md) section 8 |
| 27 | Credibility pass (21 Oct, team leader) | The result rested on two L assumptions; no on-site validation was shown | Drain size checked on imagery (no channel ≥ 8 m; pond A short below ~12 m) and storage band against MSMA 2 Ch. 7 (1–3 m; pond A needs ~2.7 m): finding holds, **M**. Site shows ground checks incl. a miss, JPS record pins, maintainers on cards; demo 14 steps from the map. [HY_ASSUMPTIONS_CHECK.md](../research/HY_ASSUMPTIONS_CHECK.md), [WEBSITE.md](WEBSITE.md) section 9 |
| 28 | Responsibility record rebuilt on official rules (21 Oct, team leader) | The record rested on a newspaper paraphrase and read "JPS maintains" from a list that does not say so | Seven lines on Selangor State Assembly answers (1996 Cabinet decision; 2020 handover rule; MMKN 17/2025). Ponds A and B: **not settled (L)**, handover status not public; drains M; 0 of 7 confirmed by the party, the pilot's measure. Site, Brief and deck slides 8 and 13 updated. [RESPONSIBILITY_RECORD.md](../research/RESPONSIBILITY_RECORD.md) |
| 29 | Levers for a built town (21 Oct, team leader) | "BBR and Setia Alam are already built" made the levers read as a design game | Levers renamed for decisions still being made (next parcels upstream, a new retrofit pond, shared drain works); new **Keep it working** levers (pond storage lost, drain blocked) and presets; simulator input `trunk_drain.blockage`, storm held fixed for like-for-like. Report-to-lever link on hold until the resident report function exists. [WEBSITE.md](WEBSITE.md) section 10 |
| 30 | After the water (21 Oct, team leader) | Who answers for flood losses was vague; a High Court held authorities liable for the 2021 Taman Sri Muda flood on 29 Sep 2026 | New page `#/after`: relief vs insurance vs compensation, six stages with sources, BBR duties from the record, the Sri Muda ruling (not final), resident steps. Duty, never blame; not legal advice. Damage record stays with the resident report work. [../research/AFTER_THE_FLOOD.md](../research/AFTER_THE_FLOOD.md), [WEBSITE.md](WEBSITE.md) section 11 |
| 31 | Findings and Recovery pages (21 Oct, team leader) | "Brief" and "After" did not invite a click; both read as walls of text | Renamed **Findings** (*Where the water has nowhere to go*) and **Recovery** (*After a flood: who helps, who pays*); five chapters with a picture each, plain words, full tables folded for engineers. [WEBSITE.md](WEBSITE.md) section 12 |
| 32 | Resident door integrated (21 Oct, team leader) | The teammate's Waterline report system (github.com/yh1127/RainReady) was built separately in its own style | Ported into the site at `#/resident` with its layout kept and the site's fonts, colours and transitions; stages changed to Reported → Checked by association → Sent to [holder] → Cleared (forward, never dispatch); each report routed by zone, council side and the responsibility record; one shared store feeds 3D pins, the Malaysia map and "Test in planner". Satellite image kept with the Esri credit. [WEBSITE.md](WEBSITE.md) section 13 |
| 33 | Platform: any township (22 Oct, team leader) | Restricting the product to BBR did not make it planner software; the lock-in was the site, not the method | Three stages built in one day: site packs and a registry; a general drain-network engine (`network.py`, equal to `screening.py` on BBR) with council-line crossings; **Seri Kembangan – Seri Serdang** generated from open data (19 JPS flood records, 8 crossings Kajang ⇄ Subang Jaya, 5 JPS-listed ponds) in ≈ 3.7 min; 2D site view, register upload, portfolio `#/sites`. AI site-setup assistant skipped; BBR 3D view and demo frozen. Pushed live 22 Oct. [PLATFORM.md](PLATFORM.md) |
| 34 | Sites 3 and 4; every 3D feature in 2D (22 Oct, team leader) | A 2D site lacked the planner's simulation and animation | Added **Kota Kemuning – Bukit Kemuning** and **Padang Jawa – Batu Tiga** (both pass the three tests; Puchong, Subang, Klang South and Rawang built and rejected). The 2D site app now has the planner's presets and levers, storm with rain, downhill flow and cross-council flow lines, pond gauges, build-out hatching, lever pointers, results, Findings and a 12-step guided tour per site. Levers reproduce the generated scenarios exactly. Pushed live 22 Oct (commit `666d72c`). [PLATFORM.md](PLATFORM.md) sections 9–10 |
| 35 | Video story deck (22 Oct, team leader) | The 14-slide presentation read as a deck, ran ~9.5 min with the demo, and repeated what the demo shows | `presentation/index.html` reworked in place into a 13-slide documentary-style story modelled on the team leader's CoreX pitch: cold open (Klang 2021, residents' 3 m as a labelled account), evidence, illustrative persona **Aiman** (developer drainage engineer, labelled not real), the council-crossing animation, the gap, a hand-off to the guided demo, then what's new, who it helps, feasibility, pilot and next, value, close. Timed beats, highlighter and spotlight; voice-over cut to ~390 words for a ~4:50 video. No team on screen (team leader). v1 archived. [VIDEO_GUIDE.md](VIDEO_GUIDE.md) |
| 36 | Story deck restyled (22 Oct, team leader) | The team leader wanted a Vox-style explainer look | Same 13 slides, text, sources, voice-over and timing, restyled as a paper collage: camera pans along one sheet, taped prints, torn clippings, yellow highlighter, red hand-drawn annotations, label boxes; Libre Franklin + Source Serif 4. Dark v2 archived. [../presentation/README.md](../presentation/README.md) |
| 24 | Website style and build (21 Oct, team leader) | The team leader owns the site; the ICQR Magic Tree page is the style reference | Cream paper, toffee accent, isometric diorama, scenario chips; Vite + React + three.js (R3F), static ([WEBSITE.md](WEBSITE.md)) |
| 25 | Website redesign (21 Oct, team leader) | The cream page felt not serious; the team leader chose the OSIRIS console as reference; the scenario panel was confusing | Dark console frame; one control model (upstream development 0–100 %, what-if pond and size, drain size, storm, capacities) with presets; every lever moves something in the model; demo pointers and highlight boxes; larger boundary and labels ([WEBSITE.md](WEBSITE.md) section 6) |
| 26 | Open markers settled (21 Oct, team leader) | JPS Selangor GIS is back online: ponds A and B are on JPS's pond list; official flood records exist at BBR (2023, 2024); Spot 2 was mislabelled as a flood report | Every [TBD] / [verify] sourced or replaced by a stated assumption ([../research/TBD_VERIFY_RESOLUTION.md](../research/TBD_VERIFY_RESOLUTION.md)); FastFlood runs used as an independent cross-check ([../research/FASTFLOOD_CROSSCHECK.md](../research/FASTFLOOD_CROSSCHECK.md)) |
| 22 | Website runs both modes (21 Oct, team leader) | A precomputed view is cheap and ready for 23 Oct; live sliders need the calculation in the browser | **Both**: mode A reads `outputs.json`, mode B runs `screening.ts`; `screening.py` stays the reference, held by a parity check (207 cases pass). Hand-off package in `exports/` ([TOWNSHIP_3D_AND_SIMULATOR.md](TOWNSHIP_3D_AND_SIMULATOR.md) 5.7). Web stack still the frontend track's call |
| 23 | Website zone colours against capacity by default (21 Oct, team leader) | Coloured only by change versus today, the map showed Today as neutral and Area B never red, though the model has the trunk drain over capacity from a 2-year storm and FastFlood and residents point to the same places | **Against capacity by default** (assumed capacities, L), with a "Colour by: Storage shortfall / Change from today" switch; red = storage or conveyance falls short, never a depth. The Brief shows gaps against the assumed capacity and a drain-size sensitivity table. Details in [WEBSITE.md](WEBSITE.md) section 7 |

---

## 5. Who is doing what

| Track | Who | Researching |
|---|---|---|
| Architecture: 3D city | Architecture student | The 3D model of the simulated township, in Blender or SketchUp only |
| Hydrology and physics | Team leader, with Claude (from 22 Oct 2026) | Rainfall to runoff, how upstream development changes downstream flooding, and how to apply flood physics to the 3D model |
| Frontend and AI | The other EE student | The project homepage, and where AI genuinely improves the product rather than decorating it |
| Team leader | You | Documentation, the tracker, the pitch deck, the appendix, integration of all three tracks, and a continuous search for features that would make the product more complete |

Research questions and tasks for each track live on the Google Sheet. Three hand-offs must be agreed between tracks directly
rather than through the team leader: the shared datum and units between the 3D model and the physics grid, the exported
model loading in the website's viewer, and the data contract between the physics and the site.

---

## 6. What exists now

| Artifact | Where | State |
|---|---|---|
| Concept v2 | [RAINREADY_CONCEPT_V2.md](RAINREADY_CONCEPT_V2.md) | Proposal from 20 Oct 2026; decisions in section 10 await team confirmation |
| Pitch deck text and appendix | [FLOOD_PITCH_DECK.md](supporting/FLOOD_PITCH_DECK.md) | v1 draft. **Slides not yet updated to the v2 outline**; appendix still the source list |
| Pitch deck, designed | [Canva](https://www.canva.com/d/lE6MCvrtngd0c4a) | 10 v1 slides; placeholders still visible; not yet updated to v2 |
| Problem validation | [PROBLEM_VALIDATION.md](supporting/PROBLEM_VALIDATION.md) | Complete |
| Live tracker | [Google Sheet](https://docs.google.com/spreadsheets/d/1gMBz5Y6DVhsBYTpGtS3eAw-8-bzyhJkBsQZhWgv-G8s/edit) | Research List, Task List, Summary and README are current |
| Why BBR | [TOWNSHIP_GAP_ANALYSIS.md](supporting/TOWNSHIP_GAP_ANALYSIS.md) | Complete |
| BBR evidence and figures | [BBR_PUBLIC_DOCUMENT_SURVEY.md](supporting/BBR_PUBLIC_DOCUMENT_SURVEY.md) | Complete |
| Data, tools and limits | [FLOOD_FEASIBILITY_SURVEY.md](supporting/FLOOD_FEASIBILITY_SURVEY.md) | Complete |
| Competition requirements | [COMPETITION_HUB.md](supporting/COMPETITION_HUB.md) | Complete |
| 2D teaching playground | [../simulations/rainready-playground/](../simulations/rainready-playground/) | Works; invented terrain and illustrative numbers, for explaining the idea to the team |
| Conceptual runoff tool | [../simulations/upstream-runoff/](../simulations/upstream-runoff/) | Pre-existing; conceptual only |
| BBR site model for the architecture track | [../research/AR1_site_model.md](../research/AR1_site_model.md) and [../research/AR1_site_model/](../research/AR1_site_model/) | Geometry, two ground surfaces, contours, sections, plan maps and a 3D viewer. **Imagery-verified 11 Oct 2026** |
| **3D township (Blender)** | [../simulations/township-3d/](../simulations/township-3d/), how-to in [TOWNSHIP_3D_AND_SIMULATOR.md](TOWNSHIP_3D_AND_SIMULATOR.md) | **Built 20 Oct 2026**: simulated township, Ghibli-inspired look, mapped flood features, invented labelled town fabric. Renders in `renders/` |
| **Draft zones, screening simulator, scene driver** | `plan_zones.py`, `build_zones.py`, `screening.py`, `inputs.json`, `drive_scene.py` in [../simulations/township-3d/](../simulations/township-3d/) | **Built 20 Oct 2026 on placeholder inputs**: 9 draft zones (check map `data/zones_check.png`), three scenarios, 30 s keyframed sequence. Renders `renders/zones_v1_*`, `sim_v1_*` |
| Extra OSM data for the model | `research/AR1_site_model/gis/roads_full_osm.geojson`, `roads_supplement.geojson`, `landuse_osm.geojson`, `water_supplement.geojson`, `drains_supplement.geojson` | Fetched 20 Oct 2026, ODbL |
| **Simulator v2 inputs (sourced)** | [../research/HY_screening_inputs.md](../research/HY_screening_inputs.md), `make_inputs.py`, `landcover.py` | **21 Oct 2026**: MSMA 2 values, H–L confidence per input, sensitivity table |
| **Website** | [../website/](../website/), see [WEBSITE.md](WEBSITE.md); live at https://rainready-wheat.vercel.app | **Built and deployed 21 Oct 2026**: planner view (3D, scenarios, live Adjust), Shared Capacity Brief, resident-door mock-ups |

Nothing else is built. No AI layer, no survey responses.

---

## 7. Open decisions for the team

Name, primary user, resident channel, who pays, higher-ground spots and upstream share were **proposed on 20 Oct** in
[concept v2 section 10](RAINREADY_CONCEPT_V2.md#10-decisions-proposed-20-oct-2026-team-to-confirm) and need the team's
confirmation. Still open beyond those:

1. **Final name check.** RainReady is proposed; check for existing products and trademarks.
2. ~~**Primary user.**~~ Proposed in v2: developer first, residents as the second door.
3. **Which features lead.** v1 suggested the pond what-if and the responsibility record. v2 plans features 1–4 as
   working and the resident door as mock-ups (concept v2 section 4). Confirm.
4. **Whether the existing runoff tool earns a place** in the demo or stays a teaching aid.
5. **Whether a second, non-developer township** should appear as a scalability example. Proposed (21 Oct 2026):
   not before 23 Oct; a 2D-only second site if shortlisted, and a new question: who pays outside developer land
   ([../research/THREE_CHALLENGES_REVIEW.md](../research/THREE_CHALLENGES_REVIEW.md) section 3).
6. **Who presents.** Pitch day on 14 November requires physical attendance.

---

## 8. Must be verified before submitting

**21 Oct 2026: every item below is now settled or replaced by a stated assumption in
[../research/TBD_VERIFY_RESOLUTION.md](../research/TBD_VERIFY_RESOLUTION.md).** Kept here as the record of what was open.

- ~~Year of the managing director's quote~~ **21 Nov 2024** (settled 21 Oct 2026).
- Whether the Taman Mutiara pond was completed after March 2025, and the date and amount in the Selangor Journal report.
- Geographic scope of "over 300 unmanned ponds, about 55 taken over" — Klang or wider.
- Which BBR neighbourhoods the developer actually built; Taman Mutiara and Pekan Meru may not be theirs.
- ~~FABDEM licence terms for a competition submission.~~ **Settled 11 Oct 2026:** non-commercial, and the host
  was down anyway. Copernicus GLO-30 is used instead, which is openly licensed.
- **Esri World Imagery terms** — *21 Oct 2026: largely settled.* Esri's guidance allows static maps and screen captures without permission where the map is not resold or directly monetised, with the credit "Sources: Esri, Maxar, Earthstar Geographics, and the GIS User Community" on or near the map (Esri Canada, "How to cite ArcGIS maps and data"; Esri developer docs, static maps). The resident door's satellite image is such a capture and now carries that credit (M; confirm with Esri before any commercial pilot). Original note: the imagery verification of 11 Oct 2026 used Esri basemap tiles. Looking at them
  is fine; **reusing them in the deck, the viewer or the site is not cleared.** Settle this before submission, or
  use `research/AR1_site_model/plan_map_clean.png`, which carries the same information with no imagery in it.
- data.gov.my licence and rate limits, and whether myPublicInfoBanjir permits any access at all.
- Whether the organisers set a two-to-three-year implementation expectation; this came from the team, not the briefing.
- The MET Malaysia heavy-rain warning tier names used in the playground.
- 3D model: township names on the boundary labels (Bandar Bukit Raja / Setia Alam); how the architecture student built
  the sketch; flood-pin dates and the Persiaran Batu Belah source. The deck must say the town fabric is simulated.
- Remaining pages of the developer's BBR booklet for further pond volumes.

---

## 9. Known weaknesses to have an answer ready for

| Weakness | Our answer |
|---|---|
| Terrain error of about 1 m is the same size as the flood depths | Risk bands only; we never state a depth |
| Three global DEMs now disagree: Copernicus GLO-30 sits 3.7 m below SRTM over the block (11 Oct 2026) | We use direction of fall, never absolute level. A LiDAR or IFSAR DTM is what would settle it, and we say so |
| The OpenStreetMap footprints are incomplete — an estimated 40–60% of the buildings standing in the block | Found by our own imagery check and written down. The model fills the gaps with generic housing and labels it as such |
| We have no catchment boundary. Terrain routing over a 30 m surface model was tried and failed, because the model climbs 8.5 m over the motorway embankment where the main ditch passes under it | We say so plainly rather than show a wrong catchment. The honest claim is the one we can prove from geometry: the drainage network and the council boundary do not coincide |
| No drain network, pond depths or pump rates are public | Assumption ledger; we compute storage *required* from public inputs |
| No site validation is possible before submitting | Back-test against documented flood spots and report the hit rate honestly |
| Government is already acting | We complement, not compete: a township layer beneath the state plan |
| The topic is a live public dispute | Neutral wording throughout; show flow and capacity, never blame |
| Nobody on the team is a hydrologist | Simple published methods, reviewed by a lecturer or mentor |
| An AI layer could undermine our credibility | Guardrails first: grounded on official warnings, no depths, no forecasts, always shows its source |
