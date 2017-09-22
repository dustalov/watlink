export LANG:=en_US.UTF-8
export SHELL:=/bin/bash

faiss.py: faiss-master.zip
	rm -rf faiss-master
	unzip faiss-master.zip
	cp -fv faiss-master/example_makefiles/makefile.inc.Linux faiss-master/makefile.inc
	patch -d faiss-master -p0 <python3-faiss.patch
	$(MAKE) -j$$(nproc) -C faiss-master all py
	mv -fv faiss-master/{faiss.py,swigfaiss.py,_swigfaiss.so} .

faiss-master.zip:
	curl -sLo 'faiss-master.zip' 'https://github.com/facebookresearch/faiss/archive/master.zip'

clean:
	rm -rf faiss* swig* _swig* __pycache__
