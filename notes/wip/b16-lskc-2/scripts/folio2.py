import re,sys,os
d=sys.argv[1]; prev=None; out={}
for f in sorted(os.listdir(d)):
    p=int(f[:3]); t=open(os.path.join(d,f)).read().strip().split('\n')
    if not t or not t[0].strip(): continue
    m=re.match(r'\s*(\d+)\s',t[0]+' ') or re.search(r'\s(\d+)\s*$',t[0])
    if m:
        off=p-int(m.group(1))
        if off!=prev: print('pdf',p,'book',m.group(1),'off',off)
        prev=off
