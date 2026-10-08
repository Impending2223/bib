"""Election Day: President, House and Senate, with maps (result, margin, swing; the Electors) and every race.

    elections/<year>.yaml   the Clerk's returns, race by race (tools/elections/make_elections.py)

A calendar entry tagged election:<year> carries that election's block, in cal.html and the reader;
build/congress.html carries each election before the Congress it chose.

Definitions (STYLE, settled):
 1. Share: a candidate's votes over all votes cast for the office in that race (scattering included).
 2. Margin: the winner's votes less the runner-up's, in votes and in points of all the votes cast in
    the race (50-45-5 is 5 votes and 5.0 pts). Where several were elected at large, the margin is
    between the last winner and the first loser. The two-party share serves only for swing.
 3. Margin (maps): the winner's margin over the runner-up (note 2), in points of all the votes, in the
    winner's color, continuous, not in steps, on the maps' one diverging scale (note 8), Republican red
    through near white at a tie to Democratic blue. Quantile
    rule: a margin's position on the ramp is the share of the 2,291 contested races for presidential
    electors, 1824-2024, decided by less (elections/pres-margins.csv; QM in templates/congress.html): 5
    points about a fifth of the way, 14 (the median) half, 41 nine-tenths; the unopposed count as 100. The
    same table for the House and Senate, so a shade means the same margin on every map. A winner of neither major party takes the color of the party
    caucused with. A shape shared by several seats of one party takes their mean.
 4. Caucus: a member of neither major party counts with the party caucused with, in the seats won, the
    net change and pickups, and is so labeled: "Conservative, caucusing with the Republicans" (elections/facts.yaml caucus:).
    Maps and bars give them a striped variant of that party's color.
 5. Pickup: the seat's winner caucuses with a party other than every incumbent who held it (the
    incumbents as Wikipedia lists them, with redistricted members under the district they ran in, and a
    vacant seat under the member who last held it). A new member of the incumbent's party is a member
    change, shaded lightly. A new seat has no incumbent.
 6. Net change: the seats the gaining party gained, by caucus, from the close of the last Congress to
    the seats won ("Net change from close: R+20"); the other party's change follows only where
    it does not mirror the gain, as when a new seat was added ("D+49 (R−48)"). The close: the seats held
    at the close of the last Congress (the
    members sitting at the election; a vacant seat with the party that last held it). In the Senate,
    the seats at stake only.
 7. Swing: the change in the Democratic share of the two-party vote (Democratic votes over Democratic
    and Republican, a fusion candidate's Liberal line with the Democratic) from the seat's previous
    election, in points, toward the Democrats or the Republicans. House: the same district where its
    lines did not change (the same shape in congress/geo.json for both Congresses), otherwise the
    State's House vote. Senate: the seat's last regular election, six years before (1952 and 1954 from
    Wikipedia's percentages, later years from the returns). No swing where either election was unopposed,
    or where the winner ran on neither major party's line.
 8. Colors: in the result view, four steps a side, held seats light and pickups dark (with Flips, held
    and flipped; the President's winner a middle step); the margin view, a straight line in OKLab from near
    white at a tie to the darkest step, by the quantile rule (note 3); the swing view, gray at no swing to
    the darkest step at 15 points or more (SWING in the template). The keys draw the scales as gradient
    bars. Every map value is also in the tables and on hover.
 9. The Senate by senator: a dot a seat; in an election, the seats at stake, and the others gray, from
    the roster at the opening of the Congress chosen, where there is one.
10. President: the Clerk's figure for a slate is the highest vote for any of its electors. Slates go to
    candidates by Wikipedia's figures, else by party (New York's Liberal line with the Democrat, its
    Conservative line with the Republican). Alabama, 1960: the Democratic slate, five electors pledged
    to Kennedy and six unpledged, counts with Kennedy; the note to the popular vote gives the other
    reckonings. Alabama, 1964: Johnson had no slate; the Democratic slate was unpledged. The electoral
    votes are as cast (tools/elections/president.py CAST).
11. The presidential map. Result: the winner's color, a third ticket (unpledged electors, Byrd,
    Wallace) amber, one flat shade. "Flips", a toggle under the map between States and Electors, applies the Congress maps'
    scheme in the result view: the States that went to another party than at the last election dark, the
    others light. The outlines stay the standard ones. Margin and swing as for the House and Senate; no swing where
    either party had no slate. Electors: a dot an elector, colored by the elector's vote, faithless
    electors included.

Map records (the JSON in each block's script.cgseats, read by templates/congress.html):
  seats.h[ST], seats.s[ST]: one record a seat. Congress at its opening (congress.py): {p, n, id, d | cl, pl?}.
  Election (rows_for): {p, n, id, d | cl, k, sh, mg?, u?, sw?, swb?, x?, pl?, ho?}
    p   party for color and counts: D, R (by caucus for a third-party member), O; at an opening also V
        (vacant), Di, Ri (a third-party member caucusing with the Democrats, the Republicans)
    n   the label on the map (a surname); pl the full party label of a third-party member
    id  the row id in the tables (e<year>-<ch>-<ST>-<seat>, or the roster's cg<c>-<ch>-<ST>-<seat>)
    d   district (0 at large) | cl Senate class
    k   pickup | change | held | new          sh the winner's share of all votes; u unopposed
    mg  the margin, points of all votes        sw swing, points toward the Democrats; swb its basis
    x   a winner of neither major party        ho a seat not at stake (the Senate, from the roster)
  seats.p[ST] (pres_rows): {p (D, R, T a third ticket, O), n, id, ev, cast [[class, electors, name]],
    sh, mg, k (held | flip | new), sw}
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
    """The party for the two-party share: the Democratic and Republican nominees' lines."""
    return "D" if c["p"] in ("D", "ID") else c["p"]


def facts():
    """elections/facts.yaml: the hand facts (caucus, the President's electors, Alabama 1960)."""
    if "facts" not in _cache:
        p = os.path.join(DIR, "facts.yaml")
        _cache["facts"] = store.load_yaml(p) if os.path.exists(p) else {}
    return _cache["facts"]


def third(surname_):
    """(label, caucus) for a member of neither major party, from facts.yaml caucus:, or None."""
    t = (facts().get("caucus") or {}).get(surname_)
    return (t["label"], t["caucus"]) if t else None


PLURAL = {"D": "Democrats", "R": "Republicans"}


def caucus(c):
    """D or R: the party a member sat with (Buckley, Conservative, with the Republicans)."""
    if c["p"] in ("D", "R"):
        return c["p"]
    if c["p"] == "ID":
        return "D"
    t = third(surname(c["n"]))
    return t[1] if t else c["p"]


def third_label(c):
    """'Conservative, caucusing with the Republicans', for a winner of neither major party."""
    t = third(surname(c["n"]))
    lab = t[0] if t else NAME.get(c["p"], c.get("party") or c["p"])
    cc = caucus(c)
    return f"{lab}, caucusing with the {PLURAL[cc]}" if cc in PLURAL else lab


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
        out["margin_pts"] = round(100 * (a - b) / total, 1) if total else None
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
    parties = {caucus(i) for i in inc}
    return "change" if caucus(winner) in parties else "pickup"


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

def roster(c):
    """The Congress's members at its opening (congress/<c>.yaml), or None."""
    p = os.path.join(store.ROOT, "congress", f"{c}.yaml")
    if ("roster", c) not in _cache:
        _cache[("roster", c)] = store.load_yaml(p) if os.path.exists(p) else None
    return _cache[("roster", c)]


def rows_for(year, data):
    """Every seat's map record and the race it came from; in the Senate also the seats not at stake,
    from the roster at the opening of the Congress chosen, where there is one."""
    E = data[year]
    sw = swings(year, data)
    prior = senate_base(year, data)
    seats = {"h": defaultdict(list), "s": defaultdict(list)}
    up = defaultdict(set)
    for r in E["races"]:
        m = metrics(r)
        winners = [c for c in r["cands"] if c.get("w")]
        for w in winners:
            cc = caucus(w)
            rec = {"p": cc if cc in ("D", "R") else "O", "n": short(w["n"]), "k": kind(r, w), "id": rid(year, r)}
            if w["p"] not in ("D", "R"):
                rec["x"], rec["pl"] = 1, third_label(w)
            opposed = any(c is not w and c.get("v") for c in r["cands"])
            if w.get("v") is None or not opposed:
                rec["u"] = 1
            rec["sh"] = round(100 * w["v"] / m["total"], 1) if w.get("v") and m["total"] else 100.0
            if m.get("margin_pts") is not None:
                rec["mg"] = m["margin_pts"]
            s = sw.get((r["ch"], r["st"], r["seat"]))
            if r["ch"] == "s" and not r.get("special"):
                ps = prior.get(r["st"])
                if ps is not None and "dshare" in m and not m.get("unopposed") and 0 < ps < 100:
                    s = (round(m["dshare"] - ps, 1), "seat")
            if s and not rec.get("x"):    # no swing where the winner ran on neither major party's line
                rec["sw"], rec["swb"] = s
            if r["ch"] == "h":
                rec["d"] = r["seat"]
            else:
                rec["cl"] = r["seat"]
                up[r["st"]].add(r["seat"])
            seats[r["ch"]][r["st"]].append(rec)
    C = roster(E["congress"])
    for r in (C or {}).get("senate", []):
        if r.get("vacant") or r["cl"] in up.get(r["st"], ()):
            continue
        sur = r["name"].split(",")[0].strip()
        cc = caucus({"p": r["party"], "n": sur})
        rec = {"p": cc if cc in ("D", "R") else "O", "n": sur, "cl": r["cl"], "ho": 1,
               "id": f"cg{E['congress']}-s-{r['st']}-{r['cl']}"}
        if r["party"] not in ("D", "R"):
            rec["x"], rec["pl"] = 1, third_label({"p": r["party"], "n": sur})
        seats["s"][r["st"]].append(rec)
    return seats


def short(n):
    n = re.sub(r"\s*\(.*?\)\s*", " ", n)
    n = re.sub(r",? (Jr|Sr)\.?$", "", n.strip())
    return n.split()[-1] if n.split() else n


def rid(year, r):
    pos = f"-p{r['position']}" if r.get("position") else ""
    sp = "-x" if r.get("special") else ""
    return f"e{year}-{r['ch']}-{r['st']}-{r['seat']}{pos}{sp}"


def ordinal(n):
    return f"{n}{'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def signed(v):
    return f"+{v}" if v > 0 else f"\u2212{-v}" if v < 0 else "0"


def net_change(before, after):
    """The seats the gaining party gained, by caucus: 'R+20'. The other party's change follows only where
    it does not mirror the gain (a new seat, a third member): 'D+49 (R−48)'. 'none' where neither changed."""
    d, r = after.get("D", 0) - before.get("D", 0), after.get("R", 0) - before.get("R", 0)
    if not d and not r:
        return "none"
    gain, other = (("D", d), ("R", r)) if d > r else (("R", r), ("D", d))
    out = f"{gain[0]}{signed(gain[1])}"
    return out if other[1] == -gain[1] else f"{out} ({other[0]}{signed(other[1])})"


def summary(year, data):
    """Seats won by party; the net change by caucus from the seats held at the close of the last
    Congress (the members sitting at the election, a vacant seat with the party that last held it);
    pickups, new members of same party, new seats."""
    E = data[year]
    out = []
    for ch, label in (("h", "House"), ("s", "Senate")):
        races = [r for r in E["races"] if r["ch"] == ch]
        wins = [(r, c) for r in races for c in r["cands"] if c.get("w")]
        won = Counter(c["p"] for r, c in wins if c["p"] in ("D", "R"))
        thirds = [c for r, c in wins if c["p"] not in ("D", "R")]
        n = len(wins)
        parts = [f"{won[p]} {NAME[p]}" for p in ("D", "R") if won.get(p)]
        parts += [f"1 {third_label(c)}" for c in thirds]
        what = "seats" if ch == "h" else "seats at stake" + (", specials included" if any(r.get("special") for r in races) else "")
        line = f"{label}, {n} {what}: " + ("; " if thirds else ", ").join(parts) + "."
        before, seen = Counter(), set()
        for r in races:
            for i in r.get("inc") or []:
                if i["n"] not in seen:
                    seen.add(i["n"])
                    before[caucus(i)] += 1
        after = Counter(caucus(c) for c in {c["n"]: c for r, c in wins}.values())   # one member who won two races (Oregon, 1960) once
        line += f" Net change from close: {net_change(before, after)}."
        pk = Counter(caucus(c) for r, c in wins if kind(r, c) == "pickup")
        ch_ = sum(1 for r, c in wins if kind(r, c) == "change")
        new = sum(1 for r, c in wins if kind(r, c) == "new")
        if pk:
            line += " Pickups: " + ", ".join(f"{NAME.get(p, p)} {v}" for p, v in pk.most_common()) + "."
        if ch_:
            line += f" New members of same party: {ch_}."
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
    if r.get("src"):            # the Clerk prints no vote: another source's (tools/elections/read.py, source)
        src = re.sub(r"[*]([^*]+)[*]", r"<i>\1</i>", esc(r["src"]))
        bits.append(f"The Clerk prints no vote; votes: {src}.")
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
    pres = E.get("president")
    note = None
    if pres:
        seats["p"] = pres_rows(year, data)
        line, note = pres_summary(year, data)
        out.append(f'<p class="elsum">{esc(line)}</p>')
        has_sw = has_sw or any("sw" in x for x in seats["p"].values())
    for line in summary(year, data):
        out.append(f'<p class="elsum">{esc(line)}</p>')
    if note:
        out.append(f'<p class="elsum elnote">{esc(note)}</p>')
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
               'Incumbents and their fates: Wikipedia\'s race tables. Margin: votes, and points of all the votes cast in the race.</p>')
    out.append("</div>")
    return "\n".join(out)


def margin_scale(third=False):
    """The margin key: one diverging gradient bar (STYLE 8), a tie in the middle, positioned by the quantile
    rule (STYLE 3); a third ticket's bar beside it."""
    out = ('<span class="lt">Republican</span><span class="gr gS"></span><span class="lt">Democratic. Lightest at a '
           'tie; darker by the share of contested elector races since 1824 decided by less: 5 points, a fifth of '
           'the way; 14, half; 41, nine-tenths; the unopposed darkest.</span>')
    return out + (' <span class="gr gA"></span><span class="lt">third ticket</span>' if third else "")


def swing_scale():
    """The swing key: one diverging gradient bar, 15 points or more each way (SWING in the template)."""
    return ('<span class="lt">15 or more Republican</span><span class="gr gW"></span>'
            '<span class="lt">15 or more Democratic</span>')


def legend(has_sw):
    sw = lambda k: f'<span class="sw e{k}"></span>'
    res = (f'<span class="lk lk-r">{sw("B2")}Democratic held {sw("B4")}Democratic pickup '
           f'{sw("R2")}Republican held {sw("R4")}Republican pickup <span class="sw pDi"></span><span class="sw pRi"></span>'
           f'Independent or third party, by the party caucused with {sw("None")}No election; '
           'Senators: <span class="sw eHo"></span>not at stake</span>')
    share = f'<span class="lk lk-s">The winner\'s margin over the runner-up, points of all the votes: {margin_scale()}</span>'
    swing = (f'<span class="lk lk-w">Swing, points: {swing_scale()} <span class="lt">redrawn districts take their '
             'State\'s swing</span> ' + sw("NA") + 'None</span>') if has_sw else ""
    return f'<p class="cgkey elkey">{res}{share}{swing}</p>'


# ---------------------------------------------------------------- the President



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
        out["margin"], out["margin_pts"] = a - b, round(100 * (a - b) / total, 1) if total else None
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
        if m.get("margin_pts") is not None:
            rec["mg"] = m["margin_pts"]
        q = pm.get(r["st"])
        if prev:
            rec["k"] = "new" if q is None else "held" if pcls(q["win"], PC) == p else "flip"
        if q and "dsh" in m and "dsh" in q:
            rec["sw"] = round(m["dsh"] - q["dsh"], 1)
        out[r["st"]] = rec
    return out


def pres_summary(year, data):
    """The electoral and popular vote; for 1960, a note on the ways of counting Alabama."""
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
    star = "*" if year == 1960 else ""
    line = f"President, {sum(ev.values())} electoral votes: " + ", ".join(f"{name(k)} {n}" for k, n in ev.most_common()) + "."
    line += f" Popular vote{star}: " + ", ".join(f"{name(k)} {pop[k]:,} ({100 * pop[k] / total:.1f}%)" for k, _ in pop.most_common()
                                                if k != "O" and 100 * pop[k] / total >= 0.5) + "."
    note = None
    if year == 1960:
        al = next(r for r in E["president"]["states"] if r["st"] == "AL")
        d = sum(x["v"] for x in al["slates"] if x["k"] == "D")
        K, N = pop["D"], pop["R"]
        A = facts()["alabama_1960"]
        top, (num_, den) = A["kennedy_top_elector"], A["cq_share"]
        k2, part = K - d + top, round(d * num_ / den)
        k3 = K - d + part
        note = (f"* Alabama's Democratic slate, eleven electors, five pledged to Kennedy and six unpledged, is counted here "
                f"with Kennedy, at its leading elector's vote ({d:,}): Kennedy ahead by {K - N:,}. At the vote of Kennedy's "
                f"own leading elector ({top:,}), the unpledged electors' apart: Kennedy ahead by {k2 - N:,}. "
                f"The slate's vote divided by its electors, {A['cq_share_words']} to Kennedy ({part:,}), as Congressional Quarterly "
                f"reckoned it: Nixon ahead by {N - k3:,}. " + " ".join(A.get("guide", "").split()) +
                " Mississippi's unpledged slate, which carried the State, counts for "
                "neither. " + " ".join(A["source"].split()) + " " + " ".join(A["check"].split()))
    return line, note


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
    res = (f'<span class="lk lk-r">{sw("B3")}Democratic {sw("R3")}Republican {sw("A3")}Third ticket (unpledged electors, Byrd, Wallace)'
           + ('; Flips, under the map: the States that went to another party than at the last election dark, the others light' if has_prev else '') + '</span>')
    share = f'<span class="lk lk-s">The winner\'s margin over the runner-up, points of all the votes: {margin_scale(third=True)}</span>'
    swing = (f'<span class="lk lk-w">Swing from the last presidential election, points: {swing_scale()} '
             '<span class="lt">none where a party had no slate</span> ' + sw("NA") + 'None</span>') if has_sw else ""
    dots = ('<span class="lk lk-e">Electors, one dot each, as they voted: <span class="sw pD"></span>Democratic '
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


KEY = re.compile(r"^[hs] [A-Z]{2} \d+(-\d+)?( special)?$")


def reading_problems(R):
    """The readings schema (tools/elections/read.py): keys 'h NY 9', rows [name, party, votes(, lines)]."""
    out = []
    for part in ("races", "untabulated", "won", "wikipedia_differs", "not_in_volume"):
        for k in (R.get(part) or []):
            if not KEY.match(str(k)):
                out.append(f"{part}: '{k}' is not a key like 'h NY 9' or 's VA 1'")
    for k, v in (R.get("races") or {}).items():
        for r in (v or {}).get("cands") or []:
            if not (isinstance(r, list) and len(r) in (3, 4) and (r[2] is None or isinstance(r[2], int))):
                out.append(f"{k}: a row is not [name, party, votes] or [name, parties, total, lines]: {r}")
    for st, v in (R.get("president") or {}).items():
        for r in (v or {}).get("slates") or []:
            if not (isinstance(r, list) and len(r) == 2 and isinstance(r[1], int)):
                out.append(f"president {st}: a slate is not [party, votes]: {r}")
    return out


def problems():
    """For ./bib check: winners against seats, votes as integers, a source per election; electoral votes;
    a caucus for every winner and member of neither major party; no reading without its race."""
    out = []
    for c in range(85, 95):
        for ch in ("house", "senate"):
            for r in (roster(c) or {}).get(ch, []):
                if not r.get("vacant") and r.get("party") not in ("D", "R") and not third(r["name"].split(",")[0].strip().lower()):
                    out.append((f"congress/{c}.yaml", f"{r['name']} ({r['party']}): add the party caucused with to "
                                                      "elections/facts.yaml caucus:"))
    rd = os.path.join(DIR, "readings")
    for y, E in load().items():
        for r in E.get("races", []):
            for c in r["cands"]:
                if c.get("w") and c["p"] not in ("D", "R", "ID") and not third(surname(c["n"])):
                    out.append((f"elections/{y}.yaml", f"{r['ch']} {r['st']} {r['seat']}: {c['n']} ({c['party']}) won; add the party "
                                        "caucused with to elections/facts.yaml caucus:"))
        p = os.path.join(rd, f"{y}.yaml")
        try:
            R = store.load_yaml(p) if os.path.exists(p) else {}
        except Exception as e:
            out.append((f"elections/readings/{y}.yaml", f"does not load: {e}"))
            continue
        out += [(f"elections/readings/{y}.yaml", m) for m in reading_problems(R)]
        have = {f"{r['ch']} {r['st']} {r['seat']}" for r in E.get("races", [])} | \
               {f"{r['ch']} {r['st']} {r['seat']}-{r['position']}" for r in E.get("races", []) if r.get("position")}
        have |= {f"{r['ch']} {r['st']} {r['seat']} special" for r in E.get("races", []) if r.get("special")}
        for k in list((R.get("races") or {})) + list(R.get("untabulated") or []) + list(R.get("won") or {}):
            if k not in have:
                out.append((f"elections/readings/{y}.yaml", f"{k}: a reading for no race in elections/{y}.yaml"))
        pst = {r["st"] for r in (E.get("president") or {}).get("states", [])}
        for st in R.get("president") or {}:
            if st not in pst:
                out.append((f"elections/readings/{y}.yaml", f"president {st}: a reading for no State in elections/{y}.yaml"))
        if not (E.get("source") or {}).get("url"):
            out.append((f"elections/{y}.yaml", "election without a source"))
        for r in E.get("races", []):
            w = sum(1 for c in r["cands"] if c.get("w"))
            if w != r.get("seats", 1):
                out.append((f"elections/{y}.yaml", f"{r['ch']} {r['st']} {r['seat']}: {w} winners for {r.get('seats', 1)} seats"))
            for c in r["cands"]:
                if c.get("v") is not None and not isinstance(c["v"], int):
                    out.append((f"elections/{y}.yaml", f"{r['st']} {r['seat']}: votes not a number for {c['n']}"))
        P = E.get("president")
        if P:
            EV = {1956: 531, 1960: 537}.get(y, 538)
            got = sum(sum(r["cast"].values()) for r in P["states"])
            if got != EV:
                out.append((f"elections/{y}.yaml", f"president: {got} electoral votes, not {EV}"))
            for r in P["states"]:
                if sum(r["cast"].values()) != r["ev"]:
                    out.append((f"elections/{y}.yaml", f"president {r['st']}: electors cast {sum(r['cast'].values())} of {r['ev']}"))
                if any(not isinstance(x.get("v"), int) for x in r["slates"]):
                    out.append((f"elections/{y}.yaml", f"president {r['st']}: a slate without a vote"))
    return out
