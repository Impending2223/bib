# Reading the vote for presidential electors by eye

For a reader given States and pages by `tools/elections/review.py` (`left` lists them, `locate` finds a
State's pages). Under each State the Clerk prints "For Presidential Electors": one line per slate, the
party as printed (Democratic, Republican, Liberal, American Independent, "Unpledged", "Courage" ...) and
the vote (the highest vote for any elector of the slate), sometimes Scattering or "Blank and void". The
State's recapitulation repeats the figures in a row "Presidential electors", with a total.

A digit wrong is worse than a State skipped. Full pages are `CACHE/YEAR/p-NN.png` (about 2550 x 3300):
crop what you need with a short PIL script into your own scratch directory, with your own file prefix,
and Read that. Do not run OCR yourself. Page numbers are file numbers (the printed page is one less).

## What you write

A YAML file at the path you are given, in the readings schema (`tools/elections/read.py`):

```yaml
president:
  NY:
    slates:
    - [Democratic, 3423909]      # the party as printed, and its vote, in printed order
    - [Liberal, 406176]          # each line separately, not a bracketed total
    - [Republican, 3446419]
    - [Scattering, 256]
    printed: >-
      The recapitulation's total counts 88,996 blank and void ballots; they are left out here.
```

- Every slate line, in printed order; `[Scattering, n]` and `[Write-in, n]` as printed. Leave out
  "Blank and void" (say so in the note).
- Check each figure and the total against the recapitulation's "Presidential electors" row. Where they
  differ, record the figure with which the total adds up, and say so in `printed:` (shown with the State's row;
  `note:` for anything else, kept in the file).
- Where the Clerk prints no vote (the District of Columbia, 1964), say so; the figures then come from
  elsewhere with a `source:` line.

Reply with the file path, the States read, and anything that did not add up.
