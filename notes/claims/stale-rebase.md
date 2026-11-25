# The stale claim maps, rebased (Nov. 25, 2026)

Step 2 of the claims work (`notes/proposals/claims-model.md`, (f) 2 and (h) 2). The tool is `tools/claims/rebase_stale.py`; its rules are at its head. The table of every entry is `notes/claims/stale-rebase.tsv`.

A map is the list of an entry's sources and the units of the line each supports. A map records which line it was made against. It is stale when the line has changed since, or when it recorded no line at all.

## The counts

- Stale maps before: 1048. After: 12.
- 905: the line's units are the same as when the map was made. Only the record of the line was missing or out of date. It is written now. Most of these maps had recorded no line; the build already showed them with their footnotes.
- 9: units were added or removed. The rows now name the present letters. A row for the whole line that was made before a sentence was added now names only the older units, so the old source is not made to support the new words.
- 122: the words of a unit changed (many are only diacritics or a spelling). The rows keep the unit. These are listed below for a reader to confirm that the source still supports the changed words.
- 4: a row names units that are gone, or letters the old line never had. These maps are not rewritten and stay stale. Listed below.
- 8: the map names letters, and the line they were counted on is in no commit (the reader hashed a draft that the audit then changed). Not rewritten; they stay stale. Listed below.
- 19 entries had been shown as one block because their map was stale and now show footnotes again. Listed below.

Variants and visibility rulings also name units by letter, and record no line. The tool does not change them. Where an entry has one and its units moved or changed, the table says so (5 entries).

## For a reader: maps not rewritten

- `cal.1961-08.china-leadership-6`: no old line
- `cal.1962-02-03.china-leadership-5`: no old line
- `cal.1962-03-20.china-leadership-6`: no old line
- `cal.1962-06-11.china-leadership`: no old line
- `cal.1963-05-02.china-leadership-8`: no old line
- `cal.1964-06-17.civil-rights-bill-4`: lost (all -> A-B, E; D not in the old line; words changed in B, E; new: C-D; has a variant or a visibility ruling that names letters)
- `cal.1966-05-04.china-leadership`: no old line
- `cal.1966-05-17.china-leadership-7`: no old line
- `cal.1966-08-24.china-leadership-15`: no old line
- `cal.1967-11-29.robert-kennedy-2`: lost (all -> B, E-F; A, C-D -> E-F; B, C, D, E, F not in the old line; words changed in B; new: A, C-D, G-J; gone (old letters): A)
- `cal.1968-07-26.elections-1968-2`: lost (all -> ? (its units are gone); all -> ? (its units are gone); new: A-C; gone (old letters): A)
- `cal.1968-11.china-leadership-6`: lost (all -> ? (its units are gone); new: A-B; gone (old letters): A-B)

## For a reader: a unit's words changed, or a variant or ruling names letters

- `cal.1960-02.defense-2`: all -> A; all -> A; words changed in A; new: B
- `cal.1960-02-07.elections-1960`: words changed in B
- `cal.1960-02-11.vietnam-diplomacy`: words changed in A
- `cal.1960-02-27.sit-ins`: words changed in D
- `cal.1960-04-08.vietnam-diplomacy`: words changed in A
- `cal.1960-04-09.vietnam-hanoi-2`: words changed in A
- `cal.1960-04-13.laos`: words changed in A
- `cal.1960-04.china-leadership-15`: words changed in B
- `cal.1960-06-30.laos`: words changed in A
- `cal.1960-07-14.elections-1960-los-angeles-3`: all -> B, D, G; all -> B, D, G; words changed in B; new: A, C, E-F; gone (old letters): A
- `cal.1960-08-03.soviet-union`: words changed in A
- `cal.1960-08-15.china-leadership-10`: words changed in A
- `cal.1960-09-02.vietnam-diplomacy`: words changed in A
- `cal.1960-09-03.laos`: words changed in A
- `cal.1960-09-26.china-leadership-12`: words changed in A
- `cal.1960-10-05.laos`: words changed in A
- `cal.1960-10-18.elections-1960-kennedy`: words changed in A; gone (old letters): A-B
- `cal.1960-11.soviet-union`: words changed in B
- `cal.1960-12-14.china-leadership`: words changed in A
- `cal.1960-12-19.laos`: words changed in A
- `cal.1960-12-24.china-leadership-10`: words changed in A
- `cal.1960-12-26.china-leadership-8`: words changed in A
- `cal.1961-01-03.laos`: words changed in A
- `cal.1961-02-10.laos`: words changed in A
- `cal.1961-06-23.laos`: words changed in A
- `cal.1961-07-24.vietnam-diplomacy`: words changed in A
- `cal.1961-08-02.vietnam-hanoi`: words changed in A
- `cal.1961-08-30.laos`: words changed in A
- `cal.1961-10-30.vietnam`: words changed in A
- `cal.1961-11-16.vietnam-2`: words changed in A, C
- `cal.1961-11-25.laos`: words changed in A
- `cal.1961-12-02.laos`: words changed in A
- `cal.1961-12-18.laos`: words changed in A
- `cal.1961-12-21.vietnam-diplomacy`: words changed in A
- `cal.1962-01-02.vietnam-2`: words changed in A
- `cal.1962-01-03.china-leadership-9`: words changed in A
- `cal.1962-01-13.vietnam-3`: words changed in B-C
- `cal.1962-01-22.laos`: words changed in A
- `cal.1962-02-07.cuba`: words changed in A
- `cal.1962-02-15.vietnam-diplomacy`: words changed in A
- `cal.1962-02-15.laos`: words changed in A
- `cal.1962-02-16.laos`: words changed in A
- `cal.1962-02-17.laos`: words changed in A
- `cal.1962-02-28.laos`: words changed in A
- `cal.1962-04-23.vietnam-diplomacy`: words changed in A
- `cal.1962-05-10.laos-2`: words changed in A
- `cal.1962-05-29.laos`: words changed in B
- `cal.1962-07-30.laos`: words changed in A
- `cal.1962-09-13.missile-crisis-2`: words changed in B
- `cal.1962-09-18.china-leadership`: words changed in A
- `cal.1962-10-23.missile-crisis-excomm`: words changed in B
- `cal.1962-10-28.missile-crisis-settlement`: all -> D-F; all -> D-F; words changed in D-E; new: A-C, G; gone (old letters): A
- `cal.1962-10-30.missile-crisis-2`: words changed in A
- `cal.1962-12-25.china-leadership-7`: words changed in A
- `cal.1963-01-01.china-leadership-9`: words changed in A
- `cal.1963-01-15.laos`: words changed in A
- `cal.1963-01-17.china-leadership-7`: words changed in A
- `cal.1963-05-04.elections-1964-2`: all -> A-B, E-F; words changed in A-B, E; new: C-D
- `cal.1963-07-08.vietnam`: words changed in A
- `cal.1963-07-26.china-leadership-11`: words changed in B
- `cal.1963-09-20.vietnam-diplomacy`: words changed in A
- `cal.1963-10-16.vietnam`: words changed in A
- `cal.1963-12-31.vietnam-operations`: A, B -> A-B; words changed in A-B; has a variant or a visibility ruling that names letters
- `cal.1964-02-21.china-leadership-4`: words changed in B
- `cal.1964-05-01.china-leadership-6`: words changed in C
- `cal.1964-06-17.civil-rights-bill-4`: all -> A-B, E; D not in the old line; words changed in B, E; new: C-D; has a variant or a visibility ruling that names letters
- `cal.1964-07-09.civil-rights-bill`: words changed in A
- `cal.1964-10-14.soviet-union`: all -> A-J; all -> A-J; new: K-M; has a variant or a visibility ruling that names letters
- `cal.1964-10.vietnam`: words changed in A
- `cal.1964-11-06.vietnam-2`: words changed in A
- `cal.1964-12-14.laos`: words changed in A
- `cal.1964-12-21.laos`: words changed in A
- `cal.1964-12-25.laos`: words changed in B
- `cal.1965-01-10.china-2`: words changed in B
- `cal.1965-02-19.laos`: words changed in A
- `cal.1965-04-05.vietnam-air-war-3`: words changed in A
- `cal.1965-04-12.vietnam-2`: words changed in A
- `cal.1965-04-14.vietnam-air-war-3`: words changed in A
- `cal.1965-04-22.vietnam-air-war`: words changed in A
- `cal.1965-05-08.china-leadership-3`: A, B-C -> A-C; words changed in A; has a variant or a visibility ruling that names letters
- `cal.1965-05-21.china-leadership`: words changed in A; has a variant or a visibility ruling that names letters
- `cal.1965-06-25.vietnam-air-war`: words changed in A
- `cal.1965-07-02.vietnam-air-war`: words changed in A
- `cal.1965-07-09.vietnam`: words changed in A
- `cal.1965-07-11.vietnam-air-war`: words changed in A
- `cal.1965-07-14.vietnam-air-war-2`: words changed in A
- `cal.1965-07-22.vietnam-2`: words changed in A
- `cal.1965-07-22.vietnam-air-war-2`: words changed in A
- `cal.1965-07-28.vietnam-air-war`: words changed in C-D
- `cal.1965-08-06.vietnam-air-war`: words changed in B
- `cal.1965-08-26.vietnam-air-war`: words changed in A
- `cal.1965-09-03.states-and-cities-2`: words changed in A
- `cal.1965-10-21.confirmations`: words changed in A
- `cal.1965-11-10.vietnam-3`: words changed in A
- `cal.1965-12-29.vietnam-pause-2`: words changed in A
- `cal.1966-01-07.china-2`: all -> A; words changed in A; new: B
- `cal.1966.china-leadership-52`: words changed in A
- `cal.1966.china-leadership-63`: words changed in B
- `cal.1966-02-06.vietnam-air-war`: words changed in A, C
- `cal.1966-02-15.vietnam-air-war`: words changed in A
- `cal.1966-03-08.vietnam`: words changed in B
- `cal.1966-04-01.vietnam`: words changed in A
- `cal.1966-05-06.china-leadership-7`: words changed in B
- `cal.1966-09.vietnam`: words changed in A
- `cal.1967-01-03.china`: all -> A; words changed in A; new: B
- `cal.1967-04-09.vietnam`: words changed in A
- `cal.1967-04-10.laos`: words changed in A
- `cal.1967-10-14.vietnam-order-of-battle`: words changed in C
- `cal.1967-10-20.vietnam`: words changed in A
- `cal.1967-11-16.vietnam-commitments`: words changed in C
- `cal.1967-12-08.vietnam`: words changed in A
- `cal.1968-01-02.china`: all -> A; words changed in A; new: B
- `cal.1968-01-23.laos`: words changed in C
- `cal.1968-01-28.robert-kennedy-campaign`: all -> A-B, D; words changed in A-B, D; new: C; gone (old letters): C
- `cal.1968-03.robert-kennedy-2`: all -> A-B; words changed in A; new: C
- `cal.1968-06-07.soviet-union`: all -> A-C; words changed in C; new: D
- `cal.1968-07-23.court-fortas`: words changed in A
- `cal.1968-08-22.press-and-broadcasting`: words changed in A
- `cal.1968-08-27.elections-1968-chicago`: words changed in B
- `cal.1968-08-28.elections-1968-chicago`: words changed in D
- `cal.1968-09-26.program`: words changed in B
- `cal.1968-10-22.vietnam`: words changed in B
- `cal.1969-01-04.china`: all -> A; words changed in A; new: B
- `cal.1969-01-19.transition-and-staff`: words changed in H

## Entries that show footnotes again

- `cal.1960-02.defense-2`
- `cal.1960-02-27.sit-ins`
- `cal.1960-07-14.elections-1960-los-angeles-3`
- `cal.1960-11.soviet-union`
- `cal.1962-10-28.missile-crisis-settlement`
- `cal.1962-10-30.missile-crisis-2`
- `cal.1963-05-04.elections-1964-2`
- `cal.1963-11-22.transition-and-staff`
- `cal.1964-10-12.soviet-union`
- `cal.1964-10-14.soviet-union`
- `cal.1964-12-14.laos`
- `cal.1965-03-01.vietnam-congress`
- `cal.1965-05-08.china-leadership-3`
- `cal.1965-05-21.china-leadership`
- `cal.1967-11-16.vietnam-commitments`
- `cal.1968-01-28.robert-kennedy-campaign`
- `cal.1968-03.robert-kennedy-2`
- `cal.1968-08-28.elections-1968-chicago`
- `cal.1969-01-19.transition-and-staff`
