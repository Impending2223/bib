import json,re,collections,random,sys
from scheme import EPISODES,COUNTRIES,PERSONS,PLACES,CRW
E=[json.loads(l) for l in open('china.jsonl')]
ACT={a['id']:a for a in json.load(open('actors.json'))}
CL=[e for e in E if e['thread']=='china-leadership']
def inwin(d,lo,hi):
    if len(d)>=7: return lo<=d[:7]<=hi
    return lo[:4]<=d[:4]<=hi[:4]
EPC=[(s,n,lo,hi,[(a,b,re.compile(r,re.I)) for a,b,r in comps],w) for s,n,lo,hi,comps,w in EPISODES]
CRWR=re.compile(CRW,re.I)
COU=[(s,re.compile(r)) for s,r in COUNTRIES]
PLA=[(s,n,re.compile(r),set(pf)) for s,n,r,pf in PLACES]
for e in CL:
    pl=[t.strip() for t in e['place'].split(' - ') if t.strip()]
    txt=e['c']+' '+' '.join('PLACE:'+p for p in pl)
    d=e['date']
    e['_ep']=[s for s,n,lo,hi,comps,w in EPC if any(inwin(d,a,b) and r.search(txt) for a,b,r in comps)]
    cou=[s for s,r in COU if r.search(e['c'])]
    e['_cou']=cou
    e['_weak']=[s for s,n,lo,hi,comps,w in EPC if w and inwin(d,*w) and CRWR.search(e['c'])] if not cou else []
    a=ACT[e['id']]['actors']; e['_act']=a[0] if a else None; e['_acts']=a
    e['_pl']=[s for s,n,r,pf in PLA if r.search(e['c']) or (set(pl)&pf)]
SPAN={s:(lo,hi) for s,n,lo,hi,c,w in EPISODES}
def winlen(s):
    lo,hi=SPAN[s]; return (int(hi[:4])*12+int(hi[5:7]))-(int(lo[:4])*12+int(lo[5:7]))
PSPAN={k:(lo,hi) for k,n,lo,hi in PERSONS}
def run(levels, label, persons=(), places=(), weak=True, keep=False):
    out=collections.Counter(); clean=amb=resolved=res=0; sizes=collections.Counter(); residual=[]; ambex=collections.Counter()
    for e in CL:
        decided=None
        for lv in levels:
            if lv=='ep':
                c=e['_ep'] or (e['_weak'] if weak else [])
            elif lv=='cou': c=[x for x in e['_cou'] if not x.startswith('(')] if 'nothread' not in label else e['_cou']
            elif lv=='cou+': c=e['_cou']
            elif lv=='person': c=[e['_act']] if e['_act'] in persons and inwin(e['date'],*PSPAN[e['_act']]) else []
            elif lv=='mao': c=['mao'] if e['_act']=='mao' else []
            elif lv=='place': c=[p for p in e['_pl'] if p in places]
            if c: decided=(lv,c); break
        if not decided:
            res+=1; residual.append(e); sizes['(residual)']+=1; continue
        lv,c=decided
        if len(c)==1: clean+=1; sizes[c[0]]+=1
        else:
            amb+=1; ambex[tuple(sorted(c))]+=1
            pick=min(c,key=winlen) if lv=='ep' else c[0]
            sizes[pick]+=1
        if keep: e['_assigned']=(lv,c)
    n=len(CL)
    return dict(label=label,clean=clean/n,amb=amb/n,res=res/n,sizes=sizes,residual=residual,ambex=ambex)
SCHEMES=[
 ('A. episodes (strong keywords only)',['ep'],(),(),False),
 ('A2. episodes, stages by date + CR words',['ep'],(),(),True),
 ('B. episodes + Mao',['ep','mao'],(),(),True),
 ('C. episodes + Mao + Liu + Zhou',['ep','person'],('mao','liu','zhou'),(),True),
 ('D. episodes + Mao, then country threads, then Liu + Zhou',['ep','mao','cou','person'],('mao','liu','zhou'),(),True),
 ('E. D + places',['ep','mao','cou','person','place'],('mao','liu','zhou'),('peking-city','shanghai','hubei','sichuan','guangxi','guangdong','henan','anhui','gansu','inner-mongolia','tibet','xinjiang','hebei','shaanxi'),True),
 ('F. E + the daybooks (Chen Yi, Zhu De, Yang Shangkun, Peng Zhen, Deng, Peng Dehuai, Chen Yun, Ye Jianying)',['ep','mao','cou','person','place'],('mao','liu','zhou','chenyi','zhu','yang','pengzhen','deng','pengdh','chenyun','ye'),('peking-city','shanghai','hubei','sichuan','guangxi','guangdong','henan','anhui','gansu','inner-mongolia','tibet','xinjiang','hebei','shaanxi'),True),
]
R=[]
for lab,lv,pers,pls,weak in SCHEMES:
    r=run(lv,lab,pers,pls,weak); R.append(r)
    sz=[v for k,v in r['sizes'].items() if k!='(residual)']
    small=[k for k,v in r['sizes'].items() if v<40 and k!='(residual)']; big=[k for k,v in r['sizes'].items() if v>3000 and k!='(residual)']
    print(f"{lab}\n  clean {r['clean']:.1%}  ambiguous {r['amb']:.1%}  residual {r['res']:.1%}  threads {len(sz)}  <40: {small}  >3000: {big}")
import pickle
pickle.dump(R,open('runs.pkl','wb'))
pickle.dump(CL,open('cl.pkl','wb'))
