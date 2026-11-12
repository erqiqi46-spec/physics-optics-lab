# v3 现象增强与画面优化检查（2026-11-12）

## 自动化结果

- 化学与流程单元测试43/43通过：计量、液封、漏气、气体分布、木条位置、检验/验满、预装七步流程、八类错误对照等。v3将石灰水关键观察暂停点移至更明显的浑浊阶段，相关流程断言通过。见evidence/unit-results-v3.txt。
- TypeScript与生产构建通过。见evidence/build-results-v3.txt。离线单文件仍有JS包较大的构建提示。
- 最终打包HTML在流畅档完成一次端到端脚本，覆盖七步场景热点点击、八类错误示范、同一时刻瓶内/瓶口对比、规范对照、原进度保留、盖口、记录保存、CSV下载、刷新后记录恢复、原理与Escape关闭、390px无横向溢出及触屏仿真tap。外部HTTP(S)请求0、JavaScript运行错误0。见evidence/panorama-check-v3.json。
- v3高清材质初轮亦通过相同端到端脚本，见evidence/panorama-check-v3-hd-initial.json；随后进行了闲置木条不点火、玻璃不投不透明实影及画质切换的优化。最终高清图像与画质切换检查由scripts/check-visual-quality.mjs单独执行，结果见evidence/visual-quality-check-v3.json。

这些是脚本中的多项断言，不冒称多条独立浏览器测试。环境为Linux Chromium 158软件渲染，不代表实体Windows触屏、低配学校电脑或Safari均已验收。

## 变化与科学边界

1. 反应与通气气泡更醒目；暂停模型时间时保留气泡观察帧，不再直接隐藏。
2. 三维石灰水从透明逐渐呈白色浑浊，沉淀颗粒与液面随当前模型变化；生成物为碳酸钙，不把CO₂本身画成有色气体。
3. 木条测试显示更明显的橙黄色火焰，熄灭后火焰消失、保留炭化端部；未进行木条测试时不在台面预先点火。
4. 同步观察窗对比“澄清参照/当前液体”和“燃烧参照/当前木条”。该窗明确标注局部示意，不声称为实物摄像机或测量仪器。
5. 本地生成环境反射，调整玻璃与金属、台面、阴影及特写，修正软管折返。高清与流畅切换只改渲染，不改反应或气体计算。

气泡尺寸和数量、沉淀颗粒、火焰大小与浑浊对比为教学放大；不预测真实速率、粒径、温度或浓度。三维器材依然是程序化临时资产，不宣称已达到最终电影级美术品质。

## 截图与复现

v3截图包含石灰水变化、特写、错误示范、完成实验、窄屏，以及最终高清准备状态/燃烧/熄灭对比。已目视检查石灰水全景和特写，白色浑浊与澄清参照可辨认；已检查最终高清燃烧与熄灭近景，火焰与木条端部取景完整。

```sh
npm run test:chemistry
npm run build:chemistry
npx playwright install chromium
node chemistry/scripts/check-panorama.mjs v3
node chemistry/scripts/check-visual-quality.mjs
python3 chemistry/scripts/package.py
```
