"""Compact geometry + the four card measures for the homepage prism-map card.
Usage: python3 card_data.py ../../data/winnebago ../../media/winnebago-card/card.json"""
import json, math, sys
from shapely.geometry import shape
from shapely.geometry.polygon import orient

D, OUT = sys.argv[1], sys.argv[2]
G = json.load(open(f"{D}/municipalities.geojson")); C = json.load(open(f"{D}/context.geojson"))
outline = next(f for f in C["features"] if f["properties"]["name"] == "outline")
b = shape(outline["geometry"]).bounds
lon0, lat0 = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
kx, ky = 111.32 * math.cos(math.radians(lat0)), 110.57


def rings(geom, tol):
    out = []
    g = shape(geom).buffer(0).simplify(tol, preserve_topology=True)
    for p in getattr(g, "geoms", [g]):
        if p.area < 2e-6:
            continue
        p = orient(p, 1.0)
        rr = [p.exterior] + list(p.interiors)
        out.append([[[round((x - lon0) * kx, 2), round((y - lat0) * ky, 2)] for x, y in list(r.coords)[:-1]] for r in rr if len(r.coords) > 3])
    return out


munis = []
for f in G["features"]:
    p = f["properties"]
    munis.append(dict(n=p["short"], t=p["type"], v=[round(p["pct20_26"], 4), round(p["pct20_50"], 4), round(p["pct65"], 4), round(p["med_income"])],
                      parts=rings(f["geometry"], 0.0007)))
lakes = []
from shapely.geometry import mapping
county = shape(outline["geometry"]).buffer(0)
for f in C["features"]:
    if f["properties"]["name"] != "outline":
        g = shape(f["geometry"]).buffer(0).intersection(county)
        if not g.is_empty:
            lakes += rings(mapping(g), 0.0009)
json.dump(dict(munis=munis, lakes=lakes, outline=rings(outline["geometry"], 0.0009)), open(OUT, "w"), separators=(",", ":"))
import os; print(os.path.getsize(OUT), "bytes", sum(len(r) for m in munis for pt in m["parts"] for r in pt), "vertices")
