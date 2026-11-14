import sys, yaml
out = sys.argv[1]; parts = sys.argv[2:]
ops = []
for p in parts:
    ops += yaml.safe_load(open(p))
doc = {"patch": "2026-11-14-b16-lskc-3",
       "by": "Claude (batch 16, reader 6: Lịch sử kháng chiến chống Mỹ cứu nước, vol. VI, to Dec. 31, 1969), Nov. 14, 2026",
       "ops": ops}
class D(yaml.SafeDumper): pass
def strrep(d, s):
    return d.represent_scalar("tag:yaml.org,2002:str", s, style="'" if any(c in s for c in ":#'\"*[]{}") or s[:1] in "'\"*[&!|>%@`" else None)
D.add_representer(str, strrep)
open(out, "w").write(yaml.dump(doc, Dumper=D, allow_unicode=True, sort_keys=False, width=100000, default_flow_style=False))
print(len(ops), "ops")
