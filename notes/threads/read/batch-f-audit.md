# China threads, batch f: the audit

Nov. 26, 2026. An audit by reading of `notes/threads/read/batch-f.tsv` and its note `batch-f.md`, under `notes/briefs/china-threads-read-audit-f.md`. The rule audited against is the assignment of the reader's brief, `notes/briefs/china-threads-read-f.md`, rule 1, with rulings 30, 58, 59 and 60 and the owner's words of Nov. 22 and Nov. 25, 2026.

## What I read

I read `CLAUDE.md`, the thread section of `notes/guide/brief.md`, rulings 30, 58, 59 and 60, the owner's words on the China threads of Nov. 22 and Nov. 25 (about 7:00 p.m.), `notes/proposals/china-threads-revision.md`, `notes/threads/china-tree-audit.md`, the reader's brief, the reader's note, and every China thread in `lists/cal/th.yaml` with its parent and its statement.

I read all 297 entries of the batch straight from `lists/cal/*.yaml` with a script of my own: the whole line and the whole note of each, Chinese characters and the "Made public", "To check" and "Check" sentences included. Nothing was cut short. For two entries I also read the entries next to them in the calendar, to see which thread holds them: `cal.1966-01.china-leadership-13` (the academic criticism, already in Hai Rui) and `cal.1966-02-06.china-leadership` (Mao on Peng Zhen's 1962 speech, in Mao Zedong).

The brief asked for four groups. All four are inside the 297 I read.

- The entries the reader's note names as doubtful, with the groups it names (the Peng Dehuai case, Yang Shangkun's stay in Shaanxi, the Tsinghua middle school, Yang Shangkun and the mass organizations): 71.
- The entries on a thread that takes fewer than five of the batch's entries as primary (Hai Rui, United front, Famine, Liu Shaoqi, Lei Feng, Dazhai, Daqing, Mao Zedong, Third Front, Red Guards, Political-legal work): 16.
- The entries kept in `china-leadership`: 25.
- A random sample of 80 of the other 196, drawn with the seed 61803.

The four groups come to 181 entries, since 11 entries fall in more than one group. The other 116 I read as well, so that a fault that repeats could be found in every row of its kind.

I read nothing in `build/`. Nothing in `lists/`, `th.yaml` or `sources/` was changed. Nothing was merged, built, committed or pushed.

## The checks by script

Over the whole tsv, before and after the mends:

- Every id of `batch-f-ids.tsv` has exactly one row, and there is no row for any other id: 297 of 297.
- Every slug in `primary` and `also` is in `th.yaml`.
- No row puts a thread beside its own parent or child, or beside any thread above or below it in the tree.
- No `also` holds the primary thread, repeats a thread, or has a space in it.

All four checks pass. The one fault the script found against ruling 59 is a row with the Center's daily work in `also` (`cal.1965-09-08.china-leadership-5`), mended below.

## The counts

Of the 181 entries in the four groups, 178 were right and 3 were wrong. Of all 297, 287 were right and 10 were wrong. An entry counts as right where its primary thread is the one rule 1 gives, or one of two that fit equally, and where no thread that plainly fits is missing and none that does not fit is present.

The 10 wrong rows are mended in `batch-f.tsv`. Each mended row's basis begins "AUDIT:" and keeps the reader's words after "Reader:". One more row had right threads but a basis that said the opposite of its placing; its basis is corrected and its threads are unchanged.

The faults, by kind:

- An episode's business placed on a system, 3. Luo Ruiqing's report on rear-area building in the first- and second-line provinces (`cal.1965-02-27.china-leadership-7`) is the Third Front's, with Army as a secondary thread. Yang Shangkun's meeting of the central organs' men who had squatted at points (`cal.1965-07-06.china-leadership-3`) is the Four Cleanups', not the Center's daily work. Xu Liqun taking over the academic criticism in January 1966 (`cal.1966-01.china-leadership-10`) is Hai Rui's; the next entry on the same work is already in Hai Rui.
- Mao or Liu Shaoqi acting inside an episode or a system, with his thread missing as a secondary thread, 3. Mao agrees to Peng Zhen's report on Peking University (`cal.1965-03-01.china-leadership-3`). The Secretariat sits under Liu on the arts (`cal.1965-03-02.china-leadership-5`). The Military Commission adopts Lin Biao's five principles on Mao's comment (`cal.1965-11-25.china-leadership-8`); the reader had given Mao to the like entry on the Public Security Force.
- A person's thread as primary where he does not act in the line, 1. The Center's instruction on half-farming, half-study schools (`cal.1965-07-14.china-leadership-6`) now has Propaganda and culture as primary and Liu's thread as secondary, as the reader did for the June 14 report on the arts graduates.
- The Center's daily work as a secondary thread, 1 (`cal.1965-09-08.china-leadership-5`). Ruling 59 says it is never one. It is dropped; Organization stays primary.
- A system or a nation's thread that plainly fits, missing, 2. The Soviet Union on the *Renmin ribao*'s satire on Khrushchev (`cal.1965-02-01.china-leadership-4`), as on the batch's other press entries on Moscow. Propaganda and culture on the radio's broadcast of "Long Live the Victory of People's War" (`cal.1965-09-02.china-leadership-7`).
- The basis corrected only, 1. Peng Zhen's report to the Youth Federation and the students' congress (`cal.1965-01-15.china-leadership-7`) is rightly in Organization, as a mass body of the kind ruling 58 (7) puts there, but the reader's basis said no thread fitted.

For each kind I searched the whole batch by script for rows of the same kind and read each one found. The search for Mao, Zhou Enlai and Liu Shaoqi in the line found 56 rows naming one of them without his thread; in the 53 besides the three above the man is only named, sent a paper, or the subject of a slogan, and does not act. The searches for the Four Cleanups' words, the Third Front's words, and the words of Hai Rui and Opera reform found no other row placed outside its episode. No other row has a person's thread as primary where he does not act, and no other row has the Center's daily work in `also`.

The primary counts after the mends: Army 65; Organization 55; Propaganda and culture 44; `china-leadership` 25; Agriculture 24; Four Cleanups 19; Luo Ruiqing 17; Center's daily work 10; Finance and economy 10; Opera reform 6; Foreign affairs 5; Hai Rui 4; United front and nationalities 3; Third Front 2; Famine 2; Lei Feng, Dazhai, Daqing 2; Mao Zedong 1; Liu Shaoqi 1; Red Guards 1; Political-legal work 1. Entries with at least one secondary thread: 65.

The reader's note's counts agree with the tsv as the reader left it.

## The reader's doubtful entries, and my ruling on each

- The Peng Dehuai and Xi Zhongxun case committee (`cal.1965-02-14.china-leadership-5`, `cal.1965-02-17.china-leadership-13`, `cal.1965-09-07.china-leadership-12`) and the Party School's talks and reports on Peng (`cal.1965-07-07.china-leadership-5`, `cal.1965-07-12.china-leadership-14`, `cal.1965-09-10.china-leadership-10`, `cal.1965-10-24.china-leadership-3`): kept in Organization. A Party body's work on a cadre's case is the Party's own bodies and cadres, as the statement says. The two visits of the Party School's men that are Peng's own talk (`cal.1965-11-24.china-leadership-11`, `cal.1965-11-28.china-leadership-8`) are rightly kept in `china-leadership`.
- Yang Shangkun's stay in Shaanxi, April to June 1965: kept as the reader placed it. The work corps' meetings and speeches are the Four Cleanups', since the stay is a station of that thread's statement. The farm visits are Agriculture's. The sightseeing, the travel days, the Baoji speech on the situation (`cal.1965-04-23.china-leadership-10`) and the Fengxiang trip (`cal.1965-04-24.china-leadership-4`) stay in `china-leadership`, since their lines name no thread's business.
- The *Wenhui bao* essay on ghost plays (`cal.1965-05-06.china-leadership-5`): kept in Propaganda and culture. Nothing in the line or the note ties it to Hai Rui. Opera reform could also hold it, since the ghost plays were that campaign's first target in 1963, but the line names only a press essay, so the system stands.
- Zhou Yang in hospital and Xu Liqun taking over the academic criticism (`cal.1966-01.china-leadership-10`): mended to Hai Rui, as above.
- Deng away and Peng Zhen in charge of the Secretariat (`cal.1965-11.china-leadership-7`): kept in the Center's daily work with Hai Rui as a secondary thread.
- Lin Biao's letter adding Yang Chengwu beside Luo (`cal.1965-04-23.china-leadership-15`): kept in Luo Ruiqing. The source reads it as aimed at Luo, and the episode comes before the system. Army cannot stand beside it, being its parent.
- Jiang Qing's army forum (`cal.1966-02-02.china-leadership`, `cal.1966-02.china-leadership-9`, `cal.1966-02-01.china-leadership-7`, `cal.1966-02-20.china-leadership-3`): kept in Propaganda and culture with Army, and Mao on the entry that records his revision of the summary. No stage thread covers February 1966, and the forum is the arts' business.
- The Tsinghua middle school (`cal.1965-02.china-leadership-3`, `cal.1965-05.china-leadership-10`, `cal.1965-10-28.china-leadership-7`): kept in Propaganda and culture, as education. The Red Guards thread begins with the Eleventh Plenum.
- Peng Zhen sending Mao his revised 1962 speech (`cal.1966-02-11.china-leadership-2`): kept in `china-leadership`. Peng acts, not Mao, and the act is of 1966, not of the 1962 conference.
- The two Army Day parties (`cal.1965-07-31.china-leadership-4`, `cal.1965-07-31.china-leadership-5`): kept in Army. Both are the army's own anniversary, and one is given by the General Political Department.
- Jiao Yulu (`cal.1966-02-07.china-leadership-5`, `cal.1966-02-09.china-leadership-6`): kept in Lei Feng, Dazhai, Daqing. The statement's head is "The emulation campaigns", and a notice to learn from a model is one.
- Yang Shangkun and the mass organizations (`cal.1965-08-09.china-leadership-3` and the like entries on the Youth League, the trade unions, the Women's Federation and the Control Commission): kept in Organization, as ruling 58 (7) and the statement say.

## Is the batch fit to apply

Yes, as mended. The structure is sound: one row an entry, real slugs only, no thread beside its parent or child, no primary thread in `also`, and now no Center's daily work in `also`. The placings are right in 178 of the 181 entries the brief named and in 287 of all 297 before the mends; the ten faults are of small kinds and each is mended. The faults the tree audit found in the word lists (a lesser figure's private day in Army or Propaganda and culture, a farm thread for factories and shows) are not repeated here: the reader put those in `china-leadership` or the fitting system.

## What I disregarded under R0

Nothing in my brief narrowed what I read. Its sample of 80 was a floor, not a limit, and I read the whole batch.
