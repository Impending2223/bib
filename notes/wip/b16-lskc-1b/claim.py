# claim.py SPEC.py... : claim an id for each A() slug not yet in ids.tsv (new-id, then ledger add); append to ids.tsv
import sys, os, subprocess, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dsl
IDS = os.path.join(dsl.HERE, 'ids.tsv')
have = {}
if os.path.exists(IDS):
    for l in open(IDS, encoding='utf-8'):
        p = l.rstrip('\n').split('\t')
        if len(p) >= 2: have[p[0]] = p[1]
for f in sys.argv[1:]:
    spec = importlib.util.spec_from_file_location('s_' + os.path.basename(f)[:-3], f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for e in dsl.ENT:
    k = e['slug']
    if k in have: continue
    r = subprocess.run(['./bib', 'new-id', 'cal', e['date'], e['thread']], capture_output=True, text=True, cwd='/home/user/bib')
    nid = r.stdout.strip().split()[-1]
    words = e['c'][:70].replace('"', "'").replace('\n', ' ')
    r2 = subprocess.run(['./bib', 'ledger', 'add', e['date'], e['thread'], nid, words, dsl.PATCH], capture_output=True, text=True, cwd='/home/user/bib')
    if r2.returncode != 0: print('LEDGER FAIL', nid, r2.stdout, r2.stderr); sys.exit(1)
    have[k] = nid
    open(IDS, 'a', encoding='utf-8').write(f"{k}\t{nid}\n")
    print(k, nid)
