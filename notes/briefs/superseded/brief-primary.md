# Stage 4: primary records for the entries that rest on books alone (brief for each agent; read brief-common.md first)

Why: the owner asked (Oct. 2, 2026) for the primary record, linked, first under every entry where one exists: the
statute, the Federal Register, the Congressional Record, the Public Papers, the presidential library's file, the FRUS
document, the case (CLAUDE.md, "So every calendar entry has", `n`). `./bib audit-cal` lists in notes/calendar-audit.md
the dated entries with none ("Primary record: None linked or named") and those that name one without a link ("Named,
not linked"). Your years are named in your prompt. Many events have no record of their own (a march, a strike, a
riot, a speech outside the Public Papers): those you leave, and say so in your notes file. The rest want theirs.

Where the records are (all in the repo or open from here; never from memory):
- The President: the daybook's President rows (daybook/<YYYY-MM>.yaml) and the Public Papers' items
  (sources/ppp-matches.json; tools/bib/ppp.py makes the cite and link: "Title, [1965 Pub. Papers 917](…) (Aug. 25,
  1965)"); APP's own page only where the Papers do not print it (orders, proclamations), linked, never fetched
  (presidency.ucsb.edu refuses automated readers: link it by its URL, read it nowhere).
- FRUS: the daybook's FRUS rows, the text in sources/frus-text/<YYYY-MM>.json.xz (read it there), history.state.gov.
- Statutes, the Federal Register, the bound Congressional Record, hearings: govinfo (STATUTE-, FR-, GPO-CRECB-, CHRG-);
  sources/statute-links.json for the Statutes' files; congress/bills.yaml and tools/congress/make_record_pages.py for
  the Record's days; the Daily Digest rows (daybook/committees/) for a hearing's day and page.
- Cases: the U.S. Reports (the Library of Congress's scans, loc.gov, or govinfo's USREPORTS), case.law's open PDFs for
  the lower courts (as the series links them already: grep lists/ for case.law and loc.gov).
- The Attorney General's and OLC's opinions: daybook/opinions.yaml. The *Bulletin*: daybook/bulletin/ and
  sources/dsb-pages.json (archive.org, by page). Recordings: daybook/recordings/ and the Miller Center's free pages
  (never PRDE's transcripts). Johnson's Daily Diary: daybook/diary.yaml (50 days only). The States' records:
  sources/states.yaml and sources/state-law.yaml.
- The records the secondary works cite, already logged: sources/cited-records/*.yaml. Every one with `found` set and
  `read: false` (30 now) is yours where its entry falls in your years: read it, cite it first, and set `read: true`
  (edit the YAML directly; check [cited-records] holds it).
- Not readable here: the newspapers (TimesMachine is a link by date, not a text), discoverlbj.org, history.defense.gov,
  jcs.mil, HathiTrust's pages (bot-checked: never get around a bot check), the presidential libraries' sites that
  refuse this environment. A record found but not readable joins "To check:" with where it is.

Do, for each entry of your years in the two lists:
1. Find the record. Read it, the part that bears on the entry. A record that does not bear the entry out is no cite
   for it (CLAUDE.md, "What each source stands for").
2. Cite it first in `n`, linked, in the forms CLAUDE.md gives (the Public Papers, FRUS with the volume's title, "[77
   Stat. 56](…)", "[111 Cong. Rec., Senate, Aug. 11, 1965](…)", the U.S. Reports), with a parenthetical where it bears
   out only part of `c`. Where it disagrees with `c` (a date, a figure, a name), the record stands: correct `c` only
   where the record settles it beyond doubt and say so ("The Papers date it Aug. 26."), else a Check. Never rewrite
   `c` beyond what the record needs.
3. The claim map: where the entry has a stored `src`, add the record's row (its link: '<url>: A, C'); where it has none,
   leave it (the mechanical map counts a link as covering all units, which is right only if the record bears out the
   whole entry: if it bears out part, write the `src` with the record's row and the other items' rows from `./bib
   claims seed ID`).
4. "Named, not linked": link what the note names, in its place, once read.
5. Rule B: none (you read records, not a book). Leads: any event the records show that the calendar lacks, and any
   record you know exists but could not reach, go in your notes file under "Leads".

Deliverables: one patch, inbox/2026-10-29-primary-<your part>.yaml (edits with `base` read just before writing;
`./bib merge --dry-run` clean; never merge it yourself); notes/primary-records/<your part>.md: for every entry of your
lists, one row: id, the record cited (or "none: <why>": a march, a strike, a statement not printed, a record not
reachable), and any Check added. Don't commit or push. Report (under 400 words): entries in your lists; records found
and cited, by kind; none and why, by kind; Checks; corrections to `c`; cited-records read; leads.
