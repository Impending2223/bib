"""Members of each Congress at its opening, 87th-93rd, from congress-legislators."""
import collections, json, os, sys, yaml
# Usage: python3 tools/congress/make_rosters.py PATH/TO/congress-legislators
#   (a clone of https://github.com/unitedstates/congress-legislators). Rewrites congress/<NN>.yaml.
#   Hand corrections live in VACANT, ADD, and NOTE below; edit those, not the output, then rerun.
SRC = sys.argv[1] if len(sys.argv) > 1 else '../congress-legislators'
L = yaml.load(open(os.path.join(SRC, 'legislators-historical.yaml')), Loader=yaml.SafeLoader) + \
    yaml.load(open(os.path.join(SRC, 'legislators-current.yaml')), Loader=yaml.SafeLoader)
OPEN={87:'1961-01-03',88:'1963-01-09',89:'1965-01-04',90:'1967-01-10',91:'1969-01-03',92:'1971-01-21',93:'1973-01-03'}
FIRSTYEAR={c:1961+2*(c-87) for c in OPEN}
A50=dict(AL=9,AZ=2,AR=6,CA=30,CO=4,CT=6,DE=1,FL=8,GA=10,ID=2,IL=25,IN=11,IA=8,KS=6,KY=8,LA=8,ME=3,MD=7,MA=14,MI=18,MN=9,MS=6,MO=11,MT=2,NE=4,NV=1,NH=2,NJ=14,NM=2,NY=43,NC=12,ND=2,OH=23,OK=6,OR=4,PA=30,RI=2,SC=6,SD=2,TN=9,TX=22,UT=2,VT=1,VA=10,WA=7,WV=6,WI=10,WY=1,AK=1,HI=1)
A60=dict(AL=8,AK=1,AZ=3,AR=4,CA=38,CO=4,CT=6,DE=1,FL=12,GA=10,HI=2,ID=2,IL=24,IN=11,IA=7,KS=5,KY=7,LA=8,ME=2,MD=8,MA=12,MI=19,MN=8,MS=5,MO=10,MT=2,NE=3,NV=1,NH=2,NJ=15,NM=2,NY=41,NC=11,ND=2,OH=24,OK=6,OR=4,PA=27,RI=2,SC=6,SD=2,TN=9,TX=23,UT=2,VT=1,VA=10,WA=7,WV=5,WI=10,WY=1)
A70=dict(AL=7,AK=1,AZ=4,AR=4,CA=43,CO=5,CT=6,DE=1,FL=15,GA=10,HI=2,ID=2,IL=24,IN=11,IA=6,KS=5,KY=7,LA=8,ME=2,MD=8,MA=12,MI=19,MN=8,MS=5,MO=10,MT=2,NE=3,NV=1,NH=2,NJ=15,NM=2,NY=39,NC=11,ND=1,OH=23,OK=6,OR=4,PA=25,RI=2,SC=6,SD=2,TN=8,TX=24,UT=2,VT=1,VA=10,WA=7,WV=4,WI=9,WY=1)
APP={87:A50,**{c:A60 for c in range(88,93)},93:A70}
assert all(sum(a.values()) == (437 if c == 87 else 435) for c, a in APP.items())
NONSTATE={'PR','DC','GU','VI','AS','MP','PI','DK'}
def nm(p):
    n=p['name']; return n.get('official_full') or (n.get('nickname') or n['first'])+' '+n['last']
def holders(c, typ):
    d=OPEN[c]; out=collections.defaultdict(list)
    for p in L:
        for t in p['terms']:
            if t['type']==typ and str(t['start'])<=d<str(t['end']) and t['state'] not in NONSTATE:
                key=(t['state'], t.get('district') if typ=='rep' else t.get('class'))
                out[key].append((p,t))
    return out
def was_in(p, c, typ='rep'):
    d=OPEN[c-1] if c-1 in OPEN else '1959-01-07'
    return any(t['type']==typ and str(t['start'])<=d<str(t['end']) for t in p['terms'])

# ---------------------------------------------------------------- rosters
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from bib import store
from datetime import date, timedelta
PARTY = {'Democrat': 'D', 'Republican': 'R', 'Conservative': 'C', 'Independent': 'I', 'Ind. Democrat': 'ID'}
def name(p):
    n = p['name']
    first, mid, last, suf, nick = n['first'], n.get('middle'), n['last'], n.get('suffix'), n.get('nickname')
    if mid and first.endswith('.'):
        s = f"{last}, {first} {mid}"; nick = None if nick == mid else nick
    else:
        s = f"{last}, {first}" + (f" {mid[0]}." if mid and not mid.startswith('(') else '')
    if suf: s += f", {suf}"
    if nick and nick != first: s += f" ({nick})"
    return s
# a term counts if it began no later than ten days after the opening (some starts are recorded late)
def party_at(t, d):
    for a in t.get('party_affiliations') or []:
        if str(a['start']) <= d < str(a['end']):
            return a['party']
    return t['party']
def holders2(c, typ):
    d = OPEN[c]; d2 = (date.fromisoformat(d) + timedelta(days=10)).isoformat()
    out = collections.defaultdict(list)
    for p in L:
        for t in p['terms']:
            if t['type'] == typ and str(t['start']) <= d2 and d < str(t['end']) and t['state'] not in NONSTATE:
                if typ == 'rep' and str(t['start']) > d and str(t['start'])[5:7] != '01': continue
                out[(t['state'], t.get('district') if typ == 'rep' else t.get('class'))].append((p, t))
    return out
VACANT = {  # seats empty at the opening: (c, chamber, st, district/class) -> note
    (88, 'h', 'CA', 1): 'Vacant. Clem Miller (D) died Oct. 7, 1962, and was reelected posthumously; Don H. Clausen (R) elected Jan. 22, 1963.',
    (93, 'h', 'LA', 2): 'Vacant. Hale Boggs (D) lost in Alaska Oct. 16, 1972, reelected; Lindy Boggs (D) elected Mar. 20, 1973.',
    (93, 'h', 'AK', 0): 'Vacant. Nick Begich (D) lost with Boggs Oct. 16, 1972, reelected; Don Young (R) elected Mar. 6, 1973.',
    (93, 'h', 'IL', 7): 'Vacant. George W. Collins (D) died Dec. 8, 1972; Cardiss Collins (D) elected June 5, 1973.',
    (92, 's', 'GA', 2): 'Vacant. Richard B. Russell (D) died Jan. 21, 1971, hours before the 92nd convened; David H. Gambrell (D) appointed Feb. 1.',
}
ADD = {  # terms missing from the dataset
    (90, 'h', 'MO', 10): ('Jones, Paul C.', 'D', ('Jones', 'Paul', 'MO')),
    (90, 'h', 'NY', 38): ('Goodell, Charles E.', 'R', ('Goodell', 'Charles', 'NY')),
    (91, 's', 'IL', 3): ('Dirksen, Everett M.', 'R', ('Dirksen', 'Everett', 'IL')),
    (92, 's', 'VT', 1): ('Prouty, Winston L.', 'R', ('Prouty', 'Winston', 'VT')),
}
NOTE = {
    (90, 'h', 'NY', 18): 'Not seated at the opening; excluded Mar. 1, 1967. *Powell v. McCormack*, 395 U.S. 486 (1969).',
}
def find_id(q):
    last, first, st = q
    hits = [p for p in L if p['name']['last'] == last and p['name']['first'].startswith(first) and any(t['state'] == st for t in p['terms'])]
    assert len(hits) == 1, q
    return hits[0]['id']['bioguide']
for c in OPEN:
    H = holders2(c, 'rep'); S = holders2(c, 'sen')
    house, senate = [], []
    for st in sorted(APP[c]):
        nd = APP[c][st]
        dists = sorted({k[1] for k in H if k[0] == st})
        seats = []
        for d in dists:
            v = H[(st, d)]
            k = 1 if d else nd - len([x for x in dists if x])
            v = sorted(v, key=lambda pt: not was_in(pt[0], c))[:k]
            for p, t in v: seats.append((d, p, t))
        for d in range(1, nd + 1):
            pass
        rows = []
        for d, p, t in seats:
            key = (c, 'h', st, d)
            if key in VACANT:
                rows.append({'st': st, 'd': d, 'vacant': True, 'n': VACANT[key]}); continue
            r = {'st': st, 'd': d, 'name': name(p), 'party': PARTY[party_at(t, OPEN[c])], 'bio': p['id']['bioguide']}
            if key in NOTE: r['n'] = NOTE[key]
            rows.append(r)
        for key, (nm_, pa, bio) in ADD.items():
            if key[0] == c and key[1] == 'h' and key[2] == st:
                rows.append({'st': st, 'd': key[3], 'name': nm_, 'party': pa, 'bio': find_id(bio), 'n': 'Term missing from the source dataset; added by hand.'})
        for key, note in VACANT.items():
            if key[0] == c and key[1] == 'h' and key[2] == st and not any(r['d'] == key[3] for r in rows):
                rows.append({'st': st, 'd': key[3], 'vacant': True, 'n': note})
        rows.sort(key=lambda r: (r['d'], r.get('name', '')))
        # sanity: seat count
        if len(rows) != nd: print('SEATS', c, st, len(rows), nd)
        house += rows
        srows = []
        for (s2, cl), v in S.items():
            if s2 != st: continue
            for p, t in v:
                srows.append({'st': st, 'cl': cl, 'name': name(p), 'party': PARTY[party_at(t, OPEN[c])], 'bio': p['id']['bioguide']})
        for key, (nm_, pa, bio) in ADD.items():
            if key[0] == c and key[1] == 's' and key[2] == st:
                srows.append({'st': st, 'cl': key[3], 'name': nm_, 'party': pa, 'bio': find_id(bio), 'n': 'Term missing from the source dataset; added by hand.'})
        for key, note in VACANT.items():
            if key[0] == c and key[1] == 's' and key[2] == st:
                srows = [r for r in srows if r['cl'] != key[3]] + [{'st': st, 'cl': key[3], 'vacant': True, 'n': note}]
        srows.sort(key=lambda r: r['cl'])
        if len(srows) != 2: print('SEN', c, st, srows)
        senate += srows
    tally = lambda rows: dict(collections.Counter(r.get('party', 'vacant') for r in rows))
    print(c, len(house), tally(house), len(senate), tally(senate))
    store.dump_yaml({'congress': c, 'opened': OPEN[c], 'house': house, 'senate': senate},
                    os.path.join(ROOT, 'congress', f'{c}.yaml'),
                    header=[f'{c}th Congress at its opening, {OPEN[c]}. House by state and district (0 = at large); Senate by state and class.',
                            'From unitedstates/congress-legislators, corrected by hand where noted. Run ./bib build after editing.'])
