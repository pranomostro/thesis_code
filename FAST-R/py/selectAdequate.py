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
import fastr_adequate
import metric

def dumpSelectedTestCases(prog, v, method, inputFile, sel, scd):
	testCases = [line.rstrip("\n") for line in open(inputFile)]
	selectedCasesFile = open(scd + "/{}.txt".format(method), "w")
	for i in sel:
		selectedCasesFile.write(testCases[i-1]+"\n")
	selectedCasesFile.close()

"""
This file runs all FAST-R algorithms (fastr_adequate.py) and the
competitors (competitors.py) in the Adequate scenario and in all input
test suite, and saves the selected test cases.
"""


usage = """USAGE: python3 py/experimentAdequate.py <coverageType> <program> <version> <repetitions>
OPTIONS:
  <coverageType>: the target coverage criterion.
	options: function, line, branch
  <program> <version>: the target subject and its respective version.
	options: flex v3, grep v3, gzip v1, make v1, sed v6, chart v0, closure v0, lang v0, math v0, time v0"""

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print(usage)
		exit()

	SIR = [("flex", "v3"), ("grep", "v3"), ("gzip", "v1"), ("sed", "v6"), ("make", "v1")]
	D4J = [("math", "v1"), ("closure", "v1"), ("time", "v1"), ("lang", "v1"), ("chart", "v1")]
	script, covType, prog, v = sys.argv

	scd = "selectedAdequate-{}/{}_{}/".format(covType, prog, v)
	if not os.path.exists(scd):
		os.makedirs(scd)

	# FAST parameters
	k, n, r, b = 5, 10, 1, 10
	dim = 10

	# FAST-f sample size
	def all_(x): return x
	def sqrt_(x): return int(math.sqrt(x)) + 1
	def log_(x): return int(math.log(x, 2)) + 1
	def one_(x): return 1

	# BLACKBOX EXPERIMENTS
	javaFlag = True if ((prog, v) in D4J) else False

	inputFile = "input/{}_{}/{}-bbox.txt".format(prog, v, prog)
	wBoxFile = "input/{}_{}/{}-{}.txt".format(prog, v, prog, covType)
	if javaFlag:
		faultMatrix = "input/{}_{}/fault_matrix.txt".format(prog, v)
	else:
		faultMatrix = "input/{}_{}/fault_matrix_key_tc.pickle".format(prog, v)

	outpath = "outputAdequate-{}/{}_{}/".format(covType, prog, v)
	sPath = outpath + "selections/"
	tPath = outpath + "measures/"

	pTime, cTime, rTime, sel = fastr_adequate.fastPlusPlus(inputFile, wBoxFile, dim=dim)
	dumpSelectedTestCases(prog, v, "FAST++", inputFile, sel, scd)

	pTime, cTime, rTime, sel = fastr_adequate.fastCS(inputFile, wBoxFile, dim=dim)
	dumpSelectedTestCases(prog, v, "FAST-CS", inputFile, sel, scd)

	pTime, cTime, rTime, sel = fastr_adequate.fast_pw(inputFile, wBoxFile, r=r, b=b, bbox=True, k=k, memory=True)
	dumpSelectedTestCases(prog, v, "FAST-pw", inputFile, sel, scd)

	sTime, cTime, pTime, sel = fastr_adequate.fast_(inputFile, wBoxFile, all_, r=r, b=b, bbox=True, k=k, memory=True)
	dumpSelectedTestCases(prog, v, "FAST-f", inputFile, sel, scd)

	pTime, rTime, sel = competitors.gaAdequacy(wBoxFile)
	dumpSelectedTestCases(prog, v, "GA", inputFile, sel, scd)

	pTime, rTime, sel = competitors.artdAdequacy(wBoxFile)
	dumpSelectedTestCases(prog, v, "ARTD", inputFile, sel, scd)

	pTime, rTime, sel = competitors.artfAdequacy(wBoxFile)
	dumpSelectedTestCases(prog, v, "ARTF", inputFile, sel, scd)
