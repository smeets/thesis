
SOURCES = base.tex                    \
	abstract.tex      popsci.tex      \
	introduction.tex  background.tex  \
	previous_work.tex methodology.tex \
	results.tex       conclusion.tex

.PHONY: report

tmp:
	mkdir tmp

report: tmp $(SOURCES)
	pdflatex -output-directory=.. -aux-directory=tmp base.tex
