# Loosely dated entries: tags and the intercalary days (Nov. 15, 2026)

The owner, Nov. 15: "Is there anything we could do, or should do, to the individual, imprecisely-dated entries to better sort them? ... Could we default to displaying them in 'ghost' days, or 'follows:' days, at the earliest date implied by their range?"; then: "I'll take your recommendations for tagging loosely dated entries, but I'm not sure about your recommendations for the display. By 'ghost' days I meant '"days" that aren't days'. 'after X' shouldn't be on X's day, but an, uh, intercalary day after X's day. 'X bis.' The heading of that intercalary 'ghost' day/'fake' day, 偽日 (にせび), is the loose date in the heading line. Not in grey, but in ordinary day styling. For early, middle, and late, divide each month into thirds, and give entry the day *before* the first portion of that third falls on. 'Early May' after 'May' and before 'May 1.' ... For seasons ... Put the intercalary seasons on 'ghost' days/'fake' days preceding the first day of the astronomical season. Year alone goes before 'January,' which is before 'early January,' which is before 'January 1.'"

Today: 3,913 entries are dated to a month only; 818 of them say more in `when` ("May, late", "Jan., early", "fall"). All sit in the month's undated block at its head. A year-only date is refused by `check` (R15 as amended allows it; queued).

## The tag (approved)
- `date` stays as the source gives it: `'1962'`, `'1962-05'`, `'1962-05-14'`. Files and sections unchanged; a year-only entry is filed in the year's January.
- A hidden `at:` names the intercalary day the entry sits on: `before 1962-05-21` (late May), `after 1962-05-12` (after May 12), `before 1962-03-21` (spring 1962). Set by a script from `when`; set or corrected by readers from the note's own detail ("after the 12th", "the week after the convention"). No `at` on an entry with a full date; none needed on a plain month ("May") or a plain year ("1962").

## The intercalary days (偽日)
- An intercalary day is a heading in the day's ordinary style whose text is the loose date ("Late May", "After May 12", "Spring"), holding every entry with that `at` and that wording, sorted as a day's entries are (thread, then text).
- The order within a year: the year ("1962"); then each month: the month ("May", the old undated block), "Early May", May 1 ... May 10, "Mid-May", May 11 ... May 20, "Late May", May 21 ... May 31. An "after X" day comes straight after X's day ("May 12 bis"), before any "before" day that falls between X and the next day. A season's day comes before the first day of the astronomical season.
- Thirds: the first day of the third k (0, 1, 2) of a month of L days is floor(kL/3) + 1. So: 31 and 30 days: the 1st, 11th, 21st; February of 28: the 1st, 10th, 19th; of 29 (1960, 1964, 1968, 1972, 1976): the 1st, 10th, 20th. "Mid-February 1962" sits before Feb. 10; "late February 1964" before Feb. 20.
- Seasons: the equinoxes and solstices, by year (Meeus's algorithm, in the build). In Washington time, 1960–69:
  1960 Mar. 20, June 21, Sept. 22, Dec. 21; 1961 Mar. 20, June 21, Sept. 23, Dec. 21; 1962 Mar. 20, June 21, Sept. 23, Dec. 22; 1963 Mar. 21, June 21, Sept. 23, Dec. 22; 1964 Mar. 20, June 21, Sept. 22, Dec. 21; 1965 Mar. 20, June 21, Sept. 23, Dec. 21; 1966 Mar. 20, June 21, Sept. 23, Dec. 22; 1967 Mar. 21, June 21, Sept. 23, Dec. 22; 1968 Mar. 20, June 21, Sept. 22, Dec. 21; 1969 Mar. 20, June 21, Sept. 23, Dec. 21. (In UTC nine of these forty fall a day later: 1960 Sept. 23, 1961 Dec. 22, 1962 Mar. 21, 1963 June 22, 1964 Sept. 23, 1965 Dec. 22, 1966 Mar. 21, 1967 June 22, 1969 Dec. 22. The owner to choose the zone.) "Winter 1962" is the winter beginning in December 1962 unless the source means the one ending in March; the reader says which in `at`.
- The thread's ⟨⟨ ⟩⟩ links, the visibility and the contents follow the same order.

## Open
- The zone of the seasons' days (Washington, or UTC).
