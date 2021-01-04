'''
This is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this source.  If not, see <http://www.gnu.org/licenses/>.
'''

import math
import os
import pickle
import sys

import competitors
import fastr
import metric

def measureTestCaseSelection(prog, v, method, sel, pTime, rTime):
	print(method, pTime, rTime)
	print(sel)
	fileListFile="input/{}_{}/{}-tests.txt".format(prog, v, prog)
	testFiles = [line.rstrip("\n") for line in open(fileListFile)]
	for i in sel:
		print("\t" + format(testFiles[i-1]))

"""
This file runs all FAST-R algorithms (fastr_adequate.py) and the
competitors (competitors.py) in the Budget scenario and in all input
test suite, and saves the selected test cases.
"""


usage = """USAGE: python3 py/experimentBudget.py <coverageType> <program> <version> <budget>
OPTIONS:
  <coverageType>: the target coverage criterion.
	options: function, line, branch
  <program> <version>: the target subject and its respective version.
	options: flex v3, grep v3, gzip v1, make v1, sed v6, chart v0, closure v0, lang v0, math v0, time v0
  <budget>: the number of test cases that can be selected
	options: any natural number"""

if __name__ == "__main__":
	if len(sys.argv) != 5:
		print(usage)
		exit()

	SIR = [("flex", "v3"), ("grep", "v3"), ("gzip", "v1"), ("sed", "v6"), ("make", "v1"), ("commons-lang", "3.11"), ("commons-math", "3.6"), ("jsoup", "1.13.1")]
	D4J = [("math", "v1"), ("closure", "v1"), ("time", "v1"), ("lang", "v1"), ("chart", "v1")]
	script, covType, prog, v, B = sys.argv

	B = int(B)

	scd = "selectedBudget-{}/{}_{}/".format(covType, prog, v)
	if not os.path.exists(scd):
		os.makedirs(scd)

	# FAST-R parameters
	k, n, r, b = 5, 10, 1, 10
	dim = 10

	# FAST-f sample size
	def all_(x): return x
	def sqrt_(x): return int(math.sqrt(x)) + 1
	def log_(x): return int(math.log(x, 2)) + 1
	def one_(x): return 1

	# BLACKBOX
	javaFlag = True if ((prog, v) in D4J) else False

	inputFile = "input/{}_{}/{}-bbox.txt".format(prog, v, prog)
	wBoxFile = "input/{}_{}/{}-{}.txt".format(prog, v, prog, covType)
	if javaFlag:
		faultMatrix = "input/{}_{}/fault_matrix.txt".format(prog, v)
	else:
		faultMatrix = "input/{}_{}/fault_matrix_key_tc.pickle".format(prog, v)

	print(javaFlag)
	print(faultMatrix)

	pTime, rTime, sel = fastr.fastPlusPlus(inputFile, dim=dim, B=B)
	fdl = metric.fdl(sel, faultMatrix, javaFlag)
	measureTestCaseSelection(prog, v, "FAST++", sel, pTime, rTime)

	pTime, rTime, sel = fastr.fastCS(inputFile, dim=dim, B=B)
	measureTestCaseSelection(prog, v, "FAST-CS", sel, pTime, rTime)

	pTime, rTime, sel = fastr.fast_pw(inputFile, r, b, bbox=True, k=k, memory=True, B=B)
	measureTestCaseSelection(prog, v, "FAST-pw", sel, pTime, rTime)

	pTime, rTime, sel = fastr.fast_(inputFile, all_, r=r, b=b, bbox=True, k=k, memory=True, B=B)
	measureTestCaseSelection(prog, v, "FAST-all", sel, pTime, rTime)

	# WHITEBOX APPROACHES
	pTime, rTime, sel = competitors.ga(wBoxFile, B=B)
	rintSelectedTestCases(prog, v, "GA", sel, ptime, rTime)

	pTime, rTime, sel = competitors.artd(wBoxFile, B=B)
	measureTestCaseSelection(prog, v, "ARTD", sel, pTime, rTime)

	pTime, rTime, sel = competitors.artf(wBoxFile, B=B)
	measureTestCaseSelection(prog, v, "ARTF", sel, pTime, rTime)
