# -*- coding: utf-8 -*-
"""Tests for notice_core with made-up rows shaped like the Nov 8 hand run (29 parcels, 17 owner rows).
Run: python tests/test_notice_core.py   (no arcpy needed)"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import notice_core as nc


def row(pid, o1, addr, site="", muni="TOWN OF SHEBOYGAN", alt="", o2="", city="SHEBOYGAN", st="WI", z5="53083", z4="", rowflag=0):
    return {"PARCELID": pid, "OWNERNME1": o1, "OWNERNME1ALT": alt, "OWNERNME2": o2, "OWNERNME2ALT": "",
            "PSTLADDRESS": addr, "PSTLCITY": city, "PSTLSTATE": st, "PSTLZIP5": z5, "PSTLZIP4": z4,
            "SITEADDRESS": site, "MUNI": muni, "isROW": rowflag}


def sample():
    r = [row("SUBJ", "EXCAVATING ACQUISITION LLC", "100 MAIN ST", "PLAYBIRD RD")]
    r += [row("C%02d" % i, "CONCORD 5 LLC", "PO BOX 12", "COBBLE DR") for i in range(12)]
    r += [row("T1", "TOWN OF SHEBOYGAN", "5821 COUNTY ROAD EE", "N 40TH ST"),
          row("T2", "TOWN OF SHEBOYGAN", "5821 County Rd EE", "")]
    r += [row("M1", "PETERSON & SONS CO LLC", "N7337 DAIRYLAND DR", "N7337 DAIRYLAND DR", "TOWN OF MOSEL"),
          row("M2", "PETERSON & SONS COMPANY LLC", "N7337 Dairyland Drive", "", "TOWN OF MOSEL"),
          row("M3", "HAESE, JEROME A", "2900 ELM AVE", "3616 PLAYBIRD RD", "TOWN OF MOSEL", alt="JEROME A HAESE", z4="1234")]
    r += [row("X%d" % i, n, "%d OAK ST" % i, "%d OAK ST" % i) for i, n in enumerate(
        ["CBMACHINE SALES LLC", "FUZZY FROG LLC", "GUTSCHOW COMPANY LLC", "LEE, ELVIS", "MEADOWLAKE APARTMENTS LLC",
         "PALECEK, CHAD M", "PREMIER GREEN MEADOWS APT LLC", "ROGERS EQUITY GROUP IV LLC", "SPAETH, GREGORY L",
         "TRIEU, HENRY QUOC"])]
    r += [row("BLANK", "", "", "")]
    return r


def test_counts():
    recs = sample()
    assert len(recs) == 29
    res = nc.build_mailing_list(recs, subject_ids=["SUBJ"])
    c = res["counts"]
    assert c["parcels_in_notice_area"] == 29
    assert c["owner_name_rows_as_recorded"] == 17, c
    assert c["parcels_excluded"] == 1
    assert c["letters_to_owners"] == 15, c            # 16 real owners minus... see below
    # 17 rows - blank - Peterson duplicate = 15 owners with names (subject owner included)
    peter = [l for l in res["letters"] if "PETERSON" in l["owner_names_in_record"]]
    assert len(peter) == 1 and peter[0]["merged_spellings"] and peter[0]["parcel_count"] == 2
    concord = [l for l in res["letters"] if l["owner_names_in_record"] == "CONCORD 5 LLC"][0]
    assert concord["parcel_count"] == 12
    town = [l for l in res["letters"] if l["owner_names_in_record"] == "TOWN OF SHEBOYGAN"][0]
    assert town["parcel_count"] == 2                   # "COUNTY ROAD" = "County Rd"
    subj = [l for l in res["letters"] if l["subject_owner"]]
    assert len(subj) == 1
    blank = [p for p in res["parcels"] if p["parcel_id"] == "BLANK"][0]
    assert blank["note"].startswith("excluded") and blank["letter"] == ""


def test_labels_and_flags():
    res = nc.build_mailing_list(sample())
    haese = [l for l in res["letters"] if "HAESE" in l["owner_names_in_record"]][0]
    assert haese["label_lines"] == ["JEROME A HAESE", "2900 ELM AVE", "SHEBOYGAN, WI  53083-1234"]
    assert haese["absentee_owner"] is True
    lee = [l for l in res["letters"] if "LEE" in l["owner_names_in_record"]][0]
    assert lee["absentee_owner"] is False


def test_review_and_rows():
    recs = [row("A", "SMITH JOHN", "1 A ST"), row("B", "SMITH JOHN", "9 B ST"),
            row("C", "SMITH JOHN A", "5 C ST"), row("R", "STATE OF WISCONSIN", "X", rowflag=1)]
    res = nc.build_mailing_list(recs)
    assert res["counts"]["letters_to_owners"] == 3
    assert res["counts"]["parcels_excluded"] == 1
    whys = [r["why"] for r in res["review"]]
    assert any("different mailing" in w for w in whys)
    assert any("similar" in w for w in whys)


def test_clerks_and_files():
    assert nc.clerks_to_notify(["TOWN OF SHEBOYGAN", "TOWN OF MOSEL", "Town of Mosel", ""], "Town of Sheboygan") == ["TOWN OF MOSEL"]
    res = nc.build_mailing_list(sample(), subject_ids=["SUBJ"])
    d = tempfile.mkdtemp()
    files = nc.write_outputs(res, ["TOWN OF MOSEL"], d, {"subject": "SUBJ", "distance": "200 ft"})
    assert all(os.path.getsize(f) > 0 for f in files)
    assert open(os.path.join(d, "labels_avery5160.pdf"), "rb").read(4) == b"%PDF"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
