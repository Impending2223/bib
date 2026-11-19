"""resultform.py: election results against the house form.

Generated once from the code's behaviour on Nov. 19, 2026 (tests/README.md): each row pins what the function returned
then. A row that fails is a change of behaviour: a regression, or a fix to be read and the row rewritten with it.
"""
import pytest

from bib import resultform

SCAN = [
    ('Smith (D) over Jones (R), 1,000 to 900, 52.6 percent.', True, False, []),
    ('Smith (D) over Jones (R), 1,000 to 900, 50.0 percent.', True, False, []),
    ('Smith won with 52 percent.', True, False, [('no-count', '52 percent', 'a share without its counts: W to L, p percent')]),
    ('Smith won 1,234,567 votes.', True, False, []),
    ('Smith won 1,234,567 votes. Check: the count.', True, True, []),
    ('The bill passed, 300 to 100.', False, False, []),
    ('Yes, 1,234; no 2,345.', True, False, [('yes-no', 'Yes, 1', 'yes and no: "Proposition 1 carries, Y to N, p percent"'),
 ('yes-no', 'no 2,345', 'yes and no: "Proposition 1 carries, Y to N, p percent"')]),
    ('by 5,000 votes', True, False, [('by-votes', 'by 5,000 votes', 'a margin: "W to L, p percent, a N-vote margin"')]),
    ('"52 percent" he said', True, False, []),
    ('[x](https://a.b/52.6 percent)', True, False, []),
    ('', False, False, []),
]
SENTENCE_START = [
    ('One. Two three.', 10, 5),
    ('Gov. Smith won. Next.', 10, 0),
    ('A: b c', 5, 3),
    ('J. F. K. won', 10, 0),
    ('x', 0, 0),
]


@pytest.mark.parametrize("text,election,checked,want", SCAN)
def test_scan(text, election, checked, want):
    assert resultform.scan(text, election, checked) == want


@pytest.mark.parametrize("text,i,want", SENTENCE_START)
def test_sentence_start(text, i, want):
    assert resultform.sentence_start(text, i) == want


def test_clean_blanks_links_and_quotes():
    t = 'a [x](https://y.z) "q" b'
    assert resultform.clean(t) == "a [x" + " " * len("](https://y.z)") + " " + " " * 3 + " b"
