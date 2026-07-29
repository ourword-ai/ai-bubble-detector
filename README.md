# 🫧 AI 泡沫检测仪 · AI Bubble Detector

**Live:** https://ourword-ai.github.io/ai-bubble-detector/
**Repo:** https://github.com/ourword-ai/ai-bubble-detector （公开，GitHub Pages 从 `main` 根目录）

拖动 6 个指标，实时算出一个 AI 项目的「泡沫指数」(0–100)，配 SVG 仪表盘 + 判词。纯娱乐，not investment advice。

---

## 这是什么 / 技术栈
- **单文件**：所有东西都在 `index.html` —— 原生 HTML/CSS/JS，**无构建、无依赖**，双击即可打开。
- 部署：GitHub Pages（`main` 分支根目录 + `.nojekyll`）。改完推到 `main`，约 1 分钟后线上更新。

## 怎么改（安全编辑指南）
逻辑都在 `index.html` 底部的 `<script>` 里：
- **`METRICS`** —— 6 个滑块，每项 `{key, w(权重，合计必须=1.0), label, lo, hi, def}`。加/改指标动这里；改完确认权重仍加到 1.0。
- **`BANDS`** —— 判词分档 `{min, name, emoji, color, quip}`，按分数取命中的最高档。
- **打分**：`score = Σ(滑块值 × 权重)` 四舍五入；指针角度 `-90 + score×1.8`；任何滑块变化触发 `compute()` 重算。
- **原则**：保持**单文件、零依赖**（quickship 是把整个文件夹发布的）；中文为主，判词俏皮但别尬；保留免责声明。

## 怎么发布更新（让线上生效）
仓库和 Pages 都已建好，所以更新 = 提交并推到 `main`（**不需要**重新建仓库）。

**方式 A —— 用 `quickship` 技能（最省事）**
让 Claude 对项目文件夹跑 `quickship`，仓库名填 `ai-bubble-detector`。同名会**强制更新**现有站点。

**方式 B —— 手动 git**
token 在 `~/quickship/token.txt`（一个有 `repo` 权限的 GitHub PAT）。在 Claude 里先连上该文件夹：`request_cowork_directory ~/quickship`。

```bash
git clone https://github.com/ourword-ai/ai-bubble-detector
cd ai-bubble-detector
#  …编辑 index.html…
git add -A && git commit -m "polish"
TOKEN="$(tr -d '[:space:]' < ~/quickship/token.txt)"
git push "https://x-access-token:$TOKEN@github.com/ourword-ai/ai-bubble-detector.git" HEAD:main
```

> GitHub Pages 的 CDN 会缓存约 10 分钟；想立刻看到改动，用浏览器对该 URL 执行一次 `fetch(url,{cache:'reload'})` 再刷新页面。

## 给接手的 Claude 的话
- **源码以 GitHub 仓库为准**。Cowork 的 outputs 目录是临时的、跨会话不保留 —— 所以**先 clone 仓库再改**，别指望上一会话的本地文件还在。
- token 路径固定 `~/quickship/token.txt`；新会话第一次读它，可能需要用户点一下"允许访问 ~/quickship"。
- 改完**务必推到 `main`**，再打开线上 URL 自检渲染正常，才算完成。

## 待办 / 可打磨方向
- **分享卡片**：加"生成结果卡"按钮，把分数 + 判词渲染成一张可分享的图（canvas → PNG）。
- **可保存链接**：把 6 个滑块状态编码进 URL hash（如 `#80-75-60-70-55-65`），加载时解析 —— 一份配置可收藏/转发。
- **预设**：一键套用几个"名场面"（超级独角兽 / 务实小厂 / 纯 PPT 创业）看分数。
- **贡献拆解**：显示每个指标对总分的贡献条。
- **文案 & 英文开关**：更锋利的判词；中英切换。

MIT.

## 两个页面

| 页面 | URL | 是什么 |
| --- | --- | --- |
| 滑块版（首页） | `/` | 拖 6 个指标算泡沫指数，纯娱乐 |
| 监测面板 | `/monitor.html` | 严肃长版：19 条监测条件（干柴 / 火药 / 扳机三级）、倒计时、八维度、红线自审、证伪清单。数据带日期与出处 |

### monitor.html 怎么维护
- 和首页一样：单文件、零依赖，直接改 HTML。
- **计数不用手改**：页首 / 记分牌 / 层级标题由脚本从三个层级块（`.tier .ti[data-h]`）实时核算。改判定只改条目的 `data-h`：`1` 命中 / `0` 未中 / `d` 口径分歧；表格行的状态芯片（`.st[data-s]`）需同步改一下样式标签。
- **价格类数据**（CDS、利差、DRAM、H100、DSO…）按页内「动态更新 → 手抄清单」回原始来源手抄；改完更新页首「数据截至」，并在 `<script>` 的 `SEED_LOG` 追加一条变更记录（`{d,k:'add|del|fix|hit',t}`）。
- 「联网核查事件」按钮只在 Claude 里打开本页时可用（公网版没有 API 凭证，点了会提示改用手抄清单）。候选 / 变更日志 / 倒计时录入在公网版存 localStorage，仅当前浏览器可见。
- 倒计时行到期自动出现「录入结果」，录完写日志并变灰；日期在 `.tr2` 的 `data-due` / `data-tid` 上。
