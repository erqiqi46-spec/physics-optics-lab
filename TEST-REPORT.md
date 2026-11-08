# Stage 01 v1.1 自动化验收报告

执行日期：2026-11-08。环境：Linux、Node.js、Vite、Vitest、Playwright Chromium；浏览器使用 SwiftShader 软件 WebGL 渲染。

## 最终结果

- TypeScript 与 Vite 生产构建：通过。
- Vitest：23 / 23 通过，0 失败。
- Playwright：6 / 6 通过，0 失败、0 跳过。
- 题库反馈微调后，额外复跑“十五道易错题、解析、错题复习、进度保留与弹窗层级”通过，确认答错题不会提示“回答正确”。

## 科学与交互验收

原有 11 项测试涵盖五类成像、公式残差、放大率、焦点两侧符号、离焦和轨道约束。新增 12 项测试验证同一物点的各条折射光直线与理论像点一致；u=f 时的倾斜平行出射光；仅虚像显示反向延长线；实线在光屏终止；移动物体改变折射方向；第三主光线受镜片孔径限制；几何裁切不改变理论光路。

浏览器端到端覆盖：

1. 原有完整实验流程、五类情境、离焦与对焦、记录持久化、CSV、重置与模式切换。
2. 390×844 的窄屏键盘和触摸操作，无横向溢出。
3. 鼠标直接拖动三维器材，镜头不随之转动，器材满足轨道约束。
4. Chromium CDP touchStart / touchMove / touchEnd 直接拖动器材。
5. 物体移动使侧视图中心光线端点实时变化；焦点处平行、焦内虚线、显示/隐藏光路切换。
6. 全部 15 道题逐题作答（刻意答错 1 题）：统计 14/15，检查每题解析与易错提示、筛选错题、返回对应实验、重新进入后保留进度、重新作答和 Escape 关闭；检查弹窗位置最上层元素属于弹窗。

## 截图与机器证据

- `evidence/unit-results.json`：23 项科学测试。
- `evidence/browser-results.json`：完整 6 组浏览器测试结果。
- `evidence/build.log`：最新生产构建日志。
- `evidence/offline-v1.1-check.json`：禁用全部外部 HTTP(S) 请求后，直接从本机 HTML 打开；光路随物体变化且 15 道题正常显示。
- `evidence/01-focused-desktop.png` ～ `05-mobile-touch.png`：完整实验与窄屏过程。
- `evidence/06-live-rays-virtual.png`：实时虚像光路。
- `evidence/07-mistake-review.png`：错题复习与弹窗层级修复。
- `evidence/sample-records.csv`：实际导出的五组记录。

首轮在 60 秒测试总限时下有截图步骤超时，其余功能断言通过；软件 WebGL 下扩大的画布与多步截图需要更长时间。最终将端到端总限时调整为 120 秒，保持原断言和单线程执行，完整重跑 6 组通过。此结果不代表真机帧率基准。

未验证真实 Windows 设备、真实多点触摸、Safari/Firefox 和 GPU 性能。器材仍为临时程序化资产，不宣称最终电影级品质。详见 `LIMITATIONS.md`。
