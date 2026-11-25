"""Links per month of the sequence pass: the final patch, and the reader's as handed in (the patch at the commit of the reader's note)."""
import glob, os, re, subprocess, sys, yaml
def count(text):
    try: d = yaml.safe_load(text)
    except Exception: return None
    add = rem = oth = 0
    for op in d.get('ops', []):
        (k, b), = op.items()
        if k == 'follows':
            add += len(b.get('add') or []); rem += len(b.get('remove') or [])
        else: oth += 1
    return add, rem, oth
rows = []
for f in sorted(glob.glob('inbox/merged/2026-11-25-sequence-19*.yaml') + glob.glob('inbox/2026-11-25-sequence-19*.yaml'), key=lambda f: f.rsplit('sequence-', 1)[1]):
    m = re.search(r'sequence-(\d{4}-\d\d)', f).group(1)
    fin = count(open(f).read())
    n = len(re.findall(r'^  - id: ', open(f'lists/cal/{m.replace("-","")}.yaml').read(), re.M))
    note = f'notes/sequence/{m}.md'
    rd = None
    if os.path.exists(note):
        c = subprocess.run(['git','log','--diff-filter=A','--format=%H','--',note],capture_output=True,text=True).stdout.split()
        if c:
            t = subprocess.run(['git','show',f'{c[-1]}:inbox/2026-11-25-sequence-{m}.yaml'],capture_output=True,text=True)
            if t.returncode == 0: rd = count(t.stdout)
    rows.append((m, n, rd, fin, 'merged' if '/merged/' in f else 'not merged'))
if '--md' in sys.argv:
    print('| Month | Entries | Reader\'s links | Links after the audit | Links taken out of the tree | Other changes (hours, Checks, notes) | State |')
    print('|---|---|---|---|---|---|---|')
    for m, n, rd, fin, st in rows:
        print(f"| {m} | {n} | {rd[0] if rd else '?'} | {fin[0]} | {fin[1]} | {fin[2]} | {st} |")
    print(f"| {len(rows)} months | {sum(r[1] for r in rows)} | {sum(r[2][0] for r in rows if r[2])} | {sum(r[3][0] for r in rows)} | {sum(r[3][1] for r in rows)} | {sum(r[3][2] for r in rows)} | |")
else:
    for m, n, rd, fin, st in rows:
        print(m, n, rd[0] if rd else '?', fin[0], fin[1], fin[2], st, sep='\t')
