export LANG:=en_US.UTF-8
export LC_COLLATE:=C

data-ru:
	$(MAKE) -C data ru

data-en:
	$(MAKE) -C data en
