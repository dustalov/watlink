export LANG:=en_US.UTF-8
export LC_COLLATE:=C
export SHELL:=/bin/bash

all: raw gold misc

raw: patterns-filter wiktionary mas joint

patterns-filter: patterns lexicon
	../filter.py -1 lexicon.txt < patterns-isas.txt > patterns-filter-isas.txt

patterns: ru-librusec-wiki-diff.csv.gz
	zcat ru-librusec-wiki-diff.csv.gz | tail -n+2 | tr ' ' '_' | sort --parallel=$$(nproc) -t$$'\t' -S1G -k3,3nr -k1,1 -s >patterns-isas.txt
	awk -F'\t' '$$3>=30' patterns-isas.txt | cut -f1,2 > patterns-limit-isas.txt

ru-librusec-wiki-diff.csv.gz:
	curl -sLO 'http://panchenko.me/data/joint/isas/ru-librusec-wiki-diff.csv.gz'

wiktionary: ruwiktionary-20170201.tsv
	../wiktionary-isas.awk -v RELATION=HYPERNYM ruwiktionary-20170201.tsv >wiktionary-isas.txt

ruwiktionary-20170201.tsv:
	curl -sLO 'http://depot.nlpub.ru/wiktionary/ruwiktionary-20170201.tsv'

mas:
	@echo "# Assuming that you have MAS as is-a-rel_MAS.txt."
	./mas-isas.awk is-a-rel_MAS.txt >mas-isas.txt

joint: patterns wiktionary mas
	cat {patterns-limit,wiktionary,mas}-isas.txt >joint-isas.txt

gold: ruthes rwn

ruthes: ruthes.xml
	xsltproc ruthes-isas.xsl ruthes.xml >ruthes-isas.txt

ruthes.xml:
	@echo "# Assuming that you have RuThes in the directory ${CURDIR}/ruthes-v2."
	./ruthes-stub.awk ruthes-v2/*.xml >ruthes.xml

rwn: rwn.xml
	xsltproc rwn-isas.xsl rwn.xml >rwn-isas.txt

rwn.xml:
	@echo "# Assuming that you have RuWordNet in the directory ${CURDIR}/rwn-xml."
	./ruthes-stub.awk -v TAG=rwn rwn-xml/*.*.xml >rwn.xml

misc: lexicon freqrnc2012.csv

lexicon:
	awk -F $$'\t' '{print $$1; print $$2}' ../../../watset/data/ru/edges.count.txt > lexicon.txt

freqrnc2012.csv:
	curl -sLO 'https://hsemysql.wikispaces.com/file/view/freqrnc2012.csv/404746392/freqrnc2012.csv'

clean:
	rm -fv lexicon.txt *-isas.txt *.csv *.gz *.tsv *.xml
