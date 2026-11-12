from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,shutil,json
R=Path(__file__).resolve().parents[1];dest=R.parent/'downloads';dest.mkdir(exist_ok=True)
zip_path=dest/'co2-video-stage01-review.zip'
with ZipFile(zip_path,'w',ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(R.rglob('*')):
  if not p.is_file():continue
  parts=p.relative_to(R).parts
  if any(x in {'node_modules','.cache','.venv','__pycache__'} for x in parts):continue
  if p.name=='co2_capture_technical_preview.mp4':continue
  z.write(p,'co2-video/'+str(p.relative_to(R)))
with ZipFile(zip_path) as z:assert z.testzip() is None
for source,name in [(R/'output/co2_capture_technical_sample.mp4','co2-video-stage01-sample.mp4'),(R/'output/narration-draft.mp3','co2-video-narration-draft.mp3')]:shutil.copy2(source,dest/name)
print('ARCHIVE',zip_path.stat().st_size,'SHA256',hashlib.sha256(zip_path.read_bytes()).hexdigest())
out=Path('/workspace/output/co2-video');out.mkdir(parents=True,exist_ok=True)
for name in ['co2-video-stage01-review.zip','co2-video-stage01-sample.mp4','co2-video-narration-draft.mp3']:shutil.copy2(dest/name,out/name)
