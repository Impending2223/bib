"""Population density for the maps of Indochina, 1960 and 1970 (Oct. 22, 2026): modelled, and made later. A one-time
script:

    python3 -I tools/vnmap/population.py ISIMIP_NC

ISIMIP_NC is ISIMIP3a's gridded historical population, population_histsoc_5arcmin_annual_1901_2021.nc, from
https://files.isimip.org/ISIMIP3a/InputData/socioeconomic/pop/histsoc/ (downloaded Oct. 22, 2026; 1.37 GB; the ISIMIP
site's content CC BY 4.0). ISIMIP's page for the data set (isimip.org, input data, details/79) says its national and
gridded population is "taken from the History Database of the Global Environment (HYDE) version 3.2.1"; the file's
own header cites Klein Goldewijk et al., "Anthropogenic land use estimates for the Holocene - HYDE 3.2", Earth Syst.
Sci. Data 9 (2017) 927-953, and HYDE 3.3 (doi:10.24416/UU01-67UHB4). HYDE's own host (geo.public.data.uu.nl) answers
with a bot check here and was not used. A count of people a 5' cell (about 9 km), modelled from national totals and
later maps: not a census.

Writes sources/indochina/population.geojson: for 1960 (band 60) and 1970 (band 70), each cell's count over its
geodesic area (pyproj.Geod), in persons a km2, put in CLASSES and traced as polygons (rasterio.features.shapes;
simplified as a coverage at 0.004 degrees, so neighbours still meet), one feature a class and year:
{"y": 1960, "c": k}; k indexes CLASSES (the lower bound of the class).
"""
import json
import os
import sys

import numpy as np
import rasterio
import rasterio.features
import rasterio.windows
import shapely
from pyproj import Geod

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "sources", "indochina")
FRAME = (97.5, 5.5, 113.0, 26.0)          # base.FRAME
CLASSES = [0, 1, 10, 25, 50, 100, 250, 500, 1000]     # persons a km2: 0-1, 1-10, ..., 1,000 and over
BANDS = {1960: 60, 1970: 70}              # time = years since 1850; band 1 is 1901


def rnd(c, p=3):
    return [rnd(x, p) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], p), round(c[1], p)]


def main():
    nc = sys.argv[1]
    geod = Geod(ellps="WGS84")
    feats = []
    with rasterio.open(f'NETCDF:"{nc}":total-population') as r:
        tr = r.transform                   # 1/12 degree, from -180, 90 (the file carries no CRS: plain lon/lat)
        win = rasterio.windows.from_bounds(*FRAME, transform=tr).round_offsets().round_lengths()
        wtr = rasterio.windows.transform(win, tr)
        h, w = int(win.height), int(win.width)
        # each row's cell area, km2
        area = np.empty(h)
        for i in range(h):
            top = wtr.f + wtr.e * i
            lons = [wtr.c, wtr.c + wtr.a, wtr.c + wtr.a, wtr.c]
            lats = [top, top, top + wtr.e, top + wtr.e]
            area[i] = abs(geod.polygon_area_perimeter(lons, lats)[0]) / 1e6
        for year, band in BANDS.items():
            assert r.tags(band)["NETCDF_DIM_time"] == str(year - 1850), r.tags(band)
            pop = r.read(band, window=win).astype(np.float64)
            pop[pop > 1e19] = np.nan
            dens = pop / area[:, None]
            cls = np.full(dens.shape, -1, np.int16)
            ok = np.isfinite(dens)
            cls[ok] = np.digitize(dens[ok], CLASSES[1:])
            gs, vals = [], []
            for geom, v in rasterio.features.shapes(cls, mask=cls >= 0, transform=wtr):
                gs.append(shapely.geometry.shape(geom))
                vals.append(int(v))
            simp = shapely.coverage_simplify(np.array(gs, dtype=object), 0.004)
            by = {}
            for g, v in zip(simp, vals):
                by.setdefault(v, []).append(g)
            for v in sorted(by):
                m = shapely.geometry.mapping(shapely.union_all(by[v]))
                feats.append({"type": "Feature", "properties": {"y": year, "c": v},
                              "geometry": {"type": m["type"], "coordinates": rnd(m["coordinates"])}})
            tot = np.nansum(pop)
            print(year, "cells", int(ok.sum()), "people in the frame", int(tot))
    s = json.dumps({"type": "FeatureCollection", "features": feats}, separators=(",", ":"))
    open(os.path.join(OUT, "population.geojson"), "w", encoding="utf-8").write(s + "\n")
    print("population.geojson", len(s), "bytes")


if __name__ == "__main__":
    main()
