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
# Sources then (each block below names its tables and pages): as first printed, read off FRASER's page images (Oct.
#   23, 2026): the exchange rates (FX: the Federal Reserve Bulletin), the mortgage rates (FHA, CONV, EFF: the Bulletin,
#   from July 1964), the debt's interest rate (TBRATE: the Treasury Bulletin) and its average length for 1963-65 (the TB
#   lines of MATURITY). As the next January's Economic Report tabled them (February in 1968; ERP_<year>.pdf, the
#   printed page plus 8 in 1962 and 1964, plus 30 in 1963, plus 6 in 1965-69): the money stock (M1, M1 and time
#   deposits), free reserves, reserve assets, the trade balances by quarter, the debt's holders and its average length
#   for 1961-62 and 1966-68; for these 'first' is the figure as the next Report tabled it, as for the Reports' series
#   in make_indicators.py, their first printings not yet read (notes/leads.md, "Money, the foreign accounts, the
#   debt's terms"). The London gold price and the liabilities to foreign official holders have no series yet.
# Sources today: FRED's public CSVs: AAA, BAA (Moody's, not revised: one figure), NFORBRES, TRESEGUSM052N, BOPBM and
#   BOPBGS (discontinued; times four for annual rates), ULCNFB and COMPNFB (nonfarm business, today only); the Board's
#   Data Download Program for H.6 (M1, M2: FRED's M1SL and M2SL are its copies) and, where FRED fails, H.3.
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
    'ERP64': ('1964-01-20', 'Economic Report of the President, Jan. 1964',
              'https://www.govinfo.gov/app/details/SERIALSET-12658_00_00-002-0278-0000'),
    'ERP65': ('1965-01-28', 'Economic Report of the President, Jan. 1965',
              'https://www.govinfo.gov/app/details/SERIALSET-12702_00_00-002-0028-0000'),
    'ERP66': ('1966-01-27', 'Economic Report of the President, Jan. 1966',
              'https://www.govinfo.gov/app/details/SERIALSET-12742_00_00-002-0348-0000'),
    'ERP67': ('1967-01-26', 'Economic Report of the President, Jan. 1967',
              'https://fraser.stlouisfed.org/title/economic-report-president-45/1967-8138'),
    'ERP68': ('1968-02-01', 'Economic Report of the President, Feb. 1968',
              'https://www.govinfo.gov/app/details/SERIALSET-12825_00_00-002-0238-0000'),
    'ERP69': ('1969-01-16', 'Economic Report of the President, Jan. 1969',
              'https://www.govinfo.gov/app/details/SERIALSET-12868_00_00-002-0028-0000'),
}

for _y in range(1960, 1970):            # the Treasury Bulletin's issues (FRASER's files): TB6202
    for _m in range(1, 13):
        SRC[f'TB{_y % 100:02d}{_m:02d}'] = (f'{_y}-{_m:02d}', f'Treasury Bulletin, {MON[_m - 1]} {_y}',
                                            f'https://fraser.stlouisfed.org/files/docs/publications/tbulletin/{_y}_{_m:02d}_treasurybulletin.pdf')
for _y in range(1960, 1970):            # the Federal Reserve Bulletin's issues (FRASER's files): FRB6407
    for _m in range(1, 13):
        SRC[f'FRB{_y % 100:02d}{_m:02d}'] = (f'{_y}-{_m:02d}', f'Federal Reserve Bulletin, {MON[_m - 1]} {_y}',
                                             f'https://fraser.stlouisfed.org/files/docs/publications/FRB/1960s/frb_{_m:02d}{_y}.pdf')

# ---------------------------------------------------------------- READ: the figures printed then
# Each block: lines "SRC/where PERIOD VALUE[/VALUE...] [prior=VALUE] [note=TEXT]". SRC is a key of SRC above, 'where'
# the table and page. A period printed in several sources is taken from the first listed. prior: the period before as
# printed in the same place (the change 'in that release'); without it, the change is taken from the period before
# where the same place prints it.

# The mortgage rates: the Federal Reserve Bulletin's table "Mortgages: new homes" (from the July 1964 issue, which
# begins it at Apr. 1963), "Mortgages: new and existing homes" (from Aug. 1966) and "Home-mortgage yields" (from Nov.
# 1968), each month as the issue that first printed it (the yield a month before the conventional rate, until the
# Aug. 1966 issue), read off FRASER's page images at 150 dpi. pdf= is the page in FRASER's file of the issue. The
# Bulletin's months are the months the data report on ("Price data are reported as of the first of the succeeding
# month"); the Economic Report dates the same figures by the first of the month after.
# FHA: the yield on FHA-insured new-home mortgages, secondary market (Sec. 203, 30-year, minimum downpayment, an
# assumed prepayment at the end of 15 years). Months the Bulletin leaves blank ("Gaps in the data are due to periods
# of adjustment to changes in maximum permissible contract interest rates"): Feb., Apr. and Oct. 1966, May 1968; Jan.
# 1967 blank in the Feb. 1967 issue, printed in Mar. The misprints of Sept. 1963 and Oct. 1965 stand, the correction
# noted.
FHA = """
FRB6407/p. 875, Mortgages: new homes 1963-09 4.45 pdf=65 note=corrected to 5.45 in the Aug. 1964 issue
FRB6511/p. 1575, Mortgages: new homes 1965-10 6.49 pdf=75 note=corrected to 5.49 in the Dec. 1965 issue
FRB6507/p. 991, Mortgages: new homes 1965-06 5.44 pdf=75
FRB6508/p. 1135, Mortgages: new homes 1965-07 5.44 pdf=87
FRB6407/p. 875, Mortgages: new homes 1963-05 5.45 pdf=65
FRB6407/p. 875, Mortgages: new homes 1963-06 5.45 pdf=65
FRB6407/p. 875, Mortgages: new homes 1963-07 5.45 pdf=65
FRB6407/p. 875, Mortgages: new homes 1963-08 5.45 pdf=65
FRB6407/p. 875, Mortgages: new homes 1963-10 5.45 pdf=65
FRB6407/p. 875, Mortgages: new homes 1963-11 5.45 pdf=65
FRB6407/p. 875, Mortgages: new homes 1963-12 5.45 pdf=65
FRB6407/p. 875, Mortgages: new homes 1964-01 5.45 pdf=65
FRB6407/p. 875, Mortgages: new homes 1964-02 5.45 pdf=65
FRB6407/p. 875, Mortgages: new homes 1964-03 5.45 pdf=65
FRB6407/p. 875, Mortgages: new homes 1964-04 5.45 pdf=65
FRB6407/p. 875, Mortgages: new homes 1964-05 5.45 pdf=65
FRB6408/p. 1047, Mortgages: new homes 1964-06 5.45 pdf=113
FRB6411/p. 1451, Mortgages: new homes 1964-10 5.45 pdf=79
FRB6412/p. 1565, Mortgages: new homes 1964-11 5.45 pdf=55
FRB6501/p. 143, Mortgages: new homes 1964-12 5.45 pdf=147
FRB6502/p. 287, Mortgages: new homes 1965-01 5.45 pdf=79
FRB6503/p. 455, Mortgages: new homes 1965-02 5.45 pdf=99
FRB6504/p. 571, Mortgages: new homes 1965-03 5.45 pdf=57
FRB6505/p. 715, Mortgages: new homes 1965-04 5.45 pdf=73
FRB6506/p. 853, Mortgages: new homes 1965-05 5.45 pdf=69
FRB6509/p. 1305, Mortgages: new homes 1965-08 5.45 pdf=111
FRB6407/p. 875, Mortgages: new homes 1963-04 5.46 pdf=65
FRB6409/p. 1171, Mortgages: new homes 1964-07 5.46 pdf=63
FRB6409/p. 1171, Mortgages: new homes 1964-08 5.46 pdf=63
FRB6410/p. 1299, Mortgages: new homes 1964-09 5.46 pdf=69
FRB6510/p. 1441, Mortgages: new homes 1965-09 5.46 pdf=79
FRB6512/p. 1753, Mortgages: new homes 1965-11 5.51 pdf=101
FRB6601/p. 73, Mortgages: new homes 1965-12 5.62 pdf=77
FRB6602/p. 235, Mortgages: new homes 1966-01 5.70 pdf=90
FRB6604/p. 565, Mortgages: new homes 1966-03 6.00 pdf=114
FRB6705/p. 816, Mortgages: new and existing homes 1967-04 6.29 pdf=128
FRB6607/p. 1011, Mortgages: new homes 1966-05 6.32 pdf=79 note=the June 1966 issue (pp. 857-858 missing from FRASER's copy) not read
FRB6704/p. 622, Mortgages: new and existing homes 1967-03 6.35 pdf=126
FRB6706/p. 1006, Mortgages: new and existing homes 1967-05 6.44 pdf=107
FRB6607/p. 1011, Mortgages: new homes 1966-06 6.45 pdf=79
FRB6703/p. 420, Mortgages: new and existing homes 1967-02 6.46 pdf=82
FRB6609/p. 1372, Mortgages: new and existing homes 1966-07 6.51 pdf=95
FRB6707/p. 1200, Mortgages: new and existing homes 1967-06 6.51 pdf=128
FRB6708/p. 1394, Mortgages: new and existing homes 1967-07 6.53 pdf=125
FRB6610/p. 1492, Mortgages: new and existing homes 1966-08 6.58 pdf=60
FRB6709/p. 1610, Mortgages: new and existing homes 1967-08 6.60 pdf=143
FRB6703/p. 420, Mortgages: new and existing homes 1967-01 6.62 pdf=82
FRB6610/p. 1492, Mortgages: new and existing homes 1966-09 6.63 pdf=60
FRB6710/p. 1780, Mortgages: new and existing homes 1967-09 6.63 pdf=104
FRB6711/p. 1952, Mortgages: new and existing homes 1967-10 6.65 pdf=100
FRB6701/p. 114, Mortgages: new and existing homes 1966-12 6.77 pdf=116
FRB6712/p. 2104, Mortgages: new and existing homes 1967-11 6.77 pdf=87
FRB6803/p. A-30, Mortgages: new and existing homes 1968-02 6.78 pdf=125
FRB6612/p. 1806, Mortgages: new and existing homes 1966-11 6.81 pdf=71
FRB6801/p. A-30, Mortgages: new and existing homes 1967-12 6.81 pdf=129
FRB6802/p. A-30, Mortgages: new and existing homes 1968-01 6.81 pdf=176
FRB6804/p. A-30, Mortgages: new and existing homes 1968-03 6.83 pdf=89
FRB6805/p. A-32, Mortgages: new and existing homes 1968-04 6.94 pdf=96
FRB6810/p. A-33, Mortgages: new and existing homes 1968-09 7.28 pdf=131
FRB6811/p. A-51, Home-mortgage yields 1968-10 7.29 pdf=112
FRB6809/p. A-33, Mortgages: new and existing homes 1968-08 7.35 pdf=102
FRB6812/p. A-51, Home-mortgage yields 1968-11 7.36 pdf=156
FRB6808/p. A-33, Mortgages: new and existing homes 1968-07 7.42 pdf=81
FRB6901/p. 51, Home-mortgage yields 1968-12 7.50 pdf=142
FRB6808/p. A-33, Mortgages: new and existing homes 1968-06 7.52 pdf=81
"""
# CONV: the contract interest rate on conventional first mortgages for new homes, the Federal Home Loan Bank Board's
# series (with the FDIC; "FHLBB series" from Aug. 1966; a "New FHLBB series" from the Apr. 1967 issue, beginning Dec.
# 1966, then July 1966), as first printed, Apr. 1963-Jan. 1968; "p" (preliminary) in the issues of Jan.-Mar. 1968. The
# Apr. 1968 issue drops it for the effective rate (EFF).
CONV = """
FRB6801/p. A-30, Mortgages: new and existing homes 1967-11 6.37 pdf=129 note=preliminary
FRB6802/p. A-30, Mortgages: new and existing homes 1967-12 6.45 pdf=176 note=preliminary
FRB6803/p. A-30, Mortgages: new and existing homes 1968-01 6.39 pdf=125 note=preliminary
FRB6505/p. 715, Mortgages: new homes 1965-03 5.72 pdf=73
FRB6506/p. 853, Mortgages: new homes 1965-04 5.74 pdf=69
FRB6412/p. 1565, Mortgages: new homes 1964-10 5.75 pdf=55
FRB6501/p. 143, Mortgages: new homes 1964-11 5.75 pdf=147
FRB6511/p. 1575, Mortgages: new homes 1965-09 5.75 pdf=75
FRB6512/p. 1753, Mortgages: new homes 1965-10 5.75 pdf=101
FRB6408/p. 1047, Mortgages: new homes 1964-06 5.76 pdf=113
FRB6409/p. 1171, Mortgages: new homes 1964-07 5.76 pdf=63
FRB6502/p. 287, Mortgages: new homes 1964-12 5.76 pdf=79
FRB6508/p. 1135, Mortgages: new homes 1965-06 5.76 pdf=87
FRB6510/p. 1441, Mortgages: new homes 1965-08 5.76 pdf=79
FRB6407/p. 875, Mortgages: new homes 1964-05 5.77 pdf=65
FRB6410/p. 1299, Mortgages: new homes 1964-08 5.77 pdf=69
FRB6411/p. 1451, Mortgages: new homes 1964-09 5.77 pdf=79
FRB6507/p. 991, Mortgages: new homes 1965-05 5.77 pdf=75
FRB6509/p. 1305, Mortgages: new homes 1965-07 5.77 pdf=111
FRB6602/p. 235, Mortgages: new homes 1965-12 5.78 pdf=90
FRB6407/p. 875, Mortgages: new homes 1964-03 5.79 pdf=65
FRB6407/p. 875, Mortgages: new homes 1964-04 5.79 pdf=65
FRB6503/p. 455, Mortgages: new homes 1965-01 5.79 pdf=99
FRB6504/p. 571, Mortgages: new homes 1965-02 5.79 pdf=57
FRB6407/p. 875, Mortgages: new homes 1963-12 5.80 pdf=65
FRB6601/p. 73, Mortgages: new homes 1965-11 5.80 pdf=77
FRB6407/p. 875, Mortgages: new homes 1963-09 5.81 pdf=65
FRB6407/p. 875, Mortgages: new homes 1964-02 5.81 pdf=65
FRB6603/p. 379, Mortgages: new homes 1966-01 5.81 pdf=78
FRB6407/p. 875, Mortgages: new homes 1963-05 5.82 pdf=65
FRB6407/p. 875, Mortgages: new homes 1963-06 5.82 pdf=65
FRB6407/p. 875, Mortgages: new homes 1963-07 5.82 pdf=65
FRB6407/p. 875, Mortgages: new homes 1963-08 5.82 pdf=65
FRB6407/p. 875, Mortgages: new homes 1963-10 5.82 pdf=65
FRB6407/p. 875, Mortgages: new homes 1963-11 5.82 pdf=65
FRB6407/p. 875, Mortgages: new homes 1964-01 5.83 pdf=65
FRB6407/p. 875, Mortgages: new homes 1963-04 5.84 pdf=65
FRB6604/p. 565, Mortgages: new homes 1966-02 5.85 pdf=114
FRB6605/p. 691, Mortgages: new homes 1966-03 5.90 pdf=58
FRB6607/p. 1011, Mortgages: new homes 1966-04 5.99 pdf=79 note=the June 1966 issue (pp. 857-858 missing from FRASER's copy) not read
FRB6607/p. 1011, Mortgages: new homes 1966-05 6.02 pdf=79
FRB6608/p. 1204, Mortgages: new and existing homes 1966-06 6.07 pdf=130
FRB6609/p. 1372, Mortgages: new and existing homes 1966-07 6.12 pdf=95
FRB6610/p. 1492, Mortgages: new and existing homes 1966-08 6.18 pdf=60
FRB6611/p. 1674, Mortgages: new and existing homes 1966-09 6.22 pdf=103
FRB6707/p. 1200, Mortgages: new and existing homes 1967-05 6.28 pdf=128
FRB6708/p. 1394, Mortgages: new and existing homes 1967-06 6.29 pdf=125
FRB6612/p. 1806, Mortgages: new and existing homes 1966-10 6.32 pdf=71
FRB6709/p. 1610, Mortgages: new and existing homes 1967-07 6.34 pdf=143
FRB6710/p. 1780, Mortgages: new and existing homes 1967-08 6.34 pdf=104
FRB6706/p. 1006, Mortgages: new and existing homes 1967-04 6.38 pdf=107
FRB6711/p. 1952, Mortgages: new and existing homes 1967-09 6.38 pdf=100
FRB6712/p. 2104, Mortgages: new and existing homes 1967-10 6.38 pdf=87
FRB6701/p. 114, Mortgages: new and existing homes 1966-11 6.40 pdf=116
FRB6705/p. 816, Mortgages: new and existing homes 1967-03 6.42 pdf=128
FRB6703/p. 420, Mortgages: new and existing homes 1967-01 6.43 pdf=82 note=old series; the Apr. 1967 issue gives 6.47 on the new FHLBB series, from Dec. 1966
FRB6702/p. 272, Mortgages: new and existing homes 1966-12 6.44 pdf=88
FRB6704/p. 622, Mortgages: new and existing homes 1967-02 6.44 pdf=126
"""
# EFF: the FHLBB series' effective rate on conventional first mortgages for new homes ("reflects fees and charges as
# well as contract rates ... and an assumed prepayment at end of 10 years"), from the Apr. 1968 issue, which prints it
# monthly from Feb. 1967; each month after Jan. 1968 marked "p" (preliminary) when first printed.
EFF = """
FRB6804/p. A-30, Mortgages: new and existing homes 1968-02 6.61 pdf=89 note=preliminary
FRB6805/p. A-32, Mortgages: new and existing homes 1968-03 6.64 pdf=96 note=preliminary
FRB6806/p. A-33, Mortgages: new and existing homes 1968-04 6.70 pdf=111 note=preliminary
FRB6807/p. A-33, Mortgages: new and existing homes 1968-05 6.83 pdf=157 note=preliminary
FRB6808/p. A-33, Mortgages: new and existing homes 1968-06 7.03 pdf=81 note=preliminary
FRB6809/p. A-33, Mortgages: new and existing homes 1968-07 7.18 pdf=102 note=preliminary
FRB6810/p. A-33, Mortgages: new and existing homes 1968-08 7.23 pdf=131 note=preliminary
FRB6811/p. A-51, Home-mortgage yields 1968-09 7.23 pdf=112 note=preliminary
FRB6812/p. A-51, Home-mortgage yields 1968-10 7.22 pdf=156 note=preliminary
FRB6901/p. 51, Home-mortgage yields 1968-11 7.21 pdf=142 note=preliminary
FRB6902/p. 51, Home-mortgage yields 1968-12 7.23 pdf=140 note=preliminary
FRB6804/p. A-30, Mortgages: new and existing homes 1967-06 6.35 pdf=89
FRB6804/p. A-30, Mortgages: new and existing homes 1967-05 6.37 pdf=89
FRB6804/p. A-30, Mortgages: new and existing homes 1967-08 6.40 pdf=89
FRB6804/p. A-30, Mortgages: new and existing homes 1967-04 6.43 pdf=89
FRB6804/p. A-30, Mortgages: new and existing homes 1967-07 6.43 pdf=89
FRB6804/p. A-30, Mortgages: new and existing homes 1967-09 6.44 pdf=89
FRB6804/p. A-30, Mortgages: new and existing homes 1967-11 6.45 pdf=89
FRB6804/p. A-30, Mortgages: new and existing homes 1967-03 6.47 pdf=89
FRB6804/p. A-30, Mortgages: new and existing homes 1967-10 6.47 pdf=89
FRB6804/p. A-30, Mortgages: new and existing homes 1968-01 6.52 pdf=89
FRB6804/p. A-30, Mortgages: new and existing homes 1967-02 6.54 pdf=89
FRB6804/p. A-30, Mortgages: new and existing homes 1967-12 6.54 pdf=89
"""

# The money stock, M1 (currency outside banks and demand deposits adjusted), averages of daily figures, seasonally
# adjusted, billions: each year's months as the next January's Report tabled them ("Money supply"; February in 1968),
# its December preliminary. Dec. 1960 and 1961: the Jan. 1962 Report, the series before the Board's revision of Aug.
# 1962; from 1962, the revised series. January's change from the Report's own December before (prior=). Read off the
# page images at 200-240 dpi; each month's currency and demand deposits read with it and found to add to it within 0.1.
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
ERP63/Table C-45, p. 226 1962-09 145.3
ERP63/Table C-45, p. 226 1962-10 146.1
ERP63/Table C-45, p. 226 1962-11 146.9
ERP63/Table C-45, p. 226 1962-12 147.9
ERP64/Table C-45, p. 262 1963-01 148.7 prior=147.9
ERP64/Table C-45, p. 262 1963-02 148.6
ERP64/Table C-45, p. 262 1963-03 148.9
ERP64/Table C-45, p. 262 1963-04 149.4
ERP64/Table C-45, p. 262 1963-05 149.4
ERP64/Table C-45, p. 262 1963-06 149.8
ERP64/Table C-45, p. 262 1963-07 150.7
ERP64/Table C-45, p. 262 1963-08 150.5
ERP64/Table C-45, p. 262 1963-09 150.9
ERP64/Table C-45, p. 262 1963-10 152.0
ERP64/Table C-45, p. 262 1963-11 153.1
ERP64/Table C-45, p. 262 1963-12 153.3
ERP65/Table B-47, p. 246 1964-01 153.8 prior=153.2
ERP65/Table B-47, p. 246 1964-02 153.8
ERP65/Table B-47, p. 246 1964-03 154.2
ERP65/Table B-47, p. 246 1964-04 154.5
ERP65/Table B-47, p. 246 1964-05 154.5
ERP65/Table B-47, p. 246 1964-06 155.6
ERP65/Table B-47, p. 246 1964-07 156.7
ERP65/Table B-47, p. 246 1964-08 157.2
ERP65/Table B-47, p. 246 1964-09 158.0
ERP65/Table B-47, p. 246 1964-10 158.6
ERP65/Table B-47, p. 246 1964-11 159.1
ERP65/Table B-47, p. 246 1964-12 159.4
ERP66/Table C-45, p. 263 1965-01 160.0 prior=159.7
ERP66/Table C-45, p. 263 1965-02 159.7
ERP66/Table C-45, p. 263 1965-03 160.3
ERP66/Table C-45, p. 263 1965-04 161.1
ERP66/Table C-45, p. 263 1965-05 160.0
ERP66/Table C-45, p. 263 1965-06 161.8
ERP66/Table C-45, p. 263 1965-07 162.5
ERP66/Table C-45, p. 263 1965-08 162.7
ERP66/Table C-45, p. 263 1965-09 164.3
ERP66/Table C-45, p. 263 1965-10 165.6
ERP66/Table C-45, p. 263 1965-11 165.7
ERP66/Table C-45, p. 263 1965-12 167.4
ERP67/Table B-46, p. 268 1966-01 168.0 prior=167.2
ERP67/Table B-46, p. 268 1966-02 168.2
ERP67/Table B-46, p. 268 1966-03 169.3
ERP67/Table B-46, p. 268 1966-04 170.9
ERP67/Table B-46, p. 268 1966-05 170.2
ERP67/Table B-46, p. 268 1966-06 171.1
ERP67/Table B-46, p. 268 1966-07 169.6
ERP67/Table B-46, p. 268 1966-08 169.6
ERP67/Table B-46, p. 268 1966-09 170.5
ERP67/Table B-46, p. 268 1966-10 169.6
ERP67/Table B-46, p. 268 1966-11 169.2
ERP67/Table B-46, p. 268 1966-12 170.2
ERP68/Table B-50, p. 268 1967-01 170.3 prior=170.4
ERP68/Table B-50, p. 268 1967-02 171.5
ERP68/Table B-50, p. 268 1967-03 173.1
ERP68/Table B-50, p. 268 1967-04 172.7
ERP68/Table B-50, p. 268 1967-05 174.5
ERP68/Table B-50, p. 268 1967-06 176.2
ERP68/Table B-50, p. 268 1967-07 177.9
ERP68/Table B-50, p. 268 1967-08 179.1
ERP68/Table B-50, p. 268 1967-09 179.2
ERP68/Table B-50, p. 268 1967-10 180.3
ERP68/Table B-50, p. 268 1967-11 181.2
ERP68/Table B-50, p. 268 1967-12 181.5
ERP69/Table B-50, p. 286 1968-01 182.3 prior=181.3
ERP69/Table B-50, p. 286 1968-02 182.7
ERP69/Table B-50, p. 286 1968-03 183.4
ERP69/Table B-50, p. 286 1968-04 184.3
ERP69/Table B-50, p. 286 1968-05 186.1
ERP69/Table B-50, p. 286 1968-06 187.4
ERP69/Table B-50, p. 286 1968-07 189.4
ERP69/Table B-50, p. 286 1968-08 190.3
ERP69/Table B-50, p. 286 1968-09 189.5
ERP69/Table B-50, p. 286 1968-10 190.2
ERP69/Table B-50, p. 286 1968-11 192.0
ERP69/Table B-50, p. 286 1968-12 193.0
"""

# M1 plus time deposits adjusted at commercial banks ("Total money supply and time deposits adjusted"), the same
# Reports and pages; Dec. 1960 and 1961 from the Jan. 1963 Report (the Jan. 1962 Report prints time deposits unadjusted
# only). M1 and time deposits found to add to it within 0.1 in every month. The Jan. 1967 Report's note 5: from June
# 1966, balances accumulated for the payment of personal loans are excluded from time deposits ($1.1 billion).
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
ERP63/Table C-45, p. 226 1962-09 238.7
ERP63/Table C-45, p. 226 1962-10 240.8
ERP63/Table C-45, p. 226 1962-11 242.9
ERP63/Table C-45, p. 226 1962-12 245.3
ERP64/Table C-45, p. 262 1963-01 247.9 prior=245.3
ERP64/Table C-45, p. 262 1963-02 248.9
ERP64/Table C-45, p. 262 1963-03 250.7
ERP64/Table C-45, p. 262 1963-04 252.0
ERP64/Table C-45, p. 262 1963-05 253.1
ERP64/Table C-45, p. 262 1963-06 254.3
ERP64/Table C-45, p. 262 1963-07 256.2
ERP64/Table C-45, p. 262 1963-08 257.3
ERP64/Table C-45, p. 262 1963-09 258.4
ERP64/Table C-45, p. 262 1963-10 260.9
ERP64/Table C-45, p. 262 1963-11 263.8
ERP64/Table C-45, p. 262 1963-12 265.0
ERP65/Table B-47, p. 246 1964-01 267.7 prior=265.5
ERP65/Table B-47, p. 246 1964-02 268.9
ERP65/Table B-47, p. 246 1964-03 269.9
ERP65/Table B-47, p. 246 1964-04 270.9
ERP65/Table B-47, p. 246 1964-05 271.9
ERP65/Table B-47, p. 246 1964-06 274.1
ERP65/Table B-47, p. 246 1964-07 276.1
ERP65/Table B-47, p. 246 1964-08 277.8
ERP65/Table B-47, p. 246 1964-09 279.7
ERP65/Table B-47, p. 246 1964-10 281.7
ERP65/Table B-47, p. 246 1964-11 284.2
ERP65/Table B-47, p. 246 1964-12 285.9
ERP66/Table C-45, p. 263 1965-01 288.8 prior=286.3
ERP66/Table C-45, p. 263 1965-02 290.7
ERP66/Table C-45, p. 263 1965-03 292.4
ERP66/Table C-45, p. 263 1965-04 294.6
ERP66/Table C-45, p. 263 1965-05 294.6
ERP66/Table C-45, p. 263 1965-06 297.7
ERP66/Table C-45, p. 263 1965-07 300.1
ERP66/Table C-45, p. 263 1965-08 302.8
ERP66/Table C-45, p. 263 1965-09 305.9
ERP66/Table C-45, p. 263 1965-10 309.2
ERP66/Table C-45, p. 263 1965-11 311.2
ERP66/Table C-45, p. 263 1965-12 314.3
ERP67/Table B-46, p. 268 1966-01 315.8 prior=314.1
ERP67/Table B-46, p. 268 1966-02 316.7
ERP67/Table B-46, p. 268 1966-03 318.8
ERP67/Table B-46, p. 268 1966-04 322.3
ERP67/Table B-46, p. 268 1966-05 323.2
ERP67/Table B-46, p. 268 1966-06 324.8 note=from June 1966 balances held to repay personal loans excluded from time deposits ($1.1bn)
ERP67/Table B-46, p. 268 1966-07 324.9
ERP67/Table B-46, p. 268 1966-08 326.2
ERP67/Table B-46, p. 268 1966-09 327.6
ERP67/Table B-46, p. 268 1966-10 326.4
ERP67/Table B-46, p. 268 1966-11 326.1
ERP67/Table B-46, p. 268 1966-12 328.2
ERP68/Table B-50, p. 268 1967-01 331.1 prior=329.0
ERP68/Table B-50, p. 268 1967-02 335.0
ERP68/Table B-50, p. 268 1967-03 339.2
ERP68/Table B-50, p. 268 1967-04 340.8
ERP68/Table B-50, p. 268 1967-05 344.4
ERP68/Table B-50, p. 268 1967-06 348.6
ERP68/Table B-50, p. 268 1967-07 352.5
ERP68/Table B-50, p. 268 1967-08 356.3
ERP68/Table B-50, p. 268 1967-09 358.2
ERP68/Table B-50, p. 268 1967-10 361.1
ERP68/Table B-50, p. 268 1967-11 363.7
ERP68/Table B-50, p. 268 1967-12 365.3
ERP69/Table B-50, p. 286 1968-01 366.4 prior=364.8
ERP69/Table B-50, p. 286 1968-02 367.9
ERP69/Table B-50, p. 286 1968-03 370.1
ERP69/Table B-50, p. 286 1968-04 371.4
ERP69/Table B-50, p. 286 1968-05 373.7
ERP69/Table B-50, p. 286 1968-06 375.6
ERP69/Table B-50, p. 286 1968-07 379.8
ERP69/Table B-50, p. 286 1968-08 384.0
ERP69/Table B-50, p. 286 1968-09 386.0
ERP69/Table B-50, p. 286 1968-10 389.8
ERP69/Table B-50, p. 286 1968-11 393.9
ERP69/Table B-50, p. 286 1968-12 397.3
"""

# Free reserves of member banks (excess reserves less borrowings at the Reserve Banks), averages of daily figures,
# millions: each year's months as the next January's Report tabled them ("Federal Reserve Bank credit and member bank
# reserves"; February in 1968), its last one or two months marked preliminary; the change in January from the Report's
# own December before (prior=). Read off the page images at 170-230 dpi; each month's excess reserves and borrowings
# read with it, and the difference found equal to the printed figure in every month.
FREE = """
ERP62/Table B-46, p. 262 1960-12 669
ERP62/Table B-46, p. 262 1961-01 696
ERP62/Table B-46, p. 262 1961-02 517
ERP62/Table B-46, p. 262 1961-03 476
ERP62/Table B-46, p. 262 1961-04 562
ERP62/Table B-46, p. 262 1961-05 453
ERP62/Table B-46, p. 262 1961-06 549
ERP62/Table B-46, p. 262 1961-07 530
ERP62/Table B-46, p. 262 1961-08 537
ERP62/Table B-46, p. 262 1961-09 552
ERP62/Table B-46, p. 262 1961-10 442
ERP62/Table B-46, p. 262 1961-11 509
ERP62/Table B-46, p. 262 1961-12 423
ERP63/Table C-47, p. 228 1962-01 546 prior=419
ERP63/Table C-47, p. 228 1962-02 434
ERP63/Table C-47, p. 228 1962-03 379
ERP63/Table C-47, p. 228 1962-04 441
ERP63/Table C-47, p. 228 1962-05 434
ERP63/Table C-47, p. 228 1962-06 371
ERP63/Table C-47, p. 228 1962-07 443
ERP63/Table C-47, p. 228 1962-08 436
ERP63/Table C-47, p. 228 1962-09 378
ERP63/Table C-47, p. 228 1962-10 419
ERP63/Table C-47, p. 228 1962-11 470
ERP63/Table C-47, p. 228 1962-12 264
ERP64/Table C-47, p. 264 1963-01 384 prior=268
ERP64/Table C-47, p. 264 1963-02 300
ERP64/Table C-47, p. 264 1963-03 271
ERP64/Table C-47, p. 264 1963-04 313
ERP64/Table C-47, p. 264 1963-05 248
ERP64/Table C-47, p. 264 1963-06 141
ERP64/Table C-47, p. 264 1963-07 158
ERP64/Table C-47, p. 264 1963-08 137
ERP64/Table C-47, p. 264 1963-09 92
ERP64/Table C-47, p. 264 1963-10 95
ERP64/Table C-47, p. 264 1963-11 39
ERP64/Table C-47, p. 264 1963-12 178
ERP65/Table B-50, p. 250 1964-01 175 prior=209
ERP65/Table B-50, p. 250 1964-02 89
ERP65/Table B-50, p. 250 1964-03 99
ERP65/Table B-50, p. 250 1964-04 167
ERP65/Table B-50, p. 250 1964-05 82
ERP65/Table B-50, p. 250 1964-06 120
ERP65/Table B-50, p. 250 1964-07 135
ERP65/Table B-50, p. 250 1964-08 83
ERP65/Table B-50, p. 250 1964-09 89
ERP65/Table B-50, p. 250 1964-10 106
ERP65/Table B-50, p. 250 1964-11 -34
ERP65/Table B-50, p. 250 1964-12 171
ERP66/Table C-49, p. 268 1965-01 106 prior=168
ERP66/Table C-49, p. 268 1965-02 36
ERP66/Table C-49, p. 268 1965-03 -75
ERP66/Table C-49, p. 268 1965-04 -105
ERP66/Table C-49, p. 268 1965-05 -180
ERP66/Table C-49, p. 268 1965-06 -182
ERP66/Table C-49, p. 268 1965-07 -174
ERP66/Table C-49, p. 268 1965-08 -134
ERP66/Table C-49, p. 268 1965-09 -155
ERP66/Table C-49, p. 268 1965-10 -149
ERP66/Table C-49, p. 268 1965-11 -82
ERP66/Table C-49, p. 268 1965-12 -11
ERP67/Table B-51, p. 274 1966-01 -44 prior=-2
ERP67/Table B-51, p. 274 1966-02 -107
ERP67/Table B-51, p. 274 1966-03 -246
ERP67/Table B-51, p. 274 1966-04 -268
ERP67/Table B-51, p. 274 1966-05 -352
ERP67/Table B-51, p. 274 1966-06 -352
ERP67/Table B-51, p. 274 1966-07 -358
ERP67/Table B-51, p. 274 1966-08 -390
ERP67/Table B-51, p. 274 1966-09 -368
ERP67/Table B-51, p. 274 1966-10 -431
ERP67/Table B-51, p. 274 1966-11 -222
ERP67/Table B-51, p. 274 1966-12 -161
ERP68/Table B-53, p. 271 1967-01 -16 prior=-165
ERP68/Table B-53, p. 271 1967-02 -4
ERP68/Table B-53, p. 271 1967-03 236
ERP68/Table B-53, p. 271 1967-04 175
ERP68/Table B-53, p. 271 1967-05 269
ERP68/Table B-53, p. 271 1967-06 297
ERP68/Table B-53, p. 271 1967-07 272
ERP68/Table B-53, p. 271 1967-08 298
ERP68/Table B-53, p. 271 1967-09 268
ERP68/Table B-53, p. 271 1967-10 160
ERP68/Table B-53, p. 271 1967-11 270
ERP68/Table B-53, p. 271 1967-12 103
ERP69/Table B-53, p. 289 1968-01 144 prior=107
ERP69/Table B-53, p. 289 1968-02 38
ERP69/Table B-53, p. 289 1968-03 -315
ERP69/Table B-53, p. 289 1968-04 -413
ERP69/Table B-53, p. 289 1968-05 -326
ERP69/Table B-53, p. 289 1968-06 -341
ERP69/Table B-53, p. 289 1968-07 -226
ERP69/Table B-53, p. 289 1968-08 -190
ERP69/Table B-53, p. 289 1968-09 -132
ERP69/Table B-53, p. 289 1968-10 -167
ERP69/Table B-53, p. 289 1968-11 -281
ERP69/Table B-53, p. 289 1968-12 -366
"""

# U.S. reserve assets, end of month, millions: GOLD/CURRENCIES/IMF/TOTAL. 1962-65 from the Reports of Jan. 1964-66,
# "United States gold stock and holdings of convertible foreign currencies by U.S. monetary authorities": the gold stock
# (its total, the Exchange Stabilization Fund's gold included) and the foreign currency holdings, the total of the two;
# no IMF position printed ("-"). 1966-68 from the Reports of Feb. 1968 and Jan. 1969, "United States reserve assets:
# gold stock, holdings of convertible foreign currencies, and reserve position in the International Monetary Fund".
# 1965 is the Jan. 1966 Report's (its gold from Sept. 1965 counts the gold the IMF deposited, $8-34 million; its note 4).
# 1966 is the Feb. 1968 Report's (the Jan. 1967 Report prints no such table). Each month's parts found to add to the
# printed total. Read off the page images at 190-210 dpi.
RES = """
ERP64/Table C-82, p. 303 1962-01 16847/116/-/16963 prior=16947/116/-/17063
ERP64/Table C-82, p. 303 1962-02 16795/153/-/16948
ERP64/Table C-82, p. 303 1962-03 16643/230/-/16873
ERP64/Table C-82, p. 303 1962-04 16519/243/-/16762
ERP64/Table C-82, p. 303 1962-05 16458/260/-/16718
ERP64/Table C-82, p. 303 1962-06 16527/554/-/17081
ERP64/Table C-82, p. 303 1962-07 16182/496/-/16678
ERP64/Table C-82, p. 303 1962-08 16139/423/-/16562
ERP64/Table C-82, p. 303 1962-09 16081/450/-/16531
ERP64/Table C-82, p. 303 1962-10 16026/338/-/16364
ERP64/Table C-82, p. 303 1962-11 16014/202/-/16216
ERP64/Table C-82, p. 303 1962-12 16057/99/-/16156
ERP64/Table C-82, p. 303 1963-01 15974/128/-/16102
ERP64/Table C-82, p. 303 1963-02 15891/132/-/16023
ERP64/Table C-82, p. 303 1963-03 15946/132/-/16078
ERP64/Table C-82, p. 303 1963-04 15914/132/-/16046
ERP64/Table C-82, p. 303 1963-05 15854/155/-/16009
ERP64/Table C-82, p. 303 1963-06 15830/126/-/15956
ERP64/Table C-82, p. 303 1963-07 15677/87/-/15764
ERP64/Table C-82, p. 303 1963-08 15633/92/-/15725
ERP64/Table C-82, p. 303 1963-09 15634/154/-/15788
ERP64/Table C-82, p. 303 1963-10 15640/270/-/15910
ERP64/Table C-82, p. 303 1963-11 15609/171/-/15780
ERP64/Table C-82, p. 303 1963-12 15596/212/-/15808
ERP65/Table B-84, p. 289 1964-01 15540/307/-/15847 prior=15596/212/-/15808
ERP65/Table B-84, p. 289 1964-02 15518/347/-/15865
ERP65/Table B-84, p. 289 1964-03 15550/440/-/15990
ERP65/Table B-84, p. 289 1964-04 15727/264/-/15991
ERP65/Table B-84, p. 289 1964-05 15693/253/-/15946
ERP65/Table B-84, p. 289 1964-06 15623/182/-/15805
ERP65/Table B-84, p. 289 1964-07 15629/211/-/15840
ERP65/Table B-84, p. 289 1964-08 15657/233/-/15890
ERP65/Table B-84, p. 289 1964-09 15643/227/-/15870
ERP65/Table B-84, p. 289 1964-10 15606/96/-/15702
ERP65/Table B-84, p. 289 1964-11 15566/758/-/16324
ERP65/Table B-84, p. 289 1964-12 15471/432/-/15903
ERP66/Table C-82, p. 305 1965-01 15208/364/-/15572 prior=15471/432/-/15903
ERP66/Table C-82, p. 305 1965-02 14993/227/-/15220
ERP66/Table C-82, p. 305 1965-03 14639/490/-/15129
ERP66/Table C-82, p. 305 1965-04 14480/404/-/14884
ERP66/Table C-82, p. 305 1965-05 14362/149/-/14511
ERP66/Table C-82, p. 305 1965-06 14049/546/-/14595
ERP66/Table C-82, p. 305 1965-07 13969/728/-/14697
ERP66/Table C-82, p. 305 1965-08 13916/1037/-/14953
ERP66/Table C-82, p. 305 1965-09 13925/959/-/14884
ERP66/Table C-82, p. 305 1965-10 13937/858/-/14795
ERP66/Table C-82, p. 305 1965-11 13879/807/-/14686
ERP66/Table C-82, p. 305 1965-12 13807/777/-/14584
ERP68/Table B-88, p. 312 1966-01 13811/639/774/15224 prior=13806/781/863/15450
ERP68/Table B-88, p. 312 1966-02 13811/377/774/14962
ERP68/Table B-88, p. 312 1966-03 13738/559/729/15026
ERP68/Table B-88, p. 312 1966-04 13668/522/726/14916
ERP68/Table B-88, p. 312 1966-05 13582/628/695/14905
ERP68/Table B-88, p. 312 1966-06 13529/722/707/14958
ERP68/Table B-88, p. 312 1966-07 13413/1093/642/15148
ERP68/Table B-88, p. 312 1966-08 13319/1299/397/15015
ERP68/Table B-88, p. 312 1966-09 13356/1148/372/14876
ERP68/Table B-88, p. 312 1966-10 13311/1213/356/14880
ERP68/Table B-88, p. 312 1966-11 13262/1108/345/14715
ERP68/Table B-88, p. 312 1966-12 13235/1321/326/14882
ERP68/Table B-88, p. 312 1967-01 13202/645/349/14196
ERP68/Table B-88, p. 312 1967-02 13161/480/357/13998
ERP68/Table B-88, p. 312 1967-03 13184/314/357/13855
ERP68/Table B-88, p. 312 1967-04 13234/315/357/13906
ERP68/Table B-88, p. 312 1967-05 13214/363/366/13943
ERP68/Table B-88, p. 312 1967-06 13169/738/367/14274
ERP68/Table B-88, p. 312 1967-07 13136/719/369/14224
ERP68/Table B-88, p. 312 1967-08 13075/1162/368/14605
ERP68/Table B-88, p. 312 1967-09 13077/1200/372/14649
ERP68/Table B-88, p. 312 1967-10 13039/1509/379/14927
ERP68/Table B-88, p. 312 1967-11 12965/2092/381/15438
ERP68/Table B-88, p. 312 1967-12 12065/2345/420/14830
ERP69/Table B-89, p. 330 1968-01 12003/2176/441/14620 prior=12065/2345/420/14830
ERP69/Table B-89, p. 330 1968-02 11900/2235/655/14790
ERP69/Table B-89, p. 330 1968-03 10703/2746/477/13926
ERP69/Table B-89, p. 330 1968-04 10547/2804/489/13840
ERP69/Table B-89, p. 330 1968-05 10468/3386/494/14348
ERP69/Table B-89, p. 330 1968-06 10681/2479/903/14063
ERP69/Table B-89, p. 330 1968-07 10676/2773/917/14366
ERP69/Table B-89, p. 330 1968-08 10681/2817/929/14427
ERP69/Table B-89, p. 330 1968-09 10755/2953/926/14634
ERP69/Table B-89, p. 330 1968-10 10788/2703/936/14427
ERP69/Table B-89, p. 330 1968-11 10897/3655/1108/15660
ERP69/Table B-89, p. 330 1968-12 10892/3528/1290/15710
"""

# Balances on merchandise trade and on goods and services, quarterly, seasonally adjusted annual rates, millions: as
# the next January's Report tabled them ("United States balance of payments", the quarters under "Seasonally adjusted
# annual rates"; February in 1968). Each Report prints the quarters through the third of the year before, so a fourth
# quarter is the Report of a year later's. MERCHANDISE/GOODS_SERVICES: the balance on goods and services as printed
# (its own column); the merchandise balance computed, merchandise exports less merchandise imports as printed (the
# Reports print no such column). Each quarter's exports less imports of goods and services found equal to the printed
# balance. The quarter before (prior=) from the same table. Read off the page images at 190 dpi. The Jan. 1962 Report
# prints no quarters (1961 by Jan.-Sept. only); the fourth quarter of 1968 is in the Report of Jan. 1970, not read.
# Printed figures, by quarter: exports of goods and services, merchandise exports, imports (as a positive figure, or
# negative from 1969), merchandise imports, balance:
#   ERP63 Table C-78, p. 262: prior (27844, 19944, 21884, 13688, 5960); 1961Q1 28276,20244,21792,13476,6484; 1961Q2 27312,19072,22040,13668,5272; 1961Q3 27564,19760,23708,15360,3856; 1961Q4 29112,20584,24152,15552,4960; 1962Q1 29008,20252,24248,15680,4760; 1962Q2 30660,21356,24912,16128,5748; 1962Q3 29480,20680,25332,16520,4148
#   ERP64 Table C-77, p. 297: prior (30200, 21080, 25128, 16508, 5072); 1962Q4 29696,19700,25364,16184,4332; 1963Q1 29788,19992,25028,16008,4760; 1963Q2 31564,21924,25740,16680,5824; 1963Q3 31964,22156,26724,17616,5240
#   ERP65 Table B-79, p. 282: prior (32148, 22440, 26932, 17472, 5216); 1963Q4 33884,23668,26976,17516,6908; 1964Q1 36000,24448,26992,17464,9008; 1964Q2 35356,24144,28032,18304,7324; 1964Q3 36656,25448,28804,18988,7852
#   ERP66 Table C-78, p. 300: prior (37340, 25528, 28544, 18836, 8796); 1964Q4 38428,26760,29528,19604,8900; 1965Q1 34660,22344,28628,18652,6032; 1965Q2 40368,26992,32388,21876,7980; 1965Q3 40104,27224,32704,22084,7400
#   ERP67 Table B-80, p. 306: prior (40064, 27304, 32980, 22380, 7084); 1965Q4 40260,28108,34160,23024,6100; 1966Q1 41980,28684,35704,24016,6276; 1966Q2 42288,28444,36848,25048,5440; 1966Q3 43792,29756,39048,26636,4744
#   ERP68 Table B-83, p. 306: prior (43652, 29528, 39048, 26320, 4604); 1966Q4 43988,29608,39652,26720,4336; 1967Q1 45444,30704,40016,26648,5428; 1967Q2 45448,30868,40152,26232,5296; 1967Q3 45916,30576,40440,26220,5476
#   ERP69 Table B-84, p. 324: prior (46052, 30504, 40616, 26164, 5436); 1967Q4 45984,29912,42592,28636,3392; 1968Q1 47440,31696,46136,31468,1304; 1968Q2 50228,33300,47860,33280,2368; 1968Q3 52988,35360,49476,34312,3512
GS = """
ERP63/Table C-78, p. 262 1961Q1 6768/6484 prior=6256/5960
ERP63/Table C-78, p. 262 1961Q2 5404/5272
ERP63/Table C-78, p. 262 1961Q3 4400/3856
ERP63/Table C-78, p. 262 1961Q4 5032/4960
ERP63/Table C-78, p. 262 1962Q1 4572/4760
ERP63/Table C-78, p. 262 1962Q2 5228/5748
ERP63/Table C-78, p. 262 1962Q3 4160/4148
ERP64/Table C-77, p. 297 1962Q4 3516/4332 prior=4572/5072
ERP64/Table C-77, p. 297 1963Q1 3984/4760
ERP64/Table C-77, p. 297 1963Q2 5244/5824
ERP64/Table C-77, p. 297 1963Q3 4540/5240
ERP65/Table B-79, p. 282 1963Q4 6152/6908 prior=4968/5216
ERP65/Table B-79, p. 282 1964Q1 6984/9008
ERP65/Table B-79, p. 282 1964Q2 5840/7324
ERP65/Table B-79, p. 282 1964Q3 6460/7852
ERP66/Table C-78, p. 300 1964Q4 7156/8900 prior=6692/8796
ERP66/Table C-78, p. 300 1965Q1 3692/6032
ERP66/Table C-78, p. 300 1965Q2 5116/7980
ERP66/Table C-78, p. 300 1965Q3 5140/7400
ERP67/Table B-80, p. 306 1965Q4 5084/6100 prior=4924/7084
ERP67/Table B-80, p. 306 1966Q1 4668/6276
ERP67/Table B-80, p. 306 1966Q2 3396/5440
ERP67/Table B-80, p. 306 1966Q3 3120/4744
ERP68/Table B-83, p. 306 1966Q4 2888/4336 prior=3208/4604
ERP68/Table B-83, p. 306 1967Q1 4056/5428
ERP68/Table B-83, p. 306 1967Q2 4636/5296
ERP68/Table B-83, p. 306 1967Q3 4356/5476
ERP69/Table B-84, p. 324 1967Q4 1276/3392 prior=4340/5436
ERP69/Table B-84, p. 324 1968Q1 228/1304
ERP69/Table B-84, p. 324 1968Q2 20/2368
ERP69/Table B-84, p. 324 1968Q3 1048/3512
"""

# Ownership of the debt, end of month, billions: TOTAL/TRUST/FED/PRIVATE, as the next January's Report tabled it
# ("Estimated ownership of U.S. Government obligations"; from the Jan. 1969 Report "... of public debt securities",
# the public debt alone, guaranteed issues out and its Government accounts on the new budget's concept): the total, held by
# U.S. Government investment accounts (the trust funds), held by the Federal Reserve Banks, held by private investors
# (the Reports of 1962 and 1963 print "held by the public", the Reserve Banks within it: private is that less the
# Reserve Banks, computed). Each month's parts found to add to the total within 0.1. No column for foreign holders
# (within "miscellaneous investors"). Read off the page images at 210 dpi.
OWN = """
ERP62/Table B-53, p. 270 1961-01 290.2/54.6/26.6/209.0 prior=290.4/55.1/27.4/207.9
ERP62/Table B-53, p. 270 1961-02 290.7/54.5/26.7/209.6
ERP62/Table B-53, p. 270 1961-03 287.7/54.9/26.7/206.1
ERP62/Table B-53, p. 270 1961-04 288.2/54.0/26.8/207.4
ERP62/Table B-53, p. 270 1961-05 290.4/55.5/26.9/208.0
ERP62/Table B-53, p. 270 1961-06 289.2/56.1/27.3/205.8
ERP62/Table B-53, p. 270 1961-07 292.6/55.2/27.4/210.0
ERP62/Table B-53, p. 270 1961-08 294.0/56.5/27.7/209.8
ERP62/Table B-53, p. 270 1961-09 294.0/55.9/27.8/210.3
ERP62/Table B-53, p. 270 1961-10 296.0/55.0/28.3/212.7
ERP62/Table B-53, p. 270 1961-11 297.3/55.4/29.2/212.7
ERP62/Table B-53, p. 270 1961-12 296.5/54.5/28.9/213.1
ERP63/Table C-54, p. 236 1962-01 296.9/53.8/28.5/214.6 prior=296.5/54.5/28.9/213.1
ERP63/Table C-54, p. 236 1962-02 297.4/54.2/28.4/214.8
ERP63/Table C-54, p. 236 1962-03 296.5/54.5/29.1/212.9
ERP63/Table C-54, p. 236 1962-04 297.4/53.7/29.2/214.4
ERP63/Table C-54, p. 236 1962-05 299.6/55.9/29.6/214.1
ERP63/Table C-54, p. 236 1962-06 298.6/56.5/29.7/212.4
ERP63/Table C-54, p. 236 1962-07 298.3/55.5/29.8/213.0
ERP63/Table C-54, p. 236 1962-08 302.3/57.1/30.4/214.9
ERP63/Table C-54, p. 236 1962-09 300.0/56.4/29.8/213.8
ERP63/Table C-54, p. 236 1962-10 302.6/56.1/30.2/216.3
ERP63/Table C-54, p. 236 1962-11 305.9/57.9/30.5/217.5
ERP63/Table C-54, p. 236 1962-12 304.0/55.6/30.8/217.6
ERP64/Table C-54, p. 272 1963-01 303.9/54.5/30.3/219.1 prior=304.0/55.6/30.8/217.6
ERP64/Table C-54, p. 272 1963-02 305.2/55.1/30.6/219.5
ERP64/Table C-54, p. 272 1963-03 303.5/55.1/31.0/217.4
ERP64/Table C-54, p. 272 1963-04 303.7/54.3/31.2/218.2
ERP64/Table C-54, p. 272 1963-05 305.8/57.1/31.3/217.4
ERP64/Table C-54, p. 272 1963-06 306.5/58.4/32.0/216.1
ERP64/Table C-54, p. 272 1963-07 305.5/57.1/32.5/215.9
ERP64/Table C-54, p. 272 1963-08 307.2/58.9/32.4/215.9
ERP64/Table C-54, p. 272 1963-09 307.3/58.3/32.6/216.4
ERP64/Table C-54, p. 272 1963-10 307.1/57.2/32.8/217.2
ERP64/Table C-54, p. 272 1963-11 308.9/57.7/33.7/217.5
ERP64/Table C-54, p. 272 1963-12 310.1/58.1/33.6/218.4
ERP65/Table B-56, p. 256 1964-01 309.3/56.5/32.8/220.0 prior=310.1/58.0/33.6/218.5
ERP65/Table B-56, p. 256 1964-02 311.1/57.5/33.2/220.5
ERP65/Table B-56, p. 256 1964-03 310.4/57.6/33.8/219.0
ERP65/Table B-56, p. 256 1964-04 308.4/56.1/33.2/219.1
ERP65/Table B-56, p. 256 1964-05 312.3/59.4/34.2/218.8
ERP65/Table B-56, p. 256 1964-06 312.5/61.1/34.8/216.6
ERP65/Table B-56, p. 256 1964-07 312.0/59.9/35.1/217.0
ERP65/Table B-56, p. 256 1964-08 314.9/61.8/35.2/218.0
ERP65/Table B-56, p. 256 1964-09 316.5/61.8/35.4/219.3
ERP65/Table B-56, p. 256 1964-10 316.5/60.5/35.7/220.2
ERP65/Table B-56, p. 256 1964-11 319.3/61.2/36.8/221.4
ERP65/Table B-56, p. 256 1964-12 318.7/60.6/37.0/221.1
ERP66/Table C-55, p. 274 1965-01 318.6/59.1/36.7/222.8 prior=318.7/60.6/37.0/221.1
ERP66/Table C-55, p. 274 1965-02 320.6/60.4/36.9/223.3
ERP66/Table C-55, p. 274 1965-03 318.4/60.7/37.6/220.2
ERP66/Table C-55, p. 274 1965-04 317.2/59.2/37.8/220.3
ERP66/Table C-55, p. 274 1965-05 319.8/62.7/38.7/218.5
ERP66/Table C-55, p. 274 1965-06 317.9/63.4/39.1/215.4
ERP66/Table C-55, p. 274 1965-07 317.1/62.3/39.2/215.6
ERP66/Table C-55, p. 274 1965-08 318.7/64.8/39.0/214.9
ERP66/Table C-55, p. 274 1965-09 317.3/63.6/39.8/213.9
ERP66/Table C-55, p. 274 1965-10 319.4/62.3/39.7/217.5
ERP66/Table C-55, p. 274 1965-11 322.2/62.8/40.6/218.8
ERP66/Table C-55, p. 274 1965-12 321.4/61.9/40.8/218.7
ERP67/Table B-57, p. 280 1966-01 322.4/60.0/40.6/221.9 prior=321.4/61.9/40.8/218.7
ERP67/Table B-57, p. 280 1966-02 323.7/61.7/40.2/221.9
ERP67/Table B-57, p. 280 1966-03 321.5/61.7/40.7/219.0
ERP67/Table B-57, p. 280 1966-04 320.1/60.5/40.7/218.9
ERP67/Table B-57, p. 280 1966-05 322.8/64.5/41.5/216.9
ERP67/Table B-57, p. 280 1966-06 320.4/66.7/42.2/211.5
ERP67/Table B-57, p. 280 1966-07 319.8/66.4/42.4/211.0
ERP67/Table B-57, p. 280 1966-08 324.9/69.3/42.5/213.1
ERP67/Table B-57, p. 280 1966-09 325.2/69.2/42.9/213.2
ERP67/Table B-57, p. 280 1966-10 327.4/68.0/43.0/216.4
ERP67/Table B-57, p. 280 1966-11 329.9/68.9/43.9/217.1
ERP67/Table B-57, p. 280 1966-12 329.8/68.8/44.3/216.8
ERP68/Table B-65, p. 286 1967-01 329.4/68.2/43.5/217.6 prior=329.8/68.8/44.3/216.8
ERP68/Table B-65, p. 286 1967-02 330.1/69.6/44.0/216.6
ERP68/Table B-65, p. 286 1967-03 331.5/70.7/44.9/215.9
ERP68/Table B-65, p. 286 1967-04 328.3/70.4/45.5/212.4
ERP68/Table B-65, p. 286 1967-05 331.4/74.6/46.1/210.8
ERP68/Table B-65, p. 286 1967-06 326.7/75.8/46.7/204.2
ERP68/Table B-65, p. 286 1967-07 331.2/75.5/46.8/208.9
ERP68/Table B-65, p. 286 1967-08 336.4/77.2/46.6/212.6
ERP68/Table B-65, p. 286 1967-09 336.4/76.4/46.9/213.1
ERP68/Table B-65, p. 286 1967-10 341.0/75.9/47.4/217.7
ERP68/Table B-65, p. 286 1967-11 345.6/76.2/48.9/220.5
ERP68/Table B-65, p. 286 1967-12 345.2/76.0/49.1/220.1
ERP69/Table B-65, p. 303 1968-01 346.3/71.9/49.1/225.3 prior=344.7/73.1/49.1/222.4
ERP69/Table B-65, p. 303 1968-02 351.6/73.4/49.0/229.2
ERP69/Table B-65, p. 303 1968-03 349.5/72.9/49.7/226.8
ERP69/Table B-65, p. 303 1968-04 347.0/73.2/50.5/223.3
ERP69/Table B-65, p. 303 1968-05 352.3/75.8/50.6/225.9
ERP69/Table B-65, p. 303 1968-06 347.6/76.2/52.2/219.2
ERP69/Table B-65, p. 303 1968-07 351.1/75.6/52.4/223.0
ERP69/Table B-65, p. 303 1968-08 354.4/76.9/53.0/224.4
ERP69/Table B-65, p. 303 1968-09 354.7/76.6/53.3/224.9
ERP69/Table B-65, p. 303 1968-10 357.2/76.2/53.3/227.7
ERP69/Table B-65, p. 303 1968-11 356.9/76.6/53.4/226.9
ERP69/Table B-65, p. 303 1968-12 358.0/76.5/52.9/228.6
"""

# Average length of the marketable interest-bearing public debt, end of month, in months (printed in years and
# months): the Reports of Jan. 1962 and 1963 (1961, 1962) and of Feb. 1968 and Jan. 1969 (1966-67, 1968),
# "Average length and maturity distribution of marketable interest-bearing public debt". Dec. 1960 4 yr 7 mo; Dec.
# 1967 in the 1969 Report 4 yr 1 mo. The Reports of 1964-67 print no such table: 1963-65 (TB lines) from the Treasury
# Bulletin, "Public debt operations" (Table 4, "Maturity Distribution and Average Length of Marketable
# Interest-Bearing Public Debt"), each month as the issue of the month after first printed it, read off FRASER's
# page images at 200 dpi. A month's change is from the month before as first printed, across sources.
MATURITY = """
ERP62/Table B-54, p. 271 1961-01 54 prior=55
ERP62/Table B-54, p. 271 1961-02 54
ERP62/Table B-54, p. 271 1961-03 55
ERP62/Table B-54, p. 271 1961-04 54
ERP62/Table B-54, p. 271 1961-05 54
ERP62/Table B-54, p. 271 1961-06 54
ERP62/Table B-54, p. 271 1961-07 52
ERP62/Table B-54, p. 271 1961-08 53
ERP62/Table B-54, p. 271 1961-09 56
ERP62/Table B-54, p. 271 1961-10 55
ERP62/Table B-54, p. 271 1961-11 56
ERP62/Table B-54, p. 271 1961-12 55
ERP63/Table C-55, p. 237 1962-01 54 prior=55
ERP63/Table C-55, p. 237 1962-02 55
ERP63/Table C-55, p. 237 1962-03 59
ERP63/Table C-55, p. 237 1962-04 58
ERP63/Table C-55, p. 237 1962-05 59
ERP63/Table C-55, p. 237 1962-06 59
ERP63/Table C-55, p. 237 1962-07 58
ERP63/Table C-55, p. 237 1962-08 58
ERP63/Table C-55, p. 237 1962-09 60
ERP63/Table C-55, p. 237 1962-10 59
ERP63/Table C-55, p. 237 1962-11 59
ERP63/Table C-55, p. 237 1962-12 59
TB6302/p. 31, Table 4 1963-01 58 pdf=47
TB6303/p. 28, Table 4 1963-02 58 pdf=46
TB6304/p. 27, Table 4 1963-03 61 pdf=41
TB6305/p. 31, Table 4 1963-04 61 pdf=45
TB6306/p. 28, Table 4 1963-05 61 pdf=42
TB6307/p. 26, Table 4 1963-06 61 pdf=40
TB6308/p. 31, Table 4 1963-07 60 pdf=45
TB6309/p. 27, Table 4 1963-08 60 pdf=45
TB6310/p. 25, Table 4 1963-09 63 pdf=39
TB6311/p. 30, Table 4 1963-10 62 pdf=44
TB6312/p. 27, Table 4 1963-11 62 pdf=41
TB6401/p. 27, Table 4 1963-12 61 pdf=45
TB6402/p. 27, Table 4 1964-01 61 pdf=41
TB6403/p. 24, Table 4 1964-02 61 pdf=38
TB6404/p. 22, Table 4 1964-03 61 pdf=36
TB6405/p. 28, Table 4 1964-04 60 pdf=42
TB6406/p. 24, Table 4 1964-05 61 pdf=38
TB6407/p. 22, Table 4 1964-06 60 pdf=40
TB6408/p. 27, Table 4 1964-07 64 pdf=43
TB6409/p. 23, Table 4 1964-08 64 pdf=37
TB6410/p. 21, Table 4 1964-09 63 pdf=35
TB6411/p. 26, Table 4 1964-10 62 pdf=42
TB6412/p. 23, Table 4 1964-11 61 pdf=37
TB6501/p. 22, Table 4 1964-12 60 pdf=40
TB6502/p. 27, Table 4 1965-01 65 pdf=45
TB6503/p. 24, Table 4 1965-02 64 pdf=38
TB6504/p. 22, Table 4 1965-03 64 pdf=36
TB6505/p. 28, Table 4 1965-04 63 pdf=42
TB6506/p. 24, Table 4 1965-05 64 pdf=38
TB6507/p. 22, Table 4 1965-06 64 pdf=36
TB6508/p. 27, Table 4 1965-07 63 pdf=41
TB6509/p. 23, Table 4 1965-08 63 pdf=37
TB6510/p. 21, Table 4 1965-09 63 pdf=35
TB6511/p. 26, Table 4 1965-10 61 pdf=40
TB6601/p. 22, Table 4 1965-11 60 pdf=36 note=the Dec. 1965 issue's figure illegible in FRASER's copy; as the Jan. 1966 issue printed it
TB6601/p. 22, Table 4 1965-12 60 pdf=36
ERP68/Table B-66, p. 287 1966-01 58
ERP68/Table B-66, p. 287 1966-02 59
ERP68/Table B-66, p. 287 1966-03 59
ERP68/Table B-66, p. 287 1966-04 58
ERP68/Table B-66, p. 287 1966-05 59
ERP68/Table B-66, p. 287 1966-06 59
ERP68/Table B-66, p. 287 1966-07 58
ERP68/Table B-66, p. 287 1966-08 59
ERP68/Table B-66, p. 287 1966-09 58
ERP68/Table B-66, p. 287 1966-10 56
ERP68/Table B-66, p. 287 1966-11 56
ERP68/Table B-66, p. 287 1966-12 55
ERP68/Table B-66, p. 287 1967-01 54
ERP68/Table B-66, p. 287 1967-02 54
ERP68/Table B-66, p. 287 1967-03 53
ERP68/Table B-66, p. 287 1967-04 53
ERP68/Table B-66, p. 287 1967-05 54
ERP68/Table B-66, p. 287 1967-06 55
ERP68/Table B-66, p. 287 1967-07 53
ERP68/Table B-66, p. 287 1967-08 53
ERP68/Table B-66, p. 287 1967-09 52
ERP68/Table B-66, p. 287 1967-10 50
ERP68/Table B-66, p. 287 1967-11 50
ERP68/Table B-66, p. 287 1967-12 49
ERP69/Table B-66, p. 304 1968-01 48 prior=49
ERP69/Table B-66, p. 304 1968-02 49
ERP69/Table B-66, p. 304 1968-03 48
ERP69/Table B-66, p. 304 1968-04 48
ERP69/Table B-66, p. 304 1968-05 49
ERP69/Table B-66, p. 304 1968-06 50
ERP69/Table B-66, p. 304 1968-07 48
ERP69/Table B-66, p. 304 1968-08 50
ERP69/Table B-66, p. 304 1968-09 49
ERP69/Table B-66, p. 304 1968-10 48
ERP69/Table B-66, p. 304 1968-11 49
ERP69/Table B-66, p. 304 1968-12 48
"""

# The computed annual interest rate on the public debt, end of month (percent): the Treasury Bulletin's "Debt
# outstanding", Table 2, "Computed Interest Charge and Computed Interest Rate on Federal Securities", the column
# "Total public debt" under "Computed annual interest rate", each month as the first issue to print it (two months
# after, to Oct. 1961; one month after, mostly, from then). Read off FRASER's page images at 200 dpi, or, for 38
# months, from the issue's text layer where it agrees with every later issue's (two or more). Revised once: Dec. 1964,
# 3.602 in the Jan. 1965 issue, 3.593 ("r") from the Feb. 1965 issue (prior= the figure the next issue printed).
TBRATE = """
TB6003/p. 20, Table 2 1960-01 3.334 pdf=32
TB6004/p. 20, Table 2 1960-02 3.378 pdf=32
TB6005/p. 25, Table 2 1960-03 3.336 pdf=37
TB6006/p. 20, Table 2 1960-04 3.325 pdf=34
TB6007/p. 20, Table 2 1960-05 3.327 pdf=32
TB6008/p. 25, Table 2 1960-06 3.297 pdf=37
TB6009/p. 21, Table 2 1960-07 3.260 pdf=35
TB6010/p. 21, Table 2 1960-08 3.179 pdf=35
TB6011/p. 26, Table 2 1960-09 3.171 pdf=38
TB6012/p. 21, Table 2 1960-10 3.167 pdf=33
TB6101/p. 21, Table 2 1960-11 3.143 pdf=33
TB6102/p. 26, Table 2 1960-12 3.137 pdf=38
TB6103/p. 21, Table 2 1961-01 3.118 pdf=33
TB6104/p. 21, Table 2 1961-02 3.081 pdf=35
TB6105/p. 26, Table 2 1961-03 3.109 pdf=44
TB6106/p. 21, Table 2 1961-04 3.091 pdf=33
TB6107/p. 22, Table 2 1961-05 3.075 pdf=38
TB6108/p. 27, Table 2 1961-06 3.072 pdf=41
TB6109/p. 22, Table 2 1961-07 3.065 pdf=38
TB6110/p. 22, Table 2 1961-08 3.082 pdf=40
TB6111/p. 27, Table 2 1961-09 3.096 pdf=41
TB6111/p. 27, Table 2 1961-10 3.098 pdf=41
TB6112/p. 22, Table 2 1961-11 3.123 pdf=36
TB6201/p. 22, Table 2 1961-12 3.135 pdf=36
TB6202/p. 27, Table 2 1962-01 3.155 pdf=41
TB6203/p. 22, Table 2 1962-02 3.180 pdf=38
TB6204/p. 22, Table 2 1962-03 3.209 pdf=36
TB6205/p. 27, Table 2 1962-04 3.215 pdf=41
TB6206/p. 22, Table 2 1962-05 3.236 pdf=36
TB6207/p. 22, Table 2 1962-06 3.239 pdf=36
TB6208/p. 29, Table 2 1962-07 3.247 pdf=47
TB6209/p. 27, Table 2 1962-08 3.262 pdf=43
TB6210/p. 25, Table 2 1962-09 3.284 pdf=39
TB6211/p. 30, Table 2 1962-10 3.277 pdf=46
TB6212/p. 27, Table 2 1962-11 3.288 pdf=45
TB6301/p. 25, Table 2 1962-12 3.297 pdf=41
TB6302/p. 30, Table 2 1963-01 3.299 pdf=46
TB6303/p. 27, Table 2 1963-02 3.304 pdf=45
TB6304/p. 26, Table 2 1963-03 3.332 pdf=40
TB6305/p. 30, Table 2 1963-04 3.337 pdf=44
TB6306/p. 27, Table 2 1963-05 3.344 pdf=41
TB6307/p. 25, Table 2 1963-06 3.360 pdf=39
TB6308/p. 30, Table 2 1963-07 3.374 pdf=44
TB6309/p. 26, Table 2 1963-08 3.402 pdf=44
TB6310/p. 24, Table 2 1963-09 3.428 pdf=38
TB6311/p. 29, Table 2 1963-10 3.460 pdf=43
TB6312/p. 26, Table 2 1963-11 3.476 pdf=40
TB6401/p. 26, Table 2 1963-12 3.486 pdf=44
TB6402/p. 26, Table 2 1964-01 3.506 pdf=40
TB6403/p. 23, Table 2 1964-02 3.531 pdf=37
TB6404/p. 21, Table 2 1964-03 3.537 pdf=35
TB6405/p. 27, Table 2 1964-04 3.546 pdf=41
TB6406/p. 23, Table 2 1964-05 3.554 pdf=37
TB6407/p. 21, Table 2 1964-06 3.560 pdf=39
TB6408/p. 26, Table 2 1964-07 3.565 pdf=42
TB6409/p. 22, Table 2 1964-08 3.565 pdf=36
TB6410/p. 20, Table 2 1964-09 3.567 pdf=34
TB6411/p. 25, Table 2 1964-10 3.572 pdf=41
TB6412/p. 22, Table 2 1964-11 3.576 pdf=36
TB6501/p. 21, Table 2 1964-12 3.602 pdf=39 note=revised to 3.593 ("r") in the Feb. 1965 issue
TB6502/p. 26, Table 2 1965-01 3.626 prior=3.593 pdf=44
TB6503/p. 23, Table 2 1965-02 3.649 pdf=37
TB6504/p. 21, Table 2 1965-03 3.657 pdf=35
TB6505/p. 27, Table 2 1965-04 3.668 pdf=41
TB6506/p. 23, Table 2 1965-05 3.672 pdf=37
TB6507/p. 21, Table 2 1965-06 3.678 pdf=35
TB6508/p. 26, Table 2 1965-07 3.675 pdf=40
TB6509/p. 22, Table 2 1965-08 3.683 pdf=36
TB6510/p. 20, Table 2 1965-09 3.688 pdf=34
TB6511/p. 25, Table 2 1965-10 3.702 pdf=39
TB6512/p. 22, Table 2 1965-11 3.730 pdf=36
TB6601/p. 21, Table 2 1965-12 3.756 pdf=35
TB6602/p. 26, Table 2 1966-01 3.793 pdf=40
TB6603/p. 24, Table 2 1966-02 3.861 pdf=38
TB6604/p. 22, Table 2 1966-03 3.941 pdf=36
TB6605/p. 28, Table 2 1966-04 3.919 pdf=42
TB6606/p. 24, Table 2 1966-05 3.967 pdf=36
TB6607/p. 23, Table 2 1966-06 3.988 pdf=35
TB6608/p. 28, Table 2 1966-07 3.996 pdf=42
TB6609/p. 24, Table 2 1966-08 4.080 pdf=38
TB6610/p. 22, Table 2 1966-09 4.125 pdf=36
TB6611/p. 28, Table 2 1966-10 4.174 pdf=42
TB6612/p. 24, Table 2 1966-11 4.222 pdf=38
TB6701/p. 23, Table 2 1966-12 4.225 pdf=35
TB6702/p. 29, Table 2 1967-01 4.211 pdf=43
TB6703/p. 24, Table 2 1967-02 4.210 pdf=38
TB6704/p. 22, Table 2 1967-03 4.163 pdf=34
TB6705/p. 31, Table 2 1967-04 4.114 pdf=45
TB6706/p. 24, Table 2 1967-05 4.080 pdf=36
TB6707/p. 22, Table 2 1967-06 4.039 pdf=36
TB6708/p. 30, Table 2 1967-07 4.063 pdf=38
TB6709/p. 39, Table 2 1967-08 4.109 pdf=53
TB6710/p. 28, Table 2 1967-09 4.137 pdf=35
TB6711/p. 35, Table 2 1967-10 4.177 pdf=43
TB6712/p. 30, Table 2 1967-11 4.258 pdf=36
TB6801/p. 28, Table 2 1967-12 4.292 pdf=35
TB6802/p. 22, Table 2 1968-01 4.322 pdf=28
TB6803/p. 20, Table 2 1968-02 4.366 pdf=24
TB6804/p. 17, Table 2 1968-03 4.371 pdf=21
TB6805/p. 24, Table 2 1968-04 4.395 pdf=29
TB6806/p. 18, Table 2 1968-05 4.480 pdf=23
TB6807/p. 16, Table 2 1968-06 4.499 pdf=28
TB6808/p. 23, Table 2 1968-07 4.521 pdf=35
TB6809/p. 18, Table 2 1968-08 4.557 pdf=22
TB6810/p. 16, Table 2 1968-09 4.551 pdf=26
TB6811/p. 23, Table 2 1968-10 4.565 pdf=33
TB6812/p. 19, Table 2 1968-11 4.595 pdf=31
TB6901/p. 18, Table 2 1968-12 4.632 pdf=30
"""

# Exchange rates: the Federal Reserve Bulletin's table "Foreign exchange rates" ("Averages of certified noon buying
# rates in New York for cable transfers", in cents a unit of the currency), each month as the issue of the month after
# first printed it (the Aug. 1961, Sept. 1963 and Dec. 1965 issues added two months: their first months are the issues
# before). Columns: the issue, its PDF page on FRASER and printed page (the Apr. 1968 issue's page number is
# illegible), the month, the pound, the deutsche mark, the franc. Read from each issue's text layer and held against
# every later issue that reprints the month (eight to thirteen readings a month, all agreeing but for the text layer's
# misreadings); where the first issue's text failed or disagreed, read by eye off its page image at 150 dpi: every such
# month but four (Oct. 1966, the pound; Apr., June and July 1968, the mark: the next issues' figure, which every later
# issue repeats). The first printings were revised once: Nov. 1960, the pound, 281.36 in the Dec. 1960 issue, 281.35
# in every issue after (FX_PRIOR gives the later figure as the change's base). The Feb. 1964 issue labels its Jan.
# 1964 row "1964-Dec." (a misprint).
FX = """
#  issue  pdf   page  period   pound   mark    franc
1960-02  132    249  1960-01  279.98  23.975  20.366
1960-03   94    349  1960-02  280.33  23.977  20.369
1960-04  102    459  1960-03  280.59  23.978  20.376
1960-05  131    595  1960-04  280.95  23.978  20.384
1960-06  112    715  1960-05  280.60  23.978  20.396
1960-07  106    831  1960-06  280.27  23.980  20.401
1960-08  126    965  1960-07  280.84  23.979  20.404
1960-09  116   1087  1960-08  281.02  23.978  20.404
1960-10  116   1209  1960-09  281.27  23.978  20.404
1960-11   97   1311  1960-10  281.16  23.968  20.375
1960-12  109   1427  1960-11  281.36  23.974  20.402
1961-01  123    121  1960-12  280.74  23.973  20.387
1961-02  131    257  1961-01  280.64  23.968  20.401
1961-03  120    383  1961-02  279.99  23.966  20.402
1961-04  115    505  1961-03  279.75  25.020  20.404
1961-05  129    639  1961-04  279.81  25.185  20.400
1961-06   97    741  1961-05  279.40  25.184  20.404
1961-07  133    883  1961-06  278.98  25.166  20.405
1961-08  133   1021  1961-07  278.74  25.127  20.405
1961-09   98   1125  1961-08  280.29  25.046  20.352
1961-10  136   1267  1961-09  281.22  25.019  20.331
1961-11  103   1375  1961-10  281.54  25.016  20.337
1961-12  113   1495  1961-11  281.49  24.987  20.364
1962-01  124    123  1961-12  280.96  25.004  20.399
1962-02  134    263  1962-01  281.10  25.028  20.403
1962-03  113    381  1962-02  281.46  25.011  20.402
1962-04  118    505  1962-03  281.53  25.012  20.405
1962-05  162    673  1962-04  281.40  25.006  20.405
1962-06  100    779  1962-05  281.21  25.009  20.405
1962-07  135    921  1962-06  280.83  25.039  20.405
1962-08  166   1093  1962-07  280.66  25.084  20.405
1962-09  153   1251  1962-08  280.38  25.020  20.405
1962-10  120   1377  1962-09  280.09  24.996  20.405
1962-11  158   1541  1962-10  280.13  24.963  20.405
1962-12  168   1715  1962-11  280.19  24.947  20.405
1963-01  109    107  1962-12  280.33  25.031  20.404
1963-02  181    293  1963-01  280.48  24.966  20.405
1963-03  115    413  1963-02  280.34  24.985  20.405
1963-04  155    573  1963-03  280.06  25.023  20.405
1963-05  163    741  1963-04  280.07  25.045  20.405
1963-06  127    873  1963-05  279.96  25.090  20.405
1963-07  150   1030  1963-06  280.02  25.121  20.405
1963-08  145   1182  1963-07  280.08  25.109  20.405
1963-09  150   1340  1963-08  279.96  25.101  20.405
1963-10  140   1486  1963-09  279.77  25.121  20.404
1963-11  125   1618  1963-10  279.78  25.137  20.400
1963-12  114   1740  1963-11  279.78  25.154  20.405
1964-01  134    132  1963-12  279.65  25.165  20.404
1964-02  129    268  1964-01  279.83  25.148  20.402
1964-03  141    416  1964-02  279.69  25.169  20.403
1964-04  118    540  1964-03  279.81  25.163  20.404
1964-05  115    662  1964-04  279.90  25.160  20.405
1964-06  133    802  1964-05  279.94  25.159  20.405
1964-07  117    928  1964-06  279.42  25.165  20.401
1964-08  167   1102  1964-07  278.97  25.159  20.405
1964-09  116   1224  1964-08  278.66  25.152  20.405
1964-10  135   1365  1964-09  278.34  25.154  20.402
1964-11  130   1503  1964-10  278.35  25.158  20.403
1964-12  106   1617  1964-11  278.48  25.148  20.405
1965-01  207    203  1964-12  279.06  25.149  20.405
1965-02  142    351  1965-01  279.13  25.135  20.404
1965-03  152    509  1965-02  279.51  25.137  20.404
1965-04  122    637  1965-03  279.24  25.144  20.400
1965-05  134    777  1965-04  279.62  25.149  20.401
1965-06  125    909  1965-05  279.71  25.097  20.397
1965-07  127   1043  1965-06  279.23  25.003  20.405
1965-08  140   1189  1965-07  279.10  24.960  20.405
1965-09  163   1357  1965-08  279.08  24.923  20.403
1965-10  130   1493  1965-09  279.67  24.934  20.400
1965-11  144   1645  1965-10  280.31  24.968  20.393
1965-12  152   1805  1965-11  280.37  24.997  20.403
1966-01  139    136  1965-12  280.21  24.992  20.402
1966-02  148    294  1966-01  280.39  24.926  20.399
1966-03  141    444  1966-02  280.25  24.904  20.401
1966-04  173    624  1966-03  279.52  24.914  20.402
1966-05  125    758  1966-04  279.34  24.902  20.403
1966-06  157    926  1966-05  279.23  24.894  20.402
1966-07  134   1066  1966-06  278.98  24.963  20.403
1966-08  196   1270  1966-07  278.88  25.046  20.403
1966-09  151   1428  1966-08  278.88  25.056  20.394
1966-10  134   1566  1966-09  278.93  25.069  20.314
1966-11  158   1730  1966-10  279.16  25.109  20.247
1966-12  126   1862  1966-11  279.11  25.150  20.231
1967-01  179    178  1966-12  279.01  25.169  20.199
1967-02  147    332  1967-01  279.10  25.140  20.199
1967-03  152    490  1967-02  279.41  25.168  20.217
1967-04  186    682  1967-03  279.63  25.165  20.203
1967-05  204    892  1967-04  279.92  25.167  20.227
1967-06  165   1064  1967-05  279.69  25.147  20.319
1967-07  189   1262  1967-06  279.12  25.122  20.375
1967-08  193   1462  1967-07  278.73  24.996  20.395
1967-09  202   1670  1967-08  278.53  24.985  20.386
1967-10  169   1846  1967-09  278.37  24.988  20.382
1967-11  157   2010  1967-10  278.32  24.974  20.393
1967-12  144   2162  1967-11  266.18  25.072  20.401
1968-01  185   A-86  1967-12  240.63  25.094  20.381
1968-02  252   A-86  1968-01  240.91  24.974  20.307
1968-03  181   A-88  1968-02  240.92  24.987  20.315
1968-04  145      -  1968-03  239.97  25.067  20.316
1968-05  162   A-88  1968-04  240.18  25.093  20.290
1968-06  168   A-90  1968-05  238.92  25.119  20.212
1968-07  214   A-90  1968-06  238.46  25.032  20.107
1968-08  146   A-90  1968-07  239.00  24.945  20.107
1968-09  159   A-90  1968-08  239.11  24.919  20.105
1968-10  188   A-90  1968-09  238.74  25.166  20.106
1968-11  159   A-90  1968-10  238.97  25.120  20.104
1968-12  195   A-90  1968-11  238.58  25.153  20.121
1969-01  181   A-90  1968-12  238.42  25.032  20.199
"""
FX_PRIOR = {('fx-sterling', '1960-12'): 281.35}     # the month before as the same issue printed it, where revised
FX_NOTES = {      # the issue's own footnote or note on the month, as printed there
    ('fx-franc', '1960-01'): 'new franc of 100 old francs introduced Jan. 1, 1960',
    ('fx-mark', '1961-03'): 'par value changed Mar. 5, 1961, from 4.20 to 4.00 marks per U.S. dollar',
    ('fx-franc', '1963-01'): 'the franc again the French monetary unit from Jan. 1, 1963, at 1 to 1 for the new franc',
    ('fx-sterling', '1967-11'): 'pound devalued Nov. 18, 1967; no quotations Nov. 21',
    ('fx-sterling', '1968-03'): 'no quotations Mar. 15, 1968',
}


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
        pdf = None
        m = re.search(r' pdf=(\d+)$', line)
        if m:
            line, pdf = line[:m.start()], m.group(1)
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
        out[p] = {'v': val(v), 'src': key, 'where': where, 'prior': val(prior) if prior else None, 'note': note,
                  'pdf': pdf}
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
        if url and x.get('pdf'):
            url = f"{url}#page={x['pdf']}"
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
    for sid, block, name, label in (
            ('mortgage-fha', FHA, 'FHA new-home mortgage yield',
             'Federal Housing Administration: yield on FHA-insured new-home mortgages, secondary market'),
            ('mortgage-conventional', CONV, 'Conventional mortgage rate, new homes (FHLBB, contract)',
             'Federal Home Loan Bank Board: contract interest rate on conventional first mortgages, new homes'),
            ('mortgage-conventional-eff', EFF, 'Conventional mortgage rate, new homes (FHLBB, effective)',
             'Federal Home Loan Bank Board: effective rate on conventional first mortgages, new homes')):
        if not want(sid):
            continue
        fr = first_rows(parse(block), 'percent', 'pts')
        for p, r in fr.items():         # the change from the month before as first printed: not across the new
            b = fr.get(prev(p))          # FHLBB series (Feb. 1967) or a misprint
            if 'chg' in r or b is None or (sid, p) == ('mortgage-conventional', '1967-02') \
                    or 'corrected' in (r.get('note') or '') + (b.get('note') or ''):
                continue
            r['chg'] = round(r['first'] - b['first'], 2)
        rows = [dict(p=p, **fr[p]) for p in MONTHS if p in fr]
        write(sid, {'id': sid, 'name': name, 'freq': 'M', 'manual': True, 'kind': 'rate', 'change': 'pts',
                    'then': {'label': label, 'unit': 'percent'}, 'now': None}, rows)


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
    if want('free-reserves'):
        now = fred_month('NFORBRES', 1000)          # FRED's copy of the H.3 figure, billions
        if now is None and h3:
            tr, rq, br = h3['RESTR14A_N.M'], h3['RESRQ14A_N.M'], h3['RESBR14A_N.M']
            now = {p: tr[p] - rq[p] - br[p] for p in tr if p in rq and p in br}
        monthly('free-reserves', {'id': 'free-reserves', 'name': 'Free reserves, member banks', 'freq': 'M', 'manual': True,
                                  'change': 'diff',
                                  'then': {'label': 'Board of Governors: member banks\' excess reserves less their borrowings at the Reserve Banks, averages of daily figures', 'unit': 'millions of dollars'},
                                  'now': {'label': 'Board of Governors, H.3 (historical): total reserves less required reserves, less borrowings from the Federal Reserve, not seasonally adjusted',
                                          'unit': 'millions of dollars',
                                          'source': 'FRED NFORBRES (Board of Governors, H.3; the same as its total less required reserves, less borrowings)',
                                          'url': FRED + 'NFORBRES'}},
                first_rows(parse(FREE), 'millions of dollars', 'diff'), now, change='diff', nd=0)
    if h6 and want('money-m2'):
        m2 = h6['M2.M']
        rows = []
        for p in MSPAN:
            v, b = m2.get(p), m2.get(prev(p))
            row = {'p': p, 'now': v}
            if v is not None and b is not None:
                row['chg_now'] = round(100 * (v / b - 1), 1)
            rows.append(row)
        write('money-m2', {'id': 'money-m2', 'name': 'Money stock, M2 (today)', 'freq': 'M', 'change': 'pct', 'then': None,
                           'now': {'label': 'Board of Governors, H.6: M2, seasonally adjusted, monthly average', 'unit': 'billions of dollars',
                                   'source': 'Board of Governors, H.6 (Data Download Program, M2.M; FRED M2SL)', 'url': FRED + 'M2SL'}}, rows)


def fred_month(sid, scale=1):
    """{YYYY-MM: value} from FRED (None where FRED does not answer)."""
    d = fred(sid)
    return None if d is None else {k[:7]: v * scale for k, v in d.items()}


def international():
    """Reserve assets as the Reports tabled them; today the IMF's reserves less gold (FRED TRESEGUSM052N)."""
    if want('reserve-assets'):
        now = fred_month('TRESEGUSM052N')
        if now is None:
            print('FRED did not answer for TRESEGUSM052N')
        rows = []
        first = first_rows(parse(RES, ['gold', 'currencies', 'imf', 'total']), 'millions of dollars', 'diff', total='total')
        for p in MSPAN:
            row = {'p': p}
            row.update(first.get(p, {}))
            if now and now.get(p) is not None:
                row['now'] = round(now[p], 1)
                if now.get(prev(p)) is not None:
                    row['chg_now'] = round(now[p] - now[prev(p)], 1)
            if len(row) > 1:
                rows.append(row)
        write('reserve-assets', {'id': 'reserve-assets', 'name': 'U.S. reserve assets', 'freq': 'M', 'manual': True,
                                 'change': 'diff', 'fields': ['gold', 'currencies', 'imf', 'total'],
                                 'then': {'label': 'Treasury and Board of Governors: gold stock, convertible foreign currencies held by the Treasury and the Federal Reserve, and (from the Feb. 1968 Report) the reserve position in the IMF, end of month', 'unit': 'millions of dollars'},
                                 'now': {'label': 'IMF, International Financial Statistics: total reserves excluding gold, United States, end of month', 'unit': 'millions of dollars',
                                         'source': 'FRED TRESEGUSM052N', 'url': FRED + 'TRESEGUSM052N'}}, rows)


def quarterly_fred(sid, scale):
    d = fred(sid)
    return None if d is None else {f'{k[:4]}Q{(int(k[5:7]) - 1) // 3 + 1}': v * scale for k, v in d.items()}


def balances():
    """The balances on merchandise and on goods and services, quarterly, as the Reports tabled them; today BEA's (FRED
    BOPBM, BOPBGS: quarterly, billions, seasonally adjusted, discontinued), at annual rates (times four)."""
    if not want('goods-services'):
        return
    m, g = quarterly_fred('BOPBM', 4000), quarterly_fred('BOPBGS', 4000)
    first = first_rows(parse(GS, ['merchandise', 'goods_services']), 'millions of dollars, annual rate', 'diff', total='goods_services')
    rows = []
    for q in [f'{y}Q{n}' for y in range(1961, 1969) for n in range(1, 5)]:
        row = {'p': q}
        row.update(first.get(q, {}))
        if m and g and q in m and q in g:
            row['now'] = {'merchandise': round(m[q]), 'goods_services': round(g[q])}
            if prev(q) in g:
                row['chg_now'] = round(g[q] - g[prev(q)])
        if len(row) > 1:
            rows.append(row)
    write('goods-services', {'id': 'goods-services', 'name': 'Balances on trade and on goods and services', 'freq': 'Q', 'manual': True,
                             'change': 'diff', 'fields': ['merchandise', 'goods_services'],
                             'then': {'label': 'Commerce, Office of Business Economics: merchandise exports less imports, and the balance on goods and services, seasonally adjusted annual rates', 'unit': 'millions of dollars, annual rate'},
                             'now': {'label': 'BEA, international transactions (discontinued on FRED): balance on merchandise trade and on goods and services, seasonally adjusted, quarterly, times four',
                                     'unit': 'millions of dollars, annual rate', 'source': 'FRED BOPBM, BOPBGS (times four)', 'url': FRED + 'BOPBGS'}}, rows)


def costs():
    """Unit labor costs and hourly compensation, nonfarm business, today only (FRED ULCNFB, COMPNFB): no contemporary
    printing read (notes/leads.md)."""
    for sid, fid, name, label in (
            ('unit-labor-cost', 'ULCNFB', 'Unit labor costs, nonfarm business (today)',
             'BLS, Productivity and Costs: nonfarm business sector, unit labor costs, index, seasonally adjusted'),
            ('compensation-hour', 'COMPNFB', 'Compensation per hour, nonfarm business (today)',
             'BLS, Productivity and Costs: nonfarm business sector, hourly compensation, index, seasonally adjusted')):
        if not want(sid):
            continue
        d = quarterly_fred(fid, 1)
        if d is None:
            print('FRED did not answer for', fid)
            continue
        rows = []
        for q in ['1960Q4'] + [f'{y}Q{n}' for y in range(1961, 1969) for n in range(1, 5)]:
            v, b = d.get(q), d.get(prev(q))
            row = {'p': q, 'now': round(v, 1)}
            if b:
                row['chg_now'] = round(100 * ((v / b) ** 4 - 1), 1)
            rows.append(row)
        write(sid, {'id': sid, 'name': name, 'freq': 'Q', 'change': 'pct_ar', 'then': None,
                    'now': {'label': label, 'unit': '2017=100', 'source': f'FRED {fid}', 'url': FRED + fid}}, rows)


def debt():
    """The ownership and the average length of the debt, as the Reports tabled them; no figure today."""
    if want('debt-ownership'):
        first = first_rows(parse(OWN, ['total', 'trust', 'fed', 'private']), 'billions of dollars', None)
        write('debt-ownership', {'id': 'debt-ownership', 'name': 'Ownership of the federal debt', 'freq': 'M', 'manual': True,
                                 'change': 'none', 'fields': ['fed', 'trust', 'private', 'total'],
                                 'then': {'label': 'Treasury: the public debt and guaranteed issues (from the Jan. 1969 Report the public debt alone) by holder, end of month, par values', 'unit': 'billions of dollars'},
                                 'now': None}, [dict(p=p, **first[p]) for p in MSPAN if p in first])
    if want('debt-interest-rate'):
        first = first_rows(parse(TBRATE), 'percent', None)
        read = parse(TBRATE)
        for p, r in first.items():
            b = read[p]['prior'] if read[p]['prior'] is not None else (first.get(prev(p)) or {}).get('first')
            if b is not None:
                r['chg'] = round(r['first'] - b, 3)
        write('debt-interest-rate', {'id': 'debt-interest-rate', 'name': 'Average interest rate on the public debt', 'freq': 'M',
                                     'manual': True, 'change': 'pts',
                                     'then': {'label': 'Treasury: computed annual interest rate on the interest-bearing public debt, end of month', 'unit': 'percent'},
                                     'now': None}, [dict(p=p, **first[p]) for p in MONTHS if p in first])
    if want('debt-maturity'):
        first = first_rows(parse(MATURITY), 'months', 'diff')
        for p, r in first.items():
            b = first.get(prev(p))
            if 'chg' not in r and b is not None:
                r['chg'] = r['first'] - b['first']
        write('debt-maturity', {'id': 'debt-maturity', 'name': 'Average length of the marketable debt', 'freq': 'M', 'manual': True,
                                'change': 'diff',
                                'then': {'label': 'Treasury: average length of the marketable interest-bearing public debt, end of month, years and months', 'unit': 'months'},
                                'now': None}, [dict(p=p, **first[p]) for p in MSPAN if p in first])


def fx():
    """The pound, the mark and the franc as the Federal Reserve Bulletin first printed them (FX above): one figure,
    not revised; its change from the month before in cents."""
    cols = ('fx-sterling', 'fx-mark', 'fx-franc')
    meta = {'fx-sterling': ('Pound sterling', 'pound'), 'fx-mark': ('Deutsche mark', 'deutsche mark'),
            'fx-franc': ('French franc', 'franc (new franc, 1960-62)')}
    read = {}
    for line in FX.strip().split('\n'):
        if line.startswith('#'):
            continue
        iss, pdf, page, p, *vals = line.split()
        y, m = int(iss[:4]), int(iss[5:7])
        url = f'https://fraser.stlouisfed.org/files/docs/publications/FRB/1960s/frb_{m:02d}{y}.pdf#page={pdf}'
        where = f'p. {page}, ' if page != '-' else ''
        for sid, v in zip(cols, vals):
            read.setdefault(sid, {})[p] = {
                'first': float(v), 'released': iss, 'unit': 'cents per unit',
                'source': f'Federal Reserve Bulletin, {MON[m - 1]} {y}, {where}Foreign exchange rates; {url}'}
    for sid in cols:
        if not want(sid):
            continue
        rows = []
        for p in MONTHS:
            r = read[sid].get(p)
            if r is None:
                continue
            row = dict(p=p, **r)
            b = FX_PRIOR.get((sid, p)) or (read[sid].get(prev(p)) or {}).get('first')
            if b is not None:
                row['chg'] = round(r['first'] - b, 3)
            if (sid, p) in FX_NOTES:
                row['note'] = FX_NOTES[(sid, p)]
            rows.append(row)
        name, cur = meta[sid]
        write(sid, {'id': sid, 'name': name, 'freq': 'M', 'manual': True, 'kind': 'fx', 'change': 'diff',
                    'then': {'label': f'Federal Reserve Bulletin: noon buying rate in New York for cable transfers, the {cur}, monthly average',
                             'unit': 'cents per unit'},
                    'now': None}, rows)


if __name__ == '__main__':
    rates()
    money()
    international()
    balances()
    costs()
    debt()
    fx()
