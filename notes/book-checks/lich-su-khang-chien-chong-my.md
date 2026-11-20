# Lịch sử kháng chiến chống Mỹ, cứu nước (w.lich-su-khang-chien-chong-my): book check

The official history of the Institute of Military History, 9 vols. (the second edition, Chính trị quốc gia – Sự thật, Hà Nội, 2013). The series card is `w.lich-su-khang-chien-chong-my` (`works/l.yaml`, made by the first reader of batch 16, Nov. 14, 2026); the two one-volume cards (`w.lich-su-khang-chien`, `w.al-lich-su-khang-chien`) are left for the lead.

## Reader 4 (vols. I–III), Nov. 19

Reader 4, batch 16 (`notes/briefs/batch16-drv.md`), resuming the run stopped Nov. 14. Patch `inbox/2026-11-14-b16-lskc-1.yaml` (patch name `2026-11-14-b16-lskc-1`): the predecessor's 37 new entries and 66 ops (its `partial-patch.yaml`, read against the volumes and carried over; the one cite of the Bến Tre rising to the Tua Hai entry, cal.1960-01-26.vietnam, dropped for its own entry) and this run's 272 new entries, 30 cites and 8 variants, with the 98 `place-key` ops its places need. Scripts and specs: `notes/wip/b16-lskc-1/` (`ops/z*.py`, `scripts2/`: the DSL, the claims in `ids.tsv`, `build.sh`).

### The copies and the text

Fetched into a new scratch directory by the brief's curl form (deleted at the end). Title pages: Bộ Quốc phòng, Viện Lịch sử quân sự Việt Nam, *Lịch sử kháng chiến chống Mỹ, cứu nước (1954–1975)*, "Xuất bản lần thứ hai", Nhà xuất bản Chính trị quốc gia – Sự thật, Hà Nội, 2013.

- Vol. I, *Nguyên nhân chiến tranh* (Drive `12mUcq536bZ6jZWo7jNRCuuruXHUV4w0Y`, 207 PDF pages; book pp. 5–203, contents at 202–03): ch. 1–3, the situation after Điện Biên Phủ, Vietnam in American strategy, peace on the base of independence and unity. Led by Lt. Gen., Prof. Hoàng Phương; chief editor Col. Nguyễn Văn Minh. Its 1960 part: nothing (the three dated mentions of 1960, I, 6, 52 and 121, are totals and plans).
- Vol. II, *Chuyển chiến lược* (Drive `1n5I87g-J1vd-YfnVXWwLDcjRsQUbfDl4`, 426 PDF pages; book pp. 5–403): ch. 4–8, July 1954 to the end of 1960; ch. 8, *Đồng khởi – bước mở đầu chiến tranh cách mạng ở miền Nam*, II, 311–89, is the year 1960 in the South. Authors Đỗ Xuân Huy, Hồ Khang, Nguyễn Huy Thục, Nguyễn Văn Minh, Nguyễn Xuân Năng.
- Vol. III, *Đánh thắng chiến tranh đặc biệt* (Drive `1NO-cIOkmT8YsO4wdlw2TvDBX_jojt1wi`, 474 PDF pages; book pp. 5–455): ch. 9–13, 1961 to mid-1965: ch. 9 the American "special war" and the Party's decisions (III, 7–56); ch. 10 the North, its economy and defense (57–136); ch. 11 to the battle of Ấp Bắc (137–240); ch. 12 1963 and the coup of November (241–326); ch. 13 1964 to July 22, 1965, the end of the Đồng Xoài campaign (327–438); conclusion 439–46. Led by Lt. Gen., Assoc. Prof. Nguyễn Đình Ước; chief editor Col. Nguyễn Văn Minh; authors Ngô Văn Bính, Hồ Khang, Trần Tiến Hoạt, Đỗ Xuân Huy, Nguyễn Huy Thục, Nguyễn Xuân Năng.
- Span covered by this run: Jan. 6, 1960 (the calendar's start) to Aug. 5, 1965 (the Liên Chiểu raid, III, 434, the last dated act of the volume).

The text layer is in the TCVN3 encoding; `python3 -I tools/vn/vkd2txt.py` converts it (as for *Văn kiện Đảng toàn tập*). One book page to a PDF page. Book page = PDF page − 2 in vol. I; in vol. II − 1 to PDF 193 and − 21 after the unnumbered plates (PDF 194–213); in vol. III − 1 to PDF 137 and − 17 after the plates (PDF 138–153). Cites give the book's page, read from the folios (`scripts/annot.py`).

### How it was read

All dated sentences of II, 311–89 (ch. 8) and of III, 7–440 were pulled by a script (a sentence with a day–month–year, a month–year, "ngày", "tháng", "đêm", a year of 1950–69) and read in full with their page; the whole page was read where an entry needed its context (about 60 pages: III, 9, 43, 49–50, 95–96, 120, 150, 180–81, 183, 189, 192–93, 205–09, 243, 250–52, 275, 279–80, 336, 396, 431–34; II, 296, 316, 351, 353–54). Undated narrative between the dated sentences was not read page by page: what the history says without a date marker in its sentence (a unit's make-up, a map's account) is not in the entries. Vol. I: the date hits only. Vol. II before ch. 8: the date hits of 1960 (II, 159–60, 183, 211, 296). The two volumes' notes and bibliographies (II, 395–403; III, 447–54) were not worked: no witnesses were registered and no "To check:" lines written for the archive items the notes name (the Institute's archive, numbered TW 816, TW 1159, TWC 17; the Party History Boards of Quảng Ngãi and Bình Định; *Nhân Dân*; the Pentagon Papers as quoted). This is the notes pass of R3, step 3, undone for this run.

### What was entered

- 309 entries in the patch, 37 the predecessor's and 272 this run's (49 of 1960, 61 of 1961, 44 of 1962, 62 of 1963, 56 of 1964, 37 of 1965): 246 with a `place`, 17 with a `time` and 41 with a `time_range` and band; 70 cites, 28 variants (the history's account of an act the calendar holds from the American side: the Tân Sơn Nhứt ball-field bombing of Feb. 9, 1964; Polei Krong and Nam Đông, July 1964; the Maddox, Aug. 2, 1964; the Qui Nhơn hotel, Feb. 1965; the Palace bombing of Feb. 27, 1962; the crowd of June 16, 1963), 3 checks, 3 `also` ops. Thread `vietnam-hanoi`, `also` `vietnam-operations`, `vietnam`, `vietnam-34a`, `laos`, `vietnam-air-war` as the act bears. The Buddhist crisis of 1963 (8 entries, thread `vietnam`), the "general offensive plan" of Feb. 1963, the pacification plan Chiến Thắng of Apr. 1, 1964 and Diệm's visit to Bến Tre (Mar. 1960) are the Saigon side's acts, tagged `polity:rvn`, entered because the history dates them and the calendar lacks them.
- The Party's and the army's secret acts take `vis:only:drv` with "Made public: 2013." (the second edition; the first, 1995–2012, circulated in the army only: R27). Battles and the Front's public acts carry no ruling.
- Places: the gazetteer's key where it had one; 98 new keys (the provinces, districts, posts and bases the history names), zone `Asia/Ho_Chi_Minh` for the South, `Asia/Bangkok` for the North. Where the entry's place is only a subject of the text (a city named as the target, "Saigon" in a Saigon commando act of another city, a strategic hamlet's name) the entry is tagged `ok:fields-place`; where an hour or a part of the day belongs to the second day of a span, `ok:fields-time`.
- Times: the hours the history gives (Bến Tre, Jan. 17, 8 a.m.; Nà Niêu, Aug. 30, 1962, 7 a.m.; Hiệp Hòa, Nov. 22, 1963, 1:00 a.m.; Cái Nước, Sept. 9, 1963, 3:40 p.m.; Ba Gia, July 5, 1965, 1:45 a.m.; and others) as `time`; "the night", "the morning" as `time_range` with the band `night` or `morning`.

### Passed over

How the list was made: the dated sentences of the extraction, set against the entries by date. Rows are by kind, with pages, because of their number.

- Out of the brief (R18, outside the span, R1): events before Jan. 6, 1960: the decree putting the Constitution in force, Jan. 1 (II, 159); the Bến Tre committee's enlarged meeting, Jan. 1 (II, 319; named in the Bến Tre entry); the Gò Tháp tower, Jan. 4 (II, 324); the Kiến Phong, Phú Yên and Rạch Giá acts of Nov.–Dec. 1959 (II, 313–14, 318, 380).
- Not events: the year-end and period tallies (III, 100, 166, 200–02, 213, 256–58, 283–84, 304, 361, 393) and the stock of the American effort in men and arms (III, 23–24, 241–42, 333–34): each is a figure of a year or of a period, no day.
- Not entered, for want of time (not an R18 ground; the next run's): the smaller dated acts of the provinces in ch. 11–13: III, 138–40 (the 1961 demonstrations other than those entered), 154 (Thủ Dầu Một, July–Oct. 1961), 162 (the Gia Trúc pass), 171 (Bình Dương, Mar.–June 1962), 173 (Apr. 20, 1962, Điện Ngọc), 185 (Oct. 26 and Dec. 1962), 186–87 (strikes of 1962), 244–46, 253–54, 258–62, 269–73 (Bến Tre, Kiến Tường, Gò Công, Long An 1963 beyond the entries), 280–83, 294–301 (eastern Nam Bộ, 1963), 357–61 (1964, the provinces), 387–93 (Dec. 1964, Region 5), 395–403 (Jan.–Mar. 1965: Jan. 17 Region 6, Jan. 20, the Hoài Đức and Tánh Linh acts), 429–35 (June–July 1965, the minor acts) and the American Air Force's days of Feb. 7–Apr. 4, 1965 beyond those entered (III, 403–13).
- Already in the calendar, no cite yet made: the history's accounts of the American and Saigon acts: III, 14–16 (NSAM 52; the Staley mission, June 19, 1961), 25–26 (the tactical zones; the strategic-hamlet program, Apr. 1962), 168 (the Thompson mission, Sept. 17, 1961), 314–15 (Lodge; Kennedy, Sept. 2, 1963), 320 (the coups of Jan. 30, 1964 to May 1965), 321 (Nov. 22, 1963), 329 (Honolulu, Nov. 20, 1963; Plan 34A), 331–32 (Taylor, Jan. 22; the Mar. 8–12 trip), 362–65 (Feb. 17, Mar. 2 DESOTO, Apr. 17, 1964), 364–69 (the Tonkin Gulf: Aug. 2, 4, 5, 7 beyond the cites made), 394–95, 403–13 (Flaming Dart, Rolling Thunder), 411–13.

### Leads (R50)

Foreign.
- The Institute's archive items the notes quote: the Politburo resolution TW 1159 (Sept. 1964), the eleventh plenum's TW 816 (Mar. 1965), the Region's TWC 17 (Nov. 1959), the Party History Boards of Quảng Ngãi, Bình Định and Phú Yên: not held; look in the Institute's archive or in *Văn kiện Đảng toàn tập*, vols. 25–26.
- The first edition (1995–2012, for the army) of vols. I–III, not read: its dates may differ from the second's.
- The Gia Trúc pass ambush by Battalion 120 with Pi Năng Tắc (III, 162), undated; the boats of Bến Tre, Cà Mau and Trà Vinh of 1961 (III, 145–46) whose sailing days the history does not give.
- The American record of the commando acts of Saigon (the Bambu restaurant, Jan. 9, 1964; the Caravelle, Aug. 25, 1964; the Việt Cường Hotel, Feb. 9, 1965; the MACV and air force club attacks, Jan. 29 and Feb. 12, 1965): to be matched to the calendar's own entries (some may be there under different days).
- The Hòn Mê and Hòn Ngư raid (July 30–31, 1964), the Aug. 2 and 4 events: variants made only where the calendar holds them.

### Persons with no name entry

Named in `c` and in "Names:", not tagged: Nguyễn Thị Định, Đỗ Cao Trí (as the history names him, Gen.), Phan Văn Hược, Vũ Tấn Hạt, Bùi Đức Thành, Huỳnh Công Thân, Nguyễn Hoài Phô. Named in `c` only: Tạ Quang Tỷ, Nguyễn Đệ, Phạm Vạn, Đặng Văn Thanh, Lê Văn Một, Bông Văn Dĩa, Tư Mâu, Hồ Văn Trí, Lê Duy Khoái, Phạm Phú Quốc, Nguyễn Văn Cử, Tô Đức Hùng, Đỗ Văn Dĩnh, Vũ Bá Linh, Nguyễn Thanh Xuân, Nguyễn Thị Minh Nguyệt, Lâm Sơn Náo, the Buddhist leaders (Thích Tịnh Khiết, Thích Quảng Đức). The predecessor's entries name others (Trần Văn Quang, Trần Lương, Nguyễn Hữu Xuyến and the Region commanders) in their Names lines.

### Doubtful

- Misprints in the volume: III, 249 "nửa cuối năm 1968" (1963); III, 47 "9-2-1961" for the ceremony of Q761's battalions, against the regiment's founding in July 1961 (entered Feb. 9, 1962, with a Check); III, 248 the Đức Phổ night of Apr. 28 against a morning of Apr. 24; III, 186 "17-2-1961" in a passage on 1962 (entered Feb. 17, 1961, Check); III, 309 "Sáng ngày 1-5" for a meeting of the Buddhist leaders at Từ Đàm; II, 363 and 364 give the Central Nam Bộ rising's day as Sept. 23, then Sept. 24 (both entered).
- Entries of the passage with two dates (a span of days with the first day's time, a "Check:" naming the second) are marked as such in each note; the owner's rule of Oct. 20 (one event an entry) was met by splitting where the history gives each day its own act.
- Figures (losses, aircraft shot down, men out of action) are the history's own and are entered as such; the American record not read for them, except where a variant was made on an entry the calendar holds.
- "Made public: 2013" for acts the history took from the Institute's archive: the history does not say whether the item was printed earlier.
- The `place` of the Institute's own units (a Region, an Interzone) is left unset where the history names the place of the unit's base only as a subject.

## Reader 5 (vols. IV and V), Nov. 19

Reader: batch 16, reader 5, resuming reader 5's first run of Nov. 14 (its 1965 ops carried over and checked against the pages, its 34 claimed ids all used), Nov. 19–20, 2026 (after 5 p.m. Pacific on a weekday). Patch: `inbox/2026-11-14-b16-lskc-2.yaml` (patch name `2026-11-14-b16-lskc-2`, the name the ledger claims stand under), 322 ops: 226 new entries (by year of `date`: 1964: 4, 1965: 44, 1966: 54, 1967: 46, 1968: 78), 55 cites, 9 variants, 4 checks on entries the calendar held, 28 place-keys. Of the new entries, 146 carry a `place:`, 62 a `time` or `time_range`, 15 an `at:`. `./bib patch-check`: 0 errors (the warnings are the "one event?" and "a duplicate of" flags on same-day, same-thread entries, each a separate act); `./bib fields --patch`: 0 findings. Not merged, not committed.

### The volumes

- Vol. IV, *Cuộc đụng đầu lịch sử* (The historic encounter), Drive `1mdEqLeFUfNJBPc4OB2QVMIz5a4BKvwsh`. Title page: "Xuất bản lần thứ hai", Nxb. Chính trị quốc gia – Sự thật, Hà Nội, 2013; the Ministry of Defense's Institute of Military History; chief of content Trung tướng Nguyễn Đình Ước, editor Đại tá Nguyễn Văn Minh. The publisher's note says it covers chapters 14–18, the years 1965–1967, "on both South and North". Chapter 14, the limited war and the first encounter (pp. 9–80); ch. 15, the first dry-season counteroffensive 1965–66 (81–150); ch. 16, the 1966 summer–autumn offensive and the Route 9–North Quảng Trị front (151–226); ch. 17, the dry season 1966–67, Junction City and the pacification pincer (227–342); ch. 18, the North in war, 1965–67: construction, air defense, transport (343–448); conclusion 449–456; bibliography 457–464; contents 465–467. 484 PDF pages.
- Vol. V, *Tổng tiến công và nổi dậy năm 1968* (The general offensive and uprising of 1968), Drive `1t4V7LDjJ02RsPv3iHHZp8WQhVghmFfl4`. Same press, 2013, second edition; chief of content Đại tá, PGS. TS. Trịnh Vương Hồng. Ch. 19, the turn to a decisive victory, the Politburo's decision, and the 1967 autumn–winter campaigns (9–77); ch. 20, the Tết offensive (78–167); ch. 21, the summer–autumn waves (168–288); ch. 22, diplomacy and the Paris talks (289–343); conclusion 344–352; bibliography from 353. 375 PDF pages. The volume ends with Nov. 1968 (a line on Nov. 25, 1969, V, 342).
- Both are TCVN3 text layers, converted with `tools/vn/vkd2txt.py` page by page (`pdftotext -layout`, the FIX table, iconv from TCVN5712-1); the headings in the capitals font come out in mixed case. One book page to a PDF page. Book page = PDF page − 1 in vol. IV from the preface to p. 47; the plates (maps and photographs, no text layer) shift it to − 3 from p. 49 (PDF 52), then − 15 from p. 129 (PDF 144); in vol. V − 1 to p. 8, − 2 from p. 9, − 3 from p. 97 and − 11 from p. 225. Every cite gives the book page printed in the running head, read from the folio, not computed. The text is on the series card `w.lich-su-khang-chien-chong-my`, cited "IV, 123".
- The 2013 second edition is the first on the open market; the card notes that the first edition circulated in the army only. Every secret act the history prints from an archive of the Institute is "Made public: 2013." with the first-edition printing not established (a lead).

### What was entered

Every event-day below is `thread: vietnam-hanoi` (its chief thread), `also:` the other threads it bears on, or `thread: vietnam-tet`, `laos`, `vietnam-khe-sanh` where the history's act is the DRV's side of a battle the calendar keeps under that thread. `polity:drv` throughout (the NLF's and the Liberation Army's acts are the DRV's: the owner, Nov. 11), `polity:us` where `c` names American units outright, `polity:rvn` and `laos` where it names those; `vis:only:drv` and "Made public: 2013." on a Politburo, Military Party Committee, COSVN, Region or Front decision, a unit's formation, and any act the history prints from an archive; none on the National Assembly's acts, Hồ Chí Minh's public appeals, a battle's fighting, a public statement. The history's day-of-month dates are cited as printed; a year, month, "early", "late" are entered with `at:` (set by `loose.at_for`) and "Check: the day". Clock times are the history's, with `time:` on the first act's hour and `time_zone` the gazetteer's zone of the place (Asia/Ho_Chi_Minh for the South, Asia/Bangkok for the North); the history does not say whose clock, and each such entry says so in its Check. A part of the day is `time_range` with its band and `range_basis: record`. The place is on the entry only where the history places the act (the Politburo's seat, a battle's named ground); a place named only as a subject takes `ok:fields-place`.

The cover: the DRV's and the Party's leadership decisions and organs (the National Defense Council of Jan. 1965, the Assembly's acts of Apr. 1965, the partial mobilization, the Military Party Committee's resolution of Feb. 1966 and its six modes, the Politburo and Military Committee of Apr. 1966 (the Trị–Thiên split), June 1966 (B5 front), Oct. 1966, Jun., Oct. and Dec. 1967, Apr. 24, Jul. 24–25 and Aug. 1968, the Fourteenth Plenum at Kim Bôi, Lê Duẩn's letter of Jan. 1967, the Central Office's resolution and conferences, Command 500, the divisions formed in 1965 and 1966, the fronts, the Foreign Minister's instruction of Jun. 3, 1968 and the DRV's side of the talks); the battles and campaigns the history dates (Núi Thành, Vạn Tường, Plei Me and Ia Đrăng, Bàu Bàng, Đất Cuốc, Việt An, Củ Chi, the north Bình Định and Quảng Ngãi sweeps of early 1966, Hastings, Attleboro, Sa Thầy, Cedar Falls, Junction City, the first artillery fire from the North's bank, Bình Long–Phước Long and Đắk Tô, the Tết offensive in Saigon, Huế, Đà Nẵng, the second wave, Khe Sanh and Route 9, the third wave); the North's air defense and transport by date; the sea supply ships of Group 125 (Mar. 1967, Jun. 1967, Feb. 1968); the Tết fighting in the provincial towns of Region 5, the Highlands and the delta on the first days (Buôn Ma Thuột, Quy Nhơn, Quảng Ngãi, Phan Thiết, Đà Lạt, Biên Hòa, Mỹ Tho, Bến Tre, Cần Thơ, Vĩnh Long); Làng Vây; the diplomatic acts the history dates (the Indochinese People's Conference, the Front's five points, Havana, the Russell Tribunal, the release of three prisoners, Trinh's words of Dec. 29, 1967).

Cites and variants: the history's account is cited, with a variant where it differs, on the American side's entries already held: Vạn Tường (the history's 900 out of action, 22 vehicles, 13 aircraft), Ia Đrăng (Nov. 16 and 17), Củ Chi, the first artillery action across the Bến Hải (Mar. 20, 1967: 2,000 rounds on Dốc Miếu against the calendar's thousand), the Fourteenth Plenum (the calendar has it at Hanoi, the history at Kim Bôi, Hòa Bình), Lê Đức Thọ's arrival in Paris (the history: mid-June; the calendar: Jun. 3), the first session in Paris (the history: the Hall of International Conferences, avenue Kléber; the calendar: the Hotel Majestic), Khe Sanh (the history's Jan. 20 opening; the calendar's first attack Jan. 21), Nam Bac (the history: attack Jan. 12; the calendar: falls Jan. 14), the Twelfth Plenum (the history: opens Dec. 27, the volume of Party documents: Dec. 21–27), and the embassy raid (the history says the sappers held the ground floor and went on to the second and third floors; the American record read has them in the compound only; a Check on the entry).

### The rules used

The brief of batch 16, batch 12's (the foreign skeletons) and the reader's brief: R5 (every dated event the history treats is an entry; only R18 takes any out), R25a (the date, `at`, time, place on every entry the text gives them for), R27 (Made public, the volume's year), R29 (the bibliography: the work's cite first; no primary record read, so "To check:" only where a document is named), R44 and R50 below. The owner's rulings of Nov. 15: Hanoi's commemorations and provincial matters stay in. One event, one entry: a battle's several named actions on one day are separate entries where the history gives each its own unit and hour (the Saigon commando squads, Huế's Mang Cá and Tây Lộc), and a run of small actions the history lists in one sentence is one entry with the run named and a Check (Cánh Trắng II, Sa Thầy). Vietnamese names with full diacritics; Americans as the series spells them. No source text beyond a few words is quoted, in translation.

### Pages read

Read in full (the pages cited with their detail): vol. IV 33–64 (the preparation of 1965; the first encounters), 91–94, 185–192, 196–198, 206–209, 212, 219–224, 233–235, 281, 392, 396–397, 404–410, 422–426; vol. V 30–44, 48–51, 65–70, 78–82, 85–88, 95–98, 121–122, 173–176, 222–223, 227–229, 233–236, 239–241, 266–267, 274, 281, 283, 323, 330–341. By the dated sentences of every page (a script lists each sentence with a day, month or year in it, footnotes cut, and the sentence is read in its page when it bears on an event): vol. IV 9–32, 66–80, 81–150, 150–226, 227–292, 343–448; vol. V 9–29, 45–64, 83–117, 118–226, 230–288, and, for the diplomacy of 1965–68, 289–341. Not read: vol. IV 293–342 (the dry season in Khu 5, the delta and the Mekong; the political struggle, 122–150), the American decisions of 1964–65 at IV, 9–32 (already in the calendar from the American side), the 1965–67 diplomacy at V, 289–329 (dated sentences only), the military history's summaries (IV, 449–456; V, 344–352), the lists of units' honors, the bibliography. No notes (footnotes) registered: the history's footnotes cite the Institute's archives (*Lưu trữ Phòng Khoa học–Công nghệ và môi trường Quân khu 5*; *Viện Lịch sử quân sự*), the Pentagon Papers in the Vietnamese translation, Westmoreland, Johnson, and AFP and Reuters dispatches; none is a witness registered (R35: no witnesses file, no by-work edges); each is named in the entry's note only where the entry rests on it.

### Passed over (R44)

By kind. R18's grounds do not apply to any of these; each row is a passed-over item for the owner's ruling, given with its pages and why.

- *Small actions the history lists in a run, left for a next run* (no R18 ground; time): IV 156–184 (the rainy-season actions of April–September 1966 in the provinces, about 70 engagements of company or battalion size with date and unit: Long Phước, Trảng Bàng, Thủ Đức, Phú Yên, Bình Định, Quảng Ngãi, Quảng Nam, Bình Thuận, Kon Tum, the delta); IV 284–342 (the dry season 1966–67 in Quảng Ngãi, Quảng Nam, Lâm Đồng, Long An, Bến Tre, Mỹ Tho, Cần Thơ); IV 100–121 (about 25 actions of Jan.–Mar. 1966 in Phú Yên, Bình Định and Quảng Ngãi: Jan. 20 Thạnh Phú, Jan. 26 Phú Phong, Jan. 30 Phú Thọ, Feb. 3–4 Núi Lạc and Ngọc Lâm, Feb. 6–9 Hòa Thịnh, Feb. 20–23 Tam Quan and Bồng Sơn, Mar. 17–28 Tịnh Hà, An Hòa, Hội Đức, Phước Lộc, Lâm Lộc, Mar. 11 A Sầu, Feb. 28 Tân Kim); V 123–126, 146–152, 156–172 and 183–224 (the Tết offensive in the other provincial towns after Jan. 31 (Pleiku, Kon Tum, Hội An, Quảng Nam, Châu Đốc, Sóc Trăng, Cà Mau, Trà Vinh, Sa Đéc, Long Xuyên), the renewed attacks from Feb. 17 to Mar. 15 and the second wave in the Central Highlands, Khu 5, Mekong Delta and Eastern Nam Bộ cities, Feb.–June 1968: about 80 engagements); V 242–265 and 268–273 (the third wave in the delta, Khu 5, Khu 6, Huế; Oct.–Dec. 1968); IV 52 (Thuận Ninh Sept. 18, Cát Sơn Oct. 10, Cát Hiệp Oct. 14, 1965 were entered; the history gives them one line each).
- *Dated items in the political-struggle passages, left for the next run* (IV 122–150): the Buddhist and student movement of Đà Nẵng, Huế, Saigon and Đà Lạt in Mar.–May 1966 (Mar. 12 the first meeting at Huế, Mar. 30 the march of 100,000, Apr. 2–3 the march of Huế's soldiers, Apr. 4 the Marines at Đà Nẵng, Apr. 7 the sixth night, Apr. 21 the shooting of four pupils, May 15 six battalions to Đà Nẵng; Jun. 17, 1966 Kỳ's devaluation decree): all are in the calendar from the American side under `vietnam-struggle`; the history's account is to take a cite on each.
- *Figures with no day* (R25: a figure is kept with its page, but a year's tally is not an event): IV 389 (834 aircraft shot down in 1965), 397 (1,005 by Apr. 30, 1966), 400 (773 in 1966), 419 (2,680 to the end of 1967), 401 (the CIA's count of dead in the North), 380, 383, 446; V 28, 52, 286 (425 aircraft in Zone 4, Apr.–Oct. 1968), 239 and 223 (the campaign tallies: entered on the closing day), 45 (the aid of 1968).
- *American decisions of 1964–65 the history reports* (IV 9–32; already in the calendar from the American side, each a cite to add): the Aug. 5, 1964 raids, the Nov. 24, 1964 working group, Feb. 8 (the Hawk battalion at Đà Nẵng), Mar. 2 (Rolling Thunder), Mar. 8 (the Marines), Apr. 1, Apr. 6 (NSAM 328), Apr. 7 (Baltimore), May 1 (Westmoreland's plan), Jun. 11–19 (the Saigon junta), Jul. 17 (the 44 battalions), the 1st Cavalry and 1st Division's moves of Jul.–Dec. 1965, the *Intrepid*. Not cited for time.
- *Out of the brief* (R18): none; the history's accounts of Saigon's inflation, corruption and prostitution (IV 123–128) and of American politics (V 9–16) are the history's argument and carry no dated act of the DRV; the American acts in them are in the calendar.

### Leads (R50)

*Foreign.* (1) IV 33–34: Nguyễn Chí Thanh, Trần Văn Trà, Chu Huy Mân, Hoàng Văn Thái, Lê Trọng Tấn, Hoàng Minh Thảo and others sent into Nam Bộ, Khu 5 and the Highlands: no date but "before the Americans came"; look in the Văn kiện Đảng toàn tập's vol. 25–26 for the Politburo's decision. (2) IV 43: the Central Office's fourth conference, held after Hồ's appeal of July 20, 1965; its date and resolution not given. (3) IV 60: the awards to the units of Plei Me–Ia Đrăng, two First Class Military Exploit Orders, Nguyễn Chí Thanh's words; no day. (4) V 81: Hồ Chí Minh's New Year poem, read over the radio at Tết, no day or hour. (5) V 342: the first formal session of the four-party conference printed "ngày 25-11-1969" at 10:25 (the calendar has Jan. 18, 1969): a misprint for Jan. 1969, or another session; check the calendar's Jan. 18–25, 1969. (6) IV 198: "ngày 206-1966" for the B5 front's enlarged conference, read "Jun. 20" and not entered. (7) IV 447: the Russell Tribunal's first session printed "May 2–13, 1966" at Stockholm (the Tribunal sat in May 1967): not entered, to settle against the calendar. (8) IV 281: "Đêm 5 rạng ngày 4-6-1967", entered on Jun. 4–5 with a Check. (9) The Institute's first edition (1995–2012) of the same text: the first-edition page of each secret act, for "Made public"; the card's note says only that it circulated in the army.

*The Executive and the series' people.* Persons the history names with no name entry in the series: see below.

### Persons named with no name entry (named in `c` and "Names:", not tagged)

Phạm Hùng, Trần Văn Quang, Hoàng Minh Thảo (in "Names:"); named in `c` only, with no name entry looked for: Nam Long, Quách Sỹ Kha, Chu Phương Đới, Nguyễn Tiến Lợi, Giáp Văn Cương, Trần Quang Khanh, Trương Chí Công, Hồ Sỹ Thản, Đậu Văn Phơn, Lê Hữu Trữ, Bùi Thanh Vân, Hoàng Minh Thắng, Ngô Thành Vân, Trần Văn Lém, Nguyễn Văn Tăng, Đỗ Tấn Phong, Đàm Văn Ngụy, Nguyễn Hữu An, Nguyễn Văn Linh, Lê Ngọc Hiền, Hà Văn Lâu (he has an entry, `ha-van-lau`; not named in a Names line), Đinh Đức Thiện, Song Hào, Trần Quý Hai, Hoàng Anh, Lê Trọng Tấn, Trần Sâm, Nguyễn Đôn, Lê Quang Đạo, Lâm Văn Kiếm, Phan Như Cẩn, Phạm Ngọc Lan; Americans without entries: Bunker, Abrams, Kinnard, Clifford, Vance (Westmoreland, Johnson, Harriman, Thiệu and Kỳ were tagged by hand from the series' name keys).

### Doubts

- The page numbers: vol. IV's plates and vol. V's printed offsets (above); every cite is from a printed folio, but a page of text lost between a plate and the next folio (IV 49–51, 129–143; V 97–100, 225–236) would shift a cite by a page. The tables are not in the PDF text layers (the maps and photographs).
- Dates printed with a slip: IV 198 "ngày 206-1966"; IV 281 "đêm 5 rạng ngày 4-6-1967"; IV 447 the Russell Tribunal's year; V 342 "25-11-1969". Each entered with a Check or not entered.
- Two figures disagree inside the history: the American 173d's Jan. 1, 1966 Marauder (IV 95) and its Jan. 8 date (IV 84); the history's 1965 divisions (IV 37 n.1) and the Party's history's; the Fourteenth Plenum's place and days (V 43).
- The history's losses are its own and unchecked, its American "admissions" cited without source: where the entry carries them, "Check" says so.
- A battle in the history may be one the calendar holds under another name or day; each cite and variant was set by the day and the ground, not by the operation's name, and a few may belong to a neighbouring day (Plei Me Oct. 23–25; Ia Đrăng Nov. 14–17).
- `./bib check`'s `ok:` tags: `ok:fields-place` is on about one third of the entries (a decision with no place, or a place named as the subject or the target), `ok:fields-time` on the entries whose hour is the battle's end or a later day's.

### Where this run stopped

Vol. IV: ch. 14–15 (to p. 121), ch. 16 (151–226, leadership and Route 9 front), ch. 17 (227–292, the dry season 1966–67 in Eastern Nam Bộ), ch. 18 (343–448, the North). Vol. V: ch. 19 (9–77), ch. 20 (78–117, Saigon, Huế, Đà Nẵng, Quảng Trị), ch. 21 (225–241, 250–251, 266–267, 274, 281–283), ch. 22 (289–341, the DRV's side, dated sentences). A next run starts with the passed-over rows above: IV 293–342 and 100–150 first, then V 123–126, 146–172, 183–224, 242–265, and the 1965–67 diplomatic dated sentences at V 289–329 not entered.

## Reader 6 (vol. VI), Nov. 19

Reader 6, batch 16 (`notes/briefs/batch16-drv.md`), resuming the run stopped Nov. 14 (its predecessor's work in `notes/wip/b16-lskc-3/`: 25 adds, 4 cites, 2 variants, all for 1969, carried over with the R25a fields added). Patch `inbox/2026-11-14-b16-lskc-3.yaml` (patch name `2026-11-14-b16-lskc-3`): 120 new entries (the predecessor's 25 and 95 of this run's), 8 cites, 3 variants, 32 `place-key` ops (`bu-dop` is also in `b16-lskc-2`, the same row). Scripts: `notes/wip/b16-lskc-3/` (the predecessor's) and `notes/wip/b16-lskc-3/scripts2/` (this run's: `lib.py` the DSL, `e1.py`–`e5.py` the entries by page range, `pre.py` the carried ops with their fields, `join.py` the patch, `ids.json` the claims by key; run in that directory, `python3 e1.py` ... `join.py`, which writes the patch).

### The volume

Vol. VI, *Thắng Mỹ trên chiến trường ba nước Đông Dương* (Victory over the Americans on the battlefields of the three Indochina states), "Xuất bản lần thứ hai", Chính trị quốc gia – Sự thật, Hà Nội, 2013; chief editor Trịnh Vương Hồng, author Hồ Khang with others. Fetched by the brief's curl form (Drive id `1zggkITSSkyz-9er0juH5iyNy1i41Uqj-`) into a new scratch directory; 403 PDF pages; the text layer is TCVN3 (`iconv -f TCVN5712-1`, the predecessor's `pages.py`), the book's folio read from each page's printed number (`compact.py`): chapter 24 opens at p. 69, chapter 25 at 163, chapter 26 at 238, the contents at 389–90, as the contents say. One book page to a PDF page. Cited as VI, folio.

Span: chs. 23–26, 1969 to the end of 1971 (ch. 23, the American strategy, 1969–71; ch. 24, the South, 1969 to mid-1970; ch. 25, the North, route 559 and the diplomacy, to 1971; ch. 26, Laos, Cambodia and the three regions, 1970–71). The brief's span, to Dec. 31, 1969, lies inside VI whole, so vol. VII was not fetched. Dates of 1970 and 1971 are out of the calendar's span (R18, first bullet) and are not entered, except the 18th plenum (the history gives "Jan. 1970") and Laird's speech of Jan. 14, 1970, which fall inside the calendar's span to Jan. 19, 1970.

### Pages read

In full: pp. 69–162 (ch. 24: the South after Tet, the Politburo's May session, the three phases of 1969, the Congress and the PRG, the winter phase, the cities, the 18th plenum); 163–177; 190–197 and 205–219 (the North's armed forces, route 559, the pipeline); 221–231 (Paris, 1969–71); 238–243 and 247–250 (Laos, Cambodia). By the dates only (every sentence with a day, month, season or year, by `sents.py`), not read through: pp. 9–68 (ch. 23, the American side: read pp. 15–16, 29, 36–37, 44, 48–50, 52, 66 for what the filter found), 178–189 and 198–204 (the North's economy, the armed forces' schools), 232–237, 244–246 and 251–378 (1970–71, and the conclusion; p. 375 and the notes of pp. 379–88 for the Politburo's April 1969 resolution). The notes of the pages cited were read where they sit under the text; items from them (the Institute's *Tóm tắt các chiến dịch*, *Những sự kiện Lịch sử Đảng*, Hồ Chí Minh's *Toàn tập*, XII, Amter's Vietnamese edition, Nguyễn Duy Trinh's *Mặt trận ngoại giao*, the Defense Ministry's archive) are "To check:" lines or named in Checks; none were reached. The `notes-coverage` pass was not run (no merge).

### What was entered

120 adds: 95 `vietnam-hanoi`, 5 `vietnam-saigon`, 4 each `vietnam-paris`, `vietnam`, `vietnam-force-levels` and `laos`, 2 `vietnam-operations`, 1 each `vietnam-congress` and `vietnam-pacification`; most of the battles carry `also:` `vietnam-operations`. With `place:` 74; with a `time` 3 (the Feb. 26 raid at Đồng Dù, 2:30 a.m.; Ka Te, Nov. 2, 4 a.m.; the cease-fire of Sept. 8, 0:00) and a `time_range` with band 12 (the nights, "đêm", and the mornings the history names); with `at:` 20. Entries with a "Check:" 71. Secret decisions and directives of the Party and the army (`vis:only:drv`, "Made public: 2013"): 15. Cites 8 (the spring and summer phases, the autumn offensive's end, Bu Prăng–Đức Lập's end, the Guam address; the predecessor's four), variants 3 (the day of the Politburo's session, the special communiqué's hour, the U Minh sweep).

Battles and campaigns are new adds: the calendar holds none of the Vietnamese war's 1969 operations (its Vietnam threads stop in 1969 with the DRV's Party documents and the Paris talks), so no battle took a cite. The American acts the history dates (the withdrawals of June 8, July 7, Sept. 16 and 30, Nixon's address of May 14, Thiệu's message of July 11, Nixon's statement of Nov. 3, Laird's speech, the Cambodian bombing, the pacification plan) went in as thin adds on the history alone, each with a "Check:" and "To check:" for the American record: a reader of the American side will find them as likely duplicates, `./bib combine`.

### The rules used

R5 and R17: an entry an event-day; a campaign opens on its day and its stages (Hamburger Hill, Đắk Tô 2, Bu Prăng–Đức Lập) are entries of their own days, pointing back ("See"). A phase the history gives only by its stretch is dated to its month or season with `at:` (R15). Vietnamese units kept in English forms ("the 66th Regiment", "Region V", "Group 559"); "Miền" the COSVN command's, as the predecessor wrote it. The history's figures are "by the history's count"; its claims of losses are not the calendar's. Quotation: a few words in translation. Place keys only where the history names the place; "Check: the place" where it names a province or a region only.

### Passed over (R44)

Each dated event of 1969 and January 1970 the volume treats is in the patch or listed here.
- Outside the calendar's span (R18): the dated events of Feb. 1970–1971 (the 18-3-1970 coup, the incursions of Apr. 30, 1970, the three-nation summit of Apr. 24–25, 1970, the Laotian five points of Mar. 6, 1970, the eight points of Sept. 17, 1970, Nixon's five points of Oct. 7, 1970, the Politburo's resolution of Mar. 15, 1970, the Central Council for Support of the Front of June 1970, the 1971 elections, the 19th plenum, Kissinger's seven points of May 31, 1971, the 1972 preparations) and the 1970 actions of Region V (Mar. 31, Apr. 6, 1970), and the first half of 1970 generally.
- Dated items cited only as the source of a quotation: Nixon's Guam and Nov. 3 addresses and Laird's speech are entered (above); the Nov. 3, 1969 agency commentary on Saigon's land reform is entered; the AP item of Feb. 8, 1970 and the *Evening Star* of Feb. 19, 1970 (p. 41) are out of the span.
- Political statistics without a day or a place (the figures of strength, p. 72, the enemy's forces of p. 86, the Region 8 and 9 force counts of pp. 79–81, the North's school and harvest figures of pp. 165, 181–88, the 1969 force levels of p. 199): not events; kept as figures in the entries they bear on where the history ties them to one (p. 93, p. 218), the rest not entered.
- "Nixon, on Jan. 20, 1969, promised to end the war in six months" (p. 66): a claim about an event the calendar holds (the inauguration); not borne out in the record the calendar has, so no cite.

### Leads (R50)

Undated even to the year by the history, or its source not reached:
1. The B3 Front's decision to open Đắk Tô 2, and the Politburo's directive and COSVN's no. 71/TVTWC "for the spring" (pp. 102–3, 118–19): day not given; the second is in the Feb. 22 entry as a unit with `vis:only:drv`.
2. Early 1969, the South: the raid on Lộ Tẻ airfield, the Đồng Dù command post raid, the Thị Tính attack, the U Minh sweeps beaten (p. 101: "Trong khi đó"); the Massachusetts Striker operation (p. 123), "early 1969".
3. Nixon's order to Abrams to stop operations against North Vietnamese positions after A Bia (p. 126); undated, and a claim the American record should settle.
4. The heads of the PRG and its Advisory Council visiting states after June 6 (p. 269); the Saigon Phoenix and Thiên Nga networks (p. 78); the Saigon government's herding of 29,000 Dầu Tiếng rubber workers into 21 "new villages", Tây Ninh (p. 141).
5. The sources the history cites that this run did not reach: Hồ Chí Minh, *Toàn tập*, XII; *Những sự kiện lịch sử Đảng*, II (1985), IV (1982); *Lịch sử Đảng Cộng sản Việt Nam*, II (1995); *Tóm tắt các chiến dịch* (2001); the Defense Ministry archive (K4) and the B3 and Region 5 war summaries; *Lời phán quyết về Việt Nam* (Amter) and Pimlott for A Bia's American dead (VI, 125 n. 1).

### Persons named with no name entry (named in `c` and "Names:", not tagged)

Huỳnh Tấn Phát, Trịnh Đình Thảo, Trần Nam Trung, Cao Văn Bổn (the PRG's ministers, in the predecessor's Jun. 6 entry; Nguyễn Hữu Thọ and Nguyễn Thị Bình are tagged); Trần Hoài Nam, Phan Đăng Lâm (Paris, Jan. 25); Nguyễn Cụ (called Nguyễn Tư Cường; Đồng Dù); Lê Văn Phích (Bình Chánh); Mai Dinh; Weldon Honeycutt (A Bia); Khamtay Siphandone; Vũ Lập, Huỳnh Đắc Hương (Campaign 139, predecessor), Đàm Văn Ngụy (predecessor's Nov. 3 entry); Abrams (named in the Feb. mid-Cambodia entry; FRUS's list holds only Abrams, Frank W.). Tagged with the key the FRUS list implies, unchecked against the Names pages: `name:zais-melvin`, `name:hoang-xuan-lam`, `name:tran-buu-kiem`, `name:vang-pao`.

### Doubts

- The history dates the first plenary session of the four-party conference Jan. 25, 1969 (p. 101) and names Harriman as the head of the American delegation (p. 102 n. 1); the calendar has Lodge named Jan. 5 and the session set for Jan. 25 (cal.1969-01-18.vietnam-paris). Said in the entry's Check.
- Dates and figures that differ between the history's pages: the Politburo's resolution "of April 1969" against its session "of May 10" (the predecessor's variant on the Sixteenth Plenum); the pacification program's first phase (p. 52 against p. 74 n. 1); Lam Sơn 271 "to Apr. 31"; the Americans' dead at A Bia (pp. 125–26, two writers' figures against the history's 1,500).
- The history puts Cambodia and the United States' restoration of ambassadorial relations in Feb. 1969 (p. 249), and the *Life* photographs of 241 dead at A Bia on June 27 (p. 126): both entered as the history's, with a Check; the American record may read them otherwise.
- The history's units for the Highlands (Regiment 66 as the main axis of Đắk Tô 2, Battalion 9 and the "biệt kích ứng chiến" battalions) are kept as printed; the Saigon units' English forms are the writer's.
- Time of day: the "night of Feb. 22–23" is a band on the day Feb. 22; the "night of May 10–11" the predawn band of May 11 (the entry's day); the entries "at dawn" (Ka Te opening Oct. 29) the early-morning band.
- Date '1970-01' of the 18th plenum: in the calendar's span only if the plenum met by Jan. 19; the history gives the month.
- The predecessor's 25 adds were read against the pages they cite for the places and numbers this run's reading touched (pp. 83–96, 103–5, 115, 131–39, 149–52, 167–69, 173, 176, 191–92, 223–24, 239–40); pp. 241–46 (Campaign 139), 197 and 36–37 were taken from its reading.

## Audit of reader 4, Nov. 19

Opus audit, Nov. 19–20, 2026 (after 5 p.m. Pacific), of `inbox/2026-11-14-b16-lskc-1.yaml` (patch name kept, the ledger's claims stand under it). The three volumes fetched by the brief's curl form into a scratch folder, converted with `tools/vn/vkd2txt.py`, read by the book's folios (the offsets above confirmed: vol. III − 1 to PDF 137, − 17 after the plates), deleted at the end. Fixed in the patch directly; not merged, not committed. `./bib patch-check` (run in a scratch copy without the other pending inbox files, one of which, `inbox/witnesses/2026-11-19-b15c-dikotter-2.yaml`, carries two errors of its own): 0 errors, 192 warnings (the "one event?" and "a duplicate of" flags, verdicts below); `./bib fields --patch`: 0 findings.

The patch now: 295 adds (309 − 14), 80 cites, 33 variants, 97 place-keys, 3 checks, 4 also.

### Samples and fault rates

- Adds: every 6th of the 309 (indices 0, 6 … 306: 52 entries, 7 of them the predecessor's), each against its page; and every add against the same-day entries of all threads and the Party documents (`vietnam-hanoi`), with a place-and-month search of the `vietnam*` and `laos` threads. In the sample: date 0/52; actor, unit or act 1/52 (Mỹ Tho put in Gia Định); figures 4/52 (a helicopter type supplied from outside the page, two figures the page gives left out, a count given to "the Region"); place 4/52 (a departure place with no key, an order placed in one of its six provinces, the province wrong, a town for a district); time 3/52 (a night band inferred for an order, an hour left out, "24 giờ" read as the day's start); visibility 1/52 (an act with the Chinese as `vis:only:drv`); duplicates 2/52; pinpoint 1/52; loose dates 0/52 (all "early, mid, late" in `when`, which `merge` turns into `at:`; "Check: the day" on plain months is R15's form and stands).
- The history's losses not said to be its count: 41 of the 45 adds with loss figures (91%): marked "by the history's count" in each.
- Duplicates, all adds: 14 of 309 (4.5%), turned to cites and variants or dropped (below).
- Place keys: all 98 against the gazetteer's rules (G1–G3): 9 faults: two duplicates of existing keys under another spelling (`quy-nhon` for `qui-nhon`, `thanh-hoa-city` for `thanh-hoa`), four places of Nghệ An given the South's zone and `rvn` (`quy-chau`, `dien-hung`, `nam-can`, `hoang-mai`), three names (`Cái Be`, and "cầu Ông Hàn", "cầu Thị Qua" for the gazetteer's "… bridge"). Zones otherwise right by G3 (`Asia/Ho_Chi_Minh` the RVN, `Asia/Bangkok` the DRV); `viet-an` and `cha-la` are in reader 5's patch too, the same rows (the merge takes a same row twice without harm).
- Cites, all 70: units wrong on 28 (40%): 26 named only a place fragment the unit splitter leaves ("Pleiku.", "Saigon.", "Gulf of Tonkin.", "Paratroops under Col.") and not the unit the history bears out; one `all` where III, 46 bears out A only; one mis-targeted (the Xá Lợi crowd of June 16, 1963, cited on the joint communiqué). Items and pages sound where read.
- Variants, all 28: 3 not disagreements (the Palace bombing's details; Đồng Xoài's town left May 12; the June 16 crowd), dropped; 10 on the wrong unit (the place fragment, or the unit before the one disputed), moved. The other 18 are real disagreements with the American or the Party record (dates: Sầm Nưa, Phạm Văn Đồng's tour, the seventh plenum, Polei Krong, Qui Nhơn; losses and claims: Tua Hai, Phước Vĩnh, Ấp Bắc, Pierce Arrow, Biên Hòa, the Brink, Bình Giã, Pleiku, the ball field, Nam Đông, the MiGs of Apr. 3, the embassy; acts: Vũng Rô scuttled, not sunk; the Maddox).
- R5 coverage (a day-date sweep of II, 311–89 and III, 7–440): 305 distinct day-dates of 1960–65 in the text; 210 held by the patch's adds, cites or variants; of the rest, 60 not inside any entry's span; of those 16 are dated events neither entered nor in "Passed over" (list below), with three more found by reading.

### What was changed

- Duplicates (adds dropped; their ledger claims to be dropped by the merger, `./bib ledger drop 2026-11-14-b16-lskc-1 ID`): cal.1964-10-11.vietnam-hanoi (the Central Military Party Committee's order of Oct. 11, already cal.1964-10-11.vietnam: a cite, III, 375); cal.1961-08.vietnam-hanoi-3 (Phạm Văn Đồng's tour, already the patch's variant on cal.1961-06.vietnam-hanoi-3); cal.1961-09.vietnam-hanoi-3 (the 1961–63 plan, already cal.1961-09.vietnam and the patch's cite there; its tally folded into the cite, units A); cal.1964.vietnam-hanoi-4 (the Left and Right Bank regions into Military Region 3, the Politburo's merger of cal.1964-01-09.vietnam-hanoi: a cite, unit B; the add's "31" was "3" with a note number); cal.1962-11-20.vietnam-hanoi (War Zone D, cal.1962-11-20.vietnam: a cite); cal.1963-09-09.vietnam-hanoi (Cái Nước and Đầm Dơi, cal.1963-09-10.vietnam-operations: a cite and a variant, the night of Sept. 9–10, 327 out of action); cal.1963-11-23.vietnam-hanoi (Chà Là, cal.1963-11-24.vietnam-operations: cite and variant); cal.1963-12-31.vietnam-hanoi (the Ranger battalion near Bến Cát, cal.1963-12-31.vietnam-operations: cite and variant); cal.1964-02-06.vietnam-hanoi (Bến Cầu, cal.1964-02-06.vietnam-operations: cite and variant); cal.1964-07-01.vietnam-hanoi (Polei Krong, already the patch's cite and variant on cal.1964-07-04.vietnam-operations); cal.1964-08-04.vietnam-hanoi (the history's denial of the second Tonkin attack: a cite, units B–C, and a variant, unit A, on cal.1964-08-04.vietnam); cal.1964-12-16.vietnam-hanoi (the Kinh Đô cinema is the Capitol Kinh Đô theater of cal.1964-02-11.vietnam-operations; the history prints "16-12-1964" between its acts of Feb. 9 and Apr. 30, 1964: cite and variant); cal.1965-06-30.vietnam-hanoi-3 (the Đà Nẵng airfield, cal.1965-07-01.vietnam-operations: cite and variant, 57 aircraft); cal.1964-05.vietnam-hanoi-3 (the May 1964 offensive on the Plain of Jars, cal.1964-05-17.laos: cite, variant with the Vietnamese part and the figures the add had left out, also `vietnam-hanoi`).
- Cites and variants: units set on 27 cites and one; 10 variants moved to the unit they dispute; the cite and variant on cal.1963-06-16.vietnam (the crowd at Xá Lợi, a separate event) and the variants on cal.1962-02-27.vietnam and cal.1965-05-11.vietnam-operations (no disagreement) removed.
- Place keys: the two duplicate keys dropped and their entries moved to `qui-nhon` and `thanh-hoa`; the four Nghệ An keys to `Asia/Bangkok`, `drv`; `cai-be` "Cái Bè"; `ong-han`, `thi-qua` "Ông Hàn bridge", "Thị Qua bridge"; `xuan-mai` (Xuân Mai, `drv`) added, the place of the first cadre group's departure (cal.1961-05-05.vietnam-hanoi); cal.1961-09.vietnam-hanoi-2 `ok:fields-place`.
- Facts: cal.1961-06-19.vietnam-hanoi (the Củng Sơn raid did not free Nguyễn Hữu Thọ: he had been moved to Tuy Hòa, III, 142); cal.1963-11-03.vietnam-hanoi (Mỹ Tho, not Gia Định: III, 282); cal.1963-12-29.vietnam-hanoi (the US Core charge did not fire, III, 353); cal.1962-12-08.vietnam-hanoi-2 ("H-21" was not the page's: "H47" as printed); cal.1965-05-31.vietnam-hanoi (put out of action, not destroyed; place `gia-lai`, not the town).
- Figures and attribution: "by the history's count" on 39 adds (with cal.1965-07-22 and cal.1965-01-03.vietnam-hanoi, where "the Region's count" was the history's "ta"); the figures the page gives added on cal.1960-09-20, cal.1964-01-09.vietnam-hanoi-2, cal.1964-08-25, cal.1964-05-10 (whose Check wrongly said the count was cut off); cal.1965-07-22.vietnam-hanoi pinpoint 416–36 narrowed to 436 and 417–19.
- Fields: cal.1960-09-14.vietnam-hanoi (an order: the inferred night band, the place and "Check: the day" removed); cal.1964-08-25.vietnam-hanoi ("at 11 sharp", morning or night not said: no field, `ok:fields-time`, a Check); cal.1964-04-04.vietnam-hanoi-2 ("24 giờ ngày 4-4" read as the midnight ending Apr. 4, with a Check).
- Visibility: cal.1962.vietnam-hanoi-2 `vis:only:drv+prc`; cal.1961-02-15.vietnam-hanoi "Made public: 2013." added to its `vis:only:drv`; cal.1962-07.vietnam-hanoi (Military Region 4's Party congress) `vis:only:drv`, "Made public: 2013.", as the patch's other Party congresses; cal.1961-10-30.vietnam-hanoi-2 `vis:only:drv` removed (Saigon hunted for Thọ at once, III, 161).
- Checks added or reworded: cal.1965-08-05.vietnam-hanoi-3 (Cooper's memorandum of Aug. 5 speaks of "the night's attack": Aug. 4–5?); cal.1962-06.vietnam-hanoi-3 (the calendar has the NLF delegation in Peking Sept. 28–30); cal.1961-07.vietnam-hanoi-4 and cal.1962-02-09.vietnam-hanoi (III, 47: two ceremonies, Feb. 9, 1961 and Feb. 9, 1962, no misprint shown). Prose: three slips mended.

### Rulings

- "Made public: 2013" stands, provisionally. The publisher's note (I, 5–6) says the first edition (Chính trị quốc gia, 1995–2012) was distributed "chủ yếu" (mainly) within the army in limited numbers; the second, 2013, "rộng rãi" (widely). That is not the internal-circulation mark R27 names, and the series lists two first-edition volumes as published works (`w.al-lich-su-khang-chien`, vol. 5, 2001; `w.lich-su-khang-chien`, vol. 6, 2003). Whether a printing "mainly in the army" is publication is the owner's ruling under R27; if it is, the year becomes the first edition of vol. II or III (not established: a lead). The card's note "circulated in the army only" overstates the publisher's "mainly": for the lead (the card is not this audit's to edit).
- The misprints: III, 47 is no misprint shown (two ceremonies a year apart; the 1961 one is a dated event for the next run); III, 248 (the night of Apr. 28 against a morning of Apr. 24) stands as a Check; III, 186 ("17-2-1961") stands as entered; III, 249 ("nửa cuối năm 1968" for 1963) is a loosely dated event of Region 5, the second half of 1963, for the next run. The Hòn Mê raid (cite on cal.1964-07-30.vietnam-34a-2) and the Maddox of Aug. 2 (cite and variant) are right; Aug. 4 is now a variant, not an entry.
- cal.1962-06.vietnam-hanoi-3, the NLF delegation's tour of June–November 1962 (one entry, six countries by month): over the week's limit (the owner, Oct. 20); left as R15's trip, for the owner or a split in the next run.
- The General Staff's and the Defense Ministry's acts placed at Hanoi (P4 names the Politburo and the Assembly only): kept.
- One event? The 12 groups inside the patch (Jan. 28, Sept. 14, Sept. 23, 1960; Oct. 30, 1961; Sept. 9, Nov. 23, Dec. 31, 1963; Apr. 8, Dec. 8, Dec. 30, 1964; June 30, 1965): each a separate act, distinct places or units: keep. The 88 remaining "a duplicate of" flags against existing entries (mostly the Secretariat's circulars and *Học Tập* of the same day or month): all distinct: keep. The merger resolves them `--take keep`.

### Not entered and not in "Passed over" (found by the audit's day-date sweep; for the next run, R44)

Dated events of the volumes' own text with no entry, cite or Passed-over row (each looked at on its page): II, 335 (Feb. 24, 1960, Unit 514's ambush at Cây Me, Route 4); II, 341 (May 6, 1960, four Saigon battalions sweep Cần Thơ); II, 347 (the evening of Mar. 30, 1960, Company 40's attack; Apr. 6); II, 351 (June 12, 1960, Kon Sâm kills a Saigon major at Kon Kô); II, 373 (July 17, 1960, the reconnaissance before Bắc Ruộng: the preparation of an act, R18); II, 381 (the night of Dec. 22, 1960, the rising at Hòa Thịnh, Phú Yên); III, 47 (Feb. 9, 1961, Q761's battalions' ceremony at Dương Minh Châu); III, 161 (Aug. 10, 1961, the sentence broken by the note); III, 165 (Jan. 9, 1962, the death of Ràng); III, 133 (June 12, 1962, the three Lao parties' agreement on a coalition: check the calendar's `laos`); III, 222 (10 p.m., Jan. 1, 1963, the Ấp Bắc command learns of the attack due Jan. 2: a preparation, R18; a cite on cal.1963-01-02.vietnam may do); III, 279 n.1 (Oct. 15, 1963, Hậu Nghĩa province set up); III, 345 (Apr. 3, 1964); III, 370, 378 (Nov. 18, 1964, the bombing at Cha Lo, western Quảng Bình, and Battery 3 of Battalion 14, 325th Division); III, 369 (Dec. 19, 1964, Thai troops into Laos by the history's account: check the calendar); III, 435 (July 20, 1965, Regiment 1 against a training center); the crowd at Xá Lợi, June 16, 1963 (III, 312, dispersed by the police: its own entry, not the communiqué's cite); the second half of 1963 in Region 5 (III, 249, printed 1968); III, 116 (early 1963, the reserve-force drive of Nghệ An, Hà Tĩnh and Quảng Bình; late 1963, Military Region 4's three lines of defense). The other day-dates the sweep found outside the entries are second days of entered spans, tallies, American acts the calendar holds, or rows already in Passed over. The sweep does not reach month- and year-dated sentences: the next run should make one for "tháng M-YYYY" and "năm YYYY" too.

### Leads (R50)

Foreign. The first edition of vols. II and III (Chính trị quốc gia, the years not given in the 2013 note): its year and its circulation, for "Made public" (R27); the card `w.lich-su-khang-chien-chong-my` and the two first-edition cards to be joined by the lead with that in hand.


## Audit of reader 6, Nov. 19

Auditor: Claude (Opus), Nov. 19, 2026, evening (after 5 p.m. Pacific). Patch `inbox/2026-11-14-b16-lskc-3.yaml`, fixed in place (patch name kept, so the ledger's claims stand). The original is kept in the auditor's scratch directory. Vol. VI fetched again by the brief's curl form (Drive `1zggkITSSkyz-9er0juH5iyNy1i41Uqj-`, 404 PDF pages, PDF 1.6). Its TCVN3 layer was converted with the predecessor's `pages.py` and `compact.py` (run from outside the copy's folder), and the book's folios read from each page; the PDF and texts were deleted when done. Every page cited by a sampled entry was read against the entry, and the notes under it. `./bib patch-check`: 0 errors, 108 warnings. The warnings are the same-day "one event?"/"a duplicate of?" prompts, all for distinct acts (below), and the edit's "sets only n". `./bib fields --patch`: 119 entries, 0 findings.

### The sample

40 adds, every third of the 120 in the patch's order (#0, #3, ... #117), 8 of them the predecessor's (Feb. 22, Apr. 27, May 8, June 12, July 29, Sept. 4–5, Oct. 25, Nov. 6). Also read against the pages: every thin American add (10), the reader's doubts, the 8 cites and 3 variants, all 32 place keys, and most other adds on the pages already open. In all, some 105 of the 120 were read. Faults in the sample of 40, by class:
- date: 0;
- force, unit or command: 0;
- the act, words not the page's: 3 (Mar. 18; Aug. 11 Bình Thuận; Aug. Saigon);
- the history's figures not marked as its own: 7 (Jan. 10, Feb. 22 Mỹ Tho, Apr., May Region 6, May 31, Nov. 11, Nhị Bình);
- the loose date's wording or `at`: 4 (1969 summer, Sept. Laos, June recognitions, Feb. Highlands);
- the place: 1 (May 11, Hớn Quản);
- time fields: 0;
- `name:` tags and "Names:": 3 (Jan. 25 Saigon; June 8 and Sept. 30, "the American President");
- the note's sources not behind "To check:": 1 (Mar. 18);
- duplicates: 0;
- `vis:` and "Made public": 0.

The predecessor's 8 in the sample: 1 fault (Oct. 25, Vang Pao untagged), and its Sept. 4–5 and Oct. 29 carried cites on the patch's own adds. Across the whole patch, the same classes were then corrected wherever they occurred (below).

### Changes

- **The history's figures**: "by the history's count" added in 25 adds (23 by the rule, Mar. 18 and Aug. Saigon in their rewriting) where reader 6's text gave enemy losses, sinkings or tonnages bare, as the run's own rule says.
- **Duplicate**: `cal.1969-09.vietnam-hanoi` (the Politburo's directive for study of the testament, "after his death") is directive no. 173-CT/TW of Sept. 29 (`cal.1969-09-29.vietnam-hanoi`, from *Văn kiện*, XXX, 330–36). The add is dropped and replaced by a cite there, VI, 170, 193, unit A. Its ledger claim is left for the merger (`./bib ledger drop 2026-11-14-b16-lskc-3 cal.1969-09.vietnam-hanoi`).
- **Ops on the patch's own adds** are folded into those adds' notes. These are three cites (May 11, Sept. 4–5, Oct. 29, as "The history adds ...") and one variant (Sept. 26, U Minh, VI, 264, now a sentence of the Check). The May 11 cite's hamlets and people freed are the spring and summer phases' together (VI, 127), not the summer's alone.
- **Text**:
  - Mar. 18: "the first bombing of Cambodia" is not the page's, and "Breakfast" was a gloss from memory. Now: the raid the Americans called, by the history, "hoạt động bữa ăn" (the meal operation), and the history's "start of the war's widening into Cambodia". The secret bombing goes in the Check, and Amter behind "To check:".
  - June 27, *Life*: "in a week's fighting" and the Check's "one week's dead" were from memory (R4). `c` now gives 241 American soldiers killed, by the history at A Bia.
  - Aug. 11, "Binh Thuận" → Bình Thuận. Its Check is dropped (the page names the Sông Mao base).
  - Nov., late: Chợ Bưng, Châu Thành → Chợ Bung, Châu Thành Bắc, as printed.
  - Feb.: Camp Ê-sê-pích → Camp Êsépic, as printed (VI, 105).
  - Aug., Saigon strikes: the Thủ Đức strike of Feb. 1970 is taken out of `c` (outside the span, R18) and named in the Check.
  - Nov. 3: Nixon's words as the history quotes them (VI, 28–29).
  - Feb. 23: Region V's phase gets its opening day, with "to Mar. 31" in `c`. It was `when` Feb. 23–Mar. 31, a span of five weeks.
  - Mid-Feb.: "the second quotation" is now the view it quotes.
  - 1969, the Navy: its separation "bước sang năm 1970" is named in the Check as an act of its own.
- **American adds**: June 8 and Sept. 30, "the American President" → Nixon (tag and "Names:"; the Check points to the inauguration entry). Sept. 30 gives the history's October 1970. Laird, Jan. 14, 1970: `place: california`, "See" the Guam entry, Nixon tagged.
- **Loose dates**:
  - 1969, the army's reorganization: "1969, mid" → "1969, summer" (p. 194, "từ mùa hè năm 1969"), at before 1969-06-21.
  - Sept., Laos: → "Sept., late" (the order to withdraw), `ok:fields-at` dropped.
  - June, the recognitions: → "June, after the PRG's formation", at after 1969-06-08.
  - Feb., "spring phase" (two entries): → "Feb., after the 22nd", a wording merge reads.
  - Ba Làng An: "1969" → "1969, first half" (the spring and summer phases' results).
  - The three "Dec., winter" entries of the winter phase: a Check that the phase opened in late October (VI, 137).
  - Tết letter: the Check gives Tết, Feb. 17, 1969 (tools/calendar).
- **Places**:
  - `hon-quan` dropped. The gazetteer's `an-loc` is the same place (VI, 136: "An Lộc (Hớn Quản)"), so May 11 and Aug. 12 take `an-loc`, with a `fix: true` row giving its name its marks, An Lộc.
  - `ba-ria` dropped: the history's Bà Rịa is the Front's province, and the entry has no place, with a Check.
  - `u-minh` → `u-minh-thuong` (the key from its name).
  - `camp-e-se-pich` → `camp-esepic`, "Camp Êsépic".
  - `binh-chanh-bridge` named "Bình Chánh bridge", as the gazetteer's Long Biên bridge is.
  - `chuong-thien` named "Chương Thiện province".
  - New `muong-soui`, Muong Soui, Asia/Vientiane, `in: laos`. June 23 and June 28 take it: the campaign was fought there, not on the Plain of Jars.
- **Time**: June 23, Mường Sủi: the night band in Asia/Vientiane (UTC+7), not Saigon's zone (UTC+8). The range is now 15:00–17:00Z.
- **Names**: tags and "Names:" added:
  - Thiệu, Kỳ, Hương (Jan. 25 Saigon);
  - Thiệu (July and mid-1969 Saigon);
  - Lon Nol (Feb., Cambodia);
  - Abrams, `name:abrams-creighton`, the calendar's key (mid-Feb.);
  - Vang Pao (June 23, Oct. 25).

  The reader's note that FRUS's list holds only Frank W. Abrams overlooked the calendar's own key.
- **Tags**: `polity:cambodia` on the Cambodian entries; `polity:drv` on June 28; `ok:fields-place` on mid-Feb. (Washington named as a subject).
- **"To check:"** lines added for the note's sources:
  - Mar. 17 (*Chiến trường Trị–Thiên–Huế*, 172);
  - 1969, the 1st Division (*Lịch sử QĐND Việt Nam*, II, 337);
  - May 23 (Amter, 255; Pimlott, 130);
  - Sept. 4 (the PRG's cable);
  - June 28 (*Lịch sử QĐND Lào*, 6);
  - mid-Feb. (Amter, 274, 175);
  - Mar. 18 (Amter, 277).
- **The patch-check error on `cal.1969-07.vietnam-hanoi`**: an `edit` (base `676e6363`), placed before the cite, gives *Văn kiện*'s pinpoint as "XXX, 365 (the print's page, by the editors' own reference to their note on a passage perhaps lost; the copy's appendix pages unnumbered, the note at its PDF 183)". The source is the 1968–69 audit's finding above, in `van-kien-dang-toan.md`. It is one page of the resolution, the only one known. The resolution's whole range in the print needs a printed copy.

Counts now: 119 adds, 6 cites (Guam; Jan. 13; May 8; COSVN's July conference; Sept. 2; Sept. 29), 2 variants (May 8, Sept. 4), 1 edit, 32 `place-key` ops (30 of the reader's, `an-loc` fix, `muong-soui`). `bu-dop` is identical to `b16-lskc-2`'s row.

### Rulings

- **Thin American adds.** Each was searched in the calendar, all threads, on its day and by words (Nixon, withdraw, Vietnamization, Cambodia, Midway, Hamburger, *Life*). These are the withdrawals of June 8, July 7, Sept. 16 and Sept. 30, Nixon's May 14 address, Thiệu's July 11 message, Nixon's Nov. 3 statement, Laird's Jan. 14, 1970 speech, the Mar. 18 bombing and the pacification plan, with Kennedy of May 21 and *Life* of June 27. The calendar holds none of them, nor do the ledger's other claims. The 1969 Public Papers are not yet in, so each thin add stands, with its Check, and none became a cite. The Guam address is held (`cal.1969-07-25.vietnam`) and takes the cite.
- **1970.** The calendar's span ends Jan. 19, 1970 (R1). Laird's speech of Jan. 14 is within it. The 18th plenum, "tháng 1-1970", stands as a month-dated entry with its Check: the history gives no day.
- **Night bands.** Upheld. "The night of D–D+1" takes the band on the entry's own day: `night` (22–24) when the entry is dated D (Feb. 22–23, June 23–24, Sept. 4–5), `predawn` (0–6) when it is dated D+1 (May 11, the offensive's day by VI, 115, Đắk Tô 2 opening the night of May 10–11).
- **"Dec., winter".** The history's "đợt đông 1969" is read by the season's rule (before the December solstice), with a Check on each such entry, since the phase opened in late October.
- **Harriman or Lodge at the Jan. 25 plenary.** The history's note (VI, 102 n. 1) names Harriman. The calendar has Lodge named Jan. 5 (`cal.1969-01-05.vietnam`). The add's Check stands: the history's note is the one in doubt.
- **Cambodia and the United States, Feb. 1969 (VI, 249).** This is the history's dating alone. It is kept, the Check now asking for the American and Cambodian records.
- **The *Life* photographs.** The entry now says only what the page says (above).
- **"31-4-1969" (VI, 113).** A date that does not exist; the Check stands.
- **The pacification phases.** VI, 52 (Nov. 1968–June 1969, July 1969–June 1970, July 1970–Feb. 1971, Mar. 1971–Mar. 1972) and VI, 74 n. 1 (start of 1969–June 1970, July 1970–June 1971, from July 1971) differ. The entry gives both, with its Check, as written.
- **Place keys.**
  - `plei-can` and `plei-thong-breng`, with names "Plây Cần" and "Plây Thông Breng", are kept. The key takes the gazetteer's Plei spelling (`plei-me`, `plei-do-lim`) and the name the history's form, as reader 4's `plei-mrong` ("Plây Mơrông") does. A uniform rule is for the lead.
  - `co-ca-va` ("Côcava" as printed) is kept in the reader's spacing.
  - Every key's zone is right: Asia/Ho_Chi_Minh for the South, Asia/Vientiane for Laos.
- **`vis:only:drv` and "Made public: 2013".** Upheld on the 15 entries, all records of Party, army or ministry decisions not published at the time. "Made public: 1985" on COSVN's directive no. 81 (*Những sự kiện lịch sử Đảng*, II, 1985) is upheld.

### Duplicate flags

All the same-day prompts of patch-check are distinct acts, so each is to be kept at the merge (`./bib resolve ID --take keep`):
- the year-dated 1969 entries (the North's support, the 1st Division moved, the pipeline, Route 559's tonnage, the Navy, Group 559's roads, the army's reorganization, Ba Làng An, Mai Dinh, Nhị Bình, Rừng Sác, Hồ's Tết letter);
- Feb. (Bầu Cối, the delta, Camp Êsépic, the Highlands);
- Feb. 22 (the offensive and Mỹ Tho);
- Mar. 17 (Atlas Wedge, Lam Sơn 271);
- Apr. (the battles, against Region V's resolutions);
- May (Hồ's letter to the class; Region 6);
- May 8, 10, 11, 12, 17, 19, 24;
- Aug. 11 and 12; Sept. 2, 4 and 8;
- Nov. (Mỹ Tho, the Bình Chánh bridge); Nov. 2, 3 and 21;
- Dec. (the ministries, the Miền's withdrawal, Bến Tre, Region 6, Bà Rịa).

The only duplicate, Sept. 1969 against Sept. 29, had no flag (its date differs) and is dealt with above. The Mường Sủi pair (June 23 opening; June 28–July 1 the end) are a campaign and its stage, kept, as are Bu Prăng–Đức Lập's stages.

### Not done

- No witnesses file or by-work edges (R35), and `notes-coverage` not run: as the reader's own run left them, for the merger to know.
- The ledger claim of the dropped add is not released (see above).
- The reader's Passed over and Leads stand. Add to Leads:
  - (Foreign) the *Life* issue of June 27, 1969, what it printed;
  - the American and Cambodian record of the restoration of relations, 1969;
  - the date the Mar. 18 bombing was made public;
  - the Navy's separation from the Northeast Military Region, "at the turn of 1970" (VI, 206): its day, for the span.

### Fit to merge

Yes, as fixed. 0 errors. The duplicate prompts are to be answered "keep", and the one ledger claim dropped.
