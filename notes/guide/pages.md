# The page budget

The owner, Nov. 19, 2026: "Do we need to split Works? Do we need to split Names further than we have already? I think we do." and "Do we not have a pass that tells us that size of each page, on calendar pages and otherwise, directs splits, and refactors navigation and pointers after the split pass? Please implement one if not." The code and its rules: `tools/bib/pages.py` (its docstring, STYLE 1–5).

```
./bib pages            after a build: every page in build/ with its size and its units (entries, persons, works,
                       rows), against its budget; a page over it marked OVER, with the split its structure proposes;
                       exit 1 while one not exempt is over (--all lists the forwarding stubs too)
./bib pages --plan     the proposal written into the plan: pages.yaml (Names, Works, the Executive, Congress) and
                       lists/cal/list.yaml `split:` (the calendar); the next ./bib build applies it
```

`pages.yaml` holds both the budget and the plan: `budget` (5 MB of HTML a page), `budgets` (the calendar's own, the owner's "some 8 MB" of Nov. 12), `fill` (a split packs its parts to 70 percent of the budget, room to grow), `why`, `exempt` (`series.html`, the one-page reader, whole by design), then the splits the plan wrote, and `retired`. Edit it by hand only to hold or undo a split.

The splits follow each page's own structure:

- The calendar: a part over its budget into quarters, a quarter still over into months, the owner's names (`cal1964Q1`, `cal1964-01`); the old part goes to `retired_parts` and its page forwards old links by their anchors (calsplit STYLE 14; calendar-by-year.md). A month's page name is matched whole in an anchor (`cal1964-01.thread.cuba`).
- The Names: a letter over budget in surname ranges, packed in key order, one person never on two pages (`names-ma-mc.html`, labelled "Ma–Mc"; one person alone a page by his name, "Johnson, Lyndon B."); the letter's old page, `names-m.html`, a stub that forwards an anchor to its range, an alias to its person.
- The Works: a page a letter (`works-a.html` …); `works.html` the index, forwarding an old `works.html#w.…` link.
- The Executive: a page a term (`executive-1961.html`), a term too large for one page cut at its heads (the departments, the agencies: `executive-1961-departments.html`), each piece opened by the term's heading, "continued"; the last term with the authorities and the sources; `executive.html` the index, forwarding.
- Congress: a page a Congress, small ones packed together (`congress-88.html`, `congress-85-87.html`); `congress.html` the index, forwarding.

A later plan keeps a part within budget as it is (stable addresses) and plans again only a part over it; a page it drops goes to `retired:` and stays a stub that forwards.

Pointers: every link to an anchor on a split page goes to the part that holds it, from every page, the reader's included: the builders ask `pages.names_href` and `pages.works_href`, and `pages.route` rewrites the rest at the write (as `calsplit.route` does for the calendar); inside a part, a bare `#X` another part holds goes there. A build of one page reads the other families' maps from `.cache/pages-map.json`. Navigation: each part carries its family's bar (the page's own unlinked) and at its foot the part before and after ("‹ Ma–Mc · Index · Md–Mi ›").

After a split: `./bib build`, `./bib links` (0 links to missing anchors, 0 to missing pages), `./bib pages` (nothing over but the exempt), `./bib readme` (README's table of the other pages).
