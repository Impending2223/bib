# The notes pass: what the Branch readers did, to standardize (Nov. 16, 2026)

The owner, Nov. 16 ("Immediate"): "The Taylor Branch readers appear to have been much better and more thorough at reading the books' footnotes, matching claims to 'To check:' pointers, and filling out the witness graph, than other readers, or than your trial/pilot with DeBenedetti. Is there anything in the Taylor Branch readers' methods that we can adapt and standardize?"

## The measure (Nov. 16, from the tree)
Per work: the calendar's cites to it; the edges in its `sources/witnesses/by-work/` file (each a note item tied to a page); the "To check: ... (cited by [[w.X]], page)" pointers made from its notes; the `via` rows tying an entry's units to its notes.

| Work | Cites | Edges | To-check pointers | via rows | Edges per cite |
|---|---|---|---|---|---|
| Branch, *At Canaan's Edge* | 2,971 | 4,330 | 2,223 | 213 | 1.46 |
| Branch, *Pillar of Fire* | 2,341 | 2,077 | 1,599 | 1,493 | 0.89 |
| Branch, *Parting the Waters* | 1,645 | 1,831 | 845 | 1,425 | 1.11 |
| Gibbons, *U.S. Government and the Vietnam War* | 3,045 | 2,027 | 1,015 | 1,592 | 0.67 |
| Preston, *War Council* | 774 | 1,445 | 260 | 532 | 1.87 |
| Garrow, *Bearing the Cross* | 496 | 539 | 192 | 520 | 1.09 |
| Thomas, *Robert Kennedy* | 1,081 | 1,032 | 279 | 225 | 0.95 |
| Kotz, *Judgment Days* | 991 | 767 | 276 | 170 | 0.77 |
| Bernstein, *Guns or Butter* | 1,755 | 870 | 412 | 63 | 0.50 |
| Perlstein, *Before the Storm* | 462 | 222 | 158 | 194 | 0.48 |
| Dallek, *Flawed Giant* | 729 | 271 | 150 | 227 | 0.37 |
| Logevall, *Choosing War* | 142 | 49 | 22 | 41 | 0.35 |
| DeBenedetti, *An American Ordeal* | 341 | 72 | 39 | 63 | 0.21 |

## What the Branch readers did (their book-check files)
The rules were the same for everyone (R35–R43: "For each page you cite for an entry, each witness the work's note gives for that passage"). The Branch readers kept them; the others rationed them. DeBenedetti's file says so: it registered the notes "for every passage cited under an entry in the tree that this run mapped" and for new entries resting on one document, and "not registered: the notes to chapters 2–4". What the Branch readers did instead:
1. **Every item of every note for every page cited.** Not the notes that seemed to matter: each document, file, wiretap, recording, interview, press account and study a passage's note gives, for every page the run cited.
2. **Works as edges, unheld studies as rows.** A work with a card is an edge (`of: w.…`, with the page the author cites); a study the series does not hold is a row, `kind: study`, `open: not held`. Nothing left out because it was "secondary".
3. **An anchor for notes without numbers.** Branch's notes are keyed to the page and a phrase; the readers anchored each edge "the page and the note's first words". A book with numbered notes anchors by chapter and number.
4. **A "To check:" from each note on each entry it bears on**, `To check: X (cited by [[w.branch-…]], 123)`, and the `via` rows tying the entry's units to the note.
5. **Matching what the series holds.** Recordings found in the Miller Center's catalogue given it as their copy; FRUS documents joined to the daybook's.
6. **Runs of about 100–130 pages.** Each volume read in four or five runs (`b3-branch-pof-1` … `-5`; `-ace-1` … `-4`), each with its pages' notes; each run's file says where it stopped. DeBenedetti was one run of 200 pages and 54 pages of notes, and the notes were what gave.
7. **A second pass where a run fell short.** When a first run left out the studies and memoirs its notes cite, the next run added them for the first run's pages (313 edges) before going on.
8. **Checked before handing in.** Pinpoints checked against the page images; both patches merged in a scratch copy, `./bib check` run there, and the errors mended in the patch.

## To standardize (for the owner's ruling)
- **R3, a step of its own:** after each run of text, "the notes pass": the notes of every page cited in the run, every item of each, as R35–R38 require: rows, edges (with the anchor), "To check:" lines and `via` rows. No item passed over as secondary.
- **R3, the run's size:** a run is about 100–150 pages of text with their notes; a longer book is several runs, each file saying where it stopped.
- **R35, the anchor:** numbered notes by chapter and note ("ch. 5 n. 21"); unnumbered notes by the page and the note's first words.
- **A coverage check (tooling, queued):** `./bib notes-coverage CARD`: the pages the calendar cites for a work against the pages its edges cover; the pages cited with no edge listed. Readers run it before handing in; the audit reads it; a run with pages cited and no notes registered goes back.
- **Re-runs of the notes pass** for the works furthest behind (edges per cite under 0.5 with full notes: DeBenedetti, Logevall, Dallek, Perlstein, Bernstein and the rest the coverage check finds), as a batch.
