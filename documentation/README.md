# RainReady — Documentation

**Project:** RainReady — one shared picture of how water moves across council and developer boundaries, with two doors:
planners see where storage falls short, residents act in time, and their reports shape the next plan.
**Competition:** Sime Darby Property University Hackathon 2026 · Theme: Planet, climate resilience.
**Reference site:** Bandar Bukit Raja, Klang, with Setia Alam upstream.
**Phase:** research and planning. **Deadline:** 23 October 2026, 11:59 p.m.

New here? Read [RAINREADY_CONCEPT_V2.md](RAINREADY_CONCEPT_V2.md), then [PROJECT_STATUS.md](PROJECT_STATUS.md), then
open the [Google Sheet tracker](https://docs.google.com/spreadsheets/d/1gMBz5Y6DVhsBYTpGtS3eAw-8-bzyhJkBsQZhWgv-G8s/edit)
to find your research questions.

---

## Current documents

| Read it for | File |
|---|---|
| **The concept we are building around**: problem, users, two doors, features, video, deck outline, decisions | [RAINREADY_CONCEPT_V2.md](RAINREADY_CONCEPT_V2.md) |
| How the 3D township (Blender) and the screening simulator are built: setup, decisions, naming, inputs, order of work | [TOWNSHIP_3D_AND_SIMULATOR.md](TOWNSHIP_3D_AND_SIMULATOR.md) |
| Where we are, the decision log, what is still open, what must be verified, what could sink us | [PROJECT_STATUS.md](PROJECT_STATUS.md) |
| The website: style (modelled on ICQR Magic Tree), screens, build, how to run it | [WEBSITE.md](WEBSITE.md) |
| How resident reports (features 5–6) become pins in the planner view: coordinates, report format, privacy | [RESIDENT_PLANNER_INTEGRATION.md](RESIDENT_PLANNER_INTEGRATION.md) |
| The platform: any township as a site pack, the network engine, the generated second site, upload, portfolio (22 Oct) | [PLATFORM.md](PLATFORM.md) |
| How to make the 5-minute video from the presentation and the guided demo: recording, editing, hand-in | [VIDEO_GUIDE.md](VIDEO_GUIDE.md) |
| The video's outline and full script, scene by scene with timecodes, and a read-through for the voice-over | [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md) |

## Research findings ([../research/](../research/README.md))

The full index is in [research/README.md](../research/README.md). The ones most often needed:

| Read it for | File |
|---|---|
| How every [TBD] and [verify] was settled. **Wins over older files** | [TBD_VERIFY_RESOLUTION.md](../research/TBD_VERIFY_RESOLUTION.md) |
| The simulator's sourced inputs (MSMA 2), result and sensitivity | [HY_screening_inputs.md](../research/HY_screening_inputs.md) |
| Who maintains ponds and drains under the official rules | [RESPONSIBILITY_RECORD.md](../research/RESPONSIBILITY_RECORD.md) |
| Three challenges to the pitch, and how RainReady scales beyond BBR | [THREE_CHALLENGES_REVIEW.md](../research/THREE_CHALLENGES_REVIEW.md), [SCALING_PLATFORM.md](../research/SCALING_PLATFORM.md) |

## Supporting documents ([supporting/](supporting/))

The evidence and reference material the concept rests on. Still valid; cite from these.

| Read it for | File |
|---|---|
| What the competition requires, when, and how it is judged | [COMPETITION_HUB.md](supporting/COMPETITION_HUB.md) |
| Whether the problem is real, whether anyone already solved it, and how our claim must be worded | [PROBLEM_VALIDATION.md](supporting/PROBLEM_VALIDATION.md) |
| Why Bandar Bukit Raja and not another township | [TOWNSHIP_GAP_ANALYSIS.md](supporting/TOWNSHIP_GAP_ANALYSIS.md) |
| The public evidence and pond figures we are allowed to cite | [BBR_PUBLIC_DOCUMENT_SURVEY.md](supporting/BBR_PUBLIC_DOCUMENT_SURVEY.md) |
| What public data exists, what it cannot do, and the limits we must state | [FLOOD_FEASIBILITY_SURVEY.md](supporting/FLOOD_FEASIBILITY_SURVEY.md) |
| v1 deck text, the judge appendix (evidence, sources, assumption ledger, limitations) and team-only notes. **Slide structure superseded by concept v2 section 8; the appendix is still the source list** | [FLOOD_PITCH_DECK.md](supporting/FLOOD_PITCH_DECK.md) |

## Everything else

| Where | What |
|---|---|
| [Google Sheet tracker](https://docs.google.com/spreadsheets/d/1gMBz5Y6DVhsBYTpGtS3eAw-8-bzyhJkBsQZhWgv-G8s/edit) | Research List, Task List, Summary, and a team mind map on the README tab. The live source of who does what |
| [Canva deck](https://www.canva.com/d/lE6MCvrtngd0c4a) | The designed 10-slide deck, built from the v1 deck text; not yet updated to v2 |
| [../research/](../research/) | Research findings, one file per Research List question, including the BBR site model |
| [../simulations/rainready-playground/](../simulations/rainready-playground/) | 2D interactive model for explaining the idea to the team. Invented terrain, illustrative numbers |
| [../simulations/upstream-runoff/](../simulations/upstream-runoff/) | Earlier conceptual runoff tool. Not for engineering decisions |
| [archive/](archive/) | Superseded RainReady files (incl. the HydroShield merge note and the hydrology input request) and the ideas from before RainReady. Nothing is deleted |
| `../SDP slides/` | The official briefing PDF and page images |

---

## Rules for anything written here

- **Risk bands, never predicted flood depths.** Terrain error is about 1 m in built-up areas.
- **Advisory, never forecast.** Anything we send builds on official MET Malaysia and drainage department warnings and
  links back to them.
- **Neutral wording** about the developer, the councils and the residents. Show where water flows and where storage runs
  short. Never assign blame.
- **Developer booklet figures are design values, not as-built.** Write "designed to hold", and write "residents said in
  2024" for the four shallow ponds.
- **Mark your confidence:** **H** high, **M** medium, **L** low. **[verify]** means unconfirmed. **[TBD]** means a blank to fill.
- **Never invent a number, a quote or a source.** If it is not in a source you have read, it does not go in.
- **No implementation or build plans while we are still researching.** Record what we have learned and what is still
  unknown; sequencing comes later.
