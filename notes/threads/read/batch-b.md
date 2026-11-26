# China threads: batch B, read

Nov. 26, 2026. Reader's note on `notes/threads/read/batch-b.tsv`. Nothing in `lists/`, `th.yaml` or `sources/` was changed.

## What I read

All 297 entries of `batch-b-ids.tsv`, each in full: the whole line and the whole note, Chinese characters, "Made public", "To check" and "Check" sentences included. I cut nothing. Where a tool printed a file in parts, I read every part. I read each against the thread statements in `lists/cal/th.yaml` and rulings 58 to 60. The entries are all of 1961 (Jan. to Aug., and some dated by the year or the season). Nothing in the brief narrowed what I read, and I disregarded nothing in it under R0.

The `th.yaml` of this branch already holds the new tree (Famine, Twelve Articles and Sixty Articles under Agriculture; Mao's and Zhou's subthreads; the nuclear threads). I used only slugs it has. The Nuclear and Cultural Revolution threads fit none of these entries. There is no thread for a Cultural Revolution parent beyond `india-and-china-cultural-revolution`, and none was needed.

## The counts

Entries kept in `china-leadership`: 23.

Entries moved, by primary thread:

- Propaganda and culture (`china-propaganda`): 65
- Sixty Articles (`china-sixty-articles`): 60
- Army (`china-army`): 42
- Agriculture (`china-agriculture`): 33
- Finance and economy (`china-economy`): 23
- Organization (`china-organization`): 18
- Famine (`china-famine`): 15
- Hai Rui (`china-hai-rui`): 5
- Center's daily work (`china-center`): 5
- Twelve Articles (`china-twelve-articles`): 2
- Zhou Enlai (`china-zhou`): 2
- Mao Zedong (`china-mao`): 1
- Liu Shaoqi (`china-liu`): 1
- United front and nationalities (`china-united-front`): 1
- Split with Moscow (`china-moscow`): 1

That is 23 kept and 274 moved, 297 in all. Secondary threads were given to 117 entries; the most used are the Center's daily work (25), Agriculture (15), Finance and economy (12), Famine (10) and Mao Zedong (8).

## Where the word lists were wrong

The lists had proposed Propaganda and culture for 82 entries, Army for 50, Agriculture for 138 and Organization for 27.

- Propaganda and culture, wrong for 19 of 82: 8 are lesser figures' private days or outings (a visit to a museum or a park, a May Day garden party, a night at the opera); 5 are the staging, printing and debate of Wu Han's play, which belong to Hai Rui; 2 are army matters (the army paper, Lin Biao's order); 1 each is Mao revising a preface, Zhou's talk to the table tennis players, a fertilizer-style economy paper, and a Sixty Articles inquiry (Lu Dingyi's visit to a county).
- Army, wrong for 11 of 50: 7 are private days or tours of lesser figures (Zhu De on a boat, a call on a sick marshal, Ye Jianying's tour of a town, Yang Shangkun on a coast terrace); 1 each are a Ninth Plenum relay, a call on a former Nationalist minister (united front), a draft letter on the Soviet–Albanian quarrel (Split with Moscow), and a Secretariat sitting on the recordings.
- Agriculture, wrong for 105 of 138: 58 belong to the Sixty Articles (the year of investigation: the drafting at Canton, the survey groups, the mess-hall letters to Mao, Chen Yun's Qingpu inquiry, and Yang Shangkun's village investigation in Hebei); 15 to Famine (grain supply, imports, rations, deaths and sickness reported); 22 to Finance and economy (plant, power and machinery inspections, fertilizer works, grain trade, cutting staff); 6 are private days or journeys with a remark about drought; and one each to the Center's daily work, Liu Shaoqi, Zhou Enlai, and Twelve Articles (the figures count the 138 as the lists' proposals, 33 of which stand). Agriculture is the parent of Famine, Twelve Articles and Sixty Articles, so an entry that fits one of them does not also carry Agriculture.
- Organization, held for 27: 18 are rightly Organization (the Youth League, trade unions, Women's Federation, Control Commission, rehabilitations, cadre rules, appointments); 3 are the Center's daily work (the recordings affair and a General Office day); 2 stay in `china-leadership` (a wife's memorial, a private matter); 2 are Propaganda and culture; 1 is the Army; 1 is Sixty Articles. Where the Organization entry was a General Office caller on a body, I added the Center's daily work as a secondary thread.

The Center's daily work is a secondary thread only where the line is a General Office caller on a body of the Party's work or a Secretariat sitting, not wherever the Center is named.

## Rules I applied beyond the brief

- `china` was dropped from every `also:` because it is the parent of every thread. `farm`, `trade` and `defense` were dropped because they are the United States' threads and nothing here is American business.
- A thread was never put beside its own parent or child. The script that wrote the file checked every pair.
- I put Yang Shangkun's, Deng's and Chen Yun's village investigations of April to July 1961 under Sixty Articles, because the Center sent them to bring material to the drafting committee for the commune regulations (the note of the entry of May 2 says so). Zhu De's own tours of communes, plants and farms, and Yang's earlier travels in Feb.–Mar. 1961, I left in Agriculture or Finance and economy.

## What I could not decide

- Two businesses in one entry, the primary a judgement: `cal.1961-05-02.china-leadership-3` (Zhou on Laos and the decision on the inquiry teams; I took Sixty Articles first), `cal.1961-05-14.china-leadership` (Zhou on grain, the investigation and Geneva; I took Zhou first), and `cal.1961-07-20.china-leadership-3` (the Control Commission and the united front forum; I took Organization first). These look like events that the entry should perhaps be split.
- Private days that might be Organization (the death rule) or Propaganda and culture: `cal.1961-01-09.china-leadership-7` (a memorial for a Party figure's wife; left in `china-leadership`), `cal.1961.china-leadership-6` and `cal.1961-02.china-leadership-19` (a lesser figure's play-going; left).
- Whether Yang Shangkun's Hebei trip of April to May belongs under Sixty Articles or Agriculture. The 22 ids are `cal.1961-04-16.china-leadership-5` and `-6`, `cal.1961-04-17.china-leadership-5`, `cal.1961-04-18.china-leadership-11`, `cal.1961-04-19.china-leadership-8` and `-9`, `cal.1961-04-20.china-leadership-6` and `-7`, `cal.1961-04-21.china-leadership-6`, `-7`, `-8` and `-9`, `cal.1961-04-22.china-leadership-4` and `-5`, `cal.1961-04-24.china-leadership-7` and `-8`, `cal.1961-04-26.china-leadership-5`, `cal.1961-05-05.china-leadership-6`, `cal.1961-05-09.china-leadership-11`, `cal.1961-05-10.china-leadership-8` and `cal.1961-05-11.china-leadership-4`, and `cal.1961-05-13.china-leadership-4`. If the owner reads Sixty Articles as the regulations only, these 22 go back to Agriculture (or Famine) by rule.
- Chen Yun's talks on grain: those on the price of grain (Jan. 1961) went to Agriculture with Finance and economy; those on supply, imports and rations went to Famine. The line between them is mine.
