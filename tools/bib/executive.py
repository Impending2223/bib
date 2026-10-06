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
      appt: PAS | PA | HD | XO | DES | MIL | CAREER | ELECTED   (see APPT)
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
      src: [POCOM, CDIR 1961-04, https://...]

An authority:

    - act: National Security Act of 1947      # the act, plan, or order, by its name or date
      date: '1947-07-26'                      # enacted, or in effect for a plan; signed for an order
      cite: 'ch. 343, § 101, 61 Stat. 495, 496'   # Statutes at Large: the page the act begins on, then the pin
      usc: '50 U.S.C. § 402 (1958)'           # as codified in the period's edition, where it was
      does: Establishes the Council.          # one clipped line
      url: https://...                        # where the cite alone does not link (orders, plans)

Dates: 'YYYY-MM-DD', or 'YYYY-MM' or 'YYYY' where the day is not known.

STYLE:
 1. Each term shows every office that existed during it, the holder at its start ("Vacant" where none, with
    the acting officer) and every change through its end. Holders who left on or before the first day of the
    term show only in the term before.
 2. A holder's line: the dates of nomination, confirmation, commission (or recess commission), and taking
    office, the year once per run; then the date of leaving and how. Acting officers say so, with their span.
 3. Authorities link to the Statutes at Large on govinfo by volume and the page the act begins on.
"""
import os
import re
from collections import defaultdict

from . import store
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
        "XO": "ex officio: held by virtue of another office",
        "DES": "designated by the President from among other officers",
        "MIL": "a military officer assigned or detailed, with the advice and consent of the Senate to the grade",
        "CAREER": "the career service",
        "ELECTED": "elected"}
UNIT_KEYS = {"unit", "name", "names", "under", "order", "from", "until", "law", "n", "offices"}
OFFICE_KEYS = {"id", "title", "titles", "rank", "appt", "under", "group", "level", "many", "from", "until",
               "law", "n", "holders"}
HOLDER_KEYS = {"name", "given", "rank", "title", "acting", "nominated", "confirmed", "recess", "appointed", "from", "to",
               "out", "n", "src"}
LAW_KEYS = {"act", "date", "cite", "usc", "does", "url"}
DATE_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
STAT_RE = re.compile(r"\b(\d+) Stat\. (\d+)")


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


# ---------------------------------------------------------------- data

def load():
    """{unit key: unit}, every file in executive/."""
    out = {}
    if not os.path.isdir(DIR):
        return out
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
    """Did the holder serve during [a, b)? One who left on the term's first day belongs to the term before."""
    return lo(h["from"]) < lo(b) and (not h.get("to") or lo(h["to"]) > lo(a))


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

def law_html(a):
    """'National Security Act of 1947, ch. 343, § 101, 61 Stat. 495, 496; 50 U.S.C. § 402 (1958).'"""
    cite = a.get("cite") or ""
    url = a.get("url")
    m = STAT_RE.search(cite)
    if not url and m:
        url = f"https://www.govinfo.gov/content/pkg/STATUTE-{m.group(1)}/pdf/STATUTE-{m.group(1)}-Pg{m.group(2)}.pdf"
    act = esc(a.get("act") or "")
    head = act + (f", {esc(cite)}" if cite else "")
    if url:
        head = f'<a href="{esc(url)}">{head}</a>'
    t = head + (f"; {esc(a['usc'])}" if a.get("usc") else "") + "."
    if a.get("does"):
        t += " " + to_html(a["does"])
    return t


def in_force(a, b):
    """Shown with a term: an authority dated before the term's end."""
    return not a.get("date") or lo(a["date"]) < lo(b)


# ---------------------------------------------------------------- holders

def holder_line(h, a, b, o=None):
    """The holder's dates, as one clipped line (HTML)."""
    pairs = []
    if h.get("acting"):
        span = fmt(h["from"])
        if h.get("to"):
            span += "–" + fmt(h["to"])
        t = f"Acting, {span}."
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


def holder_html(h, a, b, ptr, href, o=None):
    who = esc(h["name"])
    if h.get("rank"):
        who += f' <span class="exr">{esc(h["rank"])}</span>'
    if h.get("title"):
        who += f' <span class="exr">({esc(h["title"])})</span>'
    line = f'<span class="exd">{holder_line(h, a, b, o)}</span>'
    note = f'<span class="cgn">{to_html(h["n"])}</span>' if h.get("n") else ""
    pts = ptr.lines(h["name"], href) if ptr else []
    return who, line + note, pts


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


def block(i, units, ptr, href, rid, here=False):
    """The roster for one term: each unit a collapsible table of its offices and their holders."""
    a, b = term_span(i)
    day, pres, label = TERMS[i]
    rows_total, held = 0, 0
    parts = []
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
            title = esc(title_at(o, a))
            meta = []
            if o.get("appt"):
                meta.append(f'<abbr title="{esc(APPT.get(o["appt"], o["appt"]))}">{esc(o["appt"])}</abbr>')
            if o.get("level"):
                meta.append(f"Level {esc(o['level'])}")
            if o.get("from") and lo(o["from"]) > lo(START):
                meta.append(f"from {fmt(o['from'])}")
            if o.get("until") and hi(o["until"]) < lo(b):
                meta.append(f"until {fmt(o['until'])}")
            laws = "".join(f'<span class="exl">{law_html(x)}</span>' for x in o.get("law") or [] if in_force(x, b))
            onote = f'<span class="cgn">{to_html(o["n"])}</span>' if o.get("n") else ""
            cells = []
            pts_all = []
            at_start = [h for h in hs if lo(h["from"]) <= lo(a)]
            if hs and not at_start and lo(o.get("from") or START) <= lo(a):
                cells.append('<span class="exh"><i>Vacant</i> on the first day of the term.</span>')
            if not hs:
                cells.append('<span class="exh"><i>No holder recorded</i>.</span>' if not o.get("many") else
                             '<span class="exh"><i>None recorded</i>.</span>')
            for h in hs:
                who, line, pts = holder_html(h, a, b, ptr, href, o)
                cells.append(f'<span class="exh{" exa" if h.get("acting") else ""}"><b>{who}</b> {line}</span>')
                for p in pts:
                    if p not in pts_all:
                        pts_all.append(p)
            rows_total += 1
            held += bool(hs)
            rk = f' <span class="exk">{esc(RANK.get(o.get("rank"), ""))}</span>' if o.get("rank") else ""
            rows.append(f'<tr id="{rid(i, u["unit"], o["id"])}" class="d{min(od, 3)}"><td><span class="ext">{title}</span>{rk}'
                        f'<span class="exm">{" · ".join(meta)}</span>{laws}{onote}</td>'
                        f'<td>{"".join(cells)}</td><td>{"; ".join(pts_all)}</td></tr>')
        if not rows and not u.get("law"):
            continue
        ulaw = "".join(f'<li>{law_html(x)}</li>' for x in u.get("law") or [] if in_force(x, b))
        unote = f'<p class="exun">{to_html(u["n"])}</p>' if u.get("n") else ""
        heads = [h["name"].split(",")[0] for o in (u.get("offices") or [])[:1] for h in o.get("holders") or []
                 if in_term(h, a, b) and not h.get("acting")]
        who = f' <span class="exs">{esc(", ".join(dict.fromkeys(heads)))}</span>' if heads and u["unit"] != "president" else ""
        parts.append(f'<details class="exu" style="margin-left:{min(depth, 3) * .9:.1f}rem" id="{rid(i, u["unit"], "")}">'
                     f'<summary>{esc(name_at(u, a))}{who}</summary>'
                     + (f'<ul class="exlaw">{ulaw}</ul>' if ulaw else "") + unote
                     + ('<table><colgroup><col class="c1"><col class="c2"><col class="c3"></colgroup>'
                        '<thead><tr><th>Office and authority</th><th>Holders during the term</th><th>In the series</th></tr></thead>'
                        f'<tbody>{"".join(rows)}</tbody></table>' if rows else "") + '</details>')
    out = [f'<div class="ex" data-term="{a}">',
           f'<p class="cgh">The Executive Branch, {esc(label)}: {esc(fmt(a))} to {esc(fmt(term_end(b)))}</p>',
           f'<p class="exsum">{rows_total} offices; {held} with a holder recorded. Each office with its authority in law '
           'and every holder during the term: dates of nomination, confirmation, commission, and taking office; of '
           'leaving; acting officers. Open a unit for its offices.</p>',
           '<p class="exsum"><button type="button" class="exall" onclick="this.closest(\'.ex\').querySelectorAll(\'details\').forEach(d=>d.open=true)">Expand all</button> '
           '<button type="button" class="exall" onclick="this.closest(\'.ex\').querySelectorAll(\'details\').forEach(d=>d.open=false)">Collapse all</button></p>']
    out += parts
    out.append("</div>")
    return "\n".join(out)


CSS = """<style>
/* The Executive Branch roster: one block a term (tools/bib/executive.py) */
.ex{margin:1rem 0 .5rem;font-family:var(--sans)}
.ex .cgh{font-weight:700;font-size:.95rem;margin:.2rem 0 .4rem}
.ex .exsum{font-size:.82rem;line-height:1.4;color:var(--muted);margin:.15rem 0 .5rem}
.ex button.exall{font:600 .72rem/1 var(--sans);padding:.3rem .5rem;border:1px solid var(--rule);border-radius:5px;background:var(--panel);color:var(--muted);cursor:pointer}
details.exu{margin:.2rem 0;font-size:.85rem}
details.exu>summary{cursor:pointer;font-weight:600;padding:.3rem 0}
details.exu>summary .exs{font-weight:400;color:var(--muted)}
details.exu table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:.82rem;margin:.2rem 0 .8rem}
details.exu col.c1{width:36%}details.exu col.c2{width:auto}details.exu col.c3{width:17%}
details.exu th,details.exu td{text-align:left;vertical-align:top;padding:.3rem .4rem .3rem 0;border-bottom:1px solid var(--rule)}
details.exu thead th{font-size:.72rem;font-weight:600;color:var(--muted)}
details.exu tr.st th{padding-top:.8rem;font-size:.8rem;border-bottom:1px solid var(--ink)}
details.exu td:nth-child(3){font-size:.76rem;overflow-wrap:anywhere}
details.exu tr.d1 td:first-child{padding-left:.9rem}details.exu tr.d2 td:first-child{padding-left:1.8rem}details.exu tr.d3 td:first-child{padding-left:2.7rem}
details.exu tr:target td{background:var(--hl-bg);color:var(--hl-ink)}
.ex .ext{font-weight:600}
.ex .exk,.ex .exm{display:block;font-size:.72rem;color:var(--muted)}
.ex .exl{display:block;font-size:.72rem;line-height:1.35;color:var(--muted);margin-top:.15rem}
.ex .exh{display:block;margin-bottom:.3rem}
.ex .exh>b{font-weight:600}
.ex .exh.exa>b{font-weight:400;font-style:italic}
.ex .exd{display:block;font-size:.74rem;color:var(--muted);line-height:1.35}
.ex .exr{font-weight:400;font-size:.74rem;color:var(--muted)}
.ex .cgn{display:block;font-family:var(--serif);font-size:.8rem;line-height:1.35;color:var(--note)}
.ex ul.exlaw{margin:.1rem 0 .5rem 1.1rem;padding:0;font-size:.74rem;line-height:1.4;color:var(--muted)}
.ex ul.exlaw li{margin:.1rem 0}
.ex .exun{font-size:.8rem;color:var(--note);margin:.2rem 0 .4rem;font-family:var(--serif)}
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
        page = page.replace("</body>", CSS + "\n</body>", 1)
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
            'who hold no office in law; military officers, assigned to a command or a staff (MIL). XO: ex officio. '
            'DES: designated by the President. Levels: the Executive Schedule of the Federal Executive Salary Act of 1964.</p>',
            '<p class="logic">Dates: nominated, the day the nomination reached the Senate; confirmed; commissioned, the day '
            'the President signed the commission (a recess appointment, during a recess of the Senate); took office, the '
            'oath or entry on duty, or for a chief of mission the presentation of credentials; left, the last day. '
            'Sources: the Office of the Historian\'s Principal Officers and Chiefs of Mission (POCOM) for the Department '
            'of State and the missions; the Congressional Directory for each session (govinfo); the Senate\'s '
            'Executive Journal and the Congressional Record for nominations; department and service histories; the '
            'statutes in the Statutes at Large (govinfo). "Check" marks a detail still to verify.</p>',
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
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", "The Executive Branch, 1953–1974").replace("{{main}}", "\n".join(main))
    return pg.replace("</body>", CSS + "\n</body>", 1)


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
                    if h.get(d) and not DATE_RE.match(str(h[d])):
                        out.append((hw, f"bad date {d}: {h[d]!r}"))
                if h.get("to") and hi(h["to"]) < lo(h["from"]):
                    out.append((hw, "left before taking office"))
                if h.get("nominated") and h.get("confirmed") and hi(h["confirmed"]) < lo(h["nominated"]):
                    out.append((hw, "confirmed before nominated"))
                if h.get("to") and lo(h["to"]) < lo(START):
                    out.append((hw, "left before Jan. 20, 1953: not in the period"))
                if lo(h["from"]) > hi(END):
                    out.append((hw, "took office after Aug. 31, 1974: not in the period"))
                if not o.get("many") and not h.get("acting") and prev and prev.get("to") is None:
                    out.append((hw, f"follows {prev['name']}, who has no 'to'"))
                elif not o.get("many") and not h.get("acting") and prev and hi(prev["to"]) > lo(h["from"]) and \
                        lo(prev["to"]) > lo(h["from"]):
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
