include config.mk

all: empirical_evaluation_of_static_test_suite_minimization_regenfuss_2021.pdf

empirical_evaluation_of_static_test_suite_minimization_regenfuss_2021.pdf: empirical_evaluation_of_static_test_suite_minimization_regenfuss_2021.tex
	pdflatex empirical_evaluation_of_static_test_suite_minimization_regenfuss_2021.tex

clean:
	rm -f *.aux *.bbl *.bcf *.blg *.dvi *.log *.run.xml *.toc *.nav *.out *.snm

.PHONY: clean arbeit presentation
