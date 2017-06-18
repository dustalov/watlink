export LANG:=en_US.UTF-8
export LC_COLLATE:=C

data: data-ru data-en

data-ru:
	$(MAKE) -C data ru

data-en:
	$(MAKE) -C data en
