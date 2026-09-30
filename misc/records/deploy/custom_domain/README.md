# 自定义域名 **jianpu-db.org**（2026-09-30）

> 用户："好了，现在我有个 jianpu-db.org 域名了。动态的域名有了，是不是该像个网站（而非 xxx.github.io）一样部署了？"

## 一、结论：域名挂 **Cloudflare Worker**，GitHub Pages 退成只读镜像

| | 正式站点 | 只读镜像 |
|---|---|---|
| 部署 | Cloudflare Worker `jianpu-web`（`wrangler.jsonc`） | GitHub Pages（`.github/workflows/pages.yml`） |
| 地址 | **https://jianpu-db.org/**（apex；`www` 同一份） | https://jianpu-db.github.io/ |
| 能力 | 检索 / 卡片 / 谱页 / **投稿 / 补属性 / 补标签** | 检索 / 卡片 / 谱页（只读，写操作把人指到域名） |

为什么不是"域名 → GitHub Pages"：那会让**写回功能全丢**（Pages 是纯静态，`JIANPU_READONLY=true`
时"投稿/补收录/补标签"只会显示"只读镜像"）—— 而这套功能是 2026-09-29~30 刚做完的。
Pages 那份继续当镜像兼后备（它页面上的提示链接现在指向 `jianpu-db.org`）。

## 二、域名现状（实测，不是听说）

`rdap.publicinterestregistry.org` 查到的权威记录：

```
registrar : Cloudflare, Inc. (IANA 1910)
注册      : 2026-09-30 06:38:30Z    到期 2027-09-30
NS        : agustin.ns.cloudflare.com / brynne.ns.cloudflare.com
```

* **注册商就是 Cloudflare** ⇒ **不用 "Add a site"、也不用换 NS**：Cloudflare Registrar 买的域名会
  **自动**作为 zone 建在同账号下。直接问它的权威 NS 已经能拿到 `jianpu-db.org` 的 SOA
  （`PrimaryServer=agustin.ns.cloudflare.com`、`NameAdministrator=dns.cloudflare.com`）✓
* 注册局（.org）的委派在刚注册那会儿还没传播到公共 DNS（`A` 也还没有 —— 正常，还没绑 Worker）。

## 三、剩下要做的（账号侧，代码里已经准备好）

```bash
cd D:\Documents_D\jianpu-db.github.io
npm install          # 一次（已跑过：34 个包，wrangler 4.138.0 可用）
npx wrangler login   # 一次，浏览器点授权  ← **只有这步必须人来做**
npx wrangler deploy  # 绑 jianpu-db.org + www.jianpu-db.org + 签证书
```

`wrangler.jsonc` 里已经写好：

```jsonc
"routes": [
  { "pattern": "jianpu-db.org",     "custom_domain": true },
  { "pattern": "www.jianpu-db.org", "custom_domain": true }
]
```

`custom_domain: true` 会**自动**建 DNS 记录 + 签 HTTPS（不需要手配 A 记录/CNAME 文件；
`www` 想 301 到 apex 就用 Cloudflare 面板的 Redirect Rules，不用改代码）。
若 `wrangler` 报"zone 找不到"：面板 **+ Add → Connect a domain** 加一次（域名已在 Cloudflare 家，
不会要求换 NS），或用 UI 绑：Workers & Pages → `jianpu-web` → Settings → Domains & Routes →
Custom domain。

## 四、代码侧已经改好的（本仓库与站点仓库）

* `wrangler.jsonc`: `routes`（apex + www，`custom_domain: true`）；
* `static/app.js`: 只读镜像里那条提示的 `MIRROR` → `https://jianpu-db.org/`（两处文案）；
* `static/index.html`: description / canonical（**指正式域名**，镜像不抢正本）/ og:* /
  twitter:summary_large_image / theme-color / 内联 SVG favicon；分享卡片图 `static/og.png`
  （1200×630，由 `tools/make_og.py` 用 `data/stats.json` 的真实数字生成，可重跑）；
* `robots.txt` + `sitemap.xml`: 由 `tools/build_web_data.py` **随语料一起生成**
  （每首歌一个 `/s/<id>` 深链；这次 11,141 条），`build_dist.mjs` 把它们拷进 dist；
* `og:image` 按"谁在服务这个页面"写 —— cf 那份是域名地址，gh 那份在构建时改成镜像自身地址
  （域名绑好之前贴镜像链接也有图，否则是无图卡片）；
* 本地服务两处 bug（自检抓到的）：`app/server.py` 的 `resolve()` 把 `/robots.txt` 当成
  `static/robots.txt` → 本地 404（线上却是好的，最难查）；同一处绕过 MIME 表 → `.txt/.xml`
  发成 `application/octet-stream`。都已修，`check_live.mjs` 增了 6 项盯着。

## 五、域名通了之后值得做的（还没做）

1. **原图走 R2**：面板开 R2 → 建桶 `jianpu-images` → 放开 `wrangler.jsonc` 里那段注释 → 传 ~5GB
   （否则 Worker 反代 `IMG_UPSTREAM`，走家里上行）；
2. **投稿真写回**：`npx wrangler secret put API_UPSTREAM` / `API_TOKEN`（指向本机 `app/server.py`）；
3. **每谱一页的分享卡**：现在 `/s/<id>` 发出去是通用卡片。要在 Worker 里按 id 注入
   `<meta og:title/og:description>` —— 需要一个小的 `id → {曲名, 歌手, 音符数}` 索引
   （`build_web_data.py` 顺手产出即可），Worker 取一次缓存在模块作用域。**没做**。
4. `www` → apex 的 301（面板一条规则）；`robots.txt`/`sitemap.xml` 已在做，后续随语料自动更新。
