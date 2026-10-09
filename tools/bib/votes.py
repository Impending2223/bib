"""The Senate's roll calls on nominations, matched to the Executive roster's holders and the series' persons.

    sources/senate-nomination-votes.json   every roll call on a nomination, 1953-74 (tools/executive/make_votes.py,
                                           from Voteview): rc, date, yea, nay, kind (final | the procedural question)
    sources/vote-matches.yaml              kept by hand: what the rules cannot settle (its header)

STYLE
- A holder's confirmation shows its vote after the date, the count linked to the roll call on Voteview: "confirmed
  Sept. 21, 1973 (78–7)"; a procedural vote on the same nomination before it, by its outcome: "confirmed July 12,
  1962 (recommittal refused, 30–62)"; both: "(64–19; recommittal refused, 20–63)". A rejection is a date of its
  own: "rejected June 19, 1959 (46–49)". In the roster's line and the Names entries alike.
- A holder's roll calls: those naming his surname, on his confirmation day (the vote on consent) or between his
  nomination (or recess appointment, or taking office) and his confirmation (procedural votes). A holder never
  confirmed: a vote on consent naming him while he held the office or after his nomination, which the Senate
  refused, is his rejection.
- A roll call the roster does not hold (a judge, an officer, a board the roster omits) goes to a person only by
  vote-matches.yaml's persons, with the post as the vote gave it: "Confirmed Judge of the Court of Appeals for the
  Second Circuit, Sept. 11, 1962 (54–16)." in the Names entry.
"""
import json
import os
import re
import unicodedata

from . import store

VV = "https://voteview.com/rollcall/"
_C = {}


def fold(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()


def rows():
    if "rows" not in _C:
        p = os.path.join(store.ROOT, "sources", "senate-nomination-votes.json")
        _C["rows"] = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
        _C["by_rc"] = {r["rc"]: r for r in _C["rows"]}
    return _C["rows"]


def by_rc():
    rows()
    return _C["by_rc"]


def hand():
    if "hand" not in _C:
        _C["hand"] = store.load_yaml(os.path.join(store.ROOT, "sources", "vote-matches.yaml")) or {}
    return _C["hand"]


def names_in(desc, sur):
    """Does the description name the surname? ('MC CLOSKEY' for McCloskey; 'O'CONNER' for O'Connor is not.)"""
    s = re.sub(r"[^A-Z]", "", fold(sur))
    d = re.sub(r"[^A-Z ]", "", fold(desc))
    return bool(re.search(r"(?<![A-Z])" + r"\s?".join(s) + r"(?![A-Z])", d))


def passed(r):
    """Did the question carry? Cloture needs two-thirds of those voting."""
    if r["kind"] == "cloture":
        return r["yea"] * 3 >= 2 * (r["yea"] + r["nay"])
    return r["yea"] > r["nay"]


PROC = {"recommit": ("recommitted", "recommittal refused"), "postpone": ("postponed", "postponement refused"),
        "cloture": ("cloture invoked", "cloture refused"), "table": ("tabled", "tabling refused"),
        "point of order": ("point of order sustained", "point of order overruled"),
        "reconsider": ("reconsidered", "reconsideration refused"), "consider": ("taken up", "consideration refused")}


def count(r):
    return f'<a href="{VV}{r["rc"]}">{r["yea"]}–{r["nay"]}</a>'


def proc_text(r):
    if r["rc"] in (hand().get("labels") or {}):
        return f'{hand()["labels"][r["rc"]]}, {count(r)}'
    if r["kind"] == "final":               # a vote on consent of another day, added by hand
        from .executive import fmt
        return f'{fmt(r["date"])}, {count(r)}'
    yes, no = PROC.get(r["kind"], (r["kind"], r["kind"] + " refused"))
    return f"{yes if passed(r) else no}, {count(r)}"


def suffix(final, procs):
    """' (64–19; recommittal refused, 20–63)'"""
    parts = ([count(final)] if final else []) + [proc_text(r) for r in procs]
    return f" ({'; '.join(parts)})" if parts else ""


def lo(d):
    return str(d or "")[:10].ljust(10, "0")


def entry(h, key=None):
    """The holder's line in vote-matches.yaml: holders, where its office (unit.office) is his or not given."""
    hd = (hand().get("holders") or {}).get(h["name"]) or {}
    return hd if not hd.get("office") or hd["office"] == key else {}


def for_holder(h, key=None):
    """The holder's roll calls: {'final': row, 'procs': [rows], 'rejected': row, 'again': [rows]}. key: the office
    (unit.office). Hand-kept refusals, additions and reconfirmations (vote-matches.yaml: holders) apply first."""
    sur = h["name"].split(",")[0]
    hd = entry(h, key)
    refuse = set(hd.get("refuse") or []) | set(hd.get("reconfirmed") or [])
    extra = [by_rc()[x] for x in hd.get("add") or [] if x in by_rc()]
    conf = str(h.get("confirmed") or "")
    start = lo(h.get("nominated") or h.get("recess") or h.get("from"))
    out = {"final": None, "procs": [], "rejected": None,
           "again": [by_rc()[x] for x in hd.get("reconfirmed") or [] if x in by_rc()]}
    mine = [r for r in rows() if r["rc"] not in refuse and names_in(r["desc"], sur)]
    for r in sorted({r["rc"]: r for r in mine}.values(), key=lambda r: (r["date"], r["rc"])):
        if conf:
            if r["kind"] == "final" and r["date"] == conf[:10] and passed(r):
                out["final"] = r
            elif r["kind"] != "final" and start[:10] <= r["date"] <= conf[:10] and len(conf) == 10:
                out["procs"].append(r)
        elif r["kind"] == "final" and not passed(r) and start <= r["date"] and (
                not h.get("to") or r["date"] <= str(h["to"])[:10]):
            out["rejected"] = r
    for r in extra:                        # by hand: the vote on consent that day, or a vote of another day
        if conf and r["kind"] == "final" and r["date"] == conf[:10]:
            out["final"] = r
        elif conf:
            out["procs"].append(r)
    out["procs"].sort(key=lambda r: (r["date"], r["rc"]))
    return out


def confirmed_suffix(h, key=None):
    """' (78–7)' after the confirmation date; '' where no roll call."""
    m = for_holder(h, key)
    return suffix(m["final"], m["procs"]) if h.get("confirmed") else ""


def later_pairs(h, key=None):
    """The dated votes after taking office: ('rejected', date, ' (46–49)'), ('reconfirmed', date, ' (64–19)')."""
    m = for_holder(h, key)
    out = [("reconfirmed", r["date"], suffix(r, [])) for r in m["again"]]
    if m["rejected"]:
        out.append(("rejected", m["rejected"]["date"], suffix(m["rejected"], [])))
    return sorted(out, key=lambda x: x[1])


def persons():
    """vote-matches.yaml persons: {rc: {name, as}} for roll calls on posts the roster does not hold."""
    return hand().get("persons") or {}


def person_sentences(name):
    """[(date, text, source)] for the hand-matched roll calls on this person (Names entries); the source, Voteview's
    page for the roll call."""
    out = []
    for rc, p in persons().items():
        if p.get("name") != name or rc not in by_rc():
            continue
        r = by_rc()[rc]
        procs = [by_rc()[x] for x in p.get("procs") or [] if x in by_rc()]
        from .executive import fmt
        if p.get("text"):                  # a sentence of its own: {date}, {vote}
            t = p["text"].format(date=fmt(r["date"]), vote=suffix(r, procs))
        elif passed(r):
            t = f"Confirmed {p['as']}, {fmt(r['date'])}{suffix(r, procs)}."
        else:
            t = f"Nomination as {p['as']} rejected, {fmt(r['date'])}{suffix(r, procs)}."
        out.append((r["date"], t, f'<a href="{VV}{rc}">Voteview</a>'))
    return out


def problems(series):
    """vote-matches.yaml: each roll call one the file of votes holds; each holder a name the roster holds."""
    from . import executive as X
    where = "sources/vote-matches.yaml"
    names = {h["name"] for u in X.load().values() for o in u.get("offices") or [] for h in o.get("holders") or []}
    for n, v in (hand().get("holders") or {}).items():
        if n not in names:
            yield where, f"holders: {n}: no such holder in the roster"
        for rc in [x for k in ("refuse", "add", "reconfirmed") for x in (v or {}).get(k) or []]:
            if rc not in by_rc():
                yield where, f"holders: {n}: {rc}: no such roll call"
    for rc, p in persons().items():
        if rc not in by_rc():
            yield where, f"persons: {rc}: no such roll call"
        elif not (p or {}).get("name") or not (p.get("as") or p.get("text")):
            yield where, f"persons: {rc}: name, and as or text"
    for rc in hand().get("labels") or {}:
        if rc not in by_rc():
            yield where, f"labels: {rc}: no such roll call"
