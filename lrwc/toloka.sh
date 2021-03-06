#!/bin/bash -ex
export LANG=en_US.UTF-8 LC_COLLATE=C

ISAS="../data/ru/ruthes-isas.txt \
../data/ru/rwn-n-isas.txt \
../data/ru/patterns-isas.txt \
../data/ru/patterns-limit-isas.txt \
../data/ru/wiktionary-isas.txt \
../data/ru/mas-isas.txt \
../data/ru/joint-isas.txt \
patterns-limit-exp-isas.txt \
wiktionary-exp-isas.txt \
mas-exp-isas.txt \
joint-exp-isas.txt \
watset-cw-nolog-mcl-wiktionary-isas.txt \
watset-cw-nolog-mcl-wiktionary-exp-isas.txt \
watset-cw-nolog-mcl-joint-exp-isas.txt \
watset-cw-nolog-mcl-joint-isas.txt"

SKIP=0
STEP=100
WORDS=300

TRAIN_SEED=1337
TRAIN_SKIP=300
TRAIN_HITS=50

# Actual HIT

./freqrncs.py --freq=../data/ru/freqrnc2012.csv --skip=$SKIP -n=$WORDS $ISAS > isa-$WORDS-hit.tsv

./genitives.py < isa-$WORDS-hit.tsv > gent-isa-$WORDS-hit.tsv

./toloka.awk gent-isa-$WORDS-hit.tsv > toloka-isa-$WORDS-hit.tsv

for i in $(seq $STEP $STEP $WORDS); do
  OFFSET=$((SKIP+i-STEP))

  ./freqrncs.py --freq=../data/ru/freqrnc2012.csv --skip=$OFFSET -n=$STEP $ISAS > isa-$WORDS-pool-$i-hit.tsv

  ./genitives.py < isa-$WORDS-pool-$i-hit.tsv > gent-isa-$WORDS-pool-$i-hit.tsv

  ./toloka.awk gent-isa-$WORDS-pool-$i-hit.tsv > toloka-isa-$WORDS-pool-$i-hit.tsv
done

md5sum <(./toloka.awk gent-isa-$WORDS-pool-*-hit.tsv) toloka-isa-$WORDS-hit.tsv

# Training HIT

./freqrncs.py --freq=../data/ru/freqrnc2012.csv --skip=$TRAIN_SKIP -n=$TRAIN_HITS $ISAS > isa-$TRAIN_HITS-skip-$TRAIN_SKIP-train-hit.tsv

./genitives.py < isa-$TRAIN_HITS-skip-$TRAIN_SKIP-train-hit.tsv > gent-isa-$TRAIN_HITS-skip-$TRAIN_SKIP-train-hit.tsv

cat <(head -1   gent-isa-$TRAIN_HITS-skip-$TRAIN_SKIP-train-hit.tsv) \
    <(tail -n+2 gent-isa-$TRAIN_HITS-skip-$TRAIN_SKIP-train-hit.tsv |
      shuf --random-source=<(openssl enc -aes-256-ctr -pass "pass:$TRAIN_SEED" -nosalt </dev/zero 2>/dev/null) |
      head "-$TRAIN_HITS") |
./toloka.awk > toloka-isa-$TRAIN_HITS-skip-$TRAIN_SKIP-train-hit.tsv
