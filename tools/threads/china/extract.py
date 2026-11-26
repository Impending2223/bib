#!/usr/bin/env python3
"""Regex extraction of calendar entries touching China threads -> china.jsonl."""
import re, json, glob, sys
FIELDS = ('id','date','when','thread','also','c','n','place','tags')
CH = {'china','china-leadership','india-and-china-cultural-revolution'}
def unq(v):
    v=v.strip()
    if v.startswith("'") and v.endswith("'") and len(v)>=2: return v[1:-1].replace("''","'")
    if v.startswith('"') and v.endswith('"') and len(v)>=2: return v[1:-1].encode().decode('unicode_escape') if '\\' in v else v[1:-1]
    return v
def lst(v):
    v=v.strip()
    if v.startswith('['): return [x.strip().strip("'\"") for x in v[1:-1].split(',') if x.strip()]
    return [v] if v else []
out=[]; allthreads={}
for f in sorted(glob.glob('/home/user/bib/lists/cal/[0-9]*.yaml')):
    lines=open(f,encoding='utf-8').read().split('\n')
    cur=None; key=None
    def flush():
        if cur:
            th=cur.get('thread',''); al=lst(cur.get('also',''))
            allthreads[th]=allthreads.get(th,0)+1
            if th in CH or CH & set(al):
                e={k:cur.get(k,'') for k in ('id','date','when','thread','place')}
                e['c']=unq(cur.get('c','')); e['date']=e['date'].strip("'"); e['works']=re.findall(r'\[\[(w\.[^\]]+)\]\]',cur.get('n','')); e['also']=al; e['tags']=lst(cur.get('tags',''))
                e['file']=f.split('/')[-1]; out.append(e)
    for ln in lines:
        m=re.match(r'  - id: (.*)$',ln)
        if m:
            flush(); cur={'id':m.group(1).strip()}; key='id'; continue
        if cur is None: continue
        m=re.match(r'    ([a-z_]+):(?: (.*))?$',ln)
        if m:
            key=m.group(1); cur[key]=(m.group(2) or ''); continue
        if re.match(r'     +\S',ln) and key in FIELDS:
            cur[key]+= ' '+ln.strip()
        elif re.match(r'    \S',ln) or re.match(r'\S',ln):
            key=None
    flush()
with open('china.jsonl','w') as w:
    for e in out: w.write(json.dumps(e,ensure_ascii=False)+'\n')
json.dump(allthreads,open('allthreads.json','w'))
print(len(out))
