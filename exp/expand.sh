#!/bin/bash -ex
export LANG=en_US.UTF-8 LC_COLLATE=C

CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

W2V=all.norm-sz500-w10-cb0-it3-min5.w2v

CLUSTERS=20170122-russian/sz500-k20-l1.0

MODEL=regularized_hyponym

DELTA=0.7

for ISAS in $@; do
  if [ ${ISAS:-13} == "-exp-isas.txt" ]; then
    continue
  fi

  EXPANDED=$(basename "${ISAS%-isas.txt}-exp")

  PYTHONPATH=$CWD/../../faiss $CWD/neighbors.py < "$ISAS" > "$EXPANDED-knn.txt" \
    --w2v="$CWD/../../projlearn/$W2V" \
    --lexicon="lexicon.txt"

  sort -S1G --parallel=$(nproc) -uo "$EXPANDED-knn.txt" "$EXPANDED-knn.txt"

  $CWD/../../projlearn/predict.py "$EXPANDED-hyp.npz.gz" < "$EXPANDED-knn.txt" \
    --w2v="$CWD/../../projlearn/$W2V" \
    --kmeans="$CWD/../../projlearn/$CLUSTERS/kmeans.pickle" \
    --model="$MODEL" \
    --path="$CWD/../../projlearn/$CLUSTERS" \
    --gzip

  $CWD/threshold.py -d "$DELTA" < "$EXPANDED-knn.txt" > "$EXPANDED-delta.txt" \
    --w2v="$CWD/../../projlearn/$W2V" \
    --predicted="$EXPANDED-hyp.npz.gz" \
    --gzip

  cat "$ISAS" "$EXPANDED-delta.txt" > "$EXPANDED-isas.txt"
done