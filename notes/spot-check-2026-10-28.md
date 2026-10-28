# Spot check, Oct. 28, 2026: the book and official-history runs against the page

The first stage of the second reading pass (the owner's approval, Oct. 28, 2026). An independent check of the merged
patches of the book agents and the official-histories agent. It works from the printed pages alone. The agents' own
notes in `notes/book-checks/` were not used as evidence. The fixes are in one patch, `inbox/2026-10-28-spot-check.yaml`.

## Method

- **Population.** The ops of the merged patches `inbox/merged/2026-10-23-book-*.yaml`,
  `2026-10-23-official-histories.yaml`, `2026-10-24-book-*.yaml` and `2026-10-24-book-gibbons.yaml` (merged 01:09
  Oct. 28). For each op, the pinpoints `[[w.card]], PAGES` that are new against the op's base (`find_base`,
  `tools/bib/merge.py`), and every quotation in `c` that is added or newly set.
  - The book and official-history patches give 1,649 pinpoints and 366 quotations.
  - The Gibbons patch gives 555 pinpoints and 666 quotations.
  - Four edits had no base to be found (Miller, cal.1960-01-26.vietnam and cal.1963-01-02.vietnam; Dallek,
    cal.1967-06-23.soviet-union and cal.1964-08-02.vietnam). For these, every pinpoint was counted.
- **Sample.** Seed 20261028. Stratified by work: 5 percent of each work's pinpoints, rounded up, with at least 5
  (or every pinpoint where a work has fewer), drawn by `random.Random(seed).sample` in sorted card order. The main
  sample is 185 pinpoints. The Gibbons patch, drawn the same way, adds 61. Gibbons, pt. IV is one stratum, and each
  other work the Gibbons run cites is its own.
- **Grades.**
  - Pinpoints were read against the page, and the claim taken was what `c` attributes to the source under the house
    rule (a source stands for the whole entry unless its parenthetical narrows it):
    - HOLDS: the page bears the claim out.
    - PARTIAL: the page bears out part of the entry and the cite carries no parenthetical.
    - PAGE OFF: the matter is on a neighbouring page.
    - NOT THERE: the page lacks the claim.
    - WRONG: the page says otherwise (a date, a number, a word).
  - Three grades fall outside that scale and are not counted in the rates:
    - UNREAD: a pinpoint correctly behind "To check:" or in a "Made public:" pointer.
    - NO COPY: no copy of the work could be reached.
    - SECONDHAND: a work cited as read whose page the agent had only through another book's quotation.
  - Quotations were read letter for letter, and for whose words they are: EXACT, MINOR (punctuation, a bracket or a
    trailing clause dropped, the sense and the words intact), WRONG, NOT FOUND.
- **Copies used.**
  - The books: the owner's Drive scans as text (the scratchpad's `drive/*.txt`, and Zelizer and Stein fetched by
    `book-ids.txt` and deleted after use), with printed folios mapped from the running heads.
  - The official histories: the DTIC and Government Printing Office scans on archive.org (Kaplan, Drea, Watson, the
    Joint Chiefs' histories, Marolda, Futrell, Van Staaveren, Anthony, Schlight).
  - Gibbons: pts. I and IV.
  - FRUS: the TEI text (`sources/frus-text/`). The Public Papers: GPO's scans (`sources/ppp-text/`).
  - Not reached: Gibbons, pts. II and III; *Current Documents*, 1963; the Pentagon Papers (USG and Gravel eds.);
    Cooper, Califano, Perry, Clifford and the other works the Gibbons run cites from Gibbons's notes.
- **Rates.** Rates are failures over pinpoints checked (HOLDS through WRONG), with Wilson 95 percent intervals.
  "Serious" means PAGE OFF, NOT THERE and WRONG.

## Results by work

A stratum of five can only tell a clean work from a bad one. The intervals are wide.

| work | N | sampled | HOLDS | PARTIAL | PAGE OFF | NOT THERE | WRONG | SECONDHAND | UNREAD | NO COPY | failures | serious |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gibbons-u-s-government-and IV | 505 | 26 | 24 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1/25 (1%–20%) | 0/25 (0%–13%) |
| garrow-bearing-the-cross | 159 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/8 (0%–32%) | 0/8 (0%–32%) |
| dallek-flawed-giant | 123 | 7 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1/7 (3%–51%) | 0/7 (0%–35%) |
| kaplan-mcnamara-ascendancy-1961-1965 | 106 | 6 | 5 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1/6 (3%–56%) | 1/6 (3%–56%) |
| schlesinger-thousand-days-1965 | 105 | 6 | 5 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1/6 (3%–56%) | 0/6 (0%–39%) |
| johnson-vantage-point | 100 | 5 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1/5 (4%–62%) | 0/5 (-0%–43%) |
| drea-mcnamara-clifford-and-the-2011 | 90 | 5 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2/5 (12%–77%) | 0/5 (-0%–43%) |
| caro-passage-of-power | 87 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/5 (-0%–43%) | 0/5 (-0%–43%) |
| dittmer-local-people | 79 | 5 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 3/5 (23%–88%) | 0/5 (-0%–43%) |
| zelizer-taxing-america | 70 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/5 (-0%–43%) | 0/5 (-0%–43%) |
| schlesinger-robert-kennedy-and-his | 68 | 6 | 4 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1/5 (4%–62%) | 1/5 (4%–62%) |
| vietnam-victory-in-vietnam | 56 | 5 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2/5 (12%–77%) | 0/5 (-0%–43%) |
| cosmas-joint-chiefs-of-staff-2012 | 51 | 5 | 1 | 1 | 2 | 0 | 1 | 0 | 0 | 0 | 4/5 (38%–96%) | 3/5 (23%–88%) |
| schwartz-lyndon-johnson-and-europe | 49 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/5 (-0%–43%) | 0/5 (-0%–43%) |
| miller-misalliance | 44 | 5 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1/5 (4%–62%) | 0/5 (-0%–43%) |
| stein-fiscal-revolution-in-america | 39 | 5 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1/5 (4%–62%) | 0/5 (-0%–43%) |
| nguyen-hanois-war | 38 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/5 (-0%–43%) | 0/5 (-0%–43%) |
| cosmas-joint-chiefs-of-staff | 37 | 5 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 4/5 (38%–96%) | 0/5 (-0%–43%) |
| marolda-united-states-navy-and | 37 | 5 | 2 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 3/5 (23%–88%) | 1/5 (4%–62%) |
| perlstein-before-the-storm | 37 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/5 (-0%–43%) | 0/5 (-0%–43%) |
| poole-joint-chiefs-of-staff | 37 | 5 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 4/5 (38%–96%) | 0/5 (-0%–43%) |
| schulimson-joint-chiefs-of-staff | 28 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/5 (-0%–43%) | 0/5 (-0%–43%) |
| frankum-like-rolling-thunder | 27 | 5 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 3/5 (23%–88%) | 0/5 (-0%–43%) |
| poole-joint-chiefs-of-staff-2012 | 26 | 5 | 2 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 3/5 (23%–88%) | 2/5 (12%–77%) |
| asselin-hanois-road-to-the | 25 | 5 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1/5 (4%–62%) | 0/5 (-0%–43%) |
| watson-into-the-missile-age | 23 | 5 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1/5 (4%–62%) | 0/5 (-0%–43%) |
| futrell-united-states-air-force | 19 | 5 | 2 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 3/5 (23%–88%) | 2/5 (12%–77%) |
| staaveren-gradual-failure | 18 | 5 | 2 | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 3/5 (23%–88%) | 2/5 (12%–77%) |
| johns-vietnams-second-front | 15 | 5 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2/5 (12%–77%) | 0/5 (-0%–43%) |
| anthony-war-in-northern-laos | 12 | 5 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 3/5 (23%–88%) | 0/5 (-0%–43%) |
| pentagon-papers | 12 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 6 | — | — |
| jian-maos-china-and-the | 11 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/5 (-0%–43%) | 0/5 (-0%–43%) |
| staaveren-u-s-air-force | 11 | 5 | 4 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1/5 (4%–62%) | 1/5 (4%–62%) |
| def-u-s-viet-rels | 7 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | — | — |
| schlight-united-states-air-force | 4 | 4 | 0 | 2 | 1 | 0 | 1 | 0 | 0 | 0 | 4/4 (51%–100%) | 2/4 (15%–85%) |
| califano-triumph-and-tragedy-of | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 3 | 0 | — | — |
| clifford-counsel-to-the-president-2 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | — | — |
| cooper-lost-crusade | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | — | — |
| gibbons-u-s-government-and II | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | — | — |
| bohlen-witness-to-history-1929 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | — | — |
| herring-secret-diplomacy-of-the | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | — | — |
| macneil-dirksen | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | — | — |
| obrien-no-final-victories | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | — | — |
| westmoreland-soldier-reports | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | — | — |
| 77-conversations-between-chinese | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/1 (0%–79%) | 0/1 (0%–79%) |
| current-documents-1963 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | — | — |
| department-of-state-bulletin | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/1 (0%–79%) | 0/1 (0%–79%) |
| gibbons-u-s-government-and III | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | — | — |
| harris-sacred-trust | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | — | — |
| heller-new-dimensions-of-political | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | — | — |
| humphrey-education-of-a-public-1976 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | — | — |
| kalman-abe-fortas | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | — | — |
| solberg-hubert-humphrey | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | — | — |
| sorensen-kennedy | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | — | — |
| herring-lbj-and-vietnam | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | — | — |
| krulak-first-to-fight | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | — | — |
| mccarthy-year-of-the-people | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | — | — |
| perry-four-stars | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | — | — |
| salisbury-time-of-change | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | — | — |
| zaroulis-who-spoke-up | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | — | — |

Totals for all 246 sampled pinpoints:

- 193 were checked against a page: 139 HOLDS, 39 PARTIAL, 3 PAGE OFF, 3 NOT THERE and 9 WRONG.
- 54 of the 193 failed (28 percent, 22–35 percent), 15 of them seriously (8 percent, 5–12 percent).
- Not counted: 5 SECONDHAND, 33 UNREAD and 15 NO COPY.

## By agent run

| run | pinpoints | sampled | checked | failures | serious |
|---|---|---|---|---|---|
| 2026-10-24-book-gibbons | 555 | 61 | 25 | 1 (1%–20%) | 0 (0%–13%) |
| 2026-10-23-official-histories | 494 | 70 | 70 | 36 (40%–63%) | 14 (12%–31%) |
| 2026-10-24-book-garrow-cross | 159 | 8 | 8 | 0 (0%–32%) | 0 (0%–32%) |
| 2026-10-24-book-dallek-giant | 141 | 15 | 8 | 1 (2%–47%) | 0 (0%–32%) |
| 2026-10-24-book-zelizer-stein | 112 | 13 | 10 | 1 (2%–40%) | 0 (-0%–28%) |
| 2026-10-24-book-thousand-days | 107 | 7 | 7 | 1 (3%–51%) | 0 (0%–35%) |
| 2026-10-24-book-vantage-point | 100 | 5 | 5 | 1 (4%–62%) | 0 (-0%–43%) |
| 2026-10-24-book-caro-passage | 88 | 5 | 5 | 0 (-0%–43%) | 0 (-0%–43%) |
| 2026-10-23-book-dittmer | 79 | 5 | 5 | 3 (23%–88%) | 0 (-0%–43%) |
| 2026-10-23-book-schlesinger-rfk | 65 | 5 | 5 | 1 (4%–62%) | 1 (4%–62%) |
| 2026-10-24-book-asselin-nguyen | 62 | 11 | 11 | 1 (2%–38%) | 0 (0%–26%) |
| 2026-10-24-book-schwartz-chen | 58 | 9 | 9 | 0 (0%–30%) | 0 (0%–30%) |
| 2026-10-23-book-miller | 53 | 12 | 5 | 1 (4%–62%) | 0 (-0%–43%) |
| 2026-10-23-book-victory | 53 | 5 | 5 | 2 (12%–77%) | 0 (-0%–43%) |
| 2026-10-24-book-perlstein-johns | 52 | 10 | 10 | 2 (6%–51%) | 0 (-0%–28%) |
| 2026-10-23-book-frankum | 26 | 5 | 5 | 3 (23%–88%) | 0 (-0%–43%) |

Weighted by each work's population, the estimates are:

- **The official-histories run:** about 46 percent of its 494 pinpoints fail (some 230), and about 17 percent fail
  seriously (some 85).
- **The book runs other than Gibbons:** about 16 percent of 1,133 fail, nearly all PARTIAL, and about 1 percent fail
  seriously.

## Every failure

Each line gives the entry, the card, the pages, the grade, and what the page says. Every one is fixed in the patch.

- `cal.1965-02-07.vietnam` · anthony-war-in-northern-laos · 156 · **PARTIAL** · Anthony 156 gives the attack (Feb. 7, 7 killed, 109 wounded), Bundy and Taylor's recommendation, the NSC's approval; it says the four targets "were struck on the 7th and 8th" and does not give Camp Holloway, the hour, Bundy's arrival, the NSC's evening of Feb. 6, Đồng Hới, Chấp Lễ, the dependents
- `cal.1965-04-03.laos` · anthony-war-in-northern-laos · 164 · **PARTIAL** · Anthony 164 gives only "April 3 — the kickoff date for Steel Tiger" (in a passage on search and rescue); nothing on the routes, the division, the Lao or Souvanna
- `cal.1962-05-15.laos` · anthony-war-in-northern-laos · 68 · **PARTIAL** · Anthony 68 gives May 15 (MACTHAI set up; JTF 116; the Marine BLT and the 27th Division's elements to Ubon and Korat); no figure of about five thousand (pp. 67-69)
- `cal.1963-12.vietnam` · asselin-hanois-road-to-the · 162–68 · **PARTIAL** · Asselin 162-68 gives the plenum (opened Nov. 22), the decisive victory in a "not very long period", main forces, the North's aid, the PAVN to wartime strength and "complete units" south (168); not "the direct deciding factor", "limited war" or 300,000
- `cal.1967-12-19.vietnam-2` · cosmas-joint-chiefs-of-staff · 139 · **PARTIAL** · Cosmas 139 gives the Dec. 20 letter to Wheeler only ("intensified countrywide effort, perhaps a maximum effort"); nothing of a Dec. 19 message or "a psychological and political victory" (138-39)
- `cal.1968-05-10.vietnam-operations` · cosmas-joint-chiefs-of-staff · 208 · **PARTIAL** · Cosmas 208: on May 10 "a North Vietnamese division surrounded and assaulted a Special Forces camp at Kham Duc"; no Ngok Tavak, no abandonment, no Americal reinforcements
- `cal.1968-04-03.vietnam-2` · cosmas-joint-chiefs-of-staff · 176–177 · **PARTIAL** · Cosmas 177: the Chairman (Wheeler) ordered operations stopped above the 20th, the President directed a halt above the 19th; the entry calls the 20th Clifford's order
- `cal.1967-05-20.vietnam-program-5` · cosmas-joint-chiefs-of-staff · 52–53, 57–59 · **PARTIAL** · Cosmas 52-53: the JCS memoranda of May 20 (posture, wider war on the North); 57-59: the Chiefs' reply to the draft memorandum came after McNamara asked for it May 22 and June 2, not May 20
- `cal.1965-12-24.vietnam` · cosmas-joint-chiefs-of-staff-2012 · 390–391 · **PAGE OFF** · Cosmas 390-91 give the planning (the Viet Cong offer of Dec. 7, the messages of Dec. 13-19); the hours (1800 Dec. 24 to 2400 Dec. 25) and the instruction of Dec. 22 are on 392-93
- `cal.1964-01-30.vietnam` · cosmas-joint-chiefs-of-staff-2012 · 10 · **PAGE OFF** · Cosmas 10 has only the heading; the coup (bloodless, Minh and four others detained) and Khánh's charge of a neutralist plot are on 11-12; nothing of Johnson's Feb. 1
- `cal.1966-07-15.vietnam-operations` · cosmas-joint-chiefs-of-staff-2012 · 449 · **WRONG** · Cosmas 449 dates Hastings "15 June"; none of the landing, the CH-46s, Task Force Delta; the entry gives no Check (notes/official-histories-discrepancies.md ruled it but left the cite unqualified)
- `cal.1964-03-16.vietnam` · cosmas-joint-chiefs-of-staff-2012 · 33–36 · **PARTIAL** · Cosmas 33-36: no "40 percent" (22 of 43 provinces at least half VC-controlled, 34) and no 50,000; the support for Khánh, no overt action now, 72 hours and 30 days hold
- `cal.1968-01-24.open-housing` · dallek-flawed-giant · 517 · **PARTIAL** · Dallek 517 gives the message and fair housing in all housing only; not the penalties, the EEOC's powers, the juries, the three stages
- `cal.1964-07-10.mississippi` · dittmer-local-people · 250–51 · **PARTIAL** · Dittmer 250-51: Hoover opens "a new field office in Jackson" July 10 and meets the governor; nothing of its being closed since 1946
- `cal.1966-01-10.mississippi` · dittmer-local-people · 391 · **PARTIAL** · Dittmer 391: "late one night in January 1966", died "the next afternoon"; no Jan. 10, no Kelly Settlement, no NAACP office, no registration book or radio offer on the poll tax
- `cal.1964-07-06.desegregation-schools` · dittmer-local-people · 228, 256–57 · **PARTIAL** · Dittmer 228: Mize's decree of March 1964 to submit plans; 256-57: Leake County joined Jackson and Biloxi as the first systems desegregated, fall 1964; nothing of the July 6 opinion, its words, Darrell Kenyatta Evers or Aug. 31
- `cal.1966-09-26.europe-and-the-alliance` · drea-mcnamara-clifford-and-the-2011 · 409 · **PARTIAL** · Drea 409: the meeting of Sept. 26 and the joint statement's "searching reappraisal" (the tripartite review); not the offset words, reunification or McCloy
- `cal.1968-07-05.vietnam-khe-sanh` · drea-mcnamara-clifford-and-the-2011 · 196 · **PARTIAL** · Drea 196: "the official closing of the Khe Sanh base on 5 July" only; the hour and the convoy to Ca Lu not there
- `cal.1965-12-15.vietnam` · frankum-like-rolling-thunder · 33 · **PARTIAL** · Frankum 33: "In mid-December" the strike on Uông Bí, "nearly 15 percent" of capacity; not the restrikes or the boiler house
- `cal.1968-11-15.laos` · frankum-like-rolling-thunder · 126–128 · **PARTIAL** · Frankum 126-28: Commando Hunt from Nov. 15, the passes, Igloo White; not Sullivan's figures of Nov. 4
- `cal.1965-03-02.vietnam` · frankum-like-rolling-thunder · 21–22 · **PARTIAL** · Frankum 21-22: the first strike Mar. 2, 160 aircraft (the Check notes it), no announcement; nothing of Harold K. Johnson's mission
- `cal.1962-07-23.vietnam` · futrell-united-states-air-force · 147 · **NOT THERE** · Futrell 147: the Honolulu conference of July 23, 1962, on the RT-33 photo jets; nothing of withdrawal plans
- `cal.1961-10-18.vietnam` · futrell-united-states-air-force · 74 · **PARTIAL** · Futrell 74: the Mekong floods (Pipe Stem arrives Oct. 18 "just after the Mekong River had overflowed its banks"); nothing of Taylor, Rostow or the emergency
- `cal.1964-12-28.vietnam-operations` · futrell-united-states-air-force · 260 · **WRONG** · Futrell 260: "At night on December 27, two North Vietnamese regiments raided the hamlet of Binh Gia"; the rangers Dec. 28-29, the marines Dec. 30-31; none of the entry's totals
- `cal.1966-01-25.vietnam` · johns-vietnams-second-front · 105 · **PARTIAL** · Johns 105: the meeting of Jan. 25, Dirksen's and Hickenlooper's words; not Ford's or Mansfield's, nor the hour
- `cal.1965-02-17.vietnam-3` · johns-vietnams-second-front · 86–88 · **PARTIAL** · Johns 86-88: the meeting of Feb. 17, Eisenhower's objective and "negotiation from weakness"; nothing of the Tonkin and Formosa resolutions; Bundy and Goodpaster also there
- `cal.1967-11-05.vietnam` · johnson-vantage-point · 374 · **PARTIAL** · Vantage Point 374 prints Fortas's "Our duty ... is to do what we consider right" only; "total disagreement" and "an invitation to slaughter" are FRUS's (not on 373-75)
- `cal.1962-10-25.missile-crisis` · kaplan-mcnamara-ascendancy-1961-1965 · 213 · **NOT THERE** · Kaplan 213: only that Khrushchev "denied the presence of offensive missiles to the United Nations"; no Stevenson-Zorin exchange, no photographs; the book's index gives Stevenson at 185, 210 only (neither the session)
- `cal.1961-12-11.vietnam` · marolda-united-states-navy-and · 219 · **PARTIAL** · Marolda 219: Core arrives at Saigon Dec. 11 "with the first military equipment not authorized by the 1954 accord"; no helicopter companies
- `cal.1964-11-01.vietnam` · marolda-united-states-navy-and · 472 · **WRONG** · Marolda 472-73: the attack of Nov. 1, "twenty-four U.S. and South Vietnamese aircraft destroyed or damaged", four Americans killed "and seventy-two wounded" (473); the entry has 30 wounded and 27 aircraft; the casualties are on 473
- `cal.1965-02-13.vietnam` · marolda-united-states-navy-and · 504 · **PARTIAL** · Marolda 504: the President's advisers planned "a more limited air campaign against two or three selected targets"; no Feb. 13 decision, no 19th parallel for it, no Security Council or talks
- `cal.1963-06-16.vietnam` · miller-misalliance · 273 · **PARTIAL** · Miller 273: the communiqué of June 16, the ban on flags eased, a promise of further investigation; nothing of Ordinance No. 10 or the pardon
- `cal.1962-03-14.testing` · poole-joint-chiefs-of-staff · 85 · **PARTIAL** · Poole 85: the conference opens Mar. 14; nothing of Rusk and Gromyko on Berlin
- `cal.1961-10-17.berlin-and-vienna` · poole-joint-chiefs-of-staff · 157 · **PARTIAL** · Poole 157: Khrushchev drops the deadline Oct. 17; nothing of the fifty-megaton test
- `cal.1961-08-13.berlin-and-vienna` · poole-joint-chiefs-of-staff · 148 · **PARTIAL** · Poole 148: the roadblocks and wire in the early hours of Aug. 13; nothing of Hyannis Port or the protest
- `cal.1961-04-17.cuba` · poole-joint-chiefs-of-staff · 114–115 · **PARTIAL** · Poole 114-15: the landings, Red and Blue Beaches, the Río Escondido sunk; the Houston hit and forced aground, not sunk; no paratroopers or hours
- `cal.1967-04-07.middle-east` · poole-joint-chiefs-of-staff-2012 · 169 · **WRONG** · Poole 169: on Apr. 7 Syrians fire at Israeli tractors; Israeli Mirages "shot down two MiG-21s over Quneitra and four more over Damascus" (six, as fact); the entry has Israel claiming seven, Syria admitting four; nothing of UNTSO
- `cal.1965-07-22.vietnam` · poole-joint-chiefs-of-staff-2012 · 43 · **PARTIAL** · Poole 43: the White House discussions of July 21-22 (Wheeler's predictions), the recommendations of July 20; not the service secretaries, Clifford, McCloy or Dean
- `cal.1967-12-12.europe-and-the-alliance` · poole-joint-chiefs-of-staff-2012 · 120 · **NOT THERE** · Poole 120: on Dec. 12 the Defense Planning Committee accepted MC 14/3; nothing of the Council, the Harmel report or Rusk
- `cal.1968-01-30.robert-kennedy` · schlesinger-robert-kennedy-and-his · 839–41 · **WRONG** · Schlesinger 840 prints "I would not oppose Lyndon Johnson under any conceivable circumstances"; the entry quotes "under any foreseeable circumstances" with no other source
- `cal.1960-11-18.cuba` · schlesinger-thousand-days-1965 · 164 · **PARTIAL** · Schlesinger 164: on Nov. 18 Kennedy learned for the first time from Dulles and Bissell of the decision of Mar. 17, 1960, to train exiles; not Palm Beach, Radio Swan, the FRD, the plan of guerrilla action then assault
- `cal.1965-05-29.vietnam-operations` · schlight-united-states-air-force · 46 · **PARTIAL** · Schlight 46: May 29, a platoon of the Ba Gia battalion destroyed on a road-clearing operation, the battalion surrounded; May 30, three more battalions; the battle to June 4; no losses given
- `cal.1966-03-09.vietnam-operations` · schlight-united-states-air-force · 199 · **PARTIAL** · Schlight 199: the attack at 2 a.m. Mar. 9 and the defenders, "210 Vietnamese irregulars and their 10 American advisors"; nothing of the regiment, the final assaults, the helicopters, the garrison of 434 or the dead
- `cal.1966-01-24.vietnam` · schlight-united-states-air-force · 195–196 · **WRONG** · Schlight 195: Masher's "opening day, January 24" (the entry's when is Jan. 25); the cavalry, an ARVN division and a Korean battalion, Bồng Sơn; the An Lão phase 196
- `cal.1965-10-19.vietnam` · schlight-united-states-air-force · 101–103 · **PAGE OFF** · Schlight 101-03 give the siege's later days and the relief; the night attack of Oct. 19, "350 local irregular troops and a 12-man American advisory team", is on 99-100
- `cal.1965-02-10.vietnam` · staaveren-gradual-failure · 21–22 · **WRONG** · Staaveren 21-22: Qui Nhơn Feb. 10, 23 killed; Ball, Thompson, Humphrey; Flaming Dart II Feb. 11 from the three carriers on Chánh Hòa; the VNAF's target Vu Con, Chấp Lễ only an alternate
- `cal.1965-06-12.vietnam` · staaveren-gradual-failure · 149 · **WRONG** · Staaveren 149: "On June 11, Quat resigned"; power to the National Leadership Council; the entry dates it June 12
- `cal.1965-12-15.vietnam` · staaveren-gradual-failure · 203 · **PARTIAL** · Staaveren 203: Uông Bí, about 15 percent of the electricity, the attack begun Dec. 15 with ninety aircraft; not the restrikes or the boiler house (203-04)
- `cal.1965-12-06.laos` · staaveren-u-s-air-force · 100–101 · **WRONG** · Staaveren 100: "The first Tiger Hound missions were flown on December 5"; Dec. 6 the defoliation begins (101); the entry has Dec. 6 with a bare "Check the day"
- `cal.1964-01-21.economy` · stein-fiscal-revolution-in-america · 453 · **PARTIAL** · Stein 453: the budget for fiscal 1965 "$97.9 billion", published Jan. 21; not the receipts, the deficit, the comparisons with 1964, defense or civilian employment
- `cal.1964-08-05.vietnam` · vietnam-victory-in-vietnam · 132, 461 n.20 · **PARTIAL** · Victory 132, 461 n.20: 64 sorties on four naval bases and the Vinh depot, eight aircraft down (the note's Check gives it); nothing of the carriers, Alvarez, Syracuse or the message
- `cal.1967-01-08.vietnam` · vietnam-victory-in-vietnam · 196–97 · **PARTIAL** · Victory 196-97: Cedar Falls Jan. 8, "over 30,000" troops, the Iron Triangle, the tunnels; not the units, Bến Súc, the 6,000 civilians or the free-fire zone
- `cal.1960-11-04.cuba` · watson-into-the-missile-age · 766 · **PARTIAL** · Watson 766: the plan's shift to an amphibious landing by 600-750 men and the camp in Guatemala; no Nov. 4 cable, no 60-man teams
- `cal.1967-07-26.economy-surcharge` · califano-triumph-and-tragedy-of · 244 · **SECONDHAND** · Califano, 244, cited as read "(by Gibbons's quotation)"; no copy in the owner's folder
- `cal.1967-05-19.vietnam-2` · cooper-lost-crusade · 375 · **SECONDHAND** · Cooper, 375, cited as read inside Gibbons's parenthetical; no copy
- `cal.1967-04-19.vietnam` · cooper-lost-crusade · 373–74 · **SECONDHAND** · Cooper, 373-74, cited as read; no copy
- `cal.1967-05-19.vietnam-air-war` · cooper-lost-crusade · 375: many more strikes before it was out of operation · **SECONDHAND** · Cooper, 375, cited as read; no copy
- `cal.1967-09-13.vietnam-pennsylvania` · gibbons-u-s-government-and · IV, 781 · **PARTIAL** · Gibbons 781: on Sept. 13 Kissinger gave Marcovich the message for Bộ; not the words "contained neither conditions nor threats" or "remains open" (FRUS's)
- `cal.1967-08-25.defense` · perry-four-stars · 162–64, 169 · **SECONDHAND** · Perry, 162-64, 169, cited as read "(by Gibbons's quotation)", with "Check: Perry's the only account read"; no copy

## Quotations

**Book and official-history patches: 366 quotations, every one checked.**

- 332 were matched exactly in the entry's own cited sources, and 17 more differ only in case or punctuation.
- The 17 left unmatched were read by eye. 5 are WRONG, and each is corrected in the patch:
  - `cal.1963-12-02.civil-rights-bill`: "has got to go"; the source has "I think it's got to go."
  - `cal.1963-12-13.economy`: "working on my budget"; the source prints "working in [sic] my budget".
  - `cal.1968-09-24.elections-1968`: "wanting "guts"" is not the source's phrase. Now in paraphrase.
  - `cal.1961-04-21.king`: "try again in late April" is O'Donnell's advice as the author reports it, not his words.
    Now in paraphrase.
  - `cal.1965-01-05.king`: "You know what it is"; the source has "You know what this is."
- About 17 are MINOR and are left as they stand.
- "Symbol and Substance" (cal.1966-05-09.robert-kennedy) was checked against the Record's heading, 112 Cong. Rec.,
  May 9, 1966.
- The statement of Oct. 23, 1962, was checked against the *Bulletin*, Nov. 12, 1962, 723.

**Gibbons patch: 666 quotations, every one checked.**

- 501 match exactly. 7 differ in case only. 94 match letter for letter but differ in the scan's OCR, punctuation or
  spacing. 7 more match piece by piece around an ellipsis.
- The 57 left were read by eye against Gibbons, FRUS and the Public Papers: 44 EXACT (OCR damage: "tom" for "torn",
  "T ou" for "You"), 11 MINOR and 2 WRONG.
- The two WRONG, both corrected:
  - `cal.1967-02-13.vietnam`: McNamara's "if they come back with a moderated no". Gibbons quotes only from "moderated
    no" on and gives the rest in his own words.
  - `cal.1967-06-13.defense`: Mahon's "the House of Representatives is in support of the war effort" is a
    paraphrase. Gibbons, IV, 761 prints "... in support of the prosecution of the war for freedom in Southeast Asia."
- Three of the MINOR are mended to the letter:
  - `cal.1967-06-07.economy-surcharge`: "a deficit for the magnitude projected", as printed.
  - `cal.1967-10-23.vietnam`: FRUS's "rid of all the excuses".
  - `cal.1967-12-04.vietnam`: Katzenbach's "a 'firebreak' issue", singular and said of York II alone.
- Attribution: 114 matches stood outside quotation marks in the nearest 260 characters, and all were read. Each is a
  block quotation or the speaker's own words, and none is Gibbons's narration put in another's mouth.

## Judgment

**The official-histories run (2026-10-23-official-histories): recheck it whole.**

- Its pages are mostly right, but the cites rarely carry the parenthetical the house rule needs: a history that gives
  the battle is cited for the entry's units, hours and aftermath too.
- One in six pinpoints is wrong on a fact, a date or a page:
  - Cosmas pt. 3, 449: Hastings dated June 15.
  - Futrell, 260: Bình Giã, the North Vietnamese regiments and Dec. 27.
  - Marolda, 472–73: Biên Hòa's casualties and aircraft.
  - Poole vol. 9, 169: the six MiGs.
  - Schlight, 195: Masher's opening day.
  - Van Staaveren, 21–22, 149, 100: the Vu Con barracks, Quát's resignation, the first Tiger Hound missions.
  - Kaplan, 213 and Poole vol. 9, 120: not there at all.
- Where the history disagrees with the entry, the run did not write the "Check:".
- The worst works: the two Cosmas volumes, Poole vol. 8 and vol. 9, Futrell, Van Staaveren, Schlight, Marolda.
- Kaplan, Drea, Watson and Schulimson are better (Schulimson 5/5).

**The Gibbons run (2026-10-24-book-gibbons): Gibbons IV holds well.**

- 24 of 25 hold, and one is PARTIAL.
- It cited works it never had as read cites with pinpoints: Califano, 244; Cooper, 373–74 and 375 (twice); Perry,
  162–64, 169, marked "(by Gibbons's quotation)" or "Cooper's account". The patch moves them behind "To check:",
  "(cited by Gibbons, IV, N)".
- Recheck its other cites to other works the same way: 39 such pinpoints, most already behind "To check:".
- The "Made public:" pointers to the Pentagon Papers and *U.S.–Vietnam Relations* (Book 10) are taken from Gibbons's
  notes and not checked here.

**The book runs: their pages hold.**

- Clean: Garrow (0/8), Caro, Zelizer, Schwartz, Nguyen, Perlstein, Jian (0/5 each).
- Every failure but one is PARTIAL, a missing parenthetical. The exception is Schlesinger, *Robert Kennedy*, 840:
  the entry's "foreseeable" where the book prints "conceivable".
- Recheck for parentheticals: Dittmer (3/5), Frankum (3/5), *Victory in Vietnam* (2/5), Johns (2/5) and Anthony (3/5,
  official histories).

## The patch

`inbox/2026-10-28-spot-check.yaml`, `patch: spot-check`: 68 edits, each with its base from `./bib show`.
`./bib merge --dry-run` gives 68 edited and no conflicts. It does four things:

- Adds a parenthetical where the page bears out part of the entry.
- Puts the right page where the page is off: Cosmas, 390–93, 10–12; Schlight, 99–103; Marolda, 472–73.
- Drops a cite the page does not bear out: Kaplan, 213; Poole vol. 9, 120.
- Adds "Check: <Surname> gives ..." where the page disagrees.

It also moves the secondhand cites behind "To check:", and corrects the seven quotations above and the three MINOR.
Nothing else is rewritten.

## Leads

- Watson, 350 names Gates's testimony before House Science and Astronautics, Jan. 25, 1960. The Check on
  cal.1960-01-26.defense can be narrowed.
- Gibbons, pts. II and III; *Current Documents*, 1963; the Pentagon Papers, USG and Gravel eds.: no copy reached.
  Their pinpoints (UNREAD or NO COPY above) are unchecked.
- cal.1967-09-25.vietnam-congress: "47 other Republicans" against Gibbons's footnote list of 24 cosponsors (IV, 803
  n.13). It was not in the sample. Check against the Record.
- Futrell's archive.org OCR is badly garbled. Read it from the page images.
