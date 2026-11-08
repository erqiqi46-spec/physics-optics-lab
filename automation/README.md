# 教学自动化与 MP4 录制

脚本使用现有 v1.2 独立 HTML，顺序执行真实页面操作，叠加随章节切换的口播字幕、鼠标指示和控件高亮。字幕按录屏可见标记对齐，不把预计延时当作实际录制时间。

## 复现

先按项目 README 安装 Node.js 依赖并执行 `npm run build:standalone`，然后：

```bash
npx playwright install chromium
node automation/record-demo.mjs
python automation/render-demo.py recordings
```

导出需要 PATH 中有 FFmpeg/FFprobe，Python 安装 Pillow。视频输出为 H.264、1920×1080、25 fps、yuv420p、MP4 faststart，默认仅字幕不含合成配音。另输出完整口播稿、SRT、实际步骤时间轴、操作流程与校验报告。

可选环境变量：`RECORD_OUT` 指定输出文件夹；`DEMO_URL` 指定待演示的同版本页面；`DEMO_HEADLESS=0` 可显示浏览器。未指定 URL 时直接使用本机 `docs/index.html`，会阻止外部 HTTP(S) 请求。

录制以 24 个讲解章节组织，覆盖预测、观察、揭示、离焦、五类成像、实验记录和易错题。`cues.json` 可修改讲解文字与最短停留时间，实际时长会给真实操作留出余量。

输出 MP4 已烧录字幕；SRT 用于后期剪辑，播放原 MP4 时不要再叠加重复字幕。口播稿可直接用于教师配音。该脚本会在新建浏览器上下文生成演示记录，不修改用户的现有记录。

## 尾段恢复

本次成片的最后四段使用补录：首轮录屏在软件渲染环境下未完整写入尾帧，因此保留前 20 段，再补录自测与总结。源影片均为实际页面操作，转码器从可见步号恢复真实边界后剪接。

同样问题可用以下方式恢复（仅适用于本脚本的默认 24 段流程）：

```bash
DEMO_START=20 RECORD_OUT=recordings/tail node automation/record-demo.mjs
python automation/render-demo.py recordings --tail-dir recordings/tail
```

补录会恢复前段已经展示的五组记录，供画面连续性使用，再通过实际界面切换到虚像情形。它不修改物理模型或伪造成像结果。正常完整录制会额外等待尾帧写入，转码时自动去掉多余停留。
