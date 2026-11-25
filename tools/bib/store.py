"""Loading and saving the series: series.yaml, lists/<key>/list.yaml, lists/<key>/<file>.yaml.

Everything on disk is plain YAML so it can be grepped and hand-edited. This
module is the only place that knows the layout; the rest of the tools work on
the in-memory objects it returns.
"""
import datetime
import functools
import hashlib
import json
import os
import re
import unicodedata

import yaml

# The repository: the data and build/ under it. BIB_ROOT, when set, names another tree of the same layout
# (the tests' fixture, tests/fixture); every module takes its paths from here.
ROOT = os.path.abspath(os.environ.get("BIB_ROOT") or
                       os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LISTS = os.path.join(ROOT, "lists")

# Field order inside an entry. Anything else is kept, after these.
ENTRY_FIELDS = ["id", "when", "date", "at", "time", "time_approx", "place", "thread", "also", "follows", "part_of", "s", "work", "card_note", "byline", "ditto", "c", "cuts", "cut_from", "c2", "c3", "r", "n", "src", "gloss", "tags",
                "aliases", "conflict"]


# ---------------------------------------------------------------- yaml i/o

# libyaml's loader (C, about eight times faster) when this PyYAML has it, else the pure-Python one; both read every
# file of the data alike (tests/property: test_c_loader_agrees). _PyLoader, the pure-Python one, reads a file libyaml
# will not, so that the message for bad YAML is the same whichever loader is in use.
_FAST = bool(getattr(yaml, "__with_libyaml__", False)) and hasattr(yaml, "CSafeLoader")
LOADER_KIND = "libyaml" if _FAST else "python"


class _PyLoader(yaml.SafeLoader):
    pass


class _Loader(yaml.CSafeLoader if _FAST else yaml.SafeLoader):
    pass


# Dates and times stay strings: "1961-04-15" must not turn into a date object.
_PyLoader.yaml_implicit_resolvers = _Loader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


class DataError(Exception):
    """A data file that cannot be read (bad YAML, git conflict markers). An ordinary error: a handler meant for a
    file that does not load (patchcheck, patchaudit) catches it; cli.main turns it into its message and exit 1."""


_PARSED = {}                             # path -> (sha1 of the file's bytes, pickled data): each file parsed once a run
CACHE_DIR = os.path.join(ROOT, ".cache", "yaml")   # and kept between runs, by path and the bytes' sha1 (git-ignored)


def load_yaml(path):
    """A YAML file's data, parsed once: the parse is kept in memory for the run and on disk (.cache/yaml) for later
    runs, keyed by the file's path and a sha1 of its bytes (on disk, with the loader's kind; not its modification time
    and size, which a rewrite in the same tick can leave unchanged; hashing all the data's YAML costs about 0.1-0.2 s a run). Each caller gets its
    own copy (callers change what they load). _PARSED[path] holds the digest and parse of the bytes last read."""
    import pickle
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError:
        raw = None
    if raw is not None:
        sig = hashlib.sha1(raw).hexdigest()
        dkey = sig + "/" + LOADER_KIND     # on disk, the loader's kind too: a change of loader parses afresh
        hit = _PARSED.get(path)
        if hit and hit[0] == sig:
            return pickle.loads(hit[1])
        disk = os.path.join(CACHE_DIR, hashlib.sha1(os.path.abspath(path).encode()).hexdigest() + ".pickle")
        try:
            with open(disk, "rb") as f:
                dsig, blob = pickle.load(f)
            if dsig == dkey:
                _PARSED[path] = (sig, blob)
                return pickle.loads(blob)
        except (OSError, EOFError, pickle.UnpicklingError, ValueError, TypeError):
            pass
    data = _parse_yaml(path, None if raw is None else raw.decode("utf-8"))
    if raw is not None:
        blob = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
        _PARSED[path] = (sig, blob)
        try:
            os.makedirs(CACHE_DIR, exist_ok=True)
            tmp = disk + f".{os.getpid()}.tmp"
            with open(tmp, "wb") as f:
                pickle.dump((dkey, blob), f, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp, disk)
        except OSError:
            pass
    return data


def _parse_yaml(path, text=None):
    if text is None:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    if "\n<<<<<<< " in "\n" + text:
        raise DataError(f"{os.path.relpath(path, ROOT)}: git conflict markers. Run ./bib setup once so git "
                        "merges these files entry by entry, or settle the markers by hand.")
    try:
        return yaml.load(text, Loader=_Loader)
    except yaml.YAMLError:
        pass
    try:                                 # it failed: the pure-Python loader's reading and message, as before
        return yaml.load(text, Loader=_PyLoader)
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        where = f"{os.path.relpath(path, ROOT)}:{mark.line + 1}" if mark else os.path.relpath(path, ROOT)
        raise DataError(f"{where}: not valid YAML ({getattr(e, 'problem', e)}).\n"
                        "Quote a value in single quotes when it holds ': ' or ' #', or starts with * [ { ' \" & ! | > % @ `.\n"
                        "Inside single quotes, write an apostrophe as ''.")


def _scalar(v):
    """One YAML scalar on one line, quoted only when YAML needs it."""
    if isinstance(v, (datetime.date, datetime.datetime)):
        v = v.isoformat()
    out = yaml.safe_dump(v, allow_unicode=True, width=10**9, default_flow_style=True, sort_keys=False)
    out = out.rstrip("\n")
    if out.endswith("\n..."):
        out = out[:-4].rstrip("\n")
    return out


@functools.lru_cache(maxsize=4096, typed=True)    # typed: the key True is not the key 1
def _key(k):
    """A mapping key, quoted as a value would be: 'on', 'no', '1961', '#x', 'k: v' read back as written."""
    return _scalar(k)


def _emit(v, indent):
    """Block YAML with one field per line; lists of strings become '- ' items."""
    pad = " " * indent
    if isinstance(v, dict):
        lines = []
        for k, x in v.items():
            k = _key(k)
            if isinstance(x, (dict, list)) and x:
                if isinstance(x, list) and all(not isinstance(i, (dict, list)) for i in x) and k in ("also", "tags", "aliases"):
                    lines.append(f"{pad}{k}: [{', '.join(_scalar(i) for i in x)}]")
                else:
                    lines.append(f"{pad}{k}:")
                    lines.append(_emit(x, indent + 2))
            else:
                lines.append(f"{pad}{k}: {_scalar(x)}")
        return "\n".join(lines)
    if isinstance(v, list):
        lines = []
        for x in v:
            if isinstance(x, (dict, list)) and not x:       # an empty mapping or list, in flow form: {} or []
                lines.append(f"{pad}- {_scalar(x)}")
            elif isinstance(x, dict):
                inner = _emit(x, indent + 2)
                lines.append(pad + "- " + inner[indent + 2:])
            elif isinstance(x, list):
                lines.append(pad + "-")
                lines.append(_emit(x, indent + 2))
            else:
                lines.append(f"{pad}- {_scalar(x)}")
        return "\n".join(lines)
    return pad + _scalar(v)


def dump_yaml(obj, path, header=None):
    """obj written to path as YAML, atomically: through a temporary file of this process's own in the same directory
    (two writers never share one), then os.replace. The in-memory parse (load_yaml) becomes obj, keyed by the digest
    of what was written. Returns the text."""
    import pickle
    text = _emit(obj, 0) + "\n"
    if header:
        text = "".join("# " + h + "\n" for h in header) + text
    atomic_write(path, text)
    if _plain(obj):                     # what was written loads back as obj (the emitter's round trip)
        _PARSED[path] = (hashlib.sha1(text.encode("utf-8")).hexdigest(), pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL))
    else:                               # a date, a tuple: the next load parses the file
        _PARSED.pop(path, None)
    return text


def _plain(v):
    """Made only of what YAML gives back as itself: str, int, float, bool, None, lists and mappings of those."""
    if isinstance(v, dict):
        return all(_plain(k) and _plain(x) for k, x in v.items())
    if isinstance(v, list):
        return all(_plain(x) for x in v)
    return v is None or isinstance(v, (str, int, float))


def atomic_write(path, text):
    """text written to path whole or not at all: a temporary file named for this process (and thread) beside it,
    then os.replace; the temporary file removed if the write fails."""
    import threading
    tmp = f"{path}.{os.getpid()}.{threading.get_ident()}.tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def file_digest(path):
    """sha1 of a file's bytes, or None where there is no file."""
    try:
        with open(path, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()
    except OSError:
        return None


# ---------------------------------------------------------------- ids and keys

def memo(fn):
    """fn, a pure function of its arguments, computed once for each (code review C, PERF 8: fold, slug, a note's
    sentences are asked for millions of times on some tens of thousands of strings). An argument that cannot be a key
    (a list) is computed afresh, as before. fn must return what no caller can change (a str, a tuple), or its caller
    must copy it."""
    cached = functools.lru_cache(maxsize=None)(fn)

    @functools.wraps(fn)
    def call(*a, **k):
        try:
            return cached(*a, **k)
        except TypeError:
            return fn(*a, **k)
    call.cache_clear = cached.cache_clear
    return call


@memo
def slug(text, maxwords=6):
    t = unicodedata.normalize("NFKD", text.replace("Đ", "D").replace("đ", "d"))   # Đ has no decomposition
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    t = t.lower().replace("&", " and ").replace("'", "").replace("’", "")
    words = re.findall(r"[a-z0-9]+", t)
    return "-".join(words[:maxwords])


@memo
def fold(text):
    """Comparison form of a title or name: no accents, case, or punctuation."""
    return " ".join(slug(text, 999).split("-"))


def stored_form(entry):
    """The entry as its file holds it. A listing that points to works (`work:`) is given its citation and the cards'
    notes in memory when the series loads (works.resolve); here they come off again. A field changed since then is
    the writer's: a new note is the listing's note; a new citation cuts the pointer (the entry cites as written)."""
    d = entry.get("_derived")
    out = {k: v for k, v in entry.items() if not k.startswith("_")}
    ks = out.get("cuts")                   # a calendar line's cuts go back into it (tools/bib/cuts.py, STYLE 5)
    if isinstance(ks, list) and all(isinstance(x, (list, tuple)) and len(x) == 2 for x in ks):
        from . import cuts as _cuts
        del out["cuts"]
        if ks:
            bad = _cuts.problems(out.get("c") or "", ks)
            if bad:
                raise ValueError(f"{out.get('id')}: the line's cuts do not fit it ({'; '.join(bad)}); set the line "
                                 "and its cuts together (cuts.set_line)")
            out["c"] = _cuts.insert(out["c"], ks)
    if not d:
        return out
    for k, (shown, stored) in d.items():
        if out.get(k) != shown:
            if k == "c":
                out.pop("work", None)
            continue
        if stored is None:
            out.pop(k, None)
        else:
            out[k] = stored
    return out


def canonical(entry):
    """The entry without bookkeeping fields, as a stable string."""
    core = {k: v for k, v in stored_form(entry).items() if k not in ("conflict",)}
    return json.dumps(core, ensure_ascii=False, sort_keys=True)


def rev(entry):
    """Short content hash. Patches quote it to say which version they edited."""
    return hashlib.sha1(canonical(entry).encode("utf-8")).hexdigest()[:8]


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def normalize_entry(e):
    """Coerce hand-edited values into the canonical shape and order."""
    if "date" in e and isinstance(e["date"], (datetime.date, datetime.datetime)):
        e["date"] = e["date"].isoformat()
    if "date" in e and isinstance(e["date"], int) and not isinstance(e["date"], bool):
        e["date"] = str(e["date"])          # a year alone written bare (date: 1962) is the year as text
    for k in ("also", "tags", "aliases"):
        if k in e:
            e[k] = [str(x) for x in as_list(e[k])]
            if not e[k]:
                del e[k]
    for k in ("c", "work"):
        if isinstance(e.get(k), list) and len(e[k]) == 1:
            e[k] = e[k][0]
    if isinstance(e.get("c"), str) and "{" in e["c"] and str(e.get("id") or "").startswith("cal."):
        from . import cuts as _cuts        # a calendar line's cut marks, out of the line (tools/bib/cuts.py, STYLE 5)
        plain, ks = _cuts.strip(e["c"])
        if ks:
            e["c"], e["cuts"] = plain, ks
    ordered = {k: e[k] for k in ENTRY_FIELDS if k in e}
    ordered.update({k: v for k, v in e.items() if k not in ordered})
    return ordered


# ---------------------------------------------------------------- the model

class Section:
    def __init__(self, data, lst, parent=None, level=2):
        self.lst = lst
        self.parent = parent
        self.level = level
        self.id = str(data["id"])   # a YYYYMM id unquoted loads as a number
        self.num = data.get("num")
        self.title = data["title"]
        self.short = data.get("short")
        self.logic = as_list(data.get("logic"))
        self.file = data.get("file")
        self.extra = {k: v for k, v in data.items()
                      if k not in ("id", "num", "title", "short", "logic", "file", "sections")}
        self.children = [Section(c, lst, self, level + 1) for c in data.get("sections", [])]
        self.entries = []

    @property
    def code(self):
        """The section code used in cross-references: 'II.D', 'III', 'II.G.1'."""
        return (self.num or "").rstrip(".") or None

    @property
    def label(self):
        if self.short:
            return self.short
        return f"{self.num} {self.title}" if self.num else self.title

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()

    def to_data(self):
        d = {"id": self.id}
        if self.num:
            d["num"] = self.num
        d["title"] = self.title
        if self.short:
            d["short"] = self.short
        if self.logic:
            d["logic"] = self.logic
        d.update(self.extra)
        if self.file:
            d["file"] = self.file
        if self.children:
            d["sections"] = [c.to_data() for c in self.children]
        return d


class List:
    def __init__(self, key, data, meta):
        self.key = key
        self.meta = meta  # the series.yaml record
        self.data = data
        self.kind = data.get("kind", "bibliography")
        self.sections = [Section(s, self) for s in data.get("sections", [])]

    @property
    def abbr(self):
        return self.meta["abbr"]

    @property
    def dir(self):
        return os.path.join(LISTS, self.key)

    def walk(self):
        for s in self.sections:
            yield from s.walk()

    def section(self, ref):
        """Find a section by id, code ('II.D'), or file name."""
        for s in self.walk():
            if ref in (s.id, s.code, s.file, (s.file or "").rsplit(".", 1)[0]):
                return s
        return None

    def entries(self):
        for s in self.walk():
            for e in s.entries:
                yield s, e

    def threads(self):
        """Calendar lists: thread slug -> the thread's own entry. Kept while the threads section's entries are the
        same list of the same length (a merge or an edit that adds or drops a thread rebuilds it)."""
        th = self.section(self.data.get("threads_section", "")) if self.kind == "calendar" else None
        if not th:
            return {}
        key = (id(th.entries), len(th.entries))
        if getattr(self, "_threads_key", None) != key:
            self._threads = {e["id"].split(".", 2)[2]: e for e in th.entries}
            self._threads_key = key
        return self._threads

    def thread_parent(self, slug):
        """A subthread's parent slug (`parent:` on its th.yaml entry), else None."""
        e = self.threads().get(slug)
        return e.get("parent") if e else None

    def thread_line(self, slug):
        """The slug and its ancestors, nearest first: a subthread's entries belong to its parent's thread too."""
        out = []
        while slug and slug not in out:
            out.append(slug)
            slug = self.thread_parent(slug)
        return out

    def is_ghost(self, slug):
        """A ghost: a subthread without a statement of its own; named in rubrics and Continuing lines, not in the index."""
        e = self.threads().get(slug)
        return bool(e and e.get("parent") and not e.get("c"))


class Series:
    def __init__(self, root=ROOT):
        self.root = root
        self.data = load_yaml(os.path.join(root, "series.yaml"))
        self.lists = {}
        for meta in self.data["lists"]:
            key = meta["key"]
            path = os.path.join(root, "lists", key, "list.yaml")
            if not os.path.exists(path):
                continue
            lst = List(key, load_yaml(path), meta)
            for s in lst.walk():
                if s.file:
                    fp = os.path.join(root, "lists", key, s.file)
                    doc = load_yaml(fp) or {}
                    s.entries = [normalize_entry(e) for e in (doc.get("entries") or [])]
                    # the file as loaded (its digest, its parse): save_section merges a change made on disk meanwhile
                    s._disk = _PARSED.get(fp)
            self.lists[key] = lst
        self._index = None
        from . import works            # each listing that points to a card: its citation and notes, in memory
        self.works = works.Catalogue(root)
        works.resolve(self)
        from . import markup           # [[w.…]] in any text: the card's short form, linked to the A–Z bibliography
        markup.WORKS = lambda cid, cat=self.works: works.short_form(cat.alias.get(cid, cid), cat) if cat.get(cid) else None
        markup.WORKS_FULL = lambda cid, cat=self.works: works.render(cat.get(cid), cat=cat)
        markup.WORKS_ID = lambda cid, cat=self.works: cat.alias.get(cid, cid)

    # lookups
    def index(self):
        """id (and alias) -> (list, section, entry)."""
        if self._index is None:
            idx = {}
            keys = {}                    # section -> the keys it gave (reindex)
            clash = False                # a key two entries claim: an id or alias used twice
            for lst in self.lists.values():
                for s, e in lst.entries():
                    clash = clash or e["id"] in idx
                    idx[e["id"]] = (lst, s, e)
                    keys.setdefault(s, []).append(e["id"])
            for lst in self.lists.values():
                for s, e in lst.entries():
                    for a in e.get("aliases", []):
                        if a in idx:
                            clash = True
                        else:
                            idx[a] = (lst, s, e)
                            keys.setdefault(s, []).append(a)
            self._index = idx
            self._index_keys = None if clash else keys
        return self._index

    def reindex(self, sections):
        """The index brought up to date after a change confined to these sections (merge.apply_patch: each op names
        the sections it changed): their keys taken out and read again from them alone, as a whole rebuild would give
        them (code review C, PERF 5). Where it might not (the index held a key two entries claim, or one would now),
        the index is dropped and rebuilt on its next use, as invalidate does."""
        idx, keys = self._index, getattr(self, "_index_keys", None)
        if idx is None:
            return
        if keys is None:
            self._index = None
            return
        for s in sections:
            for k in keys.pop(s, ()):
                del idx[k]
        new = []
        for s in sections:
            got = keys.setdefault(s, [])
            for e in s.entries:
                if e["id"] in idx:
                    self._index = None
                    return
                idx[e["id"]] = (s.lst, s, e)
                got.append(e["id"])
                new.append((s, e))
        for s, e in new:
            for a in e.get("aliases", []):
                if a in idx:
                    self._index = None
                    return
                idx[a] = (s.lst, s, e)
                keys[s].append(a)

    def get(self, eid):
        return self.index().get(eid)

    def by_abbr(self):
        return {l.abbr: l for l in self.lists.values()}

    def invalidate(self):
        self._index = None

    # writing
    def save_section(self, sec):
        """The section written back. If its file changed on disk since this run loaded it (another merge, an agent's
        edit), the change is not overwritten: the file is merged entry by entry (merge.merge_entry_lists; base the file
        as loaded, ours the section in memory, theirs the file now), disagreements recorded as conflicts in the
        entries, and the merged entries become the section's. A file that changed and does not load now is refused."""
        lst = sec.lst
        path = os.path.join(self.root, "lists", lst.key, sec.file)
        head = [f"{lst.abbr} {sec.code or ''} {sec.title}".replace("  ", " ").strip(),
                "Entries in display order. See CLAUDE.md for the fields. Run ./bib check after editing."]
        entries = [normalize_entry(stored_form(e)) for e in sec.entries]
        loaded = getattr(sec, "_disk", None)
        if loaded is not None:
            now = file_digest(path)
            if now is not None and now != loaded[0]:
                entries = self._merge_disk(sec, path, loaded, entries)
        doc = {"list": lst.key, "section": sec.code or sec.id, "entries": entries}
        text = dump_yaml(doc, path, header=head)
        import pickle
        sec._disk = (hashlib.sha1(text.encode("utf-8")).hexdigest(), pickle.dumps(doc, protocol=pickle.HIGHEST_PROTOCOL))

    def _merge_disk(self, sec, path, loaded, ours):
        import pickle
        import sys
        from .merge import merge_entry_lists
        rel = os.path.relpath(path, self.root)
        try:
            theirs_doc = _parse_yaml(path) or {}
        except DataError as x:
            raise DataError(f"{rel} changed on disk during this run and does not load now; not overwritten "
                            f"(this run's changes to it are not saved): {x}")
        if loaded[1] is None:
            raise DataError(f"{rel} changed on disk during this run and its loaded form is not known; not overwritten")
        base = [normalize_entry(e) for e in (pickle.loads(loaded[1]) or {}).get("entries") or []]
        theirs = [normalize_entry(e) for e in theirs_doc.get("entries") or []]
        merged = merge_entry_lists(base, ours, theirs, "disk")
        n = sum(any(c.get("from") == "disk" for c in e.get("conflict") or []) for e in merged)
        print(f"{rel}: changed on disk during this run; merged entry by entry, nothing overwritten"
              + (f" ({n} entries with a conflict: ./bib conflicts)" if n else ""), file=sys.stderr)
        sec.entries = merged
        self.invalidate()
        return merged

    def save_list_meta(self, lst):
        d = dict(lst.data)
        d["sections"] = [s.to_data() for s in lst.sections]
        dump_yaml(d, os.path.join(self.root, "lists", lst.key, "list.yaml"),
                  header=[f"{lst.abbr}: page text and outline. Entries live in the files named by 'file'."])

    def save_all(self):
        for lst in self.lists.values():
            self.save_list_meta(lst)
            for s in lst.walk():
                if s.file:
                    self.save_section(s)
