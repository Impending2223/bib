"""The frames the one-time layer scripts serve (terrain.py, climate.py, population.py, layers.py): the maps of
Indochina, for which the scripts were written (Oct. 21-22, 2026), and the map of China (Nov. 26, 2026; the owner,
Nov. 25: "Which of the SEA map overlays can we also use on our China map? Bring them over."). One method and one
source a layer for both maps; a frame differs from the other by its numbers alone, and they are all here.

A script takes the frame's name as an argument of its own ("china"); with none it makes Indochina's files, as before:

    python3 -I tools/vnmap/terrain.py ETOPO_DIR china
    python3 -I tools/vnmap/climate.py KOPPEN_TIF LEGEND_TXT china
    python3 -I tools/vnmap/population.py ISIMIP_NC china
    python3 -I tools/vnmap/layers.py DL sources/china china hydro lakes climate

China is some thirty times Indochina's area, and its map opens about two zooms farther out (its first view is 62.5
degrees wide, Indochina's 10.5), so each layer is made about four times as coarse: what reads the same on the screen
at each map's own zooms, in files a browser can take (sources/china/README.md gives each file's bytes and the
choice). Indochina's numbers are those the scripts held before they served two frames: its files come out the same.

Each frame:
  out        the directory of its files, under the repository's root
  frame      lon/lat (west, south, east, north): the tiles, the depths, the contours, the population
  extent     lon/lat: the rivers, the lakes, the rain (layers.py). Indochina's is the page's first view, since the
             hosts refused on Oct. 22, 2026 (sources/indochina/README.md); China's is the map's bounds, cnmap.BOUNDS.
  etopo      the elevation model's files in ETOPO_DIR, and the grid's step in arc-seconds
  dem_maxz   the elevation tiles' deepest zoom (512 px)
  mean       the contours' and the depths' grid: the mean of mean x mean cells of the model
  depth_tol, contour_tol, contour_min   simplifying, degrees; the shortest contour run kept, degrees
  levels     the contours, metres
  bands      the elevation bands, written to hypso.json with the depths' (None: the file is kept as it is; Indochina's
             was written on Oct. 22, 2026)
  koppen_maxz the climate tiles' deepest zoom (256 px)
  pop_cells  the population's grid: pop_cells x pop_cells of the model's 5' cells summed; pop_tol, pop_prec the
             simplifying, degrees, and the decimals kept
  rain_cells the rain's grid: rain_cells x rain_cells of CRU's 10' cells, their mean
  sword      SWORD's Pfafstetter basins read for the rivers' names (and, in a delta, their channels)
  delta      the ring inside which the rivers are SWORD's channels, not HydroRIVERS's (None: no such ring)
  river_min  the least long-term mean discharge drawn, m3/s; river_read: segments under it are not read at all
             (None: all are, and a named one is drawn whatever its size)
  river_tol  simplifying, degrees; river_coarse: a second, coarser file written too (Indochina's, deleted since)
  local, hand, to_sea, same   the rivers' names: local forms written by hand, rivers traced by hand, rivers that keep
             their name to the sea, one river's two spellings (layers.py)
  lake_min   the least lake drawn, km2; lake_tol simplifying, degrees
"""
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

# the elevation bands (land) and the depths' (sea): lower bound, label, colour. The first seven land bands and the
# depths are the maps of Indochina's (layers.py BANDS, DEPTHS; sources/indochina/hypso.json).
LAND7 = [(0, "0–100 m", "#acd0a5"), (100, "100–200 m", "#c4deac"), (200, "200–500 m", "#e1e4b5"),
         (500, "500–1,000 m", "#e8d6a4"), (1000, "1,000–1,500 m", "#dbbc8a"), (1500, "1,500–2,000 m", "#c6a078")]
SEA = [(0, "0–50 m deep", "#d8eaf4"), (50, "50–200 m deep", "#c6dff0"), (200, "200–1,000 m deep", "#aacde8"),
       (1000, "1,000–2,000 m deep", "#91bcdf"), (2000, "2,000–4,000 m deep", "#7aabd6"),
       (4000, "4,000 m and deeper", "#659acd")]
# China's: the same six, then Indochina's last colour for 2,000-3,000 m and three more above it, for Tibet, the Pamirs
# and the Tian Shan: the browns run on into the grays of the usual relief tints (Wikipedia's map conventions for
# topographic maps: #ac9a7c, #baae9a, #cac3b8)
LAND_CN = LAND7 + [(2000, "2,000–3,000 m", "#ac866c"), (3000, "3,000–4,000 m", "#ac9a7c"),
                   (4000, "4,000–5,000 m", "#baae9a"), (5000, "5,000 m and over", "#cac3b8")]

FRAMES = {
    "indochina": {
        "out": "sources/indochina", "name": "Indochina",
        "frame": (97.5, 5.5, 113.0, 26.0), "extent": (100.0, 8.0, 110.5, 23.5),
        "etopo": ("N15E090.nc", "N15E105.nc", "N30E090.nc", "N30E105.nc"), "etopo_sec": 15,
        "dem_maxz": 8, "mean": 4, "depth_tol": 0.01, "contour_tol": 0.003, "contour_min": 0.03,
        "levels": [500, 1000, 1500, 2000], "bands": None,
        "koppen_maxz": 7,
        "pop_cells": 1, "pop_tol": 0.004, "pop_prec": 3,
        "rain_cells": 1,
        "sword": (43, 44),
        # The Mekong delta and the Saigon lowlands (layers.py, hydro)
        "delta": [(104.70, 11.80), (105.95, 11.80), (106.45, 11.20), (106.60, 10.86), (106.95, 10.80), (107.15, 10.40),
                  (107.15, 8.40), (104.70, 8.40)],
        "river_min": 10, "river_read": None, "river_tol": 0.002, "river_coarse": True,
        "lake_min": 1.0, "lake_tol": 0.001,
    },
    "china": {
        "out": "sources/china", "name": "China",
        "frame": (66.0, 10.0, 142.0, 58.0), "extent": (67.0, 11.0, 141.0, 57.0),
        "etopo": ('NETCDF:"{}/ETOPO_2022_v1_30s_N90W180_surface.nc":z',), "etopo_sec": 30,
        "dem_maxz": 5, "mean": 4, "depth_tol": 0.04, "contour_tol": 0.012, "contour_min": 0.12,
        "levels": [500, 1000, 2000, 3000, 4000, 5000], "bands": LAND_CN,
        "koppen_maxz": 6,
        "pop_cells": 3, "pop_tol": 0.012, "pop_prec": 2,
        "rain_cells": 3,
        "sword": (31, 32, 33, 34, 35, 36, 41, 42, 43, 44, 45, 46, 47, 48, 49),
        "delta": None,
        "river_min": 30, "river_read": 30, "river_tol": 0.008, "river_coarse": False,
        "to_sea": ("Yangtze", "Yellow River", "Amur"),
        "same": {"Chang Jiang": "Yangtze", "Salween": "Salween River", "Salween - Nujiang": "Salween River"},
        "lake_min": 10.0, "lake_tol": 0.004,
    },
}


def get(argv):
    """The frame the command line names (an argument that is a frame's name), Indochina's where it names none; and
    the arguments without it. A frame's `out` is made a path under the repository's root."""
    name = next((a for a in argv if a in FRAMES), "indochina")
    f = dict(FRAMES[name], id=name)
    f["out"] = os.path.join(ROOT, *f["out"].split("/"))
    return f, [a for a in argv if a not in FRAMES]
