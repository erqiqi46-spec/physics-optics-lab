from pathlib import Path
import json,subprocess,wave,math,shutil
import numpy as np
from fontTools.ttLib import TTFont
from fontTools import subset
R=Path(__file__).resolve().parents[1];p=R/'timeline.json';T=json.loads(p.read_text());sr=48000;duration=T['durationInFrames']/T['fps'];n=round(duration*sr);tracks=R/'output/audio_stems';tracks.mkdir(parents=True,exist_ok=True);public=R/'public/audio/film';public.mkdir(parents=True,exist_ok=True)
def wav(path,a):
 if a.ndim==1:a=np.repeat(a[:,None],2,axis=1)
 with wave.open(str(path),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(a,-.97,.97)*32767).astype('<i2').tobytes())
voice=np.zeros(n,dtype=np.float32);speech=np.zeros(n,dtype=np.float32)
for s in T['shots']:
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(R/'public'/s['audioFile']),'-ar',str(sr),'-ac','1','-f','f32le','-']);a=np.frombuffer(data,dtype='<f4');start=round((s['startFrame']+s['narrationDelayFrames'])/T['fps']*sr);end=min(n,start+len(a));voice[start:end]+=a[:end-start];speech[max(0,start-int(.2*sr)):min(n,end+int(.2*sr))]=1
wav(tracks/'narration.wav',voice);del voice
t=np.arange(n,dtype=np.float32)/sr;envelope=np.minimum(t/2,1)*np.minimum((duration-t)/3,1);duck=np.where(speech>0,.32,1).astype(np.float32)
# Original restrained ambient pad, with slow harmonic changes; no external music or samples.
music=np.zeros(n,dtype=np.float32)
for i,freq in enumerate([146.832,220,293.665,369.994]):music+=np.sin(2*np.pi*freq*t+.06*np.sin(2*np.pi*(.07+i*.011)*t+i))*.008
music*=envelope*duck
experiment=np.zeros(n,dtype=np.float32);ui=np.zeros(n,dtype=np.float32)
def pulse(dst,at,kind='bubble',amp=.013):
 count=round((.1 if kind=='bubble' else .18)*sr);x=np.arange(count)/sr
 if kind=='bubble':v=np.sin(2*np.pi*(330*x+900*x*x))*np.exp(-x*50)*amp
 elif kind=='glass':v=(np.sin(2*np.pi*950*x)+.5*np.sin(2*np.pi*1410*x))*np.exp(-x*35)*amp
 elif kind=='warning':v=(np.sin(2*np.pi*440*x)+.35*np.sin(2*np.pi*660*x))*np.sin(np.pi*x/.18)**2*amp
 else:v=np.sin(2*np.pi*880*x)*np.sin(np.pi*x/.18)**2*amp
 start=round(at*sr)
 if 0<=start<n:dst[start:min(n,start+count)]+=v[:min(count,n-start)]
for s in T['shots']:
 base=s['startFrame']/T['fps'];pulse(ui,base+.35,'confirm',.006)
 if s['shotId']=='airtightness':pulse(experiment,base+.8,'glass',.012);pulse(ui,base+s['flipFrame']/T['fps']+.4,'confirm',.012)
 if s['shotId']=='reagents':
  for at in s.get('cutFrames',[]):pulse(experiment,base+at/T['fps'],'glass',.012)
 if s['shotId'] in ['bubbles','limewater']:
  a=s['videoStartFrame']/T['fps']+base+s['phenomenonOnsetSourceSeconds'];end=base+s['videoStartFrame']/T['fps']+s['sources'][s['videoSourceIndex']]['duration']
  for v in np.arange(a,end,.34):pulse(experiment,float(v),'bubble',.009)
  if s['shotId']=='limewater':pulse(ui,end+.25,'confirm',.008);start=max(0,round((a-.3)*sr));stop=min(n,round((end+.5)*sr));music[start:stop]*=.35
 if s['shotId']=='fullness':
  at=base+s['phenomenonOnsetFrame']/T['fps'];music[max(0,round((at-.3)*sr)):min(n,round((at+.7)*sr))]*=.15
 if s['shotId'] in ['inside_error','funnel_error']:pulse(ui,base+.5,'warning',.009)
wav(tracks/'background_music.wav',music);wav(tracks/'experiment_sfx.wav',experiment);wav(tracks/'ui_sfx.wav',ui)
for file in tracks.glob('*.wav'):shutil.copy2(file,public/file.name)
T['audioTracks']=[{'name':name,'src':'audio/film/'+file,'gain':1,'muted':False} for name,file in [('Narration','narration.wav'),('Background Music','background_music.wav'),('Experiment SFX','experiment_sfx.wav'),('UI SFX','ui_sfx.wav')]]
p.write_text(json.dumps(T,ensure_ascii=False,indent=2));(R/'output/timeline.json').write_text(json.dumps(T,ensure_ascii=False,indent=2))
chars=''.join(f.read_text(errors='ignore') for f in [p,R/'narration-draft.json',*list((R/'src').glob('*.tsx'))])+'₀₁₂₃₄₅₆₇₈₉↑↓→≠'+''.join(chr(i) for i in range(32,127))
font=TTFont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',fontNumber=2);opts=subset.Options();sub=subset.Subsetter(options=opts);sub.populate(text=chars);sub.subset(font);font.flavor='woff';font.save(R/'public/fonts/ScienceSans.woff')
(R/'reports/audio-sources.json').write_text(json.dumps({'durationSeconds':duration,'sampleRate':sr,'stereo':True,'narration':'Generic Microsoft zh-CN-YunxiNeural synthetic Mandarin, not a person imitation','music':'Original procedural sine-pad composition; no third-party samples','experiment':'Original procedural post-production foley, not a live lab recording','ui':'Original quiet confirmation and amber-warning tones','ducking':'BGM reduced during narration and key visual events','tracks':T['audioTracks']},ensure_ascii=False,indent=2))
print('AUDIO_STEMS_READY',duration)
