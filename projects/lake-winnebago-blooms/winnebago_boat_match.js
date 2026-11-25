/**
 * Lake Winnebago: satellite values under the USGS boat transects
 * ---------------------------------------------------------------
 * The USGS FLAMe boat measured phycocyanin (the blue-green algae pigment) along its track on ten dates,
 * 2023 to 2025 (https://doi.org/10.5066/P1XHRFKZ). This script reads what the satellites saw at the same
 * places, so the satellite indexes can be charted against a field measurement.
 *
 *   Part A  Sentinel-2 (20 m), the nearest clear day within two days of each boat date.
 *   Part B  MODIS Terra and Aqua (250 m), the same day as the boat.
 *
 * Nothing is masked here. Cloud Score+ is exported as a column and the filtering is done afterwards,
 * so the choice of threshold can be changed without re-running Earth Engine.
 * The only output is one CSV export (Tasks tab). No charts, so the editor's limits do not apply.
 *
 * Before running: upload data/usgs_flame_winnebago_60m.csv as a table asset (Assets > NEW > CSV file upload,
 * X column: lon, Y column: lat) and put its ID in CONFIG.points.
 *
 * Written for James Krauska's Lake Winnebago project. License: MIT.
 */

// =============================== CONFIG ===================================
var CONFIG = {
  points: 'projects/gen-lang-client-0902051690/assets/usgs_flame_winnebago_60m',

  // Boat date (ymd) and the Sentinel-2 day to compare it with. daysOff = Sentinel-2 day minus boat day.
  // Chosen from winnebago_daily.csv: the clearest Sentinel-2 day within two days.
  // April 28 and May 1, 2025 are left out: overcast, and outside the bloom season.
  pairs: [
    {ymd: 20230807, s2: '2023-08-06', daysOff: -1},
    {ymd: 20230808, s2: '2023-08-06', daysOff: -2},
    {ymd: 20240624, s2: '2024-06-26', daysOff: 2},
    {ymd: 20240625, s2: '2024-06-26', daysOff: 1},
    {ymd: 20240729, s2: '2024-07-31', daysOff: 2},
    {ymd: 20240819, s2: '2024-08-20', daysOff: 1},
    {ymd: 20250707, s2: '2025-07-08', daysOff: 1},
    {ymd: 20250708, s2: '2025-07-08', daysOff: 0}
  ],

  coeffs: [14.039, 86.115, 194.325],   // Mishra & Mishra (2012) NDCI to chlorophyll-a, as in the other scripts
  s2Scale: 60,                         // metres: the boat readings are 60 m cell medians
  modisScale: 250,
  showOnMap: 0,                        // which pair to draw on the map (0 = the first)

  driveFolder: 'earthengine',
  fileName: 'winnebago_boat_match'
};
// ==========================================================================

var points = ee.FeatureCollection(CONFIG.points);
var csPlus = ee.ImageCollection('GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED');
var S2_BANDS = ['B2', 'B3', 'B4', 'B5', 'B6', 'B8A', 'B11'];

// An image with these band names and no data. Added underneath every mosaic so that a day with no
// scene gives empty columns instead of an error.
function blank(names) {
  return ee.Image.constant(ee.List.repeat(0, names.length)).rename(names).updateMask(0);
}

// ---- Part A: Sentinel-2 ---------------------------------------------------
function s2Day(dateString) {
  var d0 = ee.Date(dateString);
  var names = S2_BANDS.concat(['cs_cdf']);
  var mosaic = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(points.geometry().bounds())
    .filterDate(d0, d0.advance(1, 'day'))
    .linkCollection(csPlus, ['cs_cdf'])
    .select(names)
    .mosaic()
    .addBands(blank(names), null, false);
  var refl = mosaic.select(S2_BANDS).divide(10000);            // surface reflectance, 0 to 1
  var ndci = refl.normalizedDifference(['B5', 'B4']).rename('s2_ndci');
  var c = CONFIG.coeffs;
  var chl = ndci.expression('c0 + c1 * x + c2 * x * x', {x: ndci, c0: c[0], c1: c[1], c2: c[2]})
    .max(0).rename('s2_chl');
  // Floating Algae Index (Hu, 2009): near-infrared above a line drawn from red to shortwave infrared.
  // Band centres: B4 665 nm, B8A 865 nm, B11 1610 nm, so (865 - 665) / (1610 - 665) = 0.2116.
  var fai = refl.expression('nir - (red + (swir - red) * 0.2116)',
    {nir: refl.select('B8A'), red: refl.select('B4'), swir: refl.select('B11')}).rename('s2_fai');
  return refl.rename(['s2_blue', 's2_green', 's2_red', 's2_rededge1', 's2_rededge2', 's2_nir', 's2_swir'])
    .addBands([ndci, chl, fai, mosaic.select('cs_cdf').rename('s2_clear_score')]);
}

// ---- Part B: MODIS, same day ----------------------------------------------
function modisDay(ymd, collectionId, prefix) {
  var s = String(ymd);
  var d0 = ee.Date(s.slice(0, 4) + '-' + s.slice(4, 6) + '-' + s.slice(6, 8));
  var names = [prefix + '_red', prefix + '_nir'];
  var img = ee.ImageCollection(collectionId)
    .filterDate(d0, d0.advance(1, 'day'))
    .select(['sur_refl_b01', 'sur_refl_b02'], names)
    .mosaic()
    .addBands(blank(names), null, false)
    .multiply(0.0001);
  // Near-infrared minus red: positive where something is floating on the surface.
  return img.addBands(img.select(prefix + '_nir').subtract(img.select(prefix + '_red')).rename(prefix + '_nir_minus_red'));
}

// ---- Sample every boat cell -------------------------------------------------
var matched = ee.FeatureCollection(CONFIG.pairs.map(function (p) {
  var boat = points.filter(ee.Filter.eq('ymd', p.ymd));
  var withS2 = s2Day(p.s2).reduceRegions({collection: boat, reducer: ee.Reducer.mean(), scale: CONFIG.s2Scale});
  var modis = modisDay(p.ymd, 'MODIS/061/MOD09GQ', 'terra')
    .addBands(modisDay(p.ymd, 'MODIS/061/MYD09GQ', 'aqua'));
  return modis.reduceRegions({collection: withS2, reducer: ee.Reducer.mean(), scale: CONFIG.modisScale})
    .map(function (f) { return f.set('s2_date', p.s2, 's2_days_off', p.daysOff); });
})).flatten();

Export.table.toDrive({
  collection: matched,
  description: CONFIG.fileName,
  folder: CONFIG.driveFolder,
  fileFormat: 'CSV',
  selectors: ['ymd', 'date', 'time_utc', 'lat', 'lon', 'n', 'phycocyanin_rfu', 'chlorophyll_rfu', 'turbidity_fnu',
              'temp_c', 'bluegreen_fp_ugl', 'greenalgae_fp_ugl', 'diatoms_fp_ugl',
              's2_date', 's2_days_off', 's2_clear_score', 's2_ndci', 's2_chl', 's2_fai',
              's2_blue', 's2_green', 's2_red', 's2_rededge1', 's2_rededge2', 's2_nir', 's2_swir',
              'terra_red', 'terra_nir', 'terra_nir_minus_red', 'aqua_red', 'aqua_nir', 'aqua_nir_minus_red']
});

// ---- Map: one pair, to look at before trusting the numbers -----------------
var show = CONFIG.pairs[CONFIG.showOnMap];
var img = s2Day(show.s2);
Map.centerObject(points, 11);
Map.addLayer(img, {bands: ['s2_red', 's2_green', 's2_blue'], min: 0, max: 0.18}, 'Sentinel-2 true color ' + show.s2);
Map.addLayer(img.select('s2_chl'), {min: 0, max: 60, palette: ['08306b', '2171b5', '4eb3d3', '7fcdbb', 'c7e9b4', 'fee08b', 'fc8d59', 'd73027']},
  'Chlorophyll-a ' + show.s2, false);
Map.addLayer(points.filter(ee.Filter.eq('ymd', show.ymd)).style({color: 'ffd400', pointSize: 2, width: 0}), {}, 'Boat cells ' + show.ymd);
print('Open the Tasks tab and click RUN on ' + CONFIG.fileName + '. The map shows the pair for boat date ' + show.ymd + '.');
