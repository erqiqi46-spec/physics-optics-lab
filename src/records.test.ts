import {it,expect} from 'vitest';
import {recordsCsv} from './records';
import {initial} from './physics';
it('观察记录导出区分绝对坐标和相对距离，不泄露未揭示的理论',()=>{const csv=recordsCsv([{...initial,id:1,revealed:false}]);expect(csv).toContain('光屏轨道坐标x_s(cm)');expect(csv).toContain('实际屏距d=x_s-x_l(cm)');expect(csv).toContain('"15.0","45.0","75.0","30.0","30.0","15.0"');expect(csv).toContain('"","","","图案清晰"');expect(csv).not.toContain('倒立实像');});
it('揭示或主动选择演示后，导出相同数值和正确理论',()=>{for(const csv of [recordsCsv([{...initial,id:1,revealed:true}]),recordsCsv([{...initial,id:1,revealed:false}],true)]){expect(csv).toContain('"30.0","-1.00","倒立实像 · 等大","图案清晰"');}});
it('学生说明包含逗号、引号与换行时按 CSV 规则保存',()=>{const csv=recordsCsv([{...initial,id:1,revealed:false,observation:{clarity:'clear',note:'图案，"倒立"\n清晰'}}]);expect(csv).toContain('"图案，""倒立""\n清晰"');});
it('旧版无揭示标志的记录可继续读取已知理论，不丢历史数据',()=>expect(recordsCsv([{...initial,id:1}])).toContain('倒立实像 · 等大'));
