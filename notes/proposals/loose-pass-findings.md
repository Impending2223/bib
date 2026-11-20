# The loose-dates pass, 1961–70: what it found beyond the ghost days (Nov. 19–20, 2026)

Each year's patch was read by a reader and audited by Opus before merge (`inbox/merged/2026-11-19-loose-<year>.yaml`). Below: the entries the audits found dated to the day (for the lead to date by patch), the likely duplicates (for `./bib combine`), and the questions the rules do not settle.

## Code
- `loose.at_problems` (used by check) accepts an `at` before the entry's own month without a warning (`before 1962-12-22` on a 1963-02 entry): such an `at` silently moves the entry into the month before. Make it an error unless tagged `ok:loose-at`.

- `patch-check` does not validate `place:` keys set by an `edit` (the 1962 audit's finding): an unknown key passes and fails only at check after merge. Validate against sources/places.yaml plus the patch's own `place-key` ops.

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
