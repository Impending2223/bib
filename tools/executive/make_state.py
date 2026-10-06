"""Seed executive/state.yaml and executive/missions.yaml from POCOM, once.
# Usage: python3 tools/executive/make_state.py POCOM_DIR [--missions-only]
#   POCOM_DIR: a clone of github.com/HistoryAtState/pocom (the Office of the Historian's Principal Officers
#   and Chiefs of Mission). Writes the State Department's principal officers and every chief of mission who
#   served between Jan. 20, 1953, and Aug. 31, 1974. One-time: the files are kept by hand afterwards (titles of
#   the period, nominations, acting officers, the law), so rerunning overwrites that work. --missions-only
#   rewrites missions.yaml alone.
#
#   POCOM's dates: appointed, the commission (a recess commission where its note says so; the recommission
#   after confirmation from the note); started, the oath or entry on duty, for a chief of mission the
#   presentation of credentials; ended, the day the tenure ended, with its note ("Left post"). A chief who
#   never served (declined, not commissioned) is left out. Chargés d'affaires ad interim are acting.
"""
import datetime, glob, os, re, sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bib import store  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'executive')
LO, HI = '1953-01-20', '1974-08-31'
MONTHS = {m: i for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                       'September', 'October', 'November', 'December'], 1)}

# Positions in POCOM -> (office id, title in the period, rank, appt, group); the titles' changes in TITLES.
POSITIONS = [
    ('secretary', 'secretary', 'Secretary of State', 'head', 'PAS', None),
    ('under-secretary', 'under-secretary', 'Under Secretary of State', 'principal', 'PAS', None),
    ('deputy-secretary', 'deputy-secretary', 'Deputy Secretary of State', 'principal', 'PAS', None),
    ('under-secretary-for-political-affairs', 'under-secretary-political', 'Under Secretary of State for Political Affairs', 'principal', 'PAS', None),
    ('under-secretary-for-econ-business-ag', 'under-secretary-economic', 'Under Secretary of State for Economic Affairs', 'principal', 'PAS', None),
    ('under-secretary-for-mgmt', 'under-secretary-management', 'Under Secretary of State for Management', 'principal', 'PAS', None),
    ('under-secretary-for-arms-control', 'under-secretary-security', 'Under Secretary of State for Security Assistance', 'principal', 'PAS', None),
    ('deputy-under-secretary', 'deputy-under-secretary', 'Deputy Under Secretary of State', 'principal', 'PAS', None),
    ('deputy-under-secretary-for-political-affairs', 'deputy-under-secretary-political', 'Deputy Under Secretary of State for Political Affairs', 'principal', 'PAS', None),
    ('deputy-under-secretary-for-economic-affairs', 'deputy-under-secretary-economic', 'Deputy Under Secretary of State for Economic Affairs', 'principal', 'PAS', None),
    ('deputy-under-secretary-for-mgmt', 'deputy-under-secretary-administration', 'Deputy Under Secretary of State for Administration', 'principal', 'PAS', None),
    ('counselor', 'counselor', 'Counselor of the Department of State', 'principal', 'PAS', None),
    ('ambassador-at-large', 'ambassador-at-large', 'Ambassador at Large', 'principal', 'PAS', None),
    ('assistant-secretary-for-african-affairs', 'assistant-secretary-african', 'Assistant Secretary of State for African Affairs', 'principal', 'PAS', 'Regional bureaus'),
    ('assistant-secretary-for-european-affairs', 'assistant-secretary-european', 'Assistant Secretary of State for European Affairs', 'principal', 'PAS', 'Regional bureaus'),
    ('assistant-secretary-for-east-asian-pacific-affairs', 'assistant-secretary-far-eastern', 'Assistant Secretary of State for Far Eastern Affairs', 'principal', 'PAS', 'Regional bureaus'),
    ('assistant-secretary-for-western-hemisphere', 'assistant-secretary-inter-american', 'Assistant Secretary of State for Inter-American Affairs', 'principal', 'PAS', 'Regional bureaus'),
    ('assistant-secretary-for-near-eastern-affairs', 'assistant-secretary-near-eastern', 'Assistant Secretary of State for Near Eastern, South Asian, and African Affairs', 'principal', 'PAS', 'Regional bureaus'),
    ('assistant-secretary-international-organization-affairs', 'assistant-secretary-international-organization', 'Assistant Secretary of State for International Organization Affairs', 'principal', 'PAS', 'Functional bureaus'),
    ('assistant-secretary-for-economic-business-affairs', 'assistant-secretary-economic', 'Assistant Secretary of State for Economic Affairs', 'principal', 'PAS', 'Functional bureaus'),
    ('assistant-secretary-for-public-affairs', 'assistant-secretary-public', 'Assistant Secretary of State for Public Affairs', 'principal', 'PAS', 'Functional bureaus'),
    ('assistant-secretary-legislative-affairs', 'assistant-secretary-congressional', 'Assistant Secretary of State for Congressional Relations', 'principal', 'PAS', 'Functional bureaus'),
    ('assistant-secretary-for-educational-cultural-affairs', 'assistant-secretary-educational-cultural', 'Assistant Secretary of State for Educational and Cultural Affairs', 'principal', 'PAS', 'Functional bureaus'),
    ('assistant-secretary-for-administration', 'assistant-secretary-administration', 'Assistant Secretary of State for Administration', 'principal', 'PAS', 'Functional bureaus'),
    ('assistant-secretary-consular-affairs', 'administrator-security-consular', 'Administrator, Bureau of Security and Consular Affairs', 'principal', 'PAS', 'Functional bureaus'),
    ('assistant-secretary-intelligence-research', 'director-intelligence-research', 'Director of Intelligence and Research', 'inferior', 'HD', 'Functional bureaus'),
    ('assistant-secretary-for-politico-military-affairs', 'director-politico-military', 'Director, Bureau of Politico-Military Affairs', 'inferior', 'HD', 'Functional bureaus'),
    ('assistant-secretary2', 'assistant-secretary', 'Assistant Secretary of State', 'principal', 'PAS', 'Functional bureaus'),
    ('legal-adviser', 'legal-adviser', 'Legal Adviser', 'principal', 'PAS', 'Staff offices'),
    ('director-policy-planning', 'director-policy-planning', 'Director of the Policy Planning Staff', 'inferior', 'HD', 'Staff offices'),
    ('executive-secretary', 'executive-secretary', 'Executive Secretary of the Department', 'inferior', 'HD', 'Staff offices'),
    ('chief-of-protocol', 'chief-of-protocol', 'Chief of Protocol', 'inferior', 'PA', 'Staff offices'),
    ('director-general-foreign-service', 'director-general', 'Director General of the Foreign Service', 'inferior', 'HD', 'Staff offices'),
    ('inspector-general', 'inspector-general', 'Inspector General of the Foreign Service', 'inferior', 'HD', 'Staff offices'),
    ('director-foreign-service-institute', 'director-fsi', 'Director of the Foreign Service Institute', 'inferior', 'HD', 'Staff offices'),
    ('director-mutual-security-agency', 'director-msa', 'Director for Mutual Security', 'head', 'PAS', 'Foreign assistance'),
    ('director-foreign-operations-administration', 'director-foa', 'Director of the Foreign Operations Administration', 'head', 'PAS', 'Foreign assistance'),
    ('administrator-technical-cooperation-administration', 'administrator-tca', 'Administrator of the Technical Cooperation Administration', 'inferior', 'HD', 'Foreign assistance'),
    ('director-intl-cooperation-administration', 'director-ica', 'Director of the International Cooperation Administration', 'principal', 'PAS', 'Foreign assistance'),
    ('inspector-general-foreign-assistance', 'inspector-general-foreign-assistance', 'Inspector General, Foreign Assistance', 'principal', 'PAS', 'Foreign assistance'),
    ('deputy-inspector-general-foreign-assistance', 'deputy-inspector-general-foreign-assistance', 'Deputy Inspector General, Foreign Assistance', 'inferior', 'HD', 'Foreign assistance'),
    ('administrator-aid', 'administrator-aid', 'Administrator of the Agency for International Development', 'principal', 'PAS', 'Foreign assistance'),
    ('secretary-ad-interim', 'secretary-ad-interim', 'Secretary of State ad interim', 'principal', 'DES', None),
]
SEPARATE = {  # positions seeded into their own units
    'director-usia': ('usia', 'United States Information Agency', 'director', 'Director of the United States Information Agency'),
    'director-us-arms-control-disarmament-agency': ('acda', 'United States Arms Control and Disarmament Agency', 'director',
                                                    'Director of the United States Arms Control and Disarmament Agency'),
    'us-trade-representative': ('str', 'Office of the Special Representative for Trade Negotiations', 'special-representative',
                                'Special Representative for Trade Negotiations'),
}

# The regional bureaus of the 1960s, for grouping the missions.
REGION = {}
for r, cs in {
    'American Republics': 'argentina bolivia brazil chile colombia costa-rica cuba dominican-republic ecuador el-salvador '
                          'guatemala haiti honduras mexico nicaragua panama paraguay peru uruguay venezuela jamaica '
                          'trinidad-and-tobago barbados guyana bahamas representative-to-oas',
    'Europe': 'austria belgium bulgaria canada czechoslovakia denmark finland france germany hungary iceland ireland italy '
              'luxembourg malta netherlands norway poland portugal romania russia spain sweden switzerland united-kingdom '
              'yugoslavia holy-see representative-to-nato representative-to-oecd representative-to-eu',
    'Far East': 'australia burma cambodia china fiji indonesia japan korea laos malaysia new-zealand philippines samoa '
                'singapore thailand tonga vietnam-south',
    'Near East and South Asia': 'afghanistan bahrain bangladesh cyprus egypt greece india iran iraq israel jordan kuwait '
                                'lebanon maldives nepal oman pakistan qatar saudi-arabia sri-lanka syria turkey '
                                'united-arab-emirates yemen',
    'Africa': 'algeria benin botswana burkina-faso burundi cameroon central-african-republic chad congo-democratic-republic '
              'congo-republic cote-divoire equatorial-guinea ethiopia gabon gambia ghana guinea kenya lesotho liberia libya '
              'madagascar malawi mali mauritania mauritius morocco niger nigeria rwanda senegal sierra-leone somalia '
              'south-africa sudan swaziland tanzania togo tunisia uganda zambia',
    'International organizations': 'representative-to-un representative-uneo representative-to-unesco representative-to-iaea '
                                   'representative-to-icao representative-to-unafa representative-unvo',
}.items():
    for c in cs.split():
        REGION[c] = r
ORDER = ['International organizations', 'American Republics', 'Europe', 'Far East', 'Near East and South Asia', 'Africa']
NAMES = {'russia': 'Soviet Union', 'china': 'China (Republic of China)', 'korea': 'Korea (Republic of Korea)',
         'vietnam-south': 'Viet-Nam', 'germany': 'Germany (Federal Republic)', 'burkina-faso': 'Upper Volta',
         'benin': 'Dahomey', 'sri-lanka': 'Ceylon', 'cote-divoire': 'Ivory Coast', 'samoa': 'Western Samoa',
         'congo-democratic-republic': 'Congo (Léopoldville; Zaire from 1971)', 'congo-republic': 'Congo (Brazzaville)',
         'egypt': 'Egypt (United Arab Republic, 1958–71)', 'malaysia': 'Malaya; Malaysia from 1963',
         'tanzania': 'Tanganyika; Tanzania from 1964', 'holy-see': 'Holy See', 'united-kingdom': 'United Kingdom',
         'trinidad-and-tobago': 'Trinidad and Tobago', 'saudi-arabia': 'Saudi Arabia', 'new-zealand': 'New Zealand',
         'south-africa': 'South Africa', 'el-salvador': 'El Salvador', 'costa-rica': 'Costa Rica',
         'dominican-republic': 'Dominican Republic', 'sierra-leone': 'Sierra Leone', 'equatorial-guinea': 'Equatorial Guinea',
         'central-african-republic': 'Central African Republic', 'united-arab-emirates': 'United Arab Emirates',
         'representative-to-un': 'United Nations', 'representative-to-oas': 'Organization of American States',
         'representative-to-nato': 'North Atlantic Treaty Organization',
         'representative-to-oecd': 'Organization for Economic Cooperation and Development (OEEC to 1961)',
         'representative-to-eu': 'European Communities', 'representative-uneo': 'United Nations European Office, Geneva',
         'representative-to-unesco': 'UNESCO', 'representative-to-iaea': 'International Atomic Energy Agency',
         'representative-to-icao': 'International Civil Aviation Organization',
         'representative-to-unafa': 'United Nations agencies for food and agriculture, Rome',
         'representative-unvo': 'United Nations, Vienna'}
ROLE = {'ambassador-e-p': None, 'envoy-extraordinary-minister-plenipotentiary': 'Envoy Extraordinary and Minister Plenipotentiary',
        'charge-daffaires-ad-interim': "Chargé d'Affaires ad interim", 'charge-daffaires': "Chargé d'Affaires",
        'personal-representative-of-the-president': 'Personal Representative of the President',
        'diplomatic-agent-consul-general': 'Diplomatic Agent and Consul General', 'principal-officer': 'Principal Officer',
        'chief': None}
END_NOTE = {'Left post on': 'Left post.', 'Presented recall on': 'Presented recall.', 'Died at post on': 'Died at post.',
            'Relinquished charge': 'Relinquished charge.', 'Superseded': 'Superseded.', 'Left post on or soon after': 'Left post.'}


def text(e, path):
    x = e.find(path)
    return re.sub(r'\s+', ' ', (x.text or '')).strip() if x is not None and x.text else ''


def part3():
    """fold(surname) -> [given as Part III writes it]: the series' own forms of names."""
    out = {}
    for lst in store.Series().lists.values():
        for sec, e in lst.entries():
            if sec.code.startswith('III') and e.get('s') and ',' in e['s']:
                sur, given = (x.strip() for x in re.sub(r'\s*\([^)]*\)', '', e['s']).split(',')[:2])
                out.setdefault(store.fold(sur), []).append(given)
    return out


def fits(short, full):
    """Could 'W. Averell' or 'Dean' be a short form of 'William Averell' or 'David Dean'? Each word of the short form
    matches a word of the full one, in order: the same word, or its initial."""
    sw, fw = short.replace('.', '. ').split(), full.replace('.', '. ').split()
    i = 0
    for w in sw:
        while i < len(fw) and not (fw[i].rstrip('.').lower() == w.rstrip('.').lower() or
                                   (w.endswith('.') and fw[i][0].lower() == w[0].lower())):
            i += 1
        if i == len(fw):
            return False
        i += 1
    return bool(sw)


def short(fore, alt, sur):
    """The usual form of the given names: the altname's ('Dean Rusk' -> 'Dean'), else the first full name and the
    initials of the rest ('Charles Burke' -> 'Charles B.'; 'C. Douglas' stays)."""
    if alt and sur in alt:
        g = alt[:alt.rfind(sur)].strip(' ,')
        if g:
            return g
    w = fore.split()
    out = []
    for i, x in enumerate(w):
        if out and any(len(y.rstrip('.')) > 1 for y in out):
            out.append(x[0] + '.')
        else:
            out.append(x)
    return ' '.join(out)


def people(pocom):
    P3 = part3()
    out = {}
    for f in glob.glob(os.path.join(pocom, 'people', '*', '*.xml')):
        r = ET.parse(f).getroot()
        sur, fore, gen = text(r, 'persName/surname'), text(r, 'persName/forename'), text(r, 'persName/genName')
        alt = text(r, 'persName/altname')
        given = next((g for g in P3.get(store.fold(sur), []) if fits(g, fore)), None) or short(fore, alt, sur)
        out[text(r, 'id')] = (f'{sur}, {given}' + (f', {gen}' if gen else ''), fore if fore != given else None)
    return out


def recommission(note):
    m = re.search(r'recommissioned[^.]*? on (\w+) (\d+), (\d{4})', note or '')
    if m and m.group(1) in MONTHS:
        return f'{m.group(3)}-{MONTHS[m.group(1)]:02d}-{int(m.group(2)):02d}'
    return None


def tenure(c, person):
    who, full = person
    appointed, started, ended = text(c, 'appointed/date'), text(c, 'started/date'), text(c, 'ended/date')
    note = text(c, 'note')
    begin = started or text(c, 'arrived/date') or (appointed if 'designated' in note.lower() or c.tag == 'principal' else '')
    if not begin or begin > HI or (ended and ended < LO):
        return None
    h = {'name': who}
    if full:
        h['given'] = full
    role = text(c, 'role-title-id')
    if role == 'charge-daffaires-ad-interim':
        h['acting'] = True
    elif ROLE.get(role):
        h['title'] = ROLE[role]
    if appointed and not h.get('acting'):
        if 'recess of the Senate' in note:
            h['recess'] = appointed
            rc = recommission(note)
            if rc:
                h['appointed'] = rc
        else:
            h['appointed'] = appointed
    h['from'] = begin
    if ended:
        h['to'] = ended
        en = text(c, 'ended/note')
        if END_NOTE.get(en):
            h['out'] = END_NOTE[en]
    if note:
        h['n'] = note.rstrip('.') + '.'
    h['src'] = ['POCOM']
    return h


def missions(pocom, P):
    groups = {r: [] for r in ORDER}
    files = sorted(glob.glob(os.path.join(pocom, 'missions-countries', '*.xml')) +
                   glob.glob(os.path.join(pocom, 'missions-orgs', '*.xml')))
    for f in files:
        key = os.path.basename(f)[:-4]
        r = ET.parse(f).getroot()
        hs = [h for h in (tenure(c, P.get(text(c, 'person-id'), (text(c, 'person-id'), None))) for c in r.iter('chief')) if h]
        if not hs:
            continue
        hs.sort(key=lambda h: h['from'])
        title = NAMES.get(key, key.replace('-', ' ').title())
        oid = re.sub(r'^representative-(to-)?', '', key)
        groups[REGION.get(key, 'Europe')].append({'id': oid, 'title': title, 'rank': 'principal', 'appt': 'PAS',
                                                   'group': REGION.get(key, 'Europe'), 'holders': hs})
    offices = []
    for r in ORDER:
        offices += sorted(groups[r], key=lambda o: (o['id'] != 'un', o['title']))
    unit = {'unit': 'missions', 'name': 'Chiefs of mission', 'under': 'state', 'order': 90,
            'law': [{'act': 'Foreign Service Act of 1946', 'date': '1946-08-13', 'cite': 'ch. 957, §§ 401, 411, 60 Stat. 999, 1002, 1004',
                     'usc': '22 U.S.C. §§ 841, 901 (1958)',
                     'does': 'Chiefs of mission appointed by the President, by and with the advice and consent of the Senate; '
                             'the classes of chief of mission.'}],
            'n': 'Every chief of mission who served between Jan. 20, 1953, and Aug. 31, 1974, from POCOM. Grouped by the '
                 'regional bureaus of the 1960s. Chargés d\'affaires ad interim are acting. Took office: the presentation of '
                 'credentials. Nominations and confirmations are not given here.',
            'offices': offices}
    store.dump_yaml(unit, os.path.join(OUT, 'missions.yaml'),
                    header=['The chiefs of mission, 1953-74. Seeded from POCOM by tools/executive/make_state.py; kept by hand since.',
                            'See tools/bib/executive.py for the fields. Run ./bib executive check after editing.'])


def state(pocom, P):
    offices = []
    extra = {}
    for f in sorted(glob.glob(os.path.join(pocom, 'positions-principals', '*.xml'))):
        key = os.path.basename(f)[:-4]
        r = ET.parse(f).getroot()
        hs = [h for h in (tenure(c, P.get(text(c, 'person-id'), (text(c, 'person-id'), None))) for c in r.iter('principal')) if h]
        if not hs:
            continue
        hs.sort(key=lambda h: h['from'])
        if key in SEPARATE:
            extra[key] = hs
            continue
        pos = next((p for p in POSITIONS if p[0] == key), None)
        if not pos:
            continue
        _, oid, title, rank, appt, group = pos
        o = {'id': oid, 'title': title, 'rank': rank, 'appt': appt}
        if group:
            o['group'] = group
        if oid != 'secretary':
            o['under'] = 'secretary'
        if oid in ('secretary-ad-interim', 'ambassador-at-large'):
            o['many'] = True
        o['holders'] = hs
        offices.append((POSITIONS.index(pos), o))
    offices = [o for _, o in sorted(offices, key=lambda x: x[0])]
    unit = {'unit': 'state', 'name': 'Department of State', 'under': 'president', 'order': 30, 'offices': offices}
    store.dump_yaml(unit, os.path.join(OUT, 'state.yaml'),
                    header=['The Department of State. Seeded from POCOM by tools/executive/make_state.py; kept by hand since.',
                            'See tools/bib/executive.py for the fields. Run ./bib executive check after editing.'])
    for key, hs in extra.items():
        uk, name, oid, title = SEPARATE[key]
        unit = {'unit': uk, 'name': name, 'under': 'president', 'order': 500,
                'offices': [{'id': oid, 'title': title, 'rank': 'head', 'appt': 'PAS', 'holders': hs}]}
        store.dump_yaml(unit, os.path.join(OUT, f'{uk}.yaml'),
                        header=[f'{name}. Seeded from POCOM by tools/executive/make_state.py; kept by hand since.',
                                'See tools/bib/executive.py for the fields. Run ./bib executive check after editing.'])


if __name__ == '__main__':
    pocom = sys.argv[1]
    P = people(pocom)
    os.makedirs(OUT, exist_ok=True)
    missions(pocom, P)
    if '--missions-only' not in sys.argv:
        state(pocom, P)
