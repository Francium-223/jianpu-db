# -*- coding: utf-8 -*-
"""把 jianpu-db 导出成可上传 HuggingFace 的数据集(只读仓库, 不联网)。

产物(默认写到 hf/):
  hf/data.jsonl    一行一首; 字段见下面 COLS
  hf/README.md     dataset card(HF 要求仓库根有 README, 带 YAML front matter)
用法:
  py -3.13 export_hf.py                 # 生成
  py -3.13 export_hf.py --out some/dir  # 换目录
  py -3.13 export_hf.py --no-sections   # 不重复内联分段(体积更小)
"""
import argparse
import collections
import hashlib
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

ap = argparse.ArgumentParser()
ap.add_argument("--out", default="hf")
ap.add_argument("--no-sections", action="store_true")
args = ap.parse_args()

SRC = "scores"
SRC_RE = re.compile(r"(?m)^source=([^\s]+)\s*$")
HOST_RE = re.compile(r"^([a-z0-9]+)-")
COLS = ["file", "title", "status", "tags", "usertags", "transcriber",
        "source", "source_host", "n_notes", "sections", "score"]


def main():
    # ① source= 只在曲谱文件里(score.py 的 to_record 没带出来) -> 逐份扫
    srcmap = {}
    files = sorted(f for f in os.listdir(SRC) if f.endswith(".txt"))
    for f in files:
        try:
            t = io.open(os.path.join(SRC, f), encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        m = SRC_RE.search(t)
        srcmap[f] = m.group(1).strip() if m else ""

    # ② data.jsonl 是唯一真源(由 parse_scores.py 生成, 与 data.json 同源)
    rows, stats = [], collections.Counter()
    with io.open("data.jsonl", encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if not ln:
                continue
            r = json.loads(ln)
            f = (r.get("file") or [""])[0]
            s = srcmap.get(f, "")
            host = HOST_RE.match(s).group(1) if HOST_RE.match(s) else ""
            row = {
                "file": f,
                "title": r.get("title") or "",
                "status": r.get("status") if isinstance(r.get("status"), str) else "",
                "tags": list(r.get("tag") or []),
                "usertags": list(r.get("usertag") or []),
                "transcriber": (r.get("transcriber") or [""])[0] if isinstance(r.get("transcriber"), list) else (r.get("transcriber") or ""),
                "source": s,
                "source_host": host,
                "n_notes": int(r.get("n_notes") or 0),
            }
            if not args.no_sections:
                row["sections"] = r.get("sections") or []
            row["score"] = r.get("score") or ""
            rows.append(row)
            stats["status:" + (row["status"] or "?")] += 1
            stats["host:" + (host or "?")] += 1

    os.makedirs(args.out, exist_ok=True)
    outj = os.path.join(args.out, "data.jsonl")
    with io.open(outj, "w", encoding="utf-8", newline="\n") as g:
        for row in rows:
            g.write(json.dumps(row, ensure_ascii=False) + "\n")

    h = hashlib.sha256(open(outj, "rb").read()).hexdigest()[:16]
    print(f"写出 {len(rows)} 条 -> {outj}  ({os.path.getsize(outj)/1e6:.1f} MB, sha256[:16]={h})")
    for k, v in sorted(stats.items()):
        print(f"   {k:<22} {v}")
    print("字段:", " ".join(COLS if args.no_sections else [c for c in COLS if c != 'sections'] + ["sections"]))

    card = rf"""---
license: other
language:
- zh
pretty_name: Jianpu Melody Corpus (简谱旋律语料)
task_categories:
- text-generation
- other
tags:
- music
- symbolic-music
- jianpu
- numbered-musical-notation
- chinese
- melody
- retrieval
size_categories:
- 1K<n<10K
configs:
- config_name: default
  data_files: data.jsonl
---

# 简谱旋律语料 / Jianpu Melody Corpus

中文**简谱(jianpu)**旋律语料: {len(rows)} 首, 一行一首。每一首是**逐音符的简谱 token 序列**,
按 jianpu-ly 的记法编码, 可直接做检索 / 训练 / 对齐。

## 字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `file` | str | 源文件名(仓库 `scores/` 下) |
| `title` | str | 曲名 |
| `status` | str | `ok`=人工校对过; `ocr`=由图片机器转写; `midi`=MIDI 硬转(本数据集不含) |
| `tags` | list[str] | 标签(tag = 由 usertag 依标签图推出的闭包) |
| `usertags` | list[str] | 人写的原始标签(叶子) |
| `transcriber` | str | 转写者 |
| `source` | str | 出处(如 `qupu123-268596`, 站点-站内 id) |
| `source_host` | str | 出处站点(qupu123 / jianpucn / jianpujia …) |
| `n_notes` | int | 音符数(不含 `-`/`~`/`|`) |
| `sections` | list[dict] | 分段: `{{"subtitle": "chorus", "score": "..."}}` |
| `score` | str | 全文旋律(各段用 ` \| ` 连接) |

## token 记法

* 音高: `1`–`7`; `,` 低八度(`,6`), `'` 高八度(`'1`), 可叠(`''1`)
* 时值前缀: `q`=八分 `s`=十六分 `d`=三十二分 `h`=六十四分; **无前缀 = 四分**
* `.` 附点, `-` 延长一拍, `0` 休止, `x` 念白, `~` 连音线, `3[ … ]` 三连音

## 出处与许可

* 曲谱均来自公开曲谱站(中国曲谱网 qupu123 / 歌谱简谱网 jianpu.cn / 简谱之家 jianpujia),
  `source` 字段逐首标注站内 id, 便于回溯。
* 本站只是**旋律记谱**(不含歌词), 用于检索与研究; 版权归原词曲作者所有, 请勿商用。

## 生成方式

`data.jsonl` 由仓库 CI 每次 push 后自动重建(`parse_scores.py`), 本卡与上表同步。
"""
    with io.open(os.path.join(args.out, "README.md"), "w", encoding="utf-8", newline="\n") as g:
        g.write(card)
    print(f"写出 {args.out}/README.md (dataset card)")


if __name__ == "__main__":
    main()
