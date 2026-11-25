# Audit of clock pass C: 1966-1970

The audit of `inbox/2026-11-25-clock-times-c.yaml` and of the reader's note `notes/times/clock-pass-c.md`, Nov. 25, 2026 (Opus). The patch now holds 38 `edit` ops. `./bib patch-check` shows 0 errors and 0 warnings. Nothing is merged. No `c` is changed. A note is changed only to add the words that ground a field, or a "Check:".

## How I worked

- I read each of the 135 entries, its line and its note, against R25 and R25a as the brief states them.
- I kept the reader's rule where the brief supports it: a field goes on the entry's first act, on the entry's own day; an hour that is a limit, a deadline, a habit, another day's act, or a later act after a first act with no hour sets no field.
- I also set a range where the line or note names a part of the day for the first act ("night", "afternoon", "late evening"). The reader had looked only at clock times.
- An entry of several days that took a field now says in its note "The time is the first day's." (R25).
- Sources read: the Public Papers' text (`sources/ppp-text`), the Miller Center catalogue (`daybook/recordings/millercenter.yaml`), FRUS's text (`sources/frus-text`), the daylight-time register (`sources/daylight-time.yaml`), and from the owner's Drive or open copies: *Zhou Enlai nianpu*, III, 11, 19–20, 42, 71 (page images); Longley, 217; *Rights in Conflict*, 189, 341–43; Schlesinger, *Journals*, 253; Anthony and Sexton, 188 (archive.org text). Every copy was deleted after reading.

## Ops checked and kept as written (16)

- `cal.1966-06-30.china-leadership`: 2 a.m. (二时), Peking.
- `cal.1966-09-05.china-leadership-3`: 2 a.m. (二时), Peking.
- `cal.1968-03-05.elections-1968`: midnight of Mar. 5–6, Pacific time, is the canvassing's first hour. I kept it and added the sentence the brief asks for on an entry of two days.
- `cal.1968-03-13.robert-kennedy-campaign-decision-5`: 6:30 p.m. EST. The broadcast is the act the entry's `when` names ("evening").
- `cal.1968-05-27.robert-kennedy`: 10:30 a.m. PDT, Portland. Salinger's statement is the chief act. The spots and the wire have no hour.
- `cal.1968-06-05.assassination-12`: 7:40 a.m. PDT. The `when` names the arraignment.
- `cal.1968-06-06.assassination-3`: 2 a.m. PDT, approximate.
- `cal.1968-12-18.white-house`: 4 a.m. EST. The waking "in the night" may belong to Dec. 17, so the doctor's 4 a.m. is the first hour on the day.
- `cal.1966-01-05.steel`: morning, EST.
- `cal.1966-01-10.mississippi-3`: morning, CST.
- `cal.1966-02-07.china-leadership`: predawn, Peking. The page reads 凌晨, which I added to the note.
- `cal.1966-09-11.china-leadership`: early morning ("at dawn"), Peking. The Mao nianpu was not found on Drive, so I could not check whether it reads 凌晨, which would make it predawn.
- `cal.1967-07-22.china-leadership`: morning, Shanghai.
- `cal.1967-09-16.china-leadership`: morning, Shanghai.
- `cal.1968-04-30.white-house-2`: evening, EST.
- `cal.1968-08-25.elections-1968-chicago-11`: afternoon, EDT.

## Ops changed (4)

- `cal.1966-03-09.china-leadership-2`: the 4 p.m. time became an afternoon range. The nianpu (III, 19) has Zhou leave 下午 and reach Shijiazhuang before the 4 p.m. talk, so the first act is the afternoon departure. The page's words are added to the note.
- `cal.1967-07-25.china-leadership`: the afternoon range became a time of 5 p.m., Peking. The Wengao, cited in the note, dates Mao's note on the draft reply 5 p.m. An hour beats a band.
- `cal.1967-12-04.vietnam-support`: the evening range became a time of 7:38 p.m. EST. The Public Papers' note (1967 Pub. Papers 1094, note at 1099) gives the hour and the room. The item is now cited first, and "To check: the Public Papers" is gone.
- `cal.1968-08-27.elections-1968-chicago-6`: 9 p.m. became 8:10 p.m. CDT, approximate. *Rights in Conflict*, 189, has the march leave the park by the police broadcast of 8:10 p.m. The circling at 9 p.m. is a later act. The note says so.

## Ops added (18)

- `cal.1966-01-31.vietnam`: 10 a.m. EST, the broadcast. The Public Papers print "Broadcast from the White House Theater at 10 a.m." (114). The note says the time is the first day's.
- `cal.1966-01-31.vietnam-air-war`: `follows` removed, and the "After ..." sentence replaced. The Miller Center's catalogue puts the McNamara call at 9:20 a.m., and the Public Papers put the broadcast at 10 a.m. So the call came first. The link was wrong, and both times stand. The call reports strikes already flown, before either entry's time.
- `cal.1966-02-16.laos`: about midnight ending Feb. 16, Laos time (17:00Z), approximate. Anthony and Sexton, 188: the battle began around midnight on Feb. 16, the mortar fire following in the early morning hours. The note gives those words and the first-day sentence.
- `cal.1966-03-10.china-leadership-3`: afternoon, Peking. The nianpu (III, 20) puts the Baijiazhai meeting 下午. The words are added to the note.
- `cal.1966-06-08.africa-2`: night, Johannesburg. The line's "night" is the party's.
- `cal.1966-07-02.states-and-cities-omaha`: night of July 2, as a range an hour wider than the band. The register shows Nebraska's daylight time in 1966 as local option, so the clock is in doubt. A "Check:" and the first-day sentence are in the note.
- `cal.1966-07-27.china-leadership-5`: midnight at the end of July 27, Peking (16:00Z), approximate. The nianpu (III, 42) gives 午夜 as the day's last item, after the Peking University meeting.
- `cal.1966-10-01.china-leadership-5`: midnight at the end of Oct. 1, Peking (16:00Z). The nianpu (III, 71) gives 晚十二时 as the day's last item.
- `cal.1966-10-30.robert-kennedy`: about 10:30 p.m. EST. Schlesinger's journal (253): Kennedy reached the Dillons' about 10:30, and they left for Clarke's about midnight. The note says so.
- `cal.1967-03-10.vietnam-operations`: night, Saigon clock. The line calls it a night attack.
- `cal.1967-06-05.middle-east`: the morning of the Israeli strike, as a range covering both Cairo's and Israel's clocks, which were an hour apart that day. A "Check:" is in the note.
- `cal.1967-10-26.latin-america`: noon EDT, the arrival ceremony that the White House diary in the note gives. The first-day sentence is in the note.
- `cal.1967-11-29.defense-clifford`: evening, EST. "Late evening" is the late part of the evening band.
- `cal.1968-03-16.elections-1968-4`: the 6 p.m. wire, as a range of the two readings (Washington or the Ranch, an hour apart). There is no band, as the dayorder STYLE allows for a clock in doubt. A "Check:" and the first-day sentence are in the note.
- `cal.1968-04-04.robert-kennedy-campaign`: night, Indianapolis (eastern standard time all year, by the register). The first-day sentence is in the note.
- `cal.1968-08-20.soviet-union`: night, Prague. The first act is the invasion "the night of Aug. 20–21". The range ends where the range of `cal.1968-08-20.soviet-union-2` ends, so the entry's `follows` still holds. The note says whose time it is.
- `cal.1968-08-26.elections-1968-chicago-25`: about 10:30 p.m. CDT. Longley, 217, puts the interview after the convention's opening at 7:38 p.m. The note says so.
- `cal.1968-11-05.elections-1968-humphrey`: 7:55 a.m. CST, the landing at Minneapolis. It is the first act on the day, from Solberg in the note.

## Ops struck

None. The 20 ops were each kept or changed.

## Rows left with no field, and why

These are the reader's rows I checked and left. I agree with the reader's reason unless I say otherwise.

- `cal.1966-01-02.steel`: the first act, the telegram, has no hour, so the briefing's place does not decide anything.
- `cal.1966-02.vietnam-3`: dated to the month, so the hour has no day.
- `cal.1966-03-12.china-leadership-2`: the letter has no hour. The nianpu gives only the 12:30 departure.
- `cal.1966-03-26.china`: the hour is the attack of Mar. 24.
- `cal.1966-03-29.soviet-union-leadership-2`: the hours are Apr. 7's and 8's. The first day has none.
- `cal.1966-04-14.vietnam-hanoi-2`: the hour is the strike's. The cable has none.
- `cal.1966-05-02.alabama`: "by 3 p.m." is a limit.
- `cal.1966-05-20.soviet-union-leadership`: the hour is May 23's.
- `cal.1966-05.china-leadership-12`: dated to the month.
- `cal.1966-05.china-leadership-41`: dated to the month. The hour is May 24's meeting.
- `cal.1966-06-14.state-and-city-finance-nyc`: the hour is June 16's.
- `cal.1966-06-30.vietnam-hanoi-3`: 7 p.m. is the end of the firing.
- `cal.1966-07-13.vietnam-support`: 10 p.m. is a later act. The dinner has no hour.
- `cal.1966-07-16.china-leadership-2`: a daily meeting's hour.
- `cal.1966-07-20.war-opposition`: 6 p.m. is a permit's hour for Aug. 6.
- `cal.1966-07-30.open-housing`: "before midnight" is a limit on July 29's vigil.
- `cal.1966-08-09.mayors`: the first act, Daley's statement, has no hour. Noon is the Commission's.
- `cal.1966-08-29.china-leadership-7`: "1:50,000" is a map scale.
- `cal.1966-09-09.king`: the first act, the retreat, has no hour. The 6:51 p.m. call is the second act. The FBI New York log probably keeps New York's clock.
- `cal.1966-09-15.china-leadership-7`: midnight is Tao Zhu's sending. Mao's reply has no hour.
- `cal.1966-09-19.soviet-union-leadership`: the hour is Sept. 22's.
- `cal.1966-09-27.states-and-cities-san-francisco`: 11:39 p.m. is a later act. The shooting has no hour.
- `cal.1966-09-27.china-leadership-5`: the cremation, a later act.
- `cal.1966-10-26.china-leadership-3`: 9 a.m. is the launch time for the 27th.
- `cal.1966-11-15.china-leadership`: midnight is Nov. 16's.
- `cal.1966-11-24.china-leadership`: 1 a.m. is Nov. 28's.
- `cal.1966-11.robert-kennedy-2`: dated to the month.
- `cal.1966-12-23.china-leadership-3`: 3 a.m. is the end of the meeting.
- `cal.1967-01-02.vietnam-air-war-2`: 7 a.m. is the end of the stand-down. The air battle has no hour.
- `cal.1967-01-28.soviet-union-leadership`: the hour is Jan. 31's.
- `cal.1967-02-02.china-leadership-3`: the hours are of the meetings proposed.
- `cal.1967-02-03.soviet-union-leadership`: the hour is Feb. 2's.
- `cal.1967-02-09.vietnam`: a cease-fire's start and a report's cut-off.
- `cal.1967-02-25.china-leadership-7`: the hour is Dec. 22's.
- `cal.1967-02.china-leadership-22`: dated to the month.
- `cal.1967-03-12.india-and-china`: the first act, the MPRS vote, has no hour. I read FRUS docs. 232 and 233, and only the swearing-in has one (10:45 p.m., doc. 233 n.2).
- `cal.1967-03-19.vietnam-operations`: the hour is Mar. 21's.
- `cal.1967-03-31.vietnam-operations`: the hour is Apr. 1's.
- `cal.1967-04-12.railroads`: 12:01 a.m. May 3 is a term in the statute.
- `cal.1967-04-24.china`: a deadline.
- `cal.1967-05-09.soviet-union-leadership`: the hour is May 13's.
- `cal.1967-05-25.middle-east`: the hours are May 26's.
- `cal.1967-06-06.middle-east`: the chief act, the Council's vote, has no hour in the line. Radio Cairo's 7:40 a.m. and the President's statement are other acts.
- `cal.1967-06-09.middle-east`: the hour is June 10's.
- `cal.1967-06-17.china-leadership-9`: 8:20 a.m. is the explosion. The call came "随即" (right after), and the existing `follows` places it.
- `cal.1967-06-24.china-leadership-9`: a daily routine.
- `cal.1967-07-01.robert-kennedy`: noon is the heat, not the act.
- `cal.1967-07-05.vietnam-operations`: the first act has no hour.
- `cal.1967-07-05.vietnam-hanoi-2`: 11 p.m. is the end. The existing `follows` places it.
- `cal.1967-08.china-leadership-35`: dated to the month.
- `cal.1967-09-15.china-leadership`: noon is a deadline.
- `cal.1967-10-05.china`: the hour is Oct. 1's.
- `cal.1967-10-08.china-leadership-2`: midnight is when the order takes effect, not the notice's own hour. The day of the notice is itself in doubt (the note's Check).
- `cal.1968-01-24.china-leadership`: the hour is the 26th's.
- `cal.1968-01-27.vietnam-tet-2`: the hours are the truces' terms.
- `cal.1968-01-29.vietnam-tet-4`: the day itself is in doubt (the note's Check). 5 p.m. is the end of the fight.
- `cal.1968-02-05.vietnam-tet-3`: the hour is Jan. 31's.
- `cal.1968-02-07.jobs-and-wages-nyc`: 7 a.m. is a deadline.
- `cal.1968-02-18.vietnam-tet-3`: the hour is Feb. 19's.
- `cal.1968-02-29.vietnam-tet`: the hours bound a count.
- `cal.1968-03-19.king-poor-peoples`: the first act has no hour.
- `cal.1968-03-25.vietnam`: the hours are Mar. 26's. The first day's dinner has no hour.
- `cal.1968-04.vietnam-paris-2`: dated to the month.
- `cal.1968-05-06.robert-kennedy-campaign-primaries`: the motorcade's start has no hour. 5 p.m. was the schedule.
- `cal.1968-06-23.china-leadership-2`: the hour is June 24's.
- `cal.1968-08-05.elections-1968-miami-12`: 11:27 p.m. is the adjournment. The keynote has no hour.
- `cal.1968-08-18.elections-1968-chicago`: 11 p.m. is a nightly curfew.
- `cal.1968-08-24.elections-1968-chicago`: the first act, the command post's opening, has no hour.
- `cal.1968-08-27.elections-1968-chicago-4`: the committee's forming has no hour.
- `cal.1968-08-29.elections-1968-chicago-5`: I read *Rights in Conflict*, 341–43. The march has no hour: "By 6:30" is the gathering and "by 9:30" is a limit.
- `cal.1968-09-27.elections-1968`: the walkout has no hour.
- `cal.1968-09-28.elections-1968-2`: the auditorium event has no hour.
- `cal.1968-09-29.elections-1968-4`: the first act has no hour. The 2 p.m. meeting's place is Seattle or Salt Lake City, an hour apart.
- `cal.1968-09.elections-1968-7`: dated to the month.
- `cal.1968-09.elections-1968-16`: dated to the month.
- `cal.1968-10-25.congress`: the call's day is in doubt.
- `cal.1968-10-30.vietnam-paris`: Oct. 30's first act, Lâu's word, has no hour.
- `cal.1968-10-31.vietnam-hanoi`: the hour is the expected halt's.
- `cal.1968-11-05.elections-1968-nixon-3`: the hours are the flight's end. The existing `follows` places the entry.
- `cal.1968-12-11.transition-and-staff`: the hours are Dec. 12's.
- `cal.1968-12-16.soviet-union-leadership`: the first day has no hour.
- `cal.1969-01-19.transition-and-staff`: the first act, the Mass, has no hour.
- `cal.1969-01.transition-and-staff-4`: dated to the month.
- `cal.1969-03-07.china`: noon is the incident's. The note has no hour.
- `cal.1969-04-11.china-leadership-2`, `-04-12 ...-3`, `-04-15 ...-3`, `-04-17`, `-04-19 ...-2`: 2 a.m. is the night's end after a day of reading or writing. The entries carry `ok:fields-time`.
- `cal.1969-04-22.soviet-union-leadership`: the hours are Apr. 23's and 26's.
- `cal.1969-04-24.china-leadership-3`: the hours are the meetings Mao approves.
- `cal.1969-04-28.china-leadership-3`: the hours are the report's and the meeting's. The reply falls between them, but that span is not a band.
- `cal.1969-04.china-leadership-21`: dated to the month.
- `cal.1969-06-03.soviet-union-leadership`: the hours are June 4's.
- `cal.1969-06-06.china`: the hour is May 28's.
- `cal.1969-09-03.vietnam-hanoi`: 9:47 a.m. is the death as announced. The call has no hour.
- `cal.1969-10-03.china-leadership-9`: a log of spans over the day.
- `cal.1970-01-05.china-leadership`: the hour is the earthquake's.

## Entries that hold more than one event (for a later pass)

Each of these puts in one entry acts that R17 would give entries of their own: an act and its report, acts of different days, or a meeting and its later result.

- `cal.1966-01-31.vietnam`: the letters of Jan. 21, 27 and 28, Hồ's letter, the NSC of Jan. 29, the resumption, the broadcast, Goldberg's request, the Council's vote of Feb. 2.
- `cal.1966-01-02.steel`: the telegram; the briefing.
- `cal.1966-01-10.mississippi-3`: the hospital morning; the death.
- `cal.1966-03-09.china-leadership-2`: the Xingtai talk; the Longyao visit.
- `cal.1966-03-29.soviet-union-leadership-2`: a congress of eleven days, the editorial commission, the last sitting.
- `cal.1966-04-14.vietnam-hanoi-2`: the strike on Nam Định; the cable reporting it.
- `cal.1966-05-20.soviet-union-leadership`: the trip of May 17–23; the talks with Kim.
- `cal.1966-06-14.state-and-city-finance-nyc`: the talks; the settlement of June 16.
- `cal.1966-07-02.states-and-cities-omaha`: the riots of July 2–4; the Guard request of July 5; the mayor's meeting.
- `cal.1966-08-09.mayors`: Daley's statement; the Commission's meeting; Daley's call.
- `cal.1966-09-09.king`: the Memphis retreat; the call to Levison.
- `cal.1966-09-11.china-leadership`: Tao Zhu's sending at 1 a.m.; Mao's circling.
- `cal.1966-09-27.states-and-cities-san-francisco`: the shooting, the riot, the Guard, Sept. 28's shooting, the end of the emergency.
- `cal.1966-11-15.china-leadership`: Mao's meeting of Nov. 15; the Politburo and Mao's reply of Nov. 16.
- `cal.1966-11-24.china-leadership`: Mao's notes of Nov. 24 and Nov. 28.
- `cal.1967-01-02.vietnam-air-war-2`: the air battle; the stand-down's end.
- `cal.1967-01-28.soviet-union-leadership`, `cal.1967-05-09.soviet-union-leadership`, `cal.1968-12-16.soviet-union-leadership`, `cal.1969-04-22.soviet-union-leadership`, `cal.1969-06-03.soviet-union-leadership`: the meeting at the airport, the talks and the leave-taking of several days.
- `cal.1967-02-09.vietnam`: the cease-fire, the supply effort, the *Stoddard*, Sharp's request.
- `cal.1967-03-10.vietnam-operations`: the night attack; the phases of Mar. 17–18.
- `cal.1967-03-12.india-and-china`: the MPRS vote; the swearing-in; Green's cable of Mar. 15.
- `cal.1967-05-25.middle-east`: Eban with Rusk; the advisers' meeting; Eban with Johnson.
- `cal.1967-06-05.middle-east`: the strike; the hot line; McCloskey's statement.
- `cal.1967-06-06.middle-east`: the Council's vote; Johnson's statement; Radio Cairo; the breaks in relations.
- `cal.1967-06-09.middle-east`: Egypt's acceptance, the Golan, Nasser's resignation, the hot line, the fleet, the break, the cease-fire, Resolution 236.
- `cal.1967-07-05.vietnam-operations`: the air strikes; the artillery.
- `cal.1967-07-22.china-leadership`, `cal.1967-07-25.china-leadership`, `cal.1967-09-16.china-leadership`: two acts each, hours apart.
- `cal.1967-10-26.latin-america`: the state visit; the Chamizal transfer; the conference at El Paso.
- `cal.1968-01-24.china-leadership`: the reception of Jan. 24; the talk of the 26th.
- `cal.1968-02-05.vietnam-tet-3`: Cần Thơ; Vĩnh Long of Feb. 8.
- `cal.1968-03-16.elections-1968-4`: the wires of Mar. 16; the wire of Mar. 17; Johnson to Sidey.
- `cal.1968-03-25.vietnam`: the dinner and briefings of Mar. 25; Johnson with Wheeler and Abrams; the meeting of Mar. 26.
- `cal.1968-05-27.robert-kennedy`: the spots; the wire; Salinger's statement.
- `cal.1968-06-05.assassination-12`: Yorty's press conference; the arraignment; Reddin's statement.
- `cal.1968-08-20.soviet-union`: the invasion; Dobrynin with Johnson; the NSC; the call to Nixon and the statement of Aug. 21.
- `cal.1968-08-24.elections-1968-chicago`: the command post; the statements; the clearing.
- `cal.1968-08-27.elections-1968-chicago-4`: the committee; the delegation at 4 p.m.; the vigil.
- `cal.1968-09-27.elections-1968`: the walkout; the night's work on the speech.
- `cal.1968-09-29.elections-1968-4`: the draft, the telegram, the 2 p.m. meeting, the night session.
- `cal.1968-10-30.vietnam-paris`: Lâu's word; Johnson's meeting; the Paris meeting of Oct. 31.
- `cal.1968-11-05.elections-1968-humphrey`: the flight; the vote; the evening at the Leamington.
- `cal.1968-12-11.transition-and-staff`: the Cabinet on television; Nixon with Johnson on Dec. 12.
- `cal.1969-01-19.transition-and-staff`: the church, the calls, the visits, the buffet.
- `cal.1970-01-05.china-leadership`: the report of Jan. 5; Zhou's notes of Jan. 7.

## Owner's questions taken by default

- Where an entry holds several acts on one day and only a later act has an hour, I set no field. I read R25's "first act's time" as applying to the acts of one day as well as to entries of several days. This applies throughout the patch.
- "Late evening" took the evening band (7 to 10 p.m.). No band is closer.
