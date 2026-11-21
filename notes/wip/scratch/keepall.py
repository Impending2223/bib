# keepall.py FILE: resolve each listed duplicate flag as distinct (keep)
import sys
sys.path.insert(0, '/home/user/bib/tools')
from bib import store
from bib.merge import resolve
s = store.Series()
ids = [l.strip() for l in open(sys.argv[1]) if l.strip()]
ok = bad = 0
for i in ids:
    try:
        r = resolve(s, i, 'keep', None); ok += 1
    except SystemExit as e:
        bad += 1; print('FAIL', i, e)
print('resolved', ok, 'failed', bad)
