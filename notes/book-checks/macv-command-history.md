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
Patches: `inbox/2026-10-29-b3-macv-1964.yaml` (patch `b3-macv-1964`): 50 new entries, 16 edits; `inbox/2026-10-29-b3-macv-1964-more.yaml` (patch `b3-macv-1964-more`): 146 new entries.

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

### Entered (the owner's ruling, Oct. 28): the papers

The staff and planning papers, commanders' messages and plans first passed over as "below the level", "a step" or "to
the owner", now entries in the same patch, `inbox/2026-10-29-b3-macv-1964.yaml`:

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

Every dated event the volume treats that the calendar lacks, the chronology's (189-93) and the chapters', each its
entry, in the supplementary patch `inbox/2026-10-29-b3-macv-1964-more.yaml` (patch `b3-macv-1964-more`, merged after
`b3-macv-1964`: some of its entries point to that patch's): Saigon's governments and measures, the operations and
incidents, the border incidents with Cambodia, the visits and appointments, the papers. A month or a stretch is dated
to the month or the first day, "Check: the day". The places named; a province tagged only where the History names it.

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
`b3-macv-1965`): 121 new entries, 16 edits.

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

### New entries, and those the rulings of Oct. 28 called for

All in `inbox/2026-10-29-b3-macv-1965.yaml`: the first 22 from the reading, the rest (the chronology's dated events,
the operations, incidents, arrivals, conferences and papers) by the owner's rulings of Oct. 28 and Oct. 28, late, rows
first written here as "Passed over" and moved.

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

- The command's organization, 1965: the 1st Logistical Command (Apr. 1), III MAF (May 7), USARV (July 20), Task Force
  Alpha (Aug. 1) and Field Force, Vietnam (Sept. 25): the History's chronology (479-81) and ch. II; whether the calendar
  should hold the command's structure as it holds the MACV–MAAG merger of 1964.
- MACV's public confirmation of North Vietnamese units: the 101st Regiment (July 15), five regiments (Nov. 7): the
  History's chronology only; the press releases (MACOI) and the *New York Times* of the next days.
- The Honolulu conferences of Sept. 28 and Dec. 10 (Sharp and Westmoreland): chronology only; FRUS 1964–68, III.
- The Marble Mountain and Chu Lai attacks of Oct. 27: chronology only.
- The 1966 volume (the DMZ, Attleboro, Masher, Crimp) was not among the copies: a Sources to Fetch item.
