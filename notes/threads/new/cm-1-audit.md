# Comecon, batches a, b and c: the audit

## What I read

I read the brief for this audit, the readers' briefs (`notes/briefs/threads-new-cm-a.md`, `-b.md`, `-c.md`), rulings 58 to 62 in `notes/owner-rulings.md`, the thread's statement in `lists/cal/th.yaml`, and the three readers' notes (`cm-a.md`, `cm-b.md`, `cm-c.md`).

I read each entry from `lists/cal/*.yaml`, its whole line and its whole note. I left out only the addresses of links.

The rule I audited against is the readers' brief, rules 1 and 2, as ruling 62 settles it. Default 6 of ruling 62 says the thread holds an entry wherever a government, party or church of the eight, or one of its officials or delegations, is the actor or the other party. Protocol counts: a delegation received, an envoy's call, cables between leaders, a banquet. Whoever the other side is does not matter. A member named in passing, one of many delegations or senders, or only the place does not count. The session sent me this default while I worked, and I mended the three batches to it.

Batch a (1960, Jan. 6 to Nov. 29):

- all 10 rows with Comecon as the primary thread;
- all 160 rows the reader left out, which covers the 40 my sample would have taken;
- 50 of the 137 secondary rows, drawn by a seed of my own (4417);
- the close calls the reader named;
- seven more secondary rows of one kind (sessions with member speakers), to see whether a fault repeated.

Batch b (Nov. 30, 1960, to May 9, 1962):

- no primary rows, since the reader gave none;
- all 140 rows the reader left out (a sample of 40, then the other 100, because the sample showed faults that repeat);
- 50 of the 167 secondary rows, by the same seed;
- the close calls the reader named;
- the secondary rows that hold writers, painters, teams or exhibitions.

Batch c (May 9, 1962, to Jan. 15, 1964):

- the one primary row;
- a sample of 40 of the 117 rows left out, then the other 77, for the same reason as in b;
- 50 of the 189 secondary rows by the seed;
- the lines of the other 139 secondary rows, read through for any row out of kind;
- the close calls the reader named.

I settled the two entries that `jd.tsv` (Jewish diaspora) also places.

I then searched the whole calendar from 1960 to Jan. 15, 1964, for entries in no Comecon list. I used 137 words of my own: the names of the members' leaders, envoys, towns, papers and bodies, in Latin letters and in Chinese, in the line and then in the note. I read each entry this turned up: 31 from the line, and 48 more from the note.

## The checks by script

Each of `cm-a.tsv`, `cm-b.tsv` and `cm-c.tsv` has one row for every id of its list, and no id twice. Every slug is in `th.yaml`. No row puts the primary thread in `also`, and no row has a space in `also`.

Two rows of c set a thread beside its parent or child, from the entry's own present threads: `cal.1962-06-23.china-2` (China with China: Leadership) and `cal.1962-06.vietnam-hanoi-3` (Vietnam: Hanoi with Vietnam). I took the child or parent out of `also`. After the mends the script finds no fault in any of the three files.

The rows I added in step 4 are in the tsvs but not in the `-ids.tsv` lists, which I did not change. The apply should take its rows from the tsvs.

## The counts

| Batch | Rows | Primary | Secondary | Out | Rows mended | Rows found |
|---|---|---|---|---|---|---|
| a, before | 307 | 10 | 137 | 160 | | |
| a, after | 319 | 8 | 160 | 151 | 15 | 12 |
| b, before | 307 | 0 | 167 | 140 | | |
| b, after | 312 | 0 | 186 | 126 | 22 | 5 |
| c, before | 307 | 1 | 189 | 117 | | |
| c, after | 317 | 1 | 202 | 114 | 7 | 10 |

Every changed or added row has a `basis` beginning `AUDIT:`, and every added row begins `AUDIT: found`.

Before the audit the three readers had the thread on 147, 167 and 190 rows of 307. After it the thread holds 168 of 319, 186 of 312 and 203 of 317.

## The mends

### Batch a

The reader of a left protocol out. I found five rows of that kind among the 160 left out and put each in as a secondary thread:

- the Peking rally for Hungary's liberation day;
- the greetings, telegram and toast for the Romanian party's congress;
- the North Vietnamese banquet for the Albanian delegation;
- the Center's briefing of Lleshi of Albania;
- Liu and Khrushchev's talk with Albania as a chief matter.

Five more rows left out had a member as the actor or the other party, and I put them in:

- the Bulgarian Ambassador's proposal at Conakry;
- Mobutu's order putting the Czechoslovak embassy out;
- the Chinese answer to the Hungarian delegation at Moscow;
- the appeal to the UN against the East German death sentence on Smolka;
- Mao's note on a collection of Tito's and the Yugoslav press's statements. I put this one in to match batch c, which puts Mao's notes on the Yugoslav party's plenum in.

I took one row out: Borilă as one of seven speakers at a session in Moscow (Oct. 7, 1960). The reader had put out the like row of Oct. 4, Nemes as one of five speakers.

Four rows changed their primary thread or their `also`:

- `cal.1960-01-06.soviet-union-6`, the arrests of Jews in Romania, now has Jewish diaspora as its primary thread and Comecon in `also`, as `jd.tsv` has it. The chief business is the acts against Jews, which is that thread's statement. The Romanian government did the acts, so Comecon is the secondary thread.
- `cal.1960-01-06.soviet-union-2`, Vukmanović-Tempo's flight to Moscow, keeps Comecon as its primary thread. It now has the Soviet Union in `also`, since Moscow is the other party.
- `cal.1960-07-03.europe-and-the-alliance-2`, Karamanlis's visit to Yugoslavia, goes back to Europe and the alliance as its primary thread, with Comecon secondary. That thread's statement names Greece, so it is not a holding place.
- `cal.1960-07-02.europe-and-the-alliance-federal-republic`, the arrest of Hahn, stays out of Comecon. It takes Jewish diaspora in `also`, as `jd.tsv` has it.

### Batch b

The reader of b left out a member's dealings with Moscow wherever a third party's act was what the entry recorded, though the reader's own note counts some 70 rows of the Soviet–Albanian quarrel as in. I put in six rows where the quarrel with Albania is a chief matter of the line:

- the CPSU letter of Feb. 22, 1962;
- the Politburo's reading of that letter;
- Deng's passage on Soviet–Albanian relations;
- the Chinese reply of Apr. 7, 1962, in its two entries;
- Khrushchev's attack on Albania of Nov. 30, 1960, and Liu's answer.

I put in three North Vietnamese rows on Albania: Hồ's journey to ease the quarrel, Hanoi keeping its ties with Tirana, and the letter to the CPSU on the quarrel.

I put in eight rows where a member is the actor or the other party:

- the Polish Ambassador's report to Firyubin on the Belgian feelers;
- Spaak's approach through the Polish Embassy;
- the North Vietnamese economic delegation's tour of six members;
- Phạm Văn Đồng's delegation in Prague, and in Warsaw and Sofia;
- the Czechoslovak and Polish consuls received at Guangzhou;
- Malile's first call as Albania's Ambassador;
- the Hungarian Foreign Minister's cable, one of two senders.

I put in Zhou's report on the talks with the East German trade delegation, one of the two matters of that meeting.

I took four rows out. Three are an Albanian painter's exhibition, the same painter received, and an Albanian writer received. None of them names a government, party or church, and the reader of a put sports teams out on that ground. The fourth is the meeting of Aug. 4, 1961, on the Warsaw Treaty meeting. No member acts or is dealt with in that line, and the entries on China's observers at the Warsaw Treaty meetings are out in a and b alike.

### Batch c

I put in four rows:

- the dinner for the correspondents sent home at Czechoslovakia's demand, to match July 19 and 27;
- Deng giving the reply to the Albanian Ambassador, one of three envoys;
- the Presidium sending Brezhnev's delegation to Czechoslovakia;
- Zhou's evening with Shehu at Tirana, part of the Albanian visit, which the reader put in everywhere else.

I took out the Albanian volleyball team, on the same ground as the teams in a. I also took the parent and the child out of the two rows the script found.

## Faults that repeat, and how I looked for every row of each kind

- Protocol left out, in a: I read all 160 rows left out in a. The rows mended above are every one of the kind.
- One of several speakers put in, in a: I read every secondary row in a whose basis names a session, a meeting or speakers. Only Oct. 7 was a speaker named among many. The others name members' delegates as the chief voices.
- A member's dealings with Moscow left out, and a member's officials left out, in b: I read all 140 rows left out in b. The rows mended above are every one of the kind.
- Cultural visitors with no official put in: I searched every secondary row of a, b and c for writers, painters, teams, troupes, students and exhibitions. The Polish industrial exhibition, a state one, and the friendship associations' delegations stay in.

## The entries found

I added 27 entries, each keeping its present thread with Comecon added to `also`.

In a (12 entries):

- Lleshi's visit to Peking, June 2–7, 1960: five entries;
- the wheat for Albania sent on Shehu's request;
- the SED's talk with da Cruz of the MPLA;
- five talks of the Chinese delegation with Hysni Kapo at Moscow, October and November 1960.

In b (5 entries):

- the talk with Kapo and Alia of Dec. 1, 1960;
- Zhou's loan to Albania through Koleka;
- the letter to the CPSU on the Vlorë base;
- two meetings of Chen Yi with Rapacki at Geneva.

In c (10 entries):

- Mao's arrangements to see the Kapo delegation;
- the two steps that led to the editorial of Dec. 15, 1962, against the Czechoslovak congress's charges (the editorial itself is in);
- Khrushchev at the SED's Sixth Congress;
- the Politburo's change of the greeting to that congress, and its revision;
- the question of sitting in on the CMEA's standing commission;
- three entries of Zhou's visit to Albania: the Shkodër and Vlorë banquets, and Chen Yi's journey to Vlorë.

Each of these lines names a member's leader, town or body, or a step that the reader's batch put in elsewhere, but none of the words that found the batch. The other entries the search turned up name a member in passing or in a list, and I left them out.

## Points for the session

- Some primary rows carry an old `also` that was itself filed for want of this thread. The Polish Army entries keep the Soviet Union in `also`, and the Polish students jailed for smuggling keep Europe and the alliance. The readers' briefs did not ask for these to be pruned, and I left them as they were.
- Batch c keeps the Presidium sessions in which a member is one item among several out, as its reader did. One of them, `cal.1963-06-10.soviet-union`, holds two member items: the meat lent to Poland and the delegation to Romania. It is the closest of that kind.
- `cal.1963-10-14.china-leadership-2` (援阿) stays in as Albania, and its "Check:" stays, as the reader of c advised.

## Under R0

Nothing I was given narrowed what is an entry. The readers' briefs and default 6 limit only where a thread is put, so they did not need to be set aside. I disregarded nothing.

## Fit to apply

Yes. The three tsvs pass every check by script. Each of their rows is either one a reader made and I read, or a row I read and mended or added. They agree with `jd.tsv` on both entries the two threads share.

The apply must take its rows from the tsvs, since 27 rows are not in the `-ids.tsv` lists. It changes `thread:` and `also:` alone.
