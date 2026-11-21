# dups.py OUT: entries whose conflicts are all duplicate flags (run from tools/)
import sys
sys.path.insert(0, '/home/user/bib/tools')
from bib import store
s=store.Series(); dup=[]; other=[]
for L in (s.lists.values() if isinstance(s.lists,dict) else s.lists):
  for sec,e in L.entries():
    c=e.get('conflict')
    if not c: continue
    (dup if all(isinstance(k,dict) and k.get('kind')=='duplicate' for k in c) else other).append(e['id'])
open(sys.argv[1],'w').write('\n'.join(dup)); print(len(dup),'dup-only;',len(other),'other:',other[:20])
