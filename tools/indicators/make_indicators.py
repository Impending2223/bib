"""Monthly and quarterly indicators for the calendar, as first reported and as revised today.
# Usage: FRED_API_KEY=... python3 tools/indicators/make_indicators.py [FROM TO]
#   FROM, TO are reporting periods, default 1960-01-01 1968-12-31.
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
#   Federal debt (DEBT below): the public debt by month from the Treasury Bulletin; the debt and net interest over GNP
#   and the primary balance by quarter from the Economic Reports; OMB's fiscal-year ratios. --only debt writes these.
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request
import yaml

KEY = os.environ.get('FRED_API_KEY')     # without it, the public CSV downloads (KEYLESS below)
ONLY = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
ARGS = [a for i, a in enumerate(sys.argv[1:], 1) if a != '--only' and sys.argv[i - 1] != '--only']
FROM, TO = (ARGS[0], ARGS[1]) if len(ARGS) > 1 else ('1960-01-01', '1968-12-31')
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
        # 1957-59=100 from ALFRED's vintage of Nov. 16, 1962 (the 1957-59 average of that day's vintage is 100.0; the
        # day before, 99.3, with 1957 at 100.0); the Reports of Jan. 1967 (Table B-32) and Feb. 1968 (Table B-35) print 1957-59=100
        'INDPRO': [('1900-01-01', '1957=100'), ('1962-11-16', '1957–59=100')],
        # the benchmark revision of Aug. 19, 1965 (ALFRED's vintage of that day) moved constant dollars to 1958 prices
        'GNPC96': [('1900-01-01', 'billions of 1954 dollars, SAAR'), ('1965-08-19', 'billions of 1958 dollars, SAAR')],
        'GNPDEF': [('1900-01-01', '1954=100'), ('1965-08-19', '1958=100')]}


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


def csv_get(url, missing_ok=False):
    for i in range(5):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                rows = r.read().decode().strip().split('\n')
            head = rows[0].split(',')
            return head, [x.split(',') for x in rows[1:]]
        except urllib.error.HTTPError as e:
            if e.code == 404 and missing_ok:
                return None
            time.sleep(2 * (i + 1))
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

    def fetch(chunk):
        q = {'id': ','.join([sid] * len(chunk)), 'vintage_date': ','.join(chunk),
             'cosd': ','.join(['1959-01-01'] * len(chunk)), 'coed': ','.join([TO] * len(chunk))}
        got = csv_get(ALFRED_CSV + urllib.parse.urlencode(q, safe=','), missing_ok=True)
        if got is None:
            # ALFRED answers 404 for a day before the series' first vintage (UNRATE's is Apr. 12, 1960), and for the
            # whole request if any day in it is: ask day by day, a 404 day holding no observations.
            if len(chunk) == 1:
                _VIN[(sid, chunk[0])] = {}
                return
            for d in chunk:
                fetch([d])
            return
        head, rows = got
        col = {h.rsplit('_', 1)[-1]: j for j, h in enumerate(head) if j}
        for d in chunk:
            j = col.get(d.replace('-', ''))
            if j is None:
                raise SystemExit(f'ALFRED returned no column for {sid} {d}')
            _VIN[(sid, d)] = {r[0]: num(r[j]) for r in rows if len(r) > j and num(r[j]) is not None}

    for i in range(0, len(want), 12):
        fetch(want[i:i + 12])
    return {d: _VIN[(sid, d)] for d in days(first, last)}


def latest_vintage(sid):
    """The day the series last changed: back from today, the first day whose vintage differs from today's."""
    import datetime
    # ALFRED's newest vintage can lag our date by a day (its clock): start from the latest day it serves.
    for back in range(4):
        today = datetime.date.today() - datetime.timedelta(days=back)
        try:
            now = vintages(sid, today.isoformat(), today.isoformat())[today.isoformat()]
            if now:                        # a day not yet served comes back empty (a 404)
                break
        except SystemExit:
            continue
    else:
        raise SystemExit('ALFRED serves no recent vintage: ' + sid)
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
# Jan. 22, 1962), January 1963 (Jan. 21, 1963), January 1964 (Jan. 20, 1964; H. Doc. 88-278), January 1965
# (Jan. 28, 1965; H. Doc. 89-28, Serial Set 12702) and January 1966 (Jan. 27, 1966; H. Doc. 89-348, Serial Set 12742),
# U.S. Congressional Serial Set on govinfo (1964, 1965 and 1966 read off FRASER's scans of the same printings, checked
# against govinfo's). January 1967 (Jan. 26, 1967) read off FRASER's scan alone, page images checked against its text
# layer: govinfo holds no copy (no ERP-1967 package; its Serial Set has the Reports of 1966 and Feb. 1968, not 1967's,
# searched Oct. 15, 2026). February 1968 (transmitted Feb. 1, 1968; H. Doc. 90-238, Serial Set 12825) read off govinfo's
# scan, page images checked against its text layer. January 1969 (transmitted Jan. 16, 1969; H. Doc. 91-28, Serial Set
# 12868), Johnson's last, read off FRASER's scan (ERP_1969.pdf: the printed page plus 6) and checked against govinfo's
# (the printed page plus 4), page images against FRASER's text layer. For these series 'first' is the figure as it
# stood in the next Report (January, or February in 1968), not the first release.
ERP = {
    1962: ('1962-01-22', 'Economic Report of the President, Jan. 1962',
           'https://www.govinfo.gov/app/details/SERIALSET-12497_00_00-002-0278-0000'),
    1963: ('1963-01-21', 'Economic Report of the President, Jan. 1963',
           'https://www.govinfo.gov/app/details/SERIALSET-12600_00_00-002-0028-0000'),
    1964: ('1964-01-20', 'Economic Report of the President, Jan. 1964',
           'https://www.govinfo.gov/app/details/SERIALSET-12658_00_00-002-0278-0000'),
    1965: ('1965-01-28', 'Economic Report of the President, Jan. 1965',
           'https://www.govinfo.gov/app/details/SERIALSET-12702_00_00-002-0028-0000'),
    1966: ('1966-01-27', 'Economic Report of the President, Jan. 1966',
           'https://www.govinfo.gov/app/details/SERIALSET-12742_00_00-002-0348-0000'),
    1967: ('1967-01-26', 'Economic Report of the President, Jan. 1967',
           'https://fraser.stlouisfed.org/title/economic-report-president-45/1967-8138'),
    1968: ('1968-02-01', 'Economic Report of the President, Feb. 1968',
           'https://www.govinfo.gov/app/details/SERIALSET-12825_00_00-002-0238-0000'),
    1969: ('1969-01-16', 'Economic Report of the President, Jan. 1969',
           'https://www.govinfo.gov/app/details/SERIALSET-12868_00_00-002-0028-0000'),
}
MONTHS = [f'{y}-{m:02d}' for y, m in [(1960, 12)] + [(y, m) for y in (1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968) for m in range(1, 13)]]
RATE_MONTHS = [f'{y}-{m:02d}' for y in range(1960, 1969) for m in range(1, 13)]   # the money-rate tables' span
MANUAL = {
    'wpi': dict(
        name='Wholesale price index', freq='M', change='pct',
        then='BLS, wholesale price index, all commodities', now_label='BLS, producer price index, all commodities',
        now_unit='1982=100', now_fred='PPIACO',
        tables={1962: 'Table B-40, p. 254 (1947–49=100)', 1963: 'Table C-41, p. 220 (1957–59=100)',
                1964: 'Table C-41, p. 256 (1957–59=100)', 1965: 'Table B-43, p. 240 (1957–59=100)',
                1966: 'Table C-41, p. 257 (1957–59=100)', 1967: 'Table B-44, p. 264 (1957–59=100)',
                1968: 'Table B-48, p. 264 (1957–59=100)', 1969: 'Table B-48, p. 282 (1957–59=100)'},
        prior={'1962-01': (100.4, 1963),    # Dec. 1961 on the 1957-59 base, Table C-41
               '1963-01': (100.4, 1964),    # Dec. 1962, Table C-41 of 1964 (as the 1963 Report printed it)
               '1964-01': (100.3, 1965),    # Dec. 1963, Table B-43 of 1965 (as the 1964 Report printed it)
               '1965-01': (100.7, 1966),    # Dec. 1964, Table C-41 of 1966 (the 1965 Report: 100.8, preliminary)
               '1966-01': (104.1, 1967),    # Dec. 1965, Table B-44 of 1967 (as the 1966 Report printed it)
               '1967-01': (105.9, 1968),    # Dec. 1966, Table B-48 of 1968 (as the 1967 Report printed it, preliminary)
               '1968-01': (106.8, 1969)},   # Dec. 1967, Table B-48 of 1969 (as the 1968 Report printed it)
        # A year earlier, on the same base and from the same table, for the 12-month change.
        # Table B-40 gives 1959 as a year only, so Dec. 1960 has none.
        year_ago={1962: dict(zip(MONTHS[1:13], [119.3, 119.3, 120.0, 120.0, 119.7, 119.5,
                                                 119.7, 119.2, 119.2, 119.6, 119.6, 119.5])),   # 1960
                  1963: dict(zip(MONTHS[13:25], [101.0, 101.0, 101.0, 100.5, 100.0, 99.5,
                                                 99.9, 100.1, 100.0, 100.0, 100.0, 100.4])),   # 1961
                  1964: dict(zip(MONTHS[25:37], [100.8, 100.7, 100.7, 100.4, 100.2, 100.0,
                                                 100.4, 100.5, 101.2, 100.6, 100.7, 100.4])),   # 1962
                  1965: dict(zip(MONTHS[37:49], [100.5, 100.2, 99.9, 99.7, 100.0, 100.3,
                                                 100.6, 100.4, 100.3, 100.5, 100.7, 100.3])),   # 1963
                  1966: dict(zip(MONTHS[49:61], [101.0, 100.5, 100.4, 100.3, 100.1, 100.0,
                                                 100.4, 100.3, 100.7, 100.8, 100.7, 100.7])),   # 1964
                  1967: dict(zip(MONTHS[61:73], [101.0, 101.2, 101.3, 101.7, 102.1, 102.8,
                                                 102.9, 102.9, 103.0, 103.1, 103.5, 104.1])),   # 1965
                  1968: dict(zip(MONTHS[73:85], [104.6, 105.4, 105.4, 105.5, 105.6, 105.7,
                                                 106.4, 106.8, 106.8, 106.2, 105.9, 105.9])),   # 1966
                  1969: dict(zip(MONTHS[85:97], [106.2, 106.0, 105.7, 105.3, 105.8, 106.3,
                                                 106.5, 106.1, 106.2, 106.1, 106.2, 106.8]))},   # 1967
        rows={**{p: (v, 1962, '1947–49=100') for p, v in zip(MONTHS[:13], [
            119.5, 119.9, 120.0, 119.9, 119.4, 118.7, 118.2, 118.6, 118.9, 118.8, 118.7, 118.8, 119.2])},
              **{p: (v, 1963, '1957–59=100') for p, v in zip(MONTHS[13:25], [
            100.8, 100.7, 100.7, 100.4, 100.2, 100.0, 100.4, 100.5, 101.2, 100.6, 100.7, 100.4])},
              **{p: (v, 1964, '1957–59=100') for p, v in zip(MONTHS[25:37], [
            100.5, 100.2, 99.9, 99.7, 100.0, 100.3, 100.6, 100.4, 100.3, 100.5, 100.7, 100.3])},
              # Dec. 1964 preliminary in the Report (its note 2).
              **{p: (v, 1965, '1957–59=100') for p, v in zip(MONTHS[37:49], [
            101.0, 100.5, 100.4, 100.3, 100.1, 100.0, 100.4, 100.3, 100.7, 100.8, 100.7, 100.8])},
              # Dec. 1965 preliminary in the Report (its note 2).
              **{p: (v, 1966, '1957–59=100') for p, v in zip(MONTHS[49:61], [
            101.0, 101.2, 101.3, 101.7, 102.1, 102.8, 102.9, 102.9, 103.0, 103.1, 103.5, 104.1])},
              # Dec. 1966 preliminary in the Report (marked p); the 1968 Report prints the same 105.9.
              **{p: (v, 1967, '1957–59=100') for p, v in zip(MONTHS[61:73], [
            104.6, 105.4, 105.4, 105.5, 105.6, 105.7, 106.4, 106.8, 106.8, 106.2, 105.9, 105.9])},
              # None marked preliminary in the 1968 Report's table.
              **{p: (v, 1968, '1957–59=100') for p, v in zip(MONTHS[73:85], [
            106.2, 106.0, 105.7, 105.3, 105.8, 106.3, 106.5, 106.1, 106.2, 106.1, 106.2, 106.8])},
              # Dec. 1968 preliminary in the Report (marked p); the year 1968 printed as the January-November average
              # (its note 2). The 1967 months as the 1968 Report printed them.
              **{p: (v, 1969, '1957–59=100') for p, v in zip(MONTHS[85:97], [
            107.2, 108.0, 108.2, 108.3, 108.5, 108.7, 109.1, 108.7, 109.1, 109.1, 109.6, 109.8])}}),
    'administrative-budget': dict(
        name='Federal budget (administrative)', freq='FY', fields=('receipts', 'expenditures', 'balance'),
        then='Treasury and Bureau of the Budget, net budget receipts and budget expenditures (the administrative budget), fiscal years ending June 30, millions of dollars',
        now_label='OMB, unified budget receipts, outlays, and surplus or deficit (a later concept, from fiscal 1969)',
        now_unit='millions of dollars', now_fred=('FYFR', 'FYONET', 'FYFSD'),
        tables={1962: 'Table B-55, p. 272', 1963: 'Table C-56, p. 238', 1964: 'Table C-56, p. 274',
                1965: 'Table B-59, p. 260', 1966: 'Table C-58, p. 278', 1967: 'Table B-60, p. 284',
                1968: 'Table B-63, p. 284'},
        # The Feb. 1968 Report sets out the budget for fiscal 1969 on the unified concept (Tables B-59, B-60) and prints
        # the administrative and cash budgets once more, "under the old concepts" (Table B-63, its note: "those used in
        # budgets of the U.S. Government for years prior to fiscal 1969"), actual through fiscal 1967, estimates for 1968
        # and 1969. The unified budget is another concept (STYLE 8), not carried here.
        unit='millions of dollars',
        rows={'FY1961': ((77659, 81515, -3856), 1962, 'millions of dollars'),
              'FY1962': ((81409, 87787, -6378), 1963, 'millions of dollars'),
              'FY1963': ((86376, 92642, -6266), 1964, 'millions of dollars'),
              'FY1964': ((89459, 97684, -8226), 1965, 'millions of dollars'),   # the deficit as printed (the difference is 8,225)
              'FY1965': ((93072, 96507, -3435), 1966, 'millions of dollars'),
              'FY1966': ((104727, 106978, -2251), 1967, 'millions of dollars'),
              'FY1967': ((115849, 125718, -9869), 1968, 'millions of dollars')},
        est={'FY1962': [((82100, 89075, -6975), 1962)], 'FY1963': [((93000, 92537, 463), 1962), ((85500, 94311, -8811), 1963)],
             'FY1964': [((88400, 98405, -10005), 1964)], 'FY1965': [((93000, 97900, -4900), 1964), ((91200, 97481, -6281), 1965)],
             'FY1966': [((94400, 99687, -5287), 1965), ((100000, 106428, -6428), 1966)],
             'FY1967': [((111000, 112847, -1847), 1966), ((116995, 126729, -9734), 1967)],
             'FY1968': [((126937, 135033, -8096), 1967), ((118575, 137182, -18607), 1968)],
             'FY1969': [((135587, 147363, -11776), 1968)]}),
    'cash-budget': dict(
        name='Federal cash receipts from and payments to the public', freq='FY', fields=('receipts', 'payments', 'balance'),
        then='Treasury, Bureau of the Budget, and CEA, the consolidated cash statement, federal, fiscal years, billions of dollars',
        now_label='OMB, unified budget receipts, outlays, and surplus or deficit (a later concept, from fiscal 1969)',
        now_unit='millions of dollars', now_fred=('FYFR', 'FYONET', 'FYFSD'),
        tables={1962: 'Table B-57, p. 274', 1963: 'Table C-58, p. 240', 1964: 'Table C-58, p. 276',
                1965: 'Table B-60, p. 261', 1966: 'Table C-59, p. 279', 1967: 'Table B-61, p. 285',
                1968: 'Table B-63, p. 284'},
        # In billions through the Jan. 1967 Report; the Feb. 1968 Report's Table B-63 in millions. A row is in the unit
        # of its first-reported figure (else of its latest estimate); an estimate printed in the other unit is put into
        # the row's and keeps its printed figures ('printed'). See est_entry below.
        unit='billions of dollars',
        rows={'FY1961': ((97.2, 99.5, -2.3), 1962, 'billions of dollars'),
              'FY1962': ((101.9, 107.7, -5.8), 1963, 'billions of dollars'),
              'FY1963': ((109.7, 113.8, -4.0), 1964, 'billions of dollars'),
              'FY1964': ((115.5, 120.3, -4.8), 1965, 'billions of dollars'),
              'FY1965': ((119.7, 122.4, -2.7), 1966, 'billions of dollars'),
              'FY1966': ((134.5, 137.8, -3.3), 1967, 'billions of dollars'),   # the federal columns of Table B-61
              'FY1967': ((153596, 155142, -1546), 1968, 'millions of dollars')},
        est={'FY1962': [((102.6, 111.1, -8.5), 1962)], 'FY1963': [((116.6, 114.8, 1.8), 1962), ((108.4, 116.8, -8.3), 1963)],
             'FY1964': [((114.4, 122.7, -8.3), 1964)], 'FY1965': [((119.7, 122.7, -2.9), 1964), ((117.4, 121.4, -4.0), 1965)],
             # FY1966 of 1966: the excess as printed (the difference is 6.8; the Report rounds from unrounded figures)
             'FY1966': [((123.5, 127.4, -3.9), 1965), ((128.2, 135.0, -6.9), 1966)],
             'FY1967': [((145.5, 145.0, 0.5), 1966), ((154.7, 160.9, -6.2), 1967)],
             # FY1968 of 1968: the excess as printed (the difference is 17,158)
             'FY1968': [((168.1, 172.4, -4.3), 1967), ((158823, 175981, -17157), 1968, 'millions of dollars')],
             'FY1969': [((181146, 188725, -7579), 1968, 'millions of dollars')]}),
    # The unified budget, adopted for fiscal 1969 on the President's Commission on Budget Concepts (1967): receipts and
    # outlays (expenditures and net lending) of federal and trust funds, interfund transactions excluded. Another
    # concept, so another series (STYLE 8). The Feb. 1968 Report's estimates for fiscal 1968 and 1969 ("preliminary
    # adjustments to new budget concepts", its note 1) in Table B-59, p. 279 (FRASER's scan, p. 285); the Jan. 1969
    # Report's actual for fiscal 1968 and estimates for 1969 and 1970 in Table B-60, p. 297 ("Unified budget",
    # 1954-70; the same figures in Table B-61, p. 299). The Jan. 1969 Report prints the administrative budget only to
    # 1939 and the consolidated cash statement only for 1940-53 (Table B-60): the old budgets end with fiscal 1967
    # actual, above. Its Table B-61 gives federal funds and trust funds as memoranda (fiscal 1968: federal funds
    # receipts 114,627, outlays 143,105), not the administrative budget, so not carried.
    'unified-budget': dict(
        name='Federal budget (unified)', freq='FY', fields=('receipts', 'outlays', 'balance'),
        then='Bureau of the Budget, unified budget receipts and outlays (expenditures and net lending), fiscal years ending June 30, millions of dollars',
        now_label='OMB, unified budget receipts, outlays, and surplus or deficit',
        now_unit='millions of dollars', now_fred=('FYFR', 'FYONET', 'FYFSD'),
        tables={1968: 'Table B-59, p. 279', 1969: 'Table B-60, p. 297'},
        unit='millions of dollars',
        rows={'FY1968': ((153676, 178862, -25187), 1969, 'millions of dollars')},   # the deficit as printed (the difference is 25,186)
        est={'FY1968': [((155830, 175635, -19805), 1968)],
             'FY1969': [((178108, 186062, -7954), 1968), ((186092, 183701, 2391), 1969)],
             'FY1970': [((198686, 195272, 3414), 1969)]}),
    'federal-national-accounts': dict(
        name='Federal receipts and expenditures, national income accounts', freq='Q', fields=('receipts', 'expenditures', 'balance'),
        then='Commerce and Bureau of the Budget, federal government receipts and expenditures in the national income accounts, seasonally adjusted annual rates, billions of dollars',
        now_label='BEA, federal government current receipts and current expenditures, SAAR (balance computed)',
        now_unit='billions of dollars, SAAR', now_fred=('FGRECPT', 'FGEXPND', None),
        tables={1962: 'Table B-59, p. 276', 1963: 'Table C-60, p. 242', 1964: 'Table C-60, p. 278',
                1965: 'Table B-62, p. 263', 1966: 'Table C-61, p. 281', 1967: 'Table B-63, p. 287',
                1968: 'Table B-62, p. 283', 1969: 'Table B-63, p. 301'},
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
              '1964Q3': ((114.0, 119.2, -5.2), 1965, 'billions of dollars, annual rate'),
              # Q4 1964 from the 1966 Report, which completes it (the 1965 Report: receipts n.a., expenditures 120.3).
              '1964Q4': ((116.8, 117.9, -1.1), 1966, 'billions of dollars, annual rate'),
              '1965Q1': ((123.7, 120.1, 3.6), 1966, 'billions of dollars, annual rate'), '1965Q2': ((124.4, 120.6, 3.8), 1966, 'billions of dollars, annual rate'),
              '1965Q3': ((122.7, 125.6, -2.9), 1966, 'billions of dollars, annual rate'),
              # Q4 1965 from the 1967 Report, which completes it (the 1966 Report: receipts n.a., expenditures 127.6).
              '1965Q4': ((126.9, 127.0, -0.2), 1967, 'billions of dollars, annual rate'),
              '1966Q1': ((136.0, 133.7, 2.3), 1967, 'billions of dollars, annual rate'), '1966Q2': ((141.0, 137.1, 3.8), 1967, 'billions of dollars, annual rate'),
              '1966Q3': ((145.3, 145.8, -0.5), 1967, 'billions of dollars, annual rate'),
              # Q4 1966 from the 1968 Report, which completes it (the 1967 Report: receipts n.a., expenditures 152.2, preliminary).
              '1966Q4': ((148.6, 151.9, -3.3), 1968, 'billions of dollars, annual rate'),
              '1967Q1': ((149.1, 160.9, -11.9), 1968, 'billions of dollars, annual rate'), '1967Q2': ((148.1, 162.8, -14.7), 1968, 'billions of dollars, annual rate'),
              '1967Q3': ((152.7, 165.9, -13.2), 1968, 'billions of dollars, annual rate'),
              # Q4 1967 from the 1969 Report, which completes it (the 1968 Report: receipts n.a., expenditures 167.5, preliminary).
              '1967Q4': ((156.4, 168.6, -12.2), 1969, 'billions of dollars, annual rate'),
              # The Jan. 1969 Report, Table B-63, p. 301 (FRASER's scan, p. 307). Balances as printed (Q1 1968: the
              # difference is 8.5; Q2: 10.1). Q4 1968 preliminary (marked p): receipts and the balance not printed (the
              # corporate profits tax accruals column blank). The calendar year 1968 (p): 176.9, 182.2, -5.3.
              '1968Q1': ((166.6, 175.1, -8.6), 1969, 'billions of dollars, annual rate'), '1968Q2': ((171.8, 181.9, -10.2), 1969, 'billions of dollars, annual rate'),
              '1968Q3': ((182.1, 184.9, -2.8), 1969, 'billions of dollars, annual rate'),
              '1968Q4': ((None, 186.8, None), 1969, 'billions of dollars, annual rate')}),
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
    # The Jan. 1966 Report prints no balance on regular transactions. It prints the two balances the Government put
    # its stress on from 1965: the liquidity basis (changes in liquid liabilities to all foreign holders and in
    # reserve assets, the U.S. gold tranche position in the IMF counted among them) and the official reserve
    # transactions basis (changes in liquid and nonliquid liabilities to foreign official holders and in reserve
    # assets). Two more concepts, so two more series (STYLE 8). Table C-78, p. 301; ch. 6, pp. 160-62. The year 1965
    # is the average of the first three quarters' annual rates (its note 10); Q3 1965 is preliminary (note 12).
    'balance-of-payments-liquidity': dict(
        name='Balance of payments, liquidity basis', freq='Q', fields=('balance',),
        then='Commerce, balance on the liquidity basis (changes in liquid liabilities to foreign official and other holders and in official reserve assets: gold, convertible currencies, the IMF gold tranche position), seasonally adjusted annual rates, millions of dollars',
        now_label='No longer published', now_unit=None, now_fred=None,
        tables={1966: 'Table C-78, p. 301', 1967: 'Table B-80, p. 307', 1968: 'Table B-83, p. 307', 1969: 'Table B-84, p. 325'},
        rows={'1964Q4': ((-5464,), 1966, 'millions of dollars, annual rate'), '1965Q1': ((-2836,), 1966, 'millions of dollars, annual rate'),
              '1965Q2': ((968,), 1966, 'millions of dollars, annual rate'), '1965Q3': ((-1940,), 1966, 'millions of dollars, annual rate'),
              # The Jan. 1967 Report, Table B-80: Q4 1965 and 1966; Q3 1966 preliminary (marked p); the year 1966 the
              # average of the first three quarters' annual rates (its note 11). The year 1965 stays as the 1966 Report
              # printed it (the 1967 Report: -1,337 for the full year).
              '1965Q4': ((-1328,), 1967, 'millions of dollars, annual rate'), '1966Q1': ((-2204,), 1967, 'millions of dollars, annual rate'),
              '1966Q2': ((-564,), 1967, 'millions of dollars, annual rate'), '1966Q3': ((-872,), 1967, 'millions of dollars, annual rate'),
              '1964': ((-2798,), 1966, 'millions of dollars, year'),
              '1965': ((-1269,), 1966, 'millions of dollars, annual rate, first three quarters'),
              '1966': ((-1213,), 1967, 'millions of dollars, annual rate, first three quarters'),
              # The Feb. 1968 Report, Table B-83: Q4 1966 and 1967; Q3 1967 preliminary (marked p); the year 1967 the
              # average of the first three quarters' annual rates (its note 10). Q3 1966 and the year 1966 stay as the 1967
              # Report printed them (the 1968 Report: -660 for Q3 1966, -1,357 for the full year).
              '1966Q4': ((-1676,), 1968, 'millions of dollars, annual rate'), '1967Q1': ((-2116,), 1968, 'millions of dollars, annual rate'),
              '1967Q2': ((-2188,), 1968, 'millions of dollars, annual rate'), '1967Q3': ((-2544,), 1968, 'millions of dollars, annual rate'),
              '1967': ((-2283,), 1968, 'millions of dollars, annual rate, first three quarters'),
              # The Jan. 1969 Report, Table B-84, p. 325 (FRASER's scan, p. 331): Q4 1967 and 1968; Q3 1968 preliminary
              # (marked p); the year 1968 the average of the first three quarters' annual rates (its note 10). Q3 1967 and
              # the year 1967 stay as the 1968 Report printed them (the 1969 Report: -3,208 for Q3 1967, -3,571 for the
              # full year).
              '1967Q4': ((-6968,), 1969, 'millions of dollars, annual rate'), '1968Q1': ((-2748,), 1969, 'millions of dollars, annual rate'),
              '1968Q2': ((-656,), 1969, 'millions of dollars, annual rate'), '1968Q3': ((164,), 1969, 'millions of dollars, annual rate'),
              '1968': ((-1080,), 1969, 'millions of dollars, annual rate, first three quarters')}),
    'balance-of-payments-official': dict(
        name='Balance of payments, official reserve transactions basis', freq='Q', fields=('balance',),
        then='Commerce, balance on the official reserve transactions basis (changes in liquid and nonliquid liabilities to foreign official holders and in official reserve assets: gold, convertible currencies, the IMF gold tranche position), seasonally adjusted annual rates, millions of dollars',
        now_label='No longer published', now_unit=None, now_fred=None,
        tables={1966: 'Table C-78, p. 301', 1967: 'Table B-80, p. 307', 1968: 'Table B-83, p. 307', 1969: 'Table B-84, p. 325'},
        rows={'1964Q4': ((-3132,), 1966, 'millions of dollars, annual rate'), '1965Q1': ((-2568,), 1966, 'millions of dollars, annual rate'),
              '1965Q2': ((820,), 1966, 'millions of dollars, annual rate'), '1965Q3': ((1040,), 1966, 'millions of dollars, annual rate'),
              # As the liquidity balance above (the 1967 Report: -1,305 for the full year 1965).
              '1965Q4': ((-4632,), 1967, 'millions of dollars, annual rate'), '1966Q1': ((-964,), 1967, 'millions of dollars, annual rate'),
              '1966Q2': ((-856,), 1967, 'millions of dollars, annual rate'), '1966Q3': ((3784,), 1967, 'millions of dollars, annual rate'),
              '1964': ((-1224,), 1966, 'millions of dollars, year'),
              '1965': ((-236,), 1966, 'millions of dollars, annual rate, first three quarters'),
              '1966': ((655,), 1967, 'millions of dollars, annual rate, first three quarters'),
              # As the liquidity balance above (the 1968 Report: 3,444 for Q3 1966, 225 for the full year 1966).
              '1966Q4': ((-72,), 1968, 'millions of dollars, annual rate'), '1967Q1': ((-7260,), 1968, 'millions of dollars, annual rate'),
              '1967Q2': ((-3312,), 1968, 'millions of dollars, annual rate'), '1967Q3': ((1880,), 1968, 'millions of dollars, annual rate'),
              '1967': ((-2897,), 1968, 'millions of dollars, annual rate, first three quarters'),
              # As the liquidity balance above (the 1969 Report: 988 for Q3 1967, -3,405 for the full year 1967).
              '1967Q4': ((-4328,), 1969, 'millions of dollars, annual rate'), '1968Q1': ((-2224,), 1969, 'millions of dollars, annual rate'),
              '1968Q2': ((6112,), 1969, 'millions of dollars, annual rate'), '1968Q3': ((1776,), 1969, 'millions of dollars, annual rate'),
              '1968': ((1888,), 1969, 'millions of dollars, annual rate, first three quarters')}),
    'gap-cea': dict(
        name='Output gap, CEA (contemporary)', freq='Q',
        then='Council of Economic Advisers: potential GNP (a 3½ percent trend through actual GNP in mid-1955; from Jan. 1965, 3¾ percent after 1962; at 4 percent unemployment) less actual GNP',
        now_label=None, now_unit=None, now_fred=None,
        tables={1962: 'ch. 1, "Full Production," p. 49', 1963: "President's message, p. xiii",
                1964: 'ch. 1, "Unemployment and Unused Potential Output," p. 37',
                1965: 'ch. 1, "Problems Unsolved," p. 39',
                1966: 'ch. 1, "Balance of Output and Potential," p. 40'},
        # A figure from another page of the same Report than its table entry.
        src={'1964': 'ch. 2, "The Gap Between Actual and Potential GNP," p. 83'},
        rows={'1961Q1': (51, 1962, 'billions of 1961 dollars, annual rate'),
              '1961Q4': (28, 1962, 'billions of 1961 dollars, annual rate'),
              '1961': (40, 1962, 'billions of 1961 dollars, year'),
              '1962Q4': ('30–40', 1963, 'billions of dollars, annual rate'),
              '1963Q4': (30, 1964, 'billions of 1963 dollars, annual rate'),
              '1964Q4': ('25–30', 1965, 'billions of dollars, annual rate'),
              '1964': (27, 1965, 'billions of 1964 dollars, year'),
              # "It shrank dramatically in 1965, reaching $10 billion, in the final quarter"; the paragraph's figures
              # in 1958 prices, as Chart 3 (after the Commerce benchmark revision of Aug. 1965).
              '1965Q4': (10, 1966, 'billions of 1958 dollars, annual rate')}),
        # The Jan. 1967 Report states no gap for 1966: "The economy caught up with its economic potential in 1966"
        # (ch. 1, p. 44); Chart 1 (p. 43) draws the gap as a percent of potential near zero through 1966 (potential: 4
        # percent a year from Q4 1965) and prints no figure. Its only dollar figure is a revision of Q1 1961 ($57 billion
        # in 1966 prices, p. 42). So no 1966 row: a value read off the chart would be ours, not the Report's.
        # The Feb. 1968 Report states none for 1967 either: the gap "finally closed in the last half of 1965. Since then,
        # actual GNP has fluctuated in a relatively narrow range around its growing potential—exceeding it somewhat in the
        # boom of 1966 and falling a little short during 1967" (ch. 2, p. 60). Chart 4 (p. 61) draws the gap as a percent
        # of potential (potential: 4 percent a year from Q4 1965 to Q4 1967) and prints no figure; Q1 1961 is revised
        # again, to $50 billion in 1958 prices (p. 60). So no 1967 row.
        # The Jan. 1969 Report states none for 1968: from Q1 1961 to the end of 1965 actual output was below potential,
        # "catching up and finally closing the gap. Since then, actual output has exceeded the calculated potential most
        # of the time, as the unemployment rate has been below 4 percent" (ch. 2, "Potential Output," p. 64). Chart 5
        # (p. 65) draws the gap as a percent of potential, at or below zero (output above potential) from 1966 (potential: 3½ percent through Q4
        # 1962, 3¾ to Q4 1965, 4 to Q4 1968), and prints no figure; Q1 1961 is revised to about $60 billion in 1968
        # prices (p. 64). So no 1968 row.
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
        ('balance-of-payments-regular', '1964'): 'Q1–Q3, annual rate',
        ('balance-of-payments-liquidity', '1965'): 'Q1–Q3, annual rate',
        ('balance-of-payments-official', '1965'): 'Q1–Q3, annual rate',
        ('balance-of-payments-liquidity', '1966'): 'Q1–Q3, annual rate',
        ('balance-of-payments-official', '1966'): 'Q1–Q3, annual rate',
        ('balance-of-payments-liquidity', '1967'): 'Q1–Q3, annual rate',
        ('balance-of-payments-official', '1967'): 'Q1–Q3, annual rate',
        ('balance-of-payments-liquidity', '1968'): 'Q1–Q3, annual rate',
        ('balance-of-payments-official', '1968'): 'Q1–Q3, annual rate'}


SCALE = {('billions of dollars', 'millions of dollars'): 1000, ('millions of dollars', 'billions of dollars'): 0.001}


def est_entry(m, e, unit):
    """One estimate (values, Report[, the unit printed]) for a row in 'unit'. The renderer reads an estimate in its
    row's unit, so one printed in another is put into it, its printed figures kept beside ('printed')."""
    vals, erp = e[0], e[1]
    eu = e[2] if len(e) > 2 else m.get('unit')
    out = {'value': dict(zip(m['fields'], vals))}
    if unit and eu and eu != unit:
        k = SCALE[(eu, unit)]
        out['value'] = {f: (None if v is None else (lambda x: int(x) if x == int(x) else x)(round(v * k, 6)))
                        for f, v in out['value'].items()}
        out['printed'] = '; '.join(f'{f} {v}' for f, v in zip(m['fields'], vals)) + f' ({eu})'
    out['as_of'] = ERP[erp][0]
    out['source'] = f'{ERP[erp][1]}, {m["tables"][erp]}'
    return out


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
                row.setdefault('est', []).append(est_entry(m, e, unit if v is not None else None))
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
                # no figure yet: the row in the unit of its latest estimate
                unit = (ests[-1][2] if len(ests[-1]) > 2 else m.get('unit'))
                row = {'p': p, 'est': [est_entry(m, e, unit) for e in ests]}
                if unit:
                    row['unit'] = unit
                row['now'] = now_for(p)
                rows.append(row)
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
    for y in ('1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968'):
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
# releases, on FRASER). The two 1960 changes set the rate standing in Dec. 1960. Each 1960 release is "for release at
# 4:00 p.m." the day before the change took effect (frsbog_pr_19600609_01.pdf, frsbog_pr_19600811.pdf; FRASER items
# 697022, 697031); the Bulletin's notices say only "recently approved". No change in 1966: 4½ from Dec. 6, 1965, to
# Apr. 7, 1967. The 1967 releases: frsbog_pr_19670406_01.pdf (FRASER item 697516), "effective Friday, April 7, 1967"
# (Atlanta Apr. 10, St. Louis Apr. 14: Bulletin, Apr. 1967, p. 590); frsbog_pr_19671119.pdf (item 697571), Sunday, Nov.
# 19, "in the light of the action of the British Government to change the parity of the pound", "effective Monday,
# November 20, 1967" (Philadelphia Nov. 21, St. Louis Nov. 27: Bulletin, Nov. 1967, p. 1921; Dec. 1967, p. 2083).
# 1968: New York was not among the nine Banks raised to 5 percent on Mar. 15 (frsbog_pr_19680314_01.pdf, item 697603:
# Boston, Cleveland, Richmond, Atlanta, Chicago, St. Louis, Minneapolis, Kansas City, Dallas; San
# Francisco Mar. 15, Philadelphia Mar. 18); its rise came a week later, frsbog_pr_19680321_01.pdf (item 697609), "effective
# tomorrow" (Bulletin, Apr. 1968, p. 391: "As of March 22 the rate in effect was 5 per cent at all Federal Reserve
# Banks"; table, p. A-9). 5½ from Apr. 19: frsbog_pr_19680418_02.pdf (item 697619), New York, Philadelphia and
# Minneapolis "effective tomorrow (April 19, 1968)" (the others Apr. 19-26: Bulletin, Apr. 1968, p. 391; May 1968,
# p. A-9). 5¼ from Aug. 30: Minneapolis led, Aug. 16 (frsbog_pr_19680815_02.pdf), Richmond Aug. 19; New York with
# Atlanta, St. Louis and San Francisco, frsbog_pr_19680829.pdf (item 697672), "effective Friday, August 30, 1968"
# (Bulletin, Sept. 1968, p. 782, and p. A-9). 5½ from Dec. 18: frsbog_pr_19681217.pdf (item 697709), nine Banks with New
# York, "effective Wednesday, December 18" (St. Louis, Kansas City, San Francisco Dec. 20: Bulletin, Dec. 1968, p. 1039;
# Jan. 1969, p. 86, and p. A-9). Each release read off FRASER's scan, the image checked against the text layer.
FRASER = 'https://fraser.stlouisfed.org/title/'
DISCOUNT = [
    ('1960-06-10', '1960-06-09', 3.5, 'Board of Governors, press release, June 9, 1960; Federal Reserve Bulletin, July 1960, p. 756 (from 4 percent)'),
    ('1960-08-12', '1960-08-11', 3.0, 'Board of Governors, press release, Aug. 11, 1960; Federal Reserve Bulletin, Sept. 1960, p. 1014'),
    ('1963-07-17', '1963-07-16', 3.5, 'Board of Governors, press release, July 16, 1963; Federal Reserve Bulletin, Sept. 1963, p. 1264'),
    ('1964-11-24', '1964-11-23', 4.0, 'Board of Governors, press release, Nov. 23, 1964; Federal Reserve Bulletin, Dec. 1964, pp. 1530–31, and Feb. 1965, p. 267'),
    # announced Sunday, Dec. 5, "for release in morning papers of Monday, December 6" (the release of Dec. 3, 1965 is
    # the Board's guidelines for foreign lending in 1966)
    ('1965-12-06', '1965-12-05', 4.5, 'Board of Governors, press release, Dec. 5, 1965; Federal Reserve Bulletin, Dec. 1965, pp. 1667–68, and Jan. 1966, p. 53'),
    ('1967-04-07', '1967-04-06', 4.0, 'Board of Governors, press release, Apr. 6, 1967; Federal Reserve Bulletin, Apr. 1967, p. 590, and May 1967, p. 795'),
    ('1967-11-20', '1967-11-19', 4.5, 'Board of Governors, press release, Nov. 19, 1967; Federal Reserve Bulletin, Nov. 1967, p. 1921, and Dec. 1967, p. 2083'),
    ('1968-03-22', '1968-03-21', 5.0, 'Board of Governors, press release, Mar. 21, 1968; Federal Reserve Bulletin, Apr. 1968, p. 391 and p. A-9'),
    ('1968-04-19', '1968-04-18', 5.5, 'Board of Governors, press release, Apr. 18, 1968; Federal Reserve Bulletin, Apr. 1968, p. 391, and May 1968, p. A-9'),
    ('1968-08-30', '1968-08-29', 5.25, 'Board of Governors, press release, Aug. 29, 1968; Federal Reserve Bulletin, Sept. 1968, p. 782 and p. A-9'),
    ('1968-12-18', '1968-12-17', 5.5, 'Board of Governors, press release, Dec. 17, 1968; Federal Reserve Bulletin, Dec. 1968, p. 1039, and Jan. 1969, p. A-9'),
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
        cur = current_from(sid, '1959-12-01')
        rows = []
        for p in RATE_MONTHS:
            d = f'{p}-01'
            row = {'p': p, 'now': cur.get(d)}
            c = None if cur.get(d) is None or cur.get(prior(d, 'M')) is None else round(cur[d] - cur[prior(d, 'M')], 2)
            if c is not None and not (key in ADMIN and c == 0):
                row['chg_now'] = c
            rows.append(row)
        write(key, meta(key, sid, name, label), rows)
    rows = []
    for p in RATE_MONTHS:
        lo, hi = f'{p}-01', month_end(p)
        standing = [x for x in DISCOUNT if x[0] <= hi]
        if not standing:                   # before the first change kept here (June 1960)
            continue
        eff, ann, v, src = standing[-1]
        row = {'p': p, 'first': v}
        if lo <= eff:                      # a change this month
            if len(standing) > 1:
                row['chg'] = round(v - standing[-2][2], 2)
            row['released'] = ann or eff
            row['note'] = f'effective {label_day(eff)}' + ('' if ann else '; the announcement\'s date not kept here (Check)')
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


# ---------------------------------------------------------------- DEBT: federal debt, interest, and the primary balance
# The public debt was reported monthly: the Daily Treasury Statement for the month's last day, then the Treasury
# Bulletin, whose "Summary of Federal Fiscal Operations" (p. 1 of each issue) prints the public debt at the end of each
# month and the month's net increase or decrease (its source note: "on basis of telegraphic reports", the daily
# statement). Read off FRASER's scans of every issue, Feb. 1961 to Jan. 1969, by eye from the page images (the text
# layers are unreliable): each month from the first issue that carries it. The issues of Jan.-Oct. 1961 carry the
# month two before; Nov. 1961 adds Sept. and Oct.; from then on, the month before. The Feb. 1968 issue drops the summary
# table (its announcement, p. 1: "the tables showing administrative budget and trust fund receipts and expenditures
# have been discontinued", on the unified budget): from it, Debt Outstanding, Table 1, "Summary of Public Debt and
# Guaranteed Agency Securities" (source: Daily Treasury statement), its public debt column, which prints no change:
# the change is the difference of the issue's own last two months. The June figures of 1961-67 are marked p
# (preliminary). Each month's level plus the next month's printed change gives the next level, within the $1 million
# of rounding, through the whole run (checked when this was written).
# Columns: issue, month, printed net increase in the public debt ('d': none printed), public debt, both millions of
# dollars; then 'prior N' (the issue's figure for the month before, where no change is printed) or 'p'.
TB = 'https://fraser.stlouisfed.org/title/treasury-bulletin-407/'
TB_MON = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
          'november', 'december']
# FRASER's item numbers: one an issue from 6769 (Jan. 1961), but Oct. 1968 (6863) and Nov. 1968 (6862).
TB_ITEM = {f'{y}-{m:02d}': 6769 + 12 * (y - 1961) + m - 1 for y in range(1961, 1970) for m in range(1, 13)}
TB_ITEM.update({'1968-10': 6863, '1968-11': 6862})
# The page of Debt Outstanding, Table 1, in the issues of Feb. 1968 to Jan. 1969 (before: the summary, p. 1).
TB_PAGE = {'1968-02': 22, '1968-03': 20, '1968-04': 17, '1968-05': 24, '1968-06': 18, '1968-07': 16, '1968-08': 23,
           '1968-09': 18, '1968-10': 16, '1968-11': 23, '1968-12': 19, '1969-01': 18}
PUBLIC_DEBT = """
    1961_02 1960-12 -197 290217
    1961_03 1961-01 -181 290036
    1961_04 1961-02 508 290544
    1961_05 1961-03 -3072 287471
    1961_06 1961-04 516 287987
    1961_07 1961-05 2158 290146
    1961_08 1961-06 -1175 288971 p
    1961_09 1961-07 3433 292404
    1961_10 1961-08 1310 293714
    1961_11 1961-09 35 293750
    1961_11 1961-10 1911 295660
    1961_12 1961-11 1350 297011
    1962_01 1961-12 -842 296169
    1962_02 1962-01 345 296513
    1962_03 1962-02 470 296983
    1962_04 1962-03 -896 296088
    1962_05 1962-04 864 296952
    1962_06 1962-05 2222 299174
    1962_07 1962-06 -973 298201 p
    1962_08 1962-07 -325 297876
    1962_09 1962-08 3966 301842
    1962_10 1962-09 -2344 299498
    1962_11 1962-10 2569 302067
    1962_12 1962-11 3323 305390
    1963_01 1962-12 -1920 303470
    1963_02 1963-01 -53 303417
    1963_03 1963-02 1221 304638
    1963_04 1963-03 -1645 302993
    1963_05 1963-04 173 303166
    1963_06 1963-05 2038 305204
    1963_07 1963-06 656 305860 p
    1963_08 1963-07 -1025 304835
    1963_09 1963-08 1700 306535
    1963_10 1963-09 100 306635
    1963_11 1963-10 -193 306442
    1963_12 1963-11 1773 308215
    1964_01 1963-12 1132 309347
    1964_02 1964-01 -770 308577
    1964_03 1964-02 1780 310357
    1964_04 1964-03 -767 309590
    1964_05 1964-04 -1989 307601
    1964_06 1964-05 3931 311532
    1964_07 1964-06 181 311713 p
    1964_08 1964-07 -530 311183
    1964_09 1964-08 2906 314089
    1964_10 1964-09 1520 315610
    1964_11 1964-10 26 315635
    1964_12 1964-11 2851 318486
    1965_01 1964-12 -546 317940
    1965_02 1965-01 42 317983
    1965_03 1965-02 1900 319883
    1965_04 1965-03 -2186 317697
    1965_05 1965-04 -1140 316557
    1965_06 1965-05 2661 319218
    1965_07 1965-06 -1944 317274 p
    1965_08 1965-07 -692 316582
    1965_09 1965-08 1658 318240
    1965_10 1965-09 -1493 316748
    1965_11 1965-10 2154 318901
    1965_12 1965-11 2810 321711
    1966_01 1965-12 -807 320904
    1966_02 1966-01 1099 322003
    1966_03 1966-02 1308 323311
    1966_04 1966-03 -2312 320999
    1966_05 1966-04 -1416 319583
    1966_06 1966-05 2777 322359
    1966_07 1966-06 -2452 319907 p
    1966_08 1966-07 -627 319280
    1966_09 1966-08 5141 324420
    1966_10 1966-09 328 324748
    1966_11 1966-10 2140 326888
    1966_12 1966-11 2523 329411
    1967_01 1966-12 -92 329319
    1967_02 1967-01 -450 328869
    1967_03 1967-02 756 329625
    1967_04 1967-03 1321 330947
    1967_05 1967-04 -3145 327801
    1967_06 1967-05 3087 330888
    1967_07 1967-06 -4667 326221 p
    1967_08 1967-07 4416 330637
    1967_09 1967-08 5213 335850
    1967_10 1967-09 46 335896
    1967_11 1967-10 4606 340502
    1967_12 1967-11 4588 345090
    1968_01 1967-12 -427 344663
    1968_02 1968-01 d 346259 prior 344663
    1968_03 1968-02 d 351556 prior 346259
    1968_04 1968-03 d 349473 prior 351556
    1968_05 1968-04 d 346984 prior 349473
    1968_06 1968-05 d 352294 prior 346984
    1968_07 1968-06 d 347578 prior 352294
    1968_08 1968-07 d 351078 prior 347578
    1968_09 1968-08 d 354356 prior 351078
    1968_10 1968-09 d 354743 prior 354356
    1968_11 1968-10 d 357194 prior 354743
    1968_12 1968-11 d 356863 prior 357194
    1969_01 1968-12 d 358029 prior 356863
"""


def tb_cite(issue):
    y, m = int(issue[:4]), int(issue[5:7])
    mon = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'][m - 1]
    if issue in TB_PAGE:
        where = f'Debt Outstanding, Table 1, p. {TB_PAGE[issue]}'
    else:
        where = 'Summary of Federal Fiscal Operations, p. 1'
    return f'Treasury Bulletin, {mon} {y}, {where}', f'{TB}{TB_MON[m - 1]}-{y}-{TB_ITEM[issue]}'


# The Economic Report of the next January prints, in one Report, GNP by quarter (seasonally adjusted annual rates,
# Table 1), the federal sector of the national income accounts by quarter (its net interest paid and its surplus or
# deficit; the table federal-national-accounts reads), and the gross public debt at the end of each month of the last
# two years (U.S. Government debt, by kind of obligation). So the ratios are computed from one Report's own figures:
# the debt at the quarter's end over the quarter's GNP at an annual rate; net interest paid over GNP. Each Report also
# gives the quarter before the first it is used for, so the change is taken within the Report. Read by eye from
# FRASER's scans (ERP_<year>.pdf: the printed page plus 8 in 1962 and 1964, plus 30 in 1963, plus 6 in 1965-69),
# checked against the text layer; the surpluses agree with federal-national-accounts.
# Debt: "Gross public debt and guaranteed issues" through the Report of Feb. 1968; the Jan. 1969 Report's Table B-64,
# "Public debt securities by kind of obligation", prints the public debt alone (guaranteed issues, some $0.5bn, out).
ERP_DEBT = {
    1962: ('Table B-52, p. 269', {'1960-09': 288.6, '1960-12': 290.4, '1961-03': 287.7, '1961-06': 289.2, '1961-09': 294.0, '1961-12': 296.5}),
    1963: ('Table C-53, p. 235', {'1961-12': 296.5, '1962-03': 296.5, '1962-06': 298.6, '1962-09': 300.0, '1962-12': 304.0}),
    1964: ('Table C-53, p. 271', {'1962-12': 304.0, '1963-03': 303.5, '1963-06': 306.5, '1963-09': 307.3, '1963-12': 310.1}),
    1965: ('Table B-55, p. 255', {'1963-12': 310.1, '1964-03': 310.4, '1964-06': 312.5, '1964-09': 316.5, '1964-12': 318.7}),
    1966: ('Table C-54, p. 273', {'1964-12': 318.7, '1965-03': 318.4, '1965-06': 317.9, '1965-09': 317.3, '1965-12': 321.4}),
    1967: ('Table B-56, p. 279', {'1965-12': 321.4, '1966-03': 321.5, '1966-06': 320.4, '1966-09': 325.2, '1966-12': 329.8}),
    1968: ('Table B-64, p. 285', {'1966-12': 329.8, '1967-03': 331.5, '1967-06': 326.7, '1967-09': 336.4, '1967-12': 345.2}),
    1969: ('Table B-64, p. 302', {'1967-12': 344.7, '1968-03': 349.5, '1968-06': 347.6, '1968-09': 354.7, '1968-12': 358.0}),
}
# GNP, total, seasonally adjusted annual rates, billions; Q4 preliminary in each.
ERP_GNP = {
    1962: ('Table B-1, p. 207', {'1960Q3': 505.1, '1960Q4': 504.5, '1961Q1': 500.8, '1961Q2': 516.1, '1961Q3': 525.8, '1961Q4': 542.0}),
    1963: ('Table C-1, p. 171', {'1961Q4': 538.6, '1962Q1': 545.0, '1962Q2': 552.0, '1962Q3': 555.3, '1962Q4': 562.0}),
    1964: ('Table C-1, p. 207', {'1962Q4': 565.2, '1963Q1': 571.8, '1963Q2': 579.6, '1963Q3': 588.7, '1963Q4': 600.0}),
    1965: ('Table B-1, p. 189', {'1963Q4': 599.0, '1964Q1': 608.8, '1964Q2': 618.6, '1964Q3': 628.4, '1964Q4': 633.5}),
    1966: ('Table C-1, p. 209', {'1964Q4': 641.1, '1965Q1': 657.6, '1965Q2': 668.8, '1965Q3': 681.5, '1965Q4': 694.6}),
    1967: ('Table B-1, p. 213', {'1965Q4': 704.4, '1966Q1': 721.2, '1966Q2': 732.3, '1966Q3': 745.3, '1966Q4': 759.1}),
    1968: ('Table B-1, p. 209', {'1966Q4': 762.1, '1967Q1': 766.3, '1967Q2': 775.1, '1967Q3': 791.2, '1967Q4': 807.6}),
    1969: ('Table B-1, p. 227', {'1967Q4': 811.0, '1968Q1': 831.2, '1968Q2': 852.9, '1968Q3': 871.0, '1968Q4': 887.8}),
}
# Federal sector, national income accounts: (net interest paid, surplus or deficit), billions, SAAR; the surplus not
# printed for a preliminary fourth quarter (None). The tables of federal-national-accounts (MANUAL above).
ERP_NIPA = {
    1962: {'1960Q3': (7.1, 1.4), '1960Q4': (7.0, 0.4), '1961Q1': (6.8, -5.5), '1961Q2': (6.6, -4.3), '1961Q3': (6.4, -3.1), '1961Q4': (6.5, None)},
    1963: {'1961Q3': (6.5, -3.3), '1961Q4': (6.4, -1.3), '1962Q1': (6.6, -2.4), '1962Q2': (6.7, -0.7), '1962Q3': (6.8, -0.9), '1962Q4': (6.9, None)},
    1964: {'1962Q4': (7.3, -5.3), '1963Q1': (7.4, -4.6), '1963Q2': (7.5, -3.0), '1963Q3': (7.6, -1.8), '1963Q4': (7.6, None)},
    1965: {'1963Q3': (7.8, -0.7), '1963Q4': (7.9, 0.6), '1964Q1': (8.3, -2.4), '1964Q2': (8.4, -7.8), '1964Q3': (8.4, -5.2), '1964Q4': (8.4, None)},
    1966: {'1964Q3': (8.5, -3.6), '1964Q4': (8.4, -1.1), '1965Q1': (8.6, 3.6), '1965Q2': (8.7, 3.8), '1965Q3': (8.8, -2.9), '1965Q4': (8.9, None)},
    1967: {'1965Q3': (8.8, -2.5), '1965Q4': (8.8, -0.2), '1966Q1': (9.3, 2.3), '1966Q2': (9.5, 3.8), '1966Q3': (9.7, -0.5), '1966Q4': (10.0, None)},
    1968: {'1966Q3': (9.6, -0.7), '1966Q4': (10.0, -3.3), '1967Q1': (10.4, -11.9), '1967Q2': (10.4, -14.7), '1967Q3': (10.5, -13.2), '1967Q4': (10.7, None)},
    1969: {'1967Q3': (10.2, -12.9), '1967Q4': (10.7, -12.2), '1968Q1': (11.3, -8.6), '1968Q2': (11.8, -10.2), '1968Q3': (12.1, -2.8), '1968Q4': (12.2, None)},
}
# OMB, Historical Tables, Table 7.1, "Federal Debt at the End of Year: 1940-2025" (the Budget for fiscal 2027,
# hist07z1_fy2027.xlsx, read Oct. 20, 2026): gross federal debt and debt held by the public, percent of GDP for the
# fiscal year. Retrospective: no contemporary figure.
OMB71 = 'https://www.whitehouse.gov/wp-content/uploads/2026/04/hist07z1_fy2027.xlsx'
OMB_DEBT = {'FY1960': (54.4, 44.3), 'FY1961': (53.5, 43.6), 'FY1962': (51.7, 42.3), 'FY1963': (50.2, 41.1),
            'FY1964': (47.8, 38.8), 'FY1965': (45.4, 36.8), 'FY1966': (42.1, 33.8), 'FY1967': (40.7, 31.9),
            'FY1968': (41.1, 32.3)}


def qend(q):
    y, n = q.split('Q')
    return f'{y}-{3 * int(n):02d}'


def prevq(q):
    y, n = int(q[:4]), int(q[-1])
    return f'{y - 1}Q4' if n == 1 else f'{y}Q{n - 1}'


def qdate(q):
    y, n = q.split('Q')
    return f'{y}-{3 * (int(n) - 1) + 1:02d}-01'


def report_quarters(erp):
    """The quarters a Report is the source for (the ratios): the year before's four; the 1962 Report also Q4 1960."""
    qs = [f'{erp - 1}Q{n}' for n in range(1, 5)]
    return (['1960Q4'] if erp == 1962 else []) + qs


def debt():
    # public debt, monthly
    rows, prev_now = [], None
    gfd = current_from('GFDEBTN', '1959-01-01')
    for line in PUBLIC_DEBT.strip().split('\n'):
        f = line.split()
        issue, p = f[0].replace('_', '-'), f[1]
        level = int(f[3])
        chg = level - int(f[5]) if f[2] == 'd' else int(f[2])
        src, url = tb_cite(issue)
        row = {'p': p, 'first': level, 'released': issue, 'source': src, 'url': url, 'chg': chg,
               'unit': 'millions of dollars'}
        if 'p' in f[4:]:
            row['note'] = 'preliminary'
        q = f'{p[:4]}-{int(p[5:7]) - 2:02d}-01' if p[5:7] in ('03', '06', '09', '12') else None
        row['now'] = gfd.get(q) if q else None
        rows.append(row)
    write('public-debt', {'id': 'public-debt', 'name': 'Public debt', 'freq': 'M', 'manual': True, 'change': 'diff',
                          'then': {'label': 'Treasury, public debt outstanding at the end of the month (Daily Treasury Statement), as the Treasury Bulletin first tabled it, millions of dollars',
                                   'source': 'Treasury Bulletin'},
                          'now': {'label': 'Treasury, Federal Debt: Total Public Debt, end of quarter (from 1966)', 'unit': 'millions of dollars',
                                  'source': 'FRED GFDEBTN', 'url': FRED + 'GFDEBTN'}}, rows)

    # ratios to GNP, quarterly, each from one Report
    gdp = current_from('GDP', '1959-01-01')
    ratio = current_from('GFDEGDQ188S', '1959-01-01')
    ipay = current_from('A091RC1Q027SBEA', '1959-01-01')
    irec = current_from('B094RC1Q027SBEA', '1959-01-01')
    nlb = current_from('AD02RC1Q027SBEA', '1959-01-01')
    drows, irows = [], []
    for erp in sorted(ERP_DEBT):
        dt, debt_ = ERP_DEBT[erp]
        gt, gnp = ERP_GNP[erp]
        nt = MANUAL['federal-national-accounts']['tables'][erp]
        for q in report_quarters(erp):
            pq = prevq(q)
            r = 100 * debt_[qend(q)] / gnp[q]
            rp = 100 * debt_[qend(pq)] / gnp[pq]
            mon = ['Mar.', 'June', 'Sept.', 'Dec.'][int(q[-1]) - 1]
            row = {'p': q, 'first': round(r, 1), 'released': ERP[erp][0],
                   'source': f'{ERP[erp][1]}, {dt} (debt, end of {mon} {q[:4]}: {debt_[qend(q)]}) and {gt} (GNP: {gnp[q]})',
                   'chg': round(r - rp, 1), 'unit': 'percent of GNP'}
            n = ratio.get(qdate(q))
            row['now'] = None if n is None else round(n, 1)
            pn = ratio.get(qdate(pq))
            if n is not None and pn is not None:
                row['chg_now'] = round(n - pn, 1)
            drows.append(row)
            i, ip = ERP_NIPA[erp][q][0], ERP_NIPA[erp][pq][0]
            s, sp = 100 * i / gnp[q], 100 * ip / gnp[pq]
            row = {'p': q, 'first': round(s, 2), 'released': ERP[erp][0],
                   'source': f'{ERP[erp][1]}, {nt} (net interest paid: {i}) and {gt} (GNP: {gnp[q]})',
                   'chg': round(s - sp, 2), 'unit': 'percent of GNP'}
            def net_now(qq):
                a, b, g = ipay.get(qdate(qq)), irec.get(qdate(qq)), gdp.get(qdate(qq))
                return None if None in (a, b, g) else 100 * (a - b) / g
            n, pn = net_now(q), net_now(pq)
            row['now'] = None if n is None else round(n, 2)
            if n is not None and pn is not None:
                row['chg_now'] = round(n - pn, 2)
            irows.append(row)
    write('debt-gnp', {'id': 'debt-gnp', 'name': 'Public debt to GNP', 'freq': 'Q', 'manual': True, 'change': 'pts',
                       'then': {'label': 'Gross public debt (and guaranteed issues, through 1967) at the quarter\'s end over GNP at a seasonally adjusted annual rate, both from the next January\'s Economic Report', 'source': 'Economic Report of the President, statistical tables'},
                       'now': {'label': 'Federal Debt: Total Public Debt as Percent of GDP (from 1966)', 'unit': 'percent of GDP',
                               'source': 'FRED GFDEGDQ188S', 'url': FRED + 'GFDEGDQ188S'}}, drows)
    write('interest-gnp', {'id': 'interest-gnp', 'name': 'Federal net interest to GNP', 'freq': 'Q', 'manual': True, 'change': 'pts',
                           'then': {'label': 'Net interest paid, federal sector of the national income accounts, over GNP, both seasonally adjusted annual rates from the next January\'s Economic Report', 'source': 'Economic Report of the President, statistical tables'},
                           'now': {'label': 'BEA: federal interest payments less interest receipts over GDP', 'unit': 'percent of GDP',
                                   'source': 'FRED A091RC1Q027SBEA, B094RC1Q027SBEA, GDP', 'url': FRED + 'A091RC1Q027SBEA'}}, irows)

    # the primary balance: the surplus or deficit with net interest added back, quarterly, in the Report that
    # federal-national-accounts takes each quarter from
    prows = []
    for q, (v, erp, unit) in MANUAL['federal-national-accounts']['rows'].items():
        i, bal = ERP_NIPA[erp][q]
        pi, pbal = ERP_NIPA[erp][prevq(q)]
        prim = None if bal is None else round(bal + i, 1)
        row = {'p': q, 'first': {'balance': bal, 'interest': i, 'primary': prim}, 'released': ERP[erp][0],
               'source': f'{ERP[erp][1]}, {MANUAL["federal-national-accounts"]["tables"][erp]}',
               'unit': 'billions of dollars, annual rate'}
        if prim is not None and pbal is not None:
            row['chg'] = round(prim - (pbal + pi), 1)
        def now_of(qq):
            a, b, c = nlb.get(qdate(qq)), ipay.get(qdate(qq)), irec.get(qdate(qq))
            return None if None in (a, b, c) else (a, b - c, a + b - c)
        n, pn = now_of(q), now_of(prevq(q))
        row['now'] = None if n is None else {'balance': round(n[0], 1), 'interest': round(n[1], 1), 'primary': round(n[2], 1)}
        if n and pn:
            row['chg_now'] = round(n[2] - pn[2], 1)
        prows.append(row)
    write('federal-primary-balance', {'id': 'federal-primary-balance', 'name': 'Federal primary balance, national income accounts',
                                      'freq': 'Q', 'manual': True, 'change': 'diff', 'fields': ['balance', 'interest', 'primary'],
                                      'then': {'label': 'Surplus or deficit on income and product account plus net interest paid, federal sector, seasonally adjusted annual rates', 'source': 'Economic Report of the President, statistical tables'},
                                      'now': {'label': 'BEA: federal net lending or net borrowing, plus interest payments less interest receipts, SAAR', 'unit': 'billions of dollars, SAAR',
                                              'source': 'FRED AD02RC1Q027SBEA, A091RC1Q027SBEA, B094RC1Q027SBEA', 'url': FRED + 'AD02RC1Q027SBEA'}}, prows)

    # OMB's fiscal-year ratios, retrospective
    orows = []
    for p in sorted(OMB_DEBT)[1:]:
        g, h = OMB_DEBT[p]
        pg, ph = OMB_DEBT[f'FY{int(p[2:]) - 1}']
        orows.append({'p': p, 'now': {'public': h, 'gross': g}, 'chg_now': round(h - ph, 1), 'chg_now_gross': round(g - pg, 1)})
    write('debt-gdp-omb', {'id': 'debt-gdp-omb', 'name': 'Federal debt to GDP, OMB (retrospective)', 'freq': 'FY', 'then': None,
                           'now': {'label': 'OMB, Historical Tables, Table 7.1: debt held by the public and gross federal debt at the end of the fiscal year, percent of GDP for the fiscal year',
                                   'unit': 'percent of GDP', 'source': 'OMB, Historical Tables, Table 7.1 (Budget for fiscal 2027)', 'url': OMB71}}, orows)


if __name__ == '__main__':
    if ONLY is None or 'alfred' in ONLY:
        main()
    if ONLY is None or 'manual' in ONLY:
        manual()
    if ONLY is None or 'gap' in ONLY:
        gap_cbo()
    if ONLY is None or 'rates' in ONLY:
        rates()
    if ONLY is None or 'debt' in ONLY:
        debt()
