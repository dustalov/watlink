export LANG:=en_US.UTF-8
export SHELL:=/bin/bash

FAISS:=dcd83f95b9e091ec1972f48ec5e9ebf457f31612

faiss.py: faiss.tar.gz
	rm -rf faiss-$(FAISS)
	tar zxf $<
	patch -d faiss-$(FAISS) example_makefiles/makefile.inc.Linux -i ../python3-faiss.patch -o makefile.inc
	$(MAKE) -j$$(nproc) -C faiss-$(FAISS) all py
	mv -fv faiss-$(FAISS)/{faiss.py,swigfaiss.py,_swigfaiss.so} .

faiss.tar.gz:
	curl -sLo '$@' 'https://github.com/facebookresearch/faiss/archive/$(FAISS).tar.gz'

clean:
	rm -rf faiss* swig* _swig* __pycache__
