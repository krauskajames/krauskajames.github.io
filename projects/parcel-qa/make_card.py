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

# ---- Sheboygan County, drawn like a traverse: the county line course by course (bearings and
# distances in WISCRS Sheboygan ftUS), the Lake Michigan shore as one meander call, then the town
# and municipal lines, then a zoom down to this block for the QA sweep.
from shapely.geometry import Polygon, Point as SPoint
from shapely.ops import unary_union, substring
from shapely.geometry import LineString as SLine
Mu = gpd.read_file("raw/municipalities.gpkg")            # EPSG:8158, US survey feet
cty = unary_union(Mu.geometry).buffer(50).buffer(-50)
cty = Polygon(max(getattr(cty, "geoms", [cty]), key=lambda p: p.area).exterior)
if cty.exterior.is_ccw:
    cty = Polygon(list(cty.exterior.coords)[::-1])          # clockwise, like a traverse

def to_svg(geom):
    g3071 = gpd.GeoSeries([geom], crs=Mu.crs).to_crs(3071).iloc[0]
    return g3071

def qbearing(az):
    az %= 360
    if az <= 90: ns, ew, a = "N", "E", az
    elif az <= 180: ns, ew, a = "S", "E", 180 - az
    elif az <= 270: ns, ew, a = "S", "W", az - 180
    else: ns, ew, a = "N", "W", 360 - az
    t = round(a * 60)
    return f"{ns} {t // 60}°{t % 60:02d}′ {ew}"

simple = cty.simplify(3000)
sc = list(simple.exterior.coords)[:-1]
# corners: SW = min(x+y), NW = min(x-y), NE = max(x+y), SE = max(x-y)
SWc = min(sc, key=lambda c: c[0] + c[1]); NWc = min(sc, key=lambda c: c[0] - c[1])
NEc = max(sc, key=lambda c: c[0] + c[1]); SEc = max(sc, key=lambda c: c[0] - c[1])
def nearest_idx(ring, c):
    return min(range(len(ring)), key=lambda i: (ring[i][0] - c[0]) ** 2 + (ring[i][1] - c[1]) ** 2)
full = list(cty.simplify(350).exterior.coords)[:-1]
i_sw, i_nw, i_ne, i_se = (nearest_idx(full, c) for c in (SWc, NWc, NEc, SEc))
def ring_slice(i, j):
    return full[i:j + 1] if j >= i else full[i:] + full[:j + 1]
legs = []                                                  # (call text, coords in 8158)
for a_, b_, label in ((i_sw, i_nw, None), (i_nw, i_ne, None)):
    seg = ring_slice(a_, b_)
    p, q = seg[0], seg[-1]
    az = math.degrees(math.atan2(q[0] - p[0], q[1] - p[1])); dist = math.hypot(q[0] - p[0], q[1] - p[1])
    legs.append((f"Thence {qbearing(az)}, {dist:,.0f} ft ({dist / 5280:.1f} mi)", seg))
shore = ring_slice(i_ne, i_se)
shore_len = SLine(shore).length
legs.append((f"Thence along the shore of Lake Michigan, about {shore_len / 5280:.0f} mi", shore))
seg = ring_slice(i_se, i_sw)
p, q = seg[0], seg[-1]
az = math.degrees(math.atan2(q[0] - p[0], q[1] - p[1])); dist = math.hypot(q[0] - p[0], q[1] - p[1])
legs.append((f"Thence {qbearing(az)}, {dist:,.0f} ft ({dist / 5280:.1f} mi), to the point of beginning", seg))

def rel(pts):
    pts = [(round(sx(x)), round(sy(y))) for x, y in pts]
    out = f"M{pts[0][0]},{pts[0][1]}l"; px, py = pts[0]; parts = []
    for x, y in pts[1:]:
        if (x, y) != (px, py): parts.append(f"{x - px},{y - py}"); px, py = x, y
    return out + " ".join(parts)
def leg_d(coords):
    ls = to_svg(SLine(coords))
    return rel(list(ls.coords))
legs_svg = "".join(f'<path class="leg" pathLength="1" data-call="{c}" d="{leg_d(co)}"/>' for c, co in legs)

# municipal lines inside the county (towns, cities, villages), drawn after the outline closes
Md = Mu.dissolve(by="name").reset_index()
from shapely.ops import linemerge
inner = unary_union([g.simplify(300).boundary for g in Md.geometry]).difference(cty.exterior.buffer(600))
inner = linemerge(inner) if inner.geom_type == "MultiLineString" else inner
inner = unary_union([l.simplify(500) for l in getattr(inner, "geoms", [inner]) if l.length > 2500])
inner3071 = to_svg(inner)
def lines_d(geom):
    out = []
    for g in getattr(geom, "geoms", [geom]):
        if g.geom_type == "LineString" and g.length > 0:
            out.append(rel(list(g.coords)))
    return "".join(out)
inner_d = lines_d(inner3071)
towns = Md[Md.munitype == "Township"]
labels = []
for r in towns.itertuples():
    b = r.geometry.bounds; pt = to_svg(SPoint((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
    labels.append(f'<text x="{sx(pt.x):.0f}" y="{sy(pt.y):.0f}">{r.name.replace("Town of ", "").upper().replace("SHEBOYGAN FALLS", "SHEB. FALLS")}</text>')
pob = to_svg(SPoint(full[i_sw]))
cb = to_svg(cty).bounds
cw = (cb[2] - cb[0]) / WM * W; chh = (cb[3] - cb[1]) / HM * H
vw = max(cw * 1.2, chh * 1.5 * 5 / 3); vh = vw * 0.6
ccx, ccy = sx((cb[0] + cb[2]) / 2), sy((cb[1] + cb[3]) / 2)
county_vb = f"{ccx - vw / 2:.0f} {ccy - vh * 0.54:.0f} {vw:.0f} {vh:.0f}"
here = to_svg(SPoint(0, 0)) if False else None
blk = (500, 300)                                            # this block's center in card units
trav = (f'<g class="cty" data-county="{county_vb}">'
        f'<path class="cfill" d="{leg_d(full + [full[0]])}Z"/>'
        f'<path class="munis" pathLength="1" d="{inner_d}"/>'
        f'<g class="tlab" font-size="{vw / 66:.0f}">{"".join(labels)}</g>'
        f'{legs_svg}'
        f'<circle class="pob" cx="{sx(pob.x):.0f}" cy="{sy(pob.y):.0f}" r="{vw / 160:.0f}"/>'
        f'<rect class="here" x="{blk[0] - vw / 70:.0f}" y="{blk[1] - vw / 70:.0f}" width="{vw / 35:.0f}" height="{vw / 35:.0f}"/>'
        f'</g>')
print("county legs", [c for c, _ in legs], "view", county_vb)
svg = (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-hidden="true">'
       f'<path class="pl" d="{parcel_d}"/><path class="rd" d="{road_d}"/><g class="ad">{dots}</g>'
       f'<g class="finds">{"".join(s for _, s in finds)}</g>{trav}'
       f'<g class="scan"><rect class="band" x="-60" y="0" width="60" height="{H}"/><line class="beam" x1="0" y1="0" x2="0" y2="{H}"/></g>'
       f'</svg>')
open(OUT, "w").write(svg)
print("bytes", len(svg), "findings", len(finds), {c: int((E.check == c).sum()) for c in E.check.unique()})
