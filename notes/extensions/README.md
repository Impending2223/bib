# Extensions: proposals, plans and shelved drafts

The place for what the series might add and has not, or has begun and set aside (the owner, Oct. 28, 2026: "a place for
future extension ideas and shelved drafts"). Three kinds:

- `memos/`: the research memos written before a part was built, each on what can be sourced and what to build. They
  stay after the build as the record of why it was built so; the parts not built stay proposals.
- `shelf/`: drafts set aside, code and data, each folder with a README: what it is, why shelved, what it waits on.
  Nothing here is read by `./bib check` or `./bib build`.
- This index: each item's state, kept by hand. A lead (an event, a figure, a source not reached) goes to
  `notes/leads.md`, not here; a source to fetch, to `notes/procurement.md`.

## Memos

| Memo | Built | Not built |
|---|---|---|
| [`military-oil-vietnam.md`](memos/military-oil-vietnam.md) (Oct. 20, 2026) | The war table (deaths, strength, the enemy and the allies, the air war); the forces a year under Armed Forces Day; the Oil group and the world's oil; the Vietnam field entries (in part) | §5, HES maps and a hamlet-security row (1967–Jan. 1969); tonnage (CACTA's DLTNS); armor; the CMH, OSD and USAF hosts refused here |
| [`fiscal-congress-conventions-state.md`](memos/fiscal-congress-conventions-state.md) (Oct. 20, 2026) | State finance; the budgets, the debt limit acts, the bills' courses, the revenue effects; leaders and committees; the committees' meetings; the Republican convention of 1968; the *Bulletin* daybook and FRUS's printed concordance | The conventions of 1960, 1964 and Democratic 1968 (Bain and Parris, borrow only); *Current Documents* as a daybook list (no open scan) |
| [`indicators-suggestions.md`](memos/indicators-suggestions.md) (Oct. 20, 2026) | The measures marked "Kept", and those marked "No" later built by `make_finance.py` | The London gold price (`gold-london`: no source); the first printings of the Economic Report's money and payments tables |
| [`pvi-districts.md`](memos/pvi-districts.md) (Oct. 28, 2026) | The States' PVI, 1962–74 (`elections/pvi.yaml`); the districts', 1960, 1962 and 1964 (`elections/pvi-districts.yaml`, from the Census's Data Books); both shown, with the vote by district, cited and attributed (Oct. 28, 2026) | The districts' for 1966–74 (1964 and 1972 by district not found open; `notes/leads.md`) |
| [`simulations.md`](memos/simulations.md) (Oct. 29, 2026) | Nothing yet | The world on a date; the Congress pivots (DW-NOMINATE); the period's own macro models, then today's estimates, then the open economy; the war (the crossover point, guerrilla Lanchester, the home front); conventional, air and nuclear war (Dupuy, force scoring, no first use); surprise, morale, command and political will (the positions ledger, the warning record, opinion); the calendar hook (`sim:` tags); a game, later |
| [`witnesses.md`](memos/witnesses.md) (Oct. 30, 2026) | Nothing yet | The registry of witnesses and their edges to the roots, replacing `sources/cited-records/`; the readers' rules (every witness registered, copies kept as edges, works and collections as witnesses, branches followed, variants); `./bib stemma`; the pass by event |
| [`volume.md`](memos/volume.md) (Oct. 30, 2026) | §6, parallel readers and the merge (Oct. 31) | Nothing folded by default (the forces tables unfolded); big threads split into subthreads, the parent's index its own entries only; the calendar a page a year; thread statements written once (the scope, the stations from the events, span-tagged sentences); events as records; the merge's audit into `check`; search on the site |
| [`ag-olc-opinions.md`](memos/ag-olc-opinions.md) (Oct. 23, 2026) | `daybook/opinions.yaml`, the opinions as entries and pointers | The opinions under `known` (no copy read) |

## Shelf

| Draft | Shelved | Waits on |
|---|---|---|
| (none now: the PVI, shelved Oct. 28, 2026, came off the shelf the same day; its memo is `memos/pvi-districts.md`) | | |

## Ideas not yet a memo

Named in CLAUDE.md as not yet done, here so they are found in one place:

- *Issues and Answers* (ABC) in the Sunday programs.
- The President's Daily Diary as a line in the day layout.
- Each State's rule for proposing a constitutional amendment, for the legislatures' Article V shading (*Book of the
  States*, 1960–67).
- The Congressional Staff Directory's 1965, 1967 and 1969 editions, for the 89th–91st Congresses' subcommittees.
- NATO's own force tables.
- Small multiples on the Indicators page: every series on the calendar's span, one scale each, both vintages, one
  cursor across them all (the owner, Oct. 28, 2026, of the chart gallery's demo 8: "they might be nice in the indicators
  page, but I haven't spent any time there yet"). The gallery: https://claude.ai/artifact/8da6JMvh2SXn5g7F1hHnsH.
  Its demos 2 and 3 (tinted changes; a row that opens into a chart) went into the month tables Oct. 29, 2026
  (`tools/bib/indchart.py`).
