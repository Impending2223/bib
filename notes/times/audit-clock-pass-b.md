# Audit of clock pass b: calendar entries of 1963, 1964 and 1965

Patch audited and corrected in place: `inbox/2026-11-25-clock-times-b.yaml`. It shows 0 errors and 0 warnings under `./bib patch-check`. The reader's note is `notes/times/clock-pass-b.md`.

## What was read

Each of the 93 rows was read: the entry, its note and the patch's op. Where the hour, the day or the clock was in doubt, the source's page was read in the owner's copy or in the open record. Sources read: Yang Shangkun's diary, vol. II, pp. 273, 335, 340 (page images). Brezhnev's workbooks, vol. II, pp. 73–74, 81–82, 92, 97 (text and page image). *Lịch sử kháng chiến chống Mỹ*, III, 431–32, and IV, 62–63. Branch, *Pillar of Fire*, 113 and 463. Branch, *At Canaan's Edge*, 29, 42 and 140. Dittmer, *Local People*, 247. *United States v. Price*, 383 U.S. at 790. Young, *An Easy Burden*, 253–54. Sorensen, *Counselor*, 278–79. Califano, *Triumph and Tragedy*, 61. Lady Bird Johnson, *A White House Diary*, 91–93, 114, 177, 188, 257. Ball, *The Past Has Another Pattern*, 353–54 and 358. White, *The Making of the President 1964*, 100–01 and 372. The Free Speech Movement's leaflet (the linked chronicle). The recordings catalogues in `daybook/recordings/`. FRUS 1964–68, XXV, docs. 213, 222, 223. All copies were deleted after reading.

## Ops checked and held as written

- The Yang Shangkun entries with an hour after midnight are right to set it on the next calendar day. The page images confirm it for 1963-04-23, 1963-04-24 and 1964-01-04. The diary's own words in the note confirm it for 1964-03-13, 1964-04-05 and 1964-07-02.
- Java time (UTC+7:30 by zoneinfo) is held for Liu Shaoqi on 1963-04-16 and 1963-04-17. The nianpu does not say whose clock it uses.
- MACV's 7:15 a.m. on 1964-11-08 is held as Saigon time. MACV worked in Saigon.
- The Watts call of 1965-08-14 is held at 9:09 p.m. Eastern. Califano writes "Eastern time" on p. 61. A sentence giving his words was added to the note. The Miller Center's 8:09 p.m. stays as a Check. That 8:09 does not match the Ranch's clock either, since Texas kept standard time in 1965.
- Other hours held as set: 1963-07-12, 1963-07-20, 1963-10-10, 1963-10-26, 1963-11-04, 1963-12-23, 1964-02-05, 1964-02-23, 1964-03-05, 1964-03-23, 1964-04-19, 1964-05-09, 1964-05-12, 1964-05-13, 1964-06-06, 1964-06-10.laos, 1964-06-16, 1964-07-13, 1964-08-04 (both entries), 1964-08-18 (Ball's "around 2:00 a m Washington time", p. 358), 1964-10-27 (both entries), 1965-02-05, 1965-03-15, 1965-03-24, 1965-03-26, 1965-03-31, 1965-04-04, 1965-04-09, 1965-04-28, 1965-05-01 (both entries), 1965-06-12, 1965-08-01, 1965-09-19.china-leadership.
- The time ranges held: 1964-05-20, 1964-11-10, 1965-05-05, 1965-12-08. The range on 1963-06-11 was also kept, with a note added (below).
- Of the 21 `ok:fields-time` tags, 18 are held. In each, the clock in the line is not the time of the entry's act, or the entry is dated only to a month: 1963-02.defense-8, 1963-05.king, 1963-07-09, 1963-07-11, 1963-07-17, 1963-09-27, 1963-11-22, 1963-11.king, 1964-04-10, 1964-05-17, 1964-07-24, 1964-09-27, 1964-09.elections-1964-4, 1964-09.elections-1964-johnson, 1965-09-19.china, 1965-09-20, 1965-10-29, 1965-11-28.

## Ops changed (10)

- cal.1963-06-12.mississippi-2: the 1 a.m. is King's call to Gaston's in Birmingham (Young, 254). Birmingham's 1963 clock is in doubt, so the field is now a range covering standard and daylight time (06:00 to 07:00 UTC). A sentence giving the basis was added to the note.
- cal.1963-06-25.mississippi: the noon arrests were in Mississippi, whose clock is in doubt. The field is now a range covering both readings (17:00 to 18:00 UTC), with its basis in the note.
- cal.1963-06-11.civil-rights-bill-2: the range was kept. The note now says the range is Salinger's request, made after 4:30 p.m., up to the 8 p.m. address. It also says Kennedy's words as Wallace left came before that request, at an hour Sorensen does not give (279).
- cal.1964-03-12.succession-2: the note now says the time is the lunch's, because the diary gives the burial no hour.
- cal.1964-06-10.cyprus: the note now says the time is the arrival at Ankara at about 2 a.m. on June 11 (Ball, 353), because the Athens talk has no hour.
- cal.1964-08-23.mississippi-2: the time was midnight at the start of Aug. 23. Branch (463) has the vigil begin "At midnight Sunday", which is the night of Aug. 23–24. The time is now 04:00 UTC on Aug. 24, `time_approx` is dropped, and the note's "first day's" sentence is replaced with Branch's words.
- cal.1964-11-03.elections-1964-5: the predawn band was replaced with the "election night" band, which contains the first act (the evening in the ballroom) and the word "after midnight".
- cal.1965-06-30.vietnam-hanoi-2: the reader's change to the note was kept and reworded: the hour is the 1 a.m. attack of July 1, and the June 30 ambush has no hour. The Hanoi history does not say whose clock it uses, Saigon's (UTC+8) or Hanoi's (UTC+7), so the field is now a range covering both. The entry's old `ok:fields-time` tag is removed. The page shows the result on III, 432, not 431: the 1st Airborne Battalion destroyed, and the command post and the two other battalions badly hurt. The note's "cut off" Check can now be settled by a later pass.
- cal.1965-12-05.vietnam-hanoi: the field is now a range for the same reason, with the page's words (IV, 62) in the note. The old tag is removed.
- cal.1965-08-14.civil-disorders-watts: a note sentence was added giving Califano's words.

## Ops added (10)

- cal.1963-12-17.china-leadership-4: the time is 3:30 p.m. (07:30 UTC). The diary sets the acupuncture after the morning's talk and before the afternoon's 4:30 farewell to Luo Ronghuan (II, 335), so it cannot be a.m. The note says so.
- cal.1964-06-21.mississippi: corrected with `kind: correct`. The line read "released after 10 p.m. June 23". *United States v. Price* has Price detain the three on June 21 and release them "in the dark of that night" (383 U.S. at 790), and Dittmer has the release at "about 10:30 that night" (247). The line now reads "released after 10 p.m. June 21", and the "June 23" stays with the station wagon, with a Check for that day. The time is the arrest "shortly after 3:00 P.M." (Dittmer, 247). It is set as a range covering both readings of Mississippi's clock.
- cal.1964-07-02.civil-rights-bill-16: the tag is struck. The time is 1:44 p.m. (17:44 UTC), from the recording that PRDE's catalogue lists as Johnson and Reedy with Moyers joining (Conversation WH6407-02-4129, the Miller Center's page). The call came before the calls with Albert, not after them, so the note now says this. The recording was not heard, and a Check says so.
- cal.1964-06-15.vietnam-4: the tag is struck. The walk was "after dinner", so the field is the evening band, with its basis in the note.
- cal.1965-03-21.alabama-birmingham: the tag is struck. The first box was found at "early Sunday mass" (*Canaan's Edge*, 140), so the field is the early-morning band.
- cal.1964-10-01.students: the leaflet has the police car surrounded from "12:30 PM Thursday", so the time is 19:30 UTC on Oct. 1.
- cal.1965-03-05.civil-rights-organizations: the committee "convened before ten o'clock Friday night" (*Canaan's Edge*, 29), so the time is 10 p.m. Eastern Standard Time, approximate.
- cal.1965-12-20.soviet-union-leadership: Brezhnev left for Zavidovo at 11:00 on Dec. 20 (II, 97), so the time is 08:00 UTC, Moscow time.
- Two `tag` ops remove `ok:fields-time` from 1965-06-30 and 1965-12-05.

## Struck (3)

The `ok:fields-time` tags on 1964-06-15.vietnam-4, 1964-07-02.civil-rights-bill-16 and 1965-03-21.alabama-birmingham. Each now has its field.

## Rows left with no field, and why

- cal.1963-06-25.republican-party: the convention's first day has no hour, and the 5:15 a.m. adjournment is June 28 or 29.
- cal.1963-09-13.baker: Caro (275–77, by the note) gives no hour for the call, and the day of the 1 a.m. return is not given.
- cal.1964-01.elections-1964-9: White (100–01) says only "this Friday afternoon" in late January, so the day is not settled, and a month-dated entry takes no time.
- cal.1965-06.program: the day in June is not found.
- cal.1965-09.vietnam: the Sunday in mid-September is not found.
- cal.1965-10-05.soviet-union-leadership: the workbook gives Oct. 5 no hour (II, 73). The 9:00–11:20 talk is Oct. 7. The line also names the reception of Oct. 4 (17:40), a day before the entry's date.
- cal.1965-12-15.vietnam-hanoi: the first day is not settled. The 3 p.m. is Dec. 18 (IV, 63).
- The 18 held tags, listed above.
- cal.1965-09-19.china keeps its tag. Its act, the reply's delivery, has an hour (3:40 p.m.) in the line of cal.1965-09-19.china-leadership, from the Mao nianpu. That copy could not be read here (the Drive file is only a table of contents). A later pass can cite it and set the time.
- cal.1965-09-20.india-and-china keeps its tag. FRUS docs. 222–23 give no hour for the vote on the resolution.

## Entries that hold more than one event (for a later pass)

- cal.1963-06-25.china-leadership-2 (the flight, the recall, the return)
- cal.1963-06-25.republican-party (a convention of four days)
- cal.1963-07-09.railroads (the statement of July 9, the broadcast of July 10)
- cal.1963-10-10.berlin-and-vienna (the convoy held Oct. 10 and 11, Rusk and Dobrynin, the White House meeting, Kohler and Zorin)
- cal.1963-11-04.berlin-and-vienna (Rusk and Kornienko Nov. 4, Rusk and Dobrynin Nov. 5)
- cal.1963-11-22.press-and-broadcasting (four days of coverage)
- cal.1963-12-17.china-leadership-4 (acupuncture on Dec. 17, 19 and 21)
- cal.1964-02-05.cuba (two dinners on two days)
- cal.1964-06-10.cyprus (Athens June 10, Ankara June 11)
- cal.1964-06-21.mississippi (the arrest and release, the station wagon, Johnson and the parents)
- cal.1964-08-04.vietnam (the reports, the NSC, the leaders, the strikes, the address)
- cal.1964-10-01.students (the arrest, the pact, the founding of the FSM)
- cal.1964-10-27.elections-1964-3 (Johnson's day, three stops)
- cal.1965-03-05.civil-rights-organizations (two nights of meetings and the letter of Mar. 7)
- cal.1965-03-15.voting-rights-selma-2 (the service, the court's order, the march)
- cal.1965-03-21.alabama-birmingham (the bombs found, Moyers's report at night)
- cal.1965-04-28.latin-america (Bennett's request, the address, Bennett's cable)
- cal.1965-05-01.latin-america-dominican-republic (Wheeler's request, Masterson's plans, the Chiefs' choice)
- cal.1965-09-19.china-leadership (Mao's revision, the note delivered)
- cal.1965-09-20.india-and-china (the resolution, the acceptances, the cease-fire, Johnson's statement)
- cal.1965-10-05.soviet-union-leadership (Oct. 4 to 7)
- cal.1965-12-08.vietnam-operations (Dec. 8 and 9)
- cal.1965-12-15.vietnam-hanoi (Dec. 15 to 18)
- cal.1965-12-20.soviet-union-leadership (Zavidovo, Dec. 21, the talks of Dec. 22)

## R0

Nothing in the task brief narrowed what is an entry. Nothing was disregarded.
