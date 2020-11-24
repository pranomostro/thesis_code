#!/usr/bin/python3

import re
import sys
import pickle

import xml.dom.minidom as xmd
from collections import OrderedDict

_, program = sys.argv

victimindex=dict()
killerindex=dict()

faultmatrix=OrderedDict()

f=open("./{}-tests.txt".format(program))
i=1
for case in f:
	killerindex[case.replace('\n', '')]=i
	i=i+1

for j in range(1, i):
	try:
		faultmatrix[j]
	except:
		faultmatrix[j]=set()

victimcounter=1

f.close()

doc=xmd.parse("./mutations.xml")

for p in doc.firstChild.getElementsByTagName("mutation"):
	try:
		killers=p.getElementsByTagName("killingTests")[0].firstChild.nodeValue.split("|")
	except:
		continue
	killers=[re.search("^([_A-Za-z0-9]+\.)+", k).group() for k in killers]
	killers=[re.sub("\.$", "", k) for k in killers]
	victim=p.getElementsByTagName("mutatedClass")[0].firstChild.nodeValue
	try:
		victimindex[victim]
	except:
		victimindex[victim]=victimcounter
		victimcounter=victimcounter+1
	for k in killers:
		faultmatrix[killerindex[k]].add(victimindex[victim])

savematrix=dict()

for j in range(1, i):
	savematrix[j]=sorted(list(faultmatrix[j]))

sOut="./fault_matrix_key_tc.pickle"
pickle.dump(savematrix, open(sOut, "wb"))

fmf=open("./fault_matrix.txt".format(program), "w")

for j in range(1, len(faultmatrix)+1):
	fmf.write(" ".join([str(p) for p in savematrix[j]])+"\n")

fmf.close()
