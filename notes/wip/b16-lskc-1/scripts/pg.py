import sys,re
t=open(sys.argv[1],encoding='utf-8').read()
a,b=int(sys.argv[2]),int(sys.argv[3])
parts=re.split(r'\n\[\[PDF (\d+) \| p\. (\w+)\]\]\n',t)
for k in range(1,len(parts),3):
    bp=parts[k+1]
    if bp!='None' and a<=int(bp)<=b:
        txt=parts[k+2]
        lines=[l.strip() for l in txt.split('\n') if l.strip()]
        # drop running head
        if lines and re.match(r'^(\d+\s+lịch sử|Chương|\d+$)',lines[0]) : lines=lines[1:]
        if lines and re.search(r'\s\d+$',lines[0]) and len(lines[0])<80: lines=lines[1:]
        s=' '.join(lines); s=re.sub(r'-\s(?=[a-zđ])','',s) if False else s
        print(f"<<{bp}>> {s}")
