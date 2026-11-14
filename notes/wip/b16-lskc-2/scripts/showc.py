import sys,os,subprocess,re
sys.path.insert(0,os.path.join(os.getcwd(),'tools'))
from bib import store
s=store.Series()
for i in sys.argv[1:]:
    r=s.get(i); e=next((x for x in r if isinstance(x,dict)),None) if isinstance(r,tuple) else r
    print(i, e and e.get('when'), '|', e and e.get('c'))
    print('   n:', e and (e.get('n') or '')[:400]); print('   tags:', e and e.get('tags'))
