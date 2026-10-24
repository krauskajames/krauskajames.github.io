"""One-page County Board memo (HTML) from data/winnebago/profile.json. Print to PDF with print_memo.js.
Usage: python3 memo.py ../../data/winnebago memo.html FONT_DIR
"""
import json, sys, os

DATA, OUT, FONTS = sys.argv[1], sys.argv[2], sys.argv[3]
P = json.load(open(os.path.join(DATA, "profile.json")))
G = json.load(open(os.path.join(DATA, "municipalities.geojson")))
c = P["county"]; s = c["series"]; w = c["wi"]; acs = c["acs"]; acw = c["acs_wi"]; comp = c["components"]
econ = c["econ"]; tot = econ["totals"]; cm = c["commute"]; hu = c["housing_units"]
mfg = next(r for r in econ["rows"] if r["line"] == 500)
con = next(r for r in econ["rows"] if r["line"] == 400)
munis = sorted([f["properties"] for f in G["features"]], key=lambda p: -p["chg20_26"])
clay = next(p for p in munis if p["short"] == "Clayton")
pop26, pop20 = s["e2026"], s["c2020"]
f0 = lambda n: f"{round(n):,}"
pc = lambda x, d=1: f"{x * 100:.{d}f}%"
sp = lambda x, d=1: ("+" if x > 0 else "−" if x < 0 else "") + f"{abs(x) * 100:.{d}f}%"
si = lambda x: ("+" if x > 0 else "−" if x < 0 else "") + f"{abs(round(x)):,}"

# extrapolation: modified exponential through 2000/2010/2020 (as on the web page)
Y = [s["c2000"], s["c2010"], s["c2020"]]
b = (Y[2] - Y[1]) / (Y[1] - Y[0]); a = (Y[1] - Y[0]) / (b - 1); cc = Y[0] - a
me = lambda yr: cc + a * b ** ((yr - 2000) / 10)

# ---- chart (SVG)
W, H = 300, 135
pad = dict(l=34, r=46, t=8, b=18)
hist = [(y, s[f"c{y}"]) for y in (1970, 1980, 1990, 2000, 2010, 2020)] + [(y, s[f"e{y}"]) for y in range(2021, 2027)]
mine = [(y, me(y)) for y in range(2000, 2051)]
doa = [(y, c["proj"][str(y)]) for y in (2020, 2030, 2040, 2050)]
lo, hi = 120000, 180000
X = lambda yr: pad["l"] + (yr - 1970) / 80 * (W - pad["l"] - pad["r"])
Yv = lambda v: pad["t"] + (1 - (v - lo) / (hi - lo)) * (H - pad["t"] - pad["b"])
path = lambda pts: "M" + "L".join(f"{X(x):.1f},{Yv(v):.1f}" for x, v in pts)
grid = "".join(f'<line x1="{pad["l"]}" x2="{W - pad["r"]}" y1="{Yv(v):.1f}" y2="{Yv(v):.1f}" stroke="#d3d7c8" stroke-width=".6"/>'
               f'<text x="{pad["l"] - 4}" y="{Yv(v) + 3:.1f}" text-anchor="end" class="ax">{v // 1000}k</text>' for v in range(lo, hi + 1, 20000))
xt = "".join(f'<text x="{X(y):.1f}" y="{H - 5}" text-anchor="middle" class="ax">{y}</text>' for y in (1970, 1990, 2010, 2030, 2050))
svg = f'''<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Population 1970-2050">
<rect x="{X(2026):.1f}" y="{pad["t"]}" width="{X(2050) - X(2026):.1f}" height="{H - pad["t"] - pad["b"]}" fill="#eceee5"/>
{grid}{xt}
<path d="{path(doa)}" fill="none" stroke="#c0662a" stroke-width="1.6" stroke-dasharray="4 3"/>
<path d="{path(mine)}" fill="none" stroke="#3d6fb0" stroke-width="2" stroke-dasharray="0.5 3" stroke-linecap="round"/>
<path d="{path(hist)}" fill="none" stroke="#2f7a4b" stroke-width="1.8"/>
<circle cx="{X(2026):.1f}" cy="{Yv(pop26):.1f}" r="2.6" fill="#2f7a4b"/>
<text x="{X(2050) + 4:.1f}" y="{Yv(me(2050)) + 2:.1f}" class="dl" fill="#3d6fb0">Trend {round(me(2050) / 1000)}k</text>
<text x="{X(2050) + 4:.1f}" y="{Yv(c["proj"]["2050"]) + 3:.1f}" class="dl" fill="#c0662a">DOA {round(c["proj"]["2050"] / 1000)}k</text>
</svg>'''

old = lambda yr: sum(r["f"][str(yr)] + r["m"][str(yr)] for r in c["pyramid"] if r["age"][:2] in ("65", "70", "75", "80", "85")) / sum(r["f"][str(yr)] + r["m"][str(yr)] for r in c["pyramid"])

rows = [
    ("Residents, Jan 1, 2026", f0(pop26), f"{sp((pop26 - pop20) / pop20)} since 2020"),
    ("DOA projection, 2050", f0(c["proj"]["2050"]), f"{sp((c['proj']['2050'] - pop20) / pop20)} from 2020"),
    ("Age 65 and older", pc(old(2020), 0) + " → " + pc(old(2050), 0), "2020 to 2050"),
    ("Median household income", f"${f0(acs['med_income'])}", f"WI ${f0(acw['med_income'])}"),
    ("Median home value", f"${f0(acs['med_value'])}", f"WI ${f0(acw['med_value'])}"),
    ("Jobs, 2022", f0(tot["emp2022"]), f"{sp(tot['emp2022'] / tot['emp2012'] - 1)} since 2012 (BEA)"),
    ("Net in-commuters", si(cm["inflow_total"] - cm["outflow_total"]), f"{f0(cm['inflow_total'])} in, {f0(cm['outflow_total'])} out"),
]
table = "".join(f"<tr><th>{a}</th><td class='n'>{b}</td><td>{c_}</td></tr>" for a, b, c_ in rows)

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Winnebago County profile memo</title>
<style>
@font-face {{ font-family: "Cormorant Garamond"; font-weight: 600; src: url("{FONTS}/cormorant-garamond/files/cormorant-garamond-latin-600-normal.woff2"); }}
@font-face {{ font-family: "Public Sans"; font-weight: 400; src: url("{FONTS}/public-sans/files/public-sans-latin-400-normal.woff2"); }}
@font-face {{ font-family: "Public Sans"; font-weight: 600; src: url("{FONTS}/public-sans/files/public-sans-latin-600-normal.woff2"); }}
@font-face {{ font-family: "IBM Plex Mono"; font-weight: 500; src: url("{FONTS}/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2"); }}
@page {{ size: letter; margin: 0.5in 0.6in 0.45in; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font: 400 9pt/1.36 "Public Sans", sans-serif; color: #1b241d; }}
h1 {{ font: 600 25pt/1 "Cormorant Garamond", serif; letter-spacing: .04em; margin: 0 0 6pt; color: #2e4a34; }}
.hdr {{ display: grid; grid-template-columns: 5.2em 1fr; gap: 1pt 8pt; margin: 0; padding-bottom: 6pt; border-bottom: 1.2pt solid #1b241d; }}
.hdr dt {{ font: 500 7.4pt/1.7 "IBM Plex Mono", monospace; letter-spacing: .06em; text-transform: uppercase; color: #4c5a4f; }}
.hdr dd {{ margin: 0; }}
.notice {{ font-size: 7.4pt; color: #4c5a4f; margin: 4pt 0 8pt; }}
h2 {{ font: 600 9.6pt/1.2 "Public Sans", sans-serif; margin: 7pt 0 2pt; color: #2e4a34; }}
p {{ margin: 0 0 5pt; }}
ul {{ margin: 0 0 4pt; padding-left: 12pt; }} li {{ margin: 0 0 2.5pt; }}
.grid {{ display: grid; grid-template-columns: 1.08fr 1fr; gap: 14pt; align-items: start; }}
table {{ width: 100%; border-collapse: collapse; font-size: 8.3pt; }}
th, td {{ text-align: left; padding: 2.6pt 4pt 2.6pt 0; border-bottom: .5pt solid #c7ccbb; vertical-align: top; font-weight: 400; }}
th {{ color: #4c5a4f; }} td.n {{ font-weight: 600; white-space: nowrap; text-align: right; padding-right: 8pt; }}
.cap {{ font: 500 7pt/1.3 "IBM Plex Mono", monospace; letter-spacing: .05em; text-transform: uppercase; color: #4c5a4f; margin: 0 0 3pt; }}
.ax {{ font: 500 6.5px "IBM Plex Mono", monospace; fill: #4c5a4f; }} .dl {{ font: 600 7.5px "Public Sans", sans-serif; }}
.key {{ font-size: 7.2pt; color: #4c5a4f; margin: 2pt 0 0; }} .key b {{ font-weight: 600; }}
.foot {{ margin-top: 8pt; padding-top: 4pt; border-top: .5pt solid #c7ccbb; font-size: 6.9pt; color: #4c5a4f; line-height: 1.35; }}
</style></head><body>
<h1>MEMORANDUM</h1>
<dl class="hdr">
<dt>Date</dt><dd>October 24, 2026</dd>
<dt>To</dt><dd>Winnebago County Board of Supervisors</dd>
<dt>From</dt><dd>James Krauska, GIS analyst</dd>
<dt>Subject</dt><dd>Demographic and economic profile of Winnebago County, Wisconsin</dd>
</dl>
<p class="notice">Independent portfolio sample prepared from public data. Not an official Winnebago County document. Interactive version: krauskagis.com/winnebago.html</p>

<div class="grid">
<div>
<h2>1. Population is growing slowly, entirely through migration</h2>
<p>The Wisconsin DOA estimates {f0(pop26)} residents on January 1, 2026, up {f0(pop26 - pop20)} ({sp((pop26 - pop20) / pop20)}) from the 2020 Census, compared with {sp((w['e2026'] - w['c2020']) / w['c2020'])} statewide. Deaths ({f0(comp['deaths'])}) outnumbered births ({f0(comp['births'])}), so all of the gain came from net in-migration of {f0(comp['migration'])} people. The Town of Clayton alone added {f0(clay['chg20_26'])} residents ({sp(clay['pct20_26'], 0)}), about {pc(clay['chg20_26'] / (pop26 - pop20), 0)} of the county's growth; the City of Menasha and Town of Neenah lost population.</p>
<h2>2. The official projection may understate the county</h2>
<p>DOA's Vintage 2024 projection has the county falling to {f0(c['proj']['2050'])} by 2050, but the 2026 estimate already exceeds DOA's projection for 2030 ({f0(c['proj']['2030'])}). Trend curves fitted to the 2000–2020 censuses (modified exponential, Gompertz and logistic) level off near {round(me(2050) / 1000)},000 and came within about 1,500 of the 2026 estimate. A stable population that is aging is a more likely planning case than decline: residents 65 and older are projected to rise from {pc(old(2020), 0)} to {pc(old(2050), 0)} of the total.</p>
</div>
<div>
<p class="cap">Population, 1970–2050</p>
{svg}
<p class="key"><b style="color:#2f7a4b">━</b> Census and DOA estimates &nbsp;<b style="color:#3d6fb0">┅</b> Trend (2000–20 base) &nbsp;<b style="color:#c0662a">╍</b> DOA projection</p>
<p class="cap" style="margin-top:8pt">Key figures</p>
<table>{table}</table>
</div>
</div>

<h2>3. A manufacturing base that is shrinking, with growth elsewhere</h2>
<p>Manufacturing provides {f0(mfg['emp2022'])} jobs, {pc(mfg['share'], 0)} of the county total and {mfg['lq_us']:.1f} times its national share (location quotient). By the excess-employment method about {f0(round(tot['basic'], -2))} jobs are basic, for an economic base multiplier of {tot['multiplier']:.1f}. Manufacturing lost {f0(-mfg['chg'])} jobs from 2012 to 2022; shift-share attributes {f0(-mfg['rs'])} of that loss to local competitive factors rather than national or industry trends. Construction ({si(con['chg'])}), transportation and warehousing, finance and real estate grew. The county is a regional job center: {f0(cm['inflow_total'])} workers commute in, mostly from Outagamie, Calumet and Fond du Lac counties, against {f0(cm['outflow_total'])} who commute out.</p>
<h2>4. Housing costs less than the state average, but many renters are stretched</h2>
<p>Housing units grew {sp((hu['2026'] - hu['2020']) / hu['2020'])} from 2020 to 2026, faster than population. The median home value (${f0(acs['med_value'])}) is {pc(1 - acs['med_value'] / acw['med_value'], 0)} below the state's, and median rent is ${f0(acw['med_rent'] - acs['med_rent'])} a month lower, yet {pc(acs['rent_burden'], 0)} of renter households pay 30% or more of income for housing (Wisconsin {pc(acw['rent_burden'], 0)}).</p>
<h2>Considerations for the Board</h2>
<ul>
<li>Plan for a stable-to-growing population in comprehensive plan updates, using the DOA projection as a low scenario.</li>
<li>Prepare for an older population: senior housing, transportation and services, especially in towns where a quarter or more of residents are already 65+.</li>
<li>Coordinate workforce and transportation planning with Outagamie, Calumet and Fond du Lac counties, which supply most in-commuters.</li>
</ul>
<p class="foot">Sources: Wisconsin DOA Demographic Services Center (final 1/1/2026 estimates; components of change; housing unit estimates; Vintage 2024 projections). U.S. BEA CAEMP25N, 2012 and 2022. U.S. Census Bureau ACS 5-year 2020–2024 and LEHD LODES 8, 2023. Methods follow UW–Stevens Point GEOG 330 extrapolation, location quotient and shift-share techniques.</p>
</body></html>'''
open(OUT, "w").write(html)
print("ok")
