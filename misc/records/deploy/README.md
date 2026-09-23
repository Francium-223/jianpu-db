# 部署（systemd --user）—— 换机器照这个来

`jianpu-web.service` 与 `jianpu-web.service.d/restart.conf` 是**线上跑的那份原件**的副本
（原件在 `~/.config/systemd/user/`，不在任何仓库里，所以在这里留一份版本化的）。

## 装到新机器

```bash
mkdir -p ~/.config/systemd/user/jianpu-web.service.d
cp jianpu-web.service        ~/.config/systemd/user/
cp jianpu-web.service.d/restart.conf ~/.config/systemd/user/jianpu-web.service.d/
# **改路径**: 单元里的 WorkingDirectory / Environment=JIANPU_DB 要指向你的仓库位置
systemctl --user daemon-reload
systemctl --user enable --now jianpu-web.service     # 开机/登录自启
loginctl enable-linger "$USER"                       # 没登录会话也活着(不然退出登录就被停)
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8770/
```

## 2026-09-24 实测过的三件事

| 项 | 结果 |
|---|---|
| 端口/环境 | `127.0.0.1:8770`，`WorkingDirectory=…/jianpu-web`，`JIANPU_DB=…/jianpu-db`；`Cache-Control: no-cache`（改了静态文件刷新即生效） |
| **开机自启** | `is-enabled` = `enabled` ✓ |
| **没登录会话也活着** | `loginctl enable-linger caesium-132` 已开，`Linger=yes` ✓（**原来没开** —— 记录里"常驻"的说法当时是虚的） |
| **崩了会自动拉起** | 加了 `Restart=always` + `RestartSec=3`（drop-in）；实测 `kill -9` 主进程 → **5 秒内自动起来**、`GET /` 回到 200 ✓ |

## 常用操作

```bash
systemctl --user status jianpu-web.service
systemctl --user restart jianpu-web.service      # 改完后端代码后要重启(Python 不会热加载)
journalctl --user -u jianpu-web.service -n 50    # 日志
```

> 前端（`jianpu-web/static/*`）是直接读文件 + `no-cache`，**不用重启**、刷新页面即可；
> 后端（`app/server.py`）改了必须 `restart`。
