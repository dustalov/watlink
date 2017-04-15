#!/bin/bash -ex
export LANG=en_US.UTF-8 LC_COLLATE=C

DATA=$(find data/ru exp -regex '^.*\(patterns\|wiktionary\|mas\|joint\).*-isas\.txt$')

rm -rfv eval/ru

for WEIGHT in tf idf tfidf; do

mkdir -p "eval/ru/$WEIGHT"

for SYNSETS in data/ru/*-synsets.tsv; do

for ISAS in $DATA; do

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

eval/pathwise.py --gold=data/ru/rwn-isas.txt $DATA eval/ru/**/*-isas.txt | tee pathwise-ru-rwn.tsv | sort -t $'\t' -g -k9r | column -t

eval/pathwise.py --gold=data/ru/ruthes-isas.txt $DATA eval/ru/**/*-isas.txt | tee pathwise-ru-ruthes.tsv | sort -t $'\t' -g -k9r | column -t
