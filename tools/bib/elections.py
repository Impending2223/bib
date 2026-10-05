"""Election Day: President, House and Senate, with maps (result, vote share, swing; the Electors) and every race.

    elections/<year>.yaml   the Clerk's returns, race by race (tools/elections/make_elections.py)

A calendar entry tagged election:<year> carries that election's block, in cal.html and the reader;
build/congress.html carries each election before the Congress it chose.

Definitions (STYLE, settled):
 1. Share: a candidate's votes over all votes cast for the office in that race (scattering included).
 2. Margin: the winner's votes less the runner-up's ("numeric"), and the same difference over the two
    candidates' combined votes, in points (the two-party margin: 50-45-5 is 5 votes and 5.3 pts).
    Where several were elected at large, the margin is between the last winner and the first loser.
 3. Democratic share (maps): Democratic votes over Democratic and Republican votes in the race (a
    fusion candidate's Liberal line counts with the Democratic). A race without both parties is
    "unopposed" and takes the scale's end.
 4. Pickup: the seat's winner is of a party other than every incumbent who held it (the incumbents
    as Wikipedia lists them, with redistricted members under the district they ran in). A new member
    of the incumbent's party is a member change, shaded lightly. A new seat has no incumbent.
 5. Swing: the change in the Democratic share from the seat's previous election, in points, toward
    the Democrats (+) or Republicans (-). House: the same district where its lines did not change
    (the same shape in congress/geo.json for both Congresses), otherwise the State's House vote.
    Senate: the seat's last regular election, six years before (1952 and 1954 from Wikipedia's
    percentages, later years from the returns). No swing where either election was unopposed.
 6. Colors: one diverging scale, Republican red and Democratic blue around a gray middle, four
    steps a side (tools/bib/elections.py SCALES); in the result view, held seats light and pickups
    dark. Every map value is also in the tables and on hover.
 7. President: the Clerk's figure for a slate is the highest vote for any of its electors. Slates go to
    candidates by Wikipedia's figures, else by party (New York's Liberal line with the Democrat, its
    Conservative line with the Republican). Alabama, 1960: the Democratic slate, five electors pledged
    to Kennedy and six unpledged, counts with Kennedy. Alabama, 1964: Johnson had no slate; the
    Democratic slate was unpledged. The electoral votes are as cast (tools/elections/president.py CAST).
 8. The presidential map. Result: the winner's color, light where the party carried the State at the
    last election, dark where it changed hands; a third ticket (unpledged electors, Byrd, Wallace) amber.
    Vote share: the winner's share of all votes, under 50, 50, 55, 65 and over. Swing: the change in the
    Democratic share of the two-party vote from the last presidential election; none where either party
    had no slate. Electors: a dot an elector, colored by the elector's vote, faithless electors included.
"""
import json
import os
import re
from collections import Counter, defaultdict

from . import store

DIR = os.path.join(store.ROOT, "elections")
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
NAME = {"D": "Democratic", "R": "Republican", "ID": "Independent Democratic", "L": "Liberal", "C": "Conservative", "I": "Independent",
        "O": "other"}
# bins: Democratic share (%), and swing (points toward the Democrats)
SHARE_BINS = [(20, "R4"), (35, "R3"), (45, "R2"), (48, "R1"), (52, "N"), (55, "B1"), (65, "B2"), (80, "B3"), (101, "B4")]
SWING_BINS = [(-10, "R4"), (-6, "R3"), (-3, "R2"), (-1, "R1"), (1, "N"), (3, "B1"), (6, "B2"), (10, "B3"), (999, "B4")]

_cache = {}


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def load():
    if "data" not in _cache:
        out = {}
        if os.path.isdir(DIR):
            for f in sorted(os.listdir(DIR)):
                m = re.match(r"^(\d{4})\.yaml$", f)
                if m:
                    out[int(m.group(1))] = store.load_yaml(os.path.join(DIR, f))
        _cache["data"] = out
    return _cache["data"]


def fmt_date(d):
    y, m, dd = str(d).split("-")
    return f"{MON[int(m) - 1]} {int(dd)}, {y}"


def num(v):
    return "—" if v is None else f"{v:,}"


def party_of(c):
    return "D" if c["p"] in ("D", "ID") else c["p"]


def surname(n):
    w = [x for x in re.sub(r"\(.*?\)|,? (Jr|Sr)\.?|,? II+|[^A-Za-z' \-]", " ", n or "").split() if x]
    return w[-1].lower() if w else ""


# ---------------------------------------------------------------- race metrics

def metrics(r):
    cs = [c for c in r["cands"] if c.get("v") is not None]
    total = sum(c["v"] for c in cs) + (r.get("scat") or 0)
    k = r.get("seats", 1)
    order = sorted(cs, key=lambda c: -c["v"])
    out = {"total": total}
    if len(order) > k:
        a, b = order[k - 1]["v"], order[k]["v"]
        out["margin"] = a - b
        out["margin_pts"] = round(100 * (a - b) / (a + b), 1) if a + b else None
    d = sum(c["v"] for c in cs if party_of(c) == "D")
    rr = sum(c["v"] for c in cs if party_of(c) == "R")
    out["d"], out["r"] = d, rr
    has_d = any(party_of(c) == "D" for c in r["cands"])
    has_r = any(party_of(c) == "R" for c in r["cands"])
    if has_d and has_r and d + rr:
        out["dshare"] = round(100 * d / (d + rr), 1)
    elif has_d and not has_r:
        out["dshare"], out["unopposed"] = 100.0, "D"
    elif has_r and not has_d:
        out["dshare"], out["unopposed"] = 0.0, "R"
    return out


def kind(r, winner):
    """pickup | change | held | new, for one winner."""
    inc = r.get("inc") or []
    if not inc:
        return "new"
    if surname(winner["n"]) in {surname(i["n"]) for i in inc}:
        return "held"
    parties = {("D" if i["p"] in ("D", "ID") else i["p"]) for i in inc}
    return "change" if party_of(winner) in parties else "pickup"


def bin_of(v, bins):
    for hi, k in bins:
        if v < hi:
            return k
    return bins[-1][1]


# ---------------------------------------------------------------- swing

def geo_keys():
    p = os.path.join(store.ROOT, "congress", "geo.json")
    if "geo" not in _cache:
        _cache["geo"] = json.load(open(p, encoding="utf-8"))["congress"] if os.path.exists(p) else {}
    return _cache["geo"]


def state_share(races, st):
    d = sum(metrics(r)["d"] for r in races if r["ch"] == "h" and r["st"] == st)
    rr = sum(metrics(r)["r"] for r in races if r["ch"] == "h" and r["st"] == st)
    return 100 * d / (d + rr) if d + rr else None


def swings(year, data):
    """(ch, st, seat) -> (points, basis) for the election."""
    prev = data.get(year - 2)
    out = {}
    if not prev:
        return out
    g = geo_keys()
    c, cp = str(data[year]["congress"]), str(prev["congress"])
    R, P = data[year]["races"], prev["races"]
    pmap = {(r["st"], r["seat"]): r for r in P if r["ch"] == "h"}
    for r in R:
        if r["ch"] != "h":
            continue
        m = metrics(r)
        same = r["seat"] and g.get(c, {}).get(r["st"], {}).get(str(r["seat"])) and \
            g.get(c, {}).get(r["st"], {}).get(str(r["seat"])) == g.get(cp, {}).get(r["st"], {}).get(str(r["seat"]))
        p = pmap.get((r["st"], r["seat"]))
        if same and p:
            mp = metrics(p)
            if "unopposed" in m or "unopposed" in mp or "dshare" not in m or "dshare" not in mp:
                continue
            out[("h", r["st"], r["seat"])] = (round(m["dshare"] - mp["dshare"], 1), "district")
        else:
            a, b = state_share(R, r["st"]), state_share(P, r["st"])
            if a is not None and b is not None:
                out[("h", r["st"], r["seat"])] = (round(a - b, 1), "state")
    return out


def senate_prior():
    """Two-party Democratic shares from Wikipedia's percentages for the earlier Senate classes."""
    p = os.path.join(DIR, "senate-prior.yaml")
    return store.load_yaml(p) if os.path.exists(p) else {}


def senate_base(year, data):
    """State -> the Democratic share in the seat's last regular election, six years before: from the
    returns where we have them, else from Wikipedia's percentages (senate-prior.yaml)."""
    y0 = year - 6
    if y0 in data:
        out = {}
        for r in data[y0]["races"]:
            if r["ch"] == "s" and not r.get("special"):
                m = metrics(r)
                if "dshare" in m:
                    out[r["st"]] = m["dshare"]
        return out
    return senate_prior().get(y0, {}) or {}


# ---------------------------------------------------------------- the block

def rows_for(year, data):
    """Every seat's map record and the race it came from."""
    E = data[year]
    sw = swings(year, data)
    prior = senate_base(year, data)
    seats = {"h": defaultdict(list), "s": defaultdict(list)}
    for r in E["races"]:
        m = metrics(r)
        winners = [c for c in r["cands"] if c.get("w")]
        for i, w in enumerate(winners):
            k = kind(r, w)
            rec = {"p": party_of(w) if party_of(w) in ("D", "R") else "O", "n": short(w["n"]), "k": k,
                   "id": rid(year, r)}
            if "dshare" in m:
                rec["sh"] = m["dshare"]
            if m.get("unopposed"):
                rec["u"] = 1
            s = sw.get((r["ch"], r["st"], r["seat"]))
            if r["ch"] == "s" and not r.get("special"):
                ps = prior.get(r["st"])
                if ps is not None and "dshare" in m and not m.get("unopposed") and 0 < ps < 100:
                    s = (round(m["dshare"] - ps, 1), "seat")
            if s:
                rec["sw"], rec["swb"] = s
            if r["ch"] == "h":
                rec["d"] = r["seat"]
            else:
                rec["cl"] = r["seat"]
            seats[r["ch"]][r["st"]].append(rec)
    return seats


def short(n):
    n = re.sub(r"\s*\(.*?\)\s*", " ", n)
    n = re.sub(r",? (Jr|Sr)\.?$", "", n.strip())
    return n.split()[-1] if n.split() else n


def rid(year, r):
    pos = f"-p{r['position']}" if r.get("position") else ""
    sp = "-x" if r.get("special") else ""
    return f"e{year}-{r['ch']}-{r['st']}-{r['seat']}{pos}{sp}"


def summary(year, data):
    """Seats won by party, and the change from the last election's winners (House) or the seats up (Senate)."""
    E = data[year]
    out = []
    for ch, label in (("h", "House"), ("s", "Senate")):
        races = [r for r in E["races"] if r["ch"] == ch]
        won = Counter(party_of(c) for r in races for c in r["cands"] if c.get("w"))
        pk = Counter(party_of(c) for r in races for c in r["cands"] if c.get("w") and kind(r, c) == "pickup")
        ch_ = sum(1 for r in races for c in r["cands"] if c.get("w") and kind(r, c) == "change")
        new = sum(1 for r in races for c in r["cands"] if c.get("w") and kind(r, c) == "new")
        n = sum(won.values())
        parts = [f"{won[p]} {NAME.get(p, p)}" for p in ("D", "R") if won.get(p)]
        parts += [f"{v} {NAME.get(p, p)}" for p, v in won.items() if p not in ("D", "R")]
        what = "seats" if ch == "h" else "seats at stake" + (", specials included" if any(r.get("special") for r in races) else "")
        line = f"{label}, {n} {what}: " + ", ".join(parts) + "."
        if pk:
            line += " Pickups: " + ", ".join(f"{NAME.get(p, p)} {v}" for p, v in pk.most_common()) + "."
        if ch_:
            line += f" New members of the same party: {ch_}."
        if new:
            line += f" New seats: {new}."
        out.append(line)
    return out


ABBR = {"Democrat": "D", "Republican": "R", "Democrat, Liberal": "D, L", "Democrat-Farmer-Labor": "DFL", "Liberal": "L",
        "Conservative": "C", "Independent": "I", "Independent Democrat": "Ind. D", "Socialist Labor": "Soc. Lab.",
        "Socialist Workers": "Soc. Wkrs.", "Prohibition": "Proh."}


def cand_html(c, m):
    share = f"{100 * c['v'] / m['total']:.1f}%" if c.get("v") is not None and m["total"] else "—"
    party = esc(ABBR.get(c["party"], c["party"]))
    lines = ""
    if c.get("lines"):
        lines = '<span class="eln">' + "; ".join(f"{esc(ABBR.get(p, p))} {num(v)}" for p, v in c["lines"]) + "</span>"
    cls = ' class="w"' if c.get("w") else ""
    return (f'<span{cls}><span class="en">{esc(c["n"])}</span> <span class="ep" title="{esc(c["party"])}">{party}</span>{lines}</span>'
            f'<span class="ev">{num(c.get("v"))}</span><span class="es">{share}</span>')


def fate(i):
    """'Incumbent lost re-election. Democratic gain.' -> 'Rousselot (R) lost re-election.'"""
    t = (i.get("result") or "").split(". ")[0].rstrip(".")
    t = re.sub(r"^Incumbent\s+", "", t)
    who = f"{short(i['n'])} ({i['p']})"
    if not t or t.lower().startswith(("re-elected", "new seat")):
        return ""
    return f"{who} {t}."


def note_html(r, winners):
    bits = []
    for w in winners:
        k = kind(r, w)
        if k == "pickup":
            bits.append(f"{NAME.get(party_of(w), party_of(w))} pickup.")
        elif k == "change":
            bits.append("New member.")
        elif k == "new":
            bits.append("New seat.")
    if any(kind(r, w) != "held" for w in winners) or len(r.get("inc") or []) > len(winners):
        bits += [esc(f) for f in (fate(i) for i in r.get("inc") or []) if f]
    if r.get("how", "").startswith("unopposed;"):
        bits.append("Unopposed; the State did not tabulate the vote.")
    return " ".join(dict.fromkeys(bits))


def table(year, ch, races):
    from .congress import STATE
    label = "House" if ch == "h" else "Senate"
    rs = [r for r in races if r["ch"] == ch]
    out = [f'<details class="cgr er"><summary>{label} races, {len(rs)}, by state</summary><table>'
           '<colgroup><col class="c1"><col class="c2"><col class="c3"><col class="c4"></colgroup>'
           f'<thead><tr><th>{"District" if ch == "h" else "Class"}</th><th>Candidates, votes, share</th>'
           '<th>Margin</th><th>Note</th></tr></thead><tbody>']
    by = defaultdict(list)
    for r in rs:
        by[r["st"]].append(r)
    for st in sorted(by, key=lambda s: STATE[s]):
        out.append(f'<tr class="st"><th colspan="4">{STATE[st]}</th></tr>')
        for r in sorted(by[st], key=lambda r: (r["seat"], r.get("position") or "", r.get("special"))):
            m = metrics(r)
            winners = [c for c in r["cands"] if c.get("w")]
            ks = {kind(r, w) for w in winners}
            cls = "pk" if "pickup" in ks else "mc" if ks & {"change", "new"} else ""
            if ch == "h":
                seat = "At large" if r["seat"] == 0 else str(r["seat"])
                if r.get("position"):
                    seat += f", position {r['position']}"
                if r.get("seats", 1) > 1:
                    seat += f" ({r['seats']} seats)"
            else:
                seat = ("I", "II", "III")[r["seat"] - 1] + (", unexpired term" if r.get("special") else "")
            cands = "".join(f'<span class="ec">{cand_html(c, m)}</span>' for c in sorted(r["cands"], key=lambda c: -(c.get("v") or 0)))
            if r.get("scat"):
                cands += f'<span class="ec"><span><span class="en">Scattering</span></span><span class="ev">{num(r["scat"])}</span><span class="es"></span></span>'
            if "margin" in m:
                margin = f'{num(m["margin"])}<br><span class="es">{m["margin_pts"]:.1f} pts</span>'
            else:
                margin = "Unopposed"
            wp = party_of(winners[0]) if winners else ""
            out.append(f'<tr id="{rid(year, r)}" class="{cls} w{wp}"><td>{esc(seat)}</td><td class="ecs">{cands}</td>'
                       f'<td class="em">{margin}</td><td class="eno">{note_html(r, winners)}</td></tr>')
    out.append("</tbody></table></details>")
    return "\n".join(out)


def block(year, data, view="r"):
    E = data[year]
    c = E["congress"]
    seats = rows_for(year, data)
    has_sw = any("sw" in x for ch in seats.values() for v in ch.values() for x in v)
    out = [f'<div class="cg el" data-cg="{c}" data-ev="{year}">']
    out.append(f'<p class="cgh">Election of {esc(fmt_date(E["date"]))}: the {c}th Congress</p>')
    for line in summary(year, data):
        out.append(f'<p class="elsum">{esc(line)}</p>')
    pres = E.get("president")
    if pres:
        seats["p"] = pres_rows(year, data)
        out.append(f'<p class="elsum">{esc(pres_summary(year, data))}</p>')
        has_sw = has_sw or any("sw" in x for x in seats["p"].values())
    out.append(f'<script type="application/json" class="cgseats">{json.dumps(seats, ensure_ascii=False, separators=(",", ":"))}</script>')
    views = '<span data-views="r s' + (' w' if has_sw else '') + '"></span>'
    if pres:
        out.append('<div class="cgmaps"><figure class="cgmap" data-chamber="p"><figcaption>President, by state</figcaption>'
                   '<div class="cgv" style="aspect-ratio:960/660"></div></figure></div>')
        out.append(pres_legend(year - 4 in data and "president" in data[year - 4],
                               any("sw" in x for x in seats["p"].values())))
    out.append('<div class="cgmaps">'
               '<figure class="cgmap dots" data-chamber="h"><figcaption>House, by delegation</figcaption>'
               '<div class="cgv" style="aspect-ratio:1085/660"></div></figure>'
               '<figure class="cgmap" data-chamber="s"><figcaption>Senate, by state</figcaption>'
               '<div class="cgv" style="aspect-ratio:960/660"></div></figure></div>' + views)
    out.append(legend(has_sw))
    if pres:
        out.append(pres_table(year, data))
    out.append(table(year, "h", E["races"]))
    out.append(table(year, "s", E["races"]))
    src = E.get("source", {})
    out.append(f'<p class="elsrc">Returns: <a href="{esc(src.get("url", ""))}">{esc(src.get("label", ""))}</a>, '
               'read by OCR and checked against its recapitulation totals and Wikipedia\'s percentages, or read by eye. '
               'Incumbents and their fates: Wikipedia\'s race tables. Margin: votes, and points of the two leaders\' combined vote.</p>')
    out.append("</div>")
    return "\n".join(out)


def legend(has_sw):
    sw = lambda k: f'<span class="sw e{k}"></span>'
    share = (f'<span class="lk lk-s">Democratic share of the two-party vote: {sw("R4")}{sw("R3")}{sw("R2")}{sw("R1")}'
             f'{sw("N")}{sw("B1")}{sw("B2")}{sw("B3")}{sw("B4")} '
             '<span class="lt">under 20 · 35 · 45 · 48–52 · 55 · 65 · 80 and over; unopposed at the ends</span></span>')
    res = (f'<span class="lk lk-r">{sw("B2")}Democratic held {sw("B4")}Democratic pickup '
           f'{sw("R2")}Republican held {sw("R4")}Republican pickup {sw("None")}No election</span>')
    swing = (f'<span class="lk lk-w">Swing, points: {sw("R4")}{sw("R3")}{sw("R2")}{sw("R1")}{sw("N")}'
             f'{sw("B1")}{sw("B2")}{sw("B3")}{sw("B4")} <span class="lt">10 or more Republican · 6 · 3 · 1 · ±1 · 1 · 3 · 6 · 10 or more Democratic; '
             'redrawn districts take their State\'s swing</span> ' + sw("NA") + 'None</span>') if has_sw else ""
    return f'<p class="cgkey elkey">{res}{share}{swing}</p>'


# ---------------------------------------------------------------- the President

WIN_BINS = [(50, "1"), (55, "2"), (65, "3"), (101, "4")]   # the winner's share: plurality, 50, 55, 65


def pcls(k, cands):
    """A candidate key's color class: D, R, T (a third ticket: unpledged electors, Byrd, Wallace), O (others)."""
    like = (cands.get(k) or {}).get("like", k)
    return like if like in ("D", "R") else "T" if like in ("U", "A") else "O"


def pmetrics(rec):
    tot = {}
    for s in rec["slates"]:
        tot[s["k"]] = tot.get(s["k"], 0) + (s.get("v") or 0)
    total = sum(tot.values()) + (rec.get("scat") or 0)
    order = sorted(tot, key=lambda k: -tot[k])
    out = {"tot": tot, "total": total, "win": order[0] if order else None}
    if order and total:
        out["sh"] = round(100 * tot[order[0]] / total, 1)
    if len(order) > 1:
        a, b = tot[order[0]], tot[order[1]]
        out["margin"], out["margin_pts"] = a - b, round(100 * (a - b) / (a + b), 1) if a + b else None
    d, r = tot.get("D", 0), tot.get("R", 0)
    if d and r:
        out["dsh"] = round(100 * d / (d + r), 1)
    return out


def pcands(E):
    return {c["k"]: c for c in E["president"]["cands"]}


def pres_rows(year, data):
    """Each State's map record: winner class, share, flip, swing, and its electors as they voted."""
    E = data[year]
    C = pcands(E)
    prev = (data.get(year - 4) or {}).get("president")
    pm = {r["st"]: pmetrics(r) for r in prev["states"]} if prev else {}
    PC = pcands(data[year - 4]) if prev else {}
    out = {}
    for r in E["president"]["states"]:
        m = pmetrics(r)
        p = pcls(m["win"], C)
        rec = {"p": p, "n": short(C[m["win"]]["n"]) if m["win"] in C else "Others", "id": f"e{year}-p-{r['st']}",
               "ev": r["ev"], "cast": [[pcls(k, C), n, short(C[k]["n"]) if k in C else k] for k, n in r["cast"].items()]}
        if "sh" in m:
            rec["sh"] = m["sh"]
        q = pm.get(r["st"])
        if prev:
            rec["k"] = "new" if q is None else "held" if pcls(q["win"], PC) == p else "flip"
        if q and "dsh" in m and "dsh" in q:
            rec["sw"] = round(m["dsh"] - q["dsh"], 1)
        out[r["st"]] = rec
    return out


def pres_summary(year, data):
    E = data[year]
    C = pcands(E)
    ev, pop = Counter(), Counter()
    for r in E["president"]["states"]:
        for k, n in r["cast"].items():
            ev[k] += n
        for k, v in pmetrics(r)["tot"].items():
            pop[k] += v
    total = sum(pop.values()) + sum(r.get("scat") or 0 for r in E["president"]["states"])
    name = lambda k: C[k]["n"] if k in C else "Others"
    line = f"President, {sum(ev.values())} electoral votes: " + ", ".join(f"{name(k)} {n}" for k, n in ev.most_common()) + "."
    line += " Popular vote: " + ", ".join(f"{name(k)} {pop[k]:,} ({100 * pop[k] / total:.1f}%)" for k, _ in pop.most_common()
                                         if k != "O" and 100 * pop[k] / total >= 0.5) + "."
    return line


def pres_table(year, data):
    from .congress import STATE
    E = data[year]
    C = pcands(E)
    prev = (data.get(year - 4) or {}).get("president")
    pm = {r["st"]: pmetrics(r) for r in prev["states"]} if prev else {}
    PC = pcands(data[year - 4]) if prev else {}
    rows = sorted(E["president"]["states"], key=lambda r: STATE.get(r["st"], r["st"]))
    out = [f'<details class="cgr er"><summary>President, {len(rows)} States{" and the District" if any(r["st"] == "DC" for r in rows) else ""}</summary><table>'
           '<colgroup><col class="c1"><col class="c2"><col class="c3"><col class="c4"></colgroup>'
           '<thead><tr><th>State, electors</th><th>Slates, votes, share</th><th>Margin</th><th>Note</th></tr></thead><tbody>']
    for r in rows:
        m = pmetrics(r)
        cs = ""
        for s in sorted(r["slates"], key=lambda s: -(s.get("v") or 0)):
            who = C[s["k"]]["n"] if s["k"] in C else ""
            share = f"{100 * s['v'] / m['total']:.1f}%" if s.get("v") is not None and m["total"] else "—"
            w = ' class="w"' if s["k"] == m["win"] else ""
            cs += (f'<span class="ec"><span{w}><span class="en">{esc(s["party"])}</span>'
                   + (f' <span class="ep">{esc(who)}</span>' if who else "") +
                   f'</span><span class="ev">{num(s.get("v"))}</span><span class="es">{share}</span></span>')
        if r.get("scat"):
            cs += f'<span class="ec"><span><span class="en">Scattering</span></span><span class="ev">{num(r["scat"])}</span><span class="es"></span></span>'
        margin = f'{num(m["margin"])}<br><span class="es">{m["margin_pts"]:.1f} pts</span>' if "margin" in m else ""
        p = pcls(m["win"], C)
        note = []
        q = pm.get(r["st"])
        if q and pcls(q["win"], PC) != p:
            note.append(f"{NAME[p]} gain." if p in ("D", "R") else "Carried by a third ticket.")
        cast = "; ".join(f"{n} {C[k]['n'] if k in C else k}" for k, n in r["cast"].items())
        if len(r["cast"]) > 1 or list(r["cast"])[0] != m["win"]:
            note.append(f"Electors: {cast}.")
        if r.get("note"):
            note.append(r["note"])
        cls = "pk" if q and pcls(q["win"], PC) != p else ""
        out.append(f'<tr id="e{year}-p-{r["st"]}" class="{cls} w{p}"><td>{esc(STATE.get(r["st"], r["st"]))}<br>'
                   f'<span class="es">{r["ev"]}</span></td><td class="ecs">{cs}</td><td class="em">{margin}</td>'
                   f'<td class="eno">{esc(" ".join(note))}</td></tr>')
    out.append("</tbody></table></details>")
    return "\n".join(out)


def pres_legend(has_prev, has_sw):
    sw = lambda k: f'<span class="sw e{k}"></span>'
    res = (f'<span class="lk lk-r">{sw("B2")}Democratic {sw("R2")}Republican {sw("A2")}Third ticket'
           + (f'; dark where the State changed hands: {sw("B4")}{sw("R4")}{sw("A4")}' if has_prev else "") + '</span>')
    share = (f'<span class="lk lk-s">The winner\'s share of the vote: {sw("B1")}{sw("B2")}{sw("B3")}{sw("B4")} '
             f'{sw("R1")}{sw("R2")}{sw("R3")}{sw("R4")} {sw("A1")}{sw("A2")}{sw("A3")}{sw("A4")} '
             '<span class="lt">under 50 · 50 · 55 · 65 and over</span></span>')
    swing = (f'<span class="lk lk-w">Swing from the last presidential election, points: {sw("R4")}{sw("R3")}{sw("R2")}{sw("R1")}{sw("N")}'
             f'{sw("B1")}{sw("B2")}{sw("B3")}{sw("B4")} <span class="lt">10 or more Republican · 6 · 3 · 1 · ±1 · 1 · 3 · 6 · 10 or more Democratic; '
             'none where a party had no slate</span> ' + sw("NA") + 'None</span>') if has_sw else ""
    dots = (f'<span class="lk lk-e">Electors, one dot each, as they voted: <span class="sw pD"></span>Democratic '
            '<span class="sw pR"></span>Republican <span class="sw pT"></span>Third ticket <span class="sw pO"></span>Other</span>')
    return f'<p class="cgkey elkey elpk">{res}{share}{swing}{dots}</p>'


def tagged(series):
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^election:(\d{4})$", t)
                if m:
                    out[int(m.group(1))] = e
    return out


def problems():
    """For ./bib check: winners against seats, votes as integers, a source per election."""
    out = []
    for y, E in load().items():
        if not (E.get("source") or {}).get("url"):
            out.append((str(y), "election without a source"))
        for r in E.get("races", []):
            w = sum(1 for c in r["cands"] if c.get("w"))
            if w != r.get("seats", 1):
                out.append((str(y), f"{r['ch']} {r['st']} {r['seat']}: {w} winners for {r.get('seats', 1)} seats"))
            for c in r["cands"]:
                if c.get("v") is not None and not isinstance(c["v"], int):
                    out.append((str(y), f"{r['st']} {r['seat']}: votes not a number for {c['n']}"))
        P = E.get("president")
        if P:
            EV = {1956: 531, 1960: 537}.get(y, 538)
            got = sum(sum(r["cast"].values()) for r in P["states"])
            if got != EV:
                out.append((str(y), f"president: {got} electoral votes, not {EV}"))
            for r in P["states"]:
                if sum(r["cast"].values()) != r["ev"]:
                    out.append((str(y), f"president {r['st']}: electors cast {sum(r['cast'].values())} of {r['ev']}"))
                if any(not isinstance(x.get("v"), int) for x in r["slates"]):
                    out.append((str(y), f"president {r['st']}: a slate without a vote"))
    return out
