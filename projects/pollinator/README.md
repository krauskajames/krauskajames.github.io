# Pollinator Habitat Explorer: how to reproduce it

MaxEnt species distribution models for three Wisconsin host plants, published at
[krauskagis.com/pollinator.html](https://krauskagis.com/pollinator.html).

| Host plant | Pollinator | Test AUC |
|---|---|---|
| Swamp milkweed (*Asclepias incarnata*) | Monarch butterfly | 0.71 |
| Wild lupine (*Lupinus perennis*) | Karner blue butterfly | 0.84 |
| Fringed loosestrife (*Lysimachia ciliata*) | Loosestrife oil bee (*Macropis* spp.) | 0.68 |

Run the steps in order. Paths are set at the top of each script.

## 1. Get the data

| Data | Where | Notes |
|---|---|---|
| Plant observations | GBIF occurrence download, iNaturalist research-grade, Wisconsin | Must include `coordinateUncertaintyInMeters` |
| Climate + elevation | WorldClim 2.1, 30 arc-seconds | Downloaded with R, below |
| Soils | SoilGrids 2.0 (13 properties, 0–5 cm) | GeoTIFFs clipped to Wisconsin; NoData stored as 0 |
| Land cover | WI DNR Wiscland 2.0, Level 2 | Keep `level2.zip` zipped; the script reads it directly |
| State boundary | Any Wisconsin polygon shapefile | Used as the mask |

Climate download and crop, in R:

```r
library(geodata); library(terra)
out <- "climate30s"; options(timeout = 3600)
worldclim_tile("bio", lon = -95, lat = 45, path = out)   # Wisconsin crosses the -90° tile edge,
worldclim_tile("bio", lon = -85, lat = 45, path = out)   # so it needs both tiles
wi <- ext(-93.2, -86.5, 42.3, 47.3)
f <- list.files(out, "bio\\.tif$", recursive = TRUE, full.names = TRUE)
writeRaster(crop(merge(sprc(lapply(f, rast))), wi), file.path(out, "wi_bio_30s.tif"), overwrite = TRUE)
writeRaster(crop(elevation_30s(country = "USA", path = out), wi), file.path(out, "wi_elev_30s.tif"), overwrite = TRUE)
```

## 2. Build the MaxEnt inputs

```powershell
pip install rasterio geopandas pandas numpy scipy matplotlib
python prep_maxent_inputs.py
```

The script writes everything to `MaxEnt2026/`:

- `layers/*.asc` holds 22 predictors on one 0.0025° grid, masked to Wisconsin, with NoData set to -9999.
- `bias/target_group_bias.asc` is the smoothed density of all plant observations, used as MaxEnt's bias file.
- `occurrences/*.csv` holds the cleaned records (uncertainty ≤ 1 km, thinned to one per ~1 km cell) in species, longitude, latitude order.
- `prep_log.txt`, `correlation_matrix.csv` and `correlation_heatmap.png` record the collinearity screen (|r| ≥ 0.7). They show which variables were dropped and why.

Combine the three occurrence files into `occurrences/all_species.csv` with one header row.

## 3. Run MaxEnt 3.4.4

Start MaxEnt with `java -mx4000m -jar maxent.jar`. The default 512 MB of memory is too little for 250 m statewide grids.

| Setting | Value |
|---|---|
| Samples | `occurrences/all_species.csv` |
| Environmental layers | the `layers` folder, all continuous |
| Create response curves / Make pictures / Do jackknife | on |
| Output format / file type | Cloglog / asc |
| Features | Auto |
| Random seed | **off**, so the seed is fixed and results are reproducible |
| Random test percentage | 25 |
| Regularization multiplier | 1 |
| Max background points | 10000 |
| Maximum iterations | 5000 |
| Write plot data | on |
| Bias file | `bias/target_group_bias.asc` |

The run takes about 2½ hours on a laptop, mostly for the jackknife.

## 4. Build the web layers

```powershell
pip install pillow
python make_web_layers.py
```

This writes `web/*.png` (8-bit grayscale suitability in Web Mercator) and `web/pollinator.json` (statistics, variable importance, response curves and occurrence points). Copy both into the site's `data/pollinator/` folder.

## 5. Optional: ArcGIS Online layers

```powershell
python make_agol_layers.py
```

This writes three zipped shapefiles to `MaxEnt2026/arcgis_online/` (EPSG:3071), ready to upload as hosted feature layers:

- Suitable habitat for each species (10th-percentile threshold)
- Habitat overlap (1–3 host plants)
- The thinned records

Paste the public web map URL into `AGOL_URL` in `pollinator.html` to show the "Explore the data in ArcGIS Online" button.

## Design decisions

- **Target-group background.** It corrects for iNaturalist observer bias. Expect lower AUCs than an uncorrected model; the corrected ones are more trustworthy.
- **Land cover as % of each cell.** This works better than a single land-cover class per cell, and it was what made the two wetland plants model well. Their test AUC rose from 0.58 and 0.56 to 0.71 and 0.68.
- **Collinearity priority order.** Summer temperature is ranked ahead of soil pH, because pH follows Wisconsin's north–south climate gradient (r = 0.80). Ranking pH first would have removed every temperature variable.
- **Earlier version (2025).** It used 10-arc-minute climate rounded to whole numbers, soil NoData that MaxEnt read as real values, and background points from outside Wisconsin. All three are fixed here.
