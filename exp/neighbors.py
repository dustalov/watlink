#!/usr/bin/env python

import argparse
from gensim.models.word2vec import Word2Vec
import faiss
from collections import defaultdict
import csv
import numpy as np
import sys

parser = argparse.ArgumentParser(description='Nearest Neighbors.')
parser.add_argument('--w2v', required=True, type=argparse.FileType('rb'))
parser.add_argument('--vectors', default=None, nargs='?', type=argparse.FileType('wb'))
parser.add_argument('-k', nargs='?', type=int, default=10)
args = parser.parse_args()

w2v = Word2Vec.load_word2vec_format(args.w2v, binary=True, unicode_errors='ignore')
w2v.init_sims(replace=True)

print('Using %d word2vec dimensions from "%s".' % (w2v.layer1_size, args.w2v.name), flush=True, file=sys.stderr)

index = faiss.IndexFlatIP(w2v.layer1_size)

index.add(w2v.wv.syn0norm)

hyponyms = defaultdict(set)

Y = []

for row in csv.reader(sys.stdin, delimiter='\t', quoting=csv.QUOTE_NONE):
    if len(row) < 2 or row[0] not in w2v or row[1] not in w2v:
        continue

    hyponyms[row[1]].add(row[0])

    Y.append(w2v[row[1]])

for D, I in zip(*index.search(np.array(Y), 1 + args.k)):
    similar = zip(D.ravel(), I.ravel())

    _, hypernym_id = next(similar)

    hypernym = w2v.wv.index2word[hypernym_id]

    for similarity, neighbor_id in similar:
        neighbor = w2v.wv.index2word[neighbor_id]

        for hyponym in hyponyms[hypernym] - hyponyms[neighbor] - {hypernym, neighbor}:
            print('\t'.join((hyponym, neighbor, str(similarity))))

            if args.vectors:
                vectors = np.concatenate((w2v[hyponym], w2v[neighbor]))
                np.savetxt(args.vectors, vectors.reshape(1, w2v.layer1_size * 2))
