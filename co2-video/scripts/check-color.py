from pathlib import Path
import subprocess,json
import numpy as np
R=Path(__file__).resolve().parents[1];rows=[]
# Compare full-resolution RGB pixels; avoid adding a second colorspace-changing scale operation.
for f in [500,1765,3242]:
 ims=[]
 for name in ['co2_video_preview_render.mp4','co2_video_preview.mp4']:
  raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(f/30),'-i',str(R/'output'/name),'-frames:v','1','-pix_fmt','rgb24','-f','rawvideo','-']);ims.append(np.frombuffer(raw,dtype='uint8').astype(float))
 d=float(np.abs(ims[0]-ims[1]).mean());assert d<4,(f,d);rows.append({'frame':f,'meanAbsoluteRgbDifference':d})
(R/'reports/color-conversion-review.json').write_text(json.dumps({'passed':True,'method':'Full-resolution RGB appearance comparison of3 actual preview frames before/after range/matrix normalization; not colorimetric display calibration','samples':rows,'threshold':4},indent=2));print('COLOR_CONVERSION_PASS',rows)
