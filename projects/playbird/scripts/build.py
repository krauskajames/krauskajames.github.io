import json, csv, re
from shapely.geometry import shape, mapping
from shapely.ops import transform, unary_union
from pyproj import Transformer
U="/mnt/user-data/uploads/ZoningHearingNotice/"
parcels={r["parcel_id"]:r for r in csv.DictReader(open(U+"parcels_in_notice_area.csv"))}
letters={r["letter"]:r for r in csv.DictReader(open(U+"mailing_list.csv"))}
def otype(n):
    n=n.upper()
    if not n: return "none"
    if n.startswith("TOWN OF") or "COUNTY" in n or "STATE OF" in n: return "government"
    if re.search(r"\b(LLC|INC|CO|COMPANY|CORP|LTD|GROUP)\b",n): return "business"
    return "individual"
def rnd(g):
    return json.loads(json.dumps(mapping(g)), parse_float=lambda x: round(float(x),6))
to_ft=Transformer.from_crs(4326,3071,always_xy=True).transform  # WTM83/91 meters
to_ll=Transformer.from_crs(3071,4326,always_xy=True).transform
ctx=json.load(open("context.geojson"))["features"]
notice={f["properties"]["PARCELID"] for f in json.load(open("notice.geojson"))["features"]}
m1000={f["properties"]["PARCELID"] for f in json.load(open("m1000.geojson"))["features"]}
out=[]; subj=None
for f in ctx:
    p=f["properties"]; pid=str(p["PARCELID"]); g=shape(f["geometry"])
    props={"id":pid,"muni":(p.get("MUNI") or "").title(),"row":bool(p.get("isROW")),"acres":round(p.get("ACRES") or 0,2)}
    if pid in notice:
        r=parcels.get(pid,{})
        props["role"]="subject" if r.get("note")=="subject parcel" else ("excluded" if r.get("note","").startswith("excluded") else "notified")
        props["letter"]=int(r["letter"]) if r.get("letter") else None
        props["owner_type"]=otype(r.get("owner",""))
        if props["letter"]:
            L=letters[str(props["letter"])]
            props["absentee"]=L["absentee_owner"]=="True"; props["owner_parcels"]=int(L["parcel_count"]); props["merged"]=L["merged_spellings"]=="True"
        if props["role"]=="excluded": props["why"]="No owner name in the parcel record (likely road or other right-of-way)."
    else:
        props["role"]="context"; props["in1000"]=pid in m1000
    if props["role"]=="subject": subj=g
    out.append({"type":"Feature","properties":props,"geometry":rnd(g)})
sp=transform(to_ft,subj)
buf=transform(to_ll,sp.buffer(200*0.3048006096,resolution=24)); b1000=transform(to_ll,sp.buffer(1000*0.3048006096,resolution=24))
feat=lambda g,k:{"type":"Feature","properties":{"kind":k},"geometry":rnd(g)}
z=[]
for f in json.load(open("zoning.geojson"))["features"]:
    p=f["properties"]; z.append({"type":"Feature","properties":{"z":p["ZoneClass"],"d":p["ZoneDesc"],"m":p.get("MuniLabel")},"geometry":rnd(shape(f["geometry"]).simplify(0.000005))})
import os; os.makedirs("out",exist_ok=True)
json.dump({"type":"FeatureCollection","features":out},open("out/parcels.geojson","w"),separators=(",",":"))
json.dump({"type":"FeatureCollection","features":[feat(buf,"notice200"),feat(b1000,"clerk1000")]},open("out/buffers.geojson","w"),separators=(",",":"))
json.dump({"type":"FeatureCollection","features":z},open("out/zoning.geojson","w"),separators=(",",":"))
from collections import Counter
print(Counter(f["properties"]["role"] for f in out))
print(Counter((f["properties"].get("owner_type"),f["properties"].get("letter")) for f in out if f["properties"]["role"]!="context"))
print(Counter(f["properties"]["m"] for f in z))
for n in os.listdir("out"): print(n, os.path.getsize("out/"+n))
