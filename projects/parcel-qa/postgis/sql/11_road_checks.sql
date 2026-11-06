-- Road centerline checks R01-R02 (R03 needs the address links, so it is in 12_address_checks.sql)

-- each side of each named segment as a number range, lowest number first
CREATE VIEW qa.road_sides AS
SELECT road_id, name, name_n, muni, side, f AS from_n, t AS to_n,
       least(f, t) AS lo, greatest(f, t) AS hi, least(f, t) % 2 AS parity, geom
FROM core.road_centerlines r
CROSS JOIN LATERAL (VALUES ('left', r.from_left, r.to_left), ('right', r.from_right, r.to_right)) AS s(side, f, t)
WHERE name_n <> '';

-- R01 one side mixes odd and even
CREATE MATERIALIZED VIEW qa.r01_mixed_parity AS
SELECT 'R01'::text AS check_code, road_id AS feature_id,
       initcap(side) || ' range ' || from_n || '–' || to_n || ' mixes odd and even' AS detail,
       ST_LineInterpolatePoint(ST_GeometryN(geom, 1), 0.5)::geometry(Point, 3071) AS geom
FROM qa.road_sides
WHERE from_n > 0 AND to_n > 0 AND from_n % 2 <> to_n % 2;

-- R02 overlapping ranges: two segments of the same street in the same municipality whose ranges of the
-- same parity overlap. Comparing odd with odd and even with even (not left with left) avoids false alarms
-- where two segments were digitized in opposite directions. One row per pair of segments.
CREATE MATERIALIZED VIEW qa.r02_overlapping_ranges AS
WITH pairs AS (
  SELECT a.road_id AS id_a, b.road_id AS id_b, a.lo AS lo_a, a.hi AS hi_a, b.lo AS lo_b, b.hi AS hi_b,
         a.parity, a.geom,
         row_number() OVER (PARTITION BY least(a.road_id, b.road_id), greatest(a.road_id, b.road_id)
                            ORDER BY a.lo, b.lo) AS k
  FROM qa.road_sides a
  JOIN qa.road_sides b
    ON a.name_n = b.name_n AND a.muni = b.muni AND a.parity = b.parity
   AND a.road_id <> b.road_id AND a.lo > 0 AND b.lo > 0
   AND (a.lo, a.road_id) <= (b.lo, b.road_id) AND b.lo < a.hi
)
SELECT 'R02'::text AS check_code, least(id_a, id_b) || ' / ' || greatest(id_a, id_b) AS feature_id,
       CASE parity WHEN 1 THEN 'Odd' ELSE 'Even' END || ' ranges ' || lo_a || '–' || hi_a || ' and ' || lo_b || '–' || hi_b || ' overlap' AS detail,
       ST_LineInterpolatePoint(ST_GeometryN(geom, 1), 0.5)::geometry(Point, 3071) AS geom
FROM pairs WHERE k = 1;
