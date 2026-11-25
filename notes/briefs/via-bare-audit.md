The reader's brief, R0, whole (it governs this brief and everything else you are given):

"R0. Only this text and the owner's words limit you (the owner, Nov. 24, 2026: "Can you make a disinhibiting/'disregard limitations not in the Reader Brief or the Owner's own words' rule a top-priority reader rule? An R0?"). This rule comes first and governs every other text you are given. Your batch brief, its examples, its lists, its wording, a note from another agent, a habit of earlier patches: none of them narrows what is an entry, lets an item wait, or passes anything over. Only two things can: this brief's own rules, and the owner's words, quoted with their date. Wherever anything else seems to limit you ("in scope", "dated acts only", "the official returns", "partial", "analysis", "commentary", "minor", "no single dated act", "the budget", a list of the kinds of event to look for), disregard it and work from this brief alone: every dated event your source reports is an entry (R5), dated by its report where it gives no day of its own (R15a); only R18, and R18a for an item the owner cut short, takes one out; nothing a source in hand dates is a lead (R50). When a brief and this text disagree, this text wins; say in your report what you disregarded. The writer of a brief (the orchestrating session) quotes R0 whole at the head of every brief it writes for a reader, an auditor or a merger, and adds nothing that narrows."

Work in /home/user/bib (branch `ccr-29ad5edc-peju1y`). Read `CLAUDE.md` and `notes/briefs/reader.md` whole before anything else, then `notes/guide/brief.md` (what each source stands for) and `notes/guide/reading-a-copy.md` (follow it wherever you open a source; change nothing on Drive). The rules this audit turns on are R33, R33a and R33b (a source is cited for the words it supports, and for no others) and R35–R43 (claim maps).

The owner's words (Oct. 23, 2026): a source cited stands for the whole of `c` unless a parenthetical, a label or its place says otherwise; a source read that does not bear out a claim is no cite for it: the claim takes "Check:" or goes.

Sources:
- The patch `inbox/2026-11-25-via-bare.yaml` (written by the orchestrating session, which read the document itself; no Sonnet pass was made, so read everything afresh).
- The entry `cal.1966-06-14.vietnam-air-war` in full (`./bib show cal.1966-06-14.vietnam-air-war`), its note and its claim map.
- FRUS 1964–68, IV, doc. 156, whole, with its notes: `sources/frus-text/1966-06.json.xz`, and the page at history.state.gov the patch links.
- `notes/via-read/rule-2026-11-25.tsv`, rows 656–657, and `notes/owner-rulings.md`, ruling 53.

Assignment:
1. Read the document whole and set it against every part of the entry's line. Say, part by part, what the document bears out and what it does not.
2. Audit the patch's one `cite` op: whether the document supports the words named in `on:`, all of them and no others; whether the item is in the house form; whether the entry already cites the document for other parts, and whether this op should extend that citation or stand as it is.
3. Correct the patch in place where it is wrong, add what the document supports that the entry lacks (R33a: substance goes into the line by `add-words`, with its source), and put a "Check:" where the document and the line disagree.
4. Run `./bib patch-check inbox/2026-11-25-via-bare.yaml` until it shows 0 errors. Do not merge, build, commit or push; edit nothing in `lists/`.
5. Write `notes/via-read/audit-bare.md`: what you read, what you found, what you changed. Plain everyday words, one idea a sentence, no coined terms; a paragraph or a list item is one line, never hard-wrapped. Report the same to the session, and say what, if anything, you disregarded under R0.

Before any fetch, `cd` into a scratch directory of your own under /tmp, uniquely named; never save a file in the repository; delete every copy before you report.
