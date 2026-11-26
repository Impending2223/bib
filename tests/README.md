# The tests

A net under the code (`tools/`), so that a change, or a whole section rewritten, can be shown to leave the
site and the data as they were. They test the code, not the data: `./bib check` tests the data.

## Running them

```
pip install -r requirements.txt -r requirements-dev.txt     # once (a venv is fine: python3 -m venv .venv)
python -m pytest -q -m "not slow"     # the fast suite, about a minute; CI runs it before check on every push
python -m pytest -q -m slow           # the slow ones, over the whole of the real data: several minutes
python -m pytest -q tests/unit        # one group
```

## What each kind guards

- **`fixture/`**: a frozen slice of the real data in the repository's layout: the calendar's threads and two
  months (April and August 1961), the persons, Executive units, witnesses and works cards they need, and the
  small source files. Written by `make_fixture.py`; regenerated only on purpose (below). The tools are pointed
  at it by `BIB_ROOT` (`BIB_ROOT=tests/fixture ./bib check`). Its `check` has errors (links to months it does
  not hold); they are part of the golden, not to be fixed.
- **`golden/`**: what the tools print and write on the fixture, compared with `golden/expected/`: `check`'s
  output; the whole build (every file's checksum); 25 queries (`find`, `show`, `works`, `outline`, `status`,
  `claims`, `stemma`, `executive who`, ...); and `patch-check` with `merge --auto` on eight small patches in
  `golden/patches/` (an add; an edit; a stale base found in git; a conflict; the additive ops; a deferred op; a
  place; a duplicate), each its transcript and the files it changed. They catch any change in what the tools
  do, wanted or not.
- **`unit/`**: tables of inputs and outputs for the pure functions (markup, dateline, footnotes, claims, notemerge,
  places, store, merge, addops, resultform), and for the map of China (`test_cnmap.py`: the figure and its data on
  a small gazetteer of the test's own, `check`'s rules for the map's files, the one client, and the reading of the
  record of the 1964 counties in `tools/cnmap/counties.py`), and for the two maps wherever they stand (`test_maps.py`:
  the span and its fields, the entries' files, a map in a calendar page and on a thread's page, the client's reading of
  a typed date, run in node where node is installed, and the table of `tools/cnmap/roc.py`). Each row pins what the function returned when the table was
  written. Known bugs are marked `xfail` with the reason; a fix makes them pass (then drop the mark).
- **`property/`**: laws for any input (hypothesis): a three-way merge where both sides agree; an entry's rev
  whatever its key order; the emitter's round trip; an additive op twice equals once. The slow ones read every
  file of `lists/` and `works/`: written by the store's emitter and read back, the same data; and libyaml's
  fast loader, which the store uses when PyYAML has it, reads each as the pure-Python loader does, types and all
  (the guard on the store's loader: run it, `-m slow -k c_loader`, after any change to the loader or PyYAML).

## When a golden test fails

Read the diff it prints. If the change is a regression, fix the code. If it is meant, rewrite the goldens and
read what changed before committing them with the change:

```
python -m pytest -q tests/golden --update-goldens
git diff tests/golden/expected
```

For a page's differences on the fixture, not just its checksum: `python3 tests/ab.py HEAD . --data tests/fixture`.

To regenerate the fixture (a new month, a source the build has come to need): `python3 tests/make_fixture.py`,
then `--update-goldens`, and say why in the commit.

## A/B: proving a rewrite byte-identical on the full data

```
python3 tests/ab.py main HEAD                        # check and the whole build, both sides: about 40 minutes
python3 tests/ab.py main HEAD --build congress       # check and one page
python3 tests/ab.py HEAD . --no-build                # the working tree's code against HEAD's, check only
python3 tests/ab.py HEAD~1 HEAD --own-data           # each side its own data too
```

Each side's code is taken from git into a temporary tree; the same data (this checkout's, or `--data DIR`)
is linked into both, so only the code differs. Both run `check` and `build --force`; the outputs and every file
under `build/` are compared byte for byte (a feed's time of writing is blanked). It prints `IDENTICAL`, or each
differing file with its first differing lines, and exits 1. The full data's goldens are not stored: every
merge of data would make them stale; `ab.py` compares two versions of the code on today's data instead.
Run the long comparisons in the background; set `TMPDIR` to put the trees elsewhere.
