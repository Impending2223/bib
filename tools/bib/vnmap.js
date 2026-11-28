/* The maps of Indochina (tools/bib/vnmap.py, its STYLE notes) and the map of China (tools/bib/cnmap.py), wherever one
   stands (tools/bib/maps.py): on its own page (indochina.html, china.html), in a calendar page, at the head of a
   thread's page. The same script for all, told apart by data alone: the figure's (`map`, `mode`, `home`; `eu`, the
   entries' files, one a year; `sp`, the span the figure opens on; `th`, a thread's entries alone; `all`, the whole
   span, where the figure has year buttons) and the manifest's (`opt`: the countries whose units are shown, the dots'
   scale, the cities' circles' scale, a unit's line, the counties). Loaded as a module. MapLibre GL JS draws the map (vendored, loaded when a map
   nears the screen); this file builds the style from the manifest the build writes, wires the controls the build
   writes into the figure, reads the span's two fields, and lists the entries. No projection, gesture or label
   placement of its own: the library's. */
const LIB = /*LIB*/{};                   // the vendored files, relative to this script (vnmap.py fills it in)
const HERE = new URL('.', import.meta.url);
const MONTHS = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'];
const MAX_LIVE = 4;                      // WebGL contexts kept at once on a page (the series reader holds a map a part)

/* The span's fields (maps.py, STYLE 2). A field reads a plain ISO date ("1961-04-15") or the calendar's own form
   ("Apr. 15, 1961"; the month in full or cut to three letters or more, with or without its point or the comma; the
   day first too, "15 Apr. 1961"). A month ("1961-04", "Apr. 1961") or a year ("1961") reads as its first day in the
   first field and its last in the second. All figures ("4/15/1961") cannot be told apart and do not read; nor does a
   day the month lacks. What does not read changes nothing. */
const FULLM = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
const pad = (n) => String(n).padStart(2, '0');
const monthOf = (w) => { w = w.toLowerCase(); return w.length < 3 ? 0 : FULLM.findIndex((f) => f.startsWith(w)) + 1; };
export function readDate(text, end) {
  const s = String(text).trim();
  let y, m, d, x;
  if ((x = /^(\d{4})(?:-(\d{1,2})(?:-(\d{1,2}))?)?$/.exec(s))) { y = +x[1]; m = x[2] && +x[2]; d = x[3] && +x[3]; }
  else if ((x = /^([A-Za-z]+)\.?\s+(?:(\d{1,2})(?:\s*,\s*|\s+))?(\d{4})$/.exec(s))) { m = monthOf(x[1]); d = x[2] && +x[2]; y = +x[3]; }
  else if ((x = /^(\d{1,2})\s+([A-Za-z]+)\.?(?:\s*,\s*|\s+)(\d{4})$/.exec(s))) { d = +x[1]; m = monthOf(x[2]); y = +x[3]; }
  else return null;
  if (m === undefined) m = end ? 12 : 1;
  if (m < 1 || m > 12) return null;
  const last = new Date(Date.UTC(y, m, 0)).getUTCDate();
  if (d === undefined) d = end ? last : 1;
  if (d < 1 || d > last) return null;
  return y + '-' + pad(m) + '-' + pad(d);
}
export const showDate = (iso) => MONTHS[+iso.slice(5, 7) - 1] + ' ' + +iso.slice(8) + ', ' + iso.slice(0, 4);
/* a span as the calendar writes one: "Apr. 1–June 30, 1961"; "Aug. 1–31, 1966"; "Jan. 6, 1960–Aug. 31, 1976" */
export const showSpan = (a, b) => (a === b ? showDate(a) : a.slice(0, 7) === b.slice(0, 7) ? showDate(a).slice(0, -6) + '–' + +b.slice(8) + ', ' + b.slice(0, 4) :
  (a.slice(0, 4) === b.slice(0, 4) ? showDate(a).slice(0, -6) : showDate(a)) + '–' + showDate(b));

/* The pin (vnmap.py, STYLE 9): what it reads at a point. A point is [lon, lat]; a distance in km, on the sphere
   between two points, and on a plane laid at the pin for a line within a few tens of km (the error is far under the
   lines' own). Polygons and lines are the layers' own GeoJSON; nothing is drawn by this code. */
const RKM = 6371.0088;
const RAD = Math.PI / 180;
export const showLL = ([lon, lat]) => Math.abs(lat).toFixed(3) + '° ' + (lat < 0 ? 'S' : 'N') + ', ' +
  Math.abs(lon).toFixed(3) + '° ' + (lon < 0 ? 'W' : 'E');
export const showKm = (d) => (d < 10 ? d.toFixed(1) : Math.round(d).toLocaleString('en-US')) + ' km';
export function km(a, b) {
  const s = Math.sin((b[1] - a[1]) * RAD / 2) ** 2 + Math.cos(a[1] * RAD) * Math.cos(b[1] * RAD) * Math.sin((b[0] - a[0]) * RAD / 2) ** 2;
  return 2 * RKM * Math.asin(Math.min(1, Math.sqrt(s)));
}
const BB = new WeakMap();
function bbox(g) {                        // a geometry's [w, s, e, n], kept
  let b = BB.get(g);
  if (b) return b;
  b = [Infinity, Infinity, -Infinity, -Infinity];
  const walk = (c) => {
    if (typeof c[0] === 'number') { b[0] = Math.min(b[0], c[0]); b[1] = Math.min(b[1], c[1]); b[2] = Math.max(b[2], c[0]); b[3] = Math.max(b[3], c[1]); }
    else c.forEach(walk);
  };
  walk(g.coordinates || []);
  BB.set(g, b);
  return b;
}
function inRing([x, y], r) {
  let inside = false;
  for (let i = 0, j = r.length - 1; i < r.length; j = i++) {
    const [xi, yi] = r[i], [xj, yj] = r[j];
    if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}
export function inside(p, g) {            // a point in a Polygon or MultiPolygon, its holes out
  if (!g || !/Polygon$/.test(g.type)) return false;
  const b = bbox(g);
  if (p[0] < b[0] || p[0] > b[2] || p[1] < b[1] || p[1] > b[3]) return false;
  return (g.type === 'Polygon' ? [g.coordinates] : g.coordinates).some((rs) => inRing(p, rs[0]) && !rs.slice(1).some((h) => inRing(p, h)));
}
export function toLine(p, g) {            // km from a point to a LineString or MultiLineString
  const k = Math.cos(p[1] * RAD);
  let best = Infinity;
  for (const l of g.type === 'LineString' ? [g.coordinates] : g.type === 'MultiLineString' ? g.coordinates : []) {
    for (let i = 0; i < l.length; i++) {
      const ax = (l[i][0] - p[0]) * k, ay = l[i][1] - p[1];
      const [bx, by] = i + 1 < l.length ? [(l[i + 1][0] - p[0]) * k, l[i + 1][1] - p[1]] : [ax, ay];
      const dx = bx - ax, dy = by - ay, L = dx * dx + dy * dy;
      const t = L ? Math.max(0, Math.min(1, -(ax * dx + ay * dy) / L)) : 0;
      best = Math.min(best, (ax + t * dx) ** 2 + (ay + t * dy) ** 2);
    }
  }
  return Math.sqrt(best) * RAD * RKM;
}
export function nearest(p, feats) {       // the nearest point feature and its distance: [feature, km], or [null, Infinity]
  let best = null, d = Infinity;
  for (const f of feats) {
    const x = km(p, f.geometry.coordinates);
    if (x < d) { d = x; best = f; }
  }
  return [best, d];
}
export const within = (p, fc, keep) => ((fc && fc.features) || []).filter((f) => (!keep || keep(f.properties || {})) && inside(p, f.geometry));
/* a county's line (tools/cnmap/base.py): "zh · kind, end of 1964 · province[, prefecture] · how it is drawn[ · a guess]",
   or "zh · a later unit (about 1994), shown as it is: why". The panel keeps its characters, its prefecture, and a
   word on its lines only where they are less sure than the rest: a guess, a city at its later size, a later unit. */
export function countyOf(line) {
  const s = String(line || '').split(' · ');
  if (/^a later unit/.test(s[1] || '')) return {zh: s[0], pref: '', note: 'Name and lines of a later year.'};
  const how = s.slice(3).join(' · ');
  return {zh: s[0], pref: ((s[2] || '').split(', ')[1] || '').trim(),
    note: /a guess/.test(how) ? 'The county here is a guess.' : /^the later city, larger/.test(how) ? "Drawn at the city's later, larger size." : ''};
}
/* twelve months' bars (STYLE 9): each month's figure over its bar, the month's initial under it; the bars from the
   zero line, which stands where the figures cross it (a winter below freezing). The figure as shown (show), the
   month's in full for a pointer's title and a screen reader (full). */
const INITIAL = 'JFMAMJJASOND';
export function bars(v, show, full, label) {
  const lo = Math.min(0, ...v), hi = Math.max(0, ...v), r = hi - lo || 1, z = -lo / r * 100;
  const pc = (x) => +x.toFixed(2) + '%';
  return '<div class="vnm-bars" role="img" style="--z:' + pc(100 - z) + '" aria-label="' + esc(label + ': ' + v.map((x, i) => MONTHS[i] + ' ' + full(x)).join(', ')) + '">' +
    v.map((x, i) => '<span title="' + esc(MONTHS[i] + ' ' + full(x)) + '">' + show(x) + '<i><i style="bottom:' + pc(x < 0 ? z + x / r * 100 : z) +
      ';height:' + pc(Math.abs(x) / r * 100) + '"></i></i><span class="m">' + INITIAL[i] + '</span></span>').join('') + '</div>';
}
const minus = (t) => String(t).replace('-', '−');
/* the rivers' sizes (sources/indochina/README.md, "Rivers"): HydroRIVERS's by mean flow, SWORD's by width */
const FLOW = ['5,000 m³/s and over', '1,000–5,000 m³/s', '300–1,000 m³/s', '100–300 m³/s', '30–100 m³/s', '10–30 m³/s', 'under 10 m³/s'];
const WIDTH = ['900 m wide and over', '400–900 m wide', '200–400 m wide', '100–200 m wide', '50–100 m wide', 'under 50 m wide'];
const RIVER_KM = 20;                      // a river farther from the pin is not named
const files = {};                         // a layer's file read for the pin, once a page, whichever figure asked
const json = (url) => files[url] || (files[url] = fetch(url).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
  .catch((e) => { delete files[url]; throw e; }));
const pmt = {}, tiles = {}, tileKeys = [];   // the elevation's and the climate's files and tiles read for the pin, the last eight tiles

let libP = null;
function lib() {
  if (!libP) {
    libP = (async () => {
      const css = document.createElement('link');
      css.rel = 'stylesheet';
      css.href = new URL(LIB.css, HERE).href;
      document.head.append(css);
      const pm = new Promise((ok, bad) => {
        const s = document.createElement('script');
        s.src = new URL(LIB.pmtiles, HERE).href;
        s.onload = ok;
        s.onerror = bad;
        document.head.append(s);
      });
      const [ml] = await Promise.all([import(new URL(LIB.maplibre, HERE).href), pm]);
      const protocol = new window.pmtiles.Protocol();
      ml.addProtocol('pmtiles', protocol.tile);
      return ml;
    })();
  }
  return libP;
}

const manifests = {};
function manifest(url) {
  return manifests[url] || (manifests[url] = fetch(url).then((r) => r.json()));
}

const esc = (s) => String(s == null ? '' : s).replace(/[&<>"]/g, (c) => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const abs = (p) => new URL(p, location.href).href;
const EMPTY = {type: 'FeatureCollection', features: []};

function colors() {
  const C = {};
  for (const k of ['vz1', 'vz2', 'vz3', 'vz4', 'vz5', 'vr1', 'vr2', 'vr3', 'vr4', 'vr5', 'vr6', 'vr7', 'vr8', 'vpv',
    'vland', 'vsea', 'vop', 'vdot', 'vriv', 'vlake', 'vctr', 'vcity', 'vline', 'bg', 'ink', 'muted', 'rule']) C[k] = css('--' + k);
  C.vop = +C.vop || 0.55;
  return C;
}

/* The style: every layer from the start, the heavy GeoJSON sources empty until their layer is first shown. */
const LAZY = {rivers: 'rivers', lakes: 'lakes', contours: 'contours', bathy: 'bathy', climate: 'climate', pop: 'pop', counties: 'counties'};
const ZC = {I: 'vz1', II: 'vz2', III: 'vz3', IV: 'vz4', CMD: 'vz5'};
const RC = {'North Central Coast': 'vr1', 'South Central Coast': 'vr2', 'Central Highlands': 'vr3', 'Southeast': 'vr4',
  'Mekong Delta': 'vr5', 'Northwest': 'vr6', 'Northeast': 'vr7', 'Red River Delta': 'vr8'};
const FONT = ['Libre Franklin Regular'], BOLD = ['Libre Franklin SemiBold'], ITAL = ['Libre Franklin Italic'];

function match(prop, table, C, other) {
  const m = ['match', ['get', prop]];
  for (const [k, v] of Object.entries(table)) m.push(k, C[v]);
  m.push(other);
  return m;
}

/* The elevation bands as the colour relief's ramp: `color-relief` interpolates, so each band is a flat run between
   two stops a centimetre apart; the sea (-1 m in the tiles) transparent. */
function bands(H) {
  const r = ['interpolate', ['linear'], ['elevation'], -1, 'rgba(0,0,0,0)', -0.01, 'rgba(0,0,0,0)'];
  H.forEach((h, i) => {
    r.push(h.from, h.color);
    r.push(i + 1 < H.length ? H[i + 1].from - 0.01 : 9000, h.color);
  });
  return r;
}

function style(M, C, places) {
  const f = M.files, O = M.opt || {};
  const src = {
    admin: {type: 'geojson', data: abs(f.admin), attribution: M.credit.admin},
    places: {type: 'geojson', data: places},
    cities: {type: 'geojson', data: EMPTY},     // fetched, as the layers below, the first time its box is ticked
  };
  for (const k of Object.keys(LAZY)) if (f[k]) src[k] = {type: 'geojson', data: EMPTY, attribution: M.credit[k]};
  if (f.dem) src.dem = {type: 'raster-dem', url: 'pmtiles://' + abs(f.dem), encoding: 'terrarium', tileSize: 512, attribution: M.credit.dem};
  if (f.koppen) src.koppen = {type: 'raster', url: 'pmtiles://' + abs(f.koppen), tileSize: 256, attribution: M.credit.koppen};
  const hide = {visibility: 'none'};
  const L = [
    {id: 'bg', type: 'background', paint: {'background-color': C.vsea}},
    f.bathy && {id: 'bathy', type: 'fill', source: 'bathy', layout: hide,
      paint: {'fill-color': ['match', ['get', 'd'], ...M.depths.flatMap((d) => [d.from, d.color]), C.vsea]}},
    {id: 'land', type: 'fill', source: 'admin', filter: ['in', ['get', 'k'], ['literal', ['land', 'unit', 'disp']]], paint: {'fill-color': C.vland}},
    f.dem && {id: 'elevation', type: 'color-relief', source: 'dem', layout: hide,
      paint: {'color-relief-color': bands(M.hypso)}},
    f.koppen && {id: 'koppen', type: 'raster', source: 'koppen', layout: hide, paint: {'raster-opacity': 0.8, 'raster-resampling': 'nearest'}},
    f.climate && {id: 'rain', type: 'fill', source: 'climate', layout: hide, paint: {'fill-opacity': 0.85}},
    f.pop && {id: 'pop', type: 'fill', source: 'pop', layout: hide,
      paint: {'fill-color': ['match', ['get', 'c'], ...M.pop.classes.flatMap((c, i) => [i, c.color]), '#ccc'], 'fill-opacity': 0.85}},
    {id: 'tint', type: 'fill', source: 'admin', filter: ['==', ['get', 'k'], 'unit'], paint: {'fill-color': C.vpv, 'fill-opacity': C.vop}},
    // the counties (the map of China): their areas unseen, for the tap; their lines under the units'
    f.counties && {id: 'county', type: 'fill', source: 'counties', layout: hide, filter: ['==', ['get', 'k'], 'county'],
      paint: {'fill-color': C.vpv, 'fill-opacity': 0}},
    f.dem && {id: 'relief', type: 'hillshade', source: 'dem', layout: hide,
      paint: {'hillshade-method': 'multidirectional', 'hillshade-exaggeration': 0.45,
        'hillshade-shadow-color': 'rgba(40,40,40,0.55)', 'hillshade-highlight-color': 'rgba(255,255,255,0.35)'}},
    f.contours && {id: 'contours', type: 'line', source: 'contours', layout: hide,
      paint: {'line-color': C.vctr, 'line-opacity': 0.7, 'line-width': ['case', ['>=', ['get', 'elev_m'], 1500], 0.9, 0.6],
        'line-dasharray': ['case', ['==', ['get', 'elev_m'], 500], ['literal', [3, 2]], ['literal', [1, 0]]]}},
    f.lakes && {id: 'lakes', type: 'fill', source: 'lakes', layout: hide, filter: ['>=', ['get', 'area_km2'], 3], paint: {'fill-color': C.vlake}},
    f.rivers && {id: 'rivers', type: 'line', source: 'rivers', layout: {visibility: 'none', 'line-cap': 'round', 'line-join': 'round'},
      paint: {'line-color': C.vriv, 'line-width': ['interpolate', ['linear'], ['zoom'], 5,
        ['match', ['get', 'size'], 1, 1.6, 2, 1.2, 3, 0.9, 4, 0.7, 5, 0.5, 0.35], 10,
        ['match', ['get', 'size'], 1, 5, 2, 3.5, 3, 2.5, 4, 1.8, 5, 1.3, 1]]}},
    f.counties && {id: 'l-county', type: 'line', source: 'counties', layout: hide,
      filter: ['all', ['==', ['get', 'k'], 'line'], ['==', ['get', 'l'], 'county']],
      paint: {'line-color': C.vline, 'line-width': 0.4, 'line-opacity': 0.9}},
    {id: 'l-unit', type: 'line', source: 'admin', filter: ['all', ['==', ['get', 'k'], 'line'], ['==', ['get', 'l'], 'unit']],
      paint: {'line-color': C.vline, 'line-width': 0.6, 'line-opacity': 0.9}},
    {id: 'l-region', type: 'line', source: 'admin', filter: ['all', ['==', ['get', 'k'], 'line'], ['==', ['get', 'l'], 'region']], layout: hide,
      paint: {'line-color': C.ink, 'line-width': 1.3, 'line-opacity': 0.7}},
    {id: 'l-ctz', type: 'line', source: 'admin', filter: ['all', ['==', ['get', 'k'], 'line'], ['==', ['get', 'l'], 'ctz']],
      paint: {'line-color': C.ink, 'line-width': 1.3, 'line-opacity': 0.7}},
    {id: 'l-coast', type: 'line', source: 'admin', filter: ['all', ['==', ['get', 'k'], 'line'], ['==', ['get', 'l'], 'coast']],
      paint: {'line-color': C.muted, 'line-width': 0.5, 'line-opacity': 0.6}},
    {id: 'l-intl', type: 'line', source: 'admin', filter: ['all', ['==', ['get', 'k'], 'line'], ['==', ['get', 'l'], 'intl']],
      layout: {'line-join': 'round'}, paint: {'line-color': C.ink, 'line-width': 1.2}},
    {id: 'l-dmz', type: 'line', source: 'admin', filter: ['all', ['==', ['get', 'k'], 'line'], ['in', ['get', 'l'], ['literal', ['dmz', 'disp']]]],
      layout: {'line-join': 'round'}, paint: {'line-color': C.ink, 'line-width': 1.2, 'line-dasharray': [3, 1.5]}},
    {id: 'cities', type: 'circle', source: 'cities', layout: hide,
      paint: {'circle-radius': ['*', O.city || 0.0105, ['sqrt', ['get', 'pop']]], 'circle-color': C.vcity, 'circle-opacity': 0.35,
        'circle-stroke-color': C.vcity, 'circle-stroke-width': 1}},
    {id: 'dots-dim', type: 'circle', source: 'places', filter: ['==', ['get', 'n'], 0],
      paint: {'circle-radius': 2.4, 'circle-color': C.muted, 'circle-opacity': 0.7}},
    {id: 'dots', type: 'circle', source: 'places', filter: ['>', ['get', 'n'], 0],
      layout: {'circle-sort-key': ['-', 0, ['get', 'n']]},
      paint: {'circle-radius': ['max', 3.2, ['*', O.dot || 2.6, ['sqrt', ['get', 'n']]]], 'circle-color': C.vdot,
        'circle-stroke-color': C.bg, 'circle-stroke-width': 1}},
    // the names: the year's places above all, then the gazetteer's by rank as the zoom allows (STYLE 3)
    {id: 'lab-unit', type: 'symbol', source: 'admin', filter: ['all', ['==', ['get', 'k'], 'lab'], ['==', ['get', 'l'], 'unit']],
      layout: {visibility: 'none', 'text-field': ['get', 'name'], 'text-font': FONT, 'text-size': 11, 'text-max-width': 7,
        'symbol-sort-key': ['-', 0, ['get', 'km2']], 'text-padding': 3},
      paint: {'text-color': C.muted, 'text-halo-color': C.vland, 'text-halo-width': 1.2}},
    f.counties && {id: 'lab-county', type: 'symbol', source: 'counties', filter: ['all', ['==', ['get', 'k'], 'lab'], ['==', ['get', 'l'], 'county']],
      layout: {visibility: 'none', 'text-field': ['get', 'name'], 'text-font': FONT, 'text-size': 11, 'text-max-width': 7,
        'symbol-sort-key': ['-', 0, ['get', 'km2']], 'text-padding': 3},
      paint: {'text-color': C.muted, 'text-halo-color': C.vland, 'text-halo-width': 1.2}},
    {id: 'lab-group', type: 'symbol', source: 'admin', filter: ['all', ['==', ['get', 'k'], 'lab'], ['==', ['get', 'l'], 'ctz']],
      layout: {visibility: 'none', 'text-field': ['get', 'name'], 'text-font': BOLD, 'text-size': 12.5, 'text-max-width': 8,
        'text-transform': 'uppercase', 'text-letter-spacing': 0.08},
      paint: {'text-color': C.ink, 'text-opacity': 0.75, 'text-halo-color': C.vland, 'text-halo-width': 1.4}},
    f.rivers && {id: 'lab-river', type: 'symbol', source: 'rivers', filter: ['any', ['has', 'name_vi'], ['has', 'name']],
      layout: {visibility: 'none', 'symbol-placement': 'line', 'text-field': ['coalesce', ['get', 'name_vi'], ['get', 'name']],
        'text-font': ITAL, 'text-size': 11,
        'symbol-spacing': 400},
      paint: {'text-color': C.vriv, 'text-halo-color': C.vland, 'text-halo-width': 1.2}},
  ];
  const country = {id: 'lab-country', type: 'symbol', source: 'admin', filter: ['all', ['==', ['get', 'k'], 'lab'], ['==', ['get', 'l'], 'country']],
      layout: {'text-field': ['get', 'name'], 'text-font': ITAL, 'text-size': 14, 'text-max-width': 8, 'text-letter-spacing': 0.04,
        'symbol-sort-key': ['-', 0, ['get', 'km2']], 'text-variable-anchor': ['center', 'top', 'bottom', 'left', 'right'],
        'text-radial-offset': 1.2},
      paint: {'text-color': C.muted, 'text-halo-color': C.vland, 'text-halo-width': 1.5}};
  L.push(
    {id: 'cities-lab', type: 'symbol', source: 'cities', layout: {visibility: 'none', 'text-field': ['get', 'label'], 'text-font': FONT,
      'text-size': 11, 'text-variable-anchor': ['top', 'bottom', 'left', 'right'], 'text-radial-offset': 0.9,
      'symbol-sort-key': ['-', 0, ['get', 'pop']]},
      paint: {'text-color': C.ink, 'text-halo-color': C.vland, 'text-halo-width': 1.5}});
  for (const r of [3, 2, 1, 0]) {        // 0: a place with this year's entries; 1-3: the gazetteer's ranks
    L.push({id: 'names-' + r, type: 'symbol', source: 'places',
      filter: r ? ['all', ['==', ['get', 'n'], 0], ['==', ['get', 'r'], r]] : ['>', ['get', 'n'], 0],
      layout: {'text-field': ['get', 'name'], 'text-font': r ? FONT : BOLD, 'text-size': r ? 11 : 12,
        'text-variable-anchor': ['left', 'right', 'top', 'bottom'], 'text-radial-offset': r ? 0.55 : 0.75,
        'text-justify': 'auto', 'symbol-sort-key': r ? ['get', 'r'] : ['-', 0, ['get', 'n']], 'text-padding': 2},
      paint: {'text-color': r ? C.muted : C.ink, 'text-halo-color': C.vland, 'text-halo-width': 1.5}});
  }
  L.push(country);                         // the countries' names first: the places' names find room around them
  const fonts = Object.fromEntries(Object.entries(M.fonts).map(([k, v]) => [k, v.map((x) => ({...x, url: abs(x.url)}))]));
  return {version: 8, 'font-faces': fonts, sources: src, layers: L.filter(Boolean)};
}

/* One figure: the map, its controls, the tap's list, the folded list. */
class Figure {
  constructor(fig) {
    this.fig = fig;
    this.D = JSON.parse(fig.querySelector('.vnm-d').textContent);
    this.D.ys = this.D.ys || [];
    this.D.eu = this.D.eu || {};
    this.Y = {};                          // the entries' files read: year -> {k: the threads, e: the entries}
    this.E = [];                          // the entries in the span
    this.at = {};
    this.atv = {};
    this.box = fig.querySelector('.vnm-box');
    this.pop = fig.querySelector('.vnm-pop');
    this.pinEl = fig.querySelector('.vnm-pin');   // the pin's panel (STYLE 9)
    this.pin = null;
    this.key = 'vnm2' + (this.D.map ? '-' + this.D.map : '');   // each map its own choices
    const mode0 = this.D.mode || 'ctz';
    this.st = {mode: mode0, lay: {}, month: 7, popyear: 1960, from: this.D.sp[0], to: this.D.sp[1]};
    try {
      const s = JSON.parse(sessionStorage.getItem(this.key) || '{}');
      Object.assign(this.st, {mode: s.mode || mode0, lay: s.lay || {}, month: s.month || 7, popyear: s.popyear || 1960});
    } catch (e) { /* storage refused: the defaults */ }
    this.controls();
    const y = this.D.all && this.hashYear();
    if (y) this.setSpan(...this.yearSpan(y));
    else this.setSpan(this.st.from, this.st.to);
  }

  /* the year buttons (the map's own page): a year's span, "All years" the whole; the year an address names */
  yearSpan(y) { return y === 'all' ? this.D.all : [y + '-01-01', y + '-12-31']; }
  hashYear() {
    const m = /^#y(\d{4}|all)$/.exec(location.hash);
    return m && (m[1] === 'all' || this.D.ys.includes(m[1])) ? m[1] : null;
  }
  yearNow() {                             // the button the span is, or null
    if (!this.D.all) return null;
    const {from, to} = this.st;
    if (from === this.D.all[0] && to === this.D.all[1]) return 'all';
    const y = from.slice(0, 4);
    return from === y + '-01-01' && to === y + '-12-31' && this.D.ys.includes(y) ? y : null;
  }

  save() {
    try {
      sessionStorage.setItem(this.key, JSON.stringify({mode: this.st.mode, lay: this.st.lay, month: this.st.month, popyear: this.st.popyear}));
    } catch (e) { /* storage refused */ }
  }

  lakeYear() { return +this.st.to.slice(0, 4); }

  /* the controls the build wrote: the year links, the span's fields, the map's kind, the layers */
  controls() {
    const fig = this.fig;
    fig.querySelectorAll('.vnm-bar [data-mode]').forEach((b) => b.addEventListener('click', () => {
      this.st.mode = b.dataset.mode;
      this.save();
      this.apply();
    }));
    fig.querySelectorAll('.vnm-bar input[data-l]').forEach((i) => {
      i.checked = !!this.st.lay[i.dataset.l];
      i.addEventListener('change', () => {
        this.st.lay[i.dataset.l] = i.checked;
        this.save();
        this.apply();
      });
    });
    const month = fig.querySelector('.vnm-bar select[data-m]');
    if (month) {
      month.value = String(this.st.month);
      month.addEventListener('change', () => { this.st.month = +month.value; this.save(); this.apply(); });
    }
    const py = fig.querySelector('.vnm-bar select[data-py]');
    if (py) {
      py.value = String(this.st.popyear);
      py.addEventListener('change', () => { this.st.popyear = +py.value; this.save(); this.apply(); });
    }
    const yrs = fig.querySelector('.vnm-yrs');
    if (yrs) {
      yrs.addEventListener('click', (ev) => {
        const a = ev.target.closest('a[data-yr]');
        if (!a) return;
        ev.preventDefault();
        try { history.replaceState(null, '', '#y' + a.dataset.yr); } catch (e) { /* a sandboxed frame */ }
        this.setSpan(...this.yearSpan(a.dataset.yr));
      });
      addEventListener('hashchange', () => { const y = this.hashYear(); if (y) this.setSpan(...this.yearSpan(y)); });
    }
    // the span's two fields: each keystroke read, and taken once both read; on leaving a field, its date written out
    this.sp = [fig.querySelector('input[data-sp="from"]'), fig.querySelector('input[data-sp="to"]')];
    this.sp.forEach((el, i) => {
      if (!el) return;
      el.addEventListener('input', () => {
        const a = readDate(this.sp[0].value, false), b = readDate(this.sp[1].value, true);
        if (a && b) this.setSpan(a, b, el);
      });
      el.addEventListener('change', () => { const d = readDate(el.value, !!i); if (d) el.value = showDate(d); });
      el.addEventListener('keydown', (ev) => { if (ev.key === 'Enter') el.blur(); });
    });
    this.pop.addEventListener('click', (e) => { if (e.target.closest('.x')) this.pop.hidden = true; });
    if (this.pinEl) this.pinEl.addEventListener('click', (e) => { if (e.target.closest('.x')) this.setPin(null); });
    fig.querySelector('.vnm-list').addEventListener('toggle', () => this.fillList());
  }

  /* the span: the fields, the year buttons; then, once the map is near the screen, the entries (STYLE 2, 6) */
  setSpan(from, to, typed) {
    Object.assign(this.st, {from, to});
    this.sp.forEach((el, i) => { if (el && el !== typed) el.value = showDate(i ? to : from); });
    const y = this.yearNow(), yrs = this.fig.querySelector('.vnm-yrs');
    if (yrs) yrs.querySelectorAll('a').forEach((a) => a.toggleAttribute('aria-current', a.dataset.yr === y));
    this.pop.hidden = true;
    if (!this.awake) return;              // before the map nears the screen: the build's own count stays
    const turn = this.turn = (this.turn || 0) + 1;
    this.data().then(() => {
      if (turn !== this.turn) return;     // a later span has been asked for
      this.refresh();
      if (this.map) { this.places(); this.apply(); }
    });
  }

  /* the years the span touches, of those the figure has entries for; their files, each read once */
  years() { return this.D.ys.filter((y) => this.D.eu[y] && y + '-12-31' >= this.st.from && y + '-01-01' <= this.st.to); }
  data() {
    return Promise.all(this.years().map((y) => this.Y[y] || (this.Y[y] = fetch(this.D.eu[y]).then((r) => r.json())
      .then((d) => (this.Y[y] = d), () => { delete this.Y[y]; }))));
  }

  /* the entries in the span (a thread's alone, where the figure is a thread's; a place's, where a place's): the dots, the lists, the count */
  refresh() {
    const {from, to} = this.st, th = this.D.th, E = [], at = {}, atv = {};
    const ids = this.D.ids ? new Set(this.D.ids) : null;     // a place's page: its own entries alone (placepages.py)
    for (const y of this.years()) {
      const Y = this.Y[y];
      if (!Y || !Y.e) continue;
      const k = th ? Y.k.indexOf(th) : -1;
      if (th && k < 0) continue;
      for (const x of Y.e) {
        if (x.d < from || x.d > to || (th && !x.k.includes(k))) continue;
        if (ids && !ids.has(x.h.slice(x.h.indexOf('#') + 1))) continue;
        E.push(x);
        x.p.forEach((p) => (at[p] = at[p] || []).push(x));
        (x.v || []).forEach((v) => (atv[v] = atv[v] || []).push(x));
      }
    }
    this.E = E;
    this.at = at;
    this.atv = atv;                       // the entries placed in a unit as a whole
    this.listed = false;
    this.fillList();
    this.fig.querySelector('.vnm-list summary').textContent = 'The placed entries (' + E.length + ')';
    const cnt = this.fig.querySelector('.vnm-cnt');
    if (cnt) {
      const np = new Set(E.flatMap((x) => x.p)).size, y = this.yearNow();
      cnt.textContent = (y === 'all' ? 'All years' : y || showSpan(from, to)) + ': ' + E.length + ' placed ' +
        (E.length === 1 ? 'entry' : 'entries') + ', at ' + np + (np === 1 ? ' place.' : ' places.');
    }
    if (this.pin) this.pinShow();          // the panel's counts are the span's
  }

  /* an entry's date, with its year where the span holds more than one; its link, on the page where the page holds it */
  when(x) {
    const y = x.d.slice(0, 4);
    return esc(x.w) + (this.st.from.slice(0, 4) !== this.st.to.slice(0, 4) && !String(x.w).includes(y) ? ', ' + y : '');   // "1960", not "1960, 1960"
  }
  href(x) {
    if (this.D.here == null) return x.h;
    const id = x.h.slice(x.h.indexOf('#') + 1);
    return document.getElementById(this.D.here + id) ? '#' + this.D.here + id : x.h;
  }
  name(k) { const f = this.M && this.M.byId[k]; return f ? f.properties.name : k; }

  /* the folded list: written at once where it is short, else when it is opened */
  fillList() {
    const det = this.fig.querySelector('.vnm-list'), E = this.E || [];
    if (this.listed || (E.length > 1500 && !det.open)) { if (!this.listed) det.querySelector('ol').innerHTML = ''; return; }
    det.querySelector('ol').innerHTML = E.map((x) => '<li><a href="' + esc(this.href(x)) + '">' + this.when(x) +
      '</a> <span class="m">' + esc(x.t) + '.</span> ' + esc(x.s) +
      (x.p.length ? ' <span class="m">(' + x.p.map((k) => esc(this.name(k))).join(', ') + ')</span>' : '') + '</li>').join('');
    this.listed = true;
  }

  /* a tap's list of entries */
  rows(hits) {
    return '<ol>' + hits.map((x) => '<li><a href="' + esc(this.href(x)) + '">' + this.when(x) + '</a> <span class="m">' + esc(x.t) + '.</span> ' + esc(x.s) + '</li>').join('') + '</ol>';
  }

  /* the gazetteer's places with the span's count (`n`), for the dots and names */
  placesFC() {
    return {type: 'FeatureCollection', features: this.M.places.features.map((f) => ({
      type: 'Feature', geometry: f.geometry,
      properties: Object.assign({}, f.properties, {n: (this.at[f.properties.id] || []).length})}))};
  }

  places() { if (this.map && this.ready) this.map.getSource('places').setData(this.placesFC()); }

  async start(ml, M) {
    this.M = M;
    this.ml = ml;
    const C = this.C = colors();
    const home = this.homeBounds();
    const map = this.map = new ml.Map({
      container: this.fig.querySelector('.vnm-gl'),
      style: style(M, C, this.placesFC()),
      bounds: home, fitBoundsOptions: {padding: 8},
      maxBounds: M.bounds, renderWorldCopies: false,
      pixelRatio: Math.min(window.devicePixelRatio || 1, 2),   // a phone's 2.6 or 3 drawn at 2: fewer pixels a frame
      cooperativeGestures: true, dragRotate: false, pitchWithRotate: false, touchPitch: false, rollEnabled: false,
      attributionControl: {compact: true, customAttribution: M.credit.page},
      locale: {'CooperativeGesturesHandler.WindowsHelpText': 'Ctrl and the wheel to zoom',
        'CooperativeGesturesHandler.MacHelpText': '⌘ and the wheel to zoom',
        'CooperativeGesturesHandler.MobileHelpText': 'Two fingers to move the map'},
    });
    map.touchZoomRotate.disableRotation();
    map.keyboard.disableRotation();
    map.addControl(new ml.NavigationControl({showCompass: false}), 'top-right');
    map.addControl(new Home(home), 'top-right');
    if (ml.FullscreenControl) map.addControl(new ml.FullscreenControl({container: this.box}), 'top-right');
    this.fig._map = map;
    map.on('load', () => {
      this.ready = true;
      this.places();                      // a span changed while the map was loading
      if (this.view) map.jumpTo(this.view);   // a map given up and drawn again keeps its view
      const z = this.homeZoom = this.view ? this.homeZoom : map.getZoom();
      map.setMaxZoom(z + 6);              // 64 times the first view (STYLE 4)
      map.setMinZoom(Math.max(0, z - 1.5));
      map.setLayerZoomRange('names-2', z + 1.1, 24);   // rank 2 from about twice the first view, rank 3 from six times
      map.setLayerZoomRange('names-3', z + 2.6, 24);
      if (map.getLayer('lab-county')) map.setLayerZoomRange('lab-county', z + 2.6, 24);   // the counties' names with rank 3's
      this.apply();
      const at = this.fig.querySelector('.maplibregl-ctrl-attrib');   // the credits folded to their button
      if (at) { at.classList.remove('maplibregl-compact-show'); at.removeAttribute('open'); }
      map.once('idle', () => { this.fig.dataset.ready = '1'; });
    });
    map.on('click', (e) => this.tap(e));
    // a double tap or a double click zooms: the pin its first tap would drop is not dropped, or is taken back
    const undo = () => {
      clearTimeout(this.tapT);
      if (this.pinT && performance.now() - this.pinT < 600) { this.pinT = 0; this.setPin(this.pinWas || null); }
    };
    map.on('dblclick', undo);
    map.on('zoomstart', (e) => { const t = e.originalEvent && e.originalEvent.type; if (t === 'dblclick' || /^touch/.test(t || '')) undo(); });
    if (this.pin) this.drawPin();         // a map given up and drawn again keeps its pin
    for (const id of ['dots', 'dots-dim', 'cities']) {
      map.on('mouseenter', id, () => { map.getCanvas().style.cursor = 'pointer'; });
      map.on('mouseleave', id, () => { map.getCanvas().style.cursor = ''; });
    }
    const retheme = () => { this.C = colors(); this.paint(); };
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', retheme);
    new MutationObserver(retheme).observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
  }

  homeBounds() {
    if (!this.M.home[this.D.home]) return this.M.home.all;
    const b = this.M.home[this.D.home].slice();   // the first view widened to the span's places
    for (const k of Object.keys(this.at)) {
      const f = this.M.byId[k];
      if (!f) continue;
      const [x, y] = f.geometry.coordinates;
      b[0] = Math.min(b[0], x); b[1] = Math.min(b[1], y); b[2] = Math.max(b[2], x); b[3] = Math.max(b[3], y);
    }
    return b;
  }

  stop() {
    if (!this.map) return;
    this.view = {center: this.map.getCenter(), zoom: this.map.getZoom()};
    this.map.remove();
    this.map = null;
    this.marker = null;
    this.ready = false;
    this.loaded = {};
  }

  /* the theme's colours, after a change of theme */
  paint() {
    const m = this.map, C = this.C;
    if (!m) return;
    m.setPaintProperty('bg', 'background-color', C.vsea);
    m.setPaintProperty('land', 'fill-color', C.vland);
    for (const id of ['l-region', 'l-ctz', 'l-intl', 'l-dmz']) m.setPaintProperty(id, 'line-color', C.ink);
    if (m.getLayer('l-county')) {
      m.setPaintProperty('l-county', 'line-color', C.vline);
      m.setPaintProperty('lab-county', 'text-color', C.muted);
      m.setPaintProperty('lab-county', 'text-halo-color', C.vland);
    }
    m.setPaintProperty('l-coast', 'line-color', C.muted);
    m.setPaintProperty('dots', 'circle-color', C.vdot);
    m.setPaintProperty('dots', 'circle-stroke-color', C.bg);
    m.setPaintProperty('dots-dim', 'circle-color', C.muted);
    for (const id of ['names-0', 'cities-lab']) m.setPaintProperty(id, 'text-color', C.ink);
    for (const id of ['names-1', 'names-2', 'names-3', 'lab-country', 'lab-unit']) m.setPaintProperty(id, 'text-color', C.muted);
    for (const id of ['names-0', 'names-1', 'names-2', 'names-3', 'lab-country', 'lab-unit', 'lab-group', 'cities-lab'])
      m.setPaintProperty(id, 'text-halo-color', C.vland);
    if (m.getLayer('rivers')) m.setPaintProperty('rivers', 'line-color', C.vriv);
    if (m.getLayer('lakes')) m.setPaintProperty('lakes', 'fill-color', C.vlake);
    if (this.pin) this.drawPin();
    this.apply();
  }

  /* the state onto the map: the kind of map, the layers, the filters, the legend */
  apply() {
    const m = this.map, st = this.st, C = this.C, lay = st.lay, fig = this.fig;
    fig.querySelectorAll('.vnm-bar [data-mode]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.mode === st.mode)));
    const O = (this.M && this.M.opt) || {};
    const has = (k) => !!(this.M && this.M.files[{relief: 'dem', elevation: 'dem', koppen: 'koppen', rain: 'climate', pop: 'pop',
      rivers: 'rivers', contours: 'contours'}[k] || k]);
    const thematic = ['elevation', 'koppen', 'rain', 'pop'].some((k) => lay[k] && has(k));
    // the legend the build wrote: each part shown with what it explains
    const test = (t) => t === 'always' || (t === 'notland' ? st.mode !== 'land' : t === 'nb' ? !!lay.nb :
      t.startsWith('mode:') ? st.mode === t.slice(5) : t.startsWith('lay:') ? !!lay[t.slice(4)] && has(t.slice(4)) : false);
    fig.querySelectorAll('.vnm-key [data-show]').forEach((el) => {
      el.hidden = !el.dataset.show.split(' ').some((alt) => alt.split('+').every(test));
    });
    const mm = fig.querySelector('.vnm-key .vnm-month');
    if (mm) mm.textContent = MONTHS[st.month - 1];
    const pyl = fig.querySelector('.vnm-key .vnm-popyear');
    if (pyl) pyl.textContent = st.popyear;
    if (!m || !this.ready) return;        // before the map: the controls and the legend only
    const vis = (id, on) => { if (m.getLayer(id)) m.setLayoutProperty(id, 'visibility', on ? 'visible' : 'none'); };
    const load = (k) => {                // a heavy GeoJSON source fetched the first time its layer shows
      this.loaded = this.loaded || {};
      if (!this.loaded[k] && this.M.files[k]) { this.loaded[k] = 1; m.getSource(k).setData(abs(this.M.files[k])); }
    };
    const mode = st.mode, nb = !!lay.nb;
    const shownC = O.shown || (nb ? ['rvn', 'drv', 'laos', 'cambodia'] : ['rvn']);
    // the tints: the RVN's units by corps zone; all Vietnam's by today's region; plain; none for borders or land
    let fill = C.vpv, filt = ['all', ['==', ['get', 'k'], 'unit'], ['in', ['get', 'c'], ['literal', shownC]]];
    if (mode === 'ctz') { fill = match('ctz', ZC, C, C.vpv); }
    if (mode === 'reg') {
      fill = match('region', RC, C, C.vpv);
      if (!nb) filt = ['all', ['==', ['get', 'k'], 'unit'], ['==', ['get', 'c'], 'rvn']];
    }
    m.setFilter('tint', filt);
    m.setPaintProperty('tint', 'fill-color', fill);
    m.setPaintProperty('tint', 'fill-opacity', thematic ? 0.12 : C.vop);
    vis('tint', mode === 'ctz' || mode === 'reg' || mode === 'prov');
    const lineC = ['in', ['get', 'c'], ['literal', shownC]];
    m.setFilter('l-unit', ['all', ['==', ['get', 'k'], 'line'], ['==', ['get', 'l'], 'unit'], lineC]);
    m.setFilter('l-region', ['all', ['==', ['get', 'k'], 'line'], ['==', ['get', 'l'], 'region'], lineC]);
    const tinted = mode === 'ctz' || mode === 'reg' || mode === 'prov';
    vis('l-unit', tinted);
    // the counties under the units: their lines thin, the units' then in ink, as a zone's are (the map of China)
    const cty = !!lay.counties && has('counties') && tinted;
    if (cty) load('counties');
    vis('county', cty);
    vis('l-county', cty);
    m.setPaintProperty('l-unit', 'line-color', cty ? C.ink : C.vline);
    m.setPaintProperty('l-unit', 'line-width', cty ? 1.3 : 0.6);
    m.setPaintProperty('l-unit', 'line-opacity', cty ? 0.7 : 0.9);
    vis('l-ctz', mode === 'ctz');
    vis('l-region', mode === 'reg');
    vis('l-intl', mode !== 'land');
    vis('l-dmz', mode !== 'land');
    vis('l-coast', mode === 'land' || mode === 'borders');
    // the names of the units and groups (`names`)
    const names = !!lay.names && mode !== 'land' && mode !== 'borders';
    vis('lab-unit', names);
    vis('lab-county', names && cty);
    m.setFilter('lab-unit', ['all', ['==', ['get', 'k'], 'lab'], ['==', ['get', 'l'], 'unit'], ['in', ['get', 'c'], ['literal', shownC]]]);
    vis('lab-group', names && (mode === 'ctz' || mode === 'reg'));
    m.setFilter('lab-group', ['all', ['==', ['get', 'k'], 'lab'], ['==', ['get', 'l'], mode === 'reg' ? 'region' : 'ctz']]);
    // the layers
    for (const k of ['relief', 'elevation', 'koppen', 'contours']) vis(k, lay[k] && has(k));
    const elev = lay.elevation && has('elevation');
    if (elev) load('bathy');
    vis('bathy', elev);
    m.setPaintProperty('bg', 'background-color', elev && this.M.shallow ? this.M.shallow : C.vsea);
    if (lay.contours) load('contours');
    if (lay.rivers && has('rivers')) { load('rivers'); load('lakes'); }
    vis('rivers', lay.rivers && has('rivers'));
    vis('lakes', lay.rivers && has('rivers'));
    vis('lab-river', lay.rivers && lay.names && has('rivers'));
    if (m.getLayer('lakes')) {             // a reservoir from its dam's year (sources/indochina/README.md)
      m.setFilter('lakes', ['all', ['>=', ['get', 'area_km2'], 3],
        ['any', ['==', ['get', 'type'], 'lake'], ['!', ['has', 'dam_year']], ['<=', ['get', 'dam_year'], this.lakeYear()]]]);
    }
    if (lay.rain && has('rain')) {
      load('climate');
      m.setPaintProperty('rain', 'fill-color', ['step', ['get', 'p' + st.month], ...this.M.rain.flatMap((r, i) => (i ? [r.from, r.color] : [r.color]))]);
    }
    vis('rain', lay.rain && has('rain'));
    if (lay.pop && has('pop')) {
      load('pop');
      m.setFilter('pop', ['==', ['get', 'y'], st.popyear]);
    }
    vis('pop', lay.pop && has('pop'));
    if (lay.cities) load('cities');
    vis('cities', !!lay.cities);
    vis('cities-lab', !!lay.cities);
  }

  /* a tap: the place's entries; else a city's figures; else the pin (STYLE 9) */
  tap(e) {
    const t = e.originalEvent && e.originalEvent.target;
    if (t && t.closest && t.closest('.maplibregl-marker')) return;     // the pin's own tap (drawPin)
    const m = this.map, p = e.point, r = 10;
    const box = [[p.x - r, p.y - r], [p.x + r, p.y + r]];
    const live = (ids) => ids.filter((id) => m.getLayer(id) && m.getLayoutProperty(id, 'visibility') !== 'none');
    const dots = m.queryRenderedFeatures(box, {layers: live(['dots', 'dots-dim'])});
    if (dots.length) {
      dots.sort((a, b) => b.properties.n - a.properties.n);
      return this.showPlace(dots[0].properties);
    }
    const city = m.queryRenderedFeatures(box, {layers: live(['cities'])});
    if (city.length) return this.showCity(city[0].properties);
    clearTimeout(this.tapT);              // a second tap of a double tap zooms: the pin waits for it (start)
    const ll = [e.lngLat.lng, e.lngLat.lat];
    this.tapT = setTimeout(() => { this.pop.hidden = true; this.setPin(ll, true); }, 300);
  }

  /* the pin (STYLE 9): set, moved or taken away (ll null); drawn as the library's marker */
  setPin(ll, tapped) {
    if (tapped) { this.pinWas = this.pin; this.pinT = performance.now(); }
    this.pin = ll;
    this.pinN = (this.pinN || 0) + 1;
    this.drawPin();
    this.pinShow();
  }
  drawPin() {
    if (this.marker) { this.marker.remove(); this.marker = null; }
    if (!this.pin || !this.map || !this.ml) return;
    const mk = this.marker = new this.ml.Marker({color: this.C.ink, anchor: 'bottom'}).setLngLat(this.pin).addTo(this.map);
    const el = mk.getElement();
    el.title = 'Take the pin away';
    el.setAttribute('role', 'button');
    el.setAttribute('aria-label', 'Take the pin away');
    el.tabIndex = 0;
    let down = null;                      // a drag that starts on the pin moves the map, and keeps the pin
    el.addEventListener('pointerdown', (ev) => { down = [ev.clientX, ev.clientY]; });
    el.addEventListener('click', (ev) => {
      ev.stopPropagation();
      if (!down || Math.hypot(ev.clientX - down[0], ev.clientY - down[1]) <= 4) this.setPin(null);
    });
    el.addEventListener('keydown', (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); this.setPin(null); } });
  }

  /* the panel: what can be written at once, then each layer as its file is read */
  pinShow() {
    const el = this.pinEl;
    if (!el) return;
    if (!this.pin || !this.M) { el.hidden = true; el.innerHTML = ''; return; }
    const n = this.pinN, ll = this.pin, R = this.pinR = n === this.pinRn ? this.pinR : {};
    this.pinRn = n;
    const draw = () => { if (n === this.pinN) el.innerHTML = this.pinHTML(ll, R); };
    el.hidden = false;
    draw();
    const f = this.M.files, got = (k) => (v) => { R[k] = v; draw(); }, lost = (k) => () => { R[k] = false; draw(); };
    for (const k of ['admin', 'counties', 'bathy', 'rivers', 'lakes', 'climate', 'pop', 'cities']) {
      if (f[k] && !(k in R)) json(abs(f[k])).then(got(k), lost(k));
    }
    for (const k of ['dem', 'koppen']) if (f[k] && !(k in R)) this.pixel(k, ll).then(got(k), lost(k));
  }

  /* a raster's pixel at the point, at the tiles' deepest zoom: [r, g, b, a], or null where there is no tile */
  async pixel(k, ll) {
    const ml = await lib(), url = abs(this.M.files[k]);
    const P = pmt[url] || (pmt[url] = new window.pmtiles.PMTiles(url));
    const z = (await P.getHeader()).maxZoom, n = 2 ** z, c = ml.MercatorCoordinate.fromLngLat(ll);
    const tx = Math.floor(c.x * n), ty = Math.floor(c.y * n), key = url + '/' + z + '/' + tx + '/' + ty;
    if (!tiles[key]) {
      tiles[key] = P.getZxy(z, tx, ty).then(async (t) => {
        if (!t) return null;
        const b = await createImageBitmap(new Blob([t.data]), {premultiplyAlpha: 'none', colorSpaceConversion: 'none'});
        const cv = document.createElement('canvas');
        cv.width = b.width;
        cv.height = b.height;
        const cx = cv.getContext('2d', {willReadFrequently: true});
        cx.drawImage(b, 0, 0);
        return cx.getImageData(0, 0, b.width, b.height);
      });
      tileKeys.push(key);
      if (tileKeys.length > 8) delete tiles[tileKeys.shift()];
    }
    const d = await tiles[key];
    if (!d) return null;
    const px = Math.min(d.width - 1, Math.floor((c.x * n - tx) * d.width)), py = Math.min(d.height - 1, Math.floor((c.y * n - ty) * d.height));
    const i = (py * d.width + px) * 4;
    return Array.from(d.data.slice(i, i + 4));
  }

  /* the panel's lines (STYLE 9): the pin's place, then a line for each layer the map has */
  pinHTML(ll, R) {
    const M = this.M, f = M.files, pin = M.pin || {}, pages = pin.pages || {}, L = [];
    const line = (h) => L.push('<div>' + h + '</div>');
    const wait = (k) => (R[k] === undefined ? '…' : R[k] === false ? 'could not be read.' : null);
    const link = (text, href) => (href ? '<a href="' + esc(href) + '">' + esc(text) + '</a>' : esc(text));
    const entries = (n) => n + (n === 1 ? ' entry' : ' entries');
    // the nearest place of the gazetteer
    const [pl, d] = nearest(ll, M.places.features);
    if (pl) {
      const q = pl.properties, n = (this.at[q.id] || []).length;
      line('Nearest place: ' + link(q.name, (pages.p || {})[q.id]) + ', ' + showKm(d) + '. <span class="m">' +
        (n ? entries(n) + ' placed there' : 'No entry placed there') + (this.yearNow() === 'all' ? '' : ' in these dates') + '.</span>' +
        (this.D.gz != null ? ' <a class="m" href="' + esc(this.D.gz) + '#pl-' + esc(q.id) + '">In the gazetteer</a>' : ''));
    }
    // the borders' file and the counties: "[County], [Prefecture], [Province], [Country]." and the unit's items after
    // it, in the register's and the site's names, no kind and no date (the owner, Nov. 27, 2026)
    let sea = null;
    if (wait('admin')) line(wait('admin'));
    else {
      const A = R.admin, here = within(ll, A, (q) => ['land', 'unit', 'disp'].includes(q.k));
      const unit = here.find((x) => x.properties.k === 'unit'), land = here.find((x) => x.properties.k === 'land');
      const disp = here.find((x) => x.properties.k === 'disp');
      sea = !unit && !land && !disp;
      const names = {};
      for (const x of A.features) if (x.properties.k === 'lab' && x.properties.l === 'country') names[x.properties.id] = x.properties.name;
      const cid = unit ? unit.properties.c : land && land.properties.id;
      const cname = cid ? (pin.names || {})[cid] || names[cid] || (land || unit).properties.name : null;
      const zh = (t) => (t ? ' <span class="m" lang="zh">' + esc(t) + '</span>' : '');
      const tiers = [], items = [];             // each tier [html, characters]
      if (f.counties && unit) {
        const c = wait('counties') ? null : within(ll, R.counties, (q) => q.k === 'county')[0];
        if (wait('counties')) tiers.push(['…', null]);
        else if (c) {
          const k = countyOf(c.properties.line), py = (pin.pref || {})[k.pref];
          tiers.push([esc(c.properties.name) + zh(k.zh), k.zh]);
          if (py) tiers.push([esc(py) + zh(k.pref), k.pref]);
          if (k.note) items.push(k.note);
        }
      }
      if (unit) {
        const u = unit.properties, uz = (pin.zh || {})[u.id];
        const nm = cname ? u.name.replace(' (' + cname + ')', '') : u.name;
        if (nm !== cname) tiers.push([link(nm, (pages.u || {})[u.id]) + zh(uz), uz]);
        items.push(...this.unitItems(u));
      }
      // a tier named as the one above it is that one (a city that is its own prefecture or municipality)
      const shown = tiers.filter((t, i) => !t[1] || !tiers.slice(i + 1).some((x) => x[1] === t[1]));
      if (sea) line('At sea.');
      else {
        const head = shown.map((t) => t[0]).concat(cid ? [link(cname, (pages.c || {})[cid]) +
          (unit && unit.properties.name === cname && unit.properties.c === cid && unit.properties.kind && !(pin.names || {})[cid] ? ', ' + esc(unit.properties.kind) : '')] : []);
        if (disp) items.unshift(esc(disp.properties.name) + ', disputed.');
        const inU = unit && (M.opt || {}).unit ? this.atv[unit.properties.id] || [] : [];
        line((head.length ? head.join(', ') + '.' : '') + (items.length ? ' ' + items.join(' ') : '') +
          (inU.length ? '<details><summary>' + entries(inU.length) + ' placed in it as a whole</summary>' + this.rows(inU) + '</details>' : ''));
      }
    }
    // the elevation's tiles, and the sea's depth
    let elev = null;
    if (f.dem) {
      const v = R.dem;
      if (wait('dem')) line('Elevation: ' + wait('dem'));
      else if (!v || v[3] === 0) line('Elevation: <span class="m">no reading here.</span>');
      else {
        const e = v[0] * 256 + v[1] + v[2] / 256 - 32768;
        elev = Math.abs(e + 1) < 0.01 ? null : Math.round(e);   // the sea is -1 m in the tiles; land may lie below 0
        line(elev == null ? 'Elevation: <span class="m">the sea.</span>' : 'Elevation: about ' + elev.toLocaleString('en-US') + ' m.');
      }
    }
    if (f.bathy && (sea || (R.dem && elev == null))) {
      if (wait('bathy')) line('Depth of the sea: ' + wait('bathy'));
      else {
        const b = within(ll, R.bathy).map((x) => +x.properties.d).sort((a, c) => c - a)[0];
        const D = (M.depths || []).find((x) => +x.from === b);
        line('Depth of the sea: ' + (D ? esc(D.label) : M.depths && M.depths.length ? 'under ' + M.depths[0].from + ' m' : 'no reading') + '.');
      }
    }
    // the rivers and lakes
    if (f.rivers) {
      if (wait('rivers')) line('Rivers: ' + wait('rivers'));
      else {
        let best = null, bd = RIVER_KM, k = RIVER_KM / 111 / Math.max(0.2, Math.cos(ll[1] * RAD));
        for (const x of R.rivers.features) {
          const b = bbox(x.geometry);
          if (ll[0] < b[0] - k || ll[0] > b[2] + k || ll[1] < b[1] - RIVER_KM / 111 || ll[1] > b[3] + RIVER_KM / 111) continue;
          const dd = toLine(ll, x.geometry);
          if (dd < bd) { bd = dd; best = x.properties; }
        }
        if (!best) line('Rivers: <span class="m">none within ' + RIVER_KM + ' km.</span>');
        else {
          const nm = best.name_vi || best.name, sz = +best.size, sw = best.source === 'SWORD';
          const size = (sw ? WIDTH : FLOW)[sz - 1];
          line('Rivers: nearest, ' + (nm ? esc(nm) + (best.name_vi && best.name && best.name !== nm ? ' (' + esc(best.name) + ')' : '') : 'unnamed') +
            ', ' + showKm(bd) + '. <span class="m">' + (size ? (sw ? 'A channel ' : 'A mean flow of ') + size + ' (' + esc(best.source) + ').' : '') + '</span>');
        }
      }
      if (f.lakes) {
        if (wait('lakes')) line('Lakes: ' + wait('lakes'));
        else {
          const k = within(ll, R.lakes)[0];
          if (!k) line('Lakes: <span class="m">none here.</span>');
          else {
            const q = k.properties, dam = q.dam_year ? ', dam of ' + q.dam_year : '';
            line('Lakes: ' + (q.name ? esc(q.name) : 'unnamed') + ' <span class="m">(' + esc(q.type || 'lake') + dam + ', ' +
              Math.round(+q.area_km2).toLocaleString('en-US') + ' km²)</span>.');
          }
        }
      }
    }
    // the climate's tiles: the class by its colour
    if (f.koppen) {
      const v = R.koppen;
      if (wait('koppen')) line('Climate: ' + wait('koppen'));
      else if (!v || v[3] === 0) line('Climate: <span class="m">none here.</span>');
      else {
        const hex = '#' + v.slice(0, 3).map((x) => x.toString(16).padStart(2, '0')).join('');
        const c = (pin.koppen || M.koppen || []).find((x) => x.color.toLowerCase() === hex);
        line('Climate: ' + (c ? esc(c.code + ' ' + c.name) : '<span class="m">a colour the legend does not name (' + hex + ').</span>') + (c ? '.' : ''));
      }
    }
    // the precipitation and the temperature, month by month, as bars (CRU CL 2.0's means of 1961-1990: the page's text)
    if (f.climate) {
      if (wait('climate')) line('Precipitation: ' + wait('climate'));
      else {
        const c = within(ll, R.climate)[0];
        if (!c) line('Precipitation: <span class="m">no cell here.</span>');
        else {
          const q = c.properties, mo = (pre) => MONTHS.map((_, i) => +q[pre + (i + 1)]);
          const p = mo('p'), year = p.reduce((a, x) => a + x, 0);
          line('Precipitation: <span class="m">the year, ' + Math.round(year).toLocaleString('en-US') + ' mm.</span>' +
            bars(p, (x) => Math.round(x).toLocaleString('en-US'), (x) => x.toLocaleString('en-US') + ' mm', 'Precipitation'));
          if (q.t1 != null) {
            const t = mo('t'), mean = t.reduce((a, x) => a + x, 0) / 12;
            line('Temperature: <span class="m">the year\'s mean, ' + minus(mean.toFixed(1)) + ' °C.</span>' +
              bars(t, (x) => minus(Math.round(x) || 0), (x) => minus(x) + ' °C', 'Temperature'));
          }
        }
      }
    }
    // the population's classes, 1960 and 1970
    if (f.pop) {
      if (wait('pop')) line('Population density: ' + wait('pop'));
      else {
        const C = M.pop.classes, cls = (i) => (i + 1 < C.length ? C[i].from.toLocaleString('en-US') + '–' + C[i + 1].from.toLocaleString('en-US') : C[i].from.toLocaleString('en-US') + ' and over');
        const at = within(ll, R.pop), by = M.pop.years.map((y) => [y, at.find((x) => +x.properties.y === y)]);
        line('Population density: ' + (by.some(([, x]) => x) ? by.map(([y, x]) => y + ', ' + (x ? cls(+x.properties.c) + ' persons a km²' : 'none')).join('; ') + '.' : '<span class="m">no cell here.</span>'));
      }
    }
    // the cities of the Yearbook
    if (f.cities) {
      if (wait('cities')) line('Cities: ' + wait('cities'));
      else {
        const [c, cd] = nearest(ll, R.cities.features);
        if (!c) line('Cities: <span class="m">none on the map.</span>');
        else line('Cities: nearest, ' + esc(c.properties.name) + ', ' + showKm(cd) + '. <span class="m">' + esc(JSON.parse(c.properties.rows)[0].text) + '</span>');
      }
    }
    return '<button type="button" class="x" aria-label="Take the pin away">×</button><b>' + showLL(ll) + '</b>' + L.join('');
  }

  /* the unit's items after the place line (STYLE 9): the RVN's corps zone and region, the other countries' units
     drawn by today's lines and their region; none for the map of China's */
  unitItems(u) {
    const Z = {I: 'I Corps.', II: 'II Corps.', III: 'III Corps.', IV: 'IV Corps.', CMD: 'Capital Military District.'};
    const O = this.M.opt || {};
    if (O.unit) return [];
    return [u.src === 'today' ? "Today's " + (u.kind || 'unit') + '.' : '', Z[u.ctz] || '', u.region ? u.region + ' region.' : ''].filter(Boolean);
  }

  showPlace(q) {
    const hits = this.at[q.id] || [], all = this.yearNow() === 'all';
    const gz = this.D.gz != null ? ' <a class="m" href="' + esc(this.D.gz) + '#pl-' + esc(q.id) + '">In the gazetteer</a>' : '';
    let h = '<button type="button" class="x" aria-label="Close">×</button><b>' + esc(q.name) + '</b>';
    if (!hits.length) h += gz + '<div class="m">No entry placed here' + (all ? '' : ' in these dates') + '.</div>';
    else {
      h += ' <span class="m">' + hits.length + (hits.length > 1 ? ' entries' : ' entry') + '</span>' + gz + this.rows(hits);
    }
    this.pop.innerHTML = h;
    this.pop.hidden = false;
  }

  showCity(q) {
    const rows = JSON.parse(q.rows);
    this.pop.innerHTML = '<button type="button" class="x" aria-label="Close">×</button><b>' + esc(q.name) + '</b><ul>' +
      rows.map((r) => '<li>' + esc(r.text) + '</li>').join('') + '</ul>';
    this.pop.hidden = false;
  }
}

class Home {
  constructor(b) { this.b = b; }
  onAdd(map) {
    this.c = document.createElement('div');
    this.c.className = 'maplibregl-ctrl maplibregl-ctrl-group';
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'vnm-home';
    b.title = b.ariaLabel = 'Back to the first view';
    b.textContent = '⌂';
    b.addEventListener('click', () => map.fitBounds(this.b, {padding: 8}));
    this.c.append(b);
    return this.c;
  }
  onRemove() { this.c.remove(); }
}

/* Start a map when its figure nears the screen; keep at most MAX_LIVE drawn, the farthest given up first. */
const figs = new Map();
const live = [];
async function wake(el) {
  let F = figs.get(el);
  if (!F) { F = new Figure(el); figs.set(el, F); }
  if (F.map || F.starting) return;
  F.starting = true;
  try {
    F.awake = true;                      // the entries' files are read from here on, the span's years alone
    const [ml, M] = await Promise.all([lib(), manifest(el.dataset.geo), F.data()]);
    if (!M.byId) M.byId = Object.fromEntries(M.places.features.map((f) => [f.properties.id, f]));
    F.M = M;
    F.refresh();
    if (live.length >= MAX_LIVE) {
      const far = live.filter((x) => !x.near).sort((a, b) => a.seen - b.seen)[0] || live[0];
      far.stop();
      live.splice(live.indexOf(far), 1);
    }
    F.seen = performance.now();
    await F.start(ml, M);
    live.push(F);
  } finally {
    F.starting = false;
  }
}

function init() {
  const all = document.querySelectorAll('figure.vnm');
  if (!all.length) return;
  all.forEach((el) => { if (!figs.has(el)) figs.set(el, new Figure(el)); });
  if (!('IntersectionObserver' in window)) { all.forEach((el) => wake(el)); return; }
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    const F = figs.get(e.target);
    F.near = e.isIntersecting;
    if (e.isIntersecting) { F.seen = performance.now(); wake(e.target); }
  }), {rootMargin: '600px 0px'});
  all.forEach((el) => io.observe(el));
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
else init();
