"""A bill's course in the calendar: congress/bills.yaml (kept by hand from the bound Record's History of Bills and
Voteview). The calendar entries tagged bill:<key> carry the bill's table (STYLE 7).

STYLE
 1. One row a step, in the order of the Record: the date (a span "Jan. 30–Feb. 7"; linked to the calendar entry that
    tells the step, where one does), the chamber, the step in the series' prose, the roll calls, the Record's page.
    Dates without the year: a row across gives the year where it changes, with the Record's volume ("1964 · 110 Cong.
    Rec."); a span into another year keeps its end's year.
 2. Roll calls as the calendar writes them: the count linked to Voteview, "324–67", what the vote was on before it
    where a day has more than one, a line each ("recommittal 199–226" / "passage 271–155"). A step with no roll call
    leaves the cell empty: the History of Bills does not say "voice vote", so neither does the table.
 3. The Record: the page as the History of Bills prints it, alone, linked to the day's granule of that chamber's
    proceedings on govinfo, the full cite on hover ("111 Cong. Rec. 5798 (House, Mar. 24, 1965)"); a step dated by
    its granule and no page, "day", linked the same. A step the History misprints says so in its note (shown under
    the table, its date in full).
 4. The last row: approved, the Statutes cite linked to govinfo, the public law. The sources under the table: the
    History of Bills, by year, linked; Voteview.
 5. A step the History does not give (the message that asked for the bill, a run of roll calls on amendments) is
    dated by its own record and carries no page; a run of roll calls on amendments over several days is one row, the
    first and last linked. A bill passed in lieu of another (S. 2642 for H.R. 11377; S. 1564 for H.R. 6400; H.J. Res.
    1145 for S.J. Res. 189) keeps the other bill's steps, named in the step. The pages turn to days by the bound
    Record's granules (tools/congress/make_record_pages.py).
 6. One title (the owner, Nov. 4, 2026: "Drop ': its course'"; "where small caps title is used, keep the small caps
    title alone"): the contents' small capitals (tools/bib/contents.py), then a muted line, the bill and its Congress
    ("H.R. 6675, 89th Cong."). The chamber column unheaded, "H" or "S" (the name on hover), the President's rows
    empty, as narrow as its letter. The table fits 400px without sideways scrolling (the owner, the same day): no
    minimum width, the dates and the pages short, the step and the roll calls wrapping.
 7. Where (the owner, Nov. 4, 2026): under the entry of the bill's first introduction in either chamber, and on each
    later year's page of the calendar its course runs into, under that year's first entry concerning the bill in
    Congress; never twice on a page. The placements are the entries tagged bill:<key>, chosen by hand (the first
    entry of a year concerning the bill is a reading, not a rule); `check` holds them: the first the introduction's
    (the first step "introduced", its `entry` the same), one a part (calsplit) from the introduction's to the last
    step's, no other. Where no entry told the introduction, one was made of the table's own step and Record cite
    (Nov. 4, 2026). The first placement's anchor is tb-bill-<key>, a later one's tb-bill-<key>-y<year>, so the reader,
    which holds every year, has each once.
"""
import os
import re

from . import contents, store

PATH = os.path.join(store.ROOT, "congress", "bills.yaml")
_C = {}
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
REC = "https://www.govinfo.gov/content/pkg/{pkg}/pdf/{g}.pdf"
STAT = "https://www.govinfo.gov/content/pkg/STATUTE-{vol}/pdf/{granule}.pdf"
VV = "https://voteview.com/rollcall/R{ch}{cong:03d}{num:04d}"
VOL = {1960: 106, 1961: 107, 1962: 108, 1963: 109, 1964: 110, 1965: 111, 1966: 112, 1967: 113, 1968: 114}
STYLE = """<style id="blstyle">
.bl{margin:0 0 .5rem;font-family:var(--sans)}
.bl .blb{text-align:center;color:var(--muted);font-size:.78rem;margin:-.2rem 0 .4rem}
.bl .blw{overflow-x:auto;-webkit-overflow-scrolling:touch}
.bl table{border-collapse:collapse;width:100%;font-size:.78rem;line-height:1.35;font-variant-numeric:tabular-nums}
.bl th,.bl td{text-align:left;vertical-align:top;padding:.2rem .4rem .2rem 0;border-bottom:1px solid var(--rule)}
.bl thead th{font-weight:600;color:var(--muted);font-size:.74rem}
.bl tr.bly th{font-weight:700;padding-top:.45rem}
.bl tr.bly span{font-weight:400;color:var(--muted)}
.bl td.blc{width:1ch;text-align:center;padding-right:.3rem}
.bl td.blv a,.bl td.blr{white-space:nowrap}
.bl td.blr,.bl th.blr{text-align:right;padding-right:0}
.bl .bln{font-size:.78rem;line-height:1.45;color:var(--note);margin:.3rem 0}
.bl .blsrc{font-size:.78rem;color:var(--muted);line-height:1.4;margin:.3rem 0}
@media (max-width:520px){.bl table{font-size:.74rem}.bl th,.bl td{padding-right:.3rem}}
</style>"""
CH = {"House": ("H", "House"), "Senate": ("S", "Senate")}


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def load():
    if "d" not in _C:
        _C["d"] = (store.load_yaml(PATH) if os.path.exists(PATH) else None) or {}
    return _C["d"].get("bills") or {}


def date(iso, until=None):
    """Full, with the year: "Mar. 24, 1965" (the notes)."""
    y, m, d = iso.split("-")
    s = f"{MON[int(m) - 1]} {int(d)}"
    if until:
        y2, m2, d2 = until.split("-")
        s += "–" + (f"{int(d2)}" if m2 == m else f"{MON[int(m2) - 1]} {int(d2)}")
    return f"{s}, {y}" if not until or until[:4] == y else s


def short(iso, until=None):
    """The table's date, the year in its row (STYLE 1): "Mar.&nbsp;24", "Jan.&nbsp;30–<wbr>Feb.&nbsp;7"."""
    y, m, d = iso.split("-")
    s = f"{MON[int(m) - 1]}&nbsp;{int(d)}"
    if until:
        y2, m2, d2 = until.split("-")
        s += "–<wbr>" + (f"{int(d2)}" if m2 == m and y2 == y else f"{MON[int(m2) - 1]}&nbsp;{int(d2)}")
        if y2 != y:
            s += f", {y2}"
    return s


def rec_link(s):
    g = s.get("rec")
    if not g:
        return ""
    pkg = re.match(r"(GPO-CRECB-\d{4}-pt\d+)", g).group(1)
    y = int(g[10:14])
    ch = "House" if s.get("chamber") == "House" else "Senate"
    page = s.get("page")
    tip = f"{VOL.get(y, '')} Cong. Rec.{' ' + str(page) if page else ''} ({ch}, {date(s['date'])})"
    return f'<a href="{esc(REC.format(pkg=pkg, g=g))}" title="{esc(tip)}">{esc(page) if page else "day"}</a>'


def votes(s):
    vs = s.get("votes") or []
    out = []
    for ch, cong, num, y, n, what in vs:
        link = f'<a href="{esc(VV.format(ch=ch, cong=cong, num=num))}">{y}–{n}</a>'
        out.append(f"{esc(what)} {link}" if len(vs) > 1 else link)
    return "<br>".join(out)


def ordinal(n):
    n = int(n)
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'd', 3: 'd'}.get(n % 10, 'th')}"


def block(key, sfx=""):
    b = load().get(key)
    if not b:
        return ""
    rows, notes, year = [], [], None
    for s in b["steps"]:
        y = s["date"][:4]
        if y != year:
            year = y
            rows.append(f'<tr class="bly"><th colspan="5">{y} <span>· {VOL.get(int(y), "")} Cong. Rec.</span></th></tr>')
        d = short(s["date"], s.get("until"))
        when = f'<a href="#{esc(s["entry"])}">{d}</a>' if s.get("entry") else d
        what = esc(s["what"])
        if s.get("stat"):
            vol, page = b["stat"].split("|")
            what += f', <a href="{esc(STAT.format(vol=vol, granule=b["granule"]))}">{vol} Stat. {page}</a>, Pub. L. {esc(b["pl"])}'
        if s.get("note"):
            notes.append(f'{date(s["date"])}: {s["note"]}')
        c, full = CH.get(s.get("chamber"), ("", ""))
        ct = f' title="{full}"' if full else ""
        rows.append(f'<tr><td class="bld">{when}</td><td class="blc"{ct}>{c}</td>'
                    f'<td>{what}</td><td class="blv">{votes(s)}</td><td class="blr">{rec_link(s)}</td></tr>')
    hist = "; ".join(f'<a href="{esc(REC.format(pkg=g.rsplit("-", 1)[0], g=g))}">{y}</a>' for y, part, g in b.get("history") or [])
    cong = f', {ordinal(b["congress"])} Cong.' if b.get("congress") else ""
    return (f'<div class="bl" id="bl-{esc(key)}{sfx}"><p class="blb">{esc(b["bill"])}{cong}</p>'
            '<div class="blw"><table><thead><tr><th>Date</th><th></th><th>Step</th><th>Roll call</th><th class="blr">Page</th>'
            f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            + "".join(f'<p class="bln">{esc(n)}</p>' for n in notes)
            + f'<p class="blsrc">The steps: the bound <i>Congressional Record</i>, History of Bills and Resolutions ({hist}), '
              'each page turned to its day by the Record\'s daily parts on govinfo; the roll calls, Voteview.</p></div>')


def introduction(b):
    """The bill's first introduction in either chamber: its first step "introduced" (STYLE 7)."""
    for s in b.get("steps") or []:
        if re.search(r"\bintroduced\b", s.get("what", ""), re.I):
            return s
    return None


def placements(series):
    """{key: [(date, entry id, calendar list)]}, by date: the entries tagged bill:<key> (STYLE 7)."""
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^bill:([a-z0-9-]+)$", t)
                if m:
                    out.setdefault(m.group(1), []).append((str(e.get("date") or ""), e["id"], lst))
    for v in out.values():
        v.sort(key=lambda x: x[0])
    return out


def tagged(series):
    """{key: the entry that first carries the table}: the introduction's (committees.py links a bill there)."""
    return {k: v[0][1] for k, v in placements(series).items()}


def inject(page, series):
    used = False
    for key, ps in placements(series).items():
        for i, (d, eid, lst) in enumerate(ps):
            sfx = f"-y{d[:4]}" if i else ""
            blk = block(key, sfx)
            if not blk:
                continue
            page, k = contents.put(page, eid, blk, "bill", key)
            if k and sfx:                # STYLE 7: a later year's anchor its own, for the reader
                aid = contents.anchor_id("bill", key)
                page = re.sub(r'id="' + re.escape(aid) + r'"(?=[^>]*data-tbe="' + re.escape(eid) + '")',
                              f'id="{aid}{sfx}"', page, count=1)
            used = used or bool(k)
    if used and 'id="blstyle"' not in page:
        page = page.replace("</head>", STYLE + "\n</head>", 1)
    return page


def problems(series=None):
    out = []
    ids = None
    if series is not None:
        ids = {e["id"] for lst in series.lists.values() if lst.kind == "calendar" for _, e in lst.entries()}
    for key, b in load().items():
        where = f"congress/bills.yaml {key}"
        for f in ("title", "bill", "pl", "stat", "granule", "steps"):
            if not b.get(f):
                out.append((where, f"no {f}"))
        if not re.match(r"^\d+\|\d+$", str(b.get("stat", ""))):
            out.append((where, f"a malformed Statutes cite {b.get('stat')}"))
        last = ""
        for s in b.get("steps") or []:
            d = str(s.get("date", ""))
            if not re.match(r"^\d{4}-\d\d-\d\d$", d) or d < last:
                out.append((where, f"a step out of order or undated: {d}"))
            last = d
            if s.get("until") and str(s["until"]) < d:
                out.append((where, f"{d}: ends before it begins"))
            if s.get("rec") and not re.match(r"^GPO-CRECB-\d{4}-pt\d+-\d+-\d+$", s["rec"]):
                out.append((where, f"{d}: a malformed Record granule {s['rec']}"))
            if s.get("rec") and s["rec"][10:14] != d[:4]:
                out.append((where, f"{d}: the Record granule is of another year"))
            for v in s.get("votes") or []:
                if not (isinstance(v, list) and len(v) == 6 and v[0] in ("H", "S") and all(isinstance(x, int) for x in v[1:5])):
                    out.append((where, f"{d}: a malformed roll call {v}"))
            if ids is not None and s.get("entry") and s["entry"] not in ids:
                out.append((where, f"{d}: no calendar entry {s['entry']}"))
    if series is not None:
        from . import calsplit
        pl = placements(series)
        for key, ps in pl.items():
            if key not in load():
                out.append((ps[0][1], f"bill:{key}: no such bill in congress/bills.yaml"))
        for key, b in load().items():           # STYLE 7: the placements
            where = f"congress/bills.yaml {key}"
            s0 = introduction(b)
            ps = pl.get(key) or []
            if not s0:
                out.append((where, "no step \"introduced\": the table has no place"))
                continue
            if not ps:
                out.append((where, f"no calendar entry tagged bill:{key}"))
                continue
            d0, e0, lst = ps[0]
            if d0 != s0["date"] or s0.get("entry") != e0:
                out.append((e0, f"bill:{key}: the first table not under the introduction's entry ({s0['date']}, "
                                f"its step's entry {s0.get('entry')})"))
            want = {calsplit.half_of_date(lst, s["date"]) for s in b["steps"] if s["date"] >= s0["date"]}
            got = {}
            for d, eid, _ in ps:
                got.setdefault(calsplit.half_of_date(lst, d), []).append(eid)
            for h, eids in got.items():
                if len(eids) > 1:
                    out.append((eids[1], f"bill:{key}: a second table on one page ({', '.join(eids)})"))
                if h not in want:
                    out.append((eids[0], f"bill:{key}: a table on a page the course does not reach"))
            for h in sorted(want - set(got)):
                out.append((where, f"bill:{key}: no table on {calsplit.page_key(lst, h)}, where its course runs"))
    return out
