"""mdwrap.unwrap: a paragraph and a list item are one line each (tools/bib/mdwrap.py)."""
from bib.mdwrap import unwrap

LONG = "A line that a wrap cut, some eighty characters wide, which runs on to the very edge and"


def test_wrapped_lines_join():
    assert unwrap("One two\nthree.\n\n- item one\n  goes on\n- item two") == "One two three.\n\n- item one goes on\n- item two"
    assert unwrap(LONG + "\nthen ends.", careful=True) == LONG + " then ends."
    assert unwrap("- " + LONG + "\n  then ends.", careful=True) == "- " + LONG + " then ends."


def test_careful_a_line_under_a_list_item_that_is_not_indented_is_its_own_paragraph():
    text = "- " + LONG + "\nA paragraph that follows the list."
    assert unwrap(text, careful=True) == text


def test_careful_a_line_opening_with_two_dashes_is_not_joined():
    text = "(Nov. 24) " + LONG + "\n-- a nested point\n-- another"
    assert unwrap(text, careful=True) == text


def test_careful_two_paragraphs_set_one_under_the_other_stay_two():
    text = "Please do build the missing name tag check and run the sweep.\nTwo issues with this entry.\n" + "x" * 300 + "\nNext."
    assert unwrap(text, careful=True) == text


def test_careful_an_item_numbered_with_a_letter_is_an_item():
    text = "4. " + LONG + "\n4a. **Batch 15b.** Merged.\n   10a. another"
    assert unwrap(text, careful=True) == text


def test_unwrapped_text_is_left_alone():
    text = "# Head\n\nA paragraph a line.\n\n- one\n- two\n\n| a | b |\n|---|---|\n\n> quoted\n> lines"
    assert unwrap(text) == text and unwrap(text, careful=True) == text
