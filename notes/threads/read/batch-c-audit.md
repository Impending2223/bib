# Batch C: the audit of the reader's placings

Nov. 26, 2026. Audit on `notes/briefs/china-threads-read-audit-c.md` of the reader's placings in `notes/threads/read/batch-c.tsv` (297 entries, Aug. 18, 1961 to Oct. 29, 1962), judged by the rule of the reader's brief, `notes/briefs/china-threads-read-c.md`, its assignment 1, and ruling 59. Nothing in `lists/`, `th.yaml` or `sources/` was changed. Nothing was merged, built, committed or pushed.

## What I read

I read `CLAUDE.md`, the threads part of `notes/guide/brief.md`, rulings 30, 58, 59 and 60, the owner's words of Nov. 22 and Nov. 25 on the China threads, `notes/proposals/china-threads-revision.md`, `notes/threads/china-tree-audit.md`, the reader's brief, the reader's note and every China thread's statement in `th.yaml`. I read the entries straight from `lists/cal/*.yaml` with a script of my own, the whole line and the whole note of each, Chinese characters and the "Made public", "To check" and "Check" sentences included. I cut nothing short.

I read 171 entries whole:

- the 11 entries the reader's note names as undecided;
- the two groups the note names as resting on a rule the owner may want otherwise: the 49 entries of Peng Dehuai's village visit and Zhu De's inspections that went to Agriculture, and the 5 callers on Yang Shangkun that went to the Center's daily work (54 in all, two of them among the 11);
- the 20 entries on threads that take fewer than five of the batch as primary (Sixty Articles 4, Foreign affairs 4, Mao Zedong 3, United front 2, Polemic 2, and one each for Four Cleanups, Zhou Enlai, Hai Rui, Lei Feng, Dazhai, Daqing and India war);
- the 10 entries kept in `china-leadership`;
- 80 of the other 206, drawn at random with the seed 52817.

The first four groups overlap in four entries, so they come to 91; with the sample, 171.

Outside those, I read whole one more entry, `cal.1961-08-21.china-leadership-6`, when I checked the batch for the kind of a fault, and I read the lines (not the notes) of every row of three kinds where a fault might repeat: entries dated inside an episode's own days but placed elsewhere, entries with a person's thread, and entries on staffing and the cut of the organs. I read the lines of the threads' own entries for May 7 to 11, 1962, and the line of Zhou Enlai's report of Nov. 9, 1961, to place two entries beside them. I read nothing in `build/`.

## The checks by script

Over the whole tsv: every id of `batch-c-ids.tsv` has one row, and there are no others (297 and 297); every slug is in `th.yaml`; no thread stands beside its own parent or child; no `also` holds the primary; no `also` has a space or a slug twice; every row has a basis. All pass, before the mends and after them.

## The counts

Of the 171 read, 165 are right and 6 were wrong. With the one found outside the read set, I mended 7 rows. Six of the mends change the primary thread; one changes only the secondary threads.

By kind of fault:

- An episode's business placed in a system, 4. A meeting on grain on May 10, 1962, during the May work conference, was in Famine; the other grain meetings of that week are in Xilou and the retreat. Three entries on the staffing of the organs (Jan. 8 and Jan. 12, 1962, and July 4, 1962) were in Organization; the staffing is the streamlining, a station of the retreat, and the cut of Feb. 22 and the staff cuts of Mar. 22 are already there. I looked for every row of this kind in the batch; these three are all. Each now has the retreat first and Organization second.
- An entry kept in `china-leadership` that a system holds, 1. Peng Zhen at the Peking committee's plenum of Mar. 27, 1962 is the same meeting as Apr. 4, which the reader put in Organization; most of its points are cadres, Party branches and the review of the anti-rightist cases. It now has Organization first and Propaganda and culture second, for the intellectuals.
- A person's thread as a secondary thread where the person does not act, 1. On Nov. 6, 1961 Yang Shangkun arranges the meeting to hear Zhou Enlai's report; Zhou does not act in the entry, so "Zhou Enlai: Foreign affairs" is dropped. Polemic stays first. No other row of the batch has a person's thread where he does not act.
- A system chosen by a matter the line names, not by the act, 1 (outside the read set). The Peking committee's notice of Aug. 21, 1961 is a notice on socialist education: how the shortages are to be explained. It now has Propaganda and culture first and Famine second. No other row of the batch is of this kind.

Each mended row's basis begins with `AUDIT:` and the reason, then `reader:` and the reader's own basis.

A thread that plainly fits was missing in none of the 171, apart from the second threads the mends add. In a few entries another thread could be argued but is not plainly better: Zhu De's two talks on the army's history (June 26 and July 22, 1962) in Army, the foreign expert Manya Reiss's death in Foreign affairs, and Lei Feng's death in Lei Feng, Dazhai, Daqing without Army. I left them.

The primary threads of the 297 after the mends: Agriculture 85, Propaganda and culture 47, Army 41, Organization 37, Xilou and the retreat 24, Famine 9, `china-leadership` 9, Finance and economy 8, Seven Thousand Cadres 6, Beidaihe and the Tenth Plenum 6, Center's daily work 5, Sixty Articles 4, Foreign affairs 4, Mao Zedong 3, United front and nationalities 2, Polemic 2, and one each for Four Cleanups, Zhou Enlai, Hai Rui, Lei Feng, Dazhai, Daqing and India war.

## The reader's undecided entries, and my ruling on each

- `cal.1962-03-27.china-leadership-5` (Peking committee's plenum): mended, Organization first, Propaganda and culture second, as above.
- `cal.1962-04-04.china-leadership-8` (the same meeting): Organization, as the reader has it.
- `cal.1962-06-07.china-leadership-7`, `cal.1962-06-08.china-leadership-8`, `cal.1962-06-24.china-leadership` (the Xinhua dispatch on Chiang's raid): Army first, Propaganda and culture second, as the reader has them. The dispatch is the public side of the war preparations on the coast, which Army's statement names for June 1962; the press is only how it went out. Mao's telegram makes his thread a secondary one on June 24, rightly.
- `cal.1962-04-10.china-leadership-4` (Chen Yi's letter that his nephew go to the countryside): Xilou and the retreat, as the reader has it. The letter is private, but what it asks is the sending of town people to the villages, which the retreat's statement names.
- `cal.1962-05-20.china-leadership-4` and `cal.1962-05-26.china-leadership-5` (Zhu De's letters on Shaanxi and Xichang): Famine first, Finance and economy second, as the reader has them. Both report to the Center the people's hunger and their rations; Famine holds the famine whole; Agriculture cannot stand beside its own subthread. His letter of Mar. 3, which says most teams have grain enough, is rightly in Agriculture.
- `cal.1961-12-20.china-leadership-15` (Peng Dehuai's five village reports): Agriculture, as the reader has it. Hunger is in one report of five; the rest is output, crafts and markets.
- `cal.1961-11-03.china-leadership-2` (Peng begins his village visit): Agriculture, as the reader has it. Agriculture's statement names "Peng Dehuai at Wushi" as one of its stations.
- `cal.1961-11-13.china-leadership-6` (Zhu De's inscription for Deng Yanda): United front and nationalities, as the reader has it. Deng Yanda founded the forerunner of a democratic party, and the inscription honors him as such.
- The two groups. Peng Dehuai's village visit and Zhu De's inspections are rightly in Agriculture: its statement names the leaders' inspections of communes and farms and Peng at Wushi. The 5 callers on Yang Shangkun with no business stated are rightly in the Center's daily work, by ruling 58, question 5; callers whose business the line states (the Women's Federation's reports, the unions' work) are rightly in Organization.

## Is the batch fit to apply

Yes, as mended. Of the 171 entries read, 165 were right (96 percent), and the faults were of four kinds, each mended in every row of the batch where it occurs. The tsv passes every check by script. Nothing in the brief narrowed what I read or judged, and I disregarded nothing under R0.
