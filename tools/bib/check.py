"""Consistency checks. Errors stop a build; warnings are things to look at.

Each problem is (level, where, rule, message), where `where` is an entry id or a
file. A warning that is deliberate can be silenced on its entry with the tag
`ok:<rule>`, e.g. `tags: [ok:thread-first]`.
"""
import re

from . import store
from .markup import refs as markup_refs, plain, ITAL_RE
from .refs import Refs

ERROR, WARN = "error", "warn"
MONTHS = {"Jan.": 1, "Feb.": 2, "Mar.": 3, "Apr.": 4, "May": 5, "June": 6, "July": 7,
          "Aug.": 8, "Sept.": 9, "Oct.": 10, "Nov.": 11, "Dec.": 12}


def when_matches_date(when, date):
    m = re.match(r"^(Jan\.|Feb\.|Mar\.|Apr\.|May|June|July|Aug\.|Sept\.|Oct\.|Nov\.|Dec\.)\s*(\d+)?", when or "")
    if not m or not re.match(r"^\d{4}-\d{2}(-\d{2})?$", date or ""):
        return False
    mo = int(date[5:7])
    if MONTHS[m.group(1)] != mo:
        return False
    return (m.group(2) is None) == (len(date) == 7) and (m.group(2) is None or int(m.group(2)) == int(date[8:10]))


def run(series, only=None):
    out = []
    tags = {e["id"]: set(e.get("tags", [])) for l in series.lists.values() for _, e in l.entries() if "id" in e}

    def add(lvl, where, msg, rule="general"):
        if lvl == WARN and f"ok:{rule}" in tags.get(where, ()):
            return
        out.append((lvl, where, rule, msg))
    refs = Refs(series)

    # ids
    seen = {}
    for lst in series.lists.values():
        for sec, e in lst.entries():
            eid = e.get("id")
            if not eid:
                add(ERROR, f"lists/{lst.key}/{sec.file}", f"entry without id: {str(e)[:80]}")
                continue
            if not eid.startswith(lst.key + "."):
                add(ERROR, eid, f"id must start with '{lst.key}.'")
            if not re.match(r"^[a-z0-9][a-z0-9.\-]*$", eid):
                add(ERROR, eid, "id may hold only a-z, 0-9, '.', '-'")
            for k in [eid] + e.get("aliases", []):
                if k in seen and seen[k] != eid:
                    add(ERROR, eid, f"id or alias {k!r} also used by {seen[k]}")
                seen[k] = eid
    idx = series.index()

    for lst in series.lists.values():
        if only and lst.key != only:
            continue
        # page text: a paragraph with an unquoted ': ' loads as a mapping, not a string
        for where, paras in [(f"lists/{lst.key}/list.yaml", [lst.data.get("lede")] + store.as_list(lst.data.get("logic")))] + \
                [(f"lists/{lst.key}/list.yaml ({s.id})", s.logic) for s in lst.walk()]:
            for p in paras:
                if p is not None and not isinstance(p, str):
                    add(ERROR, where, f"paragraph is not plain text (quote it if it holds ': '): {str(p)[:60]}")
        threads = lst.threads()
        prev_date = {}
        for sec, e in lst.entries():
            eid = e.get("id", "?")
            if e.get("conflict"):
                add(ERROR, eid, "unresolved merge conflict (./bib conflicts)")
            texts = [e.get("s"), e.get("r"), e.get("n")] + store.as_list(e.get("c"))
            for t in texts:
                for r in markup_refs(t or ""):
                    if r not in idx:
                        add(ERROR, eid, f"[[{r}]] points to no entry")
                if t and t.count("*") % 2:
                    add(WARN, eid, "odd number of '*': an italic span is not closed", "italics")
            is_thread = lst.kind == "calendar" and eid.startswith(f"{lst.key}.thread.")
            if not is_thread and not e.get("c") and not (e.get("s") and (e.get("r") or e.get("n"))):
                add(ERROR, eid, "needs a 'c' line (or, for a person, 's' with 'r' or 'n')")
            if lst.kind == "calendar" and not is_thread:
                for f in ("when", "date", "thread"):
                    if not e.get(f):
                        add(ERROR, eid, f"calendar entry needs '{f}'")
                if e.get("s"):
                    add(WARN, eid, "calendar entries take no 's'; it is built from when + thread", "cal-s")
                if e.get("thread") and e["thread"] not in threads:
                    add(ERROR, eid, f"unknown thread {e['thread']!r} (threads live in {lst.key}/{lst.data.get('threads_section')})")
                for t in e.get("also", []):
                    if t not in threads:
                        add(ERROR, eid, f"unknown thread {t!r} in 'also'")
                if e.get("when") and e.get("date") and not when_matches_date(e["when"], e["date"]):
                    add(ERROR, eid, f"when {e['when']!r} and date {e['date']!r} disagree")
                lo, hi = sec.extra.get("from"), sec.extra.get("to")
                d = e.get("date") or ""
                if lo and hi and d and not (lo[:len(d)] <= d <= hi[:len(d)]):
                    add(ERROR, eid, f"dated {d}, outside section {sec.id} ({lo} to {hi})")
                if len(d) == 10:
                    p = prev_date.get(sec.id)
                    if p and d < p:
                        add(WARN, eid, f"out of date order in {sec.file} (after {p})", "order")
                    prev_date[sec.id] = d
        if lst.kind == "calendar":
            # the first entry of a thread carries its bibliography
            first = {}
            for sec, e in lst.entries():
                if "thread" in e and e["thread"] not in first:
                    first[e["thread"]] = e
            for t, e in first.items():
                if (e.get("n") or "").startswith("See "):
                    add(WARN, e["id"], f"first entry of thread {t!r} only points elsewhere; it should carry the bibliography", "thread-first")
            for t in threads:
                if t not in first:
                    add(WARN, f"{lst.key}.thread.{t}", "thread has no entries", "thread-empty")

    # section references that point nowhere, and works cited under the wrong section
    from .build import Linker
    linker = Linker(series)
    for lst in series.lists.values():
        if only and lst.key != only:
            continue
        for sec, e in lst.entries():
            for t in [e.get("n")] + store.as_list(e.get("c")):
                if not t:
                    continue
                txt = plain(t)
                for a, b, key, code in refs.scan(txt, lst.key):
                    if code and not refs.section_for(key, code):
                        add(WARN, e["id"], f"{txt[a:b]!r}: no such section", "section-ref")
                for m in ITAL_RE.finditer(t):
                    tail = t[m.end():m.end() + 200]
                    for a, b, key, code in refs.scan(plain(tail), lst.key):
                        if re.search(r"\*|;|[a-z]\.\s", plain(tail)[:a]):
                            break
                        if not code or not refs.section_for(key, code):
                            break
                        cited = refs.section_for(key, code)
                        if linker.find_title(m.group(1), key, code) is not None:
                            break
                        # not in the cited section: is it elsewhere in the series?
                        where = []
                        for k2 in series.lists:
                            x = linker.find_title(m.group(1), k2, None)
                            if x:
                                l2, s2, _ = series.get(x["id"])
                                where.append(f"{l2.abbr} {s2.code}")
                        if where:
                            add(WARN, e["id"], f"*{m.group(1)}* cited as {plain(tail)[a:b]} but found in {', '.join(where[:3])}", "cited-section")
                        break

    # economic indicators (indicators/*.yaml)
    from . import indicators
    for where, msg in indicators.problems():
        add(ERROR, f"indicators/{where}.yaml", msg, "indicators")
    # election returns (elections/*.yaml)
    from . import elections
    for where, msg in elections.problems():
        add(ERROR, where, msg, "elections")
    # the day's executive documents (daybook/*.yaml)
    from . import daybook
    for where, msg in daybook.problems():
        add(ERROR, "daybook/", f"{where}: {msg}", "daybook")
    return out


def report(problems, limit=None):
    errs = [p for p in problems if p[0] == ERROR]
    warns = [p for p in problems if p[0] == WARN]
    lines = []
    for lvl, where, rule, msg in (errs + warns)[: limit or None]:
        lines.append(f"{lvl:5}  {where}: {msg}" + (f"  [{rule}]" if lvl == WARN else ""))
    lines.append(f"{len(errs)} errors, {len(warns)} warnings")
    return "\n".join(lines), len(errs)
