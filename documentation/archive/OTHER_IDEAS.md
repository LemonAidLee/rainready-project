# Other Ideas Considered

> **Status (10 Oct 2026):** the team chose flood and drainage at Bandar Bukit Raja. Flood evidence here predates the township gap analysis; see [TOWNSHIP_GAP_ANALYSIS.md](../supporting/TOWNSHIP_GAP_ANALYSIS.md) and [PROJECT_STATUS.md](../PROJECT_STATUS.md). The scores below are older and used before the BBR evidence was found.

Alternatives to [Teduh](TEDUH_BACKGROUND.md), kept short so the team can compare. Evidence confidence: **H** high, **M** medium, **L** low. Scores are the analysis's own judgement, not the judges', and the top few are within the margin of error.

---

## How the ideas compare

Weights follow the judging criteria. Scores are 1-5. "Evidence" means how well the problem can be verified online. Full table: [ONLINE_ONLY_DECISION.md](../../research/archive/ONLINE_ONLY_DECISION.md).

| Idea | Impact (25) | Innovation (20) | Feasibility (20) | Fit (15) | Commercial (10) | Evidence (10) | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Teduh (shade)** | 3 | 4 | 4 | 4 | 3 | 3 | **71%** |
| Flood / drain readiness | 3 | 3 | 3 | 5 | 3 | 5 | **70%** |
| Maintenance and "who owns this?" | 3 | 2 | 4 | 4 | 3 | 2 | **61%** |
| Waste / recycling | 3 | 2 | 4 | 3 | 2 | 3 | **58%** |
| Walking route audit | 3 | 2 | 3 | 4 | 2 | 3 | **57%** |
| Haze / air quality | 3 | 2 | 3 | 3 | 2 | 4 | **~56%** |

---

## 1. Flood and drain readiness ("RainReady")

**Problem:** Township managers and residents learn about drain blockages and flood risk too late, causing property damage that is often uninsured.

**Evidence**
- 2025 flood losses were RM636.9m (2024: RM933.4m) ([DOSM](https://www.dosm.gov.my/portal-main/release-content/special-report-on-impact-of-floods-in-malaysia2025)). **H**
- 1,597 flash-flood hotspots nationally; 145 eliminated in 2025 ([KPKT via Newswav](https://newswav.com/article/nga-145-flash-flood-hotspots-eliminated-in-2025-A2607_jkWCqz)). **M-H**
- About two-thirds of 2021 losses were uninsured ([Bank Negara via Insurance Business](https://www.insurancebusinessmag.com/asia/news/catastrophe/bank-negara-malaysia-flags-low-flood-cover-even-in-repeathit-areas-564091.aspx)). **M-H**
- Shah Alam and Klang flood repeatedly, e.g. [November 2025](https://www.freemalaysiatoday.com/category/nation/2025/11/24/morning-downpour-causes-floods-in-shah-alam). **M**
- SDP calls the 2021 floods a "wake-up call" and uses wetlands and its town park at Bandar Bukit Raja as retention ([SDP](https://www.simedarbyproperty.com/sustainability/urbanbiodiversity/spotlight-bandar-bukit-raja.html)). **M**

**Concept:** a pre-storm tool that combines rainfall forecasts, low-lying areas and drain condition to rank which drains to clear first, with optional low-cost water-level sensors in retention ponds.

**Fit:** Strongest SDP strategy fit (climate resilience). Best skills match for the team: hydraulics (mechanical), sensors (electrical), retention-space design (architecture).

**Risks:** Losses fell in 2025 and are dominated by river floods outside any township's control; Selangor's 2025 loss was only RM26.6m. Drains mostly belong to councils. Without real drainage data the demo would use synthetic inputs.

**Choose it if:** SDP can share real drainage data, or the team wants a hardware prototype.

---

## 2. Maintenance and "who owns this?"

**Problem:** Residents do not know whom to contact about a broken street light, a blocked drain or a damaged path, so reports reach the wrong agency and wait.

**Evidence**
- The briefing lists this as an example (difficulty knowing whom to contact or track public-asset issues).
- About 29,000 complaints in Subang Jaya in 2024, mostly street lights and landscaping ([Malay Mail](https://malaymail.com/news/malaysia/2024/12/14/subang-jaya-city-council-says-received-nearly-30000-complaints-from-residents-mostly-over-faulty-street-lights-and-landscaping/159808)); 18,038 in Johor Bahru in 2022, led by trees, lighting and road damage ([Kosmo](https://www.kosmo.com.my/2023/01/02/persekitaran-kotor-lampu-jalan-rosak-antara-18038-aduan-diterima-mbjb/)). **M**
- Strata maintenance-fee arrears were 93% of 2019 tribunal cases ([MIEA](https://miea.com.my/node/2736)); dated and strata-focused. **M**

**Concept:** an ownership router that identifies who is responsible for each fault (SDP, council or TNB), tracks it to resolution and shows SDP where faults repeat.

**Fit:** Cleanest tie to the briefing and the "after residents move in" theme. Fastest to build.

**Risks:** Complaint apps already exist, so innovation is hard. Volume figures do not show unmet need. Mostly software, so it uses the mechanical engineer less.

**Choose it if:** the team wants the quickest build and a direct link to the briefing.

---

## 3. Waste and recycling

**Problem:** Residents are unsure what to recycle and where, so recycling stays below target.

**Evidence**
- The national recycling rate was 37.9% in 2024 against a 40% target ([Asia News Network](https://asianews.network/40-of-malaysias-trash-is-recyclable/)). **M**
- The briefing lists confusion about recycling rules and collection points as an example.
- No resident compliance survey found.

**Concept:** township-specific collection-point guidance, possibly with smart bins or sorting checks.

**Fit:** Good hardware angle for both engineers.

**Risks:** Crowded space; innovation is the hardest criterion to win. Weaker evidence of resident pain.

**Choose it if:** the team has a specific, differentiated hardware idea.

---

## 4. Walking route audit (general walkability)

**Problem:** Short trips on foot fail because routes are discontinuous, unsafe or uncomfortable.

**Evidence:** Broad but thin. National baselines are solid (Ipsos 77% vs 5% walking; NHMS 84%), but barrier prevalence comes from small or dated studies. Pedestrians were 285 of 4,837 road deaths in Jan-Sep 2024 (5.9%), while motorcyclists were 68%. Full review: [EVIDENCE_ANALYSIS.md](../../research/archive/EVIDENCE_ANALYSIS.md).

**Concept:** audit routes between homes, schools and transit for continuity, lighting, crossings and accessibility.

**Fit:** Moderate. Elmina is already promoted as walkable (unverified).

**Risks:** Generic and easy to copy; it needs site audits the team cannot do. Teduh is the narrowed, better-evidenced form of this idea.

---

## 5. Haze and air quality

**Problem:** Residents face unhealthy air during haze with little local information or refuge.

**Evidence**
- Haze is current: Batu Pahat closed schools on 7 October 2026 and 35 areas were unhealthy ([Malay Mail](https://www.malaymail.com/amp/news/malaysia/2026/10/07/haze-education-ministry-orders-state-and-district-education-offices-schools-to-monitor-haze-act-based-on-api-readings/238138)); Sarawak shut 591 schools in August ([The Vibes](https://www.thevibes.com/articles/news/126388/sarawak-haze-shuts-591-schools-across-10-districts)). **M-H**
- Klang Valley has had local-fire haze, not only transboundary ([NST 2016](https://nst.com.my/amp/news/2016/04/140867/klang-valley-haze-due-forest-peat-fires)). **M**
- 32,000 avoidable deaths a year is a modelled national estimate, not recorded deaths ([CREA](https://energyandcleanair.org/?p=3282)). **L-M**

**Concept:** township-level sensing and exposure guidance, or "clean-air refuge" spaces.

**Fit:** Weak SDP fit (not one of its four pillars). DOE already publishes the Air Pollutant Index hourly across 68 stations.

**Risks:** SDP cannot stop haze; it is seasonal and episodic; alert apps are crowded; sensors need calibration. Better kept as a possible extension of Teduh.

---

## 6. Weaker candidates

| Idea | Why it's weak |
|---|---|
| Parking guidance | The briefing names it, but I found no resident survey; crowded |
| Parcel collection | Only a 2019 survey (43% unhappy with delivery) and commentary |
| Neighbourhood connection | 14% of Malaysians feel lonely (2023 Meta-Gallup); no urban-cohesion survey; hard to measure impact |
| Security / safety | Gated-community fear-of-crime studies from 2011 and 2013 only |
| Strata arrears | Strong but 2019 data, strata-focused, while SDP is mostly landed |

---

## 7. How we could decide as a team

1. **Run the online resident survey.** Ask residents to rank heat, flooding, parking, waste and maintenance. The result is evidence none of these documents can provide.
2. **Check what SDP will share.** If drainage data is available, flood rises. If landscape and masterplan data is available, Teduh rises.
3. **Weigh team strength.** Flood suits a hardware-heavy team; Teduh suits a design-and-data team.

Caveat on all of the above: no idea has field validation, and the judges' scores will differ from ours.
