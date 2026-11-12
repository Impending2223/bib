# Batch 8: the "already in" rows still open, read by the card, audited (Nov. 11, 2026)

Batch 7 (`notes/briefs/batch7.md`) was stopped mid-work on Nov. 10. Its patches were merged as they stood, and the rows were sorted again (`python3 -I tools/works/alreadyin_rows.py OUT.json`): a row whose work is now cited under its entry is done. The rest are this batch. It follows the owner's word of Nov. 10, 2026 ("Agreed to all your suggestions"): Sonnet readers on the reader card, three at a time, and an Opus audit of each book on a sample of its rows, with every disagreement read, before anything is merged.

## For every reader

1. Read `CLAUDE.md` and `notes/briefs/reader-card.md`; nothing else unless the card sends you there (`notes/briefs/reader.md`, the rule by number). Never read `build/` or a whole list file.
2. Your rows: those your task names, from the rows file it gives (each row's book-check file, card, the ids it names, its `state`). For each row, the test of `notes/briefs/batch7.md`, step 3: the page bears the entry out (a `cite`, its units); the page says otherwise (a `variant` or a `check`, and the cite for what it bears); the calendar lacks the event (an entry, by the card); the page gives nothing the entry rests on (say so; no cite).
3. The copy as the card and R54 say, in your own new directory under the scratchpad, `books/b8-<short>/`; delete it when done.
4. Out of the repository until done: the patch in your scratch directory, `2026-11-11-b8-<short>.yaml`; `./bib patch-check` on it there; move it into `inbox/` only at the end. New ids: `./bib new-id`, then `./bib ledger add` as you go.
5. The book-check file, at the end: under the batch 7 line at the head of Passed over (add it if missing), each row's ruling (cited under ID; variant on ID; Check on ID; entered as ID; not borne out), and a last line, "Where batch 8 stopped: ...".
6. Never merge, never commit. Stop at a clean point by 6:30 a.m. Pacific on a weekday.
7. Last message: per work, the patch and its size; the table of rows (row, ruling, entry or ground); the rows you could not settle and why.

## For the auditor (one per book, Opus)

Blind first: before opening the reader's patch, read a sample of the book's rows from the same copy and write your own table (every row if the book has 12 or fewer; else 12 chosen across the book, and every row the reader entered as new). Then compare with the patch: each disagreement read again on the page and ruled; every unit map in the patch checked against the page (a unit the page does not state is an error); every new entry's `c` checked word by word against the page; bundling (one event, one entry). Write nothing in `lists/` or `inbox/`; your report goes to the lead, who fixes the patch before merging. Last message: agreement (rows), the errors by kind with the fix for each, the error rate, and anything the reader and you both missed.
