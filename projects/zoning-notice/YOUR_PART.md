# Zoning hearing notice packet: your part

Roadmap item 37, chapter 2 of item 46 (Playbird Rd: from farm field to neighborhood).
Written for **ArcGIS Pro 3.7.3**. No extra installs: the toolbox uses arcpy and matplotlib, which ship with Pro's default `arcgispro-py3` environment (your `arcgispro-py3-qa` clone has them too).

| # | Task | Time | Done |
|---|---|---|---|
| 1 | Hand run: 200 ft selection and owner count | 20 min | ✅ Nov 8: 29 parcels, 17 owner rows |
| 2 | Get the toolbox onto your laptop | 5 min | ✅ Nov 11 |
| 3 | Make a notice map layout (once) | 20 min | ✅ Nov 13 |
| 4 | Run the tool on 59024341550 | 10 min | ✅ Nov 13 |
| 5 | Check the results against the hand run | 15 min | ✅ 29 parcels, 15 letters, Town of Mosel |
| 6 | Send me screenshots and numbers | 10 min | ✅ Nov 13, on playbird.html |
| 7 | Re-run with **Build the notice map layout for me** checked | 5 min | |

## 2. Get the toolbox

From PowerShell (in the folder where you keep the portfolio repo):

```powershell
git pull
```

Or download `ZoningNotice.pyt` and `notice_core.py` from `projects/zoning-notice/` on GitHub into one folder. They must stay in the same folder.

In Pro: **Catalog pane → Toolboxes → right-click → Add Toolbox →** `ZoningNotice.pyt`.

## 3. Notice map layout (once)

*Since Nov 13 the tool can build this for you: leave **Build the notice map layout for me** checked and it makes a new map and an ANSI D layout called "Notice Map (auto)" (zoning underneath, red subject outline, letter labels, legend, north arrow, scale bar, sources) and exports `notice_map.pdf`. The manual steps below are only for your own layout.*

The Town's petition asks for a plot plan at **1 in = 100 ft** (1:1,200). The notice area is about 1,500 ft across, so that scale needs a big sheet.

1. **Insert → New Layout → ANSI Landscape → Tabloid (11 x 17)** or **ANSI D (22 x 34)**. Name it `Notice Map`.
2. Add one map frame for your map, a north arrow, a scale bar (feet) and a title text box.
3. Map symbology (the layers appear after the first run, so you can do this after step 4):
   - `zn_subject`: no fill, thick red outline
   - `zn_notice_buffer`: no fill, dashed outline
   - `zn_notified_parcels`: light fill, labeled with the `LETTER` field (the number on each owner's letter)
   - Town zoning layer underneath, so adjacent districts show (the plot plan must show them)

If the sheet is too small at 1:1,200, the tool warns you and still exports at that scale. Use a bigger sheet or clear the scale box to fit the page.

## 4. Run the tool

**Zoning Hearing Notice Packet**:

| Parameter | Value |
|---|---|
| Parcels | your Sheboygan County `Parcel` layer |
| Parcel ID field | `PARCELID` (filled in for you) |
| Subject parcel ID(s) | `59024341550` |
| Notice distance | 200 Feet (US Survey) |
| Municipal clerk notice distance | 1000 Feet (US Survey) |
| Municipality holding the hearing | leave blank (uses the subject parcel's MUNI) |
| Output folder | e.g. `Documents\Portfolio\zoning-notice\run1` |
| Notice map layout | `Notice Map` (after step 3) |
| Field names | filled in for you (OWNERNME1, OWNERNME1ALT, PSTLADDRESS, PSTLCITY, PSTLSTATE, PSTLZIP5, PSTLZIP4, SITEADDRESS, MUNI, isROW) |

It ignores any selection on the layer, adds three layers to the map and writes these files:

- `mailing_list.csv`: one row per letter (label lines, parcel count, absentee and subject-owner flags)
- `parcels_in_notice_area.csv`: every parcel with its letter number, or why it was left out
- `review.csv`: owner pairs that look alike but were not merged
- `clerks_to_notify.csv`: other municipalities within 1,000 ft
- `labels_avery5160.pdf`: print on Avery 5160/8160 labels
- `summary.txt`: the counts
- `notice_map.pdf`: if you picked a layout

## 5. Check it against the hand run

Expected, from your hand run on Nov 8:

- parcels in notice area: **29**
- owner name rows as recorded: **17**
- parcels excluded: **1** (the blank owner; check what that parcel is: road, outlot or common area?)
- letters to owners: **15** if the two Peterson & Sons rows have the same mailing address (they merge). If the addresses differ, it will be 16, and `review.csv` lists the pair.
- clerks to notify: **TOWN OF MOSEL**

If a number is different, send me `summary.txt` and `parcels_in_notice_area.csv`.

## 6. Send me

- `summary.txt` (paste the text)
- a screenshot of the map with the three layers
- `notice_map.pdf` (or a screenshot of it)
- page 1 of `labels_avery5160.pdf`, as a screenshot. Blur the names if you'd like, but the page will use made-up names anyway.
