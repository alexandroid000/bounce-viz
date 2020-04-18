all: \
    wafr_paper.pdf \
    perturbation.pdf \
    iterated_decomp.pdf

%.pdf: %.tex
	pdflatex $<
	bibtex $*
	pdflatex $<
	pdflatex $<

clean:
	rm *.aux *.blg *.log *.out
