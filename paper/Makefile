all: \
    	paper.pdf

%.pdf: %.tex
	pdflatex $<
	bibtex $*
	pdflatex $<
