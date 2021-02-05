import importlib
import matplotlib.pyplot as plt

f=open("/home/adrian/bachelor/code/bin/analyse.py")
source=f.read()
exec(source)
f.close()

tsrs=[]
for k in adequate.keys():
	tsrs.append([100*x for x in adequate[k]['tsr']])

fig, ax = plt.subplots(figsize = (8,5), sharex = True)
ax.set_ylim(0, 100)
ax.boxplot(tsrs, labels=adequate.keys())
plt.xticks(rotation=90)
plt.tight_layout()

plt.savefig("tsrs.png")

fdls=[]
lbls=[]
for k in adequate.keys():
	fdls.append([100*x for x in adequate[k]['fdl']])
	fdls.append([100*x for x in budget[k]['fdl']])
	lbls.append(k+' (adequate)')
	lbls.append(k+' (budget)')

fig, ax = plt.subplots(figsize = (8,5), sharex = True)
plt.xticks(rotation=90)
ax.set_ylim(0, 100)
ax.boxplot(fdls, labels=lbls)
plt.tight_layout()

plt.savefig("fdls.png")
