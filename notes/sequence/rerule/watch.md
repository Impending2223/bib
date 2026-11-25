# The re-ruling: watching and "during" (Nov. 25, 2026)

The owner's ruling of Nov. 25 (owner-rulings 56, R25c) says an entry that records someone watching, hearing or reading an event as it happens follows the entry of that event, and so does an entry whose line names an event of the same day as the time of its own act. This note lists each case found, by day, with the words that show it and what was done. The patch is `inbox/2026-11-25-rerule-watch.yaml` (39 links, `patch-check` 0 errors).

An id is written as its date and the part after the date: `1960-07-02 elections-1960-2` is `cal.1960-07-02.elections-1960-2`. "A after B" means A follows B. "Written" means the link is in the patch. "None" says why not.

How the cases were found: a script of my own read every calendar entry (59,187) for words of watching, hearing, listening, television, radio and broadcast, for "during", "while", "as" and "when" before an act, and for tickers, galleries and tuned sets. I read each hit against the entries of its day. I also read every `follows: remove` in `inbox/merged/2026-11-2*` and the lines of `notes/sequence/*.md` that leave a pair unlinked for one hour. The words found are only the lines that say it; a reception worded some other way may be missed.

A rule used throughout: where the line holds several acts and the reception is not the first, a link would put the earlier acts after the event, so none was written (R25b; the entry needs splitting first).

## Reception

- 1960-07-02: `elections-1960-nomination-13` after `elections-1960-2`. "watch Truman's telecast in Nixon's office". Written. Ruling 55 had left it out as the same hour; the other answers to Truman already follow his press conference.
- 1960-07-13: Johnson "watches it on television" is the last sentence of `elections-1960-los-angeles-2`, which also holds Rayburn's nominating speech, so there is no second entry; none. `elections-1960-nomination` (committee staff watching the broadcast) already follows `elections-1960`.
- 1960-07-15: `elections-1960-2` after `elections-1960`. "Nixon watches Kennedy's acceptance on television". Written.
- 1960-07-15: `elections-1960-3` after `elections-1960`. "watches his son's acceptance at Luce's home". Written. This puts back the link the July 1960 audit took out; its line also holds a call to Luce before the speech, which is the entry's first act, but the watching is the lead.
- 1960-09-12: `elections-1960-kennedy-6` after `elections-1960`. "while Kennedy speaks to the ministers on television" (Rayburn watching). Written. The sequence note had left it as the same hour.
- 1960-09-26 and 1960-11-09: the governors "having watched the first debate" and Kennedy's staff watching Nixon on television already follow their events. Baughman "watching the returns" (`transition-and-staff-2`): no entry of the returns that day; none.
- 1961-04-21: `cuba-bay-of-pigs-2` after `cuba`. "watches the President take responsibility at his press conference". Written. The April 1961 audit had struck it as the same hour.
- 1961-05-05: `cuba` (the Council "breaks off for Shepard's launch, watched on Evelyn Lincoln's television") and `space` (the flight). None: the entry holds the whole meeting, and the items before the break come before the launch.
- 1961-06-24: the barbecue watching the debate already follows the debate.
- 1962-10-22: `missile-crisis-8` (the ambassadors briefed, "then the address on television with them"). None: the briefing is its first act and comes before the address. The other entries about the address already follow it.
- 1962-10-25 and 1962-10-28: Kennedy watching Stevenson and Zorin, and watching the networks, already follow their entries.
- 1963-05-03: `alabama-birmingham-2` after `alabama-birmingham`. Gaston, on the telephone, "breaks off at his window over Kelly Ingram Park" at the fire hoses. Written. The May 1963 note had left it as the same hour.
- 1963-06-11: `civil-rights-bill-2` after `alabama`. "the schoolhouse door on television. As Wallace leaves the doorway". Written. The June 1963 audit had left it as the same hour. `republican-party-congress` (Robert Kennedy calls during the meeting: "Wallace at the door"): none, the call is part of a whole-day meeting entry. `civil-rights-bill-6` (Alsop's dinner, "Let's tune in the president's speech"): none, the guests have not yet heard it and Bundy says it is not yet written.
- 1963-08-28: `march-on-washington-5` after `march-on-washington`. "watching King's speech on television". Written.
- 1963-09-06, 09-13, 09-26 and 11-19: Yang Shangkun hears the radio broadcast of the first, second, third and fifth commentaries on the Soviet letter. Written, each after the entry that records the commentary's printing (`china-leadership-7` after `-5`; `-4` after `-3`; `-5` after `-4`; `china-leadership-2` after `china-leadership`). A weaker case: the other entry records the print, the line the broadcast of the same text, and on Sept. 13 and 26 the broadcast begins at midnight. The owner may strike them if reception is to mean the same medium. On Mar. 13, June 16, July 19 and Oct. 21 the same kind of line has no entry of the text that day; none.
- 1963-10-01: `china-leadership-15` after `china-leadership-8`. Peng Dehuai "watches on television the celebration" in Tiananmen Square (the parade and rally entry). Written. The evening fireworks he watches from outside the gate (`china-leadership-9`) are not linked: the entry's own range is the morning.
- 1964-06-07: Romney watching Scranton on *Face the Nation* already follows.
- 1964-07-26: McCarthy on television, "the Johnsons watching": one entry; none.
- 1964-08-24: `elections-1964-6` after `elections-1964-7`. "The White House, watching the convention's opening" (the opening night with Pastore's keynote). Written. The August 1964 note had left it as simultaneous.
- 1965-05-15: `students-2` (Johnson "watches part of the proceedings on television", after Cooper's memo) and `students` (the teach-in). None: the memo is the entry's first act and is not shown to come after the teach-in.
- 1965-07-18: Connor on *Meet the Press*, Johnson watching: one entry, the broadcast has no entry of its own; none. 1965-07-28: the governors watching the news conference already follow it.
- 1965-11-27: `china-leadership-11` after `china-leadership-2`. Ye Qun hurries back "to listen from the next room to Luo Ruiqing's talk with Lin Biao". Written.
- 1966-02-04: Johnson "watches on television" the Foreign Relations hearing, in the hearing's own entry; none.
- 1966-07-29: `china-leadership-2` after `china-leadership`. Mao "listens to the whole rally from behind a curtain" (the Peking committee's meeting of activists). Written. The July 1966 note had called it the same occasion.
- 1966-11-09, 1967-11-08 and 1968-03-12: Bliss "watching the returns", King watching the acceptance, Johnson watching part of Rusk's hearing. The returns, the acceptance and the hearing have no entry of that day; none.
- 1968-03-13: `elections-1968` (the advisers at Stephen Smith's apartment, watching the 6:30 broadcast). None: the meeting began about 4 p.m., before the interview aired (Witcover, 70, as the March 1968 audit reads it), so a link would run the wrong way.
- 1968-03-31: `vietnam-congress` (Fulbright stops his speech "so that he and his audience can watch Johnson's address"), `elections-1968-humphrey` ("For Johnson's address, the two and their wives in the library"), `elections-1968-mccarthy-3` ("watch Johnson's address") and `elections-1968-johnson-6` ("a crowd around a radio. As Johnson says he will not run") each after `elections-1968` (the address). Written, four links. The March 1968 audit had listed these as heard during the address and left them unlinked. `elections-1968-johnson-16`: none; its first act is Temple's call before the address.
- 1968-06-04: `elections-1968-nixon` after `elections-1968`. "Nixon watches the California returns" (the primaries entry). Written. A looser case: the returns come in over the evening.
- 1968-06-05: `assassination-6` (the three television sets, "the latest medical bulletin") and `king-poor-peoples` (Coretta King and Young "watch the television and the medical reports"). None: the lines do not show which bulletin, and there were several (`assassination-14`, `-15`).
- 1968-08-28: `elections-1968-chicago-15` (Humphrey, 1:40 p.m., "watching the debate on Vietnam") and `elections-1968-chicago-platform` (Johnson "in the afternoon he watches the convention"). None: the first is dated by its own hour before the plank entry's, and the second opens with morning calls.
- 1968-11-02: `china-leadership-5` after `china-leadership`. Peng Dehuai "hears the broadcast of the enlarged Twelfth Plenum" at 2 a.m.; the other entry has the communique printed. Written (the same weaker case as the commentaries).
- 1969-04-01: `china-leadership-6` after `china-leadership`. Peng "hearing ... the news on the broadcast of the opening of the Ninth Congress". Written.
- 1969-04-14: `china-leadership-5` after `china-leadership`. Peng "listens to the news broadcast ... for the names of those on the rostrum of the Ninth Congress". Written, beside its old link to `-4`.
- 1969-04-24: `china-leadership-6` ("Jiang Qing, hearing the count of her votes, leaves the hall") and `china-leadership-11` (Peng "listens closely to the broadcast of the close of the Ninth Congress") after `china-leadership` (the Congress closes and elects). Written.

## During

- 1960-04-18: `china-leadership-15` after `china-leadership-14`. "during the Foreign Ministry's reception for the Bandung anniversary". Written. The April 1960 note called it the same hour. Both have one range.
- 1960-10-09, 1961-05-21, 1962-10-22 `missile-crisis-24` ("As the President begins speaking") and 1966-08-18 (Mao "during the rally"): each already follows its event.
- 1961-04-19: `cuba-bay-of-pigs-2` after `cuba-2`. "As the beachhead falls". Written. The April 1961 audit had called it the same time. The earlier link of `cuba-3` after `cuba-2` stays out: its news came about 10 a.m., before the fall at 2:32 p.m.
- 1961-06-04: `berlin-and-vienna-3` "while the leaders meet upstairs": the day has no entry of that meeting; none.
- 1962-03-03: `china-leadership-2` ("as Zhou Enlai leaves for Peking") and `china-leadership`. None: that entry holds the flight and the later meetings, so a link would put the run-through after them.
- 1962-09-25: `white-house` after `vietnam-2` ("during Thuận's visit") and `white-house-2` after `white-house` ("kept waiting in the Cabinet Room during the Kevu visit"). Written, two links.
- 1962-10-27: `governors` ("During the morning's ExComm") and `missile-crisis-2` (Radio Moscow announces "while the ExComm meets that morning"). None: the morning meeting has no entry of its own.
- 1963-09-16, 1964-06-22 and 1964-12-15: "during the Central Committee's conference on border defense", "during the Central Work Conference". None: the line names a conference of weeks, and no entry of the day records one of its sittings.
- 1964-03-17: `latin-america-panama` "during Shriver's Peace Corps meeting": no entry of the meeting; none.
- 1964-06-04: `china-leadership-6` after `china-leadership-3`. Li Dazhang talks with Yang "during the plenary session". Written.
- 1964-10-26: `elections-1964-johnson` after `goldwater`. The flyers handed out "outside Goldwater's rally". Written; the line gives the rally as the scene and the time. The October 1964 note had called it the same hour.
- 1964-12-01: `press-and-broadcasting` after `king`. "during the Hoover–King meeting". Written. This puts back the link the December 1964 audit took out.
- 1965-11-26: `china-leadership-8` after `china-leadership-7`. Zhou "present when Luo Ruiqing reports to Mao". Written. The November 1965 note had called it one meeting, no order.
- 1965-12-27: `vietnam` after `vietnam-pause`. Johnson's deferral of the bombing, the calls to Taylor and Rusk, was made inside McNamara's talk of 8:05 to 10:55 p.m. Central time. Written with a basis. The lines do not show it; the December 1965 audit read FRUS III, docs. 253–54 and Gibbons, IV, 127, and I took the basis from its note without opening them.
- 1966-10-24: `vietnam-asian-trip-2` after `vietnam-asian-trip`. "Manila, during the conference. A luncheon". Written.
- 1967-10-21: `war-opposition-2` ("The march's weekend") and `war-opposition-3` ("During the march, McNamara ...") after `war-opposition` (the March on the Pentagon). Written, two links.
- 1968-03-13: `robert-kennedy-campaign-decision-6` after `elections-1968`. Edward Kennedy's call to Clifford at Stephen Smith's apartment. Written with a basis: Witcover, 74, has the call made during the advisers' meeting (from the March 1968 audit's note; I did not open the book).
- 1968-03-31: `elections-1968-9` after `elections-1968`. "McCarthy at a students' meeting as Johnson withdraws". Written.
- 1968-03-16: the staffs' meeting "while the candidate was en route" and the *Newsweek* call "during the afternoon session" already follow the announcement.
- 1968-05-24: Kennedy's swim and McCarthy's wire. Witcover, 213, says "while", but neither line names the other and no direction is given; none.
- 1968-06-08: `king` (Clark announces the arrest "during the Kennedy funeral"). None: the entry opens with the arrest at London Airport, hours before the funeral.
- 1968-09-07: `women` ("Inside the hall, during the broadcast, a banner"). The pageant has no entry; none.
- 1969-04-19: "During the Ninth Congress" has no entry of that day's sitting; none. 1969-04-24: `china-leadership-4` ("During the vote a delegate ... jumps onto the stage") is a part of the closing entry (`part_of`) and may follow only its sibling parts; none needed.

## The links an audit took out

- Put back above: 1960-07-15 `elections-1960-3`; 1964-12-01 `press-and-broadcasting`; 1961-04-21 `cuba-bay-of-pigs-2` (struck before the merge); 1963-06-11 `civil-rights-bill-2` (never written).
- Left out, because they are no matter of watching or "during": 1960-01-08, 1962-01-08, 1962-07-06, 1962-07-12, 1962-07-19, 1963-07-12 (`china-leadership-8` after `-7`: one talk at one evening visit, not a reception), 1963-12-17 (the call after the address, not the Chamizal vote), 1965-11-05 (Yang's diary has Peng Zhen "already" telling him; one sentence, no order), 1966-05-17, 1966-05-26, 1966-07-13, 1966-10-06, 1967-08-08, 1968-06-05 (Witcover's printed order), 1961-04-19 `cuba-3` (told after, at other hours).

## What is left

- Entries that hold two acts, one of them a reception or an act during, need splitting before they can take a link: 1961-05-05 `cuba`, 1962-03-03 `china-leadership`, 1962-10-22 `missile-crisis-8`, 1963-06-11 `republican-party-congress`, 1965-05-15 `students-2`, 1968-03-13 `elections-1968`, 1968-06-08 `king`.
- The broadcast cases (five of the Yang and Peng lines) rest on a broadcast of a text the other entry records as printed. If the owner means reception of the same medium, strike them: 1963-09-06 `china-leadership-7`, 1963-09-13 `-4`, 1963-09-26 `-5`, 1963-11-19 `-2`, 1968-11-02 `-5`.
- Days where a reception has no entry of its event (returns, hearings, speeches): left as the words only. Those events are readers' work, not links.
