# Input Request: Screening Simulator and Draft Zones

> **Superseded 21 Oct 2026.** The pair could not supply these values; Claude sourced them from MSMA 2nd Edition and
> public data: [../research/HY_screening_inputs.md](../../research/HY_screening_inputs.md). The zone sign-off (section A)
> and the open items in that file's section 6 still stand. Kept as the record of what was asked.

**For:** the hydrology pair. **From:** team leader. **As of:** 20 October 2026. **Needed by:** 22 Oct 2026, end of
day, so the video and deck can use real values before the 23 Oct deadline **[confirm date with the pair]**.

The simulator ([`screening.py`](../../simulations/township-3d/screening.py)) runs end to end and drives the 3D model, but
**every hydrology value is a placeholder**: round numbers picked so the demo shows every band, saying nothing about BBR.
Until you replace them, every frame says "illustrative values". Edit
[`inputs.json`](../../simulations/township-3d/inputs.json) directly. For each value, set `value`, change `status` to
`sourced` or `assumed`, and write the `source`. Then run `python screening.py --check` and `python screening.py`.
Method: Rational Method `Q = C·i·A/360` per zone, then a volume balance per pond. Detail is in
[TOWNSHIP_3D_AND_SIMULATOR.md](../TOWNSHIP_3D_AND_SIMULATOR.md) section 5.

## A. Sign off the zones first (areas depend on them)

Check map: [`data/zones_check.png`](../../simulations/township-3d/data/zones_check.png). For each of Z01–Z09, confirm or
redraw: (1) the edges, (2) where it drains (`drains_to`), (3) the route. Flagged doubts: **Z05** (no mapped drain:
does it go to the trunk drain or to pond B?), **Z06** (no internal drain), **Z09** (outlet unknown), the drains at the
**council corner** that run north out of the model, and whether **ponds A and B act as one linked system**. Is a
**77 ha** zone (Z07) within the Rational Method's limit in MSMA 2 **[verify the limit]**?

## B. Values we need

| # | Value (key in `inputs.json`) | Unit | Placeholder now | Where to source it |
|---|---|---|---|---|
| 1 | Design ARI (`storm.ari_years`) | years | 100 | MSMA 2 design criteria for minor and major drainage. Pick one, and say why |
| 2 | Rainfall intensity (`storm.intensity_mm_hr`) | mm/hr | 100 | MSMA 2 IDF curves or coefficients for the station nearest Klang, at the chosen ARI and duration. **[verify which station MSMA 2 lists]** |
| 3 | Storm duration (`storm.duration_min`) | min | 60 | At least the time of concentration (MSMA 2 tc formulas). Or the critical duration for storage, if you run several |
| 4 | Runoff coefficient now, per zone (`zones.Zxx.c_now`) | – | 0.45–0.55 | MSMA 2 runoff-coefficient table by land use, area-weighted. Land use from OSM `landuse_osm.geojson` and the model |
| 5 | Runoff coefficient after the upstream change (`zones.Z01.c_upstream`, `external_inflows.EXT_A.c_upstream`) | – | 0.75 | The same table, for "more paved land" in Area A. State the land-use change you assume |
| 6 | Upstream area beyond the model edge (`external_inflows.EXT_A.area_ha`) | ha | 50 | The area draining through the council-line crossing drain. JPS `Kawasan_Tadahan` (server was down on 11 Oct; retry) or a trace along the drain network. AR1's terrain method failed here; do not reuse it |
| 7 | Trunk drain capacity (`trunk_drain.capacity_m3_s`) | m³/s | 40 | Manning's equation with an assumed section and slope (state both), or a JPS / council figure. AR1 has the main ditch top width at 8–10 m from imagery |
| 8 | Pond A and B capacity (`ponds.*.capacity_m3`) | m³ | 60,000 / 40,000 | A stated figure only: SDP, MBDK (Klang council), or the JPS `KOLAM_TAKUNGAN_MSMA` layer. **Never measure it from the model.** The booklet's 16,000 / 34,000 / 50,000 m³ is the Wetland Townpark, not these ponds |
| 9 | Pond outlet release (`ponds.*.outlet_m3_s`) | m³/s | 6 / 3 | Outlet structure size if published. Otherwise a stated assumption |
| 10 | Normal water level (`ponds.*.start_fill_pct`) | share | 0.15 | Display only. Wet or dry pond? |
| 11 | Hydrograph volume factor (`method.hydrograph_volume_factor`) | – | 1.0 | Your choice of hydrograph (rectangle = 1.0; triangle; or the MSMA 2 procedure) |
| 12 | Band thresholds (`method.band_medium_from`, `band_high_from`) | ratio | 0.8 / 1.0 | Your call. Write it in the assumption ledger |
| 13 | What-if pond size and release (`what_if_pond.*`) | m³, m³/s | 25,000 / 1.0 | A test size for the demo (a planner input, not a fact) |

If a value cannot be sourced in time, mark it `assumed`, with one line of reasoning. An honest assumption beats a
placeholder. Anything still `placeholder` keeps the "illustrative values" label on screen.

**Out of scope, by house rule:** no water depths, no times to recede, no compliance verdicts, no forecast.
