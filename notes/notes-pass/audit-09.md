# Audit of batch 09: the notes pass

The patch is `inbox/2026-11-26-notes-pass-09.yaml`, corrected in place. The reader's file held 152 ops (95 add-words, 54 names, 3 checks), not the 154 its note gives. After the audit it holds 187: 102 add-words, 50 names, 11 edits, 9 checks, 6 new entries, 3 place ops, 3 follows, 2 variants, 1 cite. Of the reader's ops, 74 stand as written; the rest were reworded, repinned, moved or struck, as below. `./bib patch-check` ends with 0 errors and 10 warnings; the warnings are the duplicate-day notices for the six new entries, each a separate act from the entries it sits beside.

Every op was checked against its page. The books were fetched from the owner's Drive with curl, each into its own folder in the scratchpad, and read by their text layer with the printed page number checked on each page used. The Chinese scans (the Zhu De, Chen Yun and Ye Jianying chronologies, and the 2023 *Jianguo yilai Mao Zedong wengao*, XIX) were read as page images. The *Mao Zedong zhuan* was read in its EPUB. The FRUS documents were read at history.state.gov. Everything was deleted after.

## What was read

- Clifford, *Counsel to the President*: 454–55, 476, 503–05, 545–46, 551–52, 559–60, 561–62, 579–81, 592–93 (the file's page minus 40 in this stretch).
- Berman, *Lyndon Johnson's War*: 89–91, 98–99, 112, 119–20, 143–44, 160–62, 184, 194–95.
- Califano, *Triumph and Tragedy*: 246–48, 262–64, 273–74, 298–302, 307–11, 320–22 (the file's page minus 20 here, not minus 4).
- Witcover, *85 Days*: 51–52, 77–79, 92–93, 115–18, 197, 213–15.
- Solberg, *Hubert Humphrey*: 332–33, 353–54, 366–67, 370, 375–76.
- Lady Bird Johnson, *A White House Diary*: 620–24, 776–79 (the printed page is at the foot of each page).
- MacFarquhar and Schoenhals: 246, 274–76, 287–95. Teiwes and Sun: 92–96, 101–02, 106. Jian, *Zhou Enlai*: 584, 619, 623–24. Kotz: 405–07, 416–17. Branch: 646–48, 742–43. Bernstein: 497. Shesol: 406, 455. Longley: 163, 243–44. Chester: 178, 634. White, *1968*: 246–47. Westmoreland: 313. MACV *Command History 1967*: 361. Gibbons, IV: 605 n.145. Khoo: 66–67. Brezhnev, *Rabochie i dnevnikovye zapisi*, II: 253–54, 274–75. Yang Jisheng, II: 721–25.
- The page images: Zhu De chronology, III, 1965; Chen Yun chronology, III, 163; Ye Jianying chronology, II, 978 and 982; *Jianguo yilai*, XIX, 416–17 and 429.
- *Mao Zedong zhuan*, VI, ch. 77 at nn. 61, 77, 79, 80; ch. 78 at n.16; ch. 79 at n.42.
- FRUS 1964–68: V, doc. 364; VI, docs. 35 and 64; VII, docs. 128, 129, 158 and 181; XVII, doc. 81.

## What could not be read, and why

- The Nebraska canvass (govdocs.nebraska.gov): the connection was reset by the proxy, twice. The *West Virginia Blue Book, 1968* (wvlegislature.gov): reset the same way. The Blue Book's copy on archive.org (`westvirginiablue0000vari`) is a lending-library item and refused the text file with a 401. The Drive holds neither (searched by title). The Nebraska figures therefore stand as Chester's and Witcover's, each in that book's name, with a Check against the canvass. West Virginia has no figures in any book read.

## The reader's open points

- **FRUS XVII, doc. 81** (`cal.1968-08-20.soviet-union-czechoslovakia-3`). Read. The link was already the note's first item, so a `primary` op would add nothing. The roster, Johnson's words ("It is aggression") and his instruction ("Tell him we won't make announcement") went into the line by `add-words` with the linked record as its source. The notes give Humphrey the meeting's last words ("We need to show caution"). Clifford, 562, says Humphrey said nothing. The line now gives Clifford's version in Clifford's name, with a Check.
- **The request of Apr. 24, 1969** (`cal.1969-04-24.china-leadership-3`). Add-words cannot put words after this line, because the line ends inside single quotation marks and the tool does not see that a sentence ends there. Written instead as an `edit` (fresh base `4b811f23`). The edit puts the request first, as the editors' note gives it, then Mao's line. It is cited to *Jianguo yilai*, XIX, 429 n.1, the note's own text (R35a). The claim map was set by part, and Lin Biao was tagged. The edit changes no words already in the line, so patch-check requires no `kind:`, and none is stated: an edit that only adds words needs neither `reword` nor `correct` (cuts.py, STYLE 11).
- **Nebraska and West Virginia**: tried again and failed, as above.
- **105,000 against 108,000** (`cal.1968-02-27.vietnam`). The line's 105,000 comes from the FRUS document. Berman and Clifford give the first phase as 108,000 or "over 107,000", and Westmoreland's 108,000 already stands under a Check. No record read settles it, so the line stays (R22) and the Check stands.
- **Lin Biao's speech, Oct. 20 or Oct. 26** (`cal.1968-10-20.china-leadership`). The Ye Jianying chronology, II, 978 (read from the page image), dates the speech Oct. 20, as the Zhou chronology does. MacFarquhar alone gives Oct. 26, "the second session". No record settles it, so the date stays Oct. 20, and MacFarquhar's variant and the Check stay. The new words from MacFarquhar are put in MacFarquhar's name, with the day MacFarquhar gives.
- **Williams at the SCLC meeting** (`cal.1968-03-30.king-poor-peoples`). There is no conflict. Kotz, 406, has Williams arguing against the Washington campaign before King walks out. Branch, 743, has Williams accusing Bevel and Jackson after King has left. These are two moments of the same meeting, and both stand in their authors' names. A Check was added for the length of the meeting: Kotz gives ten hours, and the line and Branch give eight.
- **The arrests of Yang, Yu and Fu** (`cal.1968-03-22.china-leadership`). Jian, 584, does not say "earlier in March", as the reader wrote. It says the three were arrested without warning "in March", with no day, and dismissed on Mar. 22. So there is no conflict over the day, and Teiwes's 22nd is used. The sources do differ on Fu: Teiwes has him transferred, Jian has him arrested. That is now a variant on Teiwes's words, with a Check. The reader's Jian sentence was struck.

## Ops changed or struck, and why

- Wrong page: Witcover 78 should be 77 for Kennedy's "would no longer be necessary". Those words are also Clifford's, at 503, as said at the meeting, and are cited to both. The *White House Diary* has the speakers on 621–22, not 621, and Johnson's look-in on 621, not 622. The Inaugural Address is on 779, not 778. Berman's Douglas quotation is on 91, not 90–91. Branch's passage on King and his staff is on 742–43, not 743. Kotz's is on 406, not 405–06. MacFarquhar's youngest delegate is on 287–88. Shesol's is on 455, not 455–56. The *Mao zhuan* cites were written as "ch. 77 n.61" and the like, which under R35a means the endnote's own text. The words come from the body text, so they are now cited "at n.61".
- Words the page does not bear out:
  - "Wheeler: Westmoreland needs 45,000 men at once" (Feb. 9). The 45,000 is in Johnson's question in FRUS VI, doc. 64. Berman states it without saying who said it. Wheeler's figure is 15 battalions; McNamara's is about 40,000 men. Rewritten from the FRUS document.
  - "at the Hilton" (Apr. 4). The figure is not on Califano's page.
  - "has been sitting too long" (Apr. 5). Kotz prints "It's been sitting too long".
  - "I can teach it either way" (June 29). This is the punch line of Johnson's story about a schoolteacher, not his own remark. The request for two analyses of Fortas's opinions, and Ford's report (dated "June 31"), carry no day of June 29. The op was struck.
  - "all the diplomatic ducks were in a row" (Nov. 2). This is in FRUS VII, doc. 181, not Longley. It is now cited to the record.
  - "Zhang Dingcheng 1,099" (Apr. 24, 1969). This is Yang Jisheng, II, 725, not MacFarquhar. Moved there.
  - Jian's "earlier in March": see above.
  - Teiwes, 102, cited for the Office Group "in effect" replacing the Standing Committee. That is the Zhu De and Chen Yun chronologies' wording, and Teiwes gives no day for Mao's order. Both points are now attributed correctly.
  - "liaison members" (Apr. 23, 1969). The page has 中央文革碰头会, the members of the Cultural Revolution briefing meeting.
  - "Canton". Now Guangzhou (R19a).
  - "Representatives Hayden" (Oct. 23, 1967). Berman lists Hayden among the Congressmen. FRUS V, doc. 364, has Senator Hayden and adds Representative Bates. The roster was rewritten from FRUS, and Berman's list goes under a Check.
- Another act, moved or struck (R17, R25b, R33a). Each of the following was moved to its own entry or struck:
  - The 3:30 p.m. meeting and Clifford's call of Mar. 14, 1968. Two new entries.
  - The White House meeting of Oct. 27, 1968, 7:45 p.m. (FRUS VII, doc. 129; Clifford has 7:30, now a Check). New entry.
  - The Joint Chiefs' "perfectly acceptable military risk" of Oct. 31, 1968. New entry.
  - Dirksen's call to Nixon's camp and Harlow waking Nixon, Nov. 2, 1968. New entry, which follows the 9:18 p.m. call.
  - Humphrey at Houston, Sept. 10, 1968. New entry; the American Legion address follows it, on Solberg, 376.
  - Mao's approval of Mar. 30, 1969. Already the entry `cal.1969-03-30.china-leadership-2`; struck from the entry of Mar. 18.
  - The telephone turns with Tom Johnson and the "when clause" (Aug. 26, 1968). The first are the day before; the second is the act of `cal.1968-08-26.elections-1968-chicago-24`. Struck.
  - Johnson's "Everything we've gained" on the riot entry. Kept on the King entry.
  - Christian's and O'Brien's later recollections on the Legion speech. Struck.
  - Bunker's seven-hour session with Thiệu on Oct. 31. Struck.
  - Kang Sheng's and Jiang Qing's undated remarks on Apr. 14, 1969. Struck; the note already holds a Check on Kang Sheng's day.
- Added from the pages:
  - O'Donnell's "inconclusive bunch of crap" (Oct. 8, 1967).
  - Branch's four battalions and "nearly fifty thousand" marchers (Oct. 21, 1967; the latter under a Check).
  - Ball's and Harriman's words, and the dinner with Rusk and McNamara (Nov. 1–2, 1967).
  - The roster of Jan. 30, 1968 (FRUS VI, doc. 35) and of Feb. 9, 1968 (doc. 64).
  - Morton's hard count of 666 (Aug. 7–8, 1968).
  - Chester's Democratic figures for Nebraska.
  - Yang Jisheng, II, 724, on Mao's words of Apr. 11, 1969, from the recording. This also dates MacFarquhar's "What's wrong with having a few opponents".
  - Yang, II, 723: Lin Biao and Ye Qun voted against Lin.
  - Brezhnev's name and tag on the Čierna entry. The reader said it was already tagged; it was not.
- Rewordings with the same facts: Con Thien (the line already had "over 3,000"); the Berman "built on sand" line (one official's words); DePuy's ratio (Berman gives Goldberg's account of it); the Witcover corridor sentence (it was garbled); the first-meeting congress delegates. The two Kitt pins were also corrected.

## The fields (R25a)

The reader set none. The record gave these, and they were set:
- the hour: Mar. 14, 1968, 11 a.m. (Clifford, 503); Apr. 22, 1968, 10:30 a.m. Moscow (the secretaries' record);
- a part of the day:
  - Oct. 8, 1967, afternoon (Sorensen, in the note);
  - Nov. 1, 1967, the evening dinner;
  - Feb. 18, 1968, Sunday afternoon (Witcover, 52);
  - Mar. 16, 1968, afternoon (Witcover, 92);
  - Mar. 24, 1968, early night in Los Angeles (Witcover, 115);
  - Mar. 25, 1968, the dinner at State;
  - Apr. 27, 1968, the luncheon (Solberg, 332);
- a closer range for the luncheon of Jan. 18, 1968: 12:45 to about 3:55 p.m. (the *White House Diary*, 620, 624);
- places: Washington for Oct. 23 and Nov. 22, 1967; Peking for Apr. 11, 1969 (Hall 118).

The two entries of several days, Nov. 1–2, 1967 and Apr. 22–24, 1968, say in the note that the time is the first day's. Left unset, with the reason:
- the hour of the Aug. 7–8 roll call (1:19 a.m., Aug. 8), on an entry dated Aug. 7 that holds the days before. Splitting that entry under R25b is left for the next pass.
- the place of Čierna nad Tisou, which the gazetteer lacks, on an entry that also holds an act in Washington.

One citation was widened. The Bradley and Bundy words on the Wise Men entry are pinned to Berman 96–101, the item the note already prints, rather than to 99 alone. With the edit that sets this entry's time, an item at 99 beside the existing item at 96–101 made the claim check fail on the existing row.

## Whether it is ready to merge

Yes, as far as the pages go. Patch-check shows 0 errors. The six new entries are claimed in the ledger under `notes-pass-09`. Nothing was merged, built or committed.

## Under R0

Nothing in the brief narrowed what is an entry. Applying R5 and R17 as the brief requires led to the six new entries above.
