# Batch 5: the leads sent back (Nov. 5, 2026)

The owner's rulings on the docket, Nov. 5, 2026: on the leads canvass (`notes/leads-canvass.md`), "Send them all back, work by work, a reader a work, the largest first"; on the items filed as leads that are minor or now entries (its class D), "Enter those R18 now admits; move the rest to Passed over with their ground." A reader a work, the works in the order below.

## For every reader

1. Read `CLAUDE.md`, then `notes/briefs/reader.md` in full: R5, R13, R14, R17, R18, R35-R43, R44, R48, R49-R51, R50 (a lead is only what cannot go in on a source in hand: restated Nov. 5), R54. Never read `build/` or a whole list file.
2. Your work's rows: `notes/leads-canvass.md`, under your work's short name in "B: entry-writable now, by work" (and C and D, if it has rows there: `grep -n '<short>' notes/leads-canvass.md`). Your work's book-check file, `notes/book-checks/<short>.md`, names the copy read (a Drive id, an archive.org identifier, a govinfo or DTIC copy) and its folio offset; its Passed over and Leads sections are where the rows came from.
3. The copy: download it as R54 says (Drive by the direct route) into a new empty directory under the session's scratchpad, `books/b5-<short>/`; read each page you cite off the page image as well as the text; delete your copies when you finish. A copy you cannot reach: say so in the book-check file and your last message; leave the rows as they are.
4. Each B row: first see whether the calendar already has the event (`./bib ledger find DATE [--until DATE]`; `./bib find WORDS -l cal --since ... --until ...`): if so, cite your work under it (the additive `cite` op) where it is not cited; if not, the entry, on the page read (R5): its day, or "Check: the day" where the work dates it loosely (the restated rule). A row the page does not bear out: say so. A row that is in fact minor by R18: a Passed over row with the ground.
5. Each C row: a variant (R41) or a Check on the entry it disputes. Each D row: an entry where R18 now admits it (another country's domestic politics, a church body's resolution, and the like), else a row of Passed over with its R18 ground, for the owner to rule (R44).
6. In the book-check file: each row ruled (entered, cited under, Passed over, not borne out), the leads section pruned of what you settled, the Passed over rows updated. Take nothing out of `notes/leads.md` yourself; list in your last message the leads.md items you settled, and the merger removes them.
7. Witnesses (R35-R43) for the units you cite, to `inbox/witnesses/2026-11-05-b5-<short>.yaml`; edges to `sources/witnesses/by-work/<card>.yaml`.
8. One patch, `inbox/2026-11-05-b5-<short>.yaml` (a second, `-2`, past some 400 ops): new entries claimed first in the ledger (`./bib ledger add`); additive ops wherever you only add (R51); `edit` with a fresh base only where you change `c` or rewrite `n`. `./bib patch-check` until no errors.
9. Do not merge, fold or commit: the merger does. Working hours: CLAUDE.md, "Working hours"; if told to pause, stop at a clean point and say in the book-check file where you stopped.
10. Your last message: the patch's name and size (entries added, cites, checks, rows passed over), the rows not settled and why, the leads.md items settled.

## The works, largest first

Gibbons (193), Bernstein (158), Perlstein (130), Kaplan (122), Thomas (99), Kotz (98), Smith (97), Fursenko and Naftali, *Khrushchev's Cold War* (77), CQ Weekly Report, July 26, 1968 (75), Longley (72), *Rights in Conflict* (71), Herring (69), Sorensen (69), Fursenko and Naftali, *One Hell of a Gamble* (68), Logevall (65), Watson (63), Branch, *Pillar of Fire* (60), Novak (56), Kallina (55), Drea (54), Branch, *Parting the Waters* (52), the MACV Command Histories (51), Cosmas, 2012 (49), Dallek (48), Asselin (44), CQ Weekly Report, Aug. 2, 1968 (44), Woods (42), Zhai (40), and the rest of the canvass's list in its order.
