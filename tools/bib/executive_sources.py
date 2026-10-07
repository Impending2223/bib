"""The sources of the Executive Branch roster: each holder's `src`, named and linked.

A holder's `src` is a list of short forms (the schema: tools/bib/executive.py). They are read here and shown as one
line under the holder's dates, every source linked where it can be:

    CDIR 1961-04                 the Congressional Directory of that month (govinfo); 'CDIR 1965-03 to 1967-12'
                                 for a run of editions
    Cong. Rec.                   the Senate's proceedings on the days the nomination was received and confirmed
                                 (the bound Record, govinfo); 'CR, Feb. 18, 1954' for a named day;
                                 'Cong. Rec. 1973, 6695' for a page
    Cong. Rec. Index 1961        the Record's Index for the year (bare: the years of nomination and confirmation)
    POCOM                        the Office of the Historian's page for the person
    FRUS persons list[, 1961–63, V]   the lists of persons of the FRUS volumes that give the holder
    FRUS 1961–63, IX, doc. 144   a document
    Wikipedia: Title             the article
    APP[ YYYY-MM-DD]             the American Presidency Project, searched for the holder (on that day)
    Federal Register, Jan. 20, 1953   the issue (govinfo)
    a URL                        the page, labeled by its site
    anything else                sources/executive-sources.yaml, the register of named works: each a pattern,
                                 the full citation, and its link; else shown as written

The lookups (Senate days, Index volumes, POCOM ids, FRUS volumes) are in sources/executive-links.json, made by
tools/executive/make_source_links.py; the build needs no network.

Labels: CDir. (the Congressional Directory), CR (the Congressional Record), FR (the Federal Register), DSB (the
Department of State Bulletin), GOM (the Government Organization Manual), APP (the American Presidency Project), FRUS by
subseries, volume and doc.

STYLE:
 1. One line, "Sources:", muted and small, after the holder's date line and note. Sources in the order written;
    several editions of the Directory together ("CDir., Mar. 1953, Jan. 1954"), several Senate days together.
 2. Short labels in the line; the register's full citations in the page's list of sources.
"""
import json
import os
import re
from urllib.parse import quote, urlencode

from . import store

MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
MONTH_NUM = {m.rstrip("."): i for i, m in enumerate(MONTHS, 1)}
MONTH_NUM.update({"Sept": 9, "Sep": 9, "June": 6, "July": 7, "May": 5, "January": 1, "February": 2, "March": 3,
                  "April": 4, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12})


def roman(n):
    out = ""
    for v, r in ((50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            out, n = out + r, n - v
    return out


ROMAN = {roman(i): i for i in range(1, 80)}
GOVINFO = "https://www.govinfo.gov"
CDIR_COLL = GOVINFO + "/app/collection/cdir"
CRECB_COLL = GOVINFO + "/app/collection/crecb"

# The editions of the Congressional Directory on govinfo, 1952-74 (package ids)
CDIR = ["1952-01-08", "1953-03-01", "1954-01-18", "1955-02-14", "1956-01-03", "1957-03-01", "1958-01-07", "1959-03-01",
        "1960-01-06", "1961-04-01", "1962-01-10", "1963-03-01", "1964-01-01", "1965-03-01", "1966-01-10",
        "1967-02-28", "1967-12-15", "1969-03-01", "1969-12-15", "1971-03-10", "1971-12-03", "1973-03-10",
        "1973-12-22"]

_LINKS = None
_REG = None


def links():
    global _LINKS
    if _LINKS is None:
        p = os.path.join(store.ROOT, "sources", "executive-links.json")
        _LINKS = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return _LINKS


def register():
    """sources/executive-sources.yaml: [{match, cite, short, url, urls, n}], each match compiled."""
    global _REG
    if _REG is None:
        p = os.path.join(store.ROOT, "sources", "executive-sources.yaml")
        _REG = []
        for r in (store.load_yaml(p) or []) if os.path.exists(p) else []:
            try:
                _REG.append(dict(r, rx=re.compile(r["match"] + r"$")))
            except (re.error, KeyError):
                pass
    return _REG


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def a(url, text):
    return f'<a href="{esc(url)}">{text}</a>'


def fmt_day(d):
    y, m, dd = d[:4], int(d[5:7]), int(d[8:10])
    return f"{MONTHS[m - 1]} {dd}, {y}"


def fmt_month(d):
    return f"{MONTHS[int(d[5:7]) - 1]} {d[:4]}"


# ---------------------------------------------------------------- reading the list

KNOWN = re.compile(r"^(CDIR|Congressional Directory|Cong\. Rec|CR,|Wikipedia|POCOM|FRUS|APP|https?://|Federal Register"
                   r"|K–J |Viet\. |Wg\. |Adm\. |Opp\. |Cong\. |1968 |Part III|cal\.|executive/)")
FRAGMENT = re.compile(r"^(exhibit \d+|p\. \d+|pp\. [\d, –-]+|app\. [IVX]+|[IVXL]+|\d{4}–\d{4}|\d{4}\)|\d{4}-\d{2})$")


def items(src):
    """The `src` list as written, with a citation the flow list split at its commas put back together:
    ['Buck', 'A History of ... (DOE', '1983)'] -> ['Buck, A History of ... (DOE, 1983)']; 'Wikipedia' then bare
    titles -> 'Wikipedia: Title'; 'CDIR 1959-03', '1960-01' -> two editions."""
    out, wiki, used = [], False, False
    for raw in store.as_list(src):
        s = str(raw).strip()
        if not s:
            continue
        if out and out[-1].count("(") > out[-1].count(")"):
            out[-1] += ", " + s
            continue
        if re.match(r"^\d{4}-\d{2}$", s) and out and out[-1].startswith("CDIR"):
            out.append("CDIR " + s)
            continue
        if out and FRAGMENT.match(s):
            out[-1] += ", " + s
            continue
        if s == "Wikipedia":
            if wiki and not used:
                out.append("Wikipedia")
            wiki, used = True, False
            continue
        if wiki and not KNOWN.match(s) and not any(r["rx"].match(s) for r in register()):
            out.append("Wikipedia: " + s)       # 'Wikipedia', then the titles the flow list split off
            used = True
            continue
        if wiki and not used:
            out.append("Wikipedia")             # a bare 'Wikipedia' before another source
        wiki = False
        if s == "Buck":     # the author, before the title the list split off
            out.append(s)
            continue
        if out and out[-1] == "Buck":
            out[-1] = "Buck, " + s
            continue
        out.append(s)
    if wiki and not used:
        out.append("Wikipedia")
    return out


# ---------------------------------------------------------------- one source

def cdir_edition(ym):
    """'1961-04' -> '1961-04-01', the edition of that month; None if there is none."""
    for e in CDIR:
        if e.startswith(ym):
            return e
    return None


def cdir_link(ym):
    e = cdir_edition(ym)
    return a(f"{GOVINFO}/app/details/CDIR-{e}", fmt_month(e)) if e else esc(fmt_month(ym + "-01"))


def senate_link(day):
    g = links().get("senate", {}).get(day)
    if not g:
        return None
    y = day[:4]
    pkg = g.rsplit("-", 2)[0]
    return a(f"{GOVINFO}/content/pkg/{pkg}/pdf/{g}.pdf", fmt_day(day))


def index_link(year):
    g = links().get("index", {}).get(str(year))
    if not g:
        return None
    pkg = g.rsplit("-", 1)[0]
    return a(f"{GOVINFO}/content/pkg/{pkg}/pdf/{g}.pdf", f"CR Index, {year}")


def frus_volume(sub, vol):
    """('1961–63', 'VII–IX', supp) -> 'frus1961-63v07-09mSupp'; ('1969–76', 'E-1') -> 'frus1969-76ve01'."""
    sub = sub.replace("–", "-")
    vols = set(links().get("volumes") or [])
    m = re.match(r"E[-–](\d+)$", vol)
    if m:
        base = f"frus{sub}ve{int(m.group(1)):02d}"
    else:
        parts = [ROMAN.get(x) for x in re.split(r"[-–]", vol)]
        if not all(parts):
            return None
        base = f"frus{sub}v" + "-".join(f"{p:02d}" for p in parts)
    for cand in (base, base + "mSupp", base + "p1", base + "mSupp1"):
        if cand in vols or not vols:
            return cand
    return None


def frus_label(vid):
    m = re.match(r"frus(\d{4})-(\d{2})v(e?)(\d{2})(?:-(\d{2}))?(.*)$", vid)
    if not m:
        return vid
    vol = f"E-{int(m.group(4))}" if m.group(3) else roman(int(m.group(4))) + (f"–{roman(int(m.group(5)))}" if m.group(5) else "")
    rest = m.group(6)
    rest = ", microfiche supp." if rest.startswith("mSupp") else (f", pt. {rest[1:]}" if rest.startswith("p") else "")
    return f"FRUS {m.group(1)}–{m.group(2)}, {vol}{rest}"


def frus_html(s, h):
    """'FRUS 1961–63, IX, doc. 144'; 'FRUS persons list[, 1961–63, V[ and VII]]'."""
    base = "https://history.state.gov/historicaldocuments/"
    m = re.match(r"FRUS (\d{4}–\d{2}), ([IVXLE][IVXL\-–\d]*)(, (?:microfiche|mf\.) supp\.)?, docs?\. ([\d, ]+)$", s)
    if m:
        vid = frus_volume(m.group(1), m.group(2))
        nums = re.findall(r"\d+", m.group(4))
        if vid:
            ds = ", ".join(a(f"{base}{vid}/d{n}", n) for n in nums)
            return f"{esc(frus_label(vid))}, doc{'s' if len(nums) > 1 else ''}. {ds}"
        return esc(s)
    m = re.match(r"FRUS persons list(?:, (\d{4}–\d{2})(?:, (.+))?)?$", s)
    if not m:
        return esc(s)
    if m.group(2):
        vids = [frus_volume(m.group(1), v.strip()) for v in re.split(r",| and ", m.group(2)) if v.strip()]
    else:
        vids = links().get("frus", {}).get(h["name"], [])
        if m.group(1):
            want = "frus" + m.group(1).replace("–", "-")
            vids = [v for v in vids if v.startswith(want)] or vids
    vids = [v for v in vids if v]
    if not vids:
        return esc(s)
    return "; ".join(a(f"{base}{v}/persons", esc(frus_label(v)) + ", persons") for v in vids)


def app_html(s, h):
    """APP searched for the holder's surname, on the day given if one is."""
    sur = re.sub(r"\s*\([^)]*\)", "", h["name"]).split(",")[0]
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    day = None
    if m:
        day = f"{m.group(2)}-{m.group(3)}-{m.group(1)}"
    else:
        m = re.search(r"(Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)\.? (\d+), (\d{4})", s)
        if m:
            day = f"{MONTH_NUM[m.group(1)]:02d}-{int(m.group(2)):02d}-{m.group(3)}"
    q = {"field-keywords": sur, "items_per_page": 100}
    if day:
        q.update({"from[date]": day, "to[date]": day})
    label = "APP" + (s[3:] if s.startswith("APP:") else (f", {fmt_day(f'{day[6:]}-{day[:2]}-{day[3:5]}')}" if day else ""))
    return a("https://www.presidency.ucsb.edu/advanced-search?" + urlencode(q), esc(label))


def days_in(s):
    """'Federal Register, Dec. 16, 1952, Jan. 27 and Feb. 17, 1953' -> ['1952-12-16', '1953-01-27', '1953-02-17']."""
    out, pend = [], []
    for m in re.finditer(r"(Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)\.? (\d+)(?:, (\d{4}))?", s):
        pend.append((MONTH_NUM[m.group(1)], int(m.group(2))))
        if m.group(3):
            out += [f"{m.group(3)}-{mm:02d}-{dd:02d}" for mm, dd in pend]
            pend = []
    return out


def url_html(u):
    host = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
    m = re.match(r"https://history\.state\.gov/historicaldocuments/(frus[^/]+)/d(\d+)$", u)
    if m:
        return a(u, f"{esc(frus_label(m.group(1)))}, doc. {m.group(2)}")
    m = re.match(r"https://archive\.org/details/([^/?#]+)", u)
    if m:
        return a(u, "archive.org: " + esc(m.group(1)))
    if host == "presidency.ucsb.edu":
        slug = u.rstrip("/").rsplit("/", 1)[-1].replace("-", " ")
        return a(u, "APP: " + esc(slug[:60] + ("…" if len(slug) > 60 else "")))
    return a(u, esc(host))


def reg_html(s):
    for r in register():
        m = r["rx"].match(s)
        if not m:
            continue
        g = [m.group(0)] + list(m.groups())
        f = lambda t: (t or "").format(*[x or "" for x in g])
        label = esc(f(r.get("short") or r.get("cite") or s))
        url = f((r.get("urls") or {}).get(m.group(1))) if m.groups() and r.get("urls") else None
        url = url or f(r.get("url"))
        return a(url, label) if url else label
    return None


def one(s, h, ctx=None):
    """(group, html): a source, linked; group gathers several of a kind into one ("CDir., Mar. 1953, Jan. 1954")."""
    m = re.match(r"^CDIR (\d{4}-\d{2})(?: to (\d{4}-\d{2}))?$", s)
    if m:
        t = cdir_link(m.group(1))
        if m.group(2):
            t += " to " + cdir_link(m.group(2))
        return "CDir.", t
    if s in ("CDIR", "Congressional Directory"):
        return None, a(CDIR_COLL, "CDir.")
    if s == "Cong. Rec.":
        days = [str(h[k]) for k in ("nominated", "confirmed") if len(str(h.get(k) or "")) == 10]
        ls = [x for x in (senate_link(d) for d in dict.fromkeys(days)) if x]
        return ("CR, Senate", ", ".join(ls)) if ls else (None, a(CRECB_COLL, "CR"))
    m = re.match(r"^CR, (.+)$", s)
    if m:
        ls = [senate_link(d) or esc(fmt_day(d)) for d in days_in(s)]
        return "CR, Senate", ", ".join(ls) or esc(s)
    m = re.match(r"^Cong\. Rec\. (\d{4}), ([\d, ]+)$", s)
    if m:
        out = []
        for p in re.findall(r"\d+", m.group(2)):
            g = links().get("pages", {}).get(f"{m.group(1)}|{p}")
            out.append(a(f"{GOVINFO}/content/pkg/{g.rsplit('-', 2)[0]}/pdf/{g}.pdf", p) if g else p)
        return None, f"CR {m.group(1)}, " + ", ".join(out)
    m = re.match(r"^Cong\. Rec\. Index(?: (\d{4}))?$", s)
    if m:
        years = [m.group(1)] if m.group(1) else list(dict.fromkeys(
            str(h[k])[:4] for k in ("nominated", "confirmed") if h.get(k)))
        ls = [index_link(y) or f"CR Index, {y}" for y in years]
        return None, "; ".join(ls) if ls else a(CRECB_COLL, "CR Index")
    if s == "POCOM":
        pid = links().get("pocom", {}).get(h["name"])
        url = f"https://history.state.gov/departmenthistory/people/{pid}" if pid else \
            "https://history.state.gov/departmenthistory/people/principals-chiefs"
        return None, a(url, "POCOM")
    if s.startswith("FRUS"):
        return None, frus_html(s, h)
    m = re.match(r"^Wikipedia(?:: (.+))?$", s)
    if m:
        if m.group(1):
            t = m.group(1)
            return None, a("https://en.wikipedia.org/wiki/" + quote(t.replace(" ", "_")), "Wikipedia, “" + esc(t) + "”")
        given = h.get("given") or ""
        bare = re.sub(r"\s*\([^)]*\)", "", h["name"]).split(",")
        q = " ".join(x.strip() for x in ([given or (bare[1] if len(bare) > 1 else "")] + [bare[0]]) if x.strip())
        return None, a("https://en.wikipedia.org/w/index.php?" + urlencode({"search": q}), "Wikipedia")
    if s.startswith("APP"):
        return None, app_html(s, h)
    if s.startswith("Federal Register"):
        ds = days_in(s)
        if ds:
            return None, "FR, " + ", ".join(
                a(f"{GOVINFO}/content/pkg/FR-{d}/pdf/FR-{d}.pdf", fmt_day(d)) for d in ds)
    if re.match(r"^https?://", s):
        return None, url_html(s)
    m = re.match(r"^cal\.(\d{4}-\d{2}-\d{2})\.", s)
    if m:
        return None, a(f"cal.html#{s}", "Cal. " + fmt_day(m.group(1)))
    if ctx:
        t = series_html(s, *ctx)
        if t:
            return None, t
    r = reg_html(s)
    if r is not None:
        return None, r
    return None, esc(s)


def series_html(s, linker, href):
    """'K–J Adm. III.G' (or 'Part III: K–J Adm. III.G'): the section in the series, linked as the build links
    a cross-list reference."""
    s = re.sub(r"^Part III: ", "", s)
    hits = list(linker.refs.scan(s, None))
    if len(hits) != 1 or hits[0][0] != 0 or hits[0][1] != len(s) or not hits[0][3]:
        return None
    _, _, key, code = hits[0]
    sec = linker.refs.section_for(key, code)
    if not sec:
        return None
    url = href(key, sec.id)     # a list page: kja.html#p3g; the series reader: #kja--p3g
    if url.startswith("#"):
        url = f"#{key}--{sec.id}"
    return a(url, esc(s))


def resolved(s, h):
    """Whether a source is linked (for check). A reference to the series counts: the build links it."""
    return "<a " in one(s, h)[1] or bool(SERIES_RE.match(s))


SERIES_RE = re.compile(r"^(?:Part III: )?(?:K–J Adm\.|K–J Cong\.|Opp\.|Adm\.|Cong\.|Wg\.|Viet\.|1968|Cal\.) [IVX]+\.[A-Z][\w.]*$")


def html(h, ctx=None):
    """The holder's sources as one line, or ''. ctx: (linker, href) to link references to the series."""
    srcs = items(h.get("src"))
    if not srcs:
        return ""
    parts, groups = [], {}
    for s in srcs:
        g, t = one(s, h, ctx)
        if g:
            if g in groups:
                parts[groups[g]] += ", " + t
                continue
            groups[g] = len(parts)
            t = f"{g}, {t}"
        if t not in parts:
            parts.append(t)
    return '<span class="exs">Sources: ' + "; ".join(parts) + ".</span>"


# ---------------------------------------------------------------- the page's list

KINDS = [
    ("CDir.", "*Congressional Directory*, each session's edition, 1952–74 (Government Printing Office; govinfo). "
                   "Each department's and agency's officers by title, at the date of the edition."),
    ("CR", "*Congressional Record*, bound edition (govinfo): the Senate's proceedings on the day a nomination "
                   "was received and on the day it was confirmed; the annual Index, under the nominee's name."),
    ("POCOM", "Office of the Historian, U.S. Department of State, *Principal Officers and Chiefs of Mission* "
              "(history.state.gov): State's officers and the chiefs of mission, with commission, credentials, "
              "and end of mission."),
    ("FRUS", "*Foreign Relations of the United States* (Office of the Historian): the volumes' lists of persons, "
             "which give each person's offices and dates; documents, by volume and number."),
    ("Wikipedia", "Wikipedia: the articles on persons and offices, and the lists of officeholders; leads, where "
                  "no official source was at hand."),
    ("APP", "Gerhard Peters and John T. Woolley, *The American Presidency Project* (presidency.ucsb.edu): "
            "nominations, appointments, resignations, and orders, by date."),
    ("FR", "*Federal Register* (govinfo): executive orders and designations, by issue."),
]


def section(units):
    """The page's list of sources: the kinds read mechanically, then the register's works, each with the number
    of tenures that cite it."""
    from .markup import to_html
    counts = {}
    for u in units.values():
        for o in u.get("offices") or []:
            for h in o.get("holders") or []:
                for s in items(h.get("src")):
                    k = kind(s)
                    counts[k] = counts.get(k, 0) + 1
    out = ['<h2 id="sources" data-short="Sources">The sources</h2>',
           '<p class="logic">Where the names and dates come from. Each holder\'s line ends with its sources, '
           'linked: the edition of the Directory, the day in the Record, the page or volume. The number after each '
           'source is the count of tenures that cite it.</p><ol class="e exauth">']
    for k, t in KINDS:
        if counts.get(k):
            out.append(f'<li>{to_html(t)} <span class="exd">{counts[k]}.</span></li>')
    for r in register():
        n = counts.get(r["match"], 0)
        if not n or not r.get("cite"):
            continue
        cite = to_html(r["cite"].format(*([""] * 10)).replace(" , ", ", ").strip(" ,"))
        url = r.get("url") if r.get("url") and "{" not in r["url"] else None
        if url:
            cite = f'<a href="{esc(url)}">{cite}</a>' if "<a " not in cite else cite
        note = f" {to_html(r['n'])}" if r.get("n") else ""
        out.append(f'<li>{cite}.{note} <span class="exd">{n}.</span></li>')
    out.append("</ol>")
    return out


def kind(s):
    """The kind a source belongs to, for the counts: a KINDS label or a register entry's match."""
    for pre, k in (("CDIR", "CDir."), ("Congressional Directory", "CDir."), ("Cong. Rec", "CR"),
                   ("CR,", "CR"), ("POCOM", "POCOM"), ("FRUS", "FRUS"), ("Wikipedia", "Wikipedia"),
                   ("APP", "APP"), ("https://www.presidency.ucsb.edu", "APP"), ("https://history.state.gov", "FRUS"),
                   ("Federal Register", "FR")):
        if s.startswith(pre):
            return k
    for r in register():
        if r["rx"].match(s):
            return r["match"]
    return None


def unlinked(units):
    """(where, source) for every source the line cannot link, for check."""
    out = []
    for u in units.values():
        for o in u.get("offices") or []:
            for h in o.get("holders") or []:
                for s in items(h.get("src")):
                    if not resolved(s, h):
                        out.append((f"{u['unit']}.yaml: {o.get('id') or o.get('title')}: {h['name']}", s))
    return out
