"""The prefectures' names in pinyin, for the pin's panel on the map of China (tools/bib/vnmap.js; the owner, Nov. 27,
2026: "could we give the Pinyin and CJK of all tiers, not just the counties?"). A one-time script, run again after
base.py:

    python3 tools/cnmap/prefs.py [OUT]

It reads the prefectures of 1964 named in sources/china/counties.json (`pref`: 苏州专区, 延边朝鲜族自治州, 呼伦贝尔盟)
and writes {characters: pinyin} to OUT (default tools/cnmap/prefectures.json), which tools/bib/cnmap.py puts in the
manifest's `pin`. The pinyin is the name without its kind, by the counties' own rule (counties.syllables: pypinyin,
with the place-name readings it misses): 苏州专区 -> Suzhou, 延边朝鲜族自治州 -> Yanbian. A unit that is not a
prefecture (直辖单位, the units under a province directly) has no row. Needs pypinyin.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import counties as rec  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
KIND = r"((?:(?:%s)族?)*自治州|专区|地区|行政区|盟|市)$" % rec.ETHN


def romanise(n):
    """A prefecture's name in pinyin, its kind left off: the base read in the whole name, capitalised."""
    b = re.sub(KIND, "", n)
    if len(b) < 2 or not all("一" <= ch <= "鿿" for ch in b):
        return None
    syl = rec.syllables(n)[:len(b)]
    out = ""
    for i, s in enumerate(syl):
        out += ("'" if i and s[0] in "aeo" else "") + s
    return out[:1].upper() + out[1:]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "prefectures.json")
    cs = json.load(open(os.path.join(ROOT, "sources", "china", "counties.json"), encoding="utf-8"))["counties"]
    names = sorted({c["pref"] for c in cs if c.get("pref") and re.search(KIND, c["pref"])})
    rows = {n: r for n in names if (r := romanise(n))}
    json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
    print(len(rows), "prefectures;", len(names) - len(rows), "names not read:", [n for n in names if n not in rows])


if __name__ == "__main__":
    main()
