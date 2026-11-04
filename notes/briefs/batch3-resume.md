# Batch 3, resumed (Nov. 3, 2026)

The twenty readers of batch 3 stopped on Oct. 28, 11:50 p.m., on the spend limit, each in mid-task. Their patches of
Oct. 29 (`inbox/2026-10-29-b3-*.yaml`) are merged (or left with a reason: `git log`, and the merger's note in this
file's last section). Each reader is relaunched fresh: no memory of the first run but its files.

## For every reader

1. Read `CLAUDE.md`, then `notes/briefs/reader.md` in full: the rules in force, R1-R56, among them R13 (the press),
   R14 (military matters), R17 (spans and one event, one entry), R18 (what is not an entry), R35-R43 (the witnesses:
   in force from Nov. 3), R49 and R51 (the ledger and the additive ops). Never read `build/` or a whole list file.
2. Your earlier work: your book-check files in `notes/book-checks/` (the card's surname and title words), your merged
   patch (`git log --oneline -- inbox/merged/` and `grep -l <card> inbox/merged/*`), the ledger's lines with your patch
   names (`grep b3-<name> inbox/new-entries.tsv`). Read where your book-check file says you stopped, and the pages it
   lists as not yet read.
3. Your books: the owner's PDFs in Google Drive, by the ids below (load the Drive tools with ToolSearch; download into a
   new empty directory under the session's scratchpad `books/<your group>/`; never change a file's sharing). Read each
   page you cite off the page image as well as the text (R4, R54). Delete your copies when you finish.
4. Carry on: the pages not yet read, then every passage of the book within the span (1960 to Jan. 20, 1969), as R5
   and R18 rule; and, for the entries your earlier patch made or cited, the witnesses of R35 (the first run logged
   records under the rule of Oct. 28; the conversion made them witnesses, but the studies, memoirs and collections the
   notes cite were left out: register them).
5. Write one new patch, `inbox/2026-11-03-b3-<name>-2.yaml` (a second, `-3`, if the first grows past some 400 ops):
   new entries claimed first in the ledger (`./bib ledger find`, `./bib ledger add`); additive ops wherever you only
   add (R51); `edit` with a fresh base only where you change `c` or rewrite `n`. New witnesses to
   `inbox/witnesses/2026-11-03-b3-<name>-2.yaml`, never the year files; your work's edges to its file in
   `sources/witnesses/by-work/`. `./bib patch-check` your patch until it has no errors.
6. Update your book-check file (what you read, what you entered, Passed over row by row (R44, R48), "## The press"
   (R13), "## Leads" (R50)). Do not merge, fold or commit: the merger does.
7. Working hours: the owner's rule (CLAUDE.md, "Working hours"). If told to pause, stop at a clean point, leave your
   files consistent, and say where you stopped in your book-check file.

## The groups

| Group | Books (card search words) | Drive ids | Earlier patches |
|---|---|---|---|
| staff | McPherson, *A Political Education*; Califano, *Triumph and Tragedy of Lyndon Johnson* | 1BTxAg1STLYFPfTPknnzikmHhcD5sGx9K; 1qh9YNGwqjzrSf7bgtfzWw_L6Hn0oa1Ek | b3-mcpherson (Califano not yet patched) |
| state | Rusk, *As I Saw It*; Ball, *The Past Has Another Pattern* | 1e3uZQw864xl7h_GpNTpHSO30W-Gg33Aq; 1VYYws2ahDVgxIzBmtldkqxYJCx33DVb4 | b3-rusk, b3-ball |
| defense | Clifford, *Counsel to the President*; McNamara, *In Retrospect* | 1d7lxKGFK6pm_Z4EdbKV645yd3Yyyszvw; 1mQHFVkb1YAiCY7YBh9p4iPCOhiyKUiio | b3-clifford(-more) (McNamara not yet) |
| kennedy | Sorensen, *Kennedy*; *Robert Kennedy in His Own Words*; Guthman, *We Band of Brothers* | 1eMfcd_TINCTAI8pTye3ohh4nlAARwSiL; 1EGJ91-4gtWTlZJ9Ctcv5KDwzZ3o1DJAC; 1YCgq4U-svodqwu1qU9ka2ICR5a2RPXEt | b3-sorensen |
| humphrey | Humphrey, *The Education of a Public Man*; Solberg, *Hubert Humphrey* | 1JUe2RzlXd_nfLsJXMBy3H6WH49vgF-D0; 1rv7Q65c0Jia-lDppii4qe-QoW5Pn6EOJ | b3-humphrey, b3-solberg |
| 1960 | Nixon, *Six Crises*; White, *Making of the President, 1960* | 17sI8Jav8-_lO_B7ZDQR4bwB2GfFeVCIS; 1kae4kYa_YxKPz_35HKfIYzQQk7B54XU1 | b3-six-crises(-more), b3-white-1960 |
| 1964 | White and Gill, *Suite 3505*; White, *Making of the President, 1964*; Novak, *The Agony of the G.O.P.* | 19tJFKPq_l9L0hbpkrvXeh15Um2p-ztX6; 1heqak_1ped-w7tPu0oOA1xWyZfw3O7sK; 1OBjMPaii-8qeHVydUAqV4MgtgCwzp9bL | b3-suite-3505(-more) |
| 1968 | Chester et al., *An American Melodrama*; White, *Making of the President, 1968* | 12zMqX6m96ObRFw0ho-YDEzKZDUpKgXnv; 1Rwfq9JHrB1pdef9seI3MfblwJ5Gj7omm | b3-chester(-more) |
| westy | Westmoreland, *A Soldier Reports*; Berman, *Lyndon Johnson's War* | 1iR4zCqiS6W2N1cetqS-oL5qFJLFghypo; 1WL8fd1vE8-ws-U0iDozej97YVvcVhJMz | b3-westmoreland |
| soviet | Fursenko and Naftali, *One Hell of a Gamble*, *Khrushchev's Cold War*; Dobrynin, *In Confidence* | 17DBFzR13FQP4qRmxOtYcw_rf32mKqG9v; 15i7_Os1UTxm4-EzLRK8JcR0Dp6R_oCXW; 10QgMAGW7kkUW26I6daKc37iUP9Dk4ol2 | b3-fursenko-gamble |
| cuba | Bissell, *Reflections of a Cold Warrior*; Jones, *The Bay of Pigs*; Paterson, *Contesting Castro* | 1Cwaz9jMKfI3uhsR9YXEDvmVEfxCoyrma; 1o8lWJUG1lP8xreYzh2Cskg3LLSo7zlj8; 1PqDWXHNLrHyCxly1deBpCUpCI-e3AlRS | b3-bissell, b3-jones(-more) |
| branch1 | Branch, *Parting the Waters* | 1l7D-yekFQPD_jSriaoHbXlRgA44Co0tD | b3-branch-ptw-1 |
| branch2 | Branch, *Pillar of Fire* | 1Qy6Ia5k69ZoiMuq5sBszzwVvFRc3Ji4Q | b3-branch-pof-1 |
| branch3 | Branch, *At Canaan's Edge* | 1lLz_NMbtg0wjtg3iIsMfmcR62IhAIDJU | b3-branch-ace-1 |
| hill | Mann, *The Walls of Jericho*; Kotz, *Judgment Days* | 1Q5WXirErb1AgAw2bUkXGw3hPGJkt-b-D; 1Zw1l68mszWBSxdd1WcJCZib-0hLOfe-n | b3-walls-of-jericho |
| rfk | Navasky, *Kennedy Justice*; Shesol, *Mutual Contempt*; Thomas, *Robert Kennedy* | 1vqSGPsW36yFB_1Wnaz4WGt-E13RE4uA_; 1C_NeAlP7gG-1oL_LkCGdmOovyCR23cFa; 1jofUsGX9BcH18F_zlWkPTIE8XYuIhjX6 | b3-navasky |
| gop | Kabaservice, *Rule and Ruin*; Goldberg, *Barry Goldwater*; Smith, *On His Own Terms* | 11m7KXywDzwh-lkFWKjhjznKCsgG1sQvI; 1meBgl58QAEq3I6H4-Vn58GLs5XeScZck; 1Y572A1k7PdvXl8CFInR9gS7gphe84TET | b3-kabaservice(-more) |
| advisers | Preston, *The War Council*; Bird, *The Color of Truth*; Woods, *J. William Fulbright*; Woods, *Fulbright: A Biography* | 1XLA43EZrAz2zr0yyIf60TFYcX149yjWp; 10jrYYg-uRuQJSsACk9oQVTyBQGa5IlWF; 1HQv5xHGc6iKUkZdZwy7GkyRUgbecaduM; 1RdlzfOarIZkEAUUJ2KLoEel-1U8Spbph | b3-preston |
| greatsociety | Sundquist, *Politics and Policy*; Zelizer, *The Fierce Urgency of Now*; Bernstein, *Guns or Butter* | 1ExXVHzgFgUm3EGfEhdUbS4K5V2hlYpJN; 1jzLs1pgP-zyYZFareoqLZdj4LG6qrVkz; 12qiEzZniU-FNF4O8HocS9TpLHFn6xQfT | b3-sundquist |
| macv | MACV Command Histories, 1964, 1965, 1967 (3 parts), 1968 (2 parts) | 1qOJyn0edA9EzhtMmuZCdkxRb2sSl2iJs; 1Nd9hm3ZSjQqsRpb7Xoo9hxvNmCkSHT_W; 16aijqcOo1pt2CFJVrsAddc1TyfpvmDJ0, 1mGZVPkiCzoIVBTYRKYq3ydWw1aIt25ha, 1wg20QAZca5wjZSnPyEC9PwTfo91ifpch; 1mmjroe4XDgP92Vgi5QDQJnD6u99NvpVx, 1O_Ds_OWwY5ue7H2N8kEtEZHI6MixetEQ | b3-macv-1964(-more), b3-macv-1965 |

## The merger's notes

(Written after the merge of Oct. 29's patches.)

Merged Nov. 3-4, 2026, all 32 patches of Oct. 29 (`inbox/merged/2026-10-29-b3-*.yaml`), each by `./bib merge --auto
--legacy`, and fifteen small follow-up patches of the merger's own (`inbox/merged/2026-11-0[34]-b3-followups-*.yaml`,
`2026-11-03-cq-1968-08-02-reagan.yaml`). What was done, for the next merger:

- Ids taken since Oct. 29 (by the CQ readers, the other batch-3 patches, or claimed in the ledger by the readers now
  at work): the patch's adds renumbered to the next free `-N`, every reference in the patch and its -more rewritten
  (chester 35, white-1960 17, preston 20, westmoreland 6, solberg 8, clifford 5, chester-more, humphrey 3,
  kabaservice 1). The held tables in the book-checks name the old ids: they were mapped through the renumberings.
- Edits whose base the tree and git no longer know: rewritten as additive ops (cite with the patch's units, to-check,
  check, src's via rows, names), the rest of the stale note left as the tree has it. An edit on a current base that
  drops a Check or a cite (the reader's ruling: not borne out, or a Check settled) was held out of the patch and
  applied by hand on its base after the merge (six-crises 3, white-1960 5, sundquist 1, walls 2, westmoreland 1,
  suite-3505 1, humphrey 1, navasky 1); where the entry had changed since, rebuilt on the newer note.
- A note listing several FRUS documents after one label ("FRUS 1961-63, XI, docs. [63](...), [64](...)") made the
  map's rows for the later documents name nothing: split, a document an item (ball, rusk, westmoreland).
- The "one event?" flags: about a thousand, read pair by pair. Kept apart: distinct events of one day and thread. Combined
  (the older or the tree's id kept, the other its alias, the c and n joined by hand, the map rebuilt): the Chicago
  march of Apr. 27, 1968; Humphrey at the Press Club, June 20, 1968; McCarthy at Davis, May 28, 1968; Humphrey's China
  statement, July 12, 1968; the Hilton raid, Aug. 30, 1968; Unruh's motion, Aug. 26, 1968; the platform hearings'
  opening (Aug. 19, CQ's Aug. 20 a Check); Pigasus, Aug. 23, 1968; Clifford's arrival in Saigon, July 14, 1968; Burke's
  debrief of the NSC, May 5, 1961; the Tyson meeting, Apr. 12, 1962; the Senate's rules ruling, Jan. 28, 1963; *Meet
  the Press*, July 10, 1960; Nam Dong, July 6, 1964. Left apart, for a reader: the Cabinet of Apr. 20, 1961, in two
  entries (`cal.1961-04-20.vietnam`, the Gilpatric task force; `cal.1961-04-20.cuba-2`, Bowles's notes): one meeting.
- Field conflicts: notes joined by the merge (notemerge); maps joined, their letters checked against the entry's units
  and shifted where a reader had inserted a unit before others (cal.1960-11-14.transition-and-staff,
  1963-06.republican-party, 1965-02-10.vietnam, 1964-05-24.vietnam); four c conflicts on press conferences where two
  readers each appended (both kept).
- The book-checks' "For entries in pending patches" tables applied as cites once their entries landed (Chester,
  Solberg, Bissell, Clifford, Kabaservice, Mann, MACV, Westmoreland, White, Sorensen, Rusk, Sundquist); Chester's
  Sept. 29, 1968 entry (`cal.1968-09-29.elections-1968-3`, Solberg's row) was never written: Solberg's pinpoint
  (382-83) not applied.
- b3-preston: its reader registered none of the records its 543 `via` rows name (no cited-records file, no witnesses):
  the rows dropped; the records stand in the notes' "To check:". A reader should register them (R35-R43) and map them.
- Leads copied into `notes/leads.md` under their headings, a section a book (sundquist, solberg, humphrey were in
  already); no book-check had "## The press".
- Small mends on the way: Lundahl, Sevareid out of Names (no entries); Ginsburg (not Ginsberg) in two Humphrey
  entries; diacritics; seasons written month first ("Mar., spring"); a thread that does not exist taken out of `also`;
  `name:nolting-frederick-e-jr`, `name:smith-bromley-k`, `w.galbraith-ambassadors-journal`.
- The Oct. 31 CQ reader's held cite on Reagan before the Platform Committee (Aug. 2 issue) applied when Chester's
  entry landed; its lead taken out of `notes/leads.md`.
- In the first commits the readers' new `inbox/new-entries.tsv` lines and `inbox/2026-11-03-witness-test.yaml` were
  swept in by `git add -u inbox/` (f65afd5, 481e1df, 4624b62): the files as the readers left them, nothing changed.


(The second merger, Nov. 4, 2026, after the second run's first 23 patches.)

Merged, each by `./bib merge --auto` (no `--legacy`), its pending witnesses folded alone (`fold.py FILE`), checked,
committed and pushed: rusk-2, ball-2, humphrey-2, solberg-2, sorensen-2, rfk-own-words-2, guthman-2, white-1968-2,
suite-3505-2, white-1964-2, novak-agony-2, paterson-2, bissell-2, jones-2, navasky-2, shesol-2, thomas-rfk-2,
fursenko-cold-war-2, dobrynin-2, mcnamara-2 (with the defense reader's `inbox/witnesses/2026-11-03-b3-clifford-2.yaml`),
califano-2, califano-3, mcpherson-2 (`inbox/merged/`). No pending file for humphrey-2, dobrynin-2, califano-3. The same
practice as before; for the next merger:

- The "one event?" flags, some 350, read pair by pair (helper: `dups2.py` in the scratchpad's `merge2/`: each flagged
  entry with its three likeliest neighbors). Kept apart: distinct acts of one day or month (a call apart from the
  meeting, two memoranda, two cables). Combined (the tree's or older id kept, the other its alias; c and n joined by
  hand, the map rebuilt against the new units): Humphrey's visit turned back at the White House (the reader's own
  combine, KEEP's c, note and map); the $750 check, May 7, 1960 (Solberg's into White's); Wittenberg College, Oct. 17,
  1960; Johnson's call to Nixon, Nov. 3, 1968 (White's into the Chennault entry); Goldwater's Senate-office meeting,
  Dec. 1963 (both Whites); Rowe's questioning of Humphrey (White's August a Check); Robert Kennedy to Guthman on
  Jackson, July 9, 1960; Johnson to Robert Kennedy on the civil rights bill, Jan. 1964; Bundy to Lodge, Oct. 29, 1963
  (one cable, FRUS IV, doc. 236); McNamara's news conference of June 16, 1965. And the pair the first merger left: the
  Cabinet of Apr. 20, 1961 (`cal.1961-04-20.vietnam` into `cal.1961-04-20.cuba-2`, also Vietnam).
- Ball's two same-day flags kept (`--take keep`), as the reader asked. White 1968's Miami Beach entries of Aug. 5-7 and
  press entries of Aug. 27 read against their days: distinct; its three "set only n" edits applied as written.
- Check errors of the readers' patches mended by hand on the way: seasons and stretches in `when` written month first
  ("Summer" -> "June, summer"; "Late Dec." -> "Dec., late"; "Mid-Dec." -> "Dec., mid-month"), a span's `date` set to
  its first day (Feb. 17, 1966; Aug. 5, 1968; Nov. 23, 1963; Apr. 23, 1968), a month-only `date` where the day was a
  guess (July 1965, Stevenson's body), each moved to its place in date order (`reorder.py`); a `follows:` across days
  taken out; Names without a name entry taken out (Hechinger, Dearden, Fletcher, Edward Bennett Williams), others
  tagged (Eisenhower, Brown, Adams, Higginbotham, J. Irwin Miller); polls and force levels `ok:result-form`; the Ho Chi
  Minh Trail `ok:diacritics`, Điện Biên Phủ marked; "327 I.C.C." `ok:section-ref`.
- Navasky's cite on `cal.1968-05-24.king` waited in `inbox/deferred.yaml` and was applied when thomas-rfk-2 landed.
- `x.1969-07.clifford-a-viet-nam-reappraisal` was in both the Clifford and the Berman pending files; Clifford's is now
  folded, so `inbox/witnesses/2026-11-03-b3-berman-2.yaml` will be refused by `fold.py` until its row is dropped or made
  an `amend:` (the westy group's merger).
- Leads copied into `notes/leads.md`, a "(batch 3, second run, ...)" section a book under each heading; "## The press"
  rows into `notes/press.md`, by date, the work and page last (Rusk, Ball, Humphrey, Solberg, Sorensen, Guthman, White
  1968, Suite 3505, White 1964, McNamara).
- Not committed by the merger: `inbox/new-entries.tsv` (pruned by each merge; the readers still claim in it), the
  readers' book-check and by-work files, and every other group's inbox files. Check's errors in the readers' open files
  (Zelizer's, Smith's, Branch's and Bird's by-work edges, the Clifford/Berman id) came and went as they wrote; none was
  the merged work's.


(The third merger, Nov. 4, 2026, 8:30 p.m.-midnight Pacific, after the second run's last patches.)

Merged, each by `./bib merge --auto` (no `--legacy`), its pending witnesses folded alone (`fold.py FILE`; a book's
shared -2 file after the last patch that used it), checked, committed and pushed: branch-ptw-2 to -5, kotz-2,
walls-of-jericho-2, branch-pof-2 to -5, branch-ace-2 to -4, kabaservice-2, goldberg-2, smith-rockefeller-2 to -5,
six-crises-2, white-1960-2, sundquist-2, zelizer-2, bernstein-guns-2 and -3, preston-2 and -3, bird-2 and -3, woods-2 to
-4, westmoreland-2 and -3, berman-2, macv-1964-2, macv-1965-2, macv-1967-2, macv-1968-2 and -3; and, at the lead's word,
kotz-3, bernstein-guns-4, shesol-3 (43 patches; `inbox/merged/`). Left in the inbox, being written or not assigned:
bernstein-guns-5 to -7, fursenko-cold-war-3, kotz-4, woods-fulbright-1 and -2. For the next merger:

- Before merging: `cal.1960-11-01.elections-1961` renumbered `cal.1960-11-01.elections-1960-2` (patch, ledger,
  book-check); twelve withdrawn ledger claims pruned, and Shesol's two. Berman's Clifford row was already gone.
- Patches refused by `--auto` for a src row whose page the note does not cite (`via ... 745 n.2` on a note citing 724;
  MACV 1968's `34 n.18`, `35 n.19`): the row taken out of the patch, the To check or Check kept. bernstein-guns-4 was
  refused until its edges were in the by-work file: append the "# edges for" block first (`edges.py` in the
  scratchpad's `merge3/`: comment rows or live rows, `card` dropped, the block cut from the pending file).
- The "one event?" flags, about 1,150, read pair by pair (`dups2.py`; `keepdups.py` resolves the rest as keep).
  Combined (the tree's id kept, the other its alias, c and n joined, the map rebuilt): McPherson's memorandum of June 13,
  1967 (FRUS V, 197); Harris's California poll of May 29, 1964; the House's opening debate on the education bill, Mar.
  24, 1965; Fulbright's call to Johnson, Apr. 1, 1968 (into `cal.1968-04-01.vietnam`, which holds the recording). Split:
  Johnson's 8:56 p.m. call to Reuther, Aug. 21, 1964, out of Branch's Jenkins-call entry into Kotz's. Left apart with a
  Check: Curtis's two replies to Rockefeller, July 1963. Left apart: Harris's two California readings of June 1, 1964
  (different figures).
- Hand edits: (a) MACV 1965, 37-38, off `cal.1965-03-06.vietnam` (it stands on -2); (b) `cal.1964-02-29.defense` takes
  the civil rights answer (1963-64 Pub. Papers 322, item 16, read) and Kotz 119; (c) `cal.1964-11-28.vietnam` takes the
  Hoover-King answer (item 11, p. 1617, read), Branch 532, and Kotz 231 as kotz-3's cite (its edit turned into a cite);
  (d) the July 28, 1965 news conference's three rows joined into `x.1965-07-28.the-presidents-news-conference-july-28`;
  (e) Heller's notes of Nov. 23, 1963: the OCR-garbled undated row joined into
  `x.1963-11-23.notes-on-meeting-with-president-johnson`; the two Nov. 25 rows left apart (two repositories; a lead).
  The joins: `inbox/witnesses/2026-11-04-merger-joins.yaml`, folded.
- Mends on the way: whens month first ("Jan." not "January"; "Dec., late"; "Apr., spring"), day-dates the source does not
  give made month-only, spans dated by their first day and moved (a merger's patch,
  `inbox/merged/2026-11-04-merger-moves.yaml`, for two across months); curly quotation marks straightened (pof-2 on);
  name keys the readers coined (`rockefeller-nelson-a`, `meredith-james`, `elson-roy`, `moynihan-daniel-p`,
  `schwengel-fred`) to the series'; Names without an entry taken out (Wachtel, Zinn, Jim Clark, Belafonte, Kirk,
  Lehman); `mayors-chicago` (no thread) made `mayors`; printed titles with plain Khanh, Ky, Thieu, Hue `ok:diacritics`;
  shares and counts `ok:result-form`; three Berman edges added so his via rows reach their witnesses.
- Two code matters. `witnesses.problems` walked the whole registry for every via row; with the batch's witnesses
  folded, check took fifteen minutes: the reachable set now made once an entry (b7f7e24; the same answer, about a
  minute for check). And since 1fef08c (notemerge's clock rule) three map rows naming a FRUS link inside a Check failed
  [claims]: the rows taken out (9a5b432).
- Bird's starred footnotes ("212 n.*") are left as written: the via rows key on them; check warns [italics] three times.
- Leads and press: every book-check's new "Leads" into `notes/leads.md`, a section a book under each heading, and its
  "The press" rows into `notes/press.md` (the four-column tables given a kind; month-only dates as "1960-06").
- For the owner: the bundled entries `cal.1964-11-18.civil-rights-the-executive` (Hoover's remark, the package of Nov.
  21, the meeting of Dec. 1: pof-4's reader proposes a split), `cal.1968-03-14.robert-kennedy` (the Clifford meeting and
  the announcement of Mar. 16) and `cal.1968-04-24.elections-1968` (Freeman's endorsement and the next day's), both
  Shesol's reader's, `cal.1967-07-25.civil-disorders-3` (July 25-Aug. 2: Hoover's two reports and Johnson to the Cabinet)
  and `cal.1968-04-01.vietnam` (the strike of Apr. 2 with the call of Apr. 1); Six Crises' newsweekly forecasts dated
  "Oct. 25-Nov. 7"; Zelizer's Passed over not kept row by row (R44, R48); the many MACV entries of an office's routine
  (R18's "minor").


(The fourth merger, Nov. 4, 2026, midnight-1 a.m. Pacific, after the batch's last seven patches.)

Merged, in order, each by `./bib merge --auto` (no `--legacy`), the edges at its pending file's foot appended first to the
card's by-work file (`edges.py` in the scratchpad's `merge4/`), its pending witnesses folded alone, checked, committed and
pushed: kotz-4, fursenko-cold-war-3, bernstein-guns-5, -6, -7, woods-fulbright-1, -2 (`inbox/merged/`). The inbox is
empty; the ledger too. For the next merger:

- Before merging: the seven claims the readers never used pruned from the ledger (Bernstein's three, Woods 1995's
  four); no other claim of these patches was left. `sources/witnesses/by-work/woods-fulbright.yaml` made, with the
  usual header, for Woods 1995's edges (402 from the two pending files, and one added by hand: 281 n.21, the *Times* of Nov. 11, 1961, which
  a via row named and no edge reached).
- `x.1974.fager-selma-1965` was not yet in the registry (kotz-3 had not folded it): kotz-4's row folded as written, and
  bernstein-guns-6's edge to it then held.
- The edits (kotz-4's three, woods-1's two, woods-2's one) all applied on their bases with no conflict; each held
  against the tree before (nothing other runs wrote was lost).
- The "one event?" flags, 174, read pair by pair (`dups2.py`; `keepdups.py`). Combined: the congressional leaders'
  meeting of July 27, 1965 (Woods's `cal.1965-07-27.vietnam-july-decision` into `cal.1965-07-27.vietnam`, which held the
  meeting and Mansfield's statement; Mansfield's words by Woods added to c as two units, I-J, the note and map joined,
  Woods's Check on the hour kept). All else kept apart: distinct acts of one day (the calls, memoranda and statements
  around Selma, Mar. 7-18, 1965; Branigin's and Sawyer's calls of Aug. 17, 1965; the Senate's and the House
  subcommittee's reports of Apr. 9, 1965; the leaders' meeting of Apr. 28, 1965, beside the entry that names it in
  passing; the Johnson daughters of Mar. 31, 1968).
- Mends on the way: `cal.1961-07-29.right-and-the-military`, the Record of July 29, 1961 out of To check (woods-1 reads
  it); two China entries of Mar. 21 and 30, 1966 moved from the retired slug `india-and-china` (an alias of South Asia's
  thread, not a thread) to `china`; the 5 a.m. call of Mar. 9, 1965 given its `time` (its `time_approx` had none: 11:00Z,
  Selma's Central time); Kennedy and Castro tagged where Names left them ambiguous; Khánh marked (its map's hash
  rewritten); O'Donnell's schedule of Oct. 3, 1964 and the Oakland crowd of Oct. 20, 1967 `ok:result-form`.
- Leads and press: each book-check's run section into `notes/leads.md` (a section a book and run under each heading;
  Bernstein's fifth to seventh runs, written as one paragraph, split into bullets by hand) and `notes/press.md` (the
  four-column tables given a kind). The earlier helpers `leads.py` and `presstab.py` take `--all --last` for a run's own
  section: `--last` alone takes the first.
- For the owner: `cal.1965-07-27.vietnam` still bundles the NSC meeting and the evening's leaders' meeting (R17); Bernstein's
  `cal.1965-03-23.voting-rights-3` spans the Senate hearings, Mar. 23-Apr. 5; Bernstein's ch. 16, 17 and
  19 and Kotz's pp. 77-84 are unread.

- After the last merge: `./bib check` 0 errors, 26 warnings (Bird's three starred footnotes [italics], the Thomson
  cross-reference, the calendar's standing aggregate counts); `./bib audit-cal` committed; a full `./bib build` clean
  (about ten minutes); `./bib links`: 0 links to missing anchors.
