import {describe,it,expect} from 'vitest';
import {optics,constrain,initial} from './physics';
import {preset} from './teaching';
describe('薄透镜五类科学边界',()=>{
 it.each([{u:10,v:-30,m:3,real:false},{u:15,v:Infinity,m:null,real:false},{u:22.5,v:45,m:-2,real:true},{u:30,v:30,m:-1,real:true},{u:40,v:24,m:-.6,real:true}])('u=$u cm',({u,v,m,real})=>{const p=optics({object:45-u,lens:45,screen:75,f:15});expect(p.v).toBe(v);if(m===null)expect(p.m).toBeNull();else expect(p.m).toBeCloseTo(m);expect(p.real).toBe(real);if(Number.isFinite(v))expect(1/15).toBeCloseTo(1/u+1/v,12);});
 it('屏离开像点产生连续增加的弥散圈半径',()=>{const a=optics(initial),b=optics({...initial,screen:80}),c=optics({...initial,screen:90});expect(a.focused).toBe(true);expect(a.blur).toBe(0);expect(b.focused).toBe(false);expect(c.blur).toBeGreaterThan(b.blur);});
 it('虚像及焦点处永远不可用光屏接收',()=>{for(const u of [5,10,15])for(const screen of [47,75,100])expect(optics({object:45-u,lens:45,screen,f:15}).focused).toBe(false)});
 it('焦点两侧符号与发散极限',()=>{expect(optics({...initial,object:30.001}).v).toBeLessThan(-100000);expect(optics({...initial,object:29.999}).v).toBeGreaterThan(100000)});
});
describe('轨道约束和教学结构',()=>{
 it('防止器材穿透并保持 2 cm 间隙',()=>{expect(constrain(initial,'object',80).object).toBe(43);expect(constrain(initial,'lens',100).lens).toBe(73);expect(constrain(initial,'screen',0).screen).toBe(47);expect(constrain(initial,'screen',120).screen).toBe(100);expect(constrain(initial,'object',-5).object).toBe(0)});
 it('焦距区间与精度',()=>{expect(constrain(initial,'f',0).f).toBe(5);expect(constrain(initial,'f',100).f).toBe(25);expect(constrain(initial,'f',15.24).f).toBe(15.2)});
 it('教学预设涵盖五种类别',()=>expect([0,1,2,3,4].map(i=>optics(preset(i)).kind)).toEqual(['倒立实像','倒立实像','倒立实像','不成有限像','正立虚像']));
});
