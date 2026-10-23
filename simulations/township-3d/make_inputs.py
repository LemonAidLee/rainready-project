"""Write inputs.json for screening.py from the sourced values (research/HY_screening_inputs.md) and the measured land
cover (data/landcover.json). Re-run after the zones or land cover change:  python make_inputs.py

Statuses: sourced (a cited document) · measured (from the model geometry: areas and land cover only, never depths)
· assumed (a stated engineering assumption with reasoning; confidence given) · planner input (a what-if the user
sets; not a fact) · placeholder (none should remain).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
MSMA1 = "MSMA 2nd Edition (DID Malaysia, 2012), Chapter 1 Design Acceptance Criteria"
MSMA2 = "MSMA 2nd Edition (DID Malaysia, 2012), Chapter 2 Quantity Design Fundamentals"
LC = json.load(open(os.path.join(HERE, "data", "landcover.json"), encoding="utf-8"))["zones"]
Z = {z["id"]: z for z in json.load(open(os.path.join(HERE, "data", "zones.json"), encoding="utf-8"))["zones"]}


def v(value, unit, status, source, conf, note=None):
    d = dict(value=value, unit=unit, status=status, source=source, confidence=conf)
    if note:
        d["note"] = note
    return d


c_src = ("MSMA 2 Table 2.5 (Major System column) area-weighted by Eq. 2.4 over the zone's land cover in the model "
         "(landcover.py: terrace 0.90, commercial 0.95, park 0.40, bare 0.60, grass 0.50, roads 0.95, water 0.95)")
zones = {}
for k, z in Z.items():
    lc = LC[k]
    zones[k] = dict(
        name=z["name"], council=z["council"], drains_to=z["drains_to"],
        area_ha=v(z["area_ha"], "ha", "measured", "Plan area of the DRAFT zone (data/zones.json), water included", "M",
                  "Zone edges are a draft from mapped lines (TOWNSHIP_3D_AND_SIMULATOR.md 4.8), not an official catchment"),
        c_now=v(lc["c_now"], "-", "measured", c_src, "M",
                "Land cover is the SIMULATED model town; table values are H, the cover is M-L"),
        c_upstream=v(lc["c_upstream"], "-", "measured",
                     c_src + ("; upstream change: the 3.56 ha of invented aprons in Z01 become commercial (0.95)"
                              if lc["upstream_paved_ha"] else "; unchanged: the upstream change is in Z01 only"), "M"),
        cover_ha=lc["cover_ha"])

inp = {
    "_about": ("Inputs of the RainReady screening simulator v2 (screening.py / screening.ts). Researched 21 Oct 2026 by "
               "Claude for the team leader from MSMA 2nd Edition and public data; see research/HY_screening_inputs.md. "
               "Every value has a unit, status, source and confidence."),
    "_status_key": {"sourced": "from a cited document", "measured": "measured from the model (areas, land cover)",
                    "assumed": "a stated assumption with reasoning", "planner input": "a what-if set by the user"},
    "storm": {
        "ari_years": v(100, "years", "sourced", MSMA1 + ", Table 1.1: link house / apartment, major system 100 yr; "
                       "mixed developments take the highest ARI (Note 1)", "H"),
        "idf": {
            "station": "2913001 Pusat Kawalan JPS Telok Gong (Selangor)",
            "lambda": v(63.493, "-", "sourced", MSMA2 + ", Table 2.B1 (ARI 2-100 yr, 5 min-72 h), station 2913001", "H"),
            "kappa": v(0.170, "-", "sourced", MSMA2 + ", Table 2.B1, station 2913001", "H"),
            "theta": v(0.254, "-", "sourced", MSMA2 + ", Table 2.B1, station 2913001", "H"),
            "eta": v(0.872, "-", "sourced", MSMA2 + ", Table 2.B1, station 2913001", "H"),
            "station_choice": v("2913001", "-", "assumed",
                                "Nearest Selangor gauge in Table 2.B1 to BBR (3.09 N, 101.44 E). Location checked 21 Oct "
                                "2026 on JPS Selangor's own station layer (jpsselgis.selangor.gov.my, Hosted/"
                                "Stesen_Hidrologi, 'Stesen Rain Fall'): Telemetri Telok Gong at 2.9951 N, 101.3679 E, "
                                "about 13 km south-west of BBR, in Klang district, coastal like BBR; it matches the "
                                "station-number grid (29 = 2.9 N, 13 = 101.3 E). Nearer JPS gauges (Bandar Klang, Pekan "
                                "Meru) have no IDF constants in Table 2.B1. Neighbours 3314001 and 2815001 give a "
                                "sensitivity range",
                                "M", "Location H (JPS layer); that the telemetry station is the IDF gauge 2913001 is "
                                "inferred from the name and grid (M)")},
        "durations_h": v([0.5, 1, 2, 3, 6, 12, 24], "h", "assumed",
                         "MSMA 2.2.1: examine a range of storm durations; storm duration >= tc (MSMA 2.2.2). The "
                         "critical one (most storage) is reported", "M"),
        "design_duration_h": v(None, "h", "planner input",
                               "Empty: the design storm is today's critical duration. Set to one of durations_h to hold "
                               "the storm fixed, e.g. so a blocked drain is compared with the clean drain under the "
                               "same storm", "-"),
        "tc_hours": v(0.5, "h", "assumed",
                      "MSMA Table 2.1: overland flow (paved n* 0.015, 200 m, 1 % slope) ~9 min + drain flow (1 km, "
                      "n 0.018, R 0.5 m, S 0.0013) ~13 min = ~23 min, rounded up to 0.5 h. Used for the "
                      "pre-development peak (allowed release)", "L"),
    },
    "method": {
        "hydrograph_volume_factor": v(1.0, "-", "sourced",
                                      MSMA2 + ", 2.3.2 Rational Hydrograph Method: Type 1 trapezoid and Type 2 triangle "
                                      "both hold Q x d", "H"),
        "c_predevelopment": v(0.40, "-", "sourced",
                              MSMA2 + ", Table 2.5 'Sport Fields, Park and Agriculture' (major system). BBR was a "
                              "Sime Darby oil palm estate before the 2002 master plan (Wikipedia 'Bukit Raja'; EdgeProp)",
                              "M", "Used for MSMA 1.2.1 peak discharge control: Qpost <= Qpre"),
        "band_change_medium_from": v(1.05, "ratio", "assumed",
                                     "Team choice: a scenario needing 5 % more storage (or trunk demand) than today "
                                     "is 'medium'", "L"),
        "band_change_high_from": v(1.20, "ratio", "assumed", "Team choice: 20 % more than today is 'high'", "L"),
        "band_capacity_medium_from": v(0.80, "ratio", "assumed",
                                       "Team choice: storage required at 80 % of an entered stated capacity", "L"),
        "band_capacity_high_from": v(1.00, "ratio", "assumed",
                                     "At or above 100 % the entered capacity is exceeded", "M"),
    },
    "zones": zones,
    "external_inflows": {
        "EXT_A": {"name": "Area A beyond the model edge (upstream, Shah Alam side)", "council": "Shah Alam",
                  "drains_to": "trunk_drain", "enters_at": "the drain that crosses the council line (3.09294 N, 101.44433 E)",
                  "area_ha": v(50.0, "ha", "assumed",
                               "No usable upstream boundary exists (AR1, 11 Oct 2026: terrain routing failed; JPS "
                               "Kawasan_Tadahan unavailable). 50 ha is a stated test value; the website lets the "
                               "planner change it", "L"),
                  "c_now": v(LC["Z01"]["c_now"], "-", "assumed", "Same as the in-model part of Area A (Z01)", "L"),
                  "c_upstream": v(0.90, "-", "planner input",
                                  "Scenario definition: the remaining land develops as link and terrace housing "
                                  "(MSMA 2 Table 2.5, major system, 0.90), where peak control is not fully achieved. "
                                  "A what-if, not a forecast of Area A", "-")}},
    "trunk_drain": {
        "_what": "The east-west drain at y ~ 300 that carries the north side, Area A and the pond outlets west to the main ditch",
        "section": {
            "top_width_m": v(6.0, "m", "assumed",
                             "Not measurable (tree cover at the council corner, AR1 imagery). Between the model's 3 m "
                             "ditch and the 8-10 m main ditch it joins (AR1 imagery, 3.0976 N 101.4337 E)", "L"),
            "bottom_width_m": v(3.0, "m", "assumed", "Trapezoid like the main ditch (AR1 imagery)", "L"),
            "depth_m": v(2.0, "m", "assumed", "Typical for an urban concrete trunk drain; not measured", "L"),
            "manning_n": v(0.018, "-", "sourced", MSMA2 + ", Table 2.3: lined drain, concrete, rough finish", "H"),
            "slope": v(0.0013, "m/m", "assumed",
                       "Regional ground fall 1.3 m/km (AR1 plane fit to GLO-30 over 18 km2, M); drain gradients "
                       "inside the block cannot be read from the DEM", "L")},
        "blockage": v(0.0, "fraction", "planner input",
                      "Share of the drain's carrying capacity lost to silt and rubbish (0 = clean, as designed). Not "
                      "measured anywhere public; a maintenance what-if. Screening simplification: capacity scales by "
                      "(1 - blockage); capped at 0.9", "-"),
        "_limit": ("Only this drain is counted as conveyance; overland and road (major-system) flow paths are not, so "
                   "storage required is an upper-end screening figure")},
    "ponds": {
        "pond_A": {"osm_id": 399570465,
                   "capacity_m3": v(None, "m3", "planner input",
                                    "No public figure (AR1). Must not be measured from the model. Enter the stated "
                                    "capacity to see the gap", "-")},
        "pond_B": {"osm_id": 359496461,
                   "capacity_m3": v(None, "m3", "planner input", "No public figure (AR1). Enter the stated capacity", "-")}},
    "what_if_pond": {
        "_what": ("Illustrative new pond on land OSM tags brownfield (way 1267917541, 6.6 ha) in zone Z06, catching Z06 "
                  "runoff before pond A. A what-if, not a proposal"),
        "serves": ["Z06"], "osm_landuse": 1267917541, "drains_to": "pond_A",
        "capacity_m3": v(25000.0, "m3", "planner input", "Test size for the what-if (a planner input, not a fact)", "-"),
        "outlet_m3_s": v(0.0, "m3/s", "planner input",
                         "Default 0: the what-if pond holds what it catches during the storm and empties afterwards. "
                         "With the trunk drain full, a pond that passes flow on does not reduce pond A's storage", "-")},
    "scenarios": {
        "now": {"c": "c_now", "what_if_pond": False, "label": "Today's land cover"},
        "upstream": {"c": "c_upstream", "what_if_pond": False,
                     "label": "More paved land upstream, where peak control is not fully achieved"},
        "upstream_plus_pond": {"c": "c_upstream", "what_if_pond": True, "label": "Upstream change, plus a what-if pond"}},
}
json.dump(inp, open(os.path.join(HERE, "inputs.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote inputs.json")
