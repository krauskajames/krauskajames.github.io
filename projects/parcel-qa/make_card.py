"""Homepage card for the Parcel QA project, drawn as an SVG (animation: media/parcel-qa-card/sweep.js).

The card follows the project page in four beats, on a real block of the Village of Cascade:
  1. start at the point of commencement,
  2. draft James's Parcel 3 (59111521840) from its recorded description, course by course,
     with a magnifier on the 6.55 ft jog,
  3. lay the county's tax parcel over it, with the corner offsets James measured in ArcGIS Pro,
  4. zoom out and sweep the block with the QA checks.

    python3 make_card.py ../../media/parcel-qa-card/card.svg      (run where raw/ and out/ are)
"""
import math, re, sys
import geopandas as gpd
from shapely.geometry import box, Point
from shapely.ops import nearest_points

OUT = sys.argv[1]
PID = "59111521840"
CX, CY = 680701.9, 356400.3                       # Parcel 3, EPSG:3071 meters
X0, Y0, WM, HM = CX - 650, CY - 705, 1300, 780    # card window (5:3), parcel near the top, findings below
W, H = 1000, 600
sx = lambda x: (x - X0) / WM * W
sy = lambda y: H - (y - Y0) / HM * H
bb = box(X0, Y0, X0 + WM, Y0 + HM)

N = gpd.read_file("raw/parcels.gpkg")             # native EPSG:8158, US survey feet
P = N.to_crs(3071)
R = gpd.read_file("raw/roads.gpkg").to_crs(3071)
A = gpd.read_file("raw/addresses.gpkg").to_crs(3071)
E = gpd.read_file("out/qa_findings.gpkg")
P = P[P.intersects(bb)]; R = R[R.intersects(bb)]; A = A[A.intersects(bb)]
E = E[E.intersects(bb.buffer(-15)) & (E.check != "P04")]


def d_of(geom, f=None):
    f = f or (lambda x, y: (sx(x), sy(y)))
    out = []
    for g in getattr(geom, "geoms", [geom]):
        if g.is_empty:
            continue
        if g.geom_type == "Polygon":
            for ring in [g.exterior] + list(g.interiors):
                out.append("M" + "L".join("%.1f,%.1f" % f(x, y) for x, y in ring.coords) + "Z")
        elif g.geom_type == "LineString":
            out.append("M" + "L".join("%.1f,%.1f" % f(x, y) for x, y in g.coords))
        else:
            out.append(d_of(g, f))
    return "".join(out)


parcel_d = "".join(d_of(g.simplify(0.15).boundary.intersection(bb)) for g in P.geometry)
road_d = "".join(d_of(g.intersection(bb)) for g in R.geometry)
dots = "".join(f'<circle cx="{sx(p.x):.1f}" cy="{sy(p.y):.1f}" r="2.2"/>' for p in A.geometry)


def callout(text, pt, below=False, left=False):
    x, y = sx(pt.x), sy(pt.y)
    ty = y + 46 if below else y - 28
    anchor = "end" if left else "start"
    tx = x - 16 if left else x + 16
    return (f'<path class="co-line" d="M{x:.1f},{y:.1f}L{tx:.1f},{ty - 6:.1f}"/>'
            f'<text class="co" x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}">{text.upper()}</text>')


finds = []
said = set()
for r in E.itertuples():
    p = r.geometry
    x = sx(p.x)
    parts = []
    if r.check == "A06":
        pt = A[A.siteaddid == r.feature_id]
        m = re.search(r"segment (RD-\d+)", r.detail)
        if len(pt):
            seg_bad = R[R.centerlineid == pt.RdCLID.iloc[0]]
            if len(seg_bad):
                a = nearest_points(p, seg_bad.geometry.iloc[0])[1]
                parts.append(f'<path class="hit-link bad" d="M{sx(p.x):.1f},{sy(p.y):.1f}L{sx(a.x):.1f},{sy(a.y):.1f}"/>')
            if m and (R.centerlineid == m.group(1)).any():
                b = nearest_points(p, R[R.centerlineid == m.group(1)].geometry.iloc[0])[1]
                parts.append(f'<path class="hit-link ok" d="M{sx(p.x):.1f},{sy(p.y):.1f}L{sx(b.x):.1f},{sy(b.y):.1f}"/>')
        parts.append(f'<circle class="hit-dot" cx="{x:.1f}" cy="{sy(p.y):.1f}" r="8"/>')
        label = "Number outside road range"
    elif r.check == "P02":
        parts.append(f'<circle class="hit-ring" cx="{x:.1f}" cy="{sy(p.y):.1f}" r="13"/>')
        label = "Gap between parcels"
    elif r.check == "A03":
        parts.append(f'<circle class="hit-ring" cx="{x:.1f}" cy="{sy(p.y):.1f}" r="10"/>')
        label = "Outside every parcel"
    else:
        parts.append(f'<circle class="hit-ring" cx="{x:.1f}" cy="{sy(p.y):.1f}" r="10"/>')
        label = r.title
    place = {"A06": dict(below=False, left=True), "P02": dict(below=False, left=False),
             "A03": dict(below=False, left=True)}.get(r.check, {})
    if label not in said and not (r.check == "A03" and r.feature_id == "SID-45141") \
            and not (r.check == "P02" and sx(p.x) < 500):
        said.add(label)
        parts.append(callout(label, p, **place))
    finds.append((x, f'<g class="f" data-x="{x:.0f}" data-n="1">{"".join(parts)}</g>'))
finds.sort(key=lambda t: t[0])

# ---- James's COGO draft of Parcel 3 from the recorded description, starting at the county's NE corner
# (where he snapped the point of commencement). Bearings and distances are WISCRS Sheboygan grid, US feet.
COURSES = [("S", 89, 8, 58, "W", 835.44), ("S", 28, 53, 33, "E", 478.49), ("N", 62, 4, 46, "E", 6.55),
           ("N", 28, 13, 0, "W", 129.48), ("N", 80, 15, 0, "E", 670.59), ("N", 0, 22, 33, "W", 200.61)]
g = N[N.PARCELID == PID].geometry.iloc[0]
g = g.geoms[0] if g.geom_type == "MultiPolygon" else g
ne = max(g.exterior.coords, key=lambda c: c[0] + c[1])
x, y = ne
ft = [(x, y)]
for ns, d, m, s, ew, L in COURSES:
    a = math.radians(d + m / 60 + s / 3600)
    x += L * math.sin(a) * (1 if ew == "E" else -1); y += L * math.cos(a) * (1 if ns == "N" else -1)
    ft.append((x, y))
mis_ft = math.hypot(ft[-1][0] - ne[0], ft[-1][1] - ne[1])
wtm = gpd.GeoSeries(gpd.points_from_xy(*zip(*ft)), crs=N.crs).to_crs(3071)
pts = [(sx(p.x), sy(p.y)) for p in wtm]
pts[-1] = pts[0]
county = P[P.PARCELID == PID].geometry.iloc[0]

call = lambda c: f"{c[0]} {c[1]}°{c[2]:02d}′{c[3]:02d}″ {c[4]}"
tr = []
cxp = sum(p[0] for p in pts[:-1]) / 6; cyp = sum(p[1] for p in pts[:-1]) / 6
for i, (c, (a, b)) in enumerate(zip(COURSES, zip(pts, pts[1:]))):
    (x1, y1), (x2, y2) = a, b
    L = math.hypot(x2 - x1, y2 - y1)
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    rot = ang + 180 if (ang > 90 or ang < -90) else ang
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    nx, ny = -(y2 - y1) / L, (x2 - x1) / L
    if (mx + nx - cxp) ** 2 + (my + ny - cyp) ** 2 < (mx - cxp) ** 2 + (my - cyp) ** 2:
        nx, ny = -nx, -ny
    off = 8
    lab = (f'<text transform="translate({mx + nx * off:.2f},{my + ny * off:.2f}) rotate({rot:.1f})" dy="0.35em">{call(c)}</text>'
           f'<text class="dt" transform="translate({mx - nx * off:.2f},{my - ny * off:.2f}) rotate({rot:.1f})" dy="0.35em"><tspan class="dd">{c[5]:.2f}</tspan> ft</text>'
           if L > 60 else '')
    tr.append(f'<g class="tc" data-i="{i}" data-call="Thence {call(c)}, {c[5]:.2f} ft" data-dist="{c[5]:.2f}"'
              + (' data-loupe="1"' if i == 2 else '') + '>'
              f'<path d="M{x1:.2f},{y1:.2f}L{x2:.2f},{y2:.2f}" pathLength="1"/>{lab}</g>')

xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
zw = max(max(xs) - min(xs), (max(ys) - min(ys)) * 5 / 3) * 1.6
zcx, zcy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
zx, zy, zh = zcx - zw / 2, zcy - zw * 0.27, zw * 0.6
zoom = f"{zx:.1f} {zy:.1f} {zw:.1f} {zh:.1f}"
poly = "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z"

# county outline and the corner offsets James measured (Nov 5, ArcGIS Pro 3.7.3)
cty_d = d_of(county.boundary)
tags = []
for idx, text, dx, dy in [(1, "4.0 ft", -6, -10), (4, "3.5 ft", -10, 14), (5, "1.0 ft", 10, 14)]:
    px, py = pts[idx]
    anchor = "end" if dx < 0 else "start"
    tags.append(f'<g class="tag"><circle cx="{px:.2f}" cy="{py:.2f}" r="2.6"/>'
                f'<text x="{px + dx:.2f}" y="{py + dy:.2f}" text-anchor="{anchor}">{text}</text></g>')
cty = f'<g class="cty"><path d="{cty_d}"/>{"".join(tags)}</g>'

# magnifier on the strip's tip (end of course 2): 6.55 ft jog, magnified 14x
tipx, tipy = pts[2]
K = 14
lr = zw * 0.13
lcx, lcy = zx + zw - lr - zw * 0.05, zy + zh - lr - zw * 0.13       # bottom right of the zoomed view, above the caption
mag = lambda x, y: (lcx + (x - tipx) * K, lcy + (y - tipy) * K)
lpaths = []
for i in (1, 2, 3):
    (x1, y1), (x2, y2) = pts[i], pts[i + 1]
    a, b = mag(x1, y1), mag(x2, y2)
    lpaths.append(f'<path class="lp" data-i="{i}" d="M{a[0]:.2f},{a[1]:.2f}L{b[0]:.2f},{b[1]:.2f}" pathLength="1"/>')
cty_loupe = d_of(county.boundary, lambda x, y: mag(sx(x), sy(y)))
jx, jy = mag(*pts[2]); kx, ky = mag(*pts[3])
loupe = (f'<g class="loupe"><clipPath id="pq-lclip"><circle cx="{lcx:.2f}" cy="{lcy:.2f}" r="{lr:.2f}"/></clipPath>'
         f'<circle class="lbg" cx="{lcx:.2f}" cy="{lcy:.2f}" r="{lr:.2f}"/>'
         f'<g clip-path="url(#pq-lclip)"><path class="lcty" d="{cty_loupe}"/>{"".join(lpaths)}</g>'
         f'<circle class="lrim" cx="{lcx:.2f}" cy="{lcy:.2f}" r="{lr:.2f}"/>'
         f'<text class="ltx" x="{(jx + kx) / 2:.2f}" y="{(jy + ky) / 2 + 14:.2f}" text-anchor="middle">6.55 ft</text>'
         f'<text class="ltx sm" x="{lcx:.2f}" y="{lcy + lr + 11:.2f}" text-anchor="middle">×{K}</text></g>')

closure = f"Closes on the point of beginning · misclosure {mis_ft:.2f} ft"
trav = (f'<g class="trav" data-zoom="{zoom}" data-close="{closure}" '
        f'data-compare="Laid over the county\'s tax parcel: within 4 ft of the record at every corner">'
        f'<path class="tfill" d="{poly}"/>{cty}{"".join(tr)}'
        f'<circle class="pob" cx="{pts[0][0]:.2f}" cy="{pts[0][1]:.2f}" r="3"/>'
        f'<text class="pobt" x="{pts[0][0]:.2f}" y="{pts[0][1]:.2f}" dx="6" dy="-6">POC · POB</text>'
        f'<g class="narrow"><path d="M0,-14L4,0L0,-3L-4,0Z"/><text y="-17" text-anchor="middle">N</text></g>{loupe}</g>')
svg = (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-hidden="true">'
       f'<path class="pl" d="{parcel_d}"/><path class="rd" d="{road_d}"/><g class="ad">{dots}</g>'
       f'<g class="finds">{"".join(s for _, s in finds)}</g>{trav}'
       f'<g class="scan"><rect class="band" x="-60" y="0" width="60" height="{H}"/><line class="beam" x1="0" y1="0" x2="0" y2="{H}"/></g>'
       f'</svg>')
open(OUT, "w").write(svg)
print("misclosure ft", round(mis_ft, 4), "zoom", zoom, "bytes", len(svg), "findings", len(finds))
