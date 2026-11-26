# China threads: the audit of batch D

Nov. 26, 2026. An audit by reading of the reader's placings in `notes/threads/read/batch-d.tsv` (297 entries, Oct. 29, 1962 to Jan. 1, 1964), under `notes/briefs/china-threads-read-audit-d.md`. I judged each entry by rule 1 of the reader's brief, `notes/briefs/china-threads-read-d.md`, and by rulings 58, 59 and 60. Nothing in `lists/`, `th.yaml` or `sources/` was changed. Nothing was merged, built, committed or pushed.

## What I read

I read the entries straight from `lists/cal/*.yaml` with a script of my own. For each entry in the counts below I read the whole line and the whole note, with the reader's row beside it.

- The 9 entries the reader's note names as leans or uncertain.
- The 15 entries on threads that take fewer than five of the batch's entries as primary: United front and nationalities (3), Foreign affairs (3), the Center's daily work (2), Hai Rui (2), and one each of Famine, Political-legal work, Lei Feng, Dazhai, Daqing, India war and Zhou Enlai. One of these, Henan's counts of April 1963 (the only entry on Political-legal work), is also one of the leans above, so the two groups hold 23 entries.
- The 16 entries the reader kept in `china-leadership`.
- A random sample of 80 of the other 258 entries, drawn with the seed 52817.

That is 119 entries read whole and counted.

To look for faults that repeat, I then searched the line of every one of the 297 entries for the words of each kind of fault I had found. I read the lines that came up to about 250 characters, and I read 10 of them whole, line and note. Those 10 are not in the counts, except one that I mended (the Xiao, Li and Liao case, below).

I read nothing in `build/`. I read every entry in the counts to its end.

## The checks by script

Over the whole tsv, before and after the mends: every id of `batch-d-ids.tsv` has exactly one row, and no row is extra. Every slug is in `th.yaml`. No row puts a thread beside its own parent or child. No `also` holds the primary thread. No row has the Center's daily work as a secondary thread, and no row that moves keeps `china-leadership` in `also`. All passed.

## The counts

Of the 119 entries read, 111 were right as the reader placed them, and 8 were wrong in some way. I mended all 8. I mended one more, outside the counts, which the search for a repeating fault found.

The mends by kind of fault:

- An episode's business placed in a system (4, three of them in the counts). The fall in Hunan's grain land, 1958 to 1962, read from Dikötter's book on the famine, goes to Famine, not Agriculture. The Organization Department's report on the effect of Mao's speech to the Seven Thousand Cadres Conference goes to Seven Thousand Cadres, with Organization second. Henan's counts of speculators, landlords and sects sent to the Center in April 1963 go to Four Cleanups, with Political-legal work and Agriculture second; the calendar has Henan's four clean-ups of the same month in that thread. The Chongqing committee's case against Xiao, Li and Liao, read from Yang Jisheng's book on the famine, goes to Famine, with Organization second, since the calendar already files the case's earlier entries (the Youth League cadres' report on Sichuan's dead) under Famine.
- A private social occasion placed in a system (1). The dinner *Hongqi* gave Yang Shangkun and Li Bozhao, with an evening at the opera, states no business. It goes back to `china-leadership`, as the reader's own rule for calls with no business says.
- A secondary thread missing (3). Organization for the death of Shen Junru, since its statement holds the deaths of leaders. Organization for the self-examination of the trade unions' paper with the Federation of Trade Unions. Lei Feng, Dazhai, Daqing for Lin Biao on the localities learning from the army.
- A person's plain thread where his subthread fits (1). Zhou Enlai's approval of the road built to supply Vietnam is his foreign business, so it takes "Zhou Enlai: Foreign affairs", not "Zhou Enlai".

Each mended row's basis begins with `AUDIT:`.

## The searches for faults that repeat

For each kind of fault I searched the whole batch and read what came up.

- An episode's business in a system: I searched for the famine books' cards and for the words of the famine, and for the words of the Four Cleanups (class struggle, speculation, the five-antis, socialist education, the Ten Points, graft). Besides the three in the counts, this found only the Xiao, Li and Liao case. The other entries of the Four Cleanups' run-up were already placed there.
- A private occasion in a system: I searched for dinners, banquets, receptions and parties, and for plays and shows. The others were institutional events (a ministry's banquet for doctors, the army's Spring Festival parties, the banquet for the athletes of the Games of the New Emerging Forces). They fit the thread they were given.
- A missing secondary thread: I searched for deaths and mourning, and for the campaigns of learning (Lei Feng, Dazhai, Daqing, the army). There were no other gaps.
- A person's plain thread in foreign business: Zhou's Vietnam road is the only row of the batch where Mao, Zhou or Liu carries foreign business.

## The reader's leans and uncertain entries, and my ruling on each

- `cal.1963-11-11.china-leadership-2`, Yang Xianzhen's lecture at the Central Party School: Opera reform stands. The calendar files the whole "two combine into one" affair of 1964 there, and this lecture is where it began.
- `cal.1964.china-leadership-9`, Jian Bozan under fire: Opera reform stands. The calendar files the attacks of 1964 on Sun Yefang and Feng Ding there too.
- `cal.1963.china-leadership-15`, Jiang Qing meets Zhang Chunqiao through Ke Qingshi: Opera reform stands. The note ties the meeting to their work on the arts.
- `cal.1964.china-leadership-37`, Hunan's land under grain: mended to Famine, as above.
- `cal.1963-06-14.china-leadership-10`, Chen Yi at the China Welfare Institute's anniversary party: Propaganda and culture stands. The party is the Institute's own event, and children's health and welfare is nearest that thread's statement.
- `cal.1962-12-22.china-leadership-7`, Zhu De at the Nanjing radar research institute: Propaganda and culture stands, since ruling 58 puts science there.
- `cal.1963-04-06.china-leadership-6`, Zhu De hears the Changshou county committee at the reservoir's guesthouse: Agriculture stands. The entries of the day before and the day after are his inspections of the reservoir and of a production team.
- `cal.1962-12.china-leadership-6`, the Organization Department's report on Mao's speech: mended to Seven Thousand Cadres, as above.
- `cal.1963-04.china-leadership-7`, Henan's counts: mended to Four Cleanups, as above.

## Notes for whoever applies the batch

- The statement of Opera reform says "the arts rectified", but the calendar files the attacks of 1964 on philosophers, historians and economists there too, and this batch follows the calendar. The statement may want those words.
- Several entries of a leader at a modern play (Chen Yi at *The Young Generation*, the New Year's gathering with *Chaoyanggou*) could sit in Opera reform or in Propaganda and culture. The reader chose Opera reform, as the plays are the campaign's own repertoire. I let them stand.

## Is the batch fit to apply

Yes, as mended. Of 119 entries read whole, 111 were right, and the faults I found were of four kinds, none common. I searched the whole batch for each kind and mended every row I found. The tsv passes every check by script.

Nothing in my brief narrowed what I read, and I disregarded nothing in it under R0.
