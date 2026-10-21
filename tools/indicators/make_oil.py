"""Oil for the calendar's monthly tables: U.S. crude production, products supplied, trade, and proved reserves.
# Usage: python3 tools/indicators/make_oil.py
#   Rewrites indicators/oil-*.yaml. Needs the network and xlrd (EIA's history workbooks are .xls); the build does not.
#
#   As first reported ("first"): the Survey of Current Business (Commerce), its monthly statistical pages, "Petroleum
#   and products", from the Bureau of Mines (p. S-35 of each issue, 1960-69; FRASER's scans, read by eye; SCB below):
#   for each month, the issue that first printed it. The Survey printed the Bureau's monthly figures two to four
#   months after the month (the issues of Mar. 1967, Oct. 1967 and Aug. 1968 add none; the next
#   adds two); the Bureau's own Monthly Petroleum Statement came out earlier and is not read here (no
#   open copy found). Thousands of barrels in the month through the issue of Sept. 1961, millions (one decimal) from
#   Oct. 1961.
#   Proved reserves: the American Petroleum Institute's estimate for Dec. 31, as the Bureau of Mines' Minerals
#   Yearbook for the year printed it (RESERVES below; the API's own reports, issued each spring, not read here).
#   Revised today ("now"): EIA. Crude production, monthly (MCRFPUS2); products supplied, monthly from 1963 (MTTUPUS2);
#   imports, exports and net imports, annual (Monthly Energy Review, Table 3.1; EIA's monthly trade begins in 1973);
#   proved reserves, annual (RCRR01NUS_1; before 1977 EIA carries the API's figures).
#   The posted price of Arabian light at Ras Tanura is not here: no source read gives it (notes/leads.md).
"""
import calendar, csv, io, os, urllib.request
import yaml

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'indicators')
UA = {'User-Agent': 'bib-calendar/1.0 (research; github.com/impending2223/bib)'}
EIA_XLS = 'https://www.eia.gov/dnav/pet/hist_xls/{}.xls'
EIA_LEAF = 'https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s={}&f={}'
MER = 'https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T03.01'
SCB_PDF = 'https://fraser.stlouisfed.org/files/docs/publications/SCB/1960-69/SCB_{:02d}{}.pdf'
FROM, TO = '1960-01', '1969-01'
MON = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']

# The Survey of Current Business, p. S-35, the latest month's column, read by eye from FRASER's scans (Oct. 2026).
# issue (YYYYMM), month, crude production, imports of crude, imports of refined products, exports of crude, exports of
# refined products, domestic demand (total). '<.05': the Survey's note, less than 50,000 barrels; '—': no figure printed.
SCB = """
196004 1960-01 224140 28610 30713 264 5734 324828
196005 1960-02 209986 29730 29377 299 5505 301456
196006 1960-03 220977 29292 29966 260 6302 338184
196007 1960-04 211132 33877 24614 270 6477 276431
196008 1960-05 212296 30571 20711 127 6421 268522
196009 1960-06 208161 32730 20483 436 7155 280600
196010 1960-07 212645 31191 19551 248 5742 271062
196011 1960-08 215145 32768 19493 89 5938 281457
196012 1960-09 209119 32691 20634 234 5393 270562
196101 1960-10 215687 31458 20989 352 5641 277493
196102 1960-11 213992 29980 26664 0 5164 299669
196103 1960-12 221653 28677 27903 512 5326 351924
196104 1961-01 223497 33688 33481 135 5014 341610
196105 1961-02 204274 28768 30117 295 4299 294028
196106 1961-03 231596 23276 27877 339 5108 301844
196107 1961-04 219846 26969 27878 316 5279 275016
196108 1961-05 221553 33566 23902 229 5690 286691
196109 1961-06 213084 27186 18994 435 15357 272393
196110 1961-07 215.7 38.0 24.3 .2 4.8 281.2
196111 1961-08 220.2 34.0 18.8 .3 5.4 293.6
196112 1961-09 209.8 33.1 21.8 .1 4.4 276.2
196201 1961-10 220.9 33.6 23.3 .1 5.2 290.3
196202 1961-11 214.6 30.1 26.5 .4 5.0 309.6
196203 1961-12 226.6 29.2 31.0 .3 4.7 342.6
196204 1962-01 227.8 36.3 39.3 .1 4.7 367.5
196205 1962-02 209.1 31.6 27.9 .1 5.0 305.8
196206 1962-03 228.7 31.8 33.9 .2 4.6 332.2
196207 1962-04 221.7 32.2 26.9 .1 4.9 286.4
196208 1962-05 223.0 34.2 25.1 .3 5.2 292.5
196209 1962-06 217.7 33.8 24.7 <.05 4.8 286.5
196210 1962-07 224.0 35.9 22.8 .2 5.0 291.0
196211 1962-08 224.2 40.3 24.5 .2 5.2 296.8
196212 1962-09 219.6 34.4 27.2 .1 5.7 284.5
196301 1962-10 228.4 35.8 26.9 <.05 4.0 307.6
196302 1962-11 223.2 33.3 31.6 .2 4.8 330.8
196303 1962-12 228.8 31.3 37.2 .1 5.6 351.6
196304 1963-01 226.4 41.0 43.1 .2 4.1 381.1
196305 1963-02 212.4 30.9 35.5 .1 8.2 334.8
196306 1963-03 234.3 36.1 29.8 .1 5.5 317.5
196307 1963-04 228.3 32.6 32.5 .2 6.6 294.1
196308 1963-05 234.5 34.5 27.1 .2 6.2 304.7
196309 1963-06 226.9 31.9 22.3 .1 5.4 285.8
196310 1963-07 235.1 38.2 27.0 .2 5.9 308.3
196311 1963-08 236.8 36.7 25.5 .2 6.4 315.2
196312 1963-09 225.2 34.9 23.9 .1 7.0 298.7
196401 1963-10 233.6 31.4 32.7 .2 6.0 313.8
196402 1963-11 226.3 34.2 27.6 .1 6.5 313.0
196403 1963-12 232.8 30.3 38.0 .2 6.3 385.1
196404 1964-01 238.1 39.6 49.0 .1 6.7 379.0
196405 1964-02 224.5 32.2 35.2 .1 4.8 331.0
196406 1964-03 240.6 36.9 32.2 .2 6.0 333.1
196407 1964-04 233.1 33.1 35.2 .1 6.4 320.1
196408 1964-05 235.8 36.0 28.2 .2 5.7 303.8
196409 1964-06 228.3 34.4 26.3 .2 6.4 314.2
196410 1964-07 233.7 43.8 28.1 .1 6.7 320.5
196411 1964-08 232.6 40.7 28.3 .1 6.0 313.9
196412 1964-09 227.9 36.9 25.6 .1 5.6 316.2
196501 1964-10 237.3 39.2 31.8 .1 6.5 335.6
196502 1964-11 230.7 34.1 30.0 — 5.4 320.7
196503 1964-12 242.3 31.7 39.5 .1 6.2 387.4
196504 1965-01 240.9 37.3 47.1 .1 5.0 372.5
196505 1965-02 218.6 32.7 41.3 <.05 4.7 344.2
196506 1965-03 243.8 41.4 42.8 <.05 6.3 371.3
196507 1965-04 236.8 38.1 41.6 .2 6.3 334.5
196508 1965-05 283.3 39.0 32.9 0 5.8 317.2
196509 1965-06 232.4 39.9 33.3 .1 6.2 321.2
196510 1965-07 237.6 40.7 30.6 .4 5.7 324.2
196511 1965-08 240.2 40.8 29.9 0 5.7 330.2
196512 1965-09 222.5 43.2 28.4 0 5.2 319.6
196601 1965-10 244.1 39.1 36.2 .2 5.1 340.0
196602 1965-11 239.6 32.0 35.4 .1 5.5 347.0
196603 1965-12 253.6 27.9 49.0 <.05 5.3 400.9
196604 1966-01 250.5 42.0 46.9 .1 5.1 389.7
196605 1966-02 231.7 34.7 44.5 0 5.6 364.4
196606 1966-03 258.1 38.8 53.1 .1 6.2 373.8
196607 1966-04 249.2 36.5 37.6 .3 5.8 344.9
196608 1966-05 259.8 37.3 37.2 <.05 5.5 338.1
196609 1966-06 251.5 39.0 37.4 .1 6.1 350.1
196610 1966-07 256.3 39.1 37.6 .2 6.1 335.3
196611 1966-08 257.0 41.5 39.7 .2 5.9 356.8
196612 1966-09 248.8 36.0 35.4 .1 7.0 337.4
196701 1966-10 259.3 36.0 37.7 .1 6.0 354.5
196702 1966-11 252.8 34.4 39.2 .1 5.7 371.4
196704 1966-12 286.3 32.0 45.9 .1 6.0 408.9
196705 1967-01 265.6 41.1 55.2 <.05 5.7 398.2
196706 1967-02 241.5 29.2 46.4 — 6.6 368.3
196707 1967-03 264.9 37.6 51.9 .1 6.3 403.9
196708 1967-04 254.3 38.2 46.2 .3 6.8 340.7
196709 1967-05 260.0 39.9 40.2 0 6.9 363.9
196711 1967-06 256.3 33.6 36.9 1.8 7.0 354.4
196711 1967-07 283.9 30.1 31.8 8.5 7.7 351.2
196712 1967-08 292.5 31.5 35.2 8.2 8.1 367.4
196801 1967-09 272.9 31.5 32.6 6.0 8.4 340.8
196802 1967-10 279.1 31.9 46.4 1.4 7.6 381.4
196803 1967-11 269.4 29.6 40.2 .1 8.4 398.1
196804 1967-12 276.2 37.5 49.4 .1 5.9 410.7
196805 1968-01 279.7 30.5 63.3 .2 6.2 465.6
196806 1968-02 270.3 28.2 54.2 .3 6.4 416.5
196807 1968-03 288.8 35.5 58.5 <.05 8.1 404.8
196807 1968-04 273.7 32.5 43.7 .1 7.2 374.6
196809 1968-05 285.4 37.5 38.1 .1 8.0 370.6
196809 1968-06 274.4 40.2 42.9 .2 7.7 364.0
196810 1968-07 283.9 45.7 44.6 <.05 7.1 382.6
196811 1968-08 285.8 43.2 36.0 .1 7.2 394.1
196812 1968-09 269.1 42.5 42.9 .1 7.4 368.1
196901 1968-10 276.4 45.9 45.1 .1 6.6 400.1
196902 1968-11 269.3 40.8 43.1 .4 6.6 399.8
196903 1968-12 276.1 49.9 52.4 .1 7.2 465.8
196904 1969-01 275.0 37.6 66.4 0 5.8 493.9
"""
# A figure the Survey corrected later, or a change in what a row counts: shown in grey after the figure.
NOTE = {
    ('1961-06', 'trade'): 'products exports as printed, 15,357; the Oct. 1961 issue, 5.4m bbl',
    ('1965-05', 'production'): 'as printed, 283.3m bbl; the Sept. 1965 issue, 238.3',
    ('1966-12', 'production'): 'as printed, 286.3m bbl; the May 1967 issue, 263.8',
    ('1969-01', 'trade'): 'crude imports now "crude and unfinished oils"',
}

# The API's proved reserves at Dec. 31, as the Minerals Yearbook for the year printed them: millions of barrels,
# the Yearbook (volume, page) and its imprint year. The figure as the text gives it (1960, 1961 in billions, one
# decimal; 1966 the table's total, the text not giving it).
MYB = 'https://archive.org/details/pub_usgov-minerals-yearbook_{}'
RESERVES = {
    1960: (31600, '1960_2', 'II, 372', '1961'),
    1961: (31800, '1961_2', 'II, 365', '1962'),
    1962: (31389.2, '1962_2', 'II, 382', '1963'),
    1963: (30969.99, '1963_2', 'II, 398', '1964'),
    1964: (30990.51, '1964_2', 'II, 391', '1965'),
    1965: (31352.391, '1965_2', 'II, 357', '1967'),
    1966: (31452, '1966_12', 'I–II, 816, Table 3', '1967'),
    1967: (31376.67, '1967_12', 'I–II, 843', '1968'),
    1968: (30707, '1968_12', 'I–II, 816–17', '1969'),
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return r.read()


def eia_xls(code):
    """{period: value} from an EIA history workbook: 'YYYY-MM' (monthly) or 'YYYY' (annual)."""
    import xlrd
    book = xlrd.open_workbook(file_contents=get(EIA_XLS.format(code)))
    sh = book.sheet_by_name('Data 1')
    out = {}
    for i in range(3, sh.nrows):
        d, v = sh.cell(i, 0), sh.cell(i, 1).value
        if d.ctype != xlrd.XL_CELL_DATE or v in ('', None):
            continue
        y, m = xlrd.xldate_as_tuple(d.value, book.datemode)[:2]
        out[f'{y}-{m:02d}' if code.endswith('m') else f'{y}'] = float(v)
    return out


def mer():
    """{year: {imports, exports, net}} in thousand barrels a day, MER Table 3.1."""
    keys = {'PAIMPUS': 'imports', 'PAEXPUS': 'exports', 'PANIPUS': 'net'}
    out = {}
    for r in csv.DictReader(io.StringIO(get(MER).decode('utf-8'))):
        ym = r['YYYYMM']
        if r['MSN'] in keys and ym.endswith('13') and r['Value'] not in ('', 'Not Available'):
            out.setdefault(ym[:4], {})[keys[r['MSN']]] = round(float(r['Value']), 1)
    return out


def num(s):
    if s in ('—', '<.05'):
        return s
    return float(s) if '.' in s else int(s)


def scb_rows():
    out = []
    for line in SCB.strip().splitlines():
        iss, m, *v = line.split()
        y, mo = int(iss[:4]), int(iss[4:])
        out.append(dict(issue=f'{y}-{mo:02d}', p=m, prod=num(v[0]), imp_c=num(v[1]), imp_r=num(v[2]),
                        exp_c=num(v[3]), exp_r=num(v[4]), dem=num(v[5]),
                        unit='thousands of barrels' if '.' not in v[0] else 'millions of barrels',
                        source=f'Survey of Current Business, {MON[mo - 1]} {y}, p. S-35 (Bureau of Mines); '
                               + SCB_PDF.format(mo, y)))
    return out


def write(key, meta, rows):
    path = os.path.join(OUT, f'{key}.yaml')
    head = ('# Generated by tools/indicators/make_oil.py. Edit the script, not this file.\n'
            '# p: reporting period; first: as first reported, in the source\'s unit (unit), released: the issue or\n'
            '# volume; now: as revised today, in now.unit; note: a correction or change of concept, shown in grey.\n')
    body = yaml.safe_dump(dict(meta, rows=rows), sort_keys=False, allow_unicode=True, width=200,
                          default_flow_style=None)
    open(path, 'w', encoding='utf-8').write(head + body)
    print('wrote', path, len(rows))


def main():
    prod_now = eia_xls('MCRFPUS2m')
    supp_now = eia_xls('MTTUPUS2m')
    res_now = eia_xls('RCRR01NUS_1a')
    trade_now = mer()
    scb = scb_rows()
    base = dict(manual=True, change='none')

    rows = []
    for r in scb:
        row = dict(p=r['p'], first=r['prod'], released=r['issue'], unit=r['unit'], source=r['source'])
        if (r['p'], 'production') in NOTE:
            row['note'] = NOTE[(r['p'], 'production')]
        row['now'] = prod_now.get(r['p'])
        rows.append(row)
    write('oil-production', dict(id='oil-production', name='Crude oil production', freq='M', **base,
          then={'label': 'Bureau of Mines, crude petroleum production, in the month, as the Survey of Current Business printed it'},
          now={'label': 'EIA, U.S. field production of crude oil', 'unit': 'thousand barrels per day',
               'source': 'EIA MCRFPUS2', 'url': EIA_LEAF.format('MCRFPUS2', 'M')}), rows)

    rows = []
    for r in scb:
        row = dict(p=r['p'], first=r['dem'], released=r['issue'], unit=r['unit'], source=r['source'])
        if r['p'] in supp_now:
            row['now'] = supp_now[r['p']]
        rows.append(row)
    write('oil-supplied', dict(id='oil-supplied', name='Petroleum products supplied', freq='M', **base,
          then={'label': 'Bureau of Mines, domestic demand for all oils, in the month, as the Survey of Current Business printed it'},
          now={'label': 'EIA, U.S. product supplied of crude oil and petroleum products (monthly from 1963)',
               'unit': 'thousand barrels per day', 'source': 'EIA MTTUPUS2', 'url': EIA_LEAF.format('MTTUPUS2', 'M')}),
          rows)

    rows = []
    for r in scb:
        row = dict(p=r['p'], first=dict(crude_imports=r['imp_c'], product_imports=r['imp_r'],
                                        crude_exports=r['exp_c'], product_exports=r['exp_r']),
                   released=r['issue'], unit=r['unit'], source=r['source'])
        if (r['p'], 'trade') in NOTE:
            row['note'] = NOTE[(r['p'], 'trade')]
        rows.append(row)
    write('oil-trade', dict(id='oil-trade', name='Petroleum imports and exports', freq='M', **base,
          then={'label': 'Bureau of Mines, imports and exports of crude petroleum and refined products, in the month, as the Survey of Current Business printed them'},
          now=None), rows)

    rows = []
    for y in range(1960, 1969):
        t = trade_now.get(str(y))
        if t:
            rows.append(dict(p=str(y), now=t))
    write('oil-trade-year', dict(id='oil-trade-year', name='Petroleum imports and exports, year', freq='A',
          change='none', then=None,
          now={'label': 'EIA, Monthly Energy Review, Table 3.1: petroleum imports, exports, net imports',
               'unit': 'thousand barrels per day', 'source': 'EIA, Monthly Energy Review, Table 3.1', 'url': MER}),
          rows)

    rows = []
    for y, (v, vol, page, printed) in RESERVES.items():
        rows.append(dict(p=str(y), first=v, released=printed, unit='millions of barrels',
                         source=f'API estimate, Dec. 31, {y}, in Minerals Yearbook {y}, {page}; {MYB.format(vol)}',
                         now=res_now.get(str(y))))
    write('oil-reserves', dict(id='oil-reserves', name='Crude oil proved reserves', freq='A', **base,
          then={'label': 'American Petroleum Institute, Committee on Petroleum Reserves, proved reserves of crude oil, Dec. 31, as the Minerals Yearbook printed them'},
          now={'label': 'EIA, U.S. crude oil proved reserves (API figures before 1977)', 'unit': 'million barrels',
               'source': 'EIA RCRR01NUS_1', 'url': EIA_LEAF.format('RCRR01NUS_1', 'A')}), rows)


if __name__ == '__main__':
    main()
