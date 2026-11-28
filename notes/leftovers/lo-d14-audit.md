# Leftovers lo-d14: the audit

Opus audit of the reader's patch `inbox/2026-11-27-lo-d14.yaml` (Nov. 27, 2026), against `notes/leftovers/lo-d14.md` and the 34 rows of `notes/leftovers/lo-d14.tsv`. Every op was held to its page. The patch was corrected in place. `./bib patch-check`: 0 errors; 33 warnings, which are the usual "one event?" and "duplicate of" flags on the new entries and three notices that an edit sets only the note. `./bib fields --patch`: 0 findings.

## Counts

- The reader's patch had 60 ops. 27 stand as written. 32 were changed. 1 was struck: the tag op that took `name:chen-yi` off the Dec. 23 performance, because Chen Yi is now named in that line.
- 19 ops were added. They are listed under each entry below. One of them is a new entry, `cal.1965-01-27.vietnam-5`, claimed in the ledger.
- Two ops are held for the merger in `inbox/held/2026-11-27-lo-d14-saigon.yaml`. See "For the merger" below.
- Three witness amendments are in `inbox/witnesses/2026-11-27-lo-d14.yaml`.
- Every `edit`'s base was compared with the tree as it stands now. All 30 matched the current rev, so none needed refreshing. In git history, the bases of the three edits that follow additive ops on the same entry (Sept. 20, Oct. 14 Chervonenko, Feb. 19) are found, so the merge applies them three-way.
- Nothing in the brief narrowed what is an entry, so nothing was disregarded under R0.

## What was read

All of these copies were deleted when done.

- **Books on the Drive:** the Mao nianpu (EPUB); Zhou nianpu II, 677 and 687–88 (page images); the Zhou *Waijiao huodong dashiji*, 416, 429, 431 and 435 (page images); Chen Yi nianpu, 1075 and 1084 (page images); *Wengao* XVII, 489–90 (page images); Yang Shangkun's diary II, 501 and 508 (page images); Wu Lengxi, 830, 860, 862, 878–79 and 913 (page images).
- **More books on the Drive:** Branch, *Pillar of Fire*, 503, 505–06, 517, 540, 545, 547–48 and 566; Clifford, 400–02; White (1964), 368–69 and 372; Perlstein, 489–90; Califano, 19–20; Kotz, 223–24 and its note 82; Young, 185 and its notes; Cohen, 323; Thomas, 301; Lady Bird Johnson's diary, 214–15, 217–19, 224, 231–33 and 237; Fursenko and Naftali, 535–36 and notes 13–19; Schattenberg, 173.
- **The Vietnam works on the Drive:** McNamara, *In Retrospect*, ch. 6 at nn.18–19; Westmoreland, 94; Taylor, 329–30; Logevall, 292–93 and its note 79; Gibbons II, 381–82; Gibbons III, 77; Kaplan, 528–29; Bird, 304; Moyar, 352.
- **Online:** Cosmas, 207 (DTIC on archive.org); Marolda, 460 and its note 57 (archive.org's text, which this time downloaded).
- **The Wilson Center record:** PRC FMA 109-03957-06, the Drive copy, read in full.
- **Records in the repository:** FRUS 1964–68, I, docs. 451, 453 and 454, and II, docs. 41, 43, 44, 47 and 143 (`sources/frus-text`); the Public Papers for 1964 and 1965, items 662, 748 and 78 with their notes (`sources/ppp-text`).
- **The Miller Center:** the page for conversation 5876 of Oct. 14, 1964, read for its summary. The catalogues in `daybook/recordings/` give its time and place.

## Changes, entry by entry

- `cal.1964-09-20.china-leadership`: The nianpu has Mao reach Jinan 晨 and leave 下午. It gives no hour for the meeting with Boumaza on the train. The added words now say "the morning of his arrival". The range is 5 a.m. to noon, Peking, where the reader had "early morning" only. A Check says why. The quotation in the item is shortened.
- `cal.1964-09-21.vietnam-tonkin`: Marolda was read (460): Sharp answered "on 21 September". Note 57 gives the date-time group, CP 210025Z. A cite of 460 n.57 was added for the time. The Check now says that 21 September is the group's GMT day, and that at Honolulu and in Washington it was still Sept. 20. The date is kept, because the page does not say where Sharp sent the message from.
- `cal.1964-10-02.students` (the pact): The reader cited Branch for the time, but Branch gives 7:20 p.m. against the leaflet's 7:30. Branch is now cited for the truce without `on: time`, and his hour is entered as a variant of the time. The reader's parenthetical had Weinberg "freed"; Branch, 505, has him submit to arrest. That error is gone. Savio's words, the arrest and the dispersal were put into the line with an add-words op.
- `cal.1964-10-02.students-2` (the police): The Branch cite now names its part, "Five hundred police arrive on the campus". Branch gives no hour for it and no 3,000.
- `cal.1964-10-12.soviet-union` and `-2`: Fursenko has Brezhnev's call reach Khrushchev at Pitsunda. The page never puts the word to Palewski at Gagra, so the new entry is placed at Pitsunda, and the note says why. The launch entry's "To check" had lumped three of Fursenko's notes together. Now note 13 stays on the launch, note 18 goes to `-2`, and note 14 goes to `cal.1964-10-12.soviet-union-leadership` by a to-check op. An odd sentence restating the launch date was struck.
- `cal.1964-10-14.china-leadership-2`: Schattenberg (173) and Wu (830, "第二天一清早") bear out the range of 11 p.m. to 6 a.m., Peking. The Schattenberg cite now says it gives the start of the range, not the call.
- `cal.1964-10-14.elections-1964-5`: The Miller Center recording of Fortas's call is now the primary record (5876; Johnson at the Waldorf, per PRDE). The time is 3:56 p.m., set from the record, where the reader had "about 4 p.m.", marked approximate. Perlstein, 489 ("at four that afternoon") was added. White's "early evening" stays as a Check.
- `cal.1964-10-14.elections-1964-6`: Clifford, 401 ("about to call on Jackie Kennedy") was added. It is the basis for the order after the call.
- `cal.1964-10-14.elections-1964-7`: The Public Papers' note puts the President's remarks at 11:20 p.m. That replaces the reader's evening range, which had rested on "the kind of event". The Check on Perlstein's 9 p.m. is gone, because Perlstein agrees with the Papers.
- A follows op was added: the resignation, `cal.1964-10-14.elections-1964`, after the call. The basis is Clifford, 401.
- `cal.1964-10-14.republican-party`: The Check was reworded. Califano gives no hour for the statement; the reader had written that the story was "out" by 7 p.m. Branch's "early evening statement" was added. No record in hand settles the hour, so the Check stays.
- `cal.1964-10-16.china-leadership-6` and `cal.1964-11-07.china-leadership-8`: The page images bear both out. The quotations were shortened. On Nov. 7, the range's sentence was moved before "Names:", and Wu, 860 (晚上, the reception) was added as its basis.
- `cal.1964-10-27.elections-1964-3`: The wake-up is on White, 372, alone. The pin and the claim map were narrowed to it.
- The Lady Bird Special stops (`cal.1964-10-06.elections-1964-johnson`, `-2`, `-3`): Kotz, 223 bears out all three. None has a day, so each keeps "Oct. 6–9" and a Check. Kotz's note 82 (Carpenter, *Ruffles and Flourishes*, 143–71) was added to "To check:". Young, 185 was added to the Columbia stop.
- `cal.1964-11-02.elections-1964-2` (to Oct. 30): The Papers print the Chicago Stadium remarks under Oct. 30, at 8:37 p.m. The President opens on Daley's "political parade and ... political rally", so the torchlight parade and the Stadium are the same evening and the same event. The reader's Check on the parade's night was struck, and the Papers are now cited for the parade too. The merge moves the entry into the October file. The tree has no other Chicago entry on Oct. 30.
- `cal.1964-11-03.robert-kennedy` and `-2`: Thomas, 301 and the recording catalogues bear them out (23:55, Austin). These stand as written.
- `cal.1964-11-13.china-leadership` and `cal.1964-11-13.china-zhou-foreign`: The *Dashiji* (429) has no reception. It has the meeting with the Soviet leaders, then the departure, 晚上, so it is cited for the departure only. The reception rests on Zhou nianpu II, 687. With the Dubna staff gone from the departure entry, its thread moves from the Bomb to the Polemic. The reception takes the Bomb as an "also" thread.
- `cal.1964-12-09.king-2`: The line now follows Branch, 540. Rustin sought out Porter on Oslo's night life, and "the Norwegian girls" were Porter's words about other men.
- `cal.1964-12-20.black-nationalism-2`: The Mau Mau story is told as Branch tells it, with Malcolm's "I go for that". Branch's judgment that the story was "almost certainly apocryphal" went into a Commentary gloss (R19b).
- `cal.1964-12-20.vietnam` (the dissolution): FRUS doc. 451 n.2 has the Military Council meet "late on December 19". Doc. 453 has the events begin "in the middle of the night of 19–20 December". The range is now 10 p.m. Dec. 19 to 6 a.m. Dec. 20, Saigon. A Check on the day was added. Taylor's pin was narrowed to 329. "Taylor" was taken out of "Names:", since he is no longer in the line. The Pentagon Papers' to-check moved to the reproof.
- `cal.1964-12-20.vietnam-saigon` (the reproof): I read each cite the reader had moved there.
    - Doc. 451 n.4 times the meeting "from 12:09 to 1:25", so the range is 12:09 to 1:25 p.m., not the morning.
    - U. Alexis Johnson, Throckmorton and Thi were added to the line, the tags and "Names:".
    - These cites hold: Branch, 545; Westmoreland, 94; McNamara, ch. 6 at nn.18–19 (the "dishes" words; no date); Gibbons II, 381–82 (the mission's record of the opening).
    - Taylor's pin is now 329–30, not 329–31.
    - Logevall's pin is now 293, not 292–93.
    - Gibbons's note 106 (Saigon to State, PP II, 346) joined "To check:".
    - The forward pointer to Dec. 21 was struck.
- `cal.1964-12-23.china-leadership-2` and `cal.1964-12-23.china-zhou-foreign`: Chen Yi, 1075 and the *Dashiji*, 431 bear them out. Mao, Liu Shaoqi, Deng Xiaoping, Peng Zhen and Chen Yi, all present at the performance, were put into the line with their tags. A follows op puts `cal.1964-12-23.china-leadership-5` (the reception of the Cuban guests) after the dinner, on the printed order alone (1075).
- `cal.1964-12-29.china-leadership-4` and `cal.1964-12-29.china-mao`: *Wengao* XVII, 489–90 bears them out (下午六时, 下午九时半). These stand.
- `cal.1965-01-20.transition-and-staff-3`: 8:45 a.m. is when the Johnsons left for the service, not when the service was held. The `time` became a range from 8:45 a.m. to noon.
- `cal.1965-01-22.china-leadership-3` (to Jan. 23): Yang II, 501 bears it out. This stands.
- `cal.1965-01-25.voting-rights-selma`: "Some 250, down Alabama Avenue, the morning" and "The woman, Annie Lee Cooper" were put into the line from Branch, 566.
- `cal.1965-01-27.transition-and-staff-2`: The line now opens on the act that has the hour, the visit "a little past 7". The call is its circumstance (R25b).
- The Bundy–McNamara memorandum of Jan. 27: The memorandum is one act, `cal.1965-01-27.vietnam-2`. The meeting at 11:30 a.m. is a second act, `-3`. Neither is a duplicate of the other, so nothing should be combined.
    - Kaplan, 529, Cosmas, 207 and Bird, 304 were all read. They bear out the memorandum and were cited on `-2`, with their notes' via rows and "To check:" items.
    - Moyar, 352 was cited on `-3`. Its "what we ought to do" is a variant against "what we have to do".
    - Johnson's cable to Taylor of 9:46 p.m. (FRUS II, doc. 44, read) is a new entry, `cal.1965-01-27.vietnam-5` (R8). It carries Bundy's mission, which the Saigon entry had held.
    - The Saigon entry's own correction is held for the merger (below).
- `cal.1965-02-10.china-leadership-3`: The record (109-03957-06) bears out Feb. 10: at 3:20 p.m. Zhou speaks of "our mass meeting this morning", with Liu Ningyi's speech. A sentence was added: Yang's same entry for Feb. 9 has Kosygin back from Vietnam "today", which every other source puts on Feb. 10.
- `cal.1965-02-19.vietnam-2`: FRUS II, doc. 143 sets the meeting for 11:30. The Papers' note to the Gronouski swearing-in, at 12:45 p.m., says Couve "had met with the President just prior". The `time` became a range from 11:30 a.m. to 12:45 p.m., and the Papers were added to the primary record.
- Stand as written: `cal.1964-09-27.china-leadership`, `cal.1964-10-01.students` (the pointer struck), `cal.1964-12-09.king`, `cal.1964-12-20.black-nationalism`, `cal.1965-01-04.program`, `cal.1965-01-09.china-leadership`, `cal.1965-01-12.japan`, `cal.1965-01-21.transition-and-staff-2`, `cal.1965-01-23.china-leadership`, `cal.1965-01-27.transition-and-staff`, `cal.1965-02-04.republican-party-congress`.

## For the merger

- **The duplicate flags:** settle all 15 as distinct, with `./bib resolve ID --take keep`. Each is a separate act of its day: `cal.1964-10-12.soviet-union-2`, `cal.1964-10-14.elections-1964-6`, `-7`, `cal.1964-10-06.elections-1964-johnson`, `-2`, `-3`, `cal.1964-11-03.robert-kennedy-2`, `cal.1964-11-13.china-zhou-foreign`, `cal.1964-12-09.king-2`, `cal.1964-12-20.black-nationalism-2`, `cal.1964-12-20.vietnam-saigon`, `cal.1964-12-23.china-zhou-foreign`, `cal.1964-12-29.china-mao`, `cal.1965-01-27.transition-and-staff-2`, `cal.1965-01-27.vietnam-5`.
- **The held ops:** `inbox/held/2026-11-27-lo-d14-saigon.yaml` holds the edit and the tag op for `cal.1965-01-27.vietnam`. The edit takes the memorandum, the meeting and the cable out of the Saigon line and points to `-2`, `-3` and `-5`. The works that drop out of its note are the ones this patch cites on `-2`. `patch-check` refuses the edit because it counts a move only to an entry the same patch adds. Merge it after the main patch with `./bib merge inbox/held/2026-11-27-lo-d14-saigon.yaml` (not `--auto`). A merge in a scratch copy applied it, and `check` then had 0 errors.
- **Merging the main patch:** a merge of the main patch in a scratch copy, then `./bib check`, gave 0 errors. The copy had no git, so it needed the three three-way edits taken by hand.
- **The witness amendments:** `inbox/witnesses/2026-11-27-lo-d14.yaml` holds three.
    - Gibbons III, 77: the NSC record of Feb. 10 is note 93 and Cooper's notes are note 94. The by-work file has them as n.83 and n.84. Repoint both edges in `sources/witnesses/by-work/gibbons-u-s-government-and.yaml`, and the via row `III, 77 n.83` in `cal.1965-02-10.vietnam`, to n.93.
    - The third joins the two rows for Bundy's memorandum of Jan. 27 (`x.1965-01-27.mb-to-lbj-jan-27-1965` absorbs `x.1965-01-27.bundy-to-johnson-january-27-1965-nsf`).

## What still waits

- **`cal.1964-10-14.republican-party`:** the hour of the Republican statement waits on a record: the *Times* of Oct. 15, or the wire services' logs. Neither is readable here. The Check lists the five readings.
- **`cal.1964-09-21.vietnam-tonkin`:** the day of Sharp's message waits on where he sent it from.
- **`cal.1964-10-14.elections-1964`:** the resignation keeps a range placed by "the kind of event". Branch, 517 puts the announcement at 10:15 p.m. That announcement may be an entry of its own.
- **`cal.1965-01-27.vietnam-3`:** the line still carries the evacuation from State's cable of 8:48 p.m. (FRUS II, doc. 43). By R8 and R25b that cable is an entry of its own.
- **The notes not registered:** Young, 185 n.36 (Fuller, *The New Republic*; the White House's "Story of the Lady Bird Special"; Donaldson, *Liberalism's Last Hurrah*, 274, which has no card) and Logevall, 293 n.79 (Taylor's cables of Dec. 20–23). Young's Charleston sign, "Black Bird Go Home", is not entered, because it rests on Donaldson.
