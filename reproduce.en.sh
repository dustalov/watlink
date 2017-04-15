#!/bin/bash -ex
export LANG=en_US.UTF-8 LC_COLLATE=C

DATA=$(find data/en -regex '^.*\(patterns\|wiktionary\|joint\).*-isas\.txt$')

rm -rfv eval/en

for WEIGHT in tf idf tfidf; do

mkdir -p "eval/en/$WEIGHT"

for SYNSETS in data/en/*-synsets.tsv; do

for ISAS in $DATA; do

  if [ ! -f "$ISAS" ]; then
    continue
  fi

  LINKED=$(basename "${SYNSETS%-synsets.tsv}")-$(basename "${ISAS%-isas.txt}")-linked.tsv
  ./link.py --synsets=$SYNSETS --isas=$ISAS --weight=$WEIGHT | sort -t $'\t' -k2nr -k4nr -k1n -o "$LINKED"

  ISAS=${LINKED%-linked.tsv}-isas.txt
  ./linked-isas.awk "$LINKED" > "$ISAS"

  mv -fv "$LINKED" "$ISAS" "eval/en/$WEIGHT"

done

done

done

eval/pathwise.py --gold=data/en/wordnet-isas.txt $DATA eval/en/**/*-isas.txt | tee pathwise-en-wordnet.tsv | sort -t $'\t' -g -k9r | column -t
