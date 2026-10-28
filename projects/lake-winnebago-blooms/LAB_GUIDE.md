# Lake Winnebago algae blooms: lab guide

**Goal:** a portfolio page about the blooms on Lake Winnebago, made with Google Earth Engine and Sentinel-2 and Landsat imagery, and opened by your own story of the August weeks at the family cottages on the east shore.

**Your part:** run the Earth Engine scripts, export the results, get the DNR's sampled chlorophyll, and write the story. **My part:** the web page, the maps and charts, the homepage card, and the comparison with the DNR samples.

**Total time:** about 6–9 hours, spread over a week or two.

| # | Task | Time | Done |
|---|---|---|---|
| 0 | Set up Earth Engine | 20 min | ☐ |
| 1 | Warm up with three course lessons | 1.5–2 h | ☐ |
| 2 | Run the monthly chlorophyll monitor on Lake Winnebago | 45 min | ☐ |
| 3 | Run the daily script: clear days, east vs. west shore, wind | 45 min | ☐ |
| 4 | Make the summer filmstrips | 20 min | ☐ |
| 5 | Find the Augusts at the cottage (Landsat, back to 1984) | 30 min | ☐ |
| 6 | Download the DNR's chlorophyll samples | 30 min | ☐ |
| 7 | Write the story | 1–2 h | ☐ |
| 8 | Send me the files | 10 min | ☐ |

**Files in this folder**

| File | What it is |
|---|---|
| `monitor_config_winnebago.js` | Lake Winnebago settings to paste into the original chlorophyll script (step 2) |
| `winnebago_blooms.js` | The daily script I wrote for this lab: clear days, shores, wind, filmstrips, old Landsat summers (steps 3–5) |
| `lake_winnebago_outline.geojson` | The lake shoreline used in both scripts, from Census TIGER water areas |

---

## Background: why Lake Winnebago

- It is about 132,000 acres (530 km²), the largest inland lake in Wisconsin, and shallow, so the wind keeps stirring up phosphorus-rich sediment.
- The DNR has listed it as **impaired for total phosphorus** since 1998. The impairment indicators are low dissolved oxygen, excess algal growth and eutrophication. It is also listed for sediment and turbidity. In the 2022 assessment, both phosphorus and **chlorophyll-a** were above the thresholds for recreation and aquatic life.
- The Fox and Wolf rivers feed it. USGS estimates that about half the nutrients reaching Green Bay come out of Lake Winnebago.
- The blooms are mostly cyanobacteria (blue-green algae). They float, so the wind pushes the scum toward the downwind shore. On a west wind, that is the east shore, where the cottages are. The daily script tests exactly this.

On "worst water quality in the state": I couldn't find a source that ranks it that way. On the page, we'll say what we can check: impaired since 1998, and over the chlorophyll-a threshold in the 2022 assessment.

---

## 0. Set up Earth Engine

1. Go to [code.earthengine.google.com](https://code.earthengine.google.com) and sign in with your Google account.
2. When it asks for a Cloud project, create one (for example `krauska-gis`) and register it for **noncommercial use**. Earth Engine is free for personal learning and research. If it asks for a use type, pick the closest noncommercial option, such as education or personal research. A portfolio project is not commercial work.
3. You'll see four panels: scripts (left), the code editor (middle), **Console / Tasks / Inspector** (right), and the map (bottom).
4. Exports go to your Google Drive, into a folder named `earthengine`, which Earth Engine creates the first time.

---

## 1. Warm up with three course lessons

The short course is at [github.com/RisaRezaei/gee-water-resources-course](https://github.com/RisaRezaei/gee-water-resources-course). For each lesson, open the `.js` file on GitHub, click **Copy raw file**, then in the Code Editor click **NEW → File**, paste, and press **Run**.

| Lesson | Why it matters here |
|---|---|
| `01_data_import.js` | Filtering collections by place and date, cloud masking, composites, exports. Everything in steps 2–5 uses these. |
| `02_water_frequency.js` | Mapping a function over an image collection. The daily script does the same thing for every clear day. |
| `05_water_area_timeseries.js` | Turning a collection into a chart and a table. Same pattern as the chlorophyll charts. |

Lessons 3, 4 and 6 are worth doing later. Lesson 3 (Landsat 5/7/8/9 epochs) will help with the Horicon Marsh project.

**Try:** at the end of lesson 1, change the study point to Lake Winnebago, `ee.Geometry.Point([-88.41, 44.02])`, and run it again.

Things to be able to explain afterward:
- **ImageCollection vs Image**, and why you filter by place and date *before* mapping a function.
- **Server side vs client side:** why `print()` shows results later and why `getInfo()` is avoided.
- **Scale:** why `reduceRegion` needs a `scale` and what changes when you raise it.

---

## 2. Run the monthly chlorophyll monitor

This is the original script with Lake Winnebago settings. It gives monthly lake chlorophyll from Sentinel-2 alongside NASA's MODIS-Aqua, plus a map of summer 2025.

1. Open [lake_chlorophyll.js](https://github.com/RisaRezaei/gee-lake-chlorophyll/blob/main/lake_chlorophyll.js), copy it, and paste it into a new script named `winnebago_monthly`.
2. Open `monitor_config_winnebago.js` from this folder. In the Code Editor, select from `var CONFIG = {` down to its closing `};`, and paste the Lake Winnebago block over it.
3. Press **Run**. In the Console, the chart takes a minute or two.
4. On the map, look at the **Chl-a mean 2025** layer. Turn on **Permanent water mask** to see which pixels count as lake.
5. Open the **Tasks** tab and click **RUN** on both exports:
   - `winnebago_chla_monthly` (CSV)
   - `winnebago_chla_season_2025` (GeoTIFF)
6. Take a screenshot of the chart and the map.

**What to notice**
- Months with less than 50 km² of clear water are left off the chart (but kept in the CSV).
- MODIS usually reads lower than Sentinel-2. Its pixels are 4.6 km and use an ocean algorithm, and Lake Winnebago is murky and only about 16 km wide. That gap is a good interview point.

---

## 3. Run the daily script

Monthly medians smooth over the blooms you remember. Blooms come and go in days and move with the wind. `winnebago_blooms.js` works day by day:

- For every clear summer day since 2017, it records lake chlorophyll (median and 90th percentile).
- It records chlorophyll in a **2 km strip along the east shore** and the **west shore**.
- It records the **wind for that day and the two days before** (ERA5-Land).

1. Paste `winnebago_blooms.js` into a new script named `winnebago_daily` and press **Run**.
2. The Console prints, in order:
   - **Clear days kept**: how many days have at least half the lake cloud-free.
   - A dot chart of chlorophyll on every clear day.
   - **"Does the wind push the bloom?"**: each dot is one day. The x-axis is the wind's east-west component (positive = blowing toward the east shore). The y-axis is east-shore chlorophyll minus west-shore chlorophyll. If the cottages' side really gets the scum on west winds, the dots should rise to the right.
3. On the map, the blue and orange outlines are the west and east strips.
4. **Tasks → RUN** `winnebago_daily` (CSV). It takes 10–30 minutes, so you can move on while it runs.
5. Take a screenshot of the wind chart, whatever it shows. A weak or flat result is still a finding.

**If a chart says "Computation timed out":** that's normal for nine summers of daily data in the editor. The CSV export doesn't have the time limit. To see charts while you work, temporarily set `start: '2023-04-01'`.

---

## 4. Make the summer filmstrips

The same script (Part B) prints two animations of the clearest July and August days of `galleryYear` (2025):

- **True color**: what the lake looked like from space. Blooms show as green swirls and streaks.
- **Chlorophyll over true color**: the same days colored by chlorophyll-a (blue = low, red = high).

1. Watch both animations. Note any date where a bloom is stacked against the east shore.
2. Click each **Download link (GIF)** and save the GIFs.
3. Try another summer: change `galleryYear` (2018–2025) and run again. Pick the most striking year for the page.

If a filmstrip is empty, that summer had few clear days. Lower `0.8` in the `galleryDates` filter to `0.6`, or pick another year.

---

## 5. Find the Augusts at the cottage

Part C finds the clearest Landsat image of the lake from late July through August, for every year in `cottageYears`, back to 1984. It strings them into one filmstrip, one summer per frame.

1. Set `cottageYears` to the years of your story, for example `[1995, 2016]`. The script prints which date each frame comes from.
2. Run it and save the GIF from the **Download link**.
3. Look for the summers you remember. If the year a bloom stopped you swimming has a clear image within a week of your trip, that one image could carry the page.
4. Write down any frame where you can see the bloom, with its date.

Landsat 7 is left out because its images after 2003 have stripes across the lake. So some years won't have a frame.

---

## 6. Download the DNR's chlorophyll samples

The satellite numbers are an index until we check them against real water samples. The DNR samples Lake Winnebago (WBIC **131100**) for chlorophyll-a, phosphorus and Secchi depth.

1. Open the DNR's **Lake Water Quality** data search (search "Wisconsin DNR lake water quality data" or start from the Lake Winnebago impaired-water page, [apps.dnr.wi.gov/water/impairedDetail.aspx?key=358400](https://apps.dnr.wi.gov/water/impairedDetail.aspx?key=358400)).
2. Search for **Winnebago** and pick the Lake Winnebago stations. There are several, in Calumet, Fond du Lac and Winnebago counties.
3. For each station, download the results for 2017 to the present: chlorophyll-a, total phosphorus and Secchi depth. Save the station name and its latitude/longitude too.
4. **Optional:** EPA's **CyAN** app shows Sentinel-3 cyanobacteria estimates for big US lakes, including Lake Winnebago. Screenshots from bloom days make a good second check.

I can't reach the DNR sites from my side, so this step is yours. Download whatever format it gives you; I'll clean it up.

**What I'll do with it:** match each sample to the Sentinel-2 image closest in time (same day or ±1 day) at that station. Then I'll chart satellite vs. sample chlorophyll and report how well they agree. That's the accuracy check interviewers ask about.

---

## 7. Write the story

The story opens the page, and it's what makes the project yours. Write it in your own words. Aim for 150–300 words; I'll help edit. Things to cover:

- Who went, which cottage (Great Uncle Bob's, later Uncle Tom's), and roughly which years.
- What a normal day there was like before the bloom.
- What the bloom looked like (the blue and green marbled mats), how it smelled, and how fast it came in.
- How the wind changed it: which wind brought it in, and how long until you could swim again.
- What the adults said about it, and whether it changed over the years.
- Photos, if anyone has any from those Augusts. A photo of the cottage shoreline would be ideal.

**Privacy:** the site is public to anyone with the link. I'd keep the cottages at town level (for example "the east shore near Stockbridge") with no road or fire number, and first names only. That's your family's call.

---

## 8. Send me the files

Put these in `Documents\Claude outputs\LakeWinnebago\` or attach them in chat:

- [ ] `winnebago_chla_monthly.csv` and `winnebago_chla_season_2025.tif` (step 2)
- [ ] `winnebago_daily.csv` (step 3)
- [ ] The summer GIFs and the Augusts GIF, with the dates you noted (steps 4–5)
- [ ] Screenshots of the monthly chart, the wind chart and the map
- [ ] The DNR data downloads (step 6)
- [ ] Your story, plus any photos (step 7)

---

## Interview talking points

- **NDCI** = (red edge − red) / (red edge + red), using Sentinel-2 bands 5 and 4. Chlorophyll absorbs red light and reflects strongly in the red edge, so the index rises with algae. The Mishra & Mishra (2012) polynomial converts NDCI to mg/m³. It was fitted for turbid, productive water, which suits Lake Winnebago.
- **Cloud Score+** is Google's per-pixel cloud and shadow score for Sentinel-2. It masks better than the old QA60 band.
- **JRC Global Surface Water mask:** only pixels that are water at least 80% of the time are used. This keeps shoreline mixing, reeds and docks out of the statistics.
- **Daily vs. monthly:** a monthly median hides short blooms. Daily mosaics catch them, at the cost of more cloud gaps.
- **Why MODIS disagrees:** 4.6 km pixels that mix in shoreline, and an ocean algorithm used on murky lake water.
- **Wind and scum:** floating cyanobacteria pile up downwind. ERA5-Land's u-component of wind sorts days by direction.
- **Validation:** satellite estimates are only as good as their match to field samples. Report the agreement and its limits honestly: few same-day matches, and a station is a point while a pixel is an area.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "Computation timed out" on a chart | Use the CSV export, or shorten `start`/`end` while exploring |
| "User memory limit exceeded" | Raise `scale` (daily script) or `reduceScale` (monitor) to 100 |
| A filmstrip is blank | Too few clear days that summer; lower the 0.8 filter or change the year |
| Export stuck at "Submitted" | Normal; Earth Engine queues tasks. Check back later |
| Red error naming a line number | Copy the whole error message to me with the line it points to |

I haven't been able to run `winnebago_blooms.js` myself, because Earth Engine needs your login. If something breaks, send me the error and I'll fix it.

---

**Credits:** The monthly monitor and the course are by Parisa Abbasalizadehrezaei (MIT license, archived on Zenodo). Cite them on the page. The daily script builds on the monitor's method. Data: Copernicus Sentinel-2, Google Cloud Score+, JRC Global Surface Water, NASA MODIS-Aqua, ECMWF ERA5-Land, USGS Landsat, U.S. Census TIGER, Wisconsin DNR.
