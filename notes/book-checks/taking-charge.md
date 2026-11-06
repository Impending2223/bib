# Beschloss, ed., *Taking Charge* (1997): the calendar read against the book

Michael R. Beschloss, ed., *Taking Charge: The Johnson White House Tapes, 1963–1964* (1997), card `w.taking-charge`. Read Nov. 5–6, 2026 (batch 4, group 10), from the owner's Drive copy (file id 1NkEeNniIBmF0is2eEqIozpxq75cJqTmq; 45 MB, 614 PDF pages; Internet Archive's scan `takingchargejohn00john`, with its OCR text layer, read with `pdftotext -layout`; no OCR of my own). The copy was deleted when the reading was done.

The offset: printed page = PDF page − 2 through p. 224 (PDF 226); sixteen pages of plates follow, unnumbered (PDF 227–242); from p. 225 (PDF 243) printed page = PDF page − 18. Checked on pp. 19, 29, 49, 99, 283, 483, 543, 583, and against the page images at pp. 73, 248, 371 (the text layer and the image agree on every pinpoint checked).

The book is a selection of transcripts of the White House recordings, Nov. 22, 1963, to Aug. 29, 1964, each conversation headed by its day, the other party and the hour, with Beschloss's headnotes and footnotes; a prologue (Johnson's remarks of Dec. 1966–Jan. 1967 on Manchester's book) and an appendix (the Warren Report and Garrison: Sept. 18 and 28, 1964; Feb. 18 and 22, Mar. 2, 1967). Every conversation is a recording; each one cited or entered here carries the Miller Center's free page as its primary record where the daybook's catalogue holds it (`daybook/recordings/millercenter.yaml`), matched by the day, the hour within twenty-five minutes and the other party's surname, and PRDE's page where only PRDE has it (Dec. 2, 1963, Fulbright). The transcript is the book's; each recording is registered as a witness (`kind: recording`, not heard), the book's edge to it a `transcription` at the page (`sources/witnesses/by-work/taking-charge.yaml`, `PAGE n.<surname>-<hhmm>`). Quotations in the entries are a few words, as the book prints them.

## The patches

- `inbox/2026-11-05-b4-taking-charge.yaml` (Nov. 22, 1963–Apr. 10, 1964, and the waiting entries) and `inbox/2026-11-05-b4-taking-charge-2.yaml` (Apr. 14–Aug. 29, 1964, the appendix, the prologue's Nov. 1960, two events dated by the notes): together 306 new entries, 149 cites, 35 checks, with their primary records and claim-map rows. All new entries claimed in the ledger under the two patch names.
- Witnesses: `inbox/witnesses/2026-11-05-b4-taking-charge.yaml` and `-2.yaml` (393 rows: the recordings, and the documents the notes give for units cited: the UPI story of Feb. 3, 1964; the Defense Department's "Summary Statement on South Vietnam," Mar. 2, 1964; Robert Kennedy's letter of June 11, 1964; the NSC executive committee's record of May 24, 1964; Lady Bird Johnson's diary, July 4, 1964; Pincus in the *Star*, June 23, 1964; Katzenbach to Moyers, Nov. 25, 1963; Sidey's and Manchester's books). Existing registry rows reused where they matched (Mansfield to Johnson, Jan. 6, 1964; McCone's memorandum of Nov. 24, 1963; Taylor's of Mar. 4, 1964; JCSM-174-64; Fulbright's "Old Myths," Mar. 25, 1964; three recordings already registered).
- The work's edges: `sources/witnesses/by-work/taking-charge.yaml` (446 edges).

## The entries waiting on the book (To check), ruled

Held, pinned, with the page (and units where only part): `cal.1963-11-30.vietnam` (73–74), `cal.1963-12-02.vietnam-congress` (86–88, B–D; Geneva not in the book), `cal.1963-12-07.vietnam-congress` (94–95), `cal.1963-12-23.vietnam` (123–24), `cal.1964-02-03.vietnam` (213–14), `cal.1964-02-06.vietnam` (226), `cal.1964-03-02.vietnam` (264), `cal.1964-03-02.vietnam-2` (262–63), `cal.1964-03-04.vietnam-4` (266–67), `cal.1964-03-25.latin-america-2`, `-3` (297–98), `cal.1964-04-30.vietnam` (337–38), `cal.1964-05-20.vietnam` (359), `cal.1964-05-27.vietnam` (363–70), `-2` (370–72), `-4` (373–74), `cal.1964-06-09.laos-3` (393–95), `cal.1964-06-11.vietnam` (400–403), `cal.1964-06-11.robert-kennedy` (405–6, A–B; 374–75, D; Sanford, June 12, not in the book), `cal.1964-06-15.vietnam-3` (408–9), `cal.1964-06-21.mississippi` (425, A; 431–39, E), `cal.1964-07-21.robert-kennedy` (459–60, A–B; 461–62, E–F; 464–65, H), `cal.1964-07-30.elections-1964` (484, B), `cal.1964-08-02.vietnam` (493 & n.5, A–F), `cal.1964-08-24.elections-1964` (523, A), `cal.1964-01-09.latin-america` (155: the march and the flag, "more than twenty Panamanians" killed; not the torn flag, Colón or the soldiers), `cal.1964-02-15.europe-and-the-alliance` (243 & n.4: the call and the buses; the quotation is not in the book's excerpt), `cal.1964-01-31.republican-party` (213 n.7).

Not treated by the book, left behind "To check:": `cal.1963-12-07.economy` (the news conference: the book prints Russell's and McNamara's calls that day only); `cal.1963-11-22.succession` (the oath at Love Field: the prologue has only Johnson's recollection of 1966–67, cited to the combined card `w.taking-charge-2001` there); `cal.1964-08-22.mississippi` (the Credentials Committee's hearing: not in the book).

The combined card `w.taking-charge-2001` (*Taking Charge* & *Reaching for Glory*) stands behind "To check:" in eight entries; where *Taking Charge* treats the event (June 11, June 21, July 21, July 30, Aug. 2, Aug. 24, 1964) it is now cited by its own card beside it. The merger may wish to drop the combined card from those entries.

## Rulings other than "holds"

| Entry | The calendar / the record | The book | Ruling |
|---|---|---|---|
| `cal.1964-02-21.vietnam-2` | Johnson and McNamara, Feb. 21, 7:45 a.m. (Miller Center 2152), Shoup to go with McNamara | the words in a call at 11:45 a.m. printed after Feb. 20 without a date heading (248–50), the same call as the "foolish" words of `cal.1964-02-25.vietnam-force-levels` (Miller Center Feb. 25, 2191) | Check; probably one call with Feb. 25, misdated here: for the owner or the merger to combine |
| `cal.1964-04-29.civil-rights-bill-4` | Kotz: Robert Kennedy to Johnson, Apr. 29, 10:50 p.m. | Apr. 23, 10:50 p.m., Johnson in Chicago (326–27); the Miller Center the same (WH6404-12-3126) | Check, recording and book against Kotz's day |
| `cal.1963-12-23.vietnam` | Mann: Dec. 18 | Dec. 23, 9:35 p.m. (123) | Check; the recording's day kept |
| `cal.1964-03-25.vietnam-congress` | Mann: "half bright" McCarthy's word | Johnson: "As Truman said one time" (298) | Check; the entry doubles `latin-america-2` and `-3` (to combine) |
| `cal.1964-03-25.latin-america-2` | "I feel mighty blue"; "We have just gotten over" | "I felt mighty blue"; "We just have gotten over" (297–98) | Check |
| `cal.1964-04-30.vietnam` | "which call," 6:10 or 7:50 p.m. | 7:50 p.m. (337–38) | settled, parenthetical |
| `cal.1964-05-27.vietnam-2` | FRUS's wording | "What the hell is Vietnam worth to me?"; "He got no spine at all" (370–71) | Check |
| `cal.1964-05-20.vietnam` | "counterinsurgency" | "counterguerrilla" (359) | Check |
| `cal.1964-03-02.vietnam` | "is more of the same" | "is do more of the same" (264) | Check |
| `cal.1963-11-30.vietnam` | "to go out there" | "to go there" (74) | Check |
| `cal.1964-03-04.vietnam-4` | "I got to win an election" | "I'm a trustee. I've got to win an election" (267) | Check |
| `cal.1964-06-11.robert-kennedy` | the letter: "glad to do so" | "glad to go" (405 n.4) | Check |
| `cal.1964-06-09.civil-rights-bill` | Humphrey sure of sixty-six | sixty-eight, forty-two Democrats (400) | Check |
| `cal.1964-06-08.laos` | Unger opposed | the Ambassador opposed, the note naming Lodge (387 n.2) | Check |
| `cal.1964-01-06.civil-rights-bill` | 5:15 p.m. | 5:12 p.m.; "not going to get to cloture" (147–48) | Check |
| `cal.1964-06-23.mississippi-5` | 4:16 p.m. | 3:35 p.m. (431) | Check |
| `cal.1964-07-14.democratic-party` | 9:20 a.m. | 9:50 a.m. (455) | Check |
| `cal.1964-08-06.vietnam-3` | McCone told the leaders too much | the book prints McNamara on the hearings (506–7) | cited for the call only; Check with the book's matter |
| `cal.1964-08-09.democratic-party`, `cal.1964-07-13.civil-rights-the-executive`, `cal.1964-06-11.medicare`, `cal.1964-01-06.civil-rights-the-executive`, `cal.1964-02-05.elections-1964`, `cal.1964-02-12.elections-1964-2`, `cal.1964-03-07.elections-1964-2`, `cal.1964-07-25.elections-1964`, `cal.1964-05-11.poverty` | the words of other sources | the book prints another passage of the same call | cited for the call only, parenthetical |

Recordings dated otherwise by the book and the Miller Center, each entered with the book's hour and a Check: Nov. 23, 1963 (Edward Kennedy, 7:40 / 8:10 p.m.), Dec. 3 (Albert, 3:00 / 5:56 p.m.), Dec. 20 (McCormack, 6:30 / 6:06 p.m.), Dec. 23 (Mrs. Johnson, 8:35 / 7:35 p.m.), Feb. 7, 1964 (Russell, 4:30 / 6:30 p.m.), Mar. 2 (Rowley, the book's "11:25 p.m." among the morning's calls), Aug. 4 (Rowe: the book Aug. 4, the Miller Center Aug. 6).

## Passed over

Made from the conversations as the book prints them, each one read and ruled; every conversation not listed here is an entry or a cite (the waiting entries and the rulings above, the patches' ops). The rows, page | date | the event | ground:

| Page | Date | Event | Ground |
|---|---|---|---|
| 42–44 | Nov. 27, 1963, 1:35 p.m. | Nellie Connally: family and social. After the address to Congress, the Johnsons, Luci and Lynda by telephone to Nellie Connally: the Governor's recovery; their son John III at the funeral. | minor |
| 48 | Nov. 29, 1963, 11:35 a.m. | Hale Boggs: social. Boggs on the address; Lindy Boggs to help Mrs. Johnson. | minor |
| 78–79 | Nov. 30, 1963, 3:16 p.m. | Lucia Alexander: family. Johnson to his sister Lucia Alexander. | minor |
| 104 | Dec. 17, 1963, 6:04 p.m. | Office conversation: Johnson with aides over the newspapers' photographs in the Baker affair. | passed-over paper (private remarks) |
| 105 | Dec. 17, 1963, 7:30 p.m. | Lady Bird Johnson: family. Mrs. Johnson asks the President home from the office. | minor |
| 115–116 | Dec. 23, 1963, 11:38 a.m. | Eddie Senz: social. A New York hairdresser to fly down for Mrs. Johnson, the daughters and the secretaries. | minor |
| 124–126 | Dec. 23, 1963, 9:45 p.m. | Pierre Salinger: arrangements for the flights to Green's funeral, O'Donnell and Ethel Kennedy on the President's plane. | minor |
| 131–132 | Dec. 25, 1963, 1:16 p.m. | Dwight Eisenhower: social. Christmas greetings to the Eisenhowers at Palm Desert. | minor |
| 134 | Dec. 25, 1963, 8:27 p.m. | Robert McNamara: social. Christmas greetings to McNamara. | minor |
| 143–144 | Jan. 2, 1964, 12:25 p.m. | Irving Frank: social. Western suits for the staff at the Ranch. | minor |
| 146 | Jan. 3, 1964, 2:00 p.m. | Walter Jenkins: a bill from State for purchases on the vice presidential trip to northern Europe, 1963. | minor |
| 146–147 | Jan. 6, 1964, 3:30 p.m. | John Magy: office staffing; five secretaries to be found for the President's office. | minor |
| 151 | Jan. 7, 1964, 12:45 p.m. | Hale Boggs: the ceremonial call at the opening of the session, 340 Representatives present. | minor |
| 154–155 | Jan. 8, 1964, 8:00 p.m. | Theodore Sorensen: social. Mrs. Johnson thanks Sorensen for the State of the Union. | minor |
| 184–185 | Jan. 25, 1964, 4:40 p.m. | George Reedy: Johnson to Reedy, where to find him after the press meeting. | minor |
| 191 | Jan. 28, 1964, 7:30 p.m. | Walter Jenkins: private remarks; Jenkins on material about Reynolds to be typed for the President. | minor |
| 193 | Jan. 29, 1964, 11:45 a.m. | Walter Jenkins: Johnson presses Jenkins to reach Humphrey (11:45 a.m., 12:25 p.m.). | minor |
| 193 | Jan. 29, 1964, 12:25 p.m. | Walter Jenkins: as at 11:45 a.m. | minor |
| 197–198 | Jan. 30, 1964, 6:00 p.m. | Office conversation: Johnson to Clifford and Jenkins on Humphrey, "full of grits." | passed-over paper (private remarks) |
| 200–201 | Jan. 31, 1964, 6:47 p.m. | Jack Brooks: social; an invitation to a drink and the pool. | minor |
| 214 | Feb. 3, 1964, 5:57 p.m. | Everett Dirksen: social; Dirksen in Sibley Hospital with an ulcer, Johnson's banter. | minor |
| 236 | Feb. 10, 1964, 10:55 p.m. | Walter Jenkins: Johnson to Jenkins against scheduling "little tinhorn Ambassadors." | minor |
| 245 | Feb. 19, 1964, 6:34 p.m. | Marianne Means: social. Means back from Texas, interviews with Johnson's family. | minor |
| 248 | Feb. 20, 1964, 11:20 a.m. | Office conversation: Johnson to aides on leaks from State; printed after Feb. 20 without a date (perhaps Feb. 25). | passed-over paper (private remarks) |
| 260 | Mar. 2, 1964, 11:15 a.m. | Robert Wagner: social. Johnson to Wagner on his dying wife. | minor |
| 265 | Mar. 4, 1964, 1:48 p.m. | Office conversation: who leaks the poverty planning; Potter's story in the Baltimore Sun that morning (the press list). | passed-over paper (private remarks) |
| 272–274 | Mar. 7, 1964, 4:10 p.m. | Lady Bird Johnson: family. Mrs. Johnson on his East Room news conference, from her diary. | minor |
| 279 | Mar. 9, 1964, 8:30 p.m. | Jack Valenti: social. Valenti sent home to his wife. | minor |
| 286 | Mar. 13, 1964, 10:00 p.m. | Abe Fortas: social. Fortas invites Johnson dancing. | minor |
| 287 | Mar. 14, 1964, 2:44 p.m. | George Reedy: private. Reedy kept in the hospital to lose weight. | minor |
| 288–289 | Mar. 17, 1964, 12:49 p.m. | George Reedy: private. Reedy's diet in the hospital. | minor |
| 291 | Mar. 18, 1964, 11:06 a.m. | McGeorge Bundy: banter. "The only intellectual left in the White House." | minor |
| 291 | Mar. 18, 1964, 7:35 p.m. | Lady Bird Johnson: family. Johnson to Mrs. Johnson: thirty minutes at John Bailey's meeting, then supper. | minor |
| 296 | Mar. 23, 1964, 9:15 p.m. | Lady Bird Johnson: family. Johnson kept late on his speech of the morning. | minor |
| 298–299 | Mar. 25, 1964, 7:51 p.m. | Rene Verdon: social. Dinner for six or eight. | minor |
| 302–303 | Mar. 30, 1964, 11:55 a.m. | Joseph Kennedy: social. Johnson to Joseph Kennedy, paralyzed, at Palm Beach. | minor |
| 303 | Mar. 30, 1964, 8:00 p.m. | George Reedy: a man following his car at the Ranch. | minor |
| 304–305 | Mar. 31, 1964, 3:10 p.m. | Rodney White: family. Furnishing the family house at Johnson City with his nephew. | minor |
| 311 | Apr. 8, 1964, 12:13 p.m. | Office conversation: Johnson to aides, a wedding and the cherry blossoms. | minor |
| 320 | Apr. 17, 1964, 3:52 p.m. | Harry Truman: social. Blair House offered for Truman's visit to Washington. | minor |
| 321 | Apr. 20, 1964, 6:45 p.m. | Jack Brooks: social. Brooks back from Texas, Connally's hand. | minor |
| 323 | Apr. 22, 1964, 7:47 p.m. | Lady Bird Johnson: family. Johnson to Mrs. Johnson after the railroad settlement. | minor |
| 341 | May 2, 1964, 4:30 p.m. | McGeorge Bundy: social. Golf or tennis. | minor |
| 345–346 | May 11, 1964, 12:45 p.m. | Joseph Kennedy: social. Johnson to Joseph Kennedy at Hyannis Port, through Ann Gargan. | minor |
| 414–415 | June 17, 1964, 8:58 p.m. | Lady Bird Johnson: family. | minor |
| 422–423 | June 20, 1964, 6:46 p.m. | Jacqueline Kennedy:  | part of the call of 6:45 p.m., entered there. |
| 440 | June 25, 1964, 4:52 p.m. | Office conversation: Johnson to Valenti, "I imagine they're in that lake." | passed-over paper (private remarks) |
| 440–441 | June 25, 1964, 7:45 p.m. | Chester Clifton: the Secret Service men on his plane. | minor |
| 441–442 | June 26, 1964, 5:30 p.m. | Walter Jenkins: Camp David on the weekend of July 4 declined to Bundy. | minor |
| 445 | June 30, 1964, 5:35 p.m. | Edward Kennedy: social. Johnson to Edward Kennedy in Cooley Dickinson Hospital. | minor |
| 452 | July 3, 1964, 12:43 p.m. | Jesse Kellam: social. A boat ride on Lake Wirtz. | minor |
| 457 | July 17, 1964, 1:57 p.m. | A.W. Moursund: social. A boat and a fish dinner at the Ranch. | minor |
| 502 | Aug. 4, 1964, 8:35 p.m. | Lady Bird Johnson: family. Mrs. Johnson before his address. | minor |
| 511 | Aug. 9, 1964, 1:16 p.m. | Joseph Haggar Jr.: private. Slacks ordered. | minor |
| 514 | Aug. 13, 1964, 1:10 p.m. | Edward Kennedy: social. Edward Kennedy recovering. | minor |
| 99 | Dec. 12, 1963, 2:37 p.m. | Office conversation: office routine; Johnson wants texts edited so he can read them, and his office kept clear. | minor |

## Where I stopped

Every conversation of the book (pp. 17–548), the prologue's first event (Nov. 1960) and the appendix (pp. 559–66) is entered, cited or passed over above. The headnotes and footnotes date further events (Salinger's resignation, the cloture vote, the House votes, Goldwater's statements); those met while reading were checked against the calendar and two not found were entered (`cal.1964-03-05.elections-1964`, King and the write-in; `cal.1964-03-23.baker`, the Rules Committee's vote); the rest of the notes' dated events were not canvassed one by one against the calendar, a second pass for a later reader. No `time:` fields were written: the book's hours are in `c`; Johnson's place (Washington, the Ranch) would fix the zone.

## The press

Coverage the book dates, a line each (date | outlet | item | page):

- Nov. 27, 1963 | *Washington Post*, Alsop's column | Johnson "an almost pure man of action" | 45 n.3
- Dec. 3, 1963 | *U.S. News & World Report* | Rusk reluctant at the reception for the foreign dignitaries | 89
- Dec. 25, 1963 | *New York Times*, Reston's column | the politicians' wives | 133 n.3
- Jan. 22, 1964 | Evans and Novak | "Republican pros" moving toward Scranton | 173 n.1
- Feb. 3, 1964 | UPI | Nixon in North Carolina, Goldwater at Minneapolis, on Vietnam | 213 n.7
- Feb. 8, 1964 | *New York Times*, front page | Cabell Phillips: officials used secret files against Reynolds | 235
- Mar. 4, 1964 | *Baltimore Sun*, front page | Philip Potter: Shriver's planners and community action | 265 n.1
- Mar. 9, 1964 | *Washington Star*, editorial | the Kennedy name "magic" | 276
- Mar. 21, 1964 | ABC | John Scali: Rusk to resign in November | 292
- Apr. 1964 (the week of Apr. 7) | *Time* | "Mr. President, You're Fun" | 307
- Apr. 28, 1964 | AP | Doug Cornell on the beagles | 330 n.1
- June 9, 1964 | *Washington Star*, front page | John Barron, "The Johnson Money," $9 million | 392
- June 17, 1964 | *New York Times* | Reston: Robert Kennedy volunteered for Saigon | 412
- June 23, 1964 | *Washington Star* | Walter Pincus on the President's Club | 428 n.7
- June 29, 1964 | *Washington Post*, lead story | Johnson at Minneapolis: risk war to keep freedom | 443 n.2
- July 16, 1964 | *New York Times* | Goldwater on Johnson, "the biggest faker in the United States" | 457 n.1
- July 21, 1964 | *New York Daily News*, column | the Northern bosses for Kennedy | 462
- Aug. 14, 1964 | *New York Times* | Johnson endorsed Kennedy for the Senate | 517
- Aug. 25, 1964 | *Washington Post* | what Johnson asks of a Vice President, from a background interview | 536
- Aug. 26, 1964 | *Washington Star*, McGrory | "Kennedy Magic" | 537 n.3

## Leads

### National

- The prologue's calls on Manchester's *The Death of a President*: to Katzenbach (Dec. 6, 1966; Jan. 25, 1967), Fortas (Dec. 16, 1966), Kintner (Dec. 20, 1966) and Moyers (Dec. 26, 1966) (11 n.4). The book runs Johnson's remarks together without saying which call holds which: the recordings (the Miller Center's catalogue for those days) would date each.
- Press figures the book treats in exchanges with Johnson, for Part III entries where none exists: Marshall McNeil (Scripps-Howard), Walker Stone (Scripps-Howard), Gould Lincoln (*Washington Star*), Isabelle Shelton (*Washington Star*), Frances Lewine (AP), Marianne Means (Hearst), Doug Cornell (AP), Tom Collins (*Newsday*), Louis Kohlmeier (*Wall Street Journal*), John Barron (*Washington Star*); the publishers John S. Knight (*Miami Herald*), Houston Harte (*San Angelo Standard-Times*), Amon Carter Jr. (*Fort Worth Star-Telegram*), Paul Miller (Gannett), John Jones (*Houston Chronicle*); and Henry Luce, Clare Boothe Luce, Katharine Graham, Frank Stanton.
- Persons the entries name who seem to have no name entry (not tagged): Richard Maguire, Jesse Kellam, A. W. Moursund, Rose Kennedy, Nellie Connally, John Bailey, Frank Erwin, Elmer Staats, Cliff Carter, Gerri Whittington, Andrew Hatcher (tagged once), Edwin Weisl Sr., B. Everett Jordan.
