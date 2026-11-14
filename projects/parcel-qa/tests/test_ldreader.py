"""Answer key for the legal description reader: the five Sheboygan County parcels James drafted
by hand with COGO in an ArcGIS Pro 3.7.3 parcel fabric (see parcel-qa.html, "Five parcels, drawn
from their deeds"). The reader must reproduce his course counts, misclosures and areas from the
tax-roll text alone, plus a set of formats seen elsewhere in the county's tax roll.

    python3 tests/test_ldreader.py
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "legal_desc"))
import ldreader as L

# Tax-roll text (TAXDSCRP, Nov 2026) -> James's hand-drafted result
KEY = {
    "59004034130": ("PRT SE SE,SEC 14,COM AT NE COR,SD1/4,TH N89 DEG 41'W 485.6',S8 DEG 40'W 113.4', S83 DEG 27'E 506.05'TO E LN OF SEC,TH N 167.25'TO BEG.",
                    dict(ties=0, courses=4, misclose=0.12, acres=1.59)),
    "59008093220": ("A-13670 - PRT SE NE & NE SE, SEC 9,COM AT SW COR SE NE,TH N0 DEG 44'42\"W 363',E 468.62',S25 DEG 42'W 292.45' ALG CENLN HUMPHREY RD & CTH N,S47 DEG 04'W 457.45'ALG CENLN,TH N0 DEG 34'54\"W 212.15'TO BEG.",
                    dict(ties=0, courses=5, misclose=0.00, acres=3.65)),
    "59111521840": ("B-1984 - PRT SW SE,SEC 20, COM AT NE COR OF SD SW SE,TH S89 DEG 08'58\"W 835.44',S28 DEG 53'33\"E 478.49',N62 DEG 04'46\"E 6.55',N28 DEG 13'W 129.48',N80 DEG 15'E 670.59' TH N0 DEG 22'33\"W 200.61'TO BEG.",
                    dict(ties=0, courses=6, misclose=0.00, acres=4.50)),
    # misclosed as recorded; James's compass-rule area is 9.83 ac, the raw closing figure is 9.87 ac
    "59010122560": ("PRT SW NW,SEC 11,COM AT SW COR SD1/4,TH E 425.47',S89 DEG 22'17\"E 304.60',N0 DEG 3'39\"W 582.58',N88 DEG 35' 9\"W 729.74',S0 DEG 3'39\"E 80.63',TH S 511.90'TO BEG, SUBJ TO HWY CONV AS REC IN VOL 385 P 158-59.(VOL 404 P 361-62,VOL 854 P 750)",
                    dict(ties=0, courses=6, misclose=4.72, acres=9.87)),
    "59010122221": ("PRT W1/2 SE1/4,SEC 9,COM S89 DEG 30'56\"E 50'FROM CEN SD SEC,TH CONT S89 DEG 30'56\"E 1283.98',S0 DEG 13'54\"W 1161',N89 DEG 34'48\"W 931.48',S0 DEG 06'51\"W 1002.50',N89 DEG 34'48\"W 352.84'TO E R/W CTH E,N0 DEG 3'25\"E 275.28',N2 DEG 55'10\"E 100.12',N00 DEG 03'25\"E 300',N05 DEG 39'13\"W 62.79', S89 DEG 53'09\"E 218.82',N0 DEG 06'51\"E 330',N89 DEG 53' 09\"W 213.66',N05 DEG 46'05\"E 7.56',N0 DEG 03'25\"E 247.59' S82 DEG 33'09\"E 385.74',N0 DEG 6'51\"E 250',N82 DEG 33'09\"W 385.99',TH N0 DEG 3'25\" E 592.03'TO B",
                    dict(ties=1, courses=18, misclose=0.11, acres=38.44)),
}

# Other formats from the county's tax roll: (text, expected status, ties, courses, misclose or None)
FORMATS = [
    ("two ties, one distance-first; a missing comma",
     "COM 1316.57'W & N0 DEG 22'28\"E 512.98'FROM E1/4 COR SD SEC,TH N69 DEG 46'30\"W 421.25',N18 DEG 40'54\"E 323.03',N89 DEG 57'31\"E294.75',S0 DEG 22'28\"W 4.86' N89 DEG 58'46\"E 123.75',S0 DEG 22'28\"W 297',S89 DEG 58' 46\"W 123.75',TH S0 DEG 22' 28\"W 150'TO BEG.",
     "parsed", 2, 8, 0.01),
    ("degrees with no minutes, TH CONT",
     "COM N0 DEG E 794.77'FROM W1/4 COR SD SEC, TH CONT N0 DEG E 166.88', N90 DEG E 256.24',S15 DEG 39'52\"W 173.32',TH S90 DEG W 209.44'TO BEG.",
     "parsed", 1, 4, 0.00),
    ("courses that run to a line, no distance",
     "PRT SW SW,SEC 14,COM 685.25' N OF SW COR SD1/4,TH N89 DEG 25'31\"E 335',N 650'TO N LINE SW SW,W TO NW COR SD1/4,TH S TO BEG.",
     "partial", 1, 4, None),
    ("road names are not directions",
     "COM IN CEN OF CTH\"DA\" N88 DEG 15'E 686.8'FROM SW COR SD SEC,TH N88 DEG 15'E 254.36',N1 DEG 45'W 211.25',S88 DEG 15'W 254.36',TH S1 DEG 45'E 211.25'TO BEG",
     "parsed", 1, 4, 0.00),
    ("due-direction jogs",
     "COM 672.75' W OF SE COR SD1/4,TH N0 DEG 34'W 435.60',W 200',S0 DEG 34'E 134.60',W 5',S0 DEG 34'E 83',E 5',S0 DEG 34'E 37',E 5',S0 DEG 34'E 83',W 5',S0 DEG 34'E 98'TO S LINE OF SEC,TH E 200'TO BEG.",
     "parsed", 1, 12, 0.00),
    ("degree signs, curly quotes, FEET",
     "COM AT NW COR, TH S00°12'01\"E 100.00’, TH N89°47'59\"E 100.00 FEET, TH N00°12'01\"W 100.00’, TH S89°47'59\"W 100.00’ TO POB",
     "parsed", 0, 4, 0.00),
    ("record values in parentheses are set aside",
     "COM AT SE COR SD SE1/4, TH S89 DEG 07'38\"W 100',(RECD S87 DEG 26'26\"W 101') N0 DEG 52'22\"W (RECD N02 DEG W) 100', TH N89 DEG 07'38\"E 100', TH S0 DEG 52'22\"E 100' TO BEG",
     "parsed", 0, 4, 0.00),
    ("half-foot distances and * as a degree sign",
     "COM AT NW COR LOT 6C BEING THE POB, TH S 90*E 136 1/2', TH S 50', TH N 90*W 136 1/2', TH N 50' TO POB",
     "parsed", 0, 4, 0.00),
    ("a point of beginning in the middle of the text",
     "COM AT NW COR SW1/4 SEC 34, TH S 00*34'17\" W ALG W LN SW1/4 SEC 34 697.72' TO SELY ROW LN OF UNION PACIFIC RR AND THE POINT OF BEG; TH S 43*06'29\" W 161.43', TH S 56*05'38\" E 338.95', TH S 54*06'07\" E 63.61', TH S 71*12'31\" E 324', TH N 18*47'29\" E 258', TH N 71*12'31\" W 291.57', TH N 56*05'38\" W 325.19' TO ROW LN, TH S 43*06'29\" W 97.22' TO POB 3.96 A",
     "parsed", 1, 8, 0.00),
    ("a transposed digit is reported, not hidden",
     "COM AT N1/4 COR,SD SEC,TH S88 DEG 43'16\"W 834.89',S03 DEG 09'00\"E 233.90',S00 DEG 27'15\"W 757.56',N88 DEG 43' 16\"E 823.89',TH N00 DEG 27' 15\"W 991.35'TO BEG.",
     "parsed", 0, 5, 12.01),
    ("courses that end back at the point of commencement",
     "COM 674.86' N OF S1/4 COR,TH S89 DEG 11' 28\"E 975.03',S0 DEG 22'26\"W 674.81'TO S LINE OF SEC,TH N89 DEG 11'28\"W 970.63'TO BEG.",
     "parsed", 1, 4, 0.00),
    ("a curve, closed on its chord",
     "BEG AT NW COR LOT 1, TH N90 DEG E 100', TH SELY 31.42' ALONG THE ARC OF A CURVE TO THE RIGHT HAVING A RADIUS OF 20', THE CHORD OF WHICH BEARS S45 DEG E 28.28', TH S 80', TH W 120', TH N 100' TO BEG",
     "parsed", 0, 5, 0.00),
]

def main():
    bad = 0
    for pid, (txt, k) in KEY.items():
        R = L.parse(txt)
        got = dict(ties=len(R.ties), courses=len(R.courses), misclose=round(R.misclose, 2), acres=round(R.area_sqft / 43560, 2))
        ok = got == k
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {pid}: {got}" + ("" if ok else f"  expected {k}"))
    for name, txt, st, nt, nc, mc in FORMATS:
        R = L.parse(txt)
        got = (R.status, len(R.ties), len(R.courses), None if R.misclose is None else round(R.misclose, 2))
        ok = got == (st, nt, nc, mc)
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}: {got}" + ("" if ok else f"  expected {(st, nt, nc, mc)}"))
    # traverse file round trip: re-reading the DD lines must give the same misclose
    R = L.parse(KEY["59010122560"][0])
    tf = L.traverse_file(R, 0, 0)
    assert tf.startswith("DT QB\r\nDU DMS\r\nSP "), tf
    x = y = 0.0
    for line in tf.splitlines()[3:]:
        _, b, d = line.split()
        ns, ew = b[0], b[-1]; dd, mm, ss = (float(v) for v in b[1:-1].split("-"))
        a = dd + mm / 60 + ss / 3600
        az = {("N", "E"): a, ("S", "E"): 180 - a, ("S", "W"): 180 + a, ("N", "W"): 360 - a}[(ns, ew)]
        x += float(d) * math.sin(math.radians(az)); y += float(d) * math.cos(math.radians(az))
    rt = round(math.hypot(x, y), 2)
    print(f"{'ok  ' if rt == 4.72 else 'FAIL'} traverse file round trip misclose {rt}")
    bad += rt != 4.72
    print("all passed" if not bad else f"{bad} failed"); sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
