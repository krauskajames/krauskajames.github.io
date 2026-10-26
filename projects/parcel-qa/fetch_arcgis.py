"""Download every feature from ArcGIS REST feature layers into GeoPackages (paged queries).

    python3 fetch_arcgis.py config/sheboygan.json raw/

The config's "sources" maps an output name to a layer URL (…/FeatureServer/0) or to a service URL
plus a layer-name pattern, e.g. {"service": ".../TaxParcels/FeatureServer", "layer": "parcel"}.
"""
import json, os, re, sys, time, urllib.parse, urllib.request
import geopandas as gpd
import pandas as pd


def get(url, **q):
    q.setdefault("f", "json")
    full = url + ("?" + urllib.parse.urlencode(q) if q else "")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(full, timeout=120) as r:
                return json.load(r)
        except Exception as e:
            if attempt == 3:
                raise
            time.sleep(2 + attempt * 3)


def resolve(src):
    if isinstance(src, str):
        return src
    info = get(src["service"])
    pat = re.compile(src["layer"], re.I)
    for lyr in info.get("layers", []):
        if pat.search(lyr["name"]):
            return f"{src['service']}/{lyr['id']}"
    raise SystemExit(f"No layer matching {src['layer']!r} in {src['service']}: {[l['name'] for l in info.get('layers', [])]}")


def fetch(url, where="1=1"):
    meta = get(url)
    page = min(meta.get("maxRecordCount", 1000) or 1000, 2000)
    ids = get(url + "/query", where=where, returnIdsOnly="true").get("objectIds") or []
    ids.sort()
    frames = []
    for i in range(0, len(ids), page):
        chunk = ids[i:i + page]
        d = get(url + "/query", objectIds=",".join(map(str, chunk)), outFields="*", outSR=4326, f="geojson")
        if d.get("features"):
            frames.append(gpd.GeoDataFrame.from_features(d["features"], crs=4326))
        print(f"  {min(i + page, len(ids)):,}/{len(ids):,}", end="\r", flush=True)
    print()
    return pd.concat(frames, ignore_index=True) if frames else gpd.GeoDataFrame(geometry=[], crs=4326), meta


if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for name, src in cfg["sources"].items():
        url = resolve(src)
        print(name, "<-", url)
        g, meta = fetch(url)
        g.to_file(os.path.join(out, f"{name}.gpkg"), driver="GPKG")
        json.dump({k: meta.get(k) for k in ("name", "description", "copyrightText", "fields", "editingInfo")},
                  open(os.path.join(out, f"{name}.meta.json"), "w"), indent=1, default=str)
        print(f"  saved {len(g):,} features")
