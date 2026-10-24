#!/usr/bin/env bash
# Download every raw input for build_data.py into ./raw (not committed).
# ACS needs a free Census API key: CENSUS_KEY=... python3 fetch_acs.py raw/acs.json 2024
set -euo pipefail
mkdir -p raw && cd raw
T=https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb
curl -sS -o cousub.geojson "$T/tigerWMS_Current/MapServer/22/query?where=STATE%3D%2755%27+AND+COUNTY%3D%27139%27&outFields=GEOID,NAME,BASENAME,LSADC,AREALAND&outSR=4326&geometryPrecision=5&f=geojson"
curl -sS -o water.geojson "$T/Hydro/MapServer/1/query?where=AREAWATER%3E2000000&geometry=-89.0,43.88,-88.3,44.25&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=NAME,AREAWATER&outSR=4326&geometryPrecision=5&f=geojson"
for f in Final_Ests_MCD_2026 Final_Ests_Co_2026_Components Time_Series_MCD_2026 Time_Series_Co_2026 Tot_HUs_County_2026 Pop_Proj_Co_State_2020_2050 Pop_Proj_Muni_2020_2050 HH_Proj_Muni_2020-2050; do
  curl -sSL -o "$f.xlsx" "https://doa.wi.gov/DIR/$f.xlsx"
done
curl -sSL -o CAEMP25N.zip https://apps.bea.gov/regional/zip/CAEMP25N.zip && unzip -o -q CAEMP25N.zip 'CAEMP25N__ALL_AREAS_*.csv'
curl -sSL -o CAINC1.zip https://apps.bea.gov/regional/zip/CAINC1.zip && unzip -o -q CAINC1.zip 'CAINC1_WI_*.csv'
L=https://lehd.ces.census.gov/data/lodes/LODES8/wi
curl -sS -O $L/od/wi_od_main_JT00_2023.csv.gz -O $L/od/wi_od_aux_JT00_2023.csv.gz -O $L/wac/wi_wac_S000_JT00_2023.csv.gz -O $L/rac/wi_rac_S000_JT00_2023.csv.gz -O $L/wi_xwalk.csv.gz
echo "done"
