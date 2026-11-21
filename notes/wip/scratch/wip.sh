#!/bin/bash
# Copy readers' in-progress patches, witness files and by-work edge diffs into notes/wip, commit, push.
cd /home/user/bib || exit 1
for p in inbox/2026-11-2*-*.yaml; do
  n=$(basename "$p" .yaml); n=${n#2026-11-2?-}; D=notes/wip/$n; mkdir -p "$D"; cp "$p" "$D/patch.yaml"
  w=inbox/witnesses/$(basename "$p"); [ -f "$w" ] && cp "$w" "$D/witnesses.yaml"
done
git diff sources/witnesses/by-work/ > notes/wip/by-work-edges.diff
git add notes/wip inbox/new-entries.tsv notes/book-checks
git commit -q -m "WIP: readers' patches in progress (copies under notes/wip; ledger claims); unaudited, unmerged

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01SkuBbnwkyA2qeGBVGj2LDx" && git push -q origin ccr-29ad5edc-peju1y 2>&1 | tail -1
git log --oneline -1
