"""Winnebago County Community Profile: data pipeline.

Downloads are fetched by fetch_raw.sh into RAW (not committed). This script turns them into
the small JSON files the web page reads (data/winnebago/).

Sources
  Wisconsin DOA Demographic Services Center: municipal (MCD) time series 1970-2026,
    final 1/1/2026 estimates, components of change, housing units, Vintage 2024 projections.
  U.S. BEA CAEMP25N: total full- and part-time employment by NAICS industry, 2001-2022.
  U.S. BEA CAINC1: per capita personal income, 1969-2024.
  U.S. Census Bureau LEHD LODES 8 (2023): origin-destination and workplace area files.
  U.S. Census Bureau TIGERweb: county subdivisions, counties, areal hydrography.
  U.S. Census Bureau ACS 5-year (optional, acs.json from fetch_acs.py).
"""
import csv, gzip, io, json, math, os, sys
from collections import defaultdict
import openpyxl
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

RAW = sys.argv[1] if len(sys.argv) > 1 else "raw"
OUT = sys.argv[2] if len(sys.argv) > 2 else "../../data/winnebago"
os.makedirs(OUT, exist_ok=True)
CO = "55139"
DOA_CO = "Winnebago"


def rows(name, sheet=0):
    wb = openpyxl.load_workbook(os.path.join(RAW, name), read_only=True, data_only=True)
    ws = wb.worksheets[sheet] if isinstance(sheet, int) else wb[sheet]
    return [list(r) for r in ws.iter_rows(values_only=True)]


def num(v):
    if v in (None, "", "(D)", "(NA)", "(L)"):
        return None
    try:
        return float(str(v).replace(",", ""))
    except ValueError:
        return None


# ---------------------------------------------------------------- municipalities
ts = rows("Time_Series_MCD_2026.xlsx")
hdr = ts[4]
col = {h: i for i, h in enumerate(hdr) if h}
census_cols = {y: col[f"{y} Census"] for y in (1970, 1980, 1990, 2000, 2010, 2020)}
est_cols = {y: col[f"Final 1/1/{y} Estimate"] for y in range(2021, 2027)}

raw_munis = {}
for r in ts[5:]:
    if r[2] != DOA_CO:
        continue
    raw_munis[r[3]] = r

TYPE = {"T": "Town", "V": "Village", "C": "City"}
munis = {}
for code, r in raw_munis.items():
    if code == "71008":  # Town of Menasha, incorporated as Village of Fox Crossing in 2016
        continue
    name = r[1].replace(" *", "").strip()
    split = "*" in r[1]
    series = {}
    for y, c in {**census_cols, **est_cols}.items():
        v = num(r[c])
        if v is None and code == "71121":  # Fox Crossing history = Town of Menasha
            v = num(raw_munis["71008"][c])
        series[y] = v
    geoid = str(r[4])
    munis[geoid] = dict(geoid=geoid, doa=code, name=name, type=TYPE[r[0]], label=f"{TYPE[r[0]]} of {name}",
                        split=split, series=series)

# DOA projections (Vintage 2024)
for r in rows("Pop_Proj_Muni_2020_2050.xlsx")[3:]:
    if not r or r[3] != DOA_CO:
        continue
    for m in munis.values():
        if m["doa"] == r[0]:
            m["proj"] = {2020: r[4], 2030: r[5], 2040: r[6], 2050: r[7]}

# households projections (Vintage 2024), sheet layout probed at runtime
hh = rows("HH_Proj_Muni_2020-2050.xlsx", "Minor Civil Division (MCD) proj")
for r in hh[4:]:
    if not r or r[3] != DOA_CO:
        continue
    for m in munis.values():
        if m["doa"] == r[0]:
            m["hh"] = {2020: r[4], 2030: r[5], 2040: r[6], 2050: r[7]}

# ---------------------------------------------------------------- boundaries
cs = json.load(open(os.path.join(RAW, "cousub.geojson")))
water = json.load(open(os.path.join(RAW, "water.geojson")))
lakes = unary_union([shape(f["geometry"]).buffer(0) for f in water["features"]])
county_shape = unary_union([shape(f["geometry"]).buffer(0) for f in cs["features"]])
features = []
for f in cs["features"]:
    gid = f["properties"]["GEOID"]
    g = shape(f["geometry"]).buffer(0).difference(lakes)
    g = g.simplify(0.0004, preserve_topology=True)
    if gid not in munis:
        print("no DOA match for", gid, f["properties"]["NAME"])
        continue
    m = munis[gid]
    s = m["series"]
    p = dict(geoid=gid, name=m["label"], short=m["name"], type=m["type"], split=m["split"],
             pop2020=s[2020], pop2026=s[2026], pop2010=s[2010], pop2000=s[2000],
             chg20_26=s[2026] - s[2020], pct20_26=(s[2026] - s[2020]) / s[2020],
             pct10_20=(s[2020] - s[2010]) / s[2010] if s[2010] else None,
             proj2050=m.get("proj", {}).get(2050),
             pct20_50=(m["proj"][2050] - m["proj"][2020]) / m["proj"][2020] if m.get("proj") else None,
             sqmi=f["properties"]["AREALAND"] / 2589988.11)
    p["density2026"] = p["pop2026"] / p["sqmi"]
    from shapely.ops import polylabel
    big = max(getattr(g, "geoms", [g]), key=lambda x: x.area)
    lp = polylabel(big, tolerance=0.0005)
    p["lab_lat"], p["lab_lon"] = round(lp.y, 5), round(lp.x, 5)
    features.append(dict(type="Feature", properties=p, geometry=mapping(g)))


def round_geom(gj, nd=5):
    def rc(c):
        if isinstance(c[0], (int, float)):
            return [round(c[0], nd), round(c[1], nd)]
        return [rc(x) for x in c]
    gj["coordinates"] = rc(gj["coordinates"])
    return gj


for f in features:
    f["geometry"] = round_geom(dict(f["geometry"]))
    f["geometry"]["coordinates"] = json.loads(json.dumps(f["geometry"]["coordinates"]))

lake_feats = []
from shapely.geometry import box as _box
_clip = _box(*county_shape.buffer(0.03).bounds)
for lf in water["features"]:
    g = shape(lf["geometry"]).buffer(0).intersection(_clip)
    if g.area < 0.0004:
        continue
    lake_feats.append(dict(type="Feature", properties=dict(name=lf["properties"]["NAME"]),
                           geometry=round_geom(dict(mapping(g.simplify(0.0004))))))
outline = round_geom(dict(mapping(county_shape.simplify(0.0006))))

# ---------------------------------------------------------------- county series
tsc = rows("Time_Series_Co_2026.xlsx")
hc = tsc[3]
cc = {h: i for i, h in enumerate(hc) if h}


def co_series(row):
    out = {}
    for h, i in cc.items():
        if h.endswith(" Census"):
            out[f"c{h[:4]}"] = row[i]
        elif h.startswith("Final 1/1/"):
            out[f"e{h[10:14]}"] = row[i]
    return out


co_row = next(r for r in tsc if r[0] == DOA_CO)
wi_row = next(r for r in tsc if r[0] and str(r[0]).strip().upper() == "STATE TOTAL")
county = dict(series=co_series(co_row), wi=co_series(wi_row))

comp = rows("Final_Ests_Co_2026_Components.xlsx")
cr = next(r for r in comp if r[2] and str(r[2]).strip() == DOA_CO)
county["components"] = dict(census2020=cr[3], est2026=cr[4], births=cr[5], deaths=cr[6], natural=cr[7],
                            migration=cr[8], total=cr[9])
wr = next(r for r in comp if r[0] and str(r[0]).startswith("STATE TOTAL"))
county["components_wi"] = dict(census2020=wr[3], est2026=wr[4], births=wr[5], deaths=wr[6], natural=wr[7],
                               migration=wr[8], total=wr[9])

hu = rows("Tot_HUs_County_2026.xlsx")
hur = next(r for r in hu if r[2] == DOA_CO)
county["housing_units"] = {int(str(h)[4:8]): v for h, v in zip(hu[3][3:], hur[3:]) if h}
wir = next(r for r in hu if r[0] == "STATE TOTAL")
county["housing_units_wi"] = {int(str(h)[4:8]): v for h, v in zip(hu[3][3:], wir[3:]) if h}

pt = rows("Pop_Proj_Co_State_2020_2050.xlsx", "Co_Proj_2020_2050_totals")
for r in pt:
    if r and r[0] == DOA_CO:
        county["proj"] = {2020: r[1], 2030: r[2], 2040: r[3], 2050: r[4]}
    if r and r[0] and str(r[0]).strip() == "Wisconsin":
        county["proj_wi"] = {2020: r[1], 2030: r[2], 2040: r[3], 2050: r[4]}

# age-sex pyramid (DOA projections give 2020 base + 2030/40/50)
pa = rows("Pop_Proj_Co_State_2020_2050.xlsx", "Co_Proj_2020_2050_x_age_x sex")
pyr = []
for r in pa:
    if r and r[0] == DOA_CO and r[1] != "Total all ages":
        pyr.append(dict(age=r[1], f={2020: r[6], 2030: r[7], 2040: r[8], 2050: r[9]},
                        m={2020: r[10], 2030: r[11], 2040: r[12], 2050: r[13]}))
county["pyramid"] = pyr

# ---------------------------------------------------------------- extrapolation (James's GEOG 330 model)
y0 = [county["series"]["c2000"], county["series"]["c2010"], county["series"]["c2020"]]
county["extrap_base"] = {2000: y0[0], 2010: y0[1], 2020: y0[2]}

# ---------------------------------------------------------------- economy (BEA CAEMP25N)
SECT = {400: "Construction", 500: "Manufacturing", 600: "Wholesale trade", 700: "Retail trade",
        800: "Transportation & warehousing", 900: "Information", 1000: "Finance & insurance",
        1100: "Real estate", 1200: "Professional & technical services", 1300: "Management of companies",
        1400: "Administrative & waste services", 1500: "Educational services",
        1600: "Health care & social assistance", 1700: "Arts & recreation", 1800: "Accommodation & food",
        1900: "Other services", 2000: "Government", 70: "Farm", 100: "Forestry & fishing",
        200: "Mining", 300: "Utilities"}
bea = defaultdict(dict)
with open(os.path.join(RAW, "CAEMP25N__ALL_AREAS_2001_2022.csv"), encoding="latin1") as fh:
    rd = csv.reader(fh)
    h = next(rd)
    yi = {int(x): i for i, x in enumerate(h) if x.strip().isdigit()}
    for r in rd:
        if len(r) < 8:
            continue
        fips = r[0].strip().strip('"').strip()
        if fips not in ("00000", "55000", CO):
            continue
        lc = int(r[4]) if r[4].strip().isdigit() else None
        if lc in SECT or lc == 10:
            bea[fips][lc] = {y: num(r[i]) for y, i in yi.items()}

Y0, Y1 = 2012, 2022
econ = []
for lc, name in SECT.items():
    e0, e1 = bea[CO][lc][Y0], bea[CO][lc][Y1]
    u0, u1 = bea["00000"][lc][Y0], bea["00000"][lc][Y1]
    s1 = bea["55000"][lc][Y1]
    E = bea[CO][10][Y1]; U = bea["00000"][10][Y1]; S = bea["55000"][10][Y1]
    row = dict(line=lc, name=name, emp2012=e0, emp2022=e1)
    if e1 is not None:
        row["share"] = e1 / E
        row["lq_us"] = (e1 / E) / (u1 / U)
        row["lq_wi"] = (e1 / E) / (s1 / S)
        row["basic"] = max(0.0, (e1 / u1 - E / U) * u1)
    if e0 is not None and e1 is not None:
        G = bea["00000"][10][Y1] / bea["00000"][10][Y0] - 1
        gi = u1 / u0 - 1
        ri = e1 / e0 - 1
        row["ns"] = e0 * G
        row["im"] = e0 * (gi - G)
        row["rs"] = e0 * (ri - gi)
        row["chg"] = e1 - e0
    econ.append(row)
tot = dict(emp2012=bea[CO][10][Y0], emp2022=bea[CO][10][Y1], wi2012=bea["55000"][10][Y0], wi2022=bea["55000"][10][Y1],
           us2012=bea["00000"][10][Y0], us2022=bea["00000"][10][Y1])
basic = sum(r.get("basic", 0) for r in econ)
tot["basic"] = basic
tot["multiplier"] = tot["emp2022"] / basic if basic else None
tot["suppressed"] = [r["name"] for r in econ if r["emp2022"] is None]
county["econ"] = dict(rows=econ, totals=tot, years=[Y0, Y1],
                      series={k: {y: bea[k][10][y] for y in sorted(bea[k][10])} for k in ("00000", "55000", CO)})

# per capita income
pci = {}
with open(os.path.join(RAW, "CAINC1_WI_1969_2024.csv"), encoding="latin1") as fh:
    rd = csv.reader(fh)
    h = next(rd)
    yi = {int(x): i for i, x in enumerate(h) if x.strip().isdigit()}
    for r in rd:
        if len(r) < 8:
            continue
        fips = r[0].strip().strip('"').strip()
        if fips in ("55000", CO) and r[4].strip() == "3":
            pci[fips] = {y: num(r[i]) for y, i in yi.items()}
county["pci"] = pci

# ---------------------------------------------------------------- commuting (LODES 2023)
xw = {}
with gzip.open(os.path.join(RAW, "wi_xwalk.csv.gz"), "rt") as fh:
    rd = csv.DictReader(fh)
    for r in rd:
        xw[r["tabblk2020"]] = (r["cty"], r["ctyname"].replace(", WI", ""), r["ctycsub"])

inflow = defaultdict(int); outflow = defaultdict(int); live_work = 0
jobs_by_csub = defaultdict(int); res_by_csub = defaultdict(int)
for fn in ("wi_od_main_JT00_2023.csv.gz", "wi_od_aux_JT00_2023.csv.gz"):
    with gzip.open(os.path.join(RAW, fn), "rt") as fh:
        rd = csv.reader(fh)
        next(rd)
        for w, hgeo, s000, *_ in rd:
            n = int(s000)
            wc = w[:5]; hcnty = hgeo[:5]
            if wc == CO and hcnty == CO:
                live_work += n
            elif wc == CO:
                inflow[hcnty] += n
            elif hcnty == CO:
                outflow[wc] += n

cty_names = {v[0]: v[1] for v in xw.values()}


def top(d, k=8):
    items = sorted(d.items(), key=lambda kv: -kv[1])
    out = [dict(fips=f, name=cty_names.get(f, "Outside Wisconsin" if not f.startswith("55") else f), n=n) for f, n in items[:k]]
    out.append(dict(fips="other", name="All other", n=sum(n for _, n in items[k:])))
    return out


# workplace jobs by sector, by municipality (WAC)
CNS = ["Agriculture", "Mining", "Utilities", "Construction", "Manufacturing", "Wholesale", "Retail",
       "Transportation", "Information", "Finance", "Real estate", "Professional", "Management",
       "Administrative", "Education", "Health care", "Arts", "Accommodation & food", "Other services",
       "Public administration"]
wac_csub = defaultdict(lambda: [0] * 21)
with gzip.open(os.path.join(RAW, "wi_wac_S000_JT00_2023.csv.gz"), "rt") as fh:
    rd = csv.DictReader(fh)
    for r in rd:
        if not r["w_geocode"].startswith(CO):
            continue
        c = xw[r["w_geocode"]][2]
        v = wac_csub[c]
        v[0] += int(r["C000"])
        for i in range(20):
            v[i + 1] += int(r[f"CNS{i + 1:02d}"])
with gzip.open(os.path.join(RAW, "wi_rac_S000_JT00_2023.csv.gz"), "rt") as fh:
    rd = csv.DictReader(fh)
    for r in rd:
        if r["h_geocode"].startswith(CO):
            res_by_csub[xw[r["h_geocode"]][2]] += int(r["C000"])

for f in features:
    g = f["properties"]["geoid"]
    f["properties"]["jobs2023"] = wac_csub[g][0]
    f["properties"]["workers2023"] = res_by_csub[g]
    f["properties"]["jobs_per_worker"] = wac_csub[g][0] / res_by_csub[g] if res_by_csub[g] else None

county["commute"] = dict(year=2023, live_work=live_work, inflow_total=sum(inflow.values()),
                         outflow_total=sum(outflow.values()), inflow=top(inflow), outflow=top(outflow))
county["jobs_sector_lodes"] = dict(zip(["Total"] + CNS, [sum(v[i] for v in wac_csub.values()) for i in range(21)]))

# ---------------------------------------------------------------- ACS (optional)
acs_path = os.path.join(RAW, "acs.json")
if os.path.exists(acs_path):
    acs = json.load(open(acs_path))
    county["acs"] = acs.get("county")
    county["acs_wi"] = acs.get("state")
    for f in features:
        a = acs.get("cousub", {}).get(f["properties"]["geoid"])
        if a:
            f["properties"].update(a)

# ---------------------------------------------------------------- write
meta = dict(updated="2026-10-24",
            sources=["Wisconsin DOA Demographic Services Center (final 1/1/2026 estimates; Vintage 2024 projections)",
                     "U.S. BEA CAEMP25N and CAINC1", "U.S. Census Bureau LEHD LODES 8, 2023",
                     "U.S. Census Bureau TIGERweb", "U.S. Census Bureau ACS 5-year"])
json.dump(dict(type="FeatureCollection", features=features), open(os.path.join(OUT, "municipalities.geojson"), "w"),
          separators=(",", ":"))
json.dump(dict(type="FeatureCollection", features=lake_feats + [dict(type="Feature", properties=dict(name="outline"), geometry=outline)]),
          open(os.path.join(OUT, "context.geojson"), "w"), separators=(",", ":"))
munis_out = [dict(geoid=m["geoid"], name=m["label"], short=m["name"], type=m["type"], split=m["split"],
                  series=m["series"], proj=m.get("proj")) for m in munis.values()]
json.dump(dict(meta=meta, county=county, munis=munis_out), open(os.path.join(OUT, "profile.json"), "w"),
          separators=(",", ":"), default=lambda o: None)
print("features", len(features), "lakes", len(lake_feats))
for f in sorted(features, key=lambda f: -f["properties"]["pop2026"])[:6]:
    p = f["properties"]
    print(f"  {p['name']:28s} {p['pop2026']:>8.0f} {p['pct20_26']*100:6.2f}%  jobs {p['jobs2023']}")
c = county
print("county 2020/2026", c["series"].get("c2020"), c["series"].get("e2026"), "proj", c.get("proj"))
print("components", c["components"])
print("commute", {k: c["commute"][k] for k in ("live_work", "inflow_total", "outflow_total")})
print("multiplier", round(tot["multiplier"], 2), "basic", round(basic), "suppressed", tot["suppressed"])
