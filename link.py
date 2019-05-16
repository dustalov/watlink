#!/usr/bin/env python3

import argparse
import concurrent.futures
import itertools
import sys
from collections import defaultdict, Counter
from signal import signal, SIGINT

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity as sim
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Binarizer

signal(SIGINT, lambda signum, frame: sys.exit(1))

WEIGHT = {
    'tf': TfidfTransformer(use_idf=False),
    'idf': Pipeline([('binary', Binarizer()), ('idf', TfidfTransformer())]),
    'tfidf': TfidfTransformer()
}

parser = argparse.ArgumentParser()
parser.add_argument('--synsets', required=True, type=argparse.FileType('r'))
parser.add_argument('--isas', required=True, type=argparse.FileType('r'))
parser.add_argument('--weight', choices=WEIGHT.keys(), default='tfidf')
parser.add_argument('-k', nargs='?', type=int, default=6)
args = parser.parse_args()

synsets, index, lexicon = {}, defaultdict(list), set()

for line in args.synsets:
    line = line.rstrip()

    if not line:
        continue

    row = line.split('\t')

    synsets[row[0]] = [word for word in row[2].split(', ') if word]

    for word in synsets[row[0]]:
        index[word].append(row[0])

    lexicon.update(synsets[row[0]])

index = {word: {id: i + 1 for i, id in enumerate(ids)} for word, ids in index.items()}

isas = defaultdict(set)

for line in args.isas:
    line = line.rstrip()

    if not line:
        continue

    row = line.split('\t')

    if len(row) > 1 and row[0] in lexicon and row[1] in lexicon:
        isas[row[0]].add(row[1])

hctx = {}

for id, words in synsets.items():
    hypernyms = Counter(itertools.chain(*(isas[word] for word in words if word in isas)))

    if hypernyms:
        hctx[id] = hypernyms

v = Pipeline([('dict', DictVectorizer()), (args.weight, WEIGHT[args.weight])]).fit(hctx.values())


def emit(id):
    if not id in hctx:
        return (id, {})

    hvector, candidates = v.transform(hctx[id]), Counter()

    for hypernym in hctx[id]:
        hsenses = Counter({hid: sim(v.transform(Counter(synsets[hid])), hvector).item(0) for hid in index[hypernym]})

        for hid, cosine in hsenses.most_common(1):
            if cosine > 0:
                candidates[(hypernym, hid)] = cosine

    matches = [(hypernym, hid, cosine) for (hypernym, hid), cosine in
               candidates.most_common(len(candidates) if args.k == 0 else args.k) if hypernym not in synsets[id]]

    return (id, matches)


with concurrent.futures.ProcessPoolExecutor() as executor:
    futures = (executor.submit(emit, id) for id in synsets)

    for i, future in enumerate(concurrent.futures.as_completed(futures)):
        id, matches = future.result()

        senses = [(word, index[word][id]) for word in synsets[id]]
        senses_str = ', '.join(('%s#%d' % sense for sense in senses))

        isas = [(word, index[word][hid], cosine) for word, hid, cosine in matches]
        isas_str = ', '.join(('%s#%d:%.6f' % sense for sense in isas))

        print('\t'.join((str(id), str(len(synsets[id])), senses_str, str(len(isas)), isas_str)))

        if (i + 1) % 1000 == 0:
            print('%d entries out of %d done.' % (i + 1, len(synsets)), file=sys.stderr, flush=True)

if len(synsets) % 1000 != 0:
    print('%d entries out of %d done.' % (len(synsets), len(synsets)), file=sys.stderr, flush=True)
