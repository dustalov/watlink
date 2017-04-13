export LANG:=en_US.UTF-8
export LC_COLLATE:=C
export SHELL:=/bin/bash

all: raw gold misc

raw: patterns wiktionary joint

patterns: en_ps59g-rnk3-min100-nomwe-39k.csv
	tr ' ' '_' < en_ps59g-rnk3-min100-nomwe-39k.csv | sort --parallel=$$(nproc) -t$$'\t' -S1G -k3,3nr -k1,1 -s >patterns-isas.txt

en_ps59g-rnk3-min100-nomwe-39k.csv:
	curl -sLO 'http://panchenko.me/data/joint/isas/en_ps59g-rnk3-min100-nomwe-39k.csv'

wiktionary: enwiktionary-20170201.tsv
	../wiktionary-isas.awk -v RELATION=HYPERNYM enwiktionary-20170201.tsv >wiktionary-isas.txt

enwiktionary-20170201.tsv:
	curl -sLO 'http://depot.nlpub.ru/wiktionary/enwiktionary-20170201.tsv'

joint: patterns wiktionary
	cat {patterns,wiktionary}-isas.txt >joint-isas.txt

gold: wordnet

wordnet: wordnet-hypernyms-binary.csv.gz
	zcat wordnet-hypernyms-binary.csv.gz > wordnet-hypernyms-binary.csv

wordnet-hypernyms-binary.csv.gz:
	curl -sLO 'http://panchenko.me/data/joint/watset/en/wordnet-hypernyms-binary.csv.gz'

misc: lexicon

lexicon:
	awk -F $$'\t' '{print $$1; print $$2}' ../../../watset/data/en/edges.count.txt > lexicon.txt

clean:
	rm -fv lexicon.txt *-isas.txt *.csv *.gz *.tsv
