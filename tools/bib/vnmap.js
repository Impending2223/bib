/* The maps of Indochina: the calendar's annual maps and indochina.html (tools/bib/vnmap.py, its STYLE notes).
   One script for both, loaded as a module. MapLibre GL JS draws the map (vendored, loaded when a map nears the
   screen); this file builds the style from the manifest the build writes, wires the controls the build writes into
   the figure, and lists the entries. No projection, gesture or label placement of its own: the library's. */
const LIB = /*LIB*/{};                   // the vendored files, relative to this script (vnmap.py fills it in)
const HERE = new URL('.', import.meta.url);
const MONTHS = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'];
const MAX_LIVE = 4;                      // WebGL contexts kept at once on a page (the series reader holds nine maps)

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
const LAZY = {rivers: 'rivers', lakes: 'lakes', contours: 'contours', bathy: 'bathy', climate: 'climate', pop: 'pop'};
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

function style(M, C, places) {
  const f = M.files;
  const src = {
    admin: {type: 'geojson', data: abs(f.admin), attribution: M.credit.admin},
    places: {type: 'geojson', data: places},
    cities: {type: 'geojson', data: abs(f.cities)},
  };
  for (const k of Object.keys(LAZY)) if (f[k]) src[k] = {type: 'geojson', data: EMPTY, attribution: M.credit[k]};
  if (f.dem) src.dem = {type: 'raster-dem', url: 'pmtiles://' + abs(f.dem), encoding: 'terrarium', tileSize: 512, attribution: M.credit.dem};
  if (f.koppen) src.koppen = {type: 'raster', url: 'pmtiles://' + abs(f.koppen), tileSize: 256, attribution: M.credit.koppen};
  const hide = {visibility: 'none'};
  const L = [
    {id: 'bg', type: 'background', paint: {'background-color': C.vsea}},
    f.bathy && {id: 'bathy', type: 'fill', source: 'bathy', layout: hide,
      paint: {'fill-color': ['match', ['get', 'd'], ...M.depths.flatMap((d) => [d.from, d.color]), C.vsea]}},
    {id: 'land', type: 'fill', source: 'admin', filter: ['==', ['get', 'k'], 'land'], paint: {'fill-color': C.vland}},
    f.dem && {id: 'elevation', type: 'color-relief', source: 'dem', layout: hide,
      paint: {'color-relief-color': ['step', ['elevation'], 'rgba(0,0,0,0)', ...M.hypso.flatMap((h) => [h.from, h.color])]}},
    f.koppen && {id: 'koppen', type: 'raster', source: 'koppen', layout: hide, paint: {'raster-opacity': 0.8, 'raster-resampling': 'nearest'}},
    f.climate && {id: 'rain', type: 'fill', source: 'climate', layout: hide, paint: {'fill-opacity': 0.85}},
    f.pop && {id: 'pop', type: 'fill', source: 'pop', layout: hide,
      paint: {'fill-color': ['match', ['get', 'c'], ...M.pop.classes.flatMap((c, i) => [i, c.color]), '#ccc'], 'fill-opacity': 0.85}},
    {id: 'tint', type: 'fill', source: 'admin', filter: ['==', ['get', 'k'], 'unit'], paint: {'fill-color': C.vpv, 'fill-opacity': C.vop}},
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
    {id: 'l-dmz', type: 'line', source: 'admin', filter: ['all', ['==', ['get', 'k'], 'line'], ['==', ['get', 'l'], 'dmz']],
      layout: {'line-join': 'round'}, paint: {'line-color': C.ink, 'line-width': 1.2, 'line-dasharray': [3, 1.5]}},
    {id: 'cities', type: 'circle', source: 'cities', layout: hide,
      paint: {'circle-radius': ['*', 0.0105, ['sqrt', ['get', 'pop']]], 'circle-color': C.vcity, 'circle-opacity': 0.35,
        'circle-stroke-color': C.vcity, 'circle-stroke-width': 1}},
    {id: 'dots-dim', type: 'circle', source: 'places', filter: ['==', ['get', 'n'], 0],
      paint: {'circle-radius': 2.4, 'circle-color': C.muted, 'circle-opacity': 0.7}},
    {id: 'dots', type: 'circle', source: 'places', filter: ['>', ['get', 'n'], 0],
      layout: {'circle-sort-key': ['-', 0, ['get', 'n']]},
      paint: {'circle-radius': ['max', 3.2, ['*', 2.6, ['sqrt', ['get', 'n']]]], 'circle-color': C.vdot,
        'circle-stroke-color': C.bg, 'circle-stroke-width': 1}},
    // the names: the year's places above all, then the gazetteer's by rank as the zoom allows (STYLE 3)
    {id: 'lab-unit', type: 'symbol', source: 'admin', filter: ['all', ['==', ['get', 'k'], 'lab'], ['==', ['get', 'l'], 'unit']],
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
    {id: 'lab-country', type: 'symbol', source: 'admin', filter: ['all', ['==', ['get', 'k'], 'lab'], ['==', ['get', 'l'], 'country']],
      layout: {'text-field': ['get', 'name'], 'text-font': ITAL, 'text-size': 14, 'text-max-width': 8, 'text-letter-spacing': 0.04,
        'symbol-sort-key': ['-', 0, ['get', 'km2']]},
      paint: {'text-color': C.muted, 'text-halo-color': C.vland, 'text-halo-width': 1.5}},
    {id: 'cities-lab', type: 'symbol', source: 'cities', layout: {visibility: 'none', 'text-field': ['get', 'label'], 'text-font': FONT,
      'text-size': 11, 'text-variable-anchor': ['top', 'bottom', 'left', 'right'], 'text-radial-offset': 0.9,
      'symbol-sort-key': ['-', 0, ['get', 'pop']]},
      paint: {'text-color': C.ink, 'text-halo-color': C.vland, 'text-halo-width': 1.5}},
  ];
  for (const r of [3, 2, 1, 0]) {        // 0: a place with this year's entries; 1-3: the gazetteer's ranks
    L.push({id: 'names-' + r, type: 'symbol', source: 'places',
      filter: r ? ['all', ['==', ['get', 'n'], 0], ['==', ['get', 'r'], r]] : ['>', ['get', 'n'], 0],
      layout: {'text-field': ['get', 'name'], 'text-font': r ? FONT : BOLD, 'text-size': r ? 11 : 12,
        'text-variable-anchor': ['left', 'right', 'top', 'bottom'], 'text-radial-offset': r ? 0.55 : 0.75,
        'text-justify': 'auto', 'symbol-sort-key': r ? ['get', 'r'] : ['-', 0, ['get', 'n']], 'text-padding': 2},
      paint: {'text-color': r ? C.muted : C.ink, 'text-halo-color': C.vland, 'text-halo-width': 1.5}});
  }
  const fonts = Object.fromEntries(Object.entries(M.fonts).map(([k, v]) => [k, v.map((x) => ({...x, url: abs(x.url)}))]));
  return {version: 8, 'font-faces': fonts, sources: src, layers: L.filter(Boolean)};
}

/* One figure: the map, its controls, the tap's list, the folded list. */
class Figure {
  constructor(fig) {
    this.fig = fig;
    this.D = JSON.parse(fig.querySelector('.vnm-d').textContent);
    this.full = !!this.D.ys;
    this.box = fig.querySelector('.vnm-box');
    this.pop = fig.querySelector('.vnm-pop');
    this.st = {mode: 'ctz', lay: {}, month: 7, popyear: 1960, y: this.D.y};
    try {
      const s = JSON.parse(sessionStorage.getItem('vnm2') || '{}');
      Object.assign(this.st, {mode: s.mode || 'ctz', lay: s.lay || {}, month: s.month || 7, popyear: s.popyear || 1960});
    } catch (e) { /* storage refused: the defaults */ }
    if (this.full) {
      const m = /^#y(\d{4}|all)$/.exec(location.hash);
      this.st.y = m && (m[1] === 'all' || this.D.ys.includes(m[1])) ? m[1] : 'all';
    }
    this.controls();
    this.setYear(this.st.y, false);
  }

  save() {
    try {
      sessionStorage.setItem('vnm2', JSON.stringify({mode: this.st.mode, lay: this.st.lay, month: this.st.month, popyear: this.st.popyear}));
    } catch (e) { /* storage refused */ }
  }

  yearOf(i) { return this.D.e[i].y || this.D.y; }
  on(i) { return this.st.y === 'all' || this.yearOf(i) === this.st.y; }
  lakeYear() { return +(this.st.y === 'all' ? this.D.ys[this.D.ys.length - 1] : this.st.y); }

  /* the controls the build wrote: the year links, the map's kind, the layers */
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
        this.setYear(a.dataset.yr, true);
      });
      addEventListener('hashchange', () => {
        const m = /^#y(\d{4}|all)$/.exec(location.hash);
        if (m && (m[1] === 'all' || this.D.ys.includes(m[1]))) this.setYear(m[1], true);
      });
    }
    this.pop.addEventListener('click', (e) => { if (e.target.closest('.x')) this.pop.hidden = true; });
  }

  /* the year: the dots, the tap's list, the folded list, the caption, the lakes (STYLE 2, 6) */
  setYear(y, redraw) {
    this.st.y = y;
    const at = {};
    this.D.e.forEach((x, i) => { if (this.on(i)) x.p.forEach((p) => (at[p] = at[p] || []).push(i)); });
    this.at = at;
    const yrs = this.fig.querySelector('.vnm-yrs');
    if (yrs) yrs.querySelectorAll('a').forEach((a) => a.toggleAttribute('aria-current', a.dataset.yr === y));
    const E = this.D.e.filter((x, i) => this.on(i));
    const all = this.full && y === 'all';
    const names = this.D.pn || {};
    this.fig.querySelector('.vnm-list ol').innerHTML = E.map((x) => '<li><a href="' + esc(x.h) + '">' + this.when(x) +
      '</a> <span class="m">' + esc(x.t) + '.</span> ' + esc(x.s) +
      (x.p.length ? ' <span class="m">(' + x.p.map((k) => esc(names[k] || k)).join(', ') + ')</span>' : '') + '</li>').join('');
    this.fig.querySelector('.vnm-list summary').textContent = (all ? 'The placed entries' : "The year's placed entries") + ' (' + E.length + ')';
    const cnt = this.fig.querySelector('.vnm-cnt');
    if (cnt) {
      const np = new Set(E.flatMap((x) => x.p)).size;
      cnt.textContent = (all ? 'All years' : y) + ': ' + E.length + ' placed ' + (E.length === 1 ? 'entry' : 'entries') + ', at ' + np + ' places.';
    }
    this.pop.hidden = true;
    if (redraw && this.map) { this.places(); this.apply(); }
  }

  when(x) { return esc(x.w) + (this.full && this.st.y === 'all' ? ', ' + x.y : ''); }

  /* the gazetteer's places with the year's count (`n`), for the dots and names */
  placesFC() {
    return {type: 'FeatureCollection', features: this.M.places.features.map((f) => ({
      type: 'Feature', geometry: f.geometry,
      properties: Object.assign({}, f.properties, {n: (this.at[f.properties.id] || []).length})}))};
  }

  places() { if (this.map) this.map.getSource('places').setData(this.placesFC()); }

  async start(ml, M) {
    this.M = M;
    const C = this.C = colors();
    const home = this.homeBounds();
    const map = this.map = new ml.Map({
      container: this.fig.querySelector('.vnm-gl'),
      style: style(M, C, this.placesFC()),
      bounds: home, fitBoundsOptions: {padding: 8},
      maxBounds: M.bounds, renderWorldCopies: false,
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
      if (this.view) map.jumpTo(this.view);   // a map given up and drawn again keeps its view
      const z = this.homeZoom = this.view ? this.homeZoom : map.getZoom();
      map.setMaxZoom(z + 6);              // 64 times the first view (STYLE 4)
      map.setMinZoom(Math.max(0, z - 1.5));
      map.setLayerZoomRange('names-2', z + 1.1, 24);   // rank 2 from about twice the first view, rank 3 from six times
      map.setLayerZoomRange('names-3', z + 2.6, 24);
      this.apply();
      map.once('idle', () => { this.fig.dataset.ready = '1'; });
    });
    map.on('click', (e) => this.tap(e));
    for (const id of ['dots', 'dots-dim', 'cities']) {
      map.on('mouseenter', id, () => { map.getCanvas().style.cursor = 'pointer'; });
      map.on('mouseleave', id, () => { map.getCanvas().style.cursor = ''; });
    }
    const retheme = () => { this.C = colors(); this.paint(); };
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', retheme);
    new MutationObserver(retheme).observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
  }

  homeBounds() {
    if (this.full) return this.M.home.all;
    const b = this.M.home.rvn.slice();
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
    m.setPaintProperty('l-unit', 'line-color', C.vline);
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
    this.apply();
  }

  /* the state onto the map: the kind of map, the layers, the filters, the legend */
  apply() {
    const m = this.map, st = this.st, C = this.C, lay = st.lay, fig = this.fig;
    fig.querySelectorAll('.vnm-bar [data-mode]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.mode === st.mode)));
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
    const shownC = nb ? ['rvn', 'drv', 'laos', 'cambodia'] : ['rvn'];
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
    vis('l-unit', mode === 'ctz' || mode === 'reg' || mode === 'prov');
    vis('l-ctz', mode === 'ctz');
    vis('l-region', mode === 'reg');
    vis('l-intl', mode !== 'land');
    vis('l-dmz', mode !== 'land');
    vis('l-coast', mode === 'land' || mode === 'borders');
    // the names of the units and groups (`names`)
    const names = !!lay.names && mode !== 'land' && mode !== 'borders';
    vis('lab-unit', names);
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
    vis('cities', !!lay.cities);
    vis('cities-lab', !!lay.cities);
  }

  /* a tap: the place's entries; else a city's figures; else the rain or the unit under it */
  tap(e) {
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
    const at = m.queryRenderedFeatures(p, {layers: live(['rain', 'tint'])});
    const rain = at.find((f) => f.layer.id === 'rain'), unit = at.find((f) => f.layer.id === 'tint');
    if (!rain && !unit) { this.pop.hidden = true; return; }
    let h = '<button type="button" class="x" aria-label="Close">×</button>';
    if (unit) h += '<b>' + esc(unit.properties.name) + '</b> <span class="m">' + esc(this.unitLine(unit.properties)) + '</span>';
    if (rain) {
      const q = rain.properties, mo = this.st.month;
      h += '<div>Rain, ' + MONTHS[mo - 1] + ', mean of 1961–1990: ' + q['p' + mo] + ' mm' +
        (q['t' + mo] != null ? '; mean temperature ' + q['t' + mo] + ' °C' : '') + '.</div>';
    }
    this.pop.innerHTML = h;
    this.pop.hidden = false;
  }

  unitLine(u) {
    const Z = {I: 'I Corps', II: 'II Corps', III: 'III Corps', IV: 'IV Corps', CMD: 'Capital Military District'};
    if (u.c === 'rvn') return ['province of late 1966', Z[u.ctz], u.region].filter(Boolean).join(' · ');
    return [u.kind === 'province' ? "today's province" : u.kind, u.region].filter(Boolean).join(' · ');
  }

  showPlace(q) {
    const hits = this.at[q.id] || [], all = this.full && this.st.y === 'all';
    const gz = this.full ? ' <a class="m" href="#pl-' + esc(q.id) + '">In the gazetteer</a>' : '';
    let h = '<button type="button" class="x" aria-label="Close">×</button><b>' + esc(q.name) + '</b>';
    if (!hits.length) h += gz + '<div class="m">No entry placed here' + (all ? '' : ' this year') + '.</div>';
    else {
      h += ' <span class="m">' + hits.length + (hits.length > 1 ? ' entries' : ' entry') + '</span>' + gz + '<ol>' +
        hits.map((i) => { const x = this.D.e[i]; return '<li><a href="' + esc(x.h) + '">' + this.when(x) + '</a> <span class="m">' + esc(x.t) + '.</span> ' + esc(x.s) + '</li>'; }).join('') + '</ol>';
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
    const [ml, M] = await Promise.all([lib(), manifest(el.dataset.geo)]);
    if (!M.byId) M.byId = Object.fromEntries(M.places.features.map((f) => [f.properties.id, f]));
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
