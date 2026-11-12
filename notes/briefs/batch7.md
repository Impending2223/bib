# Batch 7: the "already in" rows read against the calendar (Nov. 10, 2026)

The owner, Nov. 10, 2026: "Have we gone over the readers who passed over matters 'already in' to see whether the book says something different than our calendar? I'm not sure what the then-current 'already in' rule had the readers pass over. Do we still have that rule? (I hope not!)"

The rule is gone: R44 (in force from Oct. 30) says an event already in the calendar is never passed over; it takes the work's cite (R29) and its witnesses (R43). Readers before it listed such events under "Passed over" as "already in". Of their 1,159 rows, 310 have the work cited under the entry by page; the rest are this batch: the work not cited under the entry the row names (515), or no entry named (332), or the entry missing (1). A reader a work or a few, the rows from `/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/alreadyin/rows.json` (each row's file, card, the ids it names, and `state`; take those not `cited`).

## For every reader

1. Read `CLAUDE.md`, then `notes/briefs/reader.md` in full: R5, R13, R17, R18 (as amended Nov. 6), R29, R35-R44, R48, R50, R51, R53, R54. Never read `build/` or a whole list file.
2. The copy: download it as R54 says into a new empty directory under the session's scratchpad, `books/b7-<short>/` (scripts in a subdirectory); read each page you cite off the page image as well as the text; delete your copies when you finish.
3. Each row: read the work's page; find the entry or entries (the ids the row names; where none, `./bib ledger find DATE [--until DATE]` and `./bib find WORDS -l cal --since ... --until ...`). Then:
   - the page bears the entry out: cite the work under it by page (the additive `cite` op, its units; out of "To check:" where it stands there), its witnesses (R43);
   - the page says something the entry does not, or otherwise (another day, another number, another speaker, other words): a variant (the additive `variant` op, R41) or a Check, and the cite for what it does bear out;
   - the page treats an event the calendar does not hold after all (the row's "already in" was wrong): the entry, by R5;
   - the page gives nothing the entry rests on: say so in the row; no cite.
4. In the book-check file: a line at the head of Passed over, "The 'already in' rows read against the calendar, Nov. 10, 2026 (batch 7)"; each row's ruling (cited under ID; variant on ID; Check on ID; entered as ID; not borne out), the row moved out of Passed over into the run's section where it is now cited or entered.
5. Witnesses to `inbox/witnesses/2026-11-10-b7-<short>.yaml` (write to a scratch copy and move it in when it checks: a broken file in inbox/ stops every merge); edges to `sources/witnesses/by-work/<card>.yaml`, each edge's witness registered first.
6. One patch a work, `inbox/2026-11-10-b7-<short>.yaml` (a second, `-2`, past some 400 ops): new entries claimed first in the ledger; additive ops wherever you only add (R51); `edit` with a fresh base only where you change `c` or rewrite `n`. `./bib patch-check` until no errors.
7. Do not merge, fold or commit: the lead does. Working hours: stop at a clean point by 6:30 a.m. Pacific on a weekday, and say in the book-check file where you stopped.
8. Your last message: per work, the patch's name and size (cites, variants, checks, entries), the rows not borne out, the rows not settled and why.
