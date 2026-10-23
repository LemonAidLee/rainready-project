# Teduh: Background and Problem Statement

> **Status: set aside (10 Oct 2026).** The team moved to the flood idea after the umbrella objection and because no complaint about heat or shade was documented in any SDP township. See [PROJECT_STATUS.md](../PROJECT_STATUS.md). Kept for reference.

*Working name. "Teduh" is Malay for shady or sheltered. Not yet checked for existing products or trademarks.*

**Competition:** Sime Darby Property (SDP) University Hackathon 2026, "Township of Tomorrow". Proposal due **23 October 2026, 11:59 p.m.**
**Status:** Proposed direction, open for team discussion. Scores and judgements here are the analysis's own, not the judges'.

---

## 1. One-line idea

A decision tool that shows SDP's planners **where shade will do the most good** on the routes residents walk to daily destinations and transit, and what to build there first.

## 2. The problem

> **SDP's planning and landscape teams cannot see which walking routes in a township are hottest, least shaded and most used, so shade and trees are placed by guesswork. Residents making short daily trips end up with uncomfortable routes, and short trips default to the car.**

| | |
|---|---|
| **User (decision-maker)** | SDP township planning and landscape teams |
| **Beneficiary** | Residents on short daily walks: to a bus stop, school, shop or surau |
| **Theme** | Planet → Climate resilience (it also touches People → Mobility) |
| **Pain being addressed** | Walking comfort and route choice, not a casualty crisis |

**Honest framing:** this is a tool that helps planners. Residents feel the benefit only after shade is built. See section 7.

## 3. Why this problem (evidence summary)

Confidence: **H** high, **M** medium, **L** low. Full detail is in [EVIDENCE_ANALYSIS.md](../../research/archive/EVIDENCE_ANALYSIS.md) and [ONLINE_ONLY_DECISION.md](../../research/archive/ONLINE_ONLY_DECISION.md).

| Claim | Evidence | Conf. |
|---|---|---|
| Malaysians rarely walk for daily transport | 77% name a private vehicle as main mode and 5% walking (Ipsos, n=500, 2025); 84% do not walk or cycle for transport (NHMS 2023, n=13,616) | M / H |
| People will walk short distances | Most respondents willing to walk under 10 minutes or 500 m to a station (Bangsar/Shah Alam, n=325) | M |
| Shade works in the Malaysian climate | Dense roadside canopy cut perceived heat load (PET) by about 25% on KL roads; east-west and north-west/south-east streets were hottest at PET 41-43 °C vs 37 °C ([Zaki et al. 2020](https://www.mdpi.com/2071-1050/12/3/1053)) | M |
| Shade is lacking for some | About 35% of Greater KL respondents reported shaded pedestrian lanes as insufficient or needed (n=558, 2016-17, landline) | L-M |
| Heat deters some walking | Heat named a walking barrier by 48% in a small online survey (n=60, 2021) | L |
| Heat harm exists but is small | MOH recorded 28 heat-related illnesses and 1 death by 25 Mar 2024; Selangor 3 cases | M |

**What we do not have:** a survey showing how many residents *avoid walking because of heat*, and any data from an SDP township. Both are assumptions to test with the planned online resident survey.

## 4. Why it fits SDP

- **Strategy fit.** SDP's 2025-2030 strategy includes climate resilience, urban biodiversity and community experience. Trees and shade serve all three.
- **Same shape as problems SDP names.** The briefing's Planet examples include "selecting the most suitable sites for solar", which is a siting-and-prioritisation problem like this one.
- **SDP controls the levers.** In its own townships it decides landscaping, tree planting and covered walkways, especially in new phases.
- **Caution.** Press reports describe Elmina as already having extensive walking and cycling tracks (unverified). The pitch must show a gap SDP would recognise, such as shade, not paths.

## 5. What already exists, and how Teduh differs

| Existing tool | What it does | Gap Teduh targets |
|---|---|---|
| [Cool Walks](https://www.ecowatch.com/cool-walks-app-barcelona-2653527112.html) (Barcelona) | Resident app routing through shade, using LIDAR and sun position | Resident navigation, not planner decisions |
| [Undercover](https://www.hack.gov.sg/2026/undercover/) (Singapore) | Hackathon prototype comparing shortest, shadiest and balanced routes | Prototype; no sign of a public launch |
| [Tree Equity Score](https://americanforests.org/our-work/tree-equity-score) (US) | Neighbourhood canopy-gap score, weighted by demographic need | Need weights are demographic, not footfall; not tropical |
| [UCLA / American Forests Shade Map](https://innovation.luskin.ucla.edu/2025/06/02/national-shade-map-from-ucla-and-american-forests-launched-to-combat-deadly-urban-heat) | Maps existing shade in 101 US urban areas | Shows what exists, not where to add it |
| [Cooling Singapore digital twin](https://asianews.network/?p=149980) | National-scale heat-policy simulation | Research-grade; not a developer's township tool |

I found no Malaysian township equivalent. That is not proof none exists.

**Differences we would claim:**
1. Need is weighted by **footfall to daily destinations and transit**, not demographics.
2. Both **sun and rain cover** count, which matters in the tropics.
3. A **what-if mode** lets planners test trees, covered walkways and building orientation for new phases.
4. Each priority segment gets a **fast option and a long-term option**, because newly planted trees give little early shade.

## 6. Concept in brief

1. **Core: a shade-priority score.** Each street segment is ranked by heat exposure × people served × shade gap. The output is a "fix these first" list and map.
2. **What-if mode (design stage).** Planners test interventions on a new phase and see the comfort and shade effect.
3. **Intervention options.** Fast (shade sails, extended covered walkways, bus-stop shelters) and long-term (trees), with rough cost ranges.
4. **Optional resident views.** A public "shade plan" map, and a before/after route demo. A full navigation app is out of scope.

**Inspirations**
- **Medellín's Green Corridors.** City figures report corridor air temperatures falling from 31.6 °C to 27.1 °C (2016-2019); the widely quoted citywide figure is about 2 °C. Sources do not reconcile the two ([Scroll](https://scroll.in/article/1067528/how-a-colombian-citys-green-corridors-turned-the-clock-back-on-global-warming)).
- **Barcelona's climate shelters.** About 500 shelters, with 99% of residents within a 10-minute walk of one (city figures; counts vary by source).
- **Ant trails.** Ants reinforce short routes and let long ones fade, an idea used in route-optimisation algorithms. In Teduh it inspires a footfall model that sends simulated walkers between homes and destinations.
- **Termite mounds / Eastgate Centre (Harare).** Passive cooling through airflow. For streets, the parallel is ventilation-corridor alignment, an optional extra. Energy-saving claims vary from 10% to 35% across sources, so avoid a headline figure.

## 7. Known limits

- **It serves planners first.** Residents see benefits only after construction. This is normal for planning tools, but the pitch must state user and beneficiary separately.
- **Trees take years to give shade.** Do not promise canopy benefits early; lead with fast options.
- **Impact is modelled.** Without a built pilot, outcomes such as "shaded kilometres to transit" are estimates.
- **No field validation.** The team cannot visit a township, so evidence rests on public data and an online survey.
- **Shade accuracy depends on building-height data.** Not yet confirmed as available for Malaysian townships.
- **Open scoring call.** My scoring put Teduh at about 71% against flood at 70%, which is within the margin of error. See [OTHER_IDEAS.md](OTHER_IDEAS.md).

## 8. Fit with our team

| Member | Contribution |
|---|---|
| Architecture student | Shade structures, orientation, tree and walkway options; what-if mode; visuals |
| Mechanical engineer | Comfort and heat-transfer logic; checking model outputs against published studies |
| Electrical engineer (vibe coding) | Data pipeline, scoring, app and demo; optional low-cost temperature/humidity logger for model checks |

**Gaps:** GIS and remote-sensing experience; business case and pitch ownership; landscape and tree-species knowledge.

## 9. Questions for the team

1. Do we agree that a planner tool, not a resident app, is the product?
2. Is shade a strong enough pain, or should the online survey decide between this and another idea?
3. Who owns the pitch and business case?
4. Which SDP township do we use as the example?
