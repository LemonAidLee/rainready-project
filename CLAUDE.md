# CLAUDE.md — RainReady (SDP Hackathon 2026)

Context for any Claude session in this folder. Read this, then
[documentation/RAINREADY_CONCEPT_V2.md](documentation/RAINREADY_CONCEPT_V2.md) (**the concept everything revolves
around**), then [documentation/PROJECT_STATUS.md](documentation/PROJECT_STATUS.md).

---

## 1. The project

**RainReady** — one shared picture of how water moves across council and developer boundaries, with **two doors**:
planners see where storage falls short, residents act in time, and their reports shape the next plan. Tagline:
*Property lines stop at the fence. Water doesn't.*

- **Reference site:** Bandar Bukit Raja (BBR), Klang, with Setia Alam upstream in Shah Alam.
- **Theme:** Planet → climate resilience.
- **Planner door:** catchment view · rain and upstream scenarios · pond what-if and before-you-build check · Shared
  Capacity Brief. **Resident door:** report and track through existing messaging · move-now plan on official warnings.
  Responsibility record runs through both. Full list in concept v2 section 4.
- **For the competition** these reach judges through a simulated township in 3D (loosely based on BBR), flood physics run
  over that model, and a website with an AI layer that explains the result.
- **Design principle:** decision support under uncertainty, not prediction.

**Phase: research and planning**, except the approved 3D township (built 20 Oct 2026), the screening simulator (v2 on
sourced MSMA 2 values, 21 Oct 2026) and the website (deployed 21 Oct 2026 at https://rainready-wheat.vercel.app from the private GitHub repo
LemonAidLee/rainready-website; see
[documentation/WEBSITE.md](documentation/WEBSITE.md)).
See "Start here" in [documentation/TOWNSHIP_3D_AND_SIMULATOR.md](documentation/TOWNSHIP_3D_AND_SIMULATOR.md).
Every [TBD] / [verify] was settled or replaced by a stated assumption on 21 Oct 2026:
[research/TBD_VERIFY_RESOLUTION.md](research/TBD_VERIFY_RESOLUTION.md) (wins over older files); FastFlood cross-check in
[research/FASTFLOOD_CROSSCHECK.md](research/FASTFLOOD_CROSSCHECK.md).

---

## 2. The competition

- Sime Darby Property University Hackathon 2026, "Township of Tomorrow". Themes: People or Planet. One well-defined
  problem, not a whole township.
- **Proposal deadline: 23 October 2026, 11:59 p.m.** Incomplete submissions are not considered.
- **Required:** pitch deck (max 10 main slides, appendix allowed), 5-minute video or live-demo link, prototype or code
  link. Supporting documents optional.
- **Judging:** Impact 25 · Innovation 20 · Feasibility 20 · Strategic fit 15 · Commercial value 10 · Team, evidence and
  pitch 10.
- **Later:** top 10 on 28 Oct · mentoring 2–6 Nov · refined submission 11 Nov · pitch day 14 Nov (physical) · final
  3 Dec at Elmina.
- Full detail in [COMPETITION_HUB.md](documentation/supporting/COMPETITION_HUB.md). The official briefing slides are
  image-only PDFs in `SDP slides/`.

---

## 3. The team

Five students, working in four tracks. The user is the **team leader**. **Since 22 Oct 2026 the team leader, with
Claude, does the hydrology work and checks it**; nothing waits on anyone else.

| Track | Who | Scope |
|---|---|---|
| Architecture: 3D city | Architecture student | 3D model of the simulated township. **Blender or SketchUp only**, nothing else |
| Hydrology and physics | Team leader, with Claude (from 22 Oct 2026) | Rainfall to runoff, the maths and physics, how upstream development changes downstream flooding, and how to apply flood physics to the 3D model |
| Frontend and AI | The other EE student | The project homepage, and where AI genuinely improves the product |
| Team leader | **The user** | Documentation, tracker, pitch deck, appendix, integration of all three tracks, and continuous research into features that would make the product more complete and versatile |

**Constraints:** no site visits and no interviews — everything comes from public sources and an online resident survey.
The team cannot contact SDP until shortlisted (user's statement, not confirmed in the briefing), so use public numbers
until then.

---

## 4. Key evidence (all public)

- BBR residents say **Jalan Makyong** floods **at least three times a year** (Sinar Harian, 25 May 2024; Jalan Sumazau
  is named there only for a retention pond, Persiaran Batu Belah for bigger drains); worst flood **December 2021 (3 m)**;
  latest cited **24 April 2024**. JPS Selangor's own GIS logs ponding at "Bandar Bukit Raja" in 2023 and 2024. About **583 residents across 48 associations** petitioned the Menteri Besar in 2024. They said the
  four retention ponds then in use were shallow and insufficient, and that councils and developers shift blame. Water
  flows from Setia Alam (Shah Alam) into BBR (Klang), under different councils.
- SDP's managing director: *"It is quite urgent, and this is a top priority for us"* (The Edge, 21 Nov 2024).
- SDP's BBR booklet: Wetland Townpark **designed to hold** 16,000 / 34,000 / 50,000 m³ (normal / additional / maximum);
  180-acre storm management area; 130 acres of ponds; 3.3 km of swales. **Design figures, not as-built.**
- Many programmes already exist: RM7.3m ~2 ha Taman Mutiara pond (delayed in 2024), RM150m Shah Alam works for Setia
  Alam, 17 urgent Klang projects across 13 hotspots, a joint Selangor–FT strategy (23 Aug 2026). Sinar Harian (5 May 2025):
  over 300 unowned ponds identified **in Selangor**, about 55 taken over. Ponds A and B are on JPS Selangor's own pond
  list (phase 1), so they are not among the unowned ones.
- **Our claim:** separate programmes, separate councils, no shared picture. **Never "nothing is being done".**

Sources and figures: [BBR_PUBLIC_DOCUMENT_SURVEY.md](documentation/supporting/BBR_PUBLIC_DOCUMENT_SURVEY.md) and the
appendix in [FLOOD_PITCH_DECK.md](documentation/supporting/FLOOD_PITCH_DECK.md).

---

## 5. Never use these

- KLASS RM144m, RM574.5m dual-function ponds, Sungai Kapar works finishing around 2030 — these appeared only in search
  summaries.
- **Any predicted flood depth.** Terrain error is about 1 m in built-up areas, so show risk bands or scenarios only.
- "Four shallow ponds" as current fact — say "residents said in 2024".
- National flood losses as the main argument; they fell in 2025 and are dominated by east-coast river floods.
- Anything from the archived walkability sources flagged as weak.

---

## 6. How to work with this user

- **Be honest about limits.** Say when evidence is thin, sources conflict, or something is unverified. Mark unverified
  items **[verify]** and blanks **[TBD]**. Use confidence labels **H / M / L**.
- **Never fabricate** a number, quote or source. Search before asserting. This includes plausible-looking details such as
  phone numbers and dates in mock-ups.
- **Neutral wording** about SDP, councils, developers and residents. The flood topic is a live public dispute. Never
  assign blame; show flow paths and capacity.
- **Advisory, not forecast** for any alert feature. It must build on official warnings and link back to them.
- **No implementation or build plans while the project is in the research phase.** Record what is known, what is
  assumed and what is still unknown. Do not write build sequences, learning schedules or stack decisions as
  documentation; tool choice is itself an open research question. **Exception (team leader, 20 Oct 2026):** the 3D
  township in Blender and the screening simulator are approved for implementation, and (22 Oct 2026) the platform
  ([documentation/PLATFORM.md](documentation/PLATFORM.md)); see
  [documentation/TOWNSHIP_3D_AND_SIMULATOR.md](documentation/TOWNSHIP_3D_AND_SIMULATOR.md).
- **Output as Markdown** in `documentation/` or `research/`. Keep documents detailed but not bloated.
- **Name the audience.** When producing something for teammates or judges, open the hand-over message with one line
  saying who it is written for.
- Prefer concise chat answers; put the detail in files. Link files with relative Markdown links.

---

## 7. Where things are

| Path | What |
|---|---|
| [documentation/README.md](documentation/README.md) | Index of current and supporting documents, and the house rules |
| [documentation/RAINREADY_CONCEPT_V2.md](documentation/RAINREADY_CONCEPT_V2.md) | **The concept.** Problem, users, two doors, nine features, implementation split, video, deck outline, decisions of 20 Oct 2026 |
| [documentation/TOWNSHIP_3D_AND_SIMULATOR.md](documentation/TOWNSHIP_3D_AND_SIMULATOR.md) | **Implementation** of the 3D township (Blender via the Blender MCP) and the screening simulator. Setup, decisions, data contract, order of work |
| [documentation/PROJECT_STATUS.md](documentation/PROJECT_STATUS.md) | State, decision log, open decisions, verify list, known weaknesses |
| [documentation/supporting/](documentation/supporting/) | Evidence the concept rests on, written for v1 but still valid: competition hub, problem validation, township gap analysis, BBR public document survey, feasibility survey, v1 deck text with the judge appendix (Part C team-only — delete before submitting) |
| [documentation/archive/](documentation/archive/) | Set-aside ideas and superseded files, incl. the HydroShield merge note. Nothing deleted |
| [research/](research/) | Where RainReady research findings go, one file per Research List question |
| `research/archive/` | Superseded RainReady research (QGIS plan, tool survey) and the pre-RainReady walkability and shade packs; index in its README |
| [simulations/township-3d/](simulations/township-3d/) | **The 3D township** (Blender): `township.blend`, build scripts (`style_scene` → `build_features` → `build_town` → `look_ghibli` → `build_zones` → `drive_scene`), `plan_town.py`, `plan_zones.py`, `screening.py` + `inputs.json` (simulator, no Blender), `data/`, `renders/` |
| [simulations/platform/](simulations/platform/) | **The platform** (22 Oct 2026): `network.py` (general drain-network engine, = `screening.py` on BBR) + `network.ts`, `build_site.py` (site pack from open data), `build_index.py` (registry), `sites/<id>/`. See [documentation/PLATFORM.md](documentation/PLATFORM.md) |
| [website/](website/) | **The website** (Vite + React + three.js): planner view, Findings, Recovery, and the resident door (Waterline, the teammate's report system, in `website/src/resident/`). `npm run dev` / `npm run build`; data synced from `simulations/township-3d/exports/` |
| [presentation/](presentation/) | **HTML presentation for the video** (13 slides, animated; keys in its README). Not the submitted pitch deck |
| [simulations/rainready-playground/](simulations/rainready-playground/) | 2D interactive teaching model. Invented terrain, illustrative numbers |
| [simulations/upstream-runoff/](simulations/upstream-runoff/) | Earlier conceptual runoff tool, not made in these sessions |
| `SDP slides/` | Official briefing PDF and page images |

**Live, outside the repo:**

| Link | What |
|---|---|
| [Google Sheet tracker](https://docs.google.com/spreadsheets/d/1gMBz5Y6DVhsBYTpGtS3eAw-8-bzyhJkBsQZhWgv-G8s/edit) | The source of truth for who does what. Tabs: README (with a team mind map), Research List, Task List, Summary, plus three older tabs not yet updated (Hand-offs, Assumption Ledger, Open Items) |
| [Canva deck](https://www.canva.com/d/lE6MCvrtngd0c4a) | The designed 10 slides |

### The tracker's structure

- **Research List** — 29 questions: AR1–AR7 (architecture), HY1–HY10 (hydrology), FE1–FE6 (frontend and AI),
  TL1–TL6 (team leader). Data in rows 6–60.
- **Task List** — 44 tasks: SH (shared), AT, HT, FT, TT, mirroring the research IDs. Data in rows 6–120.
- **Summary** — all formulas; counts by track and phase. Breaks silently if a Track name is misspelled.
- Columns on both work sheets: Track is **B**, Priority **L**, Start **M**, End **N**, Status **O**.

---

## 8. This machine (Windows 11, Git Bash and PowerShell)

- Python runs normally. `python -I` hides user-installed packages (e.g. openpyxl); use it only for untrusted downloads.
- `pdftotext` and `pdftoppm` (Poppler) are available. **LibreOffice is not installed**, and the xlsx skill's `recalc.py`
  fails here ("AF_UNIX"). Formulas written by openpyxl only calculate when opened in Excel or Sheets.
- **Google Sheets** works through the `nango-google-sheets` MCP tools. `batch-update-spreadsheet` is atomic: one bad
  request rolls back the whole call. Clear a basic filter before merging cells across its range, and you cannot merge
  across frozen columns.
- **Canva** works through the `claude_ai_Canva` MCP tools. Its AI generation garbles text — always read the design back
  and check numbers and spelling before handing it over.
- `WebFetch` and `WebSearch` are deferred tools: load with ToolSearch (`select:WebFetch`). Redirecting hosts (e.g.
  `fmtv5.freemalaysiatoday.com`) need the redirected URL.
- Playwright cannot open `file:` URLs; serve a local page over `http://127.0.0.1` instead.
- Image-only PDFs (the SDP booklet, the briefing slides): render pages with `pdftoppm` and read them as images.
- Temporary files go in the session scratchpad, never in the project.
- **shapely 2.2** is installed for the user (`pip --user`); run scripts that need it with plain `python`, not `python -I`.
- **Overpass API:** the main server is often overloaded; `https://maps.mail.ru/osm/tools/overpass/api/interpreter` works
  as a mirror. Save downloads to the scratchpad first.
- **Blender MCP:** long `execute_blender_code` calls return "No data received" but still finish; Windows sometimes locks
  `township.blend` on save ("file saved with @") — just save again.
