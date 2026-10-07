"""The Executive Branch, Jan. 20, 1953, to Aug. 31, 1974: every office, its authority in law, and its holders.

    executive/<unit>.yaml   one department, agency, or office of the President: its offices and their holders
                            (kept by hand; executive/missions.yaml and the State offices were seeded from POCOM
                            by tools/executive/make_state.py)

build/executive.html gives the roster at each inauguration (and Johnson's and Ford's successions), with every
change during the term. A calendar entry tagged executive:<YYYY-MM-DD> carries that term's block, in cal.html
and the reader.

A unit file:

    unit: state                    # the file's key; executive/state.yaml
    name: Department of State
    under: president               # the unit it reports to ("president" is the top)
    order: 30                      # its place among the units under the same parent
    from: '1953-04-11'             # created, where within the period; until: abolished or transferred
    names: [{name: ..., from: ...}]   # earlier or later names, where it was renamed in the period
    law: [AUTHORITY, ...]          # the acts, plans, and orders that establish it and set its authority
    n: a note
    offices: [OFFICE, ...]         # in display order

An office:

    - id: secretary                # unique in the unit; the roster's key is "state.secretary"
      title: Secretary of State
      titles: [{title: ..., from: ...}]   # where the title changed in the period
      rank: head | principal | inferior | employee | military
      appt: PAS | PA | HD | VP | XO | DES | MIL | CAREER | ELECTED   (see APPT)
      under: under-secretary       # the office it reports to, where not the unit's head ("unit.office" across units)
      group: Regional bureaus      # a subheading in the unit's table
      level: II                    # the Executive Schedule level (Federal Executive Salary Act of 1964)
      many: true                   # several hold it at once (commissioners, special assistants, staff)
      from: / until:               # created or abolished in the period
      law: [AUTHORITY, ...]
      n: a note
      holders: [HOLDER, ...]       # in order of taking office

A holder:

    - name: Rusk, Dean             # Surname, Given[, Jr.], as Part III writes it
      given: David Dean            # the full given names, where the name shortens them
      rank: Gen., USA              # a military officer's grade and service
      title: ...                   # the title held, where it differs from the office's
      acting: true                 # acting, by designation or by statute
      nominated: '1961-01-20'      # sent to the Senate
      confirmed: '1961-01-20'
      recess: '1961-01-21'         # a recess appointment: the commission signed while the Senate was away
      appointed: '1961-01-21'      # the commission, or the appointment where there is no commission
      from: '1961-01-21'           # took office: the oath, entry on duty, or assumption of command (required)
      to: '1969-01-20'             # left office; none if still there on Aug. 31, 1974
      out: Resigned.               # how it ended, clipped: "Resigned." "Died." "To Secretary of Defense."
      n: a note; "Check" marks a detail to verify
      src: [POCOM, CDIR 1961-04, https://...]   # the forms: tools/bib/executive_sources.py

An authority:

    - act: National Security Act of 1947      # the act, plan, or order, by its name or date
      date: '1947-07-26'                      # enacted, or in effect for a plan; signed for an order
      cite: 'ch. 343, § 101, 61 Stat. 495, 496'   # Statutes at Large: the page the act begins on, then the pin
      usc: '50 U.S.C. § 402 (1958)'           # as codified in the period's edition, where it was
      does: Establishes the Council.          # one clipped line
      url: https://...                        # where the cite alone does not link (orders, plans)

Dates: 'YYYY-MM-DD', or 'YYYY-MM' or 'YYYY' where the day is not known.

STYLE:
 1. Each term shows every office that existed during it, the holder at its start and every change through its
    end. Holders who left on or before the first day of the term show only in the term before. Vacancies are
    computed from the appointed holders' dates ("Vacant, Jan. 20–21, 1961"); an acting officer serves in a
    vacancy without filling it, and shows under it. A one-day handover is not a vacancy unless someone acted.
 2. A holder's line: the dates of nomination, confirmation, commission (or recess commission), and taking
    office, the year once per run; then the date of leaving and how; then the note, in the same style. Acting
    officers say so, with their span.
 3. Authorities link to the Statutes at Large on govinfo by volume and the page the act begins on.
"""
import os
import re
from collections import defaultdict

from . import store, executive_sources
from .markup import to_html, plain

DIR = os.path.join(store.ROOT, "executive")
START, END = "1953-01-20", "1974-08-31"
# Each term: its first day, the President, and how it began.
TERMS = [("1953-01-20", "Eisenhower", "Dwight D. Eisenhower, first term"),
         ("1957-01-20", "Eisenhower", "Dwight D. Eisenhower, second term"),
         ("1961-01-20", "Kennedy", "John F. Kennedy"),
         ("1963-11-22", "Johnson", "Lyndon B. Johnson, succeeding"),
         ("1965-01-20", "Johnson", "Lyndon B. Johnson, elected"),
         ("1969-01-20", "Nixon", "Richard M. Nixon, first term"),
         ("1973-01-20", "Nixon", "Richard M. Nixon, second term"),
         ("1974-08-09", "Ford", "Gerald R. Ford, succeeding")]
RANK = {"head": "Head", "principal": "Principal officer", "inferior": "Inferior officer",
        "employee": "Employee", "military": "Military officer"}
APPT = {"PAS": "the President, by and with the advice and consent of the Senate",
        "PA": "the President alone",
        "HD": "the head of the department or agency",
        "VP": "the Vice President, as President of the Senate: Senate employees, paid by the Secretary of the Senate",
        "XO": "ex officio: held by virtue of another office",
        "DES": "designated by the President from among other officers",
        "MIL": "a military officer, assigned or detailed to the post; the Senate confirms the grade, and for the chiefs and the major commands the post",
        "CAREER": "the career service: a Foreign Service or civil-service officer, assigned by the department; not a political appointment",
        "ELECTED": "elected"}
# The Executive Schedule: the Federal Executive Salary Act of 1964, title III (Pub. L. 88-426, 78 Stat. 400, 415),
# in force with the first pay period beginning on or after July 1, 1964; 5 U.S.C. §§ 5311-5316 from 1966.
LEVELS_FROM = "1964-07-01"
LEVELS = {"I": "the heads of the executive departments",
          "II": "the deputy heads of the largest departments, the service secretaries, the heads of the principal agencies",
          "III": "the under secretaries, the heads of lesser agencies",
          "IV": "the assistant secretaries, general counsels, members of the larger commissions",
          "V": "the heads of bureaus, members of the lesser boards"}
# The rates, with the day each took effect: the 1964 act (§ 303); the Federal Salary Act of 1967, § 215 (levels
# III-V, Dec. 1967); the President's recommendations under § 225 of that act, in force Feb. 1969 (34 Fed. Reg. 2241).
# No change to Aug. 1974. The pay entries on each office give the authorities.
RATES = [("1964-07-01", {"I": 35000, "II": 30000, "III": 28500, "IV": 27000, "V": 26000}),
         ("1967-12", {"I": 35000, "II": 30000, "III": 29500, "IV": 28750, "V": 28000}),
         ("1969-02-14", {"I": 60000, "II": 42500, "III": 40000, "IV": 38000, "V": 36000})]


def level_rates(lv, a, b):
    """'$28,500 (July 1964); $29,500 (Dec. 1967)': the level's rates in force in [a, b)."""
    out = []
    for i, (d, r) in enumerate(RATES):
        nxt = RATES[i + 1][0] if i + 1 < len(RATES) else None
        if lo(d) < lo(b) and (not nxt or lo(nxt) > lo(a)) and lv in r:
            out.append(f"${r[lv]:,} (from {MONTHS[int(d[5:7]) - 1]} {d[:4]})")
    return "; ".join(out)
KEY = ("PAS: appointed by the President with the advice and consent of the Senate. PA: by the President alone. "
       "HD: by the head of the department or agency. VP: by the Vice President. XO: ex officio. DES: designated by the President from among "
       "other officers. MIL: a military officer assigned to the post. CAREER: a Foreign Service or civil-service "
       "officer, not a political appointment. ELECTED: the President and Vice President.")
KEY_LEVELS = (" Levels I–V: the pay grades of the Executive Schedule, fixed by the Federal Executive Salary Act of 1964 "
              "for each office by name (I, $35,000, the heads of departments; II, $30,000; III, $28,500; IV, $27,000; "
              "V, $26,000); levels III–V raised in Dec. 1967 (Federal Salary Act of 1967), all five in Feb. 1969 ($60,000, "
              "$42,500, $40,000, $38,000, $36,000). A level marks rank as well as pay.")
UNIT_KEYS = {"unit", "name", "names", "under", "order", "from", "until", "law", "n", "offices"}
OFFICE_KEYS = {"id", "title", "titles", "rank", "appt", "under", "group", "level", "many", "from", "until",
               "law", "n", "holders"}
HOLDER_KEYS = {"name", "given", "rank", "title", "acting", "nominated", "confirmed", "recess", "appointed", "from", "to",
               "out", "n", "src"}
LAW_KEYS = {"act", "date", "effective", "until", "tags", "cite", "usc", "does", "url"}
# What an authority does for its unit or office (the label shown before it).
TAGS = {"creates": "Creates", "powers": "Powers", "appointment": "Appointment", "vacancy": "Vacancy",
        "pay": "Pay", "reorganizes": "Reorganizes"}
DATE_RE = re.compile(r"^\d{4}(-(0[1-9]|1[0-2])(-(0[1-9]|[12]\d|3[01]))?)?$")


def bad_date(d):
    """Not 'YYYY', 'YYYY-MM' or a real 'YYYY-MM-DD'."""
    import datetime
    d = str(d)
    if not DATE_RE.match(d):
        return True
    if len(d) == 10:
        try:
            datetime.date.fromisoformat(d)
        except ValueError:
            return True
    return False
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
STAT_RE = re.compile(r"\b(\d+) Stat\. (\d+)")


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


# ---------------------------------------------------------------- data

_LOADED = {}


def load():
    """{unit key: unit}, every file in executive/; parsed once a process while the files are unchanged."""
    if not os.path.isdir(DIR):
        return {}
    stamp = tuple((f, os.path.getmtime(os.path.join(DIR, f))) for f in sorted(os.listdir(DIR)) if f.endswith(".yaml"))
    if _LOADED.get("stamp") != stamp:
        _LOADED.update(stamp=stamp, units=_load())
    return _LOADED["units"]


def _load():
    out = {}
    for f in sorted(os.listdir(DIR)):
        if f.endswith(".yaml"):
            d = store.load_yaml(os.path.join(DIR, f)) or {}
            if isinstance(d, dict) and d.get("unit"):
                d["_file"] = f
                out[d["unit"]] = d
    return out


def lo(d):
    """A date as the earliest day it can mean, for sorting: '1961' -> '1961-00-00'."""
    d = str(d or "")
    return d + "-00" * (2 - d.count("-")) if d else ""


def hi(d):
    d = str(d or "")
    return d + "-99" * (2 - d.count("-")) if d else ""


def fmt(d, year=True):
    p = str(d).split("-")
    if len(p) == 1:
        return p[0]
    m = MONTHS[int(p[1]) - 1]
    if len(p) == 2:
        return f"{m} {p[0]}" if year else m
    return f"{m} {int(p[2])}, {p[0]}" if year else f"{m} {int(p[2])}"


def dates_run(pairs):
    """[(label, date)] -> 'nominated Jan. 20, confirmed Jan. 20, took office Jan. 21, 1961': the year once per run."""
    out = []
    for i, (lab, d) in enumerate(pairs):
        y = str(d)[:4]
        last = i == len(pairs) - 1 or str(pairs[i + 1][1])[:4] != y or len(str(d)) < 10
        txt = fmt(d, year=last) if len(str(d)) == 10 else fmt(d)
        out.append(f"{lab} {txt}" if lab else txt)
    return ", ".join(out)


def title_at(o, day):
    t = o.get("title")
    for x in o.get("titles") or []:
        if lo(x.get("from")) <= lo(day):
            t = x["title"]
    return t


def name_at(u, day):
    t = u.get("name")
    for x in u.get("names") or []:
        if lo(x.get("from")) <= lo(day):
            t = x["name"]
    return t


def exists(x, a, b):
    """Did a unit or office exist at some time in [a, b)?"""
    return (not x.get("from") or lo(x["from"]) < lo(b)) and (not x.get("until") or hi(x["until"]) > lo(a))


def in_term(h, a, b):
    """Did the holder serve during [a, b)? One who left on the term's first day belongs to the term before.
    A leaving date known only to the month or year of Jan. 20, 1953 ('1953', '1953-01') counts as within the period."""
    t = h.get("to")
    end = hi(t) if t and lo(t) < lo(START) else lo(t)
    return lo(h["from"]) < lo(b) and (not t or end > lo(a))


def tree(units):
    """Units in display order, depth first: [(depth, unit)]."""
    kids = defaultdict(list)
    for u in units.values():
        if u["unit"] != "president":
            kids[u.get("under") or "president"].append(u)
    out = []

    def walk(parent, depth):
        for u in sorted(kids.get(parent, []), key=lambda u: (u.get("order", 999), u["name"])):
            out.append((depth, u))
            walk(u["unit"], depth + 1)
    if "president" in units:
        out.append((0, units["president"]))
    walk("president", 1 if "president" in units else 0)
    return out


def offices_in_order(u):
    """The unit's offices, each under its superior where the superior is in the unit: [(depth, office)]."""
    offs = u.get("offices") or []
    ids = {o["id"] for o in offs}
    kids = defaultdict(list)
    roots = []
    for o in offs:
        sup = o.get("under")
        if sup and sup in ids and sup != o["id"]:
            kids[sup].append(o)
        else:
            roots.append(o)
    out = []

    def walk(o, depth):
        out.append((depth, o))
        for k in kids.get(o["id"], []):
            walk(k, depth + 1)
    for o in roots:
        walk(o, 0)
    return out


# ---------------------------------------------------------------- authorities

USC_RE = re.compile(r"(\d+) U\.S\.C\. (§§?) ?([0-9][\w\-–]*)(.*?)\((\d{4})(?: Supp\. ([IVX]+))?\)")
ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6}
_USC = None


def usc_index():
    """sources/uscode-loc.json (tools/executive/make_uscode_index.py): the Library of Congress's chapter scans."""
    global _USC
    if _USC is None:
        import json
        p = os.path.join(store.ROOT, "sources", "uscode-loc.json")
        _USC = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return _USC


def sec_key(x):
    m = re.match(r"(\d+)([a-z]*)(?:[\-–](\d+))?", str(x))
    return (int(m.group(1)), m.group(2), int(m.group(3) or 0)) if m else (0, "", 0)


def usc_url(title, sec, ed, supp=0):
    """The Library's scan of the chapter of that edition holding the section, or None."""
    k = sec_key(sec)
    for it in usc_index().get(ed, []):
        if it["title"] == int(title) and it["supp"] == supp and sec_key(it["from"]) <= k <= sec_key(it["to"]):
            return it["url"]
    return None


def usc_html(cite):
    """'50 U.S.C. § 402 (1958)', linked to the 1958 edition's chapter."""
    m = USC_RE.search(cite)
    if not m:
        return esc(cite)
    sec = re.split(r"[(\s]", m.group(3))[0].rstrip("–-")
    url = usc_url(m.group(1), sec, m.group(5), ROMAN.get(m.group(6) or "", 0))
    return f'<a href="{esc(url)}">{esc(cite)}</a>' if url else esc(cite)


_STAT = None


def stat_url(vol, page, pin=None, marker=None):
    """The govinfo file for 'vol Stat. page, pin': from sources/statute-links.json (made by
    tools/executive/resolve_statutes.py, which matches the act by its chapter or public law and finds the pin
    page), else the file named by the page the act begins on."""
    global _STAT
    if _STAT is None:
        import json
        p = os.path.join(store.ROOT, "sources", "statute-links.json")
        _STAT = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    k = f"{vol}|{page}|{pin or ''}|{marker or ''}"
    if k in _STAT:
        return _STAT[k]
    return f"https://www.govinfo.gov/content/pkg/STATUTE-{vol}/pdf/STATUTE-{vol}-Pg{page}.pdf"


STAT_PIN_RE = re.compile(r"(?:(ch\. \d+|Pub\. L\. \d+-\d+)[^;]*?)?\b(\d+) Stat\. (\d+)(?:, (\d+)(?![\d.]))?")


def stat_links(html, cite=False):
    """Every 'NN Stat. PPP[, pin]' in a piece of HTML outside links, linked to govinfo; the chapter or public law
    before it, where given, picks the act."""
    if "<a " in html:
        return html

    def one(m):
        url = stat_url(m.group(2), m.group(3), m.group(4), m.group(1))
        lead = m.group(0)[:m.start(2) - m.start(0)]
        return f'{lead}<a href="{url}">{m.group(0)[len(lead):]}</a>'
    return STAT_PIN_RE.sub(one, html)


def law_html(a):
    """[Creates · Appointment] National Security Act of 1947 (July 26, 1947), ch. 343, § 101, 61 Stat. 495, 496;
    50 U.S.C. § 402 (1958). What it does."""
    tags = " · ".join(TAGS[t] for t in store.as_list(a.get("tags")) if t in TAGS)
    act = esc(a.get("act") or "")
    if a.get("url"):
        act = f'<a href="{esc(a["url"])}">{act}</a>'
    when = []
    d = a.get("date")
    if d and str(d)[:4] not in (a.get("act") or ""):
        when.append(("ratified " if (a.get("act") or "").startswith("Constitution, Amend") else "") + fmt(d))
    if a.get("effective"):
        when.append(f"in force {fmt(a['effective'])}")
    if a.get("until"):
        when.append(f"until {fmt(a['until'])}")
    t = (f'<span class="exg">{tags}</span> ' if tags else "") + act
    if when:
        t += f' <span class="exw">({"; ".join(when)})</span>'
    if a.get("cite"):
        t += ", " + stat_links(esc(a["cite"]), cite=True)
    usc = store.as_list(a.get("usc"))
    if usc:
        t += "; " + "; ".join(usc_html(x) for x in usc)
    t += "."
    if a.get("does"):
        t += " " + stat_links(to_html(a["does"]))
    return t


def in_force(a, x, y):
    """In force at some time in [x, y): taken effect before y, not repealed by x."""
    start = a.get("effective") or a.get("date")
    return (not start or lo(start) < lo(y)) and (not a.get("until") or lo(a["until"]) > lo(x))


# ---------------------------------------------------------------- holders

def holder_line(h, a, b, o=None):
    """The holder's dates, as one clipped line (HTML)."""
    pairs = []
    if h.get("acting"):
        t = f"Acting, {span(h['from'], h.get('to'))}."
    else:
        if h.get("recess"):
            pairs.append(("recess appointment", h["recess"]))
        if h.get("nominated"):
            pairs.append(("nominated", h["nominated"]))
        if h.get("confirmed"):
            pairs.append(("confirmed", h["confirmed"]))
        if h.get("appointed") and h.get("appointed") != h.get("recess"):
            com = h.get("confirmed") or h.get("recess") or (o or {}).get("appt") in ("PAS", "MIL")
            pairs.append(("commissioned" if com else "appointed", h["appointed"]))
        pairs.append(("took office", h["from"]))
        t = dates_run(pairs)
        t = t[0].upper() + t[1:] + "."
        if h.get("to"):
            t += f" Left {fmt(h['to'])}."
    if h.get("out"):
        t += " " + to_html(h["out"]).rstrip(".") + "."
    return t


def span(x, y=None):
    """'Jan. 20–21, 1961'; 'Nov. 22, 1963–Jan. 20, 1965'; 'from Aug. 9, 1974' where there is no end."""
    if not y:
        return f"from {fmt(x)}"
    if len(str(x)) == 10 and len(str(y)) == 10 and str(x)[:4] == str(y)[:4]:
        if str(x)[:7] == str(y)[:7]:
            return f"{fmt(x, year=False)}–{int(str(y)[8:])}, {str(y)[:4]}"
        return f"{fmt(x, year=False)}–{fmt(y)}"
    return f"{fmt(x)}–{fmt(y)}"


def holder_html(h, a, b, ptr, href, o=None):
    """The name (with grade and title), then one line: the dates, how it ended, and the note."""
    who = f"<b>{esc(h['name'])}</b>"
    extra = "; ".join(esc(x) for x in (h.get("rank"), h.get("title")) if x)
    if extra:
        who += f' <span class="exr">{extra}</span>'
    line = holder_line(h, a, b, o) + (" " + to_html(h["n"]) if h.get("n") else "")
    pts = ptr.lines(h["name"], href) if ptr else []
    return who, f'<span class="exd">{line}</span>' + executive_sources.html(h, (ptr.linker, href) if ptr else None), pts


def vacancies(o, a, b):
    """Spans within [a, b) when the office was vacant: no one held it by appointment (an acting officer serves in
    a vacancy; he does not fill it). [(from, to)], clipped to the term. A day between one holder's last day and
    the next one's first is a handover, not a vacancy, unless someone acted in it. A date known only to the
    month or year counts at its outermost: a leaving date at its latest day, a taking of office at its earliest,
    so an imprecise date never makes a vacancy the sources do not show. Each span is (from, to, sure): sure where
    both ends are known to the day (a holder's leaving and the next one's taking office), or the span runs from
    the last holder known to the day for less than three months; otherwise the sources record no holder there,
    which is not proof of a vacancy."""
    import calendar
    import datetime

    def first(d):
        p = [int(x) for x in str(d).split("-")]
        return datetime.date(p[0], p[1] if len(p) > 1 else 1, p[2] if len(p) > 2 else 1)

    def final(d):
        p = [int(x) for x in str(d).split("-")]
        if len(p) == 3:
            return datetime.date(*p)
        m = p[1] if len(p) > 1 else 12
        return datetime.date(p[0], m, calendar.monthrange(p[0], m)[1])

    gaps, last, last_s = [], None, None
    acting = [h for h in o.get("holders") or [] if h.get("acting")]
    for h in sorted([h for h in o.get("holders") or [] if not h.get("acting")], key=lambda h: lo(h["from"])):
        if last and (first(h["from"]) - last).days >= 1:
            gaps.append((last_s, str(h["from"]), len(last_s or "") == 10 and len(str(h["from"])) == 10))
        if not h.get("to"):
            last, last_s = datetime.date(9999, 1, 1), None
        elif not last or final(h["to"]) > last:
            last, last_s = final(h["to"]), str(h["to"])
    end = o.get("until") or END
    if last and last.year < 9999 and final(end) > last:
        gaps.append((last_s, str(end), len(last_s or "") == 10 and (final(end) - last).days < 90))
    out = []
    for x, y, sure_vacant in gaps:
        x = a if lo(x) < lo(a) else x
        y = b if lo(y) > lo(b) else y
        if lo(x) >= lo(y):
            continue
        sure = (first(y) - final(x)).days
        acted = any(lo(x) <= lo(h["from"]) < lo(y) for h in acting)
        if sure > 1 or (sure >= 1 and acted):
            out.append((x, y, sure_vacant or acted))
    return out


# ---------------------------------------------------------------- the block

def term_span(i):
    a = TERMS[i][0]
    b = TERMS[i + 1][0] if i + 1 < len(TERMS) else "1974-09-01"
    return a, b


def term_end(b):
    """A term runs to the next one's first day (Jan. 20 to Jan. 20); the last, to Aug. 31, 1974."""
    return "1974-08-31" if b == "1974-09-01" else b


def last_day(b):
    import datetime
    if b == "1974-09-01":
        return "1974-08-31"
    d = datetime.date.fromisoformat(b) - datetime.timedelta(days=1)
    return d.isoformat()


def term_index(day):
    for i, t in enumerate(TERMS):
        if t[0] == day:
            return i
    return None


SECTIONS = [(0, None), (30, "The executive departments"), (500, "Independent establishments and agencies")]


def section_of(u, units):
    """The top-level unit's place: the President and his Office; the departments; the independent agencies."""
    while u.get("under") and u["under"] != "president" and u["under"] in units:
        u = units[u["under"]]
    if u["unit"] == "president":
        return None
    return [lab for o, lab in SECTIONS if u.get("order", 999) >= o][-1]


def path_of(u, units):
    """'Department of Defense › ' for the Department of the Army: the units above, below the President."""
    out = []
    while u.get("under") and u["under"] not in ("president", None) and u["under"] in units:
        u = units[u["under"]]
        out.append(u)
    return out[::-1]


def block(i, units, ptr, href, rid, here=False):
    """The roster for one term: each unit a collapsible table of its offices, their holders, and under each office
    the law that governs it."""
    a, b = term_span(i)
    day, pres, label = TERMS[i]
    rows_total, held = 0, 0
    parts = []
    section = None
    for depth, u in tree(units):
        if not exists(u, a, b):
            continue
        rows = []
        group = None
        for od, o in offices_in_order(u):
            if not exists(o, a, b):
                continue
            hs = [h for h in o.get("holders") or [] if in_term(h, a, b)]
            hs.sort(key=lambda h: lo(h["from"]))
            if o.get("group") != group and o.get("group"):
                group = o["group"]
                rows.append(f'<tr class="st"><th colspan="3">{esc(group)}</th></tr>')
            meta = [esc(RANK[o["rank"]])] if o.get("rank") in RANK else []
            if o.get("appt"):
                meta.append(f'<abbr title="{esc(APPT.get(o["appt"], o["appt"]))}">{esc(o["appt"])}</abbr>')
            if o.get("level") and lo(b) > lo(LEVELS_FROM):
                lv = str(o["level"])
                meta.append(f'<abbr title="Executive Schedule, level {esc(lv)}: {esc(level_rates(lv, a, b))}. '
                            f'{esc(LEVELS.get(lv, "").capitalize())}.">Level {esc(lv)}</abbr>')
            if o.get("from") and lo(o["from"]) > lo(START):
                meta.append(f"from {fmt(o['from'])}")
            if o.get("until") and hi(o["until"]) < lo(b):
                meta.append(f"until {fmt(o['until'])}")
            if od and o.get("under"):
                sup = next((x for x in u.get("offices") or [] if x["id"] == o["under"]), None)
                if sup and sup is not (u.get("offices") or [None])[0]:
                    meta.append(f"under the {esc(title_at(sup, a))}")
            laws = [law_html(x) for x in o.get("law") or [] if in_force(x, a, b)]
            onote = f'<span class="cgn">{to_html(o["n"])}</span>' if o.get("n") else ""
            # one row a holder (or vacancy), each with its own pointers; the office cell spans them
            cells = []
            gaps = [] if o.get("many") else vacancies(o, a, b)
            if not hs and not gaps:
                cells.append(('<span class="exh"><i>No holder recorded.</i></span>', []))
            # an acting officer who began before the term sorts from its first day, under the vacancy he served in
            items = [(max(lo(h["from"]), lo(a)) if h.get("acting") else lo(h["from"]), 1, h) for h in hs] \
                + [(lo(g[0]), 0, g) for g in gaps]
            gap = None
            for _, kind, x in sorted(items, key=lambda t: (t[0], t[1])):
                if kind == 0:
                    gap = x
                    when = span(x[0], term_end(x[1]) if x[1] == b else x[1])
                    gap_label = '<b>Vacant</b>' if x[2] else '<i>No holder recorded</i>'
                    cells.append((f'<span class="exh">{gap_label} <span class="exd">{when}.</span></span>', []))
                    continue
                who, line, pts = holder_html(x, a, b, ptr, href, o)
                inside = x.get("acting") and gap and lo(gap[0]) <= max(lo(x["from"]), lo(a)) < lo(gap[1])
                cells.append((f'<span class="exh{" exin" if inside else ""}">{who} {line}</span>', pts))
            rows_total += 1
            held += bool(hs)
            full = laws or onote
            n = len(cells)
            for k, (cell, pts) in enumerate(cells):
                last = k == n - 1
                cls = "exo" + ("" if last else " exmid") + (" exhl" if full and last else "")
                head = (f'<td rowspan="{n}" class="exof{" exnb" if full else ""}"><span class="ext">{esc(title_at(o, a))}</span>'
                        f'<span class="exm">{" · ".join(meta)}</span></td>') if k == 0 else ""
                pcell = "".join(f'<span class="exp">{p_}</span>' for p_ in pts)
                rid_ = f' id="{rid(i, u["unit"], o["id"])}"' if k == 0 else ""
                rows.append(f'<tr{rid_} class="{cls}">{head}<td>{cell}</td><td>{pcell}</td></tr>')
            if full:
                rows.append('<tr class="exlr"><td colspan="3">' + onote
                            + ('<ul class="exlaw">' + "".join(f"<li>{x}</li>" for x in laws) + "</ul>" if laws else "")
                            + "</td></tr>")
        ulaw = [law_html(x) for x in u.get("law") or [] if in_force(x, a, b)]
        if not rows and not ulaw:
            continue
        sec = section_of(u, units)
        if sec != section and sec:
            parts.append(f'<p class="exsec">{esc(sec)}</p>')
        section = sec
        unote = f'<p class="cgn exun">{to_html(u["n"])}</p>' if u.get("n") else ""
        heads = [h["name"].split(",")[0] for o in (u.get("offices") or [])[:1] for h in o.get("holders") or []
                 if in_term(h, a, b) and not h.get("acting")]
        who = f' <span class="cgsm">{esc(", ".join(dict.fromkeys(heads)))}</span>' if heads and u["unit"] != "president" else ""
        path = "".join(f'<span class="cgsm">{esc(name_at(p, a))} › </span>' for p in path_of(u, units))
        parts.append(f'<details class="cgr exu" id="{rid(i, u["unit"], "")}">'
                     f'<summary>{path}{esc(name_at(u, a))}{who}</summary>'
                     + ('<ul class="exlaw exul">' + "".join(f"<li>{x}</li>" for x in ulaw) + "</ul>" if ulaw else "") + unote
                     + ('<table><colgroup><col class="exc1"><col class="exc2"><col class="exc3"></colgroup>'
                        '<thead><tr><th>Office</th><th>Holders during the term</th><th>In the series</th></tr></thead>'
                        f'<tbody>{"".join(rows)}</tbody></table>' if rows else "") + '</details>')
    out = [f'<div class="cg ex" data-term="{a}">',
           f'<p class="cgh">The Executive Branch, {esc(label)}: {esc(fmt(a))} to {esc(fmt(term_end(b)))}</p>',
           f'<p class="cgs">{rows_total} offices; {held} with a holder recorded. Each office with every holder during the '
           'term (dates of nomination, confirmation, commission, and taking office; of leaving; acting officers), and under '
           'it the law in force during the term that creates it, sets its powers, governs appointment and vacancy, and fixes '
           'its pay. Open a unit for its offices.</p>',
           f'<p class="cgs exkey">{esc(KEY)}{esc(KEY_LEVELS) if lo(b) > lo(LEVELS_FROM) else ""} '
           'Hover over a code for its meaning.</p>',
           '<p class="cgs"><button type="button" class="cgb" onclick="this.closest(\'.ex\').querySelectorAll(\'details\').forEach(d=>d.open=true)">Expand all</button> '
           '<button type="button" class="cgb" onclick="this.closest(\'.ex\').querySelectorAll(\'details\').forEach(d=>d.open=false)">Collapse all</button></p>']
    out += parts
    out.append("</div>")
    return "\n".join(out)


CSS = """<style>
/* The Executive Branch roster (tools/bib/executive.py). The shared block and table rules: templates/roster.css. */
.ex .exsec{font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:1rem 0 .2rem}
details.exu table{font-size:.82rem;margin:.2rem 0 .8rem}
details.exu col.exc1{width:28%}details.exu col.exc2{width:auto}details.exu col.exc3{width:19%}
details.exu td:nth-child(3){font-size:.76rem;overflow-wrap:anywhere}
details.exu tr.exhl td{border-bottom:0}
details.exu tr.exmid td:not(.exof){border-bottom:0;padding-bottom:0}
details.exu td.exof{border-bottom:1px solid var(--rule)}
details.exu tr.exhl td.exof,details.exu td.exof.exnb{border-bottom:0}
.ex .exp{display:block;margin-bottom:.15rem}
.ex .exp a{white-space:nowrap}
details.exu tr.exlr td{padding-top:0}
.ex .ext{font-weight:600}
.ex .exm{display:block;font-size:.72rem;color:var(--muted)}
.ex .exh{display:block;margin-bottom:.3rem}
.ex .exh>b{font-weight:600}
.ex .exh.exin{margin-left:1rem}
.ex .exd{display:block;font-size:.74rem;color:var(--muted);line-height:1.35}
.ex .exs{display:block;font-size:.68rem;color:var(--muted);line-height:1.35;margin-top:.1rem}
.ex .exs a{color:inherit;text-decoration-color:var(--rule)}
.ex .exr{font-weight:400;font-size:.74rem;color:var(--muted)}
.ex .cgn{font-size:.8rem;line-height:1.35}
details.exu tr.exlr .cgn{margin:.1rem 0 .15rem}
.ex ul.exlaw{list-style:none;margin:0;padding:.2rem 0 .1rem;font-size:.74rem;line-height:1.4;color:var(--muted)}
.ex ul.exlaw.exul{margin:.1rem 0 .5rem}
.ex ul.exlaw li{margin:.12rem 0}
.ex .exg{font-size:.66rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--ink)}
.ex .exw{white-space:nowrap}
.ex .exun{margin:.2rem 0 .4rem}
.ex abbr{text-decoration:none;cursor:help}
ol.exauth li{font-size:.85rem;margin:.3rem 0}
ol.exauth .exd{display:block;font-size:.76rem;color:var(--muted)}
</style>"""


# ---------------------------------------------------------------- pages

def rid_for(prefix=""):
    return lambda i, unit, office: f"ex{TERMS[i][0][:4]}{TERMS[i][0][5:7]}-{unit}" + (f"-{office}" if office else "")


def tagged(series):
    """{term start: calendar entry tagged executive:<date>}"""
    out = {}
    for lst in series.lists.values():
        if lst.kind == "calendar":
            for sec, e in lst.entries():
                for t in e.get("tags", []):
                    m = re.match(r"^executive:(\d{4}-\d{2}-\d{2})$", t)
                    if m:
                        out[m.group(1)] = e
    return out


def inject(page, series, linker, mode):
    """Put each tagged calendar entry's term into a built page."""
    units = load()
    if not units:
        return page
    from .congress import Pointers
    ptr = None
    href = (lambda key, eid: f"#{eid}") if mode == "series" else (lambda key, eid: f"{key}.html#{eid}" if key != "cal" else f"#{eid}")
    used = False
    for day, e in tagged(series).items():
        i = term_index(day)
        if i is None:
            continue
        ptr = ptr or Pointers(series, linker)
        blk = block(i, units, ptr, href, rid_for())
        pat = re.compile(r'(<li id="' + re.escape(e["id"]) + r'"[^>]*>.*?)(</li>)', re.S)
        page, n = pat.subn(lambda mm: mm.group(1) + blk + mm.group(2), page, count=1)
        used = used or bool(n)
    if used:
        from . import roster
        page = roster.ensure(page.replace("</body>", CSS + "\n</body>", 1))
    return page


def authorities(units):
    """Every authority cited, once, in order of date: [(authority, [where])]."""
    seen = {}
    for u in units.values():
        for a in u.get("law") or []:
            k = (a.get("act"), a.get("cite"))
            seen.setdefault(k, [a, []])[1].append(u["name"])
        for o in u.get("offices") or []:
            for a in o.get("law") or []:
                k = (a.get("act"), a.get("cite"))
                seen.setdefault(k, [a, []])[1].append(o["title"])
    return sorted(seen.values(), key=lambda x: (lo(x[0].get("date")), x[0].get("act") or ""))


def page(series, linker, template):
    """build/executive.html: every term."""
    units = load()
    if not units:
        return None
    from .congress import Pointers
    ptr = Pointers(series, linker)
    href = lambda key, eid: f"{key}.html#{eid}"
    tag = tagged(series)
    n_off = sum(len(u.get("offices") or []) for u in units.values())
    n_h = sum(len(o.get("holders") or []) for u in units.values() for o in u.get("offices") or [])
    main = ["<h1>The Executive Branch, 1953–1974</h1>",
            '<p class="lede">Every office of the Executive Branch held in the period, from the President and his staff '
            'through the departments, their principal and inferior officers, the military chiefs and commanders, the '
            'independent agencies, and the chiefs of mission abroad; the law that establishes each; and everyone who '
            f'held it, Jan. 20, 1953, to Aug. 31, 1974. {n_off} offices, {n_h} tenures.</p>',
            '<p class="logic">A roster at each inauguration, and at the successions of Nov. 22, 1963, and Aug. 9, 1974, '
            'with every change during the term. Units in the order of the Congressional Directory: the President, the '
            'Vice President, the Executive Office, the departments in the order of their creation, the independent '
            'agencies. Within a unit, each office under the one it reports to.</p>',
            '<p class="logic">Rank, in the terms of Article II, § 2, cl. 2: heads of departments; principal officers, '
            'appointed by the President with the advice and consent of the Senate (PAS); inferior officers, whose '
            'appointment Congress has vested in the President alone (PA) or the heads of departments (HD); employees, '
            'who hold no office in law (VP: the Vice President\'s staff, Senate employees); military officers, assigned to a command or a staff (MIL). XO: ex officio. '
            'DES: designated by the President. Levels: the Executive Schedule of the Federal Executive Salary Act of 1964.</p>',
            '<p class="logic">Dates: nominated, the day the nomination reached the Senate; confirmed; commissioned, the day '
            'the President signed the commission (a recess appointment, during a recess of the Senate); took office, the '
            'oath or entry on duty, or for a chief of mission the presentation of credentials; left, the last day. '
            'Sources: the Office of the Historian\'s Principal Officers and Chiefs of Mission (POCOM) for the Department '
            'of State and the missions; the Congressional Directory for each session (govinfo); the Senate\'s '
            'Executive Journal and the Congressional Record for nominations; department and service histories; the '
            'statutes in the Statutes at Large (govinfo). Each holder\'s sources follow the dates, linked; '
            '<a href="#sources">the sources</a> are listed in full at the end. "Check" marks a detail still to '
            'verify.</p>',
            '<p class="logic">Pointers: the list and section where the holder appears in Part III or as the subject of a '
            'memoir or biography, and the calendar entries that name the holder.</p>',
            '<nav class="toc" aria-label="Contents">\n<h3 id="contents" style="border-top:0;margin-top:1.5rem" data-short="Contents">Contents</h3>\n<ol id="tocList"></ol>\n</nav>']
    rid = rid_for()
    for i, (day, pres, label) in enumerate(TERMS):
        a, b = term_span(i)
        main.append(f'<h2 id="t{day[:4]}{day[5:7]}" data-short="{esc(fmt(day))}">{esc(label)}, {esc(fmt(a))}–{esc(fmt(term_end(b)))}</h2>')
        if day in tag:
            main.append(f'<p class="logic">In the calendar: <a href="cal.html#{tag[day]["id"]}">{esc(tag[day]["when"])}, {day[:4]}</a>.</p>')
        main.append(block(i, units, ptr, href, rid, here=True))
    main.append('<h2 id="authorities" data-short="Authorities">The authorities</h2>')
    main.append('<p class="logic">Every act, reorganization plan, and order cited above, by date, with the units and '
                'offices that cite it.</p><ol class="e exauth">')
    for a, where in authorities(units):
        main.append(f'<li>{esc(fmt(a["date"])) + ". " if a.get("date") else ""}{law_html(a)} '
                    f'<span class="exd">{esc("; ".join(dict.fromkeys(where)))}.</span></li>')
    main.append("</ol>")
    main += executive_sources.section(units)
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", "The Executive Branch, 1953–1974").replace("{{main}}", "\n".join(main))
    from . import roster
    return roster.ensure(pg.replace("</body>", CSS + "\n</body>", 1))


# ---------------------------------------------------------------- check

def problems(series=None):
    out = []
    units = load()
    if not units:
        return out
    keys = set(units) | {"president"}
    for k, u in units.items():
        f = f"executive/{u['_file']}"
        if u["_file"] != f"{k}.yaml":
            out.append((f, f"unit {k!r} should live in executive/{k}.yaml"))
        bad = set(u) - UNIT_KEYS - {"_file"}
        if bad:
            out.append((f, f"unknown unit fields: {', '.join(sorted(bad))}"))
        if k != "president" and (u.get("under") or "president") not in keys:
            out.append((f, f"under {u.get('under')!r}: no such unit"))
        if not u.get("name"):
            out.append((f, "unit needs a name"))
        for d in ("from", "until"):
            if u.get(d) and not DATE_RE.match(str(u[d])):
                out.append((f, f"bad date {d}: {u[d]!r}"))
        out += law_problems(f, u.get("law"))
        ids = set()
        all_ids = {o.get("id") for o in u.get("offices") or []}
        for o in u.get("offices") or []:
            oid = o.get("id")
            w = f"{f} {oid}"
            if not oid or not re.match(r"^[a-z0-9][a-z0-9\-]*$", str(oid)):
                out.append((w, "office needs an id of a-z, 0-9 and '-'"))
            if oid in ids:
                out.append((w, "duplicate office id"))
            ids.add(oid)
            bad = set(o) - OFFICE_KEYS
            if bad:
                out.append((w, f"unknown office fields: {', '.join(sorted(bad))}"))
            if not o.get("title"):
                out.append((w, "office needs a title"))
            if o.get("rank") and o["rank"] not in RANK:
                out.append((w, f"rank {o['rank']!r} not one of {', '.join(RANK)}"))
            if o.get("appt") and o["appt"] not in APPT:
                out.append((w, f"appt {o['appt']!r} not one of {', '.join(APPT)}"))
            sup = o.get("under")
            if sup and sup not in all_ids:
                uu, _, oo = str(sup).partition(".")
                if uu not in units or oo not in {x.get("id") for x in units[uu].get("offices") or []}:
                    out.append((w, f"under {sup!r}: no such office"))
            for d in ("from", "until"):
                if o.get(d) and not DATE_RE.match(str(o[d])):
                    out.append((w, f"bad date {d}: {o[d]!r}"))
            for x in o.get("titles") or []:
                if not x.get("title") or not DATE_RE.match(str(x.get("from") or "")):
                    out.append((w, "titles need title and from"))
            out += law_problems(w, o.get("law"))
            prev = None
            for h in o.get("holders") or []:
                hw = f"{w} {h.get('name')}"
                bad = set(h) - HOLDER_KEYS
                if bad:
                    out.append((hw, f"unknown holder fields: {', '.join(sorted(bad))}"))
                if not h.get("name"):
                    out.append((w, "holder needs a name"))
                if not h.get("from"):
                    out.append((hw, "holder needs 'from' (the day of taking office)"))
                    continue
                for d in ("nominated", "confirmed", "recess", "appointed", "from", "to"):
                    if h.get(d) and bad_date(h[d]):
                        out.append((hw, f"bad date {d}: {h[d]!r}"))
                if h.get("to") and hi(h["to"]) < lo(h["from"]):
                    out.append((hw, "left before taking office"))
                if h.get("nominated") and h.get("confirmed") and hi(h["confirmed"]) < lo(h["nominated"]):
                    out.append((hw, "confirmed before nominated"))
                if h.get("to") and hi(h["to"]) < lo(START):
                    out.append((hw, "left before Jan. 20, 1953: not in the period"))
                if lo(h["from"]) > hi(END):
                    out.append((hw, "took office after Aug. 31, 1974: not in the period"))
                if not o.get("many") and not h.get("acting") and prev and prev.get("to") is None:
                    out.append((hw, f"follows {prev['name']}, who has no 'to'"))
                elif not o.get("many") and not h.get("acting") and prev and lo(prev["to"]) > hi(h["from"]):
                    out.append((hw, f"overlaps {prev['name']} (to {prev['to']}); acting, or 'many: true'?"))
                if prev and lo(h["from"]) < lo(prev["from"]):
                    out.append((hw, "holders out of order (by 'from')"))
                if not h.get("acting"):
                    prev = h
    return out


def law_problems(where, laws):
    out = []
    for a in laws or []:
        if not isinstance(a, dict):
            out.append((where, f"authority is not a mapping: {str(a)[:60]}"))
            continue
        bad = set(a) - LAW_KEYS
        if bad:
            out.append((where, f"unknown authority fields: {', '.join(sorted(bad))}"))
        if not a.get("act"):
            out.append((where, "authority needs 'act'"))
        if not (a.get("cite") or a.get("url") or a.get("usc")):
            out.append((where, f"authority {a.get('act')!r} needs a cite, usc, or url"))
        if a.get("date") and not DATE_RE.match(str(a["date"])):
            out.append((where, f"authority {a.get('act')!r}: bad date {a['date']!r}"))
        if not a.get("date"):
            out.append((where, f"authority {a.get('act')!r} needs a date"))
        for d in ("effective", "until"):
            if a.get(d) and not DATE_RE.match(str(a[d])):
                out.append((where, f"authority {a.get('act')!r}: bad {d} {a[d]!r}"))
        for t in store.as_list(a.get("tags")):
            if t not in TAGS:
                out.append((where, f"authority {a.get('act')!r}: tag {t!r} not one of {', '.join(TAGS)}"))
    return out


# ---------------------------------------------------------------- coverage

def holders_by_name(units):
    """fold(surname) -> [(given, unit, office, holder)]"""
    out = defaultdict(list)
    for u in units.values():
        for o in u.get("offices") or []:
            for h in o.get("holders") or []:
                sur, _, given = h["name"].partition(",")
                out[store.fold(sur.strip())].append((given.strip(), u, o, h))
    return out
