"""Write ArcGIS Online-ready layers and tables to agol/ from data/winnebago/.
Usage: python3 export_agol.py ../../data/winnebago agol"""
import csv, json, os, sys, zipfile
D, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
P = json.load(open(os.path.join(D, "profile.json"))); G = json.load(open(os.path.join(D, "municipalities.geojson")))
c = P["county"]
KEEP = [("geoid", "GEOID"), ("name", "Muni_Name"), ("short", "Short_Name"), ("type", "Muni_Type"), ("split", "Split_Muni"),
        ("pop2000", "Pop2000"), ("pop2010", "Pop2010"), ("pop2020", "Pop2020"), ("pop2026", "Pop2026"),
        ("chg20_26", "Chg20_26"), ("pct20_26", "Pct20_26"), ("proj2050", "Proj2050"), ("pct20_50", "Pct20_50"),
        ("sqmi", "Land_SqMi"), ("density2026", "Density26"), ("med_income", "MedHHInc"), ("med_income_cv", "MedInc_CV"),
        ("med_value", "MedHomeVal"), ("med_rent", "MedRent"), ("pct65", "Pct65Plus"), ("poverty", "PctPoverty"),
        ("ba_plus", "PctBAplus"), ("renter_share", "PctRenter"), ("jobs2023", "Jobs2023"), ("workers2023", "Workers23"),
        ("jobs_per_worker", "JobsPerWkr")]
feats = []
for f in G["features"]:
    p = f["properties"]
    props = {}
    for k, n in KEEP:
        v = p.get(k)
        if isinstance(v, float) and k.startswith(("pct", "poverty", "ba_plus", "renter", "med_income_cv")):
            v = round(v * 100, 2)   # percentages as 0-100
        elif isinstance(v, float):
            v = round(v, 2)
        props[n] = v
    feats.append(dict(type="Feature", properties=props, geometry=f["geometry"]))
json.dump(dict(type="FeatureCollection", features=feats), open(os.path.join(OUT, "winnebago_municipalities.geojson"), "w"))

s = c["series"]
with open(os.path.join(OUT, "county_population.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Year", "Series", "Population"])
    for k, v in sorted(s.items(), key=lambda kv: kv[0][1:]):
        if v and int(k[1:]) >= 1970:
            w.writerow([int(k[1:]), "Census" if k[0] == "c" else "DOA estimate", v])
    for y, v in c["proj"].items():
        if int(y) > 2020: w.writerow([int(y), "DOA projection", v])
    Y = [s["c2000"], s["c2010"], s["c2020"]]
    b = (Y[2] - Y[1]) / (Y[1] - Y[0]); a = (Y[1] - Y[0]) / (b - 1); cc = Y[0] - a
    for y in (2030, 2040, 2050):
        w.writerow([y, "Trend (modified exponential)", round(cc + a * b ** ((y - 2000) / 10))])

with open(os.path.join(OUT, "economy_sectors.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Sector", "Jobs2012", "Jobs2022", "Change", "Share2022", "LQ_US", "LQ_WI", "BasicJobs", "NationalShare", "IndustryMix", "RegionalComp"])
    for r in c["econ"]["rows"]:
        if r.get("emp2022") is None: continue
        w.writerow([r["name"], r["emp2012"], r["emp2022"], r.get("chg"), round(r["share"] * 100, 2), round(r["lq_us"], 3), round(r["lq_wi"], 3),
                    round(r.get("basic", 0)), round(r.get("ns", 0)), round(r.get("im", 0)), round(r.get("rs", 0))])

with open(os.path.join(OUT, "commute_flows.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Direction", "County", "Workers"])
    for d, k in (("Into Winnebago", "inflow"), ("Out of Winnebago", "outflow")):
        for r in c["commute"][k]: w.writerow([d, r["name"], r["n"]])

with open(os.path.join(OUT, "age_sex.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["AgeGroup", "Sort", "Sex", "Year", "Population"])
    for i, r in enumerate(c["pyramid"]):
        for sx, lab in (("m", "Male"), ("f", "Female")):
            for y, v in r[sx].items(): w.writerow([r["age"], i, lab, int(y), v])
with zipfile.ZipFile(os.path.join(OUT, "winnebago_dashboard_data.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    for fn in sorted(os.listdir(OUT)):
        if not fn.endswith(".zip"): z.write(os.path.join(OUT, fn), fn)
print(sorted(os.listdir(OUT)))
