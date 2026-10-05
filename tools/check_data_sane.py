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
  2. `bars` 的每个值都在 `0..有音高的音符数` 之间
  3. `sections` 拼起来 == `score`(逐字节)
  4. `file` 在 `scores/` 里真的存在、且不重复
  5. `title` 非空; `status` 在白名单 {ok, ocr, converted} 内
  6. 行数 >= 7000(整库缩水比个别行坏更严重)
只读, 不改任何东西。退出码 0 = 通过。

⚠ 2026-10-06 判据 2 的口径改了(原来比 `n_notes`, 现在比**有音高的音数**)。理由与"为什么
可以 import score"见 main() 里那段注释。这里只强调一句: **不再比 `n_notes`** ——
`n_notes` 是"token 数"(一条和弦算 1 个), 而 `bars` 是**逐音**推进的, 两者本来就不是一回事。
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
# `python tools/check_data_sane.py` 时 sys.path[0] 是 `tools/`, 不是仓库根 -> `import score`
# 会找不到(实测: `No module named 'score'`)。下面那个 import 就是靠这一行落地的。
if DB not in sys.path:
    sys.path.insert(0, DB)


def main():
    bad = collections.Counter()
    ex = collections.defaultdict(list)

    # 判据 2 的"有音高的音数"用**产生 bars 的那套 token 口径**算, 不自己写正则去数音。
    # 为什么可以在这里 import(本文件头写着"不依赖 jianpu2 / jptok"):
    #   · 两者都**没有**新依赖 —— `score.py` 与本文件同在一个仓库, 且它的 import 全部来自
    #     标准库(`schema` 也是本仓库的)。runner 只 checkout 本仓库也能 import 成功。
    #   · 它拿到的正是 CI 用的那份 token 口径: `score.py` 找不到兄弟 `jianpu2/` 时走内置兜底
    #     `_FallbackJptok`(CI 显式设 `JIANPU_ALLOW_FALLBACK_JTOK=1`)—— 也就是说这里算出来的
    #     音数**就是**重建 `data.jsonl` 时用的那一份, 不会出现"第三套正则"。
    #   · 需要的入口只有一个: `jptok.seq(score)`(整份谱 -> 有音高的音序列, 默认并连音线)。
    #     它由 `jianpu2/tools/check_jptok_parity.py` 拿全语料逐音证明与唯一实现一致。
    try:
        from score import jptok
    except Exception as e:                                          # noqa: BLE001
        print("!! 取不到 score.jptok, 无法按逐音口径判 bars 上界: %s" % e)
        return 1

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
        # converted: 2026-10-04 作者定的"由 ABC 等记谱格式**机械转换**而来(自动)", 与 midi 区分开
        # (它带完整音高记录)。2026-10-06 补齐: 作者当时同步了 `parse_scores.py` 的 OK_STATUS 与
        # `jianpu2/tools/check_corpus_invariants.py`, **漏了这里** —— 于是刚入库的 492 首
        # status=converted 会被判"不在白名单", CI 直接红、data.jsonl 不重出。三处口径必须一致。
        if r.get("status") not in ("ok", "ocr", "converted"):
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
        for i in range(1, len(bars)):
            if bars[i] <= bars[i - 1]:
                fail("bars 有重复/非递增(空小节)",
                     "%s ... %s" % (f, bars[max(0, i - 2):i + 2]))
                break
        # ⚠ 2026-10-06: 上界原来比 `n_notes`, 那是"**token** 数" —— 一条和弦 token 只算 1 个,
        #   而 `recover_bars` 2026-10-05 起**逐音**推进小节(见 score.py 里"和弦 token 要逐音推进"),
        #   于是 223 首含和弦的谱必然 `bars[-1] > n_notes`(实测刚入库的 492 首里红 24 首)。
        #   权威检查器 `check_corpus_invariants.py` 比的一直是 pitch 口径, 那 24 首在它那里是过的
        #   —— 也就是说这条判据是**比错了量**, 不是数据坏。改成与和弦口径一致: 比有音高的音数。
        #   `0`/`x`(休止/念白)不是有音高的音, 所以它们本来就不该推进小节。
        pitch = sum(1 for p in jptok.seq(score) if p[0] is not None)
        if bars and (bars[0] < 0 or bars[-1] > pitch):
            fail("bars 越界", "%s 范围 %s..%s, 有音高的音数=%d" % (f, bars[0], bars[-1], pitch))

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
    print("      (本脚本算 bars 上界用的 `jptok.seq` 就是这两份里 CI 实际走的那一份 ——")
    print("       所以上面这条提示同时覆盖'口径漂了'的两种情况: 重复线会漂、音数也会漂。)")
    return 1


if __name__ == "__main__":
    if "--help" in sys.argv[1:]:
        print(__doc__)
        print("[guard] 这是 --help 守卫打出来的用法; 没有执行任何实际动作。")
        sys.exit(0)
    sys.exit(main())
