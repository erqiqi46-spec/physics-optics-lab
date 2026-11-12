# 渲染与处理说明

原课件1080×810逐帧采集，20fps模型画面；Remotion将原生素材、取景、高亮、字幕、知识卡、公式与结构示意合成到9:16版式，输出30fps。重复帧不作伪运动插帧。静态讲解明确标记，动态前中后保留。

原始HTML SHA256、各段来源见raw-complete-qa.json及capture-manifest.json；影片配置timeline.json共12镜头/4772帧，源In/Out均有值，静态图Out为0。

早期旧headless截图流水线出现整页拼接及局部图层缺失；只检测页脚的检查曾漏报，扩展区域检查检出821个疑似异常帧，因此旧预览作废。尝试PNG和局部修补未解决整段批量捕获问题。正式脚本已显式使用chrome-for-testing新headless模式、单工作器；256帧石灰水测试的标题、知识卡与页脚差异检测无异常。随后完整重渲染，不使用旧异常预览拼凑成片。全片需通过扩展区域检查。

预览审核见preview-review.json，最终渲染尺寸、帧数、耗时见render-final.json。FFmpeg将JPEG捕获的全范围BT601规范转换为有限范围BT709/yuv420p并做混音响度处理，AAC真峰值以co2_science_video_1080x1920-loudness.json为准。

依赖与脚本随工程提供；运行配置不是性能承诺，软件浏览器和无GPU环境的全长渲染可能较慢。历史样片的验证仅证明当时16秒技术样片，不能替代本次film-final-validation.json。
