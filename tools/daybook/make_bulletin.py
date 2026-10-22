"""Write daybook/bulletin/<YYYY>.yaml: the *Department of State Bulletin*'s contents, item by item, filed by day.

    python3 tools/daybook/make_bulletin.py YEAR [YEAR ...] [--cache DIR]   (DIR: make_dsb_index.py's cache; network
                                                                            for what it lacks; the build needs none)

For each issue of the year (sources/dsb-issues.yaml, its first and last pages), from the Boston Public Library's copy on
archive.org, page by page (the hOCR text and the page numbers make_dsb_index.py reads):

 1. The issue's own index, on its inside back cover ("Index / Vol. XLVI, No. 1176"): every entry, "Subject. Title
    (names) page", the subject heading taken off (a line of its own, or the words before the first full stop where
    they are a short heading). An item the index lists under several subjects is one item: the same page and the same
    first words of its title. The title as the OCR reads it, its spaces and hyphens at line breaks mended.
 2. The item's date: where the item's first page prints its release ("Press release 23 dated January 15", "White House
    press release dated ..."), the date it gives (the year the issue's, or the one before for a December release in a
    January issue), not after the issue's date nor more than 60 days before it (`dated: release`); else the issue's
    date (`dated: issue`).
 3. Rows: key ('dsb:<issue date>:<page>:<n>'), src 'dsb', date (the day filed), issue, page, title, url (the copy's
    page). Shown in the daybook as a fifth list, "Bulletin" (tools/bib/daybook.py, STYLE 10).

Quality (1962, the first year done): see the counts this prints; titles keep OCR errors the index's type invited.
"""
import datetime
import gzip
import html
import json
import os
import re
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import make_dsb_index as ix  # noqa: E402
from bib import printed  # noqa: E402

OUT = os.path.join(ROOT, "daybook", "bulletin")
FROM, TO = datetime.date(1960, 1, 6), datetime.date(1969, 1, 20)        # the calendar's first and last days
FULL = ix.FULL
RELEASE = re.compile(r"(?:press\s+release|release)\s+(?:No\.\s*)?(?:\d+\s+)?dated\s+(" + "|".join(FULL)
                     + r")\s+(\d{1,2})", re.I)
NAME = re.compile(r"^[A-Z][\w'’\-]+(?: [A-Z][\w'’\-]+)?, [A-Z][\w.]*(?: [A-Z][\w.]*){0,3}(?:, Jr)?$")   # "Ball, George W"
INDEX = re.compile(r"\b(?:I\s?n\s?d\s?e\s?x|ndex|Inde)\b")
MONTH_END = re.compile(r"\b(?:" + "|".join(FULL) + r"|Jan|Feb|Mar|Apr|Aug|Sept?|Oct|Nov|Dec)\.?$")
LINE_END = re.compile(r"^(.*?\S)\s*[.\s]*?\s(\d{1,4})\s*$")


def mend(t):
    t = re.sub(r"(\w)- (\w)", lambda m: m.group(1) + ("-" if m.group(2)[0].isupper() else "") + m.group(2), t)
    t = re.sub(r"\s+", " ", t).strip(" .")
    return re.sub(r"\s+([,.;:)])", r"\1", t)


def index_entries(text, first, last):
    """(title, page) from an issue's index page text."""
    text = re.split(r"\n\s*N\s*a\s*m\s*e\s+I\s*n\s*d\s*e\s*x\b", text)[0]     # the names' index after it: not items
    # an entry ending mid-line, another after it: "... (Rusk) .. 83 U.S. Refutes ..."
    text = re.sub(r"(\S)\s*\.*\s+(\d{1,4})\s+(?=[A-Z\"“])",
                  lambda m: m.group(1) + " " + m.group(2) + ("\n" if first <= int(m.group(2)) <= last else " "), text)
    lines = [x.strip() for x in text.split("\n")]
    out, buf = [], ""
    for ln in lines:
        if not ln or re.match(r"^(?:Index|Vol\.?\s|[A-Z][a-z]+\s+\d{1,2},\s*\d{4})", ln) and not buf:
            continue
        cur = (buf + " " + ln).strip() if buf else ln
        if re.search(r"\s#$", cur) or len(cur) > 300:
            buf = ""                                     # an entry whose page the OCR could not read
            continue
        m = LINE_END.match(cur)
        if m and first <= int(m.group(2)) <= last and not MONTH_END.search(m.group(1)):   # "June 30": a day
            body = m.group(1)
            sub = re.match(r"^(U\.S\.S\.R|[A-Za-z][\w,'’()\-]*(?:\s+[\w,'’()\-]+){0,4}?)\.\s+(?=[A-Z0-9\"“])", body)
            if sub and not re.search(r"\b(?:U|S|Mr|Mrs|Dr|St|No|[A-Z])$", sub.group(1)) \
                    and sub.group(1).count("(") == sub.group(1).count(")"):      # not "R. A. Egger", "(Sieverts. Tinker)"
                body = body[sub.end():]                 # the subject heading off
            title = mend(body)
            if not NAME.match(title) and not re.search(r"\d,$|,\s*\d{1,4}$", title):    # not a run of pages
                out.append((title, int(m.group(2))))
            buf = ""
        elif len(cur) < 45 and not re.search(r"\d", cur) and not buf:
            buf = ""                       # a subject heading on a line of its own
        else:
            buf = cur
            if len(buf) > 400:
                buf = ""
    return out


_djvu = {}


def djvu(cache, iid):
    """{leaf: (width, [((l, b, r, t), word)])}: the copy's words with their boxes (its _djvu.xml, kept gzipped)."""
    if iid not in _djvu:
        p = os.path.join(cache, iid + ".djvu.xml.gz")
        if not os.path.exists(p) or os.path.getsize(p) < 1000:
            open(p, "wb").write(gzip.compress(ix.fetch(f"https://archive.org/download/{iid}/{iid}_djvu.xml")))
        s = gzip.open(p).read().decode("utf-8", "replace")
        out = {}
        for m in re.finditer(r'<OBJECT[^>]*?usemap="[^"]*?_(\d{4})\.djvu"[^>]*?width="(\d+)".*?</OBJECT>', s, re.S):
            out[int(m.group(1))] = (int(m.group(2)), [(tuple(map(int, c.split(","))), w.strip()) for c, w in
                                                     re.findall(r'<WORD coords="([\d,]+)"[^>]*>(.*?)</WORD>', m.group(0))])
        _djvu.clear()                                  # one copy at a time: they are large
        _djvu[iid] = out
    return _djvu[iid]


_rebuilt = {}


def rebuilt(cache, iid, leaf):
    if (iid, leaf) not in _rebuilt:
        _rebuilt[iid, leaf] = _rebuild(cache, iid, leaf)
    return _rebuilt[iid, leaf]


def _rebuild(cache, iid, leaf):
    """An index page's text laid out again from its words' boxes (RULES 4): the two columns apart (split where fewest
    words cross the middle third), each column's words in rows by their tops, each page number with the row it stands
    beside, and a row run on into the one before where it is indented (an entry's second line; its first line and a
    subject heading stand at the margin). The OCR's own text sometimes
    sets a column's page numbers in a block of their own; this puts each back at the end of its entry."""
    got = djvu(cache, iid).get(leaf)
    if not got or not got[1]:
        return ""
    W, ws = got
    ws = [x for x in ws if not re.match(r"^[.,;:'`•■\-]*$", x[1])]       # the leaders
    num = [x for x in ws if re.match(r"^(?=.*\d.*\d)[\dOoIl^]{2,4}[.,]?$|^\d[.,]?$", x[1])]   # page numbers
    text = [x for x in ws if x not in num]
    cross = [sum(l <= x <= r for (l, b, r, t), w in text) for x in range(W // 3, 2 * W // 3, 5)]
    mid = W // 3 + 5 * min(range(len(cross)), key=lambda i: (cross[i], abs(W // 3 + 5 * i - W // 2)))
    right = sorted(x[0][0] for x in text if (x[0][0] + x[0][2]) / 2 >= mid)
    edge = right[len(right) // 10] if right else mid               # the right column's left edge
    out = []
    for col in (0, 1):
        tx = [x for x in text if ((x[0][0] + x[0][2]) / 2 < mid) == (col == 0)]
        nx = [x for x in num if ((x[0][0] + x[0][2]) / 2 < edge) == (col == 0)]
        hs = sorted(b - t for (l, b, r, t), w in tx) or [30]
        tol = 0.5 * hs[len(hs) // 2]
        rows = []                                      # [top, bottom, [(l, word, r)]]: the text by its tops
        for (l, b, r, t), w in sorted(tx, key=lambda x: x[0][3]):
            if rows and t - rows[-1][0] < tol:
                rows[-1][1] = max(rows[-1][1], b)
                rows[-1][2].append((l, w, r))
            else:
                rows.append([t, b, [(l, w, r)]])
        for (l, b, r, t), w in nx:                     # a number to the row it overlaps most
            if rows:
                best = max(rows, key=lambda r_: (min(b, r_[1]) - max(t, r_[0]), -abs((t + b) - (r_[0] + r_[1]))))
                best[2].append((l, w, r))
        rows = [[r_[0], r_[2]] for r_ in rows]
        starts = [min([l for l, w, r in r_[1] if not re.match(r"^[\d.,;:#]+$", w)] or [l for l, w, r in r_[1]])
                  for r_ in rows]
        ends = [max([r for l, w, r in r_[1] if not re.match(r"^[\d.,;:#]+$", w)] or [0]) for r_ in rows]
        full = sorted(ends)[int(len(ends) * 0.9)] if ends else 0       # where a full line of the column ends
        wrapped = False
        for k, r_ in enumerate(rows):
            ln = html.unescape(" ".join(w for l, w, r in sorted(r_[1])))
            if k < 3 and re.search(r"\bVol\b|\b\S?N\s?D\s?E\s?X\b|\bIndex\b", ln):
                out.append(ln)                          # the page's head: never an entry's first line
                wrapped = False
                continue
            near = sorted(starts[max(0, k - 8):k + 9])
            margin = near[len(near) * 3 // 10]          # the column's left edge here (a scan can be skewed; debris)
            indented = starts[k] - margin > 0.012 * W   # an entry's second line is indented; its first and a heading not
            m = re.match(r"^(.*\S)\s+(\d{1,4})$", out[-1]) if out else None
            if m and m.group(1).endswith("-") and indented and not re.search(r"\s\d{1,4}$", ln):
                out[-1] = f"{m.group(1)} {ln} {m.group(2)}"   # a number set beside an entry's first line
            elif out and (indented or wrapped) and not m:
                out[-1] += " " + ln
            else:
                out.append(ln)
            wrapped = ends[k] >= full - 0.04 * W            # a line run to the column's edge goes on: a gutter can
                                                           # hide the indent
    return "\n".join(out)


def numbers(text):
    """A page number the OCR misread (RULES 6): its O for 0, l or I for 1 ("47O"); one it cannot read ("44^") is #, which
    ends the entry, so that it is not run on into the next."""
    text = re.sub(r"(?<![\w-])(\d{2,3}[Oo]|\d[Oo]\d|[Il]\d{2,3}|\d{2}[Il]|\d[Il]\d)(?![\w-])",
                  lambda m: m.group(1).translate(str.maketrans("OoIl", "0011")), text)
    return re.sub(r"(?<![\w-])\d{2,3}[\^]\w?(?![\w-])", "#", text)


def readings(cache, iid, L, i, lo, hi):
    """An index leaf's entries, from the OCR's text and from its words laid out again (RULES 4)."""
    return index_entries(numbers(L[i][2]), lo, hi) + index_entries(numbers(rebuilt(cache, iid, L[i][0])), lo, hi)


def clean(title):
    """A reading's debris taken off (RULES 8): the page's head before it ("pril 8, 1963 I n d"), a stray mark, "Ind" after
    it; a subject heading the gutter clipped ("azil. U.S. Regrets ...", "eaty Information. Current ..."); "U." lost
    before "S." at the margin; a stop the OCR read inside a word ("Pre.sents", "E.xhibiting", "19.54")."""
    title = re.sub(r"^\S{0,12}\s*\d{1,2}[,.]?\s*19[56]\d\s+(?:I\s?n\s?d\s?(?:e\s?[xX])?\s+)?", "", title)
    title = re.sub(r"\s+(?:Ind|Index|e X)$", "", re.sub(r"^[^A-Za-z0-9\"“‘(]+", "", title))
    title = re.sub(r"^[a-z][\w\-]*(?:\s[\w\-,]+){0,3}\.\s+(?=[A-Z0-9\"“])", "", title)
    title = re.sub(r"(?<=[a-z])[.;](?=[a-z])|(?<=\b[A-Z])\.(?=[a-z]{3})", "", title)   # "Pre.sents", "E.xhibiting"
    title = re.sub(r"\b19\.(\d\d)\b", r"19\1", title)                                 # "19.54"
    return re.sub(r"^S\. (?=[A-Z])", "U.S. ", title)


def garbled(title, first, last):
    """A reading run on into another entry, or the OCR's debris in it: a stray mark, the page's head, a page number."""
    return bool(re.search(r"[\^■»«#|\\*°]|\bVol\.|\be X\b|(?<=\s)0\d{2}(?=\s)|\d,\s?(?!19\d\d\b)\d"
                          r"|\b\d[a-zA-Z]\w?\b(?<!\d[sdht])(?<!\dth)(?<!\dst)(?<!\dnd)(?<!\drd)", title)) or any(
        first <= int(n) <= last for n in re.findall(r"(?<=[\s.)])(\d{2,4})(?=\s+[A-Z]|$)", title))


def best(readings_, first, last):
    """Of the readings of one item, the one to print (RULES 5): not garbled, beginning with a capital; then the one that
    holds the most of the other readings' words (a reading cut short holds fewer); then the one read most often (an
    item stands under several subjects); then the shorter (a reading run on into the next entry is longer). None where
    every reading is garbled."""
    good = [t for t in readings_ if not garbled(t, first, last) and len(t) <= 220]
    def run_on(t, r):                                    # t holds r and more: run on from another entry, or into one
        tw, rw = t.split(), r.split()
        if len(rw) < 3 or len(tw) < len(rw) + 2:
            return False
        tail = sum(a == b for a, b in zip(tw[-len(rw):], rw)) >= 0.75 * len(rw)
        head = sum(a == b for a, b in zip(tw[:len(rw)], rw)) >= 0.75 * len(rw) and not tw[len(rw)].startswith("(")
        return tail or head
    good = [t for t in good if not any(r != t and run_on(t, r) for r in good)]
    if not good:
        return None
    n = {t: good.count(t) for t in good}

    def holds(t):
        wt = words(t)
        return sum(len(words(r) & wt) >= 0.8 * len(words(r)) for r in good)
    return min(good, key=lambda t: (not re.match(r"^[A-Z0-9\"“‘]", t), -holds(t), -n[t], len(t)))


def run_ons(rows):
    """A title that holds the whole title of another item of the same issue (four words at least): two entries read as
    one (RULES 7); left out."""
    by_issue = {}
    for x in rows:
        by_issue.setdefault(x["issue"], []).append(x)
    out = []
    for x in rows:
        t = re.sub(r"\W+", " ", x["title"].lower())
        if any(y is not x and len(y["title"].split()) >= 4 and y["title"] != x["title"]
               and re.sub(r"\W+", " ", y["title"].lower()) in t for y in by_issue[x["issue"]]):
            continue
        out.append(x)
    return out


def capitals(rows):
    """A title whose first letter the binding's gutter took ("resident Kennedy", "roint News Conference"; RULES 7): the
    word the year's titles hold most often (twice at least) with a capital put before it or for its first letter."""
    from collections import Counter
    vocab = Counter(w for x in rows for w in re.findall(r"\b[A-Z][a-z]{2,}\b", x["title"]))
    for x in rows:
        m = re.match(r"^[^A-Za-z0-9(]*([a-z][a-z]+)\b", x["title"])
        if not m:
            continue
        w = m.group(1)
        cands = [c + w for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"] + [c + w[1:] for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        best_ = max(cands, key=lambda c: vocab[c])
        if vocab[best_] >= 2:
            x["title"] = best_ + x["title"][m.end(1):]


def words(title):
    return set(re.findall(r"[a-z]{3,}", title.lower())) - {"the", "and", "for", "text", "with"}


def release_date(text, issue):
    """The one release date a page prints (none where it prints several: whose is whose is not known)."""
    found = RELEASE.findall(text or "")
    if len({(a.lower(), b) for a, b in found}) != 1:
        return None
    for m in RELEASE.finditer(text or ""):
        mon, day = FULL.index(m.group(1).capitalize()) + 1, int(m.group(2))
        y = issue.year - (1 if mon > issue.month + 1 else 0)
        try:
            d = datetime.date(y, mon, day)
        except ValueError:
            continue
        if issue - datetime.timedelta(days=60) <= d <= issue:
            return d
    return None


def leaves(cache, iid):
    """[(leaf, printed page or None, text)] for one copy, in leaf order."""
    pn = json.load(open(ix.cached(cache, iid + ".pn.json", f"https://archive.org/download/{iid}/{iid}_page_numbers.json"),
                        encoding="utf-8"))
    leaf_page = {p["leafNum"]: int(p["pageNumber"]) for p in pn["pages"] if str(p.get("pageNumber") or "").isdigit()}
    pi = json.loads(gzip.open(ix.cached(cache, iid + ".pi.gz",
                                        f"https://archive.org/download/{iid}/{iid}_hocr_pageindex.json.gz")).read())
    st = gzip.open(ix.cached(cache, iid + ".st.gz",
                             f"https://archive.org/download/{iid}/{iid}_hocr_searchtext.txt.gz")).read().decode("utf-8", "replace")
    return [(k, leaf_page.get(k), st[span[0]:span[1]]) for k, span in enumerate(pi)]


HEAD_INDEX = re.compile(r"(?:I\s?I?N|\S)\s?D\s?E\s?X|I\s?n\s?d\s?e\s?[xX]|\bndex\b|\bInde?\b")   # "IIDEX", ">NDEX"
VOL_INDEX = re.compile(r"Volume\s+\S+\s*:?\s*Numbers|Numbers\s+\d{4}\s*-\s*\d{4}")
BACK = re.compile(r"OFFICIAL\s+BUSINESS|PENALTY\s+FOR\s+PRIVATE|POSTAGE\s+AND\s+FEES\s+PAID", re.I)
HEAD_DATE = re.compile(r"(" + "|".join(FULL) + r")\s*(\d{1,2})\s*[,.]\s*(19[56]\d)")
HEAD_NO = re.compile(r"No\.?\s*(1[0-5]\d\d)\b")


def run(pages):
    """The longest run of printed pages rising in leaf order (steps of 1 to 6: plates, numbers the OCR missed)."""
    best, cur = [], []
    for n in pages:
        cur = cur + [n] if cur and 0 < n - cur[-1] <= 6 else [n]
        if len(cur) > len(best):
            best = list(cur)
    return best


def index_leaves(L, lo, hi, R):
    """The leaves of a copy holding an issue's own index (RULES 1): a head with "Index" (not the volume's index), or
    the leaf before the back cover (its mailing text), whose text reads as at least eight index entries within the
    volume's pages, most of them within 150 of one another."""
    out = []
    for i, (k, p, t) in enumerate(L):
        h = t[:250]
        if VOL_INDEX.search(h):
            continue
        before_back = i + 1 < len(L) and BACK.search(L[i + 1][2][:600])
        dated = (m := HEAD_DATE.search(h)) and m.start() < 25          # the issue's date at its head ("March 27, 1961")
        if not (HEAD_INDEX.search(h) or before_back or dated):
            continue
        ents = R(i, lo, hi)
        pg = sorted(e[1] for e in ents)
        if len(pg) < 8:
            continue
        dense = max(sum(a <= x <= a + 150 for x in pg) for a in pg)    # the densest 150 pages: an OCR's 6 for 5
        if dense < max(8, 0.5 * len(pg)):
            continue
        out.append(i)
    return out


OCR_DIGIT = str.maketrans({"I": "1", "l": "1", "J": "1", "i": "1", "|": "1", "£": "2", "Z": "2", "S": "3", "O": "0",
                           "o": "0", "U": "4", "b": "6", "B": "8", "^": "4", "s": "3", "z": "2"})


def evidence(h, q):
    """How well an index leaf's head (its first 120 characters) names issue q: its date or number as printed, else as
    the OCR's misread letters for digits give them (OCR_DIGIT): a month like the printed one, the day, the number's
    last two digits."""
    d = datetime.date.fromisoformat(q["date"])
    h = re.sub(r"\s+", " ", h[:120])
    if re.search(FULL[d.month - 1] + r"\s*" + str(d.day) + r"\s*[,.]\s*" + str(d.year), h):
        return 5
    if re.search(r"No\.?\s*" + str(q["no"]) + r"\b", h):
        return 4
    score = 0
    mon = FULL[d.month - 1].lower()
    for m in re.finditer(r"([A-Za-z^\-.]{3,10})\s*([\dIlJi|£ZSOoUb^]{1,2})\s*[,.]?\s*[J1I]?\s*[\d^SJ]{3}", h):
        w = m.group(1).lower().strip("^-.")
        if len(w) >= 3 and sum(a == b for a, b in zip(w, mon)) >= min(3, len(mon)) - 1 and w[:1] in (mon[0], "^", "-"):
            score += 1
            if m.group(2).translate(OCR_DIGIT) == str(d.day):
                score += 1.5
            break
    m = re.search(r"No\.?\s*(\S{3,5})", h)
    if m and m.group(1).translate(OCR_DIGIT)[-2:] == str(q["no"])[-2:]:
        score += 1
    return score


def median(R, i, lo, hi):
    ents = sorted(x[1] for x in R(i, lo, hi))
    return ents[len(ents) // 2] if ents else 0


def place(L, segs, quarter, lo, hi, R):
    """[(seg, issue)] for one copy's index leaves, in order (RULES 2): the best alignment of the leaves with the issues,
    each leaf one issue or none, by what each head says (evidence) and, where sources/dsb-issues.yaml gives an issue's
    pages, whether they hold the median page of the leaf's entries (never matched where they do not)."""
    def score(s, q):
        e = evidence(L[s[0]][2], q)
        if q.get("first") and q.get("last") and not q.get("check"):
            if not q["first"] <= median(R, s[0], lo, hi) <= q["last"]:
                return None if e < 4 else e + 0.5     # a head's date or number stands over the covers' pages
            e += 3
        elif e == 0 and not HEAD_INDEX.search(L[s[0]][2][:250]):
            return None                                # nothing says this leaf is that issue's index
        return e + 0.5
    n, m = len(segs), len(quarter)
    dp = [[(0.0, None)] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0 and j == 0:
                continue
            best = (-1e9, None)
            if i > 0:
                best = max(best, (dp[i - 1][j][0] - 0.5, "skip leaf"))
            if j > 0:
                best = max(best, (dp[i][j - 1][0], "skip issue"))
            if i > 0 and j > 0:
                sc = score(segs[i - 1], quarter[j - 1])
                if sc is not None:
                    best = max(best, (dp[i - 1][j - 1][0] + sc, "match"))
            dp[i][j] = best
    out, i, j = [], n, m
    while i > 0 or j > 0:
        how = dp[i][j][1]
        if how == "match":
            out.append((segs[i - 1], quarter[j - 1]))
            i, j = i - 1, j - 1
        elif how == "skip leaf":
            i -= 1
        else:
            j -= 1
    return out[::-1]


def year(y, cache, since=None, until=None):
    """One year's rows: the issues dated in it (from since), and to until those of the next sixty days whose releases
    fall before it."""
    allrows = yaml.safe_load(open(ix.ISSUES, encoding="utf-8"))["issues"]
    lo_d = since or datetime.date(y, 1, 1)
    hi_d = (until + datetime.timedelta(days=60)) if until else datetime.date(y, 12, 31)
    issues = [r for r in allrows if lo_d.isoformat() <= r["date"] <= hi_d.isoformat()]
    want = {r["date"] for r in issues}
    items = json.load(open(ix.PAGES, encoding="utf-8"))["items"]
    pages, found, log = {}, {}, []
    for iid, it in sorted(items.items(), key=lambda kv: kv[1]["from"]):
        if it.get("unread") or not any(it["from"] <= d <= it["to"] for d in want):
            continue
        L = leaves(cache, iid)
        for k, p, t in L:
            if p is not None:
                pages.setdefault((it["vol"], p), t)
        lo, hi = 1, 1300                               # any page of a volume: a copy's numbering can run out of order
        f_, t_ = (datetime.date.fromisoformat(it[k]) for k in ("from", "to"))
        quarter = [r for r in allrows if (f_ - datetime.timedelta(days=14)).isoformat() <= r["date"]
                   <= (t_ + datetime.timedelta(days=14)).isoformat()]     # a copy may bind a week of the next
        segs, prev = [], None
        R = (lambda iid_, L_: lambda i, a, b: readings(cache, iid_, L_, i, a, b))(iid, L)
        for i in index_leaves(L, lo, hi, R):             # the issue's pages: the numbered leaves since the last index
            top = it["main"][0] + 200 if not segs else hi       # not the volume's index bound before the first issue
            seq = [L[j][1] for j in range((prev + 1) if prev is not None else 0, i + 1)
                   if L[j][1] is not None and it["main"][0] - 80 <= L[j][1] <= top]
            r_ = run(seq)
            sf, sl = (r_[0], r_[-1]) if r_ else (None, None)
            if sf is not None and (not segs or segs[-1][2] is None) and it["from"][5:7] in ("01", "07") and sf <= 20:
                sf = 1                                 # a volume's first issue: its covers carry no number
            elif sf is not None and segs and segs[-1][2] is not None and 0 < sf - segs[-1][2] <= 20:
                sf = segs[-1][2] + 1                   # pages the numbering missed: after the last issue's
            segs.append((i, sf, sl))
            prev = i
        placed = place(L, segs, quarter, lo, hi, R)
        done = {x[0] for x, _ in placed}
        twins = {}                                     # an index scanned twice: the leaf beside a placed one, its pages
        for s_ in segs:
            if s_[0] in done:
                continue
            near = [(x, q) for x, q in placed if abs(x[0] - s_[0]) <= 3
                    and abs(median(R, x[0], lo, hi) - median(R, s_[0], lo, hi)) <= 40]
            if near:
                twins.setdefault(near[0][0][0], []).append(s_[0])
            else:
                log.append(f"{iid} leaf {s_[0]}: an index not placed")
        for (i, sf, sl), r in placed:
            ls = [i] + twins.get(i, [])
            j = i + 1                                   # an index run on to the next leaf (not the back cover, a cover)
            if j < len(L) and not BACK.search(L[j][2][:600]) and not HEAD_INDEX.search(L[j][2][:250]) \
                    and not ix.MAST.search(L[j][2][:700]) and len(R(j, lo, hi)) > 8:
                ls.append(j)
            own = it["from"] <= r["date"] <= it["to"]
            if r["date"] not in want or r["date"] in found and (found[r["date"]]["own"] or not own):
                continue                               # an issue in two copies (or bound twice): its own quarter's, the first
            found[r["date"]] = {"iid": iid, "vol": it["vol"], "sf": sf, "sl": sl, "leaves": ls, "L": L, "R": R,
                                "own": own}
    rows, stats = [], {"issues": len(issues), "indexed": 0, "items": 0, "release": 0, "no index": []}
    for r in issues:
        if r["date"] not in found:
            stats["no index"].append(r["date"])
            continue
        f = found[r["date"]]
        vol, sf, sl, ls, L = f["vol"], f["sf"], f["sl"], f["leaves"], f["L"]
        first, last = r.get("first"), r.get("last")
        if not first or not last or r.get("check"):    # the pages the leaves give (RULES 3)
            first, last = sf, sl
            log.append(f"{r['date']}: pages from the leaves, {sf}-{sl}")
        elif not first <= median(f["R"], ls[0], 1, 1300) <= last:
            log.append(f"{r['date']}: the index's pages are not the issue's {first}-{last}: the leaves', {sf}-{sl}")
            first, last = sf, sl
        elif sf and sl and (abs(sf - first) > 2 or abs(sl - last) > 4):
            log.append(f"{r['date']}: issues {first}-{last}, leaves {sf}-{sl}")
        if not first or not last:
            stats["no index"].append(r["date"])
            continue
        stats["indexed"] += 1
        issue = datetime.date.fromisoformat(r["date"])
        seen = {}                                   # page -> [[readings]], one list an item (RULES 5)
        for j in sorted(set(ls)):
            for title, page in f["R"](j, first, last):
                title = re.sub(r"^(?:\S+\s+){0,3}Vol\.?\s+\S+,?\s+No\.?\s*\S+\s+", "", title)    # the page's head
                title = clean(title)
                w = words(title)
                if not w or title.startswith("("):
                    continue
                have = seen.setdefault(page, [])
                same = next((k for k, xs in enumerate(have) if any(
                    len(w & words(x)) >= 0.5 * min(len(w), len(words(x))) for x in xs)), None)
                if same is None:
                    have.append([title])
                else:
                    have[same].append(title)
        votes = {}                                  # one title at two pages: the OCR misread one (RULES 5)
        for p, items_ in seen.items():
            for xs in items_:
                k = re.sub(r"\W+", " ", best(xs, first, last) or "").strip().lower()
                if k:
                    votes.setdefault(k, []).append((len(xs), p))
        keep = {k: max(v)[1] for k, v in votes.items()}
        heads = set()                               # a subject heading the index sets on a line of its own
        for j in set(ls):
            for ln in rebuilt(cache, f["iid"], L[j][0]).split("\n"):     # (the OCR's own text can set numbers apart)
                ln = re.sub(r"\W+", " ", ln).strip().lower()
                if ln and not re.search(r"\d", ln) and len(ln.split()) <= 5:
                    heads.add(ln)
        for k in [k for k in keep if k in heads and len(k.split()) <= 4]:
            keep[k] = None                          # a heading read as a title, its page another entry's
        seen = {p: [best(xs, first, last) for xs in items_] for p, items_ in seen.items()}
        seen = {p: [t for t in ts if t and keep.get(re.sub(r"\W+", " ", t).strip().lower(), p) == p]
                for p, ts in seen.items()}
        n = 0
        for page, title, one in [(p, t, len(ts) == 1) for p, ts in sorted(seen.items()) for t in ts]:
            d = release_date(pages.get((vol, page)), issue) if one else None
            n += 1
            day = d or issue
            if since and day < since or until and day > until or not until and issue.year > y:
                continue
            row = {"key": f"dsb:{r['date']}:{page}:{n}", "src": "dsb", "date": day.isoformat(),
                   "issue": r["date"], "page": page, "title": title, "dated": "release" if d else "issue"}
            u = printed.page_url(r["date"], page)
            if u:
                row["url"] = u
            rows.append(row)
            stats["release"] += bool(d)
            stats["items"] += 1
    capitals(rows)
    rows = run_ons(rows)
    stats.update(items=len(rows), release=sum(x["dated"] == "release" for x in rows))
    rows.sort(key=lambda x: (x["date"], x["issue"], x["page"]))
    os.makedirs(OUT, exist_ok=True)
    head = ("# Generated by tools/daybook/make_bulletin.py from archive.org's copies of the Department of State\n"
            "# Bulletin. Edit the script, not this file. One row an item of an issue's own index: key, src (dsb),\n"
            "# date (the day filed: its release where its page prints one, else the issue's), issue, page, title (as the\n"
            "# OCR reads the index), dated (release|issue), url (the copy's page).\n")
    open(os.path.join(OUT, f"{y}.yaml"), "w", encoding="utf-8").write(
        head + yaml.safe_dump({"year": int(y), "docs": rows}, sort_keys=False, allow_unicode=True, width=200))
    print(y, stats)
    for x in log:
        print("  ", x)


def main():
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else os.path.join(tempfile.gettempdir(), "dsb")
    years = [a for a in sys.argv[1:] if re.match(r"^\d{4}$", a)]
    for y in years:                                   # the calendar's span: from Jan. 6, 1960, to Jan. 20, 1969
        y = int(y)
        year(y, cache, since=FROM if y == FROM.year else None, until=TO if y == TO.year else None)


if __name__ == "__main__":
    main()
