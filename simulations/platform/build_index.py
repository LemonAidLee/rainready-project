"""The site registry: sites/index.json, read by the website's national map and portfolio view.

    python build_index.py

Adding a site = adding a folder sites/<id>/ with site.json, inputs.json and outputs.json (build_site.py writes all
three), then re-running this. No website code changes.

Per site and scenario it works out the same comparable numbers from the network outputs:
  storage gap   sum over ponds of (storage required - capacity) where positive. Capacity: stated, else ASSUMED
                (site.json assumed_capacity_m3 for BBR; generated sites carry their assumption in inputs.json), L
  over          ponds and drains loaded to 100 % or more of their (assumed) capacity
  crossings     links whose two ends are in different councils, and the flow across them
  area high     share of zone area whose outlet is loaded to 100 % or more
Ranking is by storage gap, then crossing flow. A screening comparison, not a verdict on any site.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SITES = os.path.join(HERE, "sites")


def val(x):
    return x["value"] if isinstance(x, dict) and "value" in x else x


def metrics(site, inp, sc):
    assumed = site.get("assumed_capacity_m3", {})
    gap, ponds_over = 0.0, 0
    for pid, p in sc["ponds"].items():
        cap = p["capacity_m3"] or assumed.get(pid)
        if cap:
            gap += max(0.0, p["storage_required_m3"] - cap)
            ponds_over += p["storage_required_m3"] >= cap
    drains_over = sum(1 for d in sc["drains"].values() if (d["ratio"] or 0) >= 1.0)
    area = {z: val(x["area_ha"]) for z, x in inp["zones"].items()}

    def load(z):
        to = z["drains_to"]
        if to in sc["ponds"]:
            p = sc["ponds"][to]
            cap = p["capacity_m3"] or assumed.get(to)
            return p["storage_required_m3"] / cap if cap else None
        return sc["drains"][to]["ratio"] if to in sc["drains"] else None
    high = sum(area[z] for z, x in sc["zones"].items() if (load(x) or 0) >= 1.0)
    return dict(storage_gap_m3=round(gap), ponds=len(sc["ponds"]), ponds_over=ponds_over, drains=len(sc["drains"]),
                drains_over=drains_over, crossings=len(sc["crossings"]),
                crossing_flow_m3_s=round(sum(c["flow_m3_s"] for c in sc["crossings"]), 2),
                area_ha=round(sum(area.values()), 1), area_high_ha=round(high, 1), duration_h=sc["duration_h"])


def build():
    sites = []
    for sid in sorted(os.listdir(SITES)):
        d = os.path.join(SITES, sid)
        if not os.path.exists(os.path.join(d, "site.json")):
            continue
        site = json.load(open(os.path.join(d, "site.json"), encoding="utf-8"))
        inp = json.load(open(os.path.join(d, "inputs.json"), encoding="utf-8"))
        out = json.load(open(os.path.join(d, "outputs.json"), encoding="utf-8"))
        entry = {k: site.get(k) for k in ("id", "name", "kind", "view", "route", "state", "centre", "councils",
                                          "confidence", "label", "summary", "tests")}
        entry["flood_records"] = len(site.get("evidence", {}).get("flood_records", []))
        entry["metrics"] = {n: metrics(site, inp, sc) for n, sc in out["scenarios"].items() if n in ("now", "upstream")}
        sites.append(entry)
    sites.sort(key=lambda s: (-s["metrics"]["now"]["storage_gap_m3"], -s["metrics"]["now"]["crossing_flow_m3_s"]))
    for k, s in enumerate(sites):
        s["rank"] = k + 1
    json.dump(dict(_about="RainReady site registry, written by simulations/platform/build_index.py. Screening "
                          "comparisons on mostly assumed inputs; not a verdict on any site.", sites=sites),
              open(os.path.join(SITES, "index.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for s in sites:
        m = s["metrics"]["now"]
        print(f"#{s['rank']} {s['id']}: gap {m['storage_gap_m3']:,} m3, ponds over {m['ponds_over']}/{m['ponds']}, "
              f"drains over {m['drains_over']}/{m['drains']}, crossings {m['crossings']} ({m['crossing_flow_m3_s']} m3/s)")


if __name__ == "__main__":
    build()
