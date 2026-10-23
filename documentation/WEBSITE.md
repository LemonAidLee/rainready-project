# RainReady Website: Style, Structure and Build

**Written for:** the team leader and the next Claude session. **As of:** 21 October 2026.
**Builds on:** [RAINREADY_CONCEPT_V2.md](RAINREADY_CONCEPT_V2.md) section 4 (features), and
[TOWNSHIP_3D_AND_SIMULATOR.md](TOWNSHIP_3D_AND_SIMULATOR.md) 5.7 (the `.glb` hand-off and the two modes).
**Decision (team leader, 21 Oct 2026):** the team leader owns the website, and Claude implements it. The style is
modelled on the ICQR "Magic Tree" page (tree.icqr.com). The approval to implement extends the 20 Oct exception
(3D township and simulator) to the website.

House rules apply on every screen: risk bands, never depths · advisory, never forecast · scenario differences,
never attributions · "illustrative values" whenever an input is still a placeholder.

## 1. Style (first version, superseded by the console redesign in section 6)

**Reference read on 21 Oct 2026:** an isometric 3D diorama on a plinth, alone on a warm paper-cream page, with a lot of
empty space. Controls sit at the bottom: a translucent input, a single toffee action button, and a segmented row of
three soft chips (Spring / Summer / Autumn) plus an icon chip. A small yellow pill sits under the logo, and an ⓘ in the
top-right corner. The type is the system UI font, small and medium-weight; icons are thin line icons. The tone is
quiet, friendly and handmade, not dashboard-like.

**Why it fits RainReady:** the cream ground is calm and neutral (the topic is a live dispute), and it makes the
saturated risk bands the only loud colour on screen. The season chips map one-to-one onto the scenario switch. The
yellow pill becomes the "illustrative values" label. The ⓘ becomes "About these numbers": method, sources,
assumptions, limits.

### Tokens

Taken from the reference's computed styles (21 Oct 2026), plus RainReady's own band colours:

| Token | Value | Use |
|---|---|---|
| `--paper` | `#F6F1E7` | Page background |
| `--ink` | `#3F352B` | Main text |
| `--ink-2` | `#5F4E3D` | Secondary text, inactive chips |
| `--surface` | `rgba(255,250,242,.90)` | Inputs, cards |
| `--chip` | `rgba(253,247,238,.78)` | Inactive chip |
| `--chip-on` | `rgba(238,227,209,.95)` | Active chip |
| `--line` | `rgba(156,140,119,.26)` | 1 px borders |
| `--accent` | `#C07A3A` | The one action colour (toffee); shadow `0 1px 0 rgba(123,77,38,.25)` |
| `--pill` | `#F5C542` | Small label pill ("illustrative values") |
| `--band-low` / `--band-med` / `--band-high` / `--band-unknown` | `#2E9B5F` / `#E6A21B` / `#D2452F` / `#A59A8C` | Zone bands: saturated so they stand apart from the cream and the sage ground. Water stays the only blue (`#3D8FD6`) |
| Radius | 12 px (inputs, buttons), 11 px (chips), 16 px (cards) | — |
| Type | `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`; 12 px chips (500, active 600), 14–16 px body, 22–28 px headings (650) | Same as the reference |
| Icons | Lucide line icons | Same family as the reference |

**3D:** an orthographic, isometric-style camera (the reference's diorama look) on the existing plinth. Drag to rotate
within limits, scroll or pinch to zoom, no free fly. Soft sun and sky light on the exported `web_*` palette. The scene
keeps the Ghibli palette; the page frame supplies the reference's cream tone.

## 2. Structure

| Screen | Concept feature | What it shows | State for 23 Oct |
|---|---|---|---|
| **Planner view** (home) | 1, 2, 3 | The township; bottom chips **Today / Upstream change / + What-if pond**; a rain chip; tap a zone or pond for a card (area, where it drains, band, storage required, sources). **Adjust** drawer with sliders (rainfall, upstream paving, what-if pond size) recomputed live with `screening.ts` (mode B) | Working |
| **Shared Capacity Brief** | 4, 7 | One printable page: storage required per pond for each scenario, the gap against a planner-entered capacity, assumptions, sources, confidence, owners (TBD) | Working, generated from the same results |
| **Resident door** | 5, 6 | A chat-style report flow and a move-now card that links to the official warning. Phone frame, sample data marked "example" | Clickable mock-up |
| **About these numbers** (ⓘ) | — | Method, every input with its source and status, what is not shown (depths, times, verdicts) | Working |

## 3. Build

| Item | Choice | Why |
|---|---|---|
| Framework | **Vite + React 18 + TypeScript** | A static single-page site: no server needed, so it deploys anywhere (Vercel, Netlify, GitHub Pages). React keeps the four screens and the cards manageable |
| 3D | **three.js r169 via React Three Fiber 8 + drei 9** | The `.glb` loads as tested on 21 Oct (GLTFLoader + Draco, trees instanced). This was Eujin's suggestion, minus Next.js, which a static site does not need |
| Simulator | `simulations/township-3d/screening.ts`, imported directly | Mode B. It must keep passing `check_parity.ts` against `screening.py` |
| Data | `exports/township.glb`, `trees.json`, `inputs.json`, `outputs.json`, copied into the site's `public/` by a script | One source of truth: the simulator folder |
| Code | [`../website/`](../website/) | — |

**Deploying the site publishes it.** The team leader confirms before the first public deploy.

## 4. As built (21 Oct 2026)

**Run it:** `cd website` → `npm install` (once) → `npm run dev` (local, with hot reload) or `npm run build` (static site
in `website/dist/`, deployable as-is). Both first run `scripts/sync-data.mjs`, which copies `township.glb`,
`trees.json`, `inputs.json` and `outputs.json` from `simulations/township-3d/exports/`, writes a slim `zones_meta.json`
(ids, areas, routes; the full `zones.json` is 4.5 MB), copies `screening.ts` and three's Draco decoder. **After any
model or simulator change:** re-run `export_glb.py` in Blender, then rebuild the site.

| Part | File | What it does |
|---|---|---|
| Data, modes | `src/lib/data.ts` | Mode A: `outputs.json`. Mode B: any Adjust change re-runs `screening.ts` in the browser on a copy of the inputs |
| 3D | `src/scene/Township.tsx`, `Rain.tsx` | Loads the `.glb` (Draco); merges ~1,500 static meshes by material into a few dozen draw groups; draws 5,007 trees by instancing; zone colours, pond gauges, upstream blocks (morph target `built`), what-if pond and moving flow chevrons follow the results; tap a zone or pond for its card |
| Planner UI | `src/ui/Planner.tsx` | Top bar with the status pill, scenario dock (Today / Upstream change / + What-if pond, storm, Adjust), legend, cards, Adjust panel (drain width, upstream area and C, what-if pond size, stated capacities), "About these numbers" drawer with every input, its status, confidence and source |
| Brief | `src/ui/Brief.tsx` (`#/brief`) | Printable Shared Capacity Brief from the same results, including the responsibility record (owners [TBD]) |
| Resident door | `src/ui/Resident.tsx` (`#/resident`) | Two clickable phone mock-ups, marked EXAMPLE: report through chat; move-now plan linking to **Public Infobanjir (JPS)** and **METMalaysia** (both checked live on 21 Oct 2026) |

**Checked 21 Oct 2026 (Chromium via Playwright):** desktop 1600 × 900 and phone 390 × 844. The production build loads
with **0 console errors or warnings**. Scenarios, zone and pond cards, live recompute (a 10 m drain gives pond A
+11 % with the upstream change, as the sensitivity table predicts), Brief (follows the adjusted inputs) and the
resident flows all work. Bundle: 308 kB gzip JavaScript plus the 3.5 MB model.

**Deployed 21 Oct 2026 (team leader's request):** **https://rainready-wheat.vercel.app** (public; checked without a
login). Code: private GitHub repo **LemonAidLee/rainready-website** (branch `main`), linked to the Vercel project
`rainready`, so **every push to `main` redeploys**. The repo is the `website/` folder only; the synced data
(`public/data`, `src/sim/screening.ts`, `public/draco`) is committed, so Vercel builds it standalone (checked with a
fresh clone). **To update the live site:** re-run `export_glb.py` if the model or results changed → `npm run sync`
in `website/` → commit → `git push`. Share only the short address: per-deployment URLs sit behind Vercel's login.

## 5. Guided demo (21 Oct 2026)

For live presentations and for recording the video. Open it with the **Guided demo** button (top right) or the
address **`https://rainready-wheat.vercel.app/#/demo`**. Code: [`../website/src/ui/Demo.tsx`](../website/src/ui/Demo.tsx)
(the steps) and `App.tsx` (what each step sets). Every number in a caption is **read live from the simulator results**,
so the narration always matches the model; if the inputs change, the captions change with them.

| # | Step | What the screen does | Auto time |
|---|---|---|---|
| 1 | One shared picture | Overview, clear day; states the Area A / Area B mapping and what is mapped vs invented | 9 s |
| 2 | Property lines stop at the fence | Glides to the council corner: the boundary and the one crossing drain | 9 s |
| 3 | Where residents say it floods | Spots 1–3 (Spots 1–2 reported flooding; Spot 3 a drain request) | 9 s |
| 4 | A 100-year design storm | Rain and flow arrows start; MSMA 2 storm and gauge; what red means (over assumed capacity, not a depth) | 11 s |
| 5 | Today: how much the ponds must hold | Ponds A and B, Pond A card: storage required, trunk drain load, pond A short against the assumed capacity | 12 s |
| 6 | Scenario: more paved land upstream | Glides to Area A; upstream blocks rise | 9 s |
| 7 | The shared drain carries more | Overview; trunk-drain zones turn amber; says pond storage stays the same while the drain is full; "difference, not blame" | 11 s |
| 8 | What if a pond is added? | What-if pond appears; its card; storage cut | 10 s |
| 9 | The biggest unknown | Adjust panel opens with a 10 m drain; the result moves live | 11 s |
| 10 | The Shared Capacity Brief | Switches to the Brief, scrolls to the storage table | 9 s |
| 11 | The resident door | Switches to the resident mock-ups | 10 s |
| 12 | Close | Back to the overview; tagline | 9 s |

About 2 minutes in total on autoplay. **Controls:** Back / Play-Pause / Next / Clean frame / Exit, or keys **→ or
Space** next, **←** back, **P** play-pause, **H** clean frame, **Esc** exit. During the demo the camera is driven by
the steps; exit to explore freely.

**Recording the video (hands-free):** open **`https://rainready-wheat.vercel.app/#/demo?play&clean`** in a full-screen
browser window (F11), at 1920 × 1080 for a crisp capture. `play` starts autoplay and `clean` hides the controls and the
cursor, leaving the caption and the status label (which must stay on screen). Start the screen recorder, reload the
page, and stop after step 12. To narrate over it, keep `clean` and drop `play`, then press → at your own pace. Each
step's text doubles as a voice-over script.

**Not done yet:** an AI "explain this result"
(concept feature 9, optional); report pins in the planner view (mock-up only).

## 6. Console redesign (21 Oct 2026, team leader)

**Why:** the cream page read as not serious enough. The team leader supplied a new reference, the **OSIRIS** OSINT
console: near-black ground, thin icon rails, a live status bar, monospace instrument readouts, an evidence ticker.
They also found the old scenario panel confusing, wanted every assumption change to show in the model, wanted
visual pointers in the guided demo, and found the boundary and the spot names too small.

### Style tokens (`src/styles.css`)

| Token | Value | Use |
|---|---|---|
| `--bg` | `#060b11` | Night-water ground, with a faint 26 px survey-dot grid behind the model |
| `--panel` | `rgba(9,16,23,.86)` + 10 px blur | Panels; 1 px `--line` borders, 4 px radius |
| `--text` / `-2` / `-3` | `#d6e1eb` / `#9aabbb` / `#627485` | Text levels |
| `--gold` | `#e3b341` | Brand mark, "look here" (demo boxes and pointers), changed values |
| `--cyan` | `#35d0e6` | Water and live data; sliders |
| Bands | `#1fbf75` / `#f2a516` / `#ff4a3d` / `#6b7785` | Low / medium / high / unknown |
| Type | **IBM Plex Sans** (reading), **Plex Sans Condensed** (headings), **Plex Mono** (readouts, labels) | Google Fonts |

### Layout

| Area | What it holds |
|---|---|
| Status bar (top) | Wordmark; context line; live readouts (storm, scenario, trunk-drain load); status pill (**Screening estimate · MSMA 2**, or **Your what-if** in gold once any sourced input is changed); Guided demo |
| Rail (left) | Planner · Scenario · Layers · Brief · Residents · Demo · About |
| Scenario control (left panel) | **Presets** (Today; Upstream built out; Built out + pond; Main-ditch-size drain; Large upstream catchment; 10-year storm; Assumed pond capacity), then five levers, each with a **"Watch:"** line naming what it moves in the model |
| Results (right) | Pond A and B storage required with change vs today and a bar (marker = today, or the entered capacity), trunk-drain load against its assumed capacity, what-if pond held |
| Bottom | View bar (3D / Top / reset; Clear / Storm; "Changed: …"), cursor readout (lat/lon and zone under the pointer), band legend, evidence ticker (every item sourced) |

### One control model (replaces Today / Upstream / + Pond chips)

The screen always shows **"these settings, compared with today's land cover under the same storm and drain"**:

| Lever | Range | Visible change in the model |
|---|---|---|
| Upstream development | 0–100 % (C interpolated linearly from today to the full change in `inputs.json`) | Invented blocks rise on open land in Area A (morph weight = level); blocks fill the **"Area A beyond the model edge"** footprint north of the model |
| Area beyond the edge | 0–300 ha | The footprint resizes (side = √area) |
| Runoff C when built | 0.65–0.95 | Results only |
| What-if pond | on/off, 5,000–60,000 m³ | The pond appears in Z06 and its footprint scales with √(size / 25,000) |
| Shared trunk drain | 3–14 m top width | The drain ribbon widens (drawn 2.5× for visibility); in the storm its colour is its load (cyan, amber ≥ 80 %, red ≥ 100 %) and the chevrons speed up |
| Design storm | 2–100 yr | Rain opacity follows intensity; every result is re-run |
| Stated capacity | number, or the assumed one | Pond gauges switch to share of capacity; zones to capacity bands |

Every change also flashes a **pointer** (ring, beam, numbered callout) on the part of the model it moves, for 2.6 s.
All levers only change inputs; `screening.ts` and its parity with `screening.py` are untouched.

### Model on the site

- **Boundary:** a 130 m light curtain with a scan line along the OSM council line (`exports/overlays.json`, written
  by `simulations/township-3d/export_web_overlays.py`), a 12 m ground band, and **KLANG / SHAH ALAM** tags when
  zoomed in. The `.glb`'s 14 m curtain is hidden.
- **Labels** are HTML at a fixed screen size (areas 26 px, spots 20 px, ponds, zones, drain). Level of detail: at
  overview only areas, spots and ponds; zone chips in the storm; drain and council tags once zoomed in. The `.glb`'s
  3D text tags are removed. Spot notes follow the source (Spot 1 flooding; Spot 2 pond request; Spot 3 drain request).
- **Why the web model has less detail than Blender (team leader's question):** expected. The Blender look is made by
  node shaders (cel steps, painted noise, tinted shadows, sky, inverted-hull outlines) that glTF cannot carry, so
  `export_glb.py` swaps in flat `web_*` colours, and the site merges ~1,500 meshes for speed. The site now adds back
  what a browser can do cheaply: **cast shadows** (4096 px map, sun from the south-west at about 26° so shadows face
  the camera), a **procedural window grid** on walls (fades out below a few pixels per bay so it never shimmers) and
  **building outlines** that fade in when zoomed. Matching Blender exactly would need baked textures, a larger file
  and a heavier page.

### Guided demo pointers

Each step can name **points** in the model (anchor keys such as `label_spot_1`, `pond_A`, or `crossing`, `trunk`,
`ext`) and **UI targets** (`data-spot` selectors). Points get a gold ring, beam and numbered callout; UI targets get a
pulsing gold box with a label, scrolled into view inside their panel. Steps 6, 8 and 9 open Scenario control on the
lever being explained.

**Moving black-water backdrop (team leader, 21 Oct 2026; reference kvs.services):** `src/scene/WaterBackdrop.tsx`, a
full-screen fragment shader (perspective water plane, slow swells, fine ripples, cool glints) on its own canvas
behind the model, at half resolution and about 30 fps; a still frame under reduced motion. The presentation deck
(`../presentation/`) uses the same shader.

**Checked 21 Oct 2026 (Chrome DevTools, 1600 × 900 and 500 × 844):** production build passes (325 kB gzip JS); no
console errors; presets, levers, flash pointers, demo steps 1–10 and the Brief render as described.

## 7. Fixes after the status check (21 Oct 2026, team leader)

A check of features 1–4 found three problems. All three are fixed in the local build; the simulator and its parity
with `screening.py` are untouched.

| Problem | Cause | Fix |
|---|---|---|
| The upstream change does not move pond storage (A and B "no change"; gaps identical) | On the assumed 6 m trunk drain the drain is already at 101 % today, so the ponds get 0 % of their allowed release in both scenarios. The extra upstream water shows up in the drain (+10 %), not in the ponds. A model result, not a bug | **Brief:** new section "What the upstream change does depends on the shared drain", re-running the same inputs at 6 m (as assumed), 10 m and 14 m. At 10 m the upstream change raises both ponds' storage by 11 %, at 14 m by 15 %. **Planner:** the pond rows say "releases nothing: the shared drain has no room". **Demo step 7** says why pond storage stays the same |
| The Brief's gap column was empty by default | No stated capacity is public | Gaps now use the assumed capacity (mapped water area × 1.5 m: A 83,400 m³, B 85,900 m³, **L**) until a planner enters one, and the Brief names which capacity it used. The planner view is unchanged: it still claims no capacity by default |
| Labels cramped at the default view | Spot tags centred on close anchors; the fit (2,900 m) put the model's east edge under the results panel | Fit widened to 3,250 m; Spot 1 leans west, Spot 3 east and higher (`--ax`, `--lift`); the east-edge tags grow west; Area B moved to the model's south-west edge, clear of pond B's tag; the beyond-the-edge tag is hidden on phones |

**[open]:** confirm that ponds releasing nothing into a full trunk drain is the intended
behaviour, and whether 6 m is still the best stated size. The upstream story depends on it.

**Deployed 21 Oct 2026 (team leader's request):** commit `741635a` (with the console redesign, levers and backdrop commits
before it) pushed to `main` and live at https://rainready-wheat.vercel.app. Checked on the live address: the map loads,
the fly-in reaches `#/planner`, no console errors.

### Zone colours: against capacity by default (team leader, 21 Oct 2026)

**Problem:** no setting turned Area B red, and Today was always neutral, though FastFlood pools water at ponds A and B,
along the trunk-drain corridor and in Z03, and residents report flooding three times a year. **Cause:** zones were
coloured only by change versus today. The numbers already showed the shortfall. On the assumed 6 m drain, the drain
is over capacity from a 2-year storm (119 %); pond A is over its assumed capacity from a 10-year storm (106 %) and at
181 % in the 100-year storm.

**Decision:** the map now colours zones **against capacity by default**. Pond zones are measured against their pond's
capacity (stated, else the assumed one, **L**), and trunk-drain zones against the drain's assumed conveyance. A
**COLOUR BY: STORAGE SHORTFALL / CHANGE FROM TODAY** switch in the view bar brings back the change view. Legend
bands: *room to spare* (< 80 %), *nearly full* (80–100 %), *not enough room* (> 100 %), led by "On assumed capacities (L)";
in the change view *better* (blue, > 5 % less), *about the same*, *worse* (+5–20 %), *much worse* (> +20 %). The guided demo uses capacity for steps 1–5 and 10–12, and change for steps 6–9.
`screening.ts` is unchanged: the capacity colours are worked out in `data.ts` (`capacityLoad`, `zoneLook`).

| Today, 100-year storm | 6 m drain (as assumed) | 10 m drain, upstream built out |
|---|---|---|
| Pond A zones (Z03, Z04, Z06) | red, 181 % | red, 130 % |
| Pond B zone (Z07) | amber, 97 % | green, 70 % |
| Trunk-drain zones (Z01, Z02, Z05, Z08) | red, 101 % | amber, 94 % |
| Z09 | grey, outlet unknown | grey |

**Caution for the pitch:** red means *storage or conveyance falls short in the design storm*, on two L assumptions
(the drain's size and the 1.5 m live storage). It is not a flood map and never a depth.

**What-if pond made visible (same day).** The pond worked in the numbers (pond A −3 % at 5,000 m³, −17 % at
25,000 m³, −26 % at 60,000 m³) but no colour moved. Against capacity, pond A stays over its assumed capacity
(the what-if pond catches only Z06, about 39,700 m³). In the change view, a fall shared the green of "no change". Now: in the shortfall view, the zone the what-if pond catches (Z06) is measured against **that pond's size** (159 % at
25,000 m³, 66 % at 60,000 m³, so it turns green). Against today, a fall of 5 % or more is **blue ("down > 5 %")**, so pond A's
zones turn blue with the pond. Ceiling: beyond about 40,000 m³ a bigger pond adds nothing, because Z06 has no more
water to give. Letting the pond catch more zones is a change to `inputs.json` (`what_if_pond.serves`) **[open]**.

### Scenario presets redesigned (21 Oct 2026, team leader)

The old seven presets overlapped (four of them included "upstream built out"; "Assumed pond capacity" became
redundant once shortfall colours were the default). The new seven are in **three groups that tell the story**, each
chosen so its map looks different. Clicking a preset also sets the colour view, and each card shows a live one-line
result from the simulator (`presetSummary` in `data.ts`).

| Group (accent) | Preset | Settings | Colour view | What the map shows |
|---|---|---|---|---|
| The problem (red) | Today's design storm | 100-yr | Shortfall | Nearly all red: A 181 %, B 97 %, drain 101 % |
| | A common heavy storm | 2-yr (50 % chance each year) | Shortfall | Ponds have room (A 71 %); **only the drain corridor is red** (119 %), on both sides of the line |
| Across the council line (amber) | Upstream builds out | Area A built out | Change | Drain zones +10 % (amber) |
| | Larger upstream catchment | + 200 ha | Change | Drain +22 % (red); both ponds +7 % |
| Fixes to test (green) | Add a pond | 40,000 m³ what-if pond | Change | Pond A's zones −26 % (blue) |
| | Widen the shared drain | 10 m | Shortfall | Drain 85 %, B 63 % green; A still 117 % |
| | Fix it together | Built out + pond + 10 m drain | Shortfall | **No red left** (A 93 %, B 70 %, drain 94 %). With upstream built out, the pond alone leaves A at 134 % and the 10 m drain alone leaves A at 130 %: neither fix alone clears the red |

All figures use the assumed capacities (L). "Fix it together" is a what-if, not a design. It does not say which
party would do what: the pond and the drain may sit with different owners (see
[../research/RESPONSIBILITY_RECORD.md](../research/RESPONSIBILITY_RECORD.md)), which is the point of a shared picture.

## 8. Landing page: Malaysia map (21 Oct 2026, team leader)

**What:** the site now opens on a night globe framed on Malaysia (reference: the OSIRIS world map). Dots are flood
evidence; zooming into Bandar Bukit Raja, or clicking it, flies down (a fixed 2.4 s flight) and hands over to the
planner view, which opens top-down on the same coordinates and then glides into 3D. Elsewhere, zooming in shows
"No catchment model here yet". **Routes changed:** `#/` is the map, the planner is **`#/planner`**; `#/demo`,
`#/brief` and `#/resident` are unchanged. The rail gained **Malaysia** at the top.

| Layer | Real or example | Source |
|---|---|---|
| Country and state outlines | Real | Natural Earth 1:50m countries, 1:10m states (public domain) |
| **Official flood records** (red dots, 1,176) | **Real** | JPS Selangor GIS, public flood-record layers **2017–2024** (2021 layer skipped: a two-point map tour), read 21 Oct 2026. **Selangor only**, stated on screen. Place, district, year and type (flash, monsoon, ponding) only: the layers' **peak water levels**, durations and evacuations are **left out** (no depths). Hover a dot for its record |
| **Resident reports** (gold, pulsing) | **EXAMPLE** | `public/data/reports_example.json`, five records in the shared report format ([RESIDENT_PLANNER_INTEGRATION.md](RESIDENT_PLANNER_INTEGRATION.md)), on the three mapped flood streets and one upstream; no dates. Marked EXAMPLE everywhere |
| Catchment model (cyan ring) | — | Bandar Bukit Raja, the only model so far |

**Files:** `src/ui/Landing.tsx` (page, legend, tooltip, fade), `src/scene/Globe.tsx` (globe, dots, labels, fly-in),
`public/data/national.json` (440 kB, built by `scripts/build_national.py` from the raw downloads of
`scripts/fetch_national_sources.py`). The planner's model is preloaded on the map, so it opens without a wait.

**Checked (Playwright, 1600 × 900 and 390 × 844):** no console errors; fly-in to hand-over 2.6 s; the planner opens
top-down then glides to 3D; Guided demo from the map starts the demo; phone framing fits both the peninsula and
Borneo.

**Open:** [verify] JPS Selangor's terms for reusing its GIS layers on a public site. The guided demo still starts in
the planner; an opening step on the map (for the video's first shot) is not built.

### Map, nationwide; planner arrival; one meaning per colour (21 Oct 2026, team leader)

**Flood evidence for all of Malaysia.** No single public nationwide feed of flood points was found (searched 21 Oct
2026: data.gov.my, NADMA, MyWater). The map now combines three real sources at three levels of detail, each stated
in the legend and tooltip:

| Layer | Detail | Source | Notes |
|---|---|---|---|
| Flood records, Selangor (red) | Point | JPS Selangor GIS, 1,176 records 2017–2024 | As before; no water levels |
| **Flash-flood locations, all states** (orange, sized by count) | **Town** | JPS, *Status Lokasi Banjir Kilat 2017* (archive.data.gov.my): 493 listed locations in 91 towns, every state and federal territory | The list has place names, not coordinates: each town geocoded with OpenStreetMap Nominatim (`scripts/geocode_national.py`), checked inside its state (91 of 91). **Positions are approximate** |
| **Major flood events** (rings) | **Region** | Dartmouth Flood Observatory, *Global Active Archive of Large Flood Events*: 70 Malaysian events 1991–2021 | Centre of the affected region; month, year, cause and duration only (deaths and displacement left out). **[verify]** the archive is offered free "for scholarly research and education"; check before any commercial use |

Data sets checked and not used: JPS 2014/2015 flood events (state totals only) and JPS flood records 2000–2010
(by river basin, no points).

**Floating dots.** Dots rise off the globe on thin stems in a staggered wave when the page opens, then bob slowly;
the lift follows the zoom so stems stay about the same length on screen. Dragging now turns the globe at about the
speed of the cursor.

**Planner arrival without a stutter.** The stutter was the planner's set-up (merging ~1,500 meshes, building outlines,
compiling every shader) on the main thread. The planner now opens under a curtain the same colour as the fly-in's
fade; after four rendered frames it lifts and the **township grows from its centre outwards** behind a cyan scan edge,
buildings and trees rising out of the ground (1.8 s, shader-only: `REVEAL` in `src/scene/Township.tsx`). Arriving from
the map, it grows **in the top view** (set before the planner mounts), already in the storm colours; when the growth
ends the camera **swings into 3D on one eased arc** (`VIEW_ARC_MS` 1.8 s, `src/App.tsx`), settling about 3.7 s after the
curtain lifts. Nothing switches after that. Labels fade in at 1 s; flow arrows join when the growth ends. The TOP / 3D
buttons use the same arc.

**One risk band (revised the same day, team leader).** Every area on the map is coloured by **room for water** in
every preset: green room to spare, amber nearly full, red not enough room (against assumed capacities, L). The
"Colour by" switch and the separate change colours are gone. **Change from today shows as an arrow on each zone tag**
(e.g. "Z03 ▼ 26 %", "Z05 ▲ 10 %") when its pond's or drain's load moved by 5 % or more; the results panel's "▲ % vs
today" readouts are neutral text. Preset group headers are neutral gold. Demo steps 7–8 point at the arrows.

## 9. Credibility pass (21 Oct 2026, team leader)

**Assumptions tested** ([../research/HY_ASSUMPTIONS_CHECK.md](../research/HY_ASSUMPTIONS_CHECK.md)): satellite imagery shows no
trunk-drain channel 8 m or wider, and pond A is short for any drain under about 12 m; the 1.5 m storage band sits
inside MSMA 2 Chapter 7's 1–3 m planning range (pond A would need about 2.7 m). By MSMA's planning chart pond A is about
the right size if it could release: **the shortfall is the shared drain, not the pond.**

| Added | Where | Source of truth |
|---|---|---|
| "Checked against the ground": three agreements and **one miss** (frequent flooding points to street drains, not modelled) | About drawer, Brief (new section), demo step 12 | `src/lib/evidence.ts` `CHECKS` |
| "The two assumptions it rests on", with how far the finding depends on each | About drawer, Brief | `ASSUMPTION_CHECKS` |
| **JPS record pins** in the planner: ponding 2023, 2024 (Z03) and Setia Alam flash flood 2024 (upstream) | Planner view, demo step 4 | `JPS_RECORDS` |
| **"Maintained by"** on zone and pond cards, with confidence | Planner cards | `MAINTAINER` (from RESPONSIBILITY_RECORD.md) |

**Guided demo, now 14 steps (about 2.5 min):** 1 Malaysia map (counts read live from the map data; Next performs the
fly-in) · 2 One shared picture · 3 Council line · 4 Residents' streets **and the JPS record** · 5 Design storm · 6 Ponds
(1.5 m inside MSMA's range) · 7 Upstream · 8 Drain carries more · 9 What-if pond · 10 Drain size (**imagery finding**) ·
11 Brief · 12 **Checked against the ground** · 13 Resident door · 14 Close. `#/demo?play&clean` now starts on the map.
Brief steps scroll to their section.

**Fixes found while testing:** zone tags could not be clicked where another label's invisible wrapper overlapped them,
and a click on a tag also reached the canvas and cleared the card; both fixed (`html-pass` wrappers, the tag stops the
click).

### Responsibility record, seven lines (21 Oct 2026, team leader)

Rebuilt on Selangor's published rules ([../research/RESPONSIBILITY_RECORD.md](../research/RESPONSIBILITY_RECORD.md)): State
Assembly answers citing the Cabinet decision of 6 June 1996 (ponds: state owns, council maintains), the 2020 answer
(developer maintains ponds not yet handed over) and state cabinet decision MMKN 17/2025 (main drains JPS, secondary and
tertiary drains the council, JKR road reserves JKR). **Ponds A and B are now "not settled" (L)**: the handover status
that decides it is not public, and JPS's register has a blank land-title field for both. The drains move from L to M;
street drains and Sungai Keramat are added. No line is confirmed by its party yet.

| Where | What |
|---|---|
| Brief | Seven-line table: asset, mapped as, who maintains it by the rules, rule, confidence, confirmed by the party |
| Planner cards | Zone: "Maintained by" (what it drains to) and "Street drains" (MBDK or MBSA by side); pond: the full line |
| Source of truth | `src/lib/evidence.ts` `RECORD` |

## 10. Levers for a built town (21 Oct 2026, team leader)

**Why:** BBR and Setia Alam are already built, so "upstream development 0–100 %" and "what-if pond" read like a
design game ([../research/THREE_CHALLENGES_REVIEW.md](../research/THREE_CHALLENGES_REVIEW.md) section 1). Same maths,
reframed as the three decisions a built town still makes, plus one new kind of lever: upkeep.

| Before | Now | What changed |
|---|---|---|
| Upstream development | **Next parcels upstream** ("open land in Area A built") | Text only: the parcels not yet built, what a before-you-build check tests |
| What-if pond | **New retrofit pond** ("the kind already funded nearby, e.g. the RM7.3m Taman Mutiara pond") | Text only; tag "NEW POND · what-if" |
| Shared trunk drain | **Shared drain works** ("like the flood projects on Klang's urgent list") | Text only |
| — | **Keep it working** (section 04): *pond storage lost* 0–50 % (silt, weeds, blocked outlet) and *shared drain blocked* 0–60 % (silt, rubbish) | New |
| Presets in 3 groups | **4 groups**: The problem · Next parcels upstream · Fixes on the table · **Keep it working** | Two new presets |

**How the upkeep levers work.**
- *Pond storage lost* cuts the capacity a pond is measured against (entered, else assumed), in `data.ts` (`roomOf`).
  `screening.ts` is not involved: storage *required* does not change, the room does.
- *Drain blocked* is a new simulator input, `trunk_drain.blockage` (default 0, planner input): the drain's Manning
  capacity × (1 − blockage), capped at 0.9, in `screening.py` and `screening.ts`.
- **Same storm.** Left free, a blocked drain moves the critical duration and can look as if it carries *less*
  (2-year storm: 119 % → 102 %). So when blockage is set, the site holds the storm at the clear drain's critical
  duration, through a second new input, `storm.design_duration_h` (default empty = today's critical duration).
- Both are screening simplifications (in proportion), stated on screen; neither share is measured anywhere public.
  Street drains are still not modelled.

**New presets (read live from the simulator):**

| Preset | Settings | Result (assumed capacities, L) |
|---|---|---|
| Silted and blocked | 2-yr storm, ponds 30 % silted, drain 30 % blocked | Pond A 71 % → **102 %** (turns red), drain 119 % → **170 %** |
| Widened, then left to clog | 10 m drain, 30 % blocked | Drain 85 % → **122 %**, pond A 117 % → 139 %: the widening's gain is lost |

**Also:** Brief section "Keeping it working: silt and blockage" (kept as built / 30 % silted / 30 % blocked / both,
under the storm and drain in use); guided demo now **15 steps**, new step 11 "Keep it working" (numbers read live);
step 7 is "The next parcels upstream", step 9 "A fix on the table: a new pond". Fixed in passing: the capacity
inputs overflowed the Scenario panel (horizontal scrollbar).

**Checks (21 Oct 2026):** `screening.py --check` passes (new: blockage never lowers storage, and raises the drain's
load at the same storm); parity **216 of 216**; sourced `outputs.json` unchanged apart from the new `blockage: 0`
field; production build, Playwright 1600 × 900 and 390 × 844, every preset, Brief and demo: no console errors.

**On hold (team leader):** linking a resident's blocked-drain report to the blockage lever ("Test in planner"),
until the resident report function is built.

## 11. After the water (21 Oct 2026, team leader)

**Why:** "If BBR floods badly, who is responsible for the losses?" had no plain answer anywhere
([../research/THREE_CHALLENGES_REVIEW.md](../research/THREE_CHALLENGES_REVIEW.md) section 2). Source of every line:
[../research/AFTER_THE_FLOOD.md](../research/AFTER_THE_FLOOD.md).

| Where | What |
|---|---|
| **`#/after`** (new page; rail item **After**, life-buoy icon) | Four things to know first (no one pays automatically · insurance only with flood cover · RM1,000 federal + RM1,000 Selangor relief · compensation through a court) → the chain in six stages (before, warning, during, right after, claims, compensation) with who, what, sources and confidence → the BBR table from the responsibility record ("who holds the duty if this fails") → the Taman Sri Muda ruling, as reported, with its limits → what a resident can do, in order → where RainReady fits |
| Brief | New section "After a flood: who does what", one paragraph, linking to `#/after` |
| Planner cards | Zone: "If these fail: who does what →" under Street drains; pond: "If this fails: who does what →" under Maintained by |
| Guided demo | One sentence added to the Brief step; no new step |
| Data | `src/lib/evidence.ts`: `AFTER_STAGES`, `SRI_MUDA`, `RESIDENT_STEPS` (the BBR lines reuse `RECORD`) |

**Wording rules kept:** "who holds the duty under the published rules", never "who is liable" for BBR; the Sri Muda
ruling is stated as reported, with "not final" and "[verify] appeal and damages" on screen; "not legal advice" in the
page's label and footer. The damage record (concept feature 8) stays with the resident report work (team leader).

**Phone:** the rail now has nine items, so **Layers is hidden below 860 px** (it only toggles 3D layers).

**Fixed while testing:** the page first reused the class name `.stage`, which is the 3D view's fixed container; the
chain now uses `.chain` / `.chain-row`.

**Checked (21 Oct 2026, Playwright, 1600 × 900 and 390 × 844):** page, Brief section and card links render; no
horizontal overflow on the phone; no console errors.

## 12. Findings and Recovery: clearer names, a picture per chapter (21 Oct 2026, team leader)

**Why:** "Brief" and "After" did not say what was inside, so new visitors and judges would not click; both pages were
walls of text and tables. Routes are unchanged (`#/brief`, `#/after`); the names and the reading order changed.

| Page | Menu | Title | What a first-time reader sees |
|---|---|---|---|
| `#/brief` | **Findings** | *Where the water has nowhere to go* (kicker: Shared Capacity Brief) | One-sentence headline (numbers read live) → five chapters, each one plain sentence and one picture: **1** pond tanks (water vs room, red spill over the rim, Olympic-pool equivalent at 2,500 m³) and a drain meter · **2** an upright flow diagram (streets → ponds → shared drain → main ditch, "can't empty" when the drain is full) with five numbered steps · **3** a fixes chart (today, new pond, wider drain, both, both then 30 % blocked; pond A and drain as % of room, dashed 100 % line, "Clears it" / "Still short") · **4** "0 of 7 confirmed" bar and owner cards with holder chips · **5** check tiles (three agree, one miss) and the two assumptions. All former tables are kept in a folded **"For engineers"** section (opened automatically for printing) |
| `#/after` | **Recovery** | *After a flood: who helps, who pays* | Four icon tiles → a six-stage stepper (tap for who, what, source) → two pictograms (about 2 in 3 ringgit of 2021 losses uninsured; about 1 in 9 of one insurer's motor customers had flood cover) and a bar chart of Selangor's flood aid by district (Klang 23,450 highlighted; 72,451 in all) → a simple map of Bukit Raja's drains and ponds coloured by holder → the Sri Muda case as a four-point timeline and three "the court found" cards → five resident step cards |

**Chart rules (dataviz skill):** red / amber / green only ever mean room for water and always come with a word and an
icon; holders use a categorical set validated for colour-blind separation on the dark surface (blue MBDK `#3987e5`,
orange MBSA `#d95926`, aqua JPS `#199e70`, all-pairs PASS), plus a hatched grey for "not settled", always with the
name. A two-slice donut was replaced by a pictogram stat; the aid chart is one series with Klang emphasised. Every
mark has a hover / tap tooltip; bars and tanks grow once in view (off under reduced motion, full in print). Every number
is read from the simulator or a sourced figure; none is an example.

**Plain words:** sentences of about 20 words or fewer; "conveyance", "critical duration" and similar terms only inside the
engineers' section; dotted-underline hints for "100-year storm", "assumed" room and the drain size.

**Code:** `src/ui/Viz.tsx` (reveal, tooltips, term hints, room label, holder chips), `src/ui/Brief.tsx` (Findings; the old
page is now `Engineers`), `src/ui/After.tsx` (Recovery), styles at the end of `src/styles.css`. Demo step 12 is now "The
findings, on one page"; card links read "After a flood: who helps, who pays →".

**Phone:** the bottom menu's eight items now share the width (labels 7.5 px). **Checked (Playwright, 1440 × 900 and
390 × 844):** both pages render, no horizontal overflow, tooltips work, demo steps reach the Findings sections, no
console errors.

## 13. The resident door: Waterline integrated (21 Oct 2026, team leader)

**What:** the teammate's resident report system **Waterline** (github.com/yh1127/RainReady, Vite + React + Leaflet,
read in full before porting) now runs inside the site at **`#/resident`** (left menu **Residents**), replacing the two
phone mock-ups. **Layout kept as the original** (team leader): sidebar, top bar, township map with recent reports,
report form, my reports, inbox, report window, notifications, toasts, sign-in. **Style changed only:** IBM Plex,
the console palette, gold accent, 4–6 px corners, the site's transitions; the street map uses the same OpenStreetMap
tiles in night tones (CSS filter); every rule scoped under `.wl` so its class names never touch the site's.

| Code | What |
|---|---|
| `src/resident/ResidentApp.tsx` | Waterline's app, typed; layout and flows as the original |
| `src/resident/waterline.css` | Its stylesheet: same layout values, site fonts / colours / transitions, scoped `.wl` |
| `src/resident/data.ts`, `geocode.ts` | Issue types, stages, samples; the Nominatim address lookup (unchanged behaviour, rate-limited) |
| `src/resident/store.ts` | **One report store for the site** (browser-local, as Waterline): read by the resident door, the planner's 3D pins and the Malaysia map; `toShared()` gives the shared report format |
| `src/resident/route.ts` | **Where a report goes**: zone (point in the zone outlines, now in `zones_meta.json`) and council side (zone, else the side of the OSM council line), then the holder by the responsibility record's rules |

**What changed from the original, and why**

| Change | Why |
|---|---|
| Stages **Reported → Checked by association → Sent to [holder] → Cleared** (was Reported → Crew Dispatched → In Progress → Cleared); "Admin" is now **Residents' association** | RainReady forwards to the official channel and never dispatches anyone (team leader, 21 Oct 2026). Older stored reports are migrated |
| A **"Goes to …"** box on the form and in the report window: holder, channel, zone, side, rule, confidence | The responsibility record routes each report: drain issues → MBDK or MBSA by side (M); roads, lamps, trees → the council, JKR on its roads (L); pipe leaks → Air Selangor (M); otherwise "not known yet", never guessed |
| **"Test in planner"** on drain reports in a zone that drains to the shared drain | Opens the planner with the shared drain 30 % blocked, in the storm: residents' reports move the plan |
| Status colours: one blue ramp with words | Red, amber and green mean room for water on this site |
| Satellite image kept, compressed 2.7 MB → 337 KB, with the credit "Imagery: Esri, Maxar, Earthstar Geographics, and the GIS User Community · Powered by Esri" | It is a capture of Esri World Imagery (matched to Esri's own export of the same bounds on 21 Oct 2026). Esri allows static captures with that credit where not resold (M) |
| **Move-now plan** added to the resident's sidebar | Waterline has none; the existing mock-up (links to Public Infobanjir and METMalaysia) moved in |
| Sign-out kept; the guided demo signs in as a resident automatically | The demo must not stop at the role choice |

**Joins to the rest of the site:** open reports appear as **pins in the planner** (layer "Resident reports"; tap →
that report in the resident door); the **Malaysia map** shows them in place of the old example file
(`reports_example.json` is no longer read); guided demo step 14 is the real resident door and **new step 15**
"Reports land on the shared picture" points at a report pin (the demo is now 16 steps). On phones, Waterline's own
tab bar sits just above the site's bottom menu.

**Checked (21 Oct 2026, Playwright, 1440 × 900 and 390 × 844):** sign-in; live address lookup; a blocked-drain
report at the default pin routes to **zone Z05, Klang side, MBDK (M)**; it appears in My reports, as a 3D pin and on
the Malaysia map count; "Test in planner" opens the planner with the drain at 144 %; a pin opens its report; the
association moves it to "Sent to MBDK" with a note and history; satellite view shows the credit; no console errors.

**Not built / open:** reports stay in one browser (no backend); push notifications none (as the original);
[verify] that MBDK and MBSA take drain complaints through Sispaa and iClean Selangor today (the channel line names
both); the teammate should review the ported version and the new stages.

## 14. Scenario panel: descriptions on hover (22 Oct 2026, team leader)

The Scenario control was too crowded to read. Each preset now shows only its title and its numbers; each lever section
only its heading (with an ⓘ cue) and its sliders. The description, and the "what you will see" line, appear in a tip
beside the panel after the pointer rests about a second (`HOVER_DELAY_MS` = 900 ms in
[`../website/src/ui/HoverTip.tsx`](../website/src/ui/HoverTip.tsx)); also on keyboard focus and on a long press on
touch screens. No text was removed, only moved. **This changes the guided demo's look at the steps that open the
Scenario panel** (the spotlights still point at the same sections).

## 15. Phones: one thing at a time (22 Oct 2026, team leader)

The phone view was crowded (results over half the screen, panels over the model, labels overlapping). Below 860 px
only (desktop unchanged): the results fold to a one-line summary (tap **More**); Scenario, Layers and the 2D Site
panel open as bottom sheets with a handle; presets become one swipeable row; tips appear as a toast above the rail
(long press); the rail shows short labels (Map, Model, What-if, Report, Brief, After, Demo) and drops About (the
status pill opens it); the header shows a short pill (ESTIMATE / WHAT-IF); the 3D view keeps spots, ponds and areas
but drops record, report and drain tags and sits near the centre; the Malaysia map folds its layer list behind one
button and keeps "Open Bandar Bukit Raja" at the bottom; the inspector card is a bottom sheet. Same treatment on the
2D sites. CSS block at the end of `src/styles.css`; markup hooks in `Shell.tsx`, `Planner.tsx`, `Landing.tsx`,
`platform/Panels.tsx`.

**Round 2 (22 Oct 2026, team leader):** on phones the guided demo's caption now sits at the top (compact, scrolls
if long) and the model is lowered below it; What-if and Layers open as a shorter sheet (46 vh, 30 vh in the demo)
while the one-line result stays visible at the top, and the camera lifts the model into the space between them, so a
lever's effect on the township is seen as it moves (App.tsx `phoneY`; on 2D sites the map pans up, MapView `lift`).

**Swipe to close (22 Oct 2026, team leader):** on phones every bottom sheet (What-if, Layers, the 2D Site panel,
the inspector cards) follows the finger down from its handle or title, or from anywhere when scrolled to the top, and
closes past a quarter of its height or on a flick; it springs back otherwise. Sideways swipes (the preset row) and
scrolling inside the sheet are untouched. `src/ui/useSwipeToClose.ts`. Also: the water backdrop on portrait screens
shows a wider stretch of finer swells, rendered near real resolution (`scene/WaterBackdrop.tsx`).

## Smoothness fix (23 Oct 2026, team leader)

**Symptom:** a visible freeze when the 3D township's labels appeared, and at guided-demo steps 9 → 10 → 11.
**Cause (profiled):** the overlays found ground height by raycasting the zone meshes for every point of the drain
ribbon and council curtain, testing every triangle each time: about 365 ms when the labels mounted, and about 235 ms
whenever the drain width changed (demo steps 10 and 11). A second, smaller hitch (about 90 ms) came from mounting the
overlays' shaders and all 22 HTML labels in one frame.
**Fix (`src/scene/Overlays.tsx`, `App.tsx`):** the zones' triangles are binned once on a 40 m grid, so a height lookup
tests a handful (same heights as the raycast to 1e-13 m over 2,864 points; about 600× faster). The overlays now mount
behind the opening curtain (shaders compile unseen) and fade in; the labels mount three per frame, a 0.1 s cascade.
**Result (production build, 1920 × 1080):** no frame over 34 ms after the curtain lifts; steps 9 → 10 → 11 with no
dropped frames.
