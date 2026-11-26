# China threads: batch B, the audit

Nov. 26, 2026. An audit by reading of `notes/threads/read/batch-b.tsv`, under `notes/briefs/china-threads-read-audit-b.md`. I judged each placing by rule 1 of the reader's brief (`notes/briefs/china-threads-read-b.md`), rulings 58 to 60, and the owner's words of Nov. 25. Nothing in `lists/`, `th.yaml` or `sources/` was changed. Nothing was merged, built, committed or pushed.

## What I read

I read the entries straight from `lists/cal/*.yaml` with a script of my own, the whole line and the whole note of each, Chinese characters and the "Made public", "To check" and "Check" sentences included. I read every thread statement of the China threads in `th.yaml`.

The entries read whole for the counts below, 147 in all:

- The reader's undecided entries: the six named singly, the 22 of Yang Shangkun's Hebei trip, and the 12 of Chen Yun's talks on grain that I took the last item to mean. That is 40.
- The entries on threads that take fewer than five of the batch as primary: Twelve Articles (2), Zhou Enlai (2), Mao Zedong (1), Liu Shaoqi (1), United front and nationalities (1), Split with Moscow (1). That is 8. The Center's daily work and Hai Rui take five each, so they were not in this group; I read all of them anyway, for the next point.
- The 23 entries kept in `china-leadership`.
- A random sample of 80 of the other 230, drawn with seed 58213.

Some of these fall in two groups, so the four groups make 67 entries before the sample, and 147 with it.

To follow faults that repeat, I then read whole every other row of the same kind: the 18 unread rows that carry the Center's daily work, the 11 unread rows where the reader dropped a thread that had been in `also:`, the five Hai Rui rows, and 14 more: rows found by searching the batch for the words of the rectification under the urgent letter and for Mao, Zhou or Liu inside an episode, two of Chen Yun's evenings with the storytellers, and two of the army's bulletins on foreign questions. That is 48 more read whole, 195 in all. I also looked at the opening of the line of the other 17 rows where Mao, Zhou or Liu is named inside an episode but has no thread; in each he receives a letter or a report, or is only named, and does not act, so I did not read them whole and mended none.

I read nothing in `build/`. Nothing in my brief narrowed what I read, and I disregarded nothing in it under R0.

## The checks by script

Over the whole tsv, before and after the mends: every id of `batch-b-ids.tsv` has one row, with none missing, none extra and none twice; every slug is in `th.yaml`; no thread stands beside its own parent or child; no `also` holds the primary; no `also` has a space or a thread twice. All pass.

## The counts

Of the 147 entries read for the counts, 140 are right and 7 were wrong. By group:

- The undecided: 39 of 40 right. The one wrong is `cal.1961-05-14.china-leadership`.
- The small threads: 7 of 8 right. The one wrong is `cal.1961-04-06.china-leadership-5`, for its secondary thread only.
- The entries kept in `china-leadership`: 22 of 23 right. The one wrong is `cal.1961-03-02.china-leadership-4`.
- The sample: 76 of 80 right. The four wrong are `cal.1961-05.china-leadership-9`, `cal.1961-03-27.china-leadership-11`, `cal.1961-08-10.china-leadership-3` and `cal.1961-08-01.china-leadership-5`.

Of the seven, two had the wrong primary thread and five a wrong or missing secondary thread.

Following the kinds of fault through the batch found eight more rows to mend, each read whole first. I mended 15 rows in all, each with a `basis` that begins `AUDIT:` and keeps the reader's words after it in brackets.

By kind of fault:

- A person's thread as the primary thread inside an episode: 1. `cal.1961-05-14.china-leadership` is a sitting on grain and on the village inquiry groups, both an episode's business. Ruling 59 puts the episode first. Famine is now primary, with Sixty Articles, Zhou Enlai, the Center's daily work and Laos as secondary threads.
- The business of the Twelve Articles placed in Agriculture or left in `china-leadership`: 4. These entries are about the communes' rectification under the Center's urgent letter, or its results, but they lack the thread's name: `cal.1961-03-01.china-leadership-14` (the Center forwards a commune's rectification), `cal.1961-03-02.china-leadership-4` (Deng hears Henan's rectification and repayment; the note gives it), `cal.1961-03-06.china-leadership-9` (Zhu De's report on where the urgent letter was carried out) and `cal.1961-04-30.china-leadership-8` (Zhu De on Sichuan since the Twelve Articles were relayed). All four now have Twelve Articles as primary. Two also take Finance and economy.
- The Center's daily work as a secondary thread on a sitting or meeting about one business: 7. Its statement covers the sittings on mixed business, the General Office and its callers, and the papers sent round. A sitting on one business belongs to the thread of that business. Five Secretariat sittings on the school regulations (`cal.1961-07-29.china-leadership-2`, `cal.1961-08-01.china-leadership-5`, `cal.1961-08-02.china-leadership`, `cal.1961-08-03.china-leadership-3`, `cal.1961-08-05.china-leadership`) and the Secretariat's report meeting on the Ninth Plenum (`cal.1961-04-06.china-leadership-5`) lose it. The sitting on the plan (`cal.1961-08-10.china-leadership-3`) loses it and takes Finance and economy.
- A secondary thread that plainly fits was missing or wrongly dropped: 3. `cal.1961-05.china-leadership-9` takes Liu Shaoqi, since Liu hears the report on his own *Selected Works*. `cal.1961-03-27.china-leadership-11` keeps Agriculture, already in its `also:`, since Sanmenxia is a water conservancy work and Agriculture's statement names water. `cal.1961-07-25.china-leadership` takes Finance and economy for Deng's report on the Northeast's mines and steel, and has Zhou Enlai: Foreign affairs in place of Zhou Enlai, since Zhou's part is the international situation.

After the mends, 22 entries stay in `china-leadership`. The rest have these primary threads: Propaganda and culture 65, Sixty Articles 60, Army 42, Agriculture 30, Finance and economy 23, Organization 18, Famine 16, Twelve Articles 6, Hai Rui 5, Center's daily work 5, and one each for Mao Zedong, Zhou Enlai, Liu Shaoqi, United front and nationalities, and Split with Moscow.

The reader's note says 117 entries were given secondary threads. The tsv as the reader left it has 88; after the mends it has 84. The note's count is wrong, not the rows.

## The reader's undecided entries, and my ruling on each

- `cal.1961-05-02.china-leadership-3` (Zhou on Laos; the inquiry teams called back for the drafting committee). The reader's placing stands: Sixty Articles primary, with Laos, Zhou Enlai: Foreign affairs and the Center's daily work. Zhou's part is foreign; the decision is the drafting committee's business.
- `cal.1961-05-14.china-leadership` (Zhou at the Secretariat on grain, the inquiry groups and Geneva). Mended, as above: Famine primary, since grain leads the line and is the first sitting's business; Sixty Articles for the ten inquiry groups heard; Zhou Enlai secondary.
- `cal.1961-07-20.china-leadership-3` (the Control Commission and the united front forum heard by Peng Zhen and Yang Shangkun). The reader's placing stands: Organization primary, United front and nationalities and the Center's daily work secondary.
- The reader asks whether these three entries should each be split in two. That is a question about the entries, not their threads, and is outside this audit. I record it for whoever next edits them.
- `cal.1961-01-09.china-leadership-7` (Yang Shangkun chief mourner for Li Kenong's wife). Stays in `china-leadership`. Organization's statement holds the deaths of leaders, and she was not one.
- `cal.1961.china-leadership-6` (Kang Sheng seeing plays in Yunnan and Sichuan) and `cal.1961-02.china-leadership-19` (Chen Yun at drum ballads while resting at Tianjin). Both stay in `china-leadership`, as a lesser figure's private days. The reader's line is consistent: where Chen Yun gives the troupes or the arts officials his views on the pieces, as on Apr. 22 and Apr. 25, the entry is Propaganda and culture; where he only sees a show and meets the players, it is a private day.
- Yang Shangkun's Hebei trip of April and May 1961, the 22 ids. All stand in Sixty Articles. The thread's statement is "the year of investigation", and two entries of the batch show the Center's village inquiry groups being brought back to give their material to the drafting committee for the commune regulations (May 2) and heard by the Secretariat, Hebei among them (May 14–17). The reader added Famine where a report gives deaths, sickness or rations, and Finance and economy at the county's machine and fertilizer works; both are right. If the owner reads Sixty Articles as the regulations alone, these 22 go back to Agriculture by rule, with no reading to redo.
- Chen Yun's talks on grain. The 12 entries stand. Talks on the price of grain go to Agriculture with Finance and economy, and talks on supply, rations, shipments and imports go to Famine. This follows the two statements: Famine names "the grain taken, moved and bought abroad".

## Other points for whoever applies the batch

- After the mends, 19 rows carry the Center's daily work as a secondary thread. Every one is a sitting on mixed business or a caller on Yang Shangkun as director of the General Office, and so fits its statement. The defaults written under ruling 59 say the Center's daily work is never a secondary thread, because the word lists placed it badly. Those defaults are the session's, not the owner's. These 19 were placed by reading, and I judged them by the reader's brief's rule 1, which allows them. If the script that applies the batch follows the default, it will strip them, and no entry loses its primary thread. Either way is safe.
- The five Hai Rui entries are the play's printing and staging and the debate on it in 1961. The thread's statement starts in 1965 with Yao Wenyuan's article. I let the placings stand, since the episode is about this play and its parent, Propaganda and culture, holds the entries either way. The statement may want a sentence for 1961.
- The reader dropped `farm`, `trade` and `defense` (United States threads) and `china` (the parent of every China thread) from `also:` wherever they stood. All of these drops are right.

## Is the batch fit to apply

Yes, as mended. Of the 147 entries read for the counts, 140 were right. The faults were of four kinds, and I followed each through the whole batch and mended every row of that kind. The structural checks all pass. No row is left undecided.
