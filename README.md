# 初中物理 3D 互动实验室 · Stage 01

- 在线发布：源码已准备在 `docs/`；仓库所有者需在 Settings → Pages 选择 Deploy from a branch、main、/docs 后保存。GitHub 当前授权不允许自动开启 Pages。启用后以设置页返回的实际网址为准。
- 推荐离线下载：https://raw.githubusercontent.com/erqiqi46-spec/physics-optics-lab/main/downloads/optics-lab-offline-v1.1.zip（解压后双击 HTML）
- 离线单文件：https://raw.githubusercontent.com/erqiqi46-spec/physics-optics-lab/main/downloads/optics-lab.html
- Windows 一键离线包：https://raw.githubusercontent.com/erqiqi46-spec/physics-optics-lab/main/downloads/optics-lab-windows-x64.zip

启用 Pages 后在线版可直接在浏览器使用；离线 HTML 下载后双击打开，无需安装或联网。

在线演示需由仓库所有者启用 GitHub Pages；`docs/index.html` 为无外部网络请求的独立单文件版本，可下载后用浏览器打开。

使用 `npm run build:standalone` 重新生成 `docs/index.html`。Windows 一键运行包与独立 HTML 见仓库 downloads 目录。

首个实验：探究凸透镜成像的规律。Three.js + React Three Fiber + React + TypeScript + Vite。

## 本地运行

需要 Node.js 22.12+（或 20.19+）。解压源码包后进入项目目录：

```bash
npm ci
npm run dev
```

浏览器打开终端打印的地址（默认 http://localhost:5173）。生产构建：`npm run build`；预览构建：`npx vite preview --host 0.0.0.0`。需要支持 WebGL2 的浏览器。

## 使用方法

1. 拖动空白处旋转、滚轮或双指缩放；点击仪器选中并拖动底座、支架或本体，沿轨道移动。
2. 右侧三个位置滑块或数值输入提供精确控制；u = 透镜位置 − 物体位置；d = 光屏位置 − 透镜位置。
3. 调节焦距；观察加粗主光线、传播方向箭头、可切换的光束，以及同步侧视图、理论像距、成像性质和实际光屏。光屏与理论像点不重合时会离焦。
4. “光屏移至理想像点”仅在实像且像点位于轨道内时启用。无法接收实像的情形不会在光屏贴出清晰像。
5. 教师引导可切换五种物距情境；自主实验保持器材自由调整。虚像用透明正立 F 与虚线反向延长线表示，是教学辅助，非真实悬浮物体。
6. 记录数据、展开数据表、导出 UTF-8 CSV；记录保存于当前浏览器 localStorage，重置器材保留记录，另有“清空记录”。
7. 总结面板包含五类规律与 15 道易错自测题、答案解析、错题复习及进度统计。滑块支持方向键，所有按钮与数值输入支持键盘 Tab 操作。

## 自动化验证

```bash
npm test
npx playwright install chromium
npm run dev
# 在另一个终端运行：
npx playwright test
```

Playwright 默认使用已经启动的 5173 端口服务器；配置了无头 Chromium 的 SwiftShader 选项，便于无 GPU 的 Linux 环境。测试结果 JSON 与过程截图输出至 `evidence/`。测试脚本会在隔离的浏览器上下文生成记录并导出样例 CSV。v1.1 新增的光路与题库测试验证实时几何变化和全部 15 道题目。

## 文件结构

- `src/physics.ts`：纯数值计算、符号约定、约束；无 DOM / Three.js 依赖。
- `src/teaching.ts`：教学案例、预设配置。
- `src/rays.ts`：同物点近轴光束、屏面截光、视野裁切的纯数学函数。
- `src/RayDiagram.tsx`：与三维共用光路计算的侧视图。
- `src/questions.ts` / `src/SummaryModal.tsx`：15 道易错题与课堂反馈。
- `src/Scene.tsx`：程序化 3D 器材、材质、拖拽、光线和屏面纹理。
- `src/main.tsx`：数值控制、教学模式、记录、CSV、课堂自测。
- `src/physics.test.ts`：11 项科学与约束测试。
- `src/rays.test.ts`：12 项光束与几何裁切测试。
- `tests/lab.spec.ts`：4 组基础浏览器端到端测试。
- `tests/learning.spec.ts`：2 组实时光路与 15 道题库回归测试。
- `SCIENCE-REPORT.md`：科学检查与成像近似说明。
- `LIMITATIONS.md`：资产性质、已知局限及后续改进。
- `TEST-REPORT.md`：最终执行结果和验收范围。

## 交付范围

这是 Stage 01 可交互核心版本：程序化器材为明确标记的临时资产，尚未达到最终电影级品质。未接入账号、服务器、班级系统或跨设备记录同步。模型、纹理、光学计算均本地生成；刻度字体已内嵌，界面使用本机字体，不需要外部字体或 3D 资产服务。
