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


def scan(git, targets):
    """targets: {key: (surname, given)}. One pass over every volume."""
    by_sur = {}
    for k, (sur, given) in targets.items():
        by_sur.setdefault(M.clean(sur).lower(), []).append((k, given))
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
            for k, given in by_sur.get(M.clean(p[0]).lower(), []):
                if p[1] and compatible(given, p[1]) and M.first_word(p[1]) == M.first_word(given):
                    ids[i] = k
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
                title = re.sub(r'^' + re.escape(str(n)) + r'\.\s*', '', M.head_text(head))
                try:
                    who = M.authors(d, head, title, P, roles, bs)
                except Exception:
                    who = []
            senders = {ids[i] for i, p in P.items() if i in ids and p in [w for w in who if isinstance(w, tuple)]}
            for k in keys:
                v = out.setdefault(k, {}).setdefault(vol, {'named': [], 'sent': []})
                v['named'].append([n, date])
                if k in senders:
                    v['sent'].append([n, date, title])
                n_hit += 1
        print(vol, len(ids), n_hit, file=sys.stderr, flush=True)
    return out, titles


def main():
    git = sys.argv[1]
    if '--all' in sys.argv:
        from bib import store
        from bib.lives import people, key_of
        targets = {key_of(p['name']): (p['sur'], p['given']) for p in people(store.Series())}
    else:
        targets = {key(t): tuple(x.strip() for x in t.split(',', 1)) for t in sys.argv[2:]}
    os.makedirs(OUT, exist_ok=True)
    out, titles = scan(git, targets)
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
