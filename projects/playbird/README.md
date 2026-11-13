# Playbird Rd: from farm field to neighborhood

Roadmap item 46. Page: `playbird.html` (built with `python3 projects/assemble_page.py projects/playbird/page_body.html playbird.html ...`).

- `scripts/fetch.py`, `scripts/fetch2.py`: download the parcels within 200 ft / 1,000 ft / 1,400 ft of parcel 59024341550, the zoning districts and the ETJ check from Sheboygan County's public REST services.
- `scripts/build.py`: joins the toolbox outputs (`parcels_in_notice_area.csv`, `mailing_list.csv` from `projects/zoning-notice`) to the geometry and writes `data/playbird/*.geojson`. Owner names are not written to the web data, only owner type, letter number and flags.

Chapter 2 code: `projects/zoning-notice/`.
