"""Build the homepage card for Lake Winnebago from Space: a tunnel of nested lake outlines, one per clear day of summer 2025.

Each ring is the lake on one clear Sentinel-2 day. The green shapes are where that day's chlorophyll-a estimate was highest
(orange to red on the 0-60 mg/m3 scale, about 48 mg/m3 and up), traced from the frames of media/filmstrip_2025_chlorophyll.gif.
Summer 2025 was chosen because its blooms form separate patches that shift from day to day; 2019 was heavier but fills most of the lake.
The last ring ends with all ten days laid over each other, which shows where the chlorophyll sat most often.

Run from the repository root:  python3 projects/lake-winnebago-blooms/build_card.py
Writes media/lake-winnebago-card/tunnel.js and card.html (the figure markup for index.html).
"""
import csv, datetime, json, math, os
import cv2, numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "media", "lake-winnebago-card"); os.makedirs(OUT, exist_ok=True)
DATES = ["2025-07-03", "2025-07-13", "2025-07-18", "2025-07-20", "2025-07-21", "2025-07-28", "2025-08-02", "2025-08-07", "2025-08-15", "2025-08-30"]
YEAR = DATES[0][:4]
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

daily = {r["date"]: r for r in csv.DictReader(open(f"{HERE}/data/winnebago_daily.csv"))}
all19 = [d for d, r in sorted(daily.items()) if d[:4] == YEAR and d[5:7] in ("07", "08") and float(r["clear_frac"]) >= 0.8 and r["chl_median"]]
gif = Image.open(f"{HERE}/media/filmstrip_{YEAR}_chlorophyll.gif")
frames = []
for d in DATES:
    gif.seek(all19.index(d)); a = np.array(gif.convert("RGB")).astype(int)
    hot = ((a[..., 0] > 200) & (a[..., 1] < 170) & (a[..., 2] < 125)).astype(np.uint8) * 255      # orange to red on the palette
    hot = cv2.bitwise_and(hot, lake_mask)
    hot = cv2.morphologyEx(hot, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    hot = cv2.morphologyEx(hot, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    cs, _ = cv2.findContours(hot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cs = sorted([c for c in cs if cv2.contourArea(c) >= 60], key=cv2.contourArea, reverse=True)[:7]
    ds = []
    for c in cs:
        s = cv2.approxPolyDP(c, 1.6, True).reshape(-1, 2)
        if len(s) >= 3: ds.append(path(chaikin([tuple(map(float, p)) for p in s])))
    share = 100 * (hot > 0).sum() / (lake_mask > 0).sum()
    r = daily[d]
    frames.append(dict(date=d, label=datetime.date.fromisoformat(d).strftime("%b %-d").upper(), d="".join(ds), share=round(share),
                       east=round(float(r["chl_east"])), west=round(float(r["chl_west"]))))
    print(d, "blobs", len(ds), "share of lake", round(share), "% | east", frames[-1]["east"], "west", frames[-1]["west"], "| path chars", len(frames[-1]["d"]))

JS = r'''/* Lake Winnebago card: a tunnel of nested lake outlines, one per clear day of summer 2025.
   Built by projects/lake-winnebago-blooms/build_card.py. The green shapes are where each day's chlorophyll-a estimate was highest. */
(function () {
  var D = __DATA__;
  var fig = document.getElementById('lwcard'); if (!fig) return;
  var NS = 'http://www.w3.org/2000/svg', svg = fig.querySelector('svg'), stage = svg.querySelector('.lw-stage');
  var tick = svg.querySelector('.lw-date'), tag = svg.querySelector('.lw-tag');
  var CX = 200, CY = 120, RATIO = 0.5, N = D.frames.length;
  var rings = D.frames.map(function (f) {
    var g = document.createElementNS(NS, 'g');
    var blobs = document.createElementNS(NS, 'path'); blobs.setAttribute('d', f.d); blobs.setAttribute('class', 'lw-blob');
    var line = document.createElementNS(NS, 'path'); line.setAttribute('d', D.outline); line.setAttribute('class', 'lw-line');
    g.appendChild(blobs); g.appendChild(line); stage.insertBefore(g, stage.firstChild); return g;
  });
  /* The ending: every day's shapes laid over the last outline, so overlap shows where the chlorophyll sat most often. */
  var stack = document.createElementNS(NS, 'g'); stack.setAttribute('class', 'lw-stack');
  D.frames.forEach(function (f) { var b = document.createElementNS(NS, 'path'); b.setAttribute('d', f.d); stack.appendChild(b); });
  rings[N - 1].insertBefore(stack, rings[N - 1].firstChild);
  var clamp = function (v) { return Math.max(0, Math.min(1, v)); };
  var HOLD0 = 1100, STEP = 640, LAND = 1200, HOLD1 = 3200, FADE = 380;
  var TRAVEL = (N - 2) * STEP, TOTAL = HOLD0 + TRAVEL + LAND + HOLD1 + 2 * FADE;
  function draw(ms) {
    var t = ms % TOTAL, p, intro = 1, all = 1;
    if (t < HOLD0) { p = 0; intro = clamp((t - 500) / 500); }
    else if (t < HOLD0 + TRAVEL) p = (t - HOLD0) / STEP;
    else if (t < HOLD0 + TRAVEL + LAND) { var u = (t - HOLD0 - TRAVEL) / LAND; p = (N - 2) + 1 - Math.pow(1 - u, 3) * 1; p = Math.min(p, N - 1); }
    else p = N - 1;
    var end = TOTAL - 2 * FADE;
    if (t > end) all = t < end + FADE ? 1 - (t - end) / FADE : 0;
    if (t < FADE && ms > TOTAL) all = t / FADE;
    for (var i = 0; i < N; i++) {
      var s = Math.pow(RATIO, i - p), o;
      if (s <= 1) o = clamp((s - 0.055) / 0.07) * (i === 0 ? 1 : (p > 0 ? 1 : intro));
      else o = 1 - clamp((s - 1.1) / 0.8);
      var g = rings[i];
      if (o <= 0.01) { g.style.display = 'none'; continue; }
      g.style.display = '';
      g.setAttribute('transform', 'translate(' + CX + ' ' + CY + ') scale(' + s.toFixed(4) + ') translate(' + (-CX) + ' ' + (-CY) + ')');
      g.style.opacity = (o * all).toFixed(3);
    }
    var cur = Math.min(N - 1, Math.floor(p + 0.5));
    if (tick.textContent !== D.frames[cur].label) tick.textContent = D.frames[cur].label;
    tick.style.opacity = all; var landed = p >= N - 1 - 0.02;
    var since = t - (HOLD0 + TRAVEL + LAND);
    var st = landed ? clamp(since / 700) : 0;
    stack.style.opacity = st; rings[N - 1].firstChild.nextSibling.style.opacity = 1 - st;
    tag.style.opacity = st * all;
  }
  function still() { draw(HOLD0 + TRAVEL + LAND + 1500); }               /* the ending: all ten days stacked */
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
'''
open(os.path.join(OUT, "tunnel.js"), "w").write(JS.replace("__DATA__", json.dumps({"outline": OUTLINE, "frames": frames}, separators=(",", ":"))))
CARD = '''<!-- lake-card:start -->
<figure class="lake-card" id="lwcard" aria-label="Outline of Lake Winnebago with green patches where chlorophyll was highest. The view travels through ten nested outlines, one for each clear satellite day of July and August 2025, as the patches shift from day to day. It ends with all ten days laid over each other, darkest along the east side and the north end.">
  <svg viewBox="0 0 400 240" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <g class="lw-stage"></g>
    <text x="16" y="26" class="svg-label">SUMMER 2025 · SENTINEL-2</text>
    <text x="16" y="222" class="svg-label lw-date">JUL 3</text>
    <text x="384" y="222" class="svg-label lw-tag" text-anchor="end" style="opacity:0">ALL 10 CLEAR DAYS, STACKED</text>
  </svg>
</figure>
<!-- lake-card:end -->'''
open(os.path.join(OUT, "card.html"), "w").write(CARD)
print("ok", os.path.getsize(os.path.join(OUT, "tunnel.js")), "bytes")
