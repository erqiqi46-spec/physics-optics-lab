from pathlib import Path
import json,subprocess,sys,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];T=json.loads((R/'timeline.json').read_text());mode=sys.argv[1] if len(sys.argv)>1 else 'preview';file=R/'output'/('co2_science_video_1080x1920.mp4' if mode=='final' else 'co2_video_preview_render.mp4');target=(1080,1920) if mode=='final' else(540,960)
p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(file)]));v=next(s for s in p['streams'] if s['codec_type']=='video');a=next(s for s in p['streams'] if s['codec_type']=='audio');assert(v['width'],v['height'])==target;assert v['codec_name']=='h264' and a['codec_name']=='aac';assert v['r_frame_rate']=='30/1' and v['avg_frame_rate']=='30/1';assert v['pix_fmt'] in (['yuv420p'] if mode=='final' else ['yuv420p','yuvj420p']);assert a['channels']==2 and int(a['sample_rate'])==48000;
if mode=='final':assert v.get('color_range')=='tv' and v.get('color_space')=='bt709'
assert int(v['nb_frames'])==T['durationInFrames'];assert abs(float(p['format']['duration'])-T['durationSeconds'])<.15
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(file),'-vf','scale=108:192','-f','rawvideo','-pix_fmt','rgb24','-']);ims=np.frombuffer(raw,dtype=np.uint8).reshape((-1,192,108,3));assert len(ims)==T['durationInFrames'];black=np.where(ims.mean(axis=(1,2,3))<3)[0].tolist();assert not black
# Header and footer are static across chapters; detect displaced/composited page captures.
footer=ims[:,182:188,7:100].astype(float);ref=np.median(footer,axis=0);scores=np.abs(footer-ref).mean(axis=(1,2,3));regionScan=json.loads(subprocess.check_output(['python3',str(R/'scripts/scan-composite.py'),str(file)]));suspects=regionScan['frames']
subs=json.loads((R/'public/film-subtitles.json').read_text());last=0
for s in subs:
 assert s['end']>s['start']>=last-.001 and s['end']<T['durationSeconds'];assert len(s['text'])<=36;last=s['end']
attention=[]
for s in T['shots']:
 if s.get('attention'):
  q=s['attention'];assert q['cameraReadyFrame']<q['startFrame'];assert s.get('phenomenonOnsetFrame',s.get('flipFrame'))>q['endFrame'];attention.append(s['shotId'])
assert len(T['audioTracks'])==4 and json.loads((R/'reports/raw-complete-qa.json').read_text())['passed']
report={'passed':not suspects,'file':file.name,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'pixelFormat':v['pix_fmt'],'colorRange':v.get('color_range'),'colorSpace':v.get('color_space'),'audioChannels':a['channels'],'audioSampleRate':a['sample_rate'],'videoCodec':v['codec_name'],'audioCodec':a['codec_name'],'frames':len(ims),'durationSeconds':p['format']['duration'],'blackFrames':black,'compositeSuspectFrames':suspects,'regionChecks':regionScan['regionAnomalies'],'footerScoreMax':float(scores.max()),'subtitleChunks':len(subs),'attentionTimingPassed':attention,'audioTracks':4,'scope':'Automated encoding, source, nonblank, stable footer/title/knowledge-card regions, nonblank source, subtitle and timing checks; visual review documented separately'}
(R/'reports'/('film-'+mode+'-validation.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False));sys.exit(0 if report['passed'] else 2)
