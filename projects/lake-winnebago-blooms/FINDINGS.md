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

### Bias check: the two shores with the wind left out (added November 24, 2026, James's question)
- East strip higher on 151 of 250 clear days (60%). Medians: east 25.4, west 23.2 mg/m³; median gap +1.5.
- Wind with a westerly part on 155 days, easterly on 95, so some of the 60% is the wind itself.
- Almost no east-west wind (under 0.5 m/s, 55 days): east higher 65%, median gap +2.5. So part of the east lean is not wind. Cause not tested.
- East-west wind from the west side, 1 m/s or more (92 days): east higher 78%, median gap +6.0.
- From the east side, 1 m/s or more (48 days): east higher 25%, median gap −3.1.
- Reading: the wind moves the result both ways from a 60% starting point, and a west wind widens the east's lead more than an east wind reverses it. The fair comparison for the 80% west-wind figure is 60%, not 50%.

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

## USGS boat transects, 2023–2025 (found by James, November 24, 2026)
Phycocyanin (blue-green pigment) from a boat-mounted sensor, with GPS, including runs close to the east shore. First look, median phycocyanin (RFU) east of −88.36 against west of −88.47:
| Boat date | East | West | Nearest clear Sentinel-2 day (chlorophyll, mg/m³) |
|---|---|---|---|
| Aug 7, 2023 | 1.34 | 2.76 | Aug 6: east 25.1, west 26.3, after an east wind |
| June 24, 2024 | 0.52 | 1.48 | June 26: east 20.7, west 17.5 |
| July 29, 2024 | 6.25 | 3.86 | July 31: east 68.7, west 24.2 |
| Aug 19, 2024 | 3.44 | 3.21 | Aug 20: east 31.7, west 33.2 |

Three of the four agree in direction. The two halves of each boat run are hours apart, so this is rough.
Same-day candidate: on July 8, 2025 the boat ran 16:03–16:46 UTC in the northeast part of the lake and Sentinel-2 passed that morning with 55% of the lake clear. July 29, 2024 has the strongest bloom but Sentinel-2 was clouded out on July 28 and next clear on July 31; Sentinel-3 or Landsat may cover it.
Next: sample the satellite pixel under each 60 m cell in Earth Engine.

## Which boat dates a satellite could see (November 24, 2026)
Same-day true color from NASA GIBS (MODIS Terra about 10:30 am, NOAA-20 VIIRS about 1:30 pm); sheet in `media/usgs_boat_dates_cloud_check.png`.
- Clear: June 24, 2024 (both passes; early-season, low bloom). August 7, 2023 (afternoon). August 19, 2024 (morning; broken cloud in the afternoon). July 7, 2025 (afternoon).
- Partly usable: June 25, 2024 (north end, morning). July 8, 2025 (haze bands in the morning, partly clear in the afternoon).
- Overcast: August 8, 2023; July 29, 2024; April 28 and May 1, 2025.
July 29, 2024 has the strongest bloom in the boat data but was overcast all day, so no optical satellite can be matched to it on the day. Against NOAA's July 29–August 7 maximum composite (Sentinel-3 CIcyano, 333 pixels), boat phycocyanin correlates weakly (Spearman 0.15): the composite is not a same-day image. Both do put the east side higher that week (boat median 5.1 vs 4.3 RFU; composite DN 218 vs 184).

## Boat-to-satellite matchup (winnebago_boat_match.js, run November 24, 2026)
8,900 boat cells (60 m) on eight dates; 7,315 have boat phycocyanin and a Sentinel-2 clear score of 0.65 or more. Rank correlations (Spearman) with boat phycocyanin:
- Sentinel-2 chlorophyll estimate (NDCI): 0.63 pooled. By date: 0.49, 0.54, 0.57, 0.55, 0.25, 0.18, 0.27, and 0.67 on July 8, 2025, the only same-day pair. By time gap: 0.67 same day, 0.61 one day, 0.65 two days.
- Date medians, eight dates: 0.81 (Pearson 0.85).
- A second instrument, the FluoroProbe blue-green estimate: 0.61 (3,203 cells).
- Cloud threshold: 0.62 at 0.5, 0.63 at 0.65, 0.48 at 0.8 (the strict threshold removes about half the cells).
- Floating Algae Index: −0.17 pooled, sign changes by date. No relationship.
- MODIS near-infrared minus red, same day: 0.00 (Terra), 0.09 (Aqua). No relationship; the 250 m product has no cloud mask.
- Boat chlorophyll fluorescence against the satellite chlorophyll estimate: −0.19. The satellite index follows the boat's blue-green pigment, not its chlorophyll channel.
- Turbidity: phycocyanin and turbidity 0.74; satellite estimate and turbidity 0.66. With turbidity held constant, phycocyanin and the satellite estimate still correlate at 0.30.
