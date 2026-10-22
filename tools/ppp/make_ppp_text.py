"""The Public Papers of the Presidents, 1960-69, from the Government Publishing Office's volumes on govinfo: every
numbered item, its heading, date and pages, and its text, cleaned, with its pagination.

    python3 -I tools/ppp/make_ppp_text.py --cache DIR [--vol PPP-1961-book1 ...] [--keep-pdf] [--report FILE]

Writes sources/ppp-text/<package>.json.xz, a volume a file (VOLS), and sources/ppp-text/rules.json, the cleaning log
(each rule and how often it fired, a volume a column). Needs the network and pdftotext (poppler) once a volume: each
PDF (585-825 MB) is fetched into DIR, read word by word with its box (`pdftotext -bbox`, kept in DIR gzipped,
about 12 MB), and deleted unless --keep-pdf; a later run reads the boxes from DIR. The build needs neither the PDFs
nor the network. Generated: edit this script, never the files.

The source. GPO's collection PPP on govinfo (https://www.govinfo.gov/app/collection/ppp), the Office of the Federal
Register's volumes, scanned and given a text layer by ABBYY FineReader (2019): a PDF a book, no granules, so a page
is linked as the PDF's page (`#page=N`). Public domain: works of the United States government (17 U.S.C. § 105).

Each file: {"source", "license", "package", "title", "president", "years" (the volume's label, "1963–64"), "book"
(1 or 2 where the volume has two books, else null), "pdf" (the PDF's address), "details" (govinfo's page), "pages"
(the PDF's page count), "folios" ([[first PDF page, last PDF page, offset]]: printed page = PDF page - offset, the
runs of the body), "items": [{n, title, date, page, page_to, pdf, list_page, text}]}. `text` is a list of blocks
[kind, text]: p (a paragraph), s (a line set off: a salutation's close, a signature, a dateline), h (a heading set
large inside the item), b (a bracketed editorial note: "[Delivered in person before a joint session]"), n (the
editors' note, "NOTE: The President spoke at ..."; small type, at the item's end), f (a footnote), q (other small type:
a table, a quoted text). "[p. 123]" in a block's text marks where the printed page 123 begins; every item's first
block begins with its first page's marker.

STYLE (the reading; mechanical: the words are the volume's, nothing summarized or left out but the running heads,
the folios and the pictures):
 1. The page: the words with their boxes; the running head (the first line, at the head's place, naming the
    President, "Public Papers of the Presidents", the item number in brackets or the date) and the folio (a lone
    number on the last line) set aside. The two columns divided at the widest run of least ink near the middle of
    the text block; a line with a word across the gutter, or set large (a heading), runs across the page. The page is
    read band by band between those lines: the left column, then the right.
 2. Type sizes by each word's height against the volume's body size (the commonest height): large (over 1.15
    times: the item headings), small (under 0.92 times: the notes, footnotes, quoted texts and tables).
 3. An item: a large line opening with the next item number (OCR misreadings of digits allowed: "I4", "2I"),
    through the large lines after it; its date the last date in the heading; its title the heading less the number
    and, where the heading ends ". January 21, 1961", the date. The number must follow the last item's (a gap of up
    to three is taken and reported); the volume's List of Items (its front matter: number, title, page) gives each
    item's listed page (`list_page`) and finds a heading the large-type rule missed. The body runs from item 1 to the
    first page headed "Appendix".
 4. Paragraphs: a new one where a line is indented (more than 0.6 of the body size past its column's left edge),
    where the type size changes, after a heading, and for a line set off (indented more than a third of the column:
    `s`). Lines joined with a space; a line ending in a soft hyphen (ABBYY's mark of a word broken at the line's end)
    joined without it; a line ending in a hyphen joined keeping it, unless the volumes print the word whole more
    often than hyphenated; a line ending in a dash joined without a space.
 5. Misreadings put right by rule, each counted in rules.json: digits read as letters inside a number ("I961",
    "i960", "4I", "196r", "S31"); "J" read as "I" or "]" at a word's start ("Iuly", "]ohn"), where the volumes print
    the J form at least three times as often and the I form is not a word of its own (IWORDS); "£" for "f"; stray
    marks ('‘I', '|') alone on a line. Nothing else is guessed: a misreading no rule meets stands, as printed.
 6. Notes: a small-type paragraph opening "NOTE:" (ABBYY reads the small capitals "note:") begins the editors'
    note, and what follows in the item is note. A small-type paragraph before it opening with a mark ("*", "1") is a
    footnote; any other is `q`. A body paragraph in square brackets (not a news conference's "[1.]") is `b`.
 7. Pages: the folios read (the bottom line's number, misread digits allowed) give each PDF page's offset; a page
    whose folio is not read takes the offset of the read pages on either side where they agree, else the nearer.
"""
import argparse
import collections
import datetime
import gzip
import html
import json
import lzma
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "sources", "ppp-text")
GOV = "https://www.govinfo.gov"
UA = {"User-Agent": "bib-ppp (https://impending2223.github.io/bib/)"}
SOURCE = ("Public Papers of the Presidents of the United States (Office of the Federal Register, National Archives "
          "and Records Service), the volumes on govinfo.gov (U.S. Government Publishing Office, collection PPP), "
          "their OCR text layer")
LICENSE = "Public domain: a work of the United States government (17 U.S.C. § 105)"

# package, the volume's years, the President, the book (of two), its span
VOLS = [
    ("PPP-1960-book1", "1960–61", "Dwight D. Eisenhower", None, "1960-01-01", "1961-01-20"),
    ("PPP-1961-book1", "1961", "John F. Kennedy", None, "1961-01-20", "1961-12-31"),
    ("PPP-1962-book1", "1962", "John F. Kennedy", None, "1962-01-01", "1962-12-31"),
    ("PPP-1963-book1", "1963", "John F. Kennedy", None, "1963-01-01", "1963-11-22"),
    ("PPP-1963-book2", "1963–64", "Lyndon B. Johnson", 1, "1963-11-22", "1964-06-30"),
    ("PPP-1964-book1", "1963–64", "Lyndon B. Johnson", 2, "1964-07-01", "1964-12-31"),
    ("PPP-1965-book1", "1965", "Lyndon B. Johnson", 1, "1965-01-01", "1965-06-30"),
    ("PPP-1965-book2", "1965", "Lyndon B. Johnson", 2, "1965-07-01", "1965-12-31"),
    ("PPP-1966-book1", "1966", "Lyndon B. Johnson", 1, "1966-01-01", "1966-06-30"),
    ("PPP-1966-book2", "1966", "Lyndon B. Johnson", 2, "1966-07-01", "1966-12-31"),
    ("PPP-1967-book1", "1967", "Lyndon B. Johnson", 1, "1967-01-01", "1967-06-30"),
    ("PPP-1967-book2", "1967", "Lyndon B. Johnson", 2, "1967-07-01", "1967-12-31"),
    ("PPP-1968-book1", "1968–69", "Lyndon B. Johnson", 1, "1968-01-01", "1968-06-30"),
    ("PPP-1968-book2", "1968–69", "Lyndon B. Johnson", 2, "1968-07-01", "1969-01-20"),
]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
# words beginning with I that are words (STYLE 5): never turned to J
IWORDS = {"I", "Ian", "Iran", "Ike", "Ill", "Ill.", "Ion", "Iona", "Ira", "Iris", "Irish", "Iron", "Isle", "Iowa",
          "Iva", "Ivy", "Ivan", "Ida", "Idaho", "In", "Inn", "Is", "It", "Its", "If", "Ia", "Ian's"}

RULES = collections.Counter()


def pdf_url(pkg):
    return f"{GOV}/content/pkg/{pkg}/pdf/{pkg}.pdf"


# ---------------------------------------------------------------- the volume's words

def fetch(pkg, cache, keep_pdf):
    """The volume's words with their boxes, cached gzipped in DIR; the PDF deleted unless keep_pdf."""
    bbox = os.path.join(cache, f"{pkg}.bbox.html.gz")
    if os.path.exists(bbox):
        return bbox
    pdf = os.path.join(cache, f"{pkg}.pdf")
    if not os.path.exists(pdf):
        print(f"fetching {pdf_url(pkg)}", file=sys.stderr)
        with urllib.request.urlopen(urllib.request.Request(pdf_url(pkg), headers=UA), timeout=900) as r, \
                open(pdf + ".part", "wb") as f:
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                f.write(b)
        os.rename(pdf + ".part", pdf)
    with gzip.open(bbox + ".part", "wb") as f:
        p = subprocess.run(["pdftotext", "-bbox", pdf, "-"], check=True, stdout=subprocess.PIPE,
                           stderr=subprocess.DEVNULL)
        f.write(p.stdout)
    os.rename(bbox + ".part", bbox)
    if not keep_pdf:
        os.remove(pdf)
    return bbox


WORD = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>')
PAGE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)


def read_pages(path):
    s = gzip.open(path, "rt", encoding="utf-8").read()
    out = []
    for m in PAGE.finditer(s):
        ws = []
        for a, b, c, d, t in WORD.findall(m.group(3)):
            t = html.unescape(t)
            if t.strip():
                ws.append((float(a), float(b), float(c), float(d), t))
        out.append((float(m.group(1)), float(m.group(2)), ws))
    return out


def rows_of(ws, tol=None):
    """Words into lines: by the middle of their boxes, then left to right."""
    ws = sorted(ws, key=lambda w: (w[1] + w[3]) / 2)
    rows = []
    for w in ws:
        yc = (w[1] + w[3]) / 2
        t = tol or max(2.5, (w[3] - w[1]) * .45)
        if rows and abs(rows[-1][0] - yc) < t:
            rows[-1][1].append(w)
            n = len(rows[-1][1])
            rows[-1][0] = (rows[-1][0] * (n - 1) + yc) / n
        else:
            rows.append([yc, [w]])
    return [(yc, sorted(r, key=lambda w: w[0])) for yc, r in rows]


def med(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2] if xs else 0


# ---------------------------------------------------------------- numbers and dates, misread

DIGIT = {"I": "1", "l": "1", "i": "1", "|": "1", "!": "1", "]": "1", "O": "0", "o": "0", "S": "5", "s": "5",
         "T": "7", "Z": "2", "z": "2", "B": "8", "g": "9", "r": "1", "t": "1"}


def as_number(tok):
    """'I4' -> 14, '2I' -> 21, '54 1' -> 541; None where it is no number (STYLE 5)."""
    t = tok.strip(".,:;'’‘\"")
    if not t or len(t) > 5:
        return None
    if t.isdigit():
        return int(t)
    if not any(c.isdigit() for c in t) and t not in ("I", "l", "i", "II", "Il", "lI", "ll", "IO", "lO", "Io", "IS", "ii", "Ii", "iI"):
        return None
    s = "".join(c if c.isdigit() else DIGIT.get(c, "?") for c in t)
    return int(s) if "?" not in s else None


DATE_RE = re.compile(r"(" + "|".join(MONTHS) + r"|[IJ]an\w*|[IJ]u[nl]\w*|[IJ\]]u[nl]y|[IJ\]]une)\s+"
                     r"([\dIlOoSi]{1,2})\s*[,.]\s*([\dIlOoSi]{4}|[\dIlOoSigr]{4})")


def fix_month(m):
    for M in MONTHS:
        if m == M:
            return M
    if re.match(r"^[IJ\]]an", m):
        return "January"
    if re.match(r"^[IJ\]]un", m):
        return "June"
    if re.match(r"^[IJ\]]ul", m):
        return "July"
    return None


def dates_in(t):
    out = []
    for m in DATE_RE.finditer(t):
        mo = fix_month(m.group(1))
        d, y = as_number(m.group(2)), as_number(m.group(3).replace("g", "9"))
        if mo and d and y and 1959 <= y <= 1969 and 1 <= d <= 31:
            try:
                out.append((m.start(), m.end(), datetime.date(y, MONTHS.index(mo) + 1, d).isoformat()))
            except ValueError:
                pass
    return out


# ---------------------------------------------------------------- the page

def page_parts(W, H, ws, body_h, head_y, surname):
    """(lines, folio): the page's lines in reading order [(pos, words, size)], pos L, R or S, size b, s or L; the
    running head and the folio set aside (STYLE 1)."""
    if not ws:
        return [], None
    rows = rows_of(ws)
    folio = None
    # the running head
    if rows:
        yc, r = rows[0]
        t = " ".join(w[4] for w in r)
        if head_y is not None and abs(r[0][1] - head_y) < 9 and (
                re.search(r"\[\s*\S{1,4}\s*\]|Papers|Presidents|Appendix|Index|" + surname, t)
                or re.search(r"\b(Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)\b", t)) \
                and len(r) <= 12:
            ws = [w for w in ws if w not in r]
            rows = rows[1:]
    # the folio
    if rows:
        yc, r = rows[-1]
        t = " ".join(w[4] for w in r)
        n = as_number(t.replace(" ", "")) if len(r) <= 2 else None
        if n is not None and yc > H * .7:
            folio = n
            ws = [w for w in ws if w not in r]
        elif len(r) == 1 and re.fullmatch(r"[\W_]{1,3}|[‘'I|]{1,2}", t):
            RULES["stray mark alone on a line, dropped"] += 1
            ws = [w for w in ws if w not in r]
    if not ws:
        return [], folio
    size = lambda h: "L" if h > body_h * 1.15 else ("s" if h < body_h * .92 else "b")
    xs = sorted(w[0] for w in ws)
    xe = sorted(w[2] for w in ws)
    left, right = xs[len(xs) // 50], xe[-1 - len(xe) // 50]
    lo, hi = int(left + (right - left) * .36), int(left + (right - left) * .64)
    cov = [0] * (int(W) + 2)
    for w in ws:
        for x in range(max(lo, int(w[0])), min(hi, int(w[2])) + 1):
            cov[x] += 1
    m = min(cov[lo:hi + 1]) if hi > lo else 0
    runs, cur = [], []
    for x in range(lo, hi + 1):
        if cov[x] <= m + 1:
            if cur and x != cur[-1] + 1:
                runs.append(cur)
                cur = []
            cur.append(x)
    if cur:
        runs.append(cur)
    two = bool(runs) and m <= max(2, len(rows_of(ws)) // 12)
    if not two:                                  # one column (a table, a list across the page)
        return [("S", r, size(med([w[3] - w[1] for w in r]))) for yc, r in rows_of(ws)], folio
    run = max(runs, key=lambda r: (len(r), -abs((r[0] + r[-1]) / 2 - (left + right) / 2)))
    g = (run[0] + run[-1]) / 2
    L, R, S = [], [], []
    for w in ws:
        if (w[0] < g - 1 and w[2] > g + 1 and len(re.sub(r"\W", "", w[4])) >= 3) or w[3] - w[1] > body_h * 1.15:
            S.append(w)
        elif (w[0] + w[2]) / 2 < g:
            L.append(w)
        else:
            R.append(w)
    have = set(map(id, S))
    for yc, r in rows_of(S):                      # the rest of a line across the page
        for w in L + R:
            if id(w) not in have and abs((w[1] + w[3]) / 2 - yc) < body_h * .35:
                S.append(w)
                have.add(id(w))
    L = [w for w in L if id(w) not in have]
    R = [w for w in R if id(w) not in have]
    out = []
    bounds = [(-1e9, None)] + rows_of(S) + [(1e9, None)]
    for i in range(len(bounds) - 1):
        a, b = bounds[i][0], bounds[i + 1][0]
        for k, col in (("L", L), ("R", R)):
            for yc, r in rows_of([w for w in col if a < (w[1] + w[3]) / 2 <= b]):
                out.append((k, r, size(med([w[3] - w[1] for w in r]))))
        if bounds[i + 1][1]:
            r = bounds[i + 1][1]
            out.append(("S", r, size(med([w[3] - w[1] for w in r]))))
    return out, folio


# ---------------------------------------------------------------- words put right

class Vocab:
    def __init__(self, counts):
        self.c = counts

    def n(self, w):
        return self.c.get(w, 0)


def core(tok):
    m = re.match(r"^([\"“‘'(\[]*)(.*?)([\"”’'.,;:!?)\]]*)$", tok)
    return m.groups() if m else ("", tok, "")


def fix_word(tok, V):
    """A word's misreadings put right by rule (STYLE 5)."""
    a, w, z = core(tok)
    if not w:
        return tok
    if "£" in w:
        w = w.replace("£", "f")
        RULES["£ read for f"] += 1
    # digits read as letters inside a number
    if re.fullmatch(r"[\dIlOoSi]{2,5}", w) and sum(c.isdigit() for c in w) >= 1 and not w.isdigit() \
            and not re.fullmatch(r"[IlOoSi]+", w):
        n = as_number(w)
        if n is not None and not (w[0] in "Ss" and len(w) < 3):
            RULES["letters read for digits in a number (I961, 4I)"] += 1
            w = str(n)
    elif re.fullmatch(r"(19|i9|I9|l9|ig|Ig)[\dIlOoSi]{1,2}[\drIlOoSi]", w) and not w.isdigit():
        RULES["letters read for digits in a year (i960, 196r, ig6i)"] += 1
        w = "19" + "".join(c if c.isdigit() else DIGIT.get(c, c) for c in w[2:])
    elif w[0] in "]I" and len(w) > 2 and w[1].islower() and w not in IWORDS:
        j = "J" + w[1:]
        if w[0] == "]" or (V.n(j) >= 3 * max(1, V.n(w)) and V.n(j) >= 3):
            RULES[f"J read as {w[0]} at a word's start"] += 1
            w = j
    return a + w + z


def line_text(r):
    return " ".join(w[4] for w in r)


# ---------------------------------------------------------------- the volume

def common_height(pages):
    c = collections.Counter()
    for W, H, ws in pages:
        for w in ws:
            c[round(w[3] - w[1], 1)] += 1
    return c.most_common(1)[0][0]


def head_place(pages):
    c = collections.Counter()
    for W, H, ws in pages:
        if len(ws) > 100:
            c[round(min(w[1] for w in ws))] += 1
    return c.most_common(1)[0][0] if c else None


def list_of_items(pages, body_h, last_front):
    """{n: (title, page)} from the front matter's List of Items (STYLE 3)."""
    out = {}
    expect = 1
    cur = None
    for i in range(last_front):
        W, H, ws = pages[i]
        if not ws:
            continue
        rows = rows_of(ws)
        if not rows or not re.search(r"List|Item", line_text(rows[0][1]), re.I):
            continue
        xs = sorted(w[0] for w in ws)
        left = xs[len(xs) // 30]
        right = max(w[2] for w in ws)
        for yc, r in rows[1:]:
            t = line_text(r)
            if t.strip() in ("Page", "Item") or re.fullmatch(r"Item\s+Page|Page", t.strip()):
                continue
            pg = None
            if r[-1][0] > left + (right - left) * .9:
                pg = as_number(r[-1][4].replace(" ", ""))
                if pg is not None:
                    r = r[:-1]
                    if r and r[-1][0] > left + (right - left) * .85 and as_number(r[-1][4]) is not None:
                        pg = as_number(r[-1][4] + str(pg)) or pg      # '54 1'
                        r = r[:-1]
            if yc > H * .9 and len(r) <= 3:          # the folio (roman) and the printer's marks
                continue
            first = as_number(r[0][4]) if r else None
            numbered = (first is not None and len(r) > 1 and (expect <= first <= expect + 3 or (
                expect - 5 <= first <= expect + 40 and r[1][0] - r[0][0] > body_h)))
            if r and (numbered or cur is None or cur[3]):
                n = first if numbered else expect
                cur = [n, line_text(r[1:] if numbered else r), None, False]
                out[n] = cur
                expect = n + 1
            elif r:
                cur[1] += " " + line_text(r)
            if pg is not None and cur is not None and not cur[3]:
                cur[2], cur[3] = pg, True
    return {n: (t, p) for n, t, p, _ in out.values()}


def folio_runs(folios, npages):
    """{pdf page: offset} for every page from the read folios (STYLE 7), and the runs."""
    read = sorted((p, p - f) for p, f in folios.items() if f is not None and 0 < f < 2000)
    # keep a read folio only where a neighbour agrees with its offset
    good = []
    for i, (p, off) in enumerate(read):
        near = [o for q, o in read[max(0, i - 3):i + 4] if q != p]
        if near.count(off) >= 1:
            good.append((p, off))
    off = {}
    j = 0
    for p in range(1, npages + 1):
        while j < len(good) - 1 and good[j + 1][0] <= p:
            j += 1
        if not good:
            break
        a = good[j]
        b = good[j + 1] if j + 1 < len(good) else a
        if p <= a[0]:
            off[p] = a[1]
        elif a[1] == b[1]:
            off[p] = a[1]
        else:
            off[p] = a[1] if p - a[0] <= b[0] - p else b[1]
    runs = []
    for p in sorted(off):
        if runs and runs[-1][2] == off[p] and runs[-1][1] == p - 1:
            runs[-1][1] = p
        else:
            runs.append([p, p, off[p]])
    return off, runs


def is_item_head(r, expect):
    n = as_number(r[0][4])
    if n is None and len(r) > 1:
        n = as_number(r[0][4] + r[1][4]) if len(r[0][4]) <= 2 and len(r[1][4]) <= 2 else None
        if n is not None and expect <= n <= expect + 3:
            return n, 2
        return None, 0
    if n is not None and expect <= n <= expect + 3:
        return n, 1
    return None, 0


def read_volume(pkg, pages, V, surname):
    body_h = common_height(pages)
    head_y = head_place(pages)
    # the body: from item 1's heading to the first page headed Appendix
    parts, folios = [], {}
    for i, (W, H, ws) in enumerate(pages, 1):
        lines, folio = page_parts(W, H, ws, body_h, head_y, surname)
        parts.append(lines)
        folios[i] = folio
    first = None
    for i, lines in enumerate(parts, 1):
        if any(sz == "L" and is_item_head(r, 1)[0] == 1 for pos, r, sz in lines) and i > 8:
            # item 1 follows the List of Items; the half title has no number
            first = i
            break
    end = len(pages) + 1
    for i in range(first, len(pages) + 1):
        W, H, ws = pages[i - 1]
        rows = rows_of(ws) if ws else []
        if rows and re.search(r"Appendix|APPENDIX", line_text(rows[0][1])):
            end = i
            break
        if rows and re.fullmatch(r"\s*(INDEX|Index)\s*", line_text(rows[0][1])):
            end = i
            break
    listed = list_of_items(pages, body_h, first - 1)
    off, runs = folio_runs({p: f for p, f in folios.items() if first <= p < end}, len(pages))
    runs = [r for r in runs if r[1] >= first and r[0] < end]
    printed = lambda p: p - off[p] if p in off else None

    items = []
    expect = 1
    cur = None
    para = None           # [kind, [texts]]
    note = False

    def close_para():
        nonlocal para
        if para and cur is not None and para[1]:
            cur["blocks"].append((para[0], para[1]))
        para = None

    for p in range(first, end):
        lines = parts[p - 1]
        if not lines:
            continue
        lefts, widths = {}, {}
        for pos in ("L", "R", "S"):
            xs = sorted(r[0][0] for q, r, sz in lines if q == pos and sz != "L")
            xe = sorted(r[-1][2] for q, r, sz in lines if q == pos and sz != "L")
            if xs:
                lefts[pos] = xs[len(xs) // 8]
                widths[pos] = xe[-1 - len(xe) // 8] - lefts[pos]
        pending = f"[p. {printed(p)}]" if printed(p) is not None else None
        k = 0
        while k < len(lines):
            pos, r, sz = lines[k]
            if sz == "L":
                n, used = is_item_head(r, expect)
                lp = listed.get(n, (None, None))[1] if n else None
                if n is not None:
                    close_para()
                    head = [line_text(r[used:])]
                    k += 1
                    while k < len(lines) and lines[k][2] == "L" and is_item_head(lines[k][1], n + 1)[0] is None:
                        head.append(line_text(lines[k][1]))
                        k += 1
                    cur = {"n": n, "head": " ".join(head), "pdf": p, "page": printed(p), "last": p, "blocks": []}
                    items.append(cur)
                    expect = n + 1
                    note = False
                    pending = None          # the item's first block takes its page's marker
                    continue
            if cur is None:
                k += 1
                continue
            cur["last"] = p
            t = line_text(r)
            indent = r[0][0] - lefts.get(pos, r[0][0])
            colw = widths.get(pos) or 200
            if sz == "s" and not note and re.match(r"^\W{0,2}(note|NOTE|Note)\s*[:;.]", t):
                note = True
                close_para()
            kind = "n" if note else ("h" if sz == "L" else ("q" if sz == "s" else "p"))
            setoff = indent > colw * .34 and sz != "L"
            if setoff:
                kind = "n" if note else "s"
            if para is None or para[0] != kind or setoff or para[0] == "s" or indent > body_h * .6:
                close_para()
                para = [kind, []]
            if pending:
                para[1].append(pending)
                pending = None
            para[1].append(t)
            k += 1
    close_para()
    # the blocks' text: lines joined (STYLE 4), words put right (STYLE 5)
    out = []
    for it in items:
        blocks = []
        for kind, ls in it["blocks"]:
            t = join_lines(ls, V)
            if not t or t.startswith("[p.") and re.fullmatch(r"(\[p\. \d+\]\s*)+", t):
                if t and blocks:
                    blocks[-1][1] += " " + t.strip()
                elif t:
                    blocks.append(["p", t.strip()])
                continue
            if kind == "p" and re.match(r"^(\[p\. \d+\] )?\[(?!\d+\.\])", t) and t.rstrip().endswith("]"):
                kind = "b"
            if kind == "q" and re.match(r"^(\[p\. \d+\] )?[\*†‡§¹²³]|^(\[p\. \d+\] )?\d{1,2} [A-Z]", t):
                kind = "f"
            blocks.append([kind, t])
        # the marker of the item's first page first (STYLE: every item's first block begins with it)
        mk = f"[p. {it['page']}]" if it["page"] is not None else None
        if mk and blocks and not blocks[0][1].startswith(mk):
            blocks[0][1] = mk + " " + blocks[0][1]
        head = fix_line(it["head"], V)
        ds = dates_in(head)
        date = ds[-1][2] if ds else None
        title = head
        if ds:
            a, b, _ = ds[-1]
            tail = head[b:].strip(" .")
            if not tail and re.search(r"[.,]\s*$", head[:a]):
                title = head[:a].rstrip(" .,")
        title = re.sub(r"\s+", " ", title).strip().rstrip(".")
        n = it["n"]
        lp = listed.get(n, (None, None))[1]
        out.append({"n": n, "title": title, "date": date, "page": it["page"],
                    "page_to": printed(it["last"]), "pdf": it["pdf"], "pdf_to": it["last"], "list_page": lp,
                    "text": blocks})
    return out, runs, listed, first, end


SOFT = "\xad"


def fix_line(t, V):
    return " ".join(fix_word(w, V) for w in t.split())


def join_lines(ls, V):
    out = ""
    for l in ls:
        l = l.strip()
        if not l:
            continue
        if not out:
            out = l
            continue
        if out.endswith(SOFT):
            out = out[:-1] + l
        elif out.endswith("-") and not out.endswith("--"):
            a = re.search(r"(\w+)-$", out)
            b = re.match(r"(\w+)", l)
            if a and b and V.n(a.group(1) + b.group(1)) > V.n(a.group(1) + "-" + b.group(1)):
                RULES["hyphen at a line's end dropped (the word printed whole elsewhere)"] += 1
                out = out[:-1] + l
            else:
                out = out + l
        elif out.endswith(("—", "–")) or l.startswith("—"):
            out = out + l
        else:
            out = out + " " + l
    out = out.replace(SOFT, "")
    out = fix_line(out, V)
    out = re.sub(r"\s+([,.;:])(?=\s|$)", r"\1", out)
    return out.strip()


def vocab(all_pages):
    c = collections.Counter()
    for pages in all_pages:
        for W, H, ws in pages:
            for w in ws:
                c[core(w[4].replace(SOFT, ""))[1]] += 1
    return Vocab(c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    ap.add_argument("--vol", nargs="*")
    ap.add_argument("--keep-pdf", action="store_true")
    ap.add_argument("--report")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    vols = [v for v in VOLS if not a.vol or v[0] in a.vol]
    paths = {v[0]: fetch(v[0], a.cache, a.keep_pdf) for v in vols}
    # the vocabulary: every volume's words (STYLE 4, 5), from every volume cached
    allp = {}
    for v in VOLS:
        p = os.path.join(a.cache, f"{v[0]}.bbox.html.gz")
        if os.path.exists(p):
            allp[v[0]] = read_pages(p)
    V = vocab(allp.values())
    rules = {}
    rp = os.path.join(OUT, "rules.json")
    if os.path.exists(rp):
        rules = json.load(open(rp, encoding="utf-8"))
    report = []
    for pkg, years, pres, book, lo, hi in vols:
        RULES.clear()
        pages = allp[pkg]
        items, runs, listed, first, end = read_volume(pkg, pages, V, pres.split()[-1])
        doc = {"source": SOURCE, "license": LICENSE, "package": pkg,
               "title": f"Public Papers of the Presidents of the United States: {pres}, {years}"
                        + (f", Book {'I' * book}" if book else ""),
               "president": pres, "years": years, "book": book, "span": [lo, hi],
               "pdf": pdf_url(pkg), "details": f"{GOV}/app/details/{pkg}", "pages": len(pages),
               "body": [first, end - 1], "folios": runs, "items": items}
        data = json.dumps(doc, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        with open(os.path.join(OUT, f"{pkg}.json.xz"), "wb") as f:
            f.write(lzma.compress(data, preset=9 | lzma.PRESET_EXTREME))
        rules[pkg] = dict(RULES)
        gaps = [it["n"] for it in items if it.get("n") and False]
        miss = sorted(set(listed) - {it["n"] for it in items})
        off = [it["n"] for it in items if it["list_page"] and it["page"] and it["list_page"] != it["page"]]
        line = (f"{pkg}: pages {first}-{end - 1}, items {len(items)} (listed {len(listed)}), not found {len(miss)} "
                f"{miss[:20]}, listed page differs {len(off)} {off[:20]}, no date "
                f"{sum(1 for it in items if not it['date'])}, size {len(data):,}")
        print(line)
        report.append(line)
    with open(rp, "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    if a.report:
        open(a.report, "w").write("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
