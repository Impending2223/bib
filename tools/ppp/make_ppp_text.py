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
    `s`), but not for a line opening lower case after one that does not end a sentence (a list item's hanging
    line); a bracketed note opening a paragraph stands apart. Lines joined with a space; a line ending in a soft hyphen (ABBYY's mark of a word broken at the line's end)
    joined without it; a line ending in a hyphen joined keeping it, unless the volumes print the word whole more
    often than hyphenated; a line ending in a dash joined without a space.
 5. Misreadings put right by rule, each counted in rules.json: digits read as letters inside a number ("I961",
    "i960", "4I", "196r", "S31"); "J" read as "I" or "]" at a word's start ("Iuly", "]ohn"), where the volumes print
    the J form at least three times as often and the I form is not a word of its own (IWORDS); "£" for "f"; stray
    marks ('‘I', '|') alone on a line. Nothing else is guessed: a misreading no rule meets stands, as printed.
 6. Notes: a small-type paragraph opening "NOTE:" (ABBYY reads the small capitals "note:") begins the editors'
    note, and what follows in the item is note. A small-type paragraph before it opening with a mark ("*", "1") is a
    footnote, moved with the small type after it to the item's end (the paragraph it cut at a column's foot joined
    again); any other is `q`. A speaker's name in small capitals that ABBYY reads lower case ("the president.") is
    set in capitals. A body paragraph in square brackets (not a news conference's "[1.]") is `b`.
 7. Pages: the folios read (the bottom line's number, misread digits allowed) give each PDF page's offset, kept
    where it is the commonest offset of the folios read within ten pages and three agree; a page whose folio is not
    read, or not kept, takes the offset of the kept pages on either side where they agree, else the nearer.
"""
import argparse
import collections
import datetime
import difflib
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
    ("PPP-1965-book1", "1965", "Lyndon B. Johnson", 1, "1965-01-01", "1965-05-31"),
    ("PPP-1965-book2", "1965", "Lyndon B. Johnson", 2, "1965-06-01", "1965-12-31"),
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
         "T": "7", "Z": "2", "z": "2", "B": "8", "g": "9", "r": "1", "t": "1", "y": "7", "j": "1", "J": "1"}


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


DAYCHARS = {"n": "11", "u": "11", "y": "7", "z": "2", "Z": "2", "]": "1", "T": "7", "?": "", ".": "", "/": "",
            ",": "", "I": "1", "l": "1", "i": "1", "O": "0", "o": "0", "S": "5", "s": "5", "g": "9", "q": "9",
            "B": "8", "|": "1", "!": "1", "t": "1", "r": "1"}


def heading_date(head, span):
    """(iso date, iso month, where the date begins): the last date in a heading, its misreadings allowed: the month
    by its letters ('Nov ember', 'Qctober', 'Iuly'), the day by DAYCHARS ('n' 11, 'io' 10, 'ly' 17), the year from
    the volume's span where it is misread or lost ('196]', '961'). A day not read gives the month alone."""
    head = re.sub(r",(?=\d{4})", ", ", head)
    toks = list(re.finditer(r"\S+", head))
    lo, hi = (datetime.date.fromisoformat(x) for x in span)
    best = None
    for i, m in enumerate(toks):
        for j in (1, 2):
            if i + j > len(toks) or (j == 2 and not re.fullmatch(r"[a-z]+", toks[i + 1].group())):
                continue
            w = re.sub(r"[^A-Za-z]", "", "".join(t.group() for t in toks[i:i + j]))
            if len(w) < 3 or not w[:1].isupper() and w[:1] not in "Qq]" \
                    and not re.fullmatch(r"(ft|f)u?(ly|ine|ne)", w):
                continue
            mo = None
            loose = False
            for k, M in enumerate(MONTHS):
                r_ = difflib.SequenceMatcher(None, w.lower(), M.lower()).ratio()
                if w == M or (len(w) >= 4 and r_ >= .8):
                    mo = k + 1
                elif len(w) >= 4 and r_ >= .6 and mo is None:
                    mo, loose = k + 1, True
            if mo is None and re.fullmatch(r"([IJ\]]|ft|f|T)u?(ly|ine|ne)", w):        # 'Iuly', ']une', 'ftine'
                mo = 7 if w.endswith("ly") else 6
            if mo is None:
                continue
            rest = [t.group() for t in toks[i + j:i + j + 3]]
            day = year = None
            if rest:
                d = "".join(DAYCHARS.get(c, c) for c in rest[0])
                if re.fullmatch(r"\d{1,2}", d) and 1 <= int(d) <= 31:
                    day = int(d)
                    yt = rest[1] if len(rest) > 1 else ""
                else:
                    yt = rest[0]
                y = "".join(DAYCHARS.get(c, c) for c in yt)
                if re.fullmatch(r"19\d\d", y):
                    year = int(y)
            if loose and not (day and year):
                continue                          # a month read loosely only with its day and year
            years = [year] if year and lo.year <= year <= hi.year else list(range(lo.year, hi.year + 1))
            ok = []
            for yy in years:
                try:
                    dd = datetime.date(yy, mo, day or 1)
                except ValueError:
                    continue
                if (dd.year, dd.month) >= (lo.year, lo.month) and (dd.year, dd.month) <= (hi.year, hi.month):
                    ok.append(dd)
            if len(ok) == 1:
                dd = ok[0]
                best = (dd.isoformat() if day else None, dd.isoformat()[:7], m.start())
                break
    if best is None:
        return None, None, None
    return best


def settle_dates(items, span):
    """Items run in date order: a date out of order with both neighbours, or a month alone between neighbours of
    one day, is put right from them (counted); a date still out of order is dropped to its month."""
    ds = [it["date"] for it in items]
    for i, it in enumerate(items):
        prev = next((d for d in reversed(ds[:i]) if d), None)
        nxt = next((d for d in ds[i + 1:] if d), None)
        d = it["date"]
        if d and prev and nxt and prev <= nxt and not (prev <= d <= nxt):
            RULES["a heading's date out of order, read again from its neighbours"] += 1
            d = prev if prev == nxt else None
            it["month"] = prev[:7] if prev[:7] == nxt[:7] else it["month"]
        if not d and prev and nxt and prev == nxt and (not it["month"] or it["month"] == prev[:7]):
            RULES["a heading's day not read, given by its neighbours (the same day)"] += 1
            d = prev
        it["date"] = d
        ds[i] = d
        if d:
            it["month"] = d[:7]
    for i, it in enumerate(items):        # where a dateless item is filed: the date of the item before it
        if not it["date"]:
            prev = next((x["date"] for x in reversed(items[:i]) if x["date"]), None)
            nxt = next((x["date"] for x in items[i + 1:] if x["date"]), None)
            m = it["month"]
            if prev and (not m or prev[:7] == m):
                it["filed"] = prev
            elif nxt and (not m or nxt[:7] == m):
                it["filed"] = nxt
            else:
                it["filed"] = f"{m}-01" if m else (prev or nxt)


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
        if (head_y is not None and abs(min(w[1] for w in r) - head_y) < 9 and (
                re.search(r"\[\s*\S{1,4}\s*\]|Papers|Presidents|Appendix|Index|" + surname, t)
                or re.search(r"\b(Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)\b", t))
                or yc < H * .14 and re.search(r"Public Papers of|" + surname + r",\s*[1Iil]9", t)) \
                and len(r) <= 12:
            ws = [w for w in ws if w not in r]
            rows = rows[1:]
    # the printer's signature mark ('715-406 0—64—2'), at the foot of a signature's first page
    for yc, r in list(rows[-2:]):
        if yc > H * .8 and any(re.match(r"^\d{2,3}[-—–]\d{3}", w[4]) for w in r):
            k = next(i for i, w in enumerate(r) if re.match(r"^\d{2,3}[-—–]\d{3}", w[4]))
            RULES["printer's signature mark dropped"] += 1
            ws = [w for w in ws if w not in r[k:]]
            rows = rows_of(ws) if ws else []
            break
    # the folio
    if rows:
        yc, r = rows[-1]
        t = " ".join(w[4] for w in r)
        n = as_number(t.replace(" ", "")) if len(r) <= 2 else None
        if n is not None and yc > H * .7:
            folio = n
            ws = [w for w in ws if w not in r]
        elif len(r) == 1 and yc > H * .85 and len(t) <= 4 and (re.search(r"\d", t) or re.fullmatch(r"[lIJyi|]{1,3}", t)):
            RULES["a folio misread past reading, dropped"] += 1
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
    wide = body_h * .9
    rows = rows_of(ws)
    score = [0] * (int(W) + 2)
    for yc, r in rows:                            # the rows with a wide gap at x: a gutter there
        for u, v in zip(r, r[1:]):
            if v[0] - u[2] >= wide:
                for x in range(max(lo, int(u[2]) + 1), min(hi, int(v[0])) + 1):
                    score[x] += 1
    best = max(score[lo:hi + 1]) if hi > lo else 0
    if best < 3:                                  # one column (a table, a text across the page)
        return [("S", r, size(med([w[3] - w[1] for w in r]))) for yc, r in rows], folio
    cands = [x for x in range(lo, hi + 1) if score[x] == best]
    g = min(cands, key=lambda x: abs(x - (left + right) / 2))
    L, R, S = [], [], []
    for yc, r in rows:
        l = [w for w in r if (w[0] + w[2]) / 2 < g]
        rr = [w for w in r if (w[0] + w[2]) / 2 >= g]
        across = any(w[0] < g - 1 and w[2] > g + 1 and len(re.sub(r"\W", "", w[4])) >= 2 for w in r) \
            or any(w[3] - w[1] > body_h * 1.15 for w in r) \
            or (l and rr and rr[0][0] - l[-1][2] < wide)
        if across:
            S += r
        else:
            L += l
            R += rr
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
    elif re.fullmatch(r"[\dioIlOS]+(st|nd|rd|th)", w) and re.search(r"\d", w) and not re.fullmatch(r"\d+(st|nd|rd|th)", w):
        RULES["letters read for digits in an ordinal (iooth, 6oth)"] += 1
        k = re.search(r"(st|nd|rd|th)$", w).start()
        w = "".join(DIGIT.get(c, c) for c in w[:k]) + w[k:]
    elif w[0] in "]I" and len(w) > 2 and w[1].islower() and w not in IWORDS:
        j = "J" + w[1:]
        if w[0] == "]" or (V.n(j) >= 3 * max(1, V.n(w)) and V.n(j) >= 3):
            RULES[f"J read as {w[0]} at a word's start"] += 1
            w = j
    if len(w) >= 3 and V.n(w) <= 2 and w not in REAL and re.fullmatch(r"[A-Za-z]+", w):
        for x, y in CONFUSE:
            i = w.find(x)
            while i >= 0:
                c = w[:i] + y + w[i + len(x):]
                if V.n(c) >= max(1000 if w[0].isupper() else 100, 300 * V.n(w)):
                    RULES[f"'{x}' read for '{y}' (the word printed so 300 times as often)"] += 1
                    return a + c + z
                i = w.find(x, i + 1)
    return a + w + z


# letters the OCR confuses (STYLE 5): a word read with one of them, printed at most twice in the volumes, is put right
# where the other form is printed 300 times as often (and 100 at least; a capitalized word, 1,000); never a word of REAL
CONFUSE = [("li", "h"), ("rn", "m"), ("c", "e"), ("n", "u"), ("u", "n"), ("ri", "n"), ("in", "m"), ("ni", "m"),
           ("cl", "d"), ("h", "b"), ("b", "h"), ("f", "t"), ("t", "f"), ("o", "e"), ("i", "l"), ("l", "i"),
           ("Pv", "R"), ("ii", "u"), ("tl", "d")]
REAL = {"hook", "hooks", "bearing", "bearings", "clay", "clays", "coined", "coining", "hare", "howl", "hunch", "mall",
        "sate", "tights", "toe", "oft", "infer", "fives", "solves", "hero", "Hero", "muse", "mariner", "bard",
        "beard", "bats", "clan", "clue", "liar", "lauded", "taut", "bis", "Klans", "sou", "Mau", "tilling",
        "lien", "liens", "hale", "bale", "hob", "nub", "tab", "fen", "fin", "tins", "fun", "coin", "bunt", "bent",
        "rani", "Rani", "Lin", "Ivan", "Iran", "Ili", "Ilo", "Rio", "Hue", "Hué", "Tuy", "Bien", "Hoa", "Binh"}


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
    # keep a read folio only where its offset is the commonest of the folios read within ten pages, and at least
    # three agree (a digit misread on two or three pages together does not make a run)
    good = []
    for i, (p, off) in enumerate(read):
        near = [o for q, o in read if abs(q - p) <= 10]
        top = collections.Counter(near).most_common(1)[0]
        if off == top[0] and top[1] >= 3:
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


def is_item_head(r, expect, left=None, bh=8.6, nxt=None):
    """(number, words used) where a large line opens an item (STYLE 3): its first word the next number, read with
    the digits' misreadings; or, at the text's left edge with the title after a gap, a short word no rule reads
    ('no', 'X47', 'yj'): the number the sequence gives, counted."""
    if len(r) == 1 and as_number(r[0][4]) == expect and left is not None and nxt:
        RULES["a heading's title lost (its number and date alone)"] += 1
        return expect, 1                          # the title from the List of Items
    if len(r) < 2:
        return None, 0
    n = as_number(r[0][4])
    for k in (3, 2):                              # a number read apart ('i o i', 'i 83')
        if (n is None or not expect <= n <= expect + 3) and len(r) > k and all(len(w[4]) <= 2 for w in r[:k]) \
                and r[k - 1][2] - r[0][0] < bh * 4.5:
            j = "".join(DIGIT.get(c, c) for c in "".join(w[4] for w in r[:k]))
            n2 = int(j) if j.isdigit() else None
            if n2 is not None and expect <= n2 <= expect + 3:
                return n2, k
    if n is not None and expect <= n <= expect + 3:
        if not re.search(r"[A-Za-z]{3}", line_text(r[1:])):
            return None, 0                        # no title after it: the half title's year ('1 9 6 3')
        return n, 1
    k = 1
    while k < len(r) - 1 and k < 3 and len(r[k][4]) <= 2 and not r[k][4][:1].isupper():
        k += 1                                    # 'hi *1', '112 ?'
    if left is not None and len(r[0][4]) <= 4 and r[k][4][:1].isupper() and r[1][0] - r[0][2] > bh * .3 \
            and (r[0][0] <= left + bh * 1.5 or (nxt and nxt[0][0][0] >= r[0][0] - 2)):
        digits = re.sub(r"\D", "", r[0][4].replace("°", "0"))
        it = iter(str(expect))
        blk = line_text(r) + " " + " ".join(line_text(x) for x in (nxt or []))
        if re.search(r"Public Papers|\[\s*\S{1,4}\s*\]\s*$", line_text(r)):
            return None, 0                        # a running head the page's reading kept
        e = str(expect)
        if (digits and all(c in it for c in digits)) or (            # its digits read, in order
                len(digits) == len(e) > 1 and sum(a != b for a, b in zip(digits, e)) == 1) or (
                not digits and re.search(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b", blk)):
            RULES["item number misread, taken from the sequence"] += 1
            return expect, k
    return None, 0


def number_alone(lines, bh):
    """A heading's number set alone on its line, between the title's lines (the OCR's rows): put before the line
    above it, as one line."""
    out = list(lines)
    i = 1
    while i < len(out):
        pos, r, sz = out[i]
        if sz == "L" and len(r) == 1 and as_number(r[0][4]) is not None and out[i - 1][2] == "L" \
                and out[i - 1][1][0][0] > r[0][2] and len(out[i - 1][1]) > 1:
            RULES["a heading's number alone on its line, joined to the title"] += 1
            out[i - 1] = (out[i - 1][0], r + out[i - 1][1], "L")
            del out[i]
            continue
        i += 1
    return out


def read_volume(pkg, pages, V, surname, span, start=1):
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
        top = rows_of(pages[i - 1][2])[0][1] if pages[i - 1][2] else []
        if re.search(r"list|item|content|foreword|preface", line_text(top), re.I):
            continue                              # the front matter: the List of Items repeats the headings
        if any(sz == "L" and is_item_head(r, start)[0] == start for pos, r, sz in lines) and i > 8:
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
    expect = start
    cur = None
    para = None           # [kind, [texts]]
    para_pos = None
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
        lines = number_alone(lines, body_h)
        k = 0
        prev_sz = None
        while k < len(lines):
            pos, r, sz = lines[k]
            prev_sz, sz0 = (lines[k - 1][2] if k else None), sz
            if sz == "L":
                nxt = []                                  # the heading's next large lines
                for x in lines[k + 1:k + 4]:
                    if x[2] != "L":
                        break
                    nxt.append(x[1])
                n, used = is_item_head(r, expect, min(lefts.values()) if lefts else None, body_h, nxt)
                if n is None and prev_sz != "L" and cur is not None and r[0][4][:1].isupper():
                    # a heading whose number the OCR lost: a large block with a date of the item's period
                    blk = [line_text(r)] + [line_text(x[1]) for x in lines[k + 1:k + 4] if x[2] == "L"][:2]
                    dd, mm, cut = heading_date(" ".join(blk), span)
                    if mm and (cur.get("hd") or "0000") <= (dd or mm + "-31") and cut is not None:
                        RULES["item number lost, taken from the sequence (a large heading with a date)"] += 1
                        n, used = expect, 0
                if n is not None:
                    close_para()
                    head = [line_text(r[used:])]
                    k += 1
                    while k < len(lines) and lines[k][2] == "L" and (
                            lines[k][1][0][0] > r[0][0] + body_h * 1.5
                            or is_item_head(lines[k][1], n + 1, None, body_h)[0] is None):
                        head.append(line_text(lines[k][1]))
                        k += 1
                    cur = {"n": n, "head": " ".join(head), "pdf": p, "page": printed(p), "last": p, "blocks": []}
                    cur["hd"] = heading_date(cur["head"], span)[0]
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
            # the column's left edge here: the least start of its lines near this one (a skewed scan drifts)
            near = [x[1][0][0] for x in lines[max(0, k - 5):k + 6] if x[0] == pos and x[2] != "L"]
            edge = min(near) if len(near) >= 4 else lefts.get(pos, r[0][0])
            indent = r[0][0] - max(edge, lefts.get(pos, edge) - body_h * 2)
            colw = widths.get(pos) or 200
            if sz == "s" and not note and re.match(r"^\W{0,2}(note|NOTE|Note)\s*[:;.]", t):
                note = True
                close_para()
            kind = "n" if note else ("h" if sz == "L" else ("q" if sz == "s" else "p"))
            setoff = indent > colw * .34 and sz != "L"
            hanging = (para is not None and para[0] == kind and t[:1].islower() and para[1]
                       and not re.search(r"[.?!:]$", para[1][-1]))        # a list item's hanging line
            if setoff and not hanging:
                kind = "n" if note else "s"
            across = pos == "S"
            if para is None or para[0] != kind or (setoff and not hanging) or para[0] == "s" \
                    or (indent > body_h * .6 and not hanging) \
                    or (para_pos is not None and (para_pos == "S") != across):
                close_para()
                para = [kind, []]
            if pending:
                para[1].append(pending)
                pending = None
            para[1].append(t)
            para_pos = pos
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
            if kind == "b":
                t = re.sub(r"\[\s+", "[", re.sub(r"\s+\]", "]", t))
            if kind == "q" and re.fullmatch(r"(\[p\. \d+\] )?[^a-z]*[A-Z]{3}[^a-z]*", t):
                kind = "h"                                # a heading in small capitals
            if kind == "q" and re.match(r"^(\[p\. \d+\] )?([\*†‡§¹²³]|\d{1,2} ?[A-Z])", t):
                kind = "f"
            if kind == "n" and re.match(r"^(\[p\. \d+\] )?\W{0,2}note\s*[:;.]\s*", t, re.I):
                t = re.sub(r"^((?:\[p\. \d+\] )?)\W{0,2}note\s*[:;.]\s*", r"\1NOTE: ", t, flags=re.I)
            blocks.append([kind, t])
        blocks = tidy(blocks)
        # the marker of the item's first page first (STYLE: every item's first block begins with it)
        mk = f"[p. {it['page']}]" if it["page"] is not None else None
        if mk and blocks and not blocks[0][1].startswith(mk):
            blocks[0][1] = mk + " " + blocks[0][1]
        head = fix_line(it["head"], V)
        date, month, cut = heading_date(head, span)
        title = head
        if cut is not None and re.search(r"[.,]\s*$", head[:cut]):
            title = head[:cut].rstrip(" .,")
        title = re.sub(r"\s+", " ", title).strip().rstrip(".")
        t2 = re.sub(r"^(?:[^A-Za-z0-9“\"‘(\s]\S{0,2}|[a-z]{1,2})\s+(?=[A-Z“\"])", "", title)
        if t2 != title:
            RULES["a stray mark before a heading's title, dropped"] += 1
            title = t2
        title = title or "[Title not read]"
        if title == "[Title not read]" and it["n"] in listed and listed[it["n"]][1] is not None \
                and it["page"] is not None and abs(listed[it["n"]][1] - it["page"]) <= 1:
            lt = fix_line(listed[it["n"]][0], V)
            title = re.sub(r"[.,]?\s*(" + "|".join(MONTHS) + r")\s+\d{1,2},\s*\d{4}\s*$", "", lt).strip().rstrip(".")
        n = it["n"]
        lp = listed.get(n, (None, None))[1]
        out.append({"n": n, "title": title, "date": date, "month": month, "page": it["page"],
                    "page_to": printed(it["last"]), "pdf": it["pdf"], "pdf_to": it["last"], "list_page": lp,
                    "text": blocks})
    return out, runs, listed, first, end


SOFT = "\xad"
MK = re.compile(r"^((?:\[p\. \d+\] ?)*)")
SPEAKER = re.compile(r"^((?:\[p\. \d+\] )?)((?:the (?:vice )?president|The President|mr\.|mrs\.|miss|secretary|senator|"
                     r"ambassador|governor|mayor|general|admiral)(?: [a-z][a-z’'.-]+){0,2})\.\s")


def tidy(blocks):
    """An item's blocks put in order (STYLE 4, 6): a speaker's name in small capitals that ABBYY read lower case
    ("the president.") in capitals, its line body text; a bracketed note opening a paragraph ("[Released May 16, 1960.
    Dated May 14, 1960]") a block of its own; the footnotes (and the small type running on from them) moved from where
    the page's foot put them to the item's end, the paragraph they cut joined again."""
    out = []
    for k, t in blocks:
        m = SPEAKER.match(t)
        if m and k in ("p", "q"):
            RULES["a speaker's small capitals read lower case, set in capitals"] += 1
            t = m.group(1) + m.group(2).upper() + ". " + t[m.end():]
            k = "p"
        m = re.match(r"^((?:\[p\. \d+\] )?)(\[(?!\d+\.\])[^\[\]]{4,900}\])\s+(\S.*)$", t)
        if m and k == "p":
            out.append(["b", m.group(1) + re.sub(r"\[\s+", "[", re.sub(r"\s+\]", "]", m.group(2)))])
            out.append(["p", m.group(3)])
            continue
        out.append([k, t])
    body, feet, i = [], [], 0
    while i < len(out):
        k, t = out[i]
        if k == "f":
            j = i + 1
            while j < len(out) and out[j][0] in ("f", "q"):
                j += 1
            mk = "".join(MK.match(x[1]).group(1) for x in out[i:j])
            feet += [[x[0], x[1][len(MK.match(x[1]).group(1)):]] for x in out[i:j]]
            nxt = out[j] if j < len(out) else None
            if nxt and mk:
                nxt[1] = mk.strip() + " " + nxt[1]
            if body and nxt and body[-1][0] == "p" and nxt[0] == "p" and not re.search(r"[.?!:”\"’)\]]$", body[-1][1]) \
                    and not re.match(r"^(\[p\. \d+\] )?[\[“\"]|^(\[p\. \d+\] )?Q\.", nxt[1]):
                body[-1][1] += " " + nxt[1]           # the paragraph the foot of the column cut
                j += 1
            RULES["footnotes moved to the item's end"] += 1
            i = j
            continue
        body.append([k, t])
        i += 1
    return body + feet


def fix_line(t, V):
    ws = [fix_word(w, V) for w in t.split()]
    out = []
    i = 0
    while i < len(ws):
        w = ws[i]
        # a small capital's initial set apart ('J ohn F. K ennedy'): joined where the volumes print the word whole
        if re.fullmatch(r"[A-Z]", w) and i + 1 < len(ws):
            a, b, z = core(ws[i + 1])
            if not a and re.fullmatch(r"[a-z]{2,}", b) and V.n(w + b) >= 3 and V.n(w + b) > V.n(b):
                RULES["a small capital's initial set apart, joined"] += 1
                out.append(w + ws[i + 1])
                i += 2
                continue
        out.append(w)
        i += 1
    return " ".join(out)


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
        start = 1
        if book == 2:                     # the second book goes on with the first's numbers
            prev = os.path.join(OUT, f"{VOLS[[v[0] for v in VOLS].index(pkg) - 1][0]}.json.xz")
            start = json.loads(lzma.decompress(open(prev, "rb").read()))["items"][-1]["n"] + 1
        items, runs, listed, first, end = read_volume(pkg, pages, V, pres.split()[-1], (lo, hi), start)
        settle_dates(items, (lo, hi))
        doc = {"source": SOURCE, "license": LICENSE, "package": pkg,
               "title": f"Public Papers of the Presidents of the United States: {pres}, {years}"
                        + (f", Book {'I' * book}" if book else ""),
               "president": pres, "years": years, "book": book, "span": [lo, hi],
               "pdf": pdf_url(pkg), "details": f"{GOV}/app/details/{pkg}", "pages": len(pages),
               "body": [first, end - 1], "folios": runs,
               "missing": [n for n in range(items[0]["n"], items[-1]["n"] + 1) if n not in {x["n"] for x in items}],
               "items": items}
        data = json.dumps(doc, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        with open(os.path.join(OUT, f"{pkg}.json.xz"), "wb") as f:
            f.write(lzma.compress(data, preset=9 | lzma.PRESET_EXTREME))
        rules[pkg] = dict(RULES)
        line = (f"{pkg}: PDF pages {first}-{end - 1}, items {len(items)} ({items[0]['n']}-{items[-1]['n']}), "
                f"missing {doc['missing']}, no day {sum(1 for it in items if not it['date'])}, "
                f"listed pages agreeing {sum(1 for it in items if it['list_page'] == it['page'])}, "
                f"{len(data):,} bytes")
        print(line)
        report.append(line)
    with open(rp, "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    if a.report:
        open(a.report, "w").write("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
