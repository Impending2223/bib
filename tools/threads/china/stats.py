import json,re,collections,sys
from lexicon import EP
E=[json.loads(l) for l in open('china.jsonl')]
E=[e for e in E if e['thread'] in ('china-leadership','china') or 'india-and-china-cultural-revolution' in e['also'] or 'china-leadership' in e['also']]
def ym(d): return d[:7] if len(d)>=7 else d[:4]+'-??'
def spark(months, lo, hi):
    # entries per month across window lo..hi expanded by 2 months; text histogram
    pass
rows=[]
for slug,name,lo,hi,rx in EP:
    R=re.compile(rx,re.I)
    hits=[e for e in E if R.search(e['c'])]
    inwin=[e for e in hits if lo<=e['date'][:7]<=hi or (len(e['date'])==4 and lo[:4]<=e['date']<=hi[:4])]
    ds=sorted(e['date'] for e in inwin)
    cl=sum(e['thread']=='china-leadership' for e in inwin)
    cr=sum('india-and-china-cultural-revolution' in e['also'] for e in inwin)
    byq=collections.Counter(ym(e['date']) for e in inwin)
    top=sorted(byq.items(),key=lambda x:-x[1])[:4]
    rows.append((slug,name,len(hits),len(inwin),ds[0] if ds else '',ds[-1] if ds else '',cl/len(inwin) if inwin else 0,cr,byq,top))
json.dump([(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],dict(r[8])) for r in rows],open('episode_stats.json','w'))
for r in rows:
    print(f"{r[0]:26} all={r[2]:5} win={r[3]:5} {r[4]:10}..{r[5]:10} CL={r[6]:.0%} CR={r[7]:3} peak={' '.join(f'{a}:{b}' for a,b in r[9])}")
