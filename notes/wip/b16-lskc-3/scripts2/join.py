import yaml, sys, glob, os
HERE=os.path.dirname(os.path.abspath(__file__))
ops=[]; pk={}
files=sorted(glob.glob(HERE+'/o[0-9]*.yaml'))+[HERE+'/pre.yaml'] if os.path.exists(HERE+'/pre.yaml') else sorted(glob.glob(HERE+'/o[0-9]*.yaml'))
for f in files:
    for o in yaml.safe_load(open(f)):
        if 'place-key' in o: pk[o['place-key']['key']]=o
        else: ops.append(o)
import json
PK=json.load(open(HERE+'/pks.json'))
used=set()
for o in ops:
    pl=o.get('add',{}).get('entry',{}).get('place')
    if pl: used|=set([pl] if isinstance(pl,str) else pl)
adds=[o for o in ops if 'add' in o]; rest=[o for o in ops if 'add' not in o]
for k in used:
    if k not in pk and k in PK: pk[k]={'place-key':PK[k]}
ops=[v for k,v in pk.items() if k in used]+adds+rest
doc={'patch':'2026-11-14-b16-lskc-3','by':"Claude (batch 16, reader 6: Lịch sử kháng chiến chống Mỹ cứu nước, vol. VI, to Dec. 31, 1969), Nov. 19, 2026",'ops':ops}
class D(yaml.SafeDumper): pass
def strrep(d,s):
    sty="'" if any(ch in s for ch in ":#'\"*[]{}&!|>%@`") or s[:1] in "-?" or s!=s.strip() else None
    return d.represent_scalar('tag:yaml.org,2002:str',s,style=sty)
D.add_representer(str,strrep)
out='/home/user/bib/inbox/2026-11-14-b16-lskc-3.yaml'
open(out,'w').write(yaml.dump(doc,Dumper=D,allow_unicode=True,sort_keys=False,width=100000,default_flow_style=False))
print(len(ops),'ops',len(used),'place keys', len(pk))
