import re, sys
src, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
pat = re.compile(sys.argv[4]) if len(sys.argv) > 4 else re.compile(r"\d{1,2}-\d{1,2}-19(6[89]|70)|\b(tháng|Tháng) \d{1,2}(-\d{1,2})?-19(6[89])|(ngày|Ngày) \d{1,2}(-\d{1,2})?\b|đêm \d|cuối năm 1968|đầu năm 1969|mùa xuân 1969|Xuân 1969")
for line in open(src):
    m = re.match(r"\[p(\d+)\] (.*)", line)
    if not m: continue
    p = int(m.group(1))
    if p < lo or p > hi: continue
    for s in re.split(r"(?<=[.;!?])\s+(?=[A-ZĐÀ-ỹ_\-\d])", m.group(2)):
        if pat.search(s): print(f"{p}: {s.strip()}")
