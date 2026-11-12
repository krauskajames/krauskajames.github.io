"""Draw preview.png: the record boundary with the simulated features from field_shots_PNEZD.csv."""
import csv
from PIL import Image, ImageDraw, ImageFont
P = {int(r[0]): (float(r[1]), float(r[2]), float(r[3]), r[4]) for r in csv.reader(open("field_shots_PNEZD.csv"))}
S = list(csv.DictReader(open("stakeout_design.csv"))); q = {r["point"]: (float(r["northing"]), float(r["easting"])) for r in S}
poly = [P[i][:2] for i in range(101, 109)]
ns = [v[0] for v in P.values()]; es = [v[1] for v in P.values()]; W, H, pad = 1500, 620, 50
s = min((W - 2 * pad) / (max(es) - min(es)), (H - 2 * pad - 40) / (max(ns) - min(ns)))
X = lambda e: pad + (e - min(es)) * s; Y = lambda n: H - pad - (n - min(ns)) * s
im = Image.new("RGB", (W, H), "white"); dr = ImageDraw.Draw(im)
try: f = ImageFont.truetype("DejaVuSans.ttf", 15); fb = ImageFont.truetype("DejaVuSans-Bold.ttf", 17)
except OSError: f = fb = ImageFont.load_default()
dr.line([(X(e), Y(n)) for n, e in poly + [poly[0]]], fill=(20, 20, 20), width=3)
def line(prefix, col, close=False, w=2):
    pts = [(X(v[1]), Y(v[0])) for k, v in sorted(P.items()) if v[3].split()[0] == prefix]
    dr.line(pts + pts[:1] if close else pts, fill=col, width=w)
line("BLDG1", (120, 60, 20), True, 3); line("EP1", (110, 110, 110), True); line("EP2", (110, 110, 110)); line("EP3", (110, 110, 110)); line("FNC1", (160, 120, 60))
for k, (n, e, z, c) in P.items():
    x, y = X(e), Y(n); t = c.split()[0]
    if t == "GND": dr.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(150, 150, 150))
    elif t.startswith("CP"): dr.polygon([(x, y - 7), (x - 6, y + 5), (x + 6, y + 5)], outline=(200, 0, 0)); dr.text((x + 8, y - 8), c, font=f, fill=(200, 0, 0))
    elif t in ("IPF", "IRF", "IRS"): dr.ellipse([x - 5, y - 5, x + 5, y + 5], outline=(0, 0, 0), width=2)
    elif t == "TREE": dr.ellipse([x - 5, y - 5, x + 5, y + 5], outline=(40, 130, 60), width=2)
    elif t in ("SSMH", "CB", "HYD", "WV", "LP", "SIGN", "BM1"): dr.rectangle([x - 3, y - 3, x + 3, y + 3], outline=(30, 80, 170), width=2)
box = [(X(q[f"A{i}"][1]), Y(q[f"A{i}"][0])) for i in (1, 2, 3, 4)]; dr.line(box + box[:1], fill=(200, 0, 0), width=2)
dr.text((pad, 12), "Practice kit preview: record boundary (black) with simulated building, pavement, fence, utilities, trees and ground shots", font=fb, fill=(20, 20, 20))
dr.text((pad, H - 34), "Black circles: monuments. Red triangles: control. Red box: stakeout design. Blue squares: utilities. Grey dots: ground shots. North is up.", font=f, fill=(60, 60, 60))
dr.text((X(6500) - 160, Y(5000) + 8), "POB at S. Moorland Rd", font=f, fill=(20, 20, 20)); dr.text((X(5900), Y(5335) - 6), "Interstate 43 right-of-way", font=f, fill=(20, 20, 20))
im.save("preview.png")
