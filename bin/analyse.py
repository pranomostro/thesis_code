import pickle
from os import listdir
from collections import defaultdict

projects=['jsoup_1.13.1', 'commons-collections_4.3', 'commons-math_3.6', 'assertj-core_3.9.1', 'jopt-simple_6', 'commons-lang_3.11']
methods=['ART-D', 'ART-F', 'FAST++', 'FAST-all', 'FAST-CS', 'FAST-pw', 'GA', 'RS']
admetrics=['pTime', 'cTime', 'rTime', 'fdl', 'tsr']
bumetrics=['pTime', 'rTime', 'fdl']

rounds=50

# Project->Method->[pTime, cTime, rTime, fdl, tsr]

adequate=defaultdict()
budget=defaultdict()

for p in projects:
	adequate[p]=defaultdict()
	budget[p]=defaultdict()
	for m in methods:
		adequate[p][m]=defaultdict()
		budget[p][m]=defaultdict()
		for me in range(0, len(admetrics)):
			adequate[p][m][admetrics[me]]=list()
			for i in range(1, 51):
				tadequate=pickle.load(open("./outputAdequate-line/"+p+"/measures/"+m+"-"+str(i)+".pickle", "rb"))
				adequate[p][m][admetrics[me]].append(tadequate[me])
		for me in range(0, len(bumetrics)):
			budget[p][m][bumetrics[me]]=list()
			for i in range(1, 51):
				tbudget=pickle.load(open("./outputBudget-line/"+p+"/measures/"+m+"-1-"+str(i)+".pickle", "rb"))
				budget[p][m][bumetrics[me]].append(tbudget[me])

#addescriptive=defaultdict()
#budescriptive=defaultdict()
#
#for m in methods:
#	addescriptive[m]=defaultdict()
#	budescriptive[m]=defaultdict()
#	for p in projects:
