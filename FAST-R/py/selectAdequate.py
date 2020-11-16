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

def printSelectedTestCases(prog, v, method, sel, pTime, cTime, rTime):
	print(method, ptime, cTime, rTime)
	fileListFile="input/{}_{}/{}-tests.txt".format(prog, v, prog)
	testFiles = [line.rstrip("\n") for line in open(fileListFile)]
	for i in sel:
		print("\t" + format(testFiles[i-1]))

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
	printSelectedTestCases(prog, v, "FAST++", sel, pTime, cTime, rTime)

	pTime, cTime, rTime, sel = fastr_adequate.fastCS(inputFile, wBoxFile, dim=dim)
	printSelectedTestCases(prog, v, "FAST-CS", sel, pTime, cTime, rTime)

	pTime, cTime, rTime, sel = fastr_adequate.fast_pw(inputFile, wBoxFile, r=r, b=b, bbox=True, k=k, memory=True)
	printSelectedTestCases(prog, v, "FAST-pw", sel, pTime, cTime, rTime)

	sTime, cTime, pTime, sel = fastr_adequate.fast_(inputFile, wBoxFile, all_, r=r, b=b, bbox=True, k=k, memory=True)
	printSelectedTestCases(prog, v, "FAST-f", sel, pTime+sTime, cTime, 0.0)

	pTime, rTime, sel = competitors.gaAdequacy(wBoxFile)
	printSelectedTestCases(prog, v, "GA", sel, ptime, 0.0, rTime)

	pTime, rTime, sel = competitors.artdAdequacy(wBoxFile)
	printSelectedTestCases(prog, v, "ARTD", sel, pTime, 0.0, rTime)

	pTime, rTime, sel = competitors.artfAdequacy(wBoxFile)
	printSelectedTestCases(prog, v, "ARTF", sel, pTime, 0.0, rTime)
