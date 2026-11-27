# Leftovers lo-a: what was done with each item

Patch: `inbox/2026-11-27-lo-a.yaml` (`patch-check`: 0 errors). Records read this pass: FRUS in `sources/frus-text/`, the Public Papers in `sources/ppp-text/`, the Congressional Record on govinfo (the PDFs fetched, not the Drive), and S. Rep. No. 94-465 and 94-755, Book III, from intelligence.senate.gov. Nothing came from the Drive. The *Times* is not readable here (R56), so every item that needs a page of it waits, as does every item that needs a book held only on the Drive. Where a split makes the merge flag a duplicate, the merger settles it with `./bib resolve ID --take keep`.

## 1960

- `cal.1960-01-14.soviet-union` split: done. Dulles's report to the NSC is now `cal.1960-01-14.soviet-union-2` (FRUS 1958–60, X, pt. 1, doc. 140, read); the old line keeps the speech, and the Fursenko Check moves with the report.
- `cal.1960-01-19.japan-and-korea` hour: done. The Papers' note puts the signing in the East Room after the luncheon that began at 2:06 p.m. (1960–61 Pub. Papers 112–13); the kind range is replaced by a record range from 2:06 p.m. to 5 p.m. Eastern.
- `cal.1960-01-19.japan-and-korea` split: done. The announcement of Jan. 20 that Eisenhower would visit Japan is `cal.1960-01-20.japan-and-korea-treaty` (Pub. Papers 113, note; FRUS XVIII, doc. 134, read).
- new, Kishi–Herter talks, Jan. 19: done as `cal.1960-01-19.japan-and-korea-treaty-2` (FRUS XVIII, docs. 139–146, read: 3:30 to 5:30 p.m.).
- new, toasts at the luncheon, Jan. 19: done as `cal.1960-01-19.japan-and-korea-treaty` (Pub. Papers 110–12, read: 2:06 p.m.); the signing now follows it.
- `cal.1960-02-13.testing` map row: done. The *Bulletin* row is taken off both parts, on the audit's reading of page 361 (I did not open it); the note's Check already says the page names no place, day, yield or message.
- `cal.1960-05-05.vietnam-congress` map row: done. FRUS 1958–60, I, doc. 154 (read) is an editorial note on Mansfield's letters and Williams's reply; its row now covers the Mansfield part only.
- `cal.1960-06-15.japan-and-korea` split: done. The riot stays; Kishi's cabinet's request is `cal.1960-06-16.japan-and-korea-treaty` (FRUS XVIII, doc. 182, read: the meeting "has just decided"; announcement set for 5:30 p.m.); Eisenhower's answer in Manila is `-2` (Pub. Papers 495, note) and his message to Kishi is `-3` (FRUS doc. 184, 8 p.m. Manila). `when` is now "June 15".
- `cal.1960-06-28.economy-debt-limit` order: done. The Record (106 Cong. Rec. 14,700–11, read on govinfo) has the conference report taken up at 14,700 and adopted 61 to 32 at 14,711; the "Check: the page" is settled and the note links the pages.
- `cal.1960-06-28.soviet-union-u2` order: done. Fulbright's report is at 14,734, after the vote at 14,711, so the entry now follows `economy-debt-limit`.
- `cal.1960-06-30.jobs-and-wages` order: done. Smith's speech on the rule is at 15,187–88 and the roll call on passage, 341 to 72, at 15,226; `jobs-and-wages` follows `cal.1960-06-30.congress`, which now cites 15,187–88 in place of its "To check".
- `cal.1960-06-30.medicare` order: done as far as the Record goes. S. 3784, Saltonstall's bill, is at 15,064 (listed at 15,063). The page bears the introduction, not the fees, and the cite says so. No other Senate entry of the day carries a Record page to order it against, so no link.
- `cal.1960-06.cuba-bay-of-pigs` To check: done. FRUS 1961–63, X, doc. 231 is read through (67,000 characters; no safe house, Coral Gables, job placement company or Panama); it is linked in the Check and taken out of the "To check".
- new, cancellation of the Japan visit, June 16: done as `cal.1960-06-16.japan-and-korea-treaty-2` (the White House release in the note to Pub. Papers 495).
- `cal.1960-07-01.cuba-3` place: done by the dateline, Havana (`notes/nyt/dating-a.tsv`); the Times page itself not read.
- `cal.1960-07-02.congo` day: no change. The existing Check covers the day and the places; the July 3 page cannot be read here.
- `cal.1960-07-02.cuba-8` registry: already done. The note points to `cal.1960-07-02.cuba`, the sugar bill's first entry.
- `cal.1960-07-04.china-leadership-2` cite: waits on the Chinese source's page (Drive).
- `cal.1960-07-04.cyprus`, `cal.1960-07-04.latin-america-dominican-republic`, `cal.1960-07-04.press-and-broadcasting` splits: wait. Each needs the *Times* page of July 5 for the hour and order of its two acts.
- `cal.1960-07-05.democratic-party` and `cal.1960-07-05.elections-1960-los-angeles-7` duplicate: waits. One occasion or two turns on the Sitton and Egan pages of July 6 (the *Times*); the Check on -7 stays.
- `cal.1960-07-05.democratic-party-4` and `-5` place: done, Los Angeles, by the dateline (`notes/nyt/dating-c3.tsv`).
- `cal.1960-07-05.middle-east` Argentina's note of June 8: confirmed. `cal.1960-06-08.middle-east` holds it, cited to the *Times*, July 5, 1960, at 8.
- `cal.1960-07-05.south-asia-3` clause: done. "The Cabinet met twice the week before" is struck (it is `cal.1960-06-27.south-asia`'s, from the same item); the note says where it is entered.
- `cal.1960-07-05.soviet-union-3` place: done as Villach (new place key, Europe/Vienna, in Austria), the dateline in `dating-c3.tsv`; the paper is the Salzburg one, but the page is not in hand to put the act at Salzburg.
- `cal.1960-07-06.cuba-2` cite: already cited. The Szulc item of July 6, at 1, 3, was in the note; it moves with the law.
- `cal.1960-07-06.cuba-2` split: done. Havana's Law 851 is `cal.1960-07-06.cuba` (place Havana, the *Times* cite and the law's terms with it); the Washington entry keeps the act and the signing; the map rows are rewritten; the Aug. 6 and Oct. 24 entries now point to the new entry. Oct. 19 and Dec. 16 point to the old one for the sugar quota and stay.
- new, Font at the Miami airport, July 3; Robert Kennedy's statement, July 3; Connally's secret-ballot caucuses, July 4; Meyner, Di Salle, Symington, Lawrence, Pauley, Loveless, Draft Stevenson, Meany, July 5; the Mongolian shake-up, July 5; Frondizi with Macmillan, July 6: wait. Each is a *Times* item and cannot be read here.
- `cal.1960-09-06.antisubversion`, `-2`, `congo-4`, `immigration`, `intelligence-2`, `latin-america-dominican-republic-3`; `cal.1960-09-07.antisubversion`, `-2`, `intelligence`, `elections-1960-kennedy-7` (place): wait. The datelines are not recorded and the clippings are not on the Drive.
- `cal.1960-09-06.vietnam-2` merge risk: moot. The entry already has c4's note and "Names: Li Fuchun."
- `cal.1960-09-07.elections-1960-kennedy-6` day and `-7` clipping: wait for the *Times* of Sept. 9 and Sept. 7.
- `cal.1960-09.cuba-3` Edwards's testimony, May 30, 1975, 5–7: waits; the transcript is not held and not online here.
- `cal.1960-10-26.elections-1960-kennedy-7` order: waits for the *Times* of Oct. 27, at 29.

## 1961

- `cal.1961-01-03.congress` and `cal.1961-01-03.republican-party-congress` order: part done. The Democratic caucus met at 9:45 a.m. (the note's own Ritchie, 577) and the Senate was called to order at noon (107 Cong. Rec. 1, read); the caucus now has `time` 9:45 a.m. with a row for it, and `cal.1961-01-03.rules` follows it. The Republican conference has no hour in anything read; it waits for Wolff, 867 (Drive).
- `cal.1961-01-10.cuba` cite: done. The note now has the author, the head and "at 1", with the TimesMachine link by date.
- `cal.1961-02-01.congo` split: done. The NSC meeting is `-2` and Kennedy's approval is `-3` (FRUS XX, docs. 18 and 19, read); the memorandum keeps its line and the bibliography.
- `cal.1961-02-08.cuba` hour: done. Bundy's memorandum (FRUS X, doc. 39, read) says "this afternoon"; the entry takes the afternoon band as a record range.
- new, Kennedy's news conference, Feb. 1: done as `cal.1961-02-01.economy-2` (Pub. Papers 30, read: 4 p.m.).
- `cal.1961-04-13.berlin-and-vienna` hour: done. The note to Pub. Papers 265: spoke at 5 p.m.; `time` replaces the kind range.
- `cal.1961-04-20.cuba` hour: done as the afternoon (Pub. Papers 307, item 1: the statement "yesterday afternoon").
- `cal.1961-04-20.cuba-bay-of-pigs` hour and Checks: done. Pub. Papers 307, item 5: Nixon with Kennedy "last night" (Apr. 20); the night band is set and the three Checks are replaced by a sentence that names the Papers and the differing readings (*Six Crises*, May; Reeves, Apr. 19).
- `cal.1961-04-20.republican-party` day: waits. Nixon's "the morning" is *RN*, 233 (Drive); the Papers do not mention the Hill meeting.
- `cal.1961-04-29.vietnam` hour: done. FRUS I, doc. 40 (read): the NSC met at 10 a.m.; `time` is set, with a row.
- `cal.1961-05-29.latin-america` quotation: done. The report prints "principal" (read on the page image, p. 213); the line now says so, as `kind: correct`.
- `cal.1961-06-13.cuba` and `cal.1961-06-13.cuba-2`: one occasion. FRUS X, doc. 230 has the Study Group make its final report orally, and its n.3 points to doc. 229, the 5 p.m. meeting. Merger: `./bib combine cal.1961-06-13.cuba cal.1961-06-13.cuba-2`.
- `cal.1961-08-31.testing-2` src row: the hour is on `cal.1961-08-31.berlin-and-vienna` (4 p.m., FRUS XIV, doc. 135, n.2), not on `testing-2`; the row is added there.

## 1962

- `cal.1962-02-27.transition-and-staff` Campbell: confirmed. The report (S. Rep. No. 94-465, 129–30, read) says "the President's friend" throughout and the note already says "the friend unnamed"; the pin is now 129–30, parts 3 and 4 being on 130.
- `cal.1962-03-20.soviet-union-space` day: settled as it stands. The letter is dated Moscow, Mar. 20 (FRUS VI, doc. 43, read); Kennedy "received this morning" on Mar. 21 (Pub. Papers 254). The note says both.
- `cal.1962-03.king` page: confirmed. PDF page 91 is printed 88 and the link is right; Book III (read) names "Adviser A", not Levison, and the note now says so, with the dates of the microphone and the tap.
- `cal.1962-03.king` To check: done. Book III, 88 is the page the note cites; the "To check" is struck.
- `cal.1962-08-06.economy` and `cal.1962-11-16.economy`: the Miller Center row is narrowed to the meeting itself (the catalogue has no transcript); the words stay with Zelizer.
- `cal.1962-08-10.economy`, `-16`, `-20`: nothing more. Their Miller rows already cover part 1 only, and the quotations are labelled as Gavin's.
- `cal.1962-11-20.missile-crisis` split: done. Collins's question (7) is `cal.1962-11-20.missile-crisis-4`, after the housing order (Pub. Papers 831–32, 834, read).

## 1963

- `cal.1963-01-14.europe-and-the-alliance-2`: waits. FRUS XIII, doc. 57 (read) gives no hour for de Gaulle's conference; it needs the transcript volume or Ball, 269–70 (Drive).
- `cal.1963-01-18.congress-2`: waits for Monroney and Baker (Drive).
- `cal.1963-05-21.alabama-birmingham` page: done. Morse is at 9140 (PDF page 76), not 9139–40; the note, link and row are changed.
- `cal.1963-06-27.europe-and-the-alliance-kennedy-in-3` (11:30 a.m.), `cal.1963-06-28.europe-and-the-alliance-kennedy-in` (10:15 a.m.), `-6` (5 p.m.), `cal.1963-06-29.europe-and-the-alliance-kennedy-in` (noon): done, from the Papers' notes; Ireland on summer time.
- new, Dublin Airport 8 p.m.: done as `cal.1963-06-26.europe-and-the-alliance-kennedy-in-3`. The Papers date it June 26 (item 274), not June 28; the arrival entry follows it.
- `cal.1963-09-18.vietnam-3` split: done. Telegram 431, 4:52 p.m., is `cal.1963-09-18.vietnam-5` (`vietnam-4` was taken); doc. 128 reads "home truths", not "hard truths", and the new entry says so.
- `cal.1963-09-24.testing` page: done. The roll call, 80 to 19, is at 17,832 (read); the Check is settled.
- `cal.1963-10-05.vietnam-2` hour: waits. Forrestal's memorandum gives 9:30 a.m. and the recording catalogue 11 a.m.; the recordings list different participants, so they may be two meetings. Only the recording settles it (PRDE).
- `cal.1963-10-29.civil-rights-bill-2` hour: done. The recording catalogue (`daybook/recordings/1963-10.yaml`) and Purdum, 142–43, agree on 9:30 a.m.; `time` replaces the morning range.
