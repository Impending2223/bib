import re,json,sys,glob,yaml
S='/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/b16-lskc-1b/'
idx=json.load(open(S+'idx.json'))
# include my patch entries
d=yaml.safe_load(open('/home/user/bib/inbox/2026-11-19-b16-lskc-1b.yaml'))
for o in d['ops']:
    if 'add' in o:
        e=o['add']['entry']; idx.append([e['id'],e['date'],e['thread'],e['c'],e.get('place'),e.get('when')])
def fold(s):
    import unicodedata
    s=s.replace('Đ','D').replace('đ','d'); s=unicodedata.normalize('NFD',s)
    return ''.join(c for c in s if unicodedata.category(c)!='Mn').lower()
vol,a,b=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
t=open(S+f'txt/v{vol}a.txt',encoding='utf-8').read()
parts=re.split(r'\n\[\[PDF (\d+) \| p\. (\w+)\]\]\n',t)
for k in range(1,len(parts),3):
    bp=parts[k+1]
    if bp=='None' or not (a<=int(bp)<=b): continue
    txt=' '.join(l.strip() for l in parts[k+2].split('\n') if l.strip())
    for sent in re.split(r'(?<=[.;])\s+(?=[A-ZĐÀÁẠẢÃÂẤẦẨẪẬĂẮẰẲẴẶÈÉẸẺẼÊẾỀỂỄỆÌÍỊỈĨÒÓỌỎÕÔỐỒỔỖỘƠỚỜỞỠỢÙÚỤỦŨƯỨỪỬỮỰỲÝỴỶỸ])',txt):
        for m in re.finditer(r'[Tt]háng\s+(\d{1,2})\s*-\s*(196\d)|[Tt]háng\s+(\d{1,2})\s+năm\s+(196\d)',sent):
            mo=m.group(1) or m.group(3); yr=m.group(2) or m.group(4)
            ym=f"{yr}-{int(mo):02d}"
            caps=set(w for w in re.findall(r'\b[A-ZĐ][^\W\d_]+',sent) if len(w)>3)
            capsf={fold(w) for w in caps}-{'tieu','tinh','trung','quan','dai','luc','nam','khu','bo','chi','ngay','tham','thang','sau','cung','phoi','theo'}
            hit=False
            for i,dt,th,c,p,w in idx:
                if not (dt or '').startswith(ym[:7]) and not dt==yr: continue
                if not (th or '').startswith(('vietnam','laos')): continue
                cf=fold(c)
                if sum(1 for w2 in capsf if w2 in cf)>=2: hit=True;break
            if not hit: print(f"[{bp}] {ym}: {sent[:230]}")
            break
