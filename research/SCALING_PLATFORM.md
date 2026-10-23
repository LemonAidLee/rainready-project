# From One Township to a Planner Platform: How RainReady Scales

**Written for:** the team leader, and the deck appendix. **As of:** 22 October 2026. **Confidence:** M (the code
audit), L (the ideas in section 3, which nobody has tested yet).
**Builds on:** [THREE_CHALLENGES_REVIEW.md](THREE_CHALLENGES_REVIEW.md) section 3 ("Should we target more towns than
BBR?"), which still stands: **yes in the story, not in the build before 23 Oct.** This note goes one step further. It
asks what would turn RainReady from a BBR demo into planner software that works for any township.
**Status:** written as options; **ideas 1–5, 7, 8 and 10 (in part) were built on 22 Oct 2026** (team leader): see
[../documentation/PLATFORM.md](../documentation/PLATFORM.md). Idea 9 (AI assistant) was skipped; idea 6 (export) is open. House rules apply: risk bands, never depths; no blame.

---

## 1. Answer in five lines

1. The **method already works nationwide**. The simulator reads any set of zones, ponds and inflows from
   `inputs.json`, and the MSMA 2 rainfall curves cover gauges in every state.
2. What ties us to BBR is the **site, not the software**: the hand-built Blender model, hand-checked zones, a network
   shape fixed at one trunk drain and one what-if pond, Selangor's responsibility rules, and BBR text written into the
   website.
3. To scale, separate the **engine** (the same everywhere) from a **site pack** (the data for each place), and make
   each site pack cheap to produce.
4. The real limit is **data, not code**. Drain sizes and as-built pond volumes aren't public. A new site starts on
   stated assumptions until its council or developer adds its own data.
5. The honest market is **urban flash-flood townships** (JPS listed 493 flash-flood locations in 91 towns, 2017), not
   river or tidal floods.

## 2. Where the BBR lock-in sits (code audit, 22 Oct 2026)

| Layer | Bound to BBR? | Detail |
|---|---|---|
| Simulator ([screening.py](../simulations/township-3d/screening.py) / `.ts`) | **No** | It loops over whatever is in `inputs.json`. Its method (MSMA 2 IDF, Rational Method, Qpost ≤ Qpre release, Manning) is national |
| Network shape | **Yes** | Exactly one `trunk_drain` and one `what_if_pond` are built into `run_duration()`. Real catchments branch |
| Storm | **Partly** | One gauge (2913001 Telok Gong), picked by hand. Other gauges are rows in the same MSMA 2 table |
| 3D township (`township.glb`) | **Completely** | Hand-built in Blender; the costliest part to repeat |
| Zones | **Mostly** | `plan_zones.py` cuts along OSM drains and roads; checking against imagery is manual |
| Responsibility record | **Rules yes** | The logic is general; the rules are Selangor's state cabinet decisions |
| Website text | **Yes** | BBR names and evidence written into about 11 source files (Landing, Demo, Brief, Resident, Shell…) |
| National map, resident door, Brief layout | **No** | The map already shows flash-flood records nationwide; the resident door takes any location |

## 3. Ideas, most important first

| # | Idea | What it changes | Mainly helps |
|---|---|---|---|
| 1 | **Site packs.** One folder per place (inputs, zones, boundaries, evidence, text), loaded by name, e.g. `#/site/bbr`. BBR becomes site 1 | Makes it a platform, not a single demo. A second pack, even a rough one, shows this | Innovation, Feasibility |
| 2 | **Build a site automatically from open data.** OSM buildings, roads, drains and land use, plus the Copernicus GLO-30 terrain we already use, give a 2D or simple 3D map with draft zones. Blender stays as the showcase model for BBR | Cuts the cost of a new site from weeks to hours of checking. Generated sites carry a "screening, lower confidence" label | Feasibility, Commercial |
| 3 | **A general water network.** Zones → drains → ponds → river as nodes and links, any number of what-if ponds, nearest rain gauge picked automatically | The method fits real, branching catchments | Impact |
| 4 | **Boundaries as a layer.** Any council, developer, phase or district outline; the tool lists every place where water crosses a line, and the storage shortfall on each side | Our tagline, *"Property lines stop at the fence"*, becomes a feature that works anywhere | Innovation, Strategic fit |
| 5 | **Upload your own data.** Planners upload pond and drain registers (CSV or GeoJSON). Each value keeps its status label (sourced / assumed / planner input) and replaces our assumption | Answers the data limit in line 4 of section 1; confidence rises as owners add data | Feasibility |
| 6 | **Hand-off to engineering tools.** Export a scenario in the input format of a detailed drainage model such as EPA SWMM [verify which tools Malaysian consultants use] | RainReady becomes the shared front door and quick screen that comes before detailed design. It doesn't claim to replace consultants | Feasibility, Commercial |
| 7 | **Portfolio view for a developer.** All of SDP's townships on one map (e.g. Elmina, Serenia City, Bandar Ainsdale [verify which have usable public data]), ranked by storage gap and boundary crossings | Turns one site into a product SDP would use across its estate | Strategic fit, Commercial |
| 8 | **Reports routed by boundary.** A resident report is matched to the right council and drain owner from the boundary layer | The resident door needs no setup per town | Impact |
| 9 | **An AI assistant that sets up new sites.** Given a place name, it gathers the public layers, drafts the site pack and lists every assumption it made for a person to check | Makes AI essential to scaling rather than an add-on (concept feature 9) | Innovation |
| 10 | **Rule sets per state.** The responsibility cascade reads one rule file per state; Selangor is the first | The responsibility record can run outside Selangor | Feasibility |

Ideas 1, 2 and 5 depend on each other: site packs are the format, automatic building fills them, and uploads improve
them.

## 4. Assumptions

- OSM coverage in other townships is about as good as at BBR. At BBR it held only an estimated 40–60 % of
  buildings ([AR1_site_model.md](AR1_site_model.md)). Coverage will vary from town to town, so each site states its own.
- Runoff coefficients can be taken from land use the way they were at BBR
  ([HY_screening_inputs.md](HY_screening_inputs.md)). If not, every generated site needs a hydrology review.
- Terrain error of about 1 m applies everywhere. On flat ground, terrain-traced zones fail (as at BBR, decision 20),
  so zones follow mapped drains and roads instead.

## 5. Limits

- No basis yet for a cost or time per site; **put no figure on a slide**.
- Who pays outside developer land is an open decision ([THREE_CHALLENGES_REVIEW.md](THREE_CHALLENGES_REVIEW.md)
  section 3).
- The method covers flash floods and ponding in developed townships, not river, tidal or pump-failure floods.

## 6. Appendix slide text: "Built to repeat"

> **Deep at BBR, built to repeat.**
>
> - **Same engine, new site pack.** The screening method is MSMA 2, which applies nationwide. Each township is a data
>   folder: zones, ponds, drains, boundaries.
> - **New sites from open data.** OpenStreetMap and Copernicus terrain give a draft site in hours. Owners then upload
>   their pond and drain registers, and confidence rises.
> - **Every boundary, not just one.** Council, developer or phase lines: RainReady shows where water crosses them and
>   which side runs short of storage.
> - **From one township to a portfolio.** A developer sees all its townships ranked by storage gap; councils use the
>   same picture.
> - **The market:** JPS listed 493 flash-flood locations in 91 towns across every state (2017).
> - *Screening, not engineering design. Flash floods and ponding, not river floods. Responsibility rules are
>   Selangor's for now.*
