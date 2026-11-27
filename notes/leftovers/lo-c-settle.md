# lo-c: the conflicts settled, the splits and the rulings written

Nov. 27, 2026. Each entry below was settled by hand in its file under the tree's lock; the line says what came from the kept entry (ours) and from the dropped one (theirs), and why. Nothing in the brief was disregarded except its count: `./bib conflicts` showed 181 conflicts on 46 entries, not 53.

Six of the audit's combines had not run, because `./bib combine` stops with a cut-mark error when the dropped entry has cuts and the kept one has none (1960-12-30, 1961-06-22, 1964-01-16, 1964-07-02, 1966-02-09, 1966-03-26). I ran them in a script that puts the dropped entry's cuts into the conflict record as the other combines do, then settled them with the rest: 46 and 6 make 52 entries. The tool's fault is not mended.

Every settled line is one line with every word of both entries, the dropped entry's sentences added as parts of their own; a source goes with the words it bore in its own entry; where the two disagreed and no record settles it, the kept value stands and a Check names the other. The ten splits and the sentence moves are not in the settled lines: they are in `inbox/2026-11-27-lo-c-splits.yaml` (14 new entries, 51 other ops, `patch-check` 0 errors, not merged).

One entry outside the 52 was changed: `cal.1964-10-15.china-leadership-9` followed the dropped `-8`, which the combine put on Oct. 14, and a link across two days is none (R25c); I took the link out so that `check` ends at 0 errors.

## The settled entries

- `cal.1960-04-13.china-leadership-3`: ours' two sentences kept; theirs' invitation clause and the arrival at Kunming added as a part of its own (the patch splits it out); place stays Peking, the departure's.
- `cal.1960-11-02.peace-corps`: ours' peace-corps sentence; theirs' rescue-squad passage as a second part, since the speech text at APP holds both; place San Francisco over "California"; follows both of theirs' entries; Goodwin goes to the second part; tagged `ok:fields-time` ("the night of the ride" is no hour of the speech).
- `cal.1960-11-22.soviet-union`: ours kept whole; theirs' Yang Shangkun putting the Chinese down for a second speech added as part 8; the self-follows from the combine taken out; Made public 1999 and 2001 both kept.
- `cal.1960-12-01.transition-and-staff-2`: ours kept; theirs' Harriman exchange added as two parts after the Stevenson sentence, the journal's page 95 folded into 94–97; the journal does not say for which post, so "for Secretary of State" rests on the book.
- `cal.1961-04-19.china-leadership-3`: ours' letter text kept; theirs' sentence on the early findings is the opening part; Zhou nianpu and MacFarquhar each given their own words.
- `cal.1961-08-24.china-leadership-2`: ours kept; theirs' flexible handling of over- and under-output and the list of eight tasks folded in; Zhou nianpu now covers the whole line; the afternoon range added from Yang's "3 to 6 p.m."
- `cal.1962-01-17.china-leadership`: ours kept, with the span Jan. 17–22 left for the patch to narrow; theirs' Ke Qingshi exchanges added as four parts; the first-speaker disagreement kept as a variant on MacFarquhar, since Yang lists others as first.
- `cal.1962-07-19.china-leadership-10`: ours' July 19 (two nianpu) kept over theirs' July 18 (Mao zhuan), with the Check; theirs' title added as its own part, cited to Mao zhuan alone.
- `cal.1963-05-08.china-leadership`: ours' meeting kept; theirs' Deng attending added; the afternoon range restored from theirs, which the combine had lost; thread china-zhou, china-center in `also`.
- `cal.1963-05-22.vietnam-force-levels`: ours' news conference; theirs' test-ban and "genie" answers added as two parts with Chang, 239, and the Check on Chang's mistaken day.
- `cal.1963-05-29.transition-and-staff`: ours' Johnson-not-invited and Lincoln's words kept; theirs' staff party, gifts and Salinger added; Caro and Perlstein each on their parts.
- `cal.1963-07-16.europe-and-the-alliance`: ours' cuts; theirs' Japan clause (Marine Air Wing dropped) added as a part; the two "After McNamara's memorandum" notes joined into one.
- `cal.1963-10-01.china-leadership-10`: ours' Deng and Zhou text kept; theirs' "with no leaning" added; order made Deng's reading, Zhou's view, Deng's comment, as theirs has it; Zhou nianpu added; self-listed thread taken out of `also`.
- `cal.1963-10-16.democratic-party`: ours' lunch kept; theirs' telling "to reporters" added as a part for Shesol, 107, since the two accounts differ in the setting.
- `cal.1963-11-21.elections-1964-3`: ours' account kept; theirs' "probably on Texas politics" and Jacqueline Kennedy's account added, with Schlesinger's page 626 and its Check; night range added.
- `cal.1963-12-23.elections-1964-vice-presidency`: ours' line (theirs a subset); theirs' Schlesinger 632 added as a source; the Check on the day kept once.
- `cal.1964-01-10.latin-america-panama-3`: ours' Panama call; theirs' Goldwater and Minuteman part added, one conversation; Perlstein's words kept under a Check.
- `cal.1964-04-24.elections-1964-state-conventions`: both sentences joined: the all-Goldwater slate of six, three men and three women, and Laxalt; when stays Apr. 24–25, so theirs' Apr. 25 needs no Check.
- `cal.1964-04-27.china-leadership-9`: ours' line unchanged; theirs' Deng nianpu added as a source with its "晚"; the missing rows for Chen Yi and Zhu De written.
- `cal.1964-10-14.china-leadership-2`: date stays Oct. 14, the night, on Lengxi, Mao zhuan, MacFarquhar and Khoo against Jian's Oct. 15; theirs' request to see Mao added as a part and the "resigned" reading kept as a variant on Jian, 510.
- `cal.1964-12-15.china-leadership`: ours kept; theirs' Liu speech (cadres down to the points, class status redone) added as part 10 with Liu nianpu, 610.
- `cal.1965-02-08.vietnam-force-levels-2`: ours' Feb. 8 (Cosmas) kept over theirs' Feb. 9 (MACV, 478), which stays in the Check; theirs' battalion name added; the self-pointer taken out.
- `cal.1965-02-23.vietnam-diplomacy`: ours' Romanian-record line kept whole, theirs' Ben Bella record and its Checks added; the British approach is still in the line and the patch splits it out.
- `cal.1965-05-22.vietnam-air-war`: ours kept; theirs' first strike north of the 20th parallel added as part 4 with Drea, 61, on the ruling that May 22 is the day.
- `cal.1965-11-10.vietnam-2`: ours' JCSM-811-65 line kept; theirs' restated August aims added as part 6 with Drea, 118; "as Phase II" moved into the 113,000 sentence.
- `cal.1965-11-21.opinion`: ours' Gallup items; theirs' "Communist victory or withdrawal too few to register" added as part 4; DeBenedetti on the stalemate figures.
- `cal.1965-12-06.opinion`: ours' Harris quotation kept; theirs says the same 71 percent, so only DeBenedetti, 137, is added as a source (his "hold the line" is a paraphrase, not a new fact).
- `cal.1965-12-20.china-leadership-2`: ours kept; theirs' "unconditional negotiation" clause added; Trần Văn Thanh as the Names and tag have him, not Thành; Zhou nianpu and Chen Yi nianpu added.
- `cal.1966-02-09.china-leadership-4`: ours' Xihuating reception; theirs' topics and the Honolulu communiqué added as parts; ambassador's name 麦耶 moved into the line.
- `cal.1966-02-25.press-and-broadcasting`: ours' Life section; theirs' Hedley Donovan and "for the administration's position" added with Gibbons, IV, 240 n.77.
- `cal.1966-02-26.vietnam-air-war`: ours' Feb. 26 (Drea, 69) kept with the Check naming Staaveren's Feb. 25; theirs' area and Navy details added as part 2 under Staaveren, 237.
- `cal.1966-03-26.china-leadership-4`: ours' departure, talks and banquet kept; theirs' start of the visit, to Mar. 31, added first; the two Liu nianpu items joined; the patch splits out the talks and the banquet.
- `cal.1966-04-25.vietnam-congress-foreign-relations`: Apr. 25 kept as the one dated record; Apr. 26 and 27 tellings joined (overnight trip, fund-raising dinner, "terribly disappointed"); Gibbons and Dallek read, with the Check on the day.
- `cal.1966-05-06.china-leadership-2`: ours kept; theirs' "from every province but Tibet" and Pu, 78, added; Peng Zhen nianpu's May 6 and May 7 given as a Check.
- `cal.1966-06-03.china-leadership-9`: ours' line (June 3–4 on Pu, 152) kept; theirs' June 4 (Yang Jisheng, II, 1143) added as a source; when already covers both.
- `cal.1966-07-10.china`: ours' rally and Chen Yi kept; theirs' 10,000 from all circles, Zhou attending, added with Waijiao huodong, 500; thread china-zhou-foreign into `also`.
- `cal.1966-07-13.china-leadership-4`: ours' Hongqiao see-off; theirs' nianpu (under July 3) added as a source with a Check on the day.
- `cal.1966-07-15.open-housing`: ours' night kept; theirs' gangs renouncing violence and Young's words added as parts, Cohen, 391–92, read; the hours Check stays.
- `cal.1966-07-28.china-leadership-12`: ours' rally kept; theirs' Jiang Qing speech on beating added as part 3 with Pu, 240; Mao added to Names.
- `cal.1966-09-24.china-leadership-6`: ours' Sept. 24 kept over theirs' Sept. 23 (Zhou nianpu, 63–64), which stays as a Check; theirs' Li Xiannian report and the Sept. 16 meeting added.
- `cal.1966-10-17.china`: ours' title wording kept; theirs' variant title kept as a variant on Yang Jisheng, I, 476; the missing page row added.
- `cal.1967-02-07.china-leadership-6`: ours' Chen Yi cable; theirs' telegram to the embassies added as part 2 with the Mao nianpu and Zhou nianpu; both Made public years kept.
- `cal.1967-05-09.vietnam-air-war-2`: ours' McNamara and Vance memorandum line kept; theirs' State experts sentence added (the patch moves it to `vietnam-air-war`); Helms added to Names; Drea, 208, read.
- `cal.1967-07-12.vietnam-force-levels`: ours' three parts kept; theirs' FRUS 238 text, McNamara to the press, and the sources for the stalemate lines added; Wheeler's wording follows FRUS, with a Check on ours' older wording; the patch splits out the July 13 scene and the press words.
- `cal.1968-04-26.economy-surcharge`: ours' line covers theirs; Dallek, 535, added as a source; `cities-and-housing` into `also`, the self-listed thread out.
- `cal.1968-06-13.governors-nd`: ours' convention kept; theirs' "eight, at least six for Nixon" and Rockefeller's address added; place stays Fargo; the patch splits the address out.
- `cal.1968-06-18.elections-1968-ny`: ours' CQ figures kept; Chester's different count (63, 30, 19, 11) kept as a variant, not as the line, since a source that disagrees is no cite; "Humphrey had not campaigned" added.
- `cal.1968-06-20.china-leadership-2`: ours' PLA unit and lunch kept; theirs' factory and village visits added as part 2 with the Zhou nianpu.
- `cal.1960-12-30.china-leadership`: ours' Yinian Tang report kept; theirs' Mao zhuan account added in seven parts; self-listed thread out of `also`; `china-twelve-articles` in.
- `cal.1961-06-22.china-leadership-3`: ours' June 22 (Deng nianpu) kept, which settles theirs' open day, and its Check dropped; theirs' 240,000 cut by a third and the further 40,000 added.
- `cal.1964-01-16.transition-and-staff`: ours' quotation kept; theirs' Rowan appointment and "told beforehand" added; Miller Center page read as the primary record.
- `cal.1964-07-02.civil-rights-bill-16`: ours' television-hour call; theirs' 1:44 p.m. call, signing that evening, added as parts; Purdum, 314, kept with the note that it is another call.

## The patch

`inbox/2026-11-27-lo-c-splits.yaml`, claimed in the ledger under `lo-c-splits`: ten splits (Kunming; Blair and Lovett; the later sittings of Jan. 18–22; the British approach; Liu's talks and banquet; Fulbright's refusal; Kang Sheng's eight hours, already held by `cal.1966-05-05.china-leadership-3`, so only taken out; State's experts to `cal.1967-05-09.vietnam-air-war`; the July 13 scene and the press words; Rockefeller's address) and the ten changed rulings that are sentence moves (1960-11-25; 1961-01-27; 1961-04-20 with the Oval Office and the memorandum as new entries; 1963-10-30; 1965-02-16; 1967-05-30; 1968-02-04; 1968-03-31; 1968-04-05 and 04-07; 1968-06-14 and 06-16 with Mondale's statement as a new entry); the two ruled combines (1965-05-22, 1966-06-03) are among the settled lines above.

Defaults taken where the audit left a point open: the British approach is dated Feb. 23, the day of the French contact, with "Check: the day"; Fulbright's refusal is dated Apr. 25 with `when` Apr. 25–27; Mondale's statement is month-dated, after June 14; in `cal.1967-05-30.china-leadership-3` the Diaoyutai and Waijiao huodong, 512, stay (the entry needs its source for the reception) and 512 also goes to `-4`; a read cannot be dropped from a note by an edit, so the entries that lose an act keep the work with a pointer to the entry that took it.
