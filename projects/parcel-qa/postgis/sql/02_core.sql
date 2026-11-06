-- Fill lookups and core tables from src.* (the raw layers load_postgis.py wrote, already in EPSG:3071
-- with lowercase column names). Column names here are Sheboygan County's; for another county,
-- change only this file.

-- lookups: one row per code seen in the data, then the rules
INSERT INTO lkp.address_status (code) SELECT DISTINCT status FROM src.addresses WHERE status IS NOT NULL;
UPDATE lkp.address_status SET is_active = true WHERE code IN ('Current');
INSERT INTO lkp.road_class (code) SELECT DISTINCT roadclass FROM src.roads WHERE roadclass IS NOT NULL;
UPDATE lkp.road_class SET range_expected = false WHERE code IN ('Highway', 'Ramp', 'Freeway');
INSERT INTO lkp.road_status (code) SELECT DISTINCT rdstatus FROM src.roads WHERE rdstatus IS NOT NULL;
UPDATE lkp.road_status SET range_expected = false WHERE code IN ('Platted', 'Vacated', 'Under Construction');
INSERT INTO lkp.muni_type VALUES ('City', 'City of {name}'), ('Village', 'Village of {name}'), ('Township', '{name}');
INSERT INTO lkp.muni_type (code) SELECT DISTINCT munitype FROM src.municipalities
  WHERE munitype IS NOT NULL ON CONFLICT DO NOTHING;

INSERT INTO core.municipalities
SELECT m.src_oid, m.name, m.munitype,
       replace(coalesce(t.label_pattern, '{name}'), '{name}', m.name),
       ST_Multi(m.geom)
FROM src.municipalities m LEFT JOIN lkp.muni_type t ON t.code = m.munitype;

INSERT INTO core.parcels
SELECT src_oid, parcelid, ownernme1, siteaddress, muni,
       qa.is_blank(ownernme1) AND qa.is_blank(muni),
       ST_Multi(geom),
       CASE WHEN ST_IsValid(geom) THEN ST_Multi(geom)
            ELSE ST_Multi(ST_CollectionExtract(ST_MakeValid(geom), 3)) END
FROM src.parcels;

INSERT INTO core.road_centerlines (road_oid, road_id, name, muni, from_left, to_left, from_right, to_right, road_class, status, geom)
SELECT DISTINCT ON (centerlineid)
       src_oid, centerlineid, fullname, munileft,
       qa.to_int(fromleft::text), qa.to_int(toleft::text), qa.to_int(fromright::text), qa.to_int(toright::text),
       roadclass, rdstatus, ST_Multi(geom)
FROM src.roads WHERE centerlineid IS NOT NULL
ORDER BY centerlineid, src_oid;

INSERT INTO core.address_points (addr_oid, addr_id, addr_num_raw, street, full_addr, unit, parcel_id, road_id, muni, esn, msag, status, geom)
SELECT src_oid, siteaddid, addrnum, fullname, fulladdr, unitid, parcelid, rdclid, municipality, esn, msag, status, geom
FROM src.addresses;

-- spatial (GiST) and attribute indexes
CREATE INDEX ON core.parcels USING gist (geom);
CREATE INDEX ON core.parcels (parcel_id);
CREATE INDEX ON core.road_centerlines USING gist (geom);
CREATE INDEX ON core.road_centerlines (name_n, muni);
CREATE INDEX ON core.address_points USING gist (geom);
CREATE INDEX ON core.municipalities USING gist (geom);
ANALYZE core.parcels; ANALYZE core.road_centerlines; ANALYZE core.address_points; ANALYZE core.municipalities;
