import fs from 'node:fs';
const model=JSON.parse(fs.readFileSync(new URL('./density_24h.json',import.meta.url),'utf8'));
function primitive(p,u){return p.a*u+p.b*u*u/2+p.c*u*u*u/3+p.d*u*u*u*u/4;}
function integrate(a,b){
 let total=0,t=a;
 while(t<b-1e-12){
  const x=((t-.125)%24+24)%24;
  const i=Math.min(95,Math.floor((x+1e-12)/.25));
  const u=Math.max(0,(x-i*.25)/.25),dt=Math.min(b-t,(1-u)*.25);
  if(dt<1e-12){t+=1e-12;continue;}
  total+=.25*(primitive(model.coefficients[i],u+dt/.25)-primitive(model.coefficients[i],u));
  t+=dt;
 }
 return total;
}
/** Cumulative probability for a random event time T on [0,24] hours. */
export function cdf(t){
 if(Number.isNaN(t)||typeof t!=='number')throw new TypeError('Require numeric hour');
 if(t<=0)return 0;
 if(t>=24)return 1;
 return Math.max(0,Math.min(1,integrate(0,t)));
}
/** Probability in a non-wrapping interval [a,b] within [0,24]. */
export function probability(a,b){
 if(!Number.isFinite(a)||!Number.isFinite(b)||a<0||b>24||a>b)throw new RangeError('Require 0 <= a <= b <= 24');
 return cdf(b)-cdf(a);
}
const points=Array.from({length:1441},(_,i)=>({hour:i/60,cumulativeProbability:cdf(i/60)}));
for(let i=1;i<points.length;i++)if(points[i].cumulativeProbability+1e-12<points[i-1].cumulativeProbability)throw Error('Not monotone');
if(Math.abs(integrate(0,24)-1)>1e-10)throw Error('Normalization failure');
const checks={F0:cdf(0),F24:cdf(24),integral:integrate(0,24),monotone:true,examples:[0,5,6,9,12,14,16,19,24].map(t=>({hour:t,F:cdf(t)})),probability6to9:probability(6,9)};
fs.writeFileSync(new URL('./cdf_24h.json',import.meta.url),JSON.stringify({definition:'F(t)=integral_0^t f(s) ds',source:'density_24h.json',domainHours:[0,24],checks,points},null,2));
const line=points.map((p,i)=>(i?'L':'M')+(70+p.hour*39).toFixed(2)+','+(360-p.cumulativeProbability*280).toFixed(2)).join(' ');
const xTicks=Array.from({length:13},(_,i)=>'<text x="'+(64+i*78)+'" y="385">'+(i*2)+'</text>').join('');
const yTicks=Array.from({length:6},(_,i)=>'<line x1="70" x2="1006" y1="'+(360-i*56)+'" y2="'+(360-i*56)+'" stroke="#e5e5e5"/><text x="30" y="'+(365-i*56)+'">'+(i/5).toFixed(1)+'</text>').join('');
const svg='<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="450"><rect width="1080" height="450" fill="white"/><g font-family="Arial" font-size="13" fill="#222"><text x="70" y="28" font-size="20">Kumulative Verteilungsfunktion F(t)</text><text x="70" y="52">Erwerbsgewichtetes Tagesprofil: Wahrscheinlichkeit eines Ereignisses zwischen 00:00 und t</text>'+yTicks+'<path d="M70,80 V360 H1006" fill="none" stroke="#666"/><path d="'+line+'" fill="none" stroke="#2878b5" stroke-width="3"/>'+xTicks+'<text x="970" y="410">Uhrzeit [h]</text><text x="70" y="435">F(0) = 0; F(24) = 1. Basis: modellhaft gewichteter Londoner Verkehrsindikator.</text></g></svg>';
fs.writeFileSync(new URL('./Verteilungsfunktion.svg',import.meta.url),svg);
console.log(JSON.stringify(checks,null,2));

