# usage: pg.sh file line -> page marker before line
awk -v L=$2 'NR<=L && /^@@ /{p=$0} NR==L{print p; exit}' $1
