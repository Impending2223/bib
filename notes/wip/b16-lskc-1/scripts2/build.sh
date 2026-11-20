#!/bin/bash
# build.sh : join all specs into the patch and patch-check it (output in scratch pc.txt)
cd /home/user/bib
python3 -I notes/wip/b16-lskc-1/scripts2/join2.py inbox/2026-11-14-b16-lskc-1.yaml notes/wip/b16-lskc-1/ops/z1960b.py notes/wip/b16-lskc-1/ops/z1961b.py notes/wip/b16-lskc-1/ops/z1962b.py notes/wip/b16-lskc-1/ops/z1963b.py notes/wip/b16-lskc-1/ops/z1964b.py notes/wip/b16-lskc-1/ops/z1965b.py notes/wip/b16-lskc-1/ops/z1966b.py notes/wip/b16-lskc-1/ops/z1967b.py notes/wip/b16-lskc-1/ops/z1968b.py notes/wip/b16-lskc-1/ops/z1960c.py notes/wip/b16-lskc-1/ops/z1969b.py notes/wip/b16-lskc-1/ops/z1970b.py $(ls notes/wip/b16-lskc-1/ops/zz*.py 2>/dev/null)
./bib patch-check inbox/2026-11-14-b16-lskc-1.yaml > /tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/b16-lskc-1/pc.txt 2>&1
head -1 /tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/b16-lskc-1/pc.txt
grep "^  error" /tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/b16-lskc-1/pc.txt | cut -c1-${W:-300}
