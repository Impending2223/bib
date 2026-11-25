The reader's brief, R0, whole (it governs this brief and everything else you are given):

"R0. Only this text and the owner's words limit you (the owner, Nov. 24, 2026: "Can you make a disinhibiting/'disregard limitations not in the Reader Brief or the Owner's own words' rule a top-priority reader rule? An R0?"). This rule comes first and governs every other text you are given. Your batch brief, its examples, its lists, its wording, a note from another agent, a habit of earlier patches: none of them narrows what is an entry, lets an item wait, or passes anything over. Only two things can: this brief's own rules, and the owner's words, quoted with their date. Wherever anything else seems to limit you ("in scope", "dated acts only", "the official returns", "partial", "analysis", "commentary", "minor", "no single dated act", "the budget", a list of the kinds of event to look for), disregard it and work from this brief alone: every dated event your source reports is an entry (R5), dated by its report where it gives no day of its own (R15a); only R18, and R18a for an item the owner cut short, takes one out; nothing a source in hand dates is a lead (R50). When a brief and this text disagree, this text wins; say in your report what you disregarded. The writer of a brief (the orchestrating session) quotes R0 whole at the head of every brief it writes for a reader, an auditor or a merger, and adds nothing that narrows."

Work in /home/user/bib (branch `ccr-29ad5edc-peju1y`). Read `CLAUDE.md` and `notes/briefs/reader.md` whole before anything else, then `notes/guide/calendar-by-day.md` (the paragraph "The day's order") and `notes/guide/reading-a-copy.md` (follow it wherever you open a source; change nothing on Drive). The rules this audit turns on are R25c (the day's order: what goes after what) and R33b (the audit).

The owner's words (Nov. 24, 2026): "Shouldn't all the fellows responding to Truman's naming of them get a 'follows:' tag too? Is there a way to get this into a reader/auditor brief or a subsequent 'sort'/'sequence' pass? Many of these seem like could easily be sorted with a simple 'put them together, read them, and ask yourself \"what goes after what?\"' pass. No?"

Sources:
- The patch `inbox/2026-11-25-sequence-1961-01.yaml` (a Sonnet reader's) and its note `notes/sequence/1961-01.md`. Its brief was `notes/briefs/sequence-1961-01.md`.
- The calendar's entries of 1961-01, a day at a time: `python3 -I tools/times/day_order.py 1961 --from 1961-01 --until 1961-01 --full > <a file in a scratch directory of your own, uniquely named>` (some minutes; run it once, read every day of it).
- Each entry in full (`./bib show ID`), its note, and the sources it cites, wherever the lines do not settle an order.

Assignment:
1. Audit every link in the patch against the two entries, and against their sources where the lines do not show the order: strike a link the record does not bear out, turn round one that runs the wrong way, and point a link at the entry its entry comes directly after.
2. Read every day of the month yourself as R25c asks, and add the links the reader did not write.
3. Correct the patch in place. `./bib patch-check inbox/2026-11-25-sequence-1961-01.yaml` until it shows 0 errors.
4. Write `notes/sequence/audit-1961-01.md`: links checked, kept, struck, turned, added; what you read beyond the lines; what is left. Plain everyday prose; a paragraph or a list item is one line (never hard-wrap Markdown).
5. Do not merge, build, commit or push, and do not edit `lists/`. Report at the end in plain prose, and say whether the patch is ready to merge.
