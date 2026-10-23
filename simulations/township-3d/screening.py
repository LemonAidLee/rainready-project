"""RainReady screening simulator (v2, 21 Oct 2026). Plain Python, no Blender, no third-party packages; ported to
TypeScript in screening.ts, held equal by check_parity.ts. THIS FILE IS THE REFERENCE.

Method, from MSMA 2nd Edition (DID 2012), per scenario and per candidate storm duration d:
  1. Rainfall intensity, MSMA Eq. 2.2:   i = lambda * T^kappa / (d + theta)^eta    (mm/hr; T = ARI in years,
     d in hours; constants for the chosen raingauge, MSMA Table 2.B1)
  2. Peak flow per zone, Rational Method, MSMA Eq. 2.3:   Q = C * i * A / 360   (m3/s; A in ha; MSMA: not
     recommended above 80 ha, and not for designing storage - this is screening, not design)
  3. Runoff volume, Rational Hydrograph Method (MSMA 2.3.2):   V = k * Q * d   (k = 1: the trapezoid / triangle
     hydrographs both hold Q * d)
  4. Allowed pond release, MSMA 1.2.1 (Qpost <= Qpre): the pre-development peak flow of the pond's catchment,
     C_pre * i(T, tc) * A / 360, further limited by the room left in the shared trunk drain
  5. Trunk drain: Manning's equation on an assumed trapezoid, times (1 - blockage), the share lost to silt and
     rubbish (planner input, default 0; a screening simplification). Zones and upstream inflows that drain straight
     to it use up part of its capacity; the spare is shared by the pond outlets in proportion to their allowed release
  6. Storage required = inflow volume - released volume. The design storm is TODAY's critical duration: the one
     that needs the most storage over all ponds (MSMA 2.2.1: examine a range of durations), unless the planner
     holds it fixed (storm.design_duration_h). Every scenario uses that same storm, so scenarios compare like for
     like; storage at every duration is reported too
  7. Pond capacity is a PLANNER INPUT (team leader, 21 Oct 2026, option a: no public figure exists, and it must
     not be measured from the model). Without it: no gap, no fill %. With it: gap = required - capacity
  8. Band per zone: against capacity where the planner gave one; otherwise the CHANGE VERSUS TODAY (ratio of the
     pond's storage required, or of the trunk drain's demand, to the 'now' scenario). Outlet TBD: 'unknown'
  9. What-if pond: catches its zones' runoff and releases at its outlet rate (a planner input; default 0, i.e. it
     holds what it catches during the storm and empties afterwards, which is what helps when the drain downstream
     is full); only the overflow passes on

Outputs: storage required, change versus today, gap (when a capacity is given), band per zone, a display gauge per
pond. NO depths, NO times to recede, NO compliance verdicts. A scenario difference is never an attribution.

Run:  python screening.py              -> prints the result, writes outputs.json
      python screening.py --check      -> self-checks only
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
INPUTS = os.path.join(HERE, "inputs.json")
OUTPUTS = os.path.join(HERE, "outputs.json")
ZONES = os.path.join(HERE, "data", "zones.json")


def val(x):
    return x["value"] if isinstance(x, dict) and "value" in x else x


def placeholders(node, path=""):
    """Every input still marked placeholder, as dotted paths."""
    out = []
    if isinstance(node, dict):
        if node.get("status") == "placeholder":
            return [path]
        for k, v in node.items():
            if not k.startswith("_"):
                out += placeholders(v, f"{path}.{k}" if path else k)
    return out


def idf_intensity(idf, ari_years, d_hours):
    """MSMA 2 Eq. 2.2 (valid for 2 <= T <= 100 years and 0.0833 <= d <= 72 hours)."""
    return val(idf["lambda"]) * ari_years ** val(idf["kappa"]) / (d_hours + val(idf["theta"])) ** val(idf["eta"])


def rational_q(c, i_mm_hr, a_ha):
    """MSMA 2 Eq. 2.3, peak flow in m3/s."""
    return c * i_mm_hr * a_ha / 360.0


def manning_trapezoid(section):
    """Full-bank capacity (m3/s) of a trapezoidal channel: Q = A R^(2/3) S^(1/2) / n."""
    b, top, h = val(section["bottom_width_m"]), val(section["top_width_m"]), val(section["depth_m"])
    area = (b + top) / 2.0 * h
    side = math.hypot((top - b) / 2.0, h)
    r = area / (b + 2.0 * side)
    return area * r ** (2.0 / 3.0) * math.sqrt(val(section["slope"])) / val(section["manning_n"])


def trunk_capacity(trunk):
    """Full-bank capacity less the share lost to silt and rubbish (planner input 'blockage', 0 if absent, capped 0.9)."""
    lost = min(0.9, max(0.0, val(trunk.get("blockage", 0.0)) or 0.0))
    return manning_trapezoid(trunk["section"]) * (1.0 - lost), lost


def band_of(ratio, medium_from, high_from):
    if ratio is None:
        return "unknown"
    return "high" if ratio >= high_from else "medium" if ratio >= medium_from else "low"


def capacity_of(p):
    v = val(p.get("capacity_m3"))
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 else None


def run_duration(inp, ckey, with_pond, d_hours):
    """Volume balance for one storm duration. Returns zones, ponds, trunk and what-if pond at that duration."""
    T = val(inp["storm"]["ari_years"])
    idf = inp["storm"]["idf"]
    i = idf_intensity(idf, T, d_hours)
    i_tc = idf_intensity(idf, T, val(inp["storm"]["tc_hours"]))
    dur_s = d_hours * 3600.0
    k = val(inp["method"]["hydrograph_volume_factor"])
    c_pre = val(inp["method"]["c_predevelopment"])

    zones = {}
    for zid, z in inp["zones"].items():
        q = rational_q(val(z[ckey]), i, val(z["area_ha"]))
        zones[zid] = dict(q_m3_s=q, v_m3=k * q * dur_s, drains_to=z["drains_to"])
    ext = {}
    for eid, e in inp.get("external_inflows", {}).items():
        q = rational_q(val(e[ckey]), i, val(e["area_ha"]))
        ext[eid] = dict(q_m3_s=q, v_m3=k * q * dur_s, drains_to=e["drains_to"])

    passed = {zid: (z["q_m3_s"], z["v_m3"]) for zid, z in zones.items()}
    new = None
    if with_pond:
        wp = inp["what_if_pond"]
        cap = capacity_of(wp)
        out_q = val(wp["outlet_m3_s"])
        v_in = sum(zones[s]["v_m3"] for s in wp["serves"])
        q_in = sum(zones[s]["q_m3_s"] for s in wp["serves"])
        v_rel = min(v_in, out_q * dur_s)
        need = v_in - v_rel
        over = max(0.0, need - cap) if cap else 0.0
        new = dict(inflow_m3=v_in, release_m3_s=out_q, released_m3=v_rel, storage_required_m3=need, capacity_m3=cap,
                   gap_m3=(need - cap) if cap else None, ratio=(need / cap) if cap else None)
        for s in wp["serves"]:
            w = zones[s]["v_m3"] / v_in if v_in else 0.0
            passed[s] = ((min(q_in, out_q) + over / dur_s) * w, (v_rel + over) * w)

    trunk_cap, blockage = trunk_capacity(inp["trunk_drain"])
    direct = sum(passed[z][0] for z, d in zones.items() if d["drains_to"] == "trunk_drain") + \
        sum(e["q_m3_s"] for e in ext.values() if e["drains_to"] == "trunk_drain")
    spare = max(0.0, trunk_cap - direct)
    allowed = {pid: rational_q(c_pre, i_tc, sum(val(z["area_ha"]) for z in inp["zones"].values()
                                                 if z["drains_to"] == pid)) for pid in inp["ponds"]}
    total_allowed = sum(allowed.values())
    share = 1.0 if total_allowed <= spare else spare / total_allowed if total_allowed else 0.0

    ponds = {}
    for pid, p in inp["ponds"].items():
        v_in = sum(passed[z][1] for z, d in zones.items() if d["drains_to"] == pid)
        q_rel = allowed[pid] * share
        v_rel = min(v_in, q_rel * dur_s)
        need = v_in - v_rel
        cap = capacity_of(p)
        ponds[pid] = dict(inflow_m3=v_in, allowed_release_m3_s=allowed[pid], release_m3_s=q_rel, released_m3=v_rel,
                          storage_required_m3=need, capacity_m3=cap, gap_m3=(need - cap) if cap else None,
                          ratio=(need / cap) if cap else None)
    trunk = dict(capacity_m3_s=trunk_cap, blockage=blockage, direct_demand_m3_s=direct, spare_for_ponds_m3_s=spare,
                 pond_release_share=share, ratio=direct / trunk_cap)
    return dict(duration_h=d_hours, intensity_mm_hr=i, intensity_tc_mm_hr=i_tc, zones=zones, external=ext,
                ponds=ponds, trunk_drain=trunk, what_if_pond=new)


def run_scenario(inp, name, design_h=None):
    """All durations for one scenario; the result is taken at design_h, or at the critical duration if None."""
    sc = inp["scenarios"][name]
    runs = [run_duration(inp, sc["c"], sc["what_if_pond"], d) for d in val(inp["storm"]["durations_h"])]
    if design_h is None:
        crit = max(runs, key=lambda r: sum(p["storage_required_m3"] for p in r["ponds"].values()))
    else:
        crit = next(r for r in runs if r["duration_h"] == design_h)
    crit["label"] = sc["label"]
    crit["storage_by_duration"] = [dict(duration_h=r["duration_h"],
                                        storage_required_m3={p: v["storage_required_m3"] for p, v in r["ponds"].items()})
                                   for r in runs]
    return crit


def add_bands(inp, scenarios):
    m = inp["method"]
    cap_med, cap_high = val(m["band_capacity_medium_from"]), val(m["band_capacity_high_from"])
    chg_med, chg_high = val(m["band_change_medium_from"]), val(m["band_change_high_from"])
    base = scenarios["now"]
    for name, sc in scenarios.items():
        for pid, p in sc["ponds"].items():
            b = base["ponds"][pid]["storage_required_m3"]
            p["change_vs_now"] = p["storage_required_m3"] / b if b else None
        t = sc["trunk_drain"]
        t["change_vs_now"] = t["direct_demand_m3_s"] / base["trunk_drain"]["direct_demand_m3_s"]
        for zid, z in sc["zones"].items():
            to = z["drains_to"]
            if to in sc["ponds"] and sc["ponds"][to]["ratio"] is not None:
                z.update(band_basis="capacity", ratio=sc["ponds"][to]["ratio"])
                z["band"] = band_of(z["ratio"], cap_med, cap_high)
            elif to in sc["ponds"]:
                z.update(band_basis="change_vs_now", ratio=sc["ponds"][to]["change_vs_now"])
                z["band"] = band_of(z["ratio"], chg_med, chg_high)
            elif to == "trunk_drain":
                z.update(band_basis="change_vs_now", ratio=sc["trunk_drain"]["change_vs_now"])
                z["band"] = band_of(z["ratio"], chg_med, chg_high)
            else:
                z.update(band_basis="unknown", ratio=None, band="unknown")
    # display gauge per pond: share of capacity if given, else of the largest requirement across the scenarios
    for pid in inp["ponds"]:
        top = max(sc["ponds"][pid]["storage_required_m3"] for sc in scenarios.values())
        for sc in scenarios.values():
            p = sc["ponds"][pid]
            if p["capacity_m3"]:
                p.update(gauge=min(1.0, p["storage_required_m3"] / p["capacity_m3"]), gauge_basis="capacity")
            else:
                p.update(gauge=p["storage_required_m3"] / top if top else 0.0, gauge_basis="largest_scenario")


def check_areas(inp):
    if not os.path.exists(ZONES):
        return []
    drawn = {z["id"]: z["area_ha"] for z in json.load(open(ZONES, encoding="utf-8"))["zones"]}
    return [f"{k}: inputs {val(z['area_ha'])} ha vs zones.json {drawn.get(k)} ha"
            for k, z in inp["zones"].items() if drawn.get(k) is not None and abs(drawn[k] - val(z["area_ha"])) > 0.05]


def run(inp):
    ph = placeholders(inp)
    fixed = val(inp["storm"].get("design_duration_h"))
    now = run_scenario(inp, "now", fixed if fixed in val(inp["storm"]["durations_h"]) else None)
    scenarios = {n: now if n == "now" else run_scenario(inp, n, now["duration_h"]) for n in inp["scenarios"]}
    add_bands(inp, scenarios)
    res = dict(illustrative=bool(ph), label="ILLUSTRATIVE VALUES - placeholder inputs" if ph else "",
               placeholder_inputs=ph, area_warnings=check_areas(inp),
               note="Screening only (MSMA 2 Rational Method + volume balance): storage required, change versus "
                    "today, band. No depths, no times, no verdicts. Not a design.",
               scenarios=scenarios)
    res["storage_change"] = {pid: dict(now_m3=scenarios["now"]["ponds"][pid]["storage_required_m3"],
                                       upstream_m3=scenarios["upstream"]["ponds"][pid]["storage_required_m3"],
                                       upstream_plus_pond_m3=scenarios["upstream_plus_pond"]["ponds"][pid]["storage_required_m3"])
                             for pid in inp["ponds"]} if {"now", "upstream", "upstream_plus_pond"} <= set(scenarios) else {}
    return res


def selfcheck():
    assert abs(rational_q(1.0, 360.0, 1.0) - 1.0) < 1e-12           # 1 ha, C 1, 360 mm/hr -> 1 m3/s
    idf = dict(**{k: dict(value=v) for k, v in (("lambda", 60.0), ("kappa", 0.0), ("theta", 0.0), ("eta", 1.0))})
    assert abs(idf_intensity(idf, 100, 2.0) - 30.0) < 1e-12          # 60 / 2
    sq = dict(bottom_width_m=1.0, top_width_m=1.0, depth_m=1.0, slope=1.0, manning_n=1.0)   # 1 x 1 m box
    assert abs(manning_trapezoid(sq) - (1 / 3) ** (2 / 3)) < 1e-12
    assert band_of(1.0, 1.05, 1.2) == "low" and band_of(1.1, 1.05, 1.2) == "medium" and band_of(1.3, 1.05, 1.2) == "high"
    inp = json.load(open(INPUTS, encoding="utf-8"))
    r = run(inp)
    for name, sc in r["scenarios"].items():
        for pid, p in sc["ponds"].items():
            assert abs(p["inflow_m3"] - p["released_m3"] - p["storage_required_m3"]) < 1e-6, (name, pid)
            assert 0 <= p["released_m3"] <= p["inflow_m3"] + 1e-9
            assert p["release_m3_s"] <= p["allowed_release_m3_s"] + 1e-12       # never above Qpre
        assert sc["duration_h"] in val(inp["storm"]["durations_h"])
        assert all(z["band"] == "low" or name != "now" or z["band_basis"] != "change_vs_now"
                   for z in sc["zones"].values())                              # today is the baseline
    for pid in inp["ponds"]:   # more paving upstream never needs less storage
        assert r["scenarios"]["upstream"]["ponds"][pid]["storage_required_m3"] >= \
            r["scenarios"]["now"]["ponds"][pid]["storage_required_m3"] - 1e-6
    for b in (0.3, 0.6):       # a blocked drain never needs less pond storage, and never carries more
        c = json.loads(json.dumps(inp))
        c["trunk_drain"]["blockage"] = dict(value=b)
        c["storm"]["design_duration_h"] = dict(value=r["scenarios"]["now"]["duration_h"])   # same storm as clean
        rb = run(c)
        for name, sc in rb["scenarios"].items():
            assert sc["trunk_drain"]["capacity_m3_s"] < r["scenarios"][name]["trunk_drain"]["capacity_m3_s"]
            assert sc["trunk_drain"]["ratio"] > r["scenarios"][name]["trunk_drain"]["ratio"]
            for pid, p in sc["ponds"].items():
                assert p["storage_required_m3"] >= r["scenarios"][name]["ponds"][pid]["storage_required_m3"] - 1e-6
    print("self-checks passed")


def report(r):
    if r["illustrative"]:
        print(f"*** {r['label']}: {r['placeholder_inputs']} ***")
    for w in r["area_warnings"]:
        print("area warning:", w)
    for name, sc in r["scenarios"].items():
        t = sc["trunk_drain"]
        print(f"\n== {name}: {sc['label']}  (critical duration {sc['duration_h']} h, i = {sc['intensity_mm_hr']:.1f} mm/hr)")
        print(f"   trunk drain: demand {t['direct_demand_m3_s']:.1f} of {t['capacity_m3_s']:.1f} m3/s "
              f"(x{t['change_vs_now']:.2f} vs today), spare for ponds {t['spare_for_ponds_m3_s']:.1f}")
        for pid, p in sc["ponds"].items():
            print(f"   {pid}: in {p['inflow_m3']:,.0f} m3, released {p['released_m3']:,.0f} "
                  f"(allowed {p['allowed_release_m3_s']:.2f}, got {p['release_m3_s']:.2f} m3/s), "
                  f"storage required {p['storage_required_m3']:,.0f} m3 (x{p['change_vs_now']:.3f} vs today)")
        if sc["what_if_pond"]:
            w = sc["what_if_pond"]
            print(f"   what-if pond: storage required {w['storage_required_m3']:,.0f} m3 of {w['capacity_m3'] or 0:,.0f}")
        print("   bands:", "  ".join(f"{z} {d['band']}" for z, d in sc["zones"].items()))


if __name__ == "__main__":
    if "--check" in sys.argv:
        selfcheck()
        sys.exit(0)
    inp = json.load(open(INPUTS, encoding="utf-8"))
    r = run(inp)
    report(r)
    json.dump(r, open(OUTPUTS, "w", encoding="utf-8"), indent=1)
    print("\nwrote", OUTPUTS)
