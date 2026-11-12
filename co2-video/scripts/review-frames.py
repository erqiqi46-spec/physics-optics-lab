from pathlib import Path
import json,subprocess,sys
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];T=json.loads((R/'timeline.json').read_text());inp=R/'output'/sys.argv[1];folder=R/'frames'/('final' if '1080' in inp.name else 'preview');folder.mkdir(exist_ok=True,parents=True)
items=[]
for s in T['shots']:
 f=s['startFrame']+min(200,s['durationInFrames']//2);items.append((s['shotId'],f))
 if s.get('phenomenonOnsetFrame'):
  for label,delta in [('before',-10),('onset',0),('mid',15),('after',70)]:items.append((s['shotId']+'-'+label,s['startFrame']+s['phenomenonOnsetFrame']+delta))
for name,f in items:
 p=folder/(name+'.jpg');subprocess.run(['ffmpeg','-v','error','-ss',str(f/30),'-i',str(inp),'-frames:v','1','-q:v','2','-y',str(p)],check=True)
thumbs=[]
for name,f in items:
 im=Image.open(folder/(name+'.jpg')).convert('RGB');im.thumbnail((270,480));tile=Image.new('RGB',(290,515),'#172028');tile.paste(im,(10,26));ImageDraw.Draw(tile).text((10,8),name+' '+str(f),fill='white');thumbs.append(tile)
w=290*4;h=515*((len(thumbs)+3)//4);sheet=Image.new('RGB',(w,h),'#172028')
for i,im in enumerate(thumbs):sheet.paste(im,((i%4)*290,(i//4)*515))
sheet.save(folder/'contact.jpg',quality=90);(folder/'frame-index.json').write_text(json.dumps(items));print(folder/'contact.jpg')
