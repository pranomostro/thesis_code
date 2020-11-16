import re
import sys
import pickle

import xml.dom.minidom as xmd
from collections import OrderedDict

_, program, version = sys.argv

victimindex=dict()
killerindex=dict()

faultmatrix=OrderedDict()

f=open("input/{}_{}/{}-tests.txt".format(program, version, program))
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

doc=xmd.parse("input/{}_{}/mutations.xml".format(program, version))

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

for j in range(1, i-1):
	savematrix[j]=sorted(list(faultmatrix[j]))

print(savematrix)

sOut="input/{}_{}/fault_matrix_key_tc.pickle".format(program, version)
pickle.dump(savematrix, open(sOut, "wb"))
