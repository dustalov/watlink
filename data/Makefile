export LANG:=en_US.UTF-8
export LC_COLLATE:=C

.PHONY: ru en

ru:
	$(MAKE) -C ru all

en:
	$(MAKE) -C en all

watset: watset-acl2017
	ln -sfT $< $@
	touch $< $@

watset-acl2017: watset-acl2017.tar.xz
	tar Jxfv $<

watset-acl2017.tar.xz:
	curl -sLO 'https://github.com/dustalov/watset/releases/download/v1.0/watset-acl2017.tar.xz'

clean:
	$(MAKE) -C ru clean
	$(MAKE) -C en clean
	rm -fv *.txt
