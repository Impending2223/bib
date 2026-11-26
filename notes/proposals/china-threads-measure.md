# China threads: the proposal measured

Nov. 26, 2026. For the owner. This note measures the proposal the owner liked on Nov. 22: the episodes as threads, Mao, Zhou Enlai and Liu Shaoqi as person threads, and the party's nine functional systems for the business below them. A system here means one of the fields the party divided its work into (in Chinese *xitong* or *kou*): the Center's daily work, foreign affairs, the army, finance and economy, agriculture, political-legal work, propaganda and culture, organization, united front and nationalities. Nothing in the calendar has been changed. The assignment is in `notes/threads/china-assign.tsv`, one row an entry. The record of the test is in `notes/threads/china-assign-test.tsv`. The command that makes the measurement again is `python3 tools/threads/china/measure.py`.

## 1. The rule

Each of the 26,347 entries now under `china-leadership` goes to the first of these that fits.

- An episode thread. The 26 episodes are the survey's. An entry fits one by a word of the episode inside its months, by a conference's days, by a word of the Cultural Revolution inside a stage's months, or because it was read from a book whose whole subject is the episode.
- The person thread of Mao, Zhou Enlai or Liu Shaoqi, where he is the one acting. He acts where he heads the line, alone or in a list, where the line's opening names an act of his, where he presides, or where he receives the caller.
- The system the business belongs to. The rule looks at the line, not at the book the entry was read from. It asks three things in order: what the matter is (the words of the business), what body meets (the Politburo, the Secretariat, the General Office), and who acts (the office the person holds).

An entry that fits none is a leftover and stays in `china-leadership`.

## 2. The shares

| kind | threads | entries | share |
|---|---:|---:|---:|
| episodes | 26 | 9,147 | 34.7% |
| Mao, Zhou Enlai, Liu Shaoqi | 3 | 6,500 | 24.7% |
| systems | 9 | 9,257 | 35.1% |
| leftovers | | 1,443 | 5.5% |

The episodes take a third, the three persons a quarter, the systems a third. About one entry in eighteen fits nothing.

How each entry was placed:

| rule | entries | share |
|---|---:|---:|
| a word of an episode inside its months | 5,842 | 22.2% |
| a book whose subject is the episode | 1,640 | 6.2% |
| a word of the Cultural Revolution inside a stage's months | 1,102 | 4.2% |
| a conference's days | 257 | 1.0% |
| Yang Shangkun at his Four Cleanups post in Shaanxi | 231 | 0.9% |
| one of the fallen leaders in custody, by the stage of the month | 75 | 0.3% |
| one of the three heads the line | 6,284 | 23.9% |
| one of the three acts in another way | 216 | 0.8% |
| the words of the business name a system | 7,008 | 26.6% |
| the person's office names the system | 1,890 | 7.2% |
| a body of the Center meets on mixed business | 359 | 1.4% |

## 3. The proposed threads

All are subthreads of `china`. The statements are drafts in the form `th.yaml` uses. The episodes' statements and stations are the survey's. I checked by script that every station's date falls on an entry the rule puts in that thread. I did not read the stations against the entries. The persons' and systems' stations I chose from entries the rule places there.

### Episodes

| slug | name | span | entries | draft statement (`c`) |
|---|---|---|---:|---|
| `china-shanghai-1960` | Shanghai and Beidaihe, 1960 | 1960-01..1960-09 | 134 | The year's targets set at Shanghai; the experts withdrawn and the summer conference at Beidaihe. {{1960-01-07..1960-01-17\|The enlarged Politburo at Shanghai.}} {{1960-07-05..1960-08-10\|Beidaihe; the Soviet experts recalled.}} |
| `china-moscow-1960` | Bucharest and Moscow | 1960-04..1961-01 | 158 | The quarrel with Moscow carried into the parties' meetings, from "Long Live Leninism!" to the Moscow Statement. {{1960-04-16\|"Long Live Leninism!"}} {{1960-06-24..1960-06-26\|Peng Zhen at Bucharest.}} {{1960-11-10..1960-12-01\|The eighty-one parties at Moscow; Liu Shaoqi with Khrushchev.}} |
| `china-twelve-articles` | Twelve Articles | 1960-09..1961-01 | 84 | The communes' "communist wind" checked: the emergency letter and the Ninth Plenum. {{1960-11-03\|The Emergency Directive Letter, the "Twelve Articles."}} {{1960-11-15\|Mao's directive on the "five winds."}} {{1961-01-14..1961-01-18\|The Ninth Plenum.}} |
| `china-famine` | Famine | 1960-01..1962-12 | 962 | The famine as the provinces reported it, the grain moved and bought abroad, the deaths counted. {{1960-06-03\|The Taolin report on the deaths.}} {{1960-10-03\|Chen Yun on Hebei and Shandong.}} {{1961-01-03\|Henan's relief directive.}} |
| `china-sixty-articles` | Sixty Articles | 1961-02..1961-09 | 322 | The year of investigation: the communes' regulations drafted at Canton, revised at Peking, and the industrial articles at Lushan. {{1961-03-10..1961-03-23\|The Canton conference; the Sixty Articles.}} {{1961-04-02..1961-05-15\|Liu Shaoqi in Hunan.}} {{1961-08-23..1961-09-16\|Lushan; the Seventy Articles.}} |
| `china-seven-thousand` | Seven Thousand Cadres | 1961-11..1962-02 | 111 | The enlarged work conference of January 1962: Liu's report, Mao's self-criticism, Lin Biao's defense of the Leap. {{1962-01-11\|The conference opens.}} {{1962-01-27\|Liu Shaoqi's report.}} {{1962-01-30\|Mao's speech.}} |
| `china-retreat-1962` | Xilou and the retreat | 1962-02..1962-07 | 135 | Chen Yun's deficit and emergency program, the cities emptied, the household contracts. {{1962-02-21..1962-02-23\|The Xilou meeting.}} {{1962-05-07..1962-05-11\|The May work conference; the streamlining.}} {{1962-07-06..1962-07-23\|Mao against household contracting.}} |
| `china-tenth-plenum` | Beidaihe and the Tenth Plenum | 1962-07..1962-10 | 137 | "Never forget class struggle": the Beidaihe conference, the plenum, Peng Dehuai's case reopened. {{1962-08-06..1962-08-24\|Beidaihe.}} {{1962-08-26\|The plenum's preparatory meeting.}} {{1962-09-24..1962-09-27\|The Tenth Plenum.}} |
| `china-india-war` | India war | 1962-06..1963-03 | 102 | The border war with India and the cease-fire. {{1962-07-22\|Mao on the Galwan post.}} {{1962-11-21\|The cease-fire declared.}} {{1963-01-05\|Zhou and Bandaranaike.}} |
| `china-polemic` | Polemic | 1961-10..1964-11 | 422 | The open polemic with Moscow, from the Twenty-second Congress to Zhou in Moscow after Khrushchev's fall. {{1961-10-17..1961-10-23\|Zhou at the Twenty-second Congress.}} {{1963-06-14..1963-07-20\|The general line; Deng and Suslov.}} {{1964-11-05..1964-11-14\|Zhou in Moscow.}} |
| `china-four-cleanups` | Four Cleanups | 1962-09..1966-05 | 1,012 | The socialist education movement: the Ten Points, the work teams, Taoyuan, Niujiao, the Twenty-three Articles. {{1963-05-02..1963-05-12\|The Hangzhou conference; the First Ten Points.}} {{1964-10-28..1965-05\|Yang Shangkun at Niujiao and Xi'an.}} {{1964-12-15..1965-01-14\|The work conference; the Twenty-three Articles.}} |
| `china-models` | Lei Feng, Dazhai, Daqing | 1963-01..1965-12 | 96 | The emulation campaigns: Lei Feng, the Dazhai brigade, the Daqing oilfield, learning from the army. {{1963-03-05..1963-03-06\|"Learn from Comrade Lei Feng."}} {{1964-01-02\|The General Office on Daqing.}} {{1964-12\|Dazhai in the Government Work Report.}} |
| `china-opera` | Opera reform | 1963-10..1965-11 | 66 | The arts rectified: Mao's two instructions, the festival of modern Peking opera, the ministry purged. {{1964-06-23\|Zhou with the festival's troupes.}} {{1964-06-05..1964-07-31\|The festival of modern Peking opera.}} {{1965-04\|The Ministry of Culture reorganized.}} |
| `china-africa-tour` | Zhou in Africa | 1963-12..1964-03 | 207 | Zhou Enlai's and Chen Yi's tour of ten African countries and Albania, the eight principles of aid. {{1963-12-14\|To Cairo.}} {{1963-12-21..1963-12-27\|Algeria.}} {{1964-01-15\|Accra; the eight principles.}} |
| `china-third-front` | Third Front | 1964-04..1966-05 | 117 | The interior industrial base: the Third Plan recast for war, Panzhihua and the southwest railways. {{1964-05-15..1964-06-17\|The work conference; the third front.}} {{1965-03-29\|Zhu De at Chengdu.}} {{1965-11-13\|The plan conference.}} |
| `china-afro-asian` | Afro-Asian conference | 1964-04..1965-11 | 95 | The second Asian–African conference sought and lost at Algiers. {{1965-03-30..1965-04-01\|Zhou at Algiers.}} {{1965-06-19..1965-06-28\|Ben Bella deposed; the conference put off.}} {{1965-11-04\|China's withdrawal.}} |
| `china-bomb` | Bomb | 1963-07..1969-10 | 165 | The atomic and hydrogen bombs and the missiles: their decisions and tests. {{1963-07-28\|The test ban discussed.}} {{1964-10-16\|The first test; the statement.}} {{1966-10-27\|The missile with a warhead.}} {{1967-06-17\|The hydrogen bomb.}} |
| `china-hai-rui` | Hai Rui | 1965-09..1966-03 | 102 | Yao Wenyuan's article, the Peking committee's defense of Wu Han, the February Outline. {{1965-11-10\|Yao Wenyuan's article.}} {{1965-11-29\|The *Beijing Daily* reprints it.}} {{1966-02-12\|The February Outline circulated.}} |
| `china-luo-ruiqing` | Luo Ruiqing | 1965-11..1966-05 | 98 | The Chief of Staff accused by Lin Biao and removed at the Shanghai conference. {{1965-11-27\|Luo with Lin Biao.}} {{1965-12-08..1965-12-15\|The Shanghai conference.}} {{1966-03-04..1966-04-08\|The struggle meetings.}} |
| `china-may-sixteenth` | May Sixteenth and the work teams | 1966-04..1966-07 | 631 | The enlarged Politburo and its Circular, Peng Zhen's fall, Nie Yuanzi's poster, the fifty days of the work teams. {{1966-05-16\|The May 16 Circular.}} {{1966-05-25\|Nie Yuanzi's poster.}} {{1966-07-16\|Mao in the Yangtze.}} {{1966-07-28\|The work teams withdrawn.}} |
| `china-red-guards` | Red Guards | 1966-08..1966-12 | 1,083 | The Eleventh Plenum and the Red Guards: the rallies, the "four olds," the house searches, the attack on the "reactionary line." {{1966-08-01..1966-08-12\|The Eleventh Plenum; "Bombard the Headquarters."}} {{1966-08-18\|The first rally.}} {{1966-10-09..1966-10-28\|The October work conference.}} |
| `china-seizures` | Seizures of power | 1967-01..1967-04 | 758 | The January Storm at Shanghai, the seizures in the provinces, the army sent in, the February Countercurrent. {{1967-01-06\|The rebels take Shanghai.}} {{1967-01-23\|The army to support the left.}} {{1967-02-16\|The Huairen Hall.}} |
| `china-wuhan` | Wuhan and the army | 1967-05..1967-12 | 970 | The army's factions and the armed struggle: Wuhan, the drive against "the handful in the army," the fall of Wang Li and Guan Feng. {{1967-07-20\|The Million Heroes take Wang Li.}} {{1967-08-22\|The British office burned.}} {{1967-08-30\|Wang Li and Guan Feng detained.}} |
| `china-class-ranks` | Revolutionary committees | 1968-01..1968-09 | 706 | The revolutionary committees completed and the class ranks cleansed: Yang Chengwu's fall, the July notices, the propaganda teams. {{1968-03-24\|Yang Chengwu, Yu Lijin and Fu Chongbi dismissed.}} {{1968-07-28\|Mao with the five Red Guard leaders.}} {{1968-09-05\|The last committees, Tibet and Xinjiang.}} |
| `china-ninth-congress` | Ninth Congress | 1968-10..1969-04 | 402 | Liu Shaoqi expelled at the Twelfth Plenum; the Ninth Congress and Lin Biao as successor. {{1968-10-13..1968-10-31\|The Twelfth Plenum.}} {{1969-04-01..1969-04-24\|The Ninth Congress.}} {{1969-04-28\|Lin Biao's report printed.}} |
| `china-border-war` | Border war | 1969-02..1969-12 | 72 | The clashes on the Ussuri and in Xinjiang, the war scare, the airport talks and the border talks. {{1969-03-02\|Zhenbao.}} {{1969-09-11\|Kosygin at the Peking airport.}} {{1969-10-17..1969-10-20\|Order No. 1; the border talks.}} |

### Persons

| slug | name | span | entries | draft statement (`c`) |
|---|---|---|---:|---|
| `china-mao` | Mao | 1960-01..1970-01 | 1,567 | Mao Zedong's own acts outside the episodes: his comments and instructions, letters, talks, audiences, poems, swims, travels. {{1960-10-22\|Edgar Snow.}} {{1961-09-23\|Montgomery at Wuchang.}} {{1964-02-13\|The Spring Festival forum on education.}} {{1965-05\|Jinggangshan revisited.}} |
| `china-zhou` | Zhou Enlai | 1960-01..1970-01 | 4,361 | The Premier's day outside the episodes: the State Council, the plan, the guests and the visits abroad. {{1960-01-28\|The boundary agreement with Burma before the State Council.}} {{1960-04\|Rangoon, Delhi, Kathmandu.}} {{1963-03-02\|Bhutto; the boundary agreement with Pakistan.}} {{1965-06\|Pakistan and Tanzania.}} {{1969-09-02..1969-09-09\|Hồ Chí Minh's death.}} |
| `china-liu` | Liu Shaoqi | 1960-01..1968-07 | 572 | The head of state to his fall: his comments, forums, receptions and visits abroad. {{1963-04-12..1963-05-16\|Indonesia, Burma, Cambodia, Vietnam.}} {{1964-07\|The two labor systems and the two education systems.}} {{1966-03-26..1966-04-19\|Pakistan, Afghanistan, Burma.}} |

### Systems

| slug | name | span | entries | draft statement (`c`) |
|---|---|---|---:|---|
| `china-center` | Center's daily work | 1960-01..1969-11 | 1,909 | The Politburo's and the Secretariat's sittings on mixed business, the General Office and its callers, the papers sent round, to Yang Shangkun's removal. {{1960-04-02\|The "five many."}} {{1961-05\|The recordings.}} {{1965-11\|Yang Shangkun's last month at the General Office.}} |
| `china-foreign` | Foreign affairs | 1960-01..1969-12 | 3,812 | Foreign business not done by Mao, Zhou Enlai or Liu Shaoqi: Chen Yi's and the others' receptions, visits, speeches and cables, the Foreign Ministry and the International Liaison Department. {{1961-05-16\|Chen Yi at Geneva; the conference on Laos.}} {{1962-07-23\|The Geneva agreements on Laos.}} |
| `china-army` | Army | 1960-01..1970-01 | 618 | The Military Commission, the General Staff and the General Political Department; training, the coast, the militia, the marshals' inspections. {{1960-09..1960-10\|The enlarged Military Commission.}} {{1961-01-20\|The training conference.}} {{1962-06\|Preparing for war on the coast.}} {{1964-06-10\|The display of picked units.}} {{1965-05-22\|Ranks abolished.}} {{1969-10-18\|The orders to the General Staff.}} |
| `china-economy` | Finance and economy | 1960-01..1970-01 | 946 | The plan, industry and transport, finance and trade: the commissions' and ministries' reports, the Center's papers on them, the inspections of plants. {{1962-04-19\|The Central Finance and Economic Group under Chen Yun.}} {{1964-08-17\|The trusts.}} {{1965-11\|Deng Xiaoping in the Southwest's plants.}} |
| `china-agriculture` | Agriculture | 1960-01..1969-12 | 616 | Farming, grain, water and the communes outside the named episodes: the Center's rural papers, the leaders' inspections of communes and farms. {{1960-10-07\|Tan Zhenlin on five provinces' farming.}} {{1961-11\|Peng Dehuai at Wushi.}} {{1963-10-16\|Zhu De in the flooded provinces.}} {{1964-06-25\|The poor and lower-middle peasant associations.}} |
| `china-political-legal` | Political-legal work | 1960-02..1970-01 | 237 | The National People's Congress and its Standing Committee, public security, the procuracy and the courts, the census. {{1960-03-30\|The National People's Congress, second session.}} {{1962-03-27\|The third session.}} {{1963-02-17\|The draft Criminal Law.}} {{1964-02-10\|The census.}} |
| `china-propaganda` | Propaganda and culture | 1960-01..1969-11 | 550 | Propaganda, the press, education, science, health, the arts and sport outside the named episodes. {{1961-07-13\|The Secretariat on the schools.}} {{1962-03-05\|Chen Yi to the scientists at Canton.}} {{1962-04-30\|The Eight Articles on Literature and Art.}} {{1964-08\|The Peking Science Symposium.}} {{1966-03-08\|The Education Office.}} |
| `china-organization` | Organization | 1960-01..1970-01 | 376 | Cadres and the Party's own bodies: appointments, the control commissions, the Youth League, the trade unions and the Women's Federation, the deaths of leaders, the case groups after April 1969. {{1960-05-29\|Lin Boqu's death.}} {{1962-02-28\|The control commissions enlarged.}} {{1963-12-16\|Luo Ronghuan's death.}} {{1964-06\|The Youth League's Ninth Congress.}} {{1965-04-09\|Ke Qingshi's death.}} |
| `china-united-front` | United front and nationalities | 1960-01..1969-05 | 193 | The United Front Department, the Political Consultative Conference and the democratic parties, the nationalities and religion, the overseas Chinese, Taiwan, Hong Kong and Macao. {{1960-05\|The line on Taiwan.}} {{1961-06-15\|The forum on placing the bourgeoisie.}} {{1962-04-16\|The Kazakhs' flight.}} {{1962-05\|The national united front work conference.}} {{1965-07-27\|Li Zongren's return.}} |

### By year

| thread | entries | 1960 | 1961 | 1962 | 1963 | 1964 | 1965 | 1966 | 1967 | 1968 | 1969 | 1970 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `china-shanghai-1960` | 134 | 134 |  |  |  |  |  |  |  |  |  |  |
| `china-twelve-articles` | 84 | 50 | 34 |  |  |  |  |  |  |  |  |  |
| `china-famine` | 962 | 533 | 332 | 93 | 4 |  |  |  |  |  |  |  |
| `china-sixty-articles` | 322 |  | 322 |  |  |  |  |  |  |  |  |  |
| `china-seven-thousand` | 111 |  | 8 | 103 |  |  |  |  |  |  |  |  |
| `china-retreat-1962` | 135 |  |  | 135 |  |  |  |  |  |  |  |  |
| `china-tenth-plenum` | 137 |  |  | 137 |  |  |  |  |  |  |  |  |
| `china-moscow-1960` | 158 | 156 | 2 |  |  |  |  |  |  |  |  |  |
| `china-polemic` | 422 |  | 52 | 52 | 171 | 147 |  |  |  |  |  |  |
| `china-india-war` | 102 |  |  | 72 | 30 |  |  |  |  |  |  |  |
| `china-africa-tour` | 207 |  |  |  | 56 | 151 |  |  |  |  |  |  |
| `china-afro-asian` | 95 |  |  |  |  | 24 | 71 |  |  |  |  |  |
| `china-bomb` | 165 |  |  |  | 24 | 44 | 25 | 30 | 14 | 12 | 16 |  |
| `china-four-cleanups` | 1012 |  |  | 9 | 162 | 337 | 480 | 24 |  |  |  |  |
| `china-models` | 96 |  |  |  | 31 | 42 | 23 |  |  |  |  |  |
| `china-third-front` | 117 |  |  |  |  | 28 | 63 | 26 |  |  |  |  |
| `china-opera` | 66 |  |  |  | 4 | 50 | 12 |  |  |  |  |  |
| `china-luo-ruiqing` | 98 |  |  |  |  |  | 58 | 40 |  |  |  |  |
| `china-hai-rui` | 102 |  |  |  |  |  | 59 | 43 |  |  |  |  |
| `china-may-sixteenth` | 631 |  |  |  |  |  |  | 631 |  |  |  |  |
| `china-red-guards` | 1083 |  |  |  |  |  |  | 1083 |  |  |  |  |
| `china-seizures` | 758 |  |  |  |  |  |  |  | 758 |  |  |  |
| `china-wuhan` | 970 |  |  |  |  |  |  |  | 970 |  |  |  |
| `china-class-ranks` | 706 |  |  |  |  |  |  |  |  | 706 |  |  |
| `china-ninth-congress` | 402 |  |  |  |  |  |  |  |  | 128 | 274 |  |
| `china-border-war` | 72 |  |  |  |  |  |  |  |  |  | 72 |  |
| `china-mao` | 1567 | 291 | 179 | 175 | 170 | 205 | 193 | 108 | 90 | 77 | 77 | 2 |
| `china-zhou` | 4361 | 579 | 475 | 364 | 537 | 513 | 647 | 462 | 290 | 188 | 295 | 11 |
| `china-liu` | 572 | 107 | 91 | 52 | 107 | 71 | 73 | 66 | 3 | 2 |  |  |
| `china-center` | 1909 | 202 | 355 | 326 | 345 | 283 | 339 | 40 | 7 |  | 12 |  |
| `china-foreign` | 3812 | 619 | 498 | 434 | 557 | 591 | 609 | 286 | 106 | 78 | 34 |  |
| `china-army` | 618 | 65 | 70 | 47 | 48 | 106 | 95 | 72 | 50 | 12 | 51 | 2 |
| `china-economy` | 946 | 209 | 235 | 122 | 125 | 88 | 85 | 43 | 8 | 5 | 25 | 1 |
| `china-agriculture` | 616 | 114 | 187 | 95 | 69 | 75 | 34 | 28 | 3 | 1 | 10 |  |
| `china-political-legal` | 237 | 35 | 27 | 46 | 29 | 42 | 29 | 15 |  | 4 | 9 | 1 |
| `china-propaganda` | 550 | 76 | 104 | 57 | 64 | 92 | 68 | 52 | 13 | 3 | 21 |  |
| `china-organization` | 376 | 23 | 47 | 79 | 55 | 55 | 74 | 14 | 4 | 2 | 20 | 3 |
| `china-united-front` | 193 | 35 | 30 | 34 | 34 | 27 | 22 | 8 |  | 1 | 2 |  |
| leftover | 1443 | 202 | 232 | 181 | 231 | 242 | 197 | 76 | 22 | 17 | 38 | 5 |

### Threads under 100 and over 3,000

Six episodes fall under 100: Twelve Articles (84), Afro-Asian conference (95), Lei Feng, Dazhai, Daqing (96), Opera reform (66), Luo Ruiqing (98), Border war (72). They were larger in the survey. The test showed that their extra entries were there by a place name or a person's name alone, and the mended rule no longer takes those.

Two threads run over 3,000: Zhou Enlai (4,361) and Foreign affairs (3,812). Of Zhou's entries 2,661 are foreign business. Section 7 gives the choices.

## 4. Entries that fit two

16,859 entries (64.0 percent) fit a second thread. The second thread is in the last column of the tsv.

| the entry went to | it also fits | entries | how the rule settles it |
|---|---|---:|---|
| a person | a system | 5,676 | the person comes first |
| an episode | a system | 5,132 | the episode comes first |
| an episode | a person | 2,689 | the episode comes first |
| a system | a second system | 2,567 | the system with more of the line's words; on a tie a fixed order |
| an episode | a second episode | 500 | two rules for known joins, then the episode with the shorter span |
| a person | a second person | 290 | the one named first |

The two rules for known joins: an entry of July 1962 on household contracting goes to Xilou and the retreat before July 25 and to the Tenth Plenum from that day; a famine report that only mentions a mess hall goes to Famine and not to Twelve Articles.

The commonest pairs:

| taken by | also fits | entries |
|---|---|---:|
| `china-zhou` | `china-foreign` | 2661 |
| `china-mao` | `china-foreign` | 457 |
| `china-famine` | `china-agriculture` | 439 |
| `china-zhou` | `china-economy` | 384 |
| `china-foreign` | `china-propaganda` | 361 |
| `china-four-cleanups` | `china-center` | 303 |
| `china-liu` | `china-foreign` | 250 |
| `china-may-sixteenth` | `china-propaganda` | 225 |
| `china-wuhan` | `china-zhou` | 225 |
| `china-red-guards` | `china-propaganda` | 218 |
| `china-zhou` | `china-army` | 212 |
| `china-foreign` | `china-economy` | 211 |
| `china-polemic` | `china-foreign` | 208 |
| `china-zhou` | `china-agriculture` | 205 |
| `china-zhou` | `china-propaganda` | 185 |
| `china-seizures` | `china-zhou` | 171 |
| `china-wuhan` | `china-army` | 168 |
| `china-africa-tour` | `china-zhou` | 167 |
| `china-seizures` | `china-army` | 165 |
| `china-red-guards` | `china-zhou` | 162 |

The largest pairs of two episodes: Revolutionary committees and Ninth Congress, 98; Wuhan and Seizures of power, 86; Red Guards and May Sixteenth, 77; May Sixteenth and Hai Rui, 34. Most of these are entries dated by year only. A year-dated entry cannot be put in a stage of a few months. The rule puts it in the stage that covers most of its year. There are 869 year-dated entries in the bucket.

## 5. The test by reading

I drew 30 entries at random from each proposed thread and 60 from the leftovers, 1,200 in all, and read each line and its note. I counted an entry right where it belongs to the thread as the thread's statement describes it. I counted it wrong where it belongs to another thread or to none. Where two threads could both hold it and the rule chose one of them, I counted it right and marked it arguable. 969 of the 1,200 were right: 623 of 780 in the episodes, 81 of 90 in the persons, 218 of 270 in the systems, 47 of 60 in the leftovers.

I then mended the rules that were wrong often and measured again. For the twelve threads that scored under 24 I drew a second sample of 30 and read it. Those twelve went from 236 right of 360 to 322 of 360. The second reading printed each line's first 140 characters and the name of its source, not the whole note.

| thread | first reading, right of 30 | second reading after the mends, right of 30 |
|---|---:|---:|
| `china-shanghai-1960` | 14 | 27 |
| `china-moscow-1960` | 25 |  |
| `china-twelve-articles` | 21 | 25 |
| `china-famine` | 25 |  |
| `china-sixty-articles` | 22 | 24 |
| `china-seven-thousand` | 25 |  |
| `china-retreat-1962` | 26 |  |
| `china-tenth-plenum` | 17 | 28 |
| `china-india-war` | 25 |  |
| `china-polemic` | 19 | 28 |
| `china-four-cleanups` | 25 |  |
| `china-models` | 19 | 26 |
| `china-opera` | 17 | 30 |
| `china-africa-tour` | 30 |  |
| `china-third-front` | 24 |  |
| `china-afro-asian` | 20 | 26 |
| `china-bomb` | 20 | 27 |
| `china-hai-rui` | 28 |  |
| `china-luo-ruiqing` | 24 |  |
| `china-may-sixteenth` | 29 |  |
| `china-red-guards` | 30 |  |
| `china-seizures` | 29 |  |
| `china-wuhan` | 29 |  |
| `china-class-ranks` | 30 |  |
| `china-ninth-congress` | 27 |  |
| `china-border-war` | 23 | 28 |
| `china-mao` | 27 |  |
| `china-zhou` | 28 |  |
| `china-liu` | 26 |  |
| `china-center` | 24 |  |
| `china-foreign` | 26 |  |
| `china-army` | 24 |  |
| `china-economy` | 25 |  |
| `china-agriculture` | 25 |  |
| `china-political-legal` | 22 | 28 |
| `china-propaganda` | 22 | 25 |
| `china-organization` | 24 |  |
| `china-united-front` | 26 |  |
| leftovers | 47 of 60 | 26 of 30 |

By rule, in the first reading: a word of an episode, 503 right of 638; a book, 53 of 61; a stage's words, 50 of 52; a conference's days, 14 of 25; a person at the head, 79 of 88; the words of the business, 185 of 225; the person's office, 32 of 42.

The counts are mine alone. No second reader checked them.

## 6. What the test changed in the rules

1. A place or a person is no longer enough to put an entry in an episode. The survey's lists took every entry at Beidaihe in the summer of 1960 and 1962, every entry at Lushan in 1961, every entry naming Tian Jiaying in 1962, every entry at Algiers or Jakarta in 1964–65. Half of those were swims, calls and receptions. Now a conference's seat counts only with a word for a meeting, and a person's name only with a second word of the episode.
2. A swim, a doctor, a poem or a journey inside a conference's weeks is not part of the conference.
3. The conference-days rule no longer takes foreign business.
4. Polemic: Albania, Khrushchev and "revisionism" alone no longer place an entry. Pravda, the numbered comments and the letters to and from the Soviet party were added.
5. Bomb: the foreign conferences against atomic bombs were taken out. The Central Special Commission and the two ministries were added.
6. Lei Feng, Dazhai, Daqing: "political department" alone no longer places an entry. It had taken the General Political Department's parties.
7. Opera reform: a foreign guest taken to the theatre is foreign business.
8. Border war: "prepare for war" in a paper on the plan no longer places an entry.
9. India war: the Chinese name of Indonesia begins with the characters for India. The rule now tells them apart.
10. Sixty Articles: the leaders' rural inquiries of April and May 1961 (Tianhua, Ningxiang, Xushui, Shunyi, Huairou) were added.
11. May Sixteenth: an entry naming Peng Zhen between Apr. 9 and May 31, 1966 was added.
12. The Cultural Revolution's words: "struggled against", "case group", "interrogated", "the sentry" and the like were added, so that what was done to the fallen goes to the stage of its month. A line headed by a fallen leader after his fall goes to the stage of its month even without such a word.
13. A year-dated entry that fits two stages goes to the one that covers more of its year. Before, it went to the shorter stage.
14. Yang Shangkun's stay in Shaanxi, October 1964 to May 1965, goes to Four Cleanups wherever the line names him and the place. The survey did this for Niujiao only.
15. The systems' word lists were corrected in many small ways. The largest: a person's name is no longer a word of a system; a newspaper is the place a thing is printed and not its system; words far down a long line count for little.

One rule I tried and withdrew. It put every domestic entry of May 1966 to April 1969 that no word placed into the stage of its month, ahead of the systems. I read 30 of its entries and 17 were right. The wrong ones were National Day and Army Day appearances, a death, a budget, a visit to an exhibition. I kept only the narrow rule for the fallen (number 12).

## 7. The leftovers

1,443 entries fit nothing. By kind:

- A lesser figure's own day, 616: a swim, a doctor, a film, a poem, an inscription. "Peking. Yang Shangkun swims." "Peking Hospital, 3 p.m. Yang Shangkun's treatment goes on." "Chen Yi writes the poem 'Greeting New Year's Day 1966'." "Shanghai. Chen Yun rests, to Sept. 7."
- A lesser figure's journey with no business stated, 507. "Zhu De flies to Guangzhou." "Deng Xiaoping goes by special train to Lanzhou, arriving on the 16th." "Chen Yun goes from Hangzhou to Shanghai."
- A short line with no business stated, 161. "Zigong. Zhu De hears the heads of the Zigong committee." "Peking, the Yinian Tang. Zhu De at a meeting."
- Other, 159. "Peng Dehuai, sighing, says: it is killing me." "The drafting committee, 3 to 8 p.m., five hours, on part two of the report."

By the person at the head of the line: Yang Shangkun 451, Zhu De 413, Chen Yi 80, Chen Yun 79, Deng Xiaoping 67, Peng Dehuai 53, Peng Zhen 40, Ye Jianying 19, Lin Biao 13; no person, 70. Mao, Zhou and Liu leave almost none, because their person threads take their swims and journeys.

In the test 47 of 60 leftovers, and then 26 of 30, were rightly left. The ones wrongly left belonged to an episode or a system whose words the line did not use.

Where the nine lesser persons of the survey went, by the entries each heads:

| person | heads | episode | person | center | foreign | army | economy | agriculture | political-legal | propaganda | organization | united-front | - |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Zhu De | 1345 | 78 | 55 | 19 | 205 | 54 | 214 | 185 | 66 | 30 | 5 | 21 | 413 |
| Chen Yi | 2231 | 121 | 75 |  | 1834 | 27 | 8 | 5 | 3 | 45 | 2 | 31 | 80 |
| Yang Shangkun | 1981 | 353 | 24 | 684 | 198 | 19 | 86 | 58 | 6 | 35 | 80 | 10 | 428 |
| Peng Zhen | 1227 | 312 | 104 | 147 | 315 | 19 | 72 | 44 | 70 | 49 | 30 | 25 | 40 |
| Deng Xiaoping | 1049 | 278 | 57 | 66 | 341 | 25 | 104 | 30 | 9 | 46 | 21 | 9 | 63 |
| Chen Yun | 341 | 47 | 3 | 3 | 4 | 2 | 108 | 49 | 1 | 41 | 4 |  | 79 |
| Peng Dehuai | 323 | 182 | 1 | 10 | 2 | 5 | 15 | 32 | 1 | 7 | 15 |  | 53 |
| Ye Jianying | 284 | 97 | 3 |  | 9 | 137 | 5 |  | 1 | 9 | 1 | 3 | 19 |
| Lin Biao | 168 | 70 | 1 | 2 | 3 | 71 | 2 |  | 1 | 3 | 2 |  | 13 |

Zhu De shows this most clearly. His receptions go to Foreign affairs, his inspections to Finance and economy or Agriculture by what he inspected, his sittings to Political-legal work. 413 of his entries, nearly a third, are arrivals, departures, walks and poems, and no system holds them.

## 8. Questions that are the owner's

**1. Where a system and a person cross.** Zhou Enlai's thread holds 4,361 entries, over the limit of 3,000. 2,661 of them are foreign business: a reception, a talk, a visit abroad. If foreign business went to Foreign affairs before the person threads of Zhou and Liu, Zhou would hold 1,623 and Liu 308, and Foreign affairs would hold 6,795. Mao's 457 foreign entries stay with Mao in both counts. The default I took is the order the proposal states: the person first. Either way one thread is too large and must be divided.

**2. Where foreign business sits against the country threads the calendar already has.** Foreign affairs as measured holds 3,812. By the first country a line names, 2,598 of them fall to twelve threads the calendar has, 532 to countries with no thread, and 682 name no country.

| country thread | in china-foreign | in china-zhou or china-liu, also fitting china-foreign |
|---|---:|---:|
| (no country named) | 682 | 409 |
| africa | 427 | 442 |
| soviet-union | 561 | 221 |
| south-asia | 246 | 359 |
| vietnam-hanoi | 293 | 299 |
| (no thread) burma-cambodia-neutrals | 240 | 259 |
| (no thread) bloc-europe | 271 | 220 |
| japan | 211 | 129 |
| indonesia | 192 | 126 |
| korea | 182 | 128 |
| europe-and-the-alliance | 171 | 70 |
| middle-east | 79 | 77 |
| laos | 80 | 62 |
| cuba | 78 | 43 |
| latin-america | 78 | 37 |
| (no thread) mongolia | 21 | 30 |

The choices: keep one Foreign affairs thread for China and divide it by region or by years; or send each entry to the country's thread with `also: [china]`, as the calendar does for other nations' foreign business, and keep Foreign affairs for the 1,214 with no thread or no country. Many of these entries already carry the country's thread in `also:`. The second choice would add about 430 entries to Africa and 560 to the Soviet Union from this thread alone, and as many again from Zhou's and Liu's if question 1 goes that way.

**3. What becomes of `india-and-china-cultural-revolution`.** It has 4 entries of its own, of July and August 1966. 564 entries of `china-leadership` carry it in `also:`, dated November 1965 to January 1970, nearly all of 1968 and 1969. Under the rule they go to Zhou Enlai (198), Revolutionary committees (181), Ninth Congress (92), Mao (47), Border war (13), Bomb (9) and others (24). The six stages cover the same matter. The choice is to retire it, keeping its id as an alias so that no link breaks, or to keep the name "Cultural Revolution" over the six stages. `th.yaml` has no thread under a subthread today, so the second choice needs a ruling on form.

**4. The book rule.** 1,640 entries (6.2 percent) go to an episode because of the book they were read from: Yang Jisheng's and Dikötter's famine books to Famine, Wu Lengxi's memoir to the two Moscow threads, the four histories of the Cultural Revolution to the stage of the entry's month. This is a cut by the book read, which the owner objected to. In the test 53 of 61 such entries were right, because these books treat one subject. Without the rule the episodes fall to 28.5 percent, the systems rise to 39.8 and the leftovers to 6.6. The default taken: keep it.

**5. The office rule and the Center's daily work.** 1,890 entries (7.2 percent) state no business, and the rule places them by the office of the person named. About 1,500 of them name Yang Shangkun, the director of the General Office: "Peking. Wang Yuming with Yang Shangkun." Of the 1,909 entries in the Center's daily work, 1,558 name him. So that thread is in large part his callers and sittings of 1960 to 1965, as his diary records them. Without the office rule the Center's thread holds 359 and the leftovers rise to 12.7 percent. In the test 32 of 42 such entries were right. The default taken: a caller on the General Office's director is the Center's daily work.

**6. The private days.** 1,123 leftovers are a lesser figure's swim, illness, poem or journey. The survey asked whether some are outside the brief (R18). They stay in `china-leadership` under this rule. The owner may want them out of the calendar's threads, kept there, or given a thread of their own.

**7. Three placings I made by default.** The National People's Congress and its Standing Committee are under Political-legal work (158 of that thread's 237 entries). The Youth League, the trade unions and the Women's Federation are under Organization. Science, health and sport are under Propaganda and culture. Each could sit elsewhere.

**8. The small threads.** Six episodes hold under 100 entries. They can stand as they are or be folded: Twelve Articles into Famine or Sixty Articles, Opera reform into Propaganda and culture, Luo Ruiqing into May Sixteenth.

## 9. What was not done

The assignment was not applied. No entry, thread or source was changed. The stations were checked for date only. The `thread: china` entries (1,484) were not assigned; 383 of them would fit an episode by the same rule (Famine 71, Wuhan and the army 70, India war 64, Red Guards 40, Bomb 26). The rules for the systems are word lists, and a line that states its business in other words is missed or misplaced; the test's counts say how often.
