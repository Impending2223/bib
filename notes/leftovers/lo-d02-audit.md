# Audit of leftovers lo-d02 (April to June 1960)

Opus audit of the reader's patch `inbox/2026-11-27-lo-d02.yaml` and note `notes/leftovers/lo-d02.md`, Nov. 27, 2026. The patch is corrected in place. `./bib patch-check`: 0 errors, 18 warnings, all of them the merge's duplicate flags on the 9 new entries. Nothing merged, built or committed. Nothing in the brief narrowed the work, so nothing was disregarded under R0.

## What was read

Each copy was fetched from the owner's Drive by the download line of `notes/guide/reading-a-copy.md`, read as page images, and deleted after.

- Zhou Enlai waijiao huodong dashiji: pp. 273, 274, 276, 277, 281, 282 (PDF page = printed + 13).
- Chen Yi nianpu: pp. 809, 810, 812, 813, 818, 819, 930 (PDF page = printed + 13).
- Zhonghua renmin gongheguo waijiao dashiji, vol. 2: pp. 138, 139, 145, 146 (PDF page = printed + 9).
- Zhou Enlai nianpu, 1949–1976, vol. II: pp. 303–305, 314, 323, 470 (PDF page = printed + 3; the text layer for finding, the image for p. 470).
- Peng Zhen nianpu, vol. IV: pp. 13, 14, 35, 204 (PDF page = printed + 4).
- Deng Xiaoping nianpu, vol. III: pp. 1565 (n. 1), 1700, 1722 (printed = PDF page + 1328).
- Zhu De nianpu xinbian, vol. III: pp. 1834, 1849 (PDF page = printed + 6).
- Yang Shangkun riji, vol. I: pp. 504–513, 516, 518, 519 (PDF page = printed + 6).
- Wu Lengxi, Shinian lunzhan: p. 279 (PDF page = printed + 8).
- Mao Zedong nianpu (EPUB): May 3, 6, 7, 8, 9, 14, 17, 21, 22, 28 and June 7, 16, 1960.
- Mao Zedong zhuan (EPUB): ch. 66, the passage on the three Lenin articles and notes 18–20, 27.
- Smith, On His Own Terms: pp. 340–341 and the notes to p. 341 (printed p. 763).
- Records online: Peking Review, no. 18 (May 3, 1960), pp. 3, 6, 8 (marxists.org); The Tech (MIT), Apr. 25, 1962, Alan Levy's article (tech.mit.edu).

## The five items the reader left unread

- Deng's attendance on Aug. 26, 1962: Deng nianpu III, 1722 has him at the preparatory meeting for the Tenth Plenum, Aug. 26 to Sept. 23. Added to `cal.1962-08-26.china-leadership` ("Deng Xiaoping attends.") with its name and tag.
- The "king" reading of Apr. 26, 1960: the Waijiao dashiji, 139, has Zhou and Chen Yi call on "the king of Nepal, Himalaya Bir Bikram Shah Deva" in the visit of Apr. 26–29, with no day. The joint communique of Apr. 29 (Peking Review, no. 18, p. 6) has "His Royal Highness Prince Himalaya". The king reading is kept as a variant on the Prince entry, with a Check.
- The calls on Prince Himalaya of Apr. 26 and 27: one call, entered on Apr. 26. The Waijiao huodong (276) has it Apr. 26 at 4:30 p.m., and the Zhou nianpu (II, 314) has Zhou call on Koirala and the Prince in turn that day. The Chen Yi nianpu (813) has a call at 4:30 p.m. on Apr. 27 and none on the 26th, but its own page puts Zhou at Pokhara from the morning of the 27th to the morning of the 28th, and the Waijiao huodong (277) has Zhou in talks with Koirala at Pokhara at 4 p.m. on the 27th. Neither chronology has two calls. The reader's Apr. 27 entry is struck and its ledger claim dropped; Chen Yi's day is a variant of the date field on the Apr. 26 entry, and the entry keeps a Check, since no record settles the day beyond doubt.
- The day of Mao's "putting on a rival play": May 6, 1960. The Mao zhuan's text says only that Mao "later" said it of the three articles, but its note 19 gives the source of the quoted words as the record of Mao's talk with the Henan Provincial Committee's heads, May 6, 1960. The work therefore dates the remark May 6, and the entry already stands on that day. The reader's added Check is struck. The Mao nianpu's May 6 entry (evening, on the train, Wu Zhipu, Yang Weiping, Shi Xiangsheng, Zhao Wenfu) does not print the remark.
- The day of "the fine hand of Emmet": not settled. Smith's source (341, note) is Alan Levy, "Today's Writing: Art or Séance?", The Tech (MIT), Apr. 25, 1962, which says only that Eisenhower said it when Rockefeller "fired off a pre-convention blast". No source gives the day or the hearer. The entry stays June 8–9 with its Check, now citing Levy, with "Made public" set to the Levy article, the earliest printing found.

## Ops checked, changed, struck and added

62 ops in the reader's patch were checked against their pages. The corrected patch has 72.

Struck:

- The new entry `cal.1960-04-16.china-zhou-foreign` (the Ne Win call, 3 p.m.) and its `follows`. The tree already holds that call with its hour, `cal.1960-04-16.china-leadership-3`. The reader marked the merge's duplicate flag as a distinct act, but it was a true duplicate. The ledger claim is dropped. The edit of `cal.1960-04-16.china-leadership-2` now points to `-3`. Added on `-3`: `follows` after `-2` (the Waijiao huodong, 273: the calls of the early morning and the morning, then Ne Win at 3 p.m.); the words "Chen Yi and Zhang Hanfu with him" from Chen Yi 810, with their names; and `place: rangoon`.
- The new entry `cal.1960-04-27.china-zhou-foreign` (see above).
- The `follows` that put the Prince's call after the citizens' meeting of Apr. 26 by the printed order of the Waijiao huodong. The Zhou nianpu (II, 314) prints the two calls before the meeting, which goes against that order. The pair is left without a link, with the pages read: Waijiao huodong 276, Zhou nianpu II, 314 and Chen Yi 812. The call has its hour (4:30 p.m.) and the meeting its afternoon range.
- The Check added to `cal.1960-05-06.china-leadership-6` (see above).

Changed:

- The Koirala and Prince calls of Apr. 26 now cite the joint communique (Peking Review, no. 18, p. 6) and the Zhou nianpu (II, 314). The communique announced both calls at the time, so "Made public: 1993" and the `vis:only:prc+nepal` tags are taken off. The Prince entry adds "Chen Yi present" (Chen Yi 813; the Waijiao dashiji, 139), the date variant from Chen Yi and the "king" variant from the Waijiao dashiji.
- The citizens' meeting of Apr. 26 also cites the Zhou nianpu (II, 314).
- The edit of `cal.1960-04-26.china-leadership-2` keeps only the arrival in each parenthetical. Added from the Waijiao huodong (276): Koirala and nearly all the country's leaders at the airport; the capital takes a holiday. Koirala is named and tagged.
- The edit of `cal.1960-04-16.china-leadership-2` adds "Chen Yi with him" (Chen Yi 809–810), with his name and tag.
- The wreath of May 27 (new entry) adds Chen Yi and Molomjamts from Chen Yi 818, and cites the Zhou nianpu (II, 323, "乔巴山陵园"). The edit of `cal.1960-05-27.china-leadership-2` keeps only the arrival in Chen Yi 818's parenthetical, and adds "Tsedenbal meets him at the airport" from the Waijiao huodong (281), with his name and tag.
- June 7, the report to Mao (new entry): the long quotation of the Mao nianpu is cut to the words of the hour, 下午四时.
- `cal.1960-05-25.china-leadership-8`: 中午 is a part of the day, not an hour. The loose `time` of 12:00 becomes the house's "workday midday" range (12 to 2 p.m.), as for the other 中午 entries of the diary.
- `cal.1960-05-14.china-leadership-7`: the reword keeps "delegations" (the reader had "delegation"). The audience was of several Japanese delegations.
- `cal.1960-06-16.soviet-union`: the day of June 17 holds. Wu, 279, has the delegation leave Peking on June 16, reach Moscow that day and meet Kozlov "the next day". Peng Zhen IV, 35 has 3 to 11:20 p.m. Moscow time on June 17. Deng III, 1565 n.1 has June 17. The line now reads "arrived from Peking the day before", where the reader had "which left Peking June 16 ... the next day". The note's sentence on the day is rewritten to name the record that settles it. The Deng footnote is cited.
- `cal.1960-05-16.china-leadership` (Mao's talk with Zhou and Chen Yi, which the report of Zhang Yan and Luo Qingchang now follows): the evening band becomes the diary's own hours, 9 p.m. to 12:30 a.m. (Yang I, 508).
- Reception of the Nepal Chamber of Commerce, `cal.1960-04-26.china-leadership-6`: `follows` after the Prince's call, by the printed order alone (Waijiao huodong 276–277).
- The order of ops: every additive op on an entry the patch also edits now comes after the edit. A trial merge in a scratch copy showed that the reader's order recorded conflicts on `cal.1960-05-16.china-leadership-7` and `cal.1960-05-21.china-leadership-7`, and broke the cut marks of `cal.1960-06-07.china-leadership`.

Held as the reader wrote them, each against its page: the Apr. 18 split (Waijiao huodong 274; Chen Yi 810; Zhou II, 305); the variant of 6:35 p.m. for Pant (Chen Yi 812); the Koirala call at 1:30 and the citizens' meeting; the Apr. 30 swim (Yang I, 504); the two May Day poems and their `follows` (Chen Yi 813, "之后"); the hour ranges of May 3, 7, 8, 9, 14, 17, 21, 22 and June 16 (Yang I, 505–511, 519), each consistent with the Mao nianpu's part of the day; May 16's report from 12:30 to 2:30 a.m. (Yang I, 508); the call to Peng Zhen of May 21 with no hour (Yang I, 510); Jespersen at 3:30 p.m. (Yang I, 513); Lin Boqu's death at 10:40 a.m. (Yang I, 513; Chen Yi 819); the Ulan Bator split (Waijiao huodong 281–282); the June 7 split and its `follows` (Mao nianpu, June 7; Yang I, 516); the attendances of 1960 and 1962 (Peng IV, 13–14 and 204; Zhou II, 470; Deng III, 1700; Zhu De III, 1834 and 1849; Chen Yi 930); the 328th meeting (Peng IV, 204). The May 10 item needs nothing (Yang I, 506–507, already a variant on both entries). The Kabaservice item is a 1966 item already in the tree as `cal.1966-03.elections-1966`; its pages were not read again.

Times and zones were checked with zoneinfo: Asia/Yangon +6:30, Asia/Kathmandu +5:30, Asia/Kolkata +5:30, Asia/Ulaanbaatar +7, Asia/Shanghai +8 and Europe/Moscow +3, all in 1960. The day order was printed for April to June 1960 (`tools/times/day_order.py`) from a scratch copy with the patch merged, and read for every day the patch touches. A full `./bib check` on that copy gave 0 errors.

## Bases and the merge

All 28 edit bases match the tree as it stands at the end of this audit. At the merge, settle these duplicate flags as distinct with `./bib resolve ID --take keep`:

- `cal.1960-04-18.china-zhou-foreign`
- `cal.1960-04-26.china-zhou-foreign`
- `cal.1960-04-26.china-zhou-foreign-2`
- `cal.1960-04-26.china-zhou-foreign-3`
- `cal.1960-05-01.china-leadership-13`
- `cal.1960-05-01.china-leadership-14`
- `cal.1960-05-27.china-zhou-foreign`
- `cal.1960-06-07.china-mao-foreign`
- `cal.1960-06-08.elections-1960-rockefeller`

## What still waits

- The day and the hearer of Eisenhower's "fine hand of Emmet". It waits on a record of his remark (the Whitman diary or the Eisenhower papers for June 8–9, 1960). Nothing read gives either.
- The day of the call on Prince Himalaya, between the Waijiao huodong and the Zhou nianpu (Apr. 26) and the Chen Yi nianpu (Apr. 27). It waits on a dated report of the time: Xinhua, Renmin ribao or the BBC's Summary of World Broadcasts for Apr. 27–28, 1960, the last already behind "To check:" on the arrival entry.
- The witness registry. Two rows are not registered: Levy's article in The Tech, as the witness behind Smith 341's note, and the joint communique as printed in Peking Review. This audit may not edit `sources/`, so both wait for the merger.
- Found in passing and not changed: Chen Yi 812 puts the cable to Olympio of Togo on Apr. 26, while the tree has `cal.1960-04-27.china-2`; the Mao nianpu has Mao dine with Jespersen on May 28, which `cal.1960-05-28.china-leadership` does not say. Both are for a later pass.
