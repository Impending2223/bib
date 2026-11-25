"""footnotes.py: volumes, the id. forms, and the marks' places.

Generated once from the code's behaviour on Nov. 19, 2026 (tests/README.md): each row pins what the function returned
then. A row that fails is a change of behaviour: a regression, or a fix to be read and the row rewritten with it.
"""
import html

import pytest

from bib import footnotes

VOL = [
    ('IV, 118', ('IV', '118')),
    ('118', (None, '118')),
    ('', (None, '')),
    (None, (None, '')),
    ('XII, 3–4', ('XII', '3–4')),
    ('iv, 3', (None, 'iv, 3')),
    ('IV,118', ('IV', '118')),
]
ID = [
    ({'key': 'k', 'kind': 'card', 'text': 'T', 'pin': '5', 'paren': None}, None, True, 'T'),
    ({'key': 'k', 'kind': 'card', 'text': 'T', 'pin': '5', 'paren': None}, {'key': 'k', 'kind': 'card', 'text': 'T', 'pin': '5', 'paren': None}, True, '*Id*.'),
    ({'key': 'k', 'kind': 'card', 'text': 'T', 'pin': '5', 'paren': None}, {'key': 'k', 'kind': 'card', 'text': 'T', 'pin': '5', 'paren': None}, False, '*id*.'),
    ({'key': 'k', 'kind': 'card', 'text': 'T', 'pin': '6', 'paren': None}, {'key': 'k', 'kind': 'card', 'text': 'T', 'pin': '5', 'paren': None}, False, '*id*. at 6'),
    ({'key': 'k', 'kind': 'card', 'text': 'T', 'pin': 'IV, 6', 'paren': None}, {'key': 'k', 'kind': 'card', 'text': 'T', 'pin': 'IV, 5', 'paren': None}, False, '*id*. at 6'),
    ({'key': 'k', 'kind': 'card', 'text': 'T', 'pin': 'V, 6', 'paren': None}, {'key': 'k', 'kind': 'card', 'text': 'T', 'pin': 'IV, 5', 'paren': None}, True, '*Id*., V, 6'),
    ({'key': 'k', 'kind': 'card', 'text': 'T', 'pin': None, 'paren': None}, {'key': 'k', 'kind': 'card', 'text': 'T', 'pin': '5', 'paren': None}, False, 'T'),
    ({'key': 'k', 'kind': 'card', 'text': 'T', 'pin': '5', 'paren': '(the vote)'}, {'key': 'k', 'kind': 'card', 'text': 'T', 'pin': '5', 'paren': None}, False, '*id*. (the vote)'),
    ({'key': 'j', 'kind': 'card', 'text': 'T', 'pin': '5', 'paren': None}, {'key': 'k', 'kind': 'card', 'text': 'T', 'pin': '5', 'paren': None}, False, 'T'),
    ({'key': 'u', 'kind': 'url', 'text': 'U', 'pin': None, 'paren': None}, {'key': 'u', 'kind': 'url', 'text': 'U', 'pin': None, 'paren': None}, False, '*id*.'),
    ({'key': 'u', 'kind': 'url', 'text': 'U2', 'pin': None, 'paren': None}, {'key': 'u', 'kind': 'url', 'text': 'U', 'pin': None, 'paren': None}, True, 'U2'),
]
PLACE = [
    ('Kennedy met Rusk. They spoke of Laos.', ['Kennedy met Rusk.', 'They spoke of Laos.'], [(0, 1), (1, 2)], 'e1', ('Kennedy met Rusk.<sup class="fm"><a href="#fn-e1-1" id="fr-e1-1">1</a></sup> They spoke of Laos.<sup '
 'class="fm"><a href="#fn-e1-2" id="fr-e1-2">2</a></sup>')),
    ('Kennedy met Rusk. They spoke of Laos.', ['Kennedy met Rusk.', 'They spoke of Laos.'], [(1, 1)], 'e1', 'Kennedy met Rusk. They spoke of Laos.<sup class="fm"><a href="#fn-e1-1" id="fr-e1-1">1</a></sup>'),
    ('A. B.', ['A.', 'C.'], [(0, 1)], 'e2', None),
    ('A &amp; B.', ['A & B.'], [(0, 1)], 'e3', 'A &amp; B.<sup class="fm"><a href="#fn-e3-1" id="fr-e3-1">1</a></sup>'),
]


@pytest.mark.parametrize("pin,want", VOL)
def test_vol(pin, want):
    assert footnotes._vol(pin) == want


@pytest.mark.parametrize("cur,prev,head,want", ID)
def test_id(cur, prev, head, want):
    assert footnotes._id(cur, prev, head) == want


@pytest.mark.parametrize("whole,units,groups,eid,want", PLACE)
def test_place(whole, units, groups, eid, want):
    assert footnotes.place(whole, html.escape, units, groups, eid) == want


# STYLE 11: a work's page and a note on that page, one source when neighbouring units are compared.
def _card(pin, **kw):
    return dict(kind="card", key="w.x", pin=pin, paren="", text=f"[[w.x]], {pin}", **kw)


PAGE = _card("88")
JOINED = _card("88 & n.32", base="88", notes=("32",), joined=True)
ALONE = _card("88 n.32", base="88", notes=("32",), joined=False, alt=JOINED)
OTHER = _card("88 n.33", base="88", notes=("33",), joined=False, alt=_card("88 & n.33", base="88", notes=("33",), joined=True))
ONE = [
    ([PAGE], [JOINED], [JOINED]),                # the page, then the page with its note: the fuller citation
    ([JOINED], [PAGE], [JOINED]),
    ([PAGE], [ALONE], [JOINED]),                 # the page, then the note alone: the page with its note
    ([ALONE], [JOINED], [JOINED]),
    ([ALONE], [OTHER], None),                    # two notes of one page: two sources
    ([PAGE], [_card("89")], None),               # two pages
    ([PAGE], [dict(PAGE, key="w.y")], None),     # two works
    ([PAGE], [PAGE, JOINED], None),              # one source more
]


@pytest.mark.parametrize("a,b,want", ONE)
def test_page_and_note_one(a, b, want):
    assert footnotes._one(a, b) == want
