# MACV, *Command History*, 1964, 1965, 1967, 1968: the calendar read against the volumes

U.S. Military Assistance Command, Vietnam, *Command History* (the command's annual history, by its Military History Branch), cards `w.macv-command-history` (the set) and one a volume (`w.macv-command-history-1964` ...). Read Oct. 29, 2026 (the b3-macv reading agent) from the owner's Drive copies, declassified U.S. Government records (17 U.S.C. § 105): DTIC's scans, "regraded unclassified" page by page, some passages sanitized. Each copy's OCR layer was poor; every page was read again with tesseract at 200 dpi, and the page images were looked at wherever a figure, a date or a note number mattered. Cited by the volume's own printed page. The copies were kept outside the repo and deleted when each volume was done; the 1966 volume was not among the copies.

The method: the volume's text against the calendar, its chronology appendix first, then each chapter; each dated event looked for on its day in every thread (`./bib find -l cal --since D --until D`) and in the other pending patches. An event the calendar holds took the page (an edit); one it lacks became an entry, the History its record, the papers its notes cite behind "To check:" (each in `sources/cited-records/macv-command-history-<year>.yaml`), and FRUS read and cited first where the daybook holds the paper. Staff and planning papers, commanders' messages and intelligence studies are entries (the owner's ruling, Oct. 28, 2026).

## 1964 (`w.macv-command-history-1964`)

The copy: 209 PDF pages, a sanitized copy dated by its foreword Oct. 15, 1965; Annex A (special operations) "published separately" and not in it. The printed page is the PDF page less 10 throughout (checked on pp. 15, 32, 188). Chapters: command summary (1-9), personnel (10-38), intelligence (39-51), operations (52-134), logistics (135-154), planning (155-171), communications (173-181), appendixes (key personnel, 188; chronology, 189-93). The notes follow each chapter. Patches: `inbox/2026-10-29-b3-macv-1964.yaml` (patch `b3-macv-1964`): 50 new entries, 16 edits; `inbox/2026-10-29-b3-macv-1964-more.yaml` (patch `b3-macv-1964-more`): 146 new entries.

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

`cal.1964-03-10.vietnam-2` (OPLAN 98-64; the day's other entry is Gruening in the Senate), `cal.1964-05-15.vietnam-2` (MAAG consolidated; the other the 532d NSC), `cal.1964-08-05.vietnam-4` (Westmoreland with Khánh; the others Pierce Arrow, Syracuse, the staff meeting), `cal.1964-08-12.vietnam-2` (Hop Tac 1; the other Seaborn in Hanoi).

### For entries in pending patches

| Entry | Card, page (parenthetical) | Units |
|---|---|---|
| `cal.1964-09-20.vietnam` (b3-westmoreland) | `w.macv-command-history-1964`, 122–24, 192 (the rising of Sept. 19–20 at four camps; Ban Mê Thuột and Gia Nghĩa the objectives; Ban Mê Thuột's garrison warned by American advisers; the stand-off and Khánh's acceptance of the surrender, with amnesty; Bon Sar Pa, 192); via 122 n.169 (Hq 5th Special Forces Group, "Historical Resume of Montagnard Uprising, Sep 1964," undated). Also the primary record: [FRUS 1964–68, I, doc. 358](https://history.state.gov/historicaldocuments/frus1964-68v01/d358), Saigon 937, Sept. 24, 1964 (the Rhade uprising in Darlac; the aims: better treatment, Montagnards in office, aid, autonomy; read) | the rising and its course |
| `cal.1964-06-20.vietnam` (b3-westmoreland) | `w.macv-command-history-1964`, 9, 188 (Westmoreland COMUSMACV, June 20) | all |

### The war table (for the merger; the scripts not touched)

Figures the History prints that the table lacks "then" (the History dated Oct. 15, 1965):
- U.S. strength in Vietnam (MACV's): Jan. 1, 1964, 15,989; May 31, 16,454; Dec. 31, 23,301 (p. 16, n.20: Hq MACV to CINCPAC, Strength Report Vietnam, RCS 5314-1). The table's 1964-06 row has no "then"; its Dec. 31 "then" is the *Statistical Abstract*'s 23,300.
- U.S. casualties in 1964: 140 killed, 1,034 wounded, 22 missing, the figures reported to OASD(PA) (p. 20); the table's 1964 hostile deaths "then" is the Abstract's 147.
- Viet Cong confirmed main and local forces: about 22,900 at the start of 1964, 33,000 at its end (p. 121); the order of battle grew some 44 percent in the year (p. 39).
- RVNAF strength at the end of 1964: regular forces 246,284, total 535,851 (pp. 61, 121); the war table's RVNAF rows begin later.
- Infiltration in 1964: about 7,000 (p. 47), against the study's 4,700 by August (FRUS 1964–68, I, doc. 392).

### Entered (the owner's ruling, Oct. 28): the papers

The staff and planning papers, commanders' messages and plans first passed over as "below the level", "a step" or "to the owner", now entries in the same patch, `inbox/2026-10-29-b3-macv-1964.yaml`:

| Page | Date | Entry | Id |
|---|---|---|---|
| 10 | Feb. 15 | The Joint Chiefs ask CINCPAC's and Harkins's comments on doing away with the Military ... | `cal.1964-02-15.vietnam` |
| 10 | Feb. 18 | CINCPAC agrees with Harkins against the merger: it would be "unduly rocking the boat ... | `cal.1964-02-18.vietnam` |
| 95 | Mar. 7 | MACV's study of riot control and incapacitating chemicals in the counterinsurgency, ... | `cal.1964-03-07.vietnam` |
| 11 | Mar. 22 | CINCPAC on MACV's merger study: no major reorganization now; Harkins to end the ... | `cal.1964-03-22.vietnam` |
| 11 | Mar. 31 | Harkins asks CINCPAC for a decision on the merger, to end the uncertainty in the command. | `cal.1964-03-31.vietnam-2` |
| 11 | Apr. 1 | CINCPAC reaffirms his opposition to so large a reorganization. | `cal.1964-04-01.vietnam-2` |
| 160 | June | CINCPAC's OPLAN 38-64, "Military Operations to Terminate Aggression in Southeast ... | `cal.1964-06.vietnam` |
| 158 | June 10 | Westmoreland to CINCPAC: the longer commitment needs logistic action; the jets of the ... | `cal.1964-06-10.vietnam-force-levels-2` |
| 95 | June 24 | CINCPAC asks MACV for a plan for the use of CS gas on a wide and on a limited scale. | `cal.1964-06-24.vietnam` |
| 155 | July | "The Short Range Plan for Vietnam," MACV's new country plan on the guidance of the ... | `cal.1964-07.vietnam` |
| 159 | July 18 | Westmoreland to Trần Thiện Khiêm, MACV's counterproposal on the High Command's plan to ... | `cal.1964-07-18.vietnam` |
| 59 | July 21 | MACV asks more Army aviation: tailgate delivery of supplies to advisers in remote ... | `cal.1964-07-21.vietnam-force-levels` |
| 161–62 | Aug. 7 | After the Gulf of Tonkin, MACV's planning committee, formed Aug. 5, meets the Joint ... | `cal.1964-08-07.vietnam-2` |
| 158 | Aug. 10 | Quảng Ngãi's runway found unable to take jets, Westmoreland recommends a jet airfield ... | `cal.1964-08-10.vietnam-force-levels` |
| 162 | Aug. 13 | The combined planning with the Joint General Staff ended, by Taylor's verbal ... | `cal.1964-08-13.vietnam` |
| 155 | Aug. 21 | CINCPAC publishes the Military Assistance Planning Reference Book for South Vietnam, ... | `cal.1964-08-21.vietnam-2` |
| 158 | Sept. 26 | CINCPAC to the Joint Chiefs on the Chu Lai airfield, recommending also a second runway ... | `cal.1964-09-26.vietnam-force-levels` |
| 112 | Nov. 14 | After the mortar attack on Biên Hòa, MACV's Joint Research and Test Activity ... | `cal.1964-11-14.vietnam` |
| 23–24 | Nov. 16 | Westmoreland to Taylor, "Measures of National Mobilization to Put SVN on a War ... | `cal.1964-11-16.vietnam` |
| 112 | Dec. 2 | Westmoreland asks CINCPAC for the radars, eight countermortar and three ground ... | `cal.1964-12-02.vietnam` |
| 65–66 | Dec. 19 | The American Mission's statement on the High Command's Directive AB 139, the missions ... | `cal.1964-12-19.vietnam` |
| 161 | Dec. 21 | MACV approves its Air Defense Requirements Plan for South Vietnam, its third version, ... | `cal.1964-12-21.vietnam` |
| 112–13 | Dec. 23 | Westmoreland to CINCPAC, on the Army's offer of a single radar section to test: ... | `cal.1964-12-23.vietnam` |
| 158 | Dec. 29 | McNamara authorizes military assistance funds for architect-engineer services at Chu ... | `cal.1964-12-29.vietnam-force-levels` |

### Entered (the owner's ruling, Oct. 28, late)

Every dated event the volume treats that the calendar lacks, the chronology's (189-93) and the chapters', each its entry, in the supplementary patch `inbox/2026-10-29-b3-macv-1964-more.yaml` (patch `b3-macv-1964-more`, merged after `b3-macv-1964`: some of its entries point to that patch's): Saigon's governments and measures, the operations and incidents, the border incidents with Cambodia, the visits and appointments, the papers. A month or a stretch is dated to the month or the first day, "Check: the day". The places named; a province tagged only where the History names it.

| Page | Date | Entry | Id |
|---|---|---|---|
| 160 | Jan. | MACV's J5 presents the South's Joint General Staff the outline of a new national war ... | `cal.1964-01.vietnam` |
| 189 | Jan. 2 | Saigon. The Council of Notables convenes to draft a new constitution. | `cal.1964-01-02.vietnam-saigon` |
| 189 | Jan. 3 | A Buddhist convention promulgates the charter of the Unified Vietnamese Buddhist Church. | `cal.1964-01-03.vietnam-saigon` |
| 189 | Jan. 4 | Cambodian forces attack a South Vietnamese unit in An Giang. | `cal.1964-01-04.vietnam` |
| 189 | Jan. 6 | Maj. Gen. Trần Văn Đôn becomes commander in chief of the armed forces. | `cal.1964-01-06.vietnam-saigon` |
| 189 | Jan. 17 | The special Saigon command dissolved, the capital put under III Corps. | `cal.1964-01-17.vietnam-saigon` |
| 189 | Jan. 18 | War Zone D. The largest helilift of the war: 115 helicopters carry 1,100 troops; the ... | `cal.1964-01-18.vietnam-operations` |
| 189 | Jan. 21 | Saigon. An American naval team fights a cholera epidemic. | `cal.1964-01-21.vietnam` |
| 58 | Jan. 22 | The Joint Chiefs approve keeping the Marine helicopter squadron at Đà Nẵng to June 30, ... | `cal.1964-01-22.vietnam-force-levels` |
| 47 | Feb. | High-altitude U-2 flights begin over North and South Vietnam, Laos and Cambodia. | `cal.1964-02.vietnam` |
| 189 | Feb. 3 | Kon Tum. The advisory group's compound attacked with grenades: one American wounded, a ... | `cal.1964-02-03.vietnam-operations` |
| 189 | Feb. 7 | Saigon. The Playboy bar bombed: five Americans killed. | `cal.1964-02-07.vietnam-operations` |
| 189 | Feb. 9 | Saigon. The bleachers at Pershing Field bombed: two Americans killed, 25 wounded. | `cal.1964-02-09.vietnam-operations` |
| 189 | Feb. 10 | Khánh names himself Prime Minister, Dương Văn Minh Chief of State. | `cal.1964-02-10.vietnam-saigon` |
| 189 | Feb. 11 | Saigon. The Capitol Kinh Đô theater bombed: three Americans killed, 50 wounded. | `cal.1964-02-11.vietnam-operations` |
| 65 | Feb. 22 | Khánh's government issues the Chiến Thắng ("Victory") plan in place of the strategic ... | `cal.1964-02-22.vietnam-saigon` |
| 189 | Feb. 25 | Hilsman, Assistant Secretary of State for Far Eastern Affairs, resigns under fire. | `cal.1964-02-25.vietnam` |
| 189 | Feb. 27 | Định Tường. A Viet Cong battalion, supposedly trapped, fights its way through a ring ... | `cal.1964-02-27.vietnam-operations` |
| 165 | Mar. | Bangkok. The SEATO coordination conference on the Central Region's plan, OPLAN 4-64, ... | `cal.1964-03.vietnam` |
| 57 | Mar. 1 | The commander of the Army's Special Forces in Vietnam asks a full Special Forces ... | `cal.1964-03-01.vietnam-force-levels` |
| 189 | Mar. 3 | Kiến Phong, near the Cambodian border. South Vietnamese airborne troops kill 110 of an ... | `cal.1964-03-03.vietnam-operations` |
| 189 | Mar. 6 | Khánh replaces three of the four corps commanders and five of the nine division ... | `cal.1964-03-06.vietnam-saigon` |
| 189 | Mar. 14 | Kiến Phong. 300 Viet Cong captured in an operation. | `cal.1964-03-14.vietnam-operations` |
| 189 | Mar. 20 | South Vietnamese forces strike the Cambodian town of Chantrea by mistake. | `cal.1964-03-20.vietnam-2` |
| 189 | Mar. 23 | Kiến Phong. Phượng Hoàng 13-14/10 finds a Viet Cong battalion in a fortified village ... | `cal.1964-03-23.vietnam-operations` |
| 57 | Apr. | On his visit to Vietnam, the Chairman of the Joint Chiefs told by Westmoreland's ... | `cal.1964-04.vietnam-force-levels` |
| 47 | Apr. | The South Vietnamese air force's 716th Reconnaissance Technical Squadron converted to ... | `cal.1964-04.vietnam-2` |
| 23 | Apr. 6 | The National Service decree, from Khánh's talks with McNamara in March: all men 20 to ... | `cal.1964-04-06.vietnam-saigon` |
| 189 | Apr. 7 | Khánh makes Saigon a special zone and splits III Corps. | `cal.1964-04-07.vietnam-saigon` |
| 189 | Apr. 13 | Kiên Long, a district capital near the U Minh forest, overrun: about 300 South ... | `cal.1964-04-13.vietnam-operations` |
| 190 | Apr. 25 | Johnson announces Westmoreland to replace Harkins. | `cal.1964-04-25.vietnam` |
| 190 | Apr. 25 | A South Vietnamese ambush near Plei Ta Nag kills 84 Viet Cong. | `cal.1964-04-25.vietnam-operations` |
| 66 | May | MACV proposes three phases of pacification: clearing, securing, developing. | `cal.1964-05.vietnam` |
| 66 | May | On McNamara's recommendation, Westmoreland has the J3 work out with Saigon a way of ... | `cal.1964-05.vietnam-2` |
| 190 | May 2 | Saigon River. The aircraft ferry USNS *Card* damaged by a Viet Cong shaped charge. | `cal.1964-05-02.vietnam-operations` |
| 190 | May 3 | A Viet Cong bombing at the *Card*'s dock: eight Americans hurt. | `cal.1964-05-03.vietnam-operations` |
| 58 | May 6 | MACV to CINCPAC: the American transport helicopters in the South to be kept at their ... | `cal.1964-05-06.vietnam-force-levels` |
| 190 | May 7 | Cambodia charges a South Vietnamese armored troop with attacking the village of Taey, ... | `cal.1964-05-07.vietnam` |
| 190 | May 10 | A terrorist plot to blow up a bridge on McNamara's route found and foiled. | `cal.1964-05-10.vietnam-operations` |
| 190 | May 12 | Two Cambodian jets strafe South Vietnamese units in Tây Ninh Province. | `cal.1964-05-12.vietnam-2` |
| 57 | May 13 | McNamara: the Army's Special Forces men in South Vietnam to be replaced by permanent ... | `cal.1964-05-13.vietnam-force-levels` |
| 58 | May 24 | The Joint Chiefs, told of MACV's proposal to keep the Marine helicopter squadron, ... | `cal.1964-05-24.vietnam-force-levels` |
| 58 | May 28 | MACV again recommends to CINCPAC keeping the Marine helicopter squadron indefinitely, ... | `cal.1964-05-28.vietnam-force-levels` |
| 190 | June 5 | South Vietnamese planes bomb and burn a 20-mile strip along the Vàm Cỏ Đông, on the ... | `cal.1964-06-05.vietnam-2` |
| 190 | June 21 | A UN mission leaves New York to investigate the incidents on the Vietnamese-Cambodian ... | `cal.1964-06-21.vietnam` |
| 190 | June 24 | Thắng Long–Hải Yến 79, on the Định Tường–Kiến Phong border, kills 99 Viet Cong. | `cal.1964-06-24.vietnam-operations` |
| 190 | June 25 | Quảng Ngãi. An attack on a Viet Cong training camp kills 50. | `cal.1964-06-25.vietnam-operations` |
| 190 | June 28 | Lodge leaves Saigon. | `cal.1964-06-28.vietnam` |
| 190 | June 29 | A New Zealand Army engineer detachment arrives. | `cal.1964-06-29.vietnam-force-levels` |
| 91 | July | The Joint Chiefs recommend that Saigon be urged to a strict reading of the protocol to ... | `cal.1964-07.vietnam-2` |
| 190 | July 1 | William Sullivan named minister-counselor of the embassy in Saigon. | `cal.1964-07-01.vietnam` |
| 190 | July 1 | The Senate confirms Taylor as Ambassador to South Vietnam and U. Alexis Johnson as his ... | `cal.1964-07-01.vietnam-congress-2` |
| 190 | July 3 | Killen appointed to direct the Saigon aid mission. | `cal.1964-07-03.vietnam` |
| 190 | July 4 | The Polei Krong Special Forces camp overrun: 50 friendly killed. | `cal.1964-07-04.vietnam-operations` |
| 190 | July 4 | Hanoi charges that South Vietnamese guerrillas attacked in Laos June 27 and on its ... | `cal.1964-07-04.vietnam` |
| 190 | July 6 | The Nam Đông Special Forces camp attacked: 58 friendly killed, two Americans and an ... | `cal.1964-07-06.vietnam-operations` |
| 190 | July 15 | McNamara's press conference: no North Vietnamese units operating in the South. | `cal.1964-07-15.vietnam-2` |
| 190 | July 19 | Saigon. Khánh leads a mass rally, shouting "Bắc tiến!", "To the North!" | `cal.1964-07-19.vietnam-saigon` |
| 190 | July 20 | The 9th Regiment of the North Vietnamese 304th Division cut up in battalion encounters ... | `cal.1964-07-20.vietnam-operations` |
| 190 | July 22 | The National Vietnamese Student Association demands the nationalization of French ... | `cal.1964-07-22.vietnam-saigon` |
| 190 | July 22 | Kỳ confirms guerrilla raids on the North to the press. | `cal.1964-07-22.vietnam` |
| 57 | July 22 | Westmoreland to CINCPAC, the formal request: the Special Forces in the country from ... | `cal.1964-07-22.vietnam-force-levels` |
| 191 | July 23 | Taylor meets Khánh: they disagree over Khánh's call to go North. | `cal.1964-07-23.vietnam` |
| 24 | Aug. | Taylor sets up the Mission's manpower committee, chaired by MACV's J1, with a ... | `cal.1964-08.vietnam-saigon` |
| 89, 92 | Aug. 8 | IV Corps presents Westmoreland its pilot border control plan, a physical barrier on ... | `cal.1964-08-08.vietnam` |
| 101 | Aug. 10 | The 2d Air Division's operations analysis, "Passive Defense Measures at Bien Hoa ... | `cal.1964-08-10.vietnam-2` |
| 160 | Aug. 10 | The High Command publishes its Emergency Defense Plan, a contingency defense plan ... | `cal.1964-08-10.vietnam-saigon` |
| 191 | Aug. 19 | A Viet Cong inter-province headquarters in the Mekong valley bombed; the Viet Cong ... | `cal.1964-08-19.vietnam-operations` |
| 191 | Aug. 21 | A Viet Cong ambush in a cleared area of the Mekong Delta. | `cal.1964-08-21.vietnam-operations` |
| 177 | Aug. 24 | Saigon. An experimental Syncom satellite ground station arrives: one voice and one ... | `cal.1964-08-24.vietnam` |
| 191 | Aug. 26 | Đà Nẵng. Rioters attack an American-supported hospital; the guard fires over their heads. | `cal.1964-08-26.vietnam-saigon` |
| 191 | Aug. 28 | Saigon proposes that the UN Security Council set up a commission to investigate the ... | `cal.1964-08-28.vietnam` |
| 191 | Aug. 29 | The military triumvirate appoints Oánh to head the government; Khánh ill at Dalat. | `cal.1964-08-29.vietnam-saigon` |
| 191 | Aug. 29 | Buddhist leaders announce they will press for an all-civilian government. | `cal.1964-08-29.vietnam-struggle` |
| 110 | Aug. 31 | Westmoreland proposes to CINCPAC Hawk units for the defense of Saigon, Biên Hòa, Nha ... | `cal.1964-08-31.vietnam-force-levels` |
| 166 | Sept. | Saigon. An ad hoc committee of the American military and diplomatic representatives to ... | `cal.1964-09.laos` |
| 90 | Sept. | A MACV staff and 5th Special Forces Group plan: five new CIDG camps and others moved ... | `cal.1964-09.vietnam-force-levels` |
| 165–66 | Sept. | SEATO's force commanders meet, at CINCUSARPAC's invitation, on the headquarters, ... | `cal.1964-09.vietnam-3` |
| 96 | Sept. | MACV and High Command officers discuss riot control munitions; the High Command's ... | `cal.1964-09.vietnam-4` |
| 101 | Sept. 1 | A joint High Command–MACV survey team visits Tân Sơn Nhứt, Biên Hòa and Đà Nẵng, after ... | `cal.1964-09-01.vietnam` |
| 191 | Sept. 2 | Under Buddhist pressure, the government releases 509 rioters arrested the week before. | `cal.1964-09-02.vietnam-struggle` |
| 191 | Sept. 3 | Khánh replaces the triumvirate with a 15-member committee to elect a temporary Chief ... | `cal.1964-09-03.vietnam-saigon` |
| 191 | Sept. 4 | Taylor goes to Washington. | `cal.1964-09-04.vietnam` |
| 191 | Sept. 4 | Khiêm resigns as Defense Minister; Khánh announces that the military will leave their ... | `cal.1964-09-04.vietnam-saigon` |
| 191 | Sept. 5 | Four Cambodian jets cross the border and fire on South Vietnamese aircraft, missing. | `cal.1964-09-05.vietnam` |
| 191 | Sept. 6 | A Cambodian aircraft fires on the Chu Muong outpost. | `cal.1964-09-06.vietnam` |
| 191 | Sept. 6 | Saigon. 150,000 Buddhists parade at the funeral of the victims of the ... | `cal.1964-09-06.vietnam-struggle` |
| 191 | Sept. 8 | The government reorganized: Khánh keeps the premiership; Dương Văn Minh chairman. | `cal.1964-09-08.vietnam-saigon` |
| 191 | Sept. 9 | Khánh abolishes press censorship. | `cal.1964-09-09.vietnam-saigon` |
| 92 | Sept. 11 | The Joint Chiefs, concerned at matériel for the Viet Cong shipped to Sihanoukville, ... | `cal.1964-09-11.vietnam` |
| 91 | Sept. 11 | Saigon's cabinet works out controls on Mekong traffic to Phnom Penh: government ... | `cal.1964-09-11.vietnam-2` |
| 191 | Sept. 12 | The State Department announces no plans for international negotiations on Vietnam. | `cal.1964-09-12.vietnam` |
| 110 | Sept. 12 | CINCPAC recommends to the Joint Chiefs two Army and one Marine Hawk battalions for ... | `cal.1964-09-12.vietnam-force-levels` |
| 91 | Sept. 13 | The embassy meets the Foreign Ministry on the Mekong controls; the emphasis on ... | `cal.1964-09-13.vietnam-2` |
| 192 | Sept. 15 | Khánh arrests five of the coup's leaders. | `cal.1964-09-15.vietnam-saigon` |
| 192 | Sept. 15 | Tư Lương 134, near Quảng Ngãi city: 80 Viet Cong killed. | `cal.1964-09-15.vietnam-operations` |
| 89, 92 | Sept. 18 | MACV's answer to the Joint Chiefs on the Mekong: searchlights, heavy machine guns and ... | `cal.1964-09-18.vietnam-2` |
| 192 | Sept. 20 | Lam Sơn 129, Quảng Trị: 77 Viet Cong killed. | `cal.1964-09-20.vietnam-operations` |
| 192 | Sept. 21 | A labor strike cripples Saigon's public services. | `cal.1964-09-21.vietnam-saigon` |
| 110 | Sept. 21–27 | Army and Marine teams survey sites and plan Hawk at Tân Sơn Nhứt–Biên Hòa, Nha Trang ... | `cal.1964-09-21.vietnam-force-levels` |
| 192 | Sept. 22 | A Korean noncombatant military assistance group arrives. | `cal.1964-09-22.japan-and-korea-korean-troops` |
| 192 | Sept. 24 | The strike ends in compromises between the labor leaders and Khánh's government. | `cal.1964-09-24.vietnam-saigon` |
| 110 | Sept. 30 | CINCPAC to the Joint Chiefs on the Hawk survey: Đà Nẵng the most exposed; a Marine ... | `cal.1964-09-30.vietnam-force-levels` |
| 167 | Oct. | A SEACOORD meeting on the Lao air force's strikes in the panhandle, American jet cover ... | `cal.1964-10.laos` |
| 90 | Oct. | Westmoreland gives tacit approval to moving CIDG camps closer to the border, if a Nùng ... | `cal.1964-10.vietnam-force-levels` |
| 192 | Oct. 1 | The Bạc Liêu and Châu Đốc sectors reinstituted. | `cal.1964-10-01.vietnam-saigon` |
| 192 | Oct. 2 | Khánh: he will accept a draft call to head the government; he threatens force against ... | `cal.1964-10-02.vietnam-saigon` |
| 192 | Oct. 3 | An Xuyên. Dân Chí 73: 150 Viet Cong killed. | `cal.1964-10-03.vietnam-operations` |
| 192 | Oct. 4 | Saigon. Riot police disperse workers. | `cal.1964-10-04.vietnam-saigon` |
| 192 | Oct. 4 | The Viet Cong kill an American and 40 Vietnamese 18 miles from Saigon. | `cal.1964-10-04.vietnam-operations` |
| 192 | Oct. 7 | Saigon complains to the ICC of North Vietnamese infiltration. | `cal.1964-10-07.vietnam` |
| 192 | Oct. 9 | Brig. Gen. Cao Văn Viên becomes III Corps commander. | `cal.1964-10-09.vietnam-saigon` |
| 61 | Oct. 10 | Westmoreland orders a joint American-South Vietnamese survey of the forces needed for ... | `cal.1964-10-10.vietnam-force-levels` |
| 192 | Oct. 11 | Three Viet Cong battalions and South Vietnamese forces engaged near Gò Dầu Hạ, heavy ... | `cal.1964-10-11.vietnam-operations` |
| 89–90 | Oct. 12 | Westmoreland forwards the IV Corps border control plan, the Mekong and Bassac controls ... | `cal.1964-10-12.vietnam` |
| 192 | Oct. 14 | Khiêm named ambassador to the United States. | `cal.1964-10-14.vietnam-saigon` |
| 192 | Oct. 15 | The leaders of the coup of Sept. 13 go on trial. | `cal.1964-10-15.vietnam-saigon` |
| 192 | Oct. 17 | Dân Chí 80, on the Ba Xuyên–Bạc Liêu border: 123 Viet Cong killed in two days. | `cal.1964-10-17.vietnam-operations` |
| 192 | Oct. 18 | Hanoi charges that American and South Vietnamese aircraft bombed a North Vietnamese ... | `cal.1964-10-18.vietnam` |
| 24 | Oct. 20 | The call-up of youths 20 to 25 begins, to Nov. 2, a month's enforcement to follow: ... | `cal.1964-10-20.vietnam-saigon` |
| 192 | Oct. 21 | Khánh's government makes way for a civilian government. | `cal.1964-10-21.vietnam-saigon` |
| 192 | Oct. 23 | The coup's leaders acquitted. | `cal.1964-10-23.vietnam-saigon` |
| 97 | Oct. 25 | MACV's Army Concept Team in Vietnam (ACTIV) completes a study of the South's infantry ... | `cal.1964-10-25.vietnam` |
| 61 | Oct. 26–Nov. 7 | The force structure survey team visits each corps headquarters, Oct. 26–Nov. 5, then ... | `cal.1964-10-26.vietnam-force-levels` |
| 167 | Nov. | A SEACOORD meeting on military operations in Laos and a project to improve Route 9 ... | `cal.1964-11.laos` |
| 65 | Nov. | High Command Directive AB 139, the missions of the corps, the regular and paramilitary ... | `cal.1964-11.vietnam-saigon-2` |
| 96 | Nov. | Saigon. Riot control munitions used on rioting students, with success. | `cal.1964-11.vietnam-saigon-3` |
| 192 | Nov. 4 | Typhoon Iris hits central Vietnam: communications disrupted, crops destroyed. | `cal.1964-11-04.vietnam` |
| 159 | Nov. 7 | Khánh telephones Westmoreland for comment on draft decrees reorganizing the High Command. | `cal.1964-11-07.vietnam-saigon` |
| 159 | Nov. 8 | The decrees on the High Command, translated by 7:15 a.m. for Westmoreland, already ... | `cal.1964-11-08.vietnam-saigon` |
| 159 | Nov. 11 | The decrees withdrawn, revised on the American recommendations and reissued. | `cal.1964-11-11.vietnam-saigon` |
| 192 | Nov. 17 | The aid mission allocates flood relief supplies; Marine helicopters begin shuttling ... | `cal.1964-11-17.vietnam` |
| 192 | Nov. 21 | Định Tường. Thăng Long 27 takes Ba Dừa from the Viet Cong, killing 136. | `cal.1964-11-21.vietnam-operations` |
| 193 | Nov. 22 | Tây Ninh. Phong Hoài ends with the destruction of a Viet Cong base area and arms ... | `cal.1964-11-22.vietnam-operations` |
| 62 | Nov. 25 | MACV's J3 delivers the force structure study to CINCPAC and briefs his staff. | `cal.1964-11-25.vietnam-force-levels` |
| 62 | Nov. 29 | CINCPAC concurs in MACV's force increase, Alternative 1, to the Joint Chiefs. Their ... | `cal.1964-11-29.vietnam-force-levels` |
| 165 | Dec. | Bangkok. A SEATO conference on real estate for the Central Region's plan: essential ... | `cal.1964-12.vietnam-3` |
| 90 | Dec. | South Vietnam's High Command studies the IV Corps border plan and is briefed on it: it ... | `cal.1964-12.vietnam-4` |
| 66 | Dec. | The Mission Council approves the concept and definitions of pacification worked out by ... | `cal.1964-12.vietnam-5` |
| 193 | Dec. 5 | Kỳ's ultimatum to Khánh: support Prime Minister Hương or else; the air force on full ... | `cal.1964-12-05.vietnam-saigon` |
| 193 | Dec. 6 | IV Corps. Dân Chí 92: 138 Viet Cong killed. | `cal.1964-12-06.vietnam-operations` |
| 193 | Dec. 7 | The Viet Cong overrun a battalion command post on Hill 193 and threaten the An Lão ... | `cal.1964-12-07.vietnam-operations` |
| 193 | Dec. 9 | South Vietnamese forces retake Hill 193 and secure the An Lão subsector headquarters. | `cal.1964-12-09.vietnam-operations` |
| 193 | Dec. 9 | Quảng Tín. The Viet Cong attack the 3d Regiment's headquarters and artillery; the ... | `cal.1964-12-09.vietnam-operations-2` |
| 193 | Dec. 28 | Ba Xuyên. A South Vietnamese reaction force routs one to two of four hard-core Viet ... | `cal.1964-12-28.vietnam-operations-2` |
| 97 | Dec. 31 | MACV's chief of staff sends the Army the ACTIV weapons recommendations, asking review, ... | `cal.1964-12-31.vietnam` |

### Passed over

What is left after the rulings of Oct. 28.

| Page | Date | Event | Why |
|---|---|---|---|
| 189-93 | Jan. 14, 30; Mar. 8; May 12; June 20, 23; July 27; Aug. 2, 5, 16, 25, 27; Sept. 13-14, 18, 20; Oct. 20, 24; Nov. 1; Dec. 20, 24-25 | Westmoreland named deputy (the Jan. 27 entry's Check); Khánh's coup; McNamara's visits; Harkins leaves; Lodge resigns; the advisers; the Gulf of Tonkin; Khánh's presidency and the triumvirate; the coup of Sept. 13; the Montagnards; the charter; Sửu and Hương; Biên Hòa; the generals' coup; the Brink | already in, or in a pending patch (b3-westmoreland: May 12, June 20, Sept. 20) |
| 160-61 | Aug. 5 | The J5's outline plan against a surprise attack on Huế | a draft not sent: shelved, never forwarded to the High Command |
| 99-100 | July 30-Dec. 26; Nov. 14, 30 | JRATA's searchlight platoon, its equipment and training; booby-trapped munitions; the 25th Division's language students | an office's routine (test and evaluation) |
| 116-20; 156-57; 176-78 | year | Training; the evacuation plan's changes; the suggestion program; communications (the Mark IV terminal, Oct. 3; Wetwash, Jan. 1, 1965) | an office's routine |
| 64 | Dec. 17 | The RVNAF memorandum on the deficiencies Westmoreland listed (n.38), Khánh's order to the corps commanders | not yet entered: a dated paper for the next run |
| 102 | June 28; July 18; Aug. 1 | Big Squirt, the medium-wave transmitter near Huế | not yet entered: the pages not reread in this run |
| 96-97 | Aug.; Oct. 26 | Lazy Dog (MACV's request, CINCPAC's reply, the test) | not yet entered: the passage not found again by search in the OCR; the next run |

### Leads

- SEACOORD (the Southeast Asia Coordinating Committee): Taylor's proposal of September 1964 and Rusk's concurrence (History, 166-67, nn.61-63): look in FRUS 1964–68, I and XXVIII, for the day.
- The Command History's Annex A (special operations, MACVSOG), 1964, published separately: not in the copy read; Marolda cites it for the raids of July 30-31 (`cal.1964-08-02.vietnam`).
- When each volume was made public (its declassification): the pages carry regrading stamps ("20 NOV 1975"; "Order Sec Army By TAG per 830624"); the date not settled, so no "Made public:" line was written.

## 1965 (`w.macv-command-history-1965`)

The copy: 496 PDF pages, the History submitted Apr. 20, 1966, "regraded unclassified" page by page; its annex on special operations published separately and not in it. The printed page ("Page N of 482 Pages") is the PDF page less 14 throughout (checked on pp. 24, 41, 162, 222, 315, 479). Its text layer was usable; the footnote pages (313-17, 336, 342) and every figure, date and note number a ruling rests on were read off the page images. Chapters: the summary and the enemy (I, 1-21), the buildup and the forces (II, 22-...), plans and concept (III), operations (IV, 157-...), the footnotes after the text (313-...), the chronology (478-82). Patch: `inbox/2026-10-29-b3-macv-1965.yaml` (patch `b3-macv-1965`): 121 new entries, 16 edits.

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

- U.S. military strength in Vietnam at each month's end, 1965, as MACV's Table II-1 prints it (p. 269): Jan. 23,858; Feb. 24,937; Mar. 29,111; Apr. 36,021; May 51,728; June 59,921; July 81,422; Aug. 100,347; Sept. 132,297; Oct. 153,279; Nov. 169,571; Dec. 184,314 (Army 116,755, Navy with the Coast Guard 8,749, Marines 38,190, Air Force 20,620). The chronology: about 23,000 Jan. 1, about 184,000 Dec. 31 (478, 482). The table has no monthly strength "then".
- The enemy, MACV's holdings by month, Table I-2 (p. 268): total strength (combat, support, militia, political cadre) 93,000–113,000 in December 1964 and January 1965; 144,860–164,860 in April–May; 166,919–186,919 in July; 209,667 in August; 221,159 in October; 227,659 in November; 229,759 in December (combat 70,100; 19 regiments, 107 battalions; militia 103,573; political cadre 39,175). The table's MACV order of battle begins later (Dec. 1964 in its new format); these are the figures as MACV held them in 1965-66, a third vintage.
- Main force regiments, Nov. 21, 1965: 16 confirmed, 4 probable, 1 possible (p. 14).
- Infiltration in 1965: 26,188, 11,050 of them in North Vietnamese units, some 90 percent ethnic northerners (p. 14).
- RVNAF strength by month, 1965: charts only (Figures II-4 to II-7, pp. 293-96), no figures printed.

### New entries, and those the rulings of Oct. 28 called for

All in `inbox/2026-10-29-b3-macv-1965.yaml`: the first 22 from the reading, the rest (the chronology's dated events, the operations, incidents, arrivals, conferences and papers) by the owner's rulings of Oct. 28 and Oct. 28, late, rows first written here as "Passed over" and moved.

| Page | Date | Entry | Id |
|---|---|---|---|
| 478 | Jan. 22 | Saigon. Buddhists demonstrate against the government at the American Embassy. | `cal.1965-01-22.vietnam-saigon` |
| 478 | Jan. 25 | Huế. Martial law after serious disturbances. | `cal.1965-01-25.vietnam-saigon` |
| 478 | Feb. 8 | Johnson orders Hawk air defense missiles to South Vietnam. | `cal.1965-02-08.vietnam-force-levels` |
| 478 | Feb. 9 | Đà Nẵng. The first elements of the Marines' 1st Light Antiaircraft Missile Battalion ... | `cal.1965-02-09.vietnam-force-levels` |
| 478 | Feb. 9 | Khánh names Nguyễn Xuân Oánh acting prime minister. | `cal.1965-02-09.vietnam-saigon` |
| 37 | Feb. 11 | The Joint Chiefs recommend to McNamara a brigade of the 25th Infantry Division for ... | `cal.1965-02-11.vietnam-force-levels` |
| 12, 54, 149, 478 | Feb. 16 | Vũng Rô Bay, Phú Yên Province. A North Vietnamese ship found in a cove, about 100 tons ... | `cal.1965-02-16.vietnam-operations` |
| 478 | Feb. 19 | Jets used in the South for the first time: Air Force B-57s against the Viet Cong in ... | `cal.1965-02-19.vietnam-operations` |
| 478 | Feb. 19 | The last American government-sponsored dependents flown out of South Vietnam. | `cal.1965-02-19.vietnam-7` |
| 478 | Feb. 22 | Maj. Gen. Trần Văn Minh replaces Khánh as commander in chief of the armed forces. | `cal.1965-02-22.vietnam-saigon` |
| 478 | Feb. 25 | Some 600 Korean troops arrive in South Vietnam. | `cal.1965-02-25.japan-and-korea-korean-troops` |
| 54–55 | Mar. 3 | Saigon. MACV's planning conference on a combined American and South Vietnamese patrol ... | `cal.1965-03-03.vietnam-operations` |
| 38 | Mar. 7 | Saigon. MACV briefs the Army Chief of Staff, General Harold K. Johnson: three more ... | `cal.1965-03-07.vietnam-force-levels` |
| 38 | Mar. 10 | MACV's Enclave Study, by its planning staff: a series of well-defended areas with ... | `cal.1965-03-10.vietnam-force-levels` |
| 478 | Mar. 15 | Route 19, Qui Nhơn to Pleiku, reopened after almost two months without traffic. | `cal.1965-03-15.vietnam-operations` |
| 54–55 | Mar. 16 | The Joint Chiefs approve Market Time, a combined American and South Vietnamese patrol ... | `cal.1965-03-16.vietnam-operations` |
| 38, 478 | Mar. 19–21 | The 716th Military Police Battalion arrives, the first Army battalion-sized unit, for ... | `cal.1965-03-19.vietnam-force-levels` |
| 38 | Mar. 21 | Westmoreland to the Joint Chiefs, CINCPAC concurring: American combat troops must be ... | `cal.1965-03-21.vietnam-force-levels` |
| 478 | Mar. 21 | MACV publicly confirms that riot-control agents have been used in South Vietnam. | `cal.1965-03-21.vietnam` |
| 478 | Mar. 22 | American aircraft hit the first North Vietnamese radar site. | `cal.1965-03-22.vietnam-air-war` |
| 478 | Mar. 27 | Plei Do Lim Special Forces camp: some 30 Claymore-type mines detonated by accident, ... | `cal.1965-03-27.vietnam-operations` |
| 478 | Mar. 28 | The Seventh Fleet undertakes coastal surveillance off South Vietnam. | `cal.1965-03-28.vietnam-operations` |
| 39, 41, 98 | Mar. 30 | Westmoreland asks a field command headquarters to control the American and allied ... | `cal.1965-03-30.vietnam-force-levels` |
| 478 | Mar. 30 | Air Force planes strike the Đồng Hới airfield, the first North Vietnamese airfield hit. | `cal.1965-03-30.vietnam-air-war` |
| 55 | Apr. | After the Honolulu conference, McNamara approves buying 20 Swift patrol boats for the ... | `cal.1965-04.vietnam-operations` |
| 479 | Apr. 1 | The Army's 1st Logistical Command established in South Vietnam. | `cal.1965-04-01.vietnam-force-levels` |
| 479 | Apr. 4 | The first American planes shot down by MiGs over North Vietnam. | `cal.1965-04-04.vietnam-air-war` |
| 479 | Apr. 5 | The pacification program renamed Rural Reconstruction, under a new Central Rural ... | `cal.1965-04-05.vietnam-saigon` |
| 39 | Apr. 8–10 | Honolulu conference. CINCPAC recommends to the Joint Chiefs an Army division for the ... | `cal.1965-04-08.vietnam-force-levels` |
| 39 | Apr. 14 | The Joint Chiefs approve the 173d Airborne Brigade for temporary deployment from ... | `cal.1965-04-14.vietnam-force-levels` |
| 479 | Apr. 14 | South Vietnamese planes fly their first night attack mission over the North. | `cal.1965-04-14.vietnam-air-war` |
| 479 | Apr. 16 | The first North Vietnamese SAM site reported under construction near Hanoi. | `cal.1965-04-16.vietnam-air-war` |
| 220 | Apr. 28 | Kiến Hòa. After a month's bombing and psychological warfare, a South Vietnamese ... | `cal.1965-04-28.vietnam-operations` |
| 55 | Apr. 29 | A Coast Guard squadron of 17 patrol boats announced for Vietnam. | `cal.1965-04-29.vietnam-operations` |
| 55 | Apr. 30 | McNamara announces that the American forces of Market Time will come under ... | `cal.1965-04-30.vietnam-operations` |
| 479 | May 4 | A two-day halt of Rolling Thunder's armed reconnaissance and strikes over the North, ... | `cal.1965-05-04.vietnam-air-war` |
| 479 | May 5 | MACV's Political Warfare Advisory Directorate established. | `cal.1965-05-05.vietnam-3` |
| 479 | May 6 | The Armed Forces Council dissolves itself, voting confidence in Quát. | `cal.1965-05-06.vietnam-saigon` |
| 479 | May 7 | III Marine Amphibious Force activated, Maj. Gen. W. R. Collins commanding. | `cal.1965-05-07.vietnam-force-levels` |
| 220–21, 479 | May 11 | Sông Bé, capital of Phước Long Province. Some four Viet Cong battalions break into the ... | `cal.1965-05-11.vietnam-operations` |
| 479 | May 14 | The first ANGLICO units, the Marines' naval gunfire liaison, deployed in South Vietnam. | `cal.1965-05-14.vietnam-force-levels` |
| 479 | May 14 | The embassy announces the Joint U.S. Public Affairs Office (JUSPAO). | `cal.1965-05-14.vietnam-2` |
| 479 | May 16 | Biên Hòa air base rocked by a series of accidental explosions. | `cal.1965-05-16.vietnam-operations` |
| 479 | May 20 | The destroyer *Hamner* fires the Navy's first naval gunfire support mission in the South. | `cal.1965-05-20.vietnam-operations` |
| 479 | June 2 | The advance party of the 1st Battalion, Royal Australian Regiment, arrives. | `cal.1965-06-02.vietnam-force-levels` |
| 479 | June 4 | Brig. Gen. Lewis W. Walt takes command of III Marine Amphibious Force from Collins. | `cal.1965-06-04.vietnam-force-levels` |
| 479 | June 9 | Army combat engineers begin the base at Cam Ranh Bay. | `cal.1965-06-09.vietnam-force-levels` |
| 479 | June 11 | Quát resigns. | `cal.1965-06-11.vietnam-saigon` |
| 479 | June 14 | The generals form a National Leadership Committee under Thiệu. | `cal.1965-06-14.vietnam-saigon` |
| 479 | June 16 | Saigon. An explosive charge damages Tân Sơn Nhứt's civilian passenger terminal. | `cal.1965-06-16.vietnam-operations` |
| 479 | June 17 | The first MiGs shot down by Navy aircraft over North Vietnam. | `cal.1965-06-17.vietnam-air-war` |
| 480 | June 25 | Saigon. Viet Cong mines blast the Mỹ Cảnh floating restaurant. | `cal.1965-06-25.vietnam-operations` |
| 35, 41 | June 27 | Westmoreland's new forecast of requirements to the Joint Chiefs, beyond his request of ... | `cal.1965-06-27.vietnam-force-levels` |
| 480 | July 1 | The Viet Cong attack the Đà Nẵng and Sóc Trăng air bases. | `cal.1965-07-01.vietnam-operations` |
| 41 | July 2 | Westmoreland to CINCPAC on where the Army's combat units go: the 2d Brigade, 1st ... | `cal.1965-07-02.vietnam-force-levels` |
| 480 | July 7 | 8,000 more Marines land at Đà Nẵng and Qui Nhơn. | `cal.1965-07-07.vietnam-force-levels` |
| 226 | July 8 | Dầu Tiếng, Bình Dương. An outpost attacked by a platoon; the relief force, the 2d ... | `cal.1965-07-08.vietnam-operations` |
| 480 | July 9 | Sergeant First Class Isaac Camacho escapes after 20 months a Viet Cong prisoner. | `cal.1965-07-09.vietnam-prisoners` |
| 41, 480 | July 12 | The 2d Brigade, 1st Infantry Division, begins landing: a battalion at Cam Ranh Bay for ... | `cal.1965-07-12.vietnam-force-levels` |
| 480 | July 15 | MACV confirms the North Vietnamese 101st Regiment in South Vietnam. | `cal.1965-07-15.vietnam-order-of-battle` |
| 42 | July 16 | McNamara in Saigon. Westmoreland's concept: 44 maneuver battalions in 1965, from ... | `cal.1965-07-16.vietnam-force-levels` |
| 480 | July 16 | B-52s used in support of a ground operation for the first time. | `cal.1965-07-16.vietnam-operations` |
| 480 | July 20 | U.S. Army Support Command, Vietnam, becomes U.S. Army, Vietnam, Westmoreland its ... | `cal.1965-07-20.vietnam-force-levels` |
| 480 | July 20 | The first Coast Guard vessels to see action in a combat zone since the Second World ... | `cal.1965-07-20.vietnam-operations` |
| 480 | July 21 | A New Zealand field artillery battery arrives. | `cal.1965-07-21.vietnam-force-levels` |
| 162, 480 | July 28 | Liên Kết 4: Marines and South Vietnamese, a Vietnamese Marine battalion, a battalion ... | `cal.1965-07-28.vietnam-operations` |
| 41, 480 | July 29 | The 1st Brigade, 101st Airborne Division, lands at Cam Ranh Bay. | `cal.1965-07-29.vietnam-force-levels` |
| 480 | July 30 | Taylor leaves Saigon at the end of his tour. | `cal.1965-07-30.vietnam` |
| 480 | July 30 | Rural Reconstruction renamed Rural Construction, under a new Ministry of Rural ... | `cal.1965-07-30.vietnam-saigon` |
| 480 | July 30 | Operational control of the American coastal patrol, Market Time, passes from the ... | `cal.1965-07-30.vietnam-operations` |
| 98, 480 | Aug. 1 | Task Force Alpha activated, the first Army field force headquarters in South Vietnam, ... | `cal.1965-08-01.vietnam-force-levels` |
| 167, 480 | Aug. 1 | The battle at the Đức Cơ Special Forces camp, west of Pleiku, begins. | `cal.1965-08-01.vietnam-operations` |
| 41 | Aug. 2 | The 173d Airborne Brigade to stay in South Vietnam for good, not to be replaced by the ... | `cal.1965-08-02.vietnam-force-levels` |
| 42, 480 | Aug. 2 | Honolulu. Westmoreland and Sharp at the conference on the Phase I deployments. | `cal.1965-08-02.vietnam-force-levels-2` |
| 42–43 | Aug. 6 | CINCPAC's program for the Phase I deployment, from the Honolulu conference: the rest ... | `cal.1965-08-06.vietnam-force-levels` |
| 480 | Aug. 7 | The commander of III Marine Amphibious Force made senior adviser, I Corps, with ... | `cal.1965-08-07.vietnam-force-levels` |
| 480 | Aug. 9 | The South Vietnamese air force receives its first B-57s from the Air Force. | `cal.1965-08-09.vietnam-force-levels` |
| 480 | Aug. 14 | The 7th Marines, reinforced, begin landing at Đà Nẵng and Chu Lai. | `cal.1965-08-14.vietnam-force-levels` |
| 480 | Aug. 20 | Lodge arrives in Saigon to begin his second tour. | `cal.1965-08-20.vietnam` |
| 162–63 | Aug. 21 | Starlite ends. MACV's count, some 700 of the enemy killed; an attack on Chu Lai ... | `cal.1965-08-21.vietnam-operations` |
| 481 | Aug. 24 | A Viet Cong mortar attack hits Biên Hòa air base. | `cal.1965-08-24.vietnam-operations` |
| 481 | Aug. 31 | Military Payment Certificates replace American currency in South Vietnam. | `cal.1965-08-31.vietnam` |
| 163, 481 | Sept. 7–11 | Piranha, a four-day operation on the Batangan peninsula, 20 miles south of Chu Lai, on ... | `cal.1965-09-07.vietnam-operations` |
| 481 | Sept. 11 | Darlac. A group of Montagnards disarmed, in the government's move against FULRO. | `cal.1965-09-11.vietnam-2` |
| 44, 481 | Sept. 12 | The first elements of the 1st Cavalry Division (Airmobile) land at Qui Nhơn. | `cal.1965-09-12.vietnam-force-levels` |
| 481 | Sept. 15 | Ban Mê Thuột. A group of Montagnards reaffirms its loyalty to the government in a ... | `cal.1965-09-15.vietnam-2` |
| 167–68 | Sept. 18–19 | Gibraltar, northeast of An Khê, in Highland, the 1st Brigade, 101st Airborne's opening ... | `cal.1965-09-18.vietnam-operations` |
| 43–44 | Sept. 18 | Westmoreland's Phase II force requirements, after the conference in Saigon: two more ... | `cal.1965-09-18.vietnam-force-levels` |
| 7, 223 | Sept. 23–29 | Phù Cũ pass, Bình Định Province. The Viet Cong overrun the post, Sept. 23; the South ... | `cal.1965-09-23.vietnam-operations` |
| 42, 481 | Sept. 25 | Task Force Alpha becomes Field Force, Vietnam, with operational control of the II ... | `cal.1965-09-25.vietnam-force-levels` |
| 481 | Sept. 28 | Honolulu. Sharp and Westmoreland in conference. | `cal.1965-09-28.vietnam-force-levels` |
| 36 | Sept. 30 | Walt's estimate for Westmoreland: two Marine divisions and their air the optimum for ... | `cal.1965-09-30.vietnam-force-levels` |
| 44 | Oct. 7 | CINCPAC's program for Phase II, from its conference: the 4th Infantry Division for II ... | `cal.1965-10-07.vietnam-force-levels` |
| 44, 481 | Oct. 7 | The rest of the 1st Infantry Division arrives at Vũng Tàu. | `cal.1965-10-07.vietnam-force-levels-2` |
| 481 | Oct. 8 | The first elements of the Korean Capital Division land at Cam Ranh Bay. | `cal.1965-10-08.japan-and-korea-korean-troops` |
| 481 | Oct. 17 | Navy jets destroy the first mobile SAM site in North Vietnam. | `cal.1965-10-17.vietnam-air-war` |
| 481 | Oct. 21 | The commander of Field Force, Vietnam, made senior adviser, II Corps. | `cal.1965-10-21.vietnam-force-levels` |
| 481 | Oct. 27 | The Viet Cong attack the Marines' air installations at Đà Nẵng and Chu Lai. | `cal.1965-10-27.vietnam-operations` |
| 168, 481 | Nov. 1 | Silver Bayonet, the 1st Cavalry Division's first offensive mission: its 1st Brigade, ... | `cal.1965-11-01.vietnam-operations` |
| 481 | Nov. 1 | The commander of the 1st Infantry Division takes operational control of all Army units ... | `cal.1965-11-01.vietnam-force-levels` |
| 481 | Nov. 2 | The air base at Cam Ranh Bay operational for tactical jets. | `cal.1965-11-02.vietnam-force-levels` |
| 481 | Nov. 2 | Lt. Gen. John L. Throckmorton, Westmoreland's deputy, leaves Vietnam. | `cal.1965-11-02.vietnam-2` |
| 481 | Nov. 6 | Lt. Gen. J. A. Heintges replaces Throckmorton as deputy commander, MACV. | `cal.1965-11-06.vietnam` |
| 481 | Nov. 7 | MACV publicly confirms five North Vietnamese regiments in South Vietnam. | `cal.1965-11-07.vietnam-order-of-battle` |
| 170–71 | Nov. 8 | War Zone D, Hump, the 173d Airborne Brigade's fifth operation there. The 1st ... | `cal.1965-11-08.vietnam-operations` |
| 481 | Nov. 10 | Blue Marlin: American and South Vietnamese Marines, the first combined amphibious ... | `cal.1965-11-10.vietnam-operations` |
| 169 | Nov. 18–26 | Thắng Phong 7: three battalions of the South Vietnamese Airborne Brigade west of ... | `cal.1965-11-18.vietnam-operations` |
| 14, 44 | Nov. 21 | Westmoreland to CINCPAC: captured documents and prisoners show far larger enemy forces ... | `cal.1965-11-21.vietnam-order-of-battle` |
| 481 | Nov. 22 | The Viet Cong mortar the Sóc Trăng airfield. | `cal.1965-11-22.vietnam-operations` |
| 8, 224–26 | Nov. 27 | Michelin plantation, Bình Dương Province. A reinforced Viet Cong regiment overruns the ... | `cal.1965-11-27.vietnam-operations` |
| 481 | Nov. 27 | The Viet Cong release two American prisoners, Smith and McClure, in Cambodia. | `cal.1965-11-27.vietnam-prisoners` |
| 482 | Dec. 1 | The commander of the 1st Infantry Division made senior adviser, III Corps, with ... | `cal.1965-12-01.vietnam-force-levels` |
| 482 | Dec. 2 | The carrier *Enterprise* enters combat, its sorties against Viet Cong targets in the ... | `cal.1965-12-02.vietnam-operations` |
| 482 | Dec. 4 | Saigon. Terrorists bomb the Metropole, an American enlisted men's billet. | `cal.1965-12-04.vietnam-operations` |
| 226 | Dec. 6 | Near Củ Chi, Hậu Nghĩa. The 2d Battalion, 49th Regiment, 25th Division, ambushed on ... | `cal.1965-12-06.vietnam-operations` |
| 482 | Dec. 10 | Honolulu. Sharp and Westmoreland in conference. | `cal.1965-12-10.vietnam-force-levels` |
| 36, 45 | Dec. 11 | The Secretary of Defense approves Westmoreland's request after the Saigon briefings of ... | `cal.1965-12-11.vietnam-force-levels` |
| 226 | Dec. 16 | The same battalion ambushed again on the road from Củ Chi to Phước Hiệp, fire from 50 ... | `cal.1965-12-16.vietnam-operations` |
| 482 | Dec. 18 | FULRO briefly seizes the Quảng Đức provincial headquarters at Gia Nghĩa. | `cal.1965-12-18.vietnam` |
| 36 | Dec. 20 | The 2d Air Division asked whether it can take on III MAF's need of ten fighter ... | `cal.1965-12-20.vietnam-force-levels` |
| 45 | Dec. 29 | The 3d Brigade, 25th Infantry Division, flown from Hawaii to Pleiku, begins arriving: ... | `cal.1965-12-29.vietnam-force-levels` |

### Passed over

| Page | Date | Event | Why |
|---|---|---|---|
| 478, 482 | Jan. 1; Dec. 31 | American strength about 23,000; about 184,000 | figures, for the war table (above) |
| 478-82 | Jan. 27; Feb. 7, 10, 16, 27; Mar. 2, 8, 30; Apr. 9, 20; May 13, 18; June 10, 18, 19, 27; July 8, 24, 27, 28; Aug. 18; Oct. 19; Nov. 14, 28; Dec. 8, 15, 24 | Khánh and Hương; Pleiku; Qui Nhơn; Quát named (the Feb. 16 entry, a Check on Feb. 15); the white paper; Rolling Thunder; the Marines; the embassy; the Hainan fight; Honolulu; the pauses; Đồng Xoài; the first B-52s; Kỳ; War Zone D; Taylor and Lodge; the first SAM loss and the SAM strikes; the July decision; Starlite; Plei Me; Ia Drang; McNamara in Saigon; Harvest Moon; Uông Bí; the Christmas truce | already in, or in a pending patch (b3-westmoreland: June 27) |
| 42 | July 14 | Memo, SECDEF Saigon trip, items for discussion | a meeting's preparation; the briefing is entered (July 16) |
| 12-13; 164-65 | year | The infiltration routes and the 70th Transportation Group; the Marines' patrols and the enclaves' growth | dated to the year only: leads |

### Leads

- The command's organization, 1965: the 1st Logistical Command (Apr. 1), III MAF (May 7), USARV (July 20), Task Force Alpha (Aug. 1) and Field Force, Vietnam (Sept. 25): the History's chronology (479-81) and ch. II; whether the calendar should hold the command's structure as it holds the MACV–MAAG merger of 1964.
- MACV's public confirmation of North Vietnamese units: the 101st Regiment (July 15), five regiments (Nov. 7): the History's chronology only; the press releases (MACOI) and the *New York Times* of the next days.
- The Honolulu conferences of Sept. 28 and Dec. 10 (Sharp and Westmoreland): chronology only; FRUS 1964–68, III.
- The Marble Mountain and Chu Lai attacks of Oct. 27: chronology only.
- The 1966 volume (the DMZ, Attleboro, Masher, Crimp) was not among the copies: a Sources to Fetch item.


# Second run (Nov. 3-4, 2026): the 1967 and 1968 volumes

The batch-3 reader resumed (notes/briefs/batch3-resume.md). The 1964 and 1965 volumes were not reopened in this run: their leftovers (1964: the RVNAF memorandum of Dec. 17, Big Squirt, Lazy Dog; 1965: the chapters beyond those read) stand as listed above, for the next. No patch for them was written (`-1964-2`, `-1965-2` not made). The owner's copies were fetched through Drive's public download address (no sharing changed), into the scratchpad, each deleted when its volume was done, with its page images and text. Read by each copy's text layer (DTIC's OCR), its dated paragraphs extracted a chapter at a time; where the layer was garbled (the 1968 chronology) the page images were read by tesseract 5 (installed for the run); figures and dates a ruling rests on read off the page image (the pages named under each volume).

Patches: `inbox/2026-11-03-b3-macv-1967-2.yaml` (338 new entries; 16 cites, 5 claim-map rows and 3 Checks on entries in the tree) and `inbox/2026-11-03-b3-macv-1968-2.yaml` (76 new entries; 4 cites, 2 Checks). Both pass `./bib patch-check` (0 errors; the warnings are same-day, same-thread entries, distinct events, R17). Merged together into a scratch copy of the tree and checked there: 0 errors of their own; 76 same-day flags, each read, all distinct but four, which became cites (the Kép airfield, Apr. 24, 1967; the Tet truce, Jan. 29, 1968; Khe Sanh's abandonment announced, June 27, 1968; the rockets on Saigon, Aug. 22, 1968). Cards added to `works/m.yaml`: `w.macv-command-history-1967` (3 vols., 1968) and `w.macv-command-history-1968` (2 vols., 1969; the year of printing not read off the copy, Check).

Witnesses (R35): for the 1967 volume, the notes of the pages cited in Chs. III, IV and V (the force decisions, the strategy, the ground, air and naval operations) registered: 178 new witnesses in `inbox/witnesses/2026-11-03-b3-macv-1967-2.yaml` (the messages, memoranda, letters, MONEVALs, SITREPs, plans and studies, each as the note gives it, its DTG read for the date; OCR's garbles of "Msg" and "COMUSMACV" normalized, other garbles left and marked), 179 edges in `sources/witnesses/by-work/macv-command-history-1967.yaml`; the via rows in the entries' maps. One existing witness taken (Westmoreland's "Force Requirements," Mar. 18, 1967). Not registered: the notes of the 1967 volume's Chs. II, III (RVNAF, advisers, Free World), VI-XII and the annexes, and all of the 1968 volume's: those entries cite the text alone, the notes a task for the next run. None of the witnesses is held or read here (MACV's message files are not open).

## 1967 (`w.macv-command-history-1967`)

- Part 1 (PDF 575 pp., vol. I, pp. 1-558): printed page = PDF page - 16 to p. 357, - 17 from p. 357 (PDF 374); text layer usable (DTIC's OCR).
- Ch. I (1-12) read whole; Ch. III "United States Forces" 135-66 read (dated paragraphs, and 143-48 whole); Ch. IV 307-45 read (dated paragraphs; 336-38 whole).
- Ch. V (349-558): ground (352-98), air (399-460), naval (461-505) read by their dated paragraphs; the page image checked on p. 357 (the copy carries it twice; 14,228 helicopter sorties). Ch. II (13-120) and Ch. III's RVNAF, advisory and Free World sections (167-306) read by their dated paragraphs. Notes registered as witnesses for the pages cited in Chs. III-V (by-work file); the notes of Ch. II and of Ch. III's later sections (pp. 167-306) not registered, their entries citing the text alone.

### Rulings other than "holds" (the cites already made, and the records set against the History)

| Entry | The calendar / the record | The History | Ruling |
|---|---|---|---|
| `cal.1967-01-26.vietnam-operations` | Cedar Falls, nearly 750 of the enemy dead | 720 (387; the chronology, 1256) | Check |
| `cal.1967-12.vietnam-operations` | Westmoreland ends Fairfax (December) | the 199th ends it Dec. 14 (385) | Check |
| `cal.1967-07-06.vietnam` | Nguyễn Chí Thanh dies of a sudden illness | Hanoi's broadcast of July 8, a heart attack; a notebook, killed in action; a report, wounded in an air strike (45) | Check |
| `cal.1967-05-14.vietnam-operations` | Junction City's totals | 2,728 killed, 282 friendly (389-90) | cited for B-D |
| `cal.1967-03-18.vietnam` | the request of Mar. 18 | the optimum and minimum forces in men (143-44) | cited for B-C, via n.17 |
| new `nha-trang-conf` (Apr. 2) | | the text, 141, Apr. 3; 376 and the note's memorandum, Apr. 2 | dated Apr. 2, Check |
| new `pd-9-67` (Oct. 20) | | the text Oct. 20, the note Oct. 29 | Check |
| new `pershing-dec16` (Dec. 15) | | the text Dec. 16, the note's message Dec. 15 | dated by the message, Check |
| new `pce08` (May 8) | | 466, May 8; 505, May 15 | Check |
| new `coronado` (June 4) | | 395, June 4; 483, June 1 | Check |
| new `bien-hoa-122` (May 12) | | 999, May 12; 417, May 13 | Check |
| new `da-nang-jul` (July 15) | | 996, July 13; 79 and 1006, July 15 | Check |
| new `11th-bde-qui-nhon` | | the port changed to Qui Nhơn, yet "arrived at Da Nang" (153) | Check |

Page images checked: p. 357 (the copy carries it twice; Prairie's 14,228 helicopter sorties), p. 970 (the White House statement on prisoners, July 17), pp. 1057-58 (the Tet bonus, 700 million piasters; the 1968 defense budget, 62.6 and 17.5 billion), p. 1076 (Practice Nine's highest priority, Jan. 13).

### New entries

338, a few of the chief: the force decisions (the Army ceiling, Mar. 31; the second airmobile division; the 101st's and the 11th Brigade's deployments; Task Force Oregon, Apr. 12, and the Americal, Sept. 22; Wheeler's analysis, Mar. 22; Sharp on Course A, May 12; Program 5 approved, Oct. 5; the Korean helicopters, Nov. 7); the strategy papers (Westmoreland's concept of Aug. 26 and Oct. 13, 1966; Sharp's of Sept. 28, 1966; AB 142 and AB 143; the command guidance of Jan. 24; Planning Directives 3-67 and 9-67; Southpaw and High Port; the reorientation of Sept. 28; the DMZ memorandum to Bunker, Oct. 4); the year's named operations, their starts, battle days and ends, in every corps, the Korean and riverine ones among them; the air war's decisions (the B-52 rates, U Tapao, the Haiphong prohibited area, the SLAMs, the Shock operations in Laos, Làng Vây's bombing in error, Mar. 2); the naval war (the gunboats and cutters, Sea Dragon extended, the first minefield, Feb. 26); the RVNAF's force structure and the allies' (the Canberras, Holt's 1,700, the Thai regiment, the Korean light division); pacification (CORDS, May 28; Bunker's announcement, May 11; Takeoff; the attack on the infrastructure, June 16); the prisoners (the White House statement, July 17; the releases); the barrier (Practice Nine to Dye Marker); the chronology's year (the Bolo battle, Jan. 2; Bernard Fall killed, Feb. 21; the elections; the strikes; Percy under fire, Dec. 11).

### Passed over

How the list was made: each chapter's dated paragraphs read in turn; what was not entered is a row, by page.

| Page | Date | Event | Why |
|---|---|---|---|
| 137 | 1967 | countermortar radars: USARV to review trade-offs for ten of the 90 radar detachments deferred | no date given (a lead: the note's messages, Apr. 25-Aug. 8) |
| 139-40 | June 27 | USARV's request for more long-range artillery; the tubes allocated by corps | minor: an allocation; the passage only partly read |
| 148 | Oct. 18 | MACV Force Development Conference discusses the civilianization schedule | minor: a meeting's routine |
| 149 | Nov. 8 | CINCPAC asked to put the need for construction and O&M funds to the JCS and OSD | minor: a repetition (entered Sept. 29) |
| 153 | Sept.; Oct. 14 | the smoke generator platoon for Dye Marker from Korea; the 62d Chemical Company alerted | lead: entered later if the barrier annex dates it |
| 155-56 | Aug.; Nov. 16; Dec. 9-20 | the Army's program to standardize units' organization; a DA team's visit | minor: an office's routine |
| 158-59 | Dec. 20 | long-range patrol units assigned to divisions and brigades | minor: an assignment table |
| 162 | Apr. | a gasoline barge for NAVSUPPACT Saigon; the Game Warden helicopter squadron activated | minor: a unit's routine |
| 164-66 | Jan.-Mar. | Seventh Air Force's aircraft and strength by month; the aircraft types introduced; the C-130s at Da Nang (CINCPAC, Mar. 22) | figures (in the book-check's war-table section); Mar. 22 minor |
| 160 | early 1967 | the Marines' and the Vietnamese Marines' command relationship, "coordination and control" | no date given |
| 98 | mid-July | the North Vietnamese 152mm howitzers and long-range guns on the Marines near the DMZ | entered (July 5, the first 152mm) |
| 102 | Sept. 13; Nov. 9 | COSVN's double-agent school in Cambodia (a report); an enemy document captured on the reconnaissance of an American advisers' command post | a lead (a report's date "on or about"); minor (a document's capture) |
| 109-11 | June-Aug.; Dec. 20 | the strikes on the northern rail lines; the year's vehicles, rolling stock and watercraft destroyed or damaged (5,261; 2,475; 11,425); SAM sites 151 to 270 | figures (for the war table) |
| 82 | Nov. 13; Jan. 1968 | the enemy's District Coordination and Operation Committee to begin by Nov. 13, agents in Saigon by late January (a captured plan) | a lead: the document's own date not given |
| 170-80 | Feb. 21; May; Aug. 2; Aug. 26; June 7 | unit messes; the commissary negotiations; the JGS leave directive; Westmoreland on veterans' priorities; the post-hostilities study filed | minor (an office's routine), but Aug. 26 a lead for the next run |
| 181-83 | Dec. 13, 1966; Aug. 23 | Kỳ's decree making the Military Academy four years; Westmoreland visits it | not entered: a lead for the next run |
| 193 | Mar. 3 | Westmoreland's reply on the general reserve battalions' employment | not entered: a lead for the next run |
| 196-200 | July; July 26-Aug. 4; July 12; June | ARVN 2/1 Battalion kills 146 in Quảng Trị; the 7th Division's 234; Reserve Officer Candidate classes; the 9th Division's captains | not entered: leads for the next run |
| 206 | Feb.; May 3; Oct. 15; Oct. 24 | the Vietnamese Marines in the Rừng Sát; a Vietnamese Marine officer to command; the battalion ashore in IV Corps; the 105mm battery | not entered: leads |
| 211-15 | Feb. 25; Mar. 11; Mar. 18; Oct. 16 | the VNAF helicopter program; RF officer shortage; RF/PF allocations | minor (an office's routine) |
| 223-44 | Apr. 26; Aug. 17; Nov. 6; June 3 | advisory spaces; VNAF strength accounting; RD refresher training; the IG advisers | minor (an office's routine) |
| 248-79 | Jan. 3; Aug.; Nov. 29; Nov. | the Australian conference; PHILCAG II volunteers at Fort Magsaysay; the Thai division's training and deployment targets (Jan. 22 and July 15, 1968); the embassy at Manila on engineer battalions | Jan. 3 entered within Apr. 19; the rest leads for the next run |
| 360-98 | many | each named operation's monthly progress between its start and end (Pershing's months; Fairfax's months, May 15, 20, 24; Shelby, Aug. 17; Ala Moana's later months; Coronado III, VI, VII, VIII; Malheur II) | entered where the History gives a start, a battle day or an end; the monthly summaries passed over as a unit's routine |
| 399-460 | Jan.-Dec. | the air chapter's planning factors, sortie rates and Muscle Shoals helicopter planning (Nov. 20; Dec. 6, 21); the base-defense measures (early August); the airlift for Oregon and Greeley | minor (an office's routine) or figures |
| 461-505 | Jan.-Dec. | Market Time's and Game Warden's month-by-month incidents (Jan. 1 Soài Rạp; May sappers and swimmers; June 13, 15); the Cửa Việt suspension, Nov. 30; the VNN schools, July 24 | a unit's routine the History does not treat as an event, except where entered |

## 1968 (`w.macv-command-history-1968`)

- Part 1 (PDF 676 pp., vol. I, pp. 1-568): the copy carries pp. 1-102 twice, PDF 19-120 a first, partial run (printed = PDF - 18), PDF 121-676 the whole volume (printed = PDF - 118 to p. 93, - 119 to p. 348, - 111 from p. 356, - 110 from p. 442, - 108 from p. 457; the folios read from the bare page numbers, the OCR's Z for 2). Read: Ch. II (the strategy, 5-36) and Ch. IV's United States forces (223-48) by their dated paragraphs; Ch. V's ground operations (371-401) by their dated paragraphs. Not read: Ch. III (the enemy, 37-216, the Tet and May offensives as MACV saw them), Ch. IV's RVNAF and Free World sections (249-370), Ch. V's air (402-40) and naval (441-518) operations, Ch. VI (pacification, 519-68). Notes not registered as witnesses (the entries cite the text).
- Part 2 (PDF 560 pp., vol. II, pp. 569-1120): printed page = PDF page + 559, + 560 from PDF 219. Read: the chronology (1025-66) whole, from tesseract's OCR of every page (the text layer unreadable), the day of an item read off the page image where the OCR lost it (pp. 1026, 1038, 1048, 1053); Annex C (the Office of Information and the press, 935-96) only skimmed in its garbled text layer, nothing entered from it. Not read: Chs. VII-XII (intelligence, PSYOP, logistics, R&D, contingency plans and studies, special problems), Annexes A (Tet in retrospect), B (the barrier), D, E.

### Rulings other than "holds"

| Entry | The calendar | The History | Ruling |
|---|---|---|---|
| `cal.1968-03-16.vietnam` | Sơn Mỹ: Task Force Barker reports 128 of the enemy killed | the chronology records the day as the task force's search-and-destroy operation 9 km NE of Quảng Ngãi city, 128 enemy killed, 6 weapons; friendly 2 killed, 10 wounded (1038, read off the page image) | cited for A, E |
| `cal.1968-01-29.vietnam-tet` | the Saigon announcement not made, the press office closed | Saigon's statement released at noon, Westmoreland concurring (376) | Check |
| `cal.1968-01-08.vietnam` | Bowles in Phnom Penh, Jan. 8-12 | arrives Jan. 10 (1026) | Check |
| `cal.1968-06-27.vietnam` | Check the day of the announcement | under June 27 (1051) | cited |

### New entries

76: the strategy and force papers (York I cancelled; Westmoreland's guidance of Feb. 4; his revised request of Mar. 31; Program 6, Apr. 6; the 27th Marines and the 82d's brigade ordered, Feb. 13; the 101st made airmobile), the year's operations not yet in, and the chronology's (the casualty-withholding policy, Feb. 26; "search and destroy" dropped, Apr. 12; censorship lifted, May 30; Carroll's accreditation, July 27; LeMay's visit, Oct. 16; the Tet totals, Feb. 29; Khe Sanh's resupply, Apr. 8; the province chiefs dismissed, Mar. 11).

### Passed over

| Page | Date | Event | Why |
|---|---|---|---|
| 5-36 | Jan. 1968; Mar. 31; Aug. 19; Nov. 1; mid-Aug. and Sept. 1967 | the State of the Union and Johnson's speeches quoted; the strategy of 1967 retold | already in |
| 374-76 | Nov. 1; Jan. | the bombing halt's terms; the Tet truce debate | already in (the halt), or entered (Jan. 29) |
| 378-401 | many | the other operations and battles of the year in each corps (Jeb Stuart's months, Lancaster II and Kentucky, Allen Brook, Mameluke Thrust, Burlington Trail, Maui Peak, Meade River, Lê Lợi; Patrick, Walker, Bolling, Maeng Ho 9, Byrd; Coburg, San Angelo, Saratoga, Wilderness, Toàn Thắng's battles of Aug. 18-19, 27-29, Sept. 5-8, 11, 12, 16, Oct. 6; the convoy ambush of Dec. 17; Coronado IX's end, Hop Tac I, Quyết Chiến's battles) | not entered in this run: leads, each with its page |
| 1025-66 | many | the chronology's other items: the daily attacks by fire and ground attacks with their losses; the visits (Chapman, Beach, Sharp, McCain, Hyland, Nazzaro, Resor, Ignatius, Moorer, Foster, Weaver); the appointments (Eckhardt, Brownfield, Pearson, Baker, Corcoran, Forbes, Mildren, McLaughlin, Goodpaster, Momyer's departure, Wetherill, Schaefer, Cole, Clay, Townsend, Timothy); the records and firsts (the 786th plane lost; the IL-28; the first 120mm and 107mm rockets in new areas; the first F-111A losses; the O-1V Bronco; the first ASPB lost); the Paris talks' sessions; Kham Duc; Hương's government; the bombing halt; Speedy Express; the releases of prisoners (May, Aug. 2, Dec.); Cambodia's seizures of the *Bream* and the LCU | not entered in this run (most already in the calendar or minor by R18 as a unit's routine); the rest leads, each with its page |
| 935-96 | Feb. 9; Feb. 19; Mar. 4; Mar. 7; Apr. 12; Apr. 19; May 6; Sept. 30 | the press annex: the *Christian Science Monitor* on the press and the military; the *Washington Post*'s photographs, "A Drink of Water--Then Death"; Westmoreland on a *Los Angeles Times* article; 649 accredited correspondents; the casualty-reporting change recommended to Sharp; Delaware embargoed; the "pep talk"; the *Tampa Tribune*'s editorial | a lead: the text layer garbled, the pages to be read off the images |

## The press (Nov. 3-4)

1967-10-07 | CBS | — | the soldier's attempt at Lai Khê, filmed by John Smith for Don Webster (the incident) | 965 1967-10-09 | CBS Evening News | broadcast | Webster's ear-cutting report; Sevareid's comment | 965 1967-10 | Newsweek | article | "Their Lions--Our Rabbits," on the South Vietnamese army | 961 1967-11-14 | UPI | wire | Hochmuth's death, against the embargo | 963 1967-11-28 | UPI | wire | Alvin B. Webb Jr.: McConnell on bombing in Laos | 965 1967-11-28 | New York Times | story | Westmoreland said to recommend Walt as Commandant | 965 1967-10-10 | Saigon Daily News | front page | the northeast monsoon's arrival | 362
- Part 2 (PDF 518 pp., vol. II, pp. 559-1068): printed page = PDF page + 549 throughout. Chs. VI (pacification), VII (PSYOP), VIII (logistics), X (morale, discipline, press, prisoners, security), XI (J5 studies), XII (economy) read by their dated paragraphs, Ch. VIII and VII by a keyword skim of them; Ch. IX (R&D) skimmed. Page images checked: p. 970 (the White House statement of July 17), pp. 1057-58 (the Tet bonus, 700 million piasters; the 1968 defense budget, 62.6 and 17.5 billion). Notes of vol. II not registered as witnesses (the entries cite the text).
| 564-76 | July 12, 1966; Dec. 31, 1966; Nov. 7 and 21, 1966; Sept. 1966; Dec. 13, 1966; Dec. 29, 1966 | Thắng made Commissioner General of RD; the Ministry reorganized; MACV's RD Support Directorate; Lodge announces the Office of Civil Operations; the HES approved; the sector security directive | already in, or 1966 matters the 1966 volume treats: leads for its reader |
| 569-70 | 1965 | the pacification councils and plans of 1965 (AB 139-141) | history before the year; leads |
| 595 | early July | Westmoreland launches Project Takeoff | within the entry of May 8 |
| 600-26 | mid-June; June-Dec. | the ten high-impact actions; the refugee and police programs' months; the detention facilities | minor (an office's routine), the figures for the next run |
| 643, 646, 680-92 | July 5; May; 1966-67 | the PSYOP study; the semiannual appraisals; the Chiêu Hồi campaigns' figures | minor (an office's routine) |
| 669-72 | May 30, 1966; 1967 | the saga of Nguyễn Văn Bé, the NLF hero Hanoi's press had mourned, shown alive in his hamlet | a lead: the day of his return not read (the passage garbled in the text layer) |
| 710-60 | Jan.-Dec. | the supply system's months, the POL tankage, the munitions lists (Mar. 6), the Beehive round (April), property disposal, the highway program, the ports' waiting ships | minor (an office's routine), figures |
| 731-38 | Jan. 10; Jan. 18; May 31; Aug. 16; Sept. 2 | the M16's issue: USARV on rescinding the suspension; CINCPAC on the Koreans' rifles; Westmoreland's field comments; the Koreans' excess weapons; 5,000 more for the RVNAF | leads for the next run (the M16 entered Feb. 21, Mar. 10, Apr. 27) |
| 789-98 | July 17; Jan. 9; June | the Saigon dial exchange; the 24th Evacuation Hospital at Long Bình; the hospital ship *Sanctuary* | minor |
| 897-958 | 1967 | morale and welfare, R&R, discipline and crime | not read beyond a skim: a lead for the next run |
| 984-93 | Jan. 31; Apr. 22; May; Aug. 23; April | the camps' construction; the work advisory detachment; the press's visit to two camps | minor; the press visit a lead (the day) |
| 1024-29 | 1967 | J5's studies: Crystal Ball (firearms, internal security), the casualties after a bombing halt, the force at negotiations, a token withdrawal, operations in Cambodia, US forces into Laos, Cambodian rice | undated in the text: leads (the notes' dates) |
| 1039-62 | mid-Oct.; Dec. 30; Sept. 7-8; Jan. 31; Feb. 25; Apr. 6; June 30 | the Fall Stabilization Review; the embassy on piaster rates; the piaster workshop; the defense budget's steps; the military banking facilities (Chase Manhattan at Long Bình) | minor (an office's routine), but the Dec. 30 cable a lead |
- Part 3 (PDF 281 pp., vol. III, pp. 1069-1340): printed page = PDF page + 1059 throughout. Annex K (the command chronology, 1255-85) read whole; Annex A (the barrier, 1069-1114) by its dated paragraphs; Annex F (visitors, 1199-1201) read, its tables (1202-06) not legible in the text layer. Page image checked: p. 1076 (Johnson's approval of Practice Nine, Jan. 13). Annexes B (civilian casualties), C (Montagnards), D (international political developments and the constitution), E, H, I (the list of operations), J not read: the next run.
| 1255-85 | many | the chronology's other items: the operations launched with their losses (Seine, Ma Doo I, Sierra, Farragut, Desoto, Independence, Gadsden, Lanikai, Chinook II, Kitty Hawk, Prairie III, Newcastle, Adams, Le Jeune, Oh Jac Kyo II, Manhattan, Shawnee, Crockett, Barking Sands, Thunder Dragon, Hop Tac, Billings, Malheur II, Fremont, Ardmore, Coronado II/Song Thang III, Pike, Cochise, Coronado IV, Swift, Dragon Fire, Wheeler, Coronado V, Bolling, Shenandoah II, Santa Fe I, Strike/Uniontown, Klamath Falls, Camden); the commanders' changes (Peers, Tolson, Hay, Palmer, Davidson, Darrow, Davis, Knowlton, Lathram, Forsythe, House, Bolton, Momyer's promotion); the firsts and records (sorties, the O-2, the A-37, Gunship II, the Cobra, the A-7A, the containership *Bienville*, the PACVs, Sydney as an R&R center); the visits (Greene, Harold Johnson, Bradley, Taylor, Sharp, Humphrey, the Lodge observers) | not entered in this run: leads, each with its day and page (1255-85), for the next |
| 1199-1201 | Apr. 26; May 26 | MACV Directive 1-5 on official visits; CINCPAC's country-clearance message | minor (an office's routine); the Schwengel-Cowger delegation's complaint a lead (no date) |
1968-02-26 | MACV | announcement | casualties and damage to be withheld when the tactical situation dictates | 1035 1968-04-12 | MACV | announcement | "search and destroy" dropped | 1043 1968-05-30 | Saigon | decree | all press censorship lifted | 1048 1968-07-27 | MACV | announcement | John S. Carroll of the *Baltimore Sun*, accreditation revoked six months | 1053

## Leads (Nov. 3-4)

National
- Annex C of the 1968 volume (the Office of Information and the press, pp. 935-96): its dated incidents (above), to be read off the page images. The 1967 volume's "Press and Public Opinion," 959-69: the Washington meeting on public support (no date given); Westmoreland's instruction that TV crews be escorted (no date given).
- Propose Part III entries for the press figures named here without one: Don Webster (CBS), Osborn Elliott (*Newsweek*), John S. Carroll (*Baltimore Sun*), Alvin B. Webb Jr. (UPI); the History treats each.
- The congressional delegation of Schwengel and Cowger and its complaint to the press (1967 vol., 1201): no date given.

Foreign
- The 1967 volume's J5 studies (1024-29), undated in the text: Crystal Ball, the casualties after a bombing halt, a token withdrawal, operations in Cambodia, American forces into Laos, Cambodian rice; their dates in the notes.
- The saga of Nguyễn Văn Bé (1967 vol., 669-72): the day of his return to his hamlet.
- The 1967 volume's Annexes B (civilian casualties), C (the Montagnards), D (international political developments and the constitution), I (the list of operations); the 1968 volume's Annexes A (Tet in retrospect) and B (the barrier) and its Chs. III, VI-XII: not read.
- Kỳ's decree making the Military Academy a four-year school, Dec. 13, 1966 (1967 vol., 181); Westmoreland's reply on the general reserve battalions, Mar. 3, 1967 (193).
- The 1966 volume (still not among the copies).

The Executive roster
- MACV's staff and commanders by date, from the chronologies (1967, 1255-85; 1968, 1025-66) and the 1967 volume's Annex H (1207): the J-staff and field commanders' changes, not in the roster.


# Third run (Nov. 4, 2026): the 1964 and 1965 volumes again

The batch-3 reader "macv", second run of the 1964 and 1965 volumes (notes/briefs/batch3-resume.md; the rules of notes/briefs/reader.md, R14, R18, R35-R44, R48 especially). The owner's copies fetched through Drive's public download address (no sharing changed), one at a time into the scratchpad, each deleted with its page images and text when done. Patches: `inbox/2026-11-03-b3-macv-1964-2.yaml` (134 new entries; 3 cites, 11 `src` and 11 `to-check` ops, 1 Check, on entries in the tree) and `inbox/2026-11-03-b3-macv-1965-2.yaml` (126 new entries; 11 cites, 5 `src`, 4 `to-check`, 5 Checks). Both pass `./bib patch-check` (0 errors; the warnings are all "one event?" flags, every one read against its day's entries in the tree and the ledger: distinct events). `./bib check`: 0 errors. Ids claimed in the ledger before writing (patches `b3-macv-1964-2`, `b3-macv-1965-2`).

Witnesses (R35): 93 new rows in `inbox/witnesses/2026-11-03-b3-macv-1964-2.yaml`, 87 in `inbox/witnesses/2026-11-03-b3-macv-1965-2.yaml` (messages, letters, memoranda, studies, directives, plans, MONEVALs, Westmoreland's "Historical Briefings" of 1965, his Honolulu notebook, staff conference notes, one press item: the *Saigon Daily News* of Nov. 26, 1965), each as the History's note gives it, its DTG read for the date; their edges appended to `sources/witnesses/by-work/macv-command-history-1964.yaml` and `-1965.yaml` (under a dated comment). Two registered witnesses taken rather than repeated: Westmoreland to Wheeler, MAC 1190 (`x.1965-03-06.westmoreland-to- wheeler-mac-1190`, at 38 n.49) and MAC 3320 (`x.1965-06-30.westmoreland-to-wheeler-mac-3320`, at 41 n.74), both the Westmoreland reader's. Registered for the first run's entries that had none: 1964, Apr. 6 (23 n.33), Oct. 20 (24 n.37), Feb. 22 (65 n.40), AB 139 (65 n.41), the definitions (66 n.42), Aug. 24 (177 n.6), Sept. 1 (101 n.129), SEACOORD (166 nn.61-62), the three SEATO conferences (140 nn.21-23, with the page cited); 1965, Mar. 6 (38 n.49), the Commander's Estimate (39 n.58), June 24 (40 nn.70-72, 41 nn.73-74), War Zone D, June 27 (167 n.17), the combined command (101 n.462). Not registered: the notes of the first run's other chapter pages whose note numbers the copies' OCR did not show (1964: pp. 47, 57, 61-62, 66, 89-91, 96, 155, 159-62, 165-67; 1965: pp. 38 (Mar. 7, 19), 41-44 (the arrivals), 55 (Apr. 29), 98, 162-68 (Starlite, Piranha, Gibraltar, Silver Bayonet)), nor the 1965 chronology (no notes). None of the witnesses is held or read here; MACV's message files are not open.

## 1964 (`w.macv-command-history-1964`), second reading

The copy again (209 PDF pages; printed page = PDF page - 10, checked on the page image of p. 156). Its own OCR layer is poor: every page read again by tesseract 5 at 200 dpi (one thread a job). Read: the leftovers named above (pp. 64, 87-88 for Lazy Dog, 99-103 for JRATA and Big Squirt), every page the first run's Passed over had ruled "an office's routine" (116-20, 156-57, 173-79), and every page no entry cited (pp. 16-22, 26-30, 39-46, 48, 52-55, 60, 63, 67-88, 93, 104-06, 114-15, 135-49, 168-69), by their dated paragraphs; the notes of every chapter (36-38, 50-51, 129-34, 152-54, 170-72,
181) whole. Page images checked: p. 87 (Lazy Dog: MACV's request "in August 1964," CINCPAC's approval "on 26 September"), p. 132 (nn. 87-94), p. 156 (the evacuation plan, n.2).

### Rulings other than "holds"

| Entry | The calendar / the record | The History | Ruling |
|---|---|---|---|
| new Lazy Dog, Aug. (`lazy1`) | | MACV's request "in August 1964" (87); its note 93, a message of 260341Z Sep 64 | dated August; Check |
| new Mar. 16 (`housing1`) | | the letter to Khánh "on 16 March" (28); n.63, Ser 753, 31 Mar 64 | dated Mar. 16; Check |
| new Aug. 16 (`phil`) | | 16 Philippine officers, Aug. 16 (77); "16 doctors, nurses, technicians and civic action officers," Aug. 17 (157) | Check |
| new June 11 (`nzagree`) / `cal.1964-06-29.vietnam-force-levels` | the chronology, June 29 | July 8 (157); the 1965 volume, July 20, 1964 (71) | Check on the tree's entry (by the 1965 patch) |
| new Sept. 15 (`secplan`) | | the plan published "15 September" (157); n.3, OPLAN 61-64, 25 Sep 64 | Check |
| new July (`tanks`) | | the OCR reads "July 1966" in a 1964 paragraph | July 1964; Check |
| new Jan. (`j2reorg`) | | the OCR reads "January 1965" in a paragraph on 1964 | January 1964; Check |

### New entries

134, among them: the personnel (MACV's MPs, the dependents' policy, the decorations bill, the Murday Report, the RVNAF pay raises of Feb. 15, Mar. 2, May 1, July 1 and November, dependent housing, the WAC, Bob Hope at the Brink); the reports and assessments (the SAME, the Province Reports Center, Directive 335-10, the military assessments for Taylor); pacification and psywar (the realistic goals of Nov. 11, Hop Tac's report of Oct. 24, the civic action study, Chiêu Hồi, the bounty program, the General Political Warfare Department and the Chinese advisers, television for Vietnam, the rural water program and the Seabees); air support (Directive 95-2, the Strike Command air request system, the VNAF Air Request Net, Directive 95-6, Falcon Flight, Local Base Rescue, Lazy Dog, door gunners); security (Big Squirt, the STRATCOM site at Phú Lâm, Saigon's port, An Khánh, the *Muskingum*, Đà Nẵng's harbor, the Brink committee); the RVNAF's force structure and training (artillery, the M41s, the Rangers, the mortars, the Regional and Popular Forces, the sect companies, the Armed Combat Youth); the Free World's first contingents (State's circular of May 2, New Zealand, Australia's Caribous, the Philippines, Korea); logistics and communications (the Chu Lai briefing, the air base study, port advisers, POL barges, revetment, the Mark IV terminal, Wetwash, Southern Toll, PRC-10s); intelligence (the Laos target list of Aug. 24, Chiêu Hồi's commissioner, the collection plan, the PW directive, TRAC).

### Passed over (1964, second reading)

Each dated paragraph of the pages read, not entered, a row. The first run's rows of 64, 96-102, 116-20, 156-57 and 176-78 are ruled again here: the RVNAF memorandum (Dec. 17), Big Squirt, Lazy Dog, JRATA's projects, the evacuation and suggestion programs and the communications entered; what is left is below.

| Page | Date | Event | Why |
|---|---|---|---|
| 17 | May; Jan. 1965 | the 60-hour work week at MACV, a 70-hour week to come | minor: a headquarters' routine |
| 18 | Dec. | special procedures for colonels' assignments | minor: an office's routine |
| 18-22 | Feb.-Dec. | the exchanges and quarters; new APOs (Huế, Quảng Ngãi, Kon Tum, Bạc Liêu, Vĩnh Long); daily mail from November; 26 chaplains; Red Cross offices at Nha Trang and Cần Thơ; the Dalat retreats (Nov.); Aid-in-Kind funds for Special Services (Sept.); the Tân Sơn Nhứt theater (Sept.); R&R flights to Japan and the Philippines dropped (Apr.), the Nha Trang R&R facility (Sept.); the library; the USO; the pools (Aug.) | minor: personnel services, a command's routine |
| 22 | Feb.; Dec. | the sports program stopped after the Pershing Field bombing; its reopening planned | minor (the bombing entered, Feb. 9) |
| 26 | Oct. | the combined US-GVN study of RVNAF promotions | a lead: no day; the regulation not issued in 1964 |
| 27 | Apr.; Oct. 1 | the interpreter program turned over to ARVN | minor: an office's routine |
| 30 | Sept.; Oct.; Nov. 25 | G1 advisers re-authorized at division; the personnel advisory study; the new strength report forms | minor: an office's routine |
| 39 | Dec. | the sector intelligence centers' warnings before Bình Giã and Đại Ngãi | within those battles' entries; a lead to cite the History there |
| 40-41 | May; Aug.; Sept.; fall; Dec. | J2's reorganization, its Indications Center; the Counterintelligence Advisory Committee | minor: an office's routine |
| 43-44 | Jan.; Feb.; May; July | the MIC interrogator course; the documents library; the Cây Mai intelligence school's construction | minor: an office's routine |
| 52-54 | Jan. 1; Oct. 15 | J3's branches merged; the reporting working group disbanded | minor: an office's routine |
| 67 | May; Aug.; Nov.; Dec. | the advisers' pacification course | minor: a training routine |
| 69 | Nov. 17 | the South Vietnamese psywar directorate's proposal to put 32 million piasters into housing | minor: a budget's routine |
| 71 | Oct. 11; Nov. | the psyops officers' course and their arrival | minor: a training routine |
| 75-76 | Feb.; Mar. 25; Dec. | printing sets, Tri-Lambrettas, loudspeakers, the 1964-65 calendars | minor: supply routine |
| 85 | Aug.; Sept. | the UTT Helicopter Company redesignated the 68th Aviation Company; the reallocation directive | minor: a unit's routine |
| 99 | Aug. 12 | ACTIV told no searchlight platoons are active in the United States | minor: a staff exchange |
| 100 | Nov. 12, 23; Dec. 23 | the searchlight platoon's equipment drawn, its training, its demonstration | within the entries of Nov. 9 and Dec. 26 |
| 104 | Dec. 18 | infrared devices for Phú Lâm's towers | minor: supply routine |
| 106 | Nov. 19; Dec. 11 | the CINCPACFLT team's arrival at Đà Nẵng and its report | within the entry of Nov. 2 |
| 114 | Oct. | the airfields' responsibilities changed when "the 25th Division" moved into a corps zone | a lead: the unit garbled in the OCR |
| 116-20 | Jan.; Mar.; Apr.; July; Sept.; Oct.; Nov.; Dec. | the recruit and AIT programs revised; the Ranger battalions' training done (Oct.); infantry battalion training cut; the mortar and armor conversions' training; the RF/PF programs of instruction; the PF training centers' consolidation proposed (Oct.); the RF/PF adviser's recommendation (Dec.) | minor: training routine |
| 137 | Aug. | MACV's coordinated purchasing agency | minor: an office's routine |
| 140 | Aug. | the master planning boards and the facilities review board | minor; no day |
| 143-46 | year; Sept. 1; spring | the LST, airlift and POL figures; the petroleum laboratory; tires | figures (in n of the entries where used); minor |
| 147 | Oct. 29 | the vehicle committee's recommendations | minor: supply routine |
| 148-49 | Jan.-Dec.; Sept.; Oct. | the RVNAF Central Purchasing Office; MAP property reports reinstated; the redistribution directive | minor: an office's routine |
| 174-75 | July; Aug.; Oct. 8; June 10; Sept. | the committees' redesignation and Vietnamese counterpart (within Apr.); MACV's two communication centers combined; CINCPAC's ruling on local telephone service; J6's Navy and Air Force advisers | minor: an office's routine |
| 176 | June 15; Nov.; Dec. 24-26 | Armed Forces Radio's surveys; its studio after the Brink | minor |
| 178 | — | Northern Toll, the proposed microwave system north of Saigon | no date: a lead |
| 179 | 1964 | the aircraft radio retrofit completed | dated to the year only: a lead |
| 160-61 | Aug. 5 | the J5's outline plan against a surprise attack on Huế | a draft not sent (as ruled before) |

## 1965 (`w.macv-command-history-1965`), second reading

The copy again (496 PDF pages; printed page = PDF page - 14; the text layer used, the notes parsed by number from it). Read: Ch. II from p. 57 (the RVN forces, the advisory program, command and control, logistics, 57-136), Ch. III (137-60), Ch. IV's naval and in-country air sections and the B-52 strikes (172-98) and pacification, psyops and civic action (227-56): 57-103 by every dated paragraph, 104-256 by the paragraphs dated to a day (so a paragraph dated only to a month there is not yet read). Notes parsed for Chs. II-IV (315-345).

### Rulings other than "holds"

| Entry | The calendar | The History | Ruling |
|---|---|---|---|
| `cal.1965-03-06.vietnam` (Johnson to Ball) | carries the History, 37-38, with the parenthetical on Westmoreland's answer to the JCS and a row `w.macv-command-history-1965 37–38: all` | the passage is Westmoreland's MAC 1190 | the first run's row for the Westmoreland entry, applied by the merger to the wrong entry of the day: cited on `cal.1965-03-06.vietnam-2` (A, C; via 38 n.49). For the merger, by hand on base 3b5e9a0e (patch-check refuses a dropped cite): take `[[w.macv-command-history-1965]], 37–38 (...)` and its row out of `cal.1965-03-06.vietnam` |
| `cal.1965-06-24.vietnam-force-levels` | MAC 3240 | n.74, MAC 3320, "24 Jun 65" | Check: FRUS 1964–68, III, doc. 31, gives MAC 3320 June 30 |
| `cal.1965-10-17.vietnam-air-war` | Navy jets destroy the first mobile SAM site (chronology, 481) | the *Oriskany*'s A-4s, "in early November," "another first" (180) | Check |
| `cal.1965-09-28.vietnam-force-levels` | Honolulu, Sharp and Westmoreland | the conference Sept. 27-Oct. 1: combat forces to be accepted "even though logistical support would be marginal" (117) | cited; Check |
| `cal.1965-04.vietnam` | Westmoreland, Thiệu and Minh on a combined command (Westmoreland's memoir) | the conference Apr. 28 (101; MFR of that day) | cited for A, C; Check: the day |
| new `div10b` | | the Joint Chiefs' approval "on 9 June" (60); n.191, 191928Z Jun 65 | Check |
| new `depair` | | the JCS created it "on 14 May" (93); n.402, 092159Z May 65 | Check |
| new `crcc` | | "131 December" (244), "11 December" (247) | dated Dec. 11; Check |

### New entries

126: the RVNAF's force structure (Alternative 1 approved Jan. 23, Alternative 2, the requests of Nov. 5, the 10th Division, the PF recruiting bans of Jan. 6 and July 2 and their relaxing, the CIDG's conversion, the VNAF's squadrons and jets, the VNN's mutiny of April and the Marines made a service, May 1); the Free World's arrangements (Australia, May 5, Sept. 7 and 30; New Zealand, June 9; Korea, Feb. 8, Mar. 16, Sept. 6, Nov. 8; the Chinese C-46s; the Thais; MACV's Free World office, Dec. 22, 1964); command (Throckmorton as deputy, the air deputy, McChristian, the Army component dispute, USARV and the field forces, the combined command concept of Mar. 21, MACTHAI's separation, the Combat Operations Center, encadrement refused); the advisory program (Special Forces as subsector teams, the A detachments of July 19, the advisory letter and study of September, Directive 10-11); logistics (the logistical command, Gibson's group, Cam Ranh Bay, the Naval Support Activity, HSAS's phase-out, the ammunition officer, Red Ball, LSTs and Alaska Barge, the Traffic Management Agency, Chu Lai's land, Tuy Hòa, military aid for 1967, Saigon's defense budgets, the construction czar, MACV's new headquarters); plans (OPLAN 60-64's Change 4, OPLAN 37-65, Annex X, the Three-Month propaganda plans, AB 140 and AB 141, the security directives); the naval war (boarding, naval gunfire's procedures); the air war (the jets of January, Apr. 15, the F-104s, July 10, the air power board, Directive 95-2 of Dec. 20, the B-52s from the JCS's proposal of Mar. 4 to the Silver Bayonet strikes, 800 sorties a month, Harvest Moon; Alsop's column); pacification (the Mission Council of Jan. 20, Apr. 2, Apr. 10, the province team test, Hop Tac's extension and its reviews of Sept. 11 and 22, Ứng's death, the revolving fund, Nha Trang, Oct. 24, Thắng's 1966 plan, CRCC 1535, the economic warfare directive).

### Passed over (1965, the pages read)

| Page | Date | Event | Why |
|---|---|---|---|
| 57 | Feb.-May 1966 | the PBRs and their support ships planned | plans for 1966; a lead (their arrival) |
| 61 | July | the Regional Force cut to 134,999, the Railway Security Group to ARVN | minor: an accounting change |
| 65 | Apr.; May | the last T-28 and UH-19 out of the VNAF | within the May entry (`vnaf5`) |
| 68-69 | Mar.; May; Sept. 29; Dec. | An Thới occupied; the Guam team's ship inspection; CHNAVGP's delivery schedule; the repair facility | within `lssl`; minor: a navy's routine |
| 70 | Sept. | the Vietnamese Marines' five-year plan | a lead: not finalized in 1965 |
| 74-76 | Apr. 6; May 1; Mar. 15; May 14; Aug. 12; Sept. 14; Nov. 10, 15; Dec. 2, 22 | the changes to MACV's joint table of distribution | minor: an office's routine |
| 77-78 | Mar.; June 16; Nov. 27; Mar. 7; June 28; Sept. 10; Aug. 24 | the subsector skills survey and pilot augmentation; the 5th SFG's TOE changes | minor: an office's routine |
| 83-84 | Jan. 28; Aug. 1; Nov. 13; Dec. 18 | the Air Force Advisory Group's new teams; the OSI course | minor |
| 86-90 | Jan.; Apr.; May | the naval and Marine advisory units' strength | minor |
| 93-95 | Feb.; Mar.; early Apr.; Jan. 4; Apr. 26; May 1; Oct. 1 | joint representation on MACV's staff; Youngdale's succession (July 13 entered); the Training Directorate; DAML into the J4; the Free World office renamed (within Dec. 22, 1964) | minor |
| 96-97 | Apr.; June | Westmoreland's tailored corps concept; his repeated opposition to an Army component command | a lead (Apr.); a repetition (June) |
| 100-01 | mid-Mar.; early Apr.; Apr. 12; late Sept. | the Washington meeting on combined command; Collins kept; MAC 2029; the naval component study (entered) | a lead (mid-March); within `cal.1965-04.vietnam` |
| 102 | Mar. | Westmoreland's dissent on separating MACTHAI | within May 27 |
| 105-07 | Mar. 29; Apr. 18; May; Sept.; early July | the 1st Logistical Command's general order; CINCPAC's supply assignments; the 2d Signal Group; the 18th Engineer Brigade | within `cal.1965-04-01.vietnam-force-levels` and July 13; leads (the Signal Group, the Brigade: no day) |
| 111 | Sept. 1; Nov. 1 | clothing issued in kind | minor |
| 115 | Nov. 19 | the Secretary of the Army's direction (the copy's text cut) | a lead |
| 116 | Sept. 22 | III MAF's own Red Ball | minor |
| 117 | Aug.; Sept. 1-10; early Oct.; early Dec. | the Phase I and II troop lists | within the tree's entries of Aug. 2, Sept. 18, Oct. 7, Dec. 10 |
| 118 | Oct. 30; Nov. 24 | ships waiting at Cam Ranh Bay and Saigon; the Traffic Management chief's words | within `lsts`; minor |
| 125 | Apr. | $37 million reprogrammed for construction | a lead: no day |
| 128 | Oct. | the coastal survey team on Tuy Hòa | within Dec. 1 |
| 129-31 | Nov. 29, Dec. 2, 22, 1964; Sept. 10, 27; Oct. 5, 7; Nov. 20, 24 | the military aid program's steps | minor: a budget's routine, except those entered |
| 132 | Mar. 6; Sept. 11; Jan. 17, 1966 | guidelines for Saigon's defense budgets; the 1966 budget approved | minor; a lead (Jan. 17, 1966) |
| 134 | May 1; July | the J4's reorganizations | minor |
| 137-41 | July 21, 28; Aug. 18-21, 30 | the July decision, Starlite, the concept of operations | in the tree |
| 159 | early Jan.; Sept. | OPLAN 61-64's change; OPLAN 60-65 | minor |
| 160 | Sept. 10 | JSOP-71's Annex J | within `jsop71` |
| 179-80 | June 1; Feb.; Dec. 22 | the ANGLICO detachments; the Seventh Fleet's air; Uông Bí | in the tree |
| 183-86 | Feb. 7, 10, 19; May 11, 29; June 10, 18; July 1; Aug. 24; Oct. 25 | Pleiku, Qui Nhơn, the coup, Sông Bé, Ba Gia, Đồng Xoài, the first B-52s, the attacks on the air bases, Plei Me | in the tree |
| 188 | mid-Sept. | the Chairman's "special strike zones" for "free strike zones" | a lead: the day |
| 197 | Nov. 2-4, 7, 12-14, 26-28 | Arc Light strikes by province | minor: a unit's routine missions (the month's figures in `b52dec`) |
| 235 | July | McNamara briefed on population control, 45.9 percent | within the tree's entry of July 16 |
| 247-48 | Oct. 6 | Directive 335-10 revised | minor |
| 256 | Oct.-Dec.; Nov. 8, 24 | the civic action staff's visits and letters | minor |

### Where this run stopped

1965: not yet read: Ch. I, pp. 22-27 (the Montagnards, the press and the home front, the decisions); Ch. IV, pp. 199-219 (Rolling Thunder, Yankee Team, Barrel Roll, Steel Tiger, Tiger Hound) and 227 (the VNMC's operations, but June 18); Ch. V (257-66); the tables (267-312); Annexes A-M (347-477: the Montagnards, Free World assistance, communications, inter-agency relations, ports, base development, J5's studies, physical security, prisoners, morale, new weapons, political warfare, intelligence); and, on pp. 104-256, the paragraphs dated only to a month. The 1964 volume is read through but for the tables (31-35) and the appendixes' rosters (185-88). The 1966 volume is still not among the copies.

## The press (Nov. 4)

1965-09-24 | Joseph Alsop's column | column | the B-52s in South Vietnam, the press "favorably impressed" | 1965 vol., 193 1965-11-26 | *Saigon Daily News* | story | the Republic of China's two C-46s for the VNAF | 1965 vol., 73 n.285

## Leads (Nov. 4)

National
- Westmoreland's "Historical Briefings" (1965: Sept. 4, Oct. 3, 25, 31, Nov. 21) and his Honolulu notebook (Apr. 18, Aug. 20, 1965), cited by the 1965 volume's notes: whether CMH or the LBJ Library holds them open.
- Bob Hope's Christmas tour of 1964 (1964 vol., 20): the troupe's stops; the press.

Foreign
- SEACOORD (1964 vol., 166-67, nn.61-64): Saigon 870 (Sept. 16), 913 (Sept. 19), State 727 (Sept. 25), Saigon 1080 (Oct. 10), 1415 (Nov. 6), 1964: not in the daybook's FRUS; the State files.
- The television plan for South Vietnam (1964 vol., 76-77, 176): the Mission's TV subcommittee; its 1965 sequel.
- The 1964 volume: the sector intelligence centers before Bình Giã and Đại Ngãi (39); the airfields' change "when the 25th Division" moved (114); Northern Toll (178); the radio retrofit (179); the RVNAF promotion study (26).
- The 1965 volume: the PBRs' arrival (57); the Vietnamese Marines' five-year plan (70); the tailored corps concept, April (96); the Washington meeting on combined command, mid-March (100); the 2d Signal Group and the 18th Engineer Brigade (106); the Secretary of the Army's direction of Nov. 19 (115); the April reprogramming (125); "special strike zones" (188); Saigon's 1966 defense budget approved Jan. 17, 1966 (132).
- The *Muskingum* at Đà Nẵng, Oct. 30, 1964: what happened (the History has only CINCPACFLT's question).

# Third run (Nov. 4, 2026): the 1968 volume, the parts left unread

The batch-3 reader "macv" again (notes/briefs/batch3-resume.md), on the 1968 volume only (`w.macv-command-history-1968`). Patch: `inbox/2026-11-03-b3-macv-1968-3.yaml` (163 ops: 128 new entries, claimed in the ledger as b3-macv-1968-3; 35 additive ops on entries in the tree or pending: cites, Checks, the to-check and `src` rows of the notes). New witnesses: `inbox/witnesses/2026-11-03-b3-macv-1968-3.yaml` (78, each a note's message, report, letter, briefing or article as the note gives it, the DTG read for the date, OCR's garbles of the digits and of "Msg" normalized, a lost subject marked); the volume's edges, `sources/witnesses/by-work/macv-command-history-1968.yaml` (81). None held or read; MACV's files are not open here. `./bib patch-check`: 0 errors (the warnings are same-day, same-thread entries, distinct events, R17). `./bib check`: 0 errors.

The copies: Part 1 as the second run gives it (the offsets above; PDF 467 is p. 356: pp. 348-55, the Free World forces' section, are not in the copy). Part 2, printed = PDF + 559 to PDF 218, + 560 from PDF 219. Part 1 read by its text layer (DTIC's OCR, usable), the page image looked at for p. 50; Part 2's layer garbled throughout, so its pages read were OCR'd by tesseract 5 from the page images at 170 dpi (pp. 777-996). The notes are at each chapter's end; a note's pin is written as the text page its number stands on ("41 n.7"), as in the 1967 file (the second run's two of 1968 kept their form, "34 n.18"). Both copies deleted.

Read in this run:
- Part 1, Ch. III (the enemy, 37-199) by its dated paragraphs: Hanoi's leaders and statements, North Vietnam, the bloc's aid, the infrastructure and the Alliance, morale, the weapons, the enemy's offensives and the attacks corps by corps.
- Ch. IV, the RVNAF (249-344) by its dated paragraphs (the Free World section is missing from the copy).
- Ch. V's air (402-40) and naval (441-500) operations; Ch. VI (pacification, 519-64) by its dated sentences.
- Part 2: Ch. XI (contingency plans and studies, 777-95); Ch. XII's prisoners of war (841-59); Annex B (the barrier, 911-31); Annex C (the press, 935-92), whole.
- The notes for the second run's entries on pp. 24-35 and 225-47 where the note could be told (seven entries: their edges and `via` rows added by additive op); the rest of that patch's entries (Ch. V's ground pages, 380-401) not registered: their note numbers could not be told reliably in the text layer.

Where I stopped: not read in this run, for the next: Part 2's Chs. VII (intelligence, 569-), VIII, IX (logistics, -742), X (research and development, 743-76), XII's other sections (morale and welfare, R&R, the USO, security, MACONOMY: 799-840, 860-80), Annex A (Tet in retrospect, 882-910), Annexes D and E; the Free World section (Part 1, 348-55, not in the copy). Ch. VI's and Ch. XI's notes are mostly op. cit. chains to the chapter's first notes (the pacification messages to CINCPAC; J-5's monthly histories): not registered, their entries citing the text alone.

### Rulings other than "holds"

| Entry | The calendar | The History | Ruling |
|---|---|---|---|
| `cal.1968-01-31.vietnam-tet` | thirty-six province capitals and five of six autonomous cities | 27 of 44 province capitals, 5 of 6 cities, 58 of 245 district towns, Jan. 30-31; 32,000 killed, Jan. 29-Feb. 11 (129, 131) | cited for A, C; Check |
| `cal.1968-02-24.vietnam` | Huế retaken, the flag raised Feb. 24 | the enemy ejected from the Citadel Feb. 25 (157) | Check |
| `cal.1968-03.vietnam-khe-sanh` | single management, "Check: the day" | the directive Mar. 10, first missions Mar. 22, in effect about Apr. 1 (437) | cited; Check |
| `cal.1968-01.vietnam-khe-sanh` | the sensors shifted to Khe Sanh, "Check: the day" | diverted Jan. 19, first emplaced Jan. 21 (922) | cited; Check |
| `cal.1968-12-19.vietnam` | the LCU entered Cambodian waters July 17; "Check the day of release" | July 16; released Dec. 20, the last man Jan. 6 (849) | cited; Check |
| `cal.1968-10.vietnam-prisoners` (pending) | Mighty Yankee, October, "Check: the day" | Oct. 21 (856) | cited; Check |
| new `cal.1968-09-22.vietnam-operations` | | 91 of the enemy killed at Hậu Đức (163) and "over 200" in the summary (163) | Check |
| new `cal.1968-06-18.vietnam-may-offensive` | | the defection June 18, 119 confirmed (83); "140 odd" on June 4 (550) | Check |
| new `cal.1968-02-11.vietnam-tet-2` | | Trần Độ killed Feb. 11 (73), by MACV's account | Check |

Held: Lang Vei, the first armor (114); the third offensive the night of Aug. 17 (134); Meade River (165); Commando Hunt from Nov. 15 (411); Carroll (966-68); the release of Mar. 29 (854).

### New entries

128, by chapter: Hanoi's and its allies' word and acts (Hồ's appeals of July 20 and Nov. 3, Đồng's National Day speech, Xuân Thủy and Hà Văn Lâu at Paris, the decree on counterrevolutionary crimes, the aid agreements at Budapest, Moscow and Peking, Chen Yi, Peking's first notice of Paris, the Chinese troops' withdrawal reported); the Alliance of National, Democratic and Peace Forces (its forming, announcement, Moscow's recognition, Saigon's death sentences, the NLF's coalition with it), the Liberation Committees, the NLF's delegation at Paris; the enemy's directives and the third offensive called off; notable attacks (Jan. 2, May 28, June 11, Sept. 18, Sept. 22, Nov. 15, Nov. 17); the RVNAF's improvement and modernization (Thiệu's mobilization, Nitze's directive of Apr. 16, the 850,000 ceiling, Phase II and its acceleration), the draft, desertion; the air war (Arc Light's rates, the 45 B-52s of Jan. 30, Turnpike, Thor, the end of Rolling Thunder); the naval war (the four trawlers of Mar. 1, the friendly fire off Cap Lay, Clearwater, the twelfth Seabee battalion); pacification (Phụng Hoàng's decree and SOP, the surtax, war-risk insurance, the self-defense committee, the 1969 guidelines); the J-5's plans (El Paso, Pacific Grove, Vesuvius, Sauna Scrub, Điện Biên Phủ and Khe Sanh, T-Day, the cease-fire planning); the prisoners (the releases of Jan. 29-Feb. 16, Mar. 31, July 3-Aug. 2, Nov. 25, Dec. 19-25; the *Bream*; the LCU; Rowe; Saigon's release of 140; the seven seamen); the barrier (Duel Blade halted, closed out, Duel Blade II; Duck Blind); the press (20 entries: the *Monitor*, the *Post*'s photographs, the Marines and the press, the ground rules, Alsop's break of the Delaware embargo, Musgrove, the "pep talk," the combined briefings, the casualty-reporting proposal, Deepe, Crawford).

### Passed over

How the list was made: each chapter's dated paragraphs (Part 1) or dated sentences (Part 2) read in turn, page by page; what was not entered is a row.

| Page | Date | Event | Why |
|---|---|---|---|
| 40 | Nov. 3 | the NLF's statement of Nov. 3, quoted from the Liberation Press Agency | a lead: quoted in passing, the statement's own text not read |
| 43 | 1968 | Nguyễn Thành Lê's briefings in Paris: the United States to recognize the NLF | no day given (in the note of Aug. 28) |
| 46-50 | 1968 | conditions in North Vietnam: an indoctrination session's notes, the reconstruction study, the committee of 34 consultants, the census | no day given |
| 50 | Sept. 14 | Haiphong's ship congestion at its record level; 38 cargo ships, about 28 by mid-November | figures (an observation); a lead for the war table |
| 52 | 1968 | Hanoi asks Moscow to double its flour shipments; 22,000 metric tons a month | no day given |
| 52-53 | 1965; Dec. 1967 | Chinese troops at Đồ Sơn; a captured colonel's statements on the Chinese | before the year, or no day given; leads |
| 59 | Jan.-Dec. | the infiltration estimates by month (136,229 Jan. 1-Oct. 31) | figures: the war table carries infiltration |
| 73 | Jan. 30 | the Qui Nhơn city committee's secretary and assistant secretary killed in the attack | within the Tet attacks (in the calendar); a lead |
| 79-80 | Oct. | Đinh Bá Thi with a joint NLF and North Vietnamese delegation in France; the NLF's officials' biographies | no day given; biographies |
| 83-84 | Sept. 8; Oct. 22; Nov. 6-12 | interrogations, an agent report and a notebook on the enemy's morale | minor: a repetition of the morale entries (Sept. 5) |
| 88-89 | May; Sept. 28; Dec. 31 | the draft age raised to 33; a rallier and a prisoner; the enemy's strength at the year's end (259,000) | no day given; minor; figures (the war table carries enemy strength) |
| 106-119 | Jan.-Dec. | the weapons and munitions first found or used: the 120mm mortar cache (Jan. 3-6), the 152mm dud at Khe Sanh (Jan. 24), long-delay fuzes (Jan. 23), the first 130mm component at Đông Hà (Mar. 6), 70mm howitzers at Tam Kỳ (Mar. 5), the 140mm DKB rocket (Jan. 31), the 107mm launcher (Sept. 15), tanks near Tây Ninh (Feb. 26), the Tri-Border tanks (Nov. 6), new grenades (Oct. 3), 57mm guns in the Laotian panhandle (Mar. 17), the missile near Khe Sanh (Apr. 1), CS gas (Feb. 7, 19, 26), the first limpet mine (Mar. 14), the PM-60 mine (May 16), water mines (Sept. 3, Oct. 3, Nov. 19) | not entered in this run: leads, each with its page |
| 114 | Jan. 24 | the Royal Lao BV 33 outpost overrun by the 325C Division, its men fleeing to Lang Vei | a lead: likely in the Khe Sanh thread's days; not checked |
| 119-21 | Jan.-Oct. | the enemy's radio deception and jamming incidents | minor: a unit's routine |
| 125-27 | Mar. 10; Mar. 23; May 5 | captures of VC documents and agents, maps of bases | minor |
| 140-48 | Jan.-Dec. | terror incidents by month (figures); the Đức Tôn kidnapping (June 20); the Đà Nẵng procurement office (June 13) and bus (June 26) bombings; the A Châu newspaper bombed in Cholon (July 26); the OSI residence plot (July 23); the Saigon grenade attacks (Aug. 7, 9) | figures; not entered in this run: leads, each with its page (the A Châu bombing a press event) |
| 149-52 | Jan. 8; Jan. 10-11; Dec. 27, 1967; Jan. 15; June 13 | VC-led demonstrations at Đà Nẵng and Lai Nghi against the bombing; the circular on the truce; the letter on agents in Saigon's precincts | not entered in this run: leads |
| 155-95 | Jan.-Dec. | the enemy's attacks corps by corps, month by month (each attack on a camp, a district town, a convoy, a fire base, with its losses) | entered where the History treats a day as notable (Jan. 2, May 28, Sept. 18, Sept. 22, Nov. 15, Nov. 17, June 11); the rest not entered in this run: leads, each with its page |
| 249-52 | Jan. 11; Jan. 21, 1969; Feb. 24; Feb. 28; Mar. 4 | the revised FY69 and proposed FY70 force structure package (not approved); the VNAF helicopter expansion briefed; the modified plan briefed to the Chief of the JGS and the Mission Council | minor: a staff's steps toward the plans entered (Apr. 24, Oct. 4-Dec. 18) |
| 255 | June 8; June 13 | the Joint Chiefs ask a recomputation of the equipment needed; MACV's reply | minor: a staff's routine |
| 261-70 | Feb. 21; Mar. 14; June 25; July 16; Aug. 27; Nov. 28; Dec. 18 | the M16, M60, M79, M29, 105mm howitzer, APC and antitank-ammunition programs for the RVNAF, approvals and deliveries | not entered in this run: leads, each with its page (the approvals of Phase I, July 16 and Aug. 27, among them) |
| 270-75 | Oct. 25, 1967; Feb. 28; Mar. 21; Apr. 30; Oct. 30; Nov. 5 | the mobilization decrees and communiques; the return of essential reservists; the Interministerial Committee's hearings; MACV on the paramilitary forces in the draft; the report period extended | not entered in this run: leads (Mar. 1 and Aug. 21 entered) |
| 279 | Oct. 4; Oct. 8; Dec. 3 | the JGS's antidesertion directives and meeting | minor (Dec. 7 entered) |
| 281-99 | Feb. 11; Feb. 17; Jan. 1; June 1; Aug. 31; May 6; May 10 | training resumed after Tet; Westmoreland's letter on promotions; pay raises (the RF and regulars, Jan. 1; the PF decree, June 1); the Military Academy's funds; the National Defense College opened; the Cát Lái vocational school | not entered in this run: leads |
| 301-08 | Jan. 28; Mar. 1-5; Mar. 30; Nov. 20 | a new armored cavalry regiment authorized; the Airborne Division's expansion completed; the interpreter program | not entered in this run: leads |
| 316-43 | Feb. 20; Apr. 4; Mar. 1; Mar. 17; June 10; Aug. 1; Feb. 3 | Westmoreland on the Saigon Naval Shipyard's pay scales; the VNN's part in the trawler's capture at Hòn Hèo; the LCMMs; the Riverine Force's PBRs; JGS Memorandum 349 on the Regional Forces | not entered in this run: leads (the trawler of Mar. 1 a lead for the naval chapter) |
| 344-45 | 1968 | the CIDG camps converted to RF status (Bến Sỏi, Kinh Quan II); CIDG strength 45,000 | no day given |
| 348-55 | 1968 | the Free World forces' section | not in the copy: the copy runs from p. 347 to p. 356 (its notes, 356-70, are there) |
| 403 | Aug. 23 | the battle for Đức Lập from 0105, some 4,000 of the enemy, as the air chapter tells it | a lead: the pending entry of Aug. 23 (b3-macv-1968-2) gives two battalions; to be settled against the after-action report (n.139) |
| 405-06, 416-17, 422, 432 | Jan.-Dec. | the sortie tables (Marine, VNAF, Rolling Thunder, Arc Light, rescue); the vehicle sightings on Routes 15, 101, 137 | figures, for the war table |
| 406 | Jan. 9 | Seventh Air Force's message on the interdiction of 1967 | minor: a repetition |
| 415 | Apr. 5; Apr. 10 | the F-111As of Combat Lancer released for local and night training | not entered in this run: a lead |
| 420-21 | Feb. 22; June 19-21 | a B-52 strike in Laos, "two hours" of secondary explosions; the strikes on War Zone D | not entered in this run: leads |
| 424-26 | Jan. 5; Jan. 9-15; Jan. 15-17; Mar. 18, 23, 24 | Niagara's planning, approval (Vientiane, Jan. 16; CINCPAC, Jan. 17) and the attacks by fire on Khe Sanh; 1,398 reconnaissance sorties | already in (Niagara, Jan. 21, and Khe Sanh); the planning days leads |
| 431 | 1968 | Capt. Gerald O. Young's rescue mission, the Medal of Honor | a lead: the day not read |
| 445-46 | Jan. 31; Feb. 8; Feb. 15 | an enemy swimmer captured at Cam Ranh; Stable Door in Vũng Rô Bay | minor: a unit's routine |
| 452-53 | Jan. 11; Jan. 21; Feb. 2; Mar. 14-20; May 3 | swimmer-sapper and mining incidents on the rivers; a limpet mine captured | not entered in this run: leads |
| 458 | Feb. 1; Feb. 12; June 10 | Game Warden's men leave their compound; Eckhardt's message to Task Force 116; chain-drag sweeping to the VNN | minor; leads |
| 459-60 | Aug. 10, 22, 25; Sept. 7, 17; Dec. 4 | the merchant ships attacked in the channel to Saigon (*Southport*, a British tanker, *Lakewood Victory*, *Transnorther*, *Kalydon*) | not entered in this run: leads, each with its page |
| 466-72 | Jan. 7-8; Jan. 10; Feb. 12-13; Mar. 3; Mar. 5, 14, 22; Aug. 17; Oct. 15; Dec. 5-6; Dec. 16 | the Mobile Riverine Force's operations: Dồn Nhơn, Cái Bè, Cần Thơ, the river division sent to the Cửa Việt (Mar. 9-10), the attacks on its ships, the howitzers on monitors, its reorganization, Base Area 480 | not entered in this run: leads, each with its page |
| 474-79 | Nov. 16; Jan. 14; Mar. 30 | the Swift boats through the Rạch Giang Thành and Vĩnh Tế canals; the concrete bunkers; the first AMMI pontoon bridge | not entered in this run: leads |
| 488-94 | Feb.; June 17; Aug. 4; July 6 | the naval gunfire ships at Huế; the gunfire priorities | minor: a staff's routine (July 6 within June 18) |
| 500 | Jan. 2; Jan. 25-29 | the hospital ships for Chu Lai and northern I Corps | minor |
| 939-41 | Dec. 28, 1967; Nov. 27, 1967; Jan. 10; Mar. 25-Apr. 24; May 17; June 4 | the information advisers to the RVNAF: Viên's reply, the conferences, the press course, the RVNAF's morning release; COL Trần Văn Đắc and LTC Phan Mậu presented to the press | minor: an office's routine; the defectors' presentation a lead (no day) |
| 950-53 | Jan. 20; Feb. 11; Apr. 12; May 18; June 24; Sept. 2; Sept. 18; Nov. 6; Nov. 19; Dec. 4 | the American Forces Vietnam Network's new transmitters and stations, programs and the election coverage | minor: a unit's routine |
| 956-59 | 1968 | Gene Roberts (New York Times) on the press and the military; Sidle on the ground rules; John Wheeler (AP) on Khe Sanh; Schlesinger and Alsop | no day given: the press lines, leads |
| 964-65 | May 1 | III MAF's plan for embargoes; Donald Kirk's article | no day for the article (in the press lines) |
| 968-70 | May 27; Aug. | Westmoreland's informal guidance to his commanders; the guidance on the "Third Wave"; Clifford's message nine days later praising MACV's press work | not entered in this run: leads (the days not read) |
| 974 | July 11 | the Joint Chiefs' message on the casualty releases; Clifford on counting the eleven men of the LCU held by Cambodia | minor; a lead |
| 977-90 | Aug.-Nov. | the press's change of tone as MACV quoted it: the anticorruption campaign, the Marines' mobility (Oct. 13), Abrams likened to Ridgway, North Vietnam's draft, the Tampa Tribune (Sept. 30) | in the press lines; leads |
| 780-81 | early 1968 | MACV's four residual force levels (a MAAG to a MAAG and three divisions) | no day given (within Aug. and Oct. entries) |
| 782 | Jan. 26; Feb. 8; Feb. 9 | CINCPAC's concurrence in Pacific Grove; its revival asked; the Beach Jumper units | within the entry of Feb. 3 |
| 783 | Mar. 30; May 16; July | Sauna Scrub ordered, briefed, sent on | within the entry of Apr. 30 |
| 783-84 | 1968 | Project New Castle (the courses of action after a full bombing halt; a force into the Laotian panhandle) | no day given: a lead (its notes) |
| 786-88 | Feb. 11; Feb. 13; Mar. 22; May 24; May 15-June 1; Dec. 16; May; Apr. 21-July 16; May 3 | the Điện Biên Phủ study's stages; the vulnerability study; the PSYOP appraisals; the study of returning prisoners to the North; the 142-page report reviewing "both works"; the International Affairs Division | minor (staff steps) or not entered in this run: leads (the prisoner study and the report, their subjects to be read) |
| 789-95 | Oct.; Aug. 29; July 23; Aug. 31; Dec. 31 | the cease-fire studies (a negotiating position); the RAHIB study of a full halt; the verification study; POSEC; the Long Range Planning Task Group | not entered in this run: leads |
| 841-43 | 1968; Feb. 16-; Apr. 2 | parcels to the prisoners in the North refused; the released pilots' and the two women's debriefings | minor |
| 847 | Dec. 30-Jan. 1969 | the PLAF's conditions for the second meeting; II Field Force's answer | within Dec. 25; the rest after the span |
| 848-49 | May 25; May 29; June 2; June 4; July 22; July 30; Oct. 2 | the notes and statements over the *Bream* and the LCU | within the entries of May 20 and July 16 |
| 851-59 | Mar. 24; Dec. 1, 1967; Mar. 15; May; July 31; Aug. 10; Aug. 16; Nov. 26; Jan. 16; May 16; Apr. 1 | the reporting of captured sources; the plans for the North Vietnamese prisoners' release; the ICRC's telegram to Hanoi on 40 sick and wounded; Côn Sơn's camp | minor, or within the entries made (Mar. 29, Oct. 21, Nov. 30, Dec. 16); the ICRC's telegram a lead |
| 911-31 | June 1; Apr.; Jan. 14; Mar. 19; Jan. 28-29; July 9; Oct. 30; June 16; Aug. 25 | the barrier's code names (Muscle Shoals to Igloo White, Duck Blind); the bunkers' tests; the ARVN Dye Marker regiment and its weapons; the I Corps and III MAF meeting on Duel Blade; Duck Blind's first phase | minor (names, tests), or within the entries made; the ARVN regiment a lead |

## The press (Nov. 4, the 1968 volume's Annex C)

1967-09-06 | Los Angeles Times | article | ordnance developed under Project Gunfighter (as MACV listed the unauthorized releases) | 944 1967-09-14 | Washington Post | article | the limited supply of Walleyes | 944 1967-10-07 | UPI | wire | the new CIDG camp at Bu Prang, before its announcement | 945 1968-01-05 | CBS | broadcast | the embargo on Fargo broken, after an interview with the unit's commander | 944 1968-02-09 | Christian Science Monitor | article | "The credibility gap ... starts right in Saigon at the official United States press briefings" | 955 1968-02-09 | Los Angeles Times | article | "Marines along DMZ Disturbed at Report of Takeover by Army" | 960 1968-02-12 | Newsweek | article | Everett G. Martin, "The Devastating Effect on the People" (cited, n.16) | 993 1968-02-19 | Washington Post | front page | "A Drink of Water--Then Death," five columns, two photographs | 958 1968-02 | New York Times | article | Joseph B. Treaster on aircraft shortages in the 1st Cavalry Division (a ground-rules case) | 966 1968-02/03 | AP | wire | John Wheeler on Khe Sanh's hill outposts | 958-59 1968-03-03 | Washington Post | article | (cited, n.21: the Khe Sanh reporting; Schlesinger and Alsop) | 994 1968-03 | Los Angeles Times | article | Bill Tuohy on the Marine leadership, "singularly unimpressive, say the critics" | 961-62 1968-03-17 | Washington Star | article | Donald Kirk on the command arrangements in I Corps | 963 1968-04-21 | (Joseph Alsop) | column | the embargo on Delaware broken | 964 1968-05 | (Donald Kirk) | article | Westmoreland "convinced the press has impeded prosecution of the war" (the embargo of May 1) | 964-65 1968-07-03 | New York Times | article | (cited, n.17) | 993 1968-07-28 | Baltimore Sun | article | Carroll's six-month suspension, "the most severe penalty"; "extraordinarily vindictive" | 967 1968-07-29 | Baltimore Sun | article | at least four newsmen suspended; 23 discredited in several years | 967-68 1968-08-12 | Washington Post | article | Peter Braestrup on MACV's use of the B-52s | 977 1968-09-02 | US News & World Report | article | Ben Price, "Did US Bungle Victory?" | 995 1968-09-05 | Christian Science Monitor | article | Beverley Deepe on the Communists' criticism of their May offensive | 982-83 1968-09-13 | Christian Science Monitor | article | Deepe, "Chasing Credibility in Saigon" | 983 1968-09-30 | Tampa Tribune | editorial | "A most outspoken editorial" (the text not read off the page) | 983 1968-10-06 | Chicago Daily News | article | (cited, n.38) | 995 1968-10-07 | Newsweek | column | Kenneth Crawford, "Vietnam: All is Lost?" | 987 1968-10-13 | (wire or paper not named) | article | the Marines' new mobile posture from the Bến Hải to Khe Sanh | 988 1968-10-14 | Baltimore Sun; Christian Science Monitor | articles | (cited, nn.41-42) | 995 1968-10-27 | New York Times | article | (cited, n.43) | 995 1968-10-28 | Newsweek | column | Crawford, "It Started with Tet" | 987-88 1968-11-04 | US News & World Report | article | Sol W. Sanders, "Why Communists Need a Truce" | 995

## Leads (Nov. 4)

National
- Propose Part III entries (K–J Cong. III.J or Viet.) for the press figures the annex treats: Bill Tuohy (*Los Angeles Times*), Donald Kirk (*Washington Star*), Peter Braestrup (*Washington Post*; a name entry wanted), John S. Carroll (*Baltimore Sun*), Helen A. Musgrove (Jacksonville *Journal*), Joseph B. Treaster (*New York Times*), Gene Roberts (*New York Times*), John Wheeler (AP), Everett G. Martin (*Newsweek*).
- The 1968 volume's Annex C, its undated items: Gene Roberts's article on the press and the military; Wheeler's on Khe Sanh; the Schlesinger-Alsop exchange; the *Tampa Tribune*'s editorial of Sept. 30 (983, not read off the page); Clifford's message praising MACV's press work ("nine days later," 970).

Foreign
- 1968 vol., Ch. III: the weapons first found or used (106-19) and the terror incidents (140-48), each with its page; the corps-by-corps attacks (155-95) not entered; the NLF's statement of Nov. 3 (40); Hanoi's flour request (52).
- 1968 vol., Ch. IV: the weapons programs' approvals (261-70), the mobilization decrees (270-75), the RVNAF's units and pay (281-308, 316-43); the Free World section (348-55) is not in the copy: another copy needed.
- 1968 vol., Ch. V: Combat Lancer's F-111As (Apr. 5, 10); Capt. Gerald O. Young's rescue (431); the merchant ships attacked in the channel to Saigon (Aug. 10-Dec. 4, 459-60); the Mobile Riverine Force's operations (466-72); Turnpike's first day (407, the columns garbled); the Đức Lập battle's size (403 against the pending entry of Aug. 23).
- 1968 vol., Ch. XI: New Castle, the prisoner study, the 142-page report, the cease-fire and verification studies, POSEC, the Long Range Planning Task Group (783-95): their days and subjects in J-5's monthly histories (the notes).
- 1968 vol., Ch. XII: the ICRC's telegram to Hanoi on 40 sick and wounded prisoners, Jan. 16 (859); Sgt. Buddy Wright's escape, Sept. 22 (849).
- The 1968 volume's unread chapters and annexes (above, "Where I stopped").
