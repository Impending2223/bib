"""The State legislatures by session, 1959–1967: elections/legislatures.yaml (written by tools/elections/make_legislatures.py
from Klarner's State Partisan Balance Data).

A calendar entry tagged legislatures:<YYYY> (the year a session met: 1961 for the legislatures chosen in Nov. 1960)
carries that session's map and table.

STYLE
 1. Control of a legislature, as of the federal Constitution's: a party's majority of both chambers; then the two
    qualified majorities the Constitution asks of both Houses, by their State analogues. The Presentment Clause's
    two-thirds to pass a bill over a veto (Art. I, § 7, cl. 2): the State's own proportion to override its governor
    (Klarner: of the members elected or of those present, as the State's constitution of 1956 says; North Carolina's
    governor had no veto). Article V's two-thirds to propose an amendment: two-thirds of each chamber, the federal
    proportion (the States' own rules for proposing amendments, by session or by two successive sessions, majority,
    three-fifths or two-thirds, are not yet in the data: the *Book of the States*, 1960–67, prints them).
 2. The map: the party's color, by what it holds of both chambers: a majority (light); the State's veto-override
    proportion, where that is more than a majority and less than two-thirds (middle); two-thirds (dark, the override
    too where the State's is two-thirds). A legislature whose chambers the parties divide: gray. Nebraska's one
    nonpartisan chamber: the vacant fill. Proportions of the full membership (elected), vacancies in the count.
 3. The summary: the legislatures each party held, the divided, the parties' two-thirds of both chambers, the
    changes from the session before.
 4. The table: by State, each chamber's Democrats, Republicans and others; control; the override proportion; a note.
"""
import json
import math
import os
import re

from . import store

PATH = os.path.join(store.ROOT, "elections", "legislatures.yaml")
PARTY = {"D": "Democratic", "R": "Republican"}
_C = {}


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def load():
    if "d" not in _C:
        _C["d"] = store.load_yaml(PATH) if os.path.exists(PATH) else {}
    return _C["d"] or {}


def sessions():
    return {int(k): v for k, v in (load().get("sessions") or {}).items()}


def need(prop, tot):
    """Seats needed for a proportion of a chamber of tot: more than half for a majority, else the proportion rounded up."""
    if prop is None or not tot:
        return None
    if abs(prop - 0.5) < 1e-6:
        return tot // 2 + 1
    return math.ceil(prop * tot - 1e-9)


def holds(rec, party, prop):
    chs = [rec.get("sen"), rec.get("hs")]
    if any(c is None or c.get(party) is None for c in chs):
        return False
    return all(c[party] >= need(prop, c["T"]) for c in chs)


def level(rec):
    """(party, level): level 1 a majority of both chambers, 2 the override proportion (above a majority, below
    two-thirds), 3 two-thirds of both; (None, 0) divided; ('NP', 0) nonpartisan."""
    if rec.get("hs") is None:
        return "NP", 0
    for p in "DR":
        if holds(rec, p, 0.5):
            if holds(rec, p, 2 / 3):
                return p, 3
            ov = rec.get("override")
            if ov and 0.5 < ov < 2 / 3 - 1e-6 and holds(rec, p, ov):
                return p, 2
            return p, 1
    return None, 0


def veto_proof(rec, p):
    ov = rec.get("override")
    return bool(ov) and holds(rec, p, ov)


def fill(p, lv):
    if p == "NP":
        return "pV"
    if p is None:
        return "eN"
    return {"D": ["eB2", "eB2", "eB3", "eB4"], "R": ["eR2", "eR2", "eR3", "eR4"]}[p][lv]


def chamber(c):
    if not c:
        return "—"
    if c.get("D") is None:
        return f'{c.get("T")} members, without party labels'
    s = f'{c["D"]} D, {c["R"]} R'
    if c.get("O"):
        s += f', {c["O"]} other'
    if c.get("V"):
        s += f', {c["V"]} vacant'
    return s


def frac(p):
    if p is None:
        return "no veto"
    return {0.5: "a majority", 0.6: "three-fifths", 0.6667: "two-thirds", 0.75: "three-fourths"}.get(round(p, 4), f"{p:.2f}")


def control_text(rec):
    p, lv = level(rec)
    if p == "NP":
        return "Nonpartisan"
    if p is None:
        return "Divided"
    bits = [f"{PARTY[p]}, both chambers"]
    if veto_proof(rec, p) and (rec.get("override") or 0) > 0.5:
        bits.append("over the veto")
    if lv == 3:
        bits.append("two-thirds")
    return "; ".join(bits)


def summary(y):
    ss = sessions()
    cur = ss.get(y) or {}
    prev = ss.get(y - 2) or {}
    count = lambda S: {k: sum(1 for r in S.values() if level(r)[0] == k) for k in ("D", "R", None)}
    c, b = count(cur), count(prev)
    two = {p: sum(1 for r in cur.values() if level(r) == (p, 3)) for p in "DR"}
    vp = {p: sum(1 for r in cur.values() if level(r)[0] == p and veto_proof(r, p) and (r.get("override") or 0) > .5)
          for p in "DR"}
    out = [f"The legislatures in session in {y}: Democrats held both chambers in {c['D']}, Republicans in {c['R']}; "
           f"{c[None]} divided; Nebraska's nonpartisan."]
    if prev:
        out.append(f"Two years before: Democrats {b['D']}, Republicans {b['R']}, divided {b[None]}.")
    out.append(f"Where an override takes more than a majority, enough of both chambers to pass a bill over the governor's "
               f"veto: Democrats in {vp['D']}, Republicans in {vp['R']}. Two-thirds of both chambers: Democrats in "
               f"{two['D']}, Republicans in {two['R']}.")
    return out


def record(st, rec, y):
    from .smart import smarten
    from .congress import STATE
    p, lv = level(rec)
    t = f'{STATE.get(st, st)}, {y}: Senate {chamber(rec.get("sen"))}; House {chamber(rec.get("hs"))}; {control_text(rec)}'
    return {"id": f"lg{y}-{st}", "f": fill(p, lv), "mg": 0, "t": smarten(t)}


def row(st, rec, y):
    from .congress import STATE
    note = rec.get("note") or ""
    if rec.get("check"):
        note = (note + " " if note else "") + "Check: " + rec["check"]
    ov = rec.get("override")
    ovt = frac(ov) + (f" of those {rec.get('of')}" if ov else "")
    return (f'<tbody id="lg{y}-{st}"><tr class="gvr"><td><span title="{esc(STATE.get(st, st))}">{esc(st)}</span></td>'
            f'<td>{esc(chamber(rec.get("sen")))}</td><td>{esc(chamber(rec.get("hs")))}</td>'
            f'<td>{esc(control_text(rec))}</td></tr>'
            f'<tr class="gvn"><td></td><td class="eno" colspan="3">Override: {esc(ovt)}. '
            f'Governor: {esc(PARTY.get(rec.get("governor"), "other"))}.{" " + esc(note) if note else ""}</td></tr></tbody>')


def block(y):
    cur = sessions().get(y)
    if not cur:
        return ""
    q = {st: record(st, r, y) for st, r in cur.items()}
    sw = lambda f, t: f'<span class="pqi"><span class="sw {f}"></span>{t}</span> '
    key = ('<p class="cgkey elkey"><span class="lk lk-r">'
           + sw("eB2", "Democratic, both chambers") + sw("eB3", "and enough to override (where under two-thirds)")
           + sw("eB4", "two-thirds of both") + sw("eR2", "Republican, both chambers") + sw("eR3", "and enough to override")
           + sw("eR4", "two-thirds of both") + sw("eN", "Divided") + sw("pV", "Nonpartisan (Nebraska)")
           + '</span></p>')
    seats = json.dumps({"q": q}, ensure_ascii=False, separators=(",", ":"))
    src = load().get("source") or {}
    srcline = (f'Seats in session: <a href="{esc(src.get("url", ""))}">{esc(src.get("title", ""))}</a>, from the Council of '
               'State Governments\' <i>Book of the States</i> and the States\' manuals; the override proportions, the '
               'States\' constitutions as of 1956. Two-thirds of both chambers is the federal proportion for proposing an '
               'amendment (Art. V); the States\' own rules for proposing amendments are not yet in the data.')
    return (f'<div class="cg el pq lg" data-cg="lg{y}" id="lg{y}"><p class="cgh">The State legislatures in session, {y}</p>'
            + "".join(f'<p class="elsum">{esc(s)}</p>' for s in summary(y))
            + f'<script type="application/json" class="cgseats">{seats}</script>'
            f'<div class="cgmaps"><figure class="cgmap" data-chamber="q" data-none="no data" '
            f'data-info="Click a State for its seats." data-rows="Seats \u2193">'
            f'<figcaption>Control of the legislatures, {y}</figcaption>'
            f'<div class="cgv" style="aspect-ratio:960/660"></div></figure></div><span data-views="r"></span>{key}'
            f'<details class="cgr er esp"><summary>Legislatures, {len(cur)}, by State</summary>'
            '<table><colgroup><col class="c1"><col class="c2"><col class="c3"><col class="c4"></colgroup>'
            '<thead><tr><th>State</th><th>Senate</th><th>House</th><th>Control</th></tr></thead>'
            + "".join(row(st, r, y) for st, r in sorted(cur.items()))
            + f'</table></details><p class="elsrc">{srcline}</p></div>')


def tagged(series):
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^legislatures:(\d{4})$", t)
                if m:
                    out[int(m.group(1))] = e["id"]
    return out


def inject(page, series):
    used = False
    for y, eid in tagged(series).items():
        blk = block(y)
        if not blk:
            continue
        pat = re.compile(r'(<li id="' + re.escape(eid) + r'"[^>]*>.*?)(</li>)', re.S)
        page, k = pat.subn(lambda mm: mm.group(1) + blk + mm.group(2), page, count=1)
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
    for y, S in sessions().items():
        for st, r in S.items():
            for ch in ("sen", "hs"):
                c = r.get(ch)
                if c and not r.get("check") and None not in (c.get("D"), c.get("R"), c.get("T")) and c["D"] + c["R"] + (c.get("O") or 0) + (c.get("V") or 0) != c["T"]:
                    out.append(("elections/legislatures.yaml", f"{y} {st} {ch}: the seats do not add to {c['T']}"))
    if series is not None:
        for y, eid in tagged(series).items():
            if y not in sessions():
                out.append((eid, f"legislatures:{y}: no such session"))
    return out
