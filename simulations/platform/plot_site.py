"""Check map of a generated site pack: zones coloured by outlet, drains, ponds, rivers, the council line, JPS flood
records and the what-if pond. For the person checking a site before it is shown (the 'checking' part of the cost).

    python plot_site.py <id>      -> sites/<id>/check_map.png
"""
import itertools, json, os, sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from shapely.geometry import shape  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def parts(s):
    return list(s.geoms) if s.geom_type.startswith("Multi") or s.geom_type == "GeometryCollection" else [s]


def plot(site_id):
    d = os.path.join(HERE, "sites", site_id)
    geo = json.load(open(os.path.join(d, "geo.json"), encoding="utf-8"))
    inp = json.load(open(os.path.join(d, "inputs.json"), encoding="utf-8"))
    site = json.load(open(os.path.join(d, "site.json"), encoding="utf-8"))
    fig, ax = plt.subplots(figsize=(13, 13))
    pal, cols = itertools.cycle(plt.cm.tab20.colors), {}
    for f in geo["features"]:
        k, s = f["properties"]["kind"], shape(f["geometry"])
        if k == "zone":
            z = inp["zones"][f["properties"]["id"]]
            c = "#bbbbbb" if z["drains_to"] in ("TBD", "outfall") else cols.setdefault(z["drains_to"], next(pal))
            for p in parts(s):
                ax.fill(*p.exterior.xy, color=c, alpha=.45, lw=.5, ec="k")
            cp = s.representative_point()
            ax.text(cp.x, cp.y, f"{f['properties']['id']}\n→{z['drains_to'].replace('OSM_', '')}", fontsize=6, ha="center")
        elif k == "pond":
            for p in parts(s):
                ax.fill(*p.exterior.xy, color="#2a6fdb", alpha=.9)
            ax.text(s.centroid.x, s.centroid.y, f["properties"]["id"].replace("OSM_", ""), fontsize=6, color="navy")
        elif k == "drain":
            x = inp["drains"][f["properties"]["id"]]
            for ln in parts(s):
                ax.plot(*ln.xy, color="cyan", lw=2)
            p = s.representative_point()
            ax.text(p.x, p.y, f"{f['properties']['id']} {x['name'][:18]} →{x['drains_to']}", fontsize=6, color="darkcyan")
        elif k == "river":
            for ln in parts(s):
                ax.plot(*ln.xy, color="blue", lw=3)
        elif k == "council_line":
            for ln in parts(s):
                ax.plot(*ln.xy, color="red", lw=2, ls="--")
        elif k == "flood":
            ax.plot(*s.xy, "k^", ms=6)
        elif k == "whatif":
            for p in parts(s):
                ax.fill(*p.exterior.xy, color="magenta", alpha=.5)
    ax.set_title(f"{site['name']}: generated site pack, check map (grey = river or outlet not known; ▲ JPS flood "
                 f"record; red dashes = council line; magenta = what-if pond)", fontsize=9)
    ax.set_aspect(1.0)
    plt.tight_layout()
    out = os.path.join(d, "check_map.png")
    plt.savefig(out, dpi=90)
    print("wrote", out)


if __name__ == "__main__":
    plot(sys.argv[1])
