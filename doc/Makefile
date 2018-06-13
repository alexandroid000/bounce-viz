all: \
    wafr_paper.pdf \
    perturbation.pdf

%.pdf: %.tex
	pdflatex $<
	bibtex $*
	pdflatex $<
	pdflatex $<
