# China: borders, provinces of 1966, counties of 1964, places

The data of the map of China (`tools/bib/cnmap.py`, `build/china.html`), drawn in the browser by MapLibre GL JS with the maps of Indochina's client. Made on Nov. 26, 2026, by the one-time scripts in `tools/cnmap/`. Each script's docstring names its downloads, where they came from and every step. The downloads are not kept here. The guide: `notes/guide/china-map.md`.

## Files

| file | bytes | what | made by |
|---|---|---|---|
| `admin.geojson` | 2,364,088 | the borders: the countries (`k: land`), the disputed areas (`disp`), the 30 units of 1966 (`unit`), the lines by rank (`line`: `coast`, `intl`, `disp`, `unit`), label points (`lab`) | `base.py` |
| `counties.geojson` | 4,336,710 | the counties: 2,241 areas (`k: county`), their lines where no heavier line runs (`line`, `county`), label points (`lab`) | `base.py` |
| `units.json` | 5,679 | each unit of 1966: id, name, kind, the provinces of today it holds, km² | `base.py` |
| `counties.json` | 807,914 | each county drawn: id, name, the name in Chinese, kind, unit of 1966, province and prefecture of 1964, the later units it is made of and on what basis, `guess`; the later units shown as they are (`later`); the 1964 units not shown (`not_shown`) | `base.py` |
| `crosswalk.json` | 710,160 | the record behind the counties: each unit of the boundary file, the name it was matched to and how, the 1964 unit it walks back to and the changes used; each province's 1964 list | `counties.py` |
| `places.json` | 115,134 | the calendar's gazetteer's places in China: Wikidata's coordinates, the rule the item was chosen by, the unit of 1966 and the county of 1964 | `places.py` |

Every file is plain longitude and latitude (WGS84). Nothing is projected by hand. The frame is lon 66–142 E, lat 10–58 N (`FRAME` in `base.py`). The map's bounds lie inside it (lon 67–141, lat 11–57). The page's first view is lon 73–135.5, lat 17.5–54.

## Sources and licences

- geoBoundaries, Comprehensive Global Administrative Zones (CGAZ), release 6.0.0, ADM0 and ADM1. Runfola et al., "geoBoundaries: A global database of political administrative boundaries," *PLoS ONE* 15(4): e0231866 (2020). CC BY 4.0. The country lines are the U.S. Department of State's Large Scale International Boundaries. Read Nov. 22 and 26, 2026. Used for the countries, the coast, the disputed areas, Hong Kong and Macau.
- geoBoundaries gbOpen, China ADM2 (boundary id CHN-ADM2-17275852), "County Level", 2,391 units. Its source is the county lines of the National Administration of Surveying, Mapping and Geoinformation of China at 1:4,000,000, as Revolutionary GIS gave them out. Open Data Commons Public Domain Dedication and License 1.0. Read Nov. 26, 2026. Used for every line inside China. This file is called the boundary file below.
- 行政区划网 (xzqh.org), the pages "<province> <year> 年行政区划", 1964–1996: every county-level unit of each province at each year's end, by prefecture, and the year's changes as the State Council approved them. Read Nov. 26, 2026, a page a second. A list of facts; no text of the site is kept here but the changes the walk back used, each quoted in `crosswalk.json` with its year. This is called the record below. Its national pages for 1964, 1966 and 1967 give the provinces and their capitals.
- Wikidata (CC0), by its query service, read Nov. 26, 2026: the places' coordinates (P625) and their English Wikipedia articles. Two places take Wikipedia's own articles' items (Qianling Mausoleum, Yulin Naval Base).

Not used, and why: geoBoundaries gbOpen China ADM3 (today's 2,867 county-level units, from OpenStreetMap, ODbL) is finer but is of 2017, names many units in other languages than the record's, and would put the file under a share-alike licence. The University of Michigan China Data Center's "China historical 1964 county population census data" (Harvard Dataverse, hdl:1902.6/UZLUG) holds true 1964 county lines with the 1964 census. It is a commercial product with no open licence, and it was not read.

## The provinces of 1966

The record gives the province-level units of 1966: Peking and Shanghai, 21 provinces (and Taiwan, which the PRC counted), and five autonomous regions (Inner Mongolia, Guangxi, Ningxia, Xinjiang, Tibet). The map has these 28, with Hong Kong and Macau as the colonies they were and Taiwan as a country of the map. Checked against the record:

- Tianjin is in Hebei. It was Hebei's from February 1958 and a municipality again from Jan. 2, 1967. Hebei's capital moved from Tianjin to Baoding in April 1966.
- Hainan is in Guangdong. It became a province in 1988.
- Chongqing is in Sichuan. It became a municipality in 1997.
- Tibet is the Tibet Autonomous Region, set up in September 1965. At the end of 1964 it was under its Preparatory Committee.
- Guangxi has its coast. The Qinzhou area went from Guangdong to Guangxi in June 1965. So the counties of Hepu, Qinzhou, Lingshan and Dongxing are in Guangdong's list of 1964 and inside the Guangxi of 1966 on the map.
- Inner Mongolia is in its shape before July 1969, when its east and west were given to five neighbours. They came back in 1979, so today's shape is nearly that of 1966.
- A line that moved by less than a county since 1966 is not put back.

How they are drawn. The first version of `base.py` (Nov. 22) took the province lines from CGAZ ADM1. They were checked on Nov. 26 against places whose province is not in doubt and found to lie up to 13 km off: Nanxiong (Guangdong) fell 7 km inside Jiangxi, Qiaojia (Yunnan) 13 km inside Sichuan, Feng county (Shaanxi) 9 km inside Gansu, Linzhang (Hebei) inside Henan. So the provinces are now dissolved from the boundary file's counties, as the Republic of Vietnam's provinces were from its districts. CGAZ ADM1 is used only to tell which province a county lies in, and a county near a line is given to the province whose list has its name. The four places above now fall right, but for Linzhang (below).

Other adjustments, in `base.py`'s order:

1. The countries are CGAZ ADM0, cut to the frame. The Soviet republics are one country. Bangladesh is East Pakistan, Myanmar is Burma. Their lines are today's.
2. CGAZ's disputed areas are kept as areas of their own, in the land colour, their lines dashed: Aksai Chin, the three small sectors of the line with India (CGAZ's "CH-IN", Demchok, Dramana-Shakatoe), Kalapani and Siachen-Saltoro. The Paracels, the Senkakus and Liancourt are left out. Arunachal Pradesh is in India, as CGAZ has it.
3. Hong Kong and Macau are CGAZ ADM1's with the boundary file's own units for them. CGAZ's Hong Kong alone is only the north of the New Territories.
4. Each county of the boundary file is cut to CGAZ's China. A sliver of China no county covers goes to the nearest county.
5. The whole is cleaned as one coverage (`shapely.coverage_clean`) and simplified together at 0.008 degree, about 800 m (`coverage_simplify`), so neighbours meet. Islets under 4 km² are dropped.
6. Each line is drawn once, at its highest rank: coast, international, disputed, province, county.

## The counties of 1964

No open map of the counties of the 1960s was found. The counties are those of the end of 1964, after the mergers of 1958–61 had been undone. Each is drawn as a union of units of the boundary file.

The boundary file gives no year and names its units in pinyin without tones. Matched against the record's lists year by year, its names fit 1994 best (1,768 of 2,354 units by the same pinyin in the unit's own province; 1,691 for 1989 and 1,750 for 1996). So it is taken as of 1994. This is nearer 1964 than today's lines are, and it already draws a city's districts as one unit.

Step 1, the name. Each unit of the file is matched to a unit of the record's list for its province (`match` in `crosswalk.json`):

| how | units |
|---|---|
| the same pinyin, in the 1994 list | 1,764 |
| the same pinyin, in another year's list (1980–96) | 116 |
| the same pinyin, in the list of a province within 0.3 degree (CGAZ's province line is off) | 61 |
| a spelling two letters or fewer off (the file has slips: "Gaotangixan") | 230 |
| a looser spelling, in its own province: a guess | 42 |
| one character read another way (the file reads 柘城 as "Tuocheng"), in the prefecture its neighbours are in | 21 |
| no match | 119 |

Two names of one pinyin in a province (魏县 and 威县 in Hebei) are told apart by the prefecture their neighbours are in. Where far-apart units took one name, the better match keeps it.

Step 2, the walk back. Each matched unit is walked back a year at a time to 1964 through its province's lists (`basis`):

- `same` (1,901 counties): the list of each year before holds the name, or the name with another kind (a county made a city, an autonomous county). A name the lists spell two ways (刚察县, 冈察县) and a year's list that drops a prefecture are passed over.
- `renamed` (51): the year's changes say the unit took a new name.
- `moved` (40): the name is in another province's list the year before. These are Inner Mongolia's leagues of 1969–79, the Qinzhou area of 1965, and Hainan's and Chongqing's units in Guangdong's and Sichuan's lists.
- `part` (39): the year's changes say a later unit was set up or restored from one unit's ground. The later unit goes whole to that unit.
- `first of several` (33, a guess): the changes name several units it was taken from. It goes whole to the first named.
- `paired` (17, a guess): the changes are not given, and one name leaves the list as the other enters it (晋县, 晋州市).

Each kind of case, as drawn:

- A county that kept its name and place is the later unit.
- A city is the later city. It is larger than the city of 1964: the file draws the city with the suburbs it had in 1994. 152 cities are drawn so.
- A county since made a city, a district or an autonomous county is the later unit under its 1964 name.
- A county made or divided after 1964 does not appear. Its ground is inside the 1964 county it was taken from. Where it was taken from two or three, the line between them is off by that much. 98 counties are made of more than one later unit.
- A county joined to another before 1994 cannot be drawn apart. It is listed in `counties.json` under `not_shown`.

The counts. 2,081 counties, cities and like units of 1964 are drawn (1,816 counties, 152 cities, 59 autonomous counties, 47 banners, 3 autonomous banners, 4 others). 89 of them rest on a guess: 39 on a loose spelling, 33 on the first of several, 17 on a pairing. A tap on a county says which.

160 later units are shown as they are, under their later names, and a tap says so:

- 62 in Zhejiang. The record's pages for Zhejiang's years could not be had: its list for the province links the years from 2007 on, and its other address for a province's years answered for one year only between 1964 and 1996 (1982), with counts and no list. The whole province shows the units of 1994.
- 56 whose name was not found in the lists (the file's spelling is too far off, or the name is another province's).
- 42 that were not traced back: the name is new in some year and that year's changes are not given. The record's changes are thin for 1964–71.

153 units of the record's 1964 lists are not shown. 14 are counties since joined to the city of their name. The other 139 are units no unit of the file walked back to: counties joined to a neighbour before 1994, units the file does not have, and the other side of the 98 later units above that were not matched or traced. The record's 1964 lists hold 2,235 names outside Zhejiang. The record's own national count for the end of 1964 is 2,037 counties and like units and 207 cities.

Known faults. The file has no unit for some counties that existed throughout, and their ground is inside a neighbour's: Linzhang (Hebei) is inside the file's Anyang county, so the place Linzhang falls in Henan. The file's lines lie a few kilometres off in places (1:4,000,000). A county's name is put in pinyin by rule from its characters (`pypinyin`), so a character with an unusual reading may be wrong (蔚县 is Yu, the rule gives Wei), and a name in Mongolian, Tibetan or Uighur is the pinyin of its Chinese form. The characters are given beside it.

## The places

The places are the calendar's own gazetteer, `sources/places.yaml`: every row whose `in:` is `prc` or `roc`, and Hong Kong and Macau. On Nov. 26, 2026 that is 396 places. `places.json` holds a row for each, keyed by the gazetteer's key.

- 363 have a point: Wikidata's coordinates for the item chosen, never guessed. The rule the item was chosen by is in the row (`why`): the province the entries' text names beside the place (220); Wikipedia's article of that bare name (47); the one place of the name (37); the one city or county of the name (10); or by hand from the entries' own words (49, each with its ground: a county since renamed takes the point of the unit that followed it).
- 25 are provinces named as places (`area`). They have no point. A tap on the province lists their entries.
- 8 are not on the map (`unplaced`), each with its reason: Niujiao (241 entries, a village of Chang'an county), Tianhua (20), Taoyuan (7), Nanxucheng (5), Wangjiawan (4), Mingshui (2), Lingbei (1) and Qiliqin Island (1). Neither Wikidata nor Wikipedia has them, or the entries do not say which of several places is meant.

The province of 1966 and the county of 1964 are found by point in polygon, so they are as approximate as the lines. A point of a place in the PRC that falls just outside it (Changbai Shan, on the Korean line) takes the nearest unit within 0.3 degree. Six points fall in no county: Hong Kong, Taipei, the Gulf of Tonkin, Changbai Shan, and Gulangyu and Shantou, which lie on islets the simplifying dropped.

The Chinese name beside each place is the item's label at Wikidata, in simplified characters.
