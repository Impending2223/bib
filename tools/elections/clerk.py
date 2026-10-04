"""Read the Clerk's Statistics of the Congressional Election from OCR (tesseract TSV, one per page).

lines(dir) -> [(page, top, bottom, text)]
states(lines) -> {ST: {'senate': [...], 'house': [...], 'recap': [...]}}, each a list of parsed lines:
    {'name', 'party', 'votes', 'num' (a district number printed on the line), 'page', 'top', 'bottom', 'raw'}.
    A fusion line ('| Liberal ... 85,619') has name None and belongs to the candidate above it.
Votes are the last number on the line (the leader dots throw up stray digits before it).
"""
import csv
import glob
import os
import re

from wiki import ABBR

CAPS = {k.upper().replace(' ', ''): v for k, v in ABBR.items()}


def lines(d):
    out = []
    for f in sorted(glob.glob(os.path.join(d, 'p-*.tsv'))):
        page = int(re.search(r'p-(\d+)', f).group(1))
        rows = {}
        with open(f, encoding='utf-8') as fh:
            for r in csv.DictReader(fh, delimiter='\t', quoting=csv.QUOTE_NONE):
                if r['level'] != '5' or not r['text'].strip():
                    continue
                k = (r['block_num'], r['par_num'], r['line_num'])
                t, h = int(r['top']), int(r['height'])
                x = rows.setdefault(k, {'w': [], 'top': t, 'bot': t + h})
                x['w'].append((int(r['left']), r['text']))
                x['top'], x['bot'] = min(x['top'], t), max(x['bot'], t + h)
        for k, x in sorted(rows.items(), key=lambda kv: kv[1]['top']):
            ws = sorted(x['w'])
            # where the figure at the end of the line begins: its leading number tokens
            fx = None
            for left, w in reversed(ws):
                if re.fullmatch(r'[\d,.]+', w):
                    fx = left
                else:
                    break
            out.append((page, x['top'], x['bot'], ' '.join(w for _, w in ws), fx))
    return out


NUM = r'(\d{1,3}(?:[,.]\s?\d{3})+|\d{1,6})'
TAIL = re.compile(NUM + r'[^\d]{0,6}$')
PARTY = (r'Democrat\w*|Demo\w*|Dem\w+|Republi\w*|Repub\w*|Liberal|Conservative|Constitution|Prohibition|'
         r'Independent[\w ]*|Socialist[\w ]*|Farmer[\w\- ]*|Tax[\w ]*|Nuberal|Tiberal|Libera\w*')
SUFFIX = r'(?:,\s*(?:Jr|Sr|J[rt])\.?|,?\s*I{2,3})?'
LINE = re.compile(r'^(?P<pre>.{0,8}?)(?P<name>[A-Z][^_]{1,60}?' + SUFFIX + r'),\s*(?P<party>[A-Z][A-Za-z\- ]{2,30}?)[\s_.\-~:;|,\'"‘’`]')
LINE2 = re.compile(r'^(?P<pre>.{0,8}?)(?P<name>[A-Z][^_]{1,60}?' + SUFFIX + r')\s+(?P<party>' + PARTY + r')\b')
FUSION = re.compile(r'^.{0,8}?(?P<party>Liberal|Conservative|Democrat|Republican|Nuberal|Tiberal|Libera\w*)\b')
SCAT = re.compile(r'^.{0,8}?S[ce][ae]?t+[et]?ering')


def votes(s):
    return int(re.sub(r'\D', '', s))


def last_num(u):
    m = TAIL.search(u)
    return votes(m.group(1)) if m else None


def fix_party(p):
    p = p.strip(' _.-')
    for good, pats in (('Democrat', ('Dem',)), ('Republican', ('Rep',)), ('Liberal', ('Libera', 'Nuberal', 'Tiberal'))):
        if any(p.startswith(x) for x in pats):
            return good
    return p


def states(ls):
    out, st, sec = {}, None, None
    for page, top, bot, t, fx in ls:
        u = t.strip()
        key = re.sub(r'[^A-Z]', '', re.split(r'[—–-]', u)[0])
        if key in CAPS and (u.isupper() or '—' in u or 'Continued' in u):
            if CAPS[key] != st and 'Continued' not in u and '—' not in u:
                sec = None
            st = CAPS[key]
            out.setdefault(st, {'senate': [], 'house': [], 'recap': []})
            continue
        if st is None:
            continue
        low = u.lower()
        if low.startswith('for') and ('elector' in low or 'ectoral' in low or 'presid' in low or 'governor' in low):
            sec = 'other'
            continue
        # "For United States Senator" ("Unirep" in the OCR), "For Representatives"
        if low.startswith('for') and 'sena' in low:
            sec = 'senate'
            continue
        if low.startswith('for') and ('rese' in low or 'repr' in low):
            sec = 'house'
            continue
        if 'recapitulation' in low or 'recapiiulation' in low:
            sec = 'recap'
            continue
        if sec in (None, 'other'):
            continue
        rec = {'page': page, 'top': top, 'bottom': bot, 'raw': u, 'fx': fx}
        dm = re.match(r'^\W{0,2}(\d{1,2})\s?[.,]', u)
        if dm:
            rec['num'] = int(dm.group(1))
        if sec == 'recap':
            out[st]['recap'].append(rec)
            continue
        v = last_num(u)
        if v is None:
            continue
        rec['votes'] = v
        text = re.split(r'_{2,}|\.{3,}|-{3,}|[_.\-~]{4,}', u)[0]
        if SCAT.match(text) or SCAT.match(u):
            rec.update(name='Scattering', party='')
            out[st][sec].append(rec)
            continue
        if re.match(r'^\W*(Total|Majority|Plurality|CONGRESSIONAL|Title)', text):
            continue
        pm = list(re.finditer(r'\b(' + PARTY + r')\b', text))
        if pm:
            party_at, party = pm[-1].start(), pm[-1].group(1)
        elif ',' in text:
            party_at = text.rindex(',') + 1
            party = text[party_at:]
        else:
            continue
        name = re.sub(r'^[\W\d]*(?:[a-z]\W+)?', '', text[:party_at]).strip(' ,.;:|')
        rec['party'] = fix_party(party)
        rec['name'] = name if re.search(r'[A-Za-z]{2}', name) else None   # a fusion line: a party alone
        out[st][sec].append(rec)
    return out
