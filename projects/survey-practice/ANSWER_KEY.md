# Answer key

Work each part yourself first. Every number here was computed by `build_kit.py`, not typed by hand.

## 1. Boundary closure

| Course | Bearing | Distance (ft) | Latitude (ft) | Departure (ft) | Northing | Easting |
|---|---|---|---|---|---|---|
| POB | | | | | 5000.00 | 6500.00 |
| 1 | S 88°05'29" W | 1135.01 | -37.802 | -1134.380 | 4962.20 | 5365.62 |
| 2 | N 01°13'51" W | 158.57 | +158.533 | -3.406 | 5120.73 | 5362.21 |
| 3 | N 54°14'19" E | 272.29 | +159.129 | +220.952 | 5279.86 | 5583.17 |
| 4 | N 81°36'30" E | 398.06 | +58.093 | +393.798 | 5337.95 | 5976.96 |
| 5 | S 79°24'35" E | 155.82 | -28.637 | +153.166 | 5309.32 | 6130.13 |
| 6 | S 01°21'38" E | 288.47 | -288.389 | +6.849 | 5020.93 | 6136.98 |
| 7 | N 88°05'29" E | 362.08 | +12.059 | +361.879 | 5032.99 | 6498.86 |
| 8 | S 01°59'46" E | 33.00 | -32.980 | +1.149 | 5000.01 | 6500.01 |

- Perimeter: 2803.30 ft
- Misclosure: 0.010 ft (latitude +0.007, departure +0.007)
- Precision: 1 in 283,993
- Area by coordinates: 247,675 sq ft (5.6858 acres). The map states 247,672 sq ft (5.6858 acres), a difference of 3 sq ft from rounding in the bearings and distances.

## 2. Found monuments compared with the record corners

Simulated. Point 106 was set at the record position; the others were 'found' a little off, as real monuments are.

| Point | Corner at the end of course | Record N | Record E | Found N | Found E | Found minus record (ft) |
|---|---|---|---|---|---|---|
| 101 | POB | 5000.00 | 6500.00 | 5000.06 | 6500.02 | 0.06 |
| 102 | 1 | 4962.20 | 5365.62 | 4962.26 | 5365.63 | 0.06 |
| 103 | 2 | 5120.73 | 5362.21 | 5120.77 | 5362.21 | 0.04 |
| 104 | 3 | 5279.86 | 5583.17 | 5279.93 | 5583.15 | 0.07 |
| 105 | 4 | 5337.95 | 5976.96 | 5337.96 | 5976.96 | 0.01 |
| 106 | 5 | 5309.32 | 6130.13 | 5309.32 | 6130.13 | 0.00 |
| 107 | 6 | 5020.93 | 6136.98 | 5020.92 | 6136.92 | 0.06 |
| 108 | 7 | 5032.99 | 6498.86 | 5032.95 | 6498.83 | 0.05 |

## 3. Levelling loop

| Station | BS | HI | FS | Elevation | Adjusted elevation |
|---|---|---|---|---|---|
| BM1 | 6.19 | 866.19 | | 860.00 | 860.00 |
| TP1 | 6.50 | 867.87 | 4.82 | 861.37 | 861.37 |
| TP2 | 4.26 | 867.29 | 4.84 | 863.03 | 863.02 |
| TP3 | 3.66 | 865.78 | 5.17 | 862.12 | 862.11 |
| BM1 | | | 5.76 | 860.02 | 860.00 |

- Check: sum of backsights 20.61 minus sum of foresights 20.59 = +0.02 ft, the same as the loop misclosure.
- Misclosure: +0.02 ft. This exercise's tolerance is 0.02 ft × √(number of setups) = 0.04 ft for 4 setups, so the loop passes. That tolerance is a classroom figure chosen for the exercise; a real job uses the standard its specification names.
- Adjustment: spread the misclosure evenly, -0.005 ft per setup.
- Finished floor: HI at that setup 867.29 minus foresight 2.08 = 865.21 ft (unadjusted).

## 4. Stakeout from CP3, backsight CP2

Instrument at CP3 (N 4992.35, E 5519.71), backsight CP2 (N 5039.65, E 5888.34). Azimuth to the backsight: 82°41'17".

| Point | Northing | Easting | Angle right from backsight | Horizontal distance (ft) |
|---|---|---|---|---|
| A1 | 5071.97 | 5657.14 | 337°13'34" | 158.83 |
| A2 | 5069.97 | 5597.17 | 322°15'10" | 109.66 |
| A3 | 5109.95 | 5595.84 | 310°13'46" | 140.09 |
| A4 | 5111.95 | 5655.80 | 326°00'07" | 181.18 |
| O1 | 5072.30 | 5667.13 | 338°50'23" | 167.70 |
| O2 | 5069.64 | 5587.17 | 318°25'37" | 102.59 |
| O3 | 5109.61 | 5585.84 | 306°43'59" | 134.62 |
| O4 | 5112.28 | 5665.80 | 327°55'41" | 189.01 |

Check: A1 to A2 should measure 60.00 ft and A2 to A3 40.00 ft, and the two diagonals should match at 72.11 ft.
