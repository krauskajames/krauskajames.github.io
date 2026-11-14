# Parcel & NG911 Data QA Toolkit

Checks a county's tax parcels, site address points and road centerlines against each other and
against NG911 addressing rules, then writes every finding to one error layer.
Live results for Sheboygan County: https://krauskagis.com/parcel-qa.html

## Run it

```bash
pip install geopandas pyogrio
python3 fetch_arcgis.py config/sheboygan.json raw     # download the county's public layers
python3 parcel_qa.py   config/sheboygan.json out      # run the 19 checks
python3 make_web.py    config/sheboygan.json out ../../data/parcel-qa   # web map data
python3 tests/test_synthetic.py                       # every check must catch its planted error
```

Outputs in `out/`: `qa_findings.gpkg` (layer `findings`: check code, severity, feature IDs, plain-language detail),
`qa_summary.csv`, `qa_findings.geojson`.

## Another county

Copy `config/sheboygan.json`, point `sources` at the county's REST layers (or `inputs` at files you already
have), and map the field names. No code changes.

## In ArcGIS Pro

`ParcelQA.pyt` wraps the same checks as a geoprocessing tool. It needs geopandas in a cloned Pro
environment (instructions at the top of the file).

## The checks

| Code | Layer | Check |
|---|---|---|
| P01 | Parcels | Overlapping parcels (flags parcels nested inside another as possible unsplit CSMs or condos) |
| P02 | Parcels | Gaps between parcels that are not right-of-way |
| P03 | Parcels | Duplicate parcel IDs with conflicting attributes or overlapping pieces |
| P04 | Parcels | Missing required attributes |
| P05 | Parcels | Slivers |
| P06 | Parcels | Invalid geometry |
| A01 | Addresses | Missing NG911-required attributes |
| A02 | Addresses | Point outside the parcel its ParcelID names |
| A03 | Addresses | Point outside every parcel |
| A04 | Addresses | Broken road centerline link |
| A05 | Addresses | Street name differs from the linked road |
| A06 | Addresses | House number outside the linked road's ranges (suggests the right segment) |
| A07 | Addresses | Odd/even on the wrong side of the road |
| A08 | Addresses | Unusually far from the linked road |
| A09 | Addresses | Duplicate addresses in one municipality |
| A10 | Addresses | Municipality differs from the boundary it sits in |
| R01 | Roads | A range side mixing odd and even |
| R02 | Roads | Overlapping ranges on one street (same parity) |
| R03 | Roads | Segment with linked addresses but no range |
| L01 | Descriptions | Tax-roll legal description doesn't close (more than 1 ft and worse than 1:5,000) |
| L02 | Descriptions | Description closes but doesn't match the mapped parcel (over 10 ft after best fit, or area off by over 5%) |

## Legal description reader (L01, L02)

`legal_desc/ldreader.py` reads the metes-and-bounds descriptions in the tax roll's `TAXDSCRP` field:
tie courses, boundary courses, curves (by chord), misclosure, area, a review table of every call's
source text next to what was read, and an ArcMap-format traverse file that ArcGIS Pro's Traverse pane
loads. Parsing is deterministic (regular expressions, no machine learning).

```bash
python3 legal_desc/ldreader.py "COM AT NE COR, TH S89 DEG 08'58\"W 835.44', ... TO BEG."   # one description
python3 legal_desc/county_run.py config/sheboygan.json raw out                          # every parcel: L01 and L02
python3 tests/test_ldreader.py      # answer key: James's five hand-drafted COGO parcels, plus tax-roll formats
```

Outputs in `out/`: `legal_desc_results.csv` (one row per parcel), `legal_desc_findings.gpkg`, `legal_desc_summary.json`.
Traverse files for the five drafted parcels are in `legal_desc/traverse/`; their start points are estimated
from the county map and should be snapped to the PLSS corner in the parcel fabric.

L01 and L02 run in Python only: reading the descriptions is text parsing that has no PostGIS equivalent,
so they are not part of the 19-check SQL comparison.

## PostGIS version

The same checks as spatial SQL views in PostgreSQL/PostGIS: see [`postgis/`](postgis/README.md). On the
whole county, SQL and Python return the same 1,323 findings on the same features.

Planned next: `report/parcel_qa_report.qmd`, a Quarto report built from the database views (Python vs. SQL
counts, findings map, examples, how to rerun), rendered to HTML for the project page and to PDF.

Findings are items to review, not confirmed errors. Not an official county product.
