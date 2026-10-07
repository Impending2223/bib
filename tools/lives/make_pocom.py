"""POCOM (the Office of the Historian's Principal Officers and Chiefs of Mission) for the Lives: sources/pocom.json
and notes/pocom-matches.md.
# Usage: python3 tools/lives/make_pocom.py POCOM_DIR
#   POCOM_DIR: a clone of github.com/HistoryAtState/pocom.
#   Writes sources/pocom.json, {"match": {person key: POCOM id}, "persons": {POCOM id: {name, birth, death,
#   career, states, posts: [[label, appointed, began, ended, end note, note]]}}}, for the persons of the Lives
#   (tools/bib/lives.py, people) that POCOM holds; and notes/pocom-matches.md, the matches made by name with the
#   evidence for each, and those refused, for review.
#   Who is whom:
#   - a person the Executive roster already ties to POCOM (sources/executive-links.json, "pocom") is that record;
#   - anyone else by name (the fullest form of the person's name the series has): the surname, the forename (the
#     first given name in full or its initial, no short forms), a suffix that agrees (POCOM's "Jr." is not a name
#     written without one), a POCOM record no one else holds, and dates that fit: born at least 18 years before,
#     and not dead before, the first year the series shows the person at work (the roster, the Congresses, Part
#     III's role). Then evidence: the Directory's year of birth agrees with POCOM's (a year that differs refuses
#     it); or, without the Directory, both give a middle name or initial and they agree, or both give the same
#     suffix; or the first name alone, where the dates are known and fit and no other person on either side fits
#     (not where the series gives a middle initial POCOM lacks: 'John F. O'Leary' is not POCOM's John O'Leary);
#   - sources/pocom-matches.yaml, kept by hand, overrides: {person name: POCOM id, or null to refuse, or {id: POCOM
#     id, check: what to verify}}; a check is shown in the life as "Check: ...".
#   The build needs neither the clone nor the network.
"""
import glob, json, os, re, sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..'))
from bib import store  # noqa: E402
from bib import lives as L  # noqa: E402

ROOT = os.path.join(HERE, '..', '..')
OUT = os.path.join(ROOT, 'sources', 'pocom.json')
REPORT = os.path.join(ROOT, 'notes', 'pocom-matches.md')
HAND = os.path.join(ROOT, 'sources', 'pocom-matches.yaml')

# a country's name at the time of the post: (territory id, until, name) in order, else the id title-cased
ERA = {
    'russia': [('1917-11-07', 'Russia'), ('1991-12-25', 'Soviet Union'), ('9999', 'Russia')],
    'germany': [('1955-05-05', 'Germany'), ('1990-10-03', 'Germany (Federal Republic)'), ('9999', 'Germany')],
    'benin': [('1975-11-30', 'Dahomey'), ('9999', 'Benin')],
    'burkina-faso': [('1984-08-04', 'Upper Volta'), ('9999', 'Burkina Faso')],
    'sri-lanka': [('1972-05-22', 'Ceylon'), ('9999', 'Sri Lanka')],
    'congo-democratic-republic': [('1971-10-27', 'Congo (Léopoldville)'), ('1997-05-17', 'Zaire'),
                                  ('9999', 'Congo (Kinshasa)')],
    'congo-republic': [('9999', 'Congo (Brazzaville)')],
    'egypt': [('1958-02-22', 'Egypt'), ('1971-09-02', 'United Arab Republic'), ('9999', 'Egypt')],
    'malaysia': [('1963-09-16', 'Malaya'), ('9999', 'Malaysia')],
    'tanzania': [('1964-04-26', 'Tanganyika'), ('9999', 'Tanzania')],
    'myanmar': [('1989-06-18', 'Burma'), ('9999', 'Burma')],
    'iran': [('1935-03-21', 'Persia'), ('9999', 'Iran')],
    'thailand': [('1939-06-24', 'Siam'), ('9999', 'Thailand')],
    'cote-divoire': [('9999', 'Ivory Coast')],
    'samoa': [('1997-07-04', 'Western Samoa'), ('9999', 'Samoa')],
    'vietnam-south': [('9999', 'Viet-Nam')],
    'korea': [('1948-08-15', 'Korea'), ('9999', 'Korea (Republic of Korea)')],
    'china': [('1979-01-01', 'China'), ('9999', "China (People's Republic)")],
    'holy-see': [('9999', 'Holy See')],
    'cabo-verde': [('9999', 'Cape Verde')],
}
FIX = {'and': 'and', 'of': 'of', 'the': 'the'}
SHORT_ROLE = {'ambassador-e-p': 'Ambassador to', 'envoy-extraordinary-minister-plenipotentiary': 'Minister to',
              'minister-resident': 'Minister Resident in', 'charge-daffaires': "Chargé d'Affaires in",
              'charge-daffaires-ad-interim': "Chargé d'Affaires ad interim in"}
CAREER = {'career': 'Career Foreign Service officer', 'non-career': 'Non-career appointee',
          'both': 'Career Foreign Service officer and non-career appointee'}


def text(e, path):
    x = e.find(path)
    return (x.text or '').strip() if x is not None and x.text else ''


THE = {'Soviet Union', 'United Kingdom', 'Netherlands', 'Philippines', 'Holy See', 'Dominican Republic', 'Bahamas',
       'Gambia', 'Central African Republic', 'United Arab Emirates', 'United Arab Republic', 'Ivory Coast',
       'Marshall Islands', 'Maldives', 'Seychelles', 'Comoros', 'Solomon Islands', 'Czech Republic',
       'Slovak Republic', 'Kyrgyz Republic'}


def country(tid, day):
    """The country's name at the time of the post, with 'the' where English takes it."""
    tid = re.sub(r'-\d{4}$', '', tid)          # POCOM's 'yugoslavia-1946', 'south-vietnam-1975'
    name = next((n for until, n in ERA.get(tid, []) if (day or '0000') < until), None)
    name = name or ' '.join(FIX.get(w, w.capitalize()) for w in tid.split('-'))
    name = re.sub(r'^Congo (\w+)$', r'Congo (\1)', name)
    return f'the {name}' if name in THE or name.startswith('Congo') else name


def roles(pocom):
    out = {}
    for f in glob.glob(os.path.join(pocom, 'roles-country-chiefs', '*.xml')):
        r = ET.parse(f).getroot()
        out[text(r, 'id')] = text(r, 'names/singular')
    return out


def posts(pocom):
    """{person id: [[label, appointed, began, ended, end note, note]]}, every post POCOM gives."""
    R, out = roles(pocom), {}

    def add(c, label, principal=False):
        ap, st = text(c, 'appointed/date'), text(c, 'started/date') or text(c, 'arrived/date')
        began = st or (ap if principal else '')
        out.setdefault(text(c, 'person-id'), []).append(
            [re.sub(r'\s+', ' ', label), ap, began, text(c, 'ended/date'), text(c, 'ended/note'), text(c, 'note')])
    for f in glob.glob(os.path.join(pocom, 'missions-countries', '*.xml')):
        tid = os.path.basename(f)[:-4]
        for c in ET.parse(f).getroot().iter('chief'):
            role = text(c, 'role-title-id')
            day = text(c, 'started/date') or text(c, 'appointed/date')
            pre = SHORT_ROLE.get(role) or f"{R.get(role) or role.replace('-', ' ').title()} to"
            add(c, f'{pre} {country(text(c, "contemporary-territory-id") or tid, day)}')
    for f in glob.glob(os.path.join(pocom, 'missions-orgs', '*.xml')):
        r = ET.parse(f).getroot()
        name = re.sub(r'^Representative of the U\.S\.A\. to', 'Representative to', text(r, 'names/singular'))
        for c in r.iter('chief'):
            add(c, name)
    for f in glob.glob(os.path.join(pocom, 'positions-principals', '*.xml')):
        r = ET.parse(f).getroot()
        for c in r.iter('principal'):
            add(c, text(r, 'names/singular'), principal=True)
    for v in out.values():
        v.sort(key=lambda p: p[2] or p[1])
    return out


def records(pocom):
    out = {}
    for f in glob.glob(os.path.join(pocom, 'people', '*', '*.xml')):
        r = ET.parse(f).getroot()
        out[text(r, 'id')] = {'sur': text(r, 'persName/surname'), 'fore': text(r, 'persName/forename'),
                              'gen': text(r, 'persName/genName'), 'birth': text(r, 'birth'),
                              'death': text(r, 'death'), 'career': text(r, 'career-type'),
                              'states': [x.text for x in r.iter('state-id') if x.text]}
    return out


def bd_birth(p):
    e = L.bd_entry(p['sur'], p['given'], True, (), L.person_suffix(SERIES, p)[0])
    if not e or not L.roster_pointers(p['sur'], p['given'], p['names']):
        return None
    m = re.search(r'\bborn\b[^;]*?\b(1[89]\d\d)\b', e['text'])
    return m.group(1) if m else None


def gen_of(gen):
    return {'3rd': 'III', 'Jr.': 'Jr', 'Sr.': ''}.get(gen, gen)


def gen_ok(sfx, gen, bd):
    """The suffixes agree; POCOM's "Jr." against a name without one only where the Directory's year will decide."""
    g = gen_of(gen)
    return g == sfx if (g and sfx) else (not g or bd)


def fullest(p):
    """The person's given names in their fullest form in the series ('Nelson A.' over 'Nelson')."""
    return max((L.split_name(n)[1] for n in p['names']), key=lambda g: (len(L.gtoks(g)), len(g)))


def earliest(p, role):
    """The first year the series shows the person at work: the roster's offices, the Congresses, Part III's role."""
    ys = [str(h.get('from') or h.get('seen') or '')[:4] for u, o, h in L.holders_of(p['sur']) if h['name'] in p['names']]
    ys += [d[:4] for d, *_ in L.roster_pointers(p['sur'], p['given'], p['names'])]
    for n in p['names']:
        ys += re.findall(r'\b(19[0-7]\d)\b', role.get(n, ''))
    ys = [y for y in ys if re.fullmatch(r'\d{4}', y)]
    return min(ys) if ys else None


def dates_fit(r, first):
    if not first:
        return None
    if r['birth'] and int(r['birth']) > int(first) - 18:
        return False
    if r['death'] and r['death'] < first:
        return False
    return bool(r['birth'])


def first_ok(given, fore):
    a, b = (L.gtoks(given) or [''])[0], (L.gtoks(fore) or [''])[0]
    return a == b or (len(a) == 1 and b.startswith(a)) or (len(b) == 1 and a.startswith(b))


def main():
    global SERIES
    pocom = sys.argv[1]
    SERIES = store.Series()
    everyone = L.people(SERIES)
    recs, allposts = records(pocom), posts(pocom)
    links = json.load(open(os.path.join(ROOT, 'sources', 'executive-links.json'), encoding='utf-8')).get('pocom', {})
    hand = store.load_yaml(HAND) if os.path.exists(HAND) else {}
    hand = hand or {}
    match, taken, checks = {}, set(), {}
    for p in everyone:
        ids = sorted({links[n] for n in p['names'] if n in links and links[n] in recs})
        if ids:
            match[L.key_of(p['name'])] = ids[0]
            taken.update(ids)
    by_sur = {}
    for i, r in recs.items():
        by_sur.setdefault(L.fold(r['sur']), []).append(i)
    role = {}
    for l in SERIES.lists.values():
        for sec, e in l.entries():
            if (sec.code or '').startswith('III') and e.get('s'):
                for n in re.split(r';\s*', e['s']):
                    n = re.sub(r'\s*\(.*?\)\s*$', '', n).strip()
                    role[n] = role.get(n, '') + ' ' + (e.get('r') or '')
    fits = lambda p, i: (L.same_person(p['sur'], fullest(p), recs[i]['sur'], recs[i]['fore'])
                         and first_ok(fullest(p), recs[i]['fore'])
                         and gen_ok(L.person_suffix(SERIES, p)[0], recs[i]['gen'], bool(bd_birth(p)))
                         and dates_fit(recs[i], earliest(p, role)) is not False)
    cands = {}
    for p in everyone:
        k = L.key_of(p['name'])
        if k in match:
            continue
        c = [i for i in by_sur.get(L.fold(p['sur']), []) if i not in taken and fits(p, i)]
        if c:
            cands[k] = (p, c)
    holders = {}
    for k, (p, c) in cands.items():
        for i in c:
            holders.setdefault(i, []).append(k)
    accepted, refused = [], []
    for k, (p, c) in sorted(cands.items()):
        if p['name'] in hand:
            h = hand[p['name']]
            i, note = (h.get('id'), h.get('check')) if isinstance(h, dict) else (h, None)
            (accepted if i else refused).append((p['name'], i or c[0], 'by hand' + (f'; check: {note}' if note else '')
                                                 if i else 'refused by hand' + (f': {note}' if note else '')))
            if i:
                match[k] = i
                if note:
                    checks[k] = note
            continue
        if len(c) > 1:
            refused.append((p['name'], ', '.join(c), 'more than one POCOM record fits'))
            continue
        i, r = c[0], recs[c[0]]
        born, g, first = bd_birth(p), fullest(p), earliest(p, role)
        sfx = L.person_suffix(SERIES, p)[0]
        if born:
            if born == r['birth']:
                why = f"born {born}, the Directory and POCOM"
            else:
                refused.append((p['name'], i, f"born {born} (the Directory), {r['birth'] or 'not given'} (POCOM)"))
                continue
        elif len(holders[i]) > 1:
            refused.append((p['name'], i, 'the record fits ' + '; '.join(holders[i])))
            continue
        elif len(L.gtoks(g)) > 1 and len(L.gtoks(r['fore'])) > 1:
            why = f"{g} and {r['fore']}: the middle names agree"
        elif sfx and sfx == gen_of(r['gen']):
            why = f"{g}, {sfx}, and {r['fore']}, {r['gen']}: the suffixes agree"
        elif dates_fit(r, first) and not (len(L.gtoks(g)) > 1 and len(L.gtoks(r['fore'])) == 1):
            why = f"{g} and {r['fore']}: the first name alone, and no one else on either side; born {r['birth']}, at work {first}"
        else:
            refused.append((p['name'], i, f"{g} and {r['fore']}: nothing beyond the first name, and "
                            + (f"no year of work in the series" if not first else f"born {r['birth'] or '?'}")))
            continue
        accepted.append((p['name'], i, why))
        match[k] = i
    used = set(match.values())
    persons = {}
    for i in sorted(used):
        r = recs[i]
        persons[i] = {'name': f"{r['fore']} {r['sur']}" + (f", {r['gen']}" if r['gen'] else ''), 'birth': r['birth'],
                      'death': r['death'], 'career': CAREER.get(r['career'], ''), 'states': r['states'],
                      'posts': allposts.get(i, [])}
    json.dump({'match': match, 'persons': persons, 'check': checks}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False,
              separators=(',', ':'))
    url = 'https://history.state.gov/departmenthistory/people/'
    lines = ['# POCOM matches by name', '',
             'Made by tools/lives/make_pocom.py: the persons of the Lives that the Executive roster does not already '
             'tie to POCOM, matched by name, with the evidence. Override in sources/pocom-matches.yaml '
             '(`Name: pocom-id`, or `Name: null` to refuse); then rerun the script.', '',
             f'{len(match) - len(accepted)} persons tied through the roster; {len(accepted)} matched by name; '
             f'{len(refused)} refused.', '', '## Matched', '']
    lines += [f'- {n} = [{i}]({url}{i}) ({recs[i]["fore"]} {recs[i]["sur"]}, {recs[i]["birth"] or "?"}–'
              f'{recs[i]["death"]}): {w}' for n, i, w in accepted]
    lines += ['', '## Refused', '']
    lines += [f'- {n}: {i}: {w}' for n, i, w in refused]
    open(REPORT, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(len(match), 'persons;', len(accepted), 'by name;', len(refused), 'refused', file=sys.stderr)


if __name__ == '__main__':
    main()
