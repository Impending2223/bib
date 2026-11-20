# Reader 4's DSL (Nov. 19): entries and ops as short calls; ids from ids.tsv (claim.py); join2.py writes the patch.
import re, unicodedata, datetime, zoneinfo, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
W = '[[w.lich-su-khang-chien-chong-my]]'
PATCH = '2026-11-14-b16-lskc-1'
ENT = []    # add specs
OTHER = []  # cite/variant/check/also/... ops
MON = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']
def fold(s):
    s = s.replace('Đ', 'D').replace('đ', 'd')
    s = unicodedata.normalize('NFD', s)
    s = ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def whenof(d, d2=None):
    y, m, dd = (d.split('-') + [None, None])[:3]
    if dd is None: return MON[int(m) - 1]
    s = f"{MON[int(m)-1]} {int(dd)}"
    if d2:
        y2, m2, dd2 = d2.split('-')
        s += '–' + (f"{int(dd2)}" if m2 == m else f"{MON[int(m2)-1]} {int(dd2)}")
    return s
def utc(date, hhmm, tz):
    h, m = [int(x) for x in hhmm.split(':')]
    dt = datetime.datetime.combine(datetime.date.fromisoformat(date), datetime.time(h, m), zoneinfo.ZoneInfo(tz))
    return dt.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
BANDS = {'predawn': (0, 6), 'morning': (6, 12), 'afternoon': (12, 18), 'evening': (19, 22), 'night': (22, 24), 'daytime': (6, 19), 'day': (0, 24), 'early morning': (5, 8), 'workday daytime': (9, 17)}
def band(date, b, tz):
    a, e = BANDS[b]; z = zoneinfo.ZoneInfo(tz); d = datetime.date.fromisoformat(date)
    lo = datetime.datetime.combine(d, datetime.time(a), z); hi = datetime.datetime.combine(d, datetime.time(0), z) + datetime.timedelta(hours=e)
    f = lambda t: t.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    return [f(lo), f(hi)]
def A(slug, date, thread, c, pin, to=None, when=None, also=(), names=(), place=None, vis=False, tags=(), time=None, tz='Asia/Ho_Chi_Minh',
      approx=False, band_=None, extra='', check='', tocheck='', pub='2013', follows=None, at=None):
    """slug: unique short key (ledger words); pin: 'III, 123' or 'III, 123 (what)'; names: display names in c."""
    w = when or whenof(date, to)
    n = f"{W}, {pin}."
    n = n.replace('..', '.')
    if vis: n += f" Made public: {pub}."
    if extra: n += ' ' + extra
    if tocheck: n += ' To check: ' + tocheck
    if names: n += ' Names: ' + ', '.join(names) + '.'
    if check: n += ' Check: ' + check
    e = dict(slug=slug, date=date, when=w, thread=thread, also=list(also), c=c, n=n, names=list(names), place=place, vis=vis, tags=list(tags))
    if time: e.update(time=utc(date, time, tz), time_zone=tz, time_approx=approx)
    elif band_: e.update(time_range=band(date, band_, tz), time_band=band_, time_zone=tz)
    if follows: e['follows'] = follows
    if at: e['at'] = at
    ENT.append(e)
def C(id, pin, units='A', **kw):
    OTHER.append({'cite': {'id': id, 'item': f"{W}, {pin}", 'units': units}})
def V(id, unit, reads, at):
    OTHER.append({'variant': {'id': id, 'unit': unit, 'witness': 'w.lich-su-khang-chien-chong-my', 'reads': reads, 'at': at}})
def K(id, text): OTHER.append({'check': {'id': id, 'text': text}})
def ALSO(id, add): OTHER.append({'also': {'id': id, 'add': list(add)}})
def RAW(op): OTHER.append(op)
