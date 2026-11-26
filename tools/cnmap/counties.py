"""The counties of 1964 as unions of a later boundary file's units: the record and the crosswalk. A one-time script:

    python3 -I tools/cnmap/counties.py DIR [--fetch]

DIR is a download directory outside the repository. It holds, or with --fetch is given:
 - DIR/gb/adm2.geojson: geoBoundaries gbOpen CHN ADM2 (boundary id CHN-ADM2-17275852; "County Level", 2,391 units;
   source: National Administration of Surveying, Mapping and Geoinformation of China, by way of Revolutionary GIS;
   Open Data Commons Public Domain Dedication and License 1.0), from
   https://www.geoboundaries.org/api/current/gbOpen/CHN/ADM2/ (its gjDownloadURL), read Nov. 26, 2026;
 - DIR/cgaz/geoBoundariesCGAZ_ADM1.gpkg (tools/cnmap/base.py's download), to tell which province a unit lies in;
 - DIR/xzqh/<list>-<year>.html: 行政区划网 (xzqh.org), the pages "<province> <year> 年行政区划", 1964-1996, a page a
   province a year (http://www.xzqh.org/html/list/<list>.html and the year pages it links): every county-level unit
   of the province at the year's end, by prefecture, and the year's changes. Read Nov. 26, 2026, at a page a second.
Needs shapely >= 2.1, pyogrio, pypinyin.

The boundary file names its units in pinyin and gives no year. Its units are those of about 1993: each is matched to
a unit of the record's lists by its name, in the province it lies in, and the year that matches most is taken as the
file's (the script prints the count for each year).

The steps (sources/china/README.md states each kind of case and the counts):
 1. Each of the file's units is given its province (the CGAZ province its inner point lies in) and matched to a unit
    of that province's list: the same pinyin; else the nearest spelling in that province (`fuzzy`, a guess unless the
    two differ by two letters or fewer); else the same pinyin in a neighbouring province.
 2. Each matched unit is walked back a year at a time to 1964. While the list of the year before holds the name (or
    the name with another suffix: a county made a city), it is the same unit. Where the name is new that year, the
    year's changes say why: a new name for an old unit (`renamed`); a unit set up or restored from another's ground
    (`part`: it goes whole to the unit named, the first named where there are several, `first of several`); a unit
    moved between provinces (`moved`). Where the changes do not say, the walk stops and the unit is shown under its
    later name (`unresolved`).
 3. The 1964 units no later unit walks back to are listed with the reason, where one is found: a county since joined
    to its city, or to another county.

Writes sources/china/crosswalk.json: {"file_year": ..., "units": [{id (the file's shapeID), file (its name), zh, list,
year, match, to: {list, zh} | null, basis, via: [the changes used], guess}], "not_shown": [...], "lists": {...}}.
tools/cnmap/base.py reads it and dissolves the geometry.
"""
import collections
import difflib
import html
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "sources", "china")
UA = "map-data-script/1.0 (generic research client)"
Y0, Y1 = 1964, 1996
BASE = "http://www.xzqh.org/html/"
# 行政区划网's list of each province -> (the province today, the unit of 1966 it lies in, CGAZ ADM1's name)
LISTS = {
    "10002": ("北京市", "peking", "Beijing Municipality"), "10003": ("天津市", "hebei", "Tianjin Municipality"),
    "10004": ("河北省", "hebei", "Hebei Province"), "10005": ("山西省", "shanxi", "Shanxi Province"),
    "10006": ("内蒙古自治区", "inner-mongolia", "Inner Mongolia Autonomous Region"),
    "10007": ("辽宁省", "liaoning", "Liaoning Province"), "10008": ("吉林省", "jilin", "Jilin Province"),
    "10009": ("黑龙江省", "heilongjiang", "Heilongjiang Province"), "10011": ("上海市", "shanghai", "Shanghai Municipality"),
    "10012": ("江苏省", "jiangsu", "Jiangsu Province"), "10013": ("浙江省", "zhejiang", "Zhejiang Province"),
    "10014": ("安徽省", "anhui", "Anhui Province"), "10015": ("福建省", "fujian", "Fujian Province"),
    "10016": ("江西省", "jiangxi", "Jiangxi Province"), "10017": ("山东省", "shandong", "Shandong Province"),
    "10018": ("河南省", "henan", "Henan Province"), "10019": ("湖北省", "hubei", "Hubei Province"),
    "10020": ("湖南省", "hunan", "Hunan Province"), "10021": ("广东省", "guangdong", "Guangzhou Province"),
    "10022": ("广西壮族自治区", "guangxi", "Guangxi Zhuang Autonomous Region"),
    "10023": ("海南省", "guangdong", "Hainan Province"), "10024": ("重庆市", "sichuan", "Chongqing Municipality"),
    "10025": ("四川省", "sichuan", "Sichuan Province"), "10026": ("贵州省", "guizhou", "Guizhou Province"),
    "10027": ("云南省", "yunnan", "Yunnan Province"), "10028": ("西藏自治区", "tibet", "Tibet Autonomous Region"),
    "10029": ("陕西省", "shaanxi", "Shaanxi Province"), "10030": ("甘肃省", "gansu", "Gansu Province"),
    "10031": ("青海省", "qinghai", "Qinghai Province"),
    "10032": ("宁夏回族自治区", "ningxia", "Ningxia Ningxia Hui Autonomous Region"),
    "10033": ("新疆维吾尔自治区", "xinjiang", "Xinjiang Uyghur Autonomous Region"),
}
MUNI = {"10002": "北京市", "10003": "天津市", "10011": "上海市", "10024": "重庆市"}
PARENT = {"10003": "10004", "10023": "10021", "10024": "10025"}     # a province made since 1964: where its units were
HAN = "一-鿿"
KIND = r"(?:自治县|自治旗|县|市|旗|特区|林区|矿区|工矿区|办事处|设治局|行政区|镇|区|管理局|行政委员会|工农区)"
SUF = r"(各族自治县|[%s]{1,8}族自治县|自治县|自治旗|县|市|旗|特区|林区|矿区|工矿区|办事处|设治局|行政区|镇|区|管理局)$" % HAN


# ---- the record: fetching and reading 行政区划网's pages

def get(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 500:
        return open(path, "rb").read()
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40) as r:
                b = r.read()
            m = re.search(rb"FP_goToURL\(/\*href\*/'([^']+)'\)", b) if len(b) < 600 else None
            if m:                                    # a stub that sends the browser on: follow it once
                time.sleep(1.2)
                with urllib.request.urlopen(urllib.request.Request(m.group(1).decode(), headers={"User-Agent": UA}), timeout=40) as r:
                    b = r.read()
            open(path, "wb").write(b)
            time.sleep(1.2)
            return b
        except Exception as e:
            print("retry", url, e, flush=True)
            time.sleep(8 * (i + 1))
    return b""


def fetch(d):
    """The year pages, 1964-1996, of every province's list (a page already there is kept)."""
    os.makedirs(d, exist_ok=True)
    dec = lambda b: b.decode("gb18030", "replace")

    def menu(s):
        years = {}
        for h, lab in re.findall(r'<a href="(show/[a-z]+/\d+\.html)"[^>]*>([^<]*)</a>', s):
            y = re.search(r"((?:19|20)\d\d)年", lab)
            if y:
                years.setdefault(int(y.group(1)), h)
        return years
    for n in LISTS:
        t = dec(get(f"{BASE}list/{n}.html", os.path.join(d, f"list-{n}.html")))
        seeds = re.findall(r'href="(show/[a-z]+/\d+\.html)"[^>]*>\s*(?:19|20)\d\d年\s*<', t)
        seeds += re.findall(r'href="(show/[a-z]+/\d+\.html)"[^>]*>[^<]*(?:19|20)\d\d年[^<]*行政区划\s*<', t)
        years = {}
        for k, h in enumerate(seeds[:8]):
            years = menu(dec(get(BASE + h, os.path.join(d, f"seed-{n}-{k}.html"))))
            if len(years) >= 25:
                break
        got = sum(bool(get(BASE + years[y], os.path.join(d, f"{n}-{y}.html"))) for y in range(Y0, Y1 + 1) if y in years)
        print(n, LISTS[n][0], "years in the menu", len(years), "pages", got, flush=True)


def page(b, lid):
    """One page: {summary, units: [{n, pref, seat, top, d (a city's district)}], notes (the year's changes)}."""
    t = b.decode("gb18030", "replace")
    m = re.search(r'<div class="content">(.*?)(?:<div class="ad_|</div>)', t, re.S)
    if not m:
        return None
    body = re.sub(r"<script.*?</script>|<!--.*?-->", "", m.group(1), flags=re.S)
    body = re.sub(r"</?(?:p|div|tr|table|tbody|li|ul)[^>]*>|<br\s*/?>", "\n", body)
    body = re.sub(r"</?(?:td|th)[^>]*>", "　　", body)
    body = html.unescape(body).replace("\xa0", "　").replace("\r", "").replace(" ", "　")
    body = re.sub(r"<(strong|b)>(.*?)</\1>", lambda m: "\n".join("<b>" + x + "</b>" for x in m.group(2).split("\n")), body, flags=re.S)
    units, notes, head, summary, in_notes = [], [], None, "", False
    if lid in MUNI:
        units.append({"n": MUNI[lid], "pref": MUNI[lid], "top": True})
    for raw in body.split("\n"):
        bold = re.findall(r"<b>(.*?)</b>", raw)
        line = re.sub(r"<[^>]+>", "", raw)
        flat = line.strip("　\t")
        if not flat:
            continue
        if not summary and not bold and re.search(r"辖.*(县|区|市)", flat):
            summary = flat
            continue
        if "变更情况" in flat or re.match(r"[★◎●]　*(?:19|20)\d\d年", flat):
            in_notes = True
        if "行政区划一览" in flat:
            in_notes = False
            continue
        if in_notes:
            notes.append(flat)
            continue
        if flat in ("★", "◎"):
            continue
        if bold:
            head = re.sub(r"[（(].*$", "", re.sub("　", "", bold[0]))
            if head.endswith("市") and len(head) <= 8 and not re.search(r"[0-9０-９]", head) and head != MUNI.get(lid):
                units.append({"n": head, "pref": head, "top": True})
            line = re.sub(r"<[^>]+>", "", raw.split("</b>")[-1])
        line = re.sub(r"(^|　)([%s])　(县|区|市|旗)(?![%s])" % (HAN, HAN), r"\1\2\3", line)   # "应　县"
        for m2 in re.finditer(r"([^　（(、，,：:]+)(?:[（(]([^）)]*)[）)])?", line):
            name = m2.group(1)
            if not re.fullmatch(r"[%s]{1,15}" % HAN + KIND, name) or re.search(r"驻|辖|个$", name):
                continue
            if re.fullmatch(r"[一二三四五六七八九十百]+(个)?" + KIND, name):
                continue
            u = {"n": name, "pref": head, "seat": m2.group(2) or ""}
            if name.endswith("区") and not re.search(r"(特区|林区|矿区|工矿区|行政区|工农区)$", name) and (
                    (head or "").endswith(("市", "特区")) or lid in MUNI or head is None or re.search(r"[0-9０-９]", head or "")):
                u["d"] = True
            units.append(u)
    return {"summary": summary, "units": units, "notes": "\n".join(notes)}


def record(d):
    out = {}
    for f in sorted(os.listdir(d)):
        m = re.fullmatch(r"(\d{5})-(\d{4})\.html", f)
        if m and m.group(1) in LISTS:
            p = page(open(os.path.join(d, f), "rb").read(), m.group(1))
            if p and p["units"]:
                out.setdefault(m.group(1), {})[int(m.group(2))] = p
    return out


# ---- names

def base(n):
    """A unit's name without its kind: 阳曲县 -> 阳曲; a one-character name keeps its kind (应县)."""
    b = re.sub(SUF, "", n)
    return b if len(b) >= 2 else n


def kind(n):
    m = re.search(SUF, n)
    k = m.group(1) if m else ""
    return ("autonomous county" if k.endswith("自治县") else "autonomous banner" if k == "自治旗" else
            {"县": "county", "市": "city", "旗": "banner", "镇": "town", "特区": "special district", "林区": "forest district",
             "矿区": "mining district", "工矿区": "mining district", "办事处": "office", "设治局": "administrative bureau",
             "行政区": "administrative district", "区": "district", "管理局": "administration"}.get(k, "unit"))


def pinyin(n):
    from pypinyin import lazy_pinyin
    return "".join(lazy_pinyin(n)).replace("ü", "u").replace("v", "u").lower()


def romanise(n):
    """A name for the map, in pinyin by rule: the base, capitalised (the characters are kept beside it)."""
    from pypinyin import lazy_pinyin
    b = re.sub(SUF, "", n) or n
    b = re.sub(r"(各族|[%s]{1,8}族)$" % HAN, "", b) or b
    syl = [s.replace("ü", "u").replace("v", "u") for s in lazy_pinyin(b)]
    out = ""
    for i, s in enumerate(syl):
        out += ("'" if i and s[0] in "aeo" else "") + s
    return out[:1].upper() + out[1:]


# ---- the walk back to 1964

def sentences(notes):
    return [s for s in re.split(r"[。；;\n]", notes) if s.strip()]


def find_prev(name, prev):
    """The unit of the year before that is this one: the same name, or the same base with another kind."""
    names = [u["n"] for u in prev if not u.get("d")]
    if name in names:
        return name
    b = base(name)
    same = [n for n in names if base(n) == b]
    if len(same) == 1:
        return same[0]
    if len(same) > 1:                   # X市 and X县 both: the county for a county, the city for anything else
        want = "县" if name.endswith("县") else "市"
        return next((n for n in same if n.endswith(want)), same[0])
    return None


def from_notes(name, notes, prev):
    """What the year's changes say of a name new that year: (old unit, basis, the sentence) or None."""
    names = [u["n"] for u in prev if not u.get("d")]
    b = base(name)
    sents = sentences(notes)
    rel = []
    for i, s in enumerate(sents):
        if name in s or (len(b) >= 2 and re.search(re.escape(b) + r"(?:县|市|旗|自治县|特区|镇|区)", s)):
            rel.append(s)
            if i + 1 < len(sents) and re.match(r"\s*[\d１-９0-9.．、\s]*(以|将|其行政)", sents[i + 1]):
                rel.append(sents[i + 1])
    for s in rel:
        m = re.search(r"([%s]{1,12}?(?:县|市|旗|区))(?:更名|改名|改称|易名|改设|改)为?" % HAN + re.escape(b), s) or \
            re.search(r"撤销([%s]{1,12}?(?:县|市|旗|区))[，,、和及]?(?:[^。]{0,12})设立" % HAN + re.escape(b), s)
        if m:
            old = find_prev(m.group(1), prev) or next((n for n in names if n in m.group(1) or base(n) == base(m.group(1))), None)
            if old and base(old) != b:
                return old, "renamed", s.strip()
    found = []
    for s in rel:
        hits = []
        for n in names:
            if base(n) == b:
                continue
            i = s.find(n)
            if i < 0 and len(base(n)) >= 2:
                m = re.search(re.escape(base(n)) + r"(?=[、和及与两三四五等县市旗])", s)
                i = m.start() if m else -1
            if i >= 0:
                hits.append((i, n))
        for i, n in sorted(hits):
            if n not in [x for x, _ in found]:
                found.append((n, s.strip()))
    if found:
        return found[0][0], "part" if len(found) == 1 else "first of several", found[0][1]
    return None


def walk(lid, name, year, rec):
    """A unit of `year` walked back to 1964: (list, the 1964 name or None, basis, the changes used)."""
    basis, via = "same", []
    rank = {"same": 0, "moved": 1, "renamed": 2, "part": 3, "first of several": 4, "unresolved": 5}
    for y in range(year, Y0, -1):
        prev = rec.get(lid, {}).get(y - 1)
        if prev is None:                # the province's list does not reach back: its parent's (Hainan, Chongqing)
            if lid in PARENT and (y - 1) in rec.get(PARENT[lid], {}):
                lid = PARENT[lid]
                prev = rec[lid][y - 1]
            else:
                return lid, None, "unresolved", via + [f"{y - 1}: no list"]
        p = find_prev(name, prev["units"])
        if p:
            name = p
            continue
        got = from_notes(name, rec[lid][y]["notes"] if y in rec.get(lid, {}) else "", prev["units"])
        if got:
            old, b, s = got
            via.append(f"{y}: {s[:120]}")
            if rank[b] > rank[basis]:
                basis = b
            name = old
            continue
        moved = [(l, find_prev(name, rec[l][y - 1]["units"])) for l in rec if l != lid and (y - 1) in rec[l]]
        moved = [(l, n) for l, n in moved if n and base(n) == base(name)]
        if len(moved) == 1:
            via.append(f"{y}: in {LISTS[moved[0][0]][0]}'s list the year before")
            lid, name = moved[0]
            if rank["moved"] > rank[basis]:
                basis = "moved"
            continue
        return lid, None, "unresolved", via + [f"{y}: {name} is new, and the year's changes do not say from what"]
    return lid, name, basis, via


def main():
    d = sys.argv[1]
    if "--fetch" in sys.argv:
        fetch(os.path.join(d, "xzqh"))
    import pyogrio.raw
    import shapely
    from shapely.geometry import shape
    rec = record(os.path.join(d, "xzqh"))
    lacking = [f"{LISTS[l][0]} {y}" for l in LISTS for y in (Y0,) if y not in rec.get(l, {}) and l not in PARENT]
    if lacking:
        print("no 1964 list:", lacking)
    # the file's units, each in its province
    meta, _, geom, fields = pyogrio.raw.read(os.path.join(d, "cgaz", "geoBoundariesCGAZ_ADM1.gpkg"), where="shapeGroup='CHN'")
    cg = dict(zip([str(x).strip() for x in fields[list(meta["fields"]).index("shapeName")]],
                  [shapely.make_valid(shapely.from_wkb(g)) for g in geom]))
    by_cgaz = {v[2]: k for k, v in LISTS.items()}
    provs = [(by_cgaz[n], g) for n, g in cg.items() if n in by_cgaz]
    feats = json.load(open(os.path.join(d, "gb", "adm2.geojson"), encoding="utf-8"))["features"]
    units = []
    for f in feats:
        g = shapely.make_valid(shape(f["geometry"]))
        pt = g.representative_point()
        hit = [l for l, pg in provs if pg.contains(pt)]
        if not hit:
            near = min(provs, key=lambda t: t[1].distance(pt))
            if near[1].distance(pt) > 0.25:
                continue                    # Taiwan, Hong Kong, Macau: not the PRC's units
            hit = [near[0]]
        near2 = [l for l, pg in provs if l != hit[0] and pg.distance(g) < 0.05]
        units.append({"id": f["properties"]["shapeID"], "file": f["properties"]["shapeName"] or "", "list": hit[0], "near": near2})
    print(len(feats), "units in the file;", len(units), "in the PRC's provinces")
    # the file's year: the lists' year whose names match most
    pin = {(l, y): {pinyin(u["n"]): u["n"] for u in p["units"] if not u.get("d")} for l, ys in rec.items() for y, p in ys.items()}
    score = collections.Counter()
    for y in range(1980, Y1 + 1):
        score[y] = sum(1 for u in units if u["file"].lower() in pin.get((u["list"], y), {}))
    print("matches by year:", {y: score[y] for y in sorted(score)})
    V = max(score, key=lambda y: (score[y], -y))
    print("the file's year taken as", V)
    counts = collections.Counter()
    for u in units:
        f = u["file"].lower()
        u["year"], u["zh"], u["match"] = V, None, None
        order = [V] + sorted((y for y in range(1980, Y1 + 1) if y != V), key=lambda y: abs(y - V))
        for y in order:                                # the same pinyin, in its province, the file's year first
            if f in pin.get((u["list"], y), {}):
                u.update(zh=pin[(u["list"], y)][f], year=y, match="name" if y == V else "name, another year")
                break
        if not u["zh"]:                                # the nearest spelling in its province
            cand = pin.get((u["list"], V), {})
            best = difflib.get_close_matches(f, list(cand), n=1, cutoff=0.82)
            if best:
                diff = sum(1 for o in difflib.ndiff(f, best[0]) if o[0] in "+-")
                u.update(zh=cand[best[0]], match="spelling" if diff <= 2 else "spelling, a guess")
        if not u["zh"]:                                # the same pinyin in a neighbouring province
            for l in u["near"]:
                for y in order:
                    if f in pin.get((l, y), {}):
                        u.update(zh=pin[(l, y)][f], list=l, year=y, match="name, the next province")
                        break
                if u["zh"]:
                    break
        counts[u["match"] or "no match"] += 1
    print("matched:", dict(counts))
    # the walk back
    to = collections.defaultdict(list)
    basis = collections.Counter()
    for u in units:
        if not u["zh"]:
            u.update(to=None, basis="unmatched", via=[], guess=True)
            basis["unmatched"] += 1
            continue
        l, n, b, via = walk(u["list"], u["zh"], u["year"], rec)
        u.update(to={"list": l, "zh": n} if n else None, basis=b, via=via,
                 guess=bool(b in ("first of several", "unresolved") or (u["match"] or "").endswith("a guess")))
        basis[b] += 1
        if n:
            to[(l, n)].append(u["id"])
    print("walked back:", dict(basis))
    # the 1964 units no later unit reaches
    not_shown = []
    for l in sorted(rec):
        if Y0 not in rec[l]:
            continue
        for x in rec[l][Y0]["units"]:
            if x.get("d") or (l, x["n"]) in to:
                continue
            why = ""
            if x["n"].endswith("县") and any(k == l and base(n) == base(x["n"]) for k, n in to):
                why = "since joined to the city of its name"
            not_shown.append({"list": l, "zh": x["n"], "pref": x.get("pref") or "", "why": why})
    n64 = sum(1 for l in rec if Y0 in rec[l] for x in rec[l][Y0]["units"] if not x.get("d"))
    print("1964 units in the lists:", n64, "; drawn:", len(to), "; not shown:", len(not_shown))
    lists = {l: {"name": LISTS[l][0], "unit": LISTS[l][1],
                 "units_1964": [{"zh": x["n"], "pref": x.get("pref") or "", "seat": x.get("seat") or ""}
                                for x in rec[l][Y0]["units"] if not x.get("d")] if Y0 in rec.get(l, {}) else []}
             for l in LISTS}
    for u in units:
        u.pop("near", None)
    json.dump({"file": "geoBoundaries gbOpen CHN ADM2 (CHN-ADM2-17275852), PDDL 1.0", "file_year": V,
               "record": "行政区划网 (xzqh.org), each province's lists, 1964-1996, read Nov. 26, 2026",
               "units": units, "not_shown": not_shown, "lists": lists},
              open(os.path.join(OUT, "crosswalk.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("wrote sources/china/crosswalk.json")


if __name__ == "__main__":
    main()
