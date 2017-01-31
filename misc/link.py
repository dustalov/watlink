#!/usr/bin/env python

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

import argparse
import csv
import sys
import itertools
from collections import defaultdict, Counter
from math import log
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sim
from operator import itemgetter
import concurrent.futures

parser = argparse.ArgumentParser()
parser.add_argument('--synsets', required=True)
parser.add_argument('--isas', required=True)
parser.add_argument('--weight', choices=('tf', 'tfidf'), default='tfidf')
parser.add_argument('-k', nargs='?', type=int, default=6)
args = vars(parser.parse_args())

synsets, index, lexicon = {}, defaultdict(lambda: list()), set()

with open(args['synsets']) as f:
    reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

    for row in reader:
        synsets[int(row[0])] = [word for word in row[2].split(', ') if word]

        for word in synsets[int(row[0])]:
            index[word].append(int(row[0]))

        lexicon.update(synsets[int(row[0])])

index = {word: {id: i + 1 for i, id in enumerate(ids)} for word, ids in index.items()}

isas = defaultdict(lambda: set())

with open(args['isas']) as f:
    reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    for hyponym, hypernym in reader:
        if hyponym in lexicon and hypernym in lexicon:
            isas[hyponym].add(hypernym)

idf, D = defaultdict(lambda: 0), .0

for words in synsets.values():
    hypernyms = [isas[word] for word in words if word in isas]

    if not hypernyms:
        continue

    for hypernym in set.union(*hypernyms):
        idf[hypernym] += 1

    D += 1

idf = {hypernym: log(D / df) for hypernym, df in idf.items()}

def tf(w, words):
    return float(Counter(words)[w])

def tfidf(w, words):
    return tf(w, words) * idf.get(w, 1.)

weight = tf if args['weight'] == 'tf' else tfidf

hctx = {}

for id, words in synsets.items():
    hypernyms = list(itertools.chain(*(isas[word] for word in words if word in isas)))

    if not hypernyms:
        continue

    hctx[id] = {word: weight(word, hypernyms) for word in hypernyms}

v = DictVectorizer().fit(hctx.values())

def emit(id):
    if not id in hctx:
        return (id, {})

    hypernyms, vector, hsenses = hctx[id], v.transform(hctx[id]), {}

    for hypernym in hypernyms:
        candidates = {hid: synsets[hid] for hid in index[hypernym]}

        if not candidates:
            continue

        candidates = {hid: {word: weight(word, words) for word in words} for hid, words in candidates.items()}
        candidates = {hid: sim(vector, v.transform(words)) for hid, words in candidates.items()}

        hid, cosine = max(candidates.items(), key=itemgetter(1))

        if cosine > 0:
            hsenses[(hypernym, hid)] = cosine

    hsenses = dict(dict(sorted(hsenses.items(), key=itemgetter(1), reverse=True)[:args['k']]).keys())
    hsenses = {hypernym: hid for hypernym, hid in hsenses.items() if hypernym not in synsets[id]}

    return (id, hsenses)

with concurrent.futures.ProcessPoolExecutor() as executor:
    futures = (executor.submit(emit, id) for id in synsets)

    for i, future in enumerate(concurrent.futures.as_completed(futures)):
        id, hsenses = future.result()

        senses = [(word, index[word][id]) for word in synsets[id]]
        senses_str = ', '.join(('%s#%d' % sense for sense in senses))

        isas = [(word, index[word][hid]) for word, hid in hsenses.items()]
        isas_str = ', '.join(('%s#%d' % sense for sense in isas))

        print('\t'.join((str(id), str(len(synsets[id])), senses_str, str(len(isas)), isas_str)))

        if (i + 1) % 1000 == 0:
            print('%d entries out of %d done.' % (i + 1, len(synsets)), file=sys.stderr, flush=True)

if len(synsets) % 1000 != 0:
    print('%d entries out of %d done.' % (len(synsets), len(synsets)), file=sys.stderr, flush=True)
