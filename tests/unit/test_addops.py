"""addops.py: each additive op's result, and each applied twice equals once.

Generated once from the code's behaviour on Nov. 19, 2026 (tests/README.md): each row pins what the function returned
then. A row that fails is a change of behaviour: a regression, or a fix to be read and the row rewritten with it.
"""
import copy

import pytest

from bib import addops, store

OPS = [
    ('cite from to-check', 'cite', {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, {'item': '[[w.b]], 44'}, {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12; [[w.b]], 44. To check: [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, None),
    ('cite with units', 'cite', {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, {'item': '[[w.d]], 9 (the talk)', 'units': 'B'}, {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12; [[w.d]], 9 (the talk). To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, '
      'Rusk.',
 'src': {'c': '10716227', 'rows': ['w.a 12: all', 'w.d 9: B']},
 'tags': ['name:kennedy-john-f']}, None),
    ('cite again same', 'cite', {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, {'item': '[[w.a]], 12'}, {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, None),
    ('primary', 'primary', {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, {'text': '[FRUS, doc. 1](https://history.state.gov/d1)', 'units': 'A'}, {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[FRUS, doc. 1](https://history.state.gov/d1). [[w.a]], 12. To check: [[w.b]]; [[w.c]]. See '
      '[[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'src': {'c': '10716227', 'rows': ['w.a 12: all', 'https://history.state.gov/d1: A']},
 'tags': ['name:kennedy-john-f']}, None),
    ('to-check new', 'to-check', {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, {'add': ['[[w.e]]', 'Bundy to Johnson, NSF']}, {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]; [[w.e]]; Bundy to Johnson, NSF. See [[cal.1961-03-01.y]]. Names: '
      'Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, None),
    ('to-check cited', 'to-check', {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, {'add': ['[[w.a]]']}, {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, None),
    ('to-check bare string', 'to-check', {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, {'add': '[[w.f]]'}, {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]; [[w.f]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, None),
    ('check', 'check', {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, {'text': 'Check: the date'}, {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. Check: the date. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, None),
    ('names', 'names', {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, {'add': ['Bundy', 'Rusk'], 'tags': ['name:bundy-mcgeorge']}, {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk, Bundy.',
 'tags': ['name:kennedy-john-f', 'name:bundy-mcgeorge']}, None),
    ('also', 'also', {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, {'add': ['laos', 'cuba']}, {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'also': ['laos'],
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, None),
    ('src', 'src', {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, {'rows': ['w.a 12: A']}, {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'src': {'c': '10716227', 'rows': ['w.a 12: all', 'w.a 12: A']},
 'tags': ['name:kennedy-john-f']}, None),
    ('place', 'place', {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, {'at': 'washington', 'basis': 'c'}, {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'place': 'washington',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. To check: [[w.b]]; [[w.c]]. See [[cal.1961-03-01.y]]. Names: Kennedy, Rusk.',
 'tags': ['name:kennedy-john-f']}, None),
    ('check, no To check', 'check', {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12.',
 'tags': ['name:kennedy-john-f']}, {'text': 'Check: who.'}, {'id': 'cal.1961-04-01.x',
 'date': '1961-04-01',
 'thread': 'cuba',
 'c': 'Kennedy met Rusk. They spoke of Laos.',
 'n': '[[w.a]], 12. Check: who.',
 'tags': ['name:kennedy-john-f']}, None),
    ('to-check after Cong.', 'to-check', {'id': 'cal.1961-04-02.x',
 'date': '1961-04-02',
 'thread': 'cuba',
 'c': 'One thing.',
 'n': 'Pub. L. 87-1, 87th Cong. To check: [[w.b]].'}, {'add': ['[[w.z]]']}, {'id': 'cal.1961-04-02.x',
 'date': '1961-04-02',
 'thread': 'cuba',
 'c': 'One thing.',
 'n': 'Pub. L. 87-1, 87th Cong. To check: [[w.b]]. To check: [[w.z]].'}, None),
]


@pytest.mark.parametrize("name,kind,e,body,want,err", OPS)
def test_op(name, kind, e, body, want, err):
    new, got_err = addops.FNS[kind](copy.deepcopy(e), copy.deepcopy(body))
    assert (store.normalize_entry(new) if new else None, got_err) == (want, err)


@pytest.mark.parametrize("name,kind,e,body,want,err", [r for r in OPS if r[0] != "to-check after Cong."])
def test_op_twice_is_once(name, kind, e, body, want, err):
    """An additive op applied twice gives what it gives once (addops: ops commute and repeat safely)."""
    once, _ = addops.FNS[kind](copy.deepcopy(e), copy.deepcopy(body))
    if once is None:
        return
    twice, err2 = addops.FNS[kind](copy.deepcopy(once), copy.deepcopy(body))
    assert err2 is None and store.normalize_entry(twice) == store.normalize_entry(once)


@pytest.mark.xfail(reason="after '87th Cong.' notemerge.sentences misses the note's 'To check:' sentence, so to_check "
                          "writes a second one (code review B.1)", strict=False)
def test_to_check_after_cong_keeps_one_run():
    e = {"id": "x", "c": "C.", "n": "Pub. L. 87-1, 87th Cong. To check: [[w.b]]."}
    new, _ = addops.FNS["to-check"](e, {"add": ["[[w.z]]"]})
    assert new["n"].count("To check:") == 1
