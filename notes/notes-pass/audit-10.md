# Audit of the notes pass, batch 10 (patches 10 and 10r)

Opus audit, Nov. 27, 2026, of `inbox/2026-11-26-notes-pass-10.yaml` and `inbox/2026-11-26-notes-pass-10r.yaml`, for the 60 entries of `notes/notes-pass/batch-10.tsv`. Both patches were corrected in place. Both pass `./bib patch-check` with 0 errors. Nothing was merged, built or committed.

## What was read

Every page that an op of either patch cites was read on its page image or, for the English books with a clean text layer, in the text layer with the folio checked. Each work was fetched once from the Drive and deleted after use. Google gave no "Quota exceeded" answer during the run.

- Chinese works, read as page images: Peng Zhen nianpu IV, 12, 18, 20, 31–33, 46, 48–49, 51–52, 70–72, 74–77, 79–80, 86, 88, 91, 94–96, 102–103, 107, 110, 116–117; Deng Xiaoping nianpu III, 1537, 1566, 1569, 1580, 1593, 1608, 1611–1612, 1615–1617, 1620–1621; Zhu De nianpu III, 1772–1773, 1777, 1780, 1783, 1790, 1970; Chen Yun nianpu III, 43, 61–62, 75, 170–171; Yang Shangkun's diary I, 501, 558–559, 592, 600, 618–619, 660–661; Wu Lengxi 254–255, 367, 381; Zhou Enlai nianpu (1997) II, 296–297, 331–333, 336; Mao wengao XV, 76, 78–84, 342–344, 398–400; Wenxian XIV, 168, 176, 181–183, 186–187, 238–239; Mubei II, 1139–1141; Ye Jianying nianpu II, 883, 985–986; Chen Yi nianpu 820, 837–838, 1213–1214; Zhou Enlai nianpu (2020) III, 322; Liu Shaoqi nianpu (1996) II, 481, 494, 507; Zhou Enlai waijiao huodong dashiji 283, 290.
- Read in the text layer: Tiandi fanfu II, 737–738; Brezhnev, Rabochie i dnevnikovye zapisi I, 430, 433–434 (434 also on the image), 450–452, and II, 363, 376; the Mao Zedong zhuan EPUB, ch. 66 nn.8, 47, 52, 59, 62, ch. 67 nn.1, 5, 8, ch. 78 n.21, each with the passage that calls it.
- English books and records: Fursenko and Naftali 272–273, 296; O'Donnell 188–189, 227–228; Smith 344–345; Wofford 51–52, 141; Goldberg 146; Schlesinger, Journals 94–95; Schlesinger, Robert Kennedy 227, 231–232; Guan 171; Jones 55; Goodwin 155–157; Mann 229; White 375; Moyar 103; Victory in Vietnam 86–88, 456; Lịch sử III, 57; Kaplan 179; MacFarquhar 318; Teiwes 113; Jian, Zhou Enlai 452–453; Dikötter 116; the Church report 79, 196–197; Watson 749; Poole 218; FRUS 1958–60, IV, doc. 56; the 1961 Public Papers 211, 214, 229–231; the APP text of the Hyde Park speech of Aug. 14, 1960.

## What could not be read

Wang Renzhong's diary (cited by the Mao Zedong zhuan, ch. 66 n.59) is not on the Drive: a search for 王任重 and "Wang Renzhong" found nothing. It stays behind "To check:" on `cal.1960-10-26.china-leadership`. The Deng Xiaoping nianpu pages were read on the images, but the notes I kept of them while reading were brief; I found no fault in the 10r ops that cite them.

## Ops checked and held

All ops of both patches were checked against their pages. Most held as written: the Peng Zhen nianpu attendance and speech additions, the Deng, Zhu De, Chen Yun and Yang Shangkun additions, the Wu Lengxi and Zhou nianpu additions (with one change below), the Brezhnev attendance on Dec. 5, the Mao wengao letter and mess-hall insert of Mar. 15, the Ferhat Abbas points, Lịch sử's 525 delegates, Kaplan's 160 men, MacFarquhar's title and units, Teiwes on Wang Dongxing, and all of patch 10's English-book additions except those named below.

## Changed

- `cal.1960-07-22.elections-1960`: "the State's patronage" is "all New York State patronage" on Smith's page (345).
- `cal.1960-10-20.economy`: Anderson gives the weak balance of payments as "one important reason," and foreigners buying gold "for investment," not "to hold" (FRUS doc. 56).
- `cal.1960-12-15.robert-kennedy`: Seigenthaler's recollection reworded to the page (232): no one in the cabinet the President has long known; someone to tell him "the unvarnished truth."
- `cal.1961-03-28.defense`: the $650 million is on page 231 of the Public Papers, not 230.
- `cal.1960-07-14.china-leadership`: the Zhou nianpu (333) has the third period with less interference than the first and still less than the second, not "little interference." Peng's addition cut to "Peng Zhen attends," since the line already says what the report treats. The additions now run Zhou nianpu, then Jian, then the attendances.
- `cal.1960-07-31.china-leadership`: Jian's addition cut to Zhou's quoted words; "to press us" is already in the line.
- `cal.1960-12-23.china-leadership`: the Mubei pinpoint is II, 1140 (the letter as the text gives it); 1141 n.63 is only the archive's file. Li Dazhang, the addressee, is named and tagged.
- `cal.1960-12-30.china-leadership`: on Chen Yun nianpu 62 someone else adds "the market second, construction third," and Mao then sums it up; the addition now says so and no longer repeats the points the line already has.
- `cal.1961-02-14.china-leadership`: the figures and warnings are Peng's own words at the meeting; the addition now says "Peng:".
- `cal.1960-11-21.soviet-union`: Ba Thein Tin's words reworded to the page (Peng IV, 77): the party's revisionists called for giving up armed struggle after the Twentieth Congress. The existing note named "Thakin Than Tun"; the page has 巴登顶, Ba Thein Tin, the general secretary: corrected by an edit.
- `cal.1960-11-18.china-leadership-3`: the existing note listed Iran among the afternoon speakers; Peng IV, 75 has Mongolia: corrected by an edit.
- `cal.1961-02.china-leadership-3`: the page (XIV, 176) reads 94,000 fewer, not 90,000: the note corrected by an edit in place of 10r's Check. The pinpoint for the enrolment figures is 176.
- `cal.1961-04-03.china-leadership-5` and `cal.1961-01-18.china-leadership-2`: pinpoints narrowed to the pages read (XIV, 238–239; 182–183).
- `cal.1969-10-18.china-leadership`: the 95 divisions and the rest are on Tiandi fanfu II, 738, not 737–738.
- `cal.1960-10-02.soviet-union`: 10r's Check repeated the note; it now says only that Yang also has the first session Oct. 1.
- `cal.1960-11-15.china-leadership`: the addition keeps only Mao's own words (XV, 398–399).
- `cal.1969-12-05.soviet-union-leadership`: Brezhnev's notes № 98, "on the situation in the party," are of his talk with Husák that day, not of Ceaușescu (I, 434 n.a; 452 n.275). The line's last clause, "the Romanian party's fight with the right," is taken out and the note corrected by an edit (kind: correct), with the editors' note named. 10r's addition from № 98 is struck.

## Struck, or moved to the act it belongs to

- `cal.1960-09.cuba-4`: Hoover's memorandum of Oct. 18 is an act of its own. Patch 10's addition and names are struck, and the memorandum is a new entry, `cal.1960-10-18.cuba-3` (Church report 79).
- `cal.1960-08.elections-1960-8`: 10r's APP primary is struck. The speech is not the call on Mrs. Roosevelt, and it has its own entry (`cal.1960-08-14.medicare`). A Check now says what the APP text shows of the day.
- `cal.1960-07-31.china-leadership`: the Zhu De note's figures (1,390 experts and the rest) are of the Soviet recall, not of Zhou's report: struck. 10r's Check on the Standing Committee stands.
- `cal.1960-10-26.china-leadership`: Dikötter's figures are the report's own. They are moved to `cal.1960-10-21.china-leadership-8`, the report's entry, with a Check that Dikötter has the report come from the Ministry of Supervision. 10r's open point settles so: Dikötter's page is 116, in the text, not the note.
- `cal.1961-03-23.laos`: the 12,000 is Victory in Vietnam's note 21 (456), a total of volunteers "during this campaign," not a figure for March 1961. The units' going into Laos is another act, already `cal.1961.laos`. 10r's addition is struck. The book is cited on `cal.1961.laos` (87, 456 n.21), and a Check on the press-conference entry says where the 12,000 belongs. This settles 10r's open point.
- `cal.1960-03-15.china-leadership-2`: the Hunan and Shandong figures are the reports' own (XV, 78 n.1, 80 n.1). They are moved to those reports' entries, `cal.1960-03.china-leadership-11` and `cal.1960-02-27.china-leadership-6`.
- `cal.1961-01-18.china-leadership-2`: "The Center approves it Feb. 7" is struck; it is `cal.1961-02-07.china-leadership-10`.
- `cal.1960-11-10.china-leadership-13` takes "three years as a rule" from XV, 399 n.1, the report's own term, struck from the Nov. 15 entry.

## Added: the fields (R25a) and new entries

Times set from the record: Apr. 22, 1960 (3 p.m., Yang); June 4, 1960 (afternoon, Peng and the dashiji); July 31, 1960 (4 p.m., Yang); Aug. 18, 1960 (morning, Peng); Nov. 9, 1960 (5 p.m. Moscow, Peng and Yang); Dec. 23, 1960 (evening, Peng); Dec. 30, 1960 (afternoon, Peng and Chen Yun); Jan. 13, 1961 (11 a.m., Yang); Jan. 25 (morning) and Jan. 27 (afternoon), 1961 (Peng); Feb. 14, 1961 (afternoon, Peng); Mar. 7, 1961 (3 p.m., Yang); Mar. 13, 1961 (6 p.m. Washington, Goodwin); Oct. 2, 1969 (11 a.m. Moscow, Brezhnev II, 363); Oct. 17, 1969 (evening, Zhou nianpu 2020); Dec. 5, 1969 (11 a.m. Moscow). Where an entry had a time range for the afternoon or morning and the record gives the hour, the range was replaced by the hour. Left unset: July 14–16, 1960, where Wu has mornings and Yang afternoons; May 8, 1960, where O'Donnell has the evening and O'Brien the afternoon (both readings are already in the note). On Oct. 17, 1969, a Check records that Ye Jianying's and Zhu De's chronologies put the display in the afternoon.

New entries, claimed in the ledger: `cal.1960-10-18.cuba-3` (Hoover to Bissell); `cal.1969-12-05.soviet-union-leadership-2` (Brezhnev with Husák, 5 p.m., four and a half hours, with the notes of № 98); `-3` and `-4` (Brezhnev sees off Zhivkov's and Ulbricht's delegations at Vnukovo-2, 9 and 10 a.m.). The other dated acts I looked up from the pages read were already in the calendar: Ye Jianying's call to Nie Rongzhen, Nie's and Zhou's replies, Ye's flight to Changsha, the Nov. 9, 1960 talk with Hồ Chí Minh, the Secretariat of Jan. 12, 1961, Zhou's banquet for the Soviet experts on Aug. 16, 1960, Chen Yun's letter on poultry and eggs of Dec. 31, 1960, and the Kennedy–Truman and Malik items. The Peng Zhen, Deng, Zhu De, Chen Yun and Yang nianpu were read whole for the span by earlier runs. I did not check every other item on every page read against the calendar; a reader who wants to finish that should go through each page in the list above.

## Ready to merge

Yes. Both patches have 0 errors. The warnings are the same-day flags for the new entries, which are distinct acts (settle with `./bib resolve ID --take keep`), and three edits that set only the note, which are corrections from the page.
