"""The day's executive documents: every Public Papers and FRUS document, filed under its date.
# Usage: python3 tools/daybook/make_daybook.py [--cache DIR]
#   Rewrites daybook/<YYYY-MM>.yaml for the calendar's span (FROM..TO below). Needs the network;
#   the build does not. Abstracts live in daybook/abstracts.yaml, keyed by document, and are not
#   touched here, so a rerun keeps them.
#
#   Public Papers: the American Presidency Project's listing of every presidential document by date
#   (Public Papers items, executive orders, proclamations). Author: the President.
#   FRUS: the Office of the Historian's TEI files (github.com/HistoryAtState/frus), every volume of
#   the 1958-60 and 1961-63 subseries, microfiche supplements included. Date: the document's
#   frus:doc-dateTime-min. Editorial notes carry only their volume's span, so each is filed under
#   the date of the document before it in its volume. Author: the sender named in the heading
#   ("From the Embassy in France to ..."), shortened to the name in parentheses where there is one;
#   failing that, the drafter in the source note ("Drafted by Kohler").
#   Mechanical throughout: titles and authors are the sources' own; nothing is read or summarized.
"""
import datetime, html, os, re, sys, tempfile, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
import yaml

FROM, TO = '1961-01-01', '1963-01-03'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'daybook')
UA = {'User-Agent': 'Mozilla/5.0 (bibliography daybook)'}
APP = 'https://www.presidency.ucsb.edu'
RAW = 'https://raw.githubusercontent.com/HistoryAtState/frus/master/volumes/'
HSG = 'https://history.state.gov/historicaldocuments/'
# The volumes, from history.state.gov's lists for the Eisenhower and Kennedy administrations.
VOLS = (['frus1958-60v%02d' % i for i in (1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19)]
        + ['frus1958-60v07p1', 'frus1958-60v07p2', 'frus1958-60v10p1', 'frus1958-60v10p2',
           'frus1958-60v03mSupp', 'frus1958-60v05mSupp', 'frus1958-60v11mSupp', 'frus1958-60v15-16mSupp1',
           'frus1958-60v15-16mSupp2', 'frus1958-60v17-18mSupp', 'frus1958-60v19mSupp']
        + ['frus1961-63v%02d' % i for i in range(1, 26)]
        + ['frus1961-63v07-09mSupp', 'frus1961-63v10-12mSupp', 'frus1961-63v13-15mSupp',
           'frus1961-63v17-21mSupp', 'frus1961-63v22-24mSupp'])
T = '{http://www.tei-c.org/ns/1.0}'
F = '{http://history.state.gov/frus/ns/1.0}'
XID = '{http://www.w3.org/XML/1998/namespace}id'
ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV',
         'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV']


def fetch(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                return r.read()
        except Exception:
            time.sleep(3 * (i + 1))
    raise SystemExit('failed: ' + url)


def clean(t):
    return re.sub(r'\s+', ' ', html.unescape(t or '')).strip()


# ---------------------------------------------------------------- Public Papers (APP)

def app_docs():
    f = lambda d: f'{d[5:7]}-{d[8:10]}-{d[:4]}'
    out, page = [], 0
    while True:
        q = {'from[date]': f(FROM), 'to[date]': f(TO), 'items_per_page': 100, 'page': page}
        s = fetch(APP + '/advanced-search?' + urllib.parse.urlencode(q)).decode('utf-8', 'replace')
        n = 0
        for row in re.findall(r'<tr[^>]*>(.*?)</tr>', s, re.S):
            tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
            if len(tds) < 3:
                continue
            a = re.search(r'href="(/documents/[^"]*)"[^>]*>([^<]*)', tds[2])
            if not a:
                continue
            n += 1
            d = datetime.datetime.strptime(clean(re.sub('<[^>]+>', '', tds[0])), '%b %d, %Y').date().isoformat()
            who = clean(re.sub('<[^>]+>', '', tds[1]))
            out.append({'key': 'app:' + a.group(1).rsplit('/', 1)[-1], 'src': 'ppp', 'date': d,
                        'author': who.split()[-1], 'title': clean(a.group(2)).rstrip('.'),
                        'url': APP + a.group(1)})
        if n < 100:
            return out
        page += 1


# ---------------------------------------------------------------- FRUS (TEI)

def head_text(head):
    """The heading without its footnotes."""
    parts = [head.text or '']
    for c in head:
        if c.tag != T + 'note':
            parts.append(''.join(c.itertext()))
        parts.append(c.tail or '')
    return clean(''.join(parts))


STOP = re.compile(r'(Assistant|Adviser|Advisor|Representative|Mission|Delegation|Ambassador|Counselor|Envoy|Secretary|Deputy|Liaison)$')


def sender(title):
    """'Memorandum From the President's Special Assistant (Bundy) to the President' -> Bundy."""
    m = re.search(r'\b(?:[Ff]rom|[Pp]repared (?:by|in)|[Bb]y) (.+)$', title)
    if not m:
        return None
    s = m.group(1)
    cut = None
    for t in re.finditer(r' to ', s):
        left = s[:t.start()]
        if left.count('(') == left.count(')') and not STOP.search(left):
            cut = t.start()
            break
    s = s[:cut] if cut is not None else s
    s = re.sub(r',\s*(undated|[A-Z][a-z]+\.? \d{1,2}(, \d{4})?|[A-Z][a-z]+ \d{4})$', '', s)
    names = re.findall(r'\(([^()]+)\)', s)
    if names:
        return names[0]
    return re.sub(r'^the ', '', s).strip() or None


def drafter(head):
    """'Drafted by Kohler and approved ...' in the source note: the author of a memorandum of conversation."""
    for n in head.iter(T + 'note'):
        if n.get('type') == 'source':
            m = re.search(r'\b[Dd]rafted (?:by|in) (.+?)(?=(?: on [A-Z]| and (?:approved|cleared|initialed|revised)|[;.,:]|$))',
                          clean(''.join(n.itertext())))
            if m and len(m.group(1)) < 80:
                return re.sub(r'^the ', '', m.group(1).strip())
    return None


def day_of(stamp, is_max=False):
    """Calendar date of a frus:doc-dateTime value. Some ranges were set in another zone and read
    23:00 the day before (min) or 22:59 (max); those are moved back to the intended day."""
    d = datetime.date.fromisoformat(stamp[:10])
    if not is_max and stamp[11:16] == '23:00':
        d += datetime.timedelta(days=1)
    return d


def cite(vol):
    m = re.match(r'frus(\d{4})-(\d\d)(?:v(\d\d)(?:-(\d\d))?)?(p\d)?(mSupp\d?)?', vol)
    years = f'{m.group(1)}–{m.group(2)}'
    v = ROMAN[int(m.group(3))] + (('–' + ROMAN[int(m.group(4))]) if m.group(4) else '')
    part = f', pt. {m.group(5)[1:]}' if m.group(5) else ''
    supp = ', microfiche supp.' if m.group(6) else ''
    return f'FRUS {years}, {v}{part}{supp}'


def frus_docs(cache):
    os.makedirs(cache, exist_ok=True)
    out = []
    for vol in VOLS:
        path = os.path.join(cache, vol + '.xml')
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(RAW + vol + '.xml'))
        root = ET.parse(path).getroot()
        vt = clean(''.join(root.find(f'.//{T}titleStmt/{T}title[@type="subseries"]').itertext())
                   if root.find(f'.//{T}titleStmt/{T}title[@type="subseries"]') is not None else '')
        vsub = root.find(f'.//{T}titleStmt/{T}title[@type="volume"]')
        vt = clean(''.join(vsub.itertext())) if vsub is not None else vt
        prev = None
        for d in root.iter(T + 'div'):
            if d.get('type') != 'document':
                continue
            head = d.find(T + 'head')
            if head is None:
                continue
            title = head_text(head)
            n = d.get('n')
            title = re.sub(r'^' + re.escape(str(n)) + r'\.\s*', '', title) if n else title
            ed = d.get('subtype') == 'editorial-note'
            lo, hi = d.get(F + 'doc-dateTime-min'), d.get(F + 'doc-dateTime-max')
            if ed or not lo:
                if prev is None:
                    continue
                start, end, placed = prev, prev, True
            else:
                start, end, placed = day_of(lo), day_of(hi, True) if hi else day_of(lo), False
                if end < start:
                    end = start
                prev = start
            if not (FROM <= start.isoformat() <= TO):
                continue
            doc = {'key': f'frus:{vol}/{d.get(XID)}', 'src': 'frus', 'date': start.isoformat(),
                   'title': title, 'url': f'{HSG}{vol}/{d.get(XID)}',
                   'cite': f'{cite(vol)}, doc. {n}', 'vol': vt}
            if end != start:
                doc['until'] = end.isoformat()
            if placed:
                doc['placed'] = True
            if lo and not ed and lo[11:16] not in ('00:00', '23:00'):
                doc['time'] = lo[11:16]
            a = None if ed else (sender(title) or drafter(head))
            if a:
                doc['author'] = a
            out.append(doc)
    return out


def main():
    cache = sys.argv[sys.argv.index('--cache') + 1] if '--cache' in sys.argv else os.path.join(tempfile.gettempdir(), 'frus-tei')
    docs = app_docs() + frus_docs(cache)
    order = {'ppp': 0, 'frus': 1}
    vol_i = {v: i for i, v in enumerate(VOLS)}

    def frus_pos(x):
        vol, d = x['key'][5:].split('/')
        return (vol_i[vol], int(re.sub(r'\D', '', d) or 0))
    # The President's in APP's order; FRUS by volume, then the volume's own order.
    docs.sort(key=lambda x: (x['date'], order[x['src']]) + (frus_pos(x) if x['src'] == 'frus' else (0, 0)))
    months = {}
    for x in docs:
        months.setdefault(x['date'][:7], []).append(x)
    os.makedirs(OUT, exist_ok=True)
    head = ('# Generated by tools/daybook/make_daybook.py. Edit the script, not this file.\n'
            '# One row per document: key, src (ppp|frus), date, author, title, url; FRUS adds cite, vol (the\n'
            '# volume title), until (last day of a dated range), time, placed (an editorial note filed by its\n'
            '# place in the volume). Abstracts: daybook/abstracts.yaml.\n')
    for m, rows in sorted(months.items()):
        body = yaml.safe_dump({'month': m, 'docs': rows}, sort_keys=False, allow_unicode=True, width=200)
        open(os.path.join(OUT, f'{m}.yaml'), 'w', encoding='utf-8').write(head + body)
        print(m, len(rows))
    print('total', len(docs), 'ppp', sum(x['src'] == 'ppp' for x in docs), 'frus', sum(x['src'] == 'frus' for x in docs))


if __name__ == '__main__':
    main()
