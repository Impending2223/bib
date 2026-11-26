# China threads, batch A: the audit

Nov. 26, 2026. An audit by reading of the reader's placings in `notes/threads/read/batch-a.tsv`, under `notes/briefs/china-threads-read-audit-a.md`. The rule I judged by is the assignment of the reader's brief, `notes/briefs/china-threads-read-a.md`, rule 1 (ruling 59: the episode first, then the person thread of Mao, Zhou or Liu where he acts, then the system; every other thread that plainly fits goes in `also`). I changed nothing in `lists/`, `th.yaml` or `sources/`. I merged, built, committed and pushed nothing.

## What I read

I read the entries straight from `lists/cal/*.yaml` with a script of my own, the whole line and the whole note of each, Chinese characters, "Made public", "To check" and "Check" sentences included. I read `th.yaml` for every China thread and its statement, and the entries the calendar already holds under Twelve Articles for November 1960 to January 1961 and under the Center's daily work for the "five many", to see how those threads are filled.

I read these whole, 125 entries in all:

- The 13 entries the reader listed as undecided or close.
- The 10 entries on threads that take fewer than five of the batch's entries as primary: Foreign affairs (4), Shanghai and Beidaihe, 1960 (3), United front and nationalities (3).
- The 26 entries the reader kept in `china-leadership` (two of them are also among the undecided, and one of the United front entries is too, so these three groups hold 45 entries).
- A random sample of 80 of the other 252, drawn with the seed 58213.

To look for faults of the same kind across the batch, I also read whole 10 more entries outside those 125 (among them `cal.1960-10-07.china-leadership-2`, `cal.1960-03-14.china-leadership-9`, `cal.1960-03-22.china-leadership-11`, `cal.1960-03-02.china-leadership-4`, `cal.1960-03-08.china-leadership-4`, `cal.1960-05-24.china-leadership-4` and `cal.1960-04-07.china-leadership-10`). For the rest of the batch I read only the opening of each line, 200 to 300 characters, thread by thread and by searches for Mao, Zhou, Liu, foreign countries and the months of the Twelve Articles, the Shanghai meeting and Beidaihe. Those openings are not counted as read whole.

## The checks by script

Over the whole tsv, before and after my mends: every id of `batch-a-ids.tsv` has one row (297), and no row is extra or repeated. Every slug is in `th.yaml`. No thread stands beside its own parent or child. No `also` holds the primary thread. No `also` holds the Center's daily work. No `also` has a space. All passed.

## The counts

Of the 125 read whole, 119 are right and 6 are wrong. The search for faults of the same kind found one more, so I mended 7 rows.

By kind of fault:

- An episode missed (2). Deng Zihui's report to Mao of Nov. 21, 1960 on three-level ownership on the brigade, and Hunan's request of Dec. 13, 1960 on the size of the basic accounting unit, are the business of the Twelve Articles. That thread already holds the communes' rectification of those months. Both are now primary on Twelve Articles. I found no other entry of the batch of this kind.
- A lesser figure's day put on a system (2). Zhu De's talk with Jin Handing, "an old friend of the Yunnan army", states no business, so it goes back to `china-leadership`, not United front. Yang Shangkun at the Yulin naval port and in a submarine is sightseeing on his tour with Deng's party, so it goes to `china-leadership` with Army second, as the reader did for a leader's visit to an exhibition. It was the only tour visit of this kind on Army.
- Mao's thread missing as a secondary thread (3). The reader's rule was to leave Mao off where he only hears a report. But Mao's statement names his audiences, and the calendar elsewhere gives Mao's thread to the meetings where he hears reports. The three Military Commission reports made at Mao's meetings (Feb. 12, Oct. 7 and Dec. 4, 1960) now carry `china-mao` in `also`. A report sent to the Center and Mao in writing is not his act, and I added nothing to those.

Each mended row's `basis` begins with `AUDIT:`, says why, gives the old placing in brackets, and keeps the reader's words after "Reader:". After the mends the primary counts are: Propaganda and culture 75; Agriculture 63; Army 55; `china-leadership` 28; Finance and economy 20; Famine 17; Mao Zedong 12; Organization 11; the Center's daily work 5; Foreign affairs 4; Shanghai and Beidaihe, 1960, 3; United front and nationalities 2; Twelve Articles 2.

No thread that plainly fits was missing from the rows I read, apart from the three Mao rows. In the 125, I found no entry where Zhou Enlai or Liu Shaoqi acts and lacks his thread.

## Close calls I left as the reader had them

These have two fair readings. I left the reader's choice, since it is not plainly wrong.

- `cal.1960-03-14.china-leadership-9` and `cal.1960-03-22.china-leadership-11`: Licheng county's report on the "five many, five few", and Shandong's forwarding of it. The reader put them on Organization (the cadres' style). The Center's daily work names "the five many" among its stations, and the calendar files the campaign in the central organs there. A row could take either. The Center's daily work cannot be a secondary thread, so the choice is all or nothing.
- `cal.1960-10-09.china-leadership-13`: Chen Yun talks with Deng Zihui, no business stated, put on Agriculture by Deng's office. The batch places such talks by the office of the man met (Zhu De with the General Staff's Third Department), as ruling 58 does for callers on the General Office. I let it stand.
- `cal.1960-03-02.china-leadership-4`: Yang Shangkun with the commander of the Central Guard Regiment on its work. Army, or the Center's daily work, since the regiment guards the Center.
- `cal.1960-05-24.china-leadership-4`: Tian Jiaying and Yao Zhen arrive at Hangzhou. Propaganda and culture by Yao's office, though the series of sessions on the fourth volume they came for is on Mao's thread.
- `cal.1960.china-leadership-121`: Ye Qun made director of Lin Biao's office. Army, or Organization as an appointment.

## The reader's undecided entries, and my ruling on each

- `cal.1960-11-21.china-leadership` (Deng Zihui on adjusting the communes) and `cal.1960-12-13.china-leadership-10` (Hunan on the accounting unit): Twelve Articles, not Agriculture. Mended.
- `cal.1960-05-09.china-leadership-5` (the Secretariat adopts four rural directives) and `cal.1960-08-10.china-leadership-4` ("Everyone in the Party to farm grain"): Agriculture stands. Their business is farm labor and farming as a whole. Famine cannot also be named, since it is Agriculture's child.
- `cal.1960-05-15.china-leadership-11` (the grain distribution directive) and `cal.1960-09-23.china-leadership-5` (the oil sales cut): Famine stands. Both are measures against the shortage.
- `cal.1960-05-31.china-leadership-6` (a Hangzhou session on the fourth volume, Mao not named): Mao Zedong stands, with the series of sessions at his pool.
- `cal.1960-02-22.china-leadership-7` (the Harbin urban commune) and `cal.1960-03-04.china-leadership-6` (Peng Zhen and the Women's Federation on street residents): Agriculture stands, with the secondary threads the reader gave. Agriculture's statement names "the communes" without limit, and no other thread's statement names the urban communes. The same holds for the batch's other urban commune rows (`cal.1960-02-18.china-leadership-2`, `cal.1960-04-02.china-leadership-6`, `cal.1960-04-20.china-leadership-13`, `cal.1960-05-11.china-leadership-9`). If the owner wants the urban communes out of Agriculture, these six rows are the ones to move.
- `cal.1960-04-20.china-leadership-14` (Zhu De hears the Tibet Military Region's commissar): United front and nationalities, with Army second, stands.
- `cal.1960-10-29.china-leadership-7` (Zhu De and Jin Handing): `china-leadership`. Mended.
- `cal.1960-01-30.china-leadership-4` (Yang Shangkun on Hainan) and `cal.1960-02-13.china-leadership-5` (Yang Shangkun at an exhibition hall and a lunch): `china-leadership` with Agriculture second stands.

## Is the batch fit to apply

Yes, as mended. The faults were 6 in 125 read whole, about one in twenty. They were of three small kinds, and I searched the batch for each kind and mended every row I found. The structure checks all pass. The close calls above can be moved later by rule without harm.

One note on the file. The commit `16ab7a33` made by the orchestrating session holds an earlier state of my mends, in which a script had put a backslash before every double quotation mark in five reader rows. The later commit `08f0a690` holds the corrected file: `git diff 0248ce71 08f0a690 -- notes/threads/read/batch-a.tsv` shows only the 7 mended rows.

Nothing in my brief narrowed what I read, and I disregarded nothing under R0.
