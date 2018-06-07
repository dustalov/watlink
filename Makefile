export LANG:=en_US.UTF-8
export LC_COLLATE:=C

.PHONY: deps data

deps:
	$(MAKE) -C deps faiss.py

data: data-ru data-en data-watset

data-ru:
	$(MAKE) -C data ru

data-en:
	$(MAKE) -C data en

data-watset:
	$(MAKE) -C data watset
