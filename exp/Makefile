export LANG:=en_US.UTF-8
export LC_COLLATE:=C

expand:
	./expand.sh ../data/ru/{patterns-limit,wiktionary,mas}-isas.txt 2>&1 | tee expand.log
	cat ../data/ru/joint-isas.txt {patterns-limit,wiktionary,mas}-exp-delta.txt >joint-exp-isas.txt

clean:
	rm -fv *-{knn,delta,isas}.txt *.npy *.npy.gz
