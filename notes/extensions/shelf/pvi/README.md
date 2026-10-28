# PVI: shelved

The owner, Oct. 28, 2026: "Let's hold off on the PVI for now." Not run by the build, not shown, not checked.

## What is here

- `make_pvi.py`: each State's partisan voting index for the elections of 1962–74, the Cook construct as it stood
  1997–2021 (the State's two-party Republican share of the presidential vote, the last two elections averaged, less the
  nation's; "R+5", "EVEN" under half a point). Its STYLE: the two-party share; a State without a two-party race in a
  year (Alabama 1960 and 1964, Mississippi 1960, Wallace's States 1968) computed from the other year alone, with
  `basis`. Reads `elections/<year>.yaml`; no network. `python3 -I notes/extensions/shelf/pvi/make_pvi.py`.
- `pvi.yaml`: its output. 1960 has none (the series holds no 1952 returns by State).

## The district level: the sources (searched Oct. 28, 2026)

A district's PVI wants the presidential vote by district on that Congress's lines for the two elections before. The
vote was compiled by district at the time, and the compilations survive:

| Election | Lines | Where | Access from here |
|---|---|---|---|
| 1952 | 83d–84th | Census, *County and City Data Book, 1956*, app. G ("elections data for all districts"); reissued as *Selected Data for Congressional Districts* | not searched |
| 1952, 1956, 1960 | 87th | Census, *Congressional District Data Book (Districts of the 87th Congress)* (1961), items 75–84; its sources: 1952, the Republican Congressional Committee's *Congressional and Presidential Vote Comparison* (1957); 1956, CQ Weekly Report supplement to May 10, 1957; 1960, CQ Weekly Report, pt. II of Mar. 10, 1961 ("Complete Returns of the 1960 Elections by Congressional Districts"; CQ's copyright noted on the 1956 and 1960 figures) | **open**: archive.org `congressionaldis1961unit` (Boston Public Library; PDF and OCR) |
| 1960 (and 1964?) | 88th; the States redistricted for the 89th and 90th | Census, *Congressional District Data Book (Districts of the 88th Congress)* (1963; H. Doc. 132, 88th Cong., 1st Sess.) and its *Supplement ... Redistricted States* (parts by State, from Jan. 1965) | not found open; HathiTrust likely (bot-checked here). Check what elections the supplements print |
| 1968 | 92d | Census, *Congressional District Data, Districts of the 92d Congress* (series CDD-92, 1971) | not searched |
| 1968 | 93d | Census, *Congressional District Data Book, 93d Congress* (1973), items 1–17; its source the National Republican Congressional Committee's *Congressional District Vote Comparison* for the 1972 lines | **open**: archive.org `congressionaldis00unit` (NIH Library), `congressionaldis1973unit` (BPL) |
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

## Before it is built

- Read the 1961 and 1973 Data Books' tables into a reading file (the elections readings' loop), each figure by page.
- Find the 88th Data Book and its supplements (HathiTrust's catalog API: the holdings and rights; the owner in a
  browser for the pages), and the CDD-92 series.
- Decide the construct for a district whose lines changed between the two elections (the Data Books recompute the
  vote on the new lines: the NRCC's "vote comparison" is that recomputation).
