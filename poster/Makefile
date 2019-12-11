all: \
    main.pdf

%.pdf: %.tex
	pdflatex -interaction nonstopmode  $*
	bibtex $*
	pdflatex -interaction nonstopmode $*
	pdflatex -interaction nonstopmode $*

clean:
	rm *.aux *.blg *.log *.out
