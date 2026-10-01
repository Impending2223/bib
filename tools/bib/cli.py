"""./bib — work on the series without reading all of it. See CLAUDE.md."""
import argparse
import hashlib
import os
import re
import sys

from . import store
from .markup import plain

HERE = store.ROOT


# ---------------------------------------------------------------- helpers

_lines = {}


def line_of(lst, sec, eid):
    path = os.path.join("lists", lst.key, sec.file)
    if path not in _lines:
        m = {}
        with open(os.path.join(HERE, path), encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                mm = re.match(r"^\s*- id: (\S+)", line)
                if mm:
                    m[mm.group(1).strip("'\"")] = n
        _lines[path] = m
    return f"{path}:{_lines[path].get(eid, 1)}"


def label(lst, e):
    from .build import entry_subject
    s = entry_subject(lst, e)
    return plain(s) if s else plain(store.as_list(e.get("c"))[0] if e.get("c") else "")


def snippet(lst, e, width=110):
    head = label(lst, e)
    rest = plain(store.as_list(e.get("c"))[0]) if e.get("c") and e.get("s") or "when" in e else plain(e.get("r") or e.get("n") or "")
    t = f"{head} — {rest}" if rest and rest != head else head
    return t if len(t) <= width else t[: width - 1] + "…"


_derived_cache = {}


def derived_tags(series, lst, sec, e):
    """Tags the tools compute; never stored. Searchable like stored tags."""
    if not _derived_cache:
        from .build import Linker
        _derived_cache["linker"] = Linker(series)
    linker = _derived_cache["linker"]
    from .merge import pub_year
    t = [f"list:{lst.key}", f"section:{sec.code or sec.id}"]
    text = " ".join(plain(x) for x in [e.get("s"), e.get("r"), e.get("n")] + store.as_list(e.get("c")) if x)
    if re.search(r"\bCheck\b", text):
        t.append("check")
    if lst.kind == "calendar":
        if "thread" in e:
            t += [f"thread:{e['thread']}"] + [f"thread:{x}" for x in e.get("also", [])]
            t += ["event", f"month:{e['date'][:7]}"]
        else:
            t.append("thread")
    else:
        t.append("person" if linker.refs.is_person(lst, sec, e) else "work")
        y = pub_year(e)
        if y:
            t.append(f"pub:{y // 10 * 10}s")
        others = set()
        keys = linker.refs.work_keys(e)
        for k in keys:
            others |= {l.key for l, s, x in linker.works.get(k, []) if l.key != lst.key}
        if linker.refs.is_person(lst, sec, e):
            for k, _ in linker.refs.name_keys(e["s"]):
                others |= {l.key for l, s, x in linker.people.get(k, []) if l.key != lst.key}
        t += [f"in:{k}" for k in sorted(others)]
        if re.search(r"\bCal\.", text) or linker.calendar_entry_citing(e):
            t.append("in:cal")
    if e.get("conflict"):
        t.append("conflict")
    return t


def all_tags(series, lst, sec, e):
    return list(e.get("tags", [])) + derived_tags(series, lst, sec, e)


def resolve_list(series, name):
    if not name:
        return None
    if name in series.lists:
        return series.lists[name]
    for l in series.lists.values():
        if name in (l.abbr, l.abbr.rstrip(".")) or name.lower() == l.abbr.lower().rstrip("."):
            return l
    raise SystemExit(f"no list {name!r}; lists: {', '.join(series.lists)}")


# ---------------------------------------------------------------- commands

def cmd_status(series, a):
    total = 0
    print(f"{series.data['title']}: {len(series.lists)} lists\n")
    for l in series.lists.values():
        n = sum(1 for _ in l.entries())
        total += n
        files = sum(1 for s in l.walk() if s.file)
        print(f"  {l.key:5} {l.abbr:10} {n:4} entries in {files:2} files  {l.meta['title']}, {l.meta.get('span', '')}")
    print(f"\n  {total} entries")
    conf = [(l, e) for l in series.lists.values() for s, e in l.entries() if e.get("conflict")]
    print(f"  {len(conf)} entries with unresolved conflicts" + (" (./bib conflicts)" if conf else ""))
    inbox = os.path.join(HERE, "inbox")
    pending = [f for f in sorted(os.listdir(inbox)) if f.endswith(".yaml")] if os.path.isdir(inbox) else []
    print(f"  {len(pending)} patches waiting in inbox/" + (": " + ", ".join(pending) if pending else ""))
    stale = [k for k, st in publish_state(series).items() if st != "current"]
    print(f"  pages to republish: {', '.join(stale) if stale else 'none'} (./bib publish-plan)")


def cmd_outline(series, a):
    l = resolve_list(series, a.list)
    print(f"{l.abbr} ({l.key}) — {l.data.get('page_title')}")
    for s in l.walk():
        pad = "  " * (s.level - 1)
        n = len(s.entries)
        f = f"  lists/{l.key}/{s.file}  ({n})" if s.file else ""
        print(f"{pad}{s.code or s.id:8} {s.title}{f}")
    if l.kind == "calendar":
        from .build import thread_members
        mem = thread_members(l)
        print("\nthreads (slug: entries):")
        for slug, e in l.threads().items():
            print(f"  {slug}: {len(mem.get(slug, []))}  — {plain(e['s'])}")


def cmd_find(series, a):
    terms = [store.fold(t) for t in a.terms]
    lists = [resolve_list(series, a.list)] if a.list else list(series.lists.values())
    n = 0
    for l in lists:
        for s, e in l.entries():
            if a.section and a.section not in (s.code, s.id, (s.file or "").rsplit(".", 1)[0]):
                continue
            if a.thread and not (e.get("thread") == a.thread or a.thread in e.get("also", [])):
                continue
            d = e.get("date", "")
            if a.since and (not d or d < a.since):
                continue
            if a.until and (not d or d[:len(a.until)] > a.until):
                continue
            if a.tag:
                tags = all_tags(series, l, s, e)
                if not all(any(t == x or t.endswith(":") and x.startswith(t) for x in tags) for t in a.tag):
                    continue
            if terms:
                hay = store.fold(" ".join([e["id"]] + [plain(x) for x in [e.get("s"), e.get("r"), e.get("n"), e.get("when")] + store.as_list(e.get("c")) if x]))
                if not all(t in hay for t in terms):
                    continue
            n += 1
            if n > a.limit:
                continue
            if a.ids:
                print(e["id"])
            else:
                print(f"{e['id']}\n    {line_of(l, s, e['id'])}  {snippet(l, e)}")
    if n > a.limit:
        print(f"... {n - a.limit} more (use --limit)")
    if not a.ids:
        print(f"{n} entries")


def cmd_show(series, a):
    from .merge import backlinks
    for eid in a.ids:
        hit = series.get(eid)
        if not hit:
            print(f"# {eid}: no such entry")
            continue
        l, s, e = hit
        print(f"# {line_of(l, s, e['id'])}   {l.abbr} {s.code or s.id} {s.title}")
        print(f"# rev: {store.rev(e)}   (quote this as `base:` when you write an edit patch)")
        print(f"# derived tags: {' '.join(derived_tags(series, l, s, e))}")
        bl = backlinks(series, e["id"])
        if bl:
            print(f"# linked from: {' '.join(bl)}")
        print(store._emit([e], 0))
        print()


def cmd_check(series, a):
    from . import check
    probs = check.run(series, only=a.list)
    if a.quiet:
        probs = [p for p in probs if p[0] == check.ERROR]
    txt, nerr = check.report(probs, a.limit)
    print(txt)
    return 1 if nerr else 0


def cmd_build(series, a):
    from . import build, check
    if not a.force:
        errs = [p for p in check.run(series) if p[0] == check.ERROR]
        if errs:
            print(check.report(errs, 20)[0])
            print("build refused: fix the errors (or --force)")
            return 1
    for p in build.run(series, a.which):
        print(os.path.relpath(p, HERE), f"{os.path.getsize(p) // 1024} KB")


def cmd_merge(series, a):
    from .merge import apply_patch, Report
    rc = 0
    for path in a.patches:
        patch = store.load_yaml(path) or {}
        name = patch.get("patch") or os.path.basename(path)
        rep = Report()
        apply_patch(series, patch, name, rep, dry=a.dry_run)
        print(f"== {name}" + (" (dry run)" if a.dry_run else ""))
        print("\n".join("  " + l for l in rep.lines))
        if rep.conflicts:
            print(f"  {rep.conflicts} conflicts recorded in the entries: ./bib conflicts")
        if not a.dry_run and a.archive:
            done = os.path.join(HERE, "inbox", "merged")
            os.makedirs(done, exist_ok=True)
            os.replace(path, os.path.join(done, os.path.basename(path)))
    return rc


def cmd_conflicts(series, a):
    n = 0
    for l in series.lists.values():
        for s, e in l.entries():
            for c in e.get("conflict", []):
                n += 1
                print(f"{e['id']}   {line_of(l, s, e['id'])}")
                if "field" in c:
                    print(f"  field {c['field']!r} from {c.get('from')}")
                    for side in ("ours", "theirs", "base"):
                        v = c.get(side)
                        v = plain(" | ".join(store.as_list(v))) if v is not None else "(none)"
                        print(f"    {side:6} {v[:300]}")
                else:
                    print(f"  {c.get('kind')} from {c.get('from')}" + (f": of {', '.join(store.as_list(c.get('of')))}" if c.get("of") else ""))
    print(f"{n} conflicts")
    if n:
        print("Resolve: ./bib resolve ID --take ours|theirs|both|base [--field F]; "
              "a duplicate: ./bib combine KEEP DROP, or ./bib resolve ID --take keep; or edit the YAML and delete `conflict:`.")


def cmd_resolve(series, a):
    from .merge import resolve
    print(a.id, resolve(series, a.id, a.take, a.field))


def cmd_combine(series, a):
    from .merge import combine, Report
    rep = Report()
    touched = set()
    combine(series, a.keep, a.drop, "combine", rep, touched)
    for s in touched:
        series.save_section(s)
    print("\n".join(rep.lines))


def cmd_tag(series, a):
    from .merge import op_tag, Report
    rep = Report()
    touched = set()
    adds = [t[1:] for t in a.changes if t.startswith("+")]
    rems = [t[1:] for t in a.changes if t.startswith("-")]
    bad = [t for t in a.changes if t[:1] not in "+-"]
    if bad:
        raise SystemExit("write tags as +name or -name")
    for eid in a.ids:
        op_tag(series, {"id": eid, "add": adds, "remove": rems}, "tag", rep, touched)
        series.invalidate()
    for s in touched:
        series.save_section(s)
    print("\n".join(rep.lines))


def cmd_tags(series, a):
    from collections import Counter
    stored, derived = Counter(), Counter()
    for l in series.lists.values():
        if a.list and l.key != a.list:
            continue
        for s, e in l.entries():
            stored.update(e.get("tags", []))
            if a.derived:
                derived.update(t for t in derived_tags(series, l, s, e) if not t.startswith(("section:", "list:")))
    print("stored tags:" if stored else "stored tags: none yet")
    for t, n in sorted(stored.items()):
        print(f"  {t}  {n}")
    if a.derived:
        print("derived tags:")
        for t, n in sorted(derived.items()):
            print(f"  {t}  {n}")


def cmd_works(series, a):
    """Where a title or a person appears across the series."""
    from .build import Linker
    linker = Linker(series)
    q = store.fold(" ".join(a.query))
    hits = []
    for l in series.lists.values():
        for s, e in l.entries():
            titles = linker.refs.full_titles(e)
            names = [k for k, _ in linker.refs.name_keys(e["s"])] if linker.refs.is_person(l, s, e) else []
            notes = store.fold(plain(e.get("n") or ""))
            how = None
            if any(q in t for t in titles) or any(q in n for n in names):
                how = "entry"
            elif q in notes or any(q in store.fold(plain(c)) for c in store.as_list(e.get("c"))):
                how = "cited"
            if how:
                hits.append((how, l, s, e))
    for how, l, s, e in sorted(hits, key=lambda h: h[0] != "entry"):
        print(f"{how:6} {l.abbr:9} {s.code or s.id:8} {e['id']}\n       {snippet(l, e, 100)}")
    print(f"{len(hits)} places")


def cmd_new_id(series, a):
    l = resolve_list(series, a.list)
    base = f"{l.key}." + ".".join(store.slug(x, 6) for x in a.words)
    eid, n = base, 2
    while series.get(eid):
        eid, n = f"{base}-{n}", n + 1
    print(eid)


def published_path():
    return os.path.join(HERE, "published.yaml")


def publish_state(series):
    from . import build
    rec = store.load_yaml(published_path()) if os.path.exists(published_path()) else {}
    rec = rec or {}
    out = {}
    for key in list(series.lists) + ["series"]:
        p = os.path.join(build.OUT, f"{key}.html")
        if not os.path.exists(p):
            out[key] = "not built"
            continue
        h = hashlib.sha1(open(p, "rb").read()).hexdigest()[:12]
        out[key] = "current" if (rec.get(key) or {}).get("hash") == h else "changed"
    return out


def cmd_publish_plan(series, a):
    st = publish_state(series)
    rec = (store.load_yaml(published_path()) if os.path.exists(published_path()) else {}) or {}
    for key, state in st.items():
        url = series.data["compiled_artifact"] if key == "series" else series.lists[key].meta.get("artifact")
        last = (rec.get(key) or {}).get("date", "never")
        print(f"{key:6} {state:9} build/{key}.html -> {url}   (last recorded publish: {last})")
    print("\nAfter publishing a page with the Artifact tool, record it: ./bib mark-published KEY")


def cmd_mark_published(series, a):
    import datetime
    from . import build
    rec = (store.load_yaml(published_path()) if os.path.exists(published_path()) else {}) or {}
    for key in a.keys:
        p = os.path.join(build.OUT, f"{key}.html")
        h = hashlib.sha1(open(p, "rb").read()).hexdigest()[:12]
        rec[key] = {"hash": h, "date": datetime.date.today().isoformat()}
        print(f"{key}: recorded {h}")
    store.dump_yaml(rec, published_path(), header=["Hash of each build/ page as last published. Written by ./bib mark-published."])


def cmd_setup(series, a):
    import subprocess
    cmd = "python3 tools/bibcli.py git-merge %O %A %B %P"
    subprocess.run(["git", "config", "merge.bib.name", "bib entry-level merge"], cwd=HERE, check=True)
    subprocess.run(["git", "config", "merge.bib.driver", cmd], cwd=HERE, check=True)
    print("registered the entry-level merge driver for lists/*/*.yaml (see .gitattributes)")


def cmd_git_merge(a):
    from .merge import git_merge_driver
    return git_merge_driver(a.base, a.ours, a.theirs, a.name or "")


def cmd_import(a):
    from . import importer
    importer.run(a.path, force=a.force)
    print("imported; run ./bib check and ./bib build")


# ---------------------------------------------------------------- entry point

def main(argv=None):
    p = argparse.ArgumentParser(prog="bib", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="lists, counts, conflicts, inbox, stale pages")
    x = sub.add_parser("outline", help="a list's sections and the files that hold them")
    x.add_argument("list")
    x = sub.add_parser("find", help="search entries; prints id, file:line, and a one-line summary")
    x.add_argument("terms", nargs="*", help="words that must all appear (accents and case ignored)")
    x.add_argument("--list", "-l")
    x.add_argument("--section", "-s", help="section code or id, e.g. II.D or apr")
    x.add_argument("--tag", "-t", action="append", help="stored or derived tag; 'thread:' matches any thread. Repeatable")
    x.add_argument("--thread")
    x.add_argument("--since", help="calendar date, e.g. 1961-04")
    x.add_argument("--until")
    x.add_argument("--limit", type=int, default=60)
    x.add_argument("--ids", action="store_true", help="print ids only")
    x = sub.add_parser("show", help="full YAML of entries, with rev, tags, and backlinks")
    x.add_argument("ids", nargs="+")
    x = sub.add_parser("check", help="lint the store; exit 1 on errors")
    x.add_argument("--list", "-l")
    x.add_argument("--quiet", "-q", action="store_true", help="errors only")
    x.add_argument("--limit", type=int)
    x = sub.add_parser("build", help="write build/<key>.html and build/series.html")
    x.add_argument("which", nargs="?", help="a list key, or 'series'; default all")
    x.add_argument("--force", action="store_true")
    x = sub.add_parser("merge", help="apply patch files (see CLAUDE.md for the format)")
    x.add_argument("patches", nargs="+")
    x.add_argument("--dry-run", "-n", action="store_true")
    x.add_argument("--archive", action="store_true", help="move applied patches to inbox/merged/")
    sub.add_parser("conflicts", help="list unresolved conflicts")
    x = sub.add_parser("resolve", help="settle an entry's conflicts")
    x.add_argument("id")
    x.add_argument("--take", required=True, choices=["ours", "theirs", "both", "base", "keep"])
    x.add_argument("--field")
    x = sub.add_parser("combine", help="fold duplicate DROP into KEEP (DROP's id becomes an alias)")
    x.add_argument("keep")
    x.add_argument("drop")
    x = sub.add_parser("tag", help="add or remove stored tags: ./bib tag ID... +topic:space -todo")
    x.add_argument("ids", nargs="+", help="entry ids, then +tag/-tag")
    x = sub.add_parser("tags", help="the tag vocabulary in use")
    x.add_argument("--list", "-l")
    x.add_argument("--derived", action="store_true")
    x = sub.add_parser("works", help="where a title or person appears across the series")
    x.add_argument("query", nargs="+")
    x = sub.add_parser("new-id", help="suggest an unused id: ./bib new-id cal 1961-10-27 berlin-and-vienna")
    x.add_argument("list")
    x.add_argument("words", nargs="+")
    sub.add_parser("publish-plan", help="which built pages differ from what was last published, and where they go")
    x = sub.add_parser("mark-published", help="record that build/KEY.html was published")
    x.add_argument("keys", nargs="+")
    sub.add_parser("setup", help="register the git merge driver in this clone")
    x = sub.add_parser("git-merge", help=argparse.SUPPRESS)
    x.add_argument("base"); x.add_argument("ours"); x.add_argument("theirs"); x.add_argument("name", nargs="?")
    x = sub.add_parser("import", help="(re)build the store from a compiled HTML page")
    x.add_argument("path")
    x.add_argument("--force", action="store_true")

    a = p.parse_args(argv)
    if a.cmd == "git-merge":
        return cmd_git_merge(a)
    if a.cmd == "import":
        return cmd_import(a)
    if a.cmd == "tag":
        a.changes = [t for t in a.ids if t[:1] in "+-"]
        a.ids = [t for t in a.ids if t[:1] not in "+-"]
    series = store.Series()
    fn = globals()["cmd_" + a.cmd.replace("-", "_")]
    return fn(series, a) or 0


if __name__ == "__main__":
    sys.exit(main())
