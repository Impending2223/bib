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
    tested worst (notes/threads/china-assign-audit.md). The Center's daily work is never a secondary thread (AUDIT 2 (1)).
 5. Nuclear weapons: the bomb (measure.py's episode, and before July 1963 WEAPON_EARLY) and the diplomacy (DIPLOMACY
    below) are siblings; the diplomacy at the line's opening goes first, and Bomb only where the line names the weapon
    (AUDIT 2 (3)); talk of nuclear war gives the parent as a secondary thread (TALK; AUDIT 2 (5)).
 6. `china-leadership` stays the thread only of the entries that fit nothing.
 7. The entries of the plain `china` thread (the China the calendar's other nations deal with) are run too, for the
    episodes and the nuclear threads only: the persons' and the systems' rules were made and tested on
    `china-leadership`. One that fits nothing stays in `china`.
The audit of Nov. 26, 2026 (notes/threads/china-tree-audit.md) mended the rules; each mend is marked `AUDIT 2 (n)`
here and in measure.py.
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
    # AUDIT 2 (2): the words the first list missed: "complete and thorough prohibition", a ban on nuclear weapons,
    # a zone free of them, their spread.
    r"complete(?:,)? (?:and )?thorough(?:,? and resolute)? prohibition|prohibition and (?:thorough )?destruction of (?:nuclear|atomic)|"
    r"bann?(?:ing)? (?:on |of )?nuclear weapons|ban on nuclear|nuclear ban|nuclear-free|free of nuclear|"
    r"(?:spread|dissemination|proliferation) of nuclear|"
    r"(?:ban|banning|prohibition)(?: and [a-z ]{0,25}destruction)? (?:of|on) (?:nuclear|atomic)|"
    r"(?:ban|prohibition) and (?:thorough |complete |total )?destruction of (?:nuclear|atomic)|"
    r"禁止原子弹氢弹|部分禁止核试验|三国条约|全面禁止|彻底销毁|核扩散|核保护伞|无核区", re.I)
TALK = re.compile(r"nuclear blackmail|atomic blackmail|nuclear war\b|atomic war\b|nuclear monopoly|"
                  r"核讹诈|核垄断|核战争", re.I)
# AUDIT 2 (3, 4, 6): the weapon itself: the programme, the tests, the bombs, the missiles. NUC is any word that
# measure.py's Bomb takes; WEAPON the weapon's own words; WEAPON_EARLY those that hold before July 1963, when
# measure.py's Bomb has no window (the Center's decisions of 1961-62, the Special Commission, the design).
NUC = re.compile(r"atomic|nuclear|原子弹|核武器|核试验|核爆炸|hydrogen bomb|氢弹|missile|导弹|Lop Nur|罗布泊|two bombs|两弹|"
                 r"test ban|Qian Xuesen|钱学森|(?-i:Special Commi)|warhead|test range|Second Ministry of Machine", re.I)
WEAPON = re.compile(r"atomic bombs?|hydrogen bombs?|原子弹|氢弹|nuclear (?:tests?|explosions?|devices?|industry|weapons? (?:programme|program))|"
                    r"(?:first|second|third|new) (?:atomic |nuclear )?(?:test|explosion)|核试验|核爆炸|missiles?|导弹|warheads?|"
                    r"Lop Nur|罗布泊|two bombs|两弹|(?-i:Special Commi(?:ssion|ttee))|专门委员会|Second Ministry of Machine|"
                    r"test range|nuclear submarines?|uranium|铀", re.I)
WEAPON_EARLY = re.compile(r"atomic bombs?|原子弹|atomic weapons|nuclear (?:weapons? )?(?:programme|program)|nuclear industry|"
                          r"atomic (?:energy )?industry|核工业|原子能工业|(?-i:Special Commi(?:ssion|ttee))|专门委员会|"
                          r"Second Ministry of Machine|二机部|two bombs|两弹|Lop Nur|罗布泊|nuclear device|"
                          r"advanced weapons|frontier technology|尖端技术|尖端武器", re.I)
HEADZONE = 200


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
    later = []                                       # threads that may only follow the persons and the systems
    # AUDIT 2 (6): before July 1963 the weapon's own words place Bomb, as an episode.
    if e["date"][:7] < "1963-07" and "china-bomb" not in [t for t, _ in fits]:
        m = WEAPON_EARLY.search(text)
        if m and m.start() < HEADZONE:
            fits.append(("china-bomb", "nuclear:weapon"))
    # AUDIT 2 (4): Bomb by a word of measure.py's list that comes only after the line's opening (a remark on the bomb
    # in a planning conference, an army training conference) follows the persons and the systems.
    if "china-bomb" in [t for t, _ in fits]:
        m = NUC.search(text)
        if not m or m.start() >= HEADZONE:
            later += [x for x in fits if x[0] == "china-bomb"]
            fits = [x for x in fits if x[0] != "china-bomb"]
    dm = DIPLOMACY.search(text)
    nuc = []
    if dm and dm.start() < HEADZONE:
        # AUDIT 2 (3): the diplomacy at the line's opening goes before Bomb; Bomb stays only where the line names
        # the weapon itself (a test, the programme), not where "nuclear" and "test ban" are all it has.
        nuc = [("china-nuclear-diplomacy", "nuclear:diplomacy")]
    elif dm:
        later.append(("china-nuclear-diplomacy", "nuclear:diplomacy"))
    if dm and not WEAPON.search(text):
        fits = [x for x in fits if x[0] != "china-bomb"]
        later = [x for x in later if x[0] != "china-bomb"]
    if not dm and "china-bomb" not in [t for t, _ in fits + later] and TALK.search(text):
        later.append(("china-nuclear", "nuclear:talk"))   # AUDIT 2 (5): talk of nuclear war is a secondary thread
    bomb_first = [x for x in fits if x[0] == "china-bomb"]
    fits = [x for x in fits if x[0] != "china-bomb"]
    k = next((i for i, (t, r) in enumerate(fits) if not r.startswith(("ep:", "nuclear:"))), len(fits))
    fits[k:k] = nuc + bomb_first                     # with the episodes, after them: a stage or a conference first
    fits += later
    names = [t for t, _ in fits]
    stage = any(t in STAGES for t in names)
    foreign = "china-foreign" in names or e.get("_foreign")
    out = []
    for i, (t, r) in enumerate(fits):
        if t in SUB:                                 # 3: the person's subthread
            t = SUB[t][1] if stage else SUB[t][0] if foreign else t
        elif t in SYS_SLUG and i and e["_sc"].get(SYS_SLUG[t], 0) < STRONG and not r.startswith("sys:body"):
            continue                                 # 4: a weak second system
        elif t == "china-center" and i:
            continue                                 # AUDIT 2 (1): the Center's daily work is never a secondary thread (31 of 38 read were wrong)
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
    if "cal.thread.china-famine" in open(os.path.join(M.ROOT, "lists", "cal", "th.yaml"), encoding="utf-8").read():
        sys.exit("tree.py: the re-threading is applied (apply.py; notes/threads/china-applied.md). The rules read only "
                 "the entries still in `china-leadership` or `china`, so a run now would overwrite "
                 "notes/threads/china-tree.tsv with the few that remain. Run it on a checkout from before the "
                 "re-threading, or teach read_calendar to read the applied threads first.")
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
