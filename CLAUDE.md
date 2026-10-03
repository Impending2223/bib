# The 1968 series: how to work on it

Eight linked bibliographies and a calendar for 1961–1974, and a ninth on
Vietnam, kept as data and rendered to HTML. **Do not read the whole series,
and never read `build/`.** Find the few entries you need with `./bib`, edit
those, check, build.

## The brief (read before adding anything)

The owner's standing instructions.

**Prose.** "Compact. Plain. Compressed. Springs and Autumns, but without the
subtle words." Record what happened, not what it meant. No praise, blame,
irony, or color; no "for Moscow's benefit," "a good midterm," "the movement
reads it as a defeat." Short declaratives and fragments. Drop articles and
verbs where the line still reads. Match the original lists, not your own
register: read a few entries of the section you are adding to before writing.

**The calendar.** In the owner's words: "a calendar of executive and
legislative events, and any other events that left a trace, or should have
left a trace, on the political and policy histories of the Kennedy and
Johnson Administrations, their Congresses, or those of their members. ... at
least a month-by-month granularity. ... a brief statement for each calendar
entry and, where events span multiple calendar entries, for each thread. ...
The purpose of the statements for calendar entries is not a narrative, but a
memory aid and a bibliographic record, or a set of bibliographic pointers.
... I want the calendar to supply a bibliography for each event, if not each
entry. (That is, you might have several entries for the Vienna Summit or the
Berlin Crisis, but you might only have a full bibliography entry for the
first.) At the very least, I want the calendar entries to point to the
relevant material elsewhere in the bibliography. Names, events."

So every calendar entry has:
- `c`: what happened, in one to three clipped sentences. Who, what, the number.
- `n`: the pointers. The source for this event (message, case, statute, FRUS
  volume, a book by short title with list and section); `See [[id]]` back to
  the thread's first entry, which carries the full bibliography; and
  `Names: …` with the list and Part III section of every person in `c`.

Thread scopes in `th.yaml` are a list of the thread's stations, not a summary.

**Bibliography notes.** One or two fragments: what the book is, whose voice,
what to read it for. "Interviews with nearly everyone, Bissell included."
"Read the Washington chapters." Not reviews. Most entries need no note: when
the title does the work, leave it bare. No awards, no "start here," no side
labels ("defense," "revisionist," "from the left"); state a thesis or a
source's provenance the same way whichever side it is on.

Before and after:

```
no:  c: Gilpatric at Hot Springs, Virginia, to the Business Council. The American
        second strike is at least as large as any Soviet first strike. The missile
        gap reversed, in public, for Moscow's benefit.
yes: c: Gilpatric to the Business Council at Hot Springs. The American second
        strike at least equal to any Soviet first strike. The missile gap reversed.
     n: Ball, *Politics and Force Levels*; Kaplan, *Wizards of Armageddon* (K–J Adm.
        II.D). See [[cal.1961-02-06.defense]]. Names: Gilpatric (K–J Adm. III.F).
```

## Layout

```
series.yaml               the lists: key, abbreviation, old artifact URL
lists/<key>/list.yaml     a list's title, intro paragraphs, and outline (sections → files)
lists/<key>/<file>.yaml   one section's entries, in display order (II.D.yaml, apr.yaml)
inbox/                    patch files waiting to be merged
congress/<NN>.yaml        each Congress at its opening (87–93): House by state and
                          district (0 = at large), Senate by state and class
congress/geo.json         district and state shapes, projected and simplified
build/                    generated pages (git-ignored)
tools/bib/                the code behind ./bib
tools/congress/           one-time scripts that made congress/ (see below)
```

| key  | cited as  | list                                         |
|------|-----------|----------------------------------------------|
| kja  | K–J Adm.  | Kennedy and Johnson administrations, 1961–69 |
| kjc  | K–J Cong. | Congress, the nation, and the states, 1961–69 |
| opp  | Opp.      | The Republican opposition, 1961–69           |
| cal  | Cal.      | Calendar, Jan. 1961–Jan. 3, 1963 (87th Congress) |
| l68  | 1968      | The 1968 campaign ("the 1968 list")          |
| adm  | Adm.      | Nixon and his administration, 1969–74        |
| cong | Cong.     | Congress, the nation, and the states, 1969–74 |
| wg   | Wg.       | Watergate, 1971–74                           |
| vn   | Viet.     | Vietnam and the American war, 1945–75        |

Parts: I portrayals, II sources, III names. A reference like "K–J Adm. II.D"
is `lists/kja/II.D.yaml`. The calendar's files are named by month: `apr.yaml`
for 1961, `apr62.yaml` for 1962 (the last, `dec62.yaml`, runs to Jan. 3, 1963),
plus `th.yaml` (threads) and `pro.yaml` (prologue). Its sections are numbered
straight through, I to XXVI.

## Finding things (start here)

```
./bib status                          counts, conflicts, inbox, pages to republish
./bib outline kja                     sections → files → entry counts (calendar: threads too)
./bib find bay of pigs                every entry containing all the words
./bib find -l cal --thread cuba       one calendar thread
./bib find -l cal --since 1961-08 --until 1961-08
./bib find -t check -l cal            entries with a "Check" to verify
./bib find -t person -t in:cal -l kja tags combine (AND)
./bib show ID [ID...]                 full entry + rev + tags + what links to it
./bib works Parting the Waters        every list that holds or cites a title or person
```

`find` prints `id`, then `file:line` and a one-line summary. Open the file
at that line to edit, reading only that section.

## Entries

```yaml
- id: kja.beschloss-crisis-years       # permanent; never rename or reuse
  s: 'Kennedy, Robert F.'              # optional bold subject line (people, memoir subjects)
  c: Michael R. Beschloss, *The Crisis Years* (1991)   # citation; a list for several works
  r: Attorney General, 1961–64         # people (Part III): the role
  n: The note. Free prose.             # optional
  tags: [topic:berlin, todo]           # optional, stored tags
  aliases: [kja.old-id]                # ids folded into this one by ./bib combine
```

Calendar entries have no `s` (the build makes "Apr. 15–19 (Cuba)"):

```yaml
- id: cal.1961-04-15.cuba              # cal.<date>.<thread>, -2 if taken
  when: Apr. 15–19                     # shown as written
  date: '1961-04-15'                   # sort and range key; '1961-02' for month-only entries
  thread: cuba                         # primary thread (slug of a cal.thread.* entry)
  also: [space]                        # other threads it belongs to
  c: What happened.
  n: Sources. See [[cal.1961-02-20.school-aid]].
```

The thread index (Part I of the calendar) is generated from `thread` and
`also`; never write dates into `th.yaml`. A new thread is a new entry in
`th.yaml` (`id: cal.thread.<slug>`, `s:` name, `c:` one-line scope).

### Markup inside text

- `*Title*`: italics. `[text](https://…)`: an outside link.
- `[[id]]`: a link to another entry, shown as its label (a calendar date).
  `[[id|text]]` shows "text". Use these for "See …" in calendar notes, so a
  corrected date updates every reference. The build adds the year when the
  date linked to falls in a different year from the entry linking to it
  ("Dec. 21–22, 1961"); don't write the year in.
- Cross-list references stay plain prose ("(K–J Adm. II.D)", "Also Opp.",
  "Names: Heller, Tobin (K–J Adm. III.H)"). The build links them and `check`
  verifies the sections exist and that a cited title is in the cited section.
- YAML: quote a value in single quotes when it holds `: ` or ` #` or starts with
  `*`, `[`, `'` or `"`; double an apostrophe inside: `'Kennedy''s'`. This goes
  for the paragraphs in `list.yaml` too; `check` reports one that loaded as a
  mapping.
- "87th Cong." and the like are Congresses, not the list: the reference reader
  skips an abbreviation that follows an ordinal number.

### House style (keep it)

Short declarative sentences. Books already in a list are cited by short title
with list and section; works found only here are cited in full. "Check" marks
a detail to verify. In the calendar the first entry of each thread carries its
bibliography and later ones point back with `See [[id]]`. Bibliography sections
are chronological by publication unless their intro says "Alphabetical".

## Changing things

**Directly** (you are working in this repo): edit the section file, then

```
./bib new-id cal 1961-10-27 berlin-and-vienna   # an unused id
./bib check            # must end "0 errors"; deal with new warnings
./bib build            # build/<key>.html and build/series.html
```

**By patch**: when another session or a person will merge your work, or you
cannot touch the repo. Write `inbox/<date>-<name>.yaml` and run
`./bib merge inbox/<file> [--dry-run] [--archive]`:

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

Always give `edit` and `delete` a `base`. With it, the merge is three-way:
fields only you changed apply, fields only others changed stay, and a field
both changed becomes a conflict. Without it, your values simply overwrite.

**Git**: run `./bib setup` once per clone. Section files then merge entry by
entry (`.gitattributes`): both sides' new entries are kept in order, and a field
changed on both sides becomes a conflict record instead of `<<<<<<<` markers.

## Conflicts and duplicates

A conflict never blocks a merge; it is written into the entry:

```yaml
  conflict:
    - {field: n, ours: …, theirs: …, base: …, from: berlin-autumn}
    - {kind: duplicate, of: [cal.1961-08-13.berlin-and-vienna], from: …}
```

`./bib conflicts` lists them; `./bib check` and `./bib build` fail until
they are settled:

```
./bib resolve ID --take ours|theirs|both|base [--field n]
./bib resolve ID --take keep          # a flagged duplicate that is really distinct
./bib combine KEEP DROP               # it is a duplicate: fold DROP into KEEP
```

`combine` unions tags, threads and citation lines, keeps DROP's id as an
alias of KEEP (old links still resolve), rewrites `[[DROP]]` links, and turns
any disagreement in text into a conflict on KEEP. Or edit the YAML by hand
and delete the `conflict:` block.

## Tags

Stored tags are free; use `namespace:value` (`topic:berlin`, `status:verified`,
`todo`, `source:frus`). `./bib tag ID... +topic:berlin -todo` edits them.

Derived tags are computed and searchable with `-t` but never stored:
`list:kja section:II.D check person work event thread:cuba month:1961-04
pub:1990s in:opp in:cal conflict`. `in:<list>` means the same work or person
is also in that list.

A deliberate exception to a `check` warning is tagged `ok:<rule>` on the
entry (the rule name is printed in brackets), e.g. `ok:thread-first`.

## Congress at each opening

`./bib build` also draws each Congress at its opening: party bars (majority and
two-thirds lines), a House map by district, a Senate map by state, and rosters
by state with pointers to Part III and the calendar entries that name each
member. All seven are on `build/congress.html`. A calendar entry tagged
`congress:<NN>` carries that Congress's block in `cal.html` and the reader;
now the Jan. 3, 1961 and Jan. 3, 1963 entries.

The rosters come from unitedstates/congress-legislators by
`tools/congress/make_rosters.py`, which holds the hand corrections (seats vacant
at the opening, terms missing from the source, notes). Fix a member there and
rerun it, or edit `congress/<NN>.yaml` directly for a one-off. The shapes come
from Lewis et al.'s district files by `tools/congress/make_geo.py` (needs
shapely and pyproj; the build does not), simplified twice: at 0.01 map units,
fine enough for a single Manhattan district, and at 0.12 for the full map; 11 MB
together. The pages draw the coarse shapes and swap in the fine past 3× zoom
(`FINE` in `templates/congress.html`). Each map is drawn when it nears the
screen, the House districts when first shown, and maps off the screen are not
painted (`content-visibility`). Pointers match members to Part III by
surname and first given name (with common short forms: Sam, Bill, Mike).

The maps label a member by surname alone; by initials and surname where the
surname is shared in that Congress (H.T. Johnson, A.W. Johnson); by full given
names (the `given` field) where the initials are shared too (James Thomas and
Joel Thomas Broyhill). The House map opens in Delegations, its default view: a dot a
seat, a block a State, set on the State or, for VT, NH, MA, RI, CT, NJ, DE and MD,
in a column off the coast with two-letter codes and leader lines. The block
positions are the ON and OFF tables in `templates/congress.html`. The dots stay through
zooming until one is clicked: that zooms to its district and shows the districts.
Then a click selects a district, a double-click goes there, and a double-click on
white space (water, or land outside the States) goes back. Map labels use
the two-letter postal codes. The bars split the Democrats, non-Southern then Southern:
the eleven Southern States, the thirteen represented in the Confederate States
Congress less Missouri and Kentucky.

## Economic indicators

`./bib build` puts a table at the head of each calendar month: the figures that
report on that month, filed by the period they cover, not the date they were
issued (quarters in the quarter's last month, fiscal years in June, calendar
years in December, December 1960 in the Prologue). Each row has the figure as
first reported, its release date, and the figure as revised today.

```
indicators/<id>.yaml          one series; rows {p, first, released, chg, unit, now, chg_now, source, est, q, note}
tools/indicators/make_indicators.py   writes them: FRED_API_KEY=... python3 tools/indicators/make_indicators.py
tools/bib/indicators.py       renders them (ORDER, GROUP) and checks them
```

- ALFRED initial releases: CPI, unemployment, payrolls, industrial production,
  GNP, real GNP; the deflator is GNP over real GNP in the same release.
- Transcribed from the *Economic Report* of the next January (page images on
  govinfo; values and table/page in MANUAL in the script): wholesale prices,
  the administrative and cash budgets, the federal sector of the national
  accounts, the balance of payments. For these "first" means as reported then.
- Today's values: FRED. Budget figures today are on the unified basis (fiscal
  1969 on), not the old concepts; the over-all balance of payments is no longer
  published; the gold stock has no first-reported column.
- Output gap: the CEA's estimates then (from the Reports) and the CBO's now
  (FRED GDPPOT against GDPC1, with its vintage), in separate rows: the concepts
  are not comparable, so each row leaves the other's column "—".
- Changes use one basis in both value columns (CHANGE in the script): monthly
  percent, not annualized; quarterly percent at an annual rate; points; persons.
  CPI, WPI and industrial production also carry the change from a year earlier
  (YOY in the script; `yoy`, `yoy_now`), each column from its own figures: the
  year-earlier value in the same release or Report (for the WPI, `year_ago` in
  MANUAL, transcribed from the same tables), and today's series.
- Formatting and style are settled in the STYLE notes at the top of
  `tools/bib/indicators.py` (periods "Q1 1961", "FY1962"; "$bn" and "m"; one
  scale per group; stacked receipts/expenditures/balance right-aligned; "—"
  versus "n.a."; separate rows for incomparable concepts). Follow them, and fix
  any table that drifts from them. Each series needs a definition in DEFS, with
  pointers; `check` fails without one.
- Edit the script, not the YAML, and rerun; the key comes from the environment
  and is never written to the repo. The build needs no network.
- `check` fails on a bad period, a first-reported figure without a release
  date, or a transcribed figure without a source.

## Publishing

The site is GitHub Pages: https://impending2223.github.io/bib/ (the compiled
reader; each list at `<key>.html`). Every push to `main` runs
`.github/workflows/pages.yml`: `./bib check`, `./bib build`, deploy. A failing
check stops the deploy. So publishing is merging to `main`. Run `check` and
`build` locally before you push.

The claude.ai artifacts named in `series.yaml` are frozen copies of
Oct. 1, 2026. Don't republish them; `publish-plan` and `mark-published`
belong to that old route.

## Do not

- read `build/*.html` or a whole list to find something: use `find`/`show`/`works`;
- change an `id`, or reuse a deleted one (add an alias instead);
- write the thread index by hand, or `s:` on calendar entries;
- edit `published.yaml` by hand;
- push to `main` with errors from `./bib check`.
