#!/usr/bin/env python

import argparse
import csv
import numpy as np
import sys

parser = argparse.ArgumentParser(description='Expansion.')
parser.add_argument('-d', default=1, nargs='?', type=float)
parser.add_argument('--vectors', type=argparse.FileType('rb'))
parser.add_argument('--predicted', type=argparse.FileType('rb'))
args = parser.parse_args()

vectors, predicted = np.loadtxt(args.vectors), np.loadtxt(args.predicted)

distances = np.apply_along_axis(np.linalg.norm, 1, vectors[:, vectors.shape[1]//2:] - predicted)

reader = csv.reader(sys.stdin, delimiter='\t', quoting=csv.QUOTE_NONE)

for i, (hyponym, hypernym, similarity) in enumerate(reader):
    if distances[i] < args.d:
        print('\t'.join((hyponym, hypernym, similarity)))
