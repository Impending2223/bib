import json, os, subprocess, yaml, datetime, zoneinfo, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = '/home/user/bib'
W = '[[w.lich-su-khang-chien-chong-my]]'
PATCH = '2026-11-14-b16-lskc-3'
IDS_F = os.path.join(HERE, 'ids.json')
IDS = json.load(open(IDS_F)) if os.path.exists(IDS_F) else {}
OPS = []
GAZ = {e['key'] for e in yaml.safe_load(open(ROOT + '/sources/places.yaml'))}
PKS_F = os.path.join(HERE, 'pks.json')
PKS = json.load(open(PKS_F)) if os.path.exists(PKS_F) else {}
def save_ids(): json.dump(IDS, open(IDS_F, 'w'), ensure_ascii=False, indent=0)
def sh(*a):
    return subprocess.run(a, cwd=ROOT, capture_output=True, text=True).stdout.strip()
def claim(k, date, thread, words):
    if k in IDS: return IDS[k]
    i = sh('./bib', 'new-id', 'cal', date, thread)
    r = subprocess.run(['./bib', 'ledger', 'add', date, thread, i, words, PATCH], cwd=ROOT, capture_output=True, text=True)
    if r.returncode: raise SystemExit('ledger add failed ' + k + r.stdout + r.stderr)
    IDS[k] = i; save_ids(); return i
def P(key, name, zone='Asia/Ho_Chi_Minh', **kw):
    if key in GAZ or key in PKS: return
    d = {'key': key, 'name': name, 'zone': zone}; d.update(kw or {'in': 'rvn'})
    PKS[key] = d; json.dump(PKS, open(PKS_F, 'w'), ensure_ascii=False, indent=0)
def utc(date, hm, tz):
    z = zoneinfo.ZoneInfo(tz)
    dt = datetime.datetime.fromisoformat(f'{date} {hm}').replace(tzinfo=z)
    return dt.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
BANDS = {'predawn': (0, 6), 'morning': (6, 12), 'afternoon': (12, 18), 'evening': (19, 22), 'night': (22, 24), 'daytime': (6, 19), 'early morning': (5, 8), 'workday morning': (9, 12), 'workday afternoon': (14, 17), 'workday daytime': (9, 17), 'workday midday': (12, 14), 'day': (0, 24)}
def band(date, b, tz):
    a, c = BANDS[b]; z = zoneinfo.ZoneInfo(tz)
    d = datetime.date.fromisoformat(date)
    lo = datetime.datetime.combine(d, datetime.time(a), z)
    hi = datetime.datetime.combine(d, datetime.time(0), z) + datetime.timedelta(hours=c)
    f = lambda t: t.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    return [f(lo), f(hi)]
def E(k, date, when, c, pages, th='vietnam-hanoi', also=(), place=None, t=None, approx=False, bnd=None, bdate=None,
      at=None, vis=False, us=False, names=(), ntags=(), gloss='', words='', tocheck='', check='', see=(), tags=(), extra='',
      tz='Asia/Ho_Chi_Minh', words_pre='', lw=None, ok=(), pub='2013', polity='drv', another=None):
    i = claim(k, date, th, lw or (c[:60]))
    n = f'{W}, VI, {pages}'
    if gloss: n += f' ({gloss})'
    n += '.'
    for s in ([see] if isinstance(see, str) else see): n += f' See [[{IDS.get(s, s)}]].'
    if words: n += f' The words: {words}'
    if extra: n += ' ' + extra
    if vis: n += f' Made public: {pub}.'
    if tocheck: n += ' To check: ' + tocheck
    if names: n += ' Names: ' + ', '.join(names) + '.'
    if check: n += ' Check: ' + check
    tg = []
    if polity: tg.append('polity:' + polity)
    if us: tg.append('polity:us')
    tg += list(ntags) + list(tags)
    if vis: tg.append('vis:only:drv' if vis is True else vis)
    tg += list(ok)
    e = {'id': i, 'when': when, 'date': date, 'thread': th}
    if also: e['also'] = list(also)
    e['c'] = c; e['n'] = n; e['tags'] = tg
    if place:
        pl = [place] if isinstance(place, str) else list(place)
        for p in pl:
            if p not in GAZ and p not in PKS: raise SystemExit(f'place {p} unknown ({k})')
        e['place'] = pl[0] if len(pl) == 1 else pl
    if t:
        e['time'] = utc(bdate or date, t, tz); e['time_zone'] = tz
        if approx: e['time_approx'] = True
    elif bnd:
        e['time_range'] = band(bdate or date, bnd, tz); e['time_band'] = bnd; e['time_zone'] = tz; e['range_basis'] = 'record'
    if at: e['at'] = at
    OPS.append({'add': {'entry': e}})
    return i
def C(idk, pages, gloss, units='all', extra=''):
    i = IDS.get(idk, idk)
    OPS.append({'cite': {'id': i, 'item': f'{W}, VI, {pages} ({gloss})' + extra, 'units': units}})
def V(idk, unit, reads, at):
    i = IDS.get(idk, idk)
    OPS.append({'variant': {'id': i, 'unit': unit, 'witness': 'w.lich-su-khang-chien-chong-my', 'reads': reads, 'at': at}})
def CH(idk, text):
    OPS.append({'check': {'id': IDS.get(idk, idk), 'text': text}})
def dump(name):
    used = set()
    for o in OPS:
        pl = o.get('add', {}).get('entry', {}).get('place')
        if pl: used |= set([pl] if isinstance(pl, str) else pl)
    ops = [{'place-key': v} for k, v in PKS.items() if k in used] + OPS
    class D(yaml.SafeDumper): pass
    def strrep(d, s):
        sty = None
        if any(ch in s for ch in ":#'\"*[]{}&!|>%@`") or s[:1] in "-?" or s != s.strip(): sty = "'"
        return d.represent_scalar('tag:yaml.org,2002:str', s, style=sty)
    D.add_representer(str, strrep)
    open(os.path.join(HERE, name), 'w').write(yaml.dump(ops, Dumper=D, allow_unicode=True, sort_keys=False, width=100000, default_flow_style=False))
    print(name, len(ops), 'ops', len(PKS), 'place-keys')
