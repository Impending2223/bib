# Sources tied to parts of an entry: the design (rulings 35f and 35g)

For the owner first, the implementer second. Nov. 25, 2026.

This note replaces the design that stood here until today (a list of stored claims with frames; git history keeps it). The owner's questions of Nov. 24 and rulings 31, 32, 35 and 35f in `notes/owner-rulings.md` set that design aside. This note states ruling 35f, with the three additions of ruling 35g. The two reviews are `notes/proposals/claims-model-review.md` and `notes/proposals/claims-model-review-fable.md`.

Five terms, used the same way throughout.

- The **line** is an entry's `c`.
- A **unit** is a sentence of the line, or a clause that ends in a semicolon. The tools find the units by rule each time they need them. This is today's term.
- A **cut** is a mark stored in the line at the end of some words. The page never shows it.
- A **part** is the words between two cuts. An entry with no cut has one part, the whole line.
- A **row** is one line of an entry's `src`: a source, its page, and the words it supports.

## (a) What changes and what does not

The build already makes the footnotes the owner described on Nov. 24 at 4:00 p.m. `footnotes.py` takes the units in order. Neighbouring units with the same sources share one mark and one footnote. The footnote is compiled from the rows. Two neighbouring footnotes are never the same.

So the page does not change. One thing under it changes: how a row names the words it supports.

Today a row names units by letter: `'w.yang-jisheng-mubei II, 1150: B'`. The letters are counted from the punctuation each time. If someone adds a sentence, every later letter names a different sentence. The tools notice this for rows (the map is marked stale) and do not notice it for visibility rulings or variants.

Under 35f a row names parts by number. The number is stored in the line itself, in a cut, at the end of the part. Words can be added or changed around a cut and the number stays with its words.

What does not change:

- The line stays one string of prose.
- The note `n` stays the citation record.
- `src` keeps its rows. `all` and `?` keep their meaning.
- `footnotes.py` compiles as it does now. Its ten STYLE rules stand.
- The units stay. Footnotes and visibility still work unit by unit. A part is a run of whole units with a stored number.
- An entry with no cut is stored and shown exactly as today. That is about five entries in six.

What changes:

- About 10,000 entries get cuts: those where a row, a visibility ruling or a variant names less than the whole line.
- In those entries, rows, rulings and variants name part numbers where they now name letters.
- A patch names a part by quoting its words. The merge makes the cut.
- A row or a variant may name the entry's date, time or place (35g).
- `patch-check` applies R22 from the difference between the old line and the new, part by part.

## (b) The data on two real entries

### `cal.1960-06-23.soviet-union`

Stored today (the line and the variant's reading shortened here with "…"; the other fields left out):

```yaml
c: Bucharest, morning. The Soviet delegation hands Peng Zhen's delegation the CPSU Central Committee's letter, dated June 21, in seven parts (the era; war and peace; … unity). The same text had gone to the other parties as a "notification" on June 21, before the Chinese had it, by the Vietnamese, Korean and Albanian delegations' word. A draft communique follows, for discussion on the 24th. The delegation cables the points.
src:
  c: ec205ebb
  rows:
    - 'w.lengxi-shinian-lunzhan-1956-1966 281–283, 285: all'
    - 'w.yang-jisheng-mubei II, 1150: B'
    - 'w.westad-introduction 25: ?'
tags: [polity:prc, name:peng-zhen, vis:only:prc+ussr, 'vis:only:prc+ussr+albania+…@C-D', 'vis:only:prc@E']
variants:
  - {unit: A, witness: w.peng-zhen-nianpu-1902, reads: '… at 3 p.m. on June 23', at: 'IV, 37'}
```

The line has five units, A to E. Yang Jisheng's row names B. One ruling names C and D, another E. The variant names A.

Stored under 35f:

```yaml
c: Bucharest, morning.{1} The Soviet delegation hands … unity).{2} The same text had gone … word. A draft communique follows, for discussion on the 24th.{3} The delegation cables the points.{4}
src:
  c: (the hash of the line above, cuts included)
  rows:
    - 'w.lengxi-shinian-lunzhan-1956-1966 281–283, 285: 1, 2, 3, 4'
    - 'w.yang-jisheng-mubei II, 1150: 2'
    - 'w.westad-introduction 25: ?'
tags: [polity:prc, name:peng-zhen, vis:only:prc+ussr, 'vis:only:prc+ussr+albania+…@3', 'vis:only:prc@4']
variants:
  - {unit: 1, witness: w.peng-zhen-nianpu-1902, reads: '… at 3 p.m. on June 23', at: 'IV, 37'}
```

Four cuts, four parts. Part 1 is unit A. Part 2 is unit B. Part 3 is units C and D, which no row, ruling or variant tells apart. Part 4 is unit E. Wu Lengxi's `all` is written out as the four numbers, so that a sentence added later is not his.

The page, before and after, is the same. It has three footnotes: one after "Bucharest, morning." (Wu Lengxi), one after the sentence on the letter (Wu Lengxi; Yang Jisheng), one at the end (Wu Lengxi, and the `?` rows). There is no mark between parts 3 and 4. Their sources are the same, and only a ruling tells them apart.

### `cal.1960-02-10.cuba`

Stored today:

```yaml
c: 'Alekseyev to Moscow: Guevara, at his home, a few days after Castro''s dinner of Feb. 3, says Cuba will ask Mikoyan for an enormous credit, $500 million the opening bid (Castro and Alekseyev had spoken of $100 million in November); the Kremlin may announce it. "It is very important for Cuba to feel independent of the U.S. and to demonstrate it." Shown to Mikoyan.'
src:
  c: 67d5a62d
  rows:
    - 'w.fursenko-one-hell-of-a 38: all'
    - 'via w.fursenko-one-hell-of-a 38 n.17: all'
tags: [name:guevara-ernesto, name:castro-fidel, name:mikoyan-anastas, vis:only:ussr+cuba, vis:frame:ussr, vis:only:ussr@D]
```

Four units. One ruling names D, "Shown to Mikoyan."

Stored under 35f: two cuts, for that ruling.

```yaml
c: 'Alekseyev to Moscow: Guevara, at his home, … (Castro and Alekseyev had spoken of $100 million in November); the Kremlin may announce it. "It is very important for Cuba to feel independent of the U.S. and to demonstrate it."{1} Shown to Mikoyan.{2}'
src:
  c: (the hash of the line above)
  rows:
    - 'w.fursenko-one-hell-of-a 38: 1, 2'
    - 'via w.fursenko-one-hell-of-a 38 n.17: 1, 2'
tags: [name:guevara-ernesto, name:castro-fidel, name:mikoyan-anastas, vis:only:ussr+cuba, vis:frame:ussr, 'vis:only:ussr@2']
```

The page, before and after, is the same. One source supports the whole line, so there is one block and no mark. The visibility panel treats the four units as it does now. `vis:frame:ussr` is unchanged.

## (c) The cut in the file

**The mark.** A cut is written `{3}`: a brace, the part's number, a brace. It stands directly after the last character of the part (its full stop or semicolon, or the closing quotation mark or bracket after that) and before the space. No entry's line holds a brace today, so the mark cannot be mistaken for prose.

**All or none.** A line has no cut, or it has one at the end of every part, the last part included. So a line with cuts ends in a cut.

**Numbers.** A part's number is unique in its entry. It is never changed and never used again. A new part takes the highest number the entry has ever used, plus one. The numbers need not be in order along the line.

**When a part is cut in two.** Both halves take new numbers. The old number is recorded in the entry: `cut_from: {'5': '2', '6': '2'}` says parts 5 and 6 were cut from part 2. The merge rewrites every row, ruling and variant that named 2 to name 5 and 6. A reference to 2 from outside the entry (an auditor's file, a command) still resolves, to both.

**Loading and writing.** `store.py` takes the cuts out when it loads a calendar entry. In memory `c` is the plain line, and a second field, `cuts`, lists each cut's place in the plain line and its number. Every tool that reads `c` as prose reads what it reads now. When `store.py` writes the entry (`stored_form`), it puts the cuts back into `c` and leaves `cuts` out. The entry's rev, which a patch quotes as its `base`, is taken from the stored form, cuts included.

**What a hand editor sees.** The line with its marks. The rule: leave a mark where it is; if you move the words it follows, move it with them; never delete one. `check` reports a number that a row names and the line lacks.

**What the commands print.** `./bib show ID` prints the entry as the file holds it, marks included, because an `edit` is copied from it. `./bib claims show ID` prints the parts one to a line, each with its number and its sources, and the units' letters beside them as labels only. `./bib find` searches the plain line.

**Two kinds of id (35g, 1).** A part's id is digits: `3`. A claim's id, if the calendar ever takes atomic claims, is `a` and digits: `a3`. Nothing writes a claim's id now. The row grammar, the ruling's `@` and the variant's `unit` accept both forms from the start, so adding claims later changes no grammar.

**A cut with nothing naming it (35g, 3).** Allowed. It changes no page: the footnote compile joins neighbouring parts whose sources are the same.

**What `check` holds.** Marks well formed. Numbers unique in the entry. A line with any cut ends in one. A cut follows closing punctuation and is not inside a link, italics, a quotation or parentheses. No brace in a line other than a mark. Every number that a row, a ruling or a variant names is in the line. `src.c` matches the stored line.

## (d) Patches

**Naming a part by its words.** A patch does not write numbers. It quotes the words (the entry and the page here are made up, to show the form):

```yaml
- cite: {id: cal.1961-03-10.berlin, item: '[[w.beschloss-crisis-years]], 123', on: 'Moscow will send Zorin.'}
```

`on:` holds the part's words, from its first to its last, as the line has them. A long part may be given by its first and last words with three dots between: `on: 'The same text … for discussion on the 24th.'` With no `on:`, the source is for the whole line as it stands when the patch merges.

`primary`, `variant` and `src` take `on:` the same way.

**What `patch-check` requires.** The words are in the line, once (if twice, quote more). They begin at the start of the line, or after a cut, or after a sentence or semicolon clause ends. They end where a sentence or semicolon clause ends. They do not begin or end inside a link, italics, a quotation or parentheses. `patch-check` prints the parts the op will name, and any cut it will make.

**What the merge does.** It finds the words again in the line as it then stands. If they are parts already, the row names them. If not, the merge makes the cut or cuts, gives the new parts numbers, rewrites the rows that named the part it cut, and records `cut_from`. If the entry had no cut, the merge first gives the whole line a cut at its end and rewrites every `all` to that number; so the old sources stay with the old words. If the words are no longer in the line, the op is not applied. The merge records a conflict on the entry (`{kind: anchor, op: …, from: …}`), and `./bib conflicts` lists it.

**Adding words to an entry.** A new op, with no `base` (again made up, to show the form):

```yaml
- add-words: {id: cal.1963-10-01.china-leadership, after: 'Yang Shangkun attends.', words: 'Zhu De and Chen Yi are on the rostrum.', item: '[[w.zhu-de-nianpu-xinbian]], III, 1900'}
```

The merge puts the words after the place named (`after: end` for the end of the line), makes them a part of their own, and gives that part the source. No earlier source is made to support them. Two readers adding to one entry do not conflict.

**An `edit` that changes the line.** It carries `base`, as now. Its new line keeps every cut of the base, each after the words it followed. If the new line has no marks, `patch-check` places each one after the same words where those words are unchanged, and asks the reader to place the rest. Section (e) says what else an `edit` must state.

**A row or a variant that names a field (35g, 2).** An entry's date, time and place are facts with no words in the line. A source for one of them names the field:

```yaml
- cite: {id: cal.1960-06-23.soviet-union, item: '[[w.lengxi-shinian-lunzhan-1956-1966]], 285', on: time}
- variant: {id: cal.1960-06-23.soviet-union, field: time, value: '15:00', witness: w.peng-zhen-nianpu-1902, reads: 'at 3 p.m. on June 23', at: 'IV, 37'}
```

The fields are `date`, `time` (whichever time field the entry has) and `place`. Stored, the row reads `'w.lengxi-… 285: time'`, and the variant has `field:` where another has `unit:`. `check` requires that the entry has the field. A field takes no footnote mark. A source cited only for a field is printed in the entry's first footnote, where the day's label is printed now (`claims.py`, STYLE 7), or in the block where the entry has no footnotes.

**Letters.** A patch written before this change may still name letters, but only with `base:` the entry's rev (section (f), 1).

## (e) R22 from the difference

`patch-check` compares the base line with the new line, part by part. An entry with no cut is one part.

- A part whose words are the same: nothing to state.
- New words, set off as a part of their own with a source (`add-words`, or an `edit` followed in the same patch by an op that names the new words with `on:`): an addition. Free.
- A part whose words changed: the `edit` states `kind: reword` or `kind: correct`.
  - `reword`: `patch-check` requires that no number, no date and no tagged person's name in the part changed. The part's sources stay.
  - `correct`: the patch adds to the note the sentence that names the settling record ("The Papers date it Aug. 26.").
- A part removed: `kind: correct`, with the same sentence.

The reader's brief, a sentence each:

- **R22.** For "A unit already in an entry (a claim of `c`, as the claim map divides it, R34) changes only where a record settles it beyond doubt": "A part already in an entry (the words between two cuts, R34; the whole line where it has no cut) changes only where a record settles it beyond doubt". For "A new unit, from a source cited for it, is added freely (R33a)": "New words, from a source cited for them, are added freely as a part of their own (R33a)". Added at the end: "State which in the edit: `kind: reword` or `kind: correct`."
- **R33**, second case. For "it bears out part: pin it with the parenthetical (and the letters, R34)": "it bears out part: pin it and name the part by its words (`on:`, R34)".
- **R33a.** For "put it into `c`: an `edit` at the patch's head (fresh base) … the claim map renewed (R34), the source cited for the units it bears": "put it into `c` with `add-words`: the words, where they go, and the source, which is then cited for those words alone". For "or where its pinpoint bears on part only": nothing; those words go.
- **R34.** The whole rule: "The claim map. A source is cited for the whole line or for a part of it. Name a part by its words: `cite: {id, item, on: 'first words … last words'}`. The words end where a sentence or a semicolon clause ends. A source for the date, the hour or the place names the field (`on: time`). `./bib claims show ID` prints the parts. Keep the rows other runs wrote. Read the footnotes `./bib claims show ID --inline` makes, in a scratch copy with your patch merged."
- **R35.** For "The map ties it to its units by a `via` row: `via x.1965-02-07.bundy-to-johnson: B, E`": "The map ties it to its parts by a `src` op: `{id, row: 'via x.1965-02-07.bundy-to-johnson', on: '…'}`". For "`./bib stemma ID [--unit B]`": "`./bib stemma ID [--part 3]`". For "the additive `variant` op ({id, unit, witness, reads, at})": "the additive `variant` op ({id, on or field, witness, reads, at})".
- **R41.** For "each reading against its unit, in the witness's words, with its page": "each reading against its part, named by its words, or against the field it disputes (`field: time`, with `value:` the reading in the field's form), in the witness's words, with its page".

CLAUDE.md, the patch ops: `cite: {id, item, on}` for `cite: {id, item, units}`, and `add-words` added to the list.

## (f) Before the conversion, and the conversion

Three passes come first. Each changes some pages, and each lists the entries whose pages change. They are done first so that the conversion itself changes no page.

1. **The letter ops made safe.** Today `cite`, `primary` and `variant` take letters with no `base`. If the line changed after the reader looked, the letters name other words and nothing reports it. From this pass an op that names letters must carry `base:`, and the merge refuses it if the entry's rev differs. No page changes.
2. **The stale maps.** 1,048 readers' maps were made against a line that has since changed. Their entries are shown as one block. For each, find in git history the line whose hash the map records. Match the old units to the present ones by their text. A row keeps a unit that is unchanged. A row keeps a unit whose words changed, and the entry is listed for a reader. A row does not take a unit that is wholly new; so an `all` becomes the letters of the old units. Write the new hash. Entries that regain footnotes are listed.
3. **A work's page and its note, one source.** A row for a page (`w.x 88`) and a row for a note on that page (`via w.x 88 n.32`) are printed as one citation. Today they still count as two sources when the build compares neighbouring units, and so they can put a mark between two units. From this pass they count as one for that comparison. The registry keeps the two rows apart. By one measure 489 entries lose their only mark; the pass lists them.

**The conversion.** One year at a time, with no reader and no merge running.

- It touches only an entry in which a stored row, a visibility ruling or a variant names letters short of all.
- It compares each pair of neighbouring units. Where the rows, rulings or variants that name the two units differ, it writes a cut between them. It writes a cut at the end of the line.
- It numbers the parts 1, 2, 3 in order.
- It rewrites letters to numbers in the rows, the rulings (`@C-D` to `@3`; several numbers joined by a dot, `@3.4`) and the variants. In a converted entry it writes `all` out as the numbers.
- It writes the new hash.

**Two proofs, for each year.**

1. Unit by unit, every entry has the same sources, the same rulings and the same variants before and after.
2. The year's pages are the same, byte for byte.

An entry that fails either proof is not converted. It is listed.

## (g) Display questions, kept apart from all of the above

None of these is part of 35f. Each changes what the page prints. Each is to be shown in a preview built from the site's own HTML and CSS, with every departure listed, before it is merged. The default I would take is given for each.

1. **Sources that every footnote of an entry shares.** Today, where three or more are shared, the build drops the footnotes and shows one block (STYLE 8, "block"). 516 entries are in that state; their part-by-part sources are not on the page. The choices: (i) "block", as now; (ii) "first": the shared sources in note 1, and later notes opening "Sources cited *supra* note 1" (as coded, this also claims note 1's own sources for the later notes, and would need mending); (iii) the shared sources printed once, unnumbered, ahead of the numbered notes, as an entry with no footnotes prints its block now; the numbered notes then hold only what is particular to their passage, and a passage with nothing particular has no mark. Default: (iii). Until the owner has seen the preview, "block" stays.
2. **A footnote the same as an earlier one of its entry.** 856 entries print one. Default: "*See supra* note 1." If 1 (iii) is taken, most of these go.
3. **The `?` rows.** 19,941 rows, in 13,778 entries, are sources whose part no reader has placed. Today they are printed in the entry's last footnote, as if they supported the last passage. Default: print them after the numbered footnotes, each with the parenthetical it has in the note. Give the placing of them to the pass that goes back over the notes.
4. **Variants in footnotes.** Today no page prints a variant; the reader sees the note's "Check: … gives …". Default: no change now. A preview of the variant in its part's footnote, after "*But see*", for the owner to judge.
5. **Marks and footnotes when the visibility panel hides text.** (i) A mark is inside the last unit of its passage. If that unit is hidden and earlier units of the passage are shown, the mark is hidden too. Default: the script moves the mark to the passage's last shown unit. (ii) When every unit of a passage is hidden, its footnote is still shown below, numbered, with no mark in the text. Default: hide that footnote; grey it when the passage is greyed. (iii) The EPUB has no panel and shows every unit in full. Default: leave it.

One more, a change to the build and not to the design: marks and visibility spans are placed by rendering each unit alone and searching for it in the rendered line. Where the search fails, the entry is shown as a block. Default: after the conversion, pass a private mark through the renderer at each unit's end and place on that. Entries that regain footnotes are listed.

## (h) The order of work

Each step has its test and what can go wrong.

1. **Make the letter ops safe** (section (f), 1). Test: a golden patch whose `base` is out of date is refused. Can go wrong: nothing waits on letters; the eight NYT patches name none.
2. **Rebase the stale maps** (section (f), 2). Test: the count of stale maps is zero or a short list; the entries whose pages change are listed. Can go wrong: the clone is shallow and history does not reach the old line (fetch the full history first); a line was changed twice and the hash matches no commit (list it; a reader maps it again).
3. **A page and its note as one source** (section (f), 3). Test: a unit test of the comparison; the page difference is exactly the listed entries. Can go wrong: a note that supports a different unit from its page loses its mark on the page; the registry still holds the difference.
4. **`store.py`: cuts out on load, back on write; `cuts` and `cut_from`; the `check` rules of section (c).** Test: load and write every calendar file and get the same bytes; no built page holds a brace mark; revs unchanged for entries without cuts. Can go wrong: a tool that sets `c` directly drops the cuts (`merge.py`'s combine, `importer.py`, `works.py` set it today); give them one function to set the line and its cuts together.
5. **`claims.py`: a row's target as part numbers and fields; numbers turned into units for everything downstream.** Test: for an entry and its converted copy, `resolve()` gives the same sources for every unit. `footnotes.py` needs no change.
6. **`vis.py`, `witnesses.py`, `addops.py`, `cli.py`:** the ruling's `@` takes numbers; a variant's `unit` takes a number, or the variant has `field`; `claims show` prints parts; the stemma takes `--part`. Test: the visibility goldens unchanged on a converted fixture.
7. **The converter, dry run, on 1960.** Test: the two proofs of section (f). Shown to the owner: the counts, the list of entries not converted, four entries before and after.
8. **The patch ops** (section (d)): `on:`, the merge's cut, `cut_from`, `add-words`, an `edit` keeping its cuts, the two kinds of edit, the anchor conflict. Test: golden patches for each; two readers adding to one entry merge without conflict; an op whose words are gone becomes a conflict. Can go wrong: two merges at once (merges have no lock; one at a time, as now).
9. **The briefs**: R22, R33, R33a, R34, R35, R41 as in section (e); CLAUDE.md's patch ops; `notes/guide/brief.md` and `changing.md`. Readers and auditors may start again after this step.
10. **Convert 1960 for real, then each later year**, each with its two proofs. Then `check` refuses letters in a stored row, ruling or variant.
11. **The display previews** of section (g), each on its own.
12. **The trial of atomic claims** (35g): February 1960, written to a side file, after the first converted year.

What can go wrong across the whole:

- A hand edit deletes or misplaces a cut. `check` reports a missing number. It cannot report a cut moved to the wrong words; the stale hash reports that the line changed.
- A reader rewrites a line and moves words from one part into another. `patch-check` shows each changed part with its sources and asks for the kind of edit. A reader can still answer wrongly; the audit reads those answers.
- Braces come into use in prose. `check` forbids them in a calendar line.
- The rule for finding units is changed later. No stored number moves. A mark that the build computes from units (a link in the line; the day's label) can move, as it can today.
