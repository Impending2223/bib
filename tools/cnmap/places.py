"""The places of the map of China: each place of the calendar's gazetteer (sources/places.yaml) that lies in China, Hong
Kong, Macau or Taiwan, with coordinates from Wikidata (the item's P625; its English Wikipedia article linked where it
has one), never guessed, and its 1966 province and 1964 county by point in polygon. A one-time script, run again when
the gazetteer has new places in China (`./bib check` warns of each):

    python3 tools/cnmap/places.py CACHE_DIR [--refresh]

CACHE_DIR holds what was read from Wikidata's query service (https://query.wikidata.org/sparql; CC0), read Nov. 26,
2026: cands.json (every item with coordinates whose English or Chinese label is one of a place's names) and zh.json
(those items' labels); delete them, or pass --refresh, to read again. Needs shapely and opencc-python-reimplemented
(the entries' traditional characters to simplified, for the labels). It reads lists/ through tools/bib/store.

The steps (sources/china/README.md states the rules and the counts):
 1. Each place's names: the gazetteer's own (English: "Anguo", "Bo county"), and the Chinese name the calendar's
    entries print after it ("Anguo 安国"), with the province the entries' text names beside it, where they do.
 2. Wikidata's items with coordinates in China that carry one of the names as a label (with 市, 县, 区, 镇 and the like).
 3. One item chosen, by rule, and the rule kept in the row (`why`): the province in the entries' text; or Wikipedia's
    article of that bare name; or the one place of the name. Never two places 60 km apart without one of those.
 4. HAND: the places the rules do not settle, each settled from the entries' own words, or left unplaced with the
    reason. AREA: a province named as a place takes no point (tools/bib/cnmap.py, STYLE 2).
 5. The province of 1966 (admin.geojson) and the county of 1964 (counties.geojson) the point falls in. A point of a
    place in the PRC that falls just outside it (an island, a border peak) takes the nearest unit within 0.3 degree.
    A point that falls outside the county of its own name but within 5 km of it takes that county and its province
    (`near` in the row): the lines are approximate, and a county seat on a border river falls across it.
 6. WIKI: a point from Wikipedia's article where Wikidata's for the same item is wrong (one place).

Writes sources/china/places.json: {"read": date, "places": [{key, zh, lat, lon, src, q, wiki, why, unit, county, c,
capital} | {key, area: true, unit} | {key, unplaced: reason}]}, in key order.
"""
import collections
import json
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
OUT = os.path.join(ROOT, "sources", "china")
UA = "HistoricalMapDataBot/1.0 (one-time gazetteer lookup; low rate) python-urllib/3.13"
READ = "2026-11-26"

PROV = {"Anhui": "anhui", "Fujian": "fujian", "Gansu": "gansu", "Guangdong": "guangdong", "Guangxi": "guangxi",
        "Guizhou": "guizhou", "Hebei": "hebei", "Heilongjiang": "heilongjiang", "Henan": "henan", "Hubei": "hubei",
        "Hunan": "hunan", "Inner Mongolia": "inner-mongolia", "Jiangsu": "jiangsu", "Jiangxi": "jiangxi", "Jilin": "jilin",
        "Liaoning": "liaoning", "Ningxia": "ningxia", "Qinghai": "qinghai", "Shaanxi": "shaanxi", "Shandong": "shandong",
        "Shanxi": "shanxi", "Sichuan": "sichuan", "Tibet": "tibet", "Xinjiang": "xinjiang", "Yunnan": "yunnan",
        "Zhejiang": "zhejiang", "Hainan": "guangdong"}
# a province named as a place: gazetteer key -> 1966 unit
AREA = {"anhui": "anhui", "fujian": "fujian", "gansu": "gansu", "guangdong": "guangdong", "guangxi": "guangxi",
        "guizhou": "guizhou", "hebei": "hebei", "heilongjiang": "heilongjiang", "henan": "henan", "hubei": "hubei",
        "hunan": "hunan", "inner-mongolia": "inner-mongolia", "jiangsu": "jiangsu", "jiangxi": "jiangxi",
        "jilin-province": "jilin", "liaoning": "liaoning", "ningxia": "ningxia", "qinghai": "qinghai",
        "shaanxi": "shaanxi", "shandong": "shandong", "shanxi": "shanxi", "sichuan": "sichuan", "xinjiang": "xinjiang",
        "yunnan": "yunnan", "zhejiang": "zhejiang", "tibet": "tibet"}
# the capitals of 1964 (行政区划网, 中华人民共和国行政区划（1964年）, 一九六四年全国省级行政区一览), with Hong Kong and Taipei: rank 1
CAPITAL = {"peking", "shanghai", "tianjin", "taiyuan", "hohhot", "shenyang", "changchun", "harbin", "xian", "lanzhou",
           "yinchuan", "xining", "urumqi", "jinan", "nanjing", "hangzhou", "hefei", "nanchang", "fuzhou", "zhengzhou",
           "wuhan", "changsha", "canton", "nanning", "chengdu", "guiyang", "kunming", "lhasa", "hong-kong", "taipei"}
# settled by hand from the entries' own words: key -> (Wikidata item, the ground), or (None, why it has no point)
HAND = {
    "peking": ("Q956", "the capital"),
    "anning": ("Q567193", "the entries: the hot springs 40 km from Kunming"),
    "changan-county": ("Q1061858", "the entries: Chang'an county, by Xi'an (Yang Shangkun's stay in Shaanxi)"),
    "doumen": ("Q11080535", "the entries: Doumen of Chang'an county, where the Niujiao brigade goes to a meeting"),
    "datong": ("Q72877", "the entries: the Laobaitong mine; the city in Shanxi"),
    "fenglin": ("Q68461882", "the entries: the Fenglin forestry bureau, in the Yichun forests"),
    "huashan": ("Q112568", "the entries: the mountain east of Xi'an"),
    "jigongshan": ("Q834052", "the entries: the mountain by Xinyang"),
    "jilin-city": ("Q92277", "the entries: the city of Jilin"),
    "mudanjiang": ("Q217646", "the entries: the city, by Jingpo Lake"),
    "pingxiang": ("Q1027734", "the entries: Zhou Enlai meets the Vietnamese leaders there; the town on the border, in Guangxi"),
    "she-county": ("Q1196719", "the entries: a day's inquiry from Handan; She county of Hebei"),
    "stone-forest": ("Q38839215", "the entries: by Lunan, Yunnan"),
    "tieling": ("Q1280804", "the entries: Tieling county"),
    "lushan": ("Q622616", "the entries: the mountain"),
    "hainan": ("Q42200", "the island"),
    "wushi": ("Q10297068", "the entries: Wushi of Xiangtan county, Peng Dehuai's village"),
    "dukou": ("Q425415", "the entries: the Panzhihua iron mine; Dukou, renamed Panzhihua in 1987"),
    "bo-county": ("Q360769", "the entries: Bo county, Anhui; Bozhou since 1986"),
    "cixi": ("Q706161", "the entries: Cixi county, Zhejiang"),
    "danxian": ("Q1015132", "the entries: Dan county, Hainan; Danzhou since 1993"),
    "dayong-county": ("Q675319", "the entries: Dayong county, Hunan; Yongding district of Zhangjiajie since 1994"),
    "dongjing": ("Q10869415", "the entries: the station by the Bohai kingdom's site; Dongjingcheng, Ning'an"),
    "guan-county": ("Q1023900", "the entries: Guan county, Sichuan; Dujiangyan since 1988"),
    "huanjiang": ("Q1201707", "the entries: Huanjiang county, Guangxi"),
    "huaqingchi": ("Q4133842", "the entries: at the foot of Lishan"),
    "huaxian": ("Q498004", "the entries: Hua county, Guangdong; Huadu since 1993"),
    "kaixian": ("Q1371311", "the entries: Kai county, Sichuan; Kaizhou district since 2016"),
    "lushun": ("Q623329", "the entries: the naval base"),
    "maanchang": ("Q13909197", "the entries: Ma'anchang of Yilong county, Zhu De's birthplace; Ma'an town"),
    "tanzichong": ("Q10897415", "the entries: Liu Shaoqi's home village; the house there"),
    "wanxian": ("Q713825", "the entries: Wanxian, Sichuan; Wanzhou district since 1998"),
    "xiaoxinganling": ("Q404600", "the range"),
    "daxinganling": ("Q293713", "the range"),
    "xinjin": ("Q1362420", "the entries: Xinjin county, Liaoning; Pulandian since 1991"),
    "yuecheng-reservoir": ("Q15937304", "the reservoir"),
    "nanhai": ("Q1023893", "the entries: Nanhai county; the one county of the name"),
    "chishui": ("Q65367", "the entries: the Chishui county committee; the one county of the name, in Guizhou"),
    "emei": ("Q1335318", "the entries: Emei county, at the mountain's foot; Emeishan city"),
    "fengxiang": ("Q1201619", "the entries: from Baoji by Guozhen; Fengxiang of Shaanxi"),
    "naxi": ("Q1209106", "the entries: the battlefield of the National Protection War; Naxi by Luzhou"),
    "huzhu": ("Q1356943", "the entries: Huzhu county, Qinghai"),
    "minhe": ("Q1356925", "the entries: Minhe county, Qinghai"),
    "shizhu": ("Q1378010", "the entries: Shizhu county, Sichuan"),
    "yinjiang": ("Q1153247", "the entries: Yinjiang county, Guizhou"),
    "shehong-county": ("Q970433", "the entries: Shehong county, Sichuan"),
    "wu-county": ("Q3092999", "the entries: Wu county, Jiangsu"),
    "qianling": ("Q950653", "the entries: the tomb, by Qian county; Wikipedia's Qianling Mausoleum"),
    "yulin-hainan": ("Q114702838", "the entries: the naval port of Yulin, Hainan; Wikipedia's Yulin Naval Base"),
    "qijiang": ("Q714216", "the entries: Qijiang county, Sichuan; Qijiang district of Chongqing (the rule took the river of the name)"),
    "xinan-hebei": ("Q10946869", "the entries: Xin'an by Baiyangdian, the county committee's seat; Anxin town, the seat of Anxin county"),
    "xincheng-hebei": ("Q252959", "the entries: Xincheng county of Baoding prefecture, Hebei; Gaobeidian since 1993"),
    "longnan": (None, "Wikidata's and Wikipedia's point for Longnan, Jiangxi, lies 100 km north of the county, in Nankang; not taken"),
    "niujiao": (None, "a village of Chang'an county, Shaanxi; neither source has it"),
    "tianhua": (None, "a brigade of Changsha county, Hunan; neither source has it"),
    "nanxucheng": (None, "a village the entries do not place in a county; neither source has it"),
    "taoyuan-hebei": (None, "a brigade of Funing county, Hebei; neither source has it"),
    "lingbei": (None, "a commune; the entry does not say which of several"),
    "mingshui": (None, "the Mingshui station of the Jiabiangou farm, in Gaotai, Gansu; neither source has it"),
    "wangjiawan": (None, "a production team of Ningxiang county, Hunan; neither source has it"),
}
# A point taken from Wikipedia's article, where Wikidata's for the same item is wrong: key -> the row's fields. Read
# from en.wikipedia.org's API (prop=coordinates), Nov. 26, 2026.
WIKI = {
    "binyang-county": {"lat": 23.215, "lon": 108.854, "q": "Q864098", "zh": "宾阳县",
                       "art": "https://en.wikipedia.org/wiki/Binyang_County",
                       "why": "the entries: Binyang county, Guangxi; Wikipedia's coordinates for the article (Wikidata's "
                              "point for the item lies 70 km off, by Nanning)"},
}
OWN_KM = 5        # a point this near the county of its own name is in it: the lines are approximate
ZS = ["", "市", "县", "区", "镇", "村", "乡", "省", "岛", "山", "湖", "水库", "自治县", "地区", "特区", "街道"]
ES = ["", " County", " District", " Town", " Village", " Township", " Subdistrict", " Province", " Prefecture", " Island"]
SUFFIX = r"-(hebei|guangdong|yunnan|gansu|guizhou|hunan|sichuan|anhui|jiangxi|shandong|hainan)$"


def en_name(name):
    return re.sub(r" \(.*\)$|, .*$", "", re.sub(r"^the ", "", name))


def evidence(t2s):
    """{key: {name, n, zh: the Chinese names the entries print after the place's, near: provinces named beside it}}."""
    from bib import places as gaz, store
    series = store.Series()
    rows = store.load_yaml(os.path.join(ROOT, "sources", "places.yaml"))
    cn = {r["key"]: r for r in rows
          if {"prc", "roc"} & set(map(str, store.as_list(r.get("in")))) or r["key"] in ("hong-kong", "macau")}
    ev = {k: {"name": r["name"], "n": 0, "zh": collections.Counter(), "near": collections.Counter(),
              "c": "roc" if "roc" in store.as_list(r.get("in")) else k if k in ("hong-kong", "macau") else "prc"}
          for k, r in cn.items()}
    kinds = r"(?: county| County| city| district| commune| brigade| village| prefecture| Island| Lake| reservoir| Reservoir)?"
    for sec, e in series.lists["cal"].entries():
        if "when" not in e or "place" not in e:
            continue
        ks = [gaz.get(k)["key"] for k in gaz.keys(e) if gaz.get(k)]
        text = " ".join(store.as_list(e.get("c")))
        for k in ks:
            if k not in ev:
                continue
            d = ev[k]
            d["n"] += 1
            name = re.sub(r"^the | county$| County$| \(.*\)$|,.*$", "", cn[k]["name"])
            for p in PROV:
                if re.search(re.escape(name) + r"[^.;]{0,60}\b" + p + r"\b|\b" + p + r"\b[^.;]{0,60}" + re.escape(name), text):
                    d["near"][p] += 1
            for m in re.finditer(re.escape(name) + kinds + r" ([一-鿿]{1,10})", text + " " + " ".join(store.as_list(e.get("n")))):
                d["zh"][t2s(m.group(1))] += 1
    return {k: dict(d, zh=[z for z, _ in d["zh"].most_common(3)], near=dict(d["near"])) for k, d in ev.items()}


def sparql(q):
    data = urllib.parse.urlencode({"query": q, "format": "json"}).encode()
    for i in range(5):
        try:
            req = urllib.request.Request("https://query.wikidata.org/sparql", data=data,
                                         headers={"User-Agent": UA, "Accept": "application/sparql-results+json"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)["results"]["bindings"]
        except Exception as e:                       # 429 and time-outs: back off
            print("retry", e, flush=True)
            time.sleep(15 * (i + 1))
    raise SystemExit("Wikidata did not answer")


def labels(d):
    out = []
    for z in d["zh"]:
        base = re.sub(r"(市|县|区|镇|村|省)$", "", z) if len(z) > 2 else z
        for b in {z, base}:
            out += [(b + s, "zh") for s in ZS]
    name = en_name(d["name"])
    base = re.sub(r" (county|County|city|prefecture|reservoir|Reservoir)$", "", name)
    for b in {name, base}:
        out += [(b + s, "en") for s in ES]
    return out


def candidates(ev, cache, refresh):
    cp, zp = os.path.join(cache, "cands.json"), os.path.join(cache, "zh.json")
    old = json.load(open(cp, encoding="utf-8")) if os.path.exists(cp) and not refresh else {"rows": [], "want": {}}
    want = {}
    for k, d in ev.items():
        for lab, tag in labels(d):
            want.setdefault(f"{lab}@{tag}", set()).add(k)
    for q, _ in HAND.values():
        if q:
            want.setdefault(f"wd:{q}", set())
    new = sorted(k for k in want if k not in old["want"])
    rows = old["rows"]
    for i in range(0, len(new), 400):
        part = new[i:i + 400]
        labs = " ".join(json.dumps(x.rsplit("@", 1)[0], ensure_ascii=False) + "@" + x.rsplit("@", 1)[1] for x in part if not x.startswith("wd:"))
        ids = " ".join(x for x in part if x.startswith("wd:"))
        tail = ("?item wdt:P625 ?coord . OPTIONAL { ?item wdt:P17 ?country } "
                "OPTIONAL { ?art schema:about ?item ; schema:isPartOf <https://en.wikipedia.org/> } }")
        got = []
        if labs:
            got += sparql("SELECT ?item ?lab ?coord ?country ?art WHERE { VALUES ?lab { %s } ?item rdfs:label ?lab . %s" % (labs, tail))
        if ids:
            got += sparql("SELECT ?item ?coord ?country ?art WHERE { VALUES ?item { %s } %s" % (ids, tail))
        for b in got:
            rows.append({"q": b["item"]["value"].rsplit("/", 1)[1], "lab": b.get("lab", {}).get("value", ""),
                         "tag": b.get("lab", {}).get("xml:lang", ""), "coord": b["coord"]["value"],
                         "country": b.get("country", {}).get("value", "").rsplit("/", 1)[-1],
                         "art": urllib.parse.unquote(b.get("art", {}).get("value", ""))})
        print("labels", i, len(got), flush=True)
        time.sleep(2)
    if new:
        json.dump({"rows": rows, "want": {k: sorted(set(v) | set(old["want"].get(k, []))) for k, v in {**{k: [] for k in old["want"]}, **want}.items()}},
                  open(cp, "w", encoding="utf-8"), ensure_ascii=False)
    zh = json.load(open(zp, encoding="utf-8")) if os.path.exists(zp) and not refresh else {}
    qs = sorted({r["q"] for r in rows} - set(zh))
    for i in range(0, len(qs), 250):
        q = ('SELECT ?item ?l WHERE { VALUES ?item { %s } ?item rdfs:label ?l . FILTER(LANG(?l) IN ("zh","zh-cn","zh-hans","zh-hant","en")) }'
             % " ".join("wd:" + x for x in qs[i:i + 250]))
        for x in qs[i:i + 250]:
            zh.setdefault(x, {})
        for b in sparql(q):
            zh[b["item"]["value"].rsplit("/", 1)[1]].setdefault(b["l"]["xml:lang"], b["l"]["value"])
        print("items", i, flush=True)
        time.sleep(2)
    if qs:
        json.dump(zh, open(zp, "w", encoding="utf-8"), ensure_ascii=False)
    by = collections.defaultdict(dict)
    hand = {q for q, _ in HAND.values() if q}
    wanted = json.load(open(cp, encoding="utf-8"))["want"] if os.path.exists(cp) else {}
    items = {}
    for r in rows:
        m = re.match(r"Point\(([-\d.]+) ([-\d.]+)\)", r["coord"])
        if not m or not (66 <= float(m.group(1)) <= 142 and 10 <= float(m.group(2)) <= 58):
            continue
        if r["country"] and r["country"] not in ("Q148", "Q865", "Q8646", "Q14773") and r["q"] not in hand:
            continue
        c = items.setdefault(r["q"], {"q": r["q"], "lon": float(m.group(1)), "lat": float(m.group(2)), "art": r["art"]})
        c["art"] = c["art"] or r["art"]
        for k in wanted.get(f'{r["lab"]}@{r["tag"]}', []):
            by[k][r["q"]] = c
    return by, items, zh


def km(a, b):
    return 111.2 * math.hypot((a["lon"] - b["lon"]) * math.cos(math.radians(a["lat"])), a["lat"] - b["lat"])


def main():
    import shapely
    from opencc import OpenCC
    from shapely.geometry import Point, shape
    cache = sys.argv[1]
    os.makedirs(cache, exist_ok=True)
    t2s = OpenCC("t2s").convert
    ev = evidence(t2s)
    by, items, zh = candidates(ev, cache, "--refresh" in sys.argv)
    adm = json.load(open(os.path.join(OUT, "admin.geojson"), encoding="utf-8"))
    units = [(f["properties"]["id"], f["properties"]["c"], shape(f["geometry"])) for f in adm["features"] if f["properties"]["k"] == "unit"]
    lands = [(f["properties"]["id"], shape(f["geometry"])) for f in adm["features"] if f["properties"]["k"] == "land"]
    cp = os.path.join(OUT, "counties.geojson")
    cty = [(f["properties"]["id"], shape(f["geometry"])) for f in json.load(open(cp, encoding="utf-8"))["features"]
           if f["properties"]["k"] == "county"] if os.path.exists(cp) else []
    ctree = shapely.STRtree([g for _, g in cty]) if cty else None
    cjp = os.path.join(OUT, "counties.json")
    cj = {c["id"]: c for c in json.load(open(cjp, encoding="utf-8"))["counties"]} if os.path.exists(cjp) else {}
    stem1 = lambda z: re.sub(r"(市|县|区)$", "", z) if len(z) > 2 else z

    def own_county(zh, lon, lat):
        """The county of the place's own name, where the point lies within OWN_KM of it: (county, its unit) or None."""
        p, b = Point(lon, lat), stem1(zh or "")
        near = [(g.distance(p) * 111.2, i) for i, g in cty if i in cj and cj[i].get("zh") and stem1(cj[i]["zh"]) == b]
        near = [(d, i) for d, i in near if d <= OWN_KM]
        return (min(near)[1], cj[min(near)[1]]["unit"]) if b and near else None

    def unit_of(lon, lat, prc):
        p = Point(lon, lat)
        for i, c, g in units:
            if g.contains(p):
                return i, None
        best = min(units, key=lambda u: u[2].distance(p))
        if prc and best[2].distance(p) < 0.3:
            return best[0], None
        for i, g in lands:
            if g.contains(p):
                return None, i
        return None, None

    def county_of(lon, lat):
        if not cty:
            return None
        for j in ctree.query(Point(lon, lat), predicate="within"):
            return cty[int(j)][0]
        return None

    for c in items.values():
        c["zh"] = [t2s(v) for t, v in zh.get(c["q"], {}).items() if t.startswith("zh")]
        c["en"] = zh.get(c["q"], {}).get("en", "")
        c["u"] = unit_of(c["lon"], c["lat"], False)[0]
    rows, counts = [], collections.Counter()
    for k, d in sorted(ev.items()):
        if k in AREA:
            rows.append({"key": k, "area": True, "unit": AREA[k]})
            counts["a province named as a place"] += 1
            continue
        zhs, en = d["zh"], en_name(d["name"])
        why = best = None
        src = "wikidata"
        if k in WIKI:
            w = WIKI[k]
            best, why, src = {"lon": w["lon"], "lat": w["lat"], "q": w["q"], "art": w["art"], "zh": [w["zh"]]}, w["why"], "wikipedia"
        elif k in HAND:
            q, why = HAND[k]
            if q is None:
                rows.append({"key": k, "unplaced": why})
                counts["unplaced"] += 1
                continue
            best = items.get(q)
            if best is None:
                rows.append({"key": k, "unplaced": f"Wikidata's {q} has no coordinates"})
                counts["unplaced"] += 1
                continue
        else:
            stem = [re.sub(r"(市|县|区|省)$", "", z) if len(z) > 2 else z for z in zhs]

            def tier(c):      # 0-5: the name itself, as a city, a county, a district; 9: a town, village, street
                best = 9
                for l in c["zh"]:
                    if l in zhs:
                        best = 0
                    for b in stem:
                        for n, x in enumerate(("", "市", "县", "自治县", "区", "省")):
                            if l == b + x:
                                best = min(best, n)
                if not zhs:           # no characters in the entries: the English label must say city or county
                    base = re.sub(r" (county|County)$", "", en)
                    if c["en"] in (base + " County", base + " City") or c["art"].rsplit("/", 1)[-1].replace("_", " ") == base:
                        best = min(best, 1)
                return best
            pool = list(by.get(k, {}).values())
            if zhs:               # the entries give the characters: the item must carry them, alone or with a suffix
                pool = [c for c in pool if any(l == b + s for l in c["zh"] for b in set(zhs) | set(stem) for s in ZS)]
            hint = None
            suf = re.search(SUFFIX, k)
            if suf:
                hint = "guangdong" if suf.group(1) == "hainan" else suf.group(1)
            elif d["near"]:
                hint = PROV[max(d["near"], key=d["near"].get)]
            if hint and any(c["u"] == hint for c in pool):
                pool = [c for c in pool if c["u"] == hint]
            elif suf:
                pool = []         # the key names the province: no candidate there, no point
            elif hint:
                hint = None       # the text's province holds no candidate (a border, a transfer): the other rules
            if not pool:
                rows.append({"key": k, "unplaced": "neither source has a place of the name" + (" there" if suf or d["near"] else "")})
                counts["unplaced"] += 1
                continue
            for c in pool:
                c["tier"] = tier(c)
            small = [c for c in pool if c["tier"] == 9]
            pool = [c for c in pool if c["tier"] < 9] or pool
            title = lambda c: c["art"].rsplit("/", 1)[-1].replace("_", " ")
            bare = (en, re.sub(r" (county|County)$", "", en))
            best = max(pool, key=lambda c: (title(c) in bare and c["tier"] <= 1, -c["tier"], bool(c["art"]), -int(c["q"][1:])))
            primary = title(best) in bare
            far = [c for c in pool if km(c, best) > 60]
            others = sum(1 for c in small if km(c, best) > 60)
            if hint:
                why = "the province in the entries' text"
            elif primary and best["tier"] <= 1:
                why = "Wikipedia's article of that name"
            elif not far and not others and not (best["tier"] == 9 and re.search(r"county|County", d["name"])):
                why = "the one place of the name"
            elif not far and best["tier"] <= 3:
                why = "the one city or county of the name"
            else:
                rows.append({"key": k, "unplaced": "several places of the name, and the entries do not say which"})
                counts["unplaced"] += 1
                continue
        u, land = unit_of(best["lon"], best["lat"], d["c"] == "prc")
        row = {"key": k, "zh": (best["zh"] or [""])[0], "lat": round(best["lat"], 4), "lon": round(best["lon"], 4),
               "src": src, "q": best["q"], "wiki": best["art"] or f"https://www.wikidata.org/wiki/{best['q']}",
               "why": why, "c": d["c"] if u is None or d["c"] != "prc" else next(c for i, c, _ in units if i == u)}
        if u:
            row["unit"] = u
        elif land:
            row["country"] = {"roc": "Taiwan", "dprk": "North Korea", "ussr": "Soviet Union", "vietnam": "Vietnam"}.get(land, land)
        co = county_of(best["lon"], best["lat"])
        own = own_county(row["zh"], best["lon"], best["lat"]) if d["c"] == "prc" else None
        if own and own[0] != co and not (co and stem1(cj.get(co, {}).get("zh") or "") == stem1(row["zh"])):
            co, row["unit"] = own                # just outside the county of its own name: that county, and its unit
            row["near"] = True
        if co:
            row["county"] = co
        if k in CAPITAL:
            row["capital"] = True
        if "-v" in sys.argv and k not in HAND and (best.get("tier") == 9 or not zhs):
            print("  check:", k, best["q"], row["zh"], best.get("en", ""), u, "|", why)
        rows.append(row)
        counts[why if k not in HAND and k not in WIKI else "by hand, from the entries' words"] += 1
    json.dump({"read": READ, "source": "Wikidata (CC0), items' coordinates (P625) and English Wikipedia sitelinks",
               "places": rows}, open(os.path.join(OUT, "places.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(rows), "places:", dict(counts))
    for r in rows:
        if r.get("unplaced"):
            print("  unplaced:", r["key"], "-", r["unplaced"], f'({ev[r["key"]]["n"]} entries)')


if __name__ == "__main__":
    main()
