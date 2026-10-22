"""The States' finances by fiscal year, 1960–1968: statefin/states.yaml (written by tools/statefin/make_statefin.py from the
Census Bureau's historical finance databases, the figures its annual *State Government Finances* printed).

A calendar entry tagged statefin:<YYYY> (Census's fiscal year: each State's year ending in it) carries that year's
block: a summary, two maps, the State governments' table, and the State and its local governments together.

STYLE
 1. Census's figures on Census's classification, not the States' budgets: "revenue less expenditure" is Census's total
    revenue less its total expenditure (insurance trusts and utilities in both), not a budget balance; borrowing for
    capital outlay makes it a deficit by construction. No "surplus" or "deficit" is claimed.
 2. Fiscal years differ by State: the block counts the year-ends the database gives (most June 30; New York's Mar. 31,
    Alabama's Sept. 30, Texas's Aug. 31) and prints each in the second table.
 3. Taxes per $1,000 of personal income: the fiscal year's taxes over the personal income of the calendar year before,
    as Census's tables relate them ("Relation of selected financial items to personal income"); the personal income is
    BEA's as the database carries it (revised), not the estimate printed with the tables, so a ratio may differ a
    little from the printed one. Per head: the database's population for the year.
 4. Shares: of the State's taxes (general sales, individual income, corporate income, motor fuel, property); federal
    aid of general revenue; current operation, capital outlay and aid to local governments of total expenditure.
    "—" where the State had no such tax (Census reports nothing), "n.a." where the database prints no figure.
 5. The regime map: a State with any revenue from a general sales tax in the year, any from an individual income tax,
    both, or neither, by Census's columns however narrow the tax; the year's adopters (first revenue in the year after
    none in the year before) in the full color, the rest lighter. A tax enacted in one fiscal year shows in the first
    year it yields revenue; the calendar's entries date the acts.
 6. The burden map: taxes per $1,000 of personal income, by the State's place among the fifty that year (a quantile
    rule: the lowest at the near-white, the highest at the full amber, evenly by rank). D.C. is left off it.
 7. D.C.: the database's exhibit, a city government, in the tables and the regime map, not in the U.S. total nor the
    ranks. In the State-and-local table the U.S. total includes D.C. (Census's State-area totals, rounded to $0.1
    million).
 8. Cites: the database (linked), and the year's printed report by table and first page (from its contents), linked
    to Census's archive of the scans.
"""
import json
import os
import re

from . import contents, store

PATH = os.path.join(store.ROOT, "statefin", "states.yaml")
_C = {}
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
SHARES = [("sales", "General sales"), ("income", "Individual income"), ("corp", "Corporate income"),
          ("fuel", "Motor fuel"), ("property", "Property")]
REGIME = {"both": ("q1", "General sales and individual income taxes"), "sales": ("q2", "General sales tax only"),
          "income": ("q3", "Individual income tax only"), "neither": ("qU", "Neither")}
TLABEL = {"aggregates": "financial aggregates", "general": "general revenue", "taxes": "taxes by type",
          "revenue": "revenue by source", "character": "expenditure by character and object",
          "debt": "debt outstanding", "percap": "per capita amounts", "relation": "relation to personal income",
          "income": "population and personal income"}
STYLE = """<style id="sfstyle">
.sf{margin:1rem 0 .5rem;font-family:var(--sans)}
.sf .sfh{font-weight:700;font-size:.95rem;margin:.2rem 0 .4rem}
.sf .sfs{font-size:.85rem;line-height:1.4;margin:.15rem 0}
.sf .sfn{font-size:.78rem;line-height:1.45;color:var(--note);margin:.3rem 0}
.sf .sfm{display:grid;grid-template-columns:1fr;gap:.6rem;margin:.5rem 0}
@media (min-width:760px){.sf .sfm{grid-template-columns:1fr 1fr}}
.sf .sfm>.cg{margin:0}
.sf .sfm .cgkey{margin:.3rem 0 0}
.sf .sfw{overflow-x:auto;-webkit-overflow-scrolling:touch}
.sf .cgr table.sft{table-layout:auto;min-width:36rem;font-size:.78rem;font-variant-numeric:tabular-nums}
.sf .cgr table.sft th,.sf .cgr table.sft td{text-align:right;padding:.2rem .4rem .2rem 0;vertical-align:bottom}
.sf .cgr table.sft td{white-space:nowrap}
.sf .cgr table.sft th:first-child,.sf .cgr table.sft td:first-child{text-align:left}
.sf .cgr table.sft thead th{font-weight:600;line-height:1.25}
.sf .cgr table.sft tr.us td{font-weight:700}
.sf .cgr table.sft caption{text-align:left;font-weight:600;font-size:.8rem;padding:.6rem 0 .2rem}
</style>"""
SCRIPT = """<script id="sfscript">
(function(){function open(id){var r=document.getElementById(id);if(!r)return;var d=r.closest('details');if(d)d.open=true;}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#sf"]');if(a)open(a.getAttribute('href').slice(1));},true);
if(/^#sf/.test(location.hash))open(location.hash.slice(1));})();
</script>"""


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def load():
    if "d" not in _C:
        _C["d"] = store.load_yaml(PATH) if os.path.exists(PATH) else {}
    return _C["d"] or {}


def years():
    return {int(k): v for k, v in (load().get("states") or {}).items()}


def local(y):
    return {k: v for k, v in ((load().get("local") or {}).get(y) or (load().get("local") or {}).get(str(y)) or {}).items()}


def state_name(st):
    from .congress import STATE
    return {"US": "United States", "DC": "District of Columbia"}.get(st) or STATE.get(st, st)


def date(iso):
    y, m, d = iso.split("-")
    return f"{MON[int(m) - 1]} {int(d)}, {y}"


def ratio(a, b, k=1.0):
    if a is None or not b:
        return None
    return a * k / b


def per_inc(r):
    return ratio(r.get("tax"), r.get("pi_prev"))


def per_head(r, f="tax"):
    return ratio(r.get(f), r.get("pop"))


def share(r, f, of):
    if r.get(f) is None or not r.get(of):
        return None
    return 100.0 * r[f] / r[of]


def fmt(v, nd=1, zero_dash=False, raw=None):
    """'n.a.' where no figure; '—' where the State had none of it (raw 0)."""
    if raw == 0 and zero_dash:
        return "—"
    if v is None:
        return "n.a."
    s = f"{v:,.{nd}f}"
    return s.replace("-", "−")


def regime(r):
    s, i = bool(r.get("sales")), bool(r.get("income"))
    return "both" if s and i else "sales" if s else "income" if i else "neither"


def adopted(y, st):
    """The taxes the State first drew revenue from this year (after none the year before)."""
    S = years()
    cur, prev = (S.get(y) or {}).get(st) or {}, (S.get(y - 1) or {}).get(st) or {}
    if not prev:
        return []
    return [k for k in ("sales", "income") if cur.get(k) and not prev.get(k)]


def states50(S):
    return {k: v for k, v in S.items() if k not in ("US", "DC")}


def lighten(cls, pct=45):
    return f"v:color-mix(in oklab,var(--{cls}) {pct}%,var(--rW))"


def amber(t):
    return f"v:color-mix(in oklab,var(--rA) {100 * max(0.0, min(1.0, t)):.1f}%,var(--rW))"


def names(sts):
    sts = [state_name(s) for s in sts]
    if len(sts) <= 1:
        return "".join(sts)
    return ", ".join(sts[:-1]) + " and " + sts[-1]


def bn(v):
    return f"${v / 1e6:,.1f} billion"


def fy_ends(S):
    """'June 30, 1963, in 46 States; Mar. 31 in New York; ...'"""
    by = {}
    for st, r in states50(S).items():
        if r.get("fy_end"):
            by.setdefault(r["fy_end"], []).append(st)
    if not by:
        return ""
    main = max(by, key=lambda k: len(by[k]))
    out = [f"{date(main)}, in {len(by[main])} States"]
    for k in sorted(by, key=lambda k: (k[5:], k)):
        if k != main:
            out.append(f"{date(k)[:-6]} in {names(sorted(by[k]))}")
    return "; ".join(out)


def summary(y):
    S = years()[y]
    us = S.get("US") or {}
    S50 = states50(S)
    reg = {k: sorted(st for st, r in S50.items() if regime(r) == k) for k in REGIME}
    out = [f"Fiscal {y}, the fifty State governments together: taxes {bn(us['tax'])}, ${fmt(per_inc(us), 2)} per "
           f"$1,000 of {y - 1} personal income, ${fmt(per_head(us), 2)} a head. Federal aid {bn(us['fed'])}, "
           f"{fmt(share(us, 'fed', 'genrev'))} percent of general revenue. Long-term debt {bn(us['ltd'])} at the end of the "
           "States' fiscal years."]
    n_s = len(reg["both"]) + len(reg["sales"])
    n_i = len(reg["both"]) + len(reg["income"])
    out.append(f"General sales taxes in {n_s} States, individual income taxes in {n_i}: both in {len(reg['both'])}, "
               + (f"neither in {len(reg['neither'])} ({names(reg['neither'])})." if reg["neither"] else "neither in none."))
    ad = {k: sorted(st for st in S50 if k in adopted(y, st)) for k in ("sales", "income")}
    bits = []
    if ad["sales"]:
        bits.append(f"from a general sales tax: {names(ad['sales'])}")
    if ad["income"]:
        bits.append(f"from an individual income tax: {names(ad['income'])}")
    if bits:
        out.append("First revenue in the year " + "; ".join(bits) + ".")
    rk = sorted(((per_inc(r), st) for st, r in S50.items() if per_inc(r) is not None), reverse=True)
    top = ", ".join(f"{state_name(st)} {v:.2f}" for v, st in rk[:3])
    low = ", ".join(f"{state_name(st)} {v:.2f}" for v, st in rk[-3:][::-1])
    out.append(f"Taxes per $1,000 of personal income, highest: {top}; lowest: {low}.")
    return out


def hover(y, st, r):
    reg = REGIME[regime(r)][1].lower()
    ad = adopted(y, st)
    t = (f"{state_name(st)}, fiscal {y}: taxes ${fmt(per_inc(r), 2)} per $1,000 of personal income, "
         f"${fmt(per_head(r), 2)} a head; {reg}")
    if ad:
        t += "; first revenue from its " + " and ".join({"sales": "general sales tax", "income": "individual income tax"}[k]
                                                         for k in ad)
    if st == "DC":
        t += " (a city government, Census's exhibit)"
    return t


def maps(y):
    from .smart import smarten
    S = years()[y]
    S50 = states50(S)
    reg, qnt = {}, {}
    for st, r in S.items():
        if st == "US":
            continue
        cls = REGIME[regime(r)][0]
        reg[st] = {"id": f"sf{y}-{st}", "f": cls if adopted(y, st) else lighten(cls), "mg": 0,
                   "t": smarten(hover(y, st, r))}
    vals = sorted((per_inc(r), st) for st, r in S50.items() if per_inc(r) is not None)
    n = len(vals)
    for i, (v, st) in enumerate(vals):
        qnt[st] = {"id": f"sf{y}-{st}", "f": amber(i / (n - 1) if n > 1 else 1), "mg": 0,
                   "t": smarten(hover(y, st, S[st]) + f"; {n - i} of {n}")}
    sw = lambda f, t, style="": (f'<span class="pqi"><span class="sw {f}"{style}></span>{t}</span> ')
    key1 = "".join(sw(c, t) for c, t in REGIME.values())
    key1 += sw("", "lighter: no new tax this year", f' style="background:color-mix(in oklab,var(--q1) 45%,var(--rW))"')
    lo, hi = (vals[0][0], vals[-1][0]) if vals else (0, 0)
    key2 = f'<span class="pqi">{lo:.2f}<span class="gr gA"></span>{hi:.2f}, by rank among the fifty</span>'

    def one(q, q_id, cap, key, none):
        seats = json.dumps({"q": q}, ensure_ascii=False, separators=(",", ":"))
        return (f'<div class="cg el pq" data-cg="sf{y}{q_id}"><script type="application/json" class="cgseats">{seats}'
                f'</script><div class="cgmaps"><figure class="cgmap" data-chamber="q" data-none="{esc(none)}" '
                f'data-info="Click a State for its figures." data-rows="Figures ↓"><figcaption>{esc(cap)}</figcaption>'
                f'<div class="cgv" style="aspect-ratio:960/660"></div></figure></div><span data-views="r"></span>'
                f'<p class="cgkey elkey"><span class="lk lk-r">{key}</span></p></div>')
    return ('<div class="sfm">'
            + one(reg, "r", f"Taxes in force, {y}", key1, "no figures")
            + one(qnt, "q", f"Taxes per $1,000 of income, {y}", key2, "no figures")
            + "</div>")


def table_a(y, S):
    head = ("<tr><th>State</th><th>Per $1,000 of income</th><th>Per head ($)</th>"
            + "".join(f"<th>{t} (%)</th>" for _, t in SHARES) + "</tr>")
    body = []
    for st in ["US"] + sorted(k for k in S if k != "US"):
        r = S[st]
        cells = [fmt(per_inc(r), 2), fmt(per_head(r), 2)] + [fmt(share(r, f, "tax"), 1, True, r.get(f)) for f, _ in SHARES]
        body.append(f'<tbody id="sf{y}-{st}"><tr{" class=\"us\"" if st == "US" else ""}><td><span title="{esc(state_name(st))}">'
                    f'{"U.S." if st == "US" else esc(st)}</span></td>' + "".join(f"<td>{c}</td>" for c in cells) + "</tr></tbody>")
    return (f'<div class="sfw"><table class="sft"><caption>Taxes: the amount, and the shares of five taxes in the State\'s taxes'
            f'</caption><thead>{head}</thead>{"".join(body)}</table></div>')


def table_b(y, S):
    head = ("<tr><th>State</th><th>Federal aid, % of general revenue</th><th>Current operation (%)</th>"
            "<th>Capital outlay (%)</th><th>Aid to local governments (%)</th><th>Long-term debt per head ($)</th>"
            "<th>Revenue less expenditure ($m)</th><th>Year ended</th></tr>")
    body = []
    for st in ["US"] + sorted(k for k in S if k != "US"):
        r = S[st]
        bal = None if r.get("rev") is None or r.get("exp") is None else (r["rev"] - r["exp"]) / 1000
        fy = r.get("fy_end")
        cells = [fmt(share(r, "fed", "genrev")), fmt(share(r, "curop", "exp")), fmt(share(r, "capital", "exp")),
                 fmt(share(r, "tolocal", "exp"), 1, True, r.get("tolocal")), fmt(per_head(r, "ltd"), 2), fmt(bal, 1),
                 (f"{MON[int(fy[5:7]) - 1]} {int(fy[8:])}" if fy else "")]
        body.append(f'<tr id="sfb{y}-{st}"{" class=\"us\"" if st == "US" else ""}><td>{"U.S." if st == "US" else esc(st)}</td>'
                    + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    return (f'<div class="sfw"><table class="sft"><caption>Revenue, expenditure and debt: shares of general revenue and of '
            f'total expenditure</caption><thead>{head}</thead><tbody>{"".join(body)}</tbody></table></div>')


def table_c(y):
    L = local(y)
    if not L:
        return ""
    head = ("<tr><th>State</th><th>Taxes per $1,000 of income</th><th>Taxes per head ($)</th>"
            "<th>State government's share of the taxes (%)</th><th>Property tax, % of taxes</th>"
            "<th>Federal aid, % of general revenue</th><th>Long-term debt per head ($)</th></tr>")
    body = []
    for st in ["US"] + sorted(k for k in L if k != "US"):
        r = L[st]
        cells = [fmt(per_inc(r), 2), fmt(per_head(r), 2), fmt(share(r, "state_tax", "tax")) if st != "DC" else "—",
                 fmt(share(r, "property", "tax")), fmt(share(r, "fed", "genrev")), fmt(per_head(r, "ltd"), 2)]
        body.append(f'<tr id="sfc{y}-{st}"{" class=\"us\"" if st == "US" else ""}><td>{"U.S." if st == "US" else esc(st)}</td>'
                    + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    return (f'<div class="sfw"><table class="sft"><caption>The State and its local governments together</caption>'
            f'<thead>{head}</thead><tbody>{"".join(body)}</tbody></table></div>')


def cities(y):
    return (load().get("cities") or {}).get(y) or (load().get("cities") or {}).get(str(y)) or {}


def city_name(n):
    """'NEW YORK CITY' -> New York; 'SAN FRANCISCO CITY AND COUNTY' -> San Francisco; 'FT WORTH CITY' -> Fort Worth."""
    n = n.strip()
    if n == "WASHINGTON DC":
        return "Washington"
    for suf in (" CITY AND COUNTY", " CITY"):
        if n.endswith(suf) and n not in ("KANSAS CITY", "OKLAHOMA CITY"):
            n = n[: -len(suf)]
            break
    words = []
    for w in n.split():
        words.append({"ST": "St.", "FT": "Fort"}.get(w, w.capitalize()))
    return " ".join(words)


def table_d(y):
    C = cities(y)
    if not C:
        return ""
    head = ("<tr><th>City</th><th>Taxes per head ($)</th><th>Property (%)</th><th>General sales (%)</th>"
            "<th>Selective sales (%)</th><th>All other (%)</th><th>State aid, % of general revenue</th>"
            "<th>Federal aid, % of general revenue</th><th>Long-term debt per head ($)</th></tr>")
    body = []
    for k, r in C.items():
        cells = [fmt(ratio(r.get("tax"), r.get("pop"), 1000), 2), fmt(share(r, "property", "tax")),
                 fmt(share(r, "sales", "tax"), 1, True, r.get("sales")), fmt(share(r, "selective", "tax"), 1, True, r.get("selective")),
                 fmt(share(r, "other", "tax"), 1, True, r.get("other")), fmt(share(r, "state", "genrev")),
                 fmt(share(r, "fed", "genrev")), fmt(ratio(r.get("ltd"), r.get("pop"), 1000), 2)]
        body.append(f'<tr id="sfd{y}-{esc(k)}"><td>{esc(city_name(r["name"]))}, {esc(r["st"])}</td>'
                    + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    return (f'<div class="sfw"><table class="sft"><caption>The {len(C)} largest cities, the census year {y}: '
            f'taxes, aid and debt (per head of the 1960 census)</caption><thead>{head}</thead><tbody>{"".join(body)}'
            f'</tbody></table></div>')


def cites(y):
    d = load()
    src = d.get("source") or {}
    rep = (d.get("reports") or {}).get(y) or (d.get("reports") or {}).get(str(y)) or {}
    s, l = src.get("states") or {}, src.get("local") or {}
    out = (f'Figures: U.S. Census Bureau, <a href="{esc(s.get("url", ""))}">{esc(s.get("title", ""))}</a>; the State and '
           f'local governments together, <a href="{esc(l.get("url", ""))}">{esc(l.get("title", ""))}</a>')
    c = src.get("cities") or {}
    out += (f'; the cities, <a href="{esc(c.get("url", ""))}">{esc(c.get("title", ""))}</a>.' if cities(y) else ".")
    if rep:
        tabs = "; ".join(f"{TLABEL.get(k, k)}, table {n}, p. {p}" for k, (n, p) in rep["tables"].items())
        out += (f' Printed in Census, <i>{esc(rep["title"])}</i> ({esc(rep["series"])}, {esc(rep["published"])}): {tabs} '
                f'(<a href="{esc(src.get("scans", ""))}">Census\'s scans</a>).')
    return out


def caveats(y):
    S = years()[y]
    return [f"Census's fiscal years: each State's year ending in {y}: {fy_ends(S)}. Census's figures, on its own "
            "classification, not the States' budgets: revenue less expenditure is its total revenue less its total "
            "expenditure, insurance trusts included, and borrowing for capital outlay makes it negative; it is not a "
            "budget balance.",
            f"Per $1,000 of personal income: the year's taxes over the personal income of {y - 1}, as Census's tables relate "
            "them, the personal income BEA's as the database carries it, not the estimate printed with the tables. "
            "D.C. is a city government, Census's exhibit, outside the U.S. total and the ranks. The regime follows "
            "Census's columns: any revenue from a general sales or an individual income tax, however narrow the tax; a "
            "tax enacted during a fiscal year shows in the first year it yields revenue. The State-and-local figures are "
            "Census's State-area totals, rounded to $0.1 million; their U.S. total includes D.C."] + (
        [f"The cities: the {len(cities(y))} the database flags large, each of 300,000 or more at the 1960 census; the city "
         "government alone, as Census counts it, and cities differ in what they run (schools, hospitals, welfare), so "
         "their figures are not alike; per head of the 1960 census. "
         "The database gives no column for a city's income tax: it falls under all other taxes."] if cities(y) else [])


def block(y):
    S = years().get(y)
    if not S:
        return ""
    return (f'<div class="sf" id="sf{y}"><p class="sfh">The States\' finances, fiscal {y}</p>'
            + "".join(f'<p class="sfs">{esc(s)}</p>' for s in summary(y))
            + maps(y)
            + f'<details class="cgr sfd"><summary>The States, fiscal {y}: taxes, revenue, expenditure, debt</summary>'
            + table_a(y, S) + table_b(y, S) + table_c(y) + table_d(y) + "</details>"
            + "".join(f'<p class="sfn">{esc(c)}</p>' for c in caveats(y))
            + f'<p class="elsrc">{cites(y)}</p></div>')


def tagged(series):
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^statefin:(\d{4})$", t)
                if m:
                    out[int(m.group(1))] = e["id"]
    return out


def inject(page, series):
    used = False
    for y, eid in tagged(series).items():
        blk = block(y)
        if not blk:
            continue
        page, k = contents.put(page, eid, blk, "statefin", y)
        used = used or bool(k)
    if used:
        if 'id="cggeo"' not in page:
            from . import congress
            data, geo = congress.load()
            if geo:
                page = page.replace("</body>", congress.assets(congress.geo_subset(geo, [])) + "\n</body>", 1)
        from . import roster
        page = roster.ensure(page)
        if 'id="sfstyle"' not in page:
            page = page.replace("</head>", STYLE + "\n</head>", 1)
            page = page.replace("</body>", SCRIPT + "\n</body>", 1)
    return page


def problems(series=None):
    out = []
    d = load()
    S = years()
    reps = {int(k) for k in (d.get("reports") or {})}
    for y, St in S.items():
        if y < 1960:                 # the year before the first, for the adopters; its U.S. total lacks Hawaii
            continue
        if "US" not in St:
            out.append(("statefin/states.yaml", f"{y}: no U.S. total"))
        if len(states50(St)) != 50:
            out.append(("statefin/states.yaml", f"{y}: {len(states50(St))} States, not 50"))
        for st, r in St.items():
            parts = sum(r.get(f) or 0 for f, _ in SHARES)
            if r.get("tax") is not None and parts > r["tax"]:
                out.append(("statefin/states.yaml", f"{y} {st}: five taxes exceed the total"))
            for f in ("curop", "capital", "tolocal"):
                if r.get(f) is not None and r.get("exp") is not None and r[f] > r["exp"]:
                    out.append(("statefin/states.yaml", f"{y} {st}: {f} exceeds total expenditure"))
        us = St.get("US") or {}
        tot = sum((r.get("tax") or 0) for r in states50(St).values())
        if us.get("tax") and abs(tot - us["tax"]) > 50:
            out.append(("statefin/states.yaml", f"{y}: the States' taxes add to {tot}, the U.S. total is {us['tax']}"))
    for y in (d.get("cities") or {}):
        for k, r in cities(int(y)).items():
            parts = sum(r.get(f) or 0 for f in ("property", "sales", "selective", "other"))
            if r.get("tax") is not None and abs(parts - r["tax"]) > 2:
                out.append(("statefin/states.yaml", f"{y} {r.get('name')}: the taxes by kind add to {parts}, not {r['tax']}"))
    if series is not None:
        for y, eid in tagged(series).items():
            if y not in S:
                out.append((eid, f"statefin:{y}: no such fiscal year"))
            elif y not in reps:
                out.append((eid, f"statefin:{y}: no printed report for the year in REPORTS"))
    return out
