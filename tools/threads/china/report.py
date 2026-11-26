import json,pickle,collections,random,re
from lexicon import EP
OUT=[]; P=OUT.append
E=[json.loads(l) for l in open('china.jsonl')]
ED={e['id']:e for e in E}
CL=[e for e in E if e['thread']=='china-leadership']
BL='▁▂▃▄▅▆▇█'
def months(lo,hi):
    y,m=int(lo[:4]),int(lo[5:7]); out=[]
    while (y,m)<=(int(hi[:4]),int(hi[5:7])):
        out.append(f'{y}-{m:02d}'); m+=1
        if m>12: y+=1; m=1
    return out
def spark(by,lo,hi):
    ms=months(lo,hi); v=[by.get(m,0) for m in ms]; mx=max(v) if v and max(v) else 1
    return ''.join(' ' if x==0 else BL[min(7,int(x*7/mx+0.5))] for x in v)
P('# China: leadership — a survey of cutting lines\n')
P('Scratch analysis, Nov. 22, 2026 (Sunday). Read-only; regex over lists/cal/*.yaml (scripts beside this file). Base: the 26,320 entries with `thread: china-leadership`; where noted, also the 1,478 `thread: china` and the entries with `also: [china-leadership]` or `also: [india-and-china-cultural-revolution]` (28,423 in all touching the China threads).\n')
P('## 1. What the bucket is made of\n')
fw=collections.Counter(e['works'][0] if e['works'] else '-' for e in CL)
P('The first work cited in `n`, the source the entry was read from. The bucket is a set of digested daybooks: one diary and a dozen nianpu give about 70 percent of it.\n')
P('| first source | entries |\n|---|---:|')
for w,n in fw.most_common(25): P(f'| `{w}` | {n} |')
P('\nBy year (china-leadership): '+', '.join(f'{y} {n}' for y,n in sorted(collections.Counter(e["date"][:4] for e in CL).items()))+'. 869 entries are dated by year only, 2,094 by month only.\n')
P('## 2. Episodes: the named meetings, campaigns, documents and affairs\n')
P('Candidates from (a) the brief\'s list, (b) capitalized multi-word phrases, quoted slogans, numbered formulas and 《》 titles by frequency (`phrases.py`, `phrases.json`), (c) general knowledge of the period. Each is a regex (English and Chinese forms; `lexicon.py`) plus a date window. `all` = entries matching anywhere in 1960–70; `win` = matches inside the window; `CL` = share of `win` already in china-leadership; `CR` = how many carry `also: india-and-china-cultural-revolution`. Density: entries per month across the window, one character a month (blank = none).\n')
P('Frequency check (phrases, entries naming them): Sixty Articles 53; Seven Thousand Cadres Conference 36–40; Tenth Plenum 28–36; Eleventh Plenum 32–36; Twelfth Plenum 30–34; Ninth Congress 86; Twenty-three Articles 25–31; Ten Points 33; "four clean-ups" 72+; "five antis" 48; Third Five-Year Plan 45; third front 25+9; Three-Family Village 18; Hai Rui 39; Lei Feng 28; Red Guards 288+118; Cultural Revolution Group 113+63; Million Heroes 30; "February adverse current"/"counter-current" 17; "May 16" 12, May 16 Corps 6; 4·22 27. The named episodes are *small*: the sources name an episode in a few dozen entries and then record its days without naming it.\n')
st=json.load(open('episode_stats.json'))
P('| candidate | window | all | win | first..last | CL | CR | density (per month in window) |\n|---|---|---:|---:|---|---:|---:|---|')
win={s:(lo,hi) for s,n,lo,hi,rx in EP}
for s,n,a,w,f,l,cl,cr,by in st:
    lo,hi=win[s]; P(f'| {n} (`{s}`) | {lo}..{hi} | {a} | {w} | {f}..{l} | {cl:.0%} | {cr} | `{spark(by,lo,hi)}` |')
P('\nNotes. `all` far above `win` (Yi–Ta, polemic, February Countercurrent, Red Guards, Luo Ruiqing) means the words recur outside the episode: names of people and places (Ye Jianying, Li Fuchun, Wuhan, Xinjiang) are poor episode keys outside a tight window. Beidaihe and Lushan are places as much as meetings: in July–August every leader\'s daybook is at Beidaihe, so the window takes his swims with the conference. Soviet experts, Ninth Plenum, Investigation, Xilou, Peng\'s letter, Philosophy, Successors, Mao\'s 1967 tour, Liu\'s death, Yang–Yu–Fu, Panchen, Yi–Ta fall under 40 on their own; they are folded into neighbors in the trial scheme.\n')
# persons
pc=json.load(open('person_counts.json')); px=json.load(open('person_extra.json'))
P('## 3. Persons as actors\n')
P('Actor = the person heads `c` after a place/time prefix is stripped ("Peking 北京, Zhongnanhai. ...", "At ..., ", "Evening, ") and the characters and parentheticals removed: "Mao, on ...", "Mao to ...", "Mao\'s comment", "Zhou receives". `sole` = alone at the head; `joint` = one of a list at the head ("Mao, Liu Shaoqi and Zhu De receive ..."); `named` = named elsewhere in `c` or tagged `name:` only. `1st src` = entries read from that person\'s own nianpu/diary. All China threads (28,423).\n')
P('| person | sole actor | joint actor | named only | 1st src (own nianpu) |\n|---|---:|---:|---:|---:|')
order=['mao','zhou','chenyi','yang','zhu','pengzhen','deng','liu','chenyun','pengdh','ye','lin','kang','jiangqing','boda','lfc','lxn','tao','luo','tian','zcq','xie','wl']
names={'mao':'Mao Zedong','zhou':'Zhou Enlai','chenyi':'Chen Yi','yang':'Yang Shangkun','zhu':'Zhu De','pengzhen':'Peng Zhen','deng':'Deng Xiaoping','liu':'Liu Shaoqi','chenyun':'Chen Yun','pengdh':'Peng Dehuai','ye':'Ye Jianying','lin':'Lin Biao','kang':'Kang Sheng','jiangqing':'Jiang Qing','boda':'Chen Boda','lfc':'Li Fuchun','lxn':'Li Xiannian','tao':'Tao Zhu','luo':'Luo Ruiqing','tian':'Tian Jiaying','zcq':'Zhang Chunqiao','xie':'Xie Fuzhi','wl':'Wang Li'}
src1={'mao':2480,'zhou':5722,'chenyi':2406,'yang':4684,'zhu':1359,'pengzhen':1304,'deng':945,'liu':575,'chenyun':420,'pengdh':466,'ye':313,'lin':232}
for k in order:
    v=pc.get(k,{}); P(f"| {names[k]} | {v.get('sole',0)} | {v.get('joint',0)} | {v.get('named',0)} | {src1.get(k,'—')} |")
P('\nThe Cultural Revolution Group (Kang Sheng, Jiang Qing, Chen Boda, Zhang Chunqiao, Wang Li) are actors in under 130 entries each: they are named, not followed; no source of theirs has been read. Yang Shangkun is the keeper of the largest single source but heads only a third of its entries: his diary\'s form is "X with Yang Shangkun".\n')
P('**Mao\'s own acts by year** (sole + joint at the head; china-leadership and china):\n')
P('| year | sole | joint | named only |\n|---|---:|---:|---:|')
for y,v in sorted(px['mao_year'].items()): P(f"| {y} | {v.get('sole',0)} | {v.get('joint',0)} | {v.get('named',0)} |")
P('\nTotal: 2,155 sole + 177 joint = 2,332 of his acts; 2,573 entries name him without his acting. In the best scheme below, 1,019 of his acts (china-leadership only) fall inside an episode and 1,302 go to the Mao thread; by year, episode/Mao thread: 1960 98/238, 1961 65/142, 1962 89/129, 1963 86/133, 1964 146/146, 1965 44/160, 1966 149/106, 1967 194/90, 1968 81/80, 1969 67/76.\n')
P('Samples of the actor test (first 8 of each class, 1960): \n')
for k in ('mao:sole','mao:joint','mao:named'):
    P(f'*{k}*\n'); [P(f'- {s}') for s in px['samples'].get(k,[])[:6]]; P('')
# schemes
P('## 4. Trial partitions\n')
P('Assignment order: an episode (keyword in its window; for the Cultural Revolution stages also the date window plus a general CR vocabulary; source rules: an entry read from Yang Jisheng\'s *Mubei* or Dikötter\'s famine book, 1959-10..1962-12, goes to Famine; from Wu Lengxi\'s polemic memoir to the polemic thread of its date; from *Tiandi fanfu*, Pu Weihua, MacFarquhar–Schoenhals or Dikötter\'s CR book to the CR stage of its date); then Mao\'s act; then a foreign country matching an *existing* thread (Africa, Soviet Union, South Asia, Hanoi, Japan, Korea, Indonesia, Europe, Middle East, Laos, Cuba, Latin America); then the other persons (their act, or read from their nianpu/diary); then places. "Clean" = one candidate at the deciding level; "ambiguous" = two or more (resolved in the counts by the shorter span); "residual" = none.\n')
P('| scheme | clean | ambiguous | residual | threads | under 40 | over 3,000 |\n|---|---:|---:|---:|---:|---|---|')
R1=pickle.load(open('runs.pkl','rb')); R2=pickle.load(open('runs2.pkl','rb'))
for r in R1+R2:
    sm=[k for k,v in r['sizes'].items() if v<40 and k!='(residual)']; bg=[k for k,v in r['sizes'].items() if v>3000 and k!='(residual)']
    P(f"| {r['label']} | {r['clean']:.1%} | {r['amb']:.1%} | {r['res']:.1%} | {len([k for k in r['sizes'] if k!='(residual)'])} | {', '.join(sm) or '—'} | {', '.join(bg) or '—'} |")
P('\nReading the table. Episodes alone (A–A2, G1–G2) take a third of the bucket at most, however generous the windows. Mao adds about 5 points. The country threads and Liu and Zhou add 25. The remaining third is the other daybooks, above all Yang Shangkun\'s diary (G4 residual by first source: Yang diary 3,239; Zhu De 1,093; Chen Yi 903; Peng Zhen 695; Deng 447; Peng Dehuai 323; Chen Yun 320; MacFarquhar *Origins* 255; Ye Jianying 205). Only person threads for the daybook keepers bring the residual under 5 percent (G6).\n')
P('Sizes in G3 (episodes + Mao): '+', '.join(f'{k} {v}' for k,v in R2[2]['sizes'].most_common())+'.\n')
P('Most frequent ambiguities (G6): '+'; '.join(f"{' / '.join(k)} {v}" for k,v in R2[5]['ambex'].most_common(12))+'. Of 1,219 ambiguous entries in G6, 635 are between two countries, 363 between two keyword episodes, 221 between two stages by source rule; 290 are year-dated entries that no stage window can place.\n')
# places
P('## 5. Places within China\n')
P('Place = the `place:` field (on 14,055 of the 26,320; Peking alone 7,533) or the province/city and its chief people named in `c` with characters. "Held by" = where the entry would go before any place thread is consulted (episode; CR stage by date; Mao; an existing country thread; Liu or Zhou; another daybook keeper); "free" = what a place thread could claim without double-cutting.\n')
P('| place | entries | by `place:` | span | peak years | episode | stage | Mao | country | Liu/Zhou | other daybook | free | chief episodes |\n|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|')
for s,n,tot,byf,f,l,yrs,cl,eps in json.load(open('places.json')):
    P(f"| {n} | {tot} | {byf} | {f[:7]}..{l[:7]} | {', '.join(f'{a} {b}' for a,b in yrs)} | {cl.get('episode',0)} | {cl.get('stage (date+CR words)',0)} | {cl.get('Mao',0)} | {cl.get('country thread',0)} | {cl.get('Liu/Zhou',0)} | {cl.get('other daybook',0)} | {cl.get('free',0)} | {', '.join(f'{a} {b}' for a,b in eps)} |")
P('''
Findings.
- **Niujiao** (271, Oct. 1964–Dec. 1965) is Yang Shangkun's Four Cleanups squat point: the Niujiao brigade, Chang'an county, outside Xi'an, where he lived with a work team; every entry is from his diary. All 271 fall to Four Cleanups (a Niujiao rule is in the episode). **Xi'an 1965** (231) is the same stay: Yang posted to the Northwest Bureau, his diary at Xi'an; 70 already Four Cleanups, 145 free, 111 his daybook. Not a place thread: an episode within Four Cleanups, or Yang's thread.
- **Beidaihe** (496) and **Lushan** (159) are the leaders' summer seats: 324 and 130 fall to the conferences held there (1960, 1962; 1961); the rest is leave (swims, doctors). No place thread.
- **Hangzhou** (512) is Mao's base and the leaders' winter stop; its entries are Mao's and the daybooks'. 66 free. No place thread.
- **Wuhan 1967** (151 of 426) and **Dao county** (34 of 39, Aug.–Oct. 1967) are wholly the Wuhan-and-the-army stage; **Nanning 1968** (40) and **Guangxi** (92 in 1968) are the revolutionary-committees stage (the Guangxi killings, the July 3 notice); **Chongqing 1967** (60) splits between the 1967 and 1968 stages. Ruled out: the episodes hold them.
- **Peking the city** (971; peak 446 in 1966): 494 already episodes (May Sixteenth 175, Red Guards 112, Hai Rui 73), 67 stage, 170 free (the municipal committee's rectification reports of 1961, Deng Tuo's columns, the 1964 campus critiques). The 1966 purge of the municipal committee is the May Sixteenth stage. A Peking thread would hold about 170, thinly spread over ten years: ruled out; the 1961–65 municipal and literary matter belongs to Hai Rui (Deng Tuo, Wu Han) once its window is opened back to 1961.
- **Shanghai** (1,024): 316 episodes (seizures of power 65, 1960 conference 54), 227 daybooks, 106 country (receptions), 167 free (Ke Qingshi's cultural forums, 1967 street violence, statistics). **Sichuan** (722): 198 episodes, 217 daybooks, 177 free (famine statistics, Li Jingquan, 1966–67 local violence). **Guangdong** (615), **Hebei** (597), **Shaanxi** (751), **Hunan** (395), **Yunnan** (350): the same shape, 60–180 free each.
- The famine provinces (**Henan** 317, **Anhui** 225, **Gansu** 218, **Shandong** 258) peak in 1960–61, and their free entries are mostly famine reports the keyword rule missed; they belong in Famine, not in provinces.
- **Inner Mongolia** (158), **Tibet** (116), **Xinjiang** (151) are small and scattered (under 50 free each).

Ruling. No place thread survives the rule "not where an episode already holds its entries": in every place, the episodes and the daybooks take most, and what is left is under 200 entries over ten years, with no event of its own. Scheme G5 (places after persons Liu and Zhou) gives Shanghai 316, Sichuan 266, Shaanxi 264, Guangdong 244, Peking 223, Hebei 174; G7 (places after all the daybooks) leaves every place under 40. A place thread works only as a sorting bin for the famine and CR local reports, and for those the famine and stage threads are the better home.
''')
# best
sizes=json.load(open('best_sizes.json'))
P('## 6. The best scheme (G6, with conference day-windows; Yang split)\n')
P('Coverage of the 26,320: clean 92.6%, ambiguous 4.6% (resolved by the narrower window, or the first country), residual 2.8% (740). Of the 26,320: episodes 10,386 (39%), country threads (existing) 4,661 (18%), Mao 1,490 (6%), other persons 9,043 (34%).\n')
EPN=[('china-shanghai-1960','Shanghai and Beidaihe, 1960','The year\'s targets set at Shanghai; the experts withdrawn and the summer conference at Beidaihe.','{{1960-01-07..1960-01-17|The enlarged Politburo at Shanghai.}} {{1960-07-05..1960-08-10|Beidaihe; the Soviet experts recalled.}}'),
('china-moscow-1960','Bucharest and Moscow','The quarrel with Moscow carried into the parties\' meetings, from "Long Live Leninism!" to the Moscow Statement.','{{1960-04-16|"Long Live Leninism!"}} {{1960-06-24..1960-06-26|Peng Zhen at Bucharest.}} {{1960-11-10..1960-12-01|The eighty-one parties at Moscow; Liu Shaoqi with Khrushchev.}}'),
('china-twelve-articles','Twelve Articles','The communes\' "communist wind" checked: the emergency letter and the Ninth Plenum.','{{1960-11-03|The Emergency Directive Letter, the "Twelve Articles."}} {{1960-11-15|Mao\'s directive on the "five winds."}} {{1961-01-14..1961-01-18|The Ninth Plenum.}}'),
('china-famine','Famine','The famine as the provinces reported it, the grain moved and bought abroad, the deaths counted.','{{1960-06-03|The Taolin report on the deaths.}} {{1960-10-03|Chen Yun on Hebei and Shandong.}} {{1961-01-03|Henan\'s relief directive.}}'),
('china-sixty-articles','Sixty Articles','The year of investigation: the communes\' regulations drafted at Canton, revised at Peking, and the industrial articles at Lushan.','{{1961-03-10..1961-03-23|The Canton conference; the Sixty Articles.}} {{1961-04-02..1961-05-15|Liu Shaoqi in Hunan.}} {{1961-08-23..1961-09-16|Lushan; the Seventy Articles.}}'),
('china-seven-thousand','Seven Thousand Cadres','The enlarged work conference of January 1962: Liu\'s report, Mao\'s self-criticism, Lin Biao\'s defense of the Leap.','{{1962-01-11|The conference opens.}} {{1962-01-27|Liu Shaoqi\'s report.}} {{1962-01-30|Mao\'s speech.}}'),
('china-retreat-1962','Xilou and the retreat','Chen Yun\'s deficit and emergency program, the cities emptied, the household contracts.','{{1962-02-21..1962-02-23|The Xilou meeting.}} {{1962-05-07..1962-05-11|The May work conference; the streamlining.}} {{1962-07-06..1962-07-23|Mao against household contracting.}}'),
('china-tenth-plenum','Beidaihe and the Tenth Plenum','"Never forget class struggle": the Beidaihe conference, the plenum, Peng Dehuai\'s case reopened.','{{1962-08-06..1962-08-24|Beidaihe.}} {{1962-08-26|The plenum\'s preparatory meeting.}} {{1962-09-24..1962-09-27|The Tenth Plenum.}}'),
('china-india-war','India war','The border war with India and the cease-fire.','{{1962-07-22|Mao on the Galwan post.}} {{1962-11-21|The cease-fire declared.}} {{1963-01-05|Zhou and Bandaranaike.}}'),
('china-polemic','Polemic','The open polemic with Moscow, from the Twenty-second Congress to Zhou in Moscow after Khrushchev\'s fall.','{{1961-10-17..1961-10-23|Zhou at the Twenty-second Congress.}} {{1963-06-14..1963-07-20|The general line; Deng and Suslov.}} {{1964-11-05..1964-11-14|Zhou in Moscow.}}'),
('china-four-cleanups','Four Cleanups','The socialist education movement: the Ten Points, the work teams, Taoyuan, Niujiao, the Twenty-three Articles.','{{1963-05-02..1963-05-12|The Hangzhou conference; the First Ten Points.}} {{1964-10-28..1965-12|Yang Shangkun at Niujiao.}} {{1964-12-15..1965-01-14|The work conference; the Twenty-three Articles.}}'),
('china-models','Lei Feng, Dazhai, Daqing','The emulation campaigns: Lei Feng, the Dazhai brigade, the Daqing oilfield, the army\'s political work.','{{1963-03-05..1963-03-06|"Learn from Comrade Lei Feng."}} {{1964-01-02|The General Office on Daqing.}} {{1964-12|Dazhai in the Government Work Report.}}'),
('china-opera','Opera reform','The arts rectified: Mao\'s two instructions, the festival of modern Peking opera, the ministry purged.','{{1963-12-12|Mao\'s first instruction.}} {{1964-06-05..1964-07-31|The festival of modern Peking opera.}} {{1965-04|The Ministry of Culture reorganized.}}'),
('china-africa-tour','Zhou in Africa','Zhou Enlai\'s and Chen Yi\'s tour of ten African countries and Albania, the eight principles of aid.','{{1963-12-14|To Cairo.}} {{1963-12-21..1963-12-27|Algeria.}} {{1964-01-15|Accra; the eight principles.}}'),
('china-third-front','Third Front','The interior industrial base: the Third Plan recast for war, Panzhihua and the southwest railways.','{{1964-05-15..1964-06-17|The work conference; the third front.}} {{1965-03-29|Zhu De at Chengdu.}} {{1965-11-13|The plan conference.}}'),
('china-afro-asian','Afro-Asian conference','The second Asian–African conference sought and lost at Algiers.','{{1965-03-30..1965-04-01|Zhou at Algiers.}} {{1965-06-19..1965-06-28|Ben Bella deposed; the conference put off.}} {{1965-11-04|China\'s withdrawal.}}'),
('china-bomb','Bomb','The atomic and hydrogen bombs and the missiles: their decisions and tests.','{{1963-07-28|The test ban discussed.}} {{1964-10-16|The first test; the statement.}} {{1966-10-27|The missile with a warhead.}} {{1967-06-17|The hydrogen bomb.}}'),
('china-hai-rui','Hai Rui','Yao Wenyuan\'s article, the Peking committee\'s defense of Wu Han, the February Outline.','{{1965-11-10|Yao Wenyuan\'s article.}} {{1965-11-29|The *Beijing Daily* reprints it.}} {{1966-02-12|The February Outline circulated.}}'),
('china-luo-ruiqing','Luo Ruiqing','The Chief of Staff accused by Lin Biao and removed at the Shanghai conference.','{{1965-11-27|Luo with Lin Biao.}} {{1965-12-08..1965-12-15|The Shanghai conference.}} {{1966-03-04..1966-04-08|The struggle meetings.}}'),
('china-may-sixteenth','May Sixteenth and the work teams','The enlarged Politburo and its Circular, Peng Zhen\'s fall, Nie Yuanzi\'s poster, the fifty days of the work teams.','{{1966-05-16|The May 16 Circular.}} {{1966-05-25|Nie Yuanzi\'s poster.}} {{1966-07-16|Mao in the Yangtze.}} {{1966-07-28|The work teams withdrawn.}}'),
('china-red-guards','Red Guards','The Eleventh Plenum and the Red Guards: the rallies, the "four olds," the house searches, the attack on the "reactionary line."','{{1966-08-01..1966-08-12|The Eleventh Plenum; "Bombard the Headquarters."}} {{1966-08-18|The first rally.}} {{1966-10-09..1966-10-28|The October work conference.}}'),
('china-seizures','Seizures of power','The January Storm at Shanghai, the seizures in the provinces, the army sent in, the February Countercurrent.','{{1967-01-06|The rebels take Shanghai.}} {{1967-01-23|The army to support the left.}} {{1967-02-16|The Huairen Hall.}}'),
('china-wuhan','Wuhan and the army','The army\'s factions and the armed struggle: Wuhan, the drive against "the handful in the army," the fall of Wang Li and Guan Feng.','{{1967-07-20|The Million Heroes take Wang Li.}} {{1967-08-22|The British office burned.}} {{1967-08-30|Wang Li and Guan Feng detained.}}'),
('china-class-ranks','Revolutionary committees','The revolutionary committees completed and the class ranks cleansed: Yang Chengwu\'s fall, the July notices, the propaganda teams.','{{1968-03-24|Yang Chengwu, Yu Lijin and Fu Chongbi dismissed.}} {{1968-07-28|Mao with the five Red Guard leaders.}} {{1968-09-05|The last committees, Tibet and Xinjiang.}}'),
('china-ninth-congress','Ninth Congress','Liu Shaoqi expelled at the Twelfth Plenum; the Ninth Congress and Lin Biao as successor.','{{1968-10-13..1968-10-31|The Twelfth Plenum.}} {{1969-04-01..1969-04-24|The Ninth Congress.}} {{1969-04-28|Lin Biao\'s report printed.}}'),
('china-border-war','Border war','The clashes on the Ussuri and in Xinjiang, the war scare, the airport talks and the border talks.','{{1969-03-02|Zhenbao.}} {{1969-09-11|Kosygin at the Peking airport.}} {{1969-10-17..1969-10-20|Order No. 1; the border talks.}}'),
]
PER=[('china-mao','Mao','mao','1960–69','Mao Zedong\'s own acts outside the episodes: his comments and instructions, letters, talks, audiences, poems, swims, travels.','{{1960-10-27|Edgar Snow.}} {{1961-09-24|Montgomery at Wuchang; the Yangtze.}} {{1965-05|Jinggangshan revisited.}} {{1965-11|South, for eight months.}}'),
('china-zhou','Zhou Enlai','zhou','1960–69','The Premier\'s day outside the episodes: the State Council, the plan, the guests and the countries without a thread (Burma, Cambodia, the bloc).','{{1963-02-16|Sihanouk at the Great Wall.}} {{1964-12-21|"Four modernizations."}} {{1965-08-23|The long-term plan.}}'),
('china-liu','Liu Shaoqi','liu','1960–68','The head of state to his fall: his inspections, receptions and visits abroad.','{{1961-04-02..1961-05-15|Hunan.}} {{1963-04-12..1963-05-16|Indonesia, Burma, Cambodia, Vietnam.}} {{1967-01-13|Mao and Liu at the Great Hall.}}'),
('china-zhu','Zhu De','zhu','1960–69','The NPC chairman\'s inspections, receptions and poems.','{{1960-02-01|Conghua.}} {{1963-04-20|Mount Emei.}} {{1964-08-05|Hulunbuir.}}'),
('china-chen-yi','Chen Yi','chenyi','1960–68','The Foreign Minister\'s receptions, travels and poems, and his fall.','{{1961-05-16|Sihanouk at Geneva.}} {{1964-12|"Journey to six countries."}} {{1967-08-11|Criticized at the Great Hall.}}'),
('china-yang','Yang Shangkun','yang','1960–65','The General Office\'s director: his diary of the Center\'s business, to his removal (split at 1963: 1,403 and 1,709).','{{1960-03-07|With Mao after the Soviet Ambassador.}} {{1964-10-30|Into Niujiao.}} {{1965-11-30|His last day at the Office.}}'),
('china-peng-zhen','Peng Zhen','pengzhen','1960–66','The Secretariat and the Peking committee, to his fall.','{{1963-12-29|The People\'s Council on the arts.}} {{1964-09-03|The fifth Peking People\'s Congress.}} {{1966-03-29|His last NPC session.}}'),
('china-deng','Deng Xiaoping','deng','1960–66','The General Secretary\'s Secretariat.','{{1961-04|The Peking communes investigated.}} {{1964-04-27|*Reeds and Sparks*.}}'),
('china-chen-yun','Chen Yun','chenyun','1960–69','The planner\'s investigations and programs.','{{1961-07|Qingpu.}} {{1962-02-26|The State Council on the deficit.}}'),
('china-peng-dehuai','Peng Dehuai','pengdh','1961–69','The fallen marshal: his letters, the Third Front at Chengdu, the struggle meetings.','{{1962-06|The letter of eighty thousand characters.}} {{1965-12-30|To Chengdu.}} {{1967-09-13|Struggled at the Political School.}}'),
('china-ye','Ye Jianying','ye','1960–69','The marshal\'s military training and inspections.',''),
('china-lin','Lin Biao','lin','1960–69','The Defense Minister and successor.',''),
]
P('### Episode threads (parent `china`)\n')
P('| thread (slug) | name | span | entries | statement |\n|---|---|---|---:|---|')
for s,n,stm,stns in EPN:
    lo,hi=[(lo,hi) for x,nn,lo,hi,c,w in __import__('scheme').EPISODES if x==s][0]
    P(f'| `{s}` | {n} | {lo}..{hi} | {sizes.get(s,0)} | {stm} {stns} |')
P('\n### Person threads (parent `china`)\n')
P('| thread (slug) | name | span | entries | statement |\n|---|---|---|---:|---|')
for s,n,k,sp,stm,stns in PER:
    cnt=sizes.get(k,0) if k!='yang' else sizes.get('yang-1960-62',0)+sizes.get('yang-1963-65',0)
    P(f'| `{s}` | {n} | {sp} | {cnt} | {stm} {stns} |')
P('\n### To existing country threads (thread: the country, `also: [china]`)\n')
P('| thread | entries |\n|---|---:|')
for k in ('africa','soviet-union','south-asia','vietnam-hanoi','japan','korea','indonesia','europe-and-the-alliance','middle-east','laos','cuba','latin-america'):
    P(f'| `{k}` | {sizes.get(k,0)} |')
P('\nStations: dates and events are taken from entries in each thread (`stations.py` output, below); a few (marked by their form "{{1964-12|...}}") are from general knowledge and should be checked against the entries before use. The person statements are drafts.\n')
# residual
P('## 7. The residual (best scheme): 30 openings by year\n')
A,res=pickle.load(open('best.pkl','rb'))
by=collections.defaultdict(list)
for i in res: by[ED[i]['date'][:4]].append(ED[i])
P('Residual by year: '+', '.join(f'{y} {len(v)}' for y,v in sorted(by.items()))+'. By first source: '+', '.join(f'`{w}` {n}' for w,n in collections.Counter(ED[i]['works'][0] if ED[i]['works'] else '-' for i in res).most_common(8))+'.\n')
random.seed(11)
for y in sorted(by):
    for e in random.sample(by[y],min(3,len(by[y]))): P(f"- {e['date']} — {e['c'][:160]}")
P('\nWhat it is: the Center\'s and the State Council\'s documents on ordinary business (finance and trade, the nationalities, the plan), the scholarship\'s undated or year-dated generalizations (MacFarquhar\'s *Origins*, Dikötter), the case groups of the fallen (Peng Zhen questioned, 1967–68; his own thread ends at his fall), and people outside every thread (He Long, Li Zongren, Sun Weishi, Huang Kecheng).\n')
P(open('boundaries.md').read())
P('\n## 9. Scripts\n')
for f,d in [('extract.py','regex extraction of every entry touching the China threads → china.jsonl, allthreads.json'),('phrases.py','frequency of capitalized phrases, quoted slogans, numbered formulas, 《》 titles → phrases.json'),('lexicon.py','episode candidates: regex and window'),('stats.py','candidate counts, windows, densities → episode_stats.json'),('persons.py','actor/named counts → person_counts.json, person_extra.json, actors.json'),('scheme.py','trial episode threads, country, person and place lexicons'),('assign.py','schemes A–F → runs.pkl, cl.pkl'),('assign2.py','schemes G1–G8 (source rules, daybooks) → runs2.pkl'),('places.py','place clusters → places.json'),('final.py','best scheme (G6 + conference day-windows) → best.pkl, best_sizes.json'),('report.py','this file')]:
    P(f'- `{f}`: {d}')
open('china-threads-survey.md','w').write('\n'.join(OUT))
print(len(OUT))
