# The code review of Nov. 19, 2026: findings, recommendations, and a plan for the owner to confirm

The owner, Nov. 18, about 11:44 p.m. Pacific: "use agents to do an adversarial review pass over the codebase ... cluster and rank the recommendations ... confirm the plan with the user before executing the changes." Three reviewers read the code (no changes made): A, structure and readability; B, repetition, dead code and outside libraries; C, speed, reliability and a test plan (it profiled real runs in a scratch copy). Their full reports, with file and line references, are in the scratchpad (`review/A-architecture.md`, `B-dry-nih.md`, `C-perf-tests.md`); what follows is the synthesis. **Nothing below has been done; it waits on the owner's answers.**

## The decoder ring

| Term | Plain meaning |
|---|---|
| **code / codebase** | the programs in `tools/` (about 64,000 lines of Python) that check the data and build the website. The data (`lists/`, `works/`, `sources/`) is not code. |
| **module** | one program file, e.g. `tools/bib/places.py`. |
| **function** | a named piece of a module that does one job (e.g. "format a date"). |
| **build** | turning the data into the website's pages (`./bib build`). |
| **CI / the deploy** | the automatic run on GitHub after every merge to `main`: check, build, publish. |
| **dependency / library** | someone else's published code we install and use, rather than write ourselves. |
| **NIH** ("not invented here") | writing our own version of something a well-tested library already does. |
| **DRY** ("don't repeat yourself") | one rule, one place in the code. Its opposite: the same rule copied into 26 files, which drift apart. |
| **refactor** | changing how code is organized without changing what it produces. |
| **rewrite** | replacing a section of code with new code written fresh to do the same job. |
| **regression** | a change that silently breaks something that used to work. |
| **test** | a small program that runs part of the code and checks the result is what it should be; a whole set is a **test suite**. |
| **golden (snapshot) test** | a test that saves today's output (a page, the check's report) and fails if a change alters it unexpectedly. The safety net for a rewrite: the new code must produce byte-for-byte the same pages. |
| **fixture** | a small frozen slice of the real data the tests run on (two calendar months, the cards they cite). |
| **cache** | a saved copy of work already done, so it isn't redone (e.g. parsed YAML files). |
| **global state** | values a module keeps between uses that other modules can change behind its back: a frequent source of bugs that appear only in some orders of work. |
| **pipeline** | a fixed, written-down sequence of steps (load, check, render, write). |
| **lock** | a rule that only one process may write a file at a time. |
| **pin a version** | name the exact version of a library to install, so every machine runs the same code. |
| **libyaml / C loader** | a fast YAML reader already inside PyYAML, the one library the build uses; we use its slow pure-Python twin. |
| **tokens** | the units Claude's work is metered in; a reading run tonight cost about 0.3–0.45 million. |

## What the review found, clustered and ranked

Ranked within each cluster by risk. The clusters are in the order I recommend doing them (below).

### 1. A safety net: there is none (prerequisite)
- **No tests at all**, and the library version CI installs is not pinned. The only guard is `./bib check`, which checks the *data*, not whether the *code* still builds the same pages. Any rewrite today is unprovable.
- The output is deterministic (C ran check three ways: identical), so golden tests are practical.

### 2. Live bugs that damage data or the site (fix first, small each)
- **Duplicate "To check:" sentences.** The note reader takes "87th Cong." for a sentence's end and misses an existing "To check:", so an added work writes a second one. 5 calendar notes already have two; 13 more are shaped to.
- **Links with parentheses in the web address** (e.g. UN resolutions, `.../232(1966)`) are cut at the first ")" by eight copies of the link reader; 35 such links; some render broken.
- **Pages published with people or months missing**: three places in the build catch any error, print a line and leave the item out; CI sees only success.
- **A merge can lose work.** It reads the month files, works for minutes, then writes them back whole: an edit made meanwhile by anyone else is overwritten, and two merges at once can clobber each other (no lock). Deferred ops are removed before they are applied, so a failure loses them. A merge whose ops failed still reports success and files the patch as merged.
- **A bad patch stops a merge midway** instead of being reported (an error type that escapes the handlers meant to catch it).
- **Patch ops can rename an entry's id or remove it** (confirmed): the merge writes the files before the check notices.
- **The YAML writer mishandles some keys** (`on`, `no`, `#x`, `"1961"` would read back changed); none in the data today.
- Smaller: a cache keyed by a memory address that can be reused; a fixed temporary file name that two agents can share; a cache that can serve a file's old contents if rewritten within milliseconds.
- **Docs that promise checks that don't exist**: `CLAUDE.md` says `check` enforces "Anniston, Ala." at a small town's first mention; no code does. The calendar-by-day guide says the *Times* is unlinked during the 1962–63 strike; the code links every day.

### 3. Speed (cheap, large, and it makes every later step faster)
Measured: `check` 9 min cold (as CI always is), 3 min warm; the calendar build 16 min; patch-check of a 1,000-op patch 8.5 min; its merge about 13.
- The build recomputes one index of the whole calendar **44 times** (about half the build). One hour to fix.
- YAML is read with the slow reader: switching to the fast one PyYAML already has cuts file reading from 43 s to 5 s, identical results. Fifteen minutes.
- Patch-check runs two whole-series checks twice to compare them; the merge rebuilds its index after every op and scans the whole list for every added entry; a stale `base:` triggers a 5-minute history search; CI runs the full check twice.
- **Expected after the main fixes:** check under 1.5 min, the calendar build about 5 min, patch-check of a large patch under 1 min. For agents: faster merges, less waiting, less polling.

### 4. Repetition (DRY): one rule, many copies, drifting
- The note grammar ("To check:", "Check:", "Names:", sentence breaks) parsed in 6+ places that disagree: the source of bug 2a.
- The link and card markup re-read by ~40 private patterns in 14 modules: bug 2b.
- 28 month tables, 23 date formatters (some crash on a month-only date, some print "1962, spring, 1962").
- 14 tables of the U.S. States (one lacks Alaska, Hawaii and D.C.); 4 registries of time zones besides the new gazetteer.
- 37–40 copies of the "make text safe for HTML" function in 5 behaviours; `fold` in 4 versions (two turn "Đà Nẵng" into "a Nang"); surname in 9; ordinal in 8; 21 web fetchers.
- Recommendation: one home each (`notes.py`, `markup.py`'s patterns, `dates.py`, `states.py` on `sources/states.yaml`, the gazetteer for zones, one `esc`), every caller switched, the golden tests proving the pages unchanged.

### 5. Structure (maintainability and readability)
- **Page assembly** is about 19 steps that each patch the finished HTML text, in an order written only in comments, kept in two hand-copied lists that must match, passing data through shared global values. A step that can't find its spot drops its table silently. This is the section most likely to break when anyone changes anything.
- **About 60 hidden caches** and shared globals, cleared by hand in scattered places: whether merge and patch-check are right depends on which were cleared.
- **`check.run`** is one 410-line function covering ~40 rule families, with inconsistent result shapes; the checker imports the renderer.
- **The data's fields are not declared anywhere**: a typo like `thred:` or `time_zon:` is kept and silently ignored. A field registry and an "unknown field" check would catch them.
- Very long functions in `lives.py` (one of 379 lines, twelve functions nested inside it), `executive.py`, `daybook.py`.
- 1,300 lines of CSS and JavaScript held as text inside Python, beside real `.css`/`.js` files elsewhere: three conventions.
- STYLE rules cited by number in 234 places, so inserting a rule renumbers the rest silently.

### 6. Clean-up
- Dead code: 7 functions nothing calls; the retired publish/import route (`importer.py`, `htmlparse.py`, two commands; `status` still advertises it); ~850 lines of one-time migrations; two map scripts.
- 110 one-off scripts in 21 folders with three import styles: mark each generator or one-off; shelve the dead.

**What is good and should stay**: the data loading (clear error messages, git-conflict detection); the curling self-check in `smart.py`; the `problems()` + `ok:<rule>` convention; the `./bib` commands, the ledger's lock, the entry-by-entry git merge driver; the STYLE blocks as specifications (they need stable names, not removal).

## Outside libraries versus our own code

**The considerations.**
- *For a library*: other people have found and fixed its bugs; agents know the popular ones (pytest, Jinja2, requests) well, so code built on them is easier for an agent to change correctly; less of our code to maintain.
- *Against*: every library the build needs is one more thing that can fail the deploy, or change when a new version comes out (hence pinning); some are slower to start; and swapping one in must not change a single byte of the YAML files (people read their diffs) or the pages.
- *This project's shape*: most of our "home-made" code encodes house style no library knows (Bluebook cites, *id*. rules, the curling rules, the field-aware merge). That code should stay ours. What hurts is not that it is home-made but that it is copied.

**The recommendations, ranked.**
| Component | Ours | Candidate | Recommendation |
|---|---|---|---|
| tests | none | **pytest**, **hypothesis** | **Adopt** (test-only: not needed to build the site) |
| YAML reading | slow reader | **libyaml (CSafeLoader)**, already inside PyYAML | **Adopt** (no new library) |
| versions | unpinned | `requirements.txt`; the **tzdata** package for historical time offsets | **Adopt** |
| YAML writing | our emitter | ruamel.yaml | Keep ours; fix its key handling; tests guard its exact format |
| HTML pages | Python text | Jinja2 templates | Not as a rewrite now; reconsider only when the page assembly is rebuilt (cluster 5), if the goldens show identical output |
| markup | ours | markdown-it, mistune | Keep ours (the cite rules); centralize the patterns |
| curly quotes | `smart.py` | smartypants | Keep ours (house rules) |
| field checks | `check.py` | jsonschema, pydantic | Keep; add a small field table |
| merge | ours | none exists | Keep |
| web fetchers (21) | ours, each different | requests + requests-cache | One shared fetcher, standard library; these are local tools, not the build |

## How to carry it out: rewrite everything, rewrite sections, or edit in place

- **Rewrite the whole codebase from scratch**: not recommended. 64,000 lines of accumulated house rules (each owner ruling of the past weeks lives somewhere in the code); a fresh version would lose many silently; weeks of agent time; the reading would stop meanwhile. Highest token cost (very roughly 20–40 million) and highest risk.
- **Edit in place, piece by piece**: cheapest per change, but (as the owner says) agents editing a tangled section make local decisions that break distant things; in the page assembly especially, that is how blocks vanish. Fine for small, well-tested pieces.
- **Recommended: tests first, then rewrite whole sections behind them.** Write the golden tests and the unit tests first (cluster 1). Then:
  - *small fixes in place*, each with its test (clusters 2, 3, 6);
  - *consolidation* as "build the one new module, switch every caller, prove the pages identical" (cluster 4);
  - *three whole-section rewrites* for the tangled parts, each a fresh, self-contained replacement held to byte-identical output: the page assembly (one written pipeline, no globals), `check.run` (a registry of named rules), and the long `lives.py` functions. An agent rewriting a whole section against a test is not distracted by the old code's detours.

## What it would cost in Claude usage

Rough figures, in millions of tokens (M); a reading run tonight cost 0.3–0.45M.
| Step | Cost |
|---|---|
| 1. Tests: golden + unit + property tests, the fixture, CI job (2,000–2,500 lines) | 2–3M |
| 2. Live bugs | 1–1.5M |
| 3. Speed | 1–1.5M |
| 4. Consolidation | 2–3M |
| 5. Three section rewrites | 3–5M |
| 6. Clean-up | 0.5M |
| **Total** | **about 10–15M**, spread over several nights, 1–2 agent slots at a time |

Each step is reviewed by an Opus auditor like the reading patches (included above). **What it saves afterwards**: agents read smaller, single-purpose modules (fewer tokens to understand a task); fewer bugs to chase (tonight's deploy failure and the 90-minute build each cost a few hundred thousand tokens to diagnose); faster check and merge (less waiting and polling). A modest, continuing saving, chiefly in the code-change tasks, not the reading.

## Questions for the owner

1. **Priorities.** Defer to me (your stated order: maintainability, readability, DRY, performance, NIH), or another order? I'd bring the cheap speed fixes forward, because they make every later step and every merge faster.
2. **Approach.** Tests first, then whole-section rewrites behind them (recommended); or a whole rewrite; or edits in place only.
3. **Libraries.** Test-only tools plus pinned versions, nothing new in the build (recommended); or also Jinja2 templates for the rebuilt page assembly; or none.
4. **Timing.** The live bugs now and the rest in one or two slots alongside the reading (recommended); or all of it after the China step; or pause the reading until it's done.
