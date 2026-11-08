import {optics,type Setup} from './physics';
export type Point2=[number,number];
export type OpticalRay={id:string;color:string;principal:boolean;incident:[Point2,Point2];outgoing:[Point2,Point2];extension?:[Point2,Point2]};
export const sourceHeight=4.6875; // cm, same height as the upper edge of the F pattern
export const pupilRadius=7.4; // visible lens radius, cm
export function traceRays(s:Setup,fan=true):OpticalRay[]{
 const p=optics(s);const h=sourceHeight;
 const entries:[string,number,string,boolean][]=[['parallel',h,'#ffbf69',true],['central',0,'#68eee4',true]];
 if(!p.infinity){const y=-h*s.f/(p.u-s.f);if(Math.abs(y)<=pupilRadius)entries.push(['focal',y,'#c0a2ff',true]);}
 if(fan)for(const y of [-6,-3,2.3,6])entries.push([`fan-${y}`,y,'#83edb7',false]);
 return entries.map(([id,y,color,principal])=>{const slope=(y-h)/p.u-y/s.f;const ray:OpticalRay={id,color,principal,incident:[[s.object,h],[s.lens,y]],outgoing:[[s.lens,y],[s.screen,y+slope*p.d]]};if(!p.real&&!p.infinity)ray.extension=[[s.lens,y],[s.lens+p.v,p.m!*h]];return ray;});
}
// Restrict diagrams to a finite view without changing physical intersections.
export function clipSegment(segment:[Point2,Point2],bounds:{left:number;right:number;bottom:number;top:number}):[Point2,Point2]|null{
 const [[x,y],[bx,by]]=segment,dx=bx-x,dy=by-y;let lo=0,hi=1;
 for(const [a,b] of [[-dx,x-bounds.left],[dx,bounds.right-x],[-dy,y-bounds.bottom],[dy,bounds.top-y]]){if(Math.abs(a)<1e-12){if(b<0)return null;}else{const r=b/a;if(a<0)lo=Math.max(lo,r);else hi=Math.min(hi,r);if(lo>hi)return null;}}
 return [[x+lo*dx,y+lo*dy],[x+hi*dx,y+hi*dy]];
}
