"""Presidential primaries, 1960-1976: elections/pres-primaries.yaml, kept by hand from CQ's *Guide to U.S. Elections*,
6th ed. (2010), ch. 11 (header there).

A calendar entry tagged primary:<YYYY-MM-DD> carries the returns of that day's primaries, both parties; an entry
tagged primaries:<YYYY>-<R|D> (the opening of the party's convention) carries the party's primaries of the year: a
summary, a map of the States by winner (Result) and by the winner's margin (Margin), a key, and a table of the races.

STYLE
 1. Returns as CQ prints them: its names (the State in parentheses at a name's first appearance), votes, and
    printed shares ("—" for less than 0.05). A write-in (CQ's note 1) is marked "write-in". CQ's other notes on a
    race or a figure are quoted in the race's note, with their page and number ('CQ Guide 6th (2010) 405 n.5: “In
    addition to ...”'), but the one it repeats under a dozen races, which is paraphrased and cited ("Figures from
    Scammon's office; not in *America Votes*. CQ Guide 6th (2010) 411 n.4."). CQ's note on the year's heading is quoted in the block's sources. Nothing of CQ's is given
    in its words without quotation marks. Where a printed share does not fit the votes (more
    than 0.1 point off), the note gives both: "CQ prints 4.8 for Others; the votes give 4.4."
 2. The winner: the candidate or slate with the most votes, "Others" and "None of the names shown" aside. Margin:
    points of all the votes between the first two; the unopposed, and a race with one entry, "Unopposed".
 3. Who is who: a bare surname is the person CQ names in full under that surname earlier in the year's tables
    (Kennedy, 1968: Robert F.); NAMES settles the rest (Brown, 1976). The map and the summary count persons, not
    the forms of a name: Unpledged delegates and Unpledged delegates at large are one slate.
 4. The map: each State with a preference vote in the party's primary, by winner (a color a candidate, in order
    of States won, then votes; unpledged slates gray) or, in Margin, the winner's color paler as the race was
    closer, by the election maps' quantile rule. A State without a primary, or whose party printed none, is
    blank. The District of Columbia is a dot.
 5. Names in full, as the election tables give them: a bare surname by STYLE 3, the State CQ adds in parentheses
    left out; linked to the name entry where one person with an entry fits (namelinks.written). The figures are
    cited once, under the table, by the pages the races run over ("CQ Guide 6th (2010) 404–405"), not in each race's
    note; CQ's notes, in the note, by the page they are printed on and their number ("CQ Guide 6th (2010) 411 n.2").
 6. The Names entries: every primary in which CQ prints the person, a row in his record (person_rows): the party's
    primary in the State, the date linked to the calendar's entry for the day, every candidate with votes and
    CQ's share, the person in bold, and the pinpoint cite.
"""
import json
import os
import re
from collections import Counter, defaultdict

from . import store

PATH = os.path.join(store.ROOT, "elections", "pres-primaries.yaml")
NAMES = {(1976, "Brown"): "Edmund G. Brown Jr."}     # a bare surname the year's tables give in full nowhere
PARTY = {"R": "Republican", "D": "Democratic"}
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
NOT_A_PERSON = ("Others", "“None of the names shown”")
FILLS = 9                                             # candidate colors, q1-q9 (templates/congress.html)
CQ = "CQ Guide 6th (2010)"
_C = {}


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def load():
    if "d" not in _C:
        _C["d"] = {int(y): v for y, v in (store.load_yaml(PATH) or {}).items()} if os.path.exists(PATH) else {}
    return _C["d"]


def fmt_date(d, year=True):
    y, m, dd = str(d).split("-")
    return f"{MONTHS[int(m) - 1]} {int(dd)}" + (f", {y}" if year else "")


def bare(n):
    """'Richard M. Nixon (N.Y.)' -> 'Richard M. Nixon'; '(unpledged delegates)' stays."""
    return re.sub(r"\s*\((?:[A-Z][A-Za-z]*\.?\s?)+\)$", "", n).strip()


def surname(full):
    w = [x for x in bare(full).split() if x not in ("Jr.", "Sr.", "III")]
    return w[-1] if w else full


def people(y):
    """surname -> the first full name the year's tables give for it."""
    key = ("people", y)
    if key not in _C:
        out = {}
        for r in load()[y]["races"]:
            for p in "RD":
                for x in rows_of(r, p):
                    b = bare(x["n"])
                    if " " in b and not b.startswith("Unpledged") and b not in NOT_A_PERSON:
                        out.setdefault(surname(b), b)
        _C[key] = out
    return _C[key]


def who(y, n):
    """The person or slate a printed name stands for (STYLE 3)."""
    b = bare(n)
    if b.lower().startswith("unpledged delegates"):
        return "Unpledged delegates"
    if " " in b or b in NOT_A_PERSON or "-" in b:
        return b
    return NAMES.get((y, b)) or people(y).get(b, b)


def rows_of(r, p):
    v = r.get(p)
    return v if isinstance(v, list) else []


def share(x):
    return None if x["p"] == "—" else float(x["p"])


def ranked(y, r, p):
    """The party's rows with who, write-in, and order (votes, highest first; CQ's order kept for ties)."""
    out = []
    for i, x in enumerate(rows_of(r, p)):
        out.append(dict(x, who=who(y, x["n"]), wi=1 in (x.get("nfn") or []), i=i))
    return sorted(out, key=lambda x: (-x["v"], x["i"]))


def contenders(rs):
    return [x for x in rs if x["who"] not in NOT_A_PERSON]


def winner(y, r, p):
    c = contenders(ranked(y, r, p))
    return c[0] if c else None


def margin(y, r, p):
    rs = ranked(y, r, p)
    c = contenders(rs)
    tot = sum(x["v"] for x in rs)
    if not c or not tot or len(rs) == 1:
        return None
    second = max([x["v"] for x in rs if x is not c[0]] or [0])
    return round((c[0]["v"] - second) / tot * 100, 1)


def misprints(r, p):
    """(name, printed, from the votes) where a printed share is more than 0.1 point off its votes."""
    rs = rows_of(r, p)
    tot = sum(x["v"] for x in rs)
    out = []
    for x in rs:
        calc = x["v"] / tot * 100 if tot else 0
        printed = share(x)
        if (printed is None and calc >= 0.05) or (printed is not None and abs(printed - calc) > 0.1):
            out.append((x["n"], x["p"], calc))
    return out


def rid(y, r, p):
    return f"pq{y}-{r['date'][5:]}-{r['st']}-{p}"


def notes(y, r, p):
    """The race's note: CQ's notes on the State, the party's returns and its figures (write-ins aside), as printed;
    printed shares that do not fit the votes."""
    fn = (load()[y].get("footnotes") or {})
    nums = list(r.get("fn") or [])
    v = r.get(p)
    if isinstance(v, dict):
        nums += v.get("fn") or []
    for x in rows_of(r, p):
        nums += [n for n in (x.get("nfn") or []) if n != 1] + list(x.get("vfn") or [])
    seen, bits = set(), []
    for n in nums:
        if n not in seen and n in fn:
            seen.add(n)
            t = fn[n]
            at = f"{CQ} {load()[y].get('notes_page')} n.{n}"
            if "Scammon did not record vote totals" in t:     # the note CQ repeats under a dozen races: paraphrased
                bits.append(f"Figures from Scammon’s office; not in <i>America Votes</i>. {at}.")
            else:                                              # CQ's words, quoted
                bits.append(f"{at}: “{quote(t)}”")
    for name, printed, calc in misprints(r, p):
        bits.append(f"CQ prints {esc(printed)} for {esc(bare(name))}; the votes give {calc:.1f}.")
    return " ".join(bits)


def pages(r):
    """'404' or '404–405': the pages the race runs over."""
    return f"{r['page']}" + (f"–{r['page_to']}" if r.get("page_to") else "")


def cite(r):
    return f"{CQ} {pages(r)}"


SERIES = None    # set by inject: the series, for the candidates' name entries


def person_of(y, n):
    """The name entry a printed name stands for, where one person with an entry fits its full form; else None."""
    w = who(y, n)
    if SERIES is None or w in NOT_A_PERSON or w == "Unpledged delegates" or " " not in w or "(" in w:
        return None
    from . import namelinks
    hit = namelinks.written(SERIES, w)
    sfx = lambda n: (re.search(r"\b(Jr|Sr|II|III|IV)\.?$", n.strip()) or [None, ""])[1]
    return hit if hit and sfx(w) == sfx(hit) else None    # a son is not his father (Edmund G. Brown Jr.)


def name_html(y, x):
    """The candidate's full name (STYLE 5), linked to the name entry where one person fits."""
    w = who(y, x["n"])
    p = person_of(y, x["n"])
    if not p:
        return esc(w)
    from . import namelinks
    return f'<a class="nm" href="{esc(namelinks.url(SERIES, p))}">{esc(w)}</a>'


def quote(t):
    """CQ's words inside quotation marks: its own double quotes turned single; America Votes in italics."""
    t = esc(t).replace("“", "‘").replace("”", "’").replace("&quot;", "’")
    return re.sub(r"America Votes", "<i>America Votes</i>", t)


def cands(y, r, p):
    from .elections import pct_text
    rs = ranked(y, r, p)
    w = winner(y, r, p)
    out = []
    for x in sorted(rs, key=lambda x: x["i"]):          # CQ's order
        s = share(x)
        ss = pct_text(s) if s is not None else "—"
        cls = ' class="w"' if w is not None and x is not None and x["i"] == w["i"] else ""
        wi = ' <span class="ep">write-in</span>' if x["wi"] else ""
        out.append(f'<span class="ec"><span{cls}><span class="en">{name_html(y, x)}</span>{wi}</span>'
                   f'<span class="ev">{x["v"]:,}</span><span class="es">{ss}</span></span>')
    return "".join(out)


def race_row(y, r, p, head, note_col=True):
    from .congress import STATE
    st = "District of Columbia" if r["st"] == "DC" else STATE.get(r["st"], r["st"])
    if not rows_of(r, p):
        body, mg = f'<span class="en">No returns</span>', ""
    else:
        body = cands(y, r, p)
        m = margin(y, r, p)
        mg = f"{m:.1f} pts" if m is not None else "Unopposed"
    return (f'<tr id="{rid(y, r, p)}"><td>{head}<br><span title="{esc(st)}">{esc(r["st"])}</span></td>'
            f'<td class="ecs">{body}</td><td class="em">{mg}</td>'
            + (f'<td class="eno">{notes(y, r, p)}</td>' if note_col else "") + '</tr>')


def table_head(h, note_col=True):
    """The race table's head; the Note column only where a race in the table has a note."""
    return ('<table><colgroup><col class="c1"><col class="c2"><col class="c3">' + ('<col class="c4">' if note_col else "")
            + f'</colgroup><thead><tr><th>{h}</th><th>Candidates, votes, share</th><th>Margin</th>'
            + ("<th>Note</th>" if note_col else "") + '</tr></thead><tbody>')


def has_notes(y, pairs):
    return any(notes(y, r, p) for r, p in pairs)


def day_block(date, links=None):
    """The returns of the primaries held on a date, both parties: the calendar entry tagged primary:<date>."""
    y = int(date[:4])
    if y not in load():
        return ""
    races = [r for r in load()[y]["races"] if r["date"] == date]
    if not races:
        return ""
    pairs = [(r, p) for p in "RD" for r in races if p in r]
    nc = has_notes(y, pairs)
    rows = [race_row(y, r, p, f'<span title="{PARTY[p]}">{p}</span>', nc) for r, p in pairs]
    pgs = sorted({p_ for r in races for p_ in (r["page"], r.get("page_to") or r["page"])})
    more = ""
    if links:
        more = " The year's primaries by party: " + ", ".join(
            f'<a href="{esc(h)}">{PARTY[p]}</a>' for p, h in links) + "."
    return ('<div class="cg sprace pq"><details class="cgr er esp" open><summary>The primaries, '
            f'{esc(fmt_date(date))}</summary>' + table_head("Party<br>State", nc) + "".join(rows) +
            f'</tbody></table></details><p class="elsrc">{CQ} {"–".join(str(x) for x in pgs[:1] + pgs[1:][-1:])}.{more}</p></div>')


def year_races(y, p):
    return [r for r in load()[y]["races"] if p in r]


def standings(y, p):
    """[(who, states won, votes)] in order of States won, then votes; the fill each takes."""
    won, votes = Counter(), Counter()
    for r in year_races(y, p):
        w = winner(y, r, p)
        if w:
            won[w["who"]] += 1
        for x in ranked(y, r, p):
            votes[x["who"]] += x["v"]
    order = sorted(votes, key=lambda k: (-won[k], -votes[k]))
    fills, k = {}, 0
    for n in order:
        if not won[n]:
            continue
        if n == "Unpledged delegates":
            fills[n] = "qU"
        else:
            k += 1
            fills[n] = f"q{k}" if k <= FILLS else "pO"
    return [(n, won[n], votes[n]) for n in order], fills


def record(y, r, p, fills):
    w = winner(y, r, p)
    if not w:
        return None
    rs = ranked(y, r, p)
    tot = sum(x["v"] for x in rs)
    top = ", ".join(f'{who(y, x["n"])} {x["p"]}%' + (" (write-in)" if x["wi"] else "") for x in rs[:3] if x["v"])
    m = margin(y, r, p)
    t = f'{r["st"]}, {fmt_date(r["date"], False)}: {top}' + (f"; by {m:.1f} pts" if m is not None else "; unopposed")
    return {"id": rid(y, r, p), "f": fills.get(w["who"], "pO"), "mg": 100 if m is None else m, "t": t, "v": tot}


def block(y, p, day_links=None):
    """The party's primaries of the year: summary, map, key, table (the entry tagged primaries:<y>-<p>)."""
    if y not in load():
        return ""
    races = year_races(y, p)
    stand, fills = standings(y, p)
    q = {}
    for r in races:
        rec = record(y, r, p, fills)
        if rec:
            q[r["st"]] = rec
    total = sum(x["v"] for r in races for x in rows_of(r, p))
    printed = (load()[y].get("totals") or {}).get(p)
    with_vote = [r for r in races if rows_of(r, p)]
    first, last = with_vote[0]["date"], with_vote[-1]["date"]
    dc = any(r["st"] == "DC" for r in with_vote)
    nst = len({r["st"] for r in with_vote}) - (1 if dc else 0)
    summary = [f"{len(with_vote)} primaries with returns, {fmt_date(first, False)} to {fmt_date(last, False)}: "
               f"{nst} States" + (" and the District of Columbia" if dc else "") + f". {total:,} votes."]
    wins = [f"{n} {k}" for n, k, v in stand if k]
    summary.append("States won: " + "; ".join(wins) + ".")
    lead = [f"{n} {v:,} ({v / total * 100:.1f}%)" for n, k, v in sorted(stand, key=lambda x: -x[2])
            if v and n not in NOT_A_PERSON][:6]
    summary.append("Votes: " + "; ".join(lead) + ".")
    key = " ".join(f'<span class="sw {fills[n]}"></span>{esc(n)}' for n, k, v in stand if k and n in fills)
    key = (f'<p class="cgkey elkey"><span class="lk lk-r lk-s">{key} <span class="sw eNone"></span>No primary, or none '
           f'printed. </span><span class="lk lk-s">The winner\'s color, lightest at a tie and darker as the margin '
           f'grows, by the election maps\' quantile rule: 5 points a fifth of the way, 14 half, 41 nine-tenths; '
           f'the unopposed darkest.</span></p>')
    rows = []
    nc = has_notes(y, [(r, p) for r in races])
    for r in races:
        head = fmt_date(r["date"], False)
        if day_links and r["date"] in day_links:
            head = f'<a href="{esc(day_links[r["date"]])}">{esc(head)}</a>'
        rows.append(race_row(y, r, p, head, nc))
    star = load()[y].get("star")
    src = (f'{CQ} {load()[y]["pages"]}: Congressional Quarterly, <i>Guide to U.S. Elections</i>, 6th ed. (2010), ch. 11, '
           '"Presidential Primary Returns, 1912–2008." Votes and shares as CQ prints them; its notes in the races\' notes. '
           + (f"CQ on the year: “{quote(star)}” " if star else "")
           + (f"CQ's total, {printed:,}, is the sum of the races." if printed == total else
              f"CQ prints a total of {printed:,}; the races add to {total:,}." if printed else ""))
    seats = json.dumps({"q": q}, ensure_ascii=False, separators=(",", ":"))
    return (f'<div class="cg el pq" data-cg="pq{y}{p}" id="pq{y}{p}">'
            f'<p class="cgh">The {PARTY[p]} primaries, {y}</p>'
            + "".join(f'<p class="elsum">{esc(s)}</p>' for s in summary)
            + f'<script type="application/json" class="cgseats">{seats}</script>'
            f'<div class="cgmaps"><figure class="cgmap" data-chamber="q"><figcaption>{PARTY[p]} primaries, {y}, '
            f'by State</figcaption><div class="cgv" style="aspect-ratio:960/660"></div></figure></div>'
            f'<span data-views="r s"></span>{key}'
            f'<details class="cgr er esp"><summary>Primaries, {len(races)}, by date</summary>'
            + table_head("Date<br>State", nc) + "".join(rows) + "</tbody></table></details>"
            f'<p class="elsrc">{src}</p></div>')


def tagged(series):
    """{('day', date) | ('party', (y, p)): entry id} for the calendar's tagged entries."""
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^primary:(\d{4}-\d\d-\d\d)$", t)
                if m:
                    out[("day", m.group(1))] = e["id"]
                m = re.match(r"^primaries:(\d{4})-([RD])$", t)
                if m:
                    out[("party", (int(m.group(1)), m.group(2)))] = e["id"]
    return out


def inject(page, series):
    """Put the tagged entries' returns and maps into a built page (after congress.inject, whose assets the maps use)."""
    global SERIES
    SERIES = series
    tags = tagged(series)
    if not tags:
        return page
    days = {d: f"#{eid}" for (k, d), eid in tags.items() if k == "day"}
    used = False
    for (k, v), eid in tags.items():
        if k == "day":
            y = int(v[:4])
            links = [(p, f"#{tags[('party', (y, p))]}") for p in "RD" if ("party", (y, p)) in tags]
            blk = day_block(v, links)
        else:
            blk = block(v[0], v[1], days)
            used = used or bool(blk)
        if not blk:
            continue
        pat = re.compile(r'(<li id="' + re.escape(eid) + r'"[^>]*>.*?)(</li>)', re.S)
        page = pat.sub(lambda mm: mm.group(1) + blk + mm.group(2), page, count=1)
    if used and 'id="cggeo"' not in page:
        from . import congress
        data, geo = congress.load()
        if geo:
            page = page.replace("</body>", congress.assets(congress.geo_subset(geo, [])) + "\n</body>", 1)
    from . import roster
    return roster.ensure(page)


def problems(series=None):
    """The file: States, dates, notes that answer, votes that add to CQ's totals; the calendar's tags."""
    from .congress import STATE
    where = "elections/pres-primaries.yaml"
    out = []
    for y, Y in load().items():
        fn = Y.get("footnotes") or {}
        for r in Y.get("races") or []:
            if r.get("st") not in STATE and r.get("st") != "DC":
                out.append((where, f"{y}: {r.get('st')}: not a State"))
            if not re.fullmatch(rf"{y}-\d\d-\d\d", str(r.get("date"))):
                out.append((where, f"{y}: {r.get('st')}: bad date {r.get('date')}"))
            for p in "RD":
                v = r.get(p)
                nums = list(r.get("fn") or []) + (list(v.get("fn") or []) if isinstance(v, dict) else [])
                for x in rows_of(r, p):
                    nums += list(x.get("nfn") or []) + list(x.get("vfn") or [])
                for n in nums:
                    if n not in fn:
                        out.append((where, f"{y} {r['st']} {p}: note {n} not among the year's notes"))
        for p in "RD":
            tot = sum(x["v"] for r in Y.get("races") or [] for x in rows_of(r, p))
            if (Y.get("totals") or {}).get(p) not in (None, tot):
                out.append((where, f"{y} {p}: the races add to {tot:,}, CQ prints {Y['totals'][p]:,}"))
    if series is not None:
        for (k, v), eid in tagged(series).items():
            if k == "day" and not any(r["date"] == v for r in (load().get(int(v[:4])) or {}).get("races", [])):
                out.append((eid, f"primary:{v}: no primaries that day"))
            if k == "party" and (v[0] not in load() or not year_races(*v)):
                out.append((eid, f"primaries:{v[0]}-{v[1]}: no such primaries"))
    return out
