# 简谱查歌前端：Cloudflare 与 **GitHub Pages** 两条部署路（2026-09-25）

> **线上地址（2026-09-25 实测）：https://jianpu-db.github.io/**
> 仓库已改名/转移到组织站 **`jianpu-db/jianpu-db.github.io`** —— `<org>.github.io` 这种仓库发在
> **域名根**上（普通项目仓库才是 `user.github.io/<repo>/` 子路径）。两种位置本产物都支持。

姊妹篇: `_analysis/deploy/cloudflare/README.md`（Cloudflare 那条路的来龙去脉）。
这份回答两个问题: **① 现在是怎么部署的 ② 能不能改成 xxx.github.io 的格式** —— 能, 已经做好了。

---

## 一、现在怎么部署的（Cloudflare，主线路）

```
jianpu-db/data.jsonl + jianpu-db/scores/*.txt
        │  python3 jianpu-web/tools/build_web_data.py          ← 语料侧, 在本机跑(要语料/要 jptok)
        ▼
jianpu-web/data/songs.jsonl.gz + stats.json                     ← 已入库(.gitignore 只 ignore 明文)
        │  node jianpu-web/tools/build_dist.mjs                 ← --target cf(默认)
        ▼
jianpu-web/dist/  =  index.html + static/app.<hash>.js 等 + data/* + _headers
        │  npx wrangler pages deploy dist --project-name jianpu-web --branch master --commit-dirty=true
        ▼
https://jianpu-web.pages.dev        （国内可达; *.workers.dev 那条路在国内被 DNS 污染, 已弃）
```

* **静态部分**（占 99% 的功能）: 检索、曲名卡片、`/s/<id>` 每谱一页 —— 全部在浏览器里跑, 不需要服务端。
* **Worker 部分**（`worker/index.js`, 由 `wrangler.jsonc` 绑同一份 `dist/`）:
  * `/api/*` → 反代到本机 `app/server.py`（投稿/补收录/补标签的**写回**, 口径只有一份, 不在这边重写）;
  * `/img/*` → R2 或 `IMG_UPSTREAM` 兜底（前端已不要"原图"栏, 目前没绑 R2);
  * 其它路径 → `env.ASSETS`; 深链回退靠 `not_found_handling: "single-page-application"`。
* **缓存**: `dist/_headers` 给 `/static/*` 永久（文件名带内容哈希）、`/data/*` 一小时、HTML 不缓存。

## 二、GitHub Pages 那条路: `--target gh`（已实现并自检）

```
node tools/build_dist.mjs --target gh          →  dist-gh/   （默认 --out dist-gh）
```

产物比 cf 多/少三样, 全是 Pages 的规矩逼出来的:

| | Cloudflare (`cf`) | GitHub Pages (`gh`) |
|---|---|---|
| 深链 `/…/s/<id>` | Worker assets 的 SPA 回退 | **`404.html`**（内容 = index.html, 逐字节相同）; Pages 对未知路径就发它, HTTP 状态是 404 |
| 缓存头 | `_headers` | **不写**（Pages 不认这个语法; 靠内容哈希, `max-age=600` 也安全） |
| Jekyll | 无关 | **`.nojekyll`**（不带下划线文件被吞/被处理） |
| 写回 `/api/*` | Worker 反代本机 | 没有 → 构建注入 `window.JIANPU_READONLY=true`, 前端直接说人话 |
| 子路径 | 根 `/` | **`/jianpu-web/`**（`user.github.io/<repo>/`） |
| 老浏览器 | `songs.jsonl` 明文回退(本地部署才有) | 同样没有（明文 13MB 没入库, 与 cf 线上一致） |

* **子路径 + 深链**为什么能work: `static/index.html` 最前面那段**内联 `<base>`** 会按
  "文档地址 = 应用根 + 可能多的 `s/<id>`" 把根摆正 —— 于是 404.html 在 `/jianpu-web/s/<id>` 上发出来时,
  `./static/app.<hash>.js` 仍然解析到 `/jianpu-web/static/…`。`#/s/<id>` 这种 hash 深链也照旧可用。
* **`.gz` 的两种服务端行为都认**: 有的静态托管把 `.gz` 原样发（要自己解压）, 有的会替我们解好并带
  `Content-Encoding: gzip`。`app.js` 现在先看头、解压失败再回退读原文 —— 两条路都试过才算数。
* **只读不是残废**: 检索/卡片/谱页/元数据全都在; 只是"投稿/补收录/补标签"会显示
  "这里只读…请到 jianpu-web.pages.dev 提交", 而不是发一个必 404 的请求。
  想让镜像**也能投稿**: `--api https://jianpu-web.pages.dev`
  （Worker 已放行 `/api/*` 的跨域预检: `OPTIONS -> 204 + Access-Control-Allow-Headers: Content-Type`,
  然后它照旧转发给本机; 本机不在线时给 503 人话）。

## 三、怎么启用（一次性, 需要人点一下）

1. 仓库 **Settings → Pages → Build and deployment → Source: GitHub Actions**。
2. push 到 `master`（或手动跑 Actions 里的 `Deploy to GitHub Pages`，或对已失败的 run 点 Re-run）——
   `.github/workflows/pages.yml` 会: 跑 `JIANPU_QUICK=1 bash tools/check_gh_pages.sh` 自检 →
   `--target gh --out dist` 构建 → `actions/upload-pages-artifact` + `actions/deploy-pages` →
   **再取一次首页实测**（见下面那个坑）。
3. 线上地址: **https://jianpu-db.github.io/**（`<org>.github.io` 站点在域名根; github.io 在本机/国内可达）。

### ⚠ 实测踩到的坑：`deploy-pages` 说"成功"≠站点在发我们的东西

2026-09-25 第一次真发布（run #1, `ca830e8`）：run 全绿（build 16s + deploy 9s），可站点打开是
**GitHub Pages 的 404 页**。逐项取文件才看清: `/tools/build_dist.mjs`、`/package.json`、
`/static/app.js`（仓库源码树里有的）全是 **200**，而产物里的 `/index.html`、`/404.html`、
`/static/app.<hash>.js` 全是 **404** —— 说明 **Pages 的 Source 是"分支"模式**, 发的是仓库源码树;
artifact 根本没上线, 但 `deploy-pages` 仍然报成功。

对应改法（`063712b`，都已自测）:
* probe 步骤顺带读 Pages 配置里的 `build_type`: `workflow` 才发布; `legacy` 就**只构建+自检**并留一条
  notice 写明去改哪个下拉框（**不起红叉**, 免得又出现"绿了/红了都看不懂"的情况）; 读不到就试着发。
* `deploy` 之后加一步**取回首页**: 6 次×20s 内必须拿到引用 `static/app.<hash>.js` 的 index.html,
  否则 `::error::` 明确点出"Source 还不是 GitHub Actions"。

Runner 上**不需要语料、不需要 Python**: `data/songs.jsonl.gz` 与 `stats.json` 本来就在仓库里,
所以这条 CI 只有 node, 几十秒就完事。（`pages.yml` 里 `concurrency.cancel-in-progress: false`:
发布**故意不取消**在跑的那次 —— 今天刚踩过"被取消 = 列表里一个红叉, 看着像失败"。）

备选（没做成脚本, 需要时再加）: 本地 `node tools/build_dist.mjs --target gh` 后把 `dist-gh/` 推到一个
`gh-pages` 分支, 再把 Pages 的 Source 选成"Deploy from a branch"。同样是**一次设置页改动**, 好处是不依赖
Actions, 坏处是每次更新都要在本机再推一个 3.5MB 的分支提交。

## 四、本地怎么验（和线上同一套规矩）

```
bash tools/check_gh_pages.sh              # 构建 + 产物断言 + 真浏览器(GitHub Pages 模拟)
JIANPU_QUICK=1 bash tools/check_gh_pages.sh   # 跳过真浏览器(CI runner 上就是这么跑)
python3 tools/browser_check.py ghpages    # 单跑那一步
```

`browser_check.py ghpages` 不是"再跑一遍 subdir": 它按 **Pages 的真实规矩**起静态服务 ——
站点挂在 `/jianpu-web/` 子路径、未知路径发 `404.html`（状态 404）、**没有 SPA 回退**、没有 `/api`;
然后用真浏览器验: 首页语料加载、只读提示与投稿拦截、`/s/<id>` 由 404.html 发出仍能渲出谱页、
`#/s/<id>` 深链、「回检索」指回子路径根。

## 五、已知边界

* Pages 不给自定义响应头 → 没有长缓存, 也没有 `/img/*`; 原图栏早已去掉, 所以不痛。
* 仓库软限制 1GB / 月流量 100GB: 现在整站 3.5MB, 无碍。
* 两份部署**数据同源**: 都是 `jianpu-web/data/*`（入库的那份）; 换了语料要重跑
  `tools/build_web_data.py` 并提交, 两条路才会一起更新。
