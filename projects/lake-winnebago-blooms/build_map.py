"""Build the study-area map layers for the page: shore strips, boat tracks, stations and the summer 2025 chlorophyll overlay.

Run from the repository root before build_page.py:  python3 projects/lake-winnebago-blooms/build_map.py
Writes media/lake-winnebago/chl-2025.webp and projects/lake-winnebago-blooms/map_data.json.
"""
import csv, json, math, os
import numpy as np
from PIL import Image
from pyproj import Transformer
from shapely.geometry import shape, mapping, box, LineString, MultiLineString
from shapely.ops import transform

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "media", "lake-winnebago"); os.makedirs(OUT, exist_ok=True)
fwd = Transformer.from_crs(4326, 3071, always_xy=True).transform      # NAD83(HARN) / Wisconsin Transverse Mercator
back = Transformer.from_crs(3071, 4326, always_xy=True).transform
SHORE_KM, SPLIT_LON, LATS = 2, -88.415, (43.80, 44.15)                  # the same values as winnebago_blooms.js


def r5(geom):
    def rnd(c):
        if isinstance(c[0], (int, float)): return [round(c[0], 5), round(c[1], 5)]
        return [rnd(x) for x in c]
    m = mapping(geom); return {"type": m["type"], "coordinates": rnd(m["coordinates"])}


lake = shape(json.load(open(f"{HERE}/lake_winnebago_outline.geojson"))["features"][0]["geometry"])
lake_m = transform(fwd, lake)
strip = lake_m.difference(lake_m.buffer(-SHORE_KM * 1000))
band = transform(fwd, box(-88.70, LATS[0], -88.10, LATS[1]))
west = strip.intersection(band).intersection(transform(fwd, box(-88.70, 43.70, SPLIT_LON, 44.30)))
east = strip.intersection(band).intersection(transform(fwd, box(SPLIT_LON, 43.70, -88.10, 44.30)))
data = {
    "lake": r5(transform(back, lake_m.simplify(40))),
    "west": r5(transform(back, west.simplify(40))), "east": r5(transform(back, east.simplify(40))),
    "west_km2": round(west.area / 1e6, 1), "east_km2": round(east.area / 1e6, 1),
}

# USGS boat tracks, one multi-line per date
tracks = {}
for ft in json.load(open(f"{HERE}/data/usgs_flame_winnebago_tracks.geojson"))["features"]:
    p = ft["properties"]; d = str(p.get("utc_date") or p.get("date") or p.get("run_start_utc") or "")[:10]
    g = transform(fwd, shape(ft["geometry"])).simplify(60)
    tracks.setdefault(d, []).extend(list(g.geoms) if g.geom_type == "MultiLineString" else [g])
pig = {}
for r in csv.DictReader(open(f"{HERE}/data/usgs_flame_winnebago_60m.csv")):
    if r["phycocyanin_rfu"]: pig.setdefault(r["date"], []).append(float(r["phycocyanin_rfu"]))
data["tracks"] = [{"date": d, "pigment": round(float(np.median(pig[d])), 2) if d in pig else None,
                   "geometry": r5(transform(back, MultiLineString([l for l in ls if l.length > 0])))} for d, ls in sorted(tracks.items())]

# DNR in-lake stations and their chlorophyll sample counts
st = {}
for r in csv.DictReader(open(f"{HERE}/data/dnr_lake_winnebago_samples_2017_2026.csv")):
    s = st.setdefault(r["station_id"], {"id": r["station_id"], "name": r["station"], "lat": float(r["lat"]), "lon": float(r["lon"]), "chl": 0})
    if r["parameter"].startswith("Chlorophyll"): s["chl"] += 1
data["stations"] = sorted(st.values(), key=lambda s: -s["lat"])
data["places"] = [{"name": "Pipe", "lat": 43.9164, "lon": -88.3068, "note": "The east-shore community near the family cottage"},
                  {"name": "High Cliff State Park", "lat": 44.163, "lon": -88.290, "note": "Beach closed for several days in early August 2019"}]

# Summer 2025 chlorophyll overlay, warped to Web Mercator so it sits correctly on the web map
tif = f"{HERE}/data/winnebago_chla_season_2025.tif"
if os.path.exists(tif):
    import rasterio
    from rasterio.warp import calculate_default_transform, reproject, Resampling
    with rasterio.open(tif) as src:
        tr, w, h = calculate_default_transform(src.crs, "EPSG:3857", src.width, src.height, *src.bounds, resolution=45)
        dst = np.full((h, w), np.nan, dtype="float32")
        a = src.read(1).astype("float32"); a[a == 0] = np.nan
        reproject(a, dst, src_transform=src.transform, src_crs=src.crs, dst_transform=tr, dst_crs="EPSG:3857",
                  resampling=Resampling.average, src_nodata=np.nan, dst_nodata=np.nan)
    stops = [(0x08, 0x30, 0x6b), (0x21, 0x71, 0xb5), (0x4e, 0xb3, 0xd3), (0x7f, 0xcd, 0xbb), (0xc7, 0xe9, 0xb4), (0xfe, 0xe0, 0x8b), (0xfc, 0x8d, 0x59), (0xd7, 0x30, 0x27)]
    t = np.clip(np.nan_to_num(dst, nan=0) / 60, 0, 1) * (len(stops) - 1); i = np.minimum(t.astype(int), len(stops) - 2); fr = (t - i)[..., None]
    S = np.array(stops, dtype="float32"); rgb = S[i] * (1 - fr) + S[i + 1] * fr
    rgba = np.dstack([rgb, np.where(np.isfinite(dst), 255, 0)]).astype("uint8")
    Image.fromarray(rgba, "RGBA").save(os.path.join(OUT, "chl-2025.webp"), "WEBP", quality=88, method=6)
    inv = Transformer.from_crs(3857, 4326, always_xy=True).transform
    x0, y1 = tr * (0, 0); x1, y0 = tr * (w, h); lo0, la0 = inv(x0, y0); lo1, la1 = inv(x1, y1)
    data["overlay"] = {"file": "chl-2025.webp", "bounds": [[round(la0, 5), round(lo0, 5)], [round(la1, 5), round(lo1, 5)]], "size": [w, h]}
    json.dump(data["overlay"], open(f"{HERE}/map_overlay.json", "w"))
elif os.path.exists(f"{HERE}/map_overlay.json"):
    data["overlay"] = json.load(open(f"{HERE}/map_overlay.json"))

json.dump(data, open(f"{HERE}/map_data.json", "w"), separators=(",", ":"))
print("ok map_data.json", f"{os.path.getsize(f'{HERE}/map_data.json') / 1024:.0f} KB", "| tracks", [t["date"] for t in data["tracks"]],
      "| strips km2", data["west_km2"], data["east_km2"], "| overlay", data.get("overlay"))
