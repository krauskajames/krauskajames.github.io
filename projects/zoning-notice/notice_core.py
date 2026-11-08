# -*- coding: utf-8 -*-
"""Zoning hearing notice packet: the owner-list logic, with no arcpy needed.

ZoningNotice.pyt does the GIS part in ArcGIS Pro (select, buffer, read rows, add layers).
This module turns the parcel rows it reads into a mailing list:
  - drops right-of-way and blank-owner parcels (and says why)
  - merges owners that are the same after normalizing names and addresses
    ("PETERSON & SONS CO LLC" = "PETERSON & SONS COMPANY LLC")
  - flags near-matches it did NOT merge, for a human to look at
  - flags absentee owners (mailing address differs from site address: usually rentals)
  - formats label lines (first-last "Alt" names when present)
  - writes the CSVs, the summary and an Avery 5160 label PDF

Field names default to the Wisconsin statewide parcel schema as served by Sheboygan County
(OWNERNME1, OWNERNME1ALT, PSTLADDRESS, PSTLCITY, PSTLSTATE, PSTLZIP5, PSTLZIP4, SITEADDRESS, MUNI, isROW).
Tests: python tests/test_notice_core.py
"""
import csv
import difflib
import os
import re
from collections import OrderedDict

DEFAULT_FIELDS = {
    "id": "PARCELID",
    "owner1": "OWNERNME1",
    "owner1_alt": "OWNERNME1ALT",
    "owner2": "OWNERNME2",
    "owner2_alt": "OWNERNME2ALT",
    "addr": "PSTLADDRESS",
    "city": "PSTLCITY",
    "state": "PSTLSTATE",
    "zip5": "PSTLZIP5",
    "zip4": "PSTLZIP4",
    "site": "SITEADDRESS",
    "muni": "MUNI",
    "row": "isROW",
}

# Word-level replacements so spelling variants of one owner compare equal.
_WORDS = {
    "COMPANY": "CO", "CORPORATION": "CORP", "INCORPORATED": "INC", "LIMITED": "LTD",
    "AND": "&", "THE": "", "LLC.": "LLC", "L.L.C.": "LLC", "TRUSTEES": "TRUST", "TRUSTEE": "TRUST",
    "REVOCABLE": "REV", "LIVING": "", "ESTATE": "EST",
    "STREET": "ST", "AVENUE": "AVE", "ROAD": "RD", "DRIVE": "DR", "LANE": "LN", "COURT": "CT",
    "CIRCLE": "CIR", "BOULEVARD": "BLVD", "PLACE": "PL", "HIGHWAY": "HWY", "PARKWAY": "PKWY",
    "NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W",
    "POST": "PO", "OFFICE": "", "BOX": "BOX", "SUITE": "STE", "APARTMENT": "APT",
}


def _s(v):
    """Value to clean uppercase string ('' for None/NULL)."""
    if v is None:
        return ""
    v = str(v).strip()
    return "" if v.upper() in ("<NULL>", "NONE", "NULL") else v.upper()


def norm(text):
    """Normalize a name or address for comparing: uppercase, no punctuation, standard abbreviations."""
    t = _s(text)
    t = t.replace("P.O.", "PO").replace("L.L.C.", "LLC")
    t = re.sub(r"[.,'\"#]", " ", t)
    t = t.replace("&", " & ")
    words = [_WORDS.get(w, w) for w in t.split()]
    return " ".join(w for w in words if w)


def is_blank_owner(name):
    return norm(name) == ""


def zip_text(zip5, zip4):
    z5, z4 = _s(zip5), _s(zip4)
    if z5 and z4 and z4 not in ("0", "0000"):
        return z5 + "-" + z4.zfill(4)
    return z5


def label_lines(rec, f=DEFAULT_FIELDS):
    """Lines for one mailing label: names (Alt first-last order if present), street, city/state/zip."""
    name1 = _s(rec.get(f["owner1_alt"])) or _s(rec.get(f["owner1"]))
    name2 = _s(rec.get(f["owner2_alt"])) or _s(rec.get(f["owner2"]))
    lines = [name1]
    if name2 and norm(name2) != norm(name1):
        lines.append(name2)
    lines.append(_s(rec.get(f["addr"])))
    city = _s(rec.get(f["city"]))
    st = _s(rec.get(f["state"]))
    z = zip_text(rec.get(f["zip5"]), rec.get(f["zip4"]))
    lines.append((city + (", " if city else "") + st + ("  " + z if z else "")).strip())
    return [l for l in lines if l]


def is_absentee(rec, f=DEFAULT_FIELDS):
    """Owner's mailing street differs from the parcel's site address: usually a rental or a business owner elsewhere."""
    site, mail = norm(rec.get(f["site"])), norm(rec.get(f["addr"]))
    if not site or not mail:
        return False
    return site != mail


def build_mailing_list(records, subject_ids=(), f=DEFAULT_FIELDS, similar=0.88):
    """records: list of dicts (one per parcel in the notice area).

    Returns dict with:
      letters   - one entry per owner to mail (merged)
      parcels   - every input parcel with its letter number or an exclusion reason
      review    - near-duplicate owner pairs that were not merged
      counts    - the numbers for the summary
    """
    subject_ids = {str(s).strip() for s in subject_ids}
    letters = OrderedDict()      # key -> letter dict
    parcels, excluded = [], 0
    raw_owner_rows = set()

    for rec in records:
        pid = _s(rec.get(f["id"]))
        owner = rec.get(f["owner1"])
        row_flag = rec.get(f["row"]) if f.get("row") else None
        raw_owner_rows.add(_s(owner))
        p = {"parcel_id": pid, "owner": _s(owner), "site_address": _s(rec.get(f["site"])),
             "municipality": _s(rec.get(f["muni"])), "letter": "", "note": ""}
        if row_flag not in (None, "", 0, "0"):
            p["note"] = "excluded: right-of-way parcel (isROW)"
            excluded += 1
        elif is_blank_owner(owner):
            p["note"] = "excluded: no owner name (check the county record before mailing)"
            excluded += 1
        else:
            key = (norm(owner), norm(rec.get(f["addr"])))
            if key not in letters:
                letters[key] = {"names": set(), "lines": label_lines(rec, f), "parcels": [], "munis": set(),
                                "absentee": False, "subject_owner": False, "key": key}
            L = letters[key]
            L["names"].add(_s(owner))
            L["parcels"].append(pid)
            L["munis"].add(p["municipality"])
            L["absentee"] = L["absentee"] or is_absentee(rec, f)
            L["subject_owner"] = L["subject_owner"] or pid in subject_ids
            p["_key"] = key
        parcels.append(p)

    # Same normalized name at two different mailing addresses: keep both letters, flag for review.
    review = []
    keys = list(letters)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if a[0] == b[0]:
                review.append((a, b, "same owner name, different mailing addresses (both mailed)"))
            else:
                r = difflib.SequenceMatcher(None, a[0], b[0]).ratio()
                if r >= similar:
                    review.append((a, b, "similar owner names (%.0f%% alike), not merged" % (r * 100)))

    out_letters = []
    for n, (key, L) in enumerate(letters.items(), start=1):
        L["letter"] = n
        names = sorted(L["names"])
        out_letters.append({
            "letter": n,
            "label_lines": L["lines"],
            "owner_names_in_record": " | ".join(names),
            "merged_spellings": len(names) > 1,
            "parcel_count": len(L["parcels"]),
            "parcel_ids": " ".join(L["parcels"]),
            "municipalities": " | ".join(sorted(m for m in L["munis"] if m)),
            "absentee_owner": L["absentee"],
            "subject_owner": L["subject_owner"],
        })
    for p in parcels:
        k = p.pop("_key", None)
        if k is not None:
            p["letter"] = letters[k]["letter"]
            if p["parcel_id"] in subject_ids:
                p["note"] = "subject parcel"

    rv = [{"letter_a": letters[a]["letter"], "owner_a": " | ".join(sorted(letters[a]["names"])),
           "letter_b": letters[b]["letter"], "owner_b": " | ".join(sorted(letters[b]["names"])), "why": why}
          for a, b, why in review]

    counts = OrderedDict([
        ("parcels_in_notice_area", len(records)),
        ("owner_name_rows_as_recorded", len(raw_owner_rows)),
        ("parcels_excluded", excluded),
        ("letters_to_owners", len(out_letters)),
        ("owners_with_several_parcels", sum(1 for l in out_letters if l["parcel_count"] > 1)),
        ("letters_with_merged_spellings", sum(1 for l in out_letters if l["merged_spellings"])),
        ("absentee_owners", sum(1 for l in out_letters if l["absentee_owner"])),
        ("pairs_to_review", len(rv)),
    ])
    return {"letters": out_letters, "parcels": parcels, "review": rv, "counts": counts}


def clerks_to_notify(munis_within_1000ft, home_muni):
    """Municipalities (other than the one doing the rezoning) with land within 1,000 ft."""
    home = norm(home_muni)
    return sorted({_s(m) for m in munis_within_1000ft if _s(m) and norm(m) != home})


def write_outputs(result, clerks, out_dir, meta):
    """CSV files, a summary text file and the label PDF. Returns the list of files written."""
    os.makedirs(out_dir, exist_ok=True)
    files = []

    def w(name, rows, cols):
        path = os.path.join(out_dir, name)
        with open(path, "w", newline="", encoding="utf-8") as fh:
            wr = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            wr.writeheader()
            for r in rows:
                wr.writerow(r)
        files.append(path)

    letters = []
    for l in result["letters"]:
        r = dict(l)
        lines = l["label_lines"] + ["", "", "", ""]
        r.update({"line1": lines[0], "line2": lines[1], "line3": lines[2], "line4": lines[3]})
        letters.append(r)
    w("mailing_list.csv", letters, ["letter", "line1", "line2", "line3", "line4", "parcel_count", "parcel_ids",
                                    "municipalities", "absentee_owner", "subject_owner", "merged_spellings",
                                    "owner_names_in_record"])
    w("parcels_in_notice_area.csv", result["parcels"], ["parcel_id", "owner", "site_address", "municipality", "letter", "note"])
    w("review.csv", result["review"], ["letter_a", "owner_a", "letter_b", "owner_b", "why"])
    w("clerks_to_notify.csv", [{"municipality": c, "reason": "land within 1,000 ft of the rezoning"} for c in clerks],
      ["municipality", "reason"])

    path = os.path.join(out_dir, "summary.txt")
    with open(path, "w", encoding="utf-8") as fh:
        for k, v in meta.items():
            fh.write("%s: %s\n" % (k, v))
        fh.write("\n")
        for k, v in result["counts"].items():
            fh.write("%s: %s\n" % (k.replace("_", " "), v))
        fh.write("clerks to notify (1,000 ft): %s\n" % (", ".join(clerks) or "none"))
    files.append(path)

    pdf = os.path.join(out_dir, "labels_avery5160.pdf")
    avery5160_pdf([l["label_lines"] for l in result["letters"]] +
                  [["CLERK, " + c, "(add the clerk's mailing address)"] for c in clerks], pdf)
    files.append(pdf)
    return files


def avery5160_pdf(labels, path):
    """Avery 5160 / 8160: 30 labels per US Letter sheet, 3 x 10, 2-5/8 in x 1 in."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    top, left, w, h, gap = 0.5, 0.1875, 2.625, 1.0, 0.125
    with PdfPages(path) as pdf:
        for start in range(0, max(len(labels), 1), 30):
            fig = plt.figure(figsize=(8.5, 11))
            for i, lines in enumerate(labels[start:start + 30]):
                col, row = i % 3, i // 3
                x = left + col * (w + gap) + 0.15
                y = 11 - top - row * h - 0.22
                fig.text(x / 8.5, y / 11, "\n".join(lines[:4]), fontsize=8.5, family="DejaVu Sans",
                         va="top", ha="left", linespacing=1.25)
            pdf.savefig(fig)
            plt.close(fig)
