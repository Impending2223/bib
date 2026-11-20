#!/bin/bash
# cal.sh SINCE UNTIL [thread...] : one line per calendar entry (id, first 130 chars) for the Vietnam threads
cd /home/user/bib
S=$1; U=$2; shift 2
TH=${@:-vietnam vietnam-operations vietnam-hanoi laos}
for t in $TH; do ./bib find -l cal --thread $t --since $S --until $U | grep -A1 "^cal\." | grep -v "^--" | paste - - | sed -E 's/^(cal[^\t]*)\t +lists\/cal\/[0-9]+\.yaml:[0-9]+ +/\1 | /' | cut -c1-${W:-190}; done | sort -u
