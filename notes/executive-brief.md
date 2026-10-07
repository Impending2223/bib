# Executive Branch roster: research brief

You are filling part of a roster of the Executive Branch, Jan. 20, 1953, to Aug. 31, 1974, kept as YAML in
`executive/` and rendered by `tools/bib/executive.py` (read its docstring, lines 1–80, for the fields; it is
the schema). The roster is shown at each inauguration (1953, 1957, 1961, 1965, 1969, 1973) and at the
successions of Nov. 22, 1963, and Aug. 9, 1974, with every change during each term.

## The owner's brief

"Names, titles, dates of appointment, dates of nomination and commission where applicable, dates of
vacancies and names of acting officers and replacements. Preserve whatever hierarchy and logic we have in the
arrangement of the roster. Heads of Departments, principal officers, inferior officers, employés. Rusk and the
men under Rusk; McNamara and the men under McNamara; Robert Kennedy and the men under Robert Kennedy. ... At
the very least, anyone in the Executive Branch named in our calendar, in our bibliography, or in any of our
FRUS or PPP documents, should be placed in our Executive Branch roster. This is meant to be a formalist
account, at least at first cut. It should correspond to, and point to, the relevant provisions of law. Find,
read, and point to the relevant statutory authorities establishing offices and setting out their authorities."

Prose rules from CLAUDE.md apply to every `n`, `out` and `does`: compact, plain, clipped. Record what
happened; no praise, blame, color, or interpretation. "Resigned." "To Secretary of Defense." "Died."
"Recess appointment; nomination rejected June 19, 1959, 46–49."

## What to produce

One file per unit you are assigned: `executive/<unit>.yaml`, with `unit:` equal to the file name. Look at
`executive/president.yaml`, `executive/vp.yaml` and `executive/state.yaml` for the form. Give each unit
`under:` (its parent unit) and `order:` (its place among its siblings). Offices in display order: the head
first, then the deputy, then the rest in the order the Congressional Directory gives them; use `under:` on an
office for the one it reports to where that is not the head, and `group:` for a subheading (a bureau, a
service, "Staff offices").

For every office: `title` (the title in January 1953, or when created; `titles:` for later changes, with
dates), `rank` (head / principal / inferior / employee / military), `appt` (PAS, PA, HD, XO, DES, MIL, CAREER,
ELECTED: see APPT in the code), `level` where the Executive Schedule (1964 on) fixes one, `from`/`until`
where the office was created or abolished in the period, `law`, and `holders`.

For every holder: `name` as "Surname, Given" (as Part III of the series writes the person, if there: grep
the part3 file you were given), `from` (required: the day of taking office, the oath or entry on duty), `to`
(the last day; leave out only for one still serving on Aug. 31, 1974), and wherever you can find them:
`nominated` (the day the nomination was received in the Senate), `confirmed`, `recess` (a recess commission),
`appointed` (the commission, or the appointment where there is no commission), `out` (how it ended), `rank`
for an officer's grade and service ("Gen., USA", "Adm., USN"), `title` where the holder's title differs from
the office's, `acting: true` for acting officers. Begin each office with whoever held it on Jan. 20, 1953
(with that person's real `from`, however early), or with its first holder if it was created later. Record
acting officers wherever an office was vacant: who acted, from when to when. `src`: a short list of where the
dates came from, in the forms the build links (the docstring of tools/bib/executive_sources.py): `CDIR 1961-04`,
`Cong. Rec.`, `Cong. Rec. Index 1961`, `POCOM`, `FRUS persons list, 1961–63, V`, `FRUS 1961–63, IX, doc. 144`,
`Wikipedia: Dean Rusk`, `APP 1961-01-21`, `Federal Register, Jan. 20, 1953`, a URL, or a work named in
sources/executive-sources.yaml. Quote an item that holds a comma. `./bib executive sources` lists what does not link.

Vacancies are computed by the build from the holders' dates: don't write "Office vacant ..." in a note. An
acting officer serves in a vacancy and does not fill it; the build shows him under the vacancy. A note (`n`)
continues the holder's date line in the same style: write it as clipped facts, not commentary. POCOM's
"Commissioned during a recess of the Senate; recommissioned after confirmation on <date>" belongs in the
fields (`recess`, `confirmed` where known, `appointed` = the recommission), not in `n`.

Never invent. If you cannot find a date, leave the field out. For `from`, give the best precision you can
support ('1961-02' or '1961' is allowed) and add "Check" to the holder's `n` saying what to verify. Where two
good sources disagree, give the more official and say "Check: Wikipedia gives Feb. 3." in `n`.

## The law

For each unit, and for each office that has its own authority, `law:` entries: the act (or reorganization plan
or executive order) that establishes it and the provisions that set its powers and its manner of appointment;
amendments that changed it in the period (a new title, a new level, a transfer). Each with `act`, `date`,
`cite`, `usc` where codified, and `does` (one clipped line, in the statute's own terms where possible).

- Statutes at Large: `cite: 'ch. 343, § 101, 61 Stat. 495, 496'` (before 1957 acts have chapter numbers) or
  `cite: 'Pub. L. 87-297, § 21, 75 Stat. 631, 634'`. The FIRST page is where the act begins; the build links it
  to `https://www.govinfo.gov/content/pkg/STATUTE-<vol>/pdf/STATUTE-<vol>-Pg<page>.pdf`, which exists only for
  the page an act begins on. Verify each one: `curl -s -o /dev/null -w '%{http_code}' URL` must give 200. Read
  the act there (pdftotext is available) to write `does`.
- Reorganization plans: `act: Reorganization Plan No. 6 of 1953`, `date` its effective date, `cite` its
  Stat. page (they are printed in the Statutes), and `usc` where noted (5 U.S.C. § 133z–15 note, etc.).
- Executive orders: `act: Executive Order 10483`, `date` signed, `cite: '18 Fed. Reg. 5379'`, and `url` to
  its text on presidency.ucsb.edu where you can find it.
- U.S. Code: the edition of the period: '(1958)', '(1964)', '(1970)'. Title 5 was recodified in 1966 (Pub. L.
  89-554, 80 Stat. 378); Title 10 in 1956 (ch. 1041, 70A Stat. 1). Cite what was in force for the office.
- The Constitution: `url: https://www.archives.gov/founding-docs/constitution-transcript`.

## Sources

- The Congressional Directory, two editions a Congress, 1953–1974, as OCR text: each lists every department's
  officers by title. Use it to build the office list and to confirm who held what at each edition's date.
  OCR is rough; read around.
- FRUS persons lists for every volume 1952–76: `name<TAB>role<TAB>volume`. Roles often carry dates.
- POCOM (the Office of the Historian's data): State and the chiefs of mission. Already seeded.
- Wikipedia, through the API, for nomination and confirmation dates (often in infoboxes and lists of
  officeholders, citing the Senate Executive Journal): `curl -s -A 'bib-roster/1.0 (research bibliography)'
  'https://en.wikipedia.org/w/index.php?title=Dean_Rusk&action=raw'`. At most one request a second; a 429 means
  wait a minute. Treat it as a lead, not a final source, where an official source is at hand.
- presidency.ucsb.edu (APP): nominations, appointments, resignations, swearings-in, executive orders.
  `https://www.presidency.ucsb.edu/advanced-search?field-keywords=...&from[date]=MM-DD-YYYY&to[date]=...&items_per_page=100`.
- govinfo: Statutes at Large (as above); the Congressional Record, bound edition (CRECB), for nominations
  and confirmations; the Congressional Directory.
- archive.org: the United States Government Organization Manual (1955–56, 1958, 1966–67, 1968–69, 1970–73
  editions): each agency's creation and authority, with statutory citations. Full text at
  `https://archive.org/download/<id>/<id>_djvu.txt`; search `https://archive.org/advancedsearch.php`.
- Department histories where reachable (history.state.gov; the Army's Center of Military History;
  history.navy.mil; afhistory; justice.gov; treasury.gov; usda; dol.gov).
- Blocked here, do not try: history.defense.gov, jcs.mil, congress.gov, bioguide.congress.gov, esd.whs.mil.
  HathiTrust pages are bot-checked. Don't try to get around a bot check.

## Rules

- Write only your own files in `executive/`. Do not edit anything else in the repo, do not run git, do not
  run `./bib build`.
- Run `./bib executive check` until it reports no errors in your files (ignore errors in others' files).
- `./bib executive who SURNAME` shows where a person already is in the roster.
- Keep going until your units are complete for the whole period. Breadth first: every office and every
  holder with `from` and `to`; then the nomination, confirmation, and commission dates; then the law.
- Report at the end: the files written, the counts (offices, holders), what is still missing, and every
  "Check" you left.
