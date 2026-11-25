"""Build the homepage card for Lake Winnebago from Space: the high-chlorophyll patches of summer 2025, each clear day's shapes changing into the next day's.

The green shapes are where a day's chlorophyll-a estimate was highest (orange to red on the 0-60 mg/m3 scale, about 48 mg/m3 and up),
traced from the frames of media/filmstrip_2025_chlorophyll.gif.
Summer 2025 was chosen because its blooms form separate patches that shift from day to day; 2019 was heavier but fills most of the lake.

How the change between days is drawn: each day's shapes are stored as a small grid of distances to the shape edge (positive inside, negative outside).
The card blends two days' grids and redraws the edge where the blend crosses zero, so patches grow, shrink, join and split.
Only the ten dated shapes are data. The in-between shapes are drawn by the animation, and are not measurements.
The loop ends with all ten days laid over each other, which shows where the chlorophyll sat most often.
The wind vane points the way the wind was blowing, with its speed: the average of the three days up to each image (ERA5-Land), the same wind the page tests.
The speed is that of the averaged wind, so three days of shifting wind read lower than any one of them.

Run from the repository root:  python3 projects/lake-winnebago-blooms/build_card.py
Writes media/lake-winnebago-card/morph.js and card.html (the figure markup for index.html).
"""
import base64, csv, datetime, json, math, os, sys
import cv2, numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "media", "lake-winnebago-card"); os.makedirs(OUT, exist_ok=True)
# Usage: build_card.py [year] [--preview].  With --preview the files are written as morph_<year>.js and card_<year>.html, and the live card is left alone.
SUMMERS = {
    # "fixed": shade where the estimate is about 48 mg/m3 and up (orange to red on the palette).
    2025: dict(mode="fixed", dates=["2025-07-03", "2025-07-13", "2025-07-18", "2025-07-20", "2025-07-21", "2025-07-28", "2025-08-02", "2025-08-07", "2025-08-15", "2025-08-30"]),
    # "top": shade the fifth of the lake with the most chlorophyll that day. Most 2026 days were below the fixed cutoff.
    2026: dict(mode="top", dates=["2026-07-06", "2026-07-11", "2026-07-13", "2026-07-23", "2026-07-28", "2026-08-02", "2026-08-20", "2026-08-27"]),
}
args = [a for a in sys.argv[1:] if not a.startswith("--")]; PREVIEW = "--preview" in sys.argv
YEAR = args[0] if args else "2026"; MODE = SUMMERS[int(YEAR)]["mode"]; DATES = SUMMERS[int(YEAR)]["dates"]; TOP_SHARE = 0.20
DARKEST = {"2025": "along the east side and the north end", "2026": "down the east half of the lake"}[YEAR]
SUFFIX = f"_{YEAR}" if PREVIEW else ""
W, H = 219, 480                                # frame size of the filmstrip
VB_W, VB_H, LAKE_H = 400, 240, 200             # card viewBox and the lake's height in it

# The frames cover the lake's bounding box plus 1,500 m, in Web Mercator.
lake = json.load(open(f"{HERE}/lake_winnebago_outline.geojson"))["features"][0]["geometry"]["coordinates"][0]
lons = [c[0] for c in lake]; lats = [c[1] for c in lake]
dlat = 1500 / 111320; dlon = 1500 / (111320 * math.cos(math.radians(44.0)))
merc = lambda la: math.log(math.tan(math.pi / 4 + math.radians(la) / 2))
x0, x1 = min(lons) - dlon, max(lons) + dlon; y0, y1 = merc(min(lats) - dlat), merc(max(lats) + dlat)
px = lambda lo, la: ((lo - x0) / (x1 - x0) * W, (y1 - merc(la)) / (y1 - y0) * H)
k = LAKE_H / H; ox = VB_W / 2 - W * k / 2; oy = (VB_H - LAKE_H) / 2
card = lambda x, y: (ox + x * k, oy + y * k)

poly = np.array([px(lo, la) for lo, la in lake], dtype=np.float32)
lake_mask = np.zeros((H, W), np.uint8); cv2.fillPoly(lake_mask, [np.round(poly).astype(np.int32)], 255)
lake_mask = cv2.erode(lake_mask, np.ones((3, 3), np.uint8))          # stay off the shoreline pixels


def chaikin(pts, n=2):
    for _ in range(n):
        out = []
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            out += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]), (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        pts = out
    return pts


def path(pts):
    return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in (card(*p) for p in pts)) + "Z"


outline = cv2.approxPolyDP(poly.reshape(-1, 1, 2), 1.2, True).reshape(-1, 2)
OUTLINE = path([tuple(p) for p in outline])

CELL, CLAMP, QS = 5, 40, 3                    # grid spacing and distance limit in frame pixels; stored value = distance x QS
GW, GH = W // CELL + 1, H // CELL + 1
daily = {r["date"]: r for r in csv.DictReader(open(f"{HERE}/data/winnebago_daily.csv"))}
clear = [d for d, r in sorted(daily.items()) if d[:4] == YEAR and d[5:7] in ("07", "08") and float(r["clear_frac"]) >= 0.8 and r["chl_median"]]
gif = Image.open(f"{HERE}/media/filmstrip_{YEAR}_chlorophyll.gif")
PAL = np.array([[int(h[i:i + 2], 16) for i in (0, 2, 4)] for h in ["08306b", "2171b5", "4eb3d3", "7fcdbb", "c7e9b4", "fee08b", "fc8d59", "d73027"]], float)
LUT = np.array([[np.interp(t, np.linspace(0, 1, 8), PAL[:, c]) for c in range(3)] for t in np.linspace(0, 1, 256)])
masks = []
frames = []
for d in DATES:
    gif.seek(clear.index(d)); a = np.array(gif.convert("RGB")).astype(int)
    if MODE == "fixed":
        hot = ((a[..., 0] > 200) & (a[..., 1] < 170) & (a[..., 2] < 125)).astype(np.uint8) * 255      # orange to red on the palette
    else:
        # Read each pixel's place on the 0-60 palette back from its colour, then keep the top fifth of the lake's clear pixels.
        # Pixels that are not a palette colour (cloud) are left out. If more than a fifth of the lake is at the top of the scale, all of it is kept.
        # The GIF is dithered down to a few dozen colours, so average neighbouring pixels before matching colours to the palette.
        sm = cv2.GaussianBlur(a.astype(np.float32), (0, 0), 1.6)
        d2 = ((sm[:, :, None, :] - LUT[None, None, :, :]) ** 2).sum(-1); val = d2.argmin(-1).astype(np.float32) / 255; ok = (d2.min(-1) < 1600) & (lake_mask > 0)
        val = cv2.GaussianBlur(np.where(ok, val, 0), (0, 0), 3) / np.maximum(cv2.GaussianBlur(ok.astype(np.float32), (0, 0), 3), 1e-3)
        thr = min(np.quantile(val[ok], 1 - TOP_SHARE), 0.93)                      # 0.93 and up is the top of the scale (about 56 mg/m3)
        hot = ((val >= thr) & ok).astype(np.uint8) * 255
    hot = cv2.bitwise_and(hot, lake_mask)
    hot = cv2.morphologyEx(hot, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    hot = cv2.morphologyEx(hot, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    cs, _ = cv2.findContours(hot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cs = [c for c in cs if cv2.contourArea(c) >= 60]
    keep = np.zeros_like(hot); cv2.drawContours(keep, cs, -1, 255, -1); keep = cv2.bitwise_and(keep, hot)
    sd = cv2.distanceTransform(keep, cv2.DIST_L2, 5) - cv2.distanceTransform(255 - keep, cv2.DIST_L2, 5)
    sd = cv2.GaussianBlur(sd, (0, 0), 2.0)
    g = np.full((GH, GW), -CLAMP, np.float32)
    ys = np.minimum(np.arange(GH) * CELL, H - 1); xs = np.minimum(np.arange(GW) * CELL, W - 1)
    g[:, :] = sd[np.ix_(ys, xs)]
    g[0, :] = np.minimum(g[0, :], -2); g[-1, :] = np.minimum(g[-1, :], -2); g[:, 0] = np.minimum(g[:, 0], -2); g[:, -1] = np.minimum(g[:, -1], -2)
    q = np.clip(np.round(np.clip(g, -CLAMP, CLAMP) * QS), -127, 127).astype(np.int8)
    share = 100 * (keep > 0).sum() / (lake_mask > 0).sum(); masks.append(keep)
    u, v = float(daily[d]["wind_u"]), float(daily[d]["wind_v"])
    to = math.degrees(math.atan2(u, v)) % 360                                  # bearing the wind blows toward, clockwise from north
    frm = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][int((((to + 180) % 360) + 22.5) // 45) % 8]
    frames.append(dict(date=d, label=datetime.date.fromisoformat(d).strftime("%b %-d").upper(), to=round(to), frm=frm, mph=round(math.hypot(u, v) * 2.237), g=base64.b64encode(q.tobytes()).decode()))
    print(d, "patches", len(cs), "share of lake", round(share), "%", "| wind from", frm, "toward", round(to), "deg,", round(math.hypot(u, v) * 2.237, 1), "mph")

JS = r"""/* Lake Winnebago card: the high-chlorophyll patches of summer 2025, each clear day's shapes changing into the next day's.
   Built by projects/lake-winnebago-blooms/build_card.py. Only the ten dated shapes are data; the in-between shapes are drawn by the animation. */
(function () {
  var D = __DATA__;
  var fig = document.getElementById('lwcard'); if (!fig) return;
  var NS = 'http://www.w3.org/2000/svg', svg = fig.querySelector('svg'), stage = svg.querySelector('.lw-stage');
  var tick = svg.querySelector('.lw-date'), tag = svg.querySelector('.lw-tag'), dots = svg.querySelector('.lw-dots');
  var vane = svg.querySelector('.lw-vane'), arrow = svg.querySelector('.lw-arrow'), wind = svg.querySelector('.lw-wind'), speed = svg.querySelector('.lw-speed');
  var GW = D.gw, GH = D.gh, N = D.frames.length, M = GW * GH;
  var grids = D.frames.map(function (f) { var b = atob(f.g), a = new Float32Array(M); for (var i = 0; i < M; i++) { var c = b.charCodeAt(i); a[i] = c > 127 ? c - 256 : c; } return a; });
  function el(name, cls, parent) { var e = document.createElementNS(NS, name); if (cls) e.setAttribute('class', cls); (parent || stage).appendChild(e); return e; }
  var clip = el('clipPath'); clip.id = 'lw-clip'; el('path', null, clip).setAttribute('d', D.outline);
  var inside = el('g'); inside.setAttribute('clip-path', 'url(#lw-clip)');
  var stack = el('g', 'lw-stack', inside), blob = el('path', 'lw-blob', inside); blob.setAttribute('fill-rule', 'evenodd');
  el('path', 'lw-line').setAttribute('d', D.outline);
  var marks = D.frames.map(function (f, i) { var r = el('rect', null, dots); r.setAttribute('x', 16 + i * 7); r.setAttribute('y', 203); r.setAttribute('width', 5); r.setAttribute('height', 2); return r; });

  /* Trace the edge where a grid crosses zero (marching squares), join the pieces into closed loops, and return an SVG path. */
  var SEG = [[], [3, 2], [2, 1], [3, 1], [0, 1], [0, 3, 2, 1], [0, 2], [0, 3], [0, 3], [0, 2], [0, 1, 3, 2], [0, 1], [3, 1], [2, 1], [3, 2], []];
  var buf = new Float32Array(M);
  function trace(v) {
    var adj = {}, pt = {}, keys = [];
    function edge(i, j, side) {                       /* 0 top, 1 right, 2 bottom, 3 left */
      var k, a, b, x, y;
      if (side === 0 || side === 2) { var jj = j + (side === 2 ? 1 : 0); k = 2 * (jj * GW + i); if (!pt[k]) { a = v[jj * GW + i]; b = v[jj * GW + i + 1]; pt[k] = [i + a / (a - b), jj]; } }
      else { var ii = i + (side === 1 ? 1 : 0); k = 2 * (j * GW + ii) + 1; if (!pt[k]) { a = v[j * GW + ii]; b = v[(j + 1) * GW + ii]; pt[k] = [ii, j + a / (a - b)]; } }
      return k;
    }
    for (var j = 0; j < GH - 1; j++) for (var i = 0; i < GW - 1; i++) {
      var o = j * GW + i, c = (v[o] > 0 ? 8 : 0) | (v[o + 1] > 0 ? 4 : 0) | (v[o + GW + 1] > 0 ? 2 : 0) | (v[o + GW] > 0 ? 1 : 0);
      if (c === 0 || c === 15) continue;
      var s = SEG[c];
      for (var q = 0; q < s.length; q += 2) {
        var k1 = edge(i, j, s[q]), k2 = edge(i, j, s[q + 1]);
        if (!adj[k1]) { adj[k1] = []; keys.push(k1); } if (!adj[k2]) { adj[k2] = []; keys.push(k2); }
        adj[k1].push(k2); adj[k2].push(k1);
      }
    }
    var seen = {}, d = '';
    for (var n = 0; n < keys.length; n++) {
      var st = keys[n]; if (seen[st]) continue;
      var loop = [], cur = st, prev = -1;
      while (cur !== undefined && !seen[cur]) { seen[cur] = 1; loop.push(pt[cur]); var a2 = adj[cur], nx = a2[0] !== prev && !seen[a2[0]] ? a2[0] : a2[1]; prev = cur; cur = nx; }
      var L = loop.length; if (L < 4) continue;
      /* smooth: curve through the midpoints of the traced edge */
      var X = function (p) { return (D.ox + p[0] * D.s).toFixed(1); }, Y = function (p) { return (D.oy + p[1] * D.s).toFixed(1); };
      var mid = function (p, r) { return [(p[0] + r[0]) / 2, (p[1] + r[1]) / 2]; }, m0 = mid(loop[L - 1], loop[0]);
      d += 'M' + X(m0) + ',' + Y(m0);
      for (var e = 0; e < L; e++) { var m = mid(loop[e], loop[(e + 1) % L]); d += 'Q' + X(loop[e]) + ',' + Y(loop[e]) + ' ' + X(m) + ',' + Y(m); }
      d += 'Z';
    }
    return d;
  }
  var dayPath = grids.map(trace);
  /* The ending: every day's shapes laid over each other, so overlap shows where the chlorophyll sat most often. */
  dayPath.forEach(function (d) { var b = el('path', null, stack); b.setAttribute('d', d); b.setAttribute('fill-rule', 'evenodd'); });

  var clamp = function (x) { return Math.max(0, Math.min(1, x)); };
  var ease = function (u) { return u * u * (3 - 2 * u); };
  var HOLD0 = 1000, MORPH = 900, HOLD = 320, STEP = MORPH + HOLD, STACK = 800, HOLD1 = 3000, FADE = 380;
  var RUN = HOLD0 + (N - 1) * STEP, TOTAL = RUN + STACK + HOLD1 + 2 * FADE, last = '';
  function draw(ms) {
    var t = ms % TOTAL, i = 0, u = 0, all = 1;
    if (t >= HOLD0) { var r = t - HOLD0; i = Math.min(N - 1, Math.floor(r / STEP)); u = i < N - 1 ? ease(clamp((r - i * STEP) / MORPH)) : 0; }
    var d;
    if (u <= 0) d = dayPath[i]; else if (u >= 1) d = dayPath[i + 1];
    else { var a = grids[i], b = grids[i + 1]; for (var k = 0; k < M; k++) buf[k] = a[k] + (b[k] - a[k]) * u; d = trace(buf); }
    if (d !== last) { blob.setAttribute('d', d); last = d; }
    var cur = u >= 0.5 ? i + 1 : i;
    if (tick.textContent !== D.frames[cur].label) tick.textContent = D.frames[cur].label;
    for (var n = 0; n < N; n++) marks[n].style.opacity = n <= cur ? 0.9 : 0.25;
    /* wind vane: turn the short way round from one day's direction to the next */
    var a0 = D.frames[i].to, a1 = D.frames[Math.min(N - 1, i + 1)].to, turn = ((a1 - a0 + 540) % 360) - 180;
    arrow.setAttribute('transform', 'rotate(' + (a0 + turn * u).toFixed(1) + ')');
    var wl = 'WIND FROM ' + D.frames[cur].frm; if (wind.textContent !== wl) wind.textContent = wl;
    var sl = D.frames[cur].mph + ' MPH'; if (speed.textContent !== sl) speed.textContent = sl;
    var end = TOTAL - 2 * FADE;
    if (t > end) all = t < end + FADE ? 1 - (t - end) / FADE : 0;
    if (t < FADE && ms > TOTAL) all = t / FADE;
    var st = ease(clamp((t - RUN) / STACK));
    stack.style.opacity = st * all; blob.style.opacity = (1 - st) * all;
    tag.style.opacity = st * all; tick.style.opacity = (1 - st) * all; dots.style.opacity = all; vane.style.opacity = (1 - st) * all;
  }
  function still() { draw(RUN + STACK + 1000); }                        /* the ending: all ten days stacked */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) { still(); return; }
  var raf = null, t0 = null, offset = 0;
  function frame(now) { if (t0 === null) t0 = now; draw(offset + now - t0); raf = requestAnimationFrame(frame); }
  function start() { if (raf === null) { t0 = null; raf = requestAnimationFrame(frame); } }
  function stop() { if (raf !== null) { cancelAnimationFrame(raf); raf = null; offset += performance.now() - (t0 || performance.now()); } }
  draw(0);
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? start() : stop(); }); }, { threshold: 0.5 }).observe(fig);
  else start();
  window.__lwDraw = draw; window.__lwTotal = TOTAL;
})();
"""
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"][len(DATES)]
WHAT = "where chlorophyll was highest" if MODE == "fixed" else "over the fifth of the lake with the most chlorophyll each day"
JS = JS.replace("summer 2025", f"summer {YEAR}").replace("Only the ten dated shapes", f"Only the {NUM} dated shapes").replace("all ten days stacked", f"all {NUM} days stacked")
data = {"outline": OUTLINE, "gw": GW, "gh": GH, "ox": round(ox, 3), "oy": round(oy, 3), "s": round(CELL * k, 5), "frames": frames}
open(os.path.join(OUT, f"morph{SUFFIX}.js"), "w").write(JS.replace("__DATA__", json.dumps(data, separators=(",", ":"))))
if os.path.exists(os.path.join(OUT, "tunnel.js")): os.remove(os.path.join(OUT, "tunnel.js"))
CARD = """<!-- lake-card:start -->
<figure class="lake-card" id="lwcard" aria-label="Outline of Lake Winnebago with green patches where chlorophyll was highest. The patches change shape from one clear satellite day to the next through July and August 2025, ten days in all, while a wind vane beside the lake turns to show which way and how fast the wind had been blowing over the three days before each image. It ends with all ten days laid over each other, darkest along the east side and the north end.">
  <svg viewBox="0 0 400 240" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <g class="lw-stage"></g>
    <text x="16" y="26" class="svg-label">SUMMER 2025 · SENTINEL-2</text>
    <g class="lw-dots"></g>
    <g class="lw-vane" transform="translate(318 112)">
      <circle r="24" class="lw-ring"/>
      <path class="lw-ring" d="M0,-24V-20M24,0H20M0,24V20M-24,0H-20"/>
      <text y="-30" class="svg-label" text-anchor="middle">N</text>
      <g class="lw-arrow"><path d="M0,15V-13M-5,-7L0,-15L5,-7M-4,17L0,12L4,17M-4,12L0,7L4,12"/><circle r="2"/></g>
      <text y="44" class="svg-label lw-wind" text-anchor="middle">WIND FROM W</text>
      <text y="60" class="svg-label lw-speed" text-anchor="middle">5 MPH</text>
    </g>
    <text x="16" y="222" class="svg-label lw-date">JUL 3</text>
    <text x="384" y="222" class="svg-label lw-tag" text-anchor="end" style="opacity:0">ALL 10 CLEAR DAYS, STACKED</text>
  </svg>
</figure>
<!-- lake-card:end -->"""
CARD = (CARD.replace("where chlorophyll was highest", WHAT).replace("July and August 2025, ten days in all", f"July and August {YEAR}, {NUM} days in all")
        .replace("all ten days laid over each other, darkest along the east side and the north end", f"all {NUM} days laid over each other, darkest {DARKEST}")
        .replace("SUMMER 2025", f"SUMMER {YEAR}").replace("ALL 10 CLEAR DAYS", f"ALL {len(DATES)} CLEAR DAYS"))
assert YEAR in CARD and "ten" not in CARD.replace("often", "") or len(DATES) == 10
open(os.path.join(OUT, f"card{SUFFIX}.html"), "w").write(CARD)
np.save("/tmp/lw_masks.npy", np.array(masks))
print("ok", os.path.getsize(os.path.join(OUT, f"morph{SUFFIX}.js")), "bytes")
