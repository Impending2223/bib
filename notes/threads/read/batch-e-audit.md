# Batch E: the audit

Nov. 26, 2026. An audit by reading of the reader's placings in `notes/threads/read/batch-e.tsv`, under `notes/briefs/china-threads-read-audit-e.md`. The rule I audited against is the reader's brief's rule 1 (`notes/briefs/china-threads-read-e.md`), with rulings 30, 58, 59 and 60 and the owner's words of Nov. 22 and Nov. 25, 2026. Nothing in `lists/`, `th.yaml` or `sources/` was changed. Nothing was merged, built, committed or pushed.

## What I read

I read each entry from `lists/cal/*.yaml` with a script of my own, the whole line and the whole note. I read every China thread's name, parent and statement in `lists/cal/th.yaml`.

I read these entries whole:

- The 14 entries the reader's note lists as undecided or weak.
- The 16 entries placed on a thread that takes fewer than five of the batch's entries as primary (Polemic, Mao Zedong, Third Front, Hai Rui, Political-legal work, Zhou Enlai, Bomb, Famine). One of them, the Famine entry, is also among the undecided, so this adds 15.
- The 14 entries kept in `china-leadership`.
- A random sample of 80 of the other 254 entries, drawn with Python's `random.sample` and the seed 5821.

That is 123 entries. While looking for faults that repeat, I read 19 more whole: the Miyun reservoir trip of Apr. 26, the New Year calls on Lin Biao, the Luo Ruiqing entries of August and October 1964 and January 1965, the forum on rural work of Nov. 16, the closing of the army's arts festival, and others like them. That makes 142 read whole.

For the other 155 entries I read the opening of the line (about 110 characters) and the reader's placing, to find entries of a kind I had found wrong. I did not read those 155 whole, and I do not count them as audited.

I read nothing in `build/`. Nothing in the brief narrowed what I read, and I disregarded nothing in it under R0.

## The checks by script

Over the whole tsv: every id of `batch-e-ids.tsv` has exactly one row, and no row is extra. Every slug is in `th.yaml`. No thread stands beside its own parent or child. No `also` holds the primary thread. No `also` has a space. The Center's daily work is in no row's `also`. The checks pass before and after the mends.

## The counts

- Read and judged: 123.
- Right as the reader placed them: 116.
- Mended: 7 of the 123, and 2 more found while looking for faults that repeat. 9 in all.
- By group: the 14 undecided, 11 right; the 15 others on small threads, all right; the 14 kept in `china-leadership`, all right; the sample of 80, 76 right. In the sample the primary thread is right in 77 of 80.

The mends, by kind of fault:

- A lesser figure's private day given a system as primary thread: 3. Deng Xiaoping's two evenings at traditional Lu operas on his journey to Jinan (`cal.1964-04-18.china-leadership-8`, `cal.1964-04-19.china-leadership-6`) were in Propaganda and culture. Yang Shangkun's outing to the Miyun reservoir at Kong Yuan's invitation, with lunch and a boat (`cal.1964-05-10.china-leadership-6`), was in Agriculture. The reader kept Yang's film, museum and store in `china-leadership`, so I did the same for these. Each keeps the old thread as a secondary thread.
- An episode given where the line has none of its words: 1. `cal.1965.china-leadership-11`, the five conditions for successors taught to Shanxi peasants, was in Four Cleanups with Agriculture second. The five conditions come from Mao's talk of June 16, 1964. Teaching them is propaganda work. It is now in Propaganda and culture alone.
- A system missing as a secondary thread: 1. The Secretariat sitting of Jan. 9, 1964 (`cal.1964-01-09.china-leadership-10`) heard a report on settling youths in the countryside. The batch places that business in Agriculture, so Agriculture is added.
- Another nation's thread missing: 2. The two entries on the establishment of China–France relations (`cal.1964-01-24.china-leadership-6`, `cal.1964-01-25.china-leadership-4`) now carry `europe-and-the-alliance-france`. The reader left it off because the France thread belongs to the American alliance's family. But the calendar already files China–France recognition there (`cal.1964-01-15.china`, `cal.1964-01-28.china-leadership-2`).
- A person's thread missing where Liu Shaoqi or Zhou Enlai acts: 2. At the forum on general rural work of Nov. 16, 1964 (`cal.1964-11-16.china-leadership-11`) Liu and Zhou hear the reports. At the closing of the army's arts festival (`cal.1964-05-10.china-leadership-10`) they attend the ceremony; the reader gave Mao's thread to Mao watching the exercise of June 15, so these get Liu's and Zhou's threads the same way.

Each mended row's `basis` begins `AUDIT:` and says what was there before.

## The reader's undecided entries, and my ruling on each

- `cal.1964-05-18.china-leadership-7` and `cal.1964-05-20.china-leadership-5`, the Culture and Education Committee's telephone calls to Yang on Li Bozhao's journey: Center's daily work, as the reader placed them. The line states no business, and ruling 58, point 5, gives a caller on the General Office's director to the Center's daily work. Nothing in the line makes the journey foreign business.
- `cal.1964-10-15.china-leadership-4`, Jiangsu's self-criticism after Liu's letter to Jiang Weiqing: Four Cleanups, with Liu second, as placed. The note's source, MacFarquhar III, 414, treats the letter as part of Liu's pressure on the provinces in the movement.
- `cal.1964-08-20.china-leadership-5`, two commune papers forwarded with Liu's comment: Agriculture, with Liu second, as placed. The reader's own rule for Mao (his comment forwarded, his thread primary) would give Liu the primary thread. Both threads hold the entry, so I leave it.
- `cal.1964-07.china-leadership-7` and `cal.1964-09-05.china-leadership-2`, Kang Sheng's work group and Peng Zhen on Peking University's cadres: Four Cleanups, with Propaganda and culture second, as placed. These are the socialist education movement's work team at the university, though the notes do not use the movement's name.
- `cal.1965.china-leadership-11`, the five conditions taught to Shanxi peasants: mended to Propaganda and culture, as above.
- `cal.1965.china-leadership-30`, the two Yibin cadres expelled for the starvation they caused: Famine, with Organization second, as placed. The Famine statement takes the deaths and the Center's measures.
- `cal.1964-02-29.china-leadership-10`, the Peking committee's report on city building and jobs: Finance and economy, as placed.
- `cal.1964-07-18.china-leadership-8`, Peng Zhen on the Peking paper and military study: Propaganda and culture, with Army second, as placed.
- `cal.1964-04-15.china-leadership-4`, senior cadres' study of Marxist works: Propaganda and culture, with Army and Polemic second, as placed. Polemic is a weak second thread, since the study is at home, but it does no harm.
- `cal.1964-04-03.china-leadership-3`, Yang Xianzhen's lecture on "two combine into one": Opera reform, as placed. The calendar already files the debate's other entries there (seven of them, from January to July 1964).
- `cal.1964-01-24.china-leadership-6` and `cal.1964-01-25.china-leadership-4`, China–France relations: Foreign affairs, with Propaganda and culture second, as placed, and France added, as above.

## Found, and left as placed

These are choices between two threads that both hold the entry. I did not mend them.

- The reader's rule for Mao (his comment or instruction forwarded or relayed, his thread primary) is not followed in `cal.1964-08-17.china-leadership-3`, where Luo Ruiqing conveys Mao's instructions on defense and Army is primary, or in `cal.1964-08-20.china-leadership-5` for Liu's comment.
- Zhu De's talk with the Fujian Military District's heads (`cal.1964-01-26.china-leadership-12`) is in Army, and his hearing of the Guizhou committee and military district (`cal.1964-03-17.china-leadership-5`) stays in `china-leadership`. Both are readings the rule allows.
- Qi Benyu's article on Li Xiucheng (`cal.1964-07-25.china-leadership-6`) is in Propaganda and culture, while the same year's criticism in philosophy is in Opera reform.
- The New Year calls of Yang Chengwu and Luo Ruiqing on Lin Biao (`cal.1964-02-14.china-leadership-7`, `cal.1964-02-15.china-leadership-10`) are in Army. They are the army's chiefs calling on its head, and the note's source treats them as a sign of how the chiefs stood with Lin.

## Is the batch fit to apply

Yes, as mended. Of 123 entries read whole, 116 were right as placed, and the 7 wrong ones are mended, with 2 more of the same kinds. Most faults were in the secondary threads. Only 4 primary threads were wrong: three private days now stand in `china-leadership`, and one entry now stands in Propaganda and culture. The checks by script pass. The 155 entries not read whole were scanned for the kinds of fault found, and the two found among them are mended.
