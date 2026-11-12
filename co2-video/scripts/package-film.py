from pathlib import Path
import zipfile,json,hashlib,shutil
R=Path(__file__).resolve().parents[1];dest=R.parent/'downloads';dest.mkdir(exist_ok=True);out=dest/'co2-v3-complete-video-project.zip'
assert json.loads((R/'reports/film-final-validation.json').read_text())['passed']
selected=[]
for top in ['src','scripts','source','reports','public']:
 selected.extend(p for p in(R/top).rglob('*') if p.is_file() and '__pycache__' not in str(p))
for name in ['README.md','requirements.txt','sample-timeline.json','voice-cues.json','package.json','package-lock.json','timeline.json','narration-draft.json','voice-cues-words.json','public/film-subtitles.json']:
 selected.append(R/name)
for name in ['co2_science_video_1080x1920.mp4','co2_video_preview.mp4','co2_science_subtitles.srt','narration-final.md']:
 selected.append(R/'output'/name)
# The identical four independent WAV stems are included once under public/audio/film.
selected.extend((R/'public/audio/voice-words').glob('*'))
m=json.loads((R/'raw/capture-manifest.json').read_text());selected.append(R/'raw/capture-manifest.json')
for c in m['clips']:
 folder=R/'raw'/c['id'];selected.extend(p for p in folder.glob('*') if p.is_file())
for folder in [R/'frames/final',R/'frames/preview',R/'frames/key-events']:
 selected.extend(p for p in folder.glob('*') if p.is_file())
selected.extend(p for p in(R/'frames').glob('*audit.jpg') if p.is_file() and 'glitch' not in p.name)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(set(selected)):
  if p.exists():z.write(p,'co2-video/'+str(p.relative_to(R)))
with zipfile.ZipFile(out) as z:assert z.testzip() is None
for src,name in [(R/'output/co2_science_video_1080x1920.mp4','co2-v3-complete-teaching-video.mp4'),(R/'output/co2_video_preview.mp4','co2-v3-complete-preview.mp4'),(R/'output/narration-final.md','co2-v3-narration.md'),(R/'output/co2_science_subtitles.srt','co2-v3-subtitles.srt')]:shutil.copy2(src,dest/name)
files=[out,*[dest/n for n in ['co2-v3-complete-teaching-video.mp4','co2-v3-complete-preview.mp4','co2-v3-narration.md','co2-v3-subtitles.srt']]]
manifest={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files};(dest/'co2-v3-video-delivery.json').write_text(json.dumps(manifest,indent=2));delivery=Path('/workspace/output');delivery.mkdir(exist_ok=True)
for p in files:shutil.copy2(p,delivery/p.name)
print(json.dumps(manifest,indent=2))
