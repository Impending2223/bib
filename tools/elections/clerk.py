"""Read the Clerk's Statistics of the Congressional Election from OCR (tesseract TSV, one per page).

lines(dir) -> [(page, top, bottom, text)]
states(lines) -> {ST: {'senate': [...], 'house': [...], 'recap': [...], 'pres': [...]}}, each a list of parsed lines:
    {'name', 'party', 'votes', 'num' (a district number printed on the line), 'page', 'top', 'bottom', 'raw'}.
    A fusion line ('| Liberal ... 85,619') has name None and belongs to the candidate above it.
'pres' holds the presidential electors' lines: the slate's party as printed, and its vote.
Votes are the last number on the line (the leader dots throw up stray digits before it).
"""
import csv
import difflib
import glob
import os
import re

from wiki import ABBR

CAPS = {k.upper().replace(' ', ''): v for k, v in ABBR.items()}
CAPS['DISTRICTOFCOLUMBIA'] = 'DC'
BYLEN = sorted(CAPS, key=len, reverse=True)


def heading(u):
    """The State a heading line names, through the OCR's noise ('E - OHIO oes Pe LOE gy', 'oo “RENNESSEE'):
    a short line of capitals holding a State's name, the longest name first (ARKANSAS, not KANSAS)."""
    low = u.lower().lstrip(' -—–|.:;\'"‘“')
    if len(u) > 60 or 'recapitulation' in low or low.startswith(('for ', 'title', 'total', 'statistics', 'congressional')):
        return None
    letters = re.sub(r'[^A-Za-z]', '', u)
    if len(letters) < 4 or sum(c.isupper() for c in letters) < 0.55 * len(letters):
        return None
    caps = re.sub(r'[^A-Z]', '', u)
    for k in BYLEN:
        if k in caps:
            return CAPS[k]
    for w in re.findall(r'[A-Z]{5,}', u):
        near = difflib.get_close_matches(w, BYLEN, n=1, cutoff=0.85)
        if near:
            return CAPS[near[0]]
    return None


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


def in_caps(u):
    """A State named in a line's capitals, longest name first."""
    caps = re.sub(r'[^A-Z]', '', u)
    return next((CAPS[k] for k in BYLEN if k in caps), None)


def section(u):
    return re.match(r'^[\W\w]{0,8}?\bfor\s+(?:u|p|r|d|g|s)\w', u.lower()) is not None and not re.search(r'\d{2}', u[:8])


def headings(ls):
    """Line index -> the State whose heading it is. Besides heading(): a line just above a section ('For ...')
    holding a State's name in capitals; and, where the OCR lost a heading altogether, the State its
    recapitulation names, placed at the first section after the last State's recapitulation."""
    out, recaps = {}, []
    for i, (page, top, bot, t, fx) in enumerate(ls):
        u = t.strip()
        h = heading(u)
        if not h and i + 1 < len(ls) and section(ls[i + 1][3]) and not section(u) and len(u) < 60:
            h = in_caps(u)
        if h:
            out[i] = h
        m = re.search(r'RECAPITULATION OF VOTES CAST (?:IN|1N|IX)\s+(.*)', u)
        if m:
            recaps.append((i, in_caps(m.group(1)) or heading(m.group(1))))
    prev = -1
    for i, x in recaps:
        last = max([j for j in out if j < i] or [-1])
        if x and (last < 0 or out[last] != x and not any(out[j] == x for j in out if prev < j < i)):
            k = next((j for j in range(prev + 1, i) if section(ls[j][3])), None)
            if k is not None:
                out[k - 1 if k - 1 > prev and k - 1 not in out else k] = x
        prev = i
    return out


def states(ls):
    out, st, sec = {}, None, None
    H = headings(ls)
    for i, (page, top, bot, t, fx) in enumerate(ls):
        u = t.strip()
        key = re.sub(r'[^A-Z]', '', re.split(r'[—–-]', u.lstrip(' -—–|.:;\'"‘'))[0])
        cont = key in CAPS and ('—' in u or 'Continued' in u)
        hs = CAPS[key] if cont else H.get(i)
        if hs:
            # a new State's heading ('NEW YORE', 'EKANSAS', 'Mee PENNSYLVANIA —__ re') starts afresh
            if hs != st and not cont:
                sec = None
            st = hs
            out.setdefault(st, {'senate': [], 'house': [], 'recap': []})
            continue
        if st is None:
            continue
        low = u.lower().lstrip(' -—–|.:;\'"‘')
        m = re.match(r'^[\W\w]{0,8}?\b(for\s+(?:u|p|r|d|g|s)\w.*)$', low) if not low.startswith('for') else None
        if m and not re.search(r'\d{2}', low[:m.start(1)]):
            low = m.group(1)    # margin noise before a heading on a skewed page ('ee For Unrrep Starks ...')
        # "For Presidential Electors" ("PresipentiaL ExvEectors", "Presipentiay EvLectors"); not "For Representatives"
        if low.startswith('for') and ('elector' in low or 'ectoral' in low or 'presid' in low or re.match(r'for\s+p\w{6,}\s+\w', low)):
            sec = 'pres'
            out[st].setdefault('pres', [])
            continue
        if low.startswith('for') and ('delegate' in low or 'governor' in low):
            sec = 'other'
            continue
        # "For United States Senator" ("Unirep" in the OCR), "For U.S. Senator" ("SEnNaTor", "Smnaror"), "For Representatives"
        if low.startswith('for') and re.search(r'sena|s\w{1,2}na\w*or|u\.\s?s[.,]', low):
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
        if sec == 'pres':
            # a slate: the party (or the elector's name) and its vote
            v = last_num(u)
            text = re.split(r'_{2,}|\.{3,}|-{3,}|[_.\-~]{4,}', u)[0].strip(' ,.;:|')
            if v is None or re.match(r'^\W*(Total|Majority|Plurality)', text):
                continue
            rec.update(votes=v, party=text, name=None)
            out[st]['pres'].append(rec)
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
            # a run of parties ('Democrat, Republican': California's cross-filing) kept whole, first first
            j = len(pm) - 1
            while j and re.fullmatch(r'[\s,]*', text[pm[j - 1].end():pm[j].start()]):
                j -= 1
            party_at = pm[j].start()
            party = ', '.join(fix_party(x.group(1)) for x in pm[j:])
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
