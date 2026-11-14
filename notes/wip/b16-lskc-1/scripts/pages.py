import sys,re
t=open(sys.argv[1],encoding='utf-8').read().split('\f')
out=[]
for i,p in enumerate(t,1):
    lines=[l for l in p.split('\n') if l.strip()]
    bp=None
    for l in lines[:2]+lines[-2:]:
        m=re.match(r'^\s*(\d{1,3})\s{2,}\S',l) or re.search(r'\S\s{3,}(\d{1,3})\s*$',l) or re.match(r'^\s*(\d{1,3})\s*$',l)
        if m: bp=int(m.group(1)); break
    out.append((i,bp))
for i,bp in out[::int(sys.argv[2]) if len(sys.argv)>2 else 25]: print(i,bp, (bp-i) if bp else None)
