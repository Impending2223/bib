# Fiscal policy, Congress, conventions, State finance, foreign-policy documents: sources and what to build

Memo, Oct. 20, 2026. Read-only research; nothing in the repository changed. Links marked: **open** (tested from here, the
thing itself answers), **bot-checked**, **catalog only** (HathiTrust's catalog API answers; the pages are bot-checked
here), **borrow** (archive.org's controlled lending: item page answers, text behind a loan), **subscription**, **paper
only**, **not reached** (no answer from here). "Not verified" marks what I could not see.

---

## 1. State and city finance

### What the thread holds now

`./bib find -l cal --thread state-and-city-finance` gives 59 entries; 31 have the thread as their first, the rest
come in by `also` (State constitutions, Alabama, Governors, Students, Opinion). They are of four kinds:

- **A State's new or raised tax, enacted or refused** (about 20): West Virginia's income tax (Feb. 1961), Sanford's
  food tax (June 1961), Texas's first sales tax (Aug. 1961), Welsh's taxes in Indiana (Mar. 1963), Nevada, North
  Dakota and Oregon refusing at the polls (1963), Romney's program refused (1963) and passed (July 1967), Maryland
  (1964, 1966, 1967), Oklahoma (1965), New York's first sales tax (Aug. 1965), Virginia (1966), New Jersey (Apr.
  1966), Massachusetts (Nov. 1966), Nebraska refused (Nov. 1966), Reagan's bill (July 1967), Minnesota vetoed (June
  1967), Kentucky (Mar. 1968), Michigan's graduated tax refused (Nov. 1968).
- **City finance** (5): Detroit's income tax (1962), Wagner's borrowing (1965), New York City's income tax (July
  1966), Seattle's Forward Thrust (1968); Maryland's local enabling act (1966).
- **Bond and amendment elections** (about 15): California's water bonds, Oklahoma's, Alabama's county-tax
  amendments, Texas's, Virginia's first general obligation bonds (Nov. 1968).
- **Washington and the States' money** (6): Presidential Statement No. 6 (Oct. 1964), the Governors' Conference on
  tax sharing (July 1965, Dec. 1966), Johnson to *Newsweek* (Aug. 1965), the memorandum of Nov. 11, 1966, Gallup on
  tax sharing (Jan. 1967).

**What it adds up to.** A set of well-sourced anecdotes (each act cited to the Blue Book, the session laws, or the
Governors' *Proceedings*) with no frame. The reader cannot tell from the thread that the decade was the great
expansion of State taxation; that ten States adopted a general sales tax in the period; how big any of these sums
were against the State's budget or its income; or that federal grants to State and local governments nearly tripled, $7.0 billion in fiscal 1960 to
$20.2 billion in fiscal 1969 (OMB Historical Table 12.1, today's figures). The entries read as isolated
fights because nothing says what was normal.

**What is missing** (checked with `./bib find`):

- **The adoptions themselves.** From the Census data below: in fiscal 1960 sixteen States had no general sales tax
  (AK, DE, ID, KY, MA, MN, MT, NE, NH, NJ, NY, OR, TX, VA, VT, WI); in fiscal 1969, six (AK, DE, MT, NH, OR, VT). The
  calendar has five of the ten adoptions (TX, NY, NJ, VA, MA); it lacks Kentucky's (Combs, 1960), Wisconsin's (the
  selective sales tax of 1961–62), Idaho's (1965), Nebraska's (1967), Minnesota's (enacted over the veto, 1967; the
  calendar has only the veto). Individual income taxes: seventeen States without one in 1960, twelve in 1969; Indiana,
  Michigan, West Virginia are in, Nebraska (1967) is not (New Jersey's change in the data is probably the commuters'
  tax of 1961, not a general income tax: check). (Census's "zero" in a column is the test I used; a tax
  adopted mid-year shows the next year. Each adoption needs its act checked.)
- **Scale**: no entry gives a State's total revenue, tax burden, or rank; no national figure at all (State tax
  revenue $22.1 billion in fiscal 1963, Census).
- **Federal aid to the States** as a series (it is the thread's other half: Heller–Pechman, the Governors, creative
  federalism) and the grant programs that drove State budgets (highways, Medicaid from 1966, ESEA Title I).
- **The tax-exempt bond**: the Revenue and Expenditure Control Act of 1968 (§ 107) ended the exemption for most
  industrial development bonds; the calendar's entry on the Act (June 20–28, 1968) does not mention it (grepped).
  Check the section against 82 Stat. 251.
- **Lotteries**: New Hampshire is in; New York's lottery amendment (adopted at the polls Nov. 1966, as I recall; the
  lottery began in 1967) is not in the calendar: no entry has "lottery" or "sweepstakes" but New Hampshire's.
- **Fiscal stress in the big cities** (New York City's borrowing against future revenue after Wagner, Lindsay's 1966 package beyond the
  income tax, Medicaid's cost to New York State in 1968): sparse.

### Sources

| Source | Publisher, cadence | Granularity | Access |
|---|---|---|---|
| [Data Base on Historical Finances of State Governments, FY1942–2008 (`State_Govt_Fin.zip`, 6 MB)](https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/State_Govt_Fin.zip) | Census Bureau, Governments Division (Aug. 2010); the published *State Government Finances* series in machine-readable form | Each State government and the U.S. total, **every fiscal year 1951–2008**; ~650 items: revenue by source (property, general sales, selective sales by kind, licenses, individual and corporate income, death and gift, severance, federal aid by function), expenditure by function and by character (current operation, capital outlay, construction, equipment, aid to local governments by type, interest), debt (issued, retired, outstanding, long/short term, full faith and credit vs nonguaranteed, by purpose), cash and securities; population and personal income for each year; each State's fiscal-year end date | **open** — downloaded and read here (MS Access; `mdb-export` reads it). 52 rows a year for 1960–69 |
| [Data Base on Historical Finances of State and Local Governments, FY1957–2008 (`Govt_Finances.zip`, 15 MB)](https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/Govt_Finances.zip) | Census, the *Governmental Finances* series | **State and local combined, by State, each year** 1957–70 (read here); State and local apart from 1961; counties, cities, townships, special districts and school districts apart in the census years 1957, 1962, 1967; federal and national totals | **open** — downloaded and read |
| [Data Base on Historical Finances of Municipal Governments, FY1951–2006 (`City_Govt_Fin.zip`, 15 MB)](https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/City_Govt_Fin.zip) | Census, the *City Government Finances* series | ~320 city rows a year 1960–69 (660 in the census year 1967), revenue by tax (including income tax), expenditure, debt | **open** — downloaded and read |
| [Historical finances, Federal–State–local, national (`hist_fin.zip`)](https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/hist_fin.zip) | Census | National totals by level of government, selected years 1902–2008 | **open** (listed, not opened) |
| [The printed reports, 1915–1992, scanned (`1900-1992 State Government Finance.zip`, 795 MB)](https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/1900-1992%20State%20Government%20Finance.zip) | Census | Each year's *Summary* (No. 1) and *Compendium of State Government Finances* (No. 2), 1960–64; *State Government Finances in 19xx*, 1965–69 | **open** — listed by range request; the 1963 *Compendium* (G-SF63-No. 2, 42 pp., GPO 1964) extracted: an OCR layer, rough but searchable; its text figures match the database (current operation $12.4 billion = 12,449,211 thousand). Pages to cite |
| [The city reports, 1909–1992 (`1900-1992 City Finance.zip`, 2.2 GB)](https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/1900-1992%20City%20Finance.zip) | Census | *Compendium of City Government Finances* and *Summary*, 1959–63; *City Government Finances in 19xx*, 1964–69 | **open** — listed |
| [Individual government file (IndFin), 1967–2012](https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/_IndFin_1967-2012.zip) | Census | Every sampled government, from 1967 | **open** (HEAD only) |
| Census of Governments, 1962 and 1967: [1962 *Graphic Summary*](https://www2.census.gov/programs-surveys/cog/tables/1962/graphic-summary/1962-vol6-no5-graphic-summary.pdf), [1962 State bulletins](https://www2.census.gov/programs-surveys/cog/tables/1962/state-bulletins/1962-vol7-state-bulletins.zip), [1967 State reports, pt. 1 (159 MB PDF)](https://www2.census.gov/programs-surveys/cog/tables/1967/state-reports/1967-vol7-state-reports-part1.zip), [1967 *Graphic Summary*](https://www2.census.gov/programs-surveys/cog/tables/1967/graphic-summary/1967-vol6-no7-graphic-summary.pdf); index of all: [Census historical data page](https://www.census.gov/programs-surveys/gov-finances/data/historical-data.html) | Census, quinquennial | Every county, city, school district; the finance volume (vol. 4) itself is not on the page's list (not verified elsewhere); its figures are in `Govt_Finances` | **open** |
| [BEA State personal income, 1929– (`SAINC.zip`)](https://apps.bea.gov/regional/zip/SAINC.zip); quarterly from 1948 ([`SQINC.zip`](https://apps.bea.gov/regional/zip/SQINC.zip)) | BEA, today's revised figures | State, annual (quarterly) | **open** |
| [BEA gross State product, SIC basis, 1963–1997 (`SAGDP_SIC.zip`)](https://apps.bea.gov/regional/zip/SAGDP_SIC.zip) | BEA (estimates made decades later; no State GDP was published in the 1960s) | State, annual, by industry, current dollars | **open** (listed: `SAGDP2S_*_1963_1997.csv`). Nothing for 1960–62: use personal income, which Census's database already carries |
| *The Book of the States*, 1960–61 to 1968–69 | Council of State Governments, biennial with supplements | Each State: tax rates and their dates, budget practice, the tax enactments of the biennium, finance tables (Census's) | [archive.org 1960](https://archive.org/details/bookofstates0013vari), [1962–63](https://archive.org/details/bookofstates19620000coun), [1964–65](https://archive.org/details/bookofstates19640000coun), [1966–67](https://archive.org/details/bookofstates19660016fran), [1968–69](https://archive.org/details/bookofstates19680017vari): **borrow**; [HathiTrust](https://catalog.hathitrust.org/api/volumes/brief/issn/0068-0125.json): **catalog only** (search-only) |
| Tax Foundation, *Facts and Figures on Government Finance* | biennial | National and State tables, from Census | [1969 ed.](https://archive.org/details/factsfiguresongo0000vari): **borrow**; earlier editions not found on archive.org |
| ACIR (Advisory Commission on Intergovernmental Relations), 1959– | reports, irregular | *Tax Overlapping in the United States, 1964* ([borrow](https://archive.org/details/taxoverlappingin0000unit)); *Fiscal Balance in the American Federal System* (1967; [borrow](https://archive.org/details/fiscalbalanceina0002unit)); *State Aid to Local Government* (1969; [ERIC microfiche, open](https://archive.org/details/micro_IA41153143_0085)). *Significant Features of Fiscal Federalism* begins in the 1970s (not verified which year). UNT's ACIR archive (library.unt.edu/gpo/acir): **not reached** (the tunnel opens, nothing answers) | |
| Sylla, Legler and Wallis, State and local sources and uses of funds, ICPSR 6304 | ICPSR | State, census years | not tested (ICPSR asks a login) |

**State budget balances.** No series of "the" balance exists for the 1960s on a common basis: the States' general
funds differ, and NASBO's *Fiscal Survey of States* begins in 1979. What Census gives, State by State and year by
year, is total revenue less total expenditure (borrowing-financed capital spending makes it a deficit by
construction), long-term debt issued and retired, debt outstanding, and cash and security holdings. These are honest
measures if labelled as Census's; a "budget balance" should not be claimed.

### What we could build

1. **A State-finance table each fiscal year, on the calendar** (like the legislatures' block): a calendar entry
   tagged `statefin:<FY>` in the month Census's fiscal year closes for most States (June), or at the release of each
   *Compendium* where its date can be read off the scan (issued the following year; the 1963 one is "1964", month not
   printed on the title page). Contents, one row a State, 50 plus D.C. and the U.S.: taxes per $1,000 of personal
   income (and per head); the shares of general sales, individual income, corporate income, motor fuel, property;
   federal aid as a share of general revenue; expenditure split current operation / capital outlay / aid to local
   governments; long-term debt outstanding per head; revenue less expenditure. Cite the *Compendium* by table and page
   (the scan) and the database. A map: the tax regime (sales and income / sales only / income only / neither), the
   year's adopters marked; and a quantile map of taxes per $1,000 of income. Everything is in the three Census
   databases already downloaded and read here. Taxes over State GDP from 1963 on (BEA SIC), with the caveat that
   those GDP figures were made in the 1990s.
2. **State and local together** (`Govt_Finances`): the same table on the combined basis, which is the comparable one
   (States divide functions with their localities differently: Hawaii's schools are the State's, New Jersey's are
   local), with property tax, the localities' main tax, in view.
3. **A thread statement and entries the data call for**: each State's first general sales or income tax as an entry
   (ten sales, about five income adoptions; each act from the session laws or the *Book of the States*); the national
   numbers once a year (State taxes, grants, debt; one line in the annual entry).
4. **Cities**: the forty-odd largest cities' table (taxes by kind, debt) in the census years 1962 and 1967 from the
   city database, beside the city-finance entries (New York, Detroit, Philadelphia's income taxes).
5. **Indicators**: the national State-local series (receipts, expenditures, surplus) in the national income accounts
   are already in FRED (State and local government current receipts, annual, from 1929): a row could join the
   "Federal finance" group as "State and local", filed by the calendar year. Not built; FRED series names not checked
   here.

**Recommendation.** Build 1 and 3 first. 1 is a module like `tools/bib/legislatures.py` reading a generated
`elections/`-style YAML (`sources/` or a new `statefin/<FY>.yaml`) made by a one-time script from the Access file
(mdbtools: `apt-get install mdbtools`, present here): about two days for script, renderer, map and check. 3 is
writing: ten to fifteen entries, a day with the session laws. 2 and 4 add half a day each once 1 exists. Caveat to
print with the table: fiscal years differ by State (most end June 30; New York's Mar. 31, Alabama's Sept. 30, Texas's
Aug. 31; the database gives each), and Census figures are on its own classification, not the States' budgets.

---

## 2. Federal fiscal policy and tax policymaking

### What the series holds now

- **Indicators** (`tools/bib/indicators.py`, group "Federal finance"): the administrative budget, the cash budget, the
  unified budget (fiscal 1968 on) and the federal sector of the national accounts, each a fiscal-year total (receipts,
  expenditures, balance), as first reported in the next *Economic Report*, the January estimates (`est`), and OMB's
  revised figures today. Nothing by source of receipts or by function of spending; no debt or debt limit; no
  appropriations.
- **The calendar's Economy thread** (149 entries, `./bib find -l cal --thread economy`). Each January budget is an
  entry with its totals, fiscal 1961 through 1970, except one: Kennedy's first, for fiscal 1963 (sent Jan. 18,
  1962), is missing (no January 1962 entry mentions the budget; date from memory, check). The big tax acts are well told from 1966 on: the Tax Adjustment
  Act (Jan.–Mar. 1966), the investment credit's suspension and restoration (Sept. 1966–June 1967), the surcharge from
  the State of the Union of Jan. 1967 through Ways and Means' refusal (Oct. 1967), the Smathers–Williams amendment
  (Apr. 1968) and the Revenue and Expenditure Control Act (June 1968), each step with its Voteview roll call and the
  bound *Congressional Record* on govinfo. The debt-limit fights of 1967 are told the same way.

**Thinner earlier.** The Revenue Act of 1962 is one entry, its signing (Oct. 16, 1962): not the tax message of Apr.
20, 1961 (a sentence inside a Cuba entry), the House's passage (Mar. 29, 1962) or the Senate's (Sept. 6). The 1964
act has House passage, Senate passage and signing, not Senate Finance's hearings (Oct.–Dec. 1963) or its report. The
excise act of 1965 has the message and the signing only. Dates from memory; check each.

**Debt limit**: OMB's Historical Table 7.3 lists twelve acts changing the limit from June 30, 1960, to June 30, 1967
(a thirteenth, Apr. 7, 1969, falls after the calendar). The calendar tells five of them (74 Stat. 290; 75 Stat. 148; 77 Stat. 50; and the two of
1967 by their votes). Missing: Mar. 13, 1962 (76 Stat. 23, $300 billion), July 1, 1962 (76 Stat. 124, $308 billion
to Mar. 31, 1963), Aug. 27, 1963 (77 Stat. 131), Nov. 26, 1963 (77 Stat. 342, $315 billion), June 29, 1964 (78
Stat. 225, $324 billion), June 24, 1965 (79 Stat. 172, $328 billion), June 24, 1966 (80 Stat. 221, $330 billion).
(Read here from the table; the calendar checked by grepping each cite: its "76 Stat. 23" is the Manpower Act,
which begins on the same page.)

**What the story lacks** is the frame: what the government took in by kind of tax and spent by function, and how
those shares moved (defense down as a share to 1965, then Vietnam; excise cut; social insurance up); what each budget
proposed, what Congress did to it (appropriations cut or added against the President's estimates, session by
session), and what came out; the revenue effect of each act on a common basis; the debt against its limit.

### Sources

| Source | What, cadence | Access |
|---|---|---|
| *Budget of the United States Government*, fiscal 1961–1970 ([FRASER title](https://fraser.stlouisfed.org/title/budget-united-states-government-54); e.g. [fiscal 1965, 470 pp.](https://fraser.stlouisfed.org/files/docs/publications/usbudget/bus_1965.pdf)) | Each January: receipts by source, expenditures by function and agency, new obligational authority, three budgets compared, the year's estimates and the last year's actual; OCR'd (the fiscal 1965 text read here: "Analysis of receipts by source," p. 56; "Table 18. Administrative budget and trust expenditures by function, 1954–65," p. 457) | **open** |
| *Treasury Bulletin*, monthly ([FRASER](https://fraser.stlouisfed.org/title/treasury-bulletin-407); [Jan. 1964](https://fraser.stlouisfed.org/files/docs/publications/tbulletin/1964_01_treasurybulletin.pdf)) | Monthly receipts and expenditures, the public debt and the debt subject to limit, ownership of the debt | **open** |
| *Annual Report of the Secretary of the Treasury on the State of the Finances* ([FRASER](https://fraser.stlouisfed.org/title/annual-report-secretary-treasury-state-finances-194); [fiscal 1964](https://fraser.stlouisfed.org/files/docs/publications/treasar/AR_TREASURY_1964.pdf)) | Each fiscal year's actuals, the Secretary's statements to Congress reprinted, the tax legislation of the year | **open** |
| OMB, *Historical Tables* (the current budget's; [govinfo, fiscal 2025](https://www.govinfo.gov/app/details/BUDGET-2025-TAB); [whitehouse.gov](https://www.whitehouse.gov/omb/budget/historical-tables/)) | Today's revised figures, unified basis: Table 2.1 receipts by source 1934– ([xlsx](https://www.govinfo.gov/content/pkg/BUDGET-2025-TAB/xls/BUDGET-2025-TAB-3-1.xlsx)); 3.1 outlays by function 1940– ([xlsx](https://www.govinfo.gov/content/pkg/BUDGET-2025-TAB/xls/BUDGET-2025-TAB-4-1.xlsx)); 4.1 by agency 1962–; 7.1 debt; **7.3 statutory limits on the debt, each act with its Statutes cite** ([xlsx](https://www.govinfo.gov/content/pkg/BUDGET-2025-TAB/xls/BUDGET-2025-TAB-8-3.xlsx)); 12.1 grants to State and local governments 1940– ([xlsx](https://www.govinfo.gov/content/pkg/BUDGET-2025-TAB/xls/BUDGET-2025-TAB-13-1.xlsx)) — note govinfo's file numbers run one ahead of the table numbers | **open** (read here) |
| OMB, Public Budget Database ([govinfo](https://www.govinfo.gov/app/details/BUDGET-2025-DB)) | Outlays by account and subfunction, **fiscal 1962–** ([xlsx](https://www.govinfo.gov/content/pkg/BUDGET-2025-DB/xls/BUDGET-2025-DB-2.xlsx)); receipts by source and account, 1962– (`DB-3`); budget authority only from 1976 | **open** (read here) |
| Treasury, Office of Tax Analysis, [Working Paper 81, *Revenue Effects of Major Tax Bills*](https://home.treasury.gov/system/files/131/WP-81.pdf) (Tempalski, rev. Sept. 2006) | Each major act's estimated effect, in current dollars, constant dollars and share of GDP: the Revenue Acts of 1962 (−$0.2 bn) and 1964 (−$11.5 bn), the Tax Adjustment Act (+$5.0 bn), RECA 1968 (+$16.0 bn the second year) | **open** (read here) |
| *Congressional Record*, bound, on govinfo (`GPO-CRECB-<year>-pt<n>`): the daily proceedings; **the Index and History of Bills and Resolutions** (1960 pt15, 1961 pt17, 1962 pt18, 1963 pt20, 1964 pt19, 1965 pt22, 1966 pt22, 1967 pt28, 1968 pt25); **the Daily Digest** (the next part each year) | The History of Bills gives each bill's every step with the Record's page (H.R. 8363, 1964: Senate Finance report S. Rept. 830, p. 1275; passed Senate p. 2393; conference report H. Rept. 1149; approved, P.L. 88-272); pages convert to dates by the bound Record's daily granules. [1964 History of Bills](https://www.govinfo.gov/content/pkg/GPO-CRECB-1964-pt19/pdf/GPO-CRECB-1964-pt19-2.pdf) (155 pp., OCR in three columns, readable with care) | **open** (read here) |
| *Digest of Public General Bills and (Selected) Resolutions*, Library of Congress Legislative Reference Service, each session with cumulative issues and an index ([1964](https://archive.org/details/sim_united-states-loc-congressional-research-service-digest_1964); every year 1960–69 and its index on archive.org) | Each public bill's summary and its status | **open** |
| Voteview roll calls ([e.g.](https://voteview.com/rollcall/RH0880028)) | Every recorded vote | **open** (already used) |
| Committee reports (H. Rept., S. Rept.) and hearings | The Serial Set on govinfo carries the *Economic Reports* the series links; a few 1960s hearings are on govinfo (`CHRG-88shrg21544`, linked in the lists); individual 1960s committee reports not verified on govinfo (the govinfo search API's demo key was rate-limited here) | partly open; not verified |
| *Appropriations, Budget Estimates, Etc.*, Senate document each session (the estimates, House, Senate, conference and enacted figures by bill) | The appropriations story in one table a session | archive.org has only 1980s editions (open, ERIC microfiche); 1960s: **not verified** (HathiTrust not checked: no OCLC number in hand) |
| *CQ Almanac*, 1960–68 | Each session's appropriations table, tax bills' histories, the debt limit | [1968](https://archive.org/details/congressionalqua0024cong), [1966](https://archive.org/details/congressionalqua0000cong_c5g9): **borrow**; CQ Press Library: **subscription** (403 here) |
| IRS, *Statistics of Income, Individual Income Tax Returns*, each year ([archive page](https://www.irs.gov/statistics/soi-tax-stats-archive-1954-to-1999-individual-income-tax-return-reports); [1964](https://www.irs.gov/pub/irs-soi/64inar.pdf)) | Returns, income and tax by bracket: who paid what before and after 1964 | **open** |
| FRED/ALFRED | Already used; the Treasury's monthly receipts and outlays are not in ALFRED as first printed for the 1960s (not verified) | open |

The literature is in the catalogue already: Stein, *Fiscal Revolution*; Zelizer, *Taxing America*; Manley,
*Politics of Finance*; Fenno, *Power of the Purse*; Wildavsky; Savage; Witte; Okun; Heller; Flash; Bernstein, *Guns
or Butter*; Michelmore.

### What we could build

1. **The debt limit, complete** (cheap, sure): seven calendar entries for the signings the calendar lacks, each with
   its Statutes cite and its House and Senate roll calls (Voteview), and a small table under the thread's first
   entry or a gloss: each act, the limit, its term (OMB Table 7.3). Half a day.
2. **Each fiscal year's budget, by source and by function** (an indicators-style table filed in June, or under each
   January budget entry): receipts by kind (individual income, corporate income, excise, social insurance,
   customs, estate and gift, other) and expenditures by the budget's own functions (national defense, international,
   space, agriculture, natural resources, commerce and transportation, housing and community development, health
   labor and welfare, education, veterans, interest, general government), three columns as the indicators have them:
   proposed (that January's Budget), reported actual (the next January's Budget, or the Treasury's *Annual Report*),
   today (OMB Historical Tables 2.1, 3.2; unified basis, today's functions, so its own column, never summed with the
   others). Ten fiscal years, about twenty rows; two transcriptions a year from FRASER's OCR, checked against their
   printed totals; `check` that the parts add. Two to three days.
3. **A bill's course, as a table under its signing entry** (like the primaries' returns under a convention's
   opening): every step of each revenue and debt bill, from message to signature, each dated, its Record page
   linked to the day's granule, the report numbers, the roll calls. For: the Revenue Acts of 1962 and 1964, the
   Interest Equalization Tax Act, the Excise Tax Reduction Act of 1965, the Tax Adjustment Act of 1966, the
   suspension (Nov. 1966) and restoration (June 1967) of the investment credit, the Foreign Investors Tax Act, the
   Revenue and Expenditure Control Act, and the twelve debt-limit acts. Source: the History of Bills (govinfo) and
   the *Digest* (archive.org), the pages to dates by the Record's daily granules, the votes by Voteview. Kept by hand
   in a YAML file (`congress/bills.yaml`), rendered by a small module. About three days for the data, one for the
   module. The steps the calendar now lacks (1962's House and Senate passage, Senate Finance in 1963–64) then come
   for free as table rows, and an entry is written only where something happened worth a sentence.
4. **The revenue effect of each act** on one basis: a column in that table or a line in the signing entry, from OTA
   WP-81 (the source to cite). An hour.
5. **Appropriations**: each session's thirteen or so bills against the President's estimates, from the Senate's
   *Appropriations, Budget Estimates, Etc.* or the *CQ Almanac*. The best single measure of what Congress did to the
   budget, and the hardest to source openly from here; leave until a copy is found (HathiTrust full view likely, as
   a federal document, but not checked).

**Recommendation.** 1, 4 and 2 in that order (about three days), then 3 (four days). Together they let a reader see
the 1964 cut and the 1968 surcharge against the budgets they changed, and the steps of each act without a new entry
for each. 5 later.

---

## 3. A Congressional roster with the leadership, the committees and seniority (answer only)

**Yes; the sources are open and one of them is already structured.**

What exists now: `congress/<NN>.yaml` (87th–91st at their openings) holds each member's seat, party, given names and
Bioguide id, nothing more; the leaders appear only in calendar prose (Jan. 10, 1962: "McCormack Speaker; Albert
majority leader; Boggs whip"; Jan. 3, 1969: Kennedy over Long for whip) and the thread "Rules".

| Source | What | Access |
|---|---|---|
| Garrison Nelson, *Committee assignments, 80th–97th Congresses (House)* and *80th–102nd (Senate)*, on [Charles Stewart's data page](https://web.mit.edu/17.251/www/data_page.html): [House `hrc8097.mit`](http://web.mit.edu/cstewart/www/data/hrc8097.mit), [Senate `snc80102.mit`](http://web.mit.edu/cstewart/www/data/snc80102.mit), [codebook `cb9999`](http://web.mit.edu/cstewart/www/data/cb9999) | Fixed-width, one row a member a committee a Congress: ICPSR id, name, committee code (standing, select, joint), party status, **rank within party on the committee**, chamber seniority, **dates of assignment and of leaving**, status at the end of the Congress; and a "non-committee status" block coding the **Speaker, floor leaders and whips** of each party, with first/second holders where one changed within a Congress. Read here: 625 House rows for the 87th (372 members, 21 committees), 275 Senate rows (106 senators); Mills, Ways and Means, rank 1 in the 86th–91st; Senate committee sizes look complete | **open** (downloaded) |
| Stewart and Woon, assignments 103rd–115th (same page) | Later Congresses only | open; out of period |
| Canon, Nelson and Stewart, *Historical Congressional Standing Committees, 1st–79th* (same page, `hst*.dat`) | Earlier Congresses | open; out of period |
| *Congressional Directory*, each session: govinfo has the editions of Jan. 6, 1960; Apr. 1, 1961; Jan. 10, 1962; Mar. 1, 1963; Jan. 1, 1964; Mar. 1, 1965; Jan. 10, 1966; Feb. 28 and Dec. 15, 1967 (`CDIR` in `tools/bib/executive_sources.py`). E.g. [1963, text](https://www.govinfo.gov/content/pkg/CDIR-1963-03-01/text/CDIR-1963-03-01.txt) | Each committee's members in rank order, majority and minority (the text interleaves the two printed columns, so the parse must split them: Ways and Means 1963 reads "Mills … Byrnes … King … Baker …", D and R alternating), staff; the leaders and party officers; each member's biography with his committees | **open** (read here) |
| [House: party leaders](https://history.house.gov/People/Office/Majority-Leaders/), [party divisions](https://history.house.gov/Institution/Party-Divisions/Party-Divisions/), [Congress profiles](https://history.house.gov/Congressional-Overview/Profiles/88th/); Senate: [leaders](https://www.senate.gov/senators/majority-minority-leaders.htm), [party divisions](https://www.senate.gov/history/partydiv.htm) | Leaders, whips, conference chairs with dates; party divisions | **open** |
| unitedstates/congress-legislators (the rosters' source) | Carries ICPSR ids beside Bioguide ids (to join Nelson's rows to the rosters); its committee files are current only | open (used already) |
| Subcommittees | Not in Nelson's standing-committee rows as far as I read; the *Congressional Staff Directory* (from 1959) lists them | not verified |

**What it could look like.** On `congress.html`, under each Congress at its opening: (1) **Leadership**: Speaker,
floor leaders, whips, conference or caucus chairmen, President pro tempore, with changes during the Congress dated
(Rayburn's death, McCormack, Albert, Boggs; Halleck to Ford, Jan. 4, 1965; Long whip, 1965; Kennedy whip, 1969).
(2) **Committees**: each standing committee a block, the ratio (Ways and Means 15–10), the chairman and ranking
member, members by party in rank order, each linked to his roster row and name entry, changes during the Congress
with their dates, and the Daily Digest's or the Directory's page cited. A "Seniority" column (years in the chamber)
on the roster. (3) In each member's roster line and Names entry: his committees and rank ("Ways and Means, 1st
(chairman), 87th–90th Cong."). (4) Calendar entries tagged `committees:<NN>` could carry a Congress's block, as
`congress:<NN>` does now. Size: a one-time script (`tools/congress/make_committees.py`) reading Nelson's rows, the
codebook's committee codes, and the ICPSR–Bioguide join; a renderer; `check` that ranks are consecutive and every
member resolves. Three to four days, plus a day to check a Congress against the Directory.

---

## 4. Calendaring the committees' proceedings (answer only)

**Yes, from one open source: the bound Daily Digest.**

| Source | What | Access |
|---|---|---|
| *Congressional Record*, **Daily Digest**, bound, one part a year on govinfo: 1960 pt16, 1961 pt18, 1962 pt19, 1963 pt21, 1964 pt20, 1965 pt23, 1966 pt23, 1967 pt29, 1968 pt26 (e.g. [1964, 555 pp., 170 MB](https://www.govinfo.gov/content/pkg/GPO-CRECB-1964-pt20/pdf/GPO-CRECB-1964-pt20-1.pdf)) | For each day: each chamber's actions, and **"Committee Meetings"**: committee and subcommittee, the subject or bill, open or executive session, the witnesses by name and office, and "hearings continue" with the next date; joint committees apart; the next day's schedule. 1964 read here: an OCR text layer; plain `pdftotext` keeps the columns in order ("Committee on Ways and Means: Resumed hearings on medical care for the aged, and heard testimony from public witnesses. Hearings continue on Tuesday, January 21."); about 2,500 committee paragraphs in 1964, so some 20,000 for 1960–68 | **open** (read here) |
| *Monthly Catalog of United States Government Publications*, monthly, with annual index ([e.g. May 1966](https://archive.org/details/sim_monthly-catalog-of-united-states-government-publications_1966-05_856); every month 1960–69 on archive.org) | The printed hearings: title, Congress and session, bill, the hearing dates, pages, SuDoc number ("Minimum wage, hearings, 89th Congress, 2d session, on H.R. 13712, Apr. 6, 1966"). Gives what was printed and when held, not what was said | **open** (the July 1964 issue's text gave a server error here; May 1966 read) |
| The printed hearings themselves | Many on archive.org (the `us-congress` collection: e.g. [Ways and Means, *Medical Care for the Aged*, executive hearings, 1965](https://archive.org/details/medicalcareforag00unit), open, with OCR); HathiTrust (federal documents, generally full view: **catalog only** here); a few on govinfo (`CHRG-88shrg21544`, cited in the lists) | partly open |
| CIS *US Congressional Committee Hearings Index* (ProQuest Congressional) | Every published hearing, witnesses indexed | **subscription** ([ProQuest Congressional](https://congressional.proquest.com/) answers with its login page) |
| The House committees' final *Legislative Calendars* (each committee, each Congress: bills referred, hearings and meetings by date) | The committee's own record | not verified online; paper |
| The History of Bills (with the Index, govinfo, see 2) | Reports by committee and date | **open** |

**What it could look like.** A fourth list in each day's documents, after APP, FRUS and the recordings: "Committees"
(closed by default), one line a meeting: "Senate Foreign Relations: hearings on the Tonkin Gulf resolution, executive
session; Rusk, McNamara" with the Digest's page linked (`…pt20-1.pdf#page=N`), witnesses linked to their name
entries where one person fits (the daybook's matching), the bill linked to its history where we keep one. The
Names pages gain "Testimony before Congress" from the same rows. A calendar entry for a hearing that matters (the
Fulbright hearings of Feb. 1966, Ways and Means on the tax bill) then cites the Digest's line and the printed
hearing.

**Cost and risk.** A generator like `make_daybook.py`: download nine Digest volumes (~1.5 GB), extract text, split
by day (the day headings are regular: "Tuesday, January 21, 1964"), split each day's "Committee Meetings" into
paragraphs by the "Committee on …:" lead, normalize committee names to Nelson's codes, pull witness names. OCR
errors in names are the main risk: a witness matched by name only where the surname and an office agree. About a
week for a first pass of all nine years and a check on a month a year; the Monthly Catalog's hearing titles as a
second pass later. Not abstracted: the Digest's own sentences are the government's, and can be shown as written.

---

## 5. The conventions of 1960, 1964 and 1968

### What the calendar holds now

Each convention's opening (tagged `primaries:<YYYY>-<R|D>`, carrying the party's primary returns and map), the
nominations and acceptances, the platforms (APP, linked), the credentials fights where they made news (the
Mississippi Freedom Democrats and Alabama, 1964; Georgia, Mississippi and the unit rule at Chicago, 1968), Gallup's
"convention's choice" questions, and every primary day (CQ's returns). What is **not** there: how the other delegates
were chosen. In 1968 most delegates to both conventions were chosen by State conventions, caucuses or party
committees, some of them in 1967 (the McGovern–Fraser commission's finding, *Mandate for Reform*, in the catalogue
as `w.selection-mandate-for-reform`); `./bib find -l cal delegates` gives 51 entries, nearly all primaries. No State
convention that chose national delegates is in the calendar (Goldwater's sweep of the State conventions in 1964, the
Pennsylvania and New York delegations for Humphrey in 1968), no apportionment of delegates, no roll call by State.

### Sources

| Source | What | Access |
|---|---|---|
| *Official Report of the Proceedings of the Twenty-Ninth Republican National Convention*, Miami Beach, 1968 ([archive.org, open copy](https://archive.org/details/sim_republican-national-convention-proceedings_august-5-8-1968), 497 pp., with [index](https://archive.org/details/sim_republican-national-convention-proceedings_1968_index)) | Verbatim proceedings; **the Call, with the apportionment of delegates State by State** ("ALABAMA 10 Delegates at Large; 2 Delegates from each Congressional District—Total 26"); the roll calls by State; the rules; the delegates' names | **open** (OCR read here) |
| The same, Republican 1964 (the archive.org item [*Twenty-eighth Republican National Convention, San Francisco, 1964*](https://archive.org/details/twentyeighthrepu0000unse) is a borrow, and may be the program rather than the Proceedings: not verified), Republican 1968 second copy ([borrow](https://archive.org/details/officialreportof0000repu)); Democratic 1964 ([*Official Report of the Proceedings of the Democratic National Convention and Committee*](https://archive.org/details/officialreportof0000chai)) | Same | **borrow**; 1960 both parties and Democratic 1968: not found on archive.org; HathiTrust not checked (no OCLC in hand) |
| Bain and Parris, *Convention Decisions and Voting Records* (Brookings, 2d ed. 1973) ([borrow](https://archive.org/details/conventiondecisi0000bain); 1st ed. 1960, [borrow](https://archive.org/details/conventiondecisi0000unse)) | Every convention's narrative and the State-by-State votes on every roll call, nominations and key issues | **borrow** |
| CQ, *National Party Conventions, 1831–1972* (1976; later editions to 2008) ([borrow](https://archive.org/details/nationalpartycon0000cong_n4e9)) | Narrative, key ballots, platforms, the delegate apportionment by year | **borrow** |
| David, Goldman and Bain, *The Politics of National Party Conventions* (Brookings, 1960) ([open, Digital Library of India copy](https://archive.org/details/dli.ernet.506053)) | Delegate apportionment formulas and selection methods to 1956; the frame for 1960 | **open** |
| *Nomination and Election of the President and Vice President of the United States, including the manner of selecting delegates to national political conventions* (Senate Library compilation, each presidential year) ([1968, borrow](https://archive.org/details/nominationelecti0000na)) | **Each State's law and party practice for choosing delegates**, the dates, the primary laws; the constitutional and statutory provisions on the election | **borrow** (1968); 1960 and 1964 editions not found; as a congressional document it may be on govinfo's Serial Set or HathiTrust: not verified |
| Commission on Party Structure and Delegate Selection (McGovern–Fraser), *Mandate for Reform* (1970) | The survey of 1968 practice State by State (selection in 1967, proxy voting, unit rule, fees) | not found online here; in the catalogue |
| The Hughes Commission, *The Democratic Choice* (1968) | The report to the Chicago convention on 1968 selection | not found online here |
| APP | Platforms, acceptance addresses, the President's remarks | **open** (used) |
| CQ, *Guide to U.S. Elections*, 6th ed. (the owner's copy, already used for the primaries) | A chapter on the nominating conventions with key ballots; whether it prints State-by-State votes for 1960–68: not verified | owner's copy |
| The Republican rule and the Democratic call: delegate apportionment formulas (Republican bonus delegates for States carried; the Democrats' 1964 and 1968 bonus votes; the Democrats' 1964 resolution on discrimination and the Special Equal Rights Committee; the unit rule's abolition, Chicago 1968) | In the Calls and Proceedings above | as above |

### What we could build

1. **Delegate apportionment and selection, a table and a map for each party each year**, tagged
   `conventions:<YYYY>-<R|D>` on the convention's opening (beside the primaries map): each State's votes, how they
   were chosen (primary binding / primary advisory with convention / State convention / caucuses and convention /
   State committee / mixed), the dates of the choosing (primary day, State convention day), and the first-ballot
   vote. Map: method of selection; a second: the first-ballot leader by State. Sources: the Calls (apportionment),
   *Nomination and Election* (method and dates, for 1968 at least), Bain and Parris or the Proceedings (first ballot).
   The primaries module (`tools/bib/primaries.py`, `drawQ`) already draws the State map. About three days a year
   (six conventions: about two weeks), the 1968 Republican first, its Proceedings being open.
2. **The State conventions as calendar entries** where a delegation's choice made news (1964: Goldwater's
   conventions in the spring; 1968: Humphrey's), thread `elections-<year>`: perhaps ten a year, from the
   *New York Times* and CQ.
3. **Roll calls by State** under the nomination entries and the key procedural votes (1964: the Scott civil rights
   amendment and the extremism amendment at San Francisco; 1968: the minority plank on Vietnam, the unit rule, the
   Georgia and Mississippi seatings): a table each, from the Proceedings or Bain and Parris; a day a convention once
   a copy is in hand.
4. **The proceedings day by day**: one entry a session day is too many; better one entry a convention day with the
   keynote, the platform, the nominating speeches, each cited to the Proceedings' page (open for Republican 1968),
   APP's texts where it has them.
5. **The rules**: a gloss on each convention's opening setting out the apportionment formula and the rules on
   delegates as the Call states them, quoted and cited (the gloss form the brief allows: "what the entry rests on
   and does not say").

**Recommendation.** Start with Republican 1968 (open Proceedings): build 1 and 3 for it, see whether the shape holds,
then borrow Bain and Parris and *Nomination and Election* for the rest. The owner could also consider asking for
scans of the 1960 and 1968 Democratic Proceedings, which I could not find online.

---

## 6. *American Foreign Policy: Current Documents* and the *Department of State Bulletin*

### Where the series cites them

- *Current Documents*: ten calendar notes, all as plain text, none linked (Nov. 1960: "1960, 786–792"; Jan. 1962:
  "1962, p. 589", taken from a FRUS footnote; 1966: six entries; 1967: two). No card in `works/`.
- The *Bulletin*: ten calendar notes (Jan., Feb., May ×2 and Sept. ×2, 1960; June 1962; Feb. and Mar. 1963; Sept.
  1966; one linked, June 1962, to the Boston Public Library's volume on archive.org, `departmentofstat471962unit/page/64`);
  one card cites it as a journal (`works/r.yaml`, "Dept. State Bull."); and the Executive roster's register
  (`sources/executive-sources.yaml`, "DOS Bulletin, …") links single issues 1953–60 on archive.org (the Serials in
  Microfilm copies).
- FRUS cites both constantly in its footnotes ("printed in *American Foreign Policy: Current Documents, 1962*, pages
  1096–1098"): in three volumes sampled from the TEI the daybook reads, 6–20 citations of *Current Documents* and
  10–17 of the *Bulletin* each; across the 1958–68 volumes perhaps a thousand of each (an extrapolation, not a count).

### Open copies

| Work | Copies | Access |
|---|---|---|
| *Department of State Bulletin*, weekly, vols. 42–61 (1960–69) | Boston Public Library volumes on archive.org, a quarter or a half-year each, with OCR and page numbers: `departmentofstat421960unit` … `departmentofstat6169unit` (e.g. [vol. 50, 1964](https://archive.org/details/departmentofstat501964unit), [vol. 54, 1966](https://archive.org/details/departmentofstat541966unit), [vol. 60, 1969](https://archive.org/details/departmentofstat601969unit)); **vol. 59 (July–Dec. 1968) not found**, only its [index](https://archive.org/details/sim_department-of-state-bulletin_july-01-december-30-1968_59_index) | **open**, except the gap |
| The same, issue by issue (Serials in Microfilm) | `sim_department-of-state-bulletin_<date>_<vol>_<no>`: open 1959–61 ([e.g. Aug. 8, 1960](https://archive.org/details/sim_department-of-state-bulletin_1960-08-08_43_1102)); the sampled 1964 issue (`…_1964-01-06_50_1280`) is **borrow** | open to 1961 |
| The same on HathiTrust | [Catalog, ISSN 0041-7610](https://catalog.hathitrust.org/api/volumes/brief/issn/0041-7610.json): 1,277 items, all "Full view", vols. 40–63 present by quarter, vol. 59 (Oct.–Dec. 1968) among them | **catalog only** (pages bot-checked here); fills the 1968 gap for a reader in a browser |
| *American Foreign Policy: Current Documents*, annual, 1956–1967 (published 1959–1969) | archive.org: only [1958 (borrow)](https://archive.org/details/americanforeignp0000vari) and the later series (1981–). HathiTrust: probably full view as a federal document, but I could not find the record's number from here (catalog search bot-checked; Google Books API over quota; Open Library not reached) | **not found open**; HathiTrust **not verified** |

### What could be built

1. **The *Bulletin* as a daybook list.** Each weekly issue (dated Mondays) has a contents page and an index; the
   archive.org OCR carries the running heads ("518 DEPARTMENT OF STATE BULLETIN") that tie text to printed pages,
   and archive.org's page URLs take the printed page (`/page/518/mode/1up`, as the series already links). A
   generator: for each volume, find each issue's start and contents, list its items (title, page), and file each
   item under the date of the document where the item states it (DSB prints "Press release 23 dated January 15"),
   else under the issue date. Shown as a fifth closed list ("*Bulletin*") with page links. Some 500 issues; OCR is
   fair (sampled 1964); titles need cleaning. About a week, the 1968 gap read from HathiTrust by hand or left
   "Check".
2. **A concordance from FRUS's own footnotes**, cheap and exact: the daybook already reads every FRUS volume's TEI;
   a pass over its footnotes for "Current Documents, <year>, pages …" and "*Bulletin*, <date>, p. …" gives, under each
   FRUS document, where it was printed at the time, and the date it was made public, which is what the brief's
   "Made public:" line wants. Half a day to a day. The *Bulletin* references can be linked at once; the *Current
   Documents* ones stay unlinked until a copy is found.
3. **Systematic citation in the calendar**: cards for both (`w.current-documents-1962`, one a volume, and the
   *Bulletin* as a periodical with links by volume), then convert the nineteen plain citations, and add the
   *Bulletin*'s text of a statement wherever an entry now cites only a newspaper for a public statement of the
   Department or the President abroad.
4. ***Current Documents* as a daybook list**: each annual volume numbers its documents within chapters, each with
   its date and source; an index of every document by date would be the best single map of the public record of
   foreign policy, 1959–67, but needs an open scan. If the owner can open HathiTrust's copies in a browser, the
   volumes' lists of documents (front matter, perhaps 30 pages a volume) could be read by hand or OCR'd from
   downloaded page images.

**Recommendation.** 2 first (a day; it links FRUS to both and dates publications), then 1 (a week), then 3. 4 waits
on a copy of *Current Documents*.

---

## Summary of recommendations and sizes

| Question | First step | Size |
|---|---|---|
| 1 State and city finance | A State-finance table and maps each fiscal year from Census's database (open, read); the missing first sales and income taxes as entries | ~2 days + 1 day of entries |
| 2 Federal fiscal policy | The seven missing debt-limit acts; revenue effects (OTA WP-81); each fiscal year by source and function (FRASER budgets + OMB tables); then bill-history tables from the History of Bills | ~3 days, then ~4 |
| 3 Committees and leaders | Nelson's assignments (open, read) into `congress/` blocks with leadership and rank | ~4–5 days |
| 4 Committee proceedings | The bound Daily Digest (govinfo, open, read) into a daily "Committees" list | ~1 week |
| 5 Conventions | Republican 1968 (open Proceedings): apportionment, selection method, first ballot, roll calls; the rest from borrowed Bain and Parris | ~3 days a convention |
| 6 *Current Documents*, *Bulletin* | FRUS footnote concordance; *Bulletin* daybook from the BPL volumes on archive.org | 1 day; 1 week |
