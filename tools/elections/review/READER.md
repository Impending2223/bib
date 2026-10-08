# Reading House and Senate returns by eye

For a reader (a person or an agent) given sheets or pages by `tools/elections/review.py`. You are
transcribing vote figures from page scans of the Clerk of the House's *Statistics of the Presidential and
Congressional Election*. The OCR could not settle these races, so every figure must come from your own
reading of the image. A digit wrong is worse than a race skipped. Read every figure digit by digit;
commas separate thousands ("2, 927, 693" is 2927693). If a digit is illegible, say so in the note and
give your best reading.

## What you are given

- **Sheets** (`s_NN.png`): up to six crops, each under a label line,
  `ST SEAT  p.PAGE: Wikipedia's names and percentages`. SEAT is the district (0 = at large) or
  `Sen1`/`Sen2`/`Sen3` (the Senate class). A crop often shows neighbouring races; transcribe only the
  one the label names. Wikipedia's names and percentages are a guide to which lines belong to the race
  and a check on your figures, not a source: record the Clerk's figures even where Wikipedia differs.
- **Page thirds** (`pg_NN_a.png`, `_b`, `_c`: top, middle, bottom of page NN, overlapping), for a State
  read whole: transcribe every race on its pages.
- **Full pages** are `CACHE/YEAR/p-NN.png` (about 2550 x 3300). Do not open them whole; crop what you need
  with a short PIL script (`Image.open(p).crop((x0, y0, x1, y1)).save(out)`) into your own scratch
  directory, with your own file prefix, and Read that. Page numbers are these file numbers; the printed
  page number is one less. Do not run OCR yourself.

## What you write

A YAML file at the path you are given, in the readings schema (`tools/elections/read.py`):

```yaml
races:
  h CA 5:                      # chamber (h, s), State, seat: the district (0 at large) or Senate class
    cands:
    - [John F. Shelley, 'Democrat, Republican', 99171]       # name as printed, party as printed, votes
    - [Scattering, null, 8]
  s NY 3:
    cands:
    - [Jacob K. Javits, 'Republican, Liberal', 3269772, [[Republican, 2810836], [Liberal, 458936]]]
    - [Paul O'Dwyer, Democrat, 2150695]
    printed: >-
      What did not add up, and why this figure: "The race page prints 74,627; the recapitulation's
      84,627 is the figure its totals add up with."
```

- Every line of the race in printed order: minor candidates, write-ins, `Scattering`. Parties exactly as
  printed, several joined by ", " where the Clerk lists several (California's cross-filing).
- A candidate on several party lines (New York): name, the parties joined, the total, then the lines.
  Where the race page prints only the combined figure, take the lines from the recapitulation.
- A figure printed as a footnote mark ("(1)": unopposed, not tabulated): votes `null`, and a note.
- Leave out "Blank and void" lines. Quote a value with ": " or a leading "'" in single quotes.
- Check every race against the State's recapitulation table (its district or Senate row, and the column
  totals if printed). Where the race page and the recapitulation differ, record the figure with which
  the recapitulation's totals add up, and say so in `printed:` (shown with the race; also for a misprinted total,
  transposed figures, a party printed one way and counted another). Anything else goes in `note:`, which is kept in
  the file and not shown.

Reply with the file path, the races read, and anything that did not add up.
