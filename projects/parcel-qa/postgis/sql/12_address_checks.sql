-- Address point checks A01-A10, plus road check R03 (it needs to know which segments addresses link to)

-- +1 if the point is left of the line's direction at its nearest point, -1 if right
-- (measured 1 m either side of the nearest point; multi-part lines use their nearest part)
-- PostGIS calls are written public.ST_…: PostgreSQL 17+ builds materialized views with a locked-down search
-- path, and naming the schema (instead of SET search_path) keeps the function inlinable, which is much faster
CREATE FUNCTION qa.side_of_line(line geometry, pt geometry) RETURNS integer LANGUAGE sql IMMUTABLE PARALLEL SAFE AS $$
  WITH part AS (
    SELECT g FROM (SELECT (public.ST_Dump(public.ST_LineMerge(line))).geom AS g) d ORDER BY public.ST_Distance(g, pt) LIMIT 1
  ), ab AS (
    SELECT public.ST_LineInterpolatePoint(g, greatest(0, public.ST_LineLocatePoint(g, pt) - 1.0 / public.ST_Length(g))) AS a,
           public.ST_LineInterpolatePoint(g, least(1, public.ST_LineLocatePoint(g, pt) + 1.0 / public.ST_Length(g))) AS b
    FROM part WHERE public.ST_Length(g) > 0
  )
  SELECT CASE WHEN (public.ST_X(b) - public.ST_X(a)) * (public.ST_Y(pt) - public.ST_Y(a)) - (public.ST_Y(b) - public.ST_Y(a)) * (public.ST_X(pt) - public.ST_X(a)) > 0
              THEN 1 ELSE -1 END
  FROM ab
$$;

CREATE VIEW qa.active_addresses AS
SELECT a.* FROM core.address_points a JOIN lkp.address_status s ON s.code = a.status AND s.is_active;

-- one row per street address (an apartment building's unit points count once), with its road link
CREATE MATERIALIZED VIEW qa.address_links AS
SELECT DISTINCT ON (addr_num_raw, street, muni)
       addr_oid, addr_id, addr_num, street, street_n, muni, geom,
       CASE WHEN btrim(road_id) IN ('', 'None', 'nan') THEN NULL ELSE btrim(road_id) END AS link
FROM qa.active_addresses
ORDER BY addr_num_raw, street, muni, addr_oid;

-- A01 missing NG911-required attributes
CREATE MATERIALIZED VIEW qa.a01_missing_attributes AS
SELECT 'A01'::text AS check_code, a.addr_id AS feature_id, 'Field ''' || f.col || ''' is empty' AS detail, a.geom
FROM qa.active_addresses a
CROSS JOIN LATERAL (VALUES ('addrnum', a.addr_num_raw), ('fullname', a.street), ('municipality', a.muni),
                           ('esn', a.esn), ('msag', a.msag)) AS f(col, val)
WHERE qa.is_blank(f.val);

-- A02 / A03 parcel containment
CREATE MATERIALIZED VIEW qa.a02_a03_parcels AS
WITH hit AS (
  SELECT a.addr_id, a.geom, NULLIF(btrim(a.parcel_id), '') AS claimed,
         array_agg(p.parcel_id) FILTER (WHERE p.parcel_id IS NOT NULL) AS inside
  FROM qa.active_addresses a
  LEFT JOIN core.parcels p ON ST_Within(a.geom, p.geom)
  GROUP BY a.addr_id, a.geom, a.parcel_id
)
SELECT CASE WHEN inside IS NULL THEN 'A03' ELSE 'A02' END AS check_code, addr_id AS feature_id,
       CASE WHEN inside IS NULL
            THEN 'Point is not inside any tax parcel' || coalesce(' (claims parcel ' || claimed || ')', '')
            ELSE 'Claims parcel ' || claimed || ' but sits in ' || array_to_string(inside, ', ') END AS detail,
       geom
FROM hit
WHERE inside IS NULL
   OR (NOT qa.is_blank(claimed) AND NOT claimed = ANY (inside));

-- A04-A08: everything that compares a point with the road segment it links to
CREATE MATERIALIZED VIEW qa.a04_a08_road_links AS
WITH far AS (SELECT value AS m FROM lkp.settings WHERE name = 'far_from_road_m'),
j AS (
  SELECT u.*, r.road_id, r.name AS road_name, r.name_n AS road_name_n, r.geom AS road_geom,
         ST_Distance(r.geom, u.geom) AS dist,
         r.from_left, r.to_left, r.from_right, r.to_right
  FROM qa.address_links u LEFT JOIN core.road_centerlines r ON r.road_id = u.link
  WHERE u.link IS NOT NULL
),
sides AS (
  SELECT j.*, qa.side_of_line(road_geom, geom) AS side FROM j WHERE road_id IS NOT NULL
),
ranges AS (
  SELECT s.*,
         least(CASE WHEN side > 0 THEN coalesce(from_left, 0) ELSE coalesce(from_right, 0) END,
               CASE WHEN side > 0 THEN coalesce(to_left, 0) ELSE coalesce(to_right, 0) END) AS lo_s,
         greatest(CASE WHEN side > 0 THEN coalesce(from_left, 0) ELSE coalesce(from_right, 0) END,
                  CASE WHEN side > 0 THEN coalesce(to_left, 0) ELSE coalesce(to_right, 0) END) AS hi_s,
         least(CASE WHEN side > 0 THEN coalesce(from_right, 0) ELSE coalesce(from_left, 0) END,
               CASE WHEN side > 0 THEN coalesce(to_right, 0) ELSE coalesce(to_left, 0) END) AS lo_o,
         greatest(CASE WHEN side > 0 THEN coalesce(from_right, 0) ELSE coalesce(from_left, 0) END,
                  CASE WHEN side > 0 THEN coalesce(to_right, 0) ELSE coalesce(to_left, 0) END) AS hi_o,
         CASE WHEN side > 0 THEN 'left' ELSE 'right' END AS s_name
  FROM sides s
)
-- A04 link points to a centerline ID that does not exist
SELECT 'A04'::text AS check_code, addr_id AS feature_id, 'Road ID ' || link || ' not found in centerlines' AS detail, geom
FROM j WHERE road_id IS NULL
UNION ALL
-- A05 street name on the point differs from the segment's
SELECT 'A05', addr_id, 'Point says ''' || street || ''', road segment says ''' || road_name || '''', geom
FROM j WHERE road_id IS NOT NULL AND street_n <> '' AND road_name_n <> '' AND street_n <> road_name_n
UNION ALL
-- A08 unusually far from its segment
SELECT 'A08', addr_id, to_char(dist, 'FM999,990') || ' m from its road segment', geom
FROM j, far WHERE road_id IS NOT NULL AND dist > far.m
UNION ALL
-- A06 house number outside both sides' ranges, with a hint when a nearby segment of the same street fits
SELECT 'A06', r.addr_id,
       r.addr_num || ' is outside the segment''s ranges (' || r.lo_s || '–' || r.hi_s || ' this side, '
       || r.lo_o || '–' || r.hi_o || ' other side)'
       || coalesce('; it fits nearby segment ' || h.road_id || ' (' || to_char(h.d, 'FM999,990') || ' m away), so the road link may be wrong', ''),
       r.geom
FROM ranges r
LEFT JOIN LATERAL (
  SELECT o.road_id, ST_Distance(o.geom, r.geom) AS d
  FROM core.road_centerlines o
  WHERE o.name_n = r.street_n
    AND r.addr_num BETWEEN least(NULLIF(o.from_left, 0), NULLIF(o.to_left, 0), NULLIF(o.from_right, 0), NULLIF(o.to_right, 0))
                       AND greatest(o.from_left, o.to_left, o.from_right, o.to_right)
    AND ST_DWithin(o.geom, r.geom, 1000)
  ORDER BY ST_Distance(o.geom, r.geom), o.road_oid LIMIT 1   -- ties: first segment in download order, as in Python
) h ON true
WHERE r.addr_num > 0 AND NOT (r.hi_s <= 0 AND r.hi_o <= 0)
  AND NOT (r.addr_num BETWEEN r.lo_s AND r.hi_s) AND NOT (r.addr_num BETWEEN r.lo_o AND r.hi_o)
UNION ALL
-- A07 inside the other side's range, and the parity says it belongs over there
SELECT 'A07', addr_id, addr_num || ' is on the ' || s_name || ' side, but the ' || s_name || ' range is ' || lo_s || '–' || hi_s, geom
FROM ranges
WHERE addr_num > 0 AND NOT (hi_s <= 0 AND hi_o <= 0)
  AND (addr_num BETWEEN lo_s AND hi_s OR addr_num BETWEEN lo_o AND hi_o)
  AND hi_s > 0 AND lo_s % 2 <> addr_num % 2 AND addr_num BETWEEN lo_o AND hi_o AND lo_o % 2 = addr_num % 2 AND dist > 3;

-- R03 named segment with no range, where an address range is expected and addresses link to it
CREATE MATERIALIZED VIEW qa.r03_missing_range AS
SELECT 'R03'::text AS check_code, r.road_id AS feature_id,
       r.name || ' segment has no address range, but ' || count(*) || ' address(es) link to it' AS detail,
       ST_LineInterpolatePoint(ST_GeometryN(r.geom, 1), 0.5)::geometry(Point, 3071) AS geom
FROM core.road_centerlines r
JOIN qa.address_links u ON u.link = r.road_id
LEFT JOIN lkp.road_class c ON c.code = r.road_class
LEFT JOIN lkp.road_status s ON s.code = r.status
WHERE r.name_n <> ''
  AND coalesce(r.from_left, 0) = 0 AND coalesce(r.to_left, 0) = 0 AND coalesce(r.from_right, 0) = 0 AND coalesce(r.to_right, 0) = 0
  AND coalesce(c.range_expected, true) AND coalesce(s.range_expected, true)
GROUP BY r.road_id, r.name, r.geom;

-- A09 duplicate full address + unit + municipality
CREATE MATERIALIZED VIEW qa.a09_duplicates AS
SELECT 'A09'::text AS check_code,
       array_to_string((array_agg(addr_id ORDER BY addr_oid))[1:4], ' / ') AS feature_id,
       count(*) || ' points share ''' || k || '''' AS detail,
       (array_agg(geom ORDER BY addr_oid))[1] AS geom
FROM (SELECT addr_id, addr_oid, geom,
             btrim(upper(coalesce(full_addr, '') || ' ' || coalesce(unit, '') || ' ' || coalesce(muni, ''))) AS k
      FROM qa.active_addresses WHERE NOT qa.is_blank(full_addr)) d
GROUP BY k HAVING count(*) > 1;

-- A10 municipality on the point vs. the boundary it sits in
CREATE MATERIALIZED VIEW qa.a10_municipality AS
WITH j AS (
  SELECT DISTINCT ON (a.addr_oid) a.addr_id, a.muni, m.label, a.geom
  FROM qa.active_addresses a JOIN core.municipalities m ON ST_Within(a.geom, m.geom)
  ORDER BY a.addr_oid, m.muni_oid
)
SELECT 'A10'::text AS check_code, addr_id AS feature_id, 'Point says ''' || muni || ''', boundary says ''' || label || '''' AS detail, geom
FROM j
WHERE NOT qa.is_blank(muni)
  AND regexp_replace(upper(btrim(muni)), '\s+', ' ', 'g') <> regexp_replace(upper(btrim(label)), '\s+', ' ', 'g');
