#!/bin/bash -ex
export LANG=en_US.UTF-8 LC_COLLATE=C

DATA=$(find data/ru -regex '^.*\(patterns-limit\|wiktionary\|mas\|joint\).*-isas\.txt$')

DENSE=$(find data/konvens2018/ru -name '*.csv')

WEIGHT=tfidf

#rm -rfv "eval/konvens2018-ru"

#mkdir -p "eval/konvens2018-ru"

#for SYNSETS in deps/watset/data/ru/{rwn,ruthes}-synsets.tsv data/watset/eval/ru/w2v/watset-cw-nolog-mcl-synsets.tsv; do

#for ISAS in $DATA; do

  #LINKED=$(basename "${SYNSETS%-synsets.tsv}")-$(basename "${ISAS%-isas.txt}")-$WEIGHT-linked.tsv
  #./link.py --synsets=$SYNSETS --isas=$ISAS --weight=$WEIGHT | sort -t $'\t' -k2nr -k4nr -k1n -o "$LINKED"

  #ISAS=${LINKED%-linked.tsv}-isas.txt
  #./linked-isas.awk "$LINKED" > "$ISAS"

  #SENSEGRAM=${LINKED%-linked.tsv}-sensegram.tsv
  #./linked-sensegram.awk "$LINKED" > "$SENSEGRAM"

  #mv -fv "$LINKED" "$ISAS" "$SENSEGRAM" "eval/konvens2018-ru"

#done

#done

eval/pathwise.py --gold=data/ru/rwn-isas.txt data/ru/patterns-isas.txt $DATA $DENSE eval/konvens2018-ru/*-isas.txt | tee pathwise-konvens2018-ru-rwn.tsv | sort -t $'\t' -g -k9r | column -t

eval/pathwise.py --gold=data/ru/ruthes-isas.txt data/ru/patterns-isas.txt $DATA $DENSE eval/konvens2018-ru/*-isas.txt | tee pathwise-konvens2018-ru-ruthes.tsv | sort -t $'\t' -g -k9r | column -t
