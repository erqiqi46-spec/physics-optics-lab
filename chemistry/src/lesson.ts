import {initial,reducer,advance,cloudy,type State,type Action} from './model';
export type ToolAction='check'|'marble'|'acid'|'lime'|'collect'|'mouth'|'inside'|'cover';
export type Lesson={state:State;stage:number;notice:string;pour:number};
export const steps=['检查气密性','装入大理石','加入稀盐酸','石灰水检验','收集二氧化碳','瓶口验满','盖片与记录'];
export function prepared():State{return {...initial(),items:['flask','bung','funnel','hose','jar','beaker','splint','plate'],connection:['generator','receiver'],bung:true,tight:true,funnel:20,outlet:65,tip:10,feedback:{title:'装置已搭好，可以直接实验',text:'点击发生装置旁的“检查气密性”，开始第一步。',danger:false}};}
export const newLesson=():Lesson=>({state:prepared(),stage:0,notice:'所有器材已就位。先检查装置气密性，再加入药品。',pour:0});
const apply=(s:State,actions:Action[])=>actions.reduce(reducer,s);
export type LessonAction={type:'tool';tool:ToolAction}|{type:'next'}|{type:'tick';seconds:number}|{type:'pause'}|{type:'speed';value:number}|{type:'select';id:State['selected']}|{type:'reset'};
export function lessonReducer(l:Lesson,a:LessonAction):Lesson{let s=l.state;if(a.type==='reset')return newLesson();if(a.type==='select')return {...l,state:{...s,selected:a.id}};if(a.type==='pause'||a.type==='speed')return {...l,state:reducer(s,a)};if(a.type==='tick'){s=advance(s,a.seconds);if(l.stage===3&&s.identified&&cloudy(l.state)<=.3&&cloudy(s)>.3)s={...s,paused:true,feedback:{title:'已捕捉石灰水变浑浊的现象',text:'虚拟时间停在关键观察点。检验身份的证据已获得，点击“转入收集”继续；真实反应不会自行暂停。',danger:false}};return {...l,state:s};}
if(a.type==='next'){if(l.stage===0&&s.checked){s=apply(s,[{type:'drain'},{type:'clamp'},{type:'bung'}]);return {...l,state:s,stage:1,notice:'检查完成。检查水已排出、气路已打开、瓶塞已取下。点击台前的大理石盘，把小块沿瓶壁送入。'};}if(l.stage===1&&s.solidLoaded){s=reducer(s,{type:'bung'});return {...l,state:s,stage:2,notice:'固体已放入，装置已复装密封。点击稀盐酸瓶，经长颈漏斗加液；漏斗下端须浸入反应液。'};}if(l.stage===5&&s.wood?.valid)return {...l,stage:6,notice:'瓶口木条熄灭，获得本次规范验满现象。点击玻璃片盖口，再保存你的观察。'};return l;}
const tool=a.tool;const refuse=(text:string)=>({...l,notice:text});
if(tool==='check'){if(l.stage!==0)return refuse('本轮已完成加药前检查。需要重新检查，可重置实验。');if(s.air&&s.air.age<3)return l;s=apply(s,[{type:'check-water'},...(!s.clamp?[{type:'clamp'} as Action]:[]),{type:'air-test'}]);return {...l,state:s,notice:'正在建立漏斗液柱并观察。注意液柱是否维持；这只描述本次检查条件。'};}
if(tool==='marble'){if(l.stage!==1)return refuse('先完成加药前气密性检查，再装入固体；用当前步骤的高亮按钮继续。');if(s.solidLoaded)return refuse('本轮大理石已经装入。点击“复塞，进入加液”。');return {...l,state:reducer(s,{type:'load-solid'}),pour:l.pour+1,notice:'大理石已进入发生器。先放固体再加液体，可避免把固体直接投入液体引起飞溅。'};}
if(tool==='acid'){if(l.stage!==2)return refuse('先装入大理石并复装瓶塞，再经长颈漏斗加入稀盐酸。');s=reducer(s,{type:'add-liquid'});return {...l,state:s,stage:3,pour:l.pour+1,notice:'反应物相遇即反应。观察固体表面气泡；再点击检验烧杯，加入新鲜石灰水并切换气路进行检验。'};}
if(tool==='lime'){if(l.stage!==3)return refuse('请先完成检查、装固体和加酸，再进行石灰水检验。');s=apply(s,[{type:'lime',value:'limewater'},{type:'port',port:'generator'},{type:'port',port:'tester'}]);return {...l,state:s,notice:'气路已切换至新鲜石灰水。观察澄清→浑浊；可点“观察5秒”推进虚拟时间。'};}
if(tool==='collect'){if(l.stage!==3||!s.identified)return refuse('先观察石灰水变浑浊，获得检验证据，再切换收集。');s=apply({...s,paused:false},[{type:'port',port:'generator'},{type:'port',port:'receiver'}]);return {...l,state:s,stage:4,notice:'气路已转入瓶口朝上的集气瓶，导管末端近瓶底。继续收集，比较瓶内与瓶口的木条现象。'};}
if(tool==='mouth'||tool==='inside'){if(l.stage<4)return refuse('先完成身份检验并转入集气瓶收集，再进行木条操作。');s=reducer(s,{type:'wood',place:tool});return {...l,state:s,stage:tool==='mouth'&&s.wood?.valid?5:l.stage,notice:s.feedback.text};}
if(tool==='cover'){if(l.stage!==6)return refuse('先规范收集，并在瓶口验满，再用玻璃片盖口。');if(!s.cover)s=apply(s,[{type:'disconnect'},{type:'cover'}]);return {...l,state:s,notice:'导管已移开，玻璃片已遮盖瓶口（不等于气密封闭）。本轮完成，请记录检验与验满两组证据。'};}
return l;}
export type DemoId='funnel'|'loose'|'outlet'|'shallow'|'inverted'|'early'|'inside'|'clamp';
export const demos:{id:DemoId;title:string;phenomenon:string;why:string;correct:string}[]=[
{id:'funnel',title:'漏斗未液封',phenomenon:'发生器仍有气泡，气体从漏斗逸散，集气瓶中积聚较慢。',why:'漏斗下端高于液面，气体可从漏斗口逸出。冒泡不代表已经正确收集。',correct:'漏斗下端浸入液体，形成液封。'},
{id:'loose',title:'瓶塞未塞紧',phenomenon:'反应继续，但接头有逸散示意；相同时间内收集效果较差。',why:'反应与漏气可以同时发生。应在加药前检查密封，而不是凭气泡判断气密性。',correct:'塞紧接头，并在加药前检查气密性。'},
{id:'outlet',title:'出气管浸入反应液',phenomenon:'显示液体被推入导管的风险，当前收集与检验可能受干扰。',why:'发生器出气管和长颈漏斗用途不同。出气管浸液可能造成液体夹带。',correct:'发生器出气管下端露出液面；已夹带的这一轮应重做。'},
{id:'shallow',title:'收集导管靠近瓶口',phenomenon:'瓶口局部气流可使木条熄灭，但瓶内空气排出不充分，不能据此可靠验满。',why:'气体没有从瓶底附近进入，局部火焰现象不等于已规范收集。',correct:'导管末端到瓶底附近，用向上排空气法充分置换。'},
{id:'inverted',title:'集气瓶倒置',phenomenon:'CO₂容易逸出，倒置瓶中难以按本次方法有效积聚。',why:'本例CO₂密度大于空气，不能仿照较轻气体倒置收集。',correct:'瓶口朝上，导管末端近瓶底。'},
{id:'early',title:'过早在瓶口验满',phenomenon:'反应在进行，但瓶口木条仍燃烧；这不等于没有生成CO₂。',why:'初始导出气体含空气，且置换需要过程。瓶口还未出现使火焰熄灭的现象。',correct:'规范收集并继续观察，再在瓶口验满。'},
{id:'inside',title:'把木条伸入瓶内',phenomenon:'瓶内木条已熄灭，但同一时刻瓶口木条仍可燃烧。',why:'CO₂先在瓶内较低位置积聚；瓶内局部现象不能代替瓶口验满。',correct:'把燃着木条放在瓶口；不足时继续收集后复验。'},
{id:'clamp',title:'反应时夹闭出口',phenomenon:'触发增压风险提示，虚拟时间保护性暂停。',why:'密闭发生器仍在反应，夹闭出口可能增压。真实反应不能按按钮停止。',correct:'保持气体导出通道畅通；本演示不模拟真实危险增压。'}];
function reactingSetup(){let s=prepared();s=apply(s,[{type:'bung'},{type:'load-solid'},{type:'bung'},{type:'add-liquid'}]);return {...s,speed:0};}
export function demoSnapshot(id:DemoId,correct=false):State{let s=reactingSetup();let t=35;if(id==='funnel'&&!correct)s={...s,funnel:70};if(id==='loose'&&!correct)s={...s,tight:false};if(id==='outlet'&&!correct)s={...s,outlet:10};if(id==='shallow'){t=110;if(!correct)s={...s,tip:85};}if(id==='inverted'&&!correct)s={...s,upright:false};if(id==='early')t=correct?70:12;if(id==='inside')t=correct?70:35;if(id==='clamp'&&!correct)s={...s,clamp:true};s=advance(s,Math.min(60,t));if(t>60)s=advance(s,t-60);if(['early','inside','shallow'].includes(id))s=reducer(s,{type:'wood',place:id==='inside'&&!correct?'inside':'mouth'});return s;}
