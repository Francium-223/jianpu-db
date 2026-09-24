# Cloudflare 部署准备（2026-09-24）

> 用户：**"现在Cloudflare那边让我create an app。你要怎么准备？"**

## 0. 先说清楚：Cloudflare 里"Create an application"是**两个完全不同的东西**

| 你在哪一面 | 面板里长这样 | 这条路对这个项目意味着什么 |
|---|---|---|
| **Zero Trust → Networks → Tunnels** | *Create a tunnel* | ✅ **不用改一行代码**：把本机 `127.0.0.1:8770` 发到公网。8.9GB 扫描件照样由本机 `app/server.py` 发, 投稿写库照样跑（git commit 在本机）。**推荐先走这条。** |
| **Zero Trust → Access → Applications** | **Create an application** | 这是给**已存在的隧道**加"登录门"（Self-hosted 应用）。本站有写接口, 必须有它 —— 见下面第 3 节。 |
| **Workers & Pages → Create application → Pages** | *Create application* | 纯静态托管：前端能上（`static/` + `data/` 才 3MB）, 但 **① 8.9GB 原图无处安放**（要在 R2 另建桶 + Worker 转发）**② `/api/submit` 没人执行**（要在 Worker 里调 GitHub API 提交）。见第 4 节。 |

**所以第一个问题就是：你屏幕上那个 "Create an application" 是在 Zero Trust 里，还是在 Workers & Pages 里？**
（把页面标题/面包屑念给我就行。）两条路的准备我已经都做了/写清了。

## 1. 我已经做好的准备（本机，零 sudo）

* **装好了 `cloudflared 2026.9.1` → `~/.local/bin/cloudflared`**。
  ⚠ 这台机器 **GitHub release 资产下载被墙**（`objects.githubusercontent.com` 连不上, `curl` 报
  `unexpected eof`），所以走 Cloudflare 自己的包站下 `.deb` **免 sudo 解包**：
  ```bash
  curl -s https://pkg.cloudflare.com/cloudflared/dists/any/main/binary-amd64/Packages | awk -F': ' '/^Filename:/{print $2}' | head -1
  # 注意仓库根是 https://pkg.cloudflare.com/cloudflared/ （不是 /）
  curl -sSLo cf.deb https://pkg.cloudflare.com/cloudflared/pool/main/c/cloudflared/cloudflared_2026.9.1_amd64.deb
  sha256sum cf.deb   # 与 Packages 里的 SHA256 对上（已核对 ✓）
  dpkg-deb -x cf.deb cfx && cp cfx/usr/bin/cloudflared ~/.local/bin/
  ```
* **临时公网地址，当场验证整条链路**（`quick_tunnel.sh`，不用账号/域名）：拿到了
  `https://lbs-hiking-xhtml-rental.trycloudflare.com`，逐条打过去：

  | 路径 | 结果 |
  |---|---|
  | `/` | 200 · text/html · 5.5KB |
  | `/static/app.js` `/static/style.css` | 200（ES module 正常加载） |
  | `/data/songs.jsonl.gz` | 200 · 2.77MB |
  | `/data/images.jsonl.gz` | 200 · 502KB |
  | `/s/qupu123-313063`（谱页深链） | 200 · 同一个 index.html |
  | `/img/…/001.jpg`（真原图） | 200 · image/jpeg · 36,273B（**与本地字节数一模一样**, 没被截断/转换） |

  并且用**真浏览器走公网**跑了一遍交互自检（`browser_check.py spa https://…trycloudflare.com`）：
  查歌出卡片 → 点「本谱一页」不刷新跳转 → 地址栏变 `/s/<id>` → 后退结果还在 →
  深链出原图且**真的解码**（`naturalWidth>0`）→ 刷新仍在这一页。**全绿**（顺手修掉了这条自检在
  慢网下的一处假红：图片是 lazy 的，元素一出现就断言 `naturalWidth` 会误报，现在会等它真解码）。

  验证完就把那个临时地址**关掉了**（它是公开的，而这个站带写接口）。

## 2. 固定域名那条路（`setup_tunnel.sh`，幂等、免 sudo）

```bash
HOSTNAME=jpt.你的域名 bash _analysis/deploy/cloudflare/setup_tunnel.sh
```

它依次做：检查 `cloudflared` 与本机服务 → `tunnel login`（**只有这一步要你在浏览器点一下授权**）
→ 建/复用隧道 → 写 `~/.cloudflared/config.yml`（ingress 校验）→ 装 `cloudflared.service`
（**用户级** systemd，`Restart=always`，与本项目 `jianpu-web.service` 同一套路；linger 已经开着）
→ `tunnel route dns` 写域名 → 从公网 `curl https://$HOSTNAME/` 验证。

配套文件（都在这个目录）：`cloudflared.service`、`config.yml.template`、`quick_tunnel.sh`。

## 3. 面板上要你点的那几下（Zero Trust → Access）

* Applications → **Create an application** → **Self-hosted**
* Name：`简谱旋律查歌`；Session Duration：`1 month`
* Public hostname：`jpt.你的域名`（与隧道那条一致）
* Policy：Action=**Allow**，Include=**Emails** → 你自己的邮箱（登录方式用 One-time PIN）

**为什么必须加这道门**：`app/server.py` 的 `/api/submit` 会**在你本机 git commit 到 jianpu-db**
（这是"零登录投稿"的设计）。公网裸奔 = 任何人可以往你的语料里塞东西、在你机器上写文件。
（另有一个 `JPSUBMIT_TOKEN` 头校验，但前端表单不会带头，所以那道闸只能靠 Cloudflare Access。）

顺手在面板上关掉两个会坏事的东西：
* **Speed → Optimization → Rocket Loader = Off** —— 它会破坏 `<script type="module">`，页面直接白屏；
* **Auto Minify = Off**（对 JSON/JS 压缩没好处，还可能动到我们的数据）。
* 可选：Cache Rules 给 `/img/*` 设 "Cache Everything / Edge TTL 7 天" ——
  我们本来就发了 `Cache-Control: public, max-age=604800`，Cloudflare 默认就会缓存图片；
  **但换了图要 Purge**（图路径不变），否则最多 7 天旧图。

## 4. 如果你其实想走 Pages（静态托管）

能上的部分：`jianpu-web/` 整个仓库只有 3MB（`static/` + `data/songs.jsonl.gz` 2.77MB +
`data/images.jsonl.gz` 0.5MB），Pages 完全装得下。要补的三件事：

1. **入口**：Pages 默认找站点根 `index.html`，我们的入口在 `static/index.html` ——
   加一个根 `index.html` 转发（或在 Pages 里设 build 输出目录）。子目录部署也已经支持
   （`index.html` 里那段内联 `<base>`，`browser_check.py subdir` 专门验它）。
2. **原图 8.9GB → R2**：建桶 + 一个 Worker 路由 `/img/*` 回源到桶（R2 免费 10GB 存储、
   出网不要钱）。构建脚本要改成把本地 `images/` `images-prep/` 同步上去（`rclone`/`wrangler r2 object put`）。
   `stats.json` 里的 `img_base` 改成 CDN/Worker 的前缀即可（前端只认这一个变量）。
3. **投稿接口 → Worker**：`/api/submit` 现在做的是"写盘 + git commit"，Pages 上跑不了；
   要么在 Worker 里用 GitHub API 开 PR/提交（要一个 repo token 作 secret），
   要么**保留本机服务专门处理投稿**（前端 `window.JIANPU_API` 指到隧道域名，CORS 已允许
   `Access-Control-Allow-Origin: *`，投稿表单不用改）。

**顺序建议**：先 `setup_tunnel.sh` + Access（今天就能有可用站点、图片与原图全在），
等真要对外开放再迁 R2/Pages —— 那时语料索引照旧，只是把"图放哪"和"谁执行投稿"换掉。

## 5. 一页速查

```bash
# 免 sudo 装（GitHub 被墙时走 CF 包站）
curl -s https://pkg.cloudflare.com/cloudflared/dists/any/main/binary-amd64/Packages | awk -F': ' '/^Filename:/{print $2}' | head -1

# 临时看效果（公开! 用完 Ctrl-C）
bash _analysis/deploy/cloudflare/quick_tunnel.sh

# 固定域名 + 常驻 + Access（面板那步见 §3）
HOSTNAME=jpt.example.com bash _analysis/deploy/cloudflare/setup_tunnel.sh
systemctl --user status cloudflared        # 排障
journalctl --user -u cloudflared -n 50
curl -s https://jpt.example.com/api/health # 隧道 + 本地服务一起验
```

---

# 附：如果你在 **Workers → "Create application"** 那一面（2026-09-24 晚补）

你屏幕上的这些字样——`Start from a template` / `Continue with GitHub` / `Upload your static files` /
**`Need to use the legacy Pages workflow? Continue to Pages`** / `Select a repository`——说明这是
**新版 Workers 的创建流程**（"Continue to Pages" 那句就是标志：Pages 现在是 legacy）。
它下一步会拿你选的仓库去 `npm ci && (build) && npx wrangler deploy`。

## 选哪个仓库

**选 `jianpu-web`**（前端 + 数据索引 + Worker 包装；`jianpu-db`/`jianpu2` 不是网站, 别选）。
仓库里我已经放好了让它能一键构建部署的东西：

| 文件 | 作用 |
|---|---|
| `wrangler.jsonc` | Worker 名/入口/assets(`dist`)/SPA 回退/R2 绑定 |
| `worker/index.js` | Worker 本体: `/img/*`→R2, `/api/*`→反代本机, 其余交给 assets |
| `package.json` | `build = node tools/build_dist.mjs`, `deploy = wrangler deploy` |
| `tools/build_dist.mjs` | 把 `static/`+`data/` 拼成 `dist/`（**纯 Node**, 云端构建镜像没有 Python） |
| `tools/r2_filelist.py` / `tools/r2_sync.sh` | 只把"索引真正用到的"26,416 张图（5.08GB）传进 R2 |

面板里要填的（如果它让你填）：**Build command `npm run build`**、**Deploy command `npx wrangler deploy`**。

## 我在本机已经验证过的东西（`npx wrangler dev --local`，真跑 workerd）

| 检查 | 结果 |
|---|---|
| `/`、`/static/app.js`、`/static/style.css`、`/data/songs.jsonl.gz` | 200 |
| `/s/qupu123-313063`（深链） | 200 · 返回 index.html（SPA 回退生效） |
| `/api/health` | 200 · `{"ok":true,"deploy":"cloudflare-worker","api":false}` |
| `POST /api/submit`（没配后端时） | 503 · 人话说明"这台部署没有配投稿后端" |
| `/img/<key>`（R2 里有） | 200 · image/jpeg · 带 `cache-control: max-age=604800` |
| `/img/%2e%2e/wrangler.jsonc`（越界） | URL 规范化成 `/wrangler.jsonc` → SPA 回退给 index.html, **没泄露配置** |
| `/img/images/x.txt`（非图扩展名） | 404 |
| **真浏览器走 Worker 全流程**（`browser_check.py spa http://127.0.0.1:8787`） | 查歌出卡片 → 点「本谱一页」不刷新跳转 → 后退结果还在 → 深链出原图且真解码 → 刷新仍在这一页 · **全绿** |

⚠ 期间抓到两个真问题（都已修）：
1. **R2 key 的两种写法**：`wrangler r2 object put` 会把中文 key **百分号编码**后再存
   （实测存进去的是 `…/%E6%80%80%E5%BF%B5__…`）。Worker 现在**两种都认**（先按解码后的规范形式查,
   再按 URL 原样路径查）；批量上传请走 **S3 API（rclone/aws-cli）**, 它存的是原样 UTF-8 key。
2. **`/img/%2e%2e/...` 会被 URL 规范化掉**（`%2e%2e` 等同于 `..`），所以它压根到不了 R2 处理器 ——
   这也意味着"越界"不是 404 而是走到 SPA 回退, 测试断言要看**有没有泄露内容**, 不能只看状态码。

## 图片放哪：R2（免费额度就够）

* 只传索引引用到的 **26,416 张 / 5.08GB**（工作区里总共 9.47GB, 多出来的是没转写、或被派生件顶掉的）。
  清单：`python3 tools/r2_filelist.py` → `_analysis/r2_files.txt`；上传：`bash tools/r2_sync.sh --check` 然后
  `bash tools/r2_sync.sh`（rclone 优先, 16 并发 + 断点续传；装 rclone 不需要 sudo）。
* 一次准备：`npx wrangler r2 bucket create jianpu-images` + 面板建 R2 的 S3 凭据 + 配 rclone remote。
* 5GB 从家里上行传一次要挺久（按 10Mbps 上行 ≈ 70 分钟起）, 传完就不再管了。

## 投稿接口怎么办（`/api/submit`）

Worker 里**不重写**投稿逻辑——校验收录页 URL、归一化简谱数字、写 `scores/*.txt` + git commit
这些口径只有一份实现（`jianpu-db/linkurl.py` + `score.py` + `schema.py`）。所以 Worker 只做**反代**：

```bash
npx wrangler secret put API_UPSTREAM     # 本机服务的公网地址, 例 https://jpt-api.你的域名
npx wrangler secret put API_TOKEN        # 与本机 systemd 的 JPSUBMIT_TOKEN 同一个值
```

配好之后：**读路径完全在边缘**（检索/卡片/谱页/原图都不需要本机在线）, 只有"投稿"会回到本机。
不配也能跑, 只是投稿会回一句"这台部署没有配投稿后端"。

## 数据更新怎么办

`jianpu-web` 的 push 会触发 Cloudflare 自动构建部署（`npm run build` + `wrangler deploy`）——
所以本机跑完 `refresh.sh`（重建 `data/songs.jsonl.gz`/`stats.json`）后 `git push` 一下就发布了。
原图只在新收录时才需要补传（`r2_sync.sh` 幂等, 跑一次只补新的）。

## 你只要回我三样

1. 面板上那个页面选 **jianpu-web**（如果它问 build/deploy 命令, 按上面填）；
2. R2 桶建好后告诉我桶名（默认我写的是 `jianpu-images`）；
3. 想用的域名（如 `jpt.你的域名`）——我好把 `wrangler.jsonc` 的 routes、Worker 的 `API_UPSTREAM`
   和 Access 那条一起收尾。

---

# 最终形态（2026-09-24 深夜，用户口径定版）

## 部署在哪

**Cloudflare Pages**：`https://jianpu-web.pages.dev`（免费版：每站点 2 万文件 / 单文件 25MiB / 带宽不限；
免域名、免绑卡、**大陆可直连**——本机实测 200，`*.vercel.app` 与 `*.workers.dev` 都是 000 被污染）。
部署命令：`npm run build && npx wrangler pages deploy dist --project-name jianpu-web --branch master`
（Workers 那条 `workers.dev` 留着但**大陆打不开**，别再用了；R2 未开通，`r2_buckets` 已在 wrangler.jsonc 里注释掉）。

## 谱页长什么样（两条用户口径，都是"减"）

1. **没有"原图"那一栏** —— 不转存扫描件、也不外链图片。原站页面地址本来就在「出处」和「收录页」里。
   （曾试过：直接 hotlink 原站图 → jianpu.cn 是 http，https 页面按混合内容拦掉；Cloudflare 代取 → 需要 Functions/Worker，
   且要重新抓 7,281 页拿图片 URL。都不划算，用户直接说"不用原谱图这一栏了"。）
2. **"原谱原文"是文件 verbatim** —— 曲谱文件正文原样（`4/4`/`subtitle=`/`KeepLength`/`[`/`]`/`~`/`-`/换行全都保留），
   **不是** `data.jsonl` 里那份"展开过"的 token 流（节头去掉、省略时值补全、多节拼平 —— 67 首受影响），
   也**不注入**自动恢复的小节线。
   * 实现：`jianpu-web/tools/build_web_data.py` 在**网页构建时**直接读 `jianpu-db/scores/<file>.txt` 的正文，
     写成前端索引里的 `src` 字段（`raw` 仍保留给检索卡的命中高亮）。
   * ⚠ **`data.jsonl` / `parse_scores.py` / `score.py` 一个字都没动**（md5 与 HEAD 一致，`jianpu-db` 工作区干净）——
     语料那份口径不变，HF 数据集也不变。索引体积：2.77MB → 3.40MB gz。
   * 自检：`tools/check_tune.mjs` 断言 `pre.sheet` 的内容 `=== esc(src)`、"没有注入 span/小节线"、
     "显示的**不是** raw 那份展开版"。

## 静态资源带内容哈希

`tools/build_dist.mjs` 把 `app.js`→`app.<hash8>.js`（CSS 同理、JS 之间的 import 一起改），
`_headers` 里 `/static/*` 因此可以 `max-age=31536000, immutable`。
为什么必须：不带哈希时长缓存会让**部分边缘节点继续发旧 JS**（实测：同一个页面，截图里还在渲染碎图、
无头浏览器里 img 数为 0 —— 两种结果并存）。

## 自检入口

```bash
bash tools/check_all.sh          # 9 组: 投稿漏斗/图索引/渲染/检索/UI/谱页(verbatim)/线上/真浏览器/Worker
node tools/check_tune.mjs        # 只看"每谱一页"
SHOW_TUNE=1 node tools/show_card.mjs 铺开一片蔚蓝 1     # 文字预览谱页
bash tools/cf_deploy.sh          # 用本机 wrangler 直接部署(排障用)
```
