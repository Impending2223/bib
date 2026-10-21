"""The national conventions, 1960-1968: elections/conventions.yaml, kept by hand from each convention's Proceedings (the
Call, the roll calls) and, for how each delegation was chosen, the source its `methods` names (header there).

A calendar entry tagged conventions:<YYYY>-<R|D> (the convention's opening, beside the party's primaries) carries the
delegations: a summary, a map of the States by how they chose their delegates (Chosen), a map by the leader on the
first ballot (First ballot), keys, and a table (each delegation's votes, the Call's apportionment, how and when it was
chosen, its first-ballot vote). An entry tagged rollcall:<YYYY>-<R|D>-<ballot> (the nomination) carries that roll call,
State by State, as the Proceedings tabulate it.

STYLE
 1. Figures as the Proceedings print them: the Call's apportionment (delegates at large, two a district, the total),
    the tabulations' columns, in their order, with their surnames ("N. Rockefeller", "W. Rockefeller"); the full name
    (`names`) in the tables, linked to the name entry where one person fits (namelinks.written). "Not voting" is a
    column, not a person.
 2. Cites: the figures once, under each table, by the Proceedings' pages, linked to the page of the copy read: the
    Call and its apportionment, the roll call and the tabulation. The methods and dates of choosing, by their source,
    with its Check; a State's own Check in its row's note.
 3. Methods (the map's Chosen): primary (every delegate chosen in a primary), mixed (the districts' delegates in a
    primary, those at large by a convention or a committee), conventions (district conventions and a State
    convention), convention (a State convention alone), committee (a State committee alone), not found. A primary's
    date links to the calendar's entry for the day (primary:<date>). Whether a primary bound its delegates is not
    settled here: the Check.
 4. The first-ballot map: each State by the candidate with the most votes in its delegation, as first tabulated
    (before the changes after the roll); a color a candidate, in order of delegations led, then votes; a tie gray.
    Puerto Rico and the Virgin Islands are not drawn: the table holds them. The District of Columbia is a dot.
 5. A roll call's table: the State, its votes by candidate as first tabulated, the delegation's votes, and in the note
    the final tabulation where it differs ("Final: Nixon 26.") and the Proceedings' note on a starred State, quoted;
    the totals last, as printed.
 6. check (problems): the Call's at_large + 2 x districts = votes; the votes add to the Call's total; each State's
    ballot adds to its votes, every name a column; the columns add to the printed totals (the final tabulation too,
    the States not listed counted all for the nominee); a method in the list; a date in the convention's year or the
    year before; the calendar's tags answer.
"""
import json
import os
import re
from collections import Counter

from . import store

PATH = os.path.join(store.ROOT, "elections", "conventions.yaml")
PARTY = {"R": "Republican", "D": "Democratic"}
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
METHODS = [("primary", "q1", "In a primary"),
           ("mixed", "q5", "The districts' delegates in a primary, those at large otherwise"),
           ("conventions", "q3", "District and State conventions"),
           ("convention", "q2", "A State convention"),
           ("committee", "q4", "A State committee"),
           (None, "qU", "Not found")]
FILL = {m: f for m, f, _ in METHODS}
LABEL = {m: t for m, _, t in METHODS}
EXTRA = {"DC": "District of Columbia", "PR": "Puerto Rico", "VI": "Virgin Islands"}
NOT_A_PERSON = ("Not voting",)
FILLS = 9
STYLE = """<style id="cv-css">
.cv details.cgr.er .ec{grid-template-columns:minmax(0,1fr) 3.2em}
.cv details.cgr.er tr.cvt td{font-weight:700;border-top:1px solid var(--rule)}
.cv .cvq{display:block;margin-top:.15rem}
</style>"""
_C = {}


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def txt(t):
    """Page text: & < > escaped, quotation marks left for the build to curl (smart.py)."""
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load():
    if "d" not in _C:
        _C["d"] = (store.load_yaml(PATH) or {}) if os.path.exists(PATH) else {}
    return _C["d"]


def fmt_date(d, year=True):
    y, m, dd = str(d).split("-")
    return f"{MONTHS[int(m) - 1]} {int(dd)}" + (f", {y}" if year else "")


def days(ds, links=None):
    """'Mar. 9, 16, 23, 30, Apr. 6': the month written once for its days; each day linked where links holds it."""
    out, last = [], None
    for d in ds:
        y, m, dd = str(d).split("-")
        t = f"{int(dd)}" if m == last else f"{MONTHS[int(m) - 1]} {int(dd)}"
        last = m
        if links and str(d) in links:
            t = f'<a href="{esc(links[str(d)])}">{t}</a>'
        out.append(t)
    return ", ".join(out)


def state_name(st):
    from .congress import STATE
    return EXTRA.get(st) or STATE.get(st, st)


def page_link(C, p, text=None):
    """A page of the Proceedings, linked to the copy read ('17' or '17–19': the first page)."""
    first = str(p).split("–")[0]
    url = C["proc"].get("page_url", "").replace("{p}", first)
    return f'<a href="{esc(url)}">{esc(text or p)}</a>' if url else esc(text or p)


def proc_cite(C, pages):
    t = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", esc(C["proc"]["title"]))
    return f'<a href="{esc(C["proc"]["url"])}">{t}</a> ({esc(C["proc"]["year"])}) {page_link(C, pages)}'


SERIES = None


def full(C, n):
    return (C.get("names") or {}).get(n, n)


def name_html(C, n):
    """The full name (STYLE 1), linked to the name entry where one person fits."""
    w = full(C, n)
    if SERIES is None or n in NOT_A_PERSON or " " not in w:
        return esc(w)
    from . import namelinks
    p = namelinks.written(SERIES, w)
    return f'<a class="nm" href="{esc(namelinks.url(SERIES, p))}">{esc(w)}</a>' if p else esc(w)


def ordered(B, v):
    """A State's votes in the tabulation's column order."""
    return [(c, v[c]) for c in B["cands"] if v.get(c)]


def cands_html(C, B, v, lead=None):
    out = []
    for c, n in ordered(B, v):
        cls = ' class="w"' if c == lead else ""
        out.append(f'<span class="ec"><span{cls}><span class="en">{name_html(C, c)}</span></span>'
                   f'<span class="ev">{n:,}</span></span>')
    return "".join(out)


def leader(B, v):
    """The candidate with the most votes in the delegation; None at a tie."""
    vs = sorted(((n, c) for c, n in v.items() if c not in NOT_A_PERSON), reverse=True)
    if not vs or (len(vs) > 1 and vs[0][0] == vs[1][0]):
        return None
    return vs[0][1]


def final_votes(C, B, st):
    """A State's votes in the final tabulation: as listed, else all for the nominee (the first column of its totals)."""
    F = B.get("final")
    if not F:
        return None
    if st in (F.get("votes") or {}):
        return F["votes"][st]
    top = max(F["totals"], key=lambda c: F["totals"][c])
    return {top: C["states"][st]["votes"]}


def rid(key, st, b=None):
    return f"pqcv{key.replace('-', '')}-" + (f"{b}-" if b else "") + st


def chosen_html(C, s, links):
    bits = []
    for x in s.get("chosen") or []:
        by = x["by"]
        lk = links if by.startswith("primary") else None
        bits.append(f'{esc(by[:1].upper() + by[1:])}, {days(x.get("dates") or [], lk)}')
    return "; ".join(bits) + "." if bits else "Not found."


def apport(s):
    if s["districts"]:
        return f'{s["at_large"]} at large, 2 from each of {s["districts"]} districts.'
    return f'{s["at_large"]} at large.'


def table_head(h, cols):
    return ('<table><colgroup><col class="c1"><col class="c2"><col class="c3"><col class="c4"></colgroup>'
            f'<thead><tr><th>{h}</th><th>{cols[0]}</th><th>{cols[1]}</th><th>{cols[2]}</th></tr></thead><tbody>')


def figure(cap, q, info, rows):
    seats = json.dumps({"q": q}, ensure_ascii=False, separators=(",", ":"))
    return (f'<script type="application/json" class="cgseats">{seats}</script>'
            f'<div class="cgmaps"><figure class="cgmap" data-chamber="q" data-info="{esc(info)}" data-rows="{esc(rows)}" '
            f'data-none="no delegation"><figcaption>{esc(cap)}</figcaption>'
            f'<div class="cgv" style="aspect-ratio:960/660"></div></figure></div><span data-views="r"></span>')


def key_html(items, tail=""):
    k = " ".join(f'<span class="pqi"><span class="sw {f}"></span>{t}</span>' for f, t in items)
    return f'<p class="cgkey elkey"><span class="lk lk-r lk-s">{k}</span>{tail}</p>'


def block(key, links=None):
    """The delegations: summary, the two maps, keys, the table (the entry tagged conventions:<key>)."""
    C = load().get(key)
    if not C:
        return ""
    from .smart import smarten          # map data is not page text: curled here
    y, p = key.split("-")
    S = C["states"]
    B = C["ballots"].get("pres1") or next(iter(C["ballots"].values()))
    total = sum(s["votes"] for s in S.values())
    need = total // 2 + 1
    n = len(S)
    # summary
    by = Counter(s.get("method") for s in S.values())
    vby = Counter()
    for s in S.values():
        vby[s.get("method")] += s["votes"]
    summary = [f'The Call, {fmt_date(C["call"]["issued"])}: {total:,} delegates, a vote each; {need:,} a majority. '
               f'{n} delegations: the States, the District of Columbia, Puerto Rico and the Virgin Islands.']
    summary.append("Chosen: " + "; ".join(f'{LABEL[m][:1].lower() + LABEL[m][1:]}, {by[m]} ({vby[m]:,} votes)'
                                          for m, _, _ in METHODS if by[m]) + ".")
    tot = B["totals"]
    lead = Counter()
    for st, v in B["votes"].items():
        lead[leader(B, v) or "tie"] += 1
    summary.append(f'{B["title"]}: ' + "; ".join(f"{full(C, c)} {tot[c]:,}" for c in sorted(tot, key=lambda c: -tot[c])
                                                 if tot[c] and c not in NOT_A_PERSON) + ".")
    # maps
    q1, q2 = {}, {}
    order = sorted((c for c in lead if c != "tie"), key=lambda c: (-lead[c], -tot.get(c, 0)))
    fills = {c: (f"q{i + 1}" if i < FILLS else "pO") for i, c in enumerate(order)}
    for st, s in S.items():
        m = s.get("method")
        ch = "; ".join(f'{x["by"]}, {days(x.get("dates") or [])}' for x in s.get("chosen") or []) or "not found"
        q1[st] = {"id": rid(key, st), "f": FILL.get(m, "qU"), "mg": 100,
                  "t": smarten(f'{st}, {s["votes"]} votes: {ch}')}
        v = B["votes"].get(st) or {}
        ld = leader(B, v)
        q2[st] = {"id": rid(key, st), "f": fills.get(ld, "qU"), "mg": 100,
                  "t": smarten(f'{st}: ' + ", ".join(f"{c} {k}" for c, k in ordered(B, v)))}
    k1 = key_html([(f, t) for m, f, t in METHODS if by[m]],
                  ' <span class="lk lk-r lk-s">Puerto Rico and the Virgin Islands: the table.</span>')
    k2 = key_html([(fills[c], f"{esc(full(C, c))} {lead[c]}") for c in order]
                  + ([("qU", f'Tied {lead["tie"]}')] if lead["tie"] else []),
                  ' <span class="lk lk-r lk-s">The candidate with the most of the delegation\'s votes, as first tabulated.</span>')
    # the table
    rows = []
    for st, s in S.items():
        v = B["votes"].get(st) or {}
        note = f'{apport(s)} {chosen_html(C, s, links)}' + (f' Check: {esc(s["check"])}' if s.get("check") else "")
        rows.append(f'<tr id="{rid(key, st)}"><td><span title="{esc(state_name(st))}">{esc(st)}</span></td>'
                    f'<td class="ecs">{cands_html(C, B, v, leader(B, v))}</td><td class="em">{s["votes"]}</td>'
                    f'<td class="eno">{note}</td></tr>')
    M = C["methods"]
    src = (f'The Call ({fmt_date(C["call"]["issued"])}), {proc_cite(C, C["call"]["pages"])}; the apportionment '
           f'{page_link(C, C["call"]["table"])}, its total {C["call"]["total"]:,}'
           + (", the sum of the States'" if C["call"]["total"] == total else f"; the States add to {total:,}")
           + f'. {esc(B["title"])}: {page_link(C, B["table"])}. How and when chosen: '
           f'<a href="{esc(M["url"])}">{txt(M["cite"])}</a>, read {fmt_date(M["read"])}. '
           f'Check: {re.sub(r"[*]([^*]+)[*]", r"<i>\1</i>", txt(M["check"]))}.')
    name = f'{PARTY[p]} National Convention, {y}'
    return (f'<div class="cv">'
            f'<div class="cg el pq" data-cg="pqcv{y}{p}" id="pqcv{y}{p}">'
            f'<p class="cgh">The delegations: {esc(name)}</p>'
            + "".join(f'<p class="elsum">{s}</p>' for s in map(esc, summary))
            + figure(f"Delegations, {y}, by how chosen", q1, "Click a State for its delegation.", "Delegation ↓")
            + k1 + "</div>"
            f'<div class="cg el pq" data-cg="pqcb{y}{p}" id="pqcb{y}{p}">'
            + figure(f"{B['title']}, the leader by State", q2, "Click a State for its delegation.", "Delegation ↓")
            + k2 +
            f'<details class="cgr er esp"><summary>Delegations, {n}</summary>'
            + table_head("State", ("First ballot", "Votes", "Chosen")) + "".join(rows) + "</tbody></table></details>"
            f'<p class="elsrc">{src}</p></div></div>')


def rollcall(key, bkey):
    """A roll call by State (the entry tagged rollcall:<key>-<bkey>)."""
    C = load().get(key)
    B = (C or {}).get("ballots", {}).get(bkey)
    if not B:
        return ""
    S = C["states"]
    F = B.get("final")
    rows = []
    for st, s in S.items():
        v = B["votes"].get(st) or {}
        bits = []
        fv = final_votes(C, B, st)
        if fv is not None and fv != v:
            bits.append("Final: " + ", ".join(f"{esc(c)} {k}" for c, k in ordered(B, fv)) + ".")
        for star in (B.get("star"), (F or {}).get("star")):
            if star and star["st"] == st:
                bits.append(f'<span class="cvq">{page_link(C, star["page"], "Proceedings " + str(star["page"]))}: '
                            f'"{txt(star["text"])}"</span>')
        rows.append(f'<tr id="{rid(key, st, bkey)}"><td><span title="{esc(state_name(st))}">{esc(st)}</span></td>'
                    f'<td class="ecs">{cands_html(C, B, v, leader(B, v))}</td><td class="em">{s["votes"]}</td>'
                    f'<td class="eno">{" ".join(bits)}</td></tr>')
    total = sum(s["votes"] for s in S.values())
    tv = {c: n for c, n in B["totals"].items()}
    rows.append(f'<tr class="cvt"><td>Total</td><td class="ecs">{cands_html(C, B, tv)}</td><td class="em">{total:,}</td>'
                f'<td class="eno">' + ("Final: " + ", ".join(f"{esc(c)} {k:,}" for c, k in
                                                                ordered(B, F["totals"])) + "." if F else "") + '</td></tr>')
    y, p = key.split("-")
    summary = [f'{B["title"]}, the {esc(B["session"][0].lower())} ({fmt_date(B["session"][1])}): {total:,} votes, '
               f'{B["needed"]:,} needed. '
               + "; ".join(f"{esc(full(C, c))} {n:,}" for c, n in sorted(tv.items(), key=lambda x: -x[1]) if n) + "."]
    if F:
        summary.append(f'{esc(F["title"])}, after the delegations changed their votes: '
                       + "; ".join(f"{esc(full(C, c))} {n:,}" for c, n in sorted(F["totals"].items(), key=lambda x: -x[1]) if n) + ".")
    src = (f'{proc_cite(C, B["pages"])}: the roll call; {esc(B["title"])}, {page_link(C, B["table"])}'
           + (f'; the changes, {page_link(C, F["pages"])}; {esc(F["title"])}, {page_link(C, F["table"])}' if F else "")
           + ". As printed; each State's votes add to its delegation's, the columns to the printed totals.")
    return (f'<div class="cv"><div class="cg sprace pq"><details class="cgr er esp" open><summary>{esc(B["office"])}: '
            f'the roll call, {PARTY[p]} National Convention, {y}</summary>'
            + "".join(f'<p class="elsum">{s}</p>' for s in summary)
            + table_head("State", ("Votes", "Delegation", "Note")) + "".join(rows) +
            f'</tbody></table></details><p class="elsrc">{src}</p></div></div>')


def tagged(series):
    """{('conv', key) | ('roll', (key, ballot)): entry id}."""
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^conventions:(\d{4}-[RD])$", t)
                if m:
                    out[("conv", m.group(1))] = e["id"]
                m = re.match(r"^rollcall:(\d{4}-[RD])-(\w+)$", t)
                if m:
                    out[("roll", (m.group(1), m.group(2)))] = e["id"]
    return out


def inject(page, series):
    """Put the tagged entries' blocks into a built page (after primaries.inject, whose assets the maps share)."""
    global SERIES
    SERIES = series
    tags = tagged(series)
    if not tags:
        return page
    from . import primaries
    links = {k[1]: f"#{eid}" for k, eid in primaries.tagged(series).items() if k[0] == "day"}
    used = False
    for (k, v), eid in tags.items():
        blk = block(v, links) if k == "conv" else rollcall(*v)
        if not blk:
            continue
        pat = re.compile(r'(<li id="' + re.escape(eid) + r'"[^>]*>.*?)(</li>)', re.S)
        page, n = pat.subn(lambda mm: mm.group(1) + blk + mm.group(2), page, count=1)
        used = used or bool(n)
    if not used:
        return page
    if 'id="cv-css"' not in page:
        page = page.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="cggeo"' not in page:
        from . import congress
        data, geo = congress.load()
        if geo:
            page = page.replace("</body>", congress.assets(congress.geo_subset(geo, [])) + "\n</body>", 1)
    from . import roster
    return roster.ensure(page)


def problems(series=None):
    """STYLE 6."""
    where = "elections/conventions.yaml"
    out = []
    methods = {m for m, _, _ in METHODS}
    for key, C in load().items():
        if not re.fullmatch(r"\d{4}-[RD]", str(key)):
            out.append((where, f"{key}: not <YYYY>-<R|D>"))
            continue
        y = int(key[:4])
        S = C.get("states") or {}
        from .congress import STATE
        for st, s in S.items():
            if st not in STATE and st not in EXTRA:
                out.append((where, f"{key} {st}: not a State"))
            if s.get("at_large", 0) + 2 * s.get("districts", 0) != s.get("votes"):
                out.append((where, f"{key} {st}: {s.get('at_large')} at large + 2 x {s.get('districts')} is not {s.get('votes')}"))
            if s.get("method") not in methods:
                out.append((where, f"{key} {st}: method {s.get('method')!r} not in the list"))
            for x in s.get("chosen") or []:
                for d in x.get("dates") or []:
                    if not re.fullmatch(rf"({y}|{y - 1})-\d\d-\d\d", str(d)):
                        out.append((where, f"{key} {st}: date {d} not in {y - 1} or {y}"))
        total = sum(s.get("votes", 0) for s in S.values())
        if (C.get("call") or {}).get("total") not in (None, total):
            out.append((where, f"{key}: the States add to {total:,}, the Call prints {C['call']['total']:,}"))
        for bk, B in (C.get("ballots") or {}).items():
            cands = B.get("cands") or []
            V = B.get("votes") or {}
            if set(V) != set(S):
                out.append((where, f"{key} {bk}: States {sorted(set(S) ^ set(V))} not in both the Call and the ballot"))
            for st, v in V.items():
                bad = [c for c in v if c not in cands]
                if bad:
                    out.append((where, f"{key} {bk} {st}: {bad} not a column"))
                if st in S and sum(v.values()) != S[st]["votes"]:
                    out.append((where, f"{key} {bk} {st}: votes add to {sum(v.values())}, the delegation has {S[st]['votes']}"))
            for c in cands:
                got = sum(v.get(c, 0) for v in V.values())
                if (B.get("totals") or {}).get(c, 0) != got:
                    out.append((where, f"{key} {bk}: {c} adds to {got}, printed {(B.get('totals') or {}).get(c, 0)}"))
            F = B.get("final")
            if F:
                for st, v in (F.get("votes") or {}).items():
                    if st in S and sum(v.values()) != S[st]["votes"]:
                        out.append((where, f"{key} {bk} final {st}: votes add to {sum(v.values())}, not {S[st]['votes']}"))
                for c, n in F["totals"].items():
                    got = sum((final_votes(C, B, st) or {}).get(c, 0) for st in S)
                    if got != n:
                        out.append((where, f"{key} {bk} final: {c} adds to {got}, printed {n}"))
            for star in (B.get("star"), (F or {}).get("star")):
                if star and star.get("st") not in S:
                    out.append((where, f"{key} {bk}: star on {star.get('st')}, not a delegation"))
    if series is not None:
        for (k, v), eid in tagged(series).items():
            if k == "conv" and v not in load():
                out.append((eid, f"conventions:{v}: no such convention"))
            if k == "roll" and v[1] not in ((load().get(v[0]) or {}).get("ballots") or {}):
                out.append((eid, f"rollcall:{v[0]}-{v[1]}: no such roll call"))
    return out
