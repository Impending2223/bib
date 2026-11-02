# Stage 3: the official histories, reread (brief for each histories agent; read brief-common.md and brief-books.md first)

Why (the spot-check, notes/spot-check-2026-10-28.md): the run of Oct. 23 cited each history's page "for each entry these
histories treat": the page about the event, not the page that bears out each claim. Of 70 sampled pinpoints, 22 bear
out only part of the entry with no word of which part, 8 disagree with the entry unlogged, 3 are a page or two off and
3 are not on the page at all. It added no entries. Your volumes are named in your prompt.

Do, in this order:
1. Every pinpoint to your volumes in the calendar (`./bib works show <card>` lists them; ~500 across the four runs).
   Read the page, sentence by sentence against the entry's units (`./bib claims show ID`). Then: the right page; the
   units it grounds, as the entry's claim map (`src`, by patch; start from `./bib claims seed ID`) and, where it grounds
   only some, a parenthetical in the note; a disagreement as "Check: <Surname> gives ..." (or settled against a third
   record, as stage 2 did: the record cited, the book's version said plainly) and a row in your book-check file; a
   page that does not bear the entry out comes out of the note. Never rewrite an entry beyond what the page needs.
2. The histories' notes (rule A of brief-books.md): each record a page's note gives for a claim, described in
   sources/cited-records/<card>.yaml, tied by `via` rows. These volumes cite the JCS and OSD files, the CINCPAC and
   MACV messages, FRUS: where FRUS prints the document (grep the daybook), read it and cite it first.
3. What the calendar lacks (brief-books.md step 3 and the informal record): the dated decisions, memoranda, meetings
   and messages the volumes give within the brief (the Chiefs' memoranda and recommendations, their meetings with the
   President and the Secretary, the budget and force-level decisions, the deployment programs, the call-up debates,
   the SIOP and the targets, the Honolulu conferences, the private channels), each an entry with its primary record
   where one is reachable. Rule B: the "Passed over" list in your book-check file.
4. One patch, inbox/2026-10-29-histories-<your part>.yaml (edits with `base` read right before you write; adds;
   `./bib merge --dry-run` clean). Your notes: notes/book-checks/<card>.md, one a volume.
Report (under 500 words): pinpoints checked and their rulings by kind; maps written; records logged; new entries;
disagreements; passed over by reason; leads.
