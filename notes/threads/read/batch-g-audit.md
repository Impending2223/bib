# China threads, batch G: the audit

Nov. 26, 2026. An Opus audit of the reader's placings in `notes/threads/read/batch-g.tsv`, under `notes/briefs/china-threads-read-audit-g.md`. The rule audited against is the reader's brief, `notes/briefs/china-threads-read-g.md`, assignment 1 (ruling 59). I mended 22 rows of `batch-g.tsv`; each mended row's basis begins `AUDIT:`. Nothing in `lists/`, `th.yaml` or `sources/` was changed. Nothing was merged, built, committed or pushed.

## What I read

I read the entries straight from `lists/cal/*.yaml` with a script of my own. For each I read the whole line and the whole note, with its "Made public", "To check" and "Check" sentences. I read nothing in `build/`. The threads and their statements are from `lists/cal/th.yaml`. I also read CLAUDE.md, `notes/guide/brief.md`, rulings 30, 58, 59 and 60, the owner's words of Nov. 22 and Nov. 25, the proposal `china-threads-revision.md`, the tree audit `china-tree-audit.md`, and the reader's brief and note.

The entries read:

- Every entry the reader's note names as hard to decide: 36.
- Every entry placed on a thread that has fewer than five of the batch's entries as its primary thread: 21 (Lei Feng, Dazhai, Daqing; Zhou Enlai: Cultural Revolution; Mao Zedong; United front; Foreign affairs; Mao Zedong: Cultural Revolution; Liu Shaoqi; Third Front; Luo Ruiqing; Zhou Enlai; Political-legal work).
- Every entry kept in `china-leadership`: 35.
- These three groups overlap; together they are 80 entries.
- A random sample of 80 of the other 214, drawn with the seed 58117.
- Then, to find every row of the kinds of fault that repeated, 59 more: every row placed on a system thread whose date falls in the months of a Cultural Revolution stage and which I had not yet read, and the rows dated after April 1969 that I had not yet read.

That is 219 of the 294 entries, each read whole. To judge like entries alike I also looked up, in the calendar, the threads of entries outside the batch on the same matters (the army forum's summary, the dispersal of October 1969, the editorials of January 1967, the schools' military training, Zhou Enlai's monthly counts of his talks). I read those outside entries only as far as I needed to see what they were about.

## The check by script

Over the whole tsv, before and after the mends:

- Every id of `batch-g-ids.tsv` has one row, and there is no other row: 294.
- Every slug is in `th.yaml`.
- No row has a thread beside its own parent or child.
- No `also` holds the primary thread, and no `also` has a space or a repeated slug.

All four hold.

## The counts

Of the 219 entries read, 197 were right as the reader placed them and 22 are mended. The primary thread was right in 209 of the 219; 10 primary threads are changed. The other 12 mends change only the secondary threads.

By group:

- The 80 named in the brief: 67 right, 13 mended (7 primary threads changed, 6 secondary only).
- The random sample of 80: 75 right, 5 mended (1 primary thread changed, 4 secondary only). The primary thread was right in 79 of 80.
- The 59 read for the repeating faults: 55 right, 4 mended (2 primary threads changed, 2 secondary only).

By kind of fault:

- A Cultural Revolution stage's business, in the stage's months, placed elsewhere: 7. Three had a person's subthread as the primary thread: Mao's note on the schools' military training of Feb. 19, 1967, and Zhou's counts of his talks for May and for August 1967. The owner's words of Nov. 25 put the person's thread second inside an episode. Two had a system or another episode: the army's help to spring production of Feb. 23, 1967 (Army), and the Dukou garrison's report on supporting the left, forwarded Mar. 8, 1967 (Third Front). One was the press: the *Renmin ribao* editorial on thrift of Jan. 26, 1967 (Propaganda and culture), where every other editorial of that January is in Seizures of power. One was the all-army conference on creative work of Apr. 8, 1966 (Army), which carries out the army forum's summary, whose April steps the reader put in May Sixteenth.
- The dispersal of October 1969 carried out, left in `china-leadership`: 3 (see the ruling below).
- A thread that plainly fits left out: 8. The Cultural Revolution parent on five entries of 1969 about the provinces' factions and the arms seized in their fighting; Organization on Deng's talk in Qinghai on training minority cadres; Propaganda and culture on the summary's second draft comment of Apr. 4, 1966; United front on Soong Ching Ling's article of Nov. 13, 1966; Vietnam: Hanoi on Vietnamese students taken into the army's schools.
- A country thread dropped from `also:`: 2. Ruling 58 keeps any country an entry already has there, and ruling 59 does not change that point. Both entries are war measures against the Soviet Union (Aug. 27 and late September 1969), and the Soviet Union is restored to both.
- A secondary thread that does not fit: 2. Army on the Guizhou study class, where the army's academy is only the place. Army on Zhu De's private note on Vietnam, kept in `china-leadership`: a China thread that fits would have to be its primary thread, and the army is not the note's business.

The 22 mends in all: 10 change the primary thread, 12 change the secondary threads only.

## The reader's hard cases, and my ruling on each

- The army forum's summary, March and April 1966 (10 entries). The reader's placings stand: Hai Rui for the March steps and May Sixteenth for the April ones. The calendar already has Mao's reading of the summary of Mar. 17 in Hai Rui and Peng Zhen's draft comment of Apr. 1 in May Sixteenth, so the batch agrees with them. I added Propaganda and culture to the draft comment of Apr. 4, as the reader had it on Apr. 10. By the same reading I moved the all-army conference on creative work of Apr. 8 to May Sixteenth.
- The Shandong food shortage of spring 1966. Agriculture stands. The Famine thread holds the famine of 1959–62, and its last entry is of December 1963. Famine is under Agriculture, so it cannot stand beside it.
- Lin Biao's delay of Luo Ruiqing's surgery in 1968. Luo Ruiqing stands. It is Lin Biao's case against Luo carried on.
- The cleansing of class ranks after September 1968 (4 entries). Revolutionary committees stands. The thread's statement names the cleansing, and these are its business; its dates follow its entries.
- The leaders sent out of Peking in October and November 1969 (2 and 9 entries). The two notices stand in Border war: the dispersal was ordered for war readiness, and the war scare is in that thread's statement. Three of the nine lines with no reason given are the dispersal itself carried out: Chen Yun's departure and Zhu De's landing at Canton on Oct. 20, and Deng's flight to Nanchang on Oct. 22. They go to Border war. The other six record life at the place of exile (Deng's letter of Oct. 21, the house chosen Oct. 24, Chen Yun's move of Nov. 3, Deng's labour from Nov. 9, Chen Yun at the works from Nov. 12, Deng and his supervisor on Nov. 23). They stay in `china-leadership`.
- The study classes of 1969 (5 entries). Organization stands as the primary thread. The classes of Wuhan's, Guizhou's and Sichuan's factions now carry the Cultural Revolution parent as well. Army is dropped from the Guizhou class.
- Peng Dehuai in custody. The reader's line stands: where the case group acts, Organization; where only his behaviour is logged, `china-leadership`.
- Jiang Qing against Chen Boda, March 1969. The Ninth Congress stands: the quarrel is over Mao's comment on Deng and Liu, which the congress's report was to carry.
- Ye Jianying's standing meetings of the Military Commission. Army stands. I read all such rows in the stages' months; each is mixed army business, and none moved.

## Found outside the batch, not mended

These entries are not in the batch, so I changed nothing. They bear on the batch's mends.

- `cal.1969-10-17.china-leadership`, the decision that the old leaders leave Peking for war readiness, is in Zhou Enlai: Foreign affairs. By the rulings above it belongs in Border war.
- `cal.1967-02-14.china-leadership-4` and `cal.1967-03-07.china-leadership-2`, Mao's notes on the schools' military training, are in plain Mao Zedong. I put the batch's like entry of Feb. 19, 1967 in Seizures of power, as the army sent in. One way or the other should hold for all three.
- `cal.1967-03.china-leadership-3`, Zhou's count of his talks for March 1967, is in `china-leadership`. The counts for January and February are in Seizures of power, and the batch's May and August counts now go to Wuhan and the army.

## The reader's counts

The counts in `batch-g.md` are the reader's, before this audit. As mended, the primary threads are: Army 51, Organization 40, Propaganda and culture 38, `china-leadership` 32, May Sixteenth 19, Border war 17, Red Guards 15, Seizures of power 14, Hai Rui 12, Finance and economy 10, Wuhan and the army 9, Agriculture 8, Ninth Congress 6, Revolutionary committees 6, Lei Feng, Dazhai, Daqing 3, Mao Zedong 3, United front 2, Foreign affairs 2, Liu Shaoqi 2, and one each for Zhou Enlai: Cultural Revolution, Luo Ruiqing, Zhou Enlai, Mao Zedong: Cultural Revolution and Political-legal work.

## Is the batch fit to apply

Yes, as mended. In the random sample the primary thread was right in 79 of 80, and every placing in 75 of 80. The faults were of a few kinds. I swept the batch for each kind and mended every row of it I found. The rows I did not read (75 of 294) are of kinds whose read rows were nearly all right. No row breaks the rules the script checks.

Nothing in my brief narrowed what I read, and I disregarded nothing in it under R0.
