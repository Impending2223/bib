import sys,os
sys.path.insert(0,os.path.join(os.getcwd(),'tools'))
from bib import store, lives as L
s=store.Series()
ps=L.everyone(s)
idx={}
for p in ps:
    for n in p['names']|{p['name']}:
        idx.setdefault(L.fold(n).lower(),set()).add(L.key_of(p['name'])+'  <'+p['name']+'>')
for q in sys.argv[1:]:
    f=L.fold(q).lower()
    hits=[v for k,v in idx.items() if f in k]
    print(q,'->',sorted(set().union(*hits))[:6] if hits else 'NONE')
