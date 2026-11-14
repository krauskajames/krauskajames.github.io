# Krauska GIS portfolio roadmap

Every portfolio idea for krauskagis.com in one place, ranked by how much it helps land a GIS job weighed against how hard it is to build.

Last updated: November 14, 2026 (added item 58: finish the Pollinator ArcGIS Online web map and add a click-to-load embed to the page; earlier, Nov 13: item 3 in progress: quotes from Jonathon Stippich and Ryan Wallin are live under their roles in Experience; added the PreGISP exam to Housekeeping; earlier, Nov 12: synced the live pages: Drone 3D Captures (item 11 done), the MKE Airport page with its new radar homepage card, and the AI Use Disclosure; item 1 done: the Winnebago ArcGIS Online dashboard is public and embedded on the page; added item 57: a practice ALTA-style survey drawing in Civil 3D, for the survey technician path; earlier, Nov 8: added items 47–56: three more county pipelines like Playbird Rd (road reconstruction, spring flood, shoreland permit), a land-protection pipeline, a printed trail map and brochure, an insurance hailstorm pipeline and four remote sensing pipelines; earlier, Nov 7: new umbrella item 46, "Playbird Rd: from farm field to neighborhood", with items 6, 12, 14, 19, 20, 37–45 as its chapters; item 37 rezoning now I-1 → PUD; earlier: one community per project; item 37 set in the Town of Sheboygan (Playbird Rd field), 200 ft; earlier: added items 37–45: nine everyday county land-records tasks, all Tier 1; earlier the same day: Parcel QA progress synced, and IAT Trail Designer, IAT Parcel Picker and Eddie's Parcel Picker added as items 34–36)

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
- **Data-flow diagrams (Nov 12).** Each project page gets a "Where the data came from" flowchart: sources, processing, outputs. They are written in Mermaid, kept as a `.mmd` file beside the project's scripts, rendered with mermaid-cli and placed on the page in the site's colours. Now on every project page except DuctBuilder (James, Nov 12): Winnebago, Parcel QA, MKE Airport, Pollinator, Field Season 2025, Drone 3D Captures and Starcast. Each page's intro and description are in projects/flows.json and projects/build_flow.py rebuilds them. Workflows run in ArcGIS Pro can use an exported ModelBuilder diagram instead.
- **One community per project.** Each project uses a different Wisconsin county or municipality, so the site shows range and every project page doubles as a reference for that place. Taken so far: Sheboygan County (4, 14), Winnebago County and Lake Winnebago (1, 9), Fond du Lac and Calumet counties (10), Monroe County (15), Milwaukee (23), Washington County/West Bend (30), Stevens Point (32), Town of Sheboygan (37). Repeats are OK when a place fits a project best (James, Nov 6); the list is for variety, not a hard rule. Check this list before picking a place for a new project, and prefer a new place when one fits as well.

---

## Already live

| Item | Status | Notes |
|---|---|---|
| Portfolio site with custom domain, About, Experience, Toolkit, Contact | ✅ | Phone, email, LinkedIn and GitHub in Contact |
| DuctBuilder card and case study | ✅ | Blender render on the card, demo video on hover; plan-in / model-out pair; results table ("one person now does the work of five") |
| Starcast card and case study | ✅ | Globe video at half speed. Starcast has its own feature log in the Starcast repo |
| Pollinator Habitat Explorer (MaxEnt revamp) | ✅ | Rerun with WISCLAND 2.0 land cover; interactive map and case study; button to the ArcGIS Online Instant App. Finishing that web map and a click-to-load embed is item 58 |
| The Wellness Spa in Experience and About | ✅ | Soft-skills story: listening to clients, Client Testimonial Award |
| Outside work section with Camino placeholder | ✅ | Finisterre photo; StoryMap still to build |
| Header stays above animated cards while scrolling | ✅ | |
| Winnebago County Community Profile page and prism-map card | ✅ | ArcGIS Online dashboard finished and embedded Nov 12 (item 1) |
| Parcel and NG911 QA toolkit page and scan-line card | ✅ | COGO drafting (five parcels) and the Lima toolbox run added Nov 6; PostGIS and Quarto parts still to do (item 4) |
| Field Season 2025 page (Restoring Lands) | ✅ | Map gallery, photo-point slider, fall photo map |
| Drone 3D Captures page (North Point Water Tower and other Milwaukee splats) | ✅ | Interactive Gaussian splat viewer and homepage card (item 11) |
| MKE Airport Asset Database page and radar card | ✅ | SQL Server spatial database, ArcGIS dashboard, Survey123 inspection loop and Power BI report. Homepage card added Nov 12: the airport's footprints on a radar scope, with a sweep turning about the control tower and the eight sample inspection points flashing red as it passes (built by projects/mke-airport/build_card.py) |
| Employer quotes in Experience (item 3) | 🔧 | PX Design and Restoring Lands live Nov 13; The Wellness Spa still to ask |
| AI Use Disclosure page | ✅ | Linked from the homepage and from each page's "Built with" line |

---

## Ranked roadmap

| Rank | Item | E | F | Score | Status |
|---|---|---|---|---|---|
| 46 | **Playbird Rd: from farm field to neighborhood** (umbrella for the parcel chapters) | 5 | 3 | 4.2 | 🔜 |
| 37 | Zoning hearing notice packet (Town of Sheboygan, 200 ft) (ch. 2 of 46) | 5 | 5 | 5.0 | 🔜 |
| 1 | County profile dashboard (Winnebago County) | 5 | 4 | 4.6 | ✅ |
| 2 | Field Season 2025 page (Restoring Lands, Donges Bay Gorge) | 5 | 4 | 4.6 | ✅ |
| 38 | Year-over-year parcel change report (ch. 6 of 46) | 5 | 4 | 4.6 | 💡 |
| 39 | Addressing a new subdivision (ch. 5 of 46) | 5 | 4 | 4.6 | 💡 |
| 40 | Wisconsin statewide parcel submission dry run (ch. 6 of 46) | 5 | 4 | 4.6 | 💡 |
| 41 | NENA NG911 schema migration (ch. 5 of 46) | 5 | 4 | 4.6 | 💡 |
| 42 | County supervisory district redistricting (ch. 7 of 46) | 5 | 4 | 4.6 | 💡 |
| 43 | Public parcel viewer (Experience Builder) (ch. 8 of 46) | 5 | 4 | 4.6 | 💡 |
| 44 | Field Maps asset inventory, collected yourself (ch. 8 of 46) | 5 | 4 | 4.6 | 💡 |
| 49 | Shoreland permit: application to inspection (pipeline) | 5 | 4 | 4.6 | 💡 |
| 3 | Employer quotes and references | 4 | 5 | 4.4 | 🔧 |
| 45 | PLSS section map book (Pro Map Series) (ch. 6 of 46) | 4 | 5 | 4.4 | 💡 |
| 58 | Pollinator: finish the ArcGIS Online web map and add a click-to-load embed | 4 | 5 | 4.4 | 🔧 |
| 4 | Parcel and NG911 data QA toolkit (with PostGIS) | 5 | 3 | 4.2 | 🔧 |
| 5 | ~~Geodatabase and SQL project~~ (merged into item 4) | | | | ➡️ |
| 6 | Utility mapping from as-built drawings (ch. 1 of 46) | 5 | 3 | 4.2 | 💡 |
| 47 | County road reconstruction: pavement rating to as-built (pipeline) | 5 | 3 | 4.2 | 💡 |
| 48 | Spring flood: forecast to buyout list (pipeline) | 5 | 3 | 4.2 | 💡 |
| 7 | Dark Skies of Wisconsin poster (WLIA map contest) | 4 | 4 | 4.0 | 💡 |
| 8 | Esri Academy advanced course project | 4 | 4 | 4.0 | 💡 |
| 9 | Lake Winnebago from space, 1999–2026 (Earth Engine) | 4 | 4 | 4.0 | 🔜 |
| 10 | 3D watershed analysis: the streams that feed Lake Winnebago at Pipe | 4 | 4 | 4.0 | 🔜 |
| 11 | Drone capture and Gaussian splats of buildings | 4 | 4 | 4.0 | ✅ |
| 12 | Site plans from drone surveys and county GIS (ch. 4 of 46) | 4 | 4 | 4.0 | 🔜 |
| 13 | Deep learning feature extraction (Image Analyst) | 4 | 4 | 4.0 | 💡 |
| 14 | Network Analyst project: fire and EMS coverage in Sheboygan County (ch. 7 of 46) | 4 | 4 | 4.0 | 💡 |
| 15 | Monroe County 1965 vs. 2010 swipe map | 3 | 5 | 3.8 | 🔜 |
| 16 | Ice Age Trail plants StoryMap | 3 | 5 | 3.8 | 🔜 |
| 17 | Headshot and "Outside work" polish | 3 | 5 | 3.8 | 🔜 |
| 18 | Earth Engine water-resources short course | 3 | 5 | 3.8 | 🔜 |
| 19 | LiDAR terrain and feature extraction (ch. 1 of 46) | 4 | 3 | 3.6 | 💡 |
| 20 | Solar suitability map (ch. 4 of 46) | 4 | 3 | 3.6 | 💡 |
| 21 | Mountain lion corridors, redone in Python | 4 | 3 | 3.6 | 💡 |
| 22 | Horicon Marsh open water since 1985 (Earth Engine, Random Forest) | 4 | 3 | 3.6 | 💡 |
| 23 | Milwaukee: a divided city, 1940–2020 (StoryMap) | 4 | 3 | 3.6 | 💡 |
| 34 | IAT Trail Designer: soil- and slope-aware trail routing | 4 | 3 | 3.6 | 💡 |
| 52 | Hailstorm: radar to claims (insurance pipeline) | 4 | 3 | 3.6 | 💡 |
| 53 | Lake Michigan bluff erosion: imagery to setbacks (pipeline) | 4 | 3 | 3.6 | 💡 |
| 55 | Urban tree canopy and heat (pipeline) | 4 | 3 | 3.6 | 💡 |
| 56 | Wetland and land cover update (pipeline) | 4 | 3 | 3.6 | 💡 |
| 50 | Land protection: candidate parcel to stewardship (pipeline over 34–35) | 4 | 3 | 3.6 | 💡 |
| 57 | Practice ALTA-style survey drawing in Civil 3D (Brookfield, survey technician path) | 4 | 3 | 3.6 | 🔜 |
| 24 | Camino Francés StoryMap | 3 | 4 | 3.4 | 🔧 |
| 25 | Still maps and posters gallery | 3 | 4 | 3.4 | 💡 |
| 51 | Printed trail map and tri-fold brochure | 3 | 4 | 3.4 | 💡 |
| 35 | IAT Parcel Picker: land-protection suitability and for-sale alerts | 4 | 2 | 3.2 | 💡 |
| 36 | Eddie's Parcel Picker: a new lot for a relocated house | 3 | 3 | 3.0 | 💡 |
| 54 | A growing season: planting to crop insurance (pipeline) | 3 | 3 | 3.0 | 💡 |
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
- **Status:** ✅ Done Nov 12, 2026. The page is live (winnebago.html) with the board memo and the prism-map homepage card. The ArcGIS Online dashboard is public (https://krauskagis.maps.arcgis.com/apps/dashboards/b6983a1a3d674ebe99a53a19f6ccdc63): four indicators, the municipality map and list, and population, location quotient, shift-share and commuting charts in the site's colours. It is embedded on the page and linked from the hero button.
- **Optional polish:** a legend on the commuting chart, a U.S.-average guide on the location quotient chart, smaller markers on the population chart, and a sources note.

### 2. Field Season 2025 page (Restoring Lands, Donges Bay Gorge) · E5 F4 · 4.6
- **What:** A page linked from the Restoring Lands entry: the Trimble selfie on the Lake Michigan beach, Field Maps invasive-species screenshots for six preserves, a Donges Bay Gorge section (trail, white pine over the lake, beach, the old stone bridge and pool house), and a map of where every field photo was taken.
- **Why:** The only hands-on field GIS job on the resume. Trimble experience is a minimum requirement for the Historical Society job.
- **Have:** 9 Field Maps screenshots (Pictures\OWLT INTERNSHIP), summer photos, fall internship report, the four Donges Bay photos.
- **Need:** Permission from Ryan Wallin to show the screenshots; original photos exported with location data; skip photos of the high school interns.
- **Status:** ✅ Live (field-season-2025.html, linked from the Restoring Lands entry). Permission received Oct 30, 2026 for photos and screenshots, not the feature layers. Built from the GEOG 480 report and the nine Field Maps screenshots: Trimble beach photo, points-vs-polygons rule, map gallery, 2020/2025 Spirit Lake photo-point slider, field finds.
- **Added Oct 30:** preserve names on every screenshot; a fall field days section (Donges Bay Gorge, Oct 22; Schoof's Preserve and the Zinn Preserve's Beck Lake, Oct 29) with 13 photos placed on a map from their GPS tags.
- **Added Oct 30 (later):** the photo map now covers the whole season, August 5 to November 4 (28 photos at 10 preserves), each with that day's task from the summer and fall internship logs; the fall switch to woody invasives and trail data; the "too many points" lesson from the log.
- **Added Nov 12:** a "Plants I identified" strip: eight plants James named from his own photos (scarlet pimpernel, cardinal flower, great willowherb, eastern prickly pear, rough blazing star, hedge bindweed, blue vervain, Ohio spiderwort), each tagged native or not native with its preserve (Mayhew, Kratzsch, Fellenz Woods).
- **Added Nov 14:** Ryan Wallin's approved quote as a pull quote at the end of "The job" (it is also under the Restoring Lands role in Experience). The held-back plant is confirmed as **sweet William** (not native, Fellenz Woods), not garden phlox.
- **Done Nov 14:** sweet William card added to the plant strip (nine plants). Item complete.

### 3. Employer quotes and references · E4 F5 · 4.4
- **What:** Two or three short quotes from people who worked with you, shown in About or Experience: The Wellness Spa owner or manager, Restoring Lands supervisor, and your boss at PX Design if he is comfortable being quoted without project details.
- **Why:** Every hiring manager in the r/gis threads said soft skills decide the final pick. Someone else saying it beats you saying it.
- **Need:** Ask for a LinkedIn recommendation or a two-sentence quote; get permission to use their name and title.
- **Status:** 🔧 Two of three live (Nov 13). Each quote sits under its role in Experience, styled as a pull quote with an olive rule:
  - Jonathon Stippich, CEO, PX Design (approved)
  - Ryan Wallin, Stewardship Director, Restoring Lands (approved Nov 13)
- **Next step:** Ask Ella Adams (The Wellness Spa manager) for a two-sentence quote, then add it under the Wellness Spa role.

### 4. Parcel and NG911 data QA toolkit, with a PostGIS database · E5 F3 · 4.2
- **What:** The parcel data pipeline, in five parts:
  1. **COGO drafting:** draft 3 to 5 parcels from recorded legal descriptions in ArcGIS Pro.
  2. **QA toolkit:** a Python/ArcPy script tool that checks a county's parcels, address points and road centerlines for gaps, overlaps, missing fields, NG911 addressing errors and address points off their road, with an error map.
  3. **PostGIS database (absorbed item 5):** load the Sheboygan parcels, address points and road centerlines into PostgreSQL/PostGIS with a designed schema (keys, constraints, lookup tables standing in for domains, spatial indexes). Rewrite the core checks as spatial SQL (`ST_Within`, `ST_Intersects`, `ST_DWithin`, self-joins for duplicates and overlaps) and save them as views, so the QA report is one query per check. Connect the database to ArcGIS Pro and QGIS. Publish the schema diagram and the SQL on the project page and GitHub, with a note that the same queries port to SQL Server spatial (`geometry`/`geography`).
  4. **Reproducible QA report (Quarto):** one `.qmd` file that connects to the PostGIS database (`geopandas.read_postgis`), runs the check views, and renders the report: counts per check with the Python and SQL results side by side, an interactive findings map (folium/leafmap), before/after examples, and a "how to rerun this" section. Code is folded by default. Rendered to HTML on the project page and to PDF for printing, so when the county updates its data, rerunning one file refreshes every number, table and map.
  5. **Legal description reader (stretch, added Nov 5):** a Python tool that takes a metes-and-bounds description pasted from a deed, CSM or the tax roll (`TAXDSCRP`), plus the commencement corner's coordinates from a tie sheet or the Control Corners layer, and writes an ArcMap-format traverse file that ArcGIS Pro's Traverse tool imports into the parcel fabric. Steps: clean OCR errors and degree/minute/second symbols, split into calls on "thence", parse quadrant bearings, distances and curves (radius, arc, chord, left/right), separate tie lines (POC → POB) from boundary courses, check closure in Python before import, and write a review table of each call's source text next to what was parsed, with uncertain calls flagged. Deterministic regex parsing so every call can be traced to its text; an AI fallback only for calls the regex misses, and only if closure confirms it. Test cases: the four hand-drafted Sheboygan parcels (answer key). Stretch on the stretch: run it over `TAXDSCRP` county-wide and report how many descriptions parse, how many close, and how far the drawn shape lands from the mapped parcel, as a new QA check ("description doesn't match mapped shape"); descriptions with no bearings (CSM lot or aliquot-part only) are skipped and counted. Standalone deed plotters exist; the angle here is writing straight into a Pro parcel fabric and checking the result against the county map. Esri said in 2023 it was researching deed-course import, so check Pro's Traverse docs before calling it new.
- **Why:** Parcels, legal descriptions, NG911 and scripting appear in four of the six postings analyzed. This closes the biggest gap. Winnebago asks for "knowledge of enterprise GIS database management systems" and R&M asks for SQL; doing the SQL on the same county data turns one project into a full data-management story (draft → check in Python → check in SQL). PostGIS is the spatial SQL most postings mean; SQL Server/SSMS experience goes on the resume alongside it, since many Wisconsin county enterprise geodatabases run on SQL Server.
- **Need:** ArcGIS Pro (Personal Use license), Esri Parcel Fabric labs (Splitting and Dividing Parcels), a PLSS primer, public parcel and address data for one county, PostgreSQL with PostGIS (free; installed with the Stack Builder on Windows). Quarto (free) with the Jupyter engine. SSMS is already installed for the SQL Server note.
- **Status:** ✔️ Core project done Nov 6. Live for Sheboygan County (parcel-qa.html): 19 checks in Python and PostGIS (SQL = Python on all 1,323 findings), a Pro script tool (Town of Lima layout on the page), five parcels drafted with COGO in Pro 3.7.3 (Parcel 4 misclosure write-up), the Quarto report (HTML + PDF), and a homepage card that drafts Parcel 3 (Village of Cascade) from its deed, lays the county parcel over it, then scans the village for findings. Splitting lab done Oct 26, dividing lab Oct 28. Setup on James's laptop: PostgreSQL 18.6, PostGIS 3.6.2, Quarto 1.11.9 (arcgispro-py3-qa via QUARTO_PYTHON).
- **Next step:** Only the stretch goal is left: the legal description reader (part 5). Housekeeping: the faster 12_address_checks.sql (schema-qualified, no SET search_path) was copied onto James's laptop on Nov 12 (ParcelQA\ParcelQA_postgis\postgis\sql, old copy kept as .bak); James reran the loader with --skip-load the same day: all 19 checks match between SQL and Python, 1,323 findings (address checks took 165 s). Housekeeping done.

### 5. Geodatabase and SQL project → merged into item 4
Folded into the Parcel and NG911 QA toolkit (Nov 2, 2026) so the SQL work runs on the same Sheboygan County data. Number kept so other item references stay the same.

### 6. Utility mapping from as-built drawings · E5 F3 · 4.2
- **Part of item 46, chapter 1.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
- **What:** Digitize a sample water or sewer system from as-built style drawings into a utility network (mains, valves, hydrants, manholes with attributes and connectivity), then run a trace: "which customers lose water if this valve closes?"
- **Why:** Ruekert & Mielke's GIS Technician posting is municipal utility mapping from as-builts, and reading engineering drawings is already your strength from DuctBuilder.
- **Need:** A sample as-built (public city plans, or a fictional one like the sample clinic); Esri's utility network training.
- **Next step:** Find one public set of utility as-builts or draw a fictional one.

### 46. Playbird Rd: from farm field to neighborhood · E5 F3 · 4.2
*Added Nov 7, 2026. One made-up development on one real parcel, followed through every county and town office a GIS tech supports. Each chapter is a finished piece on its own and goes live on one project page (playbird.html) as it is done, so the page is never half-built. The existing item numbers stay as the chapters so nothing else breaks.*
- **Site:** Town of Sheboygan, parcel 59024341550 (I-1, south side of Playbird Rd, east of N 40th St). Real parcels, roads, zoning and rules; made-up developer, petition, plat and buildings. Every chapter labels which is which.
- **Chapters:**
  0. **Why this site:** a developer's site screen of Town and nearby parcels (size, zoning, sewer and water, road access), using the Parcel Picker engine planned for items 35–36.
  1. **Site analysis:** soils, slope and LiDAR terrain (item 19), floodplain and wetland check, nearby sewer and water mains (item 6), the comprehensive plan's future land use map.
  2. **Rezoning, I-1 → PUD:** the zoning hearing notice packet and toolbox (item 37), plus the petition and a staff-report-style map.
  3. **Land division:** a preliminary plat (lots, new streets, outlots for the pond and trail) drafted with COGO and the parcel fabric (item 4's drafting methods and the Esri splitting/dividing labs), checked against Town and county land division rules.
  4. **Site plan and 3D:** site plan with setbacks, building massing and rooftop solar (items 12 and 20).
  5. **Addresses and roads:** new street names checked against the county list, address points by the grid rules, NG911 checks and the NENA schema (items 39, 4 and 41).
  6. **Into the county's books:** the new parcels in the fabric, a before/after change report (item 38), the statewide submission crosswalk for them (item 40) and the PLSS section map page (item 45).
  7. **Services:** fire/EMS drive times to the new streets (item 14) and the new residents added to the wards (item 42).
  8. **Public face:** the new lots in a public parcel viewer (item 43), and a Field Maps inventory of the new hydrants, signs and inlets (item 44, collected on similar real streets nearby).
- **Not included:** item 4 stays its own county-wide project (the story borrows its tools); the IAT projects (34, 35) stay separate.
- **Why:** shows how the pieces connect: planning, land records, addressing, 911 and the assessor all touch one development. Very few portfolios show the whole chain, and it gives one strong story for WLIA 2027.
- **Order:** chapter 2 first (item 37 is ready to start), then 3 and 5 (they reuse item 4), then 1, 6, 8, 4, 7, 0.
- **Next step:** item 37's hand run in Pro (200 ft selection on parcel 59024341550).

### 37–45. Everyday county land-records tasks (added Nov 6)
*Numbered 37–45 so the other items keep their numbers. All nine score Tier 1: each is a task a county land-records or planning office does every week, and each reuses tools already on hand (the item 4 QA scripts, the PostGIS database, ArcGIS Pro Advanced). Under the one-community-per-project rule, items 38–45 each still need their own county (they were first written for Sheboygan); the Wisconsin Statewide Parcel Map covers every county.*

### 37. Zoning hearing notice packet (Town of Sheboygan, 200 ft) · E5 F5 · 5.0
- **Part of item 46, chapter 2.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
- **Where:** Town of Sheboygan, Sheboygan County. Subject parcel: the farm field on the south side of Playbird Rd, east of N 40th St, between Larry's Distributing (industrial) on the west and the apartment buildings on the east, with the Wild Meadow Dr / Green Meadow Dr subdivision to the southeast and woods along the south edge. Parcel ID **59024341550**, zoned **I-1 Light Industrial** (Town of Sheboygan zoning layer, last updated 6/24/2025; no overlay district). Neighbors: I-1 to the north across Playbird Rd and to the west, B-2 (General Business) further west, R-4 apartments to the east, R-4 lots to the south past the woods, and R-1 homes to the southeast. The woods on the south edge are not wetland/shoreland zoned.
- **Scenario (updated Nov 7):** a made-up petition to rezone the parcel from I-1 Light Industrial to PUD (Planned Unit Development, § 335-49) for a mixed-use neighborhood: apartments and townhomes (extending the R-4 next door), a small commercial node on Playbird Rd, and a stormwater pond and trail along the wooded south edge. It is believable (R-4 already borders it on two sides) and has a real conflict: the I-1 businesses on Playbird Rd would be notified that housing is coming next to their truck traffic. The mailing list mixes industrial owners, apartment owners (absentee, with renters) and homeowners. Check § 335-49 for PUD steps (pre-application meeting, general development plan) before writing the petition. Use a made-up petitioner.
- **What:** Do what the Town's planner or GIS consultant does with the petition:
  1. Buffer the subject parcel by 200 ft and select every parcel that touches the buffer.
  2. Pull owner names and mailing addresses, then clean the list: one letter per owner (combine people and LLCs with several parcels), standardized addresses, absentee owners flagged (this is how the rental buildings show up).
  3. Optional courtesy step: "Occupant" letters for the apartment units (from address points), labeled as courtesy notices since the Town code does not require tenant notice as far as checked.
  4. Run the 1,000 ft check: list any municipality within 1,000 ft whose clerk must get notice at least 10 days before the hearing (the City of Sheboygan is the one to test).
  5. Export the packet: the 200 ft owner list in petition form, mailing labels (Avery 5160 PDF), the list as CSV, and a one-page notice map at 1 in = 100 ft (the scale the Town's petition plot plan calls for) showing the subject parcel, buffer, adjacent districts and existing uses.
  6. Package steps 1–5 as a Python toolbox (.pyt) with inputs for parcel ID(s), notice distance and output folder, so the next request takes 30 seconds. Distance is an input, not hard-coded (Town of Sheboygan 200 ft, Village of Belgium 250/300 ft, Janesville 400 ft, St. Croix County 300 ft).
- **Rules (Town of Sheboygan, Ch. 335 Art. XII, as found Nov 2026):** petitions filed with the Town Clerk include a 1 in = 100 ft plot plan with adjacent districts and existing uses within 200 ft, and owners' names and addresses within 200 ft; the Plan Commission holds the hearing after a Class 2 notice, then the Town Board decides; the clerk of any municipality within 1,000 ft gets written notice at least 10 days ahead. Re-check the current code and the Town's fee schedule before publishing.
- **Why:** The most common request a planning department sends its GIS tech. Hiring managers recognize it on sight, and it stays in the county James most wants to work in.
- **Have:** Sheboygan County parcels, address points and road centerlines (item 4); ArcGIS Pro Advanced; the item 4 Python patterns.
- **Need:** the Town of Sheboygan zoning layer (for the adjacent-districts part of the plot plan); municipal boundaries.
- **Portfolio page:** zoning-notice.html with the scenario, the raw vs. cleaned owner list, the notice map, a screenshot of the tool dialog, and a link to the code. Blur or replace owner names in screenshots.
- **Hand run (Nov 8, Pro 3.7.3):** 200 ft Select By Location caught **29 parcels**; Summary Statistics on OWNERNME1 gave **17 owner rows**. Findings that the toolbox must handle: (1) Playbird Rd is the Town of Sheboygan / Town of Mosel line, so Mosel parcels north of the road are in the buffer and the Town of Mosel clerk gets the 1,000 ft notice; (2) Concord 5 LLC owns 12 Stonefield Creek lots → one letter; (3) "PETERSON & SONS CO LLC" and "PETERSON & SONS COMPANY LLC" are the same owner spelled two ways → merge (15 letters if their mailing addresses match: 17 rows − 1 blank − 1 duplicate); (4) one parcel has a blank owner name (likely road or common area; check before mailing); (5) the Town of Sheboygan owns 2 parcels and is on its own list; (6) the "First Owner Name Alt" field has names in first-last order, better for labels than "LAST, FIRST".
- **Toolbox (Nov 8):** `projects/zoning-notice/ZoningNotice.pyt` + `notice_core.py` (tested), with steps in `YOUR_PART.md`. Field names confirmed: PARCELID, OWNERNME1/1ALT/2/2ALT, PSTLADDRESS, PSTLCITY, PSTLSTATE, PSTLZIP5, PSTLZIP4, SITEADDRESS, MUNI, isROW.
- **Tool run (Nov 13, Pro 3.7.3):** matches the hand run: 29 parcels, 17 owner rows, 1 excluded (blank owner), **15 letters** (Peterson spellings merged), 3 owners with several parcels, 7 absentee owners, 0 pairs to review, clerk notice to the Town of Mosel; labels and notice_map.pdf exported.
- **Page (Nov 13):** playbird.html is live with the chapter strip and chapter 2 (interactive notice-area map with letter numbers and zoning, the 29 → 15 funnel, tool steps, a five-place comparison of notice rules, made-up label sheet); homepage card added. Found: the field is inside the City of Sheboygan's ETJ (county ETJ layer), which matters for chapter 3.
- **Notice map (Nov 13):** the toolbox now builds the map and ANSI D layout itself (notice_layout.py, arcpy.mp); fifth run approved and added to playbird.html as an image and PDF.
- **Chapter 3 directions (Nov 13):** `projects/playbird/CH3_YOUR_PART.md` + `ch3_concept_sketch.png`: rules table (Town Ch. 337, County Ch. 71, City of Sheboygan ETJ, Wis. Stat. ch. 236), Section 4 T15N R23E with tie sheets 53054000 and 53044020, boundary → streets → lots in the fabric, QA, lot table, review routing table.
- **Next step:** James works through CH3_YOUR_PART.md.

### 38. Year-over-year parcel change report · E5 F4 · 4.6
- **Part of item 46, chapter 6.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
- **What:** Two years of the Wisconsin Statewide Parcel Map for Sheboygan County (e.g. V11 and V12), compared in PostGIS: new splits and combinations, owner changes, parcels whose geometry moved, with a change map.
- **Why:** Shows data maintenance thinking, not only one-off analysis. Reuses the PostGIS database from item 4.
- **Need:** The previous version of the statewide parcel layer for the county (SCO's parcel archive).
- **Next step:** Download the earlier version and load it next to the current one in `parcel_qa`.

### 39. Addressing a new subdivision · E5 F4 · 4.6
- **Part of item 46, chapter 5.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
- **What:** Take a recorded plat (or a fictional one), add the new road centerline, and assign addresses by the county's addressing grid rules: odd and even sides, spacing, a duplicate road name check. Then run the item 4 NG911 checks on the result.
- **Why:** Addressing appears in nearly every county posting, and the QA side is already built.
- **Need:** Sheboygan County's addressing ordinance (grid origin and spacing).
- **Next step:** Find the ordinance and pick a plat.

### 40. Wisconsin statewide parcel submission dry run · E5 F4 · 4.6
- **Part of item 46, chapter 6.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
- **What:** Every Wisconsin county sends its parcels to DOA and the State Cartographer's Office each year in a set schema. Crosswalk the Sheboygan data into that schema, run SCO's validation tool, and document what failed and how it was fixed.
- **Why:** A Wisconsin hiring manager sees right away that you know their yearly deadline. Could also become a chapter of item 4.
- **Need:** The current year's submission documentation and validation tool from SCO (check the version before starting).
- **Next step:** Read the submission documentation and list the required fields.

### 41. NENA NG911 schema migration · E5 F4 · 4.6
- **Part of item 46, chapter 5.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
- **What:** Convert the county's address points and road centerlines into the NENA NG9-1-1 GIS Data Model: field mapping, domain values and a validation report.
- **Why:** Schema migration is a classic technician task, and this builds on item 4 without repeating it.
- **Need:** The current NENA NG9-1-1 GIS Data Model standard and its template geodatabase; Wisconsin's NG911 GIS requirements.
- **Next step:** Get the NENA template and draft the field crosswalk table.

### 42. County supervisory district redistricting · E5 F4 · 4.6
- **Part of item 46, chapter 7.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
- **What:** Population-balanced county supervisory districts built from 2020 census blocks and wards for one county, with a deviation table and a public-facing map.
- **Why:** Wisconsin counties redraw supervisory districts from wards after every census; county clerks and GIS staff do it together. A distinctly Wisconsin skill and a good WLIA conversation starter.
- **Need:** 2020 census blocks with population (P.L. 94-171); the county's wards (LTSB) and current districts.
- **Next step:** Pick the county and download its wards and block populations.

### 43. Public parcel viewer (Experience Builder) · E5 F4 · 4.6
- **Part of item 46, chapter 8.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
- **What:** A county-style land-records web map: search by parcel number or address, an identify panel, a link to the tax bill, a print widget.
- **Why:** Most counties' public GIS work centers on this app, and it closes the web-app gap from the posting analysis.
- **Have:** Sheboygan parcels and address points; ArcGIS Online account.
- **Next step:** Publish the parcels as a hosted layer and start the Experience Builder app.

### 44. Field Maps asset inventory, collected yourself · E5 F4 · 4.6
- **Part of item 46, chapter 8.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
- **What:** A Field Maps form for something visible from the road in a nearby town (stop signs, culverts or hydrants), 50–100 points collected with a phone's GPS, attribute domains, QA checks and a small dashboard.
- **Why:** GPS field collection is an essential function in county postings (e.g. St. Croix County's GIS Technician). This is field work that is entirely your own, beyond the Restoring Lands internship.
- **Need:** A town and asset type; a public road route to walk or drive.
- **Next step:** Design the form (fields and domains) before going out.

### 45. PLSS section map book (Pro Map Series) · E4 F5 · 4.4
- **Part of item 46, chapter 6.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
- **What:** An index map and one page per section for one township, with parcels, parcel numbers and dimensions, made with ArcGIS Pro's Map Series.
- **Why:** Looks like a real county plat book, and Map Series is a skill hiring managers look for.
- **Have:** Sheboygan parcels; PLSS sections (Wisconsin PLSS layer).
- **Next step:** Pick the township (the Town of Lima, already used in item 4) and set up the index layer.

### 58. Pollinator: finish the ArcGIS Online web map and add a click-to-load embed · E4 F5 · 4.4
*Numbered 58 so the other items keep their numbers; it ranks with the other 4.4 items. Added Nov 14 at James's request.*
- **What:** Finish the Pollinator Habitat Explorer web map in ArcGIS Online, then show it on pollinator.html in its own section lower on the page ("Also built in ArcGIS Online"). The section shows a static screenshot with a "Load interactive map" button, and the Instant App loads in place only when someone clicks it. The existing "Explore the data in ArcGIS Online ↗" button under the main map stays.
- **Already done:** Hosted feature layers published from projects/pollinator/make_agol_layers.py (suitable habitat, overlap, records); web map and Sidebar Instant App public; layer list turned on; the page button links to the app.
- **Left to do in Map Viewer:**
  1. Finish the species split: three filtered copies of Suitable Habitat, each a single symbol (wild lupine #2d5638, swamp milkweed #5f8c4c, fringed loosestrife #9bb26a), no outline, about 30% transparency; lupine on by default.
  2. Swap the Light Gray Reference labels for Living Atlas "World Boundaries and Places" (darker text) and keep it in the Reference group.
  3. Short layer names: Wild lupine, Swamp milkweed, Fringed loosestrife (grouped as "Suitable habitat"), Habitat overlap, iNaturalist records.
  4. Save, and check that the map and layers are still shared with Everyone.
- **Then on the site:** take the screenshot from the published app, add the click-to-load section, and test it on a phone.
- **Why:** Most Wisconsin county and state GIS offices work in Esri. The custom Leaflet map shows open-source web mapping; this shows the same data handled in ArcGIS Online, on the page, without slowing it down for visitors who never click.
- **Why click-to-load:** A plain embed loads several megabytes of ArcGIS code for every visitor, competes with the main map and traps the mouse wheel when scrolling.
- **Next step:** James finishes steps 1–4 in Map Viewer; then Claude builds the embed section.

### 47–56. More pipelines like Playbird Rd, plus remote sensing (added Nov 8)
*Each pipeline follows one made-up event on real public data through several offices, and each chapter is a finished piece on its own, the same as item 46. Real data, made-up event, labeled which is which. Places are suggestions under the one-community rule; check the list before starting. The public parcel viewer asked about the same day is already item 43.*

### 49. Shoreland permit: application to inspection · E5 F4 · 4.6
- **What:** One made-up shoreland zoning permit (a house addition near a lake), handled the way a county zoning office does: find the ordinary high-water mark, check the 75 ft shoreland setback and the floodplain, calculate impervious surface on the lot, score mitigation points, draw the permit map, then a follow-up inspection form in Field Maps.
- **Where (suggested):** Green Lake County (Green Lake), a new place.
- **Why:** The most common permit a Wisconsin county zoning office reviews (NR 115 and the county shoreland ordinance). Small enough to finish quickly; a short second story beside item 46.
- **Need:** The county's shoreland ordinance and permit form; county parcels, LiDAR, FEMA flood zones, DNR hydrography.
- **Next step:** Read the county ordinance and list the measurements a permit needs.

### 47. County road reconstruction: pavement rating to as-built · E5 F3 · 4.2
- **What:** A county highway department's year for one road: pavement condition (PASER ratings) and the state's local-road database (WISLR), choosing which segment to rebuild, a culvert inventory in Field Maps, right-of-way parcels to acquire, detour routing, a public notice map, then updating road centerlines, addresses and NG911 after construction.
- **Where (suggested):** Manitowoc County, a new place.
- **Why:** Transportation work is rare in portfolios and counties hire for it. Reuses item 4's road checks, item 14's routing and item 44's Field Maps form.
- **Need:** WISLR data and PASER ratings for the county; county road centerlines and parcels; LiDAR for culverts.
- **Next step:** Get the county's WISLR and PASER data and pick the road.

### 48. Spring flood: forecast to buyout list · E5 F3 · 4.2
- **What:** One made-up flood on a real river: flood extent from LiDAR and FEMA flood maps, parcels, addresses and people affected, a damage-assessment form in Survey123, a situation dashboard for the emergency operations center, the FEMA damage summary, then ranking repeatedly flooded parcels for buyout.
- **Where (suggested):** Gays Mills and the Kickapoo River, Crawford County, a new place. The village moved part of its downtown out of the floodplain after the 2007–08 floods, so the buyout chapter has a real precedent.
- **Why:** Touches emergency management, zoning and the assessor; reuses the dashboard skills from item 1.
- **Need:** LiDAR DEM, FEMA flood zones and river gauge history; county parcels and address points; census blocks.
- **Next step:** Pull the river gauge record and pick the flood stage to model.

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
- **Status:** ✅ Live (north-point.html, "Drone 3D Captures"): an interactive Gaussian splat viewer with the North Point Water Tower and other Milwaukee captures, linked from a homepage card. Only non-client buildings go on the portfolio site.
- **Next step:** Add new captures as they are flown.

### 12. Site plans from drone surveys and county GIS · E4 F4 · 4.0
- **Part of item 46, chapter 4.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
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
- **Part of item 46, chapter 7.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
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
- **Part of item 46, chapter 1.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
- **What:** From Wisconsin county LiDAR: bare-earth DEM, hillshade, canopy height and extracted building footprints for one town, with an accuracy check against existing footprints.
- **Why:** LiDAR and feature extraction show up in surveying and engineering-firm postings. The same data feeds items 20 and 32.
- **Need:** County LiDAR point cloud (WisconsinView or the county); ArcGIS Pro 3D Analyst: Classify LAS Building, then LAS Building Multipatch for roof forms; Extract LAS for site clips.
- **Point cloud skills:** Classify the raw points before extracting anything: Classify LAS Ground and Classify LAS By Height in Pro (and optionally LAStools), with a quick check of the misclassified points. "Point cloud classification" is its own keyword in surveying and remote sensing postings.
- **Tip:** Build items 19 and 20 together on the same town to save time.

### 20. Solar suitability map · E4 F3 · 3.6
- **Part of item 46, chapter 4.** Built on the Playbird Rd site when it fits; the county-wide version stays a stretch goal.
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

### 52. Hailstorm: radar to claims (insurance pipeline) · E4 F3 · 3.6
- **What:** One real hailstorm followed through an insurer's catastrophe team: hail swath from NOAA's radar hail product (MRMS MESH), checked against Storm Prediction Center hail reports; a made-up book of policies on real building footprints and address points (no real customer data); policies under 1-inch-plus hail and an estimated loss for each; before/after imagery of a sample area with roof damage flagged (free imagery is coarse, so drone captures from item 11 can be the close-up); a claims-triage dashboard and adjuster routes (Network Analyst); renewal risk scores (distance to fire station and hydrant, flood zone, hail history).
- **Where (suggested):** the Sheboygan area (Acuity is headquartered there); a repeat of Sheboygan County is fine here.
- **Why:** Opens the insurance GIS job track. Wisconsin insurers include Acuity (Sheboygan), American Family (Madison), Sentry (Stevens Point), West Bend, Church Mutual and Secura.
- **Need:** MRMS MESH archive for the storm date; SPC storm reports; building footprints; before/after imagery.
- **Next step:** Find a recent hail day over eastern Wisconsin in the SPC reports.

### 53. Lake Michigan bluff erosion: imagery to setbacks · E4 F3 · 3.6
- **What:** Bluff-top lines traced from historic aerials and LiDAR, recession rates, parcels and homes at risk in 10, 25 and 50 years, setback recommendations for county zoning, and an insurance or buyout chapter.
- **Where (suggested):** Ozaukee County shoreline, tying to the Donges Bay Gorge field season (item 2).
- **Why:** Connects remote sensing, land records and zoning; a live issue for every Lake Michigan county.
- **Need:** Historic aerials (county or USDA), LiDAR from two or more years, county parcels.
- **Next step:** Find the oldest and newest LiDAR and aerials for the Ozaukee shoreline.

### 55. Urban tree canopy and heat · E4 F3 · 3.6
- **What:** Tree canopy mapped from NAIP imagery and LiDAR, land surface temperature from Landsat, the hottest blocks with the least shade, and a tree-planting priority map for a city forestry department.
- **Where (suggested):** Green Bay, a new place (or a chapter of item 23 in Milwaukee).
- **Why:** Image classification plus a clear public-service result; city forestry and sustainability offices use exactly this.
- **Need:** NAIP, LiDAR, Landsat summer scenes, city boundaries and blocks.
- **Next step:** Pick the city and pull one clear summer Landsat scene.

### 56. Wetland and land cover update · E4 F3 · 3.6
- **What:** Classify a county's land cover from imagery and LiDAR, check accuracy against field points collected in person, and flag where the state's wetland inventory looks out of date.
- **Where (suggested):** Waushara County, a new place.
- **Why:** DNR and county conservation work; a real accuracy assessment is what most student classifications skip.
- **Need:** NAIP or Sentinel-2, LiDAR, the Wisconsin Wetland Inventory, field points.
- **Next step:** Pick the study area and plan the field points.

### 50. Land protection: candidate parcel to stewardship · E4 F3 · 3.6
- **What:** Items 34–35 framed as one land-trust chain: Parcel Picker finds the candidates, a landowner outreach list, the easement boundary drafted, a baseline documentation report, and yearly monitoring visits in Field Maps.
- **Why:** Turns the IAT ideas into the full workflow a land trust runs, which also matches the Restoring Lands experience.
- **Next step:** Build item 35 first; the rest follows from its output.

### 57. Practice ALTA-style survey drawing in Civil 3D (Brookfield) · E4 F3 · 3.6
*Numbered 57 so the other items keep their numbers; it ranks with the other 3.6 items. Scored for the survey technician path (added Nov 12), where it matches postings such as Pinnacle Engineering Group's Survey Technician.*
- **What:** One real commercial lot near Brookfield, drawn from public records as a practice ALTA/NSPS-style sheet in the Autodesk Civil 3D free trial. Six steps, each matching a duty in survey technician postings:
  1. Pull a recorded certified survey map for the lot and read its legal description (read and interpret survey maps and plats).
  2. Enter the boundary in Civil 3D by bearings and distances, then check that it closes (survey calculations; Civil 3D).
  3. Import a file of simulated "field shots" with point codes, then draw the linework and a contour surface (downloading, organizing and reviewing field data; topographic surveys).
  4. Write a page of field notes with a sketch, and work a levelling loop by hand (field notes and sketches; benchmarks and control).
  5. Lay out the sheet against the 2026 ALTA/NSPS checklist: boundary, buildings, easements, title block (ALTA/NSPS surveys).
  6. Compute stakeout points for a building corner with offsets (construction staking).
- **Where:** Brookfield, Waukesha County, a new place.
- **Why:** Civil 3D is a preferred qualification in survey technician postings and is not yet on the resume. Steps 2, 4 and 6 are also the maths on the Certified Survey Technician Level I exam.
- **Label it:** Only a licensed surveyor can produce an ALTA/NSPS Land Title Survey. The title block says "practice exercise, not a survey", and the field shots are marked as simulated.
- **Need:** The Civil 3D trial (30 days from download, so start it with a free weekend ahead); a recorded certified survey map from the Waukesha County Register of Deeds; the 2026 ALTA/NSPS Minimum Standard Detail Requirements.
- **Prep kit (Nov 12):** projects/survey-practice has the record courses, a simulated 149-point field file, a levelling loop, a stakeout exercise, a checklist against the 2026 standards and an answer key. The lot is in New Berlin, next to Brookfield (S. Moorland Road at Interstate 43), from a draft certified survey map in a public plan-commission file; it was the nearest lot with a complete public description. James to confirm the lot or swap in a Brookfield one.
- **Next step:** Install the trial and report the exact version, so the walkthrough is written for it.

### 51. Printed trail map and tri-fold brochure · E3 F4 · 3.4
- **What:** A print-ready trail and park guide: a folded map with trails, distances, parking and features, plus a tri-fold brochure, laid out in ArcGIS Pro (and finished in a design program if needed), exported with bleeds for a print shop.
- **Where (suggested):** the Devil's Lake segment of the Ice Age Trail, Sauk County, a new place; can share data with the IAT items.
- **Why:** Proves print cartography (layout, type, folds, export) on a site that is mostly web maps; parks, tourism and economic development offices make these. The interactive, playful counterpart is item 32 (Fabled Atlas).
- **Next step:** Pick the segment and get the IAT trail and county park data.

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

### 54. A growing season: planting to crop insurance · E3 F3 · 3.0
- **What:** A Sentinel-2 vegetation index time series over one county's fields, crop types from USDA's Cropland Data Layer, flooded or drought-stressed fields spotted from space, prevented-planting and crop-loss checks like those federal crop insurance adjusters make, and nutrient runoff risk toward Lake Winnebago.
- **Where:** Calumet or Fond du Lac County fields draining to Lake Winnebago (shares data with items 9 and 10).
- **Why:** Agricultural remote sensing and a second insurance angle (crop insurance).
- **Next step:** Pull one season of Sentinel-2 and the CDL in Earth Engine.

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
| Hyperspectral imagery (NASA EMIT, spectral signatures) | Saved idea below; could fit items 9, 54 or 56 | 💡 |

**FAA Part 107.** Many drone and remote sensing postings require it, and right now the drone at PX Design is flown under the boss's license. Study with the FAA's free materials, take the knowledge test at an approved testing center (fee was about $175; check the current price), then add it to the resume and LinkedIn. It also lets James fly the site plan (item 12) and splat (item 11) captures himself.

**Saved for later (Nov 8): "285 colors the eye cannot see."** A chart James liked: NASA EMIT hyperspectral reflectance (381–2493 nm) over Paraná, Brazil, with one mean line and shaded spread per land use (native forest, planted forest, soybean, pasture, urban, water at Itaipu, sample counts in the legend), dark background, labeled features (chlorophyll absorption, red edge, leaf water, cellulose and clay), gaps where the atmosphere's water bands block the signal, and the line "Every land use has a signature." A Wisconsin version is possible (EMIT covers about 52° S to 52° N): sample fields, forest, marsh, town and Lake Winnebago, and use the chart in item 9, 54 or 56. A copy of the image is in Claude outputs\Inspiration.

**Saved for later (Nov 11): [Great Lakes Trolling](https://greatlakestrolling.com/).** A free, no-account map for Great Lakes trolling anglers: water temperature at any depth, thermocline depth, currents, waves, wind, upwelling and downwelling, and a 3D lakebed view, built on NOAA's Great Lakes forecast models (GLOFS), GFS, HRRR and NWS wave forecasts. Worth studying as a reference for the fish chapter of item 9 (Lake Winnebago is not covered by GLOFS, so a Winnebago version would need other data), for Starcast's layer and time-slider design, and for anything on Lake Michigan (items 53 and 55).

---

## Housekeeping

| Item | Status | Notes |
|---|---|---|
| Decide on repo privacy (GitHub Pro, or confirm a public repo is fine with your boss) | 💡 | The old video and earlier "PX Duct Designer" wording remain in the repo history |
| Keep the resume and Work Experience Repository in sync with the site | 🔧 | Wellness Spa and DuctBuilder updates done |
| Interview prep tracker (GIS_Candidate_Standout_Tracker.xlsx) | 🔧 | In Documents\Claude outputs |
| PreGISP exam (earns the GISP-E) | 💡 | Eligible as a Dec 2025 grad. Next exam April 19–26, 2027; register by April 5, 2027. The GISP-E cuts the full GISP experience requirement from 4 years to 3 (gisci.org/PreGISP) |
| Separate remote sensing version of the resume | 💡 | Pull from the Work Experience Repository's "remote sensing keywords" section; add skills from the table above as items finish |
