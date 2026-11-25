# The sequence pass (R25c; owner-rulings 55): where each month stands

One line a month. Brief: `notes/briefs/sequence-<month>.md` (reader, Sonnet), `sequence-audit-<month>.md` (audit, Opus). Patch: `inbox/2026-11-25-sequence-<month>.yaml`, moved to `inbox/merged/` at the merge. Merges go one at a time, under the lock (`flock` on the session's `tree.lock`): `./bib merge --auto`, `./bib conflicts`, `./bib check`, commit.

- Merged (23 months): 1960-07, 1960-09, 1960-10, 1960-11, 1961-01, 1961-04, 1961-05, 1962-10, 1963-11, 1964-01, 1964-04, 1964-06, 1964-08, 1965-03, 1965-04, 1965-07, 1965-08, 1966-06, 1966-08, 1967-01, 1968-01, 1968-03, 1968-08; the two struck links.
- Audited, on the pending list (the session's `pending.txt`; Nov. 25, 2:40 a.m. PT by the clock; a full build holds the lock first, and the PR to main follows it): 1964-10, 1964-02, 1964-11, 1964-03, 1963-12, 1965-02, 1964-05, 1960-05, 1968-02, 1965-06, 1968-07, 1965-05, 1965-11, 1963-10, 1961-03.
- Audit out: 1966-05, 1965-09, 1968-05, 1964-07, 1966-07, 1965-01.
- Reader out: 1967-08, 1963-05, 1964-09, 1966-03, 1963-06, 1963-04.
- Next by size: 1963-07, 1966-09, 1967-07, 1962-01, 1960-12, 1960-03, 1964-12, 1967-03, 1967-05, 1967-02, 1963-01, 1966-04, then the rest by size.
- What the audits have shown so far: a reader's links from the entries' own words hold about nine in ten; links from the printed order of a day's items in a chronology or a volume of speeches do not (January 1964: 16 of 36 struck; R25c now says so); each audit adds about a third again.

What each audit found besides links (entries to split, hours to set, days in doubt, possible duplicates) is in its `audit-<month>.md`, for a later pass.
