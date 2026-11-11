# Changing things

Moved word for word from CLAUDE.md, Nov. 10, 2026 (the owner: "I approve both"); CLAUDE.md keeps the core and an index of these guides.

**Directly** (you are working in this repo): edit the section file, then

```
./bib new-id cal 1961-10-27 berlin-and-vienna   # an unused id
./bib check            # must end "0 errors"; deal with new warnings
./bib build            # build/<key>.html and build/series.html (a page alone: ./bib build congress | names | works | cal ...)
./bib links            # links between the built pages whose anchors are missing
```

Every YAML file is parsed once a run, and the parse kept in `.cache/yaml` (git-ignored) by path, modification time and size, so a later run parses only what changed: `check` takes about 8 s, a full build about 35 s, a page 15-20 s. A link to another page's anchor that a later build lost lands on the page's top; `./bib links` lists them.

**By patch**: when another session or a person will merge your work, or you cannot touch the repo. Write `inbox/<date>-<name>.yaml` and run `./bib merge inbox/<file> [--dry-run] [--archive]`:

```yaml
patch: berlin-autumn                  # name, shown in conflict records
by: who wrote it
ops:
  - add:                              # placed by date (calendar), by subject
      entry: {id: ..., when: ..., date: ..., thread: ..., c: ..., n: ...}
      section: II.D                   #   ("Alphabetical"), or by year; or say
      after: kja.wyden-bay-of-pigs    #   section/after
  - edit:
      id: cal.1961-08-13.berlin-and-vienna
      base: 7047fc46                  # the rev ./bib show printed when you read it
      set: {n: 'New note …'}
      unset: [r]
  - tag:     {id: ..., add: [topic:berlin], remove: [todo]}
  - move:    {id: ..., section: II.E, after: ...}
  - delete:  {id: ..., base: ...}
  - combine: {keep: ID, drop: ID}
```

Always give `edit` and `delete` a `base`. With it, the merge is three-way: fields only you changed apply, fields only others changed stay, and a field both changed becomes a conflict. Without it, your values simply overwrite.

Additive ops (the owner's request, Oct. 30, 2026: "a performant, compute-economizing solution" for parallel readers; `notes/extensions/memos/volume.md`, §6; `tools/bib/addops.py`, its STYLE): what only adds to an entry needs no `base` and merges in either order: `cite: {id, item: '[[w.card]], 123 (the vote)', units: 'A, C'}` (the work out of "To check:" into the run of works read, its claim-map row), `primary: {id, text, units}`, `to-check: {id, add}`, `check: {id, text}`, `src: {id, rows}`, `names: {id, add, tags}`, `also: {id, add}`, `variant: {id, unit, witness, reads, at}`, `follows: {id, add}`. Within a patch the adds go first. A new entry is claimed first in the ledger, `inbox/new-entries.tsv` (`./bib ledger add DATE THREAD ID "words" PATCH`; `./bib ledger find DATE [--until DATE] [--thread T]` the day's entries, tree and ledger; `tools/bib/ledger.py`), and an additive op on a claimed id not yet in the tree waits in `inbox/deferred.yaml` until it lands. `./bib patch-check PATCH [--legacy]` holds a patch to the rules before it is handed in (`tools/bib/patchcheck.py`): the patch applied in memory, the entries it adds, edits or adds to held to `check`'s own rules for an entry, by `check`'s functions (`entry_problems`: `when` against `date`, `when_matches_date`; `thread`, `also` and `to` a thread's slug, not an alias; every `[[id]]` an entry; the date in the section it lands in, January 1966's two among them), the witnesses' (`witnesses.problems`: a `via x.` row's witness reached from an item of the note) and the claim maps' (`claims.problems`: a `src` row naming what the note prints), an error the tree already had not the patch's, each message saying the fix (patchcheck STYLE 8), so a patch it passes passes `check` once merged; `./bib merge --auto PATCH...` is the rolling merge: patch-check (`--legacy` for a patch written before the ledger), apply, the deferred ops, the conflicts on `n` that `notemerge` joins with no problem and those on `src` over the same `c` joined (both sides kept), the ledger pruned, the patch archived; it stops at a patch with errors and prints the conflicts left and a sample, one changed entry in ten, to read. `./bib plan-readers CARD...` groups works by the entries they already share, a group a reader (`tools/bib/planreaders.py`).

**Git**: run `./bib setup` once per clone. Section files then merge entry by entry (`.gitattributes`): both sides' new entries are kept in order, and a field changed on both sides becomes a conflict record instead of `<<<<<<<` markers.
