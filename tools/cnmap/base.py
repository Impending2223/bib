"""One border geometry for the map of China (Nov. 22, 2026; the owner: "We should probably give ourselves a China map.
Like our Southeast Asia/Indochina map."): the countries of East and Central Asia, and the PRC's provinces as of 1966,
from one source and simplified together, so that neighbours meet and no line is drawn twice (tools/vnmap/base.py's
method). A one-time script:

    python3 -I tools/cnmap/base.py CGAZ_DIR

CGAZ_DIR holds geoBoundaries' Comprehensive Global Administrative Zones (CGAZ), main branch as read Nov. 22, 2026
(release 6.0.0), geoBoundariesCGAZ_ADM0.gpkg and geoBoundariesCGAZ_ADM1.gpkg, from
https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/main/releaseData/CGAZ/ (CC BY 4.0; the country lines
are the U.S. Department of State's Large Scale International Boundaries). Needs shapely >= 2.1, pyproj, pyogrio.

The steps (each adjustment stated in sources/china/README.md):
 1. The countries: CGAZ ADM0, cut to FRAME. CGAZ's disputed areas kept as areas of their own (Aksai Chin and the
    other sectors of the Sino-Indian line, Kalapani, Siachen); the Paracels, the Senkakus and Liancourt left out.
 2. Inside China, CGAZ ADM1 (today's provinces, cut to the country, its slivers given to the nearest unit).
 3. One coverage: shapely.coverage_clean, coverage_simplify (TOL); islets under MIN_KM2 dropped.
 4. Today's units to the 1966 provinces (UNIT): Chongqing to Sichuan, Hainan to Guangdong, Tianjin to Hebei (the
    display year 1966: Tianjin was Hebei's from 1958 to Jan. 1967); Hong Kong and Macau the colonies; Taiwan the ROC's.
 5. Dissolved: the provinces, the countries; the lines each once at its rank (intl, disp, unit), the coast apart.
    Label points: polylabel of each unit's largest part.

Writes sources/china/admin.geojson (`k`: land, disp, unit, line, lab) and sources/china/units.json (each 1966 unit's
id, name, kind, from, the today's units it was made of, km2).
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
    meta, _, geom, fields = pyogrio.raw.read(os.path.join(sys.argv[1], f"geoBoundariesCGAZ_ADM{level}.gpkg"),
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


def main():
    frame = box(*FRAME)
    a0 = read(0, None)
    log("read ADM0", len(a0))
    a1 = [d for d in read(1, "shapeGroup='CHN'") if d["shapeName"] in UNIT]
    log("read ADM1", len(a1))
    missing = set(UNIT) - {d["shapeName"] for d in a1}
    if missing:
        raise SystemExit(f"CGAZ ADM1 lacks {sorted(missing)}")
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
    for d, g in zip(a1, fill(chn, [d["g"] for d in a1])):
        pieces.append(g)
        props.append({"k": "unit", "adm1": d["shapeName"], "id1": d["shapeID"], "u": UNIT[d["shapeName"]]})
    log("pieces", len(pieces))
    clean = shapely.coverage_clean(np.array(pieces, dtype=object), gap_width=0.002)
    log("coverage valid after clean:", shapely.coverage_is_valid(clean))
    simp = shapely.coverage_simplify(clean, TOL)
    simp = [multi([q for q in polys(s) if km2(q) >= MIN_KM2]) for s in simp]
    log("simplified")
    units, made, country, disp = {}, {}, {}, {}
    for g, p in zip(simp, props):
        if g.is_empty:
            continue
        if p["k"] == "unit":
            units.setdefault(p["u"], []).append(g)
            made.setdefault(p["u"], []).append(p["adm1"])
            country.setdefault("prc" if p["u"] not in ("hong-kong", "macau") else p["u"], []).append(g)
        elif p["k"] == "disp":
            disp.setdefault(p["name"], []).append(g)
        else:
            country.setdefault(p["c"], []).append(g)
    units = {u: multi(polys(shapely.coverage_union_all(gs))) for u, gs in units.items()}
    country = {c: multi(polys(shapely.coverage_union_all(gs))) for c, gs in country.items()}
    disp = {n: multi(polys(shapely.coverage_union_all(gs))) for n, gs in disp.items()}
    land = shapely.union_all(list(country.values()) + list(disp.values()))
    fb = frame.boundary.buffer(1e-7)
    coast = shapely.difference(land.boundary, fb)
    top0 = shapely.union_all([coast, fb])
    intl = lines(list(country.values()), top0)
    dl = lines(list(disp.values()), shapely.union_all([top0, intl.buffer(1e-7)]))
    top = shapely.union_all([top0, intl.buffer(1e-7), dl.buffer(1e-7)])
    prc_units = [g for u, g in units.items() if u not in ("hong-kong", "macau")]
    unitl = lines(prc_units, top)
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
        if not g.is_empty:
            feats.append(feat(g, {"k": "line", "l": cls}))
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
    json.dump({"display_year": 1966, "source": "geoBoundaries CGAZ 6.0.0 ADM0, ADM1 (CC BY 4.0)", "units": rows},
              open(os.path.join(OUT, "units.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log("wrote admin.geojson", f"{len(s.encode()):,} bytes;", len(rows), "units")


if __name__ == "__main__":
    main()
