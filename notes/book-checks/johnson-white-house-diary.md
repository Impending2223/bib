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


---

# Part two: Nov. 22, 1963 to Nov. 21, 1964 (the 1964 reader)


Lady Bird Johnson, *A White House Diary* (1970), card `w.johnson-white-house-diary` (listed `kja.johnson-lady-bird`, K–J Adm. II.G.3, and `l68.johnson-lady-bird`, 1968 II.C.1). Read Nov. 11–12, 2026 (batch 11) from the owner's copy, Drive `1yDhieBtd5zcvoMYqrteT6Yg3a-R6sOie` (864 PDF pages, a text layer, no OCR; read with `pdftotext -layout`; the PDF and its page images deleted when done).

**Offset.** Printed page = PDF page less 14 for the front matter and Book One's text, pp. 1–182 (PDF 15–196): checked on the folios and by image at p. 7 = PDF 21, p. 87 = PDF 101, p. 94 = PDF 108, p. 158 = PDF 172. The plates (PDF 197–204, no folios) follow p. 182; after them printed page = PDF page less 22: p. 183 = PDF 205 (checked by image), p. 192 = PDF 214 (by image), p. 209 = PDF 231. Book One ends at p. 209 (PDF 231); Book Two, 1965, begins at p. 213 (PDF 235).

**Share (batch 11).** Book One, 1963–1964, pp. 3–209: Nov. 22, 1963 to Nov. 21, 1964, every page. The diary has no entry between Sept. 11 and Nov. 14, 1964 (the campaign, Mrs. Johnson says on p. 198, "I missed recording"); her retrospective note on the Whistlestop, pp. 198–99, is cited under the entry for the train. It has none for Dec. 1964. 1965 (pp. 213–) belongs to another reader.

**Form.** A diary: Mrs. Johnson's account, dated by the diary's day; "by Mrs. Johnson's account" where it matters; her words in quotation marks; hearsay marked as hers. Her entries are written the evening of the day or later (she says so for Mar. 12, "several days later", and for Aug. 25 and Sept. 4); the day is the diary's. Pinpoints are printed pages. Where the calendar already held the event, the diary is cited under it (units `?`, the parenthetical saying what the page bears and what not, never a unit mapped that the page does not state); new entries are claimed in the ledger and carry the diary alone.

**Patch.** `inbox/2026-11-12-b11-ladybird-1964.yaml` (patch `2026-11-12-b11-ladybird-1964`).

**Limits.** The quotations and numbers of the entries were read off the text layer. Checked against the page image, word for word: pp. 87, 94, 158, 183 and 192 (the quotations on them); everything else rests on the text layer alone and the auditor should check it on the image (the text layer has OCR slips: "Hie" for "The"; "Friday, January ly" is Jan. 17, by the weekday). The patch-check warns "a duplicate of ..." on many new entries, new events on a day and thread the calendar already holds; each is a distinct event, and the lead may resolve them `--take keep`.

## What was entered, cited, checked (by date)

| Date | Ruling | Entry | Pages | The page bears |
|---|---|---|---|---|
| 1963-11-22 | cited | `cal.1963-11-22.succession` | 5–6 | the oath at Mrs. Kennedy's side, Mrs. Johnson beside him, Judge Hughes before him; the bri |
| 1963-11-22 | cited | `cal.1963-11-22.succession-14` | 7 | home from Andrews in a car with Liz Carpenter; not what was said) |
| 1963-11-22 | entered | `cal.1963-11-22.assassination-13` | 3–4 | Dallas. The Johnsons ride third in the motorcade, behind the Kennedys and the Connallys, w |
| 1963-11-22 | entered | `cal.1963-11-22.succession-18` | 4–5 | Parkland Hospital, a small room lined with sheets. Johnson with Thornberry, Brooks, O'Donn |
| 1963-11-22 | entered | `cal.1963-11-22.succession-19` | 5 | Air Force One, Love Field. Word to Washington, "I believe to the Attorney General": Johnso |
| 1963-11-23 | cited | `cal.1963-11-23.succession-12` | 7 | Johnson with Mrs. Johnson to the White House, the Kennedy family in the Green Room; he wal |
| 1963-11-23 | entered | `cal.1963-11-23.succession-13` | 7 | St. John's Episcopal Church, Lafayette Square. Johnson and Mrs. Johnson at a brief service |
| 1963-11-24 | cited | `cal.1963-11-24.succession-6` | 8 | church at St. Mark's with Luci and Thornberry; Baxter's sermon: whoever fostered an atmosp |
| 1963-11-24 | entered | `cal.1963-11-24.assassination-6` | 8–10 | Washington. Johnson and Mrs. Johnson ride with Mrs. Kennedy and Robert Kennedy behind the  |
| 1963-11-26 | cited | `cal.1963-11-26.latin-america` | 12 | the East Room, about 5 p.m.: Johnson to the Alliance for Progress representatives, "contin |
| 1963-11-26 | cited | `cal.1963-11-26.succession-3` | 10 | J. B. West at The Elms in the morning on moving three suites of furniture; Mrs. Johnson's  |
| 1963-11-26 | entered | `cal.1963-11-26.succession-5` | 10–12 | The White House, 3 p.m. Mrs. Kennedy receives Mrs. Johnson to go over the housekeeping, by |
| 1963-12-02 | entered | `cal.1963-12-02.program` | 12–13 | The Cabinet Room, late afternoon. Johnson presents the Enrico Fermi Award to Oppenheimer,  |
| 1963-12-02 | entered | `cal.1963-12-02.succession-2` | 13–14 | The Elms, dinner. Johnson and Mrs. Johnson with Drew and Luvie Pearson, Justice and Mrs. G |
| 1963-12-07 | cited | `cal.1963-12-07.succession` | 14–16 | the move in the afternoon, Mr. West notifying them Mrs. Kennedy had left; the press at the |
| 1963-12-07 | Check | `cal.1963-12-07.economy-2` |  | Lady Bird Johnson, 33, has "about eighty-nine businessmen" at a stag dinner for the Business  |
| 1963-12-07 | entered | `cal.1963-12-07.press-and-broadcasting-2` | 14–15 | The White House. Liz Carpenter, Mrs. Johnson's staff director and press secretary, meets g |
| 1963-12-07 | entered | `cal.1963-12-07.succession-2` | 16 | Evening, the house of Walter and Marjorie Jenkins. Johnson and Mrs. Johnson to dinner; rep |
| 1963-12-14 | entered | `cal.1963-12-14.congress` | 16–17 | The White House, dinner. Johnson with Boggs, Albert Thomas, Mills, Brooks, Albert, Gerald  |
| 1963-12-18 | entered | `cal.1963-12-18.program-2` | 17–18 | Eva Adams, Director of the Mint, and the sculptor Gilroy Roberts show Mrs. Johnson a head  |
| 1963-12-21 | cited | `cal.1963-12-21.foreign-aid` | 18–19 | Mrs. Johnson, Dec. 21: Congress will not adjourn, so no flight home on Sunday; she goes to |
| 1963-12-24 | cited | `cal.1963-12-24.foreign-aid` | 19 | the House met early and passed the foreign aid bill, which released the Johnsons; not the  |
| 1963-12-24 | entered | `cal.1963-12-24.succession` | 19 | Johnson leaves Washington about 9:30 a.m., after the House passes the foreign aid bill. At |
| 1963-12-24 | entered | `cal.1963-12-24.succession-2` | 19 | Austin, the Governor's Mansion. Johnson and Mrs. Johnson see Connally, his arm in a sling, |
| 1963-12-25 | entered | `cal.1963-12-25.press-and-broadcasting-4` | 21 | The LBJ Ranch. The press at the house for a family Christmas picture; at a reporter's requ |
| 1963-12-27 | cited | `cal.1963-12-27.succession` | 22 | the press barbecue and Johnson's remarks to the gathering; not the budget) |
| 1963-12-27 | entered | `cal.1963-12-27.europe-and-the-alliance` | 21–22 | The Ranch. Rusk, Freeman, Ball, McGhee (Ambassador to Germany) and McGeorge Bundy with Joh |
| 1963-12-27 | entered | `cal.1963-12-27.press-and-broadcasting-2` | 22 | The Ranch, about 200 reporters, White House, Texas and German, by five buses. Mrs. Johnson |
| 1963-12-28 | entered | `cal.1963-12-28.europe-and-the-alliance-2` | 23–24 | Bergstrom Air Force Base, Austin. Johnson and Mrs. Johnson, Connally and his wife meet Erh |
| 1963-12-28 | entered | `cal.1963-12-28.europe-and-the-alliance-3` | 24 | The Ranch, evening. Stag dinner for Erhard and about forty of the German delegation. Gifts |
| 1963-12-29 | cited | `cal.1963-12-29.europe-and-the-alliance` | 26–27 | the barbecue and toasts; Rusk's introduction by Johnson; Mrs. Johnson does not give the br |
| 1963-12-29 | cited | `cal.1963-12-29.poverty` | 27 | Heller and Gordon at the Ranch, in and out of the meetings of Dec. 30; Lynda Bird talks ec |
| 1963-12-29 | entered | `cal.1963-12-29.europe-and-the-alliance-2` | 24–25 | Fredericksburg. Johnson and Mrs. Johnson with Erhard and the German party at the Pioneer M |
| 1963-12-29 | entered | `cal.1963-12-29.europe-and-the-alliance-3` | 25–27 | Stonewall school gymnasium, the barbecue for Erhard: the German delegation, the German, Wh |
| 1963-12-30 | cited | `cal.1963-12-30.defense` | 27 | the Joint Chiefs, led by Taylor and including LeMay and Shoup, at the Ranch in the morning |
| 1963-12-30 | entered | `cal.1963-12-30.succession` | 27–28 | Austin. Johnson and Mrs. Johnson at the funeral of Mrs. Tom Miller, widow of the mayor. |
| 1963-12-30 | entered | `cal.1963-12-30.succession-2` | 28 | Austin, dedication of the Agudas Achim Synagogue, postponed from Nov. 24. Novy introduces  |
| 1963-12-31 | entered | `cal.1963-12-31.succession` | 29 | The Ranch. Johnson goes deer hunting at dawn with Pickle and Don Thomas; later visitors fl |
| 1964-01-05 | entered | `cal.1964-01-05.elections-1964-johnson` | 30 | Austin. The Johnsons stop at the Governor's Mansion for coffee with Connally and his wife; |
| 1964-01-05 | entered | `cal.1964-01-05.press-and-broadcasting` | 29–30 | St. Barnabas Church, Fredericksburg. Johnson and Mrs. Johnson with James Reston of the *Ne |
| 1964-01-05 | entered | `cal.1964-01-05.succession` | 30–31 | Johnson and Mrs. Johnson fly from Austin to Washington with Mrs. Johnson's uncle and aunts |
| 1964-01-06 | entered | `cal.1964-01-06.white-house` | 31–32 | The White House, 6 to 7:30 p.m. Reception for the household staff, from cooks to gardeners |
| 1964-01-07 | entered | `cal.1964-01-07.economy-2` | 33 | The White House, evening. Stag dinner for the Business Council, about 89 businessmen: Blou |
| 1964-01-07 | entered | `cal.1964-01-07.labor` | 32 | The White House, 1 p.m. Johnson's stag luncheon for labor leaders. Mrs. Johnson stands in  |
| 1964-01-08 | cited | `cal.1964-01-08.program` | 34–35 | the House chamber: Mrs. Johnson in the front row with Luci and relatives; Johnson introduc |
| 1964-01-08 | entered | `cal.1964-01-08.poverty` | 35 | The White House family sitting room, about 5:30 p.m. Batt of the Area Redevelopment Admini |
| 1964-01-10 | entered | `cal.1964-01-10.white-house` | 36–37 | The Yellow Room, 4 p.m. Mrs. Johnson's tea for about sixty-five newswomen. She introduces  |
| 1964-01-11 | entered | `cal.1964-01-11.democratic-party` | 41 | The White House, 6:30 p.m. Mrs. Johnson with Johnson receives about 150 Democratic Nationa |
| 1964-01-11 | entered | `cal.1964-01-11.poverty` | 38–40 | Pennsylvania. Mrs. Johnson with Flood, McDade, Batt, Carpenter, Kilduff and about forty ne |
| 1964-01-11 | entered | `cal.1964-01-11.poverty-2` | 40–41 | Wilkes College, Wilkes-Barre. Mrs. Johnson meets students, then attends the dedication of  |
| 1964-01-11 | entered | `cal.1964-01-11.succession` | 41 | Johnson, in the receiving line, tells Mrs. Johnson to pack for Camp David in twenty minute |
| 1964-01-12 | cited | `cal.1964-01-12.civil-rights-bill-2` | 41–42 | Camp David: Johnson to church in Thurmont; Russell arrives about 11 and tells of Antietam, |
| 1964-01-12 | entered | `cal.1964-01-12.white-house` | 42 | Mrs. Johnson's television interview with Nancy Dickerson, filmed the week before, shown on |
| 1964-01-13 | entered | `cal.1964-01-13.latin-america-panama` | 44–45 | The Cabinet Room, from about 9 p.m. Johnson with Rusk, McNamara, Bundy and about fourteen  |
| 1964-01-14 | entered | `cal.1964-01-14.europe-and-the-alliance` | 45–46 | Union Station, noon. Johnson and Mrs. Johnson greet President Segni of Italy and Signora S |
| 1964-01-14 | entered | `cal.1964-01-14.europe-and-the-alliance-2` | 46–47 | The White House, State dinner for Segni. In the Yellow Room, Warren, Rusk, the Italian amb |
| 1964-01-15 | entered | `cal.1964-01-15.congress` | 49–50 | The White House, the Blue Room and State Dining Room. Mrs. Johnson receives about forty se |
| 1964-01-15 | entered | `cal.1964-01-15.europe-and-the-alliance` | 48–49 | The Italian Embassy, 1:30 p.m. Luncheon for Johnson and Mrs. Johnson's guests, the Segnis; |
| 1964-01-16 | entered | `cal.1964-01-16.congress` | 51–52 | The White House, 7 p.m. Dinner, about sixty-four guests, for the chairmen and ranking memb |
| 1964-01-16 | entered | `cal.1964-01-16.congress-2` | 52 | The White House, after dinner. Humphrey, the Fulbrights and the O'Briens stay upstairs wit |
| 1964-01-16 | entered | `cal.1964-01-16.white-house` | 49–51 | The White House, 1 p.m. Mrs. Johnson's luncheon for Senate wives and others: Mary Ellen Mo |
| 1964-01-17 | entered | `cal.1964-01-17.governors` | 54 | The White House, afternoon. Mrs. Johnson has tea with Governor Breathitt of Kentucky, newl |
| 1964-01-17 | entered | `cal.1964-01-17.white-house` | 53–54 | The White House, 11 a.m. Clifford with Mrs. Johnson on the committees Mrs. Kennedy set up  |
| 1964-01-17 | entered | `cal.1964-01-17.white-house-2` | 54 | The White House, 7:30 p.m. Dinner for the Charles Engelhards and the Mansfields, seven in  |
| 1964-01-20 | entered | `cal.1964-01-20.white-house` | 55–56 | New York. Mrs. Johnson, by commercial airline, tours the Metropolitan Museum of Art with M |
| 1964-01-20 | entered | `cal.1964-01-20.white-house-2` | 56–57 | New York. Mrs. Johnson with Fortas, Stevenson and Mary Lasker sees Arthur Miller's *After  |
| 1964-01-21 | entered | `cal.1964-01-21.economy-2` | 58–59 | The Canadian Embassy. Prime Minister Pearson's dinner in honor of Johnson and Mrs. Johnson |
| 1964-01-23 | cited | `cal.1964-01-23.baker` | 60 | Mrs. Johnson, in the evening: Johnson looks "relaxed, happy, successful, even after what m |
| 1964-01-23 | entered | `cal.1964-01-23.congress` | 59–60 | The White House, dinner at round tables in the State Dining Room, the Senate briefing. Mrs |
| 1964-01-23 | entered | `cal.1964-01-23.white-house` | 59 | The White House, 2 p.m. Mrs. Johnson with Cliff Carter of the Democratic National Committe |
| 1964-01-24 | entered | `cal.1964-01-24.white-house` | 60–61 | The Queen's Sitting Room. Clifford, Fortas, Walton, Salinger, Carpenter and Mrs. Johnson g |
| 1964-01-27 | entered | `cal.1964-01-27.cyprus` | 61–63 | The White House, 1 p.m. Luncheon for Queen Frederika of Greece and Princess Irene, with th |
| 1964-01-27 | entered | `cal.1964-01-27.white-house` | 63 | The White House, after the Queen's luncheon. Mrs. Johnson gives Mrs. Charles Lindbergh two |
| 1964-01-30 | entered | `cal.1964-01-30.congress` | 66 | The White House, the last of the Senate dinners and briefings: cocktails, the briefing for |
| 1964-02-05 | cited | `cal.1964-02-05.cuba` | 68 | Johnson leaves in the middle of the afternoon for New York and the Joseph P. Kennedy Found |
| 1964-02-05 | entered | `cal.1964-02-05.governors` | 68 | The White House, 1:30 p.m. Mrs. Johnson has tea with Mrs. Carl Sanders, wife of the Govern |
| 1964-02-05 | entered | `cal.1964-02-05.white-house` | 67–68 | The Mayflower Hotel, 7:30 a.m. Congressional wives' prayer breakfast, Mrs. Langford presid |
| 1964-02-11 | cited | `cal.1964-02-11.civil-rights-bill-2` | 70–71 | the diplomatic reception in the evening, Johnson at it until 9:30; not the talk of cloture |
| 1964-02-11 | entered | `cal.1964-02-11.white-house` | 69–71 | The White House, 7 p.m. Diplomatic reception. Mrs. Johnson and Johnson receive the Dean of |
| 1964-02-12 | cited | `cal.1964-02-12.europe-and-the-alliance` | 71 | the arrival ceremonies for the Douglas-Homes in the morning, brief speeches by the Prime M |
| 1964-02-12 | entered | `cal.1964-02-12.white-house` | 71–72 | The White House, dinner with William S. White, the columnist, and Mrs. White: his book, an |
| 1964-02-14 | entered | `cal.1964-02-14.program` | 72–73 | St. Louis. Johnson speaks at the city's bicentennial celebration. |
| 1964-02-14 | entered | `cal.1964-02-14.soviet-union` | 72 | The White House, late afternoon. Mrs. Johnson has John and Elaine Steinbeck to tea, back f |
| 1964-02-25 | entered | `cal.1964-02-25.white-house` | 73–74 | The Executive Office Building. Mrs. Johnson visits the volunteers answering mail for Mrs.  |
| 1964-02-26 | cited | `cal.1964-02-26.economy` | 74–76 | the East Room, evening, the signing before the congressional leaders; Johnson's statement  |
| 1964-02-26 | entered | `cal.1964-02-26.robert-kennedy` | 76 | Mrs. Kennedy's house, Georgetown, after the tax bill signing. Johnson and Mrs. Johnson mee |
| 1964-02-26 | entered | `cal.1964-02-26.succession` | 76–77 | Johnson and Mrs. Johnson call without notice on the Valentis in Georgetown and stay to sup |
| 1964-02-28 | entered | `cal.1964-02-28.governors` | 79–80 | The White House, about 4 p.m. Governor Connally and Mrs. Connally, in Washington, come for |
| 1964-02-28 | entered | `cal.1964-02-28.succession` | 77–78 | Palm Beach, Fla. Johnson and Mrs. Johnson pay a courtesy call on Joseph P. Kennedy, an inv |
| 1964-02-28 | entered | `cal.1964-02-28.white-house-2` | 78–79 | Georgetown, 11 a.m. Mrs. Johnson with Mrs. Kennedy: the Committee for the Preservation of  |
| 1964-03-10 | cited | `cal.1964-03-10.elections-1964` | 84 | on the plane that night, reporters bring word that Lodge, a write-in and away in Vietnam,  |
| 1964-03-10 | entered | `cal.1964-03-10.succession` | 81–82 | Washington. Mrs. Johnson leaves for Athens for the funeral of King Paul, co-chief with Tru |
| 1964-03-10 | entered | `cal.1964-03-10.succession-2` | 82–84 | Air Force One to Athens. Truman to Mrs. Johnson: the Truman Doctrine "was all the Marshall |
| 1964-03-11 | entered | `cal.1964-03-11.cyprus-2` | 85–86 | Athens. Mrs. Labouisse, at lunch, tells Mrs. Johnson of Greek politics: Karamanlis out, Ge |
| 1964-03-11 | entered | `cal.1964-03-11.cyprus-3` | 86–89 | The Royal Palace, Athens, 9 p.m. Informal supper for the funeral delegations; two of each  |
| 1964-03-11 | entered | `cal.1964-03-11.succession` | 84–85 | Athens, 8:45 a.m. Mrs. Johnson and Truman land, met by Prince Michael and the Grand Mistre |
| 1964-03-12 | entered | `cal.1964-03-12.succession` | 89–91 | Athens Cathedral. Requiem Mass for King Paul, Archbishop Chrysostomos and about fifty prel |
| 1964-03-12 | entered | `cal.1964-03-12.succession-2` | 91–94 | Tatoi, the royal summer palace. Burial of King Paul in the family cemetery; Queen Juliana  |
| 1964-03-12 | entered | `cal.1964-03-12.succession-3` | 94 | Athens, on the way back from Tatoi. Truman to Mrs. Johnson: Roosevelt picked him as runnin |
| 1964-03-12 | entered | `cal.1964-03-12.succession-4` | 94–95 | Athens, evening. The Labouisses' dinner for the American delegation and Embassy staff: Bra |
| 1964-03-19 | cited | `cal.1964-03-19.transition-and-staff` | 96 | Salinger tells Johnson in his office about 3 p.m. that he will resign to run for the Senat |
| 1964-03-19 | entered | `cal.1964-03-19.democratic-party-2` | 96–97 | The Armory. The Democratic fund-raising dinner, 5,300 present, for the Congressional Class |
| 1964-03-19 | entered | `cal.1964-03-19.transition-and-staff-2` | 96 | Johnson telephones George Reedy in the hospital and asks him to take the press secretary's |
| 1964-03-20 | entered | `cal.1964-03-20.white-house` | 97–98 | Mrs. Paul Mellon with Mrs. Johnson in the White House gardens. Mrs. Mellon proposes a plaq |
| 1964-03-24 | entered | `cal.1964-03-24.space` | 98–99 | Huntsville, Ala. Mrs. Johnson, with Carpenter and about thirty reporters, lands at the Mar |
| 1964-03-24 | entered | `cal.1964-03-24.space-3` | 99–101 | The Saturn exhibits and test stand. Mrs. Johnson, with Webb and Von Braun, tours the engin |
| 1964-03-24 | entered | `cal.1964-03-24.space-4` | 101 | The Administration Building auditorium. Mrs. Johnson presents service, invention and achie |
| 1964-04-07 | cited | `cal.1964-04-07.farm` | 101–02 | the night of the 7th, after the North Carolina reception: Johnson in the little room with  |
| 1964-04-07 | Check | `cal.1964-04-07.farm` |  | Lady Bird Johnson, 101–02, has the farm bill (with the food stamp plan) passing on the night  |
| 1964-04-08 | entered | `cal.1964-04-08.press-and-broadcasting` | 104 | Lippmann, on television for an hour: foreign aid will be hard to pass after what he says o |
| 1964-04-08 | entered | `cal.1964-04-08.succession` | 102–03 | Union Station and the Capitol. Funeral of General Douglas MacArthur. Johnson and Mrs. John |
| 1964-04-08 | entered | `cal.1964-04-08.succession-2` | 103–04 | The White House, Yellow Oval Room. Mrs. Johnson gives tea to Mrs. MacArthur, her son and t |
| 1964-04-09 | cited | `cal.1964-04-09.railroads` | 106 | the diary: Johnson, who told her at breakfast of the railroad strike due that night, has a |
| 1964-04-09 | entered | `cal.1964-04-09.succession` | 105–06 | New York Hilton. The first anniversary luncheon of the Eleanor Roosevelt Memorial Foundati |
| 1964-04-10 | entered | `cal.1964-04-10.press-and-broadcasting` | 107–08 | The Truman Balcony. Johnson takes Sandburg and Steichen out on the balcony and shouts back |
| 1964-04-10 | entered | `cal.1964-04-10.program` | 107–08 | The White House, 2:30 p.m. Mrs. Johnson receives Carl Sandburg, his wife and Edward Steich |
| 1964-04-10 | entered | `cal.1964-04-10.railroads-2` | 108 | The Cabinet Room. Johnson ushers Sandburg and Steichen in to see the railroad industry lea |
| 1964-04-10 | entered | `cal.1964-04-10.transition-and-staff` | 108–09 | The home of Mr. and Mrs. Dillon. Dinner in honor of Under Secretary Fowler and Mrs. Fowler |
| 1964-04-14 | entered | `cal.1964-04-14.consumers` | 109–10 | The Department of Agriculture. Mrs. Johnson opens the Food and Home Fair for Consumers, Ja |
| 1964-04-14 | entered | `cal.1964-04-14.middle-east-2` | 109 | The White House, 11:30 a.m. King Hussein of Jordan arrives by helicopter on the South Lawn |
| 1964-04-14 | entered | `cal.1964-04-14.middle-east-3` | 110–12 | The White House, State dinner for King Hussein, about 150 guests. In the Yellow Oval Room, |
| 1964-04-14 | entered | `cal.1964-04-14.white-house` | 110 | The Senate Ladies Red Cross Luncheon in Mrs. Johnson's honor, her first as guest after fif |
| 1964-04-16 | entered | `cal.1964-04-16.program` | 112–13 | The White House, dinner. Barbara Ward (Lady Jackson), staying on the third floor, and Dr.  |
| 1964-04-16 | entered | `cal.1964-04-16.white-house` | 112 | The White House, afternoon. Johnson brings some forty Texas newspaper editors and their wi |
| 1964-04-17 | entered | `cal.1964-04-17.press-and-broadcasting` | 113–14 | The Rose Garden and South Lawn, 5:30 p.m. Reception for the American Society of Newspaper  |
| 1964-04-19 | entered | `cal.1964-04-19.white-house` | 114–15 | Johnson and Mrs. Johnson to St. Mark's Church with Dillon and Mrs. Dillon and Stevenson, w |
| 1964-04-22 | cited | `cal.1964-04-22.railroads` | 116–17 | Johnson comes out of the elevator with the men for the Yellow Room, about twenty, among th |
| 1964-04-22 | entered | `cal.1964-04-22.white-house` | 115–16 | The White House, 4 p.m. Mrs. Johnson receives about 200 Daughters of the American Revoluti |
| 1964-04-22 | entered | `cal.1964-04-22.white-house-2` | 116 | The White House. Mrs. Johnson with Boisfeuillet Jones of Health, Education and Welfare, Ca |
| 1964-04-24 | cited | `cal.1964-04-24.poverty` | 117–23 | the five-State day: South Bend, Pittsburgh, Inez and Paintsville, Huntington; the Cabinet  |
| 1964-04-24 | entered | `cal.1964-04-24.poverty-2` | 117–19 | South Bend, Ind., 8:45 a.m. Johnson and Mrs. Johnson land at the Cline School playground b |
| 1964-04-24 | entered | `cal.1964-04-24.poverty-3` | 119 | Pittsburgh, the League of Women Voters' convention, 1,300 delegates; Wirtz was to speak an |
| 1964-04-24 | entered | `cal.1964-04-24.poverty-4` | 119–20 | Pittsburgh. Motorcade to David McDonald Hall, the Steelworkers' home local, a quarter of a |
| 1964-04-24 | entered | `cal.1964-04-24.poverty-5` | 120–22 | Inez, Martin County, Ky. Johnson and Mrs. Johnson at the three-room tarpaper house of Tom  |
| 1964-04-24 | entered | `cal.1964-04-24.poverty-6` | 122 | Paintsville, Ky. The Mayo State Vocational School, then Johnson's speech at the courthouse |
| 1964-04-24 | entered | `cal.1964-04-24.poverty-7` | 122–23 | Huntington, W. Va., after 6 p.m. Johnson on the plane with the Governors of the Appalachia |
| 1964-04-25 | entered | `cal.1964-04-25.succession` | 123–24 | The White House, morning. Johnson holds a brief press conference in his office, 60 to 70 r |
| 1964-04-25 | entered | `cal.1964-04-25.succession-2` | 124 | The White House, lunch after 2 p.m. Johnson with Truman, Dobie and the editors Walker Ston |
| 1964-04-25 | entered | `cal.1964-04-25.succession-3` | 124–25 | The Gridiron Dinner, Washington. Johnson attends in white tie, a stag dinner; Dobie goes w |
| 1964-04-27 | entered | `cal.1964-04-27.labor` | 127 | The White House. Johnson's impromptu reception for labor newspaper editors, nominally stag |
| 1964-04-27 | entered | `cal.1964-04-27.south-asia` | 125 | The White House, 11 a.m. Mrs. Johnson has coffee with Indira Gandhi, Mrs. Avtar Dhar of th |
| 1964-04-27 | entered | `cal.1964-04-27.white-house` | 125–27 | Georgetown. Mrs. Johnson asks Mrs. Kennedy to attend the meeting of the Committee for the  |
| 1964-04-28 | entered | `cal.1964-04-28.program` | 127–28 | The White House, black-tie dinner for business leaders. Batten of J. C. Penney, Blough of  |
| 1964-04-30 | entered | `cal.1964-04-30.democratic-party` | 130 | The Sheraton Park, evening. Johnson addresses the Democratic Women's Conference, 3,000, Ma |
| 1964-04-30 | entered | `cal.1964-04-30.japan-and-korea-far-east` | 130 | The White House, Blue Room. Mrs. Johnson, at the State Department's request, receives elev |
| 1964-04-30 | entered | `cal.1964-04-30.program-2` | 129–30 | Winchester, Va. Johnson drives to the Shenandoah Apple Blossom Festival, unannounced to Mr |
| 1964-04-30 | entered | `cal.1964-04-30.white-house` | 128–29 | The Sheraton Park, the Congressional Club's annual breakfast in honor of the First Lady, a |
| 1964-05-06 | cited | `cal.1964-05-06.press-and-broadcasting` | 132–33 | the South grounds, 4:30 p.m.: Johnson in the band shell answering questions on the gross n |
| 1964-05-06 | entered | `cal.1964-05-06.white-house` | 130–32 | The White House, 1 p.m. Mrs. Johnson's luncheon for the Senate Ladies Red Cross unit, 130  |
| 1964-05-06 | entered | `cal.1964-05-06.white-house-2` | 133 | Alice Brown, wife of George Brown of Houston, arrives as a White House guest with a Winslo |
| 1964-05-07 | cited | `cal.1964-05-07.poverty` | 134 | Johnson and Lynda Bird leave by helicopter for Andrews that morning for a five-State pover |
| 1964-05-07 | entered | `cal.1964-05-07.white-house` | 134 | The Yellow Oval Room, 10:30 a.m. First meeting under Mrs. Johnson of the Committee for the |
| 1964-05-07 | entered | `cal.1964-05-07.white-house-2` | 135–36 | The Green Room and Blue Room, 4 p.m. Mrs. Johnson's tea for about fifty-five people of the |
| 1964-05-14 | cited | `cal.1964-05-14.elections-1964` | 138–40 | the memorandum, nine pages, with a draft announcement of withdrawal, the alternatives, and |
| 1964-05-14 | Check | `cal.1964-05-14.elections-1964` |  | Lady Bird Johnson, 138–40, writes of the memorandum that she wrote it at Huntland, Middleburg |
| 1964-05-14 | entered | `cal.1964-05-14.elections-1964-johnson` | 138–40 | Huntland, Middleburg, Va. Mrs. Johnson has Dr. Hurst and Dr. James Cain of the Mayo Clinic |
| 1964-05-14 | entered | `cal.1964-05-14.elections-1964-johnson-2` | 140 | A little after midnight Johnson, back from a stag party, telephones Mrs. Johnson at Huntla |
| 1964-05-15 | entered | `cal.1964-05-15.elections-1964-johnson` | 138–40 | The White House. Dr. Hurst and Dr. James Cain meet with Dr. Larry Lamb of San Antonio and  |
| 1964-05-21 | entered | `cal.1964-05-21.poverty` | 140–41 | Kentucky. Mrs. Johnson, with Carpenter, Bess Abell, Representative Perkins, Batt of the A. |
| 1964-05-21 | entered | `cal.1964-05-21.poverty-2` | 141–42 | Warshoal Branch, Breathitt County, Ky. Mrs. Johnson walks a mile up the creek to the three |
| 1964-05-21 | entered | `cal.1964-05-21.poverty-3` | 142–44 | Lick Branch School, Breathitt County. Mrs. Johnson lunches with the 25 children of the one |
| 1964-05-21 | entered | `cal.1964-05-21.poverty-4` | 144 | Breathitt High School, Jackson, Ky. Mrs. Johnson makes her first speech of the day to abou |
| 1964-05-23 | cited | `cal.1964-05-23.europe-and-the-alliance` | 144–46 | Lexington, Va.: Johnson and Mrs. Johnson with Acheson, Rusk and Byrd; the cadets; the visi |
| 1964-05-23 | entered | `cal.1964-05-23.program` | 145 | Lexington, Va. Johnson inspects the V.M.I. cadets; he and Mrs. Johnson visit the Marshall  |
| 1964-05-25 | entered | `cal.1964-05-25.white-house` | 146–48 | New York, Museum of Modern Art, evening. Dinner for 400 at the opening of the new wing, at |
| 1964-05-25 | entered | `cal.1964-05-25.white-house-2` | 148 | New York, Waldorf Towers. Stevenson's party after the opening: Richard Rodgers, Marc Conne |
| 1964-05-27 | cited | `cal.1964-05-27.india-and-china` | 148 | the news of Nehru's death at about 6 a.m.; Rusk left at dawn for the funeral) |
| 1964-05-27 | entered | `cal.1964-05-27.europe-and-the-alliance` | 148–49 | The South Lawn. Johnson and Mrs. Johnson receive President de Valera of Ireland: the Diplo |
| 1964-05-27 | entered | `cal.1964-05-27.europe-and-the-alliance-2` | 149–50 | The White House, State dinner for de Valera. Gifts: a vermeil cigar box, an antique ballot |
| 1964-06-04 | entered | `cal.1964-06-04.elections-1964-johnson` | 154 | The Senate caucus room. Rally forming Young Citizens for Johnson, Bayh and Marvella Bayh t |
| 1964-06-04 | entered | `cal.1964-06-04.white-house` | 151–53 | The East Room, 5 p.m. Mark Bortman of Boston, who headed the People-to-People program, pre |
| 1964-06-04 | entered | `cal.1964-06-04.white-house-2` | 153 | The home of Max Freedman, Washington. Johnson and Mrs. Johnson at a birthday supper for Bi |
| 1964-06-05 | cited | `cal.1964-06-05.middle-east` | 155 | the State luncheon at the White House for the Shah and the Empress Farah, Mrs. Johnson on  |
| 1964-06-05 | entered | `cal.1964-06-05.middle-east-2` | 154–55 | National Cathedral. Memorial service for Nehru, Johnson and Mrs. Johnson attending with Ru |
| 1964-06-05 | entered | `cal.1964-06-05.program` | 155–57 | The White House. Dinner for John and Elaine Steinbeck. Steinbeck on Russia: the Russians'  |
| 1964-06-06 | cited | `cal.1964-06-06.laos` | 157–58 | the telephone call from McGeorge Bundy at 4:30 a.m. that one of the reconnaissance planes  |
| 1964-06-06 | entered | `cal.1964-06-06.laos-2` | 158 | Johnson in the White House hall to Mrs. Johnson, after a morning of Laos and Vietnam: "We' |
| 1964-06-09 | entered | `cal.1964-06-09.europe-and-the-alliance` | 160–62 | The White House, State dinner-dance for Prime Minister Jens Otto Krag of Denmark and Mrs.  |
| 1964-06-09 | entered | `cal.1964-06-09.program` | 158–60 | Cambridge, Mass. Mrs. Johnson gives the baccalaureate address at Radcliffe, in the Memoria |
| 1964-06-09 | entered | `cal.1964-06-09.program-2` | 160 | Cambridge. Mrs. Johnson, with Mrs. Peabody and Mrs. John Collins, walks the site on the Ch |
| 1964-06-10 | entered | `cal.1964-06-10.program` | 162–64 | The East Room, 5:30 p.m. Johnson presents the Presidential Scholars' medals to 121 student |
| 1964-06-10 | entered | `cal.1964-06-10.program-2` | 164–65 | The White House. The Presidential Scholars' reception with invited artists and scientists, |
| 1964-06-10 | entered | `cal.1964-06-10.robert-kennedy` | 164–65 | The South Lawn. Johnson, who has been in the West Wing in a Southeast Asia briefing with C |
| 1964-06-11 | entered | `cal.1964-06-11.elections-1964-johnson` | 165–66 | Johnson, by Mrs. Johnson's account, wants her help to get out of the race; the cloture vot |
| 1964-06-14 | entered | `cal.1964-06-14.elections-1964-johnson` | 166–67 | Afternoon. Johnson to Mrs. Johnson: the next five months, with Vietnam, Laos and Cyprus, a |
| 1964-06-14 | entered | `cal.1964-06-14.succession` | 166 | Johnson and Mrs. Johnson to the National City Christian Church with Secretary Hodges, Mrs. |
| 1964-06-14 | entered | `cal.1964-06-14.vietnam` | 167 | About 8:30 p.m. Johnson telephones Rusk at his office; Rusk brings a wire from Lodge askin |
| 1964-06-15 | entered | `cal.1964-06-15.elections-1964-johnson` | 167–68 | The White House, dinner with Joseph Alsop and Mrs. Alsop and Clifford and Mrs. Clifford. W |
| 1964-06-15 | entered | `cal.1964-06-15.succession` | 167 | The White House. Mrs. Johnson is interviewed for two hours by William Manchester, whom Mrs |
| 1964-06-16 | cited | `cal.1964-06-16.vietnam-2` | 167 | Johnson asking, if Lodge resigned, "Whom do you recommend?" of Bundy, McNamara and Rusk; t |
| 1964-06-16 | entered | `cal.1964-06-16.cities-and-housing` | 169–70 | The White House, Mrs. Johnson's Women Do-ers luncheon, with Jane Jacobs, author of *The De |
| 1964-06-16 | entered | `cal.1964-06-16.civil-rights-the-executive` | 171–72 | New York, the car in from the St. Regis, Johnson and Mrs. Johnson with Warren and Robert K |
| 1964-06-16 | entered | `cal.1964-06-16.robert-kennedy` | 170–71 | New York, the St. Regis. Dinner for 300 given by Stephen Smith and the trustees of the Ken |
| 1964-06-20 | entered | `cal.1964-06-20.civil-rights-bill` | 173 | Boggs, who comes over to see Mrs. Johnson, says the House has set July 4 as the day for pa |
| 1964-06-20 | entered | `cal.1964-06-20.congress` | 172 | Mrs. Johnson telephones Rose Kennedy and the Northampton hospital about Edward Kennedy's p |
| 1964-07-02 | cited | `cal.1964-07-02.civil-rights-bill` | 173–74 | the news of the House vote, 289 to 126, mid-afternoon; the signing in the East Room at 6:3 |
| 1964-07-02 | entered | `cal.1964-07-02.succession` | 174–75 | Johnson telephones Mrs. Johnson, as though the thought had just come to him: "We might jus |
| 1964-07-06 | entered | `cal.1964-07-06.elections-1964-johnson` | 175 | Scharnhorst Ranch. Johnson with Mrs. Johnson, Jesse Kellam and A. W. Moursund on whether h |
| 1964-07-11 | entered | `cal.1964-07-11.elections-1964-johnson-2` | 176 | The White House, the weekend. Johnson "is going through the throes of what may be the last |
| 1964-07-13 | entered | `cal.1964-07-13.elections-1964-johnson` | 177 | The White House, small room off the Oval Office, until nearly 11 p.m. Johnson with O'Donne |
| 1964-07-15 | entered | `cal.1964-07-15.elections-1964-johnson` | 178 | The White House, after midnight. Johnson watches the Republican convention on television w |
| 1964-07-16 | entered | `cal.1964-07-16.elections-1964-johnson` | 178 | The White House, 9 a.m. Galbraith to breakfast with Johnson and Mrs. Johnson, two hours. H |
| 1964-07-16 | entered | `cal.1964-07-16.program` | 179–80 | The Yellow Room, late afternoon. James Roosevelt and his daughter Anna with Mrs. Johnson.  |
| 1964-07-17 | entered | `cal.1964-07-17.elections-1964-johnson` | 182–83 | Kansas City, the Muehlebach Hotel, about 6:30 p.m. Truman and Mrs. Truman have drinks with |
| 1964-07-17 | entered | `cal.1964-07-17.program` | 180–82 | Independence, Mo. Mrs. Johnson and Lynda Bird, on a trip promised her by Truman on the fli |
| 1964-07-17 | entered | `cal.1964-07-17.white-house` | 180 | The White House. Mrs. Johnson presents the one millionth copy of the White House guidebook |
| 1964-07-24 | cited | `cal.1964-07-24.elections-1964` | 183–84 | the afternoon: Johnson's televised press conference at 3:30, which Mrs. Johnson watched fr |
| 1964-07-24 | entered | `cal.1964-07-24.elections-1964-vice-presidency` | 184 | The White House, the small room off the Oval Office, evening. Johnson with staff discussin |
| 1964-07-24 | entered | `cal.1964-07-24.labor` | 183–84 | The Mansion, after the press conference. Johnson's reception for 250 to 300 labor leaders, |
| 1964-07-26 | cited | `cal.1964-07-26.vietnam-congress` | 185 | the evening dinner at the Fulbrights', with the Restons, the Dillons and Russell; Mrs. Joh |
| 1964-07-26 | entered | `cal.1964-07-26.elections-1964-2` | 185 | Washington. Johnson and Mrs. Johnson at the Fulbrights' for dinner, with the Restons, the  |
| 1964-07-26 | entered | `cal.1964-07-26.elections-1964-3` | 185 | Johnson and Mrs. Johnson walk the grounds after church; at the gates Johnson invites about |
| 1964-08-01 | entered | `cal.1964-08-01.states-and-cities` | 186–87 | The White House, dinner for Mayor Wagner, his sons and Celebrezze and Wirtz with their wiv |
| 1964-08-01 | entered | `cal.1964-08-01.succession` | 186 | Fort Myer Chapel. Memorial service for Senator Clair Engle, the Senate Chaplain officiatin |
| 1964-08-04 | cited | `cal.1964-08-04.vietnam-congress-2` | 187–88 | Tuesday evening, cars through the Southwest Gate; Johnson an hour and a half with congress |
| 1964-08-04 | entered | `cal.1964-08-04.vietnam-tonkin-10` | 188 | Evening. Johnson delays his statement on the second attack on the destroyers in the Gulf o |
| 1964-08-04 | entered | `cal.1964-08-04.vietnam-tonkin-11` | 188–89 | After 11 p.m., after word from the Defense Department that the planes had been launched an |
| 1964-08-04 | entered | `cal.1964-08-04.vietnam-tonkin-9` | 187–88 | The White House, the regular Tuesday lunch of Johnson with the Secretary of Defense, the S |
| 1964-08-06 | cited | `cal.1964-08-06.vietnam-2` | 189–90 | the welcoming ceremony a little past 11 in the Rose Garden, without military pomp; U Thant |
| 1964-08-06 | entered | `cal.1964-08-06.civil-disorders` | 189 | The White House bedroom, morning. Mayor Daley of Chicago with Johnson in bed and Mrs. John |
| 1964-08-06 | entered | `cal.1964-08-06.europe-and-the-alliance` | 190–91 | The White House, State dinner for U Thant. Gifts: moon photographs from Ranger VII and an  |
| 1964-08-06 | entered | `cal.1964-08-06.governors` | 190 | Governor and Mrs. Pat Brown of California, the John Daltons of Missouri and the Matthew We |
| 1964-08-25 | entered | `cal.1964-08-25.elections-1964-johnson` | 192 | Johnson lunches with Rusk, McNamara and Bundy at about one, then sits alone in his room wi |
| 1964-08-25 | entered | `cal.1964-08-25.elections-1964-johnson-2` | 192 | That afternoon Mrs. Johnson, after a long talk with Lynda Bird on the South grounds, write |
| 1964-09 | cited | `cal.1964-09.elections-1964-5` | 195–98 | Sept. 11: Mrs. Johnson's telephone calls to the Governors and Senators of the States on th |
| 1964-09 | Check | `cal.1964-09.elections-1964-5` |  | Lady Bird Johnson, 195–98, dates the calls Friday, Sept. 11, 1964, and has Byrd say that beca |
| 1964-09-04 | entered | `cal.1964-09-04.elections-1964-johnson` | 194 | The White House, 11:30 a.m., three hours. Mrs. Johnson with Carpenter, Bess Abell, Scooter |
| 1964-09-04 | entered | `cal.1964-09-04.elections-1964-vice-presidency` | 193–94 | The White House. Abigail McCarthy, wife of Senator Eugene McCarthy, comes for coffee with  |
| 1964-09-11 | entered | `cal.1964-09-11.elections-1964-johnson` | 197–98 | The Yellow Oval Room, afternoon. Mrs. Johnson has the Cabinet wives to tea, Mrs. Rusk, Mrs |
| 1964-10-06 | cited | `cal.1964-10-06.elections-1964` | 198–99 | the whistle-stop through the South, "forty-seven stops in four days"; a woman at a North C |
| 1964-11-14 | entered | `cal.1964-11-14.poverty` | 199–200 | The LBJ Ranch. Celebrezze and Wirtz confer with Johnson in the morning, the fifth and sixt |
| 1964-11-14 | entered | `cal.1964-11-14.transition-and-staff-cabinet` | 200 | The Ranch, arrivals from New York: Frank Stanton of C.B.S., Donald Cook of American Electr |
| 1964-11-15 | entered | `cal.1964-11-15.succession` | 202–03 | The White House lawn, 6:30 p.m. Johnson and Mrs. Johnson return from Texas, their first si |
| 1964-11-15 | entered | `cal.1964-11-15.transition-and-staff` | 203 | The State Department, evening. Party for Walter Heller, who leaves the Council of Economic |
| 1964-11-15 | entered | `cal.1964-11-15.transition-and-staff-2` | 203 | Later that evening Johnson meets some of the staff on a talent search for the best people  |
| 1964-11-15 | entered | `cal.1964-11-15.transition-and-staff-cabinet` | 201–02 | The Ranch, breakfast. Johnson asks Watson to be Secretary of Commerce in place of Hodges;  |
| 1964-11-17 | entered | `cal.1964-11-17.program` | 205 | The White House second floor. Mary Lasker with Mrs. Johnson on giving the Inaugural ceremo |
| 1964-11-17 | entered | `cal.1964-11-17.transition-and-staff` | 204 | Mrs. Johnson calls on Walter Jenkins and Mrs. Jenkins, who are going home to Texas. Jenkin |
| 1964-11-17 | entered | `cal.1964-11-17.transition-and-staff-2` | 205 | The State Department, farewell reception for Ralph Dungan, leaving to be Ambassador to Chi |
| 1964-11-17 | entered | `cal.1964-11-17.white-house` | 205–07 | The White House, 9 p.m. Johnson's surprise party for Mrs. Johnson's thirtieth wedding anni |
| 1964-11-21 | entered | `cal.1964-11-21.farm` | 206–08 | The LBJ Ranch. Richard Juhl and a party of eleven from Iowa, including the presidents of t |
| 1964-11-21 | entered | `cal.1964-11-21.farm-2` | 208–09 | The Ranch, lunch. Freeman to Mrs. Johnson on why the Department of Agriculture grows while |
## Passed over (the card's ground, Q5, unless another is named)

Family and social matters with nothing done or said of public business: Nov. 24, Lynda Bird summoned for the funeral (10); Dec. 14, Luci's midshipman guest (16); Dec. 18, the third-floor school (18); Dec. 23, the mourning crepe removed (19); Dec. 24–25, the Ranch's guards and Christmas with the kin (20–21); Dec. 27, the hunting tower with the Connallys (22–23); Dec. 30–31, Lynda Bird and Heller by the fire, the family day (29); Jan. 5–7, Mrs. Johnson's relatives (31–33); Jan. 15, her talk with West on 2 a.m. suppers and the yellow sofas, and Time on Connally (48–50: household); Jan. 16, Luci's school (51); Jan. 21, buying clothes with Marcus (58); Jan. 30, tea with Alice Roosevelt Longworth, reminiscence only (64–65); Feb. 5, her correspondence staff, Moursund on the house and ranches, Jason Robards on television (68–69); Feb. 14, the Heart Luncheon, unspecified, and Mary Lasker's night (72–73); Feb. 25, the household expenses with Jenkins and West, a staff meeting (74); Mar. 19, Lynda Bird's birthday (95); Mar. 24, lunch with fifty-eight kin (100); Apr. 14, her income tax (110); Apr. 19 and 27, the end of Lynda Bird's engagement (115, 127); Apr. 25, Mrs. Dobie's tour (125); Apr. 28, her Women Do-ers luncheon, no content given (127); May 14, a walk with Luci (137); June 6, work on her Radcliffe speech with Mrs. Provenson, a draft of her own (158); June 10, Dorris Powell as houseguest (165); June 14–16, Lynda Bird's Hawaii trip (169); July 2, Luci's birthday and the heart-attack anniversary (173); July 13, 15 and 16, the grounds' trees, West Side Story, the tree Johnson will plant (176–79); July 24, Luci at Interlochen, bowling (184); Aug. 1, a book on Wilson (186); Sept. 4, Luci's ship, dinner with Pickle and Birdwell (194); Nov. 15, Luci's instruction in the Catholic Church, Lynda Bird and the University of Texas (203–04); Nov. 21, the Ranch decoration (206–09).

Preparations and covering matter: Jan. 13, Adler and Meloy on the Segni dinner and the fabrics with Mrs. Monroney and Mrs. Clifford (43–44); May 25, the call to Mary Lasker on her speech (146); Mrs. Johnson's own drafts and fittings.

Undated even to the month, a lead: "Late August," pp. 191: Idaho, Utah, Wyoming, Maine and Vermont; visits of Connally, Billy Graham, Cain and Hurst; television with Cronkite and Howard K. Smith.

## Rulings that took a Check

`cal.1963-12-07.economy-2` (the eighty-nine businessmen, 33, the evening of Jan. 7, 1964; the entry Dec. 7, 1963); `cal.1964-04-07.farm` (the farm bill "passed" the night of Apr. 7, 101–02; the votes Apr. 8); `cal.1964-05-14.elections-1964` (Mrs. Johnson's memorandum: Huntland, nine pages, a draft of withdrawal; "at his asking" is not in the diary, 138–40); `cal.1964-09.elections-1964-5` (the calls dated Sept. 11, Byrd's refusal given a reason, 195–98). Entered with a Check of their own: Feb. 28 (the Palm Beach visit, a day before), May 14–15 (the night call, the doctors' meeting), June 4 (the rally, "yesterday" in a June 5 entry), Aug. 4 (the hour of the statement), Sept. 4 (the heading's day).

## Where batch 11 stopped

The share is finished: Book One read whole, Nov. 22, 1963 through Nov. 21, 1964 (printed pp. 3–209, PDF 17–231); the diary has nothing later in 1964. Not done: the image check of every quoted word and number (above, Limits).


# Part three: 1966 (the 1966 reader)

Lady Bird Johnson, *A White House Diary* (1970), card `w.johnson-white-house-diary`. Read Nov. 11–12, 2026 (batch 11, the 1966 share): Book Three, "1966," printed pp. 345–465, from the owner's copy, Drive `1yDhieBtd5zcvoMYqrteT6Yg3a-R6sOie` (864 PDF pages, a text layer, no OCR; read with `pdftotext -layout`; the PDF and its page images deleted when done).

**Offset.** The folio is printed at the foot of the page. Printed page = PDF page less 30 from the half-title of Book Three through p. 406 (p. 345 = PDF 375; p. 347 = PDF 377; p. 354 = PDF 384; p. 369 = PDF 399; p. 392 = PDF 422; p. 406 = PDF 436); eight unnumbered plate pages follow (PDF 437–444: the State of the Union, Hains Point, the Oval Office, Mrs. Gandhi's gifts, the honeymoon departure, the Far East trip), then less 38 (p. 407 = PDF 445; p. 417 = PDF 455; p. 459 = PDF 497; p. 465 = PDF 503). Checked on the folios in the text layer throughout and against the page images at pp. 347, 354, 369, 392 and 459: every quotation and number on those pages read off the image and found as in the text layer; the quotations elsewhere were matched by a script against the text layer (the only differences: nested quotation marks, line-end hyphens, the OCR's "Your husband is.a passionate man"). Book Three runs from Jan. 1 (p. 345) to Dec. 24 (p. 465); the diary has long gaps (Feb. 25 to Mar. 3, Apr. 19 to June 4, Aug. 6 to Aug. 20, Oct. 6 to Oct. 20, Nov. 2 to Nov. 17, Dec. 1 to Dec. 13), no entry for Nov. 1, and none after Dec. 24.

**Share (batch 11).** Book Three, 1966, every page (pp. 345–465).

**Patch.** `inbox/2026-11-12-b11-ladybird-1966.yaml` (patch `2026-11-12-b11-ladybird-1966`): 80 new entries (ids claimed in the ledger first), 33 `cite` ops, 5 `check` ops, no `variant` (the entries cited have no claim maps). `./bib patch-check`: 0 errors; the warnings are "one event?" and "a duplicate of ..." on new entries that share a day and thread with another and are distinct events (the Jan. 3, Mar. 17, June 28, July 23, Sept. 1, 5 and 21, Oct. 25 pairs and runs); `./bib resolve ID --take keep` settles each if the merge flags it. A claim dropped: `cal.1966-06-13.opinion-3` (the Gallup 46 percent is `cal.1966-06-04.opinion`, cited there; the line stays in the ledger, "not used").

**Form.** The diary is Mrs. Johnson's account: every `n` says so; a private act on a record nobody saw then carries "Made public: 1970." Her words, and what she gives as Johnson's or another's, are in quotation marks; her inferences are hers ("the decision had been reached," June 28). The day is the diary's; where she writes "yesterday" or "last night" the entry takes that day (Jan. 11, June 3, Sept. 20). Persons are listed in `Names:` only where `c` names them or their office; the hidden `name:` tags follow the act.

## Entered (new)

| Day | Entry | Page |
|---|---|---|
| Jan. 1 | `cal.1966-01-01.vietnam-pause` | 345 |
| Jan. 3 | `cal.1966-01-03.vietnam-pause-4` | 347 |
| Jan. 5 | `cal.1966-01-05.press-and-broadcasting` | 348–49 |
| Jan. 5 | `cal.1966-01-05.steel` | 347 |
| Jan. 7 | `cal.1966-01-07.peace-corps` | 349 |
| Jan. 11 | `cal.1966-01-11.conservation` | 349–50 |
| Jan. 11 | `cal.1966-01-11.elections-1968-johnson` | 349 |
| Jan. 11 | `cal.1966-01-11.program-2` | 351 |
| Jan. 11 | `cal.1966-01-11.white-house` | 350 |
| Jan. 12 | `cal.1966-01-12.conservation` | 350–52 |
| Jan. 18 | `cal.1966-01-18.program` | 353–54 |
| Jan. 23 | `cal.1966-01-23.press-and-broadcasting` | 355 |
| Jan. 23 | `cal.1966-01-23.program` | 355 |
| Jan. 23 | `cal.1966-01-23.white-house` | 354–55 |
| Feb. 5 | `cal.1966-02-05.vietnam-honolulu` | 359 |
| Feb. 13 | `cal.1966-02-13.vietnam-support` | 359–60 |
| Feb. 20 | `cal.1966-02-20.vietnam-support` | 361–62 |
| Feb. 20 | `cal.1966-02-20.white-house` | 360–61 |
| Feb. 25 | `cal.1966-02-25.congress` | 366 |
| Feb. 25 | `cal.1966-02-25.women` | 363–66 |
| Mar. 3 | `cal.1966-03-03.congress` | 368–69 |
| Mar. 10 | `cal.1966-03-10.congress` | 369 |
| Mar. 10 | `cal.1966-03-10.program` | 369–70 |
| Mar. 10 | `cal.1966-03-10.white-house` | 369 |
| Mar. 11 | `cal.1966-03-11.vietnam-pacification` | 370–71 |
| Mar. 17 | `cal.1966-03-17.congress` | 373 |
| Mar. 17 | `cal.1966-03-17.program` | 372–73 |
| Mar. 17 | `cal.1966-03-17.program-2` | 373–74 |
| Apr. 2 | `cal.1966-04-02.conservation` | 376–80 |
| Apr. 3 | `cal.1966-04-03.conservation` | 380–83 |
| Apr. 13 | `cal.1966-04-13.conservation` | the plates after 406 |
| Apr. 19 | `cal.1966-04-19.democratic-party` | 383–85 |
| June 3 | `cal.1966-06-03.program` | 386 |
| June 4 | `cal.1966-06-04.elections-1966` | 386 |
| June 28 | `cal.1966-06-28.conservation` | 390 |
| June 28 | `cal.1966-06-28.conservation-2` | 390 |
| July 13 | `cal.1966-07-13.program` | 391–92 |
| July 13 | `cal.1966-07-13.vietnam-support` | 393 |
| July 13 | `cal.1966-07-13.white-house` | 392–93 |
| July 20 | `cal.1966-07-20.elections-1968-johnson` | 395 |
| July 20 | `cal.1966-07-20.governors` | 396 |
| July 20 | `cal.1966-07-20.latin-america` | 396 |
| July 20 | `cal.1966-07-20.program` | 396 |
| July 20 | `cal.1966-07-20.war-opposition` | 395–96 |
| July 23 | `cal.1966-07-23.conservation` | 398 |
| July 23 | `cal.1966-07-23.vietnam-support` | 396–97 |
| July 23 | `cal.1966-07-23.vietnam-support-2` | 397 |
| July 23 | `cal.1966-07-23.vietnam-support-3` | 398 |
| July 23 | `cal.1966-07-23.vietnam-support-4` | 397–98 |
| Aug. 1 | `cal.1966-08-01.jobs-and-wages-airlines` | 400, 402 |
| Aug. 2 | `cal.1966-08-02.middle-east` | 402–04 |
| Aug. 20 | `cal.1966-08-20.conservation` | 413–14 |
| Aug. 20 | `cal.1966-08-20.economy` | 414 |
| Aug. 20 | `cal.1966-08-20.program` | 414 |
| Aug. 20 | `cal.1966-08-20.vietnam-support` | 413 |
| Aug. 27 | `cal.1966-08-27.press-and-broadcasting` | 415–16 |
| Sept. 1 | `cal.1966-09-01.economy-investment-credit` | 417 |
| Sept. 1 | `cal.1966-09-01.economy-investment-credit-2` | 418 |
| Sept. 5 | `cal.1966-09-05.elections-1966` | 420 |
| Sept. 5 | `cal.1966-09-05.elections-1966-2` | 420–21 |
| Sept. 5 | `cal.1966-09-05.health` | 419–20 |
| Sept. 5 | `cal.1966-09-05.vietnam-support` | 418–19 |
| Sept. 7 | `cal.1966-09-07.soviet-union` | 421–23 |
| Sept. 20 | `cal.1966-09-20.conservation` | 423 |
| Sept. 21 | `cal.1966-09-21.conservation` | 423–25 |
| Sept. 21 | `cal.1966-09-21.conservation-2` | 425 |
| Sept. 21 | `cal.1966-09-21.conservation-3` | 426–27 |
| Sept. 23 | `cal.1966-09-23.poverty` | 427–28 |
| Oct. 25 | `cal.1966-10-25.vietnam-asian-trip-2` | 432–34 |
| Oct. 25 | `cal.1966-10-25.vietnam-asian-trip-3` | 434–35 |
| Oct. 27 | `cal.1966-10-27.succession` | 436 |
| Nov. 17 | `cal.1966-11-17.economy` | 454 |
| Nov. 17 | `cal.1966-11-17.press-and-broadcasting` | 454–55 |
| Nov. 17 | `cal.1966-11-17.succession` | 454 |
| Nov. 28 | `cal.1966-11-28.white-house` | 455–58 |
| Dec. 1 | `cal.1966-12-01.conservation` | 458 |
| Dec. 1 | `cal.1966-12-01.program` | 458–60 |
| Dec. 13 | `cal.1966-12-13.program` | 460–62 |
| Dec. 16 | `cal.1966-12-16.vietnam-diplomacy` | 463–64 |
| Dec. 24 | `cal.1966-12-24.vietnam-support` | 464–65 |

## Cited (the card) and what the page bears

Each `cite` has units `?`; the parenthetical says what the page bears and what it does not.

| Entry | Page |
|---|---|
| `cal.1966-01.steel` | 347–48 |
| `cal.1966-01-12.program` | 351–52 |
| `cal.1966-01-17.cities-and-housing` | 352–53 |
| `cal.1966-02-06.vietnam` | 358–59 |
| `cal.1966-02-20.vietnam-2` | 361 |
| `cal.1966-03-12.vietnam-us` | 371 |
| `cal.1966-03-12.press-and-broadcasting` | 371 |
| `cal.1966-03-13.vietnam` | 371–72 |
| `cal.1966-03-28.india-and-china` | 374–76 |
| `cal.1966-06-04.opinion` | 388–89 |
| `cal.1966-06-28.vietnam-congress-4` | 390–91 |
| `cal.1966-06-29.vietnam-air-war` | 391 |
| `cal.1966-07-20.vietnam-prisoners` | 396 |
| `cal.1966-07-23.vietnam-2` | 397 |
| `cal.1966-07-23.civil-disorders` | 397, 398–99 |
| `cal.1966-08-06.war-opposition-2` | 409 |
| `cal.1966-08-06.transition-and-staff` | 407 |
| `cal.1966-08-20.open-housing-2` | 411–12 |
| `cal.1966-08-31.europe-and-the-alliance` | 417 |
| `cal.1966-09-21.transition-and-staff` | 428 |
| `cal.1966-10-06.cities-and-housing` | 428–29 |
| `cal.1966-10-17.vietnam` | the plates after 406 |
| `cal.1966-10-24.vietnam-asian-trip` | 434 |
| `cal.1966-10-28.vietnam-asian-trip` | 436–37, 439–42 |
| `cal.1966-10-30.vietnam-asian-trip` | 442–46 |
| `cal.1966-11-01.vietnam` | 446–53 |
| `cal.1966-11-02.vietnam-asian-trip` | 453 |
| `cal.1966-11-16.succession` | 453 |
| `cal.1966-12-14.transition-and-staff` | 462 |
| `cal.1966-12-16.assassination` | 462 |
| `cal.1966-10-19.vietnam-asian-trip` | 429–31 |
| `cal.1966-10-20.vietnam-asian-trip` | 431–32 |
| `cal.1966-10-20.vietnam-asian-trip-2` | 430 |

## Variants and Checks

- `cal.1966-11-01.vietnam`: Check: Lady Bird Johnson, 451–52, puts Johnson's address to the National Assembly on the morning of Nov. 2 (after the National Cemetery, before the Blue House coffee and Kimpo); the entry has it with Nov. 1–2. Whether the address was Nov. 1 or Nov. 2.
- `cal.1966-12-14.transition-and-staff`: Check: Lady Bird Johnson, 462, on Friday, Dec. 16: "Yesterday came the announcement of Bill Moyers' departure," that is, Dec. 15; the entry has Moyers resigning Dec. 14.
- `cal.1966-06-28.vietnam-congress-4`: Check: Lady Bird Johnson, 390, says the dinner was "just Lyndon and Dick and I"; the entry has Johnson and Russell alone.
- `cal.1966-06-29.vietnam-air-war`: Check: Lady Bird Johnson, 391, has Johnson, Luci and herself at the church after Russell left ("Lyndon and Luci and I"); the entry has Johnson and Luci. No hour is given; the entry says after midnight.
- `cal.1966-10-28.vietnam-asian-trip`: Check: Lady Bird Johnson, 436–37, has the party leave Manila about noon on Thursday, Oct. 27, and reach U Ta Pao three hours later; the entry asks whether the day of arrival was Oct. 27 or 28.

## Passed over (with the card's ground)

Family and social matters with nothing done or said of public business (Q5): Jan. 1, Mass at Stonewall and the New Year's dinner (346–47); Jan. 5, the rat in Luci's room and Airman Nugent's transfer (347–48); Jan. 18, the United Jewish Women, Frau Schwarzhaupp and the ambassadors' wives, Luci's zoology final (353–54); Jan. 23, the Smathers story on Johnson and the newspapers (354); Jan. 27–29, New York: the Astor dinner and its guests, the Vanderbilt lunch, the matinee, the train in the blizzard (356–58; the three oblong boxes seen on a freight car at Union Station at about midnight, "I suppose their destination was Arlington," 358, is a remark, no act); Feb. 22, her desk and *Women's Wear Daily* (362); Mar. 3, the Regents' tea (367); Mar. 11, the visit to the National Gallery before the opening (370); Mar. 17, the Mellon dinner at the Sulgrave Club, "no news coverage is allowed inside" (373); June 4, Lynda Bird's graduation, the President and Mrs. Johnson there "just as parents," Keppel's commencement address (386–88: a family matter; the doubt is that the President attended and the speaker urged government service); June 13, Justice Clark's wedding party for Luci at the Supreme Court, the Justices, the Speaker and Texas Congressmen present (388–90: a family matter; the doubt is the guests); June 28, Madame Shoumatoff's sketch of Roosevelt (390); July 17, Luci's bridesmaids' story and Mrs. Johnson's reflection that the press pits Connally against Johnson (393–94: a reflection, no act); July 19, the Cabinet wives' party and Mrs. Longworth's tea (394–95); July 27, the honeymoon reservations (399–400); Aug. 1, the Diplomatic Corps' gift to Luci at the Harriman party, which Mrs. Johnson calls "a personal family event, not a State occasion" (401: the doubt is the Corps and the Soviet bloc present); Aug. 2–3, the savings bond, the staff party and the bridesmaids' party (402–06); Aug. 6, Luci's wedding itself, entered only through the two entries the calendar holds (406–11); Aug. 25, the ring (415); Aug. 27, the birthday dinner (416); Sept. 1, Aikman and *The Living White House*, the McNamara wedding (417–18); Sept. 21, San Francisco in the morning (423); Oct. 25, 27 and 29, the Bang Saen drive, Crystal Island and the Klong (436–39); Oct. 30, the Kuala Lumpur drive and mosque; Dec. 16, the Children's Party (462–63); Dec. 24, the Christmas Eve at the Ranch after Kelly (465).

Preparations and covering matter: Jan. 12, the staff gathering before the speech; the family's wedding preparations of July 20 (the parking meeting is entered for its pickets), July 27 and Aug. 1.

## Leads

- Dec. 1 (458): Mrs. Johnson tells McGeorge Bundy of Los Baños, the Rice Institute, and Johnson's good-by to Dr. Robert Chandler, "if you just keep on producing better strains of rice and Margaret Sanger's folks keep on doing what they are doing, this old world might be saved yet." The day of the remark is not given (Oct. 24–26, Philippines?); not entered.
- Oct. 17–18 (the plates): "Toasting with a native chief in Pago Pago, October 18"; "Korea turns out to greet the President and First Lady, October 31"; "After-hours in the Oval Office with the President and Secretary Rusk": the last undated.
- Oct. 26: the diary has no entry for Cam Ranh Bay or Los Baños; Nov. 1 none for Seoul.
- Sept. 5: the diary says Dayton had "boiling" with unrest "last week"; `cal.1966-09-01.states-and-cities-dayton` holds the Sept. 1 shooting.
- Mar. 3: the Tax Bill "130 to nothing" and the Economic Aid Bill votes, as Johnson gave them to the newswomen; the roll calls of Feb. 24 to Mar. 2 are to check.

## Rulings that took a Check

`cal.1966-06-28.vietnam-congress-4` and `cal.1966-06-29.vietnam-air-war` (Mrs. Johnson at the dinner and at the church, 390–91, where the entries have Johnson and Russell "alone" and Johnson and Luci); `cal.1966-10-28.vietnam-asian-trip` (arrival in Thailand Oct. 27, 436–37); `cal.1966-11-01.vietnam` (the National Assembly address on Nov. 2, 451–52); `cal.1966-12-14.transition-and-staff` (Moyers's departure announced "yesterday," Dec. 15, 462).

Rules looked up: the card's test and examples (the Humphrey ride, Libonati, the pilot and the audit) for the social occasions and the wedding; R54 for the copy. No other.

## Where batch 11 stopped (1966)

The share is finished: Book Three read whole, Jan. 1 through Dec. 24, 1966 (printed pp. 345–465, PDF 375–503). Not done: the image check of every quoted word and number outside pp. 347, 354, 369, 392 and 459 (the text layer, matched by script, above); the Public Papers volumes for the speeches and news conferences, left as "To check" on each entry.


---

# Part three: Book Four, 1967 (Jan. 5 to Dec. 24, 1967; the 1967 reader)

Card `w.johnson-white-house-diary`. Read Nov. 12, 2026 (batch 11, the 1967 share): Book Four, "1967", printed pp. 467–608 (the text begins p. 469, PDF 507), from the Drive copy `1yDhieBtd5zcvoMYqrteT6Yg3a-R6sOie` (864 PDF pages, 40 MB; a text layer, read with `pdftotext -layout`). The copy, its page images and the OCR were deleted when the reading was done.

**The offset.** Printed page = PDF page less 38 through p. 518 (p. 469 = PDF 507; p. 518 = PDF 556), checked on the folios of the text layer and by image at p. 518. Eight plate pages and a title page follow (PDF 557-564: "1967 / A grandchild comes to the White House", the captions of the photographs, Jan. 17, Camp David, Mar. 13-15, Dec. 9); the text of p. 519 is PDF 565 (the end of May 13); then printed page = PDF page less 46 (p. 520 = PDF 566, checked by image; p. 522 = PDF 568; p. 566 = PDF 612; p. 608 = PDF 654). The folio is printed at the foot; the book runs by seasons ("Winter 1967" p. 469, "Spring 1967" p. 490, "Summer 1967" p. 520, "Fall 1967" p. 565) and Book Four ends with Christmas Eve, Dec. 24 (p. 607). The diary's entries for 1967 fall on these days only: Jan. 5, 10, 17, 23, 26, 27, 31; Feb. 22; Mar. 2, 9, 14, 15, 18; Apr. 22, 23, 25; May 10, 13; June 5, 9, 11, 21, 25; July 7, 31; Aug. 1, 3, 10, 13, 16, 22, 26; Sept. 8, 12, 25, 30; Oct. 4, 8, 9, 20, 26; Nov. 12, 23, 29; Dec. 4, 5, 9, 10, 24.

**What was checked against the image.** Every quotation entered was matched by script to the text layer within the pages it is cited to (footers and hyphen joins taken out). The 119 printed pages cited (pp. 469-597, 605-06) were then run through tesseract from page images at 150 dpi and the same script run on the OCR; the disagreements were read on the image. The OCR found two errors of the text layer, both corrected in the patch: the printed word is "résumé" (p. 554; the layer has "resume") and the pickets' sign at Williams is in capitals (p. 575). The other disagreements are the OCR's own ("600,c00", a stray mark, a hyphenated line end). Pages 518, 520, 549 and 592 were also read by eye off the image (the quotations there agree).

**The patch:** `inbox/2026-11-12-b11-ladybird-1967.yaml` (patch `2026-11-12-b11-ladybird-1967`): 69 new entries (ids claimed in the ledger first), 23 `cite` ops, 1 `variant` op, 0 `check` ops. `./bib patch-check`: 0 errors, 42 warnings, all "one event?": entries of one day and thread that are distinct events (three places of the Mar. 14 Appalachian trip, the Mar. 15 day in Tennessee, the four events of the Glassboro day, the Shah's arrival and dinner, the Oct. 4 night and morning talks, and so on); `./bib resolve ID --take keep` settles each if the merge flags it. The diary is Mrs. Johnson's account throughout: every `n` says so where it matters (what she saw, what she was told, her gist of a remark), and a private act carries "Made public: 1970." The threads are the events', not chosen to avoid the duplicate check. The new thread `elections-1968-johnson` is used for the talks on whether Johnson should run.

## Entered (new)

| Day | Entry | Page |
|---|---|---|
| Jan. 5 | `cal.1967-01-05.congress` | 470 |
| Jan. 5 | `cal.1967-01-05.press-and-broadcasting` | 469–70 |
| Jan. 10 | `cal.1967-01-10.congress-2` | 471 |
| Jan. 10 | `cal.1967-01-10.congress-3` | 472 |
| Jan. 17 | `cal.1967-01-17.congress` | 474 |
| Jan. 23 | `cal.1967-01-23.congress` | 477–79 |
| Jan. 26 | `cal.1967-01-26.states-and-cities` | 479–81 |
| Jan. 27 | `cal.1967-01-27.transition-and-staff` | 482–83 |
| Jan. 31 | `cal.1967-01-31.white-house` | 484–87 |
| Mar. 2 | `cal.1967-03-02.congress` | 490–92 |
| Mar. 9 | `cal.1967-03-09.elections-1968-johnson` | 492–93 |
| Mar. 14 | `cal.1967-03-14.school-aid` | 493–97 |
| Mar. 14 | `cal.1967-03-14.school-aid-2` | 497–98 |
| Mar. 14 | `cal.1967-03-14.school-aid-3` | 498–99 |
| Mar. 15 | `cal.1967-03-15.assassination` | 499 |
| Mar. 15 | `cal.1967-03-15.school-aid` | 499–501 |
| Mar. 15 | `cal.1967-03-15.school-aid-2` | 502 |
| Mar. 15 | `cal.1967-03-15.school-aid-3` | 502–03 |
| Mar. 18 | `cal.1967-03-18.students` | 503–04 |
| Mar. 18 | `cal.1967-03-18.states-and-cities` | 504–05 |
| Mar. 18 | `cal.1967-03-18.states-and-cities-2` | 505–06 |
| Apr. 22 | `cal.1967-04-22.program` | 506–08 |
| Apr. 23 | `cal.1967-04-23.farm` | 510 |
| Apr. 25 | `cal.1967-04-25.court` | 513–14 |
| Apr. 25 | `cal.1967-04-25.white-house` | 510–12 |
| May 10 | `cal.1967-05-10.labor` | 515–16 |
| May 10 | `cal.1967-05-10.war-opposition-2` | 516–17 |
| May 13 | `cal.1967-05-13.elections-1968-johnson` | 518–19 |
| June 9 | `cal.1967-06-09.conservation` | 522–25 |
| June 9 | `cal.1967-06-09.states-and-cities` | 526–27 |
| June 11 | `cal.1967-06-11.conservation` | 527–29 |
| June 11 | `cal.1967-06-11.conservation-2` | 530–31 |
| June 25 | `cal.1967-06-25.soviet-union` | 534–40 |
| June 25 | `cal.1967-06-25.soviet-union-2` | 541 |
| June 25 | `cal.1967-06-25.soviet-union-3` | 541–42 |
| June 25 | `cal.1967-06-25.soviet-union-4` | 541–42 |
| July 7 | `cal.1967-07-07.conservation` | 543–48 |
| July 31 | `cal.1967-07-31.civil-disorders-detroit` | 549 |
| July 31 | `cal.1967-07-31.elections-1968-johnson` | 549–50 |
| Aug. 1 | `cal.1967-08-01.program` | 550 |
| Aug. 3 | `cal.1967-08-03.crime-and-hijacking` | 551–52 |
| Aug. 13 | `cal.1967-08-13.vietnam-clifford-taylor` | 554 |
| Aug. 13 | `cal.1967-08-13.program` | 554 |
| Aug. 13 | `cal.1967-08-13.state-and-city-finance` | 557 |
| Aug. 16 | `cal.1967-08-16.vietnam-support` | 559 |
| Aug. 16 | `cal.1967-08-16.conservation` | 556–57 |
| Aug. 22 | `cal.1967-08-22.middle-east-2` | 559–60 |
| Aug. 22 | `cal.1967-08-22.middle-east-3` | 560–63 |
| Sept. 12 | `cal.1967-09-12.congress-2` | 569 |
| Sept. 25 | `cal.1967-09-25.elections-1968-johnson` | 570 |
| Sept. 25 | `cal.1967-09-25.vietnam-support` | 570–71 |
| Sept. 30 | `cal.1967-09-30.court` | 571–72 |
| Oct. 4 | `cal.1967-10-04.elections-1968-johnson` | 573–74 |
| Oct. 4 | `cal.1967-10-04.elections-1968-johnson-2` | 574 |
| Oct. 4 | `cal.1967-10-04.states-and-cities` | 574 |
| Oct. 8 | `cal.1967-10-08.students` | 575–78 |
| Oct. 9 | `cal.1967-10-09.students` | 579–82 |
| Oct. 20 | `cal.1967-10-20.conservation` | 582 |
| Oct. 20 | `cal.1967-10-20.elections-1968-johnson` | 583–84 |
| Oct. 20 | `cal.1967-10-20.congress` | 584 |
| Oct. 26 | `cal.1967-10-26.latin-america-2` | 585–87 |
| Oct. 26 | `cal.1967-10-26.vietnam-air-war` | 587 |
| Nov. 29 | `cal.1967-11-29.defense-clifford` | 592–93 |
| Dec. 4 | `cal.1967-12-04.health` | 593 |
| Dec. 4 | `cal.1967-12-04.vietnam-support` | 594–95 |
| Dec. 5 | `cal.1967-12-05.congress` | 595–96 |
| Dec. 5 | `cal.1967-12-05.conservation` | 596–97 |
| Dec. 24 | `cal.1967-12-24.vietnam-johnson-asia` | 605–06 |
| Dec. 24 | `cal.1967-12-24.program` | 606 |

## Cited (the card) and what the page bears

| Entry | Page | Ruling |
|---|---|---|
| `cal.1967-01-10.program` | 471–73 | pinned in part (the cite says what and what not) |
| `cal.1967-01-10.congress` | 471–72 | pinned in part (the cite says what and what not) |
| `cal.1967-01-17.vietnam-congress` | 474 | pinned in part (the cite says what and what not) |
| `cal.1967-01-17.press-and-broadcasting` | 474–77 | pinned in part (the cite says what and what not) |
| `cal.1967-01-27.space` | 481–82 | pinned in part (the cite says what and what not) |
| `cal.1967-01-27.space-2` | 482 | pinned in part (the cite says what and what not) |
| `cal.1967-01-31.space-apollo` | 483–84 | pinned in part (the cite says what and what not) |
| `cal.1967-03-09.economy` | 493 | pinned in part (the cite says what and what not) |
| `cal.1967-03-15.vietnam` | 501 | pinned in part (the cite says what and what not) |
| `cal.1967-03-15.war-opposition` | 501–02 | pinned in part (the cite says what and what not) |
| `cal.1967-03-18.states-and-cities-us` | 505 | pinned in part (the cite says what and what not) |
| `cal.1967-04-24.europe-and-the-alliance` | 508, 510 | pinned in part (the cite says what and what not) |
| `cal.1967-06-05.middle-east` | 520–22 | pinned in part (the cite says what and what not) |
| `cal.1967-06-23.soviet-union` | 535–41 | pinned in part (the cite says what and what not) |
| `cal.1967-08-16.republican-party-congress` | 556 | pinned in part (the cite says what and what not) |
| `cal.1967-08-22.states-and-cities` | 559 | pinned in part (the cite says what and what not) |
| `cal.1967-09-08.elections-1968` | 565–67 | pinned in part (the cite says what and what not) |
| `cal.1967-10-02.court` | 572 | pinned in part (the cite says what and what not) |
| `cal.1967-10-04.vietnam-congress` | 574 | pinned in part (the cite says what and what not) |
| `cal.1967-10-26.latin-america` | 584–87 | pinned in part (the cite says what and what not) |
| `cal.1967-11-12.vietnam` | 588–89 | pinned in part (the cite says what and what not) |
| `cal.1967-11-29.defense` | 591–92 | pinned in part (the cite says what and what not) |
| `cal.1967-12-19.vietnam` | 605–06 | pinned in part (the cite says what and what not) |

## Variants and Checks

- `cal.1967-11-12.vietnam`, unit C: the page (588) reads the sermon as "we wonder if some logical, straightforward explanation might be given?" and, at its end, "we ask humbly: 'Why?'"; the entry has "we ask respectfully, why?" (a variant, not a Check: the diary quotes the sermon from memory or the copies handed out; the Washington Post's text, Nov. 13, is the record).
- `cal.1967-03-15.war-opposition`: its Check ("the day") is answered by the diary: Mar. 15, leaving the Capitol after the address; the cite says so.
- Two new entries carry a Check: `cal.1967-08-13.state-and-city-finance` (the diary says "Sunday night" in its entry of Aug. 16; the family's visit ran July 30 to Aug. 16) and `cal.1967-10-04.states-and-cities` (the day of the Rose Garden program she watched).

## Passed over (with the card's ground)

Family matter, no bearing on public business (Q5): Jan. 5 (Lynda in from Acapulco, the bowling); Jan. 10 (the china patterns); Feb. 22 (New York: fittings; Mary Lasker's dinner for the Chagalls, the Rodgerses and John Gunther, toasts and talk of the theater); Mar. 9 morning (Spanish class, fittings); Apr. 22 (Watts Branch; bridge); Apr. 23 (Mrs. Morris's house; Fredericksburg and the hope of a Madison portrait for the White House: a furnishing; the play); Apr. 25 (the Senate Ladies Luncheon, a vermeil frame for Luci's child); May 13 evening (Camp David with the McNamaras, the Pickles, the Valentis: no business said); June 21 (Patrick Lyndon Nugent born; the reporters' questions to Mrs. Johnson, "I like the status better than the title"); July 31 (the tea for the Texas delegation's wives, family day); Aug. 1 evening (chili at the Bill Whites'); Aug. 10 (Lynda tells her parents she is in love with Chuck Robb); Aug. 13 afternoon and evening (church; Luci and Pat home from Nassau); Aug. 16 afternoon (Lynda and Chuck ask Johnson's consent; the plans for Dec. 9); Aug. 26 (Kerrville: the dedication of the Butt-Holdsworth Library is named in a clause only; the Ranch house; Mount Vernon at 4:30 a.m. for Johnson's birthday); Sept. 12 afternoon (the "Country Fair" for the children of Congressmen and officials: a children's party, Johnson there with Yuki); Sept. 25 morning (the Tiffany china design: a furnishing); Sept. 30 (the family picture); Oct. 20 (the Jockey Club lunch with Lynda: a stranger's letter, a woman's "Tell the President to have courage," no act of a principal); Nov. 23 (Thanksgiving at the Ranch); Nov. 29 (autographing Christmas pictures); Dec. 4 (the Harrimans' party to introduce Lynda and Chuck to the Diplomatic Corps, Johnson there twenty minutes; the Savings Bond for the wedding); Dec. 5 (Lynda's gifts; the Boggs dinner for Lynda and Chuck, "the progress of legislation, the state of affairs on the Hill" heard in passing, no act); Dec. 9-10 (Lynda's wedding to Charles Robb in the East Room, 640 guests, the Chief Justice, the Vice President, the Rusks, Dirksen, the generals among them: a family matter, nothing of public business done or said; the letters of 1934); Dec. 24 evening (the Christmas tree and presents).

Named only, nothing said (Q5): Jan. 5 (Bill Moyers' departure "giving the press a picnic"; Charlie Schultze's remark in December); Jan. 17 afternoon (Joan Crawford's visit on beautification, cited under the dinner entry); Mar. 15 (the Hermitage's breakfast menu); Nov. 11-12 (a Gridiron dinner, "a great evening," p. 589).

## Leads

- Jan. 5 (469): Charlie Schultze to Johnson in December: "You will go down in history as the man who kept this nation together fighting a limited war"; undated (December 1966); not searched.
- Aug. 13 (556): "Today's poll has Lyndon down to thirty-nine percent—the lowest he has ever been" (the diary's day, Aug. 13?); Mrs. Johnson reads "a speech that Senator Fulbright made" that the country is damned by spending in Vietnam instead of at home (undated); not searched against the calendar's opinion and Vietnam-Congress threads.
- Dec. 4 (594): Johnson's "important appointment with William Randolph Hearst" before the National Foreign Policy Conference; not entered (an expectation of hers, not a recorded meeting).
- Sept. 25 (570): the date of the Democratic dinner, Oct. 7, as a possible day for the announcement: the calendar's Oct. entries on the draft statement (`cal.1967-10.elections-1968-3`) were not read against it.
- Oct. 8 (577): Professor James MacGregor Burns takes her through Mt. Hope Farm, "the site for the environmental planning center": not entered.
- The plate captions (PDF 557-564) date three scenes: Hello, Dolly! at the White House, Jan. 17 (see the dinner entry's cite); the Appalachia trip, Mar. 13-15; the White House wedding, Dec. 9. The first day of the Appalachian trip, Mar. 13, is not in the text (the entry for Mar. 14 begins on the second day).

Rules looked up: the card's test and examples for the social occasions, the dinners, the wedding and the Fortas, Cain and Hurst talks (the Humphrey ride, the pilot and the audit); R54 for the copy; R30 (a pinpoint names a number) for the cites' pages; the addops STYLE for `variant`. No other.

## Where batch 11 stopped (1967)

The share is finished: Book Four read whole, every page, Jan. 5 to Dec. 24, 1967 (printed pp. 469-607, PDF 507-653); the diary has nothing for the rest of the year (it resumes with Book Five, 1968-1969, p. 609, another reader's). Every dated event with a bearing on public business is in the patch, cited under the entry the calendar held, or on the lists above. Not done: a reading by eye of every quotation on the image (script on the text layer and on the OCR, with the disagreements read by eye, and four pages read directly); the auditor's blind pass is still to come.
