"""Index the Library of Congress's scans of the United States Code, 1958, 1964 and 1970 editions and supplements.
# Usage: python3 tools/executive/make_uscode_index.py [--resplit]
#   Writes sources/uscode-loc.json: for each edition, every chapter item the Library holds, with its title
#   number, its first and last sections, and the item's URL. The build links a roster citation such as
#   '50 U.S.C. § 402 (1958)' to the item that holds the section (tools/bib/executive.py, usc_link). Needs the
#   network; the build does not.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'sources', 'uscode-loc.json')
API = 'https://www.loc.gov/collections/united-states-code/'
UA = {'User-Agent': 'bib-roster/1.0 (research bibliography)'}
EDITIONS = ['1952', '1958', '1964', '1970']


def fetch(q, page):
    url = API + '?' + urllib.parse.urlencode({'fo': 'json', 'c': 150, 'sp': page, 'q': q})
    for i in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                return json.load(r)
        except Exception as e:
            print('retry', url, e, file=sys.stderr)
            time.sleep(10 * (i + 1))
    raise SystemExit('failed: ' + url)


def split_range(sec, plural):
    """'1-20' under '§§' -> ('1', '20'); '133z-15-133z-18' -> ('133z-15', '133z-18'); '133z-15' under '§' stays."""
    parts = sec.split('-')
    if not plural or len(parts) < 2:
        return sec, sec
    if len(parts) % 2 == 0:
        return '-'.join(parts[:len(parts) // 2]), '-'.join(parts[len(parts) // 2:])
    if len(parts) == 3 and re.match(r'\d+[a-z]+$', parts[0]) and parts[1].isdigit():   # '133z-15-18'
        return '-'.join(parts[:2]), '-'.join([parts[0], parts[2]])
    return parts[0], '-'.join(parts[1:])


def sec_key(s):
    """'402' -> (402, ''); '403a' -> (403, 'a'); '1305' -> (1305, '')."""
    m = re.match(r'(\d+)([a-z\-]*)', s)
    return (int(m.group(1)), m.group(2)) if m else (0, s)


def resplit():
    """Redo the ranges of an existing index from its item names, without the network."""
    d = json.load(open(OUT, encoding='utf-8'))
    for ed, items in d.items():
        for it in items:
            m = re.search(r'U\.S\.C\. (§§?) ([\w\-]+)(?:\s*[-–]\s*([\w\-]+))?', it['name'])
            if m:
                it['from'], it['to'] = (m.group(2), m.group(3)) if m.group(3) else split_range(m.group(2), m.group(1) == '§§')
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=0)


def main():
    if '--resplit' in sys.argv:
        return resplit()
    out = {}
    for ed in EDITIONS:
        items, page = [], 1
        while True:
            d = fetch(f'uscode{ed}', page)
            for r in d.get('results', []):
                iid = r.get('id', '')
                if f'/uscode{ed}-' not in iid:
                    continue
                t = r.get('title', '')
                m = re.search(r'(\d+) U\.S\.C\. §§? ([\w\-]+)(?:\s*[-–]\s*([\w\-]+))?\s*\(([^)]*)\)', t)
                if not m:
                    continue
                sup = re.search(r'Suppl?\. (\d+)', m.group(4))
                lo_, hi_ = split_range(m.group(2), m.group(2) and '§§' in t) if not m.group(3) else (m.group(2), m.group(3))
                items.append({'title': int(m.group(1)), 'from': lo_, 'to': hi_,
                              'supp': int(sup.group(1)) if sup else 0, 'url': r.get('url') or iid,
                              'name': t.replace('United States Code: ', '')})
            pg = d.get('pagination', {})
            if not pg.get('next'):
                break
            page += 1
            time.sleep(2)
        out[ed] = sorted(items, key=lambda x: (x['supp'], x['title'], sec_key(x['from'])))
        print(ed, len(items))
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=0)


if __name__ == '__main__':
    main()
