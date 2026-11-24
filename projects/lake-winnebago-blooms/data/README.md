# Lake Winnebago blooms: data

| File | What it is | Source |
|---|---|---|
| `winnebago_chla_monthly.csv` | Monthly lake chlorophyll-a, June–September 2019–2025 | Earth Engine export, `lake_chlorophyll.js` with the Lake Winnebago settings |
| `winnebago_daily.csv` | One row per Sentinel-2 day, June–September 2017–2026: lake, east-shore and west-shore chlorophyll-a and the three-day wind | Earth Engine export, `winnebago_blooms.js` Part A |
| `dnr_lake_winnebago_samples_2017_2026.csv` | Wisconsin DNR field samples at the three in-lake stations (713243, 713244, 713245): chlorophyll-a, total phosphorus and Secchi depth | Water Quality Portal (waterqualitydata.us), organization WIDNR_WQX, downloaded November 24, 2026 |

The DNR chlorophyll-a values are lab results by EPA method 445.0 (extracted, fluorescence), in µg/L. The portal labels them "Chlorophyll a (probe relative fluorescence)".

## USGS boat transects (added November 24, 2026)

| File | What it is |
|---|---|
| `usgs_flame_winnebago_60m.csv` | USGS FLAMe boat measurements on Lake Winnebago, 10 dates from August 7, 2023 to July 8, 2025, reduced to the median of the readings in each 60 m cell per date: phycocyanin (the blue-green algae pigment) and chlorophyll fluorescence, turbidity, temperature, and the FluoroProbe algae groups |
| `usgs_flame_winnebago_discrete_samples.csv` | The 44 discrete sample points inside the lake |
| `usgs_flame_winnebago_tracks.geojson` | The boat tracks as lines, for maps |
| `usgs_flame_data_dictionary.csv` | The USGS field descriptions and units, unmodified |

Source: U.S. Geological Survey, "High spatial resolution sensor-based surface water quality data along the Lake Winnebago-Fox River-Green Bay continuum in 2023-2025", https://doi.org/10.5066/P1XHRFKZ. The full continuous file (94,030 readings on the lake, 40 MB) is not kept here; James clipped it to the Wisconsin DNR lake boundary (WBIC 131100). Phycocyanin is in relative fluorescence units from a YSI EXO2 sensor, corrected for sensor response time (`bga_RFU_exo_tau`). `bluegreen_fp_ugl` is a different instrument (bbe FluoroProbe) and the two should not be mixed.
