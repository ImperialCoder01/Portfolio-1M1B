import pandas as pd, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
test=pd.read_pickle("test.pkl");res=json.load(open("sim_results.json"))
G="#2D6A4F";OR="#D9822B";RD="#C0392B";GR="#555555";LG="#E8F3EC"
plt.rcParams.update({"font.family":"DejaVu Sans","axes.spines.top":False,"axes.spines.right":False})
def day(ax,room,d,title,flag=True):
    s=test[(test.room==room)&(test.day==d)].sort_values("win");t=s.win/4
    for w in s[s.cls==1].win: ax.axvspan(w/4,(w+1)/4,color=LG,lw=0)
    ax.plot(t,s.power,color=G,lw=1.6)
    if flag:
        f=s[s.flag];ax.scatter(f.win/4,f.power,color=RD,s=14,zorder=5,label="Flagged by AI")
    ax.set_xlim(0,24);ax.set_xticks(range(0,25,3));ax.set_xlabel("Hour of day");ax.set_ylabel("Room power (kW)");ax.set_title(title,loc="left",fontsize=10.5,color=GR);ax.grid(axis="y",alpha=.25)
fig,axs=plt.subplots(1,2,figsize=(10,3.3),dpi=200,sharey=True)
day(axs[0],3,15,"A normal day: power follows the classes (green bands)",flag=False)
axs[0].annotate("Off 15 min\nafter class",xy=(14.3,0.06),xytext=(16.5,0.9),fontsize=8.5,color=OR,fontweight="bold",arrowprops=dict(arrowstyle="->",color=OR))
day(axs[1],2,16,"A fault day: AC left on overnight (relay failure)")
axs[1].legend(frameon=False,fontsize=8.5,loc="upper right")
plt.tight_layout();plt.savefig("timeline.png",facecolor="white");plt.close()
# results bars
k=["Overnight AC\n(3 events)","AC left on 2 h\nafter class\n(6 events)","Faulty AC,\n30% extra power\n(1 room)"]
v=[res["Overnight AC"]["rate_pct"],res["AC left on 2 h after class"]["rate_pct"],res["Faulty AC (+30%)"]["rate_pct"]]
fig,ax=plt.subplots(figsize=(5.2,3.4),dpi=200)
b=ax.bar(range(3),v,color=[G,G,RD],width=.6)
for i,x in enumerate(v): ax.text(i,x+2,f"{x:.0f}%",ha="center",fontweight="bold",fontsize=11)
ax.set_xticks(range(3));ax.set_xticklabels(k,fontsize=8.5);ax.set_ylim(0,118);ax.set_ylabel("Share of fault windows flagged (%)",fontsize=9);ax.grid(axis="y",alpha=.25)
ax.set_title("Simulated test: what the AI caught",loc="left",fontsize=10.5,color=GR)
plt.tight_layout();plt.savefig("results.png",facecolor="white");plt.close()
print("ok")
