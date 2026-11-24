# Chapter 1 findings so far (November 24, 2026)

All numbers come from the files in `data/`. Chlorophyll-a is the Sentinel-2 NDCI estimate (mg/m³) unless it says DNR.

## Monthly (2019–2025, June–September)
- June is always lowest (14–21). The lake median roughly doubles by late summer.
- Peak month: August in 2019, 2020, 2022, 2023, 2024; September in 2021 and 2025. Seven-year means: June 16.8, July 25.2, August 33.8, September 34.0.
- Worst month: August 2019, median 51.8, 90th percentile 67.7.
- MODIS has a value in 17 of 28 months and reads higher than Sentinel-2 in all 17 (about double on average).
- `valid_km2` is about 1.4 times too large (pixel counts on a latitude-longitude grid); the true water area is about 525 km².

## Summer 2025 map (July–September mean)
- 524 km² of water; 80% of the lake between 28 and 49; 99% below 57. Display stretch 0–60.
- 2 km east-shore strip 40.5, west strip 30.1 (east about a third higher).

## Wind test (250 clear days, June 2017 – September 2026; wind = ERA5-Land mean of the day and the two before)
| East-west wind | Days | East shore higher | Mean east minus west |
|---|---|---|---|
| Toward the east, over 1 m/s (west wind) | 92 | 78% | +11.5 |
| Under 1 m/s | 110 | 61% | +4.3 |
| Toward the west, over 1 m/s (east wind) | 48 | 25% | −4.5 |

Spearman 0.44 between wind u and east minus west; linear r² 0.11. July–September only: +14.6 on west winds, −5.5 on east winds.

By the direction the wind came from:
| From | Days | East shore higher | Mean east minus west |
|---|---|---|---|
| W | 50 | 80% | +11.8 |
| SW | 61 | 77% | +9.9 |
| S | 28 | 68% | +8.6 |
| NW | 22 | 45% | +1.9 |
| N | 12 | 58% | +1.1 |
| SE | 20 | 55% | +0.3 |
| E | 21 | 38% | −1.1 |
| NE | 36 | 25% | −4.4 |

Grandma JoAnn's claim: "The west wind blows the blue-green algae from the other side of the lake." The data agrees. A west wind is the strongest of the eight directions: the east shore is worse on 80% of those days. James also remembers finding the mat from a boat while it was crossing the lake; a possible follow-up is to show a mat moving east across consecutive clear days.

Limits: days are not independent; clear days only; an index until validated; even in light wind the east shore is higher 61% of the time.

## Worst east-shore days
2019-08-19 (east 123.5, west 61.5), 2019-07-28 (115.5 vs 36.7), 2025-09-29 (89.5 vs 45.5), 2017-08-09 (88.5 vs 19.2), 2019-08-09 (86.3 vs 29.3).

## DNR samples (Water Quality Portal)
- Three in-lake stations: 713243 (2 mi from Neenah), 713245 (3 mi off Oshkosh), 713244 (Deep Hole, south end). 120 chlorophyll-a lab results (EPA 445.0), July 2017 – September 2026. None is near the east shore.
- First check, 29 sampling dates with a clear Sentinel-2 day within two days: Spearman 0.75, Pearson 0.63; the satellite lake median is about 70–80% of the sample mean and misses most on heavy bloom days.
- Still to do: read the satellite pixel at each station on the sampling day.

## Family photos matched to data
- July 5, 2014: the kayak sail. Drifted north-northwest, so a south-southeast wind. Before the Sentinel-2 record.
- August 10–11, 2018: sheepshead; kayaks and the dog on calm water. Sentinel-2 on August 9: median 39.8, east 49.7, west 33.3. August 12: median 24.7, east 30.3, west 24.7. Light winds both days.
- September 2, 2018: the dock. Cloud on September 1 and 3. DNR samples on August 20 averaged 83.5.
- Faces are blurred in the versions for the page; James chose blurring over asking relatives. Originals are not in this repo.

## Media
`media/`: filmstrips for July–August 2025 and 2019 (true color and chlorophyll), the Landsat late-summer filmstrip 1999–2026 (21 scenes) with dated frame sheets.

## Public reports checked against the satellite (found by James, November 24, 2026)
| Report | Date | Nearest clear Sentinel-2 days |
|---|---|---|
| FOX 11: health officials warn of toxic blue-green algae in Lake Winnebago | Aug 4, 2017 | Aug 2: median 29.5, east 50.5, west 19.2. Aug 9: median 57.5, east 88.5, west 19.2. Landsat Aug 5 shows green streaks down the east side. |
| WBAY: algae bloom on Lake Winnebago | Jun 29, 2018 | Jun 28: median 43.5 (a normal June is 14–21), 90th percentile 86.5; west 40.5, east 29.2 after an east wind. |
| AnglingBuzz fishing report, Mark Schram: strong bloom, pea soup in protected areas, recent winds mixed the algae down, few slicks on the main lake as of Tuesday Sep 18 | Sep 20, 2018 | Sep 16: median 53.5, east 77.5, west 33.7. Sep 18 and 21: cloud. Sep 23: median 37.5. Sep 26: 22.5. |

| WBAY: Winnebago County Health Department warns people away from the blooms; the beach at High Cliff State Park had been closed for several days | Aug 6, 2019 | Aug 4: east 84.8, west 41.8, bright green scum visible at the north end in true color. Aug 7: east 52.2, west 23.8. |

NOAA NCCOS posts Sentinel-3 imagery of Green Bay and Lake Winnebago (the last two weeks, with a GeoTIFF archive in its HABs Explorer app). UW-Milwaukee (Todd Miller) has run a sampling buoy on the lake for algal toxins.

The fishing report adds a mechanism the wind test does not capture: strong wind mixes floating algae down into the water, so slicks form in calm weather and are moved by light to moderate wind.

Fox-Wolf Watershed Alliance (fwwa.org/harmful-algae) runs a public bloom report form; reports go to FWWA, the UW Oshkosh HABs research team and the DNR. No records are posted. Possible contact for a dated report log.

Idea for the page: a table of dated public reports (news, fishing reports, advisories) beside the satellite numbers for the same days.
