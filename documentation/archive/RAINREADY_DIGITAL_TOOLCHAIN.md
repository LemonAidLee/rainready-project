# RainReady: Digital Software and Tool Learning Plan

**Audience:** RainReady team  
**Phase:** Planning  
**Reference scope:** Bandar Bukit Raja screening-level prototype, public data only  
**Recommendation:** Learn a small shared stack. Do not attempt engineering-grade flood prediction.

## 1. Executive recommendation

RainReady can be delivered as a **static web dashboard** using prepared map layers and calculation tables. It does not require a mobile app, user accounts, a database, a paid cloud platform, an AI model, or a live sensor network.

### Minimum viable stack

| Job | Primary tool to learn | Main owner |
|---|---|---|
| Team files and tracker | Google Drive + Google Sheets | Whole team |
| Version control and code sharing | GitHub; GitHub Desktop if command-line Git is unfamiliar | EE-2, then whole team |
| Spatial data and catchment analysis | QGIS Processing tools | EE-1, Mechanical |
| Hydrology and pond calculations | Microsoft Excel or Google Sheets | Mechanical |
| 3D model and web export | Blender, exporting `.glb` | Architecture |
| Dashboard coding | VS Code + HTML/CSS/JavaScript; use Vite only if helpful | EE-2 |
| Interactive 2D map | MapLibre GL JS | EE-2 with EE-1 |
| 3D viewer | Three.js | EE-2 with Architecture |
| Charts | Chart.js | EE-2 |
| Resident survey | Google Forms linked to Google Sheets | EE-3 |
| Pitch deck | Microsoft PowerPoint or Canva; choose one | EE-3 + Architecture |
| Demo recording/editing | OBS Studio + CapCut, or another editor already known | EE-2 + EE-3 |
| Free prototype hosting | GitHub Pages | EE-2 |

This stack directly covers the tracker deliverables: GeoTIFF/GeoJSON layers, CSV hand-offs, GLB models, the four dashboard screens, survey analysis, the deck, and the five-minute video.

## 2. Tools by workstream

### A. Whole-team coordination and file control

| Tool or knowledge | Priority | Learn only this much | Why RainReady needs it |
|---|---|---|---|
| **Google Drive** | Essential | Shared folders, permissions, file naming, version history | Central location for research, layers, visuals and submission files |
| **Google Sheets** | Essential | Filters, dropdowns, formulas, charts, protected ranges | Team tracker, assumption ledger, survey results and simple calculations |
| **GitHub** | Essential | Repository, commit, pull, branch, pull request, issue, release | Code history, collaboration, prototype/code link and attribution |
| **GitHub Desktop** | Recommended for beginners | Clone, commit, pull, push, resolve simple conflicts | Easier Git workflow for non-programmers |
| **One communication channel** | Essential | Pinned decisions and short daily check-in | Use an existing WhatsApp, Discord, Teams or Telegram group; do not add a new platform unless needed |

**Team rule:** large raw terrain files and working Blender files belong in Drive, not ordinary Git history. Git should contain code, small processed data, documentation and final optimized web assets. If large assets must be versioned, learn Git LFS; otherwise avoid it during the short build.

### B. GIS, terrain and spatial data

| Tool or knowledge | Priority | Learn only this much | Output |
|---|---|---|---|
| **QGIS** | Essential | Coordinate reference systems, clipping, raster calculator, hillshade/contours, vector editing, styling and export | Study boundary, catchment, flow paths, risk bands and council boundaries |
| **QGIS Processing Toolbox** | Essential | Fill sinks/depressions, flow direction, flow accumulation, watershed/catchment extraction, raster-to-vector and zonal statistics | Repeatable DEM-to-catchment workflow |
| **GRASS or SAGA algorithms inside QGIS** | Learn as needed | Use one tested hydrology workflow; record algorithm and parameters | Catchment and channel layers without learning another full application |
| **GeoPackage** | Essential format | Store working vector layers in one file | Reliable internal GIS hand-off |
| **GeoTIFF** | Essential format | Preserve raster CRS, extent, resolution and NoData | Elevation and risk rasters |
| **GeoJSON** | Essential format | Export simplified web-ready WGS84 layers | Dashboard map layers |
| **CSV** | Essential format | UTF-8, stable column names, longitude/latitude where needed | Flood spots, pond data and responsibility records |
| **Google Earth Pro or browser satellite imagery** | Optional check | Visual comparison only, not measurement evidence | Sanity-check roads, ponds and visible land use |
| **GDAL command-line tools** | Optional | Reprojection, clipping and file conversion only | Helpful for repeatable batch processing; QGIS can do these jobs initially |
| **WhiteboxTools or Python `pysheds`** | Optional | Use only if QGIS hydrology tools fail or reproducibility demands scripting | Alternative catchment workflow |

QGIS’s official training material covers extracting channel networks and watersheds from a DEM. Keep the analysis screening-level: the project documents already note that DEM error is too large for claimed flood depths.

### C. Hydrology, pond what-if and validation

| Tool or knowledge | Priority | Learn only this much | Output |
|---|---|---|---|
| **Excel or Google Sheets** | Essential | Named inputs, units, formulas, scenario tables, charts and formula checks | Low/central/high storage requirement and pond-capacity gap |
| **MSMA 2 methods** | Essential knowledge, not software | Rational method/design inputs, runoff coefficients, time of concentration, storage assumptions | Defensible formula basis and citations |
| **JavaScript formula translation** | Essential hand-off | Match the spreadsheet calculation and test cases exactly | Pond sliders in the web dashboard |
| **Python + Jupyter Notebook** | Optional | Read CSV/raster summaries, sensitivity runs and plots | Use only if the Mechanical or GIS lead already knows Python |
| **HEC-HMS** | Stretch | One sub-catchment model, inputs/outputs and limitations | Optional supporting rainfall-runoff run; not required for the core prototype |
| **EPA SWMM** | Defer | Urban drainage network modelling | Public drain geometry and calibration data are missing, so learning it now adds little value |
| **HEC-RAS** | Defer | 1D/2D hydraulic modelling | Not justified without detailed terrain, channel/drain geometry and calibration data |

The core calculation should remain auditable in a spreadsheet. HEC-HMS is free and credible, but it should only be attempted after the map layers, storage table and dashboard work. Never tune a model merely to match the reported flood locations.

### D. Architecture and 3D modelling

| Tool or knowledge | Priority | Learn only this much | Output |
|---|---|---|---|
| **Blender** | Essential | Import terrain/geometry, organize collections, basic materials, pond variants, decimate meshes and export glTF binary | Base site, pond/wetland options and optimized `.glb` assets |
| **glTF/GLB workflow** | Essential | Scale, axes, materials, object naming, texture sizing and export checks | A model Three.js can load reliably |
| **SketchUp, Revit or Rhino** | Optional existing workflow | Model there only if already proficient; pass the final asset through Blender for web optimization | Avoid learning two new modelling packages |
| **Khronos glTF Validator / online glTF viewer** | Recommended | Validate each exported file and inspect errors | Prevent broken 3D assets during integration |

Use simple geometry and flat/PBR materials. The purpose is to communicate scenarios, not produce a photorealistic digital twin. Blender’s GLB export is appropriate because glTF is designed for efficient delivery to web and native viewers.

### E. Web dashboard and prototype

| Tool or knowledge | Priority | Learn only this much | Output |
|---|---|---|---|
| **VS Code** | Essential | Project navigation, terminal, formatter, search and browser debugging | Main coding environment |
| **HTML, CSS and JavaScript** | Essential | Components/sections, responsive layout, events, Fetch API and modules | Dashboard shell and interactions |
| **Vite** | Recommended, not mandatory | Local dev server and production build | Simple modern build workflow; skip if the existing buildless approach is faster |
| **MapLibre GL JS** | Essential | Add GeoJSON sources, style layers, popups, legend, toggles and bounds | Catchment, hotspot and responsibility map |
| **Three.js** | Essential for embedded 3D | Scene/camera/light, `GLTFLoader`, resize handling and disposal | GLB scenario viewer |
| **Chart.js** | Recommended | Line/bar charts, tooltips and responsive canvas | Sensitivity and storage-gap charts |
| **Fetch API and JSON** | Essential | Read local JSON/GeoJSON and call a permitted official endpoint | Static data and advisory screen |
| **Malaysia data.gov.my weather API** | Essential for a live advisory | Request the MET Malaysia warning endpoint, handle empty/error states, show issue/validity times | Official-warning advisory; label it “advisory, not a forecast” |
| **Chrome/Edge DevTools** | Essential | Console, network errors, responsive mode, performance and cache disabling | Integration testing |
| **GitHub Pages** | Essential | Deploy from the repository/Actions and verify the public URL | Free static demo hosting |
| **Postman or Bruno** | Optional | Inspect one API response | Browser or `curl` is enough for a single simple endpoint |

**Recommended architecture:** no backend and no database. Store prepared layers and records as static GeoJSON/JSON/CSV files. Fetch the official warning endpoint only if its terms and browser access are confirmed. If live access is unreliable, show a clearly dated saved example response and explain the production integration.

### F. Survey, evidence and source management

| Tool or knowledge | Priority | Learn only this much | Output |
|---|---|---|---|
| **Google Forms** | Essential | Bilingual sections, consent/privacy line, required fields, preview, sharing and closing responses | English/Bahasa Malaysia resident survey |
| **Google Sheets** | Essential | Clean categories, pivots, COUNTIF/COUNTIFS, charts and CSV export | Survey summary with sample limits stated |
| **Browser/PDF tools** | Essential | Search within PDF, capture source page/title/date and stable link | Evidence and licence ledger |
| **Zotero + browser connector** | Optional | Save webpages/PDFs and export citations | Useful if EE-3 already knows it; the existing sources sheet is sufficient otherwise |
| **OpenRefine** | Optional | Deduplicate and standardize messy survey/location fields | Unnecessary for a small clean survey |

Google Forms can link responses directly to Sheets, which avoids manual data entry. Do not collect names, phone numbers, precise home addresses or email addresses unless genuinely necessary and disclosed.

### G. Visual design, deck and five-minute video

| Tool or knowledge | Priority | Learn only this much | Output |
|---|---|---|---|
| **Figma** | Recommended for UI planning | Components, frames, colour styles and export | One shared dashboard mock-up/style sheet before coding |
| **PowerPoint or Canva** | Essential; choose one | Master/theme, alignment, charts, image compression and PDF export | Maximum 10-slide pitch deck plus appendix |
| **OBS Studio** | Recommended | Window/display capture, microphone, 1080p canvas and test recording | Stable dashboard screen recording |
| **CapCut or DaVinci Resolve** | Essential; choose what is already known | Trim, voice-over, captions, audio level and 1080p export | Final five-minute video |
| **Audacity** | Optional | Noise reduction and normalization | Only if voice audio needs repair |
| **Colour Contrast Checker** | Essential quick check | WCAG contrast and colour-blind-safe palette | Readable risk bands and responsibility colours |

Do not learn both Figma and Canva deeply. Figma is useful for the interface hand-off; PowerPoint/Canva is for the judged deck. Use the simplest editor the team can operate reliably.

### H. Optional bench sensor demonstration

Only proceed after all core deliverables work.

| Tool or knowledge | Priority | Use |
|---|---|---|
| **Arduino IDE or PlatformIO** | Optional | Program an ESP32/Arduino and read an ultrasonic water-level sensor |
| **Serial Plotter** | Optional | Demonstrate changing measured distance/level |
| **MQTT broker / ThingSpeak / Blynk** | Defer unless already known | Adds networking and account setup without proving the core planning claim |

The sensor must be labelled a bench demonstration, not a deployed or calibrated flood-monitoring system.

## 3. What each member should learn first

| Role | First learning block | Second learning block | Should not own now |
|---|---|---|---|
| **Architecture** | Blender terrain/site workflow | GLB optimization and validation | GIS hydrology or dashboard code |
| **Mechanical** | Spreadsheet hydrology model and units | QGIS review plus sensitivity analysis | HEC-RAS/SWMM unless core work is complete |
| **EE-1 Data/GIS** | QGIS CRS, raster and hydrology processing | Clean GeoJSON/GeoTIFF export and metadata | Dashboard styling |
| **EE-2 Dashboard** | Git/GitHub, HTML/CSS/JS and DevTools | MapLibre, Three.js, Chart.js and Pages deployment | Recalculating hydrology independently |
| **EE-3 Evidence & Pitch** | Google Forms/Sheets and source ledger | PowerPoint/Canva, narrative and video script | Coding a separate app |
| **Whole team** | Shared data contract and file naming | Signed-out link testing and one rehearsal workflow | Adding new platforms mid-project |

## 4. Shared technical conventions to agree before building

1. **Coordinate systems:** keep a suitable projected CRS for measurement/analysis in QGIS; export web GeoJSON in WGS84 longitude/latitude. Record both in the data contract.
2. **Units:** metres, square metres/hectares, cubic metres, seconds and millimetres per hour. Every calculation table must show units.
3. **Stable fields:** agree names such as `asset_id`, `asset_type`, `authority`, `confidence`, `source`, `scenario`, and `risk_band` before hand-offs.
4. **Confidence values:** use only `H`, `M`, `L` or `Unknown`, with a source for every non-unknown responsibility entry.
5. **Web asset limits:** simplify GeoJSON and GLB files; test on an ordinary laptop and phone connection.
6. **Source metadata:** save title, publisher, publication date, access date, URL, licence/terms and the claim supported.
7. **Advisory safety:** always show source, issue time, validity time and a link to the official warning. Never label RainReady output as an official forecast.
8. **Reproducibility:** save QGIS parameters, spreadsheet test cases and dashboard formula tests so one member can reproduce another member’s result.

## 5. Tools to avoid learning during the short proposal phase

- Native Android/iOS development, Flutter or React Native
- User login/authentication systems
- SQL/PostgreSQL/PostGIS or Firebase/Supabase, unless the scope later requires persistent multi-user editing
- Kubernetes, Docker and complex cloud infrastructure
- ArcGIS Pro licences when QGIS covers the proposed analysis
- Unity or Unreal Engine for the web demo
- HEC-RAS 2D, full SWMM modelling or a “digital twin” claim
- Machine learning for flood prediction
- A custom Telegram bot before the on-screen advisory is complete
- Real-time IoT dashboards before the core decision-support screens work

These tools are not inherently unsuitable; they are unnecessary for proving RainReady’s central value within the current data and time limits.

## 6. Suggested learning order

### First 48 hours

1. Whole team: Drive structure, tracker, GitHub repository and data contract.
2. EE-1 + Mechanical: one small QGIS DEM-to-catchment test and a reviewed outlet point.
3. Mechanical: spreadsheet with units and one low/central/high calculation test.
4. Architecture: one terrain/building sample exported from Blender as a small GLB.
5. EE-2: one page that loads a GeoJSON layer and the sample GLB.
6. EE-3: launch the bilingual Google Form and start the source/licence ledger.

### Go/no-go gate

Proceed only if QGIS can export a plausible catchment/risk layer, the dashboard can load it, the GLB displays, and the Mechanical spreadsheet produces checked test values. If any part fails, simplify the presentation rather than adding a second toolchain.

### After the core integration works

Add charts, the responsibility panel, official-warning advisory, polished scenario visuals, deployment and video. Only then consider HEC-HMS or a bench sensor.

## 7. Official references

- [QGIS hydrological analysis training](https://docs.qgis.org/3.44/en/docs/training_manual/processing/hydro.html)
- [MapLibre GL JS documentation](https://maplibre.org/maplibre-gl-js/docs/)
- [Three.js GLTFLoader documentation](https://threejs.org/docs/pages/GLTFLoader.html)
- [Blender glTF 2.0 documentation](https://docs.blender.org/manual/en/5.1/addons/import_export/scene_gltf2.html)
- [HEC-HMS official site](https://www.hec.usace.army.mil/software/hec-hms/)
- [Malaysia official Weather API](https://developer.data.gov.my/realtime-api/weather)
- [Google Forms response-to-Sheets help](https://support.google.com/docs/answer/2917686)
- [GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages)

