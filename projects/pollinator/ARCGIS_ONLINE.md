# Publishing the Pollinator data to ArcGIS Online

This folder has three zipped shapefiles ready to upload. All are in NAD83(HARN) / Wisconsin Transverse Mercator (EPSG:3071).

| File | What it is | Key fields |
|---|---|---|
| `PollinatorSuitableHabitat.zip` | Suitable habitat for each host plant (cells at or above the model's 10th-percentile threshold; patches under ~2.5 km² removed) | `species`, `sci_name`, `pollinator`, `threshold`, `test_auc`, `area_km2` |
| `PollinatorHabitatOverlap.zip` | Areas suitable for 1, 2 or all 3 host plants | `n_species`, `label`, `area_km2` |
| `PollinatorRecords.zip` | The 1,269 thinned iNaturalist records the models were trained and tested on | `species`, `sci_name`, `source` |

Hosted feature layers use a small amount of credit storage. These three layers are small, so the cost is negligible.

## 1. Upload the layers (about 10 minutes)

1. Sign in at arcgis.com and go to **Content → New item → Your device**.
2. Choose `PollinatorSuitableHabitat.zip`, then select **Add PollinatorSuitableHabitat.zip and create a hosted feature layer**.
3. Title: **Pollinator Host Plants – Suitable Habitat (Wisconsin)**. Tags: `MaxEnt, pollinators, Wisconsin, species distribution`. Summary: *MaxEnt-predicted suitable habitat for swamp milkweed, wild lupine and fringed loosestrife.*
4. Repeat for the other two zips:
   - **Pollinator Host Plants – Habitat Overlap**
   - **Pollinator Host Plants – iNaturalist Records**

## 2. Build the web map

1. Open **Map Viewer** and add the three layers. Put Records on top, then Suitable Habitat, then Overlap.
2. **Basemap:** Light Gray Canvas, to match the site.
3. **Suitable Habitat:** choose *Types (unique symbols)* on `species`, with fill transparency around 35% and no outline.
   - Swamp milkweed `#5f8c4c`
   - Wild lupine `#2d5638`
   - Fringed loosestrife `#9bb26a`
   - Add a **filter**, or make three copies of the layer, so viewers can turn each species on and off.
4. **Overlap:** *Types* on `label`, using the site's ramp:
   - 1 of 3 `#cdd6a3`
   - 2 of 3 `#5f8c4c`
   - 3 of 3 `#173322`
   Leave this layer turned off by default.
5. **Records:** small 4 px dark circles (`#1b241d`) with a white outline. Make them visible only when zoomed in past state level (*Visibility range*).
6. **Pop-ups:**
   - Suitable Habitat: *"{species} ({sci_name}), host plant for the {pollinator}. Model test AUC {test_auc}."*
   - Records: *"{species}, iNaturalist research-grade record"*
7. Save the map as **Pollinator Habitat Explorer – Wisconsin**. In the description, link back to https://krauskagis.com/pollinator.html.

## 3. Share and link it

1. **Share → Everyone (public).** Accept the prompt to share the layers too.
2. Optional: **Create app → Instant Apps → Sidebar**, or **Dashboards**, for a more finished viewer. Either one looks good to WLIA recruiters.
3. Copy the public URL of the web map or app.
4. In `pollinator.html` in the site repo, find this line and paste the URL between the quotes:

   ```js
   const AGOL_URL = "";
   ```

   The **Explore the data in ArcGIS Online ↗** button appears under the map once it's set. Until then it stays hidden, so the page never shows a dead link.

## Rebuilding these files

Run `python make_agol_layers.py` from the `Senior Year Geography Stevens Point` folder after any new MaxEnt run. It reads `MaxEnt2026\output_landcover` and writes this folder.
