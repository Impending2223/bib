"""Write daybook/committees/<YYYY-MM>.yaml: every committee meeting the bound Congressional Record's Daily Digest
reports, Jan. 6, 1960, to Jan. 20, 1969 (the calendar's span), and daybook/committees/volumes.yaml, the volumes read.

    python3 tools/daybook/make_committees.py [--cache DIR] [--year YYYY ...] [--keep-pdf]

Needs the network, pdftotext and about 250 MB of disk a volume (each PDF is fetched, read, and deleted unless
--keep-pdf); the build does not. The files are generated: edit this script, never them.

The source: the Daily Digest of the bound Record, one part a year on govinfo (VOLS): GPO-CRECB-<year>-pt<N>-1.pdf, a
scan with an OCR text layer. pdftotext -bbox gives each word with its box; the page is read as the printer set it
(layout): the two columns, left then right, between the lines that run across the page (the running head, the day's
heading, HIGHLIGHTS, "Senate", "House of Representatives", the rules between days).

STYLE (the rows; rendered by tools/bib/committees.py):
 1. A day: its heading ("Tuesday, January 21, 1964"), read with the OCR's misreadings allowed and resolved against the
    weekday and the day before; a heading that resolves to no later date is left as a misreading.
 2. A meeting: a paragraph of the day's "Committee Meetings" (the Senate's, the House's) or of its "Joint Committee
    Meetings", opened by its lead ("Committee on Foreign Relations:", "Joint Economic Committee:", "Conferees ...")
    under the Digest's subject heading in capitals ("METRIC SYSTEM"). Chamber: S, H or J (joint committees and
    conferees). Chamber action, the Resume of Congressional Activity, and the volume's tables are not meetings.
 3. Fields: key 'cmte:<date>-<n>', src 'cmte', date, ch, committee (the lead as printed, the OCR's stray marks
    taken out), code and name (COMMITTEES: the committee as the Congressional Directory names it, "Foreign
    Relations"; a lead no name fits keeps its printed form and a code made from it), sub (a subcommittee named in the
    paragraph's first sentence), heading (the Digest's subject heading, as printed), bills (the measures the
    paragraph names: S. 1278, H.R. 8363, S.J. Res. 189), exec (the paragraph says executive session), open (it says
    open session or open hearing), witnesses (each as printed, "Dr. Allen V. Astin, Director, National Bureau of
    Standards", split into title, name and office), next (the day hearings continue, where the paragraph gives one),
    text (the paragraph as printed: lines joined, a word broken at a line's end rejoined), page (the printed folio,
    "D3"), pdf (the page of the PDF), url (the PDF at that page).
 4. Witnesses: the persons named after the Digest's formulas ("heard testimony from", "Testimony was received
    from", "Witnesses heard were", "having as its witnesses", "a briefing from"), up to the sentence's end; one a
    semicolon, or a comma where the list is of names alone ("Senators Keating, Hart, and Kennedy"); names sharing an
    office ("John G. Palfrey and James T. Ramey, members of the Atomic Energy Commission") apart. Not persons:
    "public witnesses", "representatives of ...", "officials of ..." (kept in `others`, as printed).
 5. Folios: the running head's "D<n>"; where the OCR misreads it, the page's place among the pages whose folio reads
    (the offset of the nearest pages on either side). volumes.yaml gives each volume's runs of offset (PDF page to
    folio) and the pages whose folio was not read.
"""
import argparse
import datetime
import difflib
import glob
import gzip
import html
import os
import re
import subprocess
import sys
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "daybook", "committees")
FROM, TO = "1960-01-06", "1969-01-20"
# The Daily Digest's part of each year's bound Record (govinfo's MODS: "Daily Digest - Congressional Record (Bound
# Edition), Volume 110 (1964)": part 20).
VOLS = {1960: 16, 1961: 18, 1962: 19, 1963: 21, 1964: 20, 1965: 23, 1966: 23, 1967: 29, 1968: 26, 1969: 32}
URL = "https://www.govinfo.gov/content/pkg/GPO-CRECB-{y}-pt{p}/pdf/GPO-CRECB-{y}-pt{p}-1.pdf"
UA = {"User-Agent": "bib-daybook (https://impending2223.github.io/bib/)"}

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]

# The committees, as the Congressional Directory names them, 1960-69, by chamber. The code: the chamber and the name.
COMMITTEES = {
    "S": ["Aeronautical and Space Sciences", "Agriculture and Forestry", "Appropriations", "Armed Services",
          "Banking and Currency", "Commerce", "Interstate and Foreign Commerce", "District of Columbia", "Finance",
          "Foreign Relations", "Government Operations", "Interior and Insular Affairs", "Judiciary",
          "Labor and Public Welfare", "Post Office and Civil Service", "Public Works", "Rules and Administration",
          "Select Committee on Small Business", "Special Committee on Aging",
          "Select Committee on Standards and Conduct", "Special Committee on Unemployment Problems",
          "Select Committee on National Water Resources", "Select Committee on Improper Activities in the Labor or "
          "Management Field"],
    "H": ["Agriculture", "Appropriations", "Armed Services", "Banking and Currency", "District of Columbia",
          "Education and Labor", "Foreign Affairs", "Government Operations", "House Administration",
          "Interior and Insular Affairs", "Interstate and Foreign Commerce", "Judiciary",
          "Merchant Marine and Fisheries", "Post Office and Civil Service", "Public Works", "Rules",
          "Science and Astronautics", "Un-American Activities", "Internal Security", "Veterans' Affairs",
          "Ways and Means", "Standards of Official Conduct", "Select Committee on Small Business",
          "Select Committee on Government Research", "Select Committee on Export Control",
          "Select Committee on Crime", "Select Committee on Astronautics and Space Exploration"],
    "J": ["Joint Committee on Atomic Energy", "Joint Economic Committee", "Joint Committee on Internal Revenue "
          "Taxation", "Joint Committee on Printing", "Joint Committee on the Library", "Joint Committee on Defense "
          "Production", "Joint Committee on Reduction of Nonessential Federal Expenditures", "Joint Committee on the "
          "Organization of the Congress", "Joint Committee on Congressional Operations", "Joint Committee on "
          "Immigration and Nationality Policy", "Joint Committee on Navajo-Hopi Indian Administration",
          "Joint Committee on Disposition of Executive Papers", "Joint Committee on Washington Metropolitan Problems",
          "Joint Committee on Inaugural Arrangements", "Conferees"],
}
CHAMBER = {"S": "Senate", "H": "House", "J": ""}


def slug(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", t.lower())).strip("-")


def nelson():
    """{(ch, name): code}: Garrison Nelson's codes of the standing committees, from congress/committees.yaml
    (tools/congress/make_committees.py), where that file is."""
    p = os.path.join(ROOT, "congress", "committees.yaml")
    if not os.path.exists(p):
        return {}
    d = yaml.safe_load(open(p, encoding="utf-8")) or {}
    return {(c["ch"].upper(), c["name"]): c["code"] for c in d.get("committees") or []}


NELSON = nelson()


def code_of(ch, name):
    """Nelson's code for a standing committee (102, House Agriculture); else the chamber and the name's words
    ('j.atomic-energy', 's.special-committee-on-aging')."""
    if (ch, name) in NELSON:
        return NELSON[(ch, name)]
    return f"{ch.lower()}.{slug(re.sub(r'^(?:Joint )?Committee on (?:the )?', '', name))}"


# ---------------------------------------------------------------- the volume

def fetch(year, cache, keep_pdf):
    """The volume's words with their boxes (pdftotext -bbox), cached; the PDF is deleted unless keep_pdf."""
    bbox = os.path.join(cache, f"{year}.bbox.html.gz")
    if os.path.exists(bbox):
        return bbox
    pdf = os.path.join(cache, f"{year}.pdf")
    if not os.path.exists(pdf):
        url = URL.format(y=year, p=VOLS[year])
        print(f"fetching {url}", file=sys.stderr)
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600) as r, \
                open(pdf + ".part", "wb") as f:
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                f.write(b)
        os.rename(pdf + ".part", pdf)
    with gzip.open(bbox + ".part", "wb") as f:      # kept compressed: a seventh of the size
        p = subprocess.run(["pdftotext", "-bbox", pdf, "-"], check=True, stdout=subprocess.PIPE)
        f.write(p.stdout)
    os.rename(bbox + ".part", bbox)
    if not keep_pdf:
        os.remove(pdf)
    return bbox


WORD = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>')
PAGE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)


def pages(path):
    s = gzip.open(path, "rt", encoding="utf-8").read() if path.endswith(".gz") else open(path, encoding="utf-8").read()
    for m in PAGE.finditer(s):
        W, H = float(m.group(1)), float(m.group(2))
        yield W, H, [(float(a), float(b), float(c), float(d), html.unescape(t))
                     for a, b, c, d, t in WORD.findall(m.group(3))]


def rows_of(ws, tol=4.0):
    """Words into lines: by the middle of their boxes, then left to right."""
    ws = sorted(ws, key=lambda w: (w[1] + w[3]) / 2)
    rows = []
    for w in ws:
        yc = (w[1] + w[3]) / 2
        if rows and abs(rows[-1][0] - yc) < tol:
            rows[-1][1].append(w)
            n = len(rows[-1][1])
            rows[-1][0] = (rows[-1][0] * (n - 1) + yc) / n
        else:
            rows.append([yc, [w]])
    return [(yc, sorted(r, key=lambda w: w[0])) for yc, r in rows]


def layout(W, H, ws):
    """The page's lines in reading order: [(kind, text)], kind L or R (a column) or S (a line across the page). The
    gutter: the widest run of the least ink near the middle. A word across it (three letters or more), or set large
    (a heading), makes its line one across the page."""
    lo, hi = int(W * .38), int(W * .62)
    cov = [0] * (int(W) + 2)
    for w in ws:
        for x in range(max(lo, int(w[0])), min(hi, int(w[2])) + 1):
            cov[x] += 1
    m = min(cov[lo:hi + 1])
    runs, cur = [], []
    for x in range(lo, hi + 1):
        if cov[x] <= m + 1:
            if cur and x != cur[-1] + 1:
                runs.append(cur)
                cur = []
            cur.append(x)
    if cur:
        runs.append(cur)
    run = max(runs, key=lambda r: (len(r), -abs((r[0] + r[-1]) / 2 - W / 2)))
    g = (run[0] + run[-1]) / 2
    L, R, S = [], [], []
    for w in ws:
        if (w[0] < g - 1 and w[2] > g + 1 and len(re.sub(r"\W", "", w[4])) >= 3) or w[3] - w[1] > 18 \
                or w[4].count("#") >= 5:          # the rule between days ('#####', the OCR's reading of it)
            S.append(w)
        elif (w[0] + w[2]) / 2 < g:
            L.append(w)
        else:
            R.append(w)
    have = set(map(id, S))
    for yc, r in rows_of([w for w in S if w[3] - w[1] <= 18]):
        for w in L + R:
            if id(w) not in have and abs((w[1] + w[3]) / 2 - yc) < 2.5:
                S.append(w)
                have.add(id(w))
    L = [w for w in L if id(w) not in have]
    R = [w for w in R if id(w) not in have]
    # a day's heading, set in one column, still divides the page: what is below it in either column is the new day's
    for col in (L, R):
        for yc, r in rows_of(col):
            if day_heading(" ".join(w[4] for w in r)):
                S += r
                have.update(map(id, r))
    L = [w for w in L if id(w) not in have]
    R = [w for w in R if id(w) not in have]
    out = []
    bounds = [(-1e9, None)] + rows_of(S) + [(1e9, None)]
    for i in range(len(bounds) - 1):
        a, b = bounds[i][0], bounds[i + 1][0]
        for k, col in (("L", L), ("R", R)):
            for yc, r in rows_of([w for w in col if a < (w[1] + w[3]) / 2 <= b]):
                out.append((k, " ".join(w[4] for w in r), yc))
        if bounds[i + 1][1]:
            out.append(("S", " ".join(w[4] for w in bounds[i + 1][1]), b))
    return out


FOLIO = re.compile(r"^D\s?([\dlIOoS]{1,3})$")


def folio_of(lines, H):
    """The running head's folio ('D9'), from the page's top lines."""
    for k, t, y in lines:
        if y > H * .09:
            break
        for tok in t.split():
            m = FOLIO.match(tok.strip(".,·"))
            if m:
                d = m.group(1).translate(str.maketrans("lIOoS", "11005"))
                if d.isdigit():
                    return int(d)
    return None


def folios(raw):
    """{pdf page: folio}: the page's own where it reads and agrees with its neighbours' offset; else the offset of the
    nearest pages that read (STYLE 5). Returns (folios, unread pages, runs)."""
    n = len(raw)
    off = {i: f - i for i, f in raw.items() if f is not None}
    good = {}
    for i, o in off.items():
        near = [off[j] for j in range(i - 6, i + 7) if j != i and j in off]
        if near and sum(1 for x in near if x == o) >= max(1, len(near) // 3):
            good[i] = o
    out, unread = {}, []
    for i in range(1, n + 1):
        if i in good:
            out[i] = i + good[i]
            continue
        unread.append(i)
        before = next((good[j] for j in range(i - 1, 0, -1) if j in good), None)
        after = next((good[j] for j in range(i + 1, n + 1) if j in good), None)
        o = before if before is not None else after
        out[i] = i + (o if o is not None else 0)
    runs = []
    for i in range(1, n + 1):
        o = out[i] - i
        if runs and runs[-1]["offset"] == o and runs[-1]["to"] == i - 1:
            runs[-1]["to"] = i
        else:
            runs.append({"from": i, "to": i, "offset": o})
    return out, unread, runs


# ---------------------------------------------------------------- the days

def fuzzy(tok, words, cut=.7):
    m = difflib.get_close_matches(re.sub(r"[^A-Za-z]", "", tok).capitalize(), words, 1, cut)
    return m[0] if m else None


DIGITS = str.maketrans("lIoOBgSZ¢", "110089526")


def day_heading(t):
    """(weekday, month, day) from a line that reads as a day's heading, else None."""
    t = t.strip(" .·•'\"_-,r")
    t = re.sub(r"(?<=[a-z])[,.](?=[a-z])", "", t)          # 'Februp,ry'
    t = re.sub(r"(?<=\w)[?!~](?=\w)", "", t)                # 'Jf?ednesday'
    if len(t) > 42 or len(t) < 12:
        return None
    toks = re.findall(r"[A-Za-z0-9~:_¢.']+", t)
    if not 3 <= len(toks) <= 6:
        return None
    wd = fuzzy(toks[0], WEEKDAYS, .75)
    if not wd:
        return None
    mo = fuzzy(toks[1], MONTHS, .6)
    if not mo:
        return None
    # the year, as the OCR reads it ('1964', "'1964", '19_64', '19g4', '1¢4'): four or five marks from 1 and 9
    tail = "".join(toks[3:]).replace("_", "").replace("'", "").replace(".", "")
    if not re.fullmatch(r"[1lI][9g][\dlIoOBgSZ¢]{1,3}", tail):
        return None
    d = re.sub(r"[.,~:]+$", "", toks[2]).translate(DIGITS)
    return (wd, MONTHS.index(mo) + 1, int(d) if d.isdigit() else None)


def resolve(h, prev, year):
    """The date a heading names: as read where the weekday agrees and it falls after the day before; else the date
    within three weeks after the day before with that weekday and month whose day reads most like the heading's."""
    wd, mo, d = h
    if d:
        try:
            x = datetime.date(year, mo, d)
            if x.weekday() == WEEKDAYS.index(wd) and (prev is None or x > prev):
                return x
        except ValueError:
            pass
    start = prev or datetime.date(year, 1, 1)
    cands = [start + datetime.timedelta(days=k) for k in range(1, 22)]
    cands = [x for x in cands if x.weekday() == WEEKDAYS.index(wd) and x.month == mo and x.year == year]
    if not cands:
        return None
    if d:
        cands.sort(key=lambda x: (-difflib.SequenceMatcher(None, str(x.day), str(d)).ratio(), x))
    return cands[0]


# ---------------------------------------------------------------- the meetings

def letters(t):
    return re.sub(r"[^a-z]", "", t.lower())


def section_mark(t):
    """'senate', 'house', 'joint', 'meetings', 'chamber', 'highlights', 'resume', or None."""
    l = letters(t)
    if not l or len(t) > 60:
        return None
    if l in ("senate", "enate", "senat") or (len(l) <= 8 and difflib.SequenceMatcher(None, l, "senate").ratio() > .8):
        return "senate"
    if re.search(r"ofrep|frepresent|representatives$", l) and len(l) < 30 and l.startswith(("h", "o", "m")) \
            or difflib.SequenceMatcher(None, l, "houseofrepresentatives").ratio() > .8:
        return "house"
    if re.match(r"[jfi/]?oint", l) and (difflib.SequenceMatcher(None, l, "jointcommitteemeetings").ratio() > .8
                                         or difflib.SequenceMatcher(None, l, "jointmeetings").ratio() > .8):
        return "joint"
    if difflib.SequenceMatcher(None, l, "committeemeetings").ratio() > .82:
        return "meetings"
    if difflib.SequenceMatcher(None, l, "chamberaction").ratio() > .8:
        return "chamber"
    if len(l) <= 12 and difflib.SequenceMatcher(None, l, "highlights").ratio() > .75:     # 'HIGHUGHTS'
        return "highlights"
    if l.startswith("resumeof") or l.startswith("rsumeof") or l.startswith("resumcof") \
            or re.match(r"(historyofbillsenacted|dispositionofexecutivenomination|index$|thisindexiskeyed)", l):
        return "resume"
    return None


def caps_heading(t):
    """The Digest's subject heading over a meeting: a short line in capitals."""
    s = t.strip(" .·•'\"_-,")
    ls = re.sub(r"[^A-Za-z]", "", s)
    if len(ls) < 3 or len(s) > 70:
        return False
    up = sum(1 for c in ls if c.isupper())
    return up / len(ls) > .85 and ":" not in s


LEAD = re.compile(r"^[\s·•.,'_~\-]*([^:]{4,100}?)\s*:\s*(.*)$")


def like(tok, word, cut=.7):
    return difflib.SequenceMatcher(None, letters(tok), word).ratio() >= cut


def lead_of(t):
    """(lead, rest) where a line opens a meeting: 'Committee on Rules:' (the OCR's 'Gommt'ttee', 'Committe~' too),
    'Joint Committee on Atomic Energy:', 'Select Committee on Small Business:', 'Joint Economic Committee:',
    'Conferees ...'; not 'Committee also approved the following bills:'."""
    if re.match(r"^\W*Conferees\b", t):
        return re.sub(r"^\W*", "", t).split(None, 1)[0].rstrip(",.:"), re.sub(r"^\W*Conferees[,:]?\s*", "", t)
    t = re.sub(r"^(\W*)(?:[/fIJ]\s?oint|J\s?o\S{0,2}n\S?t|J\s?o\S{1,3}t)\b", r"\1Joint", t)      # 'I oint', '/oint', 'Joif!t'
    junk = bool(re.match(r"^\s*[^\sA-Za-z·•.,'_~\-]", t))      # '[:omm#tee', '<;ommittee': the C misread
    t = re.sub(r"^[^A-Za-z/]+", "", t)
    m = LEAD.match(t)
    if not m:
        return None
    lead, toks = m.group(1), m.group(1).split()
    if not (toks[0][:1].isupper() or toks[0][:1] in "/f" or junk):     # 'mittee on Labor met in ex<:cutive'
        return None
    cmte = lambda x: like(x, "committee") or like(x, "committees") or like(x, "subcommittee", .8)
    toks = [x for x in toks if re.search(r"\w", x)]          # 'Committee . on Banking': the stray mark out
    if len(toks) >= 2 and cmte(toks[0]) and len(letters(toks[1])) <= 3 and (letters(toks[1]) or "0")[:1] in "oa0":
        return lead, m.group(2)
    if len(toks) >= 2 and any(like(toks[0], w, .75) for w in ("joint", "select", "special", "senate", "house")) \
            and any(cmte(x) for x in toks[1:3]):
        return lead, m.group(2)
    if len(toks) == 3 and like(toks[1], "economic") and cmte(toks[2]):
        return lead, m.group(2)
    return None


def clean(t):
    """The OCR's stray marks out: middle dots, bullets, a stray underscore; spaces before punctuation."""
    t = re.sub(r"[·•]", " ", t)
    t = re.sub(r"(?<=\w)_(?=\w)", "", t)
    t = re.sub(r"\s+_|_\s+", " ", t)
    t = re.sub(r"\(\s+", "(", t)
    t = re.sub(r"\s+([,;:.)])", r"\1", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def join_lines(lines):
    """A paragraph's lines joined; a word broken at a line's end ('Sen-' 'ators') rejoined."""
    out = ""
    for l in lines:
        l = l.strip()
        if not l:
            continue
        if out.endswith("-") and not out.endswith("--") and re.match(r"[a-z]", l):
            out = out[:-1] + l
        elif out:
            out += " " + l
        else:
            out = l
    return clean(out)


# a committee's name only within these dates (renamed, created): (from, to)
VALID = {("S", "Interstate and Foreign Commerce"): ("", "1961-02-01"), ("S", "Commerce"): ("1961-01-01", "9999"),
         ("H", "Un-American Activities"): ("", "1969-02-18"), ("H", "Internal Security"): ("1969-02-18", "9999"),
         ("H", "Standards of Official Conduct"): ("1967-04-13", "9999"),
         ("S", "Select Committee on Standards and Conduct"): ("1964-07-24", "9999")}


def committee_of(ch, lead, day="1965-01-01"):
    """(chamber, printed, code, name) for a meeting's lead ('Committee on Foreign Relations') on the day."""
    printed = clean(lead)
    t = re.sub(r"^(?:[/fI] ?oint|J ?oi\S*)\b", "Joint", printed)
    t = re.sub(r"\b(?:Com\S{0,4}ittee|C\S{0,2}mm\S{0,4}ee)\b", "Committee", t)
    t = re.sub(r"\s+", " ", t).strip(" .,'")
    if re.match(r"(?i)joint\b", t) or re.match(r"(?i)conferees", t):
        ch = "J"
    if re.match(r"(?i)conferees", t):
        return ch, printed, "j.conferees", "Conferees"
    def best_of(c):
        best, score = None, 0
        for n in COMMITTEES[c]:
            a_, b_ = VALID.get((c, n), ("", "9999"))
            if not a_ <= day < b_:
                continue
            forms = [n] if n.startswith(("Select", "Special", "Joint", "Conferees")) else [
                f"Committee on {n}", f"Committee on the {n}"]
            for f in forms:
                r = difflib.SequenceMatcher(None, letters(t), letters(f)).ratio()
                if r > score:
                    best, score = n, r
        return best, score
    best, score = best_of(ch)
    if score < .85 and ch != "J":             # a committee of the other chamber: its section's heading misread
        other = "H" if ch == "S" else "S"
        b2, s2 = best_of(other)
        if s2 >= .9:
            ch, best, score = other, b2, s2
    if best and score >= .85:
        return ch, printed, code_of(ch, best), best
    return ch, printed, code_of(ch, t), t


SUB = re.compile(r"\b((?:(?:Special |Select |Ad Hoc |General |Legislative |Consultative |Joint |[A-Z][\w'.-]+ )(?:and )?)*"
                 r"Subcommittee(?: No\. ?\d+| [A-Z]| on (?:the )?[A-Z][\w,'.-]*(?: (?:and|of|on|the|for|to|in|"
                 r"[A-Z][\w,'.-]*))*)?)")


# the OCR's misreadings of the Digest's figures in a bill's number: '¢' and '<fi' for 96, '<)' and '<j' for 9,
# 'o' for 0, 'l', 'I', 'i' and '!' for 1, 'g' for 9 ('H.R. ¢37' is H.R. 9637; '6o6i' 6061)
FIG = [("¢", "96"), ("<fi", "96"), ("<)", "9"), ("<j", "9"), ("<}", "6")]
FIGS = r"(?:\d|¢|<fi|<\)|<j|<\}|[oOlIi!g](?=[\d¢oOlIi!g<]))[\d¢oOlIi!g<fij)}]*"
BILL = re.compile(r"\b(H\.\s?R\.|S\.|H\.\s?J\.\s?Res\.|S\.\s?J\.\s?Res\.|H\.\s?Con\.\s?Res\.|S\.\s?Con\.\s?Res\.|"
                  r"H\.\s?Res\.|S\.\s?Res\.)\s?(" + FIGS + r"(?:(?:,\s*|,?\s+and\s+|\s+or\s+)" + FIGS + r")*)")


def figures(t):
    for a, b in FIG:
        t = t.replace(a, b)
    return t.translate(str.maketrans("oOlIi!g", "0011119"))


def bills_of(text):
    """The measures the paragraph names, their numbers read through the OCR's misreadings (FIG); 'H.R. 8305 and
    8405' two."""
    out = []
    for m in BILL.finditer(text):
        kind = re.sub(r"\s+", "", m.group(1))
        kind = {"H.R.": "H.R.", "S.": "S.", "H.J.Res.": "H.J. Res.", "S.J.Res.": "S.J. Res.",
                "H.Con.Res.": "H. Con. Res.", "S.Con.Res.": "S. Con. Res.", "H.Res.": "H. Res.",
                "S.Res.": "S. Res."}[kind]
        for n in re.split(r",\s*|,?\s+and\s+|\s+or\s+", m.group(2)):
            n = figures(n)
            if n.isdigit() and 0 < int(n) < 30000:
                x = f"{kind} {int(n)}"
                if x not in out:
                    out.append(x)
    return out


TRIGGER = re.compile(
    r"(?:(?:heard|received|receive|hear|took|taking|with)\s+(?:further\s+|additional\s+)?testimony|testimony)"
    r"(?:\s+(?:was|were))?(?:\s+(?:also|further))?(?:\s+(?:received|heard|given|presented|taken))?"
    r"(?:[\s,]+(?:by|from)|[\s,]+(?:on|in|of|concerning|regarding)\b[^;:]{0,110}?[\s,]+from)\s*[.:]?\s+"
    r"|witnesses?\s+(?:heard\s+)?(?:today\s+)?(?:in\s+this\s+regard\s+)?(?:on\s+[^.;:]{0,40}?\s+)?"
    r"(?:were|was|included|being)\s*:?\s+"
    r"|ha\s?(?:ving|d|s)\s+as\s+(?:its|their)\s+witness(?:es)?\s+"
    r"|(?:a\s+)?briefing\s+(?:(?:on|regarding|concerning)\b[^;:]{0,80}?\s+)?(?:from|by|with)\s+|briefed\s+by\s+|(?:heard|received)\s+(?:a\s+)?(?:report|statement|"
    r"discussion)s?\s+(?:from|by)\s+"
    r"|statements?\s+(?:was|were)\s+(?:presented|submitted|received|made)\s+(?:for\s+the\s+record\s+)?(?:by|from)\s+",
    re.I)
ABBR = re.compile(r"(?:\b[A-Z]|\bDr|\bMr|\bMrs|\bMs|\bJr|\bSr|\bCo|\bInc|\bCorp|\bLtd|\bBros|\bSt|\bGen|\bLt|\bCol|"
                  r"\bAdm|\bMaj|\bCapt|\bSgt|\bRev|\bNo|\bMessrs|\bGov|\bRep|\bSen|\bVt|\bMd|\bVa|\bPa|\bMass|"
                  r"\bConn|\bCalif|\bFla|\bGa|\bIll|\bInd|\bKans|\bKy|\bLa|\bMich|\bMinn|\bMiss|\bMo|\bMont|\bNebr|"
                  r"\bNev|\bOkla|\bOreg|\bTenn|\bTex|\bWash|\bWis|\bWyo|\bAla|\bAriz|\bArk|\bColo|\bDel|\bIowa|\bN|"
                  r"\bU|\bS|\bD|\bC|\bH|\bR|\bW|\bE|\bvs|\betc|\bAssn|\bAssoc|\bDept|\bDiv|\bInst|\bUniv|\bNatl|"
                  r"\bAve|\bMt|\bFt|\bPt|\bvol|\bpp|\bLtd)\.$")
NOT_PERSON = re.compile(r"^(?:the\s+)?(?:various\s+|several\s+|numerous\s+|other\s+|additional\s+|following\s+)*"
                        r"(?:public|departmental|department|agency|administration|government|industry|private|"
                        r"Government|Department|other|several|various|representatives?\s+(?:of|from)|officials?|spokesmen|"
                        r"members|witnesses|a\s+panel|panel|staff|officers?|individuals|persons|interested|"
                        r"\d+\s+\w+|two|three|four|five|six|seven|eight|nine|ten)\b", re.I)
TITLE_FIRST = re.compile(
    r"^((?:former\s+|Acting\s+|Deputy\s+|Under\s+|Assistant\s+|Associate\s+|Vice\s+)*(?:Senators?|Representatives?|"
    r"Congressman|Congressmen|Secretary(?:\s+of\s+(?:the\s+)?[A-Z][\w,]*(?:\s+(?:and|of|the|[A-Z]\w*))*?)?|"
    r"Attorney\s+General|Postmaster\s+General|Comptroller\s+General|Solicitor\s+General|Surgeon\s+General|"
    r"Ambassador(?:\s+to\s+[A-Z]\w+(?:\s+[A-Z]\w+)?)?|Governor(?:\s+of\s+[A-Z]\w+(?:\s+[A-Z]\w+)?)?|Mayor|"
    r"Gov\.|Gen\.|General|Lt\.\s+Gen\.|Maj\.\s+Gen\.|Brig\.\s+Gen\.|Adm\.|Admiral|Vice\s+Adm\.|Rear\s+Adm\.|"
    r"Commissioner|Chairman|Director|Administrator|Judge|Justice|Chief\s+Justice|Delegate|Resident\s+Commissioner|"
    r"Ambassador-at-Large|Speaker|Vice\s+President))\s+(.+)$")
HONOR = re.compile(r"^((?:Dr|Mr|Mrs|Miss|Ms|Rev|Hon|Msgr|Father|Sister|Rabbi|Bishop|Col|Capt|Maj|Lt|Gen|Adm|Sgt|"
                   r"Cmdr|Comdr)\.?(?:\s+(?:Gen|Col|Adm)\.)?)\s+(.+)$")


def sentence_end(t, i):
    """The end of the sentence that runs from i: a period not after an initial or abbreviation, followed by a
    capital or the end."""
    depth = 0
    for j in range(i, len(t)):
        c = t[j]
        if c == "(":
            depth += 1
        elif c == ")":
            depth = max(0, depth - 1)
        elif c == "." and depth == 0:
            before = t[max(i, j - 12):j + 1]
            starter = re.match(r"\s+(?:Hearings?|Committee|Subcommittee|Testimony|Heard|Also|Prior|It|Witnesses|"
                               r"Statements?|Adjourned|Recessed|Further|Senate|House|Conferees|The\s+(?:committee|"
                               r"subcommittee|hearing))\b", t[j + 1:j + 30])
            last = before.split()[-1] if before.split() else ""
            if (ABBR.search(last) or re.search(r"[A-Z]\.$", last)) and not (
                    starter and not re.search(r"\b[A-Z]\.$", before)):
                continue
            nxt = t[j + 1:j + 3]
            if not nxt.strip() or re.match(r"\s+[A-Z(\"']", nxt + " "):
                return j
    return len(t)


def split_top(t, sep):
    out, depth, cur = [], 0, ""
    for c in t:
        if c == "(":
            depth += 1
        elif c == ")":
            depth = max(0, depth - 1)
        if c == sep and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += c
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


NAME = re.compile(r"^(?:[A-Z][\w'’.-]*\.?\s+){0,4}(?:(?:de|De|van|Van|von|Von|du|Du|La|Le|Mac|Mc|O')\s?)?"
                  r"[A-Z][\w'’-]+(?:,?\s+(?:Jr\.|Sr\.|II|III|IV))?$")


OFFICE_END = re.compile(r",?\s+(?:on|regarding|concerning|relative\s+to|in\s+support\s+of|in\s+opposition\s+to|"
                        r"with\s+respect\s+to|in\s+connection\s+with|in\s+behalf\s+of|on\s+behalf\s+of|respecting)"
                        r"\s+(?:the\s+|H\.|S\.|a\s+|an\s+|proposed\s+|pending\s+|his\s+|their\s+|its\s+|this\s+|"
                        r"legislation|bills?\b)|,?\s+(?:who\s+was\s+|were\s+|was\s+)?accompanied\s+by\b|"
                        r"\.\s+(?:Hearings?|Committee|Subcommittee)\b")


def name_office(rest):
    """('John Smith, Jr.', 'president, ...') from 'John Smith, Jr., president, ...'; the office cut where the
    sentence goes on to the subject ('..., NASA, on H.R. 9641') or to those who came with him."""
    nm, _, office = rest.partition(", ")
    m = re.match(r"^(.+?)\s*\(([^)]+)\)$", nm)           # 'Clifford Hope (former Representative)'
    if m and not office:
        nm, office = m.group(1), m.group(2)
    if re.match(r"^(?:Jr\.?|Sr\.?|II|III|IV)(?:,|$)", office):
        suf, _, office = office.partition(", ")
        suf = suf.rstrip(",")
        nm = f"{nm}, {suf + '.' if suf in ('Jr', 'Sr') else suf}"
    m = OFFICE_END.search(office)
    if m:
        office = office[:m.start()]
    return nm.strip(), office.strip(" ,.")


def person_item(item):
    """{'as', 'title', 'name', 'office'} for one witness as printed; None where it names no person."""
    item = re.sub(r"^(?:and|also|as\s+well\s+as)\s+", "", item.strip(" ,.:-·'"), flags=re.I).strip(" -·'")
    # the sentence going on to its subject: 'George W. Ball in connection with recent rioting in Panama'
    item = re.split(r",?\s+(?:in\s+connection\s+with|regarding|concerning|relative\s+to|with\s+respect\s+to|"
                    r"in\s+support\s+of|in\s+opposition\s+to|with\s+regard\s+to)\s", item, maxsplit=1)[0]
    if not item or NOT_PERSON.match(item):
        return None
    x = {"as": item}
    m = TITLE_FIRST.match(item)
    if m and not re.match(r"^(?:Director|Chairman|Commissioner|Administrator|Judge|Justice|General|Mayor)\s+of\b",
                          item):
        head, rest = m.group(1), m.group(2)
        nm, office = name_office(rest)
        member = re.match(r"^(?:Senator|Representative|Congressman|Delegate)$", head)
        if (NAME.match(nm) or member and re.match(r"^[A-Z][\w'’.-]+(?: [A-Z][\w'’.-]+)*"
                                                   r" of [A-Z][\w.]+(?: [A-Z][\w.]+)?$", nm)) and len(nm.split()) <= 5:
            x["title"] = re.sub(r"\s+", " ", head)
            x["name"] = nm
            if office:
                x["office"] = office
            return x
    m = HONOR.match(item)
    if m:
        x["title"] = m.group(1)
        item = m.group(2)
    nm, office = name_office(item)
    if not NAME.match(nm) or len(re.sub(r",.*", "", nm).split()) < 2 and "title" not in x:
        return None
    # a name with neither office nor title is a person only with an initial ('John W. Smith'): not 'Puerto Rico'
    if not office and "title" not in x and not re.search(r"\b[A-Z]\.\s", nm):
        return None
    x["name"] = nm
    if office:
        x["office"] = office
    return x


PAIR = re.compile(r",\s+and\s+(?=(?:(?:Dr|Mr|Mrs|Miss|Gen|Adm|Col|Capt|Lt\.\s+Gen|Maj\.\s+Gen|Rear\s+Adm|Vice\s+Adm)\.?\s+)?"
                  r"(?:[A-Z][\w'’.-]*\.?\s+){1,3}[A-Z][\w'’-]+(?:,\s+Jr\.)?,\s)")


NAMEI = re.compile(r"^(?:and\s+)?(?:(?:Dr|Mr|Mrs|Miss|Gen|Adm|Col|Capt|Judge)\.?\s+)?(?:[A-Z][a-z]+\s+)?(?:[A-Z]\.\s*)+"
                   r"(?:[A-Z][a-z]+\s+)?(?:Mc|Mac|O')?[A-Z][a-z][\w'’-]+$")
NOT_NAMEI = re.compile(r"\b(?:U\.\s?S|D\.\s?C|Department|Bureau|Agency|Association|Inc|Co|Corp|University|Commission|"
                       r"Council|Office|Service|Board|Institute|Company|League|Union|Federation|Division|Guard|Army|Navy|"
                       r"Force|Corps)\b")


def comma_people(part):
    """'A. L. Mills, Jr., J. L. Robertson, and Charles N. Shepardson, all members of ...': a list of persons parted by
    commas alone; a new person where a part is a name with an initial ('J. L. Robertson'), the part before not."""
    chunks = [c for c in re.split(r",\s+", part)]
    out, cur = [], []
    for c in chunks:
        if cur and NAMEI.match(c.strip()) and not NOT_NAMEI.search(c):
            out.append(", ".join(cur))
            cur = []
        cur.append(c)
    if cur:
        out.append(", ".join(cur))
    return [re.sub(r",\s+and\s+(?:other|various|several)\b.*$", "", x) for x in out]


def witnesses_of(text):
    """(witnesses, others): the persons the paragraph's formulas name (STYLE 4), and what they name that is not a
    person, as printed."""
    ws, others = [], []
    # the OCR's 'Testinion y', 'testimoq.y' before 'was', 'from', 'by': read as the word
    text = re.sub(r"\b([Ww])itness\s?e\s?s\b", r"\1itnesses", text)
    text = re.sub(r"(?<=[,;.\s])~|~(?=[,;\s])", "", text)            # 'Brumberg,~ U.S.'
    text = re.sub(r"(?<=[A-Za-z])\.(?=[a-z])", "", text)          # 'R.epresentatives'
    text = re.sub(r"\bRe\S{3,7}tative(s?)\b", r"Representative\1", text)     # 'Represe~tatives'
    text = re.sub(r"\bSe\S{1,4}tor(s?)\b", r"Senator\1", text)
    text = re.sub(r"\b(Senators?|Representatives?)[.,]\s", r"\1 ", text)       # 'Representative. FindJey'
    text = re.sub(r"\b([Tt])est[\w.;~']{2,5}(?: ?[\w.]{1,2})?(?=\s+(?:was|were|from|by|also|on)\b)", r"\1estimony", text)
    for m in TRIGGER.finditer(text):
        j = sentence_end(text, m.end())
        span = text[m.end():j].strip()
        span = re.sub(r"^(?:the\s+following(?:\s+[^:;.]{0,40}?)?\s*:)\s*|^the\s+following\s+witnesses\s+", "", span,
                      flags=re.I)
        span = re.split(r"\s+(?:on|in\s+connection\s+with|regarding|concerning|relative\s+to|in\s+support\s+of|"
                        r"in\s+opposition\s+to|with\s+regard\s+to)\s+(?:the|S\.|H\.\s?R\.|H\.|pending|proposed)\b",
                        span, maxsplit=1)[0] if ";" not in span and "," not in span[:40] else span
        parts = []
        for part in split_top(span, ";"):           # 'X, office, and Gen. Y, office': two
            for p in PAIR.split(part):
                if p.strip():
                    parts += comma_people(p)
        for part in parts:
            part = part.strip()
            # 'Senators Keating, Hart, and Kennedy': names alone after a plural title
            m2 = re.match(r"^(?:and\s+)?(Senators|Representatives|Congressmen|Messrs\.)\s+(.+)$", part)
            if m2:
                one = {"Senators": "Senator", "Representatives": "Representative", "Congressmen": "Congressman",
                       "Messrs.": "Mr."}[m2.group(1)]
                names = [n.strip() for n in re.split(r",\s*(?:and\s+)?|\s+and\s+", m2.group(2)) if n.strip()]
                # 'Andrews of North Dakota': the State stays with the name
                for n in names:
                    if re.match(r"^[A-Z][\w'’.-]+(?: [A-Z]\.)?(?: of [A-Z][\w.]+(?: [A-Z][\w.]+)?)?$", n) or \
                            re.match(r"^[A-Z][\w'’.-]+(?: [A-Z][\w.']+){0,3}$", n):
                        ws.append({"as": f"{one} {n}", "title": one, "name": n})
                continue
            # 'John G. Palfrey and James T. Ramey, members of the Atomic Energy Commission'
            nm, _, office = part.partition(", ")
            m3 = re.match(r"^(?:and\s+)?(.+?)\s+and\s+(.+)$", nm)
            two = m3 and all(NAME.match(g.strip()) and len(g.split()) >= 2 for g in (m3.group(1), m3.group(2)))
            if m3 and office and two:
                for n in (m3.group(1), m3.group(2)):
                    x = person_item(f"{n.strip()}, {office}")
                    if x:
                        x["as"] = part
                        ws.append(x)
                continue
            x = person_item(part)
            if x:
                ws.append(x)
            else:
                p = re.sub(r"^(?:and|also)\s+", "", part, flags=re.I).strip(" .")
                if p:
                    others.append(p)
    # 'heard Senator Mansfield testify in behalf of Mr. Corry'
    for m in re.finditer(r"\bheard\s+((?:Senators?|Representatives?)\s+[A-Z][^.;:]{1,60}?)\s+testify\b", text):
        ws += witnesses_of("heard testimony from " + m.group(1) + ".")[0]
    seen, out = set(), []
    for w in ws:
        k = (w.get("title"), w["name"])
        if k not in seen:
            seen.add(k)
            out.append(w)
    return out, list(dict.fromkeys(others))


CONT = re.compile(r"(?:Hearings?|Committee|Subcommittee|It)\s+(?:will\s+)?(?:continues?|resumes?|meets?\s+again|"
                  r"are\s+(?:tentatively\s+)?scheduled\s+to\s+(?:continue|resume))\b([^.]{0,80})", re.I)


def next_of(text, day):
    """The day hearings continue, where the paragraph gives it: 'tomorrow', 'on Tuesday, January 21', 'Monday'."""
    for m in CONT.finditer(text):
        t = m.group(1)
        if re.search(r"\btomorrow\b", t, re.I):
            return day + datetime.timedelta(days=1)
        m2 = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|"
                       r"December)\s+(\d{1,2})", t)
        if m2:
            mo, d = MONTHS.index(m2.group(1)) + 1, int(m2.group(2))
            y = day.year + (1 if mo < day.month else 0)
            try:
                x = datetime.date(y, mo, d)
            except ValueError:
                return None
            return x if x > day else None
        m2 = re.search(r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b", t)
        if m2:
            k = (WEEKDAYS.index(m2.group(1)) - day.weekday()) % 7 or 7
            return day + datetime.timedelta(days=k)
    return None


def session_of(text):
    ex = bool(re.search(r"\bexecutive\s+(?:session|hearing|meeting)|\bin\s+executive\b", text, re.I))
    op = bool(re.search(r"\bopen\s+(?:session|hearing|meeting)|\bin\s+open\b", text, re.I))
    return ex, op


def sub_of(text):
    """The subcommittee the paragraph opens with ('Subcommittee on Wheat held ...', 'The CIA Subcommittee met ...');
    not one it names later ('... authorizing the Housing Subcommittee to ...')."""
    first = text[:sentence_end(text, 0) + 1]
    m = SUB.search(first)
    if not m or m.start() > 4:
        return None
    s = m.group(1).strip(" ,.")
    s = re.sub(r"\s+(?:held|met|began|continued|resumed|heard|in|to|and)$", "", s)
    s = re.sub(r",.*$", "", s)
    return s if s != "Subcommittee" else None


# ---------------------------------------------------------------- one volume

def read_volume(year, bbox):
    """(rows, volume record) for one year's Digest."""
    pl, raw = [], {}
    for i, (W, H, ws) in enumerate(pages(bbox), 1):
        lines = layout(W, H, ws)
        raw[i] = folio_of(lines, H)
        # the running head is not text
        lines = [(k, t) for k, t, y in lines if not (y < H * .09 and re.search(r"CONGR|RECORD|DIGEST|^D\s?\S{1,3}$", t))]
        pl.append(lines)
    fol, unread, runs = folios(raw)
    url = URL.format(y=year, p=VOLS[year])
    rows, day, chamber, mode, prev = [], None, None, None, None
    cur = None                                  # the meeting being read: dict with lines
    heading, last_heading, blocked, met = None, False, False, set()

    def close():
        nonlocal cur
        if cur:
            rows.append(cur)
        cur = None

    seq = [(pi, k, t) for pi, lines in enumerate(pl, 1) for k, t in lines]
    for n, (pi, k, t) in enumerate(seq):
        if True:
            h = day_heading(t)
            # a day's heading opens the day's record: HIGHLIGHTS, a chamber, its action or its meetings follow
            # ('Hearings continue on / Monday, January 13, 1964.' is a sentence's end)
            if h and not any(section_mark(t2) or day_heading(t2) for _, _, t2 in seq[n + 1:n + 6]):
                h = None
            if h:
                x = resolve(h, prev, year)
                if x:
                    close()
                    day, prev, chamber, mode, heading, blocked = x, x, None, None, None, False
                    met = set()
                    continue
            if day is None:
                continue
            s = section_mark(t)
            if s in ("senate", "house") and k != "S" or blocked and s != "resume":
                s = None
            if s:
                close()
                if s == "senate":
                    chamber, mode = "S", None
                elif s == "house":
                    chamber, mode = "H", None
                elif s == "joint":
                    chamber, mode = "J", "meetings"
                elif s == "meetings":
                    # the day's first meetings with no chamber's heading read: the Senate's, which come first
                    chamber = chamber or ("S" if not met else None)
                    mode = "meetings" if chamber else None
                    if chamber:
                        met.add(chamber)
                elif s == "chamber":
                    # a second 'Chamber Action' after the Senate's meetings: the House's heading was not read
                    if chamber == "S" and "S" in met:
                        chamber = "H"
                    mode = None
                elif s == "highlights":
                    mode = None
                elif s == "resume":           # the Resume, the tables, the index: nothing till the next day
                    mode, chamber, blocked = None, None, True
                heading = None
                continue
            if mode != "meetings":
                continue
            if re.match(r"^#+|^[#\s.,'·]+$", t.strip()):
                continue
            if caps_heading(t):
                c = clean(t).strip(" .,'")
                if cur is not None:
                    # capitals within a paragraph whose sentence runs on (a title quoted) stay in it
                    if cur["lines"] and not re.search(r"[.:;)\"'”]$", re.sub(r"[\s_·•~`,-]+$", "", cur["lines"][-1])):
                        cur["lines"].append(t)
                        continue
                    close()
                    heading = c
                else:
                    heading = f"{heading} {c}" if last_heading and heading else c
                last_heading = True
                continue
            was_heading, last_heading = last_heading, False
            if len(re.sub(r"[^A-Za-z0-9]", "", t)) < 3:     # a stray mark the OCR made a line of
                continue
            m = lead_of(t)
            if m and cur is not None and cur["lines"] and re.search(r"[a-z]-$", cur["lines"][-1].strip()):
                m = None                     # the line before broke a word: this one goes on with it
            if m and cur is not None and not was_heading and cur["lines"] and \
                    re.search(r"[;:,]$", re.sub(r"[\s_·•~`'-]+$", "", cur["lines"][-1])):
                m = None                     # a list within the paragraph ('Committee on Commerce: S. Res. 283-$360,000;')
            if m:
                close()
                ch, printed, code, name = committee_of(chamber, m[0], day.isoformat())
                cur = {"date": day, "ch": ch, "committee": printed, "code": code, "name": name,
                       "heading": heading, "lines": [m[1]], "pdf": pi, "_lead_done": True}
                heading = None
                continue
            if cur is not None:
                cur["lines"].append(t)
    close()
    out = []
    for r in rows:
        text = join_lines(r.pop("lines"))
        r.pop("_lead_done", None)
        if not text:
            continue
        r["text"] = text
        out.append(r)
    vol = {"year": year, "part": VOLS[year], "url": url, "pages": len(pl), "runs": runs, "unread": unread}
    return out, vol, fol


def finish(rows, fol, url):
    """The fields of STYLE 3, keys by day."""
    by_day = {}
    out = []
    for r in rows:
        d = r["date"]
        if not (FROM <= d.isoformat() <= TO):
            continue
        n = by_day[d] = by_day.get(d, 0) + 1
        text = r["text"]
        ws, others = witnesses_of(text)
        ex, op = session_of(text)
        x = {"key": f"cmte:{d.isoformat()}-{n}", "src": "cmte", "date": d.isoformat(), "ch": r["ch"],
             "committee": r["committee"], "code": r["code"], "name": r["name"]}
        sub = sub_of(text)
        if sub:
            x["sub"] = sub
        if r.get("heading"):
            x["heading"] = r["heading"]
        b = bills_of(text)
        if b:
            x["bills"] = b
        if ex:
            x["exec"] = True
        if op:
            x["open"] = True
        if ws:
            x["witnesses"] = ws
        if others:
            x["others"] = others
        nx = next_of(text, d)
        if nx:
            x["next"] = nx.isoformat()
        x["text"] = text
        x["page"] = f"D{fol[r['pdf']]}"
        x["pdf"] = r["pdf"]
        x["url"] = f"{url}#page={r['pdf']}"
        out.append(x)
    return out


def write(rows, vols):
    os.makedirs(OUT, exist_ok=True)
    head = ("# Generated by tools/daybook/make_committees.py from the bound Congressional Record's Daily Digest\n"
            "# (govinfo). Edit the script, not this file. One row a meeting: key, src, date, ch, committee, code,\n"
            "# name, sub, heading, bills, exec, open, witnesses, others, next, text, page, pdf, url.\n")
    by_month = {}
    for x in rows:
        by_month.setdefault(x["date"][:7], []).append(x)
    for mo, xs in sorted(by_month.items()):          # each file whole, or not at all: written aside, then moved in
        tmp = os.path.join(OUT, f".{mo}.yaml.part")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(head)
            yaml.safe_dump({"month": mo, "docs": xs}, f, allow_unicode=True, sort_keys=False, width=110)
        os.replace(tmp, os.path.join(OUT, f"{mo}.yaml"))
    for y in {mo[:4] for mo in by_month}:              # a month of a year read again that now has no meeting
        for f in glob.glob(os.path.join(OUT, f"{y}-[0-9][0-9].yaml")):
            if os.path.basename(f)[:7] not in by_month:
                os.remove(f)
    p = os.path.join(OUT, "volumes.yaml")
    old = (yaml.safe_load(open(p, encoding="utf-8")) or {}).get("volumes", []) if os.path.exists(p) else []
    keep = {v["year"]: v for v in old}
    keep.update({v["year"]: v for v in vols})
    with open(p + ".part", "w", encoding="utf-8") as f:
        f.write("# Generated by tools/daybook/make_committees.py: each Daily Digest volume read, its PDF, its pages,\n"
                "# the runs of PDF pages and their offset to the printed folio (folio = page + offset, 'D' before\n"
                "# it), and the pages whose folio the OCR did not give (placed by their neighbours).\n")
        yaml.safe_dump({"volumes": [keep[y] for y in sorted(keep)]}, f, sort_keys=False, width=110)
    os.replace(p + ".part", p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(os.environ.get("TMPDIR", "/tmp"), "digest"))
    ap.add_argument("--year", type=int, nargs="*")
    ap.add_argument("--keep-pdf", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.cache, exist_ok=True)
    years = a.year or sorted(VOLS)
    vols = []
    for y in years:
        bbox = fetch(y, a.cache, a.keep_pdf)
        rows, vol, fol = read_volume(y, bbox)
        rows = finish(rows, fol, vol["url"])
        vols.append(vol)
        months = sorted({x["date"][:7] for x in rows})
        write(rows, [vol])
        print(f"{y}: {len(rows)} meetings, {len({x['date'] for x in rows})} days, "
              f"{sum(len(x.get('witnesses', [])) for x in rows)} witnesses; folios unread {len(vol['unread'])}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
