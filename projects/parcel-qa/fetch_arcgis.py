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
    body = urllib.parse.urlencode(q).encode()
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
            with urllib.request.urlopen(req, timeout=180) as r:
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


def esri_geom(g, gtype):
    """Esri JSON geometry -> shapely, without reprojection (keeps the county's native coordinates)."""
    from shapely.geometry import Point, MultiLineString, Polygon, MultiPolygon, LinearRing
    if not g:
        return None
    if gtype == "esriGeometryPoint":
        return Point(g["x"], g["y"])
    if gtype == "esriGeometryPolyline":
        return MultiLineString(g["paths"]) if len(g["paths"]) > 1 else MultiLineString(g["paths"]).geoms[0]
    rings = [r for r in g.get("rings", []) if len(r) >= 4]
    outers = [r for r in rings if not LinearRing(r).is_ccw]      # Esri: outer rings clockwise
    holes = [r for r in rings if LinearRing(r).is_ccw]
    polys = []
    for o in outers:
        po = Polygon(o)
        polys.append(Polygon(o, [h for h in holes if po.contains(Polygon(h).representative_point())]))
    if not polys:
        return None
    return polys[0] if len(polys) == 1 else MultiPolygon(polys)


def fetch(url, where="1=1"):
    from pyproj import CRS
    meta = get(url)
    page = min(meta.get("maxRecordCount", 1000) or 1000, 1000)
    sr = meta.get("extent", {}).get("spatialReference", {}) or {}
    wkid = sr.get("latestWkid") or sr.get("wkid")
    crs = CRS.from_user_input(f"EPSG:{wkid}") if wkid and wkid < 100000 else CRS.from_user_input(f"ESRI:{wkid}")
    gtype = meta.get("geometryType")
    ids = get(url + "/query", where=where, returnIdsOnly="true").get("objectIds") or []
    ids.sort()
    rows = []
    for i in range(0, len(ids), page):
        chunk = ids[i:i + page]
        d = get(url + "/query", objectIds=",".join(map(str, chunk)), outFields="*", f="json")
        for ft in d.get("features", []):
            a = dict(ft["attributes"])
            a["geometry"] = esri_geom(ft.get("geometry"), gtype)
            rows.append(a)
        print(f"  {min(i + page, len(ids)):,}/{len(ids):,}", end="\r", flush=True)
    print()
    g = gpd.GeoDataFrame(rows, geometry="geometry", crs=crs)
    for f in meta.get("fields", []):
        if f["type"] == "esriFieldTypeDate" and f["name"] in g:
            g[f["name"]] = pd.to_datetime(g[f["name"]], unit="ms", errors="coerce")
    return g, meta


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
