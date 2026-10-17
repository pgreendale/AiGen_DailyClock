import fs from 'node:fs';
const source=JSON.parse(fs.readFileSync(new URL('./profile_15min.json',import.meta.url),'utf8').replace(/^\uFEFF/,''));
const h=.25,n=96;
const y=source.map(r=>r.weighted3_pct/100/h);
const delta=y.map((v,i)=>(y[(i+1)%n]-v)/h);
const m=y.map((v,i)=>{const a=delta[(i+n-1)%n],b=delta[i];return a*b>0?2*a*b/(a+b):0;});
let pieces=y.map((a,i)=>{const j=(i+1)%n;return {startHour:.125+i*h,a,b:h*m[i],c:3*(y[j]-a)-h*(2*m[i]+m[j]),d:2*(a-y[j])+h*(m[i]+m[j])};});
const area=pieces.reduce((s,p)=>s+h*(p.a+p.b/2+p.c/3+p.d/4),0);
pieces=pieces.map(p=>({...p,a:p.a/area,b:p.b/area,c:p.c/area,d:p.d/area}));
/** t: local hour, return density in 1/hour; period 24 hours. */
export function density(t){
 if(!Number.isFinite(t))throw new TypeError('Require finite hour');
 const x=((t-.125)%24+24)%24,i=Math.min(95,Math.floor(x/h)),u=(x-i*h)/h,p=pieces[i];
 return ((p.d*u+p.c)*u+p.b)*u+p.a;
}
/** Probability of an interval, allowing b>24 for midnight crossings. */
export function probability(a,b){
 if(!Number.isFinite(a)||!Number.isFinite(b)||b<a)throw new RangeError('Require a <= b');
 const turns=Math.floor((b-a)/24);let mass=turns,t=a,end=a+((b-a)%24);
 while(t<end-1e-11){
  const x=((t-.125)%24+24)%24,i=Math.min(95,Math.floor((x+1e-12)/h));
  const u=Math.max(0,(x-i*h)/h),dt=Math.min(end-t,(1-u)*h);
  if(dt<1e-12){t+=1e-12;continue;}
  const v=u+dt/h,p=pieces[i],F=z=>p.a*z+p.b*z*z/2+p.c*z*z*z/3+p.d*z*z*z*z/4;
  mass+=h*(F(v)-F(u));t+=dt;
 }return mass;
}
const integral=pieces.reduce((s,p)=>s+h*(p.a+p.b/2+p.c/3+p.d/4),0);
let min=Infinity,max=-Infinity,maxT=0,numerical=0;
for(let i=0;i<86400;i++){const t=(i+.5)/3600,v=density(t);numerical+=v/3600;min=Math.min(min,v);if(v>max){max=v;maxT=t;}}
if(Math.abs(integral-1)>1e-12||Math.abs(numerical-1)>1e-8||min< -1e-12||density(0)!==density(24))throw Error('Validation failed');
if(Math.abs(probability(0,24)-1)>1e-12||Math.abs(probability(23,25)-probability(23,24)-probability(0,1))>1e-10)throw Error('Integral function failed');
const out={source:'weighted3_pct',periodHours:24,stepHours:h,knotOffsetHours:.125,unit:'1/hour',normalizationBeforeScaling:area,integral,numerical,min,max,maxHour:maxT,coefficients:pieces};
fs.writeFileSync(new URL('./density_24h.json',import.meta.url),JSON.stringify(out,null,2));
const samples=Array.from({length:1441},(_,i)=>({hour:i/60,density:density(i/60)}));
fs.writeFileSync(new URL('./density_1min.json',import.meta.url),JSON.stringify(samples));
const top=Math.ceil(max*100)/100;
const line=samples.map((p,i)=>(i?'L':'M')+(60+p.hour*40).toFixed(2)+','+(350-p.density/top*270).toFixed(2)).join(' ');
const ticks=Array.from({length:13},(_,i)=>'<text x="'+(60+i*80)+'" y="375">'+(i*2)+'</text>').join('');
const svg='<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="440"><rect width="1080" height="440" fill="white"/><g font-family="Arial" font-size="13" fill="#222"><text x="60" y="28" font-size="20">Normierte Dichte: erwerbsgewichtetes Tagesprofil</text><text x="60" y="51">Periodische kubische Interpolation; Integral ueber 24 h = 1; Dichte in 1/h</text><path d="M60,80 V350 H1020" fill="none" stroke="#777"/><path d="'+line+'" fill="none" stroke="#2678b8" stroke-width="2.5"/>'+ticks+'<text x="18" y="85">'+top+'</text><text x="37" y="353">0</text><text x="990" y="398">Uhrzeit [h]</text><text x="60" y="425">Londoner Verkehrsindikator mit modellhafter Erwerbsgewichtung; keine HETUS-Bevoelkerungsdichte.</text></g></svg>';
fs.writeFileSync(new URL('./Dichtefunktion.svg',import.meta.url),svg);
console.log(JSON.stringify({integral,numerical,min,max,maxT,area,blocks:[[0,5],[6,9],[12,14],[16,19]].map(([a,b])=>({a,b,p:probability(a,b)}))},null,2));

