"""Overlay lines for the website (exports/overlays.json): the Klang / Shah Alam council line clipped to the model
rectangle, in model metres (x east, y north; origin 3.0900 N 101.4360 E, as plan_zones.py).

The site draws its own, larger boundary curtain and labels from this path (WEBSITE.md section 6), because the
14 m curtain in the .glb reads too small at website zoom. Drain paths are not exported here: the .glb already
carries each drain's path in its extras.

Run with system Python (needs shapely):  python export_web_overlays.py
"""
import json
import os

from shapely.geometry import LineString, box

HERE = os.path.dirname(os.path.abspath(__file__))
GIS = os.path.join(HERE, "..", "..", "research", "AR1_site_model", "gis")
MODEL = box(-1222, -830, 1700, 608)          # model rectangle, as MODEL in build_features.py


def proj(lon, lat):
    return ((lon - 101.436) * 111158.0, (lat - 3.09) * 110572.0)


def main():
    f = json.load(open(os.path.join(GIS, "council_line.geojson"), encoding="utf-8"))["features"][0]
    cs = f["geometry"]["coordinates"]
    line = LineString([proj(*c) for c in (cs[0] if f["geometry"]["type"] == "Polygon" else cs)])
    line = line.segmentize(10.0)                # densify first: the way starts 3.6 km outside the model
    clip = line.intersection(MODEL)
    parts = list(getattr(clip, "geoms", [clip]))
    paths = [[[round(x, 1), round(y, 1)] for x, y in p.coords] for p in parts if p.length > 20]
    out = {
        "_about": "Website overlays, model metres (x east, y north), origin 3.0900 N 101.4360 E. glTF = (x, up, -y).",
        "council_line": {"osm_way": 1231162275, "source": "OpenStreetMap administrative boundary, not cadastral",
                         "paths": paths},
    }
    os.makedirs(os.path.join(HERE, "exports"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "exports", "overlays.json"), "w"), separators=(",", ":"))
    print("council line:", len(paths), "part(s),", sum(len(p) for p in paths), "points,",
          round(clip.length), "m inside the model")


if __name__ == "__main__":
    main()
