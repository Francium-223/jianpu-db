# 本机"写"服务：能不能给公网访问 + 能不能打包搬走（2026-09-30 实测）

> 用户问："本机有公网地址吗？这个 server 可不可以做个开箱即用的包，迁移到别的电脑上？"

## 一、公网可达性：**没有可用的入向公网地址，走隧道**

本机实测（2026-09-30）：

| 查什么 | 结果 |
|---|---|
| 出口 IPv4 | `222.206.18.205`（另一次 `223.80.110.109`，运营商出口会变） |
| 本机地址 | `192.168.11.1` / `192.168.50.1` / `172.25.131.255`（都在内网段，且**本机自己还在做别的网段的网关**） |
| 服务监听 | `127.0.0.1:8770` —— **只收本机连接**（这是故意的：它能写盘 + git commit） |
| `cloudflared` | **已装**：`C:\Program Files (x86)\cloudflared\cloudflared.exe`（2026.9.3） |

结论：出口 IP 看着像公网，但那**不等于能从外网进来** —— 家用宽带普遍封 80/443 入向，
路由器还要做端口映射，而且出口 IP 会变（没有固定公网地址）。**正解是打隧道**（出向连接，
不需要公网 IP、不需要端口映射、自带 HTTPS）：

```bash
cloudflared tunnel --url http://127.0.0.1:8770        # 临时地址, 先试通
# 稳定版: 命名隧道 + 子域 api.jianpu-db.org（域名已在 Cloudflare, 加一条 CNAME 即可）
```

然后把地址交给边缘 Worker（在站点仓库里）：

```bash
npx wrangler secret put API_UPSTREAM     # 隧道地址
npx wrangler secret put API_TOKEN        # 与本机 JPSUBMIT_TOKEN 同值（**必须**，否则等于把写接口挂公网）
```

验证：`curl -s https://jianpu-db.org/api/health` 应显示 `"api":true`。

## 二、开箱即用的便携包：**做好了，并且实测过**

工具：站点仓库 `tools/make_server_bundle.py` → 产出 `jianpu-server/`（约 6.5 MB，`--zip` 给压缩包）。

```
jianpu-server/
  app/server.py  app/jptok.py     服务本体 + token 口径（**只用标准库, 不需要 pip**）
  static/…  data/…  robots.txt  sitemap.xml
  setup.cmd|sh                    首次运行: 稀疏 clone 语料（实测 86 MB）
  run.cmd  |sh                    起服务（自带 JIANPU_DB/JIANPU_PORT）
  README.md  VERSION(web=… db=…)
```

为什么语料不塞进包：`jianpu-db` 仓库 176 MB（`.git` 75 MB），其中 `by_*` 那几棵链接树对服务毫无用处。
首次运行用稀疏 clone（`--depth 1 --filter=blob:none --sparse` + `sparse-checkout set scores`）
拿到的正是"根目录那几个 py/json + `scores/`"。要完全离线就 `--corpus copy`。

**模拟另一台电脑的实测**（换目录、另起端口 8790）：

* 首次运行脚本 → 语料 86 MB 到位（11,637 份 `scores` + `linkurl.py`/`schema.py`/`tags.json`/`source_pages.json`）；
* 读路径全 200：`/`、`/s/<id>`（`<title>` 是**这一首**）、`robots.txt`、`sitemap.xml`、`og.png`、`og.json`、`stats.json`；
* **写路径真跑通**：`POST /api/submit {kind:'tags',file:'101.txt',tags:['测试/便携包']}` →
  `{"ok":true,"state":"已写入","committed":true}`；包内 clone 的 `101.txt` 写入 `usertag=测试/便携包`、
  clone 里多出提交 `tags: 101.txt —— 人工补标签(测试/便携包)`、`feedback/20260930-170914-tags-101.json` 留档；
* **主仓库 `git status` 干净**（写的是包里那份 clone，没碰真库）；
* `refresh` 优雅降级（便携包不带重建流水线，只提示"没有 tools/refresh.sh 也没有 tools/refresh.py"）。

打好的包：`D:\Documents_D\jianpu-server\` 与 `D:\Documents_D\jianpu-server.zip`（5.3 MB）。
