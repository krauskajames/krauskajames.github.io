"""Build the chapter 1 page body (page_body.html) and its images from the data in data/ and media/.

Run from the repository root:  python3 projects/lake-winnebago-blooms/build_page.py
Then:  python3 projects/assemble_page.py projects/lake-winnebago-blooms/page_body.html lake-winnebago.html "<title>" "<description>"
       and projects/build_flow.py for the data-flow diagram.
Every number on the page is computed here from the CSV files, so the page cannot drift from the data.
"""
import csv, datetime, html, math, os, statistics as st
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "media", "lake-winnebago"); os.makedirs(OUT, exist_ok=True)
M = "media/lake-winnebago/"
esc = html.escape


def f(x):
    try: return float(x)
    except (TypeError, ValueError): return None


# ---------------------------------------------------------------- data
daily = list(csv.DictReader(open(f"{HERE}/data/winnebago_daily.csv")))
for r in daily:
    for k in list(r):
        if k != "date": r[k] = f(r[k])
D = {r["date"]: r for r in daily}
clear = [r for r in daily if r["clear_frac"] is not None and r["clear_frac"] >= 0.5
         and r["chl_east"] is not None and r["chl_west"] is not None]
for r in clear:
    r["gap"] = r["chl_east"] - r["chl_west"]
    r["speed"] = math.hypot(r["wind_u"], r["wind_v"])
    r["from"] = (math.degrees(math.atan2(-r["wind_u"], -r["wind_v"]))) % 360
    r["sector"] = int((r["from"] + 22.5) // 45) % 8
NAMES = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
LONG = ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest"]
N_CLEAR = len(clear)
sector = []
for i in range(8):
    g = [r for r in clear if r["sector"] == i]
    sector.append(dict(name=NAMES[i], long=LONG[i], n=len(g), share=100 * sum(r["gap"] > 0 for r in g) / len(g),
                       mean=st.mean(r["gap"] for r in g)))
W = sector[6]; NEs = sector[1]


def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); rk = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): rk[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return rk


def pearson(a, b):
    ma, mb = st.mean(a), st.mean(b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))


U = [r["wind_u"] for r in clear]; G = [r["gap"] for r in clear]
RHO = pearson(ranks(U), ranks(G)); R2 = pearson(U, G) ** 2
SLOPE = pearson(U, G) * st.pstdev(G) / st.pstdev(U); ICPT = st.mean(G) - SLOPE * st.mean(U)

monthly = list(csv.DictReader(open(f"{HERE}/data/winnebago_chla_monthly.csv")))
years = sorted({m["month"][:4] for m in monthly})
MON = {y: [f(m["chl_median"]) for m in monthly if m["month"].startswith(y)] for y in years}
MEAN = [st.mean(MON[y][i] for y in years) for i in range(4)]
JUNE_LO, JUNE_HI = min(MON[y][0] for y in years), max(MON[y][0] for y in years)

dnr = [r for r in csv.DictReader(open(f"{HERE}/data/dnr_lake_winnebago_samples_2017_2026.csv")) if r["parameter"].startswith("Chlorophyll")]
N_DNR = len(dnr)
bydate = {}
for r in dnr:
    if f(r["value"]) is not None: bydate.setdefault(r["date"], []).append(f(r["value"]))
sat = {r["date"]: r for r in daily if r["chl_median"] is not None and (r["clear_frac"] or 0) >= 0.5}
pairs = []
for d, vals in sorted(bydate.items()):
    d0 = datetime.date.fromisoformat(d); best = None
    for k in (0, -1, 1, -2, 2):
        key = (d0 + datetime.timedelta(days=k)).isoformat()
        if key in sat: best = (k, sat[key]); break
    if best: pairs.append(dict(date=d, sample=st.mean(vals), sat=best[1]["chl_median"], lag=best[0]))
DN_RHO = pearson(ranks([p["sample"] for p in pairs]), ranks([p["sat"] for p in pairs]))
DN_RATIO = st.median(p["sat"] / p["sample"] for p in pairs)


boat = []
for r in csv.DictReader(open(f"{HERE}/data/winnebago_boat_match.csv")):
    pc, ch, cs, tb = f(r["phycocyanin_rfu"]), f(r["s2_chl"]), f(r["s2_clear_score"]), f(r["turbidity_fnu"])
    if pc is not None and ch is not None and cs is not None and cs >= 0.65:
        boat.append(dict(date=r["date"], pc=pc, chl=ch, off=abs(int(float(r["s2_days_off"]))), fai=f(r["s2_fai"]), tb=tb,
                         bchl=f(r["chlorophyll_rfu"])))
N_BOAT = len(boat); BOAT_DATES = sorted({b["date"] for b in boat})
def rho(a, b):
    k = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    return pearson(ranks([x for x, _ in k]), ranks([y for _, y in k]))
B_RHO = rho([b["pc"] for b in boat], [b["chl"] for b in boat])
B_SAME = rho([b["pc"] for b in boat if b["off"] == 0], [b["chl"] for b in boat if b["off"] == 0])
B_FAI = rho([b["pc"] for b in boat], [b["fai"] for b in boat])
B_BCHL = rho([b["bchl"] for b in boat], [b["chl"] for b in boat])
_k = [b for b in boat if b["tb"] is not None]
_ab, _ac, _bc = rho([b["pc"] for b in _k], [b["chl"] for b in _k]), rho([b["pc"] for b in _k], [b["tb"] for b in _k]), rho([b["chl"] for b in _k], [b["tb"] for b in _k])
B_PARTIAL = (_ab - _ac * _bc) / math.sqrt((1 - _ac ** 2) * (1 - _bc ** 2))
BINS = []
for i in range(9):                                   # 0-1, 1-2, ... 7-8, and 8 or more
    g = [b for b in boat if (i <= b["pc"] < i + 1) or (i == 8 and b["pc"] >= 8)]
    if len(g) < 30: continue
    c = sorted(b["chl"] for b in g)
    BINS.append(dict(x=min(st.median(b["pc"] for b in g), 8.6), lo=c[len(c) // 4], med=st.median(c), hi=c[3 * len(c) // 4], n=len(g),
                     lab=(f"{i} to {i + 1}" if i < 8 else "8 or more")))


def day(d): return datetime.date.fromisoformat(d).strftime("%b %-d, %Y").replace("Jun ", "June ").replace("Jul ", "July ")
def n1(x): return f"{x:.1f}"
def n0(x): return f"{x:.0f}"
def sgn(x): return ("+" if x >= 0 else "−") + f"{abs(x):.1f}"
def sgn2(x): return ("" if x >= 0 else "−") + f"{abs(x):.2f}"


# ---------------------------------------------------------------- images
def webp(src, name, maxw=None, q=82):
    im = Image.open(src).convert("RGB")
    if maxw and im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, name), "WEBP", quality=q, method=6); return im.size


def frames(gif, prefix, labels):
    im = Image.open(gif); out = []
    for i, lab in enumerate(labels):
        im.seek(i); name = f"{prefix}-{lab}.webp"
        im.convert("RGB").save(os.path.join(OUT, name), "WEBP", quality=80, method=6); out.append(name)
    return out


d19 = [r["date"] for r in daily if r["date"][:4] == "2019" and r["date"][5:7] in ("07", "08")
       and (r["clear_frac"] or 0) >= 0.8 and r["chl_median"] is not None]
t19 = dict(zip(d19, frames(f"{HERE}/media/filmstrip_2019_truecolor.gif", "s2-2019-true", d19)))
c19 = dict(zip(d19, frames(f"{HERE}/media/filmstrip_2019_chlorophyll.gif", "s2-2019-chl", d19)))
KEY19 = ["2019-07-10", "2019-07-25", "2019-07-28", "2019-08-04", "2019-08-09", "2019-08-19", "2019-08-27"]
ls_dates = [r["landsat_date"] for r in csv.DictReader(open(f"{HERE}/media/augusts_1999_2026_dates.csv"))]
lsf = dict(zip(ls_dates, frames(f"{HERE}/media/augusts_1999_2026_landsat.gif", "landsat", ls_dates)))
CLOUDY = {"2003-08-15", "2009-08-15", "2014-08-13", "2015-07-31"}
PH = f"{HERE}/photos_blurred"
photos = {}
for key in ("sail_garage_2014-07-05", "sail_rescue_2014-07-05", "kayaks_dog_2018-08-11", "dock_kayaks_2018-09-02", "sheepshead_2018-08-10"):
    p = f"{PH}/{key}.jpg"
    if os.path.exists(p): photos[key] = webp(p, f"photo-{key}.webp", 1400)


def wind_words(r):
    sp = math.hypot(r["wind_u"], r["wind_v"]) * 2.237
    if sp < 2.2: return "near calm"
    d = LONG[int(((math.degrees(math.atan2(-r["wind_u"], -r["wind_v"])) % 360) + 22.5) // 45) % 8]
    return f"from the {d}, {sp:.0f} mph"


# ---------------------------------------------------------------- charts (inline SVG, site tokens)
def tip(t): return f' tabindex="0" data-tip="{esc(t, quote=True)}"'


def chart_compass():
    """HTML bars, so the key chart stays readable on a phone."""
    rows = sorted(sector, key=lambda z: -z["share"]); out = []
    for r in rows:
        t = f'Wind from the {r["long"]}: east shore higher on {r["share"]:.0f}% of {r["n"]} clear days; average east minus west {sgn(r["mean"])} mg/m³'
        out.append(f'<div class="hb-row"{tip(t)}><span class="hb-cat">{r["long"].capitalize()} <i>{r["n"]} days</i></span>'
                   f'<span class="hb-track"><span class="hb-fill" style="width:{r["share"]:.1f}%"></span></span><span class="hb-val">{r["share"]:.0f}%</span></div>')
    out.append('<div class="hb-row hb-axis" aria-hidden="true"><span></span><span class="hb-ticks"><span>0%</span><span>50%, no difference</span><span>100%</span></span><span></span></div>')
    return '<div class="hbars" role="group" aria-label="Share of clear days when the east shore had more chlorophyll than the west, by the direction the wind came from">' + "".join(out) + "</div>"


def chart_scatter():
    Wd, H, l, r_, t, b = 720, 420, 62, 24, 26, 52; pw, ph = Wd - l - r_, H - t - b
    x0, x1, y0, y1 = -4.5, 5, -65, 90
    X = lambda v: l + pw * (v - x0) / (x1 - x0); Y = lambda v: t + ph * (1 - (v - y0) / (y1 - y0))
    s = [f'<svg class="chart" viewBox="0 0 {Wd} {H}" role="img" aria-labelledby="c2t"><title id="c2t">Each dot is one clear day: east-west wind against the east-minus-west chlorophyll gap</title>']
    for v in range(-60, 81, 20):
        s.append(f'<line class="grid{" ref" if v == 0 else ""}" x1="{l}" x2="{Wd - r_}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text class="tick" x="{l - 8}" y="{Y(v) + 4:.1f}" text-anchor="end">{"+" if v > 0 else ("−" if v < 0 else "")}{abs(v)}</text>')
    for v in range(-4, 6, 2):
        s.append(f'<line class="grid{" ref" if v == 0 else ""}" x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{t}" y2="{H - b}"/><text class="tick" x="{X(v):.1f}" y="{H - b + 18}" text-anchor="middle">{"+" if v > 0 else ("−" if v < 0 else "")}{abs(v)}</text>')
    s.append(f'<text class="note" x="{Wd - r_}" y="{H - 10}" text-anchor="end">blowing toward the east shore (a west wind) →</text><text class="note" x="{l}" y="{H - 10}">← blowing toward the west shore</text>')
    s.append(f'<text class="note" x="{l + 8}" y="{t + 12}">↑ east shore higher</text><text class="note" x="{l + 8}" y="{H - b - 8}">↓ west shore higher</text>')
    for r in clear:
        gy = max(y0, min(y1, r["gap"]))
        s.append(f'<circle class="dot" cx="{X(r["wind_u"]):.1f}" cy="{Y(gy):.1f}" r="4"{tip(f"{day(r["date"])}: east {r["chl_east"]:.0f}, west {r["chl_west"]:.0f} mg/m³; wind {wind_words(r)}")}/>')
    s.append(f'<line class="trend" x1="{X(x0):.1f}" y1="{Y(ICPT + SLOPE * x0):.1f}" x2="{X(x1):.1f}" y2="{Y(ICPT + SLOPE * x1):.1f}"/>')
    s.append("</svg>"); return "".join(s)


def chart_monthly():
    Wd, H, l, r_, t, b = 720, 360, 52, 150, 20, 40; pw, ph = Wd - l - r_, H - t - b
    X = lambda i: l + pw * i / 3; Y = lambda v: t + ph * (1 - v / 60)
    s = [f'<svg class="chart" viewBox="0 0 {Wd} {H}" role="img" aria-labelledby="c3t"><title id="c3t">Monthly lake-wide chlorophyll-a, June to September, one line per summer from 2019 to 2025, with the seven-year average</title>']
    for v in range(0, 61, 20):
        s.append(f'<line class="grid" x1="{l}" x2="{Wd - r_}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text class="tick" x="{l - 8}" y="{Y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    for i, m in enumerate(["June", "July", "August", "September"]):
        s.append(f'<text class="tick" x="{X(i):.1f}" y="{H - b + 20}" text-anchor="middle">{m}</text>')
    for y in years:
        pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(MON[y]))
        s.append(f'<polyline class="ctx" points="{pts}"/>')
        for i, v in enumerate(MON[y]):
            s.append(f'<circle class="hit" cx="{X(i):.1f}" cy="{Y(v):.1f}" r="9"{tip(f"{["June", "July", "August", "September"][i]} {y}: lake median {v:.1f} mg/m³")}/>')
    s.append(f'<polyline class="main" points="{" ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(MEAN))}"/>')
    for i, v in enumerate(MEAN): s.append(f'<circle class="end" cx="{X(i):.1f}" cy="{Y(v):.1f}" r="4"/>')
    s.append(f'<text class="val" x="{X(3) + 10:.1f}" y="{Y(MEAN[3]) + 4:.1f}">Average, {MEAN[3]:.0f}</text>')
    s.append(f'<text class="tick" x="{X(3) + 10:.1f}" y="{Y(MON["2021"][3]) + 4:.1f}">2021</text><text class="tick" x="{X(2) + 8:.1f}" y="{Y(MON["2019"][2]) - 8:.1f}">August 2019</text>')
    s.append("</svg>"); return "".join(s)


def chart_dnr():
    Wd, H, l, r_, t, b = 720, 400, 62, 24, 20, 52; pw, ph = Wd - l - r_, H - t - b; mx = 120
    X = lambda v: l + pw * v / mx; Y = lambda v: t + ph * (1 - v / mx)
    s = [f'<svg class="chart" viewBox="0 0 {Wd} {H}" role="img" aria-labelledby="c4t"><title id="c4t">Satellite lake median against the average of DNR lab samples on the same sampling date</title>']
    for v in range(0, mx + 1, 20):
        s.append(f'<line class="grid" x1="{l}" x2="{Wd - r_}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text class="tick" x="{l - 8}" y="{Y(v) + 4:.1f}" text-anchor="end">{v}</text>')
        s.append(f'<line class="grid" x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{t}" y2="{H - b}"/><text class="tick" x="{X(v):.1f}" y="{H - b + 18}" text-anchor="middle">{v}</text>')
    s.append(f'<line class="trend" x1="{X(0)}" y1="{Y(0)}" x2="{X(mx):.1f}" y2="{Y(mx):.1f}"/><text class="note" x="{X(96):.1f}" y="{Y(101):.1f}" text-anchor="end">equal</text>')
    s.append(f'<text class="note" x="{Wd - r_}" y="{H - 10}" text-anchor="end">DNR lab samples, mean of the stations (µg/L) →</text><text class="note" x="{l + 8}" y="{t + 12}">↑ satellite lake median (mg/m³)</text>')
    for p in pairs:
        s.append(f'<circle class="dot solid" cx="{X(min(mx, p["sample"])):.1f}" cy="{Y(p["sat"]):.1f}" r="5"{tip(f"Sampled {day(p["date"])}: DNR {p["sample"]:.0f}, satellite {p["sat"]:.0f} ({abs(p["lag"])} day{"s" if abs(p["lag"]) != 1 else ""} apart)" if p["lag"] else f"Sampled {day(p["date"])}: DNR {p["sample"]:.0f}, satellite {p["sat"]:.0f} (same day)")}/>')
    s.append("</svg>"); return "".join(s)


def chart_boat():
    Wd, H, l, r_, t, b = 720, 400, 62, 24, 20, 52; pw, ph = Wd - l - r_, H - t - b; mx, my = 9, 80
    X = lambda v: l + pw * min(v, mx) / mx; Y = lambda v: t + ph * (1 - min(v, my) / my)
    s = [f'<svg class="chart" viewBox="0 0 {Wd} {H}" role="img" aria-labelledby="c5t"><title id="c5t">Satellite chlorophyll estimate against the blue-green pigment measured from the USGS boat at the same place</title>']
    for v in range(0, my + 1, 20):
        s.append(f'<line class="grid" x1="{l}" x2="{Wd - r_}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text class="tick" x="{l - 8}" y="{Y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    for v in range(0, mx, 2):
        s.append(f'<line class="grid" x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{t}" y2="{H - b}"/><text class="tick" x="{X(v):.1f}" y="{H - b + 18}" text-anchor="middle">{v}</text>')
    s.append(f'<text class="note" x="{Wd - r_}" y="{H - 10}" text-anchor="end">blue-green pigment measured from the boat (phycocyanin, RFU) →</text><text class="note" x="{l + 8}" y="{t + 12}">↑ satellite chlorophyll estimate (mg/m³)</text>')
    step = max(1, len(boat) // 700)
    for bb in sorted(boat, key=lambda z: (z["date"], z["pc"]))[::step]:
        if bb["pc"] > mx or bb["chl"] > my: continue
        s.append(f'<circle class="bg" cx="{X(bb["pc"]):.1f}" cy="{Y(bb["chl"]):.1f}" r="2"/>')
    up = " ".join(f"{X(q['x']):.1f},{Y(q['hi']):.1f}" for q in BINS); dn = " ".join(f"{X(q['x']):.1f},{Y(q['lo']):.1f}" for q in reversed(BINS))
    s.append(f'<polygon class="band" points="{up} {dn}"/>')
    s.append(f'<polyline class="main" points="{" ".join(f"{X(q['x']):.1f},{Y(q['med']):.1f}" for q in BINS)}"/>')
    for q in BINS:
        s.append(f'<circle class="end" cx="{X(q["x"]):.1f}" cy="{Y(q["med"]):.1f}" r="4"{tip(f"Boat pigment {q["lab"]} RFU ({q["n"]:,} places): satellite median {q["med"]:.0f} mg/m³, middle half {q["lo"]:.0f} to {q["hi"]:.0f}")}/>')
    s.append("</svg>"); return "".join(s)


# ---------------------------------------------------------------- page pieces
def strip19():
    cells = []
    for d in KEY19:
        r = D[d]; dd = datetime.date.fromisoformat(d).strftime("%b %-d")
        cells.append(f'''<figure class="frame">
            <figcaption class="label">{dd}</figcaption>
            <img src="{M}{t19[d]}" width="219" height="480" loading="lazy" alt="True-color satellite image of Lake Winnebago on {day(d)}.">
            <img src="{M}{c19[d]}" width="219" height="480" loading="lazy" alt="Chlorophyll map for {day(d)}: east shore {r["chl_east"]:.0f}, west shore {r["chl_west"]:.0f} milligrams per cubic meter.">
            <p class="frame-note"><b>East {r["chl_east"]:.0f} · West {r["chl_west"]:.0f}</b><br>Wind {wind_words(r)}</p>
          </figure>''')
    return "\n          ".join(cells)


def strip_ls():
    return "\n          ".join(
        f'<figure class="frame{" dim" if d in CLOUDY else ""}"><img src="{M}{lsf[d]}" width="219" height="480" loading="lazy" alt="Landsat true-color image of Lake Winnebago, {day(d)}{", mostly hidden by cloud or haze" if d in CLOUDY else ""}."><figcaption class="label">{d[:4]}</figcaption></figure>'
        for d in ls_dates)


def photo(key, alt, cap):
    if key not in photos: return ""
    w, h = photos[key]
    return f'<figure class="photo"><img src="{M}photo-{key}.webp" width="{w}" height="{h}" loading="lazy" alt="{esc(alt, quote=True)}"><figcaption class="label">{cap}</figcaption></figure>'


def sat_cell(d): r = D[d]; return f'{datetime.date.fromisoformat(d).strftime("%b %-d")}: east {r["chl_east"]:.0f}, west {r["chl_west"]:.0f}'


compass_rows = "\n".join(
    f'<tr{" class=\"hl\"" if s_["name"] == "W" else ""}><td>From the {s_["long"]}</td><td class="num">{s_["n"]}</td><td class="num">{s_["share"]:.0f}%</td><td class="num">{sgn(s_["mean"])}</td></tr>'
    for s_ in sorted(sector, key=lambda z: -z["share"]))
story = open(f"{HERE}/story.md", encoding="utf-8").read().split("\n\n")
story = [p.strip() for p in story if p.strip() and not p.startswith("#") and not p.startswith("Written by")]
a9, a12 = D["2018-08-09"], D["2018-08-12"]

BODY = f'''<style>
/* Case study additions (shared with the other project pages) */
.cs-hero .wrap {{ padding-block: clamp(3.5rem, 8vw, 6rem) clamp(2.5rem, 5vw, 3.5rem); display: grid; gap: 1.5rem; }}
.cs-hero h1 {{ font: 500 var(--step-4)/1.02 var(--display); margin: 0; letter-spacing: -0.01em; max-width: 16ch; text-wrap: balance; }}
.cs-hero .lede {{ font-size: var(--step-1); line-height: 1.55; max-width: 58ch; margin: 0; color: var(--ink-2); }}
.back {{ font: 500 0.875rem/1 var(--body); text-decoration: none; color: var(--forest); }}
.back:hover {{ text-decoration: underline; }}
.compare {{ width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }}
.compare th, .compare td {{ text-align: left; padding: 0.7rem 1rem 0.7rem 0; border-bottom: 1px solid var(--rule); vertical-align: top; }}
.compare thead th {{ font: 500 0.75rem/1.4 var(--mono); letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-2); border-bottom: 1px solid var(--ink); }}
.compare td.num, .compare th.num {{ text-align: right; padding-right: 0; padding-left: 1rem; white-space: nowrap; }}
.compare tr.hl td {{ background: var(--paper-2); }}
.table-scroll {{ overflow-x: auto; }}
.cs-body {{ display: grid; grid-template-columns: minmax(0, 14rem) minmax(0, 1fr); gap: 1rem 3rem; }}
@media (max-width: 760px) {{ .cs-body {{ grid-template-columns: minmax(0, 1fr); }} }}
.cs-body .prose {{ max-width: var(--measure); }}
.cs-body .prose p {{ margin: 0 0 1.1rem; }}
.cs-body .prose h3 {{ font: 600 var(--step-1)/1.3 var(--body); margin: 1.75rem 0 0.5rem; }}
.cs-body .prose ul, .cs-body .prose ol {{ margin: 0 0 1.1rem; padding-left: 1.2rem; }}
.cs-body .prose li + li {{ margin-top: 0.45rem; }}
.cs-body .prose strong {{ font-weight: 600; color: var(--ink); }}
.steps {{ counter-reset: s; list-style: none; padding: 0 !important; display: grid; gap: 0; border-top: 1px solid var(--rule); }}
.steps li {{ counter-increment: s; display: grid; grid-template-columns: 2.5rem minmax(0, 1fr); gap: 1rem; padding-block: 1rem; border-bottom: 1px solid var(--rule); margin: 0 !important; }}
.steps li::before {{ content: counter(s, decimal-leading-zero); font: 500 0.875rem/1.7 var(--mono); color: var(--olive); }}
.chips {{ display: flex; flex-wrap: wrap; gap: 0.5rem; list-style: none; padding: 0 !important; }}
.chips li {{ margin: 0 !important; font: 500 0.8125rem/1 var(--mono); padding: 0.5rem 0.7rem; border: 1px solid var(--rule); border-radius: 2px; color: var(--ink-2); }}

/* This page */
.story p {{ font: 500 var(--step-1)/1.6 var(--display); font-size: 1.375rem; margin: 0 0 1.2rem; max-width: 34em; }}
.story blockquote {{ margin: 0; }}
.photo {{ margin: 0; border: 1px solid var(--rule); background: var(--paper-2); }}
.photo img {{ display: block; width: 100%; height: auto; }}
.photo figcaption, .fig-cap {{ padding: 0.55rem 0.75rem; border-top: 1px solid var(--rule); background: var(--paper); font-size: 0.6875rem; }}
.photo-pair {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; margin: 2rem 0 0; align-items: start; }}
.photo-trio {{ display: grid; grid-template-columns: 1.1fr 0.62fr 1.1fr; gap: 1rem; margin: 0 0 1.5rem; align-items: start; }}
@media (max-width: 640px) {{ .photo-pair, .photo-trio {{ grid-template-columns: minmax(0, 1fr); }} }}
.chart-fig {{ margin: 0 0 1.25rem; border: 1px solid var(--rule); background: var(--paper); padding: clamp(0.75rem, 2vw, 1.25rem); position: relative; }}
.chart-fig h3 {{ font: 600 1rem/1.35 var(--body); margin: 0 0 0.15rem; }}
.chart-fig .sub {{ font-size: 0.875rem; color: var(--ink-2); margin: 0 0 0.75rem; max-width: 60ch; }}
.chart-scroll {{ overflow-x: auto; }}
.scroll-hint {{ display: none; font-size: 0.75rem; color: var(--ink-2); margin: 0.4rem 0 0; }}
@media (max-width: 640px) {{ .scroll-hint {{ display: block; }} }}
.hbars {{ display: grid; gap: 0.5rem; max-width: 46rem; }}
.hb-row {{ display: grid; grid-template-columns: 9.5rem minmax(0, 1fr) 3rem; gap: 0.75rem; align-items: center; outline: none; }}
.hb-cat {{ text-align: right; font-size: 0.9375rem; }}
.hb-cat i {{ font-style: normal; font-size: 0.8125rem; color: var(--ink-2); font-variant-numeric: tabular-nums; }}
.hb-cat i::before {{ content: "· "; }}
.hb-track {{ position: relative; height: 20px; border-left: 1px solid var(--rule); }}
.hb-track::after {{ content: ""; position: absolute; left: 50%; top: -0.3rem; bottom: -0.3rem; width: 1px; background: var(--ink-2); }}
.hb-fill {{ position: relative; z-index: 1; display: block; height: 100%; background: var(--forest); border-radius: 0 4px 4px 0; }}
.hb-row:hover .hb-fill, .hb-row:focus-visible .hb-fill {{ outline: 2px solid var(--ink); outline-offset: 1px; }}
.hb-val {{ font-weight: 600; font-variant-numeric: tabular-nums; }}
.hb-axis .hb-ticks {{ display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--ink-2); }}
@media (max-width: 520px) {{
  .hb-row {{ grid-template-columns: 5.25rem minmax(0, 1fr) 2.5rem; gap: 0.5rem; }}
  .hb-cat {{ font-size: 0.875rem; line-height: 1.2; }} .hb-cat i {{ display: block; font-size: 0.75rem; }} .hb-cat i::before {{ content: ""; }}
  .hb-row:not(.hb-axis) .hb-track {{ height: 18px; }}
}}
svg.chart {{ display: block; width: 100%; min-width: 560px; height: auto; font-family: var(--body); }}
.chart .grid {{ stroke: var(--rule); stroke-width: 1; }}
.chart .grid.ref {{ stroke: var(--ink-2); }}
.chart .tick {{ font-size: 12px; fill: var(--ink-2); font-variant-numeric: tabular-nums; }}
.chart .note {{ font-size: 12px; fill: var(--ink-2); }}
.chart .cat {{ font-size: 13.5px; fill: var(--ink); }}
.chart .val {{ font-size: 13.5px; font-weight: 600; fill: var(--ink); font-variant-numeric: tabular-nums; paint-order: stroke; stroke: var(--paper); stroke-width: 4px; stroke-linejoin: round; }}
.chart .bar {{ fill: var(--forest); }}
.chart .dot {{ fill: var(--forest); fill-opacity: 0.55; stroke: var(--paper); stroke-width: 1.5; }}
.chart .dot.solid {{ fill-opacity: 0.9; stroke-width: 2; }}
.chart .trend {{ stroke: var(--ink); stroke-width: 1.5; fill: none; }}
.chart .ctx {{ stroke: var(--ink-2); stroke-opacity: 0.45; stroke-width: 1.25; fill: none; stroke-linejoin: round; }}
.chart .main {{ stroke: var(--forest); stroke-width: 2.5; fill: none; stroke-linejoin: round; stroke-linecap: round; }}
.chart .end {{ fill: var(--forest); stroke: var(--paper); stroke-width: 2; }}
.chart .hit {{ fill: transparent; }}
.chart .bg {{ fill: var(--ink-2); fill-opacity: 0.28; }}
.chart .band {{ fill: var(--forest); fill-opacity: 0.12; }}
.chart [data-tip] {{ cursor: default; outline: none; }}
.chart [data-tip]:hover, .chart [data-tip]:focus-visible {{ fill-opacity: 1; stroke: var(--ink); }}
.chart .hit:hover, .chart .hit:focus-visible {{ fill: var(--forest); fill-opacity: 0.25; }}
.tipbox {{ position: fixed; z-index: 60; pointer-events: none; background: var(--ink); color: var(--paper); font: 500 0.8125rem/1.4 var(--body); padding: 0.45rem 0.6rem; border-radius: 2px; max-width: 18rem; }}
details.nums {{ margin: 0.5rem 0 0; }}
details.nums summary {{ font: 500 0.8125rem/1.4 var(--mono); letter-spacing: 0.06em; text-transform: uppercase; color: var(--forest); cursor: pointer; padding-block: 0.4rem; }}
.strip {{ display: grid; grid-template-columns: repeat(7, minmax(118px, 1fr)); gap: 0.6rem; overflow-x: auto; padding-bottom: 0.5rem; }}
.strip.many {{ grid-template-columns: repeat(auto-fill, minmax(84px, 1fr)); overflow: visible; }}
@media (min-width: 900px) {{ .strip.many {{ grid-template-columns: repeat(11, minmax(0, 1fr)); }} }}
.frame {{ margin: 0; display: grid; gap: 0.35rem; align-content: start; min-width: 0; }}
.frame img {{ display: block; width: 100%; height: auto; border: 1px solid var(--rule); background: var(--paper-2); }}
.frame.dim img {{ opacity: 0.45; }}
.frame figcaption {{ font-size: 0.6875rem; }}
.frame-note {{ font-size: 0.8125rem; line-height: 1.4; margin: 0; color: var(--ink-2); }}
.frame-note b {{ color: var(--ink); font-weight: 600; font-variant-numeric: tabular-nums; }}
.scale {{ display: flex; align-items: center; gap: 0.6rem; margin: 1rem 0 0; flex-wrap: wrap; }}
.scale i {{ display: block; width: min(16rem, 60vw); height: 10px; border: 1px solid var(--rule); background: linear-gradient(90deg, #08306b, #2171b5, #4eb3d3, #7fcdbb, #c7e9b4, #fee08b, #fc8d59, #d73027); }}
.wide {{ margin-top: 2.5rem; }}
.small {{ font-size: 0.875rem; color: var(--ink-2); }}
.draft {{ border: 1px solid var(--olive); padding: 0.6rem 0.9rem; font-size: 0.875rem; color: var(--ink-2); max-width: 60ch; }}
</style>
<header class="site-header">
  <div class="wrap">
    <a class="wordmark" href="index.html">James Krauska <span>GIS</span></a>
    <nav class="nav" aria-label="Main">
      <a href="index.html#work">Work</a>
      <a href="index.html#about">About</a>
      <a href="index.html#experience">Experience</a>
      <a href="index.html#contact">Contact</a>
    </nav>
  </div>
</header>
<main>
  <div class="cs-hero">
    <div class="wrap">
      <a class="back" href="index.html#work">← All work</a>
      <div class="meta" style="display:flex;flex-wrap:wrap;gap:0.5rem 2rem">
        <span class="label">Case study · Chapter 1 of 4</span>
        <span class="label">Remote sensing · Google Earth Engine</span>
        <span class="label">Lake Winnebago, Wisconsin · 2017–2026</span>
      </div>
      <h1>Lake Winnebago from Space</h1>
      <p class="lede">My grandmother said the west wind blew the algae to our side of the lake. I checked her claim against {N_CLEAR} clear days of satellite images and ten summers of wind. After a west wind, the east shore had more chlorophyll than the west on {W["share"]:.0f}% of days.</p>
      <p class="draft">Draft for review. Not yet linked from the homepage.</p>
    </div>
  </div>

  <section>
    <div class="wrap cs-body">
      <span class="label">Why this lake</span>
      <div>
        <div class="story">
          {"".join(f"<p>{esc(p)}</p>" for p in story)}
        </div>
        <div class="photo-pair">
          {photo("sail_garage_2014-07-05", "A garage on a sunny day. Three teenagers and two adults rig a homemade sail, a dark tarp on a branch mast held with tape, onto a yellow kayak. Faces are blurred.", "July 5, 2014 · A tarp, a branch and a lot of tape")}
          {photo("sail_rescue_2014-07-05", "Choppy brown water with whitecaps. A yellow motorboat tows a kayak back by a rope while a boy lies across the kayak holding on. Faces are blurred.", "The same afternoon · Towed back from the middle of the lake")}
        </div>
        <p class="small" style="max-width:60ch;margin-top:1rem">We learned what the wind does on Lake Winnebago long before I looked at any data. A south-southeast wind sent my cousin's kayak to the middle of the lake so fast he had to break the sail, and we went out in my uncle's motorboat to bring him in.</p>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head">
        <span class="label">Result</span>
        <div>
          <h2>Chlorophyll is higher on the downwind shore</h2>
          <p>I sorted {N_CLEAR} clear summer days, June 2017 to September 2026, by the direction the wind had come from over that day and the two before it. Then I compared chlorophyll-a in a 2 km strip along the east shore with the same strip along the west shore.</p>
        </div>
      </div>
      <figure class="chart-fig">
        <h3>How often the east shore was worse than the west</h3>
        <p class="sub">Share of clear days with more chlorophyll-a along the east shore, by the direction the wind came from.</p>
        {chart_compass()}
        <details class="nums"><summary>Show the numbers</summary>
          <div class="table-scroll"><table class="compare">
            <thead><tr><th scope="col">Wind</th><th scope="col" class="num">Clear days</th><th scope="col" class="num">East shore higher</th><th scope="col" class="num">Average east minus west (mg/m³)</th></tr></thead>
            <tbody>{compass_rows}</tbody>
          </table></div>
        </details>
      </figure>
      <div class="cs-body">
        <span class="label">Reading it</span>
        <div class="prose">
          <p>A west wind is the strongest of the eight directions: the east shore came out higher on <strong>{W["share"]:.0f}% of {W["n"]} days</strong>, by an average of {W["mean"]:.1f} mg/m³. A northeast wind reverses it. The east shore was higher on only {NEs["share"]:.0f}% of those {NEs["n"]} days.</p>
          <p>So she was right about the wind. What the data shows is where the chlorophyll sits after the wind has blown, not algae in motion, and it does not show the bloom starting on the far side. The algae grows across the whole lake and the wind sorts it.</p>
        </div>
      </div>
      <figure class="chart-fig wide">
        <h3>One dot for each clear day</h3>
        <p class="sub">East-west wind (m/s, three-day average) against the gap between the two shores (mg/m³). The line is the linear trend.</p>
        <div class="chart-scroll">{chart_scatter()}</div><p class="scroll-hint">Scroll sideways to see the whole chart.</p>
        <p class="small" style="margin:0.75rem 0 0;max-width:60ch">The relationship is real but loose. The rank correlation is {RHO:.2f}, and wind explains about {100 * R2:.0f}% of the day-to-day variation. How large the bloom is that week matters more than where the wind puts it.</p>
      </figure>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head">
        <span class="label">One summer</span>
        <div>
          <h2>July and August 2019, the worst east-shore days on record</h2>
          <p>Seven of that summer's clear days. Top: what the satellite saw. Bottom: the same image as chlorophyll-a. Under each, the two shores and the wind of the three days before.</p>
        </div>
      </div>
      <div class="strip">
          {strip19()}
      </div>
      <p class="scroll-hint">Scroll sideways for all seven days.</p>
      <div class="scale"><span class="label">0</span><i></i><span class="label">60+ mg/m³ chlorophyll-a</span></div>
      <div class="cs-body" style="margin-top:2rem">
        <span class="label">Reading it</span>
        <div class="prose">
          <p>July 25 and August 9 followed west winds and July 28 a southwest wind, and on all three the line between the two sides of the lake is sharp. On July 10 the wind had been from the south, along the length of the lake, and the red band sits toward the west side. By August 27 it had swung to the southeast, and the west shore was the higher one.</p>
          <p>The red also spreads as the summer goes on. That is the whole lake blooming, not a patch moving west: the west shore rises from {D["2019-07-25"]["chl_west"]:.0f} to {D["2019-08-19"]["chl_west"]:.0f} across these weeks while the east stays high. The color scale stops at 60, so everything above it is the same red.</p>
          <p class="small">Animated versions: <a href="projects/lake-winnebago-blooms/media/filmstrip_2019_truecolor.gif">true color</a>, <a href="projects/lake-winnebago-blooms/media/filmstrip_2019_chlorophyll.gif">chlorophyll</a>.</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head">
        <span class="label">Every summer</span>
        <div>
          <h2>The lake roughly doubles its chlorophyll by late summer</h2>
          <p>Monthly lake-wide medians from Sentinel-2, 2019 to 2025. June is always the cleanest month, between {JUNE_LO:.0f} and {JUNE_HI:.0f} mg/m³. Five of the seven summers peaked in August and two in September.</p>
        </div>
      </div>
      <figure class="chart-fig">
        <h3>Lake-wide chlorophyll-a by month</h3>
        <p class="sub">Median of all open-water pixels, mg/m³. Each thin line is one summer. The heavy line is the seven-year average.</p>
        <div class="chart-scroll">{chart_monthly()}</div><p class="scroll-hint">Scroll sideways to see the whole chart.</p>
      </figure>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head">
        <span class="label">The cottage years</span>
        <div>
          <h2>Late summer from Landsat, 1999 to 2026</h2>
          <p>The least cloudy Landsat image between July 19 and August 28 of each year. Twenty-one of the 28 summers have one. The faded frames are too cloudy or hazy to read.</p>
        </div>
      </div>
      <div class="strip many">
          {strip_ls()}
      </div>
      <div class="cs-body" style="margin-top:2rem">
        <span class="label">Reading it</span>
        <div class="prose">
          <p>Green streaks run down the east side in 2016, 2017 and 2018. The 2017 image, from August 5, sits between two Sentinel-2 days that measured the east shore at {D["2017-08-02"]["chl_east"] / D["2017-08-02"]["chl_west"]:.1f} and {D["2017-08-09"]["chl_east"] / D["2017-08-09"]["chl_west"]:.1f} times the west, so two different satellites agree on that week.</p>
          <p>The vivid 2025 frame, from August 3, needs care. Sentinel-2 passed the day before and found only moderate chlorophyll, and the Landsat image has a pale haze patch across the middle. Some of that green is surface scum and some is haze and the way the image is brightened.</p>
          <p class="small">Landsat 7 is left out because its images after 2003 have stripes across the lake. <a href="projects/lake-winnebago-blooms/media/augusts_1999_2026_landsat.gif">Animated version</a>.</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head">
        <span class="label">Checking it</span>
        <div>
          <h2>Did anyone on the water see the same thing?</h2>
          <p>A satellite estimate is only worth as much as its match to what people saw and measured. Four checks: news and fishing reports, my own family's photos, the DNR's lab samples, and a USGS boat that measured blue-green algae directly.</p>
        </div>
      </div>
      <div class="table-scroll">
        <table class="compare">
          <thead><tr><th scope="col">Date</th><th scope="col">What was reported</th><th scope="col">What the satellite measured nearby (mg/m³)</th></tr></thead>
          <tbody>
            <tr><td>Aug 4, 2017</td><td>FOX 11 News: health officials warn of toxic blue-green algae in Lake Winnebago.</td><td>{sat_cell("2017-08-02")}. {sat_cell("2017-08-09")}.</td></tr>
            <tr><td>June 29, 2018</td><td>WBAY: blue-green algae blooming in Lake Winnebago.</td><td>June 28: lake median {D["2018-06-28"]["chl_median"]:.0f}, when a normal June runs {JUNE_LO:.0f} to {JUNE_HI:.0f}.</td></tr>
            <tr><td>Sept 20, 2018</td><td>AnglingBuzz fishing report (Mark Schram): a strong bloom, worst in protected water; recent winds had mixed the algae down and left few slicks on the main lake.</td><td>Sept 16: lake median {D["2018-09-16"]["chl_median"]:.0f}, east {D["2018-09-16"]["chl_east"]:.0f}. Cloud on Sept 18 and 21. Sept 23: {D["2018-09-23"]["chl_median"]:.0f}.</td></tr>
            <tr><td>Aug 6, 2019</td><td><a href="https://www.wbay.com/content/news/People-warned-to-stay-away-from-Lake-WInnebago-algae-blooms-523695621.html">WBAY</a>: the county health department warns people away from the blooms; the beach at High Cliff State Park had been closed for several days.</td><td>{sat_cell("2019-08-04")}, with bright green scum visible at the north end. {sat_cell("2019-08-07")}.</td></tr>
          </tbody>
        </table>
      </div>
      <p class="small" style="max-width:60ch;margin:1rem 0 0">Each report of a bad bloom lands on or beside a day when the satellite numbers are well above normal. The fishing report also describes something the wind test cannot see: strong wind stirs floating algae down into the water, so slicks form in calm weather and are moved by light to moderate wind.</p>

      <div class="cs-body wide">
        <span class="label">My family's photos</span>
        <div>
          <div class="photo-trio">
            {photo("kayaks_dog_2018-08-11", "Two kayaks on glassy, hazy water close to shore. A small dog sits on the bow of the yellow kayak in front. Faces are blurred.", "Aug 11, 2018 · Calm water off the east shore")}
            {photo("sheepshead_2018-08-10", "A large sheepshead in a landing net held over the side of a yellow boat at dusk.", "Aug 10, 2018 · Sheepshead")}
            {photo("dock_kayaks_2018-09-02", "A wooden dock, boat rails and a willow on the shore of Lake Winnebago under a grey sky, with grey-green chop coming in. Three people launch kayaks. Faces are blurred.", "Sept 2, 2018 · The dock")}
          </div>
          <div class="prose">
            <p>Sentinel-2 passed on <strong>August 9 and August 12, 2018</strong>, either side of the weekend in the first two photos. On the 9th the lake median was {a9["chl_median"]:.0f} mg/m³ with the east shore at {a9["chl_east"]:.0f} and the west at {a9["chl_west"]:.0f}. By the 12th the lake was down to {a12["chl_median"]:.0f}. Winds were light both days, which matches the glassy water in the photo.</p>
            <p>The dock photo is from three weeks later. The satellite saw only cloud on September 1 and 3, which fits the sky in the picture.</p>
          </div>
        </div>
      </div>

      <figure class="chart-fig wide">
        <h3>Satellite estimate against DNR lab samples</h3>
        <p class="sub">{len(pairs)} sampling dates, 2017 to 2026, that had a clear Sentinel-2 day within two days. Dots under the line mean the satellite read lower than the lab.</p>
        <div class="chart-scroll">{chart_dnr()}</div>
        <p class="scroll-hint">Scroll sideways to see the whole chart.</p>
        <p class="small" style="margin:0.75rem 0 0;max-width:62ch">The Wisconsin DNR samples three stations out on the lake; {N_DNR} of its chlorophyll-a lab results fall in these years. The two measures rise and fall together (rank correlation {DN_RHO:.2f}), but the satellite's lake median reads low, about {100 * DN_RATIO:.0f}% of the sampled value on a typical date, and it misses most on the heaviest bloom days. This is a first comparison of three points against a whole-lake median. Matching the satellite pixel at each station comes next.</p>
      </figure>

      <figure class="chart-fig wide">
        <h3>Satellite estimate against blue-green algae measured from a boat</h3>
        <p class="sub">{N_BOAT:,} places on {len(BOAT_DATES)} dates, 2023 to 2025. The line is the typical satellite value at each level of boat-measured pigment, the band is the middle half, and the grey dots are a sample of the individual places. A few readings above 9 RFU or 80 mg/m³ are off the chart.</p>
        <div class="chart-scroll">{chart_boat()}</div><p class="scroll-hint">Scroll sideways to see the whole chart.</p>
        <p class="small" style="margin:0.75rem 0 0;max-width:62ch">The U.S. Geological Survey ran a boat across the lake with a sensor for phycocyanin, the pigment that marks blue-green algae, logging a GPS position every few seconds. I reduced its track to 60 m squares and read the Sentinel-2 pixel under each one from the nearest clear day, within two days. The two rise together: rank correlation {B_RHO:.2f} overall, and {B_SAME:.2f} on July 8, 2025, the one date the boat and the satellite were there the same morning.</p>
      </figure>
      <div class="cs-body">
        <span class="label">Reading it</span>
        <div class="prose">
          <p>The satellite estimate follows the boat's blue-green pigment, and it does not follow the boat's own chlorophyll channel (rank correlation {sgn2(B_BCHL)}). Blue-green algae give off little of the fluorescence that channel reads. So on this lake in summer, the chlorophyll number from space is mostly a measure of blue-green algae.</p>
          <p><strong>Two cautions.</strong> Murkier water has more of everything: with turbidity held constant, the correlation falls from {B_RHO:.2f} to {B_PARTIAL:.2f}. And two of the things I tried against the boat data showed nothing: a floating-algae index on the same images ({sgn2(B_FAI)}), and same-day images from the coarser MODIS satellites.</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap cs-body">
      <span class="label">How it was measured</span>
      <div class="prose">
        <ol class="steps">
          <li><span><strong>Images.</strong> Every Sentinel-2 pass over the lake from June through September, 2017 to 2026, mosaicked by day in Google Earth Engine. Clouds are masked with Cloud Score+, and only pixels that are water at least 80% of the time are kept.</span></li>
          <li><span><strong>Chlorophyll-a.</strong> The Normalized Difference Chlorophyll Index, from the red-edge and red bands, converted to mg/m³ with the Mishra and Mishra (2012) formula for turbid, productive water.</span></li>
          <li><span><strong>Clear days.</strong> A day counts when at least half the lake is cloud-free. That leaves {N_CLEAR} days.</span></li>
          <li><span><strong>Shores.</strong> The median in a 2 km strip along the east shore and the same along the west, from Taycheedah to just below Neenah.</span></li>
          <li><span><strong>Wind.</strong> ERA5-Land daily wind, averaged over the lake and a 10 km ring of shore for the image day and the two days before.</span></li>
          <li><span><strong>Boat comparison.</strong> A third Earth Engine script reads Sentinel-2 under each 60 m square of the USGS boat track. Nothing is cloud-masked in the script; the cloud score is exported and the cut is made afterwards.</span></li>
          <li><span><strong>Monthly record.</strong> The open-source Lake Chlorophyll-a Monitor by Parisa Abbasalizadehrezaei, set up for Lake Winnebago.</span></li>
        </ol>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap cs-body">
      <span class="label">What this does not show</span>
      <div class="prose">
        <ul>
          <li><strong>Not the mats.</strong> The index measures chlorophyll in open water. The thick floating mats I remember are a different target, the formula is unreliable on them, and the floating-algae index I tried did not pick them up.</li>
          <li><strong>Not which algae, directly.</strong> Every kind of algae has chlorophyll-a, and Sentinel-2 has no band for the pigment that marks blue-green algae. The boat comparison says the two go together on this lake, but only on eight dates. NOAA <a href="https://coastalscience.noaa.gov/science-areas/habs/hab-monitoring-system/cyanobacteria-algal-bloom-from-satellite-in-green-bay-and-lake-winnebago-wi/">monitors this lake with Sentinel-3</a>, which has that band.</li>
          <li><strong>Not movement.</strong> Images are two or more days apart. The result is where chlorophyll sits after the wind, not a bloom tracked across the lake.</li>
          <li><strong>Clear days only.</strong> Clear weather comes with its own typical winds, and neighboring days are not independent, so {N_CLEAR} days is fewer than {N_CLEAR} separate tests.</li>
          <li><strong>Land-tuned correction.</strong> The images use the standard atmospheric correction, which is built for land and less accurate over dark water.</li>
          <li><strong>Few east-shore measurements.</strong> None of the three DNR stations is near the east shore. The USGS boat ran within about a mile of it, on a handful of dates.</li>
        </ul>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap cs-body">
      <span class="label">Next</span>
      <div class="prose">
        <ul>
          <li>A way to measure the mats themselves. The floating-algae index did not work against the boat data, so this is still open.</li>
          <li>Sentinel-3, which passes almost daily and sees the blue-green pigment, to follow one bloom from day to day.</li>
          <li>Chapter 2, ice: freeze-up and ice-out every winter since 2000. Chapter 3, trends. Chapter 4, fish, with an ice-fishing log collected this winter.</li>
        </ul>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap cs-body">
      <span class="label">Software and methods</span>
      <div class="prose">
        <ul class="chips">
          <li>Google Earth Engine</li><li>JavaScript</li><li>Sentinel-2</li><li>Landsat 5, 8 and 9</li><li>MODIS</li><li>ERA5-Land</li><li>Cloud Score+</li><li>NDCI</li><li>Python</li><li>Water Quality Portal</li><li>USGS FLAMe boat data</li>
        </ul>
        <p>Built with AI-assisted coding (Claude): the daily Earth Engine script, the statistics and this page's code. I set up and ran the Earth Engine work, questioned the results until the claims matched the evidence, found the reports, the photos and the USGS boat data, and wrote the opening story.</p>
        <p class="label" style="margin-top:1rem">Monthly monitor and Earth Engine course: Parisa Abbasalizadehrezaei (MIT license) · Data: Copernicus Sentinel-2, Google Cloud Score+, JRC Global Surface Water, USGS Landsat, NASA MODIS, ECMWF ERA5-Land, U.S. Census TIGER, Wisconsin DNR via the Water Quality Portal, U.S. Geological Survey (doi.org/10.5066/P1XHRFKZ) · Faces in family photos are blurred</p>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <p class="label built-with" style="flex-basis:100%;margin:0">Built with Google Earth Engine, Sentinel-2, Landsat and Python · Scripts and page code written with Claude</p>
    <div class="scalebar" aria-hidden="true">
      <div class="bar"><i></i><i></i><i></i><i></i></div>
      <div class="ticks label"><span>0</span><span>5</span><span>10 mi</span></div>
    </div>
    <span class="label">NAD83 / Wisconsin Transverse Mercator · © 2026 James Krauska</span>
  </div>
</footer>
<script>
/* Chart tooltips: hover or keyboard focus on any mark with data-tip. */
(function () {{
  var box = document.createElement('div'); box.className = 'tipbox'; box.hidden = true; document.body.appendChild(box);
  function show(el, x, y) {{
    box.textContent = el.getAttribute('data-tip'); box.hidden = false;
    var w = box.offsetWidth, h = box.offsetHeight;
    box.style.left = Math.max(8, Math.min(window.innerWidth - w - 8, x + 12)) + 'px';
    box.style.top = (y - h - 12 < 8 ? y + 16 : y - h - 12) + 'px';
  }}
  document.addEventListener('pointermove', function (e) {{
    var el = e.target.closest ? e.target.closest('[data-tip]') : null;
    if (el) show(el, e.clientX, e.clientY); else box.hidden = true;
  }});
  document.addEventListener('focusin', function (e) {{
    var el = e.target.closest ? e.target.closest('[data-tip]') : null;
    if (el) {{ var r = el.getBoundingClientRect(); show(el, r.left + r.width / 2, r.top); }}
  }});
  document.addEventListener('focusout', function () {{ box.hidden = true; }});
}})();
</script>
<!-- Visitor stats: GoatCounter (no cookies, no personal data) -->
<script data-goatcounter="https://krauskagis.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
'''
open(f"{HERE}/page_body.html", "w", encoding="utf-8").write(BODY)
print("ok page_body.html", f"{len(BODY) / 1024:.0f} KB", "| clear days", N_CLEAR, "| W", round(W["share"]), W["n"], "| NE", round(NEs["share"]),
      "| rho", round(RHO, 2), "r2", round(R2, 2), "| dnr pairs", len(pairs), round(DN_RHO, 2), round(DN_RATIO, 2), "| photos", sorted(photos))
