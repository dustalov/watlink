#!/usr/bin/env python3

import argparse
import csv
import sys
from collections import defaultdict

import faiss
import numpy as np
from gensim.models.word2vec import Word2Vec

parser = argparse.ArgumentParser(description='Nearest Neighbors.')
parser.add_argument('--w2v', required=True, type=argparse.FileType('rb'))
parser.add_argument('--lexicon', default=None, type=argparse.FileType('r', encoding='UTF-8'))
parser.add_argument('--closer', default=False, action='store_true')
parser.add_argument('-k', default=10, type=int)
args = parser.parse_args()

if args.lexicon:
    lexicon = {word.rstrip().lower() for word in args.lexicon}

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

    if args.lexicon:
        lexicon.add(row[0])
        lexicon.add(row[1])

for D, I in zip(*index.search(np.array(Y), 1 + args.k)):
    similar = zip(D.ravel(), I.ravel())

    _, hypernym_id = next(similar)

    hypernym = w2v.wv.index2word[hypernym_id]

    for similarity, neighbor_id in similar:
        neighbor = w2v.wv.index2word[neighbor_id]

        if args.lexicon is not None and neighbor not in lexicon:
            continue

        for hyponym in hyponyms[hypernym] - hyponyms[neighbor] - {hypernym, neighbor}:
            if not args.closer or w2v.wv.similarity(hyponym, hypernym) <= w2v.wv.similarity(hyponym, neighbor):
                print('\t'.join((hyponym, neighbor, str(similarity))))
