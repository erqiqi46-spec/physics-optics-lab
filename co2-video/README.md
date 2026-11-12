# 智用实验室 · CO₂视频制作工程 / 第1批审核交付

**不是完整成片。** 本包包含v3来源审核、原生采集证据、补录清单、Remotion技术样板、四条样板音轨、口播草稿和16秒技术样片。关键录制素材不完整，因此遵照任务停机规则，没有制作或宣称通过150秒影片。

先看：

- `output/co2_capture_technical_sample.mp4`：540×960、30fps、H.264/AAC，16秒。仅2秒为实际运动采集，其余是明确标注的关键帧讲解。不是整套实验演示。
- `reports/stage01_audit.md`：源码、运行证据、未实现项、采集问题与停机结论。
- `reports/material_inventory.csv`：素材清单。capture完整与电影素材验收是两个概念。
- `reports/missing_shots.md`：必须补齐的镜头。
- `reports/science_review.md`：科学表述边界。
- `reports/sample-validation.json`：只针对16秒技术样片的自动验证。
- `output/narration-draft.md/mp3`：约146秒中文口播草稿，尚未锁定镜头和音画时序。
- `output/timeline-draft.json`：正式影片草稿，缺失sourceFile/sourceIn/sourceOut故意留null，不可直接渲染。
- `sample-timeline.json`、`output/timeline.json`：技术样片配置，非完整影片时间轴。

## 素材真实性

`source/co2-lab-v3.html`是原v3的不可变副本，SHA256见审核结果。采集仅通过原按钮和仿真时钟推进；外观CSS用于隐藏外围UI并调整取景尺寸，没有另写气泡、浑浊或火焰物理。`raw/`保留实际帧和探测视频，每个目录附metadata；中断文件与半段素材已标明不可用。采集失败的底层原因尚未确定，不将它归咎于某个未经证实的模型或设备问题。

脚本已修补时钟超时与错误示范无正常计时面板的读取保护；**修补后的全流程采集尚未重新验收**。不要把脚本存在当作完整采集已通过。

## 复现技术样片

需要Node.js 20+、FFmpeg；从本目录执行：

```sh
npm ci
npx playwright install chromium
npm run render:preview
```

这会渲染`output/co2_capture_technical_preview.mp4`。审核交付的`co2_capture_technical_sample.mp4`另外经过FFmpeg响度处理。`npm run render:final`会明确拒绝，因为关键素材未齐，工程当前只有技术样片Composition。

`src/components.tsx`提供CameraZoom、CameraPan、FocusHighlight、ScienceCallout、BeforeAfter、ErrorCompare、KnowledgeCaption、EquationReveal等基础模板；配置从JSON读取。样片实际运行了运镜、高亮、知识卡、公式、字幕、品牌和四音轨，未使用的对比组件不声称已完成视频验收。

## 补录和资产处理

采集脚本当前按含`co2-video`目录的父目录运行。Python可使用独立虚拟环境，依赖见requirements.txt。素材中途失败应保留证据并停止后续，不得补造完整实验。

```sh
node co2-video/scripts/capture-source.mjs
python co2-video/scripts/audit-stage01.py
```

录到全部关键素材后，先逐帧审核前/中/后与清晰度，再根据真实sourceIn/sourceOut和合成旁白句边界锁定正式timeline，之后按制作任务逐批验收。

## 音轨和授权来源

四条独立WAV在`public/audio/sample-narration.wav`、`sample-music.wav`、`sample-experiment.wav`、`sample-ui.wav`；JSON支持音量、淡入淡出、静音与旁白区间压低音乐。样板配乐和拟音为本项目程序生成，无第三方音乐或采样，生成脚本一并提供。标准中文合成声线非真人模仿。CJK子集字体附许可证。音效为后期拟音，不是实验现场声音。

## 后续批次状态

第1批：审核报告完成，原始电影素材门槛未通过。第2批正式时间轴：未锁定。第3–4批：仅通用代码与技术样板，非正式镜头验收。第5–7批：完整粗剪、精剪、最终1080×1920成片与教学六问验收均未完成。
