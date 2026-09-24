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
COLS = ["file", "title", "artist", "status", "tags", "usertags", "transcriber",
        "source", "source_host", "n_notes", "sections", "score", "link"]

# 简谱 token 口径的**唯一实现**在 skill 目录的 jptok.py(与 score.py 用同一份)。
# 导出的 dataset card 要报"音符总数", 必须用它数, 不许在这里再写一份正则。
_JT = os.environ.get("JIANPU_JTOK") or os.path.join(
    os.path.dirname(ROOT), "jianpu2", "skills", "jianpu-melody-lookup")
if os.path.isdir(_JT):
    sys.path.insert(0, _JT)
try:
    import jptok
except Exception as e:                       # pragma: no cover
    # CI(GitHub runner)只 checkout 了本仓库, 兄弟目录 jianpu2/ 不在 -> 找不到 jptok 是**常态**。
    # 显式设了 JIANPU_ALLOW_FALLBACK_JTOK=1 时, 用 score.py 里的兜底口径(与 jptok 已被
    # check_jptok_parity.py 拿全语料 7,237,223 个 token 证明逐项一致), 而不是让 workflow 挂掉。
    if os.environ.get("JIANPU_ALLOW_FALLBACK_JTOK") != "1":
        sys.exit(f"找不到 jptok.py(设 JIANPU_JTOK 指一下, 或 JIANPU_ALLOW_FALLBACK_JTOK=1 用兜底): {e}")
    import warnings
    warnings.warn(f"jptok 未找到({e}), 按 JIANPU_ALLOW_FALLBACK_JTOK=1 用 score.py 的兜底口径数音符")
    import score                             # 同目录; 它会自己决定用 jptok 还是兜底
    jptok = score.jptok


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
    n_pitch_notes = 0
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
                "artist": list(r.get("artist") or []),        # 歌手(独立字段, 2026-09-24)
                "usertags": list(r.get("usertag") or []),
                "transcriber": (r.get("transcriber") or [""])[0] if isinstance(r.get("transcriber"), list) else (r.get("transcriber") or ""),
                "source": s,
                "source_host": host,
                "n_notes": int(r.get("n_notes") or 0),
                # ⚠ 这里是**第三处**逐字段白名单(另两处: score.py:to_record、前端 search.js)。
                #   加新字段时三处都要加, 否则"仓库里有、导出/前端没有"(实测 mbid/link 都踩过)。
                "link": list(r.get("link") or []),
            }
            if not args.no_sections:
                row["sections"] = r.get("sections") or []
            row["score"] = r.get("score") or ""
            rows.append(row)
            stats["status:" + (row["status"] or "?")] += 1
            stats["host:" + (host or "?")] += 1
            n_pitch_notes += len(jptok.seq(row["score"]))   # 不含休止/念白, 与检索口径一致

    os.makedirs(args.out, exist_ok=True)
    outj = os.path.join(args.out, "data.jsonl")
    with io.open(outj, "w", encoding="utf-8", newline="\n") as g:
        for row in rows:
            g.write(json.dumps(row, ensure_ascii=False) + "\n")

    # 把 skill(查询脚本 + 说明)**一起放进数据集仓库**: skill 目录里不放 data.jsonl,
    # lookup.py 会自动往上一层找(HF 仓库根目录就有), 所以不产生第二份 10MB。
    import shutil
    skill_src = os.path.join(ROOT, "skill", "jianpu-melody-lookup")
    if os.path.isdir(skill_src):
        dst = os.path.join(args.out, "skill", "jianpu-melody-lookup")
        os.makedirs(dst, exist_ok=True)
        for name in sorted(os.listdir(skill_src)):
            sp = os.path.join(skill_src, name)
            if os.path.isfile(sp) and not name.endswith((".pyc",)):
                shutil.copyfile(sp, os.path.join(dst, name))
        print(f"一并放入 skill: {sorted(os.listdir(dst))}")

    h = hashlib.sha256(open(outj, "rb").read()).hexdigest()[:16]
    print(f"写出 {len(rows)} 条 -> {outj}  ({os.path.getsize(outj)/1e6:.1f} MB, sha256[:16]={h})")
    for k, v in sorted(stats.items()):
        print(f"   {k:<22} {v}")
    print("字段:", " ".join(COLS if args.no_sections else [c for c in COLS if c != 'sections'] + ["sections"]))

    card = rf"""---
license: other
pretty_name: Jianpu Melody Corpus (简谱旋律语料)
tags:
- music
- symbolic-music
- jianpu
- numbered-musical-notation
- melody
- retrieval
size_categories:
- 1K<n<10K
configs:
- config_name: default
  data_files: data.jsonl
---

# 简谱旋律语料 / Jianpu Melody Corpus

**简谱(jianpu)**旋律语料: {len(rows)} 首, 一行一首。每一首是**逐音符的旋律序列**,
按 jianpu-ly 的记法编码, 可直接做检索 / 训练 / 对齐。

## 口径声明

* 这是**旋律数据集**: 内容是音高 + 时值的符号序列, 没有歌词, 也不带语言标注
  —— 同一段 `5 6 5 3 2 1` 与它是哪首歌、用哪种语言唱无关。
* 曲名只是**检索用的元数据**, 它可能是中文、英文或日文; 这不影响 `score` 字段的内容。

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
| `link` | list[str] | 这首歌在某一站的**收录页**(人工核对过, 可多个)。只收具体页面 —— 搜索页不进数据; 原谱站那一页可由 `source` 的站点+id 推出(仓库 `source_pages.json`, 逐条抓取核对过) |
| `n_notes` | int | 音符数(不含 `-`/`~`/`|`) |
| `sections` | list[dict] | 分段: `{{"subtitle": "chorus", "score": "..."}}` |
| `score` | str | 全文旋律(各段用 ` \| ` 连接) |

### 筛选示例

```python
from datasets import load_dataset
d = load_dataset("<你的账号>/chinese-jianpu-corpus", split="train")
d.filter(lambda x: x["status"] == "ok")                    # 只看人工校对过的
d.filter(lambda x: x["source_host"] == "qupu123")          # 只看某一个来源站
d.filter(lambda x: 50 <= x["n_notes"] <= 200)              # 按长度切
d.filter(lambda x: "分类/儿歌" in x["tags"])               # 按标签切
```

## 配套 AI Skill: 旋律查歌

`skill/jianpu-melody-lookup/` 是一个**开箱即用的查询技能**: 给一段旋律(简谱唱名数字串),
在全部 {len(rows)} 首里找出它最可能是哪首歌。纯离线, 只依赖本仓库的 `data.jsonl` + numpy。

```bash
python skill/jianpu-melody-lookup/lookup.py "5 5 5 3 2 2 3 5 3 2 1 1 6 1 2 6 5 5"
#   #   错音   八度差  曲名            状态   出处
#   1    0     0  上春山           ocr  qinyipu-377784
```

实测指标(华流金曲清单 319 首中库里可定位的 262 首, 每首截一段片段查询, 按曲名判定):

| 片段长度 | 哼错音 | Top-1 | Top-3 | Top-5 |
|---|---|---|---|---|
| 11 音 | 0 | **94.4%** | 98.8% | 99.4% |
| 11 音 | 1 | 69.4% | 88.8% | 93.1% |
| 15 音 | 0 | **98.1%** | 100% | 100% |
| 15 音 | 1 | 97.5% | 100% | 100% |

更严口径(留一版本: 查询所用的那份谱从索引排除, 只能靠同一首歌的另一个版本命中, 模拟"没有原谱、
纯凭记忆"): 11 音 Top-1 **41.2%** / 15 音 **48.8%**。两个口径的落差说明**瓶颈是"片段是否独特",
不是匹配算法** —— 所以并列时请补长片段, 或多给几段(`lookup.py 片段1 片段2`)。

## token 记法

* 音高: `1`–`7`; `,` 低八度(`,6`), `'` 高八度(`'1`), 可叠(`''1`)
* 时值前缀: `q`=八分 `s`=十六分 `d`=三十二分 `h`=六十四分; **无前缀 = 四分**
* `.` 附点, `-` 延长一拍, `0` 休止, `x` 念白, `~` 连音线, `3[ … ]` 三连音

例(《东方红》开头): `5 5 6 2 | 1 1 6 2 | 5 5 6 1 6 5 | 1 1 6 2`

## 为什么这个数据集稀缺

五线谱有通用的机器可读格式(MusicXML / MEI / ABC / MIDI), **简谱没有**——
简谱在网上的存在形式基本就是**图片**: 排版工具有(jianpu-ly 等), 但交换格式没有。
所以这不是"又一份乐谱文本", 而是**把"只有图片的简谱"转成 token 序列**:
`score` 字段就是那套逐音符记法, `source` 字段逐首保留原图出处, 可回溯核对。

## 出处与许可

* 曲谱均来自公开曲谱站(中国曲谱网 qupu123 / 歌谱简谱网 jianpu.cn / 简谱之家 jianpujia),
  `source` 字段逐首标注站内 id, 便于回溯。
* 本站只是**旋律记谱**(不含歌词), 用于检索与研究; 版权归原词曲作者所有, 请勿商用。

## 数据构成(实测)

* `status`: `ocr` {stats.get('status:ocr', 0)} 首(由图片机器转写) / `ok` {stats.get('status:ok', 0)} 首(人工校对过)
* `source_host`: qupu123 {stats.get('host:qupu123', 0)} / jianpucn {stats.get('host:jianpucn', 0)} / jianpujia {stats.get('host:jianpujia', 0)} / 其它 {sum(v for k, v in stats.items() if k.startswith('host:') and k.split(':')[1] not in ('qupu123', 'jianpucn', 'jianpujia', '?'))} / 未记录 {stats.get('host:?', 0)}
* 音符总数: {n_pitch_notes:,}(不含休止/念白; 由 `jptok.seq` 统计)

> ⚠ 这三行以前是**硬编码**的(写着 `ocr 7295` / `1,422,852`), 数据涨了卡片还不动 ——
> 现在改成从本次导出的数据现算, 数字与 `data.jsonl` 永远一致。

## 生成方式

`data.jsonl` 由仓库 CI 每次 push 后自动重建(`parse_scores.py` 重生成 `data.json`/`data.jsonl`,
`export_hf.py` 转出本卡与本文件), 数字与上表同步。
"""
    with io.open(os.path.join(args.out, "README.md"), "w", encoding="utf-8", newline="\n") as g:
        g.write(card)
    print(f"写出 {args.out}/README.md (dataset card)")


if __name__ == "__main__":
    main()
