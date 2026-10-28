/**
 * Lake Winnebago blooms: daily scenes, east vs. west shore, and wind
 * -------------------------------------------------------------------
 * A companion to the Lake Chlorophyll-a Monitor (github.com/RisaRezaei/gee-lake-chlorophyll,
 * MIT, Parisa Abbasalizadehrezaei). That script gives monthly medians; blooms on Lake Winnebago
 * come and go in days and pile up wherever the wind pushes them, so this one works day by day.
 *
 *   Part A  Every clear Sentinel-2 day (2017 on): lake chlorophyll-a (NDCI), the east and west
 *           nearshore strips, and the ERA5-Land wind of that day and the two days before.
 *   Part B  Animated filmstrips of one summer: true color and chlorophyll-a.
 *   Part C  "Augusts at the cottage": the clearest late-July/August Landsat scene of each year
 *           back to 1984, as a true-color filmstrip.
 *
 * Chl-a uses the Mishra & Mishra (2012) NDCI polynomial, same as the monitor. Treat it as a
 * bloom-intensity index until it is checked against the DNR's sampled chlorophyll.
 *
 * Adapted for Lake Winnebago by James Krauska. License: MIT.
 */

// =============================== CONFIG ===================================
var CONFIG = {
  start: '2017-04-01',            // Sentinel-2 surface reflectance is complete from 2017
  end: '2026-10-01',
  months: [6, 9],                 // June to September, inclusive

  minCloudScore: 0.65,            // Cloud Score+ cs_cdf (higher = stricter)
  minWaterOccurrence: 80,         // JRC water occurrence (%) for the open-water mask
  minClearFraction: 0.5,          // keep days when at least half the lake is cloud-free
  coeffs: [14.039, 86.115, 194.325],
  scale: 60,                      // metres for the statistics (60 keeps 400+ days fast)

  shoreKm: 2,                     // width of the nearshore strips
  splitLon: -88.415,              // east/west split, roughly the middle of the lake
  stripLats: [43.80, 44.15],      // Taycheedah to below Neenah; leaves out the Neenah end

  galleryYear: 2025,              // Part B
  galleryMonths: [7, 8],
  cottageYears: [1999, 2026],     // Part C: the cottage years (Pipe, then Taycheedah)

  driveFolder: 'earthengine',
  filePrefix: 'winnebago'
};
// ==========================================================================

// Lake Winnebago shoreline (Census TIGER areal hydrography, simplified to 250 m).
var lake = ee.Geometry.Polygon([[
  [-88.4710, 43.8144], [-88.4663, 43.8162], [-88.4589, 43.8704], [-88.4638, 43.8779], [-88.4615, 43.8886],
  [-88.4681, 43.8908], [-88.4647, 43.9021], [-88.4697, 43.9027], [-88.4692, 43.9083], [-88.4736, 43.9099],
  [-88.4677, 43.9195], [-88.4751, 43.9217], [-88.4708, 43.9288], [-88.4738, 43.9273], [-88.4771, 43.9225],
  [-88.4777, 43.9221], [-88.4742, 43.9275], [-88.4807, 43.9255], [-88.4730, 43.9339], [-88.4787, 43.9341],
  [-88.4780, 43.9445], [-88.4915, 43.9481], [-88.4912, 43.9407], [-88.4918, 43.9367], [-88.4921, 43.9364],
  [-88.4931, 43.9361], [-88.4977, 43.9487], [-88.5019, 43.9460], [-88.5078, 43.9488], [-88.5265, 43.9725],
  [-88.5277, 43.9893], [-88.5357, 43.9909], [-88.5335, 44.0121], [-88.5194, 44.0072], [-88.5146, 44.0230],
  [-88.5204, 44.0249], [-88.5206, 44.0322], [-88.5094, 44.0359], [-88.5124, 44.0411], [-88.5073, 44.0444],
  [-88.5098, 44.0480], [-88.5158, 44.0401], [-88.5162, 44.0444], [-88.5244, 44.0435], [-88.5275, 44.0467],
  [-88.5234, 44.0508], [-88.5273, 44.0511], [-88.5232, 44.0510], [-88.5238, 44.0475], [-88.5195, 44.0484],
  [-88.5227, 44.0503], [-88.5170, 44.0577], [-88.5238, 44.0536], [-88.5222, 44.0589], [-88.5279, 44.0578],
  [-88.5273, 44.0655], [-88.5234, 44.0665], [-88.5267, 44.0660], [-88.5274, 44.0662], [-88.5280, 44.0665],
  [-88.5235, 44.0672], [-88.5177, 44.0663], [-88.5143, 44.0626], [-88.5092, 44.0648], [-88.5136, 44.0739],
  [-88.5093, 44.0869], [-88.4993, 44.0914], [-88.4835, 44.0920], [-88.4867, 44.0969], [-88.4775, 44.1021],
  [-88.4854, 44.1030], [-88.4832, 44.1106], [-88.4704, 44.1152], [-88.4629, 44.1257], [-88.4691, 44.1329],
  [-88.4581, 44.1475], [-88.4402, 44.1553], [-88.4369, 44.1607], [-88.4342, 44.1694], [-88.4446, 44.1686],
  [-88.4385, 44.1694], [-88.4438, 44.1743], [-88.4381, 44.1867], [-88.4045, 44.1862], [-88.4045, 44.2010],
  [-88.4143, 44.2010], [-88.4143, 44.2069], [-88.3789, 44.2089], [-88.3231, 44.1900], [-88.3004, 44.1743],
  [-88.2976, 44.1656], [-88.2950, 44.1676], [-88.2940, 44.1673], [-88.2974, 44.1652], [-88.2944, 44.1606],
  [-88.3199, 44.1248], [-88.3282, 44.1009], [-88.3251, 44.0868], [-88.3303, 44.0694], [-88.3212, 44.0351],
  [-88.3277, 43.9833], [-88.3195, 43.9677], [-88.3153, 43.9335], [-88.3199, 43.9241], [-88.3329, 43.9159],
  [-88.3432, 43.9019], [-88.3747, 43.8528], [-88.3877, 43.8413], [-88.3890, 43.8185], [-88.3924, 43.8118],
  [-88.4025, 43.8064], [-88.4024, 43.8058], [-88.4008, 43.8054], [-88.3990, 43.8036], [-88.4212, 43.8043],
  [-88.4244, 43.8004], [-88.4174, 43.8000], [-88.4367, 43.7979], [-88.4352, 43.7955], [-88.4389, 43.7948],
  [-88.4378, 43.7980], [-88.4687, 43.8073], [-88.4564, 43.7990], [-88.4610, 43.7959], [-88.4650, 43.7991],
  [-88.4618, 43.8004], [-88.4678, 43.8013], [-88.4710, 43.8144]
]]);

var water = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('occurrence')
  .gte(CONFIG.minWaterOccurrence).selfMask().clip(lake);

// Nearshore strips: the outer CONFIG.shoreKm of the lake, split into east and west halves.
var inner = lake.buffer(-CONFIG.shoreKm * 1000, 50);
var strip = lake.difference(inner, 50)
  .intersection(ee.Geometry.Rectangle([-88.70, CONFIG.stripLats[0], -88.10, CONFIG.stripLats[1]]), 50);
var west = strip.intersection(ee.Geometry.Rectangle([-88.70, 43.70, CONFIG.splitLon, 44.30]), 50);
var east = strip.intersection(ee.Geometry.Rectangle([CONFIG.splitLon, 43.70, -88.10, 44.30]), 50);

var nWater = ee.Number(water.reduceRegion({
  reducer: ee.Reducer.count(), geometry: lake, scale: CONFIG.scale, maxPixels: 1e10
}).get('occurrence'));

// ---- Sentinel-2 daily mosaics with Cloud Score+ --------------------------
var csPlus = ee.ImageCollection('GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED');
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(lake).filterDate(CONFIG.start, CONFIG.end)
  .filter(ee.Filter.calendarRange(CONFIG.months[0], CONFIG.months[1], 'month'))
  .linkCollection(csPlus, ['cs_cdf']);

// The lake crosses Sentinel-2 tiles, so tiles from the same day are mosaicked first.
var days = s2.aggregate_array('system:time_start')
  .map(function (t) { return ee.Date(t).format('YYYY-MM-dd'); }).distinct();
var daily = ee.ImageCollection(days.map(function (d) {
  var d0 = ee.Date.parse('YYYY-MM-dd', d);
  return s2.filterDate(d0, d0.advance(1, 'day')).mosaic()
    .set('system:time_start', d0.millis(), 'date', d);
}));

function chlorophyll(img) {
  var clear = img.select('cs_cdf').gte(CONFIG.minCloudScore).and(img.select('SCL').neq(11));
  var ndci = img.normalizedDifference(['B5', 'B4']).rename('NDCI');
  var c = CONFIG.coeffs;
  return ndci.expression('c0 + c1 * x + c2 * x * x', {x: ndci, c0: c[0], c1: c[1], c2: c[2]})
    .max(0).rename('CHL').updateMask(clear).updateMask(water);
}

// ---- Wind: ERA5-Land daily means around the lake -------------------------
// u > 0 means the wind blows toward the east (a west wind), which piles surface scum on the
// east shore; u < 0 piles it on the west shore. ERA5-Land is a land product, so the lake is
// averaged with a 10 km ring of shore around it.
var era = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR')
  .select(['u_component_of_wind_10m', 'v_component_of_wind_10m']);
var windArea = lake.buffer(10000, 500);

// ---- Part A: one row per day ----------------------------------------------
var stats = ee.FeatureCollection(daily.map(function (img) {
  var chl = chlorophyll(img);
  var lakeStats = chl.reduceRegion({
    reducer: ee.Reducer.median().combine(ee.Reducer.percentile([90]), null, true)
      .combine(ee.Reducer.count(), null, true),
    geometry: lake, scale: CONFIG.scale, maxPixels: 1e10, tileScale: 4
  });
  var med = function (g) {
    return chl.reduceRegion({reducer: ee.Reducer.median(), geometry: g,
      scale: CONFIG.scale, maxPixels: 1e10, tileScale: 4}).get('CHL');
  };
  var d0 = ee.Date(img.get('system:time_start'));
  var w = era.filterDate(d0.advance(-2, 'day'), d0.advance(1, 'day')).mean()
    .reduceRegion({reducer: ee.Reducer.mean(), geometry: windArea, scale: 11132});
  return ee.Feature(null, {
    date: img.get('date'), t: d0.millis(),
    clear_frac: ee.Number(lakeStats.get('CHL_count')).divide(nWater),
    chl_median: lakeStats.get('CHL_median'), chl_p90: lakeStats.get('CHL_p90'),
    chl_west: med(west), chl_east: med(east),
    wind_u: w.get('u_component_of_wind_10m'), wind_v: w.get('v_component_of_wind_10m')
  });
}));

var good = stats.filter(ee.Filter.gte('clear_frac', CONFIG.minClearFraction));
print('Clear days kept', good.size());

print(ui.Chart.feature.byFeature(good, 't', ['chl_median', 'chl_p90'])
  .setChartType('ScatterChart').setOptions({
    title: 'Lake Winnebago chlorophyll-a on clear days (mg/m³, NDCI index)',
    hAxis: {format: 'yyyy'}, vAxis: {title: 'Chl-a'}, pointSize: 2,
    series: {0: {color: '2e7d32'}, 1: {color: 'a5d6a7'}}
  }));

var paired = good.filter(ee.Filter.notNull(['chl_east', 'chl_west', 'wind_u']))
  .map(function (f) {
    return f.set('east_minus_west',
      ee.Number(f.get('chl_east')).subtract(ee.Number(f.get('chl_west'))));
  });
print(ui.Chart.feature.byFeature(paired, 'wind_u', 'east_minus_west')
  .setChartType('ScatterChart').setOptions({
    title: 'Does the wind push the bloom? East minus west shore Chl-a vs. wind',
    hAxis: {title: 'Wind u, m/s (positive = blowing toward the east shore)'},
    vAxis: {title: 'East minus west Chl-a (mg/m³)'},
    pointSize: 3, legend: {position: 'none'},
    trendlines: {0: {color: '8d6e63', lineWidth: 1}}
  }));

Export.table.toDrive({
  collection: stats, description: CONFIG.filePrefix + '_daily',
  folder: CONFIG.driveFolder, fileFormat: 'CSV',
  selectors: ['date', 'clear_frac', 'chl_median', 'chl_p90', 'chl_west', 'chl_east',
              'wind_u', 'wind_v']
});

// ---- Map ------------------------------------------------------------------
var CHL_VIS = {min: 0, max: 60, palette: ['08306b', '2171b5', '4eb3d3', '7fcdbb',
                                           'c7e9b4', 'fee08b', 'fc8d59', 'd73027']};
var RGB_VIS = {bands: ['B4', 'B3', 'B2'], min: 0, max: 1800};
Map.centerObject(lake, 10);
Map.addLayer(ee.Image().paint(west, 1, 2), {palette: ['1e88e5']}, 'West nearshore strip');
Map.addLayer(ee.Image().paint(east, 1, 2), {palette: ['e65100']}, 'East nearshore strip');

// ---- Part B: one summer as filmstrips -------------------------------------
var gy = CONFIG.galleryYear, gm = CONFIG.galleryMonths;
var galleryDates = good
  .filter(ee.Filter.date(ee.Date.fromYMD(gy, gm[0], 1), ee.Date.fromYMD(gy, gm[1], 1).advance(1, 'month')))
  .filter(ee.Filter.gte('clear_frac', 0.8))
  .aggregate_array('date');
var gallery = daily.filter(ee.Filter.inList('date', galleryDates)).sort('system:time_start');
print('Gallery dates (' + gy + ')', galleryDates);

var frameArea = lake.bounds().buffer(1500);
var filmParams = {region: frameArea, dimensions: 480, crs: 'EPSG:3857', framesPerSecond: 1};
var rgbFrames = gallery.map(function (img) { return img.visualize(RGB_VIS); });
var chlFrames = gallery.map(function (img) {
  return img.visualize(RGB_VIS).blend(chlorophyll(img).visualize(CHL_VIS));
});
print('True color, clearest days of ' + gy, ui.Thumbnail({image: rgbFrames, params: filmParams}));
print('Chlorophyll-a over true color', ui.Thumbnail({image: chlFrames, params: filmParams}));
print('Download links (GIF)', rgbFrames.getVideoThumbURL(filmParams),
      chlFrames.getVideoThumbURL(filmParams));

// ---- Part C: Augusts at the cottage (Landsat, 1984 on) ---------------------
// Landsat 7 is left out: its scan-line stripes after 2003 would cross the lake.
var L5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2').select(['SR_B3', 'SR_B2', 'SR_B1'], ['R', 'G', 'B']);
var L89 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').merge(ee.ImageCollection('LANDSAT/LC09/C02/T1_L2'))
  .select(['SR_B4', 'SR_B3', 'SR_B2'], ['R', 'G', 'B']);
var summerLandsat = L5.merge(L89)
  .filter(ee.Filter.contains({leftField: '.geo', rightValue: lake}))
  .filter(ee.Filter.calendarRange(200, 240, 'day_of_year'))   // about July 19 to August 28
  .filter(ee.Filter.lt('CLOUD_COVER', 30));

var years = ee.List.sequence(CONFIG.cottageYears[0], CONFIG.cottageYears[1]);
var augusts = ee.ImageCollection(years.map(function (y) {
  var c = summerLandsat.filter(ee.Filter.calendarRange(y, y, 'year')).sort('CLOUD_COVER');
  return ee.Image(ee.Algorithms.If(c.size().gt(0),
    c.first().set('empty', 0),
    ee.Image.constant([0, 0, 0]).rename(['R', 'G', 'B']).updateMask(0).set('empty', 1)));
})).filter(ee.Filter.eq('empty', 0));

// Collection 2 surface reflectance: reflectance = DN * 0.0000275 - 0.2, so 0 to 0.25 is 7273 to 16364.
var LS_VIS = {bands: ['R', 'G', 'B'], min: 7273, max: 16364, gamma: 1.2};
var augustFrames = augusts.map(function (img) { return img.visualize(LS_VIS); });
print('Landsat scene dates used', augusts.aggregate_array('DATE_ACQUIRED'));
print('Late summers on the lake, ' + CONFIG.cottageYears.join('–'),
      ui.Thumbnail({image: augustFrames, params: filmParams}));
print('Download link (GIF)', augustFrames.getVideoThumbURL(filmParams));
