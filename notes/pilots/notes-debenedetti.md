# Pilot: dating the calendar's loose entries by the endnotes, DeBenedetti and Chatfield, *An American Ordeal* (Nov. 13, 2026)

The patch: `inbox/2026-11-13-pilot-notes-debenedetti.yaml` (patch `pilot-notes-debenedetti`), 38 ops, `./bib patch-check` 0 errors, 0 warnings: 7 `edit` (the dated rows, with `base:`), 15 `check` and 16 `to-check` (additive, no `base`). The two models (Bigart, Sully) were done by hand and are not in the patch; row 24 below is Sully.

## Counts by ruling (134 rows)

| Ruling | Rows |
|---|---|
| Dated to the day by the note | 6 (rows 1, 7, 26, 31, 44, 98) |
| Dated to the day by the page itself (not the note) | 1 (row 59) |
| Bounded by a paper's or a document's report | 11 |
| Weekly issue | 1 (row 79; the model, row 25, is a second) |
| Month only | 5 |
| Nothing | 106 |
| Disagrees (check op) | 3 |

Of the 106 "nothing": about 60 were read (the page text read for the sentence, no superscript on it or an undated note); the rest were screened (no note within one page carried the entry's month or two of its words) and the page not read. A few carry a lead and are listed under "Not applied" below. So the rate of notes that settle a loose entry: 7 of 134 to the day (5 percent), 18 to the day or bounded (13 percent), and some of those weak.

## What the patch does, and where it departs from the brief

- **Striking a Check is refused.** `patch-check` (patchaudit `drops()`) errors on an `edit` whose new note lacks any "Check:" sentence of the note it is based on, so "strike `Check: the day`" cannot pass. The seven date edits therefore keep the old Check sentence verbatim and add "Settled: ... by 416 n.52." after it. Someone should strip `Check: the day(s). Settled: ...` in a sweep (the date and `when` are already set); or the tool should take an edit that sets `date` as striking "Check: the day". The first draft with the Checks struck had 19 such errors.
- Rows where the note only bounds the day carry an additive `check` (the narrowed sentence, with the note's number) and `to-check` (the paper, linked on the Times's TimesMachine where it is the *Times*); the old "Check: the day" stays beside it.
- The dated rows' `to-check` items are inside the rewritten `n`, as in the models. Nothing in the patch touches `c` or `src`.
- Two dated rows keep a Check for a part the note does not settle: row 7 (May 26): the entry also holds the withdrawals of Gilmore, Meacham, Pauling and Muste, which 416 n.60 puts later (Gilmore's letter June 27, 1960); row 44 (Dec. 22, Lippmann): the note gives the column's date in the Lippmann Papers, three pieces under one number.
- Entries holding two events (the owner's span rule): 7 (the board's act and the withdrawals), 38 (the SPU closing its office and Turn Toward Peace's autopsy), 99 (McReynolds's and Bloomstein's resignations, two letters two weeks apart), 107 (Spock leaving SANE, and Pickus and Temple's leaving, whose letter is Oct. 21). Not split here.

## Not applied (leads for the lead)

- Rows 5, 6 (Dodd's speech, Abrams before the Internal Security Subcommittee, May 1960): 416 n.61 cites the *Times* of May 26, 1960, at 11, but its superscript sits on the page after the October report; it may be the hearings' paper. Unresolved.
- Row 42 (Nixon on Humphrey, "very dedicated radical"): 425 n.66 cites four *Times* issues, none tied to the quotation.
- Row 103 (Mobe press conference, Aug. 1967): 441 n.81 cites "Press Statement Issued Aug. 28," *Mobilizer*, Sept. 1, 1967; the superscript was not tied to the press conference. Likely Aug. 28.
- Row 79 (Goodwin's committee, Oct. 1966): 436 n.82 cites Goodwin in *Christianity and Crisis*, Oct. 31, and *New Leader*, Nov. 7, 1966; `to-check` only (the entry's own note has Goodwin's address of Sept. 16).
- Row 32 (Church's resolution): the calendar holds "Church offers S. Res. 196, with Carlson and twenty-one other" at Sept. 12, 1963 (`cal.1963-09-12.vietnam`); the loose entry, `cal.1963-09.vietnam-congress` (DeBenedetti: thirty-two cosponsors), is the same event. Not combined; the cosponsor count may be a variant.
- Rows 30 (Ministers Committee's petition) and 32: 422 n.21 gathers *Christian Century*, the Record of Sept. 10 (16599) and Donald Harrington's recollection of the Ministers Committee, so it may date the petition, not the resolution; the superscript sits at the resolution.
- Rows already carrying a day whose Check the notes leave alone: 45 (Dec. 29 v. Stone's meeting Dec. 30), 63 (Gainesville), 65 (South Boston), 81, 86, 90, 92, 95, 96, 111, 115, 127. Row 115 (Project Resistance, 199 n.125: memorandum of Oct. 8) and rows 92, 95 (174–75 nn.22, 23: broadcasts of Apr. 14–16; letter of Feb. 24) already cite their notes.

## Table

| Row | Entry | Old date | The note read | Ruling | New date |
|---|---|---|---|---|---|
| 1 | 1960-03.testing | 1960-03 | 416 n.52 | dated to the days | Mar. 10–13 |
| 2 | 1960-04.students | 1960-04 | no superscript on the sentence, or its note is undated | nothing | — |
| 3 | 1960-04.testing | 1960-04 | no superscript on the sentence, or its note is undated | nothing | — |
| 4 | 1960-05.testing | 1960-05 | no superscript on the sentence, or its note is undated | nothing | — |
| 5 | 1960-05.antisubversion | 1960-05 | no note on the sentence; 416 n.61 (NYT May 26, 1960, at 11) sits by the October report, may cover the May hearings (not applied) | nothing | — |
| 6 | 1960-05.antisubversion-2 | 1960-05 | as row 4: 416 n.61 uncertain (not applied) | nothing | — |
| 7 | 1960-05.testing-2 | 1960-05 | 416 n.58 (n.60) | dated to the day (the board); the withdrawals later (Gilmore, June 27: Check kept) | May 26 |
| 8 | 1960-05.defense | 1960-05 | 417 n.71 by estimate (Muste, Liberation May 1960; Peck, May–June 1960) | month only | — |
| 9 | 1960-06.students | 1960-06 | no superscript on the sentence, or its note is undated | nothing | — |
| 10 | 1960-07.democratic-party | 1960-07 | no superscript on the sentence, or its note is undated | nothing | — |
| 11 | 1960-07.republican-party | 1960-07 | no superscript on the sentence, or its note is undated | nothing | — |
| 12 | 1960-08.students | 1960-08 | 415 n.48 (minutes of Aug. 27–28, 1960 SPU meeting; not said to be the merger) | month only; Check narrowed, minutes put behind To check | — |
| 13 | 1960-10.testing | 1960-10 | no superscript on the sentence, or its note is undated | nothing | — |
| 14 | 1960-10.antisubversion | 1960-10 | no superscript on the sentence, or its note is undated | nothing | — |
| 15 | 1960-12.testing | 1960-12 | no superscript on the sentence, or its note is undated | nothing | — |
| 16 | 1961-04.cuba-bay-of-pigs-7 | 1961-04 | no superscript on the sentence, or its note is undated | nothing | — |
| 17 | 1961-04.testing | 1961-04 | no superscript on the sentence, or its note is undated | nothing | — |
| 18 | 1961-05.testing-2 | 1961-05 | no superscript on the sentence, or its note is undated | nothing | — |
| 19 | 1962-03.testing | 1962-03 | no superscript on the sentence, or its note is undated | nothing | — |
| 20 | 1962-03.testing-2 | 1962-03 | no superscript on the sentence, or its note is undated | nothing | — |
| 21 | 1962-03.testing-3 | 1962-03 | no superscript on the sentence, or its note is undated | nothing | — |
| 22 | 1962-04.testing-2 | 1962-04 | no superscript on the sentence, or its note is undated | nothing | — |
| 23 | 1962-05.testing-2 | 1962-05 | no superscript on the sentence, or its note is undated | nothing | — |
| 24 | 1962-06.testing-2 | 1962-06 | no superscript on the sentence, or its note is undated | nothing | — |
| 25 | 1962-07.press-and-broadcasting-3 | 1962-08-20 (Aug. 20) | 422 nn.7, 9 | weekly issue (model, done by hand) | Aug. 20 |
| 26 | 1962-10.missile-crisis-2 | 1962-10 | 418 n.23 | dated to the day (SANE statement) | Oct. 24 |
| 27 | 1962-12.testing | 1962-12 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 28 | 1963-03.war-opposition | 1963-03 | no superscript on the sentence, or its note is undated | nothing | — |
| 29 | 1963-05.war-opposition | 1963-05 | 422 n.13 (NYT July 14, 1963, sec. 6, at 2) | disagrees: the page says two months after March; check op | — |
| 30 | 1963-08.war-opposition | 1963-08 | no superscript on the sentence, or its note is undated | nothing | — |
| 31 | 1963-09.war-opposition | 1963-09 | 422 n.17 | dated to the day (board statement) | Sept. 27 |
| 32 | 1963-09.vietnam-congress | 1963-09 | 422 n.21 (Cong. Rec. Sept. 10, 1963, at 16599) | disagrees: the calendar holds Church's S. Res. 196 on Sept. 12 (cal.1963-09-12.vietnam, an apparent duplicate); check op, no date change | — |
| 33 | 1963-10.war-opposition | 1963-10 | no superscript on the sentence, or its note is undated | nothing | — |
| 34 | 1963-10.war-opposition-2 | 1963-10 | 422 n.18 (SPU form letter, ca. Oct. 1963) | month only | — |
| 35 | 1964-03.students | 1964-03 | no superscript on the sentence, or its note is undated | nothing | — |
| 36 | 1964-03.war-opposition-2 | 1964-03 | no superscript on the sentence, or its note is undated | nothing | — |
| 37 | 1964-04.war-opposition | 1964-04 | no superscript on the sentence, or its note is undated | nothing | — |
| 38 | 1964-06.students | 1964-06 | 424 n.52 | bounded: Thomas's report dated June 30, 1964 (autopsy; entry also holds the SPU office closing) | — |
| 39 | 1964-07.war-opposition | 1964-07 | no superscript on the sentence, or its note is undated | nothing | — |
| 40 | 1964-07.war-opposition-2 | 1964-07 | no superscript on the sentence, or its note is undated | nothing | — |
| 41 | 1964-09.elections-1964-johnson-4 | 1964-09 | no superscript on the sentence, or its note is undated | nothing | — |
| 42 | 1964-10.elections-1964-goldwater | 1964-10 | 425 n.66: four NYT items (Sept. 11, Sept. 30, Oct. 2x, Oct. 25), none tied to the quotation | nothing | — |
| 43 | 1964-11.war-opposition-2 | 1964-11 | no superscript on the sentence, or its note is undated | nothing | — |
| 44 | 1964-12.war-opposition | 1964-12 | 426 n.79 | dated to the day (Lippmann column); Check kept for publication day and the quoted words | Dec. 22 |
| 45 | 1964-12-29.students | 1964-12-29 (Dec. 29) | no note bears on Dec. 29 v. 30 | nothing | — |
| 46 | 1965-02.war-opposition | 1965-02 | no superscript on the sentence, or its note is undated | nothing | — |
| 47 | 1965-02.students | 1965-02 | no superscript on the sentence, or its note is undated | nothing | — |
| 48 | 1965-04.democratic-party | 1965-04 | no superscript on the sentence, or its note is undated | nothing | — |
| 49 | 1965-05.students | 1965-05 | no superscript on the sentence, or its note is undated | nothing | — |
| 50 | 1965-05.war-opposition | 1965-05 | no superscript on the sentence, or its note is undated | nothing | — |
| 51 | 1965-05.war-opposition-2 | 1965-05 | no superscript on the sentence, or its note is undated | nothing | — |
| 52 | 1965-07.war-opposition | 1965-07 | no superscript on the sentence, or its note is undated | nothing | — |
| 53 | 1965-08.war-opposition | 1965-08 | 430 n.90 | bounded: Berkeley Barb Aug. 13, "August 12 Black Day" | — |
| 54 | 1965-09.students | 1965-09 | no superscript on the sentence, or its note is undated | nothing | — |
| 55 | 1965-10.vietnam-support | 1965-10 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 56 | 1965-11.war-opposition | 1965-11 | no superscript on the sentence, or its note is undated | nothing | — |
| 57 | 1965-11.war-opposition-2 | 1965-11 | no superscript on the sentence, or its note is undated | nothing | — |
| 58 | 1965-12.students | 1965-12 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 59 | 1966-01.war-opposition | 1966-01 | page 145 itself ("on 11 January"); 433 n.14 not relied on | dated by the page, not the note | Jan. 11 |
| 60 | 1966-01.war-opposition-3 | 1966-01 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 61 | 1966-02.war-opposition-3 | 1966-02 | no superscript on the sentence, or its note is undated | nothing | — |
| 62 | 1966-02.war-opposition-4 | 1966-02 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 63 | 1966-02-12.war-opposition | 1966-02-12 (Feb. 12) | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 64 | 1966-03.war-opposition | 1966-03 | no superscript on the sentence, or its note is undated | nothing | — |
| 65 | 1966-03-31.draft | 1966-03-31 (Mar. 31) | no superscript on the sentence, or its note is undated | nothing | — |
| 66 | 1966-04.war-opposition | 1966-04 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 67 | 1966-04.war-opposition-2 | 1966-04 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 68 | 1966-04.war-opposition-4 | 1966-04 | no superscript on the sentence, or its note is undated | nothing | — |
| 69 | 1966-04.war-opposition-5 | 1966-04 | no superscript on the sentence, or its note is undated | nothing | — |
| 70 | 1966-04.war-opposition-6 | 1966-04 | no superscript on the sentence, or its note is undated | nothing | — |
| 71 | 1966-04.war-opposition-7 | 1966-04 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 72 | 1966-05.war-opposition | 1966-05 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 73 | 1966-05.students | 1966-05 | no superscript on the sentence, or its note is undated | nothing | — |
| 74 | 1966-07.civil-rights-organizations | 1966-07 | no superscript on the sentence, or its note is undated | nothing | — |
| 75 | 1966-07.democratic-party | 1966-07 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 76 | 1966-08.draft-2 | 1966-08 | no superscript on the sentence, or its note is undated | nothing | — |
| 77 | 1966-08.students-4 | 1966-08 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 78 | 1966-08.draft-3 | 1966-08 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 79 | 1966-10.democratic-party | 1966-10 | 436 n.82 (attachment uncertain) | weekly issues, two (Christianity and Crisis Oct. 31; New Leader Nov. 7); to-check only | — |
| 80 | 1966-10.war-opposition | 1966-10 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 81 | 1966-11-08.war-opposition | 1966-11-08 (Nov. 8) | no dated note | nothing | — |
| 82 | 1966-12.students | 1966-12 | no superscript on the sentence, or its note is undated | nothing | — |
| 83 | 1966-12.draft | 1966-12 | no superscript on the sentence, or its note is undated | nothing | — |
| 84 | 1966-12.vietnam-4 | 1966-12 | no superscript on the sentence, or its note is undated | nothing | — |
| 85 | 1966-12.war-opposition | 1966-12 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 86 | 1966-12-27.war-opposition | 1966-12-27 (Dec. 27) | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 87 | 1967-01.war-opposition | 1967-01 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 88 | 1967-02.students | 1967-02 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 89 | 1967-02.intelligence | 1967-02 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 90 | 1967-02-11.war-opposition | 1967-02-11 (Feb. 11) | no note on the death | nothing | — |
| 91 | 1967-02-15.war-opposition | 1967-02-15 (Feb. 15) | 438 n.13 | bounded: Baltimore Sun Feb. 16 | — |
| 92 | 1967-02-24.war-opposition | 1967-02-24 (Feb. 24) | 175 n.23 (letter of Feb. 24) already the entry's date | nothing | — |
| 93 | 1967-03.war-opposition | 1967-03 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 94 | 1967-04.democratic-party | 1967-04 | no superscript on the sentence, or its note is undated | nothing | — |
| 95 | 1967-04-14.war-opposition | 1967-04-14 (Apr. 14–16) | 174 n.22 (broadcasts of Apr. 14, 15, 16) already cited; does not pick one | nothing | — |
| 96 | 1967-04-15.vietnam-support | 1967-04-15 (Apr. 15) | no superscript on the sentence, or its note is undated | nothing | — |
| 97 | 1967-05.students | 1967-05 | no superscript on the sentence, or its note is undated | nothing | — |
| 98 | 1967-05.democratic-party-2 | 1967-05 | 440 n.59 | dated to the days (board meeting) | May 19–21 |
| 99 | 1967-06.war-opposition-2 | 1967-06 | 441 n.87 | bounded: two letters, June 13 and June 27 | — |
| 100 | 1967-07.war-opposition | 1967-07 | 441 n.88 by estimate (Homer Jack, report on the July 1967 meeting) | month only | — |
| 101 | 1967-07.war-opposition-2 | 1967-07 | 440 n.70 | bounded: NYT July 9 | — |
| 102 | 1967-08.democratic-party-2 | 1967-08 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 103 | 1967-08.war-opposition | 1967-08 | 441 n.81 cites a Mobilizer "Press Statement Issued Aug. 28"; the superscript could not be tied to the press conference (not applied) | nothing | — |
| 104 | 1967-08.war-opposition-2 | 1967-08 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 105 | 1967-09.war-opposition | 1967-09 | 442 n.96 | bounded: National Guardian Sept. 23 | — |
| 106 | 1967-09.war-opposition-2 | 1967-09 | no superscript on the sentence, or its note is undated | nothing | — |
| 107 | 1967-09.war-opposition-3 | 1967-09 | 442 n.100 (Heller and Pickus to Keys, Oct. 21, 1967) | disagrees: Pickus and Temple's leaving falls after September; check op | — |
| 108 | 1967-09.war-opposition-4 | 1967-09 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 109 | 1967-09.war-opposition-5 | 1967-09 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 110 | 1967-09.democratic-party-2 | 1967-09 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 111 | 1967-09-02.war-opposition | 1967-09-02 (Sept. 2–4) | no dated note | nothing | — |
| 112 | 1967-10.vietnam-congress-5 | 1967-10 | no superscript on the sentence, or its note is undated | nothing | — |
| 113 | 1967-10.war-opposition-4 | 1967-10 | no superscript on the sentence, or its note is undated | nothing | — |
| 114 | 1967-10.war-opposition-5 | 1967-10 | 442 n.106 | bounded: NYT Oct. 16 | — |
| 115 | 1967-10-08.intelligence | 1967-10-08 (Oct. 8) | 199 n.125 (memorandum of Oct. 8) already the entry's date | nothing | — |
| 116 | 1967-11.labor | 1967-11 | no superscript on the sentence, or its note is undated | nothing | — |
| 117 | 1967-11.war-opposition | 1967-11 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 118 | 1967-12.war-opposition-2 | 1967-12 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 119 | 1968-01.war-opposition-2 | 1968-01 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 120 | 1968-01.opinion | 1968-01 | 443 n.5 (Good Housekeeping, Jan. 1968) | month only (monthly issue) | — |
| 121 | 1968-02.war-opposition-2 | 1968-02 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 122 | 1968-02.war-opposition-3 | 1968-02 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 123 | 1968-02.war-opposition-4 | 1968-02 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 124 | 1968-03.elections-1968-mccarthy | 1968-03 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 125 | 1968-05.intelligence | 1968-05 | 446 n.76 | bounded: Brennan to Sullivan memo May 9 | — |
| 126 | 1968-05.draft | 1968-05 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 127 | 1968-06-09.students | 1968-06-09 (June 9–15) | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 128 | 1968-07.war-opposition | 1968-07 | no superscript on the sentence, or its note is undated | nothing | — |
| 129 | 1968-08.war-opposition | 1968-08 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |
| 130 | 1968-08.war-opposition-2 | 1968-08 | 448 n.110 | bounded: NYT Aug. 25 | — |
| 131 | 1968-09.war-opposition-2 | 1968-09 | 448 n.111 | bounded: NYT Oct. 12 (attachment uncertain) | — |
| 132 | 1968-09.elections-1968-chicago-streets | 1968-09 | 447 n.89 | bounded: NYT Sept. 16 (attachment uncertain) | — |
| 133 | 1968-10.democratic-party | 1968-10 | no superscript on the sentence, or its note is undated | nothing | — |
| 134 | 1968-12.war-opposition | 1968-12 | no dated note within ±1 page matches the month or the matter (screened, superscript not read) | nothing | — |

## How the tool did

- **Estimates.** Of the 23 notes I could tie to a sentence (by the page text, and by the page image at 130–160 dpi where the text layer lost the superscript), the tool's estimate for the note was within one page of the sentence's page in 22. The failure: ch. 4 n.13 (the open letter of May 1963, p. 87), estimated at p. 85, so `page 87` did not list it (the *Times* of July 14, 1963, which disagrees with the page). The estimate drifts where a chapter's notes are dense on a page and sparse on the next.
- **What the tool does not do is the hard part**: say which note a sentence carries. About two thirds of the time went to finding the sentence on the page, reading its superscript and matching the number to a note. The OCR superscripts are "^^", "'^", "*#", "5^" for 52; at 100 dpi the images were no better; a 150 dpi crop was legible. I built a screen (notes within one page whose text names the entry's month or shares two of its words) and read the sentence and the note against each other only for the hits.
- **Index faults seen.** (1) A note number OCR'd as "53-" or "6^." merges two notes into one (n.52 and n.53; n.66 and n.67), and `page` then prints one note with both sources; (2) `page` cuts a long note short; `note CH N` prints more; (3) OCR digits in dates ("I960", "19^0", "2^ Oct.") break any date match; (4) `folios` fills the picture sections (PDF 108–119, 183–200) with interpolated folios, so a folio→PDF lookup from `folios` lands on a plate (folio 84 is PDF 118, not 106); I rebuilt the map from the running heads; (5) the printed folio is not PDF − 22 past the first plates (offset 34, then 52).
- **Time:** about half an hour of wall clock for the 134, by a reader reading the notes and writing the patch; tokens not counted (a few hundred thousand).

## What a sweep of the other books needs

1. A `sentence` command: given a page and a few words, print the lines around them with the superscript's number read from a 150 dpi crop of the line (OCR of superscripts only), and the note of that number. That is the step that was by hand.
2. The merged-note repair: renumber by sequence (a note numbered "53-" between 52 and 54 is 53); print notes whole.
3. The folio map from the running heads, with plates left unmapped, and a lookup `folio → PDF`.
4. `patch-check` should let an `edit` that sets `date` (or says so) strike "Check: the day"; as it stands the strike is refused (patchaudit `drops()`), and the entries keep a settled Check that a sweep must remove.
5. Forms of notes this book did not show: footnotes at the page foot (no endnote section), notes keyed by page and phrase ("84 Bigart's survey:"), "ibid." chains (a dated source named once, the entry cites the third "Ibid."), and reference lists by author-date. The tool's three forms are heads, page-keyed and chapter-numbered; those four would be new.
6. A tool-side rule for "the page itself dates it": one entry in this book had "Check: the day" where the cited page had a day (e.g. row 59, Jan. 11, 1966); the notes were not needed. A pass over the page text for day-level dates near each loose entry would find them before the notes are read.
