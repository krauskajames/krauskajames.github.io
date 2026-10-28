# Krauska GIS portfolio roadmap

Every portfolio idea for krauskagis.com in one place, ranked by how much it helps land a GIS job weighed against how hard it is to build.

Last updated: October 28, 2026

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

---

## Ranked roadmap

| Rank | Item | E | F | Score | Status |
|---|---|---|---|---|---|
| 1 | County profile dashboard (Winnebago County) | 5 | 4 | 4.6 | 🔧 |
| 2 | Field Season 2025 page (Restoring Lands, Donges Bay Gorge) | 5 | 4 | 4.6 | 🔜 |
| 3 | Employer quotes and references | 4 | 5 | 4.4 | 🔜 |
| 4 | Parcel and NG911 data QA toolkit | 5 | 3 | 4.2 | 🔧 |
| 5 | Geodatabase and SQL project | 5 | 3 | 4.2 | 💡 |
| 6 | Utility mapping from as-built drawings | 5 | 3 | 4.2 | 💡 |
| 7 | Dark Skies of Wisconsin poster (WLIA map contest) | 4 | 4 | 4.0 | 💡 |
| 8 | Esri Academy advanced course project | 4 | 4 | 4.0 | 💡 |
| 9 | Lake Winnebago from space, 1999–2026 (Earth Engine) | 4 | 4 | 4.0 | 🔜 |
| 10 | Monroe County 1965 vs. 2010 swipe map | 3 | 5 | 3.8 | 🔜 |
| 11 | Ice Age Trail plants StoryMap | 3 | 5 | 3.8 | 🔜 |
| 12 | Headshot and "Outside work" polish | 3 | 5 | 3.8 | 🔜 |
| 13 | Earth Engine water-resources short course | 3 | 5 | 3.8 | 🔜 |
| 14 | LiDAR terrain and feature extraction | 4 | 3 | 3.6 | 💡 |
| 15 | Solar suitability map | 4 | 3 | 3.6 | 💡 |
| 16 | Mountain lion corridors, redone in Python | 4 | 3 | 3.6 | 💡 |
| 17 | Horicon Marsh open water since 1985 (Earth Engine, Random Forest) | 4 | 3 | 3.6 | 💡 |
| 18 | Camino Francés StoryMap | 3 | 4 | 3.4 | 🔧 |
| 19 | Still maps and posters gallery | 3 | 4 | 3.4 | 💡 |
| 20 | Fall color change from satellite imagery (ESA SNAP) | 3 | 3 | 3.0 | 💡 |
| 21 | Migratory bird movements map | 3 | 3 | 3.0 | 💡 |
| 22 | Wall Tracer "try it" demo (the code console idea) | 3 | 2 | 2.6 | 💡 |
| 23 | Drone footage and Gaussian splatting | 3 | 2 | 2.6 | 💡 |
| 24 | Fabled Atlas: low-poly downtown Stevens Point | 3 | 2 | 2.6 | 💡 |
| 25 | ArchiCAD-style site plans and renders | 2 | 3 | 2.4 | 💡 |
| 26 | Rapa Nui 3D map with tiny moai | 2 | 2 | 2.0 | 💡 |
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
- **Next step:** Email Ryan; private draft of the page meanwhile.

### 3. Employer quotes and references · E4 F5 · 4.4
- **What:** Two or three short quotes from people who worked with you, shown in About or Experience: The Wellness Spa owner or manager, Restoring Lands supervisor, and your boss at PX Design if he is comfortable being quoted without project details.
- **Why:** Every hiring manager in the r/gis threads said soft skills decide the final pick. Someone else saying it beats you saying it.
- **Need:** Ask for a LinkedIn recommendation or a two-sentence quote; get permission to use their name and title.
- **Next step:** Message The Wellness Spa contact this week.

### 4. Parcel and NG911 data QA toolkit · E5 F3 · 4.2
- **What:** The parcel data pipeline: draft 3 to 5 parcels from recorded legal descriptions with COGO, then an ArcPy script tool that checks a county's parcels and address points for gaps, overlaps, missing fields and address points off their road centerline, with an error map.
- **Why:** Parcels, legal descriptions, NG911 and scripting appear in four of the six postings analyzed. This closes the biggest gap.
- **Need:** ArcGIS Pro (Personal Use license), Esri Parcel Fabric labs (Splitting and Dividing Parcels), a PLSS primer, public parcel and address data for one county.
- **Status:** 🔧 Live for Sheboygan County (parcel-qa.html): 19 checks, 1,321 items to review, a scan-line homepage card, and a Pro script tool. The splitting lab is done (Oct 26).
- **Next step:** COGO-draft four parcels and test the script tool, following YOUR_PART.md.

### 5. Geodatabase and SQL project · E5 F3 · 4.2
- **What:** Design a small enterprise-style geodatabase (domains, subtypes, relationships, versioning notes) and load it into PostGIS, then answer real questions with SQL: parcels within 500 feet of a road, address points with no parcel, duplicate records.
- **Why:** Winnebago asks for "knowledge of enterprise GIS database management systems"; R&M asks for SQL. Pairs naturally with item 4 (same county data).
- **Need:** PostgreSQL with PostGIS (free), or a file geodatabase plus SQLite/GeoPackage as a lighter start.
- **Next step:** Sketch the schema for the parcel and address data from item 4.

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
  4. **Fish and boats:** a winter ice-fishing log (Survey123) of ice thickness, depth and catches; a seasonal habitat map built from it plus depth, reefs, temperature and ice, framed as a model, not "where the fish are"; boats counted on summer NAIP aerial photos (public domain, about every two years), including around Abraham's Reef and Long Point.
- **Why:** Earth Engine, remote sensing and field data collection are missing from the portfolio, and the DNR, county land and water departments and environmental consultants ask for them. It pairs with the Winnebago County profile, and the personal story makes it memorable.
- **Have:** The open-source Earth Engine scripts by Parisa Abbasalizadehrezaei (MIT); the Lake Winnebago script, settings, lab guide and ice-log form (XLSForm) in projects/lake-winnebago-blooms/.
- **Need:** An Earth Engine account (free, noncommercial); the DNR's chlorophyll samples (WBIC 131100); the story and any cottage photos; this winter's ice log. Optional: Planet imagery (3 m daily) if a university affiliation is available.
- **Not doing:** analysis on Google Maps or Google Earth imagery (its terms don't allow extracting data from it). Browse it for ideas, then work from NAIP, Sentinel and Landsat.
- **Next step:** Chapter 1 (LAB_GUIDE.md) and publish the ice-log form before ice-up.

### 10. Monroe County 1965 vs. 2010 swipe map · E3 F5 · 3.8
- **What:** Drag-to-compare slider between the 1965 aerial photo and 2010 imagery from Remote Sensing 1, Lab 2, with your digitized land-cover change.
- **Why:** Quick, very visual, shows historical imagery and change detection.
- **Have:** BIB-3FF-248-1965.jpg, Monroe 2010 3FF-248.jpg and the finished map (USB, Fall 2024 / Remote Sensing 1).

### 11. Ice Age Trail plants StoryMap · E3 F5 · 3.8
- **What:** Link or rebuild your GEOG 343 StoryMap of edible and allergenic plants along the Ice Age Trail.
- **Why:** Proof of ArcGIS StoryMaps; fits under Outside work next to the Camino.
- **Have:** Photos and legends on the USB (Spring 2025 / GEOG 343 / Storymaps).
- **Next step:** Check whether it is still published on ArcGIS Online.

### 12. Headshot and "Outside work" polish · E3 F5 · 3.8
- **What:** Studio headshot in About (download the unwatermarked file from the photographer; crop above the shirt logo), one short "Outside work" line (stargazing, gluten-free baking, the Camino), optional dog-on-head photo for personality.
- **Why:** Makes the site feel like a person; hiring managers want to picture you as a coworker.

### 13. Earth Engine water-resources short course · E3 F5 · 3.8
- **What:** Six short, commented Earth Engine lessons (github.com/RisaRezaei/gee-water-resources-course): data import, water frequency, Landsat epochs, Random Forest soil-moisture downscaling, water-area time series, Sen's slope and Mann-Kendall trends.
- **Why:** The fastest way to learn Earth Engine before items 9 and 17. Lessons 1, 2 and 5 are the warm-up in the Lake Winnebago lab guide; lesson 3 sets up Horicon Marsh.
- **Next step:** Lessons 1, 2 and 5 (about 2 hours).

### 14. LiDAR terrain and feature extraction · E4 F3 · 3.6
- **What:** From Wisconsin county LiDAR: bare-earth DEM, hillshade, canopy height and extracted building footprints for one town, with an accuracy check against existing footprints.
- **Why:** LiDAR and feature extraction show up in surveying and engineering-firm postings. The same data feeds items 15 and 24.
- **Need:** County LiDAR point cloud (WisconsinView or the county); ArcGIS Pro or PDAL/Python.
- **Tip:** Build items 14 and 15 together on the same town to save time.

### 15. Solar suitability map · E4 F3 · 3.6
- **What:** Rooftop solar potential for a Wisconsin town from a LiDAR surface model: solar radiation, slope, aspect and shading, ranked by building.
- **Why:** A planning and sustainability analysis cities actually commission; shows raster analysis beyond defaults.
- **Need:** Item 14's surface model and footprints.

### 16. Mountain lion corridors, redone in Python · E4 F3 · 3.6
- **What:** Rebuild the GEOG 343 cartographic model (suitability surface, cost distance, least-cost corridors) as a documented Python notebook with a clean final map.
- **Why:** Spatial analysis plus scripting in one piece.
- **Have:** The full ArcGIS Pro project and rasters on the USB (Spring 2025 / GEOG 343 / Lab01 Cougars, 575 MB).

### 17. Horicon Marsh open water since 1985 (Earth Engine, Random Forest) · E4 F3 · 3.6
- **What:** Map open water in Horicon Marsh every five years from 1985 with a Random Forest on eight Landsat water indices (github.com/RisaRezaei/gee-wetland-water-rf), with hold-out accuracy and kappa, your own drawn water and land samples, and the area series set against the marsh's water-level history.
- **Why:** Wetland mapping, classification and accuracy assessment are core skills for DNR and conservation jobs, and it builds on the MaxEnt pollinator work. Horicon is the largest freshwater cattail marsh in the U.S. and an hour from Sheboygan.
- **Need:** Item 9 done first (same Earth Engine setup); drawn training samples, because the marsh's open water is shallow and full of vegetation.
- **Next step:** Course lesson 3, then run the script on Horicon with the default JRC labels as a first look.

### 18. Camino Francés StoryMap · E3 F4 · 3.4
- **What:** Route, daily stages, photos and an elevation profile of the spring 2026 walk, built from the photos' GPS locations.
- **Status:** 🔧 Placeholder card is live.
- **Need:** Original phone photos exported with location data.

### 19. Still maps and posters gallery · E3 F4 · 3.4
- **What:** A gallery page of finished static maps: lab maps worth showing (Monroe County change map, Wisconsin cities population map), the Dark Skies poster, any WLIA contest entry.
- **Why:** Shows cartographic care at a glance.

---

## Tier 3: showpieces and passion projects

### 20. Fall color change from satellite imagery (ESA SNAP) · E3 F3 · 3.0
- **What:** Track Wisconsin's fall color from north to south with Sentinel-2 imagery processed in ESA SNAP (vegetation index change between dates), as an animated map.
- **Why:** Shows non-Esri remote sensing software; very shareable. This covers both the SNAP and the changing-tree-color ideas.
- **Need:** SNAP (free), Sentinel-2 scenes from the Copernicus browser, a few cloud-free dates.

### 21. Migratory bird movements map · E3 F3 · 3.0
- **What:** Animated map of one species moving through Wisconsin by week, from eBird Status and Trends data. A natural tie-in: Forest Beach Migratory Preserve, which you mapped at Restoring Lands.
- **Why:** Conservation employers (WDNR, land trusts) and great visual appeal.
- **Need:** eBird data access request.

### 22. Wall Tracer "try it" demo · E3 F2 · 2.6
- **What:** Run the wall-detection tool in the browser on the sample clinic plan: the useful version of the code console idea.
- **Status:** Wall Tracer itself still needs work before it can be shown as working.

### 23. Drone footage and Gaussian splatting · E3 F2 · 2.6
- **What:** Turn drone footage of a building into a 3D Gaussian splat that visitors can orbit in the browser.
- **Why:** UAS and photogrammetry skills; very eye-catching.
- **Need:** Footage of a building that is not a client project, or your boss's written OK; a splatting tool and a web viewer.

### 24. Fabled Atlas: low-poly downtown Stevens Point · E3 F2 · 2.6
- **What:** An interactive, cute low-poly tourist map of downtown Stevens Point from LiDAR, building footprints and business listings.
- **Why:** Shows 3D, LiDAR and footprint skills with a lot of personality; a first city for the Fabled Atlas idea.
- **Need:** Item 14's footprints and terrain; a 3D web library (three.js).

### 25. ArchiCAD-style site plans and renders · E2 F3 · 2.4
- **What:** Architectural site plans and building renders like the ones PX Design currently outsources.
- **Why:** Bigger payoff at your current job than for GIS applications. Show only fictional or personal sites.

### 26. Rapa Nui 3D map with tiny moai · E2 F2 · 2.0
- **What:** A pannable 3D Easter Island from your existing Rapa Nui DEM (QGIS and Blender project), with tiny moai models and extracted building footprints, styled like topographic map art.
- **Why:** Pure showpiece. Great conversation starter; least tied to job postings.
- **Have:** RapaNuiDEM folder with the QGIS project and Blender file (Downloads\QGIS Tutorials).

---

## Housekeeping

| Item | Status | Notes |
|---|---|---|
| Decide on repo privacy (GitHub Pro, or confirm a public repo is fine with your boss) | 💡 | The old video and earlier "PX Duct Designer" wording remain in the repo history |
| Keep the resume and Work Experience Repository in sync with the site | 🔧 | Wellness Spa and DuctBuilder updates done |
| Interview prep tracker (GIS_Candidate_Standout_Tracker.xlsx) | 🔧 | In Documents\Claude outputs |
