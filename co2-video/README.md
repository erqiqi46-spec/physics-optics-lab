# 智用实验室 · 二氧化碳3D全景实验教学视频

本工程从未改动的v3 HTML自动操作并采集原生画面，剪辑为约159秒的9:16中文配音视频。最终文件和验收结果见 `output/`、`reports/film-final-validation.json` 和 `reports/video_quality_report.md`。历史16秒技术样片仅保留为早期记录。

## 成片与附件

- `output/co2_science_video_1080x1920.mp4`：1080×1920、30fps、H.264/AAC，包含同步字幕。
- `output/co2_video_preview.mp4`：手机预览版。
- `output/co2_science_subtitles.srt`、`output/narration-final.md`：可修改的字幕、分镜与口播。
- `public/audio/film/`：旁白、原创背景音乐、实验拟音、界面音效四条独立WAV。
- `timeline.json`：全部镜头的素材、时序、取景、配音、知识点配置。
- `source/co2-lab-v3.html`：可离线双击打开的原课件副本；影片没有更改其反应模型。
- `raw/capture-manifest.json`：原生素材来源、时间与采集记录。

## 重新渲染

渲染脚本对完整Chromium显式指定 `chromeMode: chrome-for-testing`，并使用单工作器，避免旧headless模式下的合成缺失。完整素材包含在交付压缩包内。仅克隆Git仓库时，应先下载完整工程包并恢复 `public/media`、`public/audio`。需要Node.js20+、FFmpeg，Python工具另需numpy、Pillow、fontTools。

```sh
cd co2-video
npm ci
npx playwright install chromium
npm run render:preview
# 检查预览并在 reports/preview-review.json 记录真实审核结果后：
npm run render:final
python3 scripts/master-film.py
python3 scripts/validate-film.py final
```

配音已经包含在工程中；重新生成合成配音才需要联网。素材与字体均为本地文件，渲染本身不依赖CDN。完整工程无需安装依赖即可观看已有MP4；交互课件是另外的HTML文件，MP4本身不具备点击操作功能。

## 采集与可复用模板

从仓库父目录依次执行 `node co2-video/scripts/capture-takes.mjs lime`（以及 collection、splint、errors、intro、outro），只使用原网页控件与离线时钟推进。早期素材的发生器、加酸部分已随包提供。`audit-complete.py`检测原生帧尺寸与空白。`prepare-film.mjs`生成素材代理、字幕和时间轴；`prepare-film-audio.py`生成四条混音前音轨。

`src/Film.tsx`使用JSON驱动的运镜、聚焦框、原图前后对照、错误对照、公式、结构图、品牌与字幕。通用组件在 `src/components.tsx`。素材画面按4:3保留比例，双栏对照进行裁切而不拉伸。

## 真实性与限制

- 原生素材1080×810，离线逐帧20fps，成片30fps通过重复帧编码；不宣称原生实时30fps。
- 装药、液柱建立和木条测试在原模型中是状态切换；影片明确标记分段与讲解停顿，未伪造连续倾倒或燃烧物理。
- CO₂无色。气体粒子、泄漏路径与后加结构图均为教学辅助，非真实颜色、浓度或流场测量。
- 影片不是全过程一镜到底：包含真实操作所得的关键画面、动态现象、独立错误快照和讲解停顿。
- 3D器材沿用v3程序化模型；画质受原资产限制，不宣称达到最终电影级品质。
- 旁白为标准中文合成声线；音乐与拟音由本项目生成，非实录声音。字体许可证见public/fonts。
- 自动测试和本次画面审核不能替代教师实课试用、学习效果研究及多设备音响试听。
