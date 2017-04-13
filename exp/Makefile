export LANG:=en_US.UTF-8
export LC_COLLATE:=C

expand:
	./expand.sh ../data/ru/{patterns-limit,mas}-isas.txt
	cat {patterns-limit,mas}-exp-isas.txt >joint-exp-isas.txt

isas:
	$(MAKE) -C ../data/ru raw misc

clean:
	rm -fv *-{knn,delta,isas}.txt *.npy *.npy.gz
