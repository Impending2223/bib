"""Reading by eye what the OCR leaves: the races and States make_elections.py could not settle.

    python3 tools/elections/review.py left YEAR            list what is left, with pages (writes WORK/YEAR/left.json)
    python3 tools/elections/review.py sheets YEAR [--only NY,NJ] [--skip NY] [--prefix s]
                                                           page crops of those races, six to a sheet, labeled with
                                                           Wikipedia's names and percentages (WORK/YEAR/s_NN.png)
    python3 tools/elections/review.py pages YEAR PAGE...   whole pages in thirds, for a State read whole (pg_NN_a.png)
    python3 tools/elections/review.py locate YEAR ST...    the pages a State's section spans
    python3 tools/elections/review.py verify YEAR FILE...  readers' files against the OCR's numbers and Wikipedia
    python3 tools/elections/review.py merge YEAR FILE...   readers' files into elections/readings/YEAR.yaml
    python3 tools/elections/review.py audit [YEAR...]      seat tallies, electoral votes, and the President by
                                                           State against Wikipedia, for a last look

Options: --cache DIR (the OCR cache, as for make_elections.py; default $TMPDIR/clerk-ocr) and --work DIR (sheets
and left.json; default $TMPDIR/elections-review).

The loop, for a new or corrected year:
  1. make_elections.py YEAR; review.py left YEAR.
  2. review.py sheets YEAR (States with many races left, New York always: --skip them, and review.py pages for
     their pages, from review.py locate).
  3. Give each reader (a person, or an agent) tools/elections/review/READER.md (House and Senate) or PRESIDENT.md, the
     sheets or pages, and an output path. A reader writes the readings schema (tools/elections/read.py).
  4. review.py verify YEAR FILE...: every figure is checked against the OCR's numbers for its lines and against
     Wikipedia's percentages; a CHECK line is a figure neither supports. Look at each one on the page.
  5. Settle disagreements between the race page and the recapitulation by the rule in read.py, with a note.
  6. review.py merge YEAR FILE...; make_elections.py YEAR again (it should leave nothing); review.py audit YEAR;
     ./bib check.
"""
import argparse
import difflib
import json
import os
import re
import sys
import tempfile

import yaml

sys.path.insert(0, os.path.dirname(__file__))
import clerk           # noqa: E402
import make_elections  # noqa: E402
import president       # noqa: E402

READINGS = os.path.join(os.path.dirname(__file__), '..', '..', 'elections', 'readings')
SC = re.compile(r'(?i)scatter|write-?ins?$|others?$|miscellaneous$')


def work(a, y):
    d = os.path.join(a.work, str(y))
    os.makedirs(d, exist_ok=True)
    return d


# ---------------------------------------------------------------- left, sheets, pages, locate

def cmd_left(a):
    make_elections.LEFT.clear()
    president.LEFT.clear()
    make_elections.year(a.year, a.cache, write=False)
    left = make_elections.LEFT + [dict(x, president=True, pages=pages_of(a, a.year, x['st'])) for x in president.LEFT]
    json.dump(left, open(os.path.join(work(a, a.year), 'left.json'), 'w'), indent=1)
    for x in left:
        if x.get('president'):
            print(f"president {x['st']}: {x['why']}; pages {x['pages']}")
        else:
            k = x['key']
            print(f"{k[0]} {k[1]} {k[2]}: {x['why']}; page {x['loc'][0] if x['loc'] else '?'}; "
                  + '; '.join(f'{n} {p}' for n, _, p in x['wiki']))
    print(len(left), 'left')


def cmd_sheets(a):
    from PIL import Image, ImageDraw
    d = work(a, a.year)
    left = json.load(open(os.path.join(d, 'left.json')))
    only = set(a.only.split(',')) if a.only else None
    skip = set(a.skip.split(',')) if a.skip else set()
    crops, no = [], []
    for x in left:
        if x.get('president'):
            continue
        k = x['key']
        if (only and k[1] not in only) or k[1] in skip:
            continue
        seat = f"Sen{k[2]}" if k[0] == 's' else k[2]
        if not x['loc']:
            no.append(f'{k[1]} {seat}')
            continue
        pg, top, bot = x['loc']
        im = Image.open(os.path.join(a.cache, str(a.year), f'p-{pg:02d}.png'))
        W, H = im.size
        c = im.crop((int(W * 0.08), max(0, top), int(W * 0.94), min(H, bot))).convert('L')
        c = c.resize((c.width * 3 // 4, c.height * 3 // 4))
        lab = Image.new('L', (c.width, 30), 255)
        tag = f'{k[1]} {seat}  p.{pg}: ' + '; '.join(f'{n} {p}' for n, _, p in x['wiki'])
        ImageDraw.Draw(lab).text((4, 8), tag[:180], fill=0)
        crops.append((lab, c))
    n = 0
    for i in range(0, len(crops), 6):
        grp = crops[i:i + 6]
        sh = Image.new('L', (max(x.width for p in grp for x in p), sum(a_.height + b.height + 14 for a_, b in grp)), 255)
        yy = 0
        for lab, c in grp:
            sh.paste(lab, (0, yy)); yy += lab.height
            sh.paste(c, (0, yy)); yy += c.height + 14
        sh.save(os.path.join(d, f'{a.prefix}_{n:02d}.png'))
        n += 1
    print(n, 'sheets in', d, '; no place on the page (find them with locate):', ', '.join(no) or 'none')


def cmd_pages(a):
    from PIL import Image
    d = work(a, a.year)
    for p in a.pages:
        im = Image.open(os.path.join(a.cache, str(a.year), f'p-{int(p):02d}.png'))
        W, H = im.size
        for i, (t, b) in enumerate(((0, 0.38), (0.31, 0.69), (0.62, 1.0))):
            im.crop((int(W * 0.06), int(H * t), int(W * 0.95), int(H * b))).save(os.path.join(d, f'pg_{int(p):02d}_{"abc"[i]}.png'))
    print('page thirds in', d)


def pages_of(a, y, st):
    L = clerk.lines(os.path.join(a.cache, str(y)))
    H = clerk.headings(L)
    first = {}
    for i, v in sorted(H.items()):
        first.setdefault(v, L[i][0])
    order = sorted(first.items(), key=lambda kv: kv[1])
    if st not in first:
        return []
    i = [k for k, _ in order].index(st)
    end = order[i + 1][1] if i + 1 < len(order) else first[st] + 2
    return list(range(first[st], end + 1))


def cmd_locate(a):
    for st in a.states:
        print(st, pages_of(a, a.year, st) or "no heading found: look between its neighbours")


# ---------------------------------------------------------------- verify, merge

def load_files(files):
    out = {'races': {}, 'president': {}}
    for f in files:
        d = yaml.safe_load(open(f, encoding='utf-8')) or {}
        for part in ('races', 'president'):
            for k, v in (d.get(part) or {}).items():
                if k in out[part]:
                    print('twice:', k, f)
                out[part][k] = v
    return out


def sur(n):
    n = re.sub(r',?\s+(Jr|Sr|II|III)\.?$', '', (n or '').strip())
    return re.sub(r'[^a-z]', '', n.split()[-1].lower()) if n.split() else ''


def numbers(lines):
    return {int(re.sub(r'\D', '', m)) for s in lines for m in re.findall(r'\d[\d,. ]*\d|\d', s) if re.sub(r'\D', '', m)}


def cmd_verify(a):
    left = {' '.join(map(str, x['key'])): x for x in json.load(open(os.path.join(work(a, a.year), 'left.json'))) if not x.get('president')}
    R = load_files(a.files)
    bad = 0
    for k, v in R['races'].items():
        rows = [r for r in v['cands'] if not re.match(r'(?i)blank', r[0])]
        x = left.get(k)
        if not x:
            continue    # read whole, settled already: the recapitulation is the check
        figs = [r[2] for r in rows if r[2] is not None]
        ocr = numbers(x['ocr'])
        miss = [r[2] for r in rows if r[2] is not None and r[2] not in ocr and not (len(r) > 3)]
        miss += [v_ for r in rows if len(r) > 3 for _, v_ in r[3] if v_ not in ocr]
        tot, scat = sum(figs), sum(r[2] for r in rows if SC.match(r[0]) and r[2])
        wiki_ok = None
        if x['wiki'] and all(p is not None for _, _, p in x['wiki']) and tot:
            wiki_ok = any(all(
                (m := [r for r in rows if not SC.match(r[0]) and difflib.SequenceMatcher(None, sur(r[0]), sur(n)).ratio() >= 0.75])
                and m[0][2] is not None and abs(100 * m[0][2] / T - p) <= 0.16 for n, _, p in x['wiki']) for T in (tot, tot - scat))
        if miss and not wiki_ok:
            bad += 1
            print('CHECK', k, '| not in the OCR:', miss, '| Wikipedia', {True: 'agrees', False: 'differs', None: 'n/a'}[wiki_ok],
                  x['wiki'], '|', rows)
    T = president.wiki_table(make_elections.wiki_page(f'{a.year}_United_States_presidential_election', a.cache), a.year) \
        if R['president'] else None
    for st, v in R['president'].items():
        W = T['states'].get(st)
        sl = [(p, n) for p, n in v['slates'] if not SC.match(p)]
        keys = president.assign(st, [p for p, _ in sl], [n for _, n in sl], W, T['cands'])
        got = president.totals_by(keys, [n for _, n in sl])
        diffs = [f"{c['k']} {got.get(c['k'], 0):,} against {w:,}" for c, w in zip(T['cands'], W['votes']) if w and got.get(c['k'], 0) != w]
        if diffs:
            print('LOOK', 'president', st, '| Wikipedia differs:', '; '.join(diffs), '| slates as', keys)
    print(len(R['races']), 'races,', len(R['president']), 'States read;', bad, 'to check on the page')


class Flow(list):
    pass


class Dumper(yaml.SafeDumper):
    pass


Dumper.add_representer(Flow, lambda d, x: d.represent_sequence('tag:yaml.org,2002:seq', x, flow_style=True))
Dumper.add_representer(str, lambda d, s: d.represent_scalar('tag:yaml.org,2002:str', s, style='>' if len(s) > 90 else None))


def cmd_merge(a):
    p = os.path.join(READINGS, f'{a.year}.yaml')
    R = yaml.safe_load(open(p, encoding='utf-8')) if os.path.exists(p) else {'year': a.year}
    new = load_files(a.files)
    races = R.get('races') or {}
    unt = set(R.get('untabulated') or [])
    for k, v in new['races'].items():
        rows = [r for r in v['cands'] if not re.match(r'(?i)blank', r[0])]
        named = [r for r in rows if not SC.match(r[0])]
        if len(named) == 1 and named[0][2] is None:
            unt.add(k)    # unopposed and untabulated: the Clerk's footnote
            continue
        if k in races:
            print('replaced:', k)
        e = {'cands': [Flow(r if len(r) < 4 else r[:3] + [[list(x) for x in r[3]]]) for r in rows]}
        if v.get('note'):
            e['note'] = v['note']
        races[k] = e
    if races:
        R['races'] = dict(sorted(races.items(), key=lambda kv: (kv[0].split()[1], kv[0].split()[0] != 's', kv[0].split()[2].zfill(4))))
    if unt:
        R['untabulated'] = sorted(unt)
    pres = R.get('president') or {}
    for st, v in new['president'].items():
        e = {'slates': [Flow(x) for x in v['slates'] if not re.match(r'(?i)blank', x[0])]}
        for f in ('source', 'note'):
            if v.get(f):
                e[f] = v[f]
        pres[st] = e
    if pres:
        R['president'] = dict(sorted(pres.items()))
    save(a.year, R)
    print('merged into', p, '; now rerun make_elections.py', a.year)


def save(y, R):
    """Write a year's readings in the schema's order and layout (a row a line)."""
    for k in ('races', 'untabulated', 'won', 'wikipedia_differs', 'not_in_volume', 'president'):
        if k in R:
            R[k] = R.pop(k)
    for v in (R.get('races') or {}).values():
        v['cands'] = [Flow(r if len(r) < 4 else list(r[:3]) + [[list(x) for x in r[3]]]) for r in v['cands']]
        if 'note' in v:
            v['note'] = v.pop('note')
    for v in (R.get('president') or {}).values():
        v['slates'] = [Flow(x) for x in v['slates']]
    head = (f"# {y}: figures read by eye from the Clerk's page images where the OCR did not settle\n"
            f"# (schema and rules: tools/elections/read.py). Generated returns: elections/{y}.yaml.\n")
    open(os.path.join(READINGS, f'{y}.yaml'), 'w', encoding='utf-8').write(
        head + yaml.dump(R, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=110, default_flow_style=None))


# ---------------------------------------------------------------- audit

def cmd_audit(a):
    from collections import Counter
    root = os.path.join(os.path.dirname(__file__), '..', '..')
    sys.path.insert(0, root)
    from tools.bib import elections as E
    data = E.load()
    for y in (a.years or sorted(data)):
        D = data[y]
        print(f'== {y}')
        for ch in ('h', 's'):
            won = Counter(E.caucus(c) for r in D['races'] if r['ch'] == ch for c in r['cands'] if c.get('w'))
            print(' ', 'House' if ch == 'h' else 'Senate', dict(won), sum(won.values()),
                  '| read by eye:', sum(1 for r in D['races'] if r['ch'] == ch and r.get('how') == 'read by eye'))
        if D.get('president'):
            ev = Counter()
            for r in D['president']['states']:
                ev.update(r['cast'])
            print('  electoral votes', dict(ev), sum(ev.values()))
            T = president.wiki_table(make_elections.wiki_page(f'{y}_United_States_presidential_election', a.cache), y)
            for r in D['president']['states']:
                W = T['states'].get(r['st'])
                got = Counter()
                for s_ in r['slates']:
                    got[s_['k']] += s_['v']
                diffs = [f"{c['k']} {got.get(c['k'], 0):,}/{w:,}" for c, w in zip(T['cands'], W['votes']) if w and got.get(c['k'], 0) != w]
                if diffs:
                    print(f"  {r['st']} differs from Wikipedia (Clerk/Wikipedia): {'; '.join(diffs)} [{r['how']}]")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--cache', default=os.path.join(tempfile.gettempdir(), 'clerk-ocr'))
    ap.add_argument('--work', default=os.path.join(tempfile.gettempdir(), 'elections-review'))
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('left', 'sheets', 'pages', 'locate', 'verify', 'merge'):
        p = sub.add_parser(name)
        p.add_argument('year', type=int)
        if name == 'sheets':
            p.add_argument('--only'); p.add_argument('--skip'); p.add_argument('--prefix', default='s')
        if name == 'pages':
            p.add_argument('pages', nargs='+')
        if name == 'locate':
            p.add_argument('states', nargs='+')
        if name in ('verify', 'merge'):
            p.add_argument('files', nargs='+')
    p = sub.add_parser('audit')
    p.add_argument('years', type=int, nargs='*')
    a = ap.parse_args()
    globals()['cmd_' + a.cmd](a)


if __name__ == '__main__':
    main()
