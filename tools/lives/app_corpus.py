"""The American Presidency Project's documents of Jan. 20, 1953, to Aug. 31, 1974, read once into a local corpus.
# Usage: python3 tools/lives/app_corpus.py CACHE_DIR [--workers 2]
#   1. lists every document in the span (APP's advanced search by date, 100 a page) into CACHE_DIR/index.jsonl:
#      {url, date, who, title}
#   2. fetches each document's text into CACHE_DIR/docs/<n>.json.gz: {url, text}
#   Resumable: a rerun skips what is there. Polite: each worker waits a second between requests.
#   tools/lives/app_names.py then matches every person's names against the corpus locally. The build needs neither.
"""
import concurrent.futures, gzip, hashlib, html, json, os, re, sys, time, urllib.parse, urllib.request

APP = "https://www.presidency.ucsb.edu"
UA = {"User-Agent": "Mozilla/5.0 (bibliography; one-time corpus for a research index)"}
FROM, TO = "01-20-1953", "08-31-1974"
ROW = re.compile(r'<tr class="[^"]*">\s*<td class="views-field views-field-field-docs-start-date-time-value[^"]*"\s*>\s*([^<]*?)\s*</td>'
                 r'\s*<td class="views-field views-field-field-docs-person[^"]*"\s*>\s*(?:<a[^>]*>)?([^<]*)(?:</a>)?\s*</td>'
                 r'\s*<td class="views-field views-field-title"\s*>\s*<a href="([^"]+)">([^<]*)</a>', re.S)


def get(url, tries=6):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            print("retry", url, e, file=sys.stderr)
            time.sleep(5 * (i + 1))
    return ""


def listing(cache):
    path = os.path.join(cache, "index.jsonl")
    if os.path.exists(path) and os.path.exists(path + ".done"):
        return [json.loads(l) for l in open(path, encoding="utf-8")]
    rows, page, total = [], 0, None
    while True:
        q = urllib.parse.urlencode({"field-keywords": "", "from[date]": FROM, "to[date]": TO, "items_per_page": 100,
                                    "order": "field_docs_start_date_time_value", "sort": "asc", "page": page})
        t = get(f"{APP}/advanced-search?{q}")
        m = re.search(r"of (\d+) records", t)
        total = int(m.group(1)) if m else total
        found = ROW.findall(t)
        for date, who, href, title in found:
            rows.append({"url": APP + href, "date": date.strip(), "who": html.unescape(who.strip()),
                         "title": html.unescape(title.strip())})
        page += 1
        print("listing", page, len(rows), total, file=sys.stderr)
        if not found or (total and page * 100 >= total):
            break
        time.sleep(1)
    seen, out = set(), []
    for r in rows:
        if r["url"] not in seen:
            seen.add(r["url"])
            out.append(r)
    with open(path, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    open(path + ".done", "w").write(str(len(out)))
    return out


def text_of(page):
    i = page.find('class="field-docs-content"')
    if i < 0:
        return ""
    j = page.find('<div class="field-docs-footnote', i)
    k = page.find('<div class="col-sm-4', i)
    end = min(x for x in (j, k, len(page)) if x > i)
    t = re.sub(r"<[^>]+>", " ", page[i:end].split(">", 1)[1])
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def fetch(cache, r):
    name = hashlib.sha1(r["url"].encode()).hexdigest()[:16]
    path = os.path.join(cache, "docs", name + ".json.gz")
    if os.path.exists(path):
        return False
    t = text_of(get(r["url"]))
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump({"url": r["url"], "text": t}, f, ensure_ascii=False)
    time.sleep(1)
    return True


def main():
    cache = sys.argv[1]
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 2
    os.makedirs(os.path.join(cache, "docs"), exist_ok=True)
    rows = listing(cache)
    done = 0
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        for i, got in enumerate(ex.map(lambda r: fetch(cache, r), rows)):
            done += got
            if i % 200 == 0:
                print("docs", i, len(rows), "new", done, file=sys.stderr, flush=True)
    print("done", len(rows))


if __name__ == "__main__":
    main()
