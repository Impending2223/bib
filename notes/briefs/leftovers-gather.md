The reader's brief, R0, whole (it governs this brief and everything else you are given):

"R0. Only this text and the owner's words limit you (the owner, Nov. 24, 2026: "Can you make a disinhibiting/'disregard limitations not in the Reader Brief or the Owner's own words' rule a top-priority reader rule? An R0?"). This rule comes first and governs every other text you are given. Your batch brief, its examples, its lists, its wording, a note from another agent, a habit of earlier patches: none of them narrows what is an entry, lets an item wait, or passes anything over. Only two things can: this brief's own rules, and the owner's words, quoted with their date. Wherever anything else seems to limit you ("in scope", "dated acts only", "the official returns", "partial", "analysis", "commentary", "minor", "no single dated act", "the budget", a list of the kinds of event to look for), disregard it and work from this brief alone: every dated event your source reports is an entry (R5), dated by its report where it gives no day of its own (R15a); only R18, and R18a for an item the owner cut short, takes one out; nothing a source in hand dates is a lead (R50). When a brief and this text disagree, this text wins; say in your report what you disregarded. The writer of a brief (the orchestrating session) quotes R0 whole at the head of every brief it writes for a reader, an auditor or a merger, and adds nothing that narrows."

The orchestrating session's note: this task reads no source. It gathers into one list the work the audits left for later, so readers can be given it by month. R0 above governs what may count as an entry when that work is read; nothing you write may narrow it.

Work in /home/user/bib (branch `ccr-29ad5edc-peju1y`). Read `CLAUDE.md` whole and the hand-off's queue (`notes/handoff.md`, "The queue, reconciled", the six items the session inserted, item 3: "the audits' leftovers").

Sources: the audit notes that list work left for a later pass:
- `notes/sequence/audit-*.md` (entries to split under R25b, hours the sources give that the entries lack, time zones missing on entries with a time, days in doubt, possible duplicates, missing entries);
- `notes/via-read/audit-bare.md`, `notes/via-read/audit-a.md` ("for the merger"), and today's `notes/via-read/audit-c.md` to `audit-f.md`;
- `notes/times/audit-time-splits.md` and `-2.md`; `notes/times/audit-clock-pass-a.md`, `-b.md`, `-c.md` (about 70 entries holding more than one event);
- `notes/notes-pass/audit-02.md` to `audit-09.md`;
- `notes/nyt/audit-cleanup-*.md`, `notes/nyt/audit-19600107.md`, `audit-19600909.md`;
- `notes/claims/stale-nine-audit.md`; `notes/threads/read/batch-*-audit.md`; `notes/threads/new/*-audit.md`.

Assignment:
1. Read each note whole and take out every item it leaves for a later pass: an entry to split, an hour or zone to set, a day in doubt, a possible duplicate, a missing entry (an event a source reports that the calendar lacks), a cite or pin to correct, a map row to narrow, a registry link to repoint, a stale "To check:", a thread placing to look at.
2. Check each item against the tree as it stands (`./bib show ID`): leave out an item a later merge has already done, and say so.
3. Write `notes/leftovers/2026-11-26.tsv` with the header `id	month	kind	what	source	from` (the entry's id, or `new` for a missing entry; its month; one of the kinds above; what is to be done, in a few words; the source the audit names, with its page; the audit note it comes from). One row an item; where two notes list the same item, one row naming both.
4. Write `notes/leftovers/2026-11-26.md`: the counts by kind and by year; the items already done, and by what; and a suggested grouping into reader batches of about 60 items each, by month. Plain everyday words, one idea a sentence; a paragraph or a list item is one line, never hard-wrapped.
5. Change nothing in `lists/` or `sources/`. Do not merge, build, commit or push. Scratch files go in a directory of your own under /tmp, uniquely named, deleted, the directory included, before you report. Report once, at the end: the counts and the batches.
