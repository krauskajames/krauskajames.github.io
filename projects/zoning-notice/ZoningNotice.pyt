# -*- coding: utf-8 -*-
"""ArcGIS Pro Python toolbox: zoning hearing notice packet.

Give it a parcel layer, the subject parcel ID(s) and the notice distance. It selects every parcel
within that distance, builds a cleaned mailing list (one letter per owner, merged spellings,
right-of-way and blank owners set aside, absentee owners flagged), finds other municipalities
within 1,000 ft whose clerks must get notice, writes Avery 5160 labels and CSVs, adds the
subject, buffer and notified parcels to the map, and can export a notice-map layout.

Written for ArcGIS Pro 3.7.3. Uses only arcpy plus matplotlib, both in Pro's default
arcgispro-py3 environment (no extra installs).
Add it in Pro: Catalog pane > Toolboxes > Add Toolbox > ZoningNotice.pyt.
The list logic lives in notice_core.py (same folder) and is tested without arcpy in tests/.
"""
import datetime
import importlib
import os
import sys

import arcpy

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

FIELD_PARAMS = [  # (parameter name, label, notice_core key)
    ("f_owner1", "Owner name", "owner1"),
    ("f_owner1_alt", "Owner name, first-last order (optional)", "owner1_alt"),
    ("f_owner2", "Second owner name (optional)", "owner2"),
    ("f_owner2_alt", "Second owner name, first-last order (optional)", "owner2_alt"),
    ("f_addr", "Mailing street address", "addr"),
    ("f_city", "Mailing city", "city"),
    ("f_state", "Mailing state", "state"),
    ("f_zip5", "Mailing ZIP", "zip5"),
    ("f_zip4", "Mailing ZIP+4 (optional)", "zip4"),
    ("f_site", "Site address (optional, for absentee owners)", "site"),
    ("f_muni", "Municipality", "muni"),
    ("f_row", "Right-of-way flag (optional)", "row"),
]
REQUIRED_KEYS = {"owner1", "addr", "city", "state", "zip5", "muni"}


class Toolbox:
    def __init__(self):
        self.label = "Zoning Notice"
        self.alias = "zoningnotice"
        self.tools = [NoticePacket]


class NoticePacket:
    def __init__(self):
        self.label = "Zoning Hearing Notice Packet"
        self.description = ("Selects parcels within the notice distance of the subject parcel(s), builds a cleaned "
                            "owner mailing list and labels, lists municipal clerks within 1,000 ft, and maps it.")
        self.canRunInBackground = False

    def getParameterInfo(self):
        import notice_core
        P = arcpy.Parameter
        parcels = P(name="parcels", displayName="Parcels", datatype="GPFeatureLayer", parameterType="Required", direction="Input")
        pid = P(name="pid_field", displayName="Parcel ID field", datatype="Field", parameterType="Required", direction="Input")
        pid.parameterDependencies = ["parcels"]
        subj = P(name="subject_ids", displayName="Subject parcel ID(s)", datatype="GPString", parameterType="Required",
                 direction="Input", multiValue=True)
        dist = P(name="distance", displayName="Notice distance", datatype="GPLinearUnit", parameterType="Required", direction="Input")
        dist.value = "200 FeetUS"
        mdist = P(name="muni_distance", displayName="Municipal clerk notice distance", datatype="GPLinearUnit",
                  parameterType="Required", direction="Input")
        mdist.value = "1000 FeetUS"
        home = P(name="home_muni", displayName="Municipality holding the hearing (blank = subject parcel's)",
                 datatype="GPString", parameterType="Optional", direction="Input")
        out = P(name="out_folder", displayName="Output folder", datatype="DEFolder", parameterType="Required", direction="Input")
        lay = P(name="layout", displayName="Notice map layout to export (optional)", datatype="GPString",
                parameterType="Optional", direction="Input")
        scale = P(name="map_scale", displayName="Notice map scale 1:", datatype="GPLong", parameterType="Optional", direction="Input")
        scale.value = 1200   # 1 in = 100 ft
        build = P(name="build_map", displayName="Build the notice map layout for me", datatype="GPBoolean",
                  parameterType="Optional", direction="Input")
        build.value = True
        scen = P(name="scenario", displayName="Scenario line for the map (optional)", datatype="GPString",
                 parameterType="Optional", direction="Input")
        scen.value = "Example petition: rezone from I-1 Light Industrial to PUD"
        params = [parcels, pid, subj, dist, mdist, home, out, build, scen, lay, scale]
        for name, label, key in FIELD_PARAMS:
            f = P(name=name, displayName=label, datatype="Field", parameterType="Optional", direction="Input",
                  category="Field names")
            f.parameterDependencies = ["parcels"]
            params.append(f)
        self._defaults = notice_core.DEFAULT_FIELDS
        return params

    def updateParameters(self, parameters):
        import notice_core
        p = {x.name: x for x in parameters}
        if p["parcels"].value and p["parcels"].altered and not p["parcels"].hasBeenValidated:
            names = {f.name.upper(): f.name for f in arcpy.ListFields(p["parcels"].valueAsText)}
            if not p["pid_field"].value and notice_core.DEFAULT_FIELDS["id"].upper() in names:
                p["pid_field"].value = names[notice_core.DEFAULT_FIELDS["id"].upper()]
            for name, _, key in FIELD_PARAMS:
                d = notice_core.DEFAULT_FIELDS[key].upper()
                if not p[name].value and d in names:
                    p[name].value = names[d]
        try:
            layouts = [l.name for l in arcpy.mp.ArcGISProject("CURRENT").listLayouts()]
            p["layout"].filter.list = layouts
        except Exception:
            pass
        try:
            p["layout"].enabled = not p["build_map"].value
        except Exception:
            pass

    def updateMessages(self, parameters):
        p = {x.name: x for x in parameters}
        if p["parcels"].value:
            for name, label, key in FIELD_PARAMS:
                if key in REQUIRED_KEYS and not p[name].value:
                    p[name].setErrorMessage("Pick the %s field (under Field names)." % label.lower())

    def execute(self, parameters, messages):
        import notice_core
        importlib.reload(notice_core)   # picks up edits without restarting Pro
        p = {x.name: x for x in parameters}
        fields = dict(notice_core.DEFAULT_FIELDS)
        fields["id"] = p["pid_field"].valueAsText
        for name, _, key in FIELD_PARAMS:
            fields[key] = p[name].valueAsText or ""
        subject_ids = [s.strip().strip("'\"") for s in p["subject_ids"].values]
        dist = p["distance"].valueAsText
        mdist = p["muni_distance"].valueAsText
        out_dir = p["out_folder"].valueAsText
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        gdb = aprx.defaultGeodatabase
        arcpy.env.overwriteOutput = True

        src = arcpy.Describe(p["parcels"].value).catalogPath   # the whole layer, ignoring any selection
        all_lyr = arcpy.management.MakeFeatureLayer(src, "zn_all_parcels")[0]
        fid = arcpy.AddFieldDelimiters(src, fields["id"])
        where = "%s IN (%s)" % (fid, ", ".join("'%s'" % s.replace("'", "''") for s in subject_ids))
        subj_lyr = arcpy.management.MakeFeatureLayer(src, "zn_subject_lyr", where)[0]
        n_subj = int(arcpy.management.GetCount(subj_lyr)[0])
        if n_subj == 0:
            arcpy.AddError("No parcel matched %s. Check the ID and the Parcel ID field." % where)
            return
        if n_subj != len(set(subject_ids)):
            arcpy.AddWarning("%d subject IDs given, %d parcels matched." % (len(set(subject_ids)), n_subj))

        subject_fc = os.path.join(gdb, "zn_subject")
        buffer_fc = os.path.join(gdb, "zn_notice_buffer")
        notified_fc = os.path.join(gdb, "zn_notified_parcels")
        clerk_fc = os.path.join(gdb, "zn_clerk_buffer")
        arcpy.conversion.ExportFeatures(subj_lyr, subject_fc)
        arcpy.analysis.PairwiseBuffer(subject_fc, buffer_fc, dist, dissolve_option="ALL")
        arcpy.analysis.PairwiseBuffer(subject_fc, clerk_fc, mdist, dissolve_option="ALL")

        # 1. Notice area: same as Select By Location "within a distance" by hand.
        arcpy.management.SelectLayerByLocation(all_lyr, "WITHIN_A_DISTANCE", subject_fc, dist, "NEW_SELECTION")
        read = [f for f in [fields["id"]] + [fields[k] for k in fields if k != "id"] if f]
        existing = {f.name.upper(): f.name for f in arcpy.ListFields(src)}
        missing = [f for f in read if f.upper() not in existing]
        if missing:
            arcpy.AddError("Fields not found in the parcel layer: " + ", ".join(missing))
            return
        keymap = {fields[k]: k for k in fields if fields[k]}
        recs = []
        with arcpy.da.SearchCursor(all_lyr, read) as cur:
            for row in cur:
                recs.append({f: v for f, v in zip(read, row)})
        recs_std = [{notice_core.DEFAULT_FIELDS[keymap[f]]: v for f, v in r.items()} for r in recs]
        arcpy.conversion.ExportFeatures(all_lyr, notified_fc)

        # 2. Municipal clerks within 1,000 ft.
        arcpy.management.SelectLayerByLocation(all_lyr, "WITHIN_A_DISTANCE", subject_fc, mdist, "NEW_SELECTION")
        munis = sorted({r[0] for r in arcpy.da.SearchCursor(all_lyr, [fields["muni"]]) if r[0]})
        subj_munis = sorted({r[0] for r in arcpy.da.SearchCursor(subj_lyr, [fields["muni"]]) if r[0]})
        home = p["home_muni"].valueAsText or (subj_munis[0] if subj_munis else "")
        clerks = notice_core.clerks_to_notify(munis, home)
        arcpy.management.SelectLayerByAttribute(all_lyr, "CLEAR_SELECTION")

        # 3. Mailing list and files.
        res = notice_core.build_mailing_list(recs_std, subject_ids)
        meta = {"subject parcel(s)": ", ".join(subject_ids), "hearing held by": home, "notice distance": dist,
                "municipal clerk distance": mdist, "parcel layer": src,
                "run": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "ArcGIS Pro": arcpy.GetInstallInfo()["Version"]}
        files = notice_core.write_outputs(res, clerks, out_dir, meta)

        # 4. Letter number on each notified parcel, for map labels.
        letters = {pp["parcel_id"]: pp["letter"] for pp in res["parcels"]}
        notes = {pp["parcel_id"]: pp["note"] for pp in res["parcels"]}
        arcpy.management.AddField(notified_fc, "LETTER", "SHORT")
        arcpy.management.AddField(notified_fc, "NOTE", "TEXT", field_length=120)
        with arcpy.da.UpdateCursor(notified_fc, [fields["id"], "LETTER", "NOTE"]) as cur:
            for pid_v, _, _ in cur:
                k = str(pid_v or "").strip().upper()
                cur.updateRow([pid_v, letters.get(k) or None, notes.get(k, "")])

        # 5. Add to the map; export the layout if asked.
        try:
            m = aprx.activeMap or aprx.listMaps()[0]
            for fc in (notified_fc, buffer_fc, subject_fc):
                m.addDataFromPath(fc)
        except Exception as e:
            arcpy.AddWarning("Could not add layers to the map: %s" % e)
        if p["build_map"].value:
            try:
                import notice_layout
                importlib.reload(notice_layout)
                pdf = notice_layout.build(
                    aprx, {"subject": subject_fc, "notice_buffer": buffer_fc, "clerk_buffer": clerk_fc, "notified": notified_fc},
                    src, res["counts"], {"subject": ", ".join(subject_ids), "muni": home, "distance": dist.replace("FeetUS", "ft"),
                                         "run": meta["run"][:10]},
                    clerks, os.path.join(out_dir, "notice_map.pdf"), p["map_scale"].value or 0,
                    scenario=p["scenario"].valueAsText or "")
                files.append(pdf)
                arcpy.AddMessage("Notice map: new map and layout 'Notice Map (auto)' in the project; PDF exported.")
            except Exception as e:
                arcpy.AddWarning("Notice map not built: %s" % e)
        elif p["layout"].valueAsText:
            try:
                lay = aprx.listLayouts(p["layout"].valueAsText)[0]
                mf = lay.listElements("MAPFRAME_ELEMENT")[0]
                ext = arcpy.Describe(buffer_fc).extent
                mf.camera.setExtent(ext)
                if p["map_scale"].value:
                    mf.camera.scale = p["map_scale"].value
                    need_w = ext.width * 12.0 / p["map_scale"].value     # inches, if map units are feet
                    if need_w > mf.elementWidth:
                        arcpy.AddWarning("At 1:%d the notice area is about %.1f in wide but the map frame is %.1f in. "
                                         "Use a larger page or map series." % (p["map_scale"].value, need_w, mf.elementWidth))
                pdf = os.path.join(out_dir, "notice_map.pdf")
                lay.exportToPDF(pdf)
                files.append(pdf)
            except Exception as e:
                arcpy.AddWarning("Layout export skipped: %s" % e)

        for k, v in res["counts"].items():
            arcpy.AddMessage("%-32s %s" % (k.replace("_", " "), v))
        arcpy.AddMessage("clerks to notify (1,000 ft):      %s" % (", ".join(clerks) or "none"))
        if res["review"]:
            arcpy.AddWarning("%d owner pairs to review: see review.csv" % len(res["review"]))
        arcpy.AddMessage("Files:\n  " + "\n  ".join(files))
