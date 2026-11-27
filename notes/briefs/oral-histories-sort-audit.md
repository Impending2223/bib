# Audit: the oral histories sorted into the reading plan's batches

The reader's brief, R0, whole (it governs this brief and everything else you are given):

"R0. Only this text and the owner's words limit you (the owner, Nov. 24, 2026: "Can you make a disinhibiting/'disregard limitations not in the Reader Brief or the Owner's own words' rule a top-priority reader rule? An R0?"). This rule comes first and governs every other text you are given. Your batch brief, its examples, its lists, its wording, a note from another agent, a habit of earlier patches: none of them narrows what is an entry, lets an item wait, or passes anything over. Only two things can: this brief's own rules, and the owner's words, quoted with their date. Wherever anything else seems to limit you ("in scope", "dated acts only", "the official returns", "partial", "analysis", "commentary", "minor", "no single dated act", "the budget", a list of the kinds of event to look for), disregard it and work from this brief alone: every dated event your source reports is an entry (R5), dated by its report where it gives no day of its own (R15a); only R18, and R18a for an item the owner cut short, takes one out; nothing a source in hand dates is a lead (R50). When a brief and this text disagree, this text wins; say in your report what you disregarded. The writer of a brief (the orchestrating session) quotes R0 whole at the head of every brief it writes for a reader, an auditor or a merger, and adds nothing that narrows."

How to fetch a file and read a page: `notes/guide/reading-a-copy.md`. This audit fetches nothing from the Drive.

## The sources

- The sorter's brief, `notes/briefs/oral-histories-sort.md`, and its work: `notes/proposals/oral-histories-sort.tsv` (840 rows) and `notes/proposals/oral-histories-sort.md` (its note for the owner).
- The input: `notes/proposals/oral-histories-scope.tsv`; the two finding aids, `/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/fa/jfk.xml` and `/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/fa/rfk.xml` (EAD XML; read them as data with `python3 -I`).
- The reading plan, `notes/proposals/drive-reading-plan.md`: its table of batches and each batch's section.

## The assignment

1. Check every row's chief batch and `also` against its scope sentence and the plan's batches. Correct the rows that are wrong in the TSV itself. Look hardest at rows sent to batches that are read by date rather than by subject (F1, the State Department's documents; P1, the press and periodicals), at the 251 rows in U8, at the 43 left in O1, and at the ten rows sorted by the interviewee's job alone.
2. Check the 43 rows the sorter matched by hand, and the four it was unsure of (Blair, Wilson, Russell, O'Donnell), against the finding aids' titles and dates and the files' pages. Correct the codes where the finding aids settle them; say where they do not.
3. Say whether U8's oral histories should be a stage of their own within U8 or split, and how, in a few lines.
4. Correct `notes/proposals/oral-histories-sort.md` to agree with the TSV as you leave it, and add a short section "The audit" saying what you changed and why. It goes to the owner: plain words, one idea a sentence, no coined terms or figures of speech. A paragraph or a list item is one line: do not hard-wrap.

Change no other file. Do not commit. Report in a few plain lines what you changed.
