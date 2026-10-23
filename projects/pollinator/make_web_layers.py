"""
make_web_layers.py  —  turn MaxEnt outputs into light web layers for krauskagis.com
James Krauska · Pollinator Habitat Explorer

For each species:
  * reprojects the cloglog suitability grid to Web Mercator (EPSG:3857),
  * stores it as an 8-bit grayscale+alpha PNG (value 0-250 = suitability 0-1 in 0.02 steps,
    alpha 0 = no data). The web page colours it in the browser, so the palette
    lives in CSS/JS, not baked into the image, and clicks can read real values.
Also writes pollinator.json with model statistics, variable importance,
response curves and the (thinned) occurrence points.

Requires: pip install rasterio numpy pandas pillow
Usage:    python make_web_layers.py   (edit the paths below first)
"""
import os, sys, csv, json, glob
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.transform import array_bounds
from rasterio.warp import transform_bounds
from PIL import Image

ROOT    = r"C:\Users\kraus\OneDrive\Documents\Senior Year Geography Stevens Point\MaxEnt2026"
RUN_DIR = os.path.join(ROOT, "output_landcover")
LAYERS  = os.path.join(ROOT, "layers")
OCC_DIR = os.path.join(ROOT, "occurrences")
OUT_DIR = os.path.join(ROOT, "web")
if len(sys.argv) > 1:
    globals().update(json.load(open(sys.argv[1])))

MERC_RES = 400            # metres per pixel in Web Mercator (~280 m on the ground at 45°N)
TOP_CURVES = 4            # response curves kept per species

SPECIES = [
    {"id": "Asclepias_incarnata", "common": "Swamp milkweed", "sci": "Asclepias incarnata",
     "insect": "Monarch butterfly", "insect_sci": "Danaus plexippus"},
    {"id": "Lupinus_perennis", "common": "Wild lupine", "sci": "Lupinus perennis",
     "insect": "Karner blue butterfly", "insect_sci": "Lycaeides melissa samuelis"},
    {"id": "Lysimachia_ciliata", "common": "Fringed loosestrife", "sci": "Lysimachia ciliata",
     "insect": "Loosestrife oil bee", "insect_sci": "Macropis spp."},
]

LABELS = {  # variable -> (readable label, unit, group)
    "SoilOrganicCarbon": ("Soil organic carbon", "g/kg", "Soil"),
    "SandContent": ("Sand content", "%", "Soil"),
    "WaterContent33kPa": ("Water at field capacity", "vol %", "Soil"),
    "WaterContent1500kPa": ("Water at wilting point", "vol %", "Soil"),
    "WaterContent10kPa": ("Water at 10 kPa", "vol %", "Soil"),
    "CationExchangeCapacity": ("Cation exchange capacity", "cmol(c)/kg", "Soil"),
    "CoarseFragments": ("Coarse fragments", "vol %", "Soil"),
    "SoilNitrogen": ("Soil nitrogen", "g/kg", "Soil"),
    "OrganicCarbonDensity": ("Organic carbon density", "kg/m³", "Soil"),
    "MeanTempWarmestQuarter": ("Summer mean temperature", "°C", "Climate"),
    "PrecipWarmestQuarter": ("Summer precipitation", "mm", "Climate"),
    "PrecipColdestQuarter": ("Winter precipitation", "mm", "Climate"),
    "AnnualPrecip": ("Annual precipitation", "mm", "Climate"),
    "MeanDiurnalRange": ("Mean daily temperature range", "°C", "Climate"),
    "PctEmergentWetland": ("Emergent / wet meadow", "% of cell", "Land cover"),
    "PctShrubWetland": ("Shrub wetland", "% of cell", "Land cover"),
    "PctForestedWetland": ("Forested wetland", "% of cell", "Land cover"),
    "PctGrassland": ("Grassland", "% of cell", "Land cover"),
    "PctCropland": ("Cropland", "% of cell", "Land cover"),
    "PctUplandForest": ("Upland forest", "% of cell", "Land cover"),
    "PctDeveloped": ("Developed", "% of cell", "Land cover"),
    "PctOpenWater": ("Open water", "% of cell", "Land cover"),
}

os.makedirs(OUT_DIR, exist_ok=True)
results = {r["Species"]: r for r in csv.DictReader(open(os.path.join(RUN_DIR, "maxentResults.csv")))}

def layer_range(var):
    """5th-95th percentile of a predictor inside Wisconsin, to trim MaxEnt's padded curve ends."""
    with rasterio.open(os.path.join(LAYERS, var + ".asc")) as src:
        a = src.read(1, masked=True).compressed()
    return float(np.percentile(a, 1)), float(np.percentile(a, 99))

ranges = {}
out = {"species": [], "variables": {k: {"label": v[0], "unit": v[1], "group": v[2]} for k, v in LABELS.items()}}

for sp in SPECIES:
    sid = sp["id"]
    with rasterio.open(os.path.join(RUN_DIR, sid + ".asc")) as src:
        data = src.read(1).astype("float32")
        nod = src.nodata if src.nodata is not None else -9999
        data[data == nod] = np.nan
        tr, w, h = calculate_default_transform("EPSG:4326", "EPSG:3857", src.width, src.height,
                                               *src.bounds, resolution=MERC_RES)
        merc = np.full((h, w), np.nan, "float32")
        reproject(data, merc, src_transform=src.transform, src_crs="EPSG:4326", src_nodata=np.nan,
                  dst_transform=tr, dst_crs="EPSG:3857", dst_nodata=np.nan, resampling=Resampling.bilinear)
    val = np.where(np.isfinite(merc), np.clip(np.round(merc * 50) * 5, 0, 250), 0).astype("uint8")
    alpha = np.where(np.isfinite(merc), 255, 0).astype("uint8")
    Image.fromarray(np.dstack([val, alpha]), "LA").save(os.path.join(OUT_DIR, f"{sid}.png"), optimize=True)
    minx, miny, maxx, maxy = array_bounds(h, w, tr)
    w84 = transform_bounds("EPSG:3857", "EPSG:4326", minx, miny, maxx, maxy)
    out["raster"] = {"width": w, "height": h, "res": MERC_RES,
                     "merc_bounds": [minx, miny, maxx, maxy],
                     "latlng_bounds": [[w84[1], w84[0]], [w84[3], w84[2]]]}

    r = results[sid]
    contrib = {k.replace(" contribution", ""): float(v) for k, v in r.items() if k.endswith(" contribution")}
    perm = {k.replace(" permutation importance", ""): float(v) for k, v in r.items() if k.endswith(" permutation importance")}
    order = sorted(contrib, key=lambda k: contrib[k] + perm[k], reverse=True)

    curves = []
    for var in order[:TOP_CURVES]:
        if var not in ranges:
            ranges[var] = layer_range(var)
        lo, hi = ranges[var]
        pts = [(float(x), float(y)) for _, x, y in csv.reader(open(os.path.join(RUN_DIR, "plots", f"{sid}_{var}.dat")))
               if _ != "variable"]
        pts = [p for p in pts if lo <= p[0] <= hi]
        step = max(1, len(pts) // 80)
        curves.append({"var": var, "points": [[round(x, 3), round(y, 4)] for x, y in pts[::step]]})

    occ = list(csv.DictReader(open(os.path.join(OCC_DIR, sid + ".csv"))))
    out["species"].append({
        **sp,
        "png": f"{sid}.png",
        "n_train": int(r["#Training samples"]), "n_test": int(r["#Test samples"]),
        "auc_train": float(r["Training AUC"]), "auc_test": float(r["Test AUC"]),
        "auc_sd": float(r["AUC Standard Deviation"]),
        "threshold": float(r["10 percentile training presence Cloglog threshold"]),
        "test_omission": float(r["10 percentile training presence test omission"]),
        "binomial_p": float(r["10 percentile training presence binomial probability"]),
        "iterations": int(r["Iterations"]),
        "importance": [{"var": k, "contribution": round(contrib[k], 1), "permutation": round(perm[k], 1)} for k in order],
        "curves": curves,
        "points": [[round(float(o["longitude"]), 4), round(float(o["latitude"]), 4)] for o in occ],
    })
    print(f"{sid}: {w}x{h}px  test AUC {r['Test AUC']}  top: {', '.join(order[:4])}")

with open(os.path.join(OUT_DIR, "pollinator.json"), "w") as f:
    json.dump(out, f, separators=(",", ":"))
print("Wrote", OUT_DIR)
