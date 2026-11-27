# Audit: the reading plan's rows split and their cards corrected

The reader's brief, R0, whole (it governs this brief and everything else you are given):

"R0. Only this text and the owner's words limit you (the owner, Nov. 24, 2026: "Can you make a disinhibiting/'disregard limitations not in the Reader Brief or the Owner's own words' rule a top-priority reader rule? An R0?"). This rule comes first and governs every other text you are given. Your batch brief, its examples, its lists, its wording, a note from another agent, a habit of earlier patches: none of them narrows what is an entry, lets an item wait, or passes anything over. Only two things can: this brief's own rules, and the owner's words, quoted with their date. Wherever anything else seems to limit you ("in scope", "dated acts only", "the official returns", "partial", "analysis", "commentary", "minor", "no single dated act", "the budget", a list of the kinds of event to look for), disregard it and work from this brief alone: every dated event your source reports is an entry (R5), dated by its report where it gives no day of its own (R15a); only R18, and R18a for an item the owner cut short, takes one out; nothing a source in hand dates is a lead (R50). When a brief and this text disagree, this text wins; say in your report what you disregarded. The writer of a brief (the orchestrating session) quotes R0 whole at the head of every brief it writes for a reader, an auditor or a merger, and adds nothing that narrows."

How to fetch a file and read a page: `notes/guide/reading-a-copy.md`. This audit may open a file's first page where its name alone does not settle which work it is (a ranged request, as that guide says); it reads nothing else.

## The sources

- The brief for the pass, `notes/briefs/drive-plan-rows.md`; its work: `notes/proposals/drive-reading-plan.tsv` (rewritten) and `notes/proposals/drive-plan-rows.md`; the TSV before it, in git (`git show HEAD:notes/proposals/drive-reading-plan.tsv` or the commit before the pass).
- `notes/proposals/drive-reading-plan.md`, the plan itself; the works catalogue (`./bib works`, `./bib works show`), `notes/book-checks/`, `notes/procurement.yaml`.

## The assignment

1. Check every split row and every corrected card against the files' names and the cards (`./bib works show`): one work a row; its volumes, parts and copies together; the right card. Check the 11 rows still weak and settle them, opening a first page where the name does not. Settle what the pass left open (the sets with one volume's card, Solomon, the two Cultural Revolution compilations, row 211, the NSA papers) where you can. Correct the TSV in place.
2. Bring `drive-reading-plan.md` into agreement with the TSV: the table of batches (works, files, pages, readers), each changed batch's section (its works and readers), and the totals at the head and in "The unread, in batches". Change nothing else in the plan.
3. Add a section "The audit" to `notes/proposals/drive-plan-rows.md`: what you changed and why. It goes to the owner: plain everyday words, one idea a sentence, no coined terms or figures of speech; a paragraph or a list item is one line (never hard-wrap Markdown).

Change no other file. Do not commit. Report once, at the end, in a few plain lines.
