"""Tiny synthetic county with one planted error per check, to test parcel_qa.py."""
import json, os
import geopandas as gpd
from shapely.geometry import Polygon, LineString, Point, box
D = os.path.dirname(os.path.abspath(__file__)) + "/synthetic"
os.makedirs(D, exist_ok=True)
X0, Y0 = 600000, 400000   # WTM meters
def b(x, y, w=40, h=60): return box(X0 + x, Y0 + y, X0 + x + w, Y0 + y + h)
# Main St runs west->east along y=0; parcels north (y 10..70) and south (y -70..-10)
parcels = []
for i in range(6):
    parcels.append(dict(PARCELNO=f"N{i}", OWNER="Smith", SITEADDR=f"{101 + 2*i} MAIN ST", geometry=b(i * 40, 10)))
    parcels.append(dict(PARCELNO=f"S{i}", OWNER="Jones", SITEADDR=f"{100 + 2*i} MAIN ST", geometry=b(i * 40, -70)))
parcels[2]["geometry"] = box(X0 + 40, Y0 + 10, X0 + 85, Y0 + 70)        # N1 extends 5 m into N2 -> P01 overlap
parcels[8]["geometry"] = box(X0 + 160, Y0 + 10, X0 + 197, Y0 + 70)       # N4 leaves 3 m gap to N5 -> P02
parcels[6]["geometry"] = Polygon([(X0+120, Y0+10), (X0+160, Y0+10), (X0+160, Y0+70), (X0+120, Y0+70), (X0+120, Y0+50), (X0+123, Y0+50), (X0+123, Y0+30), (X0+120, Y0+30)])  # N3 notch -> P02
parcels[10]["PARCELNO"] = "N0"                                           # N5 duplicate ID -> P03
parcels[11]["OWNER"] = ""                                                # S5 missing owner -> P04
parcels.append(dict(PARCELNO="SLV", OWNER="County", SITEADDR="", geometry=box(X0 + 240, Y0 + 10, X0 + 240.8, Y0 + 70)))  # P05
gpd.GeoDataFrame(parcels, crs=3071).to_file(f"{D}/parcels.gpkg")
roads = [
    dict(CLID="R1", FULLNAME="MAIN ST", MUNI="Town of Test", FROMLEFT=101, TOLEFT=111, FROMRIGHT=100, TORIGHT=110, geometry=LineString([(X0, Y0), (X0 + 240, Y0)])),
    dict(CLID="R2", FULLNAME="MAIN ST", MUNI="Town of Test", FROMLEFT=109, TOLEFT=131, FROMRIGHT=112, TORIGHT=131, geometry=LineString([(X0 + 240, Y0), (X0 + 480, Y0)])),   # R01 mixed parity (112-131), R02 overlap (109 < 111)
    dict(CLID="R3", FULLNAME="OAK RD", MUNI="Town of Test", FROMLEFT=0, TOLEFT=0, FROMRIGHT=0, TORIGHT=0, geometry=LineString([(X0, Y0 + 300), (X0 + 200, Y0 + 300)])),  # R03
]
gpd.GeoDataFrame(roads, crs=3071).to_file(f"{D}/roads.gpkg")
pts = []
def ap(i, num, street, pid, rd, x, y, muni="Town of Test", esn="101", status="Current", unit=""):
    pts.append(dict(SITEADDID=f"A{i}", ADDRNUM=str(num), FULLNAME=street, FULLADDR=f"{num} {street}", UNITID=unit, PARCELID=pid, RDCLID=rd, MUNICIPALITY=muni, ESN=esn, MSAG="TEST", STATUS=status, geometry=Point(X0 + x, Y0 + y)))
ap(0, 101, "MAIN ST", "N0", "R1", 20, 40)                 # clean
ap(1, 103, "MAIN ST", "N1", "R1", 100, 40)                # A02: sits in N2
ap(2, 105, "MAIN ST", "N2", "R1", 90, 400)                # A03 + A08 far
ap(3, 107, "MAIN ST", "N3", "R9", 140, 40)                # A04 broken link
ap(4, 109, "MAIN STREET", "N4", "R1", 180, 40)            # A05 name mismatch
ap(5, 199, "MAIN ST", "S0", "R1", 20, -40)                # A06 out of range
ap(6, 104, "MAIN ST", "N0", "R1", 30, 40)                 # A07 even number on odd (left) side
ap(7, 101, "MAIN ST", "N0", "R1", 25, 45)                 # A09 duplicate of A0
ap(8, 102, "MAIN ST", "S1", "R1", 60, -40, muni="Village of Elsewhere")  # A10
ap(9, "", "MAIN ST", "S2", "R1", 100, -40, esn="")        # A01 missing number + ESN
ap(10, 106, "MAIN ST", "S3", "R1", 140, -40, status="Retired")  # filtered out
gpd.GeoDataFrame(pts, crs=3071).to_file(f"{D}/addresses.gpkg")
gpd.GeoDataFrame([dict(NAME="Town of Test", geometry=box(X0 - 50, Y0 - 500, X0 + 600, Y0 + 500))], crs=3071).to_file(f"{D}/munis.gpkg")
cfg = dict(county="Synthetic test county",
    inputs=dict(parcels="synthetic/parcels.gpkg", addresses="synthetic/addresses.gpkg", roads="synthetic/roads.gpkg", municipalities="synthetic/munis.gpkg"),
    parcel_fields=dict(id="PARCELNO", required=["PARCELNO", "OWNER"]),
    road_fields=dict(id="CLID", name="FULLNAME", municipality="MUNI", fromleft="FROMLEFT", toleft="TOLEFT", fromright="FROMRIGHT", toright="TORIGHT"),
    address_fields=dict(id="SITEADDID", number="ADDRNUM", street="FULLNAME", full="FULLADDR", unit="UNITID", parcel_id="PARCELID", road_id="RDCLID", municipality="MUNICIPALITY", status="STATUS", required=["ADDRNUM", "FULLNAME", "MUNICIPALITY", "ESN", "MSAG"]),
    muni_fields=dict(name="NAME"), active_status_values=["Current"], far_from_road_m=200)
json.dump(cfg, open(os.path.join(os.path.dirname(D), "synthetic.json"), "w"), indent=1)
print("ok")
