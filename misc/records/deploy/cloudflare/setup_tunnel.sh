#!/usr/bin/env bash
# 建一条**固定的** Cloudflare 隧道: 把本机的查歌服务发到公网, 并挂上 Cloudflare Access 登录门。
#
#     HOSTNAME=jpt.example.com bash setup_tunnel.sh [隧道名=jianpu]
#
# 全程**不需要 sudo**（cloudflared 装在 ~/.local/bin, 服务用 systemd --user）。
# 需要你手动做一次的只有一步: 第一次跑 `cloudflared tunnel login` 时, 它会打印一个
# dash.cloudflare.com 的授权链接 —— 浏览器点一下, 选你的域名, 之后这台机器就有凭据了。
#
# 脚本是**幂等**的: 隧道已存在就复用, 配置/服务单元按当前内容重写, 最后 curl 验证一遍。
set -euo pipefail

TUNNEL="${1:-jianpu}"
: "${HOSTNAME:?用法: HOSTNAME=jpt.example.com bash setup_tunnel.sh [隧道名]}"
PORT="${PORT:-8770}"
CF="${CLOUDFLARED:-$HOME/.local/bin/cloudflared}"
CFDIR="$HOME/.cloudflared"
CFG="$CFDIR/config.yml"
UNIT="$HOME/.config/systemd/user/cloudflared.service"
HERE="$(cd "$(dirname "$0")" && pwd)"

say() { printf '\n\033[1m== %s\033[0m\n' "$*"; }
die() { printf '\n!! %s\n' "$*" >&2; exit 1; }

say "0/6 检查前置"
[ -x "$CF" ] || die "找不到 cloudflared（$CF）。
  免 sudo 安装（本机实测可行, GitHub release 资产被墙, 走 Cloudflare 自己的包站）:
    cd /tmp && curl -s https://pkg.cloudflare.com/cloudflared/dists/any/main/binary-amd64/Packages | awk -F': ' '/^Filename:/{print \$2}' | head -1
    curl -sSLo cf.deb https://pkg.cloudflare.com/cloudflared/pool/main/c/cloudflared/cloudflared_<版本>_amd64.deb
    dpkg-deb -x cf.deb cfx && cp cfx/usr/bin/cloudflared ~/.local/bin/"
"$CF" --version
code="$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/" || true)"
[ "$code" = "200" ] || die "本机 http://127.0.0.1:$PORT/ 返回 $code —— 先确认 jianpu-web.service 活着"
echo "本地服务 OK ($code)"

mkdir -p "$CFDIR" "$(dirname "$UNIT")"

if [ ! -f "$CFDIR/cert.pem" ]; then
  say "1/6 需要你授权一次（会打印一个 dash.cloudflare.com 链接, 浏览器点开选域名）"
  "$CF" tunnel login || die "授权没完成"
fi
echo "凭据: $(ls "$CFDIR"/*.pem 2>/dev/null | head -1)"

say "2/6 建隧道（已存在就复用）"
if "$CF" tunnel list 2>/dev/null | awk '{print $2}' | grep -qx "$TUNNEL"; then
  echo "隧道 $TUNNEL 已存在"
else
  "$CF" tunnel create "$TUNNEL"
fi
UUID="$("$CF" tunnel list 2>/dev/null | awk -v n="$TUNNEL" '$2==n{print $1}' | head -1)"
[ -n "$UUID" ] || die "拿不到隧道 UUID（cloudflared tunnel list 看看）"
echo "UUID = $UUID"
[ -f "$CFDIR/$UUID.json" ] || die "没有凭据文件 $CFDIR/$UUID.json"

say "3/6 写 $CFG"
if [ -f "$CFG" ] && ! grep -q "$TUNNEL" "$CFG"; then
  cp "$CFG" "$CFG.bak.$(date +%s)"; echo "（旧配置已备份）"
fi
cat > "$CFG" <<YAML
# 由 _analysis/deploy/cloudflare/setup_tunnel.sh 生成 $(date '+%F %T')
tunnel: $UUID
credentials-file: $CFDIR/$UUID.json
loglevel: info
metrics: 127.0.0.1:20241

ingress:
  - hostname: $HOSTNAME
    service: http://127.0.0.1:$PORT
    originRequest:
      connectTimeout: 30s
  - service: http_status:404
YAML
"$CF" tunnel ingress validate --config "$CFG" && echo "ingress 校验通过"

say "4/6 装 systemd 用户服务（常驻 + 开机自启）"
cp "$HERE/cloudflared.service" "$UNIT"
systemctl --user daemon-reload
systemctl --user enable --now cloudflared
sleep 3
systemctl --user --no-pager --lines=5 status cloudflared || true

say "5/6 绑域名（DNS 记录由 cloudflared 写, 需要域名在该账号下）"
"$CF" tunnel route dns "$TUNNEL" "$HOSTNAME" || echo "（可能已存在, 忽略）"

say "6/6 从公网验证"
for i in $(seq 1 10); do
  code="$(curl -s -m 15 -o /dev/null -w '%{http_code}' "https://$HOSTNAME/" || true)"
  echo "  https://$HOSTNAME/ -> $code"
  [ "$code" = "200" ] && break
  sleep 3
done
cat <<TIP

下一步（在 Cloudflare 面板点几下, 只有这一步必须在网页上做）:
  Zero Trust -> Access -> Applications -> **Create an application** -> Self-hosted
    Application name : 简谱旋律查歌
    Session Duration : 1 month（自己用, 别老登录）
    Public hostname  : $HOSTNAME   （就是上面那个）
    Policy           : Action=Allow, Include=Emails -> 你自己的邮箱（One-time PIN 登录）
  ⚠ 这个站有**写接口**（/api/submit 会 git commit 到 jianpu-db）—— 别把它裸奔在公网。
  面板上顺手关掉两个会坏事的东西: Speed -> Optimization 里的 **Rocket Loader = Off**
  （它会破坏 ES module, 页面直接白屏）、Auto Minify = Off。
TIP
