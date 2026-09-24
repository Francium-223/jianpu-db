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
