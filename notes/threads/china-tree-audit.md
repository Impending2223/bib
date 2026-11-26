# China threads: the audit of the tree

Nov. 26, 2026. An audit by reading of the China threads as a tree (`notes/threads/china-tree.tsv`, made by `tools/threads/china/tree.py` from the rules in `measure.py` and `systems.py`), under `notes/briefs/china-tree-audit.md`. It tests the primary thread each entry is given, the secondary threads, the second mending's counts (`notes/threads/china-assign-mend-2.md`), and the parts of tree.py no one had read: the word lists `DIPLOMACY` and `TALK`, the threshold `STRONG`, the subthreads of Mao and Zhou Enlai, the two nuclear threads and the handling of the plain `china` thread. Nothing in `lists/`, `th.yaml` or `sources/` was changed. Nothing was merged, built, committed or pushed.

## 1. What I read

I read the entries straight from `lists/cal/*.yaml` with a script of my own. For every sampled entry I read the whole line and the whole note, Chinese characters, "Made public", "To check" and "Check" sentences included. Three notes too long for one printing were printed in two parts, and I read both parts. I judged each entry against the thread statements in `notes/proposals/china-threads-measure.md` and the scheme in `notes/proposals/china-threads-revision.md`. An entry counts as right where it belongs to the thread it was given, or where two threads could hold it and the rule chose one of them. It counts as wrong where another thread fits it plainly better, or none does.

The samples were drawn at random with seeds of my own (4471 for the first round, 90210 for the fresh samples after the mends):

- 30 entries from each of the six threads the first audit found weak: 180.
- The threads and subthreads no one had seen: all 24 entries whose primary thread was Nuclear diplomacy, and 25 more that carried it as a secondary thread; all 5 whose primary thread was the parent, Nuclear weapons; 25 from Zhou Enlai: Foreign affairs; 25 from Mao Zedong: Foreign guests. Zhou Enlai: Cultural Revolution had no primary entries and Mao Zedong: Cultural Revolution one, so I read 25 entries carrying each as a secondary thread.
- 10 from each of the other 32 threads that hold primary entries: 320.
- 40 from the entries that stay in `china-leadership`, and 40 from the entries of the plain `china` thread that the rules move to an episode.
- For the secondary placings, 150 entries that carry at least one secondary thread: 40 with a system as a secondary thread, 40 with a person's thread or subthread, 30 with an episode, and 40 more from all of them.

That is 934 entries in the first round. After the mends I read fresh samples, none of them read before: 25 from Bomb, the 11 entries of Nuclear diplomacy I had not yet read, 15 from Third Front, the 5 entries that now carry Nuclear weapons as a secondary thread, and 25 of the entries the mends moved. That is 81 more, 1,015 in all.

Outside the counts, as a check on the last mend only, I read the 14 entries that its run moved; for these I read the whole line and the note to 600 characters. They are not counted anywhere below.

I read nothing in `build/`. Nothing in the brief narrowed what I read, and I disregarded nothing in it.

## 2. The primary placings

### The six weak threads

| thread | right of 30 (mine) | the second mending's last count | faults found |
|---|---:|---:|---|
| Shanghai and Beidaihe, 1960 | 29 | 28 | a Secretariat sitting of July 4 on the Bucharest quarrel, before the conference |
| Twelve Articles | 29 | 28 | Chen Yun on four years for farming, January 1961 |
| Political-legal work | 27 | 29 | Lin Biao on Liu Shaoqi's faction; men framing Zhou seized in July 1968 (a stage); a Northwest Bureau meeting of the Four Cleanups |
| Finance and economy | 26 | 27 | Deng at a Korean steel works; Peng Zhen reading a New Year editorial; Zhu De's report on farming; Zhu De's diary on flowers |
| Army | 22 | 26 | three entries of the Cultural Revolution's stages without the movement's words; Peng Dehuai's 1962 letter (Tenth Plenum); Lin Biao on Luo Ruiqing, dated by year only; Lin Biao on the two bombs in 1962; Zhu De writing for a youth paper; Yang Shangkun on archives; Peng Dehuai sightseeing |
| Propaganda and culture | 22 | 24 | the press printing a stage's business (January 1967, October 1968); Zhu De's notebook of 1969; a relay of the Shanghai meeting; Lu Dingyi's fall; Chen Yun's pipa teacher; a social call on Yang Shangkun; an Academy of Military Science journal |

The second mending's counts for Shanghai and Beidaihe, Twelve Articles and Political-legal work hold up within a point or two. Its count for Army does not: it read 26 on the opening of the line only, and I read 22 on the whole entry. Propaganda and culture reads 22 against its 24. The faults are the kinds that note named: a lesser figure's presence or private day, and an episode's business without the episode's words.

### The threads no one had seen

| thread | read | right | faults found |
|---|---:|---:|---|
| Zhou Enlai: Foreign affairs | 25 | 25 | none |
| Mao Zedong: Foreign guests | 25 | 19 | four that belong to an episode the words missed (the 1960 drafting commission, Liu Shaoqi's return from Moscow, Mao on Khrushchev's speeches of May 1960, the Hangzhou meeting of May 1963); two that are not foreign business (Li Zongren back from the United States; a paper on industry sent to Lin Biao) |
| Zhou Enlai: Cultural Revolution (as secondary) | 25 | 25 | none |
| Mao Zedong: Cultural Revolution (as secondary) | 25 | 25 | none |
| Nuclear diplomacy (primary) | 24 | 21 | a Secretariat sitting on mixed business; Mao and the head of the Japanese council against the bomb, where the talk was of the intermediate zone; Zhou with Phạm Hùng on Vietnam, where the treaty is a remark |
| Nuclear diplomacy (secondary) | 25 | 25 as secondary | but the primary thread was right in only 9 of the 25: Bomb took the test-ban statement, the telegrams to the conferences against the bomb, the non-proliferation statements and Zhou's talks on the treaty |
| Nuclear weapons, the parent (primary) | 5 | 1 | Mao and Montgomery, the opening of the National People's Congress, Zhou with Bhutto, Mao on a paper about the American army: "nuclear war" in a line about something else |

The subthreads of Mao and Zhou are sound. Every entry read was in the right part of the person's family; the six wrong Mao entries are wrong because an episode should have been primary or the plain Mao thread should have held them, not because they are not Mao's.

### The other threads, 10 each

| thread | right | thread | right |
|---|---:|---|---:|
| Bucharest and Moscow | 10 | Lei Feng, Dazhai, Daqing | 8 |
| Polemic | 10 | Opera reform | 8 |
| Border war | 9 | Hai Rui | 10 |
| India war | 10 | Luo Ruiqing | 10 |
| Zhou in Africa | 10 | May Sixteenth and the work teams | 10 |
| Afro-Asian conference | 8 | Red Guards | 10 |
| Famine | 10 | Seizures of power | 10 |
| Sixty Articles | 9 | Wuhan and the army | 10 |
| Seven Thousand Cadres | 10 | Revolutionary committees | 10 |
| Xilou and the retreat | 9 | Ninth Congress | 10 |
| Beidaihe and the Tenth Plenum | 9 | Mao Zedong | 8 |
| Four Cleanups | 9 | Zhou Enlai | 8 |
| Third Front | 9 | Liu Shaoqi | 8 |
| Bomb | 7 | Center's daily work | 9 |
| Foreign affairs | 10 | Agriculture | 5 |
| Organization | 7 | United front and nationalities | 8 |

In all, 288 of 320 are right. The faults by thread:

- Agriculture (5): Zhu De at a tractor works; the Tongwei famine report of 1965; Peng Zhen at a workers' and peasants' amateur show; the Secretariat on household contracting in June 1962 (Xilou and the retreat); Deng at a Korean farm.
- Organization (7): a condolence at a foreign embassy (the death rule); Yang Shangkun's self-criticism over the recordings of 1961 (a station of the Center's daily work); a Shaanxi letter of the Four Cleanups.
- Bomb (7): Zhou's cable to Sihanouk on the summit for a ban (Nuclear diplomacy); the 1969 plan and an army training conference, where the bomb is a remark.
- Mao, Zhou, Liu (8 each): entries whose episode the words missed: the third front's decision of August 1964, the arrests discussed with the marshals in March 1968, Bo Yibo's escort in December 1966, the Center's letter to the workers in March 1967, Liu's letter on the Jiangsu movement of 1964, Liu's flight to the Canton conference.
- Lei Feng, Dazhai, Daqing (8): a foreign delegation; a Special Commission meeting on the bomb.
- Opera reform (8): an evening at an amateur show; foreign guests taken to *The East Is Red*.
- Afro-Asian conference (8): two days of the Algerian anniversary at Algiers.
- United front (8): an airport meeting; the May Day banquet for foreign guests.
- One wrong each: Border war (Zhou on factions at Xuzhou, 1969), Center (Yang Shangkun with a county's heads on his Shaanxi stay), Four Cleanups (a telephone call at Xi'an), Sixty Articles (the Sixty Articles on Higher Education), Xilou and the retreat (the chemical industry), Tenth Plenum (an article on Greek ethics), Third Front (a Cambodian guest told of the Third Five-Year Plan).

### The leftovers and the plain `china` thread

Of 40 entries that stay in `china-leadership`, 35 are rightly left there. Five should have gone to a thread: Zhu De at the Tanggu port (Finance and economy), Zhu De on the Hebei floods of October 1963 (Agriculture, a station of its statement), Zhu De on Gao Gang during the Tenth Plenum, a caller on Yang Shangkun that the word "hospital" kept from the Center's daily work, and a visit to an institute of automatic control.

Of 40 entries of the plain `china` thread moved to an episode, 37 are right. The wrong ones: Shanghai's war preparations of December 1969 put in Bomb (they belong to the war scare of Border war); Nationalist landings in Fujian put in Polemic by the book they were read from; the China–Zambia communiqué put in Bomb by "nuclear-monopoly". The rule of tree.py for this thread (the episodes and the nuclear threads only; the rest stays in `china`) holds.

## 3. The secondary placings

Of the 150 entries, 110 carry only secondary threads that fit. There are 214 secondary placings in the 150; 171 fit and 43 do not.

| kind | fit | do not fit |
|---|---:|---:|
| a system | 77 | 39 |
| of which the Center's daily work | 7 | 31 |
| of which the other eight systems | 70 | 8 |
| a person's thread or subthread | 62 | 3 |
| an episode | 32 | 1 |

The Center's daily work is the one that fails. Its statement is the Politburo's and the Secretariat's sittings on mixed business, the General Office and its callers, and the papers sent round, to Yang Shangkun's removal. As a secondary thread the rule gave it to any line that names a body of the Center: a Politburo sitting on one episode's business, the Center's decisions in the Cultural Revolution, the Center's reply on a secretary's medical treatment. It sat on 2,767 entries as a secondary thread. The other eight systems fit 70 times in 78 as secondary threads, so the threshold `STRONG` (4) holds for them. The wrong ones were Organization from the death rule (a starved boy; Sichuan's death figures), Army for a general's private act and a military academy seen on a tour, Propaganda and culture for a Red Guard corps founded at a university, and a Cultural Revolution notice on alliances "by trades and systems" that took Army and Finance and economy.

The persons' secondary threads fit 62 times in 65. The three wrong were Zhou Enlai: Cultural Revolution on Zhou at a rally on Vietnam and on Zhou receiving the airmen who shot down an American plane (a stage had taken the entry, so Zhou's subthread followed it), and Mao Zedong: Foreign guests on a Polish article Mao sent round. The episodes' secondary threads fit 32 times in 33.

A thread that plainly fits is missing in 8 of the 150, and arguably in 5 more. The plain ones: a stage and Zhou's or Mao's Cultural Revolution subthread on three entries of 1966–67 with no word of the movement (the Jiangxi Military District's cadres, the Sichuan question, the Propaganda Department's reorganization); Army on the rally of the army's academies in November 1966; Agriculture on Zhou to the farm conferences of 1965 and on a farming article Mao sent round; Bomb on He Long's defense-industry plan of 1960; Nuclear diplomacy on the drafting of the government's statement of July 1963.

## 4. The faults that repeat, and the mends

Each mend is marked `AUDIT 2 (n)` in the code, with a line saying what it does.

1. tree.py: the Center's daily work is never a secondary thread. As a primary thread it read right 9 times in 10, and it stays.
2. tree.py: `DIPLOMACY` misses words the entries use: "complete and thorough prohibition", "prohibition of nuclear weapons", "ban and destruction of nuclear arms", "banning nuclear weapons", "nuclear-free zone", "the spread of nuclear weapons". They are added.
3. tree.py: Bomb's word list in measure.py ("atomic", "nuclear", "test ban") took the diplomacy as Bomb's. Now, where `DIPLOMACY` finds its words in the line's first 200 characters, Nuclear diplomacy comes before Bomb. Where the line has the diplomacy and no word of the weapon itself (a test, the programme, a missile, the Special Commission), Bomb is dropped. Where the diplomacy comes only later in the line, Nuclear diplomacy is a secondary thread after the persons and the systems.
4. tree.py: Bomb by a word that comes only after the line's first 200 characters (a remark on the bomb in a planning conference, an army training conference, the 1969 plan) now follows the persons and the systems.
5. tree.py: `TALK` (nuclear war, nuclear blackmail) gives the parent, Nuclear weapons, only as a secondary thread. It had taken the primary thread from Mao, Zhou and the National People's Congress.
6. tree.py: Bomb's window in measure.py opens in July 1963, so the programme's earlier decisions had no nuclear thread: the Center's decision on the nuclear industry of July 1961, the Special Committee of November 1962, the theoretical design, Luo Ruiqing's report on a test in 1964. Before July 1963 the weapon's own words at the line's opening (`WEAPON_EARLY`) now place Bomb, as an episode. This takes Bomb's span back to 1960; the thread statement will want "1960" where it says the bomb's years.
7. measure.py: "Third Five-Year Plan", "Third Plan" and 三五计划 no longer place an entry in Third Front, except in the work conference of May 15–June 17, 1964, the thread's first station. They had taken a Cambodian guest, the 1965 farm conferences, the Government Work Report of December 1964 and a talk of Mao's in January 1966.
8. measure.py: Bucharest and Moscow takes "drafting commission", "twenty-six parties" and "Khrushchev's speeches" in its months.
9. measure.py: the Sixty Articles on Higher Education are not the communes' Sixty Articles.
10. measure.py: Bomb's "Special Commission" must have its capitals; Peng Dehuai's "special committee" of 1928 had taken him into Bomb in 1967.
11. measure.py: the death rule (a death is Organization's) now needs a named person and no foreign evidence. It had given Organization condolences at foreign embassies, the memorial meetings for foreign experts and a famine book's starved boy.

Faults found that I did not mend, because no rule I could write would not do more harm:

- The stages of the Cultural Revolution miss business of their months that does not use the movement's words, above all Zhou's and Mao's: a call on a military district's cadres, a question of one province, an escort, a letter to the workers. These go to Zhou's, Mao's or a system's thread. A rule that took every non-foreign entry of Zhou's in those months would take his plan and his railway business too.
- Army and Propaganda and culture still hold a lesser figure's presence or private day (a wreck seen, a pipa teacher, a sightseeing trip) and an episode's business printed in the press.
- Agriculture's own entries mix farming with factories, shows and foreign farms. Its faults are of five kinds, one each.
- A word of an episode that falls in a list in a long line still takes the line (the Special Commission meeting that went to Lei Feng, Dazhai, Daqing by "Wang Jie").

## 5. How the sizes moved

The mends moved the primary thread of 142 entries of 27,831, and changed the secondary threads of 2,941 (2,767 of them by taking the Center's daily work out). The entries with at least one secondary thread fell from 10,523 to 8,786.

| thread | primary before | primary after | every entry before | every entry after |
|---|---:|---:|---:|---:|
| Center's daily work | 1,986 | 1,985 | 4,753 | 1,985 |
| Bomb | 190 | 145 | 234 | 228 |
| Nuclear diplomacy | 24 | 46 | 51 | 76 |
| Nuclear weapons (the parent) | 5 | 0 | 5 | 5 |
| Third Front | 111 | 85 | 114 | 87 |
| Organization | 385 | 376 | 709 | 643 |
| Sixty Articles | 317 | 312 | 319 | 314 |
| Bucharest and Moscow | 161 | 166 | 170 | 175 |
| Foreign affairs | 3,833 | 3,847 | 7,363 | 7,364 |
| Zhou Enlai | 1,456 | 1,471 | 1,738 | 1,738 |
| Zhou Enlai: Foreign affairs | 2,894 | 2,907 | 3,483 | 3,483 |
| Mao Zedong | 959 | 968 | 1,274 | 1,274 |
| Mao Zedong: Foreign guests | 620 | 624 | 883 | 883 |
| Finance and economy | 836 | 840 | 1,579 | 1,588 |
| Propaganda and culture | 515 | 520 | 1,009 | 1,014 |
| Army | 562 | 565 | 1,643 | 1,646 |
| plain `china` | 1,097 | 1,087 | 1,097 | 1,087 |
| `china-leadership` (leftovers) | 1,678 | 1,677 | 1,678 | 1,677 |

The other threads moved by two entries or fewer. The Nuclear weapons family now holds 298 entries: Bomb 228, Nuclear diplomacy 76, and 5 on the parent alone as a secondary thread. By the owner's question of Nov. 25, there is enough for Nuclear diplomacy as a sibling of Bomb, though it is small.

The fresh samples under the mended rules: Bomb 25 of 25 right (22 at the first run of the mends; the three wrong ones were Peng Dehuai's "special committee", Zhou to the Colombians on a ban and nuclear-free zones, and the World Peace Council's resolution on prohibition, and mends 2 and 10 moved all three rightly); Nuclear diplomacy 11 of 11; Third Front 15 of 15; the five entries that now carry the parent as a secondary thread have the right primary thread, and the parent fits all five; of 25 moved entries, 25 are right after mend 7's exception for the May 1964 conference (24 before it).

## 6. The verdict, thread by thread

A thread is fit to apply as it stands where about nine in ten read are right and its faults are of kinds that do no great harm. Where a sample was 10, a count of 8 is too few to tell 80 from 90 percent; I judge those by the kinds of fault.

Fit to apply as primary threads, as the rules now stand:

- Episodes: Shanghai and Beidaihe, 1960; Bucharest and Moscow; Twelve Articles; Famine; Sixty Articles; Seven Thousand Cadres; Xilou and the retreat; Beidaihe and the Tenth Plenum; India war; Polemic; Four Cleanups; Zhou in Africa; Third Front (after mend 7); Hai Rui; Luo Ruiqing; the six stages of the Cultural Revolution; Border war; Bomb and Nuclear diplomacy (after mends 2–6 and 10).
- Opera reform; Lei Feng, Dazhai, Daqing; Afro-Asian conference, each 8 of 10: fit, since their faults are a foreign guest at a show, a foreign visit at the conference's city or a word in a list, and the entries so taken are few.
- Persons: Mao Zedong, Zhou Enlai, Liu Shaoqi and the four subthreads. Their wrong entries are entries an episode should hold first; they are rightly in the person's family whichever thread is primary.
- Systems: Foreign affairs; Center's daily work; Political-legal work (27 of 30); Finance and economy (26 of 30); United front and nationalities (8 of 10, faults of two small kinds).
- The leftovers in `china-leadership` (35 of 40) and the plain `china` thread's moves (37 of 40).

Not fit to apply as primary threads as they stand:

- Propaganda and culture (22 of 30) and Army (22 of 30). Their entries, when the re-threading is done, should stay in `china-leadership`, with the thread named in `also:` so that no entry is lost to its page, until a second reading of their entries, entry by entry, sorts the lesser figures' days and the stages' business out of them. There are 520 and 565.
- Agriculture's own entries (5 of 10): its 615 primary entries should stay in `china-leadership` until read. Its three subthreads (Famine, Twelve Articles, Sixty Articles) are fit and should be applied under it, so the parent's page holds their entries.
- Organization (7 of 10 before mend 11, which takes out the faults of one of its kinds): hold its 376 primary entries in `china-leadership` until a fresh sample of 30 is read under the mended death rule.
- Nuclear weapons, the parent: it now has no primary entries, which is right; it stands as the parent of Bomb and Nuclear diplomacy.

As secondary threads:

- Fit: the persons' threads and subthreads (62 of 65), the episodes (32 of 33), and the eight systems other than the Center's daily work (70 of 78).
- Not fit: the Center's daily work as a secondary thread (7 of 38). Mend 1 takes it out of `also:` everywhere; it stays a primary thread.
- Hold as secondary threads too what is held as primary: Propaganda and culture, Army and Organization may stay in `also:` where the rules put them, since a wrong secondary thread loses nothing, but they should not be the reason an entry leaves `china-leadership`.

## 7. Is the assignment ready to apply

Yes for most of it, not for all. Of the 32 threads with primary entries sampled at 10 and the six read at 30, 34 are fit as the rules now stand, with the persons' subthreads and the two nuclear threads. Propaganda and culture, Army, Agriculture's own entries and Organization are not, and their primary entries (about 2,076) should stay in `china-leadership` with the thread in `also:` until they are read again. The Center's daily work must not go into `also:`; the mended tree.py no longer puts it there. The tsvs are in step with the rules as I leave them: `python3 tools/threads/china/measure.py`, then `python3 tools/threads/china/tree.py`, makes both again, as I ran them last. Bomb's statement will want its years opened to 1960 (mend 6).
