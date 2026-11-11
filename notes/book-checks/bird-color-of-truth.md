# Bird, *The Color of Truth* (1998): the book against the calendar

Card `w.bird-color-of-truth`. Kai Bird, *The Color of Truth: McGeorge Bundy and William Bundy: Brothers in Arms* (Simon & Schuster, 1998). The owner's copy (Drive, the file id in `notes/briefs/batch3-resume.md`, row "advisers"), a scan of 519 PDF pages with an OCR text layer (ragged spacing; a few folios misread), read with `pdftotext -layout`; cited by the printed page. Offset: printed page = PDF page - 3 to p. 224 (PDF 227); the plates PDF 228-243, unpaginated; then printed page = PDF page - 19 to the end (p. 225 = PDF 244; checked at the chapter openings, pp. 185, 226, 250, 270, 301, 350, 376, 396, and the notes, p. 410, against the contents). The PDF deleted when the run was done.

No earlier run read the book (the first batch's Preston reader cited it through Preston's notes only). This run: Nov. 4, 2026, patch `inbox/2026-11-03-b3-bird-2.yaml` (96 ops: 69 entries, 21 cites, 5 checks, 1 edit; patch-check 0 errors, 31 warnings, each a same-day flag of a distinct event, read pair by pair).

## How it was read

Chapters 8 (from 1960) to 16, pp. 181-409, sentence by sentence for a date (a day, a month, a season or a year with an event), 440 sentences; each event set against the tree and the ledger (`./bib ledger find`), the paragraph around it read where an event was dated. Chapter 15 (the Ford Foundation) and 16 (after 1969) read so too. Pages 1-180 (to 1960) out of the span but for pp. 140-153 and 181-182 (Harvard and the Goals commission, 1960), read the same way.

## The calendar's citations (R33)

| entry | the cite | the book | ruling |
|---|---|---|---|
| cal.1961-02-18.transition-and-staff | To check | no word of the OCB; the NSC's simplification, 185 | left in To check (not plainly off) |
| cal.1961-11-28.vietnam-2 | 221 (via Preston) | 221: Galbraith's Saigon cable of late November, not the New Delhi letter | holds for the cable (cal.1961-11-20); left |
| cal.1963-08-24.vietnam | To check | 254: Harriman to Forrestal, Hilsman's draft | cited, 254 |
| cal.1964-05-01.vietnam | via Preston | 280: the words, to McNaughton and Bundy | cited, 280, all |
| cal.1964-11-01.vietnam | To check | 293: the attack; 72 wounded | cited, 293; Check: 72 wounded |
| cal.1965-01-27.vietnam | To check | 304: the meeting, Bundy's memorandum | cited, 304 |
| cal.1965-02-07.vietnam | To check | 306-07: eight killed, 126 wounded, 2 a.m. | cited, 306-07; Check |
| cal.1965-03-24.vietnam-3 | 315 | 315: the memorandum of Mar. 30 on a Development Corporation, not this paper | Check written; new entry for Mar. 30 |
| cal.1965-05-15.students | To check | 318, 324 | cited |
| cal.1965-05-15.latin-america | To check | 324: the mission, no settlement | cited |
| cal.1965-06-15.students | 323 | "Earlier in June," Lowell Lecture Hall | holds |
| cal.1967-06-07.middle-east | To check | not treated (the war of June 1967 named once, 384, on Podhoretz) | taken out (edit, base 48bf15d0) |
| cal.1968-10-12.vietnam | To check | 371 | cited |

Also cited: cal.1964-12-09.vietnam-congress (296; Check: Bird dates Fulbright's warning Dec. 4), cal.1965-06-21.vietnam-support (321), cal.1965-06-30.vietnam (330-31), cal.1965-07-01.vietnam (334, unit E), cal.1965-11-07 and -14.transition-and-staff (343-44), cal.1966-01-06.vietnam (345), cal.1966-03-01.transition-and-staff (347; the Preston run's new entry), cal.1967-05-03.vietnam-program-5 (357; Check: Bird dates the letter May 4), cal.1964-07-29.robert-kennedy-2 (297), cal.1967-07.states-and-cities-nyc (383), and Branch's pending cal.1966-08-01.press-and-broadcasting (378) and cal.1966-08-02.civil-rights-organizations (380) (R49: the same events, claimed first).

Withdrawn after the claim (duplicates found after `./bib ledger add`; the claims stand in the ledger, no entry follows): cal.1964-12-04.vietnam-congress (Fulbright's warning: cal.1964-12-09.vietnam-congress), cal.1964-07.elections-1964-7 (Bundy's call to Robert Kennedy: cal.1964-07-29.robert-kennedy-2), cal.1966-01-06.vietnam-2 (McNamara at Schlesinger's: cal.1966-01-06.vietnam). For the merger: prune them.

## New entries (69)

- 1960-02 `cal.1960-02.program`: W. Bundy, Goals staff director
- 1960-06 `cal.1960-06.elections-1960-13`: W. Bundy briefs Kennedy on Goals
- 1960-11 `cal.1960-11.program`: W. Bundy sends Goals to Kennedy
- 1960-12 `cal.1960-12.transition-and-staff-nsc`: Lippmann with Kennedy, Bundy for State
- 1960-12 `cal.1960-12.transition-and-staff-nsc-2`: Kennedy offers Bundy under secretaryship
- 1960-12-30 `cal.1960-12-30.transition-and-staff-nsc`: Bundy accepts the Special Assistant post
- 1961-01 `cal.1961-01.defense`: Ellsberg briefs Bundy on the war plans
- 1961-07-06 `cal.1961-07-06.berlin-and-vienna`: Raskin to Bundy on Germany
- 1961-07-19 `cal.1961-07-19.berlin-and-vienna-2`: Riesman and Fromm letter on Germany
- 1961-08-22 `cal.1961-08-22.berlin-and-vienna-2`: Kaysen to Bundy on Berlin
- 1961-09-01 `cal.1961-09-01.berlin-and-vienna`: Harriman to Kennedy, Germany divided
- 1961-10 `cal.1961-10.testing`: ACDA Foster Panel: ceiling of 1,000
- 1961-10 `cal.1961-10.press-and-broadcasting`: Lippmann: Eisenhower thirty years younger
- 1962-04 `cal.1962-04.democratic-party`: The Liberal Papers published
- 1962-05-10 `cal.1962-05-10.laos`: Eisenhower to Bundy and McCone on Laos
- 1962-07-25 `cal.1962-07-25.cuba`: Lansdale reports on Mongoose intervention planning
- 1962-09-14 `cal.1962-09-14.cuba`: Kennedy and JCS on air attack plan
- 1962-09-19 `cal.1962-09-19.cuba`: Bundy note to Lansdale on contingencies
- 1962-10-01 `cal.1962-10-01.cuba`: McNamara orders Dennison to prepare blockade
- 1962-10-05 `cal.1962-10-05.cuba`: Bundy to McCone: policy not clear
- 1962-11 `cal.1962-11.press-and-broadcasting`: Chalmers Roberts: Bundy rates an A
- 1963-10-05 `cal.1963-10-05.vietnam-4`: Bundy to Lodge: keep sanctions secret
- 1963-10-08 `cal.1963-10-08.vietnam`: CINCPAC to Bundy on withdrawal by units
- 1963-11-21 `cal.1963-11-21.transition-and-staff-nsc`: Bundy declines Yale
- 1963-11-21 `cal.1963-11-21.vietnam-2`: Bundy to W. Bundy on the draft NSAM
- 1963-11-22 `cal.1963-11-22.transition-and-staff`: W. Bundy confirmed ASD/ISA
- 1963-11-24 `cal.1963-11-24.succession-2`: Bundy, RFK and Mrs. Kennedy on funeral readings
- 1964-01-03 `cal.1964-01-03.vietnam`: Operations Against North Vietnam report
- 1964-01-21 `cal.1964-01-21.vietnam-2`: Lodge: junta cool on covert attacks
- 1964-02-29 `cal.1964-02-29.transition-and-staff`: W. Bundy to succeed Hilsman
- 1964-03-04 `cal.1964-03-04.vietnam-4`: Johnson to Bundy: Chiefs say get in or out
- 1964-06-01 `cal.1964-06-01.vietnam-2`: Bundy to Johnson: 140 killed
- 1964-07-24 `cal.1964-07-24.vietnam-2`: Bundy to Johnson on 34-A airdrops
- 1964-07-31 `cal.1964-07-31.vietnam`: W. Bundy to M. Bundy, July 31
- 1964-08-03 `cal.1964-08-03.vietnam-5`: Forrestal to Bundy: destroyer seen as part of 34-A
- 1964-08-10 `cal.1964-08-10.vietnam-3`: Clifford calls Johnson; Cline doubts second attack
- 1964-09-15 `cal.1964-09-15.china`: Bundy, Rusk, McNamara, McCone on Chinese bomb
- 1964-10-01 `cal.1964-10-01.vietnam-2`: SNIE on South Vietnam
- 1964-10-19 `cal.1964-10-19.vietnam-2`: W. Bundy, The Choices We Face
- 1964-10-23 `cal.1964-10-23.vietnam`: Thomson to Bundy: muddle through
- 1964-11-23 `cal.1964-11-23.vietnam-2`: W. Bundy mild-view memo: it won't wash
- 1964-12 `cal.1964-12.press-and-broadcasting`: Bundy asks to go on Meet the Press: Not now
- 1964-12 `cal.1964-12.press-and-broadcasting-2`: Bundy to Johnson on Bradlee and Newsweek
- 1964-12 `cal.1964-12.press-and-broadcasting-3`: Kraft in Harpers: A Way Out in Viet-Nam
- 1965-01 `cal.1965-01.transition-and-staff-nsc`: Bundy names Moyers, Hughes, Chayes as successors
- 1965-01-06 `cal.1965-01-06.vietnam-3`: W. Bundy to Rusk: likely to come apart
- 1965-02-17 `cal.1965-02-17.press-and-broadcasting`: Lippmann column: supreme folly
- 1965-03-08 `cal.1965-03-08.press-and-broadcasting`: I. F. Stone, Reply to the White Paper
- 1965-03-10 `cal.1965-03-10.vietnam-3`: Camp David: Johnson, Bundy, Rusk, McNamara
- 1965-03-30 `cal.1965-03-30.vietnam-2`: Bundy to Johnson: SE Asia Development Corporation
- 1965-04-16 `cal.1965-04-16.students`: Bundy declines teach-in invitation
- 1965-04-20 `cal.1965-04-20.students`: Bundy to Donald Graham at the Crimson
- 1965-04-29 `cal.1965-04-29.latin-america-dominican-republic`: Goodwin to Johnson on intervention
- 1965-05-12 `cal.1965-05-12.vietnam-mayflower`: Ball to Hughes on Mayflower
- 1965-06-19 `cal.1965-06-19.vietnam-2`: W. Bundy letter to ambassadors
- 1965-06-27 `cal.1965-06-27.vietnam-july-decision`: Bundy to Johnson on Ball paper: cut our losses
- 1965-07-03 `cal.1965-07-03.press-and-broadcasting`: MacLeish and Bundy in Saturday Review
- 1965-11-13 `cal.1965-11-13.transition-and-staff`: Bundy breakfast with McCloys on Ford
- 1965-11-19 `cal.1965-11-19.transition-and-staff`: Bundy tells Johnson he will take Ford
- 1966-02 `cal.1966-02.transition-and-staff-nsc`: Moyers asks W. Bundy about the NSC post
- 1966-04-02 `cal.1966-04-02.vietnam-struggle-4`: Johnson: take a stand in Thailand
- 1966-05-23 `cal.1966-05-23.vietnam`: W. Bundy Detroit speech: encouraging
- 1967-03-09 `cal.1967-03-09.vietnam-order-of-battle`: Wheeler to Westmoreland on order of battle figures
- 1967-07 `cal.1967-07.civil-rights-organizations`: Ford grant to CORE Cleveland
- 1967-11-11 `cal.1967-11-11.vietnam-2`: Bundy to Johnson after the Wise Men
- 1967-11-27 `cal.1967-11-27.vietnam-2`: Hovey CIA cable predicting offensive
- 1968-03-21 `cal.1968-03-21.vietnam-205000`: Bundy to Johnson: draft speech discouraging
- 1968-04-01 `cal.1968-04-01.vietnam-4`: Galbraith calls on W. Bundy to resign
- 1968-06 `cal.1968-06.robert-kennedy-campaign`: Ford fellowships for RFK staff

## Witnesses (R35)

Second run, Nov. 4, 2026 (patch `inbox/2026-11-03-b3-bird-3.yaml`, 105 ops: 53 src (via rows), 33 to-check, 10 cites repeated from b3-bird-2 so the via rows have their item, 6 checks, 3 primary; patch-check 0 errors, 0 warnings). The notes (pp. 410-462, numbered by chapter) parsed from the text layer and each matched to its call in the text (the calls found by their numbers in sequence, chapter by chapter; 692 of 851 calls in chapters 7-16 placed; the rest between their neighbours), the passage read where a note was in doubt; checked on the image of p. 447 (notes 12.48-68). For each page the calendar cites (the tree's and b3-bird-2's entries), the notes of the passage: 57 new witnesses (`inbox/witnesses/2026-11-03-b3-bird-3.yaml`), 107 edges (`sources/witnesses/by-work/bird-color-of-truth.yaml`), ten witnesses already registered taking the edge (Forrestal's memorandum of May 11, 1962; the White House statement of Oct. 2, 1963; Bundy to Johnson, Jan. 7 and June 1, 1964, and Jan. 27, 1965; Forrestal to McNaughton, May 1, 1964; the Memorandum for the Record of Sept. 15, 1964 (FRUS XXX, doc. 49); the Kraft interviews of Forrestal; the *Post* of May 15, 1965; the *Times* of Aug. 3, 1966; William Bundy's Vietnam manuscript). A document Bird's text or footnote names without a note (the Riesman-Fromm letter, Raskin's memorandum of July 6, 1961, Bundy's July 24, 1964 report, the April 16, 1965 letter, Bundy's Camp David notes) registered as the text gives it (R38), `open: not found`. Works in the catalogue cited by a note (Kahin, Gardner, Gibbons, Prados, Adams, Taking Charge, Goodwin, Steel, Berman, DiLeo, Moise, Cooper, Manchester, Schlesinger, Clifford, *Robert Kennedy in His Own Words*, the *Bulletin*) are edges to their cards and join the entry's "To check:" with Bird's note; the unread documents join it the same way. FRUS read and cited first: 1964-68, I, docs. 266 (Forrestal, Aug. 3, 1964) and 368 (SNIE 53-2-64), XXX, doc. 49. Edges only, no via (the note does not bear on the entry's units): 259 n.28 (the White House statement, for the CINCPAC message; Check written), 297 n.74a-b, 294 n.65b, 287 n.47c, 275 n.12b-c and 13b, 271 n.2c, 318 n.35, 321 n.46 for all but A, 332 n.74, 344 n.105 and 107b-d, 345 n.109, 348 n.120a, 381 n.20b, 313 n.27b-c. No note found for the passage (no witness): 218 (*The Liberal Papers*), 265 (William Bundy's confirmation), 293 (Biên Hòa; the call after the paragraph is the manuscript's), 296 (note 70 is printed blank: Fulbright's warning of Dec. 4, 1964), 324 (Bosch, Bundy's mission), 334 (William Bundy to the ambassadors), 343 (McCloy's offer, the Sheraton-Carlton breakfast), 357 (the letter of May 1967), 364 (Bundy after the Wise Men), 383 (Ocean Hill), 387 (the fellowships), 347 (cal.1966-03-01.transition-and-staff is not in the tree: the notes 13.116-119 there are the *Post*'s and Lippmann's of Feb. 27-Mar. 2, 1966): a reader with the image may place them.

Dates the notes give that the entries do not (Checks written): William Bundy to Kennedy, Nov. 11, 1960 (182 n.97; cal.1960-11.program); the two memoranda on *Meet the Press* and *Newsweek*, both Dec. 2, 1964 (300 n.82); the successor memorandum, Feb. 2, 1965 (301 n.1, 348 n.120; cal.1965-01.transition-and-staff-nsc, dated January); Bundy to Lodge (258 n.24) against FRUS's telegram 533; Harriman to Kennedy printed "Sept. 1, 1991" (213 n.107).

## Passed over

Re-ruled Nov. 6, 2026, under R18 as amended (batch 6, read Nov. 10, 2026): the two rows ruled private (Harvey Bundy's death; the Fifth Avenue apartment) were read again and stand, below, "Batch 6".

Made from the 440 dated sentences, pp. 140-409; an event the calendar holds took its cite or none and is not here.

| page | date | event | why |
|---|---|---|---|
| 147 | 1960 | Harvard's admissions figures | out of the brief (no bearing on politics or policy) |
| 150-151 | 1960 | Bundy's drift from the Republicans; his vote on Strauss (1959) | not an event in the span (Strauss, 1959: before it) |
| 193 | autumn 1960 | Bundy to the *Harvard Crimson* on the Latin American liberals and Trujillo | lead: the day and the article |
| 210 | autumn 1961 | Bundy's part in drafting the "action memorandum" of flexible response | lead: the document and the day |
| 222-223 | spring 1962 | Galbraith's missive; Forrestal's memorandum of the talk with Kennedy and Harriman | not set against the calendar: lead |
| 243 | late Sept. 1962 | Bundy's note to Kaysen on Roosevelt and Cuba | lead: the day |
| 251-252 | 1962-63 | Forrestal's daily sessions with the President; Halberstam's dinner with Forrestal, end of 1963 | not dated to a month: lead |
| 260 | early 1963 | Mansfield: Kennedy told him of a withdrawal after the election | Mansfield's later account, not dated: lead |
| 265 | Oct. 7, 1963 | Harvey Bundy's death | private (a family matter) |
| 302-303 | late 1964 | Forrestal leaves the State Department; Unger in his place | lead: the day |
| 341 | autumn 1965 | the journals' coverage (a summary) | not an event |
| 351-354 | June 1965-Feb. 1966 | Indonesia: Bundy to Johnson (late June 1965); William Bundy with Colby, Sept. 29, 1965; the CIA's assessment, Jan. 3, 1966; Komer's figure, Feb. 10, 1966 | lead: set against the calendar's Indonesia thread, not done |
| 357-363 | 1966-67 | William Bundy's work on the war (summaries); Kissinger to Harriman (summer 1966); Raskin's "Call to Resist" (spring 1967) | summaries; the Call: lead |
| 376-393 | 1966-74 | the Ford Foundation: the Fifth Avenue apartment; Friendly's move; the Public Broadcasting Laboratory ($10 million, 1967); Bedford-Stuyvesant (1966); La Raza ($500,000, 1968); Wolfson College ($4.5 million, 1966); the Congress for Cultural Freedom (1967) | private (the apartment); the rest not dated to a month: leads |

## The press (R13)

None: Bird gives no day's coverage. Press entries made: Chalmers Roberts (Nov. 1962), Lippmann (autumn 1961; Feb. 17, 1965), Kraft in *Harper's* (Dec. 1964), I. F. Stone (Mar. 8, 1965), the *Saturday Review* (July 3, 1965).

## Leads

National
- The Public Broadcasting Laboratory's $10 million (1967), the Bedford-Stuyvesant Corporation's Ford grant (1966), the Southwest Council of La Raza's (1968): the days, from the Ford Foundation's annual reports or the *Times*.
- Forrestal's Kraft interviews (1964) and Joseph Kraft's papers; Bird's "Harriman/Bird Papers" (the Harriman papers held by Bird), where they went.
- I. F. Stone's "Reply to the White Paper": *I. F. Stone's Weekly*, Mar. 8, 1965 (the issue to confirm).
- Kraft and I. F. Stone have no name entries: propose Part III entries (R13). Foreign
- Indonesia, 1965-66 (Bird 351-354): the CIA's assessment of Jan. 3, 1966, and Komer's report to Johnson of Feb. 10, 1966 ("some 100,000 Communists have been killed"): to set against the Indonesia thread.

## Batch 6: the private rows re-ruled (Nov. 10, 2026)

No patch: nothing entered. The copy: the owner's PDF in Drive (10jrYYg-uRuQJSsACk9oQVTyBQGa5IlWF), downloaded again; the offsets as above (− 3 to p. 224, − 19 from p. 225); pp. 265 and 376–393 read again off the text layer; deleted when done.

| page | date | event | ruling |
|---|---|---|---|
| 265 | Oct. 7, 1963 | Harvey Bundy's death at Boston; the funeral while his sons are "intensely preoccupied with the question of Diem" | still passed over: a family matter, no bearing on public business |
| 376 | spring 1966 | the Bundys buy an apartment on Fifth Avenue | still passed over: personal, no bearing on public business |

Not borne out: none.
