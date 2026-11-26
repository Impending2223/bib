"""Relief for the maps of Indochina (Oct. 22, 2026), from one elevation model on the one border geometry
(tools/vnmap/base.py). A one-time script:

    python3 -I tools/vnmap/terrain.py ETOPO_DIR

ETOPO_DIR holds NOAA NCEI's ETOPO 2022 v1, 15 arc-seconds, surface elevation, tiles N15E090, N15E105, N30E090,
N30E105 (ETOPO_2022_v1_15s_<tile>_surface.nc, from
https://www.ngdc.noaa.gov/thredds/fileServer/global/ETOPO2022/15s/15s_surface_elev_netcdf/; public domain), saved as
<tile>.nc. Needs rasterio, mercantile, contourpy, pmtiles and Pillow (pip); no hand-made projection: rasterio.warp
reprojects the grid to each Web Mercator tile, mercantile gives the tiles' bounds.

Writes, in sources/indochina/:
 - dem.pmtiles: the land's elevation as terrain tiles (Terrarium encoding, lossless WebP, 512 px, zooms 0-MAXZ) for
   MapLibre's `raster-dem` source, which draws the hillshade and the elevation tints (`color-relief`) from it. Land is
   what admin.geojson calls land: its height, whole metres, land below sea level counted 0; the sea -1 (flat, and
   transparent in the tints).
 - bathymetry.geojson: the sea's depth bands (0-50, 50-200, 200-1,000, 1,000-2,000, 2,000-4,000, 4,000 m and deeper),
   polygons traced from the same grid at 1' (rasterio.features.shapes) and simplified as a coverage. Drawn under the
   land, so the bands run on under it.
 - contours.geojson: contours at 500, 1,000, 1,500 and 2,000 m from the same grid at 1' (each cell the mean of 4 x 4),
   traced by contourpy, simplified at 0.003 degrees (~300 m), runs under 0.03 degrees dropped.

A second frame (Nov. 26, 2026; tools/vnmap/frames.py, which holds every number that differs): the map of China,

    python3 -I tools/vnmap/terrain.py ETOPO_DIR china

where ETOPO_DIR holds the same model at 30 arc-seconds, the one global file
ETOPO_2022_v1_30s_N90W180_surface.nc (1.64 GB, from
https://www.ngdc.noaa.gov/thredds/fileServer/global/ETOPO2022/30s/30s_surface_elev_netcdf/). It writes the same
three files in sources/china/, and hypso.json, the legend of the bands, which for China run on above 2,000 m.
"""
import json
import os
import sys

import contourpy
import numpy as np
import rasterio
import rasterio.features
import rasterio.merge
import shapely
from affine import Affine
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import frames  # noqa: E402
import tiles  # noqa: E402

F, ARGS = frames.get(sys.argv[1:])      # the frame: Indochina's, or the one the command line names
OUT = F["out"]
FRAME = F["frame"]                      # base.FRAME
MAXZ = F["dem_maxz"]                    # 512-px tiles. Indochina: ~300 m a pixel at z8, the 15" grid's ~460 m
TILE = 512
SEA = -1
DEPTHS = [0, 50, 200, 1000, 2000, 4000]  # band k: deeper than DEPTHS[k]
LEVELS = F["levels"]


def mosaic(d):
    srcs = [rasterio.open(f.format(d) if "{}" in f else os.path.join(d, f)) for f in F["etopo"]]
    arr, tr = rasterio.merge.merge(srcs, bounds=FRAME, nodata=-99999.0)
    for s in srcs:
        s.close()
    return arr[0].astype(np.float32), tr


def land_mask(shape_, tr):
    fc = json.load(open(os.path.join(OUT, "admin.geojson"), encoding="utf-8"))
    geoms = [f["geometry"] for f in fc["features"] if f["properties"]["k"] in ("land", "unit", "disp")]
    return rasterio.features.rasterize(geoms, out_shape=shape_, transform=tr, fill=0, default_value=1,
                                       all_touched=False, dtype="uint8").astype(bool)


def terrarium(z):
    v = np.round(z).astype(np.int32) + 32768
    rgb = np.zeros(z.shape + (3,), np.uint8)
    rgb[..., 0] = (v >> 8) & 255
    rgb[..., 1] = v & 255
    return rgb


def dem_tiles(dem, tr):
    def render(t):
        z = tiles.warp(dem, tr, t, TILE, tiles.Resampling.bilinear if t.z >= MAXZ - 1 else tiles.Resampling.average, SEA)
        if (z <= SEA).all():
            return None             # all sea: no tile (the source's bounds stop most such requests)
        return tiles.webp_lossless(Image.fromarray(terrarium(np.where(z < 0, SEA, z))))
    tiles.write(os.path.join(OUT, "dem.pmtiles"), FRAME, range(0, MAXZ + 1), render, tiles.TileType.WEBP,
                {"name": F["name"] + " elevation", "encoding": "terrarium",
                 "attribution": "NOAA NCEI, ETOPO 2022 15 Arc-Second Global Relief Model (2022), doi:10.25921/fd45-gt74",
                 "description": "Land elevation in whole metres (sea -1), Terrarium encoding; tools/vnmap/terrain.py"})


def coarse(a, k):
    h, w = (a.shape[0] // k) * k, (a.shape[1] // k) * k
    return a[:h, :w].reshape(h // k, k, w // k, k).mean(axis=(1, 3))


def write(name, feats):
    s = json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False, separators=(",", ":"))
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(s + "\n")
    print(name, len(s), "bytes")


def rnd(c, p=3):
    return [rnd(x, p) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], p), round(c[1], p)]


def bathymetry(raw, tr, land):
    k = F["mean"]
    z = coarse(np.where(land, 0, raw), k)
    ctr = tr * Affine.scale(k)
    band = np.digitize(-z, DEPTHS[1:]).astype(np.int16)        # 0: 0-50 m (and the land), ... 5: 4,000 m and deeper
    gs, vals = [], []
    for geom, v in rasterio.features.shapes(band, transform=ctr):
        gs.append(shapely.geometry.shape(geom))
        vals.append(int(v))
    simp = shapely.coverage_simplify(np.array(gs, dtype=object), F["depth_tol"])
    by = {}
    for g, v in zip(simp, vals):
        by.setdefault(v, []).append(g)
    feats = []
    for v in sorted(by):
        if v == 0:
            continue                # the shallowest band is the sea's ground colour (vnmap STYLE)
        g = shapely.union_all(by[v])
        m = shapely.geometry.mapping(g)
        feats.append({"type": "Feature", "properties": {"d": DEPTHS[v]},
                      "geometry": {"type": m["type"], "coordinates": rnd(m["coordinates"])}})
    write("bathymetry.geojson", feats)


def contours(raw, tr, land):
    k = F["mean"]
    z = coarse(np.where(land, np.maximum(raw, 0), 0), k)
    ctr = tr * Affine.scale(k)
    ny, nx = z.shape
    xs = ctr.c + ctr.a * (np.arange(nx) + 0.5)
    ys = ctr.f + ctr.e * (np.arange(ny) + 0.5)
    gen = contourpy.contour_generator(xs, ys, z, line_type="Separate")
    feats = []
    for lv in LEVELS:
        ls = [shapely.LineString(c) for c in gen.lines(lv) if len(c) > 1]
        ls = [shapely.simplify(x, F["contour_tol"]) for x in ls]
        ls = [x for x in ls if x.length >= F["contour_min"]]
        if ls:
            m = shapely.geometry.mapping(shapely.MultiLineString(ls))
            feats.append({"type": "Feature", "properties": {"elev_m": lv},
                          "geometry": {"type": m["type"], "coordinates": rnd(m["coordinates"])}})
    write("contours.geojson", feats)


def hypso():
    """hypso.json, the legend of the bands, in the form of sources/indochina/hypso.json: for a frame that names its
    bands (frames.py). The land's bands are drawn by the map from the tiles; the depths' `d` is DEPTHS."""
    land, sea = F["bands"], frames.SEA
    assert [d for d, _, _ in sea] == DEPTHS
    cl = [{"index": i, "kind": "land", "from_m": lo, "to_m": land[i + 1][0] if i + 1 < len(land) else None,
           "label": lab, "color": col} for i, (lo, lab, col) in enumerate(land)]
    cl += [{"index": len(land) + i, "kind": "sea", "depth_from_m": lo,
            "depth_to_m": sea[i + 1][0] if i + 1 < len(sea) else None, "label": lab, "color": col}
           for i, (lo, lab, col) in enumerate(sea)]
    note = ("The legend of the elevation bands (drawn by MapLibre's color-relief from dem.pmtiles) and the depth bands "
            "(bathymetry.geojson, its `d` the band's lower depth): tools/vnmap/terrain.py. Land is what admin.geojson "
            "calls land; land below 0 m counted 0-100 m.")
    with open(os.path.join(OUT, "hypso.json"), "w", encoding="utf-8") as f:
        json.dump({"classes": cl, "note": note}, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("hypso.json", len(cl), "classes")


def main():
    raw, tr = mosaic(ARGS[0])
    raw[raw < -20000] = 0
    land = land_mask(raw.shape, tr)
    dem = np.where(land, np.maximum(raw, 0), SEA).astype(np.float32)
    steps = ARGS[1:] or ["tiles", "depths", "contours"]         # one step alone, to try a number: `... china contours`
    if "tiles" in steps:
        dem_tiles(dem, tr)
    if "depths" in steps:
        bathymetry(raw, tr, land)
    if "contours" in steps:
        contours(raw, tr, land)
    if F["bands"]:
        hypso()


if __name__ == "__main__":
    main()
