#!/bin/bash -ex
export LANG=en_US.UTF-8 LC_COLLATE=C

DATA=$(find data/en -regex '^.*\(patterns\|wiktionary\|joint\).*-isas\.txt$')
DENSE=$(find data/konvens2018/en -name 'wordnet*-s1-hmx15-hc3*.csv' -o -name 'watset-*-s1-hmx20-hc3*.csv')

rm -rfv "eval/konvens2018-en"
mkdir -p "eval/konvens2018-en"

for ALL in $DENSE; do

  ONLY=$(basename "${ALL%.csv}-sparse-isas.txt")
  egrep 'from-original-labels$' "$ALL" > "$ONLY"
  mv -fv "$ONLY" "eval/konvens2018-en"

  ONLY=$(basename "${ALL%.csv}-dense-isas.txt")
  egrep 'from-vector-linkage$' "$ALL" > "$ONLY"
  mv -fv "$ONLY" "eval/konvens2018-en"

done

eval/pathwise.py --gold=data/en/wordnet-isas.txt $DATA $DENSE eval/konvens2018-en/*-{sparse,dense}-isas.txt | sort -t $'\t' -g -k9r | tee pathwise-konvens2018-en-wordnet.tsv | column -t
