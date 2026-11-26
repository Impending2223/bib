# China: borders, provinces of 1966, counties of 1964, places

The data of the map of China (`tools/bib/cnmap.py`, `build/china.html`), drawn in the browser by MapLibre GL JS with the maps of Indochina's client. Made on Nov. 26, 2026, by the one-time scripts in `tools/cnmap/`. Each script's docstring names its downloads, where they came from and every step. The downloads are not kept here. The guide: `notes/guide/china-map.md`. The Republic of China's counties and cities were added the same day (the owner, Nov. 25, 2026: "Give Formosa and Free China their ROC subdivisions"), by `tools/cnmap/roc.py` and a second run of `base.py`. That run changed nothing else: every area, line and label of the PRC came out the same to the last digit, and only Taiwan's coast and the county lines there differ.

## Files

| file | bytes | what | made by |
|---|---|---|---|
| `admin.geojson` | 2,359,212 | the borders: the countries (`k: land`), the disputed areas (`disp`), the 32 units of 1966 (`unit`: the PRC's 28, Hong Kong, Macau, and the Republic of China's two provinces), the lines by rank (`line`: `coast`, `disp`, `intl`, `unit`), label points (`lab`) | `base.py` |
| `counties.geojson` | 4,417,400 | the counties: 2,300 areas (`k: county`; 2,276 in the PRC, 24 of the Republic of China), their lines where no heavier line runs (`line`, `county`), label points (`lab`) | `base.py` |
| `units.json` | 6,292 | each unit of 1966: id, name, kind, the provinces of today it holds, km² | `base.py` |
| `counties.json` | 822,223 | each county drawn: id, name, the name in Chinese, kind, unit of 1966, province and prefecture of 1964, the later units it is made of and on what basis, `guess`; the later units shown as they are (`later`); the Republic of China's units (`c: roc`), each with the townships and districts it is made of; the 1964 units not shown (`not_shown`) | `base.py`, `roc.py` |
| `crosswalk.json` | 709,939 | the record behind the counties: each unit of the boundary file, the name it was matched to and how, the 1964 unit it walks back to and the changes used; each province's 1964 list | `counties.py` |
| `places.json` | 115,372 | the calendar's gazetteer's places in China: Wikidata's coordinates (Wikipedia's for one), the rule the item was chosen by, the unit of 1966 and the county of 1964 | `places.py` |

Every file is plain longitude and latitude (WGS84). Nothing is projected by hand. The frame is lon 66–142 E, lat 10–58 N (`FRAME` in `base.py`). The map's bounds lie inside it (lon 67–141, lat 11–57). The page's first view is lon 73–135.5, lat 17.5–54.

## Sources and licences

- geoBoundaries, Comprehensive Global Administrative Zones (CGAZ), release 6.0.0, ADM0 and ADM1. Runfola et al., "geoBoundaries: A global database of political administrative boundaries," *PLoS ONE* 15(4): e0231866 (2020). CC BY 4.0. The country lines are the U.S. Department of State's Large Scale International Boundaries. Read Nov. 22 and 26, 2026. Used for the countries, the coast, the disputed areas, Hong Kong and Macau.
- geoBoundaries gbOpen, China ADM2 (boundary id CHN-ADM2-17275852), "County Level", 2,391 units. Its source is the county lines of the National Administration of Surveying, Mapping and Geoinformation of China at 1:4,000,000, as Revolutionary GIS gave them out. Open Data Commons Public Domain Dedication and License 1.0. Read Nov. 26, 2026. Used for every line inside China. This file is called the boundary file below.
- 行政区划网 (xzqh.org), the pages "<province> <year> 年行政区划", 1964–1996: every county-level unit of each province at each year's end, by prefecture, and the year's changes as the State Council approved them. Read Nov. 26, 2026, a page a second. A list of facts; no text of the site is kept here but the changes the walk back used, each quoted in `crosswalk.json` with its year. This is called the record below. Its national pages for 1964, 1966 and 1967 give the provinces and their capitals.
- g0v's twgeojson (github.com/g0v/twgeojson), the file `json/twTown1982.geo.json`, read Nov. 26, 2026 (sha256 e8f6e19f…0fcbb2): Taiwan's townships, county-administered cities and districts, 368 units in 377 features. The repository's README says the files are made from the boundary files that the Institute of Transportation, Ministry of Transportation and Communications, gave out, and its author waives all rights in the package (CC0 1.0). The file's name says 1982. Its units are those of after Dec. 25, 2010 and before Dec. 25, 2014: it has New Taipei City, it has Taichung, Tainan and Kaohsiung each as one city, and it still has Taoyuan as a county. Used for the lines inside Taiwan, the Pescadores, Kinmen and Matsu. This is called the township file below.
- Wikidata (CC0), by its query service, read Nov. 26, 2026: the places' coordinates (P625) and their English Wikipedia articles. Two places take Wikipedia's own articles' items (Qianling Mausoleum, Yulin Naval Base). Wikidata's points for about 120 county names were also read to check the boundary file's names (below).
- Wikipedia (en.wikipedia.org's API, `prop=coordinates`), read Nov. 26, 2026: the coordinates of one place, Binyang county, where Wikidata's point is wrong.

Not used, and why: geoBoundaries gbOpen China ADM3 (today's 2,864 county-level units, from OpenStreetMap, ODbL) is finer but is of 2017, names many units in other languages than the record's, and would put the file under a share-alike licence. It was read once, to find the units of the boundary file whose names do not fit their place (below). Nothing of it is kept, and no name rests on it alone. The University of Michigan China Data Center's "China historical 1964 county population census data" (Harvard Dataverse, hdl:1902.6/UZLUG) holds true 1964 county lines with the 1964 census. It is a commercial product with no open licence, and it was not read. For Taiwan, the government's own township file (鄉鎮市區界線, the National Land Surveying and Mapping Center, data.gov.tw dataset 7441, under the Open Government Data License) is the better source. Its host, www.tgos.tw, refused this machine on Nov. 26, 2026 (HTTP 403), so it was not read. geoBoundaries' own Taiwan townships (gbOpen TWN ADM2) come from OpenStreetMap under a share-alike licence, and were not used for the reason given above.

## The provinces of 1966

The record gives the province-level units of 1966: Peking and Shanghai, 21 provinces (and Taiwan, which the PRC counted), and five autonomous regions (Inner Mongolia, Guangxi, Ningxia, Xinjiang, Tibet). The map has these 28, with Hong Kong and Macau as the colonies they were. Taiwan is a country of the map and keeps the one name, "Taiwan". It is drawn by the Republic of China's own two provinces, Taiwan and Fujian (Kinmen and Matsu), in the tint the other provinces have (below, "The Republic of China's counties and cities"). Checked against the record:

- Tianjin is in Hebei. It was Hebei's from February 1958 and a municipality again from Jan. 2, 1967. Hebei's capital moved from Tianjin to Baoding in April 1966.
- Hainan is in Guangdong. It became a province in 1988.
- Chongqing is in Sichuan. It became a municipality in 1997.
- Tibet is the Tibet Autonomous Region, set up in September 1965. At the end of 1964 it was under its Preparatory Committee.
- Guangxi has its coast. The Qinzhou area went from Guangdong to Guangxi in June 1965. So the counties of Hepu, Qinzhou, Lingshan and Dongxing are in Guangdong's list of 1964 and inside the Guangxi of 1966 on the map.
- Inner Mongolia is in its shape before July 1969, when its east and west were given to five neighbours. They came back in 1979, so today's shape is nearly that of 1966.
- A line that moved by less than a county since 1966 is not put back.

How they are drawn. The first version of `base.py` (Nov. 22) took the province lines from CGAZ ADM1. They were checked on Nov. 26 against places whose province is not in doubt and found to lie up to 13 km off: Nanxiong (Guangdong) fell 7 km inside Jiangxi, Qiaojia (Yunnan) 13 km inside Sichuan, Feng county (Shaanxi) 9 km inside Gansu, Linzhang (Hebei) inside Henan. So the provinces are now dissolved from the boundary file's counties, as the Republic of Vietnam's provinces were from its districts. CGAZ ADM1 is used only to tell which province a county lies in, and a county near a line is given to the province whose list has its name. The four places above now fall right.

Other adjustments, in `base.py`'s order:

1. The countries are CGAZ ADM0, cut to the frame. The Soviet republics are one country. Bangladesh is East Pakistan, Myanmar is Burma. Their lines are today's.
2. CGAZ's disputed areas are kept as areas of their own, in the land colour, their lines dashed: Aksai Chin, the three small sectors of the line with India (CGAZ's "CH-IN", Demchok, Dramana-Shakatoe), Kalapani and Siachen-Saltoro. The Paracels, the Senkakus and Liancourt are left out. Arunachal Pradesh is in India, as CGAZ has it.
3. Hong Kong and Macau are CGAZ ADM1's with the boundary file's own units for them. CGAZ's Hong Kong alone is only the north of the New Territories.
4. Each county of the boundary file is cut to CGAZ's China. A sliver of China no county covers goes to the nearest county. Sixteen units lie where the CGAZ province file has no province (the four units of the Weihai cape, the two of the Leizhou peninsula, Nanhui, Yadong, and islands). The first run left them out, and their ground went to a neighbour. They are now given their province by hand (`PROVINCE` in `counties.py`).
5. The whole is cleaned as one coverage (`shapely.coverage_clean`) and simplified together at 0.008 degree, about 800 m (`coverage_simplify`), so neighbours meet. Islets under 4 km² are dropped.
6. Each line is drawn once, at its highest rank: coast, disputed, international, province, county. A disputed area's line is dashed on both its sides. (The first run ranked the international line higher, and no dashed line was left.)
7. Taiwan is no longer one area. CGAZ's Taiwan (which holds the Pescadores, Kinmen and Matsu) is cut into the Republic of China's counties and cities, each a union of the township file's units, cut to CGAZ's coast. They are cleaned and simplified in the same coverage as everything else. The two provinces are dissolved from them. No name is set at a province's label point there, so the island's one name stays the country's.

## The counties of 1964

No open map of the counties of the 1960s was found. The counties are those of the end of 1964, after the mergers of 1958–61 had been undone. Each is drawn as a union of units of the boundary file.

The boundary file gives no year and names its units in pinyin without tones. Matched against the record's lists year by year, its names fit 1990 and 1994 best (1,813 and 1,812 of 2,369 units by the same pinyin in the unit's own province; 1,734 for 1989 and 1,794 for 1996). The later year is taken, since the file has cities made in 1994 (Luquan, Shenzhou). So it is taken as of 1994. This is nearer 1964 than today's lines are, and it already draws a city's districts as one unit.

Step 1, the name. Each unit of the file is matched to a unit of the record's list for its province (`match` in `crosswalk.json`):

| how | units |
|---|---|
| by its place, by hand (below) | 49 |
| the same pinyin, in the 1994 list | 1,796 |
| the same pinyin, in another year's list (1980–96) | 118 |
| the same pinyin, in the list of a province within 0.3 degree (CGAZ's province line is off) | 59 |
| a spelling two letters or fewer off (the file has slips: "Gaotangixan") | 192 |
| a looser spelling, in its own province: a guess | 37 |
| one character read another way (the file reads 荥经 as "Yongjing"), in the prefecture its neighbours are in | 20 |
| no match | 98 |

Two names of one pinyin in a province (魏县 and 威县 in Hebei) are told apart by the prefecture their neighbours are in. Where far-apart units took one name, the better match keeps it.

The file's names, checked. The file gives some units another unit's name. It has two units named Chongmingxian, and one of them is Qingpu. Shanghai's counties each carry a neighbour's name. A unit named Anyangxian is Linzhang, in Hebei. Other names are too far from their own to match (Zhuanjiangxian for Qijiang, Liuxiangxian for Ningxiang). The first run matched these by name and drew the wrong county there. On Nov. 26 every matched unit was checked against today's county at its place (geoBoundaries ADM3, read for this alone). Each unit that did not fit was then checked against Wikidata's point for the county that should be there. 49 units are now named by their place (`NAMED` in `counties.py`, each with the file's name beside it): for each, Wikidata's point for the county of the new name falls inside the unit. Two slips of the record are set right as its pages are read: the character 灃 for 澧 (澧县, 临澧县), and 庆云县 printed 庆元县 in Shandong's lists.

Step 2, the walk back. Each matched unit is walked back a year at a time to 1964 through its province's lists (`basis`):

- `same` (1,959 counties): the list of each year before holds the name, or the name with another kind (a county made a city, an autonomous county). A name the lists spell two ways (刚察县, 冈察县) and a year's list that drops a prefecture are passed over. A unit joined to another after 1964 and restored later (辽阳县, joined to Liaoyang city in 1968, restored in 1980) is the unit of 1964.
- `renamed` (54): the year's changes say the unit took a new name.
- `moved` (40): the name is in another province's list the year before. These are Inner Mongolia's leagues of 1969–79, the Qinzhou area of 1965, and Hainan's and Chongqing's units in Guangdong's and Sichuan's lists.
- `part` (40): the year's changes say a later unit was set up or restored from one unit's ground. The later unit goes whole to that unit.
- `first of several` (29, a guess): the changes name several units it was taken from. It goes whole to the first named.
- `paired` (16, a guess): the changes are not given, and one name leaves the list as the other enters it (晋县, 晋州市).

Ten walks are settled by hand from the record's own words (`BACK` in `counties.py`, each with the sentence it rests on). The first run read a sentence wrongly for these. It took Panzhihua (渡口市, set up in 1965) from Chongqing, because a sentence of that year sets up Chongqing's 大渡口 district. It took Sanya from Haikou and Chaohu from Chu county, because a sentence listed those names first. Sanya is now Ya county (崖县), Chaohu is Chao county (巢县), Kuitun is Karamay's ground, Ulanhot is the Horqin Right Front Banner's. Panzhihua goes to Miyi and Wanshan to Yuping, each the first of the counties its sentence names, a guess. Tunliu (Shanxi) is in the lists only from 1972 and is shown as a later unit.

Each kind of case, as drawn:

- A county that kept its name and place is the later unit.
- A city is the later city. It is larger than the city of 1964: the file draws the city with the suburbs it had in 1994. 149 cities are drawn so.
- A county since made a city, a district or an autonomous county is the later unit under its 1964 name.
- A county made or divided after 1964 does not appear. Its ground is inside the 1964 county it was taken from. Where it was taken from two or three, the line between them is off by that much. 82 counties are made of more than one later unit.
- A county joined to another before 1994 cannot be drawn apart. It is listed in `counties.json` under `not_shown`.

The counts. 2,138 counties, cities and like units of 1964 are drawn (1,868 counties, 155 cities, 60 autonomous counties, 46 banners, 3 autonomous banners, 6 others). 79 of them rest on a guess: 34 on a loose spelling, 29 on the first of several, 16 on a pairing. A tap on a county says which.

138 later units are shown as they are, under their later names, and a tap says so (the owner, Nov. 25, 2026: "Show the later units"):

- 66 in Zhejiang. The record's pages for Zhejiang's years could not be had: its list for the province links the years from 2007 on, and its other address for a province's years answered for one year only between 1964 and 1996 (1982), with counts and no list. The whole province shows the units of 1994.
- 32 whose name was not found in the lists (the file's spelling is too far off, or the name is another province's).
- 40 that were not traced back: the name is new in some year and that year's changes are not given. The record's changes are thin for 1964–71.

96 units of the record's 1964 lists are not shown. 13 are counties since joined to the city of their name. The other 83 are units no unit of the file walked back to: counties joined to a neighbour before 1994, units the file does not have, and the other side of the 72 later units above that were not matched or traced. The record's 1964 lists hold 2,235 names outside Zhejiang. The record's own national count for the end of 1964 is 2,037 counties and like units and 207 cities.

Known faults. The check of the file's names found today's county of the same name at the same place for 1,618 of the 2,271 matched units. For about 610 no county of the name was found there (the county has a new name since, or today's name is not the Chinese one), and their names rest on the file alone. The rest are cities, whose districts have other names. The file has no unit for some counties that existed throughout, and their ground is inside a neighbour's. The file draws Jiading, Baoshan and Shanghai county inside the city of Shanghai. The file's lines lie a few kilometres off in places (1:4,000,000). The two parts of Dongying city both go to Lijin county, the first of the two counties the record names; the southern part was Kenli's and Guangrao's ground. A county's name is put in pinyin by rule from its characters (`pypinyin`, with six readings set right by hand: 都 du, 朝 chao, 长 chang, 漯 luo, 泊 bo, 涡 guo), so a character with an unusual reading may still be wrong, and a name in Mongolian, Tibetan or Uighur is the pinyin of its Chinese form. The characters are given beside it.

## The Republic of China's counties and cities

The owner, Nov. 25, 2026: "Give Formosa and Free China their ROC subdivisions." Taiwan, the Pescadores, Kinmen and Matsu are drawn by the Republic of China's own units as they stood through the 1960s until July 1967: two provinces, and under them 24 counties, cities and like units. They show with the Counties box, as the PRC's counties do. The method is the one used for the PRC's counties: a later boundary file's units, each given whole to the unit of the 1960s that held it. The whole record is the table in `tools/cnmap/roc.py`.

- Taiwan Province (36,163 km² as drawn): 16 counties (Taipei, Ilan, Taoyuan, Hsinchu, Miaoli, Taichung, Changhua, Nantou, Yunlin, Chiayi, Tainan, Kaohsiung, Pingtung, Taitung, Hualien, Penghu), 5 provincial cities (Taipei, Keelung, Taichung, Tainan, Kaohsiung) and the Yangmingshan Administrative Bureau.
- Fujian Province (166 km² as drawn): Kinmen county (Quemoy) and Lienchiang county (Matsu).

The names are in the forms the Republic used then (Taipei, Keelung, Hsinchu, Kaohsiung), not in pinyin. Three carry the calendar's own name beside them: "Kinmen (Quemoy)", "Lienchiang (Matsu)", "Penghu (Pescadores)". The characters are given in the tap's line.

Each adjustment, from the township file's units back to the 1960s:

1. Taipei city. It was a provincial city until July 1, 1967, and a special municipality after. On July 1, 1968 it took six townships: Neihu, Nangang, Muzha and Jingmei from Taipei county, and Shilin and Beitou from the Yangmingshan Administrative Bureau. On Mar. 12, 1990 its sixteen districts were redrawn as twelve. So the city as it stood is drawn as seven of today's districts: Zhongzheng, Datong, Zhongshan, Songshan, Da'an, Wanhua and Xinyi. These are the ten districts of before 1968 in the district lines of 1990. The city comes to 64 km² as drawn. Its line with the six townships is the line of 1990, which may differ from the line of 1968 by a few streets.
2. The Yangmingshan Administrative Bureau is today's Shilin and Beitou districts. It was a unit of the province at the county's level from 1949, and held those two townships until they went to Taipei city in 1968.
3. Taipei county is today's New Taipei City (the county's name from Dec. 25, 2010) with today's Neihu, Nangang and Wenshan districts of Taipei. Wenshan is Muzha and Jingmei, joined in 1990.
4. Hsinchu county holds today's Hsinchu city, and Chiayi county holds today's Chiayi city. Each city was a city of its county from 1951 to July 1, 1982. Hsinchu city took Xiangshan township when it left the county, and Xiangshan is with the county here too.
5. Taichung, Tainan and Kaohsiung. Each city and its county were joined on Dec. 25, 2010. The city of the 1960s is the districts the city had before that day, and the county is the rest: Taichung city is 8 districts (Central, East, South, West, North, Xitun, Nantun, Beitun); Tainan city is 6 (East, South, North, West Central, Annan, Anping; West and Central were two districts until 2004, both the city's); Kaohsiung city is 10 (Yancheng, Gushan, Zuoying, Nanzi, Sanmin, Xinxing, Qianjin, Lingya, Qianzhen, Qijin).
6. Xiaogang went from Kaohsiung county to Kaohsiung city on July 1, 1979. It is with the county here.
7. The file sets nine harbour waters apart from their districts ("前鎮區(海)"). Each is put back in its district. They lie off CGAZ's coast and add no land.
8. Keelung, Penghu, Kinmen, Lienchiang and the other eleven counties are the file's units of the name, whole. Taoyuan was a county until 2014.

Known faults. A township line that moved between the 1960s and 2010 is not put back, so a county's line is exact only where it follows a township line that has not moved. The coast is CGAZ's, not the township file's. Islets under 4 km² are dropped with the rest of the map's: Dongyin and the Juguang islands of Lienchiang, Wuqiu of Kinmen, and the Pratas and Taiping islands. So Lienchiang is Nangan and Beigan alone, 16 km². The dates above are as the Republic's own record gives them in general reference works. They could not be read again from this machine on Nov. 26, 2026, since Wikipedia's API answered 429 to every request. Check: the dates of items 1, 2, 4 and 6 against a source.

## The places

The places are the calendar's own gazetteer, `sources/places.yaml`: every row whose `in:` is `prc` or `roc`, and Hong Kong and Macau. On Nov. 26, 2026 that is 396 places. `places.json` holds a row for each, keyed by the gazetteer's key.

- 362 have a point: Wikidata's coordinates for the item chosen, never guessed (for Binyang county, Wikipedia's: Wikidata's point for it lies 70 km off). The rule the item was chosen by is in the row (`why`): the province the entries' text names beside the place (215); Wikipedia's article of that bare name (47); the one place of the name (37); the one city or county of the name (10); or by hand from the entries' own words (53, each with its ground: a county since renamed takes the point of the unit that followed it). Three of the 53 were set right on Nov. 26 after the rule had chosen wrongly: Xin'an (the seat of Anxin county, by Baiyangdian; the rule took a town of the name in Zhengding), Xincheng county (Gaobeidian since 1993; the rule took a town in Xinji) and Qijiang (the county; the rule took the river).
- 25 are provinces named as places (`area`). They have no point. A tap on the province lists their entries.
- 9 are not on the map (`unplaced`), each with its reason: Niujiao (241 entries, a village of Chang'an county), Tianhua (20), Taoyuan (7), Nanxucheng (5), Wangjiawan (4), Mingshui (2), Lingbei (1), Qiliqin Island (1) and Longnan (1). Neither Wikidata nor Wikipedia has them, or the entries do not say which of several places is meant. For Longnan, Jiangxi, both sources give one point, and it lies 100 km north of the county, so it is not taken.

The province of 1966 and the county of 1964 are found by point in polygon, so they are as approximate as the lines. A point of a place in the PRC that falls just outside it (Changbai Shan, on the Korean line) takes the nearest unit within 0.3 degree. A point that falls outside the county of its own name, but within 5 km of it, takes that county and its province (`near` in the row). There are five: Chishui (on the river that is Guizhou's line with Sichuan), Jiange, Shantou, Wu county and Zhangzhou. Four points fall in no county: Hong Kong, the Gulf of Tonkin, Changbai Shan, and Gulangyu, an islet the simplifying dropped. Taipei, the one place of the gazetteer in the Republic of China, falls in Taipei city of Taiwan Province. Its row was made again by `places.py --roc`, which takes the unit and the county by point in polygon from the files as they are and reads nothing from Wikidata. Every point of a county or city was checked against the county of its name on the map (287 places). Four still fall in a neighbour's ground, by the lines or by the history: Dandong (in Andong county, 3 km from the city), Dongying (in Kenli), Huangshan (in She county, 1 km from Taiping) and Xuanhua (in the city of Zhangjiakou, which held it in 1964).

The Chinese name beside each place is the item's label at Wikidata, in simplified characters.
