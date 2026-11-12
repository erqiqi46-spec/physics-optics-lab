from pathlib import Path
import json,subprocess,sys
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];T=json.loads((R/'timeline.json').read_text());inp=R/'output'/sys.argv[1];out=R/'frames/key-events';out.mkdir(exist_ok=True,parents=True);rows=[]
for s in T['shots']:
 if s['shotId'] not in ['airtightness','bubbles','limewater','fullness']:continue
 onset=s.get('phenomenonOnsetFrame',s.get('flipFrame'));pts=[('before-focus',0),('focus-ready',18),('before-event',onset-10),('during-event',onset+15),('after-event',min(s['durationInFrames']-10,onset+90))]
 sheet=Image.new('RGB',(1350,520),'#15232e')
 for i,(label,f) in enumerate(pts):
  p=out/(s['shotId']+'-'+label+'.jpg');g=s['startFrame']+f;subprocess.run(['ffmpeg','-v','error','-ss',str(g/30),'-i',str(inp),'-frames:v','1','-q:v','2','-y',str(p)],check=True);im=Image.open(p);im.thumbnail((260,470));sheet.paste(im,(i*270,30));ImageDraw.Draw(sheet).text((i*270+5,8),label,fill='white');rows.append({'shot':s['shotId'],'label':label,'globalFrame':g,'seconds':g/30,'path':str(p.relative_to(R))})
 sheet.save(out/(s['shotId']+'-contact.jpg'),quality=90)
(R/'reports/keyframe-crop-review.json').write_text(json.dumps({'frames':rows,'sourceAspect':'1080/810=4:3','displayAspect':'1000/750=4:3','maxDigitalScale':1.035,'fullFrameEffectiveWidth':1035,'sourceWidth':1080,'splitCrop':'Two panels cover cropped, no aspect stretching; splint flame and generator funnel visible','limitations':'Opening native dolly plus small digital pushes; source permits no continuous pouring animation'},ensure_ascii=False,indent=2));print('KEY_EVENT_FRAMES',len(rows))
