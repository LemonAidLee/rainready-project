"""Fetch Esri World Imagery around points on the trunk drain (OSM ditch chain) and draw the OSM line plus a metre
scale, to measure the channel's top width by eye. Usage: python drain_tiles.py <drains.geojson> <out_dir>"""
import io
import json
import math
import subprocess
import sys

from PIL import Image, ImageDraw

Z = 19
URL = "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"


def tile_xy(lon, lat, z=Z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return x, y


def fetch(x, y):
    b = subprocess.run(["curl", "-s", "-m", "60", URL.format(z=Z, x=x, y=y)], capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(b)).convert("RGB")


def main(drains, out):
    lines = []
    for f in json.load(open(drains, encoding="utf-8"))["features"]:
        g = f["geometry"]
        parts = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]
        for p in parts:
            if all(3.0915 < la < 3.0945 and 101.426 < lo < 101.446 for lo, la in p):   # the trunk drain band
                lines.append(p)
    points = [(101.4290, 3.0930), (101.4320, 3.0928), (101.4352, 3.0929), (101.4395, 3.0925), (101.4428, 3.0930)]
    mpp = 156543.03392 * math.cos(math.radians(3.093)) / 2 ** Z
    for i, (lo, la) in enumerate(points):
        cx, cy = tile_xy(lo, la)
        x0, y0 = int(cx) - 1, int(cy) - 1
        img = Image.new("RGB", (768, 768))
        for dx in range(3):
            for dy in range(3):
                img.paste(fetch(x0 + dx, y0 + dy), (dx * 256, dy * 256))
        d = ImageDraw.Draw(img)
        for p in lines:   # OSM centreline, thin, so the channel edges stay visible
            pts = [((tile_xy(a, b)[0] - x0) * 256, (tile_xy(a, b)[1] - y0) * 256) for a, b in p]
            d.line(pts, fill=(255, 220, 0), width=1)
        # 20 m scale with 1 m ticks, bottom left
        px = 1 / mpp
        d.rectangle([10, 730, 10 + 20 * px, 734], fill=(255, 255, 255))
        for m in range(21):
            h = 12 if m % 5 == 0 else 6
            d.line([10 + m * px, 734, 10 + m * px, 734 + h], fill=(255, 255, 255))
        d.text((12, 712), f"0-20 m (1 m ticks), {mpp:.3f} m/px, point {i + 1}: {la:.4f} N {lo:.4f} E", fill=(255, 255, 255))
        img.save(f"{out}/drain_{i + 1}.jpg", quality=92)
        print(f"drain_{i + 1}.jpg", f"{mpp:.3f} m/px")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
