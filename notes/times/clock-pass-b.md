# Clock pass b: calendar entries of 1963, 1964 and 1965

Patch: `inbox/2026-11-25-clock-times-b.yaml` (0 errors under `patch-check`). 93 rows: 54 given a `time`, 6 given a `time_range`, 21 tagged `ok:fields-time` (the clock in the line is not the act's), 12 not settled and left alone. Sources read: the entries and their notes only; the Drive copies were not downloaded (the diary and books are large scans), so no hour was checked against a page.

## Not settled (no field set, no tag)

- cal.1963-06-25.republican-party: adjourned at 5:15 a.m., but the day is June 28 or 29, more than a day from the entry's date (June 25); `check` refuses a `time` that far out.
- cal.1963-09-13.baker: "home to Andrews ... 1 a.m." is on a day the line does not give (Sept. 14 to 16); the first proposal (Sept. 13) is likely wrong.
- cal.1963-12-17.china-leadership-4: "3时半" for the acupuncture; the diary's a.m. or p.m. is not in the note (probably p.m.).
- cal.1964-01.elections-1964-9: about 2 p.m., a Friday, Jan. 24 or 31; the day is open.
- cal.1964-06-21.mississippi: the line says "released after 10 p.m. June 23", the note (Dittmer, 247) has the release about 10:30 on the night of June 21; the line's "June 23" looks like an error in `c`. Not changed.
- cal.1964-10-01.students: the pact, Oct. 2, 7:30 p.m. Pacific, is Oct. 3 in UTC, two days from the entry's date.
- cal.1965-03-05.civil-rights-organizations: "toward midnight Saturday" (Mar. 6) is Mar. 7 in UTC, two days from the date.
- cal.1965-06.program: the hours (10:30 p.m., after midnight, 2 a.m.) are of a day in June not yet found.
- cal.1965-09.vietnam: "to near midnight" on a Sunday in mid-September, day not found.
- cal.1965-10-05.soviet-union-leadership: the 9 to 11:20 talk is Oct. 7, two days from the date (Oct. 5).
- cal.1965-12-15.vietnam-hanoi: the fight ends at 3 p.m. Dec. 18, three days from the date.
- cal.1965-12-20.soviet-union-leadership: the 10:20 to 12 negotiation is Dec. 22, two days from the date.

## Tagged `ok:fields-time` (the hour is not the act's)

A deadline, a planned or quoted time, a statistic, or an appointment of another day: 1963-02.defense-8 (the hike's 7 a.m.; the day of the entry also open), 1963-05.king (2 a.m. of a day not found), 1963-07-09.railroads (midnight deadline), 1963-07-11.china-leadership-5 (the next day's session), 1963-07-17.civil-rights-bill-3 (Ervin's "at noon" of 1954), 1963-09-27.king (a figure of speech), 1963-11-22.press-and-broadcasting (a ratings hour), 1963-11.king (Dec. 3 appointment), 1964-04-10.civil-rights-bill-2 (next day's quorum call), 1964-05-17.china-leadership-4 (next morning's session), 1964-06-15.vietnam-4 (Johnson's question), 1964-07-02.civil-rights-bill-16 (the address's proposed hours), 1964-07-24.labor (the Goldwater appointment), 1964-09-27.mississippi ("before midnight", a bound), 1964-09.elections-1964-4 and 1964-09.elections-1964-johnson (daily habits), 1965-03-21.alabama-birmingham (the bombs' timer), 1965-09-19.china (a deadline), 1965-09-20.india-and-china (the cease-fire's effective hour, two days out), 1965-10-29.soviet-union-leadership and 1965-11-28.soviet-union-leadership (a flight out and a return, not the talks).

## For the auditor

- Several events, several hours; one time set, the first or the only one the line gives, and said in the note where it is not the first day's: 1963-06-25.china-leadership-2 (noon arrival; the midnight call not used), 1963-10-10.berlin-and-vienna (9 a.m. Oct. 11; the first act, Oct. 10, has no hour; the 12:30 meeting not used), 1963-11-04.berlin-and-vienna (11:30 Nov. 4; 6:10 p.m. Nov. 5 not used), 1964-05-13.elections-1964 (3:30 p.m. stop; 8 p.m. not used), 1964-08-04.vietnam (the 11:36 p.m. address; the day's other events have no hour), 1964-10-27.elections-1964-3 (2:30 a.m., the first hour of Johnson's day; 9:45, 11:30, 5:30 not used), 1965-05-01.latin-america-dominican-republic (6:40 p.m.; 2:14 a.m. and 1:03 p.m. May 2 not used), 1965-09-19.china-leadership (Mao's note at 4:30 a.m. by the Wengao, where the line says 4 a.m.; the midnight deadlines and 3:40 p.m. not used), 1965-12-08.vietnam-operations (a range for the afternoon of Dec. 8, the first act; the 10 a.m. landing of Dec. 9 not used), 1964-11-10.china-leadership (a range for the evening meeting; the 1 a.m. cable of Nov. 11 not used), 1964-05-20.china-leadership (a range from noon to the midnight return; Chen Yi's nianpu has "afternoon").
- Hours that are the end of an act ("to 5 p.m.", "until 10:15 p.m.", "done by 2 a.m.", the end of a day-long fight) are set as the `time`: 1963-04-23/24 (the telegram), 1964-02-23, 1964-03-05, 1964-03-13, 1964-03-23, 1964-04-05, 1964-05-12, 1964-06-16, 1964-07-02 (china-leadership-8), 1964-07-13, 1965-03-24, 1965-03-26, 1965-04-04, 1965-08-01, 1965-12-05, and 1963-07-20 (after 11:30, `time_approx`).
- Night hours in Yang Shangkun's diary fall on the next calendar day: confirmed by `follows` for 1963-04-24.china-leadership-13 (set at 2 a.m. Apr. 25) and 1964-01-04.china-leadership-5 (Jan. 5); assumed for 1964-03-13, 1964-04-05 ("after the evening's ball") and 1964-07-02 (the film, then the talk).
- A range of two readings by `follows`, not a doubt of clock, is used for 1963-06-11.civil-rights-bill-2 (after 4:30 p.m. to the 8 p.m. address; the "after 4:30" is a lower bound on when Salinger called the networks) and 1964-11-03.elections-1964-5 ("sometime after midnight", the predawn band).
- Clocks assumed, not found: Indonesia (Java) 1963 at UTC+7:30 (zoneinfo) for the two Liu Shaoqi entries; Mississippi and Alabama places in June 1963 and Selma and Birmingham at standard time (Etc/GMT+6 or America/Chicago); the LBJ Ranch at standard time (1965-04-09); Saigon time (+8) for the Vietnamese histories' hours (1965-06-30, 1965-12-05) and MACV (1964-11-08), whose clock the books do not say; Ball's own (Washington) clock for 1964-08-18.cyprus (the entry's place is Geneva); Turkey at +3 for 1964-06-10.cyprus.
- 1965-08-14.civil-disorders-watts: set at Califano's 9:09 p.m., read as Washington time (01:09Z Aug. 15). The Miller Center's 8:09 p.m. in the note's Check is the same instant if read as Central daylight time. Not confirmed.
- 1963-12-23.foreign-aid-4: "About 2 a.m." is set on Dec. 23 as the line dates it; the line does not say whether it was the night before the Rules vote.
- 1965-06-30.vietnam-hanoi-2: I replaced the note's sentence "The time is the first day's." with "The time is the attack's, 1 a.m. July 1." because the hour set is July 1's.
- No `place` or `at` field was added: the task was the time fields only.
- The mechanical proposals were wrong for several rows (zone Moscow for 1963-10-10; midnight at the start of Sept. 27 for a quotation; Sept. 13 for the Baker row) and were not used as given.

## R0

Nothing disregarded; no scope was narrowed by the task brief. The only limits applied are R25a's and `check`'s day-order rules.
