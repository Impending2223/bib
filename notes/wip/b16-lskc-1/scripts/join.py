import sys, yaml, importlib.util, glob, os
d=sys.argv[1]; out=sys.argv[2]
adds=[]; rest=[]
for f in sorted(glob.glob(os.path.join(d,'y*.py'))):
    spec=importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for op in m.OPS:
        (adds if 'add' in op else rest).append(op)
doc={'patch':'2026-11-14-b16-lskc-1',
     'by':'Claude (batch 16, reader 4: Lịch sử kháng chiến chống Mỹ, cứu nước, vols. I–III, 1960 to July 1965), Nov. 14, 2026',
     'ops':adds+rest}
class D(yaml.SafeDumper): pass
def strrep(dumper, s):
    style="'" if (': ' in s or ' #' in s or s[:1] in "*['\"&!%@`{|>-?," or s!=s.strip() or s.lower() in ('yes','no','true','false','null','on','off') or s[:1].isdigit()) else None
    return dumper.represent_scalar('tag:yaml.org,2002:str', s, style=style)
D.add_representer(str, strrep)
open(out,'w').write(yaml.dump(doc, Dumper=D, allow_unicode=True, sort_keys=False, width=100000, default_flow_style=False))
print(len(adds),'adds',len(rest),'other ops')
