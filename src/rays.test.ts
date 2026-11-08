import {describe,it,expect} from 'vitest';
import {clipSegment,sourceHeight,traceRays} from './rays';
import {optics,type Setup} from './physics';
const setup=(u:number):Setup=>({object:45-u,lens:45,screen:75,f:15});
describe('同一物点的近轴光束',()=>{
 it.each([10,22.5,30,40])('u=%s：折射直线交于薄透镜理论像点',u=>{const s=setup(u),p=optics(s);for(const r of traceRays(s)){const [[x,y],[bx,by]]=r.outgoing;expect(y+(by-y)/(bx-x)*p.v).toBeCloseTo(p.m!*sourceHeight,9);expect(r.incident[0]).toEqual([s.object,sourceHeight]);expect(Math.abs(r.incident[1][1])).toBeLessThanOrEqual(7.4);}});
 it('u=f：同一物点的出射光互相平行，且不强行平行主轴',()=>{const rays=traceRays(setup(15));const slopes=rays.map(r=>{const [[x,y],[bx,by]]=r.outgoing;return (by-y)/(bx-x)});for(const a of slopes)expect(a).toBeCloseTo(-sourceHeight/15,12);expect(rays.every(r=>r.extension===undefined)).toBe(true);});
 it('虚像才有数学反向延长线',()=>{expect(traceRays(setup(10)).every(r=>r.extension!==undefined)).toBe(true);expect(traceRays(setup(30)).every(r=>r.extension===undefined)).toBe(true);});
 it('实际光线在光屏终止，不随理论像点延伸穿过光屏',()=>{const s={...setup(22.5),screen:60};expect(traceRays(s).every(r=>r.outgoing[1][0]===60)).toBe(true);expect(s.lens+optics(s).v).toBe(90);});
 it('物体移动时中心光线折射方向实时变化',()=>{const a=traceRays(setup(40)).find(r=>r.id==='central')!,b=traceRays(setup(22.5)).find(r=>r.id==='central')!;expect(a.outgoing[1][1]).not.toBe(b.outgoing[1][1]);});
 it('第三主光线超出镜片孔径时省略，焦点前后不出现无限坐标',()=>{for(const u of [14.999,15,15.001])for(const r of traceRays(setup(u))){expect([...r.incident.flat(),...r.outgoing.flat(),...(r.extension?.flat()||[])].every(Number.isFinite)).toBe(true);expect(Math.abs(r.incident[1][1])).toBeLessThanOrEqual(7.4);}});
});
describe('光线视野裁切',()=>{
 const b={left:0,right:10,bottom:-5,top:5};
 it('保留穿过边界的可见部分',()=>expect(clipSegment([[-10,0],[20,0]],b)).toEqual([[0,0],[10,0]]));
 it('忽略完全越界的线段',()=>expect(clipSegment([[0,6],[10,6]],b)).toBeNull());
 it('保留垂直光屏方向线段',()=>expect(clipSegment([[5,-10],[5,10]],b)).toEqual([[5,-5],[5,5]]));
});
