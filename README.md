# 🫧 AI 泡沫检测仪 · AI Bubble Detector

**Live:** https://ourword-ai.github.io/ai-bubble-detector/
**Repo:** https://github.com/ourword-ai/ai-bubble-detector （公开，GitHub Pages 从 `main` 根目录 + `.nojekyll`）

AI 基建泡沫监测面板：19 条监测条件（干柴 / 火药 / 扳机三级）、倒计时（含到期录入）、八维度、
红线自审、证伪清单、变更日志。每个数字都带日期与出处。Not investment advice。

> 2026-07-29 起监测面板即首页；原滑块版计算器已下线（要找回去 git 历史 `b376e6d` 及之前），
> 旧地址 `/monitor.html` 保留重定向。

## 结构

| 路径 | 是什么 |
| --- | --- |
| `index.html` | 监测面板本体（单文件、零依赖、原生 HTML/CSS/JS） |
| `monitor.html` | 重定向到 `/`（兼容旧链接） |
| `data/auto.json` | 自动数据管线的输出（GitHub Actions 定时写入） |
| `scripts/update_data.py` | 抓 FRED 序列的脚本（纯 stdlib，无依赖） |
| `.github/workflows/update-data.yml` | 每个工作日跑上面的脚本，有变化才提交 |

## 数据怎么更新（三条路）

1. **自动管线（无人值守）**：GitHub Actions 每个工作日抓 FRED（核心 PCE 同比 `PCEPILFE`、
   单 A 公司债 OAS 参考 `BAMLC0A3CA`）写入 `data/auto.json`；页面加载时把 `[data-auto=…]`
   的显示值替换成最新值，页首标注刷新日期。自动值与页内快照判定冲突时（如 PCE 跌破红线 3.0）
   页面标 ⚠，等下一条的编辑核对。**自动管线只改显示，不改判定。**
2. **定时研究更新（Claude，周一 / 周四早）**：按页内「动态更新 → 手抄清单」回原始来源核对价格类数据、
   联网核查事件（评级 / 财报 / S-1 / 减值 / 清算…）、录入到期倒计时、必要时翻转红线判定（`data-h`），
   追加 `SEED_LOG` 变更记录，更新页首「数据截至」，jsdom 自检后推送。
3. **手动**：见下方维护指南。

## 维护指南（改 index.html）

- **计数不用手改**：页首 / 记分牌 / 层级标题由脚本从三个层级块（`.tier .ti[data-h]`）实时核算。
  改判定只改条目的 `data-h`：`1` 命中 / `0` 未中 / `d` 口径分歧；表格行状态芯片（`.st[data-s]`）同步改。
- **价格类数据**按手抄清单回原始来源手抄；改完更新页首「数据截至」，并在 `<script>` 的
  `SEED_LOG` 追加变更记录（`{d,k:'add|del|fix|hit',t}`）。判定翻转必须写明依据与出处。
- **接入自动管线的两条**（核心 PCE、单 A OAS 参考）不用手抄——HTML 里的快照值落后没关系，
  加载时会被 `data/auto.json` 覆盖；编辑要做的是在判定变化时更新 `data-h` 和正文。
- 倒计时行到期自动出现「录入结果」；日期在 `.tr2` 的 `data-due` / `data-tid` 上。
- 候选 / 变更日志 / 倒计时录入在公网版存 localStorage，仅当前浏览器可见。

## 发布

token 在 `~/quickship/token.txt`（`repo` 权限 classic PAT）。

```bash
git clone https://github.com/ourword-ai/ai-bubble-detector && cd ai-bubble-detector
# …编辑…
git add -A && git commit -m "update"
TOKEN="$(tr -d '[:space:]' < ~/quickship/token.txt)"
git push "https://x-access-token:$TOKEN@github.com/ourword-ai/ai-bubble-detector.git" HEAD:main
```

红线：不 force push；token 不得出现在任何输出 / 日志 / 提交；推送前自检（页首计数行渲染正常、
无 JS 报错）。Pages CDN 缓存约 10 分钟，急看用 `fetch(url,{cache:'reload'})` 后刷新。

## 给接手的 Claude 的话

- **源码以 GitHub 仓库为准**，先 clone 再改（在 VM 本地目录跑 git，挂载目录会锁文件失败）；
  Cowork outputs 目录跨会话不保留。
- 自动管线只负责两条 FRED 序列，别让它「顺便」改判定；判定与正文永远走人工 / 定时研究更新。
- 改动小而有据：没有可靠来源就不改数，宁可标「待核」。页面的可信度全部押在
  「每个数字都带日期与出处」上。

MIT.
