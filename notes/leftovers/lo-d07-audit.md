# Audit of lo-d07: March to June 1961

The Opus audit of the reader's patch `inbox/2026-11-27-lo-d07.yaml` and note `notes/leftovers/lo-d07.md`, Nov. 27, 2026. Every op was held to its page. The patch is corrected in place; `./bib patch-check` gives 0 errors (29 warnings, all the usual "one event?" and "duplicate of ...?" flags and three "sets only n" notices). Nothing in the brief narrowed what is an entry, so nothing was disregarded under R0.

## What was read

- Yang Shangkun's diary, I, 659, 665, 666, 667 and II, 1, 3, 26, 37, as page images (I: printed page plus 6; II: plus 5).
- The Zhou Enlai nianpu, II, 396, 399, 403, 404, 408, 409, 410, 411, 415, as page images (plus 3).
- The Zhou *Waijiao huodong dashiji*, 307 and 313, as page images (plus 13).
- The Chen Yi nianpu, 869, 871, 872, as page images (plus 13).
- The Mao nianpu EPUB, Apr. 25 and June 13, 1961.
- *Jianguo yilai zhongyao wenxian*, XIV, 412 and 416, as page images (plus 15).
- The Deng Xiaoping nianpu, III, 1619, 1633, 1634, 1635, 1639, as page images (PDF page = printed page less 1328).
- The Peng Zhen nianpu, IV, 130 (plus 4), and the Chen Yun nianpu, III, 86 (plus 5), as page images.
- Yang Jisheng, *Mubei*, II, 832 (page image); *Tiandi fanfu*, I, 369 (text layer); Dikötter, 238 (text layer).
- MacFarquhar, III, 32, 211 and the notes (text layer); Salinger, 148–49, 177, 178, 184, 186; O'Donnell, 335 and the passage of the Bay of Pigs night; Schlesinger, *Robert Kennedy and His Times*, 295, 380; Schlesinger's *Journals*, 111 (page image) and 113–14; Taylor, 185; Reeves, 120, 146–47, 181; Nixon, *RN*, 233; Sorensen, 539; Sundquist, 57–58 with notes 2 and 4; Branch, 429–30; Kaplan, 248 with n.75; Poole, 111 (the DTIC copy on archive.org).
- Records online: the 1961 Public Papers (pp. 135–39 and the note on the hour, 220, 307, 379–80, 382–86, 488–90); FRUS X, docs. 218 and 219; FRUS XVII, doc. 24; FRUS XXIV, doc. 122 and its note 1; Proclamation 3401 on the American Presidency Project; 107 Cong. Rec. 10494–95 and 10522; 75 Stat. 131; the FRASER item cited for Heller.
- Each copy was deleted after use. A scratch copy of the tree, with the patch merged in it, was used to read the claim maps and the day's order (`tools/times/day_order.py`), and was deleted after.

## The five moved dates

- Apr. 11 to Apr. 12 (Zhou's cable to Khrushchev): kept. The nianpu prints the cable as an item under the heading of Apr. 11, among items that run on to the talk with U Nu, which the *Waijiao huodong* (307) and the Chen Yi nianpu date Apr. 12; the *Waijiao huodong* dates the cable Apr. 12; the cable answers the flight, which the tree has on Apr. 12. Added: a variant for the nianpu's Apr. 11, and a `follows` link after `cal.1961-04-12.space`, since the line says the cable was sent on learning of the flight.
- Apr. 18 to Apr. 19 (Kennedy's walk in the Rose Garden): kept. Salinger (148–49) has the walk after a conference that began when Kennedy left the reception at midnight and ended at 4 a.m.; Schlesinger's *Journals* (113–14) has the meeting break up about 2:00; O'Donnell's "Tuesday night" stays as a variant. The time range, 2:00 to 4:45 a.m. EST, holds.
- May 15 to May 16 (the riders' landing at New Orleans): kept, tempered. Branch (429) has the plane lift off "near midnight" and Marshall's call four hours later, and no hour of landing; Schlesinger (295) gives no day. A Check on the hour of the landing was added.
- June 18 to June 16 (the urgent directive on the urban population): kept, tempered. The directive's text is dated June 16 (*Jianguo yilai zhongyao wenxian*, XIV, 416), the nine measures were approved June 16 (412), and MacFarquhar (III, 32) has the nine-point plan issued June 16. But Yang Jisheng, in both *Mubei* (II, 832) and *Tiandi fanfu* (I, 369), has the Center send out (發出) both papers on June 18, and Dikötter has the order on June 18. The date of the text and the day it was sent may differ, so a Check on the day of issue was added and the three variants were kept.
- June 26 to June 25 (Harriman and Souvanna, at Geneva): kept. FRUS XXIV, doc. 122, is Harriman's own cable from Geneva, and its note 1 puts the talk late in the evening of June 25, with Souvanna leaving for Paris next morning. Kaplan (248) has Paris and June 26, and that stays as a variant. The claim map was set: the FRUS document stands for the whole line, and Kaplan for no part. The witness Kaplan's note cites (`x.1961-06-26.conle-287-geneva-to-state-june-26`) is marked read, with the FRUS print as its copy (`inbox/witnesses/2026-11-27-lo-d07.yaml`).
- The May 16, 1961 tree planting (`cal.1961-05-16.transition-and-staff`): Dallek's *An Unfinished Life* is not on the Drive (a title search for "Unfinished" and "Dallek" found only *Flawed Giant*, *Lone Star Rising* and Matthew Dallek). Reeves (120) puts the visit on May 17 and gives no day for the tree planting; the Papers have the arrival on May 16 at 4:56 p.m. (380) and the address to Parliament on May 17 at 3:27 p.m. (the hour is on 386, now cited). The Check on the day of the injury stays.

## Changed

- Patman's letter of Mar. 30 was a second act in Martin's entry of Mar. 7, so it is split out under R17 as a new entry, `cal.1961-03-30.economy` (claimed in the ledger). It has a Check, because no source read bears it. The note on Mar. 6 now points to both entries.
- `cal.1961-03-03.china-leadership-4`: the Zhou nianpu (II, 396) has Zhou at the evening Standing Committee and the discussion of imports and exports, which the split had dropped from the line. They are added with `add-words`, and Zhou is named.
- `cal.1961-04-12.china-leadership-2`: the band "afternoon" is set beside the talk's range.
- `cal.1961-04-25.china-leadership`: the 9 a.m. hour lacked its time zone and showed as 8 p.m. Washington time. Asia/Shanghai is now set.
- `cal.1961-04-25.china-leadership-11`: the Mao nianpu says the draft notice was discussed (讨论), so the line now reads "on the draft notice", not "settles". The entry now follows `cal.1961-04-25.china-leadership-8` (Deng and Tian drafting it), on the Deng nianpu (1633–34).
- `cal.1961-05-02.china-leadership-3`: the place is set, Peking.
- `cal.1961-05-08.china-leadership-3`: Zhou's Soviet reply was split out of this entry, so the entry is now the morning session on the commune regulations and industry. Its thread is changed from china-foreign to china-sixty-articles (also farm), the Soviet tag is taken off, and the place is set.
- `cal.1961-05-08.china-leadership-17`: the entry now also follows Zhou's return (`-2`). Yang's words: back from Handan at 12 to join the meeting.
- `cal.1961-05-15.china-leadership-9`: the Chen Yun nianpu gives 下午三点 (3 p.m.), so the hour is exact, not approximate.
- `cal.1961-05-17.china-leadership-5`: the hours Yang gives (the morning to 1 p.m., and 3:30 to 6 p.m.) and Peng Zhen's presence are added to the line from the cites the patch adds. The entry takes the morning's range and the place Peking. Its edit comes before the additive ops, so it merges without a conflict.
- `cal.1961-05-31.china-leadership-2`: MacFarquhar gives Liu's warning no day and no order against Chen Yun's speech. The Check now says only that.
- `cal.1961-06-15.congress`: the Vice President swore Tower in (the Record, 10522), so Johnson's tag is added.
- `cal.1961-06-30.program`: LeMay's tag comes off with his sentence. `cal.1961-06-30.defense`: from the Papers item now cited, the line adds that LeMay was sworn in at the White House, in the Rose Garden, with Kennedy speaking; Kennedy is named.

## Held as the reader wrote them

All other ops held on their pages. These include the splits of Mar. 1, 3, 7, 10, 13, 14, 16, 24, 25 and 31, May 2, 8 and 14, and June 15 and 30; the hours of Mar. 1, 3, 4 and 15, Apr. 12, 15 and 25, May 2, 7, 8 and 28, June 3, 13, 24 and 30; the name Josef Hegen; and the day of May 16 for the Cuba Study Group luncheon. FRUS X, doc. 218 is titled "Meeting with President on May 16, 1961", and Taylor's May 15 stays as a variant. The reader's two "read, left" items stand: Yang's diary (I, 665) gives no order for the decision on Liu Xiao, and the Cabinet of Apr. 20 is already one act. Nothing was struck.

## The bases

Every `edit` base matched the tree as it stands (40 edits). One edit was added, on `cal.1961-05-17.china-leadership-5`, base `8a6d243b`. Merged in a scratch copy with the 13 flags settled as `keep`, the tree checks with 0 errors and no other conflicts.

## Duplicate flags to settle as distinct at the merge (`./bib resolve ID --take keep`)

Each of these is a separate act, split out of an entry under R17 or R25b:

- `cal.1961-03-01.africa-2`
- `cal.1961-03-10.foreign-aid-2`
- `cal.1961-03-13.foreign-aid-2`
- `cal.1961-03-15.cuba-4`
- `cal.1961-03-16.middle-east-2`
- `cal.1961-03-24.jobs-and-wages-2`
- `cal.1961-03-25.china-leadership-9`
- `cal.1961-03-31.cuba-3`
- `cal.1961-04-25.china-leadership-11`
- `cal.1961-05-02.china-leadership-10`
- `cal.1961-05-08.china-leadership-15`
- `cal.1961-05-08.china-leadership-16`
- `cal.1961-05-08.china-leadership-17`

## Still waiting

- `cal.1961-05-01.laos-2`: Mansfield to Kennedy, May 1, Vice-Presidential Security File, Johnson Library. The file cannot be reached from here.
- `cal.1961-05-16.transition-and-staff`: the day of the tree planting. Dallek is not on the Drive.
- `cal.1961-03-30.economy`: Patman's letter. No source in hand bears it.
- `cal.1961-03-01.africa-2`: Williams's place, Kenya. Neither the Papers nor Sorensen gives it.
- `cal.1961-03-13.foreign-aid-2`: the days of the hearing and of the withdrawal. Schlesinger gives neither, and Mollenhoff's *Washington Cover-Up* is not on hand.
- O'Donnell's p. 307: the passage was read in the text layer, but its printed page was not seen on an image.
