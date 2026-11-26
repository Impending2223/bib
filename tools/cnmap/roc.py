"""The Republic of China's counties and cities of the 1960s as unions of today's townships and districts (the owner,
Nov. 25, 2026: "Give Formosa and Free China their ROC subdivisions"): Taiwan Province's sixteen counties, five
provincial cities and the Yangmingshan Administrative Bureau, and Fujian Province's two counties, Kinmen and
Lienchiang. The method is tools/cnmap/counties.py's: a later boundary file's units, each given whole to the unit of
the 1960s that held it. Here the record is short, and the table below is the whole of it. tools/cnmap/base.py reads
this module and dissolves the geometry with the rest of the map's:

    python3 -I tools/cnmap/base.py DIR

DIR/twn/twTown1982.geo.json: the townships, county-administered cities and districts of Taiwan, 377 features (368
units, and nine harbour waters set apart, "(海)", each put back in its district), from g0v's twgeojson,
https://raw.githubusercontent.com/g0v/twgeojson/master/json/twTown1982.geo.json (sha256 e8f6e19f…0fcbb2), read Nov.
26, 2026. The repository's README: the files are made from the boundary files the Institute of Transportation,
Ministry of Transportation and Communications, gave out, and its author waives all rights in the package (CC0 1.0).
The file's name says 1982; its units are those of after Dec. 25, 2010 (新北市, and Taichung, Tainan and Kaohsiung
each one city) and before Dec. 25, 2014 (桃園縣). The government's own file (鄉鎮市區界線, data.gov.tw dataset 7441,
the Open Government Data License) is served from www.tgos.tw, which refused this machine (HTTP 403) on Nov. 26, 2026.

What changed between the 1960s and the file, and how each is put back (sources/china/README.md says the same):
 - Taipei. A provincial city until July 1, 1967, then a special municipality. On July 1, 1968 it took Neihu, Nangang,
   Muzha and Jingmei from Taipei county and Shilin and Beitou from the Yangmingshan Administrative Bureau. Its sixteen
   districts were redrawn as twelve on Mar. 12, 1990. So the city "as it stood" is today's Zhongzheng, Datong,
   Zhongshan, Songshan, Da'an, Wanhua and Xinyi districts (the ten districts of before 1968, in the lines of 1990);
   the Bureau is Shilin and Beitou; Neihu, Nangang and Wenshan (Muzha and Jingmei) go back to Taipei county.
 - Taipei county is today's New Taipei City (from Dec. 25, 2010) with those three districts.
 - Hsinchu and Chiayi were county-administered cities until July 1, 1982: each goes back into its county.
 - Taichung, Tainan and Kaohsiung: each city and its county were joined on Dec. 25, 2010. The city is the districts it
   had before; the county is the rest. Kaohsiung took Xiaogang from Kaohsiung county on July 1, 1979: it goes back to
   the county. Tainan's West and Central districts were joined in 2004; both were the city's.
 - Every other county, Keelung, Penghu, Kinmen and Lienchiang: the file's unit of the name, whole.
"""
import collections
import json
import re

FILE = "twTown1982.geo.json"
SOURCE = ("g0v twgeojson, json/twTown1982.geo.json (the Institute of Transportation's township boundaries, the "
          "units of 2011–14; CC0 1.0)")
FILE_YEAR = 2011

# the two provinces the Republic held: the map's units of 1966 beside the PRC's (tools/cnmap/base.py META, FULL)
PROVINCES = {
    "taiwan": {"name": "Taiwan", "zh": "臺灣省", "kind": "province",
               "full": "Taiwan Province, Republic of China (the island and the Pescadores)"},
    "fujian-roc": {"name": "Fujian (Republic of China)", "zh": "福建省", "kind": "province",
                   "full": "Fujian Province, Republic of China: Kinmen (Quemoy) and Lienchiang (Matsu) counties"},
}

CITY = "provincial city"
# id -> (name, zh, kind, province, how it is made of the file's units)
UNITS = {
    "taipei-city": ("Taipei", "臺北市", CITY, "taiwan",
                    "seven of today's districts: the city of before July 1968, in the district lines of 1990"),
    "yangmingshan": ("Yangmingshan", "陽明山管理局", "administrative bureau", "taiwan",
                     "today's Shilin and Beitou districts of Taipei, the Bureau's two townships until July 1968"),
    "taipei": ("Taipei", "臺北縣", "county", "taiwan",
               "today's New Taipei City, with Taipei's Neihu, Nangang and Wenshan districts, the county's until July 1968"),
    "keelung": ("Keelung", "基隆市", CITY, "taiwan", "today's city"),
    "ilan": ("Ilan", "宜蘭縣", "county", "taiwan", "today's county"),
    "taoyuan": ("Taoyuan", "桃園縣", "county", "taiwan", "today's county (a city since 2014)"),
    "hsinchu": ("Hsinchu", "新竹縣", "county", "taiwan",
                "today's county with Hsinchu city, a city of the county until July 1982"),
    "miaoli": ("Miaoli", "苗栗縣", "county", "taiwan", "today's county"),
    "taichung-city": ("Taichung", "臺中市", CITY, "taiwan",
                      "eight of today's districts: the city of before the joining of Dec. 2010"),
    "taichung": ("Taichung", "臺中縣", "county", "taiwan",
                 "today's Taichung City without the eight districts of the old city"),
    "changhua": ("Changhua", "彰化縣", "county", "taiwan", "today's county"),
    "nantou": ("Nantou", "南投縣", "county", "taiwan", "today's county"),
    "yunlin": ("Yunlin", "雲林縣", "county", "taiwan", "today's county"),
    "chiayi": ("Chiayi", "嘉義縣", "county", "taiwan",
               "today's county with Chiayi city, a city of the county until July 1982"),
    "tainan-city": ("Tainan", "臺南市", CITY, "taiwan",
                    "six of today's districts: the city of before the joining of Dec. 2010"),
    "tainan": ("Tainan", "臺南縣", "county", "taiwan", "today's Tainan City without the six districts of the old city"),
    "kaohsiung-city": ("Kaohsiung", "高雄市", CITY, "taiwan",
                       "ten of today's districts: the city of before July 1979, without Xiaogang"),
    "kaohsiung": ("Kaohsiung", "高雄縣", "county", "taiwan",
                  "today's Kaohsiung City without the ten districts of the old city; Xiaogang, the city's from July "
                  "1979, with the county"),
    "pingtung": ("Pingtung", "屏東縣", "county", "taiwan", "today's county"),
    "taitung": ("Taitung", "臺東縣", "county", "taiwan", "today's county"),
    "hualien": ("Hualien", "花蓮縣", "county", "taiwan", "today's county"),
    "penghu": ("Penghu (Pescadores)", "澎湖縣", "county", "taiwan", "today's county"),
    "kinmen": ("Kinmen (Quemoy)", "金門縣", "county", "fujian-roc", "today's county"),
    "lienchiang": ("Lienchiang (Matsu)", "連江縣", "county", "fujian-roc", "today's county"),
}

# the file's county (COUNTYNAME) -> the unit of the 1960s it goes to whole
WHOLE = {"基隆市": "keelung", "宜蘭縣": "ilan", "桃園縣": "taoyuan", "新竹縣": "hsinchu", "新竹市": "hsinchu",
         "苗栗縣": "miaoli", "彰化縣": "changhua", "南投縣": "nantou", "雲林縣": "yunlin", "嘉義縣": "chiayi",
         "嘉義市": "chiayi", "屏東縣": "pingtung", "台東縣": "taitung", "花蓮縣": "hualien", "澎湖縣": "penghu",
         "新北市": "taipei", "金門縣": "kinmen", "連江縣": "lienchiang"}
# the file's county -> [(its districts (TOWNNAME), the unit they go to)], the last the rest's
SPLIT = {
    "台北市": [({"中正區", "大同區", "中山區", "松山區", "大安區", "萬華區", "信義區"}, "taipei-city"),
            ({"士林區", "北投區"}, "yangmingshan"),
            ({"內湖區", "南港區", "文山區"}, "taipei")],
    "台中市": [({"中區", "東區", "南區", "西區", "北區", "西屯區", "南屯區", "北屯區"}, "taichung-city"), (None, "taichung")],
    "台南市": [({"東區", "南區", "北區", "中西區", "安南區", "安平區"}, "tainan-city"), (None, "tainan")],
    "高雄市": [({"鹽埕區", "鼓山區", "左營區", "楠梓區", "三民區", "新興區", "前金區", "苓雅區", "前鎮區", "旗津區"},
             "kaohsiung-city"), (None, "kaohsiung")],
}


def town(name):
    """A district's name without the file's mark for its harbour waters: "前鎮區(海)", "梧棲鎮(海區"."""
    return re.sub(r"\(海.*$", "", name)


def unit_of(county, name):
    """The unit of the 1960s a unit of the file goes to: its id, or None for a name the table does not know."""
    if county in WHOLE:
        return WHOLE[county]
    for names, to in SPLIT.get(county, []):
        if names is None or town(name) in names:
            return to
    return None


def read(path):
    """({unit id: [the file's features' geometries as GeoJSON]}, {unit id: {the file's county: [its districts]}}); an
    error on a unit of the file the table does not place, or a unit of the table the file leaves empty."""
    fs = json.load(open(path, encoding="utf-8"))["features"]
    geoms, made = collections.defaultdict(list), collections.defaultdict(lambda: collections.defaultdict(set))
    for f in fs:
        p = f["properties"]
        to = unit_of(p["COUNTYNAME"], p["TOWNNAME"])
        if to is None:
            raise SystemExit(f"roc.py: no unit of the 1960s for {p['COUNTYNAME']} {p['TOWNNAME']}")
        geoms[to].append(f["geometry"])
        made[to][p["COUNTYNAME"]].add(town(p["TOWNNAME"]))
    missing = sorted(set(UNITS) - set(geoms))
    if missing:
        raise SystemExit(f"roc.py: the file gives nothing for {missing}")
    for county, rules in SPLIT.items():                      # every district the table names is in the file
        have = {town(f["properties"]["TOWNNAME"]) for f in fs if f["properties"]["COUNTYNAME"] == county}
        for names, _ in rules:
            if names and names - have:
                raise SystemExit(f"roc.py: {county} has no {sorted(names - have)}")
    return dict(geoms), {k: {c: sorted(v) for c, v in sorted(d.items())} for k, d in made.items()}


def made_of(uid, made):
    """A unit's row for counties.json's `made_of`, in the shape the PRC's rows have: each of the file's counties it
    takes, whole or by the districts named."""
    out = []
    for county, towns in made.items():
        whole = county in WHOLE
        out.append({"file": county if whole else f"{county}: {'、'.join(towns)}", "zh": county, "year": FILE_YEAR,
                    "match": "by hand (tools/cnmap/roc.py)", "basis": "whole" if whole else "by district", "via": []})
    return out
