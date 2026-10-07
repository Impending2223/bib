"""The presidential documents (APP) that name each person with a Lives entry: sources/app-names/<letter>.json and
sources/app-index.jsonl.
# Usage: python3 tools/lives/app_names.py CACHE_DIR
#   CACHE_DIR: the corpus tools/lives/app_corpus.py read (index.jsonl and docs/).
#   Writes sources/app-index.jsonl, one document a line {url, date, who, title} in the corpus's order, and for
#   each person {key: [line numbers]}.
#   A document names a person where its text gives the person's name: the first given name (or a name in
#   parentheses, 'Ted'), any further given names or initials, and the surname ('Hubert Humphrey', 'Hubert H.
#   Humphrey'); or a title and the surname ('Senator Humphrey', 'Vice President Humphrey') where no other person
#   with an entry has that surname. A person whose first name and surname another entry shares is left out:
#   the text cannot tell them apart. A document is not counted as naming its own author.
"""
import gzip, hashlib, json, os, re, sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))
from bib import store  # noqa: E402
from bib.lives import people, key_of, split_name  # noqa: E402

OUT = os.path.join(HERE, "..", "..", "sources")
TITLES = (r"(?:Senator|Senators|Secretary|Ambassador|Governor|General|Gen\.|Admiral|Adm\.|Vice President|Mr\.|Mrs\.|Miss|"
          r"Dr\.|Judge|Justice|Representative|Congressman|Congresswoman|Director|Chairman|Commissioner|Attorney "
          r"General|Postmaster General|Under Secretary|Assistant Secretary|Speaker|Leader)")


def forms(p):
    """The regex for a person's names."""
    firsts, mids = set(), set()
    for n in p["names"]:
        sur, given = split_name(n)
        nick = re.findall(r"\(([A-Z][a-z]+)\)", n)
        g = re.sub(r"\([^)]*\)", "", given).replace(",", " ").split()
        g = [w for w in g if not re.fullmatch(r"(Jr|Sr|II|III|IV)\.?", w)]
        if g:
            firsts.add(g[0].rstrip("."))
            for w in g[1:]:
                mids.add(re.escape(w) if w.endswith(".") else re.escape(w) + r"|" + re.escape(w[0]) + r"\.")
        firsts.update(nick)
    first = "|".join(re.escape(f) for f in sorted(firsts) if len(f) > 1)
    if not first:
        return None
    mid = r"(?:\s+(?:" + "|".join(sorted(mids)) + r"))*" if mids else ""
    return rf"\b(?:{first}){mid}\s+{re.escape(p['sur'])}\b"


def main():
    cache = sys.argv[1]
    rows = [json.loads(l) for l in open(os.path.join(cache, "index.jsonl"), encoding="utf-8")]
    with open(os.path.join(OUT, "app-index.jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps({k: r[k] for k in ("url", "date", "who", "title")}, ensure_ascii=False) + "\n")
    everyone = people(store.Series())
    by_sur = {}
    for p in everyone:
        by_sur.setdefault(p["sur"], []).append(p)
    # first name and surname shared by two entries: the text cannot tell them apart
    seen = {}
    for p in everyone:
        for n in p["names"]:
            g = split_name(n)[1].split()
            if g:
                seen.setdefault((p["sur"], g[0]), set()).add(p["name"])
    surnames = set(by_sur)
    texts, docs_by_sur = [], {}
    for i, r in enumerate(rows):
        h = hashlib.sha1(r["url"].encode()).hexdigest()[:16]
        path = os.path.join(cache, "docs", h + ".json.gz")
        t = json.load(gzip.open(path, "rt", encoding="utf-8"))["text"] if os.path.exists(path) else ""
        texts.append(t)
        for w in set(re.findall(r"[A-Z][a-zA-Z'’\-]+", t)) & surnames:
            docs_by_sur.setdefault(w, []).append(i)
    out = {}
    for p in everyone:
        cand = docs_by_sur.get(p["sur"], [])
        if not cand:
            continue
        shared = any(len(v) > 1 for (s, g), v in seen.items() if s == p["sur"] and p["name"] in v)
        if shared:
            continue
        pats = [forms(p)]
        if len(by_sur[p["sur"]]) == 1:
            pats.append(rf"\b{TITLES}\s+{re.escape(p['sur'])}\b")
        rx = re.compile("|".join(x for x in pats if x))
        own = {store.fold(f"{split_name(n)[1].split()[0]} {p['sur']}") for n in p["names"] if split_name(n)[1]}
        hits = [i for i in cand if rx.search(texts[i]) and not any(o and o in store.fold(rows[i]["who"]) for o in own)]
        if hits:
            out[key_of(p["name"])] = hits
    letters = {}
    for k, v in out.items():
        letters.setdefault(k[0].upper(), {})[k] = v
    os.makedirs(os.path.join(OUT, "app-names"), exist_ok=True)
    for f in os.listdir(os.path.join(OUT, "app-names")):
        os.remove(os.path.join(OUT, "app-names", f))
    for L, v in letters.items():
        with open(os.path.join(OUT, "app-names", f"{L}.json"), "w", encoding="utf-8") as f:
            json.dump(v, f, separators=(",", ":"))
    print(len(out), "persons named", sum(len(v) for v in out.values()), "references")


if __name__ == "__main__":
    main()
