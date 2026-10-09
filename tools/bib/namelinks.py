"""Links from a person's name, as a source writes it, to the person's name entry (names-<letter>.html#<key>).

One person a name entry (tools/bib/lives.py, people): the names Part III, the Executive roster and the Congress
rosters write are each one person's. A name links only where it is one of those, exactly; where a source writes
the name otherwise (a calendar's 'Names:' surname, an election's candidate, a FRUS author, a work's author), the
caller finds the person first and passes one of the person's names.

STYLE: the links are muted (class "nm", templates: list.html, series.html, roster.css): the text keeps its color,
a faint underline shows the link. A name in the person's own entry is not linked (own=).
"""
import html
import re

from . import lives as L


def index(series):
    """{name as written: (url, the person's name)} for everyone with a name entry."""
    def make():
        out = {}
        for p in L.everyone(series):
            url = f"names-{L.letter_of(p)}.html#{L.key_of(p['name'])}"
            for n in p["names"] | {p["name"]}:
                out.setdefault(n, (url, p["name"]))
        return out
    return L.cached("name-links", make)


def url(series, name):
    """The name entry's address for a name as Part III or the rosters write it, or None."""
    hit = index(series).get(re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()) or index(series).get(name)
    return (L.SITE + hit[0]) if hit else None


def person(series, name):
    """The name the person's entry is filed under, or None."""
    hit = index(series).get(re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()) or index(series).get(name)
    return hit[1] if hit else None


def a(series, name, inner, own=None):
    """inner (html) linked to the person's name entry, muted; unchanged where the person has none or is `own`."""
    u = url(series, name)
    if not u or (own and person(series, name) == person(series, own)):
        return inner
    return f'<a class="nm" href="{u}">{inner}</a>'


def by_surname(series):
    """{folded surname: [person]} for everyone with a name entry."""
    def make():
        out = {}
        for p in L.cached("people", lambda: L.people(series)):
            out.setdefault(L.fold(p["sur"]), []).append(p)
        return out
    return L.cached("name-surnames", make)


def written(series, name):
    """The person a name written in running order names ('Theodore C. Sorensen', 'Lyndon B. Johnson'): the one
    person with an entry whose surname is its last word and whose given names agree with the rest. None for a bare
    surname, or where two persons fit."""
    name = name.strip()
    last = L.last_word(name)
    if not last or len(name.split()) < 2:
        return None
    hits = [p for p in by_surname(series).get(L.fold(last), []) if L.is_person(name, p["sur"], p["given"])]
    return hits[0]["name"] if len(hits) == 1 else None


def author_split(series, c, own=None):
    """(html of the citation's authors, each linked to his name entry, the rest of the citation) where any links;
    (None, c) otherwise. Not the person whose entry it is (own), not an author with no entry."""
    a = L.author_of(c)
    if not a or not c.startswith(a):
        return None, c
    out, linked = [], False
    for part in re.split(r"( & | and )", a):
        p = written(series, part) if part not in (" & ", " and ") else None
        if p and not (own and p == person(series, own)):
            out.append(f'<a class="nm" href="{url(series, p)}">{html.escape(part)}</a>')
            linked = True
        else:
            out.append(html.escape(part))
    return ("".join(out), c[len(a):]) if linked else (None, c)


def frus_sender(series, key):
    """The name entry's address for the sender of a FRUS document ('frus:frus1961-63v05/d110'), from the index of the
    documents each person sent (sources/frus-names, tools/lives/frus_names.py); or None."""
    def make():
        import glob
        import json
        import os
        out = {}
        for f in glob.glob(os.path.join(L.store.ROOT, "sources", "frus-names", "[A-Z].json")):
            for pk, vols in json.load(open(f, encoding="utf-8")).items():
                for vol, v in vols.items():
                    for row in v.get("sent") or []:
                        out.setdefault((vol, str(row[0])), set()).add(pk)
        return out
    m = re.match(r"frus:([^/]+)/d?(\w+)$", key or "")
    if not m:
        return None
    pks = L.cached("frus-senders", make).get((m.group(1), m.group(2))) or set()
    by_key = L.cached("name-keys", lambda: {L.key_of(p["name"]): p["name"] for p in L.everyone(series)})
    alias = L._CACHE.get("frus-alias", {})       # forms joined in one entry (lives.frus_groups): one sender
    whos = {by_key.get(alias.get(k, k)) for k in pks}
    if len(whos) != 1:
        return None
    who = next(iter(whos))
    return url(series, who) if who else None


CSS = ("a.nm{color:inherit;text-decoration:underline;text-decoration-color:color-mix(in srgb,var(--muted) 40%,"
       "transparent);text-decoration-thickness:1px;text-underline-offset:.2em}"
       "a.nm:hover{text-decoration-color:var(--accent,currentColor)}")
