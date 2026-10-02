"""Monthly and quarterly indicators for the calendar, as first reported and as revised today.
# Usage: FRED_API_KEY=... python3 tools/indicators/make_indicators.py [FROM TO]
#   FROM, TO are reporting periods, default 1960-12-01 1962-12-31.
#   Rewrites indicators/<id>.yaml for the series in API below. Series entered by hand from the
#   Economic Reports and budget documents (manual: true in their files) are left alone.
#   'first' is the initial release in ALFRED, with the date it was released; 'chg' is the change
#   from the prior period in that same release. 'now' is the current FRED value.
#   The key is read from the environment and never written out.
"""
import json, os, sys, time, urllib.parse, urllib.request
import yaml

KEY = os.environ.get('FRED_API_KEY') or sys.exit('set FRED_API_KEY')
FROM, TO = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ('1960-12-01', '1962-12-31')
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'indicators')
FRED = 'https://fred.stlouisfed.org/series/'
ALFRED = 'https://alfred.stlouisfed.org/series?seid='

# id: (series, freq, name, unit then, unit now, change kind, label then, label now)
API = {
    'cpi': ('CPIAUCNS', 'M', 'Consumer price index', None, '1982–84=100', 'pct',
            'BLS, Consumer Price Index for city wage-earner and clerical-worker families, all items, not seasonally adjusted',
            'BLS, CPI for all urban consumers (CPI-U), all items, not seasonally adjusted'),
    'unemployment': ('UNRATE', 'M', 'Unemployment rate', 'percent of civilian labor force', 'percent', None,
            'BLS, from the Census Current Population Survey, seasonally adjusted',
            'BLS, Current Population Survey, seasonally adjusted, ages 16 and over'),
    'payrolls': ('PAYEMS', 'M', 'Nonfarm payroll employment', 'thousands', 'thousands', 'diff',
            'BLS, establishment survey, wage and salary workers in nonagricultural establishments, seasonally adjusted',
            'BLS, Current Employment Statistics, all employees, total nonfarm, seasonally adjusted'),
    'industrial-production': ('INDPRO', 'M', 'Industrial production', None, '2017=100', 'pct',
            'Federal Reserve Board, index of industrial production, seasonally adjusted',
            'Federal Reserve Board, industrial production index, seasonally adjusted'),
    'gnp': ('GNP', 'Q', 'Gross national product', 'billions of dollars, seasonally adjusted annual rate', 'billions of dollars, SAAR', 'diff',
            'Commerce, Office of Business Economics, national income accounts',
            'BEA, national income and product accounts'),
    'real-gnp': ('GNPC96', 'Q', 'Real gross national product', None, 'billions of chained 2017 dollars, SAAR', 'pct',
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


def first_releases(sid):
    d = get('series/observations', series_id=sid, output_type=4, realtime_start='1776-07-04',
            realtime_end='9999-12-31', observation_start=FROM, observation_end=TO)
    return [(o['date'], num(o['value']), o['realtime_start']) for o in d['observations'] if num(o['value']) is not None]


def vintage(sid, date):
    d = get('series/observations', series_id=sid, realtime_start=date, realtime_end=date,
            observation_start='1959-01-01', observation_end=TO)
    return {o['date']: num(o['value']) for o in d['observations']}


def current(sid):
    d = get('series/observations', series_id=sid, observation_start=FROM, observation_end=TO)
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


def change(kind, a, b):
    if a is None or b is None:
        return None
    return round(100 * (a / b - 1), 1) if kind == 'pct' else round(a - b, 1)


def write(sid_key, meta, rows):
    path = os.path.join(OUT, f'{sid_key}.yaml')
    head = ('# Generated by tools/indicators/make_indicators.py. Edit the script, not this file.\n'
            '# p: reporting period; first: as first reported (released: date); chg: change from the prior\n'
            '# period in that release; unit: the unit then, where it differs; now: as revised today.\n')
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
            row['unit'] = base(sid, rel) or u_then
            row['now'] = cur.get(date)
            rows.append(row)
        write(key, {'id': key, 'name': name, 'freq': freq, 'change': kind,
                    'then': {'label': then, 'source': f'ALFRED {sid}, initial release', 'url': ALFRED + sid},
                    'now': {'label': now, 'unit': u_now, 'source': f'FRED {sid}', 'url': FRED + sid}}, rows)
    # Implicit deflator: nominal over real GNP in the release that first carried the quarter.
    sid, name, u_now, then, now = DEFLATOR
    cur = current(sid)
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
            row['chg'] = round(100 * (d / (100 * pn / pr) - 1), 1)
        row['unit'] = base(sid, rel)
        row['now'] = cur.get(date)
        rows.append(row)
    write('deflator', {'id': 'deflator', 'name': name, 'freq': 'Q', 'change': 'pct',
                       'then': {'label': then, 'source': 'ALFRED GNP and GNPC96, initial release', 'url': ALFRED + 'GNP'},
                       'now': {'label': now, 'unit': u_now, 'source': f'FRED {sid}', 'url': FRED + sid}}, rows)


# ---------------------------------------------------------------- series transcribed from the Economic Reports
# Values read from the page images of the Economic Report of the President, January 1962 (transmitted
# Jan. 22, 1962) and January 1963 (Jan. 21, 1963), U.S. Congressional Serial Set on govinfo. For these
# series 'first' is the figure as it stood in the next January's Report, not the first release.
ERP = {
    1962: ('1962-01-22', 'Economic Report of the President, Jan. 1962',
           'https://www.govinfo.gov/app/details/SERIALSET-12497_00_00-002-0278-0000'),
    1963: ('1963-01-21', 'Economic Report of the President, Jan. 1963',
           'https://www.govinfo.gov/app/details/SERIALSET-12600_00_00-002-0028-0000'),
}
MONTHS = [f'{y}-{m:02d}' for y, m in [(1960, 12)] + [(y, m) for y in (1961, 1962) for m in range(1, 13)]]
MANUAL = {
    'wpi': dict(
        name='Wholesale price index', freq='M', change='pct',
        then='BLS, wholesale price index, all commodities', now_label='BLS, producer price index, all commodities',
        now_unit='1982=100', now_fred='PPIACO',
        tables={1962: 'Table B-40, p. 254 (1947–49=100)', 1963: 'Table C-41, p. 220 (1957–59=100)'},
        rows={**{p: (v, 1962, '1947–49=100') for p, v in zip(MONTHS[:13], [
            119.5, 119.9, 120.0, 119.9, 119.4, 118.7, 118.2, 118.6, 118.9, 118.8, 118.7, 118.8, 119.2])},
              **{p: (v, 1963, '1957–59=100') for p, v in zip(MONTHS[13:], [
            100.8, 100.7, 100.7, 100.4, 100.2, 100.0, 100.4, 100.5, 101.2, 100.6, 100.7, 100.4])}}),
    'administrative-budget': dict(
        name='Federal budget (administrative)', freq='FY', fields=('receipts', 'expenditures', 'balance'),
        then='Treasury and Bureau of the Budget, net budget receipts and budget expenditures (the administrative budget), fiscal years ending June 30, millions of dollars',
        now_label='OMB, unified budget receipts, outlays, and surplus or deficit (a later concept, from fiscal 1969)',
        now_unit='millions of dollars', now_fred=('FYFR', 'FYONET', 'FYFSD'),
        tables={1962: 'Table B-55, p. 272', 1963: 'Table C-56, p. 238'},
        rows={'FY1961': ((77659, 81515, -3856), 1962, 'millions of dollars'),
              'FY1962': ((81409, 87787, -6378), 1963, 'millions of dollars')},
        est={'FY1962': [((82100, 89075, -6975), 1962)], 'FY1963': [((93000, 92537, 463), 1962), ((85500, 94311, -8811), 1963)]}),
    'cash-budget': dict(
        name='Federal cash receipts from and payments to the public', freq='FY', fields=('receipts', 'payments', 'balance'),
        then='Treasury, Bureau of the Budget, and CEA, the consolidated cash statement, federal, fiscal years, billions of dollars',
        now_label='OMB, unified budget receipts, outlays, and surplus or deficit (a later concept, from fiscal 1969)',
        now_unit='millions of dollars', now_fred=('FYFR', 'FYONET', 'FYFSD'),
        tables={1962: 'Table B-57, p. 274', 1963: 'Table C-58, p. 240'},
        rows={'FY1961': ((97.2, 99.5, -2.3), 1962, 'billions of dollars'),
              'FY1962': ((101.9, 107.7, -5.8), 1963, 'billions of dollars')},
        est={'FY1962': [((102.6, 111.1, -8.5), 1962)], 'FY1963': [((116.6, 114.8, 1.8), 1962), ((108.4, 116.8, -8.3), 1963)]}),
    'federal-national-accounts': dict(
        name='Federal receipts and expenditures, national income accounts', freq='Q', fields=('receipts', 'expenditures', 'balance'),
        then='Commerce and Bureau of the Budget, federal government receipts and expenditures in the national income accounts, seasonally adjusted annual rates, billions of dollars',
        now_label='BEA, federal government current receipts and current expenditures, SAAR (balance computed)',
        now_unit='billions of dollars, SAAR', now_fred=('FGRECPT', 'FGEXPND', None),
        tables={1962: 'Table B-59, p. 276', 1963: 'Table C-60, p. 242'},
        rows={'1960Q4': ((94.6, 94.2, 0.4), 1962, 'billions of dollars, annual rate'), '1961Q1': ((92.5, 98.0, -5.5), 1962, 'billions of dollars, annual rate'),
              '1961Q2': ((96.8, 101.1, -4.3), 1962, 'billions of dollars, annual rate'), '1961Q3': ((99.3, 102.4, -3.1), 1962, 'billions of dollars, annual rate'),
              '1961Q4': ((103.8, 105.1, -1.3), 1963, 'billions of dollars, annual rate'), '1962Q1': ((105.9, 108.3, -2.4), 1963, 'billions of dollars, annual rate'),
              '1962Q2': ((108.4, 109.0, -0.7), 1963, 'billions of dollars, annual rate'), '1962Q3': ((108.9, 109.8, -0.9), 1963, 'billions of dollars, annual rate'),
              '1962Q4': ((None, 112.5, None), 1963, 'billions of dollars, annual rate')}),
    'balance-of-payments': dict(
        name='Balance of payments, over-all surplus or deficit', freq='Q', fields=('balance',),
        then='Commerce, over-all balance (changes in U.S. gold stock, convertible currencies, and liquid liabilities to foreigners), seasonally adjusted annual rates, millions of dollars',
        now_label='No longer published: the over-all (liquidity) balance was dropped from the official accounts',
        now_unit=None, now_fred=None,
        tables={1963: 'Table C-78, p. 263'},
        rows={'1960Q4': ((-5252,), 1963, 'millions of dollars, annual rate'), '1961Q1': ((-1276,), 1963, 'millions of dollars, annual rate'), '1961Q2': ((704,), 1963, 'millions of dollars, annual rate'),
              '1961Q3': ((-3640,), 1963, 'millions of dollars, annual rate'), '1961Q4': ((-5632,), 1963, 'millions of dollars, annual rate'), '1962Q1': ((-1968,), 1963, 'millions of dollars, annual rate'),
              '1962Q2': ((-904,), 1963, 'millions of dollars, annual rate'), '1962Q3': ((-2876,), 1963, 'millions of dollars, annual rate'),
              '1960': ((-3925,), 1963, 'millions of dollars, year'), '1961': ((-2461,), 1963, 'millions of dollars, year'),
              '1962': ((-1916,), 1963, 'millions of dollars, annual rate, first three quarters')}),
    'gold-stock': dict(
        name='Monetary gold stock', freq='M', change='diff',
        then=None, now_label='Treasury monetary gold stock, end of month, as compiled by NBER from the Federal Reserve Bulletin',
        now_unit='millions of dollars', now_fred='M1476CUSM144NNBR', tables={}, rows={p: (None, None, None) for p in MONTHS}),
}


def fred_obs(sid):
    d = get('series/observations', series_id=sid, observation_start='1960-01-01', observation_end=TO)
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
                row['source'] = f'{ERP[erp][1]}, {m["tables"][erp]}'
                if unit:
                    row['unit'] = unit
                if m.get('change') == 'pct' and prev and prev[1] == erp:
                    row['chg'] = round(100 * (v / prev[0] - 1), 1)
                prev = (v, erp)
            for e in m.get('est', {}).get(p, []):
                row.setdefault('est', []).append({'value': dict(zip(m['fields'], e[0])), 'as_of': ERP[e[1]][0],
                                                  'source': f'{ERP[e[1]][1]}, {m["tables"][e[1]]}'})
            row['now'] = now_for(p)
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


if __name__ == '__main__':
    main()
    manual()
