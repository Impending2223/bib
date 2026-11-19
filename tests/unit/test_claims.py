"""claims.py: units of `c`, claim-map rows, items, the note's parts, chash.

Generated once from the code's behaviour on Nov. 19, 2026 (tests/README.md): each row pins what the function returned
then. A row that fails is a change of behaviour: a regression, or a fix to be read and the row rewritten with it.
"""
import pytest

from bib import claims

UNITS = [
    ('One. Two.', ['One.', 'Two.']),
    ('Kennedy met Rusk; they spoke of Laos.', ['Kennedy met Rusk;', 'they spoke of Laos.']),
    ('He said: "Go. Now." Then left.', ['He said: "Go. Now."', 'Then left.']),
    ('Pub. L. 87-1 enacted. Next.', ['Pub. L. 87-1 enacted.', 'Next.']),
    ('(A. B.) C.', ['(A. B.) C.']),
    ('The U.S. Army moves. Next.', ['The U.S. Army moves.', 'Next.']),
    ('Ends with no stop', ['Ends with no stop']),
    ('', []),
    (None, []),
    ('4 p.m. Kennedy leaves.', ['4 p.m.', 'Kennedy leaves.']),
    ('Is it? Yes! Done.', ['Is it?', 'Yes!', 'Done.']),
    ('Apr. 17. The landing.', ['Apr. 17.', 'The landing.']),
    ('J. F. Kennedy speaks. Then.', ['J. F. Kennedy speaks.', 'Then.']),
]
PARSE_ROW = [
    ('w.card 123: all', ('card', 'w.card', '123', None, 'all')),
    ('w.card IV, 118: A-C', ('card', 'w.card', 'IV, 118', None, 'A-C')),
    ('via w.card 88 n.44: B', ('via', 'w.card', '88', '44', 'B')),
    ('via w.card III, 34 n.66a: A, C', ('via', 'w.card', 'III, 34', '66a', 'A, C')),
    ('via x.1961-04-24.holt-to-marcy: B-D', ('witness', 'x.1961-04-24.holt-to-marcy', None, None, 'B-D')),
    ('https://history.state.gov/x/d51: A-B', ('url', 'https://history.state.gov/x/d51', None, None, 'A-B')),
    ('"a quoted text": ?', ('text', 'a quoted text', None, None, '?')),
    ('w.card: all', ('card', 'w.card', None, None, 'all')),
    ('nonsense', None),
    ('w.card 12: a', None),
    ('w.card 12: AA-AB', ('card', 'w.card', '12', None, 'AA-AB')),
    ('', None),
    (None, None),
]
PARSE_UNITS = [
    ('all', 3, {'B', 'A', 'C'}),
    ('?', 3, '?'),
    ('A-C', 5, {'B', 'A', 'C'}),
    ('A, C', 5, {'A', 'C'}),
    ('C-A', 5, None),
    ('A-ZZZ', 3, None),
    ('B', 1, {'B'}),
]
ITEM_KEY = [
    ('[[w.card]], 123', ('card', 'w.card', '123', None)),
    ('[[w.card]], 123 (the vote)', ('card', 'w.card', '123', '(the vote)')),
    ('[[w.card]]', ('card', 'w.card', None, None)),
    ('[[w.card]], on Rusk', ('card', 'w.card', None, None)),
    ('[[w.card]], xi–xii', ('card', 'w.card', 'xi–xii', None)),
    ('[[w.card]], [77–81](https://x.y/z#page=75) (the talk)', ('url', 'https://x.y/z#page=75')),
    ('[Doc](https://history.state.gov/d1)', ('url', 'https://history.state.gov/d1')),
    ('[UN Res. 232](https://undocs.org/S/RES/232(1966))', ('url', 'https://undocs.org/S/RES/232(1966')),
    ('Bundy to Johnson, Feb. 7, 1965, NSF', ('text', 'Bundy to Johnson, Feb.')),
    ('[[w.card|x]], 5', ('card', 'w.card', '5', None)),
]
NOTE_PARTS = [
    ('[[w.a]], 12. To check: [[w.b]]. Names: Rusk.', (['[[w.a]], 12'], ['To check: [[w.b]].', 'Names: Rusk.'])),
    ('[FRUS](https://h.s.g/d1); [[w.a]], 3 (the vote). See [[cal.x]]. Names: A, B.', (['[FRUS](https://h.s.g/d1)', '[[w.a]], 3 (the vote)'], ['See [[cal.x]].', 'Names: A, B.'])),
    ('Made public: FRUS (1997). [[w.a]], 4. Check: the date.', (['[[w.a]], 4'], ['Made public: FRUS (1997).', 'Check: the date.'])),
    ('Pub. L. 87-1, 75 Stat. 1. [[w.a]], 9.', (['Pub. L. 87-1, 75 Stat. 1', '[[w.a]], 9'], [])),
    ('', ([], [])),
    (None, ([], [])),
]
CHASH = [
    ('', 'da39a3ee'),
    (None, 'da39a3ee'),
    ('Kennedy met Rusk.', 'a8329e99'),
    ('Đà Nẵng', 'fff4a50e'),
]


@pytest.mark.parametrize("c,want", UNITS)
def test_units(c, want):
    assert claims.units(c) == want


@pytest.mark.parametrize("row,want", PARSE_ROW)
def test_parse_row(row, want):
    assert claims.parse_row(row) == want


@pytest.mark.parametrize("spec,n,want", PARSE_UNITS)
def test_parse_units(spec, n, want):
    assert claims.parse_units(spec, n) == want


@pytest.mark.parametrize("item,want", ITEM_KEY)
def test_item_key(item, want):
    assert claims.item_key(item) == want


@pytest.mark.parametrize("n,want", NOTE_PARTS)
def test_note_parts(n, want):
    assert claims.note_parts(n) == want


@pytest.mark.parametrize("c,want", CHASH)
def test_chash(c, want):
    assert claims.chash(c) == want


@pytest.mark.xfail(reason="claims.LINK stops a URL at its first ')': a UN resolution's address, "
                          ".../S/RES/232(1966), is read as .../S/RES/232(1966 (code review B.2; 35 such links)",
                   strict=False)
def test_item_key_url_with_parentheses():
    assert claims.item_key("[UN Res. 232](https://undocs.org/S/RES/232(1966))") == \
        ("url", "https://undocs.org/S/RES/232(1966)")
