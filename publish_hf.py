# -*- coding: utf-8 -*-
"""把 hf/ 里的数据集推到 HuggingFace(需要 token)。

用法:
  py -3.13 publish_hf.py USER/jianpu-db --dry-run     # 不联网也能跑, 先看要传什么
  py -3.13 publish_hf.py USER/jianpu-db --check       # 只验证 token + 目标仓库
  py -3.13 publish_hf.py USER/jianpu-db               # 建仓 + 上传

token 来源(按优先级): --token 参数 / 环境变量 HF_TOKEN / 已登录的 ~/.cache/huggingface/token
  * 没装 huggingface-cli 也行: 直接在 PowerShell 里 `$env:HF_TOKEN="hf_xxx"` 再跑本脚本。
  * **别把 token 写进仓库或贴到聊天里。**
"""
import argparse
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

ap = argparse.ArgumentParser()
ap.add_argument("repo_id", nargs="?", default="Caesium-132/jianpu-db",
                help="如 Caesium-132/jianpu-db (默认值; 也可用环境变量 HF_REPO)")
ap.add_argument("--folder", default="hf")
ap.add_argument("--token", default="")
ap.add_argument("--dry-run", action="store_true", help="只列文件与行数, 不联网")
ap.add_argument("--check", action="store_true", help="验证 token 与目标仓库")
ap.add_argument("--private", action="store_true")
args = ap.parse_args()
# 环境变量兜底: CI 里用 GitHub 仓库变量 HF_REPO 传, 本地也能设一把
if not args.repo_id or args.repo_id.startswith("-"):
    args.repo_id = "Caesium-132/jianpu-db"
args.repo_id = os.environ.get("HF_REPO") or args.repo_id

files = []
for name in sorted(os.listdir(args.folder)):
    p = os.path.join(args.folder, name)
    if os.path.isfile(p):
        files.append((name, os.path.getsize(p)))
j = os.path.join(args.folder, "data.jsonl")
n = sum(1 for _ in io.open(j, encoding="utf-8")) if os.path.exists(j) else 0
print(f"目标仓库: {args.repo_id} (dataset)")
print(f"待上传 {len(files)} 个文件, data.jsonl {n} 条:")
for name, size in files:
    print(f"   {name:<14} {size/1e6:>7.2f} MB")

if args.dry_run:
    print("\n(dry-run: 没有联网, 也没有做任何写入)")
    sys.exit(0)

try:
    from huggingface_hub import HfApi, create_repo, upload_folder
except Exception as ex:
    print(f"需要 huggingface_hub: {type(ex).__name__} {ex}")
    sys.exit(2)

token = args.token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN") or None
api = HfApi(token=token)
try:
    who = api.whoami()
    print(f"\n已认证: {who.get('name')}  (token 来源: {'参数' if args.token else '环境变量' if token else '本地已登录'})")
except Exception as ex:
    print(f"\n认证失败: {type(ex).__name__} {str(ex)[:200]}")
    print("  -> 403 'suspicious activity' 是 HF 对**出口 IP** 的风控; 关掉 VPN 直连再试, 或等 30 分钟。")
    sys.exit(3)

if args.check:
    try:
        info = api.repo_info(args.repo_id, repo_type="dataset")
        print(f"目标仓库已存在: {info.id}  私有={info.private}  最后修改={info.lastModified}")
    except Exception as ex:
        print(f"目标仓库还不存在(首次发布会自动创建): {type(ex).__name__}")
    sys.exit(0)

url = create_repo(args.repo_id, repo_type="dataset", private=args.private,
                  exist_ok=True, token=token)
print(f"仓库就绪: {url}")
commit = upload_folder(folder_path=args.folder, repo_id=args.repo_id, repo_type="dataset",
                       commit_message=f"upload {n} scores (data.jsonl + card)", token=token)
print(f"上传完成: {commit}")
print(f"数据集页: https://huggingface.co/datasets/{args.repo_id}")
print(f"本地一行验收: py -3.13 -c \"from datasets import load_dataset; d=load_dataset('{args.repo_id}', split='train'); print(len(d))\"")
