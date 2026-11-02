# One book, a first reading (brief for each single-book agent; read CLAUDE.md, brief-common.md, brief-books.md first)

Your book, its card, its Drive file id and what to read it for are in your prompt. The copy is in the owner's shared
folder: download it by the curl line in brief-books.md into your own new directory under the scratchpad, never into
the repo; read its text layer with pdftotext (an image-only scan: say so in the report and stop); establish the page
offset on three pages. Don't change any Drive file's sharing; keep no copy of the book in the repo.

1. The cites already in the calendar (`./bib works show <card>`): pin each to the page that bears it out and move it out
   of "To check:" (CLAUDE.md, "Hard and soft"), with a parenthetical where the page bears out only part; where the book
   does not bear the entry out, the cite goes and the claim takes a Check.
2. The whole book against the calendar over its span: each dated event within the brief that the calendar lacks is an
   entry; an event it holds takes the page (an edit). The informal record (meetings, calls, bargains, memoranda) and the
   parties and the members (never "minor": CLAUDE.md, "The parties and the members") as brief-books.md says.
3. Rule A (records the notes give: sources/cited-records/<card>.yaml; read and cite first what FRUS, the Public Papers,
   the Record, the daybook's recordings or the Daily Diary print) and rule B (Passed over, in notes/book-checks/<card>.md,
   with how the list was made). Leads at the end of the book-check file.
4. A book with no card: make the card first (works/, the form CLAUDE.md gives: author, title, year, and edition where the
   copy is not the first), checked by `./bib check`; another agent may be adding cards at the same time, so re-read the
   letter's file just before writing to it.

Deliverable: one patch, inbox/2026-10-29-book-<short>.yaml (edits with `base` read just before writing; `./bib merge
--dry-run` clean; never merge it yourself); the book-check and records files. Don't commit or push. Twelve other agents
are editing the calendar at the same time: read bases at the last moment. Before adding an entry, compare it with every
entry on its day in any thread (`./bib find -l cal --since D --until D`); if one already records the event, edit that one
(one event, one entry, `also:` for other threads). File each new entry under the thread its matter belongs to, even
where that thread already has an entry that day: never change an id or thread to get around the merge's duplicate flag.
No gendered pronouns for authors in notes ("the note", the surname). Report in under 400 words: copy and offset; cites
pinned or cut; new entries (count, and the chief ones); records (found and read, not found); Passed over by reason; leads.
