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


def callout(text, pt, below=False, left=False):
    x, y = sx(pt.x), sy(pt.y)
    ty = y + 42 if below else y - 26
    anchor = "end" if left else "start"
    tx = x - 14 if left else x + 14
    return (f'<path class="co-line" d="M{x:.1f},{y:.1f}L{tx:.1f},{ty - 6:.1f}"/>'
            f'<text class="co" x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}">{text.upper()}</text>')
pid = "PARCELID"
# P01 nested parcels
for r in E[E.check == "P01"].itertuples():
    ids = r.feature_id.split(" / ")
    g = P[P[pid].isin(ids)]
    small = g.loc[g.area.idxmin()].geometry
    x = sx(small.centroid.x)
    co = callout("Nested lot", small.centroid) if not any("NESTED" in t for _, t in finds) else ""
    finds.append((x, f'<g class="f" data-x="{x:.0f}" data-n="1"><path class="hit-fill" d="{d_of(small.intersection(bb))}"/>{co}</g>'))
# P05 slivers (one callout, on the westernmost)
p05x = {r.feature_id: P[P[pid] == r.feature_id].geometry.iloc[0].centroid.x
        for r in E[E.check == "P05"].itertuples() if (P[pid] == r.feature_id).any()}
for r in E[E.check == "P05"].itertuples():
    g = P[P[pid] == r.feature_id]
    if not len(g):
        continue
    geom = g.geometry.iloc[0].intersection(bb)
    x = sx(geom.centroid.x)
    co = callout("Sliver", geom.centroid, below=True) if p05x and r.feature_id == min(p05x, key=p05x.get) else ""
    finds.append((x, f'<g class="f" data-x="{x:.0f}" data-n="1"><path class="hit-line" d="{d_of(geom.boundary)}"/>{co}</g>'))
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
    parts.append(callout("Wrong road link", p, below=True, left=True))
    x = sx(p.x)
    finds.append((x, f'<g class="f" data-x="{x:.0f}" data-n="1">{"".join(parts)}</g>'))
# A05 street name mismatch: ring each point, plus a label along the road that flips between spellings
a05 = E[E.check == "A05"]
if len(a05):
    pts = A[A.siteaddid.isin(a05.feature_id)]
    for p in pts.geometry:
        x = sx(p.x)
        finds.append((x, f'<g class="f" data-x="{x:.0f}" data-n="1"><circle class="hit-ring" cx="{x:.1f}" cy="{sy(p.y):.1f}" r="9"/></g>'))
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

# ---- COGO traverse of one parcel (stand-in: courses computed from the county's parcel geometry,
# to be replaced by James's own COGO draft). Bearings and distances in WISCRS Sheboygan (ftUS).
TRAV_PID = "59282903950"
N = gpd.read_file("raw/parcels.gpkg")              # native EPSG:8158, US survey feet
tg = N[N[pid] == TRAV_PID].geometry.iloc[0]
tg = tg.geoms[0] if tg.geom_type == "MultiPolygon" else tg
ring = list(tg.simplify(0.5).exterior.coords)
to3071 = gpd.GeoSeries(gpd.points_from_xy([c[0] for c in ring], [c[1] for c in ring]), crs=N.crs).to_crs(3071)
pts = [(sx(p.x), sy(p.y)) for p in to3071]


def qbearing(az):
    az %= 360
    if az <= 90: ns, ew, a = "N", "E", az
    elif az <= 180: ns, ew, a = "S", "E", 180 - az
    elif az <= 270: ns, ew, a = "S", "W", az - 180
    else: ns, ew, a = "N", "W", 360 - az
    t = round(a * 3600)
    return f"{ns} {t // 3600}°{t % 3600 // 60:02d}′{t % 60:02d}″ {ew}", t / 3600 * (1 if (ns, ew) in (("N", "E"), ("S", "W")) else -1)


courses, ex, ey, perim = [], 0.0, 0.0, 0.0
for i, ((x1, y1), (x2, y2)) in enumerate(zip(ring, ring[1:])):
    az = math.degrees(math.atan2(x2 - x1, y2 - y1)) % 360
    dist = round(math.hypot(x2 - x1, y2 - y1), 2)
    text, _ = qbearing(az)
    t = round((az % 90 if True else az) * 3600)      # rounded azimuth to the second, for closure
    azr = math.radians(round(az * 3600) / 3600)
    ex += dist * math.sin(azr); ey += dist * math.cos(azr); perim += dist
    courses.append((text, dist))
mis = math.hypot(ex, ey)
closure = (f"misclosure {mis:.2f} ft · 1:{round(perim / mis, -2):,.0f}" if mis >= 0.005
           else "misclosure under 0.01 ft")

tr = []
for i, ((text, dist), (a, b)) in enumerate(zip(courses, zip(pts, pts[1:]))):
    (x1, y1), (x2, y2) = a, b
    L = math.hypot(x2 - x1, y2 - y1)
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    flip = ang > 90 or ang < -90
    rot = ang + 180 if flip else ang
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    # put the label outside the parcel: offset to the left of travel for a clockwise ring
    cxp = sum(p[0] for p in pts[:-1]) / (len(pts) - 1); cyp = sum(p[1] for p in pts[:-1]) / (len(pts) - 1)
    nx, ny = -(y2 - y1) / L, (x2 - x1) / L
    if (mx + nx - cxp) ** 2 + (my + ny - cyp) ** 2 < (mx - cxp) ** 2 + (my - cyp) ** 2:
        nx, ny = -nx, -ny
    off = 9
    lx, ly = mx + nx * off, my + ny * off
    tr.append(f'<g class="tc" data-call="Thence {text}, {dist:.2f} ft" data-dist="{dist:.2f}">'
              f'<path d="M{x1:.2f},{y1:.2f}L{x2:.2f},{y2:.2f}" pathLength="1"/>' +
              (f'<text transform="translate({lx:.2f},{ly:.2f}) rotate({rot:.1f})" dy="0.35em">{text}</text>' if L > 80 else "") +
              f'<text class="dt" transform="translate({mx - nx * off:.2f},{my - ny * off:.2f}) rotate({rot:.1f})" dy="0.35em"><tspan class="dd">{dist:.2f}</tspan> ft</text></g>')
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
zw = max(max(xs) - min(xs), (max(ys) - min(ys)) * 5 / 3) * 1.55
zcx, zcy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
zoom = f"{zcx - zw / 2:.1f} {zcy - zw * 0.285:.1f} {zw:.1f} {zw * 0.6:.1f}"   # sits a little high, clear of the caption bar
poly = "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z"
trav = (f'<g class="trav" data-zoom="{zoom}" data-close="Closes on the point of beginning · {closure}">'
        f'<path class="tfill" d="{poly}"/>{"".join(tr)}'
        f'<circle class="pob" cx="{pts[0][0]:.2f}" cy="{pts[0][1]:.2f}" r="3"/>'
        f'<text class="pobt" x="{pts[0][0]:.2f}" y="{pts[0][1]:.2f}" dx="6" dy="-6">POB</text>'
        f'<g class="narrow"><path d="M0,-14L4,0L0,-3L-4,0Z"/><text y="-17" text-anchor="middle">N</text></g></g>')
print("traverse", courses, closure, "zoom", zoom)
svg = (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-hidden="true">'
       f'<path class="pl" d="{parcel_d}"/><path class="rd" d="{road_d}"/><g class="ad">{dots}</g>'
       f'<g class="finds">{"".join(s for _, s in finds)}</g>{trav}'
       f'<g class="scan"><rect class="band" x="-60" y="0" width="60" height="{H}"/><line class="beam" x1="0" y1="0" x2="0" y2="{H}"/></g>'
       f'</svg>')
open(OUT, "w").write(svg)
print("bytes", len(svg), "findings", len(finds), {c: int((E.check == c).sum()) for c in E.check.unique()})
