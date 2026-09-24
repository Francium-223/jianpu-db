# 简谱查歌前端：Cloudflare 与 **GitHub Pages** 两条部署路（2026-09-25）

> **线上地址（2026-09-25 03:19 实测已上线）：https://jianpu-db.github.io/**
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

## 三、怎么启用（已生效；另有"更干净"的一种模式）

站点已经在发构建产物（`curl -sI https://jianpu-db.github.io/` → 200 + 正文引用 `static/app.<hash>.js`）。
当前用的是 **"Deploy from a branch" 模式** —— 为了让它在**不改任何设置**的前提下就能用，
构建产物被**提交到了仓库根**：`index.html`、`404.html`、`.nojekyll`、`static/app.<hash>.js` 等
（与源码不冲突：产物是带内容哈希的文件名；`data/*` 本来就在仓库里）。
`.github/workflows/pages.yml` 每次 push 都会**同步**这些产物并提交（带 `[skip ci]`），所以不会发旧版。

| | **分支模式**（当前） | **GitHub Actions 模式**（更干净） |
|---|---|---|
| 站点发什么 | 仓库根（含源码树: `tools/`、`package.json` 也对外可见） | 只发 artifact（`dist/` 那几件） |
| 要人做什么 | 什么都不用 | Settings → Pages → Build and deployment → **Source 选 'GitHub Actions'** |
| 产物在哪 | 提交进仓库根（每次构建产生新哈希文件） | 只在构建机/artifact 里，仓库干净 |
| workflow 行为 | 同步产物 + 也走一遍 Actions 部署（两边内容相同） | 只走 Actions 部署 |

切到 Actions 模式之后，把仓库根那几件产物删掉即可（`git rm index.html 404.html .nojekyll static/*.<hash>.js`），
workflow 会自动只走 Actions。**不切也能一直用** —— 只是仓库根多几件产物、且源码树对外可见。

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
