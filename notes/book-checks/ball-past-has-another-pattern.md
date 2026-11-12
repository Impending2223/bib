# Ball, *The Past Has Another Pattern* (1982): the calendar's citations, and the book against the calendar

Card `w.ball-past-has-another-pattern` (alias `-1982`). George W. Ball's memoir (Norton, first edition). The owner's copy (Drive, the file id in the batch brief; archive.org's scan `pasthasanotherpa00ball`, 552 PDF pages with a text layer), read with `pdftotext -layout`; cited by the printed page. Offset: printed page = PDF page - 18 throughout. The plates (PDF 253-273) are counted in the book's pagination as pp. 235-255: the text runs on from p. 234 to p. 256 without a break. Checked on the running folios and on the page images at PDF 402 (p. 384) and PDF 520 (the notes, p. 502). The PDF deleted when the run was done.

The first run (Oct. 29, 2026, patch `b3-ball`, merged: 134 entries added, 86 edited) read the book within the span, pp. 152-447, and wrote no book-check file; this file is the second run's (Nov. 4, 2026, patch `b3-ball-2`).

The book has notes, by chapter, pp. 495-508: few, many of them Ball's own asides. Each note was placed on its page by the superscript in the scan's text layer (its small type); the notes' running heads, "(pages 253-306)", misprint the first page of that range (233). Chapter 29 on (p. 448) is after Jan. 20, 1969.

## The second run (Nov. 4, 2026)

1. The pages the calendar did not cite, within the span: 150-185, 188-189, 197-199, 204-205, 208-210, 220-231, 259-260, 274-275, 286, 308-309, 316-322, 327-339, 359-364, 370-376, 384-387, 410-435, 448-452 (the plates aside), read for each dated event (the whole of 150-185 and 188-209; elsewhere each sentence with a date, month, season or day, and the paragraph around it where an event was dated), set against the tree and the ledger.
2. The notes on the pages the calendar cites: each witness registered (R35), the studies and memoirs the conversion of Nov. 3 left out among them.

Patch `inbox/2026-11-03-b3-ball-2.yaml` (18 ops; patch-check 0 errors, 2 warnings, both same-day flags of distinct events: `cal.1960-07-26.elections-1960` is the Republican convention, `cal.1961-09.transition-and-staff` Landis's resignation; `./bib resolve ID --take keep`).

New entries (7): Ball's letter to Stevenson, July 26, 1960 (159); Ball's first trip to Europe and Erhard, Mar. 1961 (184-85); Ball's memorandum to Kennedy on Britain, May 1961 (209); Ball Acting Secretary, Aug. 4-10, 1961 (171); Rusk's division of the Under Secretaries' work, Sept. 1961 (171-72); Alsop's column and Ball's reply, Nov. 23, 1964 (384); Clifford's statement of Dec. 29, 1968 (414).

Cites on entries in the tree: the trade bill's votes, June 28 and Sept. 19, 1962 (198); Nkrumah at the White House, Mar. 8, 1961 (185); the foreign aid message, Mar. 22, 1961 (183); Hammarskjöld's death, Sept. 18, 1961 (229); the Dominican coup, Sept. 25, 1963 (327); the guarantor powers' appeal on Cyprus, Dec. 24, 1963 (338); Wilson in Washington, Dec. 7, 1964 (336); Stevenson's death, July 14, 1965 (151-52).

Ball's account against the record, "Check:" added:

| Entry | The entry | Ball |
|---|---|---|
| `cal.1962-11-29.missile-crisis` | Kennedy with Mikoyan, Nov. 29 | Nov. 30; Ball dined with Mikoyan at Udall's that night (308) |
| `cal.1962-12-20.latin-america` | Bosch elected, Dec. 20 | Dec. 19 (327) |

## Witnesses (R35)

New rows in `inbox/witnesses/2026-11-03-b3-ball-2.yaml` (20); the edges in `sources/witnesses/by-work/ball-past-has-another-pattern.yaml` (35 added, one corrected):

- Corrected: `233 n.8` is Schlesinger, *A Thousand Days*, 576 (the address of Dec. 19, 1961 as "the definitive statement" of the Congo policy), not Ball's pamphlet; registered as a passage of Schlesinger's (`part_of` the card) resting on the address, so the via row of `cal.1961-12-19.congo` still leads to the address. The pamphlet is `229 n.5`.
- Cards: Martin, *Adlai Stevenson and the World*, 534 (160 n.2); Schlesinger, *A Thousand Days*, 157 (161 n.3); Macmillan, *At the End of the Day*, 111 (218 n.4); Ball, *Discipline of Power*, 84-85 (268 n.3); Robert Kennedy, *Thirteen Days*, 89-90 and 87 (288 n.1, 307 n.4); Hilsman, 203, Allison, 141-42, and Chayes, 96f. (306 n.2: Ball's note disputes the first two, and Abel's, on an order of August 1962 to remove the Jupiters; it quotes NSAM 181, registered); Valenti, *A Very Human President*, 319-40 (399 n.9).
- Rows: Watt's *Survey of International Affairs, 1961*; Cecil King's diary, Sept. 10, 1966; Martelli; Stebbins's *United States in World Affairs*, 1961 and 1963; Security Council resolution S/4426 and Hoskyns's chronology; Gérard- Libois; Piers Dixon's *Double Diploma*; Kulski; Abel's *Missile Crisis*; Bernstein in the *Political Science Quarterly*; Lefever's *Spear and Scepter*; Crawford Young in *Africa Report*; Weintal and Bartlett's *Facing the Brink*; Radvanyi's *Delusion and Reality*; Kennedy's address at American University (the Papers' item, not read); Johnson's remark to Ball on Goldberg's mission to the Pope (405 n.3) and Clifford's account to Ball of his Asian tour (407 n.6), both remarks known only by Ball's recollection.
- Not registered: the notes that are Ball's asides with no source (161 n.1, 200 n.3, 369 n.13, 370 n.14, 400 n.10, 359 n.3, 359 n.5), literary quotations (276 n.2), and notes on pages outside the calendar's citations (pp. 1-151, 322 n.2, 361-364, 385-387, 410-423, 427, chs. 29-30).

## Passed over

The "already in" rows read against the calendar, Nov. 10, 2026 (batch 7), the eleven still open read again Nov. 11, 2026 (batch 8, patch `2026-11-11-b8-ball`; the page images read for the dates, numbers and quotations cited):

| p. | Row | Ruling |
|---|---|---|
| 159 | the convention, McCarthy's speech, the demonstration | cited under `cal.1960-07-13.elections-1960` |
| 170 | Bowles lets it be known | entered as `cal.1961-04.cuba-3` (month, "Check: the day") |
| 172 | Rusk telephones Ball at Geneva | already cited (172, `cal.1961-11-26.transition-and-staff`) |
| 180 | the inaugural address from the steps | cited under `cal.1961-01-20.transition-and-staff` |
| 197 | Ikeda's dinner; the soundings | already cited (197, `cal.1961-07-11.japan`; 195-97, `cal.1961-07-11.foreign-aid`) |
| 225-28 | the Congo | cited under `cal.1960-06-30.congo`, `-07-10`, `-07-11`, `-07-13`, `-08-01` (Check: Ball's Aug. 3 and 8), `-08-12`, `-09-05`, `-09-14`, `cal.1961-02-13.congo`; Check on `cal.1961-02-15.congo` (Ball's Feb. 25); Sept. 18 already cited. Not entered: Gizenga's Stanleyville government, Lumumba's repulse in Katanga (no day) |
| 275 | Kennedy asks Ball to see Salazar and Ayub | cited under `cal.1963-08-28.africa`, with a Check ("early fall"; Ball left Aug. 28) |
| 327-29 | the Dominican Republic | cited under `cal.1962-12-20.latin-america`, `cal.1965-04-24`, `-04-25`, `-04-28` (the junta, the "critic" message), `-04-28` Cabinet Room meeting, `-04-30` (Martin), `-05-15` (Fortas), `-05-16`, `cal.1965-06-01`, `cal.1966-06-01`; Sept. 25, 1963 already cited. Lead: Ball's lunch with Bosch in Washington "just before he took office" (undated even to the month) |
| 361-64 | Laos to 1961 | cited under `cal.1961-01-19.laos`, `cal.1960-08-09.laos`, `-09-10`, `cal.1960-12-13.laos`, `cal.1961-03-23.laos`; Kennedy's 1956 speech before the span. Leads: Rostow's twenty-five thousand troops, Kennedy's urging the British to an International Control Commission (spring 1961, no day) |
| 370 | the Buddhist crisis | cited under `cal.1963-05-08.vietnam` (Check: nine killed against eight), `cal.1963-06-11.vietnam`, `cal.1963-08-21.vietnam`; Mme Nhu's "bonze barbecue" and the seven suicides undated (leads) |
| 432 | Ball's resignation | cited under `cal.1966-09-21.transition-and-staff` (432, beside 425) |

Where batch 8 stopped: all eleven rows read; none left.

Re-ruled Nov. 6, 2026, under R18 as amended: the rows ruled minor (private, social, no public business, a routine), in "Batch 6" at the end of this file.

Every dated event within the span on the pages read this run (step 1 above) that is not entered and not already in the calendar; the first run's passes over the cited pages were not logged and are not repeated here.

| Page | Date | Event | Ruling |
|---|---|---|---|
| 150-51, 157 | Dec. 1957; July 1959 | Ball's secret work with Stevenson for Dulles on the NATO meeting; the cruise with Stevenson | out of the brief (before the span) |
| 152 | July 1965 | Ball to London with the Vice President for Stevenson's body; the memorial service, Johnson's remark | cited on `cal.1965-07-14.transition-and-staff` |
| 153-56 | 1953-58 | the Maghreb, Gaillard, de Gaulle's return; the Saranac speech | out of the brief (before the span) |
| 159 | July 1960 | the Los Angeles convention: McCarthy's speech, the demonstration for Stevenson | already in |
| 166 | Feb. 1949; July 1957 | Kennedy's vote on the trade act; his Algeria speech | out of the brief (before the span) |
| 168 | 1961-63 | Acheson to Kennedy at a long evening meeting: "The only thing to do with the issue is to decide it" | lead: no date |
| 169 | early 1961 | Battle tells Ball Rusk wondered what Ball was doing; their talks thereafter | minor: no public business, no month |
| 169 | 1961-62 | Rusk on West New Guinea: "If the burghers of Amsterdam are not prepared to send their sons ..." | lead: no date |
| 170 | Apr. 1961 | Bowles lets it be known he advised against the Bay of Pigs | already in |
| 171 | 1961 | Kennedy's letter to the ambassadors, arranged by Bowles | lead: the day |
| 171 | Oct.-Nov. 1961 | Ball shown Rusk's daily reports of the Gromyko talks | minor: a routine, nothing new |
| 172 | Nov. 25, 1961 | Rusk telephones Ball at Geneva: Under Secretary; Harriman calls | already in (cited 172 on `cal.1961-11-26`) |
| 173 | 1961 | Ball demands "equal time" with Bundy before the President | lead: no date |
| 176 | 1956 | Mollet to Ball on Suez | out of the brief (before the span) |
| 178 | 1958 | the Brighton conference; the IISS | out of the brief (before the span) |
| 180 | Jan. 20, 1961 | the inaugural address, heard from the Capitol steps | already in |
| 184 | 1961 | Fowler Hamilton named to head AID | lead: the day of the nomination |
| 184 | 1961 | Rostow's calls to Ball for more German money for the Indian and Indonesian consortiums | lead: no month |
| 188-89 | 1961 | textiles: Feldman, the Cabinet Committee on Textiles (Hodges, Wirtz, Fowler), the Director of Defense Mobilization's finding | lead: the days of the committee and the finding |
| 197 | July 1961 | Ikeda's dinner for Ball at Geihinkan; Ball's soundings of the DAC delegations on Japan in the OECD | already in (`cal.1961-07-01`, 196); the dinner minor (social) |
| 198 | 1962 | Kennedy to Ball: "don't give the committees the impression you're too well prepared"; Hodges to lead the trade bill at Mills's insistence | lead: no month |
| 198-99 | Nov. 1962 | Herter, on Ball's suggestion, Special Representative for Trade; Blumenthal his deputy | lead: the days of the appointments |
| 204-05 | 1961 | the Balance of Payments Committee under Dillon; Roosa's operations | lead: the committee's founding day |
| 221 | Dec. 1960; Mar. 16, 1961 | Ball's report to Kennedy on the OEEC; the OECD's enabling legislation passed | lead: no OECD entry found on Mar. 16, 1961 |
| 225-28 | 1958-61 | the Congo's independence, the Belgian paratroopers, the Security Council's resolutions, Hammarskjöld and Katanga, Lumumba's death | already in (each event its own entry); lead: check that each has Ball's page |
| 229 | Sept. 18, 1961 | Ball at the Bank and Fund's meeting at Vienna when Hammarskjöld's crash is announced | cited on `cal.1961-09-18.congo` |
| 259-60 | Dec. 1958; July 1959; Apr. 1962 | de Gaulle's directorate; Dulles's trip; the political union scheme founders | out of the brief (1958-59); lead: the day of April 1962 |
| 275 | early fall 1963 | Kennedy asks Ball to see Salazar and Ayub | already in (pp. 276-85 cited) |
| 286 | late July 1962 | Soviet shipping to Mariel increases | lead: check the calendar's missile crisis entries of July-August 1962 |
| 308 | Nov. 2, 1962 | Mikoyan sent to Havana | lead: check the calendar |
| 322 | Oct. 1963; July 5, Aug. 4, 1964 | the National Liberation Committee at Brazzaville; Tshombe's government; Stanleyville taken | lead: check the calendar for each |
| 322 | summer 1963 | Ball in touch with Spaak on the Congo | lead: no act dated |
| 327-29 | Dec. 1962-June 1966 | the Dominican Republic: Bosch's election and fall, the revolt of April 1965, the evacuation, the OAS committee, the election | already in (cited on Sept. 25, 1963; a Check on Dec. 20, 1962) |
| 336 | Oct. 1964 | Labour's victory | lead: check the calendar's British election entry |
| 337-38 | 1956-63 | Makarios's exile; independence; his proposals of November 1963 | out of the brief (before 1960) or lead (the day of the proposals) |
| 359 | July 1974 | the Cyprus crisis of 1974 | out of the brief (after the span) |
| 361-64 | 1954-61 | Laos and Vietnam to 1961: Phoumi at Savannakhet and on Vientiane, Kennedy's speech of June 1956 | already in, or out of the brief |
| 370 | May-Oct. 1963 | the Buddhist crisis | already in |
| 374 | July 17, 1963 | Kennedy at his press conference: "We are not going to withdraw from that effort" | lead: no entry found on the day; the Papers' item to read |
| 384 | fall 1964 | Johnson calls Ball his "devil's advocate" | lead: no month |
| 385 | May 1961 | Johnson's domino theory on his return from Vietnam | lead: check the calendar's entry of Johnson's report, May 1961, for Ball's page |
| 410-23 | 1969-75 | Nixon's war, the Paris agreements | out of the brief (after Jan. 20, 1969), but for the line of p. 414 entered (Dec. 29, 1968) |
| 413 | early 1968 | Vietnamization begun by the Johnson administration | lead: no act dated |
| 427 | Feb. 1966 | Johnson at Honolulu: "two brave leaders"; "special pleaders who counsel retreat" | lead: the Papers' item of Honolulu to cite with Ball's page |
| 428 | 1966 | Goldberg presses for moderating policies | lead: no month |
| 432 | Sept. 1966 | Ball's resignation | already in (`cal.1966-09-21`, 425) |
| 448-49 | Nov. 1968-Jan. 1969 | six weeks in France and Spain; Christmas in Florida; back to Lehman Brothers | minor: private |
| 451 | 1968 | Ball's promise to Humphrey to support him if he ran again | lead: no month |

## The press (R13)

| Date | Outlet | Kind | Items | Page |
|---|---|---|---|---|
| 1964-11-23 | Joseph Alsop's column | column | Ball's dissent; "Ball's knowledge of Asia could be comfortably contained in a fairly small thimble" | 384 |
| 1965-07 | *Life* | picture | Ball in tears at Stevenson's memorial service (Check: the issue) | 152 |

## Leads

- National: Kennedy's letter to the chiefs of mission, 1961 (Ball 171; the day); Fowler Hamilton named to AID (184); the Cabinet Committee on Textiles and the defense mobilization finding (188-89); Herter and Blumenthal named, Nov. 1962 (198-99); the Balance of Payments Committee (204-05); Kennedy's press conference of July 17, 1963 (374; the Papers); Johnson's "devil's advocate" (384); Alsop's column of Nov. 23, 1964 (384: the paper and page); Clifford's statement of Dec. 29, 1968 (414: the occasion; the daybook's Sunday programs that day have Rostow and McGovern, not Clifford); Ball's promise to Humphrey (451).
- Foreign: the OECD's ratification, Mar. 16, 1961 (221); the political union scheme, Apr. 1962 (260); Mikoyan to Havana, Nov. 2, 1962 (308); the Congo of 1963-64 (322); Makarios's proposals, Nov. 1963 (338); Johnson at Honolulu, Feb. 1966 (427); Macmillan to Eisenhower, 1960, on a "peripheral alliance" (209: the record, FRUS 1958-60).
- Sources not held: Weintal and Bartlett, *Facing the Brink* (1967), and Abel, *The Missile Crisis* (1966), cited by Ball and by Rusk's list of works (Rusk, 641), have no cards; Radvanyi, *Delusion and Reality* (1978), neither.

## Batch 6 (Nov. 10–11, 2026): the private, social and minor rows re-ruled (b6-ball-past)

The same copy fetched again from Drive (the direct download, 50 MB), printed = PDF − 18; pp. 169, 171–72, 195–97 and 448–49 read off the text, p. 196 (PDF 214) off the page image (the DAC's days, July 11–13, 1961; the text layer had "July 1"); deleted when done. Ball gives no notes for these pages: no witnesses to register. Patch `inbox/2026-11-06-b6-ball-past.yaml` (b6-ball-past: 7 entries added; patch-check 0 errors, 2 warnings, a same-day flag of distinct events, read).

| Page | Date | Row | Ruling |
|---|---|---|---|
| 169 | early 1961 | Battle tells Ball Rusk wondered what Ball was doing; their talks thereafter | entered, `cal.1961-03.transition-and-staff-2` (said in private about the Department's business; Check: the day, "my first months in the Department") |
| 171 | late summer 1961 | (on the same page, not listed before) Rusk to Ball: "Chet isn't up to it" | entered, `cal.1961-08.transition-and-staff` |
| 171 | Oct.–Nov. 1961 | Ball shown Rusk's daily reports of the Gromyko talks | entered, `cal.1961-10.berlin-and-vienna` (the Secretary's sharing of the talks with his Under Secretary for economic affairs, the informal record, not a unit's routine) |
| 197 | July 1961 | Ikeda's dinner for Ball at Geihinkan; Ball's soundings of the DAC delegations | entered, `cal.1961-07-11.japan` (a social occasion among the principals of a pending matter, Japan in the OECD and the trade problems) and the DAC's meeting itself, which the calendar did not hold, `cal.1961-07-11.foreign-aid` (the first run's "already in" pointed at the Okinawa entry, `cal.1961-07-01.japan`) |
| 448–49 | Nov. 1968–Jan. 1969 | six weeks in France and Spain; Christmas in Florida; back to Lehman Brothers | Ball to Arthur Sulzberger aboard the *France* on Nixon's election entered, `cal.1968-11-08.elections-1968-2` (Check: the day); the return to Lehman Brothers and the boards that dropped him over his attacks on Nixon entered, `cal.1969-01.transition-and-staff` (Check: whether before Jan. 20); the crossing, the six weeks in France and Spain and Christmas in Florida passed over: family and social matters with no bearing on public business or politics |

Rows not re-ruled here (out of the brief by date, the leads): as written above.

