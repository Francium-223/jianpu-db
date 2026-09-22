# -*- coding: utf-8 -*-
"""量这个 skill 的检索指标: 从一段旋律片段能多准地找回原歌。

**口径（重要，先说清楚，免得数字好看但没意义）**

1. `Top-K`(主指标, 与 jianpu2 的 melody_retrieval_holdout.py 同口径):
   查询 = 从某首歌的**某一份谱**里截一段; 索引里**排除这份谱本身** -> 模拟"凭记忆哼"。
   **只有拥有 >=2 个版本的歌才能这样测**(只剩一份的歌, 排除后它就没了)。
   实测本库 6844 首歌里**只有 243 首有多版本**, 所以主指标的分母就是这 243 首——
   这点必须写明, 否则"Top1 xx%"会被误读成"全库准确率"。
2. `Top-K(全库口径)`: 不排除任何谱, 直接查。库里存着你查询的那份谱, 所以它会虚高;
   它的意义是"能定位到正确歌"的上界, 以及**查错时的兜底**(并列组大小)。
3. `并列下界`: 把与最优同分的歌全算错时还剩多少 —— 衡量"片段是否唯一"。

用法:
  py -3.13 eval_metric.py                    # 默认 200 查询 x (L=11/15) x (k=0/1)
  py -3.13 eval_metric.py --n 400 --lens 11,15,21
"""
import argparse
import json
import os
import random
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lookup import group_of, pitch_and_oct  # noqa: E402
from collections import Counter  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=os.path.join(HERE, "data.jsonl"))
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--lens", default="11,15")
    ap.add_argument("--errs", default="0,1")
    ap.add_argument("--seed", type=int, default=20260923)
    a = ap.parse_args()
    rnd = random.Random(a.seed)

    rows = [json.loads(l) for l in open(a.data, encoding="utf-8") if l.strip()]
    ent = []
    for r in rows:
        p, _ = pitch_and_oct(r.get("score"))
        if len(p) >= 24:
            ent.append((r, p))
    groups = {}
    for r, p in ent:
        groups.setdefault(group_of(r.get("title")), []).append((r, p))
    multi = {g: v for g, v in groups.items() if len(v) >= 2}
    arrs = {g: [(r, np.frombuffer(p.encode(), dtype=np.uint8)) for r, p in v] for g, v in groups.items()}
    print(f"库 {len(rows)} 份谱 / {len(groups)} 首歌; 其中**多版本** {len(multi)} 首 "
          f"(主指标的分母); 多版本歌的版本数分布 {dict(sorted(Counter(len(v) for v in multi.values()).items()))}")

    def candidate(g, exclude):
        """g 组的错音数 -> (min_err, tie_count)。exclude 为要排除的那份谱。"""
        best = None
        for r2, ar in arrs[g]:
            if r2 is exclude:
                continue
            if len(ar) < QL:
                continue
            w = np.lib.stride_tricks.sliding_window_view(ar, QL)
            m = int((w != qa).sum(axis=1).min())
            if best is None or m < best:
                best = m
        return best

    for L in [int(x) for x in a.lens.split(",")]:
        for k in [int(x) for x in a.errs.split(",")]:
            QL = L
            st = Counter()
            for _ in range(a.n):
                g = rnd.choice(sorted(multi))
                r0, p0 = rnd.choice(multi[g])
                if len(p0) < L:
                    continue
                i0 = rnd.randrange(0, len(p0) - L + 1)
                frag = list(p0[i0:i0 + L])
                for _x in range(k):                      # 改一个音为相邻音级(哼走音)
                    j = rnd.randrange(L)
                    d = int(frag[j])
                    cs = [x for x in (d - 1, d + 1) if 1 <= x <= 7]
                    if cs:
                        frag[j] = str(rnd.choice(cs))
                q = "".join(frag)
                qa = np.frombuffer(q.encode(), dtype=np.uint8)
                # 留一版本口径
                sc = []
                for g2 in arrs:
                    m = candidate(g2, r0)
                    if m is not None:
                        sc.append((m, g2))
                if not sc:
                    continue
                sc.sort(key=lambda x: x[0])
                top = sc[0][0]
                tied = [g2 for m, g2 in sc if m == top]
                st["n"] += 1
                ordr = [g2 for _, g2 in sc]
                if ordr[0] == g:
                    st["t1"] += 1
                if g in ordr[:3]:
                    st["t3"] += 1
                if g in ordr[:5]:
                    st["t5"] += 1
                if len(tied) == 1 and tied[0] == g:
                    st["lb"] += 1
                st["tie_sum"] += len(tied)
                # 全库口径(不排除任何谱)
                sc2 = []
                for g2 in arrs:
                    m = candidate(g2, None)
                    if m is not None:
                        sc2.append((m, g2))
                sc2.sort(key=lambda x: x[0])
                if sc2 and sc2[0][1] == g:
                    st["a1"] += 1
                if g in [x[1] for x in sc2[:5]]:
                    st["a5"] += 1
            n = st["n"]
            if not n:
                continue
            print(f"L={L:<3} 错音={k}  查询 {n:>4d}  |  留一版本: "
                  f"Top1 {st['t1']/n*100:>5.1f}%  Top3 {st['t3']/n*100:>5.1f}%  Top5 {st['t5']/n*100:>5.1f}%  "
                  f"并列下界 {st['lb']/n*100:>5.1f}%  并列组均值 {st['tie_sum']/n:>6.2f}"
                  f"  |  全库: Top1 {st['a1']/n*100:>5.1f}%  Top5 {st['a5']/n*100:>5.1f}%")


if __name__ == "__main__":
    main()
