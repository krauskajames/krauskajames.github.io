# Lake Winnebago blooms: data

| File | What it is | Source |
|---|---|---|
| `winnebago_chla_monthly.csv` | Monthly lake chlorophyll-a, June–September 2019–2025 | Earth Engine export, `lake_chlorophyll.js` with the Lake Winnebago settings |
| `winnebago_daily.csv` | One row per Sentinel-2 day, June–September 2017–2026: lake, east-shore and west-shore chlorophyll-a and the three-day wind | Earth Engine export, `winnebago_blooms.js` Part A |
| `dnr_lake_winnebago_samples_2017_2026.csv` | Wisconsin DNR field samples at the three in-lake stations (713243, 713244, 713245): chlorophyll-a, total phosphorus and Secchi depth | Water Quality Portal (waterqualitydata.us), organization WIDNR_WQX, downloaded November 24, 2026 |

The DNR chlorophyll-a values are lab results by EPA method 445.0 (extracted, fluorescence), in µg/L. The portal labels them "Chlorophyll a (probe relative fluorescence)".
