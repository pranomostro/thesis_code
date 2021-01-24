import importlib
import matplotlib.pyplot as plt

f=open("/home/adrian/bachelor/code/bin/analyse.py")
source=f.read()
exec(source)
f.close()

budgetfdls=[]
for k in adequate.keys():
	budgetfdls.append([100*x for x in budget[k]['fdl']])

fig, ax = plt.subplots(figsize = (8,5), sharex = True)
ax.set_ylim(0, 100)
ax.boxplot(budgetfdls, labels=adequate.keys())
plt.xticks(rotation=90)
plt.tight_layout()

plt.savefig("budgetfdls.png")

adeq=[]
lbls=[]
for k in adequate.keys():
	adeq.append([100*x for x in adequate[k]['tsr']])
	adeq.append([100*x for x in adequate[k]['fdl']])
	lbls.append(k+' (TSR)')
	lbls.append(k+' (FDL)')

fig, ax = plt.subplots(figsize = (8,5), sharex = True)
plt.xticks(rotation=90)
ax.set_ylim(0, 100)
ax.boxplot(adeq, labels=lbls)
plt.tight_layout()

plt.savefig("adequatemetrics")
