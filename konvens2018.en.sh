#!/bin/bash -ex
export LANG=en_US.UTF-8 LC_COLLATE=C

DATA=$(find data/en -regex '^.*\(patterns\|wiktionary\|joint\).*-isas\.txt$')

WEIGHT=tfidf

rm -rfv "eval/konvens2018-en"

mkdir -p "eval/konvens2018-en"

for SYNSETS in deps/watset/data/en/wordnet-synsets.tsv data/watset/eval/en/w2v/watset-mcl-mcl-synsets.tsv; do

for ISAS in $DATA; do

  LINKED=$(basename "${SYNSETS%-synsets.tsv}")-$(basename "${ISAS%-isas.txt}")-$WEIGHT-linked.tsv
  ./link.py --synsets=$SYNSETS --isas=$ISAS --weight=$WEIGHT | sort -t $'\t' -k2nr -k4nr -k1n -o "$LINKED"

  ISAS=${LINKED%-linked.tsv}-isas.txt
  ./linked-isas.awk "$LINKED" > "$ISAS"

  mv -fv "$LINKED" "$ISAS" "eval/konvens2018-en"

done

done

eval/pathwise.py --gold=data/en/wordnet-isas.txt $DATA eval/konvens2018-en/*-isas.txt | tee pathwise-konvens2018-en-wordnet.tsv | sort -t $'\t' -g -k9r | column -t
