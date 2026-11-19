"""notemerge.py: sentences, items, the note's parts and their rendering.

Generated once from the code's behaviour on Nov. 19, 2026 (tests/README.md): each row pins what the function returned
then. A row that fails is a change of behaviour: a regression, or a fix to be read and the row rewritten with it.
"""
import pytest

from bib import notemerge

SENTENCES = [
    ('One. Two.', ['One.', 'Two.']),
    ('[[w.a]], 12. To check: [[w.b]].', ['[[w.a]], 12.', 'To check: [[w.b]].']),
    ('Pub. L. 87-1. Next.', ['Pub. L. 87-1.', 'Next.']),
    ('Signed at 4 p.m. Names: Rusk.', ['Signed at 4 p.m.', 'Names: Rusk.']),
    ('Bundy to Johnson, 4 p.m., NSF. Next.', ['Bundy to Johnson, 4 p.m., NSF.', 'Next.']),
    ('(A. B.) C.', ['(A. B.) C.']),
    ('Apr. 17. The landing.', ['Apr. 17.', 'The landing.']),
    ('87th Cong. To check: [[w.b]].', ['87th Cong. To check: [[w.b]].']),
    ('U.S. Army. Next.', ['U.S. Army.', 'Next.']),
    ('', []),
    ('No stop', ['No stop']),
    ('Ends. *Title* starts.', ['Ends.', '*Title* starts.']),
]
ITEMS = [
    ('a; b; c', ['a', 'b', 'c']),
    ('a (b; c); d', ['a (b; c)', 'd']),
    ('[x; y](u); z', ['[x; y](u)', 'z']),
    ('', []),
    ('one', ['one']),
    ('a;b', ['a', 'b']),
]
PARSE = [
    ('[[w.a]], 12; [[w.b]], 3. To check: [[w.c]]. Names: Rusk, Bundy.', [('works', ['[[w.a]], 12', '[[w.b]], 3']), ('tc', ['[[w.c]]']), ('names', ['Rusk', 'Bundy'])]),
    ('Text first. [[w.a]], 5 (the vote). See [[cal.x]].', [('text', 'Text first.'), ('works', ['[[w.a]], 5 (the vote)']), ('text', 'See [[cal.x]].')]),
    ('Names: A.', [('names', ['A'])]),
]


@pytest.mark.parametrize("n,want", SENTENCES)
def test_sentences(n, want):
    assert notemerge.sentences(n) == want


@pytest.mark.parametrize("s,want", ITEMS)
def test_items(s, want):
    assert notemerge.items(s) == want


@pytest.mark.parametrize("n,want", PARSE)
def test_parse(n, want):
    assert notemerge.parse(n) == want


@pytest.mark.parametrize("n", [p[0] for p in PARSE])
def test_render_parse_round_trip(n):
    assert notemerge.render(notemerge.parse(n)) == n


@pytest.mark.xfail(reason="notemerge.sentences takes 'Cong.' for an abbreviation and runs on into the note's own "
                          "'To check:' sentence (code review B.1: addops.to_check then writes a second 'To check:')",
                   strict=False)
def test_sentence_after_cong():
    assert notemerge.sentences("Pub. L. 87-1, 87th Cong. To check: [[w.b]].") == \
        ["Pub. L. 87-1, 87th Cong.", "To check: [[w.b]]."]
