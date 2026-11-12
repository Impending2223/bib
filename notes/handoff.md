# Hand-off, Nov. 10, 2026 (evening; updated late evening): where the work stands

For a fresh orchestrating session. Read CLAUDE.md (the core), then this. The owner's standing rules: working hours (CLAUDE.md); ask before deleting anything of theirs; never change a Drive file's sharing; no model ids in commits.

## The new way of working (the owner, Nov. 10, 2026: "I approve both")
- CLAUDE.md is the core; topics in `notes/guide/`. Row readers work from `notes/briefs/reader-card.md`.
- Models: readers on Sonnet with the card; mechanical work (merging, duplicate flags, scripts) on Sonnet or Haiku; Opus audits a sample of each reader's rulings and every disagreement. At most 4-6 agents at once (the machine has 4 processors).
- Pilot first: `inbox/2026-11-10-pilot-humphrey.yaml` (Sonnet, the card) is to be audited row by row before anything scales.

## The queue (updated late on Nov. 11, 2026), in order
Done this evening: the splits and the press list; visibility phase 1 and the October 1962 prototype (`tools/vis/prototype.py`; the page sent to the owner); batch 9, every open "already in" row read and every op audited, all merged; batch 6 group 14 re-ruled and audited; the kind bands (elections, newspapers); the newspaper titles rewrite (1,460 notes); the Church Committee cards and plan. `./bib check` 0 errors; a full build and links before the PR.
1. A PR to main, on the owner's word.
2. The owner's rulings wanted (below): the kind-band questions; the prototype (what to change before the roll-out).
3. Visibility phase 3, the roll-out, once the owner has tried the prototype; the Western Alliance re-potting proposal (threads with polity lists); the year's Southeast Asia map moved to the year's first Monday (vnmap STYLE 8; the owner, Nov. 11).
4. The leftovers of batch 9 (its section below): one-event questions, two bundles, the Dallek 553 "thirty" against fifty, Chester and Ginsburg; and the leads with no day in each book-check file.
5. The owner items in the round-4 list and the batch-6 questions.
6. The shared folder's new material (notes/drive-additions-2026-11.md), and the foreign leadership works (the owner's question of Nov. 11: USSR, PRC, UK, France, FRG, DRV, RVN): a reading and procurement plan.
7. The Church Committee: read by the plan (`notes/proposals/church-pike-reading.md`), the plots report first; point the two kja entries at the cards.
8. The leads the batch-8 audits raised and two bundles the Ball audit found (cal.1960-08-01.congo unit C; cal.1965-06-01.latin-america).
9. `./bib works new --c` fails on an organization author: fix.

## Batch 8, the night of Nov. 10–11 (results)
- Twelve works read by Sonnet readers on the card, each audited blind by Opus, the audit's fixes applied (by Sonnet, from the auditor's exact list) and checked before merging: Barrett, Logevall, Reeves, Caro, Selverstone, Zaroulis, Schwartz, Wofford, Clifford, Ball, Rusk, Whalen. 349 rows; all merged; `./bib check` 0 errors.
- Error rate by op in the audited samples: 9–38% (Ball 9, Reeves 10, Logevall 11, Clifford 11, Whalen 16, Caro 19, Schwartz 21, Rusk 29, Wofford 32, Barrett 34, Selverstone 38; Zaroulis cites 10, variants 25). The kinds, commonest first: unit maps claiming more than the page (cured by the card's line of Nov. 11: `'?'` unless the page states the whole unit); Checks and variants that record no disagreement; cites on a neighbouring entry; new entries the calendar held already; days the work does not give; bundles. The card now carries a line for each.
- The audits also found errors already in the tree from earlier batches (over-claiming maps, an exchange turned round, a conflict on Rusk's whereabouts Mar. 30–Apr. 1, 1968): fixed in the same patches where an edit was allowed.
- Tokens (the agents' own counts): readers about 2.9M (Sonnet); audits about 2.5M (Opus); fix-appliers and the duplicate pass about 1.1M (Sonnet).
- Open rows left: about 365 (`python3 -I tools/works/alreadyin_rows.py OUT.json`), most in Dallek, Schlesinger's *Robert Kennedy*, Mann (two), Solberg and Watson (no text layer: OCR).
- Leads raised by the audits, not entered (no day or month on the page): in each work's book-check file.

## Batch 9, the evening of Nov. 11 (results so far)
- Sonnet readers on the card as amended Nov. 11; Opus audits reading every row blind and every op, each handing back the corrected patch, which the lead checked and merged. Merged: Mann *Walls*, group 1 (Berman, Nixon *RN*), Schlesinger *RFK* (two halves), Dallek *Flawed Giant* (three shares, the last audited in two halves), Solberg, Mann *Grand Delusion*, groups 2, 3 and 4. `./bib check` 0 errors after each.
- Reader error rate by op, as the audits found it: Mann *Walls* 0 of 17; Schlesinger 205–586 9%; Dallek 413–505 10%; Dallek 19–389 11%; Mann *Grand* 15%; groups 2 and 3 28%; Dallek 506–599 29%; Schlesinger 630–915 30%; Solberg 30%; group 4 39% (26% substantive). Commonest: events the calendar already held; two events in one entry; Checks and variants recording no disagreement (a different count, an omission); cites on a neighbour; notes pointing forward. The card's `'?'` line has cut over-claimed units sharply. OCR reads 3 as 5 in Dallek's face (a Pueblo "Jan. 25" variant, dropped).
- Fixed by hand from the audits: Solberg's cite on the Lincoln Park march (the wrong event); nine older maps that claimed more than the page (Schlesinger 227, 300, 302, 345, 359; Mann 250, 440, 442; Dallek 511–12); Califano 338, Johnson to bed "shortly before 11 P.M." (the entry had taken in n.29 as 11:29); the two "It's over" entries (July 1967) combined.
- Group 5 merged too (audit: 9 of 34 ops wrong, 26%); Watson merged (4 of 21 substantive, 19%; the Congo units "within 50 hours", the entry had 30; "Made public: FRUS 1958–60, IV (1992)" on two new entries, the year from the auditor's memory: to confirm). Then group 6 (16 of 47 ops, 34%; 9 of 47, 19%, without the units left `'?'` that the page states whole: the readers now under-map rather than over-map) and batch 6 group 14 (6 of 16, 37.5%). The kind bands merged (623 elections, 262 newspapers).
- Church Committee: 18 cards (`w.sen-church-*`, `w.house-pike-report-village-voice`) and the plan, `notes/proposals/church-pike-reading.md`. To do: point `kja.s-rep-no-94-465` and `kja.s-rep-no-94-755` at the cards; confirm the Chile report's date (Dec. 18, 1975, from memory). To procure (the owner): the Pike hearings, *U.S. Intelligence Agencies and Activities* (1975, six parts), *CIA: The Pike Report* (1977), H. Rep. 94-833. Bug: `./bib works new --c` fails on an organization author (AttributeError in `new_id`).
- Left for a later pass (from the audits; details in each report's book-check file): `cal.1963-12.king` and `cal.1963-12-24.king` maybe one event; `cal.1968-11-03.elections-1968-chennault-2` holds two events (the flight, the Los Angeles statement); `cal.1968-09-26.program` "thirty" years on Dallek 553's image against the entry's fifty; Mann's Feb. 2, 1967 placement of "prior and ostensibly unilateral action" (moderately sure); Poole's JCSM-461-61 and Kaplan's JCSM-476-61 (one paper or two); Ginsburg's "not ten cents" (Solberg 352) against Chester's Aug. 24 remark. Leads with no day: in the book-check files.

## Since then (Nov. 10, late evening)
- Pilot audited, corrected and merged with the b7 Humphrey patch (e2f5feb); p. 285 entered at the owner's word ("Agreed on Humphrey's son's cancer").
- Every b6 and b7 patch, the Presidium and sit-ins patches and the Caro `also` op merged (34 runs, commits from c282c02 on); the two old sit-ins Checks struck. Left in the inbox: the two held patches, and `inbox/deferred.yaml` (one Nixon RN cite waiting on bundle-splits).
- 516 duplicate flags open from those merges: `./bib check` and `./bib build` fail until settled. A Sonnet pass is writing proposals to `scratchpad/merge/dup-rulings.tsv` (keep / combine / doubt); the lead reviews every combine and doubt before applying. Then check, build, links.
- Batch 8 (`notes/briefs/batch8.md`): the 715 rows still open (`scratchpad/alreadyin/b8-rows.json`). First wave, Sonnet: Reeves, Logevall, Barrett; each to be audited by Opus before merging.
- The shared folder's new material: `notes/drive-additions-2026-11.md`.

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
- Kind bands (merged Nov. 11 evening; scripts in the session scratchpad, `kindbands-work/`): (1) elections abroad (12: Korea 1960, 1963; Japan 1960; the Dominican Republic 1962, 1966; Chile 1964; Turkey 1961, 1965; Iran 1963; South Vietnam 1966, 1967) placed on their own election night: keep? (2) evening papers (the *Star*, *Chicago Daily News*, *Post*, *Journal-American*, *Detroit News*, *Bulletin*, *World-Telegram*) and weeklies placed in the early morning like the morning papers: or the afternoon for the evening papers? (3) the range runs from the polls' closing to 2 a.m. local (the band's end), not six hours after the closing as the memo had it. (4) `cal.1964-04-14.governors-il` left unplaced: `cal.1964-04-14.republican-party` follows it but carries a workday range; which is wrong?
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
