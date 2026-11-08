"""Generate generic Mandarin speech for the recorded teaching narration."""
import argparse,asyncio,json,os,subprocess
from pathlib import Path
import edge_tts
from edge_tts import communicate
if Path('/etc/ssl/certs/ca-certificates.crt').exists():communicate._SSL_CTX.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
async def main():
 p=argparse.ArgumentParser();p.add_argument('--timeline',required=True);p.add_argument('--out',required=True);a=p.parse_args();root=Path(a.out);root.mkdir(parents=True,exist_ok=True);cues=json.loads(Path(a.timeline).read_text());sem=asyncio.Semaphore(3)
 async def generate(i,c):
  async with sem:
   audio=root/f'{i:02d}-{c["id"]}.mp3';meta=audio.with_suffix('.jsonl')
   if not audio.exists() or audio.stat().st_size<1000:
    for attempt in range(3):
     try:await edge_tts.Communicate(c['narration'],'zh-CN-XiaoxiaoNeural',rate='-3%',proxy=os.environ.get('HTTPS_PROXY'),connect_timeout=20,receive_timeout=60).save(str(audio),str(meta));break
     except Exception:
      if attempt==2:raise
      await asyncio.sleep(2)
   duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(audio)],text=True));c['audioFile']=str(audio.resolve());c['audioSeconds']=duration;print(f'Voice {i+1:02d}/{len(cues)}: {duration:.2f}s',flush=True)
 await asyncio.gather(*(generate(i,c) for i,c in enumerate(cues)));(root.parent/'voice-timeline.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2));print('VOICE READY',sum(c['audioSeconds'] for c in cues),flush=True)
asyncio.run(main())
