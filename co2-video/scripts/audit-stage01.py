from pathlib import Path
import csv,json,hashlib,subprocess,datetime,shutil
R=Path(__file__).resolve().parents[1];report=R/'reports';report.mkdir(exist_ok=True)
source=R/'source/co2-lab-v3.html';sha=hashlib.sha256(source.read_bytes()).hexdigest();manifest=json.loads((R/'raw/capture-manifest.json').read_text());completed={c['id']:c for c in manifest['clips']};rows=[]
for folder in sorted((R/'raw').iterdir()):
 if not folder.is_dir():continue
 jpgs=list(folder.glob('*.jpg'));pngs=list(folder.glob('*.png'));videos=list(folder.glob('*.webm'))+list(folder.glob('*.mp4'))
 if jpgs or pngs:
  c=completed.get(folder.name);is_clock=folder.name=='clock-probe';complete=bool(c) or is_clock and len(jpgs)==40
  fps=c.get('fps') if c else 20 if is_clock else None
  status=('complete_technical_probe_only' if is_clock else 'captured_complete_edit_review_pending') if complete else 'incomplete_do_not_use'
  meta={'path':str(folder.relative_to(R)),'kind':'original_app_frame_sequence' if jpgs else 'original_app_still','frames':len(jpgs) or len(pngs),'fps':fps,'duration':len(jpgs)/fps if fps and jpgs else None,'width':1080,'height':810,'status':status,'sourceSha256':sha,'presentationOnlyCss':True,'physicalModelModified':False,'actualObservedPhenomenon':c['label'] if c else '2s clock-stepped bubble motion probe' if is_clock else 'partial limewater capture; full transition not verified','needsReview':not complete}
  (folder/'metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2));rows.append(meta)
 for f in videos:
  p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_name,width,height,r_frame_rate,avg_frame_rate','-of','json',str(f)],capture_output=True,text=True);data=json.loads(p.stdout or '{}');duration=data.get('format',{}).get('duration');stream=next((s for s in data.get('streams',[]) if s.get('width')),{});meta={'path':str(f.relative_to(R)),'kind':'realtime_browser_recording','frames':None,'fps':stream.get('r_frame_rate'),'duration':float(duration) if duration else None,'width':stream.get('width'),'height':stream.get('height'),'status':'probe_only_not_edit_approved' if duration else 'invalid_incomplete_container','actualObservedPhenomenon':'browser recording technical probe; timings and cadence not edit-approved','ffprobe':data};f.with_suffix('.metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2));rows.append(meta)
with (report/'material_inventory.csv').open('w',newline='',encoding='utf-8-sig') as f:
 fields=['path','kind','frames','fps','duration','width','height','status','actualObservedPhenomenon'];w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
(report/'material_inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
audit={'sourceSha256':sha,'sourceCommit':'50ca134','sourceBytes':source.stat().st_size,'captureComplete':manifest['complete'],'normalCompletedIds':list(completed),'partialLimeFrames':len(list((R/'raw/09-lime-transition').glob('*.jpg'))),'expectedLimeFrames':90,'rawCapturingFailure':'exec-server transport disconnected; failed to resume exec-server session: recovery timed out after 45s','cause':'not established; do not claim an OOM, network or app-model diagnosis without further evidence','stage02Locked':True,'missingKeyPhenomena':['complete limewater transition','continuous before/after mouth retest footage','inside/mouth and funnel error shots','records and ending shots']}
(report/'stage01-result.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))

for src,dst in [('unit-results-v3.txt','reference-v3-unit-tests.txt'),('panorama-check-v3.json','reference-v3-browser-check.json'),('visual-quality-check-v3.json','reference-v3-hd-check.json')]:
 f=R.parent/'chemistry/evidence'/src
 if f.exists():shutil.copy2(f,report/dst)
print(json.dumps(audit,ensure_ascii=False));print('INVENTORY',len(rows))
