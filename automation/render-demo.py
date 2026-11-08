#!/usr/bin/env python3
"""Convert the real browser recording to MP4 and derive subtitles from visible cue markers."""
from pathlib import Path
import argparse,hashlib,json,math,subprocess,textwrap
from PIL import Image,ImageDraw,ImageFont
parser=argparse.ArgumentParser();parser.add_argument('recording_dir',nargs='?',default='recordings');parser.add_argument('--tail-dir');args=parser.parse_args()
root=Path(args.recording_dir).resolve();log=json.loads((root/'operation-log.json').read_text());raw=root/'browser-recording.webm'
def probe(file):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-show_chapters','-of','json',str(file)]))
meta=probe(raw);duration=float(meta['format']['duration'])
print('Scanning recording markers for subtitle alignment...',flush=True)
colors=[c['color'] for c in log['timeline']]
def scan(file):
 result=subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(file),'-vf','fps=10,crop=8:8:4:4,scale=1:1,format=rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE,check=True)
 found={};current=-1
 for index in range(len(result.stdout)//3):
  pixel=result.stdout[index*3:index*3+3];distances=[sum((pixel[k]-c[k])**2 for k in range(3)) for c in colors];best=min(range(len(colors)),key=lambda i:distances[i])
  if distances[best]<35**2 and best>=current:found.setdefault(best,index/10);current=best
 return found
first=scan(raw);trim=first[0];tail_dir=Path(args.tail_dir).resolve() if args.tail_dir else root/'tail';tail=tail_dir/'browser-recording.webm';chapters=[];take_count=1
if tail.exists():
 tail_log=json.loads((tail_dir/'operation-log.json').read_text());tail_first=scan(tail)
 if not set(range(20)).issubset(first) or not set(range(20,24)).issubset(tail_first):raise RuntimeError('A required chapter is missing from the retained takes')
 take_count=2;prefix_duration=first[20]-trim;tail_start=tail_first[20]
 last=log['timeline'][-1];last_hold=max(last['minSeconds'],len([c for c in last['narration'] if '\u3400'<=c<='\u9fff'])/4.3+1.5)+.5
 tail_end=min(float(probe(tail)['format']['duration']),tail_first[23]+last_hold)
 total=prefix_duration+tail_end-tail_start
 starts=[first[i]-trim if i<20 else prefix_duration+tail_first[i]-tail_start for i in range(24)]
 video_filter=f'[0:v]trim=start={trim}:end={first[20]},setpts=PTS-STARTPTS[v0];[1:v]trim=start={tail_start}:end={tail_end},setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0,drawbox=x=0:y=0:w=20:h=20:color=0x0b1520:t=fill,fps=25,format=yuv420p[v]'
 inputs=['-i',str(raw),'-i',str(tail)];map_args=['-filter_complex',video_filter,'-map','[v]'];metadata_index='2'
 log['errors']+=tail_log['errors'];log['externalRequests']+=tail_log['externalRequests']
else:
 if len(first)!=len(colors):raise RuntimeError(f'Missing chapter markers: {set(range(len(colors)))-set(first)}')
 last=log['timeline'][-1];last_hold=max(last['minSeconds'],len([c for c in last['narration'] if '\u3400'<=c<='\u9fff'])/4.3+1.5)+.5
 end=min(duration,first[len(colors)-1]+last_hold);total=end-trim;starts=[first[i]-trim for i in range(len(colors))]
 inputs=['-ss',str(trim),'-i',str(raw)];map_args=['-t',str(total),'-map','0:v:0','-vf','drawbox=x=0:y=0:w=20:h=20:color=0x0b1520:t=fill,fps=25,format=yuv420p'];metadata_index='1'
for i,cue in enumerate(log['timeline']):chapters.append({**cue,'videoStart':round(starts[i],3),'videoEnd':round(starts[i+1] if i+1<len(starts) else total,3),'take':2 if take_count==2 and i>=20 else 1})
print(f'All {len(chapters)} chapters recovered across {take_count} recording take(s).',flush=True)
out=root/'optics-lab-teaching-demo.mp4'
chapter_file=root/'chapters.ffmetadata';chapter_file.write_text(';FFMETADATA1\ntitle=凸透镜成像教学演示\n'+''.join(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(c["videoStart"]*1000)}\nEND={round(c["videoEnd"]*1000)}\ntitle={c["chapter"]}\n' for c in chapters))
command=['ffmpeg','-y','-hide_banner','-loglevel','warning',*inputs,'-i',str(chapter_file),*map_args,'-map_metadata',metadata_index,'-map_chapters',metadata_index,'-an','-c:v','libx264','-preset','veryfast','-crf','22','-threads','2','-movflags','+faststart',str(out)]
print('Encoding 1920×1080 H.264 MP4...',flush=True);subprocess.run(command,check=True)
if out.stat().st_size>90*1024*1024:
 command[command.index('22')]='25';print('Reducing bitrate to fit the distribution limit...',flush=True);subprocess.run(command,check=True)
def stamp(seconds,srt=False):
 milliseconds=round(max(0,seconds)*1000);h,m=divmod(milliseconds//1000,3600);m,s=divmod(m,60);return f'{h:02d}:{m:02d}:{s:02d}'+(',' if srt else '.')+f'{milliseconds%1000:03d}'
def wrap(text,width=42):
 lines=[]
 while len(text)>width:
  end=max([i+1 for i,ch in enumerate(text[:width]) if ch in '，。；：' and i>width//2] or [width]);lines.append(text[:end]);text=text[end:]
 return '\n'.join(lines+[text])
srt='\n\n'.join(f'{i+1}\n{stamp(c["videoStart"],True)} --> {stamp(c["videoEnd"],True)}\n{wrap(c["narration"])}' for i,c in enumerate(chapters))+'\n'
(root/'teaching-subtitles.srt').write_text(srt,encoding='utf-8-sig')
script='# 凸透镜成像 · 口播教学讲解稿\n\n对应 Stage 01 v1.2 实际网页自动演示。MP4 已内嵌逐步骤同步字幕；此版本没有合成配音，以下文字供教师口播或后期配音。字幕时段从实际录屏的可见章节标记恢复。\n\n'
for i,c in enumerate(chapters):script+=f'## {i+1:02d} · {c["chapter"]}（{stamp(c["videoStart"])}—{stamp(c["videoEnd"])}）\n\n{c["narration"]}\n\n'
script+='## 使用提示\n\n- 视频中的页面操作均由自动化脚本执行，光学状态仍由课件计算；录制叠加了字幕、鼠标指示与点击高亮。\n- 预测环节可暂停，让学生独立判断。五类情境比较期间保持焦距 15 cm。\n- 这是理想近轴薄透镜模型。实线为辅助传播示意，虚线为数学反向延长线，不代表光逆向传播。\n- SRT 供剪辑使用，MP4 本身已带字幕，播放时不必再次加载 SRT，避免字幕重复。\n'
(root/'teaching-narration.md').write_text(script)
(root/'chapter-timeline.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2))
steps={'intro':'打开 v1.2，等待三维器材就绪；保留默认先预测模式','measureU':'定位测量侧视图，高亮 u 的坐标差算式','measureD':'高亮 d 的坐标差算式','think':'回到预测面板，留出思考暂停','predict':'依次选择实像、倒立、等大并提交','observe':'定位同尺度参考与实际光屏','zoom':'选择观察放大 2×，校验仪器未移动','save':'填写清晰现象与观察说明，保存观察','reveal':'揭示，校验理论像距 30 cm','rays':'展示三维主光线与传播箭头','defocus':'实际光屏坐标从 75 逐步调至 85 cm，校验 d=40 且 v=30','blur':'查看离焦后的真实屏面投影','refocus':'点击自动对焦并校验恢复清晰','demo':'切换教师直接演示，观察倍率恢复为 1×','far':'切换 u>2f，调屏至像点，保存并查看缩小实像','between':'切换 f<u<2f，保存并查看放大实像','focus':'切换 u=f，保存并查看平行出射与空白屏','virtual':'切换 u<f，保存并查看反向延长线','empty':'检查虚像情形的空白光屏','records':'打开五组数据表','quiz':'打开课堂自测第 1 题','wrong':'故意选择常见错误，展示解析','boundary':'完成第 2 题并展示焦点边界解释','summary':'回到五类成像规律表'}
flow='# 自动化网页操作流程\n\n脚本：`automation/record-demo.mjs`。录制源为当前仓库 `docs/index.html`，使用隔离的浏览器上下文，不混入历史学生数据。所有仪器和题目操作通过页面控件进行，未直接改写 React 状态或物理结果。\n\n|步骤|时段|真实网页操作|\n|---|---|---|\n'
for i,c in enumerate(chapters):flow+=f'|{i+1:02d}|{stamp(c["videoStart"])}—{stamp(c["videoEnd"])}|{steps[c["id"]]}|\n'
(root/'automation-flow.md').write_text(flow)
metadata=probe(out);stream=next(s for s in metadata['streams'] if s['codec_type']=='video');assert stream['codec_name']=='h264' and stream['width']==1920 and stream['height']==1080 and stream['pix_fmt']=='yuv420p'
validation={'sourceVersion':log['sourceVersion'],'source':'actual browser automation recording','recordingTakes':take_count,'codec':stream['codec_name'],'width':stream['width'],'height':stream['height'],'pixelFormat':stream['pix_fmt'],'fps':stream['avg_frame_rate'],'durationSeconds':float(metadata['format']['duration']),'sizeBytes':out.stat().st_size,'chapters':len(chapters),'embeddedChapters':len(metadata.get('chapters',[])),'subtitles':'burned in and sidecar SRT','audio':'none; teacher narration script included','startupTrimSeconds':trim,'browserErrors':log['errors'],'externalRequests':log['externalRequests'],'passedChecks':log['checks'],'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
assert not validation['browserErrors'] and not validation['externalRequests'];(root/'video-validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2))
# Capture stable frames near the end of selected chapters for review.
shots=[]
for name in ['intro','zoom','rays','between','virtual','wrong']:
 c=next(c for c in chapters if c['id']==name);shot=root/f'qa-{name}.jpg';subprocess.run(['ffmpeg','-y','-v','error','-ss',str(max(c['videoStart'],c['videoEnd']-1)),'-i',str(out),'-frames:v','1','-q:v','2',str(shot)],check=True);shots.append((c,shot))
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',20);sheet=Image.new('RGB',(1440,3*440),'#0b1520');draw=ImageDraw.Draw(sheet)
for i,(c,shot) in enumerate(shots):
 image=Image.open(shot).resize((704,396));x=(i%2)*720+8;y=(i//2)*440+34;sheet.paste(image,(x,y));draw.text((x,y-28),f'{c["chapter"]}  {stamp(c["videoEnd"]-1)}',font=font,fill='#d7eee2')
sheet.save(root/'review-contact-sheet.jpg',quality=92);subprocess.run(['ffmpeg','-y','-v','error','-ss',str(next(c for c in chapters if c['id']=='rays')['videoEnd']-1),'-i',str(out),'-frames:v','1','-q:v','2',str(root/'teaching-demo-poster.jpg')],check=True)
print(json.dumps(validation,ensure_ascii=False,indent=2),flush=True)
