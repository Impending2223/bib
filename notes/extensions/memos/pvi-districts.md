# PVI by State and district: what can be sourced

Shelved Oct. 28, 2026 ("Let's hold off on the PVI for now"), and taken off the shelf the same day ("If we can
calculate the CD numbers, we should take the extension off the shelf and get started on it"): 1952–60 on the 87th
Congress's lines are open in the Census's 1961 Data Book, so they can. The work: `tools/elections/make_pvi.py`,
`elections/pvi.yaml` (the States), `elections/pvi-districts.yaml` and `elections/cd-president.yaml` (the districts),
the readings in `elections/readings/districts/`. Not shown on any page.

## The State level (built)

- `tools/elections/make_pvi.py`: each State's partisan voting index for the elections of 1962–74, the Cook construct as it stood
  1997–2021 (the State's two-party Republican share of the presidential vote, the last two elections averaged, less the
  nation's; "R+5", "EVEN" under half a point). Its STYLE: the two-party share; a State without a two-party race in a
  year (Mississippi 1960, Alabama 1964, Wallace's States 1968) computed from the other year alone, with
  `basis`. Reads `elections/<year>.yaml`; no network. `python3 -I tools/elections/make_pvi.py`.
- `elections/pvi.yaml`: its output. 1960 has none (the series holds no 1952 returns by State).

## The district level: the sources (searched Oct. 28, 2026)

A district's PVI wants the presidential vote by district on that Congress's lines for the two elections before. The
vote was compiled by district at the time, and the compilations survive:

| Election | Lines | Where | Access from here |
|---|---|---|---|
| 1952 | 83d–84th | Census, *County and City Data Book, 1956*, app. G ("elections data for all districts"); reissued as *Selected Data for Congressional Districts* | not searched |
| 1952, 1956, 1960 | 87th | Census, *Congressional District Data Book (Districts of the 87th Congress)* (1961), items 75–84; its sources: 1952, the Republican Congressional Committee's *Congressional and Presidential Vote Comparison* (1957); 1956, CQ Weekly Report supplement to May 10, 1957; 1960, CQ Weekly Report, pt. II of Mar. 10, 1961 ("Complete Returns of the 1960 Elections by Congressional Districts"; CQ's copyright noted on the 1956 and 1960 figures) | **open**: archive.org `congressionaldis1961unit` (Boston Public Library; PDF and OCR); **read** |
| 1952, 1956, 1960 | 88th; the States redistricted for the 89th and 90th | Census, *Congressional District Data Book (Districts of the 88th Congress)* (1963; H. Doc. 132, 88th Cong., 1st Sess.) and its *Supplements ... Redistricted States* (Nos. 1-7, Jan. 1965, H. Doc. 33, 89th Cong.; Nos. 8-32 later) | **read**: govinfo's Serial Set scans (12613; 12706-1, Nos. 1-7, which print 1952-60 only); Nos. 8-32 full view on HathiTrust (`mdp.39015084491953`), bot-checked here |
| 1968? | 92d | Census, *Congressional District Data, Districts of the 92d Congress* (series CDD-92, 1971) | full view on HathiTrust (`uc1.c025786080`), bot-checked here; contents not seen |
| 1968 | 93d | Census, *Congressional District Data Book, 93d Congress* (1973), items 13–17; its source the National Republican Congressional Committee's *Congressional District Vote Comparison* for the 1972 lines | **open**: archive.org `congressionaldis00unit` (NIH Library), `congressionaldis1973unit` (BPL); **read** |
| 1964, 1968 | 88th–91st | CQ Weekly Report's district returns after each election | CQ's archive: subscription |

Compiled since (each to be held against the Census volumes before use):

- Kiernan Park-Egan's *Atlas of U.S. Presidential Election Results by Congressional District*, 1952–2020, maps
  ([sites.google.com/view/presidentialbycongressionaldis](https://sites.google.com/view/presidentialbycongressionaldis/election-results));
  for 1952–64 it credits the 1961 Data Book and a Daily Kos member's spreadsheets (Daily Kos, "Presidential Results by
  1952 Districts", Feb. 19, 2013). Its figures scraped into a Kaggle set, 1952–2024 (no totals for 1964; 141 of 1960's
  rows without). Open here: the atlas's page answers.
- Gary Jacobson's district file (the major-party presidential share by district, 1952 on), the political science
  standard; not public. David Mayhew's "Amendments to Gary Jacobson dataset ... 1956–2004" (2011, works.bepress.com);
  David Broockman's replication data at Yale's ISPS archive (study d018: presidential results by district, 1952–2004;
  the page moved); Caughey and Sekhon's (David Brady's figures). ICPSR study 10, *United States Congressional District
  Data Books, 1961–1965*, the Data Books' tables as data (ICPSR refuses this environment, 403; a member's login).

So 1952–60 on the 87th's lines and 1968 on the 93d's are open in the Census's own volumes; the gap is 1964 and 1968 on
the lines of the 88th–91st Congresses (the redistricting of 1962–68, Wesberry v. Sanders), which the 88th's Data Book
and its supplements, the CQ Weekly Report, or the compilations since may close.

## What is read (Oct. 28, 2026)

`elections/readings/districts/`, a file a volume (each header the source, the copy, the schema, the checks), loaded and
held by `tools/elections/cd_readings.py`, checked by `tools/bib/pvi.py` (`./bib check` [pvi]):

| File | Volume | Lines | Elections | States, districts | Copy read |
|---|---|---|---|---|---|
| `cdb-1961.yaml` | *Congressional District Data Book (Districts of the 87th Congress)* (1961), items 75-84, pp. 5-71 | 87th | 1952, 1956, 1960 | 50, 434 | archive.org `congressionaldis1961unit` |
| `cdb-1963.yaml` | the same, *Districts of the 88th Congress* (1963; H. Doc. 132, 88th Cong., 1st Sess.), items 1-10 | 88th (Nov. 1962) | 1952, 1956, 1960 | 50, 421 | govinfo, Serial Set 12613 |
| `cdb-1965.yaml` | its Supplements Nos. 1-7, *Redistricted States* (Jan. 1965; H. Doc. 33, 89th Cong., 1st Sess.) | 89th | 1952, 1956, 1960 | 7 (S.C., Wis., Colo., Conn., Ga., Ala., Mich.), 63 | govinfo, Serial Set 12706-1 |
| `cdb-1973.yaml` | *Congressional District Data Book, 93d Congress* (1973; H. Doc. 93-109), items 13-17 (total, D, R, American Independent, percent) | 93d (Nov. 1972) | 1968 | 50, 435 | archive.org `congressionaldis00unit` |

Each figure is the OCR's (several readings agreeing, or the one that makes the State's total) or read by eye off the
page image (`eye`); the 1973 volume's every page proofed by eye against an overlay of the readings. Held: each
district row to its State column, item by item, except where the page's footnote says the State column holds votes not
distributed by district (`footnoted`; `adjust` where it gives the number); the States to the printed U.S. figures (the
1961, 1963 volumes: all add, or the difference is noted; the 1973 volume prints no District of Columbia column and its
U.S. figures are not the States' sum: `us_holds: false`); each printed percent to its figures (warnings; none left
unexplained). What the page prints that does not add stands as printed and is said so (`printed`, `over`,
`percent_as_printed`, `as_printed`, `suspect`). Every State column is also set against the Clerk's returns
(`elections/<year>.yaml`): the differences are listed by volume under `vs_clerk` in `elections/cd-president.yaml`.
They are the sources' (CQ, *America Votes*, the NRCC against the Clerk), each column being held to its districts or read
by eye. The large ones: Georgia 1956 in the 1961 volume (D 441,094 and R 216,662; the Clerk's 444,388 and 222,778);
Colorado 1956 D in the 1963 and 1965 volumes (257,997; the Clerk's 263,997; the 1961 volume's 263,997); Arkansas 1968
(D 188,228, R 190,759, A 240,982; the Clerk's 184,901, 189,062, 235,627); Alabama's 1968 A (691,425; the Clerk's
702,385); New York 1968 D (3,063,660; the Clerk's 3,378,470: the NRCC leaves out the Liberal line, below).

The 1973 volume (its p. XI): the figures are the National Republican Congressional Committee's *Congressional District
Vote Comparison*, "retabulated by the Committee to reflect the congressional district boundaries as established for
the 1972 elections", and "the vote cast for third parties endorsing the major party candidates are excluded from
figures shown here for 'Democratic' and 'Republican' but included in the total": New York's Democratic figures leave
out Humphrey's Liberal line (`excludes`; a PVI from them says so in its `basis`). Eighteen States' columns hold absentee
or other votes not distributed by district (the footnotes, quoted in the file); Colorado's 4th and 5th are marked
"Estimated."; New York's 10th-16th and 20th-23d and all seven of Washington's print "(NA)"; California's 12th prints a
total under its three parties' sum.

**CQ's copyright.** The 1961 volume says (p. XI): "The 1956 and 1960 figures are copyrighted by Congressional Quarterly
News Features and may not be reproduced without permission from that organization." The 1963 volume names CQ and *America
Votes* (both copyright) for its figures. The readings keep them for computation only; nothing is shown. The owner's
call before any page prints a district's figures (the PVI itself, a derived index, is another matter; the 1973
volume's NRCC figures carry no such notice).

## What is computed

`tools/elections/make_pvi.py` (its STYLE 4-12): `elections/pvi-districts.yaml` (each House election's districts on its
Congress's roster, with the PVI, its inputs and sources, and every district without one under `none` with the reason)
and `elections/cd-president.yaml` (the figures used, by volume; `vs_clerk`). The construct is the States' (the
two-party Republican share, the two presidential elections before, averaged, less the nation's); a figure on one
Congress's lines serves another's district only where `congress/geo.json` gives it the same shape in both; a source
on the Congress's own lines first, then the nearest.

| House election | Congress | Elections used | With a PVI | Without | Why without |
|---|---|---|---|---|---|
| 1960 | 87th | 1952, 1956 | 419 | 16 | Ky. (7), Miss. (2), Tex. and Wash. (5) redrawn after 1952 or 1956 (the volume's note: not recomputed); Alaska, Hawaii (no vote) |
| 1962 | 88th | 1956, 1960 | 321 | 105 | 100 split-county districts "n.a." (Cal., Fla., Ill., Kan., Mass., Minn., Mo., N.Y., Pa.); Wash. (4), Tex. 22d (1956 under the 8th) |
| 1964 | 89th | 1956, 1960 | 302 | 131 | the same 100; 24 "(NA)" in the 1965 supplement (Ala., Conn., Ga., Mich., Wis.); R.I. (2: New Shoreham moved, Sept. 1963, so the shapes differ); Wash., Tex. |
| 1966 | 90th | 1960, 1964 | 0 | 433 | no 1964 by district read |
| 1968 | 91st | 1960, 1964 | 0 | 434 | no 1964 by district read |
| 1970 | 92d | 1964, 1968 | 0 | 435 | no 1964; 1968 read on the 93d's lines only (409 districts' shapes differ) |
| 1972 | 93d | 1964, 1968 | 0 | 435 | no 1964 (1968 read for 417 districts: New York's 11 and Washington's 7 "(NA)") |
| 1974 | 94th | 1968, 1972 | 0 | 435 | no 1972 by district read |

A State with no two-party race in a year (Mississippi 1960; Alabama 1964; Wallace's five States, Alabama among them, 1968)
gives no district figure for that year; the other year alone serves, as for the States (`basis`).

## What is left, and what would close it

- **1964 by district** (the 1966-72 elections): the Census's later supplements to the 88th Data Book, *Redistricted
  States*, Nos. 8-32 (dates not seen), are full view on HathiTrust (`mdp.39015084491953`; Nos. 1-7 `mdp.39015084491797`),
  bot-checked here: the owner can open them in a browser and say whether they print 1964 (Nos. 1-7 print 1952-60
  only). Else CQ Weekly Report's district returns after the 1964 election (subscription), or the compilations since
  (Park-Egan's atlas, the Daily Kos spreadsheets, Jacobson's file), held against the Census volumes.
- **The redistricted States' 1956 and 1960** on the 90th-91st lines: the same Supplements Nos. 8-32.
- **1972 by district** (the 1974 election): the Census's *Congressional District Data, 94th Congress* (1974; LCCN
  74603410; not on HathiTrust by that number), the NRCC's *Vote Comparison* for 1974, CQ, Barone's *Almanac of
  American Politics* 1974 (not searched).
- **1968 on the 92d's lines** (the 1970 election): *Congressional District Data, Districts of the 92d Congress*
  (CDD-92, 1971-72; "45 State reports and one report for ...", the *Statistical Abstract*, 1971), full view on HathiTrust (`uc1.c025786080`, pts. 1-46),
  bot-checked here; whether it prints the vote is not known.
- **The split-county districts "n.a."** (1962, 1964): CQ's district figures for 1956 and 1960 (the 1961 volume's own
  source) on the 87th's lines serve only where the lines held; the rest need CQ's recomputation (none known).
- Rhode Island's two districts of 1964 differ by one town (0.1 percent): a rule to take them would be the owner's.
- The 1952 vote on the 83d-84th lines (*County and City Data Book, 1956*, app. G): not read; it would add nothing to the
  elections above.

Shown from Oct. 28, 2026 (the owner: "Show both. Be sure to cite and attribute"): tools/bib/pvi.py, STYLE 3-5.
