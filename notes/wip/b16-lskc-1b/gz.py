import sys,yaml,unicodedata,re
def fold(s):
    s=s.replace('Đ','D').replace('đ','d'); s=unicodedata.normalize('NFD',s)
    return re.sub(r'[^a-z0-9]+','-',''.join(c for c in s if unicodedata.category(c)!='Mn').lower()).strip('-')
g=yaml.safe_load(open('/home/user/bib/sources/places.yaml'))
for q in sys.argv[1:]:
    f=fold(q); hit=[(x['key'],x.get('name'),x.get('zone'),x.get('in')) for x in g if f in x['key'] or f in fold(x.get('name',''))]
    print(q,'->',hit[:8] or 'NONE')
