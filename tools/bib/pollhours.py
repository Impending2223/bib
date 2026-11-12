"""The registers of the polls' hours and of daylight time (sources/poll-hours.yaml, sources/daylight-time.yaml): checks.

Both are read by people and sessions, not yet by the build; each file's header is its schema. What the election-night
range will make of them: notes/extensions/memos/poll-hours.md. `closing(st, year, election)` and `clock(st, year, date)`
are the readers a later range-maker can call; nothing calls them yet.

STYLE
1. Every State and D.C. once in each register (sources.STATES); the poll-hours rows in the header's form: elections
   from ELECTIONS, open and close each 'HH:MM', 'HH:MM-HH:MM' (earliest-latest, in order) or null, a law, a span
   'YYYY..YYYY' within 1960-68 and in order, a span_basis, and sources, each with ref, page, an https url and a ground
   from the legend (sources.GROUNDS). An hour is the law's, local: 00:00-24:00, minutes under 60.
2. `compiled_only: true` only where every source is PPH, the projections hearing of 1967; false where any is not.
3. Daylight time: each State's years with a span as in 1, an `observed` from OBSERVED, dates 'YYYY-MM-DD..YYYY-MM-DD'
   each within its row's span and in order, and sources as in 1; the spans of one State do not overlap; surveys from
   SURVEYS with a category from CATEGORIES; zones that zoneinfo knows. federal, zones_split and tz rows carry sources
   (federal, zones_split) or the fields the header names (tz: agrees yes | no | partly).
4. A check is a fact about the file, not about the law: a Check written in a row is for a reader, never an error.
"""
import datetime
import os
import re

import yaml

from . import store
from .sources import GROUNDS, STATES

HOURS = os.path.join(store.ROOT, "sources", "poll-hours.yaml")
DST = os.path.join(store.ROOT, "sources", "daylight-time.yaml")
WH, WD = "sources/poll-hours.yaml", "sources/daylight-time.yaml"
ELECTIONS = {"general", "primary", "special", "municipal", "all"}
OBSERVED = {"none", "local", "most", "statewide", "federal", "exempt"}
SURVEYS = {"CTU-1963-S", "CTU-1963-H", "CTU-1965", "DOANE-1966"}
CATEGORIES = {"statewide", "local", "none", "reverse"}
HOUR = re.compile(r"^(\d{2}):(\d{2})$")
SPAN = re.compile(r"^(\d{4})\.\.(\d{4})$")
RANGE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.\.(\d{4}-\d{2}-\d{2})$")


def _minutes(h):
    m = HOUR.match(h)
    if not m:
        return None
    hh, mm = int(m.group(1)), int(m.group(2))
    if hh > 24 or mm > 59 or (hh == 24 and mm):
        return None
    return hh * 60 + mm


def hours(v):
    """'HH:MM' -> (m, m); 'HH:MM-HH:MM' -> (m1, m2); None -> None. Raises ValueError on a malformed value."""
    if v is None:
        return None
    parts = str(v).split("-")
    if len(parts) not in (1, 2):
        raise ValueError(v)
    ms = [_minutes(p) for p in parts]
    if None in ms or (len(ms) == 2 and ms[0] > ms[1]):
        raise ValueError(v)
    return (ms[0], ms[-1])


def span(v):
    m = SPAN.match(str(v or ""))
    if not m:
        raise ValueError(v)
    a, b = int(m.group(1)), int(m.group(2))
    if not (1960 <= a <= b <= 1968):
        raise ValueError(v)
    return a, b


def _sources(where, lab, srcs):
    out = []
    if not srcs:
        return [(where, f"{lab}: no sources")]
    for s in srcs:
        if not isinstance(s, dict):
            out.append((where, f"{lab}: a source not in the form {{ref, page, url, ground}}"))
            continue
        for k in ("ref", "page", "url"):
            if not str(s.get(k) or "").strip():
                out.append((where, f"{lab}: a source without its {k}"))
        if s.get("url") and not str(s["url"]).startswith("https://"):
            out.append((where, f"{lab}: source url {s['url']!r} not https"))
        if s.get("ground") not in GROUNDS:
            out.append((where, f"{lab}: source ground {s.get('ground')!r} not in the legend"))
    return out


def _load(path, where):
    if not os.path.exists(path):
        return None, [(where, "missing")]
    try:
        return store.load_yaml(path), []
    except yaml.YAMLError as e:
        return None, [(where, f"does not load: {e}")]


def hours_problems():
    reg, out = _load(HOURS, WH)
    if reg is None:
        return out
    seen = set()
    for e in reg or []:
        st = e.get("st")
        if st not in STATES:
            out.append((WH, f"unknown State {st!r}"))
        if st in seen:
            out.append((WH, f"{st} twice"))
        seen.add(st)
        rows = e.get("rows") or []
        if not rows:
            out.append((WH, f"{st}: no rows"))
        refs = set()
        for i, r in enumerate(rows):
            lab = f"{st}-{i + 1}"
            el = r.get("elections") or []
            if not el or not set(el) <= ELECTIONS:
                out.append((WH, f"{lab}: elections {el!r} not from {sorted(ELECTIONS)}"))
            if not str(r.get("applies") or "").strip():
                out.append((WH, f"{lab}: no applies"))
            for k in ("open", "close"):
                if k not in r:
                    out.append((WH, f"{lab}: no {k} (write null where the law fixes none)"))
                    continue
                try:
                    hours(r[k])
                except ValueError:
                    out.append((WH, f"{lab}: {k} {r[k]!r} is not 'HH:MM' or 'HH:MM-HH:MM' in order"))
            if not str(r.get("law") or "").strip():
                out.append((WH, f"{lab}: no law"))
            try:
                span(r.get("span"))
            except ValueError:
                out.append((WH, f"{lab}: span {r.get('span')!r} is not 'YYYY..YYYY' within 1960-68"))
            if not str(r.get("span_basis") or "").strip():
                out.append((WH, f"{lab}: no span_basis"))
            if r.get("effective") and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(r["effective"])):
                out.append((WH, f"{lab}: effective {r['effective']!r} not a date"))
            out += _sources(WH, lab, r.get("sources"))
            refs |= {str(s.get("ref")) for s in r.get("sources") or [] if isinstance(s, dict)}
        co = e.get("compiled_only")
        if not isinstance(co, bool):
            out.append((WH, f"{st}: compiled_only not true or false"))
        elif co != (refs <= {"PPH"}):
            out.append((WH, f"{st}: compiled_only is {co}, but its sources are {sorted(refs)}"))
    for st in sorted(STATES - seen):
        out.append((WH, f"{st} missing"))
    return out


def _zone_ok(z):
    import zoneinfo
    try:
        zoneinfo.ZoneInfo(z)
        return True
    except Exception:
        return False


def dst_problems():
    reg, out = _load(DST, WD)
    if reg is None:
        return out
    if not isinstance(reg, dict):
        return [(WD, "the top level is not a mapping (federal, zones_split, states, tz)")]
    for i, f in enumerate(reg.get("federal") or []):
        lab = f"federal-{i + 1}"
        for k in ("act", "cite", "url", "does"):
            if not str(f.get(k) or "").strip():
                out.append((WD, f"{lab}: no {k}"))
        out += _sources(WD, lab, f.get("sources"))
    for z in reg.get("zones_split") or []:
        lab = f"zones_split {z.get('st')}"
        if z.get("st") not in STATES:
            out.append((WD, f"{lab}: unknown State"))
        for zz in z.get("zones") or []:
            if not _zone_ok(zz):
                out.append((WD, f"{lab}: zone {zz!r} unknown to zoneinfo"))
        out += _sources(WD, lab, z.get("sources"))
    seen = set()
    for e in reg.get("states") or []:
        st = e.get("st")
        if st not in STATES:
            out.append((WD, f"unknown State {st!r}"))
        if st in seen:
            out.append((WD, f"{st} twice"))
        seen.add(st)
        for zz in e.get("zones") or []:
            if not _zone_ok(zz):
                out.append((WD, f"{st}: zone {zz!r} unknown to zoneinfo"))
        spans = []
        for i, y in enumerate(e.get("years") or []):
            lab = f"{st}-{i + 1}"
            try:
                a, b = span(y.get("span"))
                spans.append((a, b, lab))
            except ValueError:
                out.append((WD, f"{lab}: span {y.get('span')!r} is not 'YYYY..YYYY' within 1960-68"))
                a = b = None
            if y.get("observed") not in OBSERVED:
                out.append((WD, f"{lab}: observed {y.get('observed')!r} not from {sorted(OBSERVED)}"))
            for d in y.get("dates") or []:
                m = RANGE.match(str(d))
                if not m:
                    out.append((WD, f"{lab}: dates {d!r} not 'YYYY-MM-DD..YYYY-MM-DD'"))
                    continue
                try:
                    d1, d2 = (datetime.date.fromisoformat(x) for x in m.groups())
                except ValueError:
                    out.append((WD, f"{lab}: dates {d!r} not real days"))
                    continue
                if d1 > d2 or d1.year != d2.year:
                    out.append((WD, f"{lab}: dates {d!r} out of order or across years"))
                if a is not None and not (a <= d1.year <= b):
                    out.append((WD, f"{lab}: dates {d!r} outside the span {y.get('span')}"))
                if d1.weekday() != 6 and y.get("observed") in ("statewide", "federal") and st != "MI":
                    out.append((WD, f"{lab}: dates {d!r} does not begin on a Sunday"))
            out += _sources(WD, lab, y.get("sources"))
        spans.sort()
        for (a1, b1, l1), (a2, b2, l2) in zip(spans, spans[1:]):
            if a2 <= b1:
                out.append((WD, f"{st}: {l1} and {l2} overlap"))
        for k, v in (e.get("surveys") or {}).items():
            if k not in SURVEYS or v not in CATEGORIES:
                out.append((WD, f"{st}: survey {k}: {v!r} not from the legend"))
    for st in sorted(STATES - seen):
        out.append((WD, f"{st} missing"))
    for i, t in enumerate(reg.get("tz") or []):
        lab = f"tz-{i + 1}"
        if not _zone_ok(str(t.get("zone"))):
            out.append((WD, f"{lab}: zone {t.get('zone')!r} unknown to zoneinfo"))
        if str(t.get("agrees")) not in ("yes", "no", "partly"):
            out.append((WD, f"{lab}: agrees {t.get('agrees')!r} not yes, no or partly"))
        for k in ("places", "tz", "read"):
            if not str(t.get(k) or "").strip():
                out.append((WD, f"{lab}: no {k}"))
        try:
            span(t.get("years"))
        except ValueError:
            out.append((WD, f"{lab}: years {t.get('years')!r} not 'YYYY..YYYY' within 1960-68"))
    return out


def problems():
    return hours_problems() + dst_problems()


def closing(st, year, election="general"):
    """The latest closing hour (minutes after local midnight) the law read allows in State st for the year and the
    election, over every rule of the State: None where no row covers the year (the band's own hour then: BANDS)."""
    best = None
    for e in store.load_yaml(HOURS) or []:
        if e.get("st") != st:
            continue
        for r in e.get("rows") or []:
            a, b = span(r["span"])
            el = set(r.get("elections") or [])
            if a <= year <= b and (election in el or "all" in el):
                h = hours(r.get("close"))
                if h and (best is None or h[1] > best):
                    best = h[1]
    return best


def clock(st, date):
    """What the register reads for State st on an ISO date: the row's `observed` and whether the date falls in a range
    of its `dates` (True, False, or None where the row gives no dates)."""
    reg = store.load_yaml(DST) or {}
    d = datetime.date.fromisoformat(date)
    for e in reg.get("states") or []:
        if e.get("st") != st:
            continue
        for y in e.get("years") or []:
            a, b = span(y["span"])
            if a <= d.year <= b:
                ds = [RANGE.match(x).groups() for x in y.get("dates") or [] if RANGE.match(x)]
                inside = None
                if ds:
                    inside = any(x <= date <= z for x, z in ds)
                return y.get("observed"), inside
    return None, None
