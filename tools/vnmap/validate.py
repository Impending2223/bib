"""validate.md: python3 -I validate.py VNMAP_DIR"""
import json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xw import UNITS, REGION, districts

ROOT = sys.argv[1]
A = json.load(open(os.path.join(ROOT, "build/areas.json")))
PL = json.load(open(os.path.join(ROOT, "build/places_check.json")))
U = {u["id"]: u for u in UNITS}


def fold(s):
    s = unicodedata.normalize("NFD", (s or "").replace("Đ", "D").replace("đ", "d"))
    return re.sub(r"[^a-z]", "", "".join(c for c in s if unicodedata.category(c) != "Mn").lower())


# --- areas the sources print (km²): VI_TINH's 1964 table unless marked
REF = {
    "quang-tri": (4741, "1964"), "thua-thien": (4924, "1964"), "hue": (15, "1964"), "da-nang": (60, "1964"),
    "quang-nam": (6777, "1964"), "quang-tin": (4903, "1964"), "quang-ngai": (6981, "1964"), "kon-tum": (9112, "1964"),
    "pleiku": (8260, "1971, vi W 'Pleiku (tỉnh)'"), "phu-bon": (4822, "1971, vi W 'Phú Bổn'"), "binh-dinh": (9537, "1964"),
    "phu-yen": (5233, "1964"), "darlac": (10552, "1964"), "quang-duc": (5958, "1971, vi W 'Quảng Đức (tỉnh)'"),
    "khanh-hoa": (5985, "1964, Cam Ranh included"), "ninh-thuan": (3546, "1964"), "tuyen-duc": (4704, "vi W 'Tuyên Đức', Đà Lạt included"),
    "da-lat": (69, "1964"), "lam-dong": (4739, "1964"), "binh-thuan": (4277, "1964"), "binh-tuy": (3560, "1971, vi W 'Bình Tuy'"),
    "phuoc-long": (4604, "1964, before Phước Thành's end"), "binh-long": (2334, "1964"), "tay-ninh": (3845, "1964"),
    "hau-nghia": (1300, "1964"), "binh-duong": (1599, "1964, before Phú Giáo joined"), "bien-hoa": (2352, "1964, before Tân Uyên returned"),
    "long-khanh": (3457, "1967, vi W 'Long Khánh (tỉnh)'"), "phuoc-tuy": (1927, "1966, vi W 'Phước Tuy'"), "vung-tau": (74, "1964"),
    "long-an": (1382, "1964"), "gia-dinh": (824, "1964"), "saigon": (58, "1964"), "kien-tuong": (2297, "1964"),
    "dinh-tuong": (1640, "1967, vi W 'Định Tường'"), "go-cong": (570, "1970, vi W 'Gò Công (tỉnh)'"), "kien-hoa": (2085, "1970, vi W 'Kiến Hòa'"),
    "kien-phong": (2657, "vi W 'Kiến Phong'"), "sa-dec": (789, "vi W 'Sa Đéc (tỉnh)'"), "vinh-long": (1111, "1964 (1,900) less Sa Đéc (789)"),
    "vinh-binh": (2880, "1964"), "chau-doc": (2151, "1964"), "an-giang": (1826, "1964"), "kien-giang": (5403, "1964"),
    "chuong-thien": (2292, "1971, vi W 'Chương Thiện'"), "phong-dinh": (1623, "1964"), "ba-xuyen": (2684, "1964"),
    "bac-lieu": (2632, "1964"), "an-xuyen": (4952, "1964"), "con-son": (64, "1964"),
}

# --- corps zones by a second source
#   S1: vi W 'Việt Nam Cộng hòa', the Vùng lists (undated; Sa Đéc and Bạc Liêu present, so after Sept. 1966; before 1 July 1970)
#   S2: vi W 'Quân đoàn I/II/III/IV': division areas at Mậu Thân 1968
#   S3: en W corps articles: the reassignments of Sept. 1964
S1 = {"I": "quang-tri thua-thien quang-tin quang-ngai quang-nam da-nang",
      "II": "binh-dinh phu-yen phu-bon darlac khanh-hoa ninh-thuan binh-thuan tuyen-duc quang-duc lam-dong cam-ranh kon-tum pleiku",
      "III": "tay-ninh hau-nghia long-an phuoc-long binh-long binh-duong binh-tuy phuoc-tuy long-khanh bien-hoa vung-tau",
      "IV": "kien-tuong dinh-tuong go-cong kien-hoa kien-phong chau-doc vinh-long vinh-binh an-giang kien-giang sa-dec phong-dinh chuong-thien ba-xuyen bac-lieu an-xuyen"}
S2 = {"I": "thua-thien quang-nam da-nang quang-tin quang-ngai quang-tri",
      "II": "kon-tum pleiku phu-bon binh-dinh phu-yen darlac quang-duc tuyen-duc lam-dong khanh-hoa binh-thuan ninh-thuan cam-ranh",
      "III": "binh-duong binh-long phuoc-long bien-hoa binh-tuy gia-dinh long-khanh phuoc-tuy vung-tau hau-nghia long-an tay-ninh",
      "IV": "dinh-tuong go-cong kien-hoa kien-tuong sa-dec an-giang chau-doc kien-phong vinh-binh vinh-long an-xuyen ba-xuyen bac-lieu chuong-thien kien-giang phong-dinh"}


def zone_of(src, uid):
    for z, ids in src.items():
        if uid in ids.split():
            return z
    return None


# --- what a province name in an article can mean: the 1966 unit, the pre-2025 province, the 2025 province
M2025 = {"GiaLai": ["GiaLai", "BìnhĐịnh"], "LâmĐồng": ["LâmĐồng", "ĐắkNông", "BìnhThuận"], "ĐắkLắk": ["ĐắkLắk", "PhúYên"],
         "KhánhHòa": ["KhánhHòa", "NinhThuận"], "QuảngNgãi": ["QuảngNgãi", "KonTum"], "ĐàNẵng": ["ĐàNẵng", "QuảngNam"],
         "QuảngTrị": ["QuảngTrị", "QuảngBình"], "HồChíMinh": ["HồChíMinh", "BìnhDương", "BàRịa-VũngTàu"],
         "ĐồngNai": ["ĐồngNai", "BìnhPhước"], "TâyNinh": ["TâyNinh", "LongAn"], "ĐồngTháp": ["ĐồngTháp", "TiềnGiang"],
         "VĩnhLong": ["VĩnhLong", "BếnTre", "TràVinh"], "AnGiang": ["AnGiang", "KiênGiang"],
         "CầnThơ": ["CầnThơ", "HậuGiang", "SócTrăng"], "CàMau": ["CàMau", "BạcLiêu"]}
modern_units = {}
for un in UNITS:
    for p1, _ in districts(un):
        modern_units.setdefault(p1, set()).add(un["id"])
modern_units.setdefault("BàRịa-VũngTàu", set()).add("con-son")
names1966 = {}
for un in UNITS:
    for n in (un["name"], un["plain"]):
        names1966.setdefault(fold(n), set()).add(un["id"])
names1966.setdefault("thuathien", set()).add("hue")
names1966.setdefault("kontum", set()).add("kon-tum")


def meanings(name):
    f = fold(re.sub(r"^Vietnam's\s+", "", name or ""))
    strong = names1966.get(f, set())
    weak = set()
    for p1, ids in modern_units.items():
        if fold(p1) == f:
            weak |= ids
    for p25, olds in M2025.items():
        if fold(p25) == f:
            for o in olds:
                weak |= modern_units.get(o, set())
    if f == "huế" or f == "hue" or f == "thuathienhue":
        weak |= {"hue", "thua-thien"}
    return strong, weak


def main():
    L = []
    w = L.append
    w("# Validation of the 1966 RVN map data\n")
    w("Generated by `src/validate.py`. Sources are Wikipedia (en, vi) as fetched 21 Oct. 2026 (`dl/wiki/`); areas are GADM 4.1 "
      "geodesic areas of the unsimplified districts.\n")
    # districts
    w("## 1. Districts assigned to no unit, or to two\n")
    w(f"- Assigned to two units: {len(A['problems'])} {A['problems'] or ''}")
    w(f"- South of the Bến Hải and assigned to none: {len(A['unassigned'])} {A['unassigned'] or ''}")
    w("- Dropped as north of the Bến Hải: Quảng Trị/Vĩnh Linh, Quảng Trị/Cồn Cỏ. Not in GADM 4.1: Côn Đảo (taken from Natural Earth), "
      "Hoàng Sa and Trường Sa (left out as asked).")
    w("- Districts that straddle a 1966 line (assigned whole to the larger part, by the sources' statements or by area):")
    for un in UNITS:
        if any(k in un["note"] for k in ("straddle", "part of", "part went", "partly", "south of Thuần Mẫn", "holds the south")):
            w(f"  - **{un['name']}** ({un['conf']}): {un['note']}")
    w("")
    # places
    w("## 2. Places: the computed 1966 unit against the province the article names\n")
    w("The article's province is the first 'X province' its text names (a crude reading: it often gives today's, or post-2025, "
      "province). Verdict: **agrees** (the 1966 unit of that name), **consistent** (the modern or 2025 province of that name "
      "contains the computed unit), **disagrees**, or **none named**.\n")
    w("| place | lat, lon | computed 1966 | point | article names | verdict |")
    w("|---|---|---|---|---|---|")
    dis = []
    for e in PL:
        ap = e.get("_article_province")
        s, wk = meanings(ap)
        prov = e["province"]
        if not ap:
            v = "none named"
        elif prov in s:
            v = "agrees"
        elif prov in wk:
            v = "consistent"
        else:
            v = "**disagrees**"
            dis.append(e)
        w(f"| {e['name']} | {e['lat']}, {e['lon']} | {prov} | {e['_pip']} | {ap or '—'} | {v} |")
    w("")
    w("Disagreements, read one by one:\n")
    reasons = {
        "Sài Gòn": "the article's first province mention is Gia Định, the province around the city; the point (city hall area) is in District 1: no boundary error.",
        "Đà Nẵng": "the article names Quảng Nam as the province the city once belonged to; the point is in Hải Châu: no boundary error.",
        "Kon Tum": "the article names Quảng Ngãi, the 2025 province that absorbed Kon Tum; counted 'consistent' only if the 2025 table applies. No boundary error.",
        "Bến Tre (Trúc Giang)": "the parse caught 'Đồ Chiểu' (a person's name before 'province'), not a province: no check.",
        "Cần Thơ": "the article names Hậu Giang, the former province of the city: no boundary error.",
        "Phan Thiết": "the article names Lâm Đồng, the 2025 province that absorbed Bình Thuận: no boundary error.",
    }
    for e in dis:
        w(f"- {e['name']}: computed {e['province']}, article '{e['_article_province']}'. {reasons.get(e['name'], 'Check.')}")
    w("")
    w("Points near a line (by the sources, not the parse): Hải Vân Pass (16.2, 108.133) falls in Thừa Thiên, on the Thừa Thiên–Quảng Nam "
      "line at the pass; the Bến Hải point is the river mouth, on the demarcation line, and falls in Gio Linh (Quảng Trị); Côn Sơn and "
      "Qui Nhơn points lie just off the simplified coast and take the nearest unit. Khâm Đức falls in Quảng Tín, as its article says "
      "('Quảng Tín'). The Iron Triangle point is Bến Cát's (the article has no coordinates).\n")
    # areas
    w("## 3. Areas: GADM against the areas the sources print\n")
    w("Ratio = GADM / printed. Printed areas from vi W 'Tỉnh (Việt Nam Cộng hòa)', its 1964 table, unless the year says otherwise. "
      "The RVN's own figures for the highland provinces are rough; a ratio far from 1 there says little.\n")
    w("| unit | GADM km² | printed km² | source | ratio |")
    w("|---|---|---|---|---|")
    off = []
    for un in UNITS:
        a = A["areas"][un["id"]]
        if un["id"] not in REF:
            w(f"| {un['name']} | {a:,} | — | none found | — |")
            continue
        ref, yr = REF[un["id"]]
        r = a / ref
        flag = " **" if abs(r - 1) > 0.15 else ""
        if flag:
            off.append((un["id"], r))
        w(f"| {un['name']} | {a:,} | {ref:,} | {yr} | {r:.2f}{flag} |")
    w("")
    w("Units off by more than 15 percent, and why:\n")
    why = {
        "quang-tri": "GADM's Quảng Trị south of the Bến Hải is 750 km² smaller than the printed 1964 figure; no district is missing (Hướng Hóa and Đa Krông in). The printed figure may count the DMZ's north half or old estimates. Check against the 1967 Quảng Trị map (vi W gallery: 'Bản đồ tỉnh Quảng Trị 1967.png').",
        "hue": "the modern city (71 km²) is larger than the 1964 city (15 km²): the 1966 city drawn too large, at Thừa Thiên's expense.",
        "da-nang": "the three inner districts (91 km²) stand for a 60 km² city.",
        "quang-ngai": "GADM 5,164 against 6,981 printed: either the 1964 figure is high or the 1966 province reached into today's Kon Tum (Kon Plông). Check.",
        "darlac": "Darlac drawn larger than printed: Ea H'leo (1,335 km²) may belong largely to Phú Bổn's Thuần Mẫn (Phú Bổn is short by about as much); the vi article puts only the south of Thuần Mẫn in today's Đắk Lắk. Low-confidence line.",
        "phu-bon": "short by ~1,540 km², about Ea H'leo's area: see Darlac.",
        "phuoc-long": "drawn with Cát Tiên and Đồng Phú; the 1964 figure predates Phước Thành's dissolution (1965), whose pieces went partly here.",
        "binh-long": "the vi article gives Bình Long parts of today's Dầu Tiếng, Bàu Bàng and Phú Giáo, left with Bình Dương.",
        "binh-duong": "the 1964 figure predates Phú Giáo's transfer from Phước Thành (1965).",
        "bien-hoa": "the 1964 figure predates Tân Uyên's return (1965); Vĩnh Cửu (1,092 km²) and Trảng Bom straddle Long Khánh.",
        "hau-nghia": "GADM 1,628 against 1,300: Đức Huệ and Trảng Bàng may have been smaller then. Check.",
        "vung-tau": "the modern city includes Long Sơn island and more.",
        "da-lat": "the modern city (394 km²) is far larger than the 1964 city (69 km²).",
        "go-cong": "Tân Phú Đông (222 km² of islands) may have been partly Kiến Hòa's or Định Tường's.",
        "phong-dinh": "Phụng Hiệp straddles Chương Thiện (its western communes); Ô Môn/Cờ Đỏ lines not checked.",
        "chuong-thien": "short of 2,292 (1971) by the parts of Phụng Hiệp and U Minh Thượng left out.",
        "binh-dinh": "with An Túc (An Khê, Đak Pơ, Kbang, Kông Chro) per vi W 'Pleiku (tỉnh)'.",
        "cam-ranh": "no printed area found.",
        "con-son": "Natural Earth's islands at 10m scale.",
    }
    for uid, r in off:
        w(f"- {U[uid]['name']} ({r:.2f}): {why.get(uid, 'Check.')}")
    w("")
    # corps
    w("## 4. Corps zones against second sources\n")
    w("- S1: vi W 'Việt Nam Cộng hòa', the Vùng lists (undated; they include Sa Đéc, so after 24 Sept. 1966, and predate 1 July 1970). "
      "https://vi.wikipedia.org/wiki/Vi%E1%BB%87t_Nam_C%E1%BB%99ng_h%C3%B2a")
    w("- S2: vi W 'Quân đoàn I/II/III/IV (Việt Nam Cộng hòa)', the division areas at Mậu Thân (1968).")
    w("- S3: en W 'I Corps', 'II Corps', 'III Corps', 'IV Corps (South Vietnam)': Quảng Ngãi II→I (Sept. 1964); Lâm Đồng, Bình Thuận, "
      "Bình Tuy III→II (Sept. 1964); Long An to III and four Tiền Giang provinces to IV (5 Sept. 1964); '11 provinces' in II Corps in summer 1964.")
    w("- Not reached: the U.S. Army's Vietnam Studies and MACV command histories (not fetched).\n")
    w("| unit | ctz (data) | S1 | S2 | note |")
    w("|---|---|---|---|---|")
    for un in UNITS:
        z = un["ctz"] or "—"
        s1, s2 = zone_of(S1, un["id"]) or "—", zone_of(S2, un["id"]) or "—"
        flag = ""
        if (s1 != "—" and s1 != z) or (s2 != "—" and s2 != z):
            flag = "differs"
        w(f"| {un['name']} | {z} | {s1} | {s2} | {flag} {un.get('ctz_note', '') if flag else ''} |")
    w("")
    w("Differences: Bình Tuy (II in the data for late 1966; III in S1 and S2, both later: see its note); Gia Định (CMD in the data; "
      "S2 lists it under III's 18th Division, and MACV counted it in III CTZ; S1 omits it, the CMD being its own command). Côn Sơn "
      "is in no zone. Count: I 5 provinces + Huế, Đà Nẵng; II 13 (with Bình Tuy) + Cam Ranh, Đà Lạt; III 9 + Vũng Tàu; CMD Gia Định + "
      "Saigon; IV 16: 44 provinces.\n")
    # better map
    w("## 5. What a better map would need\n")
    w("Contemporary maps to georeference (checked from here, 21 Oct. 2026):\n")
    w("- Perry-Castañeda Library, Vietnam page: https://maps.lib.utexas.edu/maps/vietnam.html (open).")
    w("  - AMS Series **L7014 is 1:50,000**, not 1:250,000: https://maps.lib.utexas.edu/maps/topo/vietnam/ (open; ~550 sheet PDFs, e.g. "
      "an_loc-6332-3.pdf; index vietnam_index.html). District and province lines are printed on the sheets.")
    w("  - AMS **Series L509, 1:250,000** (Indochina and Thailand): https://maps.lib.utexas.edu/maps/ams/indochina_and_thailand/ "
      "(open; clickable index index_map.html; sheets as txu-oclc-6535632-<sheet>.jpg).")
    w("  - JOG 1:250,000 (Vietnam, Laos, Cambodia): https://maps.lib.utexas.edu/maps/jog/vietnam/ (open).")
    w("  - CIA, *Indochina Atlas* (1970), 'Indochina Administrative Divisions': "
      "http://maps.lib.utexas.edu/maps/indochina_atlas/txu-oclc-1092889-78343-8-70.jpg (open; provinces as of 1970).")
    w("  - CIA, 'Vietnam [South] – Population' (1972), with province lines: "
      "https://maps.lib.utexas.edu/maps/middle_east_and_asia/south_vietnam_pop_1972.jpg (open).")
    w("  - City plans of 1961–69 (Huế, Đà Nẵng, Saigon, Biên Hòa, Vĩnh Long 1966, Quảng Ngãi 1966), same page.")
    w("- Wikimedia Commons, 'Southvietmap.jpg' (administrative map of the RVN, 1967; used in the province articles): "
      "https://commons.wikimedia.org/wiki/File:Southvietmap.jpg (not fetched), and the province maps of 1967–75 in vi W's gallery "
      "('Tỉnh (Việt Nam Cộng hòa)': Quảng Trị 1967, Quảng Tín 1973, Quảng Đức 1973, Phú Bổn, Kiến Tường, Chương Thiện …).\n")
    w("Hamlet coordinates with 1960s province codes, to test the lines hamlet by hamlet:\n")
    w("- NARA, Hamlet Evaluation System files (RG 472, MACV; in the Access to Archival Databases): https://aad.archives.gov/ "
      "answers **403** from here; https://catalog.archives.gov/ answers (200, a script-driven catalogue). The HES files give "
      "hamlet UTM grid references and GVN province/district codes; download needs a browser.")
    w("- Dell and Querubin, 'Nation Building Through Foreign Intervention' (QJE 2018), replication data on the Harvard Dataverse: "
      "https://dataverse.harvard.edu/ answers **202 with an AWS WAF challenge** (bot-checked); not tried further. "
      "scholar.harvard.edu/dell and openicpsr.org answer **403**.")
    w("- With HES points, each modern district's share of each 1966 province's hamlets would replace the area judgments above "
      "(Ea H'leo, Vĩnh Cửu, Trảng Bom, Phụng Hiệp, Tân Phước, Tân Phú Đông, Mang Thít, U Minh Thượng, Cát Tiên, Quế Sơn/Nông Sơn).\n")
    open(os.path.join(ROOT, "validate.md"), "w").write("\n".join(L) + "\n")
    print("disagreements", [(e["name"], e["province"], e["_article_province"]) for e in dis])
    print("area outliers", [(u, round(r, 2)) for u, r in off])


main()
