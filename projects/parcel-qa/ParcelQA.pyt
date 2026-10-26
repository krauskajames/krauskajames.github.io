# -*- coding: utf-8 -*-
"""ArcGIS Pro Python toolbox: runs the Parcel & NG911 QA checks on layers in your map.

Add it in Pro: Catalog pane > Toolboxes > Add Toolbox > ParcelQA.pyt.
The checks themselves live in parcel_qa.py (same folder). They need geopandas; ArcGIS Pro's default
Python environment does not include it, so once:
    Pro > Settings > Package Manager > Environment Manager > clone arcgispro-py3 > activate the clone
    then in "Python Command Prompt":  conda install -c conda-forge geopandas pyogrio
The tool exports your inputs to a temporary GeoPackage, runs the checks and adds the findings to the map.
"""
import json, os, sys, tempfile
import arcpy

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def _fields(param):
    return [f.name for f in arcpy.ListFields(param.valueAsText)] if param.value else []


class Toolbox:
    def __init__(self):
        self.label = "Parcel QA"
        self.alias = "parcelqa"
        self.tools = [RunParcelQA]


class RunParcelQA:
    def __init__(self):
        self.label = "Run Parcel and NG911 QA"
        self.description = "Checks tax parcels, site address points and road centerlines for overlaps, gaps, broken road links, out-of-range house numbers and more."

    def getParameterInfo(self):
        P = lambda name, label, dtype, direction="Input", required=True, ptype="Required": arcpy.Parameter(
            name=name, displayName=label, datatype=dtype, direction=direction, parameterType=ptype if required else "Optional")
        params = [
            P("parcels", "Tax parcels", "GPFeatureLayer"),
            P("parcel_id", "Parcel ID field", "Field"),
            P("addresses", "Site address points", "GPFeatureLayer"),
            P("addr_number", "Address number field", "Field"),
            P("addr_street", "Full street name field", "Field"),
            P("addr_full", "Full address field", "Field"),
            P("addr_road", "Road centerline ID field", "Field"),
            P("addr_muni", "Municipality field", "Field", required=False),
            P("roads", "Road centerlines", "GPFeatureLayer"),
            P("road_id", "Centerline ID field", "Field"),
            P("road_name", "Road full name field", "Field"),
            P("fromleft", "From left", "Field"), P("toleft", "To left", "Field"),
            P("fromright", "From right", "Field"), P("toright", "To right", "Field"),
            P("munis", "Municipal boundaries", "GPFeatureLayer", required=False),
            P("muni_name", "Municipality name field", "Field", required=False),
            P("out_gpkg", "Output findings (GeoPackage)", "DEFile", direction="Output"),
        ]
        links = {"parcel_id": "parcels", "addr_number": "addresses", "addr_street": "addresses", "addr_full": "addresses",
                 "addr_road": "addresses", "addr_muni": "addresses", "road_id": "roads", "road_name": "roads",
                 "fromleft": "roads", "toleft": "roads", "fromright": "roads", "toright": "roads", "muni_name": "munis"}
        idx = {p.name: p for p in params}
        for f, src in links.items():
            idx[f].parameterDependencies = [src]
        idx["out_gpkg"].filter.list = ["gpkg"]
        return params

    def execute(self, parameters, messages):
        try:
            import parcel_qa
        except ImportError as e:
            arcpy.AddError("geopandas is not installed in this Python environment. See the note at the top of ParcelQA.pyt. (" + str(e) + ")")
            return
        v = {p.name: p.valueAsText for p in parameters}
        work = tempfile.mkdtemp(prefix="parcelqa_")
        gpkg = os.path.join(work, "inputs.gpkg")
        arcpy.management.CreateSQLiteDatabase(gpkg, "GEOPACKAGE")
        inputs = []
        for key, layer in (("parcels", v["parcels"]), ("addresses", v["addresses"]), ("roads", v["roads"]), ("municipalities", v["munis"])):
            if layer:
                arcpy.AddMessage(f"Exporting {key}...")
                arcpy.conversion.ExportFeatures(layer, os.path.join(gpkg, key))
                inputs.append(key)
        cfg = {
            "county": "ArcGIS Pro run",
            "inputs": {k: os.path.join(work, "inputs.gpkg") + "::" + k for k in inputs},
            "parcel_fields": {"id": v["parcel_id"], "required": [v["parcel_id"]]},
            "road_fields": {"id": v["road_id"], "name": v["road_name"], "municipality": None,
                            "fromleft": v["fromleft"], "toleft": v["toleft"], "fromright": v["fromright"], "toright": v["toright"]},
            "address_fields": {"id": "OBJECTID", "number": v["addr_number"], "street": v["addr_street"], "full": v["addr_full"],
                               "parcel_id": None, "road_id": v["addr_road"], "municipality": v["addr_muni"], "required": [v["addr_number"], v["addr_street"]]},
            "muni_fields": {"name": v["muni_name"]} if v["munis"] else {},
        }
        out_dir = os.path.join(work, "out")
        parcel_qa.run_config(cfg, out_dir)
        import shutil
        shutil.copy(os.path.join(out_dir, "qa_findings.gpkg"), v["out_gpkg"])
        arcpy.AddMessage(open(os.path.join(out_dir, "qa_summary.csv")).read())
        try:
            m = arcpy.mp.ArcGISProject("CURRENT").activeMap
            m.addDataFromPath(os.path.join(v["out_gpkg"], "main.findings"))
        except Exception:
            pass
