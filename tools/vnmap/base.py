"""One border geometry for the maps of Indochina (Oct. 22, 2026): the countries, the RVN's provinces of late 1966, and
the provinces of North Vietnam, Laos and Cambodia, all from one source and simplified together, so that neighbours
meet and no line is drawn twice. A one-time script:

    python3 -I tools/vnmap/base.py CGAZ_DIR

CGAZ_DIR holds geoBoundaries' Comprehensive Global Administrative Zones (CGAZ), release 6.0.0, downloaded Oct. 22, 2026
from https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/main/releaseData/CGAZ/
geoBoundariesCGAZ_ADM{0,1,2}.gpkg (CC BY 4.0; the country lines are the U.S. Department of State's Large Scale
International Boundaries, LSIB). Needs shapely >= 2.1 (coverage functions), pyproj and pyogrio (pip).

The steps:
 1. The countries: CGAZ ADM0, cut to FRAME. The Paracels (CGAZ's disputed area) left out, as before.
 2. Inside Vietnam, CGAZ ADM2 districts; inside Laos and Cambodia, CGAZ ADM1 provinces: each cut to its country, and
    the slivers of the country no unit covers (CGAZ's levels come from different sources and do not nest exactly)
    given to the unit with which they share most border, else the nearest. Elsewhere the country is one piece.
 3. These pieces make one coverage: shapely.coverage_clean, then shapely.coverage_simplify (TOL), which simplifies
    every shared edge once, so the two sides of a line stay identical. Islets under MIN_KM2 dropped.
 4. Each Vietnamese district goes whole to the 1966 unit of sources/vn-provinces-1966/provinces1966.geojson (the old
    GADM-based polygons, which follow the hand crosswalk, tools/vnmap/xw.py) holding most of it; a district less than
    half inside any 1966 unit is the DRV's (north of the Bến Hải: Vĩnh Linh, Cồn Cỏ, and today's provinces to the
    north). Each district's modern province is CGAZ ADM1's holding most of it. The assignment and each district's
    share go to sources/vn-provinces-1966/crosswalk-cgaz.yaml, with the districts whose share is under SURE.
 5. Everything else is dissolved from the simplified pieces (shapely.coverage_union_all): the 1966 units, the corps
    zones, today's regions, the DRV's provinces (today's, Vĩnh Linh apart as the special zone of 1954-76), Laos's and
    Cambodia's (today's), the countries (the RVN and the DRV apart). The lines are the dissolved pieces' boundaries,
    each kept once at its highest rank (international, the demarcation line, corps zone, region, province) and the
    coast apart. Label points: shapely's polylabel of each unit's largest part.

Writes sources/indochina/admin.geojson (what the map draws: `k` land, unit, line, lab; see vnmap STYLE) and, for the
series' checks and the gazetteer, sources/vn-provinces-1966/provinces1966.geojson, ctz1966.geojson, regions.geojson,
outline.geojson and indochina-outline.geojson, and the gazetteer's provinces (places.json `province`) by point in
polygon on the new units, reporting every change.
"""
import json
import os
import sys
import unicodedata

import numpy as np
import pyogrio.raw
import shapely
import yaml
from pyproj import Geod
from shapely.geometry import box, mapping, shape
from shapely.ops import polylabel

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
VN66 = os.path.join(ROOT, "sources", "vn-provinces-1966")
OUT = os.path.join(ROOT, "sources", "indochina")
FRAME = (97.0, 5.0, 114.5, 26.5)     # lon/lat: the shapes are cut here; the map's bounds lie inside (vnmap.BOUNDS)
TOL = 0.002                          # coverage_simplify tolerance, degrees (~200 m)
MIN_KM2 = 0.5                        # islets smaller than this dropped
SURE = 0.9                           # a district with a smaller share in its 1966 unit is listed as a straddler
PREC = 4                             # decimals in the output (~11 m)
GEOD = Geod(ellps="WGS84")

COUNTRY = {"VNM": "Vietnam", "LAO": "Laos", "KHM": "Cambodia", "THA": "Thailand", "CHN": "China", "MMR": "Burma",
           "MYS": "Malaysia", "IDN": "Indonesia"}
CID = {"LAO": "laos", "KHM": "cambodia", "THA": "thailand", "CHN": "china", "MMR": "burma", "MYS": "malaysia",
       "IDN": "indonesia"}

# Today's (pre-2025) regions of Vietnam: en Wikipedia, "First-level subdivisions of Vietnam", oldid 1265924465 (Dec. 29,
# 2024), the table "Regions of Vietnam"; CGAZ's ADM1 names. Côn Đảo, a CGAZ unit of its own, is Bà Rịa–Vũng Tàu's.
REGIONS = {
    "Northwest": "Điện Biên|Hòa Bình|Lai Châu|Lào Cai|Sơn La|Yên Bái",
    "Northeast": "Bắc Giang|Bắc Kạn|Cao Bằng|Hà Giang|Lạng Sơn|Phú Thọ|Quảng Ninh|Thái Nguyên|Tuyên Quang",
    "Red River Delta": "Bắc Ninh|Hà Nam|Hà Nội|Hải Dương|Hải Phòng|Hưng Yên|Nam Định|Ninh Bình|Thái Bình|Vĩnh Phúc",
    "North Central Coast": "Hà Tĩnh|Nghệ An|Quảng Bình|Quảng Trị|Thanh Hóa|Thừa Thiên Huế",
    "South Central Coast": "Bình Định|Bình Thuận|Đà Nẵng|Khánh Hòa|Ninh Thuận|Phú Yên|Quảng Nam|Quảng Ngãi",
    "Central Highlands": "Đắk Lắk|Đắk Nông|Gia Lai|Kon Tum|Lâm Đồng",
    "Southeast": "Bà Rịa–Vũng Tàu|Bình Dương|Bình Phước|Đồng Nai|Ho Chi Minh|Tây Ninh|Côn Đảo",
    "Mekong Delta": "An Giang|Bến Tre|Bạc Liêu|Cà Mau|Cần Thơ|Đồng Tháp|Hậu Giang|Kiên Giang|Long An|Sóc Trăng|"
                    "Tiền Giang|Trà Vinh|Vĩnh Long",
}
REGION_OF = {p: r for r, ps in REGIONS.items() for p in ps.split("|")}
# CGAZ's ADM1 names as the series writes them (English names stay: CLAUDE.md)
ADM1_NAME = {"Hà Nội": "Hanoi", "Hải Phòng": "Haiphong", "Ho Chi Minh": "Hồ Chí Minh City", "Ratanakiri Province": "Ratanakiri",
             "Vientiane Capital": "Vientiane (prefecture)", "Thừa Thiên Huế": "Thừa Thiên Huế"}


def fold(s):
    s = unicodedata.normalize("NFD", s.replace("Đ", "D").replace("đ", "d"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower().replace(" ", "").replace("-", "")


def km2(g):
    return abs(GEOD.geometry_area_perimeter(g)[0]) / 1e6


def polys(g):
    """The polygons of a geometry, whatever it is."""
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
    """Cut the pieces to the country and give the country's uncovered slivers to a piece (step 2)."""
    gs = [multi(polys(shapely.intersection(p, country))) for p in pieces]
    rest = shapely.difference(country, shapely.union_all(gs))
    tree = shapely.STRtree(gs)
    extra = {}
    for s in polys(rest):
        if km2(s) < 1e-4:
            continue
        near = tree.query(s.buffer(1e-6), predicate="intersects")
        best, score = None, 0
        for j in near:
            ln = shapely.intersection(s.boundary, gs[j].buffer(1e-6)).length
            if ln > score:
                best, score = j, ln
        if best is None:
            best = int(tree.query_nearest(s)[0])
        extra.setdefault(best, []).append(s)
    for j, ss in extra.items():
        gs[j] = multi(polys(shapely.union_all([gs[j]] + ss)))
    return gs


def rnd(c):
    return [rnd(x) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], PREC), round(c[1], PREC)]


def feat(g, props):
    m = mapping(g)
    return {"type": "Feature", "properties": props, "geometry": {"type": m["type"], "coordinates": rnd(m["coordinates"])}}


def dump(path, feats):
    s = json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False, separators=(",", ":"))
    open(path, "w", encoding="utf-8").write(s + "\n")
    return len(s.encode())


def lines(geoms, minus=None):
    """The boundaries of dissolved polygons, each edge once, less `minus`, merged into runs."""
    b = shapely.union_all([g.boundary for g in geoms if not g.is_empty])
    if minus is not None and not minus.is_empty:
        b = shapely.difference(b, minus)
    b = shapely.line_merge(shapely.union_all([x for x in getattr(b, "geoms", [b]) if x.geom_type in ("LineString", "MultiLineString")]))
    return b


def label_point(g):
    big = max(polys(g), key=lambda p: p.area)
    return polylabel(big, tolerance=0.005)


def main():
    frame = box(*FRAME)
    a0 = {d["shapeGroup"]: multi(polys(shapely.intersection(d["g"], frame))) for d in read(0, "shapeType='ADM0'")}
    a1 = read(1, "shapeGroup IN ('VNM','LAO','KHM')")
    a2 = read(2, "shapeGroup='VNM'")
    # 2: the pieces
    pieces, props = [], []
    vn = fill(a0["VNM"], [d["g"] for d in a2])
    for d, g in zip(a2, vn):
        pieces.append(g)
        props.append({"c": "VNM", "adm2": d["shapeName"], "id2": d["shapeID"]})
    for c in ("LAO", "KHM"):
        ds = [d for d in a1 if d["shapeGroup"] == c]
        for d, g in zip(ds, fill(a0[c], [d["g"] for d in ds])):
            pieces.append(g)
            props.append({"c": c, "adm1": d["shapeName"], "id1": d["shapeID"]})
    for c, g in a0.items():
        if c not in ("VNM", "LAO", "KHM") and c in COUNTRY:
            pieces.append(g)
            props.append({"c": c})
    keep = [i for i, g in enumerate(pieces) if not g.is_empty]
    pieces, props = [pieces[i] for i in keep], [props[i] for i in keep]
    # 4: each district's modern province and 1966 unit, on the unsimplified pieces
    vn1 = [d for d in a1 if d["shapeGroup"] == "VNM"]
    t1 = shapely.STRtree([d["g"] for d in vn1])
    old = json.load(open(os.path.join(VN66, "provinces1966.geojson"), encoding="utf-8"))["features"]
    # a rerun keeps the first run's assignment (crosswalk-cgaz.yaml), made on the GADM-based polygons
    cwp = os.path.join(VN66, "crosswalk-cgaz.yaml")
    prior = {r["shapeID"]: r for r in yaml.safe_load(open(cwp, encoding="utf-8"))["districts"]} if os.path.exists(cwp) else {}
    oldg = [shapely.make_valid(shape(f["geometry"])) for f in old]
    t66 = shapely.STRtree(oldg)
    units66 = {f["properties"]["id"]: f["properties"] for f in old}
    rows = []
    for i, (g, p) in enumerate(zip(pieces, props)):
        if p["c"] != "VNM":
            continue
        area = g.area
        best = max(t1.query(g, predicate="intersects"), key=lambda j: shapely.intersection(g, vn1[j]["g"]).area, default=None)
        p["adm1"] = vn1[best]["shapeName"] if best is not None else ""
        share = {}
        for j in t66.query(g, predicate="intersects"):
            share[old[j]["properties"]["id"]] = shapely.intersection(g, oldg[j]).area / area
        u, s = max(share.items(), key=lambda kv: kv[1], default=(None, 0))
        p["u66"] = u if s >= 0.5 else None
        if p["id2"] in prior:
            r = prior[p["id2"]]
            p["u66"], s = (None if r["unit_1966"] == "DRV" else r["unit_1966"]), r["share"]
        p["share"] = round(s, 3)
        rows.append(dict(district=p["adm2"], shapeID=p["id2"], province_today=p["adm1"], unit_1966=p["u66"] or "DRV",
                         share=round(s, 3), km2=round(km2(g), 1)))
    # 3: one coverage, simplified once
    clean = shapely.coverage_clean(np.array(pieces, dtype=object), gap_width=0.0005)
    print("coverage valid after clean:", shapely.coverage_is_valid(clean))
    simp = shapely.coverage_simplify(clean, TOL)
    simp = [multi([q for q in polys(s) if km2(q) >= MIN_KM2]) for s in simp]
    # 5: units
    def unit_of(p):
        if p["c"] == "VNM":
            if p["u66"]:
                return "rvn", p["u66"]
            if p["adm1"] == "Quảng Trị":
                return "drv", "vinh-linh"
            return "drv", "drv-" + fold(p["adm1"])
        if p["c"] in ("LAO", "KHM"):
            return CID[p["c"]], CID[p["c"]] + "-" + fold(p["adm1"]).replace("province", "")
        return CID[p["c"]], None
    groups, meta = {}, {}
    for g, p in zip(simp, props):
        cty, uid = unit_of(p)
        p["cty"], p["uid"] = cty, uid
        if uid:
            groups.setdefault(uid, []).append(g)
            if uid not in meta:
                if cty == "rvn":
                    o = units66[uid]
                    meta[uid] = dict(name=o["name"], plain=o["plain"], c="rvn", kind=o["kind"], ctz=o.get("ctz"),
                                     region=o.get("region"), conf=o.get("confidence"), src="1966")
                elif uid == "vinh-linh":
                    meta[uid] = dict(name="Vĩnh Linh", plain="Vinh Linh", c="drv", kind="special zone",
                                     region="North Central Coast", src="1954–76",
                                     note="The special zone (đặc khu) north of the Bến Hải, 1954–76: today's Vĩnh Linh "
                                          "and Cồn Cỏ districts of Quảng Trị")
                else:
                    n = p["adm1"]
                    meta[uid] = dict(name=ADM1_NAME.get(n, n), plain=None, c=cty, kind="province",
                                     region=REGION_OF.get(n) if cty == "drv" else None, src="today")
    # regions of the RVN's units: the 1966 file's (by area of today's provinces); of the DRV's, the table's
    units = {uid: multi(polys(shapely.coverage_union_all(gs))) for uid, gs in groups.items()}
    country = {}
    for g, p in zip(simp, props):
        country.setdefault(p["cty"], []).append(g)
    country = {c: multi(polys(shapely.coverage_union_all(gs))) for c, gs in country.items()}
    land = shapely.union_all(list(country.values()))
    fb = frame.boundary
    coast = shapely.difference(land.boundary, fb.buffer(1e-7))
    # the lines, each at its highest rank
    dmz = shapely.line_merge(shapely.intersection(country["rvn"].boundary, country["drv"].boundary))
    intl = lines(list(country.values()), shapely.union_all([coast, dmz, fb.buffer(1e-7)]))
    top = shapely.union_all([coast, dmz, intl, fb.buffer(1e-7)])
    vnu = {uid: g for uid, g in units.items() if meta[uid]["c"] in ("rvn", "drv")}
    ctzg = {}
    for uid, g in units.items():
        if meta[uid]["c"] == "rvn":
            ctzg.setdefault(meta[uid]["ctz"] or "none", []).append(g)
    ctzg = {z: multi(polys(shapely.union_all(gs))) for z, gs in ctzg.items()}
    ctzl = lines(list(ctzg.values()), top)
    regg = {}
    for g, p in zip(simp, props):
        if p["c"] == "VNM":
            r = REGION_OF.get(p["adm1"])
            if not r:
                print("no region for", p["adm1"])
            regg.setdefault(r, []).append(g)
    regg = {r: multi(polys(shapely.coverage_union_all(gs))) for r, gs in regg.items()}
    regl = lines(list(regg.values()), top)
    unitl = lines(list(units.values()), top)
    # the RVN's units take the region of the 1966 file (by area); the regions' lines are today's provinces' groups
    feats = []
    names = {"rvn": "Republic of Vietnam", "drv": "Democratic Republic of Vietnam", **{CID[k]: v for k, v in COUNTRY.items() if k in CID}}
    for c, g in country.items():
        feats.append(feat(g, {"k": "land", "id": c, "name": names[c]}))
    for uid, g in sorted(units.items(), key=lambda kv: (meta[kv[0]]["c"], kv[0])):
        m = meta[uid]
        feats.append(feat(g, {"k": "unit", "id": uid, **{k: v for k, v in m.items() if v is not None},
                              "km2": round(km2(g))}))
    for cls, g in (("coast", coast), ("intl", intl), ("dmz", dmz), ("ctz", ctzl), ("region", regl), ("unit", unitl)):
        if not g.is_empty:
            feats.append(feat(g, {"k": "line", "l": cls}))
    for uid, g in units.items():
        m = meta[uid]
        feats.append(feat(label_point(g), {"k": "lab", "l": "unit", "c": m["c"], "name": m["name"], "km2": round(km2(g))}))
    znames = {"I": "I Corps", "II": "II Corps", "III": "III Corps", "IV": "IV Corps", "CMD": "Capital Military District"}
    for z, g in ctzg.items():
        if z in znames:
            feats.append(feat(label_point(g), {"k": "lab", "l": "ctz", "name": znames[z], "km2": round(km2(g))}))
    for r, g in regg.items():
        feats.append(feat(label_point(g), {"k": "lab", "l": "region", "name": r, "km2": round(km2(g))}))
    size = dump(os.path.join(OUT, "admin.geojson"), feats)
    print("admin.geojson", size, "bytes,", len(feats), "features")
    # the 1966 files, for the series' checks and the gazetteer
    pf = []
    for f in old:
        uid = f["properties"]["id"]
        if uid in units:
            pf.append(feat(units[uid], f["properties"]))
        else:
            print("1966 unit with no district now:", uid)
    dump(os.path.join(VN66, "provinces1966.geojson"), pf)
    cz = json.load(open(os.path.join(VN66, "ctz1966.geojson"), encoding="utf-8"))["features"]
    dump(os.path.join(VN66, "ctz1966.geojson"), [feat(ctzg[f["properties"]["ctz"]], f["properties"]) for f in cz
                                                  if f["properties"]["ctz"] in ctzg])
    rf = []
    for r in ("North Central Coast", "South Central Coast", "Central Highlands", "Southeast", "Mekong Delta"):
        g = multi(polys(shapely.union_all([units[u] for u in units if meta[u]["c"] == "rvn" and meta[u]["region"] == r])))
        rf.append(feat(g, {"region": r, "note": "RVN territory (south of the Bến Hải) by the region of its 1966 units"}))
    dump(os.path.join(VN66, "regions.geojson"), rf)
    of = [feat(country["rvn"], {"name": "Republic of Vietnam", "kind": "rvn", "note": "union of provinces1966 (geoBoundaries CGAZ districts)"}),
          feat(country["drv"], {"name": "Democratic Republic of Vietnam", "kind": "drv", "note": "geoBoundaries CGAZ"})]
    for c in ("laos", "cambodia", "thailand"):
        of.append(feat(country[c], {"name": names[c], "kind": "neighbor", "note": "geoBoundaries CGAZ (LSIB)"}))
    dump(os.path.join(VN66, "outline.geojson"), of)
    dump(os.path.join(VN66, "indochina-outline.geojson"),
         [feat(country[c], {"id": c, "name": names[c]}) for c in ("china", "drv", "cambodia", "laos", "thailand", "burma")])
    # the crosswalk to CGAZ
    unsure = [r for r in rows if r["share"] < SURE]
    cw = {"title": "The 1966 units on geoBoundaries CGAZ districts (tools/vnmap/base.py)",
          "method": "each CGAZ ADM2 district of Vietnam given whole to the 1966 unit of the GADM-based provinces1966.geojson "
                    "(the hand crosswalk, crosswalk.yaml) holding most of it; under half in any: the DRV",
          "source": "geoBoundaries CGAZ 6.0.0, ADM0-2 (CC BY 4.0), downloaded Oct. 22, 2026",
          "straddlers": sorted(unsure, key=lambda r: r["share"]),
          "districts": sorted(rows, key=lambda r: (r["unit_1966"], r["district"]))}
    yaml.safe_dump(cw, open(os.path.join(VN66, "crosswalk-cgaz.yaml"), "w", encoding="utf-8"), allow_unicode=True,
                   sort_keys=False, width=140)
    print(len(rows), "districts;", len(unsure), "under", SURE)
    # the gazetteer's provinces by point in polygon
    pl = json.load(open(os.path.join(VN66, "places.json"), encoding="utf-8"))
    tree = shapely.STRtree([units[u] for u in units if meta[u]["c"] == "rvn"])
    ids = [u for u in units if meta[u]["c"] == "rvn"]
    changed = []
    for p in pl:
        if p.get("lat") is None or not p.get("province"):      # only the places in the RVN's units
            continue
        pt = shapely.Point(p["lon"], p["lat"])
        hit = [ids[j] for j in tree.query(pt, predicate="intersects")]
        if not hit:
            j = tree.query_nearest(pt)[0]
            hit = [ids[j]] if shapely.distance(pt, units[ids[j]]) < 0.05 else []
        new = hit[0] if hit else p.get("province")
        if p.get("province") and new != p["province"]:
            changed.append((p["id"], p["province"], new))
            p["province"] = new
    if changed:
        json.dump(pl, open(os.path.join(VN66, "places.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("gazetteer provinces changed:", changed)


if __name__ == "__main__":
    main()
