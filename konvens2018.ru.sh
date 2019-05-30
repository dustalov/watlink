#!/bin/bash -ex
export LANG=en_US.UTF-8 LC_COLLATE=C

DATA=$(find data/ru -regex '^.*\(patterns-limit\|wiktionary\|mas\|joint\).*-isas\.txt$')
DENSE=$(find data/konvens2018-new -name '*-s1-hmx20-hc3*.csv' -not -name '*ruthes*')

rm -rfv "eval/konvens2018-ru"
mkdir -p "eval/konvens2018-ru"

for ALL in $DENSE; do

  ONLY=$(basename "${ALL%.csv}-sparse-isas.txt")
  egrep 'from-original-labels$' "$ALL" > "$ONLY"
  mv -fv "$ONLY" "eval/konvens2018-ru"

  ONLY=$(basename "${ALL%.csv}-dense-isas.txt")
  egrep 'from-vector-linkage$' "$ALL" > "$ONLY"
  mv -fv "$ONLY" "eval/konvens2018-ru"

done

eval/pathwise.py --gold=data/ru/rwn-isas.txt data/ru/patterns-isas.txt $DATA $DENSE eval/konvens2018-ru/*-{sparse,dense}-isas.txt | sort -t $'\t' -g -k9r | tee pathwise-konvens2018-ru-rwn.tsv | column -t
