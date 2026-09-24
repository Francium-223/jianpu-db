#!/usr/bin/env bash
# 临时公网地址（**不用账号、不用域名**, 2 秒出 URL）—— 只适合自己看一眼/给朋友试。
# ⚠ 这个地址是**公开**的, 而且本服务有写接口(投稿会 git commit) —— 用完 Ctrl-C 关掉。
#   正式发布请用 setup_tunnel.sh（固定域名 + Cloudflare Access 登录门）。
set -euo pipefail
PORT="${1:-8770}"
CF="${CLOUDFLARED:-$HOME/.local/bin/cloudflared}"
[ -x "$CF" ] || { echo "没装 cloudflared：见 README.md 的安装段"; exit 1; }
echo "本地服务: $(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/" || echo 连不上) (期望 200)"
echo "马上会打印一个 https://xxx.trycloudflare.com —— Ctrl-C 结束"
exec "$CF" tunnel --no-autoupdate --url "http://127.0.0.1:$PORT"
