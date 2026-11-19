"""The live bugs of the code review of Nov. 19, 2026 (notes/proposals/code-review-2026-11.md, cluster 2): one test, or
a few, for each fix."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from tools.bib import addops, claims, notemerge  # noqa: E402


# ---------------------------------------------------------------- 1. the note's sentences after an abbreviation

def test_opener_after_abbreviation_starts_a_sentence():
    n = "S. 3361, 87th Cong. To check: [[w.a]]. Names: Kennedy."
    assert notemerge.sentences(n) == ["S. 3361, 87th Cong.", "To check: [[w.a]].", "Names: Kennedy."]
    for abbr in ("Cong.", "Sess.", "B.", "n.", "Rep."):
        for opener in ("To check: [[w.a]].", "Check: the day.", "Names: Rusk.", "See [[cal.1961-01-20.x]].",
                       "Made public: 1975.", "Reply: [[cal.1961-01-21.x]].", "The order: x.", "Bibliography: x."):
            n = f"H.R. 1, 87th {abbr} {opener}"
            assert notemerge.sentences(n) == [f"H.R. 1, 87th {abbr}", opener], n


def test_abbreviation_still_holds_inside_a_sentence():
    assert notemerge.sentences("106 Cong. Rec. 13,819 (1960). Names: X.") == ["106 Cong. Rec. 13,819 (1960).",
                                                                          "Names: X."]
    assert notemerge.sentences("[[w.x]], 258 n. Kotz says so.") == ["[[w.x]], 258 n. Kotz says so."]


def test_to_check_joins_the_existing_run():
    e = {"id": "cal.1962-10-24.x", "c": "A bill.", "n": "S. 3361, 87th Cong. To check: [[w.a]]. Names: X."}
    new, err = addops.to_check(e, {"add": ["[[w.b]]"]})
    assert err is None
    assert new["n"] == "S. 3361, 87th Cong. To check: [[w.a]]; [[w.b]]. Names: X."
    assert new["n"].count("To check:") == 1
    again, _ = addops.to_check(new, {"add": ["[[w.b]]"]})
    assert again["n"] == new["n"]


def test_claims_reads_made_public_after_an_abbreviation_as_no_source():
    src, other = claims.note_parts("[[w.k]], 320 n. Made public: Check; Kotz cites the taps. Names: King.")
    assert src == ["[[w.k]], 320 n"]
    assert other == ["Made public: Check; Kotz cites the taps.", "Names: King."]
