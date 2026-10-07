"""Every FRUS document that names a person, and those the person sent: sources/frus-names/<letter>.json.
# Usage: python3 tools/lives/frus_names.py FRUS_GIT [--all | 'Surname, Given' ...]
#   --all: everyone with a Lives entry (tools/bib/lives.py, people)
#   FRUS_GIT  a clone of github.com/HistoryAtState/frus (blobs present or fetchable)
#   Reads every volume 1952-54 to 1969-76: the volume's list of persons gives the person's xml:id; a document
#   names the person where its text links a persName to that id (corresp); the person sent it where the
#   daybook's rules for authors (tools/daybook/make_daybook.py, "authors as persons") give the person.
#   Writes, by the first letter of the surname, {person key: {volume: {"named": [[doc number, date]], "sent":
#   [[doc number, date, heading]]}}}, and sources/frus-names/volumes.json, {volume: its title}.
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


def scan(git, targets, heirs=None):
    """targets: {key: (surname, given, suffix, strict)}. One pass over every volume. A list's 'Byrd, Harry F., Jr.'
    is the person whose suffix is Jr.; a bare 'Byrd, Harry F.' is not, where his father, written bare, has his own
    entry (strict). heirs: {father's key: (year he died, son's key)}: a document after the father's death that names
    him bare names the son (Harry F. Byrd, d. 1966; FRUS 1969-76 writes the son bare)."""
    heirs = heirs or {}
    by_sur = {}
    for k, (sur, given, sfx, strict) in targets.items():
        by_sur.setdefault(M.clean(sur).lower(), []).append((k, given, sfx, strict))
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
        ids = {}                                   # xml:id -> person key
        for i, p in P.items():
            hits = []
            for k, given, sfx, strict in by_sur.get(M.clean(p[0]).lower(), []):
                if p[1] and compatible(given, p[1]) and M.first_word(p[1]) == M.first_word(given):
                    ps = sfx_of(p[1])
                    if (ps == sfx) if (ps or strict) else True:
                        hits.append(k)
            if len(hits) == 1:               # two persons the list's name fits: the documents cannot tell them apart
                ids[i] = hits[0]
        if not ids:
            continue
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
        everyone = people(S)
        targets = {key_of(p['name']): (p['sur'], p['given'], *person_suffix(S, p)) for p in everyone}
        heirs = heirs_of(everyone, targets)
    else:
        targets = {key(t): (*[x.strip() for x in t.split(',', 1)], sfx_of(t), False) for t in sys.argv[2:]}
        heirs = {}
    os.makedirs(OUT, exist_ok=True)
    out, titles = scan(git, targets, heirs)
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
