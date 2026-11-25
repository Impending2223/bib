# Audit of clock pass A, entries of 1960–62

The patch is `inbox/2026-11-25-clock-times-a.yaml`. It now holds 43 ops: 40 edits that set time fields, 2 `check` ops and 1 `follows` op. `./bib patch-check` shows 0 errors and 0 warnings.

## How the audit was done

I read each of the 98 rows with `./bib show`, its line and its note. I read the pages from the owner's copies on Drive: Yang Shangkun's diary (both volumes, as page images; printed page plus 6 in vol. I, plus 5 in vol. II), Ritchie's *Minutes of the Senate Democratic Conference*, Salinger's *With Kennedy*, Goodwin's *Remembering America*, *Văn kiện Đảng toàn tập*, vol. 21, the *Zhou Enlai nianpu*, vol. II, and the *Mao Zedong nianpu* (the ebook). I read the Commodore Hotel remarks on APP. All the copies are deleted.

I held each field to one rule, taken from R25 and the owner's ruling of Nov. 18, 2026. The field takes the time of the entry's first act. An entry of several days takes its first day's time, or none. Where the record gives only the end of the first act, the end is the time, and the note says so. Where the record gives both ends of the act, the field is a range between them. An hour that is a deadline, a plan, a term of a decree, or another day's act sets no field.

## Ops checked and kept as the reader wrote them

- cal.1960-07-09.elections-1960-3: evening range of July 9, Los Angeles; the note's sentence on the first day is right.
- cal.1960-10-23.china-leadership: evening range; the Mao nianpu says 晚上.
- cal.1962-07-28.china-leadership-6: morning range; the diary says 上午 for the first swim.
- cal.1962-07-28.china-leadership-5: 12:30 a.m. July 29; the diary has the train after the evening's opera.
- cal.1962-08-02.china-leadership-10 and cal.1962-08-03.china-leadership-4: 11:30 a.m.; the diary puts it in the morning.
- cal.1962-08-25.china-leadership-5: morning range; the diary says 上午.
- cal.1962-09-15.china-leadership-7: 12:30 a.m. Sept. 16; the diary puts the talk after the evening.
- cal.1962-10-22.missile-crisis-diplomacy-2: about 5 p.m. London, BST.

## Ops kept, with a sentence added to the note

- cal.1960-02-01.china-leadership-3: noon is the arrival at Haikou (diary I, 475); the note now says the hour of leaving Jiaji is not given.
- cal.1960-02-15.congress and cal.1960-02-18.congress: 12:11 p.m. and 10:54 a.m. are the adjournments; the minutes give no opening hour (I read pp. 557–75). The note now says so.
- cal.1961-11-19.elections-1964: near midnight is Rockefeller's departure; the note now says the hour the news came is not given.
- cal.1962-07-23.china-leadership-5: 7 p.m. is Yang's visit (diary II, 197, 晚间7时); the note now says the operation's hour is not given.
- cal.1962-09-25.white-house-4: 2:35 a.m. Sept. 26 is his leaving; the note now says so, and the entry now follows the theater entry, cal.1962-09-25.white-house-3.
- cal.1962-10-22.missile-crisis-quarantine: morning range; Salinger's words are "one of my first calls that day" (261), now in the note.

## Ops changed

- cal.1960-02-03.china-leadership-2: the reader set 6 p.m., the arrival at Xinhui, a later act. The diary puts the arrival at Yangjiang at midday (中午). Now a midday range, with the words in the note.
- cal.1960-07-04.china-leadership-7: the reader set 3:30 a.m., the end of the talk. The diary bounds the talk by the train's departure, 9:30 p.m., and the arrival, 3:30 a.m. Now a range between them.
- cal.1960-10-25.china-leadership: the reader set a predawn range for "after midnight". The Mao nianpu gives 晨零时十分. Now 12:10 a.m. Oct. 25.
- cal.1961-10-20.china-leadership-4: the reader set noon, approximate. The diary says 中午, a part of the day. Now a midday range, Moscow.
- cal.1962-02-01.china-leadership-3: the reader set 7 p.m., the end. The diary gives 3 to 7 p.m. for the afternoon's meetings, this one after the Mianyang group. Now a range of 3 to 7 p.m.
- cal.1962-10-31.europe-and-the-alliance-3: the reader set 6:30 p.m., a later act. The line's first act is the Cabinet sitting all day. Now a daytime range, Bonn.

## Ops struck

- cal.1960-11-05.elections-1960-kennedy-9: the "midnight brunch" in the remarks is a joke about a fundraiser "next week", not the hour of the remarks (APP). No field. A `check` op says so in the note.
- cal.1961-05-25.korea-leadership, cal.1961-05-27.korea-leadership-2, cal.1961-05-27.korea-leadership-5: "from noon" is when each decree takes effect, not when it was issued. The reader left the proclamations of May 16 and 17 unset for the same reason, so the four are now treated alike.

## Ops added (rows the reader left unset)

- cal.1960-02-04.china-leadership-2: early morning range; the diary says 晨 for the climb of Mashan (I, 476).
- cal.1960-03-07.china-leadership-5: range from 12:30 a.m. Mar. 8, when the audience ended, to 2 a.m. (I, 486).
- cal.1960-05-14.china-leadership-8: range from 5:30 p.m., when the audience ended, to 7:30 p.m. (I, 508).
- cal.1960-07-13.elections-1960-los-angeles-2: 3 p.m. Pacific, the session's opening, which is the line's first act.
- cal.1960-09-11.china-leadership-6: range from 4:30 p.m., the return from the Diaoyutai, to 5:30 p.m. (I, 543).
- cal.1960-09-22.farm-4: Goodwin names no place. Kennedy spent that night at Sioux City, Iowa, by the day's other entries. Iowa kept daylight time by local option in 1960, so the field is the range of the two readings, an hour wide. The entry now has `place: sioux-city`.
- cal.1960-11-11.vietnam-hanoi: the cable gives the state of things "by 8 p.m. this evening" (XXI, 1013). Range from 8 p.m. to midnight, Hanoi; the earlier end allows for Saigon's clock.
- cal.1961-04-08.china-leadership-4: range from the evening, after the opera, to 1 a.m. Apr. 9 (I, 673).
- cal.1961-05-10.china-leadership-2: the Zhou nianpu has 午夜 after the evening's plays. The time is midnight after May 10, approximate, the first day's.
- cal.1961-09-17.china-leadership-4: 1:10 p.m. The diary sets it after the morning's meeting and before Yang's own departure at 4 p.m. (II, 69).
- cal.1961-09-29.soviet-union-2: afternoon range. The line says "afternoon"; Salinger takes the call after an afternoon round of golf (197–98).
- cal.1962-01-16.china-leadership-8: range from 12:30 a.m. Jan. 17, when the report meeting ended, to 2:30 a.m., when Yang got home (II, 113). The entry now has `place: peking`.
- cal.1962-01-29.soviet-union: morning range, Paris. Salinger has the talks begin "the next morning" (211).
- cal.1962-01-29.china-leadership-5: range from 10 p.m. to 1:45 a.m. Jan. 30 (II, 118).
- cal.1962-02-02.china-leadership-3: range from the evening to 1:30 a.m. Feb. 3 (II, 120).
- cal.1962-07-05.china-leadership-3: range from midnight, the end of the talk before it, to 3 a.m. July 6 (II, 192).
- cal.1962-08-05.china-leadership: midday range. The Mao nianpu gives 中午 for the talk, which came before the approval of the list.
- cal.1962-12-24.china-leadership: 7:30 a.m. The Mao nianpu gives 晨七时半, which settles the a.m. or p.m. that the *Wengao* leaves open.
- cal.1961-06-03.berlin-and-vienna-5: no hour of its own. A `follows` op ties it to the first day's talks, cal.1961-06-03.berlin-and-vienna. Salinger has those talks end at 6:45 p.m. (179).
- cal.1962-10-21.missile-crisis-13: no field. A `check` op notes that Salinger places "the meeting" in the morning (259), while the NSC sat 2:30 to 4:50 p.m.

## The eight rows from Yang Shangkun's diary

All eight are settled from the pages. Each one's field is listed above: 1960-03-07, 1960-05-14, 1960-09-11, 1961-04-08, 1961-09-17, 1962-01-29, 1962-02-02 and 1962-07-05.

## Rows left with no field, and why

- cal.1960-01-06.china-leadership-3: the illness ran through the day; the sleep from 5 to 7 p.m. is a later part.
- cal.1960.vietnam-hanoi-5: dated to the year; the broadcasts are nightly.
- cal.1960-02-17.latin-america-2: 6:15 is the coming Sunday's telecast.
- cal.1960-02-29.voting-rights: 5 p.m. is the adjournment the defeated motion would have set.
- cal.1960-02-29.voting-rights-2: which night it was is not known.
- cal.1960-03-19.laos: 5 p.m. Mar. 20 is a filing deadline.
- cal.1960-03-24.china-leadership-6: 11 a.m. is a deadline; the diary gives no hour for the call (I, 491).
- cal.1960-04.china-leadership-18: dated to the month; the day of the noon death is not known.
- cal.1960-05-19.japan-and-korea: two days; the first day's acts have no hour.
- cal.1960-06-28.china-leadership-5: midnight is the earlier delivery of the draft.
- cal.1960-06-29.china-leadership: the act is the printing; the revision after 3 a.m. at Bengbu is an earlier act.
- cal.1960-06.elections-1960-12: dated to the month.
- cal.1960-07-04.china-leadership, cal.1960-07-23.china-leadership-2, cal.1960-07-28.china-leadership-2: each midnight is a past limit named in Zhou's letter.
- cal.1960-07-08.elections-1960-2: "Monday noon" is Robert Kennedy's prediction.
- cal.1960-08-23.elections-1960-kennedy: 2 and 6 p.m. are the Senate's votes, named in the telegram.
- cal.1960-08.china-leadership: 10 a.m. Aug. 4 is the planned reading.
- cal.1960-09-04.elections-1960-kennedy-2: "Saturday noon" is an itinerary.
- cal.1960-09-14.vietnam-hanoi-4: three days; the first day has no hour.
- cal.1960-10-15.elections-1960-kennedy: 2:30 a.m. is the earlier arrival; the breakfast has no hour.
- cal.1960-10-18.elections-1960-3: 8:30 is when the draft was begun; the speech has no hour.
- cal.1960-10.king: dated to the month.
- cal.1960-11-05.elections-1960-kennedy-8: 2 a.m. at Waterbury is still to come; the rally has no hour.
- cal.1960-11-07.elections-1960-5: four acts; the first three have no hour, and 11 p.m. is the last.
- cal.1960-11-17.china-leadership: the first act, the Politburo, has no hour; 10 p.m. is Zhou's draft.
- cal.1960-11.cuba-bay-of-pigs: dated to the month.
- cal.1960-12-31.soviet-union: the call has no hour; 2 a.m. is the later delivery.
- cal.1961-02-23.china-leadership: three days; the first day has no hour.
- cal.1961-02.peace-corps: dated to the month.
- cal.1961-03.civil-rights-the-executive: dated to the month.
- cal.1961-04-11.soviet-union-leadership: 9:07 is the next day's launch.
- cal.1961-04-11.china-leadership-5: 2 p.m. on the 14th is a plan.
- cal.1961-04-17.cuba-6: the first act has no hour; 3 p.m. at San Blas is later.
- cal.1961-05-11.china-leadership-7: the act is the report; the patrol hours are a routine.
- cal.1961-05-15.freedom-rides: the calls have no hour; the flight near midnight is later.
- cal.1961-05-16.korea-leadership, cal.1961-05-17.korea-leadership-3: the hours are the terms of the proclamations.
- cal.1961-06-03.berlin-and-vienna-5: no hour of its own; `follows` added.
- cal.1961-06-06.china-leadership-11: the day is in doubt; noon is the habit of the work.
- cal.1961-07-29.berlin-and-vienna: two days; the first day has no hour.
- cal.1961-08-10.berlin-and-vienna: midnight Aug. 12 is the planned hour.
- cal.1961-10-30.vietnam-hanoi-2: two days; the first day has no hour.
- cal.1962-07.robert-kennedy: dated to the month.
- cal.1962-10-21.missile-crisis-13: 7 p.m. and 5 p.m. are plans; the hour of the meeting is in doubt (`check` added).
- cal.1962-10-22.soviet-union-leadership: the session's start is not given; midnight falls inside it.
- cal.1962-10-23.missile-crisis-8: the act is the arrival; whose clock the 4 p.m. flyover is on is not said.
- cal.1962-10-25.missile-crisis-quarantine: the hours are those of the Oct. 24 buzzing.
- cal.1962-10-26.missile-crisis-5: the clock is not given; Moscow time and local time are seven hours apart, too far for a range of two readings.
- cal.1962-10-27.missile-crisis-excomm: the note says its sources do not bear out the midnight.
- cal.1962-10-30.missile-crisis-5: two days; the first day has no hour.
- cal.1962-11-14.cuba: 8 p.m. Thursday is a plan.
- cal.1962-11-24.china-leadership-3: 0:00 Nov. 22 is the hour of the cease-fire.
- cal.1962-12-24.cuba-2: the day is in doubt, and the first act has no hour.
- cal.1960-11-05.elections-1960-kennedy-9 and the three Korean decrees: struck, above.
