"""The presidential vote by State, for elections/<year>.yaml ('pres').

The Clerk's volume prints, under each State, "For Presidential Electors": a line a slate, the party as printed
and the highest vote cast for any of its electors; the State's recapitulation repeats the figures in a row,
"Presidential electors", with their total. Each figure is read three times (the page's OCR and the two
digits-only readings, as for the House and Senate) and settled as they are: the readings agree and the slates
sum to the recapitulation's total; or they sum to it; or two of three readings agree and the figures match
Wikipedia's results by State. A State that does not settle is read by eye (read.PRES).

Slates are assigned to candidates by Wikipedia's figures (a slate whose vote is the candidate's, or, with
New York's Liberal and Conservative lines, part of it), else by party. The electoral votes are Wikipedia's,
with the electors who did not vote for their slate's candidate set out in CAST.
"""
import re

import read
import reconcile
from wiki import st_of, unlink

# Electors as they voted, where a State's did not all vote for the candidate whose slate won.
CAST = {
    1956: {'AL': {'D': 10, 'Jones': 1}},    # an elector pledged to Stevenson voted for Walter B. Jones
    1960: {'AL': {'D': 5, 'Byrd': 6}, 'MS': {'Byrd': 8}, 'OK': {'R': 7, 'Byrd': 1}},
    1968: {'NC': {'R': 12, 'A': 1}},
    1972: {'VA': {'R': 11, 'Hospers': 1}},
}
# A slate's candidate where Wikipedia's figures would assign it otherwise (year, State, party as printed).
SLATE = {(1960, 'AL', 'Democratic'): 'D'}    # five Kennedy electors and six unpledged: counted with Kennedy (NOTES)
# A note for the State's row in the table.
NOTES = {
    (1960, 'AL'): 'The Democratic slate: five electors pledged to Kennedy, six unpledged; its vote is counted with Kennedy.',
    (1964, 'AL'): 'Johnson had no slate; the Democratic slate was unpledged.',
    (1968, 'AL'): 'Humphrey ran on two slates, the Democratic and the National Democratic.',
    (1968, 'CA'): 'The Clerk\'s figures run under the State\'s canvass as Wikipedia gives it: Nixon 3,467,664, Humphrey 3,244,318, Wallace 487,270.',
    (1972, 'AL'): 'McGovern ran on two slates, the Democratic and the National Democratic.',
    (1972, 'CA'): 'The Clerk\'s figures run under the State\'s canvass as Wikipedia gives it: Nixon 4,602,096, McGovern 3,475,847.',
}
# Wikipedia's column heads, where they are not the candidate's name.
NAMES = {'T. Coleman Andrews/Unpledged Electors': 'T. Coleman Andrews; unpledged electors', 'Unpledged Electors': 'Unpledged electors',
         'Nixon/Agnew': 'Richard Nixon', 'McGovern/Shriver': 'George McGovern', 'Schmitz/Anderson': 'John G. Schmitz',
         'Hospers/Nathan': 'John Hospers'}
# Who received electoral votes without a slate of their own.
ELECTEES = {'Jones': ('Walter B. Jones', 'O'), 'Byrd': ('Harry F. Byrd', 'U'), 'Hospers': ('John Hospers', 'O')}


def num(c):
    c = re.sub(r"'{2,}|<[^>]*>|\{\{[^}]*\}\}", '', c).strip()
    c = re.sub(r'^[^|]*\|\s*(?=[\d–\-—])', '', c) if '=' in c.split('|')[0] else c
    m = re.fullmatch(r'\s*([\d,]+(?:\.\d+)?)\s*', c)
    return float(m.group(1).replace(',', '')) if m and '.' in m.group(1) else int(m.group(1).replace(',', '')) if m else None


def cells(row):
    """A wikitable row's cells, attributes dropped."""
    out = []
    for c in re.split(r'\n[|!]|\|\||!!', '\n' + row.strip()):
        if not c.strip() or c.startswith('-'):
            continue
        if re.match(r'\s*[\w\-]+\s*=\s*"?[^|\[\]{}]*"?\s*\|(?!\|)', c):    # style="..." | value
            c = c.split('|', 1)[1]
        out.append(c.strip())
    return out


def wiki_table(text, year=None):
    """{'cands': [{'n', 'party', 'k'}], 'states': {ST: {'votes': [..], 'ev': [..], 'total'}}} from 'Results by state'."""
    m = re.search(r'^===+\s*Results by state\s*===+', text, re.M | re.I)
    body = text[m.end():]
    t = re.search(r'\{\|\s*class="wikitable sortable', body).start()
    body = body[t:body.index('\n|}', t)]
    rows = re.split(r'\n\|-[^\n]*', body)[1:]
    # header 1: groups (label, width, spans both rows)
    h1 = [c for c in re.split(r'\n!', '\n' + rows[0].strip()) if c.strip()]
    groups = []
    for c in h1:
        c = re.sub(r'\{\{[Ee]fn\|(?:[^{}]|\{\{[^{}]*\}\})*\}\}|\{\{verth\|stp=1\|', '', c)
        w = re.search(r'colspan\s*=\s*"?(\d+)', c)
        both = bool(re.search(r'rowspan\s*=\s*"?2', c))
        label = unlink(re.sub(r'.*?\|\s*(?=[^|]*$)', '', c) if '[[' not in c else c[c.rindex('|', 0, c.index('[[')) + 1:] if '|' in c[:c.index('[[')] else c)
        label = re.sub(r'^\s*(?:[\w\-]+\s*=\s*"?[^"|\s]*"?\s*)+', '', re.sub(r'\{\{[^}]*\}\}|\}\}', '', label))
        groups.append({'label': label.strip(), 'w': int(w.group(1)) if w else 1, 'both': both})
    h2 = [c.split('|')[-1].lower() for c in re.split(r'\n!', '\n' + rows[1].strip()) if c.strip()]
    cols, k = [], 0
    for g in groups:
        for i in range(g['w']):
            if g['both']:
                sub = ''
            else:
                sub = h2[k] if k < len(h2) else ''
                k += 1
            kind = 'ev' if ('electoral' in sub or 'ev' in sub.split('}')[0][-4:] or 'abbr|ev' in sub) else 'pct' if '%' in sub else 'n'
            cols.append((g['label'], kind))
    cands = []
    for g in groups:
        lab = g['label']
        if '<br' not in lab.lower() or re.match(r'(State|Margin|Total)', lab, re.I):
            continue
        name, _, party = re.split(r'<br\s*/?>', lab, maxsplit=1)[0], None, re.split(r'<br\s*/?>', lab)[-1]
        cands.append({'n': name.strip(), 'party': party.strip()})
    for c in cands:
        p = c['party']
        c['col'] = c['n']    # Wikipedia's column head, for finding the column
        c['n'] = NAMES.get(c['n'], c['n'].split('/')[0].strip())
        c['k'] = 'D' if p.startswith('Democratic') else 'R' if p.startswith('Republican') else \
            'U' if 'npledged' in p + c['n'] else 'A' if 'American Independent' in p else c['n'].split()[-1]
    states = {}
    for r in rows[2:]:
        cs = cells(r)
        if not cs:
            continue
        nm = re.sub(r'\{\{nowrap\|(.*)\}\}', r'\1', cs[0])
        nm = re.sub(r'\{\{abbrlink\|([^|}]+)[^}]*\}\}', r'\1', nm)
        nm = unlink(nm).replace('†', '').strip()
        st = 'DC' if 'Columbia' in cs[0] else st_of(nm)
        dm = re.match(r'([A-Z]{2})[\-–](\d)', nm)    # Maine's districts, 1972: their electoral votes go to the State
        if dm and dm.group(1) in states:
            for i, (lab, kind) in enumerate(cols):
                for j, c in enumerate(cands):
                    if kind == 'ev' and (lab.startswith(c['col']) or c['col'] in lab) and i < len(cs):
                        states[dm.group(1)]['ev'][j] += num(cs[i]) or 0
            continue
        if not st or st in states:
            continue
        rec = {'votes': [], 'ev': [], 'total': None, 'ev_total': None, 'year': year}
        ci = 0
        for (lab, kind), v in zip(cols, cs):
            if lab.lower().startswith('state') and kind == 'ev' or (lab == '' and kind == 'ev' and ci == 1):
                rec['ev_total'] = num(v)
            ci += 1
        for c in cands:
            idx = [i for i, (lab, kind) in enumerate(cols) if lab.startswith(c['col']) or c['col'] in lab]
            get = {kind: num(cs[i]) if i < len(cs) else None for i in idx for lab, kind in [cols[i]]}
            rec['votes'].append(get.get('n'))
            rec['ev'].append(get.get('ev') or 0)
        tot = [i for i, (lab, kind) in enumerate(cols) if 'total' in lab.lower() and kind == 'n']
        rec['total'] = num(cs[tot[0]]) if tot and tot[0] < len(cs) else None
        states[st] = rec
    return {'cands': cands, 'states': states}


def assign(st, parties, vals, W, cands):
    """Each slate's candidate key: by Wikipedia's figure (exact, then within 1%), else by party."""
    wv = W['votes']
    keys = []
    for p, v in zip(parties, vals):
        k = None
        exact = [c['k'] for c, x in zip(cands, wv) if x and v == x]
        close = [c['k'] for c, x in zip(cands, wv) if x and v and abs(v - x) <= 0.01 * x]
        low = p.lower()
        if (W.get('year'), st, p) in SLATE:
            k = SLATE[(W['year'], st, p)]
        elif len(exact) == 1:
            k = exact[0]
        elif st == 'NY' and 'liberal' in low:
            k = 'D'
        elif st == 'NY' and 'conservative' in low:
            k = 'R'
        elif 'unpledged' in low and any(c['k'] == 'U' for c in cands):
            k = 'U'
        elif low.startswith('dem'):
            k = 'D'
        elif low.startswith('rep'):
            k = 'R'
        elif len(close) == 1:
            k = close[0]
        elif 'american' in low and any(c['k'] == 'A' for c in cands):
            k = 'A'
        keys.append(k or 'O')
    # a candidate on a second slate ('National Democratic Party of Alabama'): the slate that completes his figure
    for c, x in zip(cands, wv):
        got = sum(v or 0 for k, v in zip(keys, vals) if k == c['k'])
        for i, (k, v) in enumerate(zip(keys, vals)):
            if x and got != x and k == 'O' and v and got + v == x:
                keys[i] = c['k']
                break
    return keys


def totals_by(keys, vals):
    out = {}
    for k, v in zip(keys, vals):
        out[k] = out.get(k, 0) + (v or 0)
    return out


def races(y, C, d, T, dg):
    """One record a State: {st, ev, slates [{party, k, v}], scat, cands [{k, v}], cast {k: electors}, how, page}."""
    R = getattr(read, 'PRES', {}).get(y, {})
    cands = T['cands']
    out = []
    for st, W in sorted(T['states'].items()):
        ev = sum(CAST[y][st].values()) if st in CAST.get(y, {}) else sum(W['ev'])    # Wikipedia leaves out Jones, 1956
        lines = [l for l in C.get(st, {}).get('pres', []) if not re.match(r'(?i)\W*blank', l['party'])]
        rec = {'st': st, 'ev': ev}
        if st in R:
            sc = re.compile(r'(?i)scatter|write-?ins?$')
            slates = [{'party': p, 'v': v} for p, v in R[st] if not sc.match(p)]
            scat = sum(v for p, v in R[st] if sc.match(p)) if any(sc.match(p) for p, _ in R[st]) else None
            how = getattr(read, 'PRES_FROM', {}).get((y, st), 'read by eye')
        else:
            sl = [l for l in lines if not re.match(r'(?i)\W*s[ce]at', l['party'])]
            sc = [l for l in lines if re.match(r'(?i)\W*s[ce]at', l['party'])]
            if not sl:
                import sys
                sys.stderr.write(f'unmatched {y} pres {st}: no slates read\n')
                continue
            readings = [(l['votes'], dg(st, 'pres', l['k'], 'dg'), dg(st, 'pres', l['k'], 'dg2')) for l in sl]
            scat = reconcile.majority([sc[0]['votes'], dg(st, 'pres', sc[0]['k'], 'dg'), dg(st, 'pres', sc[0]['k'], 'dg2')]) if sc else None
            row, tots = [], []
            for k, r in enumerate(C.get(st, {}).get('recap', [])):
                if re.search(r'(?i)presid|elector', r['raw']):
                    ns = reconcile.nums(r['raw'])
                    ex = [dg(st, 'recap', k, 'dg'), dg(st, 'recap', k, 'dg2')]
                    row = ns + [x for x in ex if x]
                    tots = sorted({x for x in [ns[-1] if ns else None] + ex if x})
                    break
            parties = [l['party'] for l in sl]

            def pct_ok(vals):
                keys = assign(st, parties, vals, W, cands)
                got = totals_by(keys, vals)
                tot = sum(vals) + (scat or 0)
                for c, wv in zip(cands, W['votes']):
                    if c['k'] in ('D', 'R', 'A', 'U') and wv and W['total']:
                        if abs(100 * got.get(c['k'], 0) / tot - 100 * wv / W['total']) > 0.16:
                            return False
                return True
            got = reconcile.settle(readings, scat, row, tots, pct_ok)
            if not got:
                import sys
                sys.stderr.write(f'unsettled {y} pres {st}: add a reading to read.PRES\n')
                continue
            slates = [{'party': p, 'v': v} for p, v in zip(parties, got[0])]
            how = got[2]
            rec['page'] = sl[0]['page']
        keys = assign(st, [s['party'] for s in slates], [s['v'] for s in slates], W, cands)
        for s, k in zip(slates, keys):
            s['k'] = k
        rec['slates'] = slates
        if scat is not None:
            rec['scat'] = scat
        rec['how'] = how
        if (y, st) in NOTES:
            rec['note'] = NOTES[(y, st)]
        by = totals_by([s['k'] for s in slates], [s['v'] for s in slates])
        win = max(by, key=by.get)    # the candidate's slates together (New York's Democratic and Liberal lines)
        rec['cast'] = dict(CAST.get(y, {}).get(st) or {win: ev})
        if sum(rec['cast'].values()) != ev and st not in CAST.get(y, {}):
            rec['cast'] = {win: ev}
        out.append(rec)
    return out
