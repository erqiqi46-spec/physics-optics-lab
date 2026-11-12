import subprocess,sys,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];T=json.loads((R/'timeline.json').read_text());raw=subprocess.check_output(['ffmpeg','-v','error','-i',sys.argv[1],'-vf','scale=108:192','-f','rawvideo','-pix_fmt','rgb24','-']);a=np.frombuffer(raw,dtype=np.uint8).reshape((-1,192,108,3));f=a[:,182:188,7:100].astype(float);score=np.abs(f-np.median(f,axis=0)).mean(axis=(1,2,3));bad=set(np.where(score>8)[0].tolist());regions={}
for s in T['shots']:
 start=s['startFrame']+10;end=s['endFrame'];b=a[start:end].astype(float);flags=set()
 for name,(y0,y1) in {'chapterTitle':(18,35),'knowledgeCard':(118,131)}.items():
  roi=b[:,y0:y1,7:100];d=np.abs(roi-np.median(roi,axis=0)).mean(axis=(1,2,3));flags.update((np.where(d>5)[0]+start).tolist())
 # Catch a blank or strongly damaged source region while allowing actual native movement.
 variance=b[:,40:112,6:102].std(axis=(1,2,3));flags.update((np.where(variance<np.median(variance)*.45)[0]+start).tolist());bad.update(flags);regions[s['shotId']]=sorted(flags)
print(json.dumps({'frames':sorted(bad),'maxScore':float(score.max()),'regionAnomalies':regions}))
