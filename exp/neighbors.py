#!/usr/bin/env python

import argparse
from gensim.models.word2vec import Word2Vec
import csv
from collections import defaultdict
import numpy as np
import sys

parser = argparse.ArgumentParser(description='Prediction.')
parser.add_argument('--w2v', required=True, type=argparse.FileType('rb'))
parser.add_argument('--faiss', required=True)
parser.add_argument('--vectors', default=None, nargs='?', type=argparse.FileType('wb'))
parser.add_argument('-k', nargs='?', type=int, default=10)
parser.add_argument('subsumptions', type=argparse.FileType('r', encoding='UTF-8'))
args = parser.parse_args()

sys.path.append(args.faiss)
import faiss

w2v = Word2Vec.load_word2vec_format(args.w2v, binary=True, unicode_errors='ignore')
w2v.init_sims(replace=True)

print('Using %d word2vec dimensions from "%s".' % (w2v.layer1_size, args.w2v.name), flush=True, file=sys.stderr)

index = faiss.IndexFlatIP(w2v.layer1_size)

index.add(w2v.wv.syn0norm)

hyponyms = defaultdict(set)

X = []

for row in csv.reader(args.subsumptions, delimiter='\t', quoting=csv.QUOTE_NONE):
    if len(row) < 2:
        continue

    print('\t'.join((row[0], row[1], '1')))

    if row[0] not in w2v or row[1] not in w2v:
        continue

    hyponyms[row[1]].add(row[0])

    X.append(w2v[row[1]])

for D, I in zip(*index.search(np.array(X), args.k + 1)):
    for n, (d, i) in enumerate(zip(D.ravel(), I.ravel())):
        hypernym = w2v.wv.index2word[i]

        if n > 0:
            for hyponym in hyponyms[hypernym]:
                print('\t'.join((hyponym, hypernym, str(d))))
