import {optics,type Setup} from './physics';
import {clarityLabels,directionLabels,kindLabels,sizeLabels,type Prediction,type Observation} from './inquiry';
export type RecordRow=Setup&{id:number;prediction?:Prediction;observation?:Observation;revealed?:boolean};
export const observedScreen=(s:Setup)=>{const p=optics(s);return p.focused?'图案清晰':p.real?'离焦模糊':'未见可承接图案';};
const fmt=(n:number)=>Number.isFinite(n)?n.toFixed(1):'∞';
export const predictedText=(p?:Prediction)=>p?[p.kind&&kindLabels[p.kind],p.direction&&directionLabels[p.direction],p.size&&sizeLabels[p.size]].filter(Boolean).join(' · '):'';
const cell=(v:unknown)=>'"'+String(v??'').replaceAll('"','""')+'"';
export function recordsCsv(records:RecordRow[],demo=false){const rows:unknown[][]=[['组别','物体轨道坐标x_o(cm)','透镜轨道坐标x_l(cm)','光屏轨道坐标x_s(cm)','物距u=x_l-x_o(cm)','实际屏距d=x_s-x_l(cm)','焦距f(cm)','学生预测','学生观察','学生说明','理论像距v(cm)','理论放大率m','理论像的性质','模型屏面状态']];records.forEach((r,i)=>{const p=optics(r),show=demo||r.revealed!==false;rows.push([i+1,fmt(r.object),fmt(r.lens),fmt(r.screen),fmt(p.u),fmt(p.d),fmt(r.f),predictedText(r.prediction),r.observation?.clarity?clarityLabels[r.observation.clarity]:'',r.observation?.note||'',show?fmt(p.v):'',show?(p.m?.toFixed(2)||'不定义'):'',show?`${p.kind} · ${p.size}`:'',observedScreen(r)]);});return '\uFEFF'+rows.map(r=>r.map(cell).join(',')).join('\r\n');}
