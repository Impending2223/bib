# China: borders, provinces of 1966, counties of 1964, places; relief, rivers and lakes, climate, rain, population, cities

The data of the map of China (`tools/bib/cnmap.py`, `build/china.html`), drawn in the browser by MapLibre GL JS with the maps of Indochina's client. Made on Nov. 26, 2026, by the one-time scripts in `tools/cnmap/`. Each script's docstring names its downloads, where they came from and every step. The downloads are not kept here. The guide: `notes/guide/china-map.md`. The Republic of China's counties and cities were added the same day (the owner, Nov. 25, 2026: "Give Formosa and Free China their ROC subdivisions"), by `tools/cnmap/roc.py` and a second run of `base.py`. That run changed nothing else: every area, line and label of the PRC came out the same to the last digit, and only Taiwan's coast and the county lines there differ.

## Files

| file | bytes | what | made by |
|---|---|---|---|
| `admin.geojson` | 2,359,212 | the borders: the countries (`k: land`), the disputed areas (`disp`), the 32 units of 1966 (`unit`: the PRC's 28, Hong Kong, Macau, and the Republic of China's two provinces), the lines by rank (`line`: `coast`, `disp`, `intl`, `unit`), label points (`lab`) | `base.py` |
| `counties.geojson` | 4,417,400 | the counties: 2,300 areas (`k: county`; 2,276 in the PRC, 24 of the Republic of China), their lines where no heavier line runs (`line`, `county`), label points (`lab`) | `base.py` |
| `units.json` | 6,292 | each unit of 1966: id, name, kind, the provinces of today it holds, km² | `base.py` |
| `counties.json` | 822,223 | each county drawn: id, name, the name in Chinese, kind, unit of 1966, province and prefecture of 1964, the later units it is made of and on what basis, `guess`; the later units shown as they are (`later`); the Republic of China's units (`c: roc`), each with the townships and districts it is made of; the 1964 units not shown (`not_shown`) | `base.py`, `roc.py` |
| `crosswalk.json` | 709,939 | the record behind the counties: each unit of the boundary file, the name it was matched to and how, the 1964 unit it walks back to and the changes used; each province's 1964 list | `counties.py` |
| `places.json` | 127,021 | the calendar's gazetteer's places in China: Wikidata's coordinates (Wikipedia's for one), the rule the item was chosen by, the unit of 1966 and the county of 1964 | `places.py` |

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

The places are the calendar's own gazetteer, `sources/places.yaml`: every row whose `in:` is `prc` or `roc`, and Hong Kong and Macau. On Nov. 26, 2026 that is 430 places: 396 that calendar entries name, and 34 cities of the UN *Demographic Yearbook* that no entry names yet (the owner, Nov. 25, 2026: "Add the cities to the gazetteer"; below, "The Yearbook's cities"). `places.json` holds a row for each, keyed by the gazetteer's key.

- 396 have a point: Wikidata's coordinates for the item chosen, never guessed (for Binyang county, Wikipedia's: Wikidata's point for it lies 70 km off). The rule the item was chosen by is in the row (`why`): the province the entries' text names beside the place (215); Wikipedia's article of that bare name (47); the one place of the name (37); the one city or county of the name (10); by hand from the entries' own words (53, each with its ground: a county since renamed takes the point of the unit that followed it); or the Yearbook's city of the name (34). Three of the 53 were set right on Nov. 26 after the rule had chosen wrongly: Xin'an (the seat of Anxin county, by Baiyangdian; the rule took a town of the name in Zhengding), Xincheng county (Gaobeidian since 1993; the rule took a town in Xinji) and Qijiang (the county; the rule took the river).
- 25 are provinces named as places (`area`). They have no point. A tap on the province lists their entries.
- 9 are not on the map (`unplaced`), each with its reason: Niujiao (241 entries, a village of Chang'an county), Tianhua (20), Taoyuan (7), Nanxucheng (5), Wangjiawan (4), Mingshui (2), Lingbei (1), Qiliqin Island (1) and Longnan (1). Neither Wikidata nor Wikipedia has them, or the entries do not say which of several places is meant. For Longnan, Jiangxi, both sources give one point, and it lies 100 km north of the county, so it is not taken.

The province of 1966 and the county of 1964 are found by point in polygon, so they are as approximate as the lines. A point of a place in the PRC that falls just outside it (Changbai Shan, on the Korean line) takes the nearest unit within 0.3 degree. A point that falls outside the county of its own name, but within 5 km of it, takes that county and its province (`near` in the row). There are six: Chishui (on the river that is Guizhou's line with Sichuan), Jiange, Shantou, Wu county, Yantai and Zhangzhou. Five points fall in no county: Hong Kong, Macau, the Gulf of Tonkin, Changbai Shan, and Gulangyu, an islet the simplifying dropped. A place of Hong Kong or Macau whose point falls off the colony as drawn is in that colony: Macau's own point lies 1 km outside the 33 km² drawn for it. Taipei falls in Taipei city of Taiwan Province. Its row was made again by `places.py --roc`, which takes the unit and the county by point in polygon from the files as they are and reads nothing from Wikidata. Every point of a county or city was checked against the county of its name on the map (287 places). Four still fall in a neighbour's ground, by the lines or by the history: Dandong (in Andong county, 3 km from the city), Dongying (in Kenli), Huangshan (in She county, 1 km from Taiping) and Xuanhua (in the city of Zhangjiakou, which held it in 1964).

### The Yearbook's cities

The owner, Nov. 25, 2026: "Add the cities to the gazetteer." The map's Cities layer shows 116 cities of the UN *Demographic Yearbook* (below, "Cities"). 82 were places of the gazetteer already. The other 34 were made places of it on Nov. 26, 2026, each with a row in `sources/places.yaml` and a row here.

- The 34: on the mainland Anqing, Benxi, Changshu, Chaozhou, Fushun, Huainan, Huangshi, Liaoyang, Liaoyuan, Nantong, Ningbo, Shaoxing, Shaoyang, Siping, Taizhou (key `taizhou-jiangsu`), Weifang, Wutongqiao, Wuzhou, Yangquan, Yangzhou, Yantai and Zibo; in Taiwan Changhua, Chiayi, Chungli, Hsinchu, Kaohsiung, Keelung, Panchiao, Pingtung, Sanchung, Taichung and Tainan; and Macau.
- None was in the gazetteer under another spelling. Each was looked for by its key, by its name, by the Yearbook's name, by its Wikidata item among the map's rows, and by any place of the map within 30 km.
- The gazetteer's rows. The mainland's names are in pinyin, as the calendar writes them, with the zone `Asia/Shanghai` and `in: prc`. Taiwan's are in the forms the Republic used, which are also the calendar's (it writes Keelung and Tainan), with `Asia/Taipei` and `in: roc`. Macau's key is `macau`, the key the map's code knows. Its name is "Macao", as the series writes it (42 times, against once for "Macau"). Its zone is `Asia/Macau`, its polity `portugal`, and `macao` is an alias.
- The points. Each place takes the Wikidata item the cities' file held for it (`CITY` in `places.py`), and the script makes its row as it makes a place settled by hand. A run of the whole script on Nov. 26, 2026 gave the 396 older rows again unchanged, and the 34 new ones at the points the cities' file held. Wikidata gives Changshu's item two points 1.6 km apart. The one the cities' file held is kept (`POINT` in `places.py`).
- The units, by point in polygon. Taiwan's cities fall in the Republic's units of the 1960s: Sanchung and Panchiao in Taipei county, Chungli in Taoyuan county, Chiayi and Hsinchu in the counties that held them, Changhua and Pingtung in their counties, and Kaohsiung, Tainan, Taichung and Keelung in the cities of their names. Chaozhou falls in Chao'an county and Wutongqiao in Leshan county, since the map draws no unit of their own name. Huainan's point lies 14 km south of the city as the map draws it, in Changfeng county. It is Wikidata's point for the item, and it is kept. Check: Huainan's point against a map of the period.

The Chinese name beside each place is the item's label at Wikidata, in simplified characters.

## The layers: relief, rivers and lakes, climate, rain, population, cities

The owner, Nov. 25, 2026: "Which of the SEA map overlays can we also use on our China map? Bring them over." Made on Nov. 26, 2026. Each layer comes from the source of the same layer of the maps of Indochina (`sources/indochina/README.md`, which gives each source's full citation and licence). Each is made by the same script, `tools/vnmap/terrain.py`, `climate.py`, `population.py` and `layers.py`, run with the word `china`. The numbers that differ between the two maps are all in `tools/vnmap/frames.py`. The downloads are not kept here.

The frame. The tiles, the depths, the contours and the population cover the frame of the borders, lon 66–142 E, lat 10–58 N. The rivers, the lakes and the rain cover the map's bounds, lon 67–141 E, lat 11–57 N, which is all the map can show. Every file is plain longitude and latitude, or Web Mercator tiles in a PMTiles archive, as on the maps of Indochina. The PMTiles files are read by HTTP range requests.

### The choice of detail

China's frame is about thirty times Indochina's in area. The map of China opens about two zooms farther out than the map of Indochina: its first view is 62.5 degrees wide, Indochina's 10.5. Both maps zoom in to 64 times their first view. So each layer is made about four times as coarse as Indochina's. A cell or a line then has the same size on the screen on both maps, at the first view and at the deepest zoom. The aim was 40 MB or less for the layers together and no file over 20 MB. The first build came to 22.6 MB, the largest file 8.6 MB. The owner then chose a sharper relief over that aim (Nov. 25, 2026: "Make the relief sharp!"). The elevation tiles were remade a zoom deeper on Nov. 26, 2026 and are 30.8 MB. The layers now come to 44.9 MB (44,870,934 bytes).

| layer | Indochina | China | why |
|---|---|---|---|
| elevation tiles | zooms 0–8, from the 15″ model | zooms 0–6, from the 30″ model | Two zooms shallower, as the rule of four gives. The first build stopped at zoom 5 to keep the file under 20 MB (8,640,449 bytes). The owner, Nov. 25, 2026: "Make the relief sharp!" So the tiles go to zoom 6. Zoom 6 alone is 22.2 MB and the file is 30.8 MB. A zoom 6 pixel is about 1.2 km at the equator, 1.1 km at 30° N and 0.9 km at Peking's latitude. The 30″ grid's cell is about 930 m from north to south. So zoom 6 shows about all the grid holds. Zoom 7 would need the 15″ grid. It would be about four times zoom 6's bytes, which is over `check`'s limit for a file. |
| depths and contours | traced on a 1′ grid, simplified at 0.01° and 0.003° | traced on a 2′ grid, simplified at 0.04° and 0.012° | Twice as coarse a grid and four times the tolerance. |
| contour levels | 500, 1,000, 1,500, 2,000 m | 500, 1,000, 2,000, 3,000, 4,000, 5,000 m | Indochina's levels stop at 2,000 m. Tibet lies above 4,000 m. |
| elevation bands | seven, the last "2,000 m and over" | ten: the same six below 2,000 m, then 2,000–3,000, 3,000–4,000, 4,000–5,000, 5,000 m and over | The same reason. |
| rivers | 10 m³/s and over, simplified at 0.002°; in the delta every reach SWORD has | 30 m³/s and over, simplified at 0.008°; in the deltas SWORD's reaches of 50 m and wider | Four times as coarse a line. 30 m³/s is the least size the client gives a line width of its own (sizes 1 to 5). A channel of 50 m is the least of SWORD's that falls in those five sizes. |
| lakes | 1 km² and over, simplified at 0.001° | 10 km² and over, simplified at 0.004° | This map shows about sixteen times the ground to a pixel that Indochina's does. The client draws no lake under 3 km² on either map. |
| climate tiles | zooms 0–7 | zooms 0–6 | One zoom shallower. The file is small, so it is kept a zoom deeper than the rule of four gives. |
| rain | CRU's own cells, 10′ | cells of 30′, each the mean of 3 × 3 of CRU's | A cell of 30′ is as large on this map's first view as a cell of 10′ is on Indochina's. At 10′ the file would hold nine times the cells, about 33 MB. |
| population | the model's own cells, 5′ | cells of 15′, 3 × 3 of the model's summed | A cell of 15′ is as large on this map's first view as a cell of 5′ is on Indochina's. |

### Files

| file | bytes | what | made by |
|---|---|---|---|
| `dem.pmtiles` | 30,840,466 | land elevation, Terrarium-encoded lossless WebP tiles, 512 px, zooms 0–6, 258 tiles | `terrain.py` |
| `bathymetry.geojson` | 959,459 | the sea's depth bands | `terrain.py` |
| `contours.geojson` | 2,313,626 | contours at 500, 1,000, 2,000, 3,000, 4,000 and 5,000 m | `terrain.py` |
| `hypso.json` | 2,452 | the elevation bands' and depth bands' ranges and colours (the legend) | `terrain.py` |
| `rivers.geojson` | 1,264,483 | rivers of 30 m³/s and over; in seven deltas, the channels of 50 m and wider | `layers.py`, step `hydro` |
| `lakes.geojson` | 2,005,130 | lakes and reservoirs of 10 km² and over | `layers.py`, step `lakes` |
| `koppen.pmtiles` | 829,886 | Köppen–Geiger classes, 1961–1990, paletted PNG tiles, zooms 0–6 | `climate.py` |
| `koppen.json` | 3,120 | their legend: value, code, name, colour, share of the frame's land | `climate.py` |
| `climate.json` | 1,260,360 | monthly rainfall and mean temperature normals, 1961–1990, a grid of half a degree | `layers.py`, step `climate` |
| `climate.geojson` | 3,683,683 | the same grid as squares, a property a month | `climate.py` |
| `population.geojson` | 1,681,039 | persons a km², 1960 and 1970, modelled, in classes | `population.py` |
| `cities.yaml` | 27,230 | the cities' populations as the UN *Demographic Yearbook* printed them, by page | kept by hand |

`check` fails on a map file over 50 MB or the map's files over 60 MB together, the same rule as for Indochina's (`cnmap.problems`). It counts a MB as 1,048,576 bytes, so the limits are 52,428,800 bytes a file and 62,914,560 bytes together. With the borders and the counties the files the map draws are 50,354,384 bytes, and `dem.pmtiles` is 30,840,466 of them. So about 12.5 million bytes are left under the limit. A new layer of any size needs one of these files made smaller first. A browser fetches a layer's file only when its box is first ticked.

### Relief: `dem.pmtiles`, `bathymetry.geojson`, `contours.geojson`, `hypso.json`

- **Source:** NOAA NCEI, *ETOPO 2022 v1* global relief model, surface elevation, 30 arc-seconds, the one global file `ETOPO_2022_v1_30s_N90W180_surface.nc` (1.64 GB) from NCEI's THREDDS file server (`https://www.ngdc.noaa.gov/thredds/fileServer/global/ETOPO2022/30s/30s_surface_elev_netcdf/`). Public domain. doi:10.25921/fd45-gt74. Indochina's is the same model at 15 arc-seconds.
- **Land and sea:** as on the maps of Indochina. Land is what `admin.geojson` calls land (the countries, the units and the disputed areas), rasterized onto the grid. Land below sea level is counted 0 m. The sea is −1 m in the tiles.
- **Lakes raised to their surface.** The owner, Nov. 25, 2026: "Mend Lake Baikal." The model holds the floor of Lake Baikal, not its surface. Much of the floor lies below sea level and was counted 0 m, so the lake showed as a basin. `terrain.py` now raises the ground under such a lake to the lake's surface before it makes anything from the grid (`fill_lakes`; the frame's `lake_fill` in `frames.py`). The rule has two parts. The lake is one of HydroLAKES's of 10 km² or more, which are the lakes the Rivers box draws. And the median of the model's land cells under the lake lies more than 50 m below the surface height HydroLAKES gives for it. In such a lake every land cell the lake's shape touches that lies below that height is set to it. A cell at or above it, an island or a shore, is left. The frame holds 1,895 lakes of 10 km² or more, and three meet the rule. Baikal is the first: 60,490 of its 64,616 cells were raised to 449 m. Their median had been 298 m below sea level, and the lowest 1,191 m below. The other two are Lake Orel' and a lake beside it, by the mouth of the Amur. HydroLAKES puts both at 0 m, and the model puts their cells below sea level. The script already counted such cells 0 m, so nothing changed there. In every other lake the model holds the surface, within a few metres of HydroLAKES's height, and the lake is left as the model has it. The source is `HydroLAKES_polys_v10.shp` (CC BY 4.0; below, "Lakes"). The step is off for the maps of Indochina. No lake in their frame meets the rule (tested on the 30″ grid), so it would change nothing there, and their files were not remade.
- **The run:** `python3 -I tools/vnmap/terrain.py ETOPO_DIR china HydroLAKES_polys_v10.shp`, on Nov. 26, 2026. It took 20 minutes, nearly all of it the tiles.
- **Tiles:** made as Indochina's are, to zoom 6: bilinear at zooms 5 and 6, the mean below. The map draws the hillshade and the elevation bands from them. Past zoom 6 it enlarges the zoom 6 tiles. The map's deepest zoom is 64 times its first view, which was zoom 8.8 in a window 1,100 px wide. There a tile's pixel is drawn about seven times its size, so the relief is still soft at the deepest zoom. It was about fourteen times with the zoom 5 tiles. Pictures of Sichuan and the lower Yangtze at the deepest zoom, before and after, showed about twice the detail.
- **Bands:** land 0–100, 100–200, 200–500, 500–1,000, 1,000–1,500, 1,500–2,000, 2,000–3,000, 3,000–4,000, 4,000–5,000, 5,000 m and over. The first six colours are Indochina's. The band 2,000–3,000 m has the colour of Indochina's last band. The three above it run from brown into gray (#ac9a7c, #baae9a, #cac3b8), the usual tints of high ground on a relief map. The sea's depth bands and their colours are Indochina's. `terrain.py` writes `hypso.json` for this frame from the bands in `frames.py`.
- **Contours:** from the grid at 2′ (the mean of 4 × 4 cells), traced by contourpy, simplified at 0.012°, runs under 0.12° dropped. One MultiLineString a level. They were remade in the run that raised the lakes. Eight lines along Baikal's shores moved a little, five at 500 m and three at 1,000 m. No other line changed. The depth bands and `hypso.json` came out the same byte for byte.
- **Known faults.** Baikal stands at 449 m, HydroLAKES's height. The lake's level is usually given as about 456 m. The Turpan depression (to 154 m below sea level) is counted 0 m, as all land below sea level is. Lakes whose surface the model holds (Qinghai, Issyk Kul) are flat at the model's own height. The relief is still soft at the map's deepest zoom (above, "Tiles").

### Rivers: `rivers.geojson`

MultiLineString features, each the merged lines of one name and one size, drawn smallest first in file order. 2,112 features. Properties: `size` (1 the largest, 5 the smallest), `source` (`HydroRIVERS` or `SWORD`), and where known `name` (the source's English form). The file was 1,185,118 bytes before the deltas were drawn (Nov. 26, 2026) and is 1,264,483 bytes after.

- **Outside the deltas: HydroRIVERS v1.0, Asia** (`https://data.hydrosheds.org/file/HydroRIVERS/HydroRIVERS_v10_as_shp.zip`). Every segment in the map's bounds with a long-term mean discharge of 30 m³/s or more. `size` by discharge as on the maps of Indochina: 1, 5,000 m³/s and over; 2, 1,000–5,000; 3, 300–1,000; 4, 100–300; 5, 30–100. Simplified at 0.008°, coordinates to 0.001°. **Licence: the HydroSHEDS version 1 License Agreement (WWF)**, as stated in `sources/indochina/README.md`. The page `china.html` carries HydroSHEDS's statement in full.
- **Inside the deltas: SWORD v17c** (the SWOT Mission River Database; Zenodo, doi:10.5281/zenodo.22259077; CC BY 4.0; the full citation is in `sources/indochina/README.md`), the reaches of the Asian basins, read out of `SWORD_v17c_shp.zip` by HTTP range requests. The owner, Nov. 25, 2026: "Draw the river deltas." The method is that of the Mekong's delta on the maps of Indochina. HydroRIVERS cannot split a river, so it sends each river down one channel, and it stops where its own coast begins, which in an estuary lies far inland. SWORD maps every channel 30 m wide or more from Landsat. Inside a ring drawn by hand the rivers are SWORD's reaches, and outside it they are HydroRIVERS's segments, each cut at the ring. Each ring crosses a river where the two sources' lines lie together. The rings are in `tools/vnmap/frames.py` (`delta`). `size` by SWORD's width, as in Indochina's file: 1, 900 m and over; 2, 400–900; 3, 200–400; 4, 100–200; 5, 50–100. Reaches under 50 m wide are left out (`delta_min`), so that the deltas have the same five sizes as the rest of the map. Indochina's file keeps them, as a sixth size. 163 features, about 15,100 km of channels.
- **The seven deltas drawn**, with the length of their channels:
  - The Pearl River's (1,600 km): from the Xi above Sanshui, the Bei, the Liuxi and the Dong at Shilong to the sea. HydroRIVERS sent the Xi and the Bei down one channel and stopped the Dong short of the estuary.
  - The Han's and the Rong's, at Shantou (230 km): from Chaozhou and Jieyang to the sea. HydroRIVERS drew the Han to one mouth.
  - The Yangtze's (570 km): from Zhenjiang to the sea, with the channels round Yangzhong island, Chongming's north and south branches, and the Huangpu's mouth. HydroRIVERS stopped the Yangtze near Jiangyin, about 180 km from the sea.
  - The Yellow River's (130 km): from Lijin to the sea. SWORD has one channel here too, the same course as HydroRIVERS's, in a smoother line. It is today's mouth, and it runs about 25 km past the coast as the map draws it: the coast's file (CGAZ) does not have the ground at the river's mouth.
  - The Red River's and the Thái Bình's (1,220 km): from above Hanoi to the sea, with the Đáy on the west.
  - The Irrawaddy's (4,550 km): from above Henzada to the sea, with the Bassein river on the west and the Rangoon and Pegu rivers on the east. HydroRIVERS stopped the Irrawaddy about 60 km from the sea.
  - The Ganges's, the Brahmaputra's and the Meghna's (6,780 km): from the Hooghly above Calcutta and the Ganges above the Gorai to the Meghna's mouth, with the tidal channels of the Sundarbans. HydroRIVERS stopped the Padma at Chandpur.
- **Looked at and not drawn.** SWORD also draws more than HydroRIVERS's one channel at six other mouths in the frame: the Indus's, the Mahanadi's and the Brahmani's, the Godavari's, the Krishna's, the Kaladan's on the Arakan coast, and the Salween's at Moulmein. No ring was drawn for them. At the Chao Phraya's, the Liao's, the Hai's and the Amur's mouths the two sources agree. The Mekong's mouths lie south of the map's bounds, and from Phnom Penh down to the bounds HydroRIVERS has both the Mekong and the Bassac. The mouths of the Min at Fuzhou and the Jiulong at Xiamen, and the rivers of Korea and Japan, were not looked at.
- **Names:** SWORD v17c's `river_name`, for the reaches of every Asian basin (`as_sword_reaches_hb31`–`hb36` and `hb41`–`hb49`). A name is given to a HydroRIVERS segment by the method of the maps of Indochina. The names are SWORD's own English forms. 69 percent of the lines' points carry a name (72 percent before the deltas, whose smaller channels SWORD does not name). Spellings of one river are joined (`same` in `frames.py`): "Chang Jiang" is "Yangtze"; "Salween" and "Salween - Nujiang" are "Salween River"; "Ayeyarwady River" is "Irrawaddy River"; "Pathein River" is "Bassein River". SWORD names the Yangtze's south branch, from Chongming's head to the sea, "Hengli River", and that is joined to "Yangtze" too. Check: "Hengli River". The Yangtze, the Yellow River and the Amur keep their name to the sea. In a delta the Yangtze, the Yellow River, the Xi, the Han, the Red River, the Irrawaddy and the Ganges are carried to the sea through reaches SWORD leaves unnamed, by the widest branch at each split (`delta_to_sea`). So "Ganges" runs down the Padma and the lower Meghna, and "Xi River" down one channel of the Pearl River's delta. SWORD names the upper Yangtze "Jinsha River" and "Tongtian River", and the upper Mekong "Lancang River". **Not named:** the Red River in its delta, where SWORD names only the Đáy; most channels of the deltas; the Yarlung Tsangpo above the Brahmaputra; and most rivers under 100 m³/s. Two rivers of one name (the Min of Sichuan and the Min of Fujian, the two Gan, the several "Xi River") are one feature of that name. SWORD's names in the deltas are as it gives them, slips included ("Kapatakkha riever"), and one near Shantou is doubtful ("Ting River"). The period's names differ in Burma (SWORD's "Yangon River" and "Bago River" are the Rangoon and Pegu rivers). No Chinese form is given. Check a name against a map of the period before it goes into the series' prose.
- **Rivers are today's courses.** The reservoirs built since the 1960s flood stretches the rivers ran through then. The deltas' channels are those of Landsat's years, 1984 and after. The Yellow River's mouth is today's. In the 1960s the river reached the sea by another course, north of this one. Check: the Yellow River's courses of 1953–64 and 1964–76 against a map of the period. Neither source has them.

### Lakes: `lakes.geojson`

- **Source:** HydroLAKES v1.0 (`https://data.hydrosheds.org/file/hydrolakes/HydroLAKES_polys_v10_shp.zip`; CC BY 4.0). Every lake and reservoir of 10 km² or more in the map's bounds: 1,847, of which 1,376 are typed lake, 463 reservoir and 8 lake control. Simplified at 0.004°, largest first. Properties as in Indochina's file.
- **`dam_year`:** GRanD's year for a dam within about 2 km of the water body, from `Res.Grand.txt` in Lehner's *Dam Impoundment Database* (Zenodo record 15350094; CC BY 4.0), as for Indochina. 423 of the 463 reservoirs have a year. The map draws a reservoir from its dam's year to the last year of the span, so the Three Gorges reservoir (2003) is not drawn in the 1960s. A water body without a year is not thereby older than 1969, nor natural.

### Climate: `koppen.pmtiles`, `koppen.json`

- **Source:** Beck et al. (2023), Köppen–Geiger maps, version 2 of the dataset (figshare, doi:10.6084/m9.figshare.21789074.v2), file `1961_1990/koppen_geiger_0p00833333.tif` out of `koppen_geiger_tif.zip` (from `https://ndownloader.figshare.com/files/61012822`, the address figshare's API gives). CC BY 4.0.
- Tiles as Indochina's, to zoom 6 (about 2.4 km a pixel). The frame holds 26 classes. The legend shows the 22 that cover over 0.1 percent of the frame's land.

### Weather: `climate.json`, `climate.geojson`

- **Source:** CRU CL 2.0, the 10-minute mean monthly climate of global land areas, 1961–1990 (New et al., 2002), files `grid_10min_pre.dat.gz` and `grid_10min_tmp.dat.gz` from `https://crudata.uea.ac.uk/cru/data/hrg/tmc/`. **Licence: Open Database License.** `climate.json` and `climate.geojson` are derived databases and are released under the ODbL too.
- A grid of 92 rows and 148 columns of half a degree, from 67 E and 57 N. Each cell is the mean of the CRU cells it holds, up to nine. 10,087 cells hold land. Rainfall in whole mm a month, temperature in tenths of a degree C in `climate.json` and in degrees in `climate.geojson`. Checks: Peking's cell 2 mm in January and 154 in July; Canton's 42 and 227; Lhasa's 2 and 91; Harbin's mean temperature −18.9 °C in January.
- A cell's figure is a mean over about 50 km, so a city in a valley reads lower or higher than its own station.

### Population: `population.geojson`

- **Source:** ISIMIP3a's gridded historical population, `population_histsoc_5arcmin_annual_1901_2021.nc` (`https://files.isimip.org/ISIMIP3a/InputData/socioeconomic/pop/histsoc/`; 1.37 GB), which ISIMIP takes from HYDE 3.2.1. CC BY 4.0.
- The bands for 1960 and 1970. Each cell of 15′ is the sum of 3 × 3 of the model's 5′ cells, over its geodesic area. Classes as Indochina's (0, 1, 10, 25, 50, 100, 250, 500, 1,000 persons a km²), traced as polygons, simplified as a coverage at 0.012°. The frame holds 1,501 million people in 1960 and 1,874 million in 1970: China, India, Japan and the other countries in it.
- **A model, made later** from national totals and later maps. Not a census. The legend says so.

### Cities: `cities.yaml`

- **Source:** the United Nations' *Demographic Yearbook*, 1966 (table 6, pp. 185, 186 and 189) and 1970 (table 8, pp. 446–448 and 456), the files "1966 DYB.pdf" and "1970 DYB.pdf" from `https://unstats.un.org/unsd/demographic-social/products/dyb/`. Read by eye off the page images at 200 dpi, as the figures for Indochina were. Every figure was then checked against the files' text layer.
- **What the Yearbooks print for the mainland:** 103 cities. For each the census of June 30, 1953, and for 40 of the larger the estimate of the end of 1957, both as the State Statistical Bureau in Peking released them. Liaoyang has a figure of a census of 1940 only. The Yearbooks of 1966 and 1970 print nothing later for the mainland. The other Yearbooks of the 1960s were not read by eye. Their text layers were searched on Nov. 26, 2026 for a page that names Peking, Shanghai and Tientsin. The Yearbooks of 1963, 1965, 1967, 1968 and 1969 have one, and it prints the same estimates of the end of 1957 for the three. The search found no such page in the Yearbooks of 1960, 1961 and 1964, and the 1962 file did not download (the connection was reset). Check: those three and 1962, by eye.
- **Taiwan, Hong Kong, Macau:** twelve cities of Taiwan and the Yangmingshan Administration (estimates of 1965, 1966 and 1969, the census of 1956), Victoria in Hong Kong (the census of 1961) and Macau (the censuses of 1950 and 1960).
- **On the map:** 116 cities, each at its place in the calendar's gazetteer. The file names the gazetteer's key for every city and holds no point of its own. 34 of the cities were made places of the gazetteer for this (above, "The Yearbook's cities").
- **Not on the map:** "Malibo" (196,300 in 1953), which was not identified (the owner, Nov. 25, 2026: "I can't identify Malibo either"), and the Yangmingshan Administration, which is an area, not a city. Their figures are kept in the file under `unplaced`.
- **This file's readings.** The Yearbook names the cities in the spellings of its day and names no province. Three readings are this file's own and stand. Check: "Chuchow" as Zhuzhou. Check: "Taichow" as Taizhou in Jiangsu. Check: "Chinchow" as Jinzhou in Liaoning. The figure for "Port Arthur and Dairen" stands at Dalian.

### Tints of the units

The maps of Indochina tint the provinces by corps zone or by today's region. The map of China has no like tint, and none is to be made (the owner, Nov. 25, 2026: "Don't tint by regional bureaus or military region").

### Tried and refused, and what was not used

- **Wikidata's API** (`www.wikidata.org/w/api.php`) answered 429 after a few requests. The cities' points were read from Wikidata's query service (`query.wikidata.org`), which answered.
- **NCEI's THREDDS server** offers no subset service for the 30″ file but OPeNDAP. The whole file was downloaded.
- **ETOPO at 15″** was not used. A zoom 6 pixel is about the size of the 30″ grid's cell (about 1.1 km at 30° N against about 930 m), so the finer grid would add little at zoom 6. North of about 40° N the pixel is a little smaller than the cell from north to south, and only there would the 15″ grid add anything. The 15″ grid is what zoom 7 would need, and zoom 7 would put the file over `check`'s limit.
- **The other Yearbooks of the 1960s** were searched by their text layer only (above, "Cities"). The pages found also carry dates from 1962 to 1968, which may be Taiwan's estimates of those years. They were not read, and the file holds none of them. Check.
- No host refused this machine on Nov. 26, 2026: NCEI, HydroSHEDS, Zenodo, figshare's API, CRU, ISIMIP and the UN's statistics site all answered.
