#!/usr/bin/env python

import argparse
import csv
from gensim.models.word2vec import Word2Vec
import numpy as np
import sys

parser = argparse.ArgumentParser(description='Expansion.')
parser.add_argument('-d', default=1, nargs='?', type=float)
parser.add_argument('--w2v', required=True, type=argparse.FileType('rb'))
parser.add_argument('--predicted', type=argparse.FileType('rb'))
args = parser.parse_args()

w2v = Word2Vec.load_word2vec_format(args.w2v, binary=True, unicode_errors='ignore')
w2v.init_sims(replace=True)

print('Using %d word2vec dimensions from "%s".' % (w2v.layer1_size, args.w2v.name), flush=True, file=sys.stderr)

Y_hat_all = np.load(args.predicted)['Y_hat_all']

reader = csv.reader(sys.stdin, delimiter='\t', quoting=csv.QUOTE_NONE)

for i, (hyponym, hypernym, similarity) in enumerate(reader):
    distance = np.linalg.norm(w2v[hypernym] - Y_hat_all[i])

    if distance < args.d:
        print('\t'.join((hyponym, hypernym, similarity)))
