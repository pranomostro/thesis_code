import re
import sys

import xml.dom.minidom as xmd
from collections import OrderedDict

program, version = sys.argv

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

doc=xmd.parse("input/{}_{}/mutation.xml".format(program, version))

for p in doc.firstChild.getElementsByTagName("mutation"):
	try:
		killers=p.getElementsByTagName("killingTests")[0].firstChild.nodeValue.split("|")
	except:
		continue
	killers=['.'.join(t.split('.')[0:-1]) for t in killers]
	victim=p.getElementsByTagName("mutatedClass")[0].firstChild.nodeValue
	try:
		victimindex[victim]
	except:
		victimindex[victim]=victimcounter
		victimcounter=victimcounter+1
	for k in killers:
		k=re.sub("\.\[[0-9]+\] .*$", "", k)
		faultmatrix[killerindex[k]].add(victimindex[victim])

for j in range(1, i-1):
	print(' '.join([str(i) for i in list(faultmatrix[j])]))
