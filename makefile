include config.mk

all: empirical_evaluation_of_test_suite_reduction_regenfuss_2021.pdf

empirical_evaluation_of_test_suite_reduction_regenfuss_2021.pdf: empirical_evaluation_of_test_suite_reduction_regenfuss_2021.tex
	latex empirical_evaluation_of_test_suite_reduction_regenfuss_2021.tex
	bibtex empirical_evaluation_of_test_suite_reduction_regenfuss_2021.aux
	latex empirical_evaluation_of_test_suite_reduction_regenfuss_2021.tex
	pdflatex empirical_evaluation_of_test_suite_reduction_regenfuss_2021.tex

clean:
	rm -f *.aux *.bbl *.bcf *.blg *.dvi *.log *.run.xml *.toc *.nav *.out *.snm

.PHONY: clean arbeit presentation
