"""Map layers for Vietnam, Laos and Cambodia: relief, rivers and lakes, climate, rainfall.

One-time script (Oct. 21, 2026). It reads downloads kept outside the repo (DL, the first argument) and writes
sources/indochina/ (OUT, the second argument). Run each step with python3 -I:

    python3 -I tools/vnmap/layers.py DL OUT [relief] [hydro] [lakes] [koppen] [climate]

The extent of every layer: lon 100.0-110.5 E, lat 8.0-23.5 N (WGS84). The rasters (PNG) are written in Web
Mercator rows: column i covers lon 100 + 10.5*i/W .. 100 + 10.5*(i+1)/W, evenly; row j is evenly spaced in
EPSG:3857 y between y(23.5) at the top and y(8.0) at the foot, so the page draws each as one <image> over the
Mercator rectangle of the bounds. Rows are sampled by bilinear (continuous fields) or nearest (classes)
interpolation at each row's centre latitude. The rainfall grid (JSON) is plain lon/lat cells.

Reads (DL/...), where from, and what each makes:

  etopo30s.dods       ETOPO 2022 v1, 30 arc-second surface elevation (NOAA NCEI), the extent's subset by OPeNDAP:
                      https://www.ngdc.noaa.gov/thredds/dodsC/global/ETOPO2022/30s/30s_surface_elev_netcdf/
                      ETOPO_2022_v1_30s_N90W180_surface.nc.dods?z[11760:1:13619][33600:1:34859]
                      -> hillshade.png, hillshade-coarse.png, hypso.png, hypso-coarse.png, hypso.json,
                         contours.geojson
  e15_N15E090.dods, e15_N15E105.dods, e15_N30E090.dods, e15_N30E105.dods   ETOPO 2022 v1, 15 arc-second surface
                      elevation, the four tiles' parts of the extent by OPeNDAP (.../15s/15s_surface_elev_netcdf/
                      ETOPO_2022_v1_15s_<tile>_surface.nc.dods?z[rows][cols]; rows 0:2039 of the N30 tiles,
                      1920:3599 of the N15; cols 2400:3599 of E090, 0:1319 of E105)
                      -> hillshade-fine.png
  ne/ne_10m_land.shp  Natural Earth 10m land 5.1.1 (naciscdn.org): the sea mask for the relief rasters
  hr/HydroRIVERS_v10_as_shp/HydroRIVERS_v10_as.shp   HydroRIVERS v1.0, Asia (data.hydrosheds.org)
  sword/shp/as_sword_reaches_hb4[34]_v17c.*          SWORD v17c reaches, Pfafstetter basins 43 and 44 (Zenodo
                      record 22259077, read out of SWORD_v17c_shp.zip by HTTP range requests): the delta's
                      distributaries HydroRIVERS cannot draw, and the rivers' names
                      -> rivers.geojson, rivers-coarse.geojson (step hydro)
  hl/HydroLAKES_polys_v10_shp/HydroLAKES_polys_v10.shp   HydroLAKES v1.0 (data.hydrosheds.org)
  grand/Res.Grand.txt GRanD's dams, one a line: rank, capacity (million m3), area (km2), year, lon, lat, ...
                      (Lehner, Dam Impoundment Database, Zenodo record 15350094): the reservoirs' dam years
                      -> lakes.geojson (step lakes)
  kg/1961_1990/koppen_geiger_0p00833333.tif, kg/legend.txt   Beck et al. (2023), Koppen-Geiger 1961-1990, 1 km,
                      figshare 10.6084/m9.figshare.21789074.v2 (koppen_geiger_tif.zip)
                      -> koppen.png, koppen-coarse.png, koppen.json
  grid_10min_pre.dat.gz, grid_10min_tmp.dat.gz   CRU CL 2.0 (New et al. 2002), 10' mean monthly climate,
                      1961-1990 (https://crudata.uea.ac.uk/cru/data/hrg/tmc/)
                      -> climate.json

Sources, licenses and what was refused: sources/indochina/README.md.
"""
import gzip, json, math, os, re, struct, sys, zlib
import numpy as np

W0, E0, S0, N0 = 100.0, 110.5, 8.0, 23.5
DL, OUT = sys.argv[1], sys.argv[2]


def merc_y(lat):
    return np.log(np.tan(np.pi / 4 + np.radians(lat) / 2))


def merc_lat(y):
    return np.degrees(2 * np.arctan(np.exp(y)) - np.pi / 2)


def merc_grid(width):
    """Column centre lons and row centre lats of a W-wide raster in Mercator rows over the bounds."""
    x0, x1 = math.radians(W0), math.radians(E0)
    y0, y1 = float(merc_y(S0)), float(merc_y(N0))
    height = int(round(width * (y1 - y0) / (x1 - x0)))
    lons = W0 + (np.arange(width) + 0.5) * (E0 - W0) / width
    ys = y1 - (np.arange(height) + 0.5) * (y1 - y0) / height
    return lons, merc_lat(ys), (y1 - y0) / height


def sample(grid, glat, glon, lats, lons, nearest=False):
    """Sample a lat/lon grid (cell centres glat ascending or descending, glon ascending) at lats x lons."""
    if glat[0] > glat[-1]:
        grid, glat = grid[::-1], glat[::-1]
    fi = np.interp(lats, glat, np.arange(len(glat)))
    fj = np.interp(lons, glon, np.arange(len(glon)))
    if nearest:
        return grid[np.rint(fi).astype(int)][:, np.rint(fj).astype(int)]
    i0 = np.clip(np.floor(fi).astype(int), 0, len(glat) - 2); ti = (fi - i0)[:, None]
    j0 = np.clip(np.floor(fj).astype(int), 0, len(glon) - 2); tj = (fj - j0)[None, :]
    a = grid[i0][:, j0]; b = grid[i0][:, j0 + 1]; c = grid[i0 + 1][:, j0]; d = grid[i0 + 1][:, j0 + 1]
    return (a * (1 - tj) + b * tj) * (1 - ti) + (c * (1 - tj) + d * tj) * ti


def write_png(path, arr, mode, palette=None, transparent=None):
    """Write a PNG with zlib alone: mode 'L', 'LA' or 'P' (palette: list of (r,g,b); transparent: alpha list)."""
    h, w = arr.shape[:2]
    ctype = {'L': 0, 'LA': 4, 'P': 3}[mode]
    raw = np.ascontiguousarray(arr.astype(np.uint8)).reshape(h, -1)
    data = b''.join(b'\x00' + raw[r].tobytes() for r in range(h))
    if mode in ('L', 'LA'):  # the 'up' filter on every row but the first: smaller shaded rasters
        rows = raw.astype(np.int16)
        up = np.vstack([rows[:1], (rows[1:] - rows[:-1]) % 256]).astype(np.uint8)
        data = b''.join((b'\x00' if r == 0 else b'\x02') + up[r].tobytes() for r in range(h))

    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    out = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, ctype, 0, 0, 0))
    if mode == 'P':
        out += chunk(b'PLTE', bytes(v for c in palette for v in c))
        if transparent is not None:
            out += chunk(b'tRNS', bytes(transparent))
    out += chunk(b'IDAT', zlib.compress(data, 9)) + chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(out)
    return len(out)


def smooth(a, sigma):
    """Separable Gaussian blur (numpy only)."""
    r = int(3 * sigma) + 1
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2); k /= k.sum()
    p = np.pad(a, r, mode='edge')
    p = np.apply_along_axis(lambda v: np.convolve(v, k, 'valid'), 0, p)
    return np.apply_along_axis(lambda v: np.convolve(v, k, 'valid'), 1, p)


# ---------------------------------------------------------------- land mask (Natural Earth 10m land)

def land_mask(lons, lats):
    import shapefile
    from PIL import Image, ImageDraw
    w, h = len(lons), len(lats)
    y0, y1 = float(merc_y(S0)), float(merc_y(N0))
    im = Image.new('L', (w, h), 0); d = ImageDraw.Draw(im)
    r = shapefile.Reader(os.path.join(DL, 'ne/ne_10m_land.shp'))

    def px(pt):
        lon, lat = pt
        lat = max(-85, min(85, lat))
        return ((lon - W0) / (E0 - W0) * w, (y1 - float(merc_y(lat))) / (y1 - y0) * h)
    for shp in r.iterShapes():
        b = shp.bbox
        if b[2] < W0 or b[0] > E0 or b[3] < S0 or b[1] > N0:
            continue
        parts = list(shp.parts) + [len(shp.points)]
        for k in range(len(parts) - 1):
            ring = shp.points[parts[k]:parts[k + 1]]
            # outer rings are clockwise in shapefiles; holes counter-clockwise
            area = sum(x0 * y1_ - x1_ * y0_ for (x0, y0_), (x1_, y1_) in zip(ring, ring[1:]))
            d.polygon([px(p) for p in ring], fill=255 if area < 0 else 0)
    return np.array(im) > 127


# ---------------------------------------------------------------- relief

def read_dods(path):
    b = open(path, 'rb').read()
    k = b.index(b'\nData:\n') + 7
    dds = b[:k].decode()
    ny, nx = map(int, re.search(r'z\[lat = (\d+)\]\[lon = (\d+)\]', dds).groups())
    n = struct.unpack('>I', b[k:k + 4])[0]; assert n == ny * nx
    k += 8
    z = np.frombuffer(b, '>f4', n, k).reshape(ny, nx).astype(np.float64); k += 4 * n
    k += 8; lat = np.frombuffer(b, '>f8', ny, k).copy(); k += 8 * ny
    k += 8; lon = np.frombuffer(b, '>f8', nx, k).copy()
    return z, lat, lon


BANDS = [  # (lower bound m, label, color); land
    (None, '0–100 m', (172, 208, 165)), (100, '100–200 m', (196, 222, 172)), (200, '200–500 m', (225, 228, 181)),
    (500, '500–1,000 m', (232, 214, 164)), (1000, '1,000–1,500 m', (219, 188, 138)),
    (1500, '1,500–2,000 m', (198, 160, 120)), (2000, '2,000 m and over', (172, 134, 108))]
DEPTHS = [  # sea, by depth below sea level
    (0, '0–50 m deep', (216, 234, 244)), (50, '50–200 m deep', (198, 223, 240)),
    (200, '200–1,000 m deep', (170, 205, 232)), (1000, '1,000–2,000 m deep', (145, 188, 223)),
    (2000, '2,000–4,000 m deep', (122, 171, 214)), (4000, '4,000 m and deeper', (101, 154, 205))]


def hillshade(z, lats, dlon, dy, zfac, az=315.0, alt=45.0):
    """Hillshade of a Mercator-row grid; ground spacing in metres from the row's latitude."""
    R = 6371008.8
    cos = np.cos(np.radians(lats))[:, None]
    dx_m = np.radians(dlon) * R * cos
    dy_m = dy * R * cos  # Mercator row step times cos(lat) = ground metres
    zz = np.pad(z * zfac, 1, mode='edge')
    gx = ((zz[1:-1, 2:] - zz[1:-1, :-2]) / 2) / dx_m
    gy = ((zz[:-2, 1:-1] - zz[2:, 1:-1]) / 2) / dy_m  # north minus south
    a, h = np.radians(az), np.radians(alt)
    # the surface normal (-gx, -gy, 1) against the light (sin a cos h, cos a cos h, sin h): east, north, up
    return (-gx * np.sin(a) * np.cos(h) - gy * np.cos(a) * np.cos(h) + np.sin(h)) / np.sqrt(1 + gx * gx + gy * gy)


def read_15s():
    """The four 15-arc-second tiles' subsets, mosaicked: lat 8-23.5 ascending, lon 100-110.5."""
    t = {k: read_dods(os.path.join(DL, f'e15_{k}.dods')) for k in ('N15E090', 'N15E105', 'N30E090', 'N30E105')}
    south = np.hstack([t['N15E090'][0], t['N15E105'][0]])
    north = np.hstack([t['N30E090'][0], t['N30E105'][0]])
    z = np.vstack([south, north])
    glat = np.concatenate([t['N15E090'][1], t['N30E090'][1]])
    glon = np.concatenate([t['N15E090'][2], t['N15E105'][2]])
    assert np.allclose(np.diff(glat), 1 / 240) and np.allclose(np.diff(glon), 1 / 240)
    assert abs(glat[0] - (S0 + 1 / 480)) < 1e-6 and abs(glon[-1] - (E0 - 1 / 480)) < 1e-6
    return z, glat, glon


def relief():
    z, glat, glon = read_dods(os.path.join(DL, 'etopo30s.dods'))
    assert abs(glat[0] - (S0 + 1 / 240)) < 1e-6 and abs(glon[0] - (W0 + 1 / 240)) < 1e-6
    z15 = read_15s()
    meta = {}
    for name, width, zfac, sig in (('-fine', 2520, 1.5, 0.0), ('', 1260, 2.0, 0.0), ('-coarse', 630, 3.0, 0.6)):
        lons, lats, dy = merc_grid(width)
        zm = sample(*(z15 if width == 2520 else (z, glat, glon)), lats, lons)
        land = land_mask(lons, lats)
        zs = smooth(zm, sig) if sig else zm
        hs = hillshade(np.where(land, np.maximum(zs, 0), 0), lats, (E0 - W0) / width, dy, zfac)
        flat = math.cos(math.radians(45))
        # gray = the shade, alpha = how far it is from the flat value; sea transparent
        g = np.clip(hs, 0, 1)
        dev = g - flat
        gray = np.where(dev < 0, 0, 255)
        alpha = np.clip(np.where(dev < 0, -dev / flat * 1.25, dev / (1 - flat) * 0.9), 0, 1) * 255
        alpha = np.where(land, np.rint(alpha / 8) * 8, 0).clip(0, 255)  # 32 levels: smaller files
        la = np.dstack([gray, alpha]).astype(np.uint8)
        s1 = write_png(os.path.join(OUT, f'hillshade{name}.png'), la, 'LA')
        if width == 2520:
            meta['fine15'] = {'width': width, 'height': len(lats), 'hillshade_bytes': s1}
            print('fine', width, len(lats), s1)
            continue
        # bands
        cls = np.zeros(zm.shape, np.uint8)
        for k, (lo, _, _) in enumerate(BANDS):
            if lo is not None:
                cls[(zm >= lo) & land] = k
        for k, (lo, _, _) in enumerate(DEPTHS):
            cls[(~land) & (-zm >= lo)] = len(BANDS) + k
        cls[(~land) & (zm > 0)] = len(BANDS)
        pal = [c for _, _, c in BANDS] + [c for _, _, c in DEPTHS]
        s2 = write_png(os.path.join(OUT, f'hypso{name}.png'), cls, 'P', pal)
        meta[name or 'fine'] = {'width': width, 'height': len(lats), 'hillshade_bytes': s1, 'hypso_bytes': s2}
        print(name or 'fine', width, len(lats), s1, s2)
    legend = {
        'bounds': {'west': W0, 'east': E0, 'south': S0, 'north': N0},
        'rows': 'evenly spaced in Web Mercator (EPSG:3857) y; columns evenly spaced in longitude',
        'files': {'hypso.png': [1260, meta['fine']['height']], 'hypso-coarse.png': [630, meta['-coarse']['height']]},
        'classes': [{'index': k, 'kind': 'land', 'from_m': lo or 0,
                     'to_m': (BANDS[k + 1][0] if k + 1 < len(BANDS) else None), 'label': lab,
                     'color': '#%02x%02x%02x' % c} for k, (lo, lab, c) in enumerate(BANDS)]
        + [{'index': len(BANDS) + k, 'kind': 'sea', 'depth_from_m': lo,
            'depth_to_m': (DEPTHS[k + 1][0] if k + 1 < len(DEPTHS) else None), 'label': lab,
            'color': '#%02x%02x%02x' % c} for k, (lo, lab, c) in enumerate(DEPTHS)],
        'note': 'Land and sea from Natural Earth 10m land; land below 0 m (ETOPO) counted 0-100 m; sea above 0 m '
                'counted 0-50 m deep. Palette index = class index.'}
    json.dump(legend, open(os.path.join(OUT, 'hypso.json'), 'w'), ensure_ascii=False, indent=1)
    contours(z, glat, glon)


def contours(z, glat, glon):
    import contourpy
    from shapely.geometry import LineString
    from shapely import simplify
    zs = smooth(z, 1.0)
    gen = contourpy.contour_generator(glon, glat, zs, line_type='Separate')
    feats = []
    for lev in (500, 1000, 1500, 2000):
        lines = []
        for seg in gen.lines(lev):
            if len(seg) < 2:
                continue
            ls = simplify(LineString(seg), 0.004, preserve_topology=False)
            if ls.length < 0.03:  # drop rings and stubs under ~3 km
                continue
            lines.append([[round(x, 3), round(y, 3)] for x, y in ls.coords])
        feats.append({'type': 'Feature', 'properties': {'elev_m': lev},
                      'geometry': {'type': 'MultiLineString', 'coordinates': lines}})
        print('contour', lev, len(lines), sum(len(l) for l in lines))
    fc = {'type': 'FeatureCollection', 'name': 'contours',
          'source': 'ETOPO 2022 v1 30s, Gaussian-smoothed (sigma 1 cell), simplified 0.004 deg, stubs < 0.03 deg dropped',
          'features': feats}
    with open(os.path.join(OUT, 'contours.geojson'), 'w') as f:
        json.dump(fc, f, separators=(',', ':'))


# ---------------------------------------------------------------- rivers and lakes

# The Mekong delta and the Saigon lowlands: HydroRIVERS, drawn from a flow-direction grid, cannot split a river, so
# it sends the whole Mekong down one channel and draws flow paths across the flat delta that are not rivers. Inside
# this ring the rivers are SWORD's reaches (mapped from Landsat, every channel 30 m wide or more); outside, HydroRIVERS.
DELTA = [(104.70, 11.80), (105.95, 11.80), (106.45, 11.20), (106.60, 10.86), (106.95, 10.80), (107.15, 10.40),
         (107.15, 8.40), (104.70, 8.40)]

# size, for drawing: 1 the largest. HydroRIVERS by long-term mean discharge (DIS_AV_CMS, m3/s); SWORD by width (m).
DIS = [5000, 1000, 300, 100, 30, 10]
WID = [900, 400, 200, 100, 50, 0]

# Vietnamese forms of names SWORD gives in English, for rivers wholly or partly in Vietnam. Only where the form is
# certain; others keep SWORD's name alone.
VI = {'Perfume River': 'Hương', 'Saigon River': 'Sài Gòn', 'Dong Nai River': 'Đồng Nai', 'Bassac': 'Hậu',
      'Red River': 'Hồng', 'Black River': 'Đà', 'Lo River': 'Lô', 'Chay River': 'Chảy', 'Gam River': 'Gâm',
      'Day River': 'Đáy', 'Ky Cung River': 'Kỳ Cùng', 'Ma River': 'Mã', 'Lam River': 'Lam (Cả)', 'Gianh River': 'Gianh',
      'Song Be': 'Bé', 'Vu Gia River': 'Vu Gia', 'Sesan River': 'Sê San', 'Srepok River': 'Srêpốk',
      'Ayun River': 'Ayun', 'Mekong River': 'Mê Kông', 'Mekong': 'Mê Kông', 'Chu River': 'Chu',
      'Pho Day River': 'Phó Đáy', 'Cong River': 'Công', 'Truong Giang River': 'Trường Giang', 'Tranh River': 'Tranh',
      'A Vuong River': 'A Vương', 'Cam Le River': 'Cẩm Lệ', 'Kon River': 'Kôn', 'Hinh River': 'Hinh', 'Bo River': 'Bồ'}

# Rivers SWORD does not name, traced on HydroRIVERS: the main stem (largest upstream area at each fork) from the
# segment nearest a point, down to the sea and up to the source. Points from sources/vn-provinces-1966/places.json
# (Wikipedia's coordinates): the Ben Hai's mouth; Quang Tri town, on the Thach Han.
HAND = [('Ben Hai River', 'Bến Hải', 17.015, 107.1125, 100), ('Thach Han River', 'Thạch Hãn', 16.7469, 107.194, 1000)]


# rivers that keep their names to the sea: whatever lies downstream of a segment so named is that river
TO_SEA = {'Red River', 'Mekong River', 'Ma River', 'Lam River', 'Gianh River', 'Perfume River', 'Chao Phraya River'}
SAME = {'Mekong': 'Mekong River', 'Nam Theun River': 'Nam Theun'}  # one river, two spellings in SWORD


def fill_runs(segs, down_of, reach=250):
    """Walk down from each segment named N through segments unnamed or otherwise named; where the walk comes back
    to N within `reach` steps, the segments walked are N's trunk: name them N (a gap in the source's names, or a
    stretch it gives a tributary's name)."""
    for k in list(segs):
        n = segs[k]['name']
        if not n:
            continue
        path, cur = [], k
        for _ in range(reach):
            d = down_of(cur)
            if not d:
                break
            cur = d[0]
            if segs[cur]['name'] == n:
                for x in path:
                    segs[x]['name'] = n
                break
            path.append(cur)


def size_of(v, steps):
    for k, t in enumerate(steps):
        if v >= t:
            return k + 1
    return len(steps) + 1


def hydro():
    import shapefile
    from shapely.geometry import LineString, Polygon, box, Point
    from shapely.ops import linemerge
    from shapely.strtree import STRtree
    from shapely import simplify
    ext = box(W0, S0, E0, N0)
    zone = Polygon(DELTA)

    def inbox(b):
        return not (b[2] < W0 or b[0] > E0 or b[3] < S0 or b[1] > N0)

    # SWORD reaches in the extent
    sw = {}
    for hb in (43, 44):
        r = shapefile.Reader(os.path.join(DL, f'sword/shp/as_sword_reaches_hb{hb}_v17c.shp'))
        for rec, shp in zip(r.iterRecords(), r.iterShapes()):
            if not inbox(shp.bbox) or len(shp.points) < 2:
                continue
            nm = rec['river_name']
            nm = None if nm in ('NODATA', '', None) else nm.split(';')[0].strip()
            nm = SAME.get(nm, nm)
            sw[rec['reach_id']] = dict(g=LineString(shp.points), name=nm, width=float(rec['width']),
                                      dn=[rec[f'rid_dn_{i}'] for i in (1, 2, 3, 4) if rec[f'rid_dn_{i}']],
                                      up=[rec[f'rid_up_{i}'] for i in (1, 2, 3, 4) if rec[f'rid_up_{i}']])
    sw_named = [(v['g'], v['name']) for v in sw.values() if v['name']]
    named = sw_named
    tree = STRtree([s[0] for s in named])
    print('sword', len(sw), 'named', len(named))
    fill_runs(sw, lambda k: [d for d in sw[k]['dn'] if d in sw][:1] if len(sw[k]['dn']) == 1 else [])
    for k, v in sw.items():  # the Mekong and the Bassac down to the sea, through unnamed reaches, by the widest
        if v['name'] not in ('Mekong River', 'Bassac') or not zone.intersects(v['g']):  # branch of a split
            continue
        cur, w = k, v['width']
        for _ in range(200):
            dn = [d for d in sw[cur]['dn'] if d in sw]
            if not dn:
                break
            nxt = max(dn, key=lambda d: sw[d]['width'])
            if sw[nxt]['name'] or sw[nxt]['width'] < 0.5 * w:
                break
            sw[nxt]['name'] = v['name']; cur = nxt

    # HydroRIVERS segments in the extent, 10 m3/s and over
    hr = {}
    r = shapefile.Reader(os.path.join(DL, 'hr/HydroRIVERS_v10_as_shp/HydroRIVERS_v10_as.shp'))
    for rec, shp in zip(r.iterRecords(), r.iterShapes()):
        if not inbox(shp.bbox):
            continue
        hr[rec['HYRIV_ID']] = dict(g=LineString(shp.points), down=rec['NEXT_DOWN'], up_area=rec['UPLAND_SKM'],
                                   dis=rec['DIS_AV_CMS'], main=rec['MAIN_RIV'], name=None, vi=None)
    ups = {}
    for k, s in hr.items():
        ups.setdefault(s['down'], []).append(k)

    def main_up(k):  # the main stem upward
        out = []
        while True:
            u = ups.get(k)
            if not u:
                return out
            k = max(u, key=lambda x: hr[x]['up_area']); out.append(k)

    def down(k):
        out = []
        while k in hr and hr[k]['down'] in hr:
            k = hr[k]['down']; out.append(k)
        return out

    # names from SWORD: two of three points along the segment within ~1 km of reaches of one name
    for k, s in hr.items():
        if s['dis'] < 10:
            continue
        votes = {}
        for f in (0.2, 0.5, 0.8):
            p = s['g'].interpolate(f, normalized=True)
            i = tree.nearest(p)
            if named[i][0].distance(p) < 0.01:
                votes[named[i][1]] = votes.get(named[i][1], 0) + 1
        best = max(votes.items(), key=lambda kv: kv[1]) if votes else None
        if best and best[1] >= 2:
            s['name'] = best[0]
    fill_runs(hr, lambda k: [hr[k]['down']] if hr[k]['down'] in hr else [])
    for k in [k for k, s in hr.items() if s['name'] in TO_SEA]:
        for x in down(k):
            hr[x]['name'] = hr[k]['name']
    # a name on fewer than three segments of a main river is a stray (a tributary's mouth beside the trunk)
    count = {}
    for s in hr.values():
        if s['name']:
            count[(s['main'], s['name'])] = count.get((s['main'], s['name']), 0) + 1
    for s in hr.values():
        if s['name'] and count[(s['main'], s['name'])] < 3:
            s['name'] = None
    for s in hr.values():
        if s['name']:
            s['vi'] = VI.get(s['name'])
    # hand traces
    for name, vi, lat, lon, min_area in HAND:
        p = Point(lon, lat)
        cand = [k for k, s in hr.items() if s['up_area'] >= min_area and s['g'].distance(p) < 0.05]
        k = min(cand, key=lambda x: hr[x]['g'].distance(p))
        mouth = ([k] + down(k))[-1]
        for x in [mouth] + main_up(mouth):
            hr[x]['name'], hr[x]['vi'] = name, vi
        print('hand', name, 'segments', 1 + len(main_up(mouth)))

    feats = {'fine': [], 'coarse': []}

    def emit(lines, props, tol_f, tol_c, coarse):
        g = linemerge(lines) if len(lines) > 1 else lines[0]
        for which, tol in (('fine', tol_f), ('coarse', tol_c)):
            if which == 'coarse' and not coarse:
                continue
            gs = simplify(g, tol, preserve_topology=False)
            parts = list(gs.geoms) if hasattr(gs, 'geoms') else [gs]
            coords = []
            for ln in parts:
                if ln.is_empty or ln.length < (0 if which == 'fine' else 0.02):
                    continue
                cs = [[round(x, 3), round(y, 3)] for x, y in ln.coords]
                cs = [c for i, c in enumerate(cs) if i == 0 or c != cs[i - 1]]
                if len(cs) > 1:
                    coords.append(cs)
            if coords:
                feats[which].append({'type': 'Feature', 'properties': props,
                                     'geometry': {'type': 'MultiLineString', 'coordinates': coords}})

    # HydroRIVERS outside the delta ring
    groups = {}
    for k, s in hr.items():
        if s['dis'] < 10 and not s['name']:
            continue
        g = s['g'].difference(zone).intersection(ext)
        if g.is_empty:
            continue
        sz = size_of(s['dis'], DIS)
        key = (s['name'], s['vi'], sz)
        groups.setdefault(key, []).extend(list(g.geoms) if hasattr(g, 'geoms') else [g])
    for (name, vi, sz), lines in sorted(groups.items(), key=lambda kv: (kv[0][2], kv[0][0] or '')):
        props = {'size': sz, 'source': 'HydroRIVERS'}
        if name:
            props['name'] = name
        if vi:
            props['name_vi'] = vi
        emit(lines, props, 0.002, 0.008, sz <= 4 or (name is not None and sz <= 5))
    # SWORD inside the delta ring
    groups = {}
    for v in sw.values():
        name, width = v['name'], v['width']
        g = v['g'].intersection(zone).intersection(ext)
        if g.is_empty:
            continue
        sz = size_of(width, WID)
        vi = VI.get(name) if name else None
        if name == 'Mekong River' and v['g'].centroid.y < 10.93:  # below the Cambodian border: the Tien
            vi = 'Tiền'
        key = (name, vi, sz)
        groups.setdefault(key, []).extend(list(g.geoms) if hasattr(g, 'geoms') else [g])
    for (name, vi, sz), lines in sorted(groups.items(), key=lambda kv: (kv[0][2], kv[0][0] or '')):
        props = {'size': sz, 'source': 'SWORD'}
        if name:
            props['name'] = name
        if vi:
            props['name_vi'] = vi
        emit(lines, props, 0.002, 0.008, sz <= 3)
    for which, fn in (('fine', 'rivers.geojson'), ('coarse', 'rivers-coarse.geojson')):
        fs = sorted(feats[which], key=lambda f: -f['properties']['size'])  # small first, so large draw on top
        fc = {'type': 'FeatureCollection', 'name': fn[:-8], 'features': fs}
        with open(os.path.join(OUT, fn), 'w') as f:
            json.dump(fc, f, ensure_ascii=False, separators=(',', ':'))
        print(fn, len(fs), os.path.getsize(os.path.join(OUT, fn)))


def lakes():
    import shapefile
    from shapely.geometry import shape, mapping, box
    from shapely import simplify
    ext = box(W0, S0, E0, N0)
    years = []  # GRanD dams: (lon, lat, year, capacity mcm), from Res.Grand.txt
    for line in open(os.path.join(DL, 'grand/Res.Grand.txt')):
        v = line.split()
        if len(v) >= 6:
            years.append((float(v[4]), float(v[5]), int(v[3]), float(v[1])))
    r = shapefile.Reader(os.path.join(DL, 'hl/HydroLAKES_polys_v10_shp/HydroLAKES_polys_v10.shp'),
                         encoding='latin-1')  # no .cpg; names with cp1252 bytes
    out = []
    for sr in r.iterShapeRecords(bbox=(W0, S0, E0, N0)):
        rec, shp = sr.record, sr.shape
        if rec['Lake_area'] < 1.0:
            continue
        g = shape(shp.__geo_interface__).intersection(ext)
        if g.is_empty:
            continue
        g = simplify(g, 0.001, preserve_topology=True)
        props = {'id': rec['Hylak_id'], 'area_km2': round(rec['Lake_area'], 1),
                 'type': {1: 'lake', 2: 'reservoir', 3: 'lake control'}.get(rec['Lake_type'])}
        if rec['Lake_name']:
            props['name'] = rec['Lake_name']
        # GRanD's year for a dam within ~2 km of the water body (HydroLAKES types as 'lake' many reservoirs of
        # the 1970s-90s, Dau Tieng among them); of several, the largest by capacity
        from shapely.geometry import Point
        gb = g.bounds
        near = [(cap, yr) for x, y, yr, cap in years if gb[0] - 0.03 < x < gb[2] + 0.03 and gb[1] - 0.03 < y < gb[3] + 0.03
                and yr > 0 and g.distance(Point(x, y)) < 0.02]
        if near:
            props['dam_year'] = max(near)[1]
        gj = mapping(g)

        def rnd(c):
            return [rnd(x) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], 4), round(c[1], 4)]
        gj = {'type': gj['type'], 'coordinates': rnd(gj['coordinates'])}
        out.append({'type': 'Feature', 'properties': props, 'geometry': gj})
    out.sort(key=lambda f: -f['properties']['area_km2'])
    fc = {'type': 'FeatureCollection', 'name': 'lakes', 'features': out}
    with open(os.path.join(OUT, 'lakes.geojson'), 'w') as f:
        json.dump(fc, f, ensure_ascii=False, separators=(',', ':'))
    print('lakes', len(out), os.path.getsize(os.path.join(OUT, 'lakes.geojson')))
    for f in out[:25]:
        print('  ', f['properties'])


# ---------------------------------------------------------------- Koppen-Geiger, 1961-1990 (Beck et al. 2023)

def koppen():
    import rasterio
    from rasterio.windows import from_bounds
    leg = {}
    for line in open(os.path.join(DL, 'kg/legend.txt'), encoding='utf-8'):
        m = re.match(r'\s*(\d+):\s+(\S+)\s+(.+?)\s+\[(\d+) (\d+) (\d+)\]', line)
        if m:
            leg[int(m[1])] = (m[2], m[3], tuple(int(m[k]) for k in (4, 5, 6)))
    with rasterio.open(os.path.join(DL, 'kg/1961_1990/koppen_geiger_0p00833333.tif')) as s:
        win = from_bounds(W0, S0, E0, N0, s.transform).round_offsets().round_lengths()
        a = s.read(1, window=win)
        t = s.window_transform(win)
    glon = t.c + (np.arange(a.shape[1]) + 0.5) * t.a
    glat = t.f + (np.arange(a.shape[0]) + 0.5) * t.e
    present = sorted(int(v) for v in np.unique(a) if v)
    # palette index 0 transparent (sea, no data); then the classes present, in the legend's order
    pal = [(0, 0, 0)] + [leg[v][2] for v in present]
    lut = np.zeros(256, np.uint8)
    for k, v in enumerate(present):
        lut[v] = k + 1
    sizes = {}
    for name, width in (('', 1260), ('-coarse', 630)):
        lons, lats, _ = merc_grid(width)
        idx = lut[sample(a, glat, glon, lats, lons, nearest=True)]
        sizes[name] = write_png(os.path.join(OUT, f'koppen{name}.png'), idx, 'P', pal, [0] + [255] * len(present))
        print('koppen', name or 'fine', idx.shape, sizes[name])
    counts = {int(v): int((a == v).sum()) for v in present}
    land = sum(counts.values())
    legend = {
        'source': 'Beck et al. (2023), Koppen-Geiger classes for 1961-1990, 0.00833 deg (1 km); '
                  'figshare doi:10.6084/m9.figshare.21789074.v2 (Jan. 2026 correction), CC BY 4.0',
        'bounds': {'west': W0, 'east': E0, 'south': S0, 'north': N0},
        'rows': 'evenly spaced in Web Mercator (EPSG:3857) y; columns evenly spaced in longitude; nearest-neighbour',
        'transparent': 'palette index 0: sea or no data',
        'classes': [{'index': k + 1, 'value': v, 'code': leg[v][0], 'name': leg[v][1],
                     'color': '#%02x%02x%02x' % leg[v][2], 'share_of_land_in_extent': round(counts[v] / land, 4)}
                    for k, v in enumerate(present)]}
    json.dump(legend, open(os.path.join(OUT, 'koppen.json'), 'w'), ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- CRU CL 2.0 monthly normals, 1961-1990

def climate():
    def read(fn, nvals):
        out = {}
        with gzip.open(os.path.join(DL, fn), 'rt') as f:
            for line in f:
                lat = float(line[0:9]); lon = float(line[9:18])
                if S0 < lat < N0 and W0 < lon < E0:
                    out[(lat, lon)] = [float(line[18 + 7 * k:25 + 7 * k]) for k in range(nvals)]
        return out
    pre = read('grid_10min_pre.dat.gz', 12)  # the 12 CVs after the means are not read
    tmp = read('grid_10min_tmp.dat.gz', 12)
    step = 1 / 6
    ncol, nrow = int(round((E0 - W0) / step)), int(round((N0 - S0) / step))

    def key(r, c):  # row 0 at the north
        return (round(N0 - (r + 0.5) * step, 3), round(W0 + (c + 0.5) * step, 3))
    keys = set(pre) | set(tmp)
    assert all(k in {key(r, c) for r in range(nrow) for c in range(ncol)} for k in keys), 'grid mismatch'
    P = [[[None] * ncol for _ in range(nrow)] for _ in range(12)]
    T = [[[None] * ncol for _ in range(nrow)] for _ in range(12)]
    for r in range(nrow):
        for c in range(ncol):
            k = key(r, c)
            for m in range(12):
                if k in pre:
                    P[m][r][c] = int(round(pre[k][m]))
                if k in tmp:
                    T[m][r][c] = int(round(tmp[k][m] * 10))
    doc = {
        'source': 'CRU CL 2.0 (New, Lister, Hulme and Makin 2002, Climate Research 21:1-25), 10-minute mean monthly '
                  'climate, 1961-1990, land only; https://crudata.uea.ac.uk/cru/data/hrg/tmc/; Open Database License',
        'bounds': {'west': W0, 'east': E0, 'south': S0, 'north': N0},
        'projection': 'plain lon/lat (EPSG:4326) cells, equal steps in degrees',
        'cell_deg': step, 'ncols': ncol, 'nrows': nrow,
        'order': 'arrays [month 0-11, Jan-Dec][row, north to south][col, west to east]; cell (r, c) spans lat '
                 'north - r*cell_deg .. north - (r+1)*cell_deg, lon west + c*cell_deg .. west + (c+1)*cell_deg; '
                 'null = sea or no data',
        'precipitation': {'units': 'mm/month', 'rounding': 'whole mm', 'values': P},
        'temperature': {'units': 'tenths of a degree C (divide by 10)', 'values': T}}
    with open(os.path.join(OUT, 'climate.json'), 'w') as f:
        json.dump(doc, f, separators=(',', ':'))
    print('climate', nrow, ncol, len(pre), len(tmp), os.path.getsize(os.path.join(OUT, 'climate.json')))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    steps = sys.argv[3:] or ['relief', 'hydro', 'lakes', 'koppen', 'climate']
    for s in steps:
        globals()[s]()
