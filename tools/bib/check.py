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
                # to: the threads an address sets going (build.py, program_links), each resolving to a later entry
                for item in e.get("to") or []:
                    slug, tid = (next(iter(item.items())) if isinstance(item, dict) else (item, None))
                    if slug not in threads:
                        add(ERROR, eid, f"unknown thread {slug!r} in 'to'")
                    elif tid is not None:
                        hit = series.get(tid)
                        te = hit[2] if hit else None
                        if not te or slug not in [te.get("thread")] + te.get("also", []):
                            add(ERROR, eid, f"to: {tid} is not an entry of thread {slug!r}")
                        elif str(te.get("date", "")) <= str(e.get("date", "")):
                            add(ERROR, eid, f"to: {tid} is not after this entry")
                if e.get("to") and not e.get("short"):
                    add(ERROR, eid, "an entry with 'to' needs 'short', its name for the From line ('State of the Union')")
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
            members = {t for sec, e in lst.entries() if "thread" in e for t in [e["thread"]] + e.get("also", [])}
            for t in threads:
                if t not in members:
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
    # special elections and party switches (congress/specials.yaml, congress/switches.yaml)
    from . import specials
    for where, msg in specials.problems(series):
        add(ERROR, where, msg, "specials")
    # presidential primaries (elections/pres-primaries.yaml)
    from . import primaries
    for where, msg in primaries.problems(series):
        add(ERROR, where, msg, "primaries")
    # races settled by hand for the lives (sources/race-matches.yaml)
    from . import lives
    for where, msg in lives.problems(series):
        add(ERROR, where, msg, "lives")
    # the register of State election sources (sources/states.yaml)
    from . import sources
    for where, msg in sources.problems():
        add(ERROR, where, msg, "sources")
    # the Executive Branch (executive/*.yaml)
    from . import executive
    for where, msg in executive.problems(series):
        add(ERROR, where, msg, "executive")
    from . import votes                  # the Senate's roll calls on nominations (sources/vote-matches.yaml)
    for where, msg in votes.problems(series):
        add(ERROR, where, msg, "votes")
    from . import executive_sources
    un = executive_sources.unlinked(executive.load())
    if un:
        add(WARN, "executive/", f"{len(un)} holder sources not linked; ./bib executive sources lists them",
            "executive-sources")
    # the day's executive documents (daybook/*.yaml)
    from . import daybook
    for where, msg in daybook.problems():
        add(ERROR, "daybook/", f"{where}: {msg}", "daybook")
    # the calendar's threads in alphabetical order of their names (THREAD_SORT_AS: a name sorted under another word)
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        names = [t.get("s", "") for t in lst.threads().values()]
        keys = [THREAD_SORT_AS.get(n, n).lower() for n in names]
        if keys != sorted(keys):
            bad = next(n for n, k, w in zip(names, keys, sorted(keys)) if k != w)
            add(WARN, f"lists/{lst.key}/th.yaml", f"threads out of alphabetical order at {bad!r}", "thread-order")
    # Vietnamese names with their diacritics, but where a quotation, a title or a byline prints none
    for where, bare in plain_vietnamese(series):
        add(WARN, where, f"{bare!r} without its diacritics (sources/name-forms.yaml, VIET_PLACES)", "diacritics")
    # the hand-kept files keep the keyboard's quotation marks; the build curls them (smart.py)
    for path, n in curly_files():
        add(WARN, path, f"{n} curly quotation mark{'s' if n > 1 else ''}; write ' and \" (the build curls them)",
            "straight-quotes")
    return out


THREAD_SORT_AS = {"War on poverty": "poverty", "Bobby Baker": "Baker"}

HAND = ["lists/**/*.yaml", "executive/*.yaml", "daybook/abstracts.yaml", "elections/facts.yaml",
        "elections/pres-primaries.yaml", "elections/renominations.yaml", "elections/primaries.yaml", "elections/cq.yaml",
        "elections/readings/*.yaml", "congress/specials-state.yaml", "congress/specials-cq.yaml",
        "congress/switches.yaml", "sources/gallup-approval.yaml", "sources/states.yaml",
        "sources/executive-sources.yaml"]


# Places in Vietnam the series writes with their diacritics; the English names stay (Saigon, Hanoi, Haiphong, Cholon,
# Dalat, Vietnam, Tonkin, the Mekong, the Ho Chi Minh Trail). Persons: the keys of sources/name-forms.yaml.
VIET_PLACES = ["Ấp Bắc", "Bến Cát", "Biên Hòa", "Bình Dương", "Bình Giã", "Cẩm Nê", "Chánh Hòa", "Chấp Lễ", "Đà Nẵng",
               "Đồng Hới", "Hòn Mê", "Hòn Ngư", "Huế", "Qui Nhơn", "An Khê", "Quảng Khê", "Vạn Tường", "Vũng Tàu",
               "Xóm Bàng", "Điện Biên Phủ", "Mỹ Lai", "Bến Tre", "Nam Định", "Định Tường", "Trảng Bàng", "An Hòa",
               "Tây Ninh", "Đồng Xoài", "Bình Định", "Quảng Ngãi", "Quảng Trị", "Kon Tum", "Ban Mê Thuột"]
VIET = set("ăâđêôơưĂÂĐÊÔƠƯạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ")


def plain_vietnamese(series):
    """(id, plain form) for each Vietnamese name the series' own prose writes without its diacritics (the calendar, the
    notes and roles of every list, the subject lines of persons), outside
    a quotation, an italic title, a link, and the byline of a work whose title has none (Ky, *Twenty Years*)."""
    import os
    forms = store.load_yaml(os.path.join(store.ROOT, "sources", "name-forms.yaml")) or {}
    marked = [k for k in forms if any(c in VIET for c in k)] + VIET_PLACES
    plain = {}
    for k in marked:
        p = store.fold(k)
        plain.setdefault(p, k)
        w, pw = k.split()[-1], p.split()[-1]
        titled = [f for f in forms.get(k) or [] if "," not in f and store.fold(f).split()[-1:] == [pw]
                  and not set(store.fold(f).split()[:-1]) & set(p.split())]
        if store.fold(w) != w.lower() and titled:
            plain.setdefault(pw, w)                 # the name he went by, as a title form gives it: President Diem
    rx = re.compile(r"(?<![\w-])(" + "|".join(sorted((re.escape(" ".join(w.capitalize() for w in p.split()))
                                                       for p in plain), key=len, reverse=True)) + r")(?![\w-])")
    prot = re.compile(r"\*[^*]+\*|\"[^\"]*\"|\[[^\]]*\]\([^)]*\)|https?://\S+")
    byline = re.compile(r"(?:\s*(?:&|and)\s*[^,;*()\[\]]{2,60}?)?(?: et al\.)?, \*([^*]+)\*")
    out = []
    for lst in series.lists.values():
        for sec, e in lst.entries():
            people = refs_people(sec)
            for f in ("c", "n", "r", "s"):
                if f == "c" and lst.kind != "calendar" or f == "s" and not people:
                    continue                # a citation: its bylines and titles as printed
                for text in store.as_list(e.get(f)):
                    if not isinstance(text, str):
                        continue
                    spans = [m.span() for m in prot.finditer(text)]
                    for m in rx.finditer(text):
                        if any(a <= m.start() < b for a, b in spans):
                            continue
                        if m.group(1) == "Ky" and text[m.end():m.end() + 1] == ".":
                            continue                # Kentucky
                        b = byline.match(text, m.end())
                        if b and not any(c in VIET for c in b.group(1)):
                            continue
                        out.append((e["id"], m.group(1)))
    return out


def refs_people(sec):
    """Part III, or a section of memoirs and biographies, whose subject lines are persons."""
    from .refs import Refs
    return Refs.is_people_section(sec)


def curly_files():
    """The hand-kept files that hold a curly quotation mark (‘ ’ “ ”), with the count. Matching files (name-forms,
    frus-joins, app-matches and the like) keep the forms the sources print and are not among them."""
    import glob
    import os
    out = []
    for pat in HAND:
        for p in sorted(glob.glob(os.path.join(store.ROOT, pat), recursive=True)):
            t = open(p, encoding="utf-8").read()
            n = sum(t.count(c) for c in "\u2018\u2019\u201c\u201d")
            if n:
                out.append((os.path.relpath(p, store.ROOT), n))
    return out


def report(problems, limit=None):
    errs = [p for p in problems if p[0] == ERROR]
    warns = [p for p in problems if p[0] == WARN]
    lines = []
    for lvl, where, rule, msg in (errs + warns)[: limit or None]:
        lines.append(f"{lvl:5}  {where}: {msg}" + (f"  [{rule}]" if lvl == WARN else ""))
    lines.append(f"{len(errs)} errors, {len(warns)} warnings")
    return "\n".join(lines), len(errs)
