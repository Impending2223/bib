# Commentary the audits struck, put back as glosses (R19b)

The reader's brief, R0, whole (it governs this brief and everything else you are given):

"R0. Only this text and the owner's words limit you (the owner, Nov. 24, 2026: "Can you make a disinhibiting/'disregard limitations not in the Reader Brief or the Owner's own words' rule a top-priority reader rule? An R0?"). This rule comes first and governs every other text you are given. Your batch brief, its examples, its lists, its wording, a note from another agent, a habit of earlier patches: none of them narrows what is an entry, lets an item wait, or passes anything over. Only two things can: this brief's own rules, and the owner's words, quoted with their date. Wherever anything else seems to limit you ("in scope", "dated acts only", "the official returns", "partial", "analysis", "commentary", "minor", "no single dated act", "the budget", a list of the kinds of event to look for), disregard it and work from this brief alone: every dated event your source reports is an entry (R5), dated by its report where it gives no day of its own (R15a); only R18, and R18a for an item the owner cut short, takes one out; nothing a source in hand dates is a lead (R50). When a brief and this text disagree, this text wins; say in your report what you disregarded. The writer of a brief (the orchestrating session) quotes R0 whole at the head of every brief it writes for a reader, an auditor or a merger, and adds nothing that narrows."

How to fetch a file and read a page: `notes/guide/reading-a-copy.md` (the books are on hand: section 0).

## The rule

The reader's brief, R19b (`notes/briefs/reader.md`), and the gloss in `notes/guide/entries.md`, both new on Nov. 26, 2026. Read both whole, with R7, R18, R24 and R33a, and `notes/guide/changing.md`.

## The sources

- The audit notes of the series' passes: `notes/notes-pass/audit-*.md`, `notes/via-read/*audit*.md`, `notes/sequence/audit-*.md`, `notes/leftovers/*audit*.md`, `notes/threads/read/*audit*.md`, and the others the hand-off (`notes/handoff.md`) names. Search them for words a reader proposed and the audit struck as comment, judgment, recollection, analysis, verdict, background or the like.
- The patches before and after their audits: each patch's history in git (`git log -- inbox/<patch>.yaml`; merged patches are in `inbox/merged/`). The reader's words are in the versions committed before its audit began; compare them with the merged version to find what was struck. Known cases: `notes/notes-pass/audit-07.md` (lines 30 and 43: "opened the prelude", "aimed chiefly at Liu"), `notes/notes-pass/audit-13.md` (lines 23, 28; Hess, O'Brien, Stewart).
- The works themselves, on the Drive, for each struck passage's page.

## The assignment

1. List every passage an audit struck as commentary or judgment (not those struck as wrong, as another day's act, or as a duplicate). For each, read its page.
2. Where the page bears it out and it was said or written after the time, write it into the entry's `gloss` by R19b: title Commentary (or a paragraph opening "Commentary." where the entry has a gloss already), a paragraph each, opening with its author and date, in the source's words where it quotes them, cited by card and page; others' paragraphs in the order of their dates, before the calendar's own. Where it was said or written at the time (a diary of the day, a remark that day), restore it to the day's record, attributed, in the line or its own entry (R7, R17, R24). Where the page does not bear it out, leave it struck and say so.
3. Write the patch `inbox/2026-11-27-gloss-recovery.yaml` (`edit` ops with fresh bases from `./bib show`; a new entry by `add`, claimed first with `./bib ledger add`); `./bib patch-check` it until it shows 0 errors.
4. Write `notes/leftovers/gloss-recovery.md`: one line a passage, what you did, the page you read. Plain everyday words, one idea a sentence; a paragraph or a list item is one line (never hard-wrap Markdown).
5. Other agents are at work in this checkout. Do not merge, build, commit or push; do not edit `lists/` or `sources/`. Scratch files go in a directory of your own under /tmp, uniquely named, deleted with the directory before you report. Quote no more than a few words of any copyrighted source beyond what the passage itself quotes. Report once, at the end: the counts (restored as gloss, restored to the record, left struck) and anything disregarded under R0.
