# 二氧化碳 3D 互动实验室

这是原凸透镜实验之外的独立初中化学实验，使用 React、Three.js、React Three Fiber、TypeScript 和 Vite。器材为程序化临时资产。

## 离线使用

下载 `downloads/chemistry-co2-lab-v1.zip`，**解压后双击“二氧化碳实验室.html”**，用较新版 Chrome / Edge 打开。下载时需联网，下载后运行无需联网、无需安装 Node.js。浏览器需支持 WebGL2。请勿在压缩包或网盘预览器内运行。

## 建议操作

1. 从器材柜取用锥形瓶、双孔塞、长颈漏斗、导气管、集气瓶、检验烧杯、木条。玻璃片可选；本实验不需酒精灯加热。
2. 安装双孔塞、塞紧。漏斗高度20、发生器出气端65、集气端10，集气瓶口朝上。点发生器接口再点集气瓶接口。
3. 加检查水、夹闭导气管、检查气密性并观察液柱。排出检查水、打开夹子，取下瓶塞，去“制气”放入大理石，然后回“装置”复装瓶塞并核对密封。
4. “检验”页加新鲜石灰水；在“装置”页把发生器改接检验烧杯。在“制气”页加稀盐酸，观察石灰水变浑浊。过量通气后可能变清，要记录过程。
5. 改接集气瓶，继续规范收集。比较木条伸入瓶内与放在瓶口的现象；瓶内熄灭不能证明收集满。规范瓶口验满后可断管、盖玻璃片。
6. 记录观察、导出CSV，打开“原理与易错辨析”做6道题。自主挑战模式先观察，按需打开分析；增压风险立即提示。

时速可选“手动推进”，每次推进5个虚拟秒，便于课堂停留讨论。**暂停仅暂停虚拟时间，真实反应不能按按钮停止。**位置刻度不是厘米读数；速率和浓度阈值是定性教学参数。

## 开发运行

在仓库根目录：

```sh
npm ci
npm run dev:chemistry
# 打开 http://localhost:5174
npm run test:chemistry
npm run build:chemistry
npx playwright install chromium
node chemistry/scripts/check-offline.mjs
python3 chemistry/scripts/package.py
```

需要 Node.js 20.19+ 或22.12+。`model.ts`负责计算，`Scene.tsx`负责三维，`main.tsx`负责操作、教学和观察记录。原物理实验入口不变。
