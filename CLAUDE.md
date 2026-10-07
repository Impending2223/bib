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
elections/<YYYY>.yaml     President, House and Senate returns, 1956–74 (generated; never edit)
elections/readings/<YYYY>.yaml  figures read by eye from the Clerk's pages, with a note on each ruling
elections/pres-margins.csv  every contested race for presidential electors, 1824–2024, by constituency (generated)
elections/facts.yaml      hand-kept facts: caucus labels, faithless electors, 1960 slates, the Alabama reckonings
congress/changes.yaml     departures and successors during each Congress (generated)
congress/specials.yaml    special elections during each Congress, 87th–93rd, with candidates (generated)
congress/switches.yaml    members who changed party in office (kept by hand)
sources/states.yaml       each State's own official election publications, where to read them, what they print (kept by hand)
daybook/<YYYY-MM>.yaml    every Public Papers (APP) and FRUS document by date (generated)
daybook/abstracts.yaml    one-sentence abstracts, keyed by document (kept by hand or agent)
executive/<unit>.yaml     the Executive Branch, 1953–74: each department or agency, its offices, their law and holders (kept by hand)
build/                    generated pages (git-ignored)
tools/bib/                the code behind ./bib
tools/congress/           one-time scripts that made congress/ (see below)
tools/executive/          the one-time script that seeded executive/ from POCOM
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

Calendar entries have no `s` (the build makes the rubric, "Cuba, Apr. 15–19", and files
the entry under its first day):

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
shapely and pyproj; the build does not), for the 85th to the 94th Congress (the
elections need the districts before and after), simplified twice: at 0.01 map units,
fine enough for a single Manhattan district, and at 0.12 for the full map; 12 MB
together, with a point for the District of Columbia. The pages draw the coarse shapes and swap in the fine past 3× zoom
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

Notes under a member in the rosters at the opening give the seat's later changes: the
departure and its date, the successor and party, the date elected (linked to the special's
row) and the date seated (`congress/changes.yaml`, made by `tools/congress/make_changes.py`
from Wikipedia's Congress pages, "Changes in membership"; check a date against the
Biographical Directory where it matters), and a change of party in office, with its date
(`congress/switches.yaml`, by hand: Thurmond, Watson, Byrd Jr., Reid, Riegle).

## The Executive Branch

`./bib build` writes `build/executive.html`: the Executive Branch at each inauguration (1953, 1957, 1961,
1965, 1969, 1973) and at the successions of Nov. 22, 1963, and Aug. 9, 1974, with every change during each
term, through Aug. 31, 1974. A calendar entry tagged `executive:<YYYY-MM-DD>` (a term's first day) carries
that term's block in `cal.html` and the reader; now Jan. 20, 1961.

```
executive/<unit>.yaml         one unit (department, agency, office of the President): its offices, in order,
                              each with its law and its holders (schema: the docstring of tools/bib/executive.py)
tools/bib/executive.py        renders the blocks and the page, checks the files (STYLE notes at the top)
tools/bib/executive_names.py  who in the series is not yet in the roster
tools/executive/make_state.py seeded state.yaml and missions.yaml from POCOM, once; don't rerun
tools/executive/resolve_statutes.py   sources/statute-links.json: the govinfo file (and pin page) for every
                              Statutes at Large cite; rerun after adding law (needs the network; the build does not)
tools/executive/make_uscode_index.py  sources/uscode-loc.json: the Library of Congress's chapter scans of the
                              1952, 1958, 1964 and 1970 Codes, so a cite like '50 U.S.C. § 402 (1958)' links
templates/roster.css          the styles the Congress, election and Executive blocks share
tools/bib/executive_sources.py  each holder's `src`, read and linked in a "Sources:" line (the forms: its docstring)
sources/executive-sources.yaml  the register of named works a `src` may cite: pattern, label, full citation, link
tools/executive/make_source_links.py  sources/executive-links.json: the Senate's day in the bound Record for each
                              date, each year's Index, POCOM person ids, FRUS volumes by person (scratch inputs; once)
notes/executive-brief.md      the brief for whoever adds to the roster, person or agent
```

```
./bib executive check                 the roster's errors only (./bib check runs them too)
./bib executive who rusk              where a person is placed
./bib executive names [part3|daybook|cal]   series persons with executive roles not yet placed
./bib executive sources [all]         holder sources the line cannot link, by form ([all]: by holder)
```

- Units nest by `under:` (the President at the top; the EOP; the departments in their order of creation;
  the independent agencies), offices within a unit by `under:` (Rusk, and the men under Rusk). Ranks in the
  terms of Art. II, § 2, cl. 2: heads of departments, principal officers (PAS), inferior officers (PA, HD),
  employees, military officers (`rank`, `appt`).
- Holders: `from` (taking office) is required; `nominated`, `confirmed`, `recess`, `appointed` (the
  commission), `to`, `out`, `acting`. Where a source shows a holder in office but not when the term began or
  ended, write `seen` (the first day shown) for `from` or `last` (the last day shown) for `to`: shown "In office
  by Sept. 30, 1968", "Last listed …; end not known", and no vacancy is computed on that side. Holders in order of taking office; two who are not acting may not
  overlap unless the office is `many: true`. Holders who left on a term's first day show only in the term before.
- Law: `act`, `date` (enacted; for an amendment, ratified), `effective` and `until` where it took effect
  later or was repealed or superseded, `tags` (creates, powers, appointment, vacancy, pay, reorganizes),
  `cite` (Statutes at Large: the page the act begins on, then the pin), `usc` (sections with the edition:
  '3 U.S.C. § 19 (1958)'), `does`. A term shows only the law in force during it, in a full-width row under
  the office. The law of the whole unit goes on the unit; an office carries only its own.
- Vacancies are computed from the appointed holders; an acting officer shows under the vacancy he served in.
- Statute links: govinfo files the Statutes by act, named by the first page (STATUTE-61-Pg495), with a
  suffix where several begin on a page (STATUTE-69-Pg9-2); a wrong name answers 200 with an empty body.
  `resolve_statutes.py` matches each cite by its chapter or public law and reports cites that point nowhere.
- Names as Part III writes them ("Rusk, Dean"), so the pointers find them; `given` for full given names.
- Sources (`src`), in the forms the line reads: `CDIR 1961-04` (an edition), `Cong. Rec.` (the Senate's days of
  nomination and confirmation), `Cong. Rec. Index 1961`, `POCOM`, `FRUS persons list[, 1961–63, V]`,
  `FRUS 1961–63, IX, doc. 144`, `Wikipedia: Title`, `APP[ YYYY-MM-DD]`, `Federal Register, Jan. 20, 1953`, a URL,
  or a work in `sources/executive-sources.yaml` (add it there first). Quote an item holding a comma: a flow list
  splits it.
- State and the chiefs of mission come from POCOM (the Office of the Historian): commission, credentials,
  end of mission. Others from the Congressional Directory (each session), the Senate's records, department
  histories, and Wikipedia's lists for nominations. "Check" in a note marks a detail still to verify.

## Special elections

Specials held between general elections are not in the Clerk's biennial *Statistics*, which print
only the November election (specials held that day are there, and in the election blocks). After
each Congress at its opening, `build/congress.html` gives that Congress's specials: a summary, House
and Senate maps of the seats filled (large dots; the other districts drawn in the base map's gray; Result, Margin, Swing from the general election that chose
the Congress, same district), and a table of the races. A calendar entry tagged `special:<key>`
carries its race's table (the 87th's thirteen, thread "Special elections"). Definitions: the STYLE
notes in `tools/bib/specials.py`.

```
tools/congress/make_specials.py   writes congress/specials.yaml from Wikipedia (needs the network)
congress/specials-state.yaml      votes read from the States' own returns, by hand (laid over specials.yaml)
tools/bib/specials.py             renders the blocks, the calendar's race tables, the roster notes' dates; checks
```

- Votes: where a State's own returns print a special (`sources/states.yaml`, `best_for_specials`), its
  figures go in `congress/specials-state.yaml`, keyed by the race, with the publication, edition, page and
  copy read (header there). The race then shows votes by round and cites them; Wikipedia's shares stay
  in `specials.yaml` underneath. A date the State's returns correct goes in `STATE` in `make_specials.py`.
- Citations shown with a race (`cite`): the State abbreviated as in the Bluebook (Cal., Mass., Vt., N.C.),
  `*title*` in italics, date, page; linked to the copy read. A race not yet read carries `pending`, the
  source to check, shown "Check: <cite> (bot-check)" with its access from `sources/states.yaml`.
- Seats are written with a hyphen: MA-6, VT-AL (summaries, tables, map hover text).

- Otherwise, shares are Wikipedia's tables of each year's House specials ("<year> United States House of
  Representatives elections"): percentages, no votes. Texas, 1961 (Tower): votes by round, from
  Bartley and Graham, *Southern Elections*. The official returns are the States' canvasses.
- Where Wikipedia's list and its year table disagree on a date, the table's is used and the race
  carries a "Check"; so do shares that do not add to 100.
- `check` fails on a duplicate key, a `special:` tag with no race, a switch not at its seat, or a reading
  whose votes do not add to its printed total or whose last round lacks the winner.
- The 85th and 86th Congresses (1957–60) have no rosters and no specials.

## Elections

Every general election from 1956 to 1974, in `elections/<year>.yaml`: the House and Senate race by
race, and in presidential years the vote for President by State with the electoral votes as cast.
1956 is a base for swing and is not shown. `build/congress.html` puts each election from 1958 to
1974 before the Congress it chose (the 86th and 94th have no rosters); a calendar entry tagged
`election:<year>` carries its block too (now Nov. 6, 1962). A block: the electoral and popular vote
first, then by chamber the seats won, the net change from the close of the last Congress, pickups,
and new members; one view switch for every map (Result; Margin, the winner's lead over the runner-up in points of all the votes, by the quantile rule; Swing, continuous); the
President's map above the House and Senate, with a States | Flips | Electors switch (Flips: in Result, the
States that flipped dark, the others light; Electors: a dot an elector, as voted); the Senate map with a Senators toggle (a dot a seat, larger than the House's: `PB`, `RB`); and every race in tables:
candidates with party, votes and share, the margin in votes and in points of all the votes cast, and
a note. Pickups are shaded in the winner's color, other member changes in gray. Members of neither
major party count with the party they caucused with, and are labeled so ("Conservative, caucusing
with the Republicans"; `caucus:` in `elections/facts.yaml`), here and in the rosters and bars at each
opening. Definitions are the STYLE notes at the top of `tools/bib/elections.py`.

```
tools/elections/make_elections.py   writes elections/<year>.yaml and senate-prior.yaml (needs network, pdftoppm, tesseract)
tools/elections/president.py        the presidential vote by State (electors, names, notes from elections/facts.yaml)
tools/elections/pres_margins.py     elections/pres-margins.csv: every contested elector race, 1824–2024 (needs network, pandas)
tools/elections/read.py             loads elections/readings/; its docstring is the readings schema
tools/elections/review.py           the by-eye loop: left, sheets, pages, locate, verify, merge, audit (docstring)
tools/elections/review/             READER.md and PRESIDENT.md: instructions to hand a reader, person or agent
tools/bib/elections.py              renders the blocks and checks the data (STYLE notes; "Map records")
```

- Votes: the Clerk's *Statistics of the Presidential and Congressional Election*
  (clerk.house.gov), OCR'd. Each figure is read three times and settled against the
  State's recapitulation total and Wikipedia's percentages (`reconcile.py`); a race that
  does not settle is read by eye into `elections/readings/<year>.yaml`. Where a race page
  and its recapitulation differ, the figure the Clerk's totals add up with is used, and the
  race's `note` says so. Where the Clerk and Wikipedia disagree after a reading, the Clerk
  stands (`wikipedia_differs`), names included.
- Reading keys: `h NY 9` (district; 0 at large), `s MD 1` (Senate class), `h NM 0-1` (an
  at-large position), `s OR 2 special` (a special held with a regular race for the same seat).
  A special Wikipedia lists that the Clerk's November volume does not print goes under
  `not_in_volume` with the reason. `check` fails on a malformed or stale key.
- Candidates, incumbents, and their fates: Wikipedia's race tables; names as Wikipedia
  gives them where the surname matches. New York's fusion candidates carry their party
  lines and the Clerk's total.
- President: each slate's vote (its highest elector), assigned to a candidate by
  Wikipedia's results by State; electoral votes from the same table, with `CAST`.
- Margins are ordinary: the leader's votes less the runner-up's, over all the votes. The
  two-party share (D over D+R) serves only for swing.
- Swing: House, the same district where its lines did not change between the two
  Congresses (the same shape key in `congress/geo.json`), otherwise the State's House vote;
  Senate, the seat's last regular election, six years before (1952 and 1954 from
  `elections/senate-prior.yaml`, Wikipedia's percentages); President, the last
  presidential election.
- Hand facts (who caucused with whom, electors who broke, the 1960 unpledged slates, the
  Alabama reckonings) live in `elections/facts.yaml`, not in code. A third-party member
  missing from `caucus:` fails `check`.
- To add or correct an election, follow the loop in the docstring of `tools/elections/review.py`:
  `make_elections.py YEAR --cache DIR`; `review.py left` and `sheets`/`pages`; readers with
  `review/READER.md`; `review.py verify`, then `merge`; rerun `make_elections.py` (it should
  leave nothing); `review.py audit YEAR`; `./bib check`; then tag the calendar entry.
- Colors are tokens at the top of `templates/congress.html` (its CSS is in commented
  sections). Result and Flips: four steps a side (`--eR1`–`--eR4`, `--eB1`–`--eB4`).
  Margin: a straight line in OKLab from `--rW` (near white) at a tie to `--rR`/`--rB`, the darkest steps, by the
  quantile rule: a margin's position is the share of the 2,291 contested races for presidential electors,
  1824–2024, decided by less (`elections/pres-margins.csv`, written by `tools/elections/pres_margins.py`; the
  build puts its percentiles into `QM`). Swing: from `--eN` (gray) at none to `--eR4`/`--eB4` at `SWING`
  points. The keys draw the same scales as gradient bars.
- "Check" in a note (as in the calendar) marks a detail still to verify:
  `grep -rn Check elections/facts.yaml elections/readings`.

## State sources

`sources/states.yaml` is the register of each State's own official publications of election returns: blue
books, legislative manuals, registers, statements of vote, canvasses, abstracts, count books, and the State
election databases. Its header is the schema. For every State and D.C. it records, for 1956–1974 first:

- each publication or database: title, publisher, which edition prints which election;
- what it prints: the general election, the specials between Novembers (with votes or not, as checked against
  `congress/specials.yaml`), State races (governor, statewide, legislature), primaries (official or party);
- every online copy with its `access` from here, tested on the date in `checked`: open, borrow, bot-check,
  blocked, dead, other;
- `best_for_specials` (where to get vote counts for that State's specials) and `gaps` (what is only on paper).

Start there before searching for a State's returns. The Clerk's *Statistics* stay the source for `elections/`;
a State figure goes in as a reading or a note, with its page. Recheck access with
`python3 tools/sources/check_access.py [--write] [--st XX ...]`; `check` fails on a State missing from the
register, an access outside the legend, or an online copy without a url or a checked date.

- Bot checks (Cloudflare, AWS WAF, captchas) are the sites' own: don't try to get around them; a person in a
  browser can open the page. HathiTrust's pages are bot-checked here, but its catalog data (the Bib API,
  `catalog.hathitrust.org/api/volumes/brief/htid/<id>.json`) answers: holdings and rights, not text.
- archive.org works: item pages, OCR text (`/download/<id>/<id>_djvu.txt`), page images
  (`/download/<id>/page/n<N>.jpg`). Many States' runs are there (CT, NH, MA, IL, CA, NC, HI, MT, AL, FL).
- A host this environment's network policy refuses ("CONNECT tunnel failed, response 403") is `blocked`; the
  owner can allow it in the environment's network settings.

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

## The calendar by day

Each dated section of the calendar (a month) is laid out by day, in `cal.html` and the
series reader alike: the month's undated entries, then every day from the section's first
to its last. A day shows its date, "*New York Times*" under it (a TimesMachine link by
date only; "No *New York Times* (strike)" from Dec. 8, 1962 to Mar. 31, 1963), the entries that begin
that day, each under its thread as a rubric (a line of muted small capitals above the entry;
the date added for a range or a month-only entry), a "Continuing" pointer under the date on each later
day of a ranged entry, and the day's documents, closed by default, with "Expand all" and
"Collapse all" under each month heading.

```
tools/daybook/make_daybook.py   writes daybook/<YYYY-MM>.yaml (needs the network; the build does not)
tools/bib/daybook.py            lays the calendar out by day (STYLE notes at the top) and checks the data
```

- The President: APP's documents by date (Public Papers items, executive orders,
  proclamations), in APP's order.
- FRUS: every volume of the 1958–60 and 1961–63 subseries, microfiche supplements
  included, from the TEI files at github.com/HistoryAtState/frus; dated by
  `frus:doc-dateTime-min`. Editorial notes carry only their volume's span, so each is
  filed under the document before it in its volume. Within a day, by volume and number.
- Authors are persons where the sources name one, read through each FRUS volume's list of
  persons (the `corresp` links on names): the heading's sender ("Director of Central
  Intelligence (Dulles)"), else, where the heading names an office ("Mission at Berlin"),
  the signer (Lightner), else the drafter of a memorandum of conversation. Initials and
  first-name signatures ("LLC", "Bob K.") count only through a link. Where FRUS's link
  is wrong, the heading's office words (Attorney General → Robert F. Kennedy) or a signature
  naming another listed namesake (John S. D. Eisenhower) correct it. Intelligence estimates go
  to the board their note says concurred (U.S. Intelligence Board). A person shows by surname
  ("Rusk") unless the lists or the Presidents hold another by that name; then by full name
  ("McGeorge Bundy", "John F. Kennedy"). An office shows where nobody signed. Rules and order:
  "authors as persons" in `tools/daybook/make_daybook.py`. Titles are the sources' own;
  nothing is read or summarized by the generator.
- FRUS citations carry the volume's title: "FRUS 1961–63, XXIV: Laos Crisis, doc. 4".
- Abstracts go in `daybook/abstracts.yaml` (`key: sentence`), never in the generated
  files, so a rerun keeps them. Keys: `app:<slug>`, `frus:<volume>/<dN>`. `check` fails
  on an abstract whose key is not in the daybook.
- To extend the span, change FROM/TO in the script and add calendar sections; the days
  follow the calendar's dated sections.

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
