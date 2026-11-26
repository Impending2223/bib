"""Apply the re-threading of the China entries (the brief: notes/briefs/china-threads-apply.md; notes/owner-rulings.md, 59,
"the re-threading as applied"; the audit whose verdict it applies: notes/threads/china-tree-audit.md).

    python3 tools/threads/china/apply.py --dry-run     # prints what it would do, thread by thread; writes nothing
    python3 tools/threads/china/apply.py               # writes lists/cal/th.yaml, the entries, notes/threads/china-held.tsv

It reads notes/threads/china-tree.tsv (a row an entry whose thread is `china-leadership` or `china`: id, date, the
primary thread, the rule, the secondary threads; tree.py makes it) and the tree itself from tree.py (PARENT), and
writes through the repository's own reading and writing of entries (tools/bib/store.py: Series, save_section), so the
files stay in the form the tools write.

The threads. Every thread of the tree that th.yaml lacks is added (THREADS below: its name, its statement), its parent
as PARENT gives it (none there: `china`). `india-and-china-cultural-revolution`, the thread the calendar has, stays as
it is and is the parent of the six stages. The China threads are kept together in th.yaml, in alphabetical order of
their full names (check.thread_key).

The entries, a row of the tsv at a time:
 1. The primary thread is the entry's present thread (it fits nothing): nothing changes.
 2. The primary thread is Organization (HELD): the entry is held. Nothing changes; the row goes into
    notes/threads/china-held.tsv.
 3. The primary thread is Propaganda and culture, Army, or Agriculture's own (ALSO_ONLY): `thread:` stays, and that
    thread goes into `also:`, the secondary threads after it.
 4. Any other primary thread: `thread:` becomes it, the secondary threads go into `also:`, and `also:` loses
    `china-leadership` and `china` (an entry that moves does not keep them).
In 3 and 4 `also:` keeps what it has, in its order; the new threads follow, each once. No thread is written beside its
own child or parent: where the entry takes one of the six stages, `also:` loses the stages' parent
(`india-and-china-cultural-revolution`), and a thread the entry already holds, or holds a subthread of, is not added.
Nothing else in an entry changes; no id changes.

Refused, and then nothing at all is written: a row whose entry is missing; a row whose entry's date is not the tsv's;
a row whose entry's present thread is not `china-leadership` or `china`, the two threads the tsv was made from (but a
row already applied, its thread and `also:` as this script would leave them, is counted and passed over, so the
script may be run again); a row naming a thread neither th.yaml nor THREADS has; the Center's daily work as a
secondary thread (the audit's mend 1).
"""
import ast
import collections
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)

from tools.bib import store  # noqa: E402

TSV = os.path.join(ROOT, "notes", "threads", "china-tree.tsv")
HELD_TSV = os.path.join(ROOT, "notes", "threads", "china-held.tsv")
BASE = ("china-leadership", "china")                 # the threads the tsv was made from
TOP = "china"
HELD = {"china-organization"}                        # 2: held until a fresh sample is read
ALSO_ONLY = {"china-propaganda", "china-army", "china-agriculture"}   # 3: not fit as a primary thread
NEVER_SECOND = {"china-center"}                      # the audit's mend 1

# slug -> (name, statement). The statements are those of notes/proposals/china-threads-measure.md, section 3, as its
# two audits left them, with the changes the brief and ruling 59 direct and the stations set on the entries each
# thread holds as applied (notes/threads/china-applied.md says which changed and why). A thread the proposal had no
# statement for has one sentence written from its entries.
THREADS = collections.OrderedDict([
    # episodes
    ("china-shanghai-1960", ("Shanghai and Beidaihe, 1960",
     "The year's targets set at Shanghai; the experts withdrawn and the summer conference at Beidaihe. "
     "{{1960-01-07..1960-01-17|The enlarged Politburo at Shanghai.}} "
     "{{1960-07-05..1960-08-10|Beidaihe; the Soviet experts recalled.}}")),
    ("china-moscow-1960", ("Bucharest and Moscow",
     "The quarrel with Moscow carried into the parties' meetings, from \"Long Live Leninism!\" to the Moscow Statement. "
     "{{1960-04-16|\"Long Live Leninism!\"}} {{1960-06-22..1960-06-26|Peng Zhen at Bucharest.}} "
     "{{1960-11-10..1960-12-01|The eighty-one parties at Moscow; Liu Shaoqi with Khrushchev.}}")),
    ("china-twelve-articles", ("Twelve Articles",
     "The communes' \"communist wind\" checked: the emergency letter and the Ninth Plenum. "
     "{{1960-11-03|The Emergency Directive Letter, the \"Twelve Articles.\"}} "
     "{{1960-11-15|Mao's directive on the \"five winds.\"}} {{1961-01-14..1961-01-18|The Ninth Plenum.}}")),
    ("china-famine", ("Famine",
     "The famine: the deaths and the reports of them, the grain taken, moved and bought abroad, the relief, the "
     "Center's measures. {{1960-06-03|The Taolin report on the deaths.}} "
     "{{1960-10-03|Chen Yun on Hebei and Shandong.}} {{1961-01-03|Henan's relief directive.}}")),
    ("china-sixty-articles", ("Sixty Articles",
     "The year of investigation: the communes' regulations drafted at Canton, revised at Peking, and the industrial "
     "articles at Lushan. {{1961-03-10..1961-03-23|The Canton conference; the Sixty Articles.}} "
     "{{1961-04-02..1961-05-15|Liu Shaoqi in Hunan.}} {{1961-08-23..1961-09-16|Lushan; the Seventy Articles.}}")),
    ("china-seven-thousand", ("Seven Thousand Cadres",
     "The enlarged work conference{{1962| of January 1962}}: Liu's report, Mao's self-criticism, Lin Biao's defense of the "
     "Leap. {{1962-01-11|The conference opens.}} {{1962-01-27|Liu Shaoqi's report.}} {{1962-01-30|Mao's speech.}}")),
    ("china-retreat-1962", ("Xilou and the retreat",
     "Chen Yun's deficit and emergency program, the cities emptied, the household contracts. "
     "{{1962-02-21..1962-02-23|The Xilou meeting.}} {{1962-05-07..1962-05-11|The May work conference; the "
     "streamlining.}} {{1962-07-06..1962-07-23|Mao against household contracting.}}")),
    ("china-tenth-plenum", ("Beidaihe and the Tenth Plenum",
     "\"Never forget class struggle\": the Beidaihe conference, the plenum, Peng Dehuai's case reopened. "
     "{{1962-08-06..1962-08-24|Beidaihe.}} {{1962-08-26|The plenum's preparatory meeting.}} "
     "{{1962-09-24..1962-09-27|The Tenth Plenum.}}")),
    ("china-india-war", ("India war",
     "The border war with India and the cease-fire. {{1962-07-22|The post in the Chip Chap valley.}} "
     "{{1962-11-21|The cease-fire declared.}} {{1963-01-05|Mao and Bandaranaike at Hangzhou.}}")),
    ("china-polemic", ("Polemic",
     "The open polemic with Moscow, from the Twenty-second Congress to Zhou in Moscow after Khrushchev's fall. "
     "{{1961-10-15..1961-10-23|Zhou at the Twenty-second Congress.}} "
     "{{1963-06-14..1963-07-20|The general line; Deng and Suslov.}} {{1964-11-05..1964-11-14|Zhou in Moscow.}}")),
    ("china-four-cleanups", ("Four Cleanups",
     "The socialist education movement: the Ten Points, the work teams, Taoyuan, Niujiao, the Twenty-three Articles. "
     "{{1963-05-02..1963-05-12|The Hangzhou conference; the First Ten Points.}} "
     "{{1964-10-28..1965-05|Yang Shangkun at Niujiao and Xi'an.}} "
     "{{1964-12-15..1965-01-14|The work conference; the Twenty-three Articles.}}")),
    ("china-models", ("Lei Feng, Dazhai, Daqing",
     "The emulation campaigns: Lei Feng, the Dazhai brigade, the Daqing oilfield, learning from the army. "
     "{{1963-03-05..1963-03-06|\"Learn from Comrade Lei Feng.\"}} {{1964-01-02|The General Office on Daqing.}} "
     "{{1964-12|Dazhai's results checked again.}}")),
    ("china-opera", ("Opera reform",
     "The arts rectified: Mao's two instructions, the festival of modern Peking opera, the ministry purged. "
     "{{1964-06-23|Zhou with the festival's troupes.}} {{1964-06-05..1964-07-31|The festival of modern Peking opera.}} "
     "{{1965-04|The Ministry of Culture's rectification ends.}}")),
    ("china-africa-tour", ("Zhou in Africa",
     "Zhou Enlai's and Chen Yi's tour of ten African countries and Albania, the eight principles of aid. "
     "{{1963-12-14|To Cairo.}} {{1963-12-21..1963-12-27|Algeria.}} {{1964-01-15|Accra; the eight principles.}}")),
    ("china-third-front", ("Third Front",
     "The interior industrial base: the Third Plan recast for war, Panzhihua and the southwest railways. "
     "{{1964-05-15..1964-06-17|The work conference; the third front.}} {{1965-03-29|Zhu De at Chengdu.}} "
     "{{1965-11-13|The plan conference.}}")),
    ("china-afro-asian", ("Afro-Asian conference",
     "The second Asian–African conference sought and lost at Algiers. {{1965-03-30..1965-04-01|Zhou at Algiers.}} "
     "{{1965-06-19..1965-06-28|Ben Bella deposed; the conference put off.}} "
     "{{1965-10-22|Zhou's letter: better not to meet.}}")),
    ("china-bomb", ("Bomb",
     "The atomic and hydrogen bombs and the missiles: their decisions and tests. "
     "{{1961-07-16|The Center's decision on the nuclear industry.}} "
     "{{1962-11-17|The special committee under Zhou Enlai.}} {{1963-07-28|The test ban discussed.}} "
     "{{1964-10-16|The first test.}} {{1966-10-27|The missile with a warhead.}} "
     "{{1967-06-17|The hydrogen bomb.}}")),
    ("china-hai-rui", ("Hai Rui",
     "Yao Wenyuan's article, the Peking committee's defense of Wu Han, the February Outline. "
     "{{1965-11-10|Yao Wenyuan's article.}} {{1965-11-29|The *Beijing Daily* reprints it.}} "
     "{{1966-02-12|The February Outline circulated.}}")),
    ("china-luo-ruiqing", ("Luo Ruiqing",
     "The Chief of Staff accused by Lin Biao and removed at the Shanghai conference. "
     "{{1965-11-27|Luo with Lin Biao.}} {{1965-12-08..1965-12-15|The Shanghai conference.}} "
     "{{1966-03-04..1966-04-08|The struggle meetings.}}")),
    ("china-may-sixteenth", ("May Sixteenth and the work teams",
     "The enlarged Politburo and its Circular, Peng Zhen's fall, Nie Yuanzi's poster, the fifty days of the work "
     "teams. {{1966-05-16|The May 16 Circular.}} {{1966-05-25|Nie Yuanzi's poster.}} "
     "{{1966-07-16|Mao in the Yangtze.}} {{1966-07-28|The work teams withdrawn.}}")),
    ("china-red-guards", ("Red Guards",
     "The Eleventh Plenum and the Red Guards: the rallies, the \"four olds,\" the house searches, the attack on the "
     "\"reactionary line.\" {{1966-08-01..1966-08-12|The Eleventh Plenum; \"Bombard the Headquarters.\"}} "
     "{{1966-08-18|The first rally.}} {{1966-10-09..1966-10-28|The October work conference.}}")),
    ("china-seizures", ("Seizures of power",
     "The January Storm at Shanghai, the seizures in the provinces, the army sent in, the February Countercurrent. "
     "{{1967-01-06|The rebels take Shanghai.}} {{1967-01-23|The army to support the left.}} "
     "{{1967-02-16|The Huairen Hall.}}")),
    ("china-wuhan", ("Wuhan and the army",
     "The army's factions and the armed struggle: Wuhan, the drive against \"the handful in the army,\" the fall of "
     "Wang Li and Guan Feng. {{1967-07-20|The Million Heroes take Wang Li.}} "
     "{{1967-08-22|The British office burned.}} {{1967-08-30|Wang Li and Guan Feng detained.}}")),
    ("china-class-ranks", ("Revolutionary committees",
     "The revolutionary committees completed and the class ranks cleansed: Yang Chengwu's fall, the July notices, "
     "the propaganda teams. {{1968-03-24|Yang Chengwu, Yu Lijin and Fu Chongbi dismissed.}} "
     "{{1968-07-28|Mao with the five Red Guard leaders.}} {{1968-09-05|The last committees, Tibet and Xinjiang.}}")),
    ("china-ninth-congress", ("Ninth Congress",
     "Liu Shaoqi expelled at the Twelfth Plenum; the Ninth Congress and Lin Biao as successor. "
     "{{1968-10-13..1968-10-31|The Twelfth Plenum.}} {{1969-04-01..1969-04-24|The Ninth Congress.}} "
     "{{1969-04-28|Lin Biao's report printed.}}")),
    ("china-border-war", ("Border war",
     "The clashes on the Ussuri and in Xinjiang, the war scare, the airport talks and the border talks. "
     "{{1969-03-02|Zhenbao.}} {{1969-09-11|Kosygin at the Peking airport.}} {{1969-10-20|The border talks open.}}")),
    # persons
    ("china-mao", ("Mao Zedong",
     "Mao Zedong's acts: his comments and instructions, letters, talks, audiences, poems, swims, travels. "
     "{{1964-02-13|The Spring Festival forum on education.}} {{1965-05|Jinggangshan revisited.}}")),
    ("china-zhou", ("Zhou Enlai",
     "The Premier's day: the State Council, the plan, the guests and the visits abroad.")),
    ("china-liu", ("Liu Shaoqi",
     "The head of state to his fall: his comments, forums, receptions and visits abroad. "
     "{{1963-04-12..1963-05-16|Indonesia, Burma, Cambodia, Vietnam.}} "
     "{{1964-07|The two labor systems and the two education systems.}} "
     "{{1966-03-26..1966-04-19|Pakistan, Afghanistan, Burma.}}")),
    # systems
    ("china-center", ("Center's daily work",
     "The Politburo's and the Secretariat's sittings on mixed business, the General Office and its callers, the "
     "papers sent round, to Yang Shangkun's removal. {{1960-04-02|The \"five many.\"}} {{1961-05|The recordings.}} "
     "{{1965-11|Yang Shangkun's last month at the General Office.}}")),
    ("china-foreign", ("Foreign affairs",
     "Foreign business not done by Mao, Zhou Enlai or Liu Shaoqi: Chen Yi's and the others' receptions, visits, "
     "speeches and cables, the Foreign Ministry and the International Liaison Department. "
     "{{1961-05-16|Chen Yi at Geneva; the conference on Laos.}} {{1962-07-23|The Geneva agreements on Laos.}}")),
    ("china-army", ("Army",
     "The Military Commission, the General Staff and the General Political Department; training, the coast, the "
     "militia, the marshals' inspections. {{1960-09..1960-10|The enlarged Military Commission.}} "
     "{{1961-01-20|The training conference.}} {{1962-06|Preparing for war on the coast.}} "
     "{{1964-06-10|The display of picked units.}} {{1965-05-22|Ranks abolished.}} "
     "{{1969-10-18|The orders to the General Staff.}}")),
    ("china-economy", ("Finance and economy",
     "The plan, industry and transport, finance and trade: the commissions' and ministries' reports, the Center's "
     "papers on them, the inspections of plants. "
     "{{1962-04-19|The Central Finance and Economic Group under Chen Yun.}} {{1964-08-17|The trusts.}} "
     "{{1965-11|Deng Xiaoping in the Southwest's plants.}}")),
    ("china-agriculture", ("Agriculture",
     "Farming, grain, water and the communes: the Center's rural papers, the leaders' inspections of communes and "
     "farms. {{1960-10-07|Tan Zhenlin on five provinces' farming.}} {{1961-11|Peng Dehuai at Wushi.}} "
     "{{1963-10-16|Zhu De in the flooded provinces.}} "
     "{{1964-06-25|The poor and lower-middle peasant associations.}}")),
    ("china-political-legal", ("Political-legal work",
     "The National People's Congress and its Standing Committee, public security, the procuracy and the courts, the "
     "census. {{1960-03-30|The National People's Congress, second session.}} {{1962-03-27|The third session.}} "
     "{{1963-02-17|The draft Criminal Law.}} {{1964-02-10|The census.}}")),
    ("china-propaganda", ("Propaganda and culture",
     "Propaganda, the press, education, science, health, the arts and sport. "
     "{{1961-07-13|The Secretariat on the schools.}} {{1962-03-05|Chen Yi to the scientists at Canton.}} "
     "{{1962-04-30|The Eight Articles on Literature and Art.}} {{1964-08|The Peking Science Symposium.}} "
     "{{1966-03-08|The Education Office.}}")),
    ("china-organization", ("Organization",
     "Cadres and the Party's own bodies: appointments, the control commissions, the Youth League, the trade unions "
     "and the Women's Federation, the deaths of leaders{{1969-04..|, the case groups after April 1969}}.")),
    ("china-united-front", ("United front and nationalities",
     "The United Front Department, the Political Consultative Conference and the democratic parties, the "
     "nationalities and religion, the overseas Chinese, Taiwan, Hong Kong and Macao. "
     "{{1960-05|The line on Taiwan.}} {{1961-06-15|The forum on placing the bourgeoisie.}} "
     "{{1962-04-16|The Kazakhs' flight.}} {{1962-05|The national united front work conference.}} "
     "{{1965-07-27|The General Office on Li Zongren.}}")),
    # the threads the measurement did not have (tree.py, NEW)
    ("china-moscow", ("Split with Moscow", None)),
    ("china-nuclear", ("Nuclear weapons", None)),
    ("china-nuclear-diplomacy", ("Nuclear diplomacy", None)),
    ("china-mao-foreign", ("Foreign guests", None)),
    ("china-mao-cr", ("Cultural Revolution", None)),
    ("china-zhou-foreign", ("Foreign affairs", None)),
    ("china-zhou-cr", ("Cultural Revolution", None)),
])


def tree():
    """(PARENT, NEW, STAGES, CR) as tree.py holds them, read from its source: tree.py is not imported, since its
    import reads the whole calendar's rules (measure.py) and the command line."""
    src = open(os.path.join(HERE, "tree.py"), encoding="utf-8").read()
    ns = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in ("CR", "STAGES", "PARENT", "NEW"):
            exec(compile(ast.Module([node], []), "tree.py", "exec"), ns)
    return ns["PARENT"], ns["NEW"], ns["STAGES"], ns["CR"]


PARENT, NEW, STAGES, CR = tree()


def parent_of(slug, threads):
    """A thread's parent: PARENT's, else `china` for a thread this script adds, else what th.yaml has."""
    if PARENT.get(slug):
        return PARENT[slug]
    if slug in THREADS:
        return TOP
    return (threads.get(slug) or {}).get("parent")


def line_of(slug, threads):
    """The thread and its parents, nearest first, as the tree will stand."""
    out = []
    while slug and slug not in out:
        out.append(slug)
        slug = parent_of(slug, threads)
    return out


def read_rows():
    with open(TSV, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    for r in rows:
        r["second"] = [t for t in (r.get("also") or "").split(",") if t]
    return rows


def plan_entry(e, row, threads):
    """(kind, thread, also) for one entry and its row: what the entry's `thread` and `also` become. kind: 'left' (it
    fits nothing), 'held', 'also' (its thread stays and takes the threads in `also`), 'set' (it moves)."""
    cur, prim, second = e["thread"], row["thread"], row["second"]
    have = list(e.get("also") or [])
    if prim in HELD:
        return "held", cur, have
    if prim == cur:
        if second:
            raise ValueError("a row that fits nothing has secondary threads")
        return "left", cur, have
    if prim in ALSO_ONLY:
        kind, thread, add = "also", cur, [prim] + second
    else:
        kind, thread, add = "set", prim, second
        have = [t for t in have if t not in BASE]            # an entry that moves keeps neither
    also = [t for t in have if t != thread]
    for t in add:
        if t != thread and t not in also:
            also.append(t)
    # no thread beside its own child or parent: of the entry's threads, the one nearer the root goes. Only the
    # threads this script writes and the stages' parent are in question; `china` beside `china-leadership` on an
    # entry that does not move is the calendar's own and is left.
    mine = set(THREADS) | {CR}
    every = [thread] + also
    drop = set()
    for t in every:
        for up in line_of(t, threads)[1:]:
            if up in every and up in mine and up != thread:
                drop.add(up)
    also = [t for t in also if t not in drop]
    return kind, thread, also


def applied(e, row, threads):
    """Whether the entry is already as this script would leave it (a second run)."""
    prim = row["thread"]
    if prim in HELD or prim in BASE or e["thread"] in BASE:
        return False
    if prim in ALSO_ONLY:
        return False
    return e["thread"] == prim and all(t in (e.get("also") or []) or t in line_of(prim, threads) for t in row["second"]) \
        and not set(e.get("also") or []) & set(BASE)


def thread_entry(slug, old, statements):
    """A thread's entry for th.yaml: id, s, c, parent, and whatever else the present entry holds."""
    name, c = THREADS[slug]
    c = statements.get(slug, c)
    out = {"id": f"cal.thread.{slug}", "s": name}
    if c:
        out["c"] = c
    out["parent"] = PARENT.get(slug) or TOP
    for k, v in (old or {}).items():
        if k not in out and k != "c":
            out[k] = v
    return out


# The statements of the threads the proposal had none for: one sentence each, written from the entries.
WRITTEN = {
    "china-moscow": "The quarrel with the Soviet party: the parties' meetings, the open polemic, the border war.",
    "china-nuclear": "China and nuclear weapons: the bomb and its tests, the diplomacy of the ban, the leaders' "
                     "words on nuclear war.",
    "china-nuclear-diplomacy": "The test ban treaty refused, the proposals for a summit, complete prohibition and no "
                               "first use, the conferences against atomic and hydrogen bombs, non-proliferation. "
                               "{{1964-10-16|The statement on the first test.}}",
    "china-mao-foreign": "Mao Zedong's foreign business: the guests received, the talks, the telegrams and statements. "
                         "{{1960-10-22|Edgar Snow.}} {{1961-09-23|Montgomery at Wuchang.}}",
    "china-mao-cr": "Mao Zedong in the Cultural Revolution's stages: his comments on papers, his instructions and "
                    "talks, the drafts he revised.",
    "china-zhou-foreign": "The Premier's foreign business: the guests received, the visits abroad, the talks, "
                          "statements and cables. {{1960-01-28|The boundary agreement with Burma before the State "
                          "Council.}} {{1960-04|Rangoon, Delhi, Kathmandu.}} {{1963-03-02|Bhutto; the boundary "
                          "agreement with Pakistan.}} {{1965-06|Pakistan and Tanzania.}} "
                          "{{1969-09-02..1969-09-09|Hồ Chí Minh's death.}}",
    "china-zhou-cr": "The Premier in the Cultural Revolution's stages: his speeches and meetings, the Center's "
                     "telegrams and notices he drafted, his instructions to the provinces and the army.",
}


def thread_key(slug, threads):
    """A thread's place in th.yaml, as check.thread_key gives it: a subthread under its parent's key."""
    te = threads[slug]
    if te.get("sort"):
        return te["sort"].lower()
    par = te.get("parent")
    if par in threads and par != slug:
        return thread_key(par, threads) + ": " + (te.get("s") or "").lower()
    return (te.get("s") or "").lower()


def main(argv):
    dry = "--dry-run" in argv
    if [a for a in argv if a != "--dry-run"]:
        sys.exit(__doc__.split("\n\n")[1])
    series = store.Series(ROOT)
    cal = series.lists["cal"]
    th = cal.section(cal.data.get("threads_section", "th"))
    threads = cal.threads()
    rows = read_rows()
    where = {}
    for sec, e in cal.entries():
        if "when" in e:
            where[e["id"]] = (sec, e)

    # ---- the threads
    for slug in list(PARENT) + list(PARENT.values()):
        if slug not in THREADS and slug not in threads:
            sys.exit(f"REFUSED: {slug!r} is in tree.py's PARENT and neither th.yaml nor THREADS has it")
    for slug, name in NEW.items():
        if THREADS.get(slug, (None,))[0] != name:
            sys.exit(f"REFUSED: tree.py names {slug!r} {name!r}; THREADS does not")
    if CR not in threads:
        sys.exit(f"REFUSED: th.yaml has no {CR!r}")
    new_threads, changed_threads = [], []
    after = dict(threads)
    for slug in THREADS:
        want = thread_entry(slug, threads.get(slug), WRITTEN)
        if slug not in threads:
            new_threads.append(slug)
        elif {k: v for k, v in threads[slug].items()} != want:
            changed_threads.append(slug)
        after[slug] = want

    # ---- the entries
    refused, seen = [], set()
    plan = []                                       # (sec, e, kind, thread, also)
    counts = collections.Counter()
    set_n, also_n = collections.Counter(), collections.Counter()
    lost = collections.Counter()
    held_rows = []
    for r in rows:
        eid = r["id"]
        if eid in seen:
            refused.append(f"{eid}: two rows")
            continue
        seen.add(eid)
        if eid not in where:
            refused.append(f"{eid}: no such entry")
            continue
        sec, e = where[eid]
        bad = [t for t in [r["thread"]] + r["second"] if t not in after]
        if bad:
            refused.append(f"{eid}: no thread {bad[0]!r}")
            continue
        if set(r["second"]) & NEVER_SECOND:
            refused.append(f"{eid}: the Center's daily work as a secondary thread")
            continue
        if str(e.get("date")) != r["date"]:
            refused.append(f"{eid}: dated {e.get('date')}, the tsv's row {r['date']}")
            continue
        if applied(e, r, after):
            counts["already applied"] += 1
            continue
        if e["thread"] not in BASE:
            refused.append(f"{eid}: its thread is {e['thread']!r}, not one the tsv was made from")
            continue
        try:
            kind, thread, also = plan_entry(e, r, after)
        except ValueError as x:
            refused.append(f"{eid}: {x}")
            continue
        counts[kind] += 1
        if kind == "held":
            held_rows.append((r, e))
        old_also = list(e.get("also") or [])
        if kind == "set":
            set_n[thread] += 1
        for t in also:
            if t not in old_also:
                also_n[t] += 1
        for t in old_also:
            if t not in also:
                lost[t] += 1
        if thread != e["thread"] or also != old_also:
            plan.append((sec, e, kind, thread, also))
    in_base = sum(1 for sec, e in where.values() if e["thread"] in BASE)
    no_row = [e["id"] for sec, e in where.values() if e["thread"] in BASE and e["id"] not in seen]

    # ---- the report
    print(f"rows {len(rows)}; entries of {' or '.join(BASE)} now: {in_base}; of them with no row: {len(no_row)}")
    print(f"threads to add to th.yaml: {len(new_threads)}; threads there already whose entry would change: "
          f"{len(changed_threads)}" + (f" ({', '.join(changed_threads)})" if changed_threads else ""))
    print(f"entries: thread set {counts['set']}; thread kept and also added {counts['also']}; held {counts['held']}; "
          f"left (fit nothing) {counts['left']}; already applied {counts['already applied']}; "
          f"entries changed {len(plan)}")
    print("\n| thread | parent | thread set | also added |\n|---|---|---:|---:|")
    order = sorted(set(THREADS) | set(set_n) | set(also_n), key=lambda t: thread_key(t, after))
    for t in order:
        print(f"| `{t}` | `{after[t].get('parent') or ''}` | {set_n[t]} | {also_n[t]} |")
    print(f"| total | | {sum(set_n.values())} | {sum(also_n.values())} |")
    print("\nalso taken out: " + (", ".join(f"`{t}` {n}" for t, n in sorted(lost.items())) or "none"))
    for msg in refused[:40]:
        print("REFUSED", msg)
    if refused:
        print(f"{len(refused)} rows refused: nothing written")
        return 1
    if dry:
        print(f"dry run: nothing written ({len({id(s) for s, *_ in plan})} entry files and th.yaml would be)")
        return 0

    # ---- the writing
    for sec, e, kind, thread, also in plan:
        e["thread"] = thread
        if also:
            e["also"] = also
        else:
            e.pop("also", None)
    block = [e for e in th.entries if TOP in line_of(e["id"].split(".", 2)[2], after)]
    at = min(th.entries.index(e) for e in block)
    rest = [e for e in th.entries if not any(e is b for b in block)]
    got = {e["id"].split(".", 2)[2]: e for e in block}
    for slug in THREADS:
        got[slug] = after[slug]
    china = [got[s] for s in sorted(got, key=lambda s: thread_key(s, after))]
    th.entries[:] = rest[:at] + china + rest[at:]
    touched = {id(sec): sec for sec, *_ in plan}
    touched[id(th)] = th
    for sec in touched.values():
        series.save_section(sec)
    with open(HELD_TSV, "w", encoding="utf-8", newline="") as w:
        w.write("id\tdate\tthread\theld from\trule\talso\n")
        for r, e in held_rows:
            w.write(f"{r['id']}\t{r['date']}\t{e['thread']}\t{r['thread']}\t{r['rule']}\t{','.join(r['second'])}\n")
    print(f"written: th.yaml, {len(touched) - 1} entry files, notes/threads/china-held.tsv ({len(held_rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
