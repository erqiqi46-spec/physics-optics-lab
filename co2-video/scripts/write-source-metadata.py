from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];m=json.loads((R/'raw/capture-manifest.json').read_text());qa=json.loads((R/'reports/raw-complete-qa.json').read_text());checks={c['id']:c for c in qa['clips']}
for c in m['clips']:
 p=R/'raw'/c['id'];d={**c,'sourceSha256':m['sha256'],'sourceFile':'source/co2-lab-v3.html','frameFiles':'%05d.jpg' if c['frames']>1 else 'still.png','nativeFrameRate':c['fps'],'durationSeconds':c.get('duration',0),'verification':checks[c['id']],'acquisition':m['acquisition'],'phenomenonScope':c['label'],'note':'Source app model time is not a real reaction-rate measurement; stills are not continuous motion.'};(p/'metadata.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
print('SOURCE_METADATA_READY',len(m['clips']))
