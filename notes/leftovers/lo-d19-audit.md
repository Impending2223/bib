# lo-d19 audit (Opus, Nov. 28, 2026)

Audit of the patch `inbox/2026-11-27-lo-d19.yaml` (the leftovers for November 1966 to May 1967) and the reader's note `notes/leftovers/lo-d19.md`. Every op was held to its page. The patch was corrected in place. After the audit, `./bib patch-check` shows 0 errors and 50 warnings. The warnings are the same-day and duplicate flags and the polity tags. Pages are printed pages. Every copy was fetched into a scratch directory and deleted after reading.

## What was read

- *Jianguo yilai Mao Zedong wengao*, XVIII, 463–465, 468–471, 491, 495, read on the page images (the file's page is the printed page plus 27). XIX, 99–100, read on the page images (plus 29).
- The Mao chronology (EPUB): Nov. 22, 1966; Feb. 3, 8, 9 and 11 and May 31, 1967.
- The Zhou Enlai chronology, 2020 edition, III, 91, 94, 106–107, 122, 148–150 and 155, read on the page images (minus 4).
- Yang Jisheng, *Tiandi fanfu*, I, 333–335, 423, 429–430 (text layer), and II, 692 (the page image).
- The Chen Yi chronology, 1176, read on the page image.
- Brezhnev's workbooks, II, 171 and 189, read on the page images.
- McPherson, 314–15. Califano, 161–63 and the source notes, 361–62. Solberg, 302–03 and its notes. Branch, *At Canaan's Edge*, 581–82, 587, 589–90, and the note for 582. Kotz, 373 and n.61. Woods, *Fulbright*, 448–49. Lady Bird Johnson's diary, 518. Thomas, 332 (the page image). MacFarquhar and Schoenhals, 165 with nn.52 and 56, and 201. Gibbons, IV, 559, 568, 601–02, 650. Barrett, 64–65. The MACV command history for 1967, 493–95.
- The 1967 Public Papers, 15–16, 28, 356, 395–99, and the 1968–69 volume, 1160, in the series' text (`sources/ppp-text`). FRUS 1964–68, V, doc. 123 (`sources/frus-text`). 113 Cong. Rec. 6886–91 (govinfo).
- Anthony, *The War in Northern Laos*, 216, from archive.org's DTIC copy (DTIC_ADA512223).
- Rogers, *Cedar Falls–Junction City*, 129–135, from archive.org's copy (CMHPub90-7). The history.army.mil copy still refuses this machine (HTTP 403).

## Corrections to entries already in the tree

- Mao's second note of Feb. 11 (*Wengao* XVIII, 468): the page reads 二月十一日二十二时, which is 10 p.m. The reader's reading holds. The first note, on Ye Jianying's draft, has no hour of its own. It keeps the old id. Its "Made public" is now 2013, because 1988 was the printing of the regulations and that belongs to the new entry. Zhou Enlai comes out of its names and tags, because its line does not name him.
- Brezhnev and Tito, Jan. 28–31 (workbook II, 171): the page holds every hour the reader gave. The station, Jan. 28, is at 10:00, with Kosygin, Mazurov, Andropov, Gromyko and Grechko, and not Podgorny. The leave-taking, Jan. 31, is at 18:00. The breakfast of Jan. 28 now reads "Brezhnev and others", as the page says, not "other members of the leadership".
- Thant's proposal, Mar. 28: the welcome (Public Papers, 395–96) does not mention it. The toast, at 2:17 p.m. at the luncheon (396–98 and the note), does. The split holds. FRUS V, doc. 123 has Thant decide that morning, after Bunche told Goldberg by telephone. That call is now an entry of its own (`cal.1967-03-28.vietnam-thant-3`), and the release follows it.
- The Laos entry of Jan. 22: the reader set only the zone. The page gives "the night of January 22/23", with the barrage "around three in the morning". The time was therefore wrong by a day. It is now 20:00 UTC on Jan. 22, which is 3 a.m. on Jan. 23 in Vientiane. The edit is now `kind: correct`, and its note says why. "By ten they had withdrawn, leaving behind sixty-five dead" goes into the line by `add-words`.
- Bàu Bàng: the unit citation (Public Papers 1968–69, 1160) says "the night of 19-20 March 1967". Rogers, read in full at 129–135, puts the probe at 2250 on Mar. 19 and the main attack at 0030 on Mar. 20. It gives 227 enemy dead, 3 prisoners, and 3 Americans killed and 63 wounded, so the entry's figures hold. The edit is now `kind: correct` and sets `time_zone: Asia/Ho_Chi_Minh`. The note gives Rogers's two hours.

## The two rows that named the wrong id

- Feb. 6, Robert Kennedy: no op lands on `-2`, the morning call to Watson. Thomas, 332, read on the page image, has Kennedy "summoned to the Oval Office at 4 p.m." The meeting entry, `cal.1967-02-06.robert-kennedy`, keeps its 4:34 p.m. from Gibbons. Thomas's hour is added as a variant on the time.
- Mar. 20, Bàu Bàng: the edit lands on `cal.1967-03-20.vietnam-operations`, which is right.

## Nov. 22, 1966: Yang Jisheng against the chronologies

The reader's pinpoint was wrong. The folio in this copy stands at the foot of the page, so the passage is on I, 334–35, not 333–34. This agrees with the tree's own Check and with `cal.1966-11-21.china-leadership-3`. Yang does not plainly date the report Nov. 21. On Nov. 21, Zhou tells Gu Mu and Yu Qiuli that he and Tao Zhu will hear them again "tomorrow". The 10 p.m. call from Li Fuchun follows in the next sentence, with no day of its own. The Mao chronology and the Zhou chronology (III, 91, "于二十二日") both give Nov. 22. Yang's source is Gu Mu's memoir, 218, which is not on the Drive. So the records do not settle the day beyond doubt. The variant stays, reworded to say what the page says, and the Check stays.

## The two hours that wait (Jan. 6, 1967)

A Drive search found neither Xu Jingxian's *Shinian yimeng* nor Chen Pixian's memoir, by title in Chinese or in English. MacFarquhar's note 56 is Xu's recollection, and note 52 is Chen's. Neither gives an hour. The words "By Xu Jingxian's account" (165 n.56) hold. Both Checks stay.

## Ops changed

- New entries: 30 checked. All are borne out by their pages, apart from the changes below.
- `cal.1967-01.transition-and-staff-3`: Solberg's note gives Kiker's *Atlantic Monthly* article as the source of the remark ("Ibid."). It is added under "To check:". In `-4`, the file is "WHCF CF, Exec FG 440, Box 348".
- `cal.1967-05-12.soviet-union-leadership-3`: the workbook names no one at the reception. Zhivkov comes out, and the line now reads "Sofia, evening. A reception, Brezhnev's delegation present."
- `cal.1967-02-09.china-seizures`: the note no longer says the revised draft was "of Feb. 7". Note 1 says the draft Lin sent Feb. 7 had four articles. The Check stays on which reading added articles five and six, because neither the *Wengao* nor the chronology says.
- `cal.1967-02-09.china-leadership` (the morning note): Lin Biao's draft of Feb. 7 is now named in the line. Zhou comes out of its names and tags. The `via … 465 n.3` row is moved off it, because Ye's letter concerns the rule as issued, which is the new entry's matter.
- `cal.1967-06-01.china-wuhan`: the Zhou chronology, III, 155 n.1, is added. It names the June 1 order.
- `cal.1967-02-09.vietnam-air-war`: the note no longer holds the acts of Feb. 10 and Feb. 11 in a parenthetical. Each is now an entry (below).
- `cal.1967-03-16.vietnam-supplemental-3`: the "Check" on the Record's order comes out. It is now a `follows` op that puts the House's debate on H.R. 6950 (`cal.1967-03-16.economy-investment-credit`) after the vote, on the Record's pages 6889 and 6891.
- `cal.1967-03-29.mississippi`: the quotation is now complete ("… could have brought about on their own"). The murder is named as Wharlest Jackson's, because "the Jackson murder" read as the city. The note cites Branch's note on 582 for the transcript. "Names: Reed." comes out, because Clark Reed has no name entry.
- `cal.1967-03.king`: King's leaving for Chicago on Mar. 24 is already `cal.1967-03-24.open-housing`. The line is now about the drafting alone. Kotz has Harding at Morehouse, and Branch has him at Spelman: this is now a Check. Kotz's interviews (373 n.61) are added under "To check:".
- `cal.1966-11-28.transportation`: Califano's note 36, his telephone log of Nov. 28, is added under "To check:". It also gives the day. The Ackley memorandum to Califano of Nov. 26 (163 n.34) is added under "To check:" on `cal.1966-11-25.transportation`.
- `cal.1967-01-06.china-leadership-4`: "Sun Yue fetches her" comes out of Yang's parenthetical. The errand is the new entry's matter.
- `cal.1967-05-09.soviet-union-leadership` (now dated May 10): the place is now Moscow, where the flight leaves and whose clock the 8:25 is. Kuznetsov is added to the names, and Zhivkov comes out of the tags. The note no longer says that May 9 holds nothing, because May 9's work on the papers is now an entry.
- `cal.1967-02-17.vietnam-air-war-2`: `time_zone: America/New_York` is set, matching the note's "3:20 a.m. in Washington".
- `cal.1966-11-30.china-leadership-3`: "The Workers' Gymnasium, evening" is added to the line by `add-words`, cited to the Chen Yi chronology, 1176.

## Entries added by the audit (claimed in the ledger)

- `cal.1967-05-09.soviet-union-leadership-2`: Brezhnev works on the Bulgarian trip's papers, 11 a.m. to 2 p.m. (workbook II, 189).
- `cal.1967-02-10.vietnam-air-war`: Sharp's further report and his order for a maximum air effort after the truce (MACV, 494).
- `cal.1967-02-11.vietnam-air-war-2`: the Chairman of the Joint Chiefs advises that operations against the North will not resume (MACV, 494–95).
- `cal.1967-04-02.king-2`: King preaches at Ebenezer while the changes to the Riverside address are made (Branch, 590).
- `cal.1967-04-02.war-opposition`: Fernandez sends the copies of the address to Heschel and Bennett, and Commager gets his. It follows `cal.1967-04-02.king` (Branch, 590).
- `cal.1967-03-28.vietnam-thant-3`: Bunche's call to Goldberg (FRUS V, doc. 123).

## Ops checked and held as written

The rest hold on their pages:

- the hours: McPherson's "last night"; the 下午 of Feb. 3; the 晚上 of Feb. 8; the 十时 of Feb. 27; the 一时 of Feb. 28; the 凌晨 of May 8; the 中午 of May 31; "a little past 3" on May 13;
- the splits: Califano's Monday call; Boyd's oath and Connor's letter (the Papers do not name Trowbridge, so the Check stays); the reindictment and Clark Reed; the Fulbright protest and apology, by the *Arkansas Democrat* of May 5; Sharp's and Westmoreland's answers of Feb. 17; Zhou's criticism of May 13; the notes of May 31 and the order of June 1; the meeting of May 19 before the 5:38 p.m. meeting.

Each new entry's note keeps only its own act's works.

## Bases and the merge

All 26 `edit` bases were checked against the tree on Nov. 28 and are current. Every new entry draws the duplicate flag at the merge. Each is a distinct act and should be settled with `./bib resolve ID --take keep`:

cal.1967-01-06.china-seizures, cal.1967-01-28.soviet-union-leadership-2, -3, cal.1967-01-31.soviet-union-leadership-2, cal.1967-01.transition-and-staff-3, -4, cal.1967-02-09.china-seizures, cal.1967-02-09.vietnam-air-war, cal.1967-02-11.china-seizures, cal.1967-02-11.vietnam-air-war-2, cal.1967-02-17.vietnam-air-war-4, cal.1967-03-16.vietnam-supplemental-3, cal.1967-03-28.vietnam-thant-2, -3, cal.1967-04-02.king-2, cal.1967-05-05.vietnam-congress-foreign-relations-2, cal.1967-05-09.soviet-union-leadership-2, cal.1967-05-12.soviet-union-leadership-2, -3, cal.1967-05-13.china-wuhan, cal.1967-05-19.vietnam-air-war-2, cal.1967-05-31.china-wuhan, cal.1967-06-01.china-wuhan.

## What still waits

- The hours of Jan. 6, 1967 (`cal.1967-01-06.china-leadership-13` and `-8`) wait on Xu Jingxian's and Chen Pixian's memoirs. Neither is on the Drive.
- The day of the report of Nov. 22, 1966 waits on Gu Mu's memoir, 218. It is not on the Drive.
- `cal.1967-05-19.vietnam-2` holds two acts: Rostow's memorandum, which Gibbons dates after the morning meeting, and the 5:38 p.m. meeting. Under R25b it should be split. It is outside this batch's ops and is left for the next pass.
- Branch, 590, has the *New York Times* print King's interview with Herbers on its front page on Apr. 2. The tree's entry of Mar. 30 cites the story as of Mar. 31, from Branch's note. This disagreement is left for a reader of the *Times*.
