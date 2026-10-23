# Three Challenges to the Pitch: Built Towns, Who Pays for Losses, and Scale

**Written for:** the team leader. **As of:** 21 October 2026. **Prompted by:** three questions from the team leader
after a status check of the website and the screening simulator.
**Reads with:** [RAINREADY_CONCEPT_V2.md](../documentation/RAINREADY_CONCEPT_V2.md),
[WEBSITE.md](../documentation/WEBSITE.md) sections 7–9, [RESPONSIBILITY_RECORD.md](RESPONSIBILITY_RECORD.md).
House rules apply: no blame, no depths, unverified items marked.

---

## 0. Where the product stands (21 Oct 2026)

| Part | State | What it shows today |
|---|---|---|
| Website (live) | Map → planner → Brief → resident mock-ups, 14-step guided demo | Works end to end; no console errors at last check |
| Screening simulator | MSMA 2 Rational Method + volume balance, sourced inputs, parity Python ↔ TypeScript | 100-yr storm, today: pond A needs ~151,000 m³, pond B ~84,000 m³; trunk drain at 101 % of its assumed size |
| Main finding | Confidence **M** after the credibility pass | **The shortfall is the shared drain, not the ponds.** Ponds cannot release into a full drain |
| Weak spots | — | Upstream lever moves only the drain (+10 %), not the ponds, on the assumed 6 m drain; what-if pond tops out near 40,000 m³ (it catches only Z06); Z09 outlet unknown; the "one miss" (frequent flooding points to street drains, which are not modelled); no survey responses; deck still v1 |

Re-run on 21 Oct 2026: `python screening.py` gives the figures above.

---

## 1. "BBR and Setia Alam are already built. Is changing these levers supposed to fix it?"

**The objection is fair.** As the levers are labelled now ("upstream development 0–100 %", "what-if pond",
"drain size"), they read like a design game for a town that does not exist yet. A judge can ask the same thing.

**But it points at a framing problem, not a product problem.** In a built town, money is still being spent on
flooding every year. The question is not "how should we have built BBR?" but **"which of the fixes now on the table
works, and who has to act together?"** That is exactly what the simulator already answers:

- The "Fix it together" preset: with the upstream change, **the pond alone leaves pond A at 134 %, a 10 m drain alone
  leaves it at 130 %; only both together clear the red** ([WEBSITE.md](../documentation/WEBSITE.md) section 7). The pond and the
  drain may sit with different owners. *This is the pitch*: one party's fix on its own side of the line does not work.
- The credibility pass: pond A is about the right size **if it could release**. So a bigger pond on the BBR side,
  which residents asked for in 2024, would help less than the drain it empties into. That is a finding that can save
  money, in a built town.

### Three decisions a built town still makes

| Decision | Is it real at BBR? | Lever on the site today | What to change |
|---|---|---|---|
| **A. Retrofit: which fix, where, together?** | Yes: Taman Mutiara pond (RM7.3m, ~2 ha, delayed 2024), 17 urgent Klang projects, RM150m Shah Alam works ([CLAUDE.md](../CLAUDE.md) section 4) | What-if pond, drain size | **Rename the levers after the real programmes**: "a new pond like the Taman Mutiara pond", "widen the shared drain (Klang works)". Same maths, but now it is a live budget question, not a fantasy |
| **B. What is still to be built** | Yes. SDP launched Laman Lakeside in BBR in Nov 2024 ([The Edge](https://theedgemalaysia.com/article/sime-darby-property-secures-72-takeup-laman-lakeside-klang)); a 2020-era source said over 70 % of BBR's land was still to be developed ([Wikipedia](https://en.wikipedia.org/wiki/Bukit_Raja)) **[verify: current figure, L]**. Setia Alam has infill and redevelopment | Upstream development | Rename "upstream development" to **"next parcels upstream"** and frame the before-you-build check as a check on the *next* launch, on either side of the line |
| **C. Keep what is built working** | Yes: residents said in 2024 the ponds were shallow; the one ground check our model missed points to street drains | **None** | **Add two maintenance levers:** "pond silted (lost depth)" and "drain partly blocked (%)". Maths: lower the stated capacity, lower the drain's conveyance. These are the levers residents' reports actually move |

**Lever C is the strongest fix to the objection.** It is the only one that matters in a fully built town every
single year, it is cheap, and it **joins the two doors**: a resident's "blocked drain" report becomes a planner input
("this stretch at 70 % conveyance"), and the planner sees what that does to storage. Today the loop is a pin on a map;
with lever C it becomes a number in the shared picture.

**Pitch line (proposed):** *"We are not redesigning Bandar Bukit Raja. We test the fixes already being paid for, and
show which only work together."*

**Done 21 Oct 2026** (levers renamed, Keep it working levers and presets, Brief section, demo step; see [WEBSITE.md](../documentation/WEBSITE.md) section 10). The link from a resident's report to the blockage lever is **on hold** until the resident report function is built.

**Implementation note.** Renaming the levers is a text change. Lever C needs a small change to inputs (a blockage
factor on the drain's Manning capacity; a capacity reduction per pond), mirrored in `screening.py` and
`screening.ts`, with the parity check re-run. The website is an approved implementation, so this is buildable before
23 Oct if the team leader wants it.

---

## 2. "If BBR floods badly, who is responsible for the losses?"

### The short answer, in plain words

1. **Nobody pays automatically.** Malaysia has no scheme that repays flood losses in full. What arrives
   automatically is **relief**, not compensation.
2. **Your own insurance is the first line**, and most people do not have flood cover.
3. **The government gives a small cash aid** to affected households.
4. **Blame, and real compensation, is decided by a court**, and since 29 Sep 2026 there is a High Court ruling that
   held public authorities liable for a Selangor flood.

### The chain, step by step

| When | Who | What they do | Source | Conf. |
|---|---|---|---|---|
| **Before** | Council (MBDK / MBSA), JPS Selangor, developer for ponds not handed over | Maintain drains, rivers, ponds under the rules in the responsibility record | [RESPONSIBILITY_RECORD.md](RESPONSIBILITY_RECORD.md) | M–H |
| **Warning** | METMalaysia (rain), JPS Public Infobanjir (river levels), NADMA (SMS alerts) | Warn | Concept v2 section 10 | H |
| **During** | District Disaster Management Committee, chaired by the District Officer (state and national committees above it) | Runs evacuation and relief centres (PPS) | Arahan MKN No. 20 ([BH, May 2024](https://www.bharian.com.my/amp/berita/nasional/2024/05/1244218/dasar-pengurusan-bencana-negara-akan-disemak-semula-ahmad-zahid)); a revision was announced in 2024, **[verify] whether issued** | M |
| **Right after** | Federal government via NADMA | **Bantuan Wang Ihsan: RM1,000 per head of household** registered at or with a relief centre; RM10,000 to heirs on a death. Verified by the state disaster committee | [MOF](https://mof.gov.my/portal/ms/berita/akhbar/bantuan-wang-ihsan-rm1-000-diperluas-untuk-setiap-ketua-isi-rumah-terjejas-banjir); [RTM](https://berita.rtm.gov.my/nasional/senarai-berita-nasional/senarai-artikel/103-kir-daerah-kuala-muda-terima-bantuan-banjir). **[verify] current rate for 2026** | M |
| | State government | Sometimes adds its own aid | **[TBD] Selangor's current scheme** | L |
| | Council | Clears debris and rubbish after the flood | Common practice **[verify] for MBDK** | L |
| **Claims** | The household's own insurer | **Home contents:** only if flood is covered. **Car:** only with the "special perils" add-on; standard comprehensive cover excludes flood. Uptake is low: one insurer said 11 % of its motor customers added it | [Motorist](https://www.motorist.my/article/6200/special-perils-add-on-is-flood-coverage-worth-it-in-malaysia); [NST 2022](https://nst.com.my/amp/news-cars-bikes-trucks/2022/11/846045/motorists-still-not-insured-against-flood); about two-thirds of 2021 losses were uninsured (concept v2) | M–H |
| **Blame and compensation** | Civil courts | A negligence claim against whoever owed a duty. See below | — | — |

### The Taman Sri Muda ruling (29 Sep 2026): it changes this question

- **What happened:** 50 Taman Sri Muda (Shah Alam) residents sued over the December 2021 flood, seeking
  RM3,767,148.51. The Shah Alam High Court (JC Dr Shoba Rajah) found the **federal government (through NADMA and
  METMalaysia), the Selangor JPS director and MBSA** liable, jointly ([The Star, 30 Sep 2026](https://www.thestar.com.my/news/nation/2026/09/30/authorities-held-liable-over-2021-floods);
  [Malaysiakini](https://www.malaysiakini.com/news/885928-snapshot-residents-win-suit-against-govt-over-2021-floods-govt-to-expand-cctv-coverage-in-boarding-schools)).
- **Why:** these bodies owed **operational duties**: JPS to run and maintain the flood assets it controls; **MBSA to
  repair, clear and maintain local drains, even though JPS owns the main flood works**; NADMA and MET to warn and
  respond competently.
- **"Act of God" rejected.** Rain heavier than the design standard was not enough; they had to show no reasonable
  preparation could have helped.
- **Not final.** Damages not yet assessed (case management 6 Oct 2026); Selangor said it is considering an appeal
  ([Malay Mail, 30 Sep 2026](https://www.malaymail.com/news/malaysia/2026/09/30/selangor-mulls-appeal-after-high-court-finds-authorities-liable-for-2021-taman-sri-muda-floods/237147)).
  It took almost five years.
- **The limit:** councils keep a statutory immunity for *approving* building plans (s. 95(2), Street, Drainage and
  Building Act 1974, upheld in the Highland Towers case, Federal Court 2006,
  [HBA archive](https://hba.org.my/archive/focus/HT/2006/council_not.htm)). So "the council should never have
  approved Setia Alam" is a much weaker claim than "the council did not clear the drain". **[verify] with a law
  lecturer before using this distinction on a slide.**
- **Sri Muda is a river and pump flood, not a township drainage flood like BBR.** It is a precedent for *how duties are
  read*, not a prediction for BBR.

### Applied to a severe flood at BBR (our reading, **L**, not legal advice)

| Asset that failed | Who held the duty, by the rules | Rule |
|---|---|---|
| Street and secondary drains, incl. the shared trunk drain (Klang side) | MBDK | R3 |
| Drains above the council line | MBSA | R3, R6 |
| Main ditch, Sungai Keramat | JPS Selangor | R3, R4 |
| Ponds A and B | **Not settled**: SDP while not handed over, MBDK after | R1, R2 |
| Warnings and relief | METMalaysia, JPS, NADMA and the district committee | Sri Muda ruling |

**Done 21 Oct 2026:** the website page `#/after`, a Brief section and card links, and slide text; facts re-checked in
[AFTER_THE_FLOOD.md](AFTER_THE_FLOOD.md), which wins over this section (adds Selangor's RM1,000 per family). The
damage record (feature 8) stays with the resident report work.

### What it means for RainReady

- **The responsibility record just became more valuable, and more sensitive.** After Sri Muda, "who maintains this
  drain" is the question a court asks. Our record answers it from published rules, which helps residents route
  complaints and helps agencies **show they did their operational duty** (a dated maintenance and response trail is
  their best defence).
- **The risk:** agencies may be *less* willing to confirm their line if they think it creates evidence against them.
  Keep the wording "who maintains, under the published rules", never "who is at fault", and make the case that a clear
  record protects the party that keeps it.
- **Feature 8 (after-the-water damage record) moves up.** Dated photos, a list of losses and receipts are what an
  insurer, a BWI officer or a court needs. It is the most direct answer to "the residents lose their belongings and
  then what?". Today it is "slide only, next phase".
- **For the video and deck:** one simple slide, "After the water: who does what", using the table above. Neutral, and
  it shows judges we understand the system residents are stuck in.

---

## 3. "Should we target more towns than BBR?"

**Short answer: yes in the story, not in the build before 23 Oct.** Scale earns points (Impact 25, Commercial
value 10), but a second half-built site would cost the depth that makes BBR convincing (Feasibility 20, Evidence 10).

### What already scales and what does not

| Part | Reuse at a new site | Per-site work |
|---|---|---|
| Simulator (`screening.py` / `.ts`) | Same code; MSMA 2 IDF constants exist for gauges nationwide | A new `inputs.json`: zones, runoff C, pond list, drain size |
| Zones | `plan_zones.py` cuts along mapped drains and roads from OSM | Checking against imagery |
| Responsibility cascade | The logic | **The rules are Selangor's** (state cabinet decisions). Every other state needs its own rule set |
| Resident door, map, Brief | Fully | None |
| **3D township (Blender)** | No | **Hand-made, the costliest part.** For scale, a new site should get a **2D map view**, not a new 3D model |

So the per-site cost is mostly **data assembly and checking**, not code. We have no basis yet for a cost per site in
ringgit; do not put one on a slide.

### Where the method fits, and where it does not

The simulator models **storage and drainage in developed townships during intense rain** (flash floods, ponding).
It does **not** model river floods, tides or pump failure, which drove Taman Sri Muda and the east-coast monsoon
floods. So the honest market is **urban flash-flood towns**, not "every flood in Malaysia". The site's own map already
gives the size of that market: **JPS listed 493 flash-flood locations in 91 towns across every state (2017)**
([WEBSITE.md](../documentation/WEBSITE.md) section 8).

### The SDP angle

Sime Darby Property has many townships, several in Selangor (where our rules already apply). Its land is also mostly
the *next* parcels (section 1, decision B), where a before-you-build check is worth most. "Other towns" for us should
mean **SDP's own pipeline first, then councils**, because:

- strategic fit (15) rewards SDP's own estate;
- the funding decision of 20 Oct (developer pays per township, councils use it free) only works on developer land. For
  non-SDP towns, **who pays** would change (state, council or JPS). That is a new open decision, not a detail.

### Recommendation

| When | What |
|---|---|
| **By 23 Oct** | No second build. Add one deck slide "How it scales": what is reused, what each site needs, the 493-location map, the Selangor-rules caveat. On the website map, keep "No catchment model here yet" but add one line: "What a new site needs: …" |
| **If shortlisted (28 Oct)** | Pick **one second site** by three tests: (1) JPS flash-flood records exist; (2) drainage crosses a council or developer line; (3) a public pond or drain register exists. Build it as a **2D screening only**, to prove the per-site cost honestly |
| **Pitch** | "Deep at BBR, built to repeat": the depth is the proof, the map is the market |

---

## 4. Proposed actions, in order

| # | Action | Effort | Owner |
|---|---|---|---|
| 1 | Rename levers after real programmes and "next parcels" (section 1, A and B) | Small, website text | Team leader / Claude |
| 2 | Add the maintenance levers (pond silted, drain blocked) and tie them to resident reports (section 1, C) | Medium, simulator + parity + site | Team leader with Claude |
| 3 | Deck slide "After the water: who does what", incl. the Sri Muda ruling (section 2) | Small | Team leader |
| 4 | Move feature 8 (damage record) to a mock-up in the resident door | Small–medium | Frontend |
| 5 | Deck slide "How it scales"; record the new open decision: who pays outside developer land (section 3) | Small | Team leader |
| 6 | Survey question on insurance and aid (does the household have flood cover? did they receive BWI?) | Small | Team leader |

## 5. Open

- [verify] Current BWI rate and eligibility for 2026; Selangor's own flood aid scheme [TBD].
- [verify] Whether the revised Arahan MKN No. 20 has been issued.
- [verify] Whether Selangor appeals the Taman Sri Muda judgment; the damages awarded.
- [verify] The s. 95(2) approval vs maintenance distinction, with a law lecturer.
- [verify] Current undeveloped share of BBR (the 70 % figure is about six years old).
