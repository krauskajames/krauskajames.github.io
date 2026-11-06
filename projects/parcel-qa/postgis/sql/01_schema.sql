-- Parcel & NG911 QA: database schema.
-- Run order: 01_schema.sql -> (load_postgis.py fills src.*) -> 02_core.sql -> 10..12 checks -> 20_report.sql
-- Tested on PostgreSQL 16-18 with PostGIS 3.4-3.6. All geometry is EPSG:3071 (Wisconsin Transverse
-- Mercator, meters) so distance and area thresholds match the Python toolkit.

CREATE EXTENSION IF NOT EXISTS postgis;

DROP SCHEMA IF EXISTS qa CASCADE;
DROP SCHEMA IF EXISTS core CASCADE;
DROP SCHEMA IF EXISTS lkp CASCADE;
CREATE SCHEMA IF NOT EXISTS src;    -- raw county layers, as downloaded (written by load_postgis.py)
CREATE SCHEMA lkp;                  -- lookup tables: the database version of geodatabase domains
CREATE SCHEMA core;                 -- cleaned, typed, constrained tables the checks read from
CREATE SCHEMA qa;                   -- one materialized view per check, plus the findings and summary views

-- ---------------------------------------------------------------- helper functions (same rules as parcel_qa.py)
-- blank(): empty, null, or a placeholder the county uses for "no value"
CREATE FUNCTION qa.is_blank(v text) RETURNS boolean LANGUAGE sql IMMUTABLE PARALLEL SAFE AS $$
  SELECT v IS NULL OR btrim(v) IN ('', 'None', 'nan', '0', '<Null>')
$$;
-- first run of digits as an integer: '123A' -> 123, 'N8598' -> 8598
CREATE FUNCTION qa.to_int(v text) RETURNS integer LANGUAGE sql IMMUTABLE PARALLEL SAFE AS $$
  SELECT substring(v FROM '\d+')::integer
$$;
-- street name normalized for comparison: 'Fond Du Lac Ave.' -> 'FOND DU LAC AVE'
CREATE FUNCTION qa.norm_name(v text) RETURNS text LANGUAGE sql IMMUTABLE PARALLEL SAFE AS $$
  SELECT btrim(regexp_replace(regexp_replace(upper(coalesce(v, '')), '[^A-Z0-9 ]', '', 'g'), '\s+', ' ', 'g'))
$$;

-- ---------------------------------------------------------------- lookup tables
CREATE TABLE lkp.qa_check (
  code        text PRIMARY KEY CHECK (code ~ '^[PAR][0-9]{2}$'),
  layer       text NOT NULL CHECK (layer IN ('parcels', 'addresses', 'roads')),
  severity    text NOT NULL CHECK (severity IN ('high', 'medium', 'low')),
  title       text NOT NULL,
  description text NOT NULL
);
INSERT INTO lkp.qa_check VALUES
 ('P01','parcels','high','Overlapping parcels','Two parcels cover the same ground.'),
 ('P02','parcels','medium','Gap between parcels','A small hole between parcels that is not a road, water or other public land.'),
 ('P03','parcels','high','Duplicate parcel ID','More than one polygon carries the same parcel number.'),
 ('P04','parcels','medium','Missing required attribute','A required field (parcel ID, owner, site address or similar) is empty.'),
 ('P05','parcels','low','Sliver parcel','A very thin polygon, usually left over from editing.'),
 ('P06','parcels','high','Invalid geometry','Self-intersecting or otherwise invalid polygon.'),
 ('A01','addresses','medium','Missing required attribute','An NG911-required field (number, street, municipality, ESN or MSAG community) is empty.'),
 ('A02','addresses','high','Outside its parcel','The point does not fall inside the parcel its ParcelID points to.'),
 ('A03','addresses','medium','Outside every parcel','The point does not fall in any tax parcel.'),
 ('A04','addresses','high','Road link broken','The road centerline ID on the point does not exist.'),
 ('A05','addresses','high','Street name mismatch','The point''s street name differs from its linked road segment.'),
 ('A06','addresses','high','Number outside road range','The house number is outside the address range of its linked road segment.'),
 ('A07','addresses','medium','Wrong side of the road','An odd number sits on the even side of the road, or the reverse.'),
 ('A08','addresses','medium','Far from its road','The point is unusually far from its linked road segment.'),
 ('A09','addresses','high','Duplicate address','Two active points share the same full address and unit.'),
 ('A10','addresses','medium','Municipality mismatch','The municipality on the point differs from the municipal boundary it sits in.'),
 ('R01','roads','medium','Mixed parity range','A side of the road range mixes odd and even numbers.'),
 ('R02','roads','high','Overlapping ranges','Two segments of the same street in the same municipality claim overlapping numbers on the same side.'),
 ('R03','roads','low','Missing range','A named road segment has no address range.');

-- Codes are filled from the data by 02_core.sql; the flags are the business rules.
CREATE TABLE lkp.address_status (code text PRIMARY KEY, is_active boolean NOT NULL DEFAULT false);
CREATE TABLE lkp.road_class     (code text PRIMARY KEY, range_expected boolean NOT NULL DEFAULT true);
CREATE TABLE lkp.road_status    (code text PRIMARY KEY, range_expected boolean NOT NULL DEFAULT true);
CREATE TABLE lkp.muni_type      (code text PRIMARY KEY, label_pattern text NOT NULL DEFAULT '{name}');
CREATE TABLE lkp.settings       (name text PRIMARY KEY, value numeric NOT NULL);
INSERT INTO lkp.settings VALUES ('overlap_min_m2', 5), ('gap_max_m2', 500), ('sliver_width_m', 1.5), ('far_from_road_m', 400);

-- ---------------------------------------------------------------- core tables
CREATE TABLE core.municipalities (
  muni_oid  integer PRIMARY KEY,
  name      text NOT NULL,
  muni_type text REFERENCES lkp.muni_type (code),
  label     text NOT NULL,                       -- 'Village of Cascade', as address points spell it
  geom      geometry(MultiPolygon, 3071) NOT NULL
);

CREATE TABLE core.parcels (
  parcel_oid   integer PRIMARY KEY,               -- row order of the download, same index the Python run uses
  parcel_id    text,                              -- not UNIQUE: multi-part parcels repeat it (P03 checks the bad cases)
  owner        text,
  site_address text,
  muni         text,
  is_row       boolean NOT NULL,                  -- right-of-way / non-tax: no owner and no municipality
  geom_raw     geometry(MultiPolygon, 3071) NOT NULL,   -- as published, possibly invalid (P06)
  geom         geometry(MultiPolygon, 3071) NOT NULL CHECK (ST_IsValid(geom))
);

CREATE TABLE core.road_centerlines (
  road_oid    integer PRIMARY KEY,
  road_id     text NOT NULL UNIQUE,
  name        text,
  name_n      text GENERATED ALWAYS AS (qa.norm_name(name)) STORED,
  muni        text,
  from_left   integer CHECK (from_left >= 0),
  to_left     integer CHECK (to_left >= 0),
  from_right  integer CHECK (from_right >= 0),
  to_right    integer CHECK (to_right >= 0),
  road_class  text REFERENCES lkp.road_class (code),
  status      text REFERENCES lkp.road_status (code),
  geom        geometry(MultiLineString, 3071) NOT NULL
);

CREATE TABLE core.address_points (
  addr_oid     integer PRIMARY KEY,
  addr_id      text NOT NULL UNIQUE,
  addr_num_raw text,
  addr_num     integer GENERATED ALWAYS AS (qa.to_int(addr_num_raw)) STORED,
  street       text,
  street_n     text GENERATED ALWAYS AS (qa.norm_name(street)) STORED,
  full_addr    text,
  unit         text,
  parcel_id    text,                              -- the parcel the point claims (no FK: checking it is A02's job)
  road_id      text,                              -- the centerline the point claims (no FK: A04)
  muni         text,
  esn          text,
  msag         text,
  status       text REFERENCES lkp.address_status (code),
  geom         geometry(Point, 3071) NOT NULL
);
