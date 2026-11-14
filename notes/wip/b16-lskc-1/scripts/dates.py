import sys,re
t=open(sys.argv[1],encoding='utf-8').read()
yrs=sys.argv[2].split(',')
# join lines into flowing text with page markers kept
pages=re.split(r'\n\[\[PDF (\d+) \| p\. (\w+)\]\]\n',t)
# pages: [pre, pdf, bp, text, pdf, bp, text...]
out=[]
D=re.compile(r'(?:(?:ngày|đêm|sáng|chiều|tối|từ|đến)\s+)?(?:\d{1,2}(?:\s*(?:,|và|-|đến)\s*\d{1,2})*\s*-\s*)?\d{1,2}\s*-\s*(19\d\d)|tháng\s+\d{1,2}\s+năm\s+(19\d\d)|ngày\s+\d{1,2}\s+tháng\s+\d{1,2}\s+năm\s+(19\d\d)')
for k in range(1,len(pages),3):
    bp=pages[k+1]; txt=pages[k+2]
    flat=re.sub(r'\s+',' ',txt)
    for m in D.finditer(flat):
        y=m.group(1) or m.group(2) or m.group(3)
        if y in yrs:
            a=max(0,m.start()-110); b=min(len(flat),m.end()+90)
            out.append(f"p{bp}: …{flat[a:b]}…")
print(len(out))
open(sys.argv[3],'w').write('\n'.join(out))
