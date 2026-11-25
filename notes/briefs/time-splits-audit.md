The reader's brief, R0, whole (it governs this brief and everything else you are given):

"R0. Only this text and the owner's words limit you (the owner, Nov. 24, 2026: "Can you make a disinhibiting/'disregard limitations not in the Reader Brief or the Owner's own words' rule a top-priority reader rule? An R0?"). This rule comes first and governs every other text you are given. Your batch brief, its examples, its lists, its wording, a note from another agent, a habit of earlier patches: none of them narrows what is an entry, lets an item wait, or passes anything over. Only two things can: this brief's own rules, and the owner's words, quoted with their date. Wherever anything else seems to limit you ("in scope", "dated acts only", "the official returns", "partial", "analysis", "commentary", "minor", "no single dated act", "the budget", a list of the kinds of event to look for), disregard it and work from this brief alone: every dated event your source reports is an entry (R5), dated by its report where it gives no day of its own (R15a); only R18, and R18a for an item the owner cut short, takes one out; nothing a source in hand dates is a lead (R50). When a brief and this text disagree, this text wins; say in your report what you disregarded. The writer of a brief (the orchestrating session) quotes R0 whole at the head of every brief it writes for a reader, an auditor or a merger, and adds nothing that narrows."

Work in /home/user/bib (branch `ccr-29ad5edc-peju1y`). Read `CLAUDE.md` and `notes/briefs/reader.md` whole before anything else, then `notes/guide/reading-a-copy.md` (follow it; change nothing on Drive) and `notes/guide/calendar-by-day.md`. The rules this audit turns on are R25b (several acts in a day, one of them timed), R17 (one event, one entry), R25 and R25a (the fields), R22 (`kind:`), R34, R4 and R54a.

The owner's words (Nov. 24, 2026): "Ruling 52 should be revised into a pair of entries, one dated precisely, and one with an inverse-'follows:', no? ('precedes:'?)"

Sources:
- The patch `inbox/2026-11-25-time-splits.yaml` (a Sonnet reader's: 26 `edit` ops, 51 `add` ops, one `place-key`) and its note `notes/times/time-splits.md`. The reader read FRUS, the Public Papers and the Miller Center catalogue, and two pages of Branch; it did not open the other books and chronologies behind its splits (Califano, Howard, Ralph, Anderson, Palermo, Witcover, the Mao and Zhou nianpu, the Wengao, MACV and others), whose hours stand as the original entries gave them.
- Each entry (`./bib show ID`), its note, and the sources cited at the pages cited.

Assignment:
1. Audit every split against the sources: read the page behind each hour, day, clock and order. Each new entry holds one act, its own sources named for its own words, its fields, its name tags and "Names:", and points back; the first entry keeps the id and the event's bibliography; `follows:` stands on the later entry with its basis in the note. Correct the patch in place.
2. Audit the about 20 entries the reader left as one entry: apply R25b and R17 to each yourself.
3. Every edit in the patch states `kind: correct`; hold each to R22 (the sentence in the note that names the settling record), or state the kind the brief calls for.
4. `./bib patch-check inbox/2026-11-25-time-splits.yaml` until it shows 0 errors. Its same-day duplicate warnings are for the merger.
5. Write `notes/times/audit-time-splits.md`: splits checked, changed, struck, added; the pages read; what could not be read and why. Plain everyday prose; a paragraph or a list item is one line (never hard-wrap Markdown).

A second reader has the candidates the first did not reach (`inbox/2026-11-25-time-splits-2.yaml`); leave those. Other agents are at work in this checkout on other files. Do not merge, do not run `./bib build`, do not edit files under `lists/`, and do not commit or push: leave your files in place and report. `./bib check` takes about five minutes. Quote no more than a few words of any copyrighted source.

Report: what you checked against a page and what you could not, what you changed and why, whether the patch is ready to merge, and what you disregarded under R0, if anything.