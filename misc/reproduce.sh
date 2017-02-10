#!/bin/bash -ex
export LANG=en_US.UTF-8 LC_COLLATE=C

for WEIGHT in tf idf tfidf; do
for SYNSETS in *-synsets.tsv; do
for ISAS in {patterns,wiktionary,mas}-filter{,-exp}-isas.txt; do
  if [ ! -f "$ISAS" ]; then
    touch "$ISAS"
  fi

  LINKED=${SYNSETS%-synsets.tsv}-${ISAS%-isas.txt}-$WEIGHT-linked.tsv
  ./link.py --synsets=$SYNSETS --isas=$ISAS | sort -t $'\t' -k2nr -k4nr -k1n -o "$LINKED"

  ISAS=${LINKED%-linked.tsv}-isas.txt
  ./linked-isas.awk "$LINKED" > "$ISAS"

  EVALUATE="$EVALUATE $ISAS"
done
done
done

./evaluate.py --gold=ruthes-isas.txt {patterns,wiktionary,mas}{,-exp}-isas.txt $EVALUATE | tee pairwise-ruthes.tsv | sort -t $'\t' -g -k9r | column -t