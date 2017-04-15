#!/usr/bin/env python

import argparse
import csv
from collections import defaultdict
import sys

REQUIRED = ['INPUT:hyponym',
            'INPUT:hypernym',
            'INPUT:genitive',
            'OUTPUT:judgement']

AGGREGATED  = REQUIRED + ['CONFIDENCE:judgement']

ASSIGNMENTS = REQUIRED + ['GOLDEN:judgement',
                          'HINT:text',
                          'ASSIGNMENT:link',
                          'ASSIGNMENT:assignment_id',
                          'ASSIGNMENT:worker_id',
                          'ASSIGNMENT:status',
                          'ASSIGNMENT:started']

parser = argparse.ArgumentParser()
parser.add_argument('--assignments', action='store_true')
parser.add_argument('path', nargs='+', type=argparse.FileType('r', encoding='UTF-8'))
args = parser.parse_args()

records, hypernyms = defaultdict(list), defaultdict(set)

for file in args.path:
    reader = csv.DictReader(file, delimiter='\t', quoting=csv.QUOTE_NONE)

    for row in reader:
        if set(row.values()) == {''}:
            continue

        if not all(field in row.keys() and row[field] for field in REQUIRED):
            print('Warning: possibly misformatted file "%s".' % (file.name), file=sys.stderr)
            print(row, file=sys.stderr)
            continue

        hyponym, hypernym, genitive = row['INPUT:hyponym'], row['INPUT:hypernym'], row['INPUT:genitive']

        hypernyms[(hyponym, genitive)].update({hypernym for hypernym in row['INPUT:hypernym'].split(', ')})

        records[(hyponym, genitive)].append(row)

print('\t'.join(ASSIGNMENTS if args.assignments else AGGREGATED))

for (hyponym, genitive), rows in sorted(records.items()):
    if args.assignments:
        for row in rows:
            print('\t'.join((
                hyponym,
                ', '.join(sorted(hypernyms[(hyponym, genitive)])),
                genitive,
                row['OUTPUT:judgement'],
                row['GOLDEN:judgement'],
                row['HINT:text'],
                row['ASSIGNMENT:link'],
                row['ASSIGNMENT:assignment_id'],
                row['ASSIGNMENT:worker_id'],
                row['ASSIGNMENT:status'],
                row['ASSIGNMENT:started']
            )))
    else:
        judgement, confidence = max((row['OUTPUT:judgement'], float(row['CONFIDENCE:judgement'][:-1])) for row in rows)

        print('\t'.join((
            hyponym,
            ', '.join(hypernyms[(hyponym, genitive)]),
            genitive,
            judgement,
            '%.2f%%' % confidence)
        ))
