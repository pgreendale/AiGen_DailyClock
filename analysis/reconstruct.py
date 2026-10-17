"""Rebuild the periodic cubic model; check frozen coefficients; plot halfday mapping."""
from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent
rows=json.loads((R/"data/profile_15min.json").read_text(encoding="utf-8-sig"))
y=np.array([r["weighted3_pct"]/100/.25 for r in rows])
delta=(np.roll(y,-1)-y)/.25
m=np.zeros(96)
for i in range(96):
 a,b=delta[i-1],delta[i]
 if a*b>0:m[i]=2*a*b/(a+b)
c=np.array([[y[i],.25*m[i],3*(y[(i+1)%96]-y[i])-.25*(2*m[i]+m[(i+1)%96]),2*(y[i]-y[(i+1)%96])+.25*(m[i]+m[(i+1)%96])] for i in range(96)])
z=np.sum(.25*(c[:,0]+c[:,1]/2+c[:,2]/3+c[:,3]/4));c/=z
model=json.loads((R/"data/density_24h.json").read_text(encoding="utf-8-sig"))
frozen=np.array([[v[k] for k in ["a","b","c","d"]] for v in model["coefficients"]])
error=float(np.max(np.abs(c-frozen)));assert error<1e-10,error
mass=.25*(c[:,0]+c[:,1]/2+c[:,2]/3+c[:,3]/4);prefix=np.r_[0,np.cumsum(mass)]
def unwrapped(t):
 turn=math.floor(t/24);x=t-turn*24;i=min(95,int(x*4));u=(x-i*.25)*4;a,b,c1,d=c[i]
 return turn+prefix[i]+.25*(a*u+b*u*u/2+c1*u**3/3+d*u**4/4)
origin=unwrapped(-.125)
def F(t):return unwrapped(t-.125)-origin
M=F(12)
t=np.linspace(0,24,2401);v=[]
for x in t:
 shifted=(x-.125)%24;i=min(95,int(shifted*4));u=(shifted-i*.25)*4
 a,b,c1,d=c[i];v.append(((d*u+c1)*u+b)*u+a)
f=np.array(v);g=f/np.where(t<12,2*M,2*(1-M))
cdf=np.array([F(x) for x in t]);G=np.where(t<=12,cdf/(2*M),.5+(cdf-M)/(2*(1-M)))
fig,axes=plt.subplots(3,1,figsize=(10,8),sharex=True,layout="constrained")
axes[0].plot(t,f,label="f: ursprüngliche Dichte");axes[0].plot(t,g,label="g: Halbtagstransformation");axes[0].set_ylabel("Dichte [1/h]");axes[0].legend()
axes[1].plot(t,cdf,label="F");axes[1].plot(t,G,label="G");axes[1].axvline(12,color=".7");axes[1].set_ylabel("kumulierte Masse");axes[1].legend()
axes[2].plot(t,360*g,color="firebrick");axes[2].set_ylabel("Winkelgeschwindigkeit [°/h]");axes[2].set_xlabel("lokale Uhrzeit [h]")
for ax in axes:ax.set_xlim(0,24);ax.set_xticks(range(0,25,2));ax.grid(alpha=.2)
out=R.parent/"docs/images/Modell.png";fig.savefig(out,dpi=150);plt.close(fig)
result={"coefficient_max_error":error,"mass_0_12":M,"integral_f":float(sum(mass)),"G_0":float(G[0]),"G_12":float(G[1200]),"G_24":float(G[-1]),"normalization_before_division":float(z)}
(R.parent/"docs/evidence/model-check.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
