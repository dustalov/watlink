export LANG:=en_US.UTF-8
export LC_COLLATE:=C

all: gold

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
