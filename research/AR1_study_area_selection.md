# AR1 — Which section of Bandar Bukit Raja should the simulated city be based on?

**Owner:** Architecture (with Hydrology for the catchment extent) · **Date:** 11 October 2026 · **Confidence: M**

Method: online only. Street and boundary positions from OpenStreetMap (Nominatim and Overpass). Ground levels from a
global DEM via the Open-Meteo elevation API, which is roughly 90 m resolution and returns whole metres. Flood accounts
from the press sources already logged in
[BBR_PUBLIC_DOCUMENT_SURVEY.md](../documentation/supporting/BBR_PUBLIC_DOCUMENT_SURVEY.md).

---

## Answer in five lines

Model the **Phase 1 block around Jalan Makyong and Jalan Sumazau**, extended north-east far enough to cross the
Klang / Shah Alam council line. This single block contains everything the project argues about: the streets that
actually flood, the lowest ground in the township, at least two existing retention ponds, a water body on the Setia Alam
side, and the council boundary itself — all within about 3 km². Nothing else in BBR puts all five in one frame.

**Recommended 3D model extent**

| | From | To | Size |
|---|---|---|---|
| Latitude | 3.0845 N | 3.0955 N | ≈ 1.22 km |
| Longitude | 101.4250 E | 101.4470 E | ≈ 2.45 km |

≈ **3.0 km²**, landscape-proportioned, roughly 2:1.

**Recommended hydrology extent (larger, does not all need to be modelled in 3D):** 3.080–3.110 N, 101.415–101.465 E,
≈ 18 km². The physics needs the higher ground upstream or the inflow is invented.

---

## Why this block

### It is where the flooding is documented

Sinar Harian reports the residents' association saying flash floods hit **at least three times a year, especially
Jalan Makyong**, since the December 2021 flood. The 2024 memorandum asks specifically for more detention ponds in
**Phase 1, along Jalan Makyong and Jalan Sumazau**, and for larger drains on **Persiaran Sungai Keramat** and
**Persiaran Batu Belah**. A 2023 report describes roads at Jalan Makyong cut by up to 0.3 m of water. These are the only
BBR streets named repeatedly in public sources.

| Feature | Position (OSM) |
|---|---|
| Jalan Makyong (sections 2–4, KU5) | 3.0890–3.0921 N, 101.4239–101.4330 E |
| Jalan Sumazau (sections 1–4, KU5) | 3.0878–3.0910 N, 101.4365–101.4437 E |
| Persiaran Batu Belah | 3.0842–3.0860 N, 101.4332 E |
| Bandar Bukit Raja, suburb centroid | 3.0852 N, 101.4377 E |

Makyong and Sumazau sit side by side on the same latitude band, about 1.3 km apart, with Persiaran Batu Belah running
along the south. They form one compact block, not scattered points.

### It is the lowest ground in the township

A 10 × 10 DEM sample over 3.3 × 5.6 km gives this pattern (metres, north at top):

```
          101.410  101.422  101.434  101.447  101.459  101.465
 3.1100       6       13       4        9       10       17
 3.1033       8       12      14        7        6       11
 3.0967       7       12       9        8        8       13
 3.0900       5        5       5        7       11       25
 3.0833       5        6       4        6        6       36
```

The southern band, lat 3.083–3.090, is a flat plain at **4–6 m**. Everything north of it runs **7–14 m**, and there is a
hill in the south-east corner reaching **25–39 m**. Jalan Makyong reads 5 m and the retention ponds beside it read 4 m —
the lowest readings anywhere in the sample. The township's oldest phase was built on the flattest, lowest part of a
former oil palm estate, and the newer, higher phases drain toward it. That is the physical core of the whole pitch.

**Do not over-read this.** At roughly 90 m resolution and whole-metre output, a 1–2 m difference between neighbouring
cells is inside the error. Only the kilometre-scale pattern — low south, higher north, hill south-east — is dependable.

### The council boundary is right on its doorstep

Reverse geocoding brackets the Klang / Shah Alam line between two points 150 m apart:

| Point | Falls in |
|---|---|
| 3.0925 N, 101.4445 E | Bandaraya Klang |
| 3.0935 N, 101.4455 E | Shah Alam |

So the boundary runs through approximately **3.093 N, 101.445 E**, which is only about **500 m north-east of the top of
Jalan Sumazau**. The cross-boundary argument is not an abstraction here; a 3 km² model can show a flooded street in
Klang and the land draining toward it in Shah Alam in the same view. **[verify]** This is OSM's administrative boundary,
not an official cadastral source.

### It already contains the water infrastructure

| Feature | Position | Note |
|---|---|---|
| Flood retention pond A | 3.0892 N, 101.4348 E | Inside the Jalan Makyong block, DEM 4 m |
| Flood retention pond B | 3.0852 N, 101.4351 E | Beside Persiaran Batu Belah, DEM 4 m |
| Tasik Setia Alam | 3.0944 N, 101.4467 E | On the Shah Alam side, ~700 m from Jalan Sumazau |
| BBR Sales Gallery Park | 3.0855 N, 101.4325 E | Useful landmark |

**[verify]** These ponds are tagged `Flood Retention Pond` by OSM volunteers. Check each against satellite imagery
before modelling; the tag proves someone mapped water there, not the design or current condition.

### There is a plausible drainage corridor through it

In the DEM sample, the cells at 3.0933 N read 5 m at both 101.447 and 101.453 E, while the cells immediately north read
8–11 m. That low corridor curves south-west and joins the 5 m band along Jalan Makyong. A drainage path running from the
Setia Alam edge down into Phase 1 is therefore physically plausible, which is the claim the residents make. Extending
the model's eastern edge to about 101.447 keeps the head of that corridor inside the frame.

---

## What this rules out, and why

| Alternative | Why not |
|---|---|
| The whole township (4,405 acres, ~17.8 km²) | Too large to model well in the time available, and most of it is newer, higher phases and industrial land with no documented flooding |
| The Wetland Townpark as the centrepiece | It is the developer's best story, but it is not where the flooding is reported. Better as context than as the subject |
| Taman Mutiara Bukit Raja (3.0754 N, 101.4489 E) | The RM7.3m pond site is real and relevant, but it sits ~1.5 km south of the Phase 1 streets and would stretch the frame without adding a flooded street |
| The western pond cluster (3.094–3.097 N, 101.414–101.420 E) | Three OSM-tagged retention ponds, but they sit in Taman Klang Utama, outside the developer's township |
| Setia Alam itself | It is the upstream side of the argument, not the place that floods. Include its edge, not its centre |

---

## Assumptions

| # | Assumption | If it is wrong |
|---|---|---|
| 1 | Jalan Makyong and Jalan Sumazau are both in Phase 1 | Stated by the residents' association via Sinar Harian; if the phase labels differ, the study area is unaffected since it is drawn by coordinates |
| 2 | The OSM-tagged retention ponds exist and are roughly where tagged | The model would show ponds that are not there. Check imagery first |
| 3 | Ground falls from north-east to south-west across the block | Supported at km scale by the DEM, but the gradient is gentle and the data coarse. FABDEM will settle it |
| 4 | The council line runs near 3.093 N, 101.445 E | If it runs elsewhere, the model may need to extend further north-east to cross it |
| 5 | A 3 km² extent is enough to tell the story | If the catchment proves larger, keep the 3D extent and enlarge only the physics extent |

---

## Limits

- This picks a study area. It does **not** establish that upstream development causes the downstream flooding; that is
  HY3's question, and the terrain here is too coarse to settle it.
- No drain network, pond depth, pump rate or as-built level is public for any of this. Pond outlines from OSM are plan
  shapes only, with no depth.
- The Wetland Townpark could not be located precisely in OSM. There is a chain of unnamed water bodies running east from
  about 101.444 to 101.458 E at 3.089–3.095 N that may be part of it. **[verify]**
- Street positions are OSM volunteer data. They are good enough to lay out a *simulated* township loosely based on BBR,
  which is all we claim, and not good enough to present as a survey of the real one.
- Everything here is desk work. No one has been to the site.

---

## One figure

Schematic of the recommended extent, north at top. Not to scale.

```
        101.425                101.440         101.447
 3.0955 ┌───────────────────────────────────┬──────┐
        │                            SHAH ALAM ↗    │   higher ground, 7-14 m
        │   · · · · · · · · · · · ╭─── council line ┤   (upstream side)
 3.0944 │                         │   ○ Tasik Setia Alam
        │                      ╭──╯                 │
 3.0921 │  ══ Jalan Makyong ══════                  │   low corridor
 3.0910 │                      ══ Jalan Sumazau ══  │   runs SW into Phase 1
 3.0892 │      ▣ retention pond A (4 m)             │
        │                                           │   PHASE 1 PLAIN  4-6 m
 3.0860 │  ──── Persiaran Batu Belah ────           │   (the flooded block)
 3.0852 │      ▣ retention pond B (4 m)             │
 3.0845 └───────────────────────────────────────────┘
          ← to Sungai Puloh / Kapar Kecil outfalls
```

---

## Sources

- [Sinar Harian — residents face flash floods three times a year](https://www.sinarharian.com.my/article/666626/edisi/selangor-kl/penduduk-bandar-bukit-raja-hadap-banjir-kilat-tiga-kali-setahun)
- [Harian Metro — two retention ponds for Klang and Bukit Raja, Jan 2025](https://www.hmetro.com.my/mutakhir/2025/01/1175432/dua-kolam-takungan-kurangkan-risiko-banjir-bandar-klang-bukit-raja) *(headline only retrieved; body not accessible)*
- [Wikipedia — Bukit Raja](https://en.wikipedia.org/wiki/Bukit_Raja) (township 4,405 acres, Phase 1 launched 2002, former oil palm estate, extends to Jalan Sungai Puloh and the Setia Alam border)
- [Wetlands International Malaysia — Bandar Bukit Raja Town Park](https://malaysia.wetlands.org/bandar-bukit-raja-town-park/) (interconnected urban wetland cells; no position or size given)
- OpenStreetMap via Nominatim and Overpass, queried 11 October 2026 — street geometry, retention ponds, water bodies, place centroids, administrative boundaries
- Open-Meteo elevation API, queried 11 October 2026 — global DEM, ~90 m, whole-metre output
