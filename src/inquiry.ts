import {optics,type Setup} from './physics';
export type Prediction={kind:''|'real'|'virtual'|'none';direction:''|'inverted'|'upright'|'none';size:''|'larger'|'same'|'smaller'|'none'};
export type Observation={clarity:''|'clear'|'blurred'|'no-image';note:string};
export type InquiryState={stage:'predict'|'observe'|'reveal';prediction:Prediction;observation:Observation;recordId?:number};
export const emptyInquiry=():InquiryState=>({stage:'predict',prediction:{kind:'',direction:'',size:''},observation:{clarity:'',note:''}});
export type InquiryAction={type:'prediction';key:keyof Prediction;value:string}|{type:'submit'}|{type:'observation';key:keyof Observation;value:string}|{type:'record';id:number}|{type:'reveal'}|{type:'setup';key:keyof Setup}|{type:'reset'};
export const predictionReady=(p:Prediction)=>!!p.kind&&!!p.direction&&!!p.size;
export function inquiryReducer(state:InquiryState,action:InquiryAction):InquiryState{
 switch(action.type){
  case 'reset':return emptyInquiry();
  case 'setup':return action.key!=='screen'?emptyInquiry():state.stage==='predict'?state:{...state,observation:{clarity:'',note:''},recordId:undefined};
  case 'prediction':return state.stage==='predict'?{...state,prediction:{...state.prediction,[action.key]:action.value}}:state;
  case 'submit':return state.stage==='predict'&&predictionReady(state.prediction)?{...state,stage:'observe'}:state;
  case 'observation':return state.stage==='observe'?{...state,observation:{...state.observation,[action.key]:action.value},recordId:undefined}:state;
  case 'record':return state.stage==='observe'&&state.observation.clarity?{...state,recordId:action.id}:state;
  case 'reveal':return state.stage==='observe'&&state.recordId!==undefined?{...state,stage:'reveal'}:state;
 }
}
export const kindLabels={real:'实像',virtual:'虚像',none:'无有限像'};
export const directionLabels={inverted:'倒立',upright:'正立',none:'不适用'};
export const sizeLabels={larger:'放大',same:'等大',smaller:'缩小',none:'不适用'};
export const clarityLabels={clear:'看到了清晰图案',blurred:'看到了模糊图案','no-image':'当前屏上未找到图案'};
export function expectedPrediction(s:Setup):Prediction{const p=optics(s);return {kind:p.infinity?'none':p.real?'real':'virtual',direction:p.infinity?'none':p.real?'inverted':'upright',size:p.infinity?'none':p.size==='放大'?'larger':p.size==='缩小'?'smaller':'same'};}
