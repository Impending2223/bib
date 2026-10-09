"""The Senate's roll calls on nominations, 83rd to 93rd Congress (1953-74), from Voteview.
# Usage: python3 tools/executive/make_votes.py
#   Writes sources/senate-nomination-votes.json: one row a roll call on a nomination, in order. Needs the network;
#   the build does not. The build matches the rows to the Executive roster's holders and the series' persons
#   (tools/bib/votes.py); sources/vote-matches.yaml settles what the rules cannot.
#
#   Voteview (Lewis et al., voteview.com): the Senate's roll calls by Congress, with the yeas and nays and a
#   description of each question (dtl_desc). A row is kept where the description is of a nomination ("NOMINATION
#   OF", "CONFIRMATION OF") and not of a bill, resolution, amendment, or treaty. Each row:
#     rc       Voteview's id (RS0930394: Senate, Congress, roll number), the link's key
#     date, yea, nay, desc (Voteview's description as written)
#     kind     'final' (the question of consent), or the procedural question: recommit, table, postpone,
#              cloture, point of order, reconsider, consider
"""
import csv, io, json, os, re, urllib.request

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'sources', 'senate-nomination-votes.json')
URL = 'https://voteview.com/static/data/out/rollcalls/S{:03d}_rollcalls.csv'
NOM = re.compile(r'N[OI]MINATIONS? OF|CONFIRMATION OF', re.I)
NOT = re.compile(r'RATIFICATION|ACCESSION|^TO AMEND|^TO PASS|EXECUTIVE SESSION|REQUIR\w* SENATE CONFIRMATION|'
                 r'NOMINATE PRESIDENTIAL|OBTAIN NOMINATION|ACADEMY|SENATE RULE|AMENDMENT TO S\. \d', re.I)
BILL = re.compile(r'^\s*(H\.?\s?R\.|S\.\s?J\.?\s?RES|S\.\s?RES|S\.\s?CON|H\.\s?J\.?\s?RES|S\.\s?\d|HR\s?\d|TO AMEND S\.?\s?RES|TO TABLE S\.?\s?RES)', re.I)
KIND = [('cloture', r'CLOSE DEBATE|CLOTURE'), ('recommit', r'RECOMMIT'), ('postpone', r'POSTPONE'),
        ('point of order', r'POINT OF ORDER'), ('reconsider', r'RECONSIDER'), ('table', r'\bTABLE\b'),
        ('consider', r'MOTION TO (PROCEED TO )?CONSIDER|TO CONSIDER THE NOMINATION|MOVE TO CONSIDER')]


def kind(d):
    for k, pat in KIND:
        if re.search(pat, d, re.I):
            return k
    return 'final'


def main():
    rows = []
    for c in range(83, 94):
        with urllib.request.urlopen(URL.format(c), timeout=120) as r:
            for x in csv.DictReader(io.StringIO(r.read().decode())):
                d = re.sub(r'\s+', ' ', (x.get('dtl_desc') or '').strip())
                if not NOM.search(d) or BILL.search(d) or NOT.search(d):
                    continue
                rows.append({'rc': f"RS{c:03d}{int(x['rollnumber']):04d}", 'date': x['date'],
                             'yea': int(x['yea_count']), 'nay': int(x['nay_count']), 'kind': kind(d), 'desc': d})
    rows.sort(key=lambda r: (r['date'], r['rc']))
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('[\n' + ',\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n]\n')
    print(len(rows), 'roll calls;', sum(r['kind'] == 'final' for r in rows), 'on consent')


if __name__ == '__main__':
    main()
