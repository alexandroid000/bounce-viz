all: \
    ijrr.pdf \

%.pdf: %.tex
	pdflatex -shell-escape -interaction nonstopmode  $*
	bibtex $*
	pdflatex -shell-escape -interaction nonstopmode $*
	pdflatex -shell-escape -interaction nonstopmode $*

clean:
	rm *.aux *.blg *.log *.out
