"""places.py: a renamed place's name on a date; a gazetteer row's problems.

Generated once from the code's behaviour on Nov. 19, 2026 (tests/README.md): each row pins what the function returned
then. A row that fails is a change of behaviour: a regression, or a fix to be read and the row rewritten with it.
"""
import pytest

from bib import places

NAME_ON = [
    ({'key': 'cape-canaveral',
 'name': 'Cape Canaveral',
 'zone': 'America/New_York',
 'names': [{'name': 'Cape Kennedy', 'from': '1963-11-29', 'until': '1973-10-09'}]}, '1963-11-28', 'Cape Canaveral'),
    ({'key': 'cape-canaveral',
 'name': 'Cape Canaveral',
 'zone': 'America/New_York',
 'names': [{'name': 'Cape Kennedy', 'from': '1963-11-29', 'until': '1973-10-09'}]}, '1963-11-29', 'Cape Kennedy'),
    ({'key': 'cape-canaveral',
 'name': 'Cape Canaveral',
 'zone': 'America/New_York',
 'names': [{'name': 'Cape Kennedy', 'from': '1963-11-29', 'until': '1973-10-09'}]}, '1968-12-21', 'Cape Kennedy'),
    ({'key': 'cape-canaveral',
 'name': 'Cape Canaveral',
 'zone': 'America/New_York',
 'names': [{'name': 'Cape Kennedy', 'from': '1963-11-29', 'until': '1973-10-09'}]}, '1973-10-09', 'Cape Kennedy'),
    ({'key': 'cape-canaveral',
 'name': 'Cape Canaveral',
 'zone': 'America/New_York',
 'names': [{'name': 'Cape Kennedy', 'from': '1963-11-29', 'until': '1973-10-09'}]}, '1973-10-10', 'Cape Canaveral'),
    ({'key': 'cape-canaveral',
 'name': 'Cape Canaveral',
 'zone': 'America/New_York',
 'names': [{'name': 'Cape Kennedy', 'from': '1963-11-29', 'until': '1973-10-09'}]}, None, 'Cape Canaveral'),
    ({'key': 'cape-canaveral',
 'name': 'Cape Canaveral',
 'zone': 'America/New_York',
 'names': [{'name': 'Cape Kennedy', 'from': '1963-11-29', 'until': '1973-10-09'}]}, '1963-11', 'Cape Canaveral'),
    ({'key': 'leopoldville',
 'name': 'Léopoldville',
 'zone': 'Africa/Kinshasa',
 'names': [{'name': 'Kinshasa', 'from': '1966-05-02'}]}, '1966-05-01', 'Léopoldville'),
    ({'key': 'leopoldville',
 'name': 'Léopoldville',
 'zone': 'Africa/Kinshasa',
 'names': [{'name': 'Kinshasa', 'from': '1966-05-02'}]}, '1966-05-02', 'Kinshasa'),
    ({'key': 'leopoldville',
 'name': 'Léopoldville',
 'zone': 'Africa/Kinshasa',
 'names': [{'name': 'Kinshasa', 'from': '1966-05-02'}]}, '1974-01-01', 'Kinshasa'),
    ({'key': 'x', 'name': 'X'}, '1961-01-01', 'X'),
]
ROW_PROBLEMS = [
    ({'key': 'ok-place', 'name': 'OK', 'zone': 'America/New_York'}, []),
    ({'key': 'Bad Key', 'name': 'B', 'zone': 'UTC'}, ["key 'Bad Key': lowercase words and hyphens"]),
    ({'key': 'nozone', 'name': 'N'}, ['nozone: zone None is no zone the zone database knows']),
    ({'key': 'badzone', 'name': 'Z', 'zone': 'Mars/Base'}, ["badzone: zone 'Mars/Base' is no zone the zone database knows"]),
    ({'key': 'noname', 'zone': 'UTC'}, ['noname: no name']),
    ({}, ['key None: lowercase words and hyphens', 'None: no name', 'None: zone None is no zone the zone database knows']),
    ({'key': 'a--b', 'name': 'A', 'zone': 'UTC'}, ["key 'a--b': lowercase words and hyphens"]),
]


@pytest.mark.parametrize("row,date,want", NAME_ON)
def test_name_on(row, date, want):
    """A place renamed in the span: its name on the entry's date (places STYLE 5)."""
    assert places.name_on(row, date) == want


@pytest.mark.parametrize("row,want", ROW_PROBLEMS)
def test_row_problems(row, want):
    assert places.row_problems(row) == want
