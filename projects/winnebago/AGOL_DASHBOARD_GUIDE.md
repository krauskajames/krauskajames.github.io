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

1. Open the municipalities layer in **Map Viewer**.
2. Basemap: **Light Gray Canvas** (or Human Geography) so the colors carry the message.
3. **Styles → Choose attribute → Pct20_26 → Counts and Amounts (color)**. Set the theme to *High to low* with a diverging ramp (brown to green), then **Classify data → Manual breaks**: −3, −1, −0.25, 0.25, 1, 3. This matches the web page.
4. **Pop-ups**: use a custom attribute expression or the field list. Show Muni_Name as the title, then Pop2026, Pct20_26, Proj2050, MedHHInc, Pct65Plus, Jobs2023. Format Pop fields with thousands separators and the percent fields with one decimal.
5. **Labels**: Short_Name, 9 pt, with a white halo.
6. Optional: duplicate the layer and style the copies by MedHHInc, Pct65Plus and Density26 (sequential greens), so the dashboard can switch layers.
7. **Save as** *Winnebago County Profile Map*.

## 3. Build the dashboard

**Create app → Dashboards**, title *Winnebago County Community Profile*. Pick a light theme, then set the background and text colors under **Theme** to match the site if you want (paper `#f1f2ec`, forest `#2e4a34`).

Suggested layout: a header across the top, indicators in a row under it, the map on the left, charts in a stacked column on the right.

1. **Header**: title plus a link to `https://krauskagis.com/winnebago.html`. Add a **Category selector** to the header on *Muni_Type* (City, Village, Town) so viewers can filter.
2. **Map**: add the web map. Under **Map actions**, turn on *Filter* for the list and indicators so selecting municipalities on the map updates them.
3. **Indicators** (four, all on the municipalities layer, *Statistic*):
   - Residents 2026: Sum of Pop2026.
   - Change since 2020: Sum of Chg20_26, with a prefix "+".
   - Jobs located in the county, 2023: Sum of Jobs2023.
   - DOA projection 2050: Sum of Proj2050. Use the reference value Sum of Pop2020 and show the percent change.
4. **List**: municipalities, sorted by Pop2026 descending. Line item text, for example: `{Muni_Name}` in bold, then `{Pop2026} residents · {Pct20_26}% since 2020`.
5. **Serial chart, population**: data = *county_population* table. Category from **Grouped values**, category field **Year**, split by **Series**, statistic **Sum of Population**. Use a line for Census and DOA estimate and dashed lines for the two projections (each series is styled in the **Series** tab).
6. **Serial chart, location quotients**: data = *economy_sectors*. Category from **Features**, category field **Sector**, value field **LQ_US**. Rotate the chart to horizontal, sort by value descending, and under **Value axis → Guides** add a guide line at 1.0 labeled "U.S. average".
7. **Serial chart, shift-share**: same table, value field **RegionalComp**, horizontal, with a guide at 0. Color the bars by value if your version supports it; otherwise leave them one color.
8. **Serial chart, commuting**: data = *commute_flows*. Category field **County**, split by **Direction**, Sum of Workers. Add a filter on the element to hide "All other" if it dominates.
9. **Details** or **Rich text** element: a short methods and sources note (copy it from the Method section of the web page) and the line "Independent portfolio project. Not an official Winnebago County product."

## 4. Share it

1. Share the four tables, the feature layer, the web map and the dashboard with **Everyone (public)**. A public dashboard shows "no data" if any layer under it is private.
2. Open the dashboard in a private browser window to confirm it loads without signing in.
3. Send me the dashboard URL. I'll put it in `AGOL_URL` near the top of the script in `winnebago.html`, which turns on the "ArcGIS Online dashboard" button on the page.

## Talking points for interviews

- Why a diverging ramp for change but a sequential ramp for income.
- Why the map cuts out the lakes (density and choropleth area are based on land).
- Why the DOA projection and the extrapolation disagree, and which you'd plan around.
- Why small-town ACS numbers need margin-of-error caveats (MedInc_CV field).
