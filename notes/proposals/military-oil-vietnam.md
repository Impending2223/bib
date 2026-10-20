# Deployments, deaths, forces, oil, and the war in Vietnam: what can be sourced

Memo for the owner, Oct. 20, 2026. Five questions, one section each. Every link was tested from this
environment on Oct. 20, 2026. The labels:

- **open**: the page or file came down (HTTP 200, the content checked).
- **bot-checked**: a Cloudflare or similar challenge came back; a person in a browser can open it.
- **catalog only**: a catalog record answers (HathiTrust's Bib API, NARA's catalog), not the text.
- **paper only**: no online copy found.
- **refused here**: this environment's network refused the host or its TLS chain failed (most `.mil`
  sites: history.army.mil, history.defense.gov, media.defense.gov, usmcu.edu, history.navy.mil; also Texas
  Tech's Vietnam Center, the Wilson Center's Digital Archive, data.mil, web.archive.org's page server). These are
  open on the public web; the owner can allow a host in the environment's network settings.

"Not verified" marks a claim taken from memory or a description I could not check here.

---

## 1. U.S. deployments and deaths in Vietnam: cadence, and an indicator series?

**Answer: yes, both, monthly. Deaths can be had by the day; strength by the month (published then by the
week), and semiannually in the DoD's own printed tables.**

### Deaths

- **NARA, Defense Casualty Analysis System (DCAS), Vietnam Conflict Extract Data File, as of Apr. 29, 2008**
  (RG 330, NAID 2240992). One record a death, 58,220 records, pipe-delimited, 24 MB. Fields: service, rank, pay
  grade, occupation, date of birth, home of record (city, county, State), **incident or death date (YYYYMMDD)**,
  province and country of casualty, unit, hostile or not, casualty type and reason (small arms, artillery,
  aircraft), aircraft type, Wall panel. Downloaded and read here.
  [Catalog](https://catalog.archives.gov/id/2240992) (open);
  [data file](https://catalog.archives.gov/medialive/92/2409/2240992/content/arcmedia/electronic-records/rg-330/dcase/DCAS.VN.EXT08.DAT) (open);
  [layout](https://catalog.archives.gov/medialive/92/2409/2240992/content/arcmedia/electronic-records/rg-330/dcase/DCAS.VN08.DOC.PDF) (open).
  NARA's own yearly counts from it: 1965, 1,928; 1966, 6,350; 1967, 11,363; 1968, 16,899; 1969, 11,780
  ([NARA, statistics](https://www.archives.gov/research/military/vietnam-war/casualty-statistics), open). My
  tally of the file by month agrees (Feb. 1968, 2,259 deaths, 2,112 hostile; May 1968, 2,416, 2,257 hostile).
  In 1968: Quang Tri 3,290, Quang Nam 2,400, Thua Thien 2,056; South Vietnam 16,613, North Vietnam 141, Laos 116.
- **NARA, Combat Area Casualties Current File (CACCF), as of Dec. 1998** (NAID 1965870), its predecessor:
  fixed-width, 58,193 records; its date is "date of death or date declared dead" (so 447 deaths fall in 1978,
  the missing declared dead). [Catalog](https://catalog.archives.gov/id/1965870) (open);
  [data file](https://catalog.archives.gov/medialive/70/9658/1965870/content/arcmedia/electronic-records/rg-330/cacdb/CAC.DEC98.CURRENT)
  (open). The DCAS file is the better base (incident date). NARA's AAD search front end answers 403 here.
- **As reported then.** MACV and the Pentagon announced the week's dead, wounded and the cumulative totals each
  Thursday (Saigon), printed in the papers the next day (not verified here: the NYT's TimesMachine is behind
  its login; a person can read it). DoD's printed tables: *Selected Manpower Statistics*, annual (OASD
  Comptroller, Directorate for Information Operations), carry "Casualties ... in connection with the conflict in
  Vietnam" by year and a table "U.S. military personnel in South Vietnam, 1960–1973"
  ([FY-74 ed., 1975, DTIC copy](https://archive.org/details/DTIC_ADA043053), open;
  [FY-63 ed.](https://archive.org/details/DTIC_AD0498411), open). The *Statistical Abstract* printed
  the same yearly ([1969 ed., parts](https://www.census.gov/library/publications/1969/compendia/statab/90ed.html),
  open; scanned, no text layer).
- OASD(SA)'s *Southeast Asia Analysis Report* (monthly, 1967–72; 50 issues) carried weekly and monthly death
  and loss figures; all of it reprinted in Thayer, *A Systems Analysis View of the Vietnam War, 1965–1972*,
  12 vols. (1975), on DTIC and the Internet Archive, open: vol. 8 *Casualties and Losses*
  ([DTIC ADA051613](https://archive.org/details/DTIC_ADA051613)); one 1967 issue alone
  ([DTIC ADA050629](https://archive.org/details/DTIC_ADA050629)). OCR poor; tables to be read from the page images.
- "U.S. Casualties in Southeast Asia" (DoD's statistical summary): not found online here; not verified.

### Strength

- **Semiannual, 1960–73**, by service: *Selected Manpower Statistics* FY-74, "U.S. Military Personnel in South
  Vietnam 1960–1973" (Dec. 31 and June 30 each year; 31 Dec 1960 "about 900"; 31 Dec 1961, 3,200; 30 June 1962,
  9,000; 31 Dec 1962, 11,300 ...), open (above).
- **Monthly**: MACV's month-end strength is in the MACV Command Histories (annual, 1964–73) and in Thayer, vol. 2
  *Forces and Manpower* ([DTIC ADA051609](https://archive.org/details/DTIC_ADA051609), open), which draws on the MACV
  monthly order-of-battle summaries (the deployment programs there: not checked in detail). The MACV histories are said to be
  at Texas Tech's Virtual Vietnam Archive (refused here; not verified).
- **Weekly, as announced then**: the MACV weekly strength figure in the press (not verified here).
- Allied (Korean, Australian, Thai, Philippine, New Zealand) and RVNAF strengths: Thayer vols. 2, 6, 7.

### What to build

1. **An indicator series, monthly, under the month's table, in a group of its own ("The war")**: U.S. deaths in
   Southeast Asia, hostile and all, by incident month (today: DCAS, exact counts, cited to the NARA file); beside
   it "as reported then", the cumulative announced each week and summed to the month (the Thursday release as
   printed, page by page), from Jan. 1965; before 1965 the yearly figures only. Second row: U.S. military
   personnel in South Vietnam, month-end (today: MACV/Thayer; then: the weekly announced strength; the DoD
   semiannual table as a check). This fits the indicators' "first vs. now" form exactly: the announced weekly
   figures were revised (late reports, missing declared dead).
2. **A map a year, deaths by home State per 100,000** (the DCAS home-of-record field), drawn with the series'
   State maps; and **deaths by province** in South Vietnam (needs province shapes; see question 5).
3. **Calendar entries**: the troop decisions (Programs 1–6, the ceilings), each dated by its record; the
   1,000th, 10,000th ... dead as reported at the time (a "trace" of the kind the brief asks for).
4. **Names**: the file names every man; the Names pages need nothing from it. Don't add 58,000 people.

Cost: deaths "now" column, a script over one file, half a day. "Then" column, a person reading ~210 weekly
releases in TimesMachine (two or three days), or the SEA Analysis Report's tables by eye (a day). Strength, two
days by eye. State maps, a day on top of the existing machinery.

---

## 2. U.S. forces and materiel; forces abroad by country; allies, adversaries, others

**Answer: men under arms by month or quarter (U.S.), by country quarterly at best (classified detail then);
aircraft and missiles by quarter (USAF); ships and nuclear weapons by year; others' forces by year.**

### United States

- **Men under arms, total and by service**: *Selected Manpower Statistics* (annual; monthly end-strengths in its
  tables), above, open for FY-63 and FY-74 (whose tables run back to 1950). Annual Reports of the Secretary of
  Defense and the posture statements: history.defense.gov (refused here); not checked in HathiTrust.
- **By country**: *Selected Manpower Statistics* FY-74 prints "U.S. Military Strength Outside the United States,
  as of March 31, 1975" by country (Germany 219,000; Japan incl. Okinawa 51,000; Korea 42,000; U.K. 21,000;
  Thailand 23,000 ...), open, above. For 1960–69 by country: DoD's quarterly report "Active Duty Military
  Personnel Strengths by Regional Area and by Country" (DIOR 309A), and DMDC's historical files, are the source
  of Tim Kane's dataset (Heritage, 2006, by country and year from 1950; not verified past the title):
  [Heritage](https://www.heritage.org/defense/report/global-us-troop-deployment-1950-2005) (bot-checked);
  [DMDC reports](https://dwp.dmdc.osd.mil/dwp/app/dod-data-reports/workforce-reports) (open, but a script-driven
  page; the 1950s–60s historical files not reached; not verified). The 1980s quarterly *Worldwide Manpower
  Distribution by Geographical Area* is on DTIC/IA (e.g. [ADA152842](https://archive.org/details/DTIC_ADA152842),
  open); the 1960s editions not found there. The FY-63 *Selected Manpower Statistics* gives civilians by country
  but no military table by country (the military figures were then withheld; not verified why).
- **Aircraft and missiles**: *United States Air Force Statistical Digest*, annual, FY1960–FY1969 all on the
  Internet Archive from DTIC, open (e.g. [FY1965](https://archive.org/details/DTIC_ADA640754),
  [FY1968](https://archive.org/details/DTIC_ADA640755), [FY1969](https://archive.org/details/DTIC_ADA551709)).
  Its tables: combat forces by kind of unit and by geographical area; aircraft by mission and design at the end
  of each quarter; missiles by design; readiness; flying hours; losses; fuel issues by location, by quarter.
  OCR fair; tables by eye.
- **Ships**: NHHC's "U.S. Ship Force Levels, 1886–present" (year-end active ships by type) (refused here, TLS;
  not verified for 1960–69 detail).
- **Nuclear weapons**: DOE OpenNet table (1994) of the U.S. stockpile by year with megatonnage, builds,
  retirements ([OpenNet](https://www.osti.gov/opennet/forms?formurl=document/press/pc26tab1.html), open; totals
  printed only to 1961: 1960, 18,638; 1961, 22,229). DoD's fact sheet of May 3, 2010 gave the rest (1967 peak,
  31,255) (defense.gov refused here). FAS's figures, as Our World in Data republishes them, give every nuclear
  state by year: U.S. 1960, 18,638; 1964, 29,463; 1967, 31,255; 1968, 29,561; USSR 1960, 1,627; 1968, 9,490;
  U.K. 1968, 317; France 36; China 35 ([OWID CSV](https://ourworldindata.org/grapher/nuclear-warhead-stockpiles),
  open; [FAS](https://fas.org/initiative/status-world-nuclear-forces/), open). Kristensen and Norris, "Global
  nuclear weapons inventories, 1945–2013," *Bull. Atomic Scientists* (2013) (bot-checked). Delivery vehicles
  (ICBMs, SLBMs, bombers): the USAF Digest for the Air Force; *Nuclear Weapons Databook*, vol. I (NRDC 1984)
  ([IA](https://archive.org/details/nuclearweaponsda0001unse), borrow only).

### Others

- **IISS, *The Military Balance***, annual from 1959 (the early titles varied; not verified): every state's
  forces, men, main equipment. Internet Archive copies are lending only
  ([1959 record](https://archive.org/details/militarybalance0000unse_f2m5)); HathiTrust search-only
  ([catalog, ISSN 0459-7222](https://catalog.hathitrust.org/api/volumes/brief/issn/0459-7222.json), catalog
  only); Taylor & Francis (bot-checked; subscription). Paper or a library login.
- **SIPRI Yearbook**, from 1968/69: the first is a free PDF
  ([SIPRI Yearbook 1968–69](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf),
  open, 8.8 MB; [archive](https://www.sipri.org/yearbook/archive), open). **SIPRI Military Expenditure
  Database, 1949–2025**, yearly by country ([xlsx](https://www.sipri.org/sites/default/files/SIPRI-Milex-data-1949-2025_v1.2.xlsx), open).
  Arms transfers database from 1950 ([page](https://www.sipri.org/databases/armstransfers), open).
- **Correlates of War, National Material Capabilities v7**: every state, yearly to 2016: military expenditure,
  military personnel, iron and steel, energy, population ([zip](https://correlatesofwar.org/wp-content/uploads/NMCv7.zip),
  open; read here: U.S. 1968, 3,550,000 men, $80.7 bn; USSR 4,100,000; China 2,800,000; North Vietnam 447,000;
  West Germany 490,000). Coarse, retrospective, no "as then" column.
- **Soviet and Chinese forces as Washington estimated them**: the NIEs (11-8 strategic attack, 11-14 general
  purpose forces, 13- China), in FRUS (in the daybook already, by date) and the CIA's reading room
  ([CIA FOIA](https://www.cia.gov/readingroom/), open; its search does not answer a script; many documents are
  mirrored on the Internet Archive, e.g. [NIE 11-8-59](https://archive.org/details/cia-readingroom-document-cia-rdp79r00904a000500010002-6), open).
  Donald P. Steury ed., *Intentions and Capabilities: Estimates on Soviet Strategic Forces, 1950–1983* (CIA 1996)
  ([DTIC ADA500074](https://archive.org/details/DTIC_ADA500074), open).

### What to build

1. **A "Forces" table in the calendar, at each year's December (or each fiscal year's June)**, not each month:
   U.S. active duty by service; outside the U.S. and in the main countries (Germany, Japan, Korea, the U.K., South
   Vietnam, Thailand); USAF aircraft by mission and missiles by type (the Digest, end of quarter: these could go
   quarterly); nuclear stockpile (then: not published; today: the 2010 figures). The "first" column only where a
   figure was published then (the Digest was classified; *Selected Manpower Statistics* was not).
2. **A world table a year** (in the calendar's January, or a page of its own): the Military Balance's figures
   as printed that year (men, divisions, tanks, combat aircraft, major warships, ICBMs/SLBMs/bombers) for the
   U.S., USSR, China, the U.K., France, West Germany, Japan, India, Israel, Egypt, the two Vietnams, the two
   Koreas; beside it COW's and SIPRI's figures today. This is the "as then / as now" form, by year.
3. **Calendar entries** for the estimates themselves (each NIE 11-8 as a dated record: what Washington thought the
   Soviet force was), threaded with the missile gap.

Cost: the Digest's quarterly aircraft and missile rows, 1960–69, by eye, three to four days. The Military
Balance, ten editions, by eye, needs the books (paper or a library login): five days. Kane/DMDC by country:
blocked here; if the owner fetches the file, a day. COW and SIPRI: an hour each.

---

## 3. Petroleum: production, consumption, trade, reserves, finds, refining; and the 1960 baseline

### What the calendar holds now (read-only search)

`./bib find -l cal oil` gives 31 entries, `petroleum` 3, `opec` 3. On the oil itself: OPEC's founding, Baghdad,
Sept. 10–21, 1960 (FRUS, Sampson, Skeet, Yergin, Garavini); Iraq's Law 80, Dec. 11, 1961; Iran's consortium,
Oct.–Nov. 1966; Khartoum, Sept. 1, 1967; Prudhoe Bay, Mar. 12, 1968 (Wikipedia only; "Check: the day"); the
Haiphong POL strikes, June 29, 1966; Rhodesia's oil, 1965–67; the excise and depletion debates in passing.
**Nothing on the Mandatory Oil Import Program**, though the daybook already holds its every amendment by date:
Proc. 3386 and 3389 (Dec. 1960, Jan. 1961), 3509 (Nov. 1962), 3531, 3541 (1963), 3693 (Dec. 1965), 3779,
3794 (1967), 3820, 3823 (1968), with Kennedy's statements on them. **Nothing on the June 1967 Arab oil
embargo**, though FRUS 1964–68, XXXIV (Energy Diplomacy), docs. 230–237 (June 3–7, 1967) are in the daybook.
Nothing on Libya's oil (found 1959, exporting 1961), Algeria's, Nigeria's, Abu Dhabi's, or the North Sea.

### Sources

- **EIA, U.S.** (all open):
  [monthly crude production from Jan. 1920](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=MCRFPUS2&f=M);
  [*Monthly Energy Review* Table 3.1, petroleum overview](https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T03.01)
  (CSV: production, imports, exports, net imports, products supplied, stocks; **annual from 1949, monthly from
  1973**); [product supplied, monthly from 1963](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=MTTUPUS2&f=M);
  [crude proved reserves, annual from 1900](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RCRR01NUS_1&f=A);
  imports monthly only from 1973 (the monthly series before that must come from the Bureau of Mines);
  refinery capacity in the navigator only from 1982–85 (the earlier Jan. 1 capacities from the Bureau's annual
  refinery surveys; not verified online).
- **Bureau of Mines, *Minerals Yearbook***, annual, vol. II *Fuels* (1959–65; vols. I–II together 1966–69):
  U.S. production by State, refinery runs and capacity, imports by country of origin, exports, stocks, **world
  production by country**, reserves. All on the Internet Archive, open (e.g.
  [1960, vol. II](https://archive.org/details/pub_usgov-minerals-yearbook_1960_2),
  [1965, vol. II](https://archive.org/details/pub_usgov-minerals-yearbook_1965_2),
  [1968, vols. I–II](https://archive.org/details/pub_usgov-minerals-yearbook_1968_12)); and full view in
  HathiTrust ([catalog, ISSN 0076-8952](https://catalog.hathitrust.org/api/volumes/brief/issn/0076-8952.json),
  1,731 volumes, full view). OCR poor in the tables (read by eye from the PDF).
- **Bureau of Mines, *Mineral Industry Surveys*, "Crude Petroleum and Petroleum Products," monthly**: the
  as-first-reported monthly U.S. figures. Not found online here (Internet Archive: none); HathiTrust likely
  (not verified). Paper otherwise.
- **API, *Petroleum Facts and Figures*** (biennial): the Internet Archive has editions to 1950 only
  ([1950](https://archive.org/details/bwb_C0-AQX-796)); 1959–71 editions not found (not verified).
- ***Oil & Gas Journal***: the year-end worldwide reserves and production issue and the refining survey;
  HathiTrust search-only for the 1960s ([catalog](https://catalog.hathitrust.org/api/volumes/brief/issn/0030-1388.json),
  catalog only). Paper or a library.
- **BP / Energy Institute *Statistical Review*** (production and consumption by country, 1965 on in the
  workbook): [Energy Institute](https://www.energyinst.org/statistical-review) (bot-checked). Not a 1960 source.
- **OPEC *Annual Statistical Bulletin*** (posted prices, production, from 1960): [OPEC](https://www.opec.org/opec_web/en/publications/202.htm) (bot-checked).
- **The import program**: the proclamations (APP, in the daybook; the Federal Register); the Cabinet Task Force on
  Oil Import Control, *The Oil Import Question* (Feb. 1970, after the span); Shaffer, *The Oil Import Program of
  the United States* (1968) ([IA](https://archive.org/details/oilimportprogram0000shaf), borrow only).

### Was the 1960 baseline "complete"? What the figures say

The owner's picture (U.S. a net exporter, Venezuela the second Western source, the Middle East underdeveloped)
is the picture of about 1945–47, not of 1960. By January 1960:

- The U.S. was a net importer: 318,000 b/d net in 1949 (EIA's series begins there), 1,613,000 b/d in 1960, 16
  percent of 9.8 million b/d supplied (EIA MER 3.1, above). Imports were capped by Proc. 3279 of Mar. 10, 1959.
- The Middle East already outproduced Venezuela: 1960, Kuwait 594 million barrels, Saudi Arabia 456 million;
  Venezuela 1,042 million (*Minerals Yearbook* 1960, II, table 89, p. 487; Iran's and Iraq's figures garbled in
  the OCR, to be read from the page). The Yearbook's text: Eastern Hemisphere output up 16.2 percent in 1960,
  "no commercial production in Libya," Libyan output "scheduled to begin in 1961"; the U.S.S.R. second in the
  world at 1,080 million barrels.
- What was still to come within the span: OPEC (Sept. 1960); Libya's rise; U.S. production rising to its peak
  (EIA: 7.04 million b/d in 1960, 9.10 in 1968, 9.64 in 1970, the highest; falling after); the closing of the
  Suez Canal (June 1967) and the embargo of 1967, which U.S. spare capacity answered; Prudhoe Bay (1968). After it:
  Ekofisk (Dec. 1969), Tripoli and Tehran (1971), 1973.

So the transition is largely complete on the ground by 1960 and the calendar opens mid-story. It does not now
tell it: no import program, no 1967 embargo, no U.S. figures.

### What to build

1. **An indicator group "Oil"** in the month's table: U.S. crude production (monthly, EIA "now"; Bureau of Mines
   monthly survey "first", if found); imports and net imports (yearly 1960–72 from EIA in December; monthly
   "first" from the Bureau's surveys); products supplied (monthly from 1963); the posted price of Arabian light at
   Ras Tanura ($1.80 from Aug. 1960, unchanged to 1970; not verified here; OPEC or *Platt's*); proved reserves,
   U.S. (yearly). Cost: EIA rows, half a day; the Bureau's monthly "first" figures, if HathiTrust has them, three
   days by eye; posted prices, a day.
2. **A world table a year**: crude production by country (the *Minerals Yearbook*'s table as printed that year,
   and the Energy Institute's figure today), the big producers only (U.S., USSR, Venezuela, Kuwait, Saudi
   Arabia, Iran, Iraq, Libya, Algeria, Canada, Indonesia, Nigeria, Abu Dhabi). Ten tables by eye: three days.
3. **Calendar entries** (a new thread "Oil", or the Middle East and Economy threads): each import proclamation
   (eleven, all in the daybook); the June 1967 embargo and the Foreign Petroleum Supply Committee (FRUS XXXIV,
   230–237 and after); Libya's first export (Sept. 1961; not verified); the Kuwait and Saudi finds as they affected
   policy (fewer); the Interior Department's quota fights (the Machiasport refinery, 1968; not verified). About 20
   entries: two days.
4. Not a map, unless of world production by country a year (the series has no world map now).

---

## 4. Vietnam: what the calendar is missing, and how to give a day-by-day, operational account

### What the calendar's Vietnam thread now cites (read-only count)

428 entries carry `vietnam` as thread or `also`. In them: FRUS in 253, APP in 101, the Miller Center tapes in 19,
govinfo in 9. Works cited most: Gallup (99), Gibbons, the set and its Pt. 4 (40), the Pentagon Papers, Gravel ed. (24),
Logevall, *Choosing War* (23), Herring, *Secret Diplomacy* (21) and *LBJ and Vietnam* (20), Kaiser (20), Johnson,
*Vantage Point* (18), McNamara (17), Berman (14), Taylor, McMaster, Clifford, Westmoreland (13 each). The
official operational histories barely: Carland's and Spector's Army volumes 5 each, Shulimson's Marine volume of
1965 4, Hunt, *Pacification* 3; Cosmas's *MACV* 1; Van Staaveren's *Interdiction in Southern Laos* 0; Thayer, *War
Without Fronts* 0; Sharp and Westmoreland, *Report on the War* 0; the PAVN official history (*Victory in
Vietnam*, Pribbenow trans.) 0, and it has **two cards** (`w.viet-victory-in-vietnam`, `w.vietnam-victory-in-vietnam`:
a `works combine` candidate). The full Pentagon study has two cards too, with different printings
(`w.def-u-s-viet-rels`, NARA 2011 release, cited twice; `w.united-states-vietnam-relations`, HASC 1971, cited
never); check whether they are one work. Viet. II.F.12 "Statistics" holds one work (Clodfelter).

So the calendar records Washington's war (decisions, memoranda, tapes, opinion) and has little of the field.

### Sources not yet used, by what they give

- **The Pentagon Papers, the full report** (OSD Vietnam Task Force, 1969; NARA's release of June 2011), 48 PDFs
  by part ([NARA](https://www.archives.gov/research/pentagon-papers), open; each part on S3, e.g.
  [IV.C.6.a](https://nara-media-001.s3.amazonaws.com/arcmedia/research/pentagon-papers/Pentagon-Papers-Part-IV-C-6-a.pdf),
  open). Gravel lacks the negotiation volumes (VI.C) and some of the documents (not checked part by part); cite
  NARA's part and page where Gravel has nothing.
- **MACV Command Histories** (annual, 1964–73, with monthly strength, operations, logistics, enemy order of
  battle) and **CINCPAC Command Histories** (annual): MACV's said to be at Texas Tech (refused here, not
  verified); CINCPAC's 1962–73 in part on the Internet Archive from the "U.S. Intelligence on China" set (e.g.
  [1966, vol. I](https://archive.org/details/us-china-intel-CI01811); not checked for access). Sharp and Westmoreland,
  *Report on the War in Vietnam (as of 30 June 1968)* ([IA](https://archive.org/details/reportonwarinvie0000unit), borrow only).
- **Thayer, *A Systems Analysis View of the Vietnam War, 1965–1972***, 12 vols., every article of OASD(SA)'s
  monthly *Southeast Asia Analysis Report*, open on the Internet Archive: [1 Situation](https://archive.org/details/DTIC_ADA039313),
  [2 Forces and Manpower](https://archive.org/details/DTIC_ADA051609), [3 VC/NVA](https://archive.org/details/DTIC_ADA039314),
  [4 Allied Ground and Naval Operations](https://archive.org/details/DTIC_ADA051610), [5 The Air War](https://archive.org/details/DTIC_ADA051611),
  [6](https://archive.org/details/DTIC_ADA039315) and [7](https://archive.org/details/DTIC_ADA051612) RVNAF,
  [8 Casualties and Losses](https://archive.org/details/DTIC_ADA051613), [9 Population Security](https://archive.org/details/DTIC_ADA039316),
  [10 Pacification and Civil Affairs](https://archive.org/details/DTIC_ADA039317), [11 Economics](https://archive.org/details/DTIC_ADA051614),
  [12 Construction and Ports](https://archive.org/details/DTIC_ADA051615). Each article dated by its issue: a
  calendar of what OSD measured, month by month, 1967–72. Also Thayer, *How to Analyze a War Without Fronts*
  (1975) ([IA](https://archive.org/details/howtoanalyzewarw00thay), open).
- **NARA's electronic records of the war** (RG 330, 472, 218, 529), open, downloadable through the catalog:
  - **CACTA**, Combat Air Activities File (CINCPAC), one record a sortie: date, unit, aircraft, base, target
    country, province, coordinates, ordnance, results, losses; monthly files Oct. 1965–Jan. 1971 (59 found)
    ([Jan. 1968](https://catalog.archives.gov/id/2190420), open; [layout](https://catalog.archives.gov/medialive/20/1904/2190420/content/electronic-records/rg-529/CACTA/CACTA.PC.TR.LAY), open).
  - **SEADAB**, Southeast Asia Data Base (JCS), the same for 1970–75 ([1970](https://catalog.archives.gov/id/1937092), open).
  - THOR, the Air Force's consolidated bombing database (1965–75), released 2015 on data.mil (refused here) and
    data.world (closed: it now redirects to "goodbye"); a Kaggle copy answers (login to download; not tested).
  - **DCAS** (deaths), above; **HES** and the pacification files, question 5.
  - **USMC command chronologies**, monthly, every unit, page images (series NAID 6160409): narrative,
    significant events, losses, enemy order of battle (e.g. [MACV enemy order of battle, Dec. 31, 1967](https://catalog.archives.gov/id/6622111),
    [III MAF order of battle, May 1969](https://catalog.archives.gov/id/6621548), open).
- **The official histories**, most already carded: CMH's U.S. Army in Vietnam (history.army.mil refused here;
  one volume in IA lending); the Marine Corps' *U.S. Marines in Vietnam* (open on IA for 1966, 1967, 1968, 1969,
  1970–71: [1966](https://archive.org/details/AnExpandingWar), [1967](https://archive.org/details/FightingTheNorthVietnamese),
  [1968](https://archive.org/details/USMarinesInVietnamTheDefiningYear1968), [1969](https://archive.org/details/HighMobilityAndStanddown));
  the Air Force's *USAF in Southeast Asia* (media.defense.gov refused here). The Navy's (Marolda and others): not checked.
- **The other side**: *Victory in Vietnam* (PAVN official history, Pribbenow trans., 2002) (HathiTrust search-only,
  [catalog](https://catalog.hathitrust.org/api/volumes/brief/isbn/0700611754.json)); Pribbenow, *Rolling Thunder and
  Linebacker: The North Vietnamese View* (carded, cited once); the nine-volume *Lịch sử kháng chiến chống Mỹ cứu
  nước* and the PAVN unit and regional histories (not verified online); CDEC captured documents and the RAND
  Viet Cong Motivation and Morale interviews (at Texas Tech; refused here); Thayer vol. 3 (MACV's estimates of
  infiltration, strength, losses, by month); the Wilson Center's CWIHP documents (refused here).
- **The tapes**: the Miller Center, already the calendar's record (19 entries in the thread).

### What to build

1. **Use the operational record in the calendar at the month level, not the day**: one entry a month in a new
   thread "The war in the field" (or under `vietnam` with `also`), from Mar. 1965: the month's major operations
   (from the official histories and the USMC chronologies), U.S. and allied strength, U.S. and RVNAF deaths, the
   enemy's estimated strength and infiltration (MACV, Thayer vol. 3), sorties flown North and in Laos (CACTA),
   each with its record. About 46 entries, 1965–Jan. 1969. Cost: two to three weeks.
2. **Day-by-day where the record supports it**: the big operations and battles get their own dated entries with
   their first entry's bibliography (Starlite, Ia Drang, Junction City, Dak To, Khe Sanh, Tet, Hue, the May
   offensive), the official volume cited by page. About 40 entries; a week.
3. **Air war tables from CACTA**: sorties and tonnage by month, by country (North Vietnam by route package, Laos,
   South Vietnam), U.S. aircraft lost; as indicator rows ("The war" group) from Oct. 1965. A script; the files are
   ~37 MB a month, 64 months: two to three days with checking against Thayer vol. 5.
4. **Add the missing cards and listings**: the NARA Pentagon Papers parts (one card with parts, or one per part),
   Thayer's twelve volumes, the MACV and CINCPAC histories, the USMC chronologies, the NARA electronic files as
   records; combine the duplicate *Victory in Vietnam* cards. A day.
5. Not narrative. The brief asks for pointers; the gain is in records cited and figures dated.

---

## 5. Control of territory, population and roads in South Vietnam

### Data

- **Hamlet Evaluation System (HES)**, monthly, Jan. 1967–1973 (HES/70 and HES/71 from 1969), every hamlet rated
  (A–E, V), with population, the questions behind the rating, and a location. NARA, RG 330 and 472, open,
  downloadable: HAMLA 1967 ([NAID 4658138](https://catalog.archives.gov/id/4658138): two tab-delimited files,
  25 and 32 MB, rows by hamlet and month from 6701; [layout](https://catalog.archives.gov/medialz/electronic-records/rg-330/HES/HAMLA.67ARLAY.html)),
  HAMLA 1968 and 1969 (NAIDs 4658141, 4658144), HES70 (4658133, 4658136), HES71 (4658121–4658131, to Jan. 1974),
  HAMDA summaries by province and corps, 1967–69 ([4658152](https://catalog.archives.gov/id/4658152)), the HES
  Basic Master File 7/1969–1/1973 (273777646).
- **The HES gazetteer** ([NAID 4628241](https://catalog.archives.gov/id/4628241), open): 18,934 records, corps,
  province, district, village and hamlet codes and names, **MGRS grid coordinates by hamlet** (e.g. "YD4665849"),
  population; as of Jan. 1973 (read here). The base for any map.
- Related NARA files, open: Territorial Forces Evaluation System (TFES, 1970–72), National Police (NAPE), Terrorist
  Incident Reporting (TIRSA), the Pacification Attitude Analysis System (PAAS, Mar. 1970–Dec. 1972,
  [289871940](https://catalog.archives.gov/id/289871940)), VNUS.
- **Dell and Querubin, "Nation Building Through Foreign Intervention" (QJE 2018), replication files**, CC0,
  575 MB ([Dataverse](https://doi.org/10.7910/DVN/F4WUD6), open; listed here): hamlet coordinates (`coords.dta`),
  HES 1969–71 recoded, SITRA (Army situation reports), PAAS, the Marines' hamlets, a bombing file, French-era
  roads, markets and posts. A cleaned panel ready to map; mostly after Jan. 1969.
- **Studies of HES**: Kalyvas and Kocher, "The Dynamics of Violence in Vietnam: An Analysis of the Hamlet
  Evaluation System (HES)," *J. Peace Research* (2009) (publisher bot-checked; not read); *Hamlet Evaluation System Study* (1968)
  ([DTIC AD0839821](https://archive.org/details/DTIC_AD0839821), open); *U.S. Progress Reports for the Vietnam War,
  1967–68* (1990) ([DTIC ADA226232](https://archive.org/details/DTIC_ADA226232), open); "A History of the Hamlet
  Evaluation System" (CIA reading room, via [IA](https://archive.org/details/cia-readingroom-document-cia-rdp80r01720r000200120001-2), open);
  Thayer vol. 9, *Population Security*, every HES article 1967–72 (open, above).
- **Before HES (1962–66)**: the Strategic Hamlet Program's claimed counts (hamlets "completed," population) in the
  GVN and MAAG reports, in FRUS 1961–63, II–IV (in the daybook) and the Pentagon Papers IV.B.2, "The Strategic
  Hamlet Program, 1961–1963" ([NARA](https://nara-media-001.s3.amazonaws.com/arcmedia/research/pentagon-papers/Pentagon-Papers-Part-IV-B-2.pdf),
  open). Province-level estimates of control by MACV and the CIA, 1964–66, in the Pentagon Papers IV.C and FRUS;
  no hamlet-level data before 1967 (not verified that none survives).
- **Maps and boundaries**: no 1960s province or district shapefile found. The University of Texas's scans of the
  1:250,000 L7014 sheets and the province maps (bot-checked); CIA's "Population Control Map of South Vietnam"
  (1972) on the Internet Archive ([IA](https://archive.org/details/cia-readingroom-document-cia-rdp80t01719r000300270002-1), open);
  the LOC's map search answers but slowly (not checked further). Province boundaries changed (Hau Nghia formed 1963,
  others later; not verified here); one can draw approximate provinces from the gazetteer's hamlet points and a coastline, and check
  them against a dated CIA or MACV map.
- **Lines of communication**: MACV's road and rail status maps in the Command Histories (not verified online);
  the CACTA target coordinates for interdiction (North Vietnam and Laos); Dell and Querubin's French-era roads.

### What to build

1. **A map of South Vietnam a quarter, Jan. 1967–Jan. 1969** (nine maps), hamlets as dots colored by HES
   security rating (A–B, C, D–E, V), with the population share "relatively secure" by corps and province in a
   table under it; carried, like the election maps, by a calendar entry tagged for the quarter. Data: HAMLA 1967–69
   and the gazetteer (MGRS to latitude/longitude with `mgrs` or `pyproj`). The series' map code (the congress
   maps) draws points and shapes already. Cost: a week, most of it decoding the HAMLA layouts and checking the
   totals against Thayer vol. 9.
2. **An indicator row, monthly from Jan. 1967**: population in A–B–C hamlets, percent (as reported then, from
   the monthly HES summaries Komer and MACV released and the SEA Analysis Report; today, recomputed from the
   files: the two differ, as the HES models were revised in 1969–70). A day after 1.
3. **1962–66**: no data series; calendar entries for the Strategic Hamlet claims and their collapse (FRUS,
   Pentagon Papers IV.B.2), and for the province estimates the Pentagon Papers quote. Two days.
4. **Province and district boundaries**: draw once (approximate), as above, for the deaths-by-province map
   (question 1) and the HES tables. Two to three days.

---

## Recommendations, in order

1. **U.S. deaths and strength in Vietnam, monthly, as an indicator group "The war"** (Q1): the data are in hand
   and open; one to two days for "now", two to three for "then".
2. **The oil import program, the 1967 embargo, and an "Oil" indicator group** (Q3): the records are already in the
   daybook; EIA is open; about a week together.
3. **HES maps and the hamlet-security row** (Q5), 1967–Jan. 1969: about a week; the strongest new picture of the
   war the series could show.
4. **Monthly field entries from the official histories, Thayer and CACTA** (Q4): two to four weeks; fix the two
   duplicate cards first.
5. **Forces tables a year** (Q2): U.S. from the USAF Digest and *Selected Manpower Statistics* (open); the world from
   the Military Balance (needs the books or a library login; IA and HathiTrust are lending or search-only). A week.

Hosts refused here that would help: history.army.mil, history.defense.gov, media.defense.gov (CMH, OSD history,
USAF histories), history.navy.mil (ship force levels), www.vietnam.ttu.edu (MACV histories, CDEC), the Wilson
Center's Digital Archive, data.mil (THOR), heritage.org (Kane; bot-checked).
