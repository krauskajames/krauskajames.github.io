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

Findings are items to review, not confirmed errors. Not an official county product.
