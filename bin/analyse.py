import pickle
import statistics
from os import listdir
from collections import defaultdict

projects=['jsoup_1.13.1', 'commons-collections_4.3', 'commons-math_3.6', 'assertj-core_3.9.1', 'jopt-simple_6', 'commons-lang_3.11']
methods=['ART-D', 'ART-F', 'FAST++', 'FAST-all', 'FAST-CS', 'FAST-pw', 'GA', 'RS']
admetrics=['pTime', 'cTime', 'rTime', 'fdl', 'tsr', 'total']
bumetrics=['pTime', 'rTime', 'fdl', 'total']
descstat=[("mean", statistics.mean), ("median", statistics.median), ("stdev", statistics.stdev)]

rounds=50

adequate=defaultdict()
budget=defaultdict()

for m in methods:
	adequate[m]=defaultdict()
	budget[m]=defaultdict()
	for me in range(0, len(admetrics)):
		adequate[m][admetrics[me]]=list()
		for i in range(1, rounds+1):
			for p in projects:
				tadequate=pickle.load(open("./outputAdequate-line/"+p+"/measures/"+m+"-"+str(i)+".pickle", "rb"))
				if admetrics[me]=='total':
					adequate[m][admetrics[me]].append(tadequate[0]+tadequate[1]+tadequate[2])
				else:
					adequate[m][admetrics[me]].append(tadequate[me])
	for me in range(0, len(bumetrics)):
		budget[m][bumetrics[me]]=list()
		for i in range(1, rounds+1):
			for p in projects:
				tbudget=pickle.load(open("./outputBudget-line/"+p+"/measures/"+m+"-1-"+str(i)+".pickle", "rb"))
				if bumetrics[me]=='total':
					budget[m][bumetrics[me]].append(tbudget[0]+tbudget[1]+tbudget[2])
				else:
					budget[m][bumetrics[me]].append(tbudget[me])

addescriptive=defaultdict()
budescriptive=defaultdict()

for m in methods:
	addescriptive[m]=defaultdict()
	budescriptive[m]=defaultdict()
	for me in range(0, len(admetrics)):
		addescriptive[m][admetrics[me]]=defaultdict()
		for d in descstat:
			addescriptive[m][admetrics[me]][d[0]]=d[1](adequate[m][admetrics[me]])
	for me in range(0, len(bumetrics)):
		budescriptive[m][bumetrics[me]]=defaultdict()
		for d in descstat:
			budescriptive[m][bumetrics[me]][d[0]]=d[1](budget[m][bumetrics[me]])
