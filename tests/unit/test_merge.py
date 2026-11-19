"""merge.py: three_way's branches and merge_entry_lists.

Generated once from the code's behaviour on Nov. 19, 2026 (tests/README.md): each row pins what the function returned
then. A row that fails is a change of behaviour: a regression, or a fix to be read and the row rewritten with it.
"""
import pytest

from bib import merge

THREE_WAY = [
    ('same both', {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}),
    ('only theirs changed', {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'theirs', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'theirs', 'n': 'N', 'tags': ['a']}),
    ('only ours changed', {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'ours', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'ours', 'n': 'N', 'tags': ['a']}),
    ('both changed alike', {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'x', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'x', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'x', 'n': 'N', 'tags': ['a']}),
    ('both changed apart', {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'ours', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'theirs', 'n': 'N', 'tags': ['a']}, {'id': 'e',
 'c': 'ours',
 'n': 'N',
 'tags': ['a'],
 'conflict': [{'field': 'c', 'ours': 'ours', 'theirs': 'theirs', 'base': 'base', 'from': 'p'}]}),
    ('no base, theirs adds', None, {'id': 'e', 'c': 'x'}, {'id': 'e', 'c': 'x', 'r': 'R'}, {'id': 'e', 'c': 'x', 'r': 'R'}),
    ('no base, ours adds', None, {'id': 'e', 'c': 'x', 'r': 'R'}, {'id': 'e', 'c': 'x'}, {'id': 'e', 'c': 'x', 'r': 'R'}),
    ('no base, differ', None, {'id': 'e', 'c': 'x'}, {'id': 'e', 'c': 'y'}, {'id': 'e', 'c': 'x', 'conflict': [{'field': 'c', 'ours': 'x', 'theirs': 'y', 'base': None, 'from': 'p'}]}),
    ('theirs removes', {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'tags': ['a']}),
    ('tags union', {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a', 'b']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a', 'c']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a', 'b', 'c']}),
    ('tags removed by theirs', {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': []}, {'id': 'e', 'c': 'base', 'n': 'N'}),
    ('conflicts carried', {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a'], 'conflict': [{'field': 'n', 'from': 'p'}]}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a'], 'conflict': [{'field': 'n', 'from': 'p'}]}),
    ('unknown field', {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a']}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a'], 'zz': 1}, {'id': 'e', 'c': 'base', 'n': 'N', 'tags': ['a'], 'zz': 2}, {'id': 'e',
 'c': 'base',
 'n': 'N',
 'tags': ['a'],
 'conflict': [{'field': 'zz', 'ours': 1, 'theirs': 2, 'base': None, 'from': 'p'},
              {'field': 'zz', 'ours': 1, 'theirs': 2, 'base': None, 'from': 'p'}],
 'zz': 1}),
]
ENTRY_LISTS = [
    ('theirs adds after', [{'id': 'a'}, {'id': 'b'}], [{'id': 'a'}, {'id': 'b'}], [{'id': 'a'}, {'id': 't'}, {'id': 'b'}], [{'id': 'a'}, {'id': 't'}, {'id': 'b'}]),
    ('ours deletes unchanged', [{'id': 'a'}, {'id': 'b'}], [{'id': 'a'}], [{'id': 'a'}, {'id': 'b'}], [{'id': 'a'}]),
    ('theirs deletes changed', [{'id': 'a', 'c': '1'}], [{'id': 'a', 'c': '2'}], [], [{'id': 'a', 'c': '2', 'conflict': [{'kind': 'deleted-by-theirs', 'from': 'p'}]}]),
    ('ours deletes, theirs changed', [{'id': 'a', 'c': '1'}], [], [{'id': 'a', 'c': '2'}], [{'id': 'a', 'c': '2', 'conflict': [{'kind': 'deleted-by-ours', 'from': 'p'}]}]),
    ('both add', [], [{'id': 'o'}], [{'id': 't'}], [{'id': 't'}, {'id': 'o'}]),
]


@pytest.mark.parametrize("name,base,ours,theirs,want", THREE_WAY)
def test_three_way(name, base, ours, theirs, want):
    assert merge.three_way(base, ours, theirs, "p") == want


@pytest.mark.parametrize("name,base,ours,theirs,want", ENTRY_LISTS)
def test_merge_entry_lists(name, base, ours, theirs, want):
    assert merge.merge_entry_lists(base, ours, theirs, "p") == want
