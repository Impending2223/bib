# Batch 9: the open "already in" rows, at the owner's pace, every cite audited (Nov. 11–12, 2026)

The rows batch 8 did not reach (`/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/alreadyin/b9-rows.json`, recomputed Nov. 11 evening). The owner, Nov. 11, 2026: "Pick up the pace with 1–4, as suggested" (more readers at once; the auditor hands back the corrected patch; the small books grouped; the waves overlapped) and "Every cite, everywhere" (the audit reads every row and every op, not a sample).

## Readers (Sonnet)

Exactly as `notes/briefs/batch8.md`, "For every reader", on the card as it stands tonight (`notes/briefs/reader-card.md`: the unit-map, Check, neighbour, search and visibility lines are new; read them twice). Patch names `2026-11-12-b9-<short>.yaml`; for a book split between readers, `-a`, `-b`, `-c` by page range; for a group of small books, `2026-11-12-b9-group-<n>.yaml`, one patch, the works' book-check files each updated.

## Auditors (Opus)

1. **Blind, every row.** Read every row of the reader's share on the page (the same copy), and write your own table of rulings and units before you open the patch or the book-check's batch-8/9 block.
2. **Every op.** Then every op in the patch: each cite on the event the page tells (not a neighbour), each unit letter against `./bib claims show ID` (a unit the page does not state wholly is an error: `'?'` and the parenthetical), each parenthetical against the page, each variant and Check a real disagreement with a unit (not added content; not a different count of a different thing; not Saigon's date for Washington's), each new entry word for word, one event, its day as the work gives it, not already in the calendar (search the days around it), its links pointing back.
3. **The corrected patch.** Write the corrected patch yourself, `<same name>-audited.yaml`, in your scratch directory, with `./bib patch-check` at 0 errors (new ids: `./bib new-id`, `./bib ledger add` under the patch's name; a dropped claimed id keeps its ledger line, its words "(not used: ...)"). If the harness refuses the write, return the fixes instead, each as an exact op, as batch 8 did.
4. **Missed by the reader**: add the ops for what the reader missed on its pages (cites, variants, Checks, entries), on the same rules.
5. Write nothing in `lists/`; never merge or commit.
6. **Last message**: agreement by row; the errors by kind with counts; the error rate (ops wrong of ops in the reader's patch); what you added; the corrected patch's path and patch-check line; anything you could not settle.

## The lead

Reads each audit's report, checks the corrected patch (`patch-check`), merges it, commits, pushes; starts the next reader the moment one finishes.
