"""Every FRUS document that names a person, and those the person sent: sources/frus-names/<letter>.json.
# Usage: python3 tools/lives/frus_names.py FRUS_GIT [--all | 'Surname, Given' ...]
#   --all: everyone with a Lives entry (tools/bib/lives.py, people)
#   FRUS_GIT  a clone of github.com/HistoryAtState/frus (blobs present or fetchable)
#   Reads every volume 1952-54 to 1969-76: the volume's list of persons gives the person's xml:id; a document
#   names the person where its text links a persName to that id (corresp); the person sent it where the
#   daybook's rules for authors (tools/daybook/make_daybook.py, "authors as persons") give the person.
#   Writes, by the first letter of the surname, {person key: {volume: {"named": [[doc number, date]], "sent":
#   [[doc number, date, heading]], "role": the list's description of the person}}}, and
#   sources/frus-names/volumes.json, {volume: its title}.
#   --all also gives every person a list holds whom no name entry holds an entry of his own (join: one a person
#   across the volumes), written to sources/frus-names/persons.json, {key: {name, names}}; tools/bib/lives.py
#   (everyone) adds them to the Names.
"""
import json, os, re, subprocess, sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'daybook'))
sys.path.insert(0, os.path.join(HERE, '..'))
import make_daybook as M  # noqa: E402
from bib.executive_names import compatible  # noqa: E402

OUT = os.path.join(HERE, '..', '..', 'sources', 'frus-names')
SUBS = ('frus1952-54', 'frus1955-57', 'frus1958-60', 'frus1961-63', 'frus1964-68', 'frus1969-76')


def volumes(git):
    names = subprocess.run(['git', '-C', git, 'ls-tree', '--name-only', 'HEAD', 'volumes/'], capture_output=True,
                           text=True).stdout.split()
    return [n for n in names if n.endswith('.xml') and os.path.basename(n).startswith(SUBS)]


def key(name):
    return re.sub(r'[^a-z]+', '-', M.clean(name).lower()).strip('-')


def sfx_of(given):
    m = re.search(r'\b(Jr|II|III|IV)\b\.?\s*$', re.sub(r'\s*\([^)]*\)', '', given))
    return m.group(1) if m else ''


# Misprints in a volume's list of persons, by volume and xml:id: the name as it should read. FRUS 1961-63, VII and XVI
# print 'Stevenson, Adlai E., III' for the Permanent Representative to the United Nations, 1961-65: the father (VII's
# own xml:id, 'p_SAEII1', says II); the son, the Senator, is III in the 1969-76 volumes.
ERRATA = {('frus1961-63v07', 'p_SAEII1'): ('Stevenson', 'Adlai E.', ''),
          ('frus1961-63v16', 'p_SAEIII1'): ('Stevenson', 'Adlai E.', '')}


def fits(given, listed):
    """A target's given names and a list's agree: the first name alike (compatible, the same first word), and where
    both give further names or initials after it, each of the fewer among the other's by its initial, in order
    ('John W.' is not 'John G.'; 'John G.' is 'John Gunther'). The suffix is judged apart."""
    if not (compatible(given, listed) and M.first_word(listed) == M.first_word(given)):
        return False
    def rest(g):
        ws = [w.strip('.,') for w in re.sub(r'\s*\([^)]*\)', '', g).split()]
        ws = [w for w in ws if w and not re.fullmatch(r'(Jr|Sr|II|III|IV)', w)]
        f = M.first_word(g)
        return [w[0].lower() for w in ws[ws.index(f) + 1:]] if f in ws else []
    a, b = rest(given), rest(listed)
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    it = iter(long_)
    return all(x in it for x in short)


def flat(t):
    """A name for comparing forms: its parentheses dropped, folded, lower case, hyphens as spaces."""
    from bib.store import fold
    t = re.sub(r'\s*\([^)]*\)', '', M.clean(t))
    return re.sub(r'[\s-]+', ' ', fold(t).lower()).strip(' ,')


def natural_hit(p, role, naturals):
    """A natural-order name (tools/bib/lives.py, natural) in a list: its whole name, or the name before a title,
    is one of the person's forms ('Mao Tse-tung', 'Souvanna Phouma, Prince'), or the name and what follows the
    comma is ('Diem, Ngo Dinh'). Not a wife listed under her husband's name ('Ngo Dinh Nhu, Madame')."""
    n0 = len(re.sub(r'\s*\([^)]*\)', '', M.clean(p[0])))
    head = re.sub(r'\s*\([^)]*\)', '', role)[n0:n0 + 12]
    wife = re.match(r'\s*,?\s*(Madame|Mme\.?|Mrs\.)', head)
    if wife:                          # 'Ngo Dinh Nhu, Madame (Tran Le Xuan)': her forms only
        return naturals.get(flat(p[0] + ', Madame'))
    for f in (flat(p[0] + (', ' + p[1] if p[1] else '')), flat(p[0]), flat(p[1] + ' ' + p[0]) if p[1] else ''):
        if f in naturals:
            return naturals[f]
    return None


def skey(sur):
    """A surname for looking up: diacritics folded, one apostrophe, lower case ('O’Neill', 'Iklé')."""
    from bib.store import fold
    return fold(re.sub(r'\s*\([^)]*\)', '', M.clean(sur))).replace('’', "'").lower().strip()


NOT_NAMES = {'pacific', 'atlantic', 'europe', 'tunku', 'tengku'}


def descriptions(root):
    """{xml:id: the description the volume's list of persons gives after the name} ('Ambassador to Laos')."""
    out = {}
    for item in root.iter(M.T + 'item'):
        pns = [pn for pn in item.iter(M.T + 'persName') if pn.get(M.XID)]
        if len(pns) != 1:                    # a list within the item, or no one: the inner items give theirs
            continue
        full = M.clean(''.join(item.itertext()))
        for pn in pns:
            if pn.get(M.XID) and pn.get(M.XID) not in out:
                raw = M.clean(''.join(pn.itertext()))
                d = full[len(raw):] if full.startswith(raw) else full.replace(raw, '', 1)
                out[pn.get(M.XID)] = d.strip(' ,.;:—–-')
    return out


TITLES = re.compile(r'^(?:(?:' + M.RANK + r'|Cmdr\.?|Cdr|Brig|Gen|Lt|Col|Capt|Adm|Maj|Mme\.?|Madame|Mlle\.?|'
                    r'Sen\.|Rep\.|Gov\.|Amb\.|Hon\.|The Honorable|Count|Countess|Baron|Marquis|Duke|King|Queen|'
                    r'President|Premier|Chairman|Minister|Viscount|Tiao|Representative|Governor|Mayor|Congressman|'
                    r'Pandit|Brigadier|Lieut|Lt\. Gen|[Oo]f [Tt]he (?:Army|Air Force|Navy))\.?(?:\s+|$))+')
OFFICE = set('''deputy commanding general director secretary minister ambassador chief assistant counselor counsellor
officer representative commander head member chairman president vice prime foreign under special acting consul
delegate adviser advisor attache attaché administrator governor senator staff executive embassy department office
army navy air force corps division mission group council committee bureau agency state defense defence affairs
section branch desk king queen prince princess emperor shah premier leader party national first second third
french british soviet indian chinese german japanese italian israeli egyptian american canadian australian korean
vietnamese lao laotian thai cambodian burmese indonesian pakistani iranian turkish greek spanish portuguese
brazilian mexican cuban argentine chilean dutch belgian norwegian swedish danish polish czech hungarian
yugoslav romanian bulgarian arab saudi jordanian syrian iraqi lebanese libyan moroccan algerian tunisian
nigerian ghanaian congolese kenyan ethiopian south north east west republic kingdom united nations un nato
oas seato cento cia usia aid fbi nsc jcs director-general secretary-general undersecretary'''.split())
SERVICE = re.compile(r'\b(?:USA|USAF|USN|USMC|USCG|RN|RAF|ret\.?)\b,?')


def loose(given, others):
    """A listed given name another person of the surname may answer to: the first names alike, by initial or short
    form ('J. Kenneth' and 'John Kenneth'; 'Michael' and 'Mike'), or the listed first name among the other's names
    ('Stuart' and 'W. Stuart', 'William S.'), or the other's first name among the listed ('Thomas Hale' and 'Hale'), or the first letters and the middle initials alike (a misprint: 'Herbert H.'
    for 'Hubert H.'). There the list's person is not given an entry of his own: he may be that person."""
    from bib.lives import gtoks, nick
    A = gtoks(given)
    if not A:
        return False
    for g in others:
        B = gtoks(g)
        if B and (A[0] == B[0] or (len(A[0]) == 1 and B[0].startswith(A[0])) or (len(B[0]) == 1 and A[0].startswith(B[0]))
                  or nick(A[0], B[0]) or A[0] in B[1:] or (len(B[0]) > 1 and B[0] in A[1:])
                  or any(len(x) == 1 and A[0].startswith(x) for x in B[1:])
                  or (A[0][0] == B[0][0] and len(A) > 1 and len(B) > 1 and A[1][0] == B[1][0])):
            return True
    return False


def recover(p, d):
    """(name, description) where the list's persName holds the surname alone and the given names follow it in the
    text ('Bagley' and 'Lieutenant Commander Worth H., USN, Naval Aide ...'): the given names taken from the text,
    titles and ranks dropped, where the words before the first comma are names (capitalized words and initials, no
    more than four); the description is what follows them. A rank or title at the head of the given names is
    dropped in any case ('Cmdr. Worth H.')."""
    head = d.split(',', 1)[0].strip()
    if head and not TITLES.sub('', head).strip():      # 'Gen., Deputy Commanding General': the rank dropped
        d = d.split(',', 1)[1].strip() if ',' in d else ''
    if p[1]:
        g, sfx = p[1], (p[2] if len(p) > 2 else '')
        m = re.match(r'(Jr|Sr|II|III|IV)\.?,\s*', g)       # 'Cushman, Jr., Lieutenant General Robert E.'
        if m:
            g, sfx = g[m.end():], m.group(1) + ('.' if m.group(1) in ('Jr', 'Sr') else '')
        g = SERVICE.sub('', TITLES.sub('', g)).strip(' ,')
        return (p[0], g, sfx), d
    if not d or ',' in p[0]:
        return p, d
    head, _, rest = d.partition(',')
    g = SERVICE.sub('', TITLES.sub('', head.strip())).strip(' ,')
    sfx = ''
    m = re.match(r'\s*(Jr|Sr|II|III|IV)\.?\s*(?:,|$)', rest)
    if m:
        sfx, rest = m.group(1) + ('.' if m.group(1) in ('Jr', 'Sr') else ''), rest[m.end():]
    words = g.split()
    if not words or len(words) > 4 or OFFICE & {w.strip('.,').lower() for w in words} or not all(re.fullmatch(r"(?:[A-Z]\.){1,3}|[A-Z][\w'’-]*\.?|(?:de|da|van|von|y)", w)
                                              for w in words):
        return p, d
    return (p[0], g, sfx), rest.strip(' ,.;:—–-')


def norm(p):
    """A listed name's key for joining across volumes: the surname, the given names as tokens, the suffix."""
    from bib.lives import gtoks
    from bib.store import fold
    sur = re.sub(r'[\s-]+', ' ', fold(re.sub(r'\s*\([^)]*\)', '', M.clean(p[0]))).lower()).strip()
    return (sur, tuple(gtoks(p[1] or '')), ((p[2] if len(p) > 2 else '') or '').rstrip('.'))


def shown(p):
    """The name as the series writes it: 'Smith, Gerard C.', 'Nolting, Frederick E., Jr.', 'Buu Hoi'."""
    sur = re.sub(r'\s*\([^)]*\)', '', M.clean(p[0])).strip()
    sfx = (p[2] if len(p) > 2 else '') or ''
    return sur + (', ' + p[1] if p[1] else '') + (', ' + sfx if sfx and p[1] else '')


def join(found, taken):
    """The persons listed in FRUS whom no name entry holds, one a person: {key: {name, names}}. The same listed
    name in every volume is one person; two forms join where the surname and suffix agree and the given names agree
    name by name, each the same or one the other's initial ('J. Graham' and 'John Graham'), and only one form so
    fits. The name shown is the fullest form. A key a name entry holds already is left out."""
    from bib.lives import key_of
    groups = {}
    for nk in found:
        groups.setdefault((nk[0], nk[2]), []).append(nk)
    parent = {nk: nk for nk in found}
    def root_of(x):
        while parent[x] != x:
            x = parent[x]
        return x
    agree = lambda a, b: len(a) == len(b) and a and all(x == y or (len(x) == 1 and y.startswith(x))
                                                        or (len(y) == 1 and x.startswith(y)) for x, y in zip(a, b))
    for g in groups.values():
        for nk in g:
            fit = [o for o in g if o != nk and agree(nk[1], o[1])]
            if len(fit) == 1:
                parent[root_of(nk)] = root_of(fit[0])
    # one name in either order ('Thanat Khoman' and 'Khoman, Thanat'; 'U Nu' and 'Nu, U'): the same words, in full
    words = {}
    for nk in found:
        w = tuple(sorted(nk[0].split() + list(nk[1])))
        if all(len(x) > 1 for x in nk[1]):
            words.setdefault((w, nk[2]), []).append(nk)
    for nks in words.values():
        for nk in nks[1:]:
            a, b = root_of(nk), root_of(nks[0])
            if a != b:
                parent[a] = b
    sets = {}
    for nk in found:
        sets.setdefault(root_of(nk), []).append(nk)
    out, keymap = {}, {}
    for r, nks in sets.items():
        names = sorted({n for nk in nks for n in found[nk]})
        name = max(names, key=lambda n: (len(re.findall(r'\w+', n)), len(n), n))
        k = key_of(name)
        if not k or k in taken or k in out:
            continue
        out[k] = {'name': name, 'names': names}
        for nk in nks:
            keymap[nk] = k
    return out, keymap


def scan(git, targets, heirs=None, naturals=None, found=None):
    """targets: {key: (surname, given, suffix, strict)}. One pass over every volume. A list's 'Byrd, Harry F., Jr.'
    is the person whose suffix is Jr.; a bare 'Byrd, Harry F.' is not, where his father, written bare, has his own
    entry (strict). heirs: {father's key: (year he died, son's key)}: a document after the father's death that names
    him bare names the son (Harry F. Byrd, d. 1966; FRUS 1969-76 writes the son bare)."""
    heirs = heirs or {}
    by_sur = {}
    for k, (sur, given, sfx, strict) in targets.items():
        by_sur.setdefault(skey(sur), []).append((k, given, sfx, strict))
    # a single word the lists give alone that names someone held ('Rayburn'; 'Diem', 'Nhu'): no entry of its own
    held_words = set(by_sur) | {skey(sur.split()[-1]) for sur, g, _, _ in targets.values() if not g and ' ' in sur}
    out, titles = {}, {}
    for path in volumes(git):
        vol = os.path.basename(path)[:-4]
        xml = subprocess.run(['git', '-C', git, 'cat-file', '-p', f'HEAD:{path}'], capture_output=True).stdout
        try:
            root = ET.fromstring(xml)
        except ET.ParseError:
            print('unreadable', vol, file=sys.stderr)
            continue
        P, roles = M.persons(root)
        desc = descriptions(root)
        pn_text = {pn.get(M.XID): M.clean(''.join(pn.itertext())) for pn in root.iter(M.T + 'persName') if pn.get(M.XID)}
        P.update({i: ERRATA[(vol, i)] for i in P if (vol, i) in ERRATA})
        ids = {}                                   # xml:id -> person key
        for i in list(P):
            P[i], desc[i] = recover(P[i], desc.get(i, ''))
        for i, p in P.items():
            hits = []
            for k, given, sfx, strict in by_sur.get(skey(p[0]), []):
                # the first names alike, and the further names and initials too where both give them ('John W.' is
                # not 'John G.')
                if p[1] and fits(given, p[1]):
                    ps = sfx_of(p[1])
                    if strict and not ps and len(p) > 2:
                        ps = (p[2] or '').rstrip('.')       # the list keeps a suffix apart: 'Dean, John W., III'
                    if (ps == sfx) if (ps or strict) else True:
                        hits.append(k)
            if naturals and not hits:
                k = natural_hit(p, roles.get(i, ''), naturals)
                if k:
                    hits.append(k)
            listed = (p[2] or '').rstrip('.') if len(p) > 2 else ''
            if len(hits) > 1 and listed:     # a father and a son: the list's suffix tells them apart
                hits = [k for k in hits if targets[k][2] == listed] or hits
            if len(hits) == 1:               # two persons the list's name fits: the documents cannot tell them apart
                ids[i] = hits[0]
            elif not hits and found is not None and desc.get(i) and not re.match(r'(see|pseudonym)\b', desc[i], re.I):
                # a person the list gives whom no name entry holds: his own entry (join, after every volume)
                nk = norm(P[i])
                kin = [g for _, g, _, _ in by_sur.get(skey(P[i][0]), [])]
                bare = not P[i][1]
                if nk[0] and (not bare or ',' not in pn_text.get(i, '')) and not loose(P[i][1], kin) \
                        and not (bare and ' ' not in nk[0] and (skey(P[i][0]) in held_words or nk[0] in NOT_NAMES)):
                    found.setdefault(nk, set()).add(shown(p))
                    ids[i] = nk
        if not ids:
            continue
        for i, k in ids.items():             # each volume's description of the person
            if desc.get(i):
                out.setdefault(k, {}).setdefault(vol, {'named': [], 'sent': []}).setdefault('role', desc[i])
        bs = {'\0role': {P[i]: roles.get(i, '') for i in P}}
        for p in dict.fromkeys(P.values()):
            for kk in {p[0].lower(), p[0].split()[-1].lower()}:
                bs.setdefault(kk, []).append(p)
        vsub = root.find(f'.//{M.T}titleStmt/{M.T}title[@type="volume"]')
        titles[vol] = M.clean(''.join(vsub.itertext())) if vsub is not None else ''
        n_hit = 0
        for d in root.iter(M.T + 'div'):
            if d.get('type') != 'document':
                continue
            refs = {(pn.get('corresp') or '').lstrip('#') for pn in d.iter(M.T + 'persName')}
            keys = {ids[r] for r in refs if r in ids}
            if not keys:
                continue
            n = d.get('n') or d.get(M.XID)
            date = (d.get(M.F + 'doc-dateTime-min') or '')[:10]
            head = d.find(M.T + 'head')
            who, title = [], ''
            if head is not None and d.get('subtype') != 'editorial-note':
                title = M.strip_number(M.head_text(head), n)
                try:
                    who = M.authors(d, head, title, P, roles, bs)
                except Exception:
                    who = []
            senders = {ids[i] for i, p in P.items() if i in ids and p in [w for w in who if isinstance(w, tuple)]}
            keys = {heirs[k][1] if k in heirs and date[:4] > heirs[k][0] else k for k in keys}
            senders = {heirs[k][1] if k in heirs and date[:4] > heirs[k][0] else k for k in senders}
            for k in keys:
                v = out.setdefault(k, {}).setdefault(vol, {'named': [], 'sent': []})
                v['named'].append([n, date])
                if k in senders:
                    v['sent'].append([n, date, title])
                n_hit += 1
        print(vol, len(ids), n_hit, file=sys.stderr, flush=True)
    return out, titles


def heirs_of(everyone, targets):
    """{father's key: (year he died, son's key)}: a bare name whose namesake with a suffix is strict, and the year of
    death the Directory gives the father."""
    from bib import store
    from bib.lives import bd_entry, same_person
    out = {}
    for k, (sur, given, sfx, strict) in targets.items():
        if not strict:
            continue
        for k2, (sur2, given2, sfx2, strict2) in targets.items():
            if k2 != k and not sfx2 and same_person(sur2, given2, sur, given):
                e = bd_entry(sur2, given2, True, (), '')
                died = re.findall(r'died[^;]*?\b(1[89]\d\d|20\d\d)\b', e['text']) if e else []
                if died:
                    out[k2] = (died[-1], k)
    return out


def main():
    git = sys.argv[1]
    if '--all' in sys.argv:
        from bib import store
        from bib.lives import people, key_of, person_suffix
        S = store.Series()
        everyone = people(S)                 # not those from FRUS's lists alone: this pass finds them again
        targets = {key_of(p['name']): (p['sur'], p['given'], *person_suffix(S, p)) for p in everyone}
        heirs = heirs_of(everyone, targets)
        from bib.lives import natural, name_forms
        naturals = {flat(f): key_of(p['name']) for p in everyone if natural(p['name']) for f in name_forms(p['name'])}
    else:
        targets = {key(t): (*[x.strip() for x in t.split(',', 1)], sfx_of(t), False) for t in sys.argv[2:]}
        heirs, naturals = {}, {}
    os.makedirs(OUT, exist_ok=True)
    found = {} if '--all' in sys.argv else None
    out, titles = scan(git, targets, heirs, naturals, found)
    if found is not None:
        persons, keymap = join(found, set(targets))
        for nk in [k for k in out if isinstance(k, tuple)]:
            v = out.pop(nk)
            if nk in keymap:
                for vol, x in v.items():
                    y = out.setdefault(keymap[nk], {}).setdefault(vol, {'named': [], 'sent': []})
                    y['named'] += [d for d in x['named'] if d not in y['named']]
                    y['sent'] += [d for d in x['sent'] if d not in y['sent']]
                    if x.get('role'):
                        y.setdefault('role', x['role'])
        with open(os.path.join(OUT, 'persons.json'), 'w', encoding='utf-8') as f:
            json.dump(persons, f, ensure_ascii=False, separators=(',', ':'))
        print(len(persons), 'persons from the lists alone', file=sys.stderr)
    letters = {}
    for k, v in out.items():
        letters.setdefault(k[0].upper(), {})[k] = v
    for L, v in letters.items():
        with open(os.path.join(OUT, f'{L}.json'), 'w', encoding='utf-8') as f:
            json.dump(v, f, ensure_ascii=False, separators=(',', ':'))
    with open(os.path.join(OUT, 'volumes.json'), 'w', encoding='utf-8') as f:
        json.dump(titles, f, ensure_ascii=False, indent=0)
    print(len(out), 'persons named', file=sys.stderr)


if __name__ == '__main__':
    main()
