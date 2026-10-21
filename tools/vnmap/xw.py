"""The 1966 crosswalk, by hand: each unit of the RVN in late 1966 (after Sa Đéc's re-creation, 24 Sept 1966)
and the GADM 4.1 districts (NAME_1/NAME_2, GADM's spelling) assigned whole to it.

Sources (W = Wikipedia):
  VI_TINH  vi W "Tỉnh (Việt Nam Cộng hòa)": the 1964 and later lists of provinces, districts, areas
  each province's own article (en / vi), cited per unit; corps from the en/vi corps articles.
"""

EN = "https://en.wikipedia.org/wiki/"
VI = "https://vi.wikipedia.org/wiki/"
VI_TINH = VI + "T%E1%BB%89nh_(Vi%E1%BB%87t_Nam_C%E1%BB%99ng_h%C3%B2a)"


def u(base, title):
    from urllib.parse import quote
    return base + quote(title.replace(" ", "_"))


# modern (pre-2025) region of each GADM NAME_1
REGION = {}
for r, ps in {
    "North Central Coast": "QuảngTrị ThừaThiênHuế QuảngBình",
    "South Central Coast": "ĐàNẵng QuảngNam QuảngNgãi BìnhĐịnh PhúYên KhánhHòa NinhThuận BìnhThuận",
    "Central Highlands": "KonTum GiaLai ĐắkLắk ĐắkNông LâmĐồng",
    "Southeast": "BìnhPhước BìnhDương ĐồngNai TâyNinh BàRịa-VũngTàu HồChíMinh",
    "Mekong Delta": "LongAn TiềnGiang BếnTre TràVinh VĩnhLong ĐồngTháp AnGiang KiênGiang CầnThơ HậuGiang SócTrăng BạcLiêu CàMau",
}.items():
    for p in ps.split():
        REGION[p] = r

DROP = ["QuảngTrị/VĩnhLinh", "QuảngTrị/CồnCỏ"]  # north of the Bến Hải: the DRV

# id, name, plain, kind, capital, ctz, districts, confidence, straddle/notes, sources
UNITS = [
 # ---------------- I CTZ
 dict(id="quang-tri", name="Quảng Trị", plain="Quang Tri", kind="province", capital="Quảng Trị", ctz="I",
      d="QuảngTrị: CamLộ ĐaKrông ĐôngHà GioLinh HảiLăng HướngHóa QuảngTrị TriệuPhong",
      conf="high", note="Today's Quảng Trị south of the Bến Hải; Vĩnh Linh and Cồn Cỏ (DRV) dropped.",
      src=[VI_TINH, u(EN, "Quảng Trị province")]),
 dict(id="thua-thien", name="Thừa Thiên", plain="Thua Thien", kind="province", capital="Huế", ctz="I",
      d="ThừaThiênHuế: ALưới HươngThủy HươngTrà NamĐông PhongĐiền PhúLộc PhúVang QuảngĐiền",
      conf="high", note="Today's Thừa Thiên Huế less the city of Huế; A Lưới (A Shau) in Thừa Thiên.",
      src=[VI_TINH, u(VI, "Thừa Thiên")]),
 dict(id="hue", name="Huế", plain="Hue", kind="city", capital="Huế", ctz="I",
      d="ThừaThiênHuế: Huế",
      conf="low", note="Autonomous city (thị xã). The modern city (GADM: 71 km²) is larger than the 1964 city (15 km², VI_TINH).",
      src=[VI_TINH, u(EN, "Huế")]),
 dict(id="da-nang", name="Đà Nẵng", plain="Da Nang", kind="city", capital="Đà Nẵng", ctz="I",
      d="ĐàNẵng: HảiChâu ThanhKhê SơnTrà",
      conf="medium", note="Autonomous city (thị xã), 60 km² in 1964 (VI_TINH); the three inner districts (≈92 km²) stand for it. "
                          "Liên Chiểu, Cẩm Lệ, Ngũ Hành Sơn (Marble Mountain) and Hòa Vang go to Quảng Nam (Hòa Vang district).",
      src=[VI_TINH, u(EN, "Da Nang")]),
 dict(id="quang-nam", name="Quảng Nam", plain="Quang Nam", kind="province", capital="Hội An", ctz="I",
      d="ĐàNẵng: HòaVang LiênChiểu CẩmLệ NgũHànhSơn; QuảngNam: ĐiệnBàn HộiAn DuyXuyên ĐạiLộc QuếSơn NôngSơn ĐôngGiang TâyGiang NamGiang",
      conf="medium", note="Districts 1966: Duy Xuyên, Đại Lộc, Điện Bàn, Đức Dục, Hiếu Đức, Hiếu Nhơn, Hòa Vang, Quế Sơn, Thường Đức. "
                          "Quế Sơn/Nông Sơn straddle the Quảng Tín line (Quảng Tín was cut partly from old Quế Sơn district).",
      src=[VI_TINH, u(EN, "Quảng Nam province")]),
 dict(id="quang-tin", name="Quảng Tín", plain="Quang Tin", kind="province", capital="Tam Kỳ", ctz="I",
      d="QuảngNam: TamKỳ PhúNinh NúiThành ThăngBình TiênPhước HiệpĐức BắcTràMy NamTràMy PhướcSơn",
      conf="medium", note="Created 31 July 1962. Districts 1965: Hậu Đức, Hiệp Đức, Lý Tín, Tam Kỳ, Tiên Phước, Thăng Bình. "
                          "Phước Sơn (Khâm Đức) and the Trà My districts (Hậu Đức) assigned here; area 5,049 km² against 4,903 (1964).",
      src=[u(EN, "Quảng Tín province"), VI_TINH]),
 dict(id="quang-ngai", name="Quảng Ngãi", plain="Quang Ngai", kind="province", capital="Quảng Ngãi", ctz="I",
      ctz_note="II CTZ until Sept. 1964, then I CTZ (W 'I Corps (South Vietnam)').",
      d="QuảngNgãi: BaTơ BìnhSơn ĐứcPhổ LýSơn MinhLong MộĐức NghĩaHành QuảngNgãi SơnHà SơnTây SơnTịnh TâyTrà TràBồng TưNghĩa",
      conf="high", note="Today's Quảng Ngãi. The 1964 area (6,981 km²) exceeds today's (≈5,150): the line with Kon Tum is not checked.",
      src=[VI_TINH, u(EN, "I Corps (South Vietnam)")]),
 # ---------------- II CTZ
 dict(id="kon-tum", name="Kon Tum", plain="Kontum", kind="province", capital="Kon Tum", ctz="II",
      d="KonTum: ĐắkGlei ĐắkHà ĐắkTô IaH'Drai KonPlông KonRẫy KonTum NgọcHồi SaThầy TuMơRông",
      conf="high", note="Today's Kon Tum.", src=[VI_TINH]),
 dict(id="pleiku", name="Pleiku", plain="Pleiku", kind="province", capital="Pleiku", ctz="II",
      d="GiaLai: ChưPăh ChưPrông ChưPưh ChưSê ĐăkĐoa ĐứcCơ IaGrai MangYang Pleiku",
      conf="high", note="vi W: today's Gia Lai less Phú Bổn (Phú Thiện, Ia Pa, Krông Pa, Ayun Pa) and An Túc of Bình Định "
                        "(An Khê, Đak Pơ, Kbang, Kông Chro). Area 8,239 km² against 8,260 (1971).",
      src=[u(VI, "Pleiku (tỉnh)")]),
 dict(id="phu-bon", name="Phú Bổn", plain="Phu Bon", kind="province", capital="Hậu Bổn (Cheo Reo)", ctz="II",
      d="GiaLai: AyunPa PhúThiện IaPa KrôngPa",
      conf="low", note="Created 1 Sept 1962 from south Pleiku and north Darlac (Thuần Mẫn). The south of Thuần Mẫn lies in Ea H'leo "
                          "(Đắk Lắk), left with Darlac. Area 3,285 km² against 4,822 (1971).",
      src=[u(VI, "Phú Bổn"), u(EN, "Phú Bổn province")]),
 dict(id="binh-dinh", name="Bình Định", plain="Binh Dinh", kind="province", capital="Qui Nhơn", ctz="II",
      d="BìnhĐịnh: AnLão AnNhơn HoàiÂn HoàiNhơn PhùCát PhùMỹ QuiNhơn TâySơn TuyPhước VânCanh VĩnhThạnh; GiaLai: AnKhê ĐăkPơ KBang KôngChro",
      conf="high", note="Today's Bình Định plus An Túc district (An Khê, Đak Pơ, Kbang, Kông Chro, now Gia Lai): vi W 'Pleiku (tỉnh)'.",
      src=[VI_TINH, u(VI, "Pleiku (tỉnh)")]),
 dict(id="phu-yen", name="Phú Yên", plain="Phu Yen", kind="province", capital="Tuy Hòa", ctz="II",
      d="PhúYên: ĐôngHòa ĐồngXuân PhúHoà SơnHòa SôngCầu SôngHinh TâyHoà TuyAn TuyHoà",
      conf="high", note="Today's Phú Yên (5,023 km² against 5,233, 1964).", src=[VI_TINH]),
 dict(id="darlac", name="Darlac", plain="Darlac", kind="province", capital="Ban Mê Thuột", ctz="II",
      d="ĐắkLắk: BuônĐôn BuônMaThuột CưKuin CưM'gar EaH'leo EaKar EaSúp KrôngANa KrôngBông KrôngBúk KrôngNăng KrôngPắc Lắk ThịXãBuônHồ; ĐắkNông: CưJút",
      conf="medium", note="Today's Đắk Lắk less M'Đrắk (Khánh Dương district of Khánh Hòa), plus Cư Jút (Ban Mê Thuột district, vi W "
                          "'Quảng Đức (tỉnh)'). Ea H'leo holds the south of Phú Bổn's Thuần Mẫn.",
      src=[u(VI, "Đắk Lắk"), u(VI, "Quảng Đức (tỉnh)")]),
 dict(id="quang-duc", name="Quảng Đức", plain="Quang Duc", kind="province", capital="Gia Nghĩa", ctz="II",
      d="ĐắkNông: ĐăkGlong ĐắkMil ĐắkR'Lấp ĐắkSong GiaNghĩa KrôngNô TuyĐức",
      conf="high", note="vi W: today's Đắk Nông less Cư Jút. Area 5,789 km² against 5,958 (1971).",
      src=[u(VI, "Quảng Đức (tỉnh)")]),
 dict(id="khanh-hoa", name="Khánh Hòa", plain="Khanh Hoa", kind="province", capital="Nha Trang", ctz="II",
      d="KhánhHòa: CamLâm DiênKhánh KhánhSơn KhánhVĩnh NhaTrang NinhHòa VạnNinh; ĐắkLắk: M'Đrắk",
      conf="medium", note="M'Đrắk was Khánh Dương district (part went to Phú Yên: vi W 'Đắk Lắk'). Area with Cam Ranh 6,034 km² against 5,985 (1964).",
      src=[VI_TINH, u(VI, "Đắk Lắk")]),
 dict(id="cam-ranh", name="Cam Ranh", plain="Cam Ranh", kind="city", capital="Cam Ranh", ctz="II",
      d="KhánhHòa: CamRanh",
      conf="medium", note="Autonomous town (thị xã) created Oct. 1965 from Cam Lâm district communes and villages of Du Long (Ninh Thuận): vi W 'Cam Ranh'.",
      src=[u(VI, "Cam Ranh")]),
 dict(id="ninh-thuan", name="Ninh Thuận", plain="Ninh Thuan", kind="province", capital="Phan Rang", ctz="II",
      d="NinhThuận: BácÁi NinhHải NinhPhước NinhSơn PhanRang-ThápChàm ThuậnBắc ThuậnNam",
      conf="high", note="Today's Ninh Thuận.", src=[VI_TINH]),
 dict(id="tuyen-duc", name="Tuyên Đức", plain="Tuyen Duc", kind="province", capital="Đà Lạt (Tùng Nghĩa from 7 Sept 1967)", ctz="II",
      d="LâmĐồng: ĐứcTrọng ĐơnDương LạcDương ĐamRông LâmHà",
      conf="medium", note="vi W: Đà Lạt, Đức Trọng (less Ninh Gia), Đơn Dương, Lạc Dương, Đam Rông and part of Lâm Hà.",
      src=[u(VI, "Tuyên Đức")]),
 dict(id="da-lat", name="Đà Lạt", plain="Dalat", kind="city", capital="Đà Lạt", ctz="II",
      d="LâmĐồng: ĐàLạt",
      conf="low", note="Autonomous city. The modern city (≈393 km²) is far larger than the 1964 city (69 km², VI_TINH).",
      src=[VI_TINH, u(EN, "Da Lat")]),
 dict(id="lam-dong", name="Lâm Đồng", plain="Lam Dong", kind="province", capital="Bảo Lộc", ctz="II",
      ctz_note="III CTZ until Sept. 1964, then II (W 'II Corps (South Vietnam)').",
      d="LâmĐồng: BảoLâm BảoLộc DiLinh ĐạHuoai ĐạTẻh",
      conf="medium", note="1966 districts Bảo Lộc, Di Linh. Cát Tiên given to Phước Long (vi W 'Phước Long (tỉnh)': most of it). "
                          "Area 4,342 km² against 4,739 (1964), which would fit with Cát Tiên.",
      src=[VI_TINH, u(VI, "Phước Long (tỉnh)")]),
 dict(id="binh-thuan", name="Bình Thuận", plain="Binh Thuan", kind="province", capital="Phan Thiết", ctz="II",
      ctz_note="III CTZ until Sept. 1964, then II (W 'II Corps (South Vietnam)').",
      d="BìnhThuận: BắcBình HàmThuậnBắc PhanThiết PhúQuí TuyPhong",
      conf="medium", note="Today's Bình Thuận less the west (Bình Tuy). Area 4,124 km² against 4,277 (1964).",
      src=[VI_TINH, u(EN, "Bình Tuy province")]),
 dict(id="binh-tuy", name="Bình Tuy", plain="Binh Tuy", kind="province", capital="Hàm Tân", ctz="II",
      ctz_note="III to II CTZ Sept. 1964 (W 'II Corps'); in II during Operation Hardihood, May–June 1966 (W); in III by 1968 "
               "(vi W 'Quân đoàn III': 18th Division's area). Date of the return to III not found. Check.",
      d="BìnhThuận: ĐứcLinh HàmTân HàmThuậnNam LaGi TánhLinh",
      conf="medium", note="en W: Hàm Tân, Hàm Thuận Nam, Tánh Linh, Đức Linh, La Gi. Area 3,681 km² against 3,560 (1971).",
      src=[u(EN, "Bình Tuy province"), u(VI, "Bình Tuy"), u(EN, "Operation Hardihood")]),
 # ---------------- III CTZ
 dict(id="phuoc-long", name="Phước Long", plain="Phuoc Long", kind="province", capital="Phước Bình (Song Bé)", ctz="III",
      d="BìnhPhước: BùĐăng BùĐốp BùGiaMập ĐồngPhú ĐồngXoài PhúRiềng PhướcLong; LâmĐồng: CátTiên",
      conf="medium", note="vi W: Đồng Xoài, Phước Long, Đồng Phú, Bù Đăng, Phú Riềng, Bù Gia Mập, Bù Đốp, part of Phú Giáo, most of Cát Tiên. "
                          "Đồng Phú was partly Phước Thành (1959–65).",
      src=[u(VI, "Phước Long (tỉnh)")]),
 dict(id="binh-long", name="Bình Long", plain="Binh Long", kind="province", capital="An Lộc", ctz="III",
      d="BìnhPhước: BìnhLong ChơnThành HớnQuản LộcNinh",
      conf="high", note="vi W: Bình Long, Chơn Thành, Hớn Quản, Lộc Ninh and parts of Dầu Tiếng, Bàu Bàng, Phú Giáo.",
      src=[u(VI, "Bình Long (tỉnh)")]),
 dict(id="tay-ninh", name="Tây Ninh", plain="Tay Ninh", kind="province", capital="Tây Ninh", ctz="III",
      d="TâyNinh: BếnCầu ChâuThành DươngMinhChâu GòDầu HòaThành TânBiên TânChâu TâyNinh",
      conf="high", note="Today's Tây Ninh less Trảng Bàng (Hậu Nghĩa). Area 3,701 km² against 3,845 (1964).",
      src=[VI_TINH]),
 dict(id="hau-nghia", name="Hậu Nghĩa", plain="Hau Nghia", kind="province", capital="Khiêm Cường (Bao Trai)", ctz="III",
      d="HồChíMinh: CủChi; LongAn: ĐứcHòa ĐứcHuệ; TâyNinh: TrảngBàng",
      conf="high", note="Created 15 Oct. 1963: Củ Chi, Đức Hòa, Đức Huệ, Trảng Bàng (en W).",
      src=[u(EN, "Hậu Nghĩa province")]),
 dict(id="binh-duong", name="Bình Dương", plain="Binh Duong", kind="province", capital="Phú Cường", ctz="III",
      d="BìnhDương: ThủDầuMột ThuậnAn BếnCát BàuBàng DầuTiếng PhúGiáo",
      conf="medium", note="Districts: Bến Cát, Châu Thành, Lái Thiêu (Thuận An), Phú Hòa, Phú Giáo (from Phước Thành, 1965), Trị Tâm (Dầu Tiếng). "
                          "Dĩ An and Tân Uyên were Biên Hòa's.",
      src=[VI_TINH, u(EN, "Phước Thành province")]),
 dict(id="bien-hoa", name="Biên Hòa", plain="Bien Hoa", kind="province", capital="Biên Hòa", ctz="III",
      d="ĐồngNai: BiênHòa LongThành NhơnTrạch TrảngBom VĩnhCửu; BìnhDương: DĩAn TânUyên BắcTânUyên; HồChíMinh: CầnGiờ",
      conf="medium", note="Districts: Công Thanh, Dĩ An, Đức Tu, Long Thành, Nhơn Trạch, Tân Uyên (back from Phước Thành, 1965), and Cần Giờ and "
                          "Quảng Xuyên (from Phước Tuy, 9 Sept 1960; to Gia Định 1970). Trảng Bom and Vĩnh Cửu straddle Long Khánh "
                          "(vi W 'Long Khánh (tỉnh)': part of each). Quận 9's Long Vĩnh Hạ canton went back to Gia Định 10 Oct 1965.",
      src=[u(VI, "Biên Hòa (tỉnh)"), u(VI, "Long Khánh (tỉnh)"), u(VI, "Quận 9")]),
 dict(id="long-khanh", name="Long Khánh", plain="Long Khanh", kind="province", capital="Xuân Lộc", ctz="III",
      d="ĐồngNai: LongKhánh CẩmMỹ ĐịnhQuán TânPhú ThốngNhất XuânLộc",
      conf="high", note="vi W: Long Khánh, Cẩm Mỹ, Định Quán, Tân Phú, Thống Nhất, Xuân Lộc and part of Trảng Bom and Vĩnh Cửu. "
                        "Area 3,375 km² against 3,457 (1967).",
      src=[u(VI, "Long Khánh (tỉnh)")]),
 dict(id="phuoc-tuy", name="Phước Tuy", plain="Phuoc Tuy", kind="province", capital="Phước Lễ (Bà Rịa)", ctz="III",
      d="BàRịa-VũngTàu: BàRịa ChâuĐức ĐấtĐỏ LongĐiền TânThành XuyênMộc",
      conf="high", note="Today's Bà Rịa–Vũng Tàu less Vũng Tàu (city from 1964) and Côn Đảo. Area 1,759 km² against 1,927 (1966).",
      src=[u(VI, "Phước Tuy"), u(EN, "Phước Tuy province")]),
 dict(id="vung-tau", name="Vũng Tàu", plain="Vung Tau", kind="city", capital="Vũng Tàu", ctz="III",
      d="BàRịa-VũngTàu: VũngTàu",
      conf="medium", note="Autonomous town (thị xã) from 1964 (vi W 'Phước Tuy'); 74 km² in 1964. The modern city includes Long Sơn island.",
      src=[u(VI, "Phước Tuy"), VI_TINH]),
 dict(id="long-an", name="Long An", plain="Long An", kind="province", capital="Tân An", ctz="III",
      ctz_note="III CTZ from 5 Sept. 1964, when the Tiền Giang Tactical Area was abolished (W 'III Corps (South Vietnam)').",
      d="LongAn: TânAn ChâuThành TânTrụ BếnLức ThủThừa CầnĐước CầnGiuộc",
      conf="high", note="Area 1,354 km² against 1,382 (1964).", src=[VI_TINH]),
 dict(id="gia-dinh", name="Gia Định", plain="Gia Dinh", kind="province", capital="Gia Định (Bình Hòa)", ctz="CMD",
      ctz_note="Capital Military District (Biệt khu Thủ đô): Saigon and Gia Định, a separate zone from 21 Nov. 1962 (Quân khu Thủ đô "
               "2 July 1965–18 July 1966); for MACV inside III CTZ. Gia Định added to MR 3 on 1 July 1970 (vi W 'Biệt khu Thủ đô').",
      d="HồChíMinh: BìnhChánh BìnhTân BìnhThạnh GòVấp HócMôn NhàBè PhúNhuận Quận12 Quận2 Quận7 Quận9 TânBình TânPhú ThủĐức",
      conf="high", note="Districts 1966: Bình Chánh, Gò Vấp, Hóc Môn, Nhà Bè, Tân Bình, Thủ Đức. Area ≈900 km² with Quận 9 against 824 (1964).",
      src=[u(VI, "Gia Định (tỉnh)"), u(VI, "Biệt khu Thủ đô")]),
 dict(id="saigon", name="Sài Gòn", plain="Saigon", kind="city", capital="Saigon", ctz="CMD",
      ctz_note="Capital Military District.",
      d="HồChíMinh: Quận1 Quận3 Quận4 Quận5 Quận6 Quận8 Quận10 Quận11",
      conf="high", note="Đô thành Sài Gòn. The eight districts sum to 58 km², the 1964 area (VI_TINH).",
      src=[VI_TINH]),
 # ---------------- IV CTZ
 dict(id="kien-tuong", name="Kiến Tường", plain="Kien Tuong", kind="province", capital="Mộc Hóa", ctz="IV",
      ctz_note="IV CTZ from 5 Sept. 1964, when the Tiền Giang Tactical Area (7th Division) was abolished and four of its five provinces went to IV (W 'IV Corps'; which four not stated). Check.",
      d="LongAn: KiếnTường MộcHóa TânHưng VĩnhHưng TânThạnh ThạnhHóa",
      conf="high", note="vi W: Kiến Tường, Mộc Hóa, Tân Hưng, Tân Thạnh, Thạnh Hóa, Vĩnh Hưng and part of Tân Phước. Area 2,276 km² against 2,297 (1964).",
      src=[u(VI, "Kiến Tường (tỉnh)")]),
 dict(id="dinh-tuong", name="Định Tường", plain="Dinh Tuong", kind="province", capital="Mỹ Tho", ctz="IV",
      ctz_note="Probably in the Tiền Giang Tactical Area until 5 Sept. 1964, then IV CTZ (W 'IV Corps'). Check.",
      d="TiềnGiang: MỹTho ChâuThành ChợGạo CaiLậy CaiLậy(Thịxã) CáiBè TânPhước",
      conf="medium", note="Tân Phước straddles Kiến Tường (its four northern communes). Area 1,762 km² against 1,640 (1967).",
      src=[u(VI, "Định Tường"), u(VI, "Kiến Tường (tỉnh)")]),
 dict(id="go-cong", name="Gò Công", plain="Go Cong", kind="province", capital="Gò Công", ctz="IV",
      ctz_note="Probably in the Tiền Giang Tactical Area until 5 Sept. 1964, then IV CTZ (W 'IV Corps'). Check.",
      d="TiềnGiang: GòCông GòCôngĐông GòCôngTây TânPhúĐông",
      conf="high", note="Re-created 20 Dec. 1963. vi W: Gò Công, Gò Công Đông, Gò Công Tây, Tân Phú Đông.",
      src=[u(VI, "Gò Công (tỉnh)")]),
 dict(id="kien-hoa", name="Kiến Hòa", plain="Kien Hoa", kind="province", capital="Trúc Giang (Bến Tre)", ctz="IV",
      ctz_note="Probably in the Tiền Giang Tactical Area until 5 Sept. 1964, then IV CTZ (W 'IV Corps'). Check.",
      d="BếnTre: BaTri BếnTre BìnhĐại ChâuThành GiồngTrôm MỏCàyBắc MỏCàyNam ThạnhPhú",
      conf="high", note="Today's Bến Tre less Chợ Lách (Vĩnh Long). Area 2,192 km² against 2,085 (1970).",
      src=[u(VI, "Kiến Hòa"), VI_TINH]),
 dict(id="kien-phong", name="Kiến Phong", plain="Kien Phong", kind="province", capital="Cao Lãnh", ctz="IV",
      d="ĐồngTháp: CaoLãnh(Thànhphố) CaoLãnh ThápMười ThanhBình TamNông HồngNgự HồngNgự(Thịxã) TânHồng",
      conf="high", note="vi W: Đồng Tháp north-west of the Tiền. Area 2,579 km² against 2,657.",
      src=[u(VI, "Kiến Phong")]),
 dict(id="sa-dec", name="Sa Đéc", plain="Sa Dec", kind="province", capital="Sa Đéc", ctz="IV",
      d="ĐồngTháp: SaĐéc LaiVung LấpVò ChâuThành",
      conf="high", note="Re-created 24 Sept. 1966 from Vĩnh Long. vi W: Đồng Tháp south of the Tiền. Area 789 km², the article's figure.",
      src=[u(VI, "Sa Đéc (tỉnh)"), VI_TINH]),
 dict(id="vinh-long", name="Vĩnh Long", plain="Vinh Long", kind="province", capital="Vĩnh Long", ctz="IV",
      d="VĩnhLong: VĩnhLong LongHồ MangThít TamBình BìnhMinh BìnhTân; BếnTre: ChợLách",
      conf="medium", note="Trà Ôn and Vũng Liêm stay with Vĩnh Bình until 14 Jan. 1967 (vi W 'Trà Ôn (huyện)', 'Vũng Liêm'). "
                          "Chợ Lách and Minh Đức (part of Mỏ Cày Bắc) were Vĩnh Long's; Mang Thít straddles Vũng Liêm.",
      src=[VI_TINH, u(VI, "Trà Ôn (huyện)"), u(VI, "Vũng Liêm")]),
 dict(id="vinh-binh", name="Vĩnh Bình", plain="Vinh Binh", kind="province", capital="Phú Vinh (Trà Vinh)", ctz="IV",
      d="TràVinh: CàngLong CầuKè CầuNgang ChâuThành DuyênHải DuyênHải(Thịxã) TiểuCần TràCú TràVinh; VĩnhLong: TràÔn VũngLiêm",
      conf="medium", note="With Trà Ôn and Vũng Liêm until 14 Jan. 1967. Area 2,910 km² against 2,880 (1964).",
      src=[VI_TINH, u(VI, "Trà Ôn (huyện)"), u(VI, "Vũng Liêm")]),
 dict(id="chau-doc", name="Châu Đốc", plain="Chau Doc", kind="province", capital="Châu Phú (Châu Đốc)", ctz="IV",
      d="AnGiang: ChâuĐốc AnPhú TânChâu PhúTân ChâuPhú TịnhBiên TriTôn",
      conf="high", note="Re-created 8 Sept. 1964. vi W: Phú Tân, Châu Phú, An Phú, Tân Châu, Tịnh Biên, Châu Đốc, two-thirds of Tri Tôn, "
                        "part of Giang Thành. Area 2,040 km² against 2,151 (1964).",
      src=[u(VI, "Châu Đốc (tỉnh)")]),
 dict(id="an-giang", name="An Giang", plain="An Giang", kind="province", capital="Long Xuyên", ctz="IV",
      d="AnGiang: LongXuyên ChâuThành ChợMới ThoạiSơn; CầnThơ: ThốtNốt VĩnhThạnh",
      conf="high", note="Districts: Châu Thành, Chợ Mới, Huệ Đức (Thoại Sơn), Thốt Nốt. A third of Tri Tôn lies here (left with Châu Đốc).",
      src=[VI_TINH, u(VI, "Châu Đốc (tỉnh)")]),
 dict(id="kien-giang", name="Kiên Giang", plain="Kien Giang", kind="province", capital="Rạch Giá", ctz="IV",
      d="KiênGiang: AnBiên AnMinh ChâuThành GiangThành GiồngRiềng HàTiên HònĐất KiênHải KiênLương PhúQuốc RạchGiá TânHiệp UMinhThượng",
      conf="medium", note="Gò Quao and Vĩnh Thuận to Chương Thiện; U Minh Thượng straddles it.",
      src=[VI_TINH, u(VI, "Chương Thiện")]),
 dict(id="chuong-thien", name="Chương Thiện", plain="Chuong Thien", kind="province", capital="Vị Thanh", ctz="IV",
      d="HậuGiang: VịThanh VịThuỷ LongMỹ LongMỹ(Thịxã); BạcLiêu: HồngDân; KiênGiang: GòQuao VĩnhThuận",
      conf="medium", note="Created 24 Dec. 1961. vi W lists today's communes: Vị Thanh, Long Mỹ, Vị Thủy, Hồng Dân, Gò Quao, Vĩnh Thuận, part of "
                          "U Minh Thượng and of Phụng Hiệp (Hòa An, Phương Bình). Area 2,150 km² against 2,292 (1971).",
      src=[u(VI, "Chương Thiện")]),
 dict(id="phong-dinh", name="Phong Dinh", plain="Phong Dinh", kind="province", capital="Cần Thơ", ctz="IV",
      d="CầnThơ: BìnhThuỷ CáiRăng CờĐỏ NinhKiều ÔMôn PhongĐiền ThớiLai; HậuGiang: ChâuThành ChâuThànhA PhụngHiệp NgãBảy",
      conf="medium", note="Phụng Hiệp straddles Chương Thiện. Area 1,847 km² against 1,623 (1964).",
      src=[VI_TINH]),
 dict(id="ba-xuyen", name="Ba Xuyên", plain="Ba Xuyen", kind="province", capital="Khánh Hưng (Sóc Trăng)", ctz="IV",
      d="SócTrăng: ChâuThành CùLaoDung KếSách LongPhú MỹTú MỹXuyên NgãNăm SócTrăng ThạnhTrị TrầnĐề",
      conf="high", note="After Bạc Liêu's re-creation (8 Sept. 1964): the pre-1956 Sóc Trăng. Vĩnh Châu to Bạc Liêu. Area 2,838 km² against 2,684 (1964).",
      src=[u(VI, "Ba Xuyên")]),
 dict(id="bac-lieu", name="Bạc Liêu", plain="Bac Lieu", kind="province", capital="Bạc Liêu", ctz="IV",
      d="BạcLiêu: BạcLiêu ĐôngHải GiáRai HoàBình PhướcLong VĩnhLợi; SócTrăng: VĩnhChâu",
      conf="high", note="Re-created 8 Sept. 1964: Giá Rai, Phước Long, Vĩnh Châu, Vĩnh Lợi. Area 2,648 km² against 2,632 (1964).",
      src=[u(VI, "Ba Xuyên"), VI_TINH]),
 dict(id="an-xuyen", name="An Xuyên", plain="An Xuyen", kind="province", capital="Quản Long (Cà Mau)", ctz="IV",
      d="CàMau: CàMau CáiNước ĐầmDơi NămCăn NgọcHiển PhúTân ThớiBình TrầnVănThời UMinh",
      conf="high", note="Today's Cà Mau.", src=[u(EN, "An Xuyên province"), VI_TINH]),
 # ---------------- not a province
 dict(id="con-son", name="Côn Sơn", plain="Con Son", kind="special", capital="Côn Sơn", ctz=None,
      ctz_note="Under the Navy command from 1 June 1961 (vi W 'Quân đoàn III'); in no corps zone.",
      d="", conf="high",
      note="Province abolished 24 Apr. 1965; then the Côn Sơn Administrative Base under the Interior Ministry (vi W 'Côn Đảo'). "
           "GADM 4.1 lacks Côn Đảo: the islands are Natural Earth's (admin-0).",
      src=[u(VI, "Côn Sơn (tỉnh)"), u(VI, "Côn Đảo")]),
]


def districts(unit):
    out = []
    for part in unit["d"].split(";"):
        if not part.strip():
            continue
        p1, names = part.split(":")
        out += [(p1.strip(), n) for n in names.split()]
    return out
