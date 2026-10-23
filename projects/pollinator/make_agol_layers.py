"""
make_agol_layers.py — package MaxEnt results for ArcGIS Online (hosted feature layers)
Outputs (zipped shapefiles, NAD83(HARN) / Wisconsin Transverse Mercator, EPSG:3071):
  PollinatorSuitableHabitat.zip  one polygon layer, field 'species' — cells >= each model's
                                 10th-percentile training-presence threshold, patches < ~1 km² removed
  PollinatorHabitatOverlap.zip   polygons by number of host plants with suitable habitat (1-3)
  PollinatorRecords.zip          thinned iNaturalist records used to train/test the models
"""
import os, sys, json, csv, zipfile, glob
import numpy as np, rasterio, geopandas as gpd, pandas as pd
from rasterio.features import shapes, sieve
from shapely.geometry import shape

RUN_DIR = r"C:\Users\kraus\OneDrive\Documents\Senior Year Geography Stevens Point\MaxEnt2026\output_landcover"
OCC_DIR = r"C:\Users\kraus\OneDrive\Documents\Senior Year Geography Stevens Point\MaxEnt2026\occurrences"
OUT_DIR = r"C:\Users\kraus\OneDrive\Documents\Senior Year Geography Stevens Point\MaxEnt2026\arcgis_online"
if len(sys.argv) > 1: globals().update(json.load(open(sys.argv[1])))
os.makedirs(OUT_DIR, exist_ok=True)

SPECIES = {"Asclepias_incarnata": ("Swamp milkweed", "Monarch butterfly"),
           "Lupinus_perennis": ("Wild lupine", "Karner blue butterfly"),
           "Lysimachia_ciliata": ("Fringed loosestrife", "Macropis nuda (oil bee)")}
MIN_CELLS = 40          # drop isolated patches smaller than ~2.5 km²
SIMPLIFY_M = 150        # generalize edges for fast web drawing
CRS_OUT = "EPSG:3071"

results = {r["Species"]: r for r in csv.DictReader(open(os.path.join(RUN_DIR, "maxentResults.csv")))}

def polygons(mask, transform, crs):
    m = sieve(mask.astype("uint8"), MIN_CELLS, connectivity=8)
    geoms = [shape(g) for g, v in shapes(m, mask=m == 1, transform=transform, connectivity=8)]
    g = gpd.GeoSeries(geoms, crs=crs).to_crs(CRS_OUT).buffer(0)
    return g.union_all().simplify(SIMPLIFY_M, preserve_topology=True)

def save(gdf, name):
    tmp = os.path.join(OUT_DIR, name)
    os.makedirs(tmp, exist_ok=True)
    gdf.to_file(os.path.join(tmp, name + ".shp"))
    with zipfile.ZipFile(os.path.join(OUT_DIR, name + ".zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in glob.glob(os.path.join(tmp, name + ".*")):
            z.write(f, os.path.basename(f))
    print("wrote", name + ".zip", f"({os.path.getsize(os.path.join(OUT_DIR, name + '.zip'))/1e6:.1f} MB)")

rows, suit = [], {}
for sid, (common, insect) in SPECIES.items():
    with rasterio.open(os.path.join(RUN_DIR, sid + ".asc")) as src:
        a = src.read(1); tr, crs = src.transform, src.crs or "EPSG:4326"
        valid = a != (src.nodata if src.nodata is not None else -9999)
    r = results[sid]; thr = float(r["10 percentile training presence Cloglog threshold"])
    suit[sid] = valid & (a >= thr)
    geom = polygons(suit[sid], tr, crs)
    rows.append({"species": common, "sci_name": sid.replace("_", " "), "pollinator": insect,
                 "threshold": round(thr, 3), "test_auc": round(float(r["Test AUC"]), 3),
                 "area_km2": round(geom.area / 1e6, 1), "geometry": geom})
    print(common, "suitable area", round(geom.area / 1e6), "km²")
save(gpd.GeoDataFrame(rows, crs=CRS_OUT), "PollinatorSuitableHabitat")

count = sum(m.astype("uint8") for m in suit.values())
ov = []
for n in (1, 2, 3):
    geom = polygons(count == n, tr, crs)
    ov.append({"n_species": n, "label": f"{n} of 3 host plants", "area_km2": round(geom.area / 1e6, 1), "geometry": geom})
save(gpd.GeoDataFrame(ov, crs=CRS_OUT), "PollinatorHabitatOverlap")

pts = []
for sid, (common, insect) in SPECIES.items():
    d = pd.read_csv(os.path.join(OCC_DIR, sid + ".csv"))
    g = gpd.GeoDataFrame(geometry=gpd.points_from_xy(d.longitude, d.latitude), crs="EPSG:4326")
    g["species"], g["sci_name"], g["source"] = common, sid.replace("_", " "), "iNaturalist via GBIF"
    pts.append(g)
save(pd.concat(pts).to_crs(CRS_OUT), "PollinatorRecords")
