"""Schemes G/H: add source rules (what the work treats) and daybook-by-source persons."""
import pickle,collections,json,random,re
from scheme import EPISODES,PERSONS
CL=pickle.load(open('cl.pkl','rb'))
def inwin(d,lo,hi):
    if len(d)>=7: return lo<=d[:7]<=hi
    return lo[:4]<=d[:4]<=hi[:4]
STAGES=[(s,w) for s,n,lo,hi,c,w in EPISODES if w]
SPAN={s:(lo,hi) for s,n,lo,hi,c,w in EPISODES}
def winlen(s):
    lo,hi=SPAN[s]; return (int(hi[:4])*12+int(hi[5:7]))-(int(lo[:4])*12+int(lo[5:7]))
CRSRC={'w.yang-jisheng-tiandi-fanfu','w.pu-weihua-zalan-jiu-shijie','w.macfarquhar-maos-last-revolution','w.dikotter-cultural-revolution'}
FAMSRC={'w.yang-jisheng-mubei','w.dikotter-maos-great-famine'}
POLSRC={'w.lengxi-shinian-lunzhan-1956-1966'}
SRCP={'w.zedong-mao-zedong-nianpu':'mao','w.jianguo-yilai-mao-zedong':'mao','w.mao-zedong-zhuan':'mao',
 'w.zhou-enlai-nianpu-1949':'zhou','w.zhou-enlai-nianpu-1949-2020':'zhou','w.zhou-enlai-waijiao-huodong':'zhou','w.jian-zhou-enlai':'zhou',
 'w.shaoqi-liu-shaoqi-nianpu-chronology':'liu','w.deng-xiaoping-nianpu-1904':'deng','w.chen-yi-nianpu':'chenyi','w.zhu-de-nianpu-xinbian':'zhu',
 'w.peng-zhen-nianpu-1902':'pengzhen','w.peng-dehuai-nianpu':'pengdh','w.chen-yun-nianpu-xiuding':'chenyun','w.liu-jixian-ye-jianying-nianpu':'ye',
 'w.yang-shangkun-riji':'yang','w.teiwes-tragedy-of-lin-biao':'lin'}
PSPAN={k:(lo,hi) for k,n,lo,hi in PERSONS}
PLACESET=('peking-city','shanghai','hubei','sichuan','guangxi','guangdong','henan','anhui','gansu','inner-mongolia','tibet','xinjiang','hebei','shaanxi')
def srcrule(e):
    w=e['works'][0] if e['works'] else ''; d=e['date']; out=[]
    if w in FAMSRC and inwin(d,'1959-10','1962-12'): out.append('china-famine')
    if w in POLSRC:
        for s in ('china-moscow-1960','china-polemic'):
            if inwin(d,*SPAN[s]): out.append(s)
    if w in CRSRC:
        out+=[s for s,win in STAGES if inwin(d,*win)]
    return out
def stage_bydate(e):
    if [c for c in e['_cou'] if not c.startswith('(')]: return []
    return [s for s,win in STAGES if inwin(e['date'],*win)]
def run(label, levels, persons, places=PLACESET, srcpersons=False):
    sizes=collections.Counter(); clean=amb=res=0; residual=[]; ambex=collections.Counter(); assign={}
    for e in CL:
        dec=None
        for lv in levels:
            if lv=='ep': c=e['_ep']
            elif lv=='weak': c=e['_weak'] or srcrule(e)
            elif lv=='stagedate': c=stage_bydate(e)
            elif lv=='mao': c=['mao'] if (e['_act']=='mao' or ('mao' in e['_acts'])) else []
            elif lv=='cou': c=[x for x in e['_cou'] if not x.startswith('(')]
            elif lv=='person':
                c=[e['_act']] if e['_act'] in persons and inwin(e['date'],*PSPAN[e['_act']]) else []
                if not c and srcpersons:
                    w=e['works'][0] if e['works'] else ''
                    p=SRCP.get(w)
                    if p in persons and inwin(e['date'],*PSPAN[p]): c=[p]
            elif lv=='place': c=[p for p in e['_pl'] if p in places]
            if c: dec=(lv,c); break
        if not dec: res+=1; residual.append(e); continue
        lv,c=dec; c=list(dict.fromkeys(c))
        if len(c)==1: clean+=1; pick=c[0]
        else:
            amb+=1; ambex[tuple(sorted(c))]+=1
            pick=min(c,key=winlen) if lv in('ep','weak','stagedate') else c[0]
        sizes[pick]+=1; assign[e['id']]=(pick,lv,c)
    n=len(CL)
    return dict(label=label,clean=clean/n,amb=amb/n,res=res/n,sizes=sizes,residual=residual,ambex=ambex,assign=assign)
DAY=('mao','liu','zhou','chenyi','zhu','yang','pengzhen','deng','pengdh','chenyun','ye','lin')
S=[
 run('G1. episodes + source rules (no persons, no places)',['ep','weak'],()),
 run('G2. G1 + CR stages by date for all domestic entries',['ep','weak','stagedate'],()),
 run('G3. G1 + Mao',['ep','weak','mao'],()),
 run('G4. G1 + Mao + country threads + Liu, Zhou',['ep','weak','mao','cou','person'],('liu','zhou')),
 run('G5. G4 + places',['ep','weak','mao','cou','person','place'],('liu','zhou')),
 run('G6. G4 + all daybooks by actor and by source (no places)',['ep','weak','mao','cou','person'],DAY,srcpersons=True),
 run('G7. G6 + places',['ep','weak','mao','cou','person','place'],DAY,srcpersons=True),
 run('G8. G7 with stages by date',['ep','weak','stagedate','mao','cou','person','place'],DAY,srcpersons=True),
]
for r in S:
    small=[k for k,v in r['sizes'].items() if v<40]; big=[k for k,v in r['sizes'].items() if v>3000]
    print(f"{r['label']}\n  clean {r['clean']:.1%}  ambiguous {r['amb']:.1%}  residual {r['res']:.1%}  threads {len(r['sizes'])}  <40 {small}  >3000 {big}")
pickle.dump(S,open('runs2.pkl','wb'))
