# Stage 5: the books read before the rules of Oct. 28 (brief for each agent; read brief-common.md and brief-books.md first)

Why: these books were read against the calendar on Oct. 23-28, before the owner's requests of Oct. 28 (CLAUDE.md,
"Claims and their sources" and "What the works rest on"): the claim maps, the records each work's notes cite, and the
"Passed over" list. Their citations stand (each was read off the page); what they lack is the rest. Your books and
their copies (the owner's, in Drive, by file id: download with the Google Drive tool into the scratchpad, never into
the repo) are named in your prompt. Each book-check file (notes/book-checks/<card>.md) gives the copy read and the
page offset: use them.

Do, for each book, in this order:

1. Every calendar entry that cites the book with a pinpoint (`./bib works show <card>`):
   - Reread the page against the entry's units (`./bib claims show ID`). Where the note's parenthetical says which part
     the page bears out, turn it into letters; where it has none and the page bears out only part, add the
     parenthetical and the letters. Write the entry's map (`src`, from `./bib claims seed ID`), keeping the rows other
     runs wrote (a stored map is theirs: add yours, never drop theirs). A page that does not bear the entry out: fix
     the pinpoint, or the cite goes and the claim takes "Check:" (CLAUDE.md, "What each source stands for").
   - Rule A of brief-books.md: each record the page's note gives for the entry, described once in
     sources/cited-records/<card>.yaml (schema: tools/bib/cited_records.py), tied by `via` rows with the letters it
     grounds; where FRUS, the Public Papers, the daybook's recordings or the Daily Diary print the record, read it and
     cite it first in the note (`found`, `read: true`); an unread one joins "To check:" with the work, page and note.
2. Rule B of brief-books.md, "Passed over": every dated event the book treats and the calendar does not hold, listed
   in the book-check file under "Passed over" (page, date, event, why: out of the brief, undated, minor, already in
   under another id, a lead). Find them by the book's dates (a script over the text layer may list every dated mention;
   then judge each against `./bib find -l cal --since ... --until ...`); say in the file how the list was made and what
   class of mention, if any, was passed over without a row of its own.
   The informal record (CLAUDE.md, "The informal record"; brief-books.md): a dated meeting, call, bargain, strategy
   session or appointment the book gives for a person with a public role is an entry, not a row of Passed over, where
   the book dates it to the day or month: enter it (an `add` in your patch), cited by page, saying whose account it
   is where it is one participant's, its primary record first where the daybook has it.
3. Leads: what the book names that the series cannot reach, under their headings, at the end of the book-check file.

One patch for your books, inbox/2026-10-29-backfill-<your part>.yaml (edits with `base` read just before writing;
`./bib merge --dry-run` clean; never merge it yourself). Other runs may edit the same entries before yours merges:
read each base at the last moment. Don't commit or push. Report (under 400 words) per book: entries reread and their
rulings; maps written; records logged (found and read, not found); new entries; Passed over, by reason; leads.

## The parties and the members (the owner's rule, Oct. 29, 2026; CLAUDE.md, "The parties and the members")

Within the brief, and never "minor": the position-taking, messaging, organization, communication, policy formation and
campaigning of either party out of the White House and of any member of Congress, leader or not (a party's statements,
papers, declarations, platforms; its committees' and leaderships' meetings and decisions; its factions and allied groups:
Ripon, the Free Society Association, YAF, the ACU, the DSG; the dated public word of a member, a governor, a party officer
or a party figure out of office on policy or politics). Enter them (threads: Republican Party, its subthread In Congress,
Democratic Party, Conservative movement; notes/threads.md). A journalist's column is an entry only where it carried an
act (a leak, a trial balloon) or made news itself. "Minor" means only: a repetition of a position already entered, with
nothing new; private or social trivia; a unit's routine the work does not treat as an event (a patrol without contact, a supply run).
