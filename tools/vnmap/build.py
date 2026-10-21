"""Build the 1966 RVN map data (one-time, Oct. 21, 2026; sources/vn-provinces-1966/README.md).  python3 -I build.py VNMAP_DIR
Reads dl/gadm/gadm41_VNM_2.json and dl/ne/ne_10m_admin_0_countries.geojson; writes crosswalk.yaml,
provinces1966.geojson, ctz1966.geojson, regions.geojson, outline.geojson and build/areas.json (for validate)."""
import json, os, sys
import shapely
from shapely.geometry import shape, mapping, box, Polygon, MultiPolygon
from pyproj import Geod
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xw import UNITS, REGION, DROP, districts

ROOT = sys.argv[1]
GEOD = Geod(ellps="WGS84")
TOL = 0.0025         # coverage_simplify tolerance (degrees, ~250 m)
MIN_PART_KM2 = 1.0   # drop island parts smaller than this
ROUND = 1e-4


def km2(g):
    return abs(GEOD.geometry_area_perimeter(g)[0]) / 1e6


def parts(g):
    return list(g.geoms) if hasattr(g, "geoms") else [g]


def drop_small(g, keep_min=MIN_PART_KM2):
    ps = [p for p in parts(g) if p.geom_type == "Polygon" and km2(p) >= keep_min]
    if not ps:  # keep the largest at least
        ps = [max(parts(g), key=lambda p: p.area)]
    return MultiPolygon(ps) if len(ps) > 1 else ps[0]


def tidy(g):
    g = shapely.set_precision(g, ROUND)
    g = shapely.make_valid(g)
    ps = [p for p in parts(g) if p.geom_type == "Polygon" and not p.is_empty]
    if hasattr(g, "geoms"):
        ps = []
        for q in g.geoms:
            if q.geom_type == "Polygon":
                ps.append(q)
            elif q.geom_type == "MultiPolygon":
                ps += list(q.geoms)
    return MultiPolygon(ps) if len(ps) > 1 else ps[0]


def feat(g, props):
    return {"type": "Feature", "properties": props, "geometry": mapping(g)}


def dump(path, feats):
    fc = {"type": "FeatureCollection", "features": feats}
    s = json.dumps(fc, ensure_ascii=False, separators=(",", ":"))
    open(path, "w").write(s)
    return len(s.encode())


def main():
    g = json.load(open(os.path.join(ROOT, "dl/gadm/gadm41_VNM_2.json")))
    by = {}
    for f in g["features"]:
        p = f["properties"]
        by[(p["NAME_1"], p["NAME_2"])] = f
    south = [k for k in by if k[0] in REGION and k[0] != "QuảngBình"]
    drop = {tuple(x.split("/")) for x in DROP}
    # assignment
    owner, problems = {}, []
    for un in UNITS:
        for k in districts(un):
            if k not in by:
                problems.append(f"unknown district {k} in {un['id']}")
            elif k in owner:
                problems.append(f"district {k} in both {owner[k]} and {un['id']}")
            else:
                owner[k] = un["id"]
    unassigned = [k for k in south if k not in owner and k not in drop]
    os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
    keys = [k for k in south if k in owner]
    raw = [shape(by[k]["geometry"]) for k in keys]
    clean = shapely.coverage_clean(raw, gap_width=0.002)
    simp = shapely.coverage_simplify(clean, TOL)
    # Côn Sơn from Natural Earth
    ne = json.load(open(os.path.join(ROOT, "dl/ne/ne_10m_admin_0_countries.geojson")))
    nef = {f["properties"]["ADMIN"]: shape(f["geometry"]) for f in ne["features"]
           if f["properties"]["ADMIN"] in ("Vietnam", "Laos", "Cambodia", "Thailand")}
    conson = [p for p in parts(nef["Vietnam"]) if box(106.4, 8.5, 106.8, 8.9).contains(p.representative_point())]
    conson = MultiPolygon(conson) if len(conson) > 1 else conson[0]

    units = {u_["id"]: u_ for u_ in UNITS}
    raw_by, simp_by, reg_simp, ctz_simp = {}, {}, {}, {}
    for k, r, c, s in zip(keys, raw, clean, simp):
        uid = owner[k]
        raw_by.setdefault(uid, []).append(c)
        simp_by.setdefault(uid, []).append(s)
        reg_simp.setdefault(REGION[k[0]], []).append(s)
    raw_by["con-son"] = [conson]
    simp_by["con-son"] = [shapely.simplify(conson, TOL / 2, preserve_topology=True)]
    reg_simp.setdefault("Southeast", []).append(simp_by["con-son"][0])  # Côn Đảo: Bà Rịa–Vũng Tàu, pre-2025

    areas, region_of, feats = {}, {}, []
    for un in UNITS:
        uid = un["id"]
        rawu = shapely.union_all(raw_by[uid])
        areas[uid] = round(km2(rawu))
        # region by area of modern provinces
        ra = {}
        for k in districts(un):
            ra[REGION[k[0]]] = ra.get(REGION[k[0]], 0) + km2(shape(by[k]["geometry"]))
        region_of[uid] = max(ra, key=ra.get) if ra else "Southeast"
        un["_region_split"] = {r: round(a) for r, a in sorted(ra.items(), key=lambda x: -x[1])}
        geom = tidy(drop_small(shapely.coverage_union_all(simp_by[uid]) if uid != "con-son" else simp_by[uid][0]))
        feats.append(feat(geom, dict(id=uid, name=un["name"], plain=un["plain"], kind=un["kind"], capital=un["capital"],
                                     ctz=un["ctz"], region=region_of[uid], confidence=un["conf"])))
        ctz_simp.setdefault(un["ctz"] or "none", []).append(shapely.coverage_union_all(simp_by[uid]) if uid != "con-son" else simp_by[uid][0])
    sizes = {}
    sizes["provinces1966.geojson"] = dump(os.path.join(ROOT, "provinces1966.geojson"), feats)
    names = {"I": "I Corps Tactical Zone", "II": "II Corps Tactical Zone", "III": "III Corps Tactical Zone",
             "IV": "IV Corps Tactical Zone", "CMD": "Capital Military District", "none": "Côn Sơn (Navy; no corps zone)"}
    cf = []
    for z in ["I", "II", "III", "IV", "CMD", "none"]:
        gz = tidy(drop_small(shapely.union_all(ctz_simp[z])))
        cf.append(feat(gz, dict(ctz=z, name=names[z], provinces=[un["id"] for un in UNITS if (un["ctz"] or "none") == z])))
    sizes["ctz1966.geojson"] = dump(os.path.join(ROOT, "ctz1966.geojson"), cf)
    rf = []
    for r in ["North Central Coast", "South Central Coast", "Central Highlands", "Southeast", "Mekong Delta"]:
        gr = tidy(drop_small(shapely.union_all(reg_simp[r])))
        rf.append(feat(gr, dict(region=r, note="RVN territory (south of the Bến Hải) by today's pre-2025 region of the modern province")))
    sizes["regions.geojson"] = dump(os.path.join(ROOT, "regions.geojson"), rf)
    # outline
    rvn = tidy(drop_small(shapely.union_all([f for v in ctz_simp.values() for f in v])))
    drv_keys = [k for k in by if k[0] == "QuảngBình"] + [tuple(x.split("/")) for x in DROP]
    drv = shapely.union_all(shapely.coverage_clean([shape(by[k]["geometry"]) for k in drv_keys], gap_width=0.002))
    drv = tidy(drop_small(shapely.simplify(drv, TOL, preserve_topology=True)))
    clip = box(102, 8, 110, 18)
    of = [feat(rvn, dict(name="Republic of Vietnam", kind="rvn", note="union of provinces1966 (GADM 4.1 districts; Côn Sơn from Natural Earth)")),
          feat(drv, dict(name="Democratic Republic of Vietnam: Quảng Bình and Vĩnh Linh", kind="drv", note="GADM 4.1; Vĩnh Linh with Cồn Cỏ"))]
    for c in ("Laos", "Cambodia", "Thailand"):
        gc = shapely.intersection(nef[c], clip)
        if gc.is_empty:
            continue
        gc = tidy(drop_small(shapely.simplify(gc, TOL * 2, preserve_topology=True), 5))
        of.append(feat(gc, dict(name=c, kind="neighbor", note="Natural Earth 10m admin-0, clipped to lon 102–110, lat 8–18")))
    sizes["outline.geojson"] = dump(os.path.join(ROOT, "outline.geojson"), of)
    # raw (unsimplified) units for point-in-polygon
    rawf = [feat(shapely.union_all(raw_by[un["id"]]), dict(id=un["id"])) for un in UNITS]
    dump(os.path.join(ROOT, "build/units_raw.geojson"), rawf)
    # crosswalk.yaml
    gid = {k: by[k]["properties"]["GID_2"] for k in by}
    cw = []
    for un in UNITS:
        e = dict(id=un["id"], name=un["name"], plain=un["plain"], kind=un["kind"], capital_1966=un["capital"],
                 ctz_1966=un["ctz"])
        if un.get("ctz_note"):
            e["ctz_note"] = un["ctz_note"]
        e["region"] = region_of[un["id"]]
        if len(un["_region_split"]) > 1:
            e["region_split_km2"] = un["_region_split"]
        e["area_km2_gadm"] = areas[un["id"]]
        e["districts"] = [dict(gid=gid[k], name_2=k[1], name_1=k[0]) for k in districts(un)]
        e["confidence"] = un["conf"]
        e["note"] = un["note"]
        e["sources"] = un["src"]
        cw.append(e)
    head = {
        "title": "Republic of Vietnam provinces, late 1966, approximated by GADM 4.1 level-2 districts",
        "date": "late 1966 (after Sa Đéc's re-creation, 24 Sept. 1966; before Trà Ôn and Vũng Liêm moved to Vĩnh Long, 14 Jan. 1967)",
        "method": "each modern district (GADM 4.1, pre-2025) assigned whole to the 1966 unit holding most of it; Vĩnh Linh and Cồn Cỏ "
                  "(north of the Bến Hải) dropped; Côn Sơn from Natural Earth (GADM lacks Côn Đảo)",
        "counts": {"provinces": sum(1 for un in UNITS if un["kind"] == "province"),
                   "autonomous_cities": [un["name"] for un in UNITS if un["kind"] == "city"],
                   "special": ["Côn Sơn (administrative base, Interior Ministry)"]},
        "general_sources": ["https://vi.wikipedia.org/wiki/T%E1%BB%89nh_(Vi%E1%BB%87t_Nam_C%E1%BB%99ng_h%C3%B2a)",
                            "https://en.wikipedia.org/wiki/First-level_subdivisions_of_Vietnam",
                            "https://en.wikipedia.org/wiki/I_Corps_(South_Vietnam)", "https://en.wikipedia.org/wiki/II_Corps_(South_Vietnam)",
                            "https://en.wikipedia.org/wiki/III_Corps_(South_Vietnam)", "https://en.wikipedia.org/wiki/IV_Corps_(South_Vietnam)",
                            "https://vi.wikipedia.org/wiki/Bi%E1%BB%87t_khu_Th%E1%BB%A7_%C4%91%C3%B4"],
        "note_sources": "No en Wikipedia article 'Provinces of South Vietnam' exists (Oct. 2026); the vi list 'Tỉnh (Việt Nam Cộng hòa)' "
                        "serves. Areas 'against N (year)' in notes compare the GADM area with the figure the articles print.",
        "later_changes_to_1975": [
            "14 Jan. 1967: Trà Ôn and Vũng Liêm from Vĩnh Bình to Vĩnh Long.",
            "7 Sept. 1967: Tuyên Đức's capital moved from Đà Lạt to Tùng Nghĩa.",
            "1967–68 (date not found): Bình Tuy back in III CTZ.",
            "1970: Gia Định takes Cần Giờ and Quảng Xuyên from Biên Hòa; Gia Định joins MR 3 (1 July 1970, CTZs renamed Military Regions).",
            "By 1974: autonomous towns added: Cần Thơ, Mỹ Tho, Nha Trang, Qui Nhơn, Rạch Giá; special zone Phú Quốc (vi W list of 1974).",
            "1 Nov. 1974: Côn Sơn becomes Phú Hải town of Gia Định.",
        ],
        "units": cw,
    }
    yaml.safe_dump(head, open(os.path.join(ROOT, "crosswalk.yaml"), "w"), allow_unicode=True, sort_keys=False, width=140)
    json.dump(dict(areas=areas, unassigned=[list(k) for k in unassigned], problems=problems, sizes=sizes,
                   region=region_of), open(os.path.join(ROOT, "build/areas.json"), "w"), ensure_ascii=False, indent=1)
    print("problems", problems)
    print("unassigned", unassigned)
    print("sizes", sizes)


main()
