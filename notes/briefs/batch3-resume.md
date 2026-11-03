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
| advisers | Preston, *The War Council*; Bird, *The Color of Truth*; Woods, *J. William Fulbright* | 1XLA43EZrAz2zr0yyIf60TFYcX149yjWp; 10jrYYg-uRuQJSsACk9oQVTyBQGa5IlWF; 1HQv5xHGc6iKUkZdZwy7GkyRUgbecaduM | b3-preston |
| greatsociety | Sundquist, *Politics and Policy*; Zelizer, *The Fierce Urgency of Now*; Bernstein, *Guns or Butter* | 1ExXVHzgFgUm3EGfEhdUbS4K5V2hlYpJN; 1jzLs1pgP-zyYZFareoqLZdj4LG6qrVkz; 12qiEzZniU-FNF4O8HocS9TpLHFn6xQfT | b3-sundquist |
| macv | MACV Command Histories, 1964, 1965, 1967 (3 parts), 1968 (2 parts) | 1qOJyn0edA9EzhtMmuZCdkxRb2sSl2iJs; 1Nd9hm3ZSjQqsRpb7Xoo9hxvNmCkSHT_W; 16aijqcOo1pt2CFJVrsAddc1TyfpvmDJ0, 1mGZVPkiCzoIVBTYRKYq3ydWw1aIt25ha, 1wg20QAZca5wjZSnPyEC9PwTfo91ifpch; 1mmjroe4XDgP92Vgi5QDQJnD6u99NvpVx, 1O_Ds_OWwY5ue7H2N8kEtEZHI6MixetEQ | b3-macv-1964(-more), b3-macv-1965 |

## The merger's notes

(Written after the merge of Oct. 29's patches.)
