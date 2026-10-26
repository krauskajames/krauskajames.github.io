"""Every check must fire exactly where an error was planted in the synthetic county."""
import os, subprocess, sys, tempfile
import geopandas as gpd
HERE = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(HERE, "make_synthetic.py")], check=True)
out = tempfile.mkdtemp()
subprocess.run([sys.executable, os.path.join(HERE, "..", "parcel_qa.py"), os.path.join(HERE, "synthetic.json"), out], check=True, capture_output=True)
E = gpd.read_file(os.path.join(out, "qa_findings.gpkg"))
expected = {"P01": "N1 / N2", "P02": "", "P03": "N0", "P04": "S5", "P05": "SLV", "A01": "A9", "A02": "A1", "A03": "A2", "A04": "A3",
            "A05": "A4", "A06": "A5", "A07": "A6", "A08": "A2", "A09": "A0 / A7", "A10": "A8", "R01": "R2", "R02": "R1 / R2", "R03": "R3"}
got = {}
for r in E.itertuples():
    got.setdefault(r.check, set()).add(r.feature_id or "")
bad = [k for k, v in expected.items() if v not in got.get(k, set())]
extra = [r.check + ":" + r.feature_id for r in E.itertuples() if r.check in expected and (r.feature_id or "") != expected[r.check] and r.check != "A01"]
print("missing:", bad or "none", "| unexpected:", extra or "none")
sys.exit(1 if bad or extra else 0)
