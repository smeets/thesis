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
	bibtex -include-directory=tmp tmp/report
	copy tmp\\report.pdf report.pdf
