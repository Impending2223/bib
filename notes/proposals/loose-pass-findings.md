# The loose-dates pass, 1961–70: what it found beyond the ghost days (Nov. 19–20, 2026)

Each year's patch was read by a reader and audited by Opus before merge (`inbox/merged/2026-11-19-loose-<year>.yaml`). Below: the entries the audits found dated to the day (for the lead to date by patch), the likely duplicates (for `./bib combine`), and the questions the rules do not settle.

## Code
- Done (Nov. 19, 309c7c4): check `[loose-at-month]` refuses an `at` before the entry's own month or year (the winter's December solstice excepted); patch-check holds an add's or edit's `place:` to check's `[place]`.


## 1965–66 (merged: 99 ops)
- Sure: 1965-02.republican-party-congress Feb. 24; 1965-04.vietnam Apr. 28; 1965-07.vietnam July 26; 1965-07.vietnam-congress-2 July 22; 1965-09.china-leadership-2 Sept. 16; 1965-09.civil-rights-the-executive Sept. 21; 1965-09.latin-america-dominican-republic Sept. 17 (drop its at); 1966-01.robert-kennedy Jan. 18; 1966-03.transportation-san-francisco Mar. 21; 1966-05.republican-party May 6; 1966-12.open-housing Dec. 16; 1965-01.transition-and-staff-nsc Feb. 2 (out of its month).
- Likely: 1965-01.china-leadership-3 Jan. 15 (bundles Jan. 12–13: split); 1965-04.vietnam-force-levels about Apr. 27; 1965-08.conservation about Aug. 9; 1966-04.war-opposition-5 about Apr. 15; 1966-05.congress May 11; 1966-05.war-opposition about May 24; 1966-07.china-leadership-13 July 9; 1966-07.vietnam-congress-2 July 16; 1966-12.students about Dec. 18; 1965-04.robert-kennedy-2 about Apr. 21–23, 1965-09.vietnam-support about Sept. 9, 1966-02.vietnam-3 about Feb. 14, 1966-07.robert-kennedy-2 July 24 (these four keep an at: drop it when dated).
- Duplicates: 1965-06.king with 1965-11.king and 1965-12.king; 1965-07.press-and-broadcasting with 1965-08.robert-kennedy.
- Ruled: a note's own date may anchor an op (L1, L3).
- For the owner: which April 1965 Honolulu conference (Apr. 8–10 or 20); the MACV History's "Apr. 10–13" conference; 1965-05.latin-america-dominican-republic (Mann's "early May" vs the Digest's July 14); 1965-03.vietnam-force-levels (Mar. 13 or 26); "at the beginning of the Cultural Revolution" (which event?).

## 1967 (merged: 69 ops)
- Sure: 02.mississippi Feb. 27, 8:10 p.m. Central; 04.republican-party-congress-3 Apr. 20.
- Likely: 05.vietnam-congress May 17; 12.vietnam-operations Dec. 14.
- For the owner: 1967.china-leadership-123 ("1967, end": the year-end ruling); 06.war-opposition-2 (two resignations, June 13 and 27: split?); 11.press-and-broadcasting-2 (Bernstein: February); 03.republican-party-5 (April?); 01.congress-powell; 07.vietnam-2, -3 (the mission's announcement, July 12 or 14); 06.civil-disorders-minneapolis; 11.vietnam-8 (December?); 05.open-housing-2; 06.open-housing-2; "by April": entries.md's example sets `before YYYY-04`, loose-pass L3 and STYLE 3a leave a "by" in the block — one rule wanted; approximate offsets ("three weeks after", "a fortnight before") placed on the computed day.

## 1968–70 (merged: 93 ops)
- Sure: 02.robert-kennedy-campaign-3 Feb. 18; -4 Feb. 17–18; 04.robert-kennedy-campaign-primaries-2 Apr. 22; 03.king Mar. 5; 10.vietnam-prisoners Oct. 21; 04.soviet-union-leadership-2 Apr. 9–10; 10.elections-1968-2 Oct. 12–13.
- Likely: 02.press-and-broadcasting Feb. 23; 03.elections-1968-2 Mar. 28 (McPherson: mid-March).
- For the owner: 12.transition-and-staff-2 ("the week before" Dec. 11); 10.china-leadership-2 (after or before the Twelfth Plenum); 02.elections-1968-2 (Manchester or Berlin, N.H.); 1969-07.vietnam-hanoi (July or August); an entry placed after an event itself loosely dated (06.elections-1968-congress, 01.robert-kennedy-2).

## All years
- Times in the text of month- or year-dated entries ("5 p.m.", "a night", "at lunch") cannot be stored without a day: should a month-dated entry carry a time band with no range?
- A year's end ("1962, end", "at the year's end"): ruling pending.

## 1964 (merged: 107 ops)
- Sure: 04.civil-rights-bill Apr. 9; 01.vietnam-4 Jan. 28; 08.elections-1964-4 Aug. 1; 09.elections-1964-5 Sept. 11; 09.vietnam Sept. 25–29; 11.vietnam-saigon-2 Nov. 11; 12.republican-party Dec. 6; 12.republican-party-2 Dec. 21; 12.press-and-broadcasting-2 Dec. 2.
- Likely: 09.laos Sept. 11 (the meeting; split); 12.press-and-broadcasting Dec. 2; 06.elections-1964-state-conventions-3 June 30; 09.goldwater-11 about Sept. 25; 01.elections-1964-3 Jan. 13; 08.robert-kennedy Aug. 1–2; 07.press-and-broadcasting about July 7; 02-23.economy Feb. 23; 05.conservation May 6 (a second event: split).
- Duplicates: cal.1964-10.elections-1964-3 into cal.1964-10-14.elections-1964-4; maybe 10.elections-1964-5 with cal.1964-10-10.elections-1964-johnson.
- The audit's ruling, applied: a newspaper of the Nth places a month-dated act on or before the Nth (a paper of the 1st–10th: early). "The week before X": before the Sunday that opens the week before X's week.
- For the owner: "1964, by April" set `before 1964-04` (entries.md's example) though STYLE 3a would leave a "by" in the block; the two rulings above; 03.vietnam-2's note still says Mar. 8 (the lead to correct); 07.vietnam-6 (June?); arguable: 07.mississippi, 07.goldwater, 08.transition-and-staff, 02.china-leadership-5, 12.program, 12.republican-party-congress-2.

## 1962 (merged: 60 ops)
- Sure: 02.elections-1964 Feb. 2; 01.defense Jan. 11 (the order); 11.king Nov. 20; 09.goldwater Sept. 27–28.
- Likely: 12.missile-crisis Dec. 8 (the *Post*'s issue date); 1962.china-leadership-5 July 22; 12.soviet-union Dec. 2; 07.china-leadership-4 July 30 (the letter of Aug. 8 a second act: split).
- Duplicates: cal.1962-03.soviet-union into cal.1962-03-07.soviet-union-2 (Salinger's Apr. 5 a variant).
- For the owner: which day opens "the crisis" (Oct. 14, 15 or 16); "after a span": after its last day?; cal.1962-04-13.goldwater as Apr. 13–14 (White)?; 07.defense-4 July 20 (calendar) or 19 (Taylor); "Easter Week" (Holy Week or the week after Easter, Apr. 22); "1962, later" as "late"?; 12.vietnam-hanoi "at the year's end"; 12.school-aid (Graham: 1963); 06.civil-rights-the-executive "after the Belafonte concert" (June 6?); 02.robert-kennedy "at the start of the trip" (Feb. 1?); 02.latin-america-3 (April?); a time band on a month-dated entry (six cues: lunch, that night, a dinner).

## 1961 (merged: 79 ops)
- Sure: 02.cuba-2 Feb. 13; 02.robert-kennedy Feb. 10; 04.china-leadership-8 Apr. 1; 05.space May 6; 06.china-leadership-2 June 22; 08.crime-and-hijacking-maheu Aug. 16; 10.desegregation-schools Oct. 16; 11.china-leadership Nov. 23; 01.republican-party-congress Jan. 3–5; 03.china-leadership-5 Mar. 15–23.
- Likely: 02.defense Feb. 24; 05.cuba May 17 (needs a split); 06.right-and-the-military June 28; 07.testing July 10; 08.mississippi Aug. 7 (runs to Aug. 22: split); 09.berlin-and-vienna Sept. 23 (Fursenko Sept. 24); 10.china Oct. 23; 10.cuba Oct. 5; 11.vietnam-hanoi Nov. 14; 12.china Dec. 15–31 (over a week); 03.laos-2 about Mar. 15.
- Duplicates: 05.civil-rights-the-executive with cal.1961-05-09.civil-rights-bill.
- For the owner: 04.testing (Easter, Apr. 2, against "shortly after the Bay of Pigs"); 06.goldwater-2 misdated (to July, "after the 13th"?); 07.press-and-broadcasting "the Fourth of July weekend" (July 4 a Tuesday); 12.press-and-broadcasting "the Christmas holiday"; day counts from an event ("about a week before the landing", "two weeks after", "three weeks after the Bay of Pigs"): no rule; a part of the day on a month-dated entry ("a November afternoon"); 03.laos-3, 05.latin-america-4 (month doubted).

## 1963 (merged: 91 ops)
- Sure: 02.defense-4 Feb. 10; 05.civil-rights-bill May 23.
- Likely: 02.defense-3 Feb. 12; 04.testing-2 Apr. 7 (bundles a later draft: split); 05.elections-1964-3 May 10; 05.crime-and-hijacking-2 Apr. 24 (out of May); possibly 02.defense-5, -6, -7 Feb. 8 and -8 Feb. 9.
- Duplicates: 09.vietnam-congress with cal.1963-09-12.vietnam; 07.elections-1964-4 with 07.republican-party-5 (the Hatfield quotation); 07.republican-party-congress with -congress-3 (Curtis); the Dec. 1 and Dec. 8 *Times* entries (one story?), then 12.republican-party after it.
- For the owner: 04.testing (Apr. 22, a Monday, against Reeves's "a Friday"); 01.goldwater; 10.civil-rights-bill (September?); 12.elections-1964 (Dec. 14 or 15); 01.china-2 (the Malraux talk of Jan. 9?); 01.democratic-party; "late spring", "late summer" (no thirds for a season); two headings after Nov. 22 ("After Nov. 22", "Nov., after the assassination"): one?; "before X" with a lower bound also given (06.europe-and-the-alliance-kennedy-in, 11.succession).
