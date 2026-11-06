# Krauska GIS portfolio roadmap

Every portfolio idea for krauskagis.com in one place, ranked by how much it helps land a GIS job weighed against how hard it is to build.

Last updated: November 6, 2026 (IAT Trail Designer expanded; IAT Parcel Picker and Eddie's Parcel Picker added as items 35 and 36)

**Status key:** ✅ Done · 🔧 In progress · 🔜 Next up · 💡 Planned for later

---

## How items are ranked

Each idea gets two scores from 1 to 5:

- **Employability (E):** how directly it matches what GIS job postings ask for and what hiring managers say they look for (county land records, data management, web apps, field work, scripting, communication).
- **Feasibility (F):** how quickly it can be built with the data, software and skills on hand. 5 = an afternoon; 1 = weeks of new learning or data that is hard to get.

**Score = 0.6 × E + 0.4 × F** (out of 5). Employability counts more because the site exists to get hired. Items are listed highest score first; ties go to the more employable item.

| Tier | Score | Meaning |
|---|---|---|
| Tier 1 | 4.2 and up | Do these first. Strong job match and realistic to finish soon. |
| Tier 2 | 3.4 to 4.1 | Good additions once Tier 1 is moving. |
| Tier 3 | below 3.4 | Showpieces and passion projects. Great for personality; build when time allows. |

---

## Decisions so far

- Site: krauskagis.com, a hand-built static site on GitHub Pages (repo krauskajames.github.io). Forest and olive greens, museum-style layout, topographic hero.
- Kept out of search engines (noindex tag and robots.txt); reachable by direct link only. The GitHub repo itself is public.
- Work done at PX Design appears under the name **DuctBuilder**, with fictional sample buildings only. No client drawings, and nothing about it posted on LinkedIn or other public places.
- Unfinished projects are labeled "Coming 2027" or "Coming soon" so the site never claims work that isn't done.
- Each project gets a card on the home page and, when finished, its own case study page (problem, what was built, result, tools).
- Restoring Lands screenshots and data go live only with the land trust's permission.

---

## Already live

| Item | Status | Notes |
|---|---|---|
| Portfolio site with custom domain, About, Experience, Toolkit, Contact | ✅ | Phone, email, LinkedIn and GitHub in Contact |
| DuctBuilder card and case study | ✅ | Blender render on the card, demo video on hover; plan-in / model-out pair; results table ("one person now does the work of five") |
| Starcast card and case study | ✅ | Globe video at half speed. Starcast has its own feature log in the Starcast repo |
| Pollinator Habitat Explorer (MaxEnt revamp) | ✅ | Rerun with WISCLAND 2.0 land cover; interactive map and case study |
| The Wellness Spa in Experience and About | ✅ | Soft-skills story: listening to clients, Client Testimonial Award |
| Outside work section with Camino placeholder | ✅ | Finisterre photo; StoryMap still to build |
| Header stays above animated cards while scrolling | ✅ | |
| Winnebago County Community Profile page and prism-map card | ✅ | ArcGIS Online dashboard still in progress (item 1) |
| Parcel and NG911 QA toolkit page and scan-line card | ✅ | COGO drafting still to do (item 4) |
| Field Season 2025 page (Restoring Lands) | ✅ | Map gallery, photo-point slider, fall photo map |

---

## Ranked roadmap

| Rank | Item | E | F | Score | Status |
|---|---|---|---|---|---|
| 1 | County profile dashboard (Winnebago County) | 5 | 4 | 4.6 | 🔧 |
| 2 | Field Season 2025 page (Restoring Lands, Donges Bay Gorge) | 5 | 4 | 4.6 | 🔧 |
| 3 | Employer quotes and references | 4 | 5 | 4.4 | 🔜 |
| 4 | Parcel and NG911 data QA toolkit (with PostGIS) | 5 | 3 | 4.2 | 🔧 |
| 5 | ~~Geodatabase and SQL project~~ (merged into item 4) | | | | ➡️ |
| 6 | Utility mapping from as-built drawings | 5 | 3 | 4.2 | 💡 |
| 7 | Dark Skies of Wisconsin poster (WLIA map contest) | 4 | 4 | 4.0 | 💡 |
| 8 | Esri Academy advanced course project | 4 | 4 | 4.0 | 💡 |
| 9 | Lake Winnebago from space, 1999–2026 (Earth Engine) | 4 | 4 | 4.0 | 🔜 |
| 10 | 3D watershed analysis: the streams that feed Lake Winnebago at Pipe | 4 | 4 | 4.0 | 🔜 |
| 11 | Drone capture and Gaussian splats of buildings | 4 | 4 | 4.0 | 🔧 |
| 12 | Site plans from drone surveys and county GIS | 4 | 4 | 4.0 | 🔜 |
| 13 | Deep learning feature extraction (Image Analyst) | 4 | 4 | 4.0 | 💡 |
| 14 | Network Analyst project: fire and EMS coverage in Sheboygan County | 4 | 4 | 4.0 | 💡 |
| 15 | Monroe County 1965 vs. 2010 swipe map | 3 | 5 | 3.8 | 🔜 |
| 16 | Ice Age Trail plants StoryMap | 3 | 5 | 3.8 | 🔜 |
| 17 | Headshot and "Outside work" polish | 3 | 5 | 3.8 | 🔜 |
| 18 | Earth Engine water-resources short course | 3 | 5 | 3.8 | 🔜 |
| 19 | LiDAR terrain and feature extraction | 4 | 3 | 3.6 | 💡 |
| 20 | Solar suitability map | 4 | 3 | 3.6 | 💡 |
| 21 | Mountain lion corridors, redone in Python | 4 | 3 | 3.6 | 💡 |
| 22 | Horicon Marsh open water since 1985 (Earth Engine, Random Forest) | 4 | 3 | 3.6 | 💡 |
| 23 | Milwaukee: a divided city, 1940–2020 (StoryMap) | 4 | 3 | 3.6 | 💡 |
| 34 | IAT Trail Designer: soil- and slope-aware trail routing | 4 | 3 | 3.6 | 💡 |
| 24 | Camino Francés StoryMap | 3 | 4 | 3.4 | 🔧 |
| 25 | Still maps and posters gallery | 3 | 4 | 3.4 | 💡 |
| 35 | IAT Parcel Picker: land-protection suitability and for-sale alerts | 4 | 2 | 3.2 | 💡 |
| 36 | Eddie's Parcel Picker: a new lot for a relocated house | 3 | 3 | 3.0 | 💡 |
| 26 | Fall color change from satellite imagery (ESA SNAP) | 3 | 3 | 3.0 | 💡 |
| 27 | Migratory bird movements map | 3 | 3 | 3.0 | 💡 |
| 28 | Atlas of the round worlds (Robinson maps of every planetary-mass body) | 3 | 3 | 3.0 | 💡 |
| 29 | Well-water nitrate surface (Geostatistical Analyst) | 3 | 3 | 3.0 | 💡 |
| 30 | Solar system to scale across Wisconsin and beyond | 2 | 4 | 2.8 | 💡 |
| 31 | Wall Tracer "try it" demo (the code console idea) | 3 | 2 | 2.6 | 💡 |
| 32 | Fabled Atlas: low-poly downtown Stevens Point | 3 | 2 | 2.6 | 💡 |
| 33 | Rapa Nui 3D map with tiny moai | 2 | 2 | 2.0 | 💡 |

---

## Tier 1: do these first

### 1. County profile dashboard (Winnebago County) · E5 F4 · 4.6
- **What:** Revamp the GEOG 330 Ozaukee County demographic and economic memos into an interactive county profile: population change, age and race, income and housing, location quotients and shift-share, refreshed with the latest Census and BEA data.
- **Why:** Winnebago County's GIS Specialist posting sits in Planning and Zoning. Showing up with a profile of their own county is the "I researched you" move hiring managers remember.
- **Have:** Spreadsheets, extrapolation models and both memos on the USB drive (Spring 2025 / GEOG 330).
- **Need:** Current ACS and BEA tables for Winnebago; dashboard (ArcGIS Dashboards or a hand-built page).
- **Status:** 🔧 The page is live (winnebago.html) with the board memo and the prism-map homepage card. The ArcGIS Online dashboard is half built; ArcGIS Online wasn't loading.
- **Next step:** Finish the dashboard (indicators, list, charts, selector targets), then send the link so it can go on the page.

### 2. Field Season 2025 page (Restoring Lands, Donges Bay Gorge) · E5 F4 · 4.6
- **What:** A page linked from the Restoring Lands entry: the Trimble selfie on the Lake Michigan beach, Field Maps invasive-species screenshots for six preserves, a Donges Bay Gorge section (trail, white pine over the lake, beach, the old stone bridge and pool house), and a map of where every field photo was taken.
- **Why:** The only hands-on field GIS job on the resume. Trimble experience is a minimum requirement for the Historical Society job.
- **Have:** 9 Field Maps screenshots (Pictures\OWLT INTERNSHIP), summer photos, fall internship report, the four Donges Bay photos.
- **Need:** Permission from Ryan Wallin to show the screenshots; original photos exported with location data; skip photos of the high school interns.
- **Status:** 🔧 Live (field-season-2025.html, linked from the Restoring Lands entry). Permission received Oct 30, 2026 for photos and screenshots, not the feature layers. Built from the GEOG 480 report and the nine Field Maps screenshots: Trimble beach photo, points-vs-polygons rule, map gallery, 2020/2025 Spirit Lake photo-point slider, field finds.
- **Added Oct 30:** preserve names on every screenshot; a fall field days section (Donges Bay Gorge, Oct 22; Schoof's Preserve and the Zinn Preserve's Beck Lake, Oct 29) with 13 photos placed on a map from their GPS tags.
- **Added Oct 30 (later):** the photo map now covers the whole season, August 5 to November 4 (28 photos at 10 preserves), each with that day's task from the summer and fall internship logs; the fall switch to woody invasives and trail data; the "too many points" lesson from the log.
- **Next step:** Optional "Plants I identified" strip from the close-ups, once James confirms the species.

### 3. Employer quotes and references · E4 F5 · 4.4
- **What:** Two or three short quotes from people who worked with you, shown in About or Experience: The Wellness Spa owner or manager, Restoring Lands supervisor, and your boss at PX Design if he is comfortable being quoted without project details.
- **Why:** Every hiring manager in the r/gis threads said soft skills decide the final pick. Someone else saying it beats you saying it.
- **Need:** Ask for a LinkedIn recommendation or a two-sentence quote; get permission to use their name and title.
- **Next step:** Message The Wellness Spa contact this week.

### 4. Parcel and NG911 data QA toolkit, with a PostGIS database · E5 F3 · 4.2
- **What:** The parcel data pipeline, in five parts:
  1. **COGO drafting:** draft 3 to 5 parcels from recorded legal descriptions in ArcGIS Pro.
  2. **QA toolkit:** a Python/ArcPy script tool that checks a county's parcels, address points and road centerlines for gaps, overlaps, missing fields, NG911 addressing errors and address points off their road, with an error map.
  3. **PostGIS database (absorbed item 5):** load the Sheboygan parcels, address points and road centerlines into PostgreSQL/PostGIS with a designed schema (keys, constraints, lookup tables standing in for domains, spatial indexes). Rewrite the core checks as spatial SQL (`ST_Within`, `ST_Intersects`, `ST_DWithin`, self-joins for duplicates and overlaps) and save them as views, so the QA report is one query per check. Connect the database to ArcGIS Pro and QGIS. Publish the schema diagram and the SQL on the project page and GitHub, with a note that the same queries port to SQL Server spatial (`geometry`/`geography`).
  4. **Reproducible QA report (Quarto):** one `.qmd` file that connects to the PostGIS database (`geopandas.read_postgis`), runs the check views, and renders the report: counts per check with the Python and SQL results side by side, an interactive findings map (folium/leafmap), before/after examples, and a "how to rerun this" section. Code is folded by default. Rendered to HTML on the project page and to PDF for printing, so when the county updates its data, rerunning one file refreshes every number, table and map.
  5. **Legal description reader (stretch, added Nov 5):** a Python tool that takes a metes-and-bounds description pasted from a deed, CSM or the tax roll (`TAXDSCRP`), plus the commencement corner's coordinates from a tie sheet or the Control Corners layer, and writes an ArcMap-format traverse file that ArcGIS Pro's Traverse tool imports into the parcel fabric. Steps: clean OCR errors and degree/minute/second symbols, split into calls on "thence", parse quadrant bearings, distances and curves (radius, arc, chord, left/right), separate tie lines (POC → POB) from boundary courses, check closure in Python before import, and write a review table of each call's source text next to what was parsed, with uncertain calls flagged. Deterministic regex parsing so every call can be traced to its text; an AI fallback only for calls the regex misses, and only if closure confirms it. Test cases: the four hand-drafted Sheboygan parcels (answer key). Stretch on the stretch: run it over `TAXDSCRP` county-wide and report how many descriptions parse, how many close, and how far the drawn shape lands from the mapped parcel, as a new QA check ("description doesn't match mapped shape"); descriptions with no bearings (CSM lot or aliquot-part only) are skipped and counted. Standalone deed plotters exist; the angle here is writing straight into a Pro parcel fabric and checking the result against the county map. Esri said in 2023 it was researching deed-course import, so check Pro's Traverse docs before calling it new.
- **Why:** Parcels, legal descriptions, NG911 and scripting appear in four of the six postings analyzed. This closes the biggest gap. Winnebago asks for "knowledge of enterprise GIS database management systems" and R&M asks for SQL; doing the SQL on the same county data turns one project into a full data-management story (draft → check in Python → check in SQL). PostGIS is the spatial SQL most postings mean; SQL Server/SSMS experience goes on the resume alongside it, since many Wisconsin county enterprise geodatabases run on SQL Server.
- **Need:** ArcGIS Pro (Personal Use license), Esri Parcel Fabric labs (Splitting and Dividing Parcels), a PLSS primer, public parcel and address data for one county, PostgreSQL with PostGIS (free; installed with the Stack Builder on Windows). Quarto (free) with the Jupyter engine. SSMS is already installed for the SQL Server note.
- **Status:** 🔧 Live for Sheboygan County (parcel-qa.html): 19 checks, 1,321 items to review, a scan-line homepage card, and a Pro script tool. The splitting lab is done (Oct 26); the dividing lab is done (Oct 28). PostGIS part started Nov 2: PostgreSQL 18 installed, PostGIS via Stack Builder. Quarto report not started.
- **Next step:** COGO drafting done Nov 6: five parcels drafted in Pro 3.7.3 and published on parcel-qa.html ("Five parcels, drawn from their deeds", plus the Parcel 4 misclosure write-up); the Pro toolbox ran on the Town of Lima (65 findings) and its layout is on the page. Remaining: PostGIS schema, loader and SQL views; then the Quarto report. Setup verified Nov 6: PostgreSQL 18.6 (service running), PostGIS 3.6.2 available, Quarto 1.11.9 using arcgispro-py3-qa (Python 3.13.13, Jupyter 5.8.1) via QUARTO_PYTHON, and sqlalchemy 2.0.43 + psycopg2-binary 2.9.13 + geoalchemy2 0.21.0 in that environment; the legal description reader stays a stretch goal. Optional: swap the homepage card's stand-in traverse for one of the drafted parcels.

### 5. Geodatabase and SQL project → merged into item 4
Folded into the Parcel and NG911 QA toolkit (Nov 2, 2026) so the SQL work runs on the same Sheboygan County data. Number kept so other item references stay the same.

### 6. Utility mapping from as-built drawings · E5 F3 · 4.2
- **What:** Digitize a sample water or sewer system from as-built style drawings into a utility network (mains, valves, hydrants, manholes with attributes and connectivity), then run a trace: "which customers lose water if this valve closes?"
- **Why:** Ruekert & Mielke's GIS Technician posting is municipal utility mapping from as-builts, and reading engineering drawings is already your strength from DuctBuilder.
- **Need:** A sample as-built (public city plans, or a fictional one like the sample clinic); Esri's utility network training.
- **Next step:** Find one public set of utility as-builts or draw a fictional one.

---

## Tier 2: good additions

### 7. Dark Skies of Wisconsin poster (WLIA map contest) · E4 F4 · 4.0
- **What:** Print light-pollution map of Wisconsin with dark-sky parks, designed in ArcGIS Pro and finished in Illustrator.
- **Why:** WLIA map contest visibility (there is a Best Student Map award), print cartography, Illustrator skill.
- **Need:** Contest rules and deadline; satellite night-lights data; Illustrator.

### 8. Esri Academy advanced course project · E4 F4 · 4.0
- **What:** Take one in-depth Esri course or MOOC and turn its final exercise into a portfolio piece with your own data. Good candidates (check the current catalog): the Cartography MOOC, Spatial Data Science, Imagery in Action, ArcGIS Experience Builder and Dashboards learning paths, Python for geoprocessing.
- **Why:** Adds a credential and a polished piece at the same time.
- **Next step:** Pick one course that feeds another item (for example Experience Builder for item 1, Python for item 4).

### 9. Lake Winnebago from space, 1999–2026 (Earth Engine) · E4 F4 · 4.0
- **What:** One page about Lake Winnebago through the seasons, opened by the family story: summers at Great Uncle Bob's cottage in Pipe and Uncle Tom's in Taycheedah (the page names Pipe only), and ice fishing with cousins. Built in chapters that each go live on their own:
  1. **Blooms:** Sentinel-2 chlorophyll-a (NDCI) on every clear summer day since 2017; east vs. west shore against the wind (does a west wind pile the scum on the cottages' side?); filmstrips; the clearest late-summer Landsat image of each year, 1999–2026; checked against the DNR's sampled chlorophyll.
  2. **Ice:** ice-on and ice-off dates every winter since 2000 from MODIS daily imagery; ice roads and shanty clusters from Sentinel-1 radar and Sentinel-2.
  3. **Trends:** summer surface temperature (Landsat thermal), clarity, bloom intensity and ice days, with Sen's slope and Mann-Kendall tests.
  4. **Fish:** a winter ice-fishing log (Survey123) of ice thickness, depth and catches; a seasonal habitat map built from it plus depth, reefs, temperature and ice, framed as a model, not "where the fish are"; checked against the DNR's fish survey and creel data where it's public. Boat and shanty counts were considered and dropped: they measure where people fish, not where fish are.
- **Why:** Earth Engine, remote sensing and field data collection are missing from the portfolio, and the DNR, county land and water departments and environmental consultants ask for them. It pairs with the Winnebago County profile, and the personal story makes it memorable.
- **Have:** The open-source Earth Engine scripts by Parisa Abbasalizadehrezaei (MIT); the Lake Winnebago script, settings, lab guide and ice-log form (XLSForm) in projects/lake-winnebago-blooms/.
- **Need:** An Earth Engine account (free, noncommercial); the DNR's chlorophyll samples (WBIC 131100); the story and any cottage photos; this winter's ice log.
- **Not doing:** analysis on Google Maps or Google Earth imagery (its terms don't allow extracting data from it). Browse it for ideas, then work from NAIP, Sentinel and Landsat.
- **Next step:** Chapter 1 (LAB_GUIDE.md) and publish the ice-log form before ice-up.

### 10. 3D watershed analysis: the streams that feed Lake Winnebago at Pipe · E4 F4 · 4.0
- **What:** Delineate the watershed of the creek that enters Lake Winnebago near Pipe (the cottage shore) from county LiDAR: fill sinks, flow direction, flow accumulation, snap a pour point at the creek mouth, then trace the watershed and its stream network. Show it in 3D: terrain with vertical exaggeration, the watershed boundary as a ridge line, streams thickening downhill, land cover draped on top (how much of what drains to the cottage shore is farm field), and an animation of "rain" flowing downhill to the lake. Check the boundary against the USGS Watershed Boundary Dataset (HUC-12).
- **Why:** Hydrology is a core skill for DNR, county land and water conservation, stormwater and engineering-firm jobs. It also gives the Lake Winnebago project (item 9) its cause: where the phosphorus behind the blooms comes from.
- **How:** in ArcGIS Pro, by hand (decided: Pro, not a Python script), so every step is James's own work to talk through in interviews. Spatial Analyst Hydrology toolset; 3D Analyst for the Local Scene and the video.
- **Have:** ArcGIS Pro Advanced with Spatial Analyst and 3D Analyst; WISCLAND 2.0 land cover from the pollinator project.
- **Need:** Fond du Lac and Calumet county LiDAR DEMs (WisconsinView or USGS 3DEP, 1 m); the creek and pour point picked on the map; an ArcGIS Pro Local Scene, exported as an animation for the site.
- **Next step:** Pick the creek: find which stream enters the lake nearest Pipe, then download its DEM tiles.

### 11. Drone capture and Gaussian splats of buildings · E4 F4 · 4.0
- **What:** Drone (DJI Air 2S, flown by the licensed boss) plus ground photos turned into Gaussian splats that visitors can orbit in the browser. First subject: the North Point Water Tower, Milwaukee (captured Oct 29, 2026: two orbits, overhead passes, 26 ground photos).
- **Why:** Reality capture is now part of the job at PX Design (splats of buildings for the business), and UAS/photogrammetry is marketable in GIS too.
- **Pipeline (proven Oct 28 on a test object):** ffmpeg frames → COLMAP poses → Brush training (RTX 2000 Ada, 8 GB) → SuperSplat cleanup → .sog for the web, .ply for SketchUp's Gaussian Splats extension and Blender (KIRI 3DGS Render).
- **Status:** 🔧 Water tower processing. Only non-client buildings go on the portfolio site.
- **Next step:** COLMAP with both cameras, train, clean, then a viewer page and an orbit-video homepage card.

### 12. Site plans from drone surveys and county GIS · E4 F4 · 4.0
- **What:** Site plans built in ArcGIS Pro: a drone orthomosaic and surface model made with Pro's ortho mapping (needs the Advanced license, which James has) from timed drone photos, contours, the county parcel lines, setbacks buffered from zoning, utilities and footprints; exported to CAD/SketchUp for the building model and renders.
- **Why:** James no longer does floor plans at PX Design; he and his boss want him to take over the site plans the business now outsources. Site planning, drone mapping and parcel/zoning work are also everyday GIS tasks for counties, cities and engineering firms.
- **Need:** A practice site that isn't a client's (for the portfolio); Esri's "Create drone imagery products with ortho mapping" tutorial; the drone flown in timed-photo mode (video frames carry no GPS tags, which ortho mapping needs).
- **Pro skills it builds:** ortho mapping (orthomosaic, DSM, DTM); contours, slope and cut/fill volumes (3D Analyst, Spatial Analyst); a sun-shadow study of a proposed building (Sun Shadow Volume); setback buffers from parcel lines; CAD/SketchUp export. Package the repeated steps as a ModelBuilder model or Python toolbox so each new site plan starts from one tool.
- **Stretch:** Process the same flight in WebODM (free, open-source) or a Metashape trial and compare the orthomosaics, so the resume can name more than one photogrammetry package.
- **Next step:** Do the ortho mapping tutorial, then a practice site plan of a public site.

### 13. Deep learning feature extraction (Image Analyst) · E4 F4 · 4.0
- **What:** Use Esri's pretrained deep learning models in Pro (Image Analyst) to detect building footprints and trees from NAIP aerials or a drone orthomosaic for one Wisconsin town, then measure accuracy against the county's footprints (precision, recall, F1).
- **Why:** "Used deep learning for feature extraction" stands out on GIS resumes, and the same skill speeds up site-plan context at PX Design.
- **Need:** ArcGIS Pro Advanced with Image Analyst (have); Esri's pretrained models from ArcGIS Living Atlas; NAIP for the town; a graphics card for inference (RTX 2000 Ada, 8 GB).
- **Next step:** Run the building footprint model on one NAIP tile and compare with the county footprints.

### 14. Network Analyst project: fire and EMS coverage in Sheboygan County · E4 F4 · 4.0
- **What:** Drive-time service areas (4, 8 and 12 minutes) from Sheboygan County's fire and EMS stations, the addresses outside each band, and where a new station would cover the most of them (location-allocation). Reuses the county's road centerlines and address points from the Parcel QA project.
- **Why:** Network Analyst backs 911, public safety, utility and transit jobs; James already holds the Esri routing and closest-facility certificates, and this turns them into a real project. It pairs with the NG911 side of item 4.
- **Need:** Network Analyst (have); a network dataset built from the county road centerlines (speed limits or road class for travel times); station locations.
- **Next step:** Build the network dataset from the county roads.

### 15. Monroe County 1965 vs. 2010 swipe map · E3 F5 · 3.8
- **What:** Drag-to-compare slider between the 1965 aerial photo and 2010 imagery from Remote Sensing 1, Lab 2, with your digitized land-cover change.
- **Why:** Quick, very visual, shows historical imagery and change detection.
- **Have:** BIB-3FF-248-1965.jpg, Monroe 2010 3FF-248.jpg and the finished map (USB, Fall 2024 / Remote Sensing 1).

### 16. Ice Age Trail plants StoryMap · E3 F5 · 3.8
- **What:** Link or rebuild your GEOG 343 StoryMap of edible and allergenic plants along the Ice Age Trail.
- **Why:** Proof of ArcGIS StoryMaps; fits under Outside work next to the Camino.
- **Have:** Photos and legends on the USB (Spring 2025 / GEOG 343 / Storymaps).
- **Next step:** Check whether it is still published on ArcGIS Online.

### 17. Headshot and "Outside work" polish · E3 F5 · 3.8
- **What:** Studio headshot in About (download the unwatermarked file from the photographer; crop above the shirt logo), one short "Outside work" line (stargazing, gluten-free baking, the Camino), optional dog-on-head photo for personality.
- **Why:** Makes the site feel like a person; hiring managers want to picture you as a coworker.

### 18. Earth Engine water-resources short course · E3 F5 · 3.8
- **What:** Six short, commented Earth Engine lessons (github.com/RisaRezaei/gee-water-resources-course): data import, water frequency, Landsat epochs, Random Forest soil-moisture downscaling, water-area time series, Sen's slope and Mann-Kendall trends.
- **Why:** The fastest way to learn Earth Engine before items 9 and 22. Lessons 1, 2 and 5 are the warm-up in the Lake Winnebago lab guide; lesson 3 sets up Horicon Marsh.
- **Next step:** Lessons 1, 2 and 5 (about 2 hours).

### 19. LiDAR terrain and feature extraction · E4 F3 · 3.6
- **What:** From Wisconsin county LiDAR: bare-earth DEM, hillshade, canopy height and extracted building footprints for one town, with an accuracy check against existing footprints.
- **Why:** LiDAR and feature extraction show up in surveying and engineering-firm postings. The same data feeds items 20 and 32.
- **Need:** County LiDAR point cloud (WisconsinView or the county); ArcGIS Pro 3D Analyst: Classify LAS Building, then LAS Building Multipatch for roof forms; Extract LAS for site clips.
- **Point cloud skills:** Classify the raw points before extracting anything: Classify LAS Ground and Classify LAS By Height in Pro (and optionally LAStools), with a quick check of the misclassified points. "Point cloud classification" is its own keyword in surveying and remote sensing postings.
- **Tip:** Build items 19 and 20 together on the same town to save time.

### 20. Solar suitability map · E4 F3 · 3.6
- **What:** Rooftop solar potential for a Wisconsin town from a LiDAR surface model: solar radiation, slope, aspect and shading, ranked by building.
- **Why:** A planning and sustainability analysis cities actually commission; shows raster analysis beyond defaults.
- **Need:** Item 19's surface model and footprints.

### 21. Mountain lion corridors, redone in Python · E4 F3 · 3.6
- **What:** Rebuild the GEOG 343 cartographic model (suitability surface, cost distance, least-cost corridors) as a documented Python notebook with a clean final map.
- **Why:** Spatial analysis plus scripting in one piece. Use rasterio, GDAL and geopandas (open-source) alongside ArcPy, so the notebook shows the Python geospatial libraries that postings name.
- **Have:** The full ArcGIS Pro project and rasters on the USB (Spring 2025 / GEOG 343 / Lab01 Cougars, 575 MB).

### 22. Horicon Marsh open water since 1985 (Earth Engine, Random Forest) · E4 F3 · 3.6
- **What:** Map open water in Horicon Marsh every five years from 1985 with a Random Forest on eight Landsat water indices (github.com/RisaRezaei/gee-wetland-water-rf), with hold-out accuracy and kappa, your own drawn water and land samples, and the area series set against the marsh's water-level history.
- **Why:** Wetland mapping, classification and accuracy assessment are core skills for DNR and conservation jobs, and it builds on the MaxEnt pollinator work. Horicon is the largest freshwater cattail marsh in the U.S. and an hour from Sheboygan.
- **Need:** Item 9 done first (same Earth Engine setup); drawn training samples, because the marsh's open water is shallow and full of vegetation.
- **Stretch (OBIA):** Classify one year a second way, object-based: segment the image (Segment Mean Shift in Pro, or SNIC in Earth Engine), classify the segments, and compare accuracy with the pixel-based Random Forest.
- **Next step:** Course lesson 3, then run the script on Horicon with the default JRC labels as a first look.

### 23. Milwaukee: a divided city, 1940–2020 (StoryMap) · E4 F3 · 3.6
- **What:** A StoryMap of how the Milwaukee metro grew and divided, decade by decade: race and Hispanic origin, country of birth and language, income and homeownership by census tract, 1940–2020, for the city and the four-county metro. Chapters on 1930s redlining (Mapping Inequality's HOLC maps), Bronzeville cleared for the freeways, the 1967–68 open-housing marches, deindustrialization and the city–suburb line today, then a methods chapter.
- **Groups through the city:** country of origin and mother tongue as a second thread (German and Polish neighborhoods, the Latino near South Side, Hmong and other later arrivals). Religion as a small aside: the census never asked it, so it comes from places of worship mapped by denomination (ethnic parishes, synagogues, temples) and the county-level U.S. Religion Census.
- **Analysis:** segregation measures computed by hand for every decade (dissimilarity, isolation and multigroup entropy indexes), with one consistent color ramp across all years so decades can be compared.
- **Why:** Census and ACS data, demographic analysis and spatial statistics are everyday work in planning departments; it's a Wisconsin story for WLIA; and normalizing tracts across 80 years of boundary changes is a strong problem-solving story.
- **Need:** NHGIS tract tables and boundaries (1940–2020); Longitudinal Tract Database or NHGIS crosswalks to put old tracts on 2020 boundaries; ACS 5-year for today; Mapping Inequality HOLC layers; IPUMS full-count records if going before 1940 (wards or enumeration districts instead of tracts).
- **Not including:** crime data.
- **Next step:** Pull NHGIS race and nativity tables for Milwaukee County, 1940 and 2020, and map both on one ramp to test the idea.

### 34. IAT Trail Designer: soil- and slope-aware trail routing · E4 F3 · 3.6
*Numbered 34 so the other items keep their numbers; it ranks with the other 3.6 items.*
- **What:** An ArcGIS Pro tool (the Ice Age Trail Alliance works in Pro) that proposes sustainable footpath routes through a parcel, built with Ella (IAT trail designer). The user marks the start, the end polygon and the points of interest the trail should reach; the tool routes between them segment by segment, offers two or three alternatives, and suggests trail structures along each. A second mode reroutes an existing trail: pick two points on the trail line (or box the eroded stretch), route a new segment between them, splice it in, and write it to a **proposed reroute** layer, not the official one (IATA's layout policy requires team sign-off).
- **How layout works today:** Ella goes to the site and walks it. The tool doesn't replace that walk; it gives her candidate corridors and control points before she goes, and a line to flag on her phone once she's there.
- **Design rules are settings, not code:** every threshold lives in a rule profile (a JSON or YAML file picked in the tool), so other trail groups can use it. A profile holds the half-rule ratio, the average and maximum grades for each soil class, tread width, allowed user types, structure triggers and their thresholds, cost weights and switchback limits. Profiles to ship: **Ice Age Trail** (from the NPS IAT handbook, 2021, checked with Ella), a generic hiking profile (USFS), a mountain bike profile (IMBA guidelines) and an accessible-trail profile (USFS accessibility guidelines). Users can copy and edit any profile.
- **The core idea (what's new):** direction-aware cost, not plain slope cost. Each step's running grade is checked against the sideslope it crosses (the half rule), and the maximum grade allowed in each cell comes from the soil (SSURGO erodibility K factor, drainage class, hydrologic group, hydric soils), so sandy glacial soils get a lower limit. Routes are scored for grade reversals and the average-grade guideline.
- **Switchbacks:** a plain least-cost path can't double back. The router tracks direction of travel (a graph whose nodes carry heading), so it can turn sharply only where the ground and the profile allow a switchback. Hardest part; prototype it first.
- **Scenic value (viewshed):** a scenic raster over the parcel. Observer points on a grid (every 20–30 m, eye height about 1.7 m) run against a LiDAR first-return surface, so trees block views the way they do in the field (Viewshed 2 in Pro, which can use the graphics card). Each cell's score weighs what can be seen: water, open ridges and glacial landforms, long distance views, varied land cover (WISCLAND 2.0), and penalties for roads, houses and industrial buildings. The raster does two jobs: it pulls the route toward scenic spots (an attraction term in the cost) and it colors the finished trail by how scenic each stretch is. Caveat: Wisconsin LiDAR is usually flown leaf-off, so a summer setting thickens the canopy from a canopy height model.
- **Glacial features as points of interest:** suggest eskers, kettles, moraines and drumlins from the Wisconsin Geological and Natural History Survey's glacial maps, plus top viewshed spots, as optional points of interest.
- **Areas to avoid:** wetlands (WI DNR Wetland Inventory), floodplains, 24K hydrography buffers, large trees from the LiDAR canopy height model, and user-drawn no-go polygons for restricted data (rare species, archaeological sites), which the tool never stores or publishes.
- **Structure suggestions (checkbox rules, thresholds set in the profile):** stream crossings → bridge or culvert; hydric or poorly drained soil → boardwalk, turnpike or puncheon; concentrated flow crossing the line (flow accumulation) → grade dip; over-grade sections → **gargoyles** (rock steps built from stone found on site) where the soil shows surface stones or shallow bedrock (SSURGO rock fragments, depth to bedrock) or LiDAR shows rough ground, otherwise built steps or a reroute; weak tread → gravel; benches and signs at viewpoints and junctions.
- **Outputs:** two or three alternatives (least construction, most scenic, shortest); an elevation profile per route with half-rule violations colored; a materials and labor estimate for the suggested structures; GPX and an ArcGIS Field Maps layer for flagging on site, with a short field form whose notes (actual soil, rock, obstacles) feed back into the next run.
- **Existing tools checked (Nov 6):** UNB TRAIL (least-cost path, ArcGIS 10-era, aimed at vehicles), USGS TRAILS (regional route connections, with sustainable routing and switchback hints), TopoTrail QGIS plugin (DEM suitability, no soils), and many slope-only least-cost-path student projects. None combine half-rule routing, soil-based grade limits, editable rule profiles, scenic viewsheds, structure prescriptions and reroutes of an existing line.
- **Why:** Raster and network analysis, Python (rasterio, GDAL, geopandas, a custom graph router), soils data, a Pro Python toolbox, and a real user with a real problem. It builds on the mountain lion corridor work (item 21) and is a strong WLIA 2027 talk or poster story.
- **Have:** ArcGIS Pro Advanced with Spatial Analyst and 3D Analyst; the cougar corridor least-cost model (item 21); Sheboygan County parcels (downloaded for item 4). The Ice Age Trail crosses Sheboygan County in the Northern Kettle Moraine, so it works as a first test area if Ella's parcel is elsewhere; the Wisconsin Statewide Parcel Map covers any other county.
- **Need:** One parcel Ella has already flagged (its line is the answer key); Wisconsin 1 m LiDAR (WisconsinView or USGS 3DEP) as both bare earth and first return; gSSURGO soils; WI DNR wetlands and 24K hydrography; WGNHS glacial maps; the IAT handbook's design specs; the IATA's trail layer (WI DNR open data); the Pro version Ella and the Alliance run. A friendly check-in with the Alliance's GIS coordinator before it's used on real projects.
- **Next step:** Get Ella's finished parcel; build a Python prototype of the half-rule router with heading-aware switchbacks and compare its route with her flagged line; then the rule profile format.

### 24. Camino Francés StoryMap · E3 F4 · 3.4
- **What:** Route, daily stages, photos and an elevation profile of the spring 2026 walk, built from the photos' GPS locations.
- **Status:** 🔧 Placeholder card is live. Photos organized and geotagged (258 in Claude outputs\Camino_Photos\Picks, with the route GeoJSON); the StoryMap layout doc has 8 chapters and 58 stops.
- **Next step:** Build it in ArcGIS StoryMaps on the personal student account (photos only for now; videos later), then send the link for the Camino card.

### 25. Still maps and posters gallery · E3 F4 · 3.4
- **What:** A gallery page of finished static maps: lab maps worth showing (Monroe County change map, Wisconsin cities population map), the Dark Skies poster, any WLIA contest entry.
- **Why:** Shows cartographic care at a glance.

---

## Tier 3: showpieces and passion projects

### 35. IAT Parcel Picker: land-protection suitability and for-sale alerts · E4 F2 · 3.2
*Numbered 35 so the other items keep their numbers; it ranks just below item 25.*
- **What:** A map and app for Ice Age Trail land protection. Step 1: a suitability surface for where the trail should go, along the planned corridor between existing segments, built from glacial landform value (WGNHS maps), the scenic viewshed raster from item 34, soils and slope, gap length to the nearest existing segment and existing public land. Step 2: score every parcel in the corridor for how much it adds (gap closed, landform and scenic value) and how purchasable it is (size, owner type, assessed value per acre, existing easements, how many owners a route would need). Step 3: watch for those parcels to be listed for sale and alert the Alliance.
- **Alerts (the hard part):** MLS data needs a broker feed, and scraping Zillow-style sites breaks their terms. Options to check: saved-search emails from land listing sites parsed into the app; county tax-delinquent and foreclosure lists; changes in the statewide parcel layer's owner field (a sale shows up after the fact); a partnership with a broker who can share an IDX feed. Pick the legal source first, then build the alert (a scheduled script, email or Teams message).
- **Why:** Multi-criteria suitability, parcel and land-records analysis, automation, and a direct match for land trust, DNR and county land-records jobs.
- **Shares:** the suitability, viewshed and parcel scoring engine with items 34 and 36.
- **Need:** The planned IAT corridor (the NPS/IATA corridor plan); Wisconsin Statewide Parcel Map; WGNHS glacial maps; an agreed listing source; a conversation with the Alliance about how they prioritize land today.
- **Next step:** Ask Ella how the Alliance picks parcels now and whether a corridor plan layer can be shared.

### 36. Eddie's Parcel Picker: a new lot for a relocated house · E3 F3 · 3.0
*Numbered 36 so the other items keep their numbers. A family project with a real deadline, so it may jump the queue.*
- **What:** The Parcel Picker engine pointed at one family's very specific list of needs: find lots where a house that is being physically moved can go. Multi-criteria scoring of parcels (size, zoning that allows a relocated house, soils and slope for a foundation and septic, flood zone, distance to the places that matter) plus a moving-route check: can the house actually get there? Network Analyst over the road network with the house's height, width and weight as limits (overhead lines, bridges and their weight limits, road width, sharp turns, tree canopy), giving the move distance and the trouble spots for the mover's permit. Listing alerts as in item 35.
- **Why:** Multi-criteria suitability and Network Analyst routing with real constraints (oversize-load routing is everyday DOT and utility work), on a problem with a real answer. It builds the Parcel Picker engine on a small scale before the bigger IAT version.
- **Privacy:** the repo and site are public, so no address, names or the family's criteria list go in them. The portfolio version uses a made-up house and town.
- **Need:** The family's list of needs written out; the house's dimensions and weight; the house mover's limits; parcels and zoning for the search area; road network with bridges (WisDOT) and overhead utility crossings where available.
- **Next step:** Write the needs list with the family, then turn each need into a map layer or a rule.

### 26. Fall color change from satellite imagery (ESA SNAP) · E3 F3 · 3.0
- **What:** Track Wisconsin's fall color from north to south with Sentinel-2 imagery processed in ESA SNAP (NDVI change between dates), as an animated map.
- **Why:** Shows non-Esri remote sensing software; very shareable. This covers both the SNAP and the changing-tree-color ideas.
- **Need:** SNAP (free), Sentinel-2 scenes from the Copernicus browser, a few cloud-free dates.

### 27. Migratory bird movements map · E3 F3 · 3.0
- **What:** Animated map of one species moving through Wisconsin by week, from eBird Status and Trends data. A natural tie-in: Forest Beach Migratory Preserve, which you mapped at Restoring Lands.
- **Why:** Conservation employers (WDNR, land trusts) and great visual appeal.
- **Need:** eBird data access request.

### 28. Atlas of the round worlds · E3 F3 · 3.0
- **What:** An interactive web map, and a print poster for the WLIA map contest, showing a Robinson-projection map of every large, round world with a solid surface, side by side at true relative size (with an equal-size toggle). Includes Mercury, Venus (Magellan radar), Earth, the Moon, Mars, Vesta, Ceres, the Galilean moons, Titan, Saturn's mid-sized moons (Mimas, Enceladus, Tethys, Dione, Rhea, Iapetus), the five big Uranian moons, Triton, Pluto and Charon. Areas no spacecraft imaged are left black: the northern halves of the Uranian moons and much of Triton (Voyager 2 saw only the sunlit south), and Pluto's and Charon's far sides at low resolution. Bodies never mapped (Eris, Haumea, Makemake, Gonggong, Quaoar, Sedna, Orcus) are black, at their known size and shape. Haumea is drawn as its stretched ellipsoid, with the reported dark red spot marked as tentative.
- **Why:** Map projections, reprojecting global rasters (GDAL), planetary coordinate systems and cartographic design in one striking poster. Also a candidate WLIA map contest entry.
- **Which bodies:** large enough to be round or nearly round. Vesta, Mimas and Iapetus are in, with a footnote that they aren't strictly in hydrostatic equilibrium. Small irregular bodies (Arrokoth, comet 67P/Churyumov-Gerasimenko, Phobos, Hyperion and the like) are out.
- **Interactive:** click a world for its size, gravity, discovery, the mission that mapped it and how much of it has been seen; toggle true relative size or equal size.
- **Need:** USGS Astrogeology and NASA PDS global mosaics (public domain); WLIA contest rules (size limits, number of entries allowed).
- **Next step:** List the bodies and find one global mosaic for each.

### 29. Well-water nitrate surface (Geostatistical Analyst) · E3 F3 · 3.0
- **What:** Interpolate private-well nitrate across a Wisconsin county with kriging in Geostatistical Analyst, with cross-validation error, and compare it with land cover (row crops) and soils.
- **Why:** Interpolation with honest error estimates is a classic GIS analyst skill (groundwater, soils, air quality), and Wisconsin well nitrate is a live public-health topic. UW-Stevens Point's Center for Watershed Science keeps the statewide well-water data.
- **Need:** Well test data (UWSP Wisconsin Well Water Quality Viewer or the DNR); Geostatistical Analyst (have).
- **Next step:** Check what well data can be downloaded for one county.

### 30. Solar system to scale across Wisconsin and beyond · E2 F4 · 2.8
- **What:** The astronomy presentation, rebuilt as an interactive map, plus a print poster for the WLIA map contest. The Sun is the water tower by UW-Milwaukee at Washington County in West Bend. Every planet, dwarf planet and Sedna sits at its real position on one chosen date, laid out by direction and distance from West Bend. Pluto is about orange-sized, at Wisconsin Dells. Zooming out goes from a map of Wisconsin to a 3D globe for Sedna's orbit, the Hills cloud, and the Oort cloud reaching about to the Moon.
- **Interactive:** toggle each body's orbit on and off (Sedna's would stretch to its far end, about 3,400 km out at this scale), pick the date, and click a body for its true size and distance next to the scaled ones.
- **Why:** Geodesic distances and bearings, coordinate transformations, ephemeris data and a scrollable story. A good conversation starter that ties to Starcast and the stargazing hobby.
- **Need:** The original presentation, for its scale and landmarks; positions for the date from JPL Horizons; a 3D globe library for the outer zoom levels.
- **Next step:** Find the presentation's scale and confirm the landmarks.

### 31. Wall Tracer "try it" demo · E3 F2 · 2.6
- **What:** Run the wall-detection tool in the browser on the sample clinic plan: the useful version of the code console idea.
- **Status:** Wall Tracer itself still needs work before it can be shown as working.

### 32. Fabled Atlas: low-poly downtown Stevens Point · E3 F2 · 2.6
- **What:** An interactive, cute low-poly tourist map of downtown Stevens Point from LiDAR, building footprints and business listings.
- **Why:** Shows 3D, LiDAR and footprint skills with a lot of personality; a first city for the Fabled Atlas idea.
- **Need:** Item 19's footprints and terrain; a 3D web library (three.js).
- **Inspiration:** isometric.nyc: 3D city geometry rendered straight-on (orthographic), restyled tile by tile with a fine-tuned AI image model, and shown in a deep-zoom viewer (OpenSeadragon). The same recipe could style a Wisconsin town from open LiDAR and building footprints.

### 33. Rapa Nui 3D map with tiny moai · E2 F2 · 2.0
- **What:** A pannable 3D Easter Island from your existing Rapa Nui DEM (QGIS and Blender project), with tiny moai models and extracted building footprints, styled like topographic map art.
- **Why:** Pure showpiece. Great conversation starter; least tied to job postings.
- **Have:** RapaNuiDEM folder with the QGIS project and Blender file (Downloads\QGIS Tutorials).

---

---

---

## Remote sensing skill gaps

Skills that remote sensing and imagery postings ask for but that aren't on the resume yet. Each one is tied to a roadmap item, so it can go on the resume honestly once that item is done.

| Skill | Covered by | Status |
|---|---|---|
| FAA Part 107 remote pilot certificate | New: earn it (see below) | 💡 |
| Google Earth Engine | Items 18, 9, 22 | 🔜 |
| Sentinel-2 imagery | Items 9, 26 | 🔜 |
| Spectral indices (NDVI, NDWI, NDCI) | Items 9 (NDCI), 22 (water indices), 26 (NDVI) | 🔜 |
| Machine-learning classification (Random Forest) | Items 18, 22 | 💡 |
| Deep learning image classification | Item 13 | 💡 |
| Object-based image analysis (OBIA) | Item 22 (stretch: segmentation comparison) | 💡 |
| SAR (radar) imagery | Item 9, chapter 2 (Sentinel-1 ice roads) | 💡 |
| ESA SNAP / non-Esri remote sensing software | Item 26 (ENVI only if a free license turns up) | 💡 |
| Drone photogrammetry software (Pro ortho mapping, WebODM or Metashape) | Items 11, 12 | 🔧 |
| Point cloud classification (ArcGIS LAS tools, LAStools) | Item 19 | 💡 |
| Python raster and vector libraries (rasterio, GDAL, geopandas) | Item 21; ArcPy in item 4 | 💡 |

**FAA Part 107.** Many drone and remote sensing postings require it, and right now the drone at PX Design is flown under the boss's license. Study with the FAA's free materials, take the knowledge test at an approved testing center (fee was about $175; check the current price), then add it to the resume and LinkedIn. It also lets James fly the site plan (item 12) and splat (item 11) captures himself.

---

## Housekeeping

| Item | Status | Notes |
|---|---|---|
| Decide on repo privacy (GitHub Pro, or confirm a public repo is fine with your boss) | 💡 | The old video and earlier "PX Duct Designer" wording remain in the repo history |
| Keep the resume and Work Experience Repository in sync with the site | 🔧 | Wellness Spa and DuctBuilder updates done |
| Interview prep tracker (GIS_Candidate_Standout_Tracker.xlsx) | 🔧 | In Documents\Claude outputs |
| Separate remote sensing version of the resume | 💡 | Pull from the Work Experience Repository's "remote sensing keywords" section; add skills from the table above as items finish |
