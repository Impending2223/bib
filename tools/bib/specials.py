"""Special elections during each Congress, and party switches in office: congress/specials.yaml (made by
tools/congress/make_specials.py, which see) and congress/switches.yaml (kept by hand).

congress.html puts, after each Congress at its opening, the specials held between general elections:
a summary, House and Senate maps of the seats filled (the election blocks' views: Result, Margin,
Swing), and a table of the races. Specials held with the November election are in that election's block,
from the Clerk's returns; they are not repeated here. A calendar entry tagged special:<key> carries its
race's table. The rosters' notes take each special's date and each switch from here.

Votes read from a State's own returns are kept by hand in congress/specials-state.yaml (keyed by the race's
key; header there) and laid over the generated file when it loads: the race then has votes by round and
cites the State's publication and page. sources/states.yaml says where each State's returns are.

STYLE:
 1. Votes and shares from the State's own returns where read (specials-state.yaml), by round: an open
    first round (a California special primary) before the deciding one; party primaries are not rounds.
    Each round is headed by its label and date only where there are two; one round needs neither.
    Next, CQ's *Guide to U.S. Elections* (specials-cq.yaml): votes and its printed shares, which count the
    candidates it does not print ("Its shares count 1.3 points for candidates it does not print"); a round
    CQ dates by year only shows the year. Otherwise Wikipedia's shares, in percent, no votes; Texas, 1961,
    votes from Bartley and Graham.
    Shares are of all the votes cast, scattering included. Margin: points between the first two.
 2. Pickup: the winner's party differs from the departed member's. A member re-elected to his own seat
    under another party (Watson, 1965) counts so, and the note says so.
 3. Swing: the change in the Democratic share of the two-party vote from the general election that
    chose the Congress, in the same district (the lines do not change within a Congress); none where
    either race lacked a Democrat or a Republican. Under the margin in the tables ("swing 2.3 to R").
    Net change: as for the general elections, the gaining party's seats, from the departed members to
    the winners ("net change: R+1").
 4. "Check" in a race's note marks what the sources disagree on (a date, shares that do not add to 100).
"""
import json
import os
import re
from collections import Counter, defaultdict

from . import store

DIR = os.path.join(store.ROOT, "congress")
NAME = {"D": "Democratic", "R": "Republican"}
PLURAL = {"D": "Democrats", "R": "Republicans"}
PARTY_LONG = {"D": "Democrat", "R": "Republican", "I": "Independent"}
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def fmt_date(d):
    if re.fullmatch(r"\d{4}", str(d)):
        return str(d)                    # a year only (CQ's first rounds)
    y, m, dd = str(d).split("-")
    return f"{MONTHS[int(m) - 1]} {int(dd)}, {y}"


def readings(name="specials-state.yaml"):
    p = os.path.join(DIR, name)
    return (store.load_yaml(p) or {}) if os.path.exists(p) else {}


def cq_readings():
    """congress/specials-cq.yaml: votes and printed shares from CQ's *Guide to U.S. Elections* (header there)."""
    return readings("specials-cq.yaml")


def load():
    """specials.yaml, with the votes read from the States' returns (specials-state.yaml) laid over it."""
    p = os.path.join(DIR, "specials.yaml")
    data = {int(k): v for k, v in (store.load_yaml(p) or {}).items()} if os.path.exists(p) else {}
    R, Q = readings(), cq_readings()
    for xs in data.values():
        for x in xs:
            r = R.get(x["key"])
            if r and r.get("pending"):
                x["pending"] = r["pending"]
            if not r or not r.get("rounds"):
                r = Q.get(x["key"])     # CQ's figures where the State's are not read
                if r and r.get("unopposed"):
                    x["wiki"] = x.get("cands")
                    x["cands"] = [[r["unopposed"][0], r["unopposed"][1], None, "won"]]
                    x["source"], x["state"], x["cq"], x["url"] = r["cite"], True, True, r.get("url")
                    x["check"] = None
                    if r.get("note"):
                        x["note"] = r["note"]
                    continue
                if not r or not r.get("rounds"):
                    continue
                x["cq"] = True
            x["wiki"] = x.get("cands")
            x["rounds"] = [{"date": str(rd["date"]), "label": rd["label"],
                            "cands": rd["cands"] + ([["Scattering", "", rd["scattering"]]] if rd.get("scattering") else [])}
                           for rd in r["rounds"]]
            x["source"] = r.get("cite") or (f"{r['source']}, {r['where']}" if r.get("where") else r["source"])
            x["state"] = True
            x["url"] = r.get("url")
            if x.get("check"):   # Wikipedia's shares no longer stand
                x["check"] = re.sub(r"\s*The shares in the source add to [\d.]+%\.", "", x["check"]).strip() or None
            if r.get("note"):
                x["note"] = r["note"]
    return data


def switches():
    p = os.path.join(DIR, "switches.yaml")
    return store.load_yaml(p) or [] if os.path.exists(p) else []


def between(c, data=None):
    """The specials held between general elections during Congress c."""
    return [x for x in (data or load()).get(c, []) if not x.get("with_general")]


def rid(x):
    return f"e{x['date']}-sp-{x['ch']}-{x['st']}-{x['seat']}"


def ordinal(n):
    return f"{n}{'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def seat_label(x):
    """MA-6, VT-AL."""
    return f"{x['st']}-{'AL' if x['seat'] == 0 else x['seat']}"


def cite_html(text, url=None, access=None):
    """A short citation: *Title* in italics, linked to the copy read; '(bot-check)' and the like where the copy is gated."""
    t = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", esc(text))
    if url:
        t = f'<a href="{esc(url)}">{t}</a>'
    return t + (f" ({esc(access)})" if access and access != "open" else "")


def surname(n):
    """The surname, accents folded ('González' and CQ's 'Gonzalez' are one)."""
    import unicodedata
    n = re.sub(r",? (Jr|Sr|II|III|IV)\.?$", "", re.sub(r"\s*\(.*?\)\s*", " ", n).strip())
    n = "".join(ch for ch in unicodedata.normalize("NFD", n) if not unicodedata.combining(ch))
    return n.split()[-1] if n.split() else n


# ---------------------------------------------------------------- the figures

def final(x):
    """[(name, party, votes or None, share or None, won)] of the deciding round."""
    if x.get("rounds"):
        rows = x["rounds"][-1]["cands"]
        tot = sum(r[2] for r in rows)
        return [(r[0], r[1], r[2], share(r, tot), r[0] == x["winner"] or surname(r[0]) == surname(x["winner"]))
                for r in sorted(rows, key=lambda r: -r[2])]
    return [(r[0], r[1], None, r[2], len(r) > 3 and r[3] == "won") for r in x.get("cands") or []]


def share(r, tot):
    """A candidate's share: as printed where the source prints one (CQ's, of all the votes, its unprinted
    candidates' included), else of the round's votes."""
    if len(r) > 3 and isinstance(r[3], (int, float)):
        return float(r[3])
    return 100 * r[2] / tot if tot else None


def unprinted(rd):
    """Points of the round's vote that went to candidates the source does not print (CQ's shares short of 100)."""
    sh = [c[3] for c in rd["cands"] if len(c) > 3 and isinstance(c[3], (int, float))]
    return round(100 - sum(sh), 1) if sh and len(sh) == len(rd["cands"]) else 0


def margin(rows):
    sh = sorted((r[3] for r in rows if r[3] is not None), reverse=True)
    return round(sh[0] - sh[1], 1) if len(sh) > 1 else None


def dshare(rows):
    d = max((r[3] for r in rows if str(r[1]).split(",")[0] == "D" and r[3] is not None), default=None)
    r_ = max((r[3] for r in rows if str(r[1]).split(",")[0] == "R" and r[3] is not None), default=None)
    return 100 * d / (d + r_) if d and r_ else None


def general_dshare(c, x, edata):
    from . import elections
    E = edata.get(1960 + 2 * (c - 87))
    if not E:
        return None
    for r in E["races"]:
        if r["ch"] == x["ch"] and r["st"] == x["st"] and r["seat"] == x["seat"] and not r.get("special"):
            m = elections.metrics(r)
            return None if m.get("unopposed") else m.get("dshare")
    return None


def record(c, x, edata):
    rows = final(x)
    p = x["party"] if x["party"] in ("D", "R") else "O"
    rec = {"p": p, "n": surname(x["winner"]), "id": rid(x), "k": "pickup" if x.get("flip") else "held"}
    rec["d" if x["ch"] == "h" else "cl"] = x["seat"]
    w = next((r for r in rows if r[4]), None)
    if w and w[3] is not None:
        rec["sh"] = round(w[3], 1)
        mg = margin(rows)
        if mg is not None:
            rec["mg"] = mg
    else:
        rec["sh"], rec["u"] = 100.0, 1
    sw = swing(c, x, edata)
    if sw is not None:
        rec["sw"], rec["swb"] = sw, "seat"
    return rec


def swing(c, x, edata):
    """Points toward the Democrats (+) or Republicans (−), from the general election in the same seat."""
    a, b = dshare(final(x)), general_dshare(c, x, edata)
    return round(a - b, 1) if a is not None and b is not None else None


def swing_words(v):
    return "no swing" if abs(v) < 0.05 else f"swing {abs(v):.1f} to {'D' if v > 0 else 'R'}"


# ---------------------------------------------------------------- the block

def summary(c, sp):
    out = []
    for ch, label in (("h", "House"), ("s", "Senate")):
        xs = [x for x in sp if x["ch"] == ch]
        if not xs:
            continue
        held = Counter(x["party"] for x in xs if not x.get("flip"))
        gains = Counter(x["party"] for x in xs if x.get("flip"))
        bits = [f"{PLURAL.get(p, p)} held {n}" for p, n in sorted(held.items())]
        for p, n in sorted(gains.items()):
            where = ", ".join((seat_label(x) if ch == "h" else x["st"]) for x in xs if x.get("flip") and x["party"] == p)
            bits.append(f"{NAME.get(p, p)} pickup{'s' if n > 1 else ''} {n} ({where})")
        from .elections import net_change
        net = net_change(Counter(x["out_party"] for x in xs), Counter(x["party"] for x in xs))
        nets = f"; net change: {net}" if net != "none" else ""
        out.append(f"{label}, {len(xs)} special election{'s' if len(xs) > 1 else ''}: " + "; ".join(bits) + nets + ".")
    return out


def cand_cell(rows, votes):
    out = []
    for name, party, v, share, won in rows:
        cls = ' class="w"' if won else ""
        vv = f"{v:,}" if votes and v is not None else ""
        ss = f"{share:.1f}%" if share is not None else "Unopposed"
        out.append(f'<span class="ec"><span{cls}><span class="en">{esc(name)}</span> <span class="ep">{esc(party)}</span></span>'
                   f'<span class="ev">{vv}</span><span class="es">{ss}</span></span>')
    return "".join(out)


def note_cell(x):
    bits = [f"{esc(x['out'])} ({esc(x['out_party'])}): {esc(x['why'].rstrip('.'))}."]
    if x.get("flip"):
        same = surname(x["out"]) == surname(x["winner"])
        bits.append(f"{NAME.get(x['party'], x['party'])} pickup" + (", the same member under another party." if same else "."))
    if x.get("note"):
        bits.append(esc(x["note"]))
    if x.get("state"):
        bits.append(f"Votes: {cite_html(x['source'], x.get('url'))}.")
        left = unprinted(x["rounds"][-1]) if x.get("rounds") else 0
        if left >= 0.5:
            bits.append(f"Its shares count {left:.1f} points for candidates it does not print.")
    for c in x.get("pending") or []:
        bits.append(f"Check: {cite_html(c['cite'], c.get('url'), c.get('access'))}.")
    if x.get("check"):
        bits.append(f"Check: {esc(x['check'])}")
    return " ".join(bits)


def table(c, sp, edata, open_=False):
    from .congress import STATE
    out = [f'<details class="cgr er"{" open" if open_ else ""}><summary>Races, {len(sp)}, by date</summary><table>'
           '<colgroup><col class="c1"><col class="c2"><col class="c3"><col class="c4"></colgroup>'
           '<thead><tr><th>Date, seat</th><th>Candidates, votes, share</th><th>Margin</th><th>Vacancy; note</th></tr></thead><tbody>']
    out += [row(x, STATE, swing(c, x, edata)) for x in sp]
    out.append("</tbody></table></details>")
    return "\n".join(out)


def row(x, STATE, sw=None):
    where = (f'<span title="{esc(STATE[x["st"]])}">{seat_label(x)}</span>' if x["ch"] == "h"
             else f'<span title="{esc(STATE[x["st"]])}, class {("I", "II", "III")[x["seat"] - 1]}">{x["st"]}, Senate</span>')
    cells = []
    if x.get("rounds"):
        for rd in x["rounds"]:
            tot = sum(r[2] for r in rd["cands"])
            rows = [(r[0], r[1], r[2], share(r, tot), rd is x["rounds"][-1] and surname(r[0]) == surname(x["winner"]))
                    for r in sorted(rd["cands"], key=lambda r: -r[2])]
            head = (f'<span class="eln">{esc(rd["label"].capitalize())}, {esc(fmt_date(rd["date"]))}</span>'
                    if len(x["rounds"]) > 1 else "")
            cells.append(head + cand_cell(rows, True))
        rows = final(x)
    else:
        rows = final(x)
        cells.append(cand_cell(rows, False))
    mg = margin(rows)
    # one candidate printed with a share short of all (CQ's Cardiss Collins, 92.5): the margin is not known
    partial = mg is None and len(rows) == 1 and rows[0][3] is not None and rows[0][3] < 99.95
    mcell = f"{mg:.1f} pts" if mg is not None else ("—" if partial else "Unopposed")
    if sw is not None:
        mcell += f'<br><span class="es">{swing_words(sw)}</span>'
    wp = x["party"] if x["party"] in ("D", "R") else ""
    return (f'<tr id="{rid(x)}" class="{"pk" if x.get("flip") else ""} w{wp}"><td>{esc(fmt_date(x["date"]))}<br>{where}</td>'
            f'<td class="ecs">{"".join(cells)}</td><td class="em">{mcell}</td><td class="eno">{note_cell(x)}</td></tr>')


def legend(has_sw):
    from .elections import margin_scale, swing_scale
    sw = lambda k: f'<span class="sw e{k}"></span>'
    res = (f'<span class="lk lk-r">{sw("B2")}Democratic held {sw("B4")}Democratic pickup '
           f'{sw("R2")}Republican held {sw("R4")}Republican pickup {sw("None")}No special election</span>')
    share = f'<span class="lk lk-s">The winner\'s margin over the runner-up, points of all the votes: {margin_scale()}</span>'
    swing = (f'<span class="lk lk-w">Swing from the general election that chose the Congress, same district, points: '
             f'{swing_scale()} {sw("NA")}None</span>') if has_sw else ""
    return f'<p class="cgkey elkey">{res}{share}{swing}</p>'


def block(c, edata=None):
    """The specials held between general elections during Congress c, or ''."""
    from . import elections
    edata = edata if edata is not None else elections.load()
    sp = between(c)
    if not sp:
        return ""
    seats = {"h": defaultdict(list), "s": defaultdict(list)}
    for x in sp:
        seats[x["ch"]][x["st"]].append(record(c, x, edata))
    has_sw = any("sw" in r for ch in seats.values() for v in ch.values() for r in v)
    out = [f'<div class="cg el sp" data-cg="{c}" data-ev="sp{c}">']
    out.append(f'<p class="cgh">Special elections during the {ordinal(c)} Congress</p>')
    for line in summary(c, sp):
        out.append(f'<p class="elsum">{esc(line)}</p>')
    out.append(f'<script type="application/json" class="cgseats">{json.dumps(seats, ensure_ascii=False, separators=(",", ":"))}</script>')
    figs = ""   # a map for each chamber that had a special
    if seats["h"]:
        figs += ('<figure class="cgmap dots" data-chamber="h"><figcaption>House, by delegation</figcaption>'
                 '<div class="cgv" style="aspect-ratio:1085/660"></div></figure>')
    if seats["s"]:
        figs += ('<figure class="cgmap" data-chamber="s"><figcaption>Senate, by state</figcaption>'
                 '<div class="cgv" style="aspect-ratio:960/660"></div></figure>')
    out.append(f'<div class="cgmaps">{figs}</div><span data-views="r s{" w" if has_sw else ""}"></span>')
    out.append(legend(has_sw))
    out.append(table(c, sp, edata))
    out.append('<p class="elsrc">Specials held between general elections; those held with the November election are in its '
               'block, from the Clerk. Returns: Wikipedia\'s tables of each year\'s House specials, which give shares, not votes; '
               'Texas, 1961: votes from Bartley and Graham, <i>Southern Elections</i>. The official returns are the States\' '
               'canvasses: the Clerk\'s biennial <i>Statistics</i> print only the November elections. Swing: from the general '
               'election that chose the Congress, in the same district.</p>')
    out.append("</div>")
    return "\n".join(out)


def race_block(key, edata=None):
    """One race's table, for the calendar entry tagged special:<key>."""
    from .congress import STATE
    from . import elections
    edata = edata if edata is not None else elections.load()
    for c, xs in load().items():
        for x in xs:
            if x["key"] == key:
                src = re.sub(r"[*]([^*]+)[*]", r"<i>\1</i>", esc(x.get("source", "")))   # *Title* in italics
                return ('<div class="cg sprace"><details class="cgr er" open><summary>The special election, '
                        f'{esc(fmt_date(x["date"]))}</summary><table>'
                        '<colgroup><col class="c1"><col class="c2"><col class="c3"><col class="c4"></colgroup>'
                        '<thead><tr><th>Date, seat</th><th>Candidates, votes, share</th><th>Margin</th><th>Vacancy; note</th></tr></thead><tbody>'
                        + row(x, STATE, swing(c, x, edata)) + '</tbody></table></details>'
                        f'<p class="elsrc">{src}. <a href="congress.html#{rid(x)}">All the specials of the '
                        f'{ordinal(c)} Congress</a>.</p></div>')
    return ""


def inject(page, series):
    """Put each tagged calendar entry's race into a built page."""
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^special:(.+)$", t)
                if m:
                    blk = race_block(m.group(1))
                    pat = re.compile(r'(<li id="' + re.escape(e["id"]) + r'"[^>]*>.*?)(</li>)', re.S)
                    page = pat.sub(lambda mm: mm.group(1) + blk + mm.group(2), page, count=1)
    if 'class="cg sprace"' in page:
        from . import roster
        page = roster.ensure(page)
    return page


# ---------------------------------------------------------------- roster notes

def for_change(c, x, data=None):
    """The special that filled a seat in congress/changes.yaml, if one: same seat, the successor's surname."""
    for s in (data or load()).get(c, []):
        if s["ch"] == x["ch"] and s["st"] == x["st"] and s["seat"] == x["seat"] and x.get("into") and \
                surname(s["winner"] or "") == surname(x["into"]):
            return s
    return None


def switch_for(c, ch, st, seat):
    return [s for s in switches() if s["cong"] == c and s["ch"] == ch and s["st"] == st and s["seat"] == seat]


def switch_note(s):
    t = f"Changed party, {fmt_date(s['date'])}: {PARTY_LONG.get(s['from'], s['from'])} to {PARTY_LONG.get(s['to'], s['to'])}."
    return t + (f" {s['note']}" if s.get("note") else "")


# ---------------------------------------------------------------- check

def problems(series=None):
    out = []
    data = load()
    keys = Counter(x["key"] for xs in data.values() for x in xs)
    byk = {x["key"]: x for xs in data.values() for x in xs}
    for k, r in readings().items():
        where = f"congress/specials-state.yaml {k}"
        if k not in byk:
            out.append((where, "no such special in congress/specials.yaml"))
            continue
        if not r.get("rounds"):
            continue
        if not r.get("source"):
            out.append((where, "no source"))
        for rd in r["rounds"]:
            tot = sum(c[2] for c in rd["cands"])   # a printed total may or may not count the scattering
            if rd.get("total") is not None and rd["total"] not in (tot, tot + (rd.get("scattering") or 0)):
                out.append((where, f"{rd['label']}: the votes add to {tot:,} (with scattering "
                                   f"{tot + (rd.get('scattering') or 0):,}), the printed total is {rd['total']:,}"))
        if not any(surname(c[0]) == surname(byk[k]["winner"]) for c in r["rounds"][-1]["cands"]):
            out.append((where, f"the winner, {byk[k]['winner']}, is not in the last round"))
    for k, r in cq_readings().items():
        where = f"congress/specials-cq.yaml {k}"
        if k not in byk:
            out.append((where, "no such special in congress/specials.yaml"))
            continue
        if not r.get("cite"):
            out.append((where, "no cite"))
        if r.get("unopposed"):
            if surname(r["unopposed"][0]) != surname(byk[k]["winner"]):
                out.append((where, f"the winner, {byk[k]['winner']}, is not the unopposed candidate"))
            continue
        for rd in r.get("rounds") or []:
            # one total behind every printed share: each candidate's votes over his share (rounded to 0.1) bound it
            lo, hi = 0, float("inf")
            printed = [c for c in rd["cands"] if len(c) > 3 and c[3]]
            if printed and len(printed) < len(rd["cands"]):
                out.append((where, f"{rd['label']}: shares printed for some candidates, not all"))
            for c in printed:
                lo, hi = max(lo, c[2] / ((c[3] + 0.05) / 100)), min(hi, c[2] / ((c[3] - 0.05) / 100) if c[3] > 0.05 else hi)
            if lo > hi + 1:
                out.append((where, f"{rd['label']}: the votes and printed shares cannot come from one total"))
            if sum(c[2] for c in rd["cands"]) > hi + 1:
                out.append((where, f"{rd['label']}: the votes add to more than the shares allow"))
        if r.get("rounds") and not any(surname(c[0]) == surname(byk[k]["winner"]) for c in r["rounds"][-1]["cands"]):
            out.append((where, f"the winner, {byk[k]['winner']}, is not in the last round"))
    out += [("congress/specials.yaml", f"duplicate key {k}") for k, n in keys.items() if n > 1]
    for s in switches():
        p = os.path.join(DIR, f"{s['cong']}.yaml")
        if not os.path.exists(p):
            out.append(("congress/switches.yaml", f"{s['name']}: no roster for the {s['cong']}th Congress"))
            continue
        R = store.load_yaml(p)
        rows = R["house" if s["ch"] == "h" else "senate"]
        if not any(r["st"] == s["st"] and (r.get("d") if s["ch"] == "h" else r.get("cl")) == s["seat"] and
                   surname(s["name"]) in r.get("name", "") for r in rows):
            out.append(("congress/switches.yaml", f"{s['name']}: not at {s['st']} {s['seat']} in the {s['cong']}th Congress"))
    if series is not None:
        known = set(keys)
        for lst in series.lists.values():
            if lst.kind != "calendar":
                continue
            for sec, e in lst.entries():
                for t in e.get("tags", []):
                    if t.startswith("special:") and t[8:] not in known:
                        out.append((e["id"], f"tag {t}: no such special in congress/specials.yaml"))
    return out
