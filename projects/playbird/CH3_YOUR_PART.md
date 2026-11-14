# Chapter 3: Land division, your part

Roadmap item 46, chapter 3. The made-up PUD from chapter 2 is approved; now the field is divided into lots, streets and an outlot on a **preliminary plat**, drafted in your parcel fabric and routed to every office that reviews it.

Written for **ArcGIS Pro 3.7.3** (your version). It reuses what you learned in the Esri splitting/dividing labs and the item 4 COGO drafting (`MyCOGO2.gdb`).

**What's real and what's made up:** the parcel, its boundary, the section corners, the ordinances and the review offices are real. The developer, the lot layout, the street names and the plat are invented. Every map and table you make says "Example, not a survey."

| # | Task | Time | Done |
|---|---|---|---|
| 1 | Read the rules and fill in the rules table | 1–1.5 h | |
| 2 | Find the section, quarter and the two monuments | 20 min | |
| 3 | Sketch the layout (blocks, streets, outlot) | 30–45 min | |
| 4 | Draft the boundary in the fabric | 30 min | |
| 5 | Draft the streets | 1–1.5 h | |
| 6 | Divide the blocks into lots | 1–2 h | |
| 7 | Check it: closure, areas, frontage, gaps | 30 min | |
| 8 | Lot table | 20 min | |
| 9 | Review routing table (who gets a copy) | 20 min | |
| 10 | Send me the results | 10 min | |

---

## 1. Read the rules

Fill in the **Value** column as you read, and keep the section number next to each value. This table becomes part of the page, and it's also exactly the kind of homework a county planner does before reviewing a plat.

| Rule | Where to look | Value |
|---|---|---|
| What counts as a "subdivision" (needs a plat) vs. a CSM | Wis. Stat. § 236.02(12); Town Ch. 337 § 337-9 | |
| Preliminary consultation required? | Town § 337-14 | |
| Preliminary plat contents and scale | Town § 337-16; Wis. Stat. § 236.11 | |
| Street right-of-way width (local street) | Town § 337-23 | |
| Cul-de-sac / dead-end limits, temporary stub rules | Town § 337-23 | |
| Block length limits | Town § 337-25 | |
| Lot minimums (width, depth, frontage, corner lots) | Town § 337-26; your made-up PUD can set its own within the zoning | |
| Utility easements (width, which lot lines) | Town § 337-24 | |
| Park or open-space dedication | Town § 337-28 and § 337-34 | |
| Shared-use paths | Town § 337-29 | |
| County review and minimum frontage | Sheboygan County Code Ch. 71 (Subdivision Ordinance) | |
| City of Sheboygan extraterritorial (ETJ) review: does it apply, and what does the City check? | City of Sheboygan land division ordinance; Wis. Stat. § 236.10 | |
| Who gets the streets when a plat in the ETJ dedicates them | City ordinance (usually the Town) | |
| State plat review (DOA), what it checks | Wis. Stat. §§ 236.12, 236.15–236.20; DOA Plat Review | |

Where to read them:
- Town of Sheboygan Code, Ch. 337 Subdivision and Land Development: [ecode360.com/40066421](https://ecode360.com/40066421)
- Sheboygan County Subdivision Ordinance (Ch. 71): [Planning & Conservation, Subdivision](https://sheboygancounty.com/departments/departments-f-q/planning-and-conservation/ordinances-regulations/subdivision). The county's CSM checklist says new lots need at least **66 ft of frontage** on a public road (the Town may require more).
- City of Sheboygan Code: search ecode360 for "Sheboygan, WI" → land division / subdivision chapter, and look for "extraterritorial."
- Wisconsin DOA Plat Review: the [platting manual review process](https://doa.wi.gov/DIR/_WI_Platting_Manual-Review_Process.pdf) explains approving vs. objecting authorities and ETJ distances.

What we already know (Nov 13): the county's ETJ layer puts the field inside the **City of Sheboygan's extraterritorial jurisdiction**. A plat there typically needs approval from the Town, the County and the City, and the City can review against its ordinance and plans but can't require improvements inside the subdivision. Confirm this in the City's code.

## 2. Section, quarter and monuments

From the county's PLSS and control corner layers (I checked these Nov 13):
- The field is in **Section 4, T15N, R23E** (Town of Sheboygan). Playbird Rd runs along the north line of Section 4, which is also the town line with the Town of Mosel (Section 33, T16N).
- **NW corner of Section 4:** tie sheet [53054000](https://gis2.sheboygancounty.com/Tiesheets/53054000.pdf), about N 196,399.454, E 206,412.662
- **N¼ corner of Section 4:** tie sheet [53044020](https://gis2.sheboygancounty.com/Tiesheets/53044020.pdf), about N 196,435.680, E 209,067.389

Open both tie sheets and write down the coordinates they list (they should match the numbers above; if not, the tie sheet wins). The field looks like it's in the **NW¼ of Section 4**, mostly the NE¼ of the NW¼. Confirm by checking where the sixteenth line falls. That gives the plat's location line: "Part of the NW¼ of Section 4, T15N, R23E, Town of Sheboygan, Sheboygan County, Wisconsin."

## 3. Sketch the layout

Start from `ch3_concept_sketch.png` (made up, not to scale):
- **Street A:** from Playbird Rd south into the site.
- **Street B:** east–west, with **stubs** to the west line and the east line so future streets can connect. Most codes want streets continued to the edge of the tract.
- **C1 commercial:** about 3 ac on Playbird Rd, at the west end.
- **Block 1:** apartment lots next to the existing R-4 apartments.
- **Blocks 2 and 3:** townhome lots.
- **Outlot 1:** stormwater pond and trail along the wooded south edge.

Before drafting, check the sketch against the rules table: street widths, block lengths, the distance of Street A from N 40th St, and whether the stubs need temporary turnarounds. Change the sketch if anything breaks a rule, and note what you changed and why. That note is good material for the page.

Decide the lot sizes for the made-up PUD (for example, townhome lots about 40–50 ft wide), then count roughly how many lots fit in each block.

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
1. Draw each **centerline** first in the record (Traverse, or the line tools with distance/direction).
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

## 9. Review routing table

Fill this in from step 1. It's the "who gets a copy" sheet a GIS tech or planning assistant keeps for every plat:

| Office | Role (approving / objecting / advisory) | What they check | Copies or format |
|---|---|---|---|
| Town of Sheboygan Plan Commission and Town Board | | | |
| Sheboygan County Planning (Ch. 71) | | | |
| City of Sheboygan (ETJ) | | | |
| Wisconsin DOA Plat Review | | | |
| Others you find (DOT if a state highway is involved, school district, sanitary district, utilities) | | | |

## 10. Send me

Into a folder like `Claude outputs\Playbird\ch3`:
- the filled-in rules table and routing table (just type them into a text file or this file)
- `ch3_lots.csv`
- the record's parcels exported to a file geodatabase or shapefile (`Export Features` on the Tax polygons, filtered to the record), so I can put them on the web map
- a screenshot of the fabric with your lots, and one of any QA results
- your notes: anything in the sketch you changed because of a rule

Then I'll build the chapter 3 section of playbird.html (the plat on the map, the lot table, the rules and routing tables), and we'll decide whether the tool should also build the preliminary plat sheet the way it builds the notice map.
