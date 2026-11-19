"""The live bugs of the code review of Nov. 19, 2026 (notes/proposals/code-review-2026-11.md, cluster 2): one test, or
a few, for each fix."""
import os
import re
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


# ---------------------------------------------------------------- 2. a link whose address holds (...)

UN = "[S.C. Res. 232](https://undocs.org/S/RES/232(1966)) (Dec. 16, 1966)."
UN_URL = "https://undocs.org/S/RES/232(1966)"


def test_one_link_pattern_reads_the_whole_address():
    from tools.bib import calaudit, claims, dayorder, markup, resultform, standing, statements, vis, works
    assert [m.group(2) for m in markup.LINK_RE.finditer(UN)] == [UN_URL]
    assert claims.LINK is markup.LINK_RE and vis.LINK is markup.LINK_RE
    assert claims.LINK.findall(UN) == [("S.C. Res. 232", UN_URL)]
    assert claims.item_key(UN) == ("url", UN_URL)
    assert standing._inline(UN) == f'<a href="{UN_URL}">S.C. Res. 232</a> (Dec. 16, 1966).'
    assert statements.plain(UN) == "S.C. Res. 232 (Dec. 16, 1966)."
    assert markup.strip_links(UN) == "S.C. Res. 232 (Dec. 16, 1966)."
    assert works.bluebook_pin("*Title*, [online](" + UN_URL + ")", "12") == ", 12"
    blank = resultform.clean(UN)
    assert UN_URL not in blank and "1966)) " not in blank and blank.endswith("(Dec. 16, 1966).")
    assert "S/RES" not in resultform.clean("see (" + UN_URL + ") here")
    assert re.findall(r"\[((?:[^\[\]]|\[[^\]]*\])*)\]\((" + markup.URL + r")\)", UN) == [("S.C. Res. 232", UN_URL)]
    assert calaudit.markup is markup


def test_dayorder_plain_strips_a_paren_link():
    from tools.bib import dayorder, store
    assert dayorder.plain_c({"c": UN}) == store.fold("S.C. Res. 232 (Dec. 16, 1966).")


def test_plain_links_unchanged():
    from tools.bib import claims, markup
    t = "[FRUS 1961–63, IV, doc. 34](https://history.state.gov/historicaldocuments/frus1961-63v04/d34). [a](http://x.org/b)"
    assert claims.LINK.findall(t) == [("FRUS 1961–63, IV, doc. 34",
                                       "https://history.state.gov/historicaldocuments/frus1961-63v04/d34"),
                                      ("a", "http://x.org/b")]
    assert markup.strip_links(t) == "FRUS 1961–63, IV, doc. 34. a"


# ---------------------------------------------------------------- 3. content left out of the build, counted

def test_committees_month_that_fails_is_counted(tmp_path, monkeypatch):
    from tools.bib import committees, faults
    faults.reset()
    (tmp_path / "1961-01.yaml").write_text("docs:\n  - {date: '1961-01-03', x: 1}\n", encoding="utf-8")
    (tmp_path / "1961-02.yaml").write_bytes(b"docs: \xff\xfe\n")          # not UTF-8: the load raises
    monkeypatch.setattr(committees, "DIR", str(tmp_path))
    monkeypatch.setattr(committees, "_cache", {})
    by = committees.load()
    assert list(by) == ["1961-01-03"]
    assert len(faults.FAULTS) == 1 and "1961-02.yaml" in faults.FAULTS[0][0]
    assert "1 build fault" in faults.report()
    faults.reset()


def test_vis_pass_that_fails_is_counted(monkeypatch):
    from tools.bib import faults, vis
    faults.reset()

    def boom(series):
        raise ValueError("no")
    monkeypatch.setattr(vis, "_problems", boom)
    assert vis.problems(None) == [("tools/bib/vis.py", "the visibility pass failed: ValueError: no")]
    assert faults.FAULTS == [("tools/bib/vis.py", "the visibility pass failed: ValueError: no")]
    faults.reset()
