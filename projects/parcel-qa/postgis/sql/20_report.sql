-- All findings in one layer (add qa.findings to ArcGIS Pro or QGIS), and the summary table that
-- matches the Python toolkit's qa_summary.csv
CREATE VIEW qa.findings AS
SELECT (row_number() OVER (ORDER BY f.check_code, f.feature_id))::integer AS fid, f.check_code, c.layer, c.severity, c.title, f.feature_id, f.detail,
       f.geom::geometry(Point, 3071) AS geom
FROM (
  SELECT * FROM qa.p01_overlaps UNION ALL SELECT * FROM qa.p02_gaps UNION ALL SELECT * FROM qa.p03_duplicate_ids
  UNION ALL SELECT * FROM qa.p04_missing_attributes UNION ALL SELECT * FROM qa.p05_slivers UNION ALL SELECT * FROM qa.p06_invalid_geometry
  UNION ALL SELECT * FROM qa.a01_missing_attributes UNION ALL SELECT * FROM qa.a02_a03_parcels
  UNION ALL SELECT * FROM qa.a04_a08_road_links UNION ALL SELECT * FROM qa.a09_duplicates UNION ALL SELECT * FROM qa.a10_municipality
  UNION ALL SELECT * FROM qa.r01_mixed_parity UNION ALL SELECT * FROM qa.r02_overlapping_ranges UNION ALL SELECT * FROM qa.r03_missing_range
) f JOIN lkp.qa_check c ON c.code = f.check_code;

CREATE VIEW qa.summary AS
WITH totals(layer, checked) AS (
  SELECT 'parcels', count(*) FROM core.parcels UNION ALL
  SELECT 'addresses', count(*) FROM qa.active_addresses UNION ALL
  SELECT 'roads', count(*) FROM core.road_centerlines
)
SELECT c.code AS check_code, c.layer, c.severity, c.title, count(f.fid) AS count, t.checked,
       round(count(f.fid) * 1000.0 / t.checked, 2) AS rate_per_1000
FROM lkp.qa_check c JOIN totals t USING (layer) LEFT JOIN qa.findings f ON f.check_code = c.code
GROUP BY c.code, c.layer, c.severity, c.title, t.checked
ORDER BY c.code;
