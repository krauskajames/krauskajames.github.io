-- Parcel checks P01-P06. Each check is a materialized view with the same four columns:
--   check_code, feature_id, detail, geom (a point to show on the map, EPSG:3071)

-- P06 invalid geometry
CREATE MATERIALIZED VIEW qa.p06_invalid_geometry AS
SELECT 'P06'::text AS check_code, parcel_id AS feature_id,
       'Invalid polygon geometry: ' || ST_IsValidReason(geom_raw) AS detail,
       ST_PointOnSurface(geom)::geometry(Point, 3071) AS geom
FROM core.parcels
WHERE NOT ST_IsValid(geom_raw);

-- P01 overlapping parcels: pairs whose intersection is at least overlap_min_m2.
-- The GiST index makes the && / ST_Intersects join fast; pieces of the same parcel are P03's job.
CREATE MATERIALIZED VIEW qa.p01_overlaps AS
WITH s AS (SELECT value AS min_m2 FROM lkp.settings WHERE name = 'overlap_min_m2'),
pairs AS (
  SELECT a.parcel_id AS id_a, b.parcel_id AS id_b, a.is_row AS row_a, b.is_row AS row_b,
         ST_Area(a.geom) AS area_a, ST_Area(b.geom) AS area_b,
         ST_Intersection(a.geom, b.geom) AS g
  FROM core.parcels a
  JOIN core.parcels b ON a.parcel_oid < b.parcel_oid AND ST_Intersects(a.geom, b.geom)
  WHERE a.parcel_id IS DISTINCT FROM b.parcel_id
)
SELECT 'P01'::text AS check_code, id_a || ' / ' || id_b AS feature_id,
       CASE WHEN row_a AND row_b THEN 'Two right-of-way polygons'
            WHEN row_a OR row_b THEN 'Parcel and right-of-way' ELSE 'Parcels' END
       || ' ' || id_a || ' and ' || id_b || ' overlap by ' || to_char(ST_Area(g), 'FM999,999,990') || ' m²'
       || CASE WHEN ST_Area(g) / least(area_a, area_b) > 0.9
               THEN ' (one sits almost entirely inside the other: possible unsplit CSM or condo)' ELSE '' END AS detail,
       ST_PointOnSurface(g)::geometry(Point, 3071) AS geom
FROM pairs, s
WHERE ST_Area(g) >= s.min_m2;

-- P02 gaps: interior rings (holes) of the dissolved parcel fabric between 1 m² and gap_max_m2
CREATE MATERIALIZED VIEW qa.p02_gaps AS
WITH s AS (SELECT value AS max_m2 FROM lkp.settings WHERE name = 'gap_max_m2'),
fabric AS (SELECT (ST_Dump(ST_Union(geom))).geom AS g FROM core.parcels),
holes AS (
  SELECT ST_MakePolygon(ST_InteriorRingN(g, n)) AS h
  FROM fabric, generate_series(1, ST_NumInteriorRings(g)) AS n
)
SELECT 'P02'::text AS check_code, ''::text AS feature_id,
       'Gap of ' || to_char(ST_Area(h), 'FM999,990') || ' m² between parcels' AS detail,
       ST_PointOnSurface(h)::geometry(Point, 3071) AS geom
FROM holes, s
WHERE ST_Area(h) BETWEEN 1 AND s.max_m2;

-- P03 duplicate parcel IDs: several polygons share an ID and either disagree on owner / site address /
-- municipality, or overlap each other (pieces of one multi-part parcel are normal)
CREATE MATERIALIZED VIEW qa.p03_duplicate_ids AS
WITH s AS (SELECT value AS min_m2 FROM lkp.settings WHERE name = 'overlap_min_m2'),
grp AS (
  SELECT parcel_id, count(*) AS n,
         array_remove(ARRAY[
           CASE WHEN count(DISTINCT btrim(coalesce(owner, ''))) > 1 THEN 'OWNERNME1' END,
           CASE WHEN count(DISTINCT btrim(coalesce(site_address, ''))) > 1 THEN 'SITEADDRESS' END,
           CASE WHEN count(DISTINCT btrim(coalesce(muni, ''))) > 1 THEN 'MUNI' END], NULL) AS conflict,
         (array_agg(geom ORDER BY parcel_oid))[1] AS first_geom
  FROM core.parcels
  WHERE NOT is_row AND NOT qa.is_blank(parcel_id)
  GROUP BY parcel_id HAVING count(*) > 1
),
ov AS (
  SELECT a.parcel_id, sum(ST_Area(ST_Intersection(a.geom, b.geom))) AS m2
  FROM core.parcels a JOIN core.parcels b
    ON a.parcel_id = b.parcel_id AND a.parcel_oid < b.parcel_oid AND ST_Intersects(a.geom, b.geom)
  WHERE NOT a.is_row AND NOT b.is_row
  GROUP BY a.parcel_id
)
SELECT 'P03'::text AS check_code, g.parcel_id AS feature_id,
       CASE WHEN cardinality(g.conflict) > 0
            THEN g.n || ' polygons share parcel ID ' || g.parcel_id || ' but differ in ' || array_to_string(g.conflict, ', ')
            ELSE g.n || ' pieces of parcel ' || g.parcel_id || ' overlap each other by ' || to_char(ov.m2, 'FM999,990') || ' m²' END,
       ST_PointOnSurface(g.first_geom)::geometry(Point, 3071)
FROM grp g LEFT JOIN ov USING (parcel_id), s
WHERE cardinality(g.conflict) > 0 OR coalesce(ov.m2, 0) >= s.min_m2;

-- P04 missing required attributes (tax parcels only; right-of-way has none by definition)
CREATE MATERIALIZED VIEW qa.p04_missing_attributes AS
SELECT 'P04'::text AS check_code, p.parcel_id AS feature_id, 'Field ''' || f.col || ''' is empty' AS detail,
       ST_PointOnSurface(p.geom)::geometry(Point, 3071) AS geom
FROM core.parcels p
CROSS JOIN LATERAL (VALUES ('PARCELID', p.parcel_id), ('OWNERNME1', p.owner), ('MUNI', p.muni)) AS f(col, val)
WHERE NOT p.is_row AND qa.is_blank(f.val);

-- P05 slivers: mean width (2 x area / perimeter) under sliver_width_m, and under 2,000 m²
CREATE MATERIALIZED VIEW qa.p05_slivers AS
WITH s AS (SELECT value AS w FROM lkp.settings WHERE name = 'sliver_width_m')
SELECT 'P05'::text AS check_code, parcel_id AS feature_id,
       'Sliver about ' || to_char(2 * ST_Area(geom) / ST_Perimeter(geom), 'FM990.0') || ' m wide, '
       || to_char(ST_Area(geom), 'FM999,990') || ' m²' AS detail,
       ST_PointOnSurface(geom)::geometry(Point, 3071) AS geom
FROM core.parcels, s
WHERE NOT is_row AND ST_Area(geom) > 0
  AND 2 * ST_Area(geom) / ST_Perimeter(geom) < s.w AND ST_Area(geom) < 2000;
