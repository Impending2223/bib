# *Alleged Assassination Plots Involving Foreign Leaders*, S. Rep. No. 94-465 (1975): the Cuba chapter and "Executive Action" against the calendar

Select Committee to Study Governmental Operations with Respect to Intelligence Activities, the interim report of Nov. 20, 1975, card `w.sen-church-alleged-assassination-plots`. Read Nov. 11–12, 2026 (batch 10, share 1, "Church, plots, Cuba"), from the AARC copy, https://www.aarclibrary.org/publib/church/reports/ir/contents.htm: `ChurchIR_3B_Cuba.pdf` (III.B, printed pp. 71–180, 110 PDF pages) and `ChurchIR_3C_ExecAction.pdf` (III.C, pp. 181–89, 9 PDF pages). The copies were deleted when the reading was done.

**The copy and its offset.** Both PDFs carry a text layer (`pdftotext -layout`), noisy on some pages (digits and letters wrong on pp. 86–88, 100–101, 128, 135; "2$" for the "2¢" of Operation Bounty, p. 144); no OCR was needed. Every quotation and number entered was read off the page image (`pdftoppm -r 100`). The folio is printed at the head of a page; the chapter's opening page (p. 71) has none. III.B: printed page = PDF page + 70 (PDF p. 1 = p. 71; checked on pp. 74, 83, 112, 125, 144, 177). III.C: printed page = PDF page + 180 (PDF p. 1 = p. 181, folio "(181)" at its foot; PDF p. 9 = p. 189). The senate.gov PDF the calendar already links (`#page=N`) runs 11 pages ahead of the printed folio (printed 74 = `#page=85`).

**The patch:** `inbox/2026-11-12-b10-church-cuba.yaml` (patch `2026-11-12-b10-church-cuba`): 40 new entries (ids claimed in the ledger first; one claimed id, `cal.1961-05-18.cuba`, not used); 31 `cite` ops; 11 `variant` ops; 6 `check` ops. `./bib patch-check`: 0 errors.

## How the chapter stood in the calendar before the reading

The calendar already held most of III.B: 59 entries cite S. Rep. No. 94-465 in the older form, "[S. Rep. No. 94-465, N (1975)](senate.gov …#page=M)", as the primary record, every unit mapped "all". Those were not cited a second time under the card: Jan. 13, Mar. 9, Mar. 14 and July 21, 1960 (the cable to Havana); the Plaza Hotel and Miami meetings and the briefing of Dulles and Cabell, Sept. 1960; the tap, Oct. 31, 1960; Harvey and the executive action capability, Jan. 25–26, 1961; the cigars and pills, Feb.–Mar. 1961; Hoover to Robert Kennedy, May 22, 1961 (Maheu to the FBI Apr. 18; Edwards May 3); the Cabinet Room, fall 1961; Szulc, Nov. 8–9, 1961; Mongoose, Nov. 30, 1961, Jan. 19, Feb. 20, Mar. 14, 1962; the wiretap case, Feb. 7 to May 7, 1962; the Special Group (Augmented), Aug. 10 and Oct. 4 and 30, 1962; Jan.–Feb. 1963; the Standing Group, Apr. 3 and May 28, 1963; the sabotage program, June 19, 1963; Cubela, Oct. 29 and Nov. 22, 1963; and the entries of the Dominican Republic, the Congo and Mar. 1967 that cite other chapters (not read here). Their pinpoints were not re-read page by page except where this patch adds a unit, a variant or a Check. A cite of the card was added only where the entry carried the report behind "To check:" or not at all, and where the page adds or disputes.

## Cited (the card) and what the page bears

| Entry | Units | Page | Ruling |
|---|---|---|---|
| `cal.1960-03-10.cuba` | ? | 93, 114 | pinned in part: the NSC's meeting of Mar. 10, 1960, from its minutes: Eisenhower, "we might have another Black Hole of Calcutta in… |
| `cal.1960-11-03.cuba` | A, B | 99, 116 | cited to A, B: Special Group Minutes, Nov. 3, 1960, quoted: Merchant's question on "direct positive action" and the Cuban governm… |
| `cal.1960-11-18.cuba` | ? | 119 | pinned in part: Dulles and Bissell "jointly briefed" the President-elect in "the latter part of November 1960" on "the most import… |
| `cal.1960-09.cuba-4` | ? | 79, 125–26 | pinned in part: Hoover to Bissell, Oct. 18, 1960, with copies to other members of the intelligence community: a source "whose reli… |
| `cal.1961-03.cuba-bay-of-pigs` | A, C, D | 123–24 | cited to A, C, D: Smathers, testimony, July 23, 1975, 6–7, 16–25, and his Oral History interview of Mar. 31, 1964: the conversation… |
| `cal.1961-04-22.cuba` | ? | 121, 135 | pinned in part: on Apr. 22, 1961 the President asked Taylor to reevaluate "our practices and programs in the areas of military and… |
| `cal.1961-05.cuba-bay-of-pigs` | ? | 125 | pinned in part: the Taylor/Kennedy Board interviewed several Cuban exile leaders of the Bay of Pigs on May 18, 1961, Robert Kenned… |
| `cal.1961-05.cuba-bay-of-pigs-2` | ? | 122–23 | pinned in part: Bissell, testimony, June 11, 1975, 27, July 22, 1975, 53–56: "the Underworld against the Castro regime"; "no idea"… |
| `cal.1961-06-06.crime-and-hijacking-maheu` | A | 128 | cited to A: Evans to Belmont, FBI, June 6, 1961: "We are conducting a full investigation in this wiretap case"; for B see Vari… |
| `cal.1961-08.crime-and-hijacking-maheu` | ? | 128 | pinned in part: on Aug. 16, 1961 the Assistant United States Attorney in Las Vegas "reported his reluctance to proceed with the ca… |
| `cal.1961-10-05.crime-and-hijacking-maheu` | ? | 128–29 | pinned in part: a Justice Department file entry of Oct. 6, 1961: "Yesterday P.M. told me that A.G. had inquired as to status of th… |
| `cal.1961-10.cuba` | B | 136–37 | cited to B: the CIA Board of National Estimates' "The Situation and Prospects in Cuba," 9: Castro's loss "by assassination or… |
| `cal.1961-06-13.cuba` | A | 121, 135 | cited to A: the "Taylor Report," issued June 13, 1961, makes no mention of the assassination plot; its conclusion that "there… |
| `cal.1961-11-16.cuba` | B | 83, 188–89 | cited to B: Harvey's notes, by the I.G. Report, 39: Bissell asked Harvey to take over the gambling syndicate operation and the… |
| `cal.1962-01-18.cuba-2` | ? | 142 | pinned in part: on Jan. 18, 1962 Lansdale assigned 32 planning tasks to the agencies and sent the Attorney General a copy with a n… |
| `cal.1962-03-16.cuba` | ? | 145 n.1 | pinned in part: SGA Memo for the Record, Mar. 16, 1962, "Discussion of Operation MONGOOSE with the President": in the presence of… |
| `cal.1962-04.cuba-2` | A | 83 | cited to A: Harvey, on "explicit orders" from Helms by his testimony, asked Edwards in early April 1962 to put him in touch wi… |
| `cal.1962-05.cuba-2` | ? | 84, 131 | pinned in part: Harvey arrived in Miami Apr. 21, 1962 and gave Rosselli the pills, four, given to the Support Chief Apr. 18 by the… |
| `cal.1962-05-09.crime-and-hijacking-maheu` | A, B, E | 132–33 and n.2 | cited to A, B, E: Hoover's memorandum for the record of May 10, 1962, of the conference of May 9: the Attorney General "wanted to ad… |
| `cal.1962-05-10.crime-and-hijacking-maheu` | ? | 132 | pinned in part: Edwards, with Houston's help, prepared a memorandum of the May 7 briefing dated May 14; for the day of the request… |
| `cal.1962-08-10.cuba` | A, B, D | 147, 161–66 | cited to A, B, D: the meeting chaired by Rusk with McNamara, McCone and Murrow present; the Group decides against Lansdale's "steppe… |
| `cal.1962-10-16.cuba` | C | 146, 147 n.2 | cited to C: Helms's memorandum of the meeting of Oct. 16, 1962: Robert Kennedy, "the general dissatisfaction of the President"… |
| `cal.1962-12.cuba-5` | ? | 85–86 | pinned in part: "Plans in Early 1963": Donovan, "not aware of the plan," to present Castro a contaminated diving suit; the I.G. da… |
| `cal.1963-04-21.cuba` | ? | 170–72 | pinned in part: Bundy's memorandum of Apr. 21, 1963 for the Standing Group, three alternatives: forcing "a non-Communist solution… |
| `cal.1963-10-24.cuba` | ? | 174 | pinned in part: Daniel, "Unofficial Envoy," New Republic, Dec. 14, 1963: he met Kennedy Oct. 24, 1963; they discussed the prospect… |
| `cal.1963-10-29.cuba` | ? | 174–75 | pinned in part: Fitzgerald "met AM/LASH in October 1963," as the personal representative of Robert Kennedy, with "assurances of fu… |
| `cal.1964-04-07.cuba` | ? | 177 | pinned in part: Special Group meeting, Apr. 7, 1964: Johnson "decided to discontinue the use of CIA-controlled sabotage raids agai… |
| `cal.1964-11.cuba` | ? | 89 | pinned in part: a CIA file entry of 1965: after Nov. 22, 1963 the CIA decided it "could have no part in the assassination of a gov… |
| `cal.1965-06.cuba` | A | 90 | cited to A: "In June 1965, CIA terminated all contact with AM/LASH and his associates for reasons related to security," I.G. R… |
| `cal.1967-03-04.robert-kennedy-3` | ? | 114 n.1 | pinned in part: Pearson's column of Mar. 3, 1967: a United States "plot" to assassinate Castro, and "one version claims that under… |
| `cal.1967-04-24.cuba` | ? | 179 | pinned in part: Pearson's article of spring 1967 prompted Johnson to direct Helms to investigate, "the Inspector General's Report… |

## Variants and Checks (the page says otherwise, or settles a day)

| Entry | Unit | The page (at) |
|---|---|---|
| `cal.1960-09.cuba-4` | A | On October 18, 1960, FBI Director Hoover sent a memorandum to DDP Bissell reporting the source's account (79, 125) |
| `cal.1960-09.cuba-4` | B | Rosselli introduced Maheu to Giancana in Miami "certainly prior to October 18"; Maheu recalls first meeting him after November 1960, at the Fountaine… (76 n.2) |
| `cal.1961-03.cuba-bay-of-pigs` | B | the President did not indicate directly that assassination had been proposed to him; Smathers's "impression" was that someone else "had apparently di… (124) |
| `cal.1961-06-06.crime-and-hijacking-maheu` | B | "the Attorney General will be orally assured that we are following up vigorously" (128) |
| `cal.1961-10-05.crime-and-hijacking-maheu` | B | the Special Group's minutes of October 6, 1961 state that the Group was told that "a contingency plan in connection with the possible removal of Cast… (136) |
| `cal.1961-11-16.cuba` | A | Bissell, in his last testimony, believed the Executive Action capability was "undoubtedly," or "very much more likely," initiated within the Agency,… (182–87) |
| `cal.1962-05.cuba-2` | A | "The keys were given to Rosselli, who watched the delivery with the Support Chief from across the street" (84) |
| `cal.1962-05.cuba-2` | B | Harvey arrived in Miami on April 21 and gave the pills to Rosselli, before the Attorney General's briefing of May 7; "In the latter half of April 196… (84, 131) |
| `cal.1962-05-10.crime-and-hijacking-maheu` | A | On May 11 the Attorney General requested Edwards to prepare a memorandum of the May 7 briefing (132) |
| `cal.1962-12.cuba-5` | A | the Inspector General: the plan was abandoned because Donovan gave Castro a different diving suit on his own initiative; Helms testified that the sui… (86) |
| `cal.1963-04-21.cuba` | A | a memorandum entitled "Cuba Alternatives" (170) |
| `cal.1960-09.cuba-4` | Check | Check: the day settled: the report, 79, 125, dates the memorandum Oct. 18, 1960 (Hoover to Bissell), not Sept. |
| `cal.1961-05.cuba-bay-of-pigs` | Check | Check: the day: the report, 125, dates the Board's interview of several exile leaders, Robert Kennedy present, May 18, 1961; the same session if San… |
| `cal.1961-10.cuba` | Check | Check: the days: the report, 136: NSAM 100 and Parrott's memorandum, Oct. 5, 1961; the Special Group's minutes, Oct. 6. |
| `cal.1961-11-16.cuba` | Check | Check: the day: the report, 83, has Harvey's notes on Nov. 16, 1961; 188, on Nov. 15. |
| `cal.1962-12.cuba-5` | Check | Check: the month: the report, 85–86, has the plan "in early 1963," the Inspector General's January 1963, "likely" earlier. |
| `cal.1967-04-24.cuba` | Check | Check: the report, 179, dates the Inspector General's Report May 23, 1967. |

Disagreements within the report: Harvey's notes put the meeting with Bissell that turned the Rosselli contact over to him on Nov. 16, 1961 (83) and on Nov. 15 (188); the Special Group (Augmented)'s cut-back of Lansdale's plan is "in February 1962" (144) against its minutes of Mar. 5 and Lansdale's memorandum of Mar. 2 (145, 152); the memorandum to Harvey is "sent" Apr. 26 and dated Apr. 27 (104); and the text of p. 139 prints "November 1962" for the Mongoose proposal, its notes 1961. Fitzgerald met AM/LASH "in late fall 1963" (87) and "in October 1963" (174); the calendar's Oct. 29 holds.

## New entries

| Entry | Event | Page |
|---|---|---|
| `cal.1960-11-25.cuba` | Eisenhower, 10:40 a.m., with Gray present: operations in another country; "there was also some… | 112 n.1 |
| `cal.1960-02-25.middle-east` | The CIA's Near East Division asks the "Health Alteration Committee" to endorse a "special oper… | 181 n. |
| `cal.1961-07-21.cuba` | The Special Group agrees that "the basic objective toward Cuba was to provide support to a U.S… | 135–36 |
| `cal.1961-10-05.cuba` | Bundy to the Secretary of State, NSAM 100, "Contingency Planning for Cuba": "In confirmation o… | 136 |
| `cal.1961-11-02.cuba` | Goodwin to the President and the Attorney General, "eyes only": a suggested organization for w… | 138 n.2 |
| `cal.1961-11-15.cuba` | Lansdale to Robert Kennedy, outlining the Mongoose proposal: a "picture of the situation has e… | 139 |
| `cal.1962-01-27.cuba` | Lansdale to the Attorney General: "we might uncork the touchdown play independently of the ins… | 142–43 |
| `cal.1962-01-30.cuba` | The Special Group (Augmented) approves Lansdale's 33 tasks for planning purposes. Task 33, add… | 143 |
| `cal.1962-01-30.cuba-2` | Craig, for the Defense Department and the Joint Chiefs on the Mongoose working group, to Lansd… | 144 |
| `cal.1962-03-05.cuba-2` | The Special Group (Augmented): major operations going beyond the collection of intelligence to… | 144–46, 152 |
| `cal.1962-03-22.cuba` | The Special Group (Augmented), a note on the minute of Mar. 16 on the President's progress rep… | 145 n.1 |
| `cal.1962-03-23.crime-and-hijacking-maheu` | Hoover to Edwards: the Criminal Division asks that the CIA "specifically advise whether it wou… | 130–31 |
| `cal.1962-04-08.cuba-2` | New York. Harvey, the Support Chief and Rosselli meet, their second meeting. By the Inspector… | 84, 134 |
| `cal.1962-04-10.cuba-3` | Harvey to McCone: "To permit requisite flexibility and professionalism for a maximum operation… | 145 |
| `cal.1962-08-13.cuba` | Lansdale to Harvey and the working group, after the meeting of Aug. 10: an outline of an alter… | 161–62 |
| `cal.1962-08-14.cuba` | Harvey to Helms, with Lansdale's memorandum, "including liquidation of leaders" excised: "The… | 162 |
| `cal.1962-08-20.cuba` | Taylor to the President: the Special Group (Augmented) sees no likelihood that Castro's govern… | 147 |
| `cal.1962-08-30.cuba-2` | The Special Group (Augmented) instructs the CIA to submit a list of possible sabotage targets:… | 147 |
| `cal.1962-09-07.cuba-3` | Miami. Harvey meets Rosselli, Sept. 7 and again Sept. 11. The Cuban is reported preparing anot… | 84 |
| `cal.1962-09-14.cuba-2` | The Special Group (Augmented) approves in principle a proposed set of operations. Bundy "made… | 146 |
| `cal.1963-04-23.cuba` | The NSC Standing Group first discusses Bundy's "Cuba Alternatives." Robert Kennedy proposes a… | 171–72 |
| `cal.1963-08-16.cuba` | Helms, asked by McCone about the *Chicago Sun-Times* of this day, which says the CIA had a con… | 107–8 |
| `cal.1963-10-03.cuba` | The Special Group approves nine operations in Cuba, several of them sabotage. | 173 |
| `cal.1963-10-24.cuba-3` | The Special Group approves thirteen major sabotage operations in Cuba for November 1963 throug… | 173 |
| `cal.1963-11-18.cuba-2` | Attwood, by his testimony in 1975, telephones a member of Castro's staff in Cuba. On White Hou… | 174 |
| `cal.1964-03.cuba` | One cache of arms for AM/LASH delivered in Cuba, by CIA cables. | 89, 176 |
| `cal.1964-04-08.cuba` | McCone's memorandum, the day after Johnson decided to stop CIA-controlled sabotage operations:… | 177 n.2 |
| `cal.1964-05-05.cuba` | The CIA's AM/LASH file: the case officer asks the Technical Services Division to produce, on a… | 89 |
| `cal.1964-06.cuba` | A second cache of arms for AM/LASH delivered in Cuba, by CIA cables. | 89, 176 |
| `cal.1964-06-10.cuba` | Helms to McCone: Agency officials have learned of several plots by Cuban exiles to assassinate… | 177–78 |
| `cal.1964-06-18.cuba` | The Special Group on Helms's report of the exile plots. McCone "somewhat skeptical," opposes m… | 178 |
| `cal.1964-06-22.cuba` | Robert Kennedy, informed a few days after the Special Group's decision of June 18 of the exile… | 178 |
| `cal.1964-08-19.cuba` | McCone to Bundy, for the Special Group: the FBI's investigation of the exile plots, summarized… | 178 and n.1 |
| `cal.1965-01-03.cuba` | A CIA document: B-1, leader of an anti-Castro group, in a lengthy interview with a case office… | 90 |
| `cal.1967-03-06.cuba` | The FBI to Attorney General Ramsey Clark, under "Central Intelligence Agency's Intentions to S… | 128 n.1 |
| `cal.1967-04-14.cuba` | McCone, out of the CIA, dictates a memorandum on the meeting of Aug. 10, 1962, after a call fr… | 164 n.2 |
| `cal.1962-04-26.cuba` | The Special Group: General Taylor asks that Harvey "attend the next meeting and report on agen… | 104 |
| `cal.1962-05-14.crime-and-hijacking-maheu` | Edwards, with Houston's help, to the Attorney General: a memorandum of the briefing of May 7.… | 98, 132 |
| `cal.1962-05-14.cuba` | Edwards, for his own files, the same day: "On this date Mr. Harvey called me and indicated tha… | 134 |
| `cal.1962-05-14.cuba-2` | Harvey, by his account to the Inspector General, briefs Helms on the meeting with the Attorney… | 104 |

## Passed over

| The report | Page | Ground |
|---|---|---|
| The testimony of 1975 on who knew or authorized (Bissell, Edwards, the Support Chief, Harvey, Helms, McCone, Elder, Carter, Houston; Gray, Goodpaster, Parrott, John Eisenhower; Rusk, McNamara, Gilpatric, Taylor, Bundy, Rostow, Goodwin, Sorensen, Lansdale, Smathers, Martin, O'Leary) | 92–121, 148–69, 175–76, 179–80, 184–89 | 1975 testimony dates only what it recalls; the days it recalls are in the entries above. Not entered apart: McCone's call to McNamara "immediately after the meeting" and Harvey's briefing of McCone "the day following" Aug. 10, 1962 (164–66), no document dating either (leads). |
| Aug. 16, 1960, the box of cigars given to be poisoned; Feb. 10 and later, 1961, the pills tested and delivered; Mar. 12, 1961 (Shimon's date) | 73, 80–82 | held: `cal.1961-02.cuba-2`, `cal.1961-03.cuba` (cite the report by the older form) |
| Apr. 18 and May 3, 1961, Maheu and Edwards to the FBI | 79, 126–27 | held: `cal.1961-05-22.robert-kennedy` (pp. 125–28) |
| Dulles's approval of King's memorandum, Dec. 11, 1959 | 92 | before the span; the approval undated |
| The Mar. 9, Mar. 10 and Mar. 14, 1960 meetings; Jan. 13, 1960 | 93, 113–16 | held (all cite the older form; Mar. 10 now takes the card) |
| Jan. 4, 1963 Bundy to the President; Apr. 3 and May 28, 1963; June 19 and Oct. 3 and 24, 1963 sabotage | 171–73 | held except Oct. 3 and 24, entered |
| Hoover's lunch with the President, Mar. 22, 1962; Hoover to Robert Kennedy and O'Donnell, Feb. 27, 1962 | 129–30 | held: `cal.1962-03-22.transition-and-staff`, `cal.1962-02-27.transition-and-staff` |
| A friend of the President in touch with Rosselli and Giancana, 70 White House telephone logs, Dec. 1960 to mid-1962 | 129 and n.2 | held in the Campbell entries of the calendar (not re-read) |
| Oct. 16, 1962 Helms memorandum, the one sabotage "attempted had failed twice" | 146 | cited on `cal.1962-10-16.cuba` |
| Mar. 5, 1962 Lansdale to Helms (weekly estimates of agents); Apr. 11, 1962 Lansdale to the Special Group (arms to resistance groups "ad hoc") | 145 | a covering instruction inside the entries of Mar. 5 and Mar. 14; left as a lead |

## Leads (undated, year-only, or a day not given)

- Mar.–Aug. 1960: the CIA's schemes to destroy Castro's image, a chemical like LSD for his studio, cigars with a disorienting chemical, thallium salts for his beard (72).
- Late spring or early summer 1960: Bissell asks Scheider to review the "capability of the clandestine service in the field of incapacitation and elimination" (181 n.); April 1960, the Health Alteration Committee's "disabling operation" and the handkerchief mailed from an Asian country, undated (181 n.; the memorandum's date printed "4/1/62").
- Early 1961 (before Jan. 25): Bissell and Harvey's first talks of Executive Action; "early in the Kennedy Administration" and "the early months of 1961": Bissell and Bundy on the capability (121, 183, 186).
- Mid-1961: the FBI told Giancana and Rosselli were in a CIA operation (106); early autumn 1961, Bissell "chewed out" in the Cabinet Room (141; `cal.1961-10.cuba-2` holds it by month).
- Apr. 19–20, 1961: the President, McNamara and Lemnitzer with a translator and Cuban exile leaders, by a CIA memorandum of Apr. 24 (124); the calendar's Bay of Pigs entries for Apr. 19–20 not searched for it.
- Sept.–Nov. 1961: Dulles's ten to twelve briefings of McCone (101 n.).
- Early 1963: the exploding seashell planned by Task Force W for Castro's skin-diving place (85); and the diving suit, early 1963 by the report's heading, "likely" earlier (86).
- Fall 1963: AM/LASH meetings with Case Officer 1, "execution"; Fitzgerald's second meeting and the cache promised Nov. 22 (86–88); fall 1964, the memorandum that the Government "cannot become involved" in the "first step" (89); early 1965, the CIA puts AM/LASH in touch with B-1 and cables that B-1 has given him a silencer (89–90).
- June or July 1962: Robert Kennedy sends a CIA official to Guantanamo (150 n.); Oct. 1962: Harvey's "confrontation" with Robert Kennedy over agent teams (148 n.); Aug. 31 and Sept. 9, 1962: Lansdale's task to "provoke incidents between Cubans and Bloc personnel," the Special Group on "attacking and harassing" Soviet personnel (147 n.1).
- 1966: Helms's memorandum to Rusk that the CIA "was not involved with [AM/LASH] in a plot to assassinate Fidel Castro" (178); May–June 1966, Rosselli and the FBI, Osborn's memorandum of June 24, 1966 (85 n.4, 96 n.2); Oct. 1966, the data that came to the FBI's attention (128 n.); spring 1967, Helms briefs Johnson orally on the Inspector General's report, the day not given (179).
- Dec. 2, 1961: Castro's "Marxist-Lenist" speech, by Larson (114 n.2); Jan. 24, 1962, the CIA memorandum listing "crime syndicates" as possible intermediaries for Task 5 (143 n.3).

## Where batch 10 stopped

III.B (pp. 71–180) and III.C (pp. 181–89) read in full. The dated events of 1960–68 are entered, cited, or listed above; testimony and the footnotes' memoranda were taken for the dates they give. Not done: the older entries' pinpoints (the 59 cited by the senate.gov form) were not re-read; the other chapters (Congo, Trujillo, Diệm, Schneider, the findings) are share 2's; no witnesses (`inbox/witnesses/`) written; claim maps (`src`) for the new entries not written, the patch's `n` carrying the pinpoints.


# Share 2 (batch 10, "Church, plots, the rest"): the Congo, Trujillo and Diem chapters against the calendar

Same report, card `w.sen-church-alleged-assassination-plots`. Read Nov. 11–12, 2026 (batch 10, share 2) from the AARC copy, https://www.aarclibrary.org/publib/church/reports/ir/contents.htm: `ChurchIR_3A_Congo.pdf` (III.A, printed pp. 13–70, 58 PDF pages), `ChurchIR_3D_Trujillo.pdf` (III.D, pp. 191–216, 26), `ChurchIR_3E_Diem.pdf` (III.E, pp. 217–24, 8), `ChurchIR_4_Findings.pdf` (IV; read for the Lodge and Bundy cables, p. 257, and the Trujillo findings, pp. 270–73) and `ChurchIR_1_Introduction.pdf` (I; the summary, nothing dated beyond the chapters). `ChurchIR_3F_Schneider.pdf` (Chile, 30 pp.): leads only, below. The copies were deleted when the reading was done.

**The copy and its offset.** The folio is printed at the head of a page. Printed page = PDF page + 12 (Congo; PDF p. 1 = p. 13; checked on the images at pp. 15, 17, 24, 44, 51), + 190 (Trujillo; checked at pp. 192, 201, 211), + 216 (Diem), + 254 (Findings; PDF p. 3 = p. 257, checked on the image). The text layer is poor on digits and caps: "9/E/60" for the cable of 9/15/60, "g/20/61" for 9/20/60, "1566 rounds" for 1500 (p. 201), "4/13/60" for the Herter memorandum of 4/14/60 (p. 192), "personal approval" for the cable's "unofficial approval" (p. 192, in italics). Every page was therefore re-read from a 300-dpi tesseract pass of the page images; each quotation and each date entered was found in that pass, and in the text layer where the layer was good (a good many quotation pieces only the tesseract pass reads, a few only the layer). The page images were opened for the pages named above and for p. 18 (the Oct. 6 cable, in a note). The pages cited are those where the quoted words stand, found by search, not counted off the text: reading the text with the folios as footers, as I first did, put the pages after p. 40 one too high.

**The patch:** `inbox/2026-11-12-b10-church-plots.yaml` (patch `2026-11-12-b10-church-plots`): 107 new entries (Congo 41, Trujillo 57, Diem 9; ids claimed in the ledger first; two same-day pairs put under neighbouring threads to keep the merge from flagging them); 33 `cite` ops; 6 `variant` ops; 5 `check` ops. `./bib patch-check`: 0 errors; 8 warnings, all "a duplicate of …?" on a day that already holds an entry under the same thread (distinct events; `./bib resolve ID --take keep` if the merge flags them).

## How the chapters stood in the calendar before the reading

The calendar already held the Congo plot in outline under the subthread `congo-lumumba` (the station's cable of Aug. 18, Bissell's of Aug. 19, the Special Group and Dulles's cable of Aug. 25–26, Sept. 19, 24 and 26, Oct. 5 and 17, the NSC of Aug. 18), the report cited as a linked URL ("S. Rep. No. 94-465, 14–15 (1975)") and some events from Fursenko and Naftali; those entries are cited again under the card, with the pages found. It held little of the Trujillo conspiracy beyond Jan. 12, Feb. 15 and 17, May 5 and May 29–31, 1961, and the Diệm coup in full from FRUS and the Pentagon Papers; the plots' own cables and memoranda were absent.

## Cited (the card) and what the page bears

| Entry | Units | Page | Ruling |
|---|---|---|---|
| `cal.1960-08-18.congo-lumumba` | ? | 14–15 | the station's cable of Aug. 18: "Congo experiencing classic Communist effort takeover government," "little time left in which take action to avoid another Cuba"; the station's objective, "replacing Lumumba with pro Western Group"; Tweedy… |
| `cal.1960-08-19.congo-lumumba` | B | 15 | the words, "You are authorized proceed with operation"; signed by Bissell, the DDP; not the telegram number or the ambassador |
| `cal.1960-08-25.congo` | A, B, C | 15–16, 60 | the Special Group minutes of Aug. 25 quoted: Gray, the President "had expressed extremely strong feelings on the necessity for very straightforward action"; planning "would not necessarily rule out 'consideration' of any particular kind … |
| `cal.1960-08-18.congo-2` | A, B, C, D, F | 55, 58 | the NSC minutes quoted: Dillon, Lumumba "was working to serve the purposes of the Soviets," Dulles, "Lumumba was in Soviet pay"; the President, "the possibility that the U.N. would be forced out was simply inconceivable," to keep the UN … |
| `cal.1960-09-19.congo` | ? | 23 | the cable of Sept. 19, signed by Bissell and Tweedy, to the "Station Officer" (Devlin), not called chief of station: "Joe" to arrive "approx 27 Sept," "Joe from Paris"; not Eisenhower and Lord Home |
| `cal.1960-09-24.congo-lumumba` | ? | 24 | Dulles's personal cable of Sept. 24: "We wish give every possible support in eliminating Lumumba from any possibility resuming governmental position or if he fails in Leopoldville, setting himself in Stanleyville or elsewhere"; the entry… |
| `cal.1960-09-26.congo-lumumba` | ? | 24, 33 | Scheider, "Joseph Scheider," the report's name for Gottlieb, with lethal biological materials, rubber gloves, mask and syringe; contact with Devlin Sept. 26; Lumumba "virtually a prisoner in U.N. custody, and inaccessible," 33; not Mobut… |
| `cal.1960-10-05.congo-lumumba` | ? | 29 | Scheider, the report's name for Gottlieb, left the Congo Oct. 5 in view of the "expiration date his material"; the station's cable of Oct. 7: "[Joe] left certain items of continuing usefulness. [Station officer] plans continue try implem… |
| `cal.1960-10-17.congo` | ? | 32 | Devlin's cable of Oct. 17, answering Tweedy's of Oct. 15: "If case officer sent, recommend HQS pouch soonest high powered foreign make rifle with telescopic scope and silencer," "hunting rifles now forbidden," would "keep rifle in office… |
| `cal.1960-09-07.congo` | B | 62 | the NSC of Sept. 7: Dulles on the Soviet aid to Lumumba, "Lumumba always seemed to come out on top in each of these struggles"; two pages of minutes, no statement by the President recorded; not the station and Mobutu |
| `cal.1960-11-27.congo` | ? | 33, 48 | Lumumba's "departure for Stanleyville on November 27" from UN custody; not the night; the station, by Devlin, "quite certain" it had no part in his leaving |
| `cal.1960-12-01.congo` | ? | 14, 48 | captured by Mobutu's troops "early in December" on the way to Stanleyville and held at Thysville; not Dec. 1, the Sankuru, or the flight back |
| `cal.1961-01-17.congo` | ? | 50 | Lumumba, Mpolo and Okito put aboard a plane Jan. 17, bound for Bakwanga, redirected to Elisabethville; the UN commission: Lumumba killed Jan. 17, "almost immediately after his arrival in Katanga"; not the beating on the way |
| `cal.1961-02-13.congo` | A | 50 | Feb. 13, Katanga's government "reported that Lumumba and his two companions escaped the previous day and died at the hands of hostile villagers"; the UN commission "not convinced" |
| `cal.1960-07-27.congo` | ? | 14, 53 | Lumumba in Washington in late July; Herter pledged economic aid; Dillon with Herter at the State Department meeting; not Blair House, the days, aid through the UN or Eisenhower |
| `cal.1961-01-12.latin-america` | ? | 196 | the Special Group, Merchant, Gray, Irwin and Dulles, approved "limited supplies of small arms and other material" for dissidents inside the Dominican Republic, the passage to be managed by the CIA and the dissidents themselves; not Eisen… |
| `cal.1961-02-15.latin-america` | ? | 203 | Rusk's memorandum to Kennedy of "February 15, 1961," the passage quoted as "[and] * * * the CIA has recently been authorized to arrange for delivery to them outside the Dominican Republic of small arms and sabotage equipment"; the note p… |
| `cal.1961-02-17.latin-america` | ? | 203–204 | Bissell's briefing paper to Bundy, requested "for higher authority": dissident leaders' "plan of action * * * implemented if they were provided with arms for 300 men, explosives, and remote control detonation devices"; a clash that "will… |
| `cal.1961-05-05.cuba` | ? | 209 | the Record of Actions: the Task Force on Cuba to prepare plans for crises in Haiti or the Dominican Republic; "Noted the President's view that the United States should not initiate the overthrow of Trujillo before we knew what government… |
| `cal.1961-05.latin-america-3` | ? | 207 | reports of an imminent assassination; Robert Kennedy talks with Dulles "apparently sometime in the early part of May," calls the President, "decided at that time that we'd put a task force on the problem"; the President "had known nothin… |
| `cal.1961-05.latin-america-4` | ? | 211 | the document of May 13, "neutralize" underscored, Goodwin circling the passage on the weapons passed, new to him; not Goodwin's taking it to the President, Kennedy's words or the instruction to Dearborn |
| `cal.1961-05-29.latin-america` | A, B | 213 | the cable of May 29, revised by Goodwin: "we must not run risk of U.S. association with political assassination, since U.S. as matter of general policy cannot condone assassination. This last principal is overriding and must prevail in d… |
| `cal.1961-05-30.latin-america` | ? | 213 | Trujillo "ambushed and assassinated near San Cristobal" late in the evening of May 30; the assassination "conducted by members of the action group, to whom the American carbines had been passed"; not the place outside Ciudad Trujillo or … |
| `cal.1961-05-31.latin-america` | B | 214 | Salinger "made the first public announcement of the assassination," several hours ahead of the news in the Dominican Republic; Rusk, by his testimony, "most concerned," his son Ramfis being in Paris; not Rusk's telephone call |
| `cal.1963-08-24.vietnam` | E, G | 218–219 | Deptel 243, "prepared by Roger Hilsman" and Harriman and approved by Kennedy: Diệm to be rid of the Nhus, "if he remains obdurate" the United States "prepared to accept the obvious implication that we can no longer support Diem"; the gen… |
| `cal.1963-10-05.vietnam` | ? | 220 | Conein contacted Minh "On October 3," not Oct. 5; Minh explained a coup was planned, asked assurances of American support if it succeeded, outlined three courses, one the assassination of Nhu and Cẩn; the station's cable of Oct. 5; not M… |
| `cal.1963-10-28.vietnam-saigon` | B, D | 222 | Oct. 28, Conein with Đôn, who "had received assurance from Lodge that Conein spoke for the United States," said he would give Lodge the coup plans "four hours before it took place" and suggested Lodge not change his plans to go to the Un… |
| `cal.1963-10-30.vietnam-2` | ? | 222 | a cable from Bundy to Lodge of Oct. 30 "expressed White House concern": "[w]e cannot accept conclusion that we have no power to delay or discourage a coup"; a second the same day told Lodge to intercede with the generals if he did not th… |
| `cal.1963-10-30.vietnam` | ? | 222 | Lodge "reported to Washington that he was powerless to stop the coup, and that the matter was entirely in Vietnamese hands"; the report's words, not Lodge's; not the hour, Diệm or "traitors" |
| `cal.1963-11-01.vietnam` | ? | 222 | the coup begun late in the morning of Nov. 1; Conein at the Joint General Staff headquarters "during most of the coup"; the generals announce the coup on the radio at 4:30 p.m.; Diệm "called Lodge and inquired about the United States' po… |
| `cal.1963-09-12.vietnam` | ? | 220 | Church, "with White House approval," introduced a resolution condemning the South Vietnamese government's handling of the Buddhists and ending aid unless the repression eased; not S. Res. 196, the cosponsors, State's draft or Church's words |
| `cal.1963-08-31.vietnam` | B | 220 | the CIA cable from Saigon, Aug. 31: "This particular coup is finished. Generals did not feel ready and did not have sufficient balance of forces. There is little doubt that GVN [South Vietnamese Government] aware US role and may have con… |
| `cal.1963-08-26.vietnam-saigon` | ? | 219 | the Director to Saigon, Aug. 26: Conein and another CIA officer told to see Generals Khiem and Khanh, "to convey to them the substance of Deptel 243, but to remind them that 'We cannot be of any help during initial action of assuming pow… |

## Variants and Checks (the page says otherwise, or settles a day)

| Entry | Unit | The page (at) |
|---|---|---|
| `cal.1960-08-18.congo-lumumba` | B | "there may be little time left in which take action to avoid another Cuba" (no "or Guinea") (14) |
| `cal.1960-11.congo-lumumba` | A | QJ/WIN, a foreign agent with a criminal record, reached Léopoldville Nov. 21, six days before Lumumba's flight; his plan, Nov. 29, was to escort Lumumba out of his residence; headquarters on Nov. 30 "prepared consider direct action"; "no… (44–45) |
| `cal.1961-01-12.latin-america` | A | the Special Group (Merchant, Gray, Irwin, Dulles) approves "limited supplies of small arms and other material" for dissidents in the Dominican Republic, the final transport by the dissidents themselves; no evidence any member but Dulles … (196) |
| `cal.1961-02-17.latin-america` | B | the sentence is Bissell's, in his memorandum to Bundy of Feb. 17, not Rusk's (204) |
| `cal.1961-05-05.cuba` | J | "the United States should not initiate the overthrow of Trujillo before we knew what government would succeed him, and that any action against Trujillo should be multilateral" (209) |
| `cal.1963-10-30.vietnam-2` | A | "[w]e cannot accept conclusion that we have no power to delay or discourage a coup" (222) |
| `cal.1960-10-17.congo` | check | when the poison was thrown into the river: Scheider testified he destroyed it and put it in the Congo River before leaving, Oct. 5; Devlin, that it was not disposed of until after Lumumba was imprisoned in early December ([[w.sen-church-… |
| `cal.1961-05-30.latin-america` | check | the report finds "no direct evidence that the weapons which were passed were used in the assassination," though one or more carbines were probably with the assassins; the killing was done "by handguns and shotguns," "near San Cristobal,"… |
| `cal.1963-10-05.vietnam` | check | the report dates Conein's contact with Minh "On October 3," the station's cable Oct. 5 ([[w.sen-church-alleged-assassination-plots]], 220). |
| `cal.1963-10-30.vietnam-2` | check | the findings give the sender as "William Bundy" and say the coup took place "three days later" ([[w.sen-church-alleged-assassination-plots]], 257); the chapter has "Bundy," at 222. |
| `cal.1963-11-01.vietnam` | check | the report: "The details of Diem's and Nhu's deaths are not known": Conein supposed they left by a tunnel for a Catholic church in Cholon; a CIA source, that they left the palace the evening before, were at the church by 8:00 a.m. and we… |

## Entered

**Congo** (41): `cal.1960-08.congo-lumumba`, `cal.1960-08-24.congo-lumumba`, `cal.1960-09-06.congo-lumumba`, `cal.1960-09-08.congo-lumumba`, `cal.1960-09-13.congo-lumumba`, `cal.1960-09-15.congo-lumumba`, `cal.1960-09-17.congo-lumumba`, `cal.1960-09-20.congo-lumumba`, `cal.1960-09-21.congo-lumumba`, `cal.1960-09-22.congo-lumumba`, `cal.1960-09-27.congo-lumumba`, `cal.1960-09-30.congo-lumumba`, `cal.1960-09-30.congo`, `cal.1960-10-06.congo-lumumba`, `cal.1960-10-07.congo-lumumba`, `cal.1960-10-07.congo`, `cal.1960-10-11.congo-lumumba`, `cal.1960-10-15.congo-lumumba`, `cal.1960-10-15.congo`, `cal.1960-10-26.congo-lumumba`, `cal.1960-10-28.congo-lumumba`, `cal.1960-10.congo-lumumba`, `cal.1960-11-02.congo-lumumba`, `cal.1960-11-03.congo-lumumba`, `cal.1960-11-13.congo-lumumba`, `cal.1960-11-14.congo-lumumba`, `cal.1960-11-21.congo-lumumba`, `cal.1960-11.congo`, `cal.1960-11-28.congo-lumumba`, `cal.1960-11-29.congo-lumumba`, `cal.1960-11-30.congo-lumumba`, `cal.1960-12-14.congo-lumumba`, `cal.1961-01-12.congo-lumumba`, `cal.1961-01-13.congo-lumumba`, `cal.1961-01-14.congo-lumumba`, `cal.1961-01-16.congo-lumumba`, `cal.1961-01-19.congo-lumumba`, `cal.1961-02-10.congo-lumumba`, `cal.1960-07-21.congo-lumumba`, `cal.1960-09.congo-lumumba`, `cal.1961-01-11.congo-lumumba`.

**Trujillo** (57): `cal.1960-02-10.latin-america-dominican-republic`, `cal.1960-04-14.latin-america-dominican-republic`, `cal.1960-04-21.latin-america-dominican-republic`, `cal.1960-06-16.latin-america-dominican-republic`, `cal.1960-06-21.latin-america-dominican-republic`, `cal.1960-06.latin-america-dominican-republic`, `cal.1960-07-01.latin-america-dominican-republic`, `cal.1960-07-01.latin-america`, `cal.1960-07-14.latin-america-dominican-republic`, `cal.1960-07-14.latin-america`, `cal.1960-08-26.latin-america-dominican-republic`, `cal.1960-09-08.latin-america-dominican-republic`, `cal.1960-10-27.latin-america-dominican-republic`, `cal.1960-10.latin-america-dominican-republic`, `cal.1960-12-29.latin-america-dominican-republic`, `cal.1961-01-12.latin-america-dominican-republic`, `cal.1961-01-19.latin-america-dominican-republic`, `cal.1961-01-31.latin-america-dominican-republic`, `cal.1961-02-10.latin-america-dominican-republic`, `cal.1961-02-14.latin-america-dominican-republic`, `cal.1961-03-13.latin-america-dominican-republic`, `cal.1961-03-15.latin-america-dominican-republic`, `cal.1961-03-16.latin-america-dominican-republic`, `cal.1961-03-20.latin-america-dominican-republic`, `cal.1961-03-24.latin-america-dominican-republic`, `cal.1961-03-26.latin-america-dominican-republic`, `cal.1961-03-31.latin-america-dominican-republic`, `cal.1961-04-05.latin-america-dominican-republic`, `cal.1961-04-07.latin-america-dominican-republic`, `cal.1961-04-07.latin-america`, `cal.1961-04-10.latin-america-dominican-republic`, `cal.1961-04-10.latin-america`, `cal.1961-04-17.latin-america-dominican-republic`, `cal.1961-04-20.latin-america-dominican-republic`, `cal.1961-04-25.latin-america-dominican-republic`, `cal.1961-04-27.latin-america-dominican-republic`, `cal.1961-04-30.latin-america-dominican-republic`, `cal.1961-05-02.latin-america-dominican-republic`, `cal.1961-05-03.latin-america-dominican-republic`, `cal.1961-05-04.latin-america-dominican-republic`, `cal.1961-05-10.latin-america-dominican-republic`, `cal.1961-05-12.latin-america-dominican-republic`, `cal.1961-05-13.latin-america-dominican-republic`, `cal.1961-05-15.latin-america-dominican-republic`, `cal.1961-05-15.latin-america`, `cal.1961-05-16.latin-america-dominican-republic`, `cal.1961-05-16.latin-america`, `cal.1961-05-16.cuba-2`, `cal.1961-05-17.latin-america-dominican-republic`, `cal.1961-05-18.latin-america-dominican-republic`, `cal.1961-05-21.latin-america-dominican-republic`, `cal.1961-05-24.latin-america-dominican-republic`, `cal.1961-05-26.latin-america-dominican-republic`, `cal.1961-05-27.latin-america-dominican-republic`, `cal.1961-05-30.latin-america-dominican-republic`, `cal.1961-05-31.latin-america-dominican-republic`, `cal.1961-06-01.latin-america-dominican-republic`.

**Diem** (9): `cal.1963-10-05.vietnam-saigon`, `cal.1963-10-05.vietnam-6`, `cal.1963-10-06.vietnam`, `cal.1963-10-07.vietnam`, `cal.1963-10.vietnam`, `cal.1963-10-24.vietnam-2`, `cal.1963-11-01.vietnam-saigon-4`, `cal.1963-11-02.vietnam-saigon`, `cal.1963-11-02.vietnam-5`.

Persons the report names who have no name entry (no `name:` tag, no Part III entry made): Hedgman (Devlin's name in the report, which the entries give as Devlin), Scheider (Gottlieb), Mulroney, Dearborn, Farland, Coerr, Parrott, Boggs, Lay, Elder, Didier, Timberlake, Mulele, Joseph Scott, Devine. The report's pseudonyms (Hedgman, Scheider, "Joe") are kept in the notes beside the names the calendar already uses; Mulroney is the report's own name.

## Judgments for the lead and the auditor

- A cable and its answer, or a note and its reply, are separate entries (Sept. 30, Oct. 7 and Oct. 15, 1960; Apr. 7 and 10, May 15 and 16, 1961; Oct. 5, 1963), by the owner's rule of Oct. 28; the Feb. 10 and 15, 1961 meetings in New York, which the report does not tell apart, are one entry.
- Testimony of 1975 dates only what it recalls: Tweedy's first talk with Bissell (Aug.), Bissell to Mulroney (Oct., late), Mulroney's "virus in the safe" (Nov. 3), the late-November meeting of the African stations, Conein told of McCone's answer "around October 20," Scheider's meeting with Tweedy (Sept.), each an entry with "Check: the day" and the witness named.
- The Aug. 25–26 entry keeps its one entry (the Special Group and the cable of the next day); not split here.
- The calendar's Sept. 26 and Oct. 5 entries name Gottlieb where the report says "Joseph Scheider"; cited with units "?" for that reason. Devlin is called "the Station Officer" and never chief of station in the report; the cite on Sept. 19 is "?" for it.

## Dated, in the report, and not entered

**Congo.** Oct. 27, 1960, Africa Division to Léopoldville on WI/ROGUE ("learns quickly and carries out any assignment without regard for danger," 46); Sept. 19 and Oct. 1960, WI/ROGUE's briefing and the cable on his use (the I.G. memorandum, 46–47); Dec. 2, his first contact with the station officer (47); Dec. 9, the cable on QJ/WIN's return (44); the cables of Oct. 29, Nov. 4 and Nov. 11 (folded into the notes of Nov. 3 and Nov. 13); the memorandum of Jan. 31, 1961 on payments to QJ/WIN (43 n.); a CIA cable of 1962 on QJ/WIN's trial (46, no day); the NSC of July 15, 1960 (Johnson present, the President absent, the words not given, 57). Not dated to a month: Dillon's Pentagon meeting, "late July or August" (53–54); Bissell's talks with Scheider, late spring to early fall (20–21); Mulroney's talks with Scheider and Helms after Bissell's request (39–40).

**Trujillo.** June 17 and 18, 1960 (Dearborn asks that the arrangement be confirmed; headquarters confirms, 192–93); Aug. 15, 1960, the staff assistant's letter to Dearborn (195); by Sept. 1, 1960, the request for 200 rifles (194); Mann to Dearborn, Oct. 10, 1960 (cited with Sept. 8); Mar. 17 and 21, 1961, the cables on pouching pistols (199); Apr. 6, the station's reply on the carbines (201); Apr. 11, the memorandum for the record of the station officer's consultation, five M3s (202); Apr. 19, the machine guns reach the station (206); Apr. 26, headquarters restates no approval (206); May 11, Dearborn's two-page draft (210); May 19, Scott to Bowles (211 n.); June 7, the CIA memorandum that two of three pistols went to a United States citizen (200); the meetings after the killing and the State Department's memorandum for the files of June 1 (214; the day of the meetings not given).

**Diem.** The chapter's retelling of the Pentagon Papers, May 8–Oct. 2, 1963 (Hue, May 8; Nolting, May 18; Trueheart, June 8 and 12; the generals' agreement "By July 4"; Nolting, Aug. 14; the raids of Aug. 21; Aug. 25, 26 and 29 cables; Bell, Sept. 8; McNamara and Taylor, Oct. 2; Stillwell, Oct. 17; Dalat, Oct. 27; Lodge, Oct. 29), which the calendar holds from FRUS and the Pentagon Papers: not cited; only the entries the report's own records bear on were (Aug. 24, 26 and 31, Sept. 12, Oct. 5, 28 and 30, Nov. 1).

**The findings** (IV, 255–73) restate the chapters' events and add nothing dated except the Lodge and Bundy cables of Oct. 30 (257, the findings call it "William Bundy" and put the coup "three days later"), and the Dec. 29, 1960, Jan. 12, Feb. 14, 15 and 17, Mar. 31 and May 3–16, 1961 events of the Trujillo case (270–73), which the entries above carry.

## Leads

- Chile, III.F (30 pp.; leads only, read for dates alone): the CIA spent over $3 million in the 1964 election (a note, no day; against `cal.1964-09-04.latin-america`); the rest is 1969–70, outside the span (the 303 Committee, Apr. 15, 1969; Sept. 4, 1970 on).
- The Special Group and NSC minutes the report quotes (Special Group: Feb. 10, Aug. 25, Sept. 8 and Dec. 29, 1960; Jan. 12, Feb. 14, May 4 and 18, 1961. NSC: July 21, Aug. 18, Sept. 7 and 21, 1960; May 5, 1961) are the primary records behind many entries above and stand behind "To check"; FRUS 1958–60, XIV (Congo) and 1961–63, XII (Dominican Republic) are where to look for them; not searched.
- Book I of the report (covert action) and the Hearings, vol. 7 (Chile) are not touched here.

Where batch 10 share 2 stopped: the Congo, Trujillo and Diem chapters read through, the findings for the dated passages; everything in them with a day or a month is in the patch or in the lists above.
