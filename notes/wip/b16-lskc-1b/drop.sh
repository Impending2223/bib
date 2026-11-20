#!/bin/bash
# drop.sh SLUG... : release the ledger claim and remove the row from ids.tsv
cd /home/user/bib
F=notes/wip/b16-lskc-1b/ids.tsv
for s in "$@"; do
  id=$(awk -F'\t' -v s="$s" '$1==s{print $2}' $F)
  [ -z "$id" ] && { echo "no $s"; continue; }
  ./bib ledger drop 2026-11-19-b16-lskc-1b $id
  grep -v -P "^$s\t" $F > $F.tmp; mv $F.tmp $F
done
