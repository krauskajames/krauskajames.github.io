"""Pull ACS 5-year indicators for Winnebago County, its county subdivisions and Wisconsin.

Usage: CENSUS_KEY=... python3 fetch_acs.py raw/acs.json [year]
The key is read from the environment and never written to disk.
"""
import json, os, sys, urllib.request, urllib.parse

OUT = sys.argv[1]
YEAR = sys.argv[2] if len(sys.argv) > 2 else "2024"
KEY = os.environ["CENSUS_KEY"]
BASE = f"https://api.census.gov/data/{YEAR}/acs/acs5"

AGE65 = [f"B01001_{i:03d}E" for i in list(range(20, 26)) + list(range(44, 50))]
RENT_BURDEN = [f"B25070_{i:03d}E" for i in (7, 8, 9, 10)]
OWN_BURDEN = [f"B25091_{i:03d}E" for i in (8, 9, 10, 11, 19, 20, 21, 22)]
BA = [f"B15003_{i:03d}E" for i in (22, 23, 24, 25)]
VARS = (["B01003_001E", "B01002_001E", "B19013_001E", "B19013_001M", "B25077_001E", "B25064_001E",
         "B17001_001E", "B17001_002E", "B15003_001E", "B25002_001E", "B25002_003E", "B25003_001E", "B25003_003E",
         "B25070_001E", "B25070_011E", "B25091_001E", "B25091_012E", "B25091_023E", "B01001_001E", "B08303_001E"]
        + AGE65 + RENT_BURDEN + OWN_BURDEN + BA)


def get(geo_for, geo_in=None):
    out = []
    for i in range(0, len(VARS), 45):
        q = {"get": ",".join(["NAME"] + VARS[i:i + 45]), "for": geo_for, "key": KEY}
        if geo_in:
            q["in"] = geo_in
        url = BASE + "?" + urllib.parse.urlencode(q, safe=":*,")
        data = json.load(urllib.request.urlopen(url, timeout=60))
        h, rows = data[0], data[1:]
        recs = [dict(zip(h, r)) for r in rows]
        if not out:
            out = recs
        else:
            for a, b in zip(out, recs):
                a.update(b)
    return out


def f(v):
    try:
        x = float(v)
        return None if x < -100000 else x
    except (TypeError, ValueError):
        return None


def derive(r):
    s = lambda ks: sum(f(r[k]) or 0 for k in ks)
    pop = f(r["B01001_001E"]) or 0
    renters = (f(r["B25070_001E"]) or 0) - (f(r["B25070_011E"]) or 0)
    owners = (f(r["B25091_001E"]) or 0) - (f(r["B25091_012E"]) or 0) - (f(r["B25091_023E"]) or 0)
    inc, moe = f(r["B19013_001E"]), f(r["B19013_001M"])
    return dict(
        acs_pop=f(r["B01003_001E"]),
        med_age=f(r["B01002_001E"]),
        med_income=inc,
        med_income_cv=(moe / 1.645 / inc) if inc and moe else None,
        med_value=f(r["B25077_001E"]),
        med_rent=f(r["B25064_001E"]),
        pct65=s(AGE65) / pop if pop else None,
        poverty=(f(r["B17001_002E"]) or 0) / f(r["B17001_001E"]) if f(r["B17001_001E"]) else None,
        ba_plus=s(BA) / f(r["B15003_001E"]) if f(r["B15003_001E"]) else None,
        vacancy=(f(r["B25002_003E"]) or 0) / f(r["B25002_001E"]) if f(r["B25002_001E"]) else None,
        renter_share=(f(r["B25003_003E"]) or 0) / f(r["B25003_001E"]) if f(r["B25003_001E"]) else None,
        rent_burden=s(RENT_BURDEN) / renters if renters > 0 else None,
        own_burden=s(OWN_BURDEN[:4] + OWN_BURDEN[4:]) / owners if owners > 0 else None,
        housing_units=f(r["B25002_001E"]),
    )


res = {"year": YEAR, "vintage": f"{int(YEAR) - 4}-{YEAR}"}
res["county"] = derive(get("county:139", "state:55")[0])
res["state"] = derive(get("state:55")[0])
res["us"] = derive(get("us:1")[0])
res["cousub"] = {r["state"] + r["county"] + r["county subdivision"]: derive(r)
                 for r in get("county subdivision:*", "state:55 county:139")}
json.dump(res, open(OUT, "w"), indent=1)
print("cousubs", len(res["cousub"]), "county income", res["county"]["med_income"], "65+", res["county"]["pct65"])
