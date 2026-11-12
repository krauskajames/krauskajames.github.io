"""Build the practice kit for roadmap item 57 (practice ALTA-style survey drawing in Civil 3D).

Real:      the eight boundary courses and two tie courses, from a certified survey map submitted to the
           City of New Berlin (draft dated October 24, 2025; see README.md).
Simulated: everything else. Found-monument positions, the building, pavement, utilities, trees, ground
           shots, elevations, the levelling loop and the stakeout design are invented for practice.

Writes csm_courses.csv, field_shots_PNEZD.csv, level_loop.csv, stakeout_design.csv and ANSWER_KEY.md.
Usage: python build_kit.py
"""
import csv, math, random
random.seed(57)
TIES = [("N", 0, 53, 38, "W", 1327.45, "along the east line of the SE 1/4"),
        ("S", 88, 5, 29, "W", 198.38, "along the south line of the NE 1/4 of the SE 1/4 to the west right-of-way of S. Moorland Road")]
COURSES = [("S", 88, 5, 29, "W", 1135.01, "south line of the NE 1/4 of the SE 1/4"),
           ("N", 1, 13, 51, "W", 158.57, "west line of the NE 1/4 of the SE 1/4, to the Interstate 43 right-of-way"),
           ("N", 54, 14, 19, "E", 272.29, "Interstate 43 southerly right-of-way"),
           ("N", 81, 36, 30, "E", 398.06, "Interstate 43 southerly right-of-way"),
           ("S", 79, 24, 35, "E", 155.82, "Interstate 43 southerly right-of-way"),
           ("S", 1, 21, 38, "E", 288.47, ""),
           ("N", 88, 5, 29, "E", 362.08, "to the west right-of-way of S. Moorland Road"),
           ("S", 1, 59, 46, "E", 33.00, "S. Moorland Road west right-of-way, to the point of beginning")]
STATED_AREA = 247672
N0, E0 = 5000.00, 6500.00                      # assumed coordinates of the point of beginning
def brg(c): return f"{c[0]} {c[1]:02d}°{c[2]:02d}'{c[3]:02d}\" {c[4]}"
def delta(c):
    a = math.radians(c[1] + c[2] / 60 + c[3] / 3600)
    return c[5] * math.cos(a) * (1 if c[0] == "N" else -1), c[5] * math.sin(a) * (1 if c[4] == "E" else -1)
n, e = N0, E0; corners = [(n, e)]; rows = []
for c in COURSES:
    dn, de = delta(c); n += dn; e += de; corners.append((n, e)); rows.append((c, dn, de, n, e))
mis_n, mis_e = n - N0, e - E0; mis = math.hypot(mis_n, mis_e); per = sum(c[5] for c in COURSES)
area = abs(sum(corners[i][1] * corners[i + 1][0] - corners[i + 1][1] * corners[i][0] for i in range(len(corners) - 1))) / 2
poly = corners[:-1]
with open("csm_courses.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["type", "course", "bearing", "distance_ft", "along"])
    for i, c in enumerate(TIES, 1): w.writerow(["tie", f"T{i}", brg(c), f"{c[5]:.2f}", c[6]])
    for i, c in enumerate(COURSES, 1): w.writerow(["boundary", i, brg(c), f"{c[5]:.2f}", c[6]])

# local frame: u runs west along the south line from the point of beginning, v runs north from it
a0 = math.radians(88 + 5 / 60 + 29 / 3600); ux, uy = -math.sin(a0), -math.cos(a0); vx, vy = -uy, ux   # (E, N) components
if vy < 0: vx, vy = -vx, -vy
def NE(u, v): return N0 + u * uy + v * vy, E0 + u * ux + v * vx
def inside(n, e):
    hit = False
    for i in range(len(poly)):
        (n1, e1), (n2, e2) = poly[i], poly[(i + 1) % len(poly)]
        if (n1 > n) != (n2 > n) and e < (e2 - e1) * (n - n1) / (n2 - n1) + e1: hit = not hit
    return hit
def ground(u, v): return 858.40 + 0.0042 * u + 0.011 * v + 0.35 * math.sin(u / 140) * math.cos(v / 90)
pts = []
def add(p, u, v, code, z=None, exact=None):
    n, e = exact if exact else NE(u, v)
    pts.append((p, round(n, 2), round(e, 2), round(ground(u, v) if z is None else z, 2), code))
CP = {1: (300, 16.5), 2: (610, 60), 3: (980, 25)}
for k, (u, v) in CP.items(): add(k, u, v, f"CP{k}")
BM = (392, 34); BM_Z = 860.00; add(4, *BM, "BM1 TOP NUT HYD", z=BM_Z)
found = {}
for i, (n, e) in enumerate(poly):
    if i == 5: pts.append((101 + i, round(n, 2), round(e, 2), 0, "IRS 3/4 REBAR SET")); found[i] = (n, e); continue
    dn, de = random.gauss(0, 0.05), random.gauss(0, 0.05); found[i] = (n + dn, e + de)
    pts.append((101 + i, round(n + dn, 2), round(e + de, 2), 0, "IPF 1IN" if i % 2 == 0 else "IRF 3/4 REBAR"))
def rel(n, e):   # back to local frame, for elevations
    dn, de = n - N0, e - E0; return dn * uy + de * ux, dn * vy + de * vx
pts = [(p, n, e, round(ground(*rel(n, e)), 2) if z == 0 else z, c) for p, n, e, z, c in pts]
BLD = [(640, 80), (820, 80), (820, 190), (640, 190)]; FF = 865.20
for i, (u, v) in enumerate(BLD): add(201 + i, u, v, "BLDG1" + (" B" if i == 0 else " CLS" if i == 3 else ""))
LOT = [(420, 45), (600, 45), (600, 250), (420, 250)]
for i, (u, v) in enumerate(LOT): add(301 + i, u, v, "EP1" + (" B" if i == 0 else " CLS" if i == 3 else ""))
k = 311
for line, v in (("EP2", 4.5), ("EP3", 28.5)):
    us = list(range(6, 420, 59)) + [420]
    for i, u in enumerate(us): add(k, u, v, line + (" B" if i == 0 else " E" if i == len(us) - 1 else "")); k += 1
for p, (u, v, c) in enumerate([(12, 31, "SIGN"), (392, 34, "HYD"), (385, 38, "WV"), (210, 16.5, "SSMH RIM"), (520, 30, "SSMH RIM"),
                               (430, 240, "CB RIM"), (590, 55, "CB RIM"), (450, 100, "LP"), (570, 100, "LP"), (450, 200, "LP"), (570, 200, "LP")], 401): add(p, u, v, c)
fence = []
for i in (2, 3, 4):   # 2 ft inside the Interstate 43 line
    (n1, e1), (n2, e2) = poly[i], poly[i + 1]; L = math.hypot(n2 - n1, e2 - e1); nx, ex = (e2 - e1) / L, -(n2 - n1) / L
    for t in (0.03, 0.5, 0.97): fence.append((n1 + (n2 - n1) * t - 2 * nx * (1 if inside(n1 + (n2 - n1) * 0.5 - 2 * nx, e1 + (e2 - e1) * 0.5 - 2 * ex) else -1),
                                              e1 + (e2 - e1) * t - 2 * ex * (1 if inside(n1 + (n2 - n1) * 0.5 - 2 * nx, e1 + (e2 - e1) * 0.5 - 2 * ex) else -1)))
for i, (n, e) in enumerate(fence): pts.append((501 + i, round(n, 2), round(e, 2), round(ground(*rel(n, e)), 2), "FNC1" + (" B" if i == 0 else " E" if i == len(fence) - 1 else "")))
for p, (u, v) in enumerate([(900, 40), (960, 60), (1040, 50), (1100, 90), (1000, 150), (900, 230), (760, 250), (1090, 30)], 601): add(p, u, v, f"TREE {random.choice([8, 10, 12, 14, 18, 24])}IN")
p = 1001
for u in range(390, 1130, 60):
    for v in range(15, 320, 45):
        n, e = NE(u, v)
        in_bld = BLD[0][0] - 3 <= u <= BLD[1][0] + 3 and BLD[0][1] - 3 <= v <= BLD[2][1] + 3
        if inside(n, e) and not in_bld: add(p, u, v, "GND", z=ground(u, v) + random.gauss(0, 0.03)); p += 1
for u in range(30, 390, 90): add(p, u, 16.5, "GND", z=ground(u, 16.5) + random.gauss(0, 0.02)); p += 1
with open("field_shots_PNEZD.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    for r in sorted(pts): w.writerow([r[0], f"{r[1]:.2f}", f"{r[2]:.2f}", f"{r[3]:.2f}", r[4]])

# levelling loop: BM1 -> TP1 -> TP2 -> TP3 -> BM1, with a side shot to the finished floor
true = [BM_Z, 861.37, 863.02, 862.11, BM_Z]; legs = []; err = [0.00, 0.01, 0.00, 0.01]
for i in range(4):
    hi = max(true[i], true[i + 1]) + random.choice([3.1, 3.6, 4.2, 4.8]) + random.randint(0, 9) / 100
    legs.append((round(hi - true[i], 2), round(hi - true[i + 1] - err[i], 2)))
ff_fs = round((true[2] + legs[2][0]) - FF, 2)
with open("level_loop.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["station", "backsight_ft", "foresight_ft", "note"])
    names = ["BM1", "TP1", "TP2", "TP3", "BM1"]
    w.writerow(["BM1", f"{legs[0][0]:.2f}", "", f"benchmark, elevation {BM_Z:.2f} (assumed)"])
    for i in range(1, 4):
        w.writerow([names[i], f"{legs[i][0]:.2f}", f"{legs[i - 1][1]:.2f}", "turning point"])
        if i == 2: w.writerow(["FF", "", f"{ff_fs:.2f}", "side shot from the same setup as the TP2 backsight: finished floor at the building door"])
    w.writerow(["BM1", "", f"{legs[3][1]:.2f}", "close on the benchmark"])
elev = [BM_Z]; his = []
for bs, fs in legs: his.append(elev[-1] + bs); elev.append(his[-1] - fs)
loop_mis = elev[-1] - BM_Z; tol = 0.02 * math.sqrt(4)
adj = [elev[i] - loop_mis * i / 4 for i in range(5)]

# stakeout: occupy CP3, backsight CP2 (both sight lines clear the building), stake a proposed 60 x 40 ft storage building
ADD = [(840, 100), (900, 100), (900, 140), (840, 140)]; OFF = [(830, 100), (910, 100), (910, 140), (830, 140)]
occ, bs_pt = [tuple(round(x, 2) for x in NE(*CP[k])) for k in (3, 2)]   # the coordinates as published in the field file
def az(a, b): return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 360
def dms(x): d = int(x); m = int((x - d) * 60); s = round(((x - d) * 60 - m) * 60); m, s = (m + 1, 0) if s == 60 else (m, s); d, m = (d + 1, 0) if m == 60 else (d, m); return f"{d}°{m:02d}'{s:02d}\""
az_bs = az(occ, bs_pt); stake = []
with open("stakeout_design.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["point", "northing", "easting", "description"])
    for lab, group in (("A", ADD), ("O", OFF)):
        for i, (u, v) in enumerate(group, 1):
            n, e = NE(u, v); n, e = round(n, 2), round(e, 2)
            w.writerow([f"{lab}{i}", f"{n:.2f}", f"{e:.2f}", "proposed storage building corner" if lab == "A" else f"10 ft offset stake for corner A{i}, on the long wall line"])
            stake.append((f"{lab}{i}", n, e, (az(occ, (n, e)) - az_bs) % 360, math.hypot(n - occ[0], e - occ[1])))

K = ["# Answer key", "", "Work each part yourself first. Every number here was computed by `build_kit.py`, not typed by hand.", "",
     "## 1. Boundary closure", "", "| Course | Bearing | Distance (ft) | Latitude (ft) | Departure (ft) | Northing | Easting |", "|---|---|---|---|---|---|---|",
     f"| POB | | | | | {N0:.2f} | {E0:.2f} |"]
for i, (c, dn, de, n, e) in enumerate(rows, 1): K.append(f"| {i} | {brg(c)} | {c[5]:.2f} | {dn:+.3f} | {de:+.3f} | {n:.2f} | {e:.2f} |")
K += ["", f"- Perimeter: {per:.2f} ft", f"- Misclosure: {mis:.3f} ft (latitude {mis_n:+.3f}, departure {mis_e:+.3f})", f"- Precision: 1 in {round(per / mis):,}",
      f"- Area by coordinates: {area:,.0f} sq ft ({area / 43560:.4f} acres). The map states {STATED_AREA:,} sq ft ({STATED_AREA / 43560:.4f} acres), a difference of {abs(area - STATED_AREA):.0f} sq ft from rounding in the bearings and distances.", "",
      "## 2. Found monuments compared with the record corners", "", "Simulated. Point 106 was set at the record position; the others were 'found' a little off, as real monuments are.", "",
      "| Point | Corner at the end of course | Record N | Record E | Found N | Found E | Found minus record (ft) |", "|---|---|---|---|---|---|---|"]
for i, (n, e) in enumerate(poly):
    fn, fe = round(found[i][0], 2), round(found[i][1], 2); K.append(f"| {101 + i} | {'POB' if i == 0 else i} | {n:.2f} | {e:.2f} | {fn:.2f} | {fe:.2f} | {math.hypot(fn - round(n, 2), fe - round(e, 2)):.2f} |")
K += ["", "## 3. Levelling loop", "", "| Station | BS | HI | FS | Elevation | Adjusted elevation |", "|---|---|---|---|---|---|", f"| BM1 | {legs[0][0]:.2f} | {his[0]:.2f} | | {BM_Z:.2f} | {BM_Z:.2f} |"]
for i in range(1, 4): K.append(f"| TP{i} | {legs[i][0]:.2f} | {his[i]:.2f} | {legs[i - 1][1]:.2f} | {elev[i]:.2f} | {adj[i]:.2f} |")
K += [f"| BM1 | | | {legs[3][1]:.2f} | {elev[4]:.2f} | {adj[4]:.2f} |", "",
      f"- Check: sum of backsights {sum(l[0] for l in legs):.2f} minus sum of foresights {sum(l[1] for l in legs):.2f} = {sum(l[0] for l in legs) - sum(l[1] for l in legs):+.2f} ft, the same as the loop misclosure.",
      f"- Misclosure: {loop_mis:+.2f} ft. This exercise's tolerance is 0.02 ft × √(number of setups) = {tol:.2f} ft for 4 setups, so the loop {'passes' if abs(loop_mis) <= tol + 1e-9 else 'fails'}. That tolerance is a classroom figure chosen for the exercise; a real job uses the standard its specification names.",
      f"- Adjustment: spread the misclosure evenly, {-loop_mis / 4:+.3f} ft per setup.",
      f"- Finished floor: HI at that setup {his[2]:.2f} minus foresight {ff_fs:.2f} = {his[2] - ff_fs:.2f} ft (unadjusted).", "",
      "## 4. Stakeout from CP3, backsight CP2", "", f"Instrument at CP3 (N {occ[0]:.2f}, E {occ[1]:.2f}), backsight CP2 (N {bs_pt[0]:.2f}, E {bs_pt[1]:.2f}). Azimuth to the backsight: {dms(az_bs)}.", "",
      "| Point | Northing | Easting | Angle right from backsight | Horizontal distance (ft) |", "|---|---|---|---|---|"]
for lab, n, e, ang, dist in stake: K.append(f"| {lab} | {n:.2f} | {e:.2f} | {dms(ang)} | {dist:.2f} |")
K += ["", "Check: A1 to A2 should measure 60.00 ft and A2 to A3 40.00 ft, and the two diagonals should match at "
      f"{math.hypot(60, 40):.2f} ft."]
open("ANSWER_KEY.md", "w", encoding="utf-8").write("\n".join(K) + "\n")
print(f"closure {mis:.3f} ft, 1:{round(per / mis):,}; area {area:,.0f}; {len(pts)} field shots; loop misclosure {loop_mis:+.2f} (tol {tol:.2f})")
