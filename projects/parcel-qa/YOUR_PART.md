# Parcel & NG911 QA toolkit: your part

The QA checks, the Sheboygan data download and the web page are done. Your part is the hands-on ArcGIS Pro work that employers ask about: **drafting parcels from legal descriptions with COGO**, plus a test run of the Pro script tool.

**Total time:** about 6–10 hours, spread over a week or two.

| # | Task | Time | Done |
|---|---|---|---|
| 1 | Finish the Esri parcel fabric labs | 2–3 h | ☐ |
| 2 | Set up a Pro project with Sheboygan's data | 30 min | ☐ |
| 3 | Draft 4 parcels from their legal descriptions (COGO) | 2–4 h | ☐ |
| 4 | Test the ParcelQA script tool in Pro | 30–60 min | ☐ |
| 5 | Send me screenshots and numbers | 15 min | ☐ |

---

## 1. Esri parcel fabric labs

1. Finish **Splitting Parcels in a Parcel Fabric** (the lab you already have open).
2. Then do one Esri tutorial on **entering legal descriptions with the Traverse tool**. Search Esri Academy or learn.arcgis.com for "traverse" or "COGO parcel fabric".
3. Things to understand by the end, because interviewers ask about them:
   - What a **parcel fabric** is: parcels, lines and points stored together, so neighboring parcels share boundaries.
   - **Point of commencement (POC)** vs **point of beginning (POB)**.
   - **Quadrant bearings** (N 89°41'00" W) vs azimuths.
   - **Misclosure** and **precision ratio** (for example 1:10,000), and what "the traverse doesn't close" means.
   - What a **record** (the legal description) is vs **measured** values.

Your ArcGIS Pro Personal Use license includes the parcel fabric. If a lab asks for a sample dataset, download it from the lab page.

---

## 2. Set up the Pro project

1. Create a new project: **Map** template, named `SheboyganParcelQA`.
2. Set the map's coordinate system: **Map Properties → Coordinate Systems**, search "Sheboygan", and pick **NAD 1983 (HARN) WISCRS Sheboygan County (US Feet)**. This is the county's own system (WKID 103458), so distances you type come out in US survey feet, matching the legal descriptions.
3. Add the county's layers: **Add Data → Data From Path**, then paste each URL:

| Layer | URL |
|---|---|
| Tax parcels | `https://gis2.sheboygancounty.com/publicgis1/rest/services/LandInformation/TaxParcels/FeatureServer/0` |
| PLSS sections | `https://gis2.sheboygancounty.com/publicgis1/rest/services/LandInformation/SecTwnRange/FeatureServer/0` |
| PLSS control corners | `https://gis2.sheboygancounty.com/publicgis1/rest/services/LandInformation/ControlCorners/FeatureServer/0` |
| Road centerlines | `https://gis2.sheboygancounty.com/publicgis1/rest/services/Addressing/Roads/FeatureServer/0` |
| Address points | `https://gis2.sheboygancounty.com/publicgis1/rest/services/Addressing/AddressPoints/FeatureServer/0` |

4. **Create your own fabric to draft in.** Don't draft in the county's layer; you can't edit it, and your parcels should be separate so you can compare them.
   - Catalog: create a file geodatabase `MyCOGO.gdb`, then a feature dataset in it with the same WISCRS Sheboygan coordinate system.
   - Geoprocessing: **Create Parcel Fabric** in that feature dataset.
   - Geoprocessing: **Add Parcel Type**, named `Tax`.
   - If the fabric gives you trouble, a plain polygon feature class with COGO enabled works for practice too. Right-click the feature class → **Data Design → Fields** isn't needed; just use the Traverse tool on it.

---

## 3. Draft 4 parcels from their legal descriptions

The descriptions come from Sheboygan's tax roll (the `TAXDSCRP` field). They get harder as you go. For each parcel:

1. **Find it.** In the Tax parcels layer, use **Select By Attributes** with `PARCELID = '…'` and zoom to it. Keep it visible with a hollow outline so you can compare your drawing to the county's.
2. **Find the point of commencement.** Each description starts from a PLSS corner. Each parcel lists the nearest monumented corners and their **tie sheets**: the county surveyor's record for that monument, with its county coordinates (North/East, in US feet, the same system as your map), a sketch, and the ties a surveyor uses to find it in the field. Open the tie sheet, note the coordinates, and check that you're looking at the right corner on the map.
   - The tie sheet number is the county key: town code, section, then corner. From the two I read, `…0000` is the SE corner and `…2000` is the E¼ corner (for example 62140000 is the SE corner of Section 14 in Herman).
   - One monument serves several sections. The E¼ corner of Section 10 is the same point as the W¼ corner of Section 11, so its tie sheet may be titled for the neighboring section.
3. **Draft it in the fabric** by following the [Pro 3.7.3 walkthrough](#pro-373-walkthrough) below: create a record named after the parcel ID, enter the courses with the Traverse tool, then Build Active.
4. **Check the closure** at the bottom of the Traverse pane: misclosure distance, ratio and calculated area.
5. **Compare to my answer key** in the parcel's section. Your misclosure and area should match to within rounding.
6. **Compare with the county's polygon.** Is it in the same place? Same shape? If it's shifted, why: a different starting corner, or a recording error?
7. **Screenshot** your drawn parcel over the county's (hollow outline), with the Traverse pane's closure numbers visible.

### Pro 3.7.3 walkthrough

Written for **ArcGIS Pro 3.7.3** after drafting Parcel 1 on Nov 5, 2026. These are the steps that actually worked, including the snags.

**A. The fabric has to be in the map as a fabric**
- Add it by dragging **MyCOGO2.gdb → Parcels → ParcelFabric** (the blue fabric icon) from Catalog into the map. Adding its feature classes one by one doesn't count: Pro won't show the **Parcel Record Workflows** tab and **Create Record** stays grey.
- The fabric layer is a controller: its sublayers (Points, Connection Lines, the Tax group with Tax_Lines, Tax and Historic) can sit anywhere in the drawing order, with only Records nested under ParcelFabric. That's normal.

**B. Units, once per project:** Project → Options → Units. Distance: US Survey Feet. Direction: Quadrant Bearing, Degrees Minutes Seconds.

**C. Create the record:** Parcel Record Workflows → Records → **Create Record**, named after the parcel ID. It becomes the active record (the box at the top left of the map). Only make one per parcel; a second record with the same name causes trouble at the build step.

**D. Traverse:** Parcel Record Workflows → Tools → **Traverse**.
- **Layer:** the fabric's **Tax_Lines** (not the county layer).
- **Set Start**, then snap to the point of commencement (zoom in first).
- Type each direction, Tab, distance, Enter (for example `N89-41-00W`, `485.6`). Pro pre-fills the next row with the last direction; press **Esc** to clear that placeholder after the last course.
- There is **no Finish button** for a closed traverse in 3.7.3. Each course is written to Tax_Lines as you enter it, and the traverse ends when it closes onto the start point.
- Screenshot the closure numbers before clicking **New**, because New clears them. (Trace Lines brings them back by clicking the lines in order.)

**E. Build:** close the Traverse pane, then Parcel Record Workflows → Construct → **Build ▾ → Build Active**. It's one click; there's nothing to click on the map afterward.
- **Nothing happened?** Click **Show Only Active**. If your lines disappear, they aren't in the active record: select one line, then the **≡** next to the record box → **Activate Record Of Selected Feature**, and build again.
- **Confirm it built:** turn on **Points** (corner points appear) or open the **Tax** attribute table and look for the new polygon. The new outline sits exactly on the lines, so it's easy to miss.
- **Nothing built, but the lines are in the record?** The loop may not be closed. Click **Create Seeds**: a seed only appears inside a closed loop. No seed means a gap at a corner; snap the loose end onto the start point (Edit Vertices) or adjust the traverse, then build.
- **Fill in the parcel's attributes** in the Tax table: **Name** = the parcel ID, **Stated Area** = the tax roll acreage, **Stated Area Unit** = Acre. Calculated Area is filled in for you (square feet).
- **Area:** read **Shape_Area** in the **Tax** attribute table (square feet; divide by 43,560 for acres). The Records table's area is the record's extent, not the parcel's.

**F. Save** (Parcel Record Workflows → Save, far left).

### Parcel 1: Town of Herman, the warm-up (4 courses)

- **Parcel ID:** 59004034130 · T16N R22E Sec 14 · 1.60 acres on the tax roll
- **Description:** *PRT SE SE, SEC 14, COM AT NE COR, SD 1/4, TH N89 DEG 41'W 485.6', S8 DEG 40'W 113.4', S83 DEG 27'E 506.05' TO E LN OF SEC, TH N 167.25' TO BEG.*
- **Reading it:** start at the northeast corner of the SE¼ of the SE¼ ("SD 1/4" means "said quarter"). It's a sixteenth corner, usually not monumented. It sits on the east section line, 1,320 ft south of the East ¼ corner. The POC is also the POB, because the last course returns "to beginning".
- **Courses:** N 89°41'00" W 485.60 · S 8°40'00" W 113.40 · S 83°27'00" E 506.05 · N 0°00'00" E 167.25
- **Nearest tie sheets:** [62140000](https://gis2.sheboygancounty.com/Tiesheets/62140000.pdf) is the **SE corner of Sec 14** (N 212,155.595, E 190,451.843). [62142000](https://gis2.sheboygancounty.com/Tiesheets/62142000.pdf) should be the E¼ corner, and your POC sits on the east line about halfway between those two. [62140020](https://gis2.sheboygancounty.com/Tiesheets/62140020.pdf) is also nearby.
- **How to place the POC:** for practice, snap to the county parcel's northeast corner. To do it properly, traverse north from the SE corner along the section line about 1,320 ft, or split the line between the SE and E¼ corners in half (that's how sixteenth corners are set).
- **Answer key:** misclosure **0.12 ft** (about 1:10,300), area **1.59 ac** (tax roll 1.60).
- **Your result (Nov 5, 2026, Pro 3.7.3):** ✅ misclosure **S32°44'33"W, 0.12 ft**, ratio **1:10,346**, calculated area **69,281.6 sq ft (1.59 ac)**. Matches the key. Built into the fabric (Tax polygon 69,281.3 sq ft) on Nov 5. **County map vs. the drafted parcel** (Measure tool, corner to corner): NE (the POC) ≈ 0 ft · SE 0.25 ft · NW 0.73 ft · SW 3.64 ft. The offset grows with distance from the starting corner, and the county's south line is slightly rotated against the recorded S83°27'E bearing.

### Parcel 2: Town of Lima, courses along a road centerline (5 courses)

- **Parcel ID:** 59008093220 · T14N R22E Sec 9 · 3.66 acres
- **Description:** *A-13670 - PRT SE NE & NE SE, SEC 9, COM AT SW COR SE NE, TH N0 DEG 44'42"W 363', E 468.62', S25 DEG 42'W 292.45' ALG CENLN HUMPHREY RD & CTH N, S47 DEG 04'W 457.45' ALG CENLN, TH N0 DEG 34'54"W 212.15' TO BEG.*
- **Reading it:** two courses run along the road centerline, so the parcel goes to the middle of the road. That's common in rural Wisconsin, and the public has an easement over the road half. "A-13670" is the county's survey or document number.
- **Courses:** N 0°44'42" W 363.00 · N 90°00'00" E 468.62 · S 25°42'00" W 292.45 · S 47°04'00" W 457.45 · N 0°34'54" W 212.15
- **Nearest tie sheets:** [42092000](https://gis2.sheboygancounty.com/Tiesheets/42092000.pdf), [42092020](https://gis2.sheboygancounty.com/Tiesheets/42092020.pdf), [42040000](https://gis2.sheboygancounty.com/Tiesheets/42040000.pdf)
- **Answer key:** closes almost exactly (**0.00 ft**), area **3.65 ac** (tax roll 3.66).
- **Bonus:** compare your two road courses with the Roads centerline layer. Do they line up?
- **Your result (Nov 5, 2026, Pro 3.7.3):** ✅ misclosure **0.00 ft** (ratio better than 1:100,000), calculated area **159,015.9 sq ft (3.65 ac)**. Matches the key. **County map vs. the drafted parcel:** POC 0 ft · SW 3.57 ft · road bend 5.46 ft · NW 5.64 ft · NE 9.15 ft. Road: the county's Roads centerline crosses the drafted S47°04'W course instead of following it, so the record's "along centerline," the centerline layer, the basemap road and the county parcel line all sit in different places.
- **Measuring tip:** in Measure, click your corner once, then double-click the county's corner. One row under Segment = the offset; Path Net Distance is first click to last click, so it's wrong when there are two rows.

### Parcel 3: Village of Cascade, a jog in the boundary (6 courses)

- **Parcel ID:** 59111521840 · T14N R21E Sec 20 · 4.50 acres
- **Description:** *B-1984 - PRT SW SE, SEC 20, COM AT NE COR OF SD SW SE, TH S89 DEG 08'58"W 835.44', S28 DEG 53'33"E 478.49', N62 DEG 04'46"E 6.55', N28 DEG 13'W 129.48', N80 DEG 15'E 670.59' TH N0 DEG 22'33"W 200.61' TO BEG.*
- **Reading it:** the short 6.55 ft course is a small jog, easy to mistype. Watch the N/S and E/W letters on every course.
- **Courses:** S 89°08'58" W 835.44 · S 28°53'33" E 478.49 · N 62°04'46" E 6.55 · N 28°13'00" W 129.48 · N 80°15'00" E 670.59 · N 0°22'33" W 200.61
- **Nearest tie sheets:** [41200020](https://gis2.sheboygancounty.com/Tiesheets/41200020.pdf), [41202020](https://gis2.sheboygancounty.com/Tiesheets/41202020.pdf), [41200000](https://gis2.sheboygancounty.com/Tiesheets/41200000.pdf)
- **Answer key:** closes almost exactly (**0.00 ft**), area **4.50 ac** (tax roll 4.50).

### Parcel 4: Town of Lyndon, a description that doesn't close (6 courses)

- **Parcel ID:** 59010122560 · T14N R21E Sec 11 · 9.84 acres
- **Description:** *PRT SW NW, SEC 11, COM AT SW COR SD 1/4, TH E 425.47', S89 DEG 22'17"E 304.60', N0 DEG 3'39"W 582.58', N88 DEG 35' 9"W 729.74', S0 DEG 3'39"E 80.63', TH S 511.90' TO BEG, SUBJ TO HWY CONV AS REC IN VOL 385 P 158-59. (VOL 404 P 361-62, VOL 854 P 750)*
- **Reading it:** the SW corner of the SW¼ of the NW¼ is the **West ¼ corner** of Section 11, a monumented PLSS corner. Its tie sheet is listed first, and the county's control point sits exactly on the parcel corner.
- **Courses:** N 90°00'00" E 425.47 · S 89°22'17" E 304.60 · N 0°03'39" W 582.58 · N 88°35'09" W 729.74 · S 0°03'39" E 80.63 · S 0°00'00" E 511.90
- **Tie sheets:** [41102000](https://gis2.sheboygancounty.com/Tiesheets/41102000.pdf) is your POC. It's titled "E¼ corner, Section 10, T14N R21E, Town of Lyndon", the same monument as the W¼ corner of Section 11, at **N 156,913.115, E 153,299.705**. Type those coordinates as the traverse start point; the history on the sheet goes back to 1972. Also nearby: [41112020](https://gis2.sheboygancounty.com/Tiesheets/41112020.pdf), [41030000](https://gis2.sheboygancounty.com/Tiesheets/41030000.pdf).
- **Answer key:** misclosure **about 4.7 ft** (about 1:560), area **9.87 ac** (tax roll 9.84).
- **This one is the lesson.** A 4.7 ft gap is far beyond typing error. Work out what to do with it:
  1. Check every course for a typo. The math above uses the description exactly as written.
  2. Look at which course would fix it. Does one bearing or distance look suspicious next to the county's polygon?
  3. Note the three recorded documents (VOL 385 P 158-59 and others). In a real job you'd pull those deeds from the Register of Deeds, or the survey the description came from, before changing anything.
  4. Decide how you'd handle it in the fabric: hold the record as written and flag it, or adjust (Pro's **compass rule** spreads the error across the courses). Write one or two sentences on your choice. Interviewers love this question.

---

## 4. Test the ParcelQA script tool in Pro

The files are in `Documents\Claude outputs\ParcelQA`: `ParcelQA.pyt` and `parcel_qa.py` (keep them in the same folder).

1. **Give Pro's Python the geopandas package** (one time):
   - Pro → **Settings → Package Manager**. Click the gear next to *Active Environment* → **Clone** `arcgispro-py3` (name it `arcgispro-py3-qa`), then **Activate** the clone and restart Pro.
   - Start menu → **ArcGIS → Python Command Prompt**, then run:
     `conda install -c conda-forge geopandas pyogrio`
2. **Add the toolbox:** Catalog pane → Toolboxes → right-click → **Add Toolbox** → `ParcelQA.pyt`.
3. **Make it fast for the first run:** select a small area (one town, for example Town of Lima, by selecting parcels, address points and roads inside it), so the tool only processes the selection.
4. **Run "Run Parcel and NG911 QA"** and fill in the fields:
   - Parcels: `PARCELID`
   - Addresses: number `addrnum`, street `fullname`, full address `fulladdr`, road ID `RdCLID`, municipality `municipality`
   - Roads: ID `centerlineid`, name `fullname`, ranges `fromleft` / `toleft` / `fromright` / `toright`
   - Output: `C:\…\SheboyganParcelQA\findings_lima.gpkg`
5. The findings layer should load into your map. If anything errors, screenshot the **Messages** tab and send it to me; it's the first real test inside Pro.

---

## 5. Send me

- Four screenshots (your parcel over the county's, with the closure numbers visible).
- For each parcel: misclosure, precision ratio, your area, and anything that surprised you.
- For parcel 4: your explanation of what you'd do about the misclosure.
- The ParcelQA tool result (or the error).

I'll add a **"Drafting from the record"** section to the case study page with your screenshots and numbers, and update the homepage card.

---

## Interview talking points this gives you

- "I drafted parcels from recorded metes-and-bounds descriptions in a parcel fabric, starting from PLSS corners and their county tie sheets, and checked each traverse's closure."
- "One description didn't close by about 5 feet. Here's how I traced it and what I'd do in a real office before editing the fabric."
- "I wrote a Python QA tool that checks a county's parcels, address points and centerlines against each other and NG911 rules, and ran it on all of Sheboygan County: 135,000 features. The most common issue was addresses linked to the wrong road segment, which affects 911 routing."
