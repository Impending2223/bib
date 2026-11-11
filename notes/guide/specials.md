# Special elections

Moved word for word from CLAUDE.md, Nov. 10, 2026 (the owner: "I approve both"); CLAUDE.md keeps the core and an index of these guides.

Specials held between general elections are not in the Clerk's biennial *Statistics*, which print only the November election. Of the specials held with a November election, the Clerk prints the Senate's and, of the House's, only Ohio-6 and Washington-3 in 1960 (as unexpired terms, under the district): those are in the election blocks; the other thirteen House specials held with November (1960-72) are `not_in_volume` in the readings and show with the Congress's specials (`specials.between`). `make_elections.py` takes Wikipedia's House specials dated on the general election (it once dropped every House special, so none reached the Clerk matching). After each Congress at its opening, `build/congress.html` gives that Congress's specials: a summary, House and Senate maps of the seats filled (large dots; the other districts drawn in the base map's gray; Result, Margin, Swing from the general election that chose the Congress, same district), and a table of the races. A calendar entry tagged `special:<key>` carries its race's table (the 86th's six of 1960, the 87th's thirteen, the 88th's of 1963–64, the 89th's of 1965–66, and the 90th's of 1967–68, thread "Special elections"). Definitions: the STYLE notes in `tools/bib/specials.py`.

```
tools/congress/make_specials.py   writes congress/specials.yaml from Wikipedia (needs the network)
congress/specials-state.yaml      votes read from the States' own returns, by hand (laid over specials.yaml)
congress/specials-cq.yaml         votes and shares from CQ's *Guide to U.S. Elections*, 6th ed. (2010), by hand (under the
                                  States' returns, over Wikipedia's shares)
tools/bib/specials.py             renders the blocks, the calendar's race tables, the roster notes' dates; checks
```

- Votes: where a State's own returns print a special (`sources/states.yaml`, `best_for_specials`), its figures go in `congress/specials-state.yaml`, keyed by the race, with the publication, edition, page and copy read (header there). The race then shows votes by round and cites them; Wikipedia's shares stay in `specials.yaml` underneath. A date the State's returns correct goes in `STATE` in `make_specials.py`.
- Citations shown with a race (`cite`): the State abbreviated as in the Bluebook (Cal., Mass., Vt., N.C.), `*title*` in italics, date, page; linked to the copy read. A race not yet read carries `pending`, the source to check, shown "Check: <cite> (bot-check)" with its access from `sources/states.yaml`.
- Seats are written with a hyphen: MA-6, VT-AL (summaries, tables, map hover text).
- Senate specials: Texas 1961 from its own page; Vermont (Jan. 7, 1972) and Georgia (Nov. 7, 1972) from `SENATE_HAND` in `make_specials.py`, their votes CQ's. Georgia's was held with the November election, but the Clerk prints the regular race only, so it carries `not_in_clerk` and shows with the specials between elections.

- Where the State's returns are not read, CQ's *Guide to U.S. Elections* (`congress/specials-cq.yaml`, header there): votes and CQ's printed shares, cited by page; the State's returns stay the Check. CQ omits minor candidates and its shares count them; `check` fails on votes and shares that cannot come from one total. Where CQ and a State's returns differ, the State's stand (`differs_from_cq` in specials-state.yaml).
- Otherwise, shares are Wikipedia's tables of each year's House specials ("<year> United States House of Representatives elections"): percentages, no votes. Texas, 1961 (Tower): votes by round, from Bartley and Graham, *Southern Elections*. The official returns are the States' canvasses.
- Where Wikipedia's list and its year table disagree on a date, the table's is used and the race carries a "Check"; so do shares that do not add to 100.
- `check` fails on a duplicate key, a `special:` tag with no race, a switch not at its seat, or a reading whose votes do not add to its printed total or whose last round lacks the winner.
- Hawaii's first elections (July 28, 1959: two Senators, one Representative) are new seats, not vacancies (`new: true` in `SENATE_HAND`): "New seat." in the note, counted apart in the summary, "(first election)" in the roster lines.
- The 85th Congress (1957–59) has its specials only, ten House races from Wikipedia (CQ's figures for three), shown in a section of their own before the 86th.
- The 85th and 86th Congresses (1957–60) have no rosters. The 86th's specials (seven House races from Wikipedia; North Dakota's Senate race of June 28, 1960, Burdick's, from the State's canvass, `SENATE_HAND`) and its changes in membership (`changes.yaml`) are in, and follow the 1958 election on `congress.html`. The scripts now run 86th-93rd; Wikipedia's pages for later Congresses have since changed (the 91st's changes, the 1973 specials), so a rerun should be merged by Congress, not taken whole.
- Notes shown with a race are for the reader: CQ's shares that count unprinted candidates, and Wikipedia's dates or shares that a State's or CQ's figures settle, stay in the files (`remarks`) and are not shown; open Checks are. A race's `note` starts a new line ("Party primaries ..."). Months as the series writes them (Feb. 15, 1961). CQ is cited "CQ Guide 6th (2010) 1266", the full title with each block's sources and in the Names' list of sources.
- The margin column gives swing as "8.3 to D" ("No swing"); the headings "Date / Seat" and "Margin / Swing".
