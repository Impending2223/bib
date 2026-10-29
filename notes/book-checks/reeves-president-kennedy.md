# Richard Reeves, *President Kennedy: Profile of Power* (1993): the calendar against the book

Card `w.reeves-president-kennedy`. Read Oct. 28–29, 2026, from the copy on the Drive: the first Touchstone edition, the
paperback of 1994 ("First Touchstone Edition 1994"; copyright 1993 by Reeves-O'Neill, Inc.). The Source Notes say they
"reflect changes in the text and sources ... 1994". The pinpoints follow its pages, and the card's note now says so ("Cited
by the pages of the Touchstone paperback (1994), its notes revised through April 1994"). Offset: printed page = PDF page −
2 through PDF 322 (printed 320). The plates take PDF 323–338. From PDF 339 the printed page is PDF page − 18. Checked by the printed
folios at pp. 100, 250, 320, 321, 400, 520, 662, and in the notes at 700 and 765. Text pp. 13–662; Source Notes pp.
663–765. The notes are unnumbered. Each is keyed by the text page it serves and its catchphrase ("108 'Discussions
revolved': NYT, 4/27/61"). `sources/cited-records/reeves-president-kennedy.yaml` keys each record by that page and the
catchphrase's first words as a slug (`then-he-paused`). Several records under one note are lettered (`.a`, `.b`), as the
Caro file does. In five notes (pp. 108, 204, 316, 600, 620) the scan's text runs the catchphrase into the note before.
Those were keyed from the catchphrase as the notes print it.

Patch: `inbox/2026-10-29-book-reeves-selverstone.yaml` (book-reeves-selverstone), shared with Selverstone's reading. Where
both books bear on one entry, the entry gets one edit.

What the book is for the calendar: the presidency day by day, Jan. 1961–Nov. 22, 1963, from the daily appointments log, the
White House transcripts and tapes, the National Security Files and the oral histories at the Kennedy Library, and the
author's interviews (51 cited). It is the informal record: the meetings, calls and memoranda behind the public acts. The
FRUS volumes and the Library's tape transcripts it cites are the primary records to read first. Reeves quotes the
recordings from the Library's transcripts; none were heard for this reading.

How the list was made: every dated or datable event in the text, pp. 13–662, was taken in page order (the candidate list
in the scratch notes, about 560 items). Each was set against every calendar entry of its day, ±3 days, in a fresh dump of
the calendar (all threads; regenerated Oct. 28, 18:30, after the other runs' merges) and against the pending patches in
`inbox/`. Where the event was in, the page was added: its claim-map row, the `via` rows of the note's records, and a
parenthetical where it bears part of the entry. Where Reeves differs, a Check was added. Where the event was not in, and
the brief takes it, an entry was made from the page and its record, read in FRUS, the Public Papers or the recordings'
catalogues where they hold it. The rest is "Passed over", below. Two entries were cited for Reeves before this reading.
Jan. 20, 1961 (transition-and-staff) carried a prose cite ("begins here and runs day by day") with a matching
malformed claim row. Both were replaced by the pinpoint, 34–41, and its rows. No other prior cite existed.

## Entries held, in part, or differing (162 edited)

Reeves's page added, with its row, its records' `via` rows and To check items, and a parenthetical where it bears part:

- 1960: Dec. 6.
- 1961: Jan. 20 (two), 28, 31; Feb. 6, 22; Mar. 11, 13, 15, 23, 28, 30; Apr. 4, 7, 16, 19 (two), 20, 21, 22, 27 (two), 28;
  May 9, 14, 16, 20, 21, 24, 25, 29, 31; June 3; July 5, 7, 8, 13, 24, 30; Aug. 13, 14, 16, 19, 21, 30; Sept. 5, 29;
  Oct. 6, 11, 21, 22, 25, 27, Oct. (force levels); Nov. 2, 3, 4, 9, 13, 15, 23; Dec. 16, 21.
- 1962: Feb. 18; Mar. 22, 31; Apr. 10, 11, 12, 13; May 12, 13, 28; June 7, 11; July 17; Aug. 6, 10, 22, 31; Sept. 4, 6,
  7, 18, 27; Oct. 16, 18 (two), 20, 22, 24, 25, 26, 27, 28; Dec. 17, 18, 26, 29.
- 1963: Jan. 2, 25; Feb. 12; Mar. 14; Apr. 20, 25, 26; May 4, 10, 12, 18; June 3, 5, 10, 11 (two), 12, 18, 22, 26, 27,
  29; July 15, 25, 26, 29; Aug. 15, 20, 21, 23, 24, 26, 28 (two), 29, 31 (two); Sept. 2, 6, 9, 10, 11, 15, 17, 19, 21,
  24, 29; Oct. 2, 5, 9, 10, 11, 24, 25, 27, 28, 29 (two); Nov. 1, 13, 20.

Every edit keeps what the entry held (each cite, each sentence of `c`, each claim row). Units added to `c` (a handful,
where Reeves gives the act the entry lacked) go at the end, and the hash is recomputed. Each edit was diffed against the
entry as it stands after the other runs' merges (Oct. 28, 18:30). Nothing of another run's is lost.

Differences, each a Check on the entry:

- 1961-01-20 (civil rights the executive): Reeves has Goodwin call the Coast Guard's commandant (40).
- 1961-03-30 (Cuba): Reeves has Fulbright asked aboard on the Thursday before Easter and the memorandum handed over on Air
  Force One "the next day" (78–79).
- 1961-04-19 (Cuba): Reeves has the jets over the beach at 6:30, an hour before the B-26s (95).
- 1961-04-20 (Bay of Pigs) and 1961-04-21 (King): Reeves puts the Nixon talk the afternoon of the meeting with the
  Revolutionary Council, Apr. 19 (99), and the King visit the same day (100).
- 1961-05-09 (Bolshakov): Reeves has the meeting "two weeks before the scheduled summit" (137).
- 1961-05-16 (Ottawa): Reeves gives the trip as May 17 (120).
- 1961-07-24 (Berlin): Reeves gives the economists' case as the reason the tax increase was dropped, not foreign aid
  (197–98).
- 1961-10-27 (Checkpoint Charlie): Reeves has the Soviet tanks back off "twenty hours later," the morning of Oct. 28 (251).
- 1961-11-13 (Vietnam): Reeves gives the words as Kennedy's to Hilsman, undated (262). The entry has them to Schlesinger.
- 1962-05-13 (Laos): Reeves has McCone report Eisenhower's support on Saturday, May 12 (308).
- 1962-10-26 (missile crisis): Reeves names Fomin, the name Feklisov went by in Washington (407–08).
- 1963-06-05 (elections 1964): Reeves dates it June 6, at El Paso (508).
- 1963-06-18 (Mississippi): Reeves's note dates the first call to Mayor Thompson June 17 (502); PRDE, June 18.
- 1963-08-23 (foreign aid): Reeves has the House vote the day before Kennedy left for Hyannis Port, Aug. 22, 222 to 188
  (560).
  The entry's roll call, 224–186, is Voteview's.
- 1963-09-11 (testing): Reeves has Dirksen bring the draft of the letter after the Huntley–Brinkley interview, Sept. 9
  (593–94); entered as the new 1963-09-09.testing.
- 1963-10-10 (King): Reeves has Robert Kennedy sign the order for the wiretap on King's home on Oct. 7 (626–27).
- 1963-10-24 (Cuba): Reeves gives the talk with Jean Daniel as Nov. 19 (659).

Rulings:

- Reeves (332) has "Senator Robert Byrd, a West Virginia Democrat" walk out when Stanley Surrey, not Dillon, came
  before the Joint Committee on Internal Revenue Taxation in January 1961. The Joint Committee's Senate members in the
  87th were Harry F. Byrd (Va.), its vice chairman, Kerr, Long, Williams and Carlson (Congressional Directory, Apr. 1961,
  265; `congress/committees-cdir.yaml`). The senator is Harry F. Byrd. Not entered: the day not given, the
  note giving no record. A lead.
- Fomin is Feklisov (the Check above). The entry keeps Feklisov.
- Where Reeves quotes a tape from the Library's transcript and PRDE or the Miller Center catalogue it, the catalogue's
  page is the primary record. The quotation stays Reeves's, with "Check: the recording not heard". Where neither
  catalogues the day (Feb.–Oct. 1963 has no Miller Center copies), the Check says so.

## New entries (30)

- 1961: Jan. 26 (Heller's background briefing; the day "six days into" the presidency, a Check); Feb. 10 (ADA's officers
  with Kennedy); Apr. 28 (the Brooklyn and Bronx leaders at the Carlyle); June 6 (the congressional leaders after Vienna);
  July 19 (the NSC on Berlin, [FRUS 1961–63, XIV, doc. 77]).
- 1962: Oct. 22 (Kennedy telephones Eisenhower; the Miller Center's copy; "-5", a distinct call).
- 1963: Jan. 30 (Louis Martin's memorandum); Apr. 21 (Harriman); May 20 (the recorded meetings on the bill); May 24
  (Reedy to Johnson); June 18 (Mansfield on cloture); July 4 (the Buddhist crisis meeting, recorded); July 24 (Rusk on the
  treaty and the Senate); July 26 (Truman, "-2"); Aug. 7 (the citizens' committee for the treaty); Aug. 7 (Griffiths on
  the tax bill); Aug. 12 (Mansfield on the hearings, "-2"); Aug. 15 (Lodge's last meeting before Saigon); Aug. 19
  (Mansfield's "long haul" memorandum); Sept. 9 (Dirksen with the draft letter); Sept. 12 (the news conference, "-2");
  Sept. 30 (O'Brien on Gore and the tax bill); Oct. 21 (Sulzberger, Halberstam); Oct. 22 (Moore's motion in Judiciary);
  Oct. 23 (the leaders on the bill, PRDE); Oct. 28 (Daley on Libonati, PRDE); Oct. 29 (Halleck, PRDE; Republican Party: In
  Congress); Nov. 2 (the 9:35 meeting, [FRUS 1961–63, IV, doc. 274]); Nov. 6 (Lodge's last weekly report, FRUS IV, docs.
  302, 304); Nov. 21 (Forrestal to go to Sihanouk).

Each was compared with every entry of its day. Four share day and thread with an entry of another event and carry `-2`
or `-5` ids. The merge will flag them as possible duplicates (`./bib resolve ID --take keep`): 1962-10-22
missile-crisis-5, 1963-07-26 testing-2, 1963-08-12 testing-2, 1963-09-12 vietnam-2.

## Records

`sources/cited-records/reeves-president-kennedy.yaml`: 259 records from the notes the entries cite. By kind: memoranda
74, interviews 51 (the author's; logged, and kept out of To check), oral histories 39, press 28, transcripts 19,
telegrams 18, reports 10, files, notes, letters and recordings the rest. Published works (the published RFK oral history,
the Pentagon Papers, the Church report, *CMC*, the memoirs and studies) are not logged, as the Caro file does not log
them. 53 were found: FRUS documents, PRDE's and the Miller Center's catalogue pages. 47 of those were read and cited as
the entries' primary record. The rest stand in the entries' To check, "(cited by [[w.reeves-president-kennedy]], PAGE)".
Not found: the Library's daily appointments log and tape transcripts (by subscription, or not online), the NSF and POF
memoranda FRUS does not print, the oral histories (the Library's, not read), and the press items, whose repository the
notes do not give.

## Passed over

How the list was made: the candidate list above, every dated or datable event pp. 13–662. For each event not entered, the
entries of its day (±3 days) were read in the calendar dump. "Already in as" names the entry that has it. Some were not
cited here: the page adds nothing the entry lacks, or the entry is another thread's and stands. "Minor" means only what
the brief's rule says: a repetition, private or social trivia, or an operation below the calendar's level. Nothing of a
member's or party figure's dated word is "minor": the few left are "lead". Page | date | event | why.

| page | date | event | why |
|---|---|---|---|
| 25 | 1960-12-08 | Kennedy meets McNamara; McNamara's letter of conditions a week later | lead: the first meeting and the letter not entered; McNamara's appointment is in, cal.1960-12-13.transition-and-staff-cabinet |
| 26 | 1960-12 | Rusk called to Palm Beach; the leak; the Stevenson call with Rusk present | already in as cal.1960-12-08 and 12-09.transition-and-staff; the leak and the call minor |
| 27 | 1960-12 | Heller to the CEA; Dillon calls Eisenhower; Gore objects to Surrey | Dillon in as cal.1960-12-16.robert-kennedy; Gore's objection: lead (undated in the book) |
| 29 | 1960-12-15 | Kennedy tells his brother at breakfast he will be Attorney General | already in as cal.1960-12-16.robert-kennedy (the naming); the breakfast minor |
| 29–33 | 1961-01-19 | Eisenhower–Kennedy, then the secretaries in the Cabinet Room; Clifford's notes | already in as cal.1961-01-19.laos |
| 39 | 1961-01-19 | Wofford: "at home" added to the inaugural draft | lead: the draft (Sorensen papers) |
| 40–41 | 1961-01-21? | Khrushchev's speech of Jan. 6 sent round the NSC, "Read, mark, learn" | the speech in as cal.1961-01-06.berlin-and-vienna; the memorandum undated, minor |
| 51 | 1961 | Rusk blocks Lansdale's ambassadorship; Nolting chosen | undated |
| 52 | 1961 | Wheeler on NSAM 22 | undated |
| 55–56 | 1961-01 | Rayburn breakfast: votes lacking on Rules; the balanced-budget statement O'Brien's price | lead: the day (the appointments log); the Rules fight is in, cal.1961-01-31.rules (cited) |
| 56 | 1961-01-29 | Heller's on-record briefing | already in as cal.1961-01-29.economy and the new 1961-01-26.economy |
| 59–61 | 1961-02-07 | Hesburgh with Kennedy; Wofford sworn in | lead: the Hesburgh meeting, by the appointments log |
| 61 | 1961-02-08 | Press conference: the New Orleans schools | lead: the press conference, 1961 Pub. Papers (not entered for this answer) |
| 68 | 1961-02-24 | Bundy's nineteen tasks approved | minor (staff operation) |
| 69 | 1961-03-01 | cable to Saigon on the Counter-Insurgency Plan; the Peace Corps order | the order already in as cal.1961-03-01.peace-corps; the cable: lead (FRUS 1961–63, I) |
| 74–75 | 1961-03 | Brown's talk; the Lippmann lunch; the Seventh Fleet; Rostow's backgrounder | already in as cal.1961-03-20, 03-21, 03-23.laos (Mar. 23 cited) |
| 76–78 | 1961-03-29 | Acheson in the Rose Garden on Cuba; his Berlin memorandum; the defense message | lead: Acheson's talk (his oral history); the defense message of Mar. 28: lead (Pub. Papers) |
| 82–83 | 1961-04-05 | Schlesinger's memorandum; Robert Kennedy: keep mouths shut | already in as cal.1961-04-05.cuba and cal.1961-04-11.cuba |
| 83 | 1961-04-01 | Schlesinger and Handleman; the *New Republic*'s piece killed; Szulc and Dryfoos | lead: the press's holding back (Apr. 6–7), Schlesinger's memorandum |
| 84 | 1961-04-05 | Bundy's "Crisis Commanders" memorandum | minor (staff paper) |
| 85 | 1961-04-05 | Kennedy with Dulles, Rusk, McNamara; Apr. 8, Bissell told to schedule | already in as cal.1961-04-04.cuba and 04-07.cuba-2 (cited) |
| 85–86 | 1961-04-12 | Gagarin; "catch them" to Johnson; press conference | already in as cal.1961-04-12.space and 04-12.cuba |
| 89–95 | 1961-04-14/19 | the landing; the strike cancelled; the midnight meeting; Berle and Schlesinger to Opa-Locka | already in as cal.1961-04-14 to 04-19.cuba (Apr. 16, 19 cited) |
| 103 | 1961-04 | Kennedy tells Dulles and Bissell they must go | lead: the day (undated in the book; Dulles left Nov. 29) |
| 105 | 1961-05-05 | NSC Record of Action on Cuba; Sarit and Diệm reassured | already in as cal.1961-05-05.cuba |
| 105 | 1961-04/05 | Rusk–Mikoyan talk | undated |
| 111–112 | 1961-04 | Lemnitzer at the airport; "troops in Laos now" to Sorensen | minor (remarks), undated |
| 113 | 1961-05 | McNamara, "eliminate Castro," at the task force | lead: the day (Goodwin's account) |
| 113–114 | 1961-05 | Bundy's offer to resign; his management memorandum | minor (staff) |
| 115 | 1961-04 | Mansfield's memorandum on Laos | lead: the memorandum's day (POF); a member's word, never minor |
| 115–116 | 1961-05 | Harriman to Nehru; Geneva | already in as cal.1961-05-16.laos |
| 116 | 1961-04-29 | NSC on the Vietnam program | already in as cal.1961-04-29.laos and cal.1961-05-11.vietnam (cited) |
| 117–118 | 1961-05-05 | NSC on British Guiana; Shepard; Johnson asked to go | Shepard in as cal.1961-05-05.space; British Guiana: lead (FRUS 1961–63, XII) |
| 119–120 | 1961-05-09 | Johnson leaves with the letter to Diệm; the reply seen May 16 | already in as cal.1961-05-12.vietnam |
| 120 | 1961-05-17 | Ottawa: Diefenbaker urged on nuclear stationing | already in as cal.1961-05-17.europe-and-the-alliance and 05-16.transition-and-staff (cited, Check) |
| 120–121 | 1961-05-23 | Johnson's report; Krock's drink and talk; White on Mao | Johnson's report in as cal.1961-05-23.vietnam-johnson-asia; the Krock talk minor (repetition) |
| 125 | 1961-05 | McNamara's Berlin planning memorandum; 500 more troops | lead: the memorandum (FRUS 1961–63, XIV) |
| 131–132 | 1961-05-19 | Peace Corps advisory council: Belafonte, Eugene Rostow urge a statement | minor (social; below the level) |
| 133 | 1961-05 | Prescott Bush's antisegregation amendment to school aid fails, 61–25 | lead: the roll call (Voteview, Cong. Rec.); a member's act, never minor |
| 133 | 1961-05 | Robert Kennedy on NBC; May 24 the cooling-off statement | already in as cal.1961-05-24.freedom-rides (cited) |
| 137–138 | 1961-05 | Robert Kennedy and Bolshakov, through Holeman | already in as cal.1961-05-09.berlin-and-vienna (cited, Check) |
| 139 | 1961-03-22 | Kennedy to Webb: no new Apollo funds | lead: the meeting (NASA's records) |
| 139 | 1961-05-06 | Bourguiba dinner, the moon question | minor (social) |
| 140–142 | 1961-01-12/05-30 | Trujillo: the arms, Rusk's memoranda, the cable to Dearborn | already in as cal.1961-05-29 and 05-30.latin-america (May 29 cited); the earlier steps: lead (Church report) |
| 143–144 | 1961-05-30 | Ben-Gurion at the Waldorf | already in as cal.1961-05-30.middle-east |
| 152–153 | 1961-06-01 | Harriman at the embassy, "Get us out" | minor (remark) |
| 172–173 | 1961-06-04 | Reston at the embassy, "worst thing in my life" | lead: a journalist's interview that made news only later; Reston's memoir |
| 173 | 1961-06-05 | to London; Radziwill christening; Alsop | minor (social) |
| 174 | 1961-06-05 | Macmillan at Admiralty House | already in as cal.1961-06-05.berlin-and-vienna |
| 178 | 1961-06-08 | Salinger discloses the back injury | out of the brief (health) |
| 178–179 | 1961-06-10 | the Soviet aides-mémoire released | lead: the release (*Bulletin*) |
| 180 | 1961-05 | Rockefeller to Kennedy on civil defense | lead: Rockefeller's letter (POF); a governor's word, never minor |
| 180 | 1961-06 | memorandum to Bundy on a civil-defense plan | minor (staff) |
| 180–181 | 1961-06-13 | Taylor's report | already in as cal.1961-06-13.cuba |
| 181 | 1961-06-15 | Khrushchev on television; Acheson asked for a plan | already in as cal.1961-06-15.berlin-and-vienna |
| 181 | 1961-06-22 | fever; Ikeda | Ikeda in as cal.1961-06-20.transition-and-staff; the fever out of the brief |
| 182–183 | 1961-06-19 | LeMay named Air Force Chief | lead: the announcement (Pub. Papers or the press) |
| 183–184 | 1961-06-29 | the letter to Diệm (200,000); Fulbright, Mansfield and Humphrey read Acheson's report | lead: the meeting with the senators (FRUS 1961–63, XIV) |
| 189 | 1961-06-29 | memoranda to Dutton on Negro unemployment | minor (staff) |
| 189 | 1961-06/07 | *Newsweek*'s JCS leak; Hoover's agents to the Pentagon | lead: the story's day |
| 194–195 | 1961-07-17 | Sorensen's and Schlesinger's memoranda on Berlin | already in as cal.1961-07-13 and 07-24.berlin-and-vienna (cited) |
| 197–198 | 1961-07-21/24 | the Berlin surtax killed | already in as cal.1961-07-24.berlin-and-vienna (cited, Check) |
| 198 | 1961-07 | Rusk to Dowling; July 24 to Macmillan | minor (cables of an event in) |
| 199 | 1961-07-25 | the Berlin address | already in as cal.1961-07-25.berlin-and-vienna |
| 203–205 | 1961-07-26/31 | McCloy with Khrushchev; McCloy reports | lead: McCloy's cable (FRUS 1961–63, XIV) |
| 205–206 | 1961-08-07/10 | Khrushchev on television; the press conference on refugees | lead: Khrushchev's speech of Aug. 7 |
| 207–208 | 1961-08 | Rostow, "Perhaps a wall" | minor (remark), undated |
| 213 | 1961-08-15 | Dulles's report; cables | already in as cal.1961-08-14 and 08-16.berlin-and-vienna (cited) |
| 214 | 1961-08-17/18 | Clay and Johnson to Berlin; the battle group ordered | already in as cal.1961-08-19.berlin-and-vienna (cited) |
| 220 | 1961-06/07 | the Staley mission; Steeves's paper | already in as cal.1961-06.vietnam |
| 220–221 | 1961-07-28 | Southeast Asia meeting: three strategies | lead: FRUS 1961–63, I |
| 221 | 1961-08-11 | Staley's recommendations endorsed | already in as cal.1961-06.vietnam (approved in August) |
| 221 | 1961-08-29 | Southeast Asia meeting: the Meo, the trainers | lead: FRUS 1961–63, I and XXIV |
| 221 | 1961-08-31 | note to McNamara on the forces | minor (staff) |
| 222–223 | 1961-08 | Taylor's "Guidance for Berlin Contingency Planning" | lead: the paper's day (FRUS 1961–63, XIV) |
| 224 | 1961-08 | letter to Macmillan on testing | lead: the letter (FRUS 1961–63, VII) |
| 225 | 1961-09-02 | Reston at Hyannis Port | minor (repetition) |
| 227–228 | 1961-09-12 | Sukarno and Keita | already in as cal.1961-09-12.africa |
| 228 | 1961-09-15 | the first underground test | already in as cal.1961-09-15.testing |
| 229–230 | 1961-09-13/14 | Lemnitzer's SIOP-62 briefing | lead: FRUS 1961–63, VIII |
| 229 | 1961-09 | McNamara's backgrounder: American superiority | minor (repetition of the Gilpatric speech) |
| 231 | 1961 | Adzhubei and Gagarin at the White House | lead: the days |
| 232 | 1961-09-18 | Norstad; *Life*'s fallout issue; letters to the governors | lead: the letter to the governors (Pub. Papers) |
| 234 | 1961-09-22 | Salinger, Bolshakov and Kharlamov at the Carlyle | lead: Salinger's memoir |
| 235 | 1961-09-25 | the UN address | already in as cal.1961-09-25.testing |
| 240–241 | 1961-10-09/11 | the Chiefs; Farm Gate; the Taylor mission | already in as cal.1961-10-11.vietnam (cited) |
| 243–244 | 1961-09 | Kraus; the gymnasium | out of the brief (health) |
| 253–255 | 1961-10-17/11-01 | the Taylor mission's cables | already in as cal.1961-10-18.vietnam and 11-03.vietnam (cited) |
| 257 | 1961-11-07 | Ball: 300,000 men | lead: the day; Ball's memoir |
| 257 | 1961-11 | Eisenhower's speeches on Cuba and Vietnam | lead: the days (the press); a party figure's word, never minor |
| 257–258 | 1961-11-08 | press conference; Mae Craig | lead: 1961 Pub. Papers |
| 258–259 | 1961-11-11 | the Rusk–McNamara paper; Harriman; Rostow | already in as cal.1961-11-11.vietnam (cited) |
| 260–261 | 1961-11-21 | Galbraith's cable; Rostow, Nov. 24 | lead: FRUS 1961–63, I |
| 261 | 1961-12 | Rusk to the NATO ministers | minor (remark) |
| 262 | 1961-12-15 | the published letters; the helicopter companies; Davis killed Dec. 22 | already in as cal.1961-12-15.vietnam; Davis's death: lead |
| 264–265 | 1961-11-08/09 | Szulc with Robert Kennedy and the President | already in as cal.1961-11-08 and 11-09.cuba (Nov. 9 cited) |
| 265–266 | 1961-10-05 | NSAM 100; the CIA's paper on Cuba | lead: FRUS 1961–63, X |
| 266 | 1961-11-16/19 | Seattle; Rayburn's funeral; Los Angeles; the carriers off Santo Domingo | already in as cal.1961-11-16.congress, 11-16.right-and-the-military, 11-19.latin-america |
| 267 | 1961-11-30 | Mongoose; Lansdale | already in as cal.1961-11-30.cuba |
| 268–269 | 1961-12 | police academies; Frondizi at Palm Beach | lead: Frondizi's visit, Dec. 24 (the *Bulletin*) |
| 270 | 1961-11-22 | the Civil Rights Commission on the housing order; "stroke of the pen" | already in as cal.1961-11-23.civil-rights-the-executive (cited) |
| 270–271 | 1961-11/12 | Sorensen and Lee White's options; the National Guard | minor (staff) |
| 271 | 1961-10/11 | Dealey at the publishers' lunch | lead: the day (the press) |
| 271–272 | 1961-11/12 | the fallout pamphlet | already in as cal.1961-11-24.defense |
| 272–273 | 1961-12-19/22 | Joseph Kennedy's stroke; Bermuda | already in as cal.1961-12-19.transition-and-staff and 12-21.europe-and-the-alliance (cited) |
| 275–277 | 1962-01-11/18 | State of the Union; the meetings with Democratic members | the address in as cal.1962-01-11.program; the meetings: lead (the appointments log) |
| 278 | 1961-12? | the historians; David Donald | minor (social) |
| 280 | 1962-01-15 | press conference, "No" | already in as cal.1962-01-15.vietnam |
| 281 | 1962-01-18 | NSAM 124; Hilsman to Vietnam | already in as cal.1962-01-18.defense |
| 282 | 1962-01-21 | Bình Hòa; "How can things like this go on" | lead: the operation (FRUS 1961–63, II) |
| 282 | 1962-01 | Mecklin; press policy | lead: the cable (FRUS 1961–63, II) |
| 283 | 1962-01-03 | defoliation approved; the first sorties | already in as cal.1962-01-03.vietnam (Selverstone) |
| 283 | 1962-02 | MACV, Harkins | already in as cal.1962-02-08.vietnam |
| 286 | 1962-02-20 | Glenn; the congressional leaders at 9 a.m. | Glenn in as cal.1962-02-20.space; the leaders' breakfast minor (weekly) |
| 288–290 | 1962-02-27/03-22 | Hoover's memorandum; the lunch; Campbell | already in as cal.1962-02-27 and 03-22.transition-and-staff (Mar. 22 cited) |
| 292 | 1962-04/05 | the CIA on Giancana; Houston briefs Robert Kennedy | already in as cal.1962-05-07.robert-kennedy |
| 303–304 | 1962-04-30 | the Chamber of Commerce speech; the *Herald Tribune* cancelled | lead: the speech (Pub. Papers); the cancellation, the press |
| 304 | 1962 | the taping system installed | lead: the date (the Library's account; PRDE) |
| 306 | 1962-04 | Burke to the DAR | lead: the day (the press) |
| 307 | 1962-05-05/10 | Nam Tha; the press conference; the Seventh Fleet | already in as cal.1962-05-06 and 05-12.laos (May 12 cited) |
| 309 | 1962-05-14/15 | troops to the Thai border | already in as cal.1962-05-15.laos |
| 310 | 1962-05-22 | Robert Kennedy and Bolshakov on Laos | already in as cal.1962-05.laos |
| 311 | 1962 | Galbraith, "losing horse"; Harriman | undated |
| 311 | 1962-05-15/17 | de Gaulle's press conference; Kennedy on testing | lead: the press conference, 1962 Pub. Papers |
| 312 | 1962-06-06 | West Point | already in as cal.1962-06-06.defense |
| 314–315 | 1962-05-19 | the Madison Square Garden gala | lead: the Democrats' gala, the press; a party's doing, never minor |
| 316 | 1962-05 | Haddad to the editors | out of the brief (private) |
| 323–325 | 1962-06-08 | the Massachusetts convention for Edward Kennedy; the *Globe* | lead: the convention (State party; the press) |
| 326 | 1962-06-27 | press conference: school prayer; the coalition since 1938 | lead: 1962 Pub. Papers |
| 327 | 1962-07-05 | press conference: the housing order | lead: 1962 Pub. Papers |
| 328–329 | 1962-07-23 | press conference by Telstar; the dollar | lead: 1962 Pub. Papers |
| 330–331 | 1962-07-12/08-01 | Sorensen's tax memorandum; the press conference | lead: the memorandum (Sorensen papers) |
| 333–334 | 1962-08-09 | Greenewalt; Heller's "Range of Tax Cut Choices" | lead: Heller's memorandum (the Library) |
| 334–335 | 1962-08-13 | the television address | already in as cal.1962-08-13.economy |
| 342–343 | 1962-08-20/23 | Plan B-plus; NSAM 181 | already in as cal.1962-08-10.cuba (cited) and 08-22.missile-crisis (cited) |
| 343–344 | 1962-08-27/29 | Capehart: invade; the press conference | Goldberg in as cal.1962-08-28.court; Capehart's speech: lead (the press; a member's word, never minor) |
| 344–345 | 1962-08-29/31 | the U-2's photographs; Keating; "Those CIA bastards" | already in as cal.1962-08-29 and 08-31.missile-crisis (Aug. 31 cited) |
| 346–347 | 1962-09 | Bolshakov in the Oval Office | already in as cal.1962-09-06.soviet-union (cited) |
| 348 | 1962-09 | Newport; Bradlee | out of the brief (private) |
| 351 | 1962-09-09 | Frost at Idlewild | already in as cal.1962-09-07.soviet-union (cited) |
| 352 | 1962-09-13 | Bundy's memorandum; press conference; the reserves | already in as cal.1962-09-13.missile-crisis |
| 353 | 1962-09-17 | Griffiths's letter: no civil rights before the election | lead: the letter (the Library); a member's word, never minor |
| 354 | 1962-09-19 | SNIE 85-3-62 | already in as cal.1962-09-19.missile-crisis |
| 354–355 | 1962-09-22 | the Emancipation centennial recording | lead: the recording (Pub. Papers) |
| 355–359 | 1962-09-25/29 | Ole Miss; the calls to Barnett | already in as cal.1962-09-25.mississippi-ole-miss and following, cal.1962-09-27.mississippi (cited) |
| 357 | 1962 | Hannah and Bernhard; Louis Martin | undated |
| 364–365 | 1962-10-03/04 | Harris's polls; the blockade's preparation; McNamara on the SA-2s | lead: Harris's memorandum (the Library) |
| 365–366 | 1962-10-04/07 | Robert Kennedy and Bolshakov; Bartlett and Bolshakov | lead: the days (Fursenko and Naftali) |
| 367 | 1962-10-08/10 | McNamara's contingencies; Keating, Oct. 10 | lead: Keating's speech (Cong. Rec.; a member's word, never minor) |
| 367 | 1962-10-12 | Reston's column, from Bundy | minor (a column without an act) |
| 368 | 1962-10-14 | Indianapolis, for Bayh against Capehart | lead: the speech (Pub. Papers) |
| 377–378 | 1962-10-17 | McCone; Acheson; Waterbury with Ribicoff | already in as cal.1962-10-16 and 10-18.missile-crisis (cited) |
| 384–387 | 1962-10-19/20 | the Chiefs; Cleveland; Chicago and Daley's captains | already in as cal.1962-10-19.missile-crisis-2 and 10-20.missile-crisis (cited) |
| 427–428 | 1962-10-29 | Schlesinger's notes; the NSC | lead: the NSC of Oct. 29 (FRUS 1961–63, XI); the settlement in as cal.1962-10-28.missile-crisis (cited) |
| 429–432 | 1962-11-06 | the elections | already in as cal.1962-11-06.elections-1962 |
| 432 | 1962-11-20 | the housing order | already in as cal.1962-11-20.civil-rights-the-executive |
| 433–435 | 1962-11-10 | Mrs. Roosevelt's funeral; Gore against the tax cut | lead: Gore's word (Gore's papers; the press) |
| 435 | 1962-11 | Sorensen on the Rockefeller Foundation; Gilpatric on Rockefeller | lead: a party figure (Rockefeller), never minor |
| 436–438 | 1962-12-16 | "After Two Years," the television conversation | already in as cal.1962-12-17.press-and-broadcasting (cited) |
| 438–440 | 1962-12-16/21 | Nassau | already in as cal.1962-12-18.europe-and-the-alliance (cited) and 12-19.testing |
| 439–440 | 1962-11 | Cousins briefed; Cousins and Khrushchev | lead: the days (Cousins's book) |
| 443–444 | 1962-12 | the year-end estimate; Hilsman's appraisal | already in as cal.1962-12-26.vietnam (cited) |
| 444 | 1962-12-12 | press conference: Vietnam | lead: 1962 Pub. Papers |
| 447–449 | 1963-01 | Hilsman and Forrestal, the annex; Kaysen on Yemen | already in as cal.1963-01-25.vietnam (cited) |
| 449–450 | 1963-02/03 | McAndrew's sister's letter; the reply | lead: the letter (Pub. Papers?) |
| 450 | 1963-01 | Rusk in executive session; Thompson's suggestion of 1,000 out | lead: the session (Foreign Relations, Executive Sessions) |
| 451–454 | 1963-01-14 | State of the Union; de Gaulle | already in as cal.1963-01-14.program and 01-14.europe-and-the-alliance |
| 454 | 1963 | Pell; Eisenhower, "fiscal recklessness"; Truman | undated; Eisenhower's word: lead (a party figure, never minor) |
| 454–455 | 1963-01-22 | the NSC on de Gaulle | already in as cal.1963-01-22.europe-and-the-alliance |
| 455 | 1963-01-29 | Frost dies; the statement | minor (a statement on a death) |
| 455–457 | 1963-01-24 | press conference: MFN, the Jupiters | lead: 1963 Pub. Papers |
| 457–458 | 1963-01 | the budget; Eisenhower's *Post* article | the budget in as cal.1963-01-17.economy; Eisenhower's article: lead (a party figure, never minor) |
| 459 | 1963-01-24 | the tax message | already in as cal.1963-01-24.economy |
| 460 | 1963 | Mills to Kennedy | undated |
| 461 | 1963-01-18? | the DNC's meeting and gala; Kennedy on Michigan and Pennsylvania | lead: the day (the press); a party's doing, never minor |
| 462 | 1963-01-28/31 | "Questions to be settled"; Louis Martin's memorandum | Martin in as the new cal.1963-01-30.civil-rights-the-executive |
| 465–466 | 1963-03 | press conference on the judges; Katzenbach | lead: 1963 Pub. Papers |
| 467 | 1963 | Ervin's bill to cut Bernhard's pay | lead: the bill (Cong. Rec.); a member's act |
| 468 | 1963-02-28 | the voting message; Humphrey asked to stop talking | the message in as cal.1963-02-28.voting-rights; Humphrey: minor (remark) |
| 469–470 | 1963-04 | the Commission's Mississippi report; the backgrounder | already in as cal.1963-04-19.mississippi |
| 471–472 | 1963-02 | the fifty-mile hikes | out of the brief |
| 472 | 1963-03-06/21 | press conferences | already in as cal.1963-03-06.economy and 03-21.cuba |
| 473 | 1963-04 | the Standing Group on Cuba | lead: FRUS 1961–63, XI |
| 476–477 | 1963-04 | Cousins with Kennedy on the test ban | lead: the day (Cousins) |
| 476 | 1963-04-09 | Churchill's citizenship | lead: the proclamation (Pub. Papers) |
| 480 | 1963-04 | Mansfield: withdraw some advisers | lead: the day; a member's word, never minor |
| 482–483 | 1963-04-17 | NIE 53-63; Thompson, Apr. 4 | Thompson in as cal.1963-04-04.vietnam-force-levels (Selverstone); the NIE: lead (FRUS 1961–63, III) |
| 484 | 1963-04-24 | press conference; the last Jupiter; Bartlett | the Jupiter in as cal.1963-04-25.europe-and-the-alliance-jupiters (cited); the press conference: lead |
| 485–490 | 1963-05-02/10 | Birmingham; ADA's officers; Eugene Rostow to Blough | already in as cal.1963-05-04.alabama-birmingham and 05-10.alabama (cited) |
| 490–491 | 1963-05-08 | press conference; Griswold | the press conference in as cal.1963-05-08.middle-east; Griswold: lead |
| 491 | 1963-05-09 | the cable after Huế | minor (a cable of an event in) |
| 492 | 1963 | the Gridiron; Philadelphia for Tate | undated |
| 492 | 1963-05 | the bail fund | already in as cal.1963-05-09.alabama-birmingham |
| 496 | 1963-05-22 | press conference: withdrawal | already in as cal.1963-05-22.vietnam-force-levels (Selverstone) |
| 497–499 | 1963-05 | Baldwin; Connor out; Allgood and Tuttle | Baldwin in as cal.1963-05-24.civil-rights-the-executive; the court rulings in as cal.1963-05-23.alabama-birmingham |
| 499–500 | 1963-05 | Ellender; Reedy's memorandum | Reedy in as the new cal.1963-05-24.civil-rights-bill; Ellender: lead |
| 500 | 1963-05 | Air Force guidance on airmen | minor (below the level) |
| 501 | 1963-05-28 | the Jackson Woolworth sit-in | already in as cal.1963-05-28.mississippi |
| 502–503 | 1963-06 | the calls to Mayor Thompson and Governor Jimmie Davis | Thompson in as cal.1963-06-18.mississippi (cited, Check); the Davis call of June 3: lead (PRDE) |
| 509–513 | 1963-06-08/10 | the American University drafts; Cousins | already in as cal.1963-06-10.testing (cited) |
| 528 | 1963-06-19 | the message; Evers buried; Wallace | already in as cal.1963-06-19.civil-rights-bill |
| 528–529 | 1963-06-19 | Rusk–McNamara on Vietnam; NSAM 249 | lead: NSAM 249 (FRUS 1961–63, XXIV) |
| 529 | 1963-06-21 | the East Room meetings; the march announced | already in as cal.1963-06-22.civil-rights-bill (cited) |
| 533–540 | 1963-06-23/07-02 | Europe: Bonn, Berlin, Ireland, Birch Grove, Rome | already in as cal.1963-06-23 to 06-29 (June 26, 29 cited) |
| 540–541 | 1963-07-01/04 | the cable on the bonzes; Khrushchev in East Berlin | the July 4 meeting is the new cal.1963-07-04.vietnam; Khrushchev's speech: lead |
| 541–542 | 1963-07-10 | SNIE on Diệm; Bowles | lead: FRUS 1961–63, III |
| 542–544 | 1963-07-17 | press conference; the RNC's resolution | already in as cal.1963-07-17.civil-rights-bill (cited); the RNC: lead (a party's word, never minor) |
| 543 | 1963-07-09? | Harriman asks the Cuban operations suspended | lead: FRUS 1961–63, XI |
| 545–549 | 1963-07-14/26 | Harriman in Moscow; the initialing | already in as cal.1963-07-15 and 07-25.testing (cited) |
| 552 | 1963-08-05/09 | the signing; Rusk at Gagra | already in as cal.1963-08-05.testing |
| 555 | 1963-08 | Teller; Fulbright's call; McNamara | already in as cal.1963-08-20.testing (cited) |
| 558–559 | 1963-08-22 | Lodge arrives; the House cuts aid | already in as cal.1963-08-23.foreign-aid (cited, Check) |
| 560 | 1963-08 | the Ministers' Vietnam Committee | lead: the day (the *Times*) |
| 602 | 1963-09 | Sullivan on the McNamara–Taylor mission | minor (staff) |
| 608 | 1963-09-26 | Lodge brings Honey to McNamara | minor (an operation below the level) |
| 610–611 | 1963-09/10 | McNamara with Vice President Thơ; Sullivan's troop paragraph | already in as cal.1963-10-02.vietnam (cited) |
| 519 | 1963-06 | the message for Thơ, Trueheart | lead: FRUS 1961–63, III |
| 625 | 1963-10 | Kennedy to Symington on the tax bill | lead: the day; a member, never minor |
| 631–634 | 1963-10-16/25 | Tito's visit; the attempt at the Waldorf | lead: no thread fits (Yugoslavia); FRUS 1961–63, XVI |
| 633 | 1963-10 | Goldwater, "We are dining with our enemy" | lead: the day (the press); a member's word, never minor |
| 661 | 1963-11-22 | the advertisement in the *Dallas Morning News* | lead: check against the assassination entries |
| — | 1963-04-05 | a meeting dated by the schedule | lead: the appointments log |
| — | 1963-06-10/11 | the June 10 meeting; Dirksen and Halleck, June 11; the Mansfield–Dirksen agreement | the bill in as cal.1963-06-11 and 06-22.civil-rights-bill (cited); the leaders' doings: lead |
| — | 1962 | Capehart; Van Zandt; the governors, Oct. 27; Gore, Nov. 10 | Capehart and Gore above; Van Zandt (404) and the governors: lead (members' words, never minor) |
| — | 1962–63 | Rockefeller's Lincoln Day speech; Eisenhower's *Post* article | lead (party figures' words, never minor) |
| 332 | 1961-01 | Surrey before the Joint Committee; Byrd and Mills walk out | lead (the day; Harry F. Byrd, not Robert: see Rulings) |

## Leads

Written into `notes/leads.md`, National, with the pages above: Prescott Bush's amendment to school aid (May 1961, 133);
Capehart, Keating and Van Zandt on Cuba before Oct. 1962 (343–44, 367, 404); Griffiths's letter of Sept. 17, 1962 (353);
Eisenhower's attacks on the administration's fiscal record and space program, 1963 (454, 457–58); the DNC's galas of May
19, 1962 and Jan. 1963 (314–15, 461); Goldwater on Tito and Madame Nhu, Oct. 1963 (633); Tito's visit, Oct. 1963
(631–34, no thread); the taping system's installation (304); the appointments log as the source for the many meetings
dated only by it.
