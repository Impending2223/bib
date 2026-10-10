"""Monthly and quarterly indicators for the calendar, as first reported and as revised today.
# Usage: FRED_API_KEY=... python3 tools/indicators/make_indicators.py [FROM TO]
#   FROM, TO are reporting periods, default 1960-12-01 1964-12-31.
#   Rewrites indicators/<id>.yaml for the series in API below. Series entered by hand from the
#   Economic Reports and budget documents (manual: true in their files) are left alone.
#   'first' is the initial release in ALFRED, with the date it was released; 'chg' is the change
#   from the prior period in that same release; 'now' and 'chg_now' are the current FRED value and
#   its change, on the same basis (CHANGE below). 'yoy' and 'yoy_now': percent change from the
#   same month a year earlier, in that release and today (YOY below).
#   The key is read from the environment and never written out. Without a key, the same figures come
#   from ALFRED's and FRED's public CSV downloads (KEYLESS below): every day's vintage, so the first
#   release is the first day an observation appears.
#   Money and credit (RATES, DISCOUNT below): interest rates, which are not revised. FRED's monthly averages
#   go in 'now' with their change in points; the New York Reserve Bank's discount rate, kept by hand from
#   the Board's announcements, goes in 'first'. --only rates writes these alone (no ALFRED calls).
"""
import json, os, sys, time, urllib.parse, urllib.request
import yaml

KEY = os.environ.get('FRED_API_KEY')     # without it, the public CSV downloads (KEYLESS below)
ONLY = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
ARGS = [a for i, a in enumerate(sys.argv[1:], 1) if a != '--only' and sys.argv[i - 1] != '--only']
FROM, TO = (ARGS[0], ARGS[1]) if len(ARGS) > 1 else ('1960-12-01', '1964-12-31')
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'indicators')
FRED = 'https://fred.stlouisfed.org/series/'
ALFRED = 'https://alfred.stlouisfed.org/series?seid='

# id: (series, freq, name, unit then, unit now, change kind, label then, label now)
API = {
    'cpi': ('CPIAUCNS', 'M', 'Consumer price index', None, '1982–84=100', 'pct',
            'BLS, Consumer Price Index for city wage-earner and clerical-worker families, all items, not seasonally adjusted',
            'BLS, CPI for all urban consumers (CPI-U), all items, not seasonally adjusted'),
    'unemployment': ('UNRATE', 'M', 'Unemployment rate', 'percent of civilian labor force', 'percent', 'pts',
            'BLS, from the Census Current Population Survey, seasonally adjusted',
            'BLS, Current Population Survey, seasonally adjusted, ages 16 and over'),
    'payrolls': ('PAYEMS', 'M', 'Nonfarm payroll employment', 'thousands', 'thousands', 'diff',
            'BLS, establishment survey, wage and salary workers in nonagricultural establishments, seasonally adjusted',
            'BLS, Current Employment Statistics, all employees, total nonfarm, seasonally adjusted'),
    'industrial-production': ('INDPRO', 'M', 'Industrial production', None, '2017=100', 'pct',
            'Federal Reserve Board, index of industrial production, seasonally adjusted',
            'Federal Reserve Board, industrial production index, seasonally adjusted'),
    'gnp': ('GNP', 'Q', 'Gross national product', 'billions of dollars, seasonally adjusted annual rate', 'billions of dollars, SAAR', 'pct_ar',
            'Commerce, Office of Business Economics, national income accounts',
            'BEA, national income and product accounts'),
    'real-gnp': ('GNPC96', 'Q', 'Real gross national product', None, 'billions of chained 2017 dollars, SAAR', 'pct_ar',
            'Commerce, Office of Business Economics, GNP in constant dollars',
            'BEA, real GNP, chained dollars'),
}
DEFLATOR = ('GNPDEF', 'Implicit price deflator for GNP', '2017=100',
            'Commerce, Office of Business Economics; GNP in current dollars over GNP in constant dollars, same release',
            'BEA, GNP implicit price deflator')
# The base in use when each series was first published, by first-release date (checked against the values).
BASE = {'CPIAUCNS': [('1900-01-01', '1947–49=100'), ('1962-02-01', '1957–59=100')],
        'INDPRO': [('1900-01-01', '1957=100')],
        'GNPC96': [('1900-01-01', 'billions of 1954 dollars, SAAR')],
        'GNPDEF': [('1900-01-01', '1954=100')]}


def get(path, **q):
    if not KEY:
        if path == 'series/observations' and set(q) <= {'series_id', 'observation_start', 'observation_end'}:
            return {'observations': [{'date': d, 'value': '.' if v is None else str(v)}
                                     for d, v in current_from(q['series_id'], q.get('observation_start', '1959-01-01')).items()]}
        raise SystemExit('this call needs FRED_API_KEY: ' + path)
    q.update(api_key=KEY, file_type='json')
    url = 'https://api.stlouisfed.org/fred/' + path + '?' + urllib.parse.urlencode(q)
    for i in range(5):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception:
            time.sleep(2 * (i + 1))
    raise SystemExit('FRED API failed: ' + path)


def num(v):
    return None if v in ('.', '', None) else float(v)


# ---------------------------------------------------------------- KEYLESS: the public CSV downloads

ALFRED_CSV = 'https://alfred.stlouisfed.org/graph/alfredgraph.csv?'
FRED_CSV = 'https://fred.stlouisfed.org/graph/fredgraph.csv?'
_VIN = {}


def csv_get(url):
    for i in range(5):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                rows = r.read().decode().strip().split('\n')
            head = rows[0].split(',')
            return head, [x.split(',') for x in rows[1:]]
        except Exception:
            time.sleep(2 * (i + 1))
    raise SystemExit('CSV download failed: ' + url)


def days(a, b):
    import datetime
    d, e = datetime.date.fromisoformat(a), datetime.date.fromisoformat(b)
    while d <= e:
        yield d.isoformat()
        d += datetime.timedelta(days=1)


def vintages(sid, first, last):
    """Every day's vintage from first to last: {day: {observation date: value}}, twelve days a request (ALFRED
    returns no more than twelve series at once), each column read by its header (SID_YYYYMMDD)."""
    want = [d for d in days(first, last) if (sid, d) not in _VIN]
    for i in range(0, len(want), 12):
        chunk = want[i:i + 12]
        q = {'id': ','.join([sid] * len(chunk)), 'vintage_date': ','.join(chunk),
             'cosd': ','.join(['1959-01-01'] * len(chunk)), 'coed': ','.join([TO] * len(chunk))}
        head, rows = csv_get(ALFRED_CSV + urllib.parse.urlencode(q, safe=','))
        col = {h.rsplit('_', 1)[-1]: j for j, h in enumerate(head) if j}
        for d in chunk:
            j = col.get(d.replace('-', ''))
            if j is None:
                raise SystemExit(f'ALFRED returned no column for {sid} {d}')
            _VIN[(sid, d)] = {r[0]: num(r[j]) for r in rows if len(r) > j and num(r[j]) is not None}
    return {d: _VIN[(sid, d)] for d in days(first, last)}


def latest_vintage(sid):
    """The day the series last changed: back from today, the first day whose vintage differs from today's."""
    import datetime
    today = datetime.date.today()
    now = vintages(sid, today.isoformat(), today.isoformat())[today.isoformat()]
    end = today
    while end.year > today.year - 3:
        start = end - datetime.timedelta(days=39)
        vs = vintages(sid, start.isoformat(), end.isoformat())
        for d in sorted(vs, reverse=True):
            if vs[d] != now:
                return (datetime.date.fromisoformat(d) + datetime.timedelta(days=1)).isoformat()
        end = start - datetime.timedelta(days=1)
    raise SystemExit('no vintage found: ' + sid)


def first_releases_keyless(sid):
    import datetime
    last = (datetime.date.fromisoformat(TO) + datetime.timedelta(days=200)).isoformat()
    vs = vintages(sid, FROM, last)
    obs = {o for d in vs for o in vs[d]}
    quarterly = obs and all(o[5:7] in ('01', '04', '07', '10') for o in obs)
    lo = max((o for o in obs if o <= FROM), default=FROM) if quarterly else FROM   # the period holding FROM, as the API gives it
    out = {}
    for d in sorted(vs):
        for o, v in vs[d].items():
            if lo <= o <= TO and o not in out:
                out[o] = (o, v, d)
    return [out[o] for o in sorted(out)]


def first_releases(sid):
    if not KEY:
        return first_releases_keyless(sid)
    d = get('series/observations', series_id=sid, output_type=4, realtime_start='1776-07-04',
            realtime_end='9999-12-31', observation_start=FROM, observation_end=TO)
    return [(o['date'], num(o['value']), o['realtime_start']) for o in d['observations'] if num(o['value']) is not None]


def vintage(sid, date):
    if not KEY:
        return vintages(sid, date, date)[date]
    d = get('series/observations', series_id=sid, realtime_start=date, realtime_end=date,
            observation_start='1959-01-01', observation_end=TO)
    return {o['date']: num(o['value']) for o in d['observations']}


def current(sid):
    return current_from(sid, '1959-01-01')


def current_from(sid, start):
    if not KEY:
        head, rows = csv_get(FRED_CSV + urllib.parse.urlencode({'id': sid, 'cosd': start, 'coed': TO}))
        return {r[0]: num(r[1]) for r in rows}
    d = get('series/observations', series_id=sid, observation_start=start, observation_end=TO)
    return {o['date']: num(o['value']) for o in d['observations']}


def base(sid, released):
    out = None
    for start, b in BASE.get(sid, []):
        if released >= start:
            out = b
    return out


def period(date, freq):
    y, m = int(date[:4]), int(date[5:7])
    return f'{y}-{m:02d}' if freq == 'M' else f'{y}Q{(m - 1) // 3 + 1}'


def prior(date, freq):
    y, m = int(date[:4]), int(date[5:7])
    m -= 1 if freq == 'M' else 3
    if m < 1:
        y, m = y - 1, m + 12
    return f'{y}-{m:02d}-01'


def year_ago(date):
    return f'{int(date[:4]) - 1}{date[4:]}'


# Percent change from the same month a year earlier, shown after the monthly change: the monthly
# series that are not seasonally adjusted (CPI, WPI) or whose monthly changes are small against
# the index's one-decimal rounding. Computed in the same release (or Report) as the figure, and
# in today's series for today's column.
YOY = {'cpi', 'wpi', 'industrial-production'}


# Change from the prior period, the same way in both columns:
#   pct     monthly percent change, not annualized (as BLS and the Fed report monthly series)
#   pct_ar  quarterly percent change at an annual rate, ((a/b)^4 - 1) (as BEA reports quarterly series)
#   pts     difference in percentage points (unemployment rate)
#   diff    difference in the series' own unit (payrolls in thousands; gold in $ millions)
def change(kind, a, b):
    if a is None or b is None or not kind:
        return None
    if kind == 'pct':
        return round(100 * (a / b - 1), 1)
    if kind == 'pct_ar':
        return round(100 * ((a / b) ** 4 - 1), 1)
    return round(a - b, 1)


def write(sid_key, meta, rows):
    path = os.path.join(OUT, f'{sid_key}.yaml')
    head = ('# Generated by tools/indicators/make_indicators.py. Edit the script, not this file.\n'
            '# p: reporting period; first: as first reported (released: date); chg: change from the prior\n'
            '# period in that release; yoy: change from a year earlier in that release; unit: the unit then,\n'
            '# where it differs; now, chg_now, yoy_now: as revised today.\n')
    body = yaml.safe_dump(dict(meta, rows=rows), sort_keys=False, allow_unicode=True, width=200,
                          default_flow_style=None)
    open(path, 'w', encoding='utf-8').write(head + body)
    print('wrote', path, len(rows))


def main():
    os.makedirs(OUT, exist_ok=True)
    firsts = {}
    for key, (sid, freq, name, u_then, u_now, kind, then, now) in API.items():
        cur = current(sid)
        rows = []
        for date, v, rel in first_releases(sid):
            vin = vintage(sid, rel)
            firsts.setdefault(sid, {})[date] = (v, rel)
            row = {'p': period(date, freq), 'first': v, 'released': rel}
            c = change(kind, v, vin.get(prior(date, freq)))
            if c is not None:
                row['chg'] = c
            if key in YOY:
                y = change('pct', v, vin.get(year_ago(date)))
                if y is not None:
                    row['yoy'] = y
            row['unit'] = base(sid, rel) or u_then
            row['now'] = cur.get(date)
            cn = change(kind, cur.get(date), cur.get(prior(date, freq)))
            if cn is not None:
                row['chg_now'] = cn
            if key in YOY:
                yn = change('pct', cur.get(date), cur.get(year_ago(date)))
                if yn is not None:
                    row['yoy_now'] = yn
            rows.append(row)
        write(key, {'id': key, 'name': name, 'freq': freq, 'change': kind,
                    'then': {'label': then, 'source': f'ALFRED {sid}, initial release', 'url': ALFRED + sid},
                    'now': {'label': now, 'unit': u_now, 'source': f'FRED {sid}', 'url': FRED + sid}}, rows)
    # Implicit deflator: nominal over real GNP in the release that first carried the quarter.
    sid, name, u_now, then, now = DEFLATOR
    cur = current(sid)
    curp = current_from(sid, '1960-07-01')
    rows = []
    for date, (g, rel) in sorted(firsts['GNP'].items()):
        vin_n, vin_r = vintage('GNP', rel), vintage('GNPC96', rel)
        r = vin_r.get(date)
        if not r:
            continue
        d = round(100 * g / r, 1)
        row = {'p': period(date, 'Q'), 'first': d, 'released': rel}
        pn, pr = vin_n.get(prior(date, 'Q')), vin_r.get(prior(date, 'Q'))
        if pn and pr:
            row['chg'] = change('pct_ar', d, 100 * pn / pr)
        row['unit'] = base(sid, rel)
        row['now'] = cur.get(date)
        cn = change('pct_ar', curp.get(date), curp.get(prior(date, 'Q')))
        if cn is not None:
            row['chg_now'] = cn
        rows.append(row)
    write('deflator', {'id': 'deflator', 'name': name, 'freq': 'Q', 'change': 'pct_ar',
                       'then': {'label': then, 'source': 'ALFRED GNP and GNPC96, initial release', 'url': ALFRED + 'GNP'},
                       'now': {'label': now, 'unit': u_now, 'source': f'FRED {sid}', 'url': FRED + sid}}, rows)


# ---------------------------------------------------------------- series transcribed from the Economic Reports
# Values read from the page images of the Economic Report of the President, January 1962 (transmitted
# Jan. 22, 1962), January 1963 (Jan. 21, 1963), January 1964 (Jan. 20, 1964; H. Doc. 88-278) and January 1965
# (Jan. 28, 1965; H. Doc. 89-28, Serial Set 12702), U.S. Congressional Serial Set on govinfo (1964 and 1965 read off
# FRASER's scans of the same printings, checked against govinfo's). For these series 'first' is the figure as it
# stood in the next January's Report, not the first release.
ERP = {
    1962: ('1962-01-22', 'Economic Report of the President, Jan. 1962',
           'https://www.govinfo.gov/app/details/SERIALSET-12497_00_00-002-0278-0000'),
    1963: ('1963-01-21', 'Economic Report of the President, Jan. 1963',
           'https://www.govinfo.gov/app/details/SERIALSET-12600_00_00-002-0028-0000'),
    1964: ('1964-01-20', 'Economic Report of the President, Jan. 1964',
           'https://www.govinfo.gov/app/details/SERIALSET-12658_00_00-002-0278-0000'),
    1965: ('1965-01-28', 'Economic Report of the President, Jan. 1965',
           'https://www.govinfo.gov/app/details/SERIALSET-12702_00_00-002-0028-0000'),
}
MONTHS = [f'{y}-{m:02d}' for y, m in [(1960, 12)] + [(y, m) for y in (1961, 1962, 1963, 1964) for m in range(1, 13)]]
MANUAL = {
    'wpi': dict(
        name='Wholesale price index', freq='M', change='pct',
        then='BLS, wholesale price index, all commodities', now_label='BLS, producer price index, all commodities',
        now_unit='1982=100', now_fred='PPIACO',
        tables={1962: 'Table B-40, p. 254 (1947–49=100)', 1963: 'Table C-41, p. 220 (1957–59=100)',
                1964: 'Table C-41, p. 256 (1957–59=100)', 1965: 'Table B-43, p. 240 (1957–59=100)'},
        prior={'1962-01': (100.4, 1963),    # Dec. 1961 on the 1957-59 base, Table C-41
               '1963-01': (100.4, 1964),    # Dec. 1962, Table C-41 of 1964 (as the 1963 Report printed it)
               '1964-01': (100.3, 1965)},   # Dec. 1963, Table B-43 of 1965 (as the 1964 Report printed it)
        # A year earlier, on the same base and from the same table, for the 12-month change.
        # Table B-40 gives 1959 as a year only, so Dec. 1960 has none.
        year_ago={1962: dict(zip(MONTHS[1:13], [119.3, 119.3, 120.0, 120.0, 119.7, 119.5,
                                                 119.7, 119.2, 119.2, 119.6, 119.6, 119.5])),   # 1960
                  1963: dict(zip(MONTHS[13:25], [101.0, 101.0, 101.0, 100.5, 100.0, 99.5,
                                                 99.9, 100.1, 100.0, 100.0, 100.0, 100.4])),   # 1961
                  1964: dict(zip(MONTHS[25:37], [100.8, 100.7, 100.7, 100.4, 100.2, 100.0,
                                                 100.4, 100.5, 101.2, 100.6, 100.7, 100.4])),   # 1962
                  1965: dict(zip(MONTHS[37:49], [100.5, 100.2, 99.9, 99.7, 100.0, 100.3,
                                                 100.6, 100.4, 100.3, 100.5, 100.7, 100.3]))},   # 1963
        rows={**{p: (v, 1962, '1947–49=100') for p, v in zip(MONTHS[:13], [
            119.5, 119.9, 120.0, 119.9, 119.4, 118.7, 118.2, 118.6, 118.9, 118.8, 118.7, 118.8, 119.2])},
              **{p: (v, 1963, '1957–59=100') for p, v in zip(MONTHS[13:25], [
            100.8, 100.7, 100.7, 100.4, 100.2, 100.0, 100.4, 100.5, 101.2, 100.6, 100.7, 100.4])},
              **{p: (v, 1964, '1957–59=100') for p, v in zip(MONTHS[25:37], [
            100.5, 100.2, 99.9, 99.7, 100.0, 100.3, 100.6, 100.4, 100.3, 100.5, 100.7, 100.3])},
              # Dec. 1964 preliminary in the Report (its note 2).
              **{p: (v, 1965, '1957–59=100') for p, v in zip(MONTHS[37:49], [
            101.0, 100.5, 100.4, 100.3, 100.1, 100.0, 100.4, 100.3, 100.7, 100.8, 100.7, 100.8])}}),
    'administrative-budget': dict(
        name='Federal budget (administrative)', freq='FY', fields=('receipts', 'expenditures', 'balance'),
        then='Treasury and Bureau of the Budget, net budget receipts and budget expenditures (the administrative budget), fiscal years ending June 30, millions of dollars',
        now_label='OMB, unified budget receipts, outlays, and surplus or deficit (a later concept, from fiscal 1969)',
        now_unit='millions of dollars', now_fred=('FYFR', 'FYONET', 'FYFSD'),
        tables={1962: 'Table B-55, p. 272', 1963: 'Table C-56, p. 238', 1964: 'Table C-56, p. 274',
                1965: 'Table B-59, p. 260'},
        rows={'FY1961': ((77659, 81515, -3856), 1962, 'millions of dollars'),
              'FY1962': ((81409, 87787, -6378), 1963, 'millions of dollars'),
              'FY1963': ((86376, 92642, -6266), 1964, 'millions of dollars'),
              'FY1964': ((89459, 97684, -8226), 1965, 'millions of dollars')},   # the deficit as printed (the difference is 8,225)
        est={'FY1962': [((82100, 89075, -6975), 1962)], 'FY1963': [((93000, 92537, 463), 1962), ((85500, 94311, -8811), 1963)],
             'FY1964': [((88400, 98405, -10005), 1964)], 'FY1965': [((93000, 97900, -4900), 1964), ((91200, 97481, -6281), 1965)],
             'FY1966': [((94400, 99687, -5287), 1965)]}),
    'cash-budget': dict(
        name='Federal cash receipts from and payments to the public', freq='FY', fields=('receipts', 'payments', 'balance'),
        then='Treasury, Bureau of the Budget, and CEA, the consolidated cash statement, federal, fiscal years, billions of dollars',
        now_label='OMB, unified budget receipts, outlays, and surplus or deficit (a later concept, from fiscal 1969)',
        now_unit='millions of dollars', now_fred=('FYFR', 'FYONET', 'FYFSD'),
        tables={1962: 'Table B-57, p. 274', 1963: 'Table C-58, p. 240', 1964: 'Table C-58, p. 276',
                1965: 'Table B-60, p. 261'},
        rows={'FY1961': ((97.2, 99.5, -2.3), 1962, 'billions of dollars'),
              'FY1962': ((101.9, 107.7, -5.8), 1963, 'billions of dollars'),
              'FY1963': ((109.7, 113.8, -4.0), 1964, 'billions of dollars'),
              'FY1964': ((115.5, 120.3, -4.8), 1965, 'billions of dollars')},
        est={'FY1962': [((102.6, 111.1, -8.5), 1962)], 'FY1963': [((116.6, 114.8, 1.8), 1962), ((108.4, 116.8, -8.3), 1963)],
             'FY1964': [((114.4, 122.7, -8.3), 1964)], 'FY1965': [((119.7, 122.7, -2.9), 1964), ((117.4, 121.4, -4.0), 1965)],
             'FY1966': [((123.5, 127.4, -3.9), 1965)]}),
    'federal-national-accounts': dict(
        name='Federal receipts and expenditures, national income accounts', freq='Q', fields=('receipts', 'expenditures', 'balance'),
        then='Commerce and Bureau of the Budget, federal government receipts and expenditures in the national income accounts, seasonally adjusted annual rates, billions of dollars',
        now_label='BEA, federal government current receipts and current expenditures, SAAR (balance computed)',
        now_unit='billions of dollars, SAAR', now_fred=('FGRECPT', 'FGEXPND', None),
        tables={1962: 'Table B-59, p. 276', 1963: 'Table C-60, p. 242', 1964: 'Table C-60, p. 278',
                1965: 'Table B-62, p. 263'},
        rows={'1960Q4': ((94.6, 94.2, 0.4), 1962, 'billions of dollars, annual rate'), '1961Q1': ((92.5, 98.0, -5.5), 1962, 'billions of dollars, annual rate'),
              '1961Q2': ((96.8, 101.1, -4.3), 1962, 'billions of dollars, annual rate'), '1961Q3': ((99.3, 102.4, -3.1), 1962, 'billions of dollars, annual rate'),
              '1961Q4': ((103.8, 105.1, -1.3), 1963, 'billions of dollars, annual rate'), '1962Q1': ((105.9, 108.3, -2.4), 1963, 'billions of dollars, annual rate'),
              '1962Q2': ((108.4, 109.0, -0.7), 1963, 'billions of dollars, annual rate'), '1962Q3': ((108.9, 109.8, -0.9), 1963, 'billions of dollars, annual rate'),
              '1962Q4': ((None, 112.5, None), 1963, 'billions of dollars, annual rate'),
              '1963Q1': ((110.0, 114.5, -4.6), 1964, 'billions of dollars, annual rate'), '1963Q2': ((112.3, 115.3, -3.0), 1964, 'billions of dollars, annual rate'),
              '1963Q3': ((114.3, 116.1, -1.8), 1964, 'billions of dollars, annual rate'),
              # Q4 1963 from the 1965 Report, which completes it (the 1964 Report: receipts n.a., expenditures 118.4).
              '1963Q4': ((117.2, 116.6, 0.6), 1965, 'billions of dollars, annual rate'),
              '1964Q1': ((114.8, 117.2, -2.4), 1965, 'billions of dollars, annual rate'), '1964Q2': ((112.3, 120.2, -7.8), 1965, 'billions of dollars, annual rate'),
              '1964Q3': ((114.0, 119.2, -5.2), 1965, 'billions of dollars, annual rate'), '1964Q4': ((None, 120.3, None), 1965, 'billions of dollars, annual rate')}),
    'balance-of-payments': dict(
        name='Balance of payments, over-all surplus or deficit', freq='Q', fields=('balance',),
        then='Commerce, over-all balance (changes in U.S. gold stock, convertible currencies, and liquid liabilities to foreigners), seasonally adjusted annual rates, millions of dollars',
        now_label='No longer published: the over-all (liquidity) balance was dropped from the official accounts',
        now_unit=None, now_fred=None,
        tables={1963: 'Table C-78, p. 263', 1964: 'Table C-77, p. 298'},
        rows={'1960Q4': ((-5252,), 1963, 'millions of dollars, annual rate'), '1961Q1': ((-1276,), 1963, 'millions of dollars, annual rate'), '1961Q2': ((704,), 1963, 'millions of dollars, annual rate'),
              '1961Q3': ((-3640,), 1963, 'millions of dollars, annual rate'), '1961Q4': ((-5632,), 1963, 'millions of dollars, annual rate'), '1962Q1': ((-1968,), 1963, 'millions of dollars, annual rate'),
              '1962Q2': ((-904,), 1963, 'millions of dollars, annual rate'), '1962Q3': ((-2876,), 1963, 'millions of dollars, annual rate'),
              '1962Q4': ((-3172,), 1964, 'millions of dollars, annual rate'), '1963Q1': ((-3460,), 1964, 'millions of dollars, annual rate'),
              '1963Q2': ((-4956,), 1964, 'millions of dollars, annual rate'), '1963Q3': ((-1024,), 1964, 'millions of dollars, annual rate'),
              '1960': ((-3925,), 1963, 'millions of dollars, year'), '1961': ((-2461,), 1963, 'millions of dollars, year'),
              '1962': ((-1916,), 1963, 'millions of dollars, annual rate, first three quarters'),
              '1963': ((-3147,), 1964, 'millions of dollars, annual rate, first three quarters')}),
    # The Jan. 1965 Report prints the balance on regular transactions in place of the over-all balance: before
    # special government transactions (debt prepayments, advances on military exports, nonmarketable bonds and
    # notes). Another concept, so another series (STYLE 8 in tools/bib/indicators.py).
    'balance-of-payments-regular': dict(
        name='Balance of payments, balance on regular transactions', freq='Q', fields=('balance',),
        then='Commerce, balance on regular transactions (before special government transactions), seasonally adjusted annual rates, millions of dollars',
        now_label='No longer published', now_unit=None, now_fred=None,
        tables={1965: 'Table B-79, p. 283'},
        rows={'1963Q4': ((-1592,), 1965, 'millions of dollars, annual rate'), '1964Q1': ((-968,), 1965, 'millions of dollars, annual rate'),
              '1964Q2': ((-2764,), 1965, 'millions of dollars, annual rate'), '1964Q3': ((-2264,), 1965, 'millions of dollars, annual rate'),
              '1963': ((-3261,), 1965, 'millions of dollars, year'),
              '1964': ((-1998,), 1965, 'millions of dollars, annual rate, first three quarters')}),
    'gap-cea': dict(
        name='Output gap, CEA (contemporary)', freq='Q',
        then='Council of Economic Advisers: potential GNP (a 3½ percent trend through actual GNP in mid-1955; from Jan. 1965, 3¾ percent after 1962; at 4 percent unemployment) less actual GNP',
        now_label=None, now_unit=None, now_fred=None,
        tables={1962: 'ch. 1, "Full Production," p. 49', 1963: "President's message, p. xiii",
                1964: 'ch. 1, "Unemployment and Unused Potential Output," p. 37',
                1965: 'ch. 1, "Problems Unsolved," p. 39'},
        # A figure from another page of the same Report than its table entry.
        src={'1964': 'ch. 2, "The Gap Between Actual and Potential GNP," p. 83'},
        rows={'1961Q1': (51, 1962, 'billions of 1961 dollars, annual rate'),
              '1961Q4': (28, 1962, 'billions of 1961 dollars, annual rate'),
              '1961': (40, 1962, 'billions of 1961 dollars, year'),
              '1962Q4': ('30–40', 1963, 'billions of dollars, annual rate'),
              '1963Q4': (30, 1964, 'billions of 1963 dollars, annual rate'),
              '1964Q4': ('25–30', 1965, 'billions of dollars, annual rate'),
              '1964': (27, 1965, 'billions of 1964 dollars, year')}),
    'gold-stock': dict(
        name='Monetary gold stock', freq='M', change='diff',
        then=None, now_label='Treasury monetary gold stock, end of month, as compiled by NBER from the Federal Reserve Bulletin',
        now_unit='millions of dollars', now_fred='M1476CUSM144NNBR', tables={}, rows={p: (None, None, None) for p in MONTHS}),
}


def fred_obs(sid):
    d = get('series/observations', series_id=sid, observation_start='1959-01-01', observation_end=TO)
    return {o['date']: num(o['value']) for o in d['observations']}


def pdate(p):
    """FRED observation date for a reporting period."""
    if p.startswith('FY'):
        return f'{p[2:]}-06-30'          # FRED dates the fiscal year by its last day? checked below
    if 'Q' in p:
        y, q = p.split('Q')
        return f'{y}-{3 * (int(q) - 1) + 1:02d}-01'
    if len(p) == 4:
        return f'{p}-01-01'
    return f'{p}-01'


def prev_p(p):
    if 'Q' in p:
        y, q = int(p[:4]), int(p[-1])
        return f'{y - 1}Q4' if q == 1 else f'{y}Q{q - 1}'
    if len(p) == 7:
        y, mo = int(p[:4]), int(p[5:7])
        return f'{y - 1}-12' if mo == 1 else f'{y}-{mo - 1:02d}'
    return p


# Qualifiers the source puts on a figure ("about $28 billion"; "some $30-40 billion").
QUAL = {('gap-cea', '1961Q4'): 'about', ('gap-cea', '1962Q4'): 'some', ('gap-cea', '1963Q4'): 'close to'}
# Notes the source attaches to a single figure, shown after it.
NOTE = {('balance-of-payments', '1962'): 'Q1–Q3, annual rate', ('balance-of-payments', '1963'): 'Q1–Q3, annual rate',
        ('balance-of-payments-regular', '1964'): 'Q1–Q3, annual rate'}


def manual():
    for key, m in MANUAL.items():
        nf = m['now_fred']
        nows = [fred_obs(s) if s else None for s in (nf if isinstance(nf, tuple) else (nf,))] if nf else []
        def now_for(p):
            if not nows:
                return None
            ds = pdate(p)
            if p.startswith('FY') and nows[0] and ds not in nows[0]:
                ds = next((d for d in nows[0] if d.startswith(p[2:])), ds)
            vals = [n.get(ds) if n else None for n in nows]
            if isinstance(nf, tuple):
                if nf[2] is None and vals[0] is not None and vals[1] is not None:
                    vals[2] = round(vals[0] - vals[1], 3)
                return dict(zip(m['fields'], vals))
            return vals[0]
        rows = []
        prev = None
        for p, (v, erp, unit) in m['rows'].items():
            row = {'p': p}
            if v is not None:
                row['first'] = dict(zip(m['fields'], v)) if m.get('fields') else v
                row['released'] = ERP[erp][0]
                row['source'] = f'{ERP[erp][1]}, {m.get("src", {}).get(p) or m["tables"][erp]}'
                if unit:
                    row['unit'] = unit
                base_v = prev if prev and prev[1] == erp else m.get('prior', {}).get(p)
                if m.get('change') and base_v and not isinstance(v, (tuple, str)):
                    row['chg'] = change(m['change'], v, base_v[0])
                if key in YOY and not isinstance(v, (tuple, str)):
                    y = change('pct', v, m.get('year_ago', {}).get(erp, {}).get(p))
                    if y is not None:
                        row['yoy'] = y
                prev = (v, erp)
                if (key, p) in QUAL:
                    row['q'] = QUAL[(key, p)]
                if (key, p) in NOTE:
                    row['note'] = NOTE[(key, p)]
            for e in m.get('est', {}).get(p, []):
                row.setdefault('est', []).append({'value': dict(zip(m['fields'], e[0])), 'as_of': ERP[e[1]][0],
                                                  'source': f'{ERP[e[1]][1]}, {m["tables"][e[1]]}'})
            row['now'] = now_for(p)
            if m.get('change') and not isinstance(row['now'], dict):
                c = change(m['change'], row['now'], now_for(prev_p(p)))
                if c is not None:
                    row['chg_now'] = c
            if key in YOY:
                y = change('pct', row['now'], now_for(f'{int(p[:4]) - 1}{p[4:]}'))
                if y is not None:
                    row['yoy_now'] = y
            rows.append(row)
        for p, ests in m.get('est', {}).items():
            if p not in m['rows']:
                rows.append({'p': p, 'est': [{'value': dict(zip(m['fields'], e[0])), 'as_of': ERP[e[1]][0],
                                              'source': f'{ERP[e[1]][1]}, {m["tables"][e[1]]}'} for e in ests],
                             'now': now_for(p)})
        meta = {'id': key, 'name': m['name'], 'freq': m['freq'], 'manual': True}
        if m.get('fields'):
            meta['fields'] = list(m['fields'])
        if m.get('change'):
            meta['change'] = m['change']
        meta['then'] = {'label': m['then'], 'source': 'Economic Report of the President, statistical tables'} if m['then'] else None
        meta['now'] = {'label': m['now_label'], 'unit': m['now_unit'],
                       'source': ('FRED ' + ', '.join(s for s in (nf if isinstance(nf, tuple) else (nf,)) if s)) if nf else None,
                       'url': (FRED + (nf[0] if isinstance(nf, tuple) else nf)) if nf else None}
        write(key, meta, rows)


def gap_cbo():
    """Retrospective output gap: CBO potential GDP against BEA real GDP, as published today."""
    pot, act = current_from('GDPPOT', '1960-01-01'), current_from('GDPC1', '1960-01-01')
    vin = (get('series/vintagedates', series_id='GDPPOT', sort_order='desc', limit=1)['vintage_dates'][0] if KEY
           else latest_vintage('GDPPOT'))
    rows, years = [], {}
    for d in sorted(pot):
        if d in act and pot[d]:
            g = round(100 * (act[d] / pot[d] - 1), 1)
            p = period(d, 'Q')
            years.setdefault(p[:4], []).append(g)
            if d >= '1960-10-01':
                rows.append({'p': p, 'now': g})
    for y in ('1960', '1961', '1962', '1963', '1964'):
        if len(years.get(y, [])) == 4:
            rows.append({'p': y, 'now': round(sum(years[y]) / 4, 1)})
    write('gap-cbo', {'id': 'gap-cbo', 'name': 'Output gap, CBO (retrospective)', 'freq': 'Q', 'then': None,
                      'now': {'label': f'CBO potential GDP (GDPPOT, vintage {vin}) against BEA real GDP (GDPC1): real GDP over potential, less 1, percent',
                              'unit': 'percent of potential', 'source': f'FRED GDPPOT and GDPC1, vintage {vin}',
                              'url': FRED + 'GDPPOT', 'vintage': vin}}, rows)


# ---------------------------------------------------------------- money and credit: interest rates
# Not revised: FRED's monthly averages are the figures the Federal Reserve Bulletin printed at the time (Feb. 1965,
# p. 286: the federal funds rate and the 3-month bill's market yield for 1964, month by month, as FRED has them).
# So one column, today's (STYLE 7 in tools/bib/indicators.py), with the change from the prior month in points.
# id: (FRED series, name, label)
RATES = {
    'federal-funds': ('FEDFUNDS', 'Federal funds rate',
                      'Board of Governors, H.15: effective federal funds rate, monthly average of daily figures'),
    'prime-rate': ('MPRIME', 'Prime rate',
                   'Board of Governors, H.15: bank prime loan rate, monthly average of daily figures'),
    'treasury-bill': ('TB3MS', 'Treasury bill rate, 3-month',
                      'Board of Governors, H.15: 3-month Treasury bill, secondary market, discount basis, monthly average of business days'),
    'treasury-10-year': ('GS10', 'Treasury yield, 10-year',
                         'Board of Governors, H.15: 10-year Treasury constant maturity, monthly average of business days'),
}
# Administered rates show a change only in a month the rate changed (the prime stood at 4½ percent throughout).
ADMIN = {'prime-rate'}

# The discount rate of the Federal Reserve Bank of New York, by hand: each change, its effective date, the day the
# Board announced it, the new rate, and where it is printed (Federal Reserve Bulletin and the Board's press
# releases, on FRASER). The two 1960 changes set the rate standing in Dec. 1960.
FRASER = 'https://fraser.stlouisfed.org/title/'
DISCOUNT = [
    ('1960-06-10', None, 3.5, 'Federal Reserve Bulletin, July 1960, p. 756 (from 4 percent)'),
    ('1960-08-12', None, 3.0, 'Federal Reserve Bulletin, Sept. 1960, p. 1014'),
    ('1963-07-17', '1963-07-16', 3.5, 'Board of Governors, press release, July 16, 1963; Federal Reserve Bulletin, Sept. 1963, p. 1264'),
    ('1964-11-24', '1964-11-23', 4.0, 'Board of Governors, press release, Nov. 23, 1964; Federal Reserve Bulletin, Dec. 1964, pp. 1530–31, and Feb. 1965, p. 267'),
]


def month_end(p):
    import calendar
    y, m = int(p[:4]), int(p[5:7])
    return f'{p}-{calendar.monthrange(y, m)[1]:02d}'


def label_day(iso):
    mon = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']
    return f'{mon[int(iso[5:7]) - 1]} {int(iso[8:])}'


def rates():
    meta = lambda key, sid, name, label: {
        'id': key, 'name': name, 'freq': 'M', 'kind': 'rate', 'change': 'pts', 'then': None,
        'now': {'label': label, 'unit': 'percent', 'source': f'FRED {sid}', 'url': FRED + sid}}
    for key, (sid, name, label) in RATES.items():
        cur = current_from(sid, '1960-11-01')
        rows = []
        for p in MONTHS:
            d = f'{p}-01'
            row = {'p': p, 'now': cur.get(d)}
            c = None if cur.get(d) is None or cur.get(prior(d, 'M')) is None else round(cur[d] - cur[prior(d, 'M')], 2)
            if c is not None and not (key in ADMIN and c == 0):
                row['chg_now'] = c
            rows.append(row)
        write(key, meta(key, sid, name, label), rows)
    rows = []
    for p in MONTHS:
        lo, hi = f'{p}-01', month_end(p)
        standing = [x for x in DISCOUNT if x[0] <= hi]
        eff, ann, v, src = standing[-1]
        row = {'p': p, 'first': v}
        if lo <= eff:                      # a change this month
            row['chg'] = round(v - standing[-2][2], 2)
            row['released'] = ann
            row['note'] = f'effective {label_day(eff)}'
        else:
            row['since'] = eff
        row['unit'] = 'percent'
        row['source'] = src
        rows.append(row)
    write('discount-rate', {'id': 'discount-rate', 'name': 'Discount rate, New York Reserve Bank', 'freq': 'M',
                            'manual': True, 'kind': 'rate', 'change': 'pts',
                            'then': {'label': 'Federal Reserve Bank of New York, rate on discounts for and advances to member banks (Secs. 13 and 13a), in effect at the end of the month',
                                     'source': 'Board of Governors, announcements and Federal Reserve Bulletin'},
                            'now': None}, rows)


if __name__ == '__main__':
    if ONLY is None or 'alfred' in ONLY:
        main()
    if ONLY is None or 'manual' in ONLY:
        manual()
    if ONLY is None or 'gap' in ONLY:
        gap_cbo()
    if ONLY is None or 'rates' in ONLY:
        rates()
