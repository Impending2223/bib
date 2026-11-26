import pickle,re,collections,json
from scheme import PLACES
CL=pickle.load(open('cl.pkl','rb'))
DAY={'mao','liu','zhou','chenyi','zhu','yang','pengzhen','deng','pengdh','chenyun','ye'}
extra=[('niujiao','Niujiao',r"Niujiao|牛角",{'niujiao'}),('xian','Xi\'an',r"Xi'an|西安",{'xian'}),('daoxian','Dao county',r"Daoxian|Dao county|道县",{'daoxian'}),
       ('chongqing','Chongqing',r"Chongqing|重庆",{'chongqing'}),('nanning','Nanning',r"Nanning|南宁",{'nanning'}),('wuhan-city','Wuhan',r"Wuhan|武汉",{'wuhan'})]
PL=[(s,n,re.compile(r),set(pf)) for s,n,r,pf in PLACES]+[(s,n,re.compile(r),pf) for s,n,r,pf in extra]
rows=[]
for s,n,r,pf in PL:
    xs=[e for e in CL if r.search(e['c']) or (set(t.strip() for t in e['place'].split(' - '))&pf)]
    if not xs: continue
    byf=sum(1 for e in xs if set(t.strip() for t in e['place'].split(' - '))&pf)
    yrs=collections.Counter(e['date'][:4] for e in xs)
    cl=collections.Counter()
    for e in xs:
        if e['_ep']: k='episode'
        elif e['_weak']: k='stage (date+CR words)'
        elif e['_act']=='mao': k='Mao'
        elif [c for c in e['_cou'] if not c.startswith('(')]: k='country thread'
        elif e['_act'] in ('liu','zhou'): k='Liu/Zhou'
        elif e['_act'] in DAY: k='other daybook'
        else: k='free'
        cl[k]+=1
    eps=collections.Counter(x for e in xs for x in e['_ep']).most_common(3)
    ds=sorted(e['date'] for e in xs)
    rows.append((s,n,len(xs),byf,ds[0],ds[-1],yrs.most_common(3),dict(cl),eps))
    print(f"{n:18} {len(xs):5} (place field {byf}) {ds[0][:7]}..{ds[-1][:7]} peak {yrs.most_common(3)}\n    {dict(cl)}  top episodes {eps}")
json.dump(rows,open('places.json','w'),ensure_ascii=False)
# what's free in the big places
import random; random.seed(2)
for s in ('peking-city','shanghai','sichuan','shaanxi','beidaihe','zhejiang'):
    n,r,pf=[(n,r,pf) for ss,n,r,pf in PL if ss==s][0]
    xs=[e for e in CL if (r.search(e['c']) or (set(t.strip() for t in e['place'].split(' - '))&pf)) and not e['_ep'] and not e['_weak'] and e['_act'] not in DAY and not [c for c in e['_cou'] if not c.startswith('(')]]
    print('== free',n,len(xs))
    for e in random.sample(xs,min(6,len(xs))): print('   ',e['date'],'|',e['c'][:120])
