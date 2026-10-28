"""The records the secondary works cite, and what each is cited for (the owner's rule, Oct. 28, 2026).

    sources/cited-records/<card>.yaml    one file a work (named by its card, `w.` dropped), kept by hand or agent

The owner: the agents to log "the materials and records cited for the claims in the secondary sources they read", and
"identify the ABCD fact, claim, or quotation it sources, along with the entry". A reading agent that cites a work's
page for a calendar entry writes down what that page rests on: each document, recording, interview or file the work's
note gives for it, and which fact, claim or quotation of the entry's `c` it is the work's ground for.

A file is a list of records:

    - record: Bundy to Johnson, Feb. 7, 1965        # as the work cites it: author to recipient, or the title; date
      kind: memorandum                              # KINDS
      date: '1965-02-07'                            # the record's date, as cited: YYYY-MM-DD, YYYY-MM, YYYY, or null
      where: NSF, Memos to the President, Bundy, vol. 8, box 2, LBJ Library   # repository and file, as cited
      cited_by: {page: '251', note: '14'}           # the work's printed page and its note (null for a text citation)
      for:                                          # every entry and claim it is cited for
        - entry: cal.1965-02-07.vietnam
          claim: the reprisal's targets             # the fact, claim or quotation of `c` it grounds (STYLE 2)
      found: FRUS 1964–68, II, doc. 84              # a copy the series can read (FRUS, the Papers, a recording), or null
      read: false                                   # true once read and cited in the entry as its primary record

STYLE
 1. Only what the work's own note gives: no record inferred from the text ("Johnson told Bundy" is not a citation).
    A note citing several records for a paragraph: each record its own row, each tied to the claim it bears where the
    note or the text says which; where it does not, `claim` says "the paragraph: ..." and the row carries `check`.
 2. `claim` names the part of `c` exactly enough to find it: a few of its words ("the vote, 61 to 32"), a quotation's
    opening words in quotation marks, or "the whole entry" where the record grounds all of it. One claim a row of
    `for`; a record grounding two claims of one entry has two rows.
 3. In the entry's note, an unread record joins "To check:" (CLAUDE.md, "Hard and soft") in the work's own form,
    after the works, with the work, page and note it comes from and the claim: "To check: Bundy to Johnson, Feb. 7,
    1965, NSF, LBJ Library (cited by [[w.dallek-flawed-giant]], 251 n.14, for the targets)." Once read (`read: true`), it
    is cited as the primary record, linked, and leaves the To check.
 4. `found`: a copy the series holds or links (the daybook's FRUS document, the Public Papers' item, the Miller
    Center's recording, the Daily Diary's day): the primary-record run reads it and cites it first.
"""
import glob
import os
import re

import yaml

from . import store

DIR = os.path.join(store.ROOT, "sources", "cited-records")
KINDS = {"memorandum", "letter", "telegram", "minutes", "notes", "diary", "recording", "transcript", "interview",
         "oral history", "file", "report", "hearing", "speech", "statement", "press", "manuscript", "other"}
DATE = re.compile(r"^\d{4}(-\d\d(-\d\d)?)?$")


def files():
    return sorted(glob.glob(os.path.join(DIR, "*.yaml")))


def load(path):
    return yaml.safe_load(open(path, encoding="utf-8")) or []


def problems(series):
    """Errors: (where, message)."""
    out = []
    for path in files():
        where = os.path.relpath(path, store.ROOT)
        card = "w." + os.path.basename(path)[:-5]
        if series.works.get(card) is None:
            out.append((where, f"names no card: {card}"))
        try:
            rows = load(path)
        except Exception as x:                  # noqa: BLE001: a file that does not load is the finding
            out.append((where, f"does not load: {x}"))
            continue
        if not isinstance(rows, list):
            out.append((where, "not a list of records"))
            continue
        for i, r in enumerate(rows):
            at = f"{where}[{i}]"
            if not isinstance(r, dict) or not r.get("record"):
                out.append((at, "no record"))
                continue
            if r.get("kind") not in KINDS:
                out.append((at, f"kind {r.get('kind')!r} not in {sorted(KINDS)}"))
            if r.get("date") is not None and not DATE.match(str(r["date"])):
                out.append((at, f"date {r['date']!r}: YYYY-MM-DD, YYYY-MM, YYYY or null"))
            cb = r.get("cited_by") or {}
            if not cb.get("page"):
                out.append((at, "cited_by without the work's page"))
            fors = r.get("for") or []
            if not fors:
                out.append((at, "cited for nothing: `for` names the entries and claims"))
            for f in fors:
                if not isinstance(f, dict) or not f.get("entry") or not f.get("claim"):
                    out.append((at, "each `for` row needs entry and claim (STYLE 2)"))
                elif series.get(f["entry"]) is None:
                    out.append((at, f"no entry {f['entry']}"))
    return out
