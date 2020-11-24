from os import listdir
from os.path import isfile, join

import xml.dom.minidom as xmd

testres = [f for f in listdir("./") if isfile(join("./", f)) and f.startswith("TEST-") and f.endswith(".xml")]

trf=open("test-execution.json", "w")
tnf=open("test-list.json", "w")

trf.write("[\n")
tnf.write("[\n")

for f in testres:
	trf.write("	{\n")
	tnf.write("	{\n")
	doc=xmd.parse(f)
	time=float(doc.firstChild.getAttribute("time"))
	tests=int(doc.firstChild.getAttribute("tests"))
	errors=int(doc.firstChild.getAttribute("errors"))
	skipped=int(doc.firstChild.getAttribute("skipped"))
	failures=int(doc.firstChild.getAttribute("failures"))
	name=doc.firstChild.getAttribute("name")
	result="PASSED"
	if failures>0:
		result="FAILURE"
	trf.write("\t\t\"uniformPath\": \"{}\",\n\t\t\"duration\": {},\n\t\t\"result\": \"{}\"\n".format(name, time, result))
	tnf.write("\t\t\"uniformPath\": \"{}\"\n".format(name))
	if f==testres[-1]:
		trf.write("	}\n")
		tnf.write("	}\n")
	else:
		trf.write("	},\n")
		tnf.write("	},\n")

trf.write("]\n")
tnf.write("]\n")

trf.close()
tnf.close()
