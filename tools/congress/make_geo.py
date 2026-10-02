"""Project, simplify, and dedupe district shapes for the 87th-93rd Congresses -> congress/geo.json

Usage: python3 tools/congress/make_geo.py PATH/TO/congressional-district-boundaries [tolerance]
  (a clone of https://github.com/JeffreyBLewis/congressional-district-boundaries; only the
  GeoJson files covering Congresses 87-93 are needed). Needs shapely and pyproj. Takes ~6 minutes.
"""
import json, glob, re, os, sys
from collections import defaultdict
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
from shapely.ops import unary_union, transform
from pyproj import Transformer
SRC = os.path.join(sys.argv[1] if len(sys.argv) > 1 else '../congressional-district-boundaries', 'GeoJson') + '/'
TOL = float(sys.argv[2]) if len(sys.argv) > 2 else 0.01
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ABBR = dict(Alabama='AL', Alaska='AK', Arizona='AZ', Arkansas='AR', California='CA', Colorado='CO', Connecticut='CT', Delaware='DE',
            Florida='FL', Georgia='GA', Hawaii='HI', Idaho='ID', Illinois='IL', Indiana='IN', Iowa='IA', Kansas='KS', Kentucky='KY',
            Louisiana='LA', Maine='ME', Maryland='MD', Massachusetts='MA', Michigan='MI', Minnesota='MN', Mississippi='MS', Missouri='MO',
            Montana='MT', Nebraska='NE', Nevada='NV', Ohio='OH', Oklahoma='OK', Oregon='OR', Pennsylvania='PA', Tennessee='TN', Texas='TX',
            Utah='UT', Vermont='VT', Virginia='VA', Washington='WA', Wisconsin='WI', Wyoming='WY')
ABBR.update({'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
             'North Dakota': 'ND', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'West Virginia': 'WV'})
# Albers USA, after d3.geoAlbersUsa: scale 1280, translate (480, 300) on a 960x600 frame
L48 = Transformer.from_crs('EPSG:4326', '+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96 +x_0=0 +y_0=0 +ellps=WGS84', always_xy=True)
AK = Transformer.from_crs('EPSG:4326', '+proj=aea +lat_1=55 +lat_2=65 +lat_0=58.5 +lon_0=-154 +x_0=0 +y_0=0 +ellps=WGS84', always_xy=True)
HI = Transformer.from_crs('EPSG:4326', '+proj=aea +lat_1=8 +lat_2=18 +lat_0=19.9 +lon_0=-157 +x_0=0 +y_0=0 +ellps=WGS84', always_xy=True)
R = 6378137.0
def proj(st):
    # origins as in d3.geoAlbersUsa: each inset centered on its own point
    if st == 'AK':
        t, k, cx, cy, ox, oy = AK, 0.35, 480 - 0.307 * 1280, 300 + 0.201 * 1280, -156.0, 58.5
    elif st == 'HI':
        t, k, cx, cy, ox, oy = HI, 1.0, 480 - 0.205 * 1280, 300 + 0.212 * 1280, -160.0, 19.9
    else:
        t, k, cx, cy, ox, oy = L48, 1.0, 480, 300, -96.6, 38.7
    X0, Y0 = t.transform(ox, oy)
    def f(x, y, z=None):
        X, Y = t.transform(x, y)
        return (cx + (X - X0) / R * 1280 * k, cy - (Y - Y0) / R * 1280 * k)
    return f
def ring(coords):
    pts = [(round(x, 1), round(y, 1)) for x, y in coords]
    out = [pts[0]]
    for p in pts[1:]:
        if p != out[-1]: out.append(p)
    if len(out) < 4: return ''
    s = 'M%g %g' % out[0]
    px, py = out[0]
    for x, y in out[1:-1]:
        s += 'l%g %g' % (round(x - px, 1), round(y - py, 1)); px, py = x, y
    return s + 'z'
def path(g):
    polys = [g] if isinstance(g, Polygon) else list(getattr(g, 'geoms', []))
    out = []
    for p in polys:
        if p.area < 0.02: continue
        out.append(ring(p.exterior.coords))
        out += [ring(i.coords) for i in p.interiors if Polygon(i).area > 0.05]
    return ''.join(out)
files = defaultdict(list)
for f in glob.glob(SRC + '*.geojson'):
    m = re.search(r'GeoJson/(.+)_(\d{3})_to_(\d{3})\.geojson$', f)
    files[ABBR.get(m.group(1), m.group(1))].append((int(m.group(2)), int(m.group(3)), f))
shapes = {}       # key -> path
congress = {}     # c -> {st: {district: key}}
cache = {}
def load(f, st):
    if f not in cache:
        g = json.load(open(f)); P = proj(st); feats = defaultdict(list)
        for x in g['features']:
            geom = shape(x['geometry'])
            if not geom.is_valid: geom = geom.buffer(0)
            feats[int(x['properties']['district'])].append(transform(P, geom))
        cache[f] = {d: unary_union(v) for d, v in feats.items()}
    return cache[f]
outline = {}
for c in range(87, 94):
    congress[c] = {}
    for st, lst in files.items():
        if st == 'District Of Columbia': continue
        cov = [x for x in lst if x[0] <= c <= x[1]]
        if st == 'AL' and c == 88:
            cov = [x for x in lst if x[0] <= 87 <= x[1]]
        m = {}
        for a, b, f in cov:
            for d, g in load(f, st).items():
                key = f'{st}-{a}-{b}-{d}' if not (st == 'AL' and c == 88) else 'AL-88-0'
                if st == 'AL' and c == 88:
                    g = unary_union(list(load(f, st).values())); d = 0
                if key not in shapes:
                    shapes[key] = path(g.simplify(TOL, preserve_topology=True))
                m[d] = key
                if st not in outline and c == 87:
                    pass
        congress[c][st] = m
# state outlines from the 87th-Congress pieces
for st, lst in files.items():
    if st == 'District Of Columbia': continue
    cov = [x for x in lst if x[0] <= 87 <= x[1]]
    gs = []
    for a, b, f in cov:
        gs += list(load(f, st).values())
    u = unary_union([g.buffer(0.3) for g in gs]).buffer(-0.3)
    outline[st] = path(u.simplify(TOL, preserve_topology=True))
    rp = u.representative_point(); cen = u.centroid
    outline[st + '@'] = [round(cen.x, 1), round(cen.y, 1)]
os.makedirs(os.path.join(ROOT, 'congress'), exist_ok=True)
json.dump({'shapes': shapes, 'congress': congress, 'states': {k: v for k, v in outline.items() if '@' not in k},
           'centers': {k[:-1]: v for k, v in outline.items() if '@' in k}},
          open(os.path.join(ROOT, 'congress', 'geo.json'), 'w'), separators=(',', ':'))
print(len(shapes), os.path.getsize(os.path.join(ROOT, 'congress', 'geo.json')) / 1e6, 'MB')
