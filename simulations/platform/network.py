"""RainReady network screening engine (22 Oct 2026). Plain Python, no third-party packages; ported to TypeScript in
network.ts, held equal by check_network.ts. THIS FILE IS THE REFERENCE for every site except BBR's 3D view, which
keeps simulations/township-3d/screening.py. On BBR's inputs (converted by bbr_to_network.py) both engines give the
same numbers: `python network.py --check` proves it.

The method is screening.py's (MSMA 2nd Edition, DID 2012), generalised from one trunk drain and one what-if pond to a
network of any size:
  1. Rainfall intensity, MSMA Eq. 2.2, constants for the site's raingauge (MSMA Table 2.B1)
  2. Peak flow per zone and per external inflow, Rational Method, MSMA Eq. 2.3: Q = C i A / 360
  3. Runoff volume, Rational Hydrograph Method (MSMA 2.3.2): V = k Q d
  4. What-if ponds (any number): each catches the zones it serves, releases at its outlet rate, and passes on only
     the overflow, split back over those zones in proportion to their runoff
  5. Drains (any number), in upstream-to-downstream order. A drain's DIRECT demand is the flow of the zones and
     inflows that reach it, plus everything leaving the drains upstream of it. Its capacity is Manning's equation
     on its (assumed or stated) trapezoid, times (1 - blockage). The spare (capacity - direct) is shared by the
     ponds that release into it, in proportion to their allowed release
  6. Ponds: allowed release = the pre-development peak flow of the pond's own catchment (MSMA 1.2.1, Qpost <= Qpre),
     limited by the spare in the drain it releases into (a pond releasing to "outfall" is not limited).
     Storage required = inflow volume - released volume
  7. Design storm = today's critical duration (the most storage over all ponds; with no ponds, the highest drain
     load), unless storm.design_duration_h holds it fixed. Every scenario uses that storm
  8. Bands, as screening.py: change versus today for every zone, pond and drain; and the capacity basis the website
     colours by: a zone's pond (storage required / capacity) or drain (direct demand / capacity)
  9. Boundaries: when zones and nodes carry a `council`, every link whose two ends lie on different sides is listed
     as a crossing, with its flow; and storage and capacity are totalled per side. A difference, never a blame

Outputs: storage required, change versus today, loads, bands, crossings. NO depths, NO times, NO verdicts.

Run:  python network.py <inputs.json> [<outputs.json>]   -> prints a summary, writes the outputs
      python network.py --check                          -> self-checks, incl. equality with screening.py on BBR
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUTFALL = "outfall"


def val(x):
    return x["value"] if isinstance(x, dict) and "value" in x else x


def placeholders(node, path=""):
    out = []
    if isinstance(node, dict):
        if node.get("status") == "placeholder":
            return [path]
        for k, v in node.items():
            if not k.startswith("_"):
                out += placeholders(v, f"{path}.{k}" if path else k)
    return out


def idf_intensity(idf, ari_years, d_hours):
    return val(idf["lambda"]) * ari_years ** val(idf["kappa"]) / (d_hours + val(idf["theta"])) ** val(idf["eta"])


def rational_q(c, i_mm_hr, a_ha):
    return c * i_mm_hr * a_ha / 360.0


def manning_trapezoid(section):
    b, top, h = val(section["bottom_width_m"]), val(section["top_width_m"]), val(section["depth_m"])
    area = (b + top) / 2.0 * h
    side = math.hypot((top - b) / 2.0, h)
    r = area / (b + 2.0 * side)
    return area * r ** (2.0 / 3.0) * math.sqrt(val(section["slope"])) / val(section["manning_n"])


def drain_capacity(d):
    lost = min(0.9, max(0.0, val(d.get("blockage", 0.0)) or 0.0))
    return manning_trapezoid(d["section"]) * (1.0 - lost), lost


def band_of(ratio, medium_from, high_from):
    if ratio is None:
        return "unknown"
    return "high" if ratio >= high_from else "medium" if ratio >= medium_from else "low"


def capacity_of(p):
    v = val(p.get("capacity_m3"))
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 else None


def drain_order(inp):
    """Drains upstream first. Raises on a loop or on a drain that leads nowhere."""
    drains = inp.get("drains", {})
    order, state = [], {}

    def visit(d):
        if state.get(d) == 2:
            return
        if state.get(d) == 1:
            raise ValueError(f"drain loop at {d}")
        state[d] = 1
        for u, x in drains.items():
            if x["drains_to"] == d:
                visit(u)
        state[d] = 2
        order.append(d)

    for d, x in drains.items():
        if x["drains_to"] != OUTFALL and x["drains_to"] not in drains:
            raise ValueError(f"drain {d} drains to unknown {x['drains_to']}")
    for d in drains:
        visit(d)
    return order


def validate(inp):
    """Drains and ponds must reach a known node. Returns a list of problems (empty when the network is sound). A zone
    or inflow may drain to an outlet not yet known (e.g. "TBD"): it is banded 'unknown', as in screening.py."""
    bad = []
    for k, p in inp.get("ponds", {}).items():
        if p["drains_to"] not in set(inp.get("drains", {})) | {OUTFALL}:
            bad.append(f"ponds.{k} must drain to a drain or the outfall, not {p['drains_to']}")
    for k, w in inp.get("what_if_ponds", {}).items():
        for s in w["serves"]:
            if s not in inp["zones"]:
                bad.append(f"what_if_ponds.{k} serves unknown zone {s}")
    try:
        drain_order(inp)
    except ValueError as e:
        bad.append(str(e))
    return bad


def run_duration(inp, ckey, whatifs, d_hours):
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

    # 4. what-if ponds
    passed = {zid: (z["q_m3_s"], z["v_m3"]) for zid, z in zones.items()}
    new = {}
    for wid in whatifs:
        wp = inp["what_if_ponds"][wid]
        cap = capacity_of(wp)
        out_q = val(wp["outlet_m3_s"])
        v_in = sum(zones[s]["v_m3"] for s in wp["serves"])
        q_in = sum(zones[s]["q_m3_s"] for s in wp["serves"])
        v_rel = min(v_in, out_q * dur_s)
        need = v_in - v_rel
        over = max(0.0, need - cap) if cap else 0.0
        new[wid] = dict(inflow_m3=v_in, release_m3_s=out_q, released_m3=v_rel, storage_required_m3=need,
                        capacity_m3=cap, gap_m3=(need - cap) if cap else None, ratio=(need / cap) if cap else None)
        for s in wp["serves"]:
            w = zones[s]["v_m3"] / v_in if v_in else 0.0
            passed[s] = ((min(q_in, out_q) + over / dur_s) * w, (v_rel + over) * w)

    # 6. allowed pond release: pre-development peak of the pond's own catchment
    allowed = {pid: rational_q(c_pre, i_tc, sum(val(z["area_ha"]) for z in inp["zones"].values() if z["drains_to"] == pid))
               for pid in inp.get("ponds", {})}

    # 5. drains, upstream first; ponds release into the spare of the drain they drain to
    drains, release = {}, {}
    for did in drain_order(inp):
        d = inp["drains"][did]
        cap, blockage = drain_capacity(d)
        direct = sum(passed[z][0] for z, x in zones.items() if x["drains_to"] == did) + \
            sum(e["q_m3_s"] for e in ext.values() if e["drains_to"] == did) + \
            sum(drains[u]["outflow_m3_s"] for u, x in inp["drains"].items() if x["drains_to"] == did)
        spare = max(0.0, cap - direct)
        mine = [pid for pid, p in inp.get("ponds", {}).items() if p["drains_to"] == did]
        total_allowed = sum(allowed[p] for p in mine)
        share = 1.0 if total_allowed <= spare else spare / total_allowed if total_allowed else 0.0
        for p in mine:
            release[p] = allowed[p] * share
        drains[did] = dict(capacity_m3_s=cap, blockage=blockage, direct_demand_m3_s=direct, spare_for_ponds_m3_s=spare,
                           pond_release_share=share, ratio=direct / cap if cap else None,
                           outflow_m3_s=direct + sum(release[p] for p in mine), drains_to=d["drains_to"])
    for pid, p in inp.get("ponds", {}).items():
        if p["drains_to"] == OUTFALL:
            release[pid] = allowed[pid]

    ponds = {}
    for pid, p in inp.get("ponds", {}).items():
        v_in = sum(passed[z][1] for z, x in zones.items() if x["drains_to"] == pid) + \
            sum(e["v_m3"] for e in ext.values() if e["drains_to"] == pid)
        q_rel = release[pid]
        v_rel = min(v_in, q_rel * dur_s)
        need = v_in - v_rel
        cap = capacity_of(p)
        ponds[pid] = dict(inflow_m3=v_in, allowed_release_m3_s=allowed[pid], release_m3_s=q_rel, released_m3=v_rel,
                          storage_required_m3=need, capacity_m3=cap, gap_m3=(need - cap) if cap else None,
                          ratio=(need / cap) if cap else None, drains_to=p["drains_to"])
    return dict(duration_h=d_hours, intensity_mm_hr=i, intensity_tc_mm_hr=i_tc, zones=zones, external=ext,
                ponds=ponds, drains=drains, what_if_ponds=new)


def scenario_whatifs(inp, sc):
    w = sc.get("what_if_ponds", [])
    return list(inp.get("what_if_ponds", {})) if w is True else [] if w is False else list(w)


def critical_key(r):
    if r["ponds"]:
        return sum(p["storage_required_m3"] for p in r["ponds"].values())
    return max((d["ratio"] or 0.0 for d in r["drains"].values()), default=0.0)


def run_scenario(inp, name, design_h=None):
    sc = inp["scenarios"][name]
    wi = scenario_whatifs(inp, sc)
    runs = [run_duration(inp, sc["c"], wi, d) for d in val(inp["storm"]["durations_h"])]
    crit = max(runs, key=critical_key) if design_h is None else next(r for r in runs if r["duration_h"] == design_h)
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
    for sc in scenarios.values():
        for pid, p in sc["ponds"].items():
            b = base["ponds"][pid]["storage_required_m3"]
            p["change_vs_now"] = p["storage_required_m3"] / b if b else None
        for did, d in sc["drains"].items():
            b = base["drains"][did]["direct_demand_m3_s"]
            d["change_vs_now"] = d["direct_demand_m3_s"] / b if b else None
        for zid, z in sc["zones"].items():
            to = z["drains_to"]
            node = sc["ponds"].get(to) or sc["drains"].get(to)
            # change basis (screening.py's): against capacity where a pond has a stated one, else the change
            if to in sc["ponds"] and node["ratio"] is not None:
                z.update(band_basis="capacity", ratio=node["ratio"], band=band_of(node["ratio"], cap_med, cap_high))
            elif node is not None:
                z.update(band_basis="change_vs_now", ratio=node["change_vs_now"],
                         band=band_of(node["change_vs_now"], chg_med, chg_high))
            else:
                z.update(band_basis="unknown", ratio=None, band="unknown")
            # capacity basis (what the website colours by): the load on whatever the zone reaches
            load = node["ratio"] if node is not None else None
            z.update(load=load, load_of=("pond" if to in sc["ponds"] else "drain" if to in sc["drains"] else None),
                     band_capacity=band_of(load, cap_med, cap_high))
        for d in sc["drains"].values():
            d["band_capacity"] = band_of(d["ratio"], cap_med, cap_high)
        for p in sc["ponds"].values():
            p["band_capacity"] = band_of(p["ratio"], cap_med, cap_high)


def side_of(inp, node_id):
    for kind in ("zones", "external_inflows", "drains", "ponds"):
        if node_id in inp.get(kind, {}):
            return inp[kind][node_id].get("council")
    return None


def add_boundaries(inp, scenarios):
    """Crossings (links whose ends lie in different councils) and storage per council. Empty without councils."""
    links = [("zone", z, x["drains_to"]) for z, x in inp["zones"].items()] + \
            [("inflow", e, x["drains_to"]) for e, x in inp.get("external_inflows", {}).items()] + \
            [("drain", d, x["drains_to"]) for d, x in inp.get("drains", {}).items()] + \
            [("pond", p, x["drains_to"]) for p, x in inp.get("ponds", {}).items()]
    for sc in scenarios.values():
        cross = []
        for kind, a, b in links:
            sa, sb = side_of(inp, a), side_of(inp, b)
            if sa and sb and sa != sb:
                q = (sc["zones"][a]["q_m3_s"] if kind == "zone" else sc["external"][a]["q_m3_s"] if kind == "inflow"
                     else sc["drains"][a]["outflow_m3_s"] if kind == "drain" else sc["ponds"][a]["release_m3_s"])
                cross.append(dict(kind=kind, source=a, to=b, from_side=sa, to_side=sb, flow_m3_s=q))
        sides = {}
        for pid, p in sc["ponds"].items():
            s = sides.setdefault(side_of(inp, pid) or "unknown", dict(storage_required_m3=0.0, capacity_m3=0.0,
                                                                      ponds=0, unstated=0))
            s["storage_required_m3"] += p["storage_required_m3"]
            s["ponds"] += 1
            if p["capacity_m3"]:
                s["capacity_m3"] += p["capacity_m3"]
            else:
                s["unstated"] += 1
        for s in sides.values():
            s["gap_m3"] = s["storage_required_m3"] - s["capacity_m3"] if not s["unstated"] else None
        sc["crossings"] = cross
        sc["by_side"] = sides


def run(inp):
    bad = validate(inp)
    if bad:
        raise ValueError("network problems: " + "; ".join(bad))
    ph = placeholders(inp)
    fixed = val(inp["storm"].get("design_duration_h"))
    now = run_scenario(inp, "now", fixed if fixed in val(inp["storm"]["durations_h"]) else None)
    scenarios = {n: now if n == "now" else run_scenario(inp, n, now["duration_h"]) for n in inp["scenarios"]}
    add_bands(inp, scenarios)
    add_boundaries(inp, scenarios)
    nodes = set(inp.get("drains", {})) | set(inp.get("ponds", {})) | {OUTFALL}
    unknown = [f"{k}: outlet {z['drains_to']}" for kind in ("zones", "external_inflows")
               for k, z in inp.get(kind, {}).items() if z["drains_to"] not in nodes]
    return dict(engine="network/1", illustrative=bool(ph), placeholder_inputs=ph, outlets_unknown=unknown,
                note="Screening only (MSMA 2 Rational Method + volume balance over a drain network): storage required, "
                     "change versus today, load, band. No depths, no times, no verdicts. Not a design.",
                scenarios=scenarios)


# ---------------------------------------------------------------------------------------------------- checks
def selfcheck():
    sys.path.insert(0, os.path.join(HERE, "..", "township-3d"))
    import screening
    from bbr_to_network import convert
    bbr = json.load(open(os.path.join(HERE, "..", "township-3d", "inputs.json"), encoding="utf-8"))
    a, b = screening.run(bbr), run(convert(bbr))
    worst = 0.0

    def same(x, y, what):
        nonlocal worst
        if x is None or y is None:
            assert x is None and y is None, what
            return
        e = abs(x - y) / max(1.0, abs(x))
        worst = max(worst, e)
        assert e < 1e-9, (what, x, y)

    for name in a["scenarios"]:
        sa, sb = a["scenarios"][name], b["scenarios"][name]
        same(sa["duration_h"], sb["duration_h"], (name, "duration"))
        for pid, p in sa["ponds"].items():
            for f in ("inflow_m3", "allowed_release_m3_s", "release_m3_s", "released_m3", "storage_required_m3",
                      "change_vs_now"):
                same(p[f], sb["ponds"][pid][f], (name, pid, f))
        t, d = sa["trunk_drain"], sb["drains"]["trunk_drain"]
        for f in ("capacity_m3_s", "direct_demand_m3_s", "spare_for_ponds_m3_s", "pond_release_share", "ratio",
                  "change_vs_now"):
            same(t[f], d[f], (name, "trunk", f))
        for zid, z in sa["zones"].items():
            assert z["band"] == sb["zones"][zid]["band"], (name, zid)
        if sa["what_if_pond"]:
            same(sa["what_if_pond"]["storage_required_m3"], sb["what_if_ponds"]["W1"]["storage_required_m3"], name)
    # BBR crosses the Klang / Shah Alam line: the upstream zones and Area A drain into a trunk drain on the Klang side
    assert any(c["from_side"] == "Shah Alam" for c in b["scenarios"]["now"]["crossings"])

    # a branched network checked by hand: two drains in series, a pond on each, one releasing to the outfall
    idf = {k: dict(value=v) for k, v in (("lambda", 60.0), ("kappa", 0.0), ("theta", 0.0), ("eta", 1.0))}
    sec = dict(bottom_width_m=1.0, top_width_m=1.0, depth_m=1.0, slope=1.0, manning_n=1.0)    # (1/3)^(2/3) m3/s
    cap = (1 / 3) ** (2 / 3)
    net = dict(storm=dict(ari_years=dict(value=100), idf=idf, durations_h=dict(value=[1.0]), tc_hours=dict(value=1.0)),
               method={k: dict(value=v) for k, v in (("hydrograph_volume_factor", 1.0), ("c_predevelopment", 0.3),
                                                     ("band_change_medium_from", 1.05), ("band_change_high_from", 1.2),
                                                     ("band_capacity_medium_from", 0.8), ("band_capacity_high_from", 1.0))},
               zones=dict(Z1=dict(area_ha=dict(value=1.0), c_now=dict(value=0.5), c_upstream=dict(value=0.5),
                                  drains_to="D1", council="X"),
                          Z2=dict(area_ha=dict(value=2.0), c_now=dict(value=0.5), c_upstream=dict(value=0.5),
                                  drains_to="P1", council="X"),
                          Z3=dict(area_ha=dict(value=1.0), c_now=dict(value=0.5), c_upstream=dict(value=0.5),
                                  drains_to="P2", council="Y")),
               drains=dict(D1=dict(section=sec, drains_to="D2", council="X"), D2=dict(section=sec, drains_to="outfall",
                                                                                    council="Y")),
               ponds=dict(P1=dict(capacity_m3=dict(value=None), drains_to="D2", council="X"),
                          P2=dict(capacity_m3=dict(value=None), drains_to="outfall", council="Y")),
               scenarios=dict(now=dict(c="c_now", label="now")))
    r = run(net)["scenarios"]["now"]
    i = 60.0                                                    # mm/h at 1 h
    q1, q2, q3 = 0.5 * i * 1 / 360, 0.5 * i * 2 / 360, 0.5 * i * 1 / 360
    assert abs(r["drains"]["D1"]["direct_demand_m3_s"] - q1) < 1e-12
    assert abs(r["drains"]["D2"]["direct_demand_m3_s"] - q1) < 1e-12             # D1's outflow passes on
    allowed1 = 0.3 * i * 2 / 360
    want = min(allowed1, cap - q1)                                                # P1 shares D2's spare
    assert abs(r["ponds"]["P1"]["release_m3_s"] - want) < 1e-12
    assert abs(r["ponds"]["P1"]["storage_required_m3"] - (q2 * 3600 - want * 3600)) < 1e-6
    assert abs(r["ponds"]["P2"]["release_m3_s"] - 0.3 * i * 1 / 360) < 1e-12      # outfall: not limited
    assert abs(r["ponds"]["P2"]["storage_required_m3"] - (q3 - 0.3 * i / 360) * 3600) < 1e-6
    assert {(c["source"], c["to"]) for c in r["crossings"]} == {("D1", "D2"), ("P1", "D2")}
    # a loop is refused
    loop = json.loads(json.dumps(net))
    loop["drains"]["D2"]["drains_to"] = "D1"
    assert validate(loop)
    print(f"self-checks passed (BBR: network = screening.py, worst relative difference {worst:.1e}; branched case by hand)")


def report(r):
    for name, sc in r["scenarios"].items():
        print(f"\n== {name}: {sc['label']}  (critical duration {sc['duration_h']} h, i = {sc['intensity_mm_hr']:.1f} mm/hr)")
        for did, d in sc["drains"].items():
            print(f"   drain {did}: {d['direct_demand_m3_s']:.2f} of {d['capacity_m3_s']:.2f} m3/s ({(d['ratio'] or 0) * 100:.0f} %)")
        for pid, p in sc["ponds"].items():
            cap = f" of {p['capacity_m3']:,.0f}" if p["capacity_m3"] else ""
            print(f"   pond {pid}: storage required {p['storage_required_m3']:,.0f}{cap} m3")
        for c in sc["crossings"]:
            print(f"   crossing: {c['kind']} {c['source']} ({c['from_side']}) -> {c['to']} ({c['to_side']}), {c['flow_m3_s']:.2f} m3/s")


if __name__ == "__main__":
    if "--check" in sys.argv:
        selfcheck()
        sys.exit(0)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(src), "outputs.json")
    res = run(json.load(open(src, encoding="utf-8")))
    report(res)
    json.dump(res, open(dst, "w", encoding="utf-8"), indent=1)
    print("\nwrote", dst)
