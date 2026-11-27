# Commentary the audits struck, put back as glosses (R19b)

Patch: `inbox/2026-11-27-gloss-recovery.yaml` (patch-check: 0 errors). Not merged. Sources searched: `notes/notes-pass/audit-*.md`, the via-read, sequence, leftovers and threads audits, and the readers' patches as committed before their audits.

## Restored as gloss (7)

- `cal.1965-11-10.china-leadership`: the Liu Shaoqi chronology (1996) says Yao Wenyuan's article "opened the prelude" to the Cultural Revolution; added as the first paragraph of the entry's gloss, the title changed from Estimates to Commentary; read Liu nianpu (1996), II, 628, as a page image.
- `cal.1966-08-05.china-leadership`: the same chronology calls Mao's poster "aimed chiefly at" Liu; new gloss; read II, 648 (and 649, whose "the plenum turns to the exposure and criticism of Liu and Deng" is a later act and stays out).
- `cal.1964-05-06.civil-rights-bill`: Larry O'Brien's "shook hell out of them", which Purdum says O'Brien "would recall"; new gloss; read Purdum 278 and its note, which cites the Miller Center's Johnson tapes (TPR, vol. 6, p. 528), not read here, so whether O'Brien said it on the day is open.
- `cal.1964-06-07.states-and-cities-us`: Hess and Broder (1967), the Governors' "attempted power play" against Goldwater that collapsed; new gloss; read Hess 31–32 (the phrase runs across the page break).
- `cal.1964-12-28.china-leadership`: Mao to Snow, Dec. 10, 1970, that Liu opposed the "capitalist road" point at the meeting, and Hu Qiaomu's different account (Liu spoke only of overlapping contradictions); two paragraphs in a new gloss; read MacFarquhar, *Origins*, III, 431 and note 1 (Snow's interview date). MacFarquhar gives no date for Hu Qiaomu's statement.
- `cal.1968-09-10.elections-1968`: Christian's insistence that the Legion speech was written a week before Humphrey's Houston statement, and O'Brien's "That isn't how I remember it"; new gloss; read Chester, Hodgson and Page, 633–34.
- `cal.1966-08-19.jobs-and-wages-airlines`: Siemiller's boast that the settlement "destroy[ed]" the guidelines, with Califano's "irresponsibly—but correctly" and "indeed dead"; new gloss (Califano gives no day for the boast); read Califano 146. The note keeps its own mention of Siemiller.

## Restored to the record (1)

- `cal.1964-05-06.civil-rights-bill`: John Stewart's diary of that day ("a minor miracle" if the pro-civil-rights forces get back in order), added to the line by `add-words`, attributed, cited to Purdum 278–79; read the page. Stewart has no name entry, so no tag.

## Left struck (1)

- `cal.1964-07-26.vietnam-congress`: "no talk of Vietnam is reported" is the reader's inference from Lady Bird Johnson's diary, not a source's commentary; it stays in the note.

## Not taken up, and why

- Struck as another act, not as commentary: Eisenhower's "fine hand of Emmet" (audit-02, June 8, 1960), Joseph Kennedy's view (audit-04), the later memoirs of who drafted the directive of Oct. 5, 1966 (audit-08: kept in the note; they tell an earlier act, so I left them), Wallace's statement after the returns (audit-06, already an entry).
- The other audits (via-read, sequence, leftovers, threads) strike for order, date, duplicate or another act; I found no commentary struck in them. The search was by words, so a passage struck without those words could be missed.

## The audit

Audited on Opus, Nov. 27, 2026. Every page the patch cites was read in the owner's copy on the Drive, and every copy was deleted after. The patch was corrected in place; `./bib patch-check` shows 0 errors and 4 warnings (each new entry is flagged as a possible duplicate of the other entries of its day and thread; each is a separate act, to be kept with `./bib resolve ID --take keep` at the merge).

What held, read on the page:

- Liu Shaoqi nianpu (1996), II, 628: "揭开了"文化大革命"的序幕" ("opened the prelude"), read on the page image. The gloss holds.
- Liu Shaoqi nianpu (1996), II, 648: "主要针对刘少奇" ("aimed chiefly at Liu Shaoqi"), read on the page image. The gloss holds.
- Hess and Broder, 31–32: the passage runs across the page break. The gloss holds.
- MacFarquhar, *Origins*, III, 431 and the note on 639: Snow's interview was Dec. 10, 1970. The gloss holds.
- Chester, Hodgson and Page, 634: Christian's account and O'Brien's reply. The gloss holds.
- Purdum, 278–79: Stewart's diary is "for the day", so it belongs to the day's record. It stays in the line.

What I changed, and why:

- O'Brien's "shook hell out of them" (May 6, 1964) is not a later recollection. Purdum's note cites the Johnson tapes, and the tapes (*The Presidential Recordings*, VI, 527–28, read on the page image) have O'Brien saying it to Johnson by telephone on May 8, 1964, at 6:11 p.m. So I took the gloss off the May 6 entry. O'Brien's words now go into the line of the May 8 call (`cal.1964-05-08.civil-rights-bill-2`), with Humphrey and Dirksen named and tagged, and a Check that Purdum calls them a recollection.
- In the same call O'Brien tells Johnson what he said to Humphrey after the votes of May 6. That talk is a dated act, so it is a new entry, `cal.1964-05-06.civil-rights-bill-6`, timed after the Senate rose.
- Siemiller's boast that the airline settlement "destroy[ed]" the guidelines was said at the time, not later, so it is the record, not commentary. It is now its own entry, `cal.1966-08.jobs-and-wages-airlines` (August, after the 19th; Califano, 146, gives no day, so the entry has a Check). Califano's "irresponsibly—but correctly" and "indeed dead" are his own later comment and are that entry's gloss. The edit to the Aug. 19 entry is dropped.
- Nov. 10, 1965: the first paragraph had "Commentary." in front of it, which the build would print twice, since the title runs into the first paragraph. I took it out. The other kind's paragraphs now open with their title, "Estimates.", as the gloss guide asks. While on the page I also found that the note misread the nianpu's footnote: Yao was on the board of *Jiefang ribao*, not *Jiefangjun bao*. The edit corrects the note.
- Dec. 28, 1964: Hu Qiaomu's words are dated by the work that first printed them, Cong Jin (1989), not by MacFarquhar (1997). Mao's paragraph now says the point is the first of the Twenty-three Articles. A short paragraph adds MacFarquhar's note that the words are in article 2, not article 1.
- Hess and Broder, and Chester and the others: I cut the long quotations from these copyrighted books to a few words each. Chester's pinpoint is 634, not 633–34.
- Stewart's diary: I shortened the quotation in the line.

Commentary the reader's search missed, found in the audit notes and the patches' history, read on the page, and added:

- `cal.1964-05.middle-east`: struck in audit-02 as "the author's framing". Friedman (2015), 110–11, says that the visit came just after Zhou Enlai's African tour and that Khrushchev needed Nasser to restore Soviet prestige. That is a historian's analysis, so it is now the entry's gloss.
- `cal.1965-08-11.states-and-cities`: struck in audit-07 as "framing". Purdum (2014), 332, calls Watts, five days after the Voting Rights Act, "a portent of widespread unrest to come". That is now the gloss.
- The Eleventh Commandment: struck from `cal.1966-06-07.elections-1966` in audit-07 as "the campaign, not the vote". Kabaservice, 171–72, gives Nofziger's interview of Oct. 10, 1978 and his own judgment. Both are now the gloss of the Commandment's own entry, `cal.1966-03.elections-1966`.

Found in the same search, and not commentary:

- Washington's precincts (struck in audit-13 as "background"). White (1965), 134, gives a state of affairs at the end of 1963. A thing a source reports for a date is an entry on that date, so it is a new entry, `cal.1963-12.goldwater-9`. White, 133–34, also has Luke Williams joining the draft when Clif White came to Seattle in June 1963; that is added to the trip's entry, `cal.1963-06.goldwater`.
- Left as the audits left them: Eisenhower's "fine hand of Emmet" (Smith, 341: a remark at the time, undated, reported in 1962); Jacqueline Kennedy's words to Bartlett (Thomas, 285: undated, at the time); Joseph Kennedy's view (his view at the time); the 1957 act's terms (a law of 1957); the drafters' memoirs of Oct. 5, 1966 (accounts of an earlier act, kept in the note).
- The sequence, threads, clock-time and *Times* audits strike links, threads and other days' acts. Read through, they struck no commentary.
