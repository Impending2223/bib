"""Polite Wikipedia API fetcher: python3 -I wiki.py LANG OUT key=value ...
Retries with backoff on rate limiting; writes the JSON response to OUT."""
import json, sys, time, urllib.error, urllib.parse, urllib.request

UA = "bib-research/1.0 (calendar project)"


def fetch(lang, params, tries=60):
    params = dict(params, format="json", formatversion="2")
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
    wait = 20
    for i in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read().decode("utf-8")
            return json.loads(body)
        except urllib.error.HTTPError as e:  # 429: honor Retry-After
            ra = int(e.headers.get("retry-after") or 30)
            print(f"retry {i} after {ra + 5}s: {e}", file=sys.stderr)
            time.sleep(ra + 5)
        except Exception as e:
            print(f"retry {i} after {wait}s: {e}", file=sys.stderr)
            time.sleep(wait)
            wait = min(wait * 2, 300)
    raise SystemExit("gave up: " + url)


if __name__ == "__main__":
    lang, out = sys.argv[1], sys.argv[2]
    params = dict(a.split("=", 1) for a in sys.argv[3:])
    d = fetch(lang, params)
    json.dump(d, open(out, "w"), ensure_ascii=False)
    time.sleep(3)
