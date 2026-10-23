# RainReady v2: One Shared Picture, Two Doors

**Written for:** the whole team. **Status:** proposal from the 20 Oct 2026 brainstorm, for the team to confirm.
**Builds on:** [HYDROSHIELD_INTEGRATION.md](archive/HYDROSHIELD_INTEGRATION.md) (Eujin's ideas, merged) and
[FLOOD_PITCH_DECK.md](supporting/FLOOD_PITCH_DECK.md) (current deck text, not yet updated).
**House rules apply:** risk bands not depths · advisory not forecast · neutral wording · no invented numbers.

---

## 1. The idea

RainReady v1 served planners. v2 adds a **resident door** to the same shared picture, and a **loop** between the two:
residents' reports feed the plan, and the plan shows back to residents as what is being done on their street.

> **One shared picture, two doors: planners see where storage falls short, residents act in time, and their reports
> shape the next plan.**

Tagline (from Eujin): *Property lines stop at the fence. Water doesn't.*

## 2. Problem statement

> Water crosses property lines and council boundaries. The plans, the records and the blame do not. Residents can see
> a flood coming but not what it means for their street, cannot get the right agency to act, and lose belongings they
> could have saved. Developers and councils plan without residents' evidence. So every flood ends in blame instead of a
> better plan.

| Evidence | Source | Conf. |
|---|---|---|
| BBR residents flood at least three times a year; worst Dec 2021 (3 m) | Sinar Harian; FMT | M–H |
| ~583 residents, 48 associations petitioned in 2024; say councils and developers shift blame | FMT | H |
| Water flows from Setia Alam (Shah Alam) into BBR (Klang), different councils | FMT (residents' account) | M |
| Funded programmes on both sides, run separately | FMT, Bernama, The Star | H |
| About two-thirds of 2021 flood losses uninsured | Bank Negara via Insurance Business | H |
| SDP MD: "quite urgent, and this is a top priority for us" | The Edge, 21 Nov 2024 | M–H |

What is missing is not effort. It is one shared picture, and a way for residents to take part in it.

**Prior art (searched 20 Oct 2026).** Residents' flood reports feeding council work is **not new**, so we do not claim it
is. What we did not find is that loop combined with a storage-gap simulator, across a developer and two councils, at
township scale. **Our claim:** *residents' reports land in the same picture as the storage gap and the council boundary.*

| Precedent | What it does | Lesson for us |
|---|---|---|
| [Chatham County, NC flood dashboard](https://www.chathamcountync.gov/Home/Components/News/News/17495/19) | Residents report flooding; feeds watershed, planning and maintenance work | Councils accept this data. County warns reports are unverified |
| [Riskmap.in, Chennai (MIT Urban Risk Lab)](https://urbanrisklab.org/news/2018/8/3/innovation-for-disaster-response-and-recovery-demo-day-at-the-white-house-h5yj4-dz965-zjpwd-yeadw-p8ann-l8te3-dszps-5gkkh) | Public map of waterlogging and blocked drains reported by residents | Reporting through social media works |
| [PetaBencana, Jakarta](https://blog.petabencana.id/2020/01/14/2020-petabencana-id-collaborates-with-nasa-bnpb-government-agencies-and-residents-in-response-to-historic-2020-flood-event/) | Chatbot reports, validated by government agencies | Someone must verify reports |
| [KDEB WhatsApp drain line, Selangor (Malaysiakini, 2022)](https://malaysiakini.com/news/637120) | Residents send clogged-drain videos by WhatsApp; drains wider than 1.5 m, monsoon drains and rivers passed to other agencies | Selangor already uses messaging for this; 2026 status unconfirmed (section 10) |

## 3. Users

| User | Door | Gets |
|---|---|---|
| Developer township and engineering teams (**primary**, funds it) | Planner | Storage gap, before-you-build check, brief |
| Councils and JPS (free) | Planner | Shared reference, routed resident reports, brief |
| Households (free) | Resident | Move-now plan, report and track |
| Residents' associations (free) | Resident | **Verify reports**, area view, organised record for meetings |

## 4. Features

| # | Feature | Door | Demo status |
|---|---|---|---|
| 1 | **Catchment view**: 3D simulated township, council boundary, flow direction, documented flood spots with sources | Both | **Working** |
| 2 | **Rain and upstream scenarios**: rain slider, "more paved land upstream" switch; ponds and zones change risk band | Planner | **Working** |
| 3 | **Pond what-if and before-you-build check**: change a pond or earthworks, watch the storage gap move | Planner | **Working** |
| 4 | **Shared Capacity Brief**: one page, storage required vs stated capacity, storage gap with and without the upstream change, assumptions, owners, confidence | Planner | **Working or static sample** |
| 5 | **Report and track**: resident reports a blocked drain or flooded street **through existing messaging (chat-style), no app to install**; association verifies; forwarded to the existing official channel for that asset (e.g. iClean Selangor or Sispaa) with a link, not replacing it; visible status; appears as a pin in the planner view | Resident | **Clickable mock-up** |
| 6 | **Move-now plan**: on an official warning, a short action list for the street (car to higher ground, lift valuables, switch off mains), linking to the warning. Higher-ground spots are **"example" spots** from the terrain model until an owner agrees | Resident | **Clickable mock-up** |
| 7 | Responsibility record: who maintains each drain, pond, river reach, with confidence | Both | Inside 4 and 5 |
| 8 | Home-readiness checklist; after-the-water damage record for claims and aid | Resident | **Slide only, next phase** |
| 9 | AI "explain this result", grounded only in on-screen numbers, source shown | Both | Optional |

Not shown: predicted depths, recession times ("water gone by 10 p.m."), compliance verdicts, fault.

## 5. How we implement it

Tool choices remain each track's call; nothing below is decided unless marked.

| Part | Owner | What it is |
|---|---|---|
| 3D simulated township | Architecture | Blender or SketchUp model exported as `.glb`. Starting point: [../research/AR1_site_model/](../research/AR1_site_model/). Invented parts labelled generic |
| Screening simulator | Hydrology | MSMA 2 Rational Method and volume balance. Inputs: rainfall, runoff coefficients, upstream scenario, pond sizes. Outputs: storage required, storage gap (with and without the upstream change), risk band per zone. Every input in the assumption ledger |
| Website | Frontend and AI | Planner door working, resident door as mock-ups, brief page. Eujin suggested Next.js + React Three Fiber on Vercel **[not decided]** |
| Data contract | Hydrology + Frontend | Agreed list of inputs and outputs above, same units and datum as the 3D model |
| Deck, video, documents, integration | Team leader | Sections 7–9 |

## 6. Expected score if executed very well

Our own estimate, **confidence L**: judges' detailed rubric is not public.

| Criterion | Weight | Estimate | Why | Biggest risk |
|---|---|---|---|---|
| Impact | 25 | 20–22 | Documented resident harm; both doors | No survey responses yet |
| Innovation | 20 | 14–16 | Reports, storage gap and council boundary in one picture | Reporting loop itself has precedents; must claim only the combination |
| Feasibility | 20 | 14–16 | Public data, published methods, honest limits | No as-built pond or drain data |
| Strategic fit | 15 | 13–14 | SDP's own BBR priority; blue-green ponds | Live dispute; tone |
| Commercial value | 10 | 6–8 | Reuse across townships; pilot ask | Who pays: assumed SDP funds the BBR pilot; per-township licence later (L; research/TBD_VERIFY_RESOLUTION.md item 10) |
| Team, evidence, pitch | 10 | 8–9 | Strong sourcing, clear story | Demo half-working |
| **Total** | **100** | **~75–85** | | |

## 7. Video (5 minutes)

| Time | Content |
|---|---|
| 0:00–0:40 | A resident's night: warning, water rising, car, belongings, blame. Evidence on screen (583 residents, 3×/year) |
| 0:40–1:10 | The gap: separate programmes, separate councils, no shared picture. Tagline |
| 1:10–3:10 | **Live demo:** catchment view → rain slider → upstream switch → add a pond → open the brief |
| 3:10–4:00 | **Resident door:** report a blocked drain → pin appears in planner view → move-now plan on a sample warning |
| 4:00–4:30 | Honest limits: bands not depths, assumption ledger, what SDP data would add |
| 4:30–5:00 | Impact, pilot ask, team. Closing line |

## 8. Pitch deck (10 slides)

1. Title, one-line pitch, tagline
2. Problem: the resident's night plus the evidence table
3. The gap: programmes exist, no shared picture; three moments (before, during, after)
4. Solution: one picture, two doors, the loop (diagram)
5. Planner door: simulator, what-if, brief (screenshots)
6. Resident door: report and track, move-now plan (mock-ups)
7. Innovation: comparison with warnings apps, council systems, HEC models, and the reporting precedents (Chatham, Riskmap, PetaBencana)
8. Feasibility and honest limits: data, methods, assumption ledger, bands not depths
9. Impact, metrics and pilot (phases, stakeholders, ask)
10. Value to SDP, scale-up, team

Appendix: evidence, data sources, assumption ledger, limitations, validation, survey results, sources.

## 9. Supporting documents

| Document | Contents |
|---|---|
| Sample Shared Capacity Brief (PDF, 1 page) | The real output, with assumptions and confidence labels |
| Assumption ledger and limitations (PDF, 1–2 pages) | Every input: sourced, assumed or [TBD]; what would change the answer |
| Resident survey summary | Questions, response count, key findings **[TBD: no responses yet]** |
| Evidence and sources | Appendix A and F of the deck |

## 10. Decisions (proposed 20 Oct 2026, team to confirm)

| # | Question | Decision | Why |
|---|---|---|---|
| 1 | Primary user and name | **Developer first**; residents are the second door. Name **RainReady**; tagline *Property lines stop at the fence. Water doesn't.* | SDP runs the competition (strategic fit 15). RainReady is neutral; HydroShield tilts towards defence |
| 2 | Is the loop new? | **No. Claim only the combination**: reports, storage gap and council boundary in one picture. Cite precedents | Search found Chatham, Riskmap, PetaBencana (section 2) |
| 3 | Resident channel | **Existing messaging for reports, a web link for viewing, no app install** | Selangor already used WhatsApp for drain reports (2022) |
| 4 | Higher-ground parking | **"Example" spots from the terrain model**, labelled. Pilot partners: SDP-owned or council car parks | Car parks belong to someone |
| 5 | Who pays | **Developer funds it per township; councils and residents use it free.** Presented as a pilot proposal | Keeps the public-interest image; matches the primary user |
| 6 | Upstream share | **Show a scenario difference, not an attribution**: "with the upstream change, the gap grows from A to B" | No catchment boundary needed; assigns no blame. Add a range only if catchment data improves |

**Verification results (searched 20 Oct 2026)**

| Item | Result | Assumption we use | Conf. |
|---|---|---|---|
| KDEB WhatsApp drain line in 2026 | **Partly verified.** The line appears only in older reports ([Malaysiakini](https://malaysiakini.com/news/637120)). The iClean Selangor app and the Sispaa complaint system were the named channels in Feb 2026 ([Malay Mail](https://www.malaymail.com/news/malaysia/2026/02/04/selangor-residents-cry-foul-over-rubbish-delays-waste-firm-moves-to-publish-collection-schedules-online/207977)). KDEB covers drains up to 1.5 m; wider drains and rivers go to other agencies | RainReady **forwards** reports to the existing official channel and links to it. We never present our own hotline. The 1.5 m split goes into the responsibility record | M |
| Car parks the developer owns in BBR | **Not verifiable** from public sources. Listings show developer shop-office projects (e.g. Quadria, Taipan) but no public car park ownership ([PropertyGuru](https://www.propertyguru.com.my/commercial-properties-for-sale/at-taipan-bbr-2-3-storey-shop-office-16131)) | Demo shows **generic "example higher-ground spots"** chosen from the terrain model; no real site named. Pilot ask: the developer and councils name real sites | L |
| Resident preference: messaging vs app | **No Malaysian survey found.** Official channels are SMS alerts by NADMA via telcos ([Malay Mail, Nov 2024](https://malaymail.com/news/malaysia/2024/11/16/nadmalaunches-sms-flood-alert-system-to-protect-at-risk-areas-with-timely-warnings/157021)), phone alerts planned ([The Star, Oct 2024](https://thestar.com.my/news/nation/2024/10/11/flood-warnings-on-your-phone-soon)), and a Johor push to smart-app alerts ([EdgeProp, Oct 2026](https://www.edgeprop.my/content/1917675/johor-strengthen-mobile-flood-warnings-after-jb-flash-floods)) | **Warnings stay on official channels.** RainReady adds a web link with what it means for your street; reports go by messaging. Survey question below confirms | L–M |
| Cross-boundary drainage design review in Selangor | **No public process found.** JPS Selangor requires 100-year ARI retention for each development application and councils monitor MSMA compliance ([The Sun](https://thesun.my/news/malaysia-news/selangor-allocates-rm5-million-for-clearing-drains-culverts-on-unowned-land-em12697605/)); upstream–downstream coordination in 2026 was handled by meetings between governments ([Malay Mail, Aug 2026](https://www.malaymail.com/amp/news/malaysia/2026/08/23/bigger-dams-more-ponds-river-dredging-kl-and-selangor-plan-five-flood-fixes-on-the-table/232373)) | Review is **per development**; we found no shared cross-boundary check. Word it as "we found no public cross-boundary review", never "none exists" | M |

**Survey question to add**

> *If you wanted to report a blocked drain or flooding on your street, how would you prefer to do it?*
> WhatsApp or Telegram message · a dedicated app · a website form · phone the council · through my residents'
> association · I would not report it
