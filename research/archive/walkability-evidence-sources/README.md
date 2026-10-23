# Malaysia Township Walkability Evidence Pack

Collected on **10 October 2026** for problem validation and independent analysis. This pack supports the working question:

> Would improving safe, continuous, shaded, accessible walking routes and first/last-mile connections solve a repeated problem for a broad group of Malaysian township residents?

Start with `CLAUDE_ANALYSIS_PROMPT.md`, then give Claude this whole folder. The numbered files follow the table below.

## Quick conclusion from the evidence

The strongest cross-source pattern is not simply “Malaysians dislike walking.” National mobility data show very low walking and strong private-vehicle dependence, while local studies repeatedly report unsafe traffic, incomplete or obstructed paths, poor crossings, heat/rain exposure, weak lighting, maintenance, security, and disconnected destinations. Social-media discussions echo these barriers, but are qualitative and cannot establish prevalence.

The defensible problem statement is therefore:

> **Residents who need or want to make short local trips cannot reliably do so on foot because routes are unsafe, discontinuous, uncomfortable in Malaysia’s climate, and poorly connected to destinations and public transport.**

This is a well-supported direction for further validation, not proof that a particular prototype will work. Before committing to a solution, identify one township and verify which route, user group, and barrier causes the most frequent or severe harm.

## Source inventory

| # | Local file | Source and coverage | What it contributes | Evidence role / limitation |
|---|---|---|---|---|
| 1 | [`01_ipsos_mobility_monitor_2026.pdf`](../coolpath-sources/context/01_ipsos_mobility_monitor_2026.pdf) | [Ipsos Malaysia Mobility Monitor press release](https://www.ipsos.com/en-my/ipsos-press-release-mobility-monitor); representative Malaysian adult sample, n=500 | 77% name private vehicles as their main mode, 5% walking; 55% say limited options make destinations hard to reach; strong road-safety concern | Current national survey; useful for scale, but n=500 and broad mobility questions do not diagnose a particular township |
| 2 | [`02_dbkl_bike_ped_masterplan_official_catalogue.html`](02_dbkl_bike_ped_masterplan_official_catalogue.html) and [`02b_dbkl_masterplan_public_copy.md`](02b_dbkl_masterplan_public_copy.md) | [DBKL Infrastructure Planning Department](https://www.dbkl.gov.my/en/departments/jabatan-perancangan-infrastruktur); KL Pedestrian and Cycling Master Plan 2019–2028 catalogue and public-copy record | Establishes policy relevance; the plan reports public-consultation priorities including safer routes, lighting/security, separation from vehicles, enforcement, shade, rest, and path comfort | Official provenance, but the masterplan download was disabled at collection time; third-party reader must be verified against an official copy |
| 3 | [`03_bangsar_shah_alam_active_transportation.pdf`](../coolpath-sources/core/03_bangsar_shah_alam_active_transportation.pdf) | [Frontiers article](https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2022.925956/full); stratified survey of Bangsar and Shah Alam residents, n=325 | High importance assigned to safe and comfortable walkways and good weather; willingness concentrates on short distances; many report safety concerns | Peer-reviewed local evidence; two urban areas, self-reported preferences |
| 4 | [`04_green_township_neighbourhood_satisfaction.md`](04_green_township_neighbourhood_satisfaction.md) | [Author-copy record](https://www.researchgate.net/publication/277307936_Neighbourhood_satisfaction_responses_from_residents_of_green_townships_in_Malaysia); one green township, 190 returned questionnaires | Connectivity/accessibility and environmental quality predict neighbourhood satisfaction; security and participation were weaker areas | Peer-reviewed, but single township and cross-sectional; PDF blocked by host |
| 5 | [`05_bandar_sunway_walkability_trid.html`](../coolpath-sources/context/05_bandar_sunway_walkability_trid.html) | [TRID record](https://trid.trb.org/View/2259777); Bandar Sunway GIS/street-audit study | Identifies street connectivity and land-use diversity as factors that make some areas more walkable than others | Bibliographic/abstract snapshot, not the complete paper |
| 6 | [`06_kampung_morten_walking_suitability_2025.pdf`](../coolpath-sources/context/06_kampung_morten_walking_suitability_2025.pdf) | [UTHM paper](https://publisher.uthm.edu.my/periodicals/index.php/mari/article/download/17192/6189/116102); Kampung Morten, n=91 plus WABSA audit | Short trips are made on foot, while missing/poor sidewalks, lighting and curb ramps reduce suitability | Recent site-specific survey and audit; small sample |
| 7 | [`07_putrajaya_subjective_walkability_2018.pdf`](07_putrajaya_subjective_walkability_2018.pdf) | [MUET journal PDF](https://publications.muet.edu.pk/index.php/muetrj/article/download/516/230/); three Putrajaya neighbourhoods using an abbreviated NEWS instrument | Residents in objectively more walkable areas generally rate their environment more favourably; also highlights subjective/objective mismatch | Peer-reviewed place comparison; older and limited to Putrajaya |
| 8 | [`08_greater_kl_urban_heat_needs_assessment.html`](../coolpath-sources/core/08_greater_kl_urban_heat_needs_assessment.html) | [Greater Kuala Lumpur heat-needs study](https://html.rhhz.net/SWYXYHJKX/html/t20181024_195618.htm); Mont Kiara, Jalan Raja Chulan and Setia Alam, n=558 | Supports shade and pedestrian-lane needs in a hot urban environment | Direct climate-comfort evidence, but only three sites |
| 9 | [`09_kl_walking_health_belief_study.md`](../coolpath-sources/context/09_kl_walking_health_belief_study.md) | [Author-copy record](https://www.researchgate.net/publication/263078668_Using_a_Health_Belief_Model_to_investigate_the_walking_behaviour_of_residents_living_in_Kuala_Lumpur_Malaysia); 478 returned surveys plus 30 interviews | Identifies heat/weather, unsafe traffic, crime, stray dogs, time, attitudes and health as walking constraints | Strong mixed-method diagnostic evidence, but older data, low response rate, and PDF blocked by host |
| 10 | [`10_klang_valley_walkable_environment_post_pandemic.pdf`](../coolpath-sources/core/10_klang_valley_walkable_environment_post_pandemic.pdf) and [`10_article_page.html`](10_article_page.html) | [Environment-Behaviour Proceedings Journal](https://ebpj.e-iph.co.uk/index.php/EBProceedings/article/view/3259); online survey in selected Klang Valley neighbourhoods | Frequently reported barriers include heat, missing/bad sidewalks, traffic, poor lighting, maintenance, and destinations that are not walkable | Useful recent local pattern; small/non-probability online survey and pandemic context |
| 11 | [`11_nhms_2023_key_findings.pdf`](../coolpath-sources/context/11_nhms_2023_key_findings.pdf) | [Ministry of Health / Institute for Public Health](https://iku.nih.gov.my/images/nhms2023/key-findings-nhms-2023.pdf); national health survey | 1 in 3 adults physically inactive; 84% do not walk or cycle for transport; 1 in 2 lead sedentary lifestyles; also documents functional limitations | Strong national health baseline; does not show that walkability alone causes inactivity |
| 12 | [`12_mot_pedestrian_road_safety_2024.pdf`](12_mot_pedestrian_road_safety_2024.pdf) | [Ministry of Transport parliamentary answer](https://www.mot.gov.my/en/SiteCollectionImages/ParlimenNew/2024/Dewan%20Rakyat/Penggal%203/Mesyuarat%20Ketiga/FINAL%20-%20BJL%20-%201%20-%20ALOR%20SETAR%20-%20MKJR%20ADVOKASI.pdf) | Reports 285 pedestrian deaths from January–September 2024 and describes road-safety action | Authoritative administrative figure; fatalities capture only the most severe outcomes |
| 13 | [`13_uitm_melaka_pedestrian_satisfaction.pdf`](13_uitm_melaka_pedestrian_satisfaction.pdf) | [UiTM repository](https://ir.uitm.edu.my/id/eprint/51435/1/51435.pdf); Jalan Tun Khalil Yaakob, Bandar Hilir, Melaka; Google Form shared via WhatsApp and Instagram | Reports dissatisfaction linked to unsafe pedestrian design, inadequate street furniture, and lack of shade | Direct local/user evidence, but convenience/social-media recruitment limits representativeness |
| 14 | [`14_planmalaysia_walkable_guidelines_catalogue.html`](14_planmalaysia_walkable_guidelines_catalogue.html) | [PLANMalaysia guideline catalogue](https://www.planmalaysia.gov.my/main/document-list?frontendpage=document-list&page=3&params=&per-page=12&q=%2Fmain%2Fdocument-list&type=garis-panduan-perancangan) | Confirms that walkable-city guidance is part of Malaysia’s formal planning framework | Policy source, not evidence of residents’ pain or implementation quality |
| 15 | [`15_planmalaysia_healthy_walkable_city_guidelines.pdf`](../coolpath-sources/context/15_planmalaysia_healthy_walkable_city_guidelines.pdf) | [PLANMalaysia Healthy Walkable City guideline](https://stag.planmalaysia.gov.my/planmalaysia/modules_resources/database_stores/17/46_25.pdf), 128 pages | Provides official design and implementation principles against which a proposal can be checked | Normative guidance rather than an outcome evaluation |
| 16 | [`16_reddit_better_walking_cycling_infrastructure.md`](../coolpath-sources/context/16_reddit_better_walking_cycling_infrastructure.md) | [r/Malaysia discussion](https://www.reddit.com/r/malaysia/comments/1fdjulu) | Lived-experience themes: willingness, path continuity, crossings, shade/rain, enforcement, motorcycles, hills and first/last mile | Qualitative, self-selected social-media evidence only |
| 17 | [`17_reddit_malaysians_least_active_walkers.md`](../coolpath-sources/context/17_reddit_malaysians_least_active_walkers.md) | [r/Malaysia discussion](https://www.reddit.com/r/malaysia/comments/1hyq22v) | Lived-experience themes: car-oriented roads, damaged/blocked paths, driver behaviour, public transport, climate and social norms | Qualitative, self-selected social-media evidence only |
| 18 | [`18_reddit_walking_rm300b_discussion.md`](18_reddit_walking_rm300b_discussion.md) | [r/Malaysia discussion](https://www.reddit.com/r/malaysia/comments/1p7r4j8) | Lived-experience themes: missing paths/crossings, obstructions, darkness, uneven surfaces, public transport and disagreement about policy | Qualitative only; does not validate the linked article’s monetary claim |

## Evidence hierarchy

Use the files with different weights:

1. **National scale and severity:** sources 1, 11 and 12.
2. **Direct local diagnosis:** sources 3, 4, 6, 7, 8, 9, 10 and 13.
3. **Policy and design feasibility:** sources 2, 14 and 15.
4. **Discovery of lived-experience themes:** sources 16–18 only.

Convergence across these layers is meaningful, but it does not make the combined material a representative township survey. Avoid adding percentages across studies, because populations, dates, instruments and sampling methods differ.

## Important gaps to investigate

- Which exact township and which 500–1,000 metre routes have the largest unmet need?
- Who is most affected: schoolchildren, older adults, people with disabilities, transit users, women travelling after dark, lower-income residents, or nearby workers?
- How often do residents abandon, reroute, or replace a walking trip because of each barrier?
- Are the worst failures missing infrastructure, maintenance/obstruction, enforcement, personal safety, climate protection, or destination distance?
- What current municipal complaint, crash, footfall, accessibility, transit-ridership or GIS data exist for the chosen location?
- What intervention is within the competition team’s scope and can produce a measurable outcome?

## Recommended validation threshold

Before selecting a solution, require at least:

- one strong national/official source showing scale or severity;
- two independent local studies showing the same barrier;
- one site-specific observation, audit, or administrative dataset for the selected township; and
- a small amount of direct current user evidence, even if only five short intercept interviews or a tightly targeted survey.

Online sources reduce discovery time, but they cannot fully replace current evidence from the exact users and route the project will serve.

## File integrity and access notes

- All nine local PDF files were checked for the `%PDF-` signature and successfully parsed for page counts.
- HTML files are snapshots and may contain navigation/scripts in addition to the article or catalogue content.
- Sources 4 and 9 have detailed records rather than PDFs because ResearchGate blocked automated access.
- Sources 16–18 have analytical source records rather than full thread archives because Reddit blocked automated download.
- Source 2’s public reader copy could not be archived due to anti-bot protection; the official DBKL catalogue snapshot is included.
- Respect each publisher’s copyright and licence. These files are for research and competition analysis, not redistribution.
