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


# claims.py, STYLE 9: a row that names parts by number gives each unit the sources its letters gave.
def _entry(c, rows, **kw):
    from bib import claims
    e = store.normalize_entry(dict({'id': 'cal.1961-03-10.berlin', 'date': '1961-03-10', 'c': c,
                                    'n': '[[w.frus]], 12. [[w.beschloss]], 123.'}, **kw))
    e['src'] = {'c': claims.chash(e['c']), 'rows': rows}
    return e


def _per_unit(e):
    from bib import claims
    us = claims.units(e['c'])
    rows = claims.resolve(e)
    return [sorted(key for r, k, key, pin, note, u, item in rows if u not in (None, '?') and claims.LETTERS[i] in u)
            for i in range(len(us))]


THREE = 'Rusk sees Dobrynin. The talks will resume on Monday; Moscow will send Zorin.'
THREE_CUT = 'Rusk sees Dobrynin. The talks will resume on Monday;{1} Moscow will send Zorin.{2}'


def test_numbers_resolve_as_the_letters_did():
    old = _entry(THREE, ['w.frus 12: all', 'w.beschloss 123: C'])
    new = _entry(THREE_CUT, ['w.frus 12: 1, 2', 'w.beschloss 123: 2'])
    assert _per_unit(old) == _per_unit(new) == [['w.frus'], ['w.frus'], ['w.beschloss', 'w.frus']]


def test_a_number_that_was_cut_resolves_to_its_halves():
    e = _entry('Rusk sees Dobrynin.{3} The talks will resume on Monday;{4} Moscow will send Zorin.{2}',
               ['w.frus 12: 1', 'w.beschloss 123: 2'], cut_from={'3': '1', '4': '1'})
    assert _per_unit(e) == [['w.frus'], ['w.frus'], ['w.beschloss']]


def test_a_field_gives_no_unit_a_source():
    from bib import claims
    e = _entry(THREE_CUT, ['w.frus 12: 1, 2', 'w.beschloss 123: time'], time='15:00')
    assert _per_unit(e) == [['w.frus'], ['w.frus'], ['w.frus']]
    assert [u for *_, u, _ in claims.resolve(e)][1] == {'time'}
    del e['time']
    assert [u for *_, u, _ in claims.resolve(e)][1] is None          # the entry has no hour: an error for check


def test_a_number_the_line_lacks_does_not_resolve():
    from bib import claims
    e = _entry(THREE_CUT, ['w.frus 12: 9'])
    assert claims.resolve(e)[0][5] is None


# Step 6: a visibility ruling, a variant and the variant op name parts by number, or a field.
def test_a_ruling_names_parts_by_number():
    from bib import vis
    e = _entry(THREE_CUT, ['w.frus 12: 1, 2'], tags=['vis:only:ussr@2', 'vis:only:prc@1.2'])
    got = {tuple(sorted(r['pols'])): r['units'] for r in vis.rulings(e)}
    assert got == {('ussr',): {'C'}, ('prc',): {'A', 'B', 'C'}}
    old = _entry(THREE, ['w.frus 12: all'], tags=['vis:only:ussr@C'])
    assert vis.rulings(old)[0]['units'] == {'C'}
    assert vis.rulings(_entry(THREE_CUT, [], tags=['vis:only:ussr@9'])) == []      # no such part: no ruling


def test_named_letters():
    from bib import claims
    e = _entry(THREE_CUT, [])
    assert claims.named_letters(e, '1') == {'A', 'B'}
    assert claims.named_letters(e, 'C') == {'C'}
    assert claims.named_letters(e, 'D') is None and claims.named_letters(e, '7') is None


def test_the_variant_op_takes_a_field():
    from bib import addops
    e = _entry(THREE_CUT, [], time='15:00')
    new, err = addops.variant(e, {'field': 'time', 'value': '14:00', 'witness': 'w.peng', 'reads': 'at 2 p.m.', 'at': 'IV, 37'})
    assert err is None and new['variants'] == [{'field': 'time', 'value': '14:00', 'witness': 'w.peng', 'reads': 'at 2 p.m.', 'at': 'IV, 37'}]
    assert addops.variant(e, {'field': 'time', 'witness': 'w.peng', 'reads': 'x'})[1]
    assert addops.lettered('variant', {'unit': 'C'}) == 'C'
    assert addops.lettered('variant', {'unit': '2'}) is None                      # a number needs no base
    assert addops.lettered('cite', {'units': '1, 2'}) is None
    assert addops.lettered('src', {'rows': ['w.frus 12: 2', 'w.frus 12: time']}) is None
