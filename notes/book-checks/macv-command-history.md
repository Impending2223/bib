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
Patch: `inbox/2026-10-29-b3-macv-1964.yaml` (patch `b3-macv-1964`): 26 new entries, 16 edits.

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

## 1965 (`w.macv-command-history-1965`)

The copy: 496 PDF pages, the History submitted Apr. 20, 1966, "regraded unclassified" page by page; its annex on special
operations published separately and not in it. The printed page ("Page N of 482 Pages") is the PDF page less 14
throughout (checked on pp. 24, 41, 162, 222, 315, 479). Its text layer was usable; the footnote pages (313-17, 336, 342)
and every figure, date and note number a ruling rests on were read off the page images. Chapters: the summary and the
enemy (I, 1-21), the buildup and the forces (II, 22-...), plans and concept (III), operations (IV, 157-...), the
footnotes after the text (313-...), the chronology (478-82). Patch: `inbox/2026-10-29-b3-macv-1965.yaml` (patch
`b3-macv-1965`): 22 new entries, 15 edits.

### Rulings other than "holds"

| Entry | The calendar / the record | The History | Ruling |
|---|---|---|---|
| `cal.1965-08-18.vietnam` | the Marines count 614 enemy dead; Check the figures | ended Aug. 21, "approximately 700 VC KIA" (162) | Check, the History's figure; the end entered, Aug. 21 |
| `cal.1965-10-26.vietnam` | Westmoreland sends the 1st Cavalry after the regiments (Check) | Silver Bayonet from Oct. 23; the 1st Brigade's search-and-destroy mission Oct. 27 (168) | Check, the History's date |
| `cal.1965-11-14.vietnam` | B-52s on the massif from Nov. 15 | the strikes Westmoreland asked "delivered on 16 November" (168); the campaign's second phase, 1,286 enemy and 217 American dead | Check |
| `cal.1965-05-05.vietnam` | `c` ended "Check the dates." | the 173d's main body from May 5 (40), its first elements May 3 (chronology, 479); the Chu Lai landing May 7 (479) | the dates borne out; "Check the dates" taken out of `c`, a Check on May 3 in the note |
| `cal.1965-09-01.vietnam-3` | the concept, Sept. 1 | "Concept of Operations, 1 Sep 65" (28, ch. II n.3); published "in late August" (43), its letter of Aug. 30 (n.91) | Check |
| `cal.1965-12-11.vietnam-force-levels` (new) | | the accelerated brigades "approved on 11 December" (45 n.102, SECDEF 112125Z); "in mid-December, the SECDEF approved" the Marines' accelerated deployment (36 n.40, the same message) | dated by the message |

### For entries in pending patches

| Entry | Card, page (parenthetical) | Units |
|---|---|---|
| `cal.1965-03-06.vietnam` (b3-westmoreland) | `w.macv-command-history-1965`, 37–38 (Westmoreland's answer to the JCS: the Viet Cong hold the initiative; in six months the South's forces clustered about the cities, "end the war" groups; his recommendations: all available tactical air, coastal surveillance, a MEB to Đà Nẵng); via 38 n.49 (Msg, MACV, 060500Z Mar 65; ch. II n.16 gives it as MAC 1190, 060500Z Mar 65) | all |
| `cal.1965-03.vietnam-force-levels` (b3-westmoreland) | `w.macv-command-history-1965`, 38–39 (the Commander's Estimate of Mar. 26: RVNAF built up to the maximum, a division on the Qui Nhơn–Pleiku axis, a brigade at Biên Hòa–Vũng Tàu, a MEB in I Corps, some 33,000 men, by June 1965; the force ratios); via 39 n.58 (Commander's Estimate of the Situation in South Vietnam, 26 Mar 65). The History dates it Mar. 26: the entry can take the day | all |
| `cal.1965-06-24.vietnam-force-levels` (b3-westmoreland) | `w.macv-command-history-1965`, 40–41 (Westmoreland's exception to any withdrawal and to 23 battalions as a ceiling; another division; the 44-battalion force to establish a favorable balance by the year's end); via 40 n.70 (CJCS, No 2323, 222338Z Jun 65), 40 n.71 (COMUSMACV, MAC 3237, 24 Jun 65), 40 n.72 (COMUSMACV, MAC 3275, 26 Jun 65), 41 n.73 (CJCS, No 2400, 22 Jun 65), 41 n.74 (COMUSMACV, MAC 3320, 24 Jun 65). Check: the entry's MAC 3240 against the History's MAC 3237 and 3320 | all |
| `cal.1965-06-27.vietnam-operations` (b3-westmoreland) | `w.macv-command-history-1965`, 166–67, 480 (June 27–30; two ARVN airborne battalions, the 48th Regiment, the Australians; over 25 enemy killed, 200 tons of food and supplies destroyed, some 50 tons of rice recovered; "the first time in over a year" friendly forces in War Zone D); via 167 n.17 (Report, 173d Airborne Brigade, 11 Jul 65, Command Report) | all |

### The war table (for the merger; the scripts not touched)

- U.S. military strength in Vietnam at each month's end, 1965, as MACV's Table II-1 prints it (p. 269): Jan. 23,858;
  Feb. 24,937; Mar. 29,111; Apr. 36,021; May 51,728; June 59,921; July 81,422; Aug. 100,347; Sept. 132,297; Oct.
  153,279; Nov. 169,571; Dec. 184,314 (Army 116,755, Navy with the Coast Guard 8,749, Marines 38,190, Air Force 20,620).
  The chronology: about 23,000 Jan. 1, about 184,000 Dec. 31 (478, 482). The table has no monthly strength "then".
- The enemy, MACV's holdings by month, Table I-2 (p. 268): total strength (combat, support, militia, political cadre)
  93,000–113,000 in December 1964 and January 1965; 144,860–164,860 in April–May; 166,919–186,919 in July; 209,667 in
  August; 221,159 in October; 227,659 in November; 229,759 in December (combat 70,100; 19 regiments, 107 battalions;
  militia 103,573; political cadre 39,175). The table's MACV order of battle begins later (Dec. 1964 in its new
  format); these are the figures as MACV held them in 1965-66, a third vintage.
- Main force regiments, Nov. 21, 1965: 16 confirmed, 4 probable, 1 possible (p. 14).
- Infiltration in 1965: 26,188, 11,050 of them in North Vietnamese units, some 90 percent ethnic northerners (p. 14).
- RVNAF strength by month, 1965: charts only (Figures II-4 to II-7, pp. 293-96), no figures printed.

### Passed over

Made from the chronology (478-82) and each chapter's dated matter read.

| Page | Date | Event | Why |
|---|---|---|---|
| 478 | Jan. 22, 25, 27; Feb. 9, 15, 19, 22 | Buddhist demonstrations; martial law in Huế; Khánh's coup against Hương; Oánh, then Quát; Thiệu's council; Minh replaces Khánh | Saigon's politics, in the calendar by their chief days |
| 478 | Feb. 7–8, 10; Mar. 2, 8 | Pleiku and Đồng Hới; dependents evacuated; Qui Nhơn; Rolling Thunder; the Marines land | already in |
| 478 | Feb. 9, 19, 25; Mar. 15, 19, 27–28 | The Hawk battalion operational at Đà Nẵng; jets first used in the South; the Korean contingent; Route 19 reopened; an MP battalion; mines at Plei Do Lim; the Seventh Fleet's coastal surveillance | below the level; the MP battalion is in the History's account of Mar. 19-21 (38) |
| 478 | Mar. 21–22, 30 | Riot-control agents confirmed; the first radar site hit in the North; the embassy bombing | already in (the embassy, Mar. 30) or below the level |
| 479 | Apr. 1, 5; May 5, 7, 14; June 4; July 20; Aug. 7; Sept. 25; Oct. 21; Nov. 1; Dec. 1 | 1st Logistical Command; Rural Reconstruction; the political warfare directorate; III MAF; JUSPAO; Walt; USARV; III MAF senior adviser for I Corps; Field Force, Vietnam; the corps advisory duties | the command's organization: a lead (below); Task Force Alpha is in the Mar. 30 entry |
| 479 | Apr. 4, 9, 16; June 17; July 24, 27; Oct. 17; Dec. 2, 15 | The air war over the North: MiGs, the first SAM site, SAMs, Uông Bí | the air war, not read against the calendar here; to the owner |
| 479 | May 4, 13, 18 | The pauses in Rolling Thunder | already in |
| 479-80 | May 16; June 16, 25; Aug. 24; Dec. 4, 22 | The explosions at Biên Hòa; the Tân Sơn Nhứt terminal; the Mỹ Cảnh restaurant; Biên Hòa mortared; the Metropole bombing; Sóc Trăng | incidents, chronology only; to the owner (the Mỹ Cảnh and the Metropole killed Americans) |
| 480 | June 2; July 12, 21; Sept. 12; Oct. 7–8 | The Australians' advance party; the 2d Brigade, 1st Division; New Zealand's battery; the 1st Cavalry at Qui Nhơn; the 1st Division's rest; the Korean Capital Division | arrivals: the deployments are entered by their decisions; to the owner |
| 480 | June 18; July 16 | The first B-52 raid; B-52s in support of ground operations | already in (June 18) / below the level |
| 480 | July 1; Oct. 27 | The attacks on Đà Nẵng and Sóc Trăng air bases; on the Marines' air installations at Đà Nẵng and Chu Lai | to the owner: the Marble Mountain attack of Oct. 27 is not in the calendar |
| 480 | July 15; Nov. 7 | MACV confirms the North Vietnamese 101st Regiment in the South; MACV publicly confirms five North Vietnamese regiments | public statements of the order of battle, chronology only: a lead |
| 480-82 | Apr. 19; Sept. 28; Dec. 10 | Honolulu conferences (McNamara, Sharp, Wheeler, Westmoreland; Sharp and Westmoreland) | Apr. 19-20 already in; Sept. 28 and Dec. 10 chronology only: a lead |
| 481 | Sept. 7–11 | Piranha, the Marines on the Batangan peninsula (163): 198 enemy killed, 2 Marines | an operation below the level; to the owner |
| 481 | Sept. 11, 15; Dec. 18 | FULRO: Montagnards disarmed in Darlac; the loyalty ceremony; the seizure of Gia Nghĩa | to the owner (the Montagnards' thread) |
| 481 | Nov. 2, 5–6, 10, 22 | Cam Ranh's airfield; Throckmorton leaves, Heintges replaces him; Blue Marlin | personnel and operations below the level |
| 481 | Nov. 27 | The Viet Cong release Sergeants Smith and McClure in Cambodia | to the owner (prisoners) |
| 482 | Dec. 2 | The *Enterprise* in combat | below the level |
| 482 | Dec. 24 | The Christmas cease-fire | already in |
| 12-13 | year | Infiltration routes by land and sea; the 70th Transportation Group | undated |
| 36 | late Sept. | III MAF's estimate: two Marine divisions for the three enclaves | month only, within the Phase II requirements of Sept. 18 |
| 37 | Feb. 11 | The JCS recommend a 25th Division brigade to Thailand, the 173d alerted | to the owner: the JCSM of Feb. 11 (the calendar's Feb. 11 holds other Vietnam entries) |
| 38 | Mar. 7 | The Army Chief of Staff's briefings in Saigon: three helicopter companies, O-1 aircraft | within Harold K. Johnson's mission, in the calendar Mar. 2 and 16; the enclave concept entered Mar. 10 |
| 39 | Apr. 8–10 | The Honolulu conference of Apr. 8–10 (Stilwell's message, n.61) | a meeting's preparation and its recommendations, entered by the decision of Apr. 14; the conference of Apr. 19–20 already in |
| 42 | July 14 | Memo, SECDEF Saigon trip, items for discussion | a meeting's preparation; the briefing entered July 16 |
| 54–55 | Mar. 3; Apr. 10–13, 29, 30 | The planning conference for Market Time; the Swift boats bought; the Coast Guard squadron; McNamara on Market Time's control | steps of Market Time (entered Mar. 16); McNamara's announcement of Apr. 30 to the owner |
| 162 | July 28 | Liên Kết 4, the first significant combined Marine and South Vietnamese operation | below the level |
| 164-65 | year | Marine patrols, Golden Fleece, the enclaves' growth (6 to 600 square miles) | below the level |
| 168 | Nov. 1 | The 1st Brigade's pursuit west of Plei Me: 216 enemy killed, 117 captured; 55 American dead | a phase of Silver Bayonet; to the owner |
| 169 | Nov. 18-26 | Than Phong 7, the South Vietnamese airborne brigade west of Pleiku | an operation below the level |
| 220 | Apr. 28 | The amphibious and airmobile operation in Kiến Hòa: a weapons cache, 162 enemy killed | an operation below the level |
| 226 | July 8; Dec. 6 | Ambushes near Dầu Tiếng and in Hậu Nghĩa | engagements below the level |

### Leads

- The command's organization, 1965: the 1st Logistical Command (Apr. 1), III MAF (May 7), USARV (July 20), Task Force
  Alpha (Aug. 1) and Field Force, Vietnam (Sept. 25): the History's chronology (479-81) and ch. II; whether the calendar
  should hold the command's structure as it holds the MACV–MAAG merger of 1964.
- MACV's public confirmation of North Vietnamese units: the 101st Regiment (July 15), five regiments (Nov. 7): the
  History's chronology only; the press releases (MACOI) and the *New York Times* of the next days.
- The Honolulu conferences of Sept. 28 and Dec. 10 (Sharp and Westmoreland): chronology only; FRUS 1964–68, III.
- The Marble Mountain and Chu Lai attacks of Oct. 27: chronology only.
- The 1966 volume (the DMZ, Attleboro, Masher, Crimp) was not among the copies: a Sources to Fetch item.
