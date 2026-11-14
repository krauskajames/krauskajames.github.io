"""Run the legal description reader over every parcel description in the county's tax roll and
compare each drawn description with the parcel the county mapped (check L01).

    python3 county_run.py ../config/sheboygan.json ../raw ../out

Tax-roll descriptions rarely give coordinates for their point of commencement, so the drawn shape
is placed by best fit: it is moved onto the mapped parcel's centroid and turned up to ±3° (to allow
for a different basis of bearings), and the remaining distance between the two outlines is the
shape offset. Only single-tract descriptions that read cleanly are compared; the rest are counted
by reason.
"""
import json, math, os, re, sys, time
import geopandas as gpd, pandas as pd
from shapely.geometry import Polygon, Point
from shapely import affinity
sys.path.insert(0, os.path.dirname(__file__))
import ldreader as L

FIT_LIMIT_FT = 10.0       # outline offset after best fit that counts as a mismatch
AREA_LIMIT = 0.05         # or drawn area differing from mapped area by more than 5%
MISCLOSE_FT, PRECISION = 1.0, 5000   # a description "closes" if it misses by 1 ft or less, or by 1:5,000 or better

def best_fit(drawn: Polygon, mapped: Polygon):
    """Move drawn onto mapped (centroid), then search rotations ±3°; return (offset_ft, rot_deg, fitted)."""
    c0, c1 = drawn.centroid, mapped.centroid
    moved = affinity.translate(drawn, c1.x - c0.x, c1.y - c0.y)
    best = (moved.exterior.hausdorff_distance(mapped.exterior), 0.0, moved)
    for step in (0.5, 0.1, 0.02):
        lo = best[1]
        for k in range(-5, 6):
            r = lo + k * step
            if abs(r) > 3: continue
            g = affinity.rotate(moved, r, origin=c1)
            d = g.exterior.hausdorff_distance(mapped.exterior)
            if d < best[0]: best = (d, r, g)
    return best

def covered(drawn: Polygon, mapped: Polygon) -> float:
    """Share of the mapped parcel the drawn description can cover when slid up to 60 ft."""
    best = (drawn.intersection(mapped).area, 0.0, 0.0)
    for step in (12.0, 3.0, 0.75):
        bx, by = best[1], best[2]
        for i in range(-5, 6):
            for j in range(-5, 6):
                dx, dy = bx + i * step, by + j * step
                if abs(dx) > 60 or abs(dy) > 60: continue
                a = affinity.translate(drawn, dx, dy).intersection(mapped).area
                if a > best[0]: best = (a, dx, dy)
    return best[0] / mapped.area

def main(cfg_path, raw, out):
    cfg = json.load(open(cfg_path))
    pid = cfg.get("fields", {}).get("parcels", {}).get("pid", "PARCELID")
    t0 = time.time()
    P = gpd.read_file(os.path.join(raw, "parcels.gpkg"), columns=[pid, "TAXDSCRP", "ACRES"])
    if P.crs.axis_info[0].unit_name.lower().find("foot") < 0:
        raise SystemExit("parcels must be in a US-feet state plane / county system")
    rows = []; finds = []
    for r in P.itertuples():
        txt = r.TAXDSCRP if isinstance(r.TAXDSCRP, str) else ""
        if not txt.strip():
            rows.append({pid: getattr(r, pid), "status": "empty"}); continue
        R = L.parse(txt)
        row = {pid: getattr(r, pid), "status": R.status, "n_ties": len(R.ties), "n_courses": len(R.courses),
               "flags": "; ".join(R.flags), "acres_roll": r.ACRES}
        if R.misclose is not None:
            row.update(misclose_ft=round(R.misclose, 3), precision=None if R.precision == math.inf else round(R.precision),
                       acres_desc=round(R.area_sqft / 43560, 3))
        vague = any(c.confidence == "vague" for c in R.courses)
        multi = any(f.startswith(("exception", "more than one", "no 'TO BEG'", "land excepted", "land added", "lot plus", "a whole aliquot")) for f in R.flags)
        clean = R.status == "parsed" and not vague and len(R.courses) >= 3
        g = r.geometry
        mapped = (max(g.geoms, key=lambda p: p.area) if g.geom_type == "MultiPolygon" else g) if g is not None else None
        here = mapped.representative_point() if mapped is not None else None
        closes = clean and (R.misclose <= MISCLOSE_FT or R.precision >= PRECISION)
        # L01: a cleanly read description that does not close
        if clean and not closes:
            row["check"] = "L01"
            finds.append({"check": "L01", "severity": "medium", "feature_id": getattr(r, pid),
                          "detail": f"Description doesn't close: misses by {R.misclose:,.2f} ft (1:{R.precision:,.0f}) over {len(R.courses)} courses",
                          "geometry": here})
        if R.status == "parsed":
            row["compare"] = ("yes" if closes and not multi and mapped is not None else
                              "vague course" if vague else "does not close" if clean and not closes else
                              "exception or several tracts" if multi else "too few courses" if len(R.courses) < 3 else "no geometry")
        if row.get("compare") == "yes":
            pts = R.coords(); drawn = Polygon(pts[:-1])
            if drawn.is_valid and drawn.area > 0 and mapped.is_valid:
                off, rot, fitted = best_fit(drawn, mapped)
                darea = drawn.area / mapped.area - 1
                row.update(acres_map=round(mapped.area / 43560, 3), fit_offset_ft=round(off, 2), fit_rot_deg=round(rot, 2), area_diff=round(darea, 4))
                pob = affinity.rotate(affinity.translate(Point(0, 0), mapped.centroid.x - drawn.centroid.x, mapped.centroid.y - drawn.centroid.y), rot, origin=mapped.centroid)
                row.update(pob_x=round(pob.x, 2), pob_y=round(pob.y, 2))
                # L02: a description that closes but does not match the parcel the county mapped
                if off > FIT_LIMIT_FT or abs(darea) > AREA_LIMIT:
                    why = []
                    if off > FIT_LIMIT_FT: why.append(f"outlines differ by up to {off:,.0f} ft after best fit")
                    if abs(darea) > AREA_LIMIT: why.append(f"description draws {R.area_sqft / 43560:,.2f} ac vs {mapped.area / 43560:,.2f} ac mapped ({darea:+.0%})")
                    road = darea > 0 and covered(fitted, mapped) >= 0.99
                    if road: why.append("the mapped parcel fits inside the description, which runs farther: usually to a road centerline or section line that the map stops short of at the right-of-way")
                    row["check"] = "L02"
                    finds.append({"check": "L02", "severity": "low" if road else "medium", "feature_id": getattr(r, pid),
                                  "detail": "Description doesn't match the mapped parcel: " + "; ".join(why), "geometry": here})
            else:
                row["compare"] = "drawn shape not a valid polygon"
        rows.append(row)
    T = pd.DataFrame(rows)
    os.makedirs(out, exist_ok=True)
    T.to_csv(os.path.join(out, "legal_desc_results.csv"), index=False)
    F = gpd.GeoDataFrame(finds, crs=P.crs) if finds else gpd.GeoDataFrame(columns=["check", "severity", "feature_id", "detail", "geometry"], geometry="geometry", crs=P.crs)
    F.to_file(os.path.join(out, "legal_desc_findings.gpkg"), layer="findings", driver="GPKG")
    c = T.status.value_counts().to_dict()
    cmp = T.get("compare", pd.Series(dtype=str)).value_counts().to_dict()
    closed = T[T.status == "parsed"]
    S = {
        "parcels": len(T), "empty": int(c.get("empty", 0)), "no_bearings": int(c.get("no_bearings", 0)),
        "with_courses": int(c.get("parsed", 0) + c.get("partial", 0)), "parsed": int(c.get("parsed", 0)), "partial": int(c.get("partial", 0)),
        "close_10000": int((closed.precision.isna() | (closed.precision >= 10000)).sum()),
        "close_5000": int((closed.precision.isna() | (closed.precision >= 5000)).sum()),
        "misclose_over_1ft": int((closed.misclose_ft > 1).sum()),
        "compared": int(cmp.get("yes", 0)), "not_compared": {k: int(v) for k, v in cmp.items() if k != "yes"},
        "L01_does_not_close": int((F.check == "L01").sum()) if len(F) else 0,
        "L02_does_not_match": int((F.check == "L02").sum()) if len(F) else 0,
        "L02_map_stops_short": int(((F.check == "L02") & (F.severity == "low")).sum()) if len(F) else 0,
        "fit_offset_median_ft": float(T.fit_offset_ft.median()) if "fit_offset_ft" in T else None,
        "fit_within_5ft": int((T.get("fit_offset_ft", pd.Series(dtype=float)) <= 5).sum()),
        "seconds": round(time.time() - t0, 1),
    }
    json.dump(S, open(os.path.join(out, "legal_desc_summary.json"), "w"), indent=1)
    print(json.dumps(S, indent=1))

if __name__ == "__main__":
    main(*sys.argv[1:4])
