# Audit of the lo-c settling and its splits patch

Nov. 27, 2026. The audit of the merger's work on leftovers lo-c: the 52 entries settled in `lists/cal/` (commit a08b2f52, note `notes/leftovers/lo-c-settle.md`) and the patch `inbox/2026-11-27-lo-c-splits.yaml`. Nothing in the brief narrowed what is an entry, so nothing was disregarded.

## What I read

Each of the 52 settled entries, set against its two parents as they stood before the merge of lo-c (`git show 4dc67894~1`), with the lo-c patch's check ops on them and the audit note's ruling. A script listed, for each entry, the parents' words, cards, pages, Checks, tags, map rows, variants and fields that the settled entry lacks; I then read every entry whole.

Records read where the parents disagreed, or where a source's support was in doubt:

- Online: the Cow Palace speech of Nov. 2, 1960 and the news conferences of May 8 and May 22, 1963 (American Presidency Project); the Miller Center pages of conversations 1303 (Jan. 10, 1964) and 4129 (July 2, 1964); FRUS 1961–63, X, doc. 158 and I, doc. 31; FRUS 1964–68, V, doc. 238.
- On the Drive, each fetched once and deleted: Zhou Enlai nianpu (1997), II, 303, 387, 452; Yang Shangkun's diary, II, 114; Liu Shaoqi nianpu (1996), II, 634; Zhou Enlai nianpu (2020), III, 38, 63–64; Pu Weihua, *Zalan jiu shijie*, 78 and 253; Schlesinger, *Journals*, 94–97.
- Not reached: the Wilson Center Digital Archive (the Romanian transcript and the Ben Bella record of 1965) refused the connection (HTTP 403, then 502). An APP search for a Johnson trip to Houston in late April 1966 found none; the day of the Fulbright invitation stays open.

## What the records settled

- 1962-01-17: Yang Shangkun's diary (II, 114) names Wang Renzhong (任重), not Song Renqiong, among the first speakers. The line, the tags and the Names are corrected, and the note says so.
- 1960-11-02: the Cow Palace text is dated Nov. 2 and holds both passages, so the Check on the day of the rejoinder is settled. The quotation now reads "ivory in their head," as the text has it; Goodwin has "on."
- 1966-07-13: the Zhou chronology (2020, III, 38) puts the see-off at Shanghai on the 13th, under the heading of July 3–13. The Check that said it put it on July 3 was wrong and is gone.
- 1966-03-26: the Liu Shaoqi chronology (II, 634) dates the talks and the welcome banquet, with Liu's words, on Mar. 26. Its "Islamabad, Mar. 28" is a visit to the capital being built, not the banquet.
- 1967-07-12: FRUS, doc. 238 has Wheeler's words as the line has them. The Check on them becomes a sentence of the note.
- 1964-07-02: the Miller Center's summary of conversation 4129 is the timing of the signing for the best television coverage, so the Check on whether this is the call Purdum quotes is settled.
- 1960-12-01: Schlesinger's journal (95) has Lovett come in for lunch after the drive to Georgetown, and (97) Kennedy say he will call Blair that night.
- 1966-09-24: the Zhou chronology (2020, III, 64) has the report sent out Sept. 23, and Pu (253) has it forwarded Sept. 24. The Check stays.

## What I mended in the tree (under the lock)

- Sources standing for words they did not bear. I cut the line into more parts and moved each source's map row to its own words on 1960-12-30, 1961-06-22, 1963-05-29, 1963-10-16, 1963-11-21, 1963-12-23, 1965-11-21, 1965-12-20, 1966-02-09, 1966-02-25, 1966-04-25, 1966-05-06 and 1966-07-10. Where one source only paraphrases the line, it now has a parenthetical and a `?` row: 1964-04-27 (Deng's chronology) and 1968-04-26 (Dallek). On 1968-06-13 I added the map that was missing, with each CQ issue on its own part. On 1960-12-30 the merged sentence had joined two sources' words so that "which he had refused in Oct. 1959" hung on the wrong clause; the two accounts are now separate parts.
- A source cited twice: 1960-11-22 (Yang, I, 622), 1962-01-17 (three cards repeated), 1964-12-15 (Teiwes), 1966-02-25 (a "To check" item), 1966-05-06 (Yang Jisheng and MacFarquhar), 1967-07-12 (Westmoreland). A source read and dropped from the note: MACV's command history, 478, on 1965-02-08, restored as a source with the Check on its day.
- "Made public" set to the earliest printing: 1963-12-23 (Schlesinger's *Robert Kennedy and His Times*, 1978), 1961-06-22, 1962-07-19, 1963-10-01, 1964-04-27, 1966-07-13 and 1968-06-20.
- Pointers and order. I restored the pointer to the event's first entry dropped on 1964-01-10 and 1966-07-13. I put the note's sentences in order on 1965-02-08, 1966-07-15, 1966-07-28 and 1967-07-12, and gave 1966-06-03-9 its `follows` link to the meeting that agreed to send the work groups, as the audit ruled.
- Names and tags. I took out a repeated name on 1964-04-27 and added Birendra on 1966-07-13. I removed the second `vis:only` tag on 1960-11-22 and 1965-02-23. On 1966-10-17 a work written as plain text is now its card. On 1965-12-20 Trần Văn Thanh is spelled the same way throughout. "Jian Zhou Enlai's account" is now "Chen Jian's account" (tagged `ok:name-untagged`, since the author has no name entry). On 1966-02-09 a Check now marks the ambassador's name, which the books give only in characters.

`./bib check`: 0 errors (1,441 warnings, as before but for two counts). `./bib conflicts`: none.

## The splits patch

Every op was read against the audit note, the tree and the records. Mended in place:

- Three new entries repeated events the tree already holds, against R17, so they are gone and their claims in the ledger released. The later sittings of Jan. 18–22, 1962 are now cites and "Zhou Enlai attends" on the tree's entries of each sitting, and Zhou's revising is added to his entry of Jan. 20. Lovett's lunch of Dec. 1, 1960 is added to the tree's Lovett entry, with the journal's page and the hour. The July 13, 1967 scene and Westmoreland's account are added to the tree's news conference and dining-room meeting of that day, with the Check on Westmoreland's own dating.
- The edits on the six settled entries I mended now carry those mends and fresh bases. Two edits that ran after an add-words op on the same entry would have conflicted at the merge ("base not found"), so they now come first.
- The Oval Office meeting of Apr. 20, 1961 now has Kennedy in the line, his tag, the hour from FRUS (about 11:45 a.m., three-quarters of an hour into the Cabinet), and FRUS's own words for the order. The British approach of Feb. 23, 1965 no longer cites the Ben Bella record, which does not mention it, and its parent's tags are corrected. The Liu banquet takes the Liu chronology's page and a Check on the place. Fulbright's refusal takes a parenthetical for each source. Blair's sounding-out cites the journal at 97. The Rockefeller-for-President reply of Apr. 7, 1968 loses a stray name. Mondale's statement tags Moyers. Two forward links became plain words.
- The State Department experts' sentence of May 9, 1967 is now a cite of Drea, 208 on Bundy's memorandum, which is that advice. The Check that went with it is dropped, because FRUS, doc. 170 shows what they proposed. The McPherson call of Mar. 31, 1968 is one edit, which also takes McPherson's book out of "To check" now that it is read.

`./bib patch-check`: 0 errors, 22 warnings, all "one event?" or "a duplicate of" on the eleven new entries. The patch now has 11 new entries and 67 other ops.

## Fit to merge

Yes. Merged in a scratch copy of the tree, it left only the eleven duplicate flags; after `./bib resolve ID --take keep` on each, `./bib check` ended with 0 errors. The eleven to keep: cal.1960-04-13.china-zhou-foreign, cal.1960-12-01.transition-and-staff-cabinet-4, cal.1965-02-23.vietnam-diplomacy-2, cal.1966-03-26.china-liu-2, cal.1966-03-26.china-liu-3, cal.1966-04-25.vietnam-congress-foreign-relations-2, cal.1967-07-12.vietnam-force-levels-2, cal.1968-06-15.elections-1968-state-conventions-2, cal.1961-04-20.cuba-7, cal.1961-04-20.vietnam-3, cal.1968-06.elections-1968-humphrey-3.

## Left for a later pass

- 1961-08-24: the variant cites Yang Jisheng's *Mubei* at "I, 956" and the note at "II, 956". This was already in the parent and is not checked here.
- 1965-05-22: a witness of the *New York Times* has the id `x.1922-05-21...`, a wrong year. This was already in the parent.
- 1963-10-01 and 1963-10-16 keep the audit's combines. Zhou's comment and Deng's instruction stand in one entry, and Shesol's "to reporters" stands as a part beside the lunch at the *Post*.
- The Romanian and Ben Bella records of 1965 wait until the Wilson Center archive answers.
