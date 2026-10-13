# bib

The 1968 series: a calendar, a bibliography and a set of reference tables for American politics and policy, 1961–74,
and the war in Vietnam, 1945–75. Kept here as data; built and published to https://impending2223.github.io/bib/ on
every push to `main`.

## The site

| page | what it holds |
|------|---------------|
| [Calendar I](https://impending2223.github.io/bib/cal.html), [Calendar II](https://impending2223.github.io/bib/cal63.html) | The executive and legislative record, day by day, Jan. 1961–Jan. 10, 1966 (I to Jan. 2, 1963; II from the 88th Congress's opening), with the presidential primaries of 1960–76. Each entry: what happened, the primary record linked, the event's bibliography, the persons named. Each day: the Public Papers, FRUS and White House recordings of that date, the Sunday interview programs. Each month: the economic indicators as first reported and as revised, money rates, Gallup's approval. 1,442 entries in 69 threads. |
| [Works](https://impending2223.github.io/bib/works.html) | The bibliography, A to Z: every work the series cites, one entry a work (2,636), with where each is cited. |
| [Names](https://impending2223.github.io/bib/names.html) | An entry for each person (12,633): offices and elections with their sources, publications and papers, and the FRUS documents, presidential documents and recordings that name the person. |
| [Congress](https://impending2223.github.io/bib/congress.html) | Each Congress at its opening, 87th–93rd: party bars, House and Senate maps, every member; every general election, 1958–74, race by race; the special elections, 85th–93rd. |
| [Executive](https://impending2223.github.io/bib/executive.html) | The Executive Branch at each inauguration and succession, 1953–74: every office, the law that governs it, every holder. |
| [The reader](https://impending2223.github.io/bib/) | All of it on one page, cross-referenced. |

### The themed lists (being retired)

Eight earlier lists, each in three parts: portrayals (I), sources (II), names (III). Their works are now in Works,
where the calendar's citations point; Parts I and II are to give way to the A–Z list. Part III stays, as the source of
the Names entries.

| list | cited as |
|------|----------|
| [Kennedy and Johnson administrations, 1961–69](https://impending2223.github.io/bib/kja.html) | K–J Adm. |
| [Congress, the nation, and the states, 1961–69](https://impending2223.github.io/bib/kjc.html) | K–J Cong. |
| [The Republican opposition, 1961–69](https://impending2223.github.io/bib/opp.html) | Opp. |
| [The 1968 campaign](https://impending2223.github.io/bib/l68.html) | 1968 |
| [Nixon and his administration, 1969–74](https://impending2223.github.io/bib/adm.html) | Adm. |
| [Congress, the nation, and the states, 1969–74](https://impending2223.github.io/bib/cong.html) | Cong. |
| [Watergate, 1971–74](https://impending2223.github.io/bib/wg.html) | Wg. |
| [Vietnam and the American war, 1945–75](https://impending2223.github.io/bib/vn.html) | Viet. |

The claude.ai artifacts named in `series.yaml` are frozen copies of Oct. 1, 2026, and are no longer updated.

## The repository

| path | holds |
|------|-------|
| `lists/cal/` | the calendar: a file a month (`apr63.yaml`), the threads (`th.yaml`), the prologue and the primary seasons |
| `works/` | the works catalogue: a card a work; every list and calendar entry points to its card |
| `lists/<key>/` | the themed lists, a file a section (`lists/kja/II.D.yaml`); Part III is the series' persons |
| `congress/` | each Congress at its opening, its changes in membership and special elections, and the district shapes |
| `elections/` | the general elections, 1956–74 (generated), the readings by eye, the presidential primaries, the hand-kept facts |
| `executive/` | the Executive Branch, a file a department or agency: its offices, their law, their holders |
| `daybook/` | the Public Papers, FRUS and White House recordings by date (generated), the Sunday programs, the abstracts |
| `indicators/` | the economic series, a file a series: first reported, released, revised |
| `sources/` | the indexes the build reads (the Biographical Directory, FRUS's lists of persons, POCOM, the Public Papers' names, statute links) and the hand-kept registers (State returns, name forms, matches) |
| `notes/` | the owner's brief, the thread framings, the calendar audit, the works inventory, the briefs for fact-checking and the Executive roster |
| `templates/` | the page templates and the shared roster styles |
| `tools/bib/` | the code behind `./bib`; `tools/*/` the scripts that made or refresh the data (most run once; their docstrings say) |
| `inbox/` | patch files waiting to be merged |
| `build/` | the generated pages (git-ignored) |

## Working on it

Every entry is a small YAML record with a permanent id. Find what you need, edit that, check, build:

```
./bib status                         counts, conflicts, inbox
./bib find bay of pigs               entries holding all the words
./bib show ID                        an entry, its tags, what links to it
./bib works list -t in:kja --sort year     the works answering a query
./bib works show w.beschloss-crisis-years  a work and every place it is cited
./bib check                          must end "0 errors"
./bib build                          every page (or one: ./bib build cal | works | names | congress | executive)
./bib links                          links between pages whose anchors are missing
```

Changes from several hands merge entry by entry: patch files (`./bib merge inbox/<file>`) and git branches (run
`./bib setup` once) both merge field by field; a disagreement is recorded in the entry as a conflict to settle, never
lost. A work cited twice over is folded with `./bib works combine KEEP DROP`, an entry with `./bib combine`.

A push to `main` runs `./bib check` and `./bib build` (`.github/workflows/pages.yml`) and publishes the result; if the
check fails, the site stays as it was.

Requires Python 3 and PyYAML. `CLAUDE.md` is the working manual: the owner's brief, the house style, and the rules of
every page.
