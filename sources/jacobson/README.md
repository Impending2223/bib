# Jacobson's district file, 1946–2014

Gary C. Jacobson, replication data for "It's Nothing Personal: The Decline of the Incumbency Advantage in U.S. House
Elections," Harvard Dataverse, version 1.0 (Mar. 20, 2015), [doi:10.7910/DVN/29559](https://doi.org/10.7910/DVN/29559).
The article: 77 J. Pol. 861 (2015) (recalled, not read: Check the volume and page). License: CC0 1.0 (the Dataverse
record), so the file is kept here whole. Fetched Oct. 31, 2026 (the owner: "Is there any way for me to get you the
ICPSR or the Jacobson?"; "Please do go ahead").

- `JOPrepfile1.tab`: Dataverse's tab-delimited copy of `JOPrepfile1.dta` (datafile 2547168; the original's MD5,
  as the record gives it and as fetched, 6706739c5d27a68d52cad6604dc8516d). A row a House seat a year, 1946–2014.
- `Documentation for JOPrepfile1 (aggregate data).doc`: his codebook and the Stata commands for the article's figures
  (datafile 2547164, MD5 705561ec334ce222aaee982257799c7b).

## The variables (his codebook, as he gives them)

| Variable | Codes |
|---|---|
| `year`, `decade` | the election's year; its decade (40, 50, ...) |
| `state` | the State, 1 to 50 in strict alphabetical order |
| `stcd` | the State and district, State × 100 + district (01 to n): "the 4th district of Illinois is 1304". A seat at large in a State that also has districts is n+1; a State's only seat, 01 |
| `inc` | 0 Republican incumbent; 1 Democratic incumbent; 2 open seat held by Democrats; 3 open seat held by Republicans; 4 open seat, new (reapportioned); 5 two incumbents, opposite parties (redistricting); 6 two Democratic incumbents; 7 two Republican incumbents; 8 Democratic incumbent, challenger is Democrat; 9 Republican incumbent, challenger is Republican; 10 two Republicans, open seat |
| `ptynow` | 1 seat held by a Democrat; 0 new seat held by neither party; −1 held by a Republican |
| `inc3` | 1 Democratic incumbent; 0 none; −1 Republican incumbent |
| `incwin` | 1 incumbent won; 0 lost |
| `dv` | the Democrat's share of the two-party vote, in points (unopposed: missing) |
| `dvp` | the same, the previous election |
| `fr` | 0 not a freshman; 1 freshman elected at the previous general election; 2 in a special more than a year earlier; 3 in a special in the election year; 9 seat not defended by a major party incumbent |
| `redist` | 1 district redrawn since the last election; 0 not |
| `dpres` | the Democrat's share of the major-party presidential vote (for midterms, the share two years earlier) |
| `cprescat` | 2 the challenger's party's presidential candidate ran 2.01 points or more ahead of his national vote in the district; 0 within 2 points; −2 2.01 or more behind |
| `midterm` | 1 midterm; 0 presidential year |
| `split` | 1 the district's plurality went to different parties for House and President; 0 the same |
| `south` | 1 the eleven States of the old Confederacy; 0 not |
| `cexpx`, `iexpx` | the challenger's and the incumbent's expenditures, 2014 dollars |
| `preswin` | not in the codebook (in the file) |

His Gelman–King estimate (the codebook, Figure 1a): `reg dv dvp ptynow inc3 if redist==0`, a year at a time, the
redistricting years left out; the "modified" one (1b) puts `dpres` for `dvp` and keeps every seat.

## What the series does with it

- `tools/elections/jacobson.py` (its STYLE) holds his shares, lags and redrawn flags against the series' returns,
  seat by seat: `notes/jacobson-compare.md` (generated; `check` warns when stale [jacobson]). The Clerk's figures
  stand; each difference is a lead to the page.
- `tools/elections/make_baseline.py` runs the baseline three ways, one of them on his lags (`dvp`).
- `tools/elections/make_pvi.py` takes his `dpres` for a district no Census volume prints, marked as his (its STYLE 13).

What he says of his sources is in the article, not the codebook (not read: Check). The figures for the 1960s agree
with the Clerk's in 97–99 percent of seats (the listing's table).
