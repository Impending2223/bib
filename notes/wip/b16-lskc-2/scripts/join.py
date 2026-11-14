import re,sys,os
d,out=sys.argv[1],sys.argv[2]; prev=None; res=[]
for f in sorted(os.listdir(d)):
    p=int(f[:3]); raw=open(os.path.join(d,f)).read()
    t=raw.strip().split('\n')
    if not raw.strip(): continue
    m=re.match(r'\s*(\d+)\s',t[0]+' ') or re.search(r'\s(\d+)\s*$',t[0])
    b=int(m.group(1)) if m else (prev+1 if prev else None)
    if m: t=t[1:]
    prev=b
    body='\n'.join(l.strip() for l in t if l.strip())
    res.append(f'@@ p.{b} (pdf {p})\n{body}\n')
open(out,'w').write('\n'.join(res))
