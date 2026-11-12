from pathlib import Path
import json,math,subprocess,wave,shutil
import numpy as np
from fontTools.ttLib import TTFont
from fontTools import subset
R=Path(__file__).resolve().parents[1];sr=48000;seconds=16;n=sr*seconds;t=np.arange(n)/sr
out=R/'public/audio';out.mkdir(parents=True,exist_ok=True)
def wav(name,a):
 a=np.clip(a,-.95,.95);a=np.repeat(a[:,None],2,axis=1)
 with wave.open(str(out/name),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes((a*32767).astype('<i2').tobytes())
# Original, entirely procedural ambient pad and restrained post-production foley.
env=np.minimum(t/2,1)*np.minimum((seconds-t)/2,1)
music=sum(np.sin(2*np.pi*f*t+.05*np.sin(2*np.pi*.11*t+i)) for i,f in enumerate([146.832,220,293.665,369.994]))*.008*env
# Narration ducking is configured per track in Remotion.
rng=np.random.default_rng(12);sfx=np.zeros(n)
for at in [2.15,2.42,2.73,3.05,3.4,3.75]:
 m=int(.09*sr);x=np.arange(m)/sr;v=np.sin(2*np.pi*(340*x+700*x*x))*np.exp(-x*55)*.014;i=int(at*sr);sfx[i:i+m]+=v
ui=np.zeros(n);i=6*sr;x=np.arange(int(.18*sr))/sr;ui[i:i+len(x)]=np.sin(2*np.pi*880*x)*np.sin(np.pi*x/.18)**2*.017
wav('sample-music.wav',music);wav('sample-experiment.wav',sfx);wav('sample-ui.wav',ui)
subprocess.run(['ffmpeg','-v','error','-i',str(out/'sample-voice.mp3'),'-af','adelay=1000|1000,apad','-t','16','-ar',str(sr),'-ac','2',str(out/'sample-narration.wav'),'-y'],check=True)
raw=[json.loads(s) for s in (out/'sample-voice.jsonl').read_text().splitlines()];subs=[]
for i,s in enumerate(raw):
 start=1+s['offset']/1e7;end=min(16,start+s['duration']/1e7)
 if i+1<len(raw):end=min(end,1+raw[i+1]['offset']/1e7-.01)
 subs.append({'start':round(start,3),'end':round(end,3),'text':s['text']})
def stamp(v):
 ms=round(v*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(R/'output/sample-subtitles.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for i,s in enumerate(subs))+'\n')
config={'status':'TECHNICAL_SAMPLE_ONLY_NOT_COMPLETE_LESSON','brand':'智用实验室','slogan':'让知识真正动起来','fps':30,'width':1080,'height':1920,'durationInFrames':480,'sourceFile':'media/clock-probe.mp4','sourceFps':20,'sourceIn':0,'sourceOut':2,'liveStartFrame':60,'liveEndFrame':120,'equationStartFrame':180,'title':'气泡观察','badge':'采集技术样片 · 非完整成片','knowledgeTitle':'气泡 ≠ 已确认气体身份','knowledgeText':'观察到放气过程，还需要进一步检验证据。','equation':'CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂↑','subtitles':subs,'camera':{'centerX':.5,'centerY':.5,'scaleStart':1,'scaleEnd':1.035,'startFrame':0,'endFrame':30,'holdFrames':450,'focusRect':{'x':.36,'y':.6,'width':.29,'height':.31},'easing':'smoothstep'},'audioTracks':[{'name':'Narration','src':'audio/sample-narration.wav','gain':1},{'name':'Background Music','src':'audio/sample-music.wav','gain':1},{'name':'Experiment SFX','src':'audio/sample-experiment.wav','gain':1},{'name':'UI SFX','src':'audio/sample-ui.wav','gain':1}]}

for track in config['audioTracks']:
 track.update({'muted':False,'fadeInFrames':12,'fadeOutFrames':24,'duckDuringNarration':track['name']=='Background Music','duckGain':.5,'duckStartFrame':30,'duckEndFrame':440})
(R/'sample-timeline.json').write_text(json.dumps(config,ensure_ascii=False,indent=2))
chars=''.join(p.read_text(errors='ignore') for p in [R/'sample-timeline.json',R/'narration-draft.json',*list((R/'src').glob('*.tsx'))] if p.exists())+'采集技术样片非完整成片气泡观察原课件逐帧采集关键帧讲解气泡不等于身份检验模型可见现象不代表真实测量数据声音为后期拟音停止后续批次补录后再制作镜头配置字幕和音效已接入复用模板'
font=TTFont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',fontNumber=2);opt=subset.Options();opt.flavor='woff';sub=subset.Subsetter(options=opt);sub.populate(text=chars+''.join(chr(i) for i in range(32,127))+'₀₁₂₃₄₅₆₇₈₉↑↓→≠');sub.subset(font);font.flavor='woff';font.save(R/'public/fonts/ScienceSans.woff');shutil.copy2('/usr/share/doc/fonts-noto-cjk/copyright',R/'public/fonts/FONT-LICENSE.txt')
print('Sample config, original stems, SRT and portable CJK font ready.')
