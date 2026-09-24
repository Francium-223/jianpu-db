#!/usr/bin/env bash
# 把三个库推到 GitHub —— 这是那位夜里唯一没法替你做的事(要凭据)。
# 醒来只要跑一条:
#
#     bash _analysis/推送.sh --check      # ① 先体检(不联网、不改任何东西)
#     bash _analysis/推送.sh              # ② 真推(用你现有的 gh 登录 / 凭据 helper)
#     GITHUB_TOKEN=ghp_xxx bash _analysis/推送.sh    # ②' 没有 gh 时用 PAT(不会写进 .git/config)
#
# 三个库与目标:
#   jianpu-db   -> Francium-223/jianpu-db   (已跟踪, 领先 15)
#   jianpu2     -> origin = Francium-223/jianpu2   ← 远端可能还不存在, 见下面提示
#   jianpu-web  -> origin = Francium-223/jianpu-web ← 同上
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPOS="jianpu-db jianpu2 jianpu-web"
MODE="${1:-push}"
FAIL=0

hr() { printf '%s\n' "------------------------------------------------------------"; }

echo "== 推送前体检 ($(date '+%F %T')) =="
for r in $REPOS; do
  hr; echo "### $r"
  d="$ROOT/$r"
  [ -d "$d/.git" ] || { echo "  !! 不是 git 仓库: $d"; FAIL=1; continue; }
  dirty="$(git -C "$d" status --porcelain | wc -l)"
  echo "  工作区: $([ "$dirty" = 0 ] && echo 干净 || echo "有 $dirty 处未提交改动")"
  git -C "$d" log --oneline -1 | sed 's/^/  最新提交: /'
  for line in $(git -C "$d" remote); do
    url="$(git -C "$d" remote get-url "$line")"
    echo "  远端 $line: $url"
  done
  git -C "$d" count-objects -vH | grep -E 'size-pack|^size:' | sed 's/^/  /'
  # 已提交的对象里有没有 >100MB 的(会撞 GitHub 硬限)
  big="$(git -C "$d" rev-list --objects --all 2>/dev/null \
        | git -C "$d" cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' 2>/dev/null \
        | awk '$1=="blob" && $3>104857600 {printf "%.1fMB %s\n", $3/1048576, $4}' | head -3)"
  if [ -n "$big" ]; then echo "  !! 有 >100MB 的文件, GitHub 会拒收:"; echo "$big" | sed 's/^/     /'; FAIL=1
  else echo "  没有 >100MB 的文件 ✓"; fi
done

hr
echo "=== 远端仓库是否存在(需要联网/凭据; 失败不代表有问题) ==="
if command -v gh >/dev/null 2>&1; then
  echo "  有 gh: $(gh --version 2>/dev/null | head -1)"
  gh auth status 2>&1 | sed 's/^/  /' | head -6
else
  echo "  没装 gh(可选: sudo apt install gh && gh auth login)"
fi
for r in jianpu2 jianpu-web; do
  u="$(git -C "$ROOT/$r" remote get-url origin 2>/dev/null || true)"
  echo -n "  $u : "
  if GIT_TERMINAL_PROMPT=0 git ls-remote --exit-code "$u" >/dev/null 2>&1; then echo "存在且可读"
  else echo "读不到(不存在 / 私有 / 要凭据) —— 若确实不存在, 先建空仓库再推"; fi
done

if [ "$MODE" = "--check" ]; then
  hr; echo "体检完(没有推送任何东西)。真推: bash _analysis/推送.sh"
  exit $FAIL
fi

# ---- 真推 ----
# 有 token 就用一个**临时** credential helper, 不落盘、不写进 .git/config
TOKEN="${GITHUB_TOKEN:-${GH_TOKEN:-}}"
# 没设环境变量时, 看这两个文件(放一次就够, 不进 shell 历史、不进 .git/config):
#   ~/.config/jianpu/github_token   或   <工作区>/_analysis/.github_token
for f in "${JIANPU_TOKEN_FILE:-}" "$HOME/.config/jianpu/github_token" "$ROOT/_analysis/.github_token"; do
  [ -n "$f" ] && [ -z "$TOKEN" ] && [ -f "$f" ] && TOKEN="$(tr -d '\r\n' < "$f")"
done
[ -n "$TOKEN" ] && echo "  读到 token(来源: 环境变量或 token 文件; 长度 ${#TOKEN})"
CRED=()
if [ -n "$TOKEN" ]; then
  echo; echo "== 用环境变量里的 token 推(不写进 .git/config) =="
  CRED=(-c "credential.helper=!f() { echo username=x-access-token; echo password=$TOKEN; }; f")
else
  echo; echo "== 用系统里已有的凭据(gh 登录 / credential.helper)推 =="
fi

# 有 token 的话, 先把"远端还不存在"的仓库建出来(空仓库, 不初始化 README)
if [ -n "$TOKEN" ]; then
  hr; echo "=== 检查/创建远端仓库 ==="
  for r in $REPOS; do
    u="$(git -C "$ROOT/$r" remote get-url origin 2>/dev/null || git -C "$ROOT/$r" remote get-url "$(git -C "$ROOT/$r" remote | head -1)" 2>/dev/null)"
    name="$(basename "$u" .git)"
    if GIT_TERMINAL_PROMPT=0 git ls-remote --exit-code "$u" >/dev/null 2>&1; then
      echo "  $name: 已存在"
    else
      printf "  %s: 不存在 -> 建空仓库 ... " "$name"
      code="$(curl -s -o /tmp/_mk.json -w '%{http_code}' -X POST \
        -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
        https://api.github.com/user/repos \
        -d "{\"name\":\"$name\",\"private\":true,\"description\":\"简谱语料/工具链(DSH 推送)\"}")"
      if [ "$code" = "201" ]; then echo "建好了 ✓"; else echo "失败(HTTP $code): $(head -c 200 /tmp/_mk.json)"; FAIL=1; fi
    fi
  done
fi

for r in $REPOS; do
  hr; echo "### 推 $r"
  d="$ROOT/$r"
  git -C "$d" remote | grep -q . || { echo "  !! 没有远端, 跳过"; FAIL=1; continue; }
  # jianpu-db 的远端叫 Francium-223; jianpu2/jianpu-web 叫 origin
  rem="$(git -C "$d" remote | head -1)"
  if git -C "$d" rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
    echo "  -> git push ${rem} $(git -C "$d" rev-parse --abbrev-ref HEAD)"
    git -C "$d" "${CRED[@]}" push "$rem" || FAIL=1
  else
    echo "  -> git push -u ${rem} $(git -C "$d" rev-parse --abbrev-ref HEAD)  (首次, 建立跟踪)"
    git -C "$d" "${CRED[@]}" push -u "$rem" "$(git -C "$d" rev-parse --abbrev-ref HEAD)" || FAIL=1
  fi
done

hr
if [ "$FAIL" = 0 ]; then
  echo "三个库都推出去了 ✓"
else
  cat <<'EOF'
有失败。常见原因与做法:
  * 远端仓库还不存在 -> 先建空仓库(不要勾 README), 然后重跑本脚本:
        gh repo create Francium-223/jianpu2   --private --source=. --remote=origin --push
        gh repo create Francium-223/jianpu-web --private --source=. --remote=origin --push
    或手工在网页上建好后:  git push -u origin master
  * 要凭据 -> 任选一种:
        gh auth login                                   # 最省事
        GITHUB_TOKEN=ghp_xxx bash _analysis/推送.sh      # PAT(只在本进程里用, 不落盘)
        git config --global credential.helper store      # 之后手输一次 PAT
EOF
fi
exit $FAIL
