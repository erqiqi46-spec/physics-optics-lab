from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];q=json.loads((R/'reports/film-final-validation.json').read_text());v=json.loads((R/'reports/final-visual-review.json').read_text());a=json.loads((R/'reports/co2_science_video_1080x1920-loudness.json').read_text());p=json.loads((R/'reports/preview-review.json').read_text());assert q['passed'] and v['passed'] and p['passed'] and float(a['input_tp'])<=-1
(R/'reports/video_quality_report.md').write_text(f'''# 最终视频质量报告

成片：output/co2_science_video_1080x1920.mp4。时长{q['durationSeconds']}秒，{q['width']}×{q['height']}，30fps，H.264/AAC，有限范围BT709/yuv420p，{q['frames']}帧。

## 自动检查

- 全部帧解码成功；全帧黑帧检测无异常。
- 对全部帧检查固定页脚，以及每章稳定后的标题、知识卡区域；未检出整页位移、卡片缺失或源画面空白。早期仅检测页脚的不足已记录并扩展检查，失败版不交付。
- 字幕{q['subtitleChunks']}段，时间无重叠、无越界，最长28字符，最短约0.88秒。中文字体随工程本地提供。
- “注意看”提示前完成聚焦，气泡/浑浊开始在提示之后；气密性前后状态也在提示之后切换。
- 四音轨均为48kHz双声道、长度一致、非空且未出现PCM削波。最终AAC测得综合响度{a['input_i']} LUFS，真峰值{a['input_tp']} dBTP，低于−1 dBTP。
- 预览与最终采用同一时间轴；最终Hash见film-final-validation.json。

## 画面审核

制作端实际查看12个章节及气泡、石灰水、验满的前中后关键帧，并检查高清分屏、公式、结构示意和字幕安全范围。素材原始4:3显示保持比例；双栏对照是裁切，不是拉伸；火焰、瓶口与漏斗可见。重点画面及索引在frames/final与frames/key-events。

镜头为原生开场推镜、器材特写、轻微数字推近与讲解停顿。长时间关键帧均有标识；不是全过程一镜到底。原生反应素材20fps，编码30fps含重复帧，未伪造更高原生帧率。

科学六项可见性见science_review.md，全部有画面证据与说明，但尚未做第三方教师签审和真实班级学习效果验证。声音依据合成词边界、音轨结构和响度检测审核；没有独立真人全片听审，不冒充此项已验证。

## 局限

v3仍是程序化3D教学模型，原生装药/木条等有离散状态；大量讲解使用有标识的关键帧观察。画质、动作细节与实际实验存在差距，不宣称最终电影级美术验收通过。见known-limitations.md。
''')
(R/'reports/stage01-result.json').write_text(json.dumps({'currentStatus':'FINAL_VIDEO_COMPLETE','sourceComplete':True,'stage02Locked':True,'previewPassed':True,'finalPassed':True,'finalFrames':q['frames'],'finalSeconds':q['durationSeconds'],'historicalFailureReports':'history-stage01/'},indent=2))
with(R/'reports/batch-status.md').open('a')as f:f.write('\n最终关闭：Batch06混音和Batch07高清成片完成；自动技术检查、扩展全帧画面检测及制作端关键画面复核通过。报告包含未验证的真人听审、教师签审与课堂效果，不将其标记为通过。\n')
print('FINAL_REPORTS_READY')
