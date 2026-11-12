import asyncio,os
from pathlib import Path
import edge_tts
from edge_tts import communicate
communicate._SSL_CTX.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
root=Path(__file__).resolve().parents[1]
text='这是从原始三维课件逐帧采集的气泡观察片段。气泡说明有气体产生，但不能单独确定气体身份。这是采集技术样片，还不是完整实验视频。'
asyncio.run(edge_tts.Communicate(text,'zh-CN-YunxiNeural',rate='+4%',proxy=os.environ.get('HTTPS_PROXY')).save(str(root/'public/audio/sample-voice.mp3'),str(root/'public/audio/sample-voice.jsonl')))
