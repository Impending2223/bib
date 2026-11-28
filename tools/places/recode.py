"""The nations' tags to short codes, in one pass (ruling 67; notes/proposals/nation-codes.md; place-pages.md, its last
two sections): each polity of sources/polities.yaml takes ISO 3166-1's two-letter code as the standard stood in 1974,
in lower case, but for the short forms the ruling keeps; the old id is kept as an alias, so that an old tag, link or
patch still means the polity (tools/bib/vis.py, `aliases`, `canon`, `tag_canon`).

    python3 -I tools/places/recode.py               dry run: what would change, a count for each file
    python3 -I tools/places/recode.py --apply       write it (refused while a patch waits in inbox/; --force)
    python3 -I tools/places/recode.py --table       the table of codes, as the note to the owner prints it
    --root DIR                                      another tree (a test's)

STYLE
 1. The codes (CODES): the standard's code of 1974 for each polity not kept; the kept ones (KEPT) as they are: the
    short forms the ruling names (`ussr`, `prc`, `uar`, `uk`; `us`, `fr`, `nz` already the standard's), the halves of
    the divided states (`rok`/`dprk`, `rvn`/`drv`, `roc`/`prc`; Germany ruled `de` and `ddr`), the state formed after
    1974 (`srv`), the movements (`nlf`, `pathet-lao`) and the organizations (`un`, `nato`, `oas`, `eec`, `oecd`,
    `imf`). EXTRA: the ids the code and the registry write that have no row in the register (the vis words' Malawi,
    Malta; FRUS's "south-arabia", a state gone before 1974, `fsa`): recoded alike, with no alias (there is no row).
 2. What it rewrites, as text, so that the files keep their comments, order and form:
    sources/polities.yaml: a polity's key (its old id added to `aliases`), its `tag` (the code in capitals), `folded`
    and `then`; the threads' and places' polity lists; the names' `polity` (a thread's slug, a place tag and a name's
    key are never touched); the header's list of the top level.
    lists/**/*.yaml and the fixture's lists: every `polity:` tag and every `vis:only:`, `vis:from:`, `vis:frame:`
    ruling's polities.
    sources/places.yaml (and the fixture's): `in:`, a value, a list or a block list.
    sources/people.yaml: `polity:`. sources/provenance.yaml: a series' `polity` and `privity`, frus_parties' lists,
    the publishers' countries, a work's `country`. sources/witnesses/: `local:`, `circulated:`.
    pages.yaml: a place's plan under a nation's old id, and its parts' names.
    The code's own literals (CODE: TOP, ARCHIVES, LOCAL_NAMES, NATIONS, FOLD, NATION_WORDS, _map's nations, the seeder's
    tables, the self-check's answers) and the tests' registers, assertions and tags (TESTS), each by its place in the
    file's syntax (ast), not by its letters: a thread's slug (`cuba`, `laos`), a map's own country key (`laos` in
    vnmap's borders, read through the aliases) and the nationalities' words (lives.py, NATION_OF) stay.
 3. YAML: Norway's `no` is written quoted ('no') where it is a YAML value or key (bare, YAML reads it as false). In a
    tag (`polity:no`) it needs no quotes.
 4. Idempotent: a second run finds nothing to change (no new code is an old id). A rule whose name, function or
    words the file no longer has, or a literal not written plainly, is reported, and --apply is refused until the
    rule is mended: the file changed under it.
 5. After --apply: `python3 -m pytest -q -m "not slow" --update-goldens` rewrites the goldens whose output lists
    tags (tests/golden/expected/queries/tags.txt sorts them by name); read the diff, then `./bib check`.
"""
import argparse
import ast
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------------- the codes (STYLE 1)

# old id: (new code, the reason). The standard: ISO 3166-1, its first edition (1974), the code of the state as it
# stood then; a name changed within 1960-74 noted, the code the state's throughout (one polity, one code).
TABLE = [
    ("us", "us", "kept: the standard's code"),
    ("ussr", "ussr", "kept: a short form the ruling keeps (the standard's SU)"),
    ("prc", "prc", "kept: a half of a divided state, the short form of its own name (the standard's CN)"),
    ("fr", "fr", "kept: the standard's code"),
    ("frg", "de", "the standard's code, as the owner ruled for the Federal Republic"),
    ("uk", "uk", "kept: a short form the ruling keeps (the standard's GB)"),
    ("gdr", "ddr", "the owner's ruling (the standard's DD)"),
    ("drv", "drv", "kept: a half of a divided state (the standard's VD)"),
    ("srv", "srv", "kept: a state formed in 1976, after the standard of 1974; the series' short form beside drv and rvn"),
    ("rvn", "rvn", "kept: a half of a divided state (the standard's VN)"),
    ("nlf", "nlf", "kept: a movement, not a state"),
    ("roc", "roc", "kept: a half of a divided state (the standard's TW)"),
    ("rok", "rok", "kept: a half of a divided state (the standard's KR)"),
    ("dprk", "dprk", "kept: a half of a divided state (the standard's KP)"),
    ("cuba", "cu", "the standard's code"),
    ("laos", "la", "the standard's code"),
    ("pathet-lao", "pathet-lao", "kept: a movement, not a state"),
    ("cambodia", "kh", "the standard's code (the Khmer Republic from Oct. 1970)"),
    ("uar", "uar", "kept: a short form the ruling keeps (Egypt from Sept. 1971; the standard's EG)"),
    ("un", "un", "kept: an organization"),
    ("nato", "nato", "kept: an organization"),
    ("oas", "oas", "kept: an organization"),
    ("eec", "eec", "kept: an organization"),
    ("oecd", "oecd", "kept: an organization"),
    ("imf", "imf", "kept: an organization"),
    ("afghanistan", "af", "the standard's code"),
    ("albania", "al", "the standard's code"),
    ("algeria", "dz", "the standard's code"),
    ("argentina", "ar", "the standard's code"),
    ("australia", "au", "the standard's code"),
    ("austria", "at", "the standard's code"),
    ("belgium", "be", "the standard's code"),
    ("bolivia", "bo", "the standard's code"),
    ("brazil", "br", "the standard's code"),
    ("bulgaria", "bg", "the standard's code"),
    ("burma", "bu", "the standard's code of 1974 (dropped in 1989 for MM)"),
    ("burundi", "bi", "the standard's code"),
    ("cameroon", "cm", "the standard's code"),
    ("canada", "ca", "the standard's code"),
    ("central-african-republic", "cf", "the standard's code"),
    ("ceylon", "lk", "the standard's code (Sri Lanka from May 1972)"),
    ("chad", "td", "the standard's code"),
    ("chile", "cl", "the standard's code"),
    ("colombia", "co", "the standard's code"),
    ("congo", "zr", "the standard's code of 1974, Zaire's (the name from Oct. 1971; today's CD)"),
    ("congo-brazzaville", "cg", "the standard's code"),
    ("costa-rica", "cr", "the standard's code"),
    ("cyprus", "cy", "the standard's code"),
    ("czechoslovakia", "cs", "the standard's code of 1974 (given to Serbia and Montenegro, 2003-06)"),
    ("dahomey", "dy", "the standard's code of 1974 (Benin from 1975: BJ)"),
    ("denmark", "dk", "the standard's code"),
    ("dominican-republic", "do", "the standard's code"),
    ("ecuador", "ec", "the standard's code"),
    ("el-salvador", "sv", "the standard's code"),
    ("ethiopia", "et", "the standard's code"),
    ("finland", "fi", "the standard's code"),
    ("gabon", "ga", "the standard's code"),
    ("ghana", "gh", "the standard's code"),
    ("greece", "gr", "the standard's code"),
    ("guatemala", "gt", "the standard's code"),
    ("guinea", "gn", "the standard's code"),
    ("guyana", "gy", "the standard's code (British Guiana to May 1966)"),
    ("honduras", "hn", "the standard's code"),
    ("hungary", "hu", "the standard's code"),
    ("iceland", "is", "the standard's code"),
    ("india", "in", "the standard's code"),
    ("indonesia", "id", "the standard's code"),
    ("iran", "ir", "the standard's code"),
    ("iraq", "iq", "the standard's code"),
    ("ireland", "ie", "the standard's code"),
    ("israel", "il", "the standard's code"),
    ("italy", "it", "the standard's code"),
    ("ivory-coast", "ci", "the standard's code"),
    ("japan", "jp", "the standard's code"),
    ("jordan", "jo", "the standard's code"),
    ("kenya", "ke", "the standard's code"),
    ("kuwait", "kw", "the standard's code"),
    ("lebanon", "lb", "the standard's code"),
    ("liberia", "lr", "the standard's code"),
    ("libya", "ly", "the standard's code"),
    ("luxembourg", "lu", "the standard's code"),
    ("malaysia", "my", "the standard's code (Malaya to Sept. 1963)"),
    ("mali", "ml", "the standard's code (the Mali Federation to Aug. 1960)"),
    ("mauritania", "mr", "the standard's code"),
    ("mexico", "mx", "the standard's code"),
    ("mongolia", "mn", "the standard's code"),
    ("morocco", "ma", "the standard's code"),
    ("nepal", "np", "the standard's code"),
    ("netherlands", "nl", "the standard's code"),
    ("nicaragua", "ni", "the standard's code"),
    ("niger", "ne", "the standard's code"),
    ("nigeria", "ng", "the standard's code"),
    ("norway", "no", "the standard's code (quoted in YAML: STYLE 3)"),
    ("nz", "nz", "kept: the standard's code"),
    ("pakistan", "pk", "the standard's code (East Pakistan Bangladesh from 1971)"),
    ("panama", "pa", "the standard's code"),
    ("paraguay", "py", "the standard's code"),
    ("peru", "pe", "the standard's code"),
    ("philippines", "ph", "the standard's code"),
    ("poland", "pl", "the standard's code"),
    ("portugal", "pt", "the standard's code"),
    ("rhodesia", "rh", "the standard's code of 1974, Southern Rhodesia's (Zimbabwe from 1980: ZW)"),
    ("romania", "ro", "the standard's code"),
    ("saudi-arabia", "sa", "the standard's code"),
    ("senegal", "sn", "the standard's code"),
    ("sierra-leone", "sl", "the standard's code"),
    ("singapore", "sg", "the standard's code (in Malaysia, Sept. 1963-Aug. 1965)"),
    ("somalia", "so", "the standard's code"),
    ("south-africa", "za", "the standard's code"),
    ("south-yemen", "yd", "the standard's code of 1974, Democratic Yemen's (the PDRY from 1970)"),
    ("sudan", "sd", "the standard's code"),
    ("spain", "es", "the standard's code"),
    ("sweden", "se", "the standard's code"),
    ("switzerland", "ch", "the standard's code"),
    ("syria", "sy", "the standard's code (in the UAR to Sept. 1961)"),
    ("tanzania", "tz", "the standard's code (Tanganyika and Zanzibar to Apr. 1964)"),
    ("thailand", "th", "the standard's code"),
    ("togo", "tg", "the standard's code"),
    ("tunisia", "tn", "the standard's code"),
    ("turkey", "tr", "the standard's code"),
    ("uganda", "ug", "the standard's code"),
    ("upper-volta", "hv", "the standard's code of 1974 (Burkina Faso from 1984: BF)"),
    ("uruguay", "uy", "the standard's code"),
    ("vatican", "va", "the standard's code"),
    ("venezuela", "ve", "the standard's code"),
    ("western-samoa", "ws", "the standard's code"),
    ("yemen", "ye", "the standard's code (the Yemen Arab Republic)"),
    ("yugoslavia", "yu", "the standard's code of 1974 (dropped in 2003)"),
    ("zambia", "zm", "the standard's code (Northern Rhodesia to Oct. 1964)"),
]
CODES = {o: n for o, n, _ in TABLE if o != n}
KEPT = {o for o, n, _ in TABLE if o == n}
# ids with no row in the register that the code (vis_words.NATIONS) or the registry (frus_parties) writes
EXTRA = {"malawi": "mw", "madagascar": "mg", "rwanda": "rw", "trinidad": "tt", "malta": "mt", "bahrain": "bh",
         "oman": "om", "haiti": "ht", "jamaica": "jm", "south-arabia": "fsa"}
ALL = {**CODES, **EXTRA}
YAML_WORDS = {"no", "yes", "on", "off", "y", "n", "true", "false", "null"}   # a bare YAML scalar that is no string


def ycode(c):
    """A code as a YAML scalar: quoted where YAML would read it as something else (STYLE 3)."""
    return f"'{c}'" if c.lower() in YAML_WORDS else c


# ---------------------------------------------------------------- tags (lists, the fixture, the tests)

TAG_RX = re.compile(r"(?<![\w:-])polity:([a-z][a-z0-9-]*)(?![\w-])"
                    r"|(?<![\w:-])vis:(only|frame|from):([a-z0-9-]+(?:\+[a-z0-9-]+)*)(?![a-z0-9+-])")


def recode_tags(text, codes=ALL):
    """(text, count): every `polity:` tag and `vis:` ruling in the text with the new codes."""
    n = 0

    def sub(m):
        nonlocal n
        if m.group(1) is not None:
            if m.group(1) in codes:
                n += 1
                return "polity:" + codes[m.group(1)]
            return m.group(0)
        ps = m.group(3).split("+")
        if not any(p in codes for p in ps):
            return m.group(0)
        n += 1
        return f"vis:{m.group(2)}:" + "+".join(codes.get(p, p) for p in ps)
    return TAG_RX.sub(sub, text), n


# ---------------------------------------------------------------- YAML lines, outside their quoted strings

def _segments(line):
    """[(quoted, text)]: a YAML line cut at its quoted strings ('...' with '' inside; "..." with \\" inside) and its
    comment (a ` #` outside quotes: kept as one quoted segment, never rewritten)."""
    out, i, buf = [], 0, ""
    while i < len(line):
        ch = line[i]
        if ch == "#" and (i == 0 or line[i - 1] in " \t"):
            out.append((False, buf))
            out.append((True, line[i:]))
            return out
        if ch in "'\"":
            j = i + 1
            while j < len(line):
                if ch == "'" and line[j] == "'" and j + 1 < len(line) and line[j + 1] == "'":
                    j += 2
                    continue
                if ch == '"' and line[j] == "\\":
                    j += 2
                    continue
                if line[j] == ch:
                    break
                j += 1
            out.append((False, buf))
            out.append((True, line[i:j + 1]))
            buf, i = "", j + 1
            continue
        buf += ch
        i += 1
    out.append((False, buf))
    return out


def _outside(line, rx, fn):
    """The line with rx.sub(fn) applied outside its quoted strings and comment; (line, count)."""
    n = [0]

    def f(m):
        r = fn(m)
        if r != m.group(0):
            n[0] += 1
        return r
    return "".join(t if q else rx.sub(f, t) for q, t in _segments(line)), n[0]


LIST_ITEM = re.compile(r"(?<=[\[,])(\s*)([a-z][a-z0-9-]*)(?=\s*[,\]])")


def _field_rx(field):
    return re.compile(rf"(?<![\w-]){field}: ([a-z][a-z0-9-]*)(?=\s*[,}}\]]|\s*$)")


def recode_list_items(line, codes):
    return _outside(line, LIST_ITEM, lambda m: m.group(1) + ycode(codes[m.group(2)]) if m.group(2) in codes
                    else m.group(0))


def recode_field(line, field, codes):
    rx = _field_rx(field)
    return _outside(line, rx, lambda m: f"{field}: {ycode(codes[m.group(1)])}" if m.group(1) in codes else m.group(0))


POL_ROW = re.compile(r"^(\s+)([a-z][a-z0-9-]*)(: \{)(.*)(\}\s*(?:#.*)?)$")


def _polity_row(line, codes):
    """A row of the register's `polities:`: its key the new code, its tag in capitals, its old id in `aliases`."""
    m = POL_ROW.match(line)
    if not m or m.group(2) not in codes:
        line, k = recode_field(line, "folded", codes)
        line, k2 = recode_field(line, "then", codes)
        return line, k + k2
    ind, old, sep, body, end = m.groups()
    new = codes[old]
    t = re.search(r"\btag: '([^']*)'", body)
    if t:
        body = body[:t.start()] + f"tag: '{new.upper()}'" + body[t.end():]
        at = t.start() + len(f"tag: '{new.upper()}'")
    else:
        at = len(body)
    a = re.search(r"\baliases: \[([^\]]*)\]", body)
    if a:
        items = [x.strip() for x in a.group(1).split(",") if x.strip()]
        if old not in items:
            body = body[:a.start()] + "aliases: [" + ", ".join(items + [old]) + "]" + body[a.end():]
    else:
        body = body[:at] + f", aliases: [{old}]" + body[at:]
    line = f"{ind}{ycode(new)}{sep}{body}{end}"
    line, _ = recode_field(line, "folded", codes)
    line, _ = recode_field(line, "then", codes)
    return line, 1


TOP_LINE = re.compile(r"^(# Top level \(§2\): )([^;]*)(;.*)$")


def recode_register(text, codes=CODES):
    """(text, count): sources/polities.yaml (or a test's copy of its form) in the new codes (STYLE 2)."""
    out, sec, n = [], None, 0
    for line in text.split("\n"):
        k = 0
        h = re.match(r"^([a-z_]+):\s*(?:#.*)?$", line)
        if h:
            sec = h.group(1)
        elif sec is None:
            m = TOP_LINE.match(line)
            if m:
                items = [codes.get(x.strip(), x.strip()) for x in m.group(2).split(",")]
                new = m.group(1) + ", ".join(items) + m.group(3)
                k = int(new != line)
                line = new
        elif sec == "polities":
            line, k = _polity_row(line, codes)
        elif sec in ("threads", "places"):
            line, k = recode_list_items(line, codes)
        elif sec == "names":
            line, k = recode_field(line, "polity", codes)
        out.append(line)
        n += k
    return "\n".join(out), n


def recode_gazetteer(text, codes=CODES):
    """(text, count): sources/places.yaml's `in:` (a value, a flow list, a block list under it)."""
    out, n, block = [], 0, None
    for line in text.split("\n"):
        k = 0
        if block is not None:
            m = re.match(r"^(\s+)- ([a-z][a-z0-9-]*)(\s*)$", line)
            if m and len(m.group(1)) > block:
                if m.group(2) in codes:
                    line, k = f"{m.group(1)}- {ycode(codes[m.group(2)])}{m.group(3)}", 1
                out.append(line)
                n += k
                continue
            block = None
        m = re.match(r"^(\s*)in:\s*$", line)
        if m:
            block = len(m.group(1))
        elif re.match(r"^\s*in: \[", line):
            line, k = recode_list_items(line, codes)
        else:
            line, k = recode_field(line, "in", codes)
        out.append(line)
        n += k
    return "\n".join(out), n


def recode_people(text, codes=CODES):
    out, n = [], 0
    for line in text.split("\n"):
        line, k = recode_field(line, "polity", codes)
        out.append(line)
        n += k
    return "\n".join(out), n


PUB_ROW = re.compile(r"^(\s+(?:'(?:[^']|'')*'|[^':#][^:#]*)): ([a-z][a-z0-9-]*)(\s*(?:#.*)?)$")


def recode_registry(text, codes=ALL):
    """(text, count): sources/provenance.yaml: series' `polity` and `privity`, frus_parties, publishers, works."""
    out, sec, n = [], None, 0
    for line in text.split("\n"):
        k = 0
        h = re.match(r"^([a-z_]+):\s*(?:#.*)?$", line)
        if h:
            sec = h.group(1)
        elif sec == "series":
            line, k = recode_field(line, "polity", codes)
            m = re.search(r"\bprivity: \[", line)
            if m:
                head, tail = line[:m.end() - 1], line[m.end() - 1:]
                j = tail.index("]") + 1
                lst, k2 = recode_list_items(tail[:j], codes)
                line, k = head + lst + tail[j:], k + k2
        elif sec == "frus_parties":
            line, k = recode_list_items(line, codes)
        elif sec == "publishers":
            m = PUB_ROW.match(line)
            if m and m.group(2) in codes:
                line, k = f"{m.group(1)}: {ycode(codes[m.group(2)])}{m.group(3)}", 1
        elif sec == "works":
            line, k = recode_field(line, "country", codes)
        out.append(line)
        n += k
    return "\n".join(out), n


def recode_witnesses(text, codes=CODES):
    out, n = [], 0
    for line in text.split("\n"):
        line, k = recode_field(line, "local", codes)
        line, k2 = recode_field(line, "circulated", codes)
        out.append(line)
        n += k + k2
    return "\n".join(out), n


def recode_pages(text, codes=CODES):
    """(text, count): pages.yaml's `places:` plan under a nation's old id: its key and its parts' page names."""
    out, sec, n, cur = [], None, 0, None
    for line in text.split("\n"):
        k = 0
        h = re.match(r"^([a-z_]+):", line)
        if h and not line.startswith(" "):
            sec, cur = h.group(1), None
        elif sec == "places":
            m = re.match(r"^  ([a-z][a-z0-9-]*):\s*$", line)
            if m:
                cur = m.group(1) if m.group(1) in codes else None
                if cur:
                    line, k = f"  {ycode(codes[cur])}:", 1
            elif cur:
                new = re.sub(rf"\bplaces-{re.escape(cur)}(?=-|\b)", f"places-{codes[cur]}", line)
                k, line = int(new != line), new
        out.append(line)
        n += k
    return "\n".join(out), n


# ---------------------------------------------------------------- the code's literals, by their place (ast)

def _offsets(src):
    """(line, utf-8 column) -> the offset in the text."""
    starts, at = [], 0
    for l in src.splitlines(keepends=True):
        starts.append(at)
        at += len(l)
    lines = src.splitlines(keepends=True)

    def off(lineno, col):
        return starts[lineno - 1] + len(lines[lineno - 1].encode("utf-8")[:col].decode("utf-8"))
    return off


def _assigned(tree, name):
    """The value of the module's first assignment to `name`."""
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return node.value
    return None


def _strs(node):
    return [n for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)] if node else []


def _const(n):
    return n if isinstance(n, ast.Constant) and isinstance(n.value, str) else None


def _rule_nodes(tree, src, rule, codes):
    """[(node, new text)] for one rule (CODE, TESTS): the string literals it names, with their new values."""
    kind = rule[0]
    up = {o.upper(): n.upper() for o, n in codes.items()}
    out = []

    def put(n, new=None):
        if n is not None and (new is not None or n.value in codes):
            out.append((n, new if new is not None else codes[n.value]))
    if kind == "all":
        for n in _strs(_assigned(tree, rule[1])):
            put(n) if n.value in codes else None
    elif kind == "keys":
        v = _assigned(tree, rule[1])
        for k in (v.keys if isinstance(v, ast.Dict) else []):
            put(_const(k)) if _const(k) is not None and k.value in codes else None
    elif kind == "values":
        v = _assigned(tree, rule[1])
        for val in (v.values if isinstance(v, ast.Dict) else []):
            for n in _strs(val):
                put(n) if n.value in codes else None
    elif kind == "item":
        v = _assigned(tree, rule[1])
        for el in (v.elts if isinstance(v, (ast.List, ast.Tuple)) else []):
            if isinstance(el, ast.Tuple) and len(el.elts) > rule[2]:
                c = _const(el.elts[rule[2]])
                put(c) if c is not None and c.value in codes else None
    elif kind == "arg":
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == rule[1] and \
                    len(n.args) > rule[2]:
                c = _const(n.args[rule[2]])
                put(c) if c is not None and c.value in codes else None
    elif kind == "func-tuple":
        for f in ast.walk(tree):
            if isinstance(f, ast.FunctionDef) and f.name == rule[1]:
                for t in ast.walk(f):
                    if isinstance(t, ast.Tuple):
                        for el in t.elts:
                            c = _const(el)
                            put(c) if c is not None and c.value in codes else None
    elif kind == "asserts":
        for a in ast.walk(tree):
            if isinstance(a, ast.Assert) and rule[1] in (ast.get_source_segment(src, a) or ""):
                for n in _strs(a):
                    put(n) if n.value in codes else None
    elif kind == "register":
        v = _assigned(tree, rule[1])
        if not isinstance(v, ast.Dict):
            return out
        secs = {k.value: val for k, val in zip(v.keys, v.values) if _const(k) is not None}
        rows = secs.get("polities", v if "polities" not in secs else None)
        if isinstance(rows, ast.Dict):
            for k, val in zip(rows.keys, rows.values):
                c = _const(k)
                if c is None or c.value not in codes:
                    continue
                put(c)
                if isinstance(val, ast.Dict):
                    out.append(("insert", val, c.value))      # its old id, as an alias
                    for fk, fv in zip(val.keys, val.values):
                        fc, vc = _const(fk), _const(fv)
                        if fc is not None and vc is not None and fc.value == "tag" and vc.value in up:
                            put(vc, up[vc.value])
        if isinstance(rows, ast.Dict):
            for val in rows.values:
                for fk, fv in zip(getattr(val, "keys", []), getattr(val, "values", [])):
                    fc, vc = _const(fk), _const(fv)
                    if fc is not None and fc.value in ("folded", "then") and vc is not None and vc.value in codes:
                        put(vc)
        for name in ("places", "threads"):
            d = secs.get(name)
            for val in (d.values if isinstance(d, ast.Dict) else []):
                for n in _strs(val):
                    put(n) if n.value in codes else None
        d = secs.get("names")
        for val in (d.values if isinstance(d, ast.Dict) else []):
            for sub in ast.walk(val):
                if isinstance(sub, ast.Dict):
                    for fk, fv in zip(sub.keys, sub.values):
                        fc, vc = _const(fk), _const(fv)
                        if fc is not None and fc.value == "polity" and vc is not None and vc.value in codes:
                            put(vc)
    elif kind == "yaml":
        c = _const(_assigned(tree, rule[1]))
        if c is not None:
            new, k = recode_register(c.value, CODES)
            if k:
                out.append(("yaml", c, new))
    return out


def _target_found(tree, rule):
    """Whether the file still has what the rule names (an assignment, a function, a call); "asserts" needs none."""
    kind = rule[0]
    if kind == "asserts":
        return True
    if kind == "func-tuple":
        return any(isinstance(f, ast.FunctionDef) and f.name == rule[1] for f in ast.walk(tree))
    if kind == "arg":
        return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == rule[1]
                   for n in ast.walk(tree))
    return _assigned(tree, rule[1]) is not None


def recode_python(src, rules, tags=False, codes=ALL):
    """(text, count, missing): a Python file's literals in the new codes, by the rules (STYLE 2); its tag literals
    too where tags; missing: the rules ("text" ones) that found neither their old nor their new form."""
    n, missing = 0, []
    texts = [r for r in rules if r[0] == "text"]
    rules = [r for r in rules if r[0] != "text"]
    if rules:
        tree = ast.parse(src)
        off = _offsets(src)
        edits = []
        for rule in rules:
            if not _target_found(tree, rule):
                missing.append(f"{rule}: its {'function' if rule[0] == 'func-tuple' else 'name'} is not in the file")
                continue
            for item in _rule_nodes(tree, src, rule, codes):
                if item[0] == "insert":
                    _, d, old = item
                    a = off(d.lineno, d.col_offset) + 1
                    if src[a - 1] != "{":
                        missing.append(f"{rule}: a row not written as a dict at line {d.lineno}")
                        continue
                    edits.append((a, a, f'"aliases": ["{old}"], '))
                    continue
                if item[0] == "yaml":
                    _, c, _ = item
                    a, b = off(c.lineno, c.col_offset), off(c.end_lineno, c.end_col_offset)
                    seg = src[a:b]
                    q = re.match(r'^[rRbBuU]*("""|\'\'\'|"|\')', seg)
                    if not q or not seg.endswith(q.group(1)):
                        missing.append(f"{rule}: a register text not written plainly at line {c.lineno}")
                        continue
                    i, j = q.end(), len(seg) - len(q.group(1))
                    body, _ = recode_register(seg[i:j], CODES)
                    edits.append((a, b, seg[:i] + body + seg[j:]))
                    continue
                node, new = item
                a, b = off(node.lineno, node.col_offset), off(node.end_lineno, node.end_col_offset)
                seg = src[a:b]
                if len(seg) < 2 or seg[0] not in "'\"" or seg[-1] != seg[0] or seg[1:-1] != node.value:
                    missing.append(f"{rule}: a literal not written plainly at line {node.lineno}")
                    continue
                edits.append((a, b, seg[0] + new + seg[0]))
        seen = set()
        for a, b, t in sorted(edits, key=lambda x: (x[0], x[1]), reverse=True):
            if (a, b, t) in seen:
                continue
            seen.add((a, b, t))
            src = src[:a] + t + src[b:]
            n += 1
    for _, old, new in texts:
        if old in src:
            n += src.count(old)
            src = src.replace(old, new)
        elif new not in src:
            missing.append(f"text {old!r}: found in neither form")
    if tags:
        src, k = recode_tags(src, codes)
        n += k
    return src, n, missing


# The code's own literals (STYLE 2): file -> (rules, tags too)
CODE = {
    "tools/bib/vis.py": ([("all", "TOP"), ("item", "ARCHIVES", 1), ("values", "LOCAL_NAMES"),
                          ("text", "vis:only:ussr+cuba", "vis:only:ussr+cu")], False),
    "tools/bib/vispage.py": ([("item", "TOP", 0)], False),
    "tools/bib/vis_words.py": ([("item", "NATIONS", 1)], False),
    "tools/bib/placepages.py": ([("all", "FOLD"), ("keys", "NATION_WORDS"), ("func-tuple", "_map"),
                                 ("text", 'preview: "laos"', 'preview: "la"')], False),
    "tools/vis/seed.py": ([("register", "POLITIES"), ("keys", "OTHER_NAMES"), ("values", "THREADS"),
                           ("values", "PLACES_HAND"), ("values", "COUNTRY"), ("arg", "S", 2), ("keys", "PUBLISHERS")],
                          False),
    "tools/vis/selfcheck.py": ([("text", '("Prime Minister of India", "india")', '("Prime Minister of India", "in")'),
                                ("text", 'strict=True), "belgium")', 'strict=True), "be")'),
                                ("text", '"CUBA:public-PA"', '"CU:public-PA"')], False),
}
# The tests (STYLE 2): their registers, their assertions on a nation's id, their tags
TESTS = {
    "tests/unit/test_place_tags.py": ([("register", "REGISTER")], True),
    "tests/unit/test_placepages.py": ([("register", "REGISTER"), ("asserts", "nation")], True),
    "tests/unit/test_maps.py": ([("yaml", "POLITIES")], False),
}


# ---------------------------------------------------------------- the pass

def _read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def plan(root=ROOT):
    """[(path relative to root, new text, count, missing)] for every file the change touches (STYLE 2)."""
    out = []

    def add(rel, fn):
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            return
        old = _read(p)
        r = fn(old)
        new, n = r[0], r[1]
        missing = r[2] if len(r) > 2 else []
        if new != old or missing:
            out.append((rel, new, n, missing))
    add("sources/polities.yaml", recode_register)
    for p in sorted(glob.glob(os.path.join(root, "lists", "**", "*.yaml"), recursive=True)):
        add(os.path.relpath(p, root), recode_tags)
    add("sources/places.yaml", recode_gazetteer)
    add("sources/people.yaml", recode_people)
    add("sources/provenance.yaml", recode_registry)
    for p in sorted(glob.glob(os.path.join(root, "sources", "witnesses", "**", "*.yaml"), recursive=True)):
        add(os.path.relpath(p, root), recode_witnesses)
    add("pages.yaml", recode_pages)
    for rel, (rules, tags) in {**CODE, **TESTS}.items():
        add(rel, lambda s, rules=rules, tags=tags: recode_python(s, rules, tags))
    for p in sorted(glob.glob(os.path.join(root, "tests", "fixture", "lists", "**", "*.yaml"), recursive=True)):
        add(os.path.relpath(p, root), recode_tags)
    add("tests/fixture/sources/places.yaml", recode_gazetteer)
    return out


def waiting(root=ROOT):
    """The patches waiting in inbox/ (its top level; held/, merged/ and superseded/ are not waiting)."""
    return sorted(os.path.basename(p) for p in glob.glob(os.path.join(root, "inbox", "*.yaml")))


def table():
    """The table of codes, as Markdown rows (the note to the owner)."""
    rows = ["| Now | New | Why |", "|---|---|---|"]
    rows += [f"| `{o}` | `{n}` | {why} |" for o, n, why in TABLE]
    return "\n".join(rows)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--apply", action="store_true", help="write the change (the default is a dry run)")
    ap.add_argument("--force", action="store_true", help="apply though a patch waits in inbox/")
    ap.add_argument("--root", default=ROOT, help="the tree to change (default: this checkout)")
    ap.add_argument("--table", action="store_true", help="print the table of codes and stop")
    a = ap.parse_args(argv)
    if a.table:
        print(table())
        return 0
    got = plan(a.root)
    total, missing = 0, []
    groups = {}
    for rel, _, n, miss in got:
        total += n
        missing += [f"{rel}: {m}" for m in miss]
        g = rel
        if rel.startswith("lists/"):
            g = "lists/" + rel.split("/")[1] + "/"
        elif rel.startswith("tests/fixture/lists/"):
            g = "tests/fixture/lists/"
        groups.setdefault(g, [0, 0])
        groups[g][0] += n
        groups[g][1] += 1
    for g, (n, files) in groups.items():
        print(f"{n:7,}  {g}" + (f"  ({files} files)" if files > 1 else ""))
    print(f"{total:7,}  in all, {len(got)} files" + ("" if a.apply else "  (a dry run: --apply writes it)"))
    for m in missing:
        print("missing  " + m)
    if not a.apply:
        return 0
    if missing:
        print("not applied: a rule found its literal in neither form (STYLE 4); mend the rule", file=sys.stderr)
        return 1
    w = waiting(a.root)
    if w and not a.force:
        print(f"not applied: {len(w)} patches wait in inbox/ ({', '.join(w[:5])}); merge them first, or --force",
              file=sys.stderr)
        return 1
    for rel, new, _, _ in got:
        with open(os.path.join(a.root, rel), "w", encoding="utf-8") as f:
            f.write(new)
    print("written. Next: python3 -m pytest -q -m \"not slow\" --update-goldens (read the diff), then ./bib check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
