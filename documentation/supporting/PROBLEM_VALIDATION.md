# Problem validation — is RainReady solving a real issue, and has someone already solved it?

**Owner:** Team leader · **Date:** 11 October 2026 · **Overall confidence: M**

Two questions the project has to survive, asked honestly and answered with evidence:

1. Is the problem real, or have we constructed one to have something to build?
2. Does a shared drainage register already exist? If it does, our central gap closes and we need a different angle.

**Short answer.** The problem is real and documented. The gap does not close, but **our claim has to change shape**,
because the Selangor state government has already named this problem in its own words and started on it. We are no
longer allowed to imply nobody has looked at it. Handled properly, that makes us more credible rather than less.

---

## Part A — Is the problem real?

**Yes, and none of it is our inference.** All of the following is in
[BBR_PUBLIC_DOCUMENT_SURVEY.md](BBR_PUBLIC_DOCUMENT_SURVEY.md) already:

- **583 residents across 48 associations** petitioned the Menteri Besar in 2024. **H**
- Residents report flooding **at least three times a year**; worst **December 2021 at 3 m**; latest cited **24 April
  2024**. **H** that they said it.
- SDP's managing director called it **"quite urgent"** and **"a top priority"**. **M–H** — The Edge, 21 Nov 2024 (settled 21 Oct 2026).
- Water crosses from **Setia Alam (Shah Alam)** into **BBR (Klang)** — two councils, one drainage system. **H**

**The coordination gap is also evidenced**, which is the part that matters for us. At least four actors are acting
separately on the same water: Shah Alam's RM150m programme for Setia Alam, Klang's 17 projects across 13 hotspots,
DID taking over ponds, and the developer's own wetland design. **M**

**The strongest single number remains:** Bernama, 5 May 2025 — over **300 retention ponds in Selangor identified as
having no owner**, with about **55 taken over by DID**. That is roughly 245 ponds that no party clearly maintains.
**M**

**What is NOT real, and we must stop short of it.** We cannot claim the flooding is caused by upstream development.
See [AR1_site_model.md](../../research/AR1_site_model.md) — the terrain data cannot support any causal or predictive
claim, and the upstream relationship rests on the public record rather than on our own analysis.

---

## Part B — The shared drainage register survey

**Method.** Online only, 11 October 2026. Searched the Selangor state GIS portal through its public ArcGIS REST API,
probed the JPS Selangor GIS server, read the national PISMA portal, and searched Malay and English press and Selangor
State Assembly (DUN) answers. No authenticated access was used and none was attempted.

### B1. Selangor has a dashboard for exactly this problem, and it is called "no man's land"

On **Geosmart Selangor** (`geosmart.selangor.gov.my`), the state's ArcGIS Enterprise portal, which is **public and
allows anonymous search**:

| Item | Type | Created | Last modified | Views |
|---|---|---|---|---|
| **NO MAN'S LAND LONGKANG/PARIT FASA 1** | Dashboard | 7 May 2025 | 4 Jun 2025 | **98** |
| HOTSPOT BANJIR 2013–2025 | Dashboard | 15 Jul 2025 | 20 Aug 2025 | 248 |
| GIS JPS Negeri Selangor | Web app | 6 Dec 2024 | — | 9 |
| Stesen Hidrologi JPS · River Water Level Data (JPS) · Banjir 2013–2021 JPS · Portal Bencana NADMA | Web apps | — | — | — |

**"No man's land" is the state's own term, not ours.** The dashboard was created **two days after** the 5 May 2025
Bernama report on unowned ponds, so it appears to be part of the same response.

**The data behind it is not public.** The feature layers powering both the no-man's-land dashboard and the flood
hotspot dashboard return **HTTP 403 Forbidden** to an anonymous user. The dashboards are listed; their contents are
not viewable. **H** — tested directly.

Note the scope limits: it is **Fasa 1** (Phase 1), and it covers **longkang/parit** — drains and ditches — **not
ponds**.

### B2. JPS Selangor has a GIS server, and it was down

`jpsselgis.selangor.gov.my` hosts layers named `KOLAM_TAKUNGAN_MSMA` (MSMA retention ponds), `Parit2022` (drains,
2022) and several `Kawasan_Tadahan` (catchment) layers.

Its ArcGIS REST endpoint returned **HTTP 503 Service Unavailable** on every attempt across several minutes. The
public front page and map viewer load, but the map pulls no data services. **H** that it was unavailable on
11 October 2026. **Update 21 Oct 2026: it is back online**; findings in ../../research/TBD_VERIFY_RESOLUTION.md part A.

### B3. PISMA — a national programme that does include an asset inventory

**PISMA** (Pelan Induk Saliran Mesra Alam) is the national drainage master plan programme under MSMA. Among its
stated objectives and outputs:

> Develop an inventory of drainage system assets — infrastructure in the study area, as a reference for local
> authorities (PBT) and related parties for monitoring and maintenance.

**This is the closest thing to a register that exists, and we must acknowledge it.** But:

- It is a **periodic consultancy study**, delivered district by district, not a live system.
- The inventory goes **to local authorities**. It is **not published** and nothing is downloadable from the portal.
- **Klang's PISMA was done in 2009.** A new study, listed as **"Klang and Petaling, Selangor", is dated 2026** —
  possibly in progress now. No public report of it found on 21 Oct 2026; assumed not yet published.

Petaling district includes Shah Alam, so a 2026 Klang–Petaling study may span both sides of our boundary. **Assume a
judge knows this and prepare for it** (Part D).

### B4. Pond ownership is counted repeatedly, and the counts do not reconcile

| Source | Year | Figure |
|---|---|---|
| DUN Selangor | 2015 | Target to take over **314** developer ponds by 2018 |
| DUN Selangor | 2020 | **547** ponds needing gazettement — 296 JPS/PBT, 247 developer |
| The Star / Selangor Journal / Sinar Harian | 2025 | ~**600** censused · ~**300** unowned · **55** taken over |
| New Straits Times (cited) | 2026 | **190+** flood retention ponds in Selangor |

Four counts, four different numbers, over eleven years. The scopes are probably different, but no source says so.
**That inconsistency is itself evidence for our case** and can be shown as a table. **M**

### B5. Verdict on the register question

**No public, shared, cross-jurisdiction drainage register exists that a council officer, a developer and a resident
can open on the same day.** What exists:

- inventories held **inside** agencies (JPS, PBT, PISMA consultants),
- a state dashboard that **names the exact problem** but whose data is **locked**,
- a state GIS server that was **offline when tested**,
- pond counts that **do not agree with each other**.

**Confidence: M.** This is an outside-in survey. We cannot see what councils see.

---

## Part C — What this does to the project

### The claim has to change

| Do not say | Say instead |
|---|---|
| "There is no shared picture." | "The pieces exist, held separately. The state's own no-man's-land dashboard names the problem; its data is not open, and the counts across agencies do not reconcile." |
| "Nobody is doing anything." | "Klang's drainage master plan was done in 2009 and is being redone in 2026. A study every seventeen years is not a live shared view." |

The second column is stronger. It shows we looked.

### The sharpest defensible line we now have

> **Klang's drainage master plan: 2009. Next one: 2026.**
> Seventeen years between snapshots, for a township that floods three times a year.

### Feature ranking, revised after this survey

| Rank | Feature | Why |
|---|---|---|
| 1 | **Who maintains each drain, pond and river reach** | Survives this check. ~245 unclaimed ponds justify it. The state started on drains and stopped at Phase 1 |
| 2 | **Catchment view across the council boundary** | We now hold real geometry: drainage runs north-east to west, the council line crosses it near perpendicular |
| 3 | **Street-level advisories on official warnings** | Feasible, as long as it stays advisory and links back |
| 4 | **Retention-pond what-if** | Weakest. The terrain data cannot carry it. Keep it as a labelled scenario sandbox, never a prediction |

**The team's effort is currently weighted toward 3D and physics, which mostly serve rank 4.** That is the main
misallocation to correct.

### Is it futile?

No. The problem is documented, the gap is real, and the state's own language supports our framing. But the project's
value is in the **register and the cross-boundary view**, not in the flood simulation. A pitch built on the first two
survives scrutiny. A pitch built on predicted flood depths does not.

---

## Part D — Objections to prepare for

**1. "PISMA 2026 covers Klang and Petaling. Why are you needed?"**
PISMA produces a plan and a snapshot inventory, delivered to councils, on a cycle measured in years and not
published. We are proposing a live, shared, public view. Different object, different cadence, different audience.
Keep the answer to three sentences.

**2. "Councils don't lack a map. They lack mandate and budget."**
Substantially correct, and we should concede it. The narrower claim we can defend: where responsibility for a
specific pond or drain reach is undefined, nothing happens by default, and roughly 245 unclaimed ponds show that
happening at scale. A register removes ambiguity. It does not create authority. **Do not claim more.**

**3. "Your flood model isn't credible."**
Also correct, if we present it as a model. Present it as a scenario comparison — same storm, two configurations,
relative difference only — and state the terrain limits before being asked. Our own design principle already says
decision support under uncertainty, not prediction.

---

## Part E — Still unknown

- **Whether councils and developers can already see the locked layers.** They probably can; that may be the whole
  point of the permissions. This is the single biggest risk to our gap. **[TBD]**
- **What is actually in the no-man's-land dataset** — how many drains, which districts, whether ownership is an
  attribute. **[TBD]**
- ~~Whether the JPS Selangor GIS 503 is permanent~~: transient, back on 21 Oct 2026.
- **Whether PISMA Klang–Petaling 2026 has started:** no public report found (21 Oct 2026); assumed not yet published.
- **Whether Bandar Bukit Raja appears in Fasa 1** of the no-man's-land exercise: data not public. Ponds A and B are on JPS's own pond list, so they are not unowned (21 Oct 2026).
- View counts may not reflect internal use; officers may reach the same data another way. Do not over-read the 98.

All of these need a direct approach to JPS Selangor, which we cannot make until shortlisted.

---

## Sources

- [Geosmart Selangor portal](https://geosmart.selangor.gov.my/portal/home/) — queried through its public ArcGIS REST
  API, 11 October 2026. Item IDs on request; data layers returned 403.
- [JPSSelGIS](http://jpsselgis.selangor.gov.my/jpsselgis/) — front page loads; REST endpoint 503 on 11 October 2026.
- [PISMA portal, Jabatan Pengairan dan Saliran](https://storm.water.gov.my/about-pisma) — objectives, outputs and the
  list of 58 studies including Klang 2009 and Klang–Petaling 2026.
- [The Star, 7 May 2025 — "S'gor in a fix over unowned ponds"](https://www.thestar.com.my/metro/metro-news/2025/05/07/sgor-in-a-fix-over-unowned-ponds)
- [Selangor Journal, May 2025 — state to take over abandoned retention ponds](https://selangorjournal.my/2025/05/state-to-take-over-management-of-abandoned-retention-ponds-izham/)
- [Sinar Harian — "Lebih 300 kolam tadahan tidak bertuan dikenal pasti di Selangor"](https://www.sinarharian.com.my/article/726836/edisi/selangor-kl/lebih-300-kolam-tadahan-tidak-bertuan-dikenal-pasti-di-selangor)
- [DUN Selangor — PELAN INDUK SALIRAN MESRA ALAM (PISMA)](https://dewan.selangor.gov.my/question/pelan-induk-saliran-mesra-alam-pisma/)
- [DUN Selangor — KOLAM TAKUNGAN](https://dewan.selangor.gov.my/question/kolam-takungan/)
- [DUN Selangor — Serahan Kolam Takungan Oleh Pemaju Kepada JPS](https://dewan.selangor.gov.my/question/serahan-kolam-takungan-oleh-pemaju-kepada-jps/)
