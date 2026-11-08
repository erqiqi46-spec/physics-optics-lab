import type {Setup} from './physics';
export const cases=[{name:'u > 2f',u:40,note:'缩小的倒立实像，像位于 f 与 2f 之间。'},{name:'u = 2f',u:30,note:'等大的倒立实像，像距等于 2f。'},{name:'f < u < 2f',u:22.5,note:'放大的倒立实像，像距大于 2f。'},{name:'u = f',u:15,note:'出射光平行，有限距离的光屏上不能得到实像。'},{name:'u < f',u:10,note:'正立放大的虚像，位于物体同侧，光屏不能接收。'}];
export function preset(i:number):Setup{return {object:45-cases[i].u,lens:45,screen:i===2?90:75,f:15};}
