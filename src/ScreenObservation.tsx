import {useEffect,useRef,useState} from 'react';
import {Eye} from 'lucide-react';
import type {Setup} from './physics';
import {objectReference,screenObservation} from './imaging';
export default function ScreenObservation({s,locked}:{s:Setup;locked:boolean}){
 const screen=useRef<HTMLCanvasElement>(null),object=useRef<HTMLCanvasElement>(null),[zoom,setZoom]=useState(1);
 useEffect(()=>{if(locked)setZoom(1);},[locked]);
 useEffect(()=>{if(locked)return;screen.current?.getContext('2d')?.drawImage(screenObservation(s),0,0);object.current?.getContext('2d')?.drawImage(objectReference(),0,0);},[s,locked]);
 return <section className="screen-observation" aria-labelledby="screen-observation-title"><h3 id="screen-observation-title"><Eye size={16}/>光屏放大观察</h3>{locked?<div className="screen-locked"><p>先提交预测，再查看光屏细节。</p><button onClick={()=>document.getElementById('prediction-form')?.scrollIntoView({behavior:'smooth',block:'center'})}>前往填写预测</button></div>:<><p className="screen-coordinates">轨道坐标 xₛ = {s.screen.toFixed(1)} cm<br/>实际屏距 d = {(s.screen-s.lens).toFixed(1)} cm（从透镜量起）</p><div className="observation-zoom" aria-label="观察倍率">{[1,2,3].map(n=><button key={n} aria-pressed={zoom===n} onClick={()=>setZoom(n)} aria-label={`观察放大${n}倍`}>{n}×</button>)}</div><div className="observation-pair"><figure><div className="screen-surface"><canvas ref={object} width="512" height="512" style={{transform:`scale(${zoom})`}} aria-label="物体图案，同尺度参考"/></div><figcaption>物体图案</figcaption></figure><figure><div className="screen-surface paper"><canvas data-testid="screen-magnifier" ref={screen} width="512" height="512" style={{transform:`scale(${zoom})`}} aria-label="实际光屏正面图像，随光屏移动实时变化"/></div><figcaption>实际光屏正面</figcaption></figure></div><p className="observation-note">两幅图按相同物理尺度显示；观察倍率同步放大两幅视图，不改变仪器、焦距或像的真实大小。2×、3×时仅显示局部。</p><p className="observation-note">这是屏面的实时投影，不是理论像点示意。离焦会模糊，不能承接时光屏为空白。照明外观与三维视角可能不同。</p></>}</section>;
}
