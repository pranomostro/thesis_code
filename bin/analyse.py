import pickle
import statistics
from os import listdir
from collections import defaultdict
from scipy import stats

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

adranks=defaultdict() #keys: tsr, fdl, rtime, total
buranks=defaultdict() #keys: fdl, rtime, total

for a in admetrics:
	medians=[addescriptive[m][a]['median'] for m in methods]
	values=[adequate[m][a] for m in methods]
	valuesaftermedians=[v for _,v in sorted(zip(medians,values))]
	methodsaftermedians=[v for _,v in sorted(zip(medians,methods))]
	adranks[a]=defaultdict()
	adranks[a]["medians"]=sorted(medians)
	adranks[a]["methods"]=methodsaftermedians
	adranks[a]["rank"]=[]
	for i in range(0, len(values)-1):
		if valuesaftermedians[i]==valuesaftermedians[i+1]:
			adranks[a]["rank"].append("=")
			continue
		vals=stats.kruskal(valuesaftermedians[i],valuesaftermedians[i+1])
		if vals[1]<0.05:
			adranks[a]["rank"].append(">")
		else:
			adranks[a]["rank"].append("=")

for b in bumetrics:
	medians=[budescriptive[m][b]['median'] for m in methods]
	values=[budget[m][b] for m in methods]
	valuesaftermedians=[v for _,v in sorted(zip(medians,values))]
	methodsaftermedians=[v for _,v in sorted(zip(medians,methods))]
	buranks[b]=defaultdict()
	buranks[b]["medians"]=sorted(medians)
	buranks[b]["methods"]=methodsaftermedians
	buranks[b]["rank"]=[]
	for i in range(0, len(values)-1):
		if valuesaftermedians[i]==valuesaftermedians[i+1]:
			buranks[b]["rank"].append("=")
			continue
		vals=stats.kruskal(valuesaftermedians[i],valuesaftermedians[i+1])
		if vals[1]<0.05:
			buranks[b]["rank"].append(">")
		else:
			buranks[b]["rank"].append("=")
