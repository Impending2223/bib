# MACV, *Command History*, 1964, 1965, 1967, 1968: the calendar read against the volumes

U.S. Military Assistance Command, Vietnam, *Command History* (the command's annual history, by its Military History
Branch), cards `w.macv-command-history` (the set) and one a volume (`w.macv-command-history-1964` ...). Read Oct. 29,
2026 (the b3-macv reading agent) from the owner's Drive copies, declassified U.S. Government records (17 U.S.C. § 105):
DTIC's scans, "regraded unclassified" page by page, some passages sanitized. Each copy's OCR layer was poor; every page
was read again with tesseract at 200 dpi, and the page images were looked at wherever a figure, a date or a note number
mattered. Cited by the volume's own printed page. The copies were kept outside the repo and deleted when each volume was
done; the 1966 volume was not among the copies.

The method: the volume's text against the calendar, its chronology appendix first, then each chapter; each dated event
looked for on its day in every thread (`./bib find -l cal --since D --until D`) and in the other pending patches. An
event the calendar holds took the page (an edit); one it lacks became an entry, the History its record, the papers its
notes cite behind "To check:" (each in `sources/cited-records/macv-command-history-<year>.yaml`), and FRUS read and cited
first where the daybook holds the paper. Staff and planning papers, commanders' messages and intelligence studies are
entries (the owner's ruling, Oct. 28, 2026).

## 1964 (`w.macv-command-history-1964`)

The copy: 209 PDF pages, a sanitized copy dated by its foreword Oct. 15, 1965; Annex A (special operations) "published
separately" and not in it. The printed page is the PDF page less 10 throughout (checked on pp. 15, 32, 188). Chapters:
command summary (1-9), personnel (10-38), intelligence (39-51), operations (52-134), logistics (135-154), planning
(155-171), communications (173-181), appendixes (key personnel, 188; chronology, 189-93). The notes follow each chapter.
Patch: `inbox/2026-10-29-b3-macv-1964.yaml` (patch `b3-macv-1964`): 23 new entries, 16 edits.

### Cites already in the calendar

| Entry | The cite | Ruling |
|---|---|---|
| `cal.1964-08-02.vietnam` | "MACV, Command History, 1964, Ann A, pp. IV-2-IV-4" (cited by Marolda, 410 n.38i) | Annex A is not in the copy read; it stays behind "To check:". The History's own account of Aug. 2, p. 109, added. |

### Rulings other than "holds"

| Entry | The calendar / the record | The History | Ruling |
|---|---|---|---|
| `cal.1964-08-04.vietnam` | the second attack reported; Herrick's doubts | "firmly established" that at least five boats engaged; 13 contacts fired on (109) | Check, the History's account cited for what it records |
| `cal.1964-12-24.vietnam` | the Brink bombing, Dec. 24, 2 killed, 50 hurt | text, Dec. 24 (20, 106); the chronology, Dec. 25, 2 Americans killed, 108 wounded (193) | Check |
| `cal.1964-10-24.vietnam` | Hương Prime Minister-designate by Oct. 31 | the chronology: Sửu elected and Hương Prime Minister, Oct. 24 (192); the charter Oct. 20, as the entry has it | Check on Hương; the charter's day borne out |
| new `cal.1964-10-31.vietnam-order-of-battle` | the infiltration study itself (FRUS 1964–68, I, doc. 392): 4,700 by August 1964, about 75 percent draftees | some 7,000 in 1964, about 90 percent draftees, citing the study (47) | the study's figures in `c`; Check on the History's |
| new `cal.1964-01-27.vietnam` | (none) | key personnel: deputy from Jan. 27 (188); the chronology: named Jan. 14 (189) | dated Jan. 27; Check |
| new `cal.1964-12-12.laos` | (none) | Barrel Roll's first missions Dec. 12 (113) | dated by the History; Check against the Air Force's and Navy's histories |
| new `cal.1964-04-10.vietnam` | (none) | the OCR read "20 April"; the page image reads "10 April" (12), as the note's message does (101545Z Apr 64) | Apr. 10 |

### Flagged as possible duplicates by the merge (distinct events; `--take keep`)

`cal.1964-03-10.vietnam-2` (OPLAN 98-64; the day's other entry is Gruening in the Senate), `cal.1964-05-15.vietnam-2`
(MAAG consolidated; the other the 532d NSC), `cal.1964-08-05.vietnam-4` (Westmoreland with Khánh; the others Pierce
Arrow, Syracuse, the staff meeting), `cal.1964-08-12.vietnam-2` (Hop Tac 1; the other Seaborn in Hanoi).

### For entries in pending patches

| Entry | Card, page (parenthetical) | Units |
|---|---|---|
| `cal.1964-09-20.vietnam` (b3-westmoreland) | `w.macv-command-history-1964`, 122–24, 192 (the rising of Sept. 19–20 at four camps; Ban Mê Thuột and Gia Nghĩa the objectives; Ban Mê Thuột's garrison warned by American advisers; the stand-off and Khánh's acceptance of the surrender, with amnesty; Bon Sar Pa, 192); via 122 n.169 (Hq 5th Special Forces Group, "Historical Resume of Montagnard Uprising, Sep 1964," undated). Also the primary record: [FRUS 1964–68, I, doc. 358](https://history.state.gov/historicaldocuments/frus1964-68v01/d358), Saigon 937, Sept. 24, 1964 (the Rhade uprising in Darlac; the aims: better treatment, Montagnards in office, aid, autonomy; read) | the rising and its course |
| `cal.1964-06-20.vietnam` (b3-westmoreland) | `w.macv-command-history-1964`, 9, 188 (Westmoreland COMUSMACV, June 20) | all |

### The war table (for the merger; the scripts not touched)

Figures the History prints that the table lacks "then" (the History dated Oct. 15, 1965):
- U.S. strength in Vietnam (MACV's): Jan. 1, 1964, 15,989; May 31, 16,454; Dec. 31, 23,301 (p. 16, n.20: Hq MACV to
  CINCPAC, Strength Report Vietnam, RCS 5314-1). The table's 1964-06 row has no "then"; its Dec. 31 "then" is the
  *Statistical Abstract*'s 23,300.
- U.S. casualties in 1964: 140 killed, 1,034 wounded, 22 missing, the figures reported to OASD(PA) (p. 20); the table's
  1964 hostile deaths "then" is the Abstract's 147.
- Viet Cong confirmed main and local forces: about 22,900 at the start of 1964, 33,000 at its end (p. 121); the order of
  battle grew some 44 percent in the year (p. 39).
- RVNAF strength at the end of 1964: regular forces 246,284, total 535,851 (pp. 61, 121); the war table's RVNAF rows
  begin later.
- Infiltration in 1964: about 7,000 (p. 47), against the study's 4,700 by August (FRUS 1964–68, I, doc. 392).

### Passed over

Made from the chronology (189-93) and each chapter's dated matter, Jan. 1964-Jan. 20, 1965.

| Page | Date | Event | Why |
|---|---|---|---|
| 189 | Jan. 2–6, 17, 21 | Council of Notables; the Buddhist charter; Cambodian forces attack in An Giang; Đôn commander in chief; Saigon command dissolved; a Navy team fights cholera | Saigon's internal measures and incidents, below the level |
| 189 | Jan. 18 | Largest helilift yet, 115 helicopters, 1,100 troops into War Zone D | an operation below the level (no contact) |
| 189 | Feb. 3, 7, 9, 11 | Terrorist bombings: Kontum compound, the Playboy bar (5 Americans killed), Pershing Field (2 killed), the Kinh Đô theater (3 killed) | incidents below the level; to the owner (Americans killed) |
| 189 | Feb. 10 | Khánh Premier, Minh Chief of State | Saigon's governments; check whether the calendar should hold it |
| 189 | Feb. 25 | Hilsman resigns | the calendar holds Hilsman's resignation? not searched here: to the owner |
| 189-90 | Mar. 3, 14, 23; Apr. 13, 25; June 24–25; Sept. 15, 20; Oct. 3, 11, 17; Nov. 21–22; Dec. 6–9, 28 | South Vietnamese operations and engagements (Kiến Phong, Kiên Long overrun, Plei Ta Nang, Thăng Long, An Lão, Quảng Tín, Đại Ngãi) | operations below the level the calendar records, each a line in the chronology |
| 189-91 | Mar. 20; May 7, 12; June 5, 21; Aug. 28; Sept. 5–6 | Border incidents with Cambodia; the UN mission; Saigon's proposal to the Security Council | to the owner: the Cambodian border thread, not searched here |
| 189 | Mar. 6; Apr. 7; Oct. 1, 9 | Khánh changes corps and division commanders; Saigon a special zone; sectors reconstituted; Viên III Corps commander | Saigon's internal measures |
| 190 | May 2–3 | The USNS Card damaged by a charge in the Saigon River; 8 Americans hurt | incident below the level; to the owner |
| 190 | May 10 | A plot to blow a bridge on McNamara's route foiled | incident below the level |
| 190 | June 28–29; July 1, 3 | Lodge leaves Saigon; New Zealand's engineers arrive; Sullivan minister-counselor; Killen to USOM | personnel and arrivals below the level (Lodge's resignation is in, June 23) |
| 190 | July 4, 6 | Polei Krong and Nam Đông Special Forces camps overrun (Nam Đông: 2 Americans and 1 Australian among 58 killed) | engagements, chronology only; to the owner |
| 190 | July 15, 19, 22–23 | McNamara: no North Vietnamese units in the South; Khánh's "Bắc tiến"; Kỳ on raids; Taylor and Khánh | the calendar's July 27 entry holds Khánh's campaign "to the North" |
| 191 | Aug. 19, 21, 26, 29; Sept. 2–4, 6, 8–9, 12 | VC headquarters bombed; an ambush; Đà Nẵng riot; Oánh; releases; the committee of 17; Khiêm resigns; Buddhist funerals; government reorganized; censorship lifted; State on negotiations | Saigon's politics, already in by their chief days (Aug. 16, 25, 27, Sept. 13) |
| 192 | Sept. 21–24; Oct. 2, 4 | The general strike in Saigon and its end; Khánh's threats; the Korean medical group arrives | Saigon's politics; the Korean group: to the owner (Korea thread) |
| 192 | Oct. 14–15, 18, 23–24 | Khiêm ambassador to Washington; the coup leaders tried, acquitted, re-arrested; Hanoi's charge of bombing | Saigon's politics, minor beside the entries held |
| 192 | Nov. 4, 17 | Typhoon Iris; flood relief, Marine helicopters from the Princeton | relief, below the level; to the owner |
| 193 | Dec. 5 | Kỳ's ultimatum to Khánh to support Hương | Saigon's politics; the calendar's Dec. 20 and the pending b3-westmoreland entries hold the generals |
| 10–11 | Feb. 15, 17; Mar. 3, 22, 31; Apr. 2, 23 | The JCS's query on MAAG; Harkins's reply; the staff's query; CINCPAC's endorsement; Harkins's renewed request; CINCPAC's opposition; the plan finalized | steps of the merger, entered at Mar. 12 (the study), Apr. 10 (the approval) and May 15 (the act); Harkins's reply of Feb. 17 is in the Mar. 12 entry |
| 23 | Apr. 6 | The National Service decree, after Khánh's talks with McNamara in March | Saigon's measure; to the owner |
| 24 | Aug.; Oct. 20–Nov. 2 | The Mission's manpower committee; the call-up of youths 20–25 | Saigon's measures, below the level |
| 57 | May 13 | McNamara: Special Forces in Vietnam to serve on permanent assignment | a statement within the buildup entered July 28 and Aug. 6 |
| 58 | Jan. 22 | The JCS extend the Marine helicopter squadron to June 30 | the step before the decision of June 10, entered |
| 59 | July 21 | MACV's request for more Army aviation (COMUSMACV 211745Z Jul 64) | a staff request; to the owner (aviation buildup, 20 units Oct. 1–Dec. 24) |
| 61-62 | Oct. 10; Oct. 26–Nov. 7; Nov. 25, 29 | The force structure survey ordered and made; J3 to CINCPAC; CINCPAC's concurrence | the survey's preparation; CINCPAC's concurrence of Nov. 29 (291030Z) passed over as a step, the JCS approval of Jan. 23, 1965 to come from the 1965 volume |
| 64 | Dec. | Khánh's order to the corps commanders to correct the deficiencies Westmoreland listed (entered Oct. 29) | a step after the entry; RVNAF memo of Dec. 17 (n.38) |
| 24–25 | Nov. 16 | Westmoreland to Taylor, "Measures of National Mobilization to Put SVN on a War Footing" (nn.33, 35, 46, 52) | the History draws figures from it, not its argument; to the owner (the call-up entry is Dec. 16) |
| 65-66 | Feb. 22; Nov. 11; Dec. 19 | The Chiến Thắng plan; RVNAF Directive AB 139; the Mission's statement on it | Saigon's plans; to the owner |
| 93-95 | Jan.; Feb. | Hand-spray defoliation delegated to the division advisers; the request of February for crop destruction authority | steps of the herbicide entries of Mar. 3 and July 29 |
| 95 | Mar. 7; June 24 | MACV's study of riot control agents; CINCPAC asks a plan | steps of the entry of Sept. 28 |
| 96 | late Nov. | Riot control munitions used on students in Saigon | undated (late November) |
| 97 | Aug.; Oct. 26 | MACV asks to use Lazy Dog; CINCPAC's reply; the test from late October | weapons trials below the level |
| 99-100 | Aug.; Sept.; Oct. 12; Dec. | The IV Corps border control plan; the Special Forces relocation study; Westmoreland on the Mekong and Bassac | staff studies without a decision; to the owner |
| 101 | Sept. 11, 13 | Saigon's cabinet on Mekong controls; the Embassy's talks | Saigon's measure; to the owner |
| 101 | Aug. 10, 15 | The Air Division's analysis of mortar attack on Biên Hòa; Westmoreland's letters on ground defense advisers | the letters are part of the Aug. 15 entry; the analysis below the level |
| 110 | Aug. 31; Sept. 21–27 | Westmoreland proposes Hawk units for five sites; the survey teams | a repetition of the Aug. 15 request; the survey below the level |
| 112-13 | Nov. 14; Dec. 23 | JRATA asks countermortar radars; Westmoreland's reply to CINCPAC | below the level |
| 113 | Feb.; May; June 28; July 18; Aug. 1 | U-2 flights over the North begin; Yankee Team begins; the Big Squirt transmitter near Huế agreed and on the air | to the owner: Yankee Team (May) month only; U-2 flights month only |
| 116-20 | year | Training: recruit, unit, Regional and Popular Force programs | below the level |
| 155 | Mar.; July; Aug. 21 | The Short Range Plan for Vietnam; the Military Assistance Planning Reference Book | plans superseded before use; to the owner |
| 158 | June 10 | Westmoreland to CINCPAC on airfields: a jet field at Chu Lai | to the owner (COMUSMACV 100449Z Jun 64; Chu Lai's start is a 1965 entry) |
| 159 | July 18; Nov. 7–11 | MACV's counterproposal on the RVNAF High Command; the decrees signed without American comment, objected to, reissued Nov. 11 | Saigon's measures; to the owner |
| 160-61 | Jan.; Aug. 5, 10 | MACV's national war plan outline; the J5 plan against a surprise attack on Huế, shelved; the Emergency Defense Plan | shelved or Saigon's; to the owner |
| 161-62 | Aug. 5, 7, 13 | The combined planning committee after Tonkin; the meeting with the JGS; OPLAN SK-1-64; the planning stopped | to the owner: combined planning begun and dropped |
| 162 | Dec. 1 | Taylor's talks in Washington (in, Dec. 1–3) | already in |
| 166-67 | Sept.; Oct.; Nov. | The SEACOORD committee of the missions in Laos, Thailand and Vietnam; Taylor's proposal; its meetings | month only: a lead (FRUS may date Taylor's proposal) |
| 175-76 | Mar.; Sept.; Dec. | SEATO planning conferences at Bangkok | below the level; to the owner |

### Leads

- SEACOORD (the Southeast Asia Coordinating Committee): Taylor's proposal of September 1964 and Rusk's concurrence
  (History, 166-67, nn.61-63): look in FRUS 1964–68, I and XXVIII, for the day.
- The Command History's Annex A (special operations, MACVSOG), 1964, published separately: not in the copy read;
  Marolda cites it for the raids of July 30-31 (`cal.1964-08-02.vietnam`).
- When each volume was made public (its declassification): the pages carry regrading stamps ("20 NOV 1975"; "Order
  Sec Army By TAG per 830624"); the date not settled, so no "Made public:" line was written.
