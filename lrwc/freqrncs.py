#!/usr/bin/env python

import argparse
import csv
from collections import defaultdict
import operator
import sys

from signal import signal, SIGINT
signal(SIGINT, lambda signum, frame: sys.exit(1))

parser = argparse.ArgumentParser()
parser.add_argument('--freq', required=True, type=argparse.FileType('r', encoding='UTF-8'))
parser.add_argument('--pos', default='s')
parser.add_argument('-n', default=300, type=int)
parser.add_argument('-k', default=5, type=int)
parser.add_argument('--skip', default=0, type=int)
parser.add_argument('path', nargs='+', type=argparse.FileType('r', encoding='UTF-8'))
args = parser.parse_args()

def sanitize(s):
    return s.rsplit('#', 1)[0].lower().replace(' ', '_')

reader = csv.DictReader(args.freq, delimiter='\t', quoting=csv.QUOTE_NONE)
freq = {sanitize(row['Lemma']): float(row['Freq']) for row in reader if row['PoS'] == args.pos}

def top(data, n, skip=0, reverse=False):
    head = sorted(data.items(), key=operator.itemgetter(1), reverse=reverse)
    return [word for i, (word, _) in enumerate(head) if i < skip + n and i >= skip]

lexicon = {word: n for n, word in enumerate(top(freq, args.n, args.skip, reverse=True))}

print('\t'.join(('path', 'hyponym', 'found', 'hypernym', 'freq', 'n')))

for path in args.path:
    isas = defaultdict(set)

    record = lambda hypernym: (
        path.name,
        hyponym,
        str(int(hypernym is not None)),
        hypernym if hypernym else '',
        str(freq[hyponym]),
        str(lexicon[hyponym])
    )

    for row in csv.reader(path, delimiter='\t'):
        hyponym, hypernym = sanitize(row[0]), sanitize(row[1])

        if hyponym in lexicon and hyponym != hypernym and not hypernym in isas[hyponym] and len(isas[hyponym]) < args.k:
            print('\t'.join(record(hypernym)))
            isas[hyponym].add(hypernym)

    for hyponym in lexicon:
        for _ in range(len(isas[hyponym]), args.k):
            print('\t'.join(record(None)))
