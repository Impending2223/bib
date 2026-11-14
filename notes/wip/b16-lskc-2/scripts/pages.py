import re,sys
t=open(sys.argv[1]).read(); lo,hi=int(sys.argv[2]),int(sys.argv[3])
for pg in re.split(r'^@@ ',t,flags=re.M):
    head,_,body=pg.partition('\n')
    try: b=int(head.split()[0][2:])
    except: continue
    if lo<=b<=hi:
        flat=re.sub(r'(?<=\w)-\n(?=\w)','',body); flat=re.sub(r'\s*\n\s*',' ',flat)
        print(f'[{b}] {flat}')
