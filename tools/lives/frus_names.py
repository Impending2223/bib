"""Every FRUS document that names a person, and those the person sent: sources/frus-names/<key>.json.
# Usage: python3 tools/lives/frus_names.py FRUS_GIT 'Surname, Given' [...]
#   FRUS_GIT  a clone of github.com/HistoryAtState/frus (blobs present or fetchable)
#   Reads every volume 1952-54 to 1969-76: the volume's list of persons gives the person's xml:id; a document
#   names the person where its text links a persName to that id (corresp); the person sent it where the
#   daybook's rules for authors (tools/daybook/make_daybook.py, "authors as persons") give the person.
#   Writes {volume: {"named": [doc numbers], "sent": [doc numbers], "title": volume title}} for each person.
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
    out = {t: {} for t in targets}
    for path in volumes(git):
        vol = os.path.basename(path)[:-4]
        xml = subprocess.run(['git', '-C', git, 'cat-file', '-p', f'HEAD:{path}'], capture_output=True).stdout
        try:
            root = ET.fromstring(xml)
        except ET.ParseError:
            print('unreadable', vol, file=sys.stderr)
            continue
        P, roles = M.persons(root)
        ids = {}
        for t in targets:
            sur, given = [x.strip() for x in t.split(',', 1)]
            ids[t] = {i for i, p in P.items() if M.clean(p[0]).lower() == sur.lower() and p[1]
                      and compatible(given, p[1]) and M.first_word(p[1]) == M.first_word(given)}
        if not any(ids.values()):
            continue
        by_sur = {'\0role': {P[i]: roles.get(i, '') for i in P}}
        for p in dict.fromkeys(P.values()):
            for k in {p[0].lower(), p[0].split()[-1].lower()}:
                by_sur.setdefault(k, []).append(p)
        vsub = root.find(f'.//{M.T}titleStmt/{M.T}title[@type="volume"]')
        vt = M.clean(''.join(vsub.itertext())) if vsub is not None else ''
        for d in root.iter(M.T + 'div'):
            if d.get('type') != 'document' or d.get('subtype') == 'editorial-note' and False:
                continue
            refs = {(pn.get('corresp') or '').lstrip('#') for pn in d.iter(M.T + 'persName')}
            hit = [t for t in targets if ids[t] & refs]
            if not hit:
                continue
            head = d.find(M.T + 'head')
            title = M.head_text(head) if head is not None else ''
            n = d.get('n') or d.get(M.XID)
            title = re.sub(r'^' + re.escape(str(n)) + r'\.\s*', '', title)
            who = M.authors(d, head, title, P, roles, by_sur) if head is not None and d.get('subtype') != 'editorial-note' else []
            for t in hit:
                v = out[t].setdefault(vol, {'title': vt, 'named': [], 'sent': []})
                row = {'n': n, 'title': title, 'date': (d.get(M.F + 'doc-dateTime-min') or '')[:10]}
                v['named'].append(row)
                if any(isinstance(p, tuple) and {M.XID: 0} and any(P.get(i) == p for i in ids[t]) for p in who):
                    v['sent'].append(n)
        print(vol, {t: len(out[t].get(vol, {}).get('named', [])) for t in targets}, file=sys.stderr)
    return out


def main():
    git, targets = sys.argv[1], sys.argv[2:]
    os.makedirs(OUT, exist_ok=True)
    for t, v in scan(git, targets).items():
        with open(os.path.join(OUT, key(t) + '.json'), 'w', encoding='utf-8') as f:
            json.dump(v, f, ensure_ascii=False, indent=0)


if __name__ == '__main__':
    main()
