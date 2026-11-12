# Lady Bird Johnson, *A White House Diary* (1970): Book Two, 1965, against the calendar

Card `w.johnson-white-house-diary` (the 1964 reader's share, Nov. 1963–Dec. 1964, patch `2026-11-12-b11-ladybird-1964`, uses the same card). Read Nov. 11–12, 2026 (batch 11, the 1965 share): Book Two, "1965", printed pp. 213–342, from the Drive copy `1yDhieBtd5zcvoMYqrteT6Yg3a-R6sOie` (864 PDF pages, 40 MB). The copy was deleted when the reading was done.

**The copy and its offset.** The PDF has a text layer (`pdftotext -layout`); no OCR was needed. The folio is printed at the foot of the page ("214 / A White House Diary"). Printed page = PDF page (counted from 1) minus 22 through p. 278 (p. 214 = PDF 236; p. 256 = PDF 278); eight unnumbered plate pages follow (PDF 301–308, the photographs, the caption of Moro's arrival of Apr. 20 on the third), then minus 30 (p. 294 = PDF 324; p. 329 = PDF 359). Checked against the page images (`pdftoppm -r 80`) at pp. 214, 256, 294 and 329. Every quotation entered was matched by a script against the text layer, and those on pp. 214, 256, 294 and 329 read off the image. Book Two runs from Jan. 1, 1965 (p. 213) to Dec. 20 (p. 342); the diary has no entry between Aug. 12 and Sept. 2, Sept. 11 and Oct. 3, or Nov. 3 and Dec. 14, and none after Dec. 20.

**The patch:** `inbox/2026-11-12-b11-ladybird-1965.yaml` (patch `2026-11-12-b11-ladybird-1965`): 95 new entries (ids claimed in the ledger first), 40 `cite` ops, 5 `variant` ops, 3 `check` ops. `./bib patch-check`: 0 errors. The warnings are "one event?" on entries that share a day and thread with another and are distinct events; `./bib resolve ID --take keep` settles each if the merge flags it. The diary is Mrs. Johnson's account throughout: every `n` says so where it matters, and a private act carries "Made public: 1970."

This book-check file was created by the 1965 reader (the 1964 reader's had not been written when this was; merge the two sections).

## Entered (new)

| Day | Entry | Page |
|---|---|---|
| Jan. 4 | `cal.1965-01-04.democratic-party` | 214–15 |
| Jan. 6 | `cal.1965-01-06.congress` | 216 |
| Jan. 14 | `cal.1965-01-14.poverty` | 219 |
| Jan. 14 | `cal.1965-01-14.transition-and-staff` | 219–20 |
| Jan. 15 | `cal.1965-01-15.trade` | 220–22 |
| Jan. 18 | `cal.1965-01-18.democratic-party` | 223–24 |
| Jan. 18 | `cal.1965-01-18.transition-and-staff` | 224–25 |
| Jan. 18 | `cal.1965-01-18.transition-and-staff-2` | 222 |
| Jan. 20 | `cal.1965-01-20.transition-and-staff-2` | 227–29 |
| Jan. 20 | `cal.1965-01-20.democratic-party-2` | 229–30 |
| Jan. 20 | `cal.1965-01-20.transition-and-staff-3` | 224 |
| Jan. 21 | `cal.1965-01-21.program` | 230–31 |
| Jan. 24 | `cal.1965-01-24.succession` | 231–32 |
| Jan. 27 | `cal.1965-01-27.europe-and-the-alliance` | 232 |
| Jan. 27 | `cal.1965-01-27.transition-and-staff` | 232–34 |
| Jan. 27 | `cal.1965-01-27.press-and-broadcasting` | 232–33 |
| Feb. 3 | `cal.1965-02-03.conservation` | 234 |
| Feb. 3 | `cal.1965-02-03.poverty` | 234–35 |
| Feb. 3 | `cal.1965-02-03.civil-rights-organizations` | 235–36 |
| Feb. 4 | `cal.1965-02-04.soviet-union-un` | 236 |
| Feb. 4 | `cal.1965-02-04.republican-party-congress` | 237 |
| Feb. 5 | `cal.1965-02-05.conservation` | 237–38 |
| Feb. 5 | `cal.1965-02-05.students` | 237–38 |
| Feb. 8 | `cal.1965-02-08.press-and-broadcasting` | 238–39 |
| Feb. 9 | `cal.1965-02-09.white-house` | 239–40 |
| Feb. 11 | `cal.1965-02-11.conservation` | 240–42 |
| Feb. 12 | `cal.1965-02-12.program` | 242–43 |
| Feb. 12 | `cal.1965-02-12.transition-and-staff` | 243–44 |
| Feb. 18 | `cal.1965-02-18.white-house` | 245 |
| Mar. 3 | `cal.1965-03-03.poverty` | 246–47 |
| Mar. 9 | `cal.1965-03-09.conservation` | 248–50 |
| Mar. 9 | `cal.1965-03-09.program` | 250 |
| Mar. 11 | `cal.1965-03-11.latin-america` | 250–51 |
| Mar. 15 | `cal.1965-03-15.voting-rights-10` | 252–54 |
| Mar. 15 | `cal.1965-03-15.congress` | 253–54 |
| Mar. 15 | `cal.1965-03-15.white-house` | 251 |
| Mar. 28 | `cal.1965-03-28.conservation` | 254 |
| Apr. 10 | `cal.1965-04-10.poverty` | 257–58 |
| Apr. 11 | `cal.1965-04-11.intelligence` | 259 |
| Apr. 11 | `cal.1965-04-11.elections-1968-johnson` | 259–60 |
| Apr. 16 | `cal.1965-04-16.elections-1968-johnson` | 260 |
| Apr. 19 | `cal.1965-04-19.program` | 261 |
| Apr. 19 | `cal.1965-04-19.vietnam-support` | 261–62 |
| Apr. 19 | `cal.1965-04-19.south-carolina` | 262–63 |
| Apr. 20 | `cal.1965-04-20.europe-and-the-alliance` | plates |
| Apr. 21 | `cal.1965-04-21.europe-and-the-alliance` | 263–64 |
| Apr. 21 | `cal.1965-04-21.vietnam-support` | 264 |
| Apr. 27 | `cal.1965-04-27.defense` | 264–65 |
| May 4 | `cal.1965-05-04.program` | 266–67 |
| May 5 | `cal.1965-05-05.poverty` | 267–69 |
| May 5 | `cal.1965-05-05.program` | 268–69 |
| May 5 | `cal.1965-05-05.soviet-union` | 268 |
| May 6 | `cal.1965-05-06.congress` | 269–70 |
| May 11 | `cal.1965-05-11.conservation` | 270–73 |
| May 11 | `cal.1965-05-11.program` | 272–73 |
| May 18 | `cal.1965-05-18.japan` | 274–75 |
| June 1 | `cal.1965-06-01.program` | 277–78 |
| June 1 | `cal.1965-06-01.republican-party` | 279 |
| June 3 | `cal.1965-06-03.states-and-cities` | 280–82 |
| June 10 | `cal.1965-06-10.conservation` | 283–84 |
| June 10 | `cal.1965-06-10.white-house` | 284–85 |
| June 15 | `cal.1965-06-15.transition-and-staff` | 287–88 |
| June 17 | `cal.1965-06-17.space-2` | 288–89 |
| June 17 | `cal.1965-06-17.crime-and-hijacking` | 290–92 |
| July 2 | `cal.1965-07-02.press-and-broadcasting` | 292–94 |
| July 2 | `cal.1965-07-02.program` | 294–95 |
| July 13 | `cal.1965-07-13.transition-and-staff` | 295–96 |
| July 16 | `cal.1965-07-16.transition-and-staff` | 298–99 |
| July 16 | `cal.1965-07-16.court-fortas` | 299–300 |
| July 17 | `cal.1965-07-17.alabama` | 301 |
| July 18 | `cal.1965-07-18.crime-and-hijacking` | 302–03 |
| July 18 | `cal.1965-07-18.press-and-broadcasting` | 303 |
| July 21 | `cal.1965-07-21.court-fortas` | 304 |
| July 21 | `cal.1965-07-21.press-and-broadcasting` | 305–06 |
| Aug. 12 | `cal.1965-08-12.poverty` | 308–11 |
| Aug. 12 | `cal.1965-08-12.conservation` | 311 |
| Aug. 12 | `cal.1965-08-12.program` | 311 |
| Aug. 12 | `cal.1965-08-12.economy` | 311 |
| Sept. 2 | `cal.1965-09-02.transition-and-staff` | 312–14 |
| Sept. 2 | `cal.1965-09-02.program` | 314–15 |
| Sept. 7 | `cal.1965-09-07.succession` | 316–17 |
| Sept. 7 | `cal.1965-09-07.conservation` | 318–20 |
| Sept. 10 | `cal.1965-09-10.states-and-cities` | 320 |
| Oct. 3 | `cal.1965-10-03.program` | 323–24 |
| Oct. 5 | `cal.1965-10-05.succession` | 324 |
| Oct. 6 | `cal.1965-10-06.congress` | 326 |
| Oct. 6 | `cal.1965-10-06.europe-and-the-alliance` | 327 |
| Oct. 11 | `cal.1965-10-11.foreign-aid` | 328 |
| Oct. 11 | `cal.1965-10-11.soviet-union` | 328 |
| Oct. 21 | `cal.1965-10-21.vietnam-support` | 329 |
| Oct. 30 | `cal.1965-10-30.white-house` | 330–32 |
| Nov. 2 | `cal.1965-11-02.elections-1965` | 332–33 |
| Nov. 3 | `cal.1965-11-03.economy` | 336 |
| Dec. 14 | `cal.1965-12-14.south-asia` | 337–40 |
| Dec. 20 | `cal.1965-12-20.europe-and-the-alliance-2` | 341–42 |

## Cited (the card) and what the page bears

| Entry | Units | Page | Ruling |
|---|---|---|---|
| `cal.1965-01-04.program` | ? | 214–15 | pinned in part (the cite says what and what not) |
| `cal.1965-01-04.congress-2` | ? | 214 | pinned in part (the cite says what and what not) |
| `cal.1965-01-12.japan-and-korea` | A | 217–19 | cited |
| `cal.1965-01-20.transition-and-staff` | A, D | 225–27 | cited |
| `cal.1965-01-24.europe-and-the-alliance` | ? | 231, 232 | pinned in part (the cite says what and what not) |
| `cal.1965-01-25.economy` | ? | 231 | pinned in part (the cite says what and what not) |
| `cal.1965-02-09.vietnam-congress-3` | ? | 240 | pinned in part (the cite says what and what not) |
| `cal.1965-02-09.soviet-union` | ? | 239 | pinned in part (the cite says what and what not) |
| `cal.1965-02-14.vietnam-congress-2` | ? | 244–45 | pinned in part (the cite says what and what not) |
| `cal.1965-03-07.vietnam` | ? | 247–48 | pinned in part (the cite says what and what not) |
| `cal.1965-03-11.civil-rights-the-executive` | ? | 250 | pinned in part (the cite says what and what not) |
| `cal.1965-03-11.voting-rights-selma-3` | ? | 251 | pinned in part (the cite says what and what not) |
| `cal.1965-03-15.vietnam` | ? | 251 | pinned in part (the cite says what and what not) |
| `cal.1965-03-15.voting-rights` | ? | 252–54 | pinned in part (the cite says what and what not) |
| `cal.1965-04-07.vietnam` | B | 256 | cited |
| `cal.1965-04-08.medicare` | ? | 257 | pinned in part (the cite says what and what not) |
| `cal.1965-04-11.school-aid` | ? | 258–59 | pinned in part (the cite says what and what not) |
| `cal.1965-04-17.vietnam` | ? | 260–61 | pinned in part (the cite says what and what not) |
| `cal.1965-05-02.latin-america` | ? | 265 | pinned in part (the cite says what and what not) |
| `cal.1965-05-18.poverty` | A | 274 | cited |
| `cal.1965-05-21.program` | A, B | 275–77 | cited |
| `cal.1965-06-10.vietnam-july-decision` | ? | 286 | pinned in part (the cite says what and what not) |
| `cal.1965-06-14.war-opposition` | E | 286–87 | cited |
| `cal.1965-06-17.space` | A-C | 290–91 | cited |
| `cal.1965-07-02.school-aid` | ? | 294 | pinned in part (the cite says what and what not) |
| `cal.1965-07-13.court` | A | 295–96 | cited |
| `cal.1965-07-14.transition-and-staff` | ? | 296 | pinned in part (the cite says what and what not) |
| `cal.1965-07-21.vietnam` | ? | 304 | pinned in part (the cite says what and what not) |
| `cal.1965-07-21.school-aid` | ? | 304–05 | pinned in part (the cite says what and what not) |
| `cal.1965-08-06.voting-rights` | ? | 306 | pinned in part (the cite says what and what not) |
| `cal.1965-08-12.vietnam` | ? | 311 | pinned in part (the cite says what and what not) |
| `cal.1965-09-03.steel` | ? | 315–16 | pinned in part (the cite says what and what not) |
| `cal.1965-10-03.immigration` | ? | 321–22 | pinned in part (the cite says what and what not) |
| `cal.1965-10-05.program` | ? | 325 | pinned in part (the cite says what and what not) |
| `cal.1965-10-06.health` | ? | 326 | pinned in part (the cite says what and what not) |
| `cal.1965-10-08.succession` | ? | 324 | pinned in part (the cite says what and what not) |
| `cal.1965-10-21.cities-and-housing` | ? | 329 | pinned in part (the cite says what and what not) |
| `cal.1965-11-03.transition-and-staff` | ? | 334–35 | pinned in part (the cite says what and what not) |
| `cal.1965-12-14.india-and-china` | A | 336–39 | cited |
| `cal.1965-12-20.europe-and-the-alliance` | ? | 340–42 | pinned in part (the cite says what and what not) |

## Variants and Checks

- `cal.1965-02-09.vietnam-congress-3`, unit A: the page (240) reads "about fifty Congressmen and their wives at each".
- `cal.1965-03-07.vietnam`, unit B: the page (248) reads "I can't get out. I can't finish it with what I have got. So what the Hell can I do?".
- `cal.1965-03-11.civil-rights-the-executive`, unit C: the page (251) reads "the demonstrators "had departed, after some urging" by the police "around 6 o'clock"".
- `cal.1965-05-18.poverty`, unit B: the page (274) reads "over sixteen hundred grants ... about 9500 pre-school centers that will serve 375,000 children this summer for eight weeks".
- `cal.1965-11-03.transition-and-staff`, unit B: the page (334) reads "First, John Gronouski was sworn in, standing in front of the fireplace, with his wife beside him".
- `cal.1965-01-28.transition-and-staff`: Check: Mrs. Johnson's diary (232–34) has Johnson naming Katzenbach Attorney General and Ramsey Clark Deputy on Jan. 27, Katzenbach and his wife at the family quarters that evening; [[cal.1965-01-27.cal.1965-01-27.transition-and-staff]].
- `cal.1965-04-15.south-asia`: Check: Mrs. Johnson's diary (261) has the postponement of the Ayub Khan and Shastri visits announced by Johnson to reporters at the Ranch on Apr. 17.
- `cal.1965-05-02.latin-america`: Check: the day of the report Mrs. Johnson watched; her diary (265), of May 4, says only "his TV report" seen at the Ranch in her three days in Texas.

## Passed over (with the card's ground)

Family matter, no bearing on public business (Q5): Jan. 1 (closets, resolutions); Jan. 4 (tickets, the girls' dressing, Luci's room); Jan. 18, 20 (houseguests, kinfolk, "Cousin Fern Baines," who turns out to be Humphrey's sister); Jan. 27 (Luci's cake); Feb. 9 (Luci's history class; Mrs. Acheson); Feb. 14 (Valentines; the National Gallery with Lynda); Mar. 7 (church, Kimberley Fry); Mar. 28 (Johnson's college years, told at Camp David); Apr. 16 (the sheep at the Scharnhorst); Apr. 21 (Mrs. Longworth to tea, her stories); May 21 (Luci's invitations, Camp David); June 1 (Luci's surprise party); June 10 (Father Montgomery on Luci's instruction; the plan, kept from the staff, is entered only at its day, July 2, where the statement was given to the press); July 14 (Lynda in the Tetons); Sept. 11 (Lynda and Luci in New York); Oct. 3 morning (the Fergusons from Johnson City); Oct. 5, 11 (the pool, the dentist); Oct. 28 (the walk; the sunset); Oct. 30 (the barrage of stories on Luci and Pat Nugent; Johnson's "I am just going to wait until this dies down"; his talk with Hurd entered; the Nicholson place); Nov. 2 (tea for the telephone operators; the roadrunner); Nov. 3 (the spinach); Dec. 14 (the Christmas album; Luci's Christmas with the Nugents); Dec. 20 (the tree, the creche).

A covering schedule, a repetition, a social occasion with no act or word of public business (Q5): May 4 (the Metropolitan Opera singers, Project HOPE, Pictures for Patients, the Multiple Sclerosis Mother, the Episcopal Home, the Bethesda Chamber of Commerce, each greeted in turn; the Senate Ladies Luncheon, "a big event of each spring"); the Congressional receptions of Feb. 11, Mar. 9 and 11 (the seventh to tenth of ten, the pattern of Feb. 9 repeated: briefing for the men, a film for the ladies, a buffet; the one on Feb. 9 is cited, Connally's talk after Mar. 9's entered); Mar. 11 (the Latin American wives' lunch entered; the Sevilla-Sacasa precedence kept to that entry); Apr. 7 (the Frick Museum's lighting); Aug. 6 (the Hirshhorn collection at Greenwich: a visit to see art, nothing of the gift said but what the May 21 lunch holds); Aug. 12 (Morgan and Gilstrap "interviews," names only); Jan. 21 (dinner with the Humphreys and the Thornberrys, nothing of business said); Feb. 4 (the Congressional Prayer Breakfast, named only; lunch with Barbara Ward on urban renewal and Latin America, her views, no act of a principal); Mar. 15 (Collins's barber story); Apr. 7 (the Frick).

Not Mrs. Johnson's own acts and not the President's, but the diary's report of another's: Mar. 9 (the Selma march turned back, "in accord with the court order": the day is the calendar's; her page adds only that she learned of the beating of Reeb later); Sept. 3 (the Home Rule bill, "a vote on September 27": see Leads); Apr. 10 (Johnson's week: Medicare 313 to 115, the Civil Rights Bill reported "quicker and stronger than ever expected," the Education Bill: Medicare is cited at its entry; the other two are leads).

## Leads

- Sept. 3 (316): "a near victory for Home Rule in the District of Columbia ... a vote on September 27," the House District Committee having held it for years; not searched against the calendar's September.
- Apr. 10 (257): "the Committee reported out the Civil Rights Bill" in the week of Apr. 8, quicker than expected (the voting bill, in the Senate Judiciary Committee?); not searched.
- Feb. 9 (240), Mar. 9 and 11 (250–52): ten Congressional receptions for about fifty Congressmen and wives at each, eight for the House and two for the Senate, each with a briefing for the men by McNamara, Ball or others; only the first is cited (the dates of the others, Feb. 11, Mar. 9 and 11, in the diary; the rest not dated by it).
- May 18 (273–74): the Hurds, a portrait of Johnson from sittings at the Ranch, Mrs. Johnson's three goals for history (the portrait, the Library, the boyhood home restored); the Library's story continues Feb. 12 and Sept. 2 (entered).
- July 21 (305): Hagerty's advice on a television adviser "as Robert Montgomery gave President Eisenhower"; the cal's press thread of July–Aug. may hold the staff changes.
- Oct. 5 (325): Udall and Bill Mauldin bring up the cartoon "Impeach Lady Bird" at the stag dinner (a billboard cartoon): a Mauldin cartoon, not searched.
- The plates (after p. 278) carry captions dated to the day: "Arrival ceremonies for Italian Prime Minister Aldo Moro on the South Grounds, April 20" (entered), "Signing of Health Research Facilities Amendments, August 9, with Paul Rogers, Horace Kornegay, Jacob Javits, Lister Hill" (not searched against the calendar's Aug. 9), "With Princess Margaret of Great Britain in the Queen's Room, November 17" (a day of 1965 the diary text does not give; not searched), and Pearson at the Ranch, Jan. 1965 (undated).
- Book Two's other dated matter (Jan. 5 and 15 and others) is in the diary's own gaps: nothing between Aug. 12 and Sept. 2, Sept. 11 and Oct. 3, Nov. 3 and Dec. 14.

Where batch 11 stopped: Book Two of the diary read through, every page, to Dec. 20 (p. 342, the end of 1965); every dated item with a bearing on public business is in the patch or in the lists above. The auditor's blind pass is still to come.
