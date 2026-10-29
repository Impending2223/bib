# Mann, *A Grand Delusion* (2001): the calendar read against the book

Robert Mann, *A Grand Delusion: America's Descent into Vietnam* (2001), card `w.mann-grand-delusion`. Read Oct. 28–29, 2026, from the owner's Drive copy (file id 1eo_ZqbCFBEtv-Y9p94cPhkJJTitEa1s7), a scan with an OCR layer, by its printed pages: the PDF's page is the printed page + 12 through p. 246, + 20 for pp. 247–502 (the plates after p. 502), + 28 from p. 503. The copy was kept outside the repo and deleted when the reading was done; nothing of its text is here but the short quotations the entries carry.

The span read is the book's 1960 to Jan. 20, 1969: the end of ch. 15 (Mansfield's subcommittee, 1959–60) through the opening of ch. 38 (Rogers before Foreign Relations, Jan. 15, 1969). The book is a history of the Senate and the war; under the owner's rule of Oct. 29 every Senator's dated word on the war is within the brief. Each dated event was looked for in the calendar on its day, in every thread: an event the calendar holds took the page (an edit, the existing cites, sentences and rows kept); one it lacks became an entry. Every quotation entered was set against the book's page, and where the book cites the *Congressional Record*, FRUS, the Public Papers or a recording the free catalogues give, against that record too (the Record's daily granules on govinfo, read page by page; FRUS from the TEI text; the Papers from GPO's volumes). The patch is `inbox/2026-10-29-book-mann.yaml` (patch `book-mann`); the records the book cites for the calendar's claims are in `sources/cited-records/mann-grand-delusion.yaml`.

## Rulings other than "holds"

Where Mann and the record (or the calendar's other sources) disagree, both stand and the entry carries a Check. The chief ones:

| Entry | The calendar / the record | Mann | Ruling |
|---|---|---|---|
| `cal.1963-09-06.vietnam-congress` | Morse's speech, the Record of Sept. 6, 1963 | Sept. 9 | Check; the Record's day kept |
| `cal.1963-12-23.vietnam` | Johnson and Valeo, PRDE and the Miller Center, Dec. 23, 9:35 p.m. | Dec. 18, "evening" | Check; the recording's day kept |
| `cal.1964-03-02.vietnam-congress` | Mansfield in the Senate, Mar. 2, 1964 | Mar. 3 | Check |
| `cal.1964-03-04.vietnam` | Morse's "murder" speech, the Record of Mar. 4 | Mar. 5 | Check |
| `cal.1964-03-10.vietnam`, `cal.1964-03-11.vietnam` | Gruening and Dodd in the Senate, Mar. 10–11, 1964 | "October" 1963 | Check |
| `cal.1964-05-18.vietnam` | the request of May 18 | May 15 | Check |
| `cal.1964-08-04.vietnam-congress-2` | the leaders at the White House, the evening of Aug. 4 | "the evening of August 5" | Check |
| `cal.1964-10-08.elections-1964-2` | the words in the Papers' Cleveland remarks | Lake County, Ind., that day | Check |
| `cal.1965-01-12.vietnam-congress` | Fulbright puts the *Ramparts* piece in the Record, Jan. 12, 1965 | Church, "a month" after McGovern | Check |
| `cal.1965-02-06.vietnam-congress`, `cal.1965-02-07.vietnam-congress` | the NSC meetings, FRUS: Feb. 6 and 7 | Feb. 7 and 8 | Check |
| `cal.1965-02-09.vietnam` | Bundy's reply, FRUS: Feb. 9 | Feb. 8 | Check |
| `cal.1965-04-02.vietnam-congress` | Fulbright's memorandum, Apr. 2 | handed to Johnson in early April, sent Apr. 6 | Check |
| `cal.1965-06-09.vietnam` | Mansfield's second course, FRUS: about 500,000 men | "the 300,000 McNamara estimate is probably too low" | Check |
| `cal.1965-06-17.vietnam-congress-3` | McGovern, the Record of June 17, 1965 | text "July 17," note June 17 | Check |
| `cal.1965-07-27.vietnam` | the leaders' meeting, FRUS: Kuchel present | Kuchel left out | Check |
| `cal.1965-07-28.vietnam-us` | the governors' resolution by voice vote, the *Proceedings* | Hatfield alone against, by his interview | Check, beside Gibbons's |
| `cal.1966-01-29.vietnam-congress-2` | Stennis's speech of Jan. 29, 600,000 men (Gibbons) | Fulbright on Jan. 28 cites Stennis's remarks of "yesterday," 690,000 and nuclear weapons | Check |
| `cal.1966-01-31.vietnam-congress` | Aiken's "first drop in the bucket," the Record of Jan. 31 | with the request of Jan. 19 | Check |
| `cal.1966-02-11.vietnam-hearings-2` | Johnson and U. Alexis Johnson, FRUS: Feb. 11, 1966 | "mid-March" | Check; FRUS's day kept |
| `cal.1966-02-08.vietnam-humphrey` | Los Angeles, Feb. 8 | Feb. 6 | Check |
| `cal.1967-03-01.vietnam` | the vote of 72–19, Mar. 1 | Feb. 28 | Check |
| `cal.1967-05-01.vietnam-congress` | "No record" | Mansfield's memorandum for the file | Check; Mann's account added |
| `cal.1967-07-25.vietnam` | "a hopeless venture" | "a hopeless adventure" | Check |
| `cal.1967-08-20.vietnam-commitments` | the AP's survey, 40 of 84 | 45 of 84, 26 Democrats and 19 Republicans | Check |
| `cal.1967-12-07.vietnam-congress` | McPherson to Mansfield, Dec. 7 (FRUS) | "late November" | Check |
| `cal.1968-02-06.vietnam-tet` | the leaders' breakfast, Feb. 6 | "the next morning, on April 6" | Check (a misprint) |
| `cal.1968-08-28.elections-1968` | the minority plank lost 1,567¾ to 1,041¼ | 1,567 to 1,048, from CQ | Check |

Some three dozen more Checks of this kind (a day "about," a place, a word) are in the entries' notes; each begins "Check: Mann."

Nine edits first written as whole notes were rewritten (Oct. 29) as additions to the notes as they now stand: `cal.1960-02-26.vietnam-congress`, `cal.1961-05-25.vietnam-johnson-asia`, `cal.1961-11-11.vietnam`, `cal.1962-01-12.vietnam-congress`, `cal.1962-02-14.vietnam`, `cal.1962-02-20.vietnam-congress`, `cal.1962-12-26.vietnam`, `cal.1963-03-06.economy` and `cal.1964-03-02.vietnam`; three of them the Selverstone and Reeves runs had changed meanwhile. On `cal.1963-03-06.economy` the Mansfield sentence the Selverstone run had entered takes Mann's page, and no sentence is added; every other run's cite, sentence and row is kept.

## Passed over

Dated events of 1960–Jan. 20, 1969 that the book treats and the patch does not enter, for the owner to rule on. The executive's deliberations the book retells from FRUS and the memoirs, without a Senator's part, are marked "a lead" where the calendar lacks them: they are within the calendar's brief, but Mann's pages are a retelling; the executive reading runs (FRUS, Gibbons) should take them from the record.

| Page | Date | Event | Why |
|---|---|---|---|
| 218–20 | Apr.–Dec. 1960 | the Caravelle manifesto, Durbrow's cables, the coup of November, the NLF | already in (`cal.1960-04-26.vietnam`, `cal.1960-09-16.vietnam`, `cal.1960-10-14.vietnam`, `cal.1960-11-11.vietnam`, `cal.1960-12-04.vietnam`, `cal.1960-12-20.vietnam`) |
| 219 | Aug. 1960 | the agrovilles given up | undated |
| 228–29 | Jan. 19, 1961 | Kennedy and Eisenhower on Laos | already in as `cal.1961-01-19.laos` |
| 228 | Jan. 30, 1961 | Kennedy approves the counterinsurgency plan's increases | a lead (executive; FRUS 1961–63, I) |
| 228 | Feb. 1, 1961 | Komer's memorandum | a lead (executive) |
| 229 | Mar. 23, 1961 | Kennedy's televised news conference on Laos | already in as `cal.1961-03-23.laos` |
| 232–33 | Apr. 20–28, 1961 | Gilpatric's task force; Rostow's "Vietnam is the place"; the Sorensen–Bundy–Bell memorandum | a lead (executive) |
| 233 | May 11, 1961 | NSAM 52 | already in as `cal.1961-05-11.vietnam` |
| 234–38 | May 5–13, 1961 | Johnson sent to Asia; Saigon; the late meeting with McGarr (Valeo's account); the communiqué | already in (`cal.1961-05-09.vietnam`, `cal.1961-05-12.vietnam`); the McGarr meeting and the communiqué a lead |
| 240 | May 26, 1961 | Rostow's memorandum | a lead (executive) |
| 243–52 | July 20–Nov. 22, 1961 | Komer; the Taylor mission and report; Ball's warning ("crazier than hell"); McNamara's memoranda; NSAM 111; Nolting and Galbraith | already in (`cal.1961-10-31.vietnam`, `cal.1961-11-03.vietnam`, `cal.1961-11-08.vietnam`, `cal.1961-11-15.vietnam`, `cal.1961-11-22.vietnam`); Komer, Ball of Nov. 7 and Galbraith a lead |
| 267–68 | Sept. 11 and 18, 1962 | Forrestal; Trueheart | a lead (executive) |
| 282 | spring 1963 | the leadership meeting; Kennedy to Mansfield, withdrawal after the election (O'Donnell's account) | undated; a lead |
| 284 | May 12, 1963 | Nhu to the *Washington Post* | already in as `cal.1963-05-12.vietnam` |
| 288–94 | Sept. 2–17, 1963 | Cronkite's and Huntley–Brinkley's interviews; Krulak–Mendenhall; Bundy and Rusk; Kennedy to Lodge on Congress | already in (`cal.1963-09-02.vietnam`, `cal.1963-09-09.vietnam`, `cal.1963-09-10.vietnam`, `cal.1963-09-11.vietnam`, `cal.1963-09-17.vietnam`) |
| 305 | Nov. 24–30, 1963 | Johnson with Lodge; Johnson to Donald Cook | already in (Lodge, Nov. 24); Cook a lead (a recording) |
| 318 | Mar. 17, 1964 | NSAM 288 | already in as `cal.1964-03-17.vietnam` |
| 322 | spring 1964 | Morse's "McNamara's war" | undated; a lead |
| 324 | 1964 | Morse at Utah State | undated |
| 330 n. | Apr. 26, 1964 (?) | Church on Hugh Scott's television program (*New York Times*, Apr. 27) | a lead: the day and the program to find |
| 342–43 | July 1964 | Goldwater's statements, the platform, the acceptance | already in (`elections-1964`) |
| 370 | Aug. 10, 1964 | the NSC after the resolution | already in as `cal.1964-08-10.vietnam-commitments` |
| 378 | Nov. 1, 1964 | Biên Hòa | already in as `cal.1964-11-01.vietnam` |
| 403–08 | Feb. 13–Mar. 2, 1965 | Rolling Thunder approved and begun | already in (`cal.1965-02-13.vietnam`, `cal.1965-03-02.vietnam`) |
| 416 | Mar. 2, 1965 | Johnson to Harold Johnson | a lead (a recording) |
| 418 | Mar. 23, 1965 | a meeting with the leaders | a lead (Mann's day uncertain) |
| 439 | May 16, 1965 | Gallup, 59 percent for the bombing | a lead (Opinion) |
| 440–43 | June 5–18, 1965 | Rusk's office, Johnson drops in; Westmoreland's request of June 7; the NSC of June 11; Johnson to Moyers, "a hitchhiker caught in a hailstorm"; Ball's memorandum of June 18 | already in (`cal.1965-06-07.vietnam`); the rest a lead (executive) |
| 447–54 | July 1–25, 1965 | the Ball, Rusk and McNamara memoranda; McNamara in Saigon; the meetings of July 21–22; Galbraith's memorandum; Clifford at Camp David | already in (`vietnam-july-decision`); Galbraith a lead |
| 452 | July 21, 1965 | the *New York Times* on McNamara's report | out of the brief (a press report) |
| 463 | late July 1965 | Dirksen, Ford and Hickenlooper on the decision (Gibbons, III, 447; IV, 22) | undated; a lead |
| 464 | Aug. 5, 1965 | Taylor to Johnson, "1966 could be a decisive year" | a lead (executive; FRUS 1964–68, III) |
| 469–70 | Nov. 30–Dec. 7, 1965 | McNamara for a pause; the meeting at the Ranch | already in (`cal.1965-12-07.vietnam-pause-2`, which takes Mann's page) |
| 471–73 | May–July 1965 | Thomas Mann and Rusk before Foreign Relations on the Dominican Republic; Holt's research at State; the closed hearings | undated in the book; a lead (the committee's *Executive Sessions*, 1965) |
| 474 | Sept. 1965 | Johnson's letter to Fulbright; the White House statement | undated; a lead (Woods, 387; *Newsweek*, Sept. 27) |
| 475 | late Nov. 1965 | Fulbright to the Commonwealth Parliamentary Association in New Zealand, by prop plane | undated; a lead |
| 476–77 | Dec. 21, 1965–Jan. 12, 1966 | the advisers on the pause; the pause begun; the State of the Union | already in (`cal.1965-12-21.vietnam-pause`, `cal.1965-12-24.vietnam`, the State of the Union) |
| 479 | Jan. 19, 1966 | the $12.7 billion supplemental asked | already in as `cal.1966-01-19.vietnam` |
| 481 | Jan. 17, 1966 | McNamara and Johnson on the pause (FRUS 1964–68, IV, 74–80) | a lead (executive) |
| 482 | Jan. 1966 | Johnson calls Hartke "obstreperous," refuses his nominees | undated; a lead |
| 482–83 | Jan. 1966 | Hồ's denunciation; Sharp's cable; Taylor and McNamara for resuming | a lead (executive; foreign) |
| 484 | Jan.–Feb. 1966 | Dirksen and Kuchel for the resumption | undated; a lead |
| 496 | Feb.–Mar. 1966 | the FBI's name checks of correspondents and watch on the hearings | undated; in `cal.1966-02-24.vietnam-support` in part |
| 497 | Feb. 28, 1966 | Harris in the *Washington Post* | already in (`opinion`) |
| 499 | July 1965 | Humphrey at Detroit, "a long, ugly, costly war" | undated; a lead |
| 503 | spring 1966 | Morse to the *New York Times*: "I blame nobody but Johnson" | undated; a lead |
| 511 | mid-July 1966 | Johnson tells the leaders of $5 to $10 billion more | already in as `cal.1966-07-19.economy` |
| 513 | June 1966 | Moyers: "the people are in a foul mood over Vietnam" | a lead (executive) |
| 514–17 | Sept. 19–Dec. 1966 | McNamara and Johnson on a halt; McNamara's October report; stabilization; Marigold | a lead (executive); Marigold in its thread |
| 519–22 | Jan. 1967 | the messages to Hanoi through Moscow | already in (`vietnam-sunflower`) |
| 527–29 | Feb. 8–13, 1967 | Wilson and Kosygin; Johnson's letter to Hồ; the NSC of Feb. 8; the statement of Feb. 13 | already in (`vietnam-sunflower`); the NSC a lead |
| 529 | early Feb. 1967 | Fulbright at State with Ashmore and Baggs, Katzenbach, Harriman and William Bundy (Ashmore's account) | undated; a lead |
| 530 | Feb. 1967 | Humphrey heckled at Stanford | undated; a lead |
| 531 | Mar. 15, 1967 | Johnson to the Tennessee legislature | a lead (executive) |
| 535 | Mar. 15, 1967 | Sidey to the White House on Robert Kennedy | out of the brief (a journalist's report) |
| 538 | Apr. 1967 | McNamara to Armed Services on the bombing | undated; a lead |
| 547 | June 28–July 12, 1967 | Bunker's report; the meeting with McNamara and Wheeler; Apple's "stalemate" (*New York Times*, Aug. 6) | a lead (executive); Apple out of the brief |
| 555 | Sept. 12, 1967 | Johnson to his advisers, "imaginative ideas" | a lead (executive) |
| 561 | Oct. 27, 1967 | McPherson's memorandum on the bombing | a lead (executive) |
| 564 | late Oct. 1967 | Goldberg to Mansfield, Johnson "as nervous as a kitten" | undated; a lead |
| 570 | Nov. 16, 1967 | Westmoreland's White House briefing for members of Congress | a lead (the briefing's transcript) |
| 573 | Feb. 8, 1968 | Bunker to Johnson | a lead (executive) |
| 577–78 | Mar. 1966; Aug. 1967 | Fulbright asks Ball of the Tonkin incidents; Bader set to work | undated |
| 585 | Feb. 27, 1968 | McNamara at the meeting of Feb. 27, by McPherson's notes | a lead (executive) |
| 588 | Mar. 1968 | the polls on the Rusk hearing | a lead (Opinion) |
| 594 | Mar. 11, 1968 | Drew Pearson to Johnson | out of the brief (a journalist's letter) |
| 595–96 | Mar. 2–22, 1968 | Johnson at Beaumont and to the Farmers Union; McPherson, Acheson, Rowe and Bundy to Johnson | a lead (executive) |
| 601 | Mar. 1968 | Russell's recollection of Johnson in tears | undated |
| 611–12 | July–Aug. 1968 | Humphrey's draft plank; Johnson's objections; Boggs | already in (`cal.1968-08-26.elections-1968-chicago`, `cal.1968-08-24.elections-1968`) in part; the July drafts a lead |
| 617–18 | Sept. 1968 | Ball's resignation and *Face the Nation*; Humphrey in South Dakota with McGovern | undated in the book; a lead |
| 621 | Nov. 1968 | Nixon calls Smathers | already in as `cal.1968-11-03.elections-1968-chennault` |
| 627 | Jan. 22, 1969 | Mansfield: Nixon "a good beginning" | out of the span |

## How the list was made

Each chapter's dated events were logged as read (the page, the date, the event, the note and its source), then each was looked for in the calendar on its day in every thread (`./bib find` by date, and a script listing the live entries of the day). The table above is that log less what the patch enters or edits.

## Leads

- The joint Republican leadership's statements of Jan. 11, 1965, put in the Record Jan. 12 at 538; Tower and Thurmond on "appeasement"; Miller's "trial balloon" at the National Committee; Church on Hugh Scott's program (spring 1964); Nixon's statement of February 1964 (in, as `cal.1964-01-31.republican-party`, from Mann and Beschloss: check the day).
- The Foreign Relations Committee's closed hearings on the Dominican Republic, May–August 1965 (*Executive Sessions*, Historical Series, XVII): the days and the witnesses (Thomas Mann, Rusk, Vance, Raborn).
- Dirksen, Ford and Hickenlooper on the July decision (Gibbons, III, 447; IV, 22): the days.
- Westmoreland's White House briefing for members of Congress, Nov. 16, 1967 (Congressional Briefings on Vietnam, Box 1, LBJ Library).
- Mansfield on *Issues and Answers*, Jan. 14, 1968 (transcript, Series XIX, Box 596, Mansfield Papers; Mann, 584 n.35).
- Humphrey at Detroit, July 1965, "a long, ugly, costly war" (Solberg, 278).
