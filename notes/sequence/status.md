# The sequence pass (R25c; owner-rulings 55): where each month stands

One line a month. Brief: `notes/briefs/sequence-<month>.md` (reader, Sonnet), `sequence-audit-<month>.md` (audit, Opus). Patch: `inbox/2026-11-25-sequence-<month>.yaml`, moved to `inbox/merged/` at the merge. Merges go one at a time, under the lock (`flock` on the session's `tree.lock`): `./bib merge --auto`, `./bib conflicts`, `./bib check`, commit.

- Merged: 1962-10, 1968-03, 1967-01, 1960-07, 1960-10.
- Audited, merging (Nov. 25, about 2:00 a.m. PT): 1961-01, 1964-06, 1965-03, 1966-08, then 1964-01.
- Audit out: 1961-04, 1968-08, 1966-06, 1963-11.
- Reader out: 1960-09, 1964-08, 1960-11, 1961-05, 1965-04, 1968-01, 1964-04, 1965-07.
- Next by size: 1963-12, 1964-11, 1964-03, 1964-02, 1964-10, 1965-08, 1968-07, 1965-02, 1965-06, 1964-05, 1968-02, 1960-05, 1965-11, 1965-05, 1963-10, 1961-03, 1965-09, then the rest by size.
- What the audits have shown so far: a reader's links from the entries' own words hold about nine in ten; links from the printed order of a day's items in a chronology or a volume of speeches do not (January 1964: 16 of 36 struck; R25c now says so); each audit adds about a third again.

What each audit found besides links (entries to split, hours to set, days in doubt, possible duplicates) is in its `audit-<month>.md`, for a later pass.
