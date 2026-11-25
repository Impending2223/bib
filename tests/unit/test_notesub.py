"""notesub.found: what an entry's citations hold that its line lacks (tools/bib/notesub.py)."""
from bib import notesub


class _S:
    _notesub_names = ({"Chen Yi", "Yi Chen", "Rusk Dean", "Dean Rusk"}, {"Thompson"})


def _e(c, n, tags=()):
    return {"id": "cal.1963-10-01.china", "c": c, "n": n, "tags": list(tags)}


def test_persons_words_and_figures_the_line_lacks():
    e = _e("Peking. The National Day parade; Yang Shangkun attends.",
           '[[w.x]], 12 (Chen Yi and Thompson on the rostrum; "the east wind prevails over the west"; 500,000 march).')
    score, what = notesub.found(_S(), e)
    assert score == 5 and what == ["persons: Chen Yi, Thompson", "words: the east wind prevails over the west", "figures: 500,000"]


def test_what_the_line_has_is_not_counted():
    e = _e("Chen Yi and Thompson on the rostrum; 500,000 march.", "[[w.x]], 12 (Chen Yi and Thompson on the rostrum; 500,000 march).")
    assert notesub.found(_S(), e) == (0, [])


def test_a_title_a_variant_a_date_and_a_page_are_not_substance():
    n = ('[*New York Times*, July 3, 1960](https://x) (James Reston, "Kennedy\'s Reply to Truman Asks Young Leaders," at 1, 189). '
         '[[w.y]], 44 (gives Oct. 20, 1962, and 1,200 men). To check: [[w.z]] (cited by [[w.y]], 44 n.3: Dean Rusk to Thompson, 3,000 words).')
    assert notesub.found(_S(), _e("Kennedy answers Truman.", n)) == (0, [])


def test_an_entry_marked_as_read_is_left():
    e = _e("The parade.", "[[w.x]], 12 (Chen Yi and Thompson on the rostrum).", tags=["ok:note-substance"])
    assert notesub.found(_S(), e) == (0, [])
