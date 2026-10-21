"""python3 -I prose.py BATCH.json TITLE [maxchars]: the page's prose, templates and refs stripped, table cells kept"""
import json, re, sys, unicodedata
N = lambda x: unicodedata.normalize("NFC", x)
def strip_templates(s):
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\{\{[^{}]*\}\}", "", s)
    return s
def clean(t):
    t = re.sub(r"<ref[^>]*?/>", "", t)
    t = re.sub(r"<ref.*?</ref>", "", t, flags=re.S)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = strip_templates(t)
    t = re.sub(r"\[\[(?:File|Image|Tập tin|Hình):[^\]]*(?:\[\[[^\]]*\]\][^\]]*)*\]\]", "", t)
    t = re.sub(r"\[\[Category:[^\]]*\]\]|\[\[Thể loại:[^\]]*\]\]", "", t)
    t = re.sub(r"\[\[([^|\]]*\|)?([^\]]*)\]\]", r"\2", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t
if __name__ == "__main__":
    d = json.load(open(sys.argv[1])); mx = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
    for p in d["query"]["pages"]:
        if N(p["title"]) == N(sys.argv[2]) and p.get("revisions"):
            print(clean(p["revisions"][0]["slots"]["main"]["content"])[:mx])
