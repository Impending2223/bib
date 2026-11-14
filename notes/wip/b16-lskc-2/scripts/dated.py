import re,sys
t=open(sys.argv[1]).read()
lo,hi=int(sys.argv[2]),int(sys.argv[3])
pages=re.split(r'^@@ ',t,flags=re.M)
dt=re.compile(r'(\d{1,2}\s*-\s*\d{1,2}\s*-\s*19\d\d|tháng\s+\d{1,2}\s*-\s*19\d\d|ngày\s+\d{1,2}\b|\bđêm\s+\d{1,2}\b|[Tt]háng\s+\d{1,2}\b|\d{1,2}\s*-\s*\d{1,2}\b)')
for pg in pages:
    if not pg.strip(): continue
    head,_,body=pg.partition('\n')
    try: b=int(head.split()[0][2:])
    except ValueError: continue
    if not (lo<=b<=hi): continue
    flat=re.sub(r'(?<=\w)-\n(?=\w)','',body); flat=re.sub(r'\s*\n\s*',' ',flat)
    sents=re.split(r'(?<=[.;!?])\s+',flat)
    out=[s for s in sents if dt.search(s)]
    if out: print('['+str(b)+']',' | '.join(o[:400] for o in out))
