all: \
    wafr_paper.pdf \
    wafr_paper_camera_ready.pdf \
    perturbation.pdf \
    iterated_decomp.pdf

%.pdf: %.tex
	pdflatex -interaction nonstopmode  $*
	bibtex $*
	pdflatex -interaction nonstopmode $*
	pdflatex -interaction nonstopmode $*

clean:
	rm *.aux *.blg *.log *.out
