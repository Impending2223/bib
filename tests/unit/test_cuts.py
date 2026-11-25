"""cuts.py: the marks out of a line and back, the parts, the rules (tools/bib/cuts.py)."""
import pytest

from bib import cuts, store

LINE = 'Rusk to Dobrynin: the talks will resume on Monday;{1} Moscow will send Zorin.{2}'
PLAIN = 'Rusk to Dobrynin: the talks will resume on Monday; Moscow will send Zorin.'


def test_strip_and_insert():
    c, ks = cuts.strip(LINE)
    assert c == PLAIN and ks == [[50, '1'], [74, '2']]
    assert cuts.insert(c, ks) == LINE
    assert cuts.strip(PLAIN) == (PLAIN, [])


def test_parts():
    c, ks = cuts.strip(LINE)
    assert cuts.parts(c, ks) == [('1', [0]), ('2', [1])]
    assert cuts.parts(PLAIN, []) == [(None, [0, 1])]
    three = 'A one. B two; C three.'
    assert cuts.parts(three, [[len(three), '7'], [len('A one. B two;'), '4']]) == [('4', [0, 1]), ('7', [2])]


PROBLEMS = [
    (PLAIN, [[50, '1'], [74, '2']], []),
    (PLAIN, [], []),
    (PLAIN, [[50, '1']], ['a line with cuts ends in one']),
    (PLAIN, [[50, '1'], [74, '1']], ["a cut's number used twice"]),
    (PLAIN + ' {x', [], ['a brace in the line that is no cut mark']),
]


@pytest.mark.parametrize("c,ks,want", PROBLEMS)
def test_problems(c, ks, want):
    assert cuts.problems(c, ks) == want


def test_a_cut_inside_a_unit_is_refused():
    assert any("does not follow the end" in m for m in cuts.problems(PLAIN, [[10, '1'], [74, '2']]))
    quoted = 'He said: "One. Two." Then left.'
    assert any("does not follow the end" in m for m in cuts.problems(quoted, [[13, '1'], [len(quoted), '2']]))


def test_next_id_never_reuses():
    assert cuts.next_id({}) == '1'
    assert cuts.next_id({'cuts': [[5, '2'], [9, '6']], 'cut_from': {'5': '3', '6': '3'}}) == '7'


def test_the_store_takes_the_marks_out_and_puts_them_back():
    e = store.normalize_entry({'id': 'cal.1961-03-10.berlin', 'date': '1961-03-10', 'c': LINE})
    assert e['c'] == PLAIN and e['cuts'] == [[50, '1'], [74, '2']]
    out = store.stored_form(e)
    assert out['c'] == LINE and 'cuts' not in out
    plain = store.normalize_entry({'id': 'cal.1961-03-10.berlin', 'date': '1961-03-10', 'c': PLAIN})
    assert 'cuts' not in plain and store.stored_form(plain)['c'] == PLAIN
    assert store.rev(e) != store.rev(plain)                 # the rev is of the stored form, cuts included


def test_only_a_calendar_line_is_read_for_marks():
    e = store.normalize_entry({'id': 'kja.x', 'c': 'A title {1}'})
    assert e['c'] == 'A title {1}' and 'cuts' not in e


def test_a_line_changed_without_its_cuts_is_not_written():
    e = store.normalize_entry({'id': 'cal.1961-03-10.berlin', 'date': '1961-03-10', 'c': LINE})
    e['c'] = 'Sunday. ' + e['c']
    with pytest.raises(ValueError):
        store.stored_form(e)
    cuts.set_line(e, 'Sunday.{3} ' + LINE)
    assert store.stored_form(e)['c'] == 'Sunday.{3} ' + LINE
