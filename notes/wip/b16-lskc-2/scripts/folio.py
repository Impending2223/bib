import re,sys,os,collections
d=sys.argv[1]
c=collections.Counter(); bad=[]
for f in sorted(os.listdir(d)):
    p=int(f[:3]); t=open(os.path.join(d,f)).read().strip().split('\n')
    if not t or not t[0].strip(): continue
    m=re.match(r'\s*(\d+)\s',t[0]+' ') or re.search(r'\s(\d+)\s*$',t[0])
    if m:
        off=p-int(m.group(1)); c[off]+=1
        if off not in (15,11): bad.append((p,m.group(1)))
print(c.most_common(5)); print(bad[:20])
