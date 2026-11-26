# Comecon, batches d, e and f: the audit (Nov. 26, 2026)

## What I read

I read the brief, `CLAUDE.md`, the threads part of `notes/guide/brief.md`, rulings 58 to 62, the thread `cal.thread.comecon`, the three readers' briefs (`threads-new-cm-d.md`, `-e.md`, `-f.md`) and their notes and tables.

I read each entry whole, the line and the note, from `lists/cal/*.yaml`. My sample was drawn with Python's `random.sample` over the sorted ids, seed 4711: 50 secondary rows and 40 rows left out in each batch.

- Batch d (1964-01-25 to 1965-07-22): the 28 entries the reader called close; the 50 secondary rows of the sample; and all 221 rows left out, because the sample showed a fault that repeats (below).
- Batch e (1965-07-23 to 1967-04-13): the 5 primary rows; the 13 close calls; the 50 secondary rows of the sample; all 45 rows left out; and 10 more rows in the thread, found by their basis words as possible repeats of a fault.
- Batch f (1967-04-16 to January 1970): the 17 close calls; the 50 secondary rows of the sample; the 40 rows left out of the sample; and about 35 more rows, in and out, found by their basis words as possible repeats of a fault.
- The search for missed entries: about 105 entries the search turned up, every one read in its line and most in full.

In all I read about 700 entries.

## The rule I held the three batches to

Ruling 62, default 6: an entry is in where a government, party or church of one of the eight, or one of its officials or delegations, is the actor or the other party, protocol included. It is out where a member is named in passing, is one of many, or is only the place. To use one rule in all three batches I settled these cases. Each is the reading the ruling best supports, and each is a default the owner can overrule.

1. Protocol is in: cables, condolences, receptions given by a member's embassy, courtesy calls of a member's ambassador, banquets, wreaths. Batch d's reader left these out as "protocol" or "minor". The reader's brief, R0, names "minor" as a word that may not narrow, and ruling 62 puts protocol in.
2. Every step of a visit is in when it takes place on a member's soil or with a member's delegation present. That covers arrivals, tours, plays, rallies and departures.
3. A Chinese or Vietnamese act done at home with no member present is out. That covers a meeting on the line to take, reading the record of talks, hearing an ambassador's report, choosing delegates, and seeing off or welcoming home one's own delegation.
4. A text addressed to a member is in, and so is its approval: a telegram, a reply to a letter, a greeting to a congress, an agreement.
5. Any delegation, troupe or team a member sends is in when a leader receives it. That includes women's, youth and press delegations, army ensembles and sports teams. The ruling says "delegations" and draws no line by kind.
6. "One of many" means a crowd or a long list: a National Day reception, fifteen foreign ministers' cables, a tournament of eight countries. A meeting with two or three named delegations is in.
7. A member's diplomat who reports on others' business is a witness, not an actor, and the entry is out. This covers the Hungarian reports from Pyongyang and Cairo.
8. One government's act toward another, whose whole subject is a member's dealings with Moscow, is in. This covers the Western statements on the Soviet–East German treaty and the American démarches on Czechoslovakia and Romania. American and Chinese meetings, assessments and press articles about those dealings are out.

## Counts

| Batch | Rows | Reader: primary / secondary / out | After the audit: primary / secondary / out | Rows mended | Rows found |
|---|---|---|---|---|---|
| d | 307 + 6 | 0 / 86 / 221 | 4 / 204 / 105 | 118 | 6 |
| e | 307 + 27 | 5 / 257 / 45 | 7 / 278 / 49 | 8 | 27 |
| f | 305 + 8 | 0 / 194 / 111 | 0 / 217 / 96 | 24 | 8 |

After the audit the thread holds 669 of the 919 entries listed, plus the 41 found. The readers had put it on 86, 262 and 194 of their lists. It now stands on 202 of 307, 258 of 307 and 209 of 305.

## The mends

Every mended row's `basis` begins `AUDIT:` and says what the row was before.

Batch d, 118 rows:

- 113 rows put in. Each is protocol, a delegation of a member received, a step of a visit, or a single country's delegation that the reader had called "one of many". All the cables, condolences, receptions, ambassadors' calls, airport meetings of members' delegations and anniversary delegations of 1964 and 1965 are among them.
- 3 rows put in because they hold a text addressed to a member or agreed with one: `cal.1965-03-24.china-leadership-10`, `cal.1965-07-10.china-leadership-7` and `cal.1965-04-16.china-leadership-6`.
- 2 rows made Comecon their primary thread: `cal.1965.europe-and-the-alliance` (Romanian delegations to Burma, Pakistan and the UAR) and `cal.1965.europe-and-the-alliance-britain` (a Romanian delegation in England). Both come from the Romanian record of May 1966, and batch e's reader placed the like entries from that record the same way. The Britain thread stays in `also:` as the host.
- Not mended: 10 of the reader's protocol rows stay out on my reading. These are Chinese delegations seen off or met at Peking, the Chinese and Vietnamese delegations at Peking airport, the cables from fifteen foreign ministers, and a DPRK reception.

Batch e, 8 rows:

- 6 rows taken out, all Chinese or Vietnamese acts done at home: Mao approves the plan for Zhou's trip (`cal.1966-06-16.china-leadership`); Zhou leaves Peking and stops in Afghanistan (`-2`); Zhou sees off the Chinese delegation (`cal.1966-10-27.china-leadership-2`); Yang hears officials back from Albania (`cal.1965-09-02.china-leadership-4`); the DRV Political Bureau hears Đồng's report (`cal.1966-10-04.vietnam-hanoi-2`); and Deng asks that an article on Tito not be printed (`cal.1965-12-17.china-leadership-5`).
- 2 rows put in: the Albanian chargé's letter of congratulation (`cal.1966-10.china-leadership-27`), and Đồng's speech at a meeting with a Czechoslovak delegation (`cal.1966.vietnam-hanoi-4`).

Batch f, 24 rows:

- 17 rows put in: receptions by the Albanian and Romanian embassies and attachés, Albanian teams, a troupe, journalists and a hydropower delegation received by Zhou, Mao's reception of the Albanian groups, the Wuhan meeting welcoming Shehu, the Vietnamese party's letter to the Romanian congress, Zhou's talk with the Albanian ambassador on the counselor's accident, and the instruction to Gronouski to tell the Poles that Warsaw would not do.
- 2 rows taken out: Zhou's note on the send-off at Peking (`cal.1968-11-16.china-leadership`), and Zhou seeing off Li Xiannian at Peking (`cal.1969-11-25.china-leadership`).
- 1 row mended in `also:`: `cal.1969-11-26.china-leadership`. The reader had added `china-foreign`, which is an ancestor of the primary thread `china-border-war`. I dropped it and kept Comecon.
- 4 rows restored: `cal.1967-12.soviet-union-czechoslovakia`, `cal.1968-01-05.vietnam`, `cal.1968-09-02.soviet-union` and `cal.1968-09-16.soviet-union`. The reader had dropped a value the entry already held, because it stood beside the primary thread's parent or child. The reader's task was to place Comecon, which has no parent and no child. The calendar keeps such pairs on purpose: the build lists an entry on a parent's index when `also:` names the parent. About 550 entries in the calendar hold one, so I put the values back.

## Entries found

I searched every entry from 1964-01-16 on that no batch listed. In the line I searched for the members' leaders and envoys (Hoxha, Shehu, Balluku, Ceaușescu, Maurer, Bodnăraș, Macovescu, Gomułka, Rapacki, Ulbricht, Mielke, Novotný, Dubček, Husák, Černík, Kádár, Zhivkov, Tito and others), their capitals and towns, their bodies (the Warsaw Pact, CMEA, Interkit, SED, Stasi) and the countries' names in several forms. In the note I searched for the chief leaders' names and the countries' and capitals' names in Chinese characters. I read each hit, and 41 are the thread's. Each is added to its batch's table, its `basis` beginning `AUDIT: found`:

- Batch d, 6 rows. These are Johnson's speech on "bridges" to Eastern Europe (May 23, 1964), three steps of the Albanian and Romanian visits of October 1964, and Maurer's visits to Austria, Iran and France. The last two take Comecon as their primary thread, since their present threads are holding places; the France thread stays in `also:` as the host.
- Batch e, 27 rows. These are steps of Shehu's visit to China in May 1966 and of Zhou's visit to Romania in June 1966, which the reader's list lacked because their lines name only the leaders. They also include Maurer's talks with the American, Dutch, Danish, Turkish and Swiss leaders; Maurer at Peking and Moscow in October 1966; Bodnăraș's briefing of the Chinese ambassador; Rapacki's three messages to Gronouski in December 1966; and the Stasi's dealings with the DRV's security ministry. Two of them, Maurer in Denmark and Maurer with Demirel, take Comecon as their primary thread.
- Batch f, 8 rows. These are Shehu at a performance, the SED's proposal of the Interkit meeting, Harriman with Macovescu, Mao with Balluku, Brezhnev with Černík and with Husák, the Soviets' word to their allies of a strike on China, and Zhou with Maurer in September 1969.

These rows have no row in the `-ids.tsv` files, which I did not change.

## The Jewish diaspora table

One entry of these batches is also in `jd.tsv`: `cal.1968-04-30.robert-kennedy-2`. Both tables leave it out of their new thread, with the same primary thread and the same `also:`. Nothing needed settling.

## The three entries filed under "Wuhan and the army" (4a)

- `cal.1967-07-07.china`, China's note to Czechoslovakia, is foreign business. The China thread that fits is "China: Foreign affairs" (`china-foreign`).
- `cal.1967-10-12.china-leadership` and `cal.1967-12-18.china-leadership` are Mao's receptions of Albanian delegations, and in both he speaks of the Cultural Revolution. The thread that fits is Mao's foreign business (`china-mao-foreign`), with `china-mao-cr` kept in `also:`. That is how batch f's own list files the like reception of Sept. 30, 1967 (`cal.1967-09-30.china-leadership`).
- In none of the three is Comecon plainly the chief business, so I did not mend their rows. They keep `china-wuhan` as their primary thread and Comecon as a secondary one. Their primary thread should be mended outside this table.
- The same thread holds other entries of 1967 that are not Wuhan's business. Three are in batch f's list: a British consul beaten at Shanghai airport (`cal.1967-05-24.china-leadership-3`), Mao on Yao Wenyuan's speech for the Albanian youth congress (`cal.1967-06-18.china-leadership`), and Zhou on the talks with the Albanian shipping company (`cal.1967-05-08.china-leadership-3`). This looks like a fault of the China re-threading, worth a check of its own.

## The checks by script

- Each table has one row for every id in its `-ids.tsv`, with no id twice. It also has the found rows, which no `-ids.tsv` lists.
- Every slug in the three tables is in `th.yaml`.
- No `also:` holds its own primary thread.
- No row puts Comecon beside a parent or child, since it has neither. Fifteen rows hold a parent and child pair that the entry already holds: in batch d, four rows with `vietnam` and `vietnam-hanoi`, one with `china` and `china-leadership`, and one found row of the same kind; in batch f, nine rows with the Soviet Union and Czechoslovakia threads or the Vietnam threads. All were in the calendar before. The tables change no thread but Comecon, except that 9 rows dropped their holding thread when Comecon became their primary thread.

## Is the table fit to apply?

Yes, on these terms.

- The apply should read the three `cm-X.tsv` tables, not the `-ids.tsv` lists, so that the 41 found rows are applied.
- It should accept a parent and child pair already held in `also:`.
- The nine rows whose primary thread becomes Comecon drop their old holding thread from `also:`, as their basis says.
- The eight defaults under "The rule I held the three batches to" are the session's own, not the owner's words. They should go into `notes/owner-rulings.md` under ruling 62, so the owner can overrule them. Each would be redone by rule from the tables' basis words.

## Disregarded under R0

Nothing in my brief narrowed what is an entry. Batch d's reader had left entries out as "minor" and as "protocol". R0 does not let "minor" narrow, and ruling 62 puts protocol in, so I mended those rows.
