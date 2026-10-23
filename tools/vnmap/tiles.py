"""Raster tiles into one PMTiles file, for the maps of Indochina (terrain.py, climate.py). mercantile gives the Web
Mercator tiles and their bounds, rasterio.warp.reproject resamples a lon/lat grid onto each, and the pmtiles package
writes the archive (https://github.com/protomaps/PMTiles), which MapLibre reads through the pmtiles protocol."""
import io
import os

import mercantile
import numpy as np
from affine import Affine
from PIL import Image
from pmtiles.tile import Compression, TileType, zxy_to_tileid
from pmtiles.writer import Writer
from rasterio.warp import Resampling, reproject


def warp(src, src_tr, tile, size, resampling, fill):
    """The lon/lat grid `src` (EPSG:4326, transform src_tr) resampled onto one Web Mercator tile, size x size."""
    b = mercantile.xy_bounds(tile)
    dst = np.full((size, size), fill, src.dtype)
    dtr = Affine((b.right - b.left) / size, 0, b.left, 0, -(b.top - b.bottom) / size, b.top)
    reproject(src, dst, src_transform=src_tr, src_crs="EPSG:4326", dst_transform=dtr, dst_crs="EPSG:3857",
              src_nodata=None, dst_nodata=None, resampling=resampling)
    return dst


def png(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def webp_lossless(img):
    buf = io.BytesIO()
    img.save(buf, format="WEBP", lossless=True, quality=100, method=6)
    return buf.getvalue()


def write(path, frame, zooms, render, tile_type, metadata):
    """render(tile) -> bytes or None (no tile). Tiles written in tile-id order (a clustered archive)."""
    w, s, e, n = frame
    todo = sorted((zxy_to_tileid(t.z, t.x, t.y), t) for z in zooms for t in mercantile.tiles(w, s, e, n, [z]))
    sizes = {}
    with open(path, "wb") as f:
        wr = Writer(f)
        for tid, t in todo:
            data = render(t)
            if data is None:
                continue
            wr.write_tile(tid, data)
            sizes[t.z] = sizes.get(t.z, 0) + len(data)
        e7 = lambda v: int(round(v * 1e7))
        wr.finalize({"tile_type": tile_type, "tile_compression": Compression.NONE,
                     "min_lon_e7": e7(w), "min_lat_e7": e7(s), "max_lon_e7": e7(e), "max_lat_e7": e7(n),
                     "center_zoom": 5, "center_lon_e7": e7((w + e) / 2), "center_lat_e7": e7((s + n) / 2)}, metadata)
    print(os.path.basename(path), os.path.getsize(path), "bytes; by zoom", sizes)


__all__ = ["warp", "png", "webp_lossless", "write", "Resampling", "TileType"]
