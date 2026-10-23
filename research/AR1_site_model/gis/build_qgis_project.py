"""
Build the RainReady QGIS project from the files in this folder.

WHY THIS EXISTS. The AR1c plan asked for a saved `rainready.qgz`. QGIS is not installed on the machine that
produced these files, so the project could not be created or tested there. This script does it instead:
run it once on a machine that has QGIS and it produces the project the plan specified.

UNTESTED [verify] - it has never been run against a real QGIS install. If a layer path or symbol call fails,
the fix is almost certainly a one-line API change, not a problem with the data.

HOW TO RUN
  1. Open QGIS (3.28 or newer).
  2. Plugins > Python Console > Show Editor, open this file, press Run.
     Or from a terminal with QGIS's python:  python3 build_qgis_project.py
  3. It writes rainready.qgz next to this script and leaves the project open.

WHAT IT BUILDS
  CRS EPSG:32647 (WGS 84 / UTM 47N). Malaysia's national grid is EPSG:3375 (GDM2000 / Peninsular Malaysia RSO) -
  switch the CRS below if anything official has to line up.
  Layers, bottom to top: the two DEM-derived rasters, contours, then roads, buildings, drains, water,
  the main ditch, the council line, the two extent rectangles and the labelled key features.
"""

import os

from qgis.core import (QgsApplication, QgsProject, QgsVectorLayer, QgsRasterLayer,
                       QgsCoordinateReferenceSystem)

HERE = os.path.dirname(os.path.abspath(__file__))
CRS = "EPSG:32647"

VECTORS = [
    ("Key features", "key_features.geojson"),
    ("Extents", "extents.geojson"),
    ("Council line (Klang / Shah Alam, OSM)", "council_line.geojson"),
    ("Main ditch (OSM way 888406336)", "main_ditch.geojson"),
    ("Water bodies", "water.geojson"),
    ("Drains and ditches (65)", "drains.geojson"),
    ("Buildings (633 mapped - about 40-60% of what stands)", "buildings.geojson"),
    ("Roads (487)", "roads.geojson"),
    ("Contours 1 m (GLO-30, indicative)", "contours_1m.geojson"),
    ("Contours 0.5 m (GLO-30 - mostly noise)", "contours_0p5m.geojson"),
    ("Catchment to pour point (NOT FIT FOR USE - see AR1_site_model.md)", "catchment.geojson"),
    ("Synthetic streams, 18 ha threshold (NOT FIT FOR USE)", "streams_18ha.geojson"),
]

RASTERS = [
    ("Hillshade (GLO-30)", "hillshade.tif"),
    ("Slope %", "slope_pct.tif"),
    ("Flow accumulation (NOT FIT FOR USE)", "flow_accumulation.tif"),
    ("DEM - Copernicus GLO-30, 30 m (a surface model)", "dem_cop30_utm.tif"),
]


def build():
    project = QgsProject.instance()
    project.setCrs(QgsCoordinateReferenceSystem(CRS))

    added, missing = [], []
    for title, fname in RASTERS + VECTORS:          # rasters first so they sit underneath
        path = os.path.join(HERE, fname)
        if not os.path.exists(path):
            missing.append(fname)
            continue
        if fname.endswith(".tif"):
            layer = QgsRasterLayer(path, title)
        else:
            layer = QgsVectorLayer(path, title, "ogr")
        if not layer.isValid():
            missing.append(fname + " (loaded but invalid)")
            continue
        project.addMapLayer(layer)
        added.append(title)

    out = os.path.join(HERE, "rainready.qgz")
    project.write(out)
    print("added %d layers:" % len(added))
    for t in added:
        print("   " + t)
    if missing:
        print("missing or invalid: " + ", ".join(missing))
    print("written: " + out)
    print("\nCheck before trusting it: the model extent rectangle should measure 2.444 x 1.223 km "
          "and the hydrology extent 18.50 km2. If they do not, the CRS is wrong.")
    return out


if __name__ == "__main__":
    try:
        QgsProject.instance()
        build()
    except NameError:                                # running outside QGIS
        QgsApplication.setPrefixPath("/usr", True)
        app = QgsApplication([], False)
        app.initQgis()
        build()
        app.exitQgis()
