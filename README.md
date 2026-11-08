# 初中物理 3D 互动实验室 · Stage 01

- 在线发布：源码已准备在 `docs/`；仓库所有者需在 Settings → Pages 选择 Deploy from a branch、main、/docs 后保存。GitHub 当前授权不允许自动开启 Pages。启用后以设置页返回的实际网址为准。
- 推荐离线下载：https://raw.githubusercontent.com/erqiqi46-spec/physics-optics-lab/main/downloads/optics-lab-offline-v1.2.zip（解压后双击 HTML）
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

默认是“探究学习”：

1. 读取轨道坐标 xₒ/xₗ/xₛ 与物距 u、实际屏距 d。侧视图标出测量区间，并显示坐标差算式，轨道位置不再与像距混用。
2. 根据物距与焦距选择像的类型、方向、大小，提交预测。此前光屏有明确的教学遮盖，理论读数、辅助光线、自动对焦及总结关闭。
3. 提交后查看光屏放大窗口，对比同尺度的物体 F 与实际屏面图案；手动移动光屏寻找清晰位置。1×/2×/3×仅放大观察，不改变器材或成像。
4. 选择自己看到的现象，填写可选说明，保存观察。再点击“揭示理论并比较”，查看预测对照、理论像距与辅助光路。
5. 保存后改变屏位或观察说明，需要重新保存；改变物体、透镜或焦距会重开一轮预测。已揭示后调屏只改变屏面清晰度，不改变理论像距。
6. 教师可选择“直接演示”，直接查看理论与光线；学生自主模式使用探究流程。教师切换五类情境时，探究模式使用待手调的屏位，直接演示使用原有预设。
7. 实验数据表及 CSV 分列保存坐标、u/d/f、预测、自述观察和理论。未揭示观察记录不导出理论答案，揭示后补充，同光学条件下的原始观察保留。
8. 总结包含五类规律和 15 道易错题，支持解析、错题复习与观察跳转。滑块支持方向键，按钮、下拉框与输入均可用键盘操作。
9. 拖动空白旋转、滚轮/双指缩放；拖动仪器沿轨道移动。重置恢复器材、当前预测和观察倍率，保留已保存的记录；可另行清空记录。

轨道单位 cm，物距 `u=xₗ−xₒ`，实际屏距 `d=xₛ−xₗ`；理论像距 `v` 从透镜量起，可与当前屏距不同。

## 自动化验证

```bash
npm test
npx playwright install chromium
npm run dev
# 在另一个终端运行：
npx playwright test
```

Playwright 默认使用已经启动的 5173 端口服务器；配置了无头 Chromium 的 SwiftShader 选项，便于无 GPU 的 Linux 环境。测试结果 JSON 与过程截图输出至 `evidence/`。测试脚本会在隔离的浏览器上下文生成记录并导出样例 CSV。v1.2 增加探究流程、答案隐藏、坐标/距离、观察记录导出、屏面放大与空白/离焦校验。

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
- `src/inquiry.ts` / `src/inquiry.test.ts`：探究状态机与 15 项流程/科学对照测试。
- `src/imaging.ts` / `src/ScreenObservation.tsx`：共享投影生成与同尺度放大观察。
- `src/records.ts` / `src/records.test.ts`：观察数据、理论揭示及 4 项 CSV 验证。
- `tests/lab.spec.ts`：4 组基础浏览器端到端测试。
- `tests/learning.spec.ts`：2 组实时光路与 15 道题库回归测试。
- `tests/inquiry.spec.ts`：4 组预测/观察/揭示、放大成像与移动端回归测试。
- `SCIENCE-REPORT.md`：科学检查与成像近似说明。
- `LIMITATIONS.md`：资产性质、已知局限及后续改进。
- `TEST-REPORT.md`：最终执行结果和验收范围。

## 交付范围

这是 Stage 01 可交互核心版本：程序化器材为明确标记的临时资产，尚未达到最终电影级品质。未接入账号、服务器、班级系统或跨设备记录同步。模型、纹理、光学计算均本地生成；刻度字体已内嵌，界面使用本机字体，不需要外部字体或 3D 资产服务。
