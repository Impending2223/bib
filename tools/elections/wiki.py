"""Parse Wikipedia's House and Senate election tables (wikitext) into races.

House: one race per district row group: incumbents (with the district they were redistricted
from), their party and the result line, and the candidates with party and percentage.
"""
import re

STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
          "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
          "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
          "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
          "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
          "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
ABBR = dict(zip(STATES, ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
                         "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
                         "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
                         "WI", "WY"]))
ABBR_OF = {v: v for v in ABBR.values()}


def unlink(t):
    t = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"'''?", "", t)
    t = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", t, flags=re.S)
    return t.strip()


def st_of(x):
    x = x.strip()
    return ABBR.get(x) or ABBR_OF.get(x.upper())


def seat_of(tpl):
    """{{ushr|California|17|X}} -> ('CA', 17); AL -> 0."""
    m = re.search(r"\{\{[Uu]shr\|([^|}]+)\|([^|}]+)", tpl)
    if not m:
        return None
    st, d = st_of(m.group(1)), m.group(2).strip()
    return st, (0 if d.upper() in ("AL", "AT-LARGE", "AT LARGE") else int(re.sub(r"\D", "", d) or 0))


def candidates(cell):
    out = []
    found = re.findall(r"^\*(.*)$", cell, re.M)
    if not found and "Party stripe" in cell:    # one candidate, no list: '| nowrap | {{Party stripe|..}}.. (Democratic) Unopposed'
        found = [cell[cell.index("{{Party stripe"):].split("\n")[0]]
    for line in found:
        line = re.sub(r"'{2,}", "", line)
        won = "{{Aye}}" in line or "{{aye}}" in line
        line = re.sub(r"\{\{Party stripe\|[^}]*\}\}|\{\{[Aa]ye\}\}|\{\{[Nn]ay\}\}", "", line)
        line = re.sub(r"\{\{(?:[Dd]agger|[Ee]f|[Rr]efn|[Nn]ote|efn)[^}]*\}\}", "", line)
        line = re.sub(r"\s*\}\}\s*$", "", line)    # the Plainlist's close on its last line
        m = re.match(r"\s*(.*?)\s*\(([^()]*)\)\s*([\d.]+)\s*%?\s*$", unlink(line))
        if m:
            out.append({"name": m.group(1).strip(), "party": m.group(2).strip(), "pct": float(m.group(3)), "won": won})
        else:
            m = re.match(r"\s*(.*?)\s*\(([^()]*)\)\s*(?:Unopposed|unopposed)?\s*$", unlink(line))
            if m:
                out.append({"name": m.group(1).strip(), "party": m.group(2).strip(), "pct": None, "won": won})
    return out


PARTIES = ("Democratic", "Republican", "DFL", "Democratic (DFL)", "Democratic–Farmer–Labor", "Democratic-NPL", "Liberal", "Conservative", "Independent", "Socialist", "Prohibition")


def sections(text):
    """[(heading, body)] at level 2."""
    parts = re.split(r"^==\s*([^=].*?)\s*==\s*$", text, flags=re.M)
    return [(unlink(parts[i]), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def flat_lists(text):
    """A {{collapsible list|title=Others| | a | b }} of minor candidates as bullets, so its rows are not taken
    for table cells."""
    def one(m):
        return "\n" + re.sub(r"\n\|\s*", "\n* ", m.group(1))
    return re.sub(r"\n?\{\{[Cc]ollapsible list\s*\|\s*title=[^|\n]*\|(.*?)\n\}\}", one, text, flags=re.S)


def house(text):
    """[{st, d, special, incumbents:[{name, party, first, result, from}], candidates:[...]}]"""
    out = []
    text = flat_lists(text)
    for head, body in sections(text):
        sp = head.lower().startswith("special")
        if sp or st_of(head):
            for r in house_rows(body):
                r["special"] = sp
                out.append(r)
    return out


def house_rows(text):
    races = []
    for block in re.split(r"\n\|-[^\n]*", text):
        hm = re.search(r"^!\s*(?:rowspan=\"?(\d+)\"?\s*\|)?\s*(\{\{[Uu]shr\|[^}]*\}\})", block, re.M)
        lines = block.strip().split("\n")
        if hm:
            seat = seat_of(hm.group(2))
            if not seat:
                continue
            race = {"st": seat[0], "d": seat[1], "incumbents": [], "candidates": []}
            races.append(race)
        elif races and lines and lines[0].startswith("|") and not lines[0].startswith("|}"):
            race = races[-1]   # another incumbent row of a rowspan
        else:
            continue
        cells = re.split(r"\n\|(?!\})", "\n" + "\n".join(l for l in lines if not l.startswith("!")))
        cells = [c for c in cells if c.strip()]
        if not cells:
            continue
        inc = {"name": unlink(re.sub(r"<br\s*/?>.*", "", re.sub(r"^\s*(?:(?:colspan|rowspan)=\S*\s*\|\s*)+", "", cells[0]), flags=re.S)).strip()}
        rf = re.search(r"[Rr]edistricted from (?:the )?\{\{[Uu]shr\|([^|}]+)\|([^|}]+)", cells[0])
        if rf:
            inc["from"] = f"{st_of(rf.group(1))}-{rf.group(2)}"
        rest = cells[1:]
        for c in rest:
            body = re.sub(r"^(?:\s*(?:rowspan|colspan|nowrap|style)[^|]*\|)+", "", c.strip())
            body = re.sub(r"^\s*\{\{[Pp]arty shading/[^}]*\}\}\s*\|", "", body).strip()
            body = re.sub(r"\{\{[Pp]arty (?:shortname|name)[^|}]*\|([^}|]*)\}\}", lambda m: "DFL" if "Farmer" in m.group(1) else
                          next((p for p in ("Democratic", "Republican", "Liberal", "Conservative", "Independent") if p in m.group(1)), m.group(1)), body)
            if "Plainlist" in c or c.strip().startswith("*") or "{{Party stripe" in c:
                race["candidates"] = candidates(c)
            elif "party" not in inc and unlink(body) in PARTIES:
                inc["party"] = unlink(body)
            elif "first" not in inc and (re.match(r"^(\[\[)?\d{4}", body) or re.search(r"\|\d{4}[^\]]*\]\]", body)):
                inc["first"] = re.sub(r"\s*\{\{[^}]*\}\}", "", unlink(body)).strip()
            elif "result" not in inc and body:
                t = re.sub(r"<br\s*/?>", " ", body)
                inc["result"] = re.sub(r"\s+", " ", unlink(re.sub(r"\{\{[^}]*\}\}", "", t))).strip()
        if inc["name"].lower().startswith("vacant"):
            # a vacancy, under the member who last held it: '[[William E. McVey]] (R) died August 10, 1958.'
            vm = re.search(r"^(.*?)\s*\(([DR])\)\s*(.*?)(?:\.|$)", inc.get("result", ""))
            if vm and vm.group(1):
                races[-1]["incumbents"].append({"name": vm.group(1).strip(), "party": {"D": "Democratic", "R": "Republican"}[vm.group(2)],
                                                "result": vm.group(3).strip() + ".", "vacant": True})
        elif inc["name"] and not inc["name"].lower().startswith(("none", "new seat")):
            races[-1]["incumbents"].append(inc)
        elif "result" in inc:
            races[-1].setdefault("result", inc["result"])
    return races


def sortname(t):
    return re.sub(r"\{\{[Ss]ortname\|([^|}]*)\|([^|}]*)(?:\|[^}]*)?\}\}", r"\1 \2", t)


def senate(text, regular_class):
    """[{st, cl, special, incumbents:[{name, party, result}], candidates:[...]}] from the race summary tables."""
    out = []
    text = flat_lists(text)
    parts = re.split(r"^===\s*(.*?)\s*===\s*$", text, flags=re.M)
    for i in range(1, len(parts) - 1, 2):
        head, body = parts[i].lower(), parts[i + 1]
        if not ("special" in head or "leading to" in head or "next congress" in head):
            continue
        body = body.split("\n|}")[0]
        sp = "special" in head
        for block in re.split(r"\n\|-[^\n]*", body):
            hm = re.search(r"^!\s*(?:(?:rowspan|scope)=\"?\w+\"?\s*\|)?\s*(?:\[\[([^|\]]*)\|)?([A-Z][A-Za-z ]+)(?:<br\s*/?>[^\]]*)?\]?\]?(.*)$", block, re.M)
            if not hm:
                continue
            st = st_of(hm.group(2))
            if not st:
                continue
            cm = re.search(r"Class (\d)", hm.group(0))
            race = {"st": st, "cl": int(cm.group(1)) if cm else regular_class, "special": sp,
                    "incumbents": [], "candidates": []}
            lines = [l for l in block.strip().split("\n") if not l.startswith("!")]
            cells = [c for c in re.split(r"\n\|(?!\})", "\n" + "\n".join(lines)) if c.strip()]
            inc = {"name": unlink(sortname(re.sub(r"<br\s*/?>.*", "", cells[0], flags=re.S))).strip()} if cells else {}
            for c in cells[1:]:
                b = re.sub(r"^(?:\s*(?:rowspan|colspan|nowrap|style|data-sort-value)[^|]*\|)+", "", c.strip())
                b = re.sub(r"^\s*\{\{[Pp]arty shading/[^}]*\}\}\s*\|", "", b).strip()
                b = re.sub(r"\{\{[Ee]fn\|.*?\}\}", "", b, flags=re.S).strip()
                b = re.sub(r"\{\{[Pp]arty (?:shortname|name)[^|}]*\|([^}|]*)\}\}", lambda m: "DFL" if "Farmer" in m.group(1) else
                           next((p for p in ("Democratic", "Republican", "Liberal", "Conservative", "Independent") if p in m.group(1)), m.group(1)), b)
                if "Plainlist" in c or "{{Party stripe" in c:
                    race["candidates"] = candidates(sortname(c))
                elif "party" not in inc and unlink(b) in PARTIES:
                    inc["party"] = unlink(b)
                elif "history" not in inc and re.match(r"^(\[\[)?\d{4}", b):
                    inc["history"] = re.sub(r"\s+", " ", unlink(re.sub(r"\{\{[^}]*\}\}|<br\s*/?>", " ", b))).strip()
                elif "result" not in inc and b:
                    inc["result"] = re.sub(r"\s+", " ", unlink(re.sub(r"\{\{[^}]*\}\}", "", re.sub(r"<br\s*/?>", " ", b)))).strip()
            if inc.get("name") and not re.search(r"admitted|colspan|rowspan|New state", inc["name"]):
                race["incumbents"].append(inc)
            out.append(race)
    return out


def changes(text):
    """A Congress's 'Changes in membership' tables:
    [{ch, st, seat, out, out_party, reason, into, into_party, seated}]; seat is the Senate class or the district (0 at large)."""
    m = re.search(r"^==\s*Changes in membership\s*==\s*$", text, re.M)
    if not m:
        return []
    body = re.split(r"^==[^=]", text[m.end():], maxsplit=1, flags=re.M)[0]
    out = []
    parts = re.split(r"^===\s*(.*?)\s*===\s*$", body, flags=re.M)
    for i in range(1, len(parts) - 1, 2):
        ch = "s" if parts[i].lower().startswith("senate") else "h" if "house" in parts[i].lower() else None
        if not ch:
            continue
        for block in re.split(r"\n\|-[^\n]*", parts[i + 1]):
            cells = [c.strip() for c in re.split(r"\n\s*[|!]\s*(?!\})", "\n" + block.strip()) if c.strip()]
            if len(cells) < 5:
                continue
            first = cells[0]
            if ch == "s":
                m = re.search(r"\|\s*([A-Z][A-Za-z ]+)\]\].*?\((\d)\)", first, re.S)
                if not m:
                    continue
                st, seat = st_of(m.group(1)), int(m.group(2))
            else:
                s = seat_of(first)
                if not s:
                    continue
                st, seat = s
            cells = [re.sub(r"^\s*(?:(?:rowspan|colspan|style|nowrap)\s*=?\s*[^|]*\|\s*)+", "", c).replace("|}", "").strip() for c in cells]

            def person(c):
                c = re.sub(r"\{\{[Pp]arty shading/[^}]*\}\}\s*(?:nowrap\s*)?\|?", "", c)
                c = re.sub(r"^\s*(?:nowrap|style=[^|]*)\s*\|", "", c)
                c = re.sub(r"<br\s*/?>.*", "", c, flags=re.S)
                m = re.match(r"\s*(.*?)\s*\(([A-Z][A-Za-z\-]*)\)\s*$", unlink(sortname(c)))
                if m:
                    return m.group(1), m.group(2)
                v = unlink(sortname(c)).strip()
                return (None, None) if v.lower().startswith(("vacant", "none")) else (v or None, None)
            o, op = person(cells[1])
            n, np_ = person(cells[3])
            reason = re.sub(r"\s+", " ", unlink(re.sub(r"<br\s*/?>", " ", re.sub(r"\{\{[^}]*\}\}", "", cells[2])))).strip()
            seated = re.sub(r"\s+", " ", unlink(re.sub(r"\{\{[^}]*\}\}", "", cells[4]))).strip()
            out.append({"ch": ch, "st": st, "seat": seat, "out": o, "out_party": op, "reason": reason,
                        "into": n, "into_party": np_, "seated": seated})
    return out
