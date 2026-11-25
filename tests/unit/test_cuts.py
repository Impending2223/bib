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


# Step 8: a patch names a part by its words (`on:`), and adds words as a part of their own.
def _note_entry():
    return store.normalize_entry({'id': 'cal.1961-03-10.berlin', 'date': '1961-03-10', 'c': THREE,
                                  'n': '[[w.frus]], 12. To check: [[w.beschloss]].'})


def test_cite_on_cuts_the_line_and_keeps_the_old_source_whole():
    from bib import addops
    new, err = addops.cite(_note_entry(), {'item': '[[w.beschloss]], 123', 'on': 'Moscow will send Zorin.'})
    assert err is None
    assert store.stored_form(new)['c'] == 'Rusk sees Dobrynin. The talks will resume on Monday;{2} Moscow will send Zorin.{3}'
    assert new['src']['rows'] == ['w.frus 12: 2, 3', 'w.beschloss 123: 3'] and new['cut_from'] == {'2': '1', '3': '1'}
    assert _per_unit(new) == [['w.frus'], ['w.frus'], ['w.beschloss', 'w.frus']]


def test_two_parts_named_for_one_source_in_either_order():
    from bib import addops
    a = {'item': '[[w.beschloss]], 123', 'on': 'Moscow will send Zorin.'}
    b = {'item': '[[w.beschloss]], 123', 'on': 'Rusk sees Dobrynin.'}
    x = addops.cite(addops.cite(_note_entry(), a)[0], b)[0]
    y = addops.cite(addops.cite(_note_entry(), b)[0], a)[0]
    assert _per_unit(x) == _per_unit(y) == [['w.beschloss', 'w.frus'], ['w.frus'], ['w.beschloss', 'w.frus']]


def test_words_not_in_the_line_are_an_anchor_refusal():
    from bib import addops
    new, err = addops.cite(_note_entry(), {'item': '[[w.beschloss]], 123', 'on': 'Moscow will send Gromyko.'})
    assert new is None and isinstance(err, addops.Anchor)
    new, err = addops.cite(_note_entry(), {'item': '[[w.beschloss]], 123', 'on': 'will send Zorin.'})
    assert new is None and 'do not begin' in err


def test_add_words_is_a_part_of_its_own_with_its_own_source():
    from bib import addops
    new, err = addops.add_words(_note_entry(), {'after': 'Rusk sees Dobrynin.', 'words': 'Thompson is present.',
                                                'item': '[[w.beschloss]], 124'})
    assert err is None
    assert store.stored_form(new)['c'] == ('Rusk sees Dobrynin.{2} Thompson is present.{4} The talks will resume on Monday; '
                                           'Moscow will send Zorin.{3}')
    assert _per_unit(new) == [['w.frus'], ['w.beschloss'], ['w.frus'], ['w.frus']]
    end, err = addops.add_words(_note_entry(), {'words': 'Thompson is present.', 'item': '[[w.beschloss]], 124'})
    assert err is None and store.stored_form(end)['c'] == THREE + '{1} Thompson is present.{2}'
    assert _per_unit(end) == [['w.frus'], ['w.frus'], ['w.frus'], ['w.beschloss']]


def test_cite_on_a_field_and_no_on_with_cuts():
    from bib import addops
    e = dict(_note_entry(), time='15:00')
    new, err = addops.cite(e, {'item': '[[w.beschloss]], 123', 'on': 'time'})
    assert err is None and new['src']['rows'][-1] == 'w.beschloss 123: time' and 'cuts' not in new
    cut = addops.cite(_note_entry(), {'item': '[[w.beschloss]], 123', 'on': 'Moscow will send Zorin.'})[0]
    more, err = addops.cite(cut, {'item': '[[w.reeves]], 9'})
    assert err is None and more['src']['rows'][-1] == 'w.reeves 9: 2, 3'           # the whole line as it stands


def test_an_edit_without_marks_carries_them():
    from bib import cuts
    c, ks = cuts.strip(THREE_CUT)
    placed, lost = cuts.carry(c, ks, 'Sunday. ' + c)
    assert lost == [] and cuts.insert('Sunday. ' + c, placed) == 'Sunday. Rusk sees Dobrynin. The talks will resume on Monday;{1} Moscow will send Zorin.{2}'
    assert cuts.carry(c, ks, c.replace('Zorin', 'Gromyko'))[1] == ['2']


def test_an_edit_may_settle_a_check_it_names():
    from bib import patchaudit
    cur = '[[w.frus]], 12. Check: the day of the call. Check: the place. Names: Rusk.'
    new = '[[w.frus]], 12. The Papers date it Aug. 26. Names: Rusk.'
    assert len(patchaudit.drops(cur, new)) == 2
    assert patchaudit.drops(cur, new, settles=['Check: the day of the call.']) == ["'Check: the place.'"]
    assert patchaudit.drops(cur, new, settles=['Check: the day', 'Check: the place.']) == []
