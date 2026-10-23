"""Each session's appropriation bills against the President's estimates: congress/appropriations.yaml (kept by hand from
the tables printed in the bound Congressional Record at each session's end). A calendar entry tagged
appropriations:<Congress>-<session> (the session's adjournment) carries the session's table.

STYLE
 1. One table a session, four columns, to fit the calendar's column and a 400px phone without sideways scrolling: the
    bill (its title as the source prints it, the bill's number under it, muted), the estimate, the amount, the change.
    Heads: "Estimate", "Enacted", "Change", "$m"; the source's own heads on hover and named under the table.
 2. Money in $ millions, one decimal, unbroken, right-aligned; the source's figure in whole dollars on hover. A
    decrease with U+2212, an increase with "+"; "0.0" where the source prints a nought; "—" where it prints nothing.
 3. The source's groups (supplementals, the fiscal year's bills) as rows across, in bold; each group's printed total,
    and the session's, in bold under a rule. A figure the source prints in parentheses (loan and contract authority,
    memoranda: not counted in the totals) in parentheses, muted; a line under a bill (its loan authority, the
    District's Federal payment) indented.
 4. Where the source prints no estimate (88th Cong., 2d sess., the House committee's summary), the estimate is the
    amount less the change, in italics, "computed" on hover, the note saying so. Where it prints the change as a
    saving (89th, 1st), the table shows it as a change all the same, the note saying so.
 5. Under the table: the rows' notes and the source's misprints (its own figures disagreeing), then the source: the
    table's heading as printed, in italics, who prepared it where it says, the Record's volume and page linked to the
    day's granule on govinfo, the chamber and the day.
"""
import os
import re

from . import contents, store
from .contents import ordinal

PATH = os.path.join(store.ROOT, "congress", "appropriations.yaml")
_C = {}
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
REC = "https://www.govinfo.gov/content/pkg/{pkg}/pdf/{g}.pdf"
VOL = {1960: 106, 1961: 107, 1962: 108, 1963: 109, 1964: 110, 1965: 111, 1966: 112, 1967: 113, 1968: 114}
ORD = {1: "1st", 2: "2d"}
STYLE = """<style id="apstyle">
.ap{margin:1rem 0 .5rem;font-family:var(--sans)}
.ap .aph{font-weight:700;font-size:.95rem;margin:.2rem 0 .4rem}
.ap table{border-collapse:collapse;width:100%;font-size:.76rem;line-height:1.3;font-variant-numeric:tabular-nums}
.ap th,.ap td{text-align:right;vertical-align:bottom;padding:.16rem 0 .16rem .5rem;border-bottom:1px solid var(--rule)}
.ap td{white-space:nowrap}
.ap th:first-child,.ap td:first-child{text-align:left;padding-left:0;white-space:normal}
.ap thead th{font-weight:600;color:var(--muted);font-size:.72rem;line-height:1.2}
.ap tr.apg th{text-align:left;font-weight:700;padding-top:.55rem;color:var(--ink);border-bottom:1px solid var(--ink)}
.ap tr.apt td{font-weight:700}
.ap tr.app td{color:var(--muted)}
.ap tr.aps td:first-child{padding-left:.8rem}
.ap .apb{display:block;color:var(--muted);font-size:.68rem}
.ap td.apc{font-style:italic}
.ap .apn{font-size:.78rem;line-height:1.45;color:var(--note);margin:.3rem 0}
.ap .apsrc{font-size:.78rem;color:var(--muted);line-height:1.4;margin:.3rem 0}
</style>"""


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def load():
    if "d" not in _C:
        _C["d"] = (store.load_yaml(PATH) if os.path.exists(PATH) else None) or {}
    return {str(k): v for k, v in (_C["d"].get("sessions") or {}).items()}


def date(iso):
    y, m, d = str(iso).split("-")
    return f"{MON[int(m) - 1]} {int(d)}, {y}"


def money(v, sign=False):
    if v is None:
        return None
    s = f"{abs(v) / 1e6:,.1f}"
    if v < 0:
        return "−" + s
    return ("+" + s) if sign and v > 0 else s


def dollars(v):
    return ("−" if v < 0 else "") + f"${abs(v):,}"


def cell(v, paren=False, sign=False, cls="", title=None):
    m = money(v, sign)
    if m is None:
        return '<td>—</td>'
    if paren:
        m = f"({m})"
    t = title or dollars(v)
    return f'<td{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} title="{esc(t)}">{m}</td>'


def est_of(s, b):
    if b.get("est") is not None:
        return b["est"], False
    if s.get("est_computed") and b.get("final") is not None and b.get("chg") is not None:
        return b["final"] - b["chg"], True
    return None, False


def row(s, b, total=False):
    paren = bool(b.get("paren"))
    e, comp = est_of(s, b)
    name = esc(b.get("title", "Total"))
    if b.get("bill"):
        name += f'<span class="apb">{esc(b["bill"])}</span>'
    cls = "apt" if total else " ".join(c for c, on in (("app", paren), ("aps", b.get("sub"))) if on)
    ecell = cell(e, paren, cls="apc" if comp else "", title="computed: the amount less the change" if comp else None)
    return (f'<tr{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}><td>{name}</td>{ecell}'
            f'{cell(b.get("final"), paren)}{cell(b.get("chg"), paren, sign=True)}</tr>')


def block(key):
    s = load().get(key)
    if not s:
        return ""
    cong, sess = key.split("-")
    rows, notes = [], []
    for g in s.get("groups") or []:
        rows.append(f'<tr class="apg"><th colspan="4">{esc(g["name"])}</th></tr>')
        for b in g.get("bills") or []:
            rows.append(row(s, b))
            for f in ("note", "misprint"):
                if b.get(f):
                    notes.append(f'{b.get("title")}{" (" + b["bill"] + ")" if b.get("bill") else ""}: {b[f]}')
        if g.get("total"):
            rows.append(row(s, dict(g["total"], title=f'Total, {g["name"]}'), total=True))
            if g["total"].get("misprint"):
                notes.append(f'Total, {g["name"]}: {g["total"]["misprint"]}')
    if s.get("total"):
        rows.append(row(s, dict(s["total"], title="Total, the session"), total=True))
        if s["total"].get("misprint"):
            notes.append(f'Total: {s["total"]["misprint"]}')
    if s.get("est_computed"):
        notes.insert(0, "The source prints no estimates: each is the amount less the change, in italics.")
    if s.get("chg_sign") == "saving":
        notes.insert(0, "The source prints each reduction as a saving, a positive figure; here a change, negative.")
    heads = "; ".join(f"{w}, “{esc(s[f])}”" for w, f in (("Estimate", "est"), ("Enacted", "final"), ("Change", "chg"))
                      if s.get(f))
    y = int(str(s["date"])[:4])
    g = s["rec"]
    pkg = re.match(r"(GPO-CRECB-\d{4}-pt\d+)", g).group(1)
    rec = f'<a href="{esc(REC.format(pkg=pkg, g=g))}">{VOL.get(y, "")} Cong. Rec. {esc(s["page"])}</a>'
    by = f' {esc(s["by"])}.' if s.get("by") else ""
    src = (f'<p class="apsrc">Source: <i>{esc(s["head"])}</i>, {rec} ({esc(s["chamber"])}, {date(s["date"])}).{by} '
           f'The columns: {heads}. Indefinite appropriations as the table counts them; no permanent or back-door '
           'authority, as it says.</p>')
    return (f'<div class="ap" id="ap-{esc(key)}"><p class="aph">Appropriations, {ordinal(cong)} Cong., '
            f'{ORD.get(int(sess), sess)} sess.: the bills against the estimates</p>'
            '<table><thead><tr><th>Bill</th><th>Estimate<br>$m</th><th>Enacted<br>$m</th><th>Change<br>$m</th></tr>'
            f'</thead><tbody>{"".join(rows)}</tbody></table>'
            + "".join(f'<p class="apn">{esc(n)}</p>' for n in notes) + src + "</div>")


def label(key):
    cong, sess = str(key).split("-")
    return f"Appropriations, {ordinal(cong)} Cong., {ORD.get(int(sess), sess)} sess."


def tagged(series):
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^appropriations:(\d+-\d)$", t)
                if m:
                    out[m.group(1)] = e["id"]
    return out


def inject(page, series):
    used = False
    for key, eid in tagged(series).items():
        blk = block(key)
        if not blk:
            continue
        page, k = contents.put(page, eid, blk, "appropriations", key)
        used = used or bool(k)
    if used and 'id="apstyle"' not in page:
        page = page.replace("</head>", STYLE + "\n</head>", 1)
    return page


def problems(series=None):
    out = []
    for key, s in load().items():
        where = f"congress/appropriations.yaml {key}"
        if not re.match(r"^\d+-[12]$", key):
            out.append((where, "a key not <Congress>-<session>"))
        for f in ("date", "chamber", "page", "rec", "head", "final", "chg", "entry", "groups"):
            if not s.get(f):
                out.append((where, f"no {f}"))
        if not s.get("est") and not s.get("est_computed"):
            out.append((where, "no estimate column and not est_computed"))
        if s.get("rec") and not re.match(r"^GPO-CRECB-\d{4}-pt\d+-\d+-\d+$", s["rec"]):
            out.append((where, f"a malformed Record granule {s['rec']}"))
        if s.get("rec") and str(s["rec"])[10:14] != str(s.get("date", ""))[:4]:
            out.append((where, "the Record granule is of another year"))
        whole = {"est": 0, "final": 0, "chg": 0}
        for g in s.get("groups") or []:
            sums = {"est": 0, "final": 0, "chg": 0}
            for b in g.get("bills") or []:
                w = f"{where} {g.get('name')}: {b.get('title')}"
                for f in ("est", "final", "chg"):
                    v = b.get(f)
                    if v is not None and not isinstance(v, int):
                        out.append((w, f"{f} not whole dollars: {v}"))
                e, f, c = b.get("est"), b.get("final"), b.get("chg")
                if None not in (e, f, c) and e + c != f and not b.get("misprint"):
                    out.append((w, f"estimate {e:,} and change {c:,} do not make the amount {f:,}"))
                if b.get("paren"):
                    continue
                for k in sums:
                    if isinstance(b.get(k), int):
                        sums[k] += b[k]
            t = g.get("total")
            if t:
                for k in sums:
                    if t.get(k) is not None and t[k] != sums[k] and not t.get("misprint"):
                        out.append((f"{where} {g.get('name')}", f"{k}: the rows add to {sums[k]:,}, the total prints {t[k]:,}"))
            for k in whole:
                whole[k] += sums[k]
        t = s.get("total")
        if t:
            for k in whole:
                if t.get(k) is not None and t[k] != whole[k] and not t.get("misprint"):
                    out.append((where, f"{k}: the groups add to {whole[k]:,}, the session's total prints {t[k]:,}"))
    if series is not None:
        ids = {e["id"]: e for lst in series.lists.values() if lst.kind == "calendar" for _, e in lst.entries()}
        tags = tagged(series)
        for key, s in load().items():
            if s.get("entry") and s["entry"] not in ids:
                out.append((f"congress/appropriations.yaml {key}", f"no calendar entry {s['entry']}"))
        for key, eid in tags.items():
            if key not in load():
                out.append((eid, f"appropriations:{key}: no such session in congress/appropriations.yaml"))
    return out
