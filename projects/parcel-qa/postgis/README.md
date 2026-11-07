# Parcel & NG911 QA in PostGIS

The same 19 checks as `parcel_qa.py`, rewritten as spatial SQL. On Sheboygan County (63,391 parcels,
61,811 address points, 9,852 road segments, data of Nov 5–6, 2026) the SQL and Python versions return
the same 1,323 findings on the same features. The checks take about 30 seconds in PostgreSQL.

| File | What it does |
|---|---|
| `sql/01_schema.sql` | Schemas `src` (raw), `lkp` (lookups), `core` (typed tables), `qa` (checks); primary keys, foreign keys to lookup tables (the database version of geodatabase domains), CHECK constraints, typed PostGIS geometry columns, generated columns for normalized street names |
| `sql/02_core.sql` | Fills the lookups and core tables from the raw layers, repairs invalid polygons into a separate column, builds GiST spatial indexes. County-specific column names live only here. |
| `sql/10_parcel_checks.sql` | P01–P06: overlaps (indexed self-join), gaps (holes in the `ST_Union` of the fabric), duplicate IDs, missing attributes, slivers, invalid geometry |
| `sql/11_road_checks.sql` | R01–R02: mixed-parity ranges, overlapping ranges on the same street |
| `sql/12_address_checks.sql` | A01–A10 and R03: parcel containment (`ST_Within`), road links, house number vs. range with a side-of-road function, nearest-segment hints (`LATERAL` + `ST_DWithin`), duplicates, municipality |
| `sql/20_report.sql` | `qa.findings` (one point layer with every finding) and `qa.summary` (counts, matching `qa_summary.csv`) |
| `load_postgis.py` | Downloads the layers if needed, loads them into `src`, runs the SQL files, prints SQL vs. Python counts |

Each check is a materialized view with the same four columns (`check_code, feature_id, detail, geom`),
so `SELECT * FROM qa.a06_a08…` or `qa.findings WHERE check_code = 'A06'` gives one check's results.
Thresholds (overlap 5 m², gap 500 m², sliver 1.5 m, far from road 400 m) are rows in `lkp.settings`.

## Run it (Windows, ArcGIS Pro's cloned Python environment)

```
activate arcgispro-py3-qa
cd "%USERPROFILE%\OneDrive\Documents\Claude outputs\ParcelQA"
python postgis\load_postgis.py config\sheboygan.json
python parcel_qa.py config\sheboygan.json out
python postgis\load_postgis.py config\sheboygan.json --skip-load --compare out\qa_summary.csv
```

Needs PostgreSQL with PostGIS (tested on 16 + PostGIS 3.4 and 18.6 + 3.6.2) and geopandas, sqlalchemy,
psycopg2-binary and geoalchemy2. It asks for the postgres password unless `PGPASSWORD` is set.

## The report

`../report/parcel_qa_report.qmd` reads the database (and `out/qa_summary.csv` from the Python run) and
renders an HTML page and a PDF: SQL vs. Python by check, a findings map, findings per 1,000 addresses by
municipality, one example of each finding, and the table inventory. With `PGPASSWORD` set:

```
quarto render report\parcel_qa_report.qmd
```

## Porting to SQL Server spatial

The logic carries over; the syntax changes. `geometry::STGeomFromText(…, 3071)` instead of typed
columns, `a.geom.STIntersects(b.geom) = 1` instead of `ST_Intersects`, `.STArea()`, `.STDistance()`,
`.STWithin()`, `geometry::UnionAggregate()` for the fabric dissolve, `.STInteriorRingN()` for the gap
holes, `CROSS APPLY` instead of `LATERAL`, and indexed views or tables refreshed by a job instead of
materialized views. Many Wisconsin county enterprise geodatabases run on SQL Server, so the same checks
can run where the data already lives.

## Known differences from the Python version

- P06 text names the reason PostGIS gives (for example `Ring Self-intersection[x y]`).
- R02: for four pairs whose ranges start at the same number, the two ranges are listed in the other order.
