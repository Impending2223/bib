The reader's brief, R0, whole (it governs this brief and everything else you are given):

"R0. Only this text and the owner's words limit you (the owner, Nov. 24, 2026: "Can you make a disinhibiting/'disregard limitations not in the Reader Brief or the Owner's own words' rule a top-priority reader rule? An R0?"). This rule comes first and governs every other text you are given. Your batch brief, its examples, its lists, its wording, a note from another agent, a habit of earlier patches: none of them narrows what is an entry, lets an item wait, or passes anything over. Only two things can: this brief's own rules, and the owner's words, quoted with their date. Wherever anything else seems to limit you ("in scope", "dated acts only", "the official returns", "partial", "analysis", "commentary", "minor", "no single dated act", "the budget", a list of the kinds of event to look for), disregard it and work from this brief alone: every dated event your source reports is an entry (R5), dated by its report where it gives no day of its own (R15a); only R18, and R18a for an item the owner cut short, takes one out; nothing a source in hand dates is a lead (R50). When a brief and this text disagree, this text wins; say in your report what you disregarded. The writer of a brief (the orchestrating session) quotes R0 whole at the head of every brief it writes for a reader, an auditor or a merger, and adds nothing that narrows."

Work in /home/user/bib (branch `ccr-29ad5edc-peju1y`). Read `CLAUDE.md` whole, then `notes/guide/brief.md` (threads and their statements), `notes/owner-rulings.md` (rulings 58–62), the new thread's entry in `lists/cal/th.yaml`, and the reader's brief you audit, `notes/briefs/threads-new-jd.md` (its assignment is the rule you audit against).

The owner's words (Nov. 26, 2026, about 1:53 p.m. PT): "Instead of antisemitism, "Jewish diaspora" (i.e., Jews not in Israel). Instead of "Eastern Europe," "Comecon" (i.e., Comecon members and associate members west of the Soviet Union, excluding observers and the later DRV/SRV)."

Sources:
- `notes/threads/new/jd-ids.tsv` (the entries the reader was given), `notes/threads/new/jd.tsv` and `jd.md` (the reader's placings and note).
- The entries themselves in `lists/cal/*.yaml`: each entry's whole line and whole note.

Assignment:
1. Read, whole, every entry the reader put in the thread (primary or secondary), every entry it names as nearest to a doubt, and a random sample of your own, with a seed of your own, of 40 of the entries it left out. Judge each by the reader's brief's rules 1 and 2.
2. Check by script over the whole tsv: one row for every id; every slug in `th.yaml`; no thread beside its parent or child; no `also` holding the primary.
3. Mend `jd.tsv` in place where it is wrong, the row's `basis` beginning `AUDIT:`; where a fault repeats, find every row of that kind and mend each, reading it first.
4. The words found the candidates; they cannot find an entry of the thread that uses none of them. Search the calendar with words of your own (the names of persons, places and bodies the thread's entries name) for entries of the thread the list missed, read each, and add a row for each to `jd.tsv` (marked `AUDIT: found`).
5. Write `notes/threads/new/jd-audit.md`: what you read, the counts, the mends, the entries found, whether the tsv is fit to apply. Plain everyday words, one idea a sentence; a paragraph or a list item is one line, never hard-wrapped.
6. Change nothing in `lists/`, `th.yaml` or `sources/`. Do not merge, build, commit or push. Scratch files go in a directory of your own under /tmp, uniquely named, deleted, the directory included, before you report. Report once, at the end.
