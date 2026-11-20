import yaml, sys
sys.path.insert(0,'.')
from lib import band, utc, GAZ, PKS
ops = yaml.safe_load(open('/home/user/bib/notes/wip/b16-lskc-3/partial-patch.yaml'))['ops']
OV = {
 'cal.1969-02-03.vietnam-hanoi': dict(place='hanoi'),
 'cal.1969-02-22.vietnam-hanoi': dict(bnd='night', ok='ok:fields-place'),
 'cal.1969-03-29.vietnam-hanoi': dict(ok='ok:fields-place'),
 'cal.1969-05.vietnam-hanoi': dict(place='hanoi'),
 'cal.1969-05-08.vietnam-hanoi-2': dict(place='paris'),
 'cal.1969-05-11.vietnam-hanoi': dict(place='dak-to', bnd='predawn'),
 'cal.1969-06-06.vietnam-hanoi': dict(place='war-zone-d'),
 'cal.1969-06-23.vietnam-hanoi': dict(place='plain-of-jars', bnd='night'),
 'cal.1969-08-11.vietnam-hanoi': dict(place='loc-ninh', bnd='night'),
 'cal.1969-09-04.vietnam-hanoi-4': dict(place='hue', bnd='night'),
 'cal.1969-09-08.vietnam-hanoi': dict(t='00:00'),
 'cal.1969-10.vietnam-hanoi': dict(at='before 1969-10-21', ok='ok:fields-place'),
 'cal.1969-10-25.vietnam-hanoi': dict(place='plain-of-jars'),
 'cal.1969-10-29.vietnam-hanoi': dict(place='ka-te', bnd='early morning'),
 'cal.1969-11-03.vietnam-hanoi': dict(place='bu-dop'),
 'cal.1969-11-06.vietnam-hanoi': dict(ok='ok:fields-place'),
 'cal.1969-12.vietnam-hanoi': dict(at='before 1969-12-01'),
}
TZ='Asia/Ho_Chi_Minh'
out=[]
for o in ops:
    if 'add' in o:
        e=o['add']['entry']; ov=OV.get(e['id'],{})
        if 'place' in ov:
            assert ov['place'] in GAZ or ov['place'] in PKS, ov['place']
            e['place']=ov['place']
        if 'bnd' in ov:
            e['time_range']=band(e['date'],ov['bnd'],TZ); e['time_band']=ov['bnd']; e['time_zone']=TZ; e['range_basis']='record'
        if 't' in ov:
            e['time']=utc(e['date'],ov['t'],TZ); e['time_zone']=TZ
        if 'at' in ov: e['at']=ov['at']
        if 'ok' in ov: e['tags'].append(ov['ok'])
    out.append(o)
adds=[o for o in out if 'add' in o]; rest=[o for o in out if 'add' not in o]
class D(yaml.SafeDumper): pass
def strrep(d,s):
    sty="'" if any(ch in s for ch in ":#'\"*[]{}&!|>%@`") or s[:1] in "-?" or s!=s.strip() else None
    return d.represent_scalar('tag:yaml.org,2002:str',s,style=sty)
D.add_representer(str,strrep)
open('pre.yaml','w').write(yaml.dump(adds+rest,Dumper=D,allow_unicode=True,sort_keys=False,width=100000,default_flow_style=False))
print(len(adds),len(rest))
