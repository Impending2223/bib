"""Climate for the maps of Indochina (Oct. 22, 2026): the Köppen-Geiger classes as raster tiles, and the monthly rain and
temperature normals as a grid of cells, both GeoJSON, so that MapLibre draws them sharp at every zoom. A one-time
script:

    python3 -I tools/vnmap/climate.py KOPPEN_TIF LEGEND_TXT

KOPPEN_TIF is 1961_1990/koppen_geiger_0p00833333.tif and LEGEND_TXT legend.txt, out of koppen_geiger_tif.zip of
Beck et al. (2023), figshare doi:10.6084/m9.figshare.21789074.v2 (from https://ndownloader.figshare.com/files/61012822,
the address figshare's API gives; CC BY 4.0). The rain and temperature are sources/indochina/climate.json (its README:
CRU CL 2.0, 1961-1990, ODbL), whose grid covers lon 100-110.5, lat 8-23.5 only: CRU's host did not answer on Oct. 22,
2026, so the grid was not widened to the map's frame (notes/leads.md).

Writes, in sources/indochina/:
 - koppen.pmtiles: the classes as raster tiles (paletted PNG, 256 px, zooms 0-7, the paper's colours, the sea
   transparent), resampled from the 1 km lon/lat grid by nearest neighbour (by mode below z7), drawn with nearest
   resampling so each cell stays sharp at any zoom; a class map's boundaries are too intricate to serve as polygons
   (5.8 MB of GeoJSON at a 400 m simplification);
 - koppen.json: the legend (the classes, the paper's colours, each class's share of the frame's land);
 - climate.geojson: one square a land cell of climate.json, {"p1".."p12": mm, "t1".."t12": degrees C}.
"""
import json
import os
import re
import sys

import numpy as np
import rasterio
import rasterio.features
import rasterio.windows
import shapely
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tiles  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "sources", "indochina")
FRAME = (97.5, 5.5, 113.0, 26.0)          # base.FRAME
MAXZ = 7                                  # 256-px tiles: ~1.2 km a pixel at z7, the 1 km grid


def rnd(c, p=4):
    return [rnd(x, p) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], p), round(c[1], p)]


def write(name, obj):
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(s + "\n")
    print(name, len(s), "bytes")


def koppen(tif, legend):
    leg = {}
    for ln in open(legend, encoding="utf-8"):
        m = re.match(r"\s*(\d+):\s+(\S+)\s+(.+?)\s+\[(\d+) (\d+) (\d+)\]", ln)
        if m:
            leg[int(m[1])] = dict(code=m[2], name=m[3], color="#%02x%02x%02x" % tuple(int(m[i]) for i in (4, 5, 6)))
    with rasterio.open(tif) as r:
        win = rasterio.windows.from_bounds(*FRAME, transform=r.transform).round_offsets().round_lengths()
        a = r.read(1, window=win)
        tr = rasterio.windows.transform(win, r.transform)
    vals = [int(v) for v in np.unique(a) if v > 0]
    land = int((a > 0).sum())
    classes = [{"value": v, **leg[v], "share_of_land_in_frame": round(int((a == v).sum()) / land, 4)} for v in vals]
    # a paletted PNG a tile: index 0 transparent (sea), then the classes in order, the paper's colours
    idx = np.zeros(256, np.uint8)
    for i, v in enumerate(vals):
        idx[v] = i + 1
    cls = idx[a]
    pal = [0, 0, 0] + [int(c["color"][k:k + 2], 16) for c in classes for k in (1, 3, 5)]

    def render(t):
        z = tiles.warp(cls, tr, t, 256, tiles.Resampling.nearest if t.z >= MAXZ else tiles.Resampling.mode, 0)
        if not z.any():
            return None
        im = Image.fromarray(z, mode="P")
        im.putpalette(pal + [0] * (768 - len(pal)))
        im.info["transparency"] = 0
        return tiles.png(im)
    tiles.write(os.path.join(OUT, "koppen.pmtiles"), FRAME, range(0, MAXZ + 1), render, tiles.TileType.PNG,
                {"name": "Köppen-Geiger classes, 1961-1990", "attribution": "Beck et al. (2023), CC BY 4.0",
                 "description": "Paletted PNG, index 0 transparent; tools/vnmap/climate.py"})
    write("koppen.json", {"source": "Beck et al. (2023), Köppen-Geiger classes for 1961-1990, 0.00833 deg (1 km); figshare "
                                    "doi:10.6084/m9.figshare.21789074.v2 (Jan. 2026 correction), CC BY 4.0",
                          "frame": FRAME, "classes": classes})


def grid():
    c = json.load(open(os.path.join(OUT, "climate.json"), encoding="utf-8"))
    b, cd = c["bounds"], c["cell_deg"]
    P, T = c["precipitation"]["values"], c["temperature"]["values"]
    feats = []
    for r in range(c["nrows"]):
        for k in range(c["ncols"]):
            if all(P[m][r][k] is None for m in range(12)):
                continue
            x0, y0 = round(b["west"] + k * cd, 4), round(b["north"] - r * cd, 4)
            x1, y1 = round(b["west"] + (k + 1) * cd, 4), round(b["north"] - (r + 1) * cd, 4)
            pr = {f"p{m + 1}": P[m][r][k] for m in range(12)}
            pr.update({f"t{m + 1}": None if T[m][r][k] is None else T[m][r][k] / 10 for m in range(12)})
            feats.append({"type": "Feature", "properties": pr, "geometry": {
                "type": "Polygon", "coordinates": [[[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]]]}})
    write("climate.geojson", {"type": "FeatureCollection", "features": feats})


if __name__ == "__main__":
    koppen(sys.argv[1], sys.argv[2])
    grid()
