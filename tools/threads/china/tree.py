"""The China threads as a tree, an entry in every thread it fits (the owner, Nov. 25, 2026; notes/owner-rulings.md, 59;
notes/proposals/china-threads-revision.md).

    python3 tools/threads/china/tree.py            # writes notes/threads/china-tree.tsv and prints the sizes

measure.py's rules find every thread an entry fits (`assign` returns them in order: episode, person, system). This
script turns that list into the entry's threads:
 1. The first fit is the primary thread; the rest go in `also` ("the tiebreaker ... should decide \"the primary
    thread,\" not \"the only thread\"").
 2. PARENT places each thread in the tree. A thread's entries are its parents' too (build.entry_threads), so a parent
    is never written beside its own child.
 3. A person's entry goes to his subthread where one fits (his foreign business; the Cultural Revolution's stages),
    else to his own thread.
 4. A system that is not the primary thread goes in `also` only on a strong score (STRONG): the systems' word lists
    tested worst (notes/threads/china-assign-audit.md).
 5. Nuclear weapons: the bomb (measure.py's episode) and the diplomacy (DIPLOMACY below) are siblings; talk of
    nuclear war goes to the parent (TALK).
 6. `china-leadership` stays the thread only of the entries that fit nothing.
 7. The entries of the plain `china` thread (the China the calendar's other nations deal with) are run too, for the
    episodes and the nuclear threads only: the persons' and the systems' rules were made and tested on
    `china-leadership`. One that fits nothing stays in `china`.
The tsv: id, date, primary thread, the rule that placed it, the secondary threads (comma-separated).
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = sys.argv[:1] + [a for a in sys.argv[1:] if a.startswith("--")]
import measure as M          # noqa: E402
import systems as SY         # noqa: E402

CR = "india-and-china-cultural-revolution"       # the thread the calendar has; kept as the six stages' parent
STAGES = ["china-may-sixteenth", "china-red-guards", "china-seizures", "china-wuhan", "china-class-ranks",
          "china-ninth-congress"]
PARENT = {                                       # thread -> its parent (None: straight under `china`)
    "china-famine": "china-agriculture", "china-twelve-articles": "china-agriculture",
    "china-sixty-articles": "china-agriculture",
    "china-retreat-1962": "china-economy", "china-third-front": "china-economy",
    "china-moscow": "china-foreign", "china-moscow-1960": "china-moscow", "china-polemic": "china-moscow",
    "china-border-war": "china-moscow", "china-india-war": "china-foreign", "china-africa-tour": "china-foreign",
    "china-afro-asian": "china-foreign",
    "china-opera": "china-propaganda", "china-models": "china-propaganda", "china-hai-rui": "china-propaganda",
    "china-luo-ruiqing": "china-army",
    "china-bomb": "china-nuclear", "china-nuclear-diplomacy": "china-nuclear",
    "china-mao-foreign": "china-mao", "china-mao-cr": "china-mao",
    "china-zhou-foreign": "china-zhou", "china-zhou-cr": "china-zhou",
    **{s: CR for s in STAGES},
}
NEW = {                                          # threads the measurement did not have: slug -> name
    "china-moscow": "Split with Moscow", "china-nuclear": "Nuclear weapons",
    "china-nuclear-diplomacy": "Nuclear diplomacy",
    "china-mao-foreign": "Foreign guests", "china-mao-cr": "Cultural Revolution",
    "china-zhou-foreign": "Foreign affairs", "china-zhou-cr": "Cultural Revolution",
}
SUB = {"china-mao": ("china-mao-foreign", "china-mao-cr"), "china-zhou": ("china-zhou-foreign", "china-zhou-cr")}
SYS_SLUG = {v[0]: k for k, v in SY.NAMES.items()}
STRONG = 4
DIPLOMACY = re.compile(
    r"against Atomic and Hydrogen Bombs|against A- and H-[Bb]ombs|bann?(?:ing)? (?:on )?atomic and hydrogen|"
    r"test[- ]ban|partial ban|three-power treaty|tripartite treaty|no first use|(?:not|never) be the first to use|"
    r"complete prohibition|thorough destruction of nuclear|non-?proliferation|nuclear umbrella|"
    r"禁止原子弹氢弹|部分禁止核试验|三国条约|全面禁止|彻底销毁|核扩散|核保护伞", re.I)
TALK = re.compile(r"nuclear blackmail|atomic blackmail|nuclear war\b|atomic war\b|nuclear monopoly|"
                  r"核讹诈|核垄断|核战争", re.I)


def line(t):
    """A thread and its parents, nearest first."""
    out = [t]
    while PARENT.get(out[-1]):
        out.append(PARENT[out[-1]])
    return out


def threads(e):
    """(primary, rule, [secondary]) for one entry."""
    _, rule, _, fits = M.assign(e)
    fits = list(fits)
    if e["thread"] == "china":                       # 7: the plain China thread's entries: the episodes only
        fits = [(t, r) for t, r in fits if r.startswith("ep:")]
    text = e["_plain"]
    nuc = [("china-nuclear-diplomacy", "nuclear:diplomacy")] if DIPLOMACY.search(text) else []
    if not nuc and "china-bomb" not in [t for t, _ in fits] and TALK.search(text):
        nuc = [("china-nuclear", "nuclear:talk")]
    k = next((i for i, (t, r) in enumerate(fits) if not r.startswith("ep:")), len(fits))
    fits[k:k] = nuc                                  # with the episodes, after them: a stage or a conference first
    names = [t for t, _ in fits]
    stage = any(t in STAGES for t in names)
    foreign = "china-foreign" in names or e.get("_foreign")
    out = []
    for i, (t, r) in enumerate(fits):
        if t in SUB:                                 # 3: the person's subthread
            t = SUB[t][1] if stage else SUB[t][0] if foreign else t
        elif t in SYS_SLUG and i and e["_sc"].get(SYS_SLUG[t], 0) < STRONG and not r.startswith("sys:body"):
            continue                                 # 4: a weak second system
        if t not in [x for x, _ in out]:
            out.append((t, r))
    if not out:
        return e["thread"], rule, []
    held = set()                                     # 2: no parent beside its child
    for t, _ in out:
        held |= set(line(t)[1:])
    out = [(t, r) for t, r in out if t not in held]
    return out[0][0], out[0][1], [t for t, _ in out[1:]]


def main():
    ALL = M.read_calendar()
    M.prepare(ALL)
    CL = [e for e in ALL if e["thread"] in ("china-leadership", "china")]
    rows = [(e, *threads(e)) for e in CL]
    path = os.path.join(M.ROOT, "notes", "threads", "china-tree.tsv")
    with open(path, "w", encoding="utf-8") as w:
        w.write("id\tdate\tthread\trule\talso\n")
        for e, t, r, also in rows:
            w.write(f"{e['id']}\t{e['date']}\t{t}\t{r}\t{','.join(also)}\n")
    prim, every, family = collections.Counter(), collections.Counter(), collections.Counter()
    n_also = collections.Counter()
    for e, t, r, also in rows:
        prim[t] += 1
        n_also[min(len(also), 3)] += 1
        fam = set()
        for x in [t] + also:
            every[x] += 1
            fam |= set(line(x))
        for x in fam:
            family[x] += 1
    kids = collections.defaultdict(list)
    for t in set(every) | set(PARENT) | set(PARENT.values()):
        kids[PARENT.get(t)].append(t)
    print(f"entries {len(rows)}; secondary threads an entry carries: " +
          ", ".join(f"{k if k < 3 else '3+'}: {v}" for k, v in sorted(n_also.items())))
    print("\n| thread | primary | every entry in it | with its subthreads |\n|---|---:|---:|---:|")

    def show(t, depth):
        print(f"| {'&nbsp;&nbsp;' * depth}`{t}` | {prim[t]} | {every[t]} | {family[t] if kids.get(t) else ''} |")
        for c in sorted(kids.get(t, []), key=lambda x: -family[x]):
            show(c, depth + 1)
    for t in sorted(kids[None], key=lambda x: -family[x]):
        show(t, 0)


if __name__ == "__main__":
    main()
