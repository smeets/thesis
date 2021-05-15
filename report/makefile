.PHONY: report
.DEFAULT: report

SOURCES = report.tex                    \
	abstract.tex      popsci.tex      \
	introduction.tex  background.tex  \
	previous_work.tex methodology.tex \
	results.tex       conclusion.tex

tmp:
	mkdir tmp

report: tmp $(SOURCES)
	pdflatex -output-directory=tmp report.tex
	bibtex tmp/report
	pdflatex -output-directory=tmp report.tex
	pdflatex -output-directory=tmp report.tex
	cp tmp/report.pdf report.pdf
