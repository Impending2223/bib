"""The tiers of times of day that need a source read once (the brief, notes/briefs/times.md, "The tier builder"): each
reads its source from a cache directory (fetching it with --fetch where the cache lacks it) and writes a small JSON
file beside this script, tools/times/data/<tier>.json, which propose.py reads; propose.py needs no network.

    python3 -I tools/times/tiers.py digest   --cache DIR [--fetch]   the Daily Digest's chamber hours, 1960-69
    python3 -I tools/times/tiers.py unsc     --cache DIR [--fetch]   the Security Council's meetings, 1960-69
    python3 -I tools/times/tiers.py launches --cache DIR [--fetch]   NASA's launch times (KSC; the chronologies)
    python3 -I tools/times/tiers.py tests    --cache DIR [--fetch]   the United States' nuclear tests (DOE/NV-209)
    python3 -I tools/times/tiers.py all      --cache DIR [--fetch]

The sources and what each tier takes from them:

digest   The bound Record's Daily Digest, one part a year (VOLS in tools/daybook/make_committees.py), the scan's own
         text layer (`pdftotext`, no layout; kept gzipped in the cache as digest-<year>.txt.gz, the PDF deleted, some
         200 MB a year). A day: its heading ("Tuesday, January 7, 1964"), a line of its own, the weekday agreeing with
         the date read. A chamber: the last heading of the day, "Senate" or "House of Representatives". What it takes:
         the chamber's "Adjournment: Adjourned at 12:23 p.m." and "Recess: Recessed at 6:47 p.m." (the chamber action's
         last item), and "Senate met at 9 a.m." where the Digest says so (it names the hour of meeting only where it
         is not the standing one); the OCR's digits put right (I, l, r for 1; o, O for 0; s for 5), a time that will
         not read left out. An adjournment in the small hours (before 6 a.m.) is the next calendar day's. The page:
         the folio printed (D123) and the PDF's page, linked.
unsc     The Dag Hammarskjold Library's research guide, "Meetings conducted by the Security Council in <year>"
         (research.un.org: the record's symbol, the date, the topic, the outcome and the resolutions), and each
         meeting's verbatim record, S/PV.<n>, in English (documents.un.org, by symbol), on the days the calendar
         names the Council: its first page's "Held in New York, on Friday, 1 April 1960, at 3 p.m." (the hour
         called), the "called to order at 3.20 p.m." where it says so, and "The meeting rose at 5.30 p.m." The PDFs
         kept in the cache (unsc/S-PV.<n>.pdf). The Official Document System answers many requests with a
         "LOADING" page (a script's check, the site's own): not got round; the symbol listed under `missing` and
         asked again at the next --fetch. A record whose text layer gives no hour is kept without one.
launches The Kennedy Space Center's "Summary of Major NASA Launchings, 1 October 1958 - 30 September 1973" (KSC
         Historical Report; NTRS 19740015280): each launch's name, date and time as printed ("10:55 a.m. EST"); and
         the Library of Congress's chronologies for NASA, *Astronautics and Aeronautics*, 1963-68 (NASA SP-4004 to
         SP-4010; NTRS), where an item of the day gives an hour with its zone ("launched at 8:04 a.m. EST"). The
         chronologies of 1961 and 1962 (the House committee's prints) are not on NTRS.
tests    DOE/NV-209 (Rev. 16, 2015), *United States Nuclear Tests, July 1945 through September 1992* (OSTI 1351809),
         its table by date: each test's name, date and time (GMT), place, type and yield, by PDF page.

STYLE
1. A tier's file holds what the source prints, read by rule, with the page; nothing the source does not say. Which
   entry a row fits is propose.py's.
2. Rerunnable: the cache keeps what was fetched; --fetch only for what it lacks. The data files are rewritten whole.
"""
import argparse
import datetime
import glob
import gzip
import html
import json
import os
import re
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, ROOT)

UA = {"User-Agent": "bib-times (https://impending2223.github.io/bib/)"}
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
OCR_DIGITS = str.maketrans({"I": "1", "l": "1", "i": "1", "r": "1", "!": "1", "o": "0", "O": "0", "Q": "0",
                            "s": "5", "S": "5", "B": "8", "g": "9", "z": "2", "Z": "2", "¢": "9"})


def fetch(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=1800) as r, \
            open(path + ".part", "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
    os.rename(path + ".part", path)


def write(name, obj):
    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, name + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=0, sort_keys=True)
        f.write("\n")
    print(f"wrote {os.path.relpath(path, ROOT)}", file=sys.stderr)


def hhmm(h, m, ap):
    """'12', '23', 'p.m.' -> '12:23' (24-hour), or None where it will not read."""
    try:
        h, m = int(h), int(m or 0)
    except ValueError:
        return None
    if not (1 <= h <= 12 and 0 <= m <= 59):
        return None
    ap = ap.replace(" ", "").replace(".", "").lower()
    h = (h % 12) + (12 if ap.startswith("p") else 0)
    return f"{h:02d}:{m:02d}"


# ------------------------------------------------------------------------------------------------------- digest

class _Head:
    def __init__(self, *g):
        self._g = g

    def groups(self):
        return self._g


def day_heading(ln):
    """A day's heading as the OCR gives it ("Wednesday} February 22J 1961", "Monday, Feb-r uary 6, 1961:"):
    (weekday, month, day, year) as read, or None. The weekday and the month by their letters, near enough."""
    if ln is None or len(ln) > 40:
        return None
    tok = re.sub(r"[^A-Za-z0-9¢]", " ", ln).split()
    if len(tok) < 4:
        return None
    yy, dd = tok[-1], re.sub(r"(?<=.)[A-Za-z]$", "", tok[-2])
    rest = tok[:-2]
    if len(yy) == 2 and len(dd) == 2 and len(tok) >= 5:          # "19 64"
        yy, dd, rest = dd + yy, re.sub(r"(?<=.)[A-Za-z]$", "", tok[-3]), tok[:-3]
    if not re.fullmatch(r"[0-9IlOoBsSrn]{1,2}", dd) or not re.fullmatch(r"[0-9IlOoBsSg¢]{4}", yy):
        return None
    for k in (1, 2, 3):
        wd, mon = "".join(rest[:k]), "".join(rest[k:])
        if mon and any(near(letters(wd), w.lower(), 0.7) for w in WEEKDAYS) and month_of(mon):
            return _Head(wd, mon, dd, yy)
    return None
D_TIME = r"([0-9IlirosSOBgz]{1,2})\s?(?:[:.=~-]\s?([0-9IlirosSOBgz]{2}))?\s?[,.]?\s?(a\.?\s?m|p\.?\s?[mn1l]|noon|midnight)"
D_ACT = re.compile(r"(?:(Adj\S{0,3}?urn\S{0,5}|Recess\S{0,2})\s*:?[·.\s]*)?"
                   r"(?:(?:the\s+)?(Senate|House)\s+)?(?:then\s+|immediately\s+)?"
                   r"(Adjourned|adjourned|Recessed|recessed|met|convened|reconvened)\s+at\s+[·\s]?" + D_TIME)
FOLIO = re.compile(r"^\s*D\s?(\d{1,4})\s*$")


def letters(s):
    return re.sub(r"[^a-z]", "", s.lower())


def near(a, b, cut=0.8):
    import difflib
    return difflib.SequenceMatcher(None, a, b).ratio() >= cut


def month_of(tok):
    t = letters(tok)
    best = [m for m in MONTHS if near(t, m.lower(), 0.75)]
    return MONTHS.index(best[0]) + 1 if len(best) == 1 else None


def chamber_head(ln):
    t = letters(ln)
    if t == "senate":
        return "S"
    if 18 <= len(t) <= 25 and near(t, "houseofrepresentatives", 0.85):
        return "H"
    return None


def read_time(h, m, ap):
    ap_l = ap.lower()
    if ap_l == "noon":
        return "12:00"
    if ap_l == "midnight":
        return "24:00"
    return hhmm(h.translate(OCR_DIGITS), (m or "0").translate(OCR_DIGITS), "p.m." if ap_l.startswith("p") else "a.m.")


def digest_year(year, txt):
    """The days of one volume: [{date, ch, kind, local, folio, pdf, raw}]."""
    rows = []
    day, ch, folio, prev = None, None, None, None
    pages = txt.split("\f")
    for pno, page in enumerate(pages, 1):
        lines = page.split("\n")
        # the folio printed on this page (D3), wherever pdftotext put it
        f = [m.group(1) for m in (FOLIO.match(ln) for ln in lines) if m]
        folio = "D" + f[0] if f else None
        heads = []                                 # the page's running heads ("March 16"), for a day whose heading is lost
        for ln in lines:
            t = re.sub(r"[^A-Za-z0-9 ]", " ", ln).split()
            if len(t) in (2, 3) and len(ln) < 22 and month_of(t[0]) and re.fullmatch(r"[0-9IlOo]{1,2}", t[1]) \
                    and (len(t) == 2 or re.fullmatch(r"[0-9IlOog¢]{3,4}", t[2])):
                try:
                    heads.append(datetime.date(year, month_of(t[0]), int(t[1].translate(OCR_DIGITS))))
                except ValueError:
                    pass
        buf = []                                   # the page's lines since the last heading, joined for matching
        for i, ln in enumerate(lines + [None]):
            m = day_heading(ln)
            head = chamber_head(ln) if ln is not None and len(ln) < 40 else None
            # The Senate comes first in a day, the House after it: a line "Senate" in the House's columns, or a
            # line "House of Representatives" in the Senate's without the chamber's "Chamber Action" under it or
            # the Senate's adjournment before it, is text, not a heading.
            act = head and any(letters(x).startswith("chamberact") or near(letters(x), "chamberaction")
                               for x in lines[i + 1:i + 16])
            lost = False
            if head == "S" and ch is not None:
                # a Senate's "Chamber Action" after the House's: the next day, its heading lost (the OCR's); its
                # date the page's running head's, where that is later, else the day unknown until the next heading
                lost = bool(act and ch == "H")
                head = "S" if lost else None
            elif head == "H" and ch != "H":
                if not act and not any(r["day"] == day and r["ch"] == "S" and r["kind"] in ("adjourned", "recessed")
                                       for r in rows[-3:]) and "djourn" not in " ".join(buf) and "ecess" not in " ".join(buf):
                    head = None
            elif head == ch:
                head = None
            if ln is None or m or head:
                text = re.sub(r"\s+", " ", " ".join(buf))
                if day and ch:
                    for a in D_ACT.finditer(text):
                        kind = {"a": "adjourned", "r": "recessed", "m": "met", "c": "met"}[a.group(3)[0].lower()]
                        if a.group(3).lower() == "reconvened":
                            kind = "reconvened"
                        who = a.group(2)
                        if not a.group(1) and not who:
                            continue                # "adjourned at" in a committee's paragraph
                        c = {"Senate": "S", "House": "H"}.get(who, ch)
                        t = read_time(a.group(4), a.group(5), a.group(6))
                        if not t:
                            continue
                        d = day
                        nxt = False
                        if kind in ("adjourned", "recessed") and (t < "06:00" or t == "24:00"):
                            d = (datetime.date.fromisoformat(day) + datetime.timedelta(days=1)).isoformat()
                            nxt = True
                            if t == "24:00":
                                t = "00:00"
                        rows.append({"day": day, "date": d, "ch": c, "kind": kind, "local": t, "folio": folio,
                                     "pdf": pno, "raw": a.group(0).strip()[:80], **({"next_day": True} if nxt else {})})
                buf = []
            if ln is None:
                break
            if m:
                wd, mon, dd, yy = m.groups()
                mo = month_of(mon)
                if not mo or len(re.sub(r"\D", "", yy.translate(OCR_DIGITS))) < 3:
                    buf.append(ln)
                    continue
                try:
                    dt = datetime.date(year, mo, int(dd.translate(OCR_DIGITS)))
                except ValueError:
                    buf.append(ln)
                    continue
                if not near(letters(wd), WEEKDAYS[dt.weekday()].lower(), 0.7) or (prev and dt <= prev) or \
                        (re.fullmatch(r"\d{4}", yy) and yy != str(year)):
                    buf.append(ln)
                    continue
                day, ch, prev = dt.isoformat(), None, dt
                continue
            if head:
                ch = head
                if lost:
                    later = sorted(h for h in heads if prev and h > prev)
                    day = later[0].isoformat() if later else None
                    if later:
                        prev = later[0]
                continue
            buf.append(ln)
    # A chamber's day with two closing hours is a day whose heading the reader missed: both left out.
    n = {}
    for r in rows:
        if r["kind"] in ("adjourned", "recessed"):
            n[(r["day"], r["ch"])] = n.get((r["day"], r["ch"]), 0) + 1
    return [r for r in rows if n.get((r["day"], r["ch"]), 0) < 2 or r["kind"] not in ("adjourned", "recessed")]


def digest(cache, do_fetch):
    from tools.daybook.make_committees import VOLS, URL
    out, years = {}, {}
    for year in sorted(VOLS):
        gz = os.path.join(cache, "digest", f"digest-{year}.txt.gz")
        if not os.path.exists(gz):
            if not do_fetch:
                print(f"digest {year}: no text in the cache (--fetch)", file=sys.stderr)
                continue
            pdf = os.path.join(cache, "digest", f"{year}.pdf")
            if not os.path.exists(pdf):
                fetch(URL.format(y=year, p=VOLS[year]), pdf)
            with gzip.open(gz + ".part", "wb") as f:
                f.write(subprocess.run(["pdftotext", pdf, "-"], check=True, stdout=subprocess.PIPE).stdout)
            os.rename(gz + ".part", gz)
            os.remove(pdf)
        txt = gzip.open(gz, "rt", encoding="utf-8", errors="replace").read()
        rows = digest_year(year, txt)
        url = URL.format(y=year, p=VOLS[year])
        days = set()
        for r in rows:
            r["url"] = f"{url}#page={r['pdf']}"
            out.setdefault(r["date"], []).append(r)
            days.add(r["day"])
        years[year] = {"days": len(days), "hours": len(rows)}
        print(f"digest {year}: {len(days)} days, {len(rows)} hours", file=sys.stderr)
    write("digest", {"source": "the bound Congressional Record's Daily Digest (govinfo)", "years": years, "by_date": out})


# --------------------------------------------------------------------------------------------------------- unsc

UN_GUIDE = "https://research.un.org/en/docs/sc/quick/meetings/{y}"
UN_PDF = "https://documents.un.org/api/symbol/access?s={sym}&l=en&t=pdf"
UN_TIME = r"(\d{1,2})(?:\s?[.:~,]\s?(\d{2}))?\s*(a\.\s?m\.?|p\.\s?m\.?)"


def cal_dates(rx):
    """The calendar's days whose entries match rx (in `c` or `n`)."""
    from tools.bib import store
    s = store.Series(ROOT)
    out = set()
    for _, e in s.lists["cal"].entries():
        d = str(e.get("date", ""))
        if len(d) == 10 and re.search(rx, str(e.get("c")) + " " + str(e.get("n"))):
            out.add(d)
    return out


def un_meetings(cache, year, do_fetch):
    path = os.path.join(cache, "unsc", f"meetings-{year}.html")
    if not os.path.exists(path):
        if not do_fetch:
            return []
        fetch(UN_GUIDE.format(y=year), path)
    t = open(path, encoding="utf-8", errors="replace").read()
    out = []
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S):
        cells = [re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", " ", c))).strip()
                 for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)]
        if len(cells) < 3 or not cells[0].startswith("S/PV."):
            continue
        m = re.match(r"(S/PV\.\d+)", cells[0])
        dm = re.match(r"(\d{1,2})\s+([A-Za-z]+)", cells[1])
        if not m or not dm or dm.group(2) not in MONTHS:
            continue
        date = datetime.date(year, MONTHS.index(dm.group(2)) + 1, int(dm.group(1))).isoformat()
        out.append({"symbol": m.group(1), "date": date, "topic": cells[2][:200],
                    "outcome": cells[3][:200] if len(cells) > 3 else "",
                    "resolutions": re.findall(r"S/RES/(\d+)", r), "closed": "closed" in cells[0]})
    return out


def un_hours(pdf):
    t = subprocess.run(["pdftotext", pdf, "-"], check=True, stdout=subprocess.PIPE).stdout.decode("utf-8", "replace")
    t1 = re.sub(r"\s+", " ", t)
    out = {}
    m = re.search(r"Held (?:at|in) [A-Z][^,.]{2,40}[,.] on (\w+)[,.]? (\d{1,2}) (\w+) (\d{4})[,.]? at " + UN_TIME, t1, re.I)
    if m:
        out["held"] = hhmm(m.group(5), m.group(6), m.group(7))
        out["held_text"] = m.group(0)
    m = re.search(r"(?:meeting|Council) was called to order at " + UN_TIME, t1)
    if m:
        out["called"] = hhmm(m.group(1), m.group(2), m.group(3))
        out["called_text"] = m.group(0)
    rs = re.findall(r"The meeting rose at " + UN_TIME, t1)
    if rs:
        out["rose"] = hhmm(*rs[-1])
        out["rose_text"] = "The meeting rose at " + rs[-1][0] + (("." + rs[-1][1]) if rs[-1][1] else "") + " " + rs[-1][2]
    sus = re.findall(r"The meeting was suspended at " + UN_TIME + r"[^.]{0,40}?resumed at " + UN_TIME, t1)
    if sus:
        out["suspended"] = [[hhmm(*x[:3]), hhmm(*x[3:])] for x in sus]
    return out


def unsc(cache, do_fetch):
    days = cal_dates(r"Security Council|S/RES|S/PV")
    rows, years, missing = [], {}, []
    for year in range(1960, 1970):
        ms = un_meetings(cache, year, do_fetch)
        if not ms:
            print(f"unsc {year}: no meetings list in the cache (--fetch)", file=sys.stderr)
        took = 0
        for m in ms:
            if m["date"] not in days:
                continue
            pdf = os.path.join(cache, "unsc", m["symbol"].replace("/", "-") + ".pdf")
            if not os.path.exists(pdf):
                if not do_fetch:
                    missing.append(m["symbol"])
                    continue
                try:
                    import time
                    time.sleep(3)                 # politely
                    fetch(UN_PDF.format(sym=m["symbol"]), pdf)
                except Exception as ex:          # noqa: BLE001
                    print(f"unsc {m['symbol']}: {ex}", file=sys.stderr)
                    missing.append(m["symbol"])
                    continue
            with open(pdf, "rb") as f:
                if f.read(5) != b"%PDF-":
                    # the Official Document System's "LOADING" page, not the record: a check the site keeps,
                    # not got round; the file removed so that a later run asks again
                    os.remove(pdf)
                    missing.append(m["symbol"])
                    continue
            try:
                h = un_hours(pdf)
            except subprocess.CalledProcessError:
                h = {}
            m.update(h)
            m["url"] = "https://undocs.org/" + m["symbol"]
            rows.append(m)
            took += 1
        years[year] = {"meetings": len(ms), "read": took}
        print(f"unsc {year}: {len(ms)} meetings, {took} on the calendar's days read", file=sys.stderr)
    write("unsc", {"source": "the Security Council's verbatim records (S/PV), by the Dag Hammarskjold Library's "
                   "meetings lists", "years": years, "missing": missing, "meetings": rows})


# ----------------------------------------------------------------------------------------------------- launches

KSC = "19740015280"
CHRON = {1963: "19650002265", 1964: "19650018040", 1965: "19670001994", 1966: "19670029479",
         1967: "19690016269", 1968: "19700017930"}
NTRS = "https://ntrs.nasa.gov/api/citations/{id}/downloads/{id}.pdf"
ZONE_LABEL = {"EST": "Etc/GMT+5", "EDT": "Etc/GMT+4", "CST": "Etc/GMT+6", "CDT": "Etc/GMT+5",
              "MST": "Etc/GMT+7", "MDT": "Etc/GMT+6", "PST": "Etc/GMT+8", "PDT": "Etc/GMT+7",
              "GMT": "Etc/UTC", "UT": "Etc/UTC", "UTC": "Etc/UTC"}
MON3 = {m[:3]: i + 1 for i, m in enumerate(MONTHS)}


def ntrs_text(cache, nid, do_fetch, layout=False):
    pdf = os.path.join(cache, "nasa", nid + ".pdf")
    txt = os.path.join(cache, "nasa", nid + (".layout" if layout else "") + ".txt")
    if not os.path.exists(txt):
        if not os.path.exists(pdf):
            if not do_fetch:
                return None
            fetch(NTRS.format(id=nid), pdf)
        subprocess.run(["pdftotext"] + (["-layout"] if layout else []) + [pdf, txt], check=True)
    return open(txt, encoding="utf-8", errors="replace").read()


def ksc_rows(t):
    rows = []
    lines = t.split("\n")
    pno = 1
    for i, ln in enumerate(lines):
        pno += ln.count("\f")
        ln = ln.replace("\f", "")
        m = re.match(r"^\s{0,8}(\S.{1,22}?)\s{2,}(\d{1,2}) ([A-Z][a-z]{2}) (\d{2})\b\s{2,}(.*)$", ln)
        if not m or m.group(3) not in MON3:
            continue
        nxt = " ".join(lines[i + 1:i + 3])
        tm = re.search(r"\(?(\d{1,2}):(\d{2})\s*(a\.\s?m\.|p\.\s?m\.)\s*([ECMP][SD]T|GMT)\)?", nxt)
        if not tm:
            continue
        y = 1900 + int(m.group(4))
        try:
            d = datetime.date(y, MON3[m.group(3)], int(m.group(2))).isoformat()
        except ValueError:
            continue
        cont = lines[i + 1][:18].strip() if not re.match(r"^\s*\(?\d", lines[i + 1][:18].strip() or "0") else ""
        remarks = " ".join(x[60:].strip() if len(x) > 60 else "" for x in lines[i:i + 8])
        rows.append({"name": (m.group(1).strip() + (" " + cont if cont else "")).strip(), "date": d,
                     "local": hhmm(tm.group(1), tm.group(2), tm.group(3)), "label": tm.group(4),
                     "zone": ZONE_LABEL[tm.group(4)], "vehicle": m.group(5).split("  ")[0].strip(),
                     "printed": f"{m.group(2)} {m.group(3)} {m.group(4)}, {tm.group(0).strip('()')}",
                     "remarks": re.sub(r"\s+", " ", remarks)[:300], "pdf": pno})
    return rows


CH_DAY = re.compile(r"^(" + "|".join(MONTHS) + r")\s+(\d{1,2})(?:\s*[-–]\s*\d{1,2})?\s*[.:;]")
CH_TIME = re.compile(r"\bat\s+(\d{1,2}):(\d{2})\s*(a\.\s?m\.|p\.\s?m\.)\s*(EST|EDT|CST|PST|PDT|GMT|e\.s\.t\.|e\.d\.t\.)")
CH_LAUNCH = re.compile(r"\b(?:launch\w*|lift\w* off|liftoff|lifted|fired|orbited|blasted off)\b", re.I)


def chron_rows(year, t):
    rows, day = [], None
    pages = t.split("\f")
    for pno, page in enumerate(pages, 1):
        para = []
        for ln in page.split("\n") + [""]:
            m = CH_DAY.match(ln)
            if m or not ln.strip():
                txt = re.sub(r"\s+", " ", " ".join(para))
                if day and txt:
                    for c in CH_TIME.finditer(txt):
                        before = txt[max(0, c.start() - 250):c.start()]
                        if not CH_LAUNCH.search(before):
                            continue            # an hour, not a launch's
                        lab = c.group(4).replace(".", "").upper()
                        st = max(before.rfind(". ") + 2, 0) if before.rfind(". ") > 0 else 0
                        sent = (before[st:] + txt[c.start():c.end() + 60].split(". ")[0]).strip()
                        rows.append({"date": day, "local": hhmm(c.group(1), c.group(2), c.group(3)), "label": lab,
                                     "zone": ZONE_LABEL[lab], "sentence": sent[:300], "pdf": pno})
                para = []
            if m:
                try:
                    d = datetime.date(year, MONTHS.index(m.group(1)) + 1, int(m.group(2)))
                    if not day or d >= datetime.date.fromisoformat(day):
                        day = d.isoformat()
                except ValueError:
                    pass
            if ln.strip():
                para.append(ln)
    return rows


def launches(cache, do_fetch):
    t = ntrs_text(cache, KSC, do_fetch, layout=True)
    ksc = ksc_rows(t) if t else []
    for r in ksc:
        r["url"] = NTRS.format(id=KSC) + f"#page={r['pdf']}"
    print(f"launches: KSC summary, {len(ksc)} launches with a time", file=sys.stderr)
    chron = []
    for y, nid in sorted(CHRON.items()):
        t = ntrs_text(cache, nid, do_fetch)
        if not t:
            print(f"launches: chronology {y} not in the cache (--fetch)", file=sys.stderr)
            continue
        rs = chron_rows(y, t)
        for r in rs:
            r["url"] = NTRS.format(id=nid) + f"#page={r['pdf']}"
            r["chronology"] = y
        chron += rs
        print(f"launches: chronology {y}, {len(rs)} launch hours", file=sys.stderr)
    write("launches", {"source": "KSC, Summary of Major NASA Launchings (NTRS 19740015280); Astronautics and "
                       "Aeronautics, 1963-68 (NTRS)", "ksc": ksc, "chronology": chron})


# -------------------------------------------------------------------------------------------------------- tests

NV209 = "https://www.osti.gov/servlets/purl/1351809"


def tests(cache, do_fetch):
    pdf = os.path.join(cache, "osti", "1351809.pdf")
    if not os.path.exists(pdf):
        if not do_fetch:
            print("tests: DOE/NV-209 not in the cache (--fetch)", file=sys.stderr)
            return
        fetch(NV209, pdf)
    t = subprocess.run(["pdftotext", "-layout", pdf, "-"], check=True, stdout=subprocess.PIPE).stdout.decode("utf-8", "replace")
    rows = []
    for pno, page in enumerate(t.split("\f"), 1):
        lines = page.split("\n")
        for i, ln in enumerate(lines):
            m = re.match(r"^\s*(\d{1,4})\s+(.*?)\s*(\d\d)/(\d\d)/(\d{4})\s+(\S+)\s+(.*?)\s+(\S+)\s+"
                         r"(\d\d):(\d\d):(\d\d)\.(\d\d)\s", ln)
            if not m:
                continue
            y = int(m.group(5))
            if not 1959 <= y <= 1970:
                continue
            col = ln.index(m.group(3) + "/")
            around = [x[:col].strip() for x in lines[max(0, i - 1):i + 1]]       # the name: this line or the one above
            place = " ".join(x[col + 25:col + 75].strip() for x in lines[max(0, i - 2):i + 2]
                             if not re.search(r"\d\d:\d\d:\d\d", x) or x is ln)
            rows.append({"no": int(m.group(1)), "date": f"{y}-{m.group(3)}-{m.group(4)}",
                         "utc": f"{m.group(9)}:{m.group(10)}:{m.group(11)}", "sponsor": m.group(6),
                         "location": re.sub(r"\s+", " ", m.group(7)).strip(), "type": m.group(8),
                         "name": re.sub(r"^\d+\s*", "", m.group(2)).replace("\uf0bd", "").strip(),
                         "names": [re.sub(r"^\d+\s*", "", x).replace("\uf0bd", "").strip() for x in around if x],
                         "place": re.sub(r"\s+", " ", place)[:120], "pdf": pno, "url": NV209 + f"#page={pno}"})
    seen, uniq = {}, []
    for r in rows:                     # the table by date first; the same test again in the tables after it, its
        if r["no"] not in seen:        # name on its own line there: the names joined
            seen[r["no"]] = r
            uniq.append(r)
        else:
            seen[r["no"]]["names"] = sorted(set(seen[r["no"]]["names"]) | {r["name"]} - {""})
    rows = uniq
    print(f"tests: DOE/NV-209, {len(rows)} tests of 1959-70", file=sys.stderr)
    write("tests", {"source": "DOE/NV-209 Rev. 16 (2015), United States Nuclear Tests (OSTI 1351809)", "tests": rows})


# --------------------------------------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("tier", choices=["digest", "unsc", "launches", "tests", "all"])
    ap.add_argument("--cache", required=True)
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args()
    for t in (["digest", "unsc", "launches", "tests"] if a.tier == "all" else [a.tier]):
        globals()[t](a.cache, a.fetch)


if __name__ == "__main__":
    main()
