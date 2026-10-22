# Vietnam, Laos and Cambodia: borders, relief, rivers and lakes, climate, rain, population

The data of the maps of Indochina (`tools/bib/vnmap.py`), drawn by MapLibre GL JS in the browser. Made by the
one-time scripts in `tools/vnmap/`, each of whose docstrings names its downloads, where they came from and every
step; the downloads are not kept here. Rebuilt Oct. 22, 2026, on one border geometry (`base.py`) and as tiles where
the data are rasters (`terrain.py`, `climate.py`, `tiles.py`); the rivers, lakes and the rain grid's source are the
work of Oct. 21 (`layers.py`).

## The frame and the projection

- Every file is plain longitude and latitude (WGS84, EPSG:4326), or Web Mercator tiles (EPSG:3857) in a PMTiles
  archive. No file is projected by hand: MapLibre projects the GeoJSON; rasterio (GDAL) warps the grids to the tiles.
- The frame: lon 97.5–113 E, lat 5.5–26 N (`FRAME` in each script); the map's bounds lie inside it (lon 98–112.5,
  lat 6–25.5), the page's first view lon 100–110.5, lat 8–23.5. The rivers, lakes and rain cover that first view only.
- Serving: the PMTiles files are read by HTTP range requests (GitHub Pages answers them; `npx http-server build`
  locally; `python3 -m http.server` does not).

## Files

| file | bytes | what |
|---|---|---|
| `admin.geojson` | 2,868,637 | the borders: countries, units (the RVN's of 1966; today's in the DRV, Laos, Cambodia), lines by rank, label points (`base.py`) |
| `dem.pmtiles` | 25,067,940 | land elevation, Terrarium-encoded lossless WebP tiles, 512 px, zooms 0–8 (`terrain.py`) |
| `bathymetry.geojson` | 468,444 | the sea's depth bands (`terrain.py`) |
| `contours.geojson` | 1,297,649 | contours at 500, 1,000, 1,500 and 2,000 m (`terrain.py`) |
| `hypso.json` | 2,216 | the elevation bands' and depth bands' ranges and colours (the legend) |
| `rivers.geojson` | 645,201 | rivers, 10 m³/s and over, and every named river (`layers.py`) |
| `lakes.geojson` | 760,891 | lakes and reservoirs of 1 km² and over (`layers.py`) |
| `koppen.pmtiles` | 196,512 | Köppen–Geiger classes, 1961–1990, paletted PNG tiles, zooms 0–7 (`climate.py`) |
| `koppen.json` | 1,432 | their legend: value, code, name, colour, share of the frame's land |
| `climate.json` | 590,629 | monthly rainfall and mean temperature normals, 1961–1990, a grid (`layers.py`) |
| `climate.geojson` | 1,534,770 | the same grid as squares, a property a month (`climate.py`) |
| `population.geojson` | 1,940,356 | persons a km², 1960 and 1970, modelled, in classes (`population.py`) |
| `cities.yaml` | 3,180 | the cities' populations as the UN *Demographic Yearbook* printed them, by page (kept by hand) |

About 35 MB together; the largest, `dem.pmtiles`, 25 MB (`check` fails on a file over 50 MB or the set over 60 MB).
A browser fetches the borders (about 0.7 MB compressed) and the library when a map nears the screen, each layer's
file or tiles only when the layer is shown.

### Borders: `admin.geojson`

- **Source:** geoBoundaries, Comprehensive Global Administrative Zones (CGAZ), ADM0, ADM1 and ADM2, the repository's
  main branch as of Oct. 22, 2026 (its latest release 6.0.0, Sept. 14, 2023), from
  `media.githubusercontent.com/media/wmgeolab/geoBoundaries/main/releaseData/CGAZ/`. CGAZ is "a global composite of
  the SSC ADM0, ADM1 and ADM2, clipped to international boundaries (US Department of State), with gaps filled between
  borders" (the project's README). License CC BY 4.0. Citation: Runfola, D. et al. (2020) geoBoundaries: A global
  database of political administrative boundaries. *PLoS ONE* 15(4): e0231866, doi:10.1371/journal.pone.0231866.
- **One coverage:** the countries (ADM0) cut to the frame; inside Vietnam its 705 districts (ADM2), inside Laos and
  Cambodia their provinces (ADM1), each cut to its country, the slivers no unit covered shared out by Voronoi cells
  of the nearest units' boundaries (CGAZ's levels come from different sources and do not nest exactly). Made a valid
  coverage (`shapely.coverage_clean`) and simplified once, every shared edge alike (`shapely.coverage_simplify`,
  0.002°, about 200 m); islets under 0.5 km² dropped; coordinates to 0.001°. Everything else is dissolved from these
  pieces, so every line on the map is the same line wherever it is drawn.
- **Features** (`k`): `land`, the countries without units (Thailand, China, Burma, Malaysia); `unit`, the RVN's 51
  units of late 1966 (from `sources/vn-provinces-1966/`: id, name, plain form, corps zone, region, confidence) and
  the DRV's, Laos's and Cambodia's provinces (today's, CGAZ's names; the DRV's region from en Wikipedia's "First-level
  subdivisions of Vietnam", oldid 1265924465, its table "Regions of Vietnam"), with Vĩnh Linh (today's Vĩnh Linh and
  Cồn Cỏ districts, north of the Bến Hải) apart as the DRV's special zone; `line`, each boundary once at its highest
  rank (`l`: `intl`, `dmz` the RVN–DRV line, `ctz`, `region`, `unit` a country at a time (`c`), and `coast`);
  `lab`, label points (polylabel of the largest part; a country's inside the first view).
- **Not of the 1960s:** the DRV's, Laos's and Cambodia's provinces are today's; no open map of their 1960s units was
  found (`notes/leads.md`, Foreign). The legend says so.

### Relief: `dem.pmtiles`, `bathymetry.geojson`, `contours.geojson`, `hypso.json`

- **Source:** NOAA NCEI, *ETOPO 2022 v1* global relief model, surface elevation, 15 arc-seconds, tiles N15E090,
  N15E105, N30E090, N30E105, from NCEI's THREDDS file server
  (`https://www.ngdc.noaa.gov/thredds/fileServer/global/ETOPO2022/15s/15s_surface_elev_netcdf/`). Public domain (U.S.
  Government work). Citation: NOAA National Centers for Environmental Information, *ETOPO 2022 15 Arc-Second Global
  Relief Model* (2022), doi:10.25921/fd45-gt74.
- **Land and sea:** land is what `admin.geojson` calls land, rasterized onto the grid; land below sea level counted
  0 m; the sea −1 m in the tiles (flat, unshaded, and transparent in the elevation bands).
- **Tiles:** each Web Mercator tile (mercantile) warped from the grid by rasterio (bilinear at zooms 7–8, the mean
  below), whole metres in the Terrarium encoding, lossless WebP, 512 px; zoom 8 is about 300 m a pixel, the grid
  about 460 m. MapLibre draws from them the hillshade (`hillshade`, its multidirectional method) and the elevation
  bands (`color-relief`) at the screen's resolution; past zoom 8 it interpolates the zoom 8 tiles (a finer model:
  `notes/leads.md`).
- **Bands:** land 0–100, 100–200, 200–500, 500–1,000, 1,000–1,500, 1,500–2,000, 2,000 m and over; sea by depth 0–50
  (the sea's ground colour), 50–200, 200–1,000, 1,000–2,000, 2,000–4,000, 4,000 m and deeper. Colours and ranges in
  `hypso.json`. The depth bands are polygons traced from the grid at 1′ (rasterio.features.shapes), simplified as a
  coverage at 0.01°; they run on under the land, which covers them.
- **Contours:** from the grid at 1′ (the mean of 4 × 4 cells), traced by contourpy at 500, 1,000, 1,500 and 2,000 m,
  simplified at 0.003°, runs under 0.03° dropped; one MultiLineString a level (`elev_m`). The bands (from the tiles)
  and the contours (from the 1′ means) do not exactly coincide.

### Rivers: `rivers.geojson`

MultiLineString features, each the merged lines of one name and one size, drawn smallest first in file order.
Properties: `size` (1 the largest, 7 the smallest), `source` (`HydroRIVERS` or `SWORD`), and where known `name` (the
source's English form) and `name_vi` (the Vietnamese form, written by hand for the rivers below).

- **Outside the delta: HydroRIVERS v1.0, Asia** (https://www.hydrosheds.org/products/hydrorivers; downloaded from
  https://data.hydrosheds.org/file/HydroRIVERS/HydroRIVERS_v10_as_shp.zip). Every segment with a long-term mean
  discharge (`DIS_AV_CMS`) of 10 m³/s or more, and every named segment. `size` by discharge: 1 ≥ 5,000 m³/s; 2
  1,000–5,000; 3 300–1,000; 4 100–300; 5 30–100; 6 10–30; 7 under 10 (named only). Simplified at 0.002°, coordinates to
  0.001° (a coarser copy at 0.008°, `rivers-coarse.geojson`, was deleted Oct. 22, 2026: MapLibre simplifies by zoom).
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

### Climate: `koppen.pmtiles`, `koppen.json`

- **Source:** Beck, H. E., McVicar, T. R., Vergopolan, N., Berg, A., Lutsko, N. J., Dufour, A., Zeng, Z., Jiang, X.,
  van Dijk, A. I. J. M., Miralles, D. G. (2023): High-resolution (1 km) Köppen-Geiger maps for 1901–2099 based on
  constrained CMIP6 projections. *Scientific Data* 10: 724, doi:10.1038/s41597-023-02549-6. Dataset: figshare,
  doi:10.6084/m9.figshare.21789074.v2 (version 2, Jan. 14, 2026, which corrects a small calculation error),
  `koppen_geiger_tif.zip` (from `https://ndownloader.figshare.com/files/61012822`, the address figshare's API gives),
  file `1961_1990/koppen_geiger_0p00833333.tif`: **the 1961–1990 period**, 0.00833° (1 km). License CC BY 4.0.
- Raster tiles, not polygons (traced and simplified at 400 m, the classes made 5.8 MB of GeoJSON): paletted PNG,
  256 px, zooms 0–7 (about 1.2 km a pixel at zoom 7), resampled by nearest neighbour (by mode below zoom 7), index 0
  transparent (sea, no data), then the classes present in the frame in the legend's order with the paper's colours
  (`legend.txt` in the archive). MapLibre draws them with nearest resampling, each cell sharp at any zoom.
  `koppen.json` gives each class's value, code, name, colour and share of the frame's land; the legend shows those
  over 0.1 percent.

### Weather: `climate.json`, `climate.geojson`

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
- `climate.geojson` (`climate.py`): each land cell a square, `p1`–`p12` (mm) and `t1`–`t12` (°C), so the map colours
  the month chosen and a tap reads the cell. CRU's host did not answer on Oct. 22, 2026: the grid was not widened to
  the map's frame (`notes/leads.md`).

### Population: `population.geojson`, `cities.yaml`

- **Density, modelled:** ISIMIP3a's gridded historical population, `population_histsoc_5arcmin_annual_1901_2021.nc`
  (`https://files.isimip.org/ISIMIP3a/InputData/socioeconomic/pop/histsoc/`; 1.37 GB), whose national and gridded
  figures ISIMIP's page (isimip.org, input data, details/79) says are "taken from the History Database of the Global
  Environment (HYDE) version 3.2.1"; the file's header cites Klein Goldewijk, Beusen, Doelman and Stehfest,
  "Anthropogenic land use estimates for the Holocene – HYDE 3.2", *Earth System Science Data* 9 (2017): 927–953, and
  HYDE 3.3 (doi:10.24416/UU01-67UHB4). The ISIMIP site's content is CC BY 4.0. The bands for 1960 and 1970, each 5′
  cell's count over its geodesic area (pyproj), in persons a km², classed (0, 1, 10, 25, 50, 100, 250, 500, 1,000)
  and traced as polygons, simplified as a coverage at 0.004°. **A model, made later** from national totals and later
  maps: not a census, and the legend says so. HYDE's own host (geo.public.data.uu.nl) answers with a bot check here.
- **Cities:** `cities.yaml`, the populations the UN *Demographic Yearbook* printed (1966, table 6; 1970, table 8),
  read by eye off the page images, each with its date, census or estimate, city proper or agglomeration, page and the
  Yearbook's marks (its header). The map draws a circle by the first figure; a tap gives every row and its page.


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
