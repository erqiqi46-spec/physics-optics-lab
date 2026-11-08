import {describe,it,expect} from 'vitest';
import {emptyInquiry,inquiryReducer,expectedPrediction,type InquiryState} from './inquiry';
import {initial} from './physics';
const predicted=():InquiryState=>({...emptyInquiry(),prediction:{kind:'real',direction:'inverted',size:'same'}});
const observed=():InquiryState=>({...predicted(),stage:'observe',observation:{clarity:'clear',note:'F 倒立'},recordId:123});
describe('先预测后揭示的状态约束',()=>{
 it('空预测不能提交，也不能提前揭示',()=>{const a=emptyInquiry();expect(inquiryReducer(a,{type:'submit'}).stage).toBe('predict');expect(inquiryReducer(a,{type:'reveal'}).stage).toBe('predict');});
 it('完整预测只解锁观察，不直接揭示',()=>expect(inquiryReducer(predicted(),{type:'submit'}).stage).toBe('observe'));
 it('没有选择观察现象时不能保存为揭示凭证',()=>expect(inquiryReducer({...predicted(),stage:'observe'},{type:'record',id:123}).recordId).toBeUndefined());
 it('保存观察后才能揭示',()=>expect(inquiryReducer(observed(),{type:'reveal'}).stage).toBe('reveal'));
 it.each(['object','lens','f'] as const)('改变 %s 时预测、观察与揭示一起失效',key=>expect(inquiryReducer({...observed(),stage:'reveal'},{type:'setup',key})).toEqual(emptyInquiry()));
 it('观察阶段移动光屏，保留预测但必须重新确认并保存观察',()=>{const a=inquiryReducer(observed(),{type:'setup',key:'screen'});expect(a.stage).toBe('observe');expect(a.prediction).toEqual(predicted().prediction);expect(a.observation.clarity).toBe('');expect(a.recordId).toBeUndefined();expect(inquiryReducer(a,{type:'reveal'}).stage).toBe('observe');});
 it('修改观察会使旧记录的揭示凭证失效',()=>{const a=inquiryReducer(observed(),{type:'observation',key:'note',value:'补充'});expect(a.recordId).toBeUndefined();});
 it('已揭示后移动光屏，不改变同一光学条件的理论结果',()=>expect(inquiryReducer({...observed(),stage:'reveal'},{type:'setup',key:'screen'}).stage).toBe('reveal'));
 it.each([{u:10,kind:'virtual',direction:'upright',size:'larger'},{u:15,kind:'none',direction:'none',size:'none'},{u:22.5,kind:'real',direction:'inverted',size:'larger'},{u:30,kind:'real',direction:'inverted',size:'same'},{u:40,kind:'real',direction:'inverted',size:'smaller'}])('u=$u 的预测对照正确',({u,kind,direction,size})=>expect(expectedPrediction({...initial,object:45-u})).toEqual({kind,direction,size}));
});
