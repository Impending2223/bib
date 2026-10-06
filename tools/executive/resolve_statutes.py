"""Find the govinfo file for every Statutes at Large citation in executive/, and report the ones that point nowhere.
# Usage: python3 tools/executive/resolve_statutes.py [--cache DIR]
#   Writes sources/statute-links.json: citation key -> URL. The build (tools/bib/executive.py, stat_url) links
#   each citation through it, falling back to the page the act begins on. Needs the network; the build does not.
#
#   govinfo files the Statutes by act ("granules"), each named by the page it begins on: STATUTE-61-Pg495. Where
#   several acts begin on one page the later ones take a suffix (STATUTE-69-Pg9-2), and a missing name answers
#   200 with an empty body, so a status code proves nothing. Each volume's package record lists its granules;
#   each granule's record gives its pages, chapter, and public law. A citation 'ch. 9, § 4(c), 69 Stat. 9, 11'
#   is matched to the granule beginning on page 9 with chapter 9, and the pin (page 11) to the page within it
#   (#page=3), or to the granule that holds it.
"""
import glob, json, os, re, sys, time, urllib.request

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from bib import store  # noqa: E402

OUT = os.path.join(ROOT, 'sources', 'statute-links.json')
META = 'https://www.govinfo.gov/metadata/'
PDF = 'https://www.govinfo.gov/content/pkg/STATUTE-{v}/pdf/{g}.pdf'
STAT = re.compile(r'(?:(ch\. \d+|Pub\. L\. \d+-\d+)[^;]*?)?\b(\d+) Stat\. (\d+)(?:, (\d+)(?![\d.]))?')


def key(vol, start, pin, marker):
    return f'{vol}|{start}|{pin or ""}|{marker or ""}'


def fetch(url, cache):
    path = os.path.join(cache, re.sub(r'[^\w.-]', '_', url.split('metadata/')[-1]))
    if os.path.exists(path):
        return open(path, encoding='utf-8').read()
    for i in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'bib-roster/1.0'}), timeout=120) as r:
                t = r.read().decode('utf-8', 'replace')
            if 'Please Retry later' in t or not t.strip():
                raise IOError('throttled')
            open(path, 'w', encoding='utf-8').write(t)
            time.sleep(1)
            return t
        except Exception as e:
            time.sleep(5 * (i + 1))
    return ''


def cites():
    """Every Stat. citation in executive/: (vol, start, pin, marker, where)."""
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'executive', '*.yaml'))):
        d = store.load_yaml(f) or {}
        texts = []
        for a in d.get('law') or []:
            texts += [(a.get('cite') or '', True), (a.get('does') or '', False)]
        for o in d.get('offices') or []:
            for a in o.get('law') or []:
                texts += [(a.get('cite') or '', True), (a.get('does') or '', False)]
        for t, is_cite in texts:
            for m in STAT.finditer(t):
                out.append((int(m.group(2)), int(m.group(3)), int(m.group(4)) if m.group(4) else None,
                            m.group(1) if is_cite else None, os.path.basename(f)))
    return out


def granules(vol, cache):
    """[(granule id, start page)] in the volume's package record, in order."""
    t = fetch(f'{META}pkg/STATUTE-{vol}/mods.xml', cache)
    out = []
    for g in re.findall(r'ID="id-(STATUTE-\d+-Pg(\d+)(?:-\d+)?)"', t):
        out.append((g[0], int(g[1])))
    return out


def granule(vol, gid, cache):
    t = fetch(f'{META}granule/STATUTE-{vol}/{gid}/mods.xml', cache)
    st, en = re.search(r'<start>(\d+)</start>', t), re.search(r'<end>(\d+)</end>', t)
    ch = re.search(r'<chapter>(\d+)', t)
    pl = re.search(r'public law citation">Public Law (\d+-\d+)<', t)
    return {'start': int(st.group(1)) if st else None, 'end': int(en.group(1)) if en else None,
            'ch': ch.group(1) if ch else None, 'pl': pl.group(1) if pl else None}


def main():
    cache = sys.argv[sys.argv.index('--cache') + 1] if '--cache' in sys.argv else os.path.join(ROOT, '.cache', 'statutes')
    os.makedirs(cache, exist_ok=True)
    links, problems = {}, []
    for vol, start, pin, marker, where in sorted(set(cites()), key=lambda x: (x[0], x[1], x[2] or 0, x[3] or '')):
        k = key(vol, start, pin, marker)
        if k in links:
            continue
        gs = granules(vol, cache)
        cands = [g for g, s in gs if s == start]
        if not cands:
            problems.append(f'{where}: no act begins at {vol} Stat. {start}')
            continue
        info = {g: granule(vol, g, cache) for g in cands}
        pick = cands[0]
        if marker and len(cands) > 1:
            num = marker.split()[-1]
            hit = [g for g in cands if num in (info[g]['ch'], info[g]['pl'])]
            if hit:
                pick = hit[0]
            else:
                problems.append(f'{where}: {marker}, {vol} Stat. {start}: no act of that number begins there')
        elif marker and info[pick]['ch'] != marker.split()[-1] and info[pick]['pl'] != marker.split()[-1]:
            problems.append(f'{where}: {marker}, {vol} Stat. {start}: the act there is ch. {info[pick]["ch"]}, '
                            f'Pub. L. {info[pick]["pl"]}')
        url = PDF.format(v=vol, g=pick)
        g = info[pick]
        if pin and g['start'] and g['end'] and g['start'] <= pin <= g['end']:
            if pin > g['start']:
                url += f'#page={pin - g["start"] + 1}'
        elif pin:
            # the granule that holds the pin page: the last to begin at or before it
            later = [x for x, s in gs if s <= pin and s >= start]
            for x in reversed(later):
                gi = granule(vol, x, cache)
                if gi['start'] and gi['end'] and gi['start'] <= pin <= gi['end']:
                    url = PDF.format(v=vol, g=x) + (f'#page={pin - gi["start"] + 1}' if pin > gi['start'] else '')
                    break
            else:
                problems.append(f'{where}: {vol} Stat. {start}, {pin}: the pin page is not in the act')
        links[k] = url
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(dict(sorted(links.items())), f, indent=0, ensure_ascii=False)
    print(f'{len(links)} citations resolved; {len(problems)} problems')
    print('\n'.join(problems))


if __name__ == '__main__':
    main()
