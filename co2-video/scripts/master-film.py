from pathlib import Path
import subprocess,json,sys
R=Path(__file__).resolve().parents[1];mode=sys.argv[1] if len(sys.argv)>1 else 'all'
for stem in (['co2_video_preview'] if mode=='preview' else ['co2_science_video_1080x1920'] if mode=='final' else ['co2_video_preview','co2_science_video_1080x1920']):
 inp=R/'output'/(stem+'_render.mp4');out=R/'output'/(stem+'.mp4')
 # Convert full-range JPEG capture to limited-range BT709/yuv420p for broad player compatibility; normalize audio.
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(inp)]))['streams'][0]
 videoArgs=['-c:v','copy'] if info.get('color_range')=='tv' and info.get('color_space')=='bt709' and info.get('pix_fmt')=='yuv420p' else ['-vf','scale=in_range=pc:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','fast','-crf','18','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709']
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(inp),*videoArgs,'-af','loudnorm=I=-16:TP=-1.7:LRA=8','-ar','48000','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True)
 log=subprocess.run(['ffmpeg','-hide_banner','-i',str(out),'-af','loudnorm=I=-16:TP=-1:LRA=8:print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
 j=json.loads(log[log.rfind('{'):log.rfind('}')+1]);assert float(j['input_tp'])<=-1,j
 (R/'reports'/(stem+'-loudness.json')).write_text(json.dumps(j,indent=2));print('MASTERED',out.name,j['input_i'],j['input_tp'])
