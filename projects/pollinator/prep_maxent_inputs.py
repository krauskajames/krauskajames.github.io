"""
prep_maxent_inputs.py  —  GEOG 399 rerun: build a clean, MaxEnt-ready input set
James Krauska · Pollinator Habitat Explorer

What it does
  1. Builds one common ~250 m grid (0.0025°, EPSG:4326) masked to Wisconsin.
  2. Resamples WorldClim 2.1 (30 arc-sec) bioclim + elevation and SoilGrids layers
     onto that grid with bilinear interpolation, converts SoilGrids to real units,
     and treats SoilGrids' 0 values (lakes / no data) as NoData — not as real soil.
  3. Screens for multicollinearity (|Pearson r| >= 0.7) using a fixed priority
     order and keeps an uncorrelated, interpretable set of predictors.
  4. Builds a target-group sampling-bias grid from ALL iNaturalist plant
     observations in Wisconsin (454k records): smoothed observation density.
  5. Cleans the three host-plant occurrence sets (coordinate uncertainty <= 1 km,
     inside the mask, thinned to one record per ~1 km cell) and writes them in
     MaxEnt's species,longitude,latitude order.

Outputs (in OUT_DIR)
  layers/*.asc            float ASCII grids, NODATA_value -9999, identical headers
  bias/target_group_bias.asc
  occurrences/*.csv       one file per species
  all_layers/*.asc        every candidate layer (for reference / jackknife)
  correlation_matrix.csv, correlation_heatmap.png, selected_variables.txt, prep_log.txt

Requires:  pip install rasterio geopandas pandas numpy scipy matplotlib
"""

import os, sys, json
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_origin
from rasterio.warp import reproject, Resampling
from scipy.ndimage import gaussian_filter

# ---------------------------------------------------------------- paths ----
ONEDRIVE = r"C:\Users\kraus\OneDrive\Documents\Senior Year Geography Stevens Point"
DOWNLOADS = r"C:\Users\kraus\Downloads\UWSP Geography Senior Year"

BIO_TIF   = os.path.join(ONEDRIVE, "climate30s", "wi_bio_30s.tif")
ELEV_TIF  = os.path.join(ONEDRIVE, "climate30s", "wi_elev_30s.tif")
SOIL_DIR  = os.path.join(ONEDRIVE, "MaxEntDirectory")
WI_SHP    = os.path.join(DOWNLOADS, "WisconsinBordersShapefile", "Wisconsin Borders Shapefile", "WisconsinBorders.shp")
MOTHER_CSV = os.path.join(DOWNLOADS, "GEOG399", "GEOG399ObservationData", "GEOG399MotherObservationsTable.csv")
# WISCLAND 2.0 Level 2 (WI DNR, 30 m) — read straight out of the downloaded zip
WISCLAND_ZIP = os.path.join(ONEDRIVE, "wiscland2", "wiscland2", "wiscland2_dataset", "level2.zip")
WISCLAND_TIF_IN_ZIP = "level2/wiscland2_level2.tif"
OUT_DIR   = os.path.join(ONEDRIVE, "MaxEnt2026")

# Allow overriding paths from the command line:  python prep_maxent_inputs.py paths.json
if len(sys.argv) > 1:
    globals().update(json.load(open(sys.argv[1])))

# ---------------------------------------------------------------- settings --
CELL = 0.0025                       # degrees (~280 m E-W, ~210 m N-S at 45°N)
XMIN, YMAX = -92.90, 47.09
NCOLS, NROWS = 2440, 1840           # covers -92.90..-86.80, 42.49..47.09
NODATA = -9999.0
CORR_THRESHOLD = 0.7
UNCERTAINTY_MAX_M = 1000
THIN_CELL_DEG = 0.0125              # ~1 km thinning cell
BIAS_SIGMA_CELLS = 20               # ~5 km Gaussian smoothing for the bias surface
SEED = 399

SPECIES = {
    "Asclepias incarnata": "Asclepias_incarnata",   # swamp milkweed -> monarch
    "Lupinus perennis":    "Lupinus_perennis",      # wild lupine    -> Karner blue
    "Lysimachia ciliata":  "Lysimachia_ciliata",    # fringed loosestrife -> Macropis bee
}

BIO_NAMES = {
    1: "AnnualMeanTemp", 2: "MeanDiurnalRange", 3: "Isothermality", 4: "TempSeasonality",
    5: "MaxTempWarmestMonth", 6: "MinTempColdestMonth", 7: "TempAnnualRange",
    8: "MeanTempWettestQuarter", 9: "MeanTempDriestQuarter", 10: "MeanTempWarmestQuarter",
    11: "MeanTempColdestQuarter", 12: "AnnualPrecip", 13: "PrecipWettestMonth",
    14: "PrecipDriestMonth", 15: "PrecipSeasonality", 16: "PrecipWettestQuarter",
    17: "PrecipDriestQuarter", 18: "PrecipWarmestQuarter", 19: "PrecipColdestQuarter",
}

# SoilGrids 2.0 mapped units -> conventional units (divide by factor)
SOIL = {  # file stem in SOIL_DIR: (output name, divisor, units)
    "unclippedOrganicCarbon":          ("SoilOrganicCarbon", 10,  "g/kg"),
    "unclippedPHWater":                ("SoilPH", 10, "pH"),
    "unclippedSandiness":              ("SandContent", 10, "%"),
    "unclippedSilt":                   ("SiltContent", 10, "%"),
    "unclippedWaterContent33kpa":      ("WaterContent33kPa", 10, "vol %"),
    "unclippedWaterContent1500kpa":    ("WaterContent1500kPa", 10, "vol %"),
    "unclippedWaterContent10kpa":      ("WaterContent10kPa", 10, "vol %"),
    "unclippedCationExchangeCapacity": ("CationExchangeCapacity", 10, "cmol(c)/kg"),
    "unclippedNitrogen":               ("SoilNitrogen", 100, "g/kg"),
    "unclippedBulkDensity":            ("BulkDensity", 100, "g/cm3"),
    "unclippedCoarseFragments":        ("CoarseFragments", 10, "vol %"),
    "unclippedCarbonDensity":          ("OrganicCarbonDensity", 10, "kg/m3"),
    "unclippedOrganicCarbonStock":     ("OrganicCarbonStock", 1, "t/ha"),
}

# WISCLAND 2.0 Level 2 classes grouped into percent-cover layers
LANDCOVER = {  # output name: Level 2 class codes
    "PctEmergentWetland": [6100, 6200],   # floating aquatic + emergent/wet meadow
    "PctShrubWetland":    [6300],         # lowland scrub/shrub
    "PctForestedWetland": [6400],
    "PctGrassland":       [3100, 3200],   # forage + idle grassland
    "PctCropland":        [2100, 2200],   # crop rotation + cranberries
    "PctUplandForest":    [4100, 4200, 4300],
    "PctDeveloped":       [1100, 1200],
    "PctOpenWater":       [5000],
}

# Priority order for the collinearity screen: a variable is kept only if it is
# not strongly correlated (|r| >= 0.7) with anything already kept. Order puts the
# most ecologically direct drivers for these wetland/sand-prairie plants first.
PRIORITY = [
    "SoilOrganicCarbon", "MeanTempWarmestQuarter", "SandContent",
    "PctEmergentWetland", "PctGrassland", "PctUplandForest", "PctCropland",
    "PctDeveloped", "PctShrubWetland", "PctForestedWetland", "PctOpenWater",
    "WaterContent33kPa", "SoilPH", "PrecipWarmestQuarter", "MinTempColdestMonth",
    "PrecipSeasonality", "MeanDiurnalRange", "TempSeasonality", "Elevation",
    "AnnualPrecip", "PrecipColdestQuarter", "PrecipDriestQuarter",
    "CationExchangeCapacity", "CoarseFragments", "SiltContent", "SoilNitrogen",
    "BulkDensity", "WaterContent1500kPa", "WaterContent10kPa",
    "OrganicCarbonDensity", "OrganicCarbonStock",
    "Isothermality", "TempAnnualRange", "MaxTempWarmestMonth", "AnnualMeanTemp",
    "MeanTempColdestQuarter", "MeanTempWettestQuarter", "MeanTempDriestQuarter",
    "PrecipWettestMonth", "PrecipDriestMonth", "PrecipWettestQuarter",
]

# ---------------------------------------------------------------- helpers ---
DST_TRANSFORM = from_origin(XMIN, YMAX, CELL, CELL)
DST_CRS = "EPSG:4326"
log_lines = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); log_lines.append(s)

def resample(src_arr, src_transform, src_crs, src_nodata):
    dst = np.full((NROWS, NCOLS), np.nan, dtype="float32")
    reproject(src_arr.astype("float32"), dst,
              src_transform=src_transform, src_crs=src_crs, src_nodata=src_nodata,
              dst_transform=DST_TRANSFORM, dst_crs=DST_CRS, dst_nodata=np.nan,
              resampling=Resampling.bilinear)
    return dst

def write_asc(path, arr):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    a = np.where(np.isfinite(arr), arr, NODATA)
    with open(path, "w", newline="\n") as f:
        f.write(f"ncols {NCOLS}\nnrows {NROWS}\nxllcorner {XMIN:.6f}\n"
                f"yllcorner {YMAX - NROWS*CELL:.6f}\ncellsize {CELL}\nNODATA_value {int(NODATA)}\n")
        np.savetxt(f, a, fmt="%.5g", delimiter=" ")

def cell_index(lon, lat):
    col = np.floor((lon - XMIN) / CELL).astype(int)
    row = np.floor((YMAX - lat) / CELL).astype(int)
    ok = (col >= 0) & (col < NCOLS) & (row >= 0) & (row < NROWS)
    return row, col, ok

# ---------------------------------------------------------------- 1. mask ---
log("== 1. Wisconsin mask")
wi = gpd.read_file(WI_SHP).to_crs(DST_CRS)
mask = rasterize(((g, 1) for g in wi.geometry), out_shape=(NROWS, NCOLS),
                 transform=DST_TRANSFORM, fill=0, dtype="uint8").astype(bool)
log("   cells inside Wisconsin:", int(mask.sum()))

# ---------------------------------------------------------------- 2. layers -
log("== 2. Resampling predictors")
layers = {}
with rasterio.open(BIO_TIF) as src:
    for b in range(1, 20):
        layers[BIO_NAMES[b]] = resample(src.read(b), src.transform, src.crs, src.nodata)
with rasterio.open(ELEV_TIF) as src:
    layers["Elevation"] = resample(src.read(1), src.transform, src.crs, src.nodata)
units = {k: ("mm" if "Precip" in k and k != "PrecipSeasonality" else
              "CV %" if k == "PrecipSeasonality" else
              "SD °C×100" if k == "TempSeasonality" else
              "%" if k == "Isothermality" else
              "m" if k == "Elevation" else "°C") for k in layers}
for stem, (name, div, unit) in SOIL.items():
    with rasterio.open(os.path.join(SOIL_DIR, stem + ".tif")) as src:
        # SoilGrids stores no-data (open water / outside coverage) as 0 in these exports
        layers[name] = resample(src.read(1), src.transform, src.crs, 0) / div
        units[name] = unit

# Land cover: percent of each ~250 m cell in each WISCLAND class group.
# Each 30 m class is turned into a 0/100 grid and averaged into the coarser cell;
# pixels with no class (outside the state) are excluded from the average.
log("   land cover (WISCLAND 2.0 Level 2) -> percent cover")
with rasterio.open(f"zip://{WISCLAND_ZIP}!{WISCLAND_TIF_IN_ZIP}") as src:
    lc = src.read(1)
    has_class = lc > 0
    for name, codes in LANDCOVER.items():
        pct = np.where(np.isin(lc, codes), 100, 0).astype("uint8")
        pct[~has_class] = 255
        dst = np.full((NROWS, NCOLS), np.nan, dtype="float32")
        reproject(pct, dst, src_transform=src.transform, src_crs=src.crs, src_nodata=255,
                  dst_transform=DST_TRANSFORM, dst_crs=DST_CRS, dst_nodata=np.nan,
                  resampling=Resampling.average)
        layers[name] = dst
        units[name] = "% of cell"
    del lc, has_class, pct

# Common valid-data mask: inside Wisconsin AND every layer has data.
valid = mask.copy()
for k, a in layers.items():
    valid &= np.isfinite(a)
log("   cells valid in every layer:", int(valid.sum()),
    f"({100*valid.sum()/mask.sum():.1f}% of Wisconsin)")
for k in layers:
    layers[k][~valid] = np.nan
    v = layers[k][valid]
    log(f"   {k:26s} min {v.min():9.2f}  median {np.median(v):9.2f}  max {v.max():9.2f}  {units.get(k,'')}")

# ---------------------------------------------------------------- 3. collinearity
log("== 3. Collinearity screen (|r| >=", CORR_THRESHOLD, ")")
rng = np.random.default_rng(SEED)
idx = rng.choice(np.flatnonzero(valid.ravel()), size=50000, replace=False)
names = list(layers)
X = pd.DataFrame({k: layers[k].ravel()[idx] for k in names})
R = X.corr(method="pearson")
assert set(PRIORITY) == set(names), set(names) ^ set(PRIORITY)
selected = []
for v in PRIORITY:
    clash = [s for s in selected if abs(R.loc[v, s]) >= CORR_THRESHOLD]
    if clash:
        log(f"   drop {v:26s} r={R.loc[v, clash[0]]:+.2f} with {clash[0]}")
    else:
        selected.append(v)
log("   KEPT:", len(selected), "->", ", ".join(selected))
os.makedirs(OUT_DIR, exist_ok=True)
R.to_csv(os.path.join(OUT_DIR, "correlation_matrix.csv"), float_format="%.3f")
with open(os.path.join(OUT_DIR, "selected_variables.txt"), "w") as f:
    f.write("\n".join(f"{v}\t{units.get(v,'')}" for v in selected))
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    order = selected + [n for n in PRIORITY if n not in selected]
    fig, ax = plt.subplots(figsize=(11, 9.5))
    im = ax.imshow(R.loc[order, order].values, cmap="BrBG", vmin=-1, vmax=1)
    ax.set_xticks(range(len(order))); ax.set_xticklabels(order, rotation=90, fontsize=7)
    ax.set_yticks(range(len(order))); ax.set_yticklabels(order, fontsize=7)
    ax.axhline(len(selected)-0.5, color="k", lw=0.8); ax.axvline(len(selected)-0.5, color="k", lw=0.8)
    ax.set_title(f"Predictor correlation (Pearson r). Kept {len(selected)} variables (upper-left block)")
    fig.colorbar(im, shrink=0.7); fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "correlation_heatmap.png"), dpi=150); plt.close(fig)
except Exception as e:
    log("   (heatmap skipped:", e, ")")

# ---------------------------------------------------------------- 4. observations
log("== 4. Reading iNaturalist observations")
obs = pd.read_csv(MOTHER_CSV, encoding="latin-1", on_bad_lines="skip", low_memory=False,
                  usecols=["species", "decimalLongitude", "decimalLatitude", "coordinateUncertaintyInMeters"])
obs = obs.dropna(subset=["decimalLongitude", "decimalLatitude"])
obs = obs[obs.coordinateUncertaintyInMeters <= UNCERTAINTY_MAX_M]
r, c, ok = cell_index(obs.decimalLongitude.values, obs.decimalLatitude.values)
inside = np.zeros(len(obs), bool); inside[ok] = valid[r[ok], c[ok]]
obs = obs[inside]
log("   plant observations kept (uncertainty <= 1 km, inside mask):", len(obs))

# Target-group bias surface: smoothed density of ALL plant observations
r, c, _ = cell_index(obs.decimalLongitude.values, obs.decimalLatitude.values)
counts = np.zeros((NROWS, NCOLS), "float64"); np.add.at(counts, (r, c), 1)
dens = gaussian_filter(counts, BIAS_SIGMA_CELLS)
dens = dens / dens[valid].max()
dens = np.clip(dens, 0.001, None)          # MaxEnt needs bias values > 0
dens[~valid] = np.nan
write_asc(os.path.join(OUT_DIR, "bias", "target_group_bias.asc"), dens.astype("float32"))
log("   wrote bias/target_group_bias.asc")

# Occurrences: filter + thin to one record per ~1 km cell
summary = []
for sci, tag in SPECIES.items():
    s = obs[obs.species == sci]
    n0 = len(s)
    key = (np.floor(s.decimalLongitude / THIN_CELL_DEG).astype(int).astype(str) + "_" +
           np.floor(s.decimalLatitude / THIN_CELL_DEG).astype(int).astype(str))
    s = s.assign(k=key.values).sample(frac=1, random_state=SEED).drop_duplicates("k")
    out = pd.DataFrame({"species": tag, "longitude": s.decimalLongitude.round(6),
                        "latitude": s.decimalLatitude.round(6)})
    os.makedirs(os.path.join(OUT_DIR, "occurrences"), exist_ok=True)
    out.to_csv(os.path.join(OUT_DIR, "occurrences", f"{tag}.csv"), index=False)
    summary.append((sci, n0, len(out)))
    log(f"   {sci:22s} {n0:5d} clean records -> {len(out):5d} after 1 km thinning")

# ---------------------------------------------------------------- 5. write grids
log("== 5. Writing ASCII grids (this takes a few minutes)")
for k in selected:
    write_asc(os.path.join(OUT_DIR, "layers", f"{k}.asc"), layers[k])
    log("   layers/" + k + ".asc")
if os.environ.get("WRITE_ALL_LAYERS"):
    for k in names:
        write_asc(os.path.join(OUT_DIR, "all_layers", f"{k}.asc"), layers[k])
with open(os.path.join(OUT_DIR, "prep_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log_lines))
log("Done. Point MaxEnt at:", os.path.join(OUT_DIR, "layers"))
