"""House and Senate returns for each election, from the Clerk's Statistics of the Congressional Election.
# Usage: python3 tools/elections/make_elections.py YEAR [YEAR ...] [--cache DIR]
#   Writes elections/<YEAR>.yaml. Needs the network, pdftoppm, and tesseract (apt-get install
#   tesseract-ocr); the build needs none of them.
#
#   1. The Clerk's volume (clerk.house.gov), each page to an image, OCR with word positions (clerk.py).
#   2. Wikipedia's race tables (wiki.py) give each race's candidates and percentages, its incumbents
#      and its result line; the Clerk's lines are matched to them by surname (match.py).
#   3. Each figure is read three times (the line, and two digits-only crops of the figure) and settled
#      against the state's recapitulation table and Wikipedia's percentages (reconcile.py).
#   4. Races that do not settle were read by eye from the page images (read.py), and those readings
#      replace the OCR.
#   Votes are the Clerk's. Names: the Clerk's where read by eye, otherwise Wikipedia's for the
#   candidates it lists and the Clerk's (OCR) for the others.
"""
import concurrent.futures
import glob
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

import yaml

sys.path.insert(0, os.path.dirname(__file__))
import clerk      # noqa: E402
import match      # noqa: E402
import president  # noqa: E402
import read       # noqa: E402
import reconcile  # noqa: E402
import wiki       # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'elections')
UA = {'User-Agent': 'Mozilla/5.0 (bibliography elections)'}
CLERK = 'https://clerk.house.gov/member_info/electionInfo/{y}election.pdf'
WIKI = 'https://en.wikipedia.org/w/index.php?title={t}&action=raw'
DATE = {1956: '1956-11-06', 1958: '1958-11-04', 1974: '1974-11-05', 1960: '1960-11-08', 1962: '1962-11-06', 1964: '1964-11-03', 1966: '1966-11-08',
        1968: '1968-11-05', 1970: '1970-11-03', 1972: '1972-11-07'}
CLASS = {1956: 3, 1958: 1, 1974: 3, 1960: 2, 1962: 3, 1964: 1, 1966: 2, 1968: 3, 1970: 1, 1972: 2}
CODE = {'Democrat': 'D', 'Democratic': 'D', 'Democrat-Farmer-Labor': 'D', 'DFL': 'D', 'Democratic–Farmer–Labor': 'D',
        'Democratic-NPL': 'D', 'Democratic (DFL)': 'D', 'Republican': 'R', 'Liberal': 'L', 'Conservative': 'C', 'Independent': 'I',
        'Independent Democrat': 'ID', 'Democrat, Liberal': 'D'}


def fetch(url, tries=6):
    import time
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == tries - 1:
                raise
            time.sleep(20 * (i + 1))    # Wikipedia's rate limit


def ocr(y, cache):
    """Page images and tesseract TSV for the Clerk's volume; then the two digits-only readings."""
    d = os.path.join(cache, str(y))
    os.makedirs(d, exist_ok=True)
    pdf = os.path.join(cache, f'{y}.pdf')
    if not os.path.exists(pdf) or not os.path.getsize(pdf):
        body = fetch(CLERK.format(y=y))
        open(pdf, 'wb').write(body)
    if not glob.glob(os.path.join(d, 'p-*.png')):
        subprocess.run(['pdftoppm', '-r', '300', '-gray', '-png', pdf, os.path.join(d, 'p')], check=True)
    env = dict(os.environ, OMP_THREAD_LIMIT='1')
    pages = sorted(glob.glob(os.path.join(d, 'p-*.png')))

    def tsv(p):
        if not os.path.exists(p[:-4] + '.tsv'):
            subprocess.run(['tesseract', p, p[:-4], '--psm', '6', 'tsv'], capture_output=True, env=env)
    with concurrent.futures.ThreadPoolExecutor(6) as ex:
        list(ex.map(tsv, pages))
    return d


def digits(y, d, C):
    """Two digits-only readings of each line's figure: cropped by page position, and by the figure's word box."""
    from PIL import Image
    env = dict(os.environ, OMP_THREAD_LIMIT='1')
    jobs = [(st, sec, k, l) for st, v in C.items() for sec in ('senate', 'house', 'recap', 'pres') for k, l in enumerate(v.get(sec, []))]
    imgs = {}
    for p in sorted({l['page'] for *_, l in jobs}):
        im = Image.open(os.path.join(d, f'p-{p:02d}.png'))
        im.load()
        imgs[p] = im

    def one(j, kind):
        st, sec, k, l = j
        out = os.path.join(d, f'{kind}_{st}_{sec}_{k}.txt')
        if os.path.exists(out):
            return
        im = imgs[l['page']]
        W, H = im.size
        if kind == 'dg':
            box = (int(W * (0.62 if sec != 'recap' else 0.40)), max(0, l['top'] - 6), W - int(W * 0.08), min(H, l['bottom'] + 6))
            scale = 2
        else:
            if not l.get('fx'):
                return
            box = (max(0, l['fx'] - 25), max(0, l['top'] - 8), W - int(W * 0.05), min(H, l['bottom'] + 8))
            scale = 3
        c = im.crop(box)
        c = c.resize((c.width * scale, c.height * scale))
        fn = os.path.join(tempfile.gettempdir(), f'el_{y}_{kind}_{st}_{sec}_{k}.png')
        c.save(fn)
        r = subprocess.run(['tesseract', fn, '-', '--psm', '7', '-c', 'tessedit_char_whitelist=0123456789,'],
                           capture_output=True, text=True, env=env).stdout.strip()
        open(out, 'w').write(r)
        os.remove(fn)
    with concurrent.futures.ThreadPoolExecutor(6) as ex:
        list(ex.map(lambda j: one(j, 'dg'), jobs))
        list(ex.map(lambda j: one(j, 'dg2'), jobs))


def wiki_page(t, cache):
    p = os.path.join(cache, f'w_{t}.txt')
    if not os.path.exists(p) or not os.path.getsize(p):
        body = fetch(WIKI.format(t=t))    # fetch before opening, so a failure leaves no empty file
        open(p, 'wb').write(body)
    return open(p, encoding='utf-8').read()


def wiki_races(y, cache):
    def page(t):
        return wiki_page(t, cache)
    H = [r for r in wiki.house(page(f'{y}_United_States_House_of_Representatives_elections')) if not r['special']]
    S = wiki.senate(page(f'{y}_United_States_Senate_elections'), CLASS[y])
    return H, S


def canon(p):
    """The party as printed, with the OCR's near misses put right ('D mocrat', 'Nemoerat', 'Farmer-Labor')."""
    import difflib
    p = (p or '').strip(' .,')
    if p in CODE or not p:
        return p
    if re.match(r'(Dem|Rep)\.?/', p):    # Wikipedia's 'Dem./Write-in'
        return 'Democrat' if p.startswith('Dem') else 'Republican'
    if 'Farmer' in p or 'Labor' in p and 'Socialist' not in p:
        return 'Democrat-Farmer-Labor'
    for good in ('Democrat', 'Republican', 'Liberal', 'Conservative', 'Independent'):
        if difflib.SequenceMatcher(None, p.lower(), good.lower()).ratio() >= 0.75:
            return good
    return p


def code(p):
    """D, R, L, C, I, ID, or O; a cross-filed or fusion candidate by the first party printed."""
    p = canon(p)
    return CODE.get(p) or CODE.get(canon((p or '').split(',')[0]), 'O')


def seat_key(r):
    return r['d'] if r['chamber'] == 'h' else r['cl']


# The races and States a run leaves for reading by eye: {year, key, why (unsettled | unmatched), loc
# (page, top, bottom) on the page images, wiki [(name, party, pct)], ocr [raw lines]}. tools/elections/review.py
# reads this list to make the reading sheets.
LEFT = []


def where(r, lines):
    """The race's place on the page images, from the lines matched to it: (page, top, bottom), or None."""
    idx = [i for c in r['candidates'] if c.get('clerk') for i in c['clerk']['lines']] + [i for x in r.get('minor', []) for i in x['lines']]
    if r.get('span'):
        idx += list(range(r['span'][0], r['span'][1] + 1))
    if not idx:
        return None, []
    pg = lines[idx[0]]['page']
    same = [lines[i] for i in idx if lines[i]['page'] == pg]
    return (pg, min(l['top'] for l in same) - 60, max(l['bottom'] for l in same) + 60), [lines[i]['raw'] for i in sorted(set(idx))]


def leave(y, key, why, r, lines):
    loc, raw = where(r, lines)
    LEFT.append({'year': y, 'key': list(key), 'why': why, 'loc': loc, 'ocr': raw,
                 'wiki': [(c['name'], c.get('party'), c.get('pct')) for c in r['candidates']]})
    sys.stderr.write(f'{why} {y} {key}: read it by eye (tools/elections/review.py)\n')


def main():
    """make_elections.py YEAR... [--cache DIR]: write elections/<year>.yaml for each year."""
    years = [int(a) for a in sys.argv[1:] if a.isdigit()]
    cache = sys.argv[sys.argv.index('--cache') + 1] if '--cache' in sys.argv else os.path.join(tempfile.gettempdir(), 'clerk-ocr')
    for y in years:
        year(y, cache)


def year(y, cache, write=True):
    """One election: the Clerk's volume OCR'd and settled, Wikipedia's races, the readings by eye; the
    year's record (and elections/<year>.yaml when write). What is left for reading goes to LEFT."""
    os.makedirs(OUT, exist_ok=True)
    d = ocr(y, cache)
    C = clerk.states(clerk.lines(d))
    for st, v in C.items():
        for sec in v:
            for k, l in enumerate(v[sec]):
                l['sec'], l['k'] = sec, k
    digits(y, d, C)
    H, S = wiki_races(y, cache)

    def dg(st, sec, k, kind):
        f = os.path.join(d, f'{kind}_{st}_{sec}_{k}.txt')
        n = reconcile.nums(open(f).read()) if os.path.exists(f) else []
        return n[-1] if n else None

    rows_cache = {}

    def recap(st, key):
        if st not in rows_cache:
            out = {'d': [], 0: [], 's': []}
            for k, r in enumerate(C.get(st, {}).get('recap', [])):
                low = r['raw'].lower()
                extra = []
                for kind in ('dg', 'dg2'):
                    f = os.path.join(d, f'{kind}_{st}_recap_{k}.txt')
                    extra += reconcile.nums(open(f).read()) if os.path.exists(f) else []
                m = re.search(r'di[s8]tr', low)
                if m:
                    out['d'].append((reconcile.nums(r['raw'][m.end():]), extra))
                elif re.search(r'at\s*large', low):
                    out[0].append((reconcile.nums(r['raw']), extra))
                elif re.search(r'senat|term', low):
                    out['s'].append((reconcile.nums(r['raw']), extra))
            rows_cache[st] = out
        R = rows_cache[st]
        rows = R['s'] if key == 's' else R[0] if key == 0 else R['d'][key - 1:key]
        return [x for a, b in rows for x in a + b], sorted({x[-1] for a, b in rows for x in (a, b) if x})

    races_out = []
    for st in sorted({r['st'] for r in H + S}):
        lines = sorted(C.get(st, {}).get('senate', []) + C.get(st, {}).get('house', []), key=lambda l: (l['page'], l['top']))
        races = ([dict(r, chamber='s') for r in S if r['st'] == st and not r['special']]
                 + [dict(r, chamber='s') for r in S if r['st'] == st and r['special']]
                 + [dict(r, chamber='h') for r in sorted([r for r in H if r['st'] == st],
                                                          key=lambda r: (r['d'] == 0 and any(x['st'] == st and x['d'] > 0 for x in H), r['d']))])
        # an at-large delegation Wikipedia lists a row a seat: one race of several seats
        merged = []
        for r in races:
            prev = next((x for x in merged if x['chamber'] == 'h' == r['chamber'] and x['d'] == 0 == r['d']), None)
            if prev:
                prev['incumbents'] += r['incumbents']
                prev['candidates'] += [c for c in r['candidates'] if c['name'] not in [x['name'] for x in prev['candidates']]]
            else:
                merged.append(r)
        races = merged
        match.align(races, lines)
        for r in races:
            key = (r['chamber'], st, seat_key(r))
            rec = race_record(y, st, r, lines, key, dg, recap)
            if rec:
                races_out.extend(rec)
    head = ('# Generated by tools/elections/make_elections.py. Edit the script or elections/readings/, not this file.\n'
            '# races: ch (h|s), st, seat (district, 0 at large; Senate class), seats (members elected), special,\n'
            '# cands [{n name, party as printed, p code, v votes, w won, lines for fusion}], scat, how (how the\n'
            '# figures were settled), page (PDF page), inc [{n, p, result}] from Wikipedia.\n')
    data = {'year': y, 'date': DATE[y], 'congress': 87 + (y - 1960) // 2,
            'source': {'label': f"Clerk of the House, Statistics of the Presidential and Congressional Election of {DATE[y][:4]}",
                       'url': CLERK.format(y=y)},
            'races': races_out}
    if y % 4 == 0:
        T = president.wiki_table(wiki_page(f'{y}_United_States_presidential_election', cache), y)
        pres = president.races(y, C, d, T, dg)
        cands = [{'k': c['k'], 'n': c['n'], 'party': c['party']} for c in T['cands']]    # 'col' dropped
        for who in sorted({k for v in president.CAST.get(y, {}).values() for k in v if k in president.ELECTEES}):
            if who not in [c['k'] for c in cands]:
                cands.append({'k': who, 'n': president.ELECTEES[who][0], 'party': None, 'like': president.ELECTEES[who][1]})
        data['president'] = {'cands': cands, 'states': pres}
        print(y, len(pres), 'States for President')
    if write:
        body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=200, default_flow_style=None)
        open(os.path.join(OUT, f'{y}.yaml'), 'w', encoding='utf-8').write(head + body)
    print(y, len(races_out), 'races')
    return data


def race_record(y, st, r, lines, key, dg, recap):
    """One or more race records (New Mexico 1962 elected by position) from Wikipedia's race and the Clerk."""
    R = read.READ.get(y, {})
    if r.get('special'):
        # a special election's own reading ('s OR 2 special'); a plain key serves where no regular race
        # is held for the same seat; left unread, it is reported under its special key
        sk = key + ('special',)
        has = lambda k: any(k in t.get(y, ()) for t in (read.READ, read.UNTABULATED, read.WON, read.NOT_IN_VOLUME))
        if has(sk) or not has(key):
            key = sk
    inc = [{'n': i['name'], 'p': code(i.get('party')), 'result': i.get('result', '')} for i in r['incumbents'] if i.get('name')]
    base = {'ch': r['chamber'], 'st': st, 'seat': seat_key(r), 'special': bool(r.get('special'))}
    winners_w = sum(c['won'] for c in r['candidates'])
    # by position: two races
    pos = sorted(k for k in R if k[:2] == key[:2] and isinstance(k[2], str) and k[2].startswith(f'{key[2]}-'))
    if pos and not r.get('special'):
        out = []
        for k in pos:
            rec = dict(base, seat=key[2], position=k[2].split('-', 1)[1], seats=1)
            rec.update(from_read(R[k]))
            rec['how'] = 'read by eye'
            rec['inc'] = inc
            out.append(winners(rec, 1))
        return out
    if key in read.UNTABULATED.get(y, set()):
        rec = dict(base, seats=1, how="unopposed; the State did not tabulate the vote",
                   cands=[{'n': c['name'], 'party': c['party'], 'p': code(c['party']), 'v': None, 'w': True}
                          for c in r['candidates'] if c.get('won') or not any(x.get('won') for x in r['candidates'])],
                   inc=inc)
        return [rec]
    if key in R:
        rec = dict(base, **from_read(R[key]))
        rec['how'] = 'read by eye'
        if key in getattr(read, 'RACE_FROM', {}).get(y, {}):   # another source's figures: where the Clerk prints no
            rec['how'] = 'another source'                     # vote, or the State's canvass, which overrides him
            rec['src'] = read.RACE_FROM[y][key]
            if (y, key) in getattr(read, 'CLERK', {}):
                rec['how'] = "the State's canvass"
                rec['clerk'] = read.CLERK[(y, key)]
        wiki_names(rec['cands'], r['candidates'])
    else:
        if any(c.get('clerk') is None for c in r['candidates']) or not r['candidates']:
            # not in the Clerk's November volume (an earlier special election), or a name the OCR lost
            if key in read.NOT_IN_VOLUME.get(y, {}):
                return None    # an earlier special election, not in the November volume
            leave(y, key, 'unmatched', r, lines)
            return None
        cands, readings = [], []
        for c in r['candidates']:
            e = c['clerk']
            l0 = lines[e['lines'][0]]
            a = match.totals(c)
            readings.append((a, None, None) if e.get('fusion') else (a, dg(st, l0['sec'], l0['k'], 'dg'), dg(st, l0['sec'], l0['k'], 'dg2')))
            cands.append({'n': c['name'], 'party': ', '.join(canon(x) for x in e['parties']), 'p': code(e['parties'][0]), 'v': a})
        for m_ in r.get('minor', []):
            l0 = lines[m_['lines'][0]]
            readings.append((m_['votes'], dg(st, l0['sec'], l0['k'], 'dg'), dg(st, l0['sec'], l0['k'], 'dg2')))
            cands.append({'n': m_['name'], 'party': canon(m_['parties'][0]), 'p': code(m_['parties'][0]), 'v': m_['votes']})
        scat = r.get('scattering')
        nW = len(r['candidates'])

        def pct_ok(vals):
            if any(c['pct'] is None for c in r['candidates']):
                return True
            for T in (sum(vals) + (scat or 0), sum(vals)):
                if T and all(abs(100 * v / T - c['pct']) <= 0.16 for c, v in zip(r['candidates'], vals[:nW])):
                    return True
            return False
        row, tots = recap(st, seat_key(r) if r['chamber'] == 'h' else 's')
        got = reconcile.settle(readings, scat, row, tots, pct_ok)
        if not got:
            leave(y, key, 'unsettled', r, lines)
            return None
        for c, v in zip(cands, got[0]):
            c['v'] = v
        rec = dict(base, cands=cands, how=got[2])
        if scat is not None:
            rec['scat'] = scat
        rec['page'] = lines[r['candidates'][0]['clerk']['lines'][0]]['page']
    rec['inc'] = inc
    rec['seats'] = max(1, winners_w) if r['chamber'] == 'h' and key[2] == 0 else 1
    won = getattr(read, 'WON', {}).get(y, {}).get(key)
    if won:    # no vote printed
        for c in rec['cands']:
            c['w'] = c['n'].split()[-1] == won.split()[-1]
        return [rec]
    return [winners(rec, rec['seats'])]


def wiki_names(cands, wcands):
    """Names as Wikipedia gives them, where a surname matches (the Clerk's misprints: 'Zelenki'); a write-in's
    party from Wikipedia ('Dale Alford, write-in')."""
    import difflib

    def sur(n):
        n = re.sub(r',?\s+(Jr|Sr|II|III)\.?$', '', n.strip())
        return re.sub(r'[^a-z]', '', n.split()[-1].lower()) if n.split() else ''
    for c in cands:
        m = [w for w in wcands if difflib.SequenceMatcher(None, sur(c['n']), sur(w['name'])).ratio() >= 0.75]
        if len(m) == 1:
            c['n'] = m[0]['name']
            if c['p'] == 'O' and code(m[0].get('party')) != 'O' and re.search(r'write|^$', c['party'] or ''):
                c['p'] = code(m[0]['party'])


def from_read(rows):
    cands, scat = [], None
    for row in rows:
        if row[0] == 'Scattering' or re.fullmatch(r'(?i)write-?ins?|others?|scattered|miscellaneous', row[0]):    # an unnamed write-in line is scattering
            scat = (scat or 0) + row[2]
            continue
        c = {'n': row[0], 'party': row[1] or '', 'p': code((row[1] or '').split(',')[0]), 'v': row[2]}
        if len(row) > 3:
            c['lines'] = [list(x) for x in row[3]]
        cands.append(c)
    out = {'cands': cands}
    if scat is not None:
        out['scat'] = scat
    return out


def winners(rec, k):
    vs = sorted((c['v'] or 0 for c in rec['cands']), reverse=True)
    cut = vs[k - 1] if len(vs) >= k else 0
    for c in rec['cands']:
        c['w'] = bool(c['v'] is not None and c['v'] >= cut and cut > 0) or (c['v'] is None and len(rec['cands']) == 1)
    return rec


def senate_prior(cache, years=(1952, 1954, 1956)):
    """elections/senate-prior.yaml: the Democratic two-party share in each State's last regular Senate
    election before the years covered, from Wikipedia's percentages (the Clerk's volumes are not read for these)."""
    out = {}
    for y in years:
        t = f'{y}_United_States_Senate_elections'
        p = os.path.join(cache, f'w_{t}.txt')
        if not os.path.exists(p) or not os.path.getsize(p):
            body = fetch(WIKI.format(t=t))    # fetch before opening, so a failure leaves no empty file
            open(p, 'wb').write(body)
        races = wiki.senate(open(p, encoding='utf-8').read(), {1952: 1, 1954: 2, 1956: 3, 1958: 1}[y])
        shares = {}
        for r in races:
            if r['special']:
                continue
            d = sum(c['pct'] or 0 for c in r['candidates'] if code(c['party']) == 'D')
            rr = sum(c['pct'] or 0 for c in r['candidates'] if code(c['party']) == 'R')
            if d and rr:
                shares[r['st']] = round(100 * d / (d + rr), 1)
            elif d or rr:
                shares[r['st']] = 100.0 if d else 0.0
        out[y] = shares
    head = ('# Generated by tools/elections/make_elections.py (senate_prior). The Democratic share of the two-party vote\n'
            '# in each State\'s regular Senate election of the year, from Wikipedia\'s percentages; the base for Senate swing.\n')
    open(os.path.join(OUT, 'senate-prior.yaml'), 'w').write(head + yaml.safe_dump(out, sort_keys=True))


if __name__ == '__main__':
    main()
    cache = sys.argv[sys.argv.index('--cache') + 1] if '--cache' in sys.argv else os.path.join(tempfile.gettempdir(), 'clerk-ocr')
    senate_prior(cache)
