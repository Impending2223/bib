# South Vietnam's provinces, late 1966, and the places the series names

No map data of the Republic of Vietnam's provinces is published. These files rebuild them from today's districts:
first (Oct. 21, 2026) GADM 4.1, level 2 (drawn before Vietnam's 2025 province mergers), each district given whole to
the 1966 province that held most of it, after Wikipedia's articles on the old provinces and the Vietnamese list *Tỉnh
(Việt Nam Cộng hòa)* (`tools/vnmap/xw.py`, `build.py`; downloads not kept: GADM's `gadm41_VNM_2.json`, Natural Earth's
10m admin-0 countries, Wikipedia's API). Then (Oct. 22, 2026) carried over to geoBoundaries CGAZ, the one border
geometry of every map of Indochina (`tools/vnmap/base.py`; `sources/indochina/README.md`): each CGAZ district given
whole to the GADM-built 1966 unit holding most of it. 696 of the 705 districts lie 90 percent or more in one unit; the
nine others are coastal and island districts whose shorelines differ between the two sources (`crosswalk-cgaz.yaml`,
`straddlers`). The gazetteer's provinces, recomputed on the new lines, did not change.

```
crosswalk.yaml          every unit of late 1966 (44 provinces, Saigon, the autonomous towns, Côn Sơn): name, plain
                        form, capital, corps zone, today's region, the GADM districts it is drawn from, sources,
                        confidence, notes; and the changes to 1975 (kept: the hand crosswalk)
crosswalk-cgaz.yaml     each CGAZ district of Vietnam: its modern province, its 1966 unit (or the DRV), its share in
                        that unit, its area; the straddlers (written by tools/vnmap/base.py)
provinces1966.geojson   one feature a unit, on the CGAZ base (WGS84, ~200 m simplification, 3 decimals)
ctz1966.geojson         the corps tactical zones (I–IV, the Capital Military District) dissolved from the provinces
regions.geojson         the RVN by its units' (today's, pre-2025) regions
places.json             the gazetteer: id, name, plain form, kind, lat/lon (Wikipedia's coordinates), years,
                        1966 province (by point in polygon), a working note, the article; `place:<id>` tags point here
validate.md             the checks of Oct. 21 (on the GADM lines): districts assigned once, areas against printed
                        figures, places against the province their articles name, corps zones against second sources
```

The countries around (once `outline.geojson` and `indochina-outline.geojson`, from Natural Earth: a second geometry
that left a band between the RVN and its neighbours) are now `sources/indochina/admin.geojson`'s.

- A line is exact where it follows a district line that has not moved; off by a district where one straddled two 1966
  provinces (Hậu Nghĩa, Kiến Tường, Phú Bổn, the Quảng Tín–Quảng Nam line; `validate.md` lists them). Low confidence:
  Huế and Đà Lạt (drawn at today's size, several times the 1964 cities), Phú Bổn (may lack Ea H'leo).
- Corps zones as of late 1966; Bình Tuy in II Corps from Sept. 1964, in III by 1968 (the date not found: Check).
- Places: coordinates from Wikipedia, never guessed; the Iron Triangle, War Zone C and Junction City take a parent
  place's (said in the note). The notes are working notes, not checked against the sources: not for the series' text.
- Better lines: the University of Texas's scans of the Army Map Service sheets (L7014, 1:50,000; L509, 1:250,000) and
  the CIA's 1970 map of administrative divisions, to trace; the Hamlet Evaluation System's hamlet coordinates with
  their 1960s provinces (NARA; Dell and Querubin's replication files), to test each line hamlet by hamlet. Neither
  hamlet source answers from this environment (403; a bot check).
