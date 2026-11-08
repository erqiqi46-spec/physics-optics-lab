# Stage 01 自动化验收报告

执行日期：2026-11-08。环境：Linux、Node.js、Vite、Vitest、Playwright Chromium。浏览器使用 SwiftShader 软件 WebGL 渲染。

## 结果

- TypeScript 检查与 Vite 生产构建：通过。
- Vitest：11 / 11 通过；0 失败。
- Playwright：4 / 4 通过；0 失败，0 跳过。
- 桌面端流程中捕获的页面运行异常：0。

## 科学单元测试

五组 u<f、u=f、f<u<2f、u=2f、u>2f；有限像薄透镜等式与放大率；焦点两侧符号与无穷趋势；光屏离焦增加；虚像及焦点对多个屏位均不能承接；三器材轨道间隔与边界；焦距限制；五类教学预设。

## 浏览器端到端验收

1. 1440×1080：初始清晰实像 → 离焦模糊 → 自动对焦；遍历全部五类情境；虚像及焦点状态不能自动对焦；记录五组数据；数据表、CSV 下载；刷新恢复；器材重置；课堂自测；自主模式切换。
2. 390×844：触控模拟上下文，键盘方向键调整焦距，触摸重置与记录；断言页面无横向溢出。
3. 真实鼠标事件拖动三维凸透镜底座，验证位置改变、器材间距满足约束，并检查固定光屏的屏幕位置不变，确认镜头未随拖拽旋转。
4. Chromium CDP touchStart / touchMove / touchEnd 直接拖动三维凸透镜底座，验证数值同步变化。

## 验收过程中的修正

- 首轮软件渲染测试超时：将 3D 场景改为按需渲染，并为接触阴影限制采样帧；最终重新运行通过。
- 初轮触控窄屏发现标签可能产生横向溢出：增加视口裁切。
- 截图人工复核发现窄屏镜头裁掉发光物体：加入画布比例自适应初始镜头，并移除手机侧边栏以增加操作面积，重新测试。
- 初轮拖拽脚本使用文字标签推算点击点而未命中底座：改为由底座空间锚点投影定位，使用真实鼠标/触摸事件复验；没有通过直接调用状态函数绕过三维交互。

## 证据

- `evidence/unit-results.json`：Vitest 机器可读结果。
- `evidence/browser-results.json`：Playwright 机器可读结果及耗时。
- `evidence/build.log`：最终构建日志。生产 JS 约 1.3 MB、gzip 约 376 KB；Vite 有分包尺寸提示，非构建失败。
- `evidence/01-focused-desktop.png`：倒立等大实像与实验控制面板。
- `evidence/02-defocused.png`：同一物体在离焦光屏上的模糊像。
- `evidence/03-virtual-image.png`：正立放大虚像与空白光屏。
- `evidence/04-data-table.png`：五组实验记录。
- `evidence/05-mobile-touch.png`：窄屏触摸界面。
- `evidence/sample-records.csv`：浏览器实际导出的五组记录。

未验证：真实硬件触摸、多点缩放、Safari/Firefox、GPU 性能、全站辅助技术兼容性。截图和程序化资产的完成度不等于最终美术验收通过，具体见 `LIMITATIONS.md`。
