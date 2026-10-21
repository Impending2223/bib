"""A bill's course in the calendar: congress/bills.yaml (kept by hand from the bound Record's History of Bills and
Voteview). A calendar entry tagged bill:<key> (the signing) carries the bill's table.

STYLE
 1. One row a step, in the order of the Record: the date (a span "Jan. 30–Feb. 7"; linked to the calendar entry that
    tells the step, where one does), the chamber, the step in the series' prose, the roll calls, the Record.
 2. Roll calls as the calendar writes them: the count linked to Voteview, "324–67", what the vote was on before it
    where a day has more than one ("recommittal 199–226; passage 271–155"). A step with no roll call leaves the cell
    empty: the History of Bills does not say "voice vote", so neither does the table.
 3. The Record: the page as the History of Bills prints it, linked to the day's granule of that chamber's proceedings
    on govinfo; a step the History misprints says so in its note (shown under the table).
 4. The last row: approved, the Statutes cite linked to govinfo, the public law. The sources under the table: the
    History of Bills, by year, linked; Voteview.
"""
import os
import re

from . import store

PATH = os.path.join(store.ROOT, "congress", "bills.yaml")
_C = {}
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
REC = "https://www.govinfo.gov/content/pkg/{pkg}/pdf/{g}.pdf"
STAT = "https://www.govinfo.gov/content/pkg/STATUTE-{vol}/pdf/{granule}.pdf"
VV = "https://voteview.com/rollcall/R{ch}{cong:03d}{num:04d}"
VOL = {1960: 106, 1961: 107, 1962: 108, 1963: 109, 1964: 110, 1965: 111, 1966: 112, 1967: 113, 1968: 114}
STYLE = """<style id="blstyle">
.bl{margin:1rem 0 .5rem;font-family:var(--sans)}
.bl .blh{font-weight:700;font-size:.95rem;margin:.2rem 0 .4rem}
.bl .blw{overflow-x:auto;-webkit-overflow-scrolling:touch}
.bl table{border-collapse:collapse;width:100%;min-width:32rem;font-size:.78rem;line-height:1.35;font-variant-numeric:tabular-nums}
.bl th,.bl td{text-align:left;vertical-align:top;padding:.2rem .5rem .2rem 0;border-bottom:1px solid var(--rule)}
.bl thead th{font-weight:600;color:var(--muted);font-size:.74rem}
.bl td.bld{white-space:nowrap}
.bl .bln{font-size:.78rem;line-height:1.45;color:var(--note);margin:.3rem 0}
.bl .blsrc{font-size:.78rem;color:var(--muted);line-height:1.4;margin:.3rem 0}
@media (max-width:520px){.bl table{min-width:0}}
</style>"""


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def load():
    if "d" not in _C:
        _C["d"] = (store.load_yaml(PATH) if os.path.exists(PATH) else None) or {}
    return _C["d"].get("bills") or {}


def date(iso, until=None):
    y, m, d = iso.split("-")
    s = f"{MON[int(m) - 1]} {int(d)}"
    if until:
        y2, m2, d2 = until.split("-")
        s += "–" + (f"{int(d2)}" if m2 == m else f"{MON[int(m2) - 1]} {int(d2)}")
    return f"{s}, {y}" if not until or until[:4] == y else s


def rec_link(s):
    g = s.get("rec")
    if not g:
        return ""
    pkg = re.match(r"(GPO-CRECB-\d{4}-pt\d+)", g).group(1)
    y = int(g[10:14])
    page = f", {s['page']}" if s.get("page") else ""
    ch = "House" if s.get("chamber") == "House" else "Senate"
    return f'<a href="{esc(REC.format(pkg=pkg, g=g))}">{VOL.get(y, "")} Cong. Rec.{page}</a> ({ch})'


def votes(s):
    vs = s.get("votes") or []
    out = []
    for ch, cong, num, y, n, what in vs:
        link = f'<a href="{esc(VV.format(ch=ch, cong=cong, num=num))}">{y}–{n}</a>'
        out.append(f"{esc(what)} {link}" if len(vs) > 1 else link)
    return "; ".join(out)


def block(key):
    b = load().get(key)
    if not b:
        return ""
    rows, notes = [], []
    for s in b["steps"]:
        d = date(s["date"], s.get("until"))
        when = f'<a href="#{esc(s["entry"])}">{d}</a>' if s.get("entry") else d
        what = esc(s["what"])
        if s.get("stat"):
            vol, page = b["stat"].split("|")
            what += f', <a href="{esc(STAT.format(vol=vol, granule=b["granule"]))}">{vol} Stat. {page}</a>, Pub. L. {esc(b["pl"])}'
        if s.get("note"):
            notes.append(f'{date(s["date"])}: {s["note"]}')
        rows.append(f'<tr><td class="bld">{when}</td><td>{esc(s.get("chamber", "President" if s.get("stat") else ""))}</td>'
                    f'<td>{what}</td><td>{votes(s)}</td><td>{rec_link(s)}</td></tr>')
    hist = "; ".join(f'<a href="{esc(REC.format(pkg=g.rsplit("-", 1)[0], g=g))}">{y}</a>' for y, part, g in b.get("history") or [])
    return (f'<div class="bl" id="bl-{esc(key)}"><p class="blh">{esc(b["title"])}, {esc(b["bill"])}: its course</p>'
            '<div class="blw"><table><thead><tr><th>Date</th><th>Chamber</th><th>Step</th><th>Roll call</th><th>Record</th>'
            f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            + "".join(f'<p class="bln">{esc(n)}</p>' for n in notes)
            + f'<p class="blsrc">The steps: the bound <i>Congressional Record</i>, History of Bills and Resolutions ({hist}), '
              'each page turned to its day by the Record\'s daily parts on govinfo; the roll calls, Voteview.</p></div>')


def tagged(series):
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^bill:([a-z0-9-]+)$", t)
                if m:
                    out[m.group(1)] = e["id"]
    return out


def inject(page, series):
    used = False
    for key, eid in tagged(series).items():
        blk = block(key)
        if not blk:
            continue
        pat = re.compile(r'(<li id="' + re.escape(eid) + r'"[^>]*>.*?)(</li>)', re.S)
        page, k = pat.subn(lambda mm: mm.group(1) + blk + mm.group(2), page, count=1)
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
        for key, eid in tagged(series).items():
            if key not in load():
                out.append((eid, f"bill:{key}: no such bill in congress/bills.yaml"))
    return out
