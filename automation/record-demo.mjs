import {chromium,expect} from '@playwright/test';
import {mkdir,readFile,writeFile,rename} from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const startIndex=Number(process.env.DEMO_START||0);
const output=path.resolve(process.env.RECORD_OUT||'recordings');await mkdir(output,{recursive:true});
const cues=JSON.parse(await readFile(new URL('./cues.json',import.meta.url),'utf8'));
const url=process.env.DEMO_URL||pathToFileURL(path.resolve('docs/index.html')).href;
const browser=await chromium.launch({headless:process.env.DEMO_HEADLESS!=='0',args:['--no-sandbox','--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader']});
const context=await browser.newContext({viewport:{width:1920,height:1080},deviceScaleFactor:1,recordVideo:{dir:output,size:{width:1920,height:1080}},reducedMotion:'reduce'});
const page=await context.newPage();page.setDefaultTimeout(60000);const errors=[],external=[],checks=[],timeline=[];
page.on('pageerror',e=>errors.push(e.message));await page.route('**/*',r=>{const u=r.request().url();if(url.startsWith('file:')&&/^https?:/.test(u)){external.push(u);return r.abort();}return r.continue();});
if(startIndex>0){
 // Restore the five rows already demonstrated in the retained first take; do not alter optical computation.
 const prior=[{object:15,lens:45,screen:75,f:15,prediction:{kind:'real',direction:'inverted',size:'same'},observation:{clarity:'clear',note:'同尺度比较：倒立、等大，屏上图案清晰。'}},{object:5,lens:45,screen:69,f:15},{object:22.5,lens:45,screen:90,f:15},{object:30,lens:45,screen:75,f:15},{object:35,lens:45,screen:75,f:15}].map((r,i)=>({...r,id:i+1,revealed:true}));
 await page.addInitScript(rows=>localStorage.setItem('optics-records',JSON.stringify(rows)),prior);
}
await page.goto(url,{waitUntil:'domcontentloaded'});await page.getByTestId('drag-anchor-lens').waitFor({state:'visible'});await page.getByTestId('theory-distance').waitFor({state:'visible'});await expect(page.getByTestId('theory-distance')).toHaveText('待揭示');
await page.evaluate(()=>{
 const style=document.createElement('style');style.textContent=`
 #demo-top,#demo-caption,#demo-pointer,#demo-highlight,#demo-sync{pointer-events:none!important;position:fixed;box-sizing:border-box}
 #demo-top{inset:0 0 auto;height:65px;background:#0b1520f5;border-bottom:1px solid #487b6b;z-index:2147483636;display:flex;align-items:center;padding:0 45px;gap:20px;font-family:"Noto Sans CJK SC","Microsoft YaHei",sans-serif;color:#ddede8}
 #demo-top b{color:#92e6c7;font-size:17px;font-weight:500;border:1px solid #41695c;border-radius:5px;padding:5px 9px}#demo-chapter{font-size:22px}#demo-counter{margin-left:auto;font-size:16px;color:#93aea7}
 #demo-caption{inset:auto 0 0;background:linear-gradient(0deg,#071018ff,#071018f5);border-top:1px solid #3b6556;z-index:2147483638;min-height:150px;padding:18px 90px 22px;display:flex;align-items:center;justify-content:center;color:#f3f8f7;font:500 30px/1.65 "Noto Sans CJK SC","Microsoft YaHei",sans-serif;text-align:center;text-wrap:balance}
 #demo-caption p{margin:0;max-width:1720px;line-height:1.65}#demo-pointer{left:-50px;top:-50px;width:25px;height:34px;z-index:2147483645;filter:drop-shadow(0 1px 3px #000a)}#demo-highlight{display:none;border:3px solid #a0efcd;border-radius:7px;box-shadow:0 0 0 5px #8aefb825,0 0 20px #7ceab82e;z-index:2147483640}#demo-sync{left:1px;top:1px;width:16px;height:16px;z-index:2147483647}
 .modal-backdrop{backdrop-filter:none!important;background:#020a13ef!important;padding-top:82px!important;padding-bottom:170px!important}.modal{max-height:calc(100vh - 260px)!important}.app{padding-bottom:180px!important}
 `;document.head.appendChild(style);
 const hud=document.createElement('div');hud.innerHTML='<div id="demo-top"><b>课堂演示</b><span id="demo-chapter"></span><span id="demo-counter"></span></div><div id="demo-caption"><p></p></div><div id="demo-pointer"><svg width="25" height="34" viewBox="0 0 25 34"><path d="M2 2 L2 27 L8 21 L14 32 L20 29 L14 19 L24 19 Z" fill="#f4fff8" stroke="#287a5c" stroke-width="2"/></svg></div><div id="demo-highlight"></div><div id="demo-sync"></div>';document.body.appendChild(hud);
 document.addEventListener('mousemove',e=>{const c=document.getElementById('demo-pointer');c.style.left=e.clientX+'px';c.style.top=e.clientY+'px';},{passive:true});
 document.addEventListener('pointerdown',()=>document.getElementById('demo-pointer')?.animate([{filter:'drop-shadow(0 0 3px #9fffcc)'},{filter:'drop-shadow(0 0 14px #9fffcc)'},{filter:'drop-shadow(0 0 3px #9fffcc)'}],{duration:450}),{passive:true});
});
const pause=ms=>page.waitForTimeout(ms);
async function focus(locator){await locator.evaluate(el=>{const rect=el.getBoundingClientRect();const free=innerHeight-260;const offset=95+Math.max(0,(free-Math.min(rect.height,free))/2);window.scrollTo({top:Math.max(0,scrollY+rect.top-offset),behavior:'smooth'});});await pause(900);}
async function glow(locator){const b=await locator.boundingBox();if(!b)return;await page.evaluate(b=>{const el=document.getElementById('demo-highlight');Object.assign(el.style,{display:'block',left:(b.x-5)+'px',top:(b.y-5)+'px',width:(b.width+10)+'px',height:(b.height+10)+'px'});},b);}
async function point(locator){await locator.scrollIntoViewIfNeeded();const b=await locator.boundingBox();if(b)await page.mouse.move(b.x+b.width/2,b.y+b.height/2,{steps:18});await glow(locator);await pause(350);}
async function click(locator){await point(locator);await locator.click();await pause(450);}
async function pick(label,value){const el=page.getByLabel(label,{exact:true});await point(el);await el.selectOption(value);await pause(550);}
async function setNumber(label,n){const el=page.getByRole('spinbutton',{name:label,exact:true});await point(el);await el.fill(String(n));await el.press('Tab');await pause(450);}
async function record(){await focus(page.locator('.record-card'));await click(page.getByRole('button',{name:'记录当前实验数据',exact:true}));}
async function caseStudy(index,{focusImage=false}={}){await focus(page.locator('.guide'));await click(page.locator('.steps button').nth(index));await focus(page.locator('.workspace'));const button=page.getByRole('button',{name:'光屏移至理想像点',exact:true});if(await button.isEnabled())await click(button);await record();await focus(focusImage?page.locator('.screen-observation'):page.locator('.ray-diagram'));}
const actions={
 intro:async()=>{await page.evaluate(()=>scrollTo(0,0));},
 measureU:async()=>{await focus(page.locator('.ray-diagram'));await glow(page.getByTestId('object-distance-equation'));},
 measureD:async()=>{await glow(page.getByTestId('screen-distance-equation'));},
 think:async()=>{await focus(page.locator('.inquiry-panel'));await glow(page.locator('.prediction-fields'));},
 predict:async()=>{await pick('预测像的类型','real');await pick('预测像的方向','inverted');await pick('预测像的大小','same');await click(page.getByRole('button',{name:'提交预测，开始观察',exact:true}));},
 observe:async()=>{await focus(page.locator('.screen-observation'));await expect(page.getByTestId('screen-magnifier')).toBeVisible();await glow(page.locator('.observation-pair'));},
 zoom:async()=>{await click(page.getByRole('button',{name:'观察放大2倍',exact:true}));await expect(page.getByRole('spinbutton',{name:'光屏位置数值'})).toHaveValue('75');checks.push('观察倍率改变未移动光屏');},
 save:async()=>{await focus(page.locator('.inquiry-panel'));await pick('我实际观察到','clear');await point(page.getByLabel('观察说明',{exact:true}));await page.getByLabel('观察说明',{exact:true}).fill('同尺度比较：倒立、等大，屏上图案清晰。');await click(page.getByRole('button',{name:'保存本次观察',exact:true}));},
 reveal:async()=>{await click(page.getByRole('button',{name:'揭示理论并比较',exact:true}));await expect(page.getByTestId('theory-distance')).toHaveText('30.0cm');await glow(page.getByTestId('prediction-comparison'));checks.push('预测—观察—揭示完整执行，v=30 cm');},
 rays:async()=>{await focus(page.locator('.workspace'));await expect(page.locator('[data-ray="central-out"]')).toBeAttached();await glow(page.getByTestId('viewport'));},
 defocus:async()=>{await focus(page.locator('.workspace'));const input=page.getByRole('spinbutton',{name:'光屏位置数值',exact:true});await point(input);for(let n=76;n<=85;n++){await input.fill(String(n));await pause(150);}await input.press('Tab');await expect(page.getByTestId('theory-distance')).toHaveText('30.0cm');await expect(page.getByTestId('screen-status')).toContainText('模糊');checks.push('屏距 d=40 cm 时 v 仍为 30 cm 且离焦');},
 blur:async()=>{await focus(page.locator('.screen-observation'));await glow(page.getByTestId('screen-magnifier'));},
 refocus:async()=>{await focus(page.locator('.control-actions'));await click(page.getByRole('button',{name:'光屏移至理想像点',exact:true}));await expect(page.getByTestId('screen-status')).toHaveText('光屏成像清晰');await focus(page.locator('.screen-observation'));},
 demo:async()=>{await focus(page.locator('.inquiry-panel'));await click(page.getByRole('button',{name:'直接演示',exact:true}));await focus(page.locator('.screen-observation'));await click(page.getByRole('button',{name:'观察放大1倍',exact:true}));},
 far:async()=>{await caseStudy(0,{focusImage:true});await expect(page.getByTestId('theory-distance')).toHaveText('24.0cm');checks.push('u=40,v=24，倒立缩小实像');},
 between:async()=>{await caseStudy(2,{focusImage:true});await expect(page.getByTestId('theory-distance')).toHaveText('45.0cm');checks.push('u=22.5,v=45，倒立放大实像');},
 focus:async()=>{await caseStudy(3);await expect(page.getByTestId('theory-distance')).toHaveText('∞cm');await expect(page.getByRole('button',{name:'光屏移至理想像点'})).toBeDisabled();checks.push('u=f，平行出射，无有限实像');},
 virtual:async()=>{await caseStudy(4);await expect(page.getByTestId('theory-distance')).toHaveText('-30.0cm');await expect(page.locator('[data-ray="central-virtual"]')).toBeVisible();checks.push('u<f，正立放大虚像，反向延长虚线');},
 empty:async()=>{await focus(page.locator('.screen-observation'));await expect(page.getByTestId('screen-status')).toContainText('无法承接');await glow(page.getByTestId('screen-magnifier'));},
 records:async()=>{await focus(page.locator('.record-card'));await click(page.getByRole('button',{name:'查看数据'}));await expect(page.locator('.data-panel tbody tr')).toHaveCount(5);await focus(page.locator('.data-panel'));await glow(page.locator('.data-panel tbody tr').first());checks.push('记录五类情形，坐标与距离分列');},
 quiz:async()=>{await focus(page.locator('footer'));await click(page.getByRole('button',{name:'实验总结与自测',exact:true}));await page.locator('.quiz-section').evaluate(el=>el.scrollIntoView({block:'center',behavior:'smooth'}));await pause(800);await glow(page.getByTestId('question-prompt'));},
 wrong:async()=>{await click(page.locator('.quiz-options button').nth(0));await expect(page.locator('.quiz-explanation')).toContainText('这道题答错了');await page.locator('.quiz-explanation').evaluate(el=>el.scrollIntoView({block:'center',behavior:'smooth'}));await pause(800);await glow(page.locator('.quiz-explanation'));},
 boundary:async()=>{await click(page.getByRole('button',{name:'第2题',exact:true}));await click(page.locator('.quiz-options button').nth(2));await expect(page.locator('.quiz-explanation')).toContainText('回答正确');await page.locator('.quiz-explanation').evaluate(el=>el.scrollIntoView({block:'center',behavior:'smooth'}));await pause(800);await glow(page.locator('.quiz-explanation'));checks.push('两道易错题，正确与错误解析均展示');},
 summary:async()=>{await page.locator('.modal').evaluate(el=>el.scrollTo({top:0,behavior:'smooth'}));await pause(800);await glow(page.locator('.modal table'));}
};
if(startIndex>0){await click(page.getByRole('button',{name:'直接演示',exact:true}));await focus(page.locator('.guide'));await click(page.locator('.steps button').nth(4));await actions.records();}
const clock=performance.now();try{
 for(let i=startIndex;i<cues.length;i++){
  const cue=cues[i],color=[60+(i%4)*60,60+(Math.floor(i/4)%3)*80,80+Math.floor(i/12)*140];
  await page.evaluate(({cue,index,total,color})=>{document.getElementById('demo-chapter').textContent=cue.chapter;document.querySelector('#demo-caption p').textContent=cue.narration;document.getElementById('demo-counter').textContent=`${String(index+1).padStart(2,'0')} / ${total}`;document.getElementById('demo-sync').style.background=`rgb(${color.join(',')})`;document.getElementById('demo-highlight').style.display='none';},{cue,index:i,total:cues.length,color});
  const start=(performance.now()-clock)/1000;console.log(`CHAPTER ${i+1}/${cues.length}: ${cue.id}`);
  await actions[cue.id]();
  const chinese=(cue.narration.match(/[\u3400-\u9fff]/g)||[]).length;const target=Math.max(cue.minSeconds,chinese/4.3+1.5);const elapsed=(performance.now()-clock)/1000-start;await pause(Math.max(1500,(target-elapsed)*1000));
  timeline.push({...cue,color,start,end:(performance.now()-clock)/1000});
 }
 await pause(35000);
 await writeFile(path.join(output,'operation-log.json'),JSON.stringify({url,sourceVersion:'Stage 01 v1.2',videoSize:{width:1920,height:1080},errors,externalRequests:external,checks,timeline},null,2));
 const video=page.video();await context.close();const original=await video.path();await rename(original,path.join(output,'browser-recording.webm'));await browser.close();if(errors.length||external.length)throw new Error('Recording contained browser errors or external requests');console.log('RECORDING COMPLETE',path.join(output,'browser-recording.webm'));
}catch(error){await writeFile(path.join(output,'failure.json'),JSON.stringify({message:String(error),errors,external,timeline},null,2));await context.close();await browser.close();throw error;}
