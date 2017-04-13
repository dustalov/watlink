#!/bin/bash -ex
export LANG=en_US.UTF-8 LC_COLLATE=C

rm -rfv eval/ru

for WEIGHT in tf idf tfidf; do

mkdir -p eval/ru/$WEIGHT

for SYNSETS in data/ru/*-synsets.tsv; do

for ISAS in data/ru/{patterns{,-limit,-filter},wiktionary,mas,joint}-isas.txt; do

  if [ ! -f "$ISAS" ]; then
    continue
  fi

  LINKED=$(basename "${SYNSETS%-synsets.tsv}")-$(basename "${ISAS%-isas.txt}")-linked.tsv
  ./link.py --synsets=$SYNSETS --isas=$ISAS --weight=$WEIGHT | sort -t $'\t' -k2nr -k4nr -k1n -o "$LINKED"

  ISAS=${LINKED%-linked.tsv}-isas.txt
  ./linked-isas.awk "$LINKED" > "$ISAS"

  mv -fv "$LINKED" "$ISAS" "eval/ru/$WEIGHT"

done

done

done

eval/pairwise.py --gold=data/ru/rwn-isas.txt data/ru/{patterns{,-limit,-filter},wiktionary,mas,joint}-isas.txt eval/ru/**/*-isas.txt | tee pairwise-ru-rwn.tsv | sort -t $'\t' -g -k9r | column -t
