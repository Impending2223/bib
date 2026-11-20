#!/bin/bash
# reclaim.sh SLUG... : release the slug's claimed id and drop the slug from ids.tsv (claim.py then claims again)
cd /home/user/bib
for s in "$@"; do
  id=$(awk -F'\t' -v s="$s" '$1==s{print $2}' notes/wip/b16-lskc-1/scripts2/ids.tsv)
  [ -z "$id" ] && { echo "no $s"; continue; }
  ./bib ledger drop 2026-11-14-b16-lskc-1 "$id"
  sed -i "/^$s\t/d" notes/wip/b16-lskc-1/scripts2/ids.tsv
done
