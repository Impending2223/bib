# The owner's books: brief for each book agent (read brief-common.md first, then this)

The owner (Oct. 23, 2026) put copies of books into a shared folder and asked: "Can you check whether our soft
citations hold up, identify page numbers if they do, identify other entries to which they may be relevant, or gaps in
the calendar they might fill, and fill them in accordingly?"

The copies: the owner's shared Drive folder. Your prompt gives your book's Drive file id; fetch it yourself:
`curl -sSL -o drive/<short>.pdf "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`
(in /tmp/claude-0/-home-user-bib/f04c9307-7a44-53db-a3d0-26f3e1375c84/scratchpad/drive/), check it is a PDF (`file`),
then `pdftotext -layout` it to <short>.txt beside it (a form feed between PDF pages). A scan without a text layer: OCR
it with `ocrmypdf` or `pdftoppm` + `tesseract` page by page (say so in the report). Delete the PDF when you finish
(keep the .txt; the disk is shared and small). Most are copyrighted: the owner's
copies, for this research. Never put the PDF or its text in the repo, never paste more than a short quotation into an
entry (a quotation only where an entry needs the words, marked and cited by page), never paraphrase at length. Cite by
the PRINTED page: find the offset between PDF pages and printed folios first (running heads and folios; it can change
at the front matter, the plates, a second volume), and check a few pinpoints against the page image
(`pdftoppm -f N -l N -r 100 -png`) before trusting the text.

Two rules of the owner's, Oct. 23, 2026 (CLAUDE.md, "What each source stands for", "Hard and soft", "The informal
record"; read them):
- A source stands for the whole entry unless the note says which claim it is for. When the book bears out only part
  of an entry (the meeting but not its date, the vote but not the count), cite it for that part: a parenthetical
  after the pinpoint, "[[w.id]], 123 (the meeting)". The unread works now stand behind "To check: ...", a sentence of
  their own before "See" and "Names:". When you read your book for an entry, MOVE its card out of the To check
  sentence into the read sources (after the primary record, in the run of pincited works), with its pinpoint; if the
  To check sentence is left empty, drop it. A source the book names that you could not read (a file, a hearing, an
  interview) may join the To check.
- The calendar now wants the informal record too: meetings, lobbying, agreements, the planning of policy, personnel,
  operations and communications in the West Wing, the members' offices, the campaign headquarters, for the persons
  with public roles. For a biography or memoir this is the main yield of step 3: the dated transactions the book gives
  (a meeting, a call, a bargain, a strategy session, an appointment settled), each an entry where the book dates it to
  the day (or month: `date: '1964-03'`), cited by page, naming whose account it is where it is one participant's ("by
  Johnson's account"; "O'Donnell recalls"). A memoir is its author's account: say so in `c` where it matters ("Johnson
  writes that ..."), never as plain fact against another record. Where the daybook's FRUS, the Public Papers, a
  recording (daybook/recordings/, the Miller Center's free pages) or the Daily Diary days in daybook/diary.yaml give the
  same transaction, that is the primary record: cite it first.

Your book's card is named in your prompt. Do, in this order:

1. Hold up every citation already there. `./bib works show <card>` lists every list entry and calendar entry that
   cites it. For each calendar entry: does the book say what the entry says, on the event the entry cites it for?
   - It holds: add the pinpoint after the card, `[[w.id]], 123–25` (Bluebook: the pages, "123–25"; several, "45, 211").
   - It holds in part, or the book gives another date, figure, name or account: don't silently rewrite the entry. If
     another record settles it (FRUS in the daybook, the Public Papers, the Statutes, the Record), propose the fix in
     the patch and say what the entry said. Otherwise add "Check: <Surname> gives ..." to the note.
   - The book does not treat the matter at all: say so (the card may belong to another entry, or it was cited for the
     thread, not the event); move or drop the citation only where the book plainly does not bear on it.
   Every case that is not a plain "holds" goes in notes/book-checks/<card>.md: entry id, what the entry says, what the
   book says (page), any third record, and your ruling. That file is for the owner to read.
2. Other entries the book bears on: work through the book's chapters (its index helps: names, events), find the
   calendar's entries on what it treats (`./bib find`, `./bib find -l cal --thread <slug>`), and add the card with
   its pinpoint to the bibliography of the EVENT's first entry (later entries of the event keep their `See [[id]]`; the
   build orders a run of works, so put it at the end of the run). Not in every entry of a long thread; where the book
   adds something of substance for that event.
3. Gaps: events the book dates and documents that the calendar lacks, and that meet the brief ("events that left a
   trace, or should have left a trace, on the political and policy histories of the Kennedy and Johnson
   Administrations, their Congresses, or those of their members"; Jan. 6, 1960–Jan. 20, 1969). New entries in the
   house style (CLAUDE.md: c, n with the primary record first where you can find one, the event's bibliography, Names,
   name: tags, state:/city:/place: tags; one event a day; `./bib new-id`). Look for the primary record the book cites
   (FRUS: `grep` the daybook, `daybook/<YYYY-MM>.yaml`; the Public Papers: `sources/ppp-matches.json` and the daybook's
   President rows; a statute; the Record); where none is reachable, the book is the bibliography and the detail it
   alone gives carries "Check". What you cannot place goes to notes/leads.md under its heading.
4. All calendar changes by one inbox patch, `inbox/2026-10-24-book-<short>.yaml` (patch name book-<short>; edit ops
   with `base:` from `./bib show`; add ops for new entries), never direct edits to lists/cal/*.yaml. Run
   `./bib merge <patch> --dry-run` before you finish. Cards: the book's own card exists; add other cards only per
   brief-common's add_cards.py.
5. Report (under 500 words): counts (citations checked: held, held with pages, disagreed, not treated; entries newly
   citing the book; new entries), the disagreements in one line each, and your leads.
Other agents read other books at the same time and edit other entries; your patch carries `base:` so the merge is
three-way. Don't edit notes/book-checks/ files but your own.

## Two more rules (the owner, Oct. 28, 2026; CLAUDE.md, "What the works rest on")

A. **Claims, sources, and what the work rests on** (CLAUDE.md, "Claims and their sources", "What the works rest on";
   tools/bib/claims.py and tools/bib/cited_records.py, read their docstrings first). Every entry's `c` is lettered into
   units (`./bib claims show ID` prints them). For each entry you cite or edit, write its claim map by patch: an edit
   op setting `src` (start from `./bib claims seed ID`; `c:` the hash it prints, made again if your patch changes `c`):
   one row per source at one page for the units it grounds: `'w.card PAGE: A, C-D'`, `'<the link's address>: all'`,
   and for each record the work's note gives for that passage, `'via w.card PAGE n.NOTE: B'`, the record described
   once in `sources/cited-records/<card without w.>.yaml` (keyed by page and note; kind, date, where, found, read).
   The precision the owner asks for is the letters: which fact, claim or quotation each source and each record
   grounds. A note citing several records for a passage: each record its row, the same letters; nothing more to say.
   Only what the note gives: never infer a record from the text. A record the series already holds (the daybook's
   FRUS, sources/ppp-matches.json, daybook/recordings/millercenter.yaml, daybook/diary.yaml): set `found`, read it, and
   if it bears out its units, cite it in the note as the primary record, linked, first, with its own row (`read: true`).
   Otherwise it joins the note's "To check:" after the works: "To check: Bundy to Johnson, Feb. 7, 1965, NSF, LBJ
   Library (cited by [[w.dallek-flawed-giant]], 251 n.14)." A work with no notes: say so in the book-check file.
   `./bib claims show ID` after your patch is merged in a scratch copy shows the footnotes your map makes: read them.
B. **What you pass over.** Your notes/book-checks/<card>.md gets a section "## Passed over": every dated event the work
   treats within the brief's span that you did not enter, a row each: page | date | event, a few words | why (out of
   the brief; undated; minor; already in as <id>; to leads). The owner rules on them. Not the background of chapters
   before 1960; everything the work dates in 1960–Jan. 20, 1969 that touches the brief's persons and institutions.
Report the counts: entries mapped (and how many finer than the whole entry), records logged (found and read, found and not read, not found), events passed over by reason.

## The parties and the members (the owner's rule, Oct. 29, 2026; CLAUDE.md, "The parties and the members")

Within the brief, and never "minor": the position-taking, messaging, organization, communication, policy formation and
campaigning of either party out of the White House and of any member of Congress, leader or not (a party's statements,
papers, declarations, platforms; its committees' and leaderships' meetings and decisions; its factions and allied groups:
Ripon, the Free Society Association, YAF, the ACU, the DSG; the dated public word of a member, a governor, a party officer
or a party figure out of office on policy or politics). Enter them (threads: Republican Party, its subthread In Congress,
Democratic Party, Conservative movement; notes/threads.md). A journalist's column is an entry only where it carried an
act (a leak, a trial balloon) or made news itself. "Minor" means only: a repetition of a position already entered, with
nothing new; private or social trivia; a unit's routine the work does not treat as an event (a patrol without contact, a supply run).
