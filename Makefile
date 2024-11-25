all: doc

doc: main.md style.sty
	@echo "Pandoc step"
	@pandoc main.md -o output.tex --bibliography b.bib --include-in-header=style.sty  --natbib 
	@echo "Bibtex and PDFtex processing.."
	@pdflatex output.tex
	@bibtex output
	@pdflatex output.tex
	@pdflatex output.tex
	@echo "Saving to final.pdf"
	@cp output.pdf final.pdf

clean:
	@rm -f template.pdf
	@rm -f output_document.tex *.aux *.bbl *.log *.pdfsync *.blg
	@latexmk -c -quiet

dev-env:
	@python3 -m venv .venv/
	@echo "Run {source .venv/bin/activate} in shell"