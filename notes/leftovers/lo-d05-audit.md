# Audit of lo-d05 (leftovers: October 1960, the books on the Drive)

The audit of the reader's patch `inbox/2026-11-27-lo-d05.yaml` and note `notes/leftovers/lo-d05.md`, Nov. 27, 2026. The patch was corrected in place. `./bib patch-check` now shows 0 errors and 34 warnings: 17 "one event?" flags and 17 duplicate flags, one pair for each new entry. A scratch copy of the tree, with the patch merged, passed `./bib check` but for those 17 flags.

## What this audit disregarded

Nothing in the brief narrowed what is an entry. The reader's note had left the Bonds for Israel luncheon, the Miami Band Shell and the debates' hours waiting or resting on Wikipedia. This audit worked each of them from the books, as the brief asked.

## What was read

- *Freedom of Communications*, pt. 1 (the owner's copy on the Drive; printed page = PDF page less 17, held on the page images of pp. 146, 259 and on every quotation's page by its running head). Every quotation the patch gives for an hour was found in the text and its page checked.
- *Freedom of Communications*, pt. 3, the joint appearances (the owner's copy on the Drive; printed page = PDF page less 19, held on the images of pp. 146 and 259). It had no card; the card `w.freedom-of-communications-part` was made.
- White, *Making of the President 1960*, 321–26; Wofford, 16–23 and 63–64; Goodwin, 108–09, 121–22 and 125–26; Thomas, *Robert Kennedy*, 101–06; Schlesinger, *Robert Kennedy and His Times*, 216–18 and note 110; Mann, 283–86; Sorensen, *Kennedy*, 188 and 215–16; Sorensen, *Counselor*, 271–72; Gifford, 85–87, 161 and notes 98–99; Nixon, *Six Crises*, 350–51 and 362.
- Yang Shangkun's diary, I, 558–59, and the Deng Xiaoping nianpu, III, 1580, each read on the page image.
- The American Presidency Project's pages for Nixon at the Buffalo War Memorial (Oct. 17) and for Kennedy's statement on his call to Mrs. King (Oct. 26).
- Kallina, *Kennedy v. Nixon*, could not be fetched: Drive's download address returned a sign-in page, so the file is not shared by link. Its rows on the King entry were moved to the new entries by the existing claim map (153 to the sentence, the call and the release; 154 to Robert Kennedy's call; 155 to King's father), not read again.
- Every copy was deleted after reading.

## The ops checked

The reader's patch held 62 ops: 6 adds, 54 edits and 2 `follows`. All were checked against their pages. Every `edit` base was refreshed against the tree just before this note was written; all 58 bases in the patch are current.

- Thirteen pinpoints stood one page off and were corrected: 643 to 644 (the night flight), 595 to 596 (New Castle), 641 to 642 (Columbus), 657 to 658 (Tampa, twice), 699 to 700 and 701 to 702 (Shawnee Mission), 707 to 708 (Green Bay), 763 to 764 (Hamtramck), 817 to 818 (Valley Forge), 835 to 836 (Convention Hall), 777 to 778 (New York University), and 699 to 700 on the Caroline entry. The other hour edits hold as written.
- The three debates (Oct. 7, 13 and 21): the Wikipedia cite and its Check are struck. The hours now rest on NBC's own announcements, printed in pt. 3. For Oct. 7 and 13, NBC radio said on Oct. 6 that both debates would run "from 7:30 to 8:30 p.m., New York time" (145–46). For Oct. 21, NBC radio said on Oct. 20 that the debate would begin "at 10 p.m., eastern time" (259). That entry now takes a `time` at 10 p.m., because no record gives the hour it ended.
- The Caroline entry (`cal.1960-10.elections-1960-kennedy`): the reader removed its Check on the day. But the date rests only on a reading of Goodwin's "the next night" (126), so the Check is back and the edit no longer claims `kind: correct`.
- The drafting committee (`cal.1960-10-02.soviet-union`): the move to Oct. 1 holds. Yang's diary and the Deng nianpu both give Oct. 1 at 1 p.m., each read on the page image. Wu Lengxi's "from Oct. 2" had been cited for the opposite of what it says; it is now a Check. The hour is set: 1 p.m., Moscow.
- *Meet the Press* (Oct. 16): the transcript was read in pt. 3 (244–51) and replaces "To check." The panel went into the line, with the place (Washington). The flight to Ohio now follows the Silver Spring rally, by Kennedy's words there, "tonight we go to the State of Ohio" (615). The Silver Spring rally follows *Meet the Press*: "as I told Meet the Press" (615).
- The night flight to Miami (Oct. 17): the arrival "at two in the morning" falls on Oct. 18. It is now an entry of that day, under R17 and R25b.
- Middletown: Goodwin's "at 4:30," the hour he had to leave (White, 325), is now in the note. No field was set, because the record gives the end of the drafting, not its hour.
- Buffalo (Oct. 17): it now follows the New England stops, by Nixon's words, "as I said earlier today in Hartford, Conn."
- The defense speech (Oct. 18): the reader's one entry held three acts with three hours. It is now three entries, under R25b. Sorensen's drafting until five is one, set before dawn. Kennedy's changes at eight are the second. Goodwin's last draft from 8:30 is the third. The Legion speech now follows the last draft (the toll gate) instead of the night's drafting.
- The Theresa rally (Oct. 12): those on the platform went into the line. Wofford's pages are cited as they read. The conference speech takes the release's planned luncheon (358) as a midday range, with a Check.
- The Lodge item (Oct. 12): it is split under R17. Nixon's answer is now `cal.1960-10-12.elections-1960-nixon` (Los Angeles, Oct. 12–13, with a Check on the day). Gifford (85) and *Six Crises* (350) give no day of their own.

## Added by this audit

- 12 new entries, each claimed in the ledger. Five come from the King split, below. The others are Nixon's answer of Oct. 12–13, the three Oct. 18 entries named above, and the 1 a.m. rally at Rockford on Oct. 24 (from Kennedy's own words at the Coronado Theater, 727; the Coronado follows it).
- The gazetteer row `reidsville-ga`.
- Wichita (Oct. 22) takes the afternoon, from Kennedy that evening: "I spoke this afternoon in Wichita" (700).
- The Bonds for Israel speech (Oct. 31) takes midday, from its own words, "this luncheon" and "here today" (831). A Check notes that the heading calls it a dinner.
- Robert Kennedy at the second debate (Oct. 7) now follows the debate: Thomas, 106, "During the next debate in Washington."

## The King entry of Oct. 25–27, split

The line held five acts over three days. It is now:

- `cal.1960-10-25.king`: the sentence, with Wofford's "six months, later reduced to four" as a Check.
- `cal.1960-10-26.king`: the move to Reidsville before dawn. The two hours given are a range: Schlesinger has 4:30, Mann about 3:30.
- `cal.1960-10-26.elections-1960-king`: Kennedy's call to Coretta King, the morning, at the O'Hare Inn. Sorensen's later judgment is in the gloss.
- `cal.1960-10-26.elections-1960-king-2`: Kennedy confirms the call to reporters in New York late that night. This is the APP statement.
- `cal.1960-10-26.elections-1960-king-3`: his telegram to the Atlanta student committee, from the same APP page.
- `cal.1960-10-26.elections-1960-king-4`: King's father at Morris Abram's office (Wofford, 19).
- `cal.1960-10-26.robert-kennedy-2`: Seigenthaler drives Robert Kennedy to the airport (Thomas, 101–02; Schlesinger, 217).
- `cal.1960-10-27.robert-kennedy-2`: Robert Kennedy's call to Judge Mitchell, dated Oct. 27 by White's "the next morning" and Wofford. A Check names Schlesinger, Thomas and Mann, who put the call on Oct. 26.

The release and the father's word were already entries (`cal.1960-10-27.king` and `cal.1960-10-28.king`). The sources moved to them by `cite` ops, each with its page.

These `follows` links are set: the call after the move to Reidsville; Robert Kennedy's anger after the call; the drive after the anger; Brinkley's bulletin and the release after Robert Kennedy's call.

## For the merger

- The 17 duplicate flags are all distinct events. Settle each with `--take keep`: the reader's six adds (`cal.1960-10-12.elections-1960-kennedy-4`, `cal.1960-10-16.elections-1960-kennedy-7`, `-8`, `cal.1960-10-17.elections-1960-kennedy-9`, `cal.1960-10-17.elections-1960-nixon`, `cal.1960-10-18.elections-1960-kennedy-6`) and this audit's eleven flagged adds (`cal.1960-10-12.elections-1960-nixon`, `cal.1960-10-18.elections-1960-kennedy-7`, `-8`, `-9`, `cal.1960-10-24.elections-1960-kennedy-7`, `cal.1960-10-26.elections-1960-king`, `-2`, `-3`, `-4`, `cal.1960-10-26.robert-kennedy-2`, `cal.1960-10-27.robert-kennedy-2`).
- `cal.1960-10-02.soviet-union` (now Oct. 1) and `cal.1960-10-01.china-leadership-9` record the same act: the committee's first session, Oct. 1 at 1 p.m., in St. George Hall. They should be combined, keeping `cal.1960-10-01.china-leadership-9`, which has the hour, the place and the thread `china-moscow-1960`. The soviet-union line also holds acts of later days: the three weeks' sittings, the work in Peking from the cables, and the disputes. After the combine, those parts should become entries of their own. This audit did not run the combine.

## What still waits, and on what

- The *New York Times* (TimesMachine refused this host). It is needed for the order of Harrisburg and Venice (Oct. 3), of the Biltmore speech, the Council of Women and Mineola (Oct. 12), and of Fulbright and Hagerty (Oct. 26). It is also needed to settle the day of Nixon's answer to Lodge (the *Times* of Oct. 13 and 14, p. 1).
- Oct. 1: the Hyannis Port meeting against the Chicago and Minneapolis texts of the same day. Pt. 1 prints those texts for Oct. 1 and nothing for Sept. 30. No record read settles it.
- Oct. 21: the limousines. Thomas, 106, gives "At the fourth debate" and no hour or order.
- Oct. 18: the Band Shell. Its text has "this morning" only of the day's news (648). White puts all of Miami before the plane at two (325). No part of the day is set.
- Grand View against the Auditorium (Oct. 22): neither text orders them.
- Items seen on pages read and not entered: Anthony Lewis's calls to Wofford, Oct. 26 (Wofford, 19); Coretta King's account to the press (the APP page; Wofford, 20); Nixon's "no comment" through Klein (*Six Crises*, 362). These are still to enter, not leads.
