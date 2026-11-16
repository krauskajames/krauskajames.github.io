# Chapter 3: Land division, your part

Roadmap item 46, chapter 3. The made-up PUD from chapter 2 is approved; now the field is divided into lots, streets and an outlot on a **preliminary plat**, drafted in your parcel fabric and routed to every office that reviews it.

Written for **ArcGIS Pro 3.7.3** (your version). It reuses what you learned in the Esri splitting/dividing labs and the item 4 COGO drafting (`MyCOGO2.gdb`).

**What's real and what's made up:** the parcel, its boundary, the section corners, the ordinances and the review offices are real. The developer, the lot layout, the street names and the plat are invented. Every map and table you make says "Example, not a survey."

| # | Task | Time | Done |
|---|---|---|---|
| 1 | Read the rules and fill in the rules table | 1–1.5 h | ✅ Nov 16 (Claude) |
| 2 | Find the section, quarter and the two monuments | 20 min | |
| 3 | Layout: concept 3, checked against the rules | 45 min | ✅ Nov 16 (Claude); you refine lots while drafting |
| 4 | Draft the boundary in the fabric | 30 min | |
| 5 | Draft the streets, including curves | 1.5–2.5 h | |
| 6 | Divide the blocks into lots | 1–2 h | |
| 7 | Check it: closure, areas, frontage, gaps | 30 min | |
| 8 | Lot table | 20 min | |
| 9 | Review routing table (who gets a copy) | 20 min | ✅ Nov 16 (Claude) |
| 10 | Send me the results | 10 min | |

---

## 1. The rules (filled in Nov 16, 2026)

Read from the Town of Sheboygan Code (Ch. 337 Subdivision and Land Development, Ch. 335 Zoning) and the City of Sheboygan Municipal Code (Ch. 103 Subdivisions) on Nov 16, 2026. Re-check before anything is published as current.

| Rule | Value | Source |
|---|---|---|
| What counts as a subdivision (needs a plat) | Town: 5 or more parcels or building sites of 1½ acres or less, created at once or by successive divisions within 5 years. City (applies in its ETJ): 3 or more parcels of 5 acres or less. Either way, this project is a subdivision and needs a plat. | Town § 337-9; City § 103-4; Wis. Stat. § 236.02(12) |
| Concept sketch / consultation | A sketch goes to the Plan Commission, Town Board and County Planning first (boundaries, roads, lot layout, slopes over 15°, soils, wet areas, floodplain, adjoining land the subdivider owns). A consultation meeting is recommended but not mandatory. | Town § 337-14 |
| Preliminary plat | Required for every subdivision; based on a survey by a Wisconsin-licensed land surveyor; scale **not more than 100 ft to the inch**. Must show title, location by section/township/range with a small location map, date/scale/owner/subdivider/surveyor, lot width and depth, streets, parks, utilities, easements, soils, wetlands, **10-ft contours**, floodplain, proposed improvements and covenants, approximate radii of all curves, and the surveyor's affidavit. | Town § 337-16; Wis. Stat. § 236.11 |
| Street right-of-way | **66 ft minimum** unless the Official Map says otherwise (subdivision code). The PUD zoning lets the Town Board set public ROW down to **49.5 ft**, and approve private streets narrower. City standard for local streets in its ETJ: 60 ft plus an 8-ft tree easement each side. | Town § 337-23; Town § 335-49D(2); City § 103-77 |
| Grades, curves, intersections | Town: max grade 6%; streets meet as near 90° as possible, no more than two streets at one point, no jogs under 125 ft, property corners rounded with a **12-ft radius**. City: local-street centerline radius **at least 100 ft**, no angle under 70°, offset intersections at least 150 ft apart, 15-ft corner radius. | Town § 337-23; City § 103-77 |
| Cul-de-sacs, dead ends | Permanent cul-de-sacs **500 ft max**, with a turnaround at least 100 ft in diameter (Town) / 50-ft radius (City). Half streets prohibited. | Town § 337-23; City § 103-77 |
| **Alleys** | **Not allowed** in the Town of Sheboygan. The City allows residential alleys only for topography or exceptional cases. | Town § 337-23; City § 103-78 |
| Blocks | Residential blocks **270–1,500 ft** between street lines; a 10-ft crosswalk may be required through blocks over 900 ft. Blocks should be wide enough for **two tiers of lots**. City: 1,200 ft max (1,500 for curvilinear designs with approval), crosswalk in blocks over 800 ft. | Town § 337-25; City § 103-79 |
| Lots | Every lot fronts on a public street; side lot lines at right angles or radial to the street; double-frontage lots avoided; corner lots wider; lot sizes follow zoning. In a PUD, lot width, yards, density and parking can all be varied, and lots may front on public or private streets as long as each has access to a public street. City: residential lots at least 40 ft wide at the street. | Town § 337-26; Town § 335-49D; City § 103-80 |
| Utility easements | At least **12 ft wide**, across lots or centered on rear/side lot lines, continuous from block to block; drainage easements along any watercourse. Each utility returns its easement needs within 10 working days. | Town §§ 337-24, 337-15 |
| Park / open space | Dedicate **5% of the subdivision area** for parks, playgrounds, public access and open space, or pay 5% of the platted market value (Town's choice). City (if its plan shows a park here): 1 acre per 35 lots. | Town § 337-34; City § 103-106 |
| Shared-use paths | The layout must provide for current and future shared-use paths for walking and biking, as the Town Board decides. | Town § 337-29 |
| County | Sheboygan County Planning gets two copies of the preliminary plat and reviews under its Subdivision Ordinance (Ch. 71). The county CSM checklist asks for 66 ft of frontage on a public road for new lots. | Town § 337-15; County Ch. 71 |
| City of Sheboygan ETJ | Yes, it applies: the City's ETJ is the unincorporated area within **3 miles** of the city limits, and the field is inside it (county ETJ layer). The City Planner gets two copies; the **Common Council** (on the Plan Commission's recommendation) approves final plats in the ETJ along with the Town and County. City § 103-126 says no lots may be sold or building permits issued in an ETJ subdivision until the subdivider installs streets, sewer and water to City specifications; state law limits what an ETJ city can require inside a town plat, so a planner would flag that conflict. | City §§ 103-4, 103-5, 103-126; Wis. Stat. § 236.10 |
| Who gets the streets | Streets are dedicated to the **Town** of Sheboygan (the Town names-and-approves them; it must not duplicate existing names). | Town §§ 337-23, 337-33 |
| State review (DOA) | DOA Plat Review gets two copies and checks the plat against the state platting rules (Wis. Stat. §§ 236.15, 236.16, 236.20, 236.21): monuments, minimum lot and street standards, and the drafting requirements of the final plat. DSPS gets copies where soil tests apply; DOT only if the plat abuts a state highway (Playbird Rd is not one). | Town § 337-15; DOA Plat Review |
| Timeline | Public hearing before the Plan Commission (Class 2 notice, plus written notice to owners within **200 ft**); Plan Commission recommends within **60 days** of filing; Town Board acts within **90 days**. Preliminary approval good for **36 months**; final plat within 36 months; record within 12 months of the last approval. | Town §§ 337-15, 337-17, 337-18 |

**What this means for the design:** concept 2 broke the Town's no-alley rule (its townhomes were loaded from rear alleys), its loop street had lots that didn't front a public street, and its townhome rows didn't make two-tier blocks. Concept 3 (`ch3_concept3.png`) is redrawn to these rules.

## 2. Section, quarter and monuments

From the county's PLSS and control corner layers (I checked these Nov 13):
- The field is in **Section 4, T15N, R23E** (Town of Sheboygan). Playbird Rd runs along the north line of Section 4, which is also the town line with the Town of Mosel (Section 33, T16N).
- **NW corner of Section 4:** tie sheet [53054000](https://gis2.sheboygancounty.com/Tiesheets/53054000.pdf), about N 196,399.454, E 206,412.662
- **N¼ corner of Section 4:** tie sheet [53044020](https://gis2.sheboygancounty.com/Tiesheets/53044020.pdf), about N 196,435.680, E 209,067.389

Open both tie sheets and write down the coordinates they list (they should match the numbers above; if not, the tie sheet wins). The field looks like it's in the **NW¼ of Section 4**, mostly the NE¼ of the NW¼. Confirm by checking where the sixteenth line falls. That gives the plat's location line: "Part of the NW¼ of Section 4, T15N, R23E, Town of Sheboygan, Sheboygan County, Wisconsin."

## 3. The layout: concept 3

Draft from `ch3_concept3.png` (made up, drawn to scale on the real outline, checked against the rules table):
- **Street A** (66 ft ROW) from Playbird Rd south to **Street C**, crossing **Street B**.
- **Street B** (66 ft) east–west with **stubs** to the west and east lines for future connections.
- **Street C**, a loop from Street B around the middle blocks, with **120-ft centerline curves** (over the City's 100-ft minimum).
- **North block (on Playbird Rd):** C1 commercial (2.7 ac, the odd-shaped corner), MU1 and MU2 mixed use framing Street A (1.6 ac each), APT1 apartments (3.1 ac) next to the existing R-4 apartments.
- **Middle blocks:** two tiers of 50-ft lots, the north tier fronting Street B and the south tier fronting Street C. No alleys, no double frontage.
- **South of Street C:** 50-ft lots backing onto the pond, with a 10-ft walk from Street A's axis down to the trail (the block is about 1,290 ft long, so a crosswalk belongs there).
- **APT2** (1.4 ac) at the east end, and **Outlot 1** (pond, trail, park) plus **Outlot 2** (park and trail) on the west: about 6.5 ac of open space, far above the 5% (1.6 ac) the Town requires.
- About **70 residential lots**, averaging about 5,400 sq ft, which the PUD allows because it can vary lot width and area.

Things to fix while drafting (the sketch doesn't do these yet):
- Make side lot lines **radial** on the curves (the sketch's are straight).
- Round the property corners at every intersection (12 ft, or 15 ft if the City asks).
- Add 12-ft utility easements centered on rear lot lines.
- Decide the townhome or twin-home pattern (for example, pairs of 25-ft twin-home lots inside each 50-ft frontage) and note it as a PUD condition.

The earlier concepts stay in the folder for the page's "how the design changed" story: concept 1 (a plain T) and concept 2 (looked good, but broke the no-alley rule).

## 4. Boundary in the fabric

Use `MyCOGO2.gdb` (the fabric from item 4) or make a new one the same way. The fabric has to be in the map as a fabric (drag ParcelFabric from Catalog), the same as before.

1. **Parcel Record Workflows → Create Record:** name it `PLAYBIRD-PRELIM-EXAMPLE`.
2. **Boundary:** the county has no legal description for this field, so take the county's lines as the starting boundary. Select parcel 59024341550 in the county layer, then use **Parcel Record Workflows → Copy Lines To** with Tax_Lines as the target. (If Copy Lines To isn't on your ribbon, traverse it instead: start at the N¼ corner coordinates and enter the courses below.)
3. **Build Active** and check you get one parcel of about **31.2 ac** (1,358,000 sq ft give or take).

County boundary courses, measured from the county polygon in WISCRS Sheboygan feet (azimuths, rounded; for checking, not a survey):

| From | Length (ft) | Azimuth |
|---|---|---|
| North line (Playbird Rd), west to east | about 1,733 | about 89.2° |
| East line, north to south | about 825 | about 178.7° |
| South line, east to west | about 1,334 | about 269.2° |
| Southwest jog, east to west | about 298 | about 269.2° |
| West line, south to north | about 584 | about 358.7° |
| Northwest diagonal | about 262 | about 335.9° |

## 5. Streets

Draft the right-of-way lines, not just centerlines:
1. Draw each **centerline** first in the record (Traverse, or the line tools with distance/direction). The Commons Loop and Street B have **curves**: in the Traverse pane, enter them as curve courses (radius, arc length or chord, and left/right). That's the same skill a surveyor's plat needs, and a good one to show. A true oval isn't a surveyed shape, so build the loop from straight tangents and circular curves (for example, two half-circles joined by short straights).
2. Offset both sides by half the ROW width from your rules table (33 ft each side for a 66 ft ROW) using **Edit → Modify → Parallel** (Copy Parallel). Snap the offsets to the boundary.
3. Where Street A meets Playbird Rd and where A meets B, add **corner curves** on the ROW lines (the Town section on streets may give a minimum radius; 15–25 ft corner radii are common). Use the **Fillet** tool, or enter a curve in the Traverse.
4. **Build Active.** The streets become their own parcel (a dedication to the Town) and the blocks between them become separate parcels.

## 6. Lots

Use the tools from the Esri labs:
- **Divide** (Parcel Record Workflows → Divide): select a block, divide by **equal frontage** or by **number of parcels** along the street side. Good for rows of townhome lots.
- **Split:** for one-off lines, like the commercial lot or the outlot line.
- Number the lots **1, 2, 3…** through the plat and give the outlot the name **Outlot 1**. Put the block number in a field if the fabric has one, or in the parcel name (B2-L5).
- **Build Active** after each block.

Aim for every lot to front on Street A, Street B or Playbird Rd, with at least the minimum frontage from your rules table.

## 7. Check it

- **Closure:** the Traverse pane's misclosure on anything you traversed (aim for 1:10,000 or better, as in item 4).
- **Areas add up:** total of all lots + outlot + streets = the boundary area. A small difference is rounding; a big one means a gap or an overlap.
- **Gaps and overlaps:** run your item 4 QA tool (or Pro's **Validate Topology** on the fabric) on the new parcels. Zero errors is the goal.
- **Frontage:** for each lot, measure the line along the street. Any lot under the minimum gets fixed.
- **Screenshot** the fabric with the Build result and any QA output.

## 8. Lot table

Export the record's parcels (Tax polygons for `PLAYBIRD-PRELIM-EXAMPLE`) to a table with: lot or outlot name, block, use (townhome, apartment, commercial, outlot, street), area in sq ft and acres, and street frontage in ft. Add **Calculate Geometry** fields for area if they're not there. Save it as `ch3_lots.csv`.

## 9. Review routing table (filled in Nov 16, 2026)

From Town § 337-15 and the City and state rules above:

| Office | Role | What they check | Copies |
|---|---|---|---|
| Town of Sheboygan Plan Commission, then Town Board | Approving | Ch. 337 design rules, PUD plan, comprehensive plan; public hearing with notice to owners within 200 ft | 2 + soil data |
| Sheboygan County Planning & Conservation | Approving (county planning agency) | County Subdivision Ordinance (Ch. 71) | 2 + soil data |
| City of Sheboygan Planner, Plan Commission and Common Council | Approving (extraterritorial plat jurisdiction) | City Ch. 103 and City plans and official map | 2 |
| Wisconsin DOA Plat Review | Objecting | State platting law (Wis. Stat. ch. 236) | 2 |
| Wisconsin DSPS | Objecting where soil tests apply | Lots not served by public sewer (not expected here) | 2 + soil data |
| Wisconsin DOT | Only if a state highway is abutted | Not needed: Playbird Rd is not a state highway | — |
| Each utility serving the area | Advisory | Easement locations and widths, due within 10 working days | 1 |

## 10. Send me

Into a folder like `Claude outputs\Playbird\ch3`:
- `ch3_lots.csv`
- the record's parcels exported to a file geodatabase or shapefile (`Export Features` on the Tax polygons, filtered to the record), so I can put them on the web map
- a screenshot of the fabric with your lots, and one of any QA results
- your notes: anything in the sketch you changed because of a rule

Then I'll build the chapter 3 section of playbird.html (the plat on the map, the lot table, the rules and routing tables), and we'll decide whether the tool should also build the preliminary plat sheet the way it builds the notice map.
