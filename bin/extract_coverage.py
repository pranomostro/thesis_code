#!/usr/bin/python3

import re
import sys
import pickle
import json

from collections import OrderedDict

def setoflines(s, pl):
	"""Argument: string describing the range, and lines preceding
	the file in which this is situated."""
	lines=set()
	for ul in s.split(","):
		if len(ul.split("-"))==1:
			lines.add(int(ul)+pl)
		else:
			lo=int(ul.split("-")[0])+pl
			hi=int(ul.split("-")[1])+pl
			lines=lines.union(set(range(lo, hi+1)))
	return lines

_, program = sys.argv

testindex=dict()
linescovered=dict()
linespreceding=dict()

f=open("./{}-tests.txt".format(program))
i=1
for case in f:
	testindex[case.replace('\n', '')]=i
	i=i+1

for j in range(1, i):
	try:
		linescovered[j]
	except:
		linescovered[j]=set()

ld=open("./source-lines.txt")
total=0
for l in ld:
	nol=int(l.split(" ")[0])
	fn=l.split(" ")[1].replace('\n', '')
	linespreceding[fn]=total
	total=total+nol

cov=open("./coverage.json")
jsondata=json.load(cov)

cov.close()
f.close()
ld.close()

for t in jsondata["tests"]:
	try:
		test=re.search("^([_A-Za-z1-9]+(\.|$))+", t["uniformPath"]).group()
		test=re.sub("\.$", "", test)
	except:
		continue
	for p in t["paths"]:
		for f in p["files"]:
			try:
				l=f["coveredLines"]
				preceding=linespreceding[p["path"]+"/"+f["fileName"]]
				ti=testindex[test]
				linescovered[ti]=linescovered[ti].union((setoflines(l, preceding)))
			except:
				continue

coverageinfo=dict()

for j in range(1, i):
	coverageinfo[j]=sorted(list(linescovered[j]))

covf=open("./{}-line.txt".format(program), "w")

for j in range(1, len(coverageinfo)+1):
	covf.write(" ".join([str(p) for p in coverageinfo[j]])+"\n")

covf.close()
