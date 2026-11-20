# Lịch sử kháng chiến chống Mỹ, cứu nước (w.lich-su-khang-chien-chong-my): book check

The official history of the Institute of Military History, 9 vols. (the second edition, Chính trị quốc gia – Sự thật, Hà Nội, 2013). The series card is `w.lich-su-khang-chien-chong-my` (`works/l.yaml`, made by the first reader of batch 16, Nov. 14, 2026); the two one-volume cards (`w.lich-su-khang-chien`, `w.al-lich-su-khang-chien`) are left for the lead.

## Reader 4 (vols. I–III), Nov. 19

Reader 4, batch 16 (`notes/briefs/batch16-drv.md`), resuming the run stopped Nov. 14. Patch `inbox/2026-11-14-b16-lskc-1.yaml` (patch name `2026-11-14-b16-lskc-1`): the predecessor's 37 new entries and 66 ops (its `partial-patch.yaml`, read against the volumes and carried over; the one cite of the Bến Tre rising to the Tua Hai entry, cal.1960-01-26.vietnam, dropped for its own entry) and this run's 253 new entries, cites and variants, with the 87 `place-key` ops its places need. Scripts and specs: `notes/wip/b16-lskc-1/` (`ops/z*.py`, `scripts2/`: the DSL, the claims in `ids.tsv`, `build.sh`).

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

- 290 new entries (47 of 1960, 61 of 1961, 42 of 1962, 61 of 1963, 54 of 1964, 25 of 1965): 227 with a `place`, 16 with a `time` and 37 with a `time_range` and band; 66 cites, 27 variants (the history's account of an act the calendar holds from the American side: the Tân Sơn Nhứt ball-field bombing of Feb. 9, 1964; Polei Krong and Nam Đông, July 1964; the Maddox, Aug. 2, 1964; the Qui Nhơn hotel, Feb. 1965; the Palace bombing of Feb. 27, 1962; the crowd of June 16, 1963), 3 checks, 3 `also` ops. Thread `vietnam-hanoi`, `also` `vietnam-operations`, `vietnam`, `vietnam-34a`, `laos`, `vietnam-air-war` as the act bears. The Buddhist crisis of 1963 (12 entries, thread `vietnam`) and Diệm's visit to Bến Tre (Mar. 1960) are the Saigon side's acts, tagged `polity:rvn`, entered because the history dates them and the calendar lacks them.
- The Party's and the army's secret acts take `vis:only:drv` with "Made public: 2013." (the second edition; the first, 1995–2012, circulated in the army only: R27). Battles and the Front's public acts carry no ruling.
- Places: the gazetteer's key where it had one; 87 new keys (the provinces, districts, posts and bases the history names), zone `Asia/Ho_Chi_Minh` for the South, `Asia/Bangkok` for the North. Where the entry's place is only a subject of the text (a city named as the target, "Saigon" in a Saigon commando act of another city, a strategic hamlet's name) the entry is tagged `ok:fields-place`; where an hour or a part of the day belongs to the second day of a span, `ok:fields-time`.
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
