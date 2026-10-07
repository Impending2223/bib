"""The Biographical Directory of the United States Congress, 1774-2005 (H. Doc. 108-222, GPO 2005), on govinfo:
each member's biography and bibliography, with its printed page. sources/bd/<letter>.json.
# Usage: python3 tools/lives/make_bd.py PARTS_DIR [LETTER ...]
#   PARTS_DIR holds the Biographies granules, GPO-CDOC-108hdoc222-4-<n>.pdf (n = 1 for A ... 25 for Z), downloaded
#   from govinfo (the url below). Each page is read a column at a time (pdftotext -layout, cropped), hyphens at
#   line ends kept where they join numbers or compound numerals, and cut into entries at each SURNAME, Given.
#   Writes [{name, page (printed), part, pdf (page in the granule), text, bib}] for each letter.
#   The build links a citation 'BD 1299' to the granule and page.
"""
import json, os, re, subprocess, sys, unicodedata

URL = 'https://www.govinfo.gov/content/pkg/GPO-CDOC-108hdoc222/pdf/GPO-CDOC-108hdoc222-4-{n}.pdf'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'sources', 'bd')
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
PARTS = {L: i + 1 for i, L in enumerate(LETTERS.replace('X', ''))}   # no X granule
NUM = r'(?:Twenty|Thirty|Forty|Fifty|Sixty|Seventy|Eighty|Ninety|one|two|three|four|five|six|seven|eight|nine)'


def pages(pdf):
    out = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    n = int(re.search(r'Pages:\s+(\d+)', out).group(1))
    w, h = (float(x) for x in re.search(r'Page size:\s+([\d.]+) x ([\d.]+)', out).groups())
    return n, w, h


def column(pdf, p, x, w, h):
    return subprocess.run(['pdftotext', '-layout', '-f', str(p), '-l', str(p), '-x', str(int(x)), '-y', '0',
                           '-W', str(int(w)), '-H', str(int(h)), pdf, '-'], capture_output=True, text=True).stdout


def join(lines):
    """Lines of one column into text: a hyphen at a line's end kept before a digit or after a numeral word."""
    out = ''
    for ln in lines:
        ln = ln.strip()
        if not ln:
            out += '\n'
            continue
        if out.endswith('-') and not out.endswith(' -'):
            if re.match(r'\d', ln) or re.search(NUM + r'-$', out) or re.search(r'\d-$', out):
                out += ln
            else:
                out = out[:-1] + ln
        else:
            out += (' ' if out and not out.endswith('\n') else '') + ln
    return out


# a surname in capitals, with its particles and lowercase prefixes as printed: McCARTHY, MacGREGOR, de la GARZA,
# du PONT, St. GERMAIN, GONZÁLEZ
UP = "A-ZÀ-ÖØ-Þ"
TOK = rf"(?:Mc|Mac|Di|De|La|Le|Van|Von)?[{UP}][{UP}'’\-]+"
SUR = rf"(?:(?:de|du|la|le|van|von|der|den|St\.|ST\.|De|La|Van|Von) )*{TOK}(?: {TOK})*"
HEAD = re.compile(rf"^({SUR}(?:, (?:Jr|Sr)\.)?), ([{UP}][^,]*)")
# an entry run on into the one before it (no indent seen): split where a heading and its role begin mid-text
RUN = re.compile(rf"(?<=[a-z.;)\]])(?<!S[Tt]\.) (?=(?:{SUR}), [{UP}][^,]*(?: \([^)]*\))?, (?:an?|the) (?:Representative|Senator|Delegate|"
                 rf"Resident Commissioner|Vice President)\b)")


def parse(pdf, part):
    n, w, h = pages(pdf)
    entries, cur = [], None
    for p in range(1, n + 1):
        full = column(pdf, p, 0, w, h)
        m = re.search(r'Biographies\s+(\d{3,4})|(\d{3,4})\s+Biographical Directory', full)
        printed = int(m.group(1) or m.group(2)) if m else None
        for x in (0, w / 2):
            txt = unicodedata.normalize('NFC', column(pdf, p, x, w / 2, h))
            lines = [l for l in txt.split('\n') if not re.match(r'\s*(Biographies\s+\d+|\d+\s+Biographical Directory|Biographies|Biographical Directory)\s*$', l)]
            # paragraphs begin indented: a new entry is an indented line opening with SURNAME, Given
            para = []
            for l in lines + ['']:
                if (l.startswith('  ') and HEAD.match(l.strip())) or not l.strip():
                    if para:
                        text = join(para)
                        hm = HEAD.match(text)
                        if hm and para[0].startswith('  ') and (cur is None or text[:2] != cur['text'][:2] or True):
                            cur = {'name': hm.group(0)[:60], 'page': printed, 'part': part, 'pdf': p, 'text': text}
                            entries.append(cur)
                        elif cur:
                            cur['text'] += ' ' + text
                    para = [l] if l.strip() else []
                else:
                    para.append(l)
    split = []
    for e in entries:
        for i, t in enumerate(RUN.split(re.sub(r'\s+', ' ', e['text']).strip())):
            split.append(dict(e, text=t, name=HEAD.match(t).group(0)[:60]) if i and HEAD.match(t) else dict(e, text=t))
    for i in range(len(split) - 1, 0, -1):
        if not HEAD.match(split[i]['text']):
            split[i - 1]['text'] += ' ' + split.pop(i)['text']
    entries = split
    for e in entries:
        t = re.sub(r'\s+', ' ', e['text']).strip()
        # a running head the column crop caught mid-text, whole or cut: '1976 Biographica', 'al Directory',
        # 'aphies 1131', 'Biogra'
        t = re.sub(r' ?\b\d{3,4} Biogra[a-z]*(?: Dir[a-z]*)?', '', t)
        t = re.sub(r' ?\b(?:Biographical|iographical|ographical|graphical|raphical|aphical|phical|hical|ical|cal|al|l)'
                   r' Dir[a-z]*\b(?: \d{3,4}\b)?', '', t)
        t = re.sub(r' ?\b[A-Za-z]*(?:aphies|phies) \d{3,4}\b', '', t)
        t = re.sub(r' Biogra(?:p|ph|phi|phic|phica|phie)?(?= |$)', '', t)
        b = t.split(' Bibliography: ', 1)
        e['text'], e['bib'] = b[0], (b[1] if len(b) > 1 else '')
    return entries


def main():
    d = sys.argv[1]
    letters = sys.argv[2:] or list(PARTS)
    os.makedirs(OUT, exist_ok=True)
    for L in letters:
        n = PARTS[L]
        pdf = os.path.join(d, f'GPO-CDOC-108hdoc222-4-{n}.pdf')
        if not os.path.exists(pdf):
            subprocess.run(['curl', '-s', '-o', pdf, URL.format(n=n)], check=True)
        es = parse(pdf, n)
        json.dump(es, open(os.path.join(OUT, f'{L}.json'), 'w'), ensure_ascii=False, indent=0)
        print(L, len(es))


if __name__ == '__main__':
    main()
