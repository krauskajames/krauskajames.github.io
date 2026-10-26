"""Web outputs for the QA page: findings GeoJSON, summary and small SVG close-ups of example findings.

    python3 make_web.py config/sheboygan.json out ../../data/parcel-qa
"""
import json, os, re, sys
import geopandas as gpd
import pandas as pd
from shapely.geometry import box, Point

cfg_path, OUT, WEB = sys.argv[1], sys.argv[2], sys.argv[3]
cfg = json.load(open(cfg_path))
base = os.path.dirname(os.path.abspath(cfg_path))
os.makedirs(WEB, exist_ok=True)
E = gpd.read_file(os.path.join(OUT, "qa_findings.gpkg"))
S = pd.read_csv(os.path.join(OUT, "qa_summary.csv"))
meta = json.load(open(os.path.join(OUT, "qa_meta.json")))
rd = lambda k: gpd.read_file(os.path.join(base, cfg["inputs"][k])).to_crs(3071)
P, A, R, M = rd("parcels"), rd("addresses"), rd("roads"), rd("municipalities")

# ---- findings for the map
W = E.to_crs(4326)
feats = []
for r in W.itertuples():
    feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [round(r.geometry.x, 6), round(r.geometry.y, 6)]},
                  "properties": {"c": r.check, "id": r.feature_id, "d": r.detail}})
json.dump({"type": "FeatureCollection", "features": feats}, open(os.path.join(WEB, "findings.geojson"), "w"), separators=(",", ":"))
mun = M.copy()
mf = cfg["muni_fields"]
mun = mun.dissolve(by=mf["name"]).reset_index()
mun["geometry"] = mun.geometry.simplify(15)
json.dump(json.loads(mun[[mf["name"], "geometry"]].rename(columns={mf["name"]: "name"}).to_crs(4326).to_json(drop_id=True)),
          open(os.path.join(WEB, "municipalities.geojson"), "w"), separators=(",", ":"))

# ---- summary
totals = meta["totals"]
summary = dict(county=meta["county"], totals=totals, checks=meta["checks"],
               counts={r.check: int(r["count"]) for _, r in S.iterrows()},
               flagged_features={"addresses": int(E[E.layer == "addresses"].feature_id.nunique()),
                                 "parcels": int(E[E.layer == "parcels"].feature_id.nunique()),
                                 "roads": int(E[E.layer == "roads"].feature_id.nunique())})
af = cfg["address_fields"]
not_run = []
if af.get("parcel_id") and (af["parcel_id"] not in A.columns or A[af["parcel_id"]].isna().all()):
    not_run.append("A02")
summary["not_run"] = not_run
json.dump(summary, open(os.path.join(WEB, "summary.json"), "w"), indent=1)

# ---- example close-ups (SVG)
pid = cfg["parcel_fields"]["id"]
aid = cfg["address_fields"]["id"]
rid = cfg["road_fields"]["id"]


def svg_close(center, radius, hl_parcels=(), hl_roads=(), hl_points=(), mark=None, w=420, h=300):
    x0, y0 = center.x - radius * w / h, center.y - radius
    x1, y1 = center.x + radius * w / h, center.y + radius
    bb = box(x0, y0, x1, y1)
    sx = lambda x: (x - x0) / (x1 - x0) * w
    sy = lambda y: h - (y - y0) / (y1 - y0) * h

    def path(g):
        out = []
        for poly in getattr(g, "geoms", [g]):
            if poly.geom_type == "Polygon":
                for ring in [poly.exterior] + list(poly.interiors):
                    out.append("M" + "L".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in ring.coords) + "Z")
            elif poly.geom_type in ("LineString",):
                out.append("M" + "L".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in poly.coords))
            elif poly.geom_type == "MultiLineString":
                for ln in poly.geoms:
                    out.append("M" + "L".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in ln.coords))
        return "".join(out)

    parts = [f'<svg viewBox="0 0 {w} {h}" role="img">']
    pp = P[P.intersects(bb)]
    for r in pp.itertuples():
        g = r.geometry.intersection(bb)
        cls = "hp" if getattr(r, pid) in hl_parcels else ("row" if getattr(r, "_nontax", False) else "p")
        parts.append(f'<path class="{cls}" d="{path(g)}"/>')
    rr = R[R.intersects(bb)]
    for r in rr.itertuples():
        g = r.geometry.intersection(bb)
        cls = "hr" if str(getattr(r, rid)) in hl_roads else "r"
        parts.append(f'<path class="{cls}" d="{path(g)}"/>')
    for r in rr.itertuples():
        if str(getattr(r, rid)) in hl_roads:
            m = r.geometry.intersection(bb)
            m = m.interpolate(0.5, normalized=True) if not m.is_empty else None
            if m is not None:
                parts.append(f'<text class="rl" x="{sx(m.x):.1f}" y="{sy(m.y) - 8:.1f}">{getattr(r, rid)}</text>')
    ap = A[A.intersects(bb)]
    for r in ap.itertuples():
        hl = getattr(r, aid) in hl_points
        parts.append(f'<circle class="{"ha" if hl else "a"}" cx="{sx(r.geometry.x):.1f}" cy="{sy(r.geometry.y):.1f}" r="{5 if hl else 2.4}"/>')
    if mark is not None:
        parts.append(f'<circle class="mk" cx="{sx(mark.x):.1f}" cy="{sy(mark.y):.1f}" r="14"/>')
    # scale bar: 50 m
    px = 50 / (x1 - x0) * w
    parts.append(f'<g class="sb"><path d="M12,{h - 14}h{px:.1f}"/><text x="12" y="{h - 20}">50 m</text></g>')
    parts.append("</svg>")
    return "".join(parts)


# mark non-tax polygons for drawing
nt = [c for c in cfg["parcel_fields"].get("nontax_when_blank", []) if c in P.columns]
P["_nontax"] = True
for c in nt:
    P["_nontax"] &= P[c].isna() | (P[c].astype(str).str.strip() == "")

Ew = E.copy()
examples = []

def pick(check, pattern=None, sort=None):
    x = Ew[Ew.check == check]
    if pattern:
        x = x[x.detail.str.contains(pattern, regex=True)]
    if sort == "area":
        x = x.assign(_a=x.detail.str.extract(r"by ([\d,]+) m²")[0].str.replace(",", "").astype(float)).sort_values("_a", ascending=False)
    return x.iloc[0] if len(x) else None

e = pick("P01", "almost entirely", "area")
if e is not None:
    ids = e.feature_id.split(" / ")
    g = P[P[pid].isin(ids)]
    c = g.geometry.union_all().centroid
    rad = max(60, (g.total_bounds[3] - g.total_bounds[1]) * 0.65)
    examples.append(dict(check="P01", title="A survey lot never cut out of its parent", detail=e.detail,
                         note="One parcel lies almost entirely inside a larger one. This often means a Certified Survey Map lot was mapped, but the parent parcel was not edited to remove it, so the same land is counted twice.",
                         svg=svg_close(c, rad, hl_parcels=ids)))
e = Ew[(Ew.check == "A06") & Ew.detail.str.contains("nearby segment")]
e = e.assign(_d=e.detail.str.extract(r"\(([\d,]+) m away")[0].str.replace(",", "").astype(float))
e = e[(e._d > 25) & (e._d < 120)].sort_values("_d")
e = e.iloc[len(e) // 2] if len(e) else None
if e is not None:
    m = re.search(r"segment (RD-\d+)", e.detail)
    pt = A[A[aid] == e.feature_id].geometry.iloc[0]
    link = A[A[aid] == e.feature_id][cfg["address_fields"]["road_id"]].iloc[0]
    examples.append(dict(check="A06", title="An address linked to the wrong road segment", detail=e.detail,
                         note=f"The point is linked to {link}, but its house number belongs to the next segment. Geocoding and 911 call routing use these links and ranges.",
                         svg=svg_close(pt, 90, hl_roads=[str(link), m.group(1) if m else ""], hl_points=[e.feature_id])))
e = pick("A05", "Fond")
if e is None:
    e = pick("A05")
if e is not None:
    pt = A[A[aid] == e.feature_id].geometry.iloc[0]
    link = A[A[aid] == e.feature_id][cfg["address_fields"]["road_id"]].iloc[0]
    examples.append(dict(check="A05", title="Two spellings of one street", detail=e.detail,
                         note="The address point and its road centerline spell the street differently. NG911 validation requires an exact match.",
                         svg=svg_close(pt, 80, hl_roads=[str(link)], hl_points=[e.feature_id])))
# choose a long, thin gap (the classic digitizing gap), not a building-shaped hole
from shapely.geometry import Polygon as _Poly
fab = P.geometry.union_all()
holes = [(_Poly(r)) for poly in getattr(fab, "geoms", [fab]) for r in poly.interiors]
holes = [h for h in holes if 20 <= h.area <= 500]
holes.sort(key=lambda h: 2 * h.area / h.length)
e = None
if holes:
    h = holes[len(holes) // 4]
    row = Ew[(Ew.check == "P02")].copy()
    row["_d"] = row.geometry.distance(h.representative_point())
    e = row.sort_values("_d").iloc[0]
if e is not None:
    examples.append(dict(check="P02", title="A gap no one owns", detail=e.detail,
                         note="A small hole between parcels that is not road right-of-way. Either a boundary was digitized short or a remnant strip was never mapped.",
                         svg=svg_close(e.geometry, 45, mark=e.geometry)))
json.dump(examples, open(os.path.join(WEB, "examples.json"), "w"), indent=1)
print("findings", len(feats), "examples", [x["check"] for x in examples])
