import json,re,collections
E=[json.loads(l) for l in open('china.jsonl')]
E=[e for e in E if e['thread'] in ('china-leadership','china') or 'india-and-china-cultural-revolution' in e['also'] or 'china-leadership' in e['also']]
P=[ # key, full, short(surname-only form allowed), tag
('mao','Mao Zedong','Mao','name:mao-zedong'),('liu','Liu Shaoqi','Liu','name:liu-shaoqi'),('zhou','Zhou Enlai','Zhou','name:zhou-enlai'),
('deng','Deng Xiaoping',None,'name:deng-xiaoping'),('lin','Lin Biao',None,'name:lin-biao'),('chenyun','Chen Yun',None,'name:chen-yun'),
('pengzhen','Peng Zhen',None,'name:peng-zhen'),('jiangqing','Jiang Qing',None,'name:jiang-qing'),('kang','Kang Sheng',None,'name:kang-sheng'),
('boda','Chen Boda',None,'name:chen-boda'),('chenyi','Chen Yi',None,'name:chen-yi'),('zhu','Zhu De',None,'name:zhu-de'),
('yang','Yang Shangkun',None,'name:yang-shangkun'),('pengdh','Peng Dehuai',None,'name:peng-dehuai'),('ye','Ye Jianying',None,'name:ye-jianying'),
('lfc','Li Fuchun',None,'name:li-fuchun'),('lxn','Li Xiannian',None,'name:li-xiannian'),('tao','Tao Zhu',None,'name:tao-zhu'),
('luo','Luo Ruiqing',None,'name:luo-ruiqing'),('helong','He Long',None,'name:he-long'),('zcq','Zhang Chunqiao',None,'name:zhang-chunqiao'),
('xie','Xie Fuzhi',None,'name:xie-fuzhi'),('tian','Tian Jiaying',None,'name:tian-jiaying'),('hu','Hu Qiaomu',None,'name:hu-qiaomu'),
('bo','Bo Yibo',None,'name:bo-yibo'),('ldy','Lu Dingyi',None,'name:lu-dingyi'),('wgm','Wang Guangmei',None,'name:wang-guangmei'),
('nie','Nie Rongzhen',None,'name:nie-rongzhen'),('tzl','Tan Zhenlin',None,'name:tan-zhenlin'),('ywy','Yao Wenyuan',None,'name:yao-wenyuan'),
('wl','Wang Li',None,'name:wang-li'),('ke','Ke Qingshi',None,'name:ke-qingshi'),('ljq','Li Jingquan',None,'name:li-jingquan'),
('dbw','Dong Biwu',None,'name:dong-biwu'),('guo','Guo Moruo',None,'name:guo-moruo'),('liao','Liao Chengzhi',None,'name:liao-chengzhi'),
('xxq','Xu Xiangqian',None,'name:xu-xiangqian'),('wdx','Wang Dongxing',None,'name:wang-dongxing'),('wlx','Wu Lengxi',None,'name:wu-lengxi'),
]
HAN=re.compile(r'[㐀-鿿　-〿＀-￯·]+')
def clean(c):
    c=HAN.sub('',c); c=re.sub(r'\s*\([^)]*\)','',c); c=re.sub(r'\*','',c); c=re.sub(r'\s+',' ',c).strip()
    c=re.sub(r'\s+([,.;:\'])',r'\1',c)
    return c
FULLS=[p[1] for p in P]
PREP=re.compile(r"^(?:At|In|On|After|Before|From|Evening|Morning|Afternoon|Night|Noon|Late|Early|That (?:evening|night|morning|afternoon)|Later|Then|Midnight|About|Around|\d)[^,]{0,60},\s+")
def strip_prefix(c):
    for _ in range(3):
        m=re.match(r"^([^.:;]{1,60}?)\.\s+(?=[A-Z\"'])",c)
        if m and not any(f in m.group(1) for f in FULLS) and not re.search(r"\b(?:Mao|Zhou|Liu)\b",m.group(1)) and len(m.group(1).split())<=8 and not re.search(r"\b(?:receives?|meets?|talks?|writes?|says?|tells?|is|are|was|opens?|reads?)\b",m.group(1)):
            c=c[m.end():]; continue
        m=PREP.match(c)
        if m: c=c[m.end():]; continue
        break
    return c
def name_rx(full,short):
    alts=[re.escape(full)]
    if short: alts.append(re.escape(short)+r"(?! [A-Z][a-z])")
    return '(?:'+'|'.join(alts)+')'
NX={p[0]:re.compile(r"\b"+name_rx(p[1],p[2])+r"\b") for p in P}
# subject at head: optional co-actors list "A, B and C" before the verb
def head_actors(s):
    """Return list of person keys forming the subject at the head of s."""
    acts=[]; pos=0
    while True:
        hit=None
        for k,rx in NX.items():
            m=rx.match(s,pos)
            if m and (hit is None or m.end()>hit[1]): hit=(k,m.end())
        if not hit: break
        acts.append(hit[0]); pos=hit[1]
        m=re.match(r"(?:,| and|, and| with)\s+",s[pos:])  # co-actor connector
        if m:
            # only treat as co-actor if another name follows
            nxt=pos+m.end()
            if any(rx.match(s,nxt) for rx in NX.values()):
                pos=nxt; continue
        break
    return acts
res=collections.defaultdict(lambda: collections.Counter())
mao_year=collections.defaultdict(collections.Counter)
samples=collections.defaultdict(list)
for e in E:
    c=clean(e['c']); s=strip_prefix(c)
    e['_s']=s
    acts=head_actors(s)
    # possessive "Mao's comment", "Mao's letter"
    e['_actors']=acts
    for k,rx in NX.items():
        named = bool(rx.search(c)) or (dict((p[0],p[3]) for p in P)[k] in e['tags'])
        if k in acts:
            role='sole' if len(acts)==1 else 'joint'
        elif named: role='named'
        else: continue
        res[k][role]+=1
        if k=='mao': mao_year[e['date'][:4]][role]+=1
        if len(samples[(k,role)])<8 and e['thread']=='china-leadership': samples[(k,role)].append(e['date']+' | '+s[:110])
json.dump({k:dict(v) for k,v in res.items()},open('person_counts.json','w'))
json.dump({'mao_year':{y:dict(v) for y,v in mao_year.items()},'samples':{f'{a}:{b}':v for (a,b),v in samples.items()}},open('person_extra.json','w'),ensure_ascii=False,indent=1)
src={'mao':['w.zedong-mao-zedong-nianpu','w.jianguo-yilai-mao-zedong','w.mao-zedong-zhuan'],'zhou':['w.zhou-enlai-nianpu-1949','w.zhou-enlai-nianpu-1949-2020','w.zhou-enlai-waijiao-huodong','w.jian-zhou-enlai'],
 'liu':['w.shaoqi-liu-shaoqi-nianpu-chronology'],'deng':['w.deng-xiaoping-nianpu-1904'],'chenyi':['w.chen-yi-nianpu'],'zhu':['w.zhu-de-nianpu-xinbian'],'pengzhen':['w.peng-zhen-nianpu-1902'],
 'pengdh':['w.peng-dehuai-nianpu'],'chenyun':['w.chen-yun-nianpu-xiuding'],'ye':['w.liu-jixian-ye-jianying-nianpu'],'yang':['w.yang-shangkun-riji'],'lin':['w.teiwes-tragedy-of-lin-biao']}
print(f"{'who':10}{'sole':>7}{'joint':>7}{'named':>7}{'1st-src':>8}")
for p in P:
    k=p[0]; v=res[k]
    fs=sum(1 for e in E if e['works'] and e['works'][0] in src.get(k,[]))
    print(f"{p[1]:14}{v['sole']:>6}{v['joint']:>6}{v['named']:>7}{fs:>8}")
print('Mao by year (sole/joint/named):')
for y in sorted(mao_year): print(y, dict(mao_year[y]))
json.dump([{'id':e['id'],'s':e['_s'],'actors':e['_actors']} for e in E],open('actors.json','w'),ensure_ascii=False)
