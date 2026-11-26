# China threads: the re-threading applied

Nov. 26, 2026. This note reports the re-threading of the China entries, done under `notes/briefs/china-threads-apply.md` and ruling 59 of `notes/owner-rulings.md` ("the re-threading as applied"). The script is `tools/threads/china/apply.py`. It read `notes/threads/china-tree.tsv` (27,831 rows) and the tree in `tools/threads/china/tree.py`, and wrote `lists/cal/th.yaml`, 122 month files of `lists/cal/` and `notes/threads/china-held.tsv`. It wrote them through the repository's own reading and writing of entries (`tools/bib/store.py`). Nothing was committed or pushed. Nothing in `sources/` or `works/` was changed. `pages.yaml` has three new splits, written by `./bib pages --plan` (section 7). No entry's id changed.

## 1. What was done, in short

- 45 threads were added to `th.yaml`. It had 306 threads and now has 351. The 306 are unchanged.
- 22,991 entries moved to a new primary thread.
- 1,700 entries stay in "China: Leadership" and now carry Propaganda and culture, Army or Agriculture in `also:`.
- 376 entries are held, unchanged, because their primary thread would be Organization.
- 2,764 entries fit nothing and are unchanged: 1,677 in "China: Leadership" and 1,087 in "China".
- 12,200 threads were added to `also:` in all, on 24,691 changed entries.
- `./bib check` ends in 0 errors. Its warnings went from 1,400 to 1,411.
- The fast tests pass with the re-threading in the tree: 1,166 passed, 1 expected failure (section 6 says how this was shown, and why two tests fail in the working tree as it stood at the end).

## 2. The threads added

Each thread has the parent that `tree.py` gives it. A thread with no parent there sits under `china`. "Cultural Revolution" (`india-and-china-cultural-revolution`) is unchanged and is now the parent of the six stages. "Thread set" counts the entries whose `thread:` is now this thread. "Also added" counts the entries that now carry it in `also:`. The last column counts the entries the thread's own page will list, which are those two together.

| thread | slug | thread set | also added | entries on its page |
|---|---|---:|---:|---:|
| China: Agriculture | `china-agriculture` | 0 | 876 | 876 |
| China: Agriculture: Famine | `china-famine` | 1,049 | 23 | 1,072 |
| China: Agriculture: Sixty Articles | `china-sixty-articles` | 312 | 2 | 314 |
| China: Agriculture: Twelve Articles | `china-twelve-articles` | 74 | 0 | 74 |
| China: Army | `china-army` | 0 | 1,635 | 1,635 |
| China: Army: Luo Ruiqing | `china-luo-ruiqing` | 97 | 14 | 111 |
| China: Beidaihe and the Tenth Plenum | `china-tenth-plenum` | 137 | 15 | 152 |
| China: Center's daily work | `china-center` | 1,985 | 0 | 1,985 |
| China: Cultural Revolution: May Sixteenth and the work teams | `china-may-sixteenth` | 639 | 80 | 719 |
| China: Cultural Revolution: Ninth Congress | `china-ninth-congress` | 413 | 107 | 520 |
| China: Cultural Revolution: Red Guards | `china-red-guards` | 1,133 | 0 | 1,133 |
| China: Cultural Revolution: Revolutionary committees | `china-class-ranks` | 729 | 1 | 730 |
| China: Cultural Revolution: Seizures of power | `china-seizures` | 787 | 93 | 880 |
| China: Cultural Revolution: Wuhan and the army | `china-wuhan` | 1,053 | 2 | 1,055 |
| China: Finance and economy | `china-economy` | 840 | 746 | 1,586 |
| China: Finance and economy: Third Front | `china-third-front` | 85 | 2 | 87 |
| China: Finance and economy: Xilou and the retreat | `china-retreat-1962` | 149 | 10 | 159 |
| China: Foreign affairs | `china-foreign` | 3,847 | 3,515 | 7,362 |
| China: Foreign affairs: Afro-Asian conference | `china-afro-asian` | 106 | 0 | 106 |
| China: Foreign affairs: India war | `china-india-war` | 166 | 3 | 169 |
| China: Foreign affairs: Split with Moscow | `china-moscow` | 0 | 0 | 0 |
| China: Foreign affairs: Split with Moscow: Border war | `china-border-war` | 84 | 8 | 92 |
| China: Foreign affairs: Split with Moscow: Bucharest and Moscow | `china-moscow-1960` | 166 | 9 | 175 |
| China: Foreign affairs: Split with Moscow: Polemic | `china-polemic` | 444 | 16 | 460 |
| China: Foreign affairs: Zhou in Africa | `china-africa-tour` | 209 | 0 | 209 |
| China: Four Cleanups | `china-four-cleanups` | 921 | 51 | 972 |
| China: Liu Shaoqi | `china-liu` | 573 | 521 | 1,094 |
| China: Mao Zedong | `china-mao` | 968 | 306 | 1,274 |
| China: Mao Zedong: Cultural Revolution | `china-mao-cr` | 1 | 496 | 497 |
| China: Mao Zedong: Foreign guests | `china-mao-foreign` | 624 | 259 | 883 |
| China: Nuclear weapons | `china-nuclear` | 0 | 5 | 5 |
| China: Nuclear weapons: Bomb | `china-bomb` | 145 | 83 | 228 |
| China: Nuclear weapons: Nuclear diplomacy | `china-nuclear-diplomacy` | 46 | 30 | 76 |
| China: Organization | `china-organization` | 0 | 267 | 267 |
| China: Political-legal work | `china-political-legal` | 207 | 181 | 388 |
| China: Propaganda and culture | `china-propaganda` | 0 | 1,014 | 1,014 |
| China: Propaganda and culture: Hai Rui | `china-hai-rui` | 102 | 41 | 143 |
| China: Propaganda and culture: Lei Feng, Dazhai, Daqing | `china-models` | 99 | 5 | 104 |
| China: Propaganda and culture: Opera reform | `china-opera` | 66 | 1 | 67 |
| China: Seven Thousand Cadres | `china-seven-thousand` | 108 | 0 | 108 |
| China: Shanghai and Beidaihe, 1960 | `china-shanghai-1960` | 74 | 0 | 74 |
| China: United front and nationalities | `china-united-front` | 175 | 85 | 260 |
| China: Zhou Enlai | `china-zhou` | 1,471 | 267 | 1,738 |
| China: Zhou Enlai: Cultural Revolution | `china-zhou-cr` | 0 | 855 | 855 |
| China: Zhou Enlai: Foreign affairs | `china-zhou-foreign` | 2,907 | 576 | 3,483 |
| total | | 22,991 | 12,200 | |

After the change "China: Leadership" is the `thread:` of 3,753 entries and its page lists 3,966. "China" is the `thread:` of 1,087 entries and its page lists 1,678. "China: Cultural Revolution" lists 296.

In `th.yaml` the China threads are together, in alphabetical order of their full names, as `check` asks. This moved "Cultural Revolution" ahead of "Leadership". The file's one warning on order was there before and is not about China: Canada, Mongolia and Singapore are out of place.

## 3. The statements

The statements are those of `notes/proposals/china-threads-measure.md`, section 3, as its two audits left them, with these changes. I checked every station by script against the entries each thread holds as applied (its `thread:` or its `also:`), and then read the entries on each station's days to see that they are the event the station names.

Changes the brief directed:

- Famine has the owner's statement: "The famine: the deaths and the reports of them, the grain taken, moved and bought abroad, the relief, the Center's measures."
- Mao Zedong's statement no longer says "outside the episodes". It reads "Mao Zedong's acts: his comments and instructions, letters, talks, audiences, poems, swims, travels." The thread is named "Mao Zedong", as the revised scheme names it. The measurement's table had "Mao".
- Zhou Enlai's statement no longer says "outside the episodes". It reads "The Premier's day: the State Council, the plan, the guests and the visits abroad."
- Liu Shaoqi's statement never said it and is unchanged.
- Bomb has two stations before July 1963, since its entries now begin in 1960: the Center's decision on the nuclear industry (July 16, 1961) and the special committee under Zhou Enlai (Nov. 17, 1962). `th.yaml` has no field for a thread's years, so the stations are how the statement reaches those years.

Stations corrected, moved or dropped because they did not fall on an entry of the thread as applied:

- Mao Zedong: "Edgar Snow" (Oct. 22, 1960) and "Montgomery at Wuchang" (Sept. 23, 1961) are entries of "Mao Zedong: Foreign guests". The two stations are now in that subthread's statement.
- Zhou Enlai: all five stations (the Burma boundary agreement, Rangoon, Delhi and Kathmandu, Bhutto and the Pakistan boundary agreement, Pakistan and Tanzania, Hồ Chí Minh's death) are entries of "Zhou Enlai: Foreign affairs". They are now in that subthread's statement. The parent's statement has no station.
- Bomb: "The first test; the statement." is now "The first test." The government's statement of Oct. 16, 1964 is an entry of Foreign affairs and Nuclear diplomacy, not of Bomb. Nuclear diplomacy's statement has it as a station.
- Organization: all five stations are dropped. Each falls on an entry whose primary thread is Organization, and those entries are held and do not carry the thread. The stations are in the proposal and can go back when the entries are released.

Changes I made that the brief did not name. Each can be undone in one line of `apply.py`.

- Agriculture's statement no longer says "outside the named episodes". The owner's words of Nov. 25 are that it is absurd to exclude the famine and related episodes from a thread like "China: agriculture". It now opens "Farming, grain, water and the communes:".
- Propaganda and culture's statement no longer says "outside the named episodes", for the same reason. It is the parent of Opera reform, the models and Hai Rui.
- Seven Thousand Cadres: the words "of January 1962" show only on the pages of 1962. `check` warns on an untagged sentence that names a year, because it shows on every page the thread is on, and this thread has entries in 1961.
- Organization: the words "the case groups after April 1969" show only from April 1969, by the same rule.

A statement I left as drafted that no longer fits: Foreign affairs still opens "Foreign business not done by Mao, Zhou Enlai or Liu Shaoqi". Under ruling 59 the thread now carries 3,515 entries in `also:`, and most of them are Mao's, Zhou's or Liu's foreign business. The owner has not spoken on this statement, so I did not change it. A wording that would fit: "Foreign business: the receptions, visits, speeches and cables, the Foreign Ministry and the International Liaison Department."

The seven threads the proposal had no statement for each have one sentence, written from their entries. None is left without a statement.

- Split with Moscow: "The quarrel with the Soviet party: the parties' meetings, the open polemic, the border war."
- Nuclear weapons: "China and nuclear weapons: the bomb and its tests, the diplomacy of the ban, the leaders' words on nuclear war."
- Nuclear diplomacy: "The test ban treaty refused, the proposals for a summit, complete prohibition and no first use, the conferences against atomic and hydrogen bombs, non-proliferation." It has one station, the statement on the first test.
- Mao Zedong: Foreign guests: "Mao Zedong's foreign business: the guests received, the talks, the telegrams and statements." It has the two stations moved from the parent.
- Mao Zedong: Cultural Revolution: "Mao Zedong in the Cultural Revolution's stages: his comments on papers, his instructions and talks, the drafts he revised."
- Zhou Enlai: Foreign affairs: "The Premier's foreign business: the guests received, the visits abroad, the talks, statements and cables." It has the five stations moved from the parent.
- Zhou Enlai: Cultural Revolution: "The Premier in the Cultural Revolution's stages: his speeches and meetings, the Center's telegrams and notices he drafted, his instructions to the provinces and the army."

The statement of "China" itself is unchanged. At least two of the events its stations name are now entries of its subthreads and not its own: "The test ban refused" (July 31, 1963) is in Nuclear diplomacy, and "Zhou Enlai in Moscow" (November 1964) is in Polemic. I left the statement alone, since the entries are still in China's family.

## 4. The entries left and held

- 1,677 entries of "China: Leadership" fit no thread and are unchanged. They are the leftovers of ruling 58, point 6.
- 1,087 entries of "China" are unchanged. The rules run that thread's entries for the episodes and the nuclear threads only, and these fit none.
- 520 entries whose primary thread is Propaganda and culture stay in "China: Leadership" and carry the thread in `also:`. The audit read 22 of 30 right.
- 565 entries whose primary thread is Army stay and carry it in `also:`. The audit read 22 of 30 right.
- 615 entries whose primary thread is Agriculture's own stay and carry it in `also:`. The audit read 5 of 10 right. Agriculture's three episodes are applied under it.
- 376 entries whose primary thread is Organization are held. Nothing on them changed. The audit read 7 of 10 right before its last mend, and asked for a fresh sample of 30. They are listed in `notes/threads/china-held.tsv` with the rule and the secondary threads their rows give.

Three things about `also:` that the counts above include:

- I read "held, unchanged" as the whole entry. So the secondary threads on the 376 held rows were not written either. There are 18 of them: Army 11, Finance and economy 2, Political-legal work 2, Foreign affairs 2, United front and nationalities 1. They are in the last column of `china-held.tsv`.
- An entry that moved lost `china` (4,400 entries) and `china-leadership` (3 entries) from `also:`.
- An entry that took one of the six stages lost "Cultural Revolution" from `also:` (274 entries), since no thread is written beside its own parent. The 292 other entries that carried "Cultural Revolution" in `also:` keep it.

One case the brief did not settle. 100 entries stay in "China: Leadership", already had `china` in `also:`, and now carry Propaganda and culture, Army, Agriculture or another new thread beside it. `china` is the parent of each of these. I left `china` on them, because the brief takes it off only an entry that moves, and these entries sat beside their parent `china` before. To take it off them is one condition in `apply.py` (`plan_entry`).

## 5. How the script was proved

- Before the change I checked that the repository's writer leaves all 138 calendar files byte for byte as they are when nothing in them changes. So a changed line in a file is a line the script meant to change.
- The dry run's table agreed with a separate count made from the tsv alone, thread by thread, for both columns.
- The script refuses a row whose entry is missing, whose date is not the entry's, whose entry's thread is not `china-leadership` or `china`, that names an unknown thread, that is given twice, or that has the Center's daily work as a secondary thread. I tested each refusal on a changed copy of the tsv. A refusal stops the run before anything is written.
- After the change a second script, which shares no code with `apply.py` or `tools/bib`, read the files back with a plain YAML reader and compared them with the files of commit `d8a7cbd4`. For all 27,831 rows it found exactly the thread and the `also:` that the brief's rules give. In every changed file, every changed line is a `thread:` line or an `also:` line. No other field of any entry changed, nor the order of the fields, nor the order of the entries. No entry outside the tsv changed. In `th.yaml` the 306 old threads are unchanged and in their old order apart from the China threads. It found 0 faults.
- That script was a scratch file and is not in the tree. Its rules are the ones in section 4.

## 6. What `check` asked, and the tests

`./bib check` ended in 0 errors at the first run after the change, so nothing in the entries had to be mended. The count of warnings went from 1,400 to 1,411. Only one rule's count moved: `thread-size` went from 36 to 47. Every other warning is the same warning as before, some on a new line number.

`thread-size` warns where a thread has more than 150 entries of its own in one part of the calendar. It is a prompt to consider subthreads, not a rule. Before, 32 of the 36 were "China: Leadership". Now 43 of the 47 are China threads: Foreign affairs 9, Leadership 9, Zhou Enlai: Foreign affairs 5, Famine 3, Revolutionary committees 3, and one or two each for Center's daily work, Four Cleanups, May Sixteenth, Red Guards, Wuhan and the army, Zhou in Africa, Ninth Congress, Seizures of power and Sixty Articles. The largest is Wuhan and the army with 722 entries in the second half of 1967.

I marked no exception on any thread or entry.

The fast tests (`python -m pytest -q -m "not slow"`). Right after the change they passed: 1,166 passed, 1 expected failure. At the end I ran them again in the working tree and two failed, `test_build_output` and `test_build_files` in `tests/golden/`. Those two build the tests' own small fixture, not the calendar's data, and compare the pages' sizes with a stored list. Two fixture pages came out 3 KB smaller. By then another agent's uncommitted changes to `templates/list.html` and `tools/bib/` (the maps) were in the working tree. To separate the two, I ran the fast tests in a clean copy of commit `d8a7cbd4`, the commit I started from, with the re-threading's files laid over it: every file of `lists/cal/`, `pages.yaml`, `apply.py` and this note. They passed: 1,166 passed, 1 expected failure. So the two failures are not from the re-threading.

## 7. The pages

What the code and the plan say (`pages.yaml`, `tools/bib/pages.py`, `tools/bib/threads.py`). A thread's page is `threads-<slug>.html`. A page over the budget of 5 MB is cut into parts by date, and the thread's own page then lists the parts. The plan only cuts a page further. It never joins parts again, so a part's address stays.

What the change does:

- "China: Leadership" keeps its 35 parts at the same addresses. They listed 26,563 entries and now list 3,966. The fewest in a part is 11 and the most is 240. The parts are far smaller than they need to be, 10.4 MB in all, but every old address still opens.
- "China" keeps its 7 parts. They listed 6,475 entries and now list 1,678, because an entry that moved no longer carries `china` in `also:`.
- 44 of the 45 new threads have a page. "Split with Moscow" has none, since it has no entry of its own.
- An old link to an entry on a thread page (`threads-china-leadership-1960Q1.html#t-<id>`) still opens that page. If the entry has moved, it is no longer on that page, and the reader lands at the top. The entry is on its new thread's page. Links to an entry in the calendar (`cal.html#<id>`, `e.html#<id>`) go by id and are not affected.

What I ran, under the lock:

- `./bib build threads` alone takes 7 minutes. I ran it.
- `./bib pages` then showed three thread pages over budget: Foreign affairs at 20.0 MB (7,362 entries), Zhou Enlai: Foreign affairs at 12.0 MB (3,483) and Army at 5.2 MB (1,635).
- `./bib pages --plan` wrote the three splits into `pages.yaml`: Foreign affairs in 9 parts, Zhou Enlai: Foreign affairs in 5, Army in 2. It added 51 lines and changed nothing else in the file. The guide's rule is that a page over budget is split by the plan, and the tool wrote it; I edited nothing by hand.
- I built the threads again and ran `./bib pages` again. No thread page is over budget. The largest part is 3.3 MB. The pass ends with exit 0. The only pages over budget are ten Names pages of one person each, which no split divides, as before.
- The largest page left whole is Mao Zedong's at 4.9 MB, just under the budget. It will want parts when it grows.

What I did not run:

- The full build. `build/` now holds thread pages of the new state and calendar pages of the old.
- `./bib links`. The thread pages link to each thread's line in the calendar's index, and the new threads' lines are made by the full build.
- `./bib readme`.

## 8. What is left

- The full build, then `./bib links`, `./bib pages` and `./bib readme`. Every calendar page names an entry's thread in its heading line, so all of them change. The splits of the three large thread pages are already in the plan, so one build should do.
- A parent's page does not list its subthreads' entries. The audit expected Agriculture's page to hold the entries of Famine, Twelve Articles and Sixty Articles. The site's code lists on a thread's page only the entries that name the thread in `thread:` or `also:` (`build.index_members`), and links the subthreads at the head of the page. The line under each entry and the highlight do keep the family together. So Agriculture's page lists its 876 entries and links the three episodes. "Split with Moscow" has no entry of its own and so has no page. Its three episodes have pages, but the Foreign affairs page does not link them and they have no link to a parent. They are reached from the list of all threads and from the calendar's index. If the owner wants a parent's page to hold the family, that is a change to `tools/bib/threads.py`, not to the entries.
- The 376 held entries want the fresh sample of 30 the audit asked for. If Organization is released, 376 rows and their 18 secondary threads go in, and the five stations go back into its statement.
- The 1,700 entries of Propaganda and culture, Army and Agriculture want reading entry by entry before any of them leaves "China: Leadership".
- The Foreign affairs statement, as section 3 says.
- The 100 entries of section 4 that keep `china` in `also:`.
- The tsv cannot now be made again as it was. `tree.py` and `measure.py` read only the entries whose thread is `china-leadership` or `china`, and 22,991 entries have left those threads. Running `tree.py` now would write a tsv of the 4,840 entries that remain, over the one that was applied. Keep `notes/threads/china-tree.tsv` as it is. To change a thread's rule later and move entries again, the two scripts first need to read the China family's entries by their present threads.
- A fault in `tools/bib/threads.py` that does no harm today. A thread part that a later plan drops is forwarded by finding the first thread whose page name its name begins with. For a part of any `china-…` thread that is "China", whose own page is in parts. So a dropped part of "China: Leadership" would forward to China's parts. No thread part is retired now. The fault matters only if someone later merges the small parts of "China: Leadership".
- Ruling 58, point 2, stands as it was: no entry moved to a country's thread, and every entry keeps the countries it had in `also:`.
