from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.cm import ScalarMappable
from matplotlib import colormaps
clock_cmap = LinearSegmentedColormap.from_list("YlGnBu_blue_to_green", colormaps["YlGnBu_r"](np.linspace(0, .75, 256)))
base=Path(__file__).resolve().parent
model=json.loads((base/"density_24h.json").read_text(encoding="utf-8-sig"))
p=np.array([[v[k] for k in ("a","b","c","d")] for v in model["coefficients"]])
h=.25
mass=h*(p[:,0]+p[:,1]/2+p[:,2]/3+p[:,3]/4)
prefix=np.r_[0,np.cumsum(mass)]
def primitive(c,u):
    return c[...,0]*u+c[...,1]*u*u/2+c[...,2]*u**3/3+c[...,3]*u**4/4
def cumulative_from_knot(z):
    z=np.asarray(z); turns=np.floor(z/24); x=z-turns*24
    i=np.minimum(95,np.floor(x/h).astype(int));u=(x-i*h)/h
    return turns*prefix[-1]+prefix[i]+h*primitive(p[i],u)
origin=cumulative_from_knot(-.125)
def F(t): return cumulative_from_knot(np.asarray(t)-.125)-origin
def density(t):
    x=(np.asarray(t)-.125)%24
    i=np.minimum(95,np.floor(x/h).astype(int));u=(x-i*h)/h;c=p[i]
    return ((c[...,3]*u+c[...,2])*u+c[...,1])*u+c[...,0]
# Normalize each half-day separately, then allocate half of the circle to each.
M0=float(F(12))
M1=float(F(24)-F(12))
assert M0>0 and M1>0
def conditional_cdf(t):
    t=np.asarray(t)
    return np.where(t<=12,F(t)/M0,(F(t)-M0)/M1)
def G(t):
    t=np.asarray(t)
    return np.where(t<=12,.5*F(t)/M0,.5+.5*(F(t)-M0)/M1)
def angle(t): return 2*np.pi*G(t)
def adjusted_density(t):
    t=np.asarray(t)
    return .5*density(t)/np.where(t<12,M0,M1)
# Exact extrema of the cubic density pieces, including both limits at noon.
candidate_times=[float((.125+i*h)%24) for i in range(96)]
for i,c in enumerate(p):
    roots=np.roots([3*c[3],2*c[2],c[1]]) if abs(c[3])>1e-20 else np.roots([2*c[2],c[1]])
    for u in roots:
        if np.isreal(u) and 0<float(np.real(u))<1:
            candidate_times.append(float((.125+i*h+float(np.real(u))*h)%24))
candidates=[float(adjusted_density(ti)) for ti in candidate_times]
candidates.extend([.5*float(density(12))/M0,.5*float(density(12))/M1])
fmax=max(candidates)
assert np.allclose(angle(np.array([0,12,24])),[0,np.pi,2*np.pi],atol=1e-12)
t=np.linspace(0,24,5761)
theta=angle(t)
assert np.all(np.diff(theta)>0)
tm=(t[:-1]+t[1:])/2
values=adjusted_density(tm)/fmax
samples=[{"hour":float(ti),"cdf_halfday_normalized":float(G(ti)),"density_halfday_normalized":float(adjusted_density(ti)),"angle_radians":float(angle(ti))} for ti in np.linspace(0,24,1441)]
(base/"halfday_profile.json").write_text(json.dumps({"source":"density_24h.json","original_mass_0_12":M0,"original_mass_12_24":M1,"conditional_density":"f(t)/M0 for t<12; f(t)/M1 for t>=12; each half integrates to 1","global_density":"g(t)=f(t)/(2*M0) for t<12; f(t)/(2*M1) for t>=12; each half integrates to 0.5","cdf":"G(t)=F(t)/(2*M0) for t<=12; 0.5+(F(t)-M0)/(2*M1) otherwise","angle":"2*pi*G(t)","max_adjusted_density":fmax,"samples":samples},indent=2))
assert min(values)>=0 and max(values)<=1+1e-10
# Display rotation only: midnight at top, clockwise.
def xy(a,r): return np.column_stack((r*np.sin(a),r*np.cos(a)))
outer=xy(theta,1); inner=xy(theta,.7375)
polys=np.stack([outer[:-1],outer[1:],inner[1:],inner[:-1]],axis=1)
plt.rcParams.update({"font.family":"DejaVu Sans","svg.fonttype":"none"})
fig,ax=plt.subplots(figsize=(10,11),facecolor="white")
fig.subplots_adjust(left=.07,right=.93,top=.94,bottom=.17)
ax.set(xlim=(-1.1,1.1),ylim=(-1.1,1.1),aspect="equal")
ax.add_collection(PolyCollection(polys,array=values,cmap=clock_cmap,norm=Normalize(0,1),edgecolors="face",linewidth=.18,rasterized=False))
# Fit each glyph inside both the annulus and its available angular sector.
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D
font=FontProperties(family="DejaVu Sans",weight="normal")
shown=[3,6]+list(range(7,24))
angles=np.array([float(angle(hr)) for hr in shown])
for idx,hr in enumerate(shown):
    a=angles[idx]
    previous=angles[idx-1] if idx>0 else angles[-1]-2*np.pi
    following=angles[idx+1] if idx<len(shown)-1 else angles[0]+2*np.pi
    left=(a-previous)*.46
    right=(following-a)*.46
    glyph=TextPath((0,0),str(hr),size=1,prop=font)
    box=glyph.get_extents()
    glyph=glyph.transformed(Affine2D().translate(-(box.x0+box.x1)/2,-(box.y0+box.y1)/2))
    # Radial alignment; flip on the left for readability.
    rotation=np.pi/2-a
    if np.cos(rotation)<0: rotation+=np.pi
    center=.86875
    def fitted(scale):
        transform=Affine2D().scale(scale).rotate(rotation).translate(np.sin(a)*center,np.cos(a)*center)
        verts=transform.transform(glyph.vertices)
        radii=np.sqrt((verts**2).sum(axis=1))
        aa=np.arctan2(verts[:,0],verts[:,1])
        diff=(aa-a+np.pi)%(2*np.pi)-np.pi
        return radii.min()>.75 and radii.max()<.985 and diff.min()>-left and diff.max()<right
    lo,hi=0.,1.
    for _ in range(45):
        mid=(lo+hi)/2
        if fitted(mid):lo=mid
        else:hi=mid
    v=float(adjusted_density(hr)/fmax)
    rgb=clock_cmap(v)[:3]
    luminance=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2]
    color="white" if luminance<.48 else "#102a39"
    trans=Affine2D().scale(lo).rotate(rotation).translate(np.sin(a)*center,np.cos(a)*center)
    ax.add_patch(PathPatch(glyph,transform=trans+ax.transData,facecolor=color,edgecolor="none",zorder=4))
    ax.plot([np.sin(a)*.7375,np.sin(a)*.7575],[np.cos(a)*.7375,np.cos(a)*.7575],color=color,lw=.9)
ax.add_patch(plt.Circle((0,0),.7375,facecolor="black",edgecolor="white",linewidth=1.2,zorder=5))
ax.set(xlim=(-1.1,1.1),ylim=(-1.1,1.1),aspect="equal")
ax.axis("off")
cbax=fig.add_axes([.26,.10,.48,.018])
cb=fig.colorbar(ScalarMappable(norm=Normalize(0,1),cmap=clock_cmap),cax=cbax,orientation="horizontal",ticks=[0,.25,.5,.75,1])
cb.outline.set_visible(False)
cb.ax.tick_params(labelsize=9,length=3)
cb.set_label("Relative Dichte  g(t) / max g(t)",fontsize=10,labelpad=8)
fig.text(.5,.045,"Je Tageshälfte normiert · 00:00 oben · 12:00 unten",ha="center",fontsize=10,color="#344f60")
fig.text(.5,.025,"Basis: Londoner Verkehrsindikator mit modellhafter Erwerbsgewichtung",ha="center",fontsize=8,color="#627582")
fig.savefig(base/"Ziffernblatt.svg")
fig.savefig(base/"Ziffernblatt.png",dpi=180)
positions=[{"hour":hr,"F_original":float(F(hr)),"F_halfday_normalized":float(G(hr)),"angle_radians_clockwise_from_top":float(angle(hr)),"x_over_r":float(np.sin(angle(hr))),"y_over_r_upwards":float(np.cos(angle(hr)))} for hr in range(24)]
(base/"Ziffernblatt_Positionen.json").write_text(json.dumps({"max_density":fmax,"color":"Matplotlib YlGnBu_r truncated to [0,0.75], blue to green; Normalize(0,1); g(t)/max(g), separate halfday normalization","rotation":"midnight at top, noon at bottom, clockwise","original_halfday_masses":[M0,M1],"positions":positions},indent=2))
print(json.dumps({"G0":float(G(0)),"G12":float(G(12)),"G24":float(G(24)),"original_halfday_masses":[M0,M1],"max_density":fmax,"segments":len(polys),"color_min":float(min(values)),"color_max":float(max(values)),"outputs":["Ziffernblatt.svg","Ziffernblatt.png","Ziffernblatt_Positionen.json"]},indent=2))








