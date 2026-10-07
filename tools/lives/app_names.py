"""The Public Papers (APP) documents that name a person: sources/app-names/<key>.json.
# Usage: python3 tools/lives/app_names.py OUT.json '"Hubert H. Humphrey"' '"Senator Humphrey"' ...
#   Each phrase searched in the American Presidency Project's full text, Jan. 20, 1953, to Aug. 31, 1974;
#   the union kept with each hit's phrases and snippets. Needs the network; the build does not.
"""
import re, sys, json, time, html, urllib.parse, urllib.request
OUT = sys.argv[1]
QS = sys.argv[2:]
UA = {'User-Agent': 'Mozilla/5.0 (bibliography)'}
rows = {}
for q in QS:
    page = 0
    while True:
        url = ('https://www.presidency.ucsb.edu/advanced-search?' + urllib.parse.urlencode(
            {'field-keywords': q, 'from[date]': '01-20-1953', 'to[date]': '08-31-1974', 'items_per_page': 100,
             'order': 'field_docs_start_date_time_value', 'sort': 'asc', 'page': page}))
        t = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read().decode('utf-8', 'replace')
        found = re.findall(r'<tr class="[^"]*">\s*<td class="views-field views-field-field-docs-start-date-time-value[^"]*"\s*>\s*([^<]*?)\s*</td>'
                           r'\s*<td class="views-field views-field-field-docs-person[^"]*"\s*>\s*(?:<a[^>]*>)?([^<]*)(?:</a>)?\s*</td>'
                           r'\s*<td class="views-field views-field-title"\s*>\s*<a href="([^"]+)">([^<]*)</a>(.*?)</td>', t, re.S)
        for date, who, href, title, snip in found:
            snip = html.unescape(re.sub(r'<[^>]+>', '', snip)).strip()
            r = rows.setdefault(href, {'date': date, 'who': who.strip(), 'url': 'https://www.presidency.ucsb.edu' + href,
                                       'title': html.unescape(title).strip(), 'q': [], 'snip': []})
            r['q'].append(q); r['snip'].append(snip[:200])
        m = re.search(r'of (\d+) records', t)
        total = int(m.group(1)) if m else 0
        page += 1
        if page * 100 >= total or not found:
            break
        time.sleep(1)
    print(q, total, file=sys.stderr)
json.dump(list(rows.values()), open(OUT, 'w'), ensure_ascii=False, indent=0)
print(len(rows))
