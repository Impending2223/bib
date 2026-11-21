"""A citation shows where a record is, never whether the series holds it (the owner, Nov. 21, 2026)."""
from bib import witnesses


def test_held_clauses_struck():
    cw = witnesses.cite_where
    assert cw("cited by the Wengao; not held") == "cited by the Wengao"
    assert cw("published; not held (no card)") == "published"
    assert cw("named in the text of Mubei (2016 ed.), I, 550; held by the author") == \
        "named in the text of Mubei (2016 ed.), I, 550"
    assert cw("cited by the Mao zedong zhuan (VI, ch. 72 n.11); the manuscript in the Central Archives, not held") == \
        "cited by the Mao zedong zhuan (VI, ch. 72 n.11); the manuscript in the Central Archives"
    assert cw("not held. Perhaps the memorandum of Mar. 11 is meant") == "Perhaps the memorandum of Mar. 11 is meant"
    assert cw("held privately (Faythe Canson)") == ""
    assert cw("not held") == ""


def test_other_where_kept():
    cw = witnesses.cite_where
    s = "NSF, Memos to the President, Bundy, vol. 8, box 2, LBJ Library"
    assert cw(s) == s
    assert cw("RGANI f.5 o.55 d.116; cited by Friedman (2015), 31 n.18") == "RGANI f.5 o.55 d.116; cited by Friedman (2015), 31 n.18"
    assert cw(None) == ""
