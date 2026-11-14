#!/bin/bash
cd /home/user/bib
for id in "$@"; do ./bib show $id 2>&1 | grep -E '^- id:|^  (when|c|n|also|tags):' | cut -c1-${W:-700}; echo; done
