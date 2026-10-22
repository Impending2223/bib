"""Money, the foreign accounts and the debt's terms for the calendar's indicator tables, as first printed then and as
given today.
# Usage: python3 -I tools/indicators/make_finance.py [--only ID,ID] [--ddp DIR]
#   Rewrites indicators/<id>.yaml for the series in SERIES below (tools/bib/finance.py renders them; its STYLE).
#   Needs the network for today's figures: FRED's public CSV downloads (never an API key) and the Board of Governors'
#   Data Download Program (H.6, H.3: --ddp DIR holds the two zips already fetched). The figures printed then are read
#   by eye off the page images, transcribed below (READ), each with its table and page: edit them here, never the
#   YAML, and rerun. A series whose figures today cannot be fetched keeps none ('now' left out); rerunning when the
#   source answers fills them.
#
# Sources then (each block below names its pages):
#   ERP   Economic Report of the President, read off FRASER's scans of each January's Report (ERP_<year>.pdf, the printed
#         page plus 6 in 1965-69): the FHA new-home mortgage yields (Table B-54, "Bond yields and interest rates"),
#         printed from the Report of Feb. 1968 on.
# Sources today:
#   FRED  AAA, BAA (Moody's, monthly averages; not revised); the Board's H.6 (M1, M2) and H.3 (total and required
#         reserves, borrowings) from its Data Download Program, the figures FRED carries as M1SL, M2SL and NFORBRES.
"""
import csv, io, json, os, re, sys, time, urllib.request, zipfile
import yaml

ONLY = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
DDP_DIR = sys.argv[sys.argv.index('--ddp') + 1] if '--ddp' in sys.argv else None
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'indicators')
FRED = 'https://fred.stlouisfed.org/series/'
FRED_CSV = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id='
DDP = 'https://www.federalreserve.gov/datadownload/Output.aspx?rel={}&filetype=zip'
MONTHS = [f'{y}-{m:02d}' for y in range(1960, 1969) for m in range(1, 13)]       # the money-rate tables' span
MSPAN = MONTHS[11:]                     # Dec. 1960-Dec. 1968, as the monthly indicators (make_indicators.py)
MON = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']


# ---------------------------------------------------------------- the printings read (SRC: date, cite, link)
# A source key names one printing: its date (the day transmitted, or the issue's month) and its cite. The Reports'
# dates and links are those of tools/indicators/make_indicators.py (ERP there).
SRC = {
    'ERP62': ('1962-01-22', 'Economic Report of the President, Jan. 1962',
              'https://www.govinfo.gov/app/details/SERIALSET-12497_00_00-002-0278-0000'),
    'ERP63': ('1963-01-21', 'Economic Report of the President, Jan. 1963',
              'https://www.govinfo.gov/app/details/SERIALSET-12600_00_00-002-0028-0000'),
    'ERP68': ('1968-02-01', 'Economic Report of the President, Feb. 1968',
              'https://www.govinfo.gov/app/details/SERIALSET-12825_00_00-002-0238-0000'),
    'ERP69': ('1969-01-16', 'Economic Report of the President, Jan. 1969',
              'https://www.govinfo.gov/app/details/SERIALSET-12868_00_00-002-0028-0000'),
}

# ---------------------------------------------------------------- READ: the figures printed then
# Each block: lines "SRC/where PERIOD VALUE[/VALUE...] [prior=VALUE] [note=TEXT]". SRC is a key of SRC above, 'where'
# the table and page. A period printed in several sources is taken from the first listed. prior: the period before as
# printed in the same place (the change 'in that release'); without it, the change is taken from the period before
# where the same place prints it.

# FHA new-home mortgage yields, secondary market, first of the month (Table B-54's column "FHA new home mortgage
# yields", its note 5: "Data for first of the month, based on the maximum permissible interest rate (6 percent
# beginning October 1966) and, thru July 1961, 25-year mortgages paid in 12 years and, thereafter, 30-year mortgages
# paid in 15 years"; the Jan. 1969 Report's note: "6¾ percent beginning early May 1968"). Blank months (no figure
# printed): Mar., May and Nov. 1966, June 1968. Read off the page images at 220 dpi. The Report of Jan. 1967 prints no
# such column (Table B-50, pp. 272-73). 1967 as the Feb. 1968 Report printed it; the Jan. 1969 Report's 1967 agrees.
FHA = """
ERP68/Table B-54, p. 273 1966-01 5.62
ERP68/Table B-54, p. 273 1966-02 5.70
ERP68/Table B-54, p. 273 1966-04 6.00
ERP68/Table B-54, p. 273 1966-06 6.32
ERP68/Table B-54, p. 273 1966-07 6.45
ERP68/Table B-54, p. 273 1966-08 6.51
ERP68/Table B-54, p. 273 1966-09 6.58
ERP68/Table B-54, p. 273 1966-10 6.63
ERP68/Table B-54, p. 273 1966-12 6.81
ERP68/Table B-54, p. 273 1967-01 6.77
ERP68/Table B-54, p. 273 1967-02 6.62
ERP68/Table B-54, p. 273 1967-03 6.46
ERP68/Table B-54, p. 273 1967-04 6.35
ERP68/Table B-54, p. 273 1967-05 6.29
ERP68/Table B-54, p. 273 1967-06 6.44
ERP68/Table B-54, p. 273 1967-07 6.51
ERP68/Table B-54, p. 273 1967-08 6.53
ERP68/Table B-54, p. 273 1967-09 6.60
ERP68/Table B-54, p. 273 1967-10 6.63
ERP68/Table B-54, p. 273 1967-11 6.65
ERP68/Table B-54, p. 273 1967-12 6.77
ERP69/Table B-54, p. 291 1968-01 6.81
ERP69/Table B-54, p. 291 1968-02 6.81
ERP69/Table B-54, p. 291 1968-03 6.78
ERP69/Table B-54, p. 291 1968-04 6.83
ERP69/Table B-54, p. 291 1968-05 6.94
ERP69/Table B-54, p. 291 1968-07 7.52
ERP69/Table B-54, p. 291 1968-08 7.42
ERP69/Table B-54, p. 291 1968-09 7.35
ERP69/Table B-54, p. 291 1968-10 7.28
ERP69/Table B-54, p. 291 1968-11 7.29
ERP69/Table B-54, p. 291 1968-12 7.36
"""

# The money stock, M1 (currency outside banks and demand deposits adjusted), averages of daily figures, seasonally
# adjusted, billions. Dec. 1960 and 1961: the Jan. 1962 Report, Table B-44, p. 260 (the series before the Board's
# revision of Aug. 1962; Dec. 1961 preliminary). Jan.-Aug. 1962: the Jan. 1963 Report, Table C-45, p. 226 (the revised
# series, the Bulletin of Aug. 1962; its Dec. 1961, 145.7, for January's change). Each month's currency and demand
# deposits read with it and found to add to it within 0.1. From Sept. 1962, the Survey of Current Business (below).
M1 = """
ERP62/Table B-44, p. 260 1960-12 140.4
ERP62/Table B-44, p. 260 1961-01 140.6
ERP62/Table B-44, p. 260 1961-02 141.2
ERP62/Table B-44, p. 260 1961-03 141.5
ERP62/Table B-44, p. 260 1961-04 142.0
ERP62/Table B-44, p. 260 1961-05 142.0
ERP62/Table B-44, p. 260 1961-06 142.1
ERP62/Table B-44, p. 260 1961-07 142.0
ERP62/Table B-44, p. 260 1961-08 141.8
ERP62/Table B-44, p. 260 1961-09 143.0
ERP62/Table B-44, p. 260 1961-10 143.7
ERP62/Table B-44, p. 260 1961-11 144.1
ERP62/Table B-44, p. 260 1961-12 144.9
ERP63/Table C-45, p. 226 1962-01 145.9 prior=145.7
ERP63/Table C-45, p. 226 1962-02 145.5
ERP63/Table C-45, p. 226 1962-03 145.7
ERP63/Table C-45, p. 226 1962-04 146.1
ERP63/Table C-45, p. 226 1962-05 145.7
ERP63/Table C-45, p. 226 1962-06 145.6
ERP63/Table C-45, p. 226 1962-07 145.7
ERP63/Table C-45, p. 226 1962-08 145.1
"""

# M1 plus time deposits adjusted at commercial banks ("Total money supply and time deposits adjusted"), averages of
# daily figures, seasonally adjusted, billions. Dec. 1960-Aug. 1962: the Jan. 1963 Report, Table C-45, p. 226 (the Jan.
# 1962 Report prints time deposits unadjusted only); M1 and time deposits found to add to it within 0.1. From Sept.
# 1962, the Survey (below).
M1T = """
ERP63/Table C-45, p. 226 1960-12 213.9
ERP63/Table C-45, p. 226 1961-01 215.1
ERP63/Table C-45, p. 226 1961-02 216.7
ERP63/Table C-45, p. 226 1961-03 217.8
ERP63/Table C-45, p. 226 1961-04 218.7
ERP63/Table C-45, p. 226 1961-05 220.2
ERP63/Table C-45, p. 226 1961-06 221.0
ERP63/Table C-45, p. 226 1961-07 222.1
ERP63/Table C-45, p. 226 1961-08 222.7
ERP63/Table C-45, p. 226 1961-09 224.0
ERP63/Table C-45, p. 226 1961-10 225.5
ERP63/Table C-45, p. 226 1961-11 227.0
ERP63/Table C-45, p. 226 1961-12 228.2
ERP63/Table C-45, p. 226 1962-01 230.0
ERP63/Table C-45, p. 226 1962-02 231.3
ERP63/Table C-45, p. 226 1962-03 233.1
ERP63/Table C-45, p. 226 1962-04 234.7
ERP63/Table C-45, p. 226 1962-05 235.2
ERP63/Table C-45, p. 226 1962-06 236.2
ERP63/Table C-45, p. 226 1962-07 237.4
ERP63/Table C-45, p. 226 1962-08 237.6
"""


def parse(block, fields=None):
    """{period: {'v': value or {field: value}, 'src': key, 'where': text, 'prior': value, 'note': text}}"""
    out = {}
    for line in block.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        note = None
        if ' note=' in line:
            line, note = line.split(' note=', 1)
        m = re.match(r'^(\w+)/(.*?) (\d{4}(?:-\d{2}|Q\d)?) (\S+)(?: prior=(\S+))?$', line)
        if not m:
            raise SystemExit('bad line: ' + line)
        key, where, p, v, prior = m.groups()
        def val(x):
            if x in ('-', '—', 'na'):
                return None
            parts = x.split('/')
            nums = [None if y in ('-', '—', 'na') else (float(y) if '.' in y else int(y)) for y in parts]
            return dict(zip(fields, nums)) if fields else nums[0]
        if p in out:
            continue
        out[p] = {'v': val(v), 'src': key, 'where': where, 'prior': val(prior) if prior else None, 'note': note}
    return out


def prev(p):
    if 'Q' in p:
        y, q = int(p[:4]), int(p[-1])
        return f'{y - 1}Q4' if q == 1 else f'{y}Q{q - 1}'
    y, m = int(p[:4]), int(p[5:7])
    return f'{y - 1}-12' if m == 1 else f'{y}-{m - 1:02d}'


def first_rows(read, unit, change=None, total=None):
    """Rows' first-reported fields from a parsed block: first, released, source, unit, chg (in that release)."""
    rows = {}
    for p, x in sorted(read.items()):
        date, cite, url = SRC[x['src']]
        row = {'first': x['v'], 'released': date, 'source': f'{cite}, {x["where"]}' + (f'; {url}' if url else ''),
               'unit': unit}
        before = x['prior']
        if before is None and prev(p) in read and read[prev(p)]['src'] == x['src'] \
                and read[prev(p)]['where'] == x['where']:
            before = read[prev(p)]['v']
        if change and before is not None and x['v'] is not None:
            a, b = (x['v'][total], before[total]) if total else (x['v'], before)
            if a is not None and b is not None:
                row['chg'] = round(a - b, 2) if change == 'pts' else (round(100 * (a / b - 1), 1) if change == 'pct'
                                                                       else round(a - b, 3))
        if x['note']:
            row['note'] = x['note']
        rows[p] = row
    return rows


# ---------------------------------------------------------------- today's figures

def fred(sid):
    """{YYYY-MM-DD: value} from FRED's public CSV, or None where FRED does not answer with a CSV."""
    for i in range(3):
        try:
            with urllib.request.urlopen(FRED_CSV + sid, timeout=60) as r:
                text = r.read().decode()
            if not text.startswith('observation_date') and not text.startswith('DATE'):
                return None                       # a maintenance page, not the series
            rows = list(csv.reader(io.StringIO(text)))
            return {d: float(v) for d, v in rows[1:] if v not in ('', '.')}
        except Exception:
            time.sleep(3 * (i + 1))
    return None


def ddp(rel):
    """{series name: {YYYY-MM: value}} from the Board's Data Download Program package for a release (H6, H3)."""
    raw = None
    if DDP_DIR and os.path.exists(os.path.join(DDP_DIR, f'{rel}.zip')):
        raw = open(os.path.join(DDP_DIR, f'{rel}.zip'), 'rb').read()
    else:
        req = urllib.request.Request(DDP.format(rel), headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
    z = zipfile.ZipFile(io.BytesIO(raw))
    xml = z.read(f'{rel}_data.xml').decode()
    out = {}
    for m in re.finditer(r'<kf:Series ([^>]*)>(.*?)</kf:Series>', xml, re.S):
        name = re.search(r'SERIES_NAME="([^"]*)"', m.group(1)).group(1)
        obs = {}
        for o in re.finditer(r'<frb:Obs ([^>]*)/>', m.group(2)):
            a = dict(re.findall(r'(\w+)="([^"]*)"', o.group(1)))
            if a.get('OBS_VALUE') not in (None, 'NaN', ''):
                obs[a['TIME_PERIOD'][:7]] = float(a['OBS_VALUE'])
        out.setdefault(name, obs)
    return out


def write(sid, meta, rows):
    path = os.path.join(OUT, f'{sid}.yaml')
    head = ('# Generated by tools/indicators/make_finance.py. Edit the script, not this file.\n'
            '# p: reporting period; first: as first printed (released: the printing, source: table and page);\n'
            '# chg: change from the period before in that printing; now, chg_now: as given today.\n')
    body = yaml.safe_dump(dict(meta, rows=rows), sort_keys=False, allow_unicode=True, width=200,
                          default_flow_style=None)
    open(path, 'w', encoding='utf-8').write(head + body)
    print('wrote', path, len(rows))


def want(sid):
    return ONLY is None or sid in ONLY


# ---------------------------------------------------------------- the series

def rates():
    """Moody's (FRED, one figure) and the mortgage rates (as first printed, one figure): kind rate."""
    for sid, fid, name, label in (
            ('corporate-aaa', 'AAA', "Corporate bond yield, Moody's Aaa",
             "Moody's Investors Service: seasoned corporate bonds rated Aaa, monthly average of daily yields"),
            ('corporate-baa', 'BAA', "Corporate bond yield, Moody's Baa",
             "Moody's Investors Service: seasoned corporate bonds rated Baa, monthly average of daily yields")):
        if not want(sid):
            continue
        cur = fred(fid)
        if cur is None:
            print('FRED did not answer for', fid, '; not written')
            continue
        rows = []
        for p in MONTHS:
            v, b = cur.get(f'{p}-01'), cur.get(f'{prev(p)}-01')
            row = {'p': p, 'now': v}
            if v is not None and b is not None:
                row['chg_now'] = round(v - b, 2)
            rows.append(row)
        write(sid, {'id': sid, 'name': name, 'freq': 'M', 'kind': 'rate', 'change': 'pts', 'then': None,
                    'now': {'label': label, 'unit': 'percent', 'source': f'FRED {fid}', 'url': FRED + fid}}, rows)
    if want('mortgage-fha'):
        fr = first_rows(parse(FHA), 'percent', 'pts')
        rows = [dict(p=p, **fr[p]) for p in MONTHS if p in fr]
        write('mortgage-fha', {'id': 'mortgage-fha', 'name': 'FHA new-home mortgage yield', 'freq': 'M', 'manual': True,
                               'kind': 'rate', 'change': 'pts',
                               'then': {'label': 'Federal Housing Administration: secondary market yields on FHA-insured new-home mortgages, first of the month',
                                        'unit': 'percent'},
                               'now': None}, rows)


def monthly(sid, meta, first, now=None, change='pct', nd=1, span=None):
    """Write a monthly series: first (rows' first-reported fields by period), now ({YYYY-MM: value} today)."""
    rows = []
    for p in span or MSPAN:
        row = {'p': p}
        if p in first:
            row.update(first[p])
        if now is not None:
            v, b = now.get(p), now.get(prev(p))
            if v is not None:
                row['now'] = round(v, nd)
                if b is not None:
                    row['chg_now'] = round(100 * (v / b - 1), 1) if change == 'pct' else round(v - b, nd)
        if len(row) > 1:
            rows.append(row)
    write(sid, meta, rows)


def money():
    """The money stock and free reserves: as first printed (READ) and today, M1 and M2 (H.6), free reserves (H.3:
    total less required reserves, less borrowings)."""
    h6 = h3 = None
    try:
        h6 = ddp('H6')
        h3 = ddp('H3')
    except Exception as e:
        print('the Board did not answer:', e)
    if want('money-m1'):
        monthly('money-m1', {'id': 'money-m1', 'name': 'Money stock, M1', 'freq': 'M', 'manual': True, 'change': 'pct',
                             'then': {'label': 'Board of Governors: currency outside banks and demand deposits adjusted, averages of daily figures, seasonally adjusted', 'unit': 'billions of dollars'},
                             'now': {'label': 'Board of Governors, H.6: M1, seasonally adjusted, monthly average', 'unit': 'billions of dollars',
                                     'source': 'Board of Governors, H.6 (Data Download Program, M1.M; FRED M1SL)', 'url': FRED + 'M1SL'}},
                first_rows(parse(M1), 'billions of dollars', 'pct'), h6 and h6['M1.M'])
    if want('money-m1-time'):
        monthly('money-m1-time', {'id': 'money-m1-time', 'name': 'Money stock and time deposits', 'freq': 'M', 'manual': True, 'change': 'pct',
                                  'then': {'label': 'Board of Governors: the money supply and time deposits adjusted at commercial banks, averages of daily figures, seasonally adjusted', 'unit': 'billions of dollars'},
                                  'now': None},
                first_rows(parse(M1T), 'billions of dollars', 'pct'))
    if h6 and want('money-m2'):
        m2 = h6['M2.M']
        rows = []
        for p in MONTHS:
            v, b = m2.get(p), m2.get(prev(p))
            row = {'p': p, 'now': v}
            if v is not None and b is not None:
                row['chg_now'] = round(100 * (v / b - 1), 1)
            rows.append(row)
        write('money-m2', {'id': 'money-m2', 'name': 'Money stock, M2 (today)', 'freq': 'M', 'change': 'pct', 'then': None,
                           'now': {'label': 'Board of Governors, H.6: M2, seasonally adjusted, monthly average', 'unit': 'billions of dollars',
                                   'source': 'Board of Governors, H.6 (Data Download Program, M2.M; FRED M2SL)', 'url': FRED + 'M2SL'}}, rows)


if __name__ == '__main__':
    rates()
    money()
