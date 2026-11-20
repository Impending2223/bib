import sys,json,yaml,re
idx=json.load(open('/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/b16-lskc-1b/idx.json'))
d=yaml.safe_load(open('/home/user/bib/inbox/2026-11-19-b16-lskc-1b.yaml'))
def toks(c):
    return set(re.findall(r'(?<![.!?] )(?<!^)\b[A-ZĐ][^\W\d_]+(?: [A-ZĐ][^\W\d_]+)?',c))|set(re.findall(r'\b\d+(?:,\d+)?\b',c))
only=sys.argv[1:] 
for o in d['ops']:
    if 'add' not in o: continue
    e=o['add']['entry']
    if only and not any(e['id'].startswith(x) for x in only): continue
    t=toks(e['c']); m=e['date'][:7]
    best=[]
    for i,dt,th,c,p,w in idx:
        if i==e['id'] or not (th or '').startswith(('vietnam','laos')): continue
        if dt[:7]!=m and not (len(e['date'])==4 and dt[:4]==e['date']): continue
        s=len(t&toks(c))
        # shared proper nouns
        sh=[x for x in t&toks(c) if not x.isdigit()]
        if len(sh)>=2: best.append((len(sh),i,sh[:5]))
    best.sort(reverse=True)
    if best: print(e['id'],'<-',[(b[1],b[2]) for b in best[:2]])
