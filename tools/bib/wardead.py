"""The war's dead by home State: sources/war-dead-states.yaml (written by tools/indicators/make_war.py from NARA's
Defense Casualty Analysis System file and the Census Bureau's estimates of the States' populations).

A calendar entry tagged wardead:<span> (wardead:1961-1964, wardead:1965 ... wardead:1968) carries that span's map and
table, drawn with the series' State maps (drawQ in templates/congress.html, one view).

STYLE
 1. The rate: deaths from all causes, by the home of record's State and the year of the incident or death, per
    100,000 people of the State (the Census Bureau's estimate for July 1 of the year; for 1961-64, the four years
    together over the mean of the four estimates). One decimal.
 2. The map: one neutral ramp, near white (--rW) to the amber of the margin maps' third color (--rA), straight in
    OKLab, on one scale for every span, zero to the highest rate of any State in any span, so the years compare;
    the key a gradient bar with its ends. No party colors: the dead have none.
 3. The summary: the span's dead with a home of record in the States and the District, the hostile among them, the
    rate for the whole; the three highest and three lowest rates, by State, as figures; the dead not mapped (Puerto
    Rico, Guam, the Virgin Islands, other territories, a home abroad, none recorded), by place.
 4. The table: by State (postal code, the name on hover): dead, hostile, population (thousands), rate. Row ids begin
    "cgwd" so a link to a row opens the table (the template's handler for "#cg...").
 5. The dead are not persons in the series: the file names every man; nothing but counts leaves it.
"""
import json
import os
import re

from . import contents, store

PATH = os.path.join(store.ROOT, "sources", "war-dead-states.yaml")
PLACE = {"PR": "Puerto Rico", "GU": "Guam", "VI": "Virgin Islands", "AS": "American Samoa", "CZ": "Canal Zone",
         "FR": "home of record coded FR", "ON": "home of record coded ON", "foreign": "a home abroad",
         "?": "no State recorded"}
_C = {}


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def load():
    if "d" not in _C:
        _C["d"] = store.load_yaml(PATH) if os.path.exists(PATH) else {}
    return _C["d"] or {}


def spans():
    return {str(k): v for k, v in (load().get("spans") or {}).items()}


def rate(rec):
    return rec["all"] * 100.0 / rec["pop"] if rec.get("pop") else None


def top():
    """The highest rate of any State in any span: the map's one scale."""
    return max((rate(r) or 0) for S in spans().values() for r in (S.get("states") or {}).values()) or 1.0


def label(span):
    return span.replace("-", "–")


def fill(r, hi):
    t = max(0.0, min(1.0, (r or 0) / hi))
    return f"v:color-mix(in oklab,var(--rA) {100 * t:.1f}%,var(--rW))"


def summary(span, S):
    from .congress import STATE
    st = S.get("states") or {}
    dead = sum(r["all"] for r in st.values())
    host = sum(r["hostile"] for r in st.values())
    pop = sum(r["pop"] for r in st.values())
    rated = sorted(((rate(r), k) for k, r in st.items()), reverse=True)
    name = lambda k: STATE.get(k, k)
    hi = "; ".join(f"{name(k)}, {v:.1f}" for v, k in rated[:3])
    lo = "; ".join(f"{name(k)}, {v:.1f}" for v, k in rated[-3:][::-1])
    out = [f"{label(span)}: {dead:,} dead with a home of record in the States and the District, {host:,} of them of "
           f"hostile causes; {dead * 100.0 / pop:.1f} per 100,000 people" + (" in the four years." if "-" in span else "."),
           f"Highest: {hi}. Lowest: {lo}."]
    el = S.get("elsewhere") or {}
    if el:
        out.append("Not mapped: " + "; ".join(f"{PLACE.get(str(k), str(k))}, {v:,}" for k, v in el.items()) + ".")
    return out


def block(span):
    from .congress import STATE
    from .smart import smarten
    S = spans().get(span)
    if not S:
        return ""
    hi = top()
    key = span.replace("-", "_")
    q, rows = {}, []
    for st, r in sorted((S.get("states") or {}).items()):
        rt = rate(r)
        rid = f"cgwd{key}-{st}"
        q[st] = {"id": rid, "f": fill(rt, hi), "mg": 0,
                 "t": smarten(f"{STATE.get(st, st)}, {label(span)}: {r['all']:,} dead, {r['hostile']:,} hostile; "
                              f"{rt:.1f} per 100,000")}
        rows.append(f'<tbody id="{rid}"><tr class="gvr"><td><span title="{esc(STATE.get(st, st))}">{esc(st)}</span></td>'
                    f'<td class="num">{r["all"]:,}</td><td class="num">{r["hostile"]:,}</td>'
                    f'<td class="num">{r["pop"]:,.0f}</td><td class="num">{rt:.1f}</td></tr></tbody>')
    seats = json.dumps({"q": q}, ensure_ascii=False, separators=(",", ":"))
    keybar = (f'<p class="cgkey elkey"><span class="pqi">Per 100,000 people: 0 '
              f'<span class="sw" style="display:inline-block;width:8em;height:.8em;vertical-align:middle;'
              f'background:linear-gradient(to right,var(--rW),var(--rA))"></span> {hi:.1f}</span></p>')
    src, pop = load().get("source") or {}, load().get("population") or {}
    srcline = (f'Deaths: <a href="{esc(src.get("url", ""))}">{esc(src.get("title", ""))}</a> '
               f'(<a href="{esc(src.get("layout", ""))}">layout</a>), by home of record and the year of the incident '
               f'or death. Populations: <a href="{esc(pop.get("url", ""))}">{esc(pop.get("title", ""))}</a>'
               + (", the mean of the four years" if "-" in span else "") + ". One scale for every year.")
    return (f'<div class="cg el pq wd" data-cg="wd{key}" id="wd{key}"><p class="cgh">The dead by home State, '
            f'{label(span)}</p>' + "".join(f'<p class="elsum">{esc(smarten(s))}</p>' for s in summary(span, S))
            + f'<script type="application/json" class="cgseats">{seats}</script>'
            f'<div class="cgmaps"><figure class="cgmap" data-chamber="q" data-none="no figure" '
            f'data-info="Click a State for its dead." data-rows="Figures ↓">'
            f'<figcaption>Deaths per 100,000 people, {label(span)}</figcaption>'
            f'<div class="cgv" style="aspect-ratio:960/660"></div></figure></div><span data-views="r"></span>{keybar}'
            f'<details class="cgr er esp"><summary>The dead by State, {label(span)}</summary>'
            '<table><thead><tr><th>State</th><th>Dead</th><th>Hostile</th><th>Population (000)</th>'
            '<th>Per 100,000</th></tr></thead>' + "".join(rows)
            + f'</table></details><p class="elsrc">{srcline}</p></div>')


def tagged(series):
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^wardead:(\d{4}(?:-\d{4})?)$", t)
                if m:
                    out[m.group(1)] = e["id"]
    return out


def inject(page, series):
    used = False
    for span, eid in tagged(series).items():
        blk = block(span)
        if not blk:
            continue
        page, k = contents.put(page, eid, blk, "wardead", span)
        used = used or bool(k)
    if used and 'id="cggeo"' not in page:
        from . import congress
        data, geo = congress.load()
        if geo:
            page = page.replace("</body>", congress.assets(congress.geo_subset(geo, [])) + "\n</body>", 1)
    if used:
        from . import roster
        page = roster.ensure(page)
    return page


def problems(series=None):
    out = []
    for span, S in spans().items():
        st = S.get("states") or {}
        if len(st) != 51:
            out.append(("sources/war-dead-states.yaml", f"{span}: {len(st)} States and the District, not 51"))
        for k, r in st.items():
            if r.get("hostile", 0) > r.get("all", 0) or not r.get("pop"):
                out.append(("sources/war-dead-states.yaml", f"{span} {k}: hostile over all, or no population"))
    if series is not None:
        for span, eid in tagged(series).items():
            if span not in spans():
                out.append((eid, f"wardead:{span}: no such span in sources/war-dead-states.yaml"))
    return out
