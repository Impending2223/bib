"""The world's oil a year, 1960-68, and the posted prices of crude: sources/oil-world.yaml (kept by hand; its header
has the schema and the sources).

    oilworld:<YYYY>        a calendar entry so tagged (the year's December entry in the Oil thread) carries the year's
                           table: crude production by country as the Bureau of Mines' Minerals Yearbook for the year
                           printed it, and, where the Oil and Gas Journal's year-end table is open (1960, 1961), proved
                           reserves.
    oilprice:ras-tanura    the entry so tagged (Esso Export's cut, Aug. 9, 1960) carries the posted prices, each dated.

Both kinds are registered in contents.KINDS ("oilworld", "oilprice"), so the contents and the Oil thread's statement
list them. Not indicator series: a year's table and a list of dated postings, not a monthly row, so they have no
statement in indicators/concepts.yaml; what each table counts is said under it, from its own source.

STYLE (settled; keep it):
 1. Production in millions of barrels a day, two decimals, the year's barrels over its days (366 in 1960, 1964, 1968),
    as the Oil table's (oil.py STYLE 1); the Yearbook's own figure, thousand barrels in the year, on hover. "e" in grey
    after a figure the table marks an estimate.
 2. Columns: Country | m b/d | Change | Share, and Reserves (bn bbl, one decimal) only in a year whose reserves are read
    (no vacant columns: the owner's ruling, Oct. 21, 2026). Change: percent from the year before as the same table
    printed it (revised), one decimal, U+2212 for a fall; "new" where the table prints no figure the year before.
    Share: percent of the table's world total. Four or five columns: a 400px phone holds them without sideways scroll;
    the country's name wraps.
 3. Rows: the countries kept (the Persian Gulf, the Caribbean, the Sahara and Libya, the Soviet Union, the United
    States and its neighbors, Indonesia, Nigeria) by production that year, largest first; then "Others" (the world
    total less them) and "World" (the table's printed total), bold. A country with no production that year has no row.
    Labels: the Yearbook's countries in the series' forms ("Soviet Union", "Neutral Zone", "Trucial States (Abu
    Dhabi)"); what a row holds that its name does not say (the Soviet Union in Asia, the Sahara, West Irian, the Neutral
    Zone printed apart) in a note under the table, only for the rows shown.
 4. Today: no open series found counts crude oil by country for the 1960s in barrels (the Energy Institute's
    Statistical Review, from 1965, counts natural gas liquids with crude and is bot-checked here; Our World in Data's
    copy, "Oil production", is in terawatt-hours, crude and liquids together). So no "today" column. For the United States,
    EIA's annual figure today is the Bureau's final count; where it differs from the Yearbook's preliminary one, a note
    under the table gives it.
 5. Under the table: the notes, then the sources, linked to archive.org's page (the Yearbook's volume, table and
    printed pages; the Journal's issue and pages).
 6. The posted prices: a table a crude (Arabian light, 34 degrees, f.o.b. Ras Tanura; Venezuela's Oficina, 35 degrees,
    f.o.b. Puerto La Cruz), stacked: Date | $ a bbl | Source. A change ("Esso Export: $1.90 to $1.76") and a reading
    of the price in force ("quoted") are rows alike, the kind in the price cell; the posting's dates of change only,
    not a monthly row. The source's short form in the cell, linked, the full citation and any note on hover.
"""
import calendar
import os
import re

from . import contents, store

PATH = os.path.join(store.ROOT, "sources", "oil-world.yaml")
ARCHIVE = "https://archive.org/details/{item}/page/n{leaf}"
EIA_US = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=MCRFPUS1&f=A"
MINUS = "−"
NAMES = {"us": "United States", "ussr": "Soviet Union", "venezuela": "Venezuela", "saudi": "Saudi Arabia",
         "kuwait": "Kuwait", "iran": "Iran", "iraq": "Iraq", "libya": "Libya", "canada": "Canada",
         "indonesia": "Indonesia", "algeria": "Algeria", "nigeria": "Nigeria", "qatar": "Qatar",
         "trucial": "Trucial States (Abu Dhabi)", "mexico": "Mexico", "neutral": "Neutral Zone"}
NOTES = {
    "ussr": "Soviet Union: with the Soviet Union in Asia (Sakhalin included).",
    "algeria": "Algeria: with the Sahara.",
    "neutral": "Neutral Zone: the Kuwait–Saudi Arabia Neutral Zone, printed apart from both.",
    "trucial": "Trucial States: Abu Dhabi alone; Dubai's Fateh field was to produce from late 1969 (*Minerals Yearbook* "
               "1968, IV, 950–951).",
}
INDONESIA_WI = "Indonesia: with West Irian, transferred May 1, 1963 (the table's note)."
STYLE = """<style id="owstyle">
.ow{margin:1rem 0 .5rem;font-family:var(--sans)}
.ow .owh{font-weight:700;font-size:.95rem;margin:.2rem 0 .4rem}
.ow .owh2{margin-top:1.1rem}
.ow table{border-collapse:collapse;width:100%;font-size:.78rem;font-variant-numeric:tabular-nums;line-height:1.35}
.ow th,.ow td{text-align:right;padding:.18rem 0 .18rem .6rem;vertical-align:bottom;border-bottom:1px solid var(--rule);
  white-space:nowrap}
.ow th:first-child,.ow td:first-child{text-align:left;padding-left:0;white-space:normal}
.ow thead th{font-weight:600;color:var(--muted);font-size:.74rem;line-height:1.25;white-space:normal}
.ow tr.owt td{font-weight:700}
.ow tr.owo td{color:var(--muted)}
.ow .owe{color:var(--muted);font-size:.7rem;margin-left:.1em}
.ow td.owsrc,.ow th.owsrc{white-space:normal;text-align:left;color:var(--muted)}
.ow table.owp td:first-child{min-width:5.4rem}
.ow table.owp td.owf{white-space:normal}
.ow .own{font-size:.78rem;line-height:1.45;color:var(--note);margin:.3rem 0}
.ow .owsrcs{font-size:.78rem;color:var(--muted);line-height:1.4;margin:.3rem 0}
</style>"""
_C = {}


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def ital(t):
    return re.sub(r"\*([^*]+)\*", r"<i>\1</i>", esc(t))


def load():
    if "d" not in _C:
        _C["d"] = (store.load_yaml(PATH) if os.path.exists(PATH) else None) or {}
    return _C["d"]


def years():
    return {int(r["year"]): r for r in load().get("production") or []}


def reserves():
    return {int(r["year"]): r for r in load().get("reserves") or []}


def _days(y):
    return 366 if calendar.isleap(int(y)) else 365


def mbd(v, y):
    return v / _days(y) / 1000.0


def _signed(x, nd=1):
    s = f"{abs(x):.{nd}f}"
    return (MINUS + s) if round(x, nd) < 0 else ("+" + s if round(x, nd) > 0 else s)


def _date(d):
    d = str(d)
    mon = contents.MONTHS
    if len(d) == 7:
        return f"{mon[int(d[5:7]) - 1]} {d[:4]}"
    return f"{mon[int(d[5:7]) - 1]} {int(d[8:10])}, {d[:4]}"


def label(year):
    return f"World oil, {year}"


# ---------------------------------------------------------------- the year's table (STYLE 1-5)

def block(year):
    from .smart import smarten
    Y = years().get(int(year))
    if not Y:
        return ""
    y = int(year)
    prod, prior, world = Y.get("production") or {}, Y.get("prior") or {}, Y["world"]
    est = set(Y.get("estimate") or [])
    R = reserves().get(y)
    rc = (R or {}).get("countries") or {}
    rworld = (R["free_world"] + R["bloc"]) if R else None
    rows = sorted(prod, key=lambda k: -prod[k])
    head = ["Country", "m b/d", "Change, %", "Share, %"] + (["Reserves, bn bbl"] if R else [])
    body = []

    def cells(name, v, pv, rv, cls="", tip="", e=False):
        ch = (_signed((v / pv - 1) * 100) if pv else "new") if v is not None else "—"
        out = (f'<td>{name}</td><td><span title="{esc(tip)}">{mbd(v, y):.2f}</span>'
               + ('<span class="owe">e</span>' if e else "") + f'</td><td>{ch}</td><td>{v * 100.0 / world:.1f}</td>')
        if R:
            out += f'<td>{rv / 1e6:.1f}</td>' if rv is not None else '<td>—</td>'
        return f'<tr{cls}>{out}</tr>'
    for k in rows:
        v = prod[k]
        body.append(cells(esc(NAMES[k]), v, prior.get(k), rc.get(k) if R else None,
                          tip=f"{v:,} thousand barrels in {y}" + (", estimate" if k in est else ""), e=k in est))
    others, pothers = world - sum(prod.values()), Y["prior_world"] - sum(prior.values())
    rothers = (rworld - sum(rc.values())) if R else None
    body.append(cells("Others", others, pothers, rothers, cls=' class="owo"', tip=f"{others:,} thousand barrels"))
    body.append(cells("World", world, Y["prior_world"], rworld, cls=' class="owt"', tip=f"{world:,} thousand barrels"))
    notes = [NOTES[k] for k in ("ussr", "algeria", "neutral", "trucial") if k in prod]
    if y >= 1964:
        notes.append(INDONESIA_WI)
    if est:
        notes.append("e: the table's estimate.")
    us_now = Y.get("us_today")
    if us_now and us_now != prod.get("us"):
        notes.append(f"United States: EIA's figure today, the Bureau's final count, {us_now:,} thousand barrels "
                     f"({mbd(us_now, y):.2f}m b/d); the Yearbook's preliminary, {prod['us']:,}.")
    if R:
        notes.append(f"Reserves: the *Oil and Gas Journal*'s year-end estimates, proved, by country; the world, its free "
                     f"world ({R['free_world'] / 1e6:.1f}bn) and “Russia and controlled areas” "
                     f"({R['bloc'] / 1e6:.1f}bn), the Soviet Union from the latter's footnote.")
    url = ARCHIVE.format(item=Y["item"], leaf=Y["leaf"])
    pp = Y["pages"]
    src = (f'Production: Bureau of Mines, <a href="{esc(url)}"><i>Minerals Yearbook {y}</i>, {esc(Y["volume"])}, '
           f'Table {Y["table"]}, {"pp." if "–" in str(pp) else "p."} {esc(pp)}</a> ({esc(Y["released"])}), '
           f'“World production of crude petroleum by countries,” the year preliminary, the year before '
           f'revised; the year’s barrels over its {_days(y)} days. ')
    if us_now and us_now != prod.get("us"):
        src += f'Today: <a href="{EIA_US}">EIA, U.S. field production of crude oil</a>. '
    if R:
        src += f'Reserves: <a href="{esc(R["url"])}">{ital(_ogj(R["source"]))}</a>.'
    title = f"World crude oil, {y}: production by country as the Minerals Yearbook first printed it" + (
        ", and proved reserves" if R else "")
    return (f'<div class="ow" id="ow{y}"><p class="owh">{esc(smarten(title))}</p><table><thead><tr>'
            + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>" + "".join(body) + "</tbody></table>"
            + "".join(f'<p class="own">{smarten(ital(n))}</p>' for n in notes)
            + f'<p class="owsrcs">{smarten(src)}</p></div>')


def _ogj(s):
    return re.sub(r"^The Oil and Gas Journal", "*The Oil and Gas Journal*", str(s))


# ---------------------------------------------------------------- the posted prices (STYLE 6)

def price_block():
    from .smart import smarten
    P = load().get("posted") or []
    if not P:
        return ""
    out = ['<div class="ow" id="owprice">']
    for i, c in enumerate(P):
        rows = []
        for r in c.get("rows") or []:
            if r.get("kind") == "change":
                fig = (f'{esc(r.get("by", ""))}: ${r["before"]:.2f} to ${r["price"]:.2f}' if r.get("before")
                       else f'{esc(r.get("by", ""))}: ${r["price"]:.2f}')
            else:
                fig = f'${r["price"]:.2f}, quoted'
            tip = r["source"] + (". " + r["note"] if r.get("note") else "")
            rows.append(f'<tr><td>{esc(_date(r["date"]))}</td><td class="owf">{fig}</td>'
                        f'<td class="owsrc"><a href="{esc(r["url"])}" title="{esc(smarten(tip))}">'
                        f'{ital(r.get("cite") or r["source"])}</a></td></tr>')
        h = "owh owh2" if i else "owh"
        out.append(f'<p class="{h}">{esc(smarten("Posted price: " + re.sub(r"(\d+)-(\d)", "\\1–\\2", c["crude"]).replace(" degrees API", "°")))}</p>'
                   '<table class="owp"><thead><tr><th>Date</th><th>$ a barrel, f.o.b.</th><th class="owsrc">Source</th>'
                   '</tr></thead><tbody>'
                   + "".join(rows) + "</tbody></table>")
    out.append('<p class="own">' + esc(smarten(
        "The posted price: the company's published price for a crude at the port. The producing government's revenue "
        "was reckoned on it, not on the price the oil sold for (FRUS 1958–60, IV, doc. 317, note); sales below it "
        "were discounts. A change is the new posting and the day it took "
        "effect; a quoted row, the price in force where a source read gives it. The sources read show Arabian light's "
        "posting unchanged from September 1960 to November 1970.")) + "</p>")
    return "".join(out) + "</div>"


# ---------------------------------------------------------------- the calendar

def tagged(series):
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^(oilworld|oilprice):([\w-]+)$", t)
                if m:
                    out[(m.group(1), m.group(2))] = e["id"]
    return out


def inject(page, series):
    used = False
    for (kind, key), eid in tagged(series).items():
        blk = block(key) if kind == "oilworld" else price_block()
        if not blk:
            continue
        page, k = contents.put(page, eid, blk, kind, key)
        used = used or bool(k)
    if used and 'id="owstyle"' not in page:
        page = page.replace("</head>", STYLE + "\n</head>", 1)
    return page


def problems(series=None):
    """For ./bib check: each year's kept rows within its world total, names known, a source for every price, tags that
    answer."""
    out, W = [], "sources/oil-world.yaml"
    if not os.path.exists(PATH):
        return [(W, "missing")]
    for y, Y in years().items():
        for part, tot in (("production", "world"), ("prior", "prior_world")):
            d = Y.get(part) or {}
            bad = [k for k in d if k not in NAMES]
            if bad:
                out.append((W, f"{y} {part}: unknown keys {bad}"))
            if not isinstance(Y.get(tot), int) or sum(d.values()) > Y.get(tot, 0):
                out.append((W, f"{y} {part}: the countries add to more than the world total, or no total"))
        for k in ("item", "leaf", "table", "pages", "volume", "released"):
            if k not in Y:
                out.append((W, f"{y}: no {k}"))
        for k in Y.get("estimate") or []:
            if k not in (Y.get("production") or {}):
                out.append((W, f"{y}: estimate for {k}, which has no row"))
    for y, R in reserves().items():
        if y not in years():
            out.append((W, f"reserves {y}: no production table that year"))
        if any(k not in NAMES for k in R.get("countries") or {}):
            out.append((W, f"reserves {y}: unknown key"))
        if sum((R.get("countries") or {}).values()) > R.get("free_world", 0) + R.get("bloc", 0):
            out.append((W, f"reserves {y}: the countries add to more than the world"))
        if not R.get("url") or not R.get("source"):
            out.append((W, f"reserves {y}: no source or url"))
    for c in load().get("posted") or []:
        for r in c.get("rows") or []:
            if not r.get("source") or not r.get("url") or r.get("kind") not in ("change", "quoted") \
                    or not isinstance(r.get("price"), (int, float)):
                out.append((W, f"posted {c.get('key')} {r.get('date')}: source, url, kind or price wanting"))
    if series is not None:
        for (kind, key), eid in tagged(series).items():
            if kind == "oilworld" and (not key.isdigit() or int(key) not in years()):
                out.append((eid, f"oilworld:{key}: no such year in {W}"))
            if kind == "oilprice" and key != "ras-tanura":
                out.append((eid, f"oilprice:{key}: unknown"))
    return out
