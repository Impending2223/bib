# Preston, *The War Council* (2006): the calendar's citations, and the book's notes

Card `w.preston-war-council`. Andrew Preston, *The War Council: McGeorge Bundy, the NSC, and Vietnam* (Harvard, 2006). The owner's copy (Drive, the file id in `notes/briefs/batch3-resume.md`, row "advisers"), 335 PDF pages, a born-digital text layer, read with `pdftotext -layout`; cited by the printed page. Offset: printed page = PDF page - 15 throughout (checked on the running folios, and on the page images of PDF 55, p. 40, and PDF 276, p. 261, the notes). Text pp. 1-248 (Introduction 1-10; ch. 1, 11-35, Bundy before 1961; ch. 2-9, 36-235; Epilogue 236-248); notes pp. 251-301, numbered by chapter; a bibliography of primary sources, 303-307. The PDF deleted when the run was done.

The first run (Oct. 29, 2026, patch `b3-preston`, merged Nov. 3: 389 entries added, 20 of them renumbered past the ledger's claims, 123 edited) read the text within the span and cited pp. 40-238, and left no book-check file. Its map named 543 records by `via` rows but registered none; the merger dropped the rows. This file is the second run's (Nov. 4, 2026, patches `inbox/2026-11-03-b3-preston-2.yaml` (400 ops: 3 entries, 1 edit, 396 map rows) and `-3.yaml` (80 map rows).

## The second run (Nov. 4, 2026)

1. The witness layer (R35-R43). Every note of chapters 2-9 and of the Epilogue to p. 238 (501 notes, 1,445 items) read off the notes' text layer, each note split into its items in the note's order (a, b, c ...; "ibid." the item before, across notes too; "idem" the author before), and each item registered:
   - a document, press item, oral history or interview: a row of `inbox/witnesses/2026-11-03-b3-preston-2.yaml` (826 rows), or, where the registry already holds the record, its row (159 edges: FRUS documents by their copies, and 23 archive documents by hand, `SAME` below);
   - a FRUS document cited by volume and page: identified by the TEI's page breaks (github.com/HistoryAtState/frus, the volumes cited, read for `<pb>`), then by date and the heading's words against the daybook; its `copies` names the document (`FRUS 1961–63, VIII, doc. 9`);
   - a work in the catalogue: the edge names its card (353 edges; no row); a work not in the catalogue: a row, one a work, the short forms joined to the full;
   - the edges: `sources/witnesses/by-work/preston-war-council.yaml`, `at` the page of the passage and the note, `pin` the cited witness's page as the note gives it. Nothing upstream was read: `read: false` throughout; the archive documents `open: not held`; a document with a FRUS copy `open: none known` (the copy is the series' to read).
2. The claim maps: the first run's 543 `via` rows (its src rows as they stood in `c6a4245`), 492 entries, mapped each to the note's item by the entry's own "cited by" text, the dates and the FRUS links (370 sure by date or link, 83 a note of one item), the rest read by hand against the note and the page. 535 rows on 477 entries, as `src` ops; a row on a card left out (a card is no witness row: the Preston row covers its units, the edge is kept). patch-check: 0 errors.
3. The pages the calendar does not cite, within chapters 2-9 and the Epilogue (36-39, 43, 46-47, 51, 54-55, 58-59, 74-76, 102, 130, 155, 161, 185, 189-191, 199, 208, 239-248): read for each dated event, set against the tree and the ledger. Three new entries: Bundy to the Ford Foundation, Mar. 1, 1966 (237, 240); Bundy to Johnson for a speech tying the policy to Kennedy's, Mar. 1965 (130); Thomson to Bowles, Sept. 1963 (185).

## The map rows read by hand (R33, R34)

| entry | the first run's row | ruling |
|---|---|---|
| cal.1961-02-18.transition-and-staff | 40 n.9b, 9c | note 9: R. Johnson's paper; Hirsch to Bundy; FRUS's footnote on the order; the signing statement in the Papers: n.9c, n.9d |
| cal.1962-04-04.vietnam-2 | 112 n.30: B | the "conspicuous" words are note 29 (p. 111), Bowles to Kennedy, Apr. 4, 1962: 111 n.29b |
| cal.1965-02-07.vietnam-4 | 174 n.42c: B | "Not much of a government is required" is McNaughton's, note 41 (p. 174), not Sharp's: 174 n.41 |
| cal.1965-02-06.soviet-union | 184 n.66: C | the Soviet statement is unit D, not C: 184 n.66a: D |
| cal.1964-06.intelligence | 152 n.52b | the passage is p. 151, the call p. 152: the note's edges at 151 |
| cal.1961-11-27.vietnam-2 | 87 n.31c, the note citing 85 | the Heeney passage is p. 87: the note's pinpoint corrected (an edit, base 11e471db) |
| cal.1965-08-05.vietnam-pause-2 | 218 n.24: B | the entry has one unit: all |
| cal.1962-08-18.vietnam | 108 n.17c | Forrestal to Bundy and Kaysen, Aug. 18, 1962 (Harriman's papers held by Bird): 107 n.17c |
| cal.1962-08.vietnam, 1962-11.vietnam | 108 n.19a | Jones, *Death of a Generation*, 241, a card: no row |
| cal.1963-12.vietnam-congress, 1964-02, 1964-05 | 149 n.46a, 47a | Johns's article, a card: no row |
| cal.1965-05-15.latin-america, 1965-05-18 | 201 n.38 | Rusk's memoir, a card: no row |
| cal.1965-07-01.vietnam | 205 n.45 | the three papers apart: Ball's (D), Rusk's (F), William Bundy's (E) |
| cal.1964-05-22.vietnam | 147 n.42a | Bundy to Johnson of May 27, as the note gives it (the entry's Check stands: FRUS's paper is May 22) |

`SAME` (the registry's rows that are Preston's records): Acheson to Kennedy, Apr. 3, 1961; Bundy to Kennedy, Apr. 4, 1961; Rostow to Bundy, Jan. 30, 1961; Sorensen to Kennedy, Apr. 28, 1961; Rusk and McNamara to Kennedy, Nov. 11, 1961; Komer to Bundy, and R. Johnson to Bundy, Oct. 31, 1961; Bowles to Kennedy, June 13, 1962; Kennedy to Lodge, Sept. 18, 1963 (FRUS IV, doc. 128); Mansfield to Johnson, Feb. 1 and Dec. 9, 1964; and twelve of Bundy's memoranda to Johnson, 1964-66, McNaughton to McNamara, Nov. 9, 1965.

## Passed over

Made by reading pp. 36-39, 43, 46-47, 51, 54-55, 58-59, 74-76, 102, 130, 155, 161, 185, 189-191, 199, 208 and 236-248 sentence by sentence for a date; each dated event the calendar holds took no row here.

| page | date | event | why |
|---|---|---|---|
| 37 | Nov. 1963 | the NSC staff after Kennedy's death (a summary) | not an event: a characterization |
| 39 | Dec. 1960 | Rusk's appointment; Bundy not considered for State | before the span |
| 43 | Jan. 1962 | Forrestal on the staff for the Far East | in the calendar, cal.1962-01-05.transition-and-staff-nsc (Schlesinger's recommendation) |
| 161 | Nov. 1964 | the Working Group's options "converged" (the Pentagon Papers' words) | in the calendar, from cal.1964-11-03.vietnam |
| 189-190 | Feb. 1965 | the turn of February (a summary) | not an event |
| 208 | July 1965 | Bundy and the troop decision (a summary) | not an event: a summary of the decision the calendar holds in July 1965 |
| 237 | May, Oct. 1967 | Bundy's two memoranda to Johnson against de-escalation | in the calendar, cal.1967-05-03.vietnam-program-5, cal.1967-10-17.vietnam |
| 238 | Nov. 1967 | the senior advisers' meeting | in the calendar, cal.1967-11-02.vietnam |
| 245 | June 1965 | Brzezinski with Bundy in the debate with Morgenthau | in the calendar, cal.1965-06-21.vietnam-support |
| 239-248 | 1969 on | Bundy at the Ford Foundation; Kissinger and his successors | after the span |

## The press (R13)

None: Preston gives no day's coverage.

## Leads

National
- The card `w.bird-color-of-truth` carries a note that is William Bundy's role line ("Asst. SecDef Int'l Sec. Affs. 29 Nov. 1963 to 14 Mar. 1964. Asst SecState E. Asia & Pac. 16 Mar. 1964 to 4 May 1969."), not a note on the book: a listing's or Part III's text carried onto the card? For the merger (works/b.yaml).
- Preston's interviews (Kaysen, Katzenbach, Bator, McNamara, Hughes, Thomson, 1999) and Joseph Kraft's interviews with Forrestal (Apr. 8, July 28, Aug. 14, 1964), registered `open: not held`: where Kraft's transcripts are (Preston names no repository).
- Forrestal to Bundy and Kaysen, Aug. 18, 1962, and Forrestal to Kennedy, Aug. 28, 1963: in Harriman's papers held privately by Kai Bird (Preston 107 n.17, 124 n.64); Bird's notes may say where they went.
- The Mar. 1965 memorandum of Bundy's for a speech on Kennedy's policy (cal.1965-03.vietnam-support): Preston names no document; Small, *Johnson, Nixon, and the Doves*, 40, and Reeves, 660-61, may.
