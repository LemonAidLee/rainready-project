# Online-Only Decision: Which Problem Should We Target?

> **Superseded (10 Oct 2026).** This recommended the shade tool (CoolPath/Teduh) on a near-tie with flood. Later findings (umbrella objection; documented flooding at Bandar Bukit Raja) moved the team to the flood idea. See [../documentation/PROJECT_STATUS.md](../../documentation/PROJECT_STATUS.md). Evidence tables here remain useful.

Prepared 10 October 2026. Constraint: **no site visits or interviews**, so every claim must be backed by public sources and the prototype must run on public data. Builds on [EVIDENCE_ANALYSIS.md](EVIDENCE_ANALYSIS.md). Proposal deadline: **23 October 2026, 11:59 p.m.**

---

## 1. Recommendation

**Target: CoolPath, a spatial decision tool that shows where shade will do the most good on the walking routes people use to reach daily destinations and transit.** Frame it under **Planet → Climate resilience** (it also touches People → Mobility).

**Runner-up and fallback: flood/drain readiness (RainReady).** It has the strongest pain evidence, but it scores lower on township actionability and on what we can credibly demonstrate without ground data.

This is a **near tie** on my scoring (section 4: 71% vs 70%), so treat the choice as a judgement call. Reasons the tie breaks toward CoolPath:

1. **We can build a real demo with no fieldwork.** Satellite surface temperature, tree/vegetation indices, street orientation and destinations can all be computed remotely for an actual SDP township.
2. **Street orientation is computable and matters.** A Kuala Lumpur study found east-west and north-west/south-east roads had PET 41-43 °C against 37 °C for other orientations, and dense canopy cut PET by 25% ([Zaki et al. 2020](https://www.mdpi.com/2071-1050/12/3/1053)).
3. **It matches the kind of problem SDP already names.** The briefing's Planet examples include "selecting the most suitable sites for solar installations", a siting/prioritisation problem. CoolPath is the same shape.
4. **The flood evidence is strong nationally, but weaker for a township tool.** Losses are dominated by monsoon river floods outside any township's control (section 3). Drains are mostly council assets. A flood demo without drain or sensor data would rest on synthetic inputs.

**What would change my mind:** if the team has hydrology/GIS-flood skills and can get real drainage data for an SDP township (for example from SDP's development engineers), flood becomes the better choice.

---

## 2. Compiled online evidence

### 2.1 Heat and walking (CoolPath)

| Finding | Source | Strength | Limitation |
|---|---|---|---|
| Dense roadside canopy (sky view factor 0.07) reduced mean radiant temperature 35% and PET 25% on KL roads; E-W and NW-SE roads reached PET 41-43 °C vs 37 °C | [Zaki et al. 2020, Sustainability](https://www.mdpi.com/2071-1050/12/3/1053) | Medium (4 roads, KL) | Percentages only; baseline temperatures not seen in the abstract |
| 28 heat-related illnesses and 1 death by 25 Mar 2024; 37 cases and 2 deaths by early April; Selangor 3 cases | [MOH via Malay Mail](https://www.malaymail.com/amp/news/malaysia/2024/03/26/health-ministry-28-heat-related-illnesses-one-death-recorded-as-of-march-25/125630); [NADMA via NST](https://www.nst.com.my/amp/news/nation/2024/04/1034601/three-year-old-child-dies-due-heat-stroke-nadma) | Medium (official) | **Counts are small.** Do not pitch this as a casualty crisis |
| MetMalaysia Level 1 heat alert (35-37 °C for 3+ days) covered Gombak and Petaling in Oct 2024 | [Says](https://says.com/my/news/metmalaysia-issues-level-1-heat-alert-for-17-areas-including-kl-petaling) | Medium | Alerts, not exposure data |
| Shaded pedestrian lanes: 59.7% sufficient, 20.8% insufficient, 14.3% not available but needed (n=558, 2016-17) | [BES 2018](https://www.besjournal.com/en/article/doi/10.3967/bes2018.095) (source 8) | Low-Medium | Dated; landline sample |
| Heat named a walking barrier by 48% (n=60, 2021, online) | Source 10 | Low | Tiny sample |
| Most people willing to walk under 10 minutes or 500 m to a station (n=325) | Source 3 | Medium | Stated preference |
| Proposal that ~3 minutes / 240 m is a thermally comfortable walking radius | [UTM paper via UKM repository](https://ptsldigital.ukm.my/handle/123456789/772699?mode=full) | Low (proposal) | Not a survey |
| 90% of 51 delivery riders said work conditions had become hotter | [Aliran](https://m.aliran.com/web-specials/on-the-road-in-rising-heat-the-daily-reality-of-malaysias-delivery-riders) | Low | n=51; riders, not residents |
| Tel Aviv study: shaded space strongly tracked pedestrian use of shade | [Building & Cities 2025](https://reference-global.com/article/10.5334/bc.574) | Low (non-Malaysian) | Context only |
| 2023 KL thermal-comfort study (n=1,157) and 2025 Shah Alam study (n=264) recommend more shade/greenery | Atmosphere 2023; UiTM colloquium 2025 (from search) | Medium | Neither measures pedestrian shade directly; full papers not read |

**Gap:** I found no survey measuring how many Malaysians avoid walking because of heat. The claim must be framed as comfort and route choice, not as proven avoidance.

### 2.2 Flood and drainage (RainReady)

| Finding | Source | Strength | Limitation |
|---|---|---|---|
| 2025 flood losses RM636.9m (2024: RM933.4m); living-quarters losses RM183.8m (2024: RM372.2m) | [DOSM](https://www.dosm.gov.my/portal-main/release-content/special-report-on-impact-of-floods-in-malaysia2025); [Malay Mail](https://www.malaymail.com/news/malaysia/2026/04/15/flood-losses-ease-malaysias-damage-bill-drops-from-rm9334m-in-2024-to-rm6369m-in-2025/216414) | High | **Losses fell in 2025.** Largest 2025 state losses were Johor RM72.1m, Terengganu RM71.8m, Kelantan RM67.1m; Selangor RM26.6m |
| 1,597 flash-flood hotspots nationally; 145 eliminated in 2025 | [Newswav (KPKT)](https://newswav.com/article/nga-145-flash-flood-hotspots-eliminated-in-2025-A2607_jkWCqz) | Medium-High | Press report; locations not seen |
| At least 15 DBKL-recognised flash-flood hotspots in KL; Dec 2025 flash floods | [The Vibes](https://www.thevibes.com/articles/news/116515/flash-floods-hit-kuala-lumpur-as-torrential-rain-overwhelms-urban-drainage-systems) | Medium | News |
| Recurring Shah Alam/Klang floods: Nov 2022 attributed to heavy rain and clogged drains; Nov 2025 flooded Taman Desa Kemuning, Taman Sri Lembayung and others | [FMT 2022](https://www.freemalaysiatoday.com/category/nation/2022/11/10/klang-shah-alam-hit-by-flash-floods); [FMT 2025](https://www.freemalaysiatoday.com/category/nation/2025/11/24/morning-downpour-causes-floods-in-shah-alam) | Medium | 2025 report names no drain cause; Elmina not named |
| Deputy minister (2024): most flash floods are due to sanitation issues such as clogged drains | [The Sun](https://thesun.my/?p=186743) | Medium | Not re-verified for 2025 |
| About two-thirds (~RM4bn) of 2021 flood losses were uninsured; flood cover is usually an optional rider | [Insurance Business](https://www.insurancebusinessmag.com/asia/news/catastrophe/bank-negara-malaysia-flags-low-flood-cover-even-in-repeathit-areas-564091.aspx) | Medium-High | 2021 |
| DOSM Klang survey after the 2021 floods (press): average damage RM14,058; 34.2% had emergency savings under RM1,000 | Press report; case study slides at [DOSM](https://v2.dosm.gov.my/uploads/files/mystats-conference/2024/scientific-papers/11-Slide-The-Impacts-of-Losses-and-Damages-by-Floods-A-Case-Study-in-Klang-Selangor.pdf) | Medium | DOSM says not an official statistic; confirm figures in the slides |
| SDP calls the 2021 floods a "wake-up call" and uses 180 acres of Bandar Bukit Raja wetlands and its town park as flood retention | [SDP](https://www.simedarbyproperty.com/sustainability/urbanbiodiversity/spotlight-bandar-bukit-raja.html) | Medium | Undated page; no outcome data |

**Counter-evidence:** national losses are falling; the biggest losses are on the east coast and Johor; and most drain assets belong to councils.

### 2.3 Other candidates (online evidence)

| Candidate | Best online evidence | Weakness |
|---|---|---|
| Maintenance / issue triage | Subang Jaya council: ~29,000 complaints in 2024, mostly street lights and landscaping ([Malay Mail](https://malaymail.com/news/malaysia/2024/12/14/subang-jaya-city-council-says-received-nearly-30000-complaints-from-residents-mostly-over-faulty-street-lights-and-landscaping/159808)); Johor Bahru 2022: 18,038 complaints, top categories trees, lighting, road damage ([Kosmo](https://www.kosmo.com.my/2023/01/02/persekitaran-kotor-lampu-jalan-rosak-antara-18038-aduan-diterima-mbjb/)) | Shows volume, not resolution delays or unmet need; council apps already exist |
| Strata arrears | 5,291 of 5,675 tribunal cases (93%) were maintenance-fee arrears, 2019 ([MIEA](https://miea.com.my/node/2736)) | 2019; strata-focused; SDP is largely landed |
| Waste / recycling | 37.9% national recycling rate in 2024 vs 40% target ([Asia News Network](https://asianews.network/40-of-malaysias-trash-is-recyclable/)) | Crowded; briefing already uses it as an example |
| Last-mile transit | Prasarana 2025 ridership 1.31m/day, +11% ([Carz](https://www.carz.com.my/2026/01/prasarana-ridership-jumps-11-in-2025)); minister says landed estates are hard to serve | A government programme already targets this |
| Walkability (general) | See EVIDENCE_ANALYSIS.md | Thin barrier prevalence; SDP/Elmina already promoted as walkable ([EdgeProp](https://www.edgeprop.my/content/1185552/world-class-city-underpinned-sustainability-wellness-and-liveability-making), unverified) |

---

## 3. What the data cannot tell us (important for the pitch)

- Whether SDP township residents specifically avoid walking in heat.
- Whether drains in any SDP township are actually blocked or undersized.
- Whether SDP already has shade or drainage inventories (ask through the official Telegram channel; no site visit needed).

State these openly as assumptions to be validated in the pilot. Judges reward honest caveats more than overclaims.

---

## 4. Scoring (my judgement; adjust if you disagree)

Weights follow the judging criteria. Scores are 1-5. "Evidence" is how well the problem can be verified online.

| Criterion (weight) | CoolPath | Flood | Maintenance triage | Waste | Walk audit |
|---|---:|---:|---:|---:|---:|
| Impact (25) | 3 | 3 | 3 | 3 | 3 |
| Innovation (20) | 4 | 3 | 2 | 2 | 2 |
| Feasibility without fieldwork (20) | 4 | 3 | 4 | 4 | 3 |
| Strategic fit (15) | 4 | 5 | 4 | 3 | 4 |
| Commercial value (10) | 3 | 3 | 3 | 2 | 2 |
| Verifiable evidence (10) | 3 | 5 | 2 | 3 | 3 |
| **Weighted total (of 500)** | **355 (71%)** | **350 (70%)** | **305 (61%)** | **290 (58%)** | **285 (57%)** |

Why flood impact is 3, not 4: its large losses are mostly river floods outside township control. Why CoolPath impact is 3: harm is comfort and route choice, not a measured casualty burden. **The top two are within my margin of error.**

---

## 5. Pitch framing for CoolPath

**Problem statement:** Township managers and residents cannot see which walking routes to daily destinations and transit are hottest and least shaded, so shade and tree planting is placed by guesswork, leaving short trips uncomfortable and car-dependent.

**Users:** SDP township and landscape/planning teams (decision-maker); residents who make short trips (beneficiary).

**Prototype (all from public data):**
1. Pick one SDP township (public masterplan boundary).
2. Layers: surface temperature (Landsat), vegetation (Sentinel-2), street orientation and building heights (OpenStreetMap), destinations and bus/rail stops (OSM and the national public-transport GTFS feed).
3. Score each street segment: heat exposure × number of destinations/stops served × shade deficit.
4. Output a ranked "first 20 segments to shade" list, and a before/after estimate using the published canopy-PET relationship.

**Measurable outcomes:** share of priority segments above a comfort threshold; kilometres of shaded route to transit stops; trees planted per priority segment.

**Feasibility and scale:** reuse the pipeline on any township; value to SDP through the urban biodiversity and climate resilience pillars of its 2025-2030 strategy.

---

## 6. Online-only work plan (13 days)

| Days | Work |
|---|---|
| 1-2 | Download and read Zaki et al. 2020 in full and the BES 2018 results; confirm the data layers load for the chosen township. Ask SDP via Telegram whether tree/shade or drainage inventories exist. |
| 3 | **Decision gate:** if the heat layer cannot be built, or SDP shares real drainage data, switch to flood. |
| 4-8 | Build the scoring and map; sanity-check by looking at satellite/street imagery. |
| 9-11 | Impact estimates with stated assumptions; deck; 5-minute demo. |
| 12-13 | Appendix of sources; test links signed out; submit. |

---

## 7. Claims safe and not safe

**Safe:**
- Dense canopy cut PET by about 25% in a KL study; road orientation changed PET from 37 °C to 41-43 °C (Zaki et al. 2020).
- Walkers are willing to walk about 10 minutes or 500 m to stations (source 3).
- MOH recorded heat-related illnesses and 2 deaths in 2024 (state counts and call them small).
- Heat alerts have covered Selangor districts such as Gombak and Petaling.
- Walkable-city guidelines and shaded-lane design guidance exist (PLANMalaysia).

**Not safe:**
- "Malaysians avoid walking because of heat" (no survey found).
- "Heat is the main walking barrier" (sources 8 and 10 do not show this).
- Any Elmina or SDP township claim without checking SDP's own materials.
- Flood loss figures as proof of township flood risk.
- Any percentage combined across sources.
