"""The general elections for governor, 1960-66: elections/governors.yaml (written by tools/elections/make_governors.py
from Wikipedia's tables and the race articles' election boxes, with the source each article gives for its figures).

A calendar entry tagged governors:<YYYY-MM-DD> carries that day's races: a summary, a map of the States by result and
by margin, a key, and a table of the races.

STYLE
 1. One row a race, by State: the State; the candidates, each with votes and share, the winner in bold; the margin;
    under it, across the candidates' and the margin's columns, the note: the incumbent and his party and what became of him (re-elected, defeated, not a candidate), the result
    (a party's hold or gain), and the source of the figures, linked.
 2. A candidate on several lines (New York's fusion lines, Vermont's) is one candidate: his votes the sum of his
    lines (the article's "Total" line where it prints one), his parties in order ("D, Liberal").
 3. Shares from the votes, over all the votes cast for governor (the article's total where it prints one larger than
    the candidates' sum). Where the article prints no votes, the year table's shares, and the note says so.
 4. The result: a party's hold or gain, by the party of the governor in office on election day (the year table).
 5. The map: Result, the winner's party, dark where it took the office, light where it held it; Margin, the winner's
    color, lightest at a tie and darker as the margin grows, by the election maps' quantile rule; a State with no race,
    blank. The District of Columbia had no governor and is not drawn.
 6. The figures' source in each row's note, as the race's article gives it, linked; Our Campaigns, or none, carries
    "Check" (the State's canvass is the record to read: sources/states.yaml).
 7. Names as the articles give them, the incumbent's "(incumbent)" dropped; linked to the name entry where one
    person with an entry fits (namelinks.written).
 8. The table marks a change as the Congress's tables do (the owner's request, Oct. 23, 2026): a party's gain shaded in
    the winner's color, a new governor of the same party in gray, both of a race's rows.
 9. An incumbent "barred from another term" (the race tables' "term-limited") is followed by the provision in force
    on the day, from elections/term-limits.yaml (the owner's request, Oct. 23, 2026: the authority, the reason and
    the scope of the bar): "barred from another term (Mo. Const. art. IV, § 17 (1945, amended 1965): not eligible for election as
    his own successor)", the cite linked to the source read; what it leaves open, a "Check" at the note's end
    (termlimits.py, its STYLE).
"""
import json
import os
import re

from . import contents, store

PATH = os.path.join(store.ROOT, "elections", "governors.yaml")
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
PARTY = {"D": "Democratic", "R": "Republican"}
PARTIES = {"Democrats": "D", "Republicans": "R"}
OTHERS = re.compile(r"^(others?|write-?ins?|scattering|blank|void)$", re.I)
SERIES = None
_C = {}


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def load():
    if "d" not in _C:
        _C["d"] = store.load_yaml(PATH) if os.path.exists(PATH) else {}
    return _C["d"] or {}


def fmt_date(d, year=True):
    y, m, dd = str(d).split("-")
    return f"{MONTHS[int(m) - 1]} {int(dd)}" + (f", {y}" if year else "")


def clean(name):
    return re.sub(r"\s*\((?:incumbent|inc\.?)\)\s*", " ", name, flags=re.I).strip()


def short_party(p):
    p = re.sub(r"\s+of\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?$", "", (p or "").strip())
    p = re.sub(r"\s{2,}", " ", p)
    p = {"Independent politician": "Independent", "Write-in candidate": "", "Write-in": "", "Nonpartisan politician": ""}.get(p, p)
    return {"N/A": "", "?": ""}.get(p, p)


def candidates(r):
    """The race's candidates (STYLE 2, 3): [{name, parties, votes, pct, won}], in the article's order."""
    rows = r.get("candidates") or []
    by, order = {}, []
    totals = {}
    for c in rows:
        n = clean(c["name"])
        if (c.get("party") or "").lower() == "total":
            totals[n] = c
            continue
        if n not in by:
            by[n] = {"name": n, "parties": [], "votes": 0 if c.get("votes") is not None else None,
                     "pct": None, "won": False}
            order.append(n)
        x = by[n]
        p = short_party(c.get("party"))
        if p and p not in x["parties"]:
            x["parties"].append(p)
        if c.get("votes") is not None:
            x["votes"] = (x["votes"] or 0) + c["votes"]
        elif c.get("pct") is not None:
            x["pct"] = (x["pct"] or 0) + c["pct"]
    for n, t in totals.items():
        if n in by and t.get("votes") is not None:
            by[n]["votes"] = t["votes"]
    out = [by[n] for n in order]
    if all(x["votes"] is not None for x in out) and out:
        tot = max(sum(x["votes"] for x in out), r.get("total") or 0)
        for x in out:
            x["pct"] = x["votes"] / tot * 100 if tot else None
        key = lambda x: x["votes"]
    else:
        key = lambda x: x["pct"] or 0
    people = [x for x in out if not OTHERS.match(x["name"])]
    chosen = [x for x in people if r.get("winner") and surname(x["name"]) == surname(r["winner"])]
    if chosen:
        chosen[0]["won"] = True                 # chosen otherwise than by the vote (Georgia, 1966)
    elif people:
        max(people, key=key)["won"] = True
    return out


def votes_known(cs):
    return all(x["votes"] is not None for x in cs)


def winner(cs):
    return next((x for x in cs if x["won"]), None)


def party_of(x):
    return x["parties"][0] if x and x["parties"] else ""


def margin(cs):
    w = winner(cs)
    if not w:
        return None
    rest = [x["pct"] or 0 for x in cs if x is not w]
    return round((w["pct"] or 0) - (max(rest) if rest else 0), 1) if rest else None


def surname(n):
    w = [x for x in n.replace(",", " ").split() if x not in ("Jr.", "Sr.", "II", "III")]
    return w[-1].lower() if w else n.lower()


SHORT = {"bill": "william", "will": "william", "jim": "james", "bob": "robert", "dick": "richard", "mike": "michael",
         "pat": "edmund", "bo": "howard", "cal": "calvin", "wally": "walter", "sam": "samuel", "tom": "thomas",
         "dan": "daniel", "ed": "edward", "fritz": "ernest", "jack": "john", "chuck": "charles", "nels": "nelson"}


def same(a, b):
    """One person under two forms of his name: the surname alike and the first names alike, a short form or a
    nickname in quotation marks counting (Bill Egan, William A. Egan; Edmund G. "Pat" Brown, Pat Brown)."""
    if surname(a) != surname(b):
        return False
    def firsts(n):
        w = n.replace('"', " ").replace(".", " ").split()
        out = {x.lower() for x in w[:-1] if len(x) > 1}
        return out | {SHORT.get(x, x) for x in out}
    fa, fb = firsts(a), firsts(b)
    return not fa or not fb or bool(fa & fb)


def fate(r, cs):
    """What became of the incumbent (STYLE 1)."""
    inc = clean(r.get("incumbent") or "")
    if not inc:
        return ""
    ran = next((x for x in cs if same(x["name"], inc)), None)
    if ran:
        return "re-elected" if ran["won"] else "defeated"
    t = (r.get("result") or "").lower()
    if "renomination" in t or "lost nomination" in t:
        return "lost renomination"
    if "term-limited" in t or "term limited" in t:
        return "barred from another term"
    if "retired" in t or "ran for" in t:
        return "not a candidate"
    return "not a candidate"


def result(r, cs):
    p = party_of(winner(cs))
    if p not in PARTY:
        return p and f"{p} gain"
    return f"{PARTY[p]} {'hold' if p == r.get('inc_party') else 'gain'}"


def rid(r):
    return f"gv{r['date']}-{r['st']}"


def races(date):
    return [r for r in load().get("races") or [] if r["date"] == date]


def name_html(n):
    if SERIES is None or OTHERS.match(n):
        return esc(n)
    from . import namelinks
    hit = namelinks.written(SERIES, n)
    sfx = lambda s: (re.search(r"\b(Jr|Sr|II|III|IV)\.?$", s.strip()) or [None, ""])[1]
    if not hit or sfx(n) != sfx(hit):
        return esc(n)
    return f'<a class="nm" href="{esc(namelinks.url(SERIES, hit))}">{esc(n)}</a>'


def source_html(r):
    s = r.get("source") or {}
    label = s.get("title") or s.get("publisher") or s.get("work") or ""
    if not label and s.get("url"):
        label = s["url"].split("/")[2]
    if not label:
        return ""
    if "ourcampaigns" in (s.get("url") or ""):
        label = "Our Campaigns"
    from .titles import tidy                     # title case, en dashes in spans of years (titles.py, STYLE 3)
    label = tidy(label)
    t = f"<i>{esc(label)}</i>" if label != "Our Campaigns" else esc(label)
    return f'<a href="{esc(s["url"])}">{t}</a>' if s.get("url") else t


def note(r, cs):
    from .congress import STATE
    bits = []
    inc = clean(r.get("incumbent") or "")
    if inc:
        f = fate(r, cs)
        if f == "barred from another term":                  # STYLE 9
            from . import termlimits
            f += termlimits.bar_html(r["st"], r["date"])
        bits.append(f"Incumbent: {name_html(inc)} ({esc(r.get('inc_party') or '?')}), {f}.")
    res = result(r, cs)
    if res:
        bits.append(esc(res[0].upper() + res[1:]) + ".")
    src = source_html(r)
    wiki = f'<a href="https://en.wikipedia.org/wiki/{esc(r["wiki"].replace(" ", "_"))}">Wikipedia</a>'
    if not votes_known(cs):
        bits.append(f"No votes printed; shares from {wiki}'s table of the year.")
    elif src:
        bits.append(f"Figures: {src} ({wiki}).")
    else:
        bits.append(f"Figures: {wiki}.")
    if r.get("note"):
        bits.append(esc(r["note"]))
    if r.get("check"):
        bits.append("Check: the State's canvass.")
    if inc and fate(r, cs) == "barred from another term":    # STYLE 9
        from . import termlimits
        if termlimits.check_html(r["st"], r["date"]):
            bits.append(termlimits.check_html(r["st"], r["date"]))
    return " ".join(bits)


def cands_html(cs):
    from .elections import pct_text
    out = []
    for x in cs:
        cls = ' class="w"' if x["won"] else ""
        ps = ", ".join(x["parties"])
        pv = f' <span class="ep">{esc(ps)}</span>' if ps else ""
        v = f'{x["votes"]:,}' if x["votes"] is not None else ""
        s = pct_text(x["pct"]) if x["pct"] is not None else "—"
        out.append(f'<span class="ec"><span{cls}><span class="en">{name_html(x["name"])}</span>{pv}</span>'
                   f'<span class="ev">{v}</span><span class="es">{s}</span></span>')
    return "".join(out)


def row(r):
    from .congress import STATE
    cs = candidates(r)
    m = margin(cs)
    mg = f"{m:.1f} pts" if m is not None else "Unopposed"
    if r.get("winner"):
        mg = "No majority"                       # chosen otherwise than by the vote (Georgia, 1966)
    st = STATE.get(r["st"], r["st"])
    p = party_of(winner(cs))                     # STYLE 8: a gain in the winner's color, a new governor gray
    k = ("pk" if p != r.get("inc_party") else "" if fate(r, cs) == "re-elected" else "mc") if p in PARTY else ""
    k = f"{k} w{p}" if k == "pk" else k
    return (f'<tbody id="{rid(r)}"><tr class="gvr {k}"><td><span title="{esc(st)}">{esc(r["st"])}</span></td>'
            f'<td class="ecs">{cands_html(cs)}</td><td class="em">{mg}</td></tr>'
            f'<tr class="gvn {k}"><td></td><td class="eno" colspan="2">{note(r, cs)}</td></tr></tbody>')


def record(r):
    """The State's mark on the map (STYLE 5)."""
    from .smart import smarten
    cs = candidates(r)
    w = winner(cs)
    p = party_of(w)
    gain = p != r.get("inc_party")
    f = {"D": "eB4" if gain else "eB2", "R": "eR4" if gain else "eR2"}.get(p, "pO")
    mf = {"D": "rB", "R": "rR"}.get(p, "rA")
    m = margin(cs)
    if r.get("winner"):
        m = 0
    top = ", ".join(f'{x["name"]} ({party_of(x)}) {x["pct"]:.1f}%' for x in cs[:2] if x["pct"] is not None)
    t = f'{r["state"]}: {top}' + (f"; {result(r, cs)}" if result(r, cs) else "")
    return {"id": rid(r), "f": f, "mf": mf, "mg": 100 if m is None else m, "t": smarten(t)}


def summary(date):
    rs = races(date)
    y = int(date[:4])
    won = {"D": [], "R": [], "": []}
    gains = {"D": [], "R": []}
    for r in rs:
        cs = candidates(r)
        p = party_of(winner(cs))
        won[p if p in won else ""].append(r)
        if p in gains and p != r.get("inc_party"):
            gains[p].append(r["state"])
    from .congress import STATE
    n = len(rs)
    out = [f"{n} race{'s' if n != 1 else ''} for governor. Democrats won {len(won['D'])}, Republicans {len(won['R'])}"
           + (f", others {len(won[''])}" if won[""] else "") + "."]
    g = [f"{ {'D': 'Democrats', 'R': 'Republicans'}[p]} gained {len(gains[p])} ({', '.join(gains[p])})" for p in "RD"
         if gains[p]]
    if g:
        out.append("; ".join(g) + ".")
    seats = ((load().get("years") or {}).get(y) or {}).get("seats") or {}
    if seats.get("D") and seats.get("R") and seats["D"].get("after") is not None:
        out.append(f"Governorships after the election: Democrats {seats['D']['after']}, Republicans {seats['R']['after']} "
                   f"(before: {seats['D']['before']} and {seats['R']['before']}).")
    return out


def block(date, head=None):
    """The day's block; head, the heading in its place inside another block (congress.election_day)."""
    rs = races(date)
    if not rs:
        return ""
    q = {r["st"]: record(r) for r in rs}
    key = ('<p class="cgkey elkey"><span class="lk lk-r">'
           '<span class="pqi"><span class="sw eB4"></span>Democratic gain</span> '
           '<span class="pqi"><span class="sw eB2"></span>Democratic hold</span> '
           '<span class="pqi"><span class="sw eR2"></span>Republican hold</span> '
           '<span class="pqi"><span class="sw eR4"></span>Republican gain</span> '
           '<span class="pqi"><span class="sw eNone"></span>No race</span></span>'
           '<span class="lk lk-s">The winner\'s color, lightest at a tie and darker as the margin grows, by the '
           'election maps\' quantile rule: 5 points a fifth of the way, 14 half, 41 nine-tenths; the unopposed '
           'darkest.</span></p>')
    seats = json.dumps({"q": q}, ensure_ascii=False, separators=(",", ":"))
    y = date[:4]
    table = load().get("years", {}).get(int(y), {}).get("table", "")
    src = (f'Figures: each race\'s article on Wikipedia and the source it gives, in the race\'s note; the incumbents and '
           f'the count of governorships, <a href="https://en.wikipedia.org/wiki/{esc(table.replace(" ", "_"))}">'
           f'Wikipedia, "{esc(table)}"</a>. Shares over all the votes cast for governor.')
    return (f'<div class="cg el pq gv" data-cg="gv{date}" id="gv{date}">'
            + (f'<p class="cgh sub">{esc(head)}</p>' if head else f'<p class="cgh">Governors, {esc(fmt_date(date))}</p>')
            + "".join(f'<p class="elsum">{esc(s)}</p>' for s in summary(date))
            + f'<script type="application/json" class="cgseats">{seats}</script>'
            f'<div class="cgmaps"><figure class="cgmap" data-chamber="q" data-none="no race for governor">'
            f'<figcaption>Governors, {esc(fmt_date(date))}, by State</figcaption>'
            f'<div class="cgv" style="aspect-ratio:960/660"></div></figure></div>'
            f'<span data-views="r s"></span>{key}'
            f'<details class="cgr er esp"><summary>Races, {len(rs)}, by State</summary>'
            '<table><colgroup><col class="c1"><col class="c2"><col class="c3"></colgroup>'
            '<thead><tr><th>State</th><th>Candidates, votes, share</th><th>Margin</th></tr></thead>'
            + "".join(row(r) for r in rs) + f'</table></details><p class="elsrc">{src}</p></div>')


def tagged(series):
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^governors:(\d{4}-\d\d-\d\d)$", t)
                if m:
                    out[m.group(1)] = e["id"]
    return out


def inject(page, series):
    """Put the tagged entries' tables and maps into a built page (after congress.inject, whose assets the maps use)."""
    global SERIES
    SERIES = series
    tags = tagged(series)
    used = False
    from .congress import COVERED
    for date, eid in tags.items():
        if date in COVERED["gv"]:                # in the day's Elections block (congress.election_day)
            page, k = contents.put(page, eid, f'<p class="tbp">The table: <a href="#gv{date}">Governors, '
                                   f'{esc(fmt_date(date))}</a>, in the elections of the day.</p>', "see", date)
            continue
        blk = block(date)
        if not blk:
            continue
        page, k = contents.put(page, eid, blk, "governors", date)
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
    """The file: States, dates, a winner in each race; the calendar's tags."""
    from .congress import STATE
    where = "elections/governors.yaml"
    out = []
    for r in load().get("races") or []:
        if r.get("st") not in STATE:
            out.append((where, f"{r.get('st')}: not a State"))
        if not re.fullmatch(r"19\d\d-\d\d-\d\d", str(r.get("date"))):
            out.append((where, f"{r.get('st')}: bad date {r.get('date')}"))
        if not winner(candidates(r)):
            out.append((where, f"{r['date']} {r.get('st')}: no winner"))
    from . import termlimits                                  # STYLE 9: each barred race finds its provision
    out += termlimits.problems([r for r in load().get("races") or [] if clean(r.get("incumbent") or "")
                                and fate(r, candidates(r)) == "barred from another term"])
    if series is not None:
        for date, eid in tagged(series).items():
            if not races(date):
                out.append((eid, f"governors:{date}: no races that day"))
    return out
