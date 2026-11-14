import sys,re
t=open(sys.argv[1],encoding='utf-8').read().split('\f')
bps=[]
for p in t:
    lines=[l for l in p.split('\n') if l.strip()]
    bp=None
    for l in lines[:2]+lines[-2:]:
        m=re.match(r'^\s*(\d{1,3})\s{2,}\S',l) or re.search(r'\S\s{3,}(\d{1,3})\s*$',l) or re.match(r'^\s*(\d{1,3})\s*$',l)
        if m: bp=int(m.group(1)); break
    bps.append(bp)
# check consistency: bp - index offset; smooth
n=len(bps); fixed=[None]*n
for i in range(n):
    if bps[i] is None: continue
    # accept if neighbor agrees
    ok=any(0<=j<n and bps[j] is not None and bps[j]-bps[i]==j-i for j in (i-1,i+1,i-2,i+2))
    if ok: fixed[i]=bps[i]
for i in range(n):
    if fixed[i] is None:
        prv=next((j for j in range(i-1,-1,-1) if fixed[j] is not None),None)
        nxt=next((j for j in range(i+1,n) if fixed[j] is not None),None)
        if prv is not None and nxt is not None and fixed[nxt]-fixed[prv]==nxt-prv: fixed[i]=fixed[prv]+i-prv
        else: fixed[i]=None
with open(sys.argv[2],'w') as f:
    for i,p in enumerate(t):
        f.write(f"\n[[PDF {i+1} | p. {fixed[i]}]]\n"); f.write(p)
gaps=[(i+1) for i in range(n) if fixed[i] is None]
print('unnumbered pdf pages:',gaps)
