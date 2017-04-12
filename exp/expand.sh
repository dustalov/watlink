#!/bin/bash -ex
export LANG=en_US.UTF-8 LC_COLLATE=C

CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

W2V=all.norm-sz500-w10-cb0-it3-min5.w2v

CLUSTERS=20170122-russian/sz500-k20-l1.0

MODEL=regularized_hyponym

DELTA=0.7

PYTHONPATH=$CWD/../../faiss $CWD/neighbors.py < $CWD/../../watset/misc/mas-isas.txt > $CWD/neighbors.txt \
  --w2v=$CWD/../../projlearn/$W2V \
  --vectors=$CWD/vectors.txt \

$CWD/../../projlearn/predict.py < $CWD/vectors.txt > $CWD/predicted.txt \
  --kmeans=$CWD/../../projlearn/$CLUSTERS/kmeans.pickle \
  --model=$MODEL \
  --path=$CWD/../../projlearn/$CLUSTERS

$CWD/threshold.py -d $DELTA < $CWD/neighbors.txt > $CWD/expand.txt \
  --vectors=$CWD/vectors.txt \
  --predicted=$CWD/predicted.txt
