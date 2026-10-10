"""Loading and saving the series: series.yaml, lists/<key>/list.yaml, lists/<key>/<file>.yaml.

Everything on disk is plain YAML so it can be grepped and hand-edited. This
module is the only place that knows the layout; the rest of the tools work on
the in-memory objects it returns.
"""
import datetime
import hashlib
import json
import os
import re
import unicodedata

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LISTS = os.path.join(ROOT, "lists")

# Field order inside an entry. Anything else is kept, after these.
ENTRY_FIELDS = ["id", "when", "date", "thread", "also", "s", "c", "c2", "r", "n", "gloss", "tags", "aliases", "conflict"]


# ---------------------------------------------------------------- yaml i/o

class _Loader(yaml.SafeLoader):
    pass


# Dates and times stay strings: "1961-04-15" must not turn into a date object.
_Loader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


class DataError(SystemExit):
    pass


_PARSED = {}                             # path -> (mtime, size, pickled data): each file parsed once a run
CACHE_DIR = os.path.join(ROOT, ".cache", "yaml")   # and kept between runs, by path, mtime and size (git-ignored)


def load_yaml(path):
    """A YAML file's data, parsed once: the parse is kept in memory for the run and on disk (.cache/yaml) for later
    runs, keyed by the file's path, modification time and size. Each caller gets its own copy (callers change
    what they load)."""
    import pickle
    try:
        st = os.stat(path)
    except OSError:
        st = None
    if st is not None:
        sig = (st.st_mtime_ns, st.st_size)
        hit = _PARSED.get(path)
        if hit and hit[0] == sig:
            return pickle.loads(hit[1])
        disk = os.path.join(CACHE_DIR, hashlib.sha1(os.path.abspath(path).encode()).hexdigest() + ".pickle")
        try:
            with open(disk, "rb") as f:
                dsig, blob = pickle.load(f)
            if dsig == sig:
                _PARSED[path] = (sig, blob)
                return pickle.loads(blob)
        except (OSError, EOFError, pickle.UnpicklingError, ValueError):
            pass
    data = _parse_yaml(path)
    if st is not None:
        blob = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
        _PARSED[path] = (sig, blob)
        try:
            os.makedirs(CACHE_DIR, exist_ok=True)
            tmp = disk + f".{os.getpid()}.tmp"
            with open(tmp, "wb") as f:
                pickle.dump((sig, blob), f, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp, disk)
        except OSError:
            pass
    return data


def _parse_yaml(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if "\n<<<<<<< " in "\n" + text:
        raise DataError(f"{os.path.relpath(path, ROOT)}: git conflict markers. Run ./bib setup once so git "
                        "merges these files entry by entry, or settle the markers by hand.")
    try:
        return yaml.load(text, Loader=_Loader)
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


def _emit(v, indent):
    """Block YAML with one field per line; lists of strings become '- ' items."""
    pad = " " * indent
    if isinstance(v, dict):
        lines = []
        for k, x in v.items():
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
            if isinstance(x, dict):
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
    text = _emit(obj, 0) + "\n"
    if header:
        text = "".join("# " + h + "\n" for h in header) + text
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


# ---------------------------------------------------------------- ids and keys

def slug(text, maxwords=6):
    t = unicodedata.normalize("NFKD", text.replace("Đ", "D").replace("đ", "d"))   # Đ has no decomposition
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    t = t.lower().replace("&", " and ").replace("'", "").replace("’", "")
    words = re.findall(r"[a-z0-9]+", t)
    return "-".join(words[:maxwords])


def fold(text):
    """Comparison form of a title or name: no accents, case, or punctuation."""
    return " ".join(slug(text, 999).split("-"))


def canonical(entry):
    """The entry without bookkeeping fields, as a stable string."""
    core = {k: v for k, v in entry.items() if k not in ("conflict",)}
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
    for k in ("also", "tags", "aliases"):
        if k in e:
            e[k] = [str(x) for x in as_list(e[k])]
            if not e[k]:
                del e[k]
    if isinstance(e.get("c"), list) and len(e["c"]) == 1:
        e["c"] = e["c"][0]
    ordered = {k: e[k] for k in ENTRY_FIELDS if k in e}
    ordered.update({k: v for k, v in e.items() if k not in ordered})
    return ordered


# ---------------------------------------------------------------- the model

class Section:
    def __init__(self, data, lst, parent=None, level=2):
        self.lst = lst
        self.parent = parent
        self.level = level
        self.id = data["id"]
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
        """Calendar lists: thread slug -> the thread's own entry."""
        th = self.section(self.data.get("threads_section", "")) if self.kind == "calendar" else None
        return {e["id"].split(".", 2)[2]: e for e in th.entries} if th else {}


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
            self.lists[key] = lst
        self._index = None

    # lookups
    def index(self):
        """id (and alias) -> (list, section, entry)."""
        if self._index is None:
            idx = {}
            for lst in self.lists.values():
                for s, e in lst.entries():
                    idx[e["id"]] = (lst, s, e)
            for lst in self.lists.values():
                for s, e in lst.entries():
                    for a in e.get("aliases", []):
                        idx.setdefault(a, (lst, s, e))
            self._index = idx
        return self._index

    def get(self, eid):
        return self.index().get(eid)

    def by_abbr(self):
        return {l.abbr: l for l in self.lists.values()}

    def invalidate(self):
        self._index = None

    # writing
    def save_section(self, sec):
        lst = sec.lst
        path = os.path.join(self.root, "lists", lst.key, sec.file)
        head = [f"{lst.abbr} {sec.code or ''} {sec.title}".replace("  ", " ").strip(),
                "Entries in display order. See CLAUDE.md for the fields. Run ./bib check after editing."]
        dump_yaml({"list": lst.key, "section": sec.code or sec.id,
                   "entries": [normalize_entry(e) for e in sec.entries]}, path, header=head)

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
