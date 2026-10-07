# bib

The 1968 series: eight linked working bibliographies and a calendar for
American politics from 1961 to 1974, and a ninth bibliography for the war in
Vietnam. Kept here as data, and published to
https://impending2223.github.io/bib/ on every push to `main`
(`.github/workflows/pages.yml`).

| list | page |
|------|------|
| All of them in one reader, with live cross-references | https://impending2223.github.io/bib/ |
| Kennedy and Johnson administrations, 1961–69 (K–J Adm.) | https://impending2223.github.io/bib/kja.html |
| Congress, the nation, and the states, 1961–69 (K–J Cong.) | https://impending2223.github.io/bib/kjc.html |
| The Republican opposition, 1961–69 (Opp.) | https://impending2223.github.io/bib/opp.html |
| Calendar, January 1961–January 1963: the 87th Congress (Cal.) | https://impending2223.github.io/bib/cal.html |
| The 1968 campaign (1968) | https://impending2223.github.io/bib/l68.html |
| Nixon and his administration, 1969–74 (Adm.) | https://impending2223.github.io/bib/adm.html |
| Congress, the nation, and the states, 1969–74 (Cong.) | https://impending2223.github.io/bib/cong.html |
| Watergate, 1971–74 (Wg.) | https://impending2223.github.io/bib/wg.html |
| Vietnam and the American war, 1945–75 (Viet.) | https://impending2223.github.io/bib/vn.html |
| Each Congress at its opening, 87th–93rd: party bars, House and Senate maps, every member | https://impending2223.github.io/bib/congress.html |
| The Executive Branch at each inauguration, 1953–74: every office, the law that governs it, every holder | https://impending2223.github.io/bib/executive.html |
| Lives: a name entry for each person, the life with its sources, the person's papers and works, and the FRUS and presidential documents that name the person | https://impending2223.github.io/bib/lives.html |

The claude.ai artifacts named in `series.yaml` are copies as of Oct. 1, 2026,
before the style revision. They are no longer updated.

## How it is kept

- Every entry is a small YAML record with a permanent id, in a file per
  section (`lists/kja/II.D.yaml`, `lists/cal/apr.yaml`). An editor, human or
  Claude, opens only the section it is changing.
- `./bib find`, `show`, `works`, and `outline` locate entries across all nine
  lists without reading them. Entries carry stored tags (`topic:berlin`, `todo`)
  and derived ones the tools compute (`check`, `person`, `thread:cuba`,
  `in:opp`).
- `./bib check` catches broken links, calendar dates outside their month,
  threads that don't exist, section references that point nowhere, and books
  cited under the wrong section.
- Changes from several hands merge entry by entry: patch files (`./bib merge`)
  and git branches (`./bib setup`) both use a three-way, field-by-field merge.
  Duplicates are flagged and can be folded together (`./bib combine`).
  Disagreements are recorded in the entry as conflicts to settle, never lost.
- `congress/` holds each Congress at its opening, 87th–93rd: the members by
  state and district or class, and the district and state shapes. The build
  draws them on `congress.html`, and in the calendar at each opening it covers.
- `executive/` holds the Executive Branch, Jan. 20, 1953 to Aug. 31, 1974: each department and agency, its
  offices in order under the head, the law that creates and governs each (linked to the Statutes at Large
  and the U.S. Code of the period), and every holder with the dates of nomination, confirmation, commission,
  taking office, and leaving. The build draws it on `executive.html`, a roster at each inauguration and
  succession, and in the calendar at the term it covers.
- `./bib build` regenerates every page, including the compiled reader's links,
  "Elsewhere" lines, and names index. A push to `main` runs `check` and
  `build` and publishes the result; if `check` fails, the site stays as it was.

Requires Python 3 and PyYAML. Start with `./bib status`. CLAUDE.md is the
working manual.
