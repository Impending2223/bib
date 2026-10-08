"""Special elections during each Congress, 87th to 93rd: the seat, who left and why, every round's
candidates, the winner, and whether the seat changed hands.
# Usage: python3 tools/congress/make_specials.py [--cache DIR]
#   Writes congress/specials.yaml. Needs the network; the build does not.
#
#   Sources, all Wikipedia (the Clerk's biennial Statistics print only the November election, so a
#   special held between general elections is not in them; the official returns are the States'):
#     "List of special elections to the United States House of Representatives": Congress, seat,
#       the member who left and why, the winner, the date;
#     "<year> United States House of Representatives elections", 1961-74, "Special elections": the
#       candidates with their shares, in percent (no votes), and the date elected;
#     "List of special elections to the United States Senate", and the race's own page where it gives
#       votes in election boxes (Texas, 1961: both rounds, from Bartley and Graham, Southern Elections).
#   Specials held with the November general election are kept too (with_general: true): the rosters'
#   notes want their dates; their returns are the Clerk's, in elections/<year>.yaml.
#   Mechanical: names, parties, shares and dates as the sources give them. Check a figure against
#   the State's canvass where it matters.
"""
import datetime
import os
import re
import sys
import tempfile
import urllib.parse
import urllib.request

import yaml

# Read in a State's own returns (sources/states.yaml), over Wikipedia: (st, seat, Wikipedia's date) -> fields to set.
STATE = {
    ('CA', 13, '1974-06-04'): {
        'date': '1974-03-05',
        'note': 'Decided at the special primary: a candidate with a majority there was declared elected (Lagomarsino, '
                '52,140 votes, 53.64%). California Statement of Vote, 1973-74 volume, p. 54.'},
}

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bib'))

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'congress', 'specials.yaml')
WIKI = 'https://en.wikipedia.org/w/index.php?title={}&action=raw'
HOUSE_LIST = 'List of special elections to the United States House of Representatives'
SENATE_LIST = 'List of special elections to the United States Senate'
GENERAL = {'1960-11-08', '1962-11-06', '1964-11-03', '1966-11-08', '1968-11-05', '1970-11-03', '1972-11-07',
           '1974-11-05'}
STATES = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO',
          'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
          'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
          'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
          'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
          'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
          'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
          'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
          'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
          'Wisconsin': 'WI', 'Wyoming': 'WY'}
PARTY = {'Democratic': 'D', 'Republican': 'R'}


def fetch(title, cache):
    p = os.path.join(cache, 'sp_' + re.sub(r'\W+', '_', title) + '.txt')
    if not os.path.exists(p):
        req = urllib.request.Request(WIKI.format(urllib.parse.quote(title.replace(' ', '_'))),
                                     headers={'User-Agent': 'Mozilla/5.0 (bibliography)'})
        open(p, 'wb').write(urllib.request.urlopen(req, timeout=120).read())
    return open(p, encoding='utf-8').read()


def plain(t):
    """Wikitext to text: links to their labels, templates and markup out."""
    t = re.sub(r'<!--.*?-->|<ref.*?</ref>|<ref[^>]*/>', '', t, flags=re.S)
    t = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\{\{(?:Small|small|nowrap)\|([^{}]*)\}\}', r'\1', t)
    t = re.sub(r'\{\{[^{}]*\}\}', '', t)
    t = re.sub(r"'''?|<br\s*/?>", ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def iso(d):
    return datetime.datetime.strptime(d.replace('.', ''), '%B %d, %Y').date().isoformat()


def human(d):
    return datetime.date.fromisoformat(d).strftime('%B %-d, %Y')


def code(party):
    return PARTY.get(party.strip(), party.strip())


def seat_of(s):
    s = s.strip()
    return 0 if s.upper() in ('AL', 'AT-LARGE', 'AT LARGE', '0') else int(s)


def state_of(s):
    s = s.strip()
    return s if len(s) == 2 else STATES[s]


# ---------------------------------------------------------------- the House

def house_list(cache):
    """{(Congress, st, seat, date): row} from the list of House specials."""
    out = {}
    for blk in fetch(HOUSE_LIST, cache).split('\n|-'):
        m = re.search(r'USCongressOrdinal\|(\d+)', blk)
        if not m or not 87 <= int(m.group(1)) <= 93:
            continue
        u = re.search(r'\{\{[Uu]shr\|([^|}]+)\|([^|}]+)', blk)
        cells = [c.strip() for c in re.split(r'\n\|', blk)]
        people = re.findall(r'\|\s*\[\[(?:[^|\]]*\|)?([^\]]+)\]\]\s*\((\w+)\)', blk)
        d = re.findall(r'([A-Z][a-z]+ \d{1,2}, \d{4})\]\]', blk) or re.findall(r'nowrap \| ([A-Z][a-z]+ \d{1,2}, \d{4})', blk)
        why = next((plain(c) for c in cells if re.match(r'(Died|Resigned|Expelled|Excluded|Seat|Election|Vacant|Lost|Retired)', plain(c))), '')
        if not (u and people and d):
            continue
        row = {'cong': int(m.group(1)), 'ch': 'h', 'st': state_of(u.group(1)), 'seat': seat_of(u.group(2)),
               'date': iso(d[-1]), 'out': people[0][0], 'out_party': people[0][1],
               'winner': people[-1][0] if len(people) > 1 else None, 'party': people[-1][1] if len(people) > 1 else None,
               'why': why}
        out[(row['cong'], row['st'], row['seat'], row['date'])] = row
    return out


CAND = re.compile(r"^\*\s*(?:\{\{Party stripe\|[^}]*\}\})?\s*(\{\{[Aa]ye\}\})?\s*(.+?)\s*\(([^()]+)\)\s*([\d.]+)\s*%?", re.M)


def year_rows(year, cache):
    """The specials table of Wikipedia's page for a year's House elections: [(st, seat, dates, cands, text)]."""
    t = fetch(f'{year} United States House of Representatives elections', cache)
    if year % 2 == 0:
        m = re.search(r'\n==+ *Special elections *==+\n(.*?)(?=\n==[^=])', t, re.S)
        t = m.group(1) if m else ''
    out = []
    for blk in t.split('\n|-'):
        u = re.search(r'\{\{[Uu]shr\|([^|}]+)\|([^|}]+)', blk)
        if not u or not re.search(r'elected|was held', blk):
            continue
        cands = []
        for aye, name, party, pct in CAND.findall(blk):
            cands.append([plain(name), code(party), float(pct)] + (['won'] if aye else []))
        cell = next((c for c in re.split(r'\n\|', blk) if 'ncumbent' in c or 'New member' in c), '')
        text = plain(cell)
        first = plain(re.split(r'<br\s*/?>', cell)[0])   # 'Incumbent died ...', up to the first line break
        dates = [iso(d) for d in re.findall(r'(?:elected|held)\b[^.]{0,60}?([A-Z][a-z]+ \d{1,2}, \d{4})', text)]
        if not cands and re.search(r'Unopposed', blk):   # unopposed: the winner, no share
            w = re.search(r"\{\{[Aa]ye\}\}\s*(.+?)\s*\(([^()]+)\)", blk)
            if w:
                cands = [[plain(w.group(1)), code(w.group(2)), None, 'won', 'unopposed']]
        try:
            out.append((state_of(u.group(1)), seat_of(u.group(2)), dates, cands, text, first))
        except (KeyError, ValueError):
            continue
    return out


# ---------------------------------------------------------------- the Senate (Texas, 1961)

def boxes(t):
    """[(title, [[name, party, votes]])] from a page's election boxes, in page order."""
    out = []
    for chunk in re.split(r'\{\{Election box begin', t, flags=re.I)[1:]:
        chunk = re.split(r'\{\{Election box end', chunk, flags=re.I)[0]
        m = re.search(r'title\s*=\s*([^<|}\n]*)', chunk)
        title = plain(m.group(1)) if m else ''
        rows = []
        for c in re.findall(r'\{\{Election box (?:winning )?candidate.*?\n\s*\}\}', chunk, re.S | re.I):
            f = dict((k.strip(), v.strip()) for k, v in re.findall(r'\|\s*(\w+)\s*=\s*([^|\n]*)', c))
            if f.get('votes'):
                party = re.sub(r'\s*\((US|United States)\)|\s+Party', '', plain(f.get('party', '')))
                rows.append([re.sub(r'\s*\(incumbent\)', '', plain(f.get('candidate', ''))), code(party),
                             int(f['votes'].replace(',', ''))])
        if rows:
            out.append((title, rows))
    return out


def senate(cache):
    page = fetch('1961 United States Senate special election in Texas', cache)
    bx = boxes(page)
    first = [b for b in bx if 'primary' in b[0].lower()][0][1]
    minor = [b for b in bx if 'minor' in b[0].lower()]
    if minor:   # the first round's minor candidates: the source's one row, named with their number
        first = [[f'Others ({len(minor[0][1])} candidates)', '', r[2]] if r[0].lower().startswith('minor') else r
                 for r in first]
    runoff = [b for b in bx if 'primary' not in b[0].lower() and 'minor' not in b[0].lower()][0][1]
    rounds = [{'date': '1961-04-04', 'label': 'first round', 'cands': first},
              {'date': '1961-05-27', 'label': 'runoff', 'cands': runoff}]
    return [{'cong': 87, 'ch': 's', 'st': 'TX', 'seat': 2, 'date': '1961-05-27', 'out': 'William A. Blakley',
             'out_party': 'D', 'why': 'Appointed January 3, 1961, on Lyndon B. Johnson\'s resignation to become '
             'Vice President; lost the special election.', 'winner': 'John Tower', 'party': 'R',
             'rounds': rounds, 'votes': True,
             'source': 'Wikipedia, "1961 United States Senate special election in Texas" (Bartley and Graham, '
                       '*Southern Elections: County and Precinct Data, 1950–1972*, 1978)'}]


# Senate specials the Wikipedia pages above do not give with figures: the facts from congress/changes.yaml; the
# votes are CQ's (congress/specials-cq.yaml). Georgia's was held with the November election, but the Clerk's volume
# prints the regular race only (elections/readings/1972.yaml, not_in_volume): not_in_clerk shows it with the
# specials between elections.
SENATE_HAND = [
    {'cong': 92, 'ch': 's', 'st': 'VT', 'seat': 1, 'date': '1972-01-07', 'out': 'Robert Stafford', 'out_party': 'R',
     'why': "Appointed September 16, 1971, on Winston L. Prouty's death (September 10, 1971); won the special election.",
     'winner': 'Robert Stafford', 'party': 'R', 'source': 'Congressional Quarterly, Guide to U.S. Elections, 6th ed. (2010)'},
    {'cong': 92, 'ch': 's', 'st': 'GA', 'seat': 2, 'date': '1972-11-07', 'out': 'David H. Gambrell', 'out_party': 'D',
     'why': "Appointed February 1, 1971, on Richard B. Russell's death (January 21, 1971).",
     'winner': 'Sam Nunn', 'party': 'D', 'not_in_clerk': True,
     'source': 'Congressional Quarterly, Guide to U.S. Elections, 6th ed. (2010)'},
]


# ---------------------------------------------------------------- all

def main():
    cache = sys.argv[sys.argv.index('--cache') + 1] if '--cache' in sys.argv else tempfile.gettempdir()
    listed = house_list(cache)
    tables = {}
    for y in range(1961, 1975):
        for st, seat, dates, cands, text, first in year_rows(y, cache):
            for d in dates or ['']:
                tables[(st, seat, d)] = (dates, cands, text, y, first)
    out = {}
    for (cong, st, seat, date), r in sorted(listed.items(), key=lambda kv: (kv[0][0], kv[0][3], kv[0][1])):
        t = tables.get((st, seat, date))
        if t is None:  # the list and the year's table can disagree on the day: the same seat within 60 days
            near = sorted((abs((datetime.date.fromisoformat(k[2]) - datetime.date.fromisoformat(date)).days), k, v)
                          for k, v in tables.items() if k[0] == st and k[1] == seat and k[2])
            t = near[0][2] if near and near[0][0] <= 60 else None
        rec = {'key': f'{date}-h-{st}-{seat}', 'ch': 'h', 'st': st, 'seat': seat, 'date': date,
               'out': r['out'], 'out_party': r['out_party'], 'why': r['why'],
               'winner': r['winner'], 'party': r['party']}
        if t:
            dates, cands, text, y, first = t
            m = re.search(r'\b[Ii]ncumbent (?:member-elect )?(.+)$', first)
            if m:   # the year's table says why more fully than the list ("disappeared in a plane crash ...")
                why = re.sub(r'\s+([.,])', r'\1', m.group(1)).strip()
                why = why if why.endswith('.') else why + '.'
                rec['why'] = why[0].upper() + why[1:]
            if dates and dates[-1] != date:   # the year's table, which gives its own source, over the list
                rec['date'], rec['key'] = dates[-1], f'{dates[-1]}-h-{st}-{seat}'
                rec['check'] = f'Wikipedia\'s list of House specials gives {human(date)}; its {y} table, {human(dates[-1])}.'
            if len(dates) > 1:
                rec['rounds_dates'] = dates
            rec['cands'] = cands
            tot = sum(c[2] or 0 for c in cands)
            if cands and cands[0][2] is not None and abs(tot - 100) > 1:
                rec['check'] = (rec.get('check', '') + f' The shares in the source add to {tot:.1f}%.').strip()
            rec['source'] = f'Wikipedia, "{y} United States House of Representatives elections" (special elections)'
        else:
            rec['source'] = 'Wikipedia, "List of special elections to the United States House of Representatives"'
        if not rec['winner']:   # re-elected to his own seat (Powell, 1967): the list names one person
            w = next((c for c in rec.get('cands') or [] if 'won' in c[3:]), None)
            if w:
                rec['winner'], rec['party'] = w[0], w[1]
        fix = STATE.get((st, seat, rec['date']))
        if fix:
            rec.update(fix)
            rec['key'] = f"{rec['date']}-h-{st}-{seat}"
        rec['flip'] = bool(rec['party'] and rec['out_party'] and rec['party'] != rec['out_party'])
        if rec['date'] in GENERAL:
            rec['with_general'] = True
        out.setdefault(cong, []).append(rec)
    for rec in senate(cache) + [dict(r) for r in SENATE_HAND]:
        cong = rec.pop('cong')
        rec = {'key': f"{rec['date']}-s-{rec['st']}-{rec['seat']}", **rec, 'flip': rec['party'] != rec['out_party']}
        if rec['date'] in GENERAL:
            rec['with_general'] = True
        out.setdefault(cong, []).insert(0, rec)
    for cong in out:   # by date, the order the file promises
        out[cong].sort(key=lambda x: x['date'])
    head = ('# Generated by tools/congress/make_specials.py from Wikipedia (see the script). Edit the script, not this file.\n'
            '# Per Congress, by date: key, ch (h|s), st, seat, date (the deciding vote), out, out_party, why, winner, party,\n'
            '# cands [[name, party, percent(, won)]] or rounds [{date, label, cands [[name, party, votes]]}], flip,\n'
            '# with_general (held with the November election: its returns are the Clerk\'s, in elections/), source,\n'
            '# note (read in the State\'s own returns: STATE in the script), check.\n')
    open(OUT, 'w', encoding='utf-8').write(head + yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=200,
                                                              default_flow_style=None))
    for c in sorted(out):
        mid = [x for x in out[c] if not x.get('with_general')]
        print(c, len(out[c]), 'specials;', len(mid), 'between general elections;',
              sum(1 for x in mid if not x.get('cands') and not x.get('rounds')), 'without candidates')


if __name__ == '__main__':
    main()
