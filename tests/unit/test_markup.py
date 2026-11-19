"""markup.py: to_html, plain, refs, italics, with stub card and entry resolvers.

Generated once from the code's behaviour on Nov. 19, 2026 (tests/README.md): each row pins what the function returned
then. A row that fails is a change of behaviour: a regression, or a fix to be read and the row rewritten with it.
"""
import pytest

from bib import markup

TO_HTML = [
    ('plain text', 'plain text'),
    ('*Italic Title*', '<i>Italic Title</i>'),
    ('A & B < C', 'A &amp; B &lt; C'),
    ('"quoted"', '"quoted"'),
    ('[a link](https://example.com/x)', '<a href="https://example.com/x">a link</a>'),
    ('[UN Res. 232](https://undocs.org/S/RES/232(1966))', '<a href="https://undocs.org/S/RES/232(1966)">UN Res. 232</a>'),
    ('[[cal.1961-04-15.cuba]]', '<a href="#cal.1961-04-15.cuba">Apr. 15</a>'),
    ('[[cal.1961-04-15.cuba|the landing]]', '<a href="#cal.1961-04-15.cuba">the landing</a>'),
    ('[[kja.unknown]]', 'kja.unknown'),
    ('[[w.beschloss-crisis-years]], 123', '<a class="x xw" href="works.html#w.beschloss-crisis-years">Beschloss, <i>Crisis Years</i></a>, 123'),
    ('[[w.kaplan-mcnamara]], 468', '<a class="x xw" href="works.html#w.kaplan-mcnamara">Kaplan, <i>McNamara Ascendancy, 1961–1965</i></a>, at 468'),
    ('[[w.kaplan-mcnamara]], I, 12', '<a class="x xw" href="works.html#w.kaplan-mcnamara">Kaplan, <i>McNamara Ascendancy, 1961–1965</i></a>, I, 12'),
    ('[[w.beschloss-crisis-years|\x01full]], 99', ('<a class="x xw xf" href="works.html#w.beschloss-crisis-years">Michael R. Beschloss, <i>The Crisis Years</i></a> '
 '(1991), 99')),
    ('[[w.unknown-card]], 5', 'w.unknown-card, 5'),
    ('*Title* and [[cal.1961-04-15.cuba]] and [x](http://a.b/c)', '<i>Title</i> and <a href="#cal.1961-04-15.cuba">Apr. 15</a> and <a href="http://a.b/c">x</a>'),
    ('', ''),
    (None, ''),
    ('**', '**'),
    ('*a* *b*', '<i>a</i> <i>b</i>'),
    ('[[w.beschloss-crisis-years|Beschloss]], 7', '<a class="x xw" href="works.html#w.beschloss-crisis-years">Beschloss</a>, 7'),
]
PLAIN = [
    ('*T*', 'T'),
    ('[t](https://x.y)', 't'),
    ('[[cal.1961-04-15.cuba]]', 'cal.1961-04-15.cuba'),
    ('[[cal.x|shown]]', 'shown'),
    ('[[w.beschloss-crisis-years]], 4', 'Beschloss, Crisis Years, 4'),
    ('[a](https://undocs.org/S/RES/232(1966)) b', 'a b'),
    (None, ''),
    ('no markup', 'no markup'),
]
REFS = [
    ('[[a]] and [[b|c]]', ['a', 'b']),
    ('none', []),
    ('[[w.x]], 1; [[cal.y]]', ['w.x', 'cal.y']),
    ('', []),
    (None, []),
    ('[[a|b]][[c]]', ['a', 'c']),
]
ITALICS = [
    ('*A* and *B*', ['A', 'B']),
    ('[*L*](https://x.y) *M*', ['L', 'M']),
    ('none', []),
    (None, []),
    ('**', []),
]

WORKS = {"w.beschloss-crisis-years": "Beschloss, *Crisis Years*", "w.kaplan-mcnamara": "Kaplan, *McNamara Ascendancy, 1961–1965*"}
FULL = {"w.beschloss-crisis-years": "Michael R. Beschloss, *The Crisis Years* (1991)",
        "w.kaplan-mcnamara": "Lawrence S. Kaplan et al., *The McNamara Ascendancy, 1961–1965* (2006)"}


@pytest.fixture(autouse=True)
def stub_works(monkeypatch):
    """The card resolvers store.Series would set, as stubs."""
    monkeypatch.setattr(markup, "WORKS", lambda cid: WORKS.get(cid))
    monkeypatch.setattr(markup, "WORKS_FULL", lambda cid: FULL[cid])
    monkeypatch.setattr(markup, "WORKS_ID", lambda cid: cid)


def resolve(eid, shown):
    if eid.startswith("cal."):
        return f'<a href="#{eid}">{shown or "Apr. 15"}</a>'
    return None


@pytest.mark.parametrize("text,want", TO_HTML)
def test_to_html(text, want):
    assert markup.to_html(text, resolve) == want


@pytest.mark.parametrize("text,want", PLAIN)
def test_plain(text, want):
    assert markup.plain(text) == want


@pytest.mark.parametrize("text,want", REFS)
def test_refs(text, want):
    assert markup.refs(text) == want


@pytest.mark.parametrize("text,want", ITALICS)
def test_italics(text, want):
    assert markup.italics(text) == want


def test_label_resolver():
    assert markup.plain("[[cal.x]] on", label=lambda i: "Apr. 1") == "Apr. 1 on"
