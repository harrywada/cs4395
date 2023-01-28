ROFF = groff -k

default: homework00.pdf
clean:
	rm -f homework00.pdf

.SUFFIXES: .mm .pdf
.mm.pdf:
	$(ROFF) -Tpdf -mm $< >$@
