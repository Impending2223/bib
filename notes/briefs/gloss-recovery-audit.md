# Audit: commentary put back as glosses (R19b)

The reader's brief, R0, whole (it governs this brief and everything else you are given):

"R0. Only this text and the owner's words limit you (the owner, Nov. 24, 2026: "Can you make a disinhibiting/'disregard limitations not in the Reader Brief or the Owner's own words' rule a top-priority reader rule? An R0?"). This rule comes first and governs every other text you are given. Your batch brief, its examples, its lists, its wording, a note from another agent, a habit of earlier patches: none of them narrows what is an entry, lets an item wait, or passes anything over. Only two things can: this brief's own rules, and the owner's words, quoted with their date. Wherever anything else seems to limit you ("in scope", "dated acts only", "the official returns", "partial", "analysis", "commentary", "minor", "no single dated act", "the budget", a list of the kinds of event to look for), disregard it and work from this brief alone: every dated event your source reports is an entry (R5), dated by its report where it gives no day of its own (R15a); only R18, and R18a for an item the owner cut short, takes one out; nothing a source in hand dates is a lead (R50). When a brief and this text disagree, this text wins; say in your report what you disregarded. The writer of a brief (the orchestrating session) quotes R0 whole at the head of every brief it writes for a reader, an auditor or a merger, and adds nothing that narrows."

How to fetch a file and read a page: `notes/guide/reading-a-copy.md` (the books are on hand: section 0).

## The sources

- The reader's brief, R19b, R7, R24, R33b (`notes/briefs/reader.md`), and the gloss in `notes/guide/entries.md`: read them whole. `notes/guide/changing.md`.
- The reader's brief for this pass, `notes/briefs/gloss-recovery.md`, its patch `inbox/2026-11-27-gloss-recovery.yaml` and its note `notes/leftovers/gloss-recovery.md`.
- The works on the Drive, for every page the patch cites; the audit notes and the patches' history in git that the reader searched.

## The assignment

1. Hold every op to its page (R33b): the words, the author, the date, the pinpoint. Check that each gloss paragraph is later commentary and each restored line is the day's record (R19b), that a gloss with more than one kind is titled by its first kind and each other kind's paragraphs open with their title, and that others' paragraphs come in date order before the calendar's own. Where O'Brien's words on May 6, 1964 rest on the Johnson tapes (Purdum's note), find the date they were said, if a source in hand gives it, and place them by R19b.
2. Search the audit notes and the patches' history once more for commentary struck that the reader missed (passages struck without the words it searched for), in the notes pass and the other passes, and add each, read on its page, to the patch.
3. Correct the patch in place until `./bib patch-check` shows 0 errors, and add a section "The audit" to `notes/leftovers/gloss-recovery.md`: what you changed and why, in plain everyday words, a paragraph or a list item one line (never hard-wrap Markdown).
4. Other agents are at work in this checkout. Do not merge, build, commit or push; do not edit `lists/` or `sources/`. Scratch files go in a directory of your own under /tmp, deleted with the directory before you report. Quote no more than a few words of any copyrighted source beyond what the passage itself quotes. Report once, at the end, in a few plain lines.
