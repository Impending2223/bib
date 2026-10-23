"""The committees' meetings, day by day: the Daily Digest's "Committee Meetings" (tools/daybook/make_committees.py),
a fourth list in each calendar day's documents, and "Testimony before Congress" in the Names entries. (The
committees' members and leaders at each opening are another module's: tools/bib/committee_rosters.py.)

    daybook/committees/<YYYY-MM>.yaml   one row a meeting (generated; the fields: the script's STYLE 3)
    daybook/committees/volumes.yaml     the Digest volumes read, their PDF pages against the printed folios

STYLE:
 1. A day's list, "Committees", after APP, FRUS and the recordings, closed with them: one line a meeting, in the
    Digest's order (the Senate's, the House's, the joint committees'): the committee, by chamber and the Directory's
    name ("Senate Foreign Relations", "House Ways and Means", "Joint Committee on Atomic Energy", "Conferees"), its
    subcommittee where the Digest names one; the Digest's subject heading, as printed, in small capitals; the
    measures; "executive session" where the Digest says so; the witnesses, by name as printed (a Member as the Digest
    writes him, "Senator Pell"), the office on hover; then, grey, the Digest's page ("Digest D3"), linked to the PDF
    at that page, and the day hearings continue, linked to that day. Nothing abstracted: the Digest's paragraph is in
    the data, not the line.
 2. A witness is linked to his name entry only where one person fits (witness_person): a Member by his title and
    surname (and State, "Andrews of North Dakota") among those the Directory seats in that chamber on that day, or
    the Congress roster at the last opening holds; an officer by surname (and given names, where printed) among the
    Executive roster's holders on that day whose office shares a telling word with the Digest's ("Secretary of
    Agriculture Freeman"); anyone else by name (person_named in tools/bib/lives.py) where his offices or roles share
    a telling word with the Digest's office. A name alike in surname alone, or an office that agrees with nothing
    known of him, is not linked.
 3. Names: "Testimony before Congress", one line a meeting, by date: the date linked to the calendar's day, the
    committee and subcommittee, the subject heading in small capitals, the measures, the Digest's page; only the
    witnesses linked by STYLE 2.
 4. Links (both lists): the committee to its table on congress.html in the Congress of the day, where the committee
    list holds its code (the standing committees by Nelson's code, the select, special and joint by the code the
    generator makes: committee_more.link_for); the subcommittee to its row, where that Congress's list holds it
    (the 87th and 88th; sub_for), the name as the OCR read it on hover where the generator put it whole; a measure
    whose course congress/bills.yaml gives, in that bill's Congress, to the entry that carries the course (its
    signing).
"""
import datetime
import glob
import html
import os
import re

from . import store

DIR = os.path.join(store.ROOT, "daybook", "committees")
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
CHAMBER = {"S": "Senate", "H": "House", "J": ""}
MEMBER = {"Senator": "s", "Senators": "s", "Representative": "h", "Representatives": "h", "Congressman": "h",
          "Congressmen": "h", "Delegate": "h", "Resident Commissioner": "h"}
_cache = {}


def esc(t):
    return html.escape(str(t), quote=True)


def fmt(d, year=True):
    d = datetime.date.fromisoformat(str(d))
    return f"{MON[d.month - 1]} {d.day}" + (f", {d.year}" if year else "")


def load():
    """Every meeting, by date ({iso: [row]}), in the Digest's order."""
    if "by_day" not in _cache:
        by = {}
        for f in sorted(glob.glob(os.path.join(DIR, "[0-9][0-9][0-9][0-9]-[0-9][0-9].yaml"))):
            try:                           # a month being written by the generator: skipped this run
                d = store.load_yaml(f) or {}
            except Exception:
                continue
            for x in d.get("docs", []):
                by.setdefault(str(x["date"]), []).append(x)
        _cache["by_day"] = by
    return _cache["by_day"]


def volumes():
    p = os.path.join(DIR, "volumes.yaml")
    return (store.load_yaml(p) or {}).get("volumes", []) if os.path.exists(p) else []


def for_day(iso):
    return load().get(iso, [])


def committee_label(x):
    """'Senate Foreign Relations'; 'Joint Committee on Atomic Energy'; 'Senate Special Committee on Aging'."""
    n = x["name"]
    if x["ch"] == "J":
        return n
    return f'{CHAMBER[x["ch"]]} {n}'


# ---------------------------------------------------------------- who the witness is (STYLE 2)

def words(t):
    from .lives import STOP, fold
    return set(re.findall(r"[a-z]{4,}", fold(t or "").lower())) - STOP - {"former", "acting", "with", "from"}


def rosters():
    """[(opened, the next opening, roster)] for the Congresses at their openings (congress/<NN>.yaml)."""
    if "rosters" not in _cache:
        rs = [store.load_yaml(f) or {} for f in sorted(glob.glob(os.path.join(store.ROOT, "congress", "[0-9][0-9].yaml")))]
        rs = [d for d in rs if d.get("opened")]
        _cache["rosters"] = [(str(d["opened"]), str(rs[i + 1]["opened"]) if i + 1 < len(rs) else "9999", d)
                             for i, d in enumerate(rs)]
    return _cache["rosters"]


def members_on(day, ch, sur, state=None):
    """The names of the men of the surname seated in the chamber on the day (STYLE 2): the Directory's service spans
    (lives.bd_service), and the Congress roster at the last opening."""
    from . import lives as L
    from .congress import STATE
    out = set()
    st = None
    if state:
        st = next((k for k, v in STATE.items() if L.fold(v).lower() == L.fold(state).lower()), None)
        if not st:
            return set()
    for e, given, seats, spans, wins in L.bd_service().get(L.fold(sur), []):
        if not any(c == ch and (st is None or s == st) for c, s in seats):
            continue
        if any(a <= day <= b for a, b in spans):
            m = re.match(r"([^,(]+), ([^(,]+)", e["name"])
            s_ = m.group(1).strip()
            out.add(f"{s_.title() if s_.isupper() else s_}, {given}")
    for opened, until, d in rosters():
        if not (opened <= day < until):
            continue
        for r in d.get("senate" if ch == "s" else "house") or []:
            if r.get("name") and L.fold(L.split_name(r["name"])[0]) == L.fold(sur) and (st is None or r["st"] == st):
                out.add(r["name"])
    return out


def witness_person(series, w, day):
    """The name an entry is filed under, for a witness as the Digest prints him, where one person fits (STYLE 2)."""
    key = (w.get("title"), w["name"], w.get("office"), day)
    memo = _cache.setdefault("who", {})
    if key not in memo:
        memo[key] = _witness(series, w, day)
    return memo[key]


def _witness(series, w, day):
    from . import lives as L
    from . import executive as X
    title, name, office = w.get("title") or "", w["name"], w.get("office") or ""
    name = re.sub(r"[~|<>{}¢]", "", name).strip()
    if not re.fullmatch(r"[A-Z][\w'’.,\- ]+", name):
        return None
    ch = MEMBER.get(title)
    if ch:
        m = re.match(r"^(.+?)(?: of ([A-Z][\w.]+(?: [A-Z][\w.]+)?))?$", name)
        nm, state = m.group(1), m.group(2)
        parts = nm.split()
        sur, given = parts[-1], " ".join(parts[:-1])
        people = set()
        for n in members_on(day, ch, sur, state):
            s_, g_ = L.split_name(n)
            if given and not L.same_person(sur, given, s_, g_):
                continue
            p = L.person_named(series, n)
            if p:
                people.add(p)
        return people.pop() if len(people) == 1 else None
    # surname and given names as printed: 'Robert S. McNamara', 'Wallace M. Greene, Jr.'
    suf = ""
    m = re.search(r",\s*(Jr\.|Sr\.|II|III|IV)$", name)
    if m:
        suf, name = m.group(1), name[:m.start()]
    parts = name.split()
    if not parts:
        return None
    sur, given = parts[-1], " ".join(parts[:-1])
    want = words(f"{title} {office}")
    if not want:
        return None
    # the Executive roster: the surname, the given names where printed, in office on the day, the office agreeing
    people = set()
    for u, o, h in L.holders_of(sur):
        a, b = X.lo(h.get("from") or h.get("seen")), X.hi(h.get("to") or h.get("last") or "9999")
        if not (a <= day <= b):
            continue
        hs, hg = L.split_name(h["name"])
        if given and not L.same_person(sur, given, hs, hg):
            continue
        if words(f"{X.title_at(o, day)} {h.get('title') or ''} {X.name_at(u, day)}") & want:
            p = L.person_named(series, h["name"])
            if p:
                people.add(p)
    if len(people) == 1:
        return people.pop()
    if people or not given:
        return None
    # anyone else by name, his offices and roles agreeing with the Digest's
    p = L.person_named(series, f"{sur}, {given}" + (f", {suf}" if suf else ""))
    if not p:
        return None
    ent = next((x for x in L.everyone(series) if x["name"] == p), None)
    names = (ent or {}).get("names") or {p}
    known = L.person_words(sur, given, names, L.part3_roles(series, names))
    known |= L.role_words(L.key_of(p))
    return p if known & want else None


# ---------------------------------------------------------------- the day's list (STYLE 1)

def witness_html(series, w, day):
    shown = esc(f'{w["title"]} {w["name"]}' if w.get("title") in MEMBER else w["name"])
    hover = ", ".join(x for x in (w.get("title") if w.get("title") not in MEMBER else "", w.get("office")) if x)
    who = witness_person(series, w, day) if series is not None else None
    if who:
        from . import namelinks
        shown = namelinks.a(series, who, shown)
    return f'<span title="{esc(hover)}">{shown}</span>' if hover else shown


def head_html(x, site=""):
    """The committee and subcommittee, each linked to its table on congress.html where the committee list holds it
    (STYLE 4; committee_more.link_for, sub_for)."""
    from . import committee_more as cm
    a = cm.link_for(x)
    head = esc(committee_label(x))
    if a:
        head = f'<a class="cmk" href="{esc(site)}congress.html#{esc(a)}">{head}</a>'
    if x.get("sub"):
        b = cm.sub_for(x)
        sub = esc(x["sub"])
        title = f' title="{esc(x["sub_printed"])}"' if x.get("sub_printed") else ""
        head += ", " + (f'<a class="cmk" href="{esc(site)}congress.html#{esc(b)}"{title}>{sub}</a>' if b else
                        (f'<span{title}>{sub}</span>' if title else sub))
    return head


def bills_html(x, series, site=None):
    """The measures, a bill whose course congress/bills.yaml gives linked to its signing entry (STYLE 4)."""
    if not x.get("bills"):
        return ""
    if "bills" not in _cache:
        from . import bills as B
        from .committee_more import congress_on
        tagged = B.tagged(series) if series is not None else {}
        _cache["bills"] = {(b["bill"], int(b["congress"])): (tagged.get(k), b["title"])
                           for k, b in B.load().items() if tagged.get(k)}
    from .committee_more import congress_on
    c = congress_on(x["date"])
    out = []
    for b in x["bills"]:
        hit = _cache["bills"].get((b, c))
        if hit:
            pre = "#" if site is None else f"{site}cal.html#"
            out.append(f'<a href="{esc(pre + hit[0])}" title="{esc(hit[1])}: its course">{esc(b)}</a>')
        else:
            out.append(esc(b))
    return ", ".join(out)


def line_html(x, series, link_next=True):
    """One meeting (STYLE 1)."""
    head = head_html(x)
    bits = []
    if x.get("heading"):
        bits.append(f'<span class="cmh">{esc(x["heading"])}</span>')
    if x.get("bills"):
        bits.append(bills_html(x, series))
    if x.get("exec"):
        bits.append("executive session")
    body = ", ".join(bits)
    ws = [witness_html(series, w, str(x["date"])) for w in x.get("witnesses", [])]
    if ws:
        body += ("; " if body else "") + ", ".join(ws)
    tail = [f'<a class="src" href="{esc(x["url"])}">Digest {esc(x["page"])}</a>']
    if x.get("next") and link_next:
        nx = str(x["next"])
        tail.append(f'<span class="src">hearings continue <a href="#d{esc(nx)}">'
                    f'{esc(fmt(nx, nx[:4] != str(x["date"])[:4]))}</a></span>')
    return f'<li><span class="au">{head}</span>{": " + body if body else ""} {" ".join(tail)}</li>'


def list_html(rows, series):
    return '<ol class="dd fr cm">' + "".join(line_html(x, series) for x in rows) + "</ol>"


STYLE = """<style>
ol.dd.cm .cmh{font-variant:small-caps;text-transform:lowercase;letter-spacing:.02em}
ol.dd.cm a.src{color:var(--muted);text-decoration-color:var(--rule)}
ol.dd.cm .src a{color:var(--muted);text-decoration-color:var(--rule)}
ol.dd.cm a.cmk{color:inherit;text-decoration-color:var(--rule)}
</style>"""


# ---------------------------------------------------------------- Names (STYLE 3)

def testimony(series):
    """{the name an entry is filed under: [(row, witness)]}, the sure matches only."""
    if "testimony" not in _cache:
        out = {}
        for day, rows in sorted(load().items()):
            for x in rows:
                for w in x.get("witnesses", []):
                    who = witness_person(series, w, day)
                    if who:
                        out.setdefault(who, []).append((x, w))
        _cache["testimony"] = out
    return _cache["testimony"]


def testimony_list(series, name, site=""):
    """The items of "Testimony before Congress" (STYLE 3)."""
    items = []
    for x, w in testimony(series).get(name, []):
        bits = [head_html(x, site)]
        if x.get("heading"):
            bits.append(f'<span class="cmh">{esc(x["heading"])}</span>')
        if x.get("bills"):
            bits.append(bills_html(x, series, site))
        day = f'<a href="{esc(site)}cal.html#d{esc(x["date"])}">{esc(fmt(x["date"]))}</a>'
        items.append(f'{day}: {", ".join(bits)}. <span class="lvc"><a href="{esc(x["url"])}">'
                     f'Digest {esc(x["page"])}</a></span>')
    return items


# ---------------------------------------------------------------- check

def problems():
    """For ./bib check: dates out of the calendar's span or not ISO, a row without its page or link, a duplicate key,
    a 'next' day not after the meeting's, a volume whose runs do not cover its pages."""
    out, seen = [], set()
    lo_, hi_ = "1960-01-06", "1969-01-20"
    for day, rows in load().items():
        for x in rows:
            k = x.get("key")
            if k in seen:
                out.append((k, "committees: duplicate key"))
            seen.add(k)
            try:
                datetime.date.fromisoformat(str(x["date"]))
            except Exception:
                out.append((k, f"committees: bad date {x.get('date')!r}"))
                continue
            if not (lo_ <= str(x["date"]) <= hi_):
                out.append((k, f"committees: {x['date']} outside the calendar's span"))
            if not re.fullmatch(r"D\d+", str(x.get("page") or "")) or not x.get("pdf") or \
                    not re.search(r"\.pdf#page=\d+$", str(x.get("url") or "")):
                out.append((k, "committees: no Digest page or link"))
            if x.get("next") and str(x["next"]) <= str(x["date"]):
                out.append((k, f"committees: hearings continue {x['next']}, not after the meeting"))
            if x.get("ch") not in ("S", "H", "J") or not x.get("name"):
                out.append((k, "committees: no chamber or committee"))
    for v in volumes():
        covered = sum(r["to"] - r["from"] + 1 for r in v.get("runs", []))
        if covered != v.get("pages"):
            out.append((f"volumes.yaml {v.get('year')}", "committees: the folio runs do not cover the volume's pages"))
    return out
