"""places.json: python3 -I places.py VNMAP_DIR
Coordinates from Wikipedia's API (prop=coordinates, coprimary=all) as fetched into dl/wiki/pl*.json; the index picks one of
an article's coordinates in page order (None: the primary, else the first). Province by point-in-polygon on the
unsimplified 1966 units (build/units_raw.geojson); a point outside every unit takes the nearest within 3 km."""
import glob, json, os, re, sys, unicodedata
from urllib.parse import quote
from shapely.geometry import shape, Point
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages import pages, redirects, resolve
from xw import UNITS

ROOT = sys.argv[1]
WIKI = sorted(glob.glob(os.path.join(ROOT, "dl/wiki/pl*.json")))
P = pages(WIKI)
R = redirects(WIKI)

# name, plain, kind, years, article, coord index, note, coord_from (if the article lacks coordinates: (parent article, why))
PLACES = [
 ("Sài Gòn", "Saigon", "city", "1960–68", "Ho Chi Minh City", None, "Capital of the RVN; the Capital Military District with Gia Định.", None),
 ("Tân Sơn Nhứt", "Tan Son Nhut", "base", "1960–68", "Tan Son Nhut Air Base", 0, "Air base on Saigon's edge; MACV headquarters beside it from 1967.", None),
 ("Huế", "Hue", "city", "1963–68", "Huế", None, "Buddhist crisis opened here, 8 May 1963; Battle of Huế, 31 Jan.–2 Mar. 1968.", None),
 ("Phú Bài", "Phu Bai", "base", "1965–68", "Phu Bai Combat Base", None, "Marine base and airfield south of Huế, from Apr. 1965.", None),
 ("Đà Nẵng", "Da Nang", "city", "1965–68", "Da Nang", None, "I Corps headquarters. Marines landed 8 Mar. 1965; Struggle Movement put down, May 1966.", None),
 ("Đà Nẵng Air Base", "Da Nang Air Base", "base", "1965–68", "Da Nang Air Base", None, "Air base; Marines' first mission its defense, Mar. 1965.", None),
 ("Hải Vân Pass", "Hai Van Pass", "region-feature", "", "Hải Vân Pass", None, "Route 1 pass between Thừa Thiên and Quảng Nam.", None),
 ("Hội An", "Hoi An", "city", "", "Hội An (city)", None, "Capital of Quảng Nam province.", None),
 ("Tam Kỳ", "Tam Ky", "city", "1962–68", "Tam Kỳ", None, "Capital of Quảng Tín, from 31 July 1962.", None),
 ("Quảng Ngãi", "Quang Ngai", "city", "", "Quảng Ngãi (city)", None, "Capital of Quảng Ngãi province.", None),
 ("Chu Lai", "Chu Lai", "base", "1965–68", "Chu Lai Base Area", None, "Marine base and airfield from 7 May 1965; Americal Division from 1967.", None),
 ("Vạn Tường", "Van Tuong", "operation", "1965", "Operation Starlite", None, "Operation Starlite, Marines' first regimental battle, 18–24 Aug. 1965.", None),
 ("Sơn Mỹ (Mỹ Lai)", "Son My (My Lai)", "battle", "1968", "My Lai massacre", None, "Massacre at Mỹ Lai 4 and Mỹ Khê 4, Sơn Mỹ village, 16 Mar. 1968.", None),
 ("Khâm Đức", "Kham Duc", "battle", "1968", "Battle of Kham Duc", None, "Special Forces camp evacuated under attack, 10–12 May 1968.", None),
 ("Quảng Trị", "Quang Tri", "city", "1968", "Quảng Trị (ward)", None, "Capital of Quảng Trị province; attacked at Tết, 31 Jan. 1968.", None),
 ("Đông Hà", "Dong Ha", "city", "1966–68", "Đông Hà", None, "Junction of Routes 1 and 9; Marine combat base from 1966.", None),
 ("Cồn Tiên", "Con Thien", "base", "1967", "Con Thien", None, "Marine base below the DMZ; shelled and besieged, Sept.–Oct. 1967.", None),
 ("Gio Linh", "Gio Linh", "base", "1967", "Gio Linh", None, "District town and Marine artillery base on Route 1 below the DMZ.", None),
 ("Camp Carroll", "Camp Carroll", "base", "1966–68", "Camp Carroll", None, "Marine artillery base on Route 9, from Oct. 1966.", None),
 ("The Rockpile", "Rockpile", "base", "1966–68", "The Rockpile", 0, "Marine observation post on Route 9, from Operation Hastings, July 1966.", None),
 ("Khe Sanh Combat Base", "Khe Sanh", "base", "1967–68", "Khe Sanh Combat Base", None, "Siege from 21 Jan. 1968; relieved by Operation Pegasus, 8 Apr. 1968.", None),
 ("Làng Vây", "Lang Vei", "battle", "1968", "Battle of Lang Vei", None, "Special Forces camp overrun by PAVN tanks, 6–7 Feb. 1968.", None),
 ("Bến Hải", "Ben Hai River", "region-feature", "1954–68", "Bến Hải River", None, "Demarcation line of the Geneva Accords, 21 July 1954; the point is at its mouth.", None),
 ("Khu phi quân sự (DMZ)", "DMZ", "region-feature", "1954–68", "Vietnamese Demilitarized Zone", None, "5 km either side of the Bến Hải, from 1954.", None),
 ("Thung lũng A Sầu", "A Shau Valley", "region-feature", "1966–68", "A Sầu Valley", None, "Special Forces camp overrun 9–10 Mar. 1966; Operation Delaware, Apr.–May 1968.", None),
 ("Kon Tum", "Kontum", "city", "", "Kon Tum", None, "Capital of Kon Tum province.", None),
 ("Đắk Tô", "Dak To", "battle", "1967", "Battle of Dak To", None, "Battle of Đắk Tô, 3–23 Nov. 1967.", None),
 ("Đồi 875", "Hill 875", "battle", "1967", "Battle of Dak To", 4, "173rd Airborne Brigade's assault, 19–23 Nov. 1967.", None),
 ("Pleiku", "Pleiku", "city", "1965–68", "Pleiku", None, "II Corps headquarters; Camp Holloway attacked 7 Feb. 1965.", None),
 ("Plei Me", "Plei Me", "battle", "1965", "Siege of Plei Me", None, "Siege of the Special Forces camp, 19–25 Oct. 1965.", None),
 ("Thung lũng Ia Drang", "Ia Drang", "battle", "1965", "Battle of Ia Drang", None, "Battle of the Ia Drang, 14–18 Nov. 1965.", None),
 ("LZ X-Ray", "LZ X-Ray", "battle", "1965", "Battle of Ia Drang", 2, "1st Battalion, 7th Cavalry, 14–16 Nov. 1965.", None),
 ("LZ Albany", "LZ Albany", "battle", "1965", "Battle of Ia Drang", 3, "2nd Battalion, 7th Cavalry ambushed, 17 Nov. 1965.", None),
 ("An Khê", "An Khe", "base", "1965–68", "Camp Radcliff", None, "Camp Radcliff, 1st Cavalry Division base, from Sept. 1965.", None),
 ("Quy Nhơn", "Qui Nhon", "city", "1965", "Quy Nhơn", None, "Capital of Bình Định; VC bombing of a U.S. billet, 10 Feb. 1965.", None),
 ("Bồng Sơn", "Bong Son", "city", "1966", "Bồng Sơn", None, "Town on the plain of Operation Masher/White Wing, Jan.–Mar. 1966.", None),
 ("Operation Masher", "Operation Masher", "operation", "1966", "Operation Masher", 0, "Masher/White Wing, 1st Cavalry Division, 24 Jan.–6 Mar. 1966; the point is its Landing Zone 4.", None),
 ("Ban Mê Thuột", "Ban Me Thuot", "city", "1964", "Buôn Ma Thuột", None, "Capital of Darlac; Montagnard (FULRO) revolt nearby, Sept. 1964.", None),
 ("Gia Nghĩa", "Gia Nghia", "city", "", "Gia Nghĩa", None, "Capital of Quảng Đức.", None),
 ("Nha Trang", "Nha Trang", "city", "1966–68", "Nha Trang", None, "Capital of Khánh Hòa; I Field Force and 5th Special Forces Group headquarters.", None),
 ("Cam Ranh", "Cam Ranh Bay", "base", "1965–68", "Cam Ranh Base", None, "Port and air base built from 1965.", None),
 ("Đà Lạt", "Dalat", "city", "", "Da Lat", None, "Autonomous city; Vietnamese National Military Academy.", None),
 ("Phan Thiết", "Phan Thiet", "city", "", "Phan Thiết", None, "Capital of Bình Thuận.", None),
 ("Biên Hòa", "Bien Hoa", "city", "1964–68", "Biên Hòa (city)", None, "III Corps headquarters; capital of Biên Hòa province.", None),
 ("Căn cứ Không quân Biên Hòa", "Bien Hoa Air Base", "base", "1964–68", "Bien Hoa Air Base", None, "Air base; B-57s destroyed by VC mortars, 1 Nov. 1964.", None),
 ("Long Bình", "Long Binh", "base", "1966–68", "Long Binh Post", 0, "U.S. Army logistics base; USARV headquarters from 1967.", None),
 ("Thủ Dầu Một (Phú Cường)", "Phu Cuong", "city", "", "Thủ Dầu Một, Ho Chi Minh City", None, "Capital of Bình Dương, as Phú Cường.", None),
 ("Tam giác Sắt", "Iron Triangle", "region-feature", "1967", "Iron Triangle (Vietnam)", None, "VC base area; Operation Cedar Falls, 8–26 Jan. 1967.",
  ("Bến Cát", "the article has no coordinates: Bến Cát's, the town of the district holding it")),
 ("Bến Súc", "Ben Suc", "operation", "1967", "Bến Súc", None, "Operation Cedar Falls: Bến Súc emptied and razed, 8 Jan. 1967.", None),
 ("Củ Chi", "Cu Chi", "base", "1966–68", "Củ Chi", None, "25th Infantry Division base camp, from Jan. 1966.", None),
 ("Địa đạo Củ Chi", "Cu Chi tunnels", "region-feature", "1966–68", "Củ Chi tunnels", None, "VC tunnel complex; Operation Crimp, Jan. 1966.", None),
 ("Tây Ninh", "Tay Ninh", "city", "", "Tây Ninh (city)", None, "Capital of Tây Ninh; the Cao Đài Holy See.", None),
 ("Chiến khu C", "War Zone C", "region-feature", "1967", "War Zone C", None, "VC base area on the Cambodian border; Operation Junction City, 22 Feb.–14 May 1967.",
  ("Tây Ninh province", "the article has no coordinates: Tây Ninh province's")),
 ("Operation Junction City", "Junction City", "operation", "1967", "Operation Junction City", None, "Largest U.S. operation to date, War Zone C, 22 Feb.–14 May 1967.",
  ("Tây Ninh province", "the article has no coordinates: Tây Ninh province's, the province of War Zone C")),
 ("An Lộc", "An Loc", "city", "", "Bình Long", None, "Capital of Bình Long, as An Lộc.", None),
 ("Lộc Ninh", "Loc Ninh", "battle", "1967", "Lộc Ninh, Đồng Nai", None, "Battle of Lộc Ninh, 29 Oct.–7 Nov. 1967.", None),
 ("Đồng Xoài", "Dong Xoai", "battle", "1965", "Battle of Đồng Xoài", None, "Battle of Đồng Xoài, 9–13 June 1965.", None),
 ("Bình Giã", "Binh Gia", "battle", "1964–65", "Battle of Binh Gia", None, "Battle of Bình Giã, 28 Dec. 1964–1 Jan. 1965.", None),
 ("Vũng Tàu", "Vung Tau", "city", "1965–68", "Vũng Tàu", None, "Autonomous town and port; Australian logistic base from 1966.", None),
 ("Tân An", "Tan An", "city", "", "Tân An (city)", None, "Capital of Long An.", None),
 ("Ấp Bắc", "Ap Bac", "battle", "1963", "Battle of Ap Bac", None, "Battle of Ấp Bắc, 2 Jan. 1963.", None),
 ("Mỹ Tho", "My Tho", "city", "1963", "Mỹ Tho (city)", None, "Capital of Định Tường; 7th Division headquarters.", None),
 ("Bến Tre (Trúc Giang)", "Ben Tre", "city", "1968", "Bến Tre (city)", None, "Capital of Kiến Hòa, as Trúc Giang; fought over at Tết, Feb. 1968.", None),
 ("Cần Thơ", "Can Tho", "city", "1963–68", "Cần Thơ", None, "IV Corps headquarters; capital of Phong Dinh.", None),
 ("Vĩnh Long", "Vinh Long", "city", "", "Vĩnh Long (city)", None, "Capital of Vĩnh Long.", None),
 ("Trà Vinh (Phú Vinh)", "Phu Vinh", "city", "", "Trà Vinh", None, "Capital of Vĩnh Bình, as Phú Vinh.", None),
 ("Cao Lãnh", "Cao Lanh", "city", "", "Cao Lãnh", None, "Capital of Kiến Phong.", None),
 ("Long Xuyên", "Long Xuyen", "city", "", "Long Xuyên", None, "Capital of An Giang.", None),
 ("Châu Đốc", "Chau Doc", "city", "", "Châu Đốc", None, "Capital of Châu Đốc province (seat Châu Phú).", None),
 ("Rạch Giá", "Rach Gia", "city", "", "Rạch Giá (city)", None, "Capital of Kiên Giang.", None),
 ("Vị Thanh", "Vi Thanh", "city", "", "Vị Thanh (city)", None, "Capital of Chương Thiện.", None),
 ("Sóc Trăng (Khánh Hưng)", "Soc Trang", "city", "", "Sóc Trăng", None, "Capital of Ba Xuyên, as Khánh Hưng.", None),
 ("Bạc Liêu", "Bac Lieu", "city", "", "Bạc Liêu (city)", None, "Capital of Bạc Liêu, re-created 8 Sept. 1964.", None),
 ("Cà Mau (Quản Long)", "Ca Mau", "city", "", "Cà Mau (city)", None, "Capital of An Xuyên, as Quản Long.", None),
 ("Côn Sơn", "Con Son", "region-feature", "1960–68", "Côn Sơn Island", None, "Prison island; province until 24 Apr. 1965.", None),
]
CORPS_HQ = {"Đà Nẵng": "I", "Pleiku": "II", "Biên Hòa": "III", "Cần Thơ": "IV", "Sài Gòn": "CMD"}


def fold(s):
    s = unicodedata.normalize("NFD", s.replace("Đ", "D").replace("đ", "d"))
    return re.sub(r"[^a-z]", "", "".join(c for c in s if unicodedata.category(c) != "Mn").lower())


def coords(title, idx):
    t = resolve(title, R)
    p = P.get(t)
    if not p or p.get("missing"):
        return None, t
    cs = p.get("coordinates") or []
    if not cs:
        return None, t
    if idx is None:
        pr = [c for c in cs if c.get("primary")]
        c = pr[0] if pr else cs[0]
    else:
        c = cs[idx]
    return (round(c["lat"], 5), round(c["lon"], 5)), t


def text(t):
    p = P.get(t)
    return p["revisions"][0]["slots"]["main"]["content"] if p and p.get("revisions") else ""


def article_province(t):
    """the first 'X province' (or 'X Province') the article's text names, past the infobox's own name"""
    s = re.sub(r"<ref.*?</ref>|<ref[^>]*/>", "", text(t), flags=re.S)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s)
    for m in re.finditer(r"((?:[A-ZĐ][^\s,.;:()|\[\]{}=]*\s){1,3})[Pp]rovince", s):
        name = m.group(1).strip()
        if fold(name) in ("the", "this", "each", "a", "southvietnam", "every", "border", "neighboring") or len(fold(name)) < 3:
            continue
        return name
    return None


def main():
    units = [(f["properties"]["id"], shape(f["geometry"])) for f in json.load(open(os.path.join(ROOT, "build/units_raw.geojson")))["features"]]
    out = []
    for name, plain, kind, years, art, idx, note, cf in PLACES:
        (ll, t) = coords(art, idx)
        src_t = t
        if ll is None and cf:
            ll, src_t = coords(cf[0], None)
            note = note + " Coordinates: " + cf[1] + "."
        if ll is None:
            print("NO COORDS", name, art)
            continue
        pt = Point(ll[1], ll[0])
        prov = next((uid for uid, g in units if g.contains(pt)), None)
        how = "within"
        if prov is None:
            d, uid = min((g.distance(pt), uid) for uid, g in units)
            if d < 0.03:
                prov, how = uid, f"nearest ({d * 111:.1f} km off the coast or line)"
            else:
                how = "outside the RVN units"
        e = dict(name=name, plain=plain, kind=kind, lat=ll[0], lon=ll[1], years=years, province=prov, note=note,
                 wiki="https://en.wikipedia.org/wiki/" + quote(t.replace(" ", "_")))
        if src_t != t:
            e["coord_source"] = "https://en.wikipedia.org/wiki/" + quote(src_t.replace(" ", "_"))
        if name in CORPS_HQ:
            e["corps_hq"] = CORPS_HQ[name]
        e["_pip"] = how
        e["_article_province"] = article_province(t)
        out.append(e)
    json.dump([{k: v for k, v in e.items() if not k.startswith("_")} for e in out],
              open(os.path.join(ROOT, "places.json"), "w"), ensure_ascii=False, indent=1)
    json.dump(out, open(os.path.join(ROOT, "build/places_check.json"), "w"), ensure_ascii=False, indent=1)
    print(len(out), "places")


main()
