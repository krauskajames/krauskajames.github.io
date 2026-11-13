import json, urllib.request, urllib.parse
B="https://gis2.sheboygancounty.com/publicgis1/rest/services"
def get(url, **q):
    return json.load(urllib.request.urlopen(urllib.request.Request(url,data=urllib.parse.urlencode(q).encode()),timeout=60))
geom=json.load(open("subject_native.json"))["geom"]; sr=json.dumps({"wkid":103458})
z=get(B+"/Planning/Zoning/MapServer/0",f="json"); print([f["name"] for f in z["fields"]])
r=get(B+"/Planning/Zoning/MapServer/0/query",geometry=geom,geometryType="esriGeometryPolygon",distance=1400,units="esriSRUnit_Foot",inSR=sr,outFields="*",returnGeometry="true",outSR=4326,f="geojson")
print("zoning",len(r["features"])); json.dump(r,open("zoning.geojson","w"))
from collections import Counter; print(Counter((f["properties"].get("ZONING") or f["properties"].get("Zoning") or str(list(f["properties"].items())[:4])) for f in r["features"]).most_common(20))
e=get(B+"/Planning/ETJ/MapServer/0/query",geometry=geom,geometryType="esriGeometryPolygon",inSR=sr,outFields="*",returnGeometry="false",f="json")
print("ETJ",[f["attributes"] for f in e["features"]])
m=json.load(open("m1000.geojson")); print(Counter(f["properties"]["MUNI"] for f in m["features"]))
