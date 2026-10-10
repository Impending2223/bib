# The 1968 series: how to work on it

Eight linked bibliographies and a calendar for 1961–1974, and a ninth on
Vietnam, kept as data and rendered to HTML. **Do not read the whole series,
and never read `build/`.** Find the few entries you need with `./bib`, edit
those, check, build.

## The brief (read before adding anything)

The owner's standing instructions; the messages they come from, verbatim, are in `notes/owner-brief.md`.

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
- `n`: the pointers, in this order:
  - the primary record, linked: the statute (Statutes at Large on govinfo, "77 Stat. 56"), the Federal Register, the
    Congressional Record, the Public Papers (APP), the presidential library's file, the FRUS document, the case.
    The owner asked for these (Oct. 2, 2026); where the record is found and the event's bibliography lacks it, add
    it there too.
  - the event's bibliography. An event is not a thread: the Bay of Pigs and Mongoose are two events in the Cuba
    thread; the Vienna Summit and the Berlin wall two in Berlin and Vienna. The event's first entry carries its
    full bibliography (works by short title with list and section); later entries of the same event point back to
    it with `See [[id]]`. An entry that opens a new event within a thread carries its own.
  - the event elsewhere in the series: the list sections that treat it ("K–J Adm. II.D"), where the bibliography
    has not already given them.
  - for an event done in private and documented in records nobody saw at the time (a recording, a memorandum, an FBI
    file), where and when it became public: "Made public: Drew Pearson's column, May 24, 1968." The brief's "left a
    trace, or should have left a trace": such events belong in the calendar, dated by the record.
  - `Names: …`, the list and Part III section of every person in `c` who has a Part III entry ("Names, events").
- `tags`: a hidden `name:<key>` (the name entry's anchor: `name:mcnamara-robert-s`) for every person the entry
  names or whose act it records and who has a name entry, the President included where the entry is his message,
  address, press conference, signature, order, proclamation, NSAM, meeting, or a poll of his approval. Tags are not
  shown; they put the entry in the person's life (Names), as do the persons of `Names:`. A namesake is not tagged
  (Edward McCormack is not the Speaker; Lucius Clay of Berlin is not his son), nor a name in a case's title.
  `check` fails on a key that names no person.

Each thread in `th.yaml` has a brief statement (`c`), as the owner asked: what the thread is, and its stations, in
one or two clipped sentences. Every thread is its matter as Washington met it, but the statements don't say so; that framing, and the scopes
taken out of the statements, are in `notes/threads.md`. `th.yaml` keeps the threads in alphabetical order of their
names (War on poverty under "poverty"; `check` warns otherwise).

`./bib audit-cal` checks the dated entries against these rules and writes `notes/calendar-audit.md`: persons in `c`
in neither `Names:` nor a `name:` tag, entries with neither a bibliography nor a `See`, entries with no primary record or with one
named but not linked, and the thread statements.

**Bibliography notes.** One or two fragments: what the book is, whose voice,
what to read it for. "Interviews with nearly everyone, Bissell included."
"Read the Washington chapters." Not reviews. Most entries need no note: when
the title does the work, leave it bare. No awards, no "start here," no side
labels ("defense," "revisionist," "from the left"); state a thesis or a
source's provenance the same way whichever side it is on. (This came of the owner's objection, Oct. 2, 2026, to
Viet. notes "unduly credulous of NVA/NLF/dovish material", which gave the critics "the unmarked default position"
and marked their opponents "the defense". The owner also asked where the Vietnamese-language works were: Viet. II.E
should hold them.)

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
elections/cq.yaml         CQ's *Guide to U.S. Elections* compared with the Clerk's figures, by page (kept by hand)
elections/renominations.yaml  renominations lost by primary, where a source says so (kept by hand)
elections/primaries.yaml  Senate primaries from CQ's *Guide*, by race (kept by hand; CQ prints no House primaries)
congress/changes.yaml     departures and successors during each Congress (generated)
congress/specials.yaml    special elections during each Congress, 87th–93rd, with candidates (generated)
congress/switches.yaml    members who changed party in office (kept by hand)
sources/states.yaml       each State's own official election publications, where to read them, what they print (kept by hand)
daybook/<YYYY-MM>.yaml    every Public Papers (APP) and FRUS document by date (generated)
daybook/abstracts.yaml    one-sentence abstracts, keyed by document (kept by hand or agent)
daybook/recordings/<YYYY-MM>.yaml  every White House recording PRDE catalogues, July 1962–Jan. 10, 1966 (generated)
daybook/sunday.yaml       the Sunday interview programs and their guests: Meet the Press, 1945–80; Face the Nation, 1959–70 (generated)
sources/loc/              the Library of Congress finding aid make_sunday.py reads (Spivak visual materials, pp020019, pp. 1–136)
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
| cal  | Cal.      | Calendar, Jan. 1961–Jan. 10, 1966 (87th and 88th Congresses; the 89th's first session); the primaries, 1960–76 |
| l68  | 1968      | The 1968 campaign ("the 1968 list")          |
| adm  | Adm.      | Nixon and his administration, 1969–74        |
| cong | Cong.     | Congress, the nation, and the states, 1969–74 |
| wg   | Wg.       | Watergate, 1971–74                           |
| vn   | Viet.     | Vietnam and the American war, 1945–75        |

Parts: I portrayals, II sources, III names. A reference like "K–J Adm. II.D"
is `lists/kja/II.D.yaml`. The calendar's files are named by month: `apr.yaml`
for 1961, `apr62.yaml` for 1962, `apr63.yaml` for 1963, `apr64.yaml` for 1964, `apr65.yaml` for 1965 (`dec62.yaml` runs to
Jan. 3, 1963; `dec63.yaml`, to Jan. 7, 1964; `jan64.yaml` from Jan. 8; `jan66.yaml` is Jan. 1–10, 1966), plus `th.yaml` (threads) and
`pro.yaml` (prologue); the primary seasons, `mar60.yaml`–`jul60.yaml` before the prologue and `mar68.yaml`–`aug76.yaml`
after Jan. 1966, hold only the primaries and the conventions' openings for now. Its sections are numbered straight
through, I to LXXXVII, in date order.

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
  short: State of the Union            # an address that sets several threads going: its name, and the threads,
  to: [economy, {health: cal.1963-02-05.program}]   # each resolving to its next entry, or the entry named
  c: What happened.
  n: Sources. See [[cal.1961-02-20.school-aid]].
  gloss: {title: Style, text: [A paragraph., Another.]}   # a note on the entry, not an entry: under it, smaller; the title run in
```

A `gloss` is for what the entry rests on and does not say: the record behind a name or a date, laid out in the
calendar's voice, quotations marked and cited, and what each piece of the record is and is not, stated plainly and
without a side (Jan. 30, 1961: the Address to the Joint Session, its *Style*). Rare.

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
- Quotation marks and apostrophes: type the keyboard's `'` and `"` in every hand-kept file (lists, executive/,
  the hand-kept sources); the build curls them in the pages' text, not in tags, URLs or scripts (`tools/bib/smart.py`,
  its STYLE notes), so a search or a match in the YAML needs only the one form. An inch is a prime (″), not a quotation
  mark. `check` warns on a curly mark in those files [straight-quotes]. Generated files keep what their sources print.

### House style (keep it)

Short declarative sentences. A calendar note points back ("See [[id]]"), not forward; where an earlier entry
must name a later one, it says what it is ("Reply: [[id]]", "The order: [[id]]", "Bibliography: [[id]]" where a
thread's first entry is excepted, `ok:thread-first`). A law the entry reports enacted is cited in `c` after its name, linked, as a case's
U.S. Reports cite is ("Equal Pay Act signed, [77 Stat. 56](…)": the volume and page, linked; no Public Law number), and the note keeps the list's
pointer ("Statute (K–J Cong. II.J.2)", as "Opinion (K–J Cong. II.J.1)"); a treaty by its U.S.T. volume and page, linked to the Library of
Congress's scan (its collection's table gives the TIAS number's volume and page), and its U.N.T.S. cite, linked to the UN's copy, at its signing, the Senate's consent, and ratification. Books already in a list are cited by short title
with list and section; works found only here are cited in full. "Check" marks
a detail to verify. In the calendar the first entry of each event carries its
bibliography and later ones point back with `See [[id]]`; a thread's first entry is its first event's. Bibliography sections
are chronological by publication unless their intro says "Alphabetical".

Vietnamese names and places carry their diacritics (Ngô Đình Diệm; Diệm, Khánh, Kỳ; Huế, Đà Nẵng), except where the
verbatim prints none: a quotation, a title, the byline of a work printed without them (Ky, *Twenty Years and Twenty
Days*; a Vietnamese-language work's byline has them), a writer who publishes without them (Lien-Hang T. Nguyen), the
FRUS and APP forms. English names stay: Saigon, Hanoi, Haiphong, Cholon, Dalat, Vietnam, Tonkin, the Mekong, Tet, Viet
Cong, Viet Minh, the Ho Chi Minh Trail. A person's entry in `sources/name-forms.yaml` lists the plain form first, for the
sources that print it; `check` warns on a plain form in the series' own prose (the calendar, every list's notes and roles, persons' subject lines; [diacritics]; places: `VIET_PLACES` in
`tools/bib/check.py`). Keys and anchors fold the marks, Đ to d (`ngo-dinh-diem`).

## Changing things

**Directly** (you are working in this repo): edit the section file, then

```
./bib new-id cal 1961-10-27 berlin-and-vienna   # an unused id
./bib check            # must end "0 errors"; deal with new warnings
./bib build            # build/<key>.html and build/series.html (a page alone: ./bib build congress | names | cal ...)
./bib links            # links between the built pages whose anchors are missing
```

Every YAML file is parsed once a run, and the parse kept in `.cache/yaml` (git-ignored) by path, modification time and
size, so a later run parses only what changed: `check` takes about 8 s, a full build about 35 s, a page 15-20 s.
A link to another page's anchor that a later build lost lands on the page's top; `./bib links` lists them.

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
that term's block in `cal.html` and the reader; now Jan. 20, 1961, and Nov. 22, 1963.

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
tools/executive/make_votes.py sources/senate-nomination-votes.json: the Senate's roll calls on nominations, 1953–74,
                              from Voteview (needs the network; the build does not)
tools/bib/votes.py            matches them to the roster's holders and the series' persons (STYLE notes at the top)
sources/vote-matches.yaml     kept by hand: what the rules cannot settle (a misspelling, a reconfirmation, a judge)
```

```
./bib executive check                 the roster's errors only (./bib check runs them too)
./bib executive who rusk              where a person is placed
./bib executive names [part3|daybook|cal]   series persons with executive roles not yet placed
./bib executive sources [all]         holder sources the line cannot link, by form ([all]: by holder)
```

- Each office shows, muted (smaller, gray, not italic), in a full-width row under the holders (over the office's law),
  at the left the holder before the term ("Before: Rusk, Dean left
  Jan. 20, 1969") and at the right the holder after it ("After: … took office …"), as precisely as known (`seen`/`last` say "in office by",
  "last listed"), each linked to the term table that holds him (Exec. 1965). The appointed holder over an acting
  one; before the term, an acting officer who held the office last follows him, marked "(acting)" (not where he is
  the term's own first holder). An office many hold at once (`many: true`) links the term tables before and after
  without naming anyone ("Before: Exec. 1957."). A link only to a table that holds the office.
- On `executive.html` each term (h2) has three parts (h3, all small caps, centered: President and Executive Office,
  Executive departments, Agencies and commissions), and the President's and departments' top units carry an h4 in
  their summary, styled as the summary, so the Outline drawer and the scroll tool stop at them; the agencies and
  commissions do not. The contents at the top list terms and parts only (`data-depth` on `tocList`). The
  calendar's copy of a term keeps plain summaries.
- Units nest by `under:` (the President at the top; the EOP; the departments in their order of creation;
  the agencies and commissions), offices within a unit by `under:` (Rusk, and the men under Rusk). Ranks in the
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
- Roll calls: a confirmation by recorded vote shows the count after the date, linked to the roll call on Voteview
  ("confirmed Sept. 21, 1973 (78–7)"), with any procedural vote on the nomination ("(64–19; recommittal refused,
  20–63)"); a rejection is a date of its own ("rejected June 19, 1959 (46–49)"); a reconfirmation for a further term
  too. A holder's roll calls name his surname, on his confirmation day or between nomination and confirmation; a
  holder never confirmed, the vote that refused him. A judge's or other post the roster does not hold shows in the
  person's Names entry by `persons` in `sources/vote-matches.yaml`. The calendar's thread "Confirmations" holds the
  contested ones of 1961–63.
- Vacancies are computed from the appointed holders; an acting officer shows under the vacancy he served in, not indented, its name in regular weight (`exac`).
- Statute links: govinfo files the Statutes by act, named by the first page (STATUTE-61-Pg495), with a
  suffix where several begin on a page (STATUTE-69-Pg9-2); a wrong name answers 200 with an empty body.
  `resolve_statutes.py` matches each cite by its chapter or public law and reports cites that point nowhere.
- Names as Part III writes them ("Rusk, Dean"), so the pointers find them; `given` for full given names.
- Sources (`src`), in the forms the line reads: `CDIR 1961-04` (an edition), `Cong. Rec.` (the Senate's days of
  nomination and confirmation), `Cong. Rec. Index 1961`, `POCOM`, `FRUS persons list[, 1961–63, V]`,
  `FRUS 1961–63, IX, doc. 144`, `Wikipedia: Title`, `APP[ YYYY-MM-DD]`, `Federal Register, Jan. 20, 1953`,
  `BD 1415` (the printed Biographical Directory of Congress, by page: a member's later offices), a URL,
  or a work in `sources/executive-sources.yaml` (add it there first). Quote an item holding a comma: a flow list
  splits it.
- State and the chiefs of mission come from POCOM (the Office of the Historian): commission, credentials,
  end of mission. Others from the Congressional Directory (each session), the Senate's records, department
  histories, and Wikipedia's lists for nominations. "Check" in a note marks a detail still to verify.

## Names

`./bib build` writes `build/names.html` (the index) and `build/names-a.html` … `names-z.html`: a name
entry for each person in Part III, the Executive roster, and the Congresses at their openings (`people` in
`tools/bib/lives.py`: one entry a person), and for each person FRUS's lists of persons (1952–76) give whom none of
those holds (`everyone`; `sources/frus-names/persons.json`, written by `frus_names.py --all`). Such an entry shows
each description the lists give, with its volumes (one post worded volume by volume is one line, in the wording most
volumes use: `same_post`, the telling words alike, dates, parentheses and "also …" clauses aside, no word of rank in one
that the other lacks), then the documents; it takes no races, roster or Directory, and
the matching of races, namesakes and authors goes by `people` alone. The lists' persons join across volumes by name
(`join`): the surname and suffix the same, the given names alike name by name (an initial for its name, a short form,
one spelling of another: Malik, Yakov Alexsandrovich, Aleksandrovich, Alexandrovich), every form that fits joined only
where those it fits fit one another ("John" does not join "John A." and "John B."); or the same words in either order
("Thanat Khoman", "Khoman, Thanat"); or, written in their own order, the same first word and the others spelled
alike with the same first letters ("Ngo Quang Troung"; not "Tran Van Chuong" and "Tran Van Huong"). A listed person
alike one person the series holds (also by the name he went by, "Thomas Hale" and "Hale", or a misprint with the same
middle initial, "Herbert H." Humphrey), where the lists' descriptions share a telling word with that person's offices,
is that person: his documents go to him (Ron Ziegler, Earl G. Wheeler, Robert J. Dole). Alike only by name, he has his
own entry (Lester B. Pearson is not Harold L.; Mohammed Ali of Pakistan not the boxer). The build joins further the persons
the lists alone give (`frus_groups` in `tools/bib/lives.py`, their documents, descriptions and APP lists united, the
other keys kept as anchors): forms alike but for the marks of transliteration and print (apostrophes and primes,
bracketed letters, the Arabic article, bin and ibn, Abdul and Abd al-, Al Sa’ud, a surname's spacing: Fahmi[y],
Fitz Gerald), the suffix the same; and, only where the lists' descriptions share a telling word or a word of office
and a country, given names agreeing by the series' rule, a Spanish or Portuguese surname's paternal part alone (Franco,
Franco y Bahamonde), or a word misspelled by a letter (Vaughan, Vaughn). A form joins a person the series holds only so, or as a form
`sources/name-forms.yaml` gives (Chou Enlai); forms joined through a third, only where every two are alike. What the rule cannot settle (a misprinted initial, a
romanization, Lin Piao and Lin Biao) is joined, or kept apart, in `sources/frus-joins.yaml`, each with its reason.
A description a list runs on into the next person's
entry is cut where that person's name begins, the name being one a FRUS list gives (`run_on` in `tools/bib/lives.py`:
"... British Foreign Office Caglayangil, Ihsan Sabri, Turkish Foreign Minister"). Where a list's persName holds
the surname alone, the given names come from the text after it; a title, office, service or nationality after the
given names is dropped (`recover`: "Jose A., Uruguayan"; "Cushman, Jr., Lieutenant General Robert E."); a name with a
digit (OCR) gets no entry.

APP: a title two persons of the surname share ("Governor Hughes": Harold E. of Iowa, Richard J. of New Jersey) gives a
document to one where its title or text names his State, a place in it, or his name in full, and nothing of the other's
(`marks` in `tools/lives/app_names.py`). The places are learned from the corpus (`places`): a town the documents write
with its State ("Atlantic City, N.J.", "Glassboro, New Jersey", APP's "Des Moines, IA") at least twice, nearly always
the one State, and not used alone thirty times for each time with it ("Washington", "Springfield" are no marks); a
place in two States is kept by hand in `sources/app-places.yaml` (the Delaware Water Gap: New Jersey, Pennsylvania).
Where the text does not settle it, the document is his who alone held the title that day (`holds`: `tenure` in
`sources/app-matches.yaml`, else the years his offices give); and for a pair whose tenure that file gives (the two
Governors Hughes, 1963-68), each of theirs, with "Check: “Governor Hughes” may be …" on the Names page
(`sources/app-names-checks.json`). `./bib names` builds those pages alone; `./bib names 'Humphrey, Hubert H.'
[--site URL] [--out FILE]` one page. The old `lives*.html` addresses forward to the new ones (`./bib lives` still works).
The scroll wheel and the Outline drawer give each entry's full name; the top bar its surname (`data-crumb`).
A Part III entry for two people writes them apart with ";" (`s: Evans, Rowland, Jr.; Novak, Robert D.`), never "&".
A name written in its own order, without a comma (Mao Zedong, Ngô Đình Diệm, Souphanouvong, U Thant, Malcolm X), is a
person too (`natural`): the whole name stands as the surname, and its other forms (romanizations, the forms FRUS lists
and the Public Papers use: Mao Tse-tung, "Diem, Ngo Dinh", President Diem) are in `sources/name-forms.yaml`, kept by
hand; FRUS and APP find the person by those. A Part III entry for a group (Wise Men, Chicago defendants) is tagged
`group` and has no name entry. A person the calendar names who fits no other Part III section goes in K–J Cong. III.K,
"Others named in the calendar".

Names link to their entries throughout (`tools/bib/namelinks.py`), muted: class `nm`, the text's own color and
a faint underline. Linked: the calendar's "Names:" (by the Part III section given), Part III subjects, the
Congress rosters, the Executive holders, election candidates (only a race matched without "Check"; a ticket by
its running name), special-election candidates (only a name with a roster seat in the State), FRUS senders in the
daybook (the index of documents sent, `sources/frus-names`, where one person fits), and a work's authors where
written in running order and one person fits ("Theodore C. Sorensen"). Not a name in its own entry, not an author
with no entry, not APP. A title alone in another person's subject entry is that person's (his memoir): his name is
put before it, linked. A President's surname alone as a title (Sorensen, *Kennedy*) is a work about him.

Who is one person (`people`, `one`): a name as written is one person in every source. Names written differently
join where the surnames agree, the given names agree (initials, middle names in order, the roster's `given`), and
the suffixes agree. Within the Congress rosters two names are two members; Part III may drop a middle initial but
not a suffix; the Executive roster may drop a suffix but not an initial (its bare "Anderson, Robert" is not Robert
B. Anderson). A bare name joins a fuller one from another source only with support: Part III's role shares a word
with the roster's office, or Part III's man sat in Congress, or the member's Directory entry gives Part III's role.
A short form ("Bob") joins only through the roster's "(Bob)", agreeing middle initials, or a role in Congress. A
father written bare and a son with "Jr." stay two (Harry F. Byrd; Barry M. Goldwater; a son `strict` in
`sources/app-matches.yaml` is never his father written bare: Lucius D. Clay and Lucius D. Clay, Jr.); the son's pointers, returns,
and FRUS documents go by his suffix, and a FRUS document naming the father bare after his death (the Directory's
year) is the son's. To keep two roster spellings of one man together, write them alike.

The Directory entry (`bd_entry`): the same surname and given names, a suffix that agrees, and an entry whose latest
year is 1953 or later, of a man not dead before 1953 or before the series first shows the person; anyone may match by
the middle name he went by (Thad Cochran, Brooks Hays); anyone not in the rosters only where the entry also names one
of his offices or Part III roles ("Governor of Arkansas"; the Presidency by "President of the United States"). Of
several, the one whose service spans the person's first seat, then the fullest agreement of given names.

Races (`election_sentences`): a candidate whose name agrees is taken. The surname may run to several words (Van Pelt,
St Germain, du Pont / DuPont). The first given name agrees as written, as a short form (Dick Clark; `SHORT` in
`tools/bib/congress.py`), as the rosters' own short form ("Daniel, Wilbur C. (Dan)": Dan Daniel), as the name the
series writes him by after an initial ("Sanders, H. Barefoot": Barefoot Sanders), or as the first initial with a
further given name spelled out where his full given names spell it (H. Carl Andersen: Herman Carl; J. Glenn Beall).
Initials alone (O. C. Fisher) and a further name alone (Dale Alford, Melvin Price) are not taken by name: "J. C.
Carter" is not Jimmy Carter, "Andrew Young" not John A. Young. The seat takes those: the winner of the surname whom
the roster seats from the race at the Congress's opening is the person, whatever the returns make of his given names
(Tip O'Neill, Mo Udall, Pete McCloskey); so is the incumbent of the surname the roster seated at the last opening,
where his first name agrees. For the 86th Congress, which has no roster: the Senator of the class at the 87th's
opening; the Representative the seat's 1960 race names as incumbent by the same name. A race the seat gives is
confirmed and refused only by his death or an executive office. Otherwise a race is
refused only on certain grounds: the race is after his death; the rosters seat another man of the name
from it, or seated one as its incumbent (by his written or full given names: J. Glenn Beall, 1964, is James G., not
John G. Jr.); the Directory's winner (`bd_winner`: its member of the name who sat for the
State and was elected to that Congress) is another man; the Directory's full given names disagree with the returns'
(George B. Murphy is not George Lloyd); he won while in executive office when the Congress met (Art. I, § 6). Nothing
is refused by State or party. A race nothing confirms (a roster seat from it, his own Directory entry as its winner
or naming his candidacy that year) shows "Check: matched by name only". `sources/race-matches.yaml` refuses or
confirms a race by hand, with the reason; `check` fails on a person or race there that does not answer.

The specials between Novembers (`congress/specials.yaml`, the States' and CQ's figures laid over) are taken by the same
rules, the seat being the roster's at the next opening ("June 28, 1960 (special)"). An incumbent who lost renomination
(the race's fates, from Wikipedia's race tables) has a row of his own, "Lost renomination", with the November
nominees, where the roster seated him from the State at the last opening; "in the Democratic primary" only where a
source says so (`elections/renominations.yaml`, kept by hand: 35 races, from the incumbents' Wikipedia articles), never
from a State's nominating law. Where `elections/primaries.yaml` holds the race's primaries (CQ's figures and printed
shares, by page), the row shows the rounds that name the person, each under its label, before the November vote
("General election"), and cites CQ, a little space above each label after the first; a lost renomination shows its
rounds alone, without the November vote, and gives the round he lost in the sentence ("in the Democratic
runoff": Jordan, 1972). `check` fails on a key there that names no race. The record table sets each candidate in three columns, the count and the
share right-aligned (under 520px the share goes under the count); a race for several seats (an at-large delegation:
Ala. 1962, N.M., N.D., Hawaii) has a dashed rule after the last winner, who is also the Xth name for X seats.

Each entry: the Directory's description (or the Part III role), the pointers into the series, then the life as
running text, with the date in each sentence; then Publications; FRUS documents sent; Oral histories given, papers,
and other primary sources; Secondary sources; and, folded, the FRUS and presidential documents that name the
person, and the White House recordings PRDE lists him speaking on (`recording_speakers`: PRDE's "Sr." and "II" are the
bare name; its "Jr." takes a bare form only where none carries "Jr." and the son is not `strict`; not in a President's
own entry). Empty sections are left out, the Life too. The FRUS and presidential lists are bulleted, a little space between items
(`lvnb`) and between the presidential documents under each year (`lvad`), and no more between years. "In the series"
leaves out the pointer the role line already gives (and is left out where that was its only one). Rules (the STYLE notes in `tools/bib/lives.py`):

- Each fact cites its ground source, linked: BD (the 2005 printed Biographical Directory, by page), the roster
  holder's own sources (CDir., CR, FR, DSB, GOM, POCOM, APP …), the Clerk's *Election Statistics* by page, a calendar
  entry's own sources. The series' pages are pointers, not sources: Exec. 1965, 87th, 88th Cong., Election 1960,
  Cal. Jan. 3, 1961, list sections — in the headings' sans serif, not underlined.
- A run of sentences with the same sources and pointers is a sentence block; its source block follows it: the
  cites, then the pointers. Each sentence block is a paragraph; a new one also at each office and election, and at
  each calendar entry, where the sources run on.
- An office is followed by the offices held ex officio by virtue of it, with their dates only where they differ.
- The Directory's color is cut (`CUT`); its bibliography is put in the series' form ("Timothy N. Thurber, *The
  Politics of Equality* (1999)"). FRUS headings with "from" in lower case.

```
tools/bib/lives.py            renders the entries and pages (STYLE notes at the top)
tools/lives/make_bd.py        sources/bd/<letter>.json: the 2005 printed Biographical Directory on govinfo, by page
tools/lives/frus_names.py     sources/frus-names/<letter>.json and volumes.json: the FRUS documents that name or were
                              sent by each person, one pass over every volume (python3 tools/lives/frus_names.py FRUS_GIT --all)
tools/lives/app_corpus.py     the APP documents of 1953-74, read once into a local corpus (resumable; about 2 hours)
tools/lives/app_names.py      sources/app-index.jsonl and sources/app-names/<letter>.json: the documents that name each
                              person, matched in the corpus
tools/lives/make_pocom.py     sources/pocom.json: POCOM's years of birth and death, career type, home State, and every
                              State post, for the persons POCOM holds (python3 tools/lives/make_pocom.py POCOM_DIR);
                              notes/pocom-matches.md, the matches made by name, with the evidence, and those refused
sources/pocom-matches.yaml    kept by hand: overrides to the name matches (Name: pocom-id, or Name: null)
sources/race-matches.yaml     kept by hand: races refused or confirmed for a person, each with its reason
sources/app-matches.yaml      kept by hand: a bare name two persons share, given to one for some years; a son known
                              only by his suffix (strict: Roosevelt, Hoover, Clay, MacArthur, Taft, Stevenson III)
sources/name-forms.yaml       kept by hand: the other forms of each name Part III writes in its own order (Mao Tse-tung)
sources/frus-joins.yaml       kept by hand: persons FRUS's lists alone give who are one (Faisal's five forms) or two
                              (`apart`), by key, each with its reason; `check` fails on a key that names no one
sources/app-places.yaml       kept by hand: places in more than one State, for telling two of a shared title apart
```

Namesakes in the FRUS and APP indexes: a further given name or initial tells two apart ('John W.' is not 'John G.';
FRUS's list gives the suffix apart, and it decides between a father and a son); a misprinted list is corrected in
`ERRATA` (`tools/lives/frus_names.py`: FRUS 1961-63, VII and XVI print Stevenson III for his father).

POCOM in a life: the years of birth and death where the Directory gives none; "Career Foreign Service officer" or
"Non-career appointee", with the home State; and the State posts the roster does not hold (ended before Jan. 20,
1953, or begun after Aug. 31, 1974), each cited POCOM and linked to the person's page. The roster's own POCOM ties
decide who is whom; anyone else is matched by name only with evidence (the rules: the script's docstring).

Rerun `frus_names.py --all` and `app_names.py` after adding people; the build needs no network.

## Special elections

Specials held between general elections are not in the Clerk's biennial *Statistics*, which print
only the November election. Of the specials held with a November election, the Clerk prints the Senate's
and, of the House's, only Ohio-6 and Washington-3 in 1960 (as unexpired terms, under the district): those are in the
election blocks; the other thirteen House specials held with November (1960-72) are `not_in_volume` in the readings
and show with the Congress's specials (`specials.between`). `make_elections.py` takes Wikipedia's House specials
dated on the general election (it once dropped every House special, so none reached the Clerk matching). After
each Congress at its opening, `build/congress.html` gives that Congress's specials: a summary, House
and Senate maps of the seats filled (large dots; the other districts drawn in the base map's gray; Result, Margin, Swing from the general election that chose
the Congress, same district), and a table of the races. A calendar entry tagged `special:<key>`
carries its race's table (the 87th's thirteen and the 88th's six of 1963, thread "Special elections"). Definitions: the STYLE
notes in `tools/bib/specials.py`.

```
tools/congress/make_specials.py   writes congress/specials.yaml from Wikipedia (needs the network)
congress/specials-state.yaml      votes read from the States' own returns, by hand (laid over specials.yaml)
congress/specials-cq.yaml         votes and shares from CQ's *Guide to U.S. Elections*, 6th ed. (2010), by hand (under the
                                  States' returns, over Wikipedia's shares)
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
- Senate specials: Texas 1961 from its own page; Vermont (Jan. 7, 1972) and Georgia (Nov. 7, 1972) from
  `SENATE_HAND` in `make_specials.py`, their votes CQ's. Georgia's was held with the November election, but the
  Clerk prints the regular race only, so it carries `not_in_clerk` and shows with the specials between elections.

- Where the State's returns are not read, CQ's *Guide to U.S. Elections* (`congress/specials-cq.yaml`, header
  there): votes and CQ's printed shares, cited by page; the State's returns stay the Check. CQ omits minor
  candidates and its shares count them; `check` fails on votes and shares that cannot come from one total. Where
  CQ and a State's returns differ, the State's stand (`differs_from_cq` in specials-state.yaml).
- Otherwise, shares are Wikipedia's tables of each year's House specials ("<year> United States House of
  Representatives elections"): percentages, no votes. Texas, 1961 (Tower): votes by round, from
  Bartley and Graham, *Southern Elections*. The official returns are the States' canvasses.
- Where Wikipedia's list and its year table disagree on a date, the table's is used and the race
  carries a "Check"; so do shares that do not add to 100.
- `check` fails on a duplicate key, a `special:` tag with no race, a switch not at its seat, or a reading
  whose votes do not add to its printed total or whose last round lacks the winner.
- Hawaii's first elections (July 28, 1959: two Senators, one Representative) are new seats, not vacancies (`new: true`
  in `SENATE_HAND`): "New seat." in the note, counted apart in the summary, "(first election)" in the roster lines.
- The 85th Congress (1957–59) has its specials only, ten House races from Wikipedia (CQ's figures for three), shown
  in a section of their own before the 86th.
- The 85th and 86th Congresses (1957–60) have no rosters. The 86th's specials (seven House races from Wikipedia;
  North Dakota's Senate race of June 28, 1960, Burdick's, from the State's canvass, `SENATE_HAND`) and its changes in
  membership (`changes.yaml`) are in, and follow the 1958 election on `congress.html`. The scripts now run 86th-93rd;
  Wikipedia's pages for later Congresses have since changed (the 91st's changes, the 1973 specials), so a rerun
  should be merged by Congress, not taken whole.
- Notes shown with a race are for the reader: CQ's shares that count unprinted candidates, and Wikipedia's dates or
  shares that a State's or CQ's figures settle, stay in the files (`remarks`) and are not shown; open Checks are.
  A race's `note` starts a new line ("Party primaries ..."). Months as the series writes them (Feb. 15, 1961). CQ is
  cited "CQ Guide 6th (2010) 1266", the full title with each block's sources and in the Names' list of sources.
- The margin column gives swing as "8.3 to D" ("No swing"); the headings "Date / Seat" and "Margin / Swing".

## Presidential primaries

`elections/pres-primaries.yaml`, kept by hand from CQ's *Guide to U.S. Elections*, 6th ed. (2010), ch. 11, pp. 404–422:
every presidential primary of 1960, 1964, 1968, 1972 and 1976, both parties, as CQ prints it (names, votes, shares,
its numbered notes; header there). Read off the pages with pdfplumber, the superscript note numbers apart; every
party's races add to CQ's printed total for the year, and `check` fails where they do not, or on a note number the
year does not print. `tools/bib/primaries.py` renders them (STYLE notes there):

- A calendar entry tagged `primary:<YYYY-MM-DD>` carries that day's returns, both parties, one row a State and party:
  candidates with votes and CQ's share (write-ins marked), the margin, CQ's notes; a printed share more than 0.1 point
  off its votes is noted ("CQ prints 4.8 for Others; the votes give 4.4"). One entry a primary day, thread
  `elections-<year>`; its `c` names the winners (a single State: the first two with shares).
- An entry tagged `primaries:<YYYY>-<R|D>` (the opening of the party's convention) carries the party's year: a
  summary (primaries, States won, votes), a map of the States by winner (Result: a color a candidate, `--q1`–`--q9`
  in `templates/congress.html`, in order of States won; unpledged slates `--qU`) and by margin (Margin: the winner's
  color by the election maps' quantile rule), and the table of races, each dated and linked to its day's entry.
  `drawQ` in `templates/congress.html` draws it.
- A bare surname in CQ's tables is the person CQ names in full under it earlier that year (Kennedy, 1968: Robert F.;
  after June 6, CQ prints Edward M.); `NAMES` in the module settles the rest (Brown, 1976). The tables give every
  candidate's full name, linked to the name entry where one person fits (a suffix must agree: Edmund G. Brown Jr. is
  not his father).
- Cites: the figures once, under the table, by the pages the races run over (`page`, `page_to`: "CQ Guide 6th (2010)
  404–405"), not in each race's note; CQ's notes are quoted with their page and number ("CQ Guide 6th (2010) 411 n.2: “…”", `notes_page`), and the
  one it repeats under a dozen races is paraphrased with the same cite. Nothing of CQ's goes out in its words unquoted.
- Names: every primary in which CQ prints a person is a row in his entry's record ("Elections and Congresses"):
  the party's primary in the State, the date linked to the calendar's day, the candidates (the person in bold), the
  pinpoint cite (`primary_rows` in `tools/bib/lives.py`).

## Rosters and elections, linked

`tools/bib/seatlinks.py`. Under each member at an opening, a muted line: the election that seated him ("Elected Nov. 8,
1960"; "Seat filled Nov. 4, 1958 (Kennedy)" where he did not win the seat's last election, as an appointed Senator;
1956 unlinked, having no block) and the seat's next ("Next: Nov. 6, 1962"; a special first, where one filled the
seat; for the House, his own race that November where one race in his State names him, else the same number's).
Under each race and special, "Roster: 87th Cong.", the seat's row at the next opening that has a roster. Under the
presidential vote, "Took office", the President and Vice President in the Executive roster at the next inauguration.
A row highlighted as a link's target (any roster or election table) goes plain when the reader clicks outside it
(`JS` in `tools/bib/roster.py`; `.unhl`). Tables write an at-large seat "AL" and leave the district column unheaded; a fusion candidacy's parties abbreviated ("D, R");
a whole vote "100%".

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
  reading's `printed` note says so: shown in the race's note, as is any other disagreement among the Clerk's own
  figures (a misprinted total, transposed figures, a party printed one way and counted another). A reading's `note`
  (other rulings) is kept in the file and not shown. Where the Clerk and Wikipedia disagree after a reading, the Clerk
  stands (`wikipedia_differs`), names included, unless the State's own canvass, read off its page, says otherwise:
  then the State's figure stands, the reading carrying `source` (the State's cite) and `clerk` (the Clerk's figures),
  both shown in the race's note (Md. 1958, Colo. 1960, Fla. and Mo. 1962; President: Wyo. 1960, Cal., Colo., Ga.
  1968, Cal. 1972). A later State compilation is not a canvass. CQ's *Guide to U.S. Elections* (6th ed., 2010) is
  compared in `elections/cq.yaml`; where it differs from the figures shown, its figures are printed in the race's note
  ("CQ Guide 6th (2010) 1275: Rivers 64,804."; `shown` there, read by the build); it fills a race only where the Clerk prints no vote (`source` without `clerk`:
  Pa.-6, 1964).
- Reading keys: `h NY 9` (district; 0 at large), `s MD 1` (Senate class), `h NM 0-1` (an
  at-large position), `s OR 2 special` (a special held with a regular race for the same seat).
  A special Wikipedia lists that the Clerk's November volume does not print goes under
  `not_in_volume` with the reason. `check` fails on a malformed or stale key.
- Candidates, incumbents, and their fates: Wikipedia's race tables. Names: the OCR's are for matching only (it
  garbles names), so a race takes Wikipedia's name where the surname matches; in a race read by eye, only where
  Wikipedia's given names agree with the printed ones (`wiki_names`): a nickname is no disagreement (Bob and Robert;
  '"Pete"' as printed), nor a first name or initial one drops; a first name nothing matches (Russell and Thomas S.
  Kleppe, N.D. 1970) or initials that differ (Gladys E. and Gladys L. Davis, Ohio-6, 1960; CQ prints E. too) is,
  and the printed name stands. Wikipedia's also mends the Clerk's surname misprints ('Zelenki'). New York's fusion
  candidates carry their party lines and the Clerk's total.
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
indicators/<id>.yaml          one series; rows {p, first, released, chg, unit, now, chg_now, source, est, q, note, since}
tools/indicators/make_indicators.py   writes them: FRED_API_KEY=... python3 tools/indicators/make_indicators.py
                              (without a key, from ALFRED's and FRED's public CSV downloads; the same figures)
tools/indicators/make_polls.py   Gallup's approval (kind: poll), a reading a row: as released (sources/gallup-approval.yaml,
                              read by hand from *The Gallup Poll, 1935–1971*, vol. III, by page) beside Gallup's series
                              today (the American Presidency Project's tables). In a table of its own under the
                              indicators, under a rule and its caption: Reading (field dates) | As published | Released | Today. The race for 1964,
                              the issues, and every other poll are calendar entries in the thread Opinion.
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
- The balance of payments changes concept as the Reports did: the over-all balance (1961–63), the balance on regular
  transactions (the January 1965 Report: 1963–64), then the liquidity balance and the official reserve transactions
  balance (January 1966: 1964–65), each its own series, never one row (STYLE 8). Real GNP and the deflator move to 1958
  prices with the benchmark revision of Aug. 19, 1965 (`BASE` in the script).
- Money and credit (`kind: rate`; RATES and DISCOUNT in the script, `--only rates` to write them alone): a table
  of its own between the indicators and the approval table, under the same rule, two columns (Rate | Percent):
  rates are not revised, so one figure each, with its change in points. The federal funds rate, the prime, the
  3-month bill and the 10-year Treasury from FRED; the New York Reserve Bank's discount rate kept by hand from the
  Board's press releases and the *Bulletin* (FRASER, by page): in a month it changed, the Board's announcement and
  the day it took effect in grey; otherwise `since` (the date it took effect, on hover). STYLE 13 in
  `tools/bib/indicators.py`.
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
the date added for a range or a month-only entry), under an address that sets several threads going (`to:`, `short:`) a "To:" line naming each thread
and the entry it leads to, and under each such entry a "From:" line back to the address (`program_links`), then a line a thread linking the entries before and
after it in the thread ("‹ Apr. 24 · Testing · June 10 ›", its `also` threads too; `thread_nav` in
`tools/bib/build.py`), a "Continuing" pointer under the date on each later
day of a ranged entry, and the day's documents, closed by default, with "Expand all" and
"Collapse all" under each month heading.

```
tools/daybook/make_daybook.py   writes daybook/<YYYY-MM>.yaml (needs the network; the build does not)
tools/daybook/make_recordings.py  writes daybook/recordings/<YYYY-MM>.yaml from PRDE's catalogue (needs the network)
tools/daybook/make_sunday.py      writes daybook/sunday.yaml from the Library's inventory, the TV listings, and the
                                  Face the Nation index (--ftn PATH; without it, its rows already written are kept)
tools/bib/daybook.py            lays the calendar out by day (STYLE notes at the top) and checks the data
```

- The President: APP's documents by date (Public Papers items, executive orders,
  proclamations), in APP's order.
- FRUS: every volume of the 1958–60, 1961–63 and 1964–68 subseries (the last for Nov. 1963 on), microfiche supplements
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
- Sunday programs: a muted line under a Sunday's date, "*Meet the Press* (NBC): Hubert H. Humphrey", each guest linked to
  his name entry, the source on hover. The record: the Library of Congress's inventory of Spivak's photographs of each
  Meet the Press television program (Prints and Photographs, pp020019, LOT 13025), by show date, its guests written as
  Part III writes names, 1945–80 (radio to 1950); the finding aid is in `sources/loc/`. The Classic TV Archive's episode
  guides (from the TV listings, 1947–Aug. 25, 1963) fill a Sunday the inventory lacks; where they name another person,
  the line carries "Listings: … Check." *Face the Nation* (CBS), Nov. 1959–1970: the index volume of *Face the Nation:
  The Collected Transcripts* (Holt, 1972), its chronological list: the date and the guests' names only (its topics and
  offices are CBS's text); the copy read is the owner's, not kept in the repo. *Issues and Answers* (ABC) is not yet in.
  A day with two programs has a line for each. Each name entry lists the person's programs ("Television interviews"). Guests and recording speakers are matched to persons by `person_named`
  in `tools/bib/lives.py`.
- Recordings: the White House tapes the Miller Center's Presidential Recordings Digital Edition (PRDE) catalogues,
  Kennedy's from July 1962 and Johnson's, a third list after APP and FRUS: PRDE's title, linked to its page, the time,
  "PRDE" and the tape cite ("Conversation WH6407-11-4288"). The catalogue only: the transcripts and the editors'
  introductions are the Edition's text, behind its subscription, and are not taken or paraphrased; what was said comes
  from published transcripts (Beschloss, *Taking Charge*, *Reaching for Glory*) and the studies. As a calendar entry's
  primary record: `[Johnson and Robert Kennedy, 12:25 p.m.](https://prde.upress.virginia.edu/conversations/4000560),
  Conversation WH6407-11-4288 (PRDE)`.
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
