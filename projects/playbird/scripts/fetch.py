import json, urllib.request, urllib.parse
B="https://gis2.sheboygancounty.com/publicgis1/rest/services"
def get(url, **q):
    data=urllib.parse.urlencode(q).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request(url,data=data),timeout=60))
P=B+"/LandInformation/TaxParcels/FeatureServer/0/query"
s=get(P,where="PARCELID='59024341550'",outFields="PARCELID",returnGeometry="true",f="json")
g=s["features"][0]["geometry"]; sr=s["spatialReference"]; print("sr",sr)
geom=json.dumps({"rings":g["rings"],"spatialReference":sr})
for d,name in [(200,"notice"),(1000,"m1000"),(1400,"context")]:
    r=get(P,geometry=geom,geometryType="esriGeometryPolygon",spatialRel="esriSpatialRelIntersects",distance=d,units="esriSRUnit_Foot",
          inSR=json.dumps(sr),outFields="PARCELID,MUNI,isROW,CLASSDSCRP,ACRES",returnGeometry="true",outSR=4326,f="geojson")
    print(name,len(r["features"])); json.dump(r,open(name+".geojson","w"))
json.dump({"geom":geom},open("subject_native.json","w"))
z=get(B+"/Planning/Zoning/MapServer",f="json"); print([(l["id"],l["name"]) for l in z["layers"]])
e=get(B+"/Planning/ETJ/MapServer",f="json"); print([(l["id"],l["name"]) for l in e["layers"]])
