# The reader's brief against the texts it replaces

Reviewed Oct. 30, 2026. Old texts: CLAUDE.md lines 8–186 (the brief section as it stands on disk; "CL") and the seven
files in `notes/briefs/superseded/` (common, books, onebook, backfill, batch3, histories, primary). New: `notes/briefs/reader.md`.
Line numbers are the old files'. Formatting conventions left to CLAUDE.md are flagged only where the pointer is missing
or wrong.

## Dropped

In the old, not in the new.

| # | Old text (file:line) | Should join |
|---|---|---|
| D1 | "where the record is found and the event's bibliography lacks it, add it there too" (CL 67–68; the owner's Oct. 2 request, OB "Primary records": "add the primary record where you've found it, but it's not in the relevant bibliographic entry") | R25 |
| D2 | "An event is not a thread: the Bay of Pigs and Mongoose are two events in the Cuba thread" (CL 69–70); "cited for the thread, not the event" (books 46–47) | R26 |
| D3 | An existing event gets the card "to the bibliography of the EVENT's first entry ... put it at the end of the run. Not in every entry of a long thread; where the book adds something of substance" (books 50–54) | R2 step 2, R26 |
| D4 | "A justice is named only where the entry quotes his opinion or is about him, not for writing or joining one" (CL 92–93) | R20 |
| D5 | "a name in its own order as it stands ('Ngô Đình Diệm', 'Satō', 'Haile Selassie')" (CL 89–90) | R20 |
| D6 | No tag for "a name in a case's title" (CL 98) | R19 |
| D7 | "File each new entry under the thread its matter belongs to, even where that thread already has an entry that day: never change an id or thread to get around the merge's duplicate flag" (onebook 25–26) | R16 |
| D8 | "Don't change any Drive file's sharing" (onebook 6) | R49 |
| D9 | The offset "can change at the front matter, the plates, a second volume"; "check a few pinpoints against the page image (`pdftoppm ...`) before trusting the text" (books 15–17) | R49 |
| D10 | Pinpoint form: "123–25"; several, "45, 211" (books 42) | R27 |
| D11 | A pointer in words: the work goes behind "To check:", "the words its parenthetical"; "a chapter's title" is words (CL 113). R27 lists "a chapter" as a valid pinpoint without saying a title is not | R27 |
| D12 | Units split "never inside a quotation, parentheses or brackets" (CL 120) | R31 |
| D13 | `src`'s `c:` hash, "made again if your patch changes `c`" (books 77; CL 124). R31 says only "re-letter" | R31 |
| D14 | "Every row names an item the note (or `c`) prints; the note stays the visible record, and `check` holds the two together [claims]" (CL 125–126) | R31 |
| D15 | Read the footnotes `./bib claims show ID` gives after a scratch merge (books 88) | R31 |
| D16 | Book-check row for each cite that does not plainly hold: "entry id, what the entry says, what the book says (page), any third record, and your ruling" (books 48–49). R30 says only "gets a row" | R30 |
| D17 | A wrong page: "fix the pinpoint" (backfill 16–17); "the right page" (histories 10–11). R30 has no case for a page a page or two off | R30 |
| D18 | Not treated: "the card may belong to another entry ... move or drop the citation only where the book plainly does not bear on it" (books 46–47); "the cite goes and the claim takes a Check" (onebook 10) | R30 |
| D19 | The pinpoint is the page that bears out each claim, not "the page about the event"; read "sentence by sentence against the entry's units" (histories 3–5, 10) | R27 / R30 |
| D20 | On settling against a third record: "propose the fix ... and say what the entry said" (books 44–45); "the book's version said plainly" (histories 13) | R22 / R30 |
| D21 | "where none is reachable, the book is the bibliography and the detail it alone gives carries 'Check'" (books 61–62) | R25 |
| D22 | "Many events have no record of their own (a march, a strike, a riot ...): those you leave, and say so" (primary 7–8) | R25 |
| D23 | Records omitted from R25's list: the AG's and OLC's opinions (`daybook/opinions.yaml`), the *Bulletin*, hearings and the Daily Digest rows, lower-court cases on case.law (primary 16–23) | R25 |
| D24 | Not readable here: the newspapers ("TimesMachine is a link by date, not a text"), history.defense.gov, jcs.mil, HathiTrust's pages (primary 28–30) | R51 |
| D25 | "Finish with `./bib check` (0 errors from your work; report others' errors without fixing them) and ... `./bib audit-cal`" (common 25–27). R47 asks only for a clean `merge --dry-run`, though readers write cards, book-check and records files that `check` reads | R47 |
| D26 | "Don't edit notes/book-checks/ files but your own" (books 70); shared files (`notes/leads.md` among them) "by small exact edits only, re-reading first" (common 11–16, 45–46) | R48 |
| D27 | How to find pending adds: `grep -l "date: 'D'" inbox/*.yaml` (batch3 21); within a group "the second book's patch builds on the first's" (batch3 17–19) | R16 / R45 |
| D28 | A new card gives the edition "where the copy is not the first" (onebook 17–18) | R48 |
| D29 | Check the download is a PDF (`file`) (books 9); after OCR "delete the images" (batch3 11) | R49 |
| D30 | Military: the threads ("Vietnam and its subthreads, Air war, Laos, Defense, the event's own"); figures kept "whether or not the war table carries the series"; logistics' examples ("a port, an airlift, the munitions, the construction program"); the theaters named (CL 58) | R13, R23 |
| D31 | Organized interests "and their leaders"; the forms of their word: "a statement, testimony, a resolution, an endorsement, a convention, a campaign" (CL 58) | R10 |
| D32 | Which Part III sections make a columnist "named": "K–J Cong. III.J, Opp. III.J, 1968 III.O, Cong. III.M", with the names; the proposal is "for the owner to rule" (CL 58) | R12 |
| D33 | "every thread is its matter as Washington and its counterparts met it" (CL 58; 149) | R4 / R9 |
| D34 | The threads' slugs and `notes/threads.md` (CL 58–59); State and city threads in `notes/threads.md` (CL 145–146) | R8, R19 |
| D35 | The prose's bad examples ("for Moscow's benefit," "a good midterm," ...) and the Before/after Gilpatric example (CL 13–15, 173–185) | R18 |
| D36 | "at least a month-by-month granularity"; a statement "for each thread"; subthreads, ghosts, no thread name beginning "The" (CL 23–24, 148–153; common 5–6). The brief points to no CLAUDE.md section for threads | R19 pointer |
| D37 | YAML quoting (common 6). No pointer to CLAUDE.md "Markup inside text" | R19 pointer |
| D38 | Card notes ("Bibliography notes": no reviews, no awards, no side labels; a thesis stated the same way whichever side, CL 159–171). Readers make cards; no pointer | R48 |
| D39 | The To check works are "the event's bibliography among them" (CL 111); the form "To check: [[w.a]]; [[w.b]]."; an emptied To check sentence is dropped (books 26) | R28 |
| D40 | Made public: "documented in records nobody saw at the time (a recording, a memorandum, an FBI file)", form "Made public: Drew Pearson's column, May 24, 1968." (CL 81–83) | R24 / R9 |
| D41 | Report items: "what you checked and how" (common 28); "the disagreements in one line each" (books 68) | R53 |

**Rule A without a counterpart in Part E** (books 74–88; backfill 18–21; CL 130–137):

| # | Old | Part E |
|---|---|---|
| E1 | `via` rows in the entry's map, `'via w.card PAGE n.NOTE: B'`, tying each record to the units it grounds | None. R33 draws "the tree for each unit" but says nothing of how a witness reaches the entry's `src` |
| E2 | "A note citing several records for a passage: each record its row, the same letters" | None |
| E3 | `found` and `read` (`read: true` for a record read and cited first) | None. R35 keeps the act (read and cite first) without the fields; R53 counts witnesses, not found/read |
| E4 | "A work with no notes: say so in the book-check file" | None |
| E5 | "Only what the note gives: never infer a record from the text" | None. R34 ("every witness you meet") does not say whether a source the text names but the notes do not counts |
| E6 | The file and its check: `sources/cited-records/<card>.yaml`, schema `tools/bib/cited_records.py`, [cited-records] | Replaced by `sources/witnesses/`, no schema named |
| E7 | Kept: the unread record behind "To check:" with the work, page and note (R35); the record the series holds read and cited first (R35); edges, roots, variants, the record that is the act (R33–R38) are new | — |

## Changed

| # | Old | New |
|---|---|---|
| C1 | The work's notice is the test for the columnists and for military matters (CL 58: "the work's notice the test, as for the columnists") | R4 makes it the test for every event: "what the work dates and treats as an event is an entry". Broader |
| C2 | "the position-taking, messaging, organization, communication, policy formation and campaigning ... of any member of Congress, leader or not"; public word "a speech, statement, press conference, interview, article or column under his own name" (CL 45–50) | R8 gives the members only their "dated public word" and drops "column" and "leader or not". Narrower |
| C3 | Tag the President where the entry is "his message, address, press conference, signature, order, proclamation, NSAM, meeting, or a poll of his approval" (CL 95–96) | R19 "where the entry is his act": a poll of his approval is not his act. Narrower |
| C4 | Papers passed over: "a covering note or transmittal, a draft not sent, a meeting's preparation, a repetition and private remarks" (CL 57–58; batch3 35) | R17 drops "a repetition" from the papers. Only "a repetition of a position" survives under minor. Narrower |
| C5 | A source stands for "the whole of `c`, its dates, numbers, names, quotations and facts"; Z stands for C and its tie, "not for A, B and D" (CL 102, 105–106) | R29 drops the enumeration and the "not for A, B and D". Looser |
| C6 | Not treated: move the cite to another entry or drop it "only where the book plainly does not bear on it"; the claim takes a Check (books 46–47; onebook 10) | R30 "the cite goes", flat |
| C7 | An existing event takes the card in its first entry, and only where the book adds substance (books 50–54) | R2 step 2 "Give each event the calendar holds its pinpoint". Broader, and it does not say which entry |
| C8 | Counterparts' decisions etc. "dated by their record, with 'Made public:' where the record was private" (CL 58) | R9 ties dating by the record and Made public only to "what Washington did not see" |
| C9 | A memoir's account named "in `c` where it matters ('Johnson writes that ...')" (books 33–34) | R21 "say so where it matters": the field is not named |
| C10 | Passed over: say "what class of mention, if any, was passed over without a row of its own" (backfill 25–26) | R44 forbids blanket rows. Follows the Oct. 30 ruling (CL 58); a deliberate change |
| C11 | An image-only scan: "say so in the report and stop" (onebook 5) | R49: OCR it. Follows batch3 1 ("overrides"); a deliberate change |
| C12 | Standing rules the owner gives "go into CLAUDE.md, dated" (common 32–33) | The brief's preamble: amend the rule here and add a row to the table. CLAUDE.md does not yet say so |
| C13 | `n`'s order fixed only "To check:" ahead of "See" and "Names:" (CL 110–111) | R24 also sets "Made public:" ahead of "To check:". A new specification, harmless |
| C14 | A link's mechanical map covers all units, which is right only where the record bears out the whole entry (primary 40–43) | R31 asks for a map on every entry cited or edited (as books A did), without this warning |
| C15 | Witnesses memo (not an old text, but R34's source): register new material "unless the new material is, in all its contents, strictly inferior"; "credit the matter that has a strictly superior claim to being upstream" | R34 "however well attested", with no exception and no crediting rule |

## Provenance

| # | Row | Finding |
|---|---|---|
| P1 | R9–R12 | Quotes the owner: "Give me the lobbies and foundations too. And Hoffa!" and "the 'name' columnists". Neither phrase is in `notes/owner-brief.md`, CLAUDE.md or any old brief. CL 58 paraphrases the ruling ("which passed over the lobbies, the foundations and Hoffa") and writes "the named columnists". Unsourced quotation |
| P2 | R4 | Gives "the work's notice is the filter" as the owner's words. CL 58 has it unquoted, the series' own wording in its account of the ruling |
| P3 | R21 | Quotes "name whose account it is" and "where accounts differ, say so" as the owner's. These are CL 38–39's own wording; in that ruling the only quoted words are "the sinews of the public history", and OB's "Scope" message holds neither phrase. R21's memoir rule comes from batch3 4, an agent brief: house rule |
| P4 | R22 | Cites the Oct. 5 "Check" message, which asks only that "Check" be written for later verification. R22's substance (change `c` only where a record settles it beyond doubt, and say so; never rewrite beyond need) is primary 37–39 and histories 14: house rule |
| P5 | R23 | "the owner, Oct. 29–30: UTC; a flag for an approximate time". No old text gives UTC or `time_approx` to the owner. Batch3 5b states them unattributed; the owner's words there cover only the raw material |
| P6 | R3 | "Never write from memory" is common 21–22 (house). The Oct. 18 Leads ruling covers only the leads half |
| P7 | R16 | The comparison with the day's entries and with the pending patches is onebook 23–25 and batch3 2 (house). The row cites only owner rulings |
| P8 | R30 | The owner's own request for holding up cites is books 3–5 (Oct. 23: "Can you check whether our soft citations hold up, identify page numbers if they do ..."). The row cites the precision message instead |
| P9 | R32–R37, R39 | Leaves out CL 130–131's Oct. 28 words ("the materials and records cited for the claims in the secondary sources they read"; "identify the ABCD fact, claim, or quotation it sources") |
| P10 | R20 | "Names, events" is the Oct. 1 calendar instruction (CL 31), not the Oct. 14 ruling it is dated with |
| P11 | missing | No row for R2 (books 3–5; batch3 1), R5, R45 (batch3 2, house) or R53 (house). R19's tag rules have no row; the row covers only places and results |

## Contradictions

| # | Finding |
|---|---|
| X1 | Part E is "not in force" until the witnesses registry is built (Nov. 2), yet R2 step 3 and R53 require it. Its only text for the rule in force now (CL 130–137: records the notes give; the unread record behind To check; the held record read and cited first) is R35, inside Part E. Approved before Nov. 2, the brief leaves the records the notes cite with no rule in force |
| X2 | R46 sends leads to `notes/leads.md` directly. The old texts put them at the end of the book-check or notes file (onebook 16; backfill 31; primary 45–46), and CLAUDE.md says "they go into the file when their work is merged". R46 also has many agents writing one shared file, against common 11–16 |
| X3 | R44 keeps "already in as <id>" as a reason to pass over. Yet R2 step 2 (and onebook 12: "an event it holds takes the page (an edit)") make such an event an edit, and R39 says already-in is never a reason to pass a witness over. The witnesses memo §0 names this reason as a fault |
| X4 | R19's pointer names "Places", "Vietnamese names", "Election results" as CLAUDE.md sections. They are paragraphs under "House style" ("Places in the calendar's entries", "Vietnamese names and places", "Election results in `c`"). There are no pointers for YAML quoting, threads and subthreads, or the Names line's own-order and justice rules |
| X5 | R23 says the time fields start Nov. 2 (as batch3 does). CL 142 presents `time:`, `time_approx:`, `follows:` as current and points to "The calendar by day", which does not document them. The inconsistency is in CLAUDE.md |
| X6 | The preamble calls the batch briefs the rules in force until approval, but they are filed as `superseded/` |

## Assignment matter, correctly left out

The Drive download commands (curl, the Google Drive tool), the scratchpad paths of `add_cards.py` and its lock, the
patch names and dates (`2026-10-24-book-*`, `2026-10-29-b3-*`, `-backfill-`, `-histories-`, `-primary-`), the
`notes/primary-records/` deliverable and its direct edits to `sources/cited-records/`, the counts of agents at work
and what each is doing, the "fifteen" and "seventy" books, the files other agents hold (build.py, check.py and the
rest), the spot-check's figures, the histories' list of Chiefs' matters, the memoir and journalist lists, the YYYYMM
renaming notice, the builder's duties (document what you build, `problems(series)` hooks), and the owner's working
hours (left to CLAUDE.md "Working hours").

## Disposition (the second draft, Oct. 30, 2026)

- Dropped: D1–D41 folded into the rules named, but D35's before-and-after example, left in CLAUDE.md and pointed to
  (R19), and D36's thread conventions, pointed to (R2). The rules are renumbered (R1–R58; R45–R47 kept free).
- Rule A: E1–E6 are R35, in force now; Part E's witness rules (R36–R43) are marked not in force until the registry is
  built. Studies, memoirs and collections the notes cite are logged under R35 meanwhile.
- Changed: C1 kept and flagged for the owner (R5's row); C2–C9, C13 (kept), C14 restored; C10 and C11 deliberate (the
  Oct. 30 ruling; batch 3); C12 stated in the preamble; C15 in R38 (the copy as an edge, the upstream credited).
- Provenance: P1, and the words behind P5, are the owner's, from the session's transcript (Oct. 29 and 30); they are
  now copied verbatim into `notes/owner-brief.md`, "The rulings of Oct. 28–30, 2026", with the other rulings of those
  days, and the table cites them there. P2–P4, P6–P11 corrected: house rules marked as such, rows added.
- Contradictions: X1 (R35 in force now), X2 (R50: leads in the book-check file, copied by the merger), X3 ("already
  in" is no reason to pass over: R44), X4 (the pointers name CLAUDE.md's headings), X5 (CLAUDE.md now says the time
  fields come Nov. 2), X6 (the preamble says "superseded on approval").
