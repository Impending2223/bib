"""Who in the series is not yet in the Executive Branch roster: ./bib executive names [part3|daybook|cal]

    part3     Part III entries whose role names an executive office (Secretary, Ambassador, Director, ...)
    daybook   the FRUS authors of the daybook who are persons and U.S. officials by their FRUS role
    cal       Part III entries named in the calendar's "Names:" lines

A person counts as placed when a holder in executive/ has the same surname and a compatible given name
(the same first name, or initials that agree). The report is advisory: Part III also holds members of
Congress, journalists and foreign leaders, and the role filter is a heuristic.
"""
import glob
import os
import re

from . import store
from .markup import plain

EXEC = re.compile(r"Secretary|Under Sec|Assistant|Ambassador|Director|Counsel|Special|Press sec|Attorney General|"
                  r"Solicitor|Administrator|Commissioner|Chairman|Chief|General\b|Gen\.|Admiral|Adm\.|aide|staff|"
                  r"adviser|advisor|Representative to|Postmaster|Surgeon|Deputy|Council of Economic|CIA|FBI|"
                  r"Joint Chiefs|White House|Commander|NSC|Budget|Peace Corps|USIA|AID|Treasurer|Comptroller", re.I)
NOT_EXEC = re.compile(r"\bSenator\b|\bRep\.|Representative \(|Representative from|Congressman|Speaker|Governor of (?!the Federal)|"
                      r"Mayor|journalist|columnist|reporter|correspondent|candidate|Prime Minister|Foreign Minister|"
                      r"President of (?!the United States)|King|Premier|Chancellor|Soviet|British|French|German|"
                      r"Vietnamese|Chinese|Cuban|Laotian|Israeli|Egyptian|Indian", re.I)
US = re.compile(r"Department of|Secretary of|Ambassador to|Embassy|Assistant Secretary|Director of|Staff|Special Assistant|"
                r"Joint Chiefs|Commander in Chief|U\.S\.|United States|Defense|Army|Navy|Air Force|Central Intelligence|"
                r"President’s|President's|White House|Bureau|Office of|Agency|Consul|Chargé|Mission|Counselor|"
                r"Under Secretary|Attorney General|Representative to|Coordinator|Policy Planning", re.I)
FOREIGN = re.compile(r"Soviet|USSR|British|French|Prime Minister|Foreign Minister|Minister of|President of (?!the United States)|"
                     r"King of|Chancellor|Premier|Chairman of the (?:Council|Presidium)|Secretary-General|Ambassador (?:of|in the United States)|"
                     r"(?:German|Italian|Indian|Pakistani|Laotian|Cambodian|Vietnamese|Chinese|Japanese|Cuban|Israeli|Egyptian|"
                     r"Iranian|Turkish|Greek|Canadian|Brazilian|Mexican|Argentine|Chilean|Congolese|Belgian|Dutch|Polish|"
                     r"Yugoslav|Korean|Thai|Burmese|Indonesian|Philippine|Australian|Norwegian|Danish|Swedish|Spanish|"
                     r"Portuguese) (?:Ambassador|Foreign|Minister|Prime|President|Chargé|Representative|official|delegate)", re.I)


def placed(units):
    """fold(surname) -> [given names] of every holder."""
    out = {}
    for u in units.values():
        for o in u.get("offices") or []:
            for h in o.get("holders") or []:
                bare = re.sub(r"\s*\([^)]*\)", "", h["name"])
                parts = [p.strip() for p in bare.split(",")]
                out.setdefault(store.fold(parts[0]), []).append(" ".join(filter(None, [parts[1] if len(parts) > 1 else "",
                                                                                         h.get("given") or ""])))
    return out


def compatible(a, b):
    """'McGeorge' ~ 'McGeorge'; 'W. Averell' ~ 'William Averell'; '' ~ anything."""
    wa = [w for w in store.fold(a).replace(".", " ").split() if w]
    wb = [w for w in store.fold(b).replace(".", " ").split() if w]
    if not wa or not wb:
        return True
    for x in wa:
        for y in wb:
            if x == y or (len(x) == 1 and y.startswith(x)) or (len(y) == 1 and x.startswith(y)):
                return True
    return False


def found(P, sur, given):
    return any(compatible(given, g) for g in P.get(store.fold(sur), []))


def part3(series):
    for lst in series.lists.values():
        for sec, e in lst.entries():
            if sec.code.startswith("III") and e.get("s") and "," in e["s"]:
                yield lst, sec, e


def report(series, units, which):
    which = set(which or ["part3", "daybook", "cal"])
    P = placed(units)
    if "part3" in which:
        miss = []
        for lst, sec, e in part3(series):
            r = plain(e.get("r") or "")
            if not EXEC.search(r) or (NOT_EXEC.search(r) and not re.search(r"Secretary|Ambassador to|Director|Attorney General", r)):
                continue
            sur, given = (x.strip() for x in re.sub(r"\s*\([^)]*\)", "", plain(e["s"])).split(",")[:2])
            if not found(P, sur, given):
                miss.append(f"  {lst.abbr} {sec.code:7} {plain(e['s']):34} {r[:90]}")
        print(f"Part III, executive roles not in the roster: {len(miss)}")
        print("\n".join(miss))
    if "daybook" in which:
        from collections import Counter
        cnt = Counter()
        for f in sorted(glob.glob(os.path.join(store.ROOT, "daybook", "*.yaml"))):
            for x in store.load_yaml(f)["docs"]:
                if x["src"] == "frus" and x.get("author"):
                    cnt[x["author"]] += 1
        miss = []
        for a, n in cnt.most_common():
            w = re.sub(r",? (Jr\.|II|III)$", "", a).split()
            if len(w) < 1 or US.search(a) and len(w) > 2 or re.search(r"\b(of|the|and|for|in)\b|\(", a):
                continue   # an office, not a person
            sur, given = w[-1], " ".join(w[:-1])
            if not found(P, sur, given):
                miss.append((a, n))
        print(f"\nDaybook FRUS authors (persons) not in the roster: {len(miss)} (foreign persons among them)")
        for a, n in miss:
            print(f"  {n:4}  {a}")
    if "cal" in which:
        from .build import Linker
        from .congress import Pointers
        linker = Linker(series)
        ptr = Pointers(series, linker)
        seen, miss = set(), []
        for lst in series.lists.values():
            if lst.kind != "calendar":
                continue
            for sec, e in lst.entries():
                for x in ptr.named(lst, e):
                    if x["id"] in seen:
                        continue
                    seen.add(x["id"])
                    r = plain(x.get("r") or "")
                    sur, given = (y.strip() for y in re.sub(r"\s*\([^)]*\)", "", plain(x["s"])).split(",")[:2])
                    if EXEC.search(r) and not found(P, sur, given):
                        miss.append(f"  {plain(x['s']):34} {r[:90]}")
        print(f"\nNamed in the calendar, executive roles, not in the roster: {len(miss)}")
        print("\n".join(miss))
