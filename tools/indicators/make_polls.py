"""Opinion polls for the calendar's monthly tables: Gallup's presidential approval, Gallup's preference among
Republicans for the 1964 nomination, and the trial heats for 1964.
# Usage: python3 tools/indicators/make_polls.py
#   Rewrites indicators/approval.yaml, indicators/gop-preference.yaml and indicators/trial-heats.yaml for the
#   calendar's span (FROM..TO). Needs the network; the build does not.
#
#   Approval: the American Presidency Project's tables of each President's job approval, "adapted from the Gallup
#   Poll and compiled by Gerhard Peters": field dates, approve, disapprove, no opinion, and approval among
#   Democrats, independents and Republicans. Filed by the month the fieldwork ended.
#   Republican preference: Wikipedia's table (1964 Republican Party presidential primaries, "National polling"),
#   Gallup's figures as OurCampaigns gives them (its pages are bot-checked here), by month of publication;
#   each row "check": to be read against The Gallup Poll: Public Opinion, 1935-1971, III (1972).
#   Trial heats: Wikipedia's table (1964 United States presidential election, "Polling"), with the page of the
#   Gallup volume it cites, or the newspaper that printed a Harris poll; "check" likewise.
"""
import html, os, re, urllib.request
import yaml

FROM, TO = '1961-01-20', '1964-01-07'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'indicators')
UA = {'User-Agent': 'bib-calendar/1.0 (research; github.com/impending2223/bib)'}
APP = 'https://www.presidency.ucsb.edu/statistics/data/'
WIKI = 'https://en.wikipedia.org/w/index.php?title={}&action=raw'
MON = {m: i for i, m in enumerate(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 1)}
MONTHS = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
          'September': 9, 'October': 10, 'November': 11, 'December': 12}
CHECK = 'The Gallup Poll: Public Opinion, 1935–1971, III (1972)'


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
        return r.read().decode('utf-8', 'replace')


def iso(d):
    m, dd, y = d.split('/')
    return f'{int(y):04d}-{int(m):02d}-{int(dd):02d}'


def approval():
    rows = []
    for slug, who in (('john-f-kennedy-public-approval', 'Kennedy'), ('lyndon-b-johnson-public-approval', 'Johnson')):
        t = get(APP + slug)
        for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
            c = [html.unescape(re.sub(r'<[^>]+>', '', x)).strip() for x in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', tr, re.S)]
            if len(c) < 9 or not re.match(r'\d{1,2}/\d{1,2}/\d{4}$', c[0]):
                continue
            a, b = iso(c[0]), iso(c[1])
            if not (FROM <= b <= TO):
                continue
            n = lambda x: int(x) if x.isdigit() else None
            rows.append({'p': b[:7], 'from': a, 'to': b, 'president': who, 'approve': n(c[2]), 'disapprove': n(c[3]),
                         'unsure': n(c[4]), 'dem': n(c[6]), 'ind': n(c[7]), 'rep': n(c[8])})
    rows.sort(key=lambda r: r['to'])
    return {'id': 'approval', 'name': 'Approval', 'kind': 'poll', 'freq': 'poll',
            'then': {'label': 'Gallup: "Do you approve or disapprove of the way [the President] is handling his job as President?"',
                     'source': 'American Presidency Project, Presidential Job Approval (Gallup, compiled by Gerhard Peters)',
                     'url': APP + 'presidential-job-approval'},
            'rows': rows}


def wiki_rows(table):
    out = []
    for row in table.split('\n|-')[1:]:
        cells = [c.strip() for c in re.split(r'\n[|!]|\|\|', '\n' + row.strip())[1:]]
        out.append(cells)
    return out


def clean(c):
    c = re.sub(r'<ref[^>]*/>|<ref.*?</ref>|\{\{efn[^}]*\}\}', '', c, flags=re.S)
    c = re.sub(r'\{\{party shading/[^}]*\}\}|align="center"|rowspan=\d+', '', c)
    return re.sub(r"'''|\s*\|\s*", ' ', c).strip()


def pct(c):
    m = re.search(r'(\d+(?:\.\d+)?)%?', clean(c))
    return float(m.group(1)) if m and '–' not in clean(c)[:1] else None


def preference():
    t = get(WIKI.format('1964_Republican_Party_presidential_primaries'))
    sec = t[t.index('=== National polling ==='):]
    sec = sec[:sec.index('|}')]
    names = re.findall(r'vert header\|stp=1\|([^}]+)\}\}', sec)
    rows = []
    for cells in wiki_rows(sec):
        cells = [x for x in cells if x]
        if len(cells) < 2 + len(names) or not cells[0].startswith('Gallup'):
            continue
        m = re.match(r'([A-Z][a-z]+)\.? (\d{4})', clean(cells[1]))
        if not m:
            continue
        p = f'{int(m.group(2)):04d}-{MON[m.group(1)[:4] if m.group(1).startswith("June") or m.group(1).startswith("July") else m.group(1)[:3]]:02d}'
        if not (FROM[:7] <= p <= TO[:7]):
            continue
        shares = {}
        for name, c in zip(names, cells[2:2 + len(names)]):
            v = pct(c)
            if v is not None:
                shares[re.sub(r' (Jr\.|II)$', '', name).split()[-1]] = int(v) if v == int(v) else v
        rows.append({'p': p, 'published': clean(cells[1]), 'shares': shares})
    return {'id': 'gop-preference', 'name': 'Republican preference', 'kind': 'poll', 'freq': 'poll',
            'then': {'label': 'Gallup: the choice of Republicans for the 1964 Republican nomination, by month of publication',
                     'source': 'Gallup, as OurCampaigns gives it, by Wikipedia, 1964 Republican Party presidential primaries, "National polling"',
                     'url': 'https://en.wikipedia.org/wiki/1964_Republican_Party_presidential_primaries#National_polling',
                     'check': CHECK},
            'rows': rows}


def trial_heats():
    t = get(WIKI.format('1964_United_States_presidential_election'))
    sec = t[t.index('===Polling==='):]
    sec = sec[:sec.index('\n|}')]
    rows = []
    for cells in wiki_rows(sec):
        if len(cells) < 6 or 'Election Results' in cells[0]:
            continue
        src = cells[0]
        who = clean(re.sub(r'<ref.*', '', src)).strip()
        page = re.search(r'cite book[^}]*\|page=(\d+)', src)
        paper = re.search(r'\|date=([^|]+?) \|title=([^|]+?) \|page=(\d+) \|work=([^|]+?) \|', src)
        when = clean(cells[1])
        m = re.match(r'([A-Z][a-z]+) (\d{1,2})(?:–(\d{1,2}))?, (\d{4})', when)
        if not m:
            continue
        y, mo = int(m.group(4)), MONTHS[m.group(1)]
        a = f'{y:04d}-{mo:02d}-{int(m.group(2)):02d}'
        b = f'{y:04d}-{mo:02d}-{int(m.group(3) or m.group(2)):02d}'
        if not (FROM <= b <= TO):
            continue
        row = {'p': b[:7], 'pollster': who, 'pair': [['Johnson', pct(cells[2])], ['Goldwater', pct(cells[3])]],
               'undecided': pct(cells[5])}
        if 'publication date is used' in src + cells[1] or who == 'Harris':
            row['published'] = b
        else:
            row.update({'from': a, 'to': b})
        if page:
            row['cite'] = f'{CHECK.replace(" (1972)", "")}, {page.group(1)}'
        elif paper:
            row['cite'] = f'*{paper.group(4).strip()}*, {paper.group(1).strip()}, {paper.group(3)}'
        rows.append(row)
    rows.sort(key=lambda r: r.get('to') or r.get('published'))
    for r in rows:
        for k, v in list(r.items()):
            if isinstance(v, float) and v == int(v):
                r[k] = int(v)
        r['pair'] = [[n, int(v) if v == int(v) else v] for n, v in r['pair']]
    return {'id': 'trial-heats', 'name': 'Trial heat', 'kind': 'poll', 'freq': 'poll',
            'then': {'label': 'The 1964 race, two names put to the national sample',
                     'source': 'Wikipedia, 1964 United States presidential election, "Polling": Gallup by the page of its volume, Harris by the newspaper that printed it',
                     'url': 'https://en.wikipedia.org/wiki/1964_United_States_presidential_election#Polling',
                     'check': CHECK},
            'rows': rows}


def write(d):
    head = ('# Generated by tools/indicators/make_polls.py. Edit the script, not this file.\n')
    path = os.path.join(OUT, d['id'] + '.yaml')
    open(path, 'w', encoding='utf-8').write(head + yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=200,
                                                                default_flow_style=None))
    print('wrote', path, len(d['rows']))


if __name__ == '__main__':
    for f in (approval, preference, trial_heats):
        write(f())
