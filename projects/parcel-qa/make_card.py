"""Homepage card for the Parcel QA project: one real Sheboygan block drawn as an SVG with its QA findings,
revealed by a scan line on hover (animation lives in media/parcel-qa-card/sweep.js).

    python3 make_card.py ../../media/parcel-qa-card/card.svg
"""
import json, math, sys
import geopandas as gpd
from shapely.geometry import box, Point
from shapely.ops import nearest_points

OUT = sys.argv[1]
X0, Y0, WM, HM = 696812, 364494, 550, 330      # window in WTM meters (5:3)
W, H = 1000, 600
sx = lambda x: (x - X0) / WM * W
sy = lambda y: H - (y - Y0) / HM * H
bb = box(X0, Y0, X0 + WM, Y0 + HM)

P = gpd.read_file("raw/parcels.gpkg").to_crs(3071)
R = gpd.read_file("raw/roads.gpkg").to_crs(3071)
A = gpd.read_file("raw/addresses.gpkg").to_crs(3071)
E = gpd.read_file("out/qa_findings.gpkg")
P = P[P.intersects(bb)]
R = R[R.intersects(bb)]
A = A[A.intersects(bb)]
E = E[E.intersects(bb.buffer(-10)) & (E.check != "P04")]


def d_of(geom):
    out = []
    for g in getattr(geom, "geoms", [geom]):
        if g.is_empty:
            continue
        if g.geom_type == "Polygon":
            for ring in [g.exterior] + list(g.interiors):
                out.append("M" + "L".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in ring.coords) + "Z")
        elif g.geom_type == "LineString":
            out.append("M" + "L".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in g.coords))
        elif g.geom_type in ("MultiLineString", "GeometryCollection", "MultiPolygon"):
            out.append(d_of(g))
    return "".join(out)


parcel_d = "".join(d_of(g.simplify(0.15).boundary.intersection(bb)) for g in P.geometry)
road_d = "".join(d_of(g.intersection(bb)) for g in R.geometry)
dots = "".join(f'<circle cx="{sx(p.x):.1f}" cy="{sy(p.y):.1f}" r="2.2"/>' for p in A.geometry)

finds = []          # (x for reveal timing, svg)
pid = "PARCELID"
# P01 nested parcels
for r in E[E.check == "P01"].itertuples():
    ids = r.feature_id.split(" / ")
    g = P[P[pid].isin(ids)]
    small = g.loc[g.area.idxmin()].geometry
    x = sx(small.centroid.x)
    finds.append((x, f'<g class="f" data-x="{x:.0f}"><path class="hit-fill" d="{d_of(small.intersection(bb))}"/></g>'))
# P05 slivers
for r in E[E.check == "P05"].itertuples():
    g = P[P[pid] == r.feature_id]
    if not len(g):
        continue
    geom = g.geometry.iloc[0].intersection(bb)
    x = sx(geom.centroid.x)
    finds.append((x, f'<g class="f" data-x="{x:.0f}"><path class="hit-line" d="{d_of(geom.boundary)}"/></g>'))
# A06 wrong segment link
for r in E[E.check == "A06"].itertuples():
    pt = A[A.siteaddid == r.feature_id]
    if not len(pt):
        continue
    p = pt.geometry.iloc[0]
    link = pt.RdCLID.iloc[0]
    import re
    m = re.search(r"segment (RD-\d+)", r.detail)
    seg_bad = R[R.centerlineid == link].geometry.iloc[0]
    seg_ok = R[R.centerlineid == m.group(1)].geometry.iloc[0] if m and (R.centerlineid == m.group(1)).any() else None
    a = nearest_points(p, seg_bad)[1]
    parts = [f'<path class="hit-seg" d="{d_of(seg_bad.intersection(bb))}"/>',
             f'<path class="hit-link bad" d="M{sx(p.x):.1f},{sy(p.y):.1f}L{sx(a.x):.1f},{sy(a.y):.1f}"/>']
    if seg_ok is not None:
        b = nearest_points(p, seg_ok)[1]
        parts.append(f'<path class="hit-link ok" d="M{sx(p.x):.1f},{sy(p.y):.1f}L{sx(b.x):.1f},{sy(b.y):.1f}"/>')
    parts.append(f'<circle class="hit-dot" cx="{sx(p.x):.1f}" cy="{sy(p.y):.1f}" r="8"/>')
    x = sx(p.x)
    finds.append((x, f'<g class="f" data-x="{x:.0f}">{"".join(parts)}</g>'))
# A05 street name mismatch: ring each point, plus a label along the road that flips between spellings
a05 = E[E.check == "A05"]
if len(a05):
    pts = A[A.siteaddid.isin(a05.feature_id)]
    for p in pts.geometry:
        x = sx(p.x)
        finds.append((x, f'<g class="f" data-x="{x:.0f}"><circle class="hit-ring" cx="{x:.1f}" cy="{sy(p.y):.1f}" r="9"/></g>'))
    link = pts.RdCLID.iloc[0]
    seg = R[R.centerlineid == link].geometry.iloc[0].intersection(bb)
    seg = max(getattr(seg, "geoms", [seg]), key=lambda s: s.length)
    mid = seg.interpolate(0.5, normalized=True)
    q1, q2 = seg.interpolate(0.45, normalized=True), seg.interpolate(0.55, normalized=True)
    ang = math.degrees(math.atan2(-(sy(q2.y) - sy(q1.y)), sx(q2.x) - sx(q1.x)))
    ang = -ang
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    x, y = sx(mid.x), sy(mid.y)
    finds.append((x, f'<g class="f lbl" data-x="{x:.0f}" transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})">'
                     f'<text class="nm a" y="30">Fond Du Lac Ave</text><text class="nm b" y="30">Fonddulac Ave</text></g>'))

finds.sort(key=lambda t: t[0])
svg = (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-hidden="true">'
       f'<path class="pl" d="{parcel_d}"/><path class="rd" d="{road_d}"/><g class="ad">{dots}</g>'
       f'<g class="finds">{"".join(s for _, s in finds)}</g>'
       f'<g class="scan"><rect class="band" x="-60" y="0" width="60" height="{H}"/><line class="beam" x1="0" y1="0" x2="0" y2="{H}"/></g>'
       f'</svg>')
open(OUT, "w").write(svg)
print("bytes", len(svg), "findings", len(finds), {c: int((E.check == c).sum()) for c in E.check.unique()})
