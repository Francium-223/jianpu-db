# -*- coding: utf-8 -*-
"""`data.jsonl` 的产物断言 —— **给 CI 用的, 不依赖 jianpu2 / jptok**。

为什么必须有: `.github/workflows/parse.yaml` 每次 push 都跑 `python parse_scores.py` 并以
`github-actions[bot]` 提交回来, 而 runner 里**只有本仓库** —— `score.py` 找不到兄弟仓库的
`jptok.py`, 于是走内置兜底 `_FallbackJptok`。2026-09-28 的真实事故:
    · 本地修好了 `jptok.recover_bars` 的"重复小节线"(3044 首), 推了数据;
    · CI 用**还没同步**的兜底口径重建 -> 把这 3044 首的重复线**又改了回去**并提交;
    · 结果远端比我发布给前端的索引多了一批重复小节线, 两边不一致。
那两个口径本来有 `jianpu2/tools/check_jptok_parity.py` 锁着 —— 但**那道锁不在 CI 里跑**,
所以漂了也没人喊。这个脚本就是放在 CI 里、不依赖兄弟仓库的那道最低防线:
重建完**先断言, 再提交**。口径漂了就让 workflow 红, 而不是静默改写 3000 首。

判据(全部只用本仓库 + 标准库):
  1. `bars` **严格递增**(相邻重复 = 空小节; 前端会画出一条没有音符的线)
  2. `bars` 的每个值都在 `0..n_notes` 之间
  3. `sections` 拼起来 == `score`(逐字节)
  4. `file` 在 `scores/` 里真的存在、且不重复
  5. `title` 非空; `status` 在白名单 {ok, ocr} 内
  6. 行数 >= 7000(整库缩水比个别行坏更严重)
只读, 不改任何东西。退出码 0 = 通过。
"""
import collections
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.dirname(HERE)
DATA = os.path.join(DB, "data.jsonl")
SCORES = os.path.join(DB, "scores")
MIN_ROWS = 7000


def main():
    bad = collections.Counter()
    ex = collections.defaultdict(list)

    def fail(kind, detail):
        bad[kind] += 1
        if len(ex[kind]) < 4:
            ex[kind].append(detail)

    rows = 0
    seen = set()
    for ln in io.open(DATA, encoding="utf-8"):
        if not ln.strip():
            continue
        rows += 1
        r = json.loads(ln)
        f = (r.get("file") or [""])[0]
        if not f:
            fail("file 为空", "(无)")
            continue
        if f in seen:
            fail("file 重复", f)
        seen.add(f)
        if not os.path.isfile(os.path.join(SCORES, f)):
            fail("file 不在 scores/ 里", f)
        if not (r.get("title") or "").strip():
            fail("title 为空", f)
        if r.get("status") not in ("ok", "ocr"):
            fail("status 不在白名单", "%s %s" % (f, r.get("status")))
        secs = r.get("sections") or []
        score = r.get("score") or ""
        if not secs:
            fail("sections 为空", f)
        else:
            joined = " | ".join(x.get("score") or "" for x in secs if x.get("score"))
            if joined != score:
                fail("sections 拼起来 != score", f)
        bars = [int(x) for x in (r.get("bars") or [])]
        nn = int(r.get("n_notes") or 0)
        for i in range(1, len(bars)):
            if bars[i] <= bars[i - 1]:
                fail("bars 有重复/非递增(空小节)",
                     "%s ... %s" % (f, bars[max(0, i - 2):i + 2]))
                break
        if bars and (bars[0] < 0 or bars[-1] > nn):
            fail("bars 越界", "%s 范围 %s..%s, n_notes=%d" % (f, bars[0], bars[-1], nn))

    if rows < MIN_ROWS:
        fail("行数太少", "%d < %d" % (rows, MIN_ROWS))

    print("data.jsonl %d 行" % rows)
    if not bad:
        print("产物断言全部通过 ✓")
        return 0
    print("!! 发现 %d 类问题:" % len(bad))
    for k, n in bad.most_common():
        print("   %-34s %5d" % (k, n))
        for d in ex[k]:
            print("        %s" % d)
    print("\n提示: 若 `bars` 有重复/非递增, 多半是 CI 走的内置兜底 `_FallbackJptok` 与")
    print("      jianpu2/skills/jianpu-melody-lookup/jptok.py **漂了**(见本文件头的事故说明)。")
    print("      先跑 `jianpu2/tools/check_jptok_parity.py` 把两份口径对齐, 再重建。")
    return 1


if __name__ == "__main__":
    if "--help" in sys.argv[1:]:
        print(__doc__)
        print("[guard] 这是 --help 守卫打出来的用法; 没有执行任何实际动作。")
        sys.exit(0)
    sys.exit(main())
