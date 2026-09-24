#!/usr/bin/env bash
# 把语料传成 HuggingFace 数据集 —— 与推送 GitHub 一样, 只差你的令牌。
#
#     bash _analysis/上传HF.sh --check        # ① 只体检: 重新导出 + 核对数字(不联网)
#     HF_TOKEN=hf_xxx bash _analysis/上传HF.sh  # ② 真上传
#
# 目标仓库: Caesium-132/chinese-jianpu-corpus (dataset)
# 产物:     jianpu-db/hf/{data.jsonl, README.md, skill/}
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DB="$ROOT/jianpu-db"
HF_DIR="$DB/hf"
REPO="${HF_REPO:-Caesium-132/chinese-jianpu-corpus}"
MODE="${1:-upload}"
FAIL=0
hr() { printf '%s\n' "------------------------------------------------------------"; }

hr; echo "=== ① 重新导出(用仓库里那份 jptok, 保证口径唯一) ==="
( cd "$DB" && python3 export_hf.py ) | tail -6 || FAIL=1

hr; echo "=== ② 核对 ==="
songs_scores=$(find "$DB/scores" -maxdepth 1 -name '*.txt' | wc -l)
songs_jsonl=$(wc -l < "$HF_DIR/data.jsonl")
songs_corpus=$(python3 -c "import io;print(sum(1 for _ in io.open('$DB/data.jsonl',encoding='utf-8')))")
echo "  scores/*.txt : $songs_scores"
echo "  data.jsonl   : $songs_jsonl"
echo "  语料 data.jsonl: $songs_corpus"
[ "$songs_jsonl" = "$songs_corpus" ] && echo "  行数与语料一致 ✓" || { echo "  !! 行数对不上"; FAIL=1; }
du -sh "$HF_DIR" | sed 's/^/  体积: /'
big=$(find "$HF_DIR" -type f -size +100M | head -3)
[ -z "$big" ] && echo "  没有 >100MB 的文件 ✓" || { echo "  !! 有大文件: $big"; FAIL=1; }
grep -m1 '音符总数' "$HF_DIR/README.md" | sed 's/^/  卡片: /'

if [ "$MODE" = "--check" ]; then
  hr; echo "体检完(没有联网)。真上传: HF_TOKEN=hf_xxx bash _analysis/上传HF.sh"
  exit $FAIL
fi

hr; echo "=== ③ 上传到 $REPO ==="
TOKEN="${HF_TOKEN:-${HUGGINGFACE_TOKEN:-}}"
for f in "${JIANPU_HF_TOKEN_FILE:-}" "$HOME/.config/jianpu/hf_token" "$ROOT/_analysis/.hf_token"; do
  [ -n "$f" ] && [ -z "$TOKEN" ] && [ -f "$f" ] && TOKEN="$(tr -d '\r\n' < "$f")"
done
# 优先用工作区里的独立 venv(系统 Python 被 PEP 668 锁着, 装不了包):
if [ -x "$ROOT/.venv-hf/bin/huggingface-cli" ]; then
  CLI="$ROOT/.venv-hf/bin/huggingface-cli"
elif [ -x "$ROOT/.venv-hf/bin/hf" ]; then
  CLI="$ROOT/.venv-hf/bin/hf"
elif command -v huggingface-cli >/dev/null 2>&1; then
  CLI=huggingface-cli
elif command -v hf >/dev/null 2>&1; then
  CLI=hf
else
  CLI=""
fi
if [ -z "$TOKEN" ]; then
  echo "!! 没有 HF_TOKEN。二选一:"
  echo "     HF_TOKEN=hf_xxx bash _analysis/上传HF.sh"
  echo "     huggingface-cli login     # 登录一次, 之后直接跑本脚本"
  exit 1
fi
if [ -z "$CLI" ]; then
  echo "!! 没装上传工具。已经给你备好一个独立 venv, 装上即可(不动系统 Python):"
  echo "     python3 -m venv $ROOT/.venv-hf && $ROOT/.venv-hf/bin/pip install -U huggingface_hub"
  echo "   (装完再跑本脚本; 也可直接用网页版拖 hf/ 里的文件)"
  exit 1
fi
"$CLI" upload "$REPO" "$HF_DIR" . --repo-type dataset \
  --commit-message "语料更新: $(date '+%F') $(python3 -c "import io;print(sum(1 for _ in io.open('$DB/data.jsonl',encoding='utf-8')))") 首" \
  || FAIL=1

hr
[ "$FAIL" = 0 ] && echo "上传完成 -> https://huggingface.co/datasets/$REPO" || echo "上传有失败, 见上面输出"
exit $FAIL
