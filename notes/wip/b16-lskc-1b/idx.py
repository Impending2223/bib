# idx.py : build/query a date index of the calendar (scratch). usage: idx.py build | idx.py D [D2] [-t thread] [-w word]
import sys,glob,json,os,yaml,re
S='/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/b16-lskc-1b/idx.json'
if sys.argv[1]=='build':
    out=[]
    for f in sorted(glob.glob('/home/user/bib/lists/cal/19[6-7]*.yaml')):
        d=yaml.load(open(f,encoding='utf-8'),Loader=getattr(yaml,"CSafeLoader",yaml.SafeLoader))
        for e in (d if isinstance(d,list) else d.get('entries',[])):
            out.append([e['id'],str(e.get('date')),e.get('thread'),(e.get('c') or '')[:400],e.get('place'),e.get('when')])
    json.dump(out,open(S,'w'),ensure_ascii=False); print(len(out))
else:
    out=json.load(open(S)); a=sys.argv[1]; b=sys.argv[2] if len(sys.argv)>2 and not sys.argv[2].startswith('-') else a
    th=None;w=None
    if '-t' in sys.argv: th=sys.argv[sys.argv.index('-t')+1]
    if '-w' in sys.argv: w=sys.argv[sys.argv.index('-w')+1].lower()
    for i,d,t,c,p,wh in out:
        if a<=d[:len(a)] or True:
            if not (d[:len(a)]>=a and d[:len(b)]<=b): continue
        if th and t!=th: continue
        if '-v' in sys.argv and not (t or '').startswith(('vietnam','laos','cambodia')): continue
        if w and w not in c.lower(): continue
        print(i,'|',c[:150])
