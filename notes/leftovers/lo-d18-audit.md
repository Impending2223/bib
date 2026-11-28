# lo-d18: the audit (July to October 1966)

Opus audit, Nov. 28, 2026, of `inbox/2026-11-27-lo-d18.yaml`, the reader's note `notes/leftovers/lo-d18.md` and the batch rows `notes/leftovers/lo-d18.tsv`. The patch was corrected in place. `./bib patch-check` ends with 0 errors and 17 warnings: "sets only n" on six edits that take words out of a note or change a pinpoint, which additive ops cannot do; "one event?" and the duplicate flags on the five new entries (below); and a subentry warning on Aug. 18 that the tree already had. `./bib fields --patch` finds nothing. All 27 edits carry the rev the tree has now. Nothing in the brief narrowed what is an entry, so nothing was disregarded under R0.

## What was read

- The Mao nianpu (EPUB): July 16–18, Aug. 3–6, Sept. 9, 11, 13–15, Oct. 2, and the item "Oct. 31 or early November".
- The *Wengao*, XVIII (page images; the PDF page is the printed page plus 27): 316–17, 323, 362–65, 386.
- Yang Jisheng, *Tiandi fanfu* (text layers): I, 196, 214, 220, 224, 240; II, 665, 1043, 1145. Vol. II's p. 665 is PDF page 87, not 569 as the reader's note says.
- Pu Weihua (page images; PDF less 20): 124, 138, 175, 190, 206.
- The Zhou Enlai nianpu (2020), III (page images; PDF less 4): 42, 63, 71, 78, 83.
- The Liu Shaoqi nianpu (1996), II, 645–46; the Deng Xiaoping nianpu, III, 1924–25; Ma Qibin, *Zhizheng sishinian* (1991), 272. All three are page images.
- MacFarquhar and Schoenhals, 83, 128–29, 146; Teiwes and Sun, 34–36; Jian, 552–53.
- Lady Bird Johnson's diary, 402–04, 414, 417, 428–29; Branch, 509, 525–26, 567; Ralph, 143–44; Anderson, 230; Bernstein, 466; Shesol, 346 and its note at 532.
- The Public Papers, 1966, II, items 395 (849–56) and 501 (1117–24), in the series' text.
- The Daily Digest, D444–45 (govinfo); the Federal Register, 31 F.R. 9265–66 (govinfo); FRUS 1964–68, IV, doc. 254 (the series' text).
- The OKRA records 660710-000 and 660826-000; crmvet.org's two Chicago documents; the PRDE and Miller Center rows for July 5.
- *128 Hours* (San Francisco Police Department, 1966), pp. 1–11. It is open on archive.org (`128hoursreportof1968long`).
- Every copy was deleted after reading.

## Ops checked and what changed

The reader's 47 ops were all read against their pages. 28 hold as written. 15 were changed in some part. 4 were struck: the Aug. 18 src op, the July 23 check, the "By Aug. 26" entry and the Sept. 27 edit. The audit added 9 ops, among them the replacements for three of those four. The patch now has 52 ops: 27 edits, 6 new entries, 7 checks, 5 src, 2 follows, 1 primary, 1 cite, 1 to-check, 1 variant and 1 add-words.

**The two days moved.**

- **Tower's amendment (Aug. 19).** This holds. D444 has, on Aug. 19, two modified Tower amendments adopted, raising the limit on any one State from 12½ to 15 percent, and another Tower amendment rejected 27 to 53. Bernstein (466) gives the 15 percent amendment no day, and his "August 9" is the day of the rejected motion. The note now puts the Digest first, as the primary record, and Bernstein after it.
- **The Catskills speech.** It belongs on Aug. 19. The Public Papers (849) have Johnson at Ellenville that evening naming Kennedy, "a young man for whom I have the deepest respect," who joined him "this afternoon" after the Senate passed the cities bill. Shesol (346) has Aug. 21. The line said the *Monitor*'s headline came "the next day", but Shesol's note dates the story Aug. 22, so the line now says "Aug. 22". That is an edit of the line, `kind: correct`. **For the merger:** `cal.1966-08-21.elections-1966` is the same speech as `cal.1966-08-19.health`. Run `./bib combine cal.1966-08-19.health cal.1966-08-21.elections-1966`. Keep the health entry, which has the Public Papers first, the 8:14 p.m. hour and the place. Make `elections-1966` and `robert-kennedy` its other threads, and join the two lines by hand.

**The five splits.**

- **Aug. 3.** This holds. The nianpu puts the remark to Liu Lantao during his speech and the remark to Song during Song's speech. Pu (190) has the four speak in turn, Liu Lantao first and Song second. Added: a follows op that puts Song's speech (`-12`) after Mao's remark to Liu Lantao, on Pu, 190. The old note keeps the nianpu and Pu, which bear on its own act.
- **Aug. 25.** Corrected. Yang, II, 1043, read for this audit, dates the operations department's poster Aug. 25, from the General Staff's summary of 1979, and says it backed the foreign affairs bureau's poster. So the new entry is `cal.1966-08-25.china-red-guards`, not "By Aug. 26". The ledger claim was moved with `./bib ledger add` and `./bib ledger drop`. The entry follows `-3`, the bureau's poster, on that page. It now cites Teiwes, 34–35, which was read for this audit, with Teiwes's note 69. "Made public" is Zhang Yunsheng's book of 1988, with the authors' names left out; the earlier printing is the internal one. Pu's note 65 (Chen Hong, 1999) and Yang's note 36 (the 1979 summary) are behind "To check". The old line is Yang's account (I, 164) and keeps its variant from Pu. Teiwes stays on the old entry too, because it bears on the signatures and on the support of He Long's staff that the old line reports.
- **Sept. 15.** This holds: the *Wengao* (364) has "可以由两个人讲" dated 十五日上午十点半. The reader said the nianpu's "morning" was not for this paper. That is wrong: the nianpu has 上午 for both drafts. So the old entry now has a morning range of record, Peking, with "The words".
- **Oct. 2.** This holds. The nianpu has 社论发表后 ("after the editorial was printed"), and the Zhou nianpu (III, 71) has 后来 ("later"). Jian (552–53) was read for this audit and moved to the new entry. The old entry is now only the *Renmin ribao* reprint, which was public. So its "Made public: 2013" and the Check on "Made public" moved to the new entry, the talk. The old entry's tag `vis:only:prc@2` was taken off, because part 2 is no longer in its line.
- **Oct. 6.** This holds. The posts and Manila are items 1 and 2 at 1117. The box score is item 10 at 1120. Mrs. Johnson and the itinerary are items 18 and 19 at 1123. All are at 3 p.m., the East Room. Added: a follows op that puts the Cities answer (item 9) after the posts entry, on the transcript's order.

**The six new entries** were each held to R17 and R25b and against their pages. The one new act found is in Yang II, 1043, above.

**The hours.**

- **July 5.** This holds: PRDE and the Miller Center give 15:48 at the LBJ Ranch. The note now names both catalogues.
- **Aug. 2.** This holds, marked approximate. At 7:40 she phones; they are to be on the Portico ten minutes later; they come down "a few minutes late". That makes about 7:55 p.m. EDT, 23:55Z. The zone was added.
- **Aug. 4.** The night of the mass meeting (Branch, 509) holds. The morning of the YMCA meeting holds, but it is on Ralph, 144, not 143. Both notes now carry "The words".
- **Aug. 9.** This holds: "late Tuesday night" (Anderson, 230).
- **Aug. 15.** The id the batch row named was wrong. The 10 p.m. note (八月十五日二十二时, XVIII, 316) is the note on Chen Boda's and Kang Sheng's report about Li Xuefeng. The reader's op is on the right entry, `cal.1966-08-15.china-leadership-2`, at 14:00Z.
- **Aug. 18.** This holds. The rally opens at 7:30, and Zhou speaks after Lin. The 7:30 was taken off Zhou's speech and the morning range put in its place.
- **Aug. 20.** This holds: 8 p.m. at the State Pier, Maine on daylight time. The zone was added.
- **Sept. 1.** This holds: a newspaper story, the early-morning range of its kind.
- **Sept. 6.** Corrected. The afternoon is right (Branch, 525). But Georgia kept standard time in 1966 (`sources/daylight-time.yaml`), so the range of 17:00 to 23:00Z is right only with the zone `Etc/GMT+5`. The reader wrote `America/New_York`, and that was changed.
- **Sept. 9, Sept. 15 (late at night), Oct. 20 and Oct. 30.** These hold on the page's own words (晚上, 深夜, 凌晨).

**Aug. 6, the variant.** Corrected rightly. Yang's note 18 (I, 224) says the nianpu has the evening of Aug. 8. The nianpu as read has "that evening" under Aug. 6. The same wrong reading stood in the Check of `cal.1966-08-08.china-leadership-11`, and an edit corrects it. The Wu Faxian memoir (n.18a) was added behind "To check" on the Aug. 6 entry.

**Other changes.**

- **July 10 and Aug. 26.** The words describing the OKRA catalogue records came out of the notes (CLAUDE.md, "Do not"). A garbled running head, "ol VADLEY MOMENTS", was cleaned out of the Aug. 26 note.
- **July 19.** The Check now says which part rests on the calendar's July 26 entry, not on a page read.
- **July 23.** Settled in part. MacFarquhar's note 76 gives two sources. The Liu Shaoqi nianpu (II, 645–46) has only July 22, as do the Deng nianpu (III, 1924–25) and Pu (175); that is the meeting held in `cal.1966-07-22.china-leadership-7`. The *Zhizheng sishinian* (272) has report meetings under Liu from July 19 to 23, and "23日下午" ("the afternoon of the 23rd") Liu's words that most work groups are good. So the July 23 entry stands on that source. It is cited, and the Liu nianpu came out of "To check". The entry is not a duplicate of July 22.
- **Aug. 18, the src op on Pu, 206.** Struck. The page has Song Binbin and the school, but not her father, and the row would have mapped the whole first sentence to it.
- **Sept. 27.** The reader's edit took the only source read out of the note. That edit was struck and rewritten. *128 Hours* was found on archive.org and read. It is now the first cite, with a link and pp. 1–4. Its words are "Shortly after 2:30 P.M." for the first sighting, so the hour is marked approximate. The officer's name went into the line with add-words, from p. 3. The book also bears the sibling entries' hours: 7:35 p.m. at p. 7, and 11:39 and 11:44 p.m. at p. 11. Those entries can take it as their first cite.
- **Oct. 20.** MacFarquhar's "to little or no avail" is later commentary. It was moved from the note into a gloss (R19b).

## For the merger

The duplicate flags on `cal.1966-08-03.china-red-guards`, `cal.1966-08-25.china-red-guards`, `cal.1966-09-15.china-red-guards`, `cal.1966-10-02.china-red-guards` and `cal.1966-10-06.vietnam-asian-trip-2` are distinct acts: settle each with `--take keep`. `cal.1966-10-06.program` raises no flag. The one true duplicate is the Ellenville pair, above.

## What still waits, and on what

- **July 17, the place.** Waits for Zhou and Gu's *Shinian wenge dashiji*. It is not on the Drive and not on archive.org.
- **July 20.** Waits for Kuai Dafu's *Qinghua wenge wushi tian*, which is not on the Drive.
- **July 29.** This does not wait. No page read gives an hour, and the evening ranges stand.
- **Aug. 6.** Two accounts and no record: the nianpu has Aug. 6; Wu Faxian, by Yang, has Aug. 8. The Wu Faxian memoir is not held.
- **Aug. 31.** Waits for Sun Yancheng (2012) and Yu Luowen (2010), which Yang cites. Neither is held.
- **Oct. 4.** Waits on the network. digitalarchive.wilsoncenter.org does not resolve in this session; digitalarchive.umd.edu answers 403; web.archive.org is refused by the session's egress policy. The host would have to be allowed in the network settings.
- **Oct. 10.** Waits for Saigon 8262 of Oct. 12 (LBJ Library, NSF), which is not held. FRUS IV, doc. 254 (read) has the talks begin Oct. 10.
- **Oct. 23.** Waits for *Dadao Deng Xiaoping*, which is not on the Drive or archive.org.
- **Oct. 31.** Oct. 31 is the earliest day the record gives, as the Check says.
- Crowe's *Prophets of Rage* is on archive.org as a lending copy only. It was not readable here.

## Seen in passing, not in the patch

- `cal.1966-08-03.china-leadership-2` has its 9 p.m. stored as 13:00Z but no `time_zone`, so the day's list shows it at 09:00.
- `cal.1966-09-06.georgia` runs the Sept. 8 arrest of Carmichael into the Sept. 6 riot. That is two acts in one entry (R17).
- The Daily Digest gives Tower's planning-bill amendment as rejected 27 to 53 on Aug. 19. `cal.1966-08-19.cities-and-housing` gives the amendment to strike all but $24 million as 26 to 55 (voteview). The two votes should be compared.
- Teiwes dates the internally printed volume (vol. 26, p. 89) to October 1988. The card `w.zhonggong-dangshi-jiaoxue-cankao` says 1986.
- The 1979 summary of the General Staff (Yang, II, 1043 n.36) needs a witness row and an edge. They were not written, because this audit may not edit `sources/`.

## The Aug. 19 combine

- **Kept.** One entry, `cal.1966-08-19.health`, with the old id `cal.1966-08-21.elections-1966` as its alias. Its thread is Health, and School aid, Robert Kennedy and 1966 elections are its other threads. It keeps the hour (8:14 p.m.), the place and every fact of both lines. The parts keep their numbers: 1 is the Catskills sentence and 3 is the *Monitor*'s headline. The old part 2 was cut into 5, 6 and 8 (`cut_from`), and the new parts are 4, 7 and 9. The claim map has one row for each source, and its hash is the hash of the line without its marks (3755ae9d).
- **Moved.** The Public Papers' parenthetical (Kennedy "joined" that afternoon after the Senate passed the cities bill) went into the line as part 7. The line now follows the Papers' order, with Kennedy named (849) before the congressmen are presented (849–50). The note says so and keeps Shesol's other order (346). Thomas's parenthetical came out: its date is in the sentence on Aug. 21, and its headline is in the Check. Thomas's *Times* of Nov. 14, 1966 went from the Check into "To check". Shesol's titles for the *Newsweek* and *U.S. News* items were added. The sentence that pointed to the entry itself was dropped. The Check sentence now comes after "Names:".
- **Read.** The Public Papers, 1966, II, 849–56, in the series' text, with Kennedy at 849, the school bill story at 853–54 and the 8:14 p.m. note at 856. McPherson, 328–29. Shesol, 345–46, and its notes at 531–32: the *Monitor*'s date, Aug. 22, is printed at 531, in the note to 345. Thomas, 327, and its note at 461, not 462. Each work was read from the Drive copy's text layer and page images, and every copy was deleted afterwards.
