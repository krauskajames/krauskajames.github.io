"""Parcel and NG911 address data QA toolkit.

Checks a county's tax parcels, site address points and road centerlines and writes every
finding to one error layer, a summary table and a GeoJSON for the web map.

    python3 parcel_qa.py config/sheboygan.json out/

Field names live in the county config file, so pointing the toolkit at another county is a
matter of writing a new config. An ArcPy wrapper (arcgis_toolbox.pyt) runs the same checks
as a geoprocessing tool inside ArcGIS Pro.
"""
import json, math, os, re, sys
from collections import defaultdict

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point
from shapely.ops import unary_union

WORK_CRS = 3071   # NAD83(HARN) / Wisconsin Transverse Mercator, meters

CHECKS = {
    # code: (layer, severity, short title, plain-language description)
    "P01": ("parcels", "high", "Overlapping parcels", "Two parcels cover the same ground."),
    "P02": ("parcels", "medium", "Gap between parcels", "A small hole between parcels that is not a road, water or other public land."),
    "P03": ("parcels", "high", "Duplicate parcel ID", "More than one polygon carries the same parcel number."),
    "P04": ("parcels", "medium", "Missing required attribute", "A required field (parcel ID, owner, site address or similar) is empty."),
    "P05": ("parcels", "low", "Sliver parcel", "A very thin polygon, usually left over from editing."),
    "P06": ("parcels", "high", "Invalid geometry", "Self-intersecting or otherwise invalid polygon."),
    "A01": ("addresses", "medium", "Missing required attribute", "An NG911-required field (number, street, municipality, ESN or MSAG community) is empty."),
    "A02": ("addresses", "high", "Outside its parcel", "The point does not fall inside the parcel its ParcelID points to."),
    "A03": ("addresses", "medium", "Outside every parcel", "The point does not fall in any tax parcel."),
    "A04": ("addresses", "high", "Road link broken", "The road centerline ID on the point does not exist."),
    "A05": ("addresses", "high", "Street name mismatch", "The point's street name differs from its linked road segment."),
    "A06": ("addresses", "high", "Number outside road range", "The house number is outside the address range of its linked road segment."),
    "A07": ("addresses", "medium", "Wrong side of the road", "An odd number sits on the even side of the road, or the reverse."),
    "A08": ("addresses", "medium", "Far from its road", "The point is unusually far from its linked road segment."),
    "A09": ("addresses", "high", "Duplicate address", "Two active points share the same full address and unit."),
    "A10": ("addresses", "medium", "Municipality mismatch", "The municipality on the point differs from the municipal boundary it sits in."),
    "R01": ("roads", "medium", "Mixed parity range", "A side of the road range mixes odd and even numbers."),
    "R02": ("roads", "high", "Overlapping ranges", "Two segments of the same street in the same municipality claim overlapping numbers on the same side."),
    "R03": ("roads", "low", "Missing range", "A named road segment has no address range."),
}


def log(*a):
    print(*a, flush=True)


def blank(s):
    return s.isna() | (s.astype(str).str.strip().isin(["", "None", "nan", "0", "<Null>"]))


def to_int(s):
    return pd.to_numeric(s.astype(str).str.extract(r"(\d+)")[0], errors="coerce")


def norm_name(s):
    return s.fillna("").astype(str).str.upper().str.replace(r"[^A-Z0-9 ]", "", regex=True).str.replace(r"\s+", " ", regex=True).str.strip()


class Findings:
    def __init__(self):
        self.rows = []

    def add(self, code, geom, feature_id, detail):
        layer, sev, title, _ = CHECKS[code]
        self.rows.append(dict(check=code, layer=layer, severity=sev, title=title, feature_id=str(feature_id), detail=detail, geometry=geom))

    def frame(self, crs):
        if not self.rows:
            return gpd.GeoDataFrame(columns=["check", "layer", "severity", "title", "feature_id", "detail", "geometry"], geometry="geometry", crs=crs)
        return gpd.GeoDataFrame(self.rows, geometry="geometry", crs=crs)


# ------------------------------------------------------------------ parcels
def check_parcels(P, cfg, F, public=None):
    f = cfg["parcel_fields"]
    pid = f["id"]
    log(f"parcels: {len(P):,}")

    bad = ~P.geometry.is_valid
    for i, r in P[bad].iterrows():
        F.add("P06", r.geometry.representative_point(), r[pid], "Invalid polygon geometry")
    P = P.copy()
    P.loc[bad, "geometry"] = P.loc[bad, "geometry"].buffer(0)

    # P03 duplicate IDs (ignore blanks; those are P04)
    ids = P[~blank(P[pid])]
    for v, g in ids.groupby(pid):
        if len(g) > 1:
            F.add("P03", g.geometry.iloc[0].representative_point(), v, f"{len(g)} polygons share parcel ID {v}")

    # P04 missing attributes
    for col in f.get("required", []):
        if col not in P.columns:
            continue
        for i, r in P[blank(P[col])].iterrows():
            F.add("P04", r.geometry.representative_point(), r[pid], f"Field '{col}' is empty")

    # P01 overlaps via spatial index
    min_ov = cfg.get("overlap_min_m2", 5.0)
    sidx = P.sindex
    geoms = P.geometry.values
    pids = P[pid].values
    left, right = sidx.query(geoms, predicate="intersects")
    seen = set()
    for a, b in zip(left, right):
        if a >= b or (a, b) in seen:
            continue
        seen.add((a, b))
        inter = geoms[a].intersection(geoms[b])
        if inter.is_empty:
            continue
        area = inter.area
        if area >= min_ov:
            F.add("P01", inter.representative_point(), f"{pids[a]} / {pids[b]}", f"{pids[a]} and {pids[b]} overlap by {area:,.0f} m²")

    # P02 gaps: holes in the dissolved parcel fabric that are small and not public land
    max_gap = cfg.get("gap_max_m2", 500.0)
    fabric = unary_union(list(geoms))
    holes = []
    for poly in getattr(fabric, "geoms", [fabric]):
        for ring in poly.interiors:
            from shapely.geometry import Polygon
            h = Polygon(ring)
            if 1.0 <= h.area <= max_gap:
                holes.append(h)
    if public is not None and len(holes):
        pu = unary_union(list(public.geometry.values))
        holes = [h for h in holes if h.difference(pu).area > 0.5 * h.area]
    for h in holes:
        F.add("P02", h.representative_point(), "", f"Gap of {h.area:,.0f} m² between parcels")

    # P05 slivers: thin polygons (Polsby-Popper compactness and width)
    thin = cfg.get("sliver_width_m", 1.5)
    for i, r in P.iterrows():
        g = r.geometry
        if g.is_empty or g.area <= 0:
            continue
        width = 2 * g.area / g.length          # approximate mean width
        if width < thin and g.area < 2000:
            F.add("P05", g.representative_point(), r[pid], f"Sliver about {width:.1f} m wide, {g.area:,.0f} m²")
    return P


# ------------------------------------------------------------------ roads
def check_roads(R, cfg, F):
    f = cfg["road_fields"]
    rid = f["id"]
    log(f"road segments: {len(R):,}")
    R = R.copy()
    for k in ("fromleft", "toleft", "fromright", "toright"):
        R[k + "_n"] = to_int(R[f[k]])
    R["name_n"] = norm_name(R[f["name"]])
    named = R["name_n"] != ""

    no_range = named & R[["fromleft_n", "toleft_n", "fromright_n", "toright_n"]].fillna(0).eq(0).all(axis=1)
    if cfg.get("report_missing_ranges", True):
        for i, r in R[no_range].iterrows():
            F.add("R03", r.geometry.interpolate(0.5, normalized=True), r[rid], f"{r[f['name']]} segment has no address range")

    for side in ("left", "right"):
        a, b = R[f"from{side}_n"], R[f"to{side}_n"]
        mixed = a.notna() & b.notna() & (a > 0) & (b > 0) & ((a % 2) != (b % 2))
        for i, r in R[mixed].iterrows():
            F.add("R01", r.geometry.interpolate(0.5, normalized=True), r[rid], f"{side.title()} range {int(r[f'from{side}_n'])}–{int(r[f'to{side}_n'])} mixes odd and even")

    # R02 overlapping ranges on the same side, same street, same municipality
    muni = f.get("municipality")
    keys = ["name_n"] + ([muni] if muni else [])
    for side in ("left", "right"):
        R["lo"] = R[[f"from{side}_n", f"to{side}_n"]].min(axis=1)
        R["hi"] = R[[f"from{side}_n", f"to{side}_n"]].max(axis=1)
        valid = named & (R["lo"] > 0)
        for _, g in R[valid].groupby(keys):
            if len(g) < 2:
                continue
            g = g.sort_values("lo")
            rows = list(g.itertuples())
            for x in range(len(rows) - 1):
                for y in range(x + 1, len(rows)):
                    if rows[y].lo > rows[x].hi:
                        break
                    if rows[y].lo < rows[x].hi and (rows[x].lo != rows[y].lo or rows[x].hi != rows[y].hi):
                        F.add("R02", rows[x].geometry.interpolate(0.5, normalized=True), f"{getattr(rows[x], rid)} / {getattr(rows[y], rid)}",
                              f"{side.title()} ranges {int(rows[x].lo)}–{int(rows[x].hi)} and {int(rows[y].lo)}–{int(rows[y].hi)} overlap")
    return R


def side_of_line(line, pt):
    """+1 if pt is left of the line's direction at its nearest point, -1 if right."""
    d = line.project(pt)
    L = line.length
    a = line.interpolate(max(0, d - 1.0))
    b = line.interpolate(min(L, d + 1.0))
    cross = (b.x - a.x) * (pt.y - a.y) - (b.y - a.y) * (pt.x - a.x)
    return 1 if cross > 0 else -1


# ------------------------------------------------------------------ addresses
def check_addresses(A, P, R, M, cfg, F):
    f = cfg["address_fields"]
    pf, rf = cfg["parcel_fields"], cfg["road_fields"]
    aid = f["id"]
    log(f"address points: {len(A):,}")
    A = A.copy()
    if f.get("status") and cfg.get("active_status_values"):
        active = A[f["status"]].astype(str).str.strip().isin(cfg["active_status_values"])
        log(f"  active: {active.sum():,}")
        A = A[active].copy()

    for col in f.get("required", []):
        if col in A.columns:
            for i, r in A[blank(A[col])].iterrows():
                F.add("A01", r.geometry, r[aid], f"Field '{col}' is empty")

    # A02 / A03 parcel containment
    hit = gpd.sjoin(A[[aid, f["parcel_id"], "geometry"]], P[[pf["id"], "geometry"]], how="left", predicate="within")
    inside_any = hit.groupby(level=0)[pf["id"]].apply(lambda s: set(s.dropna().astype(str)))
    for i, r in A.iterrows():
        inside = inside_any.get(i, set())
        claimed = str(r[f["parcel_id"]]).strip() if not blank(pd.Series([r[f["parcel_id"]]])).iloc[0] else ""
        if not inside:
            F.add("A03", r.geometry, r[aid], "Point is not inside any tax parcel" + (f" (claims parcel {claimed})" if claimed else ""))
        elif claimed and claimed not in inside:
            F.add("A02", r.geometry, r[aid], f"Claims parcel {claimed} but sits in {', '.join(sorted(inside))}")

    # road link checks
    roads = R.set_index(R[rf["id"]].astype(str))
    roads = roads[~roads.index.duplicated()]
    A["num"] = to_int(A[f["number"]])
    A["name_n"] = norm_name(A[f["street"]])
    far = cfg.get("far_from_road_m", 400.0)
    for i, r in A.iterrows():
        link = str(r[f["road_id"]]).strip() if f.get("road_id") else ""
        if not link or link in ("None", "nan"):
            continue
        if link not in roads.index:
            F.add("A04", r.geometry, r[aid], f"Road ID {link} not found in centerlines")
            continue
        seg = roads.loc[link]
        if r["name_n"] and seg["name_n"] and r["name_n"] != seg["name_n"]:
            F.add("A05", r.geometry, r[aid], f"Point says '{r[f['street']]}', road segment says '{seg[rf['name']]}'")
        dist = seg.geometry.distance(r.geometry)
        if dist > far:
            F.add("A08", r.geometry, r[aid], f"{dist:,.0f} m from its road segment")
        n = r["num"]
        if pd.isna(n) or n <= 0:
            continue
        side = side_of_line(seg.geometry, r.geometry)
        s = "left" if side > 0 else "right"
        o = "right" if s == "left" else "left"
        nz = lambda x: 0 if pd.isna(x) else x
        lo_s, hi_s = sorted([nz(seg[f"from{s}_n"]), nz(seg[f"to{s}_n"])])
        lo_o, hi_o = sorted([nz(seg[f"from{o}_n"]), nz(seg[f"to{o}_n"])])
        if hi_s <= 0 and hi_o <= 0:
            continue
        in_s = lo_s <= n <= hi_s
        in_o = lo_o <= n <= hi_o
        if not in_s and not in_o:
            F.add("A06", r.geometry, r[aid], f"{int(n)} is outside the segment's ranges ({int(lo_s)}–{int(hi_s)} this side, {int(lo_o)}–{int(hi_o)} other side)")
        elif hi_s > 0 and (lo_s % 2) != (n % 2) and in_o and (lo_o % 2) == (n % 2) and dist > 3:
            F.add("A07", r.geometry, r[aid], f"{int(n)} is on the {s} side, but the {s} range is {int(lo_s)}–{int(hi_s)}")

    # A09 duplicates
    key = [f["full"]] + ([f["unit"]] if f.get("unit") else [])
    dup = A[~blank(A[f["full"]])].copy()
    dup["k"] = dup[key].fillna("").astype(str).apply(lambda x: " ".join(x).upper().strip(), axis=1)
    for k, g in dup.groupby("k"):
        if len(g) > 1:
            F.add("A09", g.geometry.iloc[0], " / ".join(map(str, g[aid].tolist()[:4])), f"{len(g)} points share '{k}'")

    # A10 municipality vs boundary
    if M is not None and f.get("municipality"):
        mf = cfg["muni_fields"]
        j = gpd.sjoin(A[[aid, f["municipality"], "geometry"]], M[[mf["name"], "geometry"]], how="left", predicate="within")
        j = j[~j.index.duplicated()]
        alias = {k.upper(): v.upper() for k, v in cfg.get("muni_aliases", {}).items()}
        def canon(x):
            x = re.sub(r"\s+", " ", str(x).upper().strip())
            x = alias.get(x, x)
            return re.sub(r"^(CITY|VILLAGE|TOWN) OF ", "", x)
        for i, r in j.iterrows():
            a, b = r[f["municipality"]], r[mf["name"]]
            if pd.isna(b) or blank(pd.Series([a])).iloc[0]:
                continue
            if canon(a) != canon(b):
                F.add("A10", r.geometry, r[aid], f"Point says '{a}', boundary says '{b}'")
    return A


def run(cfg_path, out):
    cfg = json.load(open(cfg_path))
    base = os.path.dirname(os.path.abspath(cfg_path))
    os.makedirs(out, exist_ok=True)
    rd = lambda k: gpd.read_file(os.path.join(base, cfg["inputs"][k])).to_crs(WORK_CRS) if cfg["inputs"].get(k) else None
    P, A, R, M = rd("parcels"), rd("addresses"), rd("roads"), rd("municipalities")
    public = rd("public_land")
    F = Findings()
    P = check_parcels(P, cfg, F, public)
    R = check_roads(R, cfg, F)
    A = check_addresses(A, P, R, M, cfg, F)
    E = F.frame(WORK_CRS)
    E.to_file(os.path.join(out, "qa_findings.gpkg"), layer="findings", driver="GPKG")
    summ = (E.groupby(["check", "layer", "severity", "title"]).size().rename("count").reset_index()
            if len(E) else pd.DataFrame(columns=["check", "layer", "severity", "title", "count"]))
    totals = dict(parcels=len(P), addresses=len(A), roads=len(R))
    summ["checked"] = summ["layer"].map(totals)
    summ["rate_per_1000"] = (summ["count"] / summ["checked"] * 1000).round(2)
    summ.to_csv(os.path.join(out, "qa_summary.csv"), index=False)
    E.to_crs(4326).to_file(os.path.join(out, "qa_findings.geojson"), driver="GeoJSON")
    json.dump(dict(county=cfg["county"], totals=totals, checks={k: dict(layer=v[0], severity=v[1], title=v[2], description=v[3]) for k, v in CHECKS.items()}),
              open(os.path.join(out, "qa_meta.json"), "w"), indent=1)
    log(summ.to_string(index=False))
    return E, summ


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
