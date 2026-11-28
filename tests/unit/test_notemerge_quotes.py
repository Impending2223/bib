"""notemerge._sentences: no sentence ends inside a quotation the note closes later (the owner, Nov. 27, 2026: a To check
cut in two at its ellipsis, its second half printed among the works read)."""
from bib import notemerge


def test_ellipsis_inside_a_quotation():
    n = ('A, 3. To check: "Houston Bank Merger ... Reasons against," as dictated by Dick Maguire, WHCF (cited by B, 524). '
         'Names: Johnson.')
    assert notemerge.sentences(n) == ['A, 3.', 'To check: "Houston Bank Merger ... Reasons against," as dictated by Dick '
                                      'Maguire, WHCF (cited by B, 524).', 'Names: Johnson.']


def test_abbreviation_inside_a_headline():
    n = '"Gov. Davis Is Firm," Times, July 6, 1960. Names: Davis.'
    assert notemerge.sentences(n) == ['"Gov. Davis Is Firm," Times, July 6, 1960.', 'Names: Davis.']


def test_an_unclosed_quotation_still_splits():
    n = 'He said "we go. Then: Names: X.'
    assert len(notemerge.sentences(n)) == 2
