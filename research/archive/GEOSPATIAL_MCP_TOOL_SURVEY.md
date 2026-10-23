# RainReady: Geospatial MCP and Online Tool Survey

**Audience:** RainReady team  
**Date:** 11 October 2026  
**Research question:** Can Claude connect to a GIS or online mapping tool that locates, outlines and inspects the proposed Phase 1 study block, reducing manual map searching?

## Finding in one sentence

**QGIS MCP is the strongest current candidate** because it can let Claude work with actual QGIS layers, processing algorithms, styles and rendered maps; OpenStreetMap MCP is a useful but narrower search tool, while Copernicus Browser and QGIS basemap plugins remain necessary for imagery checks.

This is a research finding, not yet a team stack decision.

## Candidate comparison

| Candidate | What Claude could obtain or control | Fit for RainReady | Main limitation | Confidence |
|---|---|---|---|---|
| **QGIS MCP** | QGIS projects, vector/raster layers, features, processing tools, styles, layouts, rendered maps and exports | **Strongest overall** | Local installation; plugin/server versions must match; still needs authoritative input data | H |
| **QuickOSM in QGIS** | OSM roads, water bodies, buildings and administrative objects through Overpass | Strong companion to QGIS MCP | OSM is volunteer data and not cadastral truth | H |
| **QuickMapServices in QGIS** | Searchable OSM, imagery and other reference basemaps | Strong for visual context and pond checks | Service dates, licences and redistribution terms vary | H |
| **OpenStreetMap MCP** | Place search, reverse geocoding, OSM-object lookup, nearby and bounding-box queries | Useful conversational search | No satellite imagery; OSM results remain unverified; project has low adoption so far | M |
| **Copernicus Browser** | AOI upload, dated Sentinel imagery, visual comparison and image/GeoTIFF download | Strong independent imagery source | Sentinel resolution may not settle small urban pond edges | H |
| **Overpass Turbo** | Browser-based OSM queries and GeoJSON export | Good no-install fallback | Requires query-and-export workflow; same OSM limitations | H |
| **GeoMaster agent skill** | Detailed guidance for GIS, remote sensing, terrain and geospatial code | Potentially useful research knowledge | A skill is instructions, not a live GIS connection; broad dependency footprint | M |
| **Blender experimental MCP** | Natural-language access to Blender's Python API | Relevant later for the simulated scene | Not a source-verification tool; Blender warns that generated code runs without guards | H |

## What QGIS MCP appears able to do

The `nkarasiak/qgis-mcp` project is listed in the QGIS plugin repository. The listing describes more than 100 MCP tools for layers, feature editing, QGIS Processing, styling, layouts and rendering, with support for QGIS 3.28 and newer. Its documented clients include Claude Desktop and Claude Code.

For this study-area question, those capabilities should allow Claude to:

- create the proposed 3D and hydrology bounding polygons from exact coordinates;
- add the two pond points, Tasik Setia Alam and the council-line bracket points;
- load OSM, DEM and imagery-derived layers;
- compare which features intersect or fall outside the proposed model boundary;
- style sourced, assumed and unverified features differently;
- render a labelled review map; and
- export the reviewed geometry to GeoPackage, GeoJSON or KML.

What it cannot do by itself:

- turn an OSM boundary into an authoritative cadastral boundary;
- determine who owns or maintains a pond from imagery;
- verify an OSM pond tag without a separate image or source;
- make a coarse DEM accurate enough for flood-depth claims; or
- resolve whether a dataset's licence is compatible with the competition terms.

## OpenStreetMap options

### QuickOSM

QuickOSM is listed in the QGIS plugin repository and queries the Overpass API from within QGIS. It can bring the relevant OSM geometries into the same project as the DEM and imagery. Likely useful feature groups are roads, water bodies, waterways, buildings and administrative boundaries within the bounding box.

Its results should be stored with an OSM access date and labelled **unverified** until checked. The two cited retention ponds and the council boundary are particularly important examples.

### OpenStreetMap MCP

The `cyanheads/openstreetmap-mcp-server` exposes six read-only tools for Nominatim and Overpass: place search, reverse geocoding, OSM ID lookup, nearby search, bounding-box search and raw Overpass queries. It requires no API key and supports local or hosted MCP use.

It could answer questions such as:

- Which OSM water features are mapped inside the 3D box?
- Which named roads intersect the box?
- Which OSM administrative objects are near the bracket points?
- What OSM IDs and tags correspond to the two pond coordinates?

However, it does not replace QGIS for reviewing geometry and imagery together. Its GitHub repository showed six stars at the time of review, so it should be treated as a promising small project, not mature infrastructure.

No relevant GIS, QGIS, ArcGIS or Google Maps connector appeared in the available ChatGPT plugin search. This does not prove none exists outside that directory.

## Imagery and terrain tools

### Copernicus Browser

Copernicus Browser accepts uploaded KML, WKT or GeoJSON areas of interest in EPSG:4326. It offers dated Sentinel imagery and can download JPG, PNG, KMZ or GeoTIFF products. It is suitable for an independent, attributable imagery check, although small urban ponds may require higher-resolution reference imagery.

### QuickMapServices

QuickMapServices is listed in the QGIS plugin repository and provides access to a large catalogue of basemaps and geodata services. It is useful for comparing the OSM pond shapes with current-looking imagery. Each underlying service still needs its own date, attribution and usage-rights check before its image is placed in a deck or public prototype.

### FABDEM licence concern

The University of Bristol lists FABDEM V1-2 under **CC BY-NC-SA 4.0**. The competition briefing reportedly gives the organiser broad rights to modify and commercialise submissions. That creates a possible compatibility issue if FABDEM or a derived layer is redistributed in the submission. This is not a legal conclusion; it is an item to clarify before choosing the deliverable DEM.

## Coordinate audit

The proposed 3D extent is:

```text
South  3.0845
North  3.0955
West   101.4250
East   101.4470
```

Two edge conditions are visible from the supplied coordinates alone:

1. Jalan Makyong is stated to begin at `101.4239 E`, approximately **120 m west** of the proposed model boundary. Therefore the box does not contain the entire supplied Makyong range.
2. Tasik Setia Alam at `101.4467 E` is only approximately **33 m inside** the eastern edge. This gives very little context around the upstream lake.

A larger rectangle worth testing during map review is:

```text
South  3.0840
North  3.0960
West   101.4235
East   101.4480
```

This is **not a selected extent**. It is a candidate comparison box that includes the stated Makyong start and provides a small buffer around Tasik Setia Alam. The final crop should be chosen only after the real road and water geometries are visible.

The proposed hydrology extent remains internally consistent with its stated purpose:

```text
South  3.080
North  3.110
West   101.415
East   101.465
```

## Evidence layers that should remain separate

| Proposed evidence layer | Source status | Confidence |
|---|---|---|
| `aoi_3d_candidate` | Team-defined extent | H |
| `aoi_hydrology_candidate` | Team-defined extent | H |
| `documented_street_ranges` | Coordinates supplied by the team; reconcile with mapped roads | M |
| `ponds_osm_unverified` | OSM volunteer tags | L |
| `tasik_setia_alam_candidate` | Supplied point; verify name and outline | M |
| `council_boundary_osm_unverified` | OSM, not cadastral | L |
| `dem_90m_rough` | Coarse global DEM, rounded metres | L |
| `fabdem_screening` | Better-resolution screening candidate; licence unresolved | M |

Keeping these separate prevents a polished map from making all inputs look equally authoritative.

## Questions still open

- Does QGIS MCP behave reliably on the team's actual Windows/QGIS/Claude setup?
- Can Claude call QuickOSM Processing operations through the MCP, or will a person need to run the OSM query?
- Which imagery source is current and sufficiently detailed over the two pond locations?
- Is there an authoritative MBDK/MBSA boundary layer available publicly?
- Is the Wetland Townpark identifiable from an authoritative developer plan rather than inference from unnamed water bodies?
- Is FABDEM use or redistribution compatible with the hackathon's IP and commercialisation terms?
- Does the final 3D crop need the entire stated Makyong range or only the documented flood segment?

## Sources

- [QGIS MCP plugin listing](https://plugins.qgis.org/plugins/qgis_mcp_plugin/)
- [QGIS MCP repository](https://github.com/nkarasiak/qgis-mcp)
- [QuickOSM plugin](https://plugins.qgis.org/plugins/QuickOSM/)
- [QuickMapServices plugin](https://plugins.qgis.org/plugins/quick_map_services/)
- [OpenStreetMap MCP server](https://github.com/cyanheads/openstreetmap-mcp-server)
- [Overpass Turbo GeoJSON documentation](https://wiki.openstreetmap.org/wiki/Overpass_turbo/GeoJSON)
- [Copernicus Browser documentation](https://documentation.dataspace.copernicus.eu/Applications/Browser.html)
- [Blender experimental MCP server](https://www.blender.org/lab/mcp-server/)
- [FABDEM V1-2 dataset and licence](https://research-information.bris.ac.uk/en/datasets/fabdem-v1-2/)
- [GeoMaster skill](https://skills.sh/k-dense-ai/scientific-agent-skills/geomaster)

