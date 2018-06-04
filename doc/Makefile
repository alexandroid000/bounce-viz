all: \
    wafr_paper.pdf

%.pdf: %.tex
	pdflatex $<
	bibtex $*
	pdflatex $<
	pdflatex $<
