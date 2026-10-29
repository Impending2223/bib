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

## The second patch (book-mann-2)

The coordinator's ruling of Oct. 29: a lead means only what cannot be placed or verified, so every event the book dates to the day or the month, within the brief, is an entry. `inbox/2026-10-29-book-mann-2.yaml` (patch `book-mann-2`, 96 operations: 71 entries, 25 edits) enters the rows the first patch had passed over as leads, each checked against its day in the merged tree, FRUS, the Public Papers, the Record or the Daily Digest read first and cited first where they print the event:

- the executive deliberations Mann retells, from FRUS: Komer, Feb. 1, 1961; the Gilpatric task force, Apr. 20; Rostow, Apr. 21 and May 26; Sorensen, Apr. 28; Johnson in Saigon, May 12–13; Komer, July 20; Robert H. Johnson, Oct. 31; Ball with Taylor, McNamara and Gilpatric, Nov. 4; Galbraith, Nov. 20, 1961; Forrestal, Sept. 18, and Trueheart, Sept. 19, 1962; the breakfast of Mar. 2, 1965; the Tuesday lunch of Mar. 23; Wheeler, May 17; Taylor, June 3 and 5; the NSC, June 11; Galbraith, July 22, 1965; Sharp, Jan. 12, and McNamara, Jan. 17, 1966; the CIA, July 23 and 25; McNamara, Sept. 19, 1966; Bunker, June 28, 1967, and Feb. 8, 1968; and as edits (Mann's page, a sentence added, others' cites and rows kept) the meetings of Jan. 20, 22 and 27, 1966, Komer of July 1, 1966, McNamara's report of Oct. 14, the decision of Nov. 11, 1966, the NSC of Feb. 8, 1967, the meetings of July 12 and Sept. 12, 1967, Feb. 27, 1968, and the Taylor report at the NSC of Aug. 5, 1965;
- the Senate and the parties: the joint Republican leadership's statements of Jan. 11, 1965 (the Record, Jan. 12, at 538: the Coordinating Committee proposed); Tower, Thurmond and Miller on Fulbright's "Old Myths," Mar. 1964; Church on Hugh Scott's program, Apr. 1964; Dirksen, Ford and Hickenlooper on the July decision, July 1965; Mansfield on *Issues and Answers*, Jan. 14, 1968; Westmoreland's briefing for members of Congress, Nov. 16, 1967; Foreign Relations on the Dominican Republic (Thomas Mann, May 1965; Rusk, May 21; the closed sessions of July 14–15, 16, 19, 23 and 29, from the Daily Digest); Johnson's letter to Fulbright and the White House's statement, Sept. 1965; Fulbright to New Zealand, Nov. 1965; Hartke "obstreperous," and Mansfield's counsel of a breakfast with Fulbright, Jan. 1966; Fulbright and Ball on the Tonkin incidents, Mar. 1966; Bader set to work, Aug. 1967; Fulbright with Ashmore and Baggs at State, Feb. 1967; Goldberg to Mansfield, Oct. 1967;
- the President and his staff in public and in private: Johnson to Donald Cook, Nov. 30, 1963; to Holland and Bundy on Fulbright's speech, Mar. 25, 1964; Humphrey at Detroit, July 1965; Moyers's "foul mood," June 1966; "every possible item of pressure," Mar. 1967; McPherson, Oct. 27, 1967, and Mar. 18, 1968; Rostow, July 1, 1967; Johnson at Beaumont, Mar. 1, and to the VFW, Mar. 12, 1968; McGeorge Bundy, Mar. 22; Panzer, Mar. 25; Durbrow on the agrovilles, June 6, 1960;
- 1968's campaign: Nixon's Seattle interview, Sept. 24, and his questionnaire, Sept. 29; Ball's press conference, Sept., and *Face the Nation*, Sept. 29; O'Brien to Humphrey and Humphrey in South Dakota, Sept.

An entry dated to the month carries "Check: the day." The Checks the second patch adds where Mann and the record differ: Forrestal's memorandum is of Sept. 18, 1962, not Sept. 11 (the date of the cable it reports); the Beaumont dinner is of Mar. 1, 1968, not Mar. 2; McNamara before Armed Services on the bombing (`cal.1967-01-23.vietnam-supplemental`) was in January, not April 1967; Mann's "Democratic colleague" Fong was a Republican; Moyers's call to Rusk was May 21, 1966, not June; Sharp's cable of Jan. 12, 1966, came before Hồ Chí Minh's letter, not after it; the Daily Digest shows no session of Foreign Relations with Thomas Mann in May 1965. Twenty-one of the adds share a day and a thread with another entry and the merge flags them "possible duplicate"; each was compared with its neighbors and is a distinct event (`--take keep`).

## Passed over

Dated events of 1960–Jan. 20, 1969 that the book treats and neither patch enters, for the owner to rule on.

| Page | Date | Event | Why |
|---|---|---|---|
| 218–20 | Apr.–Dec. 1960 | the Caravelle manifesto, Durbrow's cables, the coup of November, the NLF | already in (`cal.1960-04-26.vietnam`, `cal.1960-09-16.vietnam`, `cal.1960-10-14.vietnam`, `cal.1960-11-11.vietnam`, `cal.1960-12-04.vietnam`, `cal.1960-12-20.vietnam`) |
| 219 | by Aug. 1960 | the agrovilles given up | undated |
| 228–29 | Jan. 19, 1961 | Kennedy and Eisenhower on Laos | already in as `cal.1961-01-19.laos` |
| 229 | Mar. 23, 1961 | Kennedy's televised news conference on Laos | already in as `cal.1961-03-23.laos` |
| 233 | May 11, 1961 | NSAM 52 | already in as `cal.1961-05-11.vietnam` |
| 234–36 | May 9–12, 1961 | Johnson sent to Asia; Saigon | already in (`cal.1961-05-09.vietnam`, `cal.1961-05-12.vietnam`) |
| 243–52 | Oct.–Nov. 1961 | the Taylor mission and report; McNamara's memoranda; NSAM 111 | already in (`cal.1961-10-31.vietnam`, `cal.1961-11-03.vietnam`, `cal.1961-11-08.vietnam`, `cal.1961-11-15.vietnam`, `cal.1961-11-22.vietnam`) |
| 282 | spring 1963 | the leadership meeting; Kennedy to Mansfield, withdrawal after the election (O'Donnell's account) | undated; a lead |
| 284 | May 12, 1963 | Nhu to the *Washington Post* | already in as `cal.1963-05-12.vietnam` |
| 288–94 | Sept. 2–17, 1963 | Cronkite's and Huntley–Brinkley's interviews; Krulak–Mendenhall; Bundy and Rusk; Kennedy to Lodge on Congress | already in (`cal.1963-09-02.vietnam`, `cal.1963-09-09.vietnam`, `cal.1963-09-10.vietnam`, `cal.1963-09-11.vietnam`, `cal.1963-09-17.vietnam`) |
| 305 | Nov. 24, 1963 | Johnson with Lodge | already in |
| 318 | Mar. 17, 1964 | NSAM 288 | already in as `cal.1964-03-17.vietnam` |
| 322 | spring 1964 | Morse's "McNamara's war" | undated; a lead |
| 324 | 1964 | Morse at Utah State | undated; a lead |
| 342–43 | July 1964 | Goldwater's statements, the platform, the acceptance | already in (`elections-1964`) |
| 370 | Aug. 10, 1964 | the NSC after the resolution | already in as `cal.1964-08-10.vietnam-commitments` |
| 378 | Nov. 1, 1964 | Biên Hòa | already in as `cal.1964-11-01.vietnam` |
| 403–08 | Feb. 13–Mar. 2, 1965 | Rolling Thunder approved and begun | already in (`cal.1965-02-13.vietnam`, `cal.1965-03-02.vietnam`) |
| 439 | May 16, 1965 | Johnson orders the bombing resumed | already in as `cal.1965-05-16.vietnam-mayflower` |
| 440–42 | June 5–10, 1965 | the lunch at State; Westmoreland's request; the meeting of June 10 | already in (`cal.1965-06-05.vietnam`, edited; `cal.1965-06-07.vietnam`; `cal.1965-06-10.vietnam-july-decision`) |
| 442 | June 1965 | Johnson to Moyers: "a hitchhiker caught in a hailstorm on a Texas highway" (PBS's transcript) | undated; a lead |
| 447–54 | July 1–25, 1965 | the Ball, Rusk and McNamara memoranda; McNamara in Saigon; the meetings of July 21–22; Clifford at Camp David | already in (`vietnam-july-decision`) |
| 452 | July 21, 1965 | the *New York Times* on McNamara's report | out of the brief (a press report) |
| 469–70 | Nov. 30–Dec. 7, 1965 | McNamara for a pause; the meeting at the Ranch | already in (`cal.1965-12-07.vietnam-pause-2`, which takes Mann's page) |
| 476–77 | Dec. 21, 1965–Jan. 12, 1966 | the advisers on the pause; the pause begun; the State of the Union | already in (`cal.1965-12-21.vietnam-pause`, `cal.1965-12-24.vietnam`, the State of the Union) |
| 479 | Jan. 19, 1966 | the $12.7 billion supplemental asked | already in as `cal.1966-01-19.vietnam` |
| 482 | Jan. 24–28, 1966 | Hồ Chí Minh's letter; the reply to the fifteen Senators | already in (`cal.1966-01-31.vietnam`) |
| 484 | Jan.–Feb. 1966 | Dirksen and Kuchel for the resumption | Dirksen already in (`cal.1966-01-31.vietnam-congress`); Kuchel undated, not in the Senate's Record of Jan. 31; a lead |
| 496 | Feb.–Mar. 1966 | the FBI's name checks of correspondents and watch on the hearings | undated; in `cal.1966-02-24.vietnam-support` in part |
| 497 | Feb. 28, 1966 | Harris in the *Washington Post* | already in (`opinion`) |
| 503 | spring 1966 | Morse to the *New York Times*: "I blame nobody but Johnson" | undated; a lead |
| 511 | mid-July 1966 | Johnson tells the leaders of $5 to $10 billion more | already in as `cal.1966-07-19.economy` |
| 516–17 | Nov.–Dec. 1966 | Marigold | already in (`vietnam-marigold`) |
| 519–22 | Jan. 1967 | the messages to Hanoi through Moscow | already in (`vietnam-sunflower`) |
| 527–29 | Feb. 8–15, 1967 | Wilson and Kosygin; Johnson's letter to Hồ; the statement of Feb. 13; the briefing of Feb. 15 | already in (`vietnam-sunflower`; `cal.1967-02-15.vietnam-congress`) |
| 530 | Feb. 1967 | Javits turns against the war | undated (his later account) |
| 535 | Mar. 15, 1967 | Sidey to the White House on Robert Kennedy | out of the brief (a journalist's report) |
| 547 | Aug. 6, 1967 | Apple's "stalemate" (*New York Times*) | out of the brief (a press report) |
| 570 | Nov. 19–21, 1967 | Westmoreland on *Meet the Press* and at the National Press Club | already in (`cal.1967-11-19.vietnam`, `cal.1967-11-21.vietnam-2`) |
| 594 | Mar. 11, 1968 | Drew Pearson to Johnson | out of the brief (a journalist's letter) |
| 596–97 | Mar. 13–19, 1968 | Mansfield's memorandum; Goldberg for a halt; the meeting of Mar. 19 | already in (`cal.1968-03-13.vietnam-congress`, `cal.1968-03-15.vietnam-205000-2`, `cal.1968-03-19.vietnam-205000`) |
| 601 | Mar. 1968 | Russell's recollection of Johnson in tears | undated; a lead |
| 611–12 | late July–Aug. 1968 | Humphrey's softened draft; Johnson's promise of news from Paris; the VFW speech; Boggs | undated (the draft, the promise); the rest already in (`cal.1968-08-19.vietnam-paris`, `cal.1968-08-26.elections-1968-chicago`, `cal.1968-08-24.elections-1968`); a lead |
| 621 | Nov. 1968 | Nixon calls Smathers | already in as `cal.1968-11-03.elections-1968-chennault` |
| 627 | Jan. 22, 1969 | Mansfield: Nixon "a good beginning" | out of the span |

## How the list was made

Each chapter's dated events were logged as read (the page, the date, the event, the note and its source), then each was looked for in the calendar on its day in every thread (`./bib find` by date, and a script listing the live entries of the day). The table above is that log less what the two patches enter or edit.

## Leads

- Undated in the book, the day to find: Kennedy's spring 1963 meeting with the leaders and his words to Mansfield on withdrawal after the election (O'Donnell's account); Morse's "McNamara's war" (spring 1964), his speech at Utah State (1964) and his "I blame nobody but Johnson" to the *New York Times* (spring 1966); Kuchel for the resumption of the bombing, Jan.–Feb. 1966 (Dietz, 150–51); Johnson to Moyers, "a hitchhiker caught in a hailstorm" (June 1965?; PBS, *Vietnam: A Television History*, "LBJ Goes to War"); Russell's recollection of Johnson in tears, Mar. 1968; Humphrey's softened draft and Johnson's promise of a development in Paris, late July 1968 (Solberg, 346–50).
- Nixon's statement of February 1964 (in, as `cal.1964-01-31.republican-party`, from Mann and Beschloss): check the day.
- Thomas Mann before Foreign Relations in "early May" 1965 (entered as `cal.1965-05.latin-america-dominican-republic`): the Daily Digest shows no such session; the committee's *Executive Sessions*, 1965 (Historical Series, XVII), would give it.
