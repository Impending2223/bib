# Hand-off, Nov. 10, 2026 (evening): where the work stands

For a fresh orchestrating session. Read CLAUDE.md (the core), then this. The owner's standing rules: working hours (CLAUDE.md); ask before deleting anything of theirs; never change a Drive file's sharing; no model ids in commits.

## The new way of working (the owner, Nov. 10, 2026: "I approve both")
- CLAUDE.md is the core; topics in `notes/guide/`. Row readers work from `notes/briefs/reader-card.md`.
- Models: readers on Sonnet with the card; mechanical work (merging, duplicate flags, scripts) on Sonnet or Haiku; Opus audits a sample of each reader's rulings and every disagreement. At most 4-6 agents at once (the machine has 4 processors).
- Pilot first: `inbox/2026-11-10-pilot-humphrey.yaml` (Sonnet, the card) is to be audited row by row before anything scales.

## The inbox (not merged)
- 63 batch-6 patches (`inbox/2026-11-06-b6-*.yaml`) and 28 batch-7 (`inbox/2026-11-10-b7-*.yaml`), their witnesses in `inbox/witnesses/` by the same names; `inbox/2026-11-10-presidium-records.yaml`; `inbox/2026-11-10-sit-ins-feb-1960.yaml` (witnesses `inbox/witnesses/2026-11-10-sit-ins.yaml`).
- Order: clifford-counsel is in; then caro-passage, then a one-op patch `also: {id: cal.1963-11-26.succession-3, add: [white-house]}`.
- After the sit-ins patch lands: strike the two old Checks on cal.1960-02-08.sit-ins ("Check: the dates of the cities." and Branch's long Check) that its split settles.
- Held for the owner: `inbox/2026-11-05-bundle-splits.yaml`, `inbox/2026-11-05-press-part-iii.yaml`.
- Merge one run at a time (no lock), two or three patches a run, commit and push after each; read each duplicate flag's `c` beside its neighbours (keep, or combine). Readers' broken witness files block every merge: the reader fixes its own.

## Unfinished work
- Batch 6 (`notes/briefs/batch6.md`): group 14 (young-easy-burden, reeves, dallek, mcnamara, kotz, cq-08-09, peirce-great-plains) stopped mid-work; its Reeves witness file had bad values.
- Batch 7 (`notes/briefs/batch7.md`; the rows: `python3 -I tools/works/alreadyin_rows.py OUT.json`, those not `cited`): done for Westmoreland, McPherson, Zelizer, Branch (Parting); stopped mid-work for the rest.
- To redo with the card: the rows still passed over as private, social or personal, where the page puts the press, cameras, a crowd or a principal's staff in the scene (the owner's example: Humphrey's ride at the Ranch, pp. 307-08).
- Poll hours and daylight time registers (`sources/poll-hours.yaml`, `sources/daylight-time.yaml`; memo `notes/extensions/memos/poll-hours.md`): partial.
- To apply once the inbox is merged: `python3 -I tools/works/newspaper_cites.py --write` (dry run checked: 1,388 notes).
- Newspapers and elections: bands added (dayorder KINDS_PLACE); not yet applied to entries.
- Church Committee reports: all open at aarclibrary.org/publib/church/reports/; Pike hearings to be procured by the owner.

## For the owner (their rulings wanted)
## Round 4 items (for the owner)
1965:
- dup? cal.1965-02-26.vietnam and cal.1965-02-26.vietnam-3 (same meeting, Ball's account?)
- bundle: cal.1965-12-17.vietnam (Dec. 17-21) holds meetings of Dec. 18 and 21 that have entries of their own (12-18.vietnam-pause, 12-21.vietnam-pause)
- dup? cal.1965-08-03.voting-rights (Aug. 3-4, Senate 79-18 of Aug. 4) and cal.1965-08-04.voting-rights (final passage)
From round 3:
- 1962: cal.1962-10-23.foreign-aid (Congress completes appropriation ten days after sine die: the signing?); cal.1962-10-30.testing ("Geneva" but Kuznetsov in New York)
- 1963: 03-25.transportation misdated (Papers: Mar. 23); 10-03.defense misdated (House vote Oct. 8) - Checks added
- 1965: 12-17.vietnam-3/-4 (Westmoreland at Honolulu, Lodge's answer from Saigon: answer before message in their zones)
- 1966: 07-01.vietnam-congress-2 (Senate in recess; June 30?)
- 1968: 03-06.defense-clifford ("first Monday staff meeting" on a Wednesday)
- 1960-61 reviewer wrote three exact times earlier rounds had refused: 1961-01-25 (6 p.m. news conference), 1961-06-06 (7 p.m. report on Vienna), 1961-04-19.cuba-2 (2:32 p.m.)
- 1964 reviewer wrote 58 exact times beyond ranges (51 Miller Center recordings, 6 Papers notes, 1 Berkeley)
1966:
- dup? 12-21.democratic-party and 12-21.elections-1966 (the governors at the Ranch)
- dup? 08-04.war-opposition and 08-04.vietnam-support (McPherson's Rhode Island memo)
- dup? 01-28.conservation and 07-01.conservation (identical text and source, two dates)
- dup? 07-18.civil-disorders and 07-19.civil-disorders (Humphrey at New Orleans)
- overlaps: span 02-17.vietnam-hearings holds Rusk's Feb. 18 (own entry 02-18.vietnam-hearings); span 05-29.vietnam-struggle holds Lodge's May 30 (05-30.vietnam-struggle)
1967:
- dup? 04-05.king and 04-05.vietnam-support (Roche on King, "thrown in with the commies")
- dup? 05-06.war-opposition and 05-07.war-opposition (St. Mark's meeting; Gibbons May 6, Bernstein May 7)
- dup? 11-11.war-opposition and 11-11.vietnam-prisoners (the three sergeants released to Hayden)
- doubtful: 10-11.vietnam and 11-08.vietnam-2, "Tuesday lunch" on a Wednesday
- three DTG times taken from Gibbons's citations (01-14, 01-25, 02-01 vietnam-air-war): the cables themselves unread
- bundles: 04-12.railroads (votes Apr. 11, signing Apr. 12); 01-10.rules (Speaker vote and rules votes)
1963:
- dup? 11-22.assassination-8 (the Chiefs raise alertness, about 2 p.m.) and 11-22.defense (forces worldwide on alert)
- doubtful: 08-07.civil-rights-bill (Celler at "the NAACP's convention at the Statler-Hilton", but the convention was in Chicago in July)
- order: 10-29.republican-party-congress (12:45 call to Halleck "after the vote"; Whalen puts the call on Oct. 24)
- Daily Diary disagreements for notes/diary-discrepancies.md: Nov. 25 King's call (Diary 9:16, Miller Center 9:20); economic advisers (Diary 9:20 vs schedule 8:45, Bernstein 9:15)
- sort fix: an unplaced entry a placed one follows now takes that place (dayorder STYLE 6)
1962:
- dup: 07-01.berlin-and-vienna and 07-01.soviet-union (same Presidium, Protocol 39): one entry, also:
- dup: 10-01.defense and 10-01.transition-and-staff (Taylor succeeds Lemnitzer)
- bundle: 10-23.missile-crisis (OAS vote, Proclamation ~7 p.m., RFK sees Dobrynin, repeating missile-crisis-5)
- held: 07-27.voting-rights should follow 07-27.press-and-broadcasting (both in held patches)
1960-61:
- dup? 1961-03-23.laos-2 (Schulimson) and 1961-03-24.laos (Anthony): the C-47 shot down, two days
- dup: 1961-11-07.states-and-cities repeats 1961-11-07.governors-nj (Hughes over Mitchell)
- dup? 1961-11-23 and 11-24.civil-rights-the-executive (housing order put off; Reeves: Nov. 25)
- doubtful: 1961-09-30.foreign-aid (Congress votes after Sept. 27 adjournment; Check added); 1960-07-02.amendments (Check)
- held: 1960-07-15.elections-1960-3 should follow 1960-07-15.elections-1960 (press-part-iii patch)
- propose.py's Papers tier misses "from 10:33 to 11:02 o'clock" and "at 4:10 o'clock" forms (only 1960-61 affected)
1964:
- dup? 08-25.elections-1964-6 and 08-25.elections-1964-freedom-democrats (Sanders and Connally, both 4:32 p.m.)
- doubtful: 08-28.elections-1964-atlantic-city (belongs to Aug. 26; Check there); 09-02.black-nationalism ("a Sunday afternoon"; Check there)
1968-69:
- dup: 1968-02-27.vietnam-205000 and 1968-02-27.vietnam (same meeting at State)
- dup: 1968-05-22.economy and 1968-05-23.economy (same text)
- dup: 1968-05-21.vietnam-force-levels and -2 (same Chiefs' reply)
- dup? 1969-01-17.conservation and 1969-01-18.conservation-2 (Johnson-Udall call)
- overlaps: 1968-04-04.elections-1968-4 / 04-04.vietnam-paris; 1968-08-28.elections-1968-chicago-17 / 08-28.elections-1968
- doubtful: 1968-11-20.vietnam-operations-2 ("Tuesday lunch" on a Wednesday); 1968-04-10.elections-1968 (Cooke installed Apr. 4; Check there)
Batch 6 (for the owner):
- Gifford: private citizens' letters (Blough, Walker, Fay, Greenbaum, Davenport, National Review readers, letters to Byrnes, Knezevich) kept passed over: R7 covers persons with a public role; does amended R18's "anything said in private about politics" take them in?
- Garrow's book-check excludes whole classes in a sentence (against R48): not re-ruled.
- Smith: Michael Rockefeller search entered for its government side; Murphy custody suit out as family.
- Dobrynin (b6): other rows marked "lead: the day" date to a month: entries under R50, left.
- Mann, Walls: undated rows that the Nov. 3-4 note says should become entries, left.
- Solberg: Humphrey's bladder polyp (June 9, 1967) and Johnson's departure in the blackout (Nov. 22, 1967) entered (fitness, candidacy, protest climate): the owner may rule otherwise.
- Barrett: "below the calendar's level" rows ruled too (R18 limits it to a unit's routine).
- Moyar: Halberstam's dispatches Aug. 22-31, 1963, and Lodge's arrival and dinners with the correspondents entered (the old "already repeated" was not borne out).
- Longley: Aeroflot cancellation: FRUS XVII docs. 92-93 put it Sept. 3-4, 1968, not at the Ranch in August (Check).
- Readers did not take up rows on other grounds that R14/R15/R50 now make entries: Moyar "below the level" operations and month-dated rows; Longley's dated "lead" rows; Mann (Walls) undated rows; Dobrynin month-dated "lead: the day" rows. A batch for these?
- Gibbons: Rostow to Rusk dated Jan. 5, 1967 by Gibbons's note; FRUS 1964-68, V, doc. 10 dates it Jan. 6 (Check).
- MACV: the 1964 J5 plan against an attack on Hue: entered as a completed plan shelved (R8), not "a draft not sent".
- Readers entered some rows on "where in doubt, enter it" (Soracco letter, Amite County regular's remark, Rusk's baseball game).
Sit-ins Feb. 8-13, 1960 (patch inbox/2026-11-10-sit-ins-feb-1960.yaml): after merge, strike the two old Checks on cal.1960-02-08.sit-ins ("Check: the dates of the cities." and Branch's long Check) that the split settles.
Times wanted (owner): Feb. 9, 10, 11, 12, 13, 14, 1960 sit-in articles; Feb. 11 most (Raleigh's first day Feb. 8 or 10; Hampton's Feb. 10 or 11; Nashville 40 or 500).
- Whalen (b6): the owner's examples all entered (Rodino favour, Libonati, Busby draft, the move, Dirksen's Christmas party, Mansfield's party, the Texas lunch). Doubtful: CQ, Aug. 2, 1968: Teresa McGovern's arrest entered (CQ prints it among McGovern's political news).
- Schwartz: three rows ruled out of the brief as another country's politics (Krone, Macmillan, Erhard's defeat): R18 now takes them in; left for a later run.
Batch 7 (already in):
- Westmoreland: 17 rows gave 44 cites, 11 variants + Checks (Barrel Roll Dec. 14, 1964; Hill 875 Nov. 17, 1967; Trinh's reception Dec. 30, 1967; Lang Vei after midnight Feb. 6, 1968; Komer and Abrams May 4, 1967; Cedar Falls 17 days; Junction City 282 dead US+ARVN; Ong Thanh 55 killed; March 1966 228 dead I Corps), 12 new entries.
- McPherson: "already in" wrong for the Panama flags; 6 entries (Canal Zone tour, Okinawa, Nixon's Rule XXII ruling, Wilkins's paper, two 1961 Senate votes).
- Zelizer: who Mills told to "choose guns" (Zelizer: the President; the entry, from Sanders's memo: Treasury's liaison): unsettled variant.
