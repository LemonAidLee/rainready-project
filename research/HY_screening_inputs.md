# Screening Simulator Inputs: Sourced Values (MSMA 2nd Edition and Public Data)

**Written for:** the team leader and the judges' appendix. **As of:** 21 October 2026.
**Why:** no sourced inputs were available, so the team leader asked Claude to source them. This replaces
the placeholders listed in [../documentation/HY_INPUT_REQUEST.md](../documentation/archive/HY_INPUT_REQUEST.md).
**Used by:** [`make_inputs.py`](../simulations/township-3d/make_inputs.py), which writes `inputs.json` for
`screening.py` / `screening.ts`. Confidence: **H** (cited figure), **M** (cited method, our application), **L**
(stated assumption).

## 1. Sources

| Ref | Document | How it was read |
|---|---|---|
| **MSMA-1** | *Urban Stormwater Management Manual for Malaysia (MSMA), 2nd Edition*, DID Malaysia, 2012. Chapter 1, Design Acceptance Criteria. PDF from JPS Sarawak, `did.sarawak.gov.my` (attachment *Chapter 1 - Design Acceptance Criteria*), downloaded 21 Oct 2026 | Text, plus the page image of Table 1.1 |
| **MSMA-2** | Same manual, Chapter 2, Quantity Design Fundamentals (61 pages, dated Aug 2012), same server, downloaded 21 Oct 2026 | Text, plus the page images of Tables 2.3, 2.5 and 2.B1 (the extracted text **misaligns** these tables; only the images were used) |
| W1 | Wikipedia, "Bukit Raja"; EdgeProp, "Bandar Bukit Raja — breathing new life into northern Klang" | Land history (oil palm estate; master plan 2002) |
| AR1 | [AR1_site_model.md](AR1_site_model.md): terrain, imagery check, drain network | Ground fall, main ditch width, why terrain routing failed |

**Warning about online copies:** a search-result copy of Table 2.B1 gave λ = 57.3495 for JPS Sungai Manggis. The
official PDF gives **56.052**. Scraped copies on Scribd, PDFCoffee and similar sites are unreliable; quote only the PDF.

## 2. The values

| Input | Value | Status | Source and reasoning | Conf. |
|---|---|---|---|---|
| Method: peak flow | `Q = C·i·A/360` | sourced | MSMA-2 Eq. 2.3 | H |
| Rational Method limits | Not for catchments **> 80 ha**, nor for designing storage facilities | sourced | MSMA-2 2.3.1.2. All 9 draft zones are ≤ 77.2 ha. The storage caveat is why the site says **screening, not design** | H |
| Runoff volume | `V = Q·d` (factor 1.0) | sourced | MSMA-2 2.3.2, Rational Hydrograph Method: the Type 1 trapezoid (d > tc) and the Type 2 triangle (d = tc) both hold Q·d | H |
| Design ARI | **100 years** | sourced | MSMA-1 Table 1.1: link house / apartment, major system 100 yr; mixed developments take the highest ARI (Note 1) | H |
| IDF equation | `i = λT^κ/(d+θ)^η` | sourced | MSMA-2 Eq. 2.2, valid for T = 2–100 yr, d = 5 min–72 h | H |
| IDF station | **2913001 Pusat Kawalan JPS Telok Gong**: λ 63.493, κ 0.170, θ 0.254, η 0.872 | sourced constants; station choice assumed | MSMA-2 Table 2.B1 (Selangor). Chosen as the nearest listed gauge. **Location checked 21 Oct 2026** on JPS Selangor's station layer: Telemetri Telok Gong, **2.9951 N, 101.3679 E**, about 13 km SW of BBR, in Klang district, coastal like BBR; matches the station-number grid (29 = 2.9 N, 13 = 101.3 E). Nearer JPS gauges (Bandar Klang, Pekan Meru) have no Table 2.B1 constants | H / M |
| Storm durations tested | 0.5, 1, 2, 3, 6, 12, 24 h | assumed | MSMA-1 2.2.1: examine a range of durations; storm ≥ tc (MSMA-2 2.2.2). The design storm is today's critical duration (most storage), used for all scenarios | M |
| Time of concentration | **0.5 h** | assumed | MSMA-2 Table 2.1: overland, paved (n* 0.015, Table 2.2), 200 m at 1 % ≈ 9 min; drain, 1 km, n 0.018, R 0.5 m, S 0.0013 ≈ 13 min; total ≈ 23 min, rounded up. Used only for the pre-development peak | L |
| Runoff coefficients, now | Z01 0.648 · Z02 0.628 · Z03 0.782 · Z04 0.710 · Z05 0.720 · Z06 0.664 · Z07 0.727 · Z08 0.699 · Z09 0.763 | measured | MSMA-2 Table 2.5, major-system column: terrace 0.90, commercial 0.95, park 0.40, bare soil 0.60, grass 0.50, roads 0.95, detention pond 0.95. Area-weighted by Eq. 2.4 over each zone's land cover in the model ([`landcover.py`](../simulations/township-3d/landcover.py)). **The cover is the simulated town**, so the table is H but the cover is M–L | M |
| Upstream change, Z01 | 0.648 → **0.717** | measured | The 3.56 ha of invented aprons in Z01 become commercial (0.95), the same change the 3D scene shows | M |
| Upstream beyond the edge (`EXT_A`) | **50 ha**, C 0.648 → **0.90** | assumed / planner input | No usable upstream boundary (AR1: terrain routing failed; JPS `Kawasan_Tadahan` unavailable). 50 ha is a test value. The scenario is defined as the remaining land developing like link and terrace housing (Table 2.5, 0.90) **where peak control is not fully achieved**. A what-if, not a forecast | L |
| Pre-development C | **0.40** | sourced | MSMA-2 Table 2.5, "Sport Fields, Park and Agriculture". BBR was a Sime Darby oil palm estate before the 2002 master plan (W1) | M |
| Allowed pond release | Pre-development peak flow of the pond's catchment | sourced rule | MSMA-1 1.2.1: "Post development peak flow of any ARI at the project outlet must be less than or equal to the pre-development peak flow of the corresponding ARI (Qpost ≤ Qpre)". Further limited by the room left in the trunk drain | M |
| Trunk drain conveyance | Concrete trapezoid, top 6 m, bottom 3 m, depth 2 m → **19.5 m³/s** | assumed (n sourced) | Manning, n = **0.018** (MSMA-2 Table 2.3, concrete, rough finish). The section is not measurable: tree cover at the council corner (AR1 imagery). Chosen between the model's 3 m ditch and the 8–10 m main ditch it joins. Slope 0.0013 from the regional ground fall (AR1, M) | **L** |
| Pond A and B capacity | **None (planner input)** | — | No public figure (AR1). Must not be measured from the model. Team leader, 21 Oct 2026: option (a), so the headline is **storage required**, and the gap appears only when a planner enters a stated capacity | — |
| What-if pond | 25,000 m³, release 0 during the storm, on the OSM brownfield in Z06 | planner input | A test size. Release 0 because, with the trunk drain full, a pond that passes flow on does not reduce pond A's storage | — |
| Band thresholds | Change vs today: medium ≥ 1.05, high ≥ 1.20. Vs an entered capacity: 0.8 / 1.0 | assumed (team choice) | Bands show scenario differences unless a capacity is entered | L |

## 3. Result on these values (21 Oct 2026)

The design storm is a 100-year, 3-hour storm: i = 49.6 mm/hr at Telok Gong.

| Scenario | Trunk drain demand / conveyance | Pond A storage required | Pond B storage required |
|---|---|---|---|
| Today | 19.6 / 19.5 m³/s (**full**) | **151,100 m³** | **83,600 m³** |
| More paved land upstream | 21.6 / 19.5 (**+10 %**) | 151,100 (no change: it already releases nothing) | 83,600 |
| + what-if pond (25,000 m³) | 21.6 / 19.5 | **126,100 (−17 %)** | 83,600 |

**What it says:** with the assumed drain, the shared trunk drain is full in a 100-year storm even before the upstream
change. So ponds A and B must hold the whole storm, and the upstream change shows up as **10 % more load on the shared
drain**, not as more pond storage. Storage added upstream of pond A reduces its requirement one for one.

## 4. Sensitivity (how much the answer depends on the assumptions)

| Change | Design storm | Pond A today | Pond A, upstream change | Trunk drain, upstream change |
|---|---|---|---|---|
| Base (Telok Gong, 6 m drain) | 3 h | 151k m³ | ×1.00 | ×1.10 |
| Gauge 3314001 (P Setia) | 3 h | 159k | ×1.00 | ×1.10 |
| Gauge 2815001 (Sg Manggis) | 2 h | 117k | ×1.01 | — |
| Gauge 3117070 (JPS Ampang) | 3 h | 151k | ×1.00 | ×1.10 |
| Drain 3 m top (model width) | 12 h | 190k | ×1.00 | ×1.10 |
| **Drain 10 m top (main-ditch-like)** | 1 h | 103k | **×1.10** | ×1.10 |
| **Drain 14 m top** | 0.5 h | 50k | **×1.16** | ×1.10 |
| 10-year ARI (minor system) | 2 h | 88k | ×1.07 | ×1.10 |
| `EXT_A` 200 ha | 6 h | 159k | ×1.07 | ×1.22 |

**Reading it:** the gauge choice moves pond A's storage by about ±20 %. **The trunk drain's size decides the story.**
If the drain is small, it is already full and the upstream change only adds load on the drain. If it is as large as
the main ditch, the ponds can release part of the storm, and the upstream change raises their storage requirement by
10–16 %. This is why the website exposes the drain size and the upstream area as sliders: the uncertainty is the
point. **The one measurement that would most improve the screening is the trunk drain's cross-section.**

## 5. Limits to state on screen and in the appendix

- **Screening, not design.** MSMA does not recommend the Rational Method for designing storage. A design would use
  hydrograph routing (MSMA-2 2.3.3–2.4) and surveyed levels.
- Only the trunk drain is counted as conveyance. Overland and road flow paths (the major system) are not, so storage
  required is an upper-end figure.
- The land cover is the simulated town, and the zone edges are a draft from mapped lines, not an official catchment.
- No pond capacity is claimed. No depths, no times to recede, no compliance verdicts.

**Update 21 Oct 2026:** both key assumptions checked in [HY_ASSUMPTIONS_CHECK.md](HY_ASSUMPTIONS_CHECK.md) (drain width on imagery; storage band against MSMA 2 Chapter 7). The finding holds across the plausible range.

## 6. Still open

- ~~Coordinates of station 2913001~~: checked 21 Oct 2026 (section 7).
- The trunk drain's real cross-section (the biggest lever, section 4): drawings from the council or SDP, if shortlisted.
- Stated capacities of ponds A and B. JPS lists both ponds (K02, K03) in its phase-1 pond layer but publishes no volume; `KOLAM_TAKUNGAN_MSMA` has no Klang data (21 Oct 2026). An assumed capacity is offered as a preset (section 7).
- The upstream catchment draining through the council-line crossing.

## 7. Added 21 Oct 2026: checks and stated assumptions

Full ledger: [TBD_VERIFY_RESOLUTION.md](TBD_VERIFY_RESOLUTION.md). What changed for the simulator:

| Item | Value | Status | Conf. | Effect on results |
|---|---|---|---|---|
| IDF gauge location | Telemetri Telok Gong, 2.9951 N 101.3679 E (JPS Selangor GIS, `Hosted/Stesen_Hidrologi`) | checked | H (location) / M (gauge ID) | None: the constants were already 2913001's |
| Assumed pond capacity (preset only) | Pond A 83,400 m³, pond B 85,900 m³ = OSM water area × 1.5 m live storage | assumed | L | Only when the planner picks the "Assumed pond capacity" preset or button. Pond A's 151,100 m³ need is then 81 % over; pond B's 83,600 m³ is 97 % of capacity. Today's default still claims no capacity (option a) |
| Pond owners | Ponds A and B are on JPS Selangor's phase-1 pond list (K02, K03, surveyed 2011) | sourced | M | Responsibility record only |
| Independent check | FastFlood (two runs) pools water in ponds A and B and along the trunk-drain corridor | checked | M | None; see [FASTFLOOD_CROSSCHECK.md](FASTFLOOD_CROSSCHECK.md) |
| Website levers | Upstream development 0–100 % (C interpolated linearly from today to the full change), upstream area 0–300 ha, built-out C 0.65–0.95, what-if pond 5,000–60,000 m³, trunk drain 3–14 m, ARI 2–100 yr | planner input | — | Each re-runs `screening.ts` in the browser; the method is unchanged, so parity with `screening.py` holds |

## 8. Added 21 Oct 2026: upkeep inputs (planner what-ifs, not sourced values)

| Input | Default | Meaning | Conf. |
|---|---|---|---|
| `trunk_drain.blockage` | 0 | Share of the shared drain's carrying capacity lost to silt and rubbish; Manning capacity × (1 − blockage), capped at 0.9 | — (planner input; no public record) |
| `storm.design_duration_h` | empty | Holds the design storm at one duration; the website sets it to the clear drain's critical duration whenever blockage is set, so the comparison faces the same storm | — |
| Pond storage lost (website only) | 0 | Cuts the capacity a pond is measured against; storage required is unchanged | — |

**[verify]:** scaling capacity in proportion to blockage is a simplification (a part-blocked
channel loses flow area and hydraulic radius, so the real loss can be larger). Confirm it is acceptable for screening.
