# HY — Checking the Two Assumptions the Result Rests On

**Owner:** team leader · **Date:** 21 October 2026 · **Confidence:** see each line
**Builds on:** [HY_screening_inputs.md](HY_screening_inputs.md) (the inputs), [FASTFLOOD_CROSSCHECK.md](FASTFLOOD_CROSSCHECK.md),
[TBD_VERIFY_RESOLUTION.md](TBD_VERIFY_RESOLUTION.md). **Wins over:** the "L, not measurable" notes on these two inputs.

## Answer in five lines

1. The shared trunk drain's size is still not known exactly (stays **L**), but imagery shows **no channel 8 m or wider**
   along it: a narrow grass-lined channel (water surface about 1–2 m) in 10–15 m grass reserves.
2. **Pond A falls short for any drain narrower than about 12 m**, so the main finding does not hang on the 6 m guess:
   a smaller drain only makes it worse. Confidence in the *finding*: **M**.
3. The 1.5 m live-storage band is **inside MSMA 2's own range**: its planning chart uses 1–3 m of flood storage and it
   caps normal pond depth at 3.0 m. Pond A would need about **2.7 m** to hold its storm; pond B about 1.5 m.
4. By MSMA's planning chart, **pond A is about the right size for a 1.5 m band if it can release** water as it fills.
   Our screening says it cannot, because the shared drain is full. **The shortfall is the shared drain, not the pond.**
5. The screening matches the official record and an independent model where it should, and **does not explain** the
   residents' "three times a year": that frequent flooding is more likely the street drains, which it does not model.

## 1. The trunk drain's size (was: "not measurable", L)

**Method.** Esri World Imagery at zoom 19 (0.298 m per pixel), five points along the OSM ditch chain from 101.429 E to
101.443 E, with the OSM line and a 1 m scale drawn on (`AR1_site_model/verification/trunk_drain_*`, made by
`trunk_drain_imagery.py`). Measured by eye.

| Point | What the imagery shows |
|---|---|
| 1 (101.4290 E) | Grassed reserve beside the road; a narrow dark channel, about 1 m |
| 2 (101.4320 E) | Narrow channel behind the terraces; a grass strip about 15 m wide to the road |
| 3 (101.4352 E) | A dark water strip about 2 m wide in grass; banks vegetated |
| 4 (101.4395 E) | Under trees by the road; not visible |
| 5 (101.4428 E) | Under the highway ramps at the council corner (the earlier "tree cover" note) |

**Reading.** No concrete channel 8 m or wider appears anywhere along the line (a 10 m channel would be about 33 pixels
across and plain to see; the main ditch it feeds was measured that way, 8–10 m, `ditchW3_z19.png`). What shows is a
grass-lined channel of a few metres; the grass reserves around it may carry extra water in a big storm (SDP's booklet
mentions 3.3 km of natural swales). The exact top width, depth and lining **stay L**: vegetation hides the banks.

**What the result does with that** (same inputs, only the drain changed; `screening.ts`):

| Drain top width | 3 m | 5 m | 6 m (used) | 8 m | 9 m | 10 m | 11 m | 12 m | 14 m |
|---|---|---|---|---|---|---|---|---|---|
| Pond A storage needed (m³) | 190,200 | 151,100 | 151,100 | 115,700 | 115,700 | 97,700 | 90,100 | 84,500 | 54,500 |
| Against the assumed 83,400 m³ | short | short | short | short | short | short | short | short (101 %) | room |
| Shared drain load, 100-yr storm | 126 % | 144 % | 101 % | 131 % | 105 % | 85 % | 111 % | 93 % | 70 % |

(The drain load is not monotonic because the critical storm duration changes with the drain.) **Conclusion:** for any
drain the imagery allows, pond A is short and the shared drain is at or over capacity. Confidence in the finding: **M**.

## 2. The live-storage band (was: 1.5 m, assumed, L)

**Source.** MSMA 2nd Edition (DID 2012), **Chapter 7 Detention Pond**, PDF from JPS Sarawak (`did.sarawak.gov.my`,
attachment "MSMA 2nd Edition. 2012"), downloaded 21 Oct 2026.

| MSMA 2 says | Where |
|---|---|
| "The maximum pond water depth should not exceed **3.0 m** under normal operating conditions…" | 7.2.6.2 a), p. 7-7 |
| Planning chart for pond area with **flood storage depths of 1, 2 and 3 m** (100-yr ARI, catchment slope 1 %, catchment < 100 ha) | Figure 7.5, p. 7-10 |
| Dry ponds: depth limited to 1.2 or 1.5 m for public safety, or fenced | 7.2.6 (e) |

| Pond | Water area (OSM) | Storage needed, 100-yr | Band needed to hold it | At 1.5 m |
|---|---|---|---|---|
| A (JPS K02) | 55,611 m² | 151,100 m³ | **2.7 m** (MSMA max 3.0 m) | 83,400 m³: short |
| B (JPS K03) | 57,255 m² | 83,600 m³ | **1.5 m** | 85,900 m³: just enough |

**The MSMA planning check (Figure 7.5).** Pond A's catchment (Z03 + Z04 + Z06) is 139.1 ha with an area-weighted C of
about 0.73; the pond is 5.56 ha, **4.0 %** of it. Read off the chart at C 0.73: about 4.5 % for 1 m of flood storage,
3.5 % for 2 m, 2.7 % for 3 m; about **4.0 % for 1.5 m**. So by MSMA's planning method pond A is about the size a 1.5 m
band needs, **on the chart's assumption that the pond releases as it fills.** The screening finds it cannot release,
because the shared drain is full (section 1). Limits: the chart is for catchments under 100 ha and a 1 % slope; pond A's
is 139 ha and flatter (about 0.13 %). JPS lists K02 as a 12-acre lot (4.9 ha), smaller than the OSM water area; using it
would lower the capacity.

**Conclusion:** 1.5 m is a fair, MSMA-consistent planning value (stays an assumption, but **L → M** for "reasonable").
Pond A is short unless its band is at least 2.7 m deep, close to MSMA's 3.0 m ceiling.

## 3. Does the result match what is known on the ground?

| Check | Result | Conf. |
|---|---|---|
| **JPS's own flood records** ("Bandar Bukit Raja", ponding, 2023 and 2024, at 3.0906 N 101.4317 E) | Fall in **Z03**, which the screening marks "not enough room" in the design storm | H (record), M (match) |
| **FastFlood**, an independent hydrodynamic model (global data, 100-yr storm) | Pools water in ponds A and B and along the trunk-drain corridor: the two places the screening flags | H / M |
| **Residents' flood street**, Jalan Makyong (Spot 1) | In **Z03**; FastFlood pools water within ~60 m of it in its larger run | M |
| **Does not explain:** residents report flooding "at least three times a year" | In a 2-year storm (50 % chance a year) the screening has pond A with room (71 %); only the shared-drain zones are short. Frequent flooding on Jalan Makyong is more likely the street drains (the minor system), which the screening does not model, and fits the residents' request for bigger drains | M |

## Assumptions

- Drain section: trapezoid, bottom half the top width, n 0.018 (concrete). If the channel is grass-lined, n is higher
  (about 0.03–0.035) and its capacity lower, which only strengthens the finding.
- Pond capacity = OSM water area × the band; side slopes and the permanent pool are not modelled.

## Limits

- Widths read by eye from imagery of unknown exact date (between about Dec 2025 and Sep 2026, per the verification
  README); no survey, no drawings.
- Figure 7.5 read by eye from the page image; ±0.2 % of catchment.
- The screening counts only the trunk drain as conveyance (stated on the site).

## Still open

- The drain's real cross-section (council or SDP drawings, if shortlisted). [TBD]
- Pond A's and B's design storage (SDP or JPS). [TBD]
- Esri imagery terms before any image goes public. [verify]
