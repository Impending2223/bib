# Marc J. Selverstone, *The Kennedy Withdrawal: Camelot and the American Commitment to Vietnam* (2022): the calendar against the book

Card `w.selverstone-kennedy-withdrawal`. Read Oct. 28–29, 2026, from the owner's copy on the Drive: Harvard University Press's PDF of the first printing (2022; the cloth ISBN 9780674048812), paginated as the print. Printed page = PDF page − 10 throughout, checked by the printed folios at pp. 20, 100, 150, 200, 240, 252 and 290. Text pp. 1–248; notes pp. 249–310, numbered by chapter, each headed "Notes to Pages ...". `sources/cited-records/selverstone-kennedy-withdrawal.yaml` keys each note by the text page it serves and its number. Several records under one note are lettered (`3a`, `3b`).

Patch: `inbox/2026-10-29-book-reeves-selverstone.yaml` (book-reeves-selverstone), shared with Reeves's reading. An entry both books bear on gets one edit, built on the entry as it now stands.

What the book is for the calendar: the withdrawal of the thousand and the 1965 target, from planning in 1962 to the Model Plan's end in March 1964. It draws on the recorded meetings (the Miller Center's draft transcripts), the NSF and the Defense and JCS files, FRUS, and the Public Papers. Its thesis, stated as the book states it: the withdrawal was McNamara's plan as much as Kennedy's, a hedge kept conditional on the war's progress. It served as pressure on Saigon and as cover at home more than as a decision to leave. The memory of it after 1963 made "Camelot's" Vietnam. The thread it most concerns is Force levels (`vietnam-force-levels`). Its statement for Cal. II (`c2`) now names the 1963 stations: the May conference and the thousand, the White House statement of Oct. 2 and NSAM 263, Harkins's announcement of the first 300, and the Model Plan superseded in March 1964. Those stations had been in `c`, which speaks to Cal. I. Cal. I keeps Krock, Honolulu 1962 and the October conference. `c3` is unchanged.

How the list was made: every date in the text, pp. 1–248, was scanned in page order (147 dated mentions), the year taken from the chapter's span where the sentence does not give it (and corrected by hand where the scan erred: pp. 157, 161, 200, 201, 209). Each was set against every entry of its day in a fresh dump of the calendar (all threads; Oct. 28, 18:30) and against the pending patches. Where the event was in, the page was added, with its row, its records' `via` rows and a parenthetical where it bears part. Where it was not in and the brief takes it, an entry was made from the page and its records, read first in FRUS, the Public Papers, the Record and the recordings' catalogues. Four of the adds first planned had meanwhile been entered by other runs (Jan. 3 and Feb. 21, 1962, Vietnam; Feb. 13, 1962, Republican Party; Aug. 31 and Sept. 23, 1963, Vietnam). Those became edits of the entries now in, keeping their text, cites and rows. Selverstone's page and rows were added, and a Check where he differs. Three entries cited the book before this reading, without a pinpoint (Sept. 2, Sept. 21 and Oct. 11, 1963). Each was read and pinned.

## Entries held, in part, or differing (35 edited)

- 1961: Jan. 28; May 11; Nov. 3, 11, 15, 22.
- 1962: Jan. 3; Feb. 13 (Republican Party), 21 (Laos), 21 (Vietnam); Apr. 4; May 1; July 23; Dec. 26.
- 1963: Feb. 24; Mar. 6 (economy: the news conference's answer on aid to South Vietnam added at the end); May 17; July 17 (the news conference's Vietnam answer, the same); Aug. 31 (vietnam-2); Sept. 2, 21, 23; Oct. 2, 8, 9 (trade), 11, 31 (elections 1964); Nov. 20, 24, 26; Dec. 21.
- 1964: Feb. 3, 29 (defense); Mar. 17.
- The thread statement, Force levels (above).

Eleven of these are also Reeves's edits; each entry is one op. Units added to `c` (eight entries: Feb. 13 and Feb. 21, 1962; Mar. 6, July 17, Sept. 23, Oct. 9 and Oct. 31, 1963; Feb. 29, 1964; each news conference's Vietnam answer is listed in Vietnam by `also:`, one event, one entry) go at the end, and the hash is recomputed. Every edit was diffed against the entry as it now stands. No cite, sentence or row of another run's is lost.

Differences, each a Check:

- 1962-02-13 (Republican Party): the day. Selverstone gives Feb. 13; the *Times* reports it Feb. 14.
- 1962-05-01 (Ball's speech): the day and place. Selverstone gives Apr. 30, the Economic Club of Detroit (69).
- 1963-09-23 (the McNamara–Taylor mission's sendoff, recorded): the recording not heard; the words are Selverstone's transcript's.
- 1964-01-31 (Lindsay, new): Selverstone dates it Jan. 28; the Record's page is the House's of Jan. 31.
- 1963-10-05 (vietnam-2, new): the hour. Forrestal gives 9:30 a.m., PRDE 11 a.m.
- 1963-12-03 (Johnson on the withdrawal, new): the day is the memorandum's.

## New entries (32)

- 1961: Dec. 16 (Honolulu, McNamara's first conference on Vietnam).
- 1962: Apr. 6 (Kennedy and Harriman on Galbraith's memorandum); May 1 (vietnam-2, the White House meeting); Sept. 25 (Taylor's report, recorded); Oct. 8 (Honolulu).
- 1963: Jan. 30 (Felt at the Pentagon, "three years"); Feb. 1 (the recorded meeting); Feb. 4 (Wheeler); Apr. 4 (Robert Thompson with Kennedy); Apr. 29 (McNamara with the Chiefs on the thousand); May 6 (Honolulu, the eighth conference); May 7 (McNamara to Kennedy, recorded); May 22 (the news conference); Sept. 3 (the plan approved for planning); Sept. 6 (the Model Plan approved); Sept. 11 (vietnam-2, the 6 p.m. meeting at State); Sept. 19 (the recorded meeting on the mission); Oct. 5 (vietnam-2, the Cabinet Room); Nov. 14 (the news conference); Dec. 2 (Harkins's announcement); Dec. 3 (Johnson questions the withdrawal).
- 1964: Jan. 31 (Lindsay in the House; Republican Party: In Congress); Feb. 25 (Johnson to McNamara, recorded); Feb. 26 (Bundy to the overseas writers); Feb. 27 (Dirksen and Halleck for the joint leadership; In Congress); Mar. 2 (Johnson to McNamara, recorded); Mar. 5 (McNamara's news conference); Mar. 7 (Johnson's news conference); Mar. 9 (Keating's "20 Questions"; In Congress); Mar. 15 (the networks' interview); Mar. 26 (McNamara to the Forrestal dinner); Mar. 27 (the Model Plan's phase-down superseded).

Each was compared with every entry of its day. Three share day and thread with an entry of another event, a distinct meeting each, and carry `-2` ids. The merge will flag them as possible duplicates (`./bib resolve ID --take keep`): 1962-05-01 vietnam-2, 1963-09-11 vietnam-2, 1963-10-05 vietnam-2.

## Records

`sources/cited-records/selverstone-kennedy-withdrawal.yaml`: 99 records from the notes the entries cite. Memoranda 36, transcripts 17, recordings 13, minutes 6, reports 5, press 5, speeches 4, and the rest. 64 were found: FRUS documents, the Public Papers, the bound Record, PRDE's and the Miller Center's pages. 29 were read and stand as the entries' primary records. The recordings were not heard; their catalogue pages are cited, the quotation with "Check: the recording not heard". The unread records stand in To check, "(cited by [[w.selverstone-kennedy-withdrawal]], PAGE n.N)". Not found (paper only, or not online): the NSF and Defense files the notes give by box (JFK Library; RG 218 and RG 330, National Archives), the JCS files, and the Miller Center's draft transcripts (Selverstone's own, not public).

## Passed over

Re-ruled Nov. 6, 2026, under R18 as amended (batch 6; the rulings in "Batch 6" below).

How the list was made: the date scan above. Each dated mention not cited by an entry was read in its paragraph and set against the entries of its day (±3 days). "Already in as" names the entry that has it: cited where Selverstone adds something, otherwise left. "Minor" means only what the brief's rule says. Page | date | event | why.

The "already in" rows read against the calendar, Nov. 10, 2026 (batch 7), and again by the reader's card, Nov. 11, 2026 (batch 8; patch `inbox/2026-11-11-b8-selverstone.yaml`). Rulings, page by entry:

- Cited under the entry: p. 20 (Jan. 6, 1961, berlin-and-vienna); 21 (Jan. 30, program); 29 (May 25, space); 31 (Aug. 13, berlin-and-vienna); 36 (Oct. 11, vietnam); 38 (Oct. 18, vietnam); 48 (Dec. 8, vietnam); 52 (Jan. 11, 1962, program); 55 (Feb. 8, vietnam); 57 (Feb. 14, vietnam); 58 (Feb. 20, vietnam-congress); 63-64 (Feb. 27, vietnam); 98 (Jan. 2, 1963, vietnam); 118 (May 8, vietnam); 126 (May 12, vietnam); 133 (June 11, vietnam); 142 (Aug. 21, vietnam); 143 (Aug. 28, vietnam); 143-44 (Aug. 29, vietnam; the row's p. 146 is de Gaulle's Aug. 29 statement, not Kennedy); 150 (Sept. 5, vietnam-congress); 147-48, 152 (Sept. 9, vietnam; and 152 under vietnam-saigon, Lodge with Diem); 154 (Sept. 10, vietnam); 158 (Sept. 15, alabama); 158-59 (Sept. 17, vietnam; the row's p. 158 is the sending of McNamara and Taylor); 163 (Sept. 26, vietnam-congress); 196 (Nov. 1, vietnam); 217 (Jan. 30, 1964, vietnam); 218 (Jan. 16, 1964, vietnam, the approval; 34A from Feb. 1); 219 (Feb. 21, 1964, vietnam).
- Variant and Check on: Aug. 21, 1963 (p. 142 puts the raids and martial law on the night of Aug. 21); May 8, 1963 (p. 118: "over twenty" killed and injured, against eight killed). Variant already on Mar. 24, 1963, foreign-aid (p. 111: the Clay report "Released on March 22"): no cite, the page disputes the unit.
- Not borne out (no cite): Apr. 29, 1961, laos (p. 24 treats the NSC meeting of that day, entered as cal.1961-04-29.vietnam by the batch 8 Reeves patch; the entry is Rusk's meeting at State); Oct. 1, 1963, vietnam-saigon (p. 136: Oct. 1 is Felt's earliest date for the decision, a planning date; the entry is Taylor's call on Minh); Oct. 30, 1963, vietnam (p. 153: the troop peak of 16,732 by Oct. 30; the entry is Lodge's cable).
- Background rows, no single entry and nothing on the page the series rests on: Bay of Pigs (p. 23, two sentences); the missile crisis (p. 96); Dallas (pp. 203, 233). On p. 203 Kennedy's remarks prepared for the Trade Mart, Nov. 22 ("key role," "we dare not weary of the task"): not in `c` of the assassination entry, which cites the Public Papers text; a possible entry for the owner.
- Notes not read: the cited records behind these pages are not added under "To check:" in this patch.

Where batch 8 stopped: all 36 rows ruled; none left open.


| page | date | event | why |
|---|---|---|---|
| 20 | 1961-01-06 | Khrushchev's wars of national liberation speech | already in as cal.1961-01-06.berlin-and-vienna (background) |
| 21 | 1961-01-30 | State of the Union | already in as cal.1961-01-30.program (background) |
| 23 | 1961-04-15/21 | the Bay of Pigs; Kennedy the "responsible officer" | already in under Cuba, Apr. 15–21 (background) |
| 24 | 1961-04-29 | NSC on Laos and Vietnam | already in as cal.1961-04-29.laos |
| 29 | 1961-05-25 | the urgent needs message | already in as cal.1961-05-25.space |
| 31 | 1961-08-13 | the Berlin wall | already in as cal.1961-08-13.berlin-and-vienna |
| 34 | 1961-09-18 | Phước Vĩnh, Phước Thành's capital, taken by the PLAF | lead: the attack (FRUS 1961–63, I; the press) |
| 36 | 1961-10-11 | the NSC sends Taylor | already in as cal.1961-10-11.vietnam |
| 38 | 1961-10-18 | Taylor in Saigon | already in as cal.1961-10-18.vietnam |
| 39 | 1961-10-24 | Taylor, finishing the tour, warns of reinforcement | lead: Taylor's cable (FRUS 1961–63, I) |
| 47 | 1961-11-20 | Galbraith to Kennedy against the program | lead: the letter (FRUS 1961–63, I); also Reeves 260 |
| 48 | 1961-12-08 | the Jorden report, *A Threat to the Peace* | already in as cal.1961-12-08.vietnam |
| 52 | 1962-01-11 | State of the Union | already in as cal.1962-01-11.program |
| 55 | 1962-02-08 | MACV | already in as cal.1962-02-08.vietnam |
| 57 | 1962-02-07 | news conference: less than forthcoming on Vietnam | lead: 1962 Pub. Papers |
| 57 | 1962-02-14 | news conference: "We have not sent combat troops" | already in as cal.1962-02-14.vietnam |
| 58 | 1962-02-20 | Harriman before Foreign Relations | already in as cal.1962-02-20.vietnam-congress |
| 63 | 1962-02-27 | the palace bombed | already in as cal.1962-02-27.vietnam |
| 64 | 1962-04-01 | Clifton to Bundy: prod McNamara on the plan | minor (staff) |
| 68 | 1962-04-11 | State's circular: a Vietnamese war | lead: the circular (FRUS 1961–63, II) |
| 69 | 1962-03-16 | *Life*'s "Story of the Week" | minor (a magazine's story without an act) |
| 69 | 1962-04-30 | Higgins on Ball's speech | minor (a column); the speech in as cal.1962-05-01.vietnam (cited, Check) |
| 96 | 1962-10-16/11-20 | the missile crisis | already in under Missile crisis (background) |
| 98 | 1963-01-02 | Ấp Bắc | already in as cal.1963-01-02.vietnam |
| 105 | 1963-01-21 | press and liaison officials plan "favorable accounts" | minor (an operation below the level) |
| 111 | 1963-03-22 | the Clay Committee's report released | already in as cal.1963-03-24.foreign-aid; Selverstone gives the release as Mar. 22 (111): lead, the day |
| 118, 126, 133 | 1963-05-08 | Huế | already in as cal.1963-05-08.vietnam |
| 126 | 1963-05-12 | the Ngôs' campaign against the American profile | already in as cal.1963-05-12.vietnam |
| 126 | 1963-06-05 | the cost study due | minor (a deadline) |
| 133 | 1963-06-11 | Quảng Đức | already in as cal.1963-06-11.vietnam |
| 133 | 1963-06-25/07-01 | Krulak's inspection | lead: Krulak's report (FRUS 1961–63, III) |
| 136 | 1963-07-21 | Felt submits the thousand-man plan to the Chiefs | lead: the plan (the JCS files; Selverstone 136 n.76) |
| 136 | 1963-10-01 | not before Oct. 1 | already in as cal.1963-10-01.vietnam-saigon (other matter); a planning date, minor |
| 139 | 1963-10-20 | the Chiefs' decision due | minor (a deadline) |
| 142, 150 | 1963-08-21 | the pagoda raids | already in as cal.1963-08-21.vietnam |
| 143 | 1963-08-28 | the CIA station's and the estimates' judgments | already in as cal.1963-08-28.vietnam |
| 146 | 1963-08-29 | Kennedy on helping the Vietnamese unify | already in as cal.1963-08-29.vietnam |
| 147, 152 | 1963-09-02/12 | ten days of statements; Church's resolution | already in as cal.1963-09-02.vietnam (cited), 09-12.vietnam and 09-12.vietnam-2 (Reeves) |
| 150 | 1963-09-05 | Hilsman before the Far East subcommittee | already in as cal.1963-09-05.vietnam-congress |
| 152 | 1963-09-09 | Lodge to Diệm on the Senate's mood | already in as cal.1963-09-09.vietnam and 09-09.vietnam-saigon |
| 153 | 1963-10-30 | deployments "critical to current operational" needs | already in as cal.1963-10-30.vietnam |
| 154 | 1963-09-10 | Krulak and Mendenhall | already in as cal.1963-09-10.vietnam |
| 157 | 1963-09-14/15 | Hilsman's "tracks" | lead: the paper (FRUS 1961–63, IV) |
| 157 | 1963-08-29 | de Gaulle's statement on Vietnam | lead: the statement (the press; no entry found) |
| 158 | 1963-09-15 | the Birmingham church bombing | already in as cal.1963-09-15.alabama |
| 158 | 1963-09-16 | Diệm ends martial law | lead: the day (FRUS 1961–63, IV) |
| 158 | 1963-09-17 | Kennedy sends McNamara and Taylor | already in as cal.1963-09-17.vietnam |
| 161 | 1963-05-07 | the White House conversation with McNamara | already in as the new cal.1963-05-07.vietnam-force-levels |
| 163 | 1963-09-26 | McGovern urges withdrawal | already in as cal.1963-09-26.vietnam-congress |
| 176, 184 | 1963-10-03/04 | working sessions on the report and the statement | already in as cal.1963-10-02.vietnam (cited) and the new 10-05.vietnam-2 |
| 188 | 1963-11-15 | the CPSVN's revision due | minor (a deadline) |
| 191 | 1963-10-07 | Bundy at the staff meeting: "pollyana-ish" | minor (a staff meeting) |
| 192 | 1963-10-18 | the draft press release, 16,730 | minor (a draft) |
| 193 | 1963-10-21 | the 16,500 figure to be leaked | minor (an operation below the level) |
| 193 | 1963-11-04/05 | the Chiefs approve the revised composition; Felt told | lead: the Chiefs' paper (JCS files) |
| 196 | 1963-11-01 | the coup | already in as cal.1963-11-01.vietnam |
| 200 | 1963-11-20 | Defense "reaffirms" the thousand | lead: the release (the press); the conference in as cal.1963-11-20.vietnam (cited) |
| 200 | 1963-12-03 | the first 300 leave | already in as the new cal.1963-12-02.vietnam-force-levels |
| 201 | 1963-09-23 | McNamara with Kennedy | already in as cal.1963-09-23.vietnam (cited) |
| 203, 233 | 1963-11-22 | Dallas | already in under the assassination (background) |
| 209 | 1963-10-02 | the statement and the coup | already in as cal.1963-10-02.vietnam |
| 209 | 1963-11-24 | Johnson's first meeting | already in as cal.1963-11-24.vietnam (cited) |
| 211 | 1963-11-30 | Sihanouk proposes a conference to neutralize Indochina | lead: the proposal (FRUS 1961–63, IV; the press) |
| 217 | 1964-01-30 | Khánh's coup | already in as cal.1964-01-30.vietnam |
| 218 | 1964-02-01 | 34A to begin | already in as cal.1964-01-16.vietnam (the approval) |
| 219 | 1964-02-21 | Johnson at Los Angeles | already in as cal.1964-02-21.vietnam |
| 221 | 1964-02-15 | Felt: the planning assumption "no longer valid" | lead: Felt's message (JCS files; Selverstone 221 n.85) |
| 236–241 | 2001–2009 | Sept. 11; Iraq; Obama's Afghanistan decision | out of the brief |

## Batch 6: the rows re-ruled (Nov. 10–11, 2026)

The owner's copy again (Drive 1knBIhZOfZe3OXNlKBtBKn-CXqFoKXt4C, the publisher's PDF, by the direct route into the scratchpad; deleted after): printed page = PDF page − 10 held (pp. 64, 69, 105, 191–193 and the note pages 264, 266, 275, 293 read on their images as well as the text). Patch `inbox/2026-11-06-b6-selverstone.yaml` (7 entries added, their claim-map rows); witnesses `inbox/witnesses/2026-11-06-b6-selverstone.yaml` (7 rows and one amendment: the memorandum of Oct. 7, 1963, read); 8 edges appended to `sources/witnesses/by-work/selverstone-kennedy-withdrawal.yaml`. Three records read in FRUS and cited first: 1961–63, III, doc. 23; IV, docs. 187, 201. Re-ruled: the rows ruled minor for staff, a draft, a magazine's story, or "an operation below the level" (R18 as amended: "below the level" means only a unit's routine; the planning of communications is R7's).

| Page | Date | Event | Ruling now |
|---|---|---|---|
| 64 | Mar. 29, 1962 | Clifton to Bundy: prod McNamara on the plan (the note's date) | entered, `cal.1962-03-29.vietnam-force-levels` (Check: whose words) |
| 69 | Mar. 16, 1962 | *Life*'s "Story of the Week" | entered, `cal.1962-03-16.press-and-broadcasting` (R13: *Life*) |
| 69 | Apr. 26, 1962 | Ball and Bundy by telephone on the speech; Kennedy's guidance (not logged before) | entered, `cal.1962-04-26.vietnam` |
| 69 | Apr. 30, 1962 | Higgins on Ball's speech | already in: `cal.1962-05-01.vietnam` carries the *Herald Tribune*'s reading |
| 105 | Jan. 21, 1963 | press and liaison officials plan "favorable accounts" | entered, `cal.1963-01-21.vietnam` (FRUS 1961–63, III, doc. 23) |
| 191 | Oct. 7, 1963 | Bundy at the staff meeting: "pollyana-ish" | entered, `cal.1963-10-07.vietnam-force-levels` (FRUS IV, doc. 187) |
| 192 | Oct. 18, 1963 | the draft press release, 16,730 | entered, `cal.1963-10-18.vietnam-force-levels` (FRUS IV, doc. 201: Kattenburg to Hilsman on the proposed release) |
| 193 | Oct. 19–21, 1963 | the 16,500 figure to be leaked | entered, `cal.1963-10-19.vietnam-force-levels` (the telegram's day; the leak set for Oct. 21) |
| 126, 139, 188 | June 5, Oct. 20, Nov. 15, 1963 | the deadlines (the cost study, the Chiefs' decision, the CPSVN's revision) | still passed over: a deadline set is no event; the papers that set them are the entries already cited |
| 136 | Oct. 1, 1963 | "not before Oct. 1" | still passed over: a planning date, no event |

## Leads

Written into `notes/leads.md`, Foreign: Phước Vĩnh, Sept. 18, 1961; Taylor's cable of Oct. 24, 1961, and Galbraith's letter of Nov. 20, 1961 (FRUS 1961–63, I); State's circular of Apr. 11, 1962; Krulak's inspection, June 25–July 1, 1963; Felt's plan of July 21, 1963, and his message of Feb. 15, 1964; Hilsman's tracks, Sept. 14–15, 1963; de Gaulle's statement of Aug. 29, 1963; Diệm's end of martial law, Sept. 16, 1963; Sihanouk's proposal of Nov. 30, 1963; the Clay report's release day.
