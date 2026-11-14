import re,sys
t=open(sys.argv[1]).read(); pat=re.compile(sys.argv[2]); w=int(sys.argv[3]) if len(sys.argv)>3 else 200
pages=re.split(r'^@@ ',t,flags=re.M)
flat_all=[];
for pg in pages:
    if not pg.strip(): continue
    head,_,body=pg.partition('\n')
    flat=re.sub(r'(?<=\w)-\n(?=\w)','',body); flat=re.sub(r'\s*\n\s*',' ',flat)
    flat_all.append((head.split()[0],flat))
# join consecutive to allow cross-page windows
for i,(h,f) in enumerate(flat_all):
    nxt=flat_all[i+1][1][:w] if i+1<len(flat_all) else ''
    s=f+' '+nxt
    last=-10**9
    for m in pat.finditer(f):
        if m.start()-last< w: continue
        last=m.start()
        print(h, '…'+s[max(0,m.start()-w//2):m.end()+w].replace('\n',' ')+'…')
