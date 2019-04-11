#!/usr/bin/env python3

import argparse
import csv
import sys
from signal import signal, SIGINT

signal(SIGINT, lambda signum, frame: sys.exit(1))

parser = argparse.ArgumentParser()
parser.add_argument('lexicon', type=argparse.FileType('r', encoding='UTF-8'))
parser.add_argument('-1', action='store_true', dest='first')
args = parser.parse_args()

with args.lexicon as f:
    lexicon = {word for word in f.read().splitlines()}

for row in csv.reader(sys.stdin, delimiter='\t'):
    if row[0] in lexicon and (args.first or row[1] in lexicon):
        print('\t'.join((row[0], row[1])))
