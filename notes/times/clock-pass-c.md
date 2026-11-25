# Clock pass C: 1966-1970

The rows of the clock pass dated 1966, 1967, 1968, 1969 and 1970 (135). The patch is `inbox/2026-11-25-clock-times-c.yaml`: 20 entries given fields (10 with a `time`, 10 with a `time_range` from a part of the day the line itself names, `range_basis: record`); `./bib patch-check` shows 0 errors. Nothing is merged and `c` and `n` are untouched.

## The rule I worked by

- A `time` or a range goes on an entry only where the hour or part of the day belongs to the entry's own first or chief act, on the entry's own day. An hour that is a limit ("by 3 p.m.", a deadline), a term (a truce's start), a habit (a daily meeting), another day's (a later day of a multi-day entry, the day before), or a later act of a scene whose first act has no hour is left alone and listed below. R25 gives a multi-day entry its first act's time.
- Zones: Peking and Shanghai Asia/Shanghai; Washington and New York America/New_York, Chicago America/Chicago, Los Angeles and Portland, Ore., America/Los_Angeles; Hattiesburg in January is Central standard time. A `time` carries `time_zone`. `propose.py`'s guess of New York for Peking entries, and of Saigon for the Miami convention entry, was not taken.
- The 10 ranges: the part of the day is the line's own word ("morning", "before dawn", "afternoon", "evening"; "at dawn" read as the early-morning band, 5 to 8) and the note's cite stands for it, so nothing was added to `n`.

## Entries given a `time`

- `cal.1966-03-09.china-leadership-2`: 4 p.m. is the Xingtai leaders' meeting, the first hour given; the 11 p.m. Longyao visit is a later act of the line
- `cal.1966-06-30.china-leadership`: Mao's note at 2 a.m. (the Wengao's 'two o'clock').
- `cal.1966-09-05.china-leadership-3`: Mao reads the draft at 2 a.m.
- `cal.1968-03-05.elections-1968`: 'at midnight' of the night of Mar. 5 read as 00:00 Mar. 6, Pacific standard time, the season's first hour; the entry runs Mar. 5-6. The auditor may take it the other way.
- `cal.1968-03-13.robert-kennedy-campaign-decision-5`: 6:30 p.m. EST is the broadcast; the taping was 'late in the afternoon' (the line), so the act and the hour are the broadcast's.
- `cal.1968-05-27.robert-kennedy`: Salinger's statement at 10:30 a.m., Portland, PDT; `propose.py` had New York. The line's other acts (the spots, the poll) have no hour.
- `cal.1968-06-05.assassination-12`: arraignment 7:40 a.m., Los Angeles, PDT.
- `cal.1968-06-06.assassination-3`: `when` says 2 a.m. and the line's 'twenty-five hours and forty-seven minutes after the shooting' (12:15 a.m. June 5) gives 2:02; set 2:00 PDT with `time_approx`. The death (1:44 a.m.) is the line's other hour.
- `cal.1968-08-27.elections-1968-chicago-6`: 9 p.m. CDT, the police letting the march circle the barn.
- `cal.1968-12-18.white-house`: 4 a.m., the doctor's insistence; the 9:30 a.m. departure is a later act of the line.

## Entries given a `time_range`

- `cal.1966-01-05.steel`: "the White House, morning"; 12:30 to 2:30 is Johnson's sleep, not the act.
- `cal.1966-01-10.mississippi-3`: "the morning after the attack" (Hattiesburg, CST); the 3:45 p.m. death is a later hour of the line.
- `cal.1966-02-07.china-leadership`: Zhou writes "before dawn" (predawn band, 0 to 6); the 3:30 p.m. is the meeting he proposes (the note's Deng nianpu entry says afternoon).
- `cal.1966-09-11.china-leadership`: Mao circles the draft "at dawn"; the 1 a.m. is Tao Zhu's sending.
- `cal.1967-07-22.china-leadership`: "morning, Shanghai"; the 8:20 a.m. is Zhou's call at Wuhan relayed, and the 11 a.m. talk is a second act.
- `cal.1967-07-25.china-leadership`: "afternoon"; the note's pinpoint says 5 p.m. for Mao's note; the 10 p.m. revision is a second act.
- `cal.1967-09-16.china-leadership`: Mao leaves Shanghai "in the morning"; the noon talk on the train is a second act.
- `cal.1967-12-04.vietnam-support`: "evening"; home at 9:30 is the line's last act.
- `cal.1968-04-30.white-house-2`: "evening"; Alsop moves to go at 10:30 is the end.
- `cal.1968-08-25.elections-1968-chicago-11`: "Sunday afternoon to after midnight", Washington, by Clifford's account; the range is the afternoon only.

## Entries with several events and several hours

These got a field for the first or chief act and keep their other hours in the line: the Xingtai and Longyao visits (Mar. 9, 1966), the hospital morning and the death (Jan. 10, 1966), the dawn circling and the 1 a.m. sending (Sept. 11, 1966), the Wuhan entries of July 22 and 25, 1967, the Mao train entry of Sept. 16, 1967, the Kennedy broadcast of Mar. 13, 1968, the Johnson illness of Dec. 18, 1968. The unlisted ones below hold several events (the Soviet and Chinese multi-day travel diaries, the Middle East entries of 1967, the invasion of Czechoslovakia entry of Aug. 20-21, 1968) and I split nothing.

## Rows left without fields

One line each; none was settled, for the reason given. The midnight rows (marked) may be settled by the Chinese or English source's own wording, which I did not read.

- `cal.1966-01-02.steel` (2:15 p.m.): two acts (Johnson's telegram, no hour; the 2:15 p.m. briefing); the briefing's place is not given (Washington or the Ranch, an hour apart).
- `cal.1966-01-31.vietnam` (10 a.m.): several acts; the 10 a.m. broadcast (PPP 114: White House Theater, 10 a.m.) would put this entry after cal.1966-01-31.vietnam-air-war, which follows it at 14:20Z: check [day-order] fails; the auditor may reorder the `follows`.
- `cal.1966-02-16.laos` (midnight): 'midnight' with no way to tell the start or the end of the day from the line; the Chinese and English sources (not read) may say ('about midnight Feb. 16').
- `cal.1966-02.vietnam-3` (7 a.m.): month-dated; the 7 a.m. call has no day, so no UTC instant.
- `cal.1966-03-10.china-leadership-3` (5 p.m.): the 5 p.m. hour is the departure for Peking, the closing act; the speech has none.
- `cal.1966-03-12.china-leadership-2` (noon; 12:30): the 12:30 hour is the departure for Tianjin, a second act; the letter has none (it was written before noon).
- `cal.1966-03-26.china` (1 a.m.): the 1 a.m. is the attack of Mar. 24 the note reports; the note has no hour.
- `cal.1966-03-29.soviet-union-leadership-2` (9:15; 1:20): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (Apr. 7, Apr. 8).
- `cal.1966-04-14.vietnam-hanoi-2` (6:27 a.m.): the 6:27 a.m. is the air strike the cable reports; the cable has no hour (the strike's zone would be Asia/Bangkok).
- `cal.1966-05-02.alabama` (3 p.m.): 'by 3 p.m.' is a limit on the posting, not an hour; Hayneville's clock in May 1966 (Alabama daylight time was a local choice) is in doubt.
- `cal.1966-05-20.soviet-union-leadership` (6:20 p.m.): the hour is another day's, not the entry's act (6:20 p.m. May 23, the return).
- `cal.1966-05.china-leadership-12` (noon): month-dated ('before the 11th'); the noon deadline has no day.
- `cal.1966-05.china-leadership-41` (4 p.m.): the hour is another day's, not the entry's act (4 p.m. on the 24th, the meeting the poster cites).
- `cal.1966-06-08.africa-2` (4 a.m.): 4 a.m. is when the party ended, past midnight; the party itself has no hour.
- `cal.1966-06-14.state-and-city-finance-nyc` (4:10 a.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (4:10 a.m., June 16).
- `cal.1966-06-30.vietnam-hanoi-3` (7 p.m.): 7 p.m. is when firing stopped, the end of the ambush; the note's own Check says the history gives no start.
- `cal.1966-07-02.states-and-cities-omaha` (12:30 a.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (after 12:30 a.m. July 5).
- `cal.1966-07-13.vietnam-support` (10 p.m.): the 10 p.m. 'about' is the coming in to the White House after the Sequoia dinner, a later act; the dinner has no hour.
- `cal.1966-07-16.china-leadership-2` (3 p.m.): 3 p.m. is a daily meeting's habitual hour, not the day's act.
- `cal.1966-07-20.war-opposition` (6 p.m.): 6 p.m. is a permit's start for a picket, a plan, not the act.
- `cal.1966-07-27.china-leadership-5` (midnight): 'midnight' with no way to tell the start or the end of the day from the line; the Chinese and English sources (not read) may say (Zhou with Faruque).
- `cal.1966-07-30.open-housing` (midnight): 'before midnight' is the end of the July 29 vigil, another day's act.
- `cal.1966-08-09.mayors` (noon): two acts (Daley's appeal, no hour; the Commission's noon meeting); Chicago was on daylight time, so noon would be 17:00Z; left for the auditor to say which act the entry is.
- `cal.1966-08-29.china-leadership-7` (1:50): false hit: '1:50,000' is a map scale.
- `cal.1966-09-09.king` (6:51 p.m.): 6:51 p.m. is the FBI's wiretap log of a call between Memphis and New York; whose clock (Memphis, whose daylight time that month is in doubt, or New York) is not in the line.
- `cal.1966-09-15.china-leadership-7` (midnight): midnight is when Tao Zhu sent the editorial; Mao's reply has no hour.
- `cal.1966-09-19.soviet-union-leadership` (6:56 p.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (6:56 p.m. Sept. 22).
- `cal.1966-09-27.states-and-cities-san-francisco` (11:39 p.m.): the 11:39 p.m. Guard request is a later act of the day; the shooting has no hour.
- `cal.1966-09-27.china-leadership-5` (midnight): 'that midnight' is the cremation, after the death.
- `cal.1966-10-01.china-leadership-5` (midnight): 'midnight' with no way to tell the start or the end of the day from the line; the Chinese and English sources (not read) may say (Zhou with Chen Boda).
- `cal.1966-10-26.china-leadership-3` (9 a.m.): 9 a.m. on the 27th is the launch time Zhou approves, another day's act.
- `cal.1966-10-30.robert-kennedy` (2:30 a.m.): 2:30 a.m. is the end of the talk; the talk began about 10:30 p.m. (note, Schlesinger's journal) but that is not in the line.
- `cal.1966-11-15.china-leadership` (midnight): midnight is Mao's reply of Nov. 16, another day.
- `cal.1966-11-24.china-leadership` (1 a.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (1 a.m. Nov. 28).
- `cal.1966-11.robert-kennedy-2` (2:30 a.m.): month-dated; 'about 2:30 a.m.' has no day.
- `cal.1966-12-23.china-leadership-3` (3 a.m.): 3 a.m. is when the mayor signed, the end of the meeting.
- `cal.1967-01-02.vietnam-air-war-2` (7 a.m.): 7 a.m. is the stand-down's end, the second act; the air battle has no hour (a Saigon clock).
- `cal.1967-01-28.soviet-union-leadership` (6:22 p.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (6:22 p.m. Jan. 31).
- `cal.1967-02-02.china-leadership-3` (10 p.m.; 3:30 p.m.): 10 p.m. and 3:30 p.m. are the hours of meetings Zhou proposes to hold regularly, not the act.
- `cal.1967-02-03.soviet-union-leadership` (6:35 p.m.): the hour is another day's, not the entry's act (6:35 p.m. Feb. 2, the train's departure).
- `cal.1967-02-09.vietnam` (8 a.m.; noon): 8 a.m. is Feb. 8's cease-fire start and noon a report's cut-off, neither the entry's act.
- `cal.1967-02-25.china-leadership-7` (midnight): midnight of Dec. 22 is Peng's seizure, two months earlier.
- `cal.1967-02.china-leadership-22` (10 p.m.): month-dated ('after the 15th'); 10 p.m. is Feb. 16's oral report, another day's act.
- `cal.1967-03-10.vietnam-operations` (midnight; 12:01 a.m.): midnight and 12:01 a.m. are the dates of Phases I and II of Junction City (Mar. 17-18), not the night attack of Mar. 10, which has no hour.
- `cal.1967-03-12.india-and-china` (10:45 p.m.): two acts (the MPRS vote, no hour; Suharto's swearing-in at 10:45 p.m.); FRUS docs. 232-33 not opened for the hour.
- `cal.1967-03-19.vietnam-operations` (10 p.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (10 p.m. Mar. 21).
- `cal.1967-03-31.vietnam-operations` (4:55 a.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (4:55 a.m. Apr. 1).
- `cal.1967-04-12.railroads` (12:01 a.m.): false hit: 12:01 a.m. May 3 is the no-strike period's end; the signing is at Punta del Este with no hour.
- `cal.1967-04-24.china` (24:00): 24:00 on Apr. 30 is a deadline for the diplomats to leave.
- `cal.1967-05-09.soviet-union-leadership` (2:55 p.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (2:55 p.m. May 13).
- `cal.1967-05-25.middle-east` (1:30 p.m.; 7:15; 8:40 p.m.): all three hours are May 26's (Johnson 1:30 p.m.; Eban 7:15-8:40 p.m.); the entry's first day (Eban with Rusk, May 25) has none.
- `cal.1967-06-05.middle-east` (7:57 a.m.): several acts and hours: the Israeli strike ('in the morning', Cairo or Israel clock), the 7:57 a.m. hot-line message (Washington; FRUS docs. 157, 159 and the Miller Center tape agree on 7:57), McCloskey's statement.
- `cal.1967-06-06.middle-east` (7:40 a.m.): 7:40 a.m. is Radio Cairo's broadcast, a later act; the Council's vote and the President's 8 p.m. statement (PPP 598) are other acts of the line.
- `cal.1967-06-09.middle-east` (8:48 a.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (8:48 a.m. June 10, the hot line).
- `cal.1967-06-17.china-leadership-9` (8:20 a.m.): 8:20 a.m. is the explosion; Ye's telephone call came after, with no hour.
- `cal.1967-06-24.china-leadership-9` (10:30): hours are a habitual routine over twelve days.
- `cal.1967-07-01.robert-kennedy` (noon): '110 degrees at noon' is the heat, not an hour of the climb.
- `cal.1967-07-05.vietnam-operations` (7:45 a.m.; 1:45 p.m.): 7:45 a.m. to 1:45 p.m. is the enemy artillery's span, the second act; the first act has no hour (a Vietnam clock).
- `cal.1967-07-05.vietnam-hanoi-2` (11 p.m.): about 11 p.m. is Thanh's return, the end of the evening; the walk and dinner have no hour.
- `cal.1967-08.china-leadership-35` (midnight): month-dated ('early August'); 'after midnight' has no day.
- `cal.1967-09-15.china-leadership` (noon): noon is the deadline Zhou sets for leaving the compound.
- `cal.1967-10-05.china` (3 a.m.): 3 a.m. on Oct. 1 is the attack, another day.
- `cal.1967-10-08.china-leadership-2` (midnight): 'midnight' with no way to tell the start or the end of the day from the line; the Chinese and English sources (not read) may say (the General Office's notice; the book gives 'midnight Oct. 8').
- `cal.1967-10-26.latin-america` (12:01 a.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (12:01 a.m. Oct. 28, the boundary change).
- `cal.1967-11-29.defense-clifford` (2 a.m.): 'nearly 2 a.m.' is the end of the evening with the Connallys, which began 'late evening'; no band fits 'late evening' between 'evening' (7-10) and 'night' (10-12).
- `cal.1968-01-24.china-leadership` (midnight): midnight is on the 26th, another day.
- `cal.1968-01-27.vietnam-tet-2` (1 a.m.; 1 a.m.; 6 p.m.; 6 a.m.): all the hours are the terms of the truces (1 a.m. Jan. 27 to 1 a.m. Feb. 3; 6 p.m. Jan. 29 to 6 a.m. Jan. 31), not the hour of the declarations.
- `cal.1968-01-29.vietnam-tet-4` (5 p.m.): 5 p.m. is the end of the day's fighting; the note's Check queries the day.
- `cal.1968-02-05.vietnam-tet-3` (2:30 a.m.): about 2:30 a.m. Jan. 31 is another day's offensive.
- `cal.1968-02-07.jobs-and-wages-nyc` (7 a.m.): 7 a.m. Thursday is the ultimatum's deadline.
- `cal.1968-02-18.vietnam-tet-3` (9 p.m.): 9 p.m. is Feb. 19's withdrawal, another day.
- `cal.1968-02-29.vietnam-tet` (6 p.m.; midnight): 6 p.m. and midnight bound the MACV count's period.
- `cal.1968-03-16.elections-1968-4` (6:33 p.m.; 2:06 p.m.): the 6 and 6:33 p.m. messages run between Washington (Tom Johnson) and the Ranch (Jim Jones); whose clock is not in the line (an hour apart); the 2:06 p.m. wire is Mar. 17's.
- `cal.1968-03-19.king-poor-peoples` (midnight): 'after midnight' is the last stop, Hattiesburg, of Mar. 19-20; the entry's first act has no hour.
- `cal.1968-03-25.vietnam` (10:30 a.m.; 12:15 p.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (10:30 a.m. to 12:15 p.m., Mar. 26).
- `cal.1968-04-04.robert-kennedy-campaign` (3 a.m.): about 3 a.m. is Apr. 5's, a later act.
- `cal.1968-04.vietnam-paris-2` (8:30; 8:29): month-dated; 8:30 and 8:29 a.m. have no day.
- `cal.1968-05-06.robert-kennedy-campaign-primaries` (5 p.m.): 5 p.m. is the hour the speech was scheduled; the motorcade reached Whiting after 10.
- `cal.1968-06-23.china-leadership-2` (3 p.m.): 'by 3 p.m. the next day' is June 24's.
- `cal.1968-08-05.elections-1968-miami-12` (11:27 p.m.): 11:27 p.m. is the adjournment, the end of the session; the keynote has no hour.
- `cal.1968-08-18.elections-1968-chicago` (11 p.m.): 11 p.m. is the park's nightly curfew, a habit.
- `cal.1968-08-20.soviet-union` (8:15 p.m.; 10:15 p.m.; 11:22 p.m.): several acts and hours: the invasion (the night of Aug. 20-21), Dobrynin at 8:15 p.m. EDT and the NSC at 10:15 p.m. (FRUS docs. 80, 81 agree), Johnson's statement 11:22 p.m. Aug. 21; the entry's date is the invasion's, which has no hour; `follows` set on two entries.
- `cal.1968-08-24.elections-1968-chicago` (5 p.m.; 11 p.m.): two later hours (by 5 p.m., about 11 p.m. the clearing); the first act (the command post's opening) has none.
- `cal.1968-08-26.elections-1968-chicago-25` (10:30): 'about 10:30' has no a.m. or p.m. in the line or the note's pinpoint; Longley, 217, not read.
- `cal.1968-08-27.elections-1968-chicago-4` (11 p.m.; 4 p.m.): two later hours (4 p.m. delegation; vigil from 11 p.m.); the committee's forming has none.
- `cal.1968-08-29.elections-1968-chicago-5` (9:30): '79 arrested by 9:30' is a limit on the arrests; the march has no hour.
- `cal.1968-09-27.elections-1968` (midnight): 'after midnight' is a later act, in the night of Sept. 27-28.
- `cal.1968-09-28.elections-1968-2` (2 a.m.): 2 a.m. is the staff talk after the auditorium event, past the entry's day.
- `cal.1968-09-29.elections-1968-4` (2 p.m.; 2 a.m.): 2 p.m. is a list of those at the draft's meeting, which Solberg and O'Brien's book both disown (the note); the night session's end is 2 a.m., 4:30 a.m., 5:15 a.m. or 'three or four' by different accounts (the note's Checks).
- `cal.1968-09.elections-1968-7` (midnight): month-dated; 'midnight, Sept. 20' is the signature deadline.
- `cal.1968-09.elections-1968-16` (2:30 a.m.): month-dated ('after the 9th'); 2:30 a.m. has no day.
- `cal.1968-10-25.congress` (10:30 p.m.): the 10:30 p.m. call has no settled day (the note's Check).
- `cal.1968-10-30.vietnam-paris` (1:30 a.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (1:30 a.m. Oct. 31, Paris).
- `cal.1968-10-31.vietnam-hanoi` (8 a.m.): 7 or 8 a.m. Nov. 1 is the expected end of the bombing, not the cable's hour.
- `cal.1968-11-05.elections-1968-nixon-3` (6:15 p.m.; 7:05): 6:15 p.m. (Newark) and 7:05 (the Waldorf) are the flight's end; the first acts (Nixon thanking his writers) have no hour.
- `cal.1968-11-05.elections-1968-humphrey` (midnight): 'shortly before midnight' is the entry's last act, after the flight and the vote.
- `cal.1968-12-11.transition-and-staff` (5:35; 7:25 p.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (5:35 to 7:25 p.m. Dec. 12); the television presentation of Dec. 11 has no hour in the line.
- `cal.1968-12-16.soviet-union-leadership` (8 p.m.; 9 a.m.): the 5 to 8 p.m. talks have no day among Dec. 16-18, and 9 a.m. is Dec. 18's.
- `cal.1969-01-19.transition-and-staff` (11 p.m.): 'shortly before 11 p.m.' is bedtime, the last act of a day of many acts.
- `cal.1969-01.transition-and-staff-4` (5 p.m.): month-dated ('before the inauguration'; the note's Check: the day); the 5 p.m. call has no day.
- `cal.1969-03-07.china` (noon): noon is the Moscow incident the note reports; the note has no hour.
- `cal.1969-04-11.china-leadership-2` (2 a.m.): 2 a.m. is when Peng wept after a day of reading, the end of the day.
- `cal.1969-04-12.china-leadership-3` (2 a.m.): after 2 a.m. is the night's end, after a day of reading.
- `cal.1969-04-15.china-leadership-3` (2 a.m.): after 2 a.m. is the night's end, after a day of reading.
- `cal.1969-04-17.china-leadership` (2 a.m.): after 2 a.m. is the night's end, after a day's writing.
- `cal.1969-04-19.china-leadership-2` (2 a.m.): 2 a.m. is the night's end, after a day of reading.
- `cal.1969-04-22.soviet-union-leadership` (9 a.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (9 a.m. Apr. 23; the session at 10; Apr. 26, 2 to 4).
- `cal.1969-04-24.china-leadership-3` (3:30 p.m.): 3:30 and 4 p.m. are the meeting hours Mao approves; his reply has no hour.
- `cal.1969-04-28.china-leadership-3` (7 a.m.; 4 p.m.; 4 p.m.): 7 a.m. is the report's, 4 p.m. the meeting's Mao approves; his reply has no hour (after 7 a.m.).
- `cal.1969-04.china-leadership-21` (8 p.m.; 6 a.m.): month-dated ('during the Congress'; the note's Check: the day); 8 p.m. to 6 a.m. has no day.
- `cal.1969-06-03.soviet-union-leadership` (10 p.m.): the hour is a later day's of a multi-day entry; the entry's first day has none (R25: the first act's time) (10 to 1 and 8 to 10 p.m. June 4).
- `cal.1969-06-06.china` (noon): noon on May 28 is the end of a shooting period the note recounts.
- `cal.1969-09-03.vietnam-hanoi` (9:47 a.m.): 9:47 a.m. is the hour of Hồ's death as the call announces it (he died Sept. 2); the call has no hour.
- `cal.1969-10-03.china-leadership-9` (10 a.m.; 4 p.m.; 10 p.m.): the hours are a log of sitting still in two-hour spans over the day, not an act.
- `cal.1970-01-05.china-leadership` (1 a.m.): 1 a.m. is the earthquake's; Zhou's hearing the report has no hour.

## For the auditor

- `cal.1966-01-31.vietnam` and `cal.1966-01-31.vietnam-air-war`: setting the 10 a.m. broadcast on the first fails [day-order], because the second `follows` the first and is timed 14:20Z (9:20 a.m. EST). The `follows` may be wrong or the 14:20Z; I left both.
- `cal.1966-09-09.king`, `cal.1968-03-16.elections-1968-4`, `cal.1966-01-02.steel`: whose clock the hour is in; a call or a wire between two places.
- No `place` was set or changed in this pass.
- Southern places in summer (Hayneville in May 1966, Memphis in Sept. 1966, Omaha in July 1966) have daylight time in doubt; none was timed.
- `propose.py` was run once for its proposals; it rewrote `notes/times-proposals.yaml`, which I restored with `git checkout`.
