"""Build the MKE Airport homepage card: a radar scope over the airport's footprints.

Reads the OpenStreetMap extract and the Survey123 inspection export from the project folder
(Claude outputs\\MKE Airport GIS\\data) and writes media/mke-airport-card/card.svg, then swaps it
into index.html between the radar-card markers. The sweep turns about the control tower; each
sample inspection point flashes as the sweep passes and then fades. Animation is CSS only.

Usage: python build_card.py <folder with kmke_osm.json and inspections.csv> [repo root]
"""
import csv, json, math, re, sys
src = sys.argv[1]; root = sys.argv[2] if len(sys.argv) > 2 else "../.."
els = json.load(open(f"{src}/kmke_osm.json", encoding="utf-8"))["elements"]
W, H, PAD, T = 1000, 600, 34, 5.0          # canvas, padding, seconds per sweep
PARK = 150                                  # bearing where the sweep rests before it is played, so the blips east of the tower are lit

def rings(e):
    if e["type"] == "way": return [e.get("geometry", [])]
    if e["type"] == "relation": return [m["geometry"] for m in e["members"] if m.get("role") == "outer" and m.get("geometry")]
    return []
feat = {"runway": [], "closed": [], "taxiway": [], "apron": [], "building": []}
tower = None
for e in els:
    t = e.get("tags", {}); a = t.get("aeroway")
    for g in rings(e):
        if len(g) < 2: continue
        if a == "runway" and t.get("runway") != "displaced_threshold":
            closed = t.get("ref") == "01R/19L"          # corrected status: permanently closed
            feat["closed" if closed else "runway"].append((g, float(t.get("width", 45))))
        elif a == "taxiway": feat["taxiway"].append(g)
        elif a == "apron": feat["apron"].append(g)
        elif "building" in t or a in ("terminal", "hangar", "tower"):
            feat["building"].append(g)
            if a == "tower": tower = (sum(p["lat"] for p in g) / len(g), sum(p["lon"] for p in g) / len(g))
pts = [p for k in ("runway", "closed") for g, _ in feat[k] for p in g] + [p for k in ("taxiway", "building") for g in feat[k] for p in g]
lat0 = sum(p["lat"] for p in pts) / len(pts); kx = math.cos(math.radians(lat0))
xs = [p["lon"] * kx for p in pts]; ys = [p["lat"] for p in pts]
s = min((W - 2 * PAD) / (max(xs) - min(xs)), (H - 2 * PAD) / (max(ys) - min(ys)))
ox = (W - s * (max(xs) - min(xs))) / 2 - s * min(xs); oy = (H + s * (max(ys) - min(ys))) / 2 + s * min(ys)
P = lambda lat, lon: (ox + s * lon * kx, oy - s * lat)
m_per_px = 111320 / s
def d(g, close=False, nd=0):
    out = []; last = None
    for p in g:
        x, y = P(p["lat"], p["lon"]); q = (round(x, nd), round(y, nd))
        if q != last: out.append(q); last = q
    if len(out) < (3 if close else 2): return ""           # smaller than a pixel at this scale
    return "M" + "L".join(f"{x:g},{y:g}" for x, y in out) + ("Z" if close else "")
tx, ty = P(*tower)
R = max(math.hypot(cx - tx, cy - ty) for cx in (0, W) for cy in (0, H)) + 10

o = [f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">',
     f'<rect class="rc-bg" width="{W}" height="{H}"/>', '<g class="rc-grid">']
km = 1000 / m_per_px
for i in range(1, int(R / (km / 2)) + 1): o.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="{i * km / 2:.1f}"/>')
for a in range(0, 180, 30):
    dx, dy = R * math.sin(math.radians(a)), -R * math.cos(math.radians(a))
    o.append(f'<path d="M{tx - dx:.1f},{ty - dy:.1f}L{tx + dx:.1f},{ty + dy:.1f}"/>')
o.append('</g>')
o.append('<path class="rc-apron" d="' + "".join(d(g, True) for g in feat["apron"]) + '"/>')
o.append('<path class="rc-taxi" d="' + "".join(d(g) for g in feat["taxiway"]) + '"/>')
for k in ("closed", "runway"):
    for g, w in feat[k]: o.append(f'<path class="rc-rwy{" rc-shut" if k == "closed" else ""}" stroke-width="{max(4, w / m_per_px):.1f}" d="{d(g, nd=1)}"/>')
o.append('<path class="rc-bld" d="' + "".join(d(g, True) for g in feat["building"]) + '"/>')
# sweep: a fading wedge trailing a bright leading edge, drawn pointing north around 0,0
o.append(f'<g transform="translate({tx:.1f},{ty:.1f})"><g class="rc-sweep">')
STEP, N = 4, 14
for i in range(N):
    a0, a1 = math.radians(-(i + 1) * STEP), math.radians(-i * STEP)
    o.append(f'<path d="M0,0L{R * math.sin(a0):.1f},{-R * math.cos(a0):.1f}A{R:.1f},{R:.1f} 0 0 1 {R * math.sin(a1):.1f},{-R * math.cos(a1):.1f}Z" opacity="{0.30 * (1 - i / N) ** 1.6:.3f}"/>')
o.append(f'<path class="rc-edge" d="M0,0L0,{-R:.1f}"/></g></g>')
o.append(f'<circle class="rc-tower" cx="{tx:.1f}" cy="{ty:.1f}" r="3.2"/>')
n = 0
for r in csv.DictReader(open(f"{src}/inspections.csv", encoding="utf-8-sig")):
    x, y = P(float(r["y"]), float(r["x"])); n += 1
    bearing = math.degrees(math.atan2(x - tx, -(y - ty))) % 360
    delay = (bearing - PARK) / 360 * T - T
    o.append(f'<g class="rc-blip" style="animation-delay:{delay:.2f}s"><circle cx="{x:.1f}" cy="{y:.1f}" r="11"/><circle cx="{x:.1f}" cy="{y:.1f}" r="4.2"/></g>')
o.append('</svg>')
svg = "\n".join(o)
open(f"{root}/media/mke-airport-card/card.svg", "w", encoding="utf-8").write(svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1))
fig = (f'<figure class="radar-card" id="rcard" style="--rc-t:{T:g}s;--rc-park:{-PARK / 360 * T:.2f}s" aria-label="Radar-style map of Milwaukee Mitchell International Airport: runways, taxiways and buildings in green, with a sweep turning around the control tower. {n} sample inspection points flash red as the sweep passes, then fade.">\n'
       + svg + f'\n<span class="label rc-label" aria-hidden="true">KMKE · {n} sample inspections</span>\n</figure>')
p = f"{root}/index.html"; h = open(p, encoding="utf-8").read()
a, b = "<!-- radar-card:start -->", "<!-- radar-card:end -->"
assert h.count(a) == 1 and h.count(b) == 1
h = h[: h.index(a) + len(a)] + "\n" + fig + "\n" + h[h.index(b):]
open(p, "w", encoding="utf-8").write(h)
print(f"ok: {n} blips, tower at {tx:.0f},{ty:.0f}, {m_per_px:.1f} m/px, svg {len(svg) / 1024:.0f} KB")
