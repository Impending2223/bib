"""One-time import of the published pages into the YAML store.

Reads the compiled reader ("The 1968 series"), which holds every list with its
calendar links already resolved, and writes series.yaml and lists/. Links the
compiler added (section refs, "Elsewhere" lines, the names index) are dropped;
the build regenerates them. Kept for re-imports: `./bib import PATH --force`.
"""
import json
import os
import re

from . import store
from .htmlparse import parse, Node
from .markup import plain

MONTHS = {"Jan.": 1, "Feb.": 2, "Mar.": 3, "Apr.": 4, "May": 5, "June": 6, "July": 7,
          "Aug.": 8, "Sept.": 9, "Oct.": 10, "Nov.": 11, "Dec.": 12}

ARTIFACTS = {
    "kja": "https://claude.ai/artifact/GUYbuovFgtY7vupMuTTJ4g",
    "kjc": "https://claude.ai/artifact/9APT15miQoMTDCewtvQTmq",
    "opp": "https://claude.ai/artifact/RJgBq4vjC92oWH91e1b9wR",
    "cal": "https://claude.ai/artifact/RfxuiEcENspJmjbGyT5zXh",
    "l68": "https://claude.ai/artifact/728hqXTjcv3aogmvCBnpgM",
    "adm": "https://claude.ai/artifact/UnACbvVAd3HguTvpsaE6RM",
    "cong": "https://claude.ai/artifact/1rzmmHQPAvEZpqVvxshNkc",
    "wg": "https://claude.ai/artifact/R7oEex8RCkSQhjjec7puCG",
}
PAGE_TITLES = {
    "kja": "Kennedy and Johnson Administrations, 1961–1969: Bibliography",
    "kjc": "Congress, the Nation, and the States, 1961–1969: Bibliography",
    "opp": "Republican Opposition, 1961–1969: Bibliography",
    "cal": "Calendar, January–September 1961",
    "l68": "1968 Thriller: Bibliography",
    "adm": "Nixon Administration, 1969–1974: Bibliography",
    "cong": "Congress, the Nation, and the States, 1969–1974: Bibliography",
    "wg": "Watergate, 1971–1974: Bibliography",
}
COMPILED = "https://claude.ai/artifact/9VsXuvj8UhFT9pLFxVMav5"


# ---------------------------------------------------------------- inline html -> markup

def inline(node, xd):
    """Markup text for a span's children. xd collects (placeholder) calendar refs."""
    out = []
    for c in node.children:
        if isinstance(c, str):
            out.append(c)
            continue
        if c.tag == "i":
            out.append("*" + inline(c, xd) + "*")
        elif c.tag == "a" and "x" in c.classes:
            inner = inline(c, xd)
            if "xd" in c.classes:
                out.append(f"[[@{c.attrs['href'][1:]}|{inner}]]")
            else:
                out.append(inner)
        elif c.tag == "a":
            out.append(f"[{inline(c, xd)}]({c.attrs['href']})")
        else:
            raise ValueError(f"unexpected <{c.tag}> in text")
    return "".join(out)


def heading(h):
    num = None
    title_parts = []
    for c in h.children:
        if isinstance(c, Node) and "num" in c.classes:
            num = c.text().strip()
        else:
            title_parts.append(c if isinstance(c, str) else c.text())
    title = "".join(title_parts).strip()
    if num is None:
        m = re.match(r"^([IVX]+\.(?:[A-Z](?:\.\d+)?)?)\s+(.*)$", title)
        if m:
            num, title = m.group(1), m.group(2)
    return num, title


# ---------------------------------------------------------------- ids

def _author_title_slug(c0):
    text = plain(c0)
    m = re.search(r"\*([^*]+)\*", c0)
    title = m.group(1) if m else ""
    if c0.startswith("*") or not text.split(",")[0].strip():
        return store.slug(title or text, 5)
    author = re.split(r"\s+(?:&|with)\s+", text.split(",")[0])[0]
    words = [w for w in author.replace(".", " ").split() if w not in ("Jr", "Sr", "II", "III")]
    sur = store.slug(words[-1] if words else author, 2)
    t = re.sub(r"^(the|a|an)\s+", "", (title or text[len(text.split(',')[0]) + 1:]).strip(), flags=re.I)
    return f"{sur}-{store.slug(t, 3)}".strip("-")


def make_id(key, sec, e, taken):
    if e.get("s"):
        base = store.slug(plain(e["s"]), 5)
        part = (sec.get("num") or "").split(".")[0]
        base = f"{key}.{'who.' if part == 'III' else ''}{base}"
    else:
        base = f"{key}.{_author_title_slug(store.as_list(e['c'])[0])}"
    eid, n = base, 2
    while eid in taken:
        eid, n = f"{base}-{n}", n + 1
    taken.add(eid)
    return eid


def parse_when(when, year):
    """'Apr. 15–19' -> '1961-04-15'; 'Feb.' -> '1961-02'; 'June–July' -> '1961-06'."""
    m = re.match(r"^(Jan\.|Feb\.|Mar\.|Apr\.|May|June|July|Aug\.|Sept\.|Oct\.|Nov\.|Dec\.)\s*(\d+)?", when)
    if not m:
        raise ValueError(f"cannot date {when!r}")
    mo = MONTHS[m.group(1)]
    return f"{year}-{mo:02d}-{int(m.group(2)):02d}" if m.group(2) else f"{year}-{mo:02d}"


# ---------------------------------------------------------------- import

def run(path, root=store.ROOT, force=False):
    if os.path.exists(os.path.join(root, "series.yaml")) and not force:
        raise SystemExit("series.yaml exists; pass --force to overwrite the store from HTML")
    raw = open(path, encoding="utf-8").read()
    dom = parse(raw)
    meta = json.loads(re.search(r"var META=(\{.*?\}), ORDER=", raw).group(1))
    order = json.loads(re.search(r"ORDER=(\[.*?\]);", raw).group(1))

    sections = {s.attrs["data-key"]: s for s in dom.find_all(lambda n: n.tag == "section" and "list" in n.classes)}
    home = sections["home"]
    home_data = {"h1": None, "lede": None, "logic": []}
    for el in home.elements():
        if el.tag == "h1":
            home_data["h1"] = el.text().strip()
        elif el.tag == "p" and "lede" in el.classes:
            home_data["lede"] = inline(el, None)
        elif el.tag == "p" and "logic" in el.classes:
            home_data["logic"].append(inline(el, None))
    # the first home paragraph quotes link counts; the build fills them in
    home_data["logic"] = [re.sub(r"\d+ links and \d+ such lines in all\.", "{counts}", p) for p in home_data["logic"]]

    series = {
        "title": meta["home"]["title"],
        "compiled_artifact": COMPILED,
        "home": home_data,
        "names_index": {"title": meta["nx"]["title"]},
        "outside_lists": ["the Vietnam bibliography"],
        "lists": [],
    }
    old_to_new = {}
    lists_out = {}
    taken = set()

    for key in order:
        if key in ("home", "nx"):
            continue
        sec_el = sections[key]
        m = meta[key]
        rec = {"key": key, "abbr": m["abbr"], "title": m["title"], "span": m["span"],
               "group": m["group"], "artifact": ARTIFACTS.get(key)}
        if key == "l68":
            rec["cite_as"] = ["the 1968 list", "The 1968 list", "1968 list"]
        series["lists"].append(rec)
        ldata = {"page_title": PAGE_TITLES.get(key, m["title"]), "h1": None, "lede": None, "logic": []}
        if key == "cal":
            ldata.update({"kind": "calendar", "year": 1961, "threads_section": "th"})
        tops, stack = [], []
        current = None
        entries_by_sec = {}
        for el in sec_el.elements():
            if el.tag == "h1":
                ldata["h1"] = el.text().strip()
            elif el.tag == "p" and "lede" in el.classes:
                ldata["lede"] = inline(el, None)
            elif el.tag == "p" and "logic" in el.classes:
                (current["logic"] if current else ldata["logic"]).append(inline(el, None))
            elif el.tag in ("h2", "h3", "h4"):
                level = int(el.tag[1])
                num, title = heading(el)
                sid = el.attrs["id"].split("--", 1)[1]
                node = {"id": sid, "num": num, "title": title, "logic": [], "sections": []}
                short = el.attrs.get("data-short")
                if short and short != (f"{num} {title}" if num else title):
                    node["short"] = short
                while stack and stack[-1][0] >= level:
                    stack.pop()
                (stack[-1][1]["sections"] if stack else tops).append(node)
                stack.append((level, node))
                current = node
            elif el.tag == "ol" and "e" in el.classes:
                if current is None:
                    raise ValueError(f"{key}: entries before any heading")
                lst = entries_by_sec.setdefault(current["id"], [])
                for li in el.elements():
                    if li.tag != "li":
                        continue
                    e = {"_old": li.attrs.get("id"), "c": []}
                    for sp in li.elements():
                        cls = sp.classes[0] if sp.classes else ""
                        if cls == "x2":
                            continue
                        if cls not in ("s", "c", "r", "n"):
                            raise ValueError(f"{key}: unexpected span .{cls}")
                        val = inline(sp, None).strip()
                        if cls == "c":
                            e["c"].append(val)
                        elif cls in e:
                            raise ValueError(f"{key}: two .{cls} in {li.attrs.get('id')}")
                        else:
                            e[cls] = val
                    lst.append(e)
            elif el.tag in ("nav",):
                continue
            else:
                raise ValueError(f"{key}: unexpected <{el.tag}> at top level")

        # file names and ids
        def assign(nodes):
            for n in nodes:
                if n["id"] in entries_by_sec:
                    code = (n["num"] or "").rstrip(".")
                    n["file"] = (n["id"] if key == "cal" or not code else code) + ".yaml"
                assign(n["sections"])
        assign(tops)

        def clean(nodes):
            for n in nodes:
                if not n["logic"]:
                    del n["logic"]
                if not n["num"]:
                    del n["num"]
                clean(n["sections"])
                if not n["sections"]:
                    del n["sections"]
        clean(tops)
        if key == "cal":
            _calendar_ranges(tops, 1961)
        ldata["sections"] = tops
        if not ldata["logic"]:
            del ldata["logic"]

        flat = {}
        def secmap(nodes):
            for n in nodes:
                flat[n["id"]] = n
                secmap(n.get("sections", []))
        secmap(tops)

        for sid, ents in entries_by_sec.items():
            for e in ents:
                if key == "cal" and sid != "th":
                    mm = re.match(r"^(.*?) \((.+)\)$", e["s"])
                    e["when"], e["_thread_name"] = mm.group(1), mm.group(2)
                    e["date"] = parse_when(e["when"], 1961)
                if key == "cal" and sid == "th":
                    e["_thread_slug"] = store.slug(e["s"], 8)
        if key == "cal":
            names = {e["s"]: e["_thread_slug"] for e in entries_by_sec["th"]}
            for sid, ents in entries_by_sec.items():
                if sid == "th":
                    continue
                for e in ents:
                    e["thread"] = names[e.pop("_thread_name")]
                    del e["s"]
                    base = f"cal.{e['date']}.{e['thread']}"
                    eid, n = base, 2
                    while eid in taken:
                        eid, n = f"{base}-{n}", n + 1
                    taken.add(eid)
                    e["id"] = eid
            for e in entries_by_sec["th"]:
                e["id"] = f"cal.thread.{e.pop('_thread_slug')}"
                taken.add(e["id"])
        else:
            for sid, ents in entries_by_sec.items():
                for e in ents:
                    e["id"] = make_id(key, flat[sid], e, taken)
        for ents in entries_by_sec.values():
            for e in ents:
                if e.get("_old"):
                    old_to_new[e["_old"]] = e["id"]
        lists_out[key] = (ldata, flat, entries_by_sec)

    # resolve calendar links, derive thread membership
    # Only notes carry deliberate cross-references ("See Apr. 15-19"). The compiler
    # also linked dates mentioned in passing in event lines and the intro, some to
    # the wrong entry; those go back to plain text.
    def fix(text):
        return re.sub(r"\[\[@([^|\]]+)\|([^\]]+)\]\]", lambda m: f"[[{old_to_new[m.group(1)]}|{m.group(2)}]]", text)

    def unlink(text):
        return re.sub(r"\[\[@([^|\]]+)\|([^\]]+)\]\]", lambda m: m.group(2), text)

    for key, (ldata, flat, ents_by) in lists_out.items():
        if ldata.get("lede"):
            ldata["lede"] = unlink(ldata["lede"])
        if ldata.get("logic"):
            ldata["logic"] = [unlink(p) for p in ldata["logic"]]
        for n in flat.values():
            if "logic" in n:
                n["logic"] = [unlink(p) for p in n["logic"]]
        for ents in ents_by.values():
            for e in ents:
                for f in ("s", "r"):
                    if f in e:
                        e[f] = unlink(e[f])
                if "n" in e:
                    e["n"] = fix(e["n"])
                e["c"] = [unlink(x) for x in e["c"]]

    if "cal" in lists_out:
        _calendar_threads(lists_out["cal"])

    # drop the shown text where it is just the target's label
    labels = {}
    for key, (ldata, flat, ents_by) in lists_out.items():
        for ents in ents_by.values():
            for e in ents:
                if "when" in e:
                    labels[e["id"]] = e["when"]
    def tidy(text):
        return re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]",
                      lambda m: f"[[{m.group(1)}]]" if labels.get(m.group(1)) == m.group(2) else m.group(0), text)
    for key, (ldata, flat, ents_by) in lists_out.items():
        if ldata.get("lede"):
            ldata["lede"] = tidy(ldata["lede"])
        if ldata.get("logic"):
            ldata["logic"] = [tidy(p) for p in ldata["logic"]]
        for ents in ents_by.values():
            for e in ents:
                for f in ("s", "r", "n"):
                    if f in e:
                        e[f] = tidy(e[f])
                e["c"] = [tidy(x) for x in e["c"]]

    # write
    store.dump_yaml(series, os.path.join(root, "series.yaml"),
                    header=["The series: its lists, their abbreviations, and where each is published.",
                            "Order here is the order of the compiled reader."])
    for key, (ldata, flat, ents_by) in lists_out.items():
        d = os.path.join(root, "lists", key)
        os.makedirs(d, exist_ok=True)
        for fn in os.listdir(d):
            if fn.endswith(".yaml"):
                os.remove(os.path.join(d, fn))
        store.dump_yaml(ldata, os.path.join(d, "list.yaml"),
                        header=[f"{dict((l['key'], l['abbr']) for l in series['lists'])[key]}: page text and outline. "
                                "Entries live in the files named by 'file'."])
        for sid, ents in ents_by.items():
            sec = flat[sid]
            out = []
            for e in ents:
                e.pop("_old", None)
                if not e["c"]:
                    del e["c"]
                if key == "cal" and sid == "th":
                    e.pop("n", None)  # derived from the entries
                out.append(store.normalize_entry(e))
            code = (sec.get("num") or "").rstrip(".") or sid
            abbr = dict((l['key'], l['abbr']) for l in series['lists'])[key]
            store.dump_yaml({"list": key, "section": code, "entries": out}, os.path.join(d, sec["file"]),
                            header=[f"{abbr} {code} {sec['title']}",
                                    "Entries in display order. See CLAUDE.md for the fields. Run ./bib check after editing."])
    return lists_out


def _calendar_threads(cal):
    """Each thread lists its dates. Where a date's entry belongs to another thread,
    record this thread under the entry's 'also'. The thread lines are then derived."""
    ldata, flat, ents_by = cal
    byid = {e["id"]: e for sid, ents in ents_by.items() if sid != "th" for e in ents}
    for t in ents_by["th"]:
        slug = t["id"].split(".", 2)[2]
        for m in re.finditer(r"\[\[([^|\]]+)\|([^\]]+)\]\]", t.get("n", "")):
            target = byid[m.group(1)]
            if target["thread"] != slug:
                target.setdefault("also", [])
                if slug not in target["also"]:
                    target["also"].append(slug)


FULL_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
               "September", "October", "November", "December"]


def _calendar_ranges(tops, year):
    """Give each month section the dates it holds, from its title:
    'February' -> whole month; 'January 20–31'; 'Prologue, January 3–19'."""
    import calendar
    for n in tops:
        m = re.search(r"(" + "|".join(FULL_MONTHS) + r")(?:\s+(\d+)–(\d+))?", n["title"])
        if not m:
            continue
        mo = FULL_MONTHS.index(m.group(1)) + 1
        d1 = int(m.group(2) or 1)
        d2 = int(m.group(3) or calendar.monthrange(year, mo)[1])
        if n["id"] == "pro":
            d1 = 1
        n["from"] = f"{year}-{mo:02d}-{d1:02d}"
        n["to"] = f"{year}-{mo:02d}-{d2:02d}"
