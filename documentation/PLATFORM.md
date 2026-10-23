# RainReady Platform: From One Township to Any Township

**Written for:** the team leader and the next Claude session. **As of:** 22 October 2026.
**Decision (team leader, 22 Oct 2026):** build all three scaling stages today; site 2 chosen by Claude against the
three tests; AI site-setup assistant skipped; BBR's 3D view and the guided demo kept frozen. This extends the
implementation exception of 20–21 Oct (3D township, simulator, website).
**Why:** [../research/SCALING_PLATFORM.md](../research/SCALING_PLATFORM.md) (the ideas and the lock-in audit).
House rules apply on every screen: risk bands, never depths · a crossing is a difference, never a blame · every input
shows status, source and confidence · generated sites say "lower confidence".

## 1. What was built

| Stage | What | Where |
|---|---|---|
| 1. Site packs | A site is a folder (`site.json`, `inputs.json`, `outputs.json`, `geo.json`, `register_template.csv`). A registry (`sites/index.json`) lists them; the Malaysia map and the portfolio read it. `#/site/<id>` opens any site; `#/site/bbr` opens the 3D planner | `simulations/platform/sites/`, `build_index.py`; website `src/platform/` |
| 2. Second site, generated | **Seri Kembangan – Seri Serdang** (Subang Jaya ⇄ Kajang), built from open data by one command, shown in a 2D map view | `build_site.py`, `plot_site.py`; `#/site/serdang` |
| 3.1 General water network | Any number of drains (in series or branching), ponds and what-if ponds. Same MSMA 2 method as `screening.py` | `network.py` (reference), `network.ts` (port) |
| 3.2 Boundary layer | Every link whose two ends lie in different councils, with its flow; storage required vs capacity per council side | `network.py` `add_boundaries`; Boundary tab |
| 3.3 Upload | A planner's CSV or GeoJSON register (pond capacity or live depth; drain sizes) replaces our assumptions in the browser, as "planner input" with its source; unmatched rows are listed, never guessed | `src/platform/data.ts` `applyRegister`; Upload tab |
| 3.4 Portfolio | All sites ranked by storage gap, then flow across council lines; today or open land built out | `#/sites` |
| 3.5 AI site-setup assistant | **Skipped** (team leader, 22 Oct 2026): it needs a live model and an API key on a public site | — |

## 2. "Done when", as delivered

| Stage | Criterion | Result |
|---|---|---|
| 1 | BBR looks and behaves as before | **Met.** The guided demo's first frame still reads "1 · BANDAR BUKIT RAJA" with no site list (checked in Chromium); planner loads with 0 console errors or warnings; `public/data` and `screening.ts` unchanged (git) |
| 1 | Numbers identical | **Met.** `check_parity.ts` 216 cases; `network.py --check`: the network engine equals `screening.py` on BBR (worst difference 0) |
| 1 | No BBR text in the code | **Changed (honest deviation).** BBR's 3D view, Findings, Recovery and the demo keep their BBR text, because the demo was to stay frozen. The platform code (`src/platform/`) holds no site text: everything comes from the site pack |
| 1 | Old addresses work | **Met.** `#/`, `#/planner`, `#/brief`, `#/demo?play&clean` unchanged |
| 1 | Registry, no code change to add a site | **Met.** Folder + `build_index.py` |
| 1 | Build passes | **Met.** Production build; desktop 1600 × 900 and phone 390 × 844 checked |
| 2 | One command builds a pack | **Met.** `build_site.py` |
| 2 | Every value labelled | **Met.** Status, source, confidence on every input |
| 2 | 2D view with zones, ponds, drains, boundary, scenarios, cards, inputs | **Met.** Plus a "lower confidence" pill and a warning box |
| 2 | Passes the three tests | **Met.** 19 JPS flood records (2017–2024); 8 crossing links; 5 ponds on JPS's list |
| 2 | Real time recorded | **Met.** Fresh downloads 207 s (public Overpass servers busy, with retries) + processing 14 s ≈ **3.7 min**. Checking: one review of the check map found 3 generator faults, fixed in the generator (section 5). A person's checking time per site is **[TBD]**, not yet measured |
| 3 | Network: BBR unchanged, branched case by hand, parity | **Met.** 630 Python ⇄ TypeScript cases (BBR, Seri Kembangan, a branched network) |
| 3 | Boundary, upload, portfolio | **Met.** Upload tested with a throwaway register: match by JPS code, by our id, by position (150 m), and an unmatched row reported |
| 3 | Docs | This file; decision 33 in [PROJECT_STATUS.md](PROJECT_STATUS.md) |
| All | Seen by the team leader before going live | **Met.** Approved and pushed 22 Oct 2026 (commit `666d72c`), live at https://rainready-wheat.vercel.app; checked live with 0 console errors |

## 3. How to run

```
cd simulations/platform
python build_site.py <id> "<name>" <south> <west> <north> <east>   # downloads to sites/<id>/source/ (cached; --refresh to re-fetch)
python plot_site.py <id>                                          # sites/<id>/check_map.png: look at it before showing the site
python build_index.py                                             # sites/index.json (the registry)
python network.py --check                                         # engine self-checks, incl. = screening.py on BBR
node --experimental-strip-types check_network.ts                  # Python ⇄ TypeScript parity over every site
python bbr_to_network.py                                          # after any change to simulations/township-3d/inputs.json
cd ../../website && npm run build                                 # sync copies network.ts and the site packs into the site
```

Needs `shapely`, `pyproj`, `rasterio`, `numpy`, `requests` (all installed; plain `python`, not `python -I`).

## 4. Site 2: how it was chosen

Scored on 22 Oct 2026 from JPS Selangor's pond list (652 ponds, public ArcGIS layer) and the JPS flood records already
on the site, then checked for a council line with OSM (admin_level 7).

| Candidate | JPS flood records within 2 km | Ponds on JPS's list | Council line | Kind of flood | Result |
|---|---|---|---|---|---|
| **Seri Kembangan – Seri Serdang** | 19 (2017–2024; BESRAYA U-turn / Bluewater estate in 2017, 2018, 2019, 2022, 2023, 2024) | 3 near the centre (5 in the final extent) | Subang Jaya ⇄ Kajang, ~1.2 km east | Urban flash flood | **Chosen** |
| Puchong (IOI / LDP) | 5 | 4 | Not settled: 1 of 5 lookups answered (Subang Jaya); the rest hit server errors | Ponding | Second |
| Rawang | 12 | 19 | Not settled: 2 of 5 lookups answered, both Selayang; the rest hit server errors | Flash flood, kampung and town | Not chosen |
| Dengkil / Jenderam clusters | 6–36 | 2–9 | — | River and monsoon floods, villages | Out of scope (method does not model rivers) |
| Taman Sri Muda | 13 | 2 | — | River and pump failure (2021) | Out of scope, as above |

Not an SDP township. Choosing one of SDP's (strategic fit) remains open; `build_site.py` can build any Selangor
extent in minutes, outside Selangor it needs that state's MSMA gauges and pond list.

## 5. How a site is generated (and the three faults found by checking)

Full method in the header of [`build_site.py`](../simulations/platform/build_site.py). In short: OSM roads, railways,
waterways, water, land use, buildings and council lines; Copernicus GLO-30 only to tell which end of a drain is
lower; JPS's pond list plus OSM water ≥ 0.2 ha; the area cut along mapped lines into blocks; each block drains to the
pond it touches, the drain on its edge, a river on its edge, or (fallback, L) the nearest drain or pond 2 m lower;
blocks merged by outlet and council up to 75 ha; runoff C from MSMA 2 Table 2.5 over land cover (as `landcover.py`);
nearest MSMA 2 Table 2.B1 gauge (positions from JPS's own station layer,
[`data/msma2_idf_selangor.json`](../simulations/platform/data/msma2_idf_selangor.json)); pond capacity assumed = water
area × 1.5 m (BBR's stated rule, L); drain sizes typical by OSM type (L).

The first check map showed three faults; each was fixed **in the generator**, so they do not recur at the next site:

1. Blocks beside the river drained into small ditches → a block on a river's edge now drains to the river (where water
   leaves; not modelled).
2. Sungai Kuyoh is tagged `ditch` in OSM → a named *Sungai* / *Sg* / *Parit* is at least stream-sized; and a drain is
   never smaller than one that flows into it.
3. The Kajang side has no mapped drains → terrain fallback, labelled L on every zone it touches.

## 6. What the screen shows (and what it does not)

- **Seri Kembangan, today:** storage gap 92,694 m³ (5 of 15 ponds over their *assumed* capacity), 4 of 7 drains over
  their *assumed* size, 8 links from the Kajang side into Subang Jaya ponds and drains; pond P13 (JPS-listed, by the
  BESRAYA / Bluewater flood records) receives Kajang-side zones. All screening on mostly L inputs.
- **BBR in the portfolio** uses the same assumed-capacity rule as its planner view (83,400 / 85,900 m³, L).
- Not shown: depths, times, verdicts, any ranking of *who* is at fault. Rivers are where water leaves the model.

## 7. Files

| Path | What |
|---|---|
| `simulations/platform/network.py`, `network.ts`, `check_network.ts` | Engine, port, parity check |
| `simulations/platform/bbr_to_network.py` | BBR's inputs in network form (no values changed) |
| `simulations/platform/build_site.py`, `plot_site.py`, `build_index.py` | Generator, check map, registry |
| `simulations/platform/data/` | `msma2_idf_selangor.json` (Table 2.B1, Selangor); `jps_ponds_selangor.geojson` (JPS pond list; staff names and land-title numbers dropped) |
| `simulations/platform/sites/<id>/` | Site packs; `source/` holds the raw downloads (not copied to the website) |
| `website/src/platform/` | `Root.tsx` (routes), `SiteView.tsx`, `Portfolio.tsx`, `data.ts`, `platform.css` |
| `website/public/sites/` | Synced copies of the packs |

Website edits outside `src/platform/`: `main.tsx` (renders `Root`), `Landing.tsx` and `Globe.tsx` (site list, rings
and the catchment readout, **only outside the guided demo**), `App.tsx` (passes `inDemo`), `scripts/sync-data.mjs`.

## 8. Open

- [TBD] Measure a person's checking time on a third site; that, not the 3.7 min, is the real cost per site.
- [verify] Drain sizes at Seri Kembangan (Sungai Kuyoh especially) from imagery, as was done for BBR's trunk drain.
- [open] An SDP township as site 3 (strategic fit), and who pays outside developer land (THREE_CHALLENGES_REVIEW 3).
- [open] Responsibility rules outside Selangor; MSMA gauges and pond lists for other states.
- The basemap uses OpenStreetMap's public tiles (fine for a demo; heavy use needs a tile provider).

## 9. The 2D site app: every 3D feature, made for a map (22 Oct 2026, team leader)

**Request:** sites without a 3D model should still have everything the BBR planner has, animations included.
Code: `website/src/platform/` — `SiteApp.tsx` (the app), `MapView.tsx` (map and animations), `Rain2D.tsx`,
`Panels.tsx` (frame and panels), `model.ts` (levers and presets), `Tour.tsx`, `Findings.tsx`, `SitePanels.tsx`.
The engine is unchanged: every lever edits a copy of the site's inputs and re-runs `network.ts` in the browser, with two
scenarios per run (today, and these settings) so every change reads as a difference from today.

| BBR 3D planner | 2D site |
|---|---|
| Status bar (storm, scenario, drain load, status pill, guided demo) | Same; the drain readout becomes the storage gap |
| Icon rail | Same, plus Site (the site's tabs) and All sites |
| Scenario control: 9 presets in 4 groups with live summaries, hover tips | Same 9 presets for any network (half / full build-out, retrofit pond, drains ×1.5, together, silted and blocked, enlarged then clogged), live summaries, hover tips |
| Levers: next parcels, retrofit pond, drain works, upkeep (silt, blocked), design storm, stated capacities, reset | Open land built (0–100 %), what-if pond on/size, drain works (every mapped drain × 0.5–3), upkeep (silt, blocked; storm held), design storm 2–100 yr, stated capacity for the five fullest ponds (or a whole register by upload), reset |
| Rain | Rain drawn over the map, density by intensity; the basemap darkens in the storm |
| Flow arrows on drains | Drains animate downhill (drawn high end first by `build_site.py`), faster and redder as they fill; every zone has an animated flow line to its outlet, **gold where it crosses a council line** |
| Pond fill | Pond fill gauges (fullest eight) and a ripple in the storm |
| Upstream blocks rising | Blocks with open land hatch in gold as the build-out lever moves |
| What-if pond appears | The pond grows in on its parcel |
| Township reveal | Zones reveal in sequence as the site opens; the storm comes on |
| Pointers when a lever moves | Gold rings with a label on the zones, ponds or drains the lever moves (2.6 s) |
| Zone tags with ▲ / ▼ | Same |
| Results panel, inspector card, legend, cursor and zone readout, LIVE COMPUTE, evidence ticker | Same; the ticker carries the site's own JPS flood records |
| Layers panel | Zones, labels and gauges, flow, council boundary, JPS records, resident reports, street map |
| Resident report pins | Open reports inside the site's extent |
| Findings (Shared Capacity Brief) | `#/site/<id>/findings`: ponds, drains, options side by side, crossings, who looks after what (only JPS's list; all else [TBD]), limits. Printable |
| Guided demo (12 steps, captions read live, spotlights, autoplay, keys, clean frame) | `#/site/<id>/tour` (`?play&clean` for recording): 12 steps generated for any site, captions computed from its own results |
| 3D / TOP camera | Not applicable; a reset-view button instead |
| Resident door, Recovery | Shared with BBR (the rail links to them); not rebuilt per site |

## 10. Sites 3 and 4 (22 Oct 2026, team leader)

Chosen the same way as site 2: urban flood clusters in JPS Selangor's records, scored on records and listed ponds, then
**built** and kept only if the generator's own three tests pass. Five candidates were built; two passed.

| Site | Extent | JPS flood records | Council line, crossings | Listed ponds | Result |
|---|---|---|---|---|---|
| **Kota Kemuning – Bukit Kemuning** (`kemuning`) | 2.972–3.022 N, 101.490–101.530 E | 32 (2017–2024) | Shah Alam ⇄ Klang, 1 link (the line runs along a mapped ditch, D01) | 1 | **Site 3** |
| **Padang Jawa – Batu Tiga** (`batutiga`) | 3.042–3.079 N, 101.465–101.502 E | 32 (2017–2024; Kg Air Kuning, Bukit Kuda, Padang Jawa, Taman Rashna, Sungai Rasau) | Klang ⇄ Shah Alam, 4 links (Klang-side zones and a ditch into Shah Alam's D01b) | 2 | **Site 4** |
| Puchong – IOI | | 5 | none: wholly in Subang Jaya | 7 | Rejected |
| Subang | | 9 | PJ and Shah Alam inside, no drain links them | 2 | Rejected |
| Klang South (Taman Saujana, Kota Raja) | | 25 | Klang and Shah Alam inside, no drain links them | 1 | Rejected |
| Rawang town | | 15 | none: wholly in Selayang | 3 | Rejected |

Rejected packs are kept in `simulations/platform/rejected/` with a README. Kemuning's first extent clipped the line only
at a corner and was moved; a shifted extent lost its one listed pond; the final, taller extent holds both. Download
times with the public servers busy: Kemuning 348 s, Padang Jawa 222 s; processing 17 s and 8 s.

**Generator fix found by site 3:** an extent that straddles a whole degree (3.0 N) needs two Copernicus tiles; the
generator read one and failed. It now merges every tile the extent touches.

**Honest weak points:** Kemuning's single crossing is thin, and most of its drains are tagged `ditch` in OSM, so they
get the smallest assumed size and many run red: a result about the assumption as much as the place (the drain-works
lever shows how much). Padang Jawa – Batu Tiga lies about 5 km south-east of BBR; the extents do not overlap.
