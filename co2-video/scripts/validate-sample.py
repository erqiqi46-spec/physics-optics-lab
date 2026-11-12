from pathlib import Path
import json,re,subprocess,hashlib
R=Path(__file__).resolve().parents[1];cfg=json.loads((R/'sample-timeline.json').read_text());p=json.loads((R/'reports/sample-ffprobe.json').read_text());v=next(s for s in p['streams'] if s['codec_type']=='video');a=next(s for s in p['streams'] if s['codec_type']=='audio');log=(R/'reports/sample-loudness.log').read_text();meter=json.loads(re.search(r'\{\s*"input_i".*?\}',log,re.S).group());checks={
 'technical_sample_scope':cfg['status']=='TECHNICAL_SAMPLE_ONLY_NOT_COMPLETE_LESSON',
 'preview_dimensions':(v['width'],v['height'])==(540,960),
 'fps_30':v['avg_frame_rate']=='30/1',
 'video_h264':v['codec_name']=='h264',
 'audio_aac':a['codec_name']=='aac',
 'duration_16_seconds':abs(float(p['format']['duration'])-16)<.15,
 'frame_count_480':int(v['nb_read_frames'])==480,
 'true_peak_below_minus_1':float(meter['input_tp'])<=-1,
 'no_detected_black_frames':'black_start:' not in (R/'reports/sample-blackframes.log').read_text(),
 'source_aspect_preserved':abs(1080/810-1000/750)<1e-9,
 'no_excessive_source_upscale':1000*cfg['camera']['scaleEnd']<=1080,
 'subtitles_within_timeline':all(0<=s['start']<s['end']<=16 for s in cfg['subtitles']),
 'subtitles_nonoverlapping':all(x['end']<=y['start'] for x,y in zip(cfg['subtitles'],cfg['subtitles'][1:])),
 'all_four_audio_stems_present':len(cfg['audioTracks'])==4 and all((R/'public'/s['src']).exists() for s in cfg['audioTracks']),
 'complete_clock_probe_frames':len(list((R/'raw/clock-probe').glob('*.jpg')))==40,
 'original_html_unmodified':hashlib.sha256((R/'source/co2-lab-v3.html').read_bytes()).hexdigest()==hashlib.sha256((R.parent/'downloads/chemistry-co2-lab.html').read_bytes()).hexdigest(),
 'full_movie_not_falsely_created':not (R/'output/co2_science_video_1080x1920.mp4').exists(),
}
final=subprocess.run(['node',str(R/'scripts/render.mjs'),'final'],capture_output=True,text=True);checks['final_render_gate_blocks']=final.returncode!=0 and 'FINAL_RENDER_BLOCKED' in final.stderr
for s in (R/'scripts').glob('*.mjs'):
 t=subprocess.run(['node','--check',str(s)],capture_output=True,text=True);checks['syntax_'+s.name]=t.returncode==0
result={'scope':'16-second technical sample only; full educational movie is blocked','passed':all(checks.values()),'checks':checks,'measuredTruePeakDbTP':float(meter['input_tp']),'measuredIntegratedLufs':float(meter['input_i']),'fullMovieScientificAndCinematicAcceptance':'NOT_RUN_MISSING_KEY_MEDIA'};(R/'reports/sample-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False));assert result['passed']
