# Notes pass, batch 03: the audit

Auditor: Claude (Opus), Nov. 25, 2026, from about 9 p.m. to 1 a.m. Pacific. Brief: `notes/briefs/notes-pass-audit-03.md`. The patch audited and corrected in place: `inbox/2026-11-25-notes-pass-03.yaml` (the reader's version kept in my scratch directory until the end of the run, then deleted). `./bib patch-check`: 0 errors, 30 warnings, every one a "one event?" or "duplicate at the merge" flag on a new entry, each read against the entries of its day and found distinct (the merger keeps them with `./bib resolve ID --take keep`).

## How the pages were read

Every page an op cites was read, in the owner's copy or the linked record, except where said below. The copies came from the owner's Drive by `curl` (recipe 3 of `notes/guide/reading-a-copy.md`), each into my own scratch directory, and were deleted when done.

- Scans with no text layer, read as page images (pdfimages or pdftoppm, then the image read directly), the offset checked on the folio of each page read: *Peng Zhen nianpu*, IV (PDF = printed + 4): 10–11, 13 (not read; see Apr. 2), 17, 30, 33, 35–38, 45–47, 60, 71, 77–82. *Deng Xiaoping nianpu*, III (PDF = printed − 1328): 1537–1541, 1550, 1558, 1564–1565, 1593–1594, 1599–1600. *Yang Shangkun riji*, I (PDF = printed + 6): 495–496, 552–553, 622–623, 625, 627, 630–631. *Zhu De nianpu*, III (PDF = printed + 6): 1770–1771, 1775–1776, 1779. *Chen Yun nianpu*, III (PDF = printed + 5): 34, 38–40, 167. *Chen Yi nianpu* (PDF = printed + 13): 824, 1212. Wu Lengxi, *Shinian lunzhan* (PDF = printed + 8): 253–254, 258, 263–264, 309–313, 339, 341–343. Bu Weihua, *Zalan jiu shijie* (PDF = printed + 20): 12, 225. *Liu Shaoqi nianpu*, II (PDF = printed + 5): 491–492. *Ye Jianying nianpu*, II (PDF = printed − 553): 980. *Waijiao dashiji*, II (PDF = printed + 9): 143. *Jianguo yilai zhongyao wenxian*, XIII (PDF = printed + 15): 190, 213, 438. *Jianguo yilai Mao Zedong wengao*, XV (PDF = printed + 25): 249–250, 252, 401–402. Watson, *Into the Missile Age* (archive.org scan, leaf = printed + 39): 722–723.
- Text layers (`pdftotext`, the folio read off the running head of each page): Yang Jisheng, *Tiandi fanfu*, I, 530–531, 538–540; the *Zhou Enlai nianpu*, II, 330; Zelizer, 270–271; Bernstein, 357; Zaroulis, 144, 168–169; Califano, 255, 270, 316–317; Lady Bird Johnson, 618–620; Shesol, 36, 417–418; Thomas, 97, 102, 359; White 1960, 95–96, 115; White 1964, 411–414; White 1968, 162, 334–335; DeBenedetti, 215; Goodwin, 533; O'Brien, 242; Solberg, 208, 375; Friedman, 46, 52; Fursenko, 263–266; Dobrynin, 43; Novak, 23 n.5; Gifford, 137; Wofford, 24, 53; O'Donnell, 221–223; Westmoreland, 228, 230; Barrett, 104; Berman, 55–56; Sorensen, *Counselor*, 461–462; Witcover, 223–224; Dikötter, *The Cultural Revolution*, 125; MacFarquhar and Schoenhals, 141; Jian Chen, *Zhou Enlai*, 454, 577; Gibbons, IV, 585.
- The *Mao Zedong zhuan* EPUB, ch. 66 and ch. 76, read in its text, by the note numbers.
- FRUS from the repository's own copies (`sources/frus-text/`): 1964–68, V, docs. 149, 177, 239, 240; VI, docs. 68, 70, 103, 104, 176; 1958–60, IV, doc. 58.
- The *New York Times* of July 4, 5 and 6, 1960: the owner's screenshots of Nov. 23 on Drive (99 images), read by OCR (tesseract) and the passages found checked line by line.

## What could not be read, and why

- *Peng Zhen nianpu*, IV, 13–14 (the Secretariat of Apr. 2–3, 1960): the copy had been deleted before the Apr. 2 entry was reached. The reader's "Peng Zhen is there" stood on Deng, III, 1537–1538, which does not name him; it is struck from the add rather than moved to an unread page.
- Nothing else cited by an op was left unread.

## The ops: checked, changed, struck

All 10 `edit` ops that appended clauses are gone: their new words are now `add-words` ops, each cited to the record it came from (`text:` the FRUS document or the *Times*), or to the work's page. Each FRUS and *Times* passage was found in the record. Changes by entry:

- Apr. 27, 1967: words hold (FRUS V, 149). McNamara's question is Westmoreland's account and is cited to 228, not 227–28. Time set from FRUS's source note: 10:35 a.m., the first session; the inferred `time_range` (range_basis: kind) removed.
- May 19, 1967: holds (doc. 177).
- July 13, 1967: the reader had put FRUS V, doc. 240 into the news-conference entry. Doc. 240 is a separate meeting, 1:25–2:45 p.m., in the Family Dining Room, not the Cabinet Room, and it is Westmoreland, not Wheeler, who says the figures should not be announced. Now a new entry of its own. Westmoreland's 47,000 package is the decision of the meeting the day before (doc. 240 n.2 dates the plan July 12): moved to `cal.1967-07-12.vietnam-force-levels`. Barrett 104 and Berman 55–56 hold.
- Feb. 12, 1968: the cable (doc. 68, 0612Z) and the meeting (doc. 70, 1:45–3:08 p.m.) are two acts. The cable's words go into the entry, timed 0612Z; the meeting is a new entry, `follows` the cable. Open: the entry's existing parts {3} and {4} (the units sent; the Chiefs' call-up) belong to the meeting; moving them needs an edit of the line's cut parts, left for the merger or a later pass.
- Mar. 4, 1968: holds (doc. 104). Time set from the source note, 5:33 p.m., the Cabinet Room.
- Apr. 3, 1968: holds (doc. 176). The 90 percent and Humphrey are Sorensen's account (*Counselor*, 461–62), said so.
- July 3–5, 1960 (*Times*): hold, except that Truman's no comment of July 4 is his own act: now its own entry. The July 5 announcement takes its hour from Shesol, 36 ("one o'clock"), already cited.
- Nov. 15, 1960: holds (FRUS 1958–60, IV, 58).
- Sept. 6, 1966: holds (Bu, 225); n.60 is about the convener, not cited.
- Nov. 9, 1966: MacFarquhar dates the meeting of the seventeen factories Nov. 6; it is a separate act, now its own entry. Added from Dikötter, 125: the inauguration on Cultural Plaza and Cao Diqiu's "dregs of humanity."
- Jan. 24, 1967: Halleck's and Dirksen's words are their own acts (R9); now two entries. Halleck was the former House minority leader. Pinpoint 271.
- Feb. 3, 1967: the decisive-battle words hold (Mao zhuan, ch. 76, at n.11). The reader's "Jiang Qing's people did not show the article ..." is Mao's account to the Albanians on Feb. 3 (Bu, 12), now written as his.
- July 20, 1967: Mao zhuan holds. Yang Jisheng, 530–531: the 0:30 approach at the north gate is a separate timed act, now its own entry; the fourteen men demanded to be received, they did not bring a letter so worded. The main entry's time set to 5:10 a.m., the storming.
- July 25, 1967; Aug. 4, 1967: hold (Yang Jisheng, 538, 540; Jian, 577). Jian has "hundreds of thousands," Yang over 100,000; both kept, each by its source.
- Nov. 29, 1967: Bernstein holds. Zaroulis, 144, compresses: Clifford was not named on Nov. 29 (he was named Jan. 19, 1968). The add is struck and a Check put in its place.
- Jan. 17, 1968: Califano holds (255, the text and its footnote). Lady Bird Johnson, 618–19: "no clapping for the tax or civil rights" is not on the pages and is struck; her three minutes' applause at his entry added.
- Mar. 12, 1968: Moyers's words to Schlesinger, on the drive to "21," are their own act; now an entry. McCarthy's 42 percent is the primary's figure, not the dinner's; struck.
- Mar. 31, 1968: Califano, 270, says "a final edit," not "in his own hand"; reworded.
- Apr. 26–27, 1968: hold; King's reading made precise (notes said found in her husband's pockets).
- May 28, 1968: the vote is the primary's (struck here, put as a Check on `cal.1968-05-28.elections-1968-2`). O'Brien, 242 holds.
- Sept. 9, 1968: White, 334, says a rally "in downtown Philadelphia," not John F. Kennedy Plaza; reworded. White has reporters asking, Solberg a student panel: both given.
- Sept. 13, 1968: Porter's visit and Johnson's "We won't withdraw" were the evening before the hearings (Califano, 316), and Dirksen's withdrawal came after Tennery's testimony (317): both are new entries; struck from the Sept. 13 line.
- Jan. 25, 1969: holds; Chen Yun's page names Zhou Enlai too, added.
- Mar. 24, 1960: holds; Liao Luyan and Wu Lengxi added from Wu's own page.
- Apr. 2–4, 1960: Yang, 495, does not name Tan Zhenlin for the morning; reworded. Deng, 1537–38, does not name Peng Zhen; struck. The Politburo's hours (8 to 10 p.m.) added from Yang, 496. Time range: the morning of Apr. 2, the first act.
- Apr. 5, 1960: Solberg holds. White, 95–96, puts the pressure on Humphrey "in the next few days," not that night: now its own entry, the names confirmed on the page (Walter Reuther, Gov. Pat Brown, Orville Freeman, Jim Rowe).
- Apr. 10, 1960: the 38 and 10 percent are not on Deng, III, 1539–1540; the add struck and a Check added against the note's claim. The rest holds.
- Apr. 11, 1960 (Conakry): Sadat, Lumumba and Kasavubu hold. Liu Ningyi's "no peaceful coexistence" was in his report home after the conference, not at it: now its own entry.
- Apr. 11 (Jurentang), Apr. 16, May 6, May 20, May 23, June 10, June 16, June 23, June 18: hold, with these corrections: "heads hot but cooler" now "heads warm but cooler still"; Wu Zhipu named as the speaker of the Xinyang figures; the 1959 steel meeting sentence made faithful to Chen Yun, 38; the *Ten-Year Summary* pinpoint is XV, 250; Mao zhuan's two million is ch. 66, after n.31; Wu's Apr. 16 pinpoint is 263 (264 is a plate).
- May 1, 1960: Fursenko has the villagers see a parachute about 11 a.m. and reach Powers; "S-75" is not on the page; reworded. Time set, approximate, 11 a.m. Sverdlovsk time.
- May 14, 1960: the visit of May 9–14 and Hồ's reception are other acts; only the communiqué's words kept.
- May 15–17, 1960: Watson holds. Hagerty's announcement is dated May 17, evening, by Dobrynin, 43.
- June 1960 (WFTU): the second half of the add is the page's note (IV, 33 n.1), cited so (R35a). The early-June dinner and the East Europeans' word in Moscow (Friedman, 52) are new entries.
- July 5, 1960: the conference's directives and measures were not acts of July 5: now their own entry, dated by the conference's span with a Check for each day.
- July 8, 1960: holds; Wu dates Peng's report July 6 (309): a Check.
- July 14, 1960: Robert Kennedy put the chairmanship question to Rayburn, not to Johnson (O'Donnell, 221); fixed. Graham's call is on White 1964, 414. Shriver at 2:30 a.m. is already `cal.1960-07-14.elections-1960-los-angeles-2`; struck. Conway's warning is now its own entry.
- Sept. 10, Sept. 20 (Ponomarev "throws down" his pencils, not "snaps"), Nov. 7, Nov. 15, Nov. 22 (Sharkey is in Yang, 622, not in Peng; the add split by source), Nov. 24 (Yang also gives forty minutes), Nov. 25 (the delegation's names are on Peng, 79 and Yang, 627), Nov. 27, Nov. 30: hold, as corrected.
- Nov. 6, 1960: Thomas's leaflet words hold. The first printing (Oct. 29–30) and the reprint (by Nov. 1) are earlier acts: two new entries from Wofford, 24.

The name tags the reader set "by context" on Apr. 5, 1960 (Reuther, Freeman, Rowe) are confirmed on White, 95–96, and now sit on the new entry.

## Added by the audit

21 new entries, each claimed in the ledger under this patch: `cal.1967-07-13.vietnam-program-5-2`, `cal.1968-02-12.vietnam-tet-2`, `cal.1966-11-06.china-leadership-4`, `cal.1966-11-09.china-leadership-9`, `cal.1967-01-24.republican-party`, `cal.1967-01-24.republican-party-congress`, `cal.1967-07-20.china-leadership-20`, `cal.1968-03-12.robert-kennedy-campaign-decision`, `cal.1968-05-28.robert-kennedy-campaign-primaries-9` (Witcover's postmortem), `cal.1968-09-12.court-fortas`, `cal.1968-09.court-fortas-2`, `cal.1960-04.elections-1960-primaries-3`, `cal.1960-04.china-2`, `cal.1960-06.china-4`, `cal.1960-06.soviet-union-2`, `cal.1960-07-05.china-leadership-6`, `cal.1960-07-14.elections-1960-los-angeles-25`, `cal.1960-10-29.elections-1960-king`, `cal.1960-11-01.elections-1960-king`, `cal.1960-11-24.soviet-union-3` (Lukman), `cal.1960-07-04.elections-1960-nomination-6` (Truman's no comment of July 4, 1960). Times set by `edit` on nine entries (Apr. 27 and Feb. 12 and Mar. 4 above; July 20, 1967; May 1, July 5, Nov. 7, 24, 25 and 30, 1960), each from a clock time on the page; a morning range on Apr. 2, 1960.

Of the acts the reader's note named: the Red Workers' march is the rebels' own march of Nov. 9 (Dikötter does not describe a counter-march); entered. The Anting train and Zhang Chunqiao's arrival are already in the calendar (Nov. 10–12). The replies to Truman of July 2, 1960 and Truman's "no second choice" of July 5 are already entries (`cal.1960-07-02.elections-1960-nomination-4` to `-14`; `cal.1960-07-05.elections-1960-nomination-5`); nothing added.

## Left open

- `cal.1968-02-12.vietnam-tet`, parts {3} and {4}, to move to the new meeting entry (above).
- `cal.1960-06-16.soviet-union` is dated June 16 while the Peng and Deng chronologies put the talks June 17; a Check stands, the date not changed.
- Mao's comment of May 6, 1960 ("putting on a rival play") is dated by the Mao zhuan's note 19 (a record of May 6), the text saying only "later."
