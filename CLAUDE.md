# The 1968 series: how to work on it

Eight linked bibliographies and a calendar for 1961–1974, and a ninth on Vietnam, kept as data and rendered to HTML. **Do not read the whole series, and never read `build/`.** Find the few entries you need with `./bib`, edit those, check, build.

This file is the core every task needs. The rest is in topic guides, `notes/guide/<topic>.md`, moved there word for word (Nov. 10, 2026, the owner: "I approve both"): read a guide when your task touches its topic, and only then. A pointer elsewhere to "CLAUDE.md, *Section*" means that section's guide (the index at the foot).

## The brief, in short (full: `notes/guide/brief.md`; the reader's rules: `notes/briefs/reader.md`)

The owner's standing instructions; their messages, verbatim, in `notes/owner-brief.md`.

**Prose.** "Compact. Plain. Compressed. Springs and Autumns, but without the subtle words." Record what happened, not what it meant. No praise, blame, irony or color. Short declaratives and fragments; drop articles and verbs where the line still reads. Read a few entries of the section you add to before writing.

**The calendar.** "A calendar of executive and legislative events, and any other events that left a trace, or should have left a trace, on the political and policy histories of the Kennedy and Johnson Administrations, their Congresses, or those of their members ... not a narrative, but a memory aid and a bibliographic record ... Names, events." What is an entry: the reader's brief (R5, the test: what the work being read dates and treats as an event; R7, the informal record; R18, what is not an entry).

Every calendar entry has:
- `c`: what happened, one to three clipped sentences. Who, what, the number.
- `n`, in this order: the primary record, linked (the statute, "77 Stat. 56"; the Congressional Record, "[106 Cong. Rec. 13,819](…) (1960)"; the Public Papers, "Title, [1961 Pub. Papers 1](…) (Jan. 20, 1961)"; the FRUS document; the case; the recording); then the event's bibliography, works as cards (`[[w.beschloss-crisis-years]], 123`), the event's first entry carrying it in full and later ones pointing back (`See [[id]]`); for a private act on a record nobody saw then, "Made public: ..."; then "To check: ..." (works and records not yet read, a sentence of its own); then `Names: Heller, Tobin.` (every person in `c` with a name entry, by surname); then any "Check: ..." sentence.
- `tags`: a hidden `name:<key>` for every person named or whose act it records (the President for his own acts); `state:`, `city:` tags for the States and cities.

What each source stands for (the owner, Oct. 23, 2026): a source cited stands for the whole of `c` unless a parenthetical, a label or its place says otherwise ("[[w.x]], 123 (the vote)"). A source read that does not bear out a claim is no cite for it: the claim takes "Check:" or goes. Sources read come first, with their pinpoints (a page, a document, a note: a number, or the place linked); works not yet read stand behind "To check:". A work with no card yet gets one first: `./bib works new`. Claim maps (`src`), witnesses (`sources/witnesses/`, readers' new ones in `inbox/witnesses/`), variants: `notes/guide/brief.md` and the reader's brief, R35–R43.

**Spans and events** (the owner, Oct. 20 and 28, 2026): an entry is an event-day; two or three days good, a week the limit; never several events in one entry (an announcement and the act, hearings and the vote, a note and its reply). One event touching several threads is one entry, `thread:` its chief one, `also:` the rest.

**Bibliography notes.** One or two fragments: what the book is, whose voice, what to read it for. Not reviews; no side labels. Most entries need none.

**Forms that `check` enforces** (details in the guides): election results "Winner (P) over Loser (P), W to L, p percent" (`entries.md`); a small town's State at first mention, "Anniston, Ala." (`entries.md`); Vietnamese diacritics, "Ngô Đình Diệm" (`entries.md`); straight quotes in the YAML; en dashes in ranges; a law enacted cited in `c` after its name, linked.

## Entries, in short (full: `notes/guide/entries.md`)

```yaml
- id: kja.beschloss-crisis-years       # permanent; never rename or reuse
  s: 'Kennedy, Robert F.'              # optional subject line (people, memoir subjects); never on calendar entries
  c: Michael R. Beschloss, *The Crisis Years* (1991)
  r: Attorney General, 1961–64         # people (Part III): the role
  n: The note.
  tags: [topic:berlin]
- id: cal.1961-04-15.cuba              # calendar: cal.<date>.<thread>, -2 if taken (./bib new-id cal DATE THREAD)
  when: Apr. 15–19                     # shown as written
  date: '1961-04-15'                   # '1961-02' for month-only entries
  thread: cuba                         # a thread's slug (th.yaml)
  also: [space]
  c: What happened.
  n: Sources. See [[cal.1961-02-20.school-aid]].
```

Markup: `*Title*` italics; `[text](https://…)` a link; `[[w.id]]` a work's card (full cite at first appearance in a year's page, short form after); `[[id]]` another entry (shown as its date). YAML: single-quote a value holding `: ` or ` #` or starting with `*`, `[`, `'`, `"`; double an apostrophe inside (`'Kennedy''s'`). Type the keyboard's `'` and `"`; the build curls them. A calendar note points back ("See [[id]]"), not forward.

## Changing things, in short (full: `notes/guide/changing.md`)

Directly: edit the section file, then `./bib check` (must end "0 errors"), `./bib build` (a page alone: `./bib build cal | names | works | congress ...`), `./bib links`.

By patch (readers working at once): `inbox/<date>-<name>.yaml`, ops `add` (a new entry, claimed first in the ledger: `./bib ledger add DATE THREAD ID "words" PATCH`), `edit` (with `base:` the rev `./bib show` printed), and the additive ops that need no base: `cite: {id, item, units}`, `primary`, `to-check: {id, add}`, `check: {id, text}`, `src`, `names: {id, add, tags}`, `also`, `variant`, `follows`. `./bib patch-check PATCH` until no errors. `./bib merge --auto PATCH...` merges (one merge at a time: merges have no lock; readers never merge). `./bib setup` once per clone.

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
./bib works list -t in:kja -t pub:1990s --sort year   the cards answering a query (below, "The works catalogue")
./bib works show w.beschloss-crisis-years             a card and every place it is listed
```

`find` prints `id`, then `file:line` and a one-line summary. Open the file at that line to edit, reading only that section.

## Conflicts and duplicates

A conflict never blocks a merge; it is written into the entry:

```yaml
  conflict:
    - {field: n, ours: …, theirs: …, base: …, from: berlin-autumn}
    - {kind: duplicate, of: [cal.1961-08-13.berlin-and-vienna], from: …}
```

`./bib conflicts` lists them; `./bib check` and `./bib build` fail until they are settled:

```
./bib resolve ID --take ours|theirs|both|base [--field n]
./bib resolve ID --take keep          # a flagged duplicate that is really distinct
./bib combine KEEP DROP               # it is a duplicate: fold DROP into KEEP
```

`combine` unions tags, threads and citation lines, keeps DROP's id as an alias of KEEP (old links still resolve), rewrites `[[DROP]]` links, and turns any disagreement in text into a conflict on KEEP. Or edit the YAML by hand and delete the `conflict:` block.

## Tags

Stored tags are free; use `namespace:value` (`topic:berlin`, `status:verified`, `todo`, `source:frus`). `./bib tag ID... +topic:berlin -todo` edits them.

Derived tags are computed and searchable with `-t` but never stored: `list:kja section:II.D check person work event thread:cuba month:1961-04 pub:1990s in:opp in:cal conflict`. `in:<list>` means the same work or person is also in that list.

A deliberate exception to a `check` warning is tagged `ok:<rule>` on the entry (the rule name is printed in brackets), e.g. `ok:thread-first`.

## Working hours

The owner's standing rule (Oct. 28, 2026): no work between 7 a.m. and 5 p.m. Pacific, Monday to Friday; Saturday and Sunday are exempt (the same day). At 7 a.m. the running agents are stopped, their work committed as WIP and listed for resuming; a task or an agent's report that comes in before 5 p.m. is queued, not acted on, and answered with the one word "Queued." (the owner, the same day); after 5 p.m. the agents are resumed and the queue taken up in order. Two scheduled tasks keep it in the session that runs the reading (6:46 a.m. and 5:04 p.m. Pacific, weekdays).

## Publishing

The site is GitHub Pages: https://impending2223.github.io/bib/ (the compiled reader; each list at `<key>.html`). Every push to `main` runs `.github/workflows/pages.yml`: `./bib check`, `./bib build`, deploy. A failing check stops the deploy. So publishing is merging to `main`. Run `check` and `build` locally before you push.

The claude.ai artifacts named in `series.yaml` are frozen copies of Oct. 1, 2026. Don't republish them; `publish-plan` and `mark-published` belong to that old route.

## Do not

- read `build/*.html` or a whole list to find something: use `find`/`show`/`works`;
- change an `id`, or reuse a deleted one (add an alias instead);
- write the thread index by hand, or `s:` on calendar entries;
- edit `published.yaml` by hand;
- push to `main` with errors from `./bib check`.

## Topic guides (`notes/guide/`; read the one your task touches)

- `brief.md`: the brief in full (the calendar's entry, sources, claims, witnesses, threads and their statements, bibliography notes).
- `layout.md`: every directory and data file, what made it, whether to edit it.
- `entries.md`: entry fields, glosses, spans, subthreads, markup, house style, election-result form, places, Vietnamese names, leads, date lists.
- `changing.md`: patches, additive ops, the ledger, patch-check, merge, git.
- `works.md`: the works catalogue, cards, the A–Z bibliography.
- `calendar-by-year.md`, `calendar-contents.md`, `calendar-by-day.md`: the calendar's pages, its tables and maps, the day layout, the day's order and times, the daybook (FRUS, APP, recordings, committees, Bulletin, Diary, opinions).
- `public-papers.md`: the Public Papers volumes, cites, APP links.
- `names.md`: the Names pages, who is one person, races, hearings.
- `executive.md`: the Executive Branch roster.
- `congress-opening.md`, `committees.md`, `rosters-elections.md`: each Congress at its opening, leaders and committees, roster and race links.
- `elections.md`, `specials.md`, `primaries.md`, `conventions.md`, `governors.md`, `legislatures.md`: returns and their sources.
- `state-sources.md`, `state-finance.md`: the States' publications and law registers; State finance.
- `indicators.md`, `armed-forces.md`, `budgets-bills.md`: economic indicators, the war's tables, forces, budgets, bills, appropriations.
- `indochina-maps.md`: the maps of Indochina.
- `ebooks-feeds.md`, `desk.md`: the ebooks and feeds; the owner's desk.

