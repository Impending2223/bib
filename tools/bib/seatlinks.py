"""The links between the Congress rosters and the elections: each member at an opening to the election that seated him
and the seat's next election; each race forward to the roster that holds its seat next; each presidential election
to the Executive roster's term.

A seat is (chamber, State, district or class). Its elections, in order of date: the November races
(elections/<year>.yaml, 1956-1974; 1956 is a base and has no block, so it shows unlinked) and the specials between
them (congress/specials.yaml). House districts are numbered anew at each reapportionment: a member's next race is
the one in his State that names him (by surname) where one race does, else the race for the same number.

STYLE: one muted line under the member, "Elected Nov. 8, 1960. Next: Nov. 6, 1962." ("Seat filled", with the winner,
where the member did not win the seat's last election: an appointed Senator); under a race, "Roster: 87th Cong.".
"""
import re
from collections import defaultdict

from . import store

_cache = {}


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def letters(s):
    from .lives import letters as L
    return L(s)


def surname_of(n):
    """The last word of a name as the returns print it, its suffix dropped: 'Harry F. Byrd Jr.' -> 'Byrd'."""
    ws = [w for w in re.sub(r",", " ", n or "").split() if not re.fullmatch(r"(Jr|Sr|II|III|IV)\.?", w)]
    return ws[-1] if ws else ""


def agrees(roster_name, returns_name):
    """The roster's surname (one or more words) ends the returns' name."""
    sur = roster_name.split(",")[0]
    ws = [w for w in re.sub(r",", " ", returns_name or "").split() if not re.fullmatch(r"(Jr|Sr|II|III|IV)\.?", w)]
    return any(letters(" ".join(ws[-k:])) == letters(sur) for k in (1, 2, 3) if len(ws) > k)


def events():
    """{(ch, st, seat): [(date, href or None, label, [winners], [candidates], year or None)]} by date."""
    if "events" in _cache:
        return _cache["events"]
    from . import elections, specials
    out = defaultdict(list)
    for y, E in sorted(elections.load().items()):
        for r in E["races"]:
            href = None if y == 1956 else f"congress.html#{elections.rid(y, r)}"
            lab = elections.fmt_date(E["date"]) + (" (special)" if r.get("special") else "")
            out[(r["ch"], r["st"], r["seat"])].append(
                (E["date"], href, lab, [c["n"] for c in r["cands"] if c.get("w")], [c["n"] for c in r["cands"]], y))
    sp = specials.load()
    for c in sorted(sp):
        for x in specials.between(c, sp):
            names = [row[0] for row in specials.final(x)]
            out[(x["ch"], x["st"], x["seat"])].append(
                (x["date"], f"congress.html#{specials.rid(x)}",
                 specials.fmt_date(x["date"]) + (" (first election)" if x.get("new") else " (special)"),
                 [x["winner"]], names, None))
    for k in out:
        out[k].sort(key=lambda e: e[0])
    _cache["events"] = out
    return out


def by_year_state():
    """{(year, ch, st): [(seat, event)]}: the November races, for finding a member's next race in his State."""
    if "bys" in _cache:
        return _cache["bys"]
    out = defaultdict(list)
    for (ch, st, seat), evs in events().items():
        for e in evs:
            if e[5]:
                out[(e[5], ch, st)].append((seat, e))
    _cache["bys"] = out
    return out


def link(e, here):
    if not e[1]:
        return esc(e[2])
    href = e[1].replace("congress.html", "") if here else e[1]
    return f'<a href="{href}">{esc(e[2])}</a>'


def member_line(c, opened, ch, st, seat, name, here=False):
    """The muted line under a member at Congress c's opening: the election before, the seat's next. HTML or ''."""
    evs = events().get((ch, st, seat), [])
    before = [e for e in evs if e[0] < opened]
    after = [e for e in evs if e[0] > opened]
    won = lambda e: any(agrees(name, w) for w in e[3])
    bits = []
    if before:
        same = [e for e in before if e[0] == before[-1][0]]        # a special held with the November race
        last = next((e for e in same if won(e)), None)
        if last is None and ch == "h" and seat == 0:
            last = next((e for e in reversed(before) if won(e)), None)   # an at-large seat several fill
        if last:
            bits.append(f"Elected {link(last, here)}.")
        else:
            e = next((e for e in same if not e[2].endswith("(special)")), same[-1])
            w = ", ".join(surname_of(x) for x in e[3])
            bits.append(f"Seat filled {link(e, here)}" + (f" ({esc(w)})" if w else "") + ".")
    nxt = after[0] if after else None
    ny = int(opened[:4]) + 1                     # the November election during the Congress
    if ch == "h" and name and (nxt is None or nxt[5]):
        # the House: his own race that November in his State, where one race names him; else the same number's
        # (a special for the seat during the Congress comes first)
        own = [e for s_, e in by_year_state().get((ny, ch, st), []) if any(agrees(name, n) for n in e[4])]
        if len(own) > 1:                         # two of the surname: the one whose given names agree
            from .lives import same_person, split_name, returns_split
            sur, given = split_name(name)
            own = [e for e in own if any((lambda sp: sp and same_person(sur, given, sur, sp[0]))(returns_split(n, sur))
                                         for n in e[4])]
        if len(own) == 1:
            nxt = own[0]
    if nxt:
        bits.append(f"Next: {link(nxt, here)}.")
    return f'<span class="cgn cgel">{" ".join(bits)}</span>' if bits else ""


def rostered():
    if "rostered" not in _cache:
        from .elections import roster
        _cache["rostered"] = {c: roster(c) for c in range(80, 100) if roster(c)}
    return _cache["rostered"]


def roster_after(date, ch, st, seat, here=False):
    """'Roster: 87th Cong.', linked to the seat's row at the first opening after the date. HTML or ''."""
    from .congress import ordinal
    for c, R in sorted(rostered().items()):
        if str(R.get("opened")) <= date:
            continue
        rows = R.get("house" if ch == "h" else "senate") or []
        if any(r["st"] == st and (r.get("d", 0) if ch == "h" else r.get("cl")) == seat for r in rows):
            href = ("#" if here else "congress.html#") + f"cg{c}-{ch}-{st}-{seat}"
            return f'Roster: <a href="{href}">{ordinal(c)} Cong.</a>'
        return ""
    return ""


def exec_after(year, here=False):
    """'Exec. 1961': the President and Vice President at the inauguration that followed, in the Executive roster."""
    from .executive import TERMS
    day = f"{int(year) + 1}-01-20"
    for i, t in enumerate(TERMS):
        if t[0] == day:
            k = f"ex{day[:4]}{day[5:7]}"
            return (f'Took office: <a href="executive.html#{k}-president-president">President</a>, '
                    f'<a href="executive.html#{k}-vp-vice-president">Vice President</a> (Exec. {day[:4]})')
    return ""
