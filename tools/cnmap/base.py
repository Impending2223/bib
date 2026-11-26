"""One border geometry for the map of China (Nov. 22, 2026; the owner: "We should probably give ourselves a China map.
Like our Southeast Asia/Indochina map. The minimum viable product would give us the provinces, counties, places."): the
countries of East and Central Asia, the PRC's provinces as of 1966 and its counties as of 1964, from one coverage
simplified together, so that neighbours meet and no line is drawn twice (tools/vnmap/base.py's method). A one-time
script, run after tools/cnmap/counties.py has written sources/china/crosswalk.json:

    python3 -I tools/cnmap/base.py DIR

DIR is the download directory counties.py names. This script reads from it:
 - DIR/cgaz/geoBoundariesCGAZ_ADM0.gpkg and geoBoundariesCGAZ_ADM1.gpkg: geoBoundaries' Comprehensive Global
   Administrative Zones (CGAZ), main branch as read Nov. 22 and 26, 2026 (release 6.0.0), from
   https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/main/releaseData/CGAZ/ (CC BY 4.0; the country
   lines are the U.S. Department of State's Large Scale International Boundaries);
 - DIR/gb/adm2.geojson: geoBoundaries gbOpen CHN ADM2, the county-level units (counties.py's docstring; PDDL 1.0).
Needs shapely >= 2.1, pyproj, pyogrio, pypinyin.

The steps (each adjustment stated in sources/china/README.md):
 1. The countries: CGAZ ADM0, cut to FRAME. CGAZ's disputed areas kept as areas of their own (Aksai Chin and the
    other sectors of the Sino-Indian line, Kalapani, Siachen); the Paracels, the Senkakus and Liancourt left out.
 2. Hong Kong and Macau: CGAZ ADM1's, cut to the country.
 3. Inside the rest of China, the county file's units, each cut to the country, the country's slivers that no unit
    covers given to the nearest unit. (The first version, of Nov. 22, took the provinces from CGAZ ADM1: its province
    lines lie up to 13 km off, Nanxiong in Jiangxi, Linzhang in Henan, so the provinces are now dissolved from the
    counties, as the Republic of Vietnam's were from its districts.)
 4. One coverage: shapely.coverage_clean, coverage_simplify (TOL); islets under MIN_KM2 dropped.
 5. Dissolved: the counties of 1964 (crosswalk.json: each later unit's county; a unit not traced back stays as it
    is), the provinces of 1966 (Chongqing in Sichuan, Hainan in Guangdong, Tianjin in Hebei: the display year 1966;
    Tianjin was Hebei's from 1958 to Jan. 1967), the countries; the lines each once at its rank (intl, disp, unit,
    county), the coast apart. Label points: polylabel of each area's largest part.

Writes, in sources/china/: admin.geojson (`k`: land, disp, unit, line, lab), counties.geojson (`k`: county, line, lab),
units.json (each 1966 unit's id, name, kind, the today's provinces it holds, km2) and counties.json (each county of
1964 drawn: id, name in pinyin by rule, zh, kind, 1966 unit, its 1964 province and prefecture, the later units it is
made of and on what basis, `guess`; each later unit shown as it is; the 1964 units not shown).
"""
import json
import os
import sys
import time

import numpy as np
import pyogrio.raw
import shapely
from pyproj import Geod
from shapely.geometry import box, mapping
from shapely.ops import polylabel

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "sources", "china")
FRAME = (66.0, 10.0, 142.0, 58.0)    # lon/lat: the shapes are cut here; cnmap.BOUNDS lies inside
TOL = 0.008                          # coverage_simplify tolerance, degrees (~800 m)
MIN_KM2 = 4.0
PREC = 3
GEOD = Geod(ellps="WGS84")

COUNTRY = {"CHN": "China", "TWN": "Taiwan", "MNG": "Mongolia", "RUS": "Soviet Union", "PRK": "North Korea",
           "KOR": "South Korea", "JPN": "Japan", "VNM": "Vietnam", "LAO": "Laos", "MMR": "Burma", "IND": "India",
           "NPL": "Nepal", "BTN": "Bhutan", "BGD": "East Pakistan", "PAK": "Pakistan", "AFG": "Afghanistan",
           "TJK": "Soviet Union", "KGZ": "Soviet Union", "KAZ": "Soviet Union", "UZB": "Soviet Union",
           "THA": "Thailand", "PHL": "Philippines", "KHM": "Cambodia", "TKM": "Soviet Union"}
# the country ids the map uses (the Soviet republics one country; East Pakistan named for the 1960s)
CID = {"CHN": "prc", "TWN": "roc", "MNG": "mongolia", "RUS": "ussr", "TJK": "ussr", "KGZ": "ussr", "KAZ": "ussr",
       "UZB": "ussr", "TKM": "ussr", "PRK": "dprk", "KOR": "rok", "JPN": "japan", "VNM": "vietnam", "LAO": "laos",
       "MMR": "burma", "IND": "india", "NPL": "nepal", "BTN": "bhutan", "BGD": "pakistan-east", "PAK": "pakistan",
       "AFG": "afghanistan", "THA": "thailand", "PHL": "philippines", "KHM": "cambodia"}
NAMES = {"prc": "China", "roc": "Taiwan", "mongolia": "Mongolia", "ussr": "Soviet Union", "dprk": "North Korea",
         "rok": "South Korea", "japan": "Japan", "vietnam": "Vietnam", "laos": "Laos", "burma": "Burma",
         "india": "India", "nepal": "Nepal", "bhutan": "Bhutan", "pakistan-east": "East Pakistan",
         "pakistan": "Pakistan", "afghanistan": "Afghanistan", "thailand": "Thailand", "philippines": "Philippines",
         "cambodia": "Cambodia"}
DROP_DISP = ("Paracel Is", "Senkakus", "Liancourt Rocks")

# CGAZ ADM1 (China) -> the 1966 unit; its name, kind and dates (sources/china/README.md, each with its source)
UNIT = {
    "Anhui Province": "anhui", "Fujian Province": "fujian", "Gansu Province": "gansu",
    "Guangzhou Province": "guangdong", "Hainan Province": "guangdong",          # Hainan: Guangdong's until 1988
    "Guangxi Zhuang Autonomous Region": "guangxi", "Guizhou Province": "guizhou",
    "Hebei Province": "hebei", "Tianjin Municipality": "hebei",                # Tianjin: Hebei's, 1958 - Jan. 1967
    "Heilongjiang Province": "heilongjiang", "Henan Province": "henan", "Hubei Province": "hubei",
    "Hunan Province": "hunan", "Inner Mongolia Autonomous Region": "inner-mongolia", "Jiangsu Province": "jiangsu",
    "Jiangxi Province": "jiangxi", "Jilin Province": "jilin", "Liaoning Province": "liaoning",
    "Ningxia Ningxia Hui Autonomous Region": "ningxia", "Qinghai Province": "qinghai", "Shaanxi Province": "shaanxi",
    "Shandong Province": "shandong", "Shanxi Province": "shanxi",
    "Sichuan Province": "sichuan", "Chongqing Municipality": "sichuan",         # Chongqing: Sichuan's until 1997
    "Tibet Autonomous Region": "tibet", "Xinjiang Uyghur Autonomous Region": "xinjiang", "Yunnan Province": "yunnan",
    "Zhejiang Province": "zhejiang", "Beijing Municipality": "peking", "Shanghai Municipality": "shanghai",
    "Hong Kong Special Administrative Region": "hong-kong", "Macau Special Administrative Region": "macau",
}
META = {
    "anhui": ("Anhui", "province"), "fujian": ("Fujian", "province"), "gansu": ("Gansu", "province"),
    "guangdong": ("Guangdong", "province"), "guangxi": ("Guangxi", "autonomous region"),
    "guizhou": ("Guizhou", "province"), "hebei": ("Hebei", "province"), "heilongjiang": ("Heilongjiang", "province"),
    "henan": ("Henan", "province"), "hubei": ("Hubei", "province"), "hunan": ("Hunan", "province"),
    "inner-mongolia": ("Inner Mongolia", "autonomous region"), "jiangsu": ("Jiangsu", "province"),
    "jiangxi": ("Jiangxi", "province"), "jilin": ("Jilin", "province"), "liaoning": ("Liaoning", "province"),
    "ningxia": ("Ningxia", "autonomous region"), "qinghai": ("Qinghai", "province"), "shaanxi": ("Shaanxi", "province"),
    "shandong": ("Shandong", "province"), "shanxi": ("Shanxi", "province"), "sichuan": ("Sichuan", "province"),
    "tibet": ("Tibet", "autonomous region"), "xinjiang": ("Xinjiang", "autonomous region"),
    "yunnan": ("Yunnan", "province"), "zhejiang": ("Zhejiang", "province"), "peking": ("Peking", "municipality"),
    "shanghai": ("Shanghai", "municipality"), "hong-kong": ("Hong Kong", "British colony"),
    "macau": ("Macau", "Portuguese colony"),
}
FULL = {"guangxi": "Guangxi Zhuang Autonomous Region (from Mar. 1958)",
        "ningxia": "Ningxia Hui Autonomous Region (from Oct. 1958)",
        "tibet": "Tibet Autonomous Region (from Sept. 1965; the Tibet region, under its Preparatory Committee, before)",
        "xinjiang": "Xinjiang Uighur Autonomous Region (from 1955)",
        "inner-mongolia": "Inner Mongolia Autonomous Region (its pre-1969 shape)",
        "hebei": "Hebei (with Tianjin, its capital 1958–66; Tianjin a municipality again from Jan. 1967)",
        "sichuan": "Sichuan (with Chongqing, a municipality only from 1997)",
        "guangdong": "Guangdong (with Hainan, a province only from 1988)"}


def km2(g):
    return abs(GEOD.geometry_area_perimeter(g)[0]) / 1e6


def polys(g):
    if g is None or g.is_empty:
        return []
    if g.geom_type == "Polygon":
        return [g]
    if hasattr(g, "geoms"):
        return [p for q in g.geoms for p in polys(q)]
    return []


def multi(ps):
    ps = [p for p in ps if not p.is_empty]
    return shapely.MultiPolygon(ps) if len(ps) > 1 else (ps[0] if ps else shapely.Polygon())


def read(level, where):
    meta, _, geom, fields = pyogrio.raw.read(os.path.join(sys.argv[1], "cgaz", f"geoBoundariesCGAZ_ADM{level}.gpkg"),
                                             bbox=FRAME, where=where)
    names = list(meta["fields"])
    out = []
    for i in range(len(geom)):
        d = dict(zip(names, [f[i] for f in fields]))
        d["g"] = multi(polys(shapely.make_valid(shapely.from_wkb(geom[i]))))
        d["shapeName"] = (d.get("shapeName") or "").strip()
        out.append(d)
    return out


def fill(country, pieces):
    """The pieces cut to the country; each sliver of the country no piece covers to the piece nearest it."""
    gs = [multi(polys(shapely.intersection(p, country))) for p in pieces]
    rest = [s for s in polys(shapely.difference(country, shapely.union_all(gs))) if s.area > 1e-8]
    tree = shapely.STRtree(gs)
    extra = {}
    for s in rest:
        j = int(tree.query_nearest(s)[0])
        extra.setdefault(j, []).append(s)
    for j, ss in extra.items():
        gs[j] = multi(polys(shapely.union_all([gs[j]] + ss)))
    return gs


def rnd(c):
    return [rnd(x) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], PREC), round(c[1], PREC)]


def feat(g, props):
    m = mapping(g)
    return {"type": "Feature", "properties": props, "geometry": {"type": m["type"], "coordinates": rnd(m["coordinates"])}}


def lines(geoms, minus=None):
    b = shapely.union_all([g.boundary for g in geoms if not g.is_empty])
    if minus is not None and not minus.is_empty:
        b = shapely.difference(b, minus)
    return shapely.line_merge(shapely.union_all([x for x in getattr(b, "geoms", [b])
                                                 if x.geom_type in ("LineString", "MultiLineString")]))


def label_point(g):
    big = max(polys(g), key=lambda p: p.area)
    return polylabel(big, tolerance=0.01)


T0 = time.time()


def log(*a):
    print(f"{time.time() - T0:7.1f}s", *a, flush=True)


BASIS = {"same": "the later unit of the name", "renamed": "the later unit, under the name of 1964",
         "moved": "the later unit of the name, in another province's list since",
         "part": "with a later unit set up from its ground", "first of several": "with a later unit set up from its "
         "ground and others' (a guess)"}


def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import counties as rec
    from shapely.geometry import shape
    frame = box(*FRAME)
    X = json.load(open(os.path.join(OUT, "crosswalk.json"), encoding="utf-8"))
    xw = {u["id"]: u for u in X["units"]}
    a0 = read(0, None)
    log("read ADM0", len(a0))
    a1 = {d["shapeName"]: d for d in read(1, "shapeGroup='CHN'")}
    log("read ADM1", len(a1))
    pieces, props = [], []
    chn = None
    for d in a0:
        g = multi(polys(shapely.intersection(d["g"], frame)))
        if g.is_empty:
            continue
        if d["shapeType"] == "DISP":
            if d["shapeName"] in DROP_DISP:
                continue
            pieces.append(g)
            props.append({"k": "disp", "name": d["shapeName"]})
        elif d["shapeGroup"] == "CHN":
            chn = g
        elif d["shapeGroup"] in CID:
            pieces.append(g)
            props.append({"k": "land", "c": CID[d["shapeGroup"]]})
    all2 = json.load(open(os.path.join(sys.argv[1], "gb", "adm2.geojson"), encoding="utf-8"))["features"]
    # Hong Kong and Macau: CGAZ ADM1's (its Hong Kong is the New Territories' north alone) with the county file's own
    colony = {}
    for n, u in UNIT.items():
        if u in ("hong-kong", "macau"):
            own = [shapely.make_valid(shape(f["geometry"])) for f in all2 if rec.COLONY.get(f["properties"]["shapeName"] or "") == u]
            colony[u] = multi(polys(shapely.intersection(shapely.union_all([a1[n]["g"]] + own), chn)))
    main_ = multi(polys(shapely.difference(chn, shapely.union_all(list(colony.values())))))
    feats2 = [f for f in all2 if f["properties"]["shapeID"] in xw]
    gs2 = [multi(polys(shapely.make_valid(shape(f["geometry"])))) for f in feats2]
    for f, g in zip(feats2, fill(main_, gs2)):
        if g.is_empty:
            continue
        pieces.append(g)
        props.append({"k": "x", "id": f["properties"]["shapeID"]})
    for u, g in colony.items():
        pieces.append(g)
        props.append({"k": "colony", "u": u})
    log("pieces", len(pieces))
    clean = shapely.coverage_clean(np.array(pieces, dtype=object), gap_width=0.002)
    log("coverage valid after clean:", shapely.coverage_is_valid(clean))
    simp = shapely.coverage_simplify(clean, TOL)
    simp = [multi([q for q in polys(s) if km2(q) >= MIN_KM2]) for s in simp]
    log("simplified")
    # each later unit's county of 1964 (or itself, where it is not traced back), and its unit of 1966
    L = X["lists"]
    info64 = {(l, x["zh"]): x for l, v in L.items() for x in v["units_1964"]}
    cty, cmeta, units, made, country, disp = {}, {}, {}, {}, {}, {}
    for g, p in zip(simp, props):
        if g.is_empty:
            continue
        if p["k"] == "x":
            u = xw[p["id"]]
            u66 = L[u["list"]]["unit"]
            if u.get("to"):
                key = ("c", u["to"]["list"], u["to"]["zh"])
            else:
                key = ("x", u["list"], u.get("zh") or u["file"])
            cty.setdefault(key, []).append(g)
            cmeta.setdefault(key, []).append(u)
            units.setdefault(u66, []).append(g)
            made.setdefault(u66, set()).add(L[u["list"]]["name"])
            country.setdefault("prc", []).append(g)
        elif p["k"] == "colony":
            units.setdefault(p["u"], []).append(g)
            made.setdefault(p["u"], set()).add(META[p["u"]][0])
            country.setdefault(p["u"], []).append(g)
        elif p["k"] == "disp":
            disp.setdefault(p["name"], []).append(g)
        else:
            country.setdefault(p["c"], []).append(g)
    diss = lambda d: {k: multi(polys(shapely.coverage_union_all(gs))) for k, gs in d.items()}
    cty, units, country, disp = diss(cty), diss(units), diss(country), diss(disp)
    land = shapely.union_all(list(country.values()) + list(disp.values()))
    fb = frame.boundary.buffer(1e-7)
    coast = shapely.difference(land.boundary, fb)
    top0 = shapely.union_all([coast, fb])
    intl = lines(list(country.values()), top0)
    dl = lines(list(disp.values()), shapely.union_all([top0, intl.buffer(1e-7)]))
    top = shapely.union_all([top0, intl.buffer(1e-7), dl.buffer(1e-7)])
    prc_units = [g for u, g in units.items() if u not in ("hong-kong", "macau")]
    unitl = lines(prc_units, top)
    countyl = lines(list(cty.values()), shapely.union_all([top, unitl.buffer(1e-7)]))
    log("lines")
    feats = []
    for c, g in sorted(country.items()):
        if c in ("prc", "hong-kong", "macau"):
            continue
        feats.append(feat(g, {"k": "land", "id": c, "name": NAMES[c]}))
    for n, g in sorted(disp.items()):
        feats.append(feat(g, {"k": "disp", "name": n, "km2": round(km2(g))}))
    rows = []
    for u, g in sorted(units.items()):
        name, kind = META[u]
        c = "prc" if u not in ("hong-kong", "macau") else u
        a = round(km2(g))
        feats.append(feat(g, {"k": "unit", "id": u, "name": name, "kind": kind, "c": c, "km2": a,
                              **({"full": FULL[u]} if u in FULL else {})}))
        rows.append({"id": u, "name": name, "kind": kind, "c": c, "full": FULL.get(u, name),
                     "made_of": sorted(made[u]), "km2": a})
    for cls, g in (("coast", coast), ("intl", intl), ("disp", dl), ("unit", unitl)):
        if not g.is_empty:                  # the units' lines carry the country, as tools/vnmap/base.py's do (the client's filter)
            feats.append(feat(g, {"k": "line", "l": cls, **({"c": "prc"} if cls == "unit" else {})}))
    for u, g in units.items():
        pt = label_point(g)
        feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": rnd([pt.x, pt.y])},
                      "properties": {"k": "lab", "l": "unit", "id": u, "name": META[u][0], "km2": round(km2(g)),
                                     "c": "prc" if u not in ("hong-kong", "macau") else u}})
    for c, g in country.items():
        if c in ("hong-kong", "macau"):
            continue
        inview = multi([q for q in polys(shapely.intersection(g, box(70, 14, 138, 55)))])
        if inview.is_empty or km2(inview) < 20000:
            continue
        pt = label_point(inview)
        feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": rnd([pt.x, pt.y])},
                      "properties": {"k": "lab", "l": "country", "id": c, "name": NAMES[c], "km2": round(km2(inview))}})
    os.makedirs(OUT, exist_ok=True)
    s = json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False, separators=(",", ":"))
    open(os.path.join(OUT, "admin.geojson"), "w", encoding="utf-8").write(s + "\n")
    json.dump({"display_year": 1966, "source": "geoBoundaries CGAZ 6.0.0 ADM0 (CC BY 4.0); gbOpen CHN ADM2 (PDDL 1.0)",
               "units": rows}, open(os.path.join(OUT, "units.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log("wrote admin.geojson", f"{len(s.encode()):,} bytes;", len(rows), "units")
    # the counties
    cf, crow, ids = [], [], set()
    for key, g in sorted(cty.items(), key=lambda kv: (kv[0][1], kv[0][2])):
        traced, l, zh = key[0] == "c", key[1], key[2]
        us = cmeta[key]
        u66 = L[us[0]["list"]]["unit"]
        han = any("\u4e00" <= ch <= "\u9fff" for ch in zh)
        name = rec.romanise(zh) if han else rec_file_name(zh)
        low = zh.lower()
        kind = rec.kind(zh) if han else ("county" if low.endswith("xian") else "city" if low.endswith("shi")
                                         else "banner" if low.endswith("qi") else "unit")
        cid = base_id = f"{L[l]['unit'] if traced else u66}-{rec.pinyin(zh) if han else zh.lower()}"
        n = 2
        while cid in ids:
            cid, n = f"{base_id}-{n}", n + 1
        ids.add(cid)
        a = round(km2(g))
        if traced:
            worst = max(us, key=lambda u: list(BASIS).index(u["basis"]) if u["basis"] in BASIS else 9)
            guess = any(u.get("guess") for u in us)
            x = info64.get((l, zh), {})
            later = sorted({u["zh"] for u in us if u["zh"] != zh})
            what = BASIS.get(worst["basis"], worst["basis"])
            if kind == "city" and worst["basis"] in ("same", "moved"):
                what = "the later city, larger than the city of 1964"
            line = f"{zh} · {kind}, end of 1964 · {L[l]['name']}" + (f", {x['pref']}" if x.get("pref") and x["pref"] != zh else "") \
                + f" · {what}" + (": " + "、".join(later) if later else "") + (" · a guess" if guess and "guess" not in what else "")
            crow.append({"id": cid, "name": name, "zh": zh, "kind": kind, "unit": u66, "province_1964": L[l]["name"],
                         "pref": x.get("pref") or "", "seat": x.get("seat") or "", "km2": a, "guess": guess,
                         "made_of": [{"file": u["file"], "zh": u["zh"], "year": u["year"], "match": u["match"],
                                      "basis": u["basis"], "via": u["via"]} for u in us]})
        else:
            u = us[0]
            why = ("no list of 1964 was had for " + L[l]["name"]) if not L[l]["units_1964"] and l not in rec.PARENT else \
                ("its name was not found in the lists" if u["basis"] == "unmatched" else "not traced back to 1964")
            line = f"{zh} · a later unit (about {X['file_year']}), shown as it is: {why}"
            crow.append({"id": cid, "name": name, "zh": zh if han else "", "kind": kind, "unit": u66, "later": True,
                         "why": why, "km2": a, "guess": True,
                         "made_of": [{"file": u["file"], "zh": u.get("zh"), "year": u.get("year"), "match": u.get("match"),
                                      "basis": u["basis"], "via": u.get("via", [])} for u in us]})
        cf.append(feat(g, {"k": "county", "id": cid, "name": name, "line": line, "u": u66}))
        pt = label_point(g)
        cf.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": rnd([pt.x, pt.y])},
                   "properties": {"k": "lab", "l": "county", "id": cid, "name": name, "km2": a}})
    if not countyl.is_empty:
        cf.append(feat(countyl, {"k": "line", "l": "county"}))
    s = json.dumps({"type": "FeatureCollection", "features": cf}, ensure_ascii=False, separators=(",", ":"))
    open(os.path.join(OUT, "counties.geojson"), "w", encoding="utf-8").write(s + "\n")
    json.dump({"year": 1964, "file": X["file"], "file_year": X["file_year"], "record": X["record"], "counties": crow,
               "not_shown": [dict(x, province=L[x["list"]]["name"]) for x in X["not_shown"]]},
              open(os.path.join(OUT, "counties.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    n64 = sum(1 for c in crow if not c.get("later"))
    log("wrote counties.geojson", f"{len(s.encode()):,} bytes;", n64, "counties of 1964,",
        sum(1 for c in crow if c.get("guess") and not c.get("later")), "on a guess;",
        len(crow) - n64, "later units shown as they are;", len(X["not_shown"]), "units of 1964 not shown")


def rec_file_name(n):
    """A unit known only by the file's pinyin name: its base, capitalised (Zunyixian -> Zunyi)."""
    import re
    b = re.sub(r"(zizhixian|zizhiqi|xian|shi|qi|qu)$", "", n) or n
    return b[:1].upper() + b[1:]


if __name__ == "__main__":
    main()
