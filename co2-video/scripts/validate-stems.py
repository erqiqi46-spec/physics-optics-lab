from pathlib import Path
import wave,json
import numpy as np
R=Path(__file__).resolve().parents[1];T=json.loads((R/'timeline.json').read_text());total=None;rows=[]
for p in sorted((R/'output/audio_stems').glob('*.wav')):
 with wave.open(str(p)) as w:
  assert w.getframerate()==48000 and w.getnchannels()==2 and w.getsampwidth()==2
  a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2).astype(np.float32)/32768;assert abs(len(a)/48000-T['durationSeconds'])<.001
 peak=float(np.abs(a).max());assert 0<peak<1;rows.append({'file':p.name,'duration':len(a)/48000,'samplePeak':peak});total=a if total is None else total+a
assert len(rows)==4
peak=float(np.abs(total).max());assert peak<1
(R/'reports/stems-validation.json').write_text(json.dumps({'passed':True,'stems':rows,'preMasterSumPeak':peak,'stereo':True,'sampleRate':48000,'scope':'PCM structure, duration, nonzero and no sample clipping; final AAC true peak checked separately'},indent=2));print('STEMS_QA_PASS',peak)
