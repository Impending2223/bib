"""Figures read by eye from the Clerk's page images, where the OCR did not settle: elections/readings/<year>.yaml.

These replace the OCR in make_elections.py. Each file:

    year: 1972
    notes: >-                        what was read whole, and anything general
    races:
      h NY 9:                        chamber (h, s), State, seat: the district (0 at large) or Senate class;
                                     'h NM 0-1' is New Mexico's at-large position 1 (1962); 's OR 2 special'
                                     a special election (needed where a regular race is held for the same seat)
        cands:
        - [Name as printed, Party as printed, 123456]
        - [Name, 'Democrat, Liberal', 141323, [[Democrat, 47371], [Liberal, 9965]]]   # fusion: total, then lines
        - [Scattering, null, 12]     # also 'Write-in', 'Others', 'Miscellaneous': counted as scattering
        note: >-                     a ruling: why this figure and not another
        source: >-                   where the figures are not the Clerk's (the Clerk prints none): the short cite
                                     shown with the race ('CQ, *Guide to U.S. Elections*, 6th ed. (2010), p. 1275')
    untabulated: [h AR 1]            unopposed, and the State did not count the vote (the Clerk's footnote)
    won: {h PA 6: George M. Rhodes}  the winner where the Clerk prints no vote for a contested race
    wikipedia_differs: [s MD 1]      read and confirmed; Wikipedia's percentages differ and the Clerk stands
    not_in_volume: {s ND 1: why}     a special election Wikipedia lists that the Clerk's November volume does not
    president:
      NY:
        slates:
        - [Democratic, 3423909]      a slate's party as printed, and its vote, in printed order
        - [Scattering, 256]
        source: >-                   where the figures are not the Clerk's
        note: >-

Rules for a reading (the review tools in tools/elections/review/ apply them):
  - Every figure from the page image, digit by digit; checked against the State's recapitulation.
  - Where the race page and the recapitulation differ, the figure the Clerk's own totals add up with
    is used, and the race's note says so.
  - Names and parties as printed; make_elections.py gives Wikipedia's name where the surname matches.

Exposed as before: READ[year][(ch, st, seat)] = [(name, party, votes[, lines])]; UNTABULATED, WON,
AGREE_NOT (wikipedia_differs), PRES[year][st] = [(party, votes)], PRES_FROM[(year, st)], NOTES[year][key].
"""
import glob
import os

import yaml

DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'elections', 'readings')


def key(s):
    """'h NY 9' -> ('h', 'NY', 9); 'h NM 0-1' -> ('h', 'NM', '0-1'); 's OR 2 special' -> ('s', 'OR', 2, 'special')."""
    ch, st, seat, *sp = s.split()
    return (ch, st, int(seat) if seat.isdigit() else seat) + tuple(sp)


def row(r):
    r = list(r)
    if len(r) > 3:
        r[3] = [tuple(x) for x in r[3]]
    return tuple(r)


READ, UNTABULATED, WON, AGREE_NOT, PRES, PRES_FROM, NOTES, NOT_IN_VOLUME, RACE_FROM = {}, {}, {}, {}, {}, {}, {}, {}, {}
for f in sorted(glob.glob(os.path.join(DIR, '*.yaml'))):
    d = yaml.safe_load(open(f, encoding='utf-8')) or {}
    y = d['year']
    READ[y] = {key(k): [row(r) for r in v['cands']] for k, v in (d.get('races') or {}).items()}
    NOTES[y] = {key(k): v['note'] for k, v in (d.get('races') or {}).items() if v.get('note')}
    RACE_FROM[y] = {key(k): v['source'] for k, v in (d.get('races') or {}).items() if v.get('source')}
    UNTABULATED[y] = {key(k) for k in d.get('untabulated') or []}
    WON[y] = {key(k): v for k, v in (d.get('won') or {}).items()}
    AGREE_NOT[y] = {key(k) for k in d.get('wikipedia_differs') or []}
    NOT_IN_VOLUME[y] = {key(k): v for k, v in (d.get('not_in_volume') or {}).items()}
    PRES[y] = {st: [tuple(x) for x in v['slates']] for st, v in (d.get('president') or {}).items()}
    for st, v in (d.get('president') or {}).items():
        if v.get('source'):
            PRES_FROM[(y, st)] = v['source']
