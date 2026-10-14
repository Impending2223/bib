# Leads, raw

What the drafting agents (calendar, State and local, threads, Executive roster) reported they could not place,
source or verify, copied from their reports of Oct. 2026, by report. To be sorted into `notes/leads.md`.

## I wrote the three NSC files and `./bib executive check` shows no errors in them. A test re

**People placed from part3.tsv and authors.tsv:** McGeorge Bundy, Rostow, Kissinger, Haig, Komer, Forrestal, Cooper (Chester), Thomson, Halperin, Lake, Lord, David Young, Taylor (PFIAB and the committees), Clifford (PFIAB), Kaysen, Robert H. Johnson, Bromley Smith, Brubeck, Klein, Saunders, Gordon Gray, Haskins, Landon, Kissinger's 1961 consultancy, Owen, Chase, Belk, Parrott, Thomas W. Davis, Orrick and Nitze (ExComm subcommittees). The `names` report leaves none of the NSC people unplaced; "Karl Kaysen" there is a FRUS misspelling of Carl Kaysen, who is placed.

  **Not placed:**
  - Legere (20 documents), assistant to the Military Representative of the President. That office belongs to the White House file, as do Taylor's 1961–62 post and Moyers.
  - "David W. Gray" (4 documents), probably the JCS officer, for the military agent.
  - "Ruth S" (3 documents) could not be identified.
  - I left out people who joined the staff only under Ford or Carter, or in a month of 1974 I couldn't establish: Oakley, Low, Hadley, Molander.

- **USIB texts:** the 1958 and 1972 texts of NSCID No. 1 were not found. Lay is recorded as USIB Executive Secretary only for Mar. 1964, in a note.
  - **Staff entries:** most month and year dates on both the 1953–69 and 1969–74 staffs, taken from FRUS volume ranges.

## Uniformed military and defense agencies, 1953–74: report

### Not placed (other units, or not offices)
  - **White House or the Executive Office of the President:** Taylor's 1961–62 post as Military Representative of the President is in no file yet. Neither are his staff Legere, Bagley (1961) and W. Y. Smith, or Clifton.
  - **Office of the Secretary of Defense:** Lansdale's special-operations posts (1957–63) are not in `defense.yaml`. Heinz, McCrea, and Craig and Harris (the Mongoose project officers) are not placed. ARPA is already there.
  - **CIA:** Cabell and Cushman as Deputy Director of Central Intelligence.
  - **Junior officers, left out as holding no office:** Moore, Vann, Robb, Nugent, Kerry, Stockdale, Denton, Thompson.

- **Holders not found:** Commander in Chief, Alaska (no holders at all); Northeast Command (not entered); MACTHAI after 1965; Seventh Air Force after 1973; SACSA after 1969.
  - **Staff posts held only to the year:** the operations deputy and Research and Development rows come from Congressional Directory snapshots.

## Interior and Agriculture roster: done

**Placed from part3, authors and the calendar:** Udall, Hickel, Morton, Freeman, Butz (as Secretary and as Assistant Secretary 1954–57), Benson, Hardin; and the FRUS persons Carr, Carver, Kelly, Train, Pecora, Whitaker, Dole, Frizzell, Paarlberg, Palmby, Brunthaver, Yeutter, Schnittker, Morse, Murphy, McConnell and others. McGovern (Food for Peace) is left to the White House agent; his post was not in USDA. `./bib executive names` reports no Interior or Agriculture persons unplaced.

## The three files are written: treasury.yaml, commerce.yaml and labor.yaml in /home/user/bib

- **Pre-1953 holders left out:** where the predecessor's 1953 end date could not be found, he is named in a note instead: Marzall (Patents), Peel (Census), Frieda Miller (Women's Bureau), Horne (Civil Aeronautics).
  - **Acting secretaries:** none found for the gaps of Sept.–Oct. 1953 (Labor), Feb. 15–29, 1972 (Commerce) and Jan. 20–22, 1969 (Treasury).

## I wrote 25 unit files for the independent regulatory commissions, boards and corporations,

**Persons from part3, authors, calendar and Public Papers, all placed:** Martin and Burns (FRB); Minow, and Burch (FCC chairman 1969–74); Weinberger (FTC chairman 1970); Dixon (FTC); Cary, Cohen, Budge, Casey and Garrett (SEC); Swidler, Lee C. White and Nassikas (FPC); Hannah, Hesburgh and Flemming (CCR); Roosevelt Jr., Shulman, Alexander and Brown III (EEOC); Wagner (TVA, from the Feb. 11, 1961 Public Papers item); Casey again as Export-Import Bank president from Mar. 14, 1974. `./bib executive names` shows nothing left unplaced for these bodies.

- **Acting chairmen not found:** SEC, Jan.–Apr. 1971 and Feb.–Mar. and May–Aug. 1973. The NLRB general counsel is also uncovered, Dec. 1954–Mar. 1955.
  - **Acting by statute, flagged:** some acting chairmen are entered only because the statute names the vice chairman or first vice president. These are Holcomb at the EEOC (1966, 1967), Horn at the CCR (1972–74) and Sauer at the Export-Import Bank (1973–74).
  - **Predecessors left out:** Herbert E. Gaston (Export-Import Bank) and Cyrus S. Ching (FMCS) are omitted, because their leaving dates are unknown and may fall before Jan. 20, 1953. Each office's note asks for the date.
  - **Sources that disagree with the Directory:** Wikipedia's FPC list gives later end dates for Wimberly, Nelson Lee Smith and Connole. The FMC list gives later start dates for Stakem, Barrett, Patterson and Bentley. The FTC list has Carson from 1948. The Directory is used in each case and the disagreement is noted.
  - **Not done:** the FEA Deputy Administrators.

  **Conflict in another agent's file:** interior.yaml has David S. Black as Under Secretary of the Interior from 1967-09. FPC records have him leaving the FPC on Sept. 13, 1966, and I recorded that he left to become Under Secretary (`out: To Under Secretary of the Interior`).

  Scratch files are in `/tmp/claude-0/-home-user-bib/f04c9307-7a44-53db-a3d0-26f3e1375c84/scratchpad/agents/commissions/`. The most useful: the Directory extracts (`cdir-*.txt`), the bios (`bio/`), the statute PDFs (`stat/`), and two helpers: `tools/sortholders.py` (sorts holders by date) and `gen/icc.py` (builds the ICC member list from the Directory editions).

## State, missions and foreign-affairs agencies: done

- **Not verified:**
    - The 1919 act's chapter number.
    - The section numbers for the Director General (60 Stat. 1000) and the Foreign Service Institute (§ 701, 60 Stat. 1018).
    - The 1958 U.S. Code section numbers beyond 5 U.S.C. §§ 151 and 151a.
    - Federal Register citations for EOs 11041 and 11603: I gave APP links instead.

- **About 250 unplaced FRUS author strings.** Mostly offices, fragments ("William E", "G"), foreigners, other departments' people (military aides Bagley, Legere, Clifton, Burris; Lansdale), or drafters with no persons-list entry I could identify (Swayne, Kupinsky, Dozier, Mudd, Plakias, Lamberty, Ruff, Nickel, Mountain, Moffett and others).
  - **Uncovered persons:** none in Part III or the calendar, and none of the identifiable State/USIA/AID/ACDA authors.
  - **Delegation chiefs:** Harriman's 1961–62 Laos conference delegation is not entered; my sources have no dates for it.
  - **Lower AID, USIA and ACDA posts** before 1961 and after 1969 are thin.
  - **Some vacancies have no acting officer:** the Under Secretary in 1970, the Counselor's gaps, and several Director General gaps.

## I finished the cleanup and coverage pass. `./bib executive check` and `./bib check` both r

- **Deliberately not placed:**
    - LaRue: Wikipedia says he had no White House title, salary or listing.
    - "Carl Rankin" and "Karl Kaysen" are FRUS misspellings of people already placed.
    - Stalder, Pardee and Rossow: no given name was found.
    - Also left out: foreign persons, members of Congress and their staff (Marcy, Valeo), justices, private persons (Fishel, Beesley), and initials-only fragments.

- **Not found:** Secretary of the Army (both 1961 and 1965), Navy 1954, ISA 1964, Interior Jan. 1969, Commerce Feb. 1972, Treasury Jan. 1969, Federal Highway Administration 1969, AEC chairman (1958 and 1973), SEC chairman (all three gaps). The SEC's own site refuses requests without a contact address, which I did not supply.

## I've added Senate nomination and confirmation dates from the bound Congressional Record to

**Matches I left out on purpose:**
  - **Confirmations for a reappointment to a new term, not the original appointment:** Brooke (FPC, 1969), Robertson (Home Loan Bank Board, 1957), Harper (Railroad Retirement Board, 1954), McMurray's 1974 renomination (National Mediation Board; his 1972 nomination is in), McSweeney's 1966 nomination as Minister to Bulgaria.
  - **Nominations that were withdrawn or never confirmed, where the confirmed one could not be told apart:** Twining as Air Force Chief, 1953; Stassen's FOA confirmation of Aug. 1, 1953; W. H. Brown III (EEOC); Gould (Netherlands, withdrawn 1973); Roderick's 1954 dates on his civil-military entry (they belong to his financial-management entry).
  - **Different posts with the same name:** alternate delegates to the UNESCO General Conference (Graham, W. B. Jones).
  - **Earlier nominations kept even though later ones exist,** because those are the dates the State agent recorded: Byroade, Allen (Near East), Tappin, Oliver, Mills, Laise, Cyr, Enders, Coombs, Powell, F. G. Meyer.

  **How the matching works.** I downloaded every remaining Senate day of the bound Record, 1,541 days, into the State agent's cache, so all 3,546 Senate days of 1953–74 now have text. I pulled each day's nominations received, confirmed, and withdrawn into 4,047 sections, checking every heading date against the day's own date (the misread February 1974 heading was among those fixed). Each holder was matched by surname, given name, and title wording within a date window, with the year's Index as a fallback. Where a nomination was sent in again in a new session, I recorded the one that was confirmed. Every flagged case I read by eye. The edits change only `nominated`, `confirmed` and `src` lines, and each file is checked after writing to confirm nothing else changed. Where a holder's `src` only pointed to a shared list, I wrote that list out in full for the holder. `src` gets "Cong. Rec." or "Cong. Rec. Index YYYY".

  Everything is in `/tmp/claude-0/-home-user-bib/f04c9307-7a44-53db-a3d0-26f3e1375c84/scratchpad/agents/noms/`:
  - `unfound.tsv`
  - `recess-candidates.tsv`
  - `match.py`, `decide.py`, `apply.py`, `sec.py`

## I worked through the non-date Checks in other-B.tsv. About 50 are settled or narrowed; the

- **Not found in the CR, the Federal Register issues sampled, APP, or Wikipedia:**
    - aec: acting chairman, Jan.–Feb. 1973.
    - hew: who acted at Social Security, Jan. 1959 (ssa.gov returns 403); whether Saunders was acting in 1970–71.
    - justice: whether Stern acted as Solicitor General; the Associate Attorney General order; the Office of Legal Counsel order (justice.gov was unreachable).
    - labor: whether Mashburn acted the whole time.
    - nlrb: who acted as General Counsel, Dec. 1954–Mar. 1955.
    - sec: acting chairman in 1971; who presided in Feb. 1973.
    - transportation: who acted as Federal Highway Administrator, Jan.–Mar. 1969.
    - usps: first Board chairman.
    - agriculture: Inspector General order; Edminster's and S. R. Smith's given names.
    - hud: how the Deputy Administrator was appointed; Mason as acting Federal Housing Commissioner (only Wikipedia's citation to a 1966 CQ book).
    - treasury: the portfolios of Upton, Reed and Wallace.
    - interior: Alaska Power Administration order (narrowed to June 1967).
  - **Narrowed to a remaining day or authority:** the ICC 1953–55 rotation days; the NMB rotation days; the days of the recess commissions (Walsh, Mitchell, Wood, Bicks); McKevitt's confirmation; the authority for the 1969 High Commissioner nomination; whether anyone acted as FEA Deputy Administrator.

  Scratch work, including the Senate-day grep tool and downloaded reports, is in /tmp/claude-0/-home-user-bib/f04c9307-7a44-53db-a3d0-26f3e1375c84/scratchpad/agents/checksB/.

## Plum Book comparison applied to executive/

## Offices left out of part 6
  - **Agencies with no unit file** (owner's call): Administrative Conference, Farm Credit Administration, the two Endowments, the D.C. Commissioner, the Canal Zone, the World Bank/IMF/IDB executive directors, OPIC, the OSH Review Commission, NCUA, Cabinet Committee on Spanish-Speaking People, Inter-American Foundation.
  - **Career GS-18/NEA bureau heads and deputy under secretaries:**
    - Agriculture: International Agricultural Development Service, Rural Community Development Service.
    - Army deputy under secretaries Siena and Koren; Navy deputy under secretary Grimes.
    - Labor: Battle.
    - Interior: Saline Water, Oil Import, Water Resources Research, science adviser Schaefer.
    - State: Security and Consular Affairs deputy, Cieplinski.
    - HUD: Ross.
  - **Deputies and associates of bureau heads:** ESSA and NOAA deputies and associates, FHWA deputy Jamieson, IRS deputy commissioner Harless, AID auditor general and special assignments.
  - **Not clearly at the roster's level:** Defense assistants Glass and Baroody, deputy DDR&Es, Court of Military Appeals, the Commerce regional-commission cochairmen.
  - **Unsettled:** CLC Pay Board and Price Commission members and executive directors (OCR garbled); GSA service commissioners (headings uncertain) and Griffin; Justice Board of Parole members; Postal Rate commissioners (no Senate record); HEW special assistant Egeberg.
  - **Book names no holder:** HEW National Institute of Education and Justice drug-enforcement office (both vacant).

## I've added the 1963 figures from the January 1964 *Economic Report* to MANUAL, ERP, MONTHS

**Left out or doubtful**
  - **Dec. 1963 WPI is marked preliminary.** I added no NOTE, to match the 1963 Report's Dec. 1962, which has none.
  - **Two other statements of the gap:**
    - The President's message, p. 7: "could readily add about $30 billion more to our $600 billion GNP".
    - The CEA's ch. 1, p. 46: "output still about $30 billion short of potential" in Q4 1963.
    - I used the p. 37 wording; the other two are there if you prefer one of them.
  - **1962Q1 gap not added.** Page 37 also says the gap fell "to $30 billion by the first quarter of 1962", restating Q1 1961 as $50 billion in 1963 prices. MANUAL has no 1962Q1 gap row, and this is not a first report.
  - **No FY1964 estimate from the 1963 Report.** The `est` entries for FY1964 hold only the 1964 Report's estimates. The Jan. 1963 Report's own FY1964 estimates (its Tables C-56 and C-58) were never added, so the FY1964 line shows one estimate where FY1963 shows two.
  - **FY1965 lies outside the calendar.** Its estimates file under June 1965, after Jan. 7, 1964, so they will likely not show.

  The downloads and page crops are in my scratchpad under `erp64/`.

## I've written 47 calendar entries for my months. `./bib check` ends with 14 errors, all exp

**Things I was less sure of, or left out**
  - **Dates and swings**
    - **Stevenson in Dallas:** dated Oct. 24 (UN Day) as the brief says, though Wikipedia gives Oct. 25.
    - **Texas 10th:** Dec. 21 matches `congress/specials.yaml`, and it was the runoff. Pickle was sworn Dec. 24, per the House Record.
    - **North Dakota 1st:** no swing given, because Hove's party label "Dem" keeps the build from computing one; the State canvass figures are used.
    - **Pennsylvania 23rd and Texas 10th:** swings are computed with `tools/bib/specials.py`.
  - **Figures**
    - **Foreign aid appropriation:** "about $3 billion" against $4.5 billion asked comes from adding up the statute's items and from Johnson's statement of Dec. 14. I left the authorization total out.
    - **The 1965 budget:** the $97.9 billion figure, sent Jan. 21, 1964, is from memory and outside the span. Within the span the only sources are the news conferences of Dec. 7 and Dec. 27; there is no public "under $100 billion" statement before Jan. 8.
  - **Name tags:** Villeda Morales is tagged `villeda-morales-jose-ramon`, the key with the 1958–60 documents.
  - **Primary records:** the audit lists seven of my entries with no linked primary record, because I couldn't find one online:
    - the North Dakota and Pennsylvania specials
    - Stevenson in Dallas
    - Rockefeller's announcement
    - the Reynolds testimony
    - Oswald's killing
    - the Warren Commission's first meeting

    The audit's other flags on my entries ("Day", "Albert") are false positives.
  - **Left out:** the Senate Finance hearings on the tax bill (Oct. 15), because I couldn't verify the date, and the railroad arbitration award of Nov. 26.

## Report (dallas): threads assassination, succession, elections-1964, right-and-the-military

### Left out
  - I did not use Mailer's *Oswald's Tale*, Summers's *Conspiracy*, Specter's *Passion for Truth*, Updegrove's *Indomitable Will*, Clint Hill, or Greenberg & Parker. They are not needed beyond the works chosen.
  - No work was dropped for failing verification.

## **vietnam: the patch is ready.** It is `/home/user/bib/inbox/2026-10-09-bib63-vietnam.yaml

**Left out because I couldn't confirm a detail:**
  - Galbraith, "Exit Strategy," *Boston Review* (2003): sources disagree on the issue date.
  - Đoàn Thêm's chronicles: catalog years conflict.
  - Warner's 1974–75 articles on the fall of Diem: not confirmed.
  - Peter Dale Scott's essay in the Gravel edition: pages not confirmed.

## civilrights: the patch for the 1963 civil rights events is ready

### Left out
  - *Integration with Dignity* (Skip Eisiminger ed., 2003), on Gantt: the full subtitle could not be confirmed.
  - Ackerman & Nou's 2009 poll-tax article: not found on Crossref.
  - The House Judiciary subcommittee and Senate Judiciary hearings of 1963: the govinfo search API was rate-limited, so I could not confirm titles or links.
  - *Matthew J. Perry* (Burke & Gergel eds.): the year was unclear.
  - No chapter numbers for Branch, Garrow, or Eskew: I could not get their tables of contents.

## I added six new Johnson approval readings, rewrote `indicators/approval.yaml`, and drafted

- **Left out:**
    - The Jan. 22 trial heats, which `cal.1964-01-07.opinion-5` already covers.
    - The approval releases, which belong to the indicator table.
    - Items of lesser weight: drinking, lotteries, vacations, most admired man, repeat trial heats and the like.
  - **Gaps:** there are no Warren Report or Medicare-specific releases in 1964. Medicare appears only as a ranked item, on Jan. 17 and Nov. 18.
  - **Validation:** I merged the patch for real in a throwaway copy of the repo. `check` gave 0 errors there, and `audit-cal` flags only "Gallup", which it flags on every existing Opinion entry. Like the 1963 entries, these have no primary record.
  - **Nothing is marked Check.** Every figure was compared against the page images.

## I drafted March and April 1964 in `lists/cal/mar64.yaml` and `lists/cal/apr64.yaml`. `./bi

**Ids outside my months that I link to (not written yet):**
  - `cal.1964-01-08.program`, from the poverty message and from the Apr. 20 testing entry.
  - `cal.1964-01-09.latin-america`, from Fulbright and from Panama.
  - `cal.1964-02-10.civil-rights-bill`, from the Mar. 9 entry.
  - `cal.1964-06-10.civil-rights-bill`, from Mar. 30, written as "Cloture: …".

  **Patch** (`inbox/2026-10-10-cal64-marapr-names.yaml`, dry run clean):
  - New III.K person: `kjc.who.baker-irene-bailey` (Irene Baker, TN-2). The tag `name:baker-irene-bailey` fails `check` until the patch is merged.
  - Works added, each checked against catalog records:
    - Parker, *Brazil and the Quiet Intervention, 1964* (1979), in K–J Adm. II.D.
    - Leacock, *Requiem for Revolution* (1990), in K–J Adm. II.D.
    - Eller, *Uneven Ground* (2008), in K–J Adm. II.B.
    - Caudill, *Night Comes to the Cumberlands* (1963), in K–J Cong. II.F.
  - The calendar already cites these four by short title. `check` did not flag them before the merge.

  **Threads:** I needed no new thread. The Cyprus entry is in europe-and-the-alliance, Hoffa in crime-and-hijacking, and the draft study in defense.

**Unsure or left out:**
  - In the Mar. 26 Morse vote, Voteview counts 49–34 and the Record 50–34. The text gives 50–34 and the note says so.
  - I couldn't find Green's swearing-in in the Record, so the PA-5 entry has no Record link.
  - On Apr. 9 I wrote that the brotherhoods' strike was "called" against the Illinois Central, because I couldn't confirm it had actually started.
  - I didn't name the losers in either special, the Kentucky porch host at Inez, or the railroad mediators (Kheel and Taylor), so as not to add more III.K people.
  - I found nothing on Bobby Baker or Medicare that falls in these two months.
  - `notes/calendar-audit.md` flags "Sullivan," "Reynolds" (Wisconsin's governor) and "Jackson" (the city) on my entries. These match a namesake or a place name, not a person.

## I drafted 34 calendar entries: 17 in `lists/cal/jan64.yaml` (Jan. 8–31) and 17 in `lists/c

**What I left out because I couldn't verify it:**
  - The Finance Committee's vote on the tax bill. The entry gives only Long's report of Jan. 28.
  - The date Baker took the Fifth.
  - Military aid cut off to allies trading with Cuba (Feb. 18).
  - The farm bill's Feb. 27 motion, which I left to the March drafter.

## I've written the May and June 1965 calendar entries: 20 in May (`lists/cal/may65.yaml`) an

- **Considered and left out:** Ben Bella's overthrow (no fitting thread), the Rhodesian election, the White House Festival of the Arts, *United States v. Brown* and *Estes*, and Senate Finance's Medicare report of June 30 (I confirmed the report but not its contents).
  - **Primary record:** the Liuzzo trial, the teach-in, Vietnam Day and the Wagner entry still have no linked primary record.

## Goldwater thread: report

**Looked for and not found or not verified**
  - **FBI name checks:** they are in Church Committee **Book II**, not Book III. Book III has nothing on Goldwater.
  - **"Five O'Clock Club":** no reliable source for the name. Feldman's research on Goldwater is attested only in general terms, so I made no entry.
  - **Advisers' meeting before Jan. 3, 1964:** no date, place or names found.
  - **No entries made for:**
    - his reaction to the Jenkins arrest on Oct. 14, beyond what the Oct. 19 entry holds;
    - the withdrawal of the daisy ad, beyond "shown once" in the existing entry;
    - *Why Not Victory?*, for want of a publication date;
    - the 1962 elections as chairman of the Republican Senate campaign committee;
    - a Kennedy–Goldwater meeting in Apr. 1961.
  - **Recording content:** what was said on Aug. 4, 1964 and Aug. 30, 1965 comes from the LBJ Library's catalog descriptions, as quoted in search results. discoverlbj.org blocks direct fetching (Cloudflare).

  **Tool note:** `./bib audit-cal` does not count PRDE recordings, archive.org, newspapers or KU Libraries as a primary record. So some new entries will show under "no primary record" even though the brief prescribes the PRDE form.

## The patch is written and the dry run is clean: `/home/user/bib/inbox/2026-10-10-thread-hal

- **Robert Kennedy `c2`:** this is the Attorney General's later stations plus the Johnson ones. I left out his 1963 Vietnam meetings and his 1965 Senate speeches rather than pad.
  - **Elections of 1964 `c2`:** this is the full original station list, since nearly all of it falls from 1963 on. `c` is short: the draft's Chicago meetings and Gallup's trial heats.
  - **Medicare `c2`:** it keeps "the conference deadlocked", but no entry of its own holds that. It probably sits inside the Sept. 2, 1964 entry.

  The drafting script is in the scratchpad (`halves.py`) if the patch needs regenerating against new revs.

## The patch is written: `/home/user/bib/inbox/2026-10-10-south-four.yaml` (patch `south-1964

**Looked for and not found or not verified**
  - Georgia's 1964 congressional redistricting after *Wesberry*.
  - Mississippi's June 2 House and Senate primaries; I could not get CQ or State figures.
  - The Mississippi regulars' July 28 State convention and electors.
  - Hattiesburg Freedom Day (Jan. 22).
  - Maddox closing the Pickrick (the Sept. 4 permanent injunction exists, at 234 F. Supp. 179).
  - The Deacons for Defense (Jonesboro, late 1964; no federal role that year).
  - *United States v. Fox* (Plaquemines registrar, 5th Cir. July 21): found, left out as minor.
  - Louisiana's 1964 elector moves, and Perez in 1964.

## I wrote 37 entries for January 6 to February 29, 1960: 16 in `lists/cal/jan60.yaml` and 21

**Persons in `c` with no name entry:** Thomas C. Hennings Jr. (Jan. 19). Henry M. Wriston (Feb. 7). Also the Greensboro four, not named in `c` (Ezell Blair Jr., Franklin McCain, Joseph McNeil, David Richmond), and James Lawson, left out of the Nashville entry.

  **Persons with a name entry but no Part III entry:** tagged and left out of `Names:`. They are Herter, Kishi, Fujiyama, MacArthur II, Bonsal, Dorticós, Gates, Power, Glennan, Mitchell, Holland, Gray, Blatnik, Kubitschek, Alessandri, Benson and Monroney. Brunsdale has no name entry, so I left him out.

**Placement:** every event fit an existing thread. The campaign-finance bill went in `congress`, also `elections-1960`. I left out Kennedy's Jan. 2 announcement as a separate entry because it falls before Jan. 6; the Jan. 14 entry cites it.

## I wrote 34 entries: 17 in January 1966 (`lists/cal/jan66.yaml`, after the existing Jan. 1–

**Persons in `c` with no name entry** (for Part III): Vernon Dahmer; Fred W. Friendly; Lurleen Wallace; Elliot M. See Jr.; Charles A. Bassett II; Eugene Cernan; John P. East; Orin Lehman; Jeffrey St. John; Augustus O. Bacon (the testator in *Evans*). I tagged, but left out of `Names:`, the people who have only roster or FRUS name entries, such as Wood, Vaughn and Brimmer.

- **Not written:**
    - the four-year House term amendment (Jan. 20);
    - the rural America message (Jan. 25);
    - the international education message (Feb. 2);
    - the Nigerian coup (Jan. 15);
    - Albert Thomas's death (Feb. 15), left for the TX-8 special;
    - Johnson's Freedom House speech (Feb. 23);
    - Bundy's departure (Feb. 28).

## I wrote September and October 1966: 19 entries in `lists/cal/sep66.yaml` and 14 in `lists/

**Could not place or left out:**
  - The campaign fund has no fitting thread; I put it in `program`, with `congress` as a second thread.
  - Left out for want of a verified source or a bibliography: the "Crisis and Commitment" statement of Wilkins, Randolph and others (Oct. 1966); the Hunters Point riot (Sept. 27); the GE strike and the Taft-Hartley injunction (Oct. 2–18); China's missile-delivered nuclear test (Oct. 27).
  - Left out as minor: Marcos's state visit (Sept. 14–15), which is mentioned in the Manila entry, and the Urban Mass Transportation amendments (Sept. 8).
  - I wrote no opinion entries, as instructed.

## I wrote 47 entries across November 1966, December 1966 and Jan. 1–3, 1967. `./bib check` e

**Not placed:**
  - Israel's raid on Samu, Jordan (Nov. 13): no thread fits.
  - The Amistad Dam meeting with Díaz Ordaz (Dec. 3): no bibliography to hand.
  - Moyers's resignation: I could not verify the date.

  I also left out a Fed policy change in late December I couldn't verify, and the Johnson–Mills call of Nov. 12 (its content is behind PRDE's subscription).

## **alms: Alabama and Mississippi, done.** The patch is at `/tmp/claude-0/-home-user-bib/f04

**Could not place or verify**
  - Mayoral elections not found: Jackson (Allen Thompson, 1961 and 1965), Montgomery (Earl James), Mobile (the commission; Langan), Huntsville (Hearn, 1964), Tuscaloosa, Meridian (Key over Burns, 1965), Hattiesburg.
  - Returns not found: Birmingham's referendum and the Mar. 5, 1963 first round.
  - Mississippi vote counts not found: right-to-work, §241-A and the 1963 reapportionment amendment.
  - Dates not confirmed: the Aug. 17, 1965 vote, from *Time* and an MFDP leaflet; the date of Act No. 252.
  - Not found at all: Mississippi's "1960 amendment authorizing the closing of schools" and a 1962 Mississippi voter-qualification amendment; the only 1962 measures I found are statutes. Also Alabama's textbook and teacher laws and its other laws aimed at the movement.
  - Not written: Mississippi's 1966 special session on reapportionment, and the date of the 1966 congressional redistricting act.

## New York patch (ny): done

### Not placed or not verified
  - Not placed:
    - the 1961 State fair-housing extension (Metcalf-Baker);
    - the 1961 law creating CUNY and the tuition fight;
    - the 1966 Condon-Wadlin amnesty for the transit strikers;
    - the 1963 Downstate Medical Center protests;
    - the West Village urban renewal fight;
    - Rochester's council elections and its mayors (Gillette, Lamb);
    - Yonkers's elections;
    - the 1963 off-track-betting amendment.
  - Facts marked Check in the entries:
    - the exact days of the death-penalty, divorce, Medicaid and sales-tax laws;
    - the city income tax terms;
    - the Lower Manhattan Expressway vote's day (Dec. 6 or 11);
    - the 1965 primary date;
    - the Surrogate primary's date and vote;
    - the review-board vote ("nearly two to one");
    - the 1964–66 legislative seat counts;
    - the *Orans* cites, 15 N.Y.2d 339 and 17 N.Y.2d 107;
    - the 1961 charter vote;
    - Buffalo 1961: whether Sedita lost the primary or the general;
    - the March 1964 and September 1964 boycott counts.

## gascflla: I wrote 51 calendar entries and 25 Part III entries for Georgia, South Carolina,

**Not placed or not verified**
  - Florida:
    - The Constitution Revision Commission of 1965–67: created in 1965, Chesterfield Smith chairman, but I found no dates.
    - Miami and Dade Metro: no reliable dates or figures for the charter and home-rule fights, Chuck Hall's 1963–64 election as the first Metro mayor, or High's Miami re-elections of 1959, 1961, 1963 and 1965.
    - Burns's 1965 road bond referendum (defeated): no date.
    - The amendment shortening the governor's term: the date it was ratified is unverified; the entries say only that the 1964 term was two years.
    - Jacksonville's 1964 loss of accreditation: no date (mentioned inside the Oct. 1, 1965 entry).
    - Tampa, St. Petersburg, Orlando: nothing found.
  - Georgia:
    - Atlanta's 1965 mayoral race (Allen over Muldawer): no source for the date or figures.
    - The 1964 congressional redistricting after *Wesberry*.
    - The constitutional amendments, which number in the dozens, mostly local.
    - Savannah 1963, Augusta, Macon.
  - South Carolina: the Charleston movement of 1963; Columbia and Greenville; the constitutional amendments.
  - Louisiana:
    - The exact number and date of the 1960 suitable-home act.
    - The four later extraordinary sessions of 1960–61.
    - The New Orleans general election of 1962 (Schiro over Buckley).
    - Bogalusa 1965: not in the calendar, and I did not write it.
    - Baton Rouge, Shreveport, and a full list of amendments.
  - Entries carrying "Check":
    - Collins's speech: the date and wording.
    - The Flemming Rule: the date and the 23,000 figure.
    - The second Louisiana amendment: that it was on the Nov. 8, 1966 ballot.
    - The New Orleans runoff date (Mar. 3, 1962).
    - The extent of the June 15, 1965 Georgia House elections and the count of eleven Negro members.

## midwest1 report: Ohio, Michigan, Indiana, Illinois and their cities

### Not placed or not verified
  - **Illinois FEPC Act of 1961:** I found no signing date, so it gets no entry of its own; it is named in the Motorola entry.
  - **The Motorola examiner's 1964 ruling:** I could not find its date or that it was cited in the Senate's Title VII debate; marked Check.
  - **Chicago's West Side riot of Aug. 1965:** not verified, not written.
  - **Robert Taylor Homes** (no date beyond "1962") and **the University of Illinois site at Harrison–Halsted** (no exact date): not written.
  - **Figures I could not find**, so the entries carry none or mark them Check: Chicago's Feb. 1964 boycott, Akron's charter vote, Cleveland's 1962 primary and general, Gary 1963, the Michigan legislature's 1964 seat counts, the Indiana right-to-work repeal's day.
  - **Cleveland 1965:** Wikipedia's figures give Locher a 142-vote margin; checked against nothing official.
  - **Not covered:** Cincinnati, Columbus, Toledo, Flint, Grand Rapids, Ogilvie (Cook County 1966), Illinois's 1966 revenue article, Indiana's 1960 convention and reapportionment, the States' Medicaid laws.

## txok (Texas and Oklahoma): report

**Not placed or not verified:**
  - **Houston mayoral races:** the 1961 Cutrer–Welch runoff (no date found). For 1963, the dates and figures of both rounds are unknown, and the runoff opponent is spelled both "Hervey" and "Harvey" in the *Texas Observer*, so I left him unnamed.
  - **Other cities:** I found no dated, sourced election entries for San Antonio (the Good Government League, McAllister), Fort Worth, Austin, Tulsa (Hewgley 1966) or Oklahoma City (Wilkes 1963; Shirk appointed 1964).
  - **Houston:** annexations and the school board fights are left out for want of dated sources.
  - **Texas Democratic Coalition** (1963): no founding date found.
  - **Connally's stand on public accommodations, 1963:** not verified.
  - **Texas Medicaid:** joining the program fell in 1967, outside the span; the 1964 and 1965 enabling amendments are in.
  - **Marked Check:**
    - Crystal City: the Apr. 2 date, since the *Observer*'s "Tuesday of last week" is ambiguous.
    - Dallas schools: the count of 18.
    - The sales tax act's chapter number.
    - The registration law of the February 1966 special session.
    - The date of Johnson's Senate removal.
    - Lockridge's district.
    - The Texas primary figures (from Wikipedia and the *Texas Almanac*, not the canvass).

## west: report

### Events I could not place or verify, so left out
  - Las Vegas: the Black Book (the gaming commission's list of excluded persons, 1960); Sinatra's Cal-Neva license (1963); the FBI microphones in the casinos (1966); Gragson's 1963 re-election; the Clark County commission.
  - Nevada's civil rights act of 1965.
  - Idaho's 1965 sales tax and its 1966 referendum.
  - Arizona's 1961 loyalty oath act; *Klahr v. Goddard* (only mentioned, with a Check).
  - Washington's 1965 redistricting act (date unknown); Washington's Referendum Bill 16 of 1966 (congressional districts).
  - The Colorado legislature after *Lucas*; the reapportionments in Montana, Utah, Idaho, Wyoming and New Mexico, 1964–66.
  - The Alaska primaries of 1962 and 1966: no figures.
  - The Hawaii 1966 primary: only nominal contests.
  - The exact days of the Wyoming primaries (1962, 1966), the New Mexico primary of 1962 and Herndon's crash: entered month-only, with "Check the day".
  - Cities: Portland (Schrunk), Denver (Currigan, urban renewal), Phoenix's Charter Government, Tucson, Salt Lake City (Bracken Lee), Albuquerque, Honolulu (Blaisdell), Spokane and Reno all lacked verifiable data from here.
  - Unverified details marked Check in the entries: the grounds and votes in *O'Meara* and *Case* (CourtListener is bot-checked); the Tacoma vote figures; whether 1966 was the first time Republicans held both Arizona houses.

## I wrote the national patch at /tmp/claude-0/-home-user-bib/f04c9307-7a44-53db-a3d0-26f3e13

**Could not place or verify**
  - **The "Murphy amendment fight of 1965":** I found no such 1965 vote. The 1965 fight over the governors' veto is already in the calendar (Prouty, Dominick, Ayres). Murphy's governors' veto amendment, over legal services, came in 1969, outside the span.
  - **Southern Governors' Conference on civil rights, Democratic governors' other meetings with Johnson, and the National League of Cities' policy acts:** I wrote no entries for these.
  - **Exact dates still uncertain:**
    - The Council of State Governments' assembly of December 1962 (entered by month).
    - Denver, Dec. 4–5, 1964 (from a newspaper index and the *Michigan Daily*).
    - Colorado Springs, Dec. 9–10, 1966 (from "the second weekend in December").
  - **Left as "Check" in the entries:**
    - The one "no" at Los Angeles, July 7, 1966, as Hatfield; the proceedings give no roll.
    - Mississippi's rejection, which rests on the House Manual alone.
    - Johnson's shelving of the plan in December 1964, from the *Ripon Forum*.
    - The Article V counts, from the Article V Library's compilation; each Congressional Record cite needs reading.
  - **Legislature summaries:** these rest on Klarner's dataset (session totals compiled from the Book of the States), not the Book itself. The seat gains are "some" approximations; Minnesota is coded by caucus and Nebraska left out.

## **Report, uppersouth (Va., N.C., Tenn., Ky., Ark.)

**Could not place or verify (no entry written)**
  - Richmond:
    - the annexation fight: 1961 merger referendum (Henrico 61 percent against) and the 1965 Henrico award of 16–17 sq. mi. at $55 million, which the city declined (422 U.S. 362–63). No dates.
    - the at-large council elections.
  - Memphis: the 1963 race (Ingram) and the commission. No source. The 1967 race falls after the span.
  - First Metro election and Briley: sources give 1962 and 1963.
  - Arkansas Tucker-farm report of 1966: no date reachable.
  - Tennessee 1965 limited constitutional convention.
  - Tennessee death penalty (Clement's commutations).
  - Research Triangle: IBM and NIEHS in 1965, month unknown.
  - Durham 1963.
  - Virginia's 1963 special session (certificate of residence) and its 1964 special session dates.
  - Kentucky's 1960 sales tax: no date found.
  - Little Rock schools and city government, Norfolk, Lexington, Raleigh, Winston-Salem, Chattanooga, Knoxville: nothing verifiable written.

## midwest2 report (Wisconsin, Minnesota, Iowa, Missouri, Kansas, Nebraska, the Dakotas)

**Not placed or not verified:**
  - **St. Paul mayoral races (1960, 1962, 1964, 1966):** no source with dates or votes; not written.
  - **Des Moines, Wichita, Kansas City (Kans.) mayors:** not written.
  - **Pruitt–Igoe:** nothing dated inside the span; not written.
  - **Medicaid adoption in these States:** no start dates I could verify (the SSA Bulletin was unreachable); not written.
  - **Wisconsin's 1961–62 sales tax fight; Iowa's liquor-by-the-drink law of 1963; Milwaukee annexations; St. Louis's 1961 public accommodations ordinance; Kansas's 1966 school unification:** not written.
  - **Governors' general elections not written:** Wisconsin 1960, 1962 and 1966; Iowa 1960, 1964 and 1966; Missouri 1960 and 1964; Kansas 1962 and 1964; Nebraska 1960, 1964 and 1966; North Dakota 1960, 1962 and 1964; South Dakota 1962, 1964 and 1966. None had an incumbent beaten or another reason under the brief, except perhaps Nebraska 1966 (the tax fight, which I put in the measures entry instead).
  - **Marked "Check" in the entries:**
    - Kansas City referendum: the day (sources say Apr. 8 or Apr. 18; I used Apr. 7, the election day) and the vote (about 1,700 votes).
    - Iowa death penalty: the House vote and the signing date (entry dated Feb. 1965 by month).
    - Missouri Public Accommodations Act: the day of signing (the archives give June 30 as passage).
    - Missouri Fair Employment Practices Act: the date (the archives' chronology gives Aug. 1).
    - Minnesota's 1966 apportionment law: approved May 24 per MNopedia, May 20 per the Legislative Reference Library.
    - Milwaukee 1964 mayoral race: opponent and vote.
    - Minneapolis 1963 and 1965 races: votes (1965 also its day).
    - St. Louis 1961: the opponent and the vote.
    - Kansas City 1963 and Omaha 1961 and 1965: the day.
    - Amos suit: the filing day. Second Milwaukee boycott: the days.
    - Groppi's Eagles pickets: the month they began.
    - Jefferson Bank: the court order and the sentences.

