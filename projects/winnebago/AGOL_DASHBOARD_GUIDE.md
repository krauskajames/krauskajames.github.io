# Winnebago County profile: ArcGIS Online Dashboard

Build time: about 60–90 minutes. Everything you upload is in `agol/winnebago_dashboard_data.zip`.

| File | Becomes | Used for |
|---|---|---|
| `winnebago_municipalities.geojson` | Hosted feature layer (22 polygons) | Map, indicators, list |
| `county_population.csv` | Hosted table | Population line chart |
| `economy_sectors.csv` | Hosted table | Location quotient and shift-share bar charts |
| `commute_flows.csv` | Hosted table | Commuting bar charts |
| `age_sex.csv` | Hosted table | Age pyramid (optional) |

Percent fields (`Pct20_26`, `Pct20_50`, `Pct65Plus`, `PctPoverty`, `PctBAplus`, `PctRenter`, `MedInc_CV`) are stored as 0–100, not 0–1.

## 1. Upload the data

1. Unzip the file on your computer.
2. In ArcGIS Online, open **Content → New item**, drag in `winnebago_municipalities.geojson`, and choose **Add the file and create a hosted feature layer**. Title: *Winnebago County Municipalities 2026*. Tags: Winnebago, demographics, portfolio.
3. Repeat for each CSV. When asked about locations, choose **Do not locate features** (or "Create a hosted table") so each becomes a table.
4. Open each item's **Settings** and check that the field types came through as numbers (Pop2026, Jobs2022 and so on). If one came in as text, delete the item and re-upload; that usually means an empty cell in the first rows.

## 2. Make the web map

Your map is saved as *Winnebago Community Profile Webmap*. It ends up with four copies of the municipalities layer, one per measure.

### 2a. Basemap

1. **Basemap → Light Gray Canvas**.
2. In the basemap's layer list, hide or remove **Light Gray Reference**. This drops the basemap's own place names (Orihula, Larsen, Waukau) so they don't double up with your labels.

### 2b. Population change since 2020 (main layer)

Map Viewer's diverging themes ("Above and below") didn't work reliably on this layer, so the style uses an Arcade expression instead.

1. Rename the layer *Population change since 2020*.
2. **Styles → + Expression**, name it **Change since 2020**, and paste:

```
var v = $feature.Pct20_26;
When(
  v < -1,    "1. Lost more than 1%",
  v < -0.25, "2. Lost 0.25–1%",
  v <= 0.25, "3. About the same",
  v <= 1,    "4. Grew 0.25–1%",
  v <= 3,    "5. Grew 1–3%",
             "6. Grew more than 3%"
)
```

3. Make sure it is the **only** attribute selected (remove Pct20_26 if it is listed, or you get sized circles), then pick **Types (unique symbols)**.
4. In **Style options**, use the **⋯** next to the category count to **Sort by label**. Then set each color by clicking its swatch:

| Category | Color |
|---|---|
| 1. Lost more than 1% | `#bf7d47` |
| 2. Lost 0.25–1% | `#e3bf96` |
| 3. About the same | `#dfe1d8` |
| 4. Grew 0.25–1% | `#a8c69a` |
| 5. Grew 1–3% | `#5f945f` |
| 6. Grew more than 3% | `#2b5c37` |

5. Check the result: Clayton, Poygan, Rushford and the towns of Omro and Winneconne are darkest green. The City of Menasha, Town of Neenah, Appleton, Nekimi and Nepeuskun are brown.

### 2c. Pop-up

1. **Pop-ups → Title:** `{Muni_Name}`.
2. Delete the default fields list, then **+ Add content → Arcade**, and paste:

```
var f = $feature;
var chg = f.Pct20_26;
var sign = IIf(chg > 0, "+", "");
var inc = Text(f.MedHHInc, "$#,###");
var incNote = IIf(f.MedInc_CV > 12, " (wide margin of error)", "");

var html =
  "<b>" + Text(f.Pop2026, "#,###") + "</b> residents, Jan 1, 2026<br>" +
  sign + Text(f.Chg20_26, "#,###") + " (" + sign + Text(chg, "0.0") + "%) since the 2020 Census<br>" +
  "DOA projection for 2050: " + Text(f.Proj2050, "#,###") + "<br><br>" +
  "Median household income: " + inc + incNote + "<br>" +
  "Age 65 and older: " + Text(f.Pct65Plus, "0") + "%<br>" +
  "Jobs located here (2023): " + Text(f.Jobs2023, "#,###");

if (f.Split_Muni) { html += "<br><br><i>Winnebago County portion only.</i>"; }

return { type: "text", text: html };
```

Test it on Clayton: 5,213 residents, +884 (+20.4%) since the 2020 Census.

### 2d. Labels (two classes)

Several towns share a name with a city or village (Omro, Winneconne, Neenah, Oshkosh), so cities and towns get separate label classes.

1. **Labels → Enable labels**.
2. **Class 1, cities and villages.** Filter: `Muni_Type is not Town`. Label field: Short_Name. Bold, 10–11 pt, white halo.
3. **Class 2, towns.** **Add label class**, filter `Muni_Type is Town`. For the label, click **</>** and enter `"Town of " + $feature.Short_Name`. Regular or italic, 9 pt, slightly grey, white halo.

### 2e. Three more measures (duplicate layers)

1. In **Layers**, use the layer's **⋯ → Duplicate** three times. The copies keep the pop-up and labels.
2. Rename the copies *Median household income*, *Residents 65 and older* and *Population density*.
3. Style each one. Remove the expression, then **+ Field**, **Counts and Amounts (color)**, and a **Greens** ramp from very light to dark forest green.
4. Turn on **Classify data** with **Manual breaks**:

| Layer | Field | Breaks |
|---|---|---|
| Median household income | MedHHInc | 70000, 85000, 100000, 110000, 120000 |
| Residents 65 and older | Pct65Plus | 15, 18, 21, 24, 27 |
| Population density | Density26 | 50, 100, 250, 1000, 2500 |

   If **Classify data** stays greyed out, leave the style continuous and drag the histogram handles to the first and last break.
5. Use the eye icons so only *Population change since 2020* is visible, then **Save**.

## 3. Build the dashboard

These steps are for the current ArcGIS Dashboards editor, where selectors are elements on the canvas rather than part of the header.

**Create app → Dashboards**, title *Winnebago County Community Profile*. Under **Theme**, set the background to `#f1f2ec` and the text and accent color to `#2e4a34` to match the site.

Suggested layout: header across the top, a thin selector strip under it, indicators in a row, the map on the left, and charts stacked on the right.

1. **Header** (gear icon on the header):
   - Title: `{item/title}`. Subtitle: *Independent portfolio project · public data, 2026*.
   - **Menu items:** add **Full interactive profile** linking to `https://krauskagis.com/winnebago.html`. A URL typed in the subtitle isn't clickable; menu items are.
2. **Map:** **Add element → Map**, pick *Winnebago Community Profile Webmap*. In its settings, turn on **Legend** and **Layer visibility** so viewers can switch between the four measures.
3. **Category selector:** **Add element → Category selector** (it may be inside a **Selectors** group).
   - Data: **Grouped values**, layer *Population change since 2020*, field **Muni_Type** (City 5, Village 2, Town 15).
   - Display: **Button bar**, single selection, **None** option labeled **All**.
   - Actions: **Filter** the map's four municipality layers, the list and the four indicators. Leave the county-wide charts unticked, because their tables have no Muni_Type field.
   - Drag it into a short strip directly under the header.
4. **Indicators** (four, on *Population change since 2020*, **Statistic**):
   - Residents 2026: Sum of Pop2026.
   - Change since 2020: Sum of Chg20_26, with a "+" prefix.
   - Jobs located here, 2023: Sum of Jobs2023.
   - DOA projection 2050: Sum of Proj2050, with reference value Sum of Pop2020 shown as a percent change.
5. **List:** municipalities sorted by Pop2026, descending. Line item: `{Muni_Name}` in bold, then `{Pop2026} residents · {Pct20_26}% since 2020`.
6. **Map actions:** in the map element's **Actions** tab, add **Filter** on selection for the list and indicators, so clicking municipalities on the map narrows them.
7. **Serial chart, population:** table *county_population*. Category from **Grouped values**, field **Year**, split by **Series**, **Sum of Population**. Use solid lines for Census and DOA estimate and dashed lines for the two projections (styled in the **Series** tab).
8. **Serial chart, location quotients:** table *economy_sectors*. Category from **Features**, field **Sector**, value **LQ_US**. Horizontal, sorted by value descending, with a value-axis guide at 1.0 labeled "U.S. average".
9. **Serial chart, shift-share:** same table, value **RegionalComp**, horizontal, with a guide at 0.
10. **Serial chart, commuting:** table *commute_flows*. Category **County**, split by **Direction**, Sum of Workers. Filter out "All other" if it dominates.
11. **Rich text:** a short methods and sources note (from the Method section of the web page), plus "Independent portfolio project. Not an official Winnebago County product."

To test, click **Town** in the selector. The map should keep only the 15 towns, and the residents indicator should drop from 174,690 to 36,973. Click **All** to reset.

## 4. Share it

1. Share the four tables, the feature layer, the web map and the dashboard with **Everyone (public)**. A public dashboard shows "no data" if any layer under it is private.
2. Open the dashboard in a private browser window to confirm it loads without signing in.
3. Send me the dashboard URL. I'll put it in `AGOL_URL` near the top of the script in `winnebago.html`, which turns on the "ArcGIS Online dashboard" button on the page.

## Talking points for interviews

- Why a diverging (brown–grey–green) scheme for change but a single-hue sequential ramp for income, age and density.
- Why you switched to an Arcade expression for the change classes when the built-in theme failed.
- Why the map cuts out the lakes (density and choropleth area are based on land).
- Why the DOA projection and the extrapolation disagree, and which you'd plan around.
- Why small-town ACS numbers need margin-of-error caveats (MedInc_CV field).
