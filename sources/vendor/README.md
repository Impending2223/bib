# Vendored libraries and fonts

Served from the site itself (the build copies each directory to `build/vnmap/<dir>/`), so the maps of Indochina
depend on no CDN. Each directory is named by its exact version; to update, fetch the new version from npm
(`npm pack <name>@<version>`), copy the same files into a directory of the new name, change the name in
`tools/bib/vnmap.py` (`MAPLIBRE`, `PMTILES`, `FONT`), and rerun `./bib check` (it fails on a missing file).

| directory | what | from | license |
|---|---|---|---|
| `maplibre-gl-6.13.0/` | MapLibre GL JS 6.13.0 (Oct. 6, 2026): `maplibre-gl.mjs`, `maplibre-gl-worker.mjs` (found beside the first by its own URL), `maplibre-gl.css` | npm `maplibre-gl@6.13.0`, `dist/` | BSD-3-Clause (`LICENSE.txt`: © MapLibre contributors; the Mapbox code of v1.13 and earlier, © Mapbox) |
| `pmtiles-4.5.0/` | PMTiles 4.5.0 (Aug. 10, 2026), `pmtiles.js` (the browser bundle, which sets the global `pmtiles`) | npm `pmtiles@4.5.0`, `dist/pmtiles.js` | BSD-3-Clause (`LICENSE`, © Protomaps LLC, from github.com/protomaps/PMTiles) |
| `libre-franklin-5.3.0/` | Libre Franklin, regular, semibold and italic, the latin, latin-ext and vietnamese subsets (WOFF2): the map's names, through the style's `font-faces` | npm `@fontsource/libre-franklin@5.3.0`, `files/` | SIL Open Font License 1.1 (`LICENSE`, © The Libre Franklin Project Authors) |

Sizes: MapLibre 1.6 MB (the script 1,079,357 bytes and its worker 508,314; gzipped, 284,973 and 143,415), PMTiles
20 KB (8 KB gzipped), the fonts 113 KB.
