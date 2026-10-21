# Vietnam, Laos and Cambodia: relief, rivers and lakes, climate, rainfall

Map layers for the calendar's maps of 1960–69, drawn by d3 over a Mercator projection. Built Oct. 21, 2026, by
`tools/vnmap/layers.py` (a one-time script; its docstring names every download, where it came from, and the step that
reads it). The downloads are not kept here.

## The common frame

- **Extent of every layer:** lon 100.0–110.5 E, lat 8.0–23.5 N, WGS84. In Web Mercator (EPSG:3857) metres: x
  11,131,949.08–12,300,803.73, y 893,463.75–2,692,598.22.
- **Rasters (every PNG) are in Web Mercator rows.** Columns are evenly spaced in longitude (as Mercator x is); rows
  are evenly spaced in EPSG:3857 y, from y(23.5° N) at the top to y(8.0° N) at the foot, each sampled at its centre
  latitude. Draw each as one `<image>` stretched over the projected rectangle of the bounds: `[proj([100, 23.5]),
  proj([110.5, 8])]`. No reprojection in the browser. Continuous fields are sampled bilinearly, classes by nearest
  neighbour.
- **Vectors (GeoJSON) and the climate grid** are plain lon/lat (EPSG:4326).

| raster | size (px) | source cell | file |
|---|---|---|---|
| fine | 2520 × 3879 | 15″ (~460 m) | `hillshade-fine.png` |
| standard | 1260 × 1939 | 30″ (~920 m) | `hillshade.png`, `hypso.png`, `koppen.png` |
| coarse | 630 × 970 | from the 30″ grid | `hillshade-coarse.png`, `hypso-coarse.png`, `koppen-coarse.png` |

Use the coarse rasters for the whole-country view, the standard ones when zoomed, and `hillshade-fine.png` (4.1 MB)
only past about 3× zoom.

## Files

| file | bytes | what |
|---|---|---|
| `hillshade-fine.png` | 4,111,243 | hillshade from ETOPO 2022 15″ |
| `hillshade.png` | 1,041,102 | hillshade from ETOPO 2022 30″ |
| `hillshade-coarse.png` | 241,476 | hillshade from ETOPO 2022 30″, smoothed |
| `hypso.png`, `hypso-coarse.png` | 166,658; 57,356 | elevation bands and sea depths, indexed |
| `hypso.json` | 2,216 | their legend: class, range, color |
| `contours.geojson` | 469,580 | contours at 500, 1,000, 1,500 and 2,000 m |
| `rivers.geojson` | 645,201 | rivers, 10 m³/s and over, and every named river |
| `rivers-coarse.geojson` | 123,796 | rivers, 100 m³/s and over (named rivers 30 m³/s and over) |
| `lakes.geojson` | 760,891 | lakes and reservoirs of 1 km² and over |
| `koppen.png`, `koppen-coarse.png` | 65,023; 24,706 | Köppen–Geiger classes, 1961–1990, indexed |
| `koppen.json` | 1,700 | their legend: code, name, color, share of the extent's land |
| `climate.json` | 590,629 | monthly rainfall and mean temperature normals, 1961–1990 |

8.0 MB together.

### Relief: `hillshade*.png`, `hypso*.png`, `hypso.json`, `contours.geojson`

- **Source:** NOAA NCEI, *ETOPO 2022 v1* global relief model, surface elevation (ice surface, EGM2008 heights), 30
  arc-seconds (`ETOPO_2022_v1_30s_N90W180_surface.nc`) and 15 arc-seconds (tiles N15E090, N15E105, N30E090,
  N30E105), the extent's part read by OPeNDAP from NCEI's THREDDS server,
  https://www.ngdc.noaa.gov/thredds/catalog/global/ETOPO2022/catalog.html. Cells are pixel-centred
  (`node_offset 1`). Public domain (U.S. Government work).
  Citation: NOAA National Centers for Environmental Information, *ETOPO 2022 15 Arc-Second Global Relief Model*
  (2022), doi:10.25921/fd45-gt74.
- **Sea mask:** Natural Earth 10m land, v5.1.1 (https://www.naturalearthdata.com; public domain), rasterized onto each
  grid. Land is what the mask calls land, whatever its ETOPO height; the Tonle Sap and other lakes are land here (draw
  `lakes.geojson` over them).
- **Hillshade:** sun from the northwest (azimuth 315°), 45° high; the ground spacing of each row from its latitude;
  vertical exaggeration 1.5 (fine), 2 (standard), 3 (coarse, after a Gaussian blur of 0.6 px). Land below sea level
  counted 0 m. Encoding: two channels, gray and alpha. Gray is 0 where a slope is darker than flat ground and 255 where
  it is lighter; alpha is how much darker or lighter (flat ground and the sea transparent), in 32 steps. Lay it over the
  tint or a plain ground.
- **Bands (`hypso*.png`):** an indexed PNG, the palette index the class. Land: 0–100, 100–200, 200–500, 500–1,000,
  1,000–1,500, 1,500–2,000, 2,000 m and over (indices 0–6). Sea, by depth: 0–50, 50–200, 200–1,000, 1,000–2,000,
  2,000–4,000, 4,000 m and deeper (indices 7–12). Colors and ranges in `hypso.json`; recolor by rewriting the PNG's
  palette (PLTE) or by drawing the classes yourself. Land below 0 m is counted 0–100 m, and sea cells above 0 m 0–50 m
  deep.
- **Contours:** from the 30″ grid after a Gaussian blur of one cell (about 1 km), traced at 500, 1,000, 1,500 and
  2,000 m, simplified at 0.004° (about 400 m), lines under 0.03° dropped, coordinates to 0.001°. One MultiLineString
  feature a level (`elev_m`). Good to about 1:500,000; the bands and the contours do not exactly coincide (the contours
  are smoothed).

### Rivers: `rivers.geojson`, `rivers-coarse.geojson`

MultiLineString features, each the merged lines of one name and one size, drawn smallest first in file order.
Properties: `size` (1 the largest, 7 the smallest), `source` (`HydroRIVERS` or `SWORD`), and where known `name` (the
source's English form) and `name_vi` (the Vietnamese form, written by hand for the rivers below).

- **Outside the delta: HydroRIVERS v1.0, Asia** (https://www.hydrosheds.org/products/hydrorivers; downloaded from
  https://data.hydrosheds.org/file/HydroRIVERS/HydroRIVERS_v10_as_shp.zip). Every segment with a long-term mean
  discharge (`DIS_AV_CMS`) of 10 m³/s or more, and every named segment. `size` by discharge: 1 ≥ 5,000 m³/s; 2
  1,000–5,000; 3 300–1,000; 4 100–300; 5 30–100; 6 10–30; 7 under 10 (named only). Simplified at 0.002° (fine) and
  0.008° (coarse), coordinates to 0.001°.
  Citation: Lehner, B., Grill, G. (2013): Global river hydrography and network routing: baseline data and new
  approaches to study the world's large river systems. *Hydrological Processes* 27(15): 2171–2186. Data at
  https://www.hydrosheds.org.
  **License: the HydroSHEDS version 1 License Agreement (WWF)**, Appendix A of the HydroSHEDS Technical Documentation
  v1.4: free for non-commercial and commercial use; distributed only as incorporated into a derivative work (never as a
  stand-alone product), with this statement:
  > This product [the 1968 series' map layers] incorporates data from the HydroSHEDS version 1 database which is ©
  > World Wildlife Fund, Inc. (2006-2022) and has been used herein under license. WWF has not evaluated the data as
  > altered and incorporated within [the 1968 series' map layers], and therefore gives no warranty regarding its
  > accuracy, completeness, currency or suitability for any particular purpose. Portions of the HydroSHEDS v1 database
  > incorporate data which are the intellectual property rights of © USGS (2006-2008), NASA (2000-2005), ESRI
  > (1992-1998), CIAT (2004-2006), UNEP-WCMC (1993), WWF (2004), Commonwealth of Australia (2007), and Her Royal
  > Majesty and the British Crown and are used under license. The HydroSHEDS v1 database and more information are
  > available at https://www.hydrosheds.org.

  The page that draws `rivers*.geojson` should carry that statement (or link to this README) where it credits sources.
- **Inside the delta: SWORD v17c** (the SWOT Mission River Database), reaches of Pfafstetter basins 43 and 44
  (`as_sword_reaches_hb43_v17c`, `hb44`), read out of `SWORD_v17c_shp.zip`, Zenodo record 22259077
  (doi:10.5281/zenodo.22259077), by HTTP range requests (the archive is 3.8 GB). SWORD maps every channel 30 m wide or
  more from Landsat (it is built on GRWL), so it has the distributaries a flow-direction network cannot: HydroRIVERS
  sends the whole Mekong down one channel and draws flow paths across the flat delta that are not rivers. The ring:
  from Phnom Penh's latitude (11.8° N) south, east to the Đồng Nai below Biên Hòa and the Rừng Sát (`DELTA` in the
  script); inside it every SWORD reach, outside every HydroRIVERS segment, cut at the ring (the two meet within a few
  hundred metres). `size` by SWORD's width: 1 ≥ 900 m; 2 400–900; 3 200–400; 4 100–200; 5 50–100; 6 under 50.
  Coarse: sizes 1–3.
  License CC BY 4.0. Citation: Altenau, E. H., Pavelsky, T. M., Durand, M. T., Yang, X., Frasson, R. P. d. M.,
  Bendezu, L. (2021): The Surface Water and Ocean Topography (SWOT) Mission River Database (SWORD): A Global River
  Network for Satellite Data Products. *Water Resources Research* 57: e2021WR030054; the dataset, v17c: Gearon, J. H.,
  Altenau, E. H., Pavelsky, T. M., Durand, M. T., et al., Zenodo (2026), doi:10.5281/zenodo.22259077.
- **Names.** SWORD's `river_name` (from GRWL; English or romanized, no diacritics), given to the HydroRIVERS segments
  that lie within about 1 km of SWORD reaches of one name at two of three points along them; then filled along each
  trunk where the source skips a stretch or gives it a tributary's name (`fill_runs`); a name on fewer than three
  segments of a river dropped as a stray. The Red, Mekong, Mã, Lam, Gianh, Perfume and Chao Phraya keep their names to
  the sea; the Mekong and the Bassac are carried to the sea through the delta by the widest branch. Two rivers SWORD
  does not name are traced by hand on HydroRIVERS's main stem (the largest upstream area at each fork), down to the sea
  and up to the source, from points in `sources/vn-provinces-1966/places.json` (Wikipedia's coordinates): the Bến Hải
  from its mouth (17.015 N, 107.1125 E), the Thạch Hãn through Quảng Trị (16.7469 N, 107.194 E). `name_vi`, written by
  hand (`VI` in the script) only where the form is certain: Hồng, Đà, Lô, Chảy, Gâm, Đáy, Phó Đáy, Công, Kỳ Cùng, Mã,
  Chu, Lam (Cả), Gianh, Bến Hải, Thạch Hãn, Bồ, Hương, Cẩm Lệ, Vu Gia, A Vương, Tranh, Trường Giang, Kôn, Ayun, Hinh,
  Sê San, Srêpốk, Bé, Đồng Nai, Sài Gòn, Hậu (the Bassac), Mê Kông, and Tiền for the Mekong below the Cambodian border.
  **Not named** (no source here names them): the Thái Bình, Thu Bồn, Trà Khúc, Ba (Đà Rằng), the upper Đồng Nai, the
  Vàm Cỏ Đông and Tây (SWORD names a river from Cambodia toward the Vàm Cỏ "Prek Kampong Spean": Check), and the delta's distributaries (Cổ
  Chiên, Hàm Luông, Mỹ Tho, Ba Lai, Soài Rạp, Lòng Tàu). The Mekong's name runs to the sea down one branch only (the
  widest); the others are unnamed. Names are for labels and highlighting; check a name against a map of the period
  before it goes into the series' prose.
- **Rivers are today's courses** (SRTM 2000 and Landsat 1984–2015): the Mekong's and the Red River's channels have
  moved a little since the 1960s; the reservoirs built since (below) flood stretches the rivers ran through then.

### Lakes: `lakes.geojson`

- **Source:** HydroLAKES v1.0 (https://www.hydrosheds.org/products/hydrolakes;
  https://data.hydrosheds.org/file/hydrolakes/HydroLAKES_polys_v10_shp.zip). Every lake and reservoir of 1 km² or more
  in the extent (698), cut to the extent, simplified at 0.001° (topology kept), coordinates to 0.0001°, largest first.
  Properties: `id` (Hylak_id), `area_km2`, `type` (lake, reservoir, lake control), `name` (where HydroLAKES has one:
  the Tonle Sap and a few Thai lakes), `dam_year`.
  License CC BY 4.0. Citation: Messager, M. L., Lehner, B., Grill, G., Nedeva, I., Schmitt, O. (2016): Estimating the
  volume and age of water stored in global lakes using a geo-statistical approach. *Nature Communications* 7: 13603,
  doi:10.1038/ncomms13603.
- **`dam_year`:** the year GRanD gives for a dam within about 2 km of the water body (of several, the largest), from
  `Res.Grand.txt` in Lehner's *Dam Impoundment Database*, Zenodo record 15350094 (doi:10.5281/zenodo.15350094; CC BY
  4.0), its columns read as rank, capacity, area, year, lon, lat (checked: Owen Falls 1954, Kariba 1959, Bratsk 1964;
  Trị An 1987, 277 km² in both). GRanD: Lehner, B., et al. (2011): High-resolution mapping of the world's reservoirs
  and dams for sustainable river-flow management. *Frontiers in Ecology and the Environment* 9(9): 494–502,
  doi:10.1890/100125. 48 of 53 reservoirs have a year. **A water body without a year is not thereby older than 1969,
  nor natural:** HydroLAKES types as "lake" reservoirs GRanD's table lacks, the Dầu Tiếng reservoir on the Saigon river
  (187 km², 106.32 E 11.43 N) among them. For a map of the 1960s, draw only `type: lake` and reservoirs with `dam_year`
  ≤ the map's year, and treat the large unnamed "lakes" of the plateaus and the Saigon basin with suspicion.

### Climate: `koppen*.png`, `koppen.json`

- **Source:** Beck, H. E., McVicar, T. R., Vergopolan, N., Berg, A., Lutsko, N. J., Dufour, A., Zeng, Z., Jiang, X.,
  van Dijk, A. I. J. M., Miralles, D. G. (2023): High-resolution (1 km) Köppen-Geiger maps for 1901–2099 based on
  constrained CMIP6 projections. *Scientific Data* 10: 724, doi:10.1038/s41597-023-02549-6. Dataset: figshare,
  doi:10.6084/m9.figshare.21789074.v2 (version 2, Jan. 14, 2026, which corrects a small calculation error),
  `koppen_geiger_tif.zip`, file `1961_1990/koppen_geiger_0p00833333.tif`: **the 1961–1990 period**, 0.00833° (1 km).
  License CC BY 4.0.
- An indexed PNG: palette index 0 transparent (sea, no data), then one index a class present in the extent, in the
  legend's order, with the paper's colors (the standard Köppen palette): Af, Am, Aw, BSh (a few cells), Cwa, Cwb, Cfa,
  Cfb. `koppen.json` gives each index's value, code, name, color and share of the extent's land. Nearest-neighbour
  sampling at both sizes.

### Weather: `climate.json`

- **Source:** CRU CL 2.0, the 10-minute mean monthly climate of global land areas, **1961–1990**: New, M., Lister, D.,
  Hulme, M., Makin, I. (2002): A high-resolution data set of surface climate over global land areas. *Climate Research*
  21: 1–25. Files `grid_10min_pre.dat.gz` (precipitation) and `grid_10min_tmp.dat.gz` (mean temperature) from
  https://crudata.uea.ac.uk/cru/data/hrg/tmc/ (no known problems, says the site's list). Acknowledge "Climatic
  Research Unit, University of East Anglia". **License: Open Database License, contents under the Database Contents
  License (attribution and share-alike)**: `climate.json` is a derived database, and is released under the ODbL too.
- A 63 × 93 grid of 10′ cells (1/6°), plain lon/lat, from 100.0 E and 23.5 N; cell (r, c) spans lat 23.5 − r/6 to
  23.5 − (r+1)/6 and lon 100 + c/6 to 100 + (c+1)/6. `precipitation.values[m][r][c]` in whole mm a month,
  `temperature.values[m][r][c]` in tenths of a degree C, months 0–11 January to December, rows north to south; `null`
  over the sea (3,889 land cells). Checks: Saigon's cell 8 mm in February and 272 in September; Huế's 520 in October;
  Hanoi's 296 in August; Vientiane's 4 in December.

## Tried and refused, and what was not used

- **figshare.com**'s download links (`figshare.com/ndownloader/files/...`) answer an AWS WAF challenge (202,
  `x-amzn-waf-action: challenge`): a bot check, not gone around. Figshare's public API (api.figshare.com/v2/articles/
  21789074) gives each file's `download_url` on `ndownloader.figshare.com`, which answered with the file.
- **OpenStreetMap** (overpass-api.de, download.geofabrik.de): the connection is closed by this environment's proxy;
  no OSM river names or delta channels. The owner can allow the hosts in the environment's network settings.
- **sedac.ciesin.columbia.edu** (GRanD's original host): connection reset. GRanD's years came from Zenodo instead.
- **Natural Earth's `ne_10m_rivers_asia.zip`** on naciscdn.org: 403. Natural Earth's 10m
  rivers were read and not used: in the extent they name only the Mekong, Red, Black, Cả, Ba, Tonle Sap and a few
  Lao and Thai rivers.
- **GRWL** (Allen and Pavelsky 2018; Zenodo 1297434, CC BY 4.0): its vector archive is 3.1 GB; SWORD, built on it,
  serves the same channels with names.
- **Wikipedia's coordinates** for the rivers (English and Vietnamese APIs; rate-limited, 429, then answered): most
  articles carry none (Thạch Hãn, Bến Hải's is a landmark's, Cửa Việt none); used only through `places.json`.
- **Not done:** ocean depth is in the bands but not hillshaded; no 15″ tint or contours (the 30″ are enough for
  them); CRU TS 4.x was not needed (CRU CL 2.0 is the 1961–1990 normal at finer resolution).
