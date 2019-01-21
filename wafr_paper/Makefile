all: \
    wafr_paper_camera_ready.pdf \
    supplementary/wafr_paper.pdf \
    supplementary/perturbation.pdf \
    supplementary/iterated_decomp.pdf

%.pdf: %.tex
	pdflatex -interaction nonstopmode  $*
	bibtex $*
	pdflatex -interaction nonstopmode $*
	pdflatex -interaction nonstopmode $*

clean:
	rm *.aux *.blg *.log *.out
