# Rules for every agent working in /home/user/bib (read first)

- Read /home/user/bib/CLAUDE.md first and follow it exactly: the brief's prose (compact, plain, no color), the calendar
  entry rules (c; n with the primary record linked first, then the event's bibliography as [[w.…]] cards or `See
  [[id]]`, Names:, name: tags), the spans rule (an entry is an event-day; never bundle), subthreads and ghosts (no
  thread name begins with "The"), State tags (state:, city:), place: tags for Indochina, leads, YAML quoting, the
  indicators' STYLE notes in tools/bib/indicators.py, the works catalogue (new cards via
  `flock /tmp/claude-0/-home-user-bib/f04c9307-7a44-53db-a3d0-26f3e1375c84/scratchpad/works.lock python3 /tmp/claude-0/-home-user-bib/f04c9307-7a44-53db-a3d0-26f3e1375c84/scratchpad/add_cards.py FILE.yaml`
  from /home/user/bib; read that script's head first).
- Never read build/ or whole list files; use `./bib find`, `./bib show`, grep -n, and read only the lines you need.
- Never run git. Several agents work in the same repo at once: other agents are editing calendar files, th.yaml,
  tools/bib/build.py (the inject chain), tools/bib/check.py, tools/bib/indicators.py and
  tools/indicators/make_indicators.py. Re-read the exact lines right before each edit; make small exact-string
  edits (Edit, or a script that re-reads the file immediately before writing and changes only its own lines); never
  rewrite a shared file from a stale read; put new code in new files (a new module or script) wherever you can and
  touch shared files only to hook it in.
- Network goes through a proxy (/root/.ccr/README.md if a tool fails). Never disable TLS; don't get around bot
  checks (record a refused host as a lead). Downloads in your own scratch directory under
  /tmp/claude-0/-home-user-bib/f04c9307-7a44-53db-a3d0-26f3e1375c84/scratchpad/, run python with -I on downloaded
  data; don't keep copyrighted PDFs in the repo. Never write an API key anywhere.
- Every figure from a source read, with its page or table; nothing from memory into the data or the calendar
  ("Check" marks a detail to verify; anything not placed goes to the leads).
- Document what you build where CLAUDE.md documents its kind (a section or a bullet; the module's STYLE notes) and
  add `check` rules for new data in the module (a `problems(series)` function hooked into tools/bib/check.py).
- Finish with `./bib check` (0 errors from your work; report others' errors without fixing them) and, for calendar
  entries, `./bib audit-cal`. You may build one page to test (`./bib build cal --force` takes ~4 min; use
  run_in_background and wait) but report rather than chase others' errors.
- Report (under 500 words): what you built (files, entries with ids, counts), what you checked and how, what is
  left, and leads for notes/leads.md (under its heading: States and cities, National, Foreign).
- The calendar's month files and section ids are now YYYYMM (`lists/cal/196104.yaml`, section `196104`; Jan. 1966 is
  `196601` and `196601b`); the old ids (`apr`, `apr60`) stay as `old_id` in list.yaml. Use the new names.
- The owner (the user) is "the owner" in CLAUDE.md. Standing rules the owner gives go into CLAUDE.md, dated
  ("the owner's rule, Oct. 21, 2026"), where that kind of thing is documented.
- The Public Papers now come from GPO's volumes (CLAUDE.md, "The Public Papers"): a primary record for a President's
  document is its cite, "Title, [1961 Pub. Papers 1](govinfo…#page=N) (date)", from sources/ppp-matches.json (the item,
  its pages, its link); APP only where the Papers do not print it. Never fetch from presidency.ucsb.edu.
- Calendar files: no agent edits lists/cal/*.yaml directly. Every agent writes its calendar changes as one patch,
  inbox/2026-10-24-<your-name>.yaml (CLAUDE.md, "By patch"; `base` revs from `./bib show` read right before you write
  the op; check with `./bib merge inbox/<file> --dry-run`); Claude merges it. th.yaml likewise, by patch.
- Since Oct. 24, 2026 the works not yet read stand behind "To check: ..." in each note (CLAUDE.md, "Hard and soft");
  each source stands for the whole entry unless the note says which claim it is for ("What each source stands for").
- Other agents work at the same time on: fifteen of the owner's books (inbox/2026-10-24-book-*.yaml), the State
  term limits and the State sources listings (notes/, elections/), the Attorney General's and OLC's opinions, and the
  form of election results in the calendar's text; Claude works on the election blocks' build code (congress.py,
  elections.py, governors.py, legislatures.py, contents.py, templates/). Keep to your files; touch shared ones
  (build.py, check.py, CLAUDE.md, README.md, notes/leads.md) by small exact edits only, re-reading first.
