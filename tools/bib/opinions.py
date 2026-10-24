"""The opinions of the Attorney General and the Office of Legal Counsel, 1960-69: daybook/opinions.yaml (kept by hand;
its header is the schema), logged in each day's Documents block as a list of their own, "Opinions" (daybook STYLE 12).

The record (notes/proposals/ag-olc-opinions.md, the memo on what the Attorneys General and the Office did by opinion):
  - the Official Opinions of the Attorneys General: vol. 41 (Jan. 1, 1949, to Dec. 31, 1960) for 1960, vol. 42 (Jan. 1,
    1961, to June 30, 1974, with one opinion of Nov. 30, 1960) for the rest; Google's scans on archive.org (item
    op-atty-gen, files 041 and 042), read page by page; every opinion of 1960-69 in them is a row (44);
  - the Supplemental Opinions of the Office of Legal Counsel, vol. 1 (2013), the Office's selection from its files,
    on justice.gov: its opinions of 1961-69 (13) and two of its "other memoranda" (the blockade memorandum of Oct. 19,
    1962, unsigned; the Deputy Attorney General's on Mississippi, July 1, 1964);
  - the legal memoranda of the Attorney General, his deputy and the Office printed in FRUS (the texts the daybook files,
    sources/frus-text/); and, noted apart, the State Department Legal Adviser's on Vietnam (the Bulletin, Mar. 28, 1966);
  - under `known`, opinions another document names (the Public Papers) and no copy read: not shown, each with its Check.

STYLE:
 1. A row a document, in the day's Documents block after FRUS and before the recordings: the signer by surname (in
    full, running order, where the surname is shared: "Robert F. Kennedy", "Ramsey Clark"), linked to his name entry
    where one person fits (lives.person_named), his title as signed on hover; the title as printed, linked to the copy read at its
    first page; the cite in grey ("42 Op. Att'y Gen. 69", the Bluebook's; "1 Op. O.L.C. Supp. 195", the form the
    Office's supplement prints for itself; the FRUS document), the full cite on hover; "to the President" in grey; then
    the holding on its own line, as an abstract (daybook STYLE 5).
 2. The kind on hover of the cite: the Official Opinions; the Office of Legal Counsel; the Department of Justice (a
    Deputy Attorney General's, an Attorney General's informal memorandum); the State Department's Legal Adviser,
    marked "State" after the cite, never as the Office's.
 3. Under the holding, muted, where the record says so: "Released for publication Oct. 26, 1965" (the volume's
    footnote); "Made public: 2013" (the supplement) or the earlier printing the editor names; a note on the signer
    or the date ("Signed by Cox as Solicitor General").
 4. An undated memorandum printed in FRUS is filed under the date of the document that prints it, and says so ("filed
    by the FRUS document that prints it"). The register runs to Dec. 31, 1969, as the owner asked (Oct. 24, 2026); the
    calendar's days end Jan. 20, 1969, so the later rows (four) are in the register and the memo, not on a page.
 5. The calendar: the major opinions are entries of their own, the opinion the primary record; the others that speak
    to an entry are a pointer in its note ("Opinion: 42 Op. Att'y Gen. 229 (1963), to the Secretary of State: ...").
    Both are in the calendar's data (lists/cal/), not here; the memo lists them.

check [opinions]: fails on a duplicate key, a key not of its kind's form, a kind outside the legend, a date outside
1960-69 or not a date, a cite that does not answer its key (volume and page), a row without title, holding, copy or
read, a copy that is not an address; warns on a signer no name entry fits.
"""
import datetime
import html
import os
import re

from . import store

PATH = os.path.join(store.ROOT, "daybook", "opinions.yaml")
KINDS = {"ag": "Official Opinions of the Attorneys General",
         "olc": "Office of Legal Counsel",
         "doj": "Department of Justice",
         "state": "State Department, Legal Adviser"}
KEY = {"ag": re.compile(r"^oag:(\d+)-(\d+)$"), "olc": re.compile(r"^(olc:supp1-\d+|frus:[\w-]+/d\d+)$"),
       "doj": re.compile(r"^(olc:supp1-\d+|frus:[\w-]+/d\d+)$"), "state": re.compile(r"^dsb:\d{4}-\d\d-\d\d-[a-z]+$")}
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
_cache = {}


def esc(t):
    return html.escape(str(t), quote=True)


def load():
    """{'opinions': [row], 'known': [row]} from daybook/opinions.yaml; empty where the file is not there."""
    if "d" not in _cache:
        d = store.load_yaml(PATH) if os.path.exists(PATH) else {}
        _cache["d"] = {"opinions": (d or {}).get("opinions") or [], "known": (d or {}).get("known") or []}
    return _cache["d"]


def by_day():
    if "day" not in _cache:
        out = {}
        for x in load()["opinions"]:
            out.setdefault(str(x.get("date")), []).append(x)
        _cache["day"] = out
    return _cache["day"]


def for_day(iso):
    """The day's opinions, in the register's order."""
    return by_day().get(iso, [])


def day_label(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{MON[d.month - 1]} {d.day}, {d.year}"


def short_cite(x):
    """The cite without its year: '42 Op. Att'y Gen. 69'; the FRUS and Bulletin cites whole."""
    return re.sub(r"\s*\(\d{4}\)$", "", x["cite"])


def signer(by, series=None):
    """'Kennedy, Robert F.' -> 'Katzenbach' by surname; in running order, 'Robert F. Kennedy', where another person
    with a name entry has the surname (Kennedy, Clark, White, Cox), or without the series (STYLE 1)."""
    sur, _, given = [t.strip() for t in by.partition(",")]
    full = f"{given} {sur}".strip()
    if series is None:
        return full
    from . import namelinks, store as st
    return full if len(namelinks.by_surname(series).get(st.fold(sur), [])) > 1 else sur


def line_html(x, series=None):
    """One row (STYLE 1-4)."""
    au = ""
    if x.get("by"):
        au = esc(signer(x["by"], series))
        if series is not None:
            from . import lives, namelinks
            who = lives.person_named(series, x["by"])
            au = namelinks.a(series, who, au) if who else au
        au = f'<span class="au" title="{esc(x.get("by_title", ""))}">{au}</span> '
    title = f'<a href="{esc(x["copy"])}" title="{esc(x.get("read", ""))}">{esc(x["title"])}</a>'
    bits = [f'<span class="src" title="{esc(KINDS[x["kind"]] + ": " + x["cite"])}">{esc(short_cite(x))}</span>']
    if x["kind"] == "state":
        bits.append('<span class="src">State</span>')
    if x.get("to"):
        bits.append(f'<span class="src">to {esc(x["to"])}</span>')
    if x.get("filed") == "frus":
        bits.append('<span class="src">filed by the FRUS document that prints it</span>')
    more = []
    if x.get("released"):
        more.append(f'Released for publication {esc(day_label(str(x["released"])))}.')
    if x.get("made_public"):
        more.append(f'Made public: {esc(x["made_public"])}.')
    if x.get("note"):
        more.append(esc(x["note"]))
    pr = f'<span class="pr">{" ".join(more)}</span>' if more else ""
    return f'<li>{au}{title} {" ".join(bits)}<span class="ab">{esc(x["holding"])}</span>{pr}</li>'


def list_html(rows, series=None):
    return '<ol class="dd fr op">' + "".join(line_html(x, series) for x in rows) + "</ol>"


def problems(series=None):
    """For ./bib check [opinions]: (level, where, message)."""
    out, seen = [], set()
    where = "daybook/opinions.yaml"
    for x in load()["opinions"]:
        k, kind = x.get("key"), x.get("kind")
        if k in seen:
            out.append(("error", where, f"{k}: a second row of this key"))
        seen.add(k)
        if kind not in KINDS:
            out.append(("error", where, f"{k}: kind {kind!r} is not one of {', '.join(KINDS)}"))
            continue
        if not KEY[kind].match(str(k)):
            out.append(("error", where, f"{k}: not a key of kind {kind}"))
        d = str(x.get("date", ""))
        try:
            datetime.date.fromisoformat(d)
            if not ("1960-01-01" <= d <= "1969-12-31"):
                out.append(("error", where, f"{k}: {d} outside 1960-69"))
        except ValueError:
            out.append(("error", where, f"{k}: date {d!r} is not YYYY-MM-DD"))
        for f in ("cite", "title", "holding", "copy", "read"):
            if not x.get(f):
                out.append(("error", where, f"{k}: no {f}"))
        if x.get("copy") and not re.match(r"^https://", str(x["copy"])):
            out.append(("error", where, f"{k}: copy is not an address"))
        m = re.match(r"^oag:(\d+)-(\d+)$", str(k))
        if m and not str(x.get("cite", "")).startswith(f"{m.group(1)} Op. Att'y Gen. {m.group(2)} ({d[:4]})"):
            out.append(("error", where, f"{k}: cite {x.get('cite')!r} does not answer the key and the year"))
        m = re.match(r"^olc:supp1-(\d+)$", str(k))
        if m and not str(x.get("cite", "")).startswith(f"1 Op. O.L.C. Supp. {m.group(1)} ({d[:4]})"):
            out.append(("error", where, f"{k}: cite {x.get('cite')!r} does not answer the key and the year"))
        if x.get("by") and series is not None:
            from . import lives
            if not lives.person_named(series, x["by"]):
                out.append(("warn", where, f"{k}: no name entry fits the signer {x['by']!r}"))
        if x.get("filed") not in (None, "frus"):
            out.append(("error", where, f"{k}: filed {x.get('filed')!r}: only 'frus'"))
    for x in load()["known"]:
        if x.get("kind") != "known" or not x.get("source") or not x.get("check"):
            out.append(("error", where, f"{x.get('key')}: a known opinion needs kind known, a source and a check"))
    return out
