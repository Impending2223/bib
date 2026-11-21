"""footnotes.py and claims.py, the owner's notes of Nov. 21, 2026 on two entries' footnotes (Oct. 1 and Oct. 2, 1963)
and on the unread records ("I don't want to drop the unread works. Can you check and fix the doubles instead?").

Each row pins a fix: a label's item stands for the first unit; a note's item that is only a pinpoint stays with its
cite; a pointer to a themed list is no source; the line's own links in their citation forms; a label's items a
sentence of their own; the shared sources; the unread records joined to "To check:" without doubles.
"""
import pytest

from bib import claims, footnotes, notemerge

DD = "The Senate sat from noon to 7:02 p.m.: [Daily Digest, D468](https://www.govinfo.gov/x.pdf#page=466)"
C3 = ("Senate extends the Commission one year, [71–15](https://voteview.com/rollcall/RS0880144), as an amendment. "
      "House agrees Oct. 7, [265–80](https://voteview.com/rollcall/RH0880072). Signed Oct. 17, "
      "[77 Stat. 271](https://www.govinfo.gov/content/pkg/STATUTE-77/pdf/STATUTE-77-Pg271-2.pdf).")


# ---------------------------------------------------------------- 1. a label's item: the first unit

LABELS = [
    (DD, "The Senate sat from noon to 7:02 p.m."),
    ("The meetings, recorded: [11 a.m.](https://prde.upress.virginia.edu/conversations/1), JFK Meeting Tape 114_A49.2",
     "The meetings, recorded"),
    ("The Senate sat from noon (its order of June 29) to 5:25 p.m.: [Daily Digest, D322](https://x.gov/a)",
     "The Senate sat from noon (its order of June 29) to 5:25 p.m."),
    ("Votes: [Ala. *Register*, 557](https://archive.org/x)", "Votes"),
    ("FRUS 1961–63, XXIV: [Laos Crisis, doc. 4](https://history.state.gov/x)", None),     # a cite's own colon
    ("Special Message to the Congress: Program for Economic Recovery, [1961 Pub. Papers 41](https://x)", None),
    ("*The Gulf of Tonkin: Hearing*, [pt. 1](https://x)", None),                           # a title's colon
    ("[[w.miller-misalliance]], 300–02", None),
]


@pytest.mark.parametrize("item,want", LABELS)
def test_label_of(item, want):
    assert claims.label_of(item) == want


def test_label_sentence_items_share_the_label():
    n = ("The meetings, recorded: [11 a.m.](https://prde.upress.virginia.edu/conversations/1), Tape 2; "
         "[6:05 p.m.](https://prde.upress.virginia.edu/conversations/2), Tape 4 (PRDE only). [[w.a]], 12.")
    labels = claims.note_labels(n)
    assert set(labels.values()) == {"The meetings, recorded"} and len(labels) == 2


def test_mechanical_label_item_first_unit_only():
    e = {"c": C3, "n": DD + ". To check: [[w.x]]."}
    rows = claims.mechanical(e)["rows"]
    assert rows[0] == "https://www.govinfo.gov/x.pdf#page=466: A"
    assert "https://voteview.com/rollcall/RH0880072: B" in rows


def test_mechanical_label_item_one_unit_is_all():
    e = {"c": "Senate meets.", "n": DD + "."}
    assert claims.mechanical(e)["rows"] == ["https://www.govinfo.gov/x.pdf#page=466: all"]


# ---------------------------------------------------------------- 3. the splitter; the pointer to a themed list

ITEMS = [
    ("FRUS 1961–63, IV, docs. [167](https://h/d167), [169](https://h/d169); doc. [170](https://h/d170)",
     ["FRUS 1961–63, IV, docs. [167](https://h/d167), [169](https://h/d169); doc. [170](https://h/d170)"]),
    ("[[w.a]], 12; pp. 14–15", ["[[w.a]], 12", "pp. 14–15"]),                       # never into a card's cite
    ("FRUS, IV, doc. [127](https://h/d127); [[w.c]], 854–55; doc. [119](https://h/d119) (Nolting)",  # its own cite's
     ["FRUS, IV, doc. [127](https://h/d127); doc. [119](https://h/d119) (Nolting)", "[[w.c]], 854–55"]),
    ("[[w.a]], 12; [[w.b]], 3", ["[[w.a]], 12", "[[w.b]], 3"]),
    ("Docs. 4 and 5; [[w.b]], 3", ["Docs. 4 and 5", "[[w.b]], 3"]),                 # a capital opens a cite
]


@pytest.mark.parametrize("s,want", ITEMS)
def test_items_keep_a_bare_pinpoint_with_its_cite(s, want):
    assert notemerge.items(s) == want


def test_xref_goes_with_the_other_sentences():
    n = "Report of McNamara and Taylor to the President (Viet. II.I.3). [[w.a]], 12. Names: Taylor."
    src, other = claims.note_parts(n)
    assert src == ["[[w.a]], 12"]
    assert other[0] == "Report of McNamara and Taylor to the President (Viet. II.I.3)."
    assert claims.is_xref("Statute (K–J Cong. II.J.2)") and not claims.is_xref("[77 Stat. 56](https://x) (K–J Cong. II.J.2)")


# ---------------------------------------------------------------- 2. the line's own links

class _E(dict):
    pass


@pytest.fixture
def statutes(monkeypatch):
    monkeypatch.setattr(footnotes, "_statutes", lambda series: {("77", "271"): (None, "88-152", None),
                                                               ("75", "47"): ("Area Redevelopment Act", "87-27", "1961")})


def _line(unit, url_part, e=None):
    e = e or {"date": "1963-10-01", "when": "Oct. 1"}
    lk = next(m for m in claims.LINK.finditer(unit) if url_part in m.group(2))
    return footnotes._line(None, e, unit, lk)


def test_line_vote():
    x = _line("Senate extends it, [71–15](https://voteview.com/rollcall/RS0880144), as an amendment.", "voteview")
    assert x["text"] == "[S. Roll Call No. 144, 88th Cong. (1963)](https://voteview.com/rollcall/RS0880144) (Voteview)"
    x = _line("House agrees Oct. 7, [265–80](https://voteview.com/rollcall/RH0880072).", "voteview")
    assert x["text"].startswith("[H. Roll Call No. 72, 88th Cong. (1963)]")


def test_line_statute_full_and_short(statutes):
    u = "Signed Oct. 17, [77 Stat. 271](https://www.govinfo.gov/content/pkg/STATUTE-77/pdf/STATUTE-77-Pg271-2.pdf)."
    x = _line(u, "STATUTE")
    assert x["full"] == ("Act of Oct. 17, 1963, Pub. L. No. 88-152, "
                         "[77 Stat. 271](https://www.govinfo.gov/content/pkg/STATUTE-77/pdf/STATUTE-77-Pg271-2.pdf)")
    assert x["short"] == "Pub. L. No. 88-152, [77 Stat. at 271](https://www.govinfo.gov/content/pkg/STATUTE-77/pdf/STATUTE-77-Pg271-2.pdf)"
    assert x["stat"] == ("77", "271")


def test_line_statute_named(statutes):
    u = "Area Redevelopment Act signed, [75 Stat. 47](https://www.govinfo.gov/content/pkg/STATUTE-75/pdf/STATUTE-75-Pg47-2.pdf)."
    x = _line(u, "STATUTE", {"date": "1961-05-01", "when": "May 1"})
    assert x["full"].startswith("Area Redevelopment Act, Pub. L. No. 87-27, [75 Stat. 47](") and x["full"].endswith(" (1961)")


def test_line_case():
    u = "*Baker v. Carr*, [369 U.S. 186](https://tile.loc.gov/x.pdf): the Court takes the question."
    assert _line(u, "tile.loc")["text"] == "*Baker v. Carr*, [369 U.S. 186](https://tile.loc.gov/x.pdf) (1963)"
    u = "*Williams v. Wallace*, [240 F. Supp. 100](https://static.case.law/x.pdf) (M.D. Ala. 1965): the plan approved."
    assert _line(u, "case.law")["text"].endswith("(https://static.case.law/x.pdf) (M.D. Ala. 1965)")


# ---------------------------------------------------------------- 3. a label's items, a sentence of their own

def _c(text, key=None, label=None, kind="url"):
    return dict(kind=kind, key=key or text, pin="", paren="", text=text, label=label)


def test_footnote_label_sentence_then_cites():
    cites = [_c("[Daily Digest, D468](https://dd)", label="The Senate sat from noon to 7:02 p.m."),
             _c("[S. Roll Call No. 144, 88th Cong. (1963)](https://vv) (Voteview)", kind="line")]
    got = footnotes._footnote(cites, None, lambda st: True, set())
    assert got == ("The Senate sat from noon to 7:02 p.m.: [Daily Digest, D468](https://dd). "
                   "[S. Roll Call No. 144, 88th Cong. (1963)](https://vv) (Voteview).")


def test_footnote_label_items_joined_under_one_label():
    cites = [_c("[11 a.m.](https://p/1), Tape 2", label="The meetings, recorded"), _c("[[w.a]], 12", kind="card"),
             _c("[6:05 p.m.](https://p/2), Tape 4 (PRDE only)", label="The meetings, recorded")]
    got = footnotes._footnote(cites, None, lambda st: True, set())
    assert got == ("The meetings, recorded: [11 a.m.](https://p/1), Tape 2; [6:05 p.m.](https://p/2), Tape 4 (PRDE only). "
                   "[[w.a]], 12.")


def test_footnote_statute_full_once_then_short():
    st = dict(kind="line", key="stat:77:271", pin="", paren="", text="F", full="F", short="S", stat=("77", "271"))
    printed = set()
    assert footnotes._footnote([st], None, lambda s: True, printed) == "F."
    assert footnotes._footnote([st], None, lambda s: True, printed) == "S."
    assert footnotes._footnote([dict(st)], None, lambda s: False, set()) == "S."


# ---------------------------------------------------------------- 5. the shared sources

def _runs(*lists):
    return [[None, i, [_c(t, kind="card") for t in ts]] for i, ts in enumerate(lists)]


def test_shared_block_where_three_under_every_mark():
    runs = _runs(["a", "b", "c", "d"], ["a", "b", "c", "e"])
    assert footnotes.shared(runs, "block", 3) is None
    assert footnotes.shared(runs, None, 3) is runs
    assert footnotes.shared(_runs(["a", "b", "d"], ["a", "b", "e"]), "block", 3) is not None


def test_shared_first():
    out = footnotes.shared(_runs(["a", "b", "c", "d"], ["a", "b", "c", "e"]), "first", 3)
    assert [x["text"] for x in out[0][2]] == ["a", "b", "c", "d"]
    assert [x["text"] for x in out[1][2]] == ["Sources cited *supra* note 1", "e"]


# ---------------------------------------------------------------- 4 and the unread records: what the note holds

def _cited(n, c=""):
    return footnotes.Cited({"n": n, "c": c})


WORDS = [   # the record's words, the note, held already?
    ('Coffin, William Sloane, Jr, Once to Every Man: A Memoir (1977)',
     "[[w.b]], 644. To check: Coffin, *Once to Every Man* (1977), 238–44 (cited by [[w.b]], 644).", True),
    ("Manatos to O'Brien, May 6, 1964, Legislative Background, Civil Rights Act, 1964 File, Johnson Library",
     "[[w.w]], 176. To check: Manatos to O'Brien, May 6, 1964, Ex Hu2, LBJ Library (cited by [[w.w]], 264).", True),
    ("Manatos to O'Brien, May 7, 1964",
     "[[w.w]], 176. To check: Manatos to O'Brien, May 6, 1964, Ex Hu2, LBJ Library (cited by [[w.w]], 264).", False),
    ("NYT, Aug. 29, 1964, p. 6",
     "[[w.b]], 475. To check: [*New York Times*, Aug. 29, 1964](https://t), at 6 (cited by [[w.b]], 475).", True),
    ("New York Times, Jan. 18, 1968",
     "[[w.b]], 667. To check: [*New York Times*, Jan. 17, 1968](https://t), at 42 (cited by [[w.b]], 667).", False),
    ("Burke Marshall interview (Evan Thomas)", "[[w.thomas]], 147–48. Names: Marshall, Robert Kennedy.", False),
    ("Hoover to RFK, July 14, 1961, House Assassinations Committee Records, National Archives",
     "[[w.t]], 162. To check: Hoover to Robert Kennedy, July 14, 1961, House Assassinations Committee Records (cited by [[w.t]], 162).", True),
]


@pytest.mark.parametrize("what,n,want", WORDS)
def test_cited_words(what, n, want):
    assert _cited(n).words(what) is want


def test_cited_printed_frus_and_papers():
    n = "FRUS 1961–63, IV, docs. [167](https://history.state.gov/historicaldocuments/frus1961-63v04/d167). [1963 Pub. Papers 759](https://g)."
    assert _cited(n).printed({"copies": ["FRUS 1961–63, IV, doc. 167"]})
    assert _cited(n).printed({"copies": ["1963 Pub. Papers 759"]})
    assert not _cited(n).printed({"copies": ["FRUS 1961–63, IV, doc. 168"]})


def test_cited_recorded_by_conversation_number():
    n = "[Johnson and James Rowe, 5:56 p.m.](https://millercenter.org/x), Conversation WH6407-20-4436 (Miller Center)."
    c = _cited(n)
    assert c.recorded({"kind": "recording", "what": "Recording, Johnson and James Rowe, July 30, 1964, 5:56 p.m.",
                       "where": "Tape WH6407.20, Citation #4436"})
    assert not c.recorded({"kind": "recording", "what": "Recording, Johnson and Hubert Humphrey, July 30, 1964, 6:46 p.m.",
                           "where": "Tape WH6407.20, Citation #4441"})


def test_pointed_items_and_records():
    n = "[[w.a]], 207. To check: the instruction, *VKD*, 26:198–203 (cited by [[w.a]], 207 n.11)."
    c = _cited(n)
    recs = [("x.1", "w.a", "207 n.11a", '"Chi thi cua Ban Bi thu, so 99-CT/TW" [the mobilization of women], VKD, instruction'),
            ("x.2", "w.a", "207 n.11b", "Nguyen Thi Thap, Lich su phong trao phu nu Viet nam (Hanoi, 1981), 109")]
    assert c.pointed(recs) == {"x.1"}
    n2 = "[[w.a]], 5. To check: Hu Qiaomu to Mao and its four enclosures (cited at [[w.a]], XVI, 5 n.2a–e)."
    recs2 = [(f"x.{i}", "w.a", f"XVI, 5 n.2{ch}", "a letter") for i, ch in enumerate("abcde")]
    assert _cited(n2).pointed(recs2) == {f"x.{i}" for i in range(5)}


AT = [("257 n.4f", "257 n.4"), ("190 n.27", "190 n.27"), ("611 n.i-cant-buy-this.a", "611"), ("XVI, 77 n.2", "XVI, 77 n.2")]


@pytest.mark.parametrize("at,want", AT)
def test_at(at, want):
    assert footnotes._at(at) == want


@pytest.mark.parametrize("what", ["Int", "Ibid., p. 24", "p. 30", "FRUS, Vol. 4", "bid., p. 166"])
def test_stub(what):
    assert len(what) < 12 or footnotes._STUB.match(what)


JOIN = [
    ("[[w.a]], 12. To check: [[w.b]]. See [[cal.x]]. Names: A.", "[[w.a]], 12. To check: [[w.b]]; NEW. See [[cal.x]]. Names: A."),
    ("[[w.a]], 12. See [[cal.x]]. Names: A.", "[[w.a]], 12. To check: NEW. See [[cal.x]]. Names: A."),
    ("[[w.a]], 12.", "[[w.a]], 12. To check: NEW."),
    ("[[w.a]], 12. Check: the day.", "[[w.a]], 12. To check: NEW. Check: the day."),
]


@pytest.mark.parametrize("n,want", JOIN)
def test_with_unread_joins_to_check(monkeypatch, n, want):
    monkeypatch.setattr(footnotes, "unread", lambda series, e: ([("x.1", "NEW")], []))
    assert footnotes.with_unread(None, {"n": n}, n) == want
