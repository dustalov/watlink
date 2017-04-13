#!/usr/bin/env python

import argparse
from gzip import GzipFile
import csv
from gensim.models.word2vec import Word2Vec
import numpy as np
import sys

parser = argparse.ArgumentParser(description='Expansion.')
parser.add_argument('-d', default=1, nargs='?', type=float)
parser.add_argument('--w2v', required=True, type=argparse.FileType('rb'))
parser.add_argument('--predicted', type=argparse.FileType('rb'))
parser.add_argument('--gzip', default=False, action='store_true')
args = parser.parse_args()

def predictions(f):
    i = 0

    while True:
        try:
            for Y_hat in np.load(f):
                yield Y_hat
            i += 1
        except OSError:
            break

    print('%d slices passed' % i, flush=True, file=sys.stderr)

w2v = Word2Vec.load_word2vec_format(args.w2v, binary=True, unicode_errors='ignore')
w2v.init_sims(replace=True)

print('Using %d word2vec dimensions from "%s".' % (w2v.layer1_size, args.w2v.name), flush=True, file=sys.stderr)

with args.predicted if not args.gzip else GzipFile(fileobj=args.predicted, mode='rb') as f:
    Y_hat_all = predictions(f)

    reader = csv.reader(sys.stdin, delimiter='\t', quoting=csv.QUOTE_NONE)

    for i, (hyponym, hypernym, similarity) in enumerate(reader):
        Y_hat = next(Y_hat_all)

        distance = np.linalg.norm(w2v[hypernym] - Y_hat)

        if distance < args.d:
            print('\t'.join((hyponym, hypernym, similarity)))
