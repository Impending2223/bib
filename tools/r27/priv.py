import re
LEAD=r"(Mao|Liu Shaoqi|Liu|Zhou|Deng|Chen Yun|Peng Zhen|Lin Biao|Kang Sheng|Jiang Qing|Chen Boda|Zhu De|Li Fuchun|Li Xiannian|Tan Zhenlin|Bo Yibo|Yang Shangkun|Luo Ruiqing|Ye Jianying|He Long|Peng Dehuai|Tao Zhu|Wang Li|Guan Feng|Qi Benyu|Zhang Chunqiao|Yao Wenyuan|Xie Fuzhi|Chen Yi|Wang Dongxing|Ke Qingshi|Li Jingquan|Li Xuefeng|Wu Lengxi|Hu Qiaomu|Tian Jiaying|Lu Dingyi|Zhou Yang|Wang Renzhong|Liu Lantao|the Center|the Centre|the Central Committee|the Politburo|the provincial committee|Party committee)"
PRIV=re.compile(r"\bPolitburo\b|Secretariat|Standing Committee of the Politburo|Politburo Standing|\bwork conference\b|\bCentral Work Conference\b|\btalks? (with|to) "+LEAD+r"|\b(writes|letter) to "+LEAD+r"|\binstruct|\bcomments? (on|that)|批示|\bapproves\b|\breports? to "+LEAD+r"|\btelephone|\bphones\b|\bprivate(ly)?\b|\bsecret(ly)?\b|\bconfidential|\bminutes\b|\bdiary\b|\binner-Party\b|\binternal\b|Zhongnanhai|\bat (his|Mao's|Zhou's|Liu's|Lin's) (home|residence|lodging|house)|\bsummons "+LEAD+r"|\bcalls in\b|\bself-criticism\b|\bcriticizes "+LEAD+r"|\btells "+LEAD,re.I)
PUB=re.compile(r"banquet|airport|\brally\b|mass meeting|\breceives\b|ceremony|\bposter\b|broadcast|\bpublishe[sd]\b|editorial|Renmin ribao|People's Daily|\bprints\b|signs (an|the) (agreement|treaty|communiqu|joint)|communiqu|joint statement|performance|sees? off|welcom|\bNPC\b|National People's Congress|CPPCC|National Day|reviews|Tiananmen|parade|\bpress\b|news conference|\bstadium\b|struggle meeting|\bcrowd|demonstrat|\bmarch(es)?\b|\bkilling\b|\bkilled\b|\bbeaten\b|\braid|\bseize|\bstorm|airfield|reception|delegation|ambassador|chargé|embassy|consul|state visit|\bvisits?\b|\btours?\b|\binspects?\b|Xinhua|NCNA|announces|\bopens\b|\bcongress of\b|\bfuneral\b|memorial|wreath|photograph|\bcables?\b|condolence|congratulat|\bprotest|\bexpels?\b|\bplay\b|drama|\bsong|\bfilm|\bwatches\b|holiday|forum of|reporters|journalist|Red Guards? (of|from)|students of|\bschool\b|\buniversity\b",re.I)
PRESS=re.compile(r"Renmin ribao|People.s Daily|Peking Review|NCNA|Xinhua(?! shudian)|SCMP|Survey of China Mainland|New York Times|communiqu|Hongqi|Guangming ribao|Jiefangjun bao|Wenhui bao|Radio Peking|Daily Report|FBIS|Pravda|\bTASS\b",re.I)
RECORD=re.compile(r"digitalarchive\.wilsoncenter\.org|Wilson Center|history\.state\.gov|FRUS|Minutes of (the )?Conversation|Memorandum of (a )?Conversation|Record of (a )?Conversation|Transcript of|Cable from|Telegram from|AVPRF|RGANI|RGASPI|Archiv|archive",re.I)
def private_candidate(r):
    c=r['c'] or ''
    if r['mp']: return False
    if PRESS.search(r['n'] or ''): return False
    if PUB.search(c): return False
    return bool(PRIV.search(c))
def record_candidate(r):
    if r['mp']: return False
    return bool(RECORD.search(r['n'] or ''))
