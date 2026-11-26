"""threads.py, STYLE 9 and 10: a thread and its subthreads. A parent's page lists its own entries alone and names every
thread under it at the end of its head, each with its count and its span; a thread with entries only under it has a
page, its head alone; the count says both numbers where the family holds more; an old link to an entry the page no
longer holds goes on to the calendar; a dropped part is its own thread's, not a thread's whose name its name begins
with. On the fixture: Cuba over Bay of Pigs; the 1960 elections, with one entry, its subthread's; and a small tree of
the test's own for the order and the names."""
import os
import re
import shutil
import subprocess

import pytest

from bib import build, pages, store, threads

LI = re.compile(r'<li (?:class="[^"]*" )?id="t-([^"]+)"')
SUBS = re.compile(r'<p class="logic">([^<]*)</p>\n<ol class="e thx">(.*?)</ol>', re.S)
ONLY = {"cuba", "cuba-bay-of-pigs", "elections-1960", "elections-1960-chicago", "vietnam"}


@pytest.fixture(scope="module")
def series():
    return store.Series()


@pytest.fixture(scope="module")
def cal(series):
    return series.lists["cal"]


@pytest.fixture(scope="module")
def built(series):
    pages.reset()
    return dict(threads.pages_(series, build.Linker(series), os.path.join(build.TEMPLATES, "list.html"), only=ONLY))


def own(cal, slug):
    return [e["id"] for _, e in cal.entries() if "when" in e and (
        e.get("thread") == slug or slug in (e.get("also") or []))]


def test_parent_lists_its_own_entries_alone(cal, built):
    """The owner's rule of Nov. 4: an entry filed under a subthread is on the subthread's page, not its parent's."""
    page = built["threads-cuba.html"]
    assert sorted(LI.findall(page)) == sorted(own(cal, "cuba"))
    under_only = set(own(cal, "cuba-bay-of-pigs")) - set(own(cal, "cuba"))
    assert under_only and not under_only & set(LI.findall(page))


def test_subthreads_at_the_end_of_the_head(cal, built):
    """Under the statement and the line, above the entries: the index's list, a line a subthread, its name after the
    page's thread, linked, its count and its span."""
    page = built["threads-cuba.html"]
    m = SUBS.search(page)
    assert m and m.group(1) == "1 subthread, on its own page."
    n = len(own(cal, "cuba-bay-of-pigs"))
    assert m.group(2) == ('<li><span class="s"><a href="threads-cuba-bay-of-pigs.html">Bay of Pigs</a></span>'
                          f'<span class="n">{n} entries, Apr.–Aug. 1961.</span></li>')
    assert page.index('<p class="lede">') < page.index("The thread in the calendar") < m.start() < page.index('<li id="t-')
    assert "Subthreads: " not in page                     # the list in place of the names in the line
    # a ghost as the index marks it; no list on a thread with nothing under it
    assert '<li class="thg"><span class="s"><a href="threads-vietnam-johnson-asia.html">LBJ in Asia</a>' \
        in SUBS.search(built["threads-vietnam.html"]).group(2)
    assert not SUBS.search(built["threads-cuba-bay-of-pigs.html"])


def test_both_counts_where_they_differ(cal, built):
    fam = {e["id"] for e in build.thread_members(cal)["cuba"]}
    mine = own(cal, "cuba")
    assert fam == set(mine) | set(own(cal, "cuba-bay-of-pigs")) and len(fam) > len(mine)
    page = built["threads-cuba.html"]
    assert f"{len(mine)} entries, in the calendar's order" in page
    assert f"The thread and its subthreads together hold {len(fam)}, an entry counted once" in page
    assert "together hold" not in built["threads-cuba-bay-of-pigs.html"]
    assert threads.count(cal, "cuba") == f"{len(mine)} entries; {len(fam)} with its subthreads"
    assert threads.count(cal, "cuba-bay-of-pigs") == f"{len(own(cal, 'cuba-bay-of-pigs'))} entries"
    assert f'<span class="n">{len(mine)} entries; {len(fam)} with its subthreads.</span>' in built["threads.html"]


def test_parent_with_no_entries_of_its_own_has_a_page(cal, built):
    """Its statement, the line, its subthreads; no list of entries. Its subthread's "Part of" leads to it."""
    assert not own(cal, "elections-1960") and own(cal, "elections-1960-chicago")
    page = built["threads-elections-1960.html"]
    assert "<h1>1960 elections</h1>" in page and '<p class="lede">' in page
    assert "No entries of its own. Its subthreads hold 1, an entry counted once" in page
    assert not LI.findall(page) and '<ol class="e">' not in page and "<h2 " not in page[page.index("<h1>"):]
    assert SUBS.search(page).group(2) == ('<li><span class="s"><a href="threads-elections-1960-chicago.html">Chicago</a>'
                                         '</span><span class="n">1 entry, Apr. 1961.</span></li>')
    assert 'Part of <a href="threads-elections-1960.html">1960 elections</a>' in built["threads-elections-1960-chicago.html"]
    ix = built["threads.html"]
    assert '<a href="threads-elections-1960.html">1960 elections</a>' in ix
    assert '<span class="n">No entries of its own; 1 in its subthreads.</span>' in ix
    assert threads.index_link(cal, "elections-1960") == ""        # the calendar's "All entries": its own entries


def test_every_thread_with_entries_in_its_family_has_a_page(cal):
    have = threads.slugs(cal)
    fam = build.thread_members(cal)
    assert have == [s for s, te in cal.threads().items() if not te.get("see") and fam.get(s)]
    for s in have:                                   # a "Part of" never leads to a page that is not built
        par = cal.threads()[s].get("parent")
        assert not par or par in have, s
    assert len(have) > len([s for s in have if threads.members(cal, s)])


class Tree:
    """A thread tree of the test's own: th.yaml's order, a subthread filed away from its parent."""
    T = {"a": {"s": "A"}, "a-x": {"s": "X", "parent": "a"}, "a-y": {"s": "Y", "parent": "a", "c": "y"},
         "b": {"s": "B"}, "a-x-1": {"s": "One", "parent": "a-x", "c": "1"}, "a-x-2": {"s": "*Two*", "parent": "a-x"},
         "a-z": {"s": "Z", "parent": "a"}, "old": {"s": "Old", "see": "a"}}
    OWN = {"a": 3, "a-x": 0, "a-y": 2, "b": 1, "a-x-1": 4, "a-x-2": 1, "a-z": 0}

    def threads(self):
        return self.T

    def thread_parent(self, s):
        return (self.T.get(s) or {}).get("parent")

    thread_line = store.List.thread_line
    is_ghost = store.List.is_ghost


def entry(date, n=0):
    return {"id": f"cal.{date}.t-{n}", "date": date, "when": date}


@pytest.fixture
def tree(monkeypatch):
    lst = Tree()
    own_ = {s: [entry("1961-04-15", i) for i in range(n)] for s, n in Tree.OWN.items()}
    own_["a-x-1"] = [entry("1960-01-05"), entry("1960-03"), entry("1961"), entry("1962-12-31")]

    def fam(l, s):
        return own_.get(s, []) + [e for k, es in own_.items() if k != s and s in lst.thread_line(k) for e in es]
    monkeypatch.setattr(threads, "members", lambda l, s: own_.get(s, []))
    monkeypatch.setattr(threads, "family", fam)
    return lst


def test_order_and_names(tree):
    """The index's order, a subthread's own subthreads after it; a thread with no entries in its family left out; a
    name after the page's thread."""
    assert threads.slugs(tree) == ["a", "a-x", "a-y", "b", "a-x-1", "a-x-2"]
    assert threads.under(tree, "a") == ["a-x", "a-x-1", "a-x-2", "a-y"]
    assert threads.under(tree, "a-x") == ["a-x-1", "a-x-2"] and threads.under(tree, "b") == []
    assert [threads.name_under(tree, s, "a") for s in threads.under(tree, "a")] == ["X", "X: One", "X: Two", "Y"]
    assert threads.name_under(tree, "a-x-1", "a-x") == "One"
    got = threads.subthreads(tree, "a")
    assert got[0] == '<p class="logic">4 subthreads, each on its own page.</p>'
    assert got[1] == ('<ol class="e thx">'
                      '<li class="thg"><span class="s"><a href="threads-a-x.html">X</a></span>'
                      '<span class="n">No entries of its own; 5 in its subthreads, 1960–1962.</span></li>'
                      '<li><span class="s"><a href="threads-a-x-1.html">X: One</a></span>'
                      '<span class="n">4 entries, 1960–1962.</span></li>'
                      '<li class="thg"><span class="s"><a href="threads-a-x-2.html">X: Two</a></span>'
                      '<span class="n">1 entry, Apr. 1961.</span></li>'
                      '<li><span class="s"><a href="threads-a-y.html">Y</a></span>'
                      '<span class="n">2 entries, Apr. 1961.</span></li></ol>')
    assert threads.subthreads(tree, "b") == []
    assert threads.count(tree, "a") == "3 entries; 10 with its subthreads"
    assert threads.count(tree, "a", True) == "3 entries, Apr. 1961; 10 with its subthreads"


def test_span():
    """As a part's span is written: a month for an entry placed in a month, a year for one placed in a year."""
    assert threads.span([entry("1961-04-15")]) == "Apr. 1961"
    assert threads.span([entry("1961-04-15"), entry("1961-08-02")]) == "Apr.–Aug. 1961"
    assert threads.span([entry("1961-10-03"), entry("1962-03")]) == "Oct. 1961–Mar. 1962"
    assert threads.span([entry("1961")]) == "1961"
    assert threads.span([entry("1960-01-06"), entry("1968-12-30")]) == "1960–1968"
    assert threads.span([entry("1961"), entry("1962-02-01")]) == "Jan. 1961–Feb. 1962"
    assert threads.span([]) == ""


def test_retired_part_is_its_own_threads(cal, series, monkeypatch):
    """A dropped part of "China: Leadership" forwards to that thread, not to "China", whose name its name begins with
    (STYLE 10)."""
    assert threads.retired_of(cal, "threads-china-leadership-1960Q1") == "china-leadership"
    assert threads.retired_of(cal, "threads-china-leadership-1966-04") == "china-leadership"
    assert threads.retired_of(cal, "threads-china-1962") == "china"
    assert threads.retired_of(cal, "threads-china-1962x") == "china"
    assert threads.retired_of(cal, "threads-elections-1960-1961") == "elections-1960"
    assert threads.retired_of(cal, "threads-elections-1960") is None      # no thread "elections": a page, not a part
    assert threads.retired_of(cal, "threads-china-leadership") is None
    assert threads.retired_of(cal, "threads-no-such-thread-1960") is None
    assert threads.retired_of(cal, "names-ba-1960") is None
    plan = {"threads": {"china": [{"page": "threads-china-1960", "from": "1960-01-01", "label": "1960"},
                                  {"page": "threads-china-1961", "from": "1961-01-01", "label": "1961"}],
                        "china-leadership": [{"page": "threads-china-leadership-1960", "from": "1960-01-01", "label": "1960"},
                                             {"page": "threads-china-leadership-1961", "from": "1961-01-01", "label": "1961"}]},
            "retired": ["threads-china-leadership-1960Q1", "threads-vietnam-1961", "names-ba-blanch"]}
    monkeypatch.setattr(pages, "conf", lambda: plan)
    got = dict(threads.pages_(series, build.Linker(series), os.path.join(build.TEMPLATES, "list.html"),
                              only={"china-leadership", "vietnam"}))
    stub = got["threads-china-leadership-1960Q1.html"]
    assert '"threads-china-leadership-1961"' in stub and '"threads-china-1961"' not in stub
    assert '<a href="threads-china-leadership.html">the index</a>' in stub
    one = got["threads-vietnam-1961.html"]                # the thread one page again: there
    assert '"f":[["","threads-vietnam"]]' in one and '<a href="threads-vietnam.html">the index</a>' in one
    assert "names-ba-blanch.html" not in got


def test_onward_script_on_a_page_of_entries(built):
    assert "sent on to the calendar" in built["threads-cuba.html"]
    assert "sent on to the calendar" not in built["threads-elections-1960.html"]
    assert "sent on to the calendar" not in built["threads.html"]


@pytest.mark.skipif(not shutil.which("node"), reason="node is not installed: the page's script is not run")
def test_onward_script(tmp_path):
    """An entry the page does not hold goes to its permalink, a day to the calendar's; an anchor the page holds, one
    not the page's own form, and a month's or a year's stay."""
    js = re.search(r"<script>(.*)</script>", threads.onward("cal"), re.S).group(1)
    cases = {"t-cal.1960-02-03.china-leadership-5": "e.html#cal.1960-02-03.china-leadership-5",
             "t-cal.1961-04.cuba": "e.html#cal.1961-04.cuba",
             "t-d1961-04-17": "cal.html#d1961-04-17",
             "t-cal.1961-04-17.cuba": None,               # held
             "t-m1961-04": None, "t-y1961": None, "vis": None, "": None, "cal.1961-04-17.cuba": None,
             "t-cal.1961-04-17.caf%C3%A9": "e.html#cal.1961-04-17.café"}
    p = tmp_path / "t.js"
    p.write_text("var out={};var held={'t-cal.1961-04-17.cuba':1};\n"
                 "var document={getElementById:function(i){return held[i]||null}};\n"
                 "var window={addEventListener:function(){}};\n"
                 "var cases=" + __import__("json").dumps(list(cases)) + ";\n"
                 "cases.forEach(function(h){var to=null;\n"
                 "  var location={hash:h?'#'+h:'',replace:function(u){to=u}};\n"
                 "  (function(){" + js + "})();\n"
                 "  out[h]=to;});\n"
                 "console.log(JSON.stringify(out));\n", encoding="utf-8")
    r = subprocess.run(["node", str(p)], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    assert __import__("json").loads(r.stdout) == cases
