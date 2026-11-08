# Zoning hearing notice packet

Roadmap item 37 · chapter 2 of item 46 (Playbird Rd: from farm field to neighborhood).

A made-up petition to rezone Town of Sheboygan parcel 59024341550 from I-1 to PUD. The Town's code (Ch. 335, Art. XII) asks for the owners of all property within 200 ft, a 1 in = 100 ft plot plan, and written notice to the clerk of any municipality within 1,000 ft.

- `ZoningNotice.pyt`: ArcGIS Pro toolbox (Pro 3.7.3, arcpy + matplotlib only)
- `notice_core.py`: mailing-list logic, no arcpy (merge spellings, set aside right-of-way and blank owners, flag absentee owners, labels)
- `tests/test_notice_core.py`: `python tests/test_notice_core.py`
- `YOUR_PART.md`: the Pro steps

Hand run (Nov 8): 29 parcels, 17 owner rows. Playbird Rd is the Town of Sheboygan / Town of Mosel line, so Mosel's clerk is notified.
