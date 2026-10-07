"""The lookups that let the roster link its sources: sources/executive-links.json.
# Usage: python3 tools/executive/make_source_links.py CRECB_DIR POCOM_DIR FRUS_PERSONS_TSV FRUS_VOLS
#   CRECB_DIR         pages-YYYY.tsv for each year 1953-74: every granule of the bound Congressional Record on
#                     govinfo (first page, last page, date, chamber, granule id), and log.txt naming each year's
#                     Index granule
#   POCOM_DIR         a clone of github.com/HistoryAtState/pocom
#   FRUS_PERSONS_TSV  the lists of persons of the FRUS volumes, 1952-76: name<TAB>role<TAB>volume id
#   FRUS_VOLS         the volume files of github.com/HistoryAtState/frus, one path a line (volumes/frus1961-63v05.xml)
# Writes, for the build (tools/bib/executive.py, sources), which needs no network:
#   senate      {date: granule}: the Senate's proceedings for each day, where a holder's "Cong. Rec." points
#   index       {year: granule}: the year's Index, where "Cong. Rec. Index YYYY" points
#   pocom       {holder name: person id}: the Office of the Historian's page for each holder sourced to POCOM
#   frus        {holder name: [volume id, ...]}: the volumes whose lists of persons give the holder, for "FRUS persons list"
#   volumes     [volume id]: every FRUS volume 1952-76, to read "FRUS 1961–63, VII–IX, microfiche supp., doc. 4"
#   pages       {"YYYY|page": granule}: the granule holding a page cited as "Cong. Rec. 1973, 6695"
# Rerun after adding holders sourced to POCOM or FRUS.
"""
import ast, glob, json, os, re, sys

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
sys.path.insert(0, os.path.dirname(__file__))
from bib import store  # noqa: E402
from bib.executive_names import compatible  # noqa: E402

OUT = os.path.join(ROOT, 'sources', 'executive-links.json')
MONTHS = {m: i for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                       'September', 'October', 'November', 'December'], 1)}


def senate_days(d, cited=()):
    days, index, pages = {}, {}, {}
    for f in sorted(glob.glob(os.path.join(d, 'pages-*.tsv'))):
        for line in open(f, encoding='utf-8'):
            p = line.rstrip('\n').split('\t')
            if len(p) < 5:
                continue
            yr = re.search(r'(\d{4})', p[2])
            for y, pg in cited:
                if yr and yr.group(1) == y and p[0].isdigit() and p[1].isdigit() and int(p[0]) <= pg <= int(p[1]):
                    pages.setdefault(f'{y}|{pg}', p[4])
            if p[3] != 'Senate':
                continue
            m = re.match(r'(\w+) (\d+), (\d{4})', p[2])
            if m and m.group(1) in MONTHS:
                day = f'{m.group(3)}-{MONTHS[m.group(1)]:02d}-{int(m.group(2)):02d}'
                days.setdefault(day, p[4])
    log = os.path.join(d, 'log.txt')
    if os.path.exists(log):
        for line in open(log, encoding='utf-8'):
            m = re.match(r"(\d{4}) parts \d+ granules \d+ index (\[.*\])", line)
            if m:
                ids = ast.literal_eval(m.group(2))
                if ids:
                    index[m.group(1)] = ids[0]
    index.setdefault('1952', 'GPO-CRECB-1952-pt12-1')   # 82d Cong., 2d sess.: before the pages files begin
    return days, index, pages


def holders():
    """(name, given, src list, from, to) for every holder in the roster."""
    for f in sorted(glob.glob(os.path.join(ROOT, 'executive', '*.yaml'))):
        for o in (store.load_yaml(f) or {}).get('offices') or []:
            for h in o.get('holders') or []:
                yield h['name'], h.get('given') or '', [str(x) for x in store.as_list(h.get('src'))], \
                    str(h.get('from') or ''), str(h.get('to') or ''), o.get('title') or ''


def split(name):
    bare = re.sub(r'\s*\([^)]*\)', '', name)
    p = [x.strip() for x in bare.split(',')]
    return store.fold(p[0]), p[1] if len(p) > 1 else ''


def pocom_ids(pocom):
    import xml.etree.ElementTree as ET
    by_sur = {}
    for f in glob.glob(os.path.join(pocom, 'people', '*', '*.xml')):
        r = ET.parse(f).getroot()
        t = lambda p: re.sub(r'\s+', ' ', (r.findtext(p) or '')).strip()
        by_sur.setdefault(store.fold(t('persName/surname')), []).append(
            (t('id'), t('persName/forename'), t('persName/altname'), t('birth')))
    out = {}
    for name, given, src, frm, *_ in holders():
        if 'POCOM' not in src or name in out:
            continue
        sur, g = split(name)
        cands = by_sur.get(sur, [])
        hits = [i for i, fore, alt, b in cands if (g and compatible(g, fore)) or (given and compatible(given, fore))]
        if len(hits) > 1:   # the initials too: 'Charles E.' is Charles Eustis, not Charles Wesley
            words = store.fold(given or g).replace('.', ' ').split()
            hits = [i for i, fore, alt, b in cands if i in hits and
                    all(any(f.startswith(w) for f in store.fold(fore).replace('.', ' ').split()) for w in words)]
        if len(hits) > 1:   # father and son: alive and of age when the holder took office, and the suffix
            y = int(frm[:4]) if frm[:4].isdigit() else 1960
            info = {i: (alt, b) for i, fore, alt, b in cands}
            hits = [i for i in hits if not info[i][1].isdigit() or 22 <= y - int(info[i][1]) <= 85] or hits
            suf = re.search(r',\s*(Jr\.|II|III|IV)$', name)
            if len(hits) > 1:
                marked = [i for i in hits if re.search(r'(Jr\.?|\bII|\bIII|\bIV)$', info[i][0]) or i.endswith('-jr')]
                hits = (marked if suf else [i for i in hits if i not in marked]) or hits
            if len(hits) > 1:   # the forename exactly as the roster gives it ('Nathaniel', not Nathaniel P.)
                fore = {i: f for i, f, alt, b in cands}
                hits = [i for i in hits if store.fold(fore[i]) == store.fold(given or g)] or hits
        if len(hits) == 1:
            out[name] = hits[0]
    return out


def frus_vols(tsv):
    by_sur = {}
    for line in open(tsv, encoding='utf-8'):
        p = line.rstrip('\n').split('\t')
        if len(p) == 3:
            by_sur.setdefault(store.fold(p[0].split(',')[0].strip()), []).append(p)
    out = {}
    for name, given, src, frm, to, title in holders():
        if not any(s.startswith('FRUS') for s in src):
            continue
        sur, g = split(name)
        words = {w.lower() for w in re.findall(r'[A-Za-z]{4,}', title)}
        y0, y1 = int((frm or '1953')[:4]), int((to or '1974')[:4])
        scored = []
        for n, role, vol in by_sur.get(sur, []):
            vg = n.split(',', 1)[1].strip() if ',' in n else ''
            if not (compatible(g, vg) or compatible(given, vg)):
                continue
            m = re.match(r'frus(\d{4})-(\d{2,4})', vol)
            if not m:
                continue
            a = int(m.group(1))
            b = int(m.group(2)) if len(m.group(2)) == 4 else int(m.group(1)[:2] + m.group(2))
            overlap = a <= y1 and b >= y0
            fit = len(words & {w.lower() for w in re.findall(r'[A-Za-z]{4,}', role)})
            scored.append((-(overlap * 10 + fit), vol))
        vols = []
        for _, v in sorted(scored):
            if v not in vols:
                vols.append(v)
        if vols:
            out.setdefault(name, vols[:2])
    return out


def cited_pages():
    out = set()
    for *_, src, _f, _t, _o in ((None, None, s, f, t, o) for _n, _g, s, f, t, o in holders()):
        for x in src:
            m = re.match(r'Cong\. Rec\. (\d{4}), ([\d, ]+)$', x)
            if m:
                out |= {(m.group(1), int(p)) for p in re.findall(r'\d+', m.group(2))}
    return out


def main():
    crecb, pocom, frus, vols = sys.argv[1:5]
    days, index, pages = senate_days(crecb, cited_pages())
    volumes = sorted({re.sub(r'.*/|\.xml$', '', x.strip()) for x in open(vols, encoding='utf-8') if x.strip()})
    out = {'senate': days, 'index': index, 'pages': pages, 'volumes': volumes,
           'pocom': pocom_ids(pocom), 'frus': frus_vols(frus)}
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=0, sort_keys=True)
    print({k: len(v) for k, v in out.items()})


if __name__ == '__main__':
    main()
