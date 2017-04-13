#!/bin/bash -ex
export LANG=en_US.UTF-8 LC_COLLATE=C

rm -rfv eval/en

for WEIGHT in tf idf tfidf; do

mkdir -p eval/en/$WEIGHT

for SYNSETS in data/en/*-synsets.tsv; do

for ISAS in data/en/{patterns,wiktionary,joint}-isas.txt; do

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

eval/pairwise.py --gold=data/en/wordnet-isas.txt data/en/{patterns,wiktionary,joint}-isas.txt eval/en/**/*-isas.txt | tee pairwise-en-wordnet.tsv | sort -t $'\t' -g -k9r | column -t
