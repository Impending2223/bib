"""Best scheme (G6 + conference day-windows, Yang split) and the survey file."""
import pickle,re,collections,json,random
import assign2 as A
from scheme import EPISODES
CL=A.CL
CONF=[('china-shanghai-1960','1960-01-07','1960-01-17'),('china-shanghai-1960','1960-07-05','1960-08-10'),('china-twelve-articles','1961-01-14','1961-01-18'),
 ('china-sixty-articles','1961-03-10','1961-03-23'),('china-sixty-articles','1961-05-21','1961-06-12'),('china-sixty-articles','1961-08-23','1961-09-16'),
 ('china-seven-thousand','1962-01-11','1962-02-07'),('china-retreat-1962','1962-02-21','1962-02-23'),('china-tenth-plenum','1962-07-25','1962-08-24'),('china-tenth-plenum','1962-09-24','1962-09-27'),
 ('china-four-cleanups','1963-05-02','1963-05-12'),('china-four-cleanups','1964-12-15','1965-01-14'),('china-luo-ruiqing','1965-12-08','1965-12-15'),
 ('china-may-sixteenth','1966-05-04','1966-05-26'),('china-red-guards','1966-08-01','1966-08-12'),('china-red-guards','1966-10-09','1966-10-28'),
 ('china-ninth-congress','1968-10-13','1968-10-31'),('china-ninth-congress','1969-04-01','1969-04-24')]
W=re.compile(r"conference|会议|大会|plenary|plenum|全会|group meeting|小组|the meeting|Politburo|政治局|Congress|代表",re.I)
for e in CL:
    d=e['date']
    e['_conf']=[s for s,lo,hi in CONF if len(d)==10 and lo<=d<=hi and W.search(e['c'])]
    if e['_conf']: e['_ep']=list(dict.fromkeys(e['_ep']+e['_conf']))
r=A.run('BEST',['ep','weak','mao','cou','person'],A.DAY,srcpersons=True)
D={e['id']:e for e in CL}
# Yang split at 1963
for i,(k,lv,c) in list(r['assign'].items()):
    if k=='yang':
        nk='yang-1960-62' if D[i]['date'][:4]<'1963' else 'yang-1963-65'
        r['assign'][i]=(nk,lv,c)
T=collections.defaultdict(list)
for i,(k,lv,c) in r['assign'].items(): T[k].append(D[i])
pickle.dump((r['assign'],[e['id'] for e in r['residual']]),open('best.pkl','wb'))
print(f"clean {r['clean']:.1%} amb {r['amb']:.1%} res {r['res']:.1%}")
for k in sorted(T,key=lambda k:-len(T[k])): print(k,len(T[k]))
json.dump({k:len(v) for k,v in T.items()},open('best_sizes.json','w'))
