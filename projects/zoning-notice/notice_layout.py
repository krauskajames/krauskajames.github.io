# -*- coding: utf-8 -*-
"""Build the notice map: a new map and an ANSI D layout made entirely with arcpy.mp.

Called by ZoningNotice.pyt after the selection. Written for ArcGIS Pro 3.7.3.
Every decoration step is wrapped so one failure (a missing style item, say) gives a
warning and the rest of the map is still made.

Page: ANSI D landscape (34 x 22 in). Map frame 26 x 21 in on the left; at 1:1,200
(1 in = 100 ft, the Town of Sheboygan plot plan scale) it shows 2,600 x 2,100 ft.
Side panel on the right: title, scenario, counts, legend, north arrow, scale bar, sources.
"""
import arcpy

PAGE_W, PAGE_H = 34.0, 22.0
FRAME = (0.5, 0.5, 26.5, 21.5)          # xmin, ymin, xmax, ymax in inches
PANEL_X = 27.25
ZONING_URL = "https://gis2.sheboygancounty.com/publicgis1/rest/services/Planning/Zoning/MapServer/0"

RED = [181, 70, 42, 100]
FOREST = [47, 82, 56, 100]
GRAY = [120, 120, 120, 100]
NONE = [0, 0, 0, 0]


def _warn(step, e):
    arcpy.AddWarning("Notice map: %s skipped (%s)" % (step, e))


def _simple(lyr, fill, outline, width):
    sym = lyr.symbology
    if not hasattr(sym, "renderer"):
        return
    sym.updateRenderer("SimpleRenderer")
    s = sym.renderer.symbol
    s.color = {"RGB": fill}
    s.outlineColor = {"RGB": outline}
    s.outlineWidth = width
    lyr.symbology = sym


def _labels(lyr, expression, where=None, size=None):
    lc = lyr.listLabelClasses()[0]
    lc.expressionEngine = "Arcade"
    lc.expression = expression
    if where:
        lc.SQLQuery = where
    lc.visible = True
    lyr.showLabels = True
    if size:
        cim = lyr.getDefinition("V3")
        sym = cim.labelClasses[0].textSymbol.symbol
        sym.height = size
        sym.symbol.symbolLayers[0].color.values = [20, 20, 20, 100]
        lyr.setDefinition(cim)


def _text(aprx, lyt, x, y, text, size, name):
    # In Pro 3.x text and graphics are created on the project, with the layout as the container.
    return aprx.createTextElement(lyt, arcpy.Point(x, y), "POINT", text, size, name=name)


def build(aprx, paths, parcels_src, counts, meta, clerks, out_pdf, scale=1200, zoning_url=ZONING_URL,
          title="Rezoning Notice Area", scenario=""):
    """paths: dict with subject, notice_buffer, clerk_buffer, notified (feature class paths)."""
    name = "Notice Map (auto)"
    for item in aprx.listLayouts(name) + aprx.listMaps(name):
        try:
            aprx.deleteItem(item)
        except Exception as e:
            _warn("removing the old " + name, e)

    m = aprx.createMap(name, "MAP")
    m.spatialReference = arcpy.Describe(paths["subject"]).spatialReference
    for lyr in m.listLayers():          # a new map can come with a basemap; keep the sheet plain
        if lyr.isBasemapLayer:
            m.removeLayer(lyr)

    # Layers bottom to top: zoning, all parcels, 1,000 ft line, 200 ft buffer, notified, subject.
    try:
        z = m.addDataFromPath(zoning_url)
        z.name = "Zoning districts"
        sym = z.symbology
        sym.updateRenderer("UniqueValueRenderer")
        sym.renderer.fields = ["ZoneClass"]
        z.symbology = sym
        z.transparency = 70
        _labels(z, "$feature.ZoneClass", size=11)
    except Exception as e:
        _warn("zoning layer", e)
    layers = {}
    for key, label in [("parcels", "Parcels"), ("clerk_buffer", "1,000 ft municipal clerk notice"),
                       ("notice_buffer", "200 ft owner notice area"), ("notified", "Notified parcel (letter number)"),
                       ("subject", "Subject parcel")]:
        src = parcels_src if key == "parcels" else paths[key]
        try:
            layers[key] = m.addDataFromPath(src)
            layers[key].name = label
        except Exception as e:
            _warn("adding " + label, e)
    style = {"parcels": (NONE, GRAY, 0.4), "clerk_buffer": (NONE, [60, 60, 60, 100], 1.5),
             "notice_buffer": (NONE, FOREST, 2.5), "notified": (NONE, FOREST, 1.6),
             "subject": (NONE, RED, 4)}
    for key, (fill, outline, width) in style.items():
        if key in layers:
            try:
                _simple(layers[key], fill, outline, width)
            except Exception as e:
                _warn("symbol for " + key, e)
    for key in ("parcels", "subject", "notice_buffer", "clerk_buffer"):
        if key in layers:
            try:
                layers[key].showLabels = False      # the county service labels parcel IDs by default
            except Exception:
                pass
    try:
        _labels(layers["notified"], "$feature.LETTER", "LETTER IS NOT NULL", size=18)
    except Exception as e:
        _warn("letter labels", e)

    lyt = aprx.createLayout(PAGE_W, PAGE_H, "INCH", name)
    mf = lyt.createMapFrame(arcpy.Extent(*FRAME), m, "Map")
    ext = arcpy.Describe(paths["notice_buffer"]).extent
    mf.camera.setExtent(ext)
    if scale:
        mf.camera.scale = scale
        unit = m.spatialReference.linearUnitName.lower()
        to_ft = 1.0 if "foot" in unit else 3.28084
        need_w = ext.width * to_ft * 12.0 / scale
        need_h = ext.height * to_ft * 12.0 / scale
        fw, fh = FRAME[2] - FRAME[0], FRAME[3] - FRAME[1]
        if need_w > fw or need_h > fh:
            arcpy.AddWarning("At 1:%d the notice area needs %.1f x %.1f in but the frame is %.0f x %.0f in; "
                             "fitting to the frame instead." % (scale, need_w, need_h, fw, fh))
            mf.camera.setExtent(ext)

    y = PAGE_H - 0.9
    try:
        _text(aprx, lyt, PANEL_X, y, title, 34, "Title"); y -= 0.85
        _text(aprx, lyt, PANEL_X, y, "Parcel %s · %s" % (meta.get("subject", ""), meta.get("muni", "").title().replace(" Of ", " of ")), 18, "Subtitle"); y -= 0.7
        if scenario:
            _text(aprx, lyt, PANEL_X, y, scenario, 14, "Scenario"); y -= 0.8
        dist_txt = meta.get("distance", "").replace("Feet", "ft").replace("FeetUS", "ft")
        lines = ["%s parcels within %s" % (counts["parcels_in_notice_area"], dist_txt),
                 "%s letters to owners" % counts["letters_to_owners"],
                 "Clerk notice (1,000 ft): %s" % (", ".join(c.title().replace(" Of ", " of ") for c in clerks) or "none")]
        _text(aprx, lyt, PANEL_X, y, "\n".join(lines), 14, "Counts"); y -= 1.3
    except Exception as e:
        _warn("title text", e)
    try:
        leg = lyt.createMapSurroundElement(arcpy.Point(PANEL_X, y - 7.0), "LEGEND", mf, None, "Legend")
        try:
            leg.fittingStrategy = "AdjustFrame"
        except Exception:
            pass
        for it in list(leg.items):
            if it.name in ("Parcels", "1,000 ft municipal clerk notice"):
                try:
                    leg.removeItem(it)        # parcels need no legend; the 1,000 ft line is off this sheet
                except Exception:
                    pass
        for it in leg.items:
            try:
                it.showVisibleFeatures = True   # only zoning classes that are on the map
            except Exception:
                pass
        try:
            cim = lyt.getDefinition("V3")
            for e2 in cim.elements:
                if e2.name == "Legend":
                    for li in e2.items:
                        li.showHeading = False        # drop the "ZoneClass" field heading
                        try:
                            li.labelSymbol.symbol.height = 14
                            li.layerNameSymbol.symbol.height = 16
                        except Exception:
                            pass
            lyt.setDefinition(cim)
        except Exception as e:
            _warn("legend text size", e)
    except Exception as e:
        _warn("legend", e)
    try:
        na = aprx.listStyleItems("ArcGIS 2D", "NORTH_ARROW", "ArcGIS North 1")
        el = lyt.createMapSurroundElement(arcpy.Point(PANEL_X, 4.2), "NORTH_ARROW", mf, na[0] if na else None, "North Arrow")
        el.elementHeight = 1.4
    except Exception as e:
        _warn("north arrow", e)
    try:
        sb = aprx.listStyleItems("ArcGIS 2D", "SCALE_BAR", "Alternating Scale Bar 1")
        el = lyt.createMapSurroundElement(arcpy.Point(PANEL_X + 1.6, 4.4), "SCALE_BAR", mf, sb[0] if sb else None, "Scale Bar")
        el.elementWidth = 4.5
        cim = lyt.getDefinition("V3")
        for e2 in cim.elements:
            if e2.name == "Scale Bar":
                e2.units = {"uwkid": 9003}        # US survey feet
                e2.unitLabel = "Feet"
                e2.divisions = 2
                e2.subdivisions = 0
        lyt.setDefinition(cim)
    except Exception as e:
        _warn("scale bar", e)
    try:
        note = ("Scale 1 in = %d ft at 34 x 22 in.\nThe 1,000 ft clerk-notice line is outside this view.\n"
                "Data: Sheboygan County parcels and zoning, %s.\n"
                "Made with the Zoning Hearing Notice Packet toolbox.\n"
                "Example for a portfolio. Not an official notice.") % (round((scale or 1200) / 12.0), meta.get("run", ""))
        _text(aprx, lyt, PANEL_X, 2.4, note, 12, "Sources")
    except Exception as e:
        _warn("source note", e)

    lyt.exportToPDF(out_pdf, resolution=200)
    return out_pdf
