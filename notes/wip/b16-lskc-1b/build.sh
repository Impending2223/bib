#!/bin/bash
cd /home/user/bib
python3 -I notes/wip/b16-lskc-1b/join.py inbox/2026-11-19-b16-lskc-1b.yaml $(ls notes/wip/b16-lskc-1b/ops/*.py | sort)
./bib patch-check inbox/2026-11-19-b16-lskc-1b.yaml > /tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/b16-lskc-1b/pc.txt 2>&1
head -2 /tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/b16-lskc-1b/pc.txt
grep -i "error" /tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/b16-lskc-1b/pc.txt | cut -c1-${W:-300}
