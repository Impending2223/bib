# Final candidate threads (episodes), places, countries, persons, for assign.py
from lexicon import EP
C={s:(lo,hi,rx) for s,n,lo,hi,rx in EP}
def comp(*slugs, lo=None, hi=None, extra=None):
    out=[]
    for s in slugs:
        a,b,rx=C[s]; out.append((max(a,lo) if lo else a, min(b,hi) if hi else b, rx))
    if extra: out+=extra
    return out
CRW=(r"Cultural Revolution|文化大革命|文革|rebels?\b|造反|Red Guards?|红卫兵|revolutionary masses|革命群众|struggle (?:sessions?|meetings?)|批斗|seiz\w+ power|夺权|factions?\b|派性|big-character|大字报|capitalist[- ]roaders?|走资|power[- ]holders?|当权派|by name|点名|denounc\w+|揪|dragged? out|black gang|黑帮|ox[- ]ghosts|牛鬼蛇神|counter-?revolutionar\w+|反革命|liaison stations?|联络站|Cultural Revolution Group|中央文革|revolutionary committees?|革委会|革命委员会|criticism and repudiation|大批判|mass organizations?|群众组织|headquarters|司令部|PLACE:")  # weak lexicon, stages only (PLACE: never matches; placeholder)
EPISODES=[ # slug, name, span lo, hi, strong components [(lo,hi,rx)], weak rx or None
 ('china-shanghai-1960','Shanghai and Beidaihe, 1960','1960-01','1960-08', comp('leap-1960','beidaihe-1960','soviet-experts', extra=[('1960-01','1960-01',r"enlarged Politburo|政治局扩大会议|PLACE:shanghai")]), None),
 ('china-twelve-articles','Twelve Articles','1960-09','1961-01', comp('rectify-communes','ninth-plenum',lo='1960-09',hi='1961-01'), None),
 ('china-famine','Famine','1959-10','1962-12', comp('famine','grain'), None),
 ('china-sixty-articles','Sixty Articles','1961-01','1961-09', comp('investigation-1961','sixty-articles','lushan-1961','articles-1961',hi='1961-09'), None),
 ('china-seven-thousand','Seven Thousand Cadres','1961-11','1962-02', comp('seven-thousand'), None),
 ('china-retreat-1962','Xilou and the retreat','1962-02','1962-07', comp('xilou','retrenchment','household-contracting','verdicts-reversed',lo='1962-02',hi='1962-07'), None),
 ('china-tenth-plenum','Beidaihe and the Tenth Plenum','1962-07','1962-10', comp('beidaihe-1962','tenth-plenum','peng-letter-1962','household-contracting',lo='1962-07',hi='1962-10'), None),
 ('china-moscow-1960','Bucharest and Moscow','1960-04','1961-01', comp('polemic',lo='1960-04',hi='1961-01'), None),
 ('china-polemic','Polemic','1961-10','1964-11', comp('polemic',lo='1961-10',hi='1964-11'), None),
 ('china-india-war','India war','1962-06','1963-03', comp('sino-indian-war'), None),
 ('china-africa-tour','Zhou in Africa','1963-12','1964-03', comp('african-tour'), None),
 ('china-afro-asian','Second Bandung','1964-04','1965-11', comp('afro-asian-1965'), None),
 ('china-bomb','Bomb','1963-07','1969-12', comp('nuclear'), None),
 ('china-four-cleanups','Four Cleanups','1962-09','1966-05', comp('socialist-education',hi='1966-05', extra=[('1964-10','1965-12',r"PLACE:niujiao|Niujiao|牛角|Chang'an county|长安县")]), None),
 ('china-models','Lei Feng, Dazhai, Daqing','1963-01','1965-12', comp('emulation'), None),
 ('china-third-front','Third Front','1964-04','1966-05', comp('third-front',hi='1966-05'), None),
 ('china-opera','Opera reform','1963-09','1965-12', comp('arts-rectification','philosophy-1964',hi='1965-12'), None),
 ('china-luo-ruiqing','Luo Ruiqing','1965-11','1966-05', comp('luo-ruiqing'), None),
 ('china-hai-rui','Hai Rui','1965-09','1966-04', comp('hai-rui',hi='1966-04'), None),
 # owner's Cultural Revolution stages
 ('china-may-sixteenth','May Sixteenth and the work teams','1966-04','1966-07', comp('may-16-circular','work-teams','hai-rui',lo='1966-04',hi='1966-07'), ('1966-05','1966-07')),
 ('china-red-guards','Red Guards','1966-08','1966-12', comp('eleventh-plenum','red-guards','reactionary-line',lo='1966-08',hi='1966-12'), ('1966-08','1966-12')),
 ('china-seizures','January Storm and the seizures of power','1967-01','1967-04', comp('january-storm','february-countercurrent','red-guards','army-support-left',lo='1967-01',hi='1967-04'), ('1967-01','1967-04')),
 ('china-wuhan','Wuhan and the army','1967-05','1967-12', comp('wuhan','army-support-left','wang-guan-qi','foreign-ministry-1967','factions-1967','mao-tour-1967',lo='1967-05',hi='1967-12', extra=[('1967-08','1967-10',r"PLACE:daoxian|Dao county|道县")]), ('1967-05','1967-12')),
 ('china-class-ranks','Revolutionary committees and the class ranks','1968-01','1968-09', comp('revolutionary-committees','class-ranks','yang-yu-fu','tsinghua-1968','factions-1967','army-support-left',lo='1968-01',hi='1968-09'), ('1968-01','1968-09')),
 ('china-ninth-congress','Ninth Congress','1968-10','1969-04', comp('twelfth-plenum','ninth-congress','class-ranks','revolutionary-committees',lo='1968-10',hi='1969-04'), ('1968-10','1969-04')),
 ('china-border-war','Border war','1969-03','1969-12', comp('zhenbao'), None),
]
# existing country threads, for foreign matter (thread: X, also: china)
COUNTRIES=[
 ('soviet-union', r"Soviet|USSR|苏联|苏共|CPSU|Moscow|莫斯科|Khrushchev|赫鲁晓夫|Kosygin|Brezhnev|Mikoyan|Chervonenko|契尔沃年科|Suslov|Kozlov|Voroshilov|Gromyko"),
 ('vietnam-hanoi', r"Vietnam|越南|DRV|Hồ Chí Minh|胡志明|Phạm Văn Đồng|Lê Duẩn|Võ Nguyên Giáp|Trường Chinh|Hanoi|河内|NLF|Nguyễn|Lê Đức|Hoàng Văn"),
 ('laos', r"Laos|老挝|Lao\b|Souvanna|Souphanouvong|Quinim|Phoumi|Pathet"),
 ('korea', r"Korea|朝鲜|DPRK|Kim Il|金日成|Pyongyang|平壤|Choe Yong"),
 ('japan', r"Japan|日本|Tokyo|东京|Miyamoto|宫本|Matsumura|松村|Takasaki|高碕|Kenzō|Okazaki|JCP|JSP|Sōhyō"),
 ('indonesia', r"Indonesia|印尼|印度尼西亚|Sukarno|苏加诺|Subandrio|Aidit|PKI|Jakarta|雅加达"),
 ('south-asia', r"India\b|Indian|印度(?!尼)|Nehru|Pakistan|巴基斯坦|Ayub|Bhutto|Ceylon|锡兰|Bandaranaike|Nepal|尼泊尔|Mahendra|Afghan|阿富汗|Karachi|Rawalpindi|Kathmandu|Katmandu|New Delhi"),
 ('africa', r"Africa|非洲|Ghana|加纳|Guinea|几内亚|Mali\b|马里|Algeri|阿尔及利亚|Tanzania|Tanganyika|Zanzibar|坦桑|Congo|刚果|Somali|索马里|Sudan|苏丹|Ethiopia|埃塞俄比亚|Morocc|摩洛哥|Tunisia|突尼斯|Kenya|肯尼亚|Uganda|乌干达|Zambia|赞比亚|Nkrumah|Nyerere|Touré|Keïta|Modibo|Ben Bella|Boumediene|Mauritania|Senegal|Cameroon|Burundi|Nigeria|Rhodesia|Kaunda|Brazzaville|Accra|Conakry|Bamako|Dar es Salaam"),
 ('middle-east', r"\bUAR\b|Egypt|埃及|Nasser|纳赛尔|Cairo|开罗|Syria|叙利亚|Iraq|伊拉克|Yemen|也门|Palestin|巴勒斯坦|Iran\b|伊朗|Lebanon|Kuwait|Jordan|Israel"),
 ('cuba', r"Cuba|古巴|Castro|卡斯特罗|Guevara|格瓦拉|Havana"),
 ('latin-america', r"Brazil|巴西|Chile|智利|Mexic|墨西哥|Argentin|阿根廷|Venezuel|Peru\b|秘鲁|Bolivia|Uruguay|Colombia\b|Ecuador|Latin America|拉丁美洲|拉美"),
 ('europe-and-the-alliance', r"France|French|法国|de Gaulle|戴高乐|Britain|British|英国|London|伦敦|Ital(?:y|ian)|意大利|Sweden|Swedish|瑞典|Switzerland|Swiss|瑞士|Norw|挪威|Denmark|Danish|丹麦|Netherlands|Dutch|荷兰|Finland|芬兰|Austria|奥地利|Belgi|比利时|Federal Republic|West German|联邦德国|Montgomery|Snow\b|斯诺"),
 # no thread yet: the bloc in Europe, Southeast Asia's neutrals, Mongolia
 ('(no thread) bloc-europe', r"Albania|阿尔巴尼亚|Hoxha|Shehu|Tirana|Romania|罗马尼亚|Bucharest|Ceaușescu|Gheorghiu|Maurer|Poland|Polish|波兰|Czech|捷克|Hungar|匈牙利|Kádár|Bulgaria|保加利亚|GDR|East German|民主德国|Ulbricht|Yugoslav|南斯拉夫|Tito"),
 ('(no thread) burma-cambodia-neutrals', r"Burm|缅甸|Ne Win|奈温|U Nu|Rangoon|仰光|Cambodia|柬埔寨|Sihanouk|西哈努克|Phnom Penh|金边|Ceylon"),
 ('(no thread) mongolia', r"Mongolian People's Republic|Mongolia(?!n People's Party)\b|蒙古人民共和国|Tsedenbal|泽登巴尔|Ulan Bator|乌兰巴托"),
]
PERSONS=[('mao','Mao','1960-01','1969-12'),('liu','Liu Shaoqi','1960-01','1968-10'),('zhou','Zhou Enlai','1960-01','1969-12'),
         ('chenyi','Chen Yi','1960-01','1968-12'),('zhu','Zhu De','1960-01','1969-12'),('yang','Yang Shangkun','1960-01','1965-11'),
         ('pengzhen','Peng Zhen','1960-01','1966-05'),('deng','Deng Xiaoping','1960-01','1966-10'),('pengdh','Peng Dehuai','1960-01','1969-12'),
         ('chenyun','Chen Yun','1960-01','1969-12'),('ye','Ye Jianying','1960-01','1969-12'),('lin','Lin Biao','1960-01','1969-12')]
# places: (slug, name, regex on c, place-field values)
PLACES=[
 ('peking-city','Peking (the city)', r"Peking (?:municipal|Party|city) committee|Peking Municipal|北京市委|北京市|市委书记处|Peking University|北京大学|北大|Tsinghua|清华|Peking Normal|北京师范|Beijing ribao|北京日报|Beijing wanbao|北京晚报|Frontline|《前线》|Liu Ren|刘仁|Wan Li|万里|Wu Han|吴晗|Deng Tuo|邓拓|Peking's (?:schools|students|middle schools|suburbs|factories|districts)|Peking No\.|middle school|中学|Haidian|海淀|Xicheng|西城|Dongcheng|东城|Changping|昌平|Peking's", []),
 ('shanghai','Shanghai', r"Shanghai|上海", ['shanghai']),
 ('hubei','Wuhan and Hubei', r"Wuhan|武汉|Hubei|湖北", ['wuhan']),
 ('sichuan','Sichuan', r"Sichuan|四川|Chengdu|成都|Chongqing|重庆|Li Jingquan|李井泉", ['chengdu','chongqing']),
 ('guangxi','Guangxi', r"Guangxi|广西|Nanning|南宁|Guilin|桂林|Wei Guoqing|韦国清", ['nanning','guilin']),
 ('guangdong','Guangdong', r"Guangdong|广东|Canton|广州|Conghua|从化|Zhao Ziyang|赵紫阳", ['canton','conghua','guangdong']),
 ('henan','Henan', r"Henan|河南|Xinyang|信阳|Zhengzhou|郑州|Wu Zhipu|吴芝圃", ['zhengzhou']),
 ('anhui','Anhui', r"Anhui|安徽|Hefei|合肥|Zeng Xisheng|曾希圣", ['hefei']),
 ('gansu','Gansu', r"Gansu|甘肃|甘肅|Lanzhou|兰州|Tianshui|天水|Baiyin|白银|Zhang Zhongliang|张仲良", ['lanzhou']),
 ('shandong','Shandong', r"Shandong|山东|Jinan|济南|Qingdao|青岛", ['jinan']),
 ('inner-mongolia','Inner Mongolia', r"Inner Mongolia|内蒙古|内蒙|Hohhot|呼和浩特|Ulanhu|Ulanfu|乌兰夫|Baotou|包头", ['hohhot']),
 ('tibet','Tibet', r"Tibet|西藏|Lhasa|拉萨|Panchen|班禅|Dalai|达赖", []),
 ('xinjiang','Xinjiang', r"Xinjiang|新疆|Urumqi|乌鲁木齐|\bIli\b|伊犁|Kashgar|Tacheng|塔城|Wang Enmao|王恩茂", []),
 ('hebei','Hebei', r"Hebei|河北|Baoding|保定|Shijiazhuang|石家庄|Xushui|徐水|Anguo|安国|Tianjin|天津|Xiaozhan|小站|Taoyuan|桃园|Lin Tie|林铁", ['tianjin','baoding','xushui','shijiazhuang','anguo','hebei']),
 ('shaanxi','Shaanxi', r"Shaanxi|陕西|Xi'an|西安|Niujiao|牛角|Chang'an|长安县|Yan'an|延安", ['xian','niujiao','shaanxi']),
 ('zhejiang','Hangzhou', r"Hangzhou|杭州|Zhejiang|浙江", ['hangzhou']),
 ('beidaihe','Beidaihe', r"Beidaihe|北戴河", ['beidaihe']),
 ('lushan','Lushan', r"Lushan|庐山", ['lushan']),
 ('hunan','Hunan', r"Hunan|湖南|Changsha|长沙|Daoxian|Dao county|道县|Shaoshan|韶山", ['changsha','daoxian','hunan']),
 ('yunnan','Yunnan', r"Yunnan|云南|Kunming|昆明", ['kunming','yunnan']),
]
