"""The register of the States' laws and constitutions (sources/state-law.yaml): its checks.

The register is read by people and sessions, not by the build; its header is the schema. tools/sources/make_listing.py
writes notes/state-law-sources.md from it (tools/sources/law_listing.py), and sources.warnings() says when that is stale.

STYLE
1. Every State and D.C. once, each with a session-laws item (the owner's floor: "all fifty and D.C. at least for the
   session laws' title and an access line").
2. An item: a kind from KINDS, a title, a basis (sources.basis_problems: a ground from the legend and a ref), cited_as
   patterns that compile, online copies each with a url, an access from the legend and a checked date
   (sources.online_problems).
3. Authority: an item gives the law that obliged an officer to make, keep, compile or publish it (`authority`, each
   {law, read | cited_in}) or says what was searched for it (`authority_searched`), or both. A law read names what was
   read; a law cited names where it is cited. "Identified authority is strongly preferred" (the owner): an item with
   neither is an error, so nothing is silently unsourced.
"""
import os

import yaml

from . import store
from .sources import STATES, basis_problems, online_problems

PATH = os.path.join(store.ROOT, "sources", "state-law.yaml")
KINDS = {"session laws", "code", "constitution", "journal", "ag opinions", "other"}
WHERE = "sources/state-law.yaml"


def load():
    return store.load_yaml(PATH) or []


def problems():
    if not os.path.exists(PATH):
        return [(WHERE, "missing")]
    try:
        reg = load()
    except yaml.YAMLError as e:
        return [(WHERE, f"does not load: {e}")]
    out, seen = [], set()
    for e in reg:
        st = e.get("st")
        if st not in STATES:
            out.append((WHERE, f"unknown State {st!r}"))
        if st in seen:
            out.append((WHERE, f"{st} twice"))
        seen.add(st)
        items = e.get("items") or []
        if not any(it.get("kind") == "session laws" for it in items):
            out.append((WHERE, f"{st}: no session-laws item"))
        for i, it in enumerate(items):
            lab = f"{st}-{i + 1}"
            if it.get("kind") not in KINDS:
                out.append((WHERE, f"{lab}: kind {it.get('kind')!r} not in the legend"))
            if not str(it.get("title") or "").strip():
                out.append((WHERE, f"{lab}: no title"))
            out += [(w, f"{lab}: {m}") for w, m in basis_problems(WHERE, it)]
            out += online_problems(lab, it, WHERE)
            auth = it.get("authority") or []
            if not auth and not str(it.get("authority_searched") or "").strip():
                out.append((WHERE, f"{lab}: neither an authority nor what was searched for one"))
            for a in auth:
                if not isinstance(a, dict) or not str(a.get("law") or "").strip():
                    out.append((WHERE, f"{lab}: an authority without its law"))
                elif not (a.get("read") or a.get("cited_in")):
                    out.append((WHERE, f"{lab}: authority {str(a['law'])[:40]!r} says neither where read nor where cited"))
    for st in sorted(STATES - seen):
        out.append((WHERE, f"{st} missing"))
    return out


def online_lines():
    """(st, url, access) of every online copy, for tools/sources/check_access.py --law."""
    out = []
    for e in load():
        for it in e.get("items") or []:
            for o in it.get("online") or []:
                out.append((e["st"], o.get("url"), o.get("access"), o.get("host")))
    return out
