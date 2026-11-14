import re,sys
t=open(sys.argv[1]).read(); lo,hi=int(sys.argv[2]),int(sys.argv[3]); pat=re.compile(sys.argv[4])
for pg in re.split(r'^@@ ',t,flags=re.M):
    head,_,body=pg.partition('\n')
    try: b=int(head.split()[0][2:])
    except: continue
    if not lo<=b<=hi: continue
    flat=re.sub(r'(?<=\w)-\n(?=\w)','',body); flat=re.sub(r'\s*\n\s*',' ',flat)
    for s in re.split(r'(?<=[.;!?])\s+',flat):
        if pat.search(s): print(f'[{b}]',s[:600])
