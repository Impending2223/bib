# join2.py OUT.yaml SPEC.py... : the predecessor's partial patch (sound ops) + the specs -> one patch
import sys, os, re, json, glob, importlib.util, yaml, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dsl
out = sys.argv[1]
ids = {}
for l in open(os.path.join(dsl.HERE, 'ids.tsv'), encoding='utf-8'):
    p = l.rstrip('\n').split('\t'); ids[p[0]] = p[1]
for f in sys.argv[2:]:
    spec = importlib.util.spec_from_file_location('s_' + os.path.basename(f)[:-3], f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
# known names
known = set()
for f in glob.glob('/home/user/bib/lists/cal/19*.yaml'):
    for l in open(f, encoding='utf-8'):
        for mm in re.finditer(r'name:([a-z0-9-]+)', l): known.add(mm.group(1))
known |= set(json.load(open('/home/user/bib/sources/frus-names/persons.json')).keys())
gaz = {x['key'] for x in yaml.safe_load(open('/home/user/bib/sources/places.yaml'))}
noname = collections.OrderedDict()
usedplace = set()
adds = []
for e in dsl.ENT:
    tg = [] if any(t.startswith('polity:') for t in e['tags']) else ['polity:drv']
    for nm in e['names']:
        k = dsl.fold(nm)
        if k in known: tg.append('name:' + k)
        else: noname[nm] = 1
    if e['vis']: tg.append('vis:only:drv')
    tg += e['tags']
    ent = collections.OrderedDict()
    ent['id'] = ids[e['slug']]; ent['when'] = e['when']; ent['date'] = e['date']
    if e.get('at'): ent['at'] = e['at']
    if e['place']:
        ent['place'] = e['place']
        for p in ([e['place']] if isinstance(e['place'], str) else e['place']): usedplace.add(p)
    ent['thread'] = e['thread']
    if e['also']: ent['also'] = e['also']
    ent['c'] = e['c']; ent['n'] = e['n']; ent['tags'] = tg
    for k in ('time', 'time_approx', 'time_range', 'time_band', 'time_zone'):
        if e.get(k): ent[k] = e[k]
    if e.get('follows'): ent['follows'] = e['follows']
    adds.append({'add': {'entry': ent}})
pre_adds=[]; pre_rest=[]
# placeups for predecessor adds
PU = getattr(dsl, 'PLACEUP', {})
for o in pre_adds:
    en = o['add']['entry']
    if en['id'] in PU:
        d = PU[en['id']]
        for k, v in d.items():
            if k == 'place':
                en['place'] = v
                for p in ([v] if isinstance(v, str) else v): usedplace.add(p)
            elif k == 'tags_add': en['tags'] = en['tags'] + [t for t in v if t not in en['tags']]
            else: en[k] = v
    if en.get('place'):
        for p in ([en['place']] if isinstance(en['place'], str) else en['place']): usedplace.add(p)
NP = getattr(dsl, 'NEWP', {})
pk = []
for p in sorted(usedplace):
    if p in gaz: continue
    if p not in NP: print('MISSING PLACE KEY', p); continue
    nm, inn, tz = NP[p]
    pk.append({'place-key': {'key': p, 'name': nm, 'zone': tz, 'in': inn}})
ops = pk + pre_adds + adds + pre_rest + dsl.OTHER
doc = {'patch': dsl.PATCH, 'by': 'Claude (batch 16, reader 4b: Lịch sử kháng chiến chống Mỹ, cứu nước, vols. I–III, the rest), Nov. 19, 2026', 'ops': ops}
class D(yaml.SafeDumper): pass
def strrep(dumper, s):
    style = "'" if (': ' in s or ' #' in s or s[:1] in "*['\"&!%@`{|>-?," or s != s.strip() or s.lower() in ('yes', 'no', 'true', 'false', 'null', 'on', 'off') or s[:1].isdigit() or s.endswith(':')) else None
    return dumper.represent_scalar('tag:yaml.org,2002:str', s, style=style)
D.add_representer(str, strrep)
D.add_representer(collections.OrderedDict, lambda d, o: d.represent_dict(o.items()))
open(out, 'w').write(yaml.dump(doc, Dumper=D, allow_unicode=True, sort_keys=False, width=100000, default_flow_style=False))
print(len(pk), 'place-keys', len(pre_adds), 'pre adds', len(adds), 'new adds', len(pre_rest), 'pre other', len(dsl.OTHER), 'new other')
json.dump(list(noname), open(os.path.join(dsl.HERE, 'noname.json'), 'w'), ensure_ascii=False)
print('no name entry:', list(noname))
