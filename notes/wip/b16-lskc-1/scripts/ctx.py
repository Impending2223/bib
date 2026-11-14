import sys,re
t=open(sys.argv[1],encoding='utf-8').read()
pat=re.compile(sys.argv[2]); before=int(sys.argv[3]) if len(sys.argv)>3 else 150; after=int(sys.argv[4]) if len(sys.argv)>4 else 700
parts=re.split(r'\n\[\[PDF (\d+) \| p\. (\w+)\]\]\n',t)
flat='';marks=[]
for k in range(1,len(parts),3):
    marks.append((len(flat),parts[k+1])); 
    lines=[l.strip() for l in parts[k+2].split('\n') if l.strip()]
    flat+=' '.join(lines)+' '
def page(i):
    p=None
    for pos,bp in marks:
        if pos<=i: p=bp
        else: break
    return p
last=-10**9
for m in pat.finditer(flat):
    if m.start()<last+after: continue
    last=m.start()
    a=max(0,m.start()-before); b=min(len(flat),m.end()+after)
    print(f"[p{page(m.start())}–{page(b)}] {flat[a:b]}\n")
