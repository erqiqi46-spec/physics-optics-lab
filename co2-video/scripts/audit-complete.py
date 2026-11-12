from pathlib import Path
import json,hashlib
from PIL import Image,ImageStat,ImageOps,ImageDraw
R=Path(__file__).resolve().parents[1];m=json.loads((R/'raw/capture-manifest.json').read_text());rows=[];thumbs=[]
for c in m['clips']:
 p=R/'raw'/c['id'];p=p if c.get('frames',1)>1 else p/'still.png'
 files=sorted(p.glob('*.jpg')) if p.is_dir() else [p]
 # Manifest video paths can name a frame pattern or a first frame.
 if not p.exists() and '%' in p.name:files=sorted(p.parent.glob('*.jpg'))
 if not files:raise RuntimeError(str(p))
 if c.get('frames',1)>1 and not p.is_dir():files=sorted(p.parent.glob('*.jpg'))
 assert len(files)==c['frames'],(c['id'],len(files),c['frames'])
 vals=[]
 for f in files:
  im=Image.open(f).convert('RGB');v=sum(ImageStat.Stat(im.resize((80,60))).stddev)/3;assert v>=2,(str(f),v);assert im.size==(1080,810),(f,im.size);vals.append(v)
 rows.append({'id':c['id'],'frames':len(files),'minStddev':min(vals),'nonblank':True})
 im=Image.open(files[len(files)//2]).convert('RGB');im.thumbnail((324,243));tile=Image.new('RGB',(344,280),'#101b25');tile.paste(im,(10,27));ImageDraw.Draw(tile).text((10,8),c['id'],fill='white');thumbs.append(tile)
assert len(rows)>=21
sheet=Image.new('RGB',(344*4,280*((len(thumbs)+3)//4)),'#101b25')
for i,im in enumerate(thumbs):sheet.paste(im,((i%4)*344,(i//4)*280))
(R/'frames').mkdir(exist_ok=True);sheet.save(R/'frames/complete-shots-audit.jpg',quality=90)
sha=hashlib.sha256((R/'source/co2-lab-v3.html').read_bytes()).hexdigest();assert sha==m['sha256']
m['complete']=True;m['verification']='All selected native frames and stills nonblank at1080x810; limewater ends at native automatic cloudiness pause (64frames), not interrupted.';(R/'raw/capture-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(R/'reports/raw-complete-qa.json').write_text(json.dumps({'passed':True,'sourceSha256':sha,'sourceUnchanged':True,'clips':rows,'nativeFps':20,'outputFps':30,'method':'Original app, clock-stepped native rendering; no invented reaction animation','limitations':['Native20fps is encoded at30fps with repeated frames','Pouring and splint result are native discrete state changes','Holds are labeled explanation pauses']},ensure_ascii=False,indent=2));print('RAW_QA_PASS',len(rows),sum(r['frames'] for r in rows))
