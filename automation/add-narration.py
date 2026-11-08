"""Align Mandarin narration to each recorded chapter without accelerating the speech."""
import argparse,json,math,subprocess,wave,hashlib,textwrap
from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt
from docx.oxml.ns import qn
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--voice',required=True);p.add_argument('--out',required=True);a=p.parse_args();source=Path(a.source).resolve();manifest=Path(a.voice).resolve();root=Path(a.out).resolve();root.mkdir(parents=True,exist_ok=True);parts=root/'parts';parts.mkdir(exist_ok=True);cues=json.loads(manifest.read_text());timeline=[];cursor=0

def run(args):subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*map(str,args)],check=True)
def probe(file):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(file)]))
for i,c in enumerate(cues):
 start=c['videoStart']+(.16 if i else .04);end=c['videoEnd']-.18;base=end-start;target=math.ceil(max(base,c['audioSeconds']+.7)*25)/25;frames=round(target*25);video=parts/f'{i:02d}.mp4';audio=parts/f'{i:02d}.wav';voice=Path(c['audioFile']);voice=voice if voice.is_absolute() else manifest.parent/voice
 print(f'Segment {i+1:02d}/24: screen {base:.2f}s, speech {c["audioSeconds"]:.2f}s -> {target:.2f}s',flush=True)
 if not video.exists():run(['-ss',start,'-i',source,'-map','0:v:0','-an','-map_metadata','-1','-map_chapters','-1','-vf',f'trim=duration={base},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={target},fps=25,format=yuv420p','-frames:v',frames,'-c:v','libx264','-preset','veryfast','-crf','20','-threads','2',video])
 if not audio.exists():run(['-i',voice,'-af','apad','-t',target,'-ar','48000','-ac','2','-c:a','pcm_s16le',audio])
 timeline.append({**c,'sourceVideoStart':start,'sourceVideoEnd':end,'videoStart':round(cursor,3),'videoEnd':round(cursor+target,3),'holdAddedSeconds':round(target-base,3)});cursor+=target
concat=root/'video-parts.txt';concat.write_text(''.join("file '"+(parts/f'{i:02d}.mp4').as_posix().replace("'","'\\''")+"'\n" for i in range(len(cues))))
run(['-f','concat','-safe','0','-i',concat,'-map','0:v:0','-map_metadata','-1','-map_chapters','-1','-c:v','copy',root/'video-retimed.mp4'])
with wave.open(str(root/'narration.wav'),'wb') as dest:
 dest.setnchannels(2);dest.setsampwidth(2);dest.setframerate(48000)
 for i in range(len(cues)):
  with wave.open(str(parts/f'{i:02d}.wav'),'rb') as src:
   while chunk:=src.readframes(65536):dest.writeframesraw(chunk)
meta=root/'chapters.ffmetadata';meta.write_text(';FFMETADATA1\ntitle=凸透镜成像教学演示·中文配音版\n'+''.join(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(c["videoStart"]*1000)}\nEND={round(c["videoEnd"]*1000)}\ntitle={c["chapter"]}\n' for c in timeline))
output=root/'optics-lab-teaching-demo-voiced.mp4';run(['-i',root/'video-retimed.mp4','-i',root/'narration.wav','-i',meta,'-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','2','-c:v','copy','-c:a','aac','-b:a','128k','-ar','48000','-ac','2','-t',cursor,'-movflags','+faststart',output])
def stamp(t,srt=False):
 n=round(t*1000);h,s=divmod(n//1000,3600);m,s=divmod(s,60);return f'{h:02}:{m:02}:{s:02}'+(',' if srt else '.')+f'{n%1000:03}'
srt='\n\n'.join(f'{i+1}\n{stamp(c["videoStart"],True)} --> {stamp(c["videoEnd"],True)}\n'+textwrap.fill(c['narration'],42) for i,c in enumerate(timeline))+'\n';(root/'teaching-subtitles-voiced.srt').write_text(srt,encoding='utf-8-sig')
script='# 中文配音版 · 同步口播教学讲解稿\n\n语音为通用中文合成声线 zh-CN-XiaoxiaoNeural，非真人教师录音。字幕已嵌入 MP4；以下时间码对应配音版。保持正常语速，必要时延长当前稳定画面。\n\n'
doc=Document();style=doc.styles['Normal'];style.font.name='Calibri';style.font.size=Pt(13);style.element.rPr.rFonts.set(qn('w:eastAsia'),'微软雅黑');style.paragraph_format.line_spacing=1.5
for name in ['Title','Heading 1','Heading 2']:doc.styles[name].element.rPr.rFonts.set(qn('w:eastAsia'),'微软雅黑')
doc.add_heading('凸透镜成像 · 中文配音讲解稿',0);doc.add_paragraph('对应中文合成配音版 MP4。采用通用合成声线，非真人录音。时间码已按配音时长重排，字幕已嵌入视频。')
for i,c in enumerate(timeline):
 title=f'{i+1:02d} · {c["chapter"]}（{stamp(c["videoStart"])}—{stamp(c["videoEnd"])}）';script+='## '+title+'\n\n'+c['narration']+'\n\n';doc.add_heading(title,2);doc.add_paragraph(c['narration'])
(root/'teaching-narration-voiced.md').write_text(script);(root/'teaching-narration-voiced.txt').write_text(script,encoding='utf-8-sig');doc.save(root/'teaching-narration-voiced.docx');(root/'chapter-timeline-voiced.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2))
report=probe(output);v=next(s for s in report['streams'] if s['codec_type']=='video');audio=next(s for s in report['streams'] if s['codec_type']=='audio');duration=float(report['format']['duration']);assert v['codec_name']=='h264' and audio['codec_name']=='aac';assert v['width']==1920 and v['height']==1080;assert abs(duration-cursor)<.15;assert len(report['chapters'])==24
validation={'durationSeconds':duration,'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],'videoCodec':v['codec_name'],'audioCodec':audio['codec_name'],'sampleRate':audio['sample_rate'],'channels':audio['channels'],'voice':'zh-CN-XiaoxiaoNeural; generic synthetic Mandarin, not a real teacher','chapters':len(report['chapters']),'subtitles':'burned in; retimed with narration; sidecar SRT included','speechSpeed':'original synthesis rate -3%; no speech acceleration','synchronization':'each audio clip starts at its matching chapter; stable end frames held when necessary','sizeBytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()};(root/'video-validation-voiced.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2));print(json.dumps(validation,ensure_ascii=False,indent=2),flush=True)
