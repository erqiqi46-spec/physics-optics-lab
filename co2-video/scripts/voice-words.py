import asyncio,json,os,subprocess
from pathlib import Path
import edge_tts
from edge_tts import communicate
communicate._SSL_CTX.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
ROOT=Path(__file__).resolve().parents[1]
async def main():
 cues=json.loads((ROOT/'narration-draft.json').read_text());out=ROOT/'public/audio/voice-words';out.mkdir(parents=True,exist_ok=True);sem=asyncio.Semaphore(2)
 async def one(c):
  async with sem:
   a=out/(c['id']+'.mp3');m=out/(c['id']+'.jsonl')
   if not a.exists() or a.stat().st_size<1000:
    for i in range(3):
     try:
      await edge_tts.Communicate(c['narration'],'zh-CN-YunxiNeural',rate='+4%',boundary='WordBoundary',proxy=os.environ.get('HTTPS_PROXY'),connect_timeout=20,receive_timeout=60).save(str(a),str(m));break
     except Exception:
      if i==2:raise
      await asyncio.sleep(2)
   c['audioSeconds']=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(a)],text=True));c['audioFile']='audio/voice-words/'+a.name;print('VOICE',c['id'],c['audioSeconds'],flush=True)
 await asyncio.gather(*(one(c) for c in cues));(ROOT/'voice-cues-words.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2));print('TOTAL_VOICE_SECONDS',sum(c['audioSeconds'] for c in cues),flush=True)
asyncio.run(main())
