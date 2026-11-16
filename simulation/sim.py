import numpy as np, pandas as pd, json
from sklearn.ensemble import IsolationForest
rng=np.random.default_rng(42)
ROOMS=10;DAYS=28;WPD=96
# rated power from sources: AC 1.05-1.8 kW, fan 50-75 W, LED tube 20 W
rows=[]
ac_kw=rng.uniform(1.05,1.8,ROOMS)
for r in range(ROOMS):
    for d in range(DAYS):
        dow=d%7  # 0..6, 5-6 weekend
        cls=np.zeros(WPD,bool)
        if dow<5:
            for hr in range(9,16):
                if rng.random()<0.7: cls[hr*4:hr*4+4]=True   # one-hour classes
        occ=np.where(cls,rng.uniform(0.7,1.0,WPD),rng.uniform(0,0.08,WPD))
        # appliances: on during class; after class end stays on until 15 min empty (rule), then off
        on=np.zeros(WPD,bool);empty=0
        for w in range(WPD):
            if cls[w]: on[w]=True;empty=0
            else:
                empty+=1
                on[w]= on[w-1] and empty<=1 if w>0 else False   # 15-minute grace = 1 window
        pw=np.where(on,ac_kw[r]+0.24+0.12,0.03)+rng.normal(0,0.03,WPD)
        for w in range(WPD):
            rows.append((r,d,w,max(pw[w],0.0),occ[w],int(on[w]),int(cls[w]),w//4,dow,"normal","normal"))
df=pd.DataFrame(rows,columns="room day win power occ on cls hour dow label kind".split())
# inject faults in test period (days 14-27)
def inject(kind,r,d,w0,w1,add=None,mult=None):
    m=(df.room==r)&(df.day==d)&(df.win>=w0)&(df.win<w1)&(df.cls==0)
    if add is not None: df.loc[m,"power"]=add+rng.normal(0,0.03,m.sum()); df.loc[m,"on"]=1
    df.loc[m,"label"]=kind;df.loc[m,"kind"]=kind
for (r,d) in [(2,16),(5,20),(8,24)]: inject("Overnight AC",r,d,0,24,add=ac_kw[r]+0.36)   # 00:00-06:00
for (r,d) in [(1,15),(3,17),(4,18),(6,21),(7,22),(9,23)]: inject("AC left on 2 h after class",r,d,64,72,add=ac_kw[r]+0.36)  # 16:00-18:00
for r in (0,):  # faulty AC draws 30% more during class, all test days
    m=(df.room==r)&(df.day>=14)&(df.cls==1); df.loc[m,"power"]*=1.3; df.loc[m,"label"]="Faulty AC (+30%)"
df["label"]=df.label.where(df.label!="normal","normal")
# features
med=df.groupby(["day","win"]).power.transform("median")
df["peer"]=df.power/(med+0.05)
X=["power","occ","on","cls","hour","dow","peer"]
train=df[df.day<14];test=df[df.day>=14].copy()
iso=IsolationForest(n_estimators=200,contamination=0.01,random_state=1).fit(train[X])
test["score"]=-iso.score_samples(test[X]);thr=np.quantile(-iso.score_samples(train[X]),0.99)
test["flag"]=test.score>thr
out={}
norm=test[test.label=="normal"]
out["normal_windows"]=int(len(norm));out["false_flags"]=int(norm.flag.sum());out["false_rate_pct"]=round(100*norm.flag.mean(),2)
for k in ["Overnight AC","AC left on 2 h after class","Faulty AC (+30%)"]:
    s=test[test.label==k];out[k]={"windows":int(len(s)),"flagged":int(s.flag.sum()),"rate_pct":round(100*s.flag.mean(),1)}
# event level for the 2h events
ev=test[test.label=="AC left on 2 h after class"].groupby(["room","day"]).flag.any();out["after_class_events_caught"]=f"{int(ev.sum())} of {len(ev)}"
ev=test[test.label=="Overnight AC"].groupby(["room","day"]).flag.any();out["overnight_events_caught"]=f"{int(ev.sum())} of {len(ev)}"
print(json.dumps(out,indent=1))
df.to_pickle("df.pkl");test.to_pickle("test.pkl");json.dump(out,open("sim_results.json","w"),indent=1)
