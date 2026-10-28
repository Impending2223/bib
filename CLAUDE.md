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

The informal record (the owner's rule, Oct. 23, 2026: "the sinews of the public history"): the calendar is not the
public record narrowly construed. For the persons with public roles (executive, legislative, policy, foreign
relations, the administration of justice, the campaigns and the parties' communications), the transactions behind it
belong too: informal meetings, lobbying, agreements, the planning of policy, personnel, operations and communications,
in the West Wing, the members' offices, the campaign headquarters. Their record is mostly memoirs, biographies, oral
histories, recordings and diaries: date each by its source, cite it by page, name whose account it is where it is one
participant's ("by O'Donnell's account"), and where accounts differ, say so ("Check: Sorensen gives ..."). The reading
runs look for them.

The parties and the members (the owner's rule, Oct. 29, 2026, on the readings' "minor": "What rule makes this kind of
position-taking, messaging, organization, communication, policy formation, campaigning, etc., in the opposition and
among non-majority-leadership MCs 'minor'? Can we amend it?"; "I'm quite interested in what the Republicans were up to,
and what they were saying, in these years"): within the brief, and never "minor", the position-taking, messaging,
organization, communication, policy formation and campaigning of either party out of the White House and of any member
of Congress, leader or not: a party's statements, papers, declarations and platforms; its committees' and leaderships'
meetings and decisions; the founding and doings of its factions and allied groups (the Ripon Society, the Free Society
Association, Young Americans for Freedom, the American Conservative Union, the Democratic Study Group); and the dated
public word (a speech, statement, press conference, interview, article or column under his own name) of a member, a
governor, a party officer or a party figure out of office (Eisenhower, Nixon, Goldwater, Rockefeller, Romney, Scranton,
Percy, Reagan) on policy or politics. A journalist's column is an entry only where it carried an act (a leak, a trial
balloon) or made news itself. "Minor", as a reason in a "Passed over" list, means only: a repetition of a position
already entered, with nothing new; private or social trivia; an operation or incident below the level the calendar
records. The threads: Republican Party (`republican-party`; its subthread "In Congress", `republican-party-congress`),
Conservative movement (`conservative-movement`), Democratic Party (`democratic-party`); `notes/threads.md`.

So every calendar entry has:
- `c`: what happened, in one to three clipped sentences. Who, what, the number.
- `n`: the pointers, in this order:
  - the primary record, linked: the statute (Statutes at Large on govinfo, "77 Stat. 56"), the Federal Register, the
    Congressional Record, the Public Papers (GPO's volume, "1961 Pub. Papers 1"; APP where they do not print it: "The
    Public Papers"), the presidential library's file, the FRUS document, the case.
    The owner asked for these (Oct. 2, 2026); where the record is found and the event's bibliography lacks it, add
    it there too.
  - the event's bibliography. An event is not a thread: the Bay of Pigs and Mongoose are two events in the Cuba
    thread; the Vienna Summit and the Berlin wall two in Berlin and Vienna. The event's first entry carries its
    full bibliography (each work by its short form, "Surname, *Main Title*", the leading article dropped, linked to
    its entry in the A–Z bibliography; no list or section; a run of works printed in order of publication, then by
    the first author's surname or the short title, then the short title: `ordered` in `tools/bib/works.py`, at build); later entries of the same event point back to it with
    `See [[id]]`. An entry that opens a new event within a thread carries its own. This is how the calendar points
    "to the relevant material elsewhere in the bibliography" (the owner's words); it no longer names the themed lists'
    sections that treat the event (the owner's ruling, Oct. 13, 2026, with the move to one A–Z list). Write a work as
    its card, `[[w.beschloss-crisis-years]]` (a pinpoint after it: `[[w.gallup-poll]], III, 1862`): the build prints
    the full citation at the work's first appearance in each part of the calendar, the short form after (the owner's
    request, Oct. 13, 2026; FIRST CITE in `tools/bib/works.py`). A work with no card yet: make one first (`works/`, or
    `./bib works adopt`).
  - for an event done in private and documented in records nobody saw at the time (a recording, a memorandum, an FBI
    file), where and when it became public: "Made public: Drew Pearson's column, May 24, 1968." The brief's "left a
    trace, or should have left a trace": such events belong in the calendar, dated by the record.
  - `Names: …`, every person in `c` who has a name entry ("Names, events"), by surname, commas between: "Names: Heller,
    Tobin." No list or section after the names (the owner's ruling, Oct. 14, 2026; taken out of the data Oct. 15). Each
    name is found by its `name:` tag and the name index (`who_named` in `tools/bib/build.py`) and linked to the name
    entry; a person with a name entry but no Part III entry (from the rosters or FRUS's lists) by his tag alone
    (`tagged_named`). Where the tagged persons share a surname, write the given name ("Martin Luther King", "Frank Johnson"); a son
    or father with his suffix ("Harry F. Byrd Jr.", "Martin Luther King Sr."); a name in its own order as it stands
    ("Ngô Đình Diệm", "Satō", "Haile Selassie"). Nothing after the names but a sentence of its own ("Check: …").
    `check` warns on a list or section written in the line [names-section], a name no person fits [names-unknown], and
    one several fit that the tags do not settle [names-ambiguous]. A justice is named only where the entry quotes his
    opinion or is about him, not for writing or joining one.
- `tags`: a hidden `name:<key>` (the name entry's anchor: `name:mcnamara-robert-s`) for every person the entry
  names (every name of `Names:` among them) or whose act it records and who has a name entry, the President included where the entry is his message,
  address, press conference, signature, order, proclamation, NSAM, meeting, or a poll of his approval. Tags are not
  shown; they put the entry in the person's life (Names), as do the persons of `Names:`. A namesake is not tagged
  (Edward McCormack is not the Speaker; Lucius Clay of Berlin is not his son), nor a name in a case's title.
  `check` fails on a key that names no person.

What each source stands for (the owner's rule, Oct. 23, 2026): a source cited under an entry stands for the whole of
`c`, its dates, numbers, names, quotations and facts, unless the note says otherwise; where it does not, the entry and
the note together say which claim each source is for: a parenthetical after the cite ("[[w.x]], 123 (the vote)"), a
label before it ("Votes: ..."), or the cite in the sentence of `c` it supports. Omission implies, determinately: under
an entry ABCD, "X; Y; Z (C)" says X and Y stand for A, B and D, and Z for C and C's tie to the rest (the same person,
act or thing), not for A, B and D. A source read that does not bear out a claim is no cite for it: the claim takes
"Check:" or goes.

Hard and soft (the same day): the sources read (the primary record, linked; a work cited with its pinpoint, read off
the page) come first; the works not yet read stand behind "To check:", a sentence of its own before "See" and
"Names:" ("To check: [[w.a]]; [[w.b]]."), the event's bibliography among them. A reading run that reads one moves it
out, with its pinpoint and, where it stands for part of the entry, its parenthetical; a source found and not yet read
(a book, a hearing, a file) joins the To check. "Check:" marks a detail to verify; "To check:", sources not yet read.
Swept Oct. 24, 2026: every work cited without a pinpoint went behind "To check:" (2,439 notes; a work inside a
sentence of prose, some two dozen, left as written).

Claims and their sources (the owner's request, Oct. 28, 2026: "break the entries down into (invisible?)
sentence-by-sentence, clause-by-clause units, and accord to each the appropriate (invisible?) pincite", in a form "readily
and programmatically transformed into a 'verbose' citation format ... footnotes or inline citations"; invisible for now):
each entry's `c` is split into units at its sentences' ends and its semicolons, never inside a quotation, parentheses or
brackets, lettered A, B, C (the ABCD of the rule above; a finer unit is a semicolon, nothing is marked in `c`). Its
claim map says which source grounds which units at which page: worked out from the note whenever wanted (a work read and
no parenthetical, all; with one, `?`, to be turned into letters by a reader), and stored only where a reader maps it, as
the hidden `src` (`{c: <hash of c>, rows: ['w.caro-passage-of-power 492: A', 'w.dallek-flawed-giant 70: B-E', 'via
w.dallek-flawed-giant 70 n.36: B, E', '<a link's address>: all']}`), written by patch. Every row names an item the note
(or `c`) prints; the note stays the visible record, and `check` holds the two together [claims]. `./bib claims show ID
[--inline]` prints the units and the entry with its sources as footnotes (or inline), `./bib claims seed ID` the
mechanical map to start from, `./bib claims stats` the count. The STYLE: `tools/bib/claims.py`.

What the works rest on (the same day: the agents to log "the materials and records cited for the claims in the
secondary sources they read", and "identify the ABCD fact, claim, or quotation it sources, along with the entry"): a
reading run that cites a work's page for an entry describes each record the work's note gives for it once, in
`sources/cited-records/<card>.yaml` (the schema: `tools/bib/cited_records.py`; check [cited-records]), and ties it to
the units it grounds by a `via` row of the entry's map (`via w.dallek-flawed-giant 70 n.36: B, E`); several records
under one note for one passage, each its row, the same letters. The unread record joins "To check:" with the work it
comes from ("To check: Bundy to Johnson, Feb. 7, 1965, NSF, LBJ Library (cited by [[w.dallek-flawed-giant]], 251
n.14)."). And what a reading passes over: every dated event the work treats and the run did not enter is listed in its
`notes/book-checks/` file under "Passed over", page, date, event and why (out of the brief, undated, minor, already in
under another id, a lead), for the owner to rule on. "Minor" as the parties-and-members rule above defines it.

Calendar entries on the States and the cities take hidden `state:<postal code>` and `city:<slug>` tags (`state:ny`,
`city:nyc`) and the threads in `notes/threads.md` ("The States and the cities").

Each thread in `th.yaml` has a brief statement (`c`), as the owner asked: what the thread is, and its stations, in
one or two clipped sentences. Every thread is its matter as Washington met it, but the statements don't say so; that framing, and the scopes
taken out of the statements, are in `notes/threads.md`. `th.yaml` keeps the threads in alphabetical order of their
names (War on poverty under "poverty"; `check` warns otherwise). The calendar is built in three parts (below, "The
calendar in three parts"): a thread's `c` speaks to the first part it has entries in, and `c2`, `c3` to the second and
third where it has entries in an earlier one too; the scope stays the same in all, the stations each part's own.

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

A work's note is either the card's (the card note: true of the book wherever it is listed: "Interviews with nearly
everyone, Bissell included") or the listing's (why it is in this list: "Read the Washington chapters"). The card note
shows first, then the listing's; a listing may write `card_note: replace` or `omit`.

Before and after:

```
no:  c: Gilpatric at Hot Springs, Virginia, to the Business Council. The American
        second strike is at least as large as any Soviet first strike. The missile
        gap reversed, in public, for Moscow's benefit.
yes: c: Gilpatric to the Business Council at Hot Springs. The American second
        strike at least equal to any Soviet first strike. The missile gap reversed.
     n: '[[w.ball-politics-and-force-levels]]; [[w.kaplan-wizards-of-armageddon]]. See
        [[cal.1961-02-06.defense]]. Names: Gilpatric.'
     tags: [name:gilpatric-roswell-l]
        (shown: Ball, *Politics and Force Levels*; Kaplan, *Wizards of Armageddon*. See Feb. 6. …)
```

## Layout

```
series.yaml               the lists: key, abbreviation, old artifact URL
lists/<key>/list.yaml     a list's title, intro paragraphs, and outline (sections → files)
lists/<key>/<file>.yaml   one section's entries, in display order (II.D.yaml, apr.yaml)
works/<letter>.yaml       the works catalogue: one card a work, by the first letter of its id (w.beschloss-crisis-years);
                          shown A to Z on build/works.html
inbox/                    patch files waiting to be merged
congress/<NN>.yaml        each Congress at its opening (87–93), on build/congress.html ("Elections"): House by state and
                          district (0 = at large), Senate by state and class
congress/geo.json         district and state shapes, projected and simplified
elections/<YYYY>.yaml     President, House and Senate returns, 1956–74 (generated; never edit)
elections/readings/<YYYY>.yaml  figures read by eye from the Clerk's pages, with a note on each ruling
elections/pres-margins.csv  every contested race for presidential electors, 1824–2024, by constituency (generated)
elections/pvi.yaml        each State's partisan voting index for the elections of 1962–74, from the two presidential
                          elections before (generated by tools/elections/make_pvi.py; never edit; shown: tools/bib/pvi.py)
elections/readings/districts/<cdb-YYYY>.yaml  the presidential vote by congressional district as the Census's Data Books
                          print it, a file a volume, each figure by page (kept by agent; tools/elections/cd_readings.py)
elections/pvi-districts.yaml, elections/cd-president.yaml  each district's PVI, 1960-74, where its lines carry both
                          elections, and the figures used (generated by make_pvi.py; never edit; shown;
                          notes/extensions/memos/pvi-districts.md)
elections/facts.yaml      hand-kept facts: caucus labels, faithless electors, 1960 slates, the Alabama reckonings
elections/cq.yaml         CQ's *Guide to U.S. Elections* compared with the Clerk's figures, by page (kept by hand)
elections/renominations.yaml  renominations lost by primary, where a source says so (kept by hand)
elections/primaries.yaml  Senate primaries from CQ's *Guide*, by race (kept by hand; CQ prints no House primaries)
elections/conventions.yaml  the national conventions: each delegation's votes, how chosen, the roll calls (kept by hand)
sources/cited-records/    the records each secondary work cites for the calendar's claims, described once, a file a work
                          (kept by agent); the claims each grounds are `via` rows of the entries' maps (tools/bib/claims.py)
notes/extensions/         proposals and shelved drafts: memos/ (the research memos before a part was built), shelf/ (drafts
                          set aside, code and data, not read by check or build), README.md (the index, by hand)
notes/leads.md            leads to check later: events, figures and sources the drafting agents could not place
congress/changes.yaml     departures and successors during each Congress (generated)
congress/specials.yaml    special elections during each Congress, 87th–93rd, with candidates (generated)
congress/switches.yaml    members who changed party in office (kept by hand)
congress/committees.yaml  each Congress's leaders and standing committees, 87th-93rd, and the committee list (generated)
congress/committees-hand.yaml  the leaders Nelson does not code, the ICPSR joins and row corrections (kept by hand)
congress/committees-cdir.yaml  each Congress's select, special and joint committees, 87th-93rd, from the Congressional
                          Directory (generated by tools/congress/make_cdir_committees.py; never edit)
congress/subcommittees.yaml  the subcommittees of the 87th, 88th and 92nd, with their members, from the Congressional Staff
                          Directory (generated by tools/congress/make_subcommittees.py; never edit)
elections/governors.yaml  every general election for governor, 1960–68 (generated from Wikipedia; never edit)
elections/legislatures.yaml  each State legislature's parties by session, 1959–69 (generated from Klarner; never edit)
statefin/states.yaml      each State's finances by fiscal year, 1959–68, State and local together, the large cities (generated
                          from Census's databases; never edit)
budgets/budgets.yaml      each fiscal year's budget, 1961–70, by source and function: proposed and first reported (kept by hand)
budgets/today.yaml        the same years as OMB's Historical Tables give them today (generated; never edit)
budgets/debt-limits.yaml  the thirteen acts changing the debt limit, June 30, 1960–Apr. 7, 1969 (kept by hand)
congress/bills.yaml       a bill's course, step by step, from the History of Bills and Voteview (kept by hand)
congress/appropriations.yaml  each session's appropriation bills against the estimates, 1960–68, from the Record (kept by hand)
sources/states.yaml       each State's own official election publications, where to read them, what they print (kept by hand)
sources/state-law.yaml    each State's session laws, code, constitution, journals and attorney general's opinions, 1959-69: the
                          authority for each, where to read them (kept by hand)
notes/state-sources.md, notes/state-law-sources.md  the two registers as listings (generated by tools/sources/make_listing.py)
daybook/<YYYY-MM>.yaml    every Public Papers (APP) and FRUS document by date (generated)
daybook/abstracts.yaml    one-sentence abstracts, keyed by document (kept by hand or agent)
daybook/recordings/<YYYY-MM>.yaml  every White House recording PRDE catalogues, July 1962–Jan. 20, 1969 (generated)
daybook/recordings/millercenter.yaml  the same span's recordings the Miller Center gives free, page and audio (generated)
daybook/diary.yaml        the days of Johnson's Daily Diary the National Archives Catalog gives scanned (50), address and
                          page count (generated by tools/daybook/make_daily_diary.py; never edit)
sources/frus-text/<YYYY-MM>.json.xz  the text of every FRUS document the daybook files, in XHTML, for the ebooks (generated by
                          tools/ebooks/make_frus_text.py from the TEI; public domain; 38 MB)
sources/ppp-text/<package>.json.xz  the Public Papers, 1960–69, GPO's 14 volumes on govinfo: every item, its heading, date,
                          pages and cleaned text with its pagination (generated by tools/ppp/make_ppp_text.py; public domain)
sources/ppp-matches.json  the APP documents matched to Public Papers items, and the items' index (tools/ppp/match_app.py)
daybook/sunday.yaml       the Sunday interview programs and their guests: Meet the Press, 1945–80; Face the Nation, 1959–70 (generated)
daybook/printed.yaml      where FRUS's notes say each document, or a text they cite, was printed then: the *Bulletin*, *Current
                          Documents* (generated by tools/daybook/make_printed.py)
daybook/bulletin/<YYYY>.yaml  the *Department of State Bulletin*'s items by day, from each issue's index; Jan. 6, 1960-Jan. 20,
                          1969, but July-Dec. 1968 (generated)
sources/dsb-pages.json, sources/dsb-issues.yaml  the *Bulletin*'s copies on archive.org and its issues, 1956–69, number, date,
                          pages (generated by tools/daybook/make_dsb_index.py)
sources/loc/              the Library of Congress finding aid make_sunday.py reads (Spivak visual materials, pp020019, pp. 1–136)
executive/<unit>.yaml     the Executive Branch, 1953–74: each department or agency, its offices, their law and holders (kept by hand)
sources/vn-provinces-1966/  South Vietnam's provinces of late 1966 rebuilt from today's districts, the corps zones, regions,
                          and the gazetteer of places in Indochina (its README; made by tools/vnmap/)
sources/indochina/        the maps of Indochina's data: one border geometry, relief tiles, rivers, climate, rain, population
                          (its README; made by tools/vnmap/)
sources/vendor/           MapLibre GL JS, PMTiles and the map's font, pinned and served from the site (its README)
build/                    generated pages (git-ignored); build/days/, the calendar's daily blocks a month a file
tools/bib/                the code behind ./bib
tools/congress/           one-time scripts that made congress/ (see below)
tools/executive/          the one-time script that seeded executive/ from POCOM
```

| key  | cited as  | list                                         |
|------|-----------|----------------------------------------------|
| kja  | K–J Adm.  | Kennedy and Johnson administrations, 1961–69 |
| kjc  | K–J Cong. | Congress, the nation, and the states, 1961–69 |
| opp  | Opp.      | The Republican opposition, 1961–69           |
| cal  | Cal.      | Calendar, Jan. 6, 1960–Jan. 20, 1969 (the 86th Congress's second session; the 87th through the 90th; the 91st's opening); the primaries, 1960–76; built as three pages, Cal. I (`cal.html`, 1960–62), Cal. II (`cal63.html`, Jan. 1963–Jan. 9, 1966) and Cal. III (`cal66.html`, from Jan. 10, 1966) |
| l68  | 1968      | The 1968 campaign ("the 1968 list")          |
| adm  | Adm.      | Nixon and his administration, 1969–74        |
| cong | Cong.     | Congress, the nation, and the states, 1969–74 |
| wg   | Wg.       | Watergate, 1971–74                           |
| vn   | Viet.     | Vietnam and the American war, 1945–75        |

Parts: I portrayals, II sources, III names. A reference like "K–J Adm. II.D"
is `lists/kja/II.D.yaml`. The calendar's files are named by month, year and month, `YYYYMM.yaml` (`196104.yaml`;
any year: `178904.yaml` would do), and so are their section ids (`196104`; the old ids, `apr`, `apr60`, kept as
`old_id`, which the headings still anchor); every section a calendar month (`196001.yaml` from Jan. 6, 1960, the
calendar's first day; `196901.yaml` to Jan. 20, 1969, its last; January 1966 two, `196601.yaml` and `196601b.yaml`, at the
third part's opening), plus `th.yaml` (threads); the primary seasons after Jan. 1969, `197203.yaml`–`197608.yaml`, hold
only the primaries and the conventions' openings for now. Its sections are numbered straight through, I to CXXIV, in date order, in the data (`num`); the headings show the
dates alone.

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

A list entry for a work points to its card instead of writing the citation (`work: w.beschloss-crisis-years`, or a
list for several) and keeps its own note; "The works catalogue" below. A new entry may still be written with `c`:
`./bib merge` and `./bib works adopt` make the card.

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

Spans (the owner's ruling, Oct. 20, 2026): an entry is an event-day. Spans of two or three days are good, under a week
tolerable; anything longer deserves close scrutiny, and an entry never bundles several events (an announcement and the
act it announces, hearings and the vote, a note and its reply): each gets its own entry, dated to the day its record
bears, the first keeping the event's bibliography and the rest pointing back. A day's "Continuing" line names what is
under way; it should say something. 1961 is the model.

One event, one entry (the owner's ruling, Oct. 28, 2026: "One entry, listed in both threads"): a meeting, a call, a
document or an address whose matter falls in several threads is one entry, filed under its chief thread (`thread:`) and
listed in the others (`also:`), never one entry a thread. Its bibliography is in one place; each thread's index and
⟨⟨ ⟩⟩ line find it by `also:`. (Several events on one day stay several entries, as above.)

Subthreads: a thread in `th.yaml` may name a `parent:` ("Defense: McNamara to Clifford", `id:
cal.thread.defense-clifford`, `s: McNamara to Clifford`, `parent: defense`). Its entries are the parent's too (the
index's dates, the ⟨⟨ ⟩⟩ line, the highlight); the rubric, the ⟨⟨ ⟩⟩ line and the Continuing line give its full name. A
subthread without a statement (`c`) is a ghost: named where it is under way, and in the thread index by a line under its parent: its
full name ("Vietnam: Pennsylvania") muted, not underlined, as the A–Z bibliography's ghosts are, then its dates as any
thread's (its rubric links there; STYLE 9 in `tools/bib/calsplit.py`); give it a `c` to promote it. A renamed thread
may keep its old name in the index, muted, a link to the thread, naming it ("Desegregation: schools: School desegregation"; `s:`
the old name, `see:` the slug), or, where the old name went to several threads, the old name in the text's color and the
threads muted, linked, a middle dot between ("Legislatures: Districting and apportionment · State legislatures"; `see:` a
list; STYLE 10). A hidden `sort:` files a thread under other words, the name unchanged ("1960 elections" as "Elections
of 1960"; "Special elections" as "Elections, special", a redirect left at S); `check` holds th.yaml to it. A statement
may end in "*See also* X · Y" (`see_also:`, slugs; set right, in the thread names' type; STYLE 11), for related matter
elsewhere in the index, not for a parent, its subthreads or an alphabetical neighbor (the owner's rules, Oct. 21,
2026). A university's desegregation is a subthread of School desegregation, in its State's thread too by `also:`
(Ole Miss, University of Georgia). No thread or subthread name begins with "The"
(the owner's rule, Oct. 21, 2026: "Jupiters", "Air war"). Use one where a thread holds two or more events at once,
or where the thread's name does not say what is going on. In `th.yaml`, after its parent (alphabetical by full name).
`thread_name`, `entry_threads` in `tools/bib/build.py`; `thread_line`, `is_ghost` in `tools/bib/store.py`.

The thread index (Part I of the calendar) is generated from `thread` and
`also`; never write dates into `th.yaml`. A new thread is a new entry in
`th.yaml` (`id: cal.thread.<slug>`, `s:` name, `c:` one-line scope).

### Markup inside text

- `*Title*`: italics. `[text](https://…)`: an outside link. A link out of the site (a DOI, a record, a newspaper) shows
  in the accent blue; a link within it (an entry, a work's A–Z entry, a list's section, a date) as a name link does,
  the text's own color with a faint underline (`:where(main) a` in `templates/list.html` and `series.html`; a link a
  class styles keeps its own). A work's first citation in full links its author and title to the A–Z entry without an
  underline (`a.xf`), the faint underline shown only under the pointer, while pressed (`:active`; on a phone, the touch
  before it lifts: the templates listen for touches so iOS Safari shows it), or at keyboard focus. An article's link spans the volume, the journal and the first page: `[27 J. Latin Am.
  Stud. 1](https://…)`.
- `[[w.id]]`: a work of the catalogue, linked to its entry on `works.html`: in the calendar, its full citation at its
  first appearance in each part (FIRST CITE), its short form after ("Beschloss, *Crisis Years*"; SHORT FORM in
  `tools/bib/works.py`; a card's `short` overrides); elsewhere the short form. `[[w.id|full]]` the full citation
  wherever it stands; `[[w.id|text]]` shows "text". A merged card's old id still answers. `check` fails on a card that
  does not exist.
- `[[id]]`: a link to another entry, shown as its label (a calendar date).
  `[[id|text]]` shows "text". Use these for "See …" in calendar notes, so a
  corrected date updates every reference. The build adds the year when the
  date linked to falls in a different year from the entry linking to it
  ("Dec. 21–22, 1961"); don't write the year in.
- Cross-list references stay plain prose ("(K–J Adm. II.D)", "Also Opp."). The build links them and `check`
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
Congress's scan (its collection's table gives the TIAS number's volume and page), and its U.N.T.S. cite, linked to the UN's copy, at its signing, the Senate's consent, and ratification. Books already in the catalogue are cited by their cards (`[[w.id]]`),
shown by short form and linked to the A–Z bibliography (no list or section); works found only here are cited in full. "Check" marks
a detail to verify. In the calendar the first entry of each event carries its
bibliography and later ones point back with `See [[id]]`; a thread's first entry is its first event's. Bibliography sections
are chronological by publication unless their intro says "Alphabetical".

Election results in `c` (the owner's rule, Oct. 23, 2026: "fix the form to a single, prescribed standard"; "the
simplest forms here, e.g., 'Anderson (R) over Governor Docking (D), 511,534 to 402,261, 55.4 percent', are perfectly
fine. Keep those everywhere"). One form, commas only, no colon or semicolon: a race, "Winner (P) over Loser (P), W to
L, p percent", the winner's count first, p the winner's share to one decimal (in a primary no party: "Kennedy over
Humphrey, 476,024 to 366,753, 56.5 percent"); a margin, where the entry gives one or the race was close, after the
share, "..., 50.3 percent, a 1,988-vote margin", never "by 1,988 votes"; a measure, yes first, p the yes share:
"Proposition 1 carries, 3,008,328 to 2,834,384, 51.5 percent", "Proposal 2 fails, 1,876,185 to 3,408,090, 35.5
percent", never "yes ..., no ..." or "p percent yes"; a third candidate or more after the two, in the same sentence,
"Name N, p percent". Always both counts and the percentage. The denominator: all the votes cast for the office (for a
measure, yes and no) where the source prints that total (as the Clerk's figures and CQ's specials do); where it gives
only the two leading counts and others ran, their sum, "p percent of the two". Where a rule differs (a measure needing
a majority of all voting at the election, or two-thirds; a runoff below a majority), a few words after the figures
say so ("a majority of all who voted at the election needed"). Several races or measures in one entry: each in the
form, a sentence or a clause each. A missing count or share comes from the entry's own source, the series' data
(`elections/`, `congress/specials*.yaml`) or a source read then, cited in `n`; else what the entry has stands, and
the note says "Check: the count" (or "the percentage"). `check` warns on a result not in the form, on a share the
counts do not give, and on a margin that is not W - L [result-form] (`tools/bib/resultform.py`, its STYLE); a
quotation is not read, and an entry the form does not fit (several places on one ballot, a crowd's count) takes
`ok:result-form`. Not results: a convention's ballot of delegates, electoral votes, the polls, other countries'
parliamentary elections.

Leads (the owner's standing rule, Oct. 18, 2026): anything recalled but not placed or verified (an event without a
date, a figure without a source read, a source not reached, an item left out as minor) is written into
`notes/leads.md` under its heading (States and cities, National, Foreign, the Executive roster), with the entry it
concerns and where to look; never into the calendar unchecked. A lead leaves the list when it is entered or settled. Every
drafting brief asks its agents for their leads, and they go into the file when their work is merged.

A run of calendar dates, wherever the series prints one (the thread index, the pointers under each member and holder in
the Congress and Executive rosters, the Names' "In the series"), is written by year: "Cal. **1961** Jan. 20, May 16.
**1962** Jan. 22–31.", the year in the sans, a little heavier, unlinked, a full stop after each year's dates. One
function writes them all (`tools/bib/datelist.py`, its STYLE notes); a new list of dates calls it.

Places in the calendar's entries (`c`): a city or town of the United States under 75,000 people at both the 1960 and
the 2020 census takes its State by the Bluebook's abbreviation at its first mention in each thread, in each calendar
(an entry in several threads takes it where it is the first in any): "Anniston, Ala.", "Muncie, Ind.", "Concord, N.H.".
Not Gettysburg, Atlantic City, Key West or Palm Beach; Huntington, W. Va. (83,627 in 1960) takes it all the same. An
unincorporated place takes it too ("Parchman, Miss.", "Longdale, Miss.", "Hye, Tex."), Hyannis Port excepted. So too,
anywhere, a named military base, a cape, and Liberty Island ("Fort Benning, Ga.", "At Andrews, Md.", "West Point, N.Y.",
"Homestead, Fla.", "Cape Cod, Mass.", "Cape Canaveral, Fla."), Camp David excepted; not a hospital (Bethesda Naval
Hospital), nor the Oakland Army Terminal. Two places of one name take their States wherever either is meant ("Oxford,
Miss.", "Oxford, Ohio"; "Albany, Ga.", "Albany, N.Y."; Athens; "Hot Springs, Va."; "Cambridge, Md."), but Philadelphia is
Philadelphia (only the Mississippi town takes its State). Columbia is not the District. A county is left to the
writer's judgment (those tagged so far: the Deep South's, and "Prince Edward County, Va."). A neighborhood of a city
named goes without (Harlem, Watts, South Boston, Hollywood). An entry in one State's thread (Alabama, Georgia,
Mississippi, South Carolina) whose places all lie in that State names no State at all: the rubric does it. Washington
(the White House, the Oval Office) is no place elsewhere. Not the thread statements, not the notes, not a quotation ("in
Selma, Alabama"). The census figures: Wikipedia's tables of each place's censuses, read Oct. 12, 2026 (Muncie 68,603
and 65,194; Albany, Ga. 55,890 and 69,647; Rock Hill 29,404 and 74,372; Homestead 9,152 and 80,737).

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
./bib build            # build/<key>.html and build/series.html (a page alone: ./bib build congress | names | works | cal ...)
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

## The works catalogue

Every work the lists cite is a card in `works/`, once; the lists point to it (`work:`), so a correction to the card
changes every listing, short form and page. `tools/bib/works.py` is the only code that reads the cards; everything
else asks it (its docstring has the fields and the STYLE notes). A card is structured (author, title, year, and the
rest as fields; the citation is rendered from them) or verbatim (`c`, the citation as written, where the fields cannot
yet render it; author, title and year read from it for sorting and search).

```yaml
- id: w.beschloss-crisis-years          # permanent; w. and the first author's surname and the title's words
  author: [Michael R. Beschloss]         # running order; editor, translator, director the same
  title: 'The Crisis Years: Kennedy and Khrushchev, 1960–1963'
  year: '1991'
  n: Interviews with nearly everyone.    # the card note
  tags: [topic:berlin]
```

- Editions, translations and chapters are cards of their own. A chapter or a volume points to its container (`in:`)
  and takes from it what it lacks; a correction to the container changes every chapter. The short form of a
  multi-volume work is Bluebook's ("Logevall, Title, 2 CHVW 123"). `edition_of:` and `translates:` join an edition or a
  translation to its original.
- Under a person's subject line the author it names is not repeated (the citation starts at the title); `byline:
  true` (or `byline: [w.…]`, some of several) keeps it. A listing of several works naming their author at the first
  only writes `ditto: true`.
- Queries (`./bib works list`): `-t` every one of, `--any` at least one of, `--not` none of. Stored tags pass down from
  a container to what is in it. Worked out for every card: `in:kja`, `section:vn.II.C.1`, `author:logevall`,
  `year:1991`, `pub:1990s`, `kind:film`, `form:verbatim`; `in:` alone is any list, `section:vn.II.C*` a prefix.
- Periodicals by the Bluebook's abbreviations, the 21st edition's where the Indigo Book differs ("Int'l Sec." for
  *International Security*: the Bluebook abbreviates "Security" and "Securities" both "Sec."). A dissertation's or
  thesis's title in roman, as any unpublished work's (`kind: thesis`, verbatim, no italics). STYLE 7 and 8 in
  `tools/bib/works.py`.
- No publisher in a citation, as Bluebook's: "(2007)", not "(University of North Carolina Press, 2007)"; a work
  published before 1900 keeps its place of publication and its publisher ("(Venice, Vitale Mascardi 1665)"); a
  publisher's edition named as such ("Random House ed. 1966") and a film's network stay. A count of volumes after the
  title: "*Reporting Vietnam*, 2 vols. (1998)". STYLE 5 and 6 in `tools/bib/works.py`; `check` warns [publisher].
- Change a card with `./bib works set ID FIELD=VALUE` or by hand; tag it with `./bib works tag ID +TAG`. To fix a
  citation, fix the card, not the listing: a listing's `c` written over cuts its pointer.
- `check` fails on a pointer to no card, a card neither structured nor verbatim, an `in` that comes round to itself;
  warns on a card nothing points to and on a work cited as text (`./bib works adopt`).
- `notes/works-inventory.md` (`./bib works inventory`): the works written differently that are probably one, the
  editions, the works listed in several places with differing notes, the calendar's citations, suspected errors.
  `tools/works/make_cards.py` made the catalogue from the lists, once (Oct. 13, 2026), and `make_chapters.py` the
  chapters and their volumes (34 chapters, 28 volumes); don't rerun either.
- Not yet in the catalogue: primary documents (cases, laws, orders, hearings, speeches), periodicals as such
  (newspapers, the *Pa. Manual*; the *Department of State Bulletin* excepted, `w.department-of-state-bulletin`, `kind:
  periodical`, cited with its issue and page linked, "[[w.department-of-state-bulletin]], [July 9, 1962, 64](…)"; and
  *American Foreign Policy: Current Documents*, a card a year, `w.current-documents-1956` … `-1967`), and a few works the calendar names in passing ("translated as *The Feast of the
  Goat*"). One-time scripts, Oct. 13, 2026 (don't rerun): `tools/works/convert_calendar.py` turned the calendar's
  short citations into pointers (2,287, with a second pass for several titles under one author, "and", a bare
  surname, a chapter); `adopt_calendar.py` made cards of the 85 works the calendar cited in full and found nowhere
  else, and pointed those citations (and their "see [[…]]" short forms) at them; `merge_duplicates.py` folded 80
  cards into the work they repeat (one first author, main title and year).
- A work on two cards: `./bib works combine KEEP DROP` (works.combine): DROP's id stays an alias, listings and
  `[[w.…]]` links follow, the notes are joined (a bare "Also …" pointer to a list now holding the card gives way).
- The A–Z bibliography, `build/works.html` (`./bib build works`; `tools/bib/bibliography.py`, its STYLE notes): every
  card, A to Z, built beside the themed lists, which stay until it replaces their Parts I–II (Part III stays). Filed
  by the first-listed author's surname; a film under its director's; an organization only where the card names it as
  the author (cards are not edited to add one); a compilation of one writer's texts under the writer (`files_under`:
  Ladejinsky's *Selected Papers*, Walinsky ed.; the Public Papers and the edited White House tapes under each
  President, though many speak in them); recordings and records of talks under the one or few named persons they
  record (the Abrams tapes under Abrams, *The Kissinger Transcripts* under Kissinger), not a study that draws on
  them, nor a film cut from them (a film files as a film: *The Lady Bird Diaries* under Porter); otherwise the short title,
  its leading article and subtitle dropped (edited volumes included), the heading in italics; then the year; then the
  short title (FILING in `tools/bib/works.py`; `./bib works list` sorts the same way). A work is entered again, a ghost,
  under its other authors, the writer it was written "with", its editors and translators, and any name in `also_under`
  (Cincinnatus [Cecil B. Currey] under Currey): its citation in the muted gray, the whole of it a link to the work's own
  entry, not underlined, and nothing more (no "Filed under"; the owner's ruling, Oct. 20, 2026). One person written two ways is one heading: by
  the marks alone (Andrade, Andradé) under the marked form; otherwise by `SAME` (William Colby, William E. Colby); each
  citation keeps its card's form. An author's works under the name, inverted ("Beschloss, Michael R."; a particle with the surname, "De Palma,
  Brian"; a Vietnamese, Chinese or Japanese name in its own order, as written; `OWN_ORDER`, `RUNNING`, `SURNAME` for
  what the rules cannot tell), linked to the name entry where one person fits; a work without an author under its
  title as the heading; a leading article dropped, another language's too (*La Guerre du Vietnam* under G); a title
  beginning with a number under the number spelled out ("The 30-Year War" under T). Each work's full citation, its
  author in running order, nothing indented; no notes on this page; a book's, a film's or an edited collection's title in
  plain roman, an article's or a chapter's title in italics, its journal or collection in roman (Bluebook's small caps
  tried and set aside), here only; the type of the series' entries (18px, line height
  1.55). After it, on its
  line, muted, no closing stop: the list sections holding it, linked to the listing, and the calendar entries pointing
  to it (`[[w.…]]`, or a short title and list not yet converted), by year. The anchor is the card's id (`works.html#w.beschloss-crisis-years`), lit as a
  roster row is: white, an en dash past it on either side, plain again at a click outside.

## Congress at each opening

The top bar (`nav.pg` in `templates/list.html`) names each page by a glyph, its name on hover and to screen readers (the
owner's request, Oct. 22, 2026): 本 Series, 票 Elections, 長 Executive, 名 Names, 文 Works, 数 Indicators, 図 Indochina
(the Japanese forms, set `lang="ja"` in a Mincho face); the reader's Pages drawer keeps the words. A new top-level page takes a glyph there.

`build/congress.html` is the Elections page (the top bar's 票; the file keeps its name so old links work):
every election, 1958–74, by the Congress it chose, each with the States' elections of the same span placed by date
(the governors chosen that day and the legislatures the election chose, `state_blocks` in `tools/bib/congress.py`; the
odd years' governors after the Congress's roster), then the Congress at its opening and its specials. The Senate
summary of each election ends with the Senate at the opening (`senate_opening` in `tools/bib/elections.py`: the roster,
or for the 86th and 94th `senate_opening` in `elections/facts.yaml`).

`./bib build` also draws each Congress at its opening: party bars (majority and
two-thirds lines), a House map by district, a Senate map by state, and rosters
by state with pointers to Part III and the calendar entries that name each
member. All seven are on `build/congress.html`. A calendar entry tagged
`congress:<NN>` carries that Congress's block in the calendar's pages and the reader;
now the openings of the 87th to the 91st (Jan. 3, 1961, to Jan. 3, 1969).

The rosters come from unitedstates/congress-legislators by
`tools/congress/make_rosters.py`, which holds the hand corrections (seats vacant
at the opening, terms missing from the source, notes). Fix a member there and
rerun it, or edit `congress/<NN>.yaml` directly for a one-off. The shapes come
from Lewis et al.'s district files by `tools/congress/make_geo.py` (needs
shapely and pyproj; the build does not), for the 85th to the 94th Congress (the
elections need the districts before and after), simplified twice: at 0.01 map units,
fine enough for a single Manhattan district, and at 0.12 for the full map; 12 MB
together, with a point for the District of Columbia. The shapes are not in the pages (the owner's ruling, Oct. 16, 2026):
the build writes them beside the pages, `build/geo/base-<hash>.json` (the coarse shapes, the State outlines, each
Congress's districts; 2.6 MB) and `fine-<hash>.json` (9.8 MB), shared by every page with a map (`geo_files` in
`tools/bib/congress.py`); a page fetches the coarse when its first map nears the screen and the fine when a map is first
zoomed past 3× (`FINE` in `templates/congress.html`). Fetched, not read from disk: open the pages through a server
(`python3 -m http.server` in `build/`), not as files. Each map is drawn when it nears the
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
the two-letter postal codes. Each map has three types, in the toggle under it: the map (Districts, States), the dots
(Delegations, Senators) and the Chamber (the owner's request, Oct. 20, 2026): a semicircle, a dot a seat, the
Democrats and those caucusing with them on the left, the Republicans and theirs on the right, each side from its end
to the middle by the margin of the race that seated each member, the narrowest in the middle, those not elected to
the seat (appointed) at the ends, filled in a snake (STYLE 12 in `tools/bib/elections.py`; `hemi`, `chamberOrder`
in the template). One switch above the maps colors all three: Party (the default), Result (held or picked up) and
Margin, the last two of the race that seated each (`seat_figures` in `tools/bib/seatlinks.py`), gray where he was not
elected to the seat or the race has no figures. The bars split the Democrats, non-Southern then Southern:
the eleven Southern States, the thirteen represented in the Confederate States
Congress less Missouri and Kentucky.

Notes under a member in the rosters at the opening give the seat's later changes: the
departure and its date, the successor and party, the date elected (linked to the special's
row) and the date seated (`congress/changes.yaml`, made by `tools/congress/make_changes.py`
from Wikipedia's Congress pages, "Changes in membership"; check a date against the
Biographical Directory where it matters), and a change of party in office, with its date
(`congress/switches.yaml`, by hand: Thurmond, Watson, Byrd Jr., Reid, Riegle).

## Leaders and committees

`congress/committees.yaml`, written once by `tools/congress/make_committees.py` from Garrison Nelson's committee files
on Charles Stewart III's data page (House `hrc8097.mit`, Senate `snc80102.mit`, codebook `cb9999`; never edit the
output): for the 87th to the 93rd Congress, each chamber's standing committees, their members in Nelson's order (by
side, the *Journals*' listing at the first session by rank, then the additions to an enlarged committee and the
replacements by date of assignment), the chairmen and ranking minority members, the dates of assignment and of
leaving and why; the leaders; and each roster member's whole years in the chamber at the opening (congress-legislators'
terms). Members join the rosters by ICPSR id through unitedstates/congress-legislators (the rosters' source). Its
`committees:` list (Nelson's code, chamber, the name the *Congressional Directory* prints, the Congresses it has
members in) is the series' committee list: the hearings calendar (daybook/committees/) keys to it. Nelson's files for
these Congresses hold the standing committees only (no select, special or joint committee, no subcommittee), and
code only the Senate's floor leaders and whips (code 620); the House's leaders (Speaker, floor leaders, whips, caucus
and conference chairmen) and the Senate's President pro tempore and conference chairmen are in
`congress/committees-hand.yaml`, read from the House's and the Senate's own lists (its `sources`), each change dated
as the list dates it, and the script stops where Nelson's Senate leaders differ from the Senate's lists. The hand file
also holds an ICPSR id congress-legislators carries differently (Kenneth J. Gray) and any row correction, each with its
reason. Rerun the script after changing the hand file (it needs the Nelson files and a congress-legislators checkout;
the build does not).

`tools/bib/committee_rosters.py` renders them (STYLE notes at the top): on `congress.html`, under each Congress at its
opening, "Leadership" (a table a chamber: office, holder linked to his name entry and roster row, party, the dated
changes) and "Committees" (a collapsible table a chamber, a tbody a committee anchored `cm<NN>-<h|s>-<code>`: the
ratio, chairman and ranking member, Democrats and Republicans side by side in rank order, each linked to his name entry
and his roster row, the changes with their dates); in each roster row, a column "Yrs" (years in the chamber at the
opening) and a muted line of his committees and rank; in each Names entry, "Committees" across the Congresses ("House
Ways and Means: 1st (chairman), 87th–93rd Cong."). A calendar entry tagged `committees:<NN>` carries the Leadership
and Committees blocks, as `congress:<NN>` carries the roster (now the five openings, 87th-91st). `check` fails on
ranks not consecutive within side and group, a member who is neither in the roster at the opening nor his seat's
successor in `congress/changes.yaml`, a leader not in the roster, a code not in the list; warns on a committee with no
chairman and a leader with no name entry [committee-rosters].

The select, special and joint committees, and the subcommittees (`tools/bib/committee_more.py`, its STYLE notes):

- `congress/committees-cdir.yaml`, written by `tools/congress/make_cdir_committees.py` (its RULES) from each Congress's
  first-session *Congressional Directory* on govinfo (Apr. 1, 1961 to Mar. 10, 1973), read page by page from the scan's
  OCR (`pdftotext -layout`): the Senate's and the House's select and special committees and the joint committees (not
  the party committees, the House's housekeeping committees, the commissions and boards), each member in the order
  printed with his role (chairman, vice chairman, cochairman), joined to the rosters by surname, chamber and State;
  the party is the roster's (the Directory prints none in these lists); the printed page of each committee, linked to
  the PDF at its page. A committee created later in the Congress (the House's Select Committee on Government
  Research, 1963) from the second-session edition. 28 committees, 1,319 places, 87th–93rd. Their codes are the hearings
  calendar's (`code_of` in `tools/daybook/make_committees.py`: `j.atomic-energy`, `s.special-committee-on-aging`), and
  they join the committee list (`committee_rosters.names`), so the hearings' rows link to them; so do, by name alone,
  the committees the Digest holds and no Directory read lists (`DIGEST_ONLY`: the Senate's Select Committee on National
  Water Resources, the House's on Export Control) and a lead too garbled to name one (`<ch>.unread`, "committee (name
  unread)", make_committees.py STYLE 7).
- Subcommittees: the *Directory* prints none in any edition from 1961 to Mar. 1971, and from Dec. 3, 1971 only each
  one's chairman and ranking minority member. `congress/subcommittees.yaml`, written by
  `tools/congress/make_subcommittees.py` (its RULES), comes from the *Congressional Staff Directory* (Brownson; the
  1961, 1963 and 1971 editions, the Digital Library of India's scans on archive.org, read by their OCR): every standing,
  select and joint committee's subcommittees, their chairmen and members by surname, each matched to his committee's
  members, the printed counts held against the names read, each name and page linked to the leaf. 87th, 88th and
  92nd only: the 1965, 1967 and 1969 editions were not found open (`notes/leads.md`; searched again Oct. 23, 2026).
  726 subcommittees, about 6,500 places (the 92nd's 267 and 2,641, added Oct. 23, 2026); what the rules could not settle (a count not met, a name unread) is the subcommittee's `check`, shown muted.
- Rendered after the standing committees, under each Congress on `congress.html` and in the calendar's
  `committees:<NN>` blocks, each folded and closed: "Senate (House) select and special committees", "Joint
  committees" (two columns, a tbody a committee, anchored `cm<NN>-<s|h|j>-<code>`), and "Senate (House) subcommittees",
  "Joint committees' subcommittees" (one column of text, a row a subcommittee, anchored `sc<NN>-<ch>-<code>-<n>`, so
  nothing is wider than the column at 400px); a Congress with none read says so. A member's roster line goes on with
  his select, special and joint committees; his Names entry's "Committees" with them and his subcommittees, a Congress
  an item. `check` fails on a code not in the list, a committee without members, a subcommittee without its committee
  or page; warns on a member not joined and on the hearings' committees the list lacks [committee-more].

## The Executive Branch

`./bib build` writes `build/executive.html`: the Executive Branch at each inauguration (1953, 1957, 1961,
1965, 1969, 1973) and at the successions of Nov. 22, 1963, and Aug. 9, 1974, with every change during each
term, through Aug. 31, 1974. A calendar entry tagged `executive:<YYYY-MM-DD>` (a term's first day) carries
that term's block in the calendar's pages and the reader; now Jan. 6, 1960 (the 1957 term, at the calendar's opening), Jan. 20, 1961, Nov. 22, 1963, Jan. 20, 1965, and Jan. 20, 1969. The calendar's copy is
slimmer (`cal_block`, CAL STYLE in `tools/bib/executive.py`): in full, with every holder but no law and no notes, the
President, the Cabinet (the Vice President, the department heads, the Representative to the UN), the Chairman of the
Federal Reserve, the Chairman of the Joint Chiefs, the Director of the FBI, and the Special Counsel, Press Secretary,
Secretary to the President, Military Representative, Personal Secretary, CEA Chairman and Special Assistant for National
Security Affairs, and the Director of Central Intelligence, the Budget Director, the science adviser, the trade
representative, the Directors of the USIA and the Peace Corps (`CAL_FULL`), each holder's pointers under his line, no
column of them; by title alone, linked to executive.html, an office beside a named office of its own unit, answering to
the same officer (`cal_beside`: Staff Secretary beside the Appointments Secretary), never one beneath a named office; an
entity with no named office, by its name alone, beside a named entity under the same department (`cal_entity`: the ICA
beside the Peace Corps and the missions; the services, commands and defense agencies beside the Joint Chiefs), or in the
Executive Office (the foreign intelligence board, Civil and Defense Mobilization, the Space Council). Every row flush. Not shown: the White House's special
assistants (`CAL_OUT`). The Agencies and commissions one link, the Federal Reserve, the CIA, the USIA under it; the parts
in centered small capitals; the units open, not collapsible. Each office's rows are a `tbody`
carrying its anchor, on both pages, so a link lights the holders and the Before/After row, not the law or the note.

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
  `FRUS 1961–63, IX, doc. 144`, `Wikipedia: Title`, `APP[ YYYY-MM-DD]` (shown as the Public Papers' items of that day
  that name the holder, where APP's documents match them; an APP address likewise: `ppp_on_day`, `url_html` in
  `tools/bib/executive_sources.py`), `Federal Register, Jan. 20, 1953`,
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
The scroll wheel and the Outline drawer give each entry's full name; the top bar its surname (`data-crumb`). The index
and each letter's page carry the A–Z bar, the letters at 1rem, 0.36em apart (STYLE 7 in
`tools/bib/lives.py`); each letter's page opens with the index's opening paragraphs, its count of persons, and the index's list for its
letter, linked to the entries below.
A Part III entry for two people writes them apart with ";" (`s: Evans, Rowland, Jr.; Novak, Robert D.`), never "&".
A name written in its own order, without a comma (Mao Zedong, Ngô Đình Diệm, Souphanouvong, U Thant, Malcolm X), is a
person too (`natural`): the whole name stands as the surname, and its other forms (romanizations, the forms FRUS lists
and the Public Papers use: Mao Tse-tung, "Diem, Ngo Dinh", President Diem) are in `sources/name-forms.yaml`, kept by
hand; FRUS and APP find the person by those. A Part III entry for a group (Wise Men, Chicago defendants) is tagged
`group` and has no name entry. A person the calendar names who fits no other Part III section goes in K–J Cong. III.K,
"Others named in the calendar".

Names link to their entries throughout (`tools/bib/namelinks.py`), muted: class `nm`, the text's own color and
a faint underline. Linked: the calendar's "Names:" (by the entry's `name:` tags and the name index), Part III subjects, the
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
father written bare and a son with "Jr." stay two (a work's author written with "Jr." is never linked to, or listed
under, a man without it: James Lawton Collins, Jr. is not J. Lawton Collins; Harry F. Byrd; Barry M. Goldwater; a son `strict` in
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
person, "Testimony before Congress" (the committee meetings the Daily Digest names him a witness at, the sure matches
only: `testimony` in `tools/bib/committees.py`), and the White House recordings PRDE lists him speaking on
(`recording_speakers`: PRDE's "Sr." and "II" are the
bare name; its "Jr." takes a bare form only where none carries "Jr." and the son is not `strict`; not in a President's
own entry). Empty sections are left out, the Life too. The FRUS and presidential lists are bulleted, a little space between items
(`lvnb`) and between the presidential documents under each year (`lvad`), and no more between years; a presidential
document is cited by its item in the Public Papers ("1961 Pub. Papers 1", linked to the page in GPO's volume) where one
matches, else "APP" (below, "The Public Papers"). "In the series"
leaves out the pointer the role line already gives (and is left out where that was its only one). Rules (the STYLE notes in `tools/bib/lives.py`):

- Each fact cites its ground source, linked: BD (the 2005 printed Biographical Directory, by page), the roster
  holder's own sources (CDir., CR, FR, DSB, GOM, POCOM, APP …), the Clerk's *Election Statistics* by page, a calendar
  entry's own sources. The series' pages are pointers, not sources: Exec. 1965, 87th, 88th Cong., Election 1960,
  Cal. Jan. 3, 1961, list sections — in the headings' sans serif, not underlined.
- A run of sentences with the same sources and pointers is a sentence block; its source block follows it: the
  cites, then the pointers. Each sentence block is a paragraph; a new one also at each office and election, and at
  each calendar entry, where the sources run on.
- An office is followed by the offices held ex officio by virtue of it, with their dates only where they differ.
- The Directory's text in the series' forms (`bd_style`): the States as the Bluebook abbreviates them (T12.1 of the
  Indigo Book, https://law.resource.org/pub/us/code/blue/IndigoBook.html: N.D., S.D., Cal., Kan., Neb., Or., N.M., W.
  Va., Wis.), spans with an en dash ("January 3, 1971–present"). A short form of a first name ("Sam" for "Samuel
  William") takes the Directory's entry of a man the rosters lack only where two words of his offices agree with it.
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
sources/people-apart.yaml     kept by hand: two names the rules would join that are two persons (Robert Moses the builder,
                              Robert P. Moses of SNCC), each pair with its reason; `check` fails on a name no source writes
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
carries its race's table (the 86th's six of 1960, the 87th's thirteen, the 88th's of 1963–64, the 89th's of 1965–66, and the 90th's of 1967–68, thread "Special elections"). Definitions: the STYLE
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

## National conventions

`elections/conventions.yaml`, kept by hand (header there: the schema), one block a convention (`1968-R`): the Call's
apportionment, State by State, from the convention's *Official Report of the Proceedings*; how and when each delegation
was chosen, from the source its `methods` names, with that source's Check; and the roll calls as the Proceedings
tabulate them. `tools/bib/conventions.py` renders them (STYLE notes there); `drawQ` in `templates/congress.html` draws
the maps, as for the primaries.

- A calendar entry tagged `conventions:<YYYY>-<R|D>` (the opening, beside `primaries:`) carries the delegations: a
  summary, a map by how chosen (primary; the districts in a primary, at large otherwise; district and State
  conventions; a State convention; a State committee; not found), a map by the first-ballot leader, and the table
  (each delegation's first-ballot vote, its votes, the Call's at large and districts, the bodies and dates of
  choosing, a primary's date linked to its day). Its `gloss` sets out the Call's formula, quoted and cited by page.
- An entry tagged `rollcall:<YYYY>-<R|D>-<ballot>` (the nomination) carries that roll call by State: the first
  tabulation, the final where the delegations changed their votes after the roll, the Proceedings' starred notes,
  the printed totals. Now Miami Beach, 1968: `pres1` (Aug. 7) and `vp` (Aug. 8). No procedural roll call was taken
  there: the credentials report and the platform went by voice vote.
- `check` fails where the Call's at large and districts do not make a State's votes, the States do not add to the
  Call's total, a State's ballot does not add to its votes, or the columns do not add to the printed totals.
- Sources and access: the Republican Proceedings of 1968 open on archive.org (`sim_republican-national-convention-
  proceedings_august-5-8-1968`; 1972 on too); 1964 both parties, Bain and Parris's *Convention Decisions and Voting
  Records*, CQ's *National Party Conventions* and the Senate Library's *Nomination and Election of the President and
  Vice President* (1968) borrow only; 1960 both and Democratic 1968 not found (`notes/leads.md`).
- A convention not yet read keeps only a source's table of how its delegations were chosen (`hughes`): Democratic
  1968, the Hughes Commission's Table I (*The Democratic Choice*, 114 Cong. Rec. 31549, Oct. 14, 1968), each State's
  marks as printed, `check` holding them to the printed column totals. No block until the Call and the roll call are in.

## Governors

`elections/governors.yaml`, written by `tools/elections/make_governors.py` from Wikipedia (needs the network; the build
does not): every general election for governor, 1960–68, odd years included (New Jersey and Virginia, 1961 and 1965;
Kentucky and Mississippi, 1963 and 1967; Louisiana, Mar. 3, 1964, and Feb. 6, 1968). The races and incumbents from Wikipedia's tables of each
year; the figures from each race's article, its election box, with the source the article gives for them (most the
State's canvass or *America Votes*; Our Campaigns, or none, marks Check). What the articles cannot settle is `HAND` in
the script (Georgia, 1966: the legislature elected Maddox; Minnesota, 1962: the recount). Never edit the file by hand.
`tools/bib/governors.py` renders them (STYLE notes there):

- A calendar entry tagged `governors:<YYYY-MM-DD>` carries the day's races (on a November election day, inside the day's
  "Elections of" block, the entry pointing to it): a summary (races, wins, each party's
  gains, the governorships after), a map (Result: the winner's party, dark where it took the office; Margin: the
  election maps' quantile rule), and the table, one race a `tbody`: the candidates with votes and shares, the margin,
  and under them the note (the incumbent and his fate, the hold or gain, the source). Now Nov. 8, 1960, Nov. 6, 1962,
  Nov. 3, 1964, Nov. 8, 1966, Nov. 7, 1967, Feb. 6, 1968 (Louisiana) and Nov. 5, 1968 (thread "Governors"); the other odd years' races are entries of their own.
- Names: each race a row in the candidate's record (`governor_rows` in `tools/bib/lives.py`), the date linked to the
  day's table.
- The primaries for governor are calendar entries (thread "Governors"), their figures cited in each entry.
- The bars on re-election (the owner's request, Oct. 23, 2026: "the authority and reason for the bar, and its scope"):
  `elections/term-limits.yaml`, kept by hand (header the schema), a State an entry for each State whose incumbent
  was barred, 1960-68: each provision in force over the span (cite, words, scope, from and to), each read by page
  (Thorpe's *Federal and State Constitutions* of 1909 for the old texts, the States' manuals, session laws, codes and
  election returns for the rest), the changes since, the text today, and a Check for what is not settled. A race
  the tables call "term-limited" shows "barred from another term (Mo. Const. art. IV, § 17 (1945, amended 1965): not
  eligible for election as his own successor)", the cite linked, and the rule's Check (STYLE 9 in
  `tools/bib/governors.py`; `tools/bib/termlimits.py`, its STYLE). `check` fails on a barred race with no provision,
  a rule without its words, scope or a linked source, a span out of order.

## Legislatures

`elections/legislatures.yaml`, written by `tools/elections/make_legislatures.py` from Carl Klarner's State Partisan
Balance Data (Harvard Dataverse; the seats compiled from the *Book of the States* and the States' manuals; never edit):
each State's Senate and House by session, 1959–69, as in session (Democrats, Republicans, others, vacancies), the
proportion needed to override the governor's veto (the 1956 provisions) and the governor's party. `HAND` in the script
for what the data cannot say (North Carolina's governor had no veto; Minnesota's and Nebraska's nonpartisan
legislatures); `HAND_YEAR` a Check (Kansas, 1967). `tools/bib/legislatures.py` renders them (STYLE notes there):

- A calendar entry tagged `legislatures:<YYYY>` (the year the session met: 1961 for the legislatures chosen in Nov.
  1960) carries the session's map and table: a party's color where it holds both chambers, light for a majority,
  middle for the State's override proportion where that lies between a majority and two-thirds, dark for two-thirds
  of both (the Presentment Clause's and Article V's proportion); divided gray; Nebraska's nonpartisan chamber ivory
  (`--pNP`, the owner's request, Oct. 23, 2026). Now the
  five "legislatures-us" entries of Nov. 1960, 1962, 1964, 1966 and 1968.
- Article V's analogue is drawn at the federal two-thirds for every State: each State's own rule for proposing an
  amendment (the vote, the sessions) is not yet in the data; the *Book of the States*, 1960–67, prints it.

## State finance

`statefin/states.yaml`, written by `tools/statefin/make_statefin.py` from the Census Bureau's historical finance databases
(the figures its annual *State Government Finances* printed; Access files read with mdbtools; the build needs no network;
never edit): each State government, D.C.'s exhibit and the U.S. total by Census's fiscal year, 1959–68 (revenue, five
taxes, federal aid, expenditure by character, aid to local governments, long-term debt, population, personal income);
the State and its local governments together (`local`); the 43 large cities in the census years 1962 and 1967
(`cities`); and each year's printed report, its tables and first pages (`reports`, kept in the script). `tools/bib/statefin.py`
renders them (STYLE notes there):

- A calendar entry tagged `statefin:<YYYY>` carries that fiscal year's block: a summary, a map of the taxes in force
  (general sales and individual income, either, neither; the year's adopters in the full color) and a quantile map of
  taxes per $1,000 of personal income, then, folded, the State governments' tables (taxes: per $1,000 and a head, five
  shares; revenue, expenditure and debt), the State and local governments together, and in 1962 and 1967 the large
  cities; the caveats (Census's classification, not the States' budgets; fiscal years differ); the database and the
  report cited by table and page. Now the nine "state-and-city-finance-us" entries of June 30, 1960–68 (thread "State
  and city finance").
- Taxes per $1,000 of personal income take the calendar year before, as Census's tables do, with BEA's revised figures
  as the database carries them; the regime follows Census's columns (any revenue from the tax). The acts are calendar
  entries of their own, dated by the session laws.

## Rosters and elections, linked

`tools/bib/seatlinks.py`. Under each member at an opening, a muted line: the election that seated him ("Elected Nov. 8,
1960"; "Seat filled Nov. 4, 1958 (Kennedy)" where he did not win the seat's last election, as an appointed Senator;
1956 unlinked, having no block) and the seat's next ("Next: Nov. 6, 1962"; a special first, where one filled the
seat; for the House, his own race that November where one race in his State names him, else the same number's).
Under each race and special, "Roster: 87th Cong.", the seat's row at the next opening that has a roster. Under the
presidential vote, "Took office", the President and Vice President in the Executive roster at the next inauguration.
A row highlighted as a link's target (any roster or election table) is white, as a lit thread is (`--tgt` in
`templates/roster.css`), an en dash past the table on either side (side shadows of the outer cells, `--dash`), and goes plain when the reader clicks outside it (`JS` in `tools/bib/roster.py`; `.unhl`). Tables write an at-large seat "AL" and leave the district column unheaded; a fusion candidacy's parties abbreviated ("D, R");
a whole vote "100%".

## Elections

Every general election from 1956 to 1974, in `elections/<year>.yaml`: the House and Senate race by
race, and in presidential years the vote for President by State with the electoral votes as cast.
1956 is a base for swing and is not shown. `build/congress.html` puts each election from 1958 to
1974 before the Congress it chose (the 86th and 94th have no rosters); a calendar entry tagged
`election:<year>` carries its block too (now every November election, 1960–68). A block: the electoral and popular vote
first, then by chamber the seats won, the net change from the close of the last Congress, pickups,
and new members; one view switch for every map (Result; Party, the parties' flat colors; Margin, the winner's lead over the runner-up in points of all the votes, by the quantile rule; Swing, continuous); the
President's map above the House and Senate, with a States | Electors | Chamber switch (Electors: a dot an elector, as voted); the Senate map with a Senators toggle (a dot a seat, larger than the House's: `PB`, `RB`); a Chamber under every map but the specials' (a semicircle, a dot a seat or an elector as cast; the Democrats and their allies left, the Republicans and theirs right, a third ticket between; each side from its end in by margin, the narrowest in the middle, the Senate's seats not at stake gray at the ends; filled in a snake whose midpoint is the middle dot on the center line; a faithless or unpledged elector by his vote, in its color; its Result held and picked up, the President's too: STYLE 12 in `tools/bib/elections.py`); and every race in tables (the candidate first, in bold where he won, his party under or after him; under 520px the share
under the count and the note on a line of its own):
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
  (clerk.house.gov), OCR'd; the OCR's misread party labels and names put right by `tools/elections/labels.py`. Each figure is read three times and settled against the
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
- The partisan voting index (the owner, Oct. 28, 2026: "If we can calculate the CD numbers, we should take the extension
  off the shelf"): the States' from these returns, the districts' from the Census's
  *Congressional District Data Books*, read by page into `elections/readings/districts/` (1952-60 on the 87th, 88th
  and 89th Congresses' lines; 1968 on the 93d's), each district row held to its State column and each State column set
  against these returns (`vs_clerk`); `python3 -I tools/elections/make_pvi.py` (its STYLE; `check` [pvi],
  `tools/bib/pvi.py`). The 1960, 1962 and 1964 House elections have district PVIs (419, 321, 302); the later ones wait
  on 1964 and 1972 by district (the memo, notes/extensions/memos/pvi-districts.md). Shown (the owner, Oct. 28, 2026:
  "Show both. Be sure to cite and attribute"), in each election's block and the calendar's `election:` entries: the
  index under each race's seat (the district's; a Senate race and the President's table, the State's), a map view
  "PVI", and, folded under the race tables, the States' and the districts' indexes with their inputs and the vote by
  district as each Data Book prints it, every table citing its volume by page and naming the compilers the Census
  names (the Republican Congressional Committee, CQ, *America Votes*, the NRCC); the vote taken as fact, not CQ's
  selection or arrangement (*Feist*): STYLE 3-5 in `tools/bib/pvi.py`.
- Hand facts (who caucused with whom, electors who broke, the 1960 unpledged slates, the
  Alabama reckonings) live in `elections/facts.yaml`, not in code. A third-party member
  missing from `caucus:` fails `check`.
- To add or correct an election, follow the loop in the docstring of `tools/elections/review.py`:
  `make_elections.py YEAR --cache DIR`; `review.py left` and `sheets`/`pages`; readers with
  `review/READER.md`; `review.py verify`, then `merge`; rerun `make_elections.py` (it should
  leave nothing); `review.py audit YEAR`; `./bib check`; then tag the calendar entry.
- Colors are tokens at the top of `templates/congress.html` (its CSS is in commented
  sections); the parties' are the *New York Times*'s election colors (the owner's choice, Oct. 22, 2026: #1375B7, #C93135). Result: four steps a side (`--eR1`–`--eR4`, `--eB1`–`--eB4`).
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
- The probe reads the page, not the proxy (Oct. 23, 2026): the proxy's "200 Connection Established" is no status (it
  once made a failed TLS handshake read as open); a 200 carrying a challenge (Anubis, Turnstile, Imperva, AWS WAF) is
  `bot-check`; a TLS failure, a firewall's "Request Rejected" and a proxy 502 are `other`. Google Books lines are kept
  by hand, as `borrow` is (their preview). A failure is retried an hour later before it goes in the register. A site
  that sends the wrong intermediate certificate ("unable to get local issuer certificate") is read with the issuer its
  certificate names (its AIA), added to the system's roots, as a browser does: verified, not bypassed (`aia_bundle` in
  `tools/sources/check_access.py`; Alaska's elections site, whose returns of 1960–74 are open so).
- The States' session laws and journals, where a lead needs an act's day: Alabama's *Acts* and both Journals, 1961–70,
  every session, and Kentucky's Journals, 1959–68, are on archive.org (`alabama-acts-1966`, `jsencoky1960`); the
  revisors' sites give Idaho's, Minnesota's (with the vetoes, lrl.mn.gov), Nevada's (leg.state.nv.us/Statutes) and
  Washington's session laws; Texas's, the Legislative Reference Library (its bill search names the chapter); Missouri's
  *Laws* and Journals, Missouri Digital Heritage's CONTENTdm (`molaws`, full text by `dmQuery`).
- Kansas's *Election Statistics*, 1899–2010, every issue, are in the State Library's KGI Online Library (CONTENTdm,
  `p16884coll129/83`); Washington's statewide figures, 1898–2006, in the Secretary of State's archive workbook; a
  State library's CONTENTdm is searched by its API (`dmQuery`, `dmGetCompoundObjectInfo`), its pages being scripts.
- The basis of belief (the owner's request, Oct. 23, 2026: "note the basis for your belief that a named source exists";
  "a (then-effective) law or regulation obliging a person to create a record, to preserve it, to transfer it, to hold
  or keep it, to publish it ... would probably be the best authorities"): every publication, archival series and county
  or city record (`local`) carries `basis`, one ground a line, `seen` (a copy read), `catalog` (a catalog or finding-aid
  record, not the text), `law` (the provision obliging an officer to make, keep, transfer or publish it, as then in
  force where found, read or only cited by the publication), `cited` (a source naming it), `assumed` (no ground yet:
  what was searched); and `cited_as`, the patterns by which the series' files cite it. `check` fails on an item
  without a basis or with a ground outside the legend [sources].
- The listing (the owner's request, the same day: "Make it a .MD and link it in the readme"): `notes/state-sources.md`,
  written by `python3 tools/sources/make_listing.py` (deterministic; its STYLE notes): a section a State, each item's
  editions, contents, copies with access and checked date (open; closed; paper only), basis, and what the series has
  used it for, by its `cited_as` and its copies' addresses; then the Check pointers to State records in the calendar,
  the specials, the governors' races and the readings, each ruled *found* (it names an item with a ground), *assumed*
  (the item named has none) or *unmatched*. So "Check: the State canvass" or a pointer to the State archives says
  there whether it names a source found, and where, or an assumption. Rerun after every change to the register;
  `check` warns when either listing is stale [state-sources], and on a register title with a hyphen in a span of years.
- The law register (the owner's request, Oct. 23, 2026: "create and maintain a similar listing for sourcing State
  constitutions and laws ... take care for the legal authority for the recording, compilation, and publication of the
  constitution and the laws. Identified authority is strongly preferred"): `sources/state-law.yaml` (its header the
  schema), every State and D.C., 1959-69, at least the session laws: each item's title (the volume's own words where
  read), officer, `authority` (the law, as then in force where found, with where it was read, or only where it is
  cited) or `authority_searched` (what was searched; one or the other always), basis, `cited_as`, and copies tested
  from here (HathiTrust's records verified by its Bib API, their pages bot-checked). Listed in
  `notes/state-law-sources.md` by the same script (`tools/sources/law_listing.py`), with the calendar's Check
  pointers to a State's laws or journals; checked by `tools/bib/state_law.py` [state-law]; access rechecked by
  `python3 tools/sources/check_access.py --law`. Readable law of the period found so far: Minnesota Statutes 1961
  (the Revisor's site), the Code of Laws of South Carolina 1952 and its 1960 supplement, the Revised Codes of Montana
  1947 and the Election Laws of Montana (archive.org), the United States Code of 1964 (the Library of Congress's
  scans), the constitutions as the 1960s blue books print them (California's in the Statutes, North Carolina's,
  Pennsylvania's, Connecticut's).

## Economic indicators

`./bib build` puts a table at the head of each calendar month: the figures that
report on that month, filed by the period they cover, not the date they were
issued (quarters in the quarter's last month, fiscal years in June, calendar
years in December). Each row has the figure as
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
tools/indicators/make_oil.py  the Oil group (oil-*.yaml): the Survey of Current Business's monthly figures, read by eye (SCB in
                              the script), and the Minerals Yearbook's reserves, beside EIA's today (needs the network, xlrd)
tools/bib/oil.py              renders the Oil cells and the Oil table, and checks them (STYLE notes at the top)
tools/bib/oilworld.py         the world's oil a year and the posted prices of crude, from sources/oil-world.yaml (kept by
                              hand; tags oilworld:<YYYY>, oilprice:ras-tanura; STYLE notes at the top)
tools/indicators/make_war.py  The war (war-deaths.yaml, war-strength.yaml) and sources/war-dead-states.yaml: NARA's DCAS file
                              counted, the figures printed then read by hand (THEN_* in the script; needs the network once)
tools/indicators/make_war_forces.py  the enemy and the allies (war-enemy-*.yaml, war-infiltration, war-rvnaf-*, war-fwmaf-
                              strength): every figure read by eye off Thayer, Collins, Larsen and FRUS, by page, in the script
tools/indicators/make_war_air.py  the air war (war-air-attack.yaml, war-air-nvn-rp.yaml): attack sorties by country, as OSD's
                              Report printed them (Thayer, vol. 5, THEN in the script) and as NARA's CACTA file counts them
                              (--count reads every month over the network into sources/war-air-cacta.json; the build does not)
tools/bib/warair.py           the air war rows' checks (STYLE notes at the top)
tools/bib/war.py              renders The war's cells and checks them (STYLE notes at the top)
tools/bib/wartable.py         The war table, under the first Thursday of each month (STYLE notes at the top)
tools/bib/afday.py            the forces tables under Armed Forces Day, the third Saturday in May (STYLE notes at the top)
tools/bib/dayblocks.py        day blocks: a table set under a date in the day layout, not under an entry (its docstring)
tools/bib/wardead.py          the dead by home State per 100,000, a map a year (tag wardead:<YYYY>; STYLE notes at the top)
tools/bib/indicators.py       renders them (ORDER, GROUP) and checks them
indicators/concepts.yaml      the master statement of concepts and sources, kept by hand: a text a series, each piece
                              tagged with the periods it concerns ({{1961..1962-06|...}}; the file's header)
tools/bib/concepts.py         the master page (build/indicators.html) and the calendar's servants (STYLE notes at the top)
```

Concepts and sources (the owner's rule, Oct. 21, 2026; standing): what each series measures, then and today, and
where its figures come from, is written once, in the master, `indicators/concepts.yaml`, each sentence or clause
tagged with the span of reporting periods it concerns; never in a module, a table or a page. Each calendar page
(Cal. I, II, III; the reader's three blocks alike) writes a servant of it right after the month table where a series
first appears on that page (The war's after its own table, under the first Thursday: below): of the series first used there, grouped under the tables' subheadings (Prices,
Employment, Output, Federal finance, Federal debt, International, Oil, The war, Money and credit, Opinion), only the pieces whose
span holds a period that page files for the series; no series the page does not show, nothing about periods
outside it. Each servant ends "See the master entry for a full statement of indicator concepts and sources used in
the series", linked to the master. Every row's name, in every later table on the page, links to its servant
(`#ind-<page>-<series>`); a series with no servant on its page links to the master, and `check` warns
[indicator-servant]. The full tables, every row of every series, then and today, live on the master page,
`build/indicators.html` ("Indicators": the statement by group, then the tables; `./bib build indicators`), listed in
the series index, the README and the top bar (数; at first kept out of the bar, then put in it, the owner's request, Oct. 22, 2026). A new series: its statement goes into the master with its spans;
`check` fails on a series without one, a span it cannot read, or an unknown `{VAR}`.

- ALFRED initial releases: CPI, unemployment, payrolls, industrial production,
  GNP, real GNP; the deflator is GNP over real GNP in the same release.
- Transcribed from the next *Economic Report*, of January (February in 1968), the Reports of Jan. 1962 to Jan. 1969
  (page images on govinfo and FRASER; values and table/page in MANUAL in the script): wholesale prices,
  the administrative and cash budgets (actual through fiscal 1967; the Jan. 1969 Report prints the unified budget
  alone), the unified budget (fiscal 1968 on, its own series), the federal sector of the national
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
- Federal debt and balances (DEBT in the script, `--only debt`; the owner's request, Oct. 20, 2026): the public debt monthly,
  as the *Treasury Bulletin* first printed each month-end and its change (p. 1, then Debt Outstanding, Table 1, from Feb.
  1968), today FRED's GFDEBTN; debt over GNP and net interest over GNP quarterly, each computed within one Economic
  Report (no report printed the ratios); the federal primary balance quarterly (the national accounts' surplus or
  deficit, net lending or borrowing, with net interest added back); and OMB's debt-to-GDP by fiscal year, today's only.
  Today's net interest counts imputed interest on federal pensions: not the 1960s measure (the statement in `indicators/concepts.yaml`). Other numbers worth
  keeping: `notes/extensions/memos/indicators-suggestions.md`.
- Money and credit (`kind: rate`; RATES and DISCOUNT in the script, `--only rates` to write them alone): a table
  of its own between the indicators and the approval table, under the same rule, two columns (Rate | Percent):
  rates are not revised, so one figure each, with its change in points. The federal funds rate, the prime, the
  3-month bill and the 10-year Treasury from FRED; the New York Reserve Bank's discount rate kept by hand from the
  Board's press releases and the *Bulletin* (FRASER, by page): in a month it changed, the Board's announcement and
  the day it took effect in grey; otherwise `since` (the date it took effect, on hover). STYLE 13 in
  `tools/bib/indicators.py`.
- Money, the foreign accounts and the debt's terms (the measures `notes/extensions/memos/indicators-suggestions.md` marked "No";
  `tools/indicators/make_finance.py`, its docstring the sources, each figure with its table and page in READ blocks;
  `tools/bib/finance.py`, its STYLE; indicators STYLE 17). As first printed, read off FRASER's page images: the exchange
  rates (the pound, the mark, the franc: the *Federal Reserve Bulletin*'s "Foreign exchange rates", 1960–68, the issue
  of the month after; one figure, a table of their own, "Exchange rates and gold"); the FHA new-home yield and the
  FHLBB's conventional mortgage rate, contract (Apr. 1963–Jan. 1968) and effective (from Feb. 1967), as rates (the
  *Bulletin*, from July 1964); the debt's computed interest rate (the *Treasury Bulletin*, Debt outstanding, Table 2,
  1960–68) and its average length for 1963–65 (the same, Public debt operations, Table 4). As the next January's
  *Economic Report* tabled them (their first printings not yet read: `notes/leads.md`): the money stock M1 and M1 with
  time deposits, free reserves, reserve assets (gold, currencies, IMF position), the balances on merchandise and on
  goods and services (quarterly, annual rates), the debt's holders (Federal Reserve, trust funds) and its average
  length for 1961–62 and 1966–68. Moody's Aaa and Baa (FRED, rates, one figure). Today: FRED (M1SL/H.6, NFORBRES,
  TRESEGUSM052N, BOPBM and BOPBGS times four); today's M2 and unit labor costs and hourly compensation (nonfarm
  business) as rows of their own, no figure then. Groups: the money stock and free reserves "Money and credit" in the
  indicators table; the public debt, its ratios and the debt's terms "Federal debt". The London gold price has its id
  (`gold-london`) and waits for a source. Rerun: `python3 -I tools/indicators/make_finance.py [--only IDS]`.
- Oil (the owner's request, Oct. 21, 2026; `tools/bib/oil.py`, its STYLE): U.S. crude production and products supplied
  monthly, imports and exports monthly, as the *Survey of Current Business* first printed the Bureau of Mines' figures
  (p. S-35, FRASER, the issue its "Released"), in millions of barrels a day, with the change from the month before and
  a year earlier (percent, day for day; trade, net imports in m b/d; reserves, bn bbl; oil.py STYLE 2); today EIA's
  (products supplied from 1963; trade by year, in December, its own row); proved reserves at Dec. 31, the API's as the
  *Minerals Yearbook* printed them, beside EIA's. The Survey's misprints stand, the correction in grey. A table of its
  own under the month's indicators, without vacant columns (the owner's ruling, Oct. 21, 2026): the rows with both
  figures in four columns, those with one in Indicator | Figure | Reported (oil.py STYLE 5). Today's crude production
  is the Survey's to its rounding in most months: the data, not a bug (the statement says where they differ). Its
  calendar thread: Oil. The world a year (the owner's request, Oct. 22, 2026; `tools/bib/oilworld.py`, its STYLE;
  `sources/oil-world.yaml`, kept by hand): crude production by country, 1960-68, as the Bureau of Mines' *Minerals
  Yearbook* for the year printed it (its world table, by page, archive.org's copies; each year's column held to the
  table's printed totals), in m b/d with the change from the year before as the same table revised it and the share
  of the world; proved reserves by country where the *Oil and Gas Journal*'s year-end table is open (1960, 1961: the
  Journal on archive.org runs June 1959-Dec. 1961 only). No today column: no open series found counts crude by country
  in barrels for the 1960s; the U.S. figure today (EIA) is noted where it differs. Carried by the December entries
  tagged `oilworld:<YYYY>` (`cal.1960-12.oil` ... `cal.1968-12.oil`). The posted prices of Arabian light at Ras
  Tanura and Venezuela's Oficina, each change dated (the *Journal*, the CIA's memoranda), a table under Esso Export's
  cut of Aug. 9, 1960 (`oilprice:ras-tanura`). Neither is an indicator series: no statement in the master; each
  table says under it what it counts.
- The war (the owner's request, Oct. 21, 2026; `tools/bib/war.py`, its STYLE; plan: `notes/extensions/memos/military-oil-vietnam.md`,
  section 1): U.S. deaths in Southeast Asia, all causes, hostile and since 1961, by month from Jan. 1965 and by year
  1960-68 (in December), today from NARA's Defense Casualty Analysis System file (2008), counted by the incident or death
  date; as first printed, the hostile deaths: the *Statistical Abstract* (1967-69 eds.) by year, the *Southeast Asia
  Analysis Report* (Oct. 1967, Thayer vol. 8, p. 102) for Jan.-Sept. 1967; the weekly Thursday releases not read ("—").
  U.S. military personnel in South Vietnam, June 30 and Dec. 31: today the DoD's table of 1974 (*Selected Manpower
  Statistics*, FY-74, p. 63), then the *Statistical Abstract*'s Dec. 31 and first-quarter figures. No monthly strength
  read. The dead by home of record per 100,000 (Census estimates, July 1): a map a year, 1961-64 together and 1965-68,
  on one scale, carried by the December entries tagged `wardead:<YYYY>` (`cal.1964-12.vietnam` ... `cal.1968-12.vietnam`).
  The file names the dead; nothing but counts leaves it, and they are not persons in the series.
- The war table (the owner's request, Oct. 22, 2026: the military numbers "in a separate table altogether", on "the
  first X of each month"; `tools/bib/wartable.py`, its STYLE): the war's series (kind: war) are not in the month's
  tables; they make a table of their own, filed by the period covered and set under the FIRST THURSDAY of the next
  month in the day layout (the day of the week the command in Saigon and the Pentagon gave out the weekly casualty
  figures: the convention, not verified against the papers), quarters and years in the month after they end. Its own
  caption, solid rule and panel; two columns, Reported then | Later, each figure with its date; a series a tbody, its
  name on a line across, so it fits 400px. The war's statements are servants after the war table where each series
  first appears on a page, "The war: concepts and sources" (the master: `indicators/concepts.yaml`). Beside U.S. deaths
  and strength: MACV's order of battle (new format, monthly, Dec. 1964-June 1968, two vintages: Oct. 31, 1967 and Sept.
  3, 1968; Thayer, vol. 8, pp. 24, 38; vol. 2, p. 7), its old format (Oct. 1967, vol. 2, p. 8), SNIE 14.3-67 (as of Oct.
  1, 1967; FRUS 1964-68, V, doc. 397), enemy strength at the quarter's end, 1968 (vol. 1, p. 126), infiltration
  (monthly, 1965-68: as first given, vol. 2, pp. 33, 64; later, pp. 62, 71, 80), enemy killed (1966-68, vol. 8, p. 5;
  vol. 1, p. 123), RVNAF killed (by year 1960-65, by month 1966-68: OPREP-5 then, MACV J-1 and the JGS's verified
  figures later; vol. 8, pp. 205, 212, 216), RVNAF strength (quarterly, vol. 8, p. 212, vol. 1, p. 126; by year and
  service, Collins, app. D, p. 151) and the other allies' (by year and country, Larsen and Collins, table 1, p. 23;
  quarterly 1968, vol. 1, p. 126). Thayer: *A Systems Analysis View of the Vietnam War* (1975), DTIC on archive.org,
  by the volume's page. A figure read once, from a source dated more than a year after its period, is "later".
  `check`: figures counts and sourced, parts adding to totals (or a `printed` note saying how the source's differ), a
  table on a day the calendar holds [war-table].
- The air war (`tools/indicators/make_war_air.py`, its docstring the rules of the count; `tools/bib/warair.py`, its STYLE):
  U.S. and VNAF fixed-wing attack sorties (strike, flak suppression, interdiction, armed reconnaissance, close and direct
  air support; not the B-52s) by the target's country, North Vietnam, Laos, South Vietnam, monthly, in The war table:
  then, as OSD's *Southeast Asia Analysis Report* printed them, Nov. 1966-Nov. 1968, where it gave a month (Thayer, vol.
  5, read by eye off the page images: pp. 222, 240, 254, 260, 275, 280, 284, 289); later, the Combat Air Activities
  file (CACTA, RG 529, NARA series 2123846, open on the catalog), counted: each sortie once (mission, sortie and launch
  unit), under its first target's country, by its number of aircraft. 32 months of Oct. 1965-Dec. 1968 survive (none
  for Aug. 1966, July and Nov. 1967, Mar., Apr., July and Nov. 1968; July 1966 to the 15th); North Vietnam by route
  package from Sept. 1966 (`war-air-nvn-rp`, CACTA only). The count runs some 5 to 15 percent under the Report in Laos
  and North Vietnam (Jan.-Feb. 1968), close to it in South Vietnam; both shown, never one for the other. Tonnage not
  yet: the load fields (LTONS, LCLAS) need NARA's subroutine DLTNS, not in the documentation read (`notes/leads.md`).
- Armed Forces Day (the owner's request, Oct. 22, 2026; `tools/bib/afday.py`, its STYLE): the year's forces tables under
  the third Saturday in May, 1960-68 (Proclamation 3399, Mar. 18, 1961, "the third Saturday of May in 1961 and ... each
  succeeding year"; Proclamation 3655, May 7, 1965, the same): the U.S. and world forces (`tools/bib/forces.py`,
  another module's, called by the name in `FORCES_FNS` it exposes) and, beside them, the RVNAF by service and the other
  allies by country, with their battalions, for the year before.
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
  any table that drifts from them. Each series needs a statement in the master
  (`indicators/concepts.yaml`, above), with pointers; `check` fails without one.
- Edit the script, not the YAML, and rerun; the key comes from the environment
  and is never written to the repo. The build needs no network.
- `check` fails on a bad period, a first-reported figure without a release
  date, or a transcribed figure without a source.

## Armed forces a year

The owner's request (Oct. 20–22, 2026): the forces and the machines a year, apart from the economic tables, under Armed
Forces Day (`tools/bib/afday.py` calls `forces.afd_block(y)`: the figures of the year before; `forces.block(year)` renders
a year). `forces/us.yaml` and `forces/world.yaml`, kept by hand, every figure read off a page (the headers are the
schema); `tools/bib/forces.py` renders and checks them (STYLE notes at the top). A table a kind, each folded, its date
and unit in the summary, its sources linked under it; a column only where the year has it ("Printed then" beside
"DMDC today", never empty); wide tables split to fit 400px.

- The United States: men on active duty by service, June 30 (the *Statistical Abstract*, 1965 and 1969 eds., beside
  DMDC's June files today); where they were, Dec. 31 (1960, 1965, 1968: Abstract 1969, table 375); by place, Sept. 30
  (DMDC's reports as *troopdata* transcribes them; not published then); major forces, June 30 (Abstract 1969, table
  369: divisions, ships, air groups, squadrons, aircraft by service); the Budget's strategic and general purpose forces
  (ICBM squadrons, Polaris boats and missiles, bomber wings, divisions, warships; 1964–68, the Abstract's reprints);
  ships by class, active and reserve (1960–65); Air Force aircraft by type and missiles by design (Atlas, Titan,
  Minuteman, Thor, Jupiter, Hound Dog, Quail; the *USAF Statistical Digest*, classified then, DTIC's copies on
  archive.org); nuclear weapons (DOE's 1994 table; FAS's estimate).
- The world, then and later apart: men by service as the *Military Balance* printed them (the Abstract's reprints,
  1966–68); ACDA's first table, spending and men, 1966; Jane's warships by type, 1967–68; SIPRI's first yearbook
  (1969), the NATO and Warsaw Pact countries' military spending a year at 1960 prices, 1960–68 (its NATO sources
  NATO's own published figures among them; its bracketed estimates count in the sums); an ally's own count, Britain's
  regular forces at June 30 by service, 1960–68, as the *Annual Abstract of Statistics* first printed them (a decimal
  as printed, `tol: 0.05`); and, made since, the Correlates of War's military personnel every year and FAS's warheads.
- `check` holds every total to its parts (`sum` rows, `sumcols`), every column to a source, and allows a printed
  figure that does not add only with its `printed` note. No armor yet, nor NATO's own tables: notes/leads.md, Foreign.
- The estimates of the Soviet forces are calendar entries, a document each, in the subthread "Defense: Soviet forces"
  (NIE 11-8 and its kin, FRUS 1958–60 III, 1961–63 VIII, 1964–68 X).

## Federal budgets, the debt limit, and bills

`tools/bib/budgets.py` and `tools/bib/bills.py` (STYLE notes at the top of each):

- A January budget entry tagged `budget:<FY>` (fiscal 1961–70) carries two tables, stacked (the owner's request, Oct.
  22, 2026: no sideways scrolling, no empty columns, titles that name the year). First "Fiscal 1964: the administrative
  budget, proposed and first reported" (the unified from fiscal 1969), receipts by source then expenditures by
  function: Proposed (that January's *Budget*), First reported (the *Budget* two Januaries later; fiscal 1967's
  expenditures from the Treasury's *Annual Report*; fiscal 1968's not found, so that year has no such column, its note
  saying why). Then "Fiscal 1964 on today's unified basis (OMB, *Historical Tables* 2.1, 3.1)", receipts then outlays,
  today's functions, one column headed by the edition read ("FY2025 ed."), never summed with the first. "Today" never
  stands alone in a title or head. Tables under each January entry, not indicator series filed in June:
  the proposal belongs to the message; the then and now classifications share no rows (indicators STYLE 8), so a
  June row a line would not align them; and twenty lines a June would swamp the month tables. `budgets/budgets.yaml`
  is read off FRASER's scans (each column's document, table, printed page and PDF page); a line shares a row with
  another column's only where it means the same thing. `check` holds each column's lines to its printed total
  (half a unit a line). Today's: `python3 -I tools/budgets/make_today.py` (needs the network; the build does not).
- The entry tagged `debt-limits` (the Debt limit thread's first, June 8, 1960) carries the table of the thirteen acts
  (OMB Table 7.3, each act read in the Statutes); every act has its signing entry, the House and Senate roll calls
  entries of their own (thread `economy-debt-limit`).
- A signing entry tagged `bill:<key>` carries the bill's course (`congress/bills.yaml`): each step dated by the bound
  Record's daily parts (the History of Bills prints pages, not dates), its page linked to that chamber's day on
  govinfo, its roll calls linked to Voteview. Now the Revenue Acts of 1962 and 1964, the Trade Expansion Act, the
  Civil Rights Acts of 1964 and 1968, the Economic Opportunity Act, the Southeast Asia (Gulf of Tonkin) resolution, the
  Voting Rights Act, the Social Security Amendments of 1965, the Elementary and Secondary Education Act, the Immigration
  and Nationality Act Amendments, the Tax Adjustment Act and the Revenue and Expenditure Control Act. A page turns to
  its day by `tools/congress/make_record_pages.py OUT YEAR...` (needs the network; the build does not): each bound
  part's MODS on govinfo, every granule's first and last page, day and chamber, written as `pages-<YEAR>.tsv` (also
  the input `tools/executive/make_source_links.py` reads); the History's page is looked up in the chamber the step
  names. A page the History misprints (another day's, another chamber's) is replaced by the page the Record's day
  shows, the step's note saying so; a step the History does not give (the message, a roll call on an amendment) is
  dated by its own record (the Public Papers, Voteview). A day of many roll calls on amendments is one row, the first
  and last linked.
- A session's adjournment entry tagged `appropriations:<Congress>-<session>` (86-2 to 90-2) carries the session's
  appropriation bills against the President's estimates (`congress/appropriations.yaml`, `tools/bib/appropriations.py`,
  its STYLE): one table a session, read off the table printed in the bound Record at the session's end (the House or
  Senate Appropriations Committee's, found by the Record's Index under Appropriations, Tables), each figure as printed in
  whole dollars, shown in $m: estimate, enacted, change, in the source's groups (the fiscal year's bills, the
  supplementals) and with its printed totals; loan and contract authority in parentheses, uncounted, as printed. The
  sources differ session to session (the estimates to the Senate, or the House's; the 1964 summary prints no estimates,
  the 1965 table "savings"): each table names its source's columns. `check` fails where a row's estimate and change do
  not make its amount or the rows do not add to the printed total, unless the row or total carries the source's
  `misprint`, shown under the table.
- Revenue effects of the tax acts: Tempalski, OTA Working Paper 81 (`[[w.tempalski-revenue-effects-of-major]]`), by
  table and page, in the signing entries of the Revenue Acts of 1962 and 1964, the Tax Adjustment Act and the Revenue
  and Expenditure Control Act; the paper has no figures for the excise act of 1965 or the investment credit's
  suspension and restoration.

## Maps of Indochina

`tools/bib/vnmap.py` (STYLE notes at the top): a map of Vietnam, Laos and Cambodia for each year, 1960–68, set in the
year's first calendar entry tagged with a place in the Republic of Vietnam, showing every entry of the year tagged with
a place: a dot a place, larger by the year's entries there, a tap listing them, each linked; under the map, folded, the
year's placed entries; names placed by the library's collision, the year's places first, then the gazetteer's rank. The
provinces as of late 1966, tinted by corps zone (the default), today's region, or plain; or the borders alone; or land
and water. Boxes: Names; North Vietnam, Laos, Cambodia (their provinces, today's); Relief, Elevation, Contours, Rivers,
Climate, Rain (by month), Population (1960, 1970: modelled, later) and Cities (the UN *Demographic Yearbook*'s figures).

- Drawn by MapLibre GL JS (the owner's spouse, Oct. 22, 2026: "Use libraries and don't reinvent the wheel"), vendored in
  `sources/vendor/` at a pinned version (its README: versions, licenses, how to update) and copied to `build/vnmap/`;
  no CDN. One client for the annual maps and the page, `tools/bib/vnmap.js` and `vnmap.css` (copied hashed to
  `build/vnmap/`, one `<script type="module">` a page), which loads the library only when a map nears the screen.
  Its gestures, label collision, hillshade (`raster-dem`, `hillshade`) and colour relief (`color-relief`) are the
  library's: write no projection, gesture or label placement of our own. The build computes no geometry (CI has only
  pyyaml): it copies the files and writes a manifest (`build/geo/vn-manifest-<hash>.json`).
- The data, made once by `tools/vnmap/` (each script's docstring names its downloads; they need shapely >= 2.1, pyproj,
  pyogrio, rasterio, mercantile, contourpy, pmtiles): one border geometry for everything, `sources/indochina/admin.geojson`,
  from geoBoundaries CGAZ (`base.py`: the countries, Vietnam's districts, Laos's and Cambodia's provinces as one
  coverage, simplified with shared edges, so neighbours meet; the 1966 units dissolved from the districts; each line
  drawn once at its rank). Rasters as PMTiles (`dem.pmtiles`, `koppen.pmtiles`; `tiles.py`), vectors as GeoJSON.
  Serving PMTiles needs HTTP range requests: GitHub Pages answers them; locally use `npx http-server build`, not
  `python3 -m http.server`. `check` fails on a map file over 50 MB, the map's files over 60 MB together, or a vendored
  file missing.
- Tags, hidden: `place:<id>`, a place in `sources/vn-provinces-1966/places.json` (the gazetteer: name with its
  diacritics, plain form, kind, Wikipedia's coordinates, 1966 province, country, rank for names); `province:<id>`, a
  1966 unit, where an entry names a province and no finer place. An event in Indochina or off its coast takes them; a
  decision about it made in Washington, Honolulu or Manila does not. `check` fails on a tag that names nothing.
- A place not in the gazetteer: add it, with Wikipedia's coordinates (never guessed) and its province by point in
  polygon. The lines are approximate (the README there); the gazetteer's notes are working notes, not the series'.
- A city's population (`sources/indochina/cities.yaml`, kept by hand): each figure as the Yearbook prints it, with its
  table and page; `check` fails on a row without them.
- The map on a page of its own (the owner's request, Oct. 22, 2026): `build/indochina.html`, "Indochina" in the top
  bar (`templates/list.html`), the reader's Pages and its front page; `./bib build indochina` alone. The same figure and
  script (vnmap STYLE 6), as tall as the screen, every placed entry, with a year selector (All years, 1960–68), each
  year anchored (`indochina.html#y1965`); then the gazetteer as a table (place, plain form, kind, 1966 province, corps
  zone, the entries tagged there by year, each row anchored `pl-<id>`) and the sources and licenses, HydroSHEDS's
  statement in full, the software's licenses (`tools/bib/indochina.py`, its STYLE notes). Each annual map closes with a
  muted line to it.

## The calendar in three parts

One list in the data (`lists/cal/`), three pages in the build, parted at the 88th Congress's opening (by the month) and at
the 89th's second session (the owner's ruling, Oct. 17, 2026): `cal.html` (Cal. I, Jan. 6, 1960, to Dec. 31, 1962),
`cal63.html` (Cal. II, Jan. 1, 1963, to Jan. 9, 1966) and `cal66.html` (Cal. III, from Jan. 10, 1966); in the reader,
three blocks. January 1966 is two sections, `196601` (Jan. 1–9) and `196601b` (Jan. 10–31). `split:` in
`lists/cal/list.yaml` is a list: the first item the first part's labels (abbr, title, span; its page texts are the
list's own), each later item a part with the date it begins (`from`), its page, and its own page_title, h1, lede,
logic, abbr, title and span. A dated section goes to the part its first day falls in; the threads section is in all.
`tools/bib/calsplit.py` (STYLE notes at the top):

- Each part's thread index lists the threads with entries in it, with that part's statement (`c` in the first part the
  thread has entries in; `c2`, `c3` in the second and third where it has entries earlier, else the latest before) and
  its dates by year: the year unlinked, in the sans, a little heavier ("**1961** Jan. 23, Feb. 20. **1962** …").
  Across the divides, muted: after its dates, the year and date of the thread's next entry in a later part (". 1963
  Jan. 14."), the year linked, not underlined, to the thread in that part's index, the date to the entry; before its
  dates, its last entry in an earlier part, linked the same way.
- The later parts' thread entries are anchored `cal63.thread.<slug>`, `cal66.thread.<slug>`; a rubric links to its
  own part's index.
- At each seam, muted: "‹ Dec. 31, 1962, in the first calendar" at the head of a part's first day; "Jan. 1, 1963, in
  the second calendar ›" at the foot of the part before's last.
- Links: write `[[id]]` as ever. The build routes a link whose anchor is in another part to that page, on the
  calendar's pages and on every other page (`cal.html#X` → `cal63.html#X`); `./bib links` checks them all.
- `./bib build cal` (or `cal63`, `cal66`) builds all three.
- A tap on a thread's entry in the index, or on its line under an entry (not on a link), lights the thread: its
  entries and its index entry on white (a lighter panel in the dark theme), each entry's own box from its rule to the
  next and an en dash past the rules' ends on either side, the rules as they were; a day's first or last entry takes a
  rule while lit where it has none. A rubric's thread name, followed to the index, lights it too, never clears it. Tapped again, cleared; kept for the tab (sessionStorage). While it is lit, a mark a
  lit entry in the thumb's column, its place and height the entry's share of the page (3px at least), no bar behind:
  amber while the scroll wheel's headings show (they stay 1.5 s after it is let go, `LINGER` in the templates), white
  after; a click on a mark brings its entry to the top (STYLE 8). The headings the scroll wheel shows are links while they show: a click goes there. On every page the scroll wheel is hidden until the reader
  scrolls (the wheel, a finger, the keys, the page's scroll bar; not a link followed or a jump: `HAND` in
  `templates/list.html` and `series.html`), and goes 1.2 s after the scrolling stops. Nothing moves (STYLE 7,
  `SCRIPT` in `tools/bib/calsplit.py`; `data-threads`, `data-thread`, `data-t` in `tools/bib/build.py`).

## The calendar's contents, and its tables and maps

Two standing rules (the owner's rules, Oct. 21, 2026; `tools/bib/contents.py`, its STYLE notes):

- The contents at the head of each calendar page (and the Outline drawer, a copy of them): the Threads line, then the
  months in a grid, a year cell spanning the year's rows and six months a row (Jan–Jun, Jul–Dec), each month in its
  three-letter form ("Sep"; this form here only, the Bluebook's everywhere else), linked to its section; a month the
  page lacks leaves its cell empty, a year takes only the rows it has months in (1969 one; the primary seasons of
  1972 and 1976 after a gap). January 1966 is one section on each of its two pages.
- After the grid, under "Tables and maps", every table and map on the page, in the order it first appears, each linked
  to its anchor, grouped by year in the grid's year column: the Executive Branch at each term, each Congress at its
  opening, the leaders and committees, the November elections, the governors, the legislatures, State finance, the
  budgets, the debt limit acts, a bill's course, the session's appropriations, each party's primaries, the conventions' delegations and roll calls,
  the dead by home State, the maps of Indochina. Not the one-off elections (a special, a single primary day), nor the
  month's indicators. And each thread's statement in the thread index lists the tables and maps its entries carry on
  the page, in order, in a muted line set right above the See also line ("*Tables and maps* Election of Nov. 8, 1960 ·
  Governors, Nov. 8, 1960"); in the reader, each part's index its part's.
- Each listed table or map is titled by its label, centered in small capitals ("ELECTIONS OF NOV. 8, 1960"), as the
  Executive roster's parts are (the owner's request, Oct. 23, 2026: "a distinct title style to visually demarcate them
  from the calendar day entries"; all-caps titles "must be unusually brief", so the labels are): STYLE 5 in
  `tools/bib/contents.py`. A November election day is one block, "Elections of Nov. 8, 1960" (`election_day` in
  `tools/bib/congress.py`): "Presidential electors", "Congress" (with the unexpired terms filled that day), "State
  elections" (the governors chosen that day, the legislatures it chose); the governors' and legislatures' entries point
  to their parts. The governors' tables shade a party's gain in the winner's color and a new governor gray, as the
  Congress's tables do (STYLE 8 in `tools/bib/governors.py`).
- Every table or map an inject sets in a calendar entry goes through `contents.put(page, eid, blk, kind, key)`: it puts
  the block at the end of the entry's `<li>` and its anchor (`tb-<kind>-<key>`) before it. A new type of table or map
  registers its kind in `KINDS` there, with its label ("Election of Nov. 8, 1960"), or `None` for one the contents
  leave out; `put` refuses an unregistered kind, and `contents.finish` (after the injects, in `build.py`) lists it in
  the contents and the threads with no more code. `check` warns on a tag whose label cannot be made [contents].
- A table set under a date, not in an entry (a day block, `tools/bib/dayblocks.py`: the war table, Armed Forces Day)
  takes its anchor from `contents.day_mark(kind, key, iso, threads)`, which names the day and the threads in the
  entry's place; the contents and the threads list it the same way. Listed: the first war table of each year on a page
  ("The war, 1965: first Thursdays", thread Vietnam) and each Armed Forces Day ("Armed forces, 1965", Defense and
  Vietnam); the other war tables, like the month's indicators, not.

## The calendar by day

Each dated section of the calendar (a month) is laid out by day, in both calendar pages and the
series reader alike: the month's undated entries, then every day from the section's first
to its last. A day shows its date, "*New York Times*" under it (a TimesMachine link by
date only; "No *New York Times* (strike)" from Dec. 8, 1962 to Mar. 31, 1963), the entries that begin
that day, each under its thread as a rubric (a line of muted small capitals above the entry, each thread's name
linked, in the rubric's own color, to its entry in the thread index at the top;
the date added for a range or a month-only entry), under an address that sets several threads going (`to:`, `short:`) a "To:" line naming each thread
and the entry it leads to, and under each such entry a "From:" line back to the address (`program_links`), then a line a thread linking the entries before and
after it in the thread ("⟨⟨ Testing ⟩⟩", the brackets the links, not underlined, the date on hover; its `also` threads too; `thread_nav` in
`tools/bib/build.py`), a "Continuing" pointer under the date on each later
day of a ranged entry, and the day's materials in two folded blocks, each closed by default and shown only where it
holds something (the owner's request, Oct. 22, 2026): "Documents" (APP, FRUS, the opinions, the recordings) and "Other records" (the
committees' meetings, the *Bulletin*, and any list added later), each summary counting its own lists; "Expand all" and
"Collapse all" under each month heading open or close both (STYLE 12 in `tools/bib/daybook.py`). The Sunday programs
and the *New York Times* line are not daily materials: they stay under the date, in neither block. A day block (the
war table on the first Thursday, the forces on Armed Forces Day: `tools/bib/dayblocks.py`) stands after the day's
entries and before its folded blocks: `section_days` sets a placeholder (`dayblocks.marker`), filled after the
indicators by `dayblocks.inject` in both build chains.

The two blocks are filled when opened (`tools/bib/lazydays.py`, its docstring; daybook STYLE 14): the build keeps each
day's closed summaries in the page and writes the blocks' contents to a file a month beside it,
`build/days/<page>-<YYYY-MM>-<hash>.json` (named by its content's hash, so a cache never serves an old month; a page's
stale months removed at each build), so a calendar page sheds some two thirds of its weight (Cal. II, 18.8 to 6.6 MB).
The first opening of a block, by a tap, Expand all (the months from the button's on, two at a time; in the reader the
list's own blocks), or a link to an anchor inside one (the page's `lzmap` names the file that holds each; the reader's
`jump` asks `window.lzGo`, and opens the folded blocks around its target, as `list.html`'s `openTo` does), fetches the month once and fills all its blocks; "loading" after the summary meanwhile.
`lazydays.split` runs on the finished page, after the injects and the routing, and curls the contents as `smart.py`
curls the page; `./bib links` reads each page with its month files. Opened as files (not through a server), the blocks
stay empty.

```
tools/daybook/make_daybook.py   writes daybook/<YYYY-MM>.yaml (needs the network; the build does not)
tools/daybook/make_recordings.py  writes daybook/recordings/<YYYY-MM>.yaml from PRDE's catalogue (needs the network)
tools/daybook/make_sunday.py      writes daybook/sunday.yaml from the Library's inventory, the TV listings, and the
                                  Face the Nation index (--ftn PATH; without it, its rows already written are kept)
tools/daybook/fetch_daily_diary.py  for the owner to run on his own computer: Johnson's Daily Diary from the LBJ Library,
                                  a PDF a day, the busiest days first, politely; stops at a challenge (its docstring)
tools/daybook/make_committees.py  writes daybook/committees/<YYYY-MM>.yaml from the bound Record's Daily Digest
                                  (--cache DIR; downloads each year's part, ~200 MB, reads it, deletes it)
tools/bib/daybook.py            lays the calendar out by day (STYLE notes at the top) and checks the data
tools/bib/committees.py         the committees' list and "Testimony before Congress" (STYLE notes) and checks the data
```

- The President: APP's documents by date (Public Papers items, executive orders,
  proclamations), in APP's order; each title linked to the item of the Public Papers that prints it, in GPO's volume
  on govinfo, its cite in grey ("1961 Pub. Papers 1"), and to APP, marked "APP", only where none does (below, "The
  Public Papers"; STYLE 13 in `tools/bib/daybook.py`).
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
- Sunday programs: a muted line under a Sunday's date, "*Meet the Press*: Hubert H. Humphrey", each guest linked to
  his name entry, the network and the source on hover. The record: the Library of Congress's inventory of Spivak's photographs of each
  Meet the Press television program (Prints and Photographs, pp020019, LOT 13025), by show date, its guests written as
  Part III writes names, 1945–80 (radio to 1950); the finding aid is in `sources/loc/`. The Classic TV Archive's episode
  guides (from the TV listings, 1947–Aug. 25, 1963) fill a Sunday the inventory lacks; where they name another person,
  the line carries "Listings: … Check." *Face the Nation* (CBS), Nov. 1959–1970: the index volume of *Face the Nation:
  The Collected Transcripts* (Holt, 1972), its chronological list: the date and the guests' names only (its topics and
  offices are CBS's text); the copy read is the owner's, not kept in the repo. *Issues and Answers* (ABC) is not yet in.
  A day's programs share one line, Face the Nation first, a semicolon between, no closing stop ("*Face the Nation*:
  John F. Kennedy; *Meet the Press*: Hubert H. Humphrey"). Each name entry lists the person's programs
  ("Television interviews"), and under the list, on one line, a sentence a program for its source ("*Face the Nation* interviews from
  *Face the Nation, 1954–1970: Index* (1972)."), not a cite on each item. An office the index gives a guest goes into
  the Life only where asked (`FTN_ROLES` in `make_sunday.py`: Percy, 1960), cited to the index by page. Guests and recording speakers are matched to persons by `person_named`
  in `tools/bib/lives.py`.
- Recordings: the White House tapes, Kennedy's from July 1962 and Johnson's, a third list after APP and FRUS. Two
  catalogues: the Presidential Recordings Digital Edition's (PRDE: titles and speakers; its transcripts by
  subscription) and the Miller Center's Secret White House Tapes (free: a page and the audio for each; the LBJ
  Library's tape and citation number), written by `tools/daybook/make_millercenter.py` from the site's public JSON:API.
  A PRDE row shows PRDE's title linked to the free page, the time, the tape cite ("Conversation WH6407-11-4288") and
  "PRDE" linked to the Edition's page ("PRDE (PRDE only)" where the Miller Center has no copy); a recording only the Miller Center gives, its title in title case. The same
  recording (`free` in `tools/bib/daybook.py`, STYLE 8): Johnson's by citation number; else the day, the time within
  twenty minutes and a name in both titles; else the day and the same title (Kennedy's); else Kennedy's tape and item.
  93 percent of PRDE's rows match; machine noise and PRDE's daily introductions are left out. The catalogue only: the transcripts and the editors'
  introductions are the Edition's text, behind its subscription, and are not taken or paraphrased; what was said comes
  from published transcripts (Beschloss, *Taking Charge*, *Reaching for Glory*) and the studies. As a calendar entry's
  primary record, the free page: `[Johnson and Robert Kennedy, 12:25 p.m.](https://millercenter.org/the-presidency/
  secret-white-house-tapes/…), Conversation WH6407-11-4288 (Miller Center)`; PRDE's page only where the Miller Center
  has no copy, cited "(PRDE only)".
- The printed record (`tools/bib/printed.py`, STYLE notes; daybook STYLE 9 and 11): under each FRUS document, where its
  own text was printed then ("Printed: *Bulletin*, Jan. 15, 1962, p. 93") and where the texts its notes cite were ("In
  the notes: …"), read from FRUS's notes by `tools/daybook/make_printed.py` (1,392 documents; the *Bulletin*'s pages
  linked to the Boston Public Library's copies on archive.org, a quarter a scan, by printed page; *Current Documents*
  unlinked, no open copy found; a date no issue bears, or a page outside its issue, "Check"). The *Bulletin* as a fifth
  list, "Bulletin": each issue's own index, item by item, filed by the release date its page prints, else the issue's
  (`tools/daybook/make_bulletin.py YEAR`: 1960 from Jan. 6 to 1969 to Jan. 20, 7,071 items; its docstring logs
  the rules, RULES 1-10, and the accuracy read against the page images: 94 percent of the items found, a title in six
  with an OCR misreading; `check` holds the rows to the span and their issues, `tools/bib/bulletin.py`). The issues and
  the copies' pages: `tools/daybook/make_dsb_index.py` (vol. 59, July–Dec. 1968, has no open copy: HathiTrust's are
  full view but bot-checked here; `notes/leads.md`). A calendar entry on a private document FRUS shows printed later carries
  "Made public: [[w.department-of-state-bulletin]], Nov. 19, 1973, 640–645." (`printed.made_public`).
- Committees: the Daily Digest's "Committee Meetings" (the Senate's, the House's, the joint committees' and the
  conferees'), a fourth list after the recordings, one line a meeting: "Senate Foreign Relations, Subcommittee on
  American Republics Affairs: PANAMA, executive session; George W. Ball", the Digest's subject heading as printed in
  small capitals, the measures, the witnesses by name as printed (office on hover), the Digest's page linked to the
  PDF's page, and the day hearings continue. The source: the bound *Congressional Record*'s Daily Digest on govinfo,
  one part a year (1960 pt16, 1961 pt18, 1962 pt19, 1963 pt21, 1964 pt20, 1965 pt23, 1966 pt23, 1967 pt29, 1968 pt26,
  1969 pt32: `VOLS`), a scan with an OCR text layer, read word by word with its box (`pdftotext -bbox`) and laid out
  column by column; the rows keep the paragraph as printed (`text`), and the PDF's pages against the printed folios
  are in `daybook/committees/volumes.yaml`. Committees by the Directory's names; a standing committee's `code` is
  Garrison Nelson's (`congress/committees.yaml`). A witness is linked only where one person fits by surname and office
  (a Member by the chamber and the day; an officer by the Executive roster on the day; anyone else by name and a
  telling word of his office): `witness_person`, STYLE 2 in `tools/bib/committees.py`. Checked by eye against January
  1964 (203 meetings, 359 witnesses): the misses left are the OCR's (a name or a stop misread). `check` fails on a row
  out of the calendar's span, without its page or link, or with a "continue" day not after it.
  A meeting held on a day the chamber did not sit is reported in the next day's Digest ("On Friday, June 3,
  subcommittee concluded ..."): it is filed under the day it was held, the Digest's day kept (`digest`). The day
  headings, the chambers' headings and the "Committee Meetings" heading the OCR loses or misreads are read by rule
  (STYLE 1-2 in `tools/daybook/make_committees.py`: a heading run together, "Tuesday.June14, 1966"; a chamber's
  heading within one column; a day whose heading is lost, dated by the page's running head); the gaps of six days and
  more that are left are recesses (Easter 1968, Labor Day 1966, Lincoln's Birthday 1967). The committee is linked to
  its table on `congress.html` in the Congress of the day, the subcommittee to its row where that Congress's list
  holds it, and a bill whose course `congress/bills.yaml` gives to the entry that carries it (STYLE 4 in
  `tools/bib/committees.py`); a subcommittee's name the OCR cut short is put whole where one name settles it
  (`settle_subs`: the Staff Directory's list, else the Digest's own longer forms), the name as read kept
  (`sub_printed`).
- The President's Daily Diary (Johnson's; Oct. 23, 2026): `daybook/diary.yaml`, written by
  `tools/daybook/make_daily_diary.py` from the National Archives Catalog, which gives the Diary's page images for 50 days
  only (Nov. 22-30, 1963; Tonkin Gulf, Selma, the signings, the trips, Glassboro, Apr. 4-7, 1968): a row a day, its
  item's address, its page count and the Catalog's title, nothing of the text. The whole Diary is on discoverlbj.org
  (`item/pdd-YYYYMMDD`), which refuses this environment and whose robots.txt (Cloudflare's managed file) bars the AI crawlers by name, ClaudeBot, anthropic-ai and Claude-Web among them, and leaves other agents to its general rule (allowed: search=yes, ai-train=no, use=reference): not read. As a
  calendar entry's primary record, after the document of the act and before the bibliography: "[President's Daily
  Diary, Aug. 4, 1964](https://catalog.archives.gov/id/192446), images 3, 5 (LBJ Library; National Archives
  Catalog)", an image the page's number in the Catalog's item; where the Diary disagrees, "Check: the Daily Diary
  gives ..." and a line in `notes/diary-discrepancies.md` (the owner's request, Oct. 23, 2026). Not yet a line in the
  day layout. `check` [diary]: STYLE and checks in `tools/bib/diary.py`.
- Opinions (the owner's request, Oct. 23, 2026: the opinions of the Attorney General and OLC "logged with the documents
  in the calendar"; 1960–69, Oct. 24): `daybook/opinions.yaml`, kept by hand (its header the schema), a list after FRUS
  in the Documents block, rendered by `tools/bib/opinions.py` (its STYLE notes; check [opinions]): every opinion of the
  *Official Opinions of the Attorneys General*, vols. 41–42, of 1960–69 (44; Google's scans on archive.org, item
  `op-atty-gen`, by leaf), the Office of Legal Counsel's of the period in its *Supplemental Opinions*, vol. 1 (2013; the
  Office's PDF on justice.gov, by PDF page), and the Department's legal memoranda FRUS prints; each the signer, the
  title linked to the copy read, the cite ("42 Op. Att'y Gen. 69", "1 Op. O.L.C. Supp. 195"), the addressee and the
  holding in one line. Nothing from memory: an opinion another document names and no copy read is under `known`, with
  its Check, and not shown. In the calendar (`notes/extensions/memos/ag-olc-opinions.md`): an opinion that shaped or was the
  decision is an entry of its own, dated to the opinion, the opinion its primary record ("[42 Op. Att'y Gen. 69](…)
  (1961)"); one that speaks to an entry is a pointer in its note ("Opinion: [42 Op. Att'y Gen. 229](…) (1963), Robert
  Kennedy to Rusk, Oct. 9: …"); the rest stay in the day's list.
- Abstracts go in `daybook/abstracts.yaml` (`key: sentence`), never in the generated
  files, so a rerun keeps them. Keys: `app:<slug>`, `frus:<volume>/<dN>`. `check` fails
  on an abstract whose key is not in the daybook.
- To extend the span, change FROM/TO in the script and add calendar sections; the days
  follow the calendar's dated sections.

## The Public Papers

The owner's request (Oct. 22, 2026): "Yes to govinfo (be sure to clean them, indicate their pagination in-text, and
replace our APP links with PPP links where possible, while leaving the APP links where it's not)." The *Public Papers
of the Presidents* (Office of the Federal Register), 1960–69, from GPO's volumes on govinfo (collection PPP): Eisenhower
1960–61 (`PPP-1960-book1`), Kennedy 1961, 1962, 1963 (`PPP-1961-book1` … `PPP-1963-book1`), Johnson 1963–64 Books I
and II (`PPP-1963-book2`, `PPP-1964-book1`), 1965–1968–69 Books I and II (`PPP-1965-book1` … `PPP-1968-book2`):
fourteen scanned books, each one PDF with ABBYY's OCR layer and no granules. Public domain (17 U.S.C. § 105). Nothing is
taken from presidency.ucsb.edu (its robots.txt bars AI crawlers): APP's own pages are linked, never read.

```
tools/ppp/make_ppp_text.py   fetches each PDF (585–825 MB) into --cache, reads its words with their boxes (pdftotext
                             -bbox, kept gzipped there, ~12 MB), deletes the PDF; segments and cleans (its docstring:
                             the reading and the cleaning, STYLE 1–7); writes sources/ppp-text/<package>.json.xz and
                             sources/ppp-text/rules.json (each cleaning rule and how often it fired, by volume)
tools/ppp/match_app.py       matches APP's documents (the daybook's President rows, sources/app-index.jsonl) to the items
                             (its STYLE); writes sources/ppp-matches.json: the matches, the unmatched on each side, each
                             volume's particulars and an index of its items
tools/ppp/relink.py          rewrites the lists' links to matched APP documents as Public Papers cites (prints each change)
tools/bib/ppp.py             the cite, the link, the texts for the ebooks, and check (STYLE notes at the top)
```

- An item: its number, heading (title and date as printed; a date the OCR lost is `month` alone or `filed` under the
  item before), first and last printed page, first and last PDF page, and its text as blocks: paragraphs, set-off
  lines (salutations' closes, signatures), the editors' bracketed notes, the "NOTE:" after the text, footnotes, small
  type. "[p. 123]" marks where each printed page begins; every item's text opens with its first page's marker. A year's
  two books are paginated through, so a page finds its item without the book. 5,414 items (three of 1968 lost by the
  OCR, `missing`), 8.5 MB compressed, the matches file 1.4 MB.
- The cite, the Bluebook's: the volume's years, "Pub. Papers", the item's first page ("1961 Pub. Papers 1",
  "1963–64 Pub. Papers 842", "1960–61 Pub. Papers 589"), linked to the PDF at that page (`…/PPP-1961-book1.pdf#page=59`);
  in a calendar note after the title and before the date: "Inaugural Address, [1961 Pub. Papers 1](…) (Jan. 20,
  1961)". The hover names the volume, item and pages. Write new notes so; the APP link only where the Papers do not
  print the document (executive orders, proclamations, platforms, the campaign of 1960) or no item matches.
- Where the series showed APP, the Papers now stand where an item matches (STYLE 3 in `tools/bib/ppp.py`): the
  daybook's President list (daybook STYLE 13), the calendar's and the lists' notes (rewritten in the data by
  `relink.py`: 1,284 links in 109 files, Oct. 22, 2026; 176 left on APP), the Names' presidential documents, the
  Executive roster's APP sources (an APP address, or `APP YYYY-MM-DD`: the day's items that name the holder). Of APP's
  7,505 documents of Jan. 1960–Jan. 20, 1969, 5,326 match an item (98.5 percent of the 5,405 the Papers could print;
  1,163 are orders, proclamations and platforms, 937 a candidate's or Nixon's); 5,325 of the 5,414 items match.
- Accuracy, checked by eye against the page images (Oct. 22, 2026: 13 pages, 31 items, every volume but 1965 Book II and
  1966 Book II, read as text only): item numbers, headings, dates, boundaries and page markers right on every page;
  the words as the OCR read them (an italic salutation can come out garbled: "My jello tv Americans"), its misreadings put right by the rules logged in
  `rules.json` (digits in numbers and years, J read as I, "£", split small capitals, hyphens at line ends, a fixed
  table of letter confusions against the volumes' own vocabulary). A misreading no rule meets stands.
- `check` [ppp]: fails on a file in `sources/ppp-text/` that is not a volume's or `rules.json`, an item out of order,
  pages or markers out of order, a PDF page outside the volume, a date outside the volume's span, an item with no
  text or not opening with its page's marker, a match naming no item; warns on items the OCR lost (`missing`) and on a
  list's APP link the Papers print (run `relink.py`). Rerun `make_ppp_text.py --cache DIR` (DIR holding the boxes, or
  the network) and then `match_app.py` after changing either; the build needs neither.

## Ebooks and feeds

The owner's request (Oct. 22, 2026): "ebooks of documents, arranged chronologically, and RSS feeds of accessible
recordings, dated and sorted chronologically ... to go through this material systematically." `build/ebooks.html`
lists both, by year (the series index's Pages, README).

- Ebooks (`tools/bib/ebooks.py`, its STYLE): an EPUB 3 a month, `build/ebooks/documents-<YYYY-MM>.epub`, Jan. 1960 to
  Jan. 1969: every FRUS document the daybook files that month, in full with its footnotes, and the President's Public
  Papers in full (above, "The Public Papers"; each item's text with its pages marked and linked to the PDF, the
  documents the Papers do not print by title, linked to APP), day by day in the daybook's order; a title page (contents, order, sources, terms),
  the contents by day, each document's citation and links to history.state.gov and to its day in the calendar. The
  text from `sources/frus-text/` (`python3 tools/ebooks/make_frus_text.py --cache DIR`, the TEI make_daybook.py
  reads; rerun after make_daybook.py; its STYLE the conversion). The build needs neither TEI nor network. The
  Papers' text from `sources/ppp-text/` (GPO's scans, their OCR cleaned), never APP's transcriptions (its site's; its
  robots.txt refuses automated readers, ClaudeBot by name). `ebooks.validate` checks each book's structure (the mimetype first
  and stored, container, manifest, spine, nav, every file well-formed, every inner link); epubcheck 5.1.0 passes
  them (not in the workflow: it needs Java).
- Feeds (`tools/bib/feeds.py`, its STYLE): RSS 2.0, a feed a year (the owner's choice, Oct. 22, 2026), `build/feeds/recordings-<YYYY>.xml`, and
  `feeds/recordings.opml` for all: every recording the Miller Center gives free (PRDE-only recordings left out), its
  page the link and its audio the enclosure, linked, never copied; dated by the recording (the catalogue's time,
  Eastern; noon without one), in date order, numbered, `itunes:type` serial; the description catalogue data only.
  Each calendar page's head names its years' feeds, and its lede points to the page.
- `./bib build ebooks` (the books, the feeds, the page), `./bib build feeds` (the feeds and the page); the full build
  does both. `check` fails on a file in `sources/frus-text/` that is not a daybook month's xz, and warns on a daybook
  month without one [ebooks].

## Working hours

The owner's standing rule (Oct. 28, 2026): no work between 7 a.m. and 5 p.m. Pacific. At 7 a.m. the running agents are
stopped, their work committed as WIP and listed for resuming; a task or an agent's report that comes in before 5 p.m.
is queued, not acted on; after 5 p.m. the agents are resumed and the queue taken up in order. Two scheduled tasks keep
it in the session that runs the reading (6:46 a.m. and 5:04 p.m. Pacific).

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
